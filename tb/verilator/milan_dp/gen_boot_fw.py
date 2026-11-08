#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Stage the firmware's boot for the bootsa leg (#839).

The leg drives milan_datapath through the boot the bare-metal firmware runs,
so the order and the words must be the firmware's own, not a copy. This
writes three files into --out:

  boot_fw.c    the firmware's CSR accessors, configure_fabric() and
               entity_advertise(), copied out of milan_baremetal.c with two
               edits: the CSR load and the CSR store call the harness, and
               the fence after the store is blanked (a host cannot assemble
               it). Both edits must apply exactly once.
  boot_fw.h    the order milan_init() calls its four stages in, read out of
               milan_init() itself, the station MAC the firmware writes, the
               firmware's own offsets of the CSRs the leg writes outside
               configure_fabric(), the boot words configure_fabric() writes
               to MAAP_CTRL, AAF_CTRL and CRFT_CTRL, and whether the config
               declares the CRF Media Clock Output.
  gptp_ucode.hex  the gPTP program for this leg's 2 MHz clock, generated
               with the same station MAC (the builder does the same for a
               product build, at the product clock).

The generated words are boot_policy.fabric_constants() over the builder's own
outputs for the config, which is what milan_soc.py publishes to the firmware.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "sw" / "litex"))

import boot_policy  # noqa: E402

GPTP_UCODE = ROOT / "gptp-processor" / "hdl" / "ucode" / "gen_gptp_ucode.py"
#: milan_init()'s stages, in no particular order: the leg knows how to run
#: these four and refuses a firmware that calls anything else among them
STAGES = ("configure_fabric", "load_aem_image", "nvm_boot", "entity_advertise")
#: the functions copied verbatim, in source order
COPIED = ("milan_reg", "milan_read", "milan_write", "configure_fabric",
          "entity_advertise")
#: the firmware's CSR offsets the leg writes itself, outside configure_fabric()
#: (the early-enable boots and the pair-order boots), by their boot_fw.h names
OFFSETS = {"kMacAddrLo": "MILAN_MAC_ADDR_LO", "kMacAddrHi": "MILAN_MAC_ADDR_HI",
           "kMaapCtrl": "MILAN_MAAP_CTRL", "kAafCtrl": "MILAN_AAF_CTRL",
           "kCrfTxCtrl": "MILAN_CRF_TX_CTRL"}
LOAD = "\treturn *milan_reg(offset);\n"
STORE = "\t*milan_reg(offset) = value;\n"
FENCE = '\t__asm__ volatile("fence iorw, iorw" ::: "memory");\n'


def function_text(source: str, name: str) -> str:
    """The definition of `name`, from its signature line to its closing brace."""
    head = re.search(rf"(?m)^static [^\n;]*\b{name}\s*\([^)]*\)\s*\n\{{", source)
    if head is None:
        raise SystemExit(f"gen_boot_fw: no definition of {name}() in the firmware")
    depth = 0
    for at in range(head.end() - 1, len(source)):
        depth += {"{": 1, "}": -1}.get(source[at], 0)
        if depth == 0:
            return source[head.start():at + 1] + "\n"
    raise SystemExit(f"gen_boot_fw: {name}() never closes")


def replace_once(text: str, old: str, new: str, what: str) -> str:
    """`text` with `old`, which must occur exactly once, replaced by `new`."""
    if text.count(old) != 1:
        raise SystemExit(f"gen_boot_fw: {what} occurs {text.count(old)} times, not once")
    return text.replace(old, new)


def stage_order(source: str) -> list[str]:
    """The stages milan_init() calls, in the order it calls them."""
    body = function_text(source, "milan_init")
    # a comment that names a stage is not a call to it
    body = re.sub(r"/\*.*?\*/|//[^\n]*", " ", body, flags=re.DOTALL)
    calls = [m.group(1) for m in re.finditer(r"\b([a-z_]+)\s*\(", body)
             if m.group(1) in STAGES]
    if sorted(calls) != sorted(STAGES):
        raise SystemExit(f"gen_boot_fw: milan_init() calls {calls}; the leg runs "
                         f"exactly {list(STAGES)}, each once")
    return calls


