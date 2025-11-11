# ---------------------------------------------------------------------
# Copyright (c) 2025 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
import os
import re
import subprocess
from typing import Any

from qai_hub_apps.configs.versions_yaml import VersionsRegistry
from qai_hub_apps.utils.android.android_sdk_installer import get_android_sdk_root
from qai_hub_apps.utils.verify_result import VerifyResult
from qai_hub_models.models.common import QAIRTVersion

# Names of dependencies that are verified by this class.
LITERT_DEP = "com.google.ai.edge.litert:litert"
TFLITE_DEP = "org.tensorflow:tensorflow-lite"
TFLITE_SUPPORT_DEP = "org.tensorflow:tensorflow-lite-support"
TFLITE_GPU_DEP = "org.tensorflow:tensorflow-lite-gpu"
TFLITE_GPU_API_DEP = "org.tensorflow:tensorflow-lite-gpu-api"
TFLITE_GPU_PLUGIN_DEP = "org.tensorflow:tensorflow-lite-gpu-delegate-plugin"
ONNX_DEP = "com.microsoft.onnxruntime:onnxruntime"
QAIRT_DEP = "com.qualcomm.qti:qnn-runtime"
QAIRT_TFLITE_DELEGATE_DEP = "com.qualcomm.qti:qnn-litert-delegate"


def verify_android_app_versions_match(
    app_root: str | os.PathLike,
    versions: VersionsRegistry = VersionsRegistry.load(),
) -> VerifyResult:
    """
    Verifies that the Android app at the given root directory
    uses the same versions of runtimes as are listed in the versions yaml.

    Parameters
    ----------
    app_root
        Path to the root directory of the application source code.
    versions
        Registry of version information for dependencies and components.

    Returns
    -------
    VerifyResult
        The warnings and errors produced by this verification process.
    """
    errors = []
    warnings = []

    try:
        get_android_sdk_root()
    except ValueError as e:
        errors.append(e.args[0])
        return VerifyResult(errors)

    def verify_same_as_versions_yaml_or_add_error(
        name, app_version, required_version
    ) -> bool:
        if app_version != required_version:
            errors.append(
                f"App uses {name} version {app_version}, expected {required_version} as defined in versions.yaml."
            )
            return False
        return True

    # Check declared Android API level
    api_versions = extract_api_versions(app_root)
    verify_same_as_versions_yaml_or_add_error(
        "Android min API", api_versions["minAPI"], versions.android_min_api
    )
    verify_same_as_versions_yaml_or_add_error(
        "Android target API", api_versions["targetAPI"], versions.android_target_api
    )
    verify_same_as_versions_yaml_or_add_error(
        "Android compile API", api_versions["compileAPI"], versions.android_compile_api
    )

    # Check java version
    compile_api_java_version = get_java_target_compatibility_version(
        versions.android_compile_api
    )
    min_api_java_version = get_java_target_compatibility_version(
        versions.android_min_api
    )
    if compile_api_java_version > min_api_java_version:
        warnings.append(
            f"Minimum Android API level {versions.android_min_api} supports up Java {min_api_java_version}, but compile API level {versions.android_compile_api} targets Java {compile_api_java_version}. Using Java {compile_api_java_version} features may result in crashes on Android API {versions.android_min_api}."
        )

    java_major_version = int(
        versions.java_sdk.split(".")[0]
    )  # convert "17.0.15-tem" -> 17
    verify_same_as_versions_yaml_or_add_error(
        "javaTargetCompatibility",
        api_versions["javaSourceCompatibility"],
        java_major_version,
    )
    verify_same_as_versions_yaml_or_add_error(
        "javaSourceCompatibility",
        api_versions["javaTargetCompatibility"],
        java_major_version,
    )

    # Check ML runtime version
    deps = get_project_dependencies(app_root)

    # TF Lite + Dependencies
    if LITERT_DEP in deps:
        errors.append("AI Hub does not yet target LiteRT. Use TensorFlow Lite instead.")
    if TFLITE_DEP in deps:
        required_tflite_version = versions.tf_lite
        app_tflite_version = deps[TFLITE_DEP]
        verify_same_as_versions_yaml_or_add_error(
            TFLITE_DEP, app_tflite_version, required_tflite_version
        )

        for dep in [TFLITE_GPU_DEP, TFLITE_GPU_API_DEP]:
            if dep_version := deps.get(dep):
                if dep_version != app_tflite_version:
                    errors.append(
                        f"Dependencies {TFLITE_DEP} ({app_tflite_version}) and {dep} ({dep_version}) should be the same version."
                    )

        required_tflite_support_version = versions.tf_lite_support
        litert_support_version: str | None = deps.get(TFLITE_SUPPORT_DEP)
        if litert_support_version is not None:
            verify_same_as_versions_yaml_or_add_error(
                TFLITE_SUPPORT_DEP,
                litert_support_version,
                required_tflite_support_version,
            )

        if QAIRT_TFLITE_DELEGATE_DEP not in deps:
            errors.append(
                f"Missing {QAIRT_TFLITE_DELEGATE_DEP} (QAIRT delegate for TF Lite) in app dependencies."
            )

    # ONNX
    if ONNX_DEP in deps:
        required_onnx_version = versions.onnx_runtime
        app_onnx_version = deps[ONNX_DEP]
        verify_same_as_versions_yaml_or_add_error(
            ONNX_DEP, app_onnx_version, required_onnx_version
        )

    # QAIRT + QAIRT-Dependent
    if QAIRT_DEP in deps:
        required_qairt_version = versions.qairt_sdk
        app_qairt_version = deps[QAIRT_DEP]
        req_v = QAIRTVersion(required_qairt_version, validate_exists_on_ai_hub=False)
        app_v = QAIRTVersion(app_qairt_version, validate_exists_on_ai_hub=False)
        same = verify_same_as_versions_yaml_or_add_error(
            "QAIRT", app_v.api_version, req_v.api_version
        )
        if same and app_v.framework.patch != req_v.framework.patch:
            warnings.append(
                f"versions.yaml ({req_v.full_version}) and app ({app_v.full_version}) QAIRT API versions match, but patch versions differ."
            )

        if (
            QAIRT_TFLITE_DELEGATE_DEP in deps
            and deps[QAIRT_TFLITE_DELEGATE_DEP] != app_qairt_version
        ):
            errors.append(
                f"Dependencies {QAIRT_DEP} ({app_qairt_version}) and {QAIRT_TFLITE_DELEGATE_DEP} ({deps[QAIRT_TFLITE_DELEGATE_DEP]}) should be the same version."
            )

    return VerifyResult(errors, warnings)


