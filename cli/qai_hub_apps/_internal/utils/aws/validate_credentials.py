# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------

from __future__ import annotations

import configparser
import contextlib
import functools
import logging
import os
import shutil
import subprocess
import sys
from typing import TYPE_CHECKING

import boto3
import botocore
import botocore.exceptions

if TYPE_CHECKING:
    from mypy_boto3_sts import STSClient

PROFILE = "qaihm"
REGION = "us-west-2"
SESSION_DURATION = 3600


def _load_env(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        raise ValueError(
            f"Missing required environment variable {name}. "
            "See https://qualcomm-confluence.atlassian.net/wiki/spaces/ML/pages/3188064594/Private+AWS+Access+Setup for setup instructions."
        )
    return value


def profile_exists() -> bool:
    try:
        boto3.Session(profile_name=PROFILE)
    except botocore.exceptions.ProfileNotFound:
        logging.warning(f"Profile not found: {PROFILE}")
        return False
    return True


def add_profile() -> None:
    config = configparser.ConfigParser()
    config_file = os.path.expanduser(f"~{os.sep}.aws{os.sep}config")

    config_dir = os.path.dirname(config_file)
    os.makedirs(config_dir, exist_ok=True)

    config.read(config_file)
    with contextlib.suppress(configparser.DuplicateSectionError):
        config.add_section(f"profile {PROFILE}")

    config.set(f"profile {PROFILE}", "region", REGION)
    config.set(f"profile {PROFILE}", "sts_regional_endpoints", "regional")

    with open(config_file, "w") as f:
        config.write(f)


def prune_default() -> None:
    """
    Removes the bare [default] section from ~/.aws/config if it exists.

    AWS allows the default profile as either [profile default] or [default].
    If both exist, CDK blows up, so delete the bare [default] section.
    """
    config = configparser.ConfigParser()
    config_file = os.path.expanduser(f"~{os.sep}.aws{os.sep}config")
    config.read(config_file)

    config.remove_section("default")

    with open(config_file, "w") as f:
        config.write(f)


def create_saml2aws_config(account_id: str, role: str, idp_app_id: str) -> None:
    config_file = os.path.expanduser("~/.saml2aws")
    user_email = None
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        with contextlib.suppress(configparser.NoSectionError):
            user_email = config.get("default", "username")

    user_email = user_email or input("Your qualcomm email address: ")

    with open(config_file, "w") as f:
        f.write(
            f"""[default]
app_id                  = {idp_app_id}
url                     = https://account.activedirectory.windowsazure.com
username                = {user_email}
provider                = AzureAD
mfa                     = Auto
skip_verify             = false
timeout                 = 0
aws_urn                 = urn:amazon:webservices
aws_session_duration    = {SESSION_DURATION}
aws_profile             = {PROFILE}
role_arn                = arn:aws:iam::{account_id}:role/{role}
region                  = {REGION}
saml_cache              = false
disable_remember_device = false
disable_sessions        = false
download_browser_driver = false
headless                = false
"""
        )


def add_default_credentials_section() -> None:
    config_file = os.path.expanduser("~/.aws/credentials")

    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section("default"):
        config.add_section("default")

    for option, value in config.items(PROFILE):
        config.set("default", option, value)

    with open(config_file, "w") as f:
        config.write(f)


@functools.cache
def credentials_valid() -> bool:
    session: boto3.Session = boto3.Session(profile_name=PROFILE)
    sts_client: STSClient = session.client("sts")

    try:
        sts_client.get_caller_identity()
    except (
        botocore.exceptions.NoCredentialsError,
        botocore.exceptions.ClientError,
    ):
        logging.warning(f"Could not get caller identity for aws profile '{PROFILE}'")
        return False

    return True


@functools.cache
def _pass_initialized() -> bool:
    """Check if pass (password-store) has a valid GPG key configured."""
    gpg_id_file = os.path.expanduser("~/.password-store/.gpg-id")
    if not os.path.exists(gpg_id_file):
        return False
    with open(gpg_id_file) as f:
        key_id = f.readline().strip()
    result = subprocess.run(
        ["gpg", "--list-keys", key_id],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


@functools.cache
def is_password_saved() -> bool:
    if sys.platform == "darwin":
        result = subprocess.run(
            [
                "security",
                "find-internet-password",
                "-s",
                "account.activedirectory.windowsazure.com",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout.find("saml2aws") != -1:
            return True
    elif sys.platform == "linux" and _pass_initialized():
        result = subprocess.run(
            [
                "pass",
                "show",
                "saml2aws/https:/account.activedirectory.windowsazure.com",
            ],
            capture_output=True,
            check=False,
        )
        return result.returncode == 0

    return False


def clear_saved_password() -> None:
    if sys.platform == "darwin":
        subprocess.run(
            [
                "security",
                "delete-internet-password",
                "-s",
                "account.activedirectory.windowsazure.com",
            ],
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    account_id = _load_env("QAIHM_AWS_ACCOUNT_ID")
    admin_role = os.environ.get("QAIHM_AWS_ADMIN_ROLE", "")
    role = admin_role or _load_env("QAIHM_AWS_ROLE")
    idp_app_id = _load_env("QAIHM_AWS_IDP_APP_ID")

    if not profile_exists():
        logging.info("Creating AWS profile entry")
        add_profile()

    create_saml2aws_config(account_id, role, idp_app_id)

    prune_default()

    if credentials_valid():
        sys.exit(0)

    logging.info("Obtaining AWS credentials")

    if not sys.stdin.isatty():
        raise RuntimeError(
            "This is not a TTY and hence this script cannot prompt you for your password. Please re-run this in a different, interactive terminal."
        )

    print(f"Getting AWS credentials for {PROFILE}")

    command = ["saml2aws", "login"]

    if is_password_saved():
        command.append("--skip-prompt")

    env: dict[str, str] = os.environ.copy()

    if sys.platform == "linux" and not _pass_initialized():
        command.append("--disable-keychain")
        if shutil.which("pass"):
            print(
                "pass is installed but not configured. Disabling keychain for now.\n"
                "To set up pass so saml2aws can save your password:\n\n"
                "gpg --batch --passphrase '' --quick-gen-key saml2aws\n"
                "pass init $(gpg --list-keys --with-colons saml2aws"
                " | awk -F: '/^fpr/{print $10; exit}')\n"
            )

    try:
        subprocess.run(command, check=True, env=env)
    except Exception:
        if is_password_saved():
            print(
                "Failed to authenticate. If you updated your password recently, that's probably why."
            )
            should_clear = input(
                "Would you like me to erase your saved password? y/N: "
            )
            if should_clear.lower() in ["y", "yes"]:
                clear_saved_password()
                print("Saved password erased. Please try again.")

        raise

    add_default_credentials_section()
