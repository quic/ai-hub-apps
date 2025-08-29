# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import argparse
from datetime import datetime

import sounddevice as sd
from qai_hub_models.models._shared.hf_whisper.app import HfWhisperApp
from qai_hub_models.utils.onnx_torch_wrapper import (
    OnnxModelTorchWrapper,
    OnnxSessionOptions,
)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler="error",
    )
    parser.add_argument(
        "--audio-file",
        type=str,
        default=None,
        help="Audio file path or URL",
    )
    parser.add_argument(
        "--stream-audio-device",
        type=int,
        default=None,
        help="Audio device (number) to stream from.",
    )
    parser.add_argument(
        "--stream-audio-chunk-size",
        type=int,
        default=10,
        help="For audio streaming, the number of seconds to record between each transcription attempt. A minimum of around 10 seconds is recommended for best accuracy.",
    )
    parser.add_argument(
        "--list-audio-devices",
        action="store_true",
        help="Pass this to list audio devices and exit.",
    )
    parser.add_argument(
        "--encoder-path",
        type=str,
        default="build\\whisper_base\\HfWhisperEncoder\\model.onnx",
        help="Encoder model path",
    )
    parser.add_argument(
        "--decoder-path",
        type=str,
        default="build\\whisper_base\\HfWhisperDecoder\\model.onnx",
        help="Decoder model path",
    )
    parser.add_argument(
        "--model-size",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v3-turbo"],
        help="Size of the model being run, corresponding to a specific model checkpoint on huggingface.",
    )
    args = parser.parse_args()

    if args.list_audio_devices:
        print(sd.query_devices())
        return

    # Disable compile caching becuase Stable Diffusion is Pre-Compiled
    # This is needed due to a bug in onnxruntime 1.22, and can be removed after the next ORT release.
    options = OnnxSessionOptions.aihub_defaults()
    options.context_enable = False

    print("Loading model...")
    app = HfWhisperApp(
        OnnxModelTorchWrapper.OnNPU(args.encoder_path),
        OnnxModelTorchWrapper.OnNPU(args.decoder_path),
        f"openai/whisper-{args.model_size}",
    )

    if args.stream_audio_device:
        app.stream(args.stream_audio_device, args.stream_audio_chunk_size)
    else:
        audio = args.audio_file
        assert (
            audio is not None
        ), "No audio file selected. Pass --audio-file or stream from a microphone using --stream-audio-device"

        # Perform transcription
        print("Before transcription: " + str(datetime.now().astimezone()))
        transcription = app.transcribe(audio)
        print(f"Transcription: {transcription}")
        print("After transcription: " + str(datetime.now().astimezone()))


if __name__ == "__main__":
    main()
