# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from dataclasses import dataclass, field


@dataclass
class VerifyResult:
    """
    Storage for errors & warnings found during model / app verification.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)

    @property
    def pretty_errors(self) -> str:
        if not self.has_errors:
            return ""
        return (
            """============\nERRORS\n"""
            + "   \n   ".join(self.errors)
            + """\n============"""
        )

    @property
    def pretty_warnings(self) -> str:
        if not self.has_warnings:
            return ""
        return (
            """============\nWARNINGS\n"""
            + "   \n   ".join(self.warnings)
            + """\n============"""
        )

    def merge(self, other: "VerifyResult") -> "VerifyResult":
        return VerifyResult(
            errors=other.errors + self.errors, warnings=other.warnings + self.warnings
        )
