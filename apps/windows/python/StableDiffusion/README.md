## Run Stable Diffusion on Snapdragon X Elite

Follow instructions to run the demo:

1. Enable PowerShell Scripts. Open PowerShell in administrator mode, and run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser Unrestricted -Force
```

2. Open Anaconda PowerShell Prompt in this folder. If you don't have Anaconda PowerShell, use regular PowerShell.

3. Install platform dependencies:

```powershell
..\install_platform_deps.ps1
```

The above script will install:
  * Anaconda for x86-64. We use x86-64 Python for compatibility with other Python packages. However, inference in ONNX Runtime will, for the most part, run natively with ARM64 code.
  * Git for Windows. This is required to load the AI Hub Models package, which contains the application code used by this demo.

4. Open (or re-open) Anaconda Powershell Prompt to continue.

5. Create & activate your python environment:

```powershell
..\activate_venv.ps1 -name AI_Hub
```

6. Install python packages:

```powershell
..\install_python_deps.ps1 -model stable-diffusion-v2-1
```

In your currently active python environment, the above script will install:
  * AI Hub Models and model dependencies for stable diffusion.
  * The onnxruntime-qnn package, both to enable native ARM64 ONNX inference, as well as to enable targeting Qualcomm NPUs.

7. Export model:

```powershell
python -m qai_hub_models.models.stable_diffusion_v2_1.export --target-runtime precompiled_qnn_onnx --device "Snapdragon X Elite CRD" --fetch-static-assets v0.36.0
# WARNING: Do not rename `model.bin` files. This will break the demo.
Expand-Archive -Path .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\Stable-Diffusion-v2.1_text_encoder_w8a16.onnx.zip -DestinationPath .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite
mv .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\model.onnx .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\text_encoder.onnx
Expand-Archive -Path .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\Stable-Diffusion-v2.1_unet_w8a16.onnx.zip -DestinationPath .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite
mv .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\model.onnx .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\unet.onnx
Expand-Archive -Path .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\Stable-Diffusion-v2.1_vae_w8a16.onnx.zip -DestinationPath .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite
mv .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\model.onnx .\build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\vae_decoder.onnx
```

In the end, your `.\build` folder should look like this:
```
build\stable_diffusion_v2_1\precompiled\qualcomm-snapdragon-x-elite\
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



8. Run demo:

```powershell
python demo.py --prompt "A girl taking a walk at sunset" --num-steps 20
```
