# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_arms.py - the arms of the control-plane firmware's host test (see test_ctrl_firmware.py)."""

from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path

from ctrl_build import (CTRL, HERE, PORTABLE, PP_ADP_PKG, ROOT, RV32_CANDIDATES, RV32_FLAGS, RV32_LIBC, TB_COMMON,
                        TB_MBX, Outcome, Refusal, Tree, compile_c, compile_tests, execute, firmware, includes, link,
                        run, sources)


def arm_model(tree: Tree) -> Outcome:
    """The RTL's mailbox checks, on the host model."""
    objs = (compile_c(tree, sources(tree, ("host/mbx_model.c",)), "model", measured=False) +
            compile_tests(tree, ("model_suite.cpp",), "model/tests", (f"-I{TB_COMMON}", f"-I{TB_MBX}")))
    return execute("model", link(tree, "model_suite", objs))


def arm_port(tree: Tree) -> Outcome:
    """The port layer, the driver and the loop."""
    objs = firmware(tree, PORTABLE, "port") + compile_tests(tree, ("test_port_loop.cpp",), "port/tests")
    return execute("port", link(tree, "test_port_loop", objs))


def arm_adp(tree: Tree) -> Outcome:
    """The ADP core, its adapter and the latency bounds."""
    objs = firmware(tree, PORTABLE, "adp") + compile_tests(tree, ("test_adp.cpp",), "adp/tests")
    return execute("adp", link(tree, "test_adp", objs))


def arm_maap(tree: Tree) -> Outcome:
    """Annex B core, allocation CSR port and H-MAAP on the host mailbox."""
    objs = firmware(tree, PORTABLE, "maap")
    results = [execute("maap", link(tree, name.removesuffix(".cpp"),
                                   objs + compile_tests(tree, (name,), "maap/tests")))
               for name in ("test_maap.cpp", "test_maap_mbx.cpp")]
    return Outcome("maap", max(r.rc for r in results), "\n".join(r.log for r in results))


def arm_maap_debug(tree: Tree) -> Outcome:
    """Debug builds assert on synchronous port reentry; release is measured."""
    objs = compile_c(tree, sources(tree, ("maap/maap.c",)), "maap_debug", ("-UNDEBUG",), measured=False)
    test = compile_tests(tree, ("test_maap_debug.cpp",), "maap_debug/tests")
    return execute("maap_debug", link(tree, "test_maap_debug", objs + test))


def arm_maap_if2(tree: Tree) -> Outcome:
    """The real generator's two-interface contract, on the same host checks."""
    out = tree.out / "maap_if2"
    result = run([sys.executable, str(ROOT / "sw/mailbox/gen_mailbox.py"),
                  "--variant-interfaces", "2", "--out", str(out / "gen")])
    if result.returncode != 0:
        raise Refusal(result.stdout + result.stderr)
    extra = (f"-include{out / 'gen/mbx_contract.h'}",)
    objs = compile_c(tree, sources(tree, PORTABLE), "maap_if2", extra)
    objs += compile_c(tree, sources(tree, ("host/mbx_model.c", "host/mbx_plat_host.c")),
                      "maap_if2/host", extra, measured=False)
    test = compile_tests(tree, ("test_maap_mbx.cpp",), "maap_if2/tests", extra)
    return execute("maap_if2", link(tree, "test_maap_if2", objs + test))


def arm_unit(tree: Tree) -> Outcome:
    """The driver, the loop and the composition on GoogleMock's HAL and port-layer
    mocks; then the MMIO platform over a host window."""
    fw = tuple(n for n in PORTABLE if n != "port/shlan_port.c")
    objs = compile_c(tree, sources(tree, fw), "unit") + compile_tests(tree, UNIT_TESTS, "unit/tests")
    seams = execute("unit", link(tree, "test_unit", objs))
    window = (f"-include{HERE / 'mmio_window.h'}", "-DCTRL_MBX_BASE=((uintptr_t)ctrl_test_window)",
              "-DCTRL_MBX_WFI=ctrl_test_wfi")
    mmio = compile_c(tree, sources(tree, ("plat/mbx_plat_mmio.c",)), "mmio", window)
    platform = execute("unit", link(tree, "test_mmio", mmio + compile_tests(tree, ("test_mmio.cpp",), "mmio/tests")))
    return Outcome("unit", max(seams.rc, platform.rc), f"{seams.log}\n{platform.log}")


