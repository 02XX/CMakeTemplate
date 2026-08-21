from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

import pytest
from copier import run_copy

REPO = Path(__file__).resolve().parents[1]


def generate(dst: Path, data: Mapping[str, object] | None = None) -> Path:
    run_copy(
        src_path=str(REPO),
        dst_path=str(dst),
        data=dict(data or {}),
        defaults=True,
        overwrite=True,
        vcs_ref="HEAD",
        unsafe=True,
    )
    return dst


def cmake_lists(root: Path) -> list[Path]:
    return sorted(root.rglob("CMakeLists.txt"))


def toolchain_names(root: Path) -> set[str]:
    return {p.name for p in (root / "cmake" / "toolchains").glob("*.cmake")}


def configure_preset_names(root: Path) -> set[str]:
    presets = json.loads((root / "CMakePresets.json").read_text(encoding="utf-8"))
    return {p["name"] for p in presets["configurePresets"]}


def assert_no_blank_lines(path: Path) -> None:
    blanks = [i for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1) if line.strip() == ""]
    assert not blanks, f"{path} has blank lines: {blanks}"


def test_default_layout(tmp_path: Path) -> None:
    dst = generate(tmp_path / "MEngine", {"project_name": "MEngine"})

    assert (dst / "include" / "MEngine" / "Core.hpp").is_file()
    assert [p.name for p in (dst / "include").iterdir()] == ["MEngine"]
    assert (dst / "src" / "Core" / "Core.cpp").is_file()
    assert (dst / "src" / "Core" / "CMakeLists.txt").is_file()
    assert (dst / "apps" / "MEngine" / "main.cpp").is_file()
    assert (dst / "tests" / "Unit" / "Core" / "Core.cpp").is_file()
    assert (dst / "tests" / "Integration" / "smoke.cpp").is_file()
    assert (dst / "CMakeUserPresets.json").is_file()
    assert (dst / ".github" / "workflows" / "ci.yml").is_file()
    assert (dst / ".github" / "workflows" / "cd.yml").is_file()
    assert (dst / "LICENSE").is_file()
    assert not (dst / "libs").exists()

    toolchains = toolchain_names(dst)
    assert "windows-x64-msvc.cmake" in toolchains
    assert "linux-x64-gcc.cmake" in toolchains
    assert "macos-arm64-clang.cmake" in toolchains

    vcpkg = json.loads((dst / "vcpkg.json").read_text(encoding="utf-8"))
    assert vcpkg["name"] == "mengine"
    assert "gtest" in vcpkg.get("dependencies", [])
    assert (dst / "vcpkg-configuration.json").is_file()

    main = (dst / "apps" / "MEngine" / "main.cpp").read_text(encoding="utf-8")
    assert "#include <MEngine/Core.hpp>" in main

    unit = (dst / "tests" / "Unit" / "Core" / "CMakeLists.txt").read_text(encoding="utf-8")
    assert unit.count("add_executable") == 1
    assert unit.count("target_link_libraries") == 1
    assert "MEngine::Core" in unit

    user_presets = json.loads((dst / "CMakeUserPresets.json").read_text(encoding="utf-8"))
    presets = json.loads((dst / "CMakePresets.json").read_text(encoding="utf-8"))
    assert user_presets["version"] == presets["version"]
    names = {p["name"] for p in presets["configurePresets"]}
    assert "vcpkg" in names
    assert "windows-x64-msvc-vs2022" in names
    assert "linux-x64-gcc-ninja-debug" in names
    assert "macos-arm64-clang-ninja-debug" in names

    for path in cmake_lists(dst):
        assert_no_blank_lines(path)


def test_multi_module_without_optional_bits(tmp_path: Path) -> None:
    dst = generate(
        tmp_path / "MEngine",
        {
            "project_name": "MEngine",
            "modules": ["Core", "Net"],
            "apps": ["MEngine", "Tool"],
            "enable_testing": False,
            "use_vcpkg": False,
            "use_github_actions": False,
            "license": "none",
        },
    )

    assert (dst / "include" / "MEngine" / "Core.hpp").is_file()
    assert (dst / "include" / "MEngine" / "Net.hpp").is_file()
    assert (dst / "src" / "Net" / "Net.cpp").is_file()
    assert (dst / "apps" / "Tool" / "main.cpp").is_file()
    assert not (dst / "tests").exists()
    assert not (dst / ".github").exists()
    assert not (dst / "LICENSE").exists()
    assert not (dst / "vcpkg.json").exists()

    src_cmake = (dst / "src" / "CMakeLists.txt").read_text(encoding="utf-8").splitlines()
    assert src_cmake == ["add_subdirectory(Core)", "add_subdirectory(Net)"]

    app_cmake = (dst / "apps" / "MEngine" / "CMakeLists.txt").read_text(encoding="utf-8")
    assert "MEngine::Core" in app_cmake
    assert "MEngine::Net" in app_cmake

    presets = json.loads((dst / "CMakePresets.json").read_text(encoding="utf-8"))
    names = {p["name"] for p in presets["configurePresets"]}
    assert "vcpkg" not in names
    assert "windows-x64-msvc-vs2022" in names

    for path in cmake_lists(dst):
        assert_no_blank_lines(path)


