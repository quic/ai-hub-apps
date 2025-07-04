# Object Detection CLI application

Object Detection application for Windows on Snapdragon® with [Yolo-v8](https://aihub.qualcomm.com/compute/models/yolov8_det) using ONNX runtime.

The app demonstrates how to use the [QNN execution provider](https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html) to accelerate the model using the Snapdragon® Neural Processing Unit (NPU).

## Requirements

### Platform

- Snapdragon® Platform (e.g. X Elite)
- Windows 11+

### Tools and SDK

- Visual Studio 22
  - Download any variant of [Visual Studio here](https://visualstudio.microsoft.com/vs/)
  - Make sure **Desktop development with C++ tools** are selected during installation or installed separately later

## Build App

### Downloading model from AI Hub

Download the **float**/**onnx** variant of [YOLO-X](https://aihub.qualcomm.com/compute/models/yolox) from AI Hub.
Rename it and place it into:
```
<project directory>/assets/models/detection.onnx
```

### Build project in Visual Studio 22

1. Open `ObjectDetection.sln`
2. Setting up dependencies
   - NuGet packages
     - NuGet packages should automatically restore in Visual Studio during build
     - If packages are not restored automatically, try the following:
       - If prompted by Visual Studio to `restore` NuGet packages
         - Click on `restore` to restore all `NuGet` packages
       - Otherwise,
         - Go to `Project -> Manage NuGet packages` in Visual studio
         - Install [ONNX-Runtime-QNN](https://www.nuget.org/packages/Microsoft.ML.OnnxRuntime.QNN) 1.19.0

   - vcpkg packages
     - Project is configured to work with vcpkg in [manifest mode](https://learn.microsoft.com/en-us/vcpkg/concepts/manifest-mode)
     - If opencv headers are missing, vcpkg is not setup correctly.
     - [Integrate vcpkg]((https://learn.microsoft.com/en-us/vcpkg/commands/integrate#vcpkg-integrate-install)) with Visual Studio:
         - Go to `View -> Terminal` in Visual studio
         - Run the following command in terminal

         ```bash
         vcpkg integrate install
         ```

3. Build project in Visual Studio

## Running App

### Running via Visual Studio

Visual studio project is configured with the following command arguments:

```bash
--model .\assets\models\detection.onnx --image .\assets\images\kitchen.jpg
```

You can simply run the app from Visual Studio to run object detection on sample image.

### Running app via CLI

```bash
.\ARM64\Debug\ObjectDetection.exe --model .\assets\models\detection.onnx --image .\assets\images\kitchen.jpg
```

You can additionally run `--help` to get more information about all available options:

```bash
.\ARM64\Debug\ObjectDetection.exe --help
```

Please refer to [QNN EP options](https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html#configuration-options) that can be provided as `--qnn_options` to the app.

### Sample Input

![sample_input](assets/images/kitchen.jpg)

### Sample Output

![sample_output](assets/images/sample_outputs/kitchen_output.jpg)

## App and model details

1. Model input resolution: 640x640
    - If input image is of different shape, it's resized to 640x640
    - You can override model input dimensions if model uses different spatial image dimensions
2. App is built to work with post-processed outputs
    - App processes output logits and produces consumable output as follows:
        - Output boxes
        - Output scores
        - Output labels
    - If you want to try out any other model than Yolo (with post-processing included in model), please update output handling accordingly.

## FAQ

1. If you get a DLL error message upon launch (for instance that
   `opencv_core4d.dll` was not found). Try Build -> Clean Solution and
   re-build. If this still happens, please go over the NuGet and vcpkg
   instructions again carefully.
2. How do I use a model with different input shape than 640x640?
   - Use `--model_input_ht` / `--model_input_wt` to model input dimensions.
3. I have a model that does not have post-processing embedded into the model. Can I still use the app?
   - You will have to modify the app and add the necessary post-processing to accommodate that models.

## Project setup

Please see the [Classification app](../Classification/README.md) for
instructions of how to set up a project with ONNXRuntime QNN Execution Provider
from scratch.
