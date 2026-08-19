# CMakeTemplate

用 [Copier](https://copier.readthedocs.io/) 生成跨平台现代 C++ / CMake 工程。

生成出的项目自带：

- CMake 3.31+ 与 `CMakePresets.json`（Windows / Linux / macOS，MSVC / Clang / GCC）
- 按目标平台拆分的 toolchain 文件
- 可选 vcpkg 清单模式（`vcpkg.json`；baseline 由使用者生成后自行钉死）
- clang-format / clang-tidy
- 公开头在顶层 `include/<包名>/`，库实现在 `src/<模块>/`，程序入口在 `apps/<Name>/`
- 头文件使用项目前缀：`#include <project/Module.hpp>`
- GoogleTest + CTest（`tests/Unit`、`tests/Integration`）
- GitHub Actions CI（可选）

## 依赖

- Python 3.9+
- [Copier](https://copier.readthedocs.io/) 9.6+
- CMake 3.31+
- 编译器：MSVC、Clang 或 GCC
- 若启用 vcpkg：安装 [vcpkg](https://vcpkg.io/) 并设置 `VCPKG_ROOT`

安装 Copier：

```bash
pipx install copier
```

## 生成项目

```bash
copier copy <本仓库路径或 Git URL> <新项目路径>
```

本地仓库、尚未打 tag 时需要指定 `HEAD`：

```bash
copier copy --vcs-ref HEAD ./CMakeTemplate ../MyApp
```

按提示填写工程名、库模块、可执行程序等。大部分问题都有默认值。全部使用默认值可以加 `--defaults`。

若生成时启用了 vcpkg，**进入新项目后先钉死 baseline**（用使用者本机的 vcpkg，模板不会预写提交哈希）：

```bash
cd <新项目路径>
vcpkg x-update-baseline --add-initial-baseline
```

生成结束时 Copier 也会打印这一步。把改过的 `vcpkg.json` 提交进 git。

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
