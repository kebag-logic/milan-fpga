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
with no fabric source) and requires each to be refused. A clean run of the
tracked outputs is the positive control.

Usage:
    python3 sw/mailbox/gen_mailbox.py --write
    python3 sw/mailbox/gen_mailbox.py --check --crosscheck
    python3 sw/mailbox/gen_mailbox.py --selftest

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
from mailbox_model import CONTRACT, Contract, ContractError, load  # noqa: E402
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
SV_REG_REF = re.compile(r"\bMBX_(?:REG|IF_REG|CH_REG)_(\w+)_C\b")


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
    for reg in contract.registers + contract.if_registers + contract.ch_registers:
        if reg.name not in named:
            findings.append(f"skeleton: register {reg.name} is never decoded")
    findings += [f"skeleton: decodes {n}, which the contract does not define"
                 for n in sorted(named - {r.name for r in contract.registers + contract.if_registers
                                          + contract.ch_registers})]
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
    ]


def _contract_arms() -> list[tuple[str, str, str]]:
    """(arm, YAML substitution old, new): each must make load() or the skeleton refuse."""
    return [
        ("overlapping field", "- {name: MAJOR, lsb: 8, width: 8", "- {name: MAJOR, lsb: 4, width: 8"),
        ("ring not a power of two", "rx: {base: 0x1000, words: 256}", "rx: {base: 0x1000, words: 192}"),
        ("rings overlap", "tx: {base: 0x1400, words: 128}", "tx: {base: 0x1000, words: 128}"),
        ("two channels, one EtherType", "match: {ethertypes: [0x22F0], subtype: 0xFC}",
         "match: {ethertypes: [0x22F0], subtype: 0xFA}"),
        ("register outside its block", "  - name: BUS_ERR\n    offset: 0x070", "  - name: BUS_ERR\n    offset: 0x400"),
        ("register with no fabric source", "  - name: BUS_ERR\n    offset: 0x070",
         "  - name: BUS_ERRX\n    offset: 0x070"),
        ("term past the frame", "{test: eq_own, offset: 34, field: talker_entity_id",
         "{test: eq_own, offset: 124, field: talker_entity_id"),
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
    print(f"selftest: {failures} arm(s) failed")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and run the selected modes."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--write", action="store_true", help="write every output")
    ap.add_argument("--check", action="store_true", help="fail when a tracked output drifted")
    ap.add_argument("--crosscheck", action="store_true", help="compare the tracked outputs name by name")
    ap.add_argument("--selftest", action="store_true", help="prove both checks can fail")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        contract = load()
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