#: The unit binary: the two link-seam mocks and the tests written on them.
UNIT_TESTS = ("mock_mbx_hal.cpp", "mock_shlan_port.cpp", "test_unit_seams.cpp", "test_unit_driver.cpp")


def entity_caps() -> int:
    """pp_adp_pkg::ADP_ENTITY_CAPS_C, the value the processor's ADP engine sends."""
    m = re.search(r"ADP_ENTITY_CAPS_C\s*=\s*32'h([0-9A-Fa-f_]+)\s*;", PP_ADP_PKG.read_text(encoding="utf-8"))
    if m is None:
        raise Refusal(f"no ADP_ENTITY_CAPS_C in {PP_ADP_PKG.relative_to(ROOT)}")
    return int(m.group(1).replace("_", ""), 16)


def arm_walk(tree: Tree) -> Outcome:
    """The processor's ADP walk, reused, on the firmware and the model."""
    extra = (f"-I{tree.reuse}", f"-DPP_ENTITY_CAPS=0x{entity_caps():X}u")
    objs = firmware(tree, PORTABLE, "walk") + compile_tests(tree, ("adp_walk.cpp",), "walk/tests", extra)
    return execute("walk", link(tree, "adp_walk", objs))


# ---- entity: the firmware's fields against the fabric's sources, per shipped config ----

#: struct adp_entity field -> (wire byte, bytes) in an 82-byte ENTITY_AVAILABLE
#: (IEEE 1722.1-2021 Figure 6-1, after the 14-byte Ethernet header).
WIRE = {"mac": (6, 6), "entity_id": (18, 8), "entity_model_id": (26, 8), "entity_capabilities": (34, 4),
        "talker_stream_sources": (38, 2), "talker_capabilities": (40, 2), "listener_stream_sinks": (42, 2),
        "listener_capabilities": (44, 2), "identify_control_index": (66, 2)}

#: The fabric's ADP shape constants: field -> localparam in the builder's adp_shape include.
SVH = {"talker_stream_sources": "ADP_TALKER_SRC_C", "listener_stream_sinks": "ADP_LISTENER_SINK_C",
       "talker_capabilities": "ADP_TALKER_CAPS_C", "listener_capabilities": "ADP_LISTENER_CAPS_C"}


def svh_value(svh: str, name: str) -> int:
    """One localparam of the generated ADP shape include."""
    m = re.search(rf"localparam\s+[^=;]*\b{name}\s*=\s*(?:16'h([0-9A-Fa-f_]+)|(\d+))\s*;", svh)
    if m is None:
        raise Refusal(f"the ADP shape include declares no {name}")
    return int(m.group(1).replace("_", ""), 16) if m.group(1) else int(m.group(2))


def fabric_view(config: Path) -> dict[str, int]:
    """What the fabric is programmed with (boot_policy) and compiled with (the shape include) for one config."""
    sys.path.insert(0, str(ROOT / "sw/builder"))
    sys.path.insert(0, str(ROOT / "sw/litex"))
    import boot_policy  # noqa: E402
    import endstation_builder as eb  # noqa: E402

    cfg = eb.load_config(str(config))
    overlay = eb.emit_aem_overlay(cfg)
    words = boot_policy.fabric_constants(overlay, eb.emit_lwsrp_table(cfg))
    svh = eb.emit_adp_shape_svh(cfg, overlay)
    mac = words["MILAN_STATION_MAC_LO"].to_bytes(4, "little") + words["MILAN_STATION_MAC_HI"].to_bytes(2, "little")
    view = {"entity_id": words["MILAN_ENTITY_ID_HI"] << 32 | words["MILAN_ENTITY_ID_LO"],
            "entity_model_id": words["MILAN_MODEL_ID_HI"] << 32 | words["MILAN_MODEL_ID_LO"],
            "mac": int.from_bytes(mac, "big"), "entity_capabilities": entity_caps(),
            # ADP_IDX0[31:16], reset 0 and written by no firmware (milan_csr.sv adp_idx0)
            "identify_control_index": 0}
    view.update({field: svh_value(svh, name) for field, name in SVH.items()})
    return view


