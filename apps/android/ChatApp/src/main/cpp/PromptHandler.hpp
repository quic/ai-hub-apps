//
// Created by Bhushan Sonawane on 10/6/24.
//

// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
#pragma once

#include <string>

namespace AppUtils
{

class PromptHandler
{
  private:
    bool m_is_first_prompt;

  public:
    PromptHandler();
    std::string GetPromptWithTag(const std::string& user_prompt);
};

} // namespace AppUtils
