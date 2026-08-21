add_executable(smokeTests smoke.cpp)
target_link_libraries(
    smokeTests
    PRIVATE
        tmp::Core
        GTest::gtest_main
)
project_set_warnings(smokeTests)
project_enable_sanitizers(smokeTests)
gtest_discover_tests(smokeTests)
