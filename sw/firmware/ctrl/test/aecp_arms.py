# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Firmware AECP arms on the existing host harness."""
from __future__ import annotations
import sys
from pathlib import Path
from ctrl_build import CTRL, HERE, ROOT, HARNESS, C_FLAGS, Tree, Outcome, Refusal, run
import fw_gtest


def image_arm(tree: Tree, config: Path) -> Outcome:
    """Load every descriptor from a real generated shape and grade refusals."""
    out = tree.out / ("aecp-image-" + config.stem)
    out.mkdir(parents=True, exist_ok=True)
    result = run([sys.executable, "-B", str(CTRL / "aecp/aecp_entity.py"),
                  str(config), "-o", str(out / "aecp_entity_gen.h")])
    if result.returncode:
        raise Refusal(result.stderr)
    inc = [f"-I{tree.src / 'aecp'}", f"-I{tree.src / 'wire'}",
           f"-I{HARNESS}", f"-I{out}"]
    try:
        objects = fw_gtest.compile_c(tree.build, C_FLAGS, inc,
                                     [tree.src / "aecp/aecp_image.c"], out / "firmware")
        tests = fw_gtest.compile_tests(tree.build, inc, [HERE / "test_aecp_image.cpp"], out / "tests")
        exe = fw_gtest.link(tree.build, [*objects, *tests, fw_gtest.main_object(tree.build, out / "main")],
                            out / "suite")
        ok, log = fw_gtest.run_binary(exe)
    except fw_gtest.BuildError as error:
        raise Refusal(str(error)) from error
    (out / "run.log").write_text(log, encoding="utf-8")
    return Outcome(out.name, 0 if ok else 1, log)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml")
    parser.add_argument("--coverage", action="store_true")
    args = parser.parse_args()
    result = image_arm(Tree(CTRL, args.output, args.output / "reuse",
                            fw_gtest.Build(coverage=args.coverage, jobs=4)), args.config)
    print(result.log)
    raise SystemExit(result.rc)
