#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""twin_fw.py - the split half's firmware for the two-placement simulation (#665).

The split placement's control firmware is the platform ctrl_plat.c composes
(sw/firmware/ctrl/plat): the mailbox driver, the loop, ADP, ACMP, MAAP, AECP
with its face and saved state, SRP over lwSRP, the CSR window and the console.
This builds that composition for the host exactly as the firmware's own boot
test builds it (plat_arms.arm_platboot): the same source list, the same C11
flags, the shape's generated headers from the same generators, and F1's flash
model as the flash. It leaves out the mailbox model and mbx_plat_host.c, because
twin_main.cpp answers mbx_hal.h on the RTL mailbox and ctrl_plat_io.h on the
split datapath's CSR window.

One simulation-only setting is compiled in: CTRL_PLAT_MAAP_PREFERRED, MAAP's
first range, which the two-placement comparison pins in both placements
(#665), so MAAP's frames compare as raw bytes. The image never defines it.

srptx_mutants.py (#867) builds a planted firmware through this same list:
--replace ORIGINAL=COPY compiles COPY in ORIGINAL's place, each named file once.

Output, under --out: libtwinfw.a, and cflags, the include and define flags a
C++ unit that includes the platform's headers needs, on one line. The C units
force-include the generated srp_entity_gen.h, as SRP requires; a C++ unit
includes it by name before the platform's headers instead, so the Verilated
model's own units are not handed it.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))

from aecp_arms import AECP_SOURCES  # noqa: E402
from ctrl_arms import lwsrp_pin  # noqa: E402
from ctrl_build import C_FLAGS, CTRL, NVM_DIR, PORTABLE, STACK, Tree, source  # noqa: E402
from plat_arms import CSR_CONSOLE, generated  # noqa: E402
from srp_arms import LWSRP_SOURCES, prepared  # noqa: E402

LWSRP = ROOT / "third_party/lwSRP"
#: lwSRP's own flags, as the boot arm compiles it (plat_arms.arm_platboot)
LWSRP_FLAGS = ("-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic")


def firmware_sources() -> list[Path]:
    """The boot arm's firmware list: the portable core, AECP, SRP, the platform and the store."""
    names = [source(CTRL, STACK, n) for n in PORTABLE]
    names += [CTRL / "aecp" / n for n in (*AECP_SOURCES, "aecp_mbx.c", "aecp_face.c", "aecp_nvm.c")]
    names += [CTRL / n for n in ("app/ctrl_app_aecp.c", "app/ctrl_app_srp.c", "srp/srp_mbx.c",
                                 "plat/ctrl_plat.c", *CSR_CONSOLE)]
    return names + [NVM_DIR / "nvm_klj2.c", NVM_DIR / "nvm_store.c", NVM_DIR / "host/nvm_fmodel.c"]


def include_flags(config: Path, out: Path) -> list[str]:
    """The shape's generated headers and every include the composition needs, as the boot arm sets them."""
    tree = Tree(src=CTRL, out=out, reuse=out / "reuse")
    _, inc = prepared(tree, 1, out, config)
    inc += [f"-I{CTRL / d}" for d in ("aecp", "plat")] + generated(tree, config, out)
    lwsrp_pin(LWSRP)
    return inc + ["-DLWSRP_MILAN=1", f"-I{LWSRP / 'src/include'}", f"-I{LWSRP / 'src'}",
                  f"-I{NVM_DIR / 'host'}"]


def cxx_flags(inc: list[str]) -> list[str]:
    """The include flags without the C units' force-included shape header, which a C++ unit includes by name."""
    out: list[str] = []
    skip = False
    for flag in inc:
        if skip or flag == "-include":
            skip = not skip
            continue
        out.append(flag)
    return out


def compile_one(flags: list[str], src: Path, obj: Path) -> str:
    """Compile one C source; its diagnostics, empty when it compiled clean."""
    result = subprocess.run(["cc", *flags, "-c", str(src), "-o", str(obj)], capture_output=True, text=True,
                            check=False)
    return "" if result.returncode == 0 else f"{src}:\n{result.stdout}{result.stderr}"


def build(config: Path, out: Path, preferred: int, jobs: int, replace: dict[Path, Path] | None = None) -> int:
    """Generate the headers, compile every unit and archive them; 0, or 1 with each failing unit named.
    replace maps a source to the planted copy compiled in its place."""
    out.mkdir(parents=True, exist_ok=True)
    inc = include_flags(config, out)
    pin = [f"-DCTRL_PLAT_MAAP_PREFERRED={preferred:#x}ULL"]
    units = [(list(C_FLAGS) + inc + pin, s) for s in firmware_sources()]
    units += [(list(LWSRP_FLAGS) + inc, LWSRP / "src" / n) for n in LWSRP_SOURCES]
    replace = replace or {}
    named = [s.resolve() for _, s in units]
    for original in replace:
        if named.count(original) != 1:
            print(f"twin_fw: --replace names {original}, which is not one of the firmware's units", file=sys.stderr)
            return 1
    units = [(flags, replace.get(s.resolve(), s)) for flags, s in units]
    objs = [out / "obj" / f"{k:02d}_{s.stem}.o" for k, (_, s) in enumerate(units)]
    (out / "obj").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        errors = [e for e in pool.map(compile_one, [f for f, _ in units], [s for _, s in units], objs) if e]
    if errors:
        print("twin_fw: the firmware did not compile\n" + "\n".join(errors), file=sys.stderr)
        return 1
    lib = out / "libtwinfw.a"
    lib.unlink(missing_ok=True)
    subprocess.run(["ar", "crs", str(lib), *map(str, objs)], check=True)
    # the harness asserts its own copy of the pin against the one compiled in
    (out / "cflags").write_text(" ".join([*cxx_flags(inc), f"-DTWIN_FW_MAAP_PREFERRED={preferred:#x}ULL"]) + "\n")
    print(f"twin_fw: {len(objs)} units into {lib.name}; MAAP pinned at {preferred:#014x}")
    return 0


def main() -> int:
    """Build the split half's firmware for the configuration named."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, required=True, help="the end-station configuration (its shape)")
    parser.add_argument("--out", type=Path, required=True, help="the build directory")
    parser.add_argument("--maap-preferred", type=lambda v: int(v, 0), required=True,
                        help="MAAP's pinned first range, a MAC address in the IEEE 1722-2016 B.4 pool")
    parser.add_argument("--jobs", type=int, default=8)
    parser.add_argument("--replace", action="append", default=[], metavar="ORIGINAL=COPY",
                        help="compile COPY in ORIGINAL's place (srptx_mutants.py)")
    args = parser.parse_args()
    replace = {Path(o).resolve(): Path(c).resolve() for o, c in (r.split("=", 1) for r in args.replace)}
    return build(args.config.resolve(), args.out.resolve(), args.maap_preferred, args.jobs, replace)


if __name__ == "__main__":
    sys.exit(main())