def extract_api_versions(app_root: str | os.PathLike) -> dict[str, int]:
    """
    Extract the
        * android (min, target, compile) API levels
        * Java (source, target) API levels
    from the build.gradle in the given app folder.

    Parameters
    ----------
    app_root
        Path to the root directory of the application source code.

    Returns
    -------
    dict[str, int]
        Map from version information -> version. Example:
        dict(
            minAPI=30
            targetAPI=34
            compileAPI=34
            javaSourceCompatibility=11
            javaTargetCompatibility=11
        )
    """
    result = subprocess.run(
        "gradle printAPIVersion -q",
        cwd=app_root,
        capture_output=True,
        text=True,
        shell=True,
    ).stdout.split("\n")
    result_split = [x.strip().split("=", maxsplit=1) for x in result]
    return {x[0]: int(x[1]) for x in result_split}


def get_project_dependencies(
    project_root: str | os.PathLike,
    subproject: str | None = None,
    configuration: str = "releaseRuntimeClasspath",
    env: dict[str, Any] | None = None,
) -> dict[str, str]:
    """
    Get top-level (non-recursive) dependencies for this project + configuration, in { name: version } format.
    WARNING: All required build tools for this project need to be available to gradle for this to work. Otherwise output may be empty.

    Parameters
    ----------
    project_root
        Gradle project root.
    subproject
        Subproject name. Ex 'mySubproject:nestedSubProject'
    configuration
        Project configuration to get deps for.
    env
        Gradle execution environment.

    Returns
    -------
    dict[str, str]
        Map from dependency name -> dependency version
    """
    subproject = f":{subproject}" if subproject is not None else ""
    deps_out = subprocess.run(
        f"gradle {subproject}dependencies  --configuration {configuration}",
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True,
        shell=True,
    ).stdout.split("\n")
    deps: dict[str, str] = dict()
    for line in deps_out:
        # Match the following output from Gradle:
        #   +--- mypackage:version
        #    --- mypackage:version
        # And save them to the `deps` dictionary.
        if match := re.match("^(\\+---|\\\---) (.*):([^\\s]*)", line):  # noqa: W605
            if match.group(2) not in deps:
                deps[match.group(2)] = match.group(3)
            elif deps[match.group(2)] != match.group(3):
                print(
                    f"Warning: found 2 different versions of {match.group(2)} in deps: {deps[match.group(2)]} and {match.group(3)}"
                )
    return deps


def get_java_target_compatibility_version(platform_version: int) -> int:
    """
    Get the maximum version of Java that can be used for this Android platform version.

    Parameters
    ----------
    platform_version
        Android platform version.

    Returns
    -------
    int
        Max java version supported by the Android platform.
    """
    if platform_version > 34 or platform_version < 30:
        raise NotImplementedError()
    if platform_version == 34:
        return 17
    elif platform_version >= 30:
        return 11
    raise NotImplementedError()
