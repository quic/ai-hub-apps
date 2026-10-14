# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
"""Resolve the apps/_shared/scripts root directory."""

from __future__ import annotations

from pathlib import Path

from qai_hub_apps._internal.utils.paths import REPOSITORY_ROOT

_DEFAULT_SCRIPTS_ROOT = REPOSITORY_ROOT / "apps" / "_shared" / "scripts"


def resolve_scripts_root(override: Path | None = None) -> Path:
    """Return the path to the shared scripts directory.

    Parameters
    ----------
    override:
        Explicit path to the shared scripts directory. If given, returned as-is.
        If None, the default repo location is used.

    Returns
    -------
    Path
        Path to the shared scripts directory.
    """
    if override is not None:
        return override
    return _DEFAULT_SCRIPTS_ROOT
