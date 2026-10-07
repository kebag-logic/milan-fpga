#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gen_mailbox.py - the packet-mailbox contract's generator and its gate.

ONE SOURCE, FOUR OUTPUTS. ``sw/mailbox/mailbox.yaml`` is the contract between
the fabric and the control-plane firmware (#665 lane F0). This script writes:

  hdl/milan/mailbox/KL_mbx_pkg.sv      every constant and run-time table
  hdl/milan/mailbox/KL_mbx.sv          the fabric skeleton
  sw/firmware/ctrl/mbx/mbx_contract.h  the C header
  docs/reference/MAILBOX_CONTRACT.md   the reference page

TWO CHECKS, BECAUSE THEY CATCH DIFFERENT THINGS.

  --check       Regenerates every output in memory and compares it byte for
                byte with the tracked file. A hand edit, or a YAML change
                nobody regenerated, fails by name.
  --crosscheck  Reads the three tracked constant carriers back (the package,
                the header and the page's constant table) the way a reader
                would, by name, and requires every name to carry the
                contract's value in all three, every run-time table to list
                the channels in id order, and the skeleton to name every
                register the contract defines. This is the check that sees a
                FIELD MISMATCH between outputs, whatever produced it.

``--selftest`` proves both can fail: it plants a field mismatch into a copy of
each output and requires the cross-check to name the planted constant, and it
plants contract defects into copies of the YAML (an overlapping field, a ring
that is not a power of two, two channels claiming one EtherType, a register
with no fabric source, a match tuple naming a VLAN tag's TPID or no
destination, an own-MAC block that spills or collides, message types named
with no subtype or wider than four bits, a message_type byte not the one after
the subtype, a bound-talker table that spills its interface stride or runs into
the channel registers) and requires each to be refused. A clean run of the tracked outputs is the positive control.

``--variant-interfaces N --out DIR`` writes the package, the skeleton and the
header of the same contract elaborated for N AVB interfaces into a build
directory, cross-checked; the mailbox suite builds its per-interface own-MAC
checks on a two-interface variant. It never writes the tree.

Usage:
    python3 sw/mailbox/gen_mailbox.py --write
    python3 sw/mailbox/gen_mailbox.py --check --crosscheck
    python3 sw/mailbox/gen_mailbox.py --selftest
    python3 sw/mailbox/gen_mailbox.py --variant-interfaces 2 --out obj_if2/gen

Exit 0 = clean; 1 = drift, a mismatch, or a self-test arm that did not bite;
2 = the contract itself is refused.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mailbox_emit import all_constants, emit_c_header, emit_doc, emit_sv_package, _tables  # noqa: E402
from mailbox_model import CONTRACT, Contract, ContractError, load, with_interfaces  # noqa: E402
from mailbox_skeleton import emit_sv_top  # noqa: E402

REPO = HERE.parent.parent

#: Every output: repository path -> emitter.
OUTPUTS: dict[str, Callable[[Contract], str]] = {
    "hdl/milan/mailbox/KL_mbx_pkg.sv": emit_sv_package,
    "hdl/milan/mailbox/KL_mbx.sv": emit_sv_top,
    "sw/firmware/ctrl/mbx/mbx_contract.h": emit_c_header,
    "docs/reference/MAILBOX_CONTRACT.md": emit_doc,
}

C_CONST = re.compile(r"^#define MBX_(\w+) (0x[0-9A-F]+|\d+)u$", re.M)
C_TABLE = re.compile(r"^#define MBX_(\w+_TBL) \{ (.*) \}$", re.M)
SV_CONST = re.compile(r"^\s*localparam int unsigned MBX_(\w+)_C = 32'([hd])([0-9A-F_]+);$", re.M)
SV_TABLE = re.compile(r"^\s*localparam int unsigned MBX_(\w+_TBL)_C \[[^\]]+\] = '\{(.*)\};$", re.M)
DOC_CONST = re.compile(r"^\| `MBX_(\w+)` \| `(0x[0-9a-f]+)` \|$", re.M)
SV_REG_REF = re.compile(r"\bMBX_(?:REG|IF_REG|IFF_REG|BND_REG|CH_REG)_(\w+)_C\b")


def parse_c(text: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    """Constants and tables of the C header, by name."""
    consts = {m[1]: int(m[2], 0) for m in C_CONST.finditer(text)}
    tables = {m[1]: [n.strip().removeprefix("MBX_") for n in m[2].split(",")] for m in C_TABLE.finditer(text)}
    return consts, tables


def parse_sv(text: str) -> tuple[dict[str, int], dict[str, list[str]]]:
    """Constants and tables of the SystemVerilog package, by name."""
    consts = {m[1]: int(m[3].replace("_", ""), 16 if m[2] == "h" else 10) for m in SV_CONST.finditer(text)}
    tables = {m[1]: [n.strip().removeprefix("MBX_").removesuffix("_C") for n in m[2].split(",")]
              for m in SV_TABLE.finditer(text)}
    return consts, tables


def parse_doc(text: str) -> dict[str, int]:
    """The reference page's constant table, by name."""
    return {m[1]: int(m[2], 16) for m in DOC_CONST.finditer(text)}


def crosscheck(contract: Contract, texts: dict[str, str]) -> list[str]:
    """Every name, every value, every table and every register, across the outputs."""
    want = {c.name: c.value for c in all_constants(contract)}
    c_consts, c_tables = parse_c(texts["sw/firmware/ctrl/mbx/mbx_contract.h"])
    sv_consts, sv_tables = parse_sv(texts["hdl/milan/mailbox/KL_mbx_pkg.sv"])
    doc_consts = parse_doc(texts["docs/reference/MAILBOX_CONTRACT.md"])
    findings: list[str] = []
    for label, got in (("C header", c_consts), ("SV package", sv_consts), ("reference page", doc_consts)):
        for name, value in want.items():
            if name not in got:
                findings.append(f"{label}: MBX_{name} is missing")
            elif got[name] != value:
                findings.append(f"{label}: MBX_{name} = {got[name]:#x}, the contract says {value:#x}")
        findings += [f"{label}: MBX_{name} is not in the contract" for name in sorted(set(got) - set(want))]
    for table, members in _tables(contract):
        for label, got_tables in (("C header", c_tables), ("SV package", sv_tables)):
            if got_tables.get(table) != members:
                findings.append(f"{label}: table MBX_{table} lists {got_tables.get(table)}, want {members}")
    top = texts["hdl/milan/mailbox/KL_mbx.sv"]
    named = set(SV_REG_REF.findall(top))
    every = (contract.registers + contract.if_registers + contract.iff_registers + contract.bnd_registers
             + contract.ch_registers)
    for reg in every:
        if reg.name not in named:
            findings.append(f"skeleton: register {reg.name} is never decoded")
    findings += [f"skeleton: decodes {n}, which the contract does not define"
                 for n in sorted(named - {r.name for r in every})]
    return findings


def generate(contract: Contract) -> dict[str, str]:
    """Every output's text."""
    return {path: emit(contract) for path, emit in OUTPUTS.items()}


def tracked_texts(root: Path = REPO) -> dict[str, str]:
    """The tracked outputs as they are on disk."""
    return {path: (root / path).read_text(encoding="utf-8") for path in OUTPUTS}


def check_drift(contract: Contract, root: Path = REPO) -> list[str]:
    """Outputs that differ from what the contract generates."""
    findings = []
    for path, text in generate(contract).items():
        target = root / path
        if not target.is_file():
            findings.append(f"{path}: missing; run gen_mailbox.py --write")
        elif target.read_text(encoding="utf-8") != text:
            findings.append(f"{path}: differs from what {CONTRACT.name} generates; run gen_mailbox.py --write")
    return findings


def write_all(contract: Contract, root: Path = REPO) -> None:
    """Write every output."""
    for path, text in generate(contract).items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        print(f"wrote {path}")


#: The outputs a variant build compiles: the package, the skeleton and the header.
VARIANT_OUTPUTS = ("hdl/milan/mailbox/KL_mbx_pkg.sv", "hdl/milan/mailbox/KL_mbx.sv",
                   "sw/firmware/ctrl/mbx/mbx_contract.h")


def write_variant(contract: Contract, interfaces: int, out: Path) -> list[str]:
    """The contract for `interfaces` AVB interfaces, its compiled outputs written
    flat into `out` (a build directory, never the tree); returns the cross-check's
    findings on them, which must be none."""
    variant = with_interfaces(contract, interfaces)
    texts = generate(variant)
    out.mkdir(parents=True, exist_ok=True)
    for path in VARIANT_OUTPUTS:
        (out / Path(path).name).write_text(texts[path], encoding="utf-8")
        print(f"wrote {out / Path(path).name} ({interfaces} interfaces)")
    return crosscheck(variant, texts)


def _plant(texts: dict[str, str], path: str, old: str, new: str) -> dict[str, str]:
    """A copy of the outputs with one substitution, refused if it does not apply."""
    if texts[path].count(old) != 1:
        raise AssertionError(f"self-test fixture {old!r} does not occur exactly once in {path}")
    planted = dict(texts)
    planted[path] = texts[path].replace(old, new)
    return planted


def _plant_all(texts: dict[str, str], path: str, old: str, new: str) -> dict[str, str]:
    """A copy of the outputs with every occurrence substituted, refused if there is none."""
    if old not in texts[path]:
        raise AssertionError(f"self-test fixture {old!r} does not occur in {path}")
    planted = dict(texts)
    planted[path] = texts[path].replace(old, new)
    return planted


def _output_arms(contract: Contract) -> list[tuple[str, dict[str, str], str]]:
    """(arm, planted outputs, the finding the arm must produce)."""
    base = generate(contract)
    pkg = "hdl/milan/mailbox/KL_mbx_pkg.sv"
    hdr = "sw/firmware/ctrl/mbx/mbx_contract.h"
    doc = "docs/reference/MAILBOX_CONTRACT.md"
    top = "hdl/milan/mailbox/KL_mbx.sv"
    return [
        ("C header field width", _plant(base, hdr, "#define MBX_RXREC_W0_LEN_WIDTH 16u",
                                        "#define MBX_RXREC_W0_LEN_WIDTH 15u"), "MBX_RXREC_W0_LEN_WIDTH"),
        ("C header field moved", _plant(base, hdr, "#define MBX_TMR_CMD_TAG_LSB 8u",
                                        "#define MBX_TMR_CMD_TAG_LSB 0u"), "MBX_TMR_CMD_TAG_LSB"),
        ("SV package ring base", _plant(base, pkg, "MBX_CH_ADP_RX_BASE_C = 32'h00001000",
                                        "MBX_CH_ADP_RX_BASE_C = 32'h00001400"), "MBX_CH_ADP_RX_BASE"),
        ("SV package field lsb", _plant(base, pkg, "MBX_EV_TIMER_W1_SLOT_LSB_C = 32'd16",
                                        "MBX_EV_TIMER_W1_SLOT_LSB_C = 32'd24"), "MBX_EV_TIMER_W1_SLOT_LSB"),
        ("reference page value", _plant(base, doc, "| `MBX_REG_TMR_CMD` | `0x3c` |",
                                        "| `MBX_REG_TMR_CMD` | `0x38` |"), "MBX_REG_TMR_CMD"),
        ("C header constant dropped", _plant(base, hdr, "#define MBX_EV_TYPE_GM 3u\n", ""), "MBX_EV_TYPE_GM"),
        ("C header table order", _plant(base, hdr, "{ MBX_CH_ADP_RX_WORDS, MBX_CH_ACMP_RX_WORDS,",
                                        "{ MBX_CH_ACMP_RX_WORDS, MBX_CH_ADP_RX_WORDS,"), "CH_RX_WORDS_TBL"),
        ("skeleton register dropped", _plant_all(base, top, "MBX_REG_OWN_EID_HI_C", "MBX_REG_OWN_EID_LO_C"),
         "OWN_EID_HI"),
        # lane FC: the tuple, the AECP response term, the counter and the own MAC
        ("C header tuple destination", _plant(base, hdr, "#define MBX_CH_AECP_M0_DST 2u",
                                              "#define MBX_CH_AECP_M0_DST 1u"), "MBX_CH_AECP_M0_DST"),
        ("SV package tuple address", _plant(base, pkg, "MBX_CH_SRP_M1_DST_LO_C = 32'hC2000021",
                                            "MBX_CH_SRP_M1_DST_LO_C = 32'hC200000E"), "MBX_CH_SRP_M1_DST_LO"),
        ("C header response term", _plant(base, hdr, "#define MBX_CH_AECP_T1_MSG_MASK 0xAAAAu",
                                          "#define MBX_CH_AECP_T1_MSG_MASK 0x5555u"), "MBX_CH_AECP_T1_MSG_MASK"),
        ("reference page counter", _plant(base, doc, "| `MBX_REG_FILTER_MISMATCH` | `0x74` |",
                                          "| `MBX_REG_FILTER_MISMATCH` | `0x70` |"), "MBX_REG_FILTER_MISMATCH"),
        ("C header tuple table order", _plant(base, hdr, "{ MBX_CH_ADP_M0_ETHERTYPE, MBX_CH_ADP_M1_ETHERTYPE,",
                                              "{ MBX_CH_ADP_M1_ETHERTYPE, MBX_CH_ADP_M0_ETHERTYPE,"),
         "TUPLE_ETHERTYPE_TBL"),
        ("skeleton own MAC dropped", _plant_all(base, top, "MBX_IFF_REG_OWN_MAC_HI_C", "MBX_IFF_REG_OWN_MAC_LO_C"),
         "OWN_MAC_HI"),
        # lane FC round 2: the MAAP DEFEND to own unicast (IEEE 1722-2016 B.2.1)
        ("C header DEFEND tuple's message types", _plant(base, hdr, "#define MBX_CH_MAAP_M1_MSG_MASK 0x4u",
                                                         "#define MBX_CH_MAAP_M1_MSG_MASK 0xFFFFu"),
         "MBX_CH_MAAP_M1_MSG_MASK"),
        ("SV package DEFEND tuple dropped", _plant(base, pkg, "MBX_CH_MAAP_M1_DST_C = 32'd2;",
                                                   "MBX_CH_MAAP_M1_DST_C = 32'd0;"), "MBX_CH_MAAP_M1_DST"),
        # lane F3 round 2: the adp channel's bound-talker term (#665, comment 6029368753)
        ("C header bound term's message types", _plant(base, hdr, "#define MBX_CH_ADP_T2_MSG_MASK 0x3u",
                                                       "#define MBX_CH_ADP_T2_MSG_MASK 0x7u"),
         "MBX_CH_ADP_T2_MSG_MASK"),
        ("SV package bound term's test", _plant(base, pkg, "MBX_CH_ADP_T2_TEST_C = 32'd5;",
                                                "MBX_CH_ADP_T2_TEST_C = 32'd2;"), "MBX_CH_ADP_T2_TEST"),
        ("reference page entry stride", _plant(base, doc, "| `MBX_BND_ENTRY_STRIDE` | `0x10` |",
                                               "| `MBX_BND_ENTRY_STRIDE` | `0x8` |"), "MBX_BND_ENTRY_STRIDE"),
        ("C header table size", _plant(base, hdr, "#define MBX_N_BOUND 16u", "#define MBX_N_BOUND 8u"), "MBX_N_BOUND"),
        ("skeleton bound enable dropped", _plant_all(base, top, "MBX_BND_REG_BOUND_EN_C", "MBX_BND_REG_BOUND_EID_LO_C"),
         "BOUND_EN"),
    ]


def _contract_arms() -> list[tuple[str, str, str]]:
    """(arm, YAML substitution old, new): each must make load() or the skeleton refuse."""
    return [
        ("overlapping field", "- {name: MAJOR, lsb: 8, width: 8", "- {name: MAJOR, lsb: 4, width: 8"),
        ("ring not a power of two", "rx: {base: 0x1000, words: 256}", "rx: {base: 0x1000, words: 192}"),
        ("rings overlap", "tx: {base: 0x1400, words: 128}", "tx: {base: 0x1000, words: 128}"),
        ("two channels, one EtherType", "- {dst: 0x91E0F0010000, ethertype: 0x22F0, subtype: 0xFC,",
         "- {dst: 0x91E0F0010000, ethertype: 0x22F0, subtype: 0xFA,"),
        ("register outside its block", "  - name: BUS_ERR\n    offset: 0x070", "  - name: BUS_ERR\n    offset: 0x400"),
        ("register with no fabric source", "  - name: BUS_ERR\n    offset: 0x070",
         "  - name: BUS_ERRX\n    offset: 0x070"),
        ("term past the frame", "{test: eq_own, offset: 34, field: talker_entity_id",
         "{test: eq_own, offset: 124, field: talker_entity_id"),
        # lane FC: a tagged frame reaches no channel, a tuple names its destination, the own-MAC block fits
        ("a tuple names the C-VLAN TPID", "{dst: 0x0180C2000021, ethertype: 0x88F5,",
         "{dst: 0x0180C2000021, ethertype: 0x8100,"),
        ("a tuple names the S-VLAN TPID", "{dst: 0x0180C200000E, ethertype: 0x22EA,",
         "{dst: 0x0180C200000E, ethertype: 0x88A8,"),
        ("a tuple with no destination", "- {dst: own, ethertype: 0x22F0, subtype: 0xFB,",
         "- {ethertype: 0x22F0, subtype: 0xFB,"),
        ("own MAC spills its stride", "  stride: 0x08\n", "  stride: 0x04\n"),
        ("own MAC over the channel registers", "interface_filter_registers:\n  base: 0x080",
         "interface_filter_registers:\n  base: 0x100"),
        # lane FC round 2: a tuple's message types sit in the byte after its subtype
        ("message types with no subtype", "{dst: 0x0180C2000021, ethertype: 0x88F5,",
         "{dst: 0x0180C2000021, ethertype: 0x88F5, msg_types: [2],"),
        ("a message type wider than four bits", "subtype: 0xFE, msg_types: [2],", "subtype: 0xFE, msg_types: [16],"),
        ("message_type not the byte after the subtype", "msg_type_byte: 15", "msg_type_byte: 16"),
        # lane F3 round 2: the bound-talker table fits its block and the register space
        ("bound-talker entries spill their interface stride", "bound_talkers: 16 ", "bound_talkers: 17 "),
        ("bound-talker entry registers spill their entry", "  entry_stride: 0x10 ", "  entry_stride: 0x08 "),
        ("bound-talker table over the channel registers", "interface_bound_registers:\n  base: 0x200",
         "interface_bound_registers:\n  base: 0x100"),
        ("bound-talker table past the register space", "interface_bound_registers:\n  base: 0x200",
         "interface_bound_registers:\n  base: 0x380"),
        ("an unknown filter test", "{test: eq_bound, offset: 18,", "{test: eq_bonded, offset: 18,"),
    ]


def selftest() -> int:
    """Every arm must bite, and the tracked outputs must pass."""
    contract = load()
    failures = 0
    clean = crosscheck(contract, generate(contract))
    print(f"[{'ok' if not clean else 'FAIL'}] positive control: generated outputs cross-check clean")
    failures += bool(clean)
    for arm, planted, needle in _output_arms(contract):
        found = crosscheck(contract, planted)
        bit = any(needle in f for f in found)
        print(f"[{'ok' if bit else 'FAIL'}] planted {arm}: {found[0] if found else 'NOTHING FOUND'}")
        failures += not bit
    text = CONTRACT.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="mbx-selftest-") as tmp:
        for arm, old, new in _contract_arms():
            if text.count(old) != 1:
                print(f"[FAIL] contract arm {arm}: fixture does not occur exactly once")
                failures += 1
                continue
            planted = Path(tmp) / "mailbox.yaml"
            planted.write_text(text.replace(old, new), encoding="utf-8")
            try:
                generate(load(planted))
                print(f"[FAIL] contract arm {arm}: accepted")
                failures += 1
            except ContractError as exc:
                print(f"[ok] contract arm {arm}: refused ({exc})")
        # The two-interface variant the suite builds cross-checks clean; one
        # whose interface blocks run into the global registers is refused.
        found = write_variant(contract, 2, Path(tmp) / "if2")
        print(f"[{'ok' if not found else 'FAIL'}] variant of 2 interfaces: "
              f"{found[0] if found else 'generated outputs cross-check clean'}")
        failures += bool(found)
        try:
            with_interfaces(contract, 4)
            print("[FAIL] variant of 4 interfaces: accepted")
            failures += 1
        except ContractError as exc:
            print(f"[ok] variant of 4 interfaces: refused ({exc})")
    print(f"selftest: {failures} arm(s) failed")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and run the selected modes."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--write", action="store_true", help="write every output")
    ap.add_argument("--check", action="store_true", help="fail when a tracked output drifted")
    ap.add_argument("--crosscheck", action="store_true", help="compare the tracked outputs name by name")
    ap.add_argument("--selftest", action="store_true", help="prove both checks can fail")
    ap.add_argument("--variant-interfaces", type=int, metavar="N",
                    help="write the package, skeleton and header for N interfaces into --out")
    ap.add_argument("--out", type=Path, help="the build directory a variant is written into")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        contract = load()
        if args.variant_interfaces is not None:
            if args.out is None:
                ap.error("--variant-interfaces needs --out")
            found = write_variant(contract, args.variant_interfaces, args.out)
            for f in found:
                print(f"[FAIL] {f}")
            return 1 if found else 0
    except ContractError as exc:
        print(f"REFUSED: {exc}")
        return 2
    if args.write:
        write_all(contract)
    findings: list[str] = []
    if args.check or not (args.write or args.crosscheck):
        findings += check_drift(contract)
    if args.crosscheck:
        findings += crosscheck(contract, tracked_texts())
    for f in findings:
        print(f"[FAIL] {f}")
    print(f"gen_mailbox: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
