# SPDX-License-Identifier: CERN-OHL-W-2.0
"""SRP host, debug and RV32 arms using the shared firmware harness."""
from __future__ import annotations
import re
import resource
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from ctrl_build import (CTRL, ROOT, HERE, HARNESS, C_FLAGS, HOST, INCLUDE_DIRS, STACK_INCLUDE, STACK_TESTS,
                        PORTABLE, NVM_DIR, RV32_FLAGS, RV32_LIBC, Outcome, Refusal, Tree, run, source)
import fw_gtest
import fw_rv32
from ctrl_arms import lwsrp_pin, symbols, fabric_view

LWSRP_SOURCES = ("core/mrp_mad.c", "core/mrp_pdu.c", "ports/timer.c", "modules/msrp.c", "modules/mvrp.c")
SRP_SOURCES = PORTABLE + ("srp/srp_mbx.c", "app/ctrl_app_srp.c")
DEFAULT_ENTITY = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
#: srp_listeners.cpp's seams (#930): the firmware's calls of lwSRP's msrp_app_create and mrp_set_observer, which only
#: srp_mbx.c makes, renamed to the suite's, which restore the reference walk's schedule in its reference run; and its
#: calls of mrp_rx, mrp_reclaim and mrp_set_rx_filter, which restore the reclaim's and the filter's as they stood
#: before the SRP cut (#665's ruling of 2026-11-20, item 3) in the suite's other reference run.
LISTENER_SEAMS = ("-Dmsrp_app_create=srp_test_msrp_app_create", "-Dmrp_set_observer=srp_test_set_observer",
                  "-Dmrp_rx=srp_test_mrp_rx", "-Dmrp_reclaim=srp_test_mrp_reclaim",
                  "-Dmrp_set_rx_filter=srp_test_set_rx_filter")
#: The 8x8 entity, whose one-interface shape srp_listeners.cpp runs at beside 1x1/1if (#930).
ENTITY_8X8 = ROOT / "configs/endstation_ax7101_8x8.yaml"


