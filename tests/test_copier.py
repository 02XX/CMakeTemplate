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
    assert (dst / "LICENSE").is_file()
    assert not (dst / "libs").exists()

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

    for path in cmake_lists(dst):
        assert_no_blank_lines(path)


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
