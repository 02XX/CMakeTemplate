#pragma once

#include <string>
#include <string_view>

namespace tmp::Core
{

[[nodiscard]] std::string greet(std::string_view name = "world");

} // namespace tmp::Core
