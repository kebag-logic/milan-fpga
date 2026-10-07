# SPDX-License-Identifier: CERN-OHL-W-2.0
"""SRP host, debug and RV32 arms using the shared firmware harness."""
from __future__ import annotations
import resource
import shutil
import sys
from pathlib import Path
from ctrl_build import (CTRL, ROOT, HERE, HARNESS, C_FLAGS, HOST, INCLUDE_DIRS,
                        PORTABLE, NVM_DIR, RV32_FLAGS, RV32_LIBC, Outcome, Refusal, Tree, run)
import fw_gtest
import fw_rv32
from ctrl_arms import lwsrp_pin, symbols, fabric_view

LWSRP_SOURCES = ("core/mrp_mad.c", "core/mrp_pdu.c", "ports/timer.c", "modules/msrp.c", "modules/mvrp.c")
SRP_SOURCES = PORTABLE + ("srp/srp_mbx.c", "app/ctrl_app_srp.c")
DEFAULT_ENTITY = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"


def prepared(tree: Tree, interface_count: int, out: Path, config: Path) -> tuple[Path, list[str]]:
    """Generate the entity shape and, for two interfaces, the mailbox header."""
    out.mkdir(parents=True, exist_ok=True)
    header = out / "srp_entity_gen.h"
    result = run([sys.executable,"-B",str(CTRL / "srp/srp_entity.py"),str(config),"-o",str(header)])
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
    inc = [f"-I{include_tree / d}" for d in (*INCLUDE_DIRS,"srp")]
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
    build = fw_gtest.Build(coverage=tree.build.coverage and not debug,jobs=tree.build.jobs,cache=tree.build.cache)
    flags = [*C_FLAGS, "-UNDEBUG" if debug else "-DNDEBUG"]
    sources = [(variant if p.startswith("mbx/") else tree.src) / p for p in SRP_SOURCES]
    try:
        ours = fw_gtest.compile_c(build,flags,inc,sources,out / "firmware")
        host = fw_gtest.compile_c(build,C_FLAGS,inc,[tree.src / p for p in HOST],out / "host",False)
        theirs = fw_gtest.compile_c(build,[*C_FLAGS,"-Dshlan_calloc=srp_test_calloc"],inc,
                                    [lw / p for p in LWSRP_SOURCES],out / "library",False)
        tests = fw_gtest.compile_tests(build,inc,[HERE / ("srp_debug.cpp" if debug else test)],out / "tests")
        main = fw_gtest.main_object(build,out / "main")
        exe = fw_gtest.link(build,[*ours,*host,*theirs,*tests,main],out / "suite")
        ok, log = fw_gtest.run_binary(exe,[f"--gtest_filter={selected}"],cwd=out)
    except fw_gtest.BuildError as error:
        raise Refusal(str(error)) from error
    (out / "run.log").write_text(log,encoding="utf-8")
    return Outcome(name,0 if ok else 1,log)


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
    sources = [(variant if p.startswith("mbx/") else tree.src) / p for p in SRP_SOURCES]
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


def all_shapes(tree: Tree, lwsrp: Path, rv32: bool = False) -> list[Outcome]:
    """Exercise static storage at every shipped entity shape and interface count."""
    outcomes = []
    for config in sorted((ROOT / "configs").glob("endstation_*.yaml")):
        for interfaces in (1, 2):
            outcomes.append(arm_srp(tree, lwsrp, interfaces, test="srp_shape.cpp", config=config))
            if rv32:
                outcomes.append(arm_srp_rv32(tree, lwsrp, interfaces, config))
    return outcomes
