add_executable(tmp main.cpp)
add_executable(tmp::tmp ALIAS tmp)
target_compile_features(tmp PRIVATE "cxx_std_${CMAKE_CXX_STANDARD}")
target_link_libraries(
    tmp
    PRIVATE
        tmp::Core
)
project_set_warnings(tmp)
project_enable_sanitizers(tmp)
set_target_properties(tmp PROPERTIES EXPORT_NAME "tmp")