def expect_header(config: Path) -> str:
    """entity_expect_gen.hpp: each field's place in the frame and the fabric's value of it."""
    rows = ",\n".join(f'    {{"{field}", {WIRE[field][0]}u, {WIRE[field][1]}u, 0x{want:X}ull}}'
                       for field, want in fabric_view(config).items())
    return "\n".join([
        f"// GENERATED by sw/firmware/ctrl/test/ctrl_arms.py from {config.name}; DO NOT EDIT.",
        "#pragma once",
        "#include <cstdint>",
        "namespace entity_expect {",
        "struct Field {",
        "    const char* name;",
        "    unsigned at;",
        "    unsigned bytes;",
        "    std::uint64_t want;",
        "};",
        f'inline constexpr const char* kConfig = "{config.stem}";',
        f'inline constexpr const char* kLabel = "ctrl ADP entity fields ({config.stem})";',
        "inline constexpr Field kFields[] = {",
        rows,
        "};",
        "}  // namespace entity_expect",
        ""])


def entity_binary(tree: Tree, config: Path, objs: list[Path]) -> Path:
    """The entity test for one config, against adp_entity.py's header and the fabric's view."""
    gen = tree.out / "entity" / config.stem
    gen.mkdir(parents=True, exist_ok=True)
    res = run([sys.executable, "-B", str(CTRL / "adp/adp_entity.py"), str(config), "-o", str(gen / "adp_entity_gen.h")])
    if res.returncode != 0:
        raise Refusal(f"adp_entity.py {config.name}: {res.stderr.strip()}")
    (gen / "entity_expect_gen.hpp").write_text(expect_header(config), encoding="utf-8")
    test = compile_tests(tree, ("entity_fields.cpp",), f"entity/{config.stem}/tests", (f"-I{gen}",))
    return link(tree, f"entity_fields_{config.stem}", objs + test)


def arm_entity(tree: Tree) -> Outcome:
    """Every shipped config's ADPDU fields against the fabric's sources."""
    objs = compile_c(tree, sources(tree, ("adp/adp.c",)), "entity")
    outcomes = [execute("entity", entity_binary(tree, config, objs))
                for config in sorted((ROOT / "configs").glob("endstation_*.yaml"))]
    return Outcome("entity", max(o.rc for o in outcomes), "\n".join(o.log for o in outcomes))


# ---- rv32: freestanding RV32I build, no heap and no OS ---------------------------------

def rv32_compiler() -> str | None:
    """An explicit bare-metal compiler, otherwise the first installed candidate."""
    explicit = os.environ.get("CTRL_RV32_CC")
    if explicit:
        found = shutil.which(explicit)
        if found is None:
            raise Refusal("CTRL_RV32_CC does not name an executable compiler")
        return found
    for cand in RV32_CANDIDATES:
        found = shutil.which(cand)
        if found is not None:
            return found
    return None


def symbols(tool: str, objs: list[Path], undefined: bool) -> set[str]:
    """The undefined, or the defined, symbols of a set of objects."""
    res = run([tool, "-u" if undefined else "--defined-only", *map(str, objs)])
    if res.returncode != 0:
        raise Refusal(f"{tool}: {res.stderr.strip()}")
    return {ln.split()[-1] for ln in res.stdout.splitlines() if ln.strip() and not ln.endswith(":")}


def arm_rv32(tree: Tree, require: bool) -> Outcome:
    """The portable set and the MMIO platform, cross-compiled; only C-library and libgcc symbols left open."""
    cc = rv32_compiler()
    if cc is None:
        if require:
            raise Refusal("no RV32 compiler (the pinned SDK's riscv32-linux-gcc or a bare-metal one)")
        return Outcome("rv32", 0, "  SKIPPED: no RV32 compiler; --require-rv32 refuses instead")
    obj_dir = tree.out / "rv32"
    obj_dir.mkdir(parents=True, exist_ok=True)
    objs = []
    for src in sources(tree, PORTABLE + ("plat/mbx_plat_mmio.c",)):
        obj = obj_dir / f"{src.parent.name}_{src.stem}.o"
        res = run([cc, *RV32_FLAGS, *includes(tree), "-c", str(src), "-o", str(obj)])
        if res.returncode != 0:
            return Outcome("rv32", 1, f"  [FAIL] {src.name} does not build for RV32I:\n{res.stderr}")
        objs.append(obj)
    tool = cc.removesuffix("gcc")
    open_syms = symbols(tool + "nm", objs, True) - symbols(tool + "nm", objs, False)
    stray = sorted(s for s in open_syms if s not in RV32_LIBC and not s.startswith("__"))
    size = run([tool + "size", "-t", *map(str, objs)]).stdout.strip().splitlines()
    lines = [f"  {cc.rsplit('/', 1)[-1]} {' '.join(RV32_FLAGS[:4])}: {len(objs)} objects",
             f"  size (text data bss dec): {' '.join(size[-1].split()[:4]) if size else 'unknown'}",
             f"  undefined: {', '.join(sorted(open_syms))}"]
    if stray:
        lines.append(f"  [FAIL] symbols outside the C library and libgcc: {', '.join(stray)}")
    lines += [f"== ctrl RV32I freestanding build: checks: 1   failures: {1 if stray else 0} ==",
              f"RESULT: {'FAIL' if stray else 'PASS'}"]
    return Outcome("rv32", 1 if stray else 0, "\n".join(lines))


