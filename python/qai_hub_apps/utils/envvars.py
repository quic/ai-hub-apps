# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from qai_hub_models.utils.envvar_bases import QAIHMBoolEnvvar


class AutoYesPromptEnvvar(QAIHMBoolEnvvar):
    """
    Environment variable that controls responding 'yes' automatically to y/n shell prompts.
    This is generally only useful in a testing or CI environment, when user input is inaccessible.
    """

    VARNAME = "QAIHA_AUTO_YES_PROMPT"

    @classmethod
    def default(cls) -> bool:
        return False
