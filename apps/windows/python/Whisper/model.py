# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import numpy as np
import onnxruntime
from qai_hub_models.models._shared.whisper.model import Whisper


def get_onnxruntime_session_with_qnn_ep(path):
    options = onnxruntime.SessionOptions()
    session = onnxruntime.InferenceSession(
        path,
        sess_options=options,
        providers=["QNNExecutionProvider"],
        provider_options=[
            {
                "backend_path": "QnnHtp.dll",
                "htp_performance_mode": "burst",
                "high_power_saver": "sustained_high_performance",
                "enable_htp_fp16_precision": "1",
                "htp_graph_finalization_optimization_mode": "3",
            }
        ],
    )
    return session


class ONNXEncoderWrapper:
    def __init__(self, encoder_path):
        self.session = get_onnxruntime_session_with_qnn_ep(encoder_path)

    def to(self, *args):
        return self

    def __call__(self, audio):
        return self.session.run(None, {"audio": audio})


class ONNXDecoderWrapper:
    def __init__(self, decoder_path):
        self.session = get_onnxruntime_session_with_qnn_ep(decoder_path)

    def to(self, *args):
        return self

    def __call__(
        self, x, index, k_cache_cross, v_cache_cross, k_cache_self, v_cache_self
    ):
        return self.session.run(
            None,
            {
                "x": x.astype(np.int32),
                "index": np.array(index),
                "k_cache_cross": k_cache_cross,
                "v_cache_cross": v_cache_cross,
                "k_cache_self": k_cache_self,
                "v_cache_self": v_cache_self,
            },
        )


class WhisperBaseEnONNX(Whisper):
    def __init__(self, encoder_path, decoder_path):
        return super().__init__(
            ONNXEncoderWrapper(encoder_path),
            ONNXDecoderWrapper(decoder_path),
            num_decoder_blocks=6,
            num_heads=8,
            attention_dim=512,
        )
