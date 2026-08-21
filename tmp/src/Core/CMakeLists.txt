add_library(tmp_Core)
add_library(tmp::Core ALIAS tmp_Core)
target_compile_features(tmp_Core PUBLIC "cxx_std_${CMAKE_CXX_STANDARD}")
target_sources(
    tmp_Core
    PRIVATE
        Core.cpp
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS "${PROJECT_SOURCE_DIR}/include"
        FILES "${PROJECT_SOURCE_DIR}/include/tmp/Core.hpp"
)
project_set_warnings(tmp_Core)
project_enable_sanitizers(tmp_Core)
set_target_properties(tmp_Core PROPERTIES EXPORT_NAME "Core")
