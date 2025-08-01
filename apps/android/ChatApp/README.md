[![Qualcomm® AI Hub Apps](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/quic-logo.jpg)](https://aihub.qualcomm.com)

# Sample Chat App

Chat application for Android on Snapdragon® with LLMs from [Qualcomm® AI Hub Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models) using Genie SDK.

The app demonstrates how to use the Genie C++ APIs from [QAIRT SDK](https://qpm.qualcomm.com/#/main/tools/details/Qualcomm_AI_Runtime_SDK) to run and accelerate LLMs using the Snapdragon® Neural Processing Unit (NPU).

## Current limitations on running ChatApp

:warning: This demo app **does not work on all** the consumer devices with Android 14.

Genie SDK requires newer meta-build to run LLMs on-device. Depending on which meta-build is picked by your phone vendor, this feature may or may not work.

We recommend using a device from [QDC](https://qdc.qualcomm.com/) for rest of this demo to run models on-device.
Android devices on QDC have newer meta-build and can run this demo on Android 14+.

We have verified sample ChatApp for the following device:

| Device name | QAIRT version | OS | Build Version |
| --- | --- | --- | --- |
| Samsung Galaxy S24 Plus  | 2.29.0 | One UI 6.1 (Android 14) | UP1A.231005.007.S926U1UEU4AXK4 |
| Samsung Galaxy S25 Ultra | 2.33.0 | One UI 7.0 (Android 15) | AP3A.240905.015.A2.S938U1UEU1AYA1 |

If you have a device listed in the above table, you can update OS to above mentioned or newer OS to run Sample App locally.

If your device is not listed above, we request to try this app on your device and share your feedback as a comment on [this issue](https://github.com/quic/ai-hub-apps/issues/29).

We are looking forward for community contributions for trying out this app on different devices and keep this information up-to-date.

## Demo

https://github.com/user-attachments/assets/7b23c632-cc4e-48ed-b1df-ea98ec0f51b7

## Requirements

### Platform

- Snapdragon® Gen 3 or Snapdragon® 8 Elite
- Or access to Android device on [QDC](https://qdc.qualcomm.com/)
- The host computer can run Windows, Linux, or macOS.

### Tools and SDK

1. Clone this repository **with [Git-LFS](https://git-lfs.com) enabled.**
2. Download [Android Studio](https://developer.android.com/studio). **Version 2024.3.1 or newer** is required.
3. Install AI Hub and AI Hub models.

    ```bash
    pip install qai-hub
    pip install "qai-hub-models[llama-v3-2-3b-instruct]"
    ```

    - This Android ChatApp works with Llama 3.2 3B out of the box. It also works with other LLMs in AI Hub Models. Go to the README of the LLM of your choice in [Qualcomm® AI Hub Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models) to learn how to install it.

4. Download and extract QAIRT SDK compatible with sample app:

We recommend using same QAIRT SDK (also "QNN SDK" for older versions) version as the one used by AI Hub for generating QNN context binaries.
You can find the AI Hub QAIRT version in the compile job page as shown in the following screenshot:

![QNN version on AI Hub](assets/ai-hub-qnn-version.png)

Having different QAIRT versions could result in runtime or load-time failures.

Follow these steps to configure QAIRT SDKs for ChatApp:

- Download and extract [Qualcomm® AI Runtime SDK](https://qpm.qualcomm.com/#/main/tools/details/Qualcomm_AI_Runtime_SDK) (see [QNN SDK](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct) for older versions) for Linux.

- If you are using macOS, then we recommend using [Docker](https://www.docker.com/) to install `qpm-cli` to extract `.qik` file.

- If successful, you will see a message like

    ```bash
    SUCCESS: Installed qualcomm_ai_engine_direct.Core at /opt/qcom/aistack/qairt/<version>
    ```

## Build App

1. Go to ChatApp directory

```bash
cd <ai-hub-apps-repo-root>/apps/android/ChatApp/
```

2. Get QNN context binaries for the LLM of your choice from Qualcomm AI Hub. There are two ways to get these assets:

    - Run export script to get context binaries for Llama variants. We will export these models with context length 4096 by default. You can add the argument --context-length with your desired context length value while exporting the model for modifying (recommended to use lower or equal to 4096). Make sure the size option in the genie config matches your model's context length.

    - Download directly from our website. Make sure to select the correct device when downloading the context binaries.

    - Read more about [exporting LLMs via AI Hub here](https://github.com/quic/ai-hub-apps/tree/main/tutorials/llm_on_genie#1-generate-genie-compatible-qnn-binaries-from-ai-hub)
        - You'll have to replace model name from the above tutorial with `llama_v3_2_3b_instruct` or the model id of your choice and reduce context length for this demo when exporting.

    - The following command exports Llama 3.2 3B model with context length 4096:

    ```bash
    python -m qai_hub_models.models.llama_v3_2_3b_instruct.export --device "Snapdragon 8 Elite QRD" --output-dir genie_bundle --skip-profiling --skip-inferencing
    ```

    - Exporting Llama 3.2 models will take a while depending on your internet connectivity.
    - This takes around 1-2 hours with good internet connectivity.

3. Navigate to `src/main/assets/models/llm` and use this directory to store the assets.

    - Download and save `tokenizer.json` from the [LLM On-Device Deployment](https://github.com/quic/ai-hub-apps/tree/main/tutorials/llm_on_genie#genie-config) tutorial to `src/main/assets/models/llm/`.

    -  If you would like, you may also go to the [HuggingFace](https://huggingface.co/) repository of your desired model and save `tokenizer.json` from there.

4. Copy model binaries (`genie_bundle/*.bin`) from step 1 to `src/main/assets/models/llm/`

    ```bash
    cp genie_bundle/*.bin src/main/assets/models/llm/
    ```

5. If your model is not Llama 3.2 3B, you do not need to modify the HTP config, but the `genie_config.json` will need to be updated to support the model of your choice. Use the Prepare Genie Configs section of the [LLM On-Device Deployment tutorial](https://github.com/quic/ai-hub-apps/tree/main/tutorials/llm_on_genie#prepare-genie-configs) to access the correct `genie_config.json`.

    - Replace the tokenizer path with a placeholder. It may look like this:

        ```code
        "path": "<tokenizer_path>"
        ```

    - Replace the HTP config path with a placeholder. It may look like this:

        ```code
        "extensions": "<htp_backend_ext_path>"
        ```

    - Replace the context binary paths with placeholders. It may look like this but will differ depending on the model and number of binaries generated:

        ```code
        "ctx-bins": [
                "<models_path>/weight_sharing_model_1_of_4.serialized.bin",
                "<models_path>/weight_sharing_model_2_of_4.serialized.bin",
                "<models_path>/weight_sharing_model_3_of_4.serialized.bin",
                "<models_path>/weight_sharing_model_4_of_4.serialized.bin"
            ]
        ```

    - These placeholders will be resolved by the app and are important so that the Android app can locate your files on device.

    - If your model is Llama 3.2 3B, you do not need to set up the `genie_config.json` and the HTP config. These files are already set up for you.

6. Update the text in `apps/android/ChatApp/src/main/res/values/strings.xml` to display the model you would like to chat with in the application. If you are using Llama 3.2 3B, it may look like this:

    ```code
    <string name="chat_with_llm">Chat with Llama 3.2 3B</string>
    ```

    - If you are using a model that is not one of the Llama 3 models, you will have to update the prompt format in `PromptHandler.cpp` first. Check out the Prompt Formats section in the [LLM On-Device Deployment tutorial](https://github.com/quic/ai-hub-apps/tree/main/tutorials/llm_on_genie#prompt-formats) to learn more.

7. Update `<ai-hub-apps-repo-root>/apps/android/ChatApp/build.gradle` with path to QNN SDK root directory. If you are on QNN version 2.28.2 and have extracted to the default location on Linux, it may look like this:

    ```code
    def qnnSDKLocalPath="/opt/qcom/aistack/qairt/2.28.2.241116"
    ```

8. Build APK
    - Open **the PARENT folder (`android`) (NOT THIS FOLDER)** in Android Studio
    - Run gradle sync
    - Build the `ChatApp` target
        - Click on `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`
    - You can find `APK` at the following path

    ```text
    <ai-hub-apps-repo-root>/apps/android/ChatApp/build/outputs/apk/{build_type}/
    # here {build_type} can be either `release` or `debug`
    ```

9. Run on Android device

    We recommend using [QDC](https://qdc.qualcomm.com/) to run this app.

    **Current limitations**

    - This app does not work on consumer Android 14 devices. It might work if you have newer meta-build as mentioned in [current limitations section](#current-limitations-on-running-chatapp).
    - This app has not yet been verified on Android 15 beta.

    **Steps for running `ChatApp` on QDC**

    1. Copy APK to QDC device: You can upload APK on QDC device instance with one of the following method:

        - Upload at the start of the instance. You can find this option to upload model when you create a QDC device instance
        - Upload APK for existing session
            - Open your QDC instance in browser
            - Open File browser view
            - Upload `ChatApp APK` to device
        - Upload using SSH tunneling
            - You must upload your public ssh key when you create a QDC session to use this path
            - Please check [QDC](https://qdc.qualcomm.com/) documentation for more information.

                ```bash
                adb -P <PORT> push <path to ChatApp.apk on host> /data/local/tmp/
                ```

    2. Open ADB shell on QDC device
        - In browser, open you QDC session
        - Open ADB console

    3. Install ChatApp.apk on-device using adb shell

        ```bash
        # ASSUMPTION: you are already in adb shell after step 2
        pm install -t <path to ChatApp.apk on-device>
        # e.g. pm install -t /data/local/tmp/ChatApp-release.apk
        ```

    4. Use browser UI instance to open and run ChatApp

## License

This app is released under the [BSD-3 License](../../../LICENSE) found at the root of this repository.

All models from [AI Hub Models](https://github.com/quic/ai-hub-models) are released under separate license(s). Refer to the [AI Hub Models repository](https://github.com/quic/ai-hub-models) for details on each model.

The QNN SDK dependency is also released under a separate license. Please refer to the LICENSE file downloaded with the SDK for details.
