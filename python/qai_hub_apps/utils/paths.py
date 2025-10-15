# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import os
from functools import lru_cache
from pathlib import Path

# Repository Global Paths
REPOSITORY_ROOT = Path(os.path.dirname(__file__)).parent.parent.parent
CACHE_ROOT = Path.home() / ".cache" / ".qaiha"
APPS_ROOT = REPOSITORY_ROOT / "apps"
MAX_APP_SEARCH_DEPTH = 3


def is_app_root(path: str | os.PathLike) -> bool:
    return (Path(path) / "info.yaml").exists()


def _get_all_apps(
    base: str | os.PathLike = APPS_ROOT,
    root: str | os.PathLike = APPS_ROOT,
    depth: int = 0,
) -> list[Path]:
    if depth >= MAX_APP_SEARCH_DEPTH:
        return []

    app_dirs = []
    for filename in os.listdir(root):
        path = Path(root) / filename
        if os.path.isdir(path):
            if is_app_root(path):
                app_dirs.append(path.relative_to(base))
            else:
                app_dirs.extend(_get_all_apps(base, path, depth + 1))

    return app_dirs


@lru_cache
def get_all_apps(root: str | os.PathLike = APPS_ROOT) -> list[Path]:
    """
    Get path to every app relative to the given root directory.
    """
    return _get_all_apps(root, root, 0)
