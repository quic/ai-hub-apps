## Run Stable Diffusion on Snapdragon X Elite

Follow instructions to run the demo:

1. Download ONNX model files from https://aihub.qualcomm.com/models/stable_diffusion_v2_1_quantized:
    * Unzip each file.
    * Move each file to `.\models`
    * Rename each FOLDER to `text_encoder.onnx`, `unet.onnx`, and `vae_decoder.onnx`, respectively.

In the end, your `.\models` folder should look like this:
```
models\
  text_encoder.onnx\
    model.bin
    model.onnx
  unet.onnx\
     model.bin
     model.onnx
  vae_decoder.onnx\
     model.bin
     model.onnx
```

2. Enable PowerShell Scripts. Open PowerShell in administrator mode, and run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force
```

3. Open Anaconda PowerShell Prompt in this folder. If you don't have Anaconda PowerShell, use regular PowerShell.

4. Install platform dependencies:

```powershell
..\install_platform_deps.ps1
```

The above script will install:
  * Anaconda for x86-64. We use x86-64 Python for compatibility with other Python packages. However, inference in ONNX Runtime will, for the most part, run natively with ARM64 code.
  * Git for Windows. This is required to load the AI Hub Models package, which contains the application code used by this demo.

5. Open (or re-open) Anaconda Powershell Prompt to continue.

6. Create & activate your python environment:

```powershell
..\activate_venv.ps1 -name AI_Hub
```

7. Install python packages:

```powershell
..\install_python_deps.ps1 -model stable-diffusion-v2-1-quantized
```

In your currently active python environment, the above script will install:
  * AI Hub Models and model dependencies for stable diffusion.
  * The onnxruntime-qnn package, both to enable native ARM64 ONNX inference, as well as to enable targeting Qualcomm NPUs.

8. Run demo:

```powershell
python demo.py --prompt "A girl taking a walk at sunset" --num-steps 20
```
