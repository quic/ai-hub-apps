[![Qualcomm® AI Hub Apps](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/quic-logo.jpg)](https://aihub.qualcomm.com)

# Object Detection Sample App

This sample app performs object detection on live camera input.

The app aims to showcase an example of combining streaming camera, TFLite, and OpenCV.

## Prerequisites
1. Clone this repository **with [Git-LFS](https://git-lfs.com) enabled.**
2. Download [Android Studio](https://developer.android.com/studio). **Version 2023.1.1 or newer** is required.
3. [Enable USB debugging](https://developer.android.com/studio/debug/dev-options) on your Android device.

## Build the APK

1. Download or export a [compatible model](#compatible-ai-hub-models) from [AI Hub Models](https://aihub.qualcomm.com/mobile/models).
2. Copy the `.tflite` file to `src/main/assets/objectdetection.tflite`
4. Copy the labels file (see list below) to `src/main/assets/labels.txt`
3. (Optional) Both model and labels file can have custom names. If so,
   please edit [../gradle.properties](../gradle.properties) and update
   `objectdetection_tfLiteModelAsset` and `objectdetection_tfLiteLabelsAsset`.
5. Open **the PARENT folder (`android`) (NOT THIS FOLDER)** in Android Studio, run gradle sync, and build the `ObjectDetection` target.

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
| `image` | An RGB image | [1, Height, Width, 3] | float32 input expecting inputs normalized to [0, 1]

| OUTPUT | Description | Shape | Data Type
| -- | -- | -- | --
| `boxes` | Bounding Boxes | [1, Anchors, 4] | float32 boxes (x0, y0, x1, y1) in pixel space
| `scores` | Class Scores | [1, Anchors] | float32 class logit predictions
| `class_idx` | Class Index | [1, Anchors] | uint8 or int32 class index

The app is developed to work best with a Width/Height ratio of 1.

## Compatible [AI Hub Models](https://aihub.qualcomm.com/mobile/models)

The app is currently compatible with the TFLite `float` variant of these models:

- 91-class COCO  ([coco_labels_91.txt](https://github.com/quic/ai-hub-models/blob/main/qai_hub_models/labels/coco_labels_91.txt))
  - [DETR-ResNet50](https://aihub.qualcomm.com/mobile/models/detr_resnet50)
  - [DETR-ResNet101](https://aihub.qualcomm.com/mobile/models/detr_resnet101)
- 80-class COCO ([coco_labels.txt](https://github.com/quic/ai-hub-models/blob/main/qai_hub_models/labels/coco_labels.txt))
  - [Yolo-v3](https://aihub.qualcomm.com/mobile/models/yolov3)
  - [Yolo-v5](https://aihub.qualcomm.com/mobile/models/yolov5)
  - [Yolo-v6](https://aihub.qualcomm.com/mobile/models/yolov6)
  - [Yolo-v7](https://aihub.qualcomm.com/mobile/models/yolov7)
  - [YOLOv8-Detection](https://aihub.qualcomm.com/mobile/models/yolov8_det)
  - [YOLOv10-Detection](https://aihub.qualcomm.com/mobile/models/yolov10_det)
  - [YOLOv11-Detection](https://aihub.qualcomm.com/mobile/models/yolov11_det)
  - [Yolo-X](https://aihub.qualcomm.com/mobile/models/yolox)

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

## License

This app is released under the [BSD-3 License](../../../LICENSE) found at the root of this repository.

All models from [AI Hub Models](https://github.com/quic/ai-hub-models) are released under separate license(s). Refer to the [AI Hub Models repository](https://github.com/quic/ai-hub-models) for details on each model.

The QNN SDK dependency is also released under a separate license. Please refer to the LICENSE file downloaded with the SDK for details.
