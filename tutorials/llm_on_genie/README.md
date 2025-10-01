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
| Llama-v3.2-1B-Instruct | 2.36.3 | Snapdragon® 8 Elite |
| Llama-v3.2-3B-Instruct | 2.27.7 | Snapdragon® 8 Elite<br>Snapdragon® 8 Gen 3 (Context length 2048) |
| Llama-v3.2-3B-Instruct | 2.28.0 | Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama-SEA-LION-v3.5-8B-R | 2.28.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Llama3-TAIDE-LX-8B-Chat-Alpha1 | 2.27.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Baichuan2-7B | 2.27.7 |  Snapdragon® 8 Elite |
| Qwen2-7B-Instruct | 2.27.7 |  Snapdragon® 8 Elite |
| Qwen2.5-7B-Instruct | 2.27.7 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® X Plus |
| Mistral-7B-Instruct-v0.3 | 2.27.7 |  Snapdragon® 8 Elite |
| Phi-3.5-Mini-Instruct | 2.29.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite<br>Snapdragon® 8 Gen 3 |
| IBM-Granite-v3.1-8B-Instruct | 2.30.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite |
| Falcon3-7B-Instruct | 2.37.0 | Snapdragon® 8 Elite<br>Snapdragon® X Elite |

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
Hub](https://aihub.qualcomm.com). If you download the model,
you need to prepare a Genie bundle manually by following [these
instructions](manual_bundle.md).

For Llama and other recipe-based models, it has to be exported through [AI Hub
Models](https://github.com/quic/ai-hub-models/tree/main/qai_hub_models/models),
which will help construct the Genie bundle as well.

To generate the Llama assets, we will run a single command that performs the
following steps:

1. Download model weights from Hugging Face. You will need to sign the Llama
license if you haven't already done so.

2. Upload models to AI Hub for compilation.

3. Download compiled context binaries. Note that there are multiple binaries as
   we have split up the model.

4. Prepare auxiliary files, such as tokenizer and Genie configurations.

#### Exporting Llama models takes time and resources.

The export command below may take 4-6 hours.

Note that the export also requires a lot of memory (RAM + swap) on the host
device (for Llama 3, we recommend 80 GB). If we detect that you have less
memory than recommended, the export command will print a warning with
instructions of how to increase your swap space.

#### For Android on Snapdragon® 8 Elite

```bash
python -m qai_hub_models.models.llama_v3_8b_instruct.export --chipset qualcomm-snapdragon-8-elite --skip-profiling --output-dir genie_bundle
```

For Snapdragon 8 Gen 3, please use `--chipset qualcomm-snapdragon-8gen3`.

#### For Windows on Snapdragon® X Elite

```bash
python -m qai_hub_models.models.llama_v3_8b_instruct.export --chipset qualcomm-snapdragon-x-elite --skip-profiling --output-dir genie_bundle
```

Note: For more memory-constrained devices, you may need to adjust the context
length using `--context-length <context-length>`.

The export script will place context binaries, tokenizer, and Genie
configuration files into the `genie_bundle` folder. If you plan to run this
directly through `genie-t2t-run`, then please follow the instructions printed
at the end of the export script to copy the QAIRT files into the bundle as
well.

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
| Llama-v3-8B-Instruct <br> Llama-v3.1-8B-Instruct <br> Llama-v3.2-3B-Instruct <br> Llama-v3.2-1B-Instruct | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\nWhat is France's capital?<&#124;eot_id&#124;><&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;> |
| Llama3-TAIDE-LX-8B-Chat-Alpha1 | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>system<&#124;end_header_id&#124;>\n\n你是一個來自台灣的AI助理，你的名字是 TAIDE，樂於以台灣人的立場幫助使用者，會用繁體中文回答問題<&#124;eot_id&#124;>\n<&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\n介紹台灣特色<&#124;eot_id&#124;>\n<&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;> |
| Llama-SEA-LION-v3.5-8B-R (non-thinking mode) | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>system<&#124;end_header_id&#124;>\n\ndetailed thinking off<&#124;eot_id&#124;><&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\nThủ đô của Việt Nam là thành phố nào?<&#124;eot_id&#124;><&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;>\n\n&lt;think&gt;\n\n&lt;/think&gt;>\n\n |
| Llama-SEA-LION-v3.5-8B-R (thinking mode) | <&#124;begin_of_text&#124;><&#124;start_header_id&#124;>system<&#124;end_header_id&#124;>\n\ndetailed thinking on<&#124;eot_id&#124;><&#124;start_header_id&#124;>user<&#124;end_header_id&#124;>\n\nThủ đô của Việt Nam là thành phố nào?<&#124;eot_id&#124;><&#124;start_header_id&#124;>assistant<&#124;end_header_id&#124;>\n\n&lt;think&gt;\nHere is my thinking:\n |
| Qwen2-7B-Instruct <br> Qwen2.5-7B-Instruct | <&#124;im_start&#124;>system\nYou are a helpful AI Assistant<&#124;im_end&#124;><&#124;im_start&#124;>What is France's capital?\n<&#124;im_end&#124;>\n<&#124;im_start&#124;>assistant\n |
| Phi-3.5-Mini-Instruct | <&#124;system&#124;>\nYou are a helpful assistant. Be helpful but brief.<&#124;end&#124;>\n<&#124;user&#124;>What is France's capital?\n<&#124;end&#124;>\n<&#124;assistant&#124;>\n |
| Mistral-7B-Instruct-v0.3 | &lt;s&gt;[INST] You are a helpful assistant\n\nTranslate 'Good morning, how are you?' into French.[/INST] |
| IBM-Granite-v3.1-8B-Instruct | <&#124;start_of_role&#124;>system<&#124;end_of_role&#124;>You are a helpful AI assistant.<&#124;end_of_text&#124;>\n <&#124;start_of_role&#124;>user<&#124;end_of_role&#124;>What is France's capital?<&#124;end_of_text&#124;>\n <&#124;start_of_role&#124;>assistant<&#124;end_of_role&#124;>\n |
| Falcon3-7B-Instruct | <&#124;system&#124;>\nYou are a helpful friendly assistant Falcon3 from TII, try to follow instructions as much as possible.\n<&#124;user&#124;>\nWhat is France's capital?\n<&#124;assistant&#124;>\n |

> [!IMPORTANT]
> Many system prompts contain the line feed character (`\n`, ascii 0x0a) as
> part of the correct prompt format. We have to pay extra attention to how
> we pass this into the LLM so that it is not passed in as `\` and `n` as two
> separate characters. This is platform specific, so more on this in the
> sections below.
>
> On all platforms, we do recommend copy-pasting the prompts into a separate
> file (e.g., `prompt.txt`) and passing that prompt into `genie-t2t-run` with
> `--promt_file prompt.txt`. If you take this approach, please make sure
> you replace the `\n` characters with real newlines.

### 1. Run Genie On-Device via `genie-t2t-run`

#### Genie on Windows with Snapdragon® X

In PowerShell, navigate to the bundle directory and run

```bash
./genie-t2t-run.exe -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>`n`nWhat is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

Note that this prompt format is specific to Llama 3.

Also note that we changed `\n` to `` `n ``, since that is how to pass a proper
line feed character in Windows Powershell.

For languages that use non-latin characters (e.g., Chinese, Arabic), you may
need to first [configure Windows to use UTF-8](windows/utf8.md).

#### Genie on Android

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
./genie-t2t-run -c genie_config.json -p "<|begin_of_text|><|start_header_id|>user<|end_header_id|>"$'\n\n'$"What is France's capital?<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
```

Note that in order to pass real line feed characters into Genie, we have to
replace the `"\n\n"` with `$'\n\n'$`. This is a Bash convention and may not
apply to other shells. We generally recommend using a prompt file instead where
you can use real newlines.

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

Note: QAIRT 2.35 and above does not show KPIs at the end of the response. You can pass `--profile /path/to/txt/file` to store KPIs in that file to look at it later.


### 2. Sample C++ Chat App Powered by Genie SDK

We provide a sample C++ app to show how to build an application using the Genie SDK.
See [CLI Windows ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/windows/cpp/ChatApp) for more details.

### 3. Sample Android Chat App Powered by Genie SDK

We provide a sample Android (Java and C++ app) to show how to build an application using the Genie SDK for mobile.
See [Android ChatApp](https://github.com/quic/ai-hub-apps/tree/main/apps/android/ChatApp) for more details.
