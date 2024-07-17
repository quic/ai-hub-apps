[![Qualcomm® AI Hub Apps](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/quic-logo.jpg)](https://aihub.qualcomm.com)

# Qualcomm® AI Hub Apps

The Qualcomm® AI Hub Apps are a collection of sample machine learning apps ready to deploy on Qualcomm® devices.

Each app is designed to work with one or more models from [Qualcomm® AI Hub Models](https://aihub.qualcomm.com/).

With this repository, you can...
* Explore apps optimized for on-device deployment of various machine learning tasks.
* View open-source app recipes for running [Qualcomm® AI Hub Models](https://aihub.qualcomm.com/) on local devices.

### Supported runtimes
* [TensorFlow Lite](https://www.tensorflow.org/lite)

### Supported Deployment Targets
* Android 11 Red Velvet Cake & Newer, API v30+

### Supported compute units
* CPU, GPU, NPU (includes [hexagon HTP](https://developer.qualcomm.com/hardware/qualcomm-innovators-development-kit/ai-resources-overview/ai-hardware-cores-accelerators))

### Chipsets supported for NPU Acceleration
* [Snapdragon 888/888+](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-8-series-mobile-platforms/snapdragon-888-5g-mobile-platform)
* [Snapdragon 8 Gen 1](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-8-series-mobile-platforms/snapdragon-8-gen-1-mobile-platform)
* [Snapdragon 8 Gen 2](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-8-series-mobile-platforms/snapdragon-8-gen-2-mobile-platform)
* [Snapdragon 8 Gen 3](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-8-series-mobile-platforms/snapdragon-8-gen-3-mobile-platform)
* ... and all other [Snapdragon® chipsets supported by the QNN SDK](https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-50/overview.html#supported-snapdragon-devices)

_Weight and activation type required for NPU Acceleration:_
* Floating Point: FP16 (All Snapdragon® chipsets with Hexagon® Architecture v69 or newer)
* Integer : INT8 (All Snapdragon® chipsets)

__NOTE: These apps will run without NPU acceleration on non-Snapdragon® chipsets.__

## Getting Started

1. Search for your desired OS & app in [this folder](apps), or in the [app directory](#app_directory) at the bottom of this file.

2. The README of the selected app will contain build & installation instructions.

## App Directory

| Task | OS | Language | Inference API | Special Tags
| -- | -- | -- | -- | --
| | | |
| [Image Classification](apps/android/ImageClassification) | Android | Java | TensorFlow Lite |
| [Super Resolution](apps/android/SuperResolution) | Android |  Java | TensorFlow Lite |
| [Semantic Segmentation](apps/android/SemanticSegmentation) | Android |  Java | TensorFlow Lite | OpenCV, Live Camera Feed

## LICENSE

Qualcomm® AI Hub Apps is licensed under BSD-3. See the [LICENSE file](../LICENSE).