# ---- lwsrp: lwSRP's MRP core on the port layer -----------------------------------------

LWSRP_SOURCES = ("src/core/mrp_mad.c", "src/core/mrp_pdu.c", "src/ports/timer.c", "src/modules/mvrp.c")

#: The lwSRP revision port/shlan_port.h is written against (it restates that
#: revision's src/ports/alloc.h). Fetch it with
#:     git clone https://github.com/kebag-logic/lwSRP lwSRP
#:     git -C lwSRP checkout 19f5796b63652eb1151906de73cb827d4980a53f
#: and pass --lwsrp lwSRP. Moving the pin is a reviewed change to this line.
LWSRP_URL = "https://github.com/kebag-logic/lwSRP"
LWSRP_REV = "19f5796b63652eb1151906de73cb827d4980a53f"
#: Every source and header the arm compiles lives under this directory.
LWSRP_TREE = "src"


def lwsrp_pin(lwsrp: Path) -> str:
    """Refuse a checkout that is not the pin, or whose compiled tree differs from it.

    `--no-optional-locks` keeps `git status` from refreshing the index, so a
    read-only checkout is read and never written.
    """
    head = run(["git", "-C", str(lwsrp), "rev-parse", "HEAD"]).stdout.strip()
    if head != LWSRP_REV:
        raise Refusal(f"lwSRP at {head or 'no git HEAD'} is not the pinned {LWSRP_REV} "
                      f"(fetch {LWSRP_URL} and check the pin out)")
    dirty = run(["git", "--no-optional-locks", "-C", str(lwsrp), "status", "--porcelain", "--untracked-files=all",
                 "--", LWSRP_TREE])
    if dirty.returncode != 0 or dirty.stdout.strip():
        changed = ", ".join(ln[3:] for ln in dirty.stdout.splitlines()) or dirty.stderr.strip()
        raise Refusal(f"lwSRP's {LWSRP_TREE}/ differs from the pinned {LWSRP_REV[:8]}: {changed}")
    return head


def arm_lwsrp(tree: Tree, lwsrp: Path) -> Outcome:
    """lwSRP's own core and MVRP, unmodified, against the static pool, the loop's tick and the SRP channel."""
    missing = [s for s in LWSRP_SOURCES if not (lwsrp / s).is_file()]
    if missing:
        raise Refusal(f"{lwsrp} is not a lwSRP checkout: no {', '.join(missing)}")
    head = lwsrp_pin(lwsrp)
    lw_inc = (f"-I{lwsrp / 'src/include'}", f"-I{lwsrp / 'src'}")
    ours = firmware(tree, PORTABLE, "lwsrp")
    test = compile_tests(tree, ("lwsrp_port.cpp",), "lwsrp/tests", lw_inc)
    obj_dir = tree.out / "lwsrp_core"
    obj_dir.mkdir(parents=True, exist_ok=True)
    theirs = []
    for src in LWSRP_SOURCES:
        obj = obj_dir / f"{Path(src).stem}.o"
        # lwSRP's own flags (its CMakeLists), not this gate's -Werror: the library is not ours to fix here
        res = run(["gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic", *lw_inc, "-c", str(lwsrp / src),
                   "-o", str(obj)])
        if res.returncode != 0:
            raise Refusal(f"lwSRP {src} does not compile:\n{res.stderr}")
        theirs.append(obj)
    outcome = execute("lwsrp", link(tree, "lwsrp_port", ours + test + theirs))
    return Outcome("lwsrp", outcome.rc, f"  lwSRP at {head}\n{outcome.log}")


# ---- the verdict -------------------------------------------------------------------------

def report(outcomes: list[Outcome]) -> bool:
    """Print every arm's evidence lines and verdict; True when one failed."""
    failed = False
    for o in outcomes:
        print(f"[{'ok' if o.rc == 0 else 'FAIL'}] arm {o.arm}")
        for ln in o.log.splitlines():
            if ln.startswith(("  ", "==", "RESULT")):
                print(f"    {ln.strip()}")
        failed = failed or o.rc != 0
    return failed
