# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from sys import argv

from qai_hub_apps.configs.versions_yaml import VersionsRegistry


def main():
    """
    Prints the version string of a build tool or SDK defined in versions.yaml.
    The tool name is passed as the first argument to this script.
    """
    if len(argv) != 2:
        print("Pass 1 argument (the tool name)")
        exit(1)

    tool = argv[1]
    if tool in VersionsRegistry.model_fields:
        print(getattr(VersionsRegistry.load(), tool))
    else:
        print(f"No version found for {tool}")


if __name__ == "__main__":
    main()
