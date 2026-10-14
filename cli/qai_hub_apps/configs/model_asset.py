# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path

from pydantic import ConfigDict, model_validator

from qai_hub_apps.configs.base_config import BaseConfig
from qai_hub_apps.utils.devices import device_to_chipset


class ModelAsset(BaseConfig):
    """Identifies a model to bundle into an app.

    Either ``model_id`` (downloaded from AI Hub) or ``path`` (a locally-exported
    model directory or ``.zip``) is set. For a local export, ``model_id`` is
    derived from the export's ``metadata.json`` and ``chipset``/``device`` do
    not apply.

    ``chipset`` and ``device`` are mutually exclusive ways to target an asset.
    """

    model_config = ConfigDict(frozen=True)

    model_id: str | None = None
    chipset: str | None = None
    device: str | None = None
    path: Path | None = None

    @model_validator(mode="after")
    def _check_exclusive_target(self) -> ModelAsset:
        if self.chipset is not None and self.device is not None:
            raise ValueError("Provide at most one of 'chipset' or 'device'.")
        return self

    def resolved_chipset(self) -> str | None:
        """The chipset this targets, whichever way the target was named.

        Returns
        -------
        str | None
            The chipset, or None when no target was given.

        Raises
        ------
        KeyError
            If ``device`` is not a known AI Hub device.
        """
        if self.chipset is not None:
            return self.chipset
        if self.device is not None:
            return device_to_chipset(self.device)
        return None

    def __str__(self) -> str:
        if self.path is not None:
            return f"the model at '{self.path}'"
        target = self.chipset or self.device
        if target is None:
            return f"'{self.model_id}'"
        return f"'{self.model_id}' for '{target}'"
