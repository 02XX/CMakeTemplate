# tmp

A modern C++ project

## 构建

CMake 3.31+，[vcpkg](https://vcpkg.io/)（`VCPKG_ROOT`）。

```bash
cmake --list-presets
cmake --workflow --preset windows-arm64-msvc-vs2022-debug
```

分步：`cmake --preset …` → `cmake --build --preset …` → `ctest --preset …` → `cpack --preset …`。

本机覆盖写 `CMakeUserPresets.json`（gitignore）。

## 结构

```
include/tmp/   # 公开头  #include <tmp/Core.hpp>
src/<模块>/                  # 实现
apps/<程序>/                 # 入口
tests/Unit/<模块>/         # 单测
tests/Integration/           # 集成测试
```

加库：`include/tmp/Foo.hpp`、`src/Foo/`，再在 `src/CMakeLists.txt` 里 `add_subdirectory(Foo)`；单测复制 `tests/Unit/Core/`。

加程序：复制 `apps/tmp/`，在 `apps/CMakeLists.txt` 里 `add_subdirectory`。


## 依赖

```bash
"$VCPKG_ROOT/vcpkg" add port fmt
"$VCPKG_ROOT/vcpkg" x-update-baseline
```

`vcpkg.json` / `vcpkg-configuration.json` 进 git。CI 需要完整克隆 vcpkg，浅克隆可能对不上 baseline。



## 许可

GPL-3.0。见 `LICENSE`。


