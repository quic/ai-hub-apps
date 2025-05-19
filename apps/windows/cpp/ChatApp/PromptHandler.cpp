// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
#include "PromptHandler.hpp"
#include "ChatApp.hpp"

using namespace AppUtils;

// Prompt formats: LLAMA3, LLAMA3_TAIDE, LLAMA2
#define LLAMA3

#ifdef LLAMA3
// Llama3 prompt
// Ref: https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-3/
constexpr const std::string_view c_begin_system =
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYour name is Qbot and you are a helpful AI "
    "assistant. Please keep answers concise and to the point. <|eot_id|>\n\n";
constexpr const std::string_view c_begin_user = "<|start_header_id|>user<|end_header_id|>\n\n";
constexpr const std::string_view c_end_user = "<|eot_id|>";
constexpr const std::string_view c_begin_assistant = "<|start_header_id|>assistant<|end_header_id|>\n\n";
constexpr const std::string_view c_end_assistant = "<|eot_id|>";

#elif defined LLAMA3_TAIDE
// Llama3-TAIDE
constexpr const std::string_view c_begin_system =
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n你是一個來自台灣的AI助理，你的名字是 "
    "TAIDE，樂於以台灣人的立場幫助使用者，會用繁體中文回答問題<|eot_id|>\n\n";
constexpr const std::string_view c_begin_user = "<|start_header_id|>user<|end_header_id|>\n\n";
constexpr const std::string_view c_end_user = "<|eot_id|>";
constexpr const std::string_view c_begin_assistant = "<|start_header_id|>assistant<|end_header_id|>\n\n";
constexpr const std::string_view c_end_assistant = "<|eot_id|>";

#elif defined LLAMA2
// Llama2 system prompt
// Ref: https://www.llama.com/docs/model-cards-and-prompt-formats/meta-llama-2/
constexpr const std::string_view c_begin_system =
    "<s>[INST] <<SYS>>\nYour name is Qbot and you are a helpful AI assistant. Please keep answers concise and to the "
    "point.\n<</SYS>>\n\n";
constexpr const std::string_view c_begin_assistant = "";
constexpr const std::string_view c_end_assistant = "\n</s>\n";
constexpr const std::string_view c_begin_user = "<s>[INST] ";
constexpr const std::string_view c_end_user = " [/INST] ";
#endif

PromptHandler::PromptHandler()
    : m_is_first_prompt(true)
{
}

std::string PromptHandler::GetPromptWithTag(const std::string& user_prompt)
{
    if (m_is_first_prompt)
    {
        m_is_first_prompt = false;
        return std::string(c_begin_system) + c_begin_user.data() + user_prompt.data() + c_end_user.data() +
               c_begin_assistant.data();
    }
    return std::string(c_end_assistant) + c_begin_user.data() + user_prompt.data() + c_end_user.data() +
           c_begin_assistant.data();
}
