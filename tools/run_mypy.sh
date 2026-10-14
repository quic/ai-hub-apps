#!/usr/bin/env bash
# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
# Activates qaiha-dev and runs mypy in the given working directory.
# Usage: tools/run_mypy.sh <working-dir> <mypy-args...>

set -euo pipefail

REPO=$(git rev-parse --show-toplevel)

source "$REPO/qaiha-dev/bin/activate" 2>/dev/null || {
    echo "[ERROR] qaiha-dev not found. run 'bash tools/setup_env.sh'"
    exit 1
}

cd "$REPO/$1"
shift
exec mypy "$@"
