// ---------------------------------------------------------------------
// Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// ---------------------------------------------------------------------
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

#include "ChatApp.hpp"

namespace
{

constexpr const std::string_view c_option_model_config_path = "--model_config";
constexpr const std::string_view c_option_models_path = "--models";
constexpr const std::string_view c_option_htp_config_path = "--htp_config";
constexpr const std::string_view c_option_tokenizer_path = "--tokenizer";
constexpr const std::string_view c_option_help = "--help";
constexpr const std::string_view c_option_help_short = "-h";

void PrintHelp()
{
    std::cout << "\n:::::::: Chat with " << App::c_bot_name << " options ::::::::\n\n";
    std::cout << c_option_model_config_path << " <Local file path>: [Required] Path to local genie config for model.\n";
    std::cout << c_option_models_path
              << " <Local directory path>: [Required] Path to local models downloaded from AI Hub.\n";
    std::cout << c_option_htp_config_path << " <Local file path>: [Required] Path to local HTP backend extensions.\n"
              << "\tAvailable htp configurations are located here <project_dir>/assets/configs/htp_backend_ext/\n";
    std::cout << c_option_tokenizer_path << " <Local file path>: [Required] Path to local tokenizer json.\n"
              << "\tAvailable tokenizers are located here <project_dir>/assets/configs/tokenizer/\n";
    std::cout << "\nDuring chat with " << App::c_bot_name << ", please type " << App::c_exit_prompt
              << " as a prompt to terminate chat.\n ";
}

void PrintWelcomeMessage()
{
    std::cout << "\n:::::::: Welcome to Chat with " << App::c_bot_name << " ::::::::\n ";
    std::cout << App::c_bot_name << " will use provided configuration file for conversation.\n";
    std::cout << "At any time during chat, please type `" << App::c_exit_prompt
              << "` to terminate the conversation.\n\n";
    std::cout << "Let's begin with an introduction,\n";
    std::cout << "I'm `" << App::c_bot_name << "`! what's your name ? ";
}

} // namespace

int main(int argc, char* argv[])
{
    std::string model_config_path;
    std::string models_path;
    std::string htp_config_path;
    std::string tokenizer_path;
    bool invalid_arguments = false;

    // Check if argument file path is accessible
    auto check_arg_path = [&invalid_arguments](const std::string_view& arg_name, const std::string& value)
    {
        if (value.empty() || !std::filesystem::exists(value))
        {
            std::cout << "\nInvalid argument for " << arg_name
                      << ": It must be a valid and accessible local path. Provided: " << value << std::endl;
            invalid_arguments = true;
        }
    };

    // Arg parser
    for (int i = 1; i < argc; ++i)
    {
        if (c_option_model_config_path == argv[i])
        {
            model_config_path = argv[++i];
            check_arg_path(c_option_model_config_path, model_config_path);
        }
        else if (c_option_models_path == argv[i])
        {
            models_path = argv[++i];
            check_arg_path(c_option_models_path, models_path);
        }
        else if (c_option_htp_config_path == argv[i])
        {
            htp_config_path = argv[++i];
            check_arg_path(c_option_htp_config_path, htp_config_path);
        }
        else if (c_option_tokenizer_path == argv[i])
        {
            tokenizer_path = argv[++i];
            check_arg_path(c_option_tokenizer_path, tokenizer_path);
        }
        else if (c_option_help == argv[i] || c_option_help_short == argv[i])
        {
            PrintHelp();
            return 0;
        }
        else
        {
            std::cout << "Unsupported option " << argv[i] << " provided.\n";
            invalid_arguments = true;
        }
    }

    // If invalid arguments, print help and exit.
    if (invalid_arguments)
    {
        PrintHelp();
        return 1;
    }

    try
    {
        std::string user_name;

        App::ChatApp app(model_config_path, models_path, htp_config_path, tokenizer_path);

        // Get user name to chat with
        PrintWelcomeMessage();
        std::getline(std::cin, user_name);

        // Interactive chat
        app.ChatWithUser(user_name);
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    catch (...)
    {
        std::cerr << "Unknown error.\n";
        return 1;
    }
    return 0;
}
