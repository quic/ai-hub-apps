# LLM On-Device Deployment

In this tutorial we will show an end to end workflow deploying large language
models (LLMs) to Snapdragon® platforms such as Snapdragon® 8 Elite,
Snapdragon® 8 Gen 3 (e.g., Samsung Galaxy S24 family) and Snapdragon® X Elite
(e.g. Snapdragon® based Microsoft Surface Pro). We will use
[Qualcomm AI Hub](https://aihub.qualcomm.com/) to compile the models to QAIRT
context binaries and run them with Genie from the [QAIRT
SDK](https://qpm.qualcomm.com/#/main/tools/details/Qualcomm_AI_Runtime_SDK).

We will use Llama3 8B as a running example. Other LLMs from [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models)
will work with the same flow.

## Overview

We will walk you through the follow steps:

1. Get access to [Llama 3 weights from Hugging Face](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct).
2. Use Qualcomm [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models) to export Llama 3 using AI Hub.
3. Prepare assets required by Qualcomm Genie, the inference runtime for LLMs.
4. Run the LLM on device with an example prompt on Android / Windows PC with Snapdragon®.

Note that because this is a large model, it may take 4-6 hours to generate required assets.

If you have any questions, please feel free to post on [AI Hub Slack channel](https://aihub.qualcomm.com/community/slack)

## Device Requirements

| Model name | Minimum Compile QAIRT SDK version | Supported devices |
| --- | --- | --- |
| Llama-v2-7B-Chat | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® 8 Gen 3<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama-v3-8B-Instruct | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama-v3.1-8B-Instruct | 2.27.7 | Snapdragon® 8 Elite |
| Llama-v3.1-8B-Instruct | 2.28.0 | Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama-v3.2-3B-Instruct | 2.27.7 | Snapdragon® 8 Elite<br>Snapdragon® 8 Gen 3 (Context length 2048) |
| Llama-v3.2-3B-Instruct | 2.28.0 | Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama3-TAIDE-LX-8B-Chat-Alpha1 | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Baichuan2-7B | 2.27.7 |  Snapdragon® 8 Elite |
| Qwen2-7B-Instruct | 2.27.7 |  Snapdragon® 8 Elite |
| Mistral-7B-Instruct-v0.3 | 2.27.7 |  Snapdragon® 8 Elite |
| Phi-3.5-Mini-Instruct | 2.29.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® 8 Gen 3 |
| IBM-Granite-v3.1-8B-Instruct | 2.30.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite |

Device requirements:

- Android 15
- At least Genie SDK from QAIRT (or QNN) SDK 2.29.0 (earlier versions have issues with long prompts).
- Hexagon architecture v73 or above (please see [Devices](https://app.aihub.qualcomm.com/devices/) list).
- 16GB memory or more for 7B+ or 4096 context length models.
- 12GB memory or more for 3B+ models (and you may need to adjust down context length).

> [!IMPORTANT]
> Please make sure device requirements are met before proceeding.

## Required Software

The following packages are required:

1. [QAIRT SDK](https://qpm.qualcomm.com/#/main/tools/details/Qualcomm_AI_Runtime_SDK) (see [QNN SDK](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct) for versions prior to 2.32)
2. [qai-hub-models](https://pypi.org/project/qai-hub-models/) and any extras for your desired model.
3. [qai-hub](https://pypi.org/project/qai-hub/)

### QAIRT Installation

Typically we recommend using the same QAIRT SDK version that AI Hub uses to compile
the assets. You can find this version by clicking the job links posted printed
by the export command.

Go to [QAIRT
SDK](https://qpm.qualcomm.com/#/main/tools/details/Qualcomm_AI_Runtime_SDK) (or [QNN SDK](https://qpm.qualcomm.com/#/main/tools/details/qualcomm_ai_engine_direct) for older versions) and
follow the installation instructions. Note that the first time after log in you
would be redirected to QPM home page. Click on the link again to get to the
QAIRT download page.

If you are on a Mac laptop, we recommend using
[Docker](https://www.docker.com/) to install qpm-cli to extract the `.qik` file.

If successful, you should see a message with the install path. This will depend on
the platform and can look like this:

```text
/opt/qcom/aistack/qairt/<version>
C:\Qualcomm\AIStack\QAIRT\<version>
```

Set your `QNN_SDK_ROOT` environment variable to point to this directory. On
Linux or Mac you would run:

```bash
export QNN_SDK_ROOT=/opt/qcom/aistack/qairt/<version>
```

On Windows, you can search the taskbar for "Edit the system environment
variables".

### Python Packages

Following standard best practices, we recommend creating a virtual environment specifically for
exporting AI Hub models. The following steps can be performed on Windows,
Linux, or Mac. On Windows, you can either install x86-64 Python (since package
support is limited on native ARM64 Python) or use Windows Subsystem for Linux
(WSL).

#### Create Virtual Environment

Create a [virtualenv](https://virtualenv.pypa.io/en/latest/) for `qai-hub-models` with Python 3.10.
You can also use [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

For clarity, we recommend creating a virtual env:

```bash
python3.10 -m venv llm_on_genie_venv
```

#### Install `qai-hub-models`

In a shell session, install `qai-hub-models` in the virtual environment:

```bash
source llm_on_genie_venv/bin/activate
pip install -U "qai-hub-models[llama-v3-8b-instruct]"
```

Replace `llama-v3-8b-instruct` with the desired llama model from [AI Hub
Model](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models).
Note to replace `_` with `-` (e.g. `llama_v3_8b_instruct` -> `llama-v3-8b-instruct`)

Make sure Git is installed in your environment. This command should work:

```bash
git --version
```

Ensure at least 80GB of memory (RAM + swap). On Ubuntu (including through WSL) you can check it by

```bash
free -h
```

Increase swap size if needed.

We use
[qai-hub-models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/)
to adapt Huggingface Llama models for on-device inference.

## Acquire Genie Compatible QNN binaries from AI Hub

### [Llama Only] Setup Hugging Face token

Setting up Hugging Face token is required only for the Llama model family.
Request model access on Hugging Face for Llama models. For instance, you can [apply here](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) to access Llama 3.2 3B model.

Set up Hugging Face token locally by following the instructions [here](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

### Download or Generate Genie Compatible QNN Binaries

Some of the models can be downloaded directly from [AI
Hub](https://aihub.qualcomm.com). For Llama, it has to be exported through [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models).

To generate the Llama assets, we will run a single command that performs the
following steps:

1. Download model weights from Hugging Face. You will need to sign the Llama
license if you haven't already done so.

2. Upload models to AI Hub for compilation.

3. Download compiled context binaries. Note that there are multiple binaries as
   we have split up the model.

Make a directory to put in all deployable assets. For this example we use

```bash
mkdir -p genie_bundle
```

#### [Optional] Upgrade PyTorch

The export command below may take 4-6 hours. It takes an additional 1-2 hours
on PyTorch versions earlier than 2.4.0. We recommend upgrading PyTorch first:

```bash
pip install torch==2.4.0
```

This version is not yet supported in general by AI Hub Models but will work
for the below export command.

Note that the export also requires a lot of memory (RAM + swap) on the host
device (for Llama 3, we recommend 80 GB). If we detect that you have less
memory than recommended, the export command will print a warning with
instructions of how to increase your swap space.

#### For Android on Snapdragon® 8 Elite

```bash
python -m qai_hub_models.models.llama_v3_8b_instruct.export --device "Snapdragon 8 Elite QRD" --skip-inferencing --skip-profiling --output-dir genie_bundle
```

For Snapdragon 8 Gen 3, please use `--device "Snapdragon 8 Gen 3 QRD"`.

#### For Windows on Snapdragon® X Elite

```bash
python -m qai_hub_models.models.llama_v3_8b_instruct.export --device "Snapdragon X Elite CRD" --skip-inferencing --skip-profiling --output-dir genie_bundle
```

Note: For older devices, you may need to adjust the context length using
`--context-length <context-length>`.

The `genie_bundle` would now contain both the intermediate models (`token`,
`prompt`) and the final context binaries (`*.bin`). Remove the intermediate
models to have a smaller deployable artifact:

```bash
# Remove intermediate assets
rm -rf genie_bundle/{prompt,token}
```

## Prepare Genie Configs

### Tokenizer

To download the tokenizer, go to the source model's Hugging Face page and go to "Files
and versions." You can find a Hugging Face link through the model card on
[AI Hub](https://aihub.qualcomm.com/). This will take you to the Qualcomm Hugging Face page,
which in turn will have a link to the source Hugging Face page. The file will be named `tokenizer.json`
and should be downloaded to the `genie_bundle` directory. The tokenizers are only hosted on the source Hugging Face page.

| Model name | Tokenizer | Notes |
| --- | --- | --- |
| Llama-v2-7B-Chat | [tokenizer.json](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf/blob/main/tokenizer.json) | |
| Llama-v3-8B-Chat | [tokenizer.json](https://huggingface.co/meta-llama/Meta-Llama-3-8B/blob/main/tokenizer.json) | |
| Llama-v3.1-8B-Chat | [tokenizer.json](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/blob/main/tokenizer.json) | |
| Llama-v3.2-3B-Chat | [tokenizer.json](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct/blob/main/tokenizer.json) | |
| Llama3-TAIDE-LX-8B-Chat-Alpha1 | [tokenizer.json](https://huggingface.co/taide/Llama3-TAIDE-LX-8B-Chat-Alpha1/blob/main/tokenizer.json) | |
| Baichuan2-7B | [tokenizer.json](https://qaihub-public-assets.s3.us-west-2.amazonaws.com/qai-hub-models/models/baichuan2_7b_quantized/v2/tokenizer.json) | |
| Qwen2-7B-Instruct | [tokenizer.json](https://huggingface.co/Qwen/Qwen2-7B-Instruct/blob/main/tokenizer.json) | |
| Phi-3.5-Mini-Instruct | [tokenizer.json](https://huggingface.co/microsoft/Phi-3.5-mini-instruct/blob/main/tokenizer.json) | To see appropriate spaces in the output, remove lines 193-196 (Strip rule) in the tokenizer file. |
| Mistral-7B-Instruct-v0.3 | [tokenizer.json](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3/blob/main/tokenizer.json) | |
| IBM-Granite-v3.1-8B-Instruct | [tokenizer.json](https://huggingface.co/ibm-granite/granite-3.1-8b-base/blob/main/tokenizer.json) | |

### [Optional] Use the Windows PowerShell LLM Runner

**Do not use this script to create your Genie bundle if you are building Windows ChatApp. Continue with the rest of the tutorial instead.**

The easiest path to running an LLM on a Windows on Snapdragon® device is to use the [PowerShell implementation](powershell/)
of the rest of this tutorial. It will automatically generate the appropriate configuration files and execute `genie-t2t-run.exe`
on a prompt of your choosing.

### Genie Config

Check out the [AI Hub Apps repository](https://github.com/quic/ai-hub-apps)
using Git:

```bash
git clone https://github.com/quic/ai-hub-apps.git
```

Now run (replacing `llama_v3_8b_instruct` with the desired model id):

```bash
cp ai-hub-apps/tutorials/llm_on_genie/configs/genie/llama_v3_8b_instruct.json genie_bundle/genie_config.json
```

For Windows laptops, please set `use-mmap` to `false`.

If you customized context length by adding `--context-length` to the export
command, please open `genie_config.json` and modify the `"size"` option (under
`"dialog"` -> `"context"`) to be consistent.

In `genie_bundle/genie_config.json`, also ensure that the list of bin files in
`ctx-bins` matches with the bin files under `genie_bundle`. Genie will look for
QNN binaries specified here.

### HTP Backend Config

Copy the HTP config template:

```bash
cp ai-hub-apps/tutorials/llm_on_genie/configs/htp/htp_backend_ext_config.json.template genie_bundle/htp_backend_ext_config.json
```

Edit `soc_model` and `dsp_arch` in `genie_bundle/htp_backend_ext_config.json`
depending on your target device (should be consistent with the `--device` you
specified in the export command):

| Generation               | `soc_model` | `dsp_arch` |
|--------------------------|--------|----------|
| Snapdragon® Gen 2        | 43     | v73      |
| Snapdragon® Gen 3        | 57     | v75      |
| Snapdragon® 8 Elite      | 69     | v79      |
| Snapdragon® X Elite      | 60     | v73      |
| Snapdragon® X Plus       | 60     | v73      |

## Collect & Finalize Genie Bundle

When finished with the above steps, your bundle should look like this:
```
genie_bundle/
   genie_config.json
   htp_backend_ext_config.json
   tokenizer.json
   <model_id>_part_1_of_N.bin
   ...
   <model_id>_part_N_of_N.bin
```

where <model_id> is the name of the model. This is the name of the json you copied from `configs/genie/<model_name>.json`.

## Run LLM on Device

You have three options to run the LLM on device:

 1. Use the `genie-t2t-run` CLI command.
 2. Use the [CLI Windows ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/windows/cpp/ChatApp) (Windows only).
 3. Use the [Android ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/android/ChatApp).

### Prompt Formats

All the LLMs have different formats. To get sensible output from the LLMs, it is important to use the correct prompt format for the model. These can also be found on the Hugging Face repository for each of the model. Adding samples for a few models here.

| Model name | Sample Prompt |
| --- | --- |
| Llama-v2-7B-Chat | &lt;s&gt;[INST] &lt;&lt;SYS&gt;&gt;You are a helpful AI Assistant.&lt;&lt;/SYS&gt;&gt;[/INST]&lt;/s>&lt;s&gt;[INST]What is France's capital?[/INST] |
| Llama-v3-8B-Chat <br> Llama-v3.1-8B-Chat <br> Llama-v3.2-3B-Chat | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\nWhat is France's capital?<&#124;eot_id&#124;><&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;> |
| Llama3-TAIDE-LX-8B-Chat-Alpha1 | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>system<&#124;end_header_id&#124;>\n\n你是一個來自台灣的AI助理，你的名字是 TAIDE，樂於以台灣人的立場幫助使用者，會用繁體中文回答問題<&#124;eot_id&#124;>\n<&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\n介紹台灣特色<&#124;eot_id&#124;>\n<&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;> |
| Qwen2-7B-Instruct | <&#124;im_start&#124;>system\nYou are a helpful AI Assistant<&#124;im_end&#124;><&#124;im_start&#124;>What is France's capital?\n<&#124;im_end&#124;>\n<&#124;im_start&#124;>assistant\n |
| Phi-3.5-Mini-Instruct | <&#124;system&#124;>\nYou are a helpful assistant. Be helpful but brief.<&#124;end&#124;>\n<&#124;user&#124;>What is France's capital?\n<&#124;end&#124;>\n<&#124;assistant&#124;>\n |
| Mistral-7B-Instruct-v0.3 | &lt;s&gt;[INST] You are a helpful assistant\n\nTranslate 'Good morning, how are you?' into French.[/INST] |
| IBM-Granite-v3.1-8B-Instruct | <&#124;start_of_role&#124;>system<&#124;end_of_role&#124;>You are a helpful AI assistant.<&#124;end_of_text&#124;>\n <&#124;start_of_role&#124;>user<&#124;end_of_role&#124;>What is France's capital?<&#124;end_of_text&#124;>\n <&#124;start_of_role&#124;>assistant<&#124;end_of_role&#124;>\n |

### 1. Run Genie On-Device via `genie-t2t-run`

#### Genie on Windows with Snapdragon® X

Copy Genie's shared libraries and executable to our bundle.
(Note you can skip this step if you used the powershell script to prepare your bundle.)

```bash
cp $QNN_SDK_ROOT/lib/hexagon-v73/unsigned/* genie_bundle
cp $QNN_SDK_ROOT/lib/aarch64-windows-msvc/* genie_bundle
cp $QNN_SDK_ROOT/bin/aarch64-windows-msvc/genie-t2t-run.exe genie_bundle
```

In Powershell, navigate to the bundle directory and run

```bash
./genie-t2t-run.exe -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

Note that this prompt format is specific to Llama 3.

#### Genie on Android

Copy Genie's shared libraries and executable to our bundle.

```bash
# For 8 Gen 2
cp $QNN_SDK_ROOT/lib/hexagon-v73/unsigned/* genie_bundle
# For 8 Gen 3
cp $QNN_SDK_ROOT/lib/hexagon-v75/unsigned/* genie_bundle
# For 8 Elite
cp $QNN_SDK_ROOT/lib/hexagon-v79/unsigned/* genie_bundle
# For all devices
cp $QNN_SDK_ROOT/lib/aarch64-android/* genie_bundle
cp $QNN_SDK_ROOT/bin/aarch64-android/genie-t2t-run genie_bundle
```

Copy `genie_bundle` from the host machine to the target device using ADB and
open up an interactive shell on the target device:

```bash
adb push genie_bundle /data/local/tmp
adb shell
```

On device, navigate to the bundle directory:

```bash
cd /data/local/tmp/genie_bundle
```

Set `LD_LIBRARY_PATH` and `ADSP_LIBRARY_PATH` to the current directory:

```bash
export LD_LIBRARY_PATH=$PWD
export ADSP_LIBRARY_PATH=$PWD
```

Then run:

```bash
./genie-t2t-run -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

#### Sample Output

```text
Using libGenie.so version 1.1.0

[WARN]  "Unable to initialize logging in backend extensions."
[INFO]  "Using create From Binary List Async"
[INFO]  "Allocated total size = 323453440 across 10 buffers"
[PROMPT]: <|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>

[BEGIN]: \n\nFrance's capital is Paris.[END]

[KPIS]:
Init Time: 6549034 us
Prompt Processing Time: 196067 us, Prompt Processing Rate : 86.707710 toks/sec
Token Generation Time: 740568 us, Token Generation Rate: 12.152884 toks/sec
```

### 2. Sample C++ Chat App Powered by Genie SDK

We provide a sample C++ app to show how to build an application using the Genie SDK.
See [CLI Windows ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/windows/cpp/ChatApp) for more details.

### 3. Sample Android Chat App Powered by Genie SDK

We provide a sample Android (Java and C++ app) to show how to build an application using the Genie SDK for mobile.
See [Android ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/android/ChatApp) for more details.
