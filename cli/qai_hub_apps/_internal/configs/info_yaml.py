# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import os
from enum import Enum, unique
from os import PathLike
from pathlib import Path

from pydantic import Field, model_validator

from qai_hub_apps._internal.utils.paths import APPS_ROOT, REPOSITORY_ROOT
from qai_hub_apps.configs.app_yaml import (
    INFO_FILENAME,
    AppInfo,
    AppLanguage,
    AppStatus,
    AppType,
    AppUrl,
)
from qai_hub_apps.configs.base_config import BaseConfig
from qai_hub_apps.configs.field_types import Device, Precision

__all__ = [
    "AppInfo",
    "AppInfoInternal",
    "AppLanguage",
    "AppLicense",
    "AppOS",
    "AppStatus",
    "AppType",
    "AppUrl",
    "DeviceTestStatus",
    "SupportedDevice",
]


@unique
class AppLicense(Enum):
    UNLICENSED = "unlicensed"
    COMMERCIAL = "commercial"
    APACHE_2_0 = "apache-2.0"
    MIT = "mit"
    BSD_3_CLAUSE = "bsd-3-clause"
    CC_BY_4_0 = "cc-by-4.0"
    AGPL_3_0 = "agpl-3.0"
    GPL_3_0 = "gpl-3.0"
    OTHER_NON_COMMERCIAL = "other-non-commercial"
    CC_BY_NON_COMMERCIAL_4_0 = "cc-by-non-commercial-4.0"


@unique
class DeviceTestStatus(Enum):
    TESTED = "Tested"  # The device this app is tested on in CI
    NOT_TESTED = "Not Tested"


class SupportedDevice(BaseConfig):
    name: Device
    status: DeviceTestStatus = DeviceTestStatus.NOT_TESTED


class AppOS(BaseConfig):
    name: str
    version: str


class AppInfoInternal(AppInfo):
    """Full internal app info — adds CI/build fields on top of CLI-facing fields."""

    ##########################
    # General Information
    ##########################

    # Operating system the app targets (name + minimum version). Used by
    # website-import; not consumed by CI/build tooling here.
    os: AppOS

    # Optional when app_repo_relative_path is set; generate_registry resolves a
    # concrete URL before writing the registry, where it is required.
    app_repo_url: str | None = None  # type: ignore[assignment]

    skip_test: str | None = None
    skip_related_models_verify: str | None = None
    supported_devices: list[SupportedDevice] = Field(  # type: ignore[assignment]
        default_factory=list
    )
    app_repo_relative_path: str | None = (
        None  # relative path within qualcomm/ai-hub-apps
    )

    @model_validator(mode="after")
    def _validate_supported_devices(self) -> "AppInfoInternal":
        if not self.supported_devices:
            return self
        tested = [
            d for d in self.supported_devices if d.status is DeviceTestStatus.TESTED
        ]
        if len(tested) != 1:
            raise ValueError(
                f"App '{self.id}': exactly one supported_devices entry must have "
                f"status '{DeviceTestStatus.TESTED.value}', got {len(tested)}"
            )
        return self

    @property
    def tested_device(self) -> Device | None:
        """The device this app is tested on, or None if no devices are declared."""
        return next(
            (
                d.name
                for d in self.supported_devices
                if d.status is DeviceTestStatus.TESTED
            ),
            None,
        )

    @model_validator(mode="after")
    def _validate_repo(self) -> "AppInfoInternal":
        if not self.app_repo_url and not self.app_repo_relative_path:
            raise ValueError(
                f"App '{self.id}': one of app_repo_url or app_repo_relative_path must be set"
            )
        return self

    # License information
    license_url: str
    license_type: AppLicense

    ##########################
    # Build System Information
    ##########################

    base_docker: str | None = None  # Dockerfile filename relative to tools/docker/

    # Path to private S3 URLs that CI will use to fetch certain models. map<Model ID, map<Precision, map<Chipset, Relative S3 Path>>
    # This is necessary for complex models (like LLMs) until AI Hub Models has a good way to fetch these.
    private_model_s3_paths: dict[str, dict[Precision, dict[str, str]]] = Field(
        default_factory=dict
    )

    @staticmethod
    def from_app(path: str | PathLike) -> tuple["AppInfoInternal", Path]:
        """
        Load an app info from this directory or yaml file.

        If the path is relative, dir is assumed to be relative to qai-hub-apps/apps.
        """
        path = Path(path)
        if not os.path.isabs(path):
            if path.parts and path.parts[0] == "apps":
                path = REPOSITORY_ROOT / path
            else:
                path = APPS_ROOT / path
        yaml_path = path / INFO_FILENAME if os.path.isdir(path) else path
        adir = path if os.path.isdir(path) else Path(os.path.dirname(path))
        return AppInfoInternal.from_yaml(yaml_path), adir
