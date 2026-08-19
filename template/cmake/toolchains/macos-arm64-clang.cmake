include_guard(GLOBAL)

# Target: macos / arm64 / clang
set(CMAKE_SYSTEM_PROCESSOR "arm64" CACHE STRING "Target processor")
set(CMAKE_C_COMPILER "clang" CACHE FILEPATH "C compiler")
set(CMAKE_CXX_COMPILER "clang++" CACHE FILEPATH "C++ compiler")
set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "macOS target architecture")
