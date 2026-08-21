#include <tmp/Core.hpp>

#include <string>
#include <string_view>

namespace tmp::Core
{

std::string greet(std::string_view name)
{
    return "Hello from Core, " + std::string(name) + "!";
}

} // namespace tmp::Core