def main() -> int:
    """Write boot_fw.c, boot_fw.h and gptp_ucode.hex into --out."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--firmware", type=Path, required=True)
    ap.add_argument("--build", type=Path, required=True,
                    help="the builder's output directory for the config")
    ap.add_argument("--clk-hz", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    source = args.firmware.read_text()
    overlay = json.loads((args.build / "aem_overlay.json").read_text())
    lwsrp = json.loads((args.build / "lwsrp_table.json").read_text())
    words = boot_policy.fabric_constants(overlay, lwsrp)

    defines = re.findall(r"(?m)^#define MILAN_[A-Z0-9_]+\s+0x[0-9a-fA-F]+u\s*$", source)
    offsets = {m.group(1): int(m.group(2), 16) for m in re.finditer(
        r"(?m)^#define (MILAN_[A-Z0-9_]+)\s+0x([0-9a-fA-F]+)u\s*$", source)}
    missing = sorted(set(OFFSETS.values()) - set(offsets))
    if missing:
        raise SystemExit(f"gen_boot_fw: the firmware defines no {missing}")
    body ="".join(function_text(source, name) for name in COPIED)
    body = replace_once(body, LOAD, "\treturn boot_fw_csr_read(offset);\n", "the CSR load")
    body = replace_once(body, STORE, "\tboot_fw_csr_write(offset, value);\n", "the CSR store")
    body = replace_once(body, FENCE, "", "the store's fence")
    # milan_reg() is left with no caller once both accesses call the harness
    body = body.replace("static inline volatile uint32_t *milan_reg",
                        "static inline __attribute__((unused)) volatile uint32_t *milan_reg", 1)

    args.out.mkdir(parents=True, exist_ok=True)
    c = ["/* generated by gen_boot_fw.py from " + args.firmware.name + "; do not edit */",
         "#include <stdint.h>", "#include <stdio.h>", "",
         "#define MILAN_CSR_BASE ((uintptr_t)0u)",
         *defines,
         *(f"#define {name} 0x{value:x}u" for name, value in words.items()), "",
         "uint32_t boot_fw_csr_read(unsigned int offset);",
         "void boot_fw_csr_write(unsigned int offset, uint32_t value);",
         "void boot_fw_configure_fabric(void);",
         "void boot_fw_entity_advertise(int verified);", "",
         body,
         "void boot_fw_configure_fabric(void)\n{\n\tconfigure_fabric();\n}\n",
         "void boot_fw_entity_advertise(int verified)\n{\n\tentity_advertise(verified);\n}\n"]
    (args.out / "boot_fw.c").write_text("\n".join(c))

    mac = bytes.fromhex(overlay["adp"]["mac_address"].replace(":", ""))
    order = stage_order(source)
    h = ["// generated by gen_boot_fw.py; do not edit",
         "#pragma once", "#include <cstdint>", "",
         "//! milan_init()'s stages, in the order it calls them",
         "constexpr const char* kBootStages[] = {" +
         ", ".join(f'"{s}"' for s in order) + "};",
         "//! the station MAC configure_fabric() writes, wire order",
         "constexpr std::uint64_t kStationMac = 0x" + mac.hex() + "ULL;",
         "constexpr std::uint32_t kStationMacLo = 0x%08xu;" % words["MILAN_STATION_MAC_LO"],
         "constexpr std::uint32_t kStationMacHi = 0x%08xu;" % words["MILAN_STATION_MAC_HI"],
         "constexpr std::uint64_t kEntityId = 0x%016xULL;" % int(overlay["adp"]["entity_id"], 16),
         "//! the firmware's own CSR offsets (milan_baremetal.c)",
         *(f"constexpr std::uint16_t {name} = 0x{offsets[define]:x}u;"
           for name, define in OFFSETS.items()),
         "//! the boot words configure_fabric() writes to MAAP_CTRL, AAF_CTRL and CRFT_CTRL",
         "constexpr std::uint32_t kMaapCtrlBoot = 0x%08xu;" % words["MILAN_MAAP_CTRL_BOOT"],
         "constexpr std::uint32_t kAafCtrlBoot = 0x%08xu;" % words["MILAN_AAF_CTRL_BOOT"],
         "constexpr std::uint32_t kCrfTxCtrlBoot = 0x%08xu;" % words["MILAN_CRF_TX_CTRL_BOOT"],
         "//! the config declares the CRF Media Clock Output (clocking.crf_output)",
         "constexpr bool kCrfOutputDeclared = %s;"
         % ("true" if boot_policy.crf_output_declared(overlay) else "false"),
         ""]
    (args.out / "boot_fw.h").write_text("\n".join(h))

    subprocess.run([sys.executable, str(GPTP_UCODE), "--clk-hz", str(args.clk_hz),
                    "--cease-ms", "3000", "--mac", "0x" + mac.hex(),
                    "-o", str(args.out / "gptp_ucode.hex")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
