## Run Whisper on Snapdragon X Elite

Follow instructions to run the demo:

1. Enable PowerShell Scripts. Open PowerShell in administrator mode, and run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force
```

2. Open Anaconda PowerShell Prompt in this folder. If you don't have Anaconda PowerShell, use regular PowerShell.

3. Install platform dependencies:

```powershell
..\install_platform_deps.ps1 -extra_pkgs ffmpeg
```

The above script will install:
  * Anaconda for x86-64. We use x86-64 Python for compatibility with other Python packages. However, inference in ONNX Runtime will, for the most part, run natively with ARM64 code.
  * Git for Windows. This is required to load the AI Hub Models package, which contains the application code used by this demo.
  * ffmpeg for reading audio files (Note that as of writing this, WinGet does not have an ARM64 distribution of ffmpeg. You will install a slower emulated x86-64 ffmpeg distribution instead.)

4. Open (or re-open) Anaconda Powershell Prompt to continue.

5. Create & activate your python environment:

```powershell
..\activate_venv.ps1 -name AI_Hub
```

6. Install python packages:

```powershell
..\install_python_deps.ps1 -model whisper-base-en
```

In your currently active python environment, the above script will install:
  * AI Hub Models and dependencies for whisper.
  * The onnxruntime-qnn package, both to enable native ARM64 ONNX inference, as well as to enable targeting Qualcomm NPUs.

7. Export model:

```powershell
python -m qai_hub_models.models.whisper_base_en.export --target-runtime onnx --device "Snapdragon X Elite CRD" --skip-profiling --skip-inferencing
```

8. Get microphone device number:

```powershell
python demo.py --list-audio-devices
```

9. Stream whisper from your microphone:

```powershell
python demo.py --stream-audio-device <device_number>
```
