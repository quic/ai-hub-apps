# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

# pragma: exclude file
import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict
from typing_extensions import Self


class BaseConfig(BaseModel):
    """Pydantic v2 model with YAML (de)serialization."""

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def from_yaml(cls, path: Path | str) -> Self:
        with open(path, encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f)
        return cls.model_validate(data)

    def to_yaml(self, path: Path | str, write_if_empty: bool = False) -> bool:
        """Dump this instance to a YAML file.

        Defaults and ``None`` values are omitted. If the result is empty, the
        file is written only when *write_if_empty* is True, and an empty file
        is removed. Returns True if a non-empty file was written.
        """
        data = self.model_dump(mode="json", exclude_defaults=True, exclude_none=True)
        if not data and not write_if_empty:
            if os.path.exists(path):
                os.remove(path)
            return False
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(
                data,
                f,
                sort_keys=False,
                default_flow_style=False,
                width=4096,
                allow_unicode=True,
            )
        return bool(data)
