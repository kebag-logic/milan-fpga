#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer differential probe for PR #543 (issue #536), round R281-1.

Builds MVU-relevant AECP command frames with the candidate model's OWN
builders (tests/steps/aecp_engine_model.py), addressed with the pinned
processor's tb/pp_top identities, and records what the candidate model answers.

  mvu_cases.py gen  --tests <clone>/tests --cases <file> [--mutant-tree <dir>]
  mvu_cases.py diff --tests <clone>/tests --cases <file> --rtl <file>
                    [--mutant-tree <dir> ...]

`gen` writes one line per case: `<name> <command-hex>`.
`diff` reads the RTL answers (`<name> <response-hex>|NONE`, written by the
probe phase in the scratch pp_top copy) and compares every case byte for byte
with the model at the exact head, then reports, for each mutant tree given,
the cases on which that mutant's model and the pinned RTL disagree.
"""
from __future__ import annotations

import argparse
import importlib
import struct
import sys
from pathlib import Path

# tb/pp_top identities (sim_main.cpp: OWN_MAC, EID, CTLR_MAC, CTLR_EID)
OWN_MAC = bytes.fromhex("0A0B0C0D0E0F")
EID = 0x123456789ABCDEF0
CTLR_MAC = bytes.fromhex("0202DEADBEEF")
CTLR_EID = 0x7777000000000042


def load(tests_dir: Path, with_steps: bool = True):
    """Import the model (and, once, the step module's SERVED tables) from one
    tree.  Mutant trees change only the model file, so they reuse the exact
    head's step tables: importing a second step module would register every
    behave step twice."""
    steps = str((tests_dir / "steps").resolve())
    for mod in ("aecp_engine_model",) + (("aecp_engine_steps",) if with_steps else ()):
        sys.modules.pop(mod, None)
    sys.path.insert(0, steps)
    try:
        model = importlib.import_module("aecp_engine_model")
        steps_mod = importlib.import_module("aecp_engine_steps") if with_steps else None
    finally:
        sys.path.remove(steps)
    return model, steps_mod


def cases(m):
    """(name, frame) pairs: every MVU-shaped frame the contract feature sends,
    then the reviewer's boundary and robustness frames."""
    pid = m.MILAN_PROTOCOL_ID
    seq = [0xB000]

    def env(**kw):
        seq[0] += 1
        base = dict(target_eid=EID, ctlr_eid=CTLR_EID, seq=seq[0],
                    src_mac=CTLR_MAC, dst_mac=OWN_MAC)
        base.update(kw)
        return base

    def body(ct, reserved=0, extra=b"", tail=pid[2:6]):
        return tail + struct.pack(">HH", ct, reserved) + extra

    out = []
    # --- the scenario rows, built exactly as the steps build them ---------
    for ct in (0x0000, 0x0001, 0x0002, 0x0003, 0x0004):
        out.append(("row_mvu_%04x" % ct, m.build_mvu_command(ct, **env())))
    out.append(("row_foreign_c101", m.build_mvu_command(
        0x0000, bytes.fromhex("001BC50AC101"), 0, **env(cdl=20))))
    out.append(("row_r1", m.build_mvu_command(0x8000, pid, 0, **env(cdl=20))))
    out.append(("row_short_cdl19", m.build_mvu_command(0x0000, pid, 0,
                                                       **env(cdl=19))))
    out.append(("row_junk_reserved", m.build_mvu_command(0x0000, pid, 0xDEAD,
                                                         **env(cdl=20))))
    vu_pl = struct.pack(">IHH", 0xAABBCCDD, 0, 0)
    for oui in (0x0004, 0x0026, 0x0029, 0x002B, 0x8004, 0xFC1B):
        out.append(("row_vu_oui_%04x" % oui,
                    m.build_command(m.MT_VU_COMMAND, oui, vu_pl, **env())))
    for mt, word in ((4, 0x0004), (4, 0x0014), (8, 0x0004), (10, 0x0006),
                     (12, 0x0016), (14, 0x0018)):
        out.append(("row_mt%d_%04x" % (mt, word),
                    m.build_command(mt, word, vu_pl, **env())))
    out.append(("row_vu_response_input", m.build_command(
        m.MT_VU_RESPONSE, m.OP_READ_DESCRIPTOR,
        struct.pack(">HHHH", 0, 0, 0, 0), **env())))
    # --- reviewer boundary / robustness frames -----------------------------
    head = (pid[0] << 8) | pid[1]
    out.append(("x_overlong_cdl24", m.build_command(
        m.MT_VU_COMMAND, head, body(0, extra=bytes(4)), **env())))
    out.append(("x_overlong_cdl112", m.build_command(
        m.MT_VU_COMMAND, head, body(0, extra=bytes(range(92))), **env())))
    out.append(("x_short_cdl18", m.build_mvu_command(0x0000, pid, 0,
                                                     **env(cdl=18))))
    out.append(("x_short_cdl12", m.build_mvu_command(0x0000, pid, 0,
                                                     **env(cdl=12))))
    for tag, h, tail in (("22", 0xFF1B, pid[2:6]), ("23", 0x00FF, pid[2:6]),
                         ("24", head, bytes.fromhex("FF0AC100")),
                         ("25", head, bytes.fromhex("C5FFC100")),
                         ("26", head, bytes.fromhex("C50AFF00")),
                         ("27", head, bytes.fromhex("C50AC1FF"))):
        out.append(("x_pid_foreign_at_%s" % tag, m.build_command(
            m.MT_VU_COMMAND, h, body(0, tail=tail), **env())))
    for mt in (m.MT_AEM_COMMAND, m.MT_AA_COMMAND, 4, 8, 14):
        out.append(("x_mt%d_carrying_mvu_bytes" % mt,
                    m.build_command(mt, head, body(0), **env())))
    out.append(("x_fig55_set_system_unique_id_cdl28", m.build_command(
        m.MT_VU_COMMAND, head,
        body(0x0001, extra=struct.pack(">Q", 0x0102030405060708)), **env())))
    name = b"DEFAULT".ljust(64, b"\x00")
    out.append(("x_fig56_set_mcr_info_cdl92", m.build_command(
        m.MT_VU_COMMAND, head,
        body(0x0003, 0x0000, extra=bytes((0x03, 0, 0, 0x80)) + bytes(4) + name),
        **env())))
    out.append(("x_fig57_get_mcr_info_cdi1", m.build_command(
        m.MT_VU_COMMAND, head, body(0x0004, 0x0001), **env())))
    for ct in (0x0005, 0x7FFF, 0xFFFF):
        out.append(("x_ct_%04x" % ct, m.build_command(
            m.MT_VU_COMMAND, head, body(ct), **env())))
    out.append(("x_other_entity", m.build_mvu_command(
        0x0000, **env(target_eid=EID ^ 1))))
    out.append(("x_vu_response_mvu_bytes", m.build_command(
        m.MT_VU_RESPONSE, head, body(0), **env())))
    return out


def model_answer(m, steps_mod, frame):
    eng = m.AecpEngineModel(steps_mod.SERVED, m.DescriptorImage(),
                            entity_id=EID, own_mac=OWN_MAC,
                            mvu_served=steps_mod.SERVED_MVU)
    return eng.deliver(frame)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("gen", "diff"))
    ap.add_argument("--tests", required=True, type=Path)
    ap.add_argument("--cases", required=True, type=Path)
    ap.add_argument("--rtl", type=Path)
    ap.add_argument("--mutant-tree", action="append", default=[], type=Path)
    a = ap.parse_args()
    m, st = load(a.tests)
    cs = cases(m)
    if a.mode == "gen":
        a.cases.write_text("".join("%s %s\n" % (n, f.hex()) for n, f in cs))
        print("%d cases written to %s" % (len(cs), a.cases))
        return 0
    rtl = {}
    for line in a.rtl.read_text().splitlines():
        if not line.strip():
            continue
        n, r = line.split()
        rtl[n] = None if r == "NONE" else bytes.fromhex(r)
    listed = dict(l.split() for l in a.cases.read_text().splitlines() if l.strip())
    bad = 0
    print("== exact-head model vs pinned RTL, byte for byte ==")
    for n, f in cs:
        assert listed[n] == f.hex(), "case file does not match builder: " + n
        got = model_answer(m, st, f)
        want = rtl[n]
        same = got == want
        bad += not same
        desc = "silence" if want is None else "mt=%d st=%d cdl=%d len=%d" % (
            want[15] & 0x0F, want[16] >> 3,
            ((want[16] & 7) << 8) | want[17], len(want))
        print("%-38s %s  rtl: %s" % (n, "MATCH" if same else "DIFFER", desc))
        if not same:
            print("   model %s" % (got.hex() if got else "NONE"))
            print("   rtl   %s" % (want.hex() if want else "NONE"))
    print("exact-head: %d cases, %d differ" % (len(cs), bad))
    for tree in a.mutant_tree:
        mm, _ = load(tree / "tests", with_steps=False)
        div = [n for n, f in cs if model_answer(mm, st, f) != rtl[n]]
        print("mutant %-26s diverges from the pinned RTL on %d case(s): %s"
              % (tree.name, len(div), ", ".join(div) or "-"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