def test_windows_x64_msvc_only(tmp_path: Path) -> None:
    dst = generate(
        tmp_path / "MEngine",
        {
            "project_name": "MEngine",
            "platforms": ["windows"],
            "architectures": ["x64"],
            "windows_compilers": ["msvc"],
        },
    )

    assert toolchain_names(dst) == {"windows-x64-msvc.cmake"}

    names = configure_preset_names(dst)
    assert "base" in names
    assert "vcpkg" in names
    assert "windows" in names
    assert "windows-x64-msvc-vs2022" in names
    assert not any(n.startswith("linux") or n.startswith("macos") for n in names)
    assert not any("clang" in n or "arm64" in n for n in names)

    ci = (dst / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "windows-x64-msvc-vs2022-debug" in ci
    assert "ubuntu-latest" not in ci
    assert "macos-latest" not in ci
    assert "lukka/run-vcpkg@v11" in ci
    assert "lukka/run-cmake@v10.9" in ci
    assert "workflowPreset" in ci

    cd = (dst / ".github" / "workflows" / "cd.yml").read_text(encoding="utf-8")
    assert "windows-x64-msvc-vs2022-release" in cd
    assert "workflowPreset" in cd
    assert "lukka/run-vcpkg@v11" in cd
    assert "lukka/run-cmake@v10.9" in cd

    readme = (dst / "README.md").read_text(encoding="utf-8")
    assert "windows-x64-msvc-vs2022-debug" in readme
    assert "linux-" not in readme
    assert "macos-" not in readme


def test_linux_x64_gcc_ninja_only(tmp_path: Path) -> None:
    dst = generate(
        tmp_path / "MEngine",
        {
            "project_name": "MEngine",
            "platforms": ["linux"],
            "architectures": ["x64"],
            "linux_compilers": ["gcc"],
            "linux_generators": ["ninja"],
            "use_vcpkg": False,
        },
    )

    assert toolchain_names(dst) == {"linux-x64-gcc.cmake"}

    names = configure_preset_names(dst)
    assert "linux-x64-gcc-ninja-debug" in names
    assert "linux-x64-gcc-ninja-release" in names
    assert not any("make" in n for n in names)
    assert not any(n.startswith("windows") or n.startswith("macos") for n in names)

    ci = (dst / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "linux-x64-gcc-ninja-debug" in ci
    assert "windows-latest" not in ci
    assert "macos-latest" not in ci
    assert "workflowPreset" in ci
    assert "lukka/run-cmake@v10.9" in ci
    assert "lukka/run-vcpkg@v11" not in ci

    cd = (dst / ".github" / "workflows" / "cd.yml").read_text(encoding="utf-8")
    assert "linux-x64-gcc-ninja-release" in cd
    assert "workflowPreset" in cd


def test_windows_arm64_clang_ci_uses_substitute_preset(tmp_path: Path) -> None:
    dst = generate(
        tmp_path / "MEngine",
        {
            "project_name": "MEngine",
            "platforms": ["windows"],
            "architectures": ["arm64"],
            "windows_compilers": ["clang"],
            "use_vcpkg": False,
        },
    )

    names = configure_preset_names(dst)
    assert "windows-arm64-clang-ninja-debug" in names
    assert "windows-x64-msvc-vs2022" not in names

    ci = (dst / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "windows-arm64-clang-ninja-debug" in ci
    assert "windows-x64-msvc-vs2022-debug" not in ci


def test_gpl_license(tmp_path: Path) -> None:
    dst = generate(tmp_path / "MEngine", {"project_name": "MEngine", "license": "gpl-3.0"})
    text = (dst / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in text
    assert "Version 3, 29 June 2007" in text


@pytest.mark.skipif(shutil.which("cmake") is None, reason="cmake not on PATH")
def test_cmake_list_presets(tmp_path: Path) -> None:
    dst = generate(tmp_path / "MEngine", {"project_name": "MEngine", "use_vcpkg": False})
    result = subprocess.run(
        ["cmake", "--list-presets"],
        cwd=dst,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "windows-x64-msvc-vs2022" in result.stdout


@pytest.mark.skipif(shutil.which("cmake") is None, reason="cmake not on PATH")
def test_cmake_list_presets_windows_only(tmp_path: Path) -> None:
    dst = generate(
        tmp_path / "MEngine",
        {
            "project_name": "MEngine",
            "platforms": ["windows"],
            "architectures": ["x64"],
            "windows_compilers": ["msvc"],
            "use_vcpkg": False,
        },
    )
    result = subprocess.run(
        ["cmake", "--list-presets"],
        cwd=dst,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "windows-x64-msvc-vs2022" in result.stdout
