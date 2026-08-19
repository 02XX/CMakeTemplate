# CMakeTemplate

用 [Copier](https://copier.readthedocs.io/) 生成跨平台现代 C++ / CMake 工程。

生成出的项目自带：

- CMake 3.31+ 与 `CMakePresets.json`（Windows / Linux / macOS，MSVC / Clang / GCC）
- 按目标平台拆分的 toolchain 文件
- 可选 vcpkg（Presets/CI 接 toolchain；`vcpkg.json` 由 `--trust` 后的 `_tasks` 通过 `VCPKG_ROOT` 调用 `vcpkg new` 创建）
- clang-format / clang-tidy
- `include/<工程名>/`、`src/<模块>/`、`apps/<Name>/`
- `#include <MEngine/Module.hpp>`（vcpkg 名用小写 `project_slug`）
- GoogleTest + CTest（`tests/Unit`、`tests/Integration`）
- 可选 GitHub Actions CI

## 依赖

- Python 3.9+
- [Copier](https://copier.readthedocs.io/) 9.6+
- CMake 3.31+
- 编译器：MSVC、Clang 或 GCC
- 若启用 vcpkg：安装 [vcpkg](https://vcpkg.io/) 并设置 `VCPKG_ROOT`

```bash
uvx copier copy --trust --vcs-ref HEAD ./CMakeTemplate ../MyApp
```

`--trust` 才会跑 `_tasks`。启用 vcpkg 时任务用 `VCPKG_ROOT` 找可执行文件（不要求在 PATH 里），自动 `vcpkg new`，测试开启则再 `vcpkg add port gtest`。

未加 `--trust` 时手动：

```bash
"$VCPKG_ROOT/vcpkg" new --name <project_slug> --version <version>
"$VCPKG_ROOT/vcpkg" add port gtest
```

## 构建

进入生成出的项目后，用 preset 配置、编译、测试、打包：

```bash
cmake --workflow --preset windows-x64-msvc-vs2022-debug
cmake --workflow --preset linux-x64-gcc-ninja-debug
cmake --workflow --preset macos-arm64-clang-ninja-debug
```

查看全部 preset：

```bash
cmake --list-presets
```

本地覆盖（额外 cache 变量、环境变量、打开 CMake trace 等）写在 `CMakeUserPresets.json`，该文件已被 gitignore。

## 从模板更新

生成时会写入 `.copier-answers.yaml`。之后在项目根目录执行：

```bash
copier update
```

模板使用语义化 Git tag（`vX.Y.Z`）作为版本。请给本仓库打 tag，生成项目才能锁定并升级模板版本。

## 测试模板

```bash
uv run --group dev pytest
# 或
uvx --with pytest --with copier pytest
```

会用 Copier `--trust` 生成临时项目并执行 `_tasks`（需要 `VCPKG_ROOT`），检查目录、`CMakeLists.txt`、Presets，以及 `cmake --list-presets`（本机有 CMake 时）。

## 仓库结构

```
.
├── copier.yml          # Copier 问卷与设置
├── README.md           # 本说明
└── template/           # 真正拷贝到新项目的内容
    ├── CMakeLists.txt.jinja
    ├── CMakePresets.json.jinja
    ├── cmake/toolchains/
    └── ...
```
