# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html.
# For more examples on how to use CMake, see https://github.com/android/ndk-samples.

# Sets the minimum CMake version required for this project.
cmake_minimum_required(VERSION 3.22.1)

# Declares the project name. The project name can be accessed via ${ PROJECT_NAME},
# Since this is the top level CMakeLists.txt, the project name is also accessible
# with ${CMAKE_PROJECT_NAME} (both CMake variables are in-sync within the top level
# build script scope).
project("chatapp")

set(GENIE_HEADERS_PATH "${QNN_SDK_ROOT_PATH}/include/Genie")
set(GENIE_LIB_PATH "${QNN_SDK_ROOT_PATH}/lib/aarch64-android/libGenie.so")

include_directories("includes")

# Include Genie headers here
if(EXISTS ${GENIE_HEADERS_PATH})
    include_directories(${GENIE_HEADERS_PATH})
else()
    message(FATAL_ERROR "Cannot find Genie headers at ${GENIE_HEADERS_PATH}. Please set QNN_SDK_ROOT_PATH in JNI Cmake file.")
endif()

add_library(${CMAKE_PROJECT_NAME} SHARED
        # List C/C++ source files with relative paths to this CMakeLists.txt.
        PromptHandler.cpp
        GenieWrapper.cpp
        GenieLib.cpp)

# Link libGenie.so here
if(EXISTS ${GENIE_LIB_PATH})
    target_link_libraries(${CMAKE_PROJECT_NAME}
            "${GENIE_LIB_PATH}"
            android
            log)
else()
    message(FATAL_ERROR "Cannot find libGenie.so at ${GENIE_LIB_PATH}. Please set QNN_SDK_ROOT_PATH in JNI Cmake file.")
endif()
