#!/usr/bin/env python3
"""Tie each new or changed MVU row to a frame the pinned RTL answered.

The two review rounds R280-1 and R281-1 drove MVU frames through a build of
the pinned processor's tb/pp_top (424c688) and published each command frame
and the RTL's answer (R281-1 receipts/mvu_cases.txt + mvu_rtl_answers.txt,
R280-1 receipts/rtl_probe_run.txt). This lane did not build or run RTL.

For every row, the command is built the way the step builds it, and a receipt
case is looked for with the same message_type, the same control_data_length
and the same AECPDU octets from @22 to the end of the payload: every octet the
engine can read. Addressing and sequence_id are the review bench's, so they
are not compared, but only receipt frames addressed to the bench's own
entity are used. The head model is then fed that receipt case's own command,
with the bench identities, and its frame is compared byte for byte with the
RTL's.

usage: python3 -B xcheck_rows_vs_rtl.py <lane-root> <review-evidence/536-r1>
"""

import struct
import sys
from pathlib import Path

LANE = Path(sys.argv[1]).resolve()
EVID = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(LANE / "tests" / "steps"))
import aecp_engine_model as m  # noqa: E402
from aecp_engine_steps import SERVED, SERVED_MVU  # noqa: E402

EID = 0x123456789ABCDEF0                     # tb/pp_top/sim_main.cpp
OWN_MAC = bytes.fromhex("0A0B0C0D0E0F")


def receipts():
    """name -> (command frame, RTL answer frame or None), both review rounds."""
    out = {}
    r281 = EVID / "reviews/R281-1/receipts"
    cmds = dict(ln.split() for ln in (r281 / "mvu_cases.txt").read_text().splitlines() if ln.strip())
    for ln in (r281 / "mvu_rtl_answers.txt").read_text().splitlines():
        if ln.strip():
            name, resp = ln.split()
            out["R281-1 " + name] = (bytes.fromhex(cmds[name]),
                                     None if resp == "NONE" else bytes.fromhex(resp))
    r280 = {}
    for ln in (EVID / "reviews/R280-1/receipts/rtl_probe_run.txt").read_text().splitlines():
        parts = ln.split()
        if len(parts) == 4 and parts[0] == "R280":
            r280.setdefault(parts[2], {})[parts[1]] = bytes.fromhex(parts[3])
    for name, pair in r280.items():
        out["R280-1 " + name] = (pair["CMD"], pair["GOT"])
    return out


def readable(frame):
    """(message_type, cdl, AECPDU @22 to the end of the payload)."""
    pdu = frame[m.ETH_HDR:]
    cdl = ((pdu[2] & 0x07) << 8) | pdu[3]
    return pdu[1] & 0x0F, cdl, bytes(pdu[22:12 + cdl])


def rows():
    """(row label, command frame) for each new or changed row, built as the steps build them."""
    out = []
    for ct, (fig, at30, from32) in m.MVU_COMMAND_FORMS.items():
        out.append(("MVU %#06x in %s" % (ct, fig),
                    m.build_mvu_command(ct, reserved=at30, from_32=from32)))
    pid = "00-1B-C5-0A-C1-00"
    guard = [("FF-1B-C5-0A-C1-00", 0, 0, 20), ("00-FF-C5-0A-C1-00", 0, 0, 20),
             ("00-1B-FF-0A-C1-00", 0, 0, 20), ("00-1B-C5-FF-C1-00", 0, 0, 20),
             ("00-1B-C5-0A-FF-00", 0, 0, 20), ("00-1B-C5-0A-D1-00", 0, 0, 20),
             ("00-1B-C5-0A-C2-00", 0, 0, 20), ("00-1B-C5-0A-C1-FF", 0, 0, 20),
             ("00-1B-C5-0A-C1-01", 0, 0, 20), (pid, 0x8000, 0, 20), (pid, 0, 0, 19),
             (pid, 0, 0xDEAD, 20), (pid, 0, 0, 24), (pid, 0, 0, 112)]
    for p, word, res, cdl in guard:
        out.append(("guard %s word %#06x reserved %#06x cdl %d" % (p, word, res, cdl),
                    m.build_mvu_command(word, bytes.fromhex(p.replace("-", "")), res,
                                        bytes(range(max(cdl - 20, 0))), cdl=cdl)))
    for mt in (0, 2, 4, 8, 10, 12, 14):
        f = bytearray(m.build_mvu_command())
        f[m.ETH_HDR + 1] = (f[m.ETH_HDR + 1] & 0xF0) | mt
        out.append(("GET_MILAN_INFO octets as message_type %d" % mt, bytes(f)))
    return out


def model_answer(cmd):
    eng = m.AecpEngineModel(SERVED, m.DescriptorImage(), entity_id=EID, own_mac=OWN_MAC,
                            mvu_served=SERVED_MVU)
    return eng.deliver(cmd)


def main():
    rec = receipts()
    by_content = {}
    for name, (cmd, _rtl) in rec.items():
        #! only frames addressed to the bench entity: a frame for another
        #! entity tests the drop arc, not the row's decode
        if int.from_bytes(cmd[m.ETH_HDR + 4:m.ETH_HDR + 12], "big") == EID:
            by_content.setdefault(readable(cmd), []).append(name)
    matched = unmatched = bad = 0
    for label, frame in rows():
        key = readable(frame)
        names = by_content.get(key, [])
        if not names:
            unmatched += 1
            near = [n for ns in by_content.values() for n in ns
                    if readable(rec[n][0])[:2] == key[:2]]
            diffs = {}
            for n in near:
                other = readable(rec[n][0])[2]
                diffs[n] = [22 + i for i, (a, b) in enumerate(zip(key[2], other)) if a != b]
            best = min(diffs.items(), key=lambda kv: len(kv[1])) if diffs else None
            print("NO RTL CASE  %-58s mt %d cdl %d%s" % (
                label, key[0], key[1],
                "; nearest %s differs at @%s" % (best[0], ",@".join(map(str, best[1])))
                if best else "; no case of that message_type and length"))
            continue
        matched += 1
        verdicts = []
        for n in names:
            cmd, rtl = rec[n]
            same = model_answer(cmd) == rtl
            bad += not same
            desc = "silence" if rtl is None else "st %d cdl %d" % (
                rtl[16] >> 3, ((rtl[16] & 7) << 8) | rtl[17])
            verdicts.append("%s (%s, model %s)" % (n, desc, "==" if same else "!="))
        print("RTL CASE     %-58s %s" % (label, "; ".join(verdicts)))
    print("%d rows matched to an RTL-answered frame, %d without one; %d model/RTL mismatches"
          % (matched, unmatched, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
