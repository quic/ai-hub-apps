# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import os
import platform
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path

from qai_hub_apps.utils.envvars import AutoYesPromptEnvvar
from qai_hub_models.utils.asset_loaders import download_file


def recommended_android_sdk_root() -> Path:
    """
    Get the recommended Android SDK root location for this machine.

    Returns
    -------
    Path
        Path to the recommended SDK root.
    """
    platf = platform.system()
    if platf == "Windows":
        sdk_root = Path.home() / "AppData" / "Local" / "Android" / "sdk"
    elif platf == "Linux":
        sdk_root = Path.home() / "Android" / "Sdk"
    elif platf == "Darwin":
        sdk_root = Path.home() / "Library" / "Android" / "sdk"
    else:
        raise NotImplementedError(f"Unsupported platform: {platf}")

    return sdk_root


def get_android_sdk_root() -> Path:
    """
    Fetch the root of the android SDK.

    Returns
    -------
    Path
        Path to the SDK root.

    Raises
    ------
    ValueError
        If ANDROID_HOME is not set.
    """
    if home := os.getenv("ANDROID_HOME"):
        return Path(home)

    raise ValueError(
        f"ANDROID_HOME is not set, cannot find Android SDK root. Recommended location: {recommended_android_sdk_root()}"
    )


def get_android_sdk_root_optional() -> Path | None:
    """
    Fetch the root of the android SDK.

    Returns
    -------
    Path | None
        Path to the recommended SDK root, or None if unset.
    """
    try:
        return get_android_sdk_root()
    except ValueError:
        return None


def install_android_sdk(
    sdk_root: str | os.PathLike,
    build_tools: set[int],
    platforms: set[int],
    ndks: set[str],
    cmdline_tools: str,
):
    """
    Installs the Android SDK components required for building and compiling Android applications.

    Parameters
    ----------
    sdk_root
        Path to the Android SDK root directory. If the directory does not exist, it will be created.
    build_tools
        Set of Android compile API levels (build tool versions) that must be supported by the SDK.
    platforms
        Set of Android platform API levels that must be supported by the SDK.
    ndks
        Set of Android NDK versions that must be included in the SDK.
    cmdline_tools
        Android command-line tool version that must be included in the SDK.
    """
    sdk_root = Path(sdk_root)

    # Install SDK Tools
    cmdlinetools_to_install = set()
    cmdline_tools_dir = sdk_root / "cmdline-tools"
    for tools_version in cmdline_tools:
        if not os.path.exists(cmdline_tools_dir / tools_version):
            cmdlinetools_to_install.add(tools_version)

    packages_to_install = []

    # platform-tools
    platform_tools_dir = sdk_root / "platform-tools"
    if not os.path.exists(platform_tools_dir):
        packages_to_install.append("platform-tools")

    # Platforms
    platforms_dir = sdk_root / "platforms"
    for platform_num in platforms:
        platform_dir = platforms_dir / f"android-{platform_num}"
        if not os.path.exists(platform_dir):
            packages_to_install.append(f"platforms;android-{str(platform_num)}")

    # Build Tools
    build_tools_dir = sdk_root / "build-tools"
    for build_tool_version in build_tools:
        build_tools_version_dir = build_tools_dir / f"{build_tool_version}.0.0"
        if not os.path.exists(build_tools_version_dir):
            packages_to_install.append(f"build-tools;{build_tool_version}.0.0")

    # NDK
    ndk_dir = sdk_root / "ndk"
    for ndk_version in ndks:
        ndk_version_dir = ndk_dir / ndk_version
        if not os.path.exists(ndk_version_dir):
            packages_to_install.append(f"ndk;{ndk_version}")

    # Install all packages via SDK Manager
    if packages_to_install:
        if not AutoYesPromptEnvvar().get():
            print_packages = packages_to_install.copy()
            for tools_version in cmdline_tools:
                print_packages.append(f"cmdlinetools;{tools_version}")
            print(
                f"The following components need to be installed in the Android SDK at {sdk_root}: {print_packages}. Continue (y)?"
            )
            while True:
                i = input().lower()
                if i in ["yes", "y"]:
                    break
                if i in ["no", "n"]:
                    raise ValueError(
                        "Cannot continue as Android SDK does not have the correct components."
                    )

        install_android_sdk_cmdline_tools(
            cmdline_tools, cmdline_tools_dir / cmdline_tools
        )

        packages = '"' + '" "'.join(packages_to_install) + '"'
        sendlines = None
        if AutoYesPromptEnvvar.get() and not (sdk_root / "licenses").is_dir():
            sendlines = ["y"]

        p = subprocess.Popen(
            f'{sdk_root / "cmdline-tools" / next(iter(cmdline_tools)) / "bin" / "sdkmanager"} --install {packages} --sdk_root="{sdk_root}"',
            shell=True,
            text=True,
            stdin=subprocess.PIPE,
        )
        if p.stdin is not None and sendlines:
            p.stdin.writelines(sendlines)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            print(f"Command line tools failed to install:\n{stdout}\n{stderr}")


def install_android_sdk_cmdline_tools(version: str, cmdlinetools_dir: Path):
    """
    Installs the version of Android command line tools to the target dir.

    Parameters
    ----------
    version
        SDKTools version.
    cmdlinetools_dir
        Dir in which the tools should be installed.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "cmdline-tools.zip"
        download_file(
            f"https://dl.google.com/android/repository/commandlinetools-linux-{version}.zip",
            str(zip_path),
        )
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)
        cmdlinetools_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(Path(tmpdir) / "cmdline-tools", cmdlinetools_dir)

    if os.name == "posix":
        for root, _, files in os.walk(cmdlinetools_dir / "bin"):
            for file in files:
                f = Path(root) / file
                os.chmod(f, f.stat().st_mode | stat.S_IEXEC)
    print(f"Android Command Line Tools {version} installed at {cmdlinetools_dir}")
