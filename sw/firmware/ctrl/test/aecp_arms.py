# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Firmware AECP arms on the existing host harness."""
from __future__ import annotations
import sys
from pathlib import Path
from ctrl_build import CTRL, HERE, ROOT, HARNESS, C_FLAGS, Tree, Outcome, Refusal, run
import fw_gtest

AEC_P_SOURCES = ("aecp.c", "aecp_commands.c", "aecp_maps.c", "aecp_image.c", "aecp_state.c")


def core_arm(tree: Tree, config: Path, interfaces: int = 1, mailbox: bool = False, nvm: bool = False,
             selected: str = "*") -> Outcome:
    """The protocol owner against explicit environment ports at either interface count."""
    out = tree.out / f"aecp-{'mailbox' if mailbox else 'core'}-{config.stem}-if{interfaces}"
    out.mkdir(parents=True, exist_ok=True)
    result = run([sys.executable, "-B", str(CTRL / "aecp/aecp_entity.py"),
                  str(config), "-o", str(out / "aecp_entity_gen.h")])
    if result.returncode:
        raise Refusal(result.stderr)
    inc = [f"-I{tree.src / 'aecp'}", f"-I{tree.src / 'wire'}", f"-I{HARNESS}",
           f"-I{out}", f"-DAECP_TEST_INTERFACES={interfaces}"]
    sources = [tree.src / "aecp" / n for n in AEC_P_SOURCES]
    host_sources = []
    if nvm:
        sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))
        import nvm_bench
        shape = nvm_bench.shape_inputs(config, out / "shape")
        gen = out / "gen"
        nvm_bench.write_headers(gen, nvm_bench.shape_header(shape.shape, shape.donor, shape.ident), shape.clock_hz)
        directory = ROOT / "sw/firmware/ctrl_nvm"
        inc += [f"-I{gen}", f"-I{directory}", "-DAECP_TEST_NVM"]
        sources += [tree.src / "aecp/aecp_nvm.c", directory / "nvm_klj2.c", directory / "nvm_store.c"]
        host_sources += [directory / "host/nvm_fmodel.c"]
    if mailbox:
        from srp_arms import prepared
        variant, extra = prepared(tree, interfaces, out, config)
        inc += [*extra, "-DAECP_TEST_MAILBOX"]
        sources += [tree.src / "aecp/aecp_mbx.c", tree.src / "loop/ctrl_loop.c", variant / "mbx/mbx.c"]
        host_sources += [tree.src / "host" / n for n in ("mbx_model.c", "mbx_plat_host.c")]
    try:
        objects = fw_gtest.compile_c(tree.build, C_FLAGS, inc, sources, out / "firmware")
        objects += fw_gtest.compile_c(tree.build, C_FLAGS, inc, host_sources, out / "host", measured=False)
        tests = fw_gtest.compile_tests(tree.build, inc, [HERE / "test_aecp.cpp"], out / "tests")
        exe = fw_gtest.link(tree.build, [*objects, *tests, fw_gtest.main_object(tree.build, out / "main")],
                            out / "suite")
        ok, log = fw_gtest.run_binary(exe, [f"--gtest_filter={selected}"])
    except fw_gtest.BuildError as error:
        raise Refusal(str(error)) from error
    (out / "run.log").write_text(log, encoding="utf-8")
    return Outcome(out.name, 0 if ok else 1, log)


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
    parser.add_argument("--core", action="store_true")
    parser.add_argument("--mailbox", action="store_true")
    parser.add_argument("--nvm", action="store_true")
    parser.add_argument("--filter", default="*")
    parser.add_argument("--interfaces", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    tree = Tree(CTRL, args.output, args.output / "reuse", fw_gtest.Build(coverage=args.coverage, jobs=4))
    result = core_arm(tree, args.config, args.interfaces, args.mailbox, args.nvm, args.filter) if args.core or args.mailbox or args.nvm else image_arm(tree, args.config)
    print(result.log)
    raise SystemExit(result.rc)
