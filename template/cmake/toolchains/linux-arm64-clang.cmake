include_guard(GLOBAL)

# Target: linux / arm64 / clang
set(CMAKE_SYSTEM_NAME "Linux" CACHE STRING "Target system")
set(CMAKE_SYSTEM_PROCESSOR "aarch64" CACHE STRING "Target processor")
set(CMAKE_C_COMPILER "clang" CACHE FILEPATH "C compiler")
set(CMAKE_CXX_COMPILER "clang++" CACHE FILEPATH "C++ compiler")
set(CMAKE_C_COMPILER_TARGET "aarch64-linux-gnu" CACHE STRING "C compiler target triple")
set(CMAKE_CXX_COMPILER_TARGET "aarch64-linux-gnu" CACHE STRING "C++ compiler target triple")