def prepared(tree: Tree, interface_count: int, out: Path, config: Path) -> tuple[Path, list[str]]:
    """Generate the entity shape and, for two interfaces, the mailbox header."""
    out.mkdir(parents=True, exist_ok=True)
    header = out / "srp_entity_gen.h"
    result = run([sys.executable,"-B",str(CTRL / "srp/srp_entity.py"),str(config),"-o",str(header),
                  "--interfaces",str(interface_count)])
    if result.returncode:
        raise Refusal(f"SRP entity generation failed: {result.stderr}")
    include_tree = tree.src
    if interface_count != 1:
        include_tree = out / "variant"
        shutil.copytree(tree.src, include_tree, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        sys.path.insert(0,str(ROOT / "sw/mailbox"))
        import gen_mailbox
        findings = gen_mailbox.write_variant(gen_mailbox.load(),interface_count,out / "contract")
        if findings:
            raise Refusal(f"mailbox variant findings: {findings}")
        shutil.copyfile(out / "contract/mbx_contract.h",include_tree / "mbx/mbx_contract.h")
    inc = [f"-I{include_tree / d}" for d in (*INCLUDE_DIRS,"srp")] + [f"-I{tree.stack / STACK_INCLUDE}"]
    return include_tree, [*inc,f"-I{NVM_DIR}",f"-I{HARNESS}","-include",str(header)]


def arm_srp(tree: Tree, lwsrp: Path, interfaces: int, debug: bool = False,
            test: str | tuple[str, str] = "srp_mbx.cpp", config: Path = DEFAULT_ENTITY) -> Outcome:
    """The original SRP source is measured for both generated interface shapes."""
    test, selected = (test, "*") if isinstance(test, str) else test
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    lwsrp_pin(lwsrp)
    name = f"srp-{'debug' if debug else test.removesuffix('.cpp')}-if{interfaces}-{config.stem}"
    out = tree.out / name
    variant, inc = prepared(tree,interfaces,out,config)
    if test == "test_acmp_mbx.cpp":
        inc += ["-DCTRL_APP_TEST_SRP"]
        from ctrl_reuse import cut_reuse
        cut_reuse(tree.reuse)
        inc.append(f"-I{tree.reuse}")
    if test == "srp_shape.cpp":
        expected = fabric_view(config)
        inc += [f"-DSRP_EXPECT_SOURCES={expected['talker_stream_sources']}",
                f"-DSRP_EXPECT_SINKS={expected['listener_stream_sinks']}"]
    if test == "srp_walk.cpp":
        from srp_reuse import cut_srp
        cut_srp(out)
        inc.append(f"-I{out}")
    lw = lwsrp / "src"
    inc += ["-DLWSRP_MILAN=1",f"-I{lw / 'include'}",f"-I{lw}"]
    build = fw_gtest.Build(coverage=tree.build.coverage and not debug,
                           address_sanitizer=tree.build.address_sanitizer,
                           jobs=tree.build.jobs,cache=tree.build.cache)
    flags = [*C_FLAGS, "-UNDEBUG" if debug else "-DNDEBUG"]
    if test == "srp_listeners.cpp":
        flags += LISTENER_SEAMS
    sources = [source(variant if p.startswith("mbx/") else tree.src, tree.stack, p) for p in SRP_SOURCES]
    try:
        ours = fw_gtest.compile_c(build,flags,inc,sources,out / "firmware")
        host = fw_gtest.compile_c(build,C_FLAGS,inc,[tree.src / p for p in HOST],out / "host",False)
        library_flags = [*C_FLAGS,"-Dshlan_calloc=srp_test_calloc"]
        if test == "srp_app.cpp":
            library_flags.append("-Dmrp_transmit=srp_test_transmit_real")
        theirs = fw_gtest.compile_c(build,library_flags,inc,
                                    [lw / p for p in LWSRP_SOURCES],out / "library",False)
        tests = fw_gtest.compile_tests(build,[*inc,f"-I{STACK_TESTS}"],
                                       [HERE / ("srp_debug.cpp" if debug else test)],out / "tests")
        main = fw_gtest.main_object(build,out / "main")
        exe = fw_gtest.link(build,[*ours,*host,*theirs,*tests,main],out / "suite")
        ok, log = fw_gtest.run_binary(exe,[f"--gtest_filter={selected}"],cwd=out)
    except fw_gtest.BuildError as error:
        raise Refusal(str(error)) from error
    (out / "run.log").write_text(log,encoding="utf-8")
    return Outcome(name,0 if ok else 1,log)


def talker_arms(tree: Tree, lwsrp: Path) -> list[Outcome]:
    """The Talker declarations as their validity moves them (#895): srp_talker.cpp at 1x1/1if and 8x8/2if, and the
    composition's (test_acmp_mbx.cpp's SrpGate, which its own arms run at the 1x1 entity) at 8x8/2if."""
    return [arm_srp(tree, lwsrp, 1, test="srp_talker.cpp"),
            arm_srp(tree, lwsrp, 2, test="srp_talker.cpp", config=ROOT / "configs/endstation_ax7101_8x8.yaml"),
            arm_srp(tree, lwsrp, 2, test=("test_acmp_mbx.cpp", "SrpGate.*"),
                    config=ROOT / "configs/endstation_ax7101_8x8.yaml")]


def listener_arms(tree: Tree, lwsrp: Path) -> list[Outcome]:
    """SRP's Listener copies against the reference walk (#930): srp_listeners.cpp at 1x1/1if and 8x8/1if."""
    return [arm_srp(tree, lwsrp, 1, test="srp_listeners.cpp"),
            arm_srp(tree, lwsrp, 1, test="srp_listeners.cpp", config=ENTITY_8X8)]


def mbx_entity_arms(tree: Tree, lwsrp: Path) -> list[Outcome]:
    """srp_mbx.cpp at the 8x8 entity at both interface counts (#929): its startup and dispatch tests hold every
    source of the compiled shape, and the two-interface campaign's 8x8 plants of them need this clean control."""
    return [arm_srp(tree, lwsrp, i, config=ROOT / "configs/endstation_ax7101_8x8.yaml") for i in (1, 2)]


def arm_srp_rv32(tree: Tree, lwsrp: Path, interfaces: int,
                  config: Path = DEFAULT_ENTITY) -> Outcome:
    """Freestanding object identity, runtime closure and static frame check."""
    lwsrp_pin(lwsrp)
    cc = fw_rv32.compiler()
    if cc is None:
        raise Refusal("SRP requires the pinned RV32 SDK")
    name = f"srp-rv32-if{interfaces}-{config.stem}"
    out = tree.out / name
    variant, inc = prepared(tree,interfaces,out,config)
    lw = lwsrp / "src"
    inc += ["-DLWSRP_MILAN=1",f"-I{lw / 'include'}",f"-I{lw}",*fw_rv32.includes(cc)]
    sources = [source(variant if p.startswith("mbx/") else tree.src, tree.stack, p) for p in SRP_SOURCES]
    sources += [lw / p for p in LWSRP_SOURCES]
    sources += [tree.src / "plat/mbx_plat_mmio.c"]
    objects = []
    for src in sources:
        obj = out / f"{src.parent.name}_{src.stem}.o"
        result = run([cc,*RV32_FLAGS,"-DNDEBUG",*inc,"-c",str(src),"-o",str(obj)])
        if result.returncode:
            raise Refusal(f"SRP RV32 compile failed: {result.stderr}")
        objects.append(obj)
    findings = fw_rv32.object_findings(cc,objects)
    nm = cc.removesuffix("gcc") + "nm"
    open_symbols = symbols(nm, objects, True) - symbols(nm, objects, False)
    stray = open_symbols - RV32_LIBC - {"memcmp","memmove"} - fw_rv32.HELPERS
    if stray:
        findings.append(f"unexpected runtime dependencies: {sorted(stray)}")
    largest = fw_rv32.stack_frames(objects)
    size = run([cc.removesuffix("gcc") + "size","-t",*map(str,objects)])
    if size.returncode:
        raise Refusal("SRP RV32 size check failed")
    failures = len(findings)
    log = "\n".join([f"  largest static frame: {largest} bytes (not a call-chain bound)",
                     f"  runtime dependencies: {sorted(open_symbols)}",size.stdout,
                     *[f"  [FAIL] {f}" for f in findings],
                     f"== SRP RV32 object checks: checks: {len(objects)}   failures: {failures} ==",
                     f"RESULT: {'FAIL' if failures else 'PASS'}"])
    (out / "run.log").write_text(log,encoding="utf-8")
    return Outcome(name,bool(failures),log)


#: The words the build fails with at a shape ctrl_loop.h does not list (its #error; THE SHAPES, #894's shape
#: ruling, item (b)).
UNLISTED = "THE SHAPES: the shape (MBX_N_IF, CTRL_SRP_SOURCES, CTRL_SRP_SINKS) is not one ctrl_loop.h lists"


def listed_shapes(tree: Tree) -> set[tuple[int, int, int]]:
    """The shapes the built tree's ctrl_loop.h lists, each (interfaces, talker sources, listener sinks)."""
    text = (tree.src / "loop/ctrl_loop.h").read_text(encoding="utf-8")
    found = re.findall(r"^#(?:el)?if CTRL_LOOP_SHAPE\((\d+)u, (\d+)u, (\d+)u\)", text, re.M)
    return {(int(n), int(sources), int(sinks)) for n, sources, sinks in found}


def refused(name: str, arm: Callable[[], Outcome]) -> Outcome:
    """An arm at a shape ctrl_loop.h does not list: passing only where its build is refused in the #error's words."""
    try:
        built = arm()
    except Refusal as exc:
        said = str(exc)
        held = UNLISTED in said
        return Outcome(name, 0 if held else 1,
                       f"{'refused by THE SHAPES' if held else 'refused, not in the words of THE SHAPES'}: {said}")
    return Outcome(name, 1, f"built at a shape ctrl_loop.h does not list (THE SHAPES), rc {built.rc}")


def all_shapes(tree: Tree, lwsrp: Path, rv32: bool = False) -> list[Outcome]:
    """Exercise static storage at every shipped entity shape and interface count ctrl_loop.h lists (THE SHAPES); at
    every other one, hold that the build is refused in the words of its #error."""
    listed = listed_shapes(tree)
    outcomes = []
    for config in sorted((ROOT / "configs").glob("endstation_*.yaml")):
        view = fabric_view(config)
        for interfaces in (1, 2):
            shape = (interfaces, view["talker_stream_sources"], view["listener_stream_sinks"])
            arms = [(f"srp-srp_shape-if{interfaces}-{config.stem}",
                     lambda i=interfaces, c=config: arm_srp(tree, lwsrp, i, test="srp_shape.cpp", config=c))]
            if rv32:
                arms.append((f"srp-rv32-if{interfaces}-{config.stem}",
                             lambda i=interfaces, c=config: arm_srp_rv32(tree, lwsrp, i, c)))
            outcomes += [arm() if shape in listed else refused(name, arm) for name, arm in arms]
    return outcomes
