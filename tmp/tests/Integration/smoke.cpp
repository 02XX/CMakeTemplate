
#include <tmp/Core.hpp>

#include <gtest/gtest.h>

TEST(Smoke, AllModulesLink)
{

    EXPECT_FALSE(tmp::Core::greet().empty());

}
