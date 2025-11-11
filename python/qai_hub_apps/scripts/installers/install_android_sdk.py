# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from pathlib import Path

from qai_hub_apps.configs.versions_yaml import VersionsRegistry
from qai_hub_apps.utils.android.android_sdk_installer import (
    get_android_sdk_root_optional,
    install_android_sdk,
    recommended_android_sdk_root,
)
from tap import Tap


class AndroidSDKInstallParams(Tap):
    sdk_root: Path | None = get_android_sdk_root_optional()  # Android SDK root.
    compile_api: set[int] = {
        VersionsRegistry.load().android_compile_api
    }  # Android compile APIs (build tool versions) that must be supported by the SDK.
    platforms: set[int] = {
        VersionsRegistry.load().android_target_api
    }  # Android platforms that must be supported by the SDK.
    ndks: set[str] = {
        VersionsRegistry.load().android_ndk
    }  # NDK versions that the SDK must include.
    cmdline_tools: str = VersionsRegistry.load().android_cmdline_tools


def main():
    args = AndroidSDKInstallParams().parse_args()
    sdk_root = args.sdk_root
    if not sdk_root:
        raise ValueError(
            f"sdk_root was not provided and ANDROID_HOME and is not set, cannot find Android SDK root. Recommended location: {recommended_android_sdk_root()}"
        )

    install_android_sdk(
        sdk_root, args.compile_api, args.platforms, args.ndks, args.cmdline_tools
    )

    print(f"Android SDK is installed at {sdk_root}")


if __name__ == "__main__":
    main()
