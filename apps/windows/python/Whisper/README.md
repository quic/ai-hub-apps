## Run Whisper on Snapdragon X Elite

Follow instructions to run the demo:

1. Download & [Install Python (x86)](https://www.python.org) and add it to your system path.

2. Download & Install [Git for Windows](https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.1/Git-2.45.2-64-bit.exe) and add it to your system path.

3. Download & Extract [FFMPeg for Windows](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) and add it to your system path.

4. Install dependencies by running `python -m pip install -r requirements.txt`

5. From this folder, run `python -m qai_hub_models.models.whisper_base_en.export --target-runtime onnx`

6. Run demo `python demo.py --audio_path /path/to/test/data.mp3`
