# Classification CLI application

Classification application for Windows on Snapdragon® with [MobileNet-V2](https://aihub.qualcomm.com/compute/models/mobilenet_v2) using ONNX runtime.

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

Download the **float**/**onnx** variant of [MobileNet-V2](https://aihub.qualcomm.com/compute/models/mobilenet_v2) from AI Hub.
Rename it and place it into:
```
<project directory>/assets/models/classification.onnx
```

### Build project in Visual Studio 22

1. Open `Classification.sln`
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

3. Build and run project in Visual Studio

## Running App

### Running via Visual Studio

Visual Studio project is configured with the following command arguments:

```bash
--model .\assets\models\classification.onnx --image .\assets\images\keyboard.jpg
```

You can simply run the app from Visual Studio to run classification on sample image.

### Running app via CLI

```bash
.\ARM64\Debug\Classification.exe --model .\assets\models\classification.onnx --image .\assets\images\keyboard.jpg
```

You can additionally run `--help` to get more information about all available options:

```bash
.\ARM64\Debug\Classification.exe --help
```

Please refer to [QNN EP options](https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html#configuration-options) that can be provided as `--qnn_options` to the app.

### Sample Input

![sample_input](assets/images/keyboard.jpg)

### Sample Output

![sample_output](assets/images/classificationOutput.png)

## App and model details

1. Model input resolution: 224x224
    - If input image is of different shape, it's resized to 224x224
    - You can override model input dimensions if model uses different spatial image dimensions
2. App is built to work with post-processed outputs
    - App processes output logits and produces consumable output as Class Label.
    - If you want to try out any other model than Yolo (with post-processing included in model), please update output handling accordingly.

## FAQ

1. If you get a DLL error message upon launch (for instance that
   `opencv_core4d.dll` was not found). Try Build -> Clean Solution and
   re-build. If this still happens, please go over the NuGet and vcpkg
   instructions again carefully.
2. How do I use a model with different input shape than 224x224?
   - Use `--model_input_ht` / `--model_input_wt` to model input dimensions.
3. I have a model that does have different post-processing. Can I still use the app?
   - You will have to modify the app and add the necessary post-processing to accommodate that models.

## Project setup

Following section describes how to configure your own project with NuGet and vcpkg from scratch:

1. Start empty Visual Studio project
2. Set up NuGet to install ONNXRuntime QNN Execution provider
   - Go to `Project` -> `Manage NuGet Packages`
   - Look up and install the following packages
     - [Microsoft.ML.OnnxRuntime.QNN](https://www.nuget.org/packages/Microsoft.ML.OnnxRuntime.QNN)
   - This NuGet package does not properly copy all necessary files to the build
     folder, so we use a batch script
     [copy_missing_qnn_ep_files.bat](copy_missing_qnn_ep_files.bat) to do this
     for us. Copy this script into your project and make sure it runs by adding
         this to your `.vcxproj` file:
     ```
     <Target Name="PostBuildCopyQnn" AfterTargets="Build">
       <Exec Command="&quot;$(ProjectDir)copy_missing_qnn_ep_files.bat&quot; &quot;$(OutDir)&quot;" />
     </Target>
     ```
3. Set up Visual Studio for vcpkg
   - Enable vcpkg [manifest mode](https://learn.microsoft.com/en-us/vcpkg/concepts/manifest-mode)
      - Go to Project Setting
      - General -> vcpkg
      - Enable Manifest mode
   - Add `OpenCV` dependency in vcpkg
      - Run the following commands in Visual Studio powershell:

      ```bash
      vcpkg —new application
      vcpkg add port opencv
      ```
   - **Important**: To get around a vcpkg bug affecting ARM64, please add the
     following to your `.vcxproj` file:
     ```
     <PropertyGroup>
       <VcpkgPlatformTarget Condition="'$(Platform)'=='ARM64'">arm64</VcpkgPlatformTarget>
     </PropertyGroup>
     ```
     If this is not added, you will see an error message like this:
     ```
     error: Invalid triplet name. Triplet names are all lowercase alphanumeric+hyphens.
     ```
4. Now project is setup to work with the vcpkg and NuGet package managers
