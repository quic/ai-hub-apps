# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import argparse
from datetime import datetime

from qai_hub_models.models.whisper_base_en import App as WhisperApp
from whisper_model_onnx import WhisperBaseEnONNX


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler="error",
    )
    parser.add_argument(
        "--audio_path",
        type=str,
        required=True,
        help="Path to audio file that needs to be tested. Only .mp3 are supported.",
    )
    args = parser.parse_args()
    # Input files
    encoder_path = "build/whisper_base_en_WhisperEncoder.onnx"
    decoder_path = "build/whisper_base_en_WhisperDecoder.onnx"

    # Load whisper model
    print("Loading model...")
    whisper = WhisperApp(WhisperBaseEnONNX(encoder_path, decoder_path))

    # Execute Whisper Model
    print("Before transcription: " + str(datetime.now().astimezone()))
    text = whisper.transcribe(args.audio_path)
    print("After transcription: " + str(datetime.now().astimezone()))
    with open("transcript.txt", "w") as file:
        file.write(text)
    print("After writing file: " + str(datetime.now().astimezone()))


if __name__ == "__main__":
    main()
