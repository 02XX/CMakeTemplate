cmake_minimum_required(VERSION 3.31)
project(
    tmp
    VERSION 0.1.0
    DESCRIPTION "A modern C++ project"
    LANGUAGES CXX
)
include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/PreventInSourceBuilds.cmake")
include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/CompilerWarnings.cmake")
include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/Sanitizers.cmake")
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_OPTIMIZE_DEPENDENCIES ON)
set(CMAKE_COLOR_DIAGNOSTICS ON)
set(CMAKE_COMPILE_WARNING_AS_ERROR OFF)
option(ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
option(ENABLE_SANITIZER_UNDEFINED "Enable undefined-behavior sanitizer" OFF)
option(ENABLE_SANITIZER_LEAK "Enable leak sanitizer" OFF)
option(ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
add_subdirectory(src)
add_subdirectory(apps)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
install(
    TARGETS
        tmp_Core
        tmp
    EXPORT tmpTargets
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    FILE_SET HEADERS DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)
install(
    EXPORT tmpTargets
    FILE tmpTargets.cmake
    NAMESPACE tmp::
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/tmp"
)
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/tmpConfig.cmake"
    INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/tmp"
)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/tmpConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion
)
install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/tmpConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/tmpConfigVersion.cmake"
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/tmp"
)
if(PROJECT_IS_TOP_LEVEL)
    include(CTest)
    if(BUILD_TESTING)
        add_subdirectory(tests)
    endif()
endif()
set(CPACK_PACKAGE_NAME "tmp")
set(CPACK_PACKAGE_VENDOR "${PROJECT_NAME}")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "${PROJECT_DESCRIPTION}")
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_GENERATOR "TGZ")
if(WIN32)
    set(CPACK_GENERATOR "ZIP")
endif()
include(CPack)
