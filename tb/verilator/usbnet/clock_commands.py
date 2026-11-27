#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Connect the existing AECP command fixture to the fabric LED predicate.

The firmware is compiled without LED code. Only the test executable links the
RTL model, which receives explicit media levels after each real command.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
import aecp_arms
import fw_gtest
from ctrl_build import CTRL, STACK, Tree, stack_pin


def main() -> int:
    """Use the firmware's compiler and generated Arty descriptor model."""
    out = Path(sys.argv[1]).resolve()
    rtl = Path(sys.argv[2]).resolve()
    stack_pin(STACK)
    runtime = Path(subprocess.check_output(["verilator", "-getenv", "VERILATOR_ROOT"], text=True).strip())
    compile_tests, link = fw_gtest.compile_tests, fw_gtest.link

    def tests(build: fw_gtest.Build, includes: list[str], sources: list[Path],
              directory: Path, **kwargs: object) -> list[Path]:
        """Compile the unchanged command fixture followed by the fabric checks."""
        if not any(source.name == "test_aecp.cpp" for source in sources):
            return compile_tests(build, includes, sources, directory, **kwargs)
        directory.mkdir(parents=True, exist_ok=True)
        combined = directory / "clock_fixture.cpp"
        combined.write_text((CTRL / "test/test_aecp.cpp").read_text() + "\n" +
                            (HERE / "test_clock.cpp").read_text())
        return compile_tests(build, [*includes, f"-I{CTRL / 'test'}", f"-I{HERE}", f"-I{rtl}",
                                    "-isystem", str(runtime / "include")],
                             [combined], directory, **kwargs)

    def linked(build: fw_gtest.Build, objects: list[Path], executable: Path) -> Path:
        """Link the fabric model into the test executable only."""
        extra = [rtl / name for name in ("VKL_status_led_truth__ALL.a", "verilated.o", "verilated_threads.o")]
        return link(build, [*objects, *extra], executable)

    fw_gtest.compile_tests, fw_gtest.link = tests, linked
    result = aecp_arms.core_arm(Tree(CTRL, out, out / "reuse", fw_gtest.Build(jobs=4), STACK),
                              ROOT / "configs/endstation_arty_split.yaml", selected="FabricClock.*")
    print(result.log)
    return result.rc


if __name__ == "__main__":
    raise SystemExit(main())
