# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import argparse

import numpy as np
from diffusers import EulerDiscreteScheduler
from PIL import Image
from qai_hub_models.models._shared.stable_diffusion.app import StableDiffusionApp
from qai_hub_models.utils.args import add_output_dir_arg
from qai_hub_models.utils.display import display_or_save_image, to_uint8
from qai_hub_models.utils.onnx_torch_wrapper import (
    OnnxModelTorchWrapper,
    OnnxSessionOptions,
)
from transformers import CLIPTokenizer

DEFAULT_PROMPT = "A girl taking a walk at sunset"
HF_REPO = "stabilityai/stable-diffusion-2-1-base"


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler="error",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=DEFAULT_PROMPT,
        help="Prompt for stable diffusion",
    )
    parser.add_argument(
        "--num-steps",
        type=int,
        default=20,
        help="Number of diffusion steps",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random generator seed",
    )
    parser.add_argument(
        "--text-encoder",
        type=str,
        default="models\\text_encoder.onnx\\model.onnx",
        help="Text Encoder ONNX model path",
    )
    parser.add_argument(
        "--unet",
        type=str,
        default="models\\unet.onnx\\model.onnx",
        help="UNET ONNX model path",
    )
    parser.add_argument(
        "--vae-decoder",
        type=str,
        default="models\\vae_decoder.onnx\\model.onnx",
        help="VAE Decoder ONNX model path",
    )
    add_output_dir_arg(parser)
    args = parser.parse_args()

    # Disable compile caching becuase Stable Diffusion is Pre-Compiled
    # This is needed due to a bug in onnxruntime 1.22, and can be removed after the next ORT release.
    options = OnnxSessionOptions.aihub_defaults()
    options.context_enable = False

    # Load model
    print("Loading model and app...")
    sdapp = StableDiffusionApp(
        OnnxModelTorchWrapper.OnNPU(args.text_encoder, options),
        OnnxModelTorchWrapper.OnNPU(args.vae_decoder, options),
        OnnxModelTorchWrapper.OnNPU(args.unet, options),
        CLIPTokenizer.from_pretrained(HF_REPO, subfolder="tokenizer"),
        EulerDiscreteScheduler.from_pretrained(HF_REPO, subfolder="scheduler"),
        channel_last_latent=True,
    )

    # Generate image
    print("Generating image...")
    image = sdapp.generate_image(args.prompt, args.num_steps, args.seed)
    pil_img = Image.fromarray(to_uint8(np.asarray(image))[0])
    display_or_save_image(pil_img, args.output_dir)


if __name__ == "__main__":
    main()
