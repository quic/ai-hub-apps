# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from pathlib import Path


def path_idfn(val):
    """
    Pytest generates test titles based on the parameterization of each test.
    This title can both be used as a filter during test selection and is
    printed to console to identify the test. An example title:
    qai_hub_models/models/whisper_base_en/test_generated.py::test_compile[qnn-cs_8_gen_2]

    Several unit tests parameterize based on path objects. Pytest is not capable by default
    of understanding what string identifier to use for a path object, so it will print
    the name of the arg in the title of those tests rather than the actual path.

    Passing this function to the @pytest.mark.parametrize hook (ids=path_idfn) will
    instruct pytest to print the name of the device in the test title instead.

    See https://docs.pytest.org/en/stable/example/parametrize.html#different-options-for-test-ids
    """
    if isinstance(val, Path):
        return str(val)
