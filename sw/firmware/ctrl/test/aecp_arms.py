# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Firmware AECP arms on the existing host harness."""
from __future__ import annotations
import sys
from pathlib import Path
from ctrl_build import (CTRL, HERE, ROOT, HARNESS, C_FLAGS, STACK, STACK_INCLUDE, STACK_TESTS, Tree, Outcome, Refusal,
                        run, source, stack_pin)
import fw_gtest

AECP_SOURCES = ("aecp.c", "aecp_commands.c", "aecp_maps.c", "aecp_image.c", "aecp_state.c")


def saved_state(tree: Tree, config: Path, out: Path) -> tuple[list, list, list]:
    """Generate the F1 record geometry and bind its real host flash device."""
    sys.path.insert(0, str(ROOT / "sw/firmware/ctrl_nvm/test"))
    import nvm_bench
    shape = nvm_bench.shape_inputs(config, out / "shape")
    gen = out / "gen"
    nvm_bench.write_headers(gen, nvm_bench.shape_header(shape.shape, shape.donor, shape.ident), shape.clock_hz)
    directory = ROOT / "sw/firmware/ctrl_nvm"
    inc = [f"-I{gen}", f"-I{directory}", "-DAECP_TEST_NVM"]
    sources = [tree.src / "aecp/aecp_nvm.c", directory / "nvm_klj2.c", directory / "nvm_store.c"]
    return inc, sources, [directory / "host/nvm_fmodel.c"]


def mailbox_sources(tree: Tree, config: Path, interfaces: int, out: Path) -> tuple[list, list, list]:
    """Compile the adapter against the generated one- or two-interface contract."""
    from srp_arms import prepared
    variant, extra = prepared(tree, interfaces, out, config)
    sources = [tree.src / "aecp/aecp_mbx.c", tree.src / "loop/ctrl_loop.c", variant / "mbx/mbx.c"]
    host = [tree.src / "host" / name for name in ("mbx_model.c", "mbx_plat_host.c")]
    return [*extra, "-DAECP_TEST_MAILBOX"], sources, host


def application_sources(tree: Tree) -> tuple[list, list, list]:
    """Use the existing F0-F4 composition and the deferred AECP bridge."""
    from ctrl_build import PORTABLE
    from ctrl_arms import lwsrp_pin
    from srp_arms import LWSRP_SOURCES
    lw = ROOT / "third_party/lwSRP"
    lwsrp_pin(lw)
    inc = ["-DAECP_TEST_APP", "-DLWSRP_MILAN=1", f"-I{lw/'src/include'}", f"-I{lw/'src'}"]
    sources = [source(tree.src, tree.stack, n) for n in PORTABLE if n not in ("loop/ctrl_loop.c", "mbx/mbx.c")]
    sources += [tree.src / n for n in ("app/ctrl_app_aecp.c", "app/ctrl_app_srp.c", "srp/srp_mbx.c")]
    sources += [lw / "src" / n for n in LWSRP_SOURCES]
    return inc, sources, []


def core_arm(tree: Tree, config: Path, interfaces: int = 1, mode: str = "core",
             selected: str = "*") -> Outcome:
    """The protocol owner against explicit environment ports at either interface count."""
    app = mode == "app"
    debug = mode == "debug"
    mailbox = app or mode == "mailbox"
    nvm = app or mode == "nvm"
    out = tree.out / f"aecp-{'mailbox' if mailbox else 'core'}-{config.stem}-if{interfaces}"
    out.mkdir(parents=True, exist_ok=True)
    result = run([sys.executable, "-B", str(CTRL / "aecp/aecp_entity.py"),
                  str(config), "-o", str(out / "aecp_entity_gen.h")])
    if result.returncode:
        raise Refusal(result.stderr)
    inc = [f"-I{tree.src / 'aecp'}", f"-I{tree.stack / STACK_INCLUDE}", f"-I{HARNESS}",
           f"-I{out}", f"-I{tree.src / 'test'}", f"-DAECP_TEST_INTERFACES={interfaces}"]
    sources = [tree.src / "aecp" / n for n in AECP_SOURCES]
    host_sources = []
    groups = []
    if nvm:
        groups.append(saved_state(tree, config, out))
    if mailbox:
        groups.append(mailbox_sources(tree, config, interfaces, out))
    if app:
        groups.append(application_sources(tree))
    for extra, modules, host in groups:
        inc += extra
        sources += modules
        host_sources += host
    if debug:
        inc += ["-DCTRL_REENTRY_ASSERT"]
    test_source = "test_aecp_debug.cpp" if debug else "test_aecp.cpp"
    try:
        objects = fw_gtest.compile_c(tree.build, C_FLAGS, inc, sources, out / "firmware", measured=not debug)
        objects += fw_gtest.compile_c(tree.build, C_FLAGS, inc, host_sources, out / "host", measured=False)
        tests = fw_gtest.compile_tests(tree.build, [*inc, f"-I{STACK_TESTS}"], [HERE / test_source], out / "tests")
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
    inc = [f"-I{tree.src / 'aecp'}", f"-I{tree.stack / STACK_INCLUDE}",
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


def all_arms(tree: Tree) -> list[Outcome]:
    """Full application on both contracts, plus every builder image and the debug guard."""
    shipping = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    results = [core_arm(tree, shipping, i, mode="app") for i in (1, 2)]
    results += [image_arm(tree, p) for p in sorted((ROOT / "configs").glob("endstation_*.yaml"))]
    if not tree.build.coverage:
        results.append(core_arm(Tree(tree.src, tree.out / "debug", tree.reuse, tree.build, tree.stack), shipping,
                                mode="debug"))
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml")
    parser.add_argument("--coverage", action="store_true")
    parser.add_argument("--asan", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--core", action="store_true")
    parser.add_argument("--mailbox", action="store_true")
    parser.add_argument("--nvm", action="store_true")
    parser.add_argument("--filter", default="*")
    parser.add_argument("--app", action="store_true")
    parser.add_argument("--interfaces", type=int, choices=(1, 2), default=1)
    parser.add_argument("--stack", type=Path, default=STACK, help="the tsn-c-stack checkout (default: the submodule)")
    args = parser.parse_args()
    try:
        print(f"tsn-c-stack at {stack_pin(args.stack.resolve())}", flush=True)
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        raise SystemExit(2) from exc
    build = fw_gtest.Build(coverage=args.coverage, address_sanitizer=args.asan, jobs=4)
    tree = Tree(CTRL, args.output, args.output / "reuse", build, args.stack.resolve())
    mode = next((n for n in ("app", "debug", "mailbox", "nvm", "core") if getattr(args, n)), "image")
    result = (image_arm(tree, args.config) if mode == "image" else
              core_arm(tree, args.config, args.interfaces, mode, args.filter))
    print(result.log)
    raise SystemExit(result.rc)
