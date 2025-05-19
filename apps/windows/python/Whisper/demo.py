# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import argparse
from datetime import datetime

import sounddevice as sd
from qai_hub_models.models._shared.whisper.app import WhisperApp
from qai_hub_models.utils.onnx_torch_wrapper import OnnxModelTorchWrapper


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
        default="build\\whisper_base_en\\WhisperEncoderInf.onnx",
        help="Encoder model path",
    )
    parser.add_argument(
        "--decoder-path",
        type=str,
        default="build\\whisper_base_en\\WhisperDecoderInf.onnx",
        help="Decoder model path",
    )
    args = parser.parse_args()

    if args.list_audio_devices:
        print(sd.query_devices())
        return

    print("Loading model...")
    app = WhisperApp(
        OnnxModelTorchWrapper.OnNPU(args.encoder_path),
        OnnxModelTorchWrapper.OnNPU(args.decoder_path),
        num_decoder_blocks=6,
        num_decoder_heads=8,
        attention_dim=512,
        mean_decode_len=224,
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
