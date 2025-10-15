# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import os
from pathlib import Path
from typing import Union

from qai_hub_apps.utils.paths import APPS_ROOT, REPOSITORY_ROOT
from qai_hub_models.configs.info_yaml import MODEL_LICENSE as LICENSE
from qai_hub_models.models.common import Precision, TargetRuntime
from qai_hub_models.utils.base_config import BaseQAIHMConfig


class QAIHMAppInfo(BaseQAIHMConfig):
    ##########################
    # General Information
    ##########################

    # App name
    name: str

    # License information
    license_url: str
    license_type: LICENSE

    # Model IDs / Precisions / Runtime this app supports
    models: list[str]
    precisions: list[Precision]
    runtime: TargetRuntime

    ##########################
    # Build System Information
    ##########################

    # Path in which downloaded model files should be placed
    # A list can be used for multi-component models.
    model_file_paths: Union[Path, list[Path]]

    @staticmethod
    def from_app(path: str | os.PathLike) -> tuple["QAIHMAppInfo", Path]:
        """
        Load an app info from this directory or yaml file.

        If the path is relative, dir is assumed to be relative to qai-hub-apps/apps.
        """
        path = Path(path)
        if not os.path.isabs(path):
            if path.parts and path.parts[0] == "apps":
                path = REPOSITORY_ROOT / path
            else:
                path = APPS_ROOT / path
        yaml_path = path / "info.yaml" if os.path.isdir(path) else path
        return QAIHMAppInfo.from_yaml(yaml_path), path if path.is_dir() else path.parent
