# LLM on-device deployment

In this tutorial we will show how an end to end workflow of deploying
large language models (LLMs) to run on Snapdragon® platform such as Snapdragon®
8 Elite, Snapdragon® 8 Gen 3 chipset (e.g., Samsung Galaxy S24 family) and
Snapdragon® X Elite (e.g. Snapdragon® based Microsoft Surface Pro). We will use
[Qualcomm AI Hub](https://aihub.qualcomm.com/) to compile the models to QNN binaries,
and run it with Genie in [QNN
SDK](https://qpm.qualcomm.com/main/tools/details/qualcomm_ai_engine_direct).

We will use Llama3 8B as a running example. Other LLMs from [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models)
will work with the same flow.

## Overview

We will walk you through the follow steps:

1. Get access to [Llama 3 weights from huggingface](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)
2. Use Qualcomm [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models) to export Llama 3 using AI Hub
3. Prepare assets required by Qualcomm Genie, the inference runtime for LLMs

On Android / Windows PC with Snapdragon® platform

4. Run the LLM on device with an example prompt

Note that because this is a large model, it may take 1-2 hours to generate required assets.

If you have any questions, please feel free to post on [AI Hub slack channel](https://aihub.qualcomm.com/community/slack)

## Requirements

1. [QNN SDK](https://qpm.qualcomm.com/main/tools/details/qualcomm_ai_engine_direct)
2. [qai-hub-models](https://pypi.org/project/qai-hub-models/)
3. [qai-hub](https://pypi.org/project/qai-hub/)

## Device Requirements

| Model name | Minimum QNN SDK version | Supported devices |
| --- | --- | --- |
| Llama-v2-7B-Chat | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® 8 Gen 3<br>Snapdragon® X Elite |
| Llama-v3-8B-Chat | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite |
| Llama-v3.1-8B-Chat | 2.27.7 | Snapdragon® 8 Elite |
| Llama-v3.1-8B-Chat | 2.28.0 | Snapdragon® X Elite |
| Llama-v3.2-3B-Chat | 2.27.7 | Snapdragon® 8 Elite<br>Snapdragon® 8 Gen 3 (Context length 2048) |
| Llama-v3.2-3B-Chat | 2.28.0 | Snapdragon® X Elite |
| Baichuan2-7B | 2.27.7 |  Snapdragon® 8 Elite |
| Qwen2-7B-Instruct | 2.27.7 |  Snapdragon® 8 Elite |
| Mistral-7B-Instruct-v0.3 | 2.27.7 |  Snapdragon® 8 Elite |

Device requirements:
- 16GB memory or more for 7B+ or 4096 context length models.
- 12GB memory or more for 3B+ models (and you may need to adjust down context length).

Models that require 2.27.7 will be available on Snapdragon® X Elite starting
from QNN SDK 2.28.0.

## 1. Generate Genie compatible QNN binaries from AI Hub

### Requirements

### Set up huggingface token

Setting up huggingface token is required only for Llama model family.
Request model access on huggingface for Llama models. For instance, you can [apply here](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) to access Llama 3.2 2B model.

Setup huggingface token locally by following the instructions [here](https://huggingface.co/docs/huggingface_hub/en/guides/cli).

### Set up virtual envs

Create a [virtualenv](https://virtualenv.pypa.io/en/latest/) for `qai-hub-models` with Python 3.10.
You can also use [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).

For clarity, we recommend creating a virtual env:

```
python3.10 -m venv llm_on_genie_venv
```

### Install QAI-Hub-Models

In shell session, install `qai-hub-models` under `hub_model` virtual env

```bash
source llm_on_genie_venv/bin/activate
pip install -U "qai_hub_models[llama-v3-8b-chat-quantized]"
```

Replace `llama-v3-8b-chat-quantized` with the desired llama model from [AI Hub
Model](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models).
Note to replace `_` with `-` (e.g. `llama_v3_8b_chat_quantized` -> `llama-v3-8b-chat-quantized`)

Ensure at least 80GB of memory (RAM + swap). On Ubuntu you can check it by

```
free -h
```

Increase swap size if needed.

We use
[qai-hub-models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/)
to adapt Huggingface Llama models for on-device inference.

### Download or Generate Genie-compatible QNN binaries

Some of the models can be downloaded directly from [AI
Hub](https://aihub.qualcomm.com). For Llama, it has to be exported through [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models).

To generate the Llama assets, we will run a single command that performs the
following steps:

1. Download model weights from Huggingface. You will need to sign the Llama
license if you haven't already done so.

2. Upload models to AI Hub for compilation.

3. Download compiled QNN binaries. Note that it's multiple binaries as we split the model.

Make a directory to put in all deployable assets. For this example we use

```bash
mkdir -p genie_bundle
```

#### (Optional) Upgrade PyTorch

The export command below typically takes 1-2 hours. However, it may take 3-4
hours on PyTorch versions earlier than 2.4.0. We recommend upgrading PyTorch
first:

```bash
pip install torch==2.4.0
```

This version is not yet supported in general by AI Hub Models but will work
for the below export command.

Note that the export also requires a lot of memory (RAM + swap) on the host
device (for Llama 3, we recommend 80 GB). If we detect that you have less
memory than recommended, the export command will print a warning with
instructions of how to increase your swap space.

#### For Snapdragon® 8 Elite Android device:

```bash
python -m qai_hub_models.models.llama_v3_8b_chat_quantized.export --chipset qualcomm-snapdragon-8-elite --skip-inferencing --skip-profiling --output-dir genie_bundle
```

For Snapdragon 8 Gen 3, please use `--chipset qualcomm-snapdragon-8gen3`.

#### For Windows with Snapdragon® X Elite

```bash
python -m qai_hub_models.models.llama_v3_8b_chat_quantized.export --chipset qualcomm-snapdragon-x-elite --skip-inferencing --skip-profiling --output-dir genie_bundle
```

Note: For older devices, you may need to adjust the context length using
`--context-length <context-length>`.

The `genie_bundle` would now contain both the intermediate models (`token`,
`prompt`) and the final QNN models (`*.bin`). Remove the intermediate models to
have a smaller deployable artifact:

```bash
# Remove intermediate assets
rm -rf genie_bundle/{prompt,token}
```

### Install QNN

Typically we recommend using the same QNN SDK version that AI Hub uses to compile
the assets. You can find this version by clicking the job links posted printed
by the export command.

However, if the [Model Requirements](#model-requirements) table above requires a
newer version than AI Hub uses, please use the newer version.

Go to [QNN
SDK](https://qpm.qualcomm.com/main/tools/details/qualcomm_ai_engine_direct) and
follow the installation instructions. Note that the first time after log in you
would be redirected to QPM home page. Click on the link again to get to QNN
download page.

If you are on a Mac laptop, we recommend using
[Docker](https://www.docker.com/) to install qpm-cli to extract the `.qik` file.

If successful, you'd see a message like

```
SUCCESS: Installed qualcomm_ai_engine_direct.Core at /opt/qcom/aistack/qairt/<version>
```

Set your `QNN_SDK_ROOT` environment variable to point to this directory. For
instance, on Linux you would run:

```
export QNN_SDK_ROOT=/opt/qcom/aistack/qairt/<version>
```

## Prepare Genie Configs

### HTP Backend Config

Check out the [AI Hub Apps repository](https://github.com/quic/ai-hub-apps)
using Git:


```bash
git clone https://github.com/quic/ai-hub-apps.git
```

Now copy the HTP config template:

```bash
cp ai-hub-apps/tutorials/llm_on_genie/configs/htp/htp_backend_ext_config.json.template genie_bundle/htp_backend_ext_config.json
```

Edit `soc_model` and `dsp_arch` in `genie_bundle/htp_backend_ext_config.json`
depending on your target device (should be consistent with the `--device` you
specified in the export command):

| Generation | `soc_model` | `dsp_arch` |
|------------|--------|----------|
| Snapdragon® Gen 2      | 43     | v73      |
| Snapdragon® Gen 3      | 57     | v75      |
| Snapdragon® 8 Elite      | 69     | v79      |
| Snapdragon® X Elite      | 60     | v73      |

### Tokenizer

To download the tokenizer, go to the source model's Hugging Face page and go to "Files
and versions." You can find a Hugging Face link through the model card on
[AI Hub](https://aihub.qualcomm.com/). This will take you to the Qualcomm Hugging Face page,
which in turn will have a link to the source Hugging Face page. The tokenizer is
only hosted on the source Hugging Face page (e.g.
[here](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/tree/main)
for Llama 3.0).
The file will be named `tokenizer.json`
and should be downloaded to the `genie_bundle` directory.

### Genie Config

Please run (replacing `llama_v3_8b_chat_quantized` with the desired model id):

```bash
cp ai-hub-apps/tutorials/llm_on_genie/configs/genie/llama_v3_8b_chat_quantized.json genie_bundle/genie_config.json
```

For Windows laptops, please set `use-mmap` to `false`.

If you customized context length by adding `--context-length` to the export
command, please open `genie_config.json` and modify the `"size"` option (under
`"dialog"` -> `"context"`) to be consistent.

In `genie_bundle/genie_config.json`, also ensure that the list of bin files in
`ctx-bins` matches with the bin files under `genie_bundle`. Genie will look for
QNN binaries specified here.

## Copy Genie Binaries

Copy Genie's shared libraries and executable to our bundle.

### For Windows device

```bash
cp $QNN_SDK_ROOT/lib/hexagon-v73/unsigned/* genie_bundle
cp $QNN_SDK_ROOT/lib/aarch64-windows-msvc/* genie_bundle
cp $QNN_SDK_ROOT/bin/aarch64-windows-msvc/genie-t2t-run.exe genie_bundle
```

### For Android device

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

## Run LLM on device

You have two options to run the LLM on device:

 1. Use the `genie-t2t-run` CLI command
 2. Use the [CLI Windows ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/windows/cpp/ChatApp) (Windows only)

### 1. Run Genie On-Device via `genie-t2t-run`

#### For Windows with Snapdragon® X Elite

In Powershell, navigate to the bundle directory and run

```bash
./genie-t2t-run.exe -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

Note that this prompt format is specific to Llama 3.

#### For Android device:

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

Set `LD_LIBRARY_PATH` to the current directory:

```bash
export LD_LIBRARY_PATH=$PWD
```

Then run:

```bash
./genie-t2t-run -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

#### Sample output

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
