[![Qualcomm® AI Hub Apps](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/quic-logo.jpg)](https://aihub.qualcomm.com)

# Semantic Segmentation Sample App

This sample app performs semantic segmentation on live camera input.

The app aims to showcase an example of combining streaming camera, TFLite, and OpenCV.

## Prerequisites
1. Clone this repository **with [Git-LFS](https://git-lfs.com) enabled.**
2. Download [Android Studio](https://developer.android.com/studio). **Version 2023.1.1 or newer** is required.
3. [Enable USB debugging](https://developer.android.com/studio/debug/dev-options) on your Android device.

## Build the APK

1. Download or export a [compatible model](#compatible-ai-hub-models) from [AI Hub Models](https://aihub.qualcomm.com/mobile/models).
2. Copy the `.tflite` file to `src/main/assets/<your_model>.tflite`
3. In [../gradle.properties](../gradle.properties), modify the value of `semanticsegmentation_tfLiteModelAsset` to the name of your model file (`<your_model>.tflite`)
4. Open **the PARENT folder (`android`) (NOT THIS FOLDER)** in Android Studio, run gradle sync, and build the `SemanticSegmentation` target.

## Supported Hardware (TF Lite Delegates)

By default, this app supports the following hardware:
* [Qualcomm Hexagon NPU -- via QNN](https://developer.qualcomm.com/software/qualcomm-ai-engine-direct-sdk)
* [GPU -- via GPUv2](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/delegates/gpu)
* [CPU -- via XNNPack](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/delegates/xnnpack/README.md)

Comments have been left in [TFLiteHelpers.java](src/main/java/com/qualcomm/tflite/TFLiteHelpers.java) and [AIHubDefaults.java](src/main/java/com/qualcomm/tflite/AIHubDefaults.java) to guide you on how to add support for additional TF Lite delegates that could target other hardware.

## AI Model Requirements

### Model Runtime Formats
- TensorFlow Lite (.tflite)

### I/O Specification

| INPUT | Description | Shape | Data Type
| -- | -- | -- | --
| Image | An RGB image | [1, Height, Width, 3] | float32 input expecting inputs normalized by a per-channel mean and standard deviation (see app code for details)

| OUTPUT | Description | Shape | Data Type
| -- | -- | -- | --
| Classes | **CityScapes** Classes | [1, Height', Width', 19] | float32 lower resolution class logit predictions

Refer to the CityScapes segmentation
[model.py](https://github.com/quic/ai-hub-models/blob/main/qai_hub_models/models/_shared/cityscapes_segmentation/model.py)
for class label information.

The app is developed to work best with a Width/Height ratio of 2.

## Compatible [AI Hub Models](https://aihub.qualcomm.com/mobile/models)

The app is currently compatible with the TFLite `float` variant of these models:

- [FFNet-40S](https://aihub.qualcomm.com/mobile/models/ffnet_40s)
- [FFNet-54S](https://aihub.qualcomm.com/mobile/models/ffnet_54s)
- [FFNet-78S](https://aihub.qualcomm.com/mobile/models/ffnet_78s)
- [FFNet-78S-LowRes](https://aihub.qualcomm.com/mobile/models/ffnet_78s_lowres)
- [FFNet-122NS-LowRes](https://aihub.qualcomm.com/mobile/models/ffnet_122ns_lowres)

## Replicating an AI Hub Profile / Inference Job

Each AI Hub profile or inference job, once completed, will contain a `Runtime Configuration` section.

Modify [TFLiteHelpers.java](src/main/java/com/qualcomm/tflite/TFLiteHelpers.java) according to the runtime configuration applied to the job. **Comment stubs are included** to help guide you (search for `TO REPLICATE AN AI HUB JOB...`)

Note that if your job uses delegates other than QNN NPU, GPUv2, and TFLite, then you'll also need to add support for those delegates to the app.

## Technologies Used by this App

- [Android SDK](https://developer.android.com/studio)
- [TensorFlow Lite](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite)
- [OpenCV](https://opencv.org)
- [QNN SDK (TF Lite Delegate)](https://developer.qualcomm.com/software/qualcomm-ai-engine-direct-sdk)
- [GPUv2 Delegate](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/delegates/gpu)
- [XNNPack Delegate](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/delegates/xnnpack/README.md)

## Expected Camera Environment

This app uses models trained on the [Cityscapes Dataset](https://www.cityscapes-dataset.com). That means it will __only produce valid results if the camera is pointed at street scenes!__
When in doubt, point the camera at the following sample image to verify accuracy:

![Cityscapes-like example image](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/models/cityscapes_segmentation/v1/cityscapes_like_demo_2048x1024.jpg "Cityscapes-like example image")

## License

This app is released under the [BSD-3 License](../../../LICENSE) found at the root of this repository.

All models from [AI Hub Models](https://github.com/quic/ai-hub-models) are released under separate license(s). Refer to the [AI Hub Models repository](https://github.com/quic/ai-hub-models) for details on each model.

The QNN SDK dependency is also released under a separate license. Please refer to the LICENSE file downloaded with the SDK for details.
