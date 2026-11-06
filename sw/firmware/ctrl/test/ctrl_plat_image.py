#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Link the split platform's image (#665): plat/ctrl_plat_main.c's main, not a fixture's.

The composition is the one ctrl_srp_image.py --with-aecp --layout split links,
F0-F5 and F1 with the entity-sized lwSRP pool, but its entry is the platform's
(sw/firmware/ctrl/plat): the boot sequence, the CSR window's identity and
policy, the console, MAAP's allocation port and SRP's sources. Its two
generated headers come from ctrl_plat_gen.py: the policy from --config, the
bus map from --csr-csv, the export of the SoC the image runs on (a split
export with any image gives it; docs/design/SPLIT_CONTROL_MEMORY.md section 4).
The mailbox's base is the map's, so the fixture's placeholder is dropped. F1's
flash port keeps its own addresses (ctrl_nvm/test/rv32/generated), as every
split image at this base does.

The link, the audits and the bank plan are ctrl_srp_image.py's, reused. The
report adds the five largest .bss objects, the platform measurement against the
56-tile budget, with the platform's one static object, ctrl_plat, counted as
its members (each measured by sizeof, compiled as the image is).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from ctrl_build import CTRL, PORTABLE, RV32_FLAGS, STACK, Refusal, source
import ctrl_srp_image as image
from ctrl_arms import lwsrp_pin
from srp_arms import LWSRP_SOURCES, prepared
import fw_rv32

ROOT = CTRL.parents[2]
PLAT_SOURCES = ("plat/mbx_plat_mmio.c", "plat/ctrl_plat_mmio.c", "plat/ctrl_plat_csr.c",
                "plat/ctrl_plat_console.c", "plat/ctrl_plat.c", "plat/ctrl_plat_main.c")
#: What the image must hold for the platform's boot to have been linked, not discarded.
REQUIRED = {"main", "ctrl_plat", "ctrl_plat_boot", "ctrl_plat_step", "ctrl_plat_csr_identity",
            "ctrl_plat_csr_policy", "ctrl_plat_console_poll", "maap_csr_allocation", "ctrl_app_compose",
            "ctrl_app_open", "ctrl_app_open_held", "ctrl_app_release_adp", "ctrl_app_compose_aecp",
            "ctrl_app_open_aecp", "ctrl_app_attach_srp", "srp_mbx_init", "aecp_image_load", "nvm_store_boot",
            "nvm_store_service", "ctrl_loop_step"}
#: The fixture's placeholder for the mailbox (ctrl_build.RV32_FLAGS); the map's replaces it.
PLACEHOLDER = re.compile(r"-DCTRL_MBX_BASE=.*")


def generate(config: Path, csr_csv: Path, out: Path) -> None:
    """The platform's two headers, through their generator."""
    gen = CTRL / "plat/ctrl_plat_gen.py"
    image.checked([sys.executable, "-B", str(gen), "policy", str(config), "-o", str(out / "ctrl_plat_policy_gen.h")])
    image.checked([sys.executable, "-B", str(gen), "map", str(csr_csv), "-o", str(out / "ctrl_plat_map_gen.h")])


#: The members of struct ctrl_plat (plat/ctrl_plat.h), the platform's one static object, each measured apart.
MEMBERS = ("console", "maap_csr", "app", "config", "acmp", "bridge", "aecp", "aecp_config", "face", "state",
           "binding", "srp", "srp_config", "sources")


def member_sizes(cc: str, flags: list[str], inc: list[str], out: Path) -> dict[str, int]:
    """sizeof each member of struct ctrl_plat, compiled as the image is: one object per member, read by nm -S."""
    probe = out / "ctrl_plat_members.c"
    probe.write_text('#include "ctrl_plat.h"\n' + "".join(
        f"const unsigned char ctrl_plat_member_{m}[sizeof ctrl_plat.{m}] = {{1}};\n" for m in MEMBERS))
    obj = out / "ctrl_plat_members.o"
    image.checked([cc, *flags, *inc, "-c", str(probe), "-o", str(obj)])
    found = {}
    for line in image.checked([cc.removesuffix("gcc") + "nm", "-S", str(obj)]).splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[3].startswith("ctrl_plat_member_"):
            found[fields[3].removeprefix("ctrl_plat_member_")] = int(fields[1], 16)
    if set(found) != set(MEMBERS):
        raise Refusal(f"the member probe measured {sorted(found)}, not {sorted(MEMBERS)}")
    return found


def largest_bss(symbols: str, sections: dict[str, tuple[int, int]], members: dict[str, int],
                count: int = 5) -> list[dict]:
    """The `count` largest objects inside .bss, by `nm -S`, with ctrl_plat counted as its members."""
    start, size = sections[".bss"]
    found = []
    for line in symbols.splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[2] in "bBdD":
            address, length = int(fields[0], 16), int(fields[1], 16)
            if start <= address < start + size and fields[3] != "ctrl_plat":
                found.append({"symbol": fields[3], "bytes": length})
    found += [{"symbol": f"ctrl_plat.{name}", "bytes": length} for name, length in members.items()]
    return sorted(found, key=lambda s: (-s["bytes"], s["symbol"]))[:count]


