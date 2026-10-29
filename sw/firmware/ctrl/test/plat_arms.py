# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""plat_arms.py - the split platform's arms of the control-plane firmware's host test (#665 S3).

  plat      the CSR window, the console and the MMIO platform, each on its own
            host bus (test_plat.cpp, test_plat_mmio.cpp);
  platboot  the boot and composition of ctrl_plat.c, at the shipping shape with
            one and with two AVB interfaces, on the mailbox model, F1's flash
            model and the host bus (test_plat_boot.cpp);
  plattrace the CSR initialisation against milan_baremetal.c's own, compiled on
            the host as builder gate 35 compiles it, for every shipped config,
            with its planted controls (plat_trace.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

from ctrl_build import (C_FLAGS, CTRL, HERE, HOST, NVM_DIR, PORTABLE, ROOT, Outcome, Refusal, Tree, compile_c,
                        compile_tests, execute, link, run, source)
import fw_gtest

#: The shape the boot arm is generated for: the shipping 1x1.
SHIPPING = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
#: The platform's sources each arm measures.
CSR_CONSOLE = ("plat/ctrl_plat_csr.c", "plat/ctrl_plat_console.c")


def nvm_tree(tree: Tree) -> Path:
    """The saved-state store beside the tree: a campaign's planted copy (aecp_mutants.py copies it), else the
    checkout's (ctrl_mutants.py copies the ctrl tree alone)."""
    beside = tree.src.parent / "ctrl_nvm"
    return beside if beside.is_dir() else NVM_DIR


def arm_plat(tree: Tree) -> Outcome:
    """The CSR window and the console on the host bus; the MMIO platform over a host array."""
    inc = (f"-I{tree.src / 'plat'}",)
    objs = compile_c(tree, [tree.src / n for n in CSR_CONSOLE], "plat", inc)
    units = execute("plat", link(tree, "test_plat", objs + compile_tests(
        tree, ("plat_bus.cpp", "test_plat.cpp"), "plat/tests", inc)))
    mmio = compile_c(tree, [tree.src / "plat/ctrl_plat_mmio.c"], "plat/mmio", inc)
    platform = execute("plat", link(tree, "test_plat_mmio", mmio + compile_tests(
        tree, ("test_plat_mmio.cpp",), "plat/mmio/tests", inc)))
    return Outcome("plat", max(units.rc, platform.rc), f"{units.log}\n{platform.log}")


def generated(tree: Tree, config: Path, out: Path) -> list[str]:
    """The shape's generated headers: the entity, the AEM image, the platform policy and F1's record geometry."""
    sys.path.insert(0, str(NVM_DIR / "test"))
    import nvm_bench  # noqa: E402
    for argv in ([str(CTRL / "adp/adp_entity.py"), str(config), "-o", str(out / "adp_entity_gen.h")],
                 [str(CTRL / "aecp/aecp_entity.py"), str(config), "-o", str(out / "aecp_entity_gen.h")],
                 [str(CTRL / "plat/ctrl_plat_gen.py"), "policy", str(config),
                  "-o", str(out / "ctrl_plat_policy_gen.h")]):
        result = run([sys.executable, "-B", *argv])
        if result.returncode:
            raise Refusal(f"{Path(argv[0]).name}: {result.stdout}{result.stderr}")
    try:
        shape = nvm_bench.shape_inputs(config, out / "shape")
    except nvm_bench.Refusal as exc:
        raise Refusal(str(exc)) from exc
    nvm_bench.write_headers(out / "gen", nvm_bench.shape_header(shape.shape, shape.donor, shape.ident),
                            shape.clock_hz)
    return [f"-I{out}", f"-I{out / 'gen'}"]


def arm_platboot(tree: Tree, interfaces: int) -> Outcome:
    """ctrl_plat.c's boot and composition at the shipping shape, one or two interfaces."""
    from aecp_arms import AECP_SOURCES
    from ctrl_arms import lwsrp_pin
    from srp_arms import LWSRP_SOURCES, prepared
    out = tree.out / f"platboot-if{interfaces}"
    variant, inc = prepared(tree, interfaces, out, SHIPPING)
    inc += [f"-I{variant / d}" for d in ("aecp", "plat")] + generated(tree, SHIPPING, out)
    lw = ROOT / "third_party/lwSRP"
    lwsrp_pin(lw)
    inc += ["-DLWSRP_MILAN=1", f"-I{lw / 'src/include'}", f"-I{lw / 'src'}"]
    store = nvm_tree(tree)
    firmware = [source(variant if n.startswith("mbx/") else tree.src, tree.stack, n) for n in PORTABLE]
    firmware += [tree.src / "aecp" / n for n in (*AECP_SOURCES, "aecp_mbx.c", "aecp_face.c", "aecp_nvm.c")]
    firmware += [tree.src / n for n in ("app/ctrl_app_aecp.c", "app/ctrl_app_srp.c", "srp/srp_mbx.c",
                                        "plat/ctrl_plat.c", *CSR_CONSOLE)]
    firmware += [store / "nvm_klj2.c", store / "nvm_store.c"]
    models = [tree.src / n for n in HOST if n != "host/mbx_plat_host.c"] + [store / "host/nvm_fmodel.c"]
    label = f"-DPLAT_TEST_SHAPE=\"{SHIPPING.stem} if{interfaces}\""
    # The variant's include path alone, so its two-interface contract is the one every unit sees
    # (srp_arms.prepared); the harness's build and grade, as aecp_arms.core_arm uses them.
    try:
        objs = fw_gtest.compile_c(tree.build, C_FLAGS, inc, firmware, out / "fw")
        objs += fw_gtest.compile_c(tree.build, C_FLAGS, inc, models, out / "models", measured=False)
        objs += fw_gtest.compile_c(tree.build, ("-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic"), inc,
                                   [lw / "src" / n for n in LWSRP_SOURCES], out / "lwsrp", measured=False)
        objs += fw_gtest.compile_tests(tree.build, [*inc, label], [HERE / "plat_bus.cpp",
                                                                   HERE / "test_plat_boot.cpp"], out / "tests")
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc
    return execute("platboot", link(tree, f"test_plat_boot_if{interfaces}", objs))


def arm_platrv32(tree: Tree, require: bool) -> Outcome:
    """The platform and its composition, cross-compiled freestanding for RV32I at the shipping shape: ABI,
    instruction set and runtime closure, as the SRP arm checks its own (srp_arms.arm_srp_rv32). main() is the
    linked image's (ctrl_plat_image.py), which needs the SoC's csr.csv."""
    import fw_rv32
    from aecp_arms import AECP_SOURCES
    from ctrl_arms import lwsrp_pin, symbols
    from ctrl_build import RV32_FLAGS, RV32_LIBC
    from srp_arms import LWSRP_SOURCES, prepared
    cc = fw_rv32.compiler()
    if cc is None:
        if require:
            raise Refusal("no RV32 compiler (the pinned SDK's riscv32-linux-gcc or a bare-metal one)")
        return Outcome("platrv32", 0, "  SKIPPED: no RV32 compiler; --require-rv32 refuses instead")
    out = tree.out / "platrv32"
    variant, inc = prepared(tree, 1, out, SHIPPING)
    inc += [f"-I{variant / d}" for d in ("aecp", "plat")] + generated(tree, SHIPPING, out)
    lw = ROOT / "third_party/lwSRP"
    lwsrp_pin(lw)
    inc += ["-DLWSRP_MILAN=1", f"-I{lw / 'src/include'}", f"-I{lw / 'src'}", f"-I{NVM_DIR / 'test/rv32'}",
            f"-I{NVM_DIR / 'plat'}", *fw_rv32.includes(cc)]
    store = nvm_tree(tree)
    sources = [source(variant if n.startswith("mbx/") else tree.src, tree.stack, n) for n in PORTABLE]
    sources += [tree.src / "aecp" / n for n in (*AECP_SOURCES, "aecp_mbx.c", "aecp_face.c", "aecp_nvm.c")]
    sources += [tree.src / n for n in ("app/ctrl_app_aecp.c", "app/ctrl_app_srp.c", "srp/srp_mbx.c",
                                       "plat/mbx_plat_mmio.c", "plat/ctrl_plat_mmio.c", "plat/ctrl_plat.c",
                                       *CSR_CONSOLE)]
    sources += [store / "nvm_klj2.c", store / "nvm_store.c", store / "plat/nvm_flash_litespi.c"]
    sources += [lw / "src" / n for n in LWSRP_SOURCES]
    objects = []
    for index, src in enumerate(sources):
        obj = out / f"{index}-{src.stem}.o"
        result = run([cc, *RV32_FLAGS, *inc, "-c", str(src), "-o", str(obj)])
        if result.returncode:
            return Outcome("platrv32", 1, f"  [FAIL] {src.name} does not build for RV32I:\n{result.stderr}")
        objects.append(obj)
    findings = fw_rv32.object_findings(cc, objects)
    nm = cc.removesuffix("gcc") + "nm"
    open_symbols = symbols(nm, objects, True) - symbols(nm, objects, False)
    stray = open_symbols - RV32_LIBC - {"memcmp", "memmove"} - fw_rv32.HELPERS
    if stray:
        findings.append(f"unexpected runtime dependencies: {sorted(stray)}")
    log = "\n".join([f"  {len(objects)} objects; runtime dependencies: {sorted(open_symbols)}",
                     f"  largest static frame: {fw_rv32.stack_frames(objects)} bytes (not a call-chain bound)",
                     *[f"  [FAIL] {f}" for f in findings],
                     f"== ctrl split platform RV32I build: checks: 1   failures: {1 if findings else 0} ==",
                     f"RESULT: {'FAIL' if findings else 'PASS'}"])
    return Outcome("platrv32", 1 if findings else 0, log)


def arm_plattrace(tree: Tree) -> Outcome:
    """The CSR initialisation's writes against milan_baremetal.c's, for every shipped config, and its plants."""
    import plat_trace
    return plat_trace.arm(tree.src, tree.out / "plattrace")


def all_arms(tree: Tree, require_rv32: bool) -> list[Outcome]:
    """Every platform arm, as the suites run them."""
    return [arm_plat(tree), arm_platboot(tree, 1), arm_platboot(tree, 2), arm_platrv32(tree, require_rv32),
            arm_plattrace(tree)]


def coverage_arms(tree: Tree) -> list[Outcome]:
    """The arms that execute the platform's firmware, for the coverage run."""
    return [arm_plat(tree), arm_platboot(tree, 1), arm_platboot(tree, 2)]

