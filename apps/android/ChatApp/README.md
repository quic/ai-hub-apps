[![Qualcomm® AI Hub Apps](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/quic-logo.jpg)](https://aihub.qualcomm.com)

# Sample Chat App

Chat application for Android on Snapdragon® with [Llama 3.2 3B](https://aihub.qualcomm.com/compute/models/llama_v3_2_3b_instruct) using Genie SDK.

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
3. Install AI Hub and AI Hub models

    ```bash
    pip install qai-hub
    pip install "qai-hub-models[llama-v3-2-3b-instruct]"
    ```

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

We will use Llama 3.2 3B with context length 2048 as an example for this demo.

1. Go to ChatApp directory

```bash
cd <ai-hub-apps-repo-root>/apps/android/ChatApp/
```

1. Export Llama 3.2 3B model with context length 2048 (if you change this, please update the `"size"` option in the `apps/android/ChatApp/src/main/assets/models/llama3_2_3b/genie_config.json` file)

    - Read more about [exporting LLMs via AI Hub here](https://github.com/quic/ai-hub-apps/tree/main/tutorials/llm_on_genie#1-generate-genie-compatible-qnn-binaries-from-ai-hub)
        - You'll have to replace model name from the above tutorial with `llama_v3_2_3b_instruct` and reduce context length for this demo.

    - Export Llama 3.2 3B model with context length 2048

    ```bash
    python -m qai_hub_models.models.llama_v3_2_3b_instruct.export --context-length 2048 --device "Snapdragon 8 Elite QRD" --output-dir genie_bundle
    ```

    - Exporting Llama3.2 models will take a while depending on your internet connectivity.
    - This takes around 1-2 hours with good internet connectivity.

2. Download and save `tokenizer.json` from [Huggingface Llama3.2](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) to `src/main/assets/models/llama3_2_3b/`

3. Copy model binaries (`genie_bundle/*.bin`) from step 1 to `src/main/assets/models/llama3_2_3b/`

    ```bash
    cp genie_bundle/*.bin src/main/assets/models/llama3_2_3b/
    ```

4. Note that you do not need to set up the `genie_config.json` and the HTP
   config. These files are already set up for you. In the `genie_config.json`, you will find
   placeholders like `<models_path>`. These will be resolved by the app and are
   important so that the Android app can locate your files on device.

5. Update `<ai-hub-apps-repo-root>/apps/android/ChatApp/build.gradle` with path to QNN SDK root directory. If you are on QNN version 2.28.2 and have extracted to the default location on Linux, it may look like this:

    ```code
    def qnnSDKLocalPath="/opt/qcom/aistack/qairt/2.28.2.241116"
    ```

6. Build APK
    - Open **the PARENT folder (`android`) (NOT THIS FOLDER)** in Android Studio
    - Run gradle sync
    - Build the `ChatApp` target
        - Click on `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`
    - You can find `APK` at the following path

    ```text
    <ai-hub-apps-repo-root>/apps/android/ChatApp/build/outputs/apk/{build_type}/
    # here {build_type} can be either `release` or `debug`
    ```


7. Run on Android device

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