def arguments() -> argparse.Namespace:
    """The shape, the SoC's map and the runtime archives."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--ctrl-source", type=Path, default=CTRL,
                        help="the firmware tree to compile (a planted copy for a control; default the checkout's)")
    parser.add_argument("--csr-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--interfaces", type=int, choices=(1, 2), default=1)
    parser.add_argument("--ledgered-point", choices=sorted(image.ctrl_memory.LEDGERED),
                        help="plan a ledgered point's image to its ledgered tiles (ctrl_memory.LEDGERED); the "
                             "platform's is platform-8x8-two-interfaces, and any other image is refused")
    parser.add_argument("--libc", type=Path, required=True)
    parser.add_argument("--compiler-runtime", type=Path, required=True)
    return parser.parse_args()


def compile_all(cc: str, args: argparse.Namespace, out: Path) -> tuple[list[Path], dict[str, int]]:
    """Every source of the platform image, compiled as ctrl_srp_image.py compiles its own."""
    tree = image.source_tree(args.ctrl_source.resolve(), STACK.resolve(), out)
    variant, inc = prepared(tree, args.interfaces, out, args.config)
    image.checked([sys.executable, "-B", str(CTRL / "adp/adp_entity.py"), str(args.config),
                   "-o", str(out / "adp_entity_gen.h")])
    generate(args.config, args.csr_csv.resolve(), out)
    lw = ROOT / "third_party/lwSRP"
    lwsrp_pin(lw)
    flags = [f for f in RV32_FLAGS if not PLACEHOLDER.fullmatch(f)]
    flags += ["-DNDEBUG", "-fno-pie", "-ffunction-sections", "-fdata-sections", "-DLWSRP_MILAN=1",
              "-include", str(out / "ctrl_plat_map_gen.h")]
    inc += [f"-I{out}", f"-I{tree.src / 'plat'}", f"-I{lw / 'src/include'}", f"-I{lw / 'src'}",
            *fw_rv32.includes(cc)]
    extra_inc, aecp_sources = image.aecp_inputs(tree, args.config, out)
    inc += extra_inc
    sources = [source(variant if n.startswith("mbx/") else tree.src, tree.stack, n) for n in PORTABLE]
    sources += [tree.src / n for n in PLAT_SOURCES] + aecp_sources
    sources += [tree.src / "app/ctrl_app_srp.c", tree.src / "srp/srp_mbx.c",
                *[lw / "src" / n for n in LWSRP_SOURCES]]
    objects = []
    for index, src in enumerate(sources):
        obj = out / f"{index}-{src.stem}.o"
        image.checked([cc, *flags, *inc, "-c", str(src), "-o", str(obj)])
        objects.append(obj)
    findings = fw_rv32.object_findings(cc, objects)
    if findings:
        raise Refusal(str(findings))
    return objects, member_sizes(cc, flags, inc, out)


def main() -> int:
    """Link and measure one shape's platform image."""
    args = arguments()
    args.config = args.config.resolve()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    try:
        cc = fw_rv32.compiler()
        if cc is None:
            raise Refusal("the pinned RV32 compiler is required")
        objects, members = compile_all(cc, args, out)
        libraries = [args.libc.resolve(), args.compiler_runtime.resolve()]
        elf, mapfile = image.link(cc, args.ctrl_source.resolve(), out, objects, libraries, "split")
        image.verify_abi(cc, elf)
        tool = cc.removesuffix("gcc")
        symbols = image.checked([tool + "nm", "-S", str(elf)])
        if image.checked([tool + "nm", "-u", str(elf)]).strip():
            raise Refusal("linked runtime has unresolved symbols")
        names = {line.split()[-1] for line in symbols.splitlines() if line.split()}
        if names & {"malloc", "calloc", "realloc", "free", "sbrk", "_sbrk"}:
            raise Refusal("heap dependency in the platform image")
        if REQUIRED - names:
            raise Refusal(f"the platform image discarded required code or storage: {sorted(REQUIRED - names)}")
        size = image.checked([tool + "size", "-A", "-x", str(elf)])
        sections = {name: (int(addr, 16), int(length, 16))
                    for name, length, addr in re.findall(r"^(\.\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)", size, re.M)}
        if any(name not in sections for name in (".text", ".rodata", ".bss", ".stack")):
            raise Refusal("missing measured sections")
        plan = image.ctrl_memory.plan(image.ctrl_memory.read_elf(elf), ledgered=args.ledgered_point)
        report = {"shape": args.config.stem, "interfaces": args.interfaces, "entry": "plat/ctrl_plat_main.c",
                  "sections": {name: length for name, (_, length) in sections.items()},
                  "largest_bss": largest_bss(symbols, sections, members), "ctrl_plat_members": members,
                  "split": plan.summary(),
                  "artifacts": [{"name": p.name, "size": p.stat().st_size,
                                 "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                                for p in (*libraries, elf, mapfile)]}
        (out / "symbols.txt").write_text(symbols)
        (out / "size.txt").write_text(size)
        (out / "size.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        return 0
    except (Refusal, OSError, ValueError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
