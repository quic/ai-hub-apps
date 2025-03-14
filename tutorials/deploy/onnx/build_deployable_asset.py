# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import argparse

import numpy as np
import onnx
import onnx_graphsurgeon as gs
from onnx_graphsurgeon.ir.tensor import Tensor


def _natively_quantize_tensor(
    variable: Tensor,
    scales: np.ndarray,
    zero_points: np.ndarray,
    dtype: np.dtype,
    axis: int,
    name: str,
):
    rank = len(variable.shape)
    iinfo = np.iinfo(dtype)

    if rank == 0:
        w_unclipped = (
            np.round(
                np.array(variable.values).astype(np.float64) / scales.astype(np.float64)
            ).astype(np.int64)
            + zero_points
        )
        return np.array(w_unclipped.clip(iinfo.min, iinfo.max).astype(dtype))
    axis = axis % rank
    trailing_ones = rank - axis - 1
    broadcast_shape = (-1,) + (1,) * trailing_ones
    scales_fullrank = scales.reshape(broadcast_shape)
    zero_points_fullrank = zero_points.reshape(broadcast_shape)
    w_unclipped = (
        np.round(
            variable.values.astype(np.float64) / scales_fullrank.astype(np.float64)
        ).astype(np.int64)
        + zero_points_fullrank
    )

    w_unclipped_min = w_unclipped.min()
    w_unclipped_max = w_unclipped.max()
    if w_unclipped_min < iinfo.min or iinfo.max < w_unclipped_max:

        print(
            f"Parameter {name} in quantized range [{w_unclipped.min()}, {w_unclipped.max()}] is being clipped to [{iinfo.min}, {iinfo.max}]; this may result in accuracy loss."
        )

    w = w_unclipped.clip(iinfo.min, iinfo.max).astype(dtype)
    return w


def convert_to_deployable_onnx(onnx_filepath: str):
    """
    Converts an ONNX graph (QDQ format with weights are stored as float 32) to ONNX graph where all the quantization is applied.
    The nodes in input graph look like:
        Constant weights (FP) -> Q -> DQ
    The nodes in output graph:
        Constant weights (INT) -> DQ
    """

    onnx_model = onnx.load(onnx_filepath)
    graph = gs.import_onnx(onnx_model)
    b_quantized_dtype = np.dtype("int32")
    unquantized_dtype = np.dtype("float32")

    for node in graph.nodes:
        bias_present = (
            node.op in ["Gemm", "Conv", "TransposeConv"] and len(node.inputs) == 3
        )
        for inputs in node.inputs:
            for dequantized_node in inputs.inputs:
                if (
                    dequantized_node.op == "DequantizeLinear"
                    and len(dequantized_node.inputs[0].inputs) > 0
                    and dequantized_node.i(0, 0).op == "QuantizeLinear"
                    and isinstance(dequantized_node.i(0, 0).inputs[0], gs.Constant)
                ):

                    quantize_node = dequantized_node.i(0, 0)

                    scales_w = quantize_node.inputs[1].values
                    bitwidth = dequantized_node.inputs[2].dtype

                    zero_points_w = np.array(
                        quantize_node.inputs[2].values,
                        dtype=bitwidth,
                    )

                    weights_data = quantize_node.inputs[0]

                    quantized_weight = _natively_quantize_tensor(
                        weights_data,
                        scales_w,
                        zero_points_w,
                        dtype=bitwidth,
                        axis=dequantized_node.attrs.get("axis", 0),
                        name=node.name,
                    )

                    # Add new information to dequantize linear
                    dequantized_node.inputs[0] = gs.Constant(
                        dequantized_node.inputs[0].name + "_folded",
                        quantized_weight,
                    )
                    print(f"Applied quantization for node {node.name}")

                    # Only applicable when bias is present
                    if (
                        bias_present
                        and node.inputs[0].inputs[0].op == "DequantizeLinear"
                        and len(node.inputs[0].inputs[0].inputs) > 2
                    ):

                        bias_var = node.inputs[2]

                        # Scale of bias is product of scale of weights and inputs
                        input_scales = node.i(0, 0).inputs[1].values

                        scales_b = np.array(input_scales * scales_w)
                        zero_points_b = np.full(scales_b.shape, 0).astype(
                            b_quantized_dtype
                        )
                        # Quantize the bias
                        quantized_bias = _natively_quantize_tensor(
                            bias_var,
                            scales_b,
                            zero_points_b,
                            dtype=b_quantized_dtype,
                            axis=node.attrs.get("axis", 0),
                            name=node.name,
                        )
                        dq_node_name = dequantized_node.inputs[0].name + "_b_folded"
                        d_bias = gs.Constant(dq_node_name, quantized_bias)

                        # Add dequantize linear node
                        dq_b_scales = gs.Constant(bias_var.name + "_scales", scales_b)
                        dq_b_zero_points = gs.Constant(
                            bias_var.name + "_zero_points", zero_points_b
                        )
                        dq_y = gs.Variable(
                            bias_var.name + "_dq",
                            dtype=unquantized_dtype,
                            shape=bias_var.shape,
                        )

                        node.inputs[2] = dq_y
                        dq = gs.Node(
                            op="DequantizeLinear",
                            inputs=[d_bias, dq_b_scales, dq_b_zero_points],
                            outputs=[dq_y],
                            attrs=dequantized_node.attrs,
                        )
                        graph.nodes.append(dq)

    # Graph cleanup removes all dangling nodes
    # Toplogical sort is needed by ORT
    graph.cleanup().toposort()
    model = gs.export_onnx(graph)

    # Save the modified graph in filepath.
    onnx.save(model, onnx_filepath)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Convert to deployable ONNX asset (QDQ that maps to QOp representation)"
    )
    parser.add_argument("-f", "--onnx_file", required=True)
    args = parser.parse_args()
    convert_to_deployable_onnx(args.onnx_file)
