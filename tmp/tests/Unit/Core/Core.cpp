#include <tmp/Core.hpp>

#include <gtest/gtest.h>

#include <string>

TEST(Core, GreetContainsName)
{
    const std::string greeting = tmp::Core::greet("Ada");
    EXPECT_NE(greeting.find("Ada"), std::string::npos);
}
