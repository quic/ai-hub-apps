# CLI Chat application

Chat application for Windows on Snapdragon® with [Llama 2](https://aihub.qualcomm.com/compute/models/llama_v2_7b_chat_quantized) using Genie SDK.

The app demonstrates how to use the Genie APIs from [QNN SDK](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct) to run and accelerate LLMs using the Snapdragon® Neural Processing Unit (NPU).

## Requirements

### Platform

- Snapdragon® Platform (e.g. X Elite)
- Windows 11+

### Tools and SDK

- Visual Studio 22
  - Download any variant of [Visual Studio here](https://visualstudio.microsoft.com/vs/)
  - Make sure Desktop development with C++ tools are selected during installation or installed separately later
- QNN SDK: [Qualcomm AI Engine Direct](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct)
  - Refer to [Setup QNN SDK](#setup-qnn-sdk) to install compatible QNN SDK for models downloaded from AI Hub.

## Build App

### Downloading models from AI Hub

1. Please follow the instructions from [Llama2 from AI Hub Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models/llama_v2_7b_chat_quantized/gen_ondevice_llama) to generate models and assets required by ChatApp
2. Copy assets to target device (e.g., Snapdragon® based Windows)

NOTE: This process takes a long time e.g. ~2 hours to export models, ~2 hours to build QNN binaries to run on-device.

### Setup QNN SDK

Please ensure that the QNN SDK version installed on the system is the same as the one used by AI Hub for generating QNN context binaries.
You can find the AI Hub QNN version in the compile job page as shown in the following screenshot:

![QNN version on AI Hub](assets/images/ai-hub-qnn-version.png)

Having different QNN versions could result in runtime or load-time failures.

Please follow the following steps to configure QNN SDKs for ChatApp:

1. Download and install [Qualcomm AI Engine Direct](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct)
2. Set global environment variable `QNN_SDK_ROOT` to root path of QNN SDK e.g. `C:\Qualcomm\AIStack\QAIRT\2.26.0.240828`

    - Make sure you can run the following command with no error and that it prints the various libraries available with your QNN package:

    ```powershell
    ls ${env:QNN_SDK_ROOT}/lib
    ```

    ![QNN SDK Verion check](assets/images/sample-qnn-sdk-check.png)
3. If command from step 2 succeeds, QNN SDK is correctly configured to work with ChatApp.


### Build project in Visual Studio 22

Make sure `QNN_SDK_ROOT` is set globally pointing to QNN SDK before you build the project.

1. Open `ChatApp.sln`
2. Build project in Visual Studio
   - It takes around 2 mins to build on X Elite.

## Running App

### Providing local paths

Make sure to provide paths to local config file and models using `\\` or `/` as a path separator and not `\`


#### Correct file path examples

```powershell
1. C:\\Path\\To\\Model\\Config\\llama2_7b.json
2. C:/Path/To/Model/Config/llama2_7b.json
```

#### Incorrect file path example

```powershell
1. C:\Path\To\Model\Config\llama2_7b.json
```

### Running app via CLI

```powershell
cd {Project directory}
.\ARM64\Debug\ChatApp.exe --model_config .\\assets\\configs\\genie\\llama2_7b.json --htp_config .\\assets\\configs\\htp_backend_ext\\v73.json --tokenizer .\\assets\\configs\\tokenizer\\llama2_7b.json --models {Directory path with models and htp-extension-config downloaded from AI Hub}
```

You can additionally run `--help` to get more information about all available options:

```powershell
.\ARM64\Debug\ChatApp.exe --help
```

### Running via Visual Studio

Visual studio project is configured with the following command arguments:

```powershell
--model_config .\\assets\\configs\\genie\\llama2_7b.json --htp_config .\\assets\\configs\\htp_backend_ext\\v73.json --tokenizer .\\assets\\configs\\tokenizer\\llama2_7b.json --models {Directory path with models and htp-extension-config downloaded from AI Hub}
```

### Sample Output

![sample_output](assets/images/sample_output.png)
