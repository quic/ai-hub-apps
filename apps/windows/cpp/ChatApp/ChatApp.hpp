// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
#pragma once

#include <string>

#include "GenieCommon.h"
#include "GenieDialog.h"

namespace App
{
constexpr const std::string_view c_exit_prompt = "exit";
constexpr const std::string_view c_bot_name = "Qbot";

class ChatApp
{
  private:
    GenieDialogConfig_Handle_t m_config_handle = nullptr;
    GenieDialog_Handle_t m_dialog_handle = nullptr;
    std::string m_user_name;

  public:
    /**
     * ChatApp: Initializes ChatApp
     *    - Loads Model config with provided model path, htp config and tokenizer
     *    - Creates handle for Genie
     *
     * @param model_config_path: local path to model Genie config file
     * @param models_path: local path to directory that contains model context binaries (e.g., downloaded from AI Hub)
     * @param htp_config_path: local path to backend htp configuration
     * @param tokenizer_path: local path to tokenizer to use
     *
     * @thows on failure to create handle for Genie config, dialog
     *
     */
    ChatApp(const std::string& model_config_path,
            const std::string& models_path,
            const std::string& htp_config_path,
            const std::string& tokenizer_path);
    ChatApp() = delete;
    ChatApp(const ChatApp&) = delete;
    ChatApp(ChatApp&&) = delete;
    ChatApp& operator=(const ChatApp&) = delete;
    ChatApp& operator=(ChatApp&&) = delete;
    ~ChatApp();

    /**
     * ChatWithUser: Starts Chat with user using previously loaded config
     *
     * @param user_name: User name to  use during chat
     *
     * @throws on failure to query model response during chat
     *
     */
    void ChatWithUser(const std::string& user_name);
};
} // namespace App
