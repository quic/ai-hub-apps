# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from pydantic import Field, ValidationError
from typing_extensions import Self

from qai_hub_apps.configs.base_config import BaseConfig
from qai_hub_apps.configs.model_asset import ModelAsset

logger = logging.getLogger(__name__)

# Provenance file written into every fetched app dir.
MANIFEST_FILENAME = "qai_hub_apps.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ModelProvenance(BaseConfig):
    """Records the model placed in an app and the files it put there.

    NOTE: ``files`` exists because the asset's ``metadata.json`` does not list
    every file packaged in the download (e.g. weight sidecars), so it cannot be
    used to clean up a previous model. Once metadata.json is complete this can
    be dropped in favour of deriving the file list from it:
    https://github.com/qcom-ai-hub/tetracode/issues/19248
    """

    model_id: str
    requested: ModelAsset | None = None
    files: list[str] = Field(default_factory=list)
    fetched_at: str = Field(default_factory=_now)


class Manifest(BaseConfig):
    """Provenance for a fetched app: the versions that fetched it and its model."""

    cli_version: str | None = None
    qai_hub_models_version: str | None = None
    registry_version: str | None = None
    fetched_at: str | None = None
    model: ModelProvenance | None = None

    @classmethod
    def load(cls, app_dir: Path) -> Self:
        """Read the manifest from *app_dir*, or an empty one if it is absent or unreadable."""
        path = app_dir / MANIFEST_FILENAME
        try:
            return cls.model_validate_json(path.read_text())
        except (OSError, ValidationError):
            logger.debug("No usable manifest at %s", path)
            return cls()

    def write(self, app_dir: Path) -> None:
        """Write this manifest into *app_dir*."""
        data = self.model_dump(mode="json", exclude_none=True)
        path = app_dir / MANIFEST_FILENAME
        path.write_text(
            json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8"
        )
        logger.debug("Wrote manifest %s: %s", MANIFEST_FILENAME, data)
