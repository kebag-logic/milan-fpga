#!/usr/bin/env python3
"""Every MVU row of the head's contract feature, built exactly as its When
step builds it, answered by the pinned RTL (tb/pp_top probe) and by the head
model, compared byte for byte.  Plus reviewer-chosen extra frames.

Usage:
  rtl_vs_model.py --repo <clone> --sim <probe Vpp_top_sim dir> --out <receipt>

The pinned harness addresses the device as EID/OWN_MAC and speaks as
CTLR_EID/CTLR_MAC (tb/pp_top/sim_main.cpp).  Each captured frame has those
four envelope fields and a unique sequence_id rewritten; the model is built
with the same identity, so the two answers are comparable on every octet.
The model's answer to the ORIGINAL (unrewritten) frame is also required to
equal its answer to the rewritten one outside those fields.
"""
import argparse
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True)
ap.add_argument("--sim", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

REPO = Path(args.repo).resolve()
sys.path.insert(0, str(REPO / "tests" / "steps"))
import aecp_engine_model as M          # noqa: E402
import aecp_engine_steps as S          # noqa: E402

PP_OWN_MAC = bytes.fromhex("0A0B0C0D0E0F")
PP_EID = 0x123456789ABCDEF0
PP_CTLR_MAC = bytes.fromhex("0202DEADBEEF")
PP_CTLR_EID = 0x7777000000000042


class Ctx:
    pass


def fresh():
    c = Ctx()
    S.step_engine_milan8(c)
    return c


def rewrite(frame, seq):
    f = bytearray(frame)
    f[0:6] = PP_OWN_MAC
    f[6:12] = PP_CTLR_MAC
    f[18:26] = struct.pack(">Q", PP_EID)
    f[26:34] = struct.pack(">Q", PP_CTLR_EID)
    f[34:36] = struct.pack(">H", seq)
    return bytes(f)


def mask_env(rsp):
    """The response with its envelope fields zeroed (for model-vs-model)."""
    f = bytearray(rsp)
    for a, b in ((0, 12), (18, 36)):
        f[a:b] = bytes(b - a)
    return bytes(f)


def outline_rows(title):
    """Rows of the named Scenario Outline in the head's feature, as dicts."""
    text = (REPO / "tests/features/aecp_response_contract.feature").read_text()
    start = text.index("Scenario Outline: " + title)
    nxt = re.search(r"\n  (Scenario|# ---)", text[start + 10:])
    block = text[start: start + 10 + (nxt.start() if nxt else len(text))]
    rows, header = [], None
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("Examples:"):
            header = None
            continue
        if s.startswith("|"):
            cells = [x.strip() for x in s.strip("|").split("|")]
            if header is None:
                header = cells
            else:
                rows.append(dict(zip(header, cells)))
    return rows


cases = []   # (label, frame as the step built it, expectation text)

for r in outline_rows("a Milan MVU command is answered as a VENDOR_UNIQUE "
                      "response with its protocol_id intact"):
    c = fresh()
    S.step_send_mvu(c, r["command_type"], r["form"])
    cases.append(("ROW mvu %s %s" % (r["command_type"], r["form"]),
                  c.aecp_cmd, "status %s cdl %s" % (r["status"], r["cdl"])))

for r in outline_rows("only a whole Figure 5.3 GET_MILAN_INFO is served"):
    c = fresh()
    S.step_send_mvu_shaped(c, r["protocol_id"], r["word"], r["reserved"],
                           int(r["cdl_in"]))
    cases.append(("ROW guard %s w%s res%s cdl%s (%s)" % (
        r["protocol_id"], r["word"], r["reserved"], r["cdl_in"], r["varied"]),
        c.aecp_cmd, "status %s cdl %s" % (r["status"], r["cdl"])))

for r in outline_rows("the GET_MILAN_INFO octets under another message_type "
                      "are not an MVU command"):
    c = fresh()
    S.step_send_mvu_bytes_other_type(c, int(r["mt"]))
    cases.append(("ROW mt %s %s" % (r["mt"], r["message_type"]), c.aecp_cmd,
                  "status 1 cdl 20"))

n_rows = len(cases)

# reviewer-chosen extras: more @26 nibbles, longer served commands, junk
# past Figure 5.3, the RECOMMENDED forms under a foreign protocol_id
for pid in ("00-1B-C5-0A-C0-00", "00-1B-C5-0A-C3-00", "00-1B-C5-0A-01-00",
            "00-1B-C5-0A-F1-00", "00-1B-C5-0A-41-00", "00-1B-C5-0A-CF-00",
            "00-1B-C5-0B-C1-00", "00-1B-C5-0A-C1-80"):
    c = fresh()
    S.step_send_mvu_shaped(c, pid, "0x0000", "0x0000", 20)
    cases.append(("EXTRA guard %s cdl20" % pid, c.aecp_cmd, "echo"))
for cdl in (21, 27, 28, 60, 200, 300, 400, 500, 592, 600):
    # the guard step's fill is bytes(range(n)), which stops at 255 octets,
    # so the long forms are built with the same builder and a wrapping fill
    f = M.build_mvu_command(0, from_32=bytes(i & 0xFF for i in range(cdl - 20)))
    cases.append(("EXTRA served-long cdl%d" % cdl, f, "?"))
for word in ("0x0001", "0x0005", "0x7FFF", "0xFFFF", "0x0100"):
    c = fresh()
    S.step_send_mvu_shaped(c, "00-1B-C5-0A-C1-00", word, "0x0000", 20)
    cases.append(("EXTRA word %s cdl20" % word, c.aecp_cmd, "echo"))
for ct in (1, 3):
    form, at30, from32 = M.MVU_COMMAND_FORMS[ct]
    f = M.build_mvu_command(ct, bytes.fromhex("001BC50AC101"), at30, from32)
    cases.append(("EXTRA foreign-pid %s" % form, f, "echo"))
# junk (non-zero) octets past Figure 5.3 on a served command
f = bytearray(M.build_mvu_command(0, from_32=bytes([0xA5] * 12)))
cases.append(("EXTRA served cdl32 junk tail", bytes(f), "served"))

seq0 = 0xD000
lines, model_rsp = [], []
for i, (label, frame, _) in enumerate(cases):
    rw = rewrite(frame, seq0 + i)
    lines.append(rw.hex())
    mdl = M.AecpEngineModel(S.SERVED, M.DescriptorImage(), entity_id=PP_EID,
                            own_mac=PP_OWN_MAC, mvu_served=S.SERVED_MVU)
    a = mdl.deliver(rw)
    orig = M.AecpEngineModel(S.SERVED, M.DescriptorImage(),
                             mvu_served=S.SERVED_MVU).deliver(frame)
    assert (a is None) == (orig is None) and (
        a is None or mask_env(a) == mask_env(orig)), label
    model_rsp.append((a, mdl.cmd_count, mdl.resp_count))

work = Path(args.out).resolve().parent.parent / "scratch"
work.mkdir(parents=True, exist_ok=True)
pin, pout = work / "probe_in.txt", work / "probe_out.txt"
pin.write_text("\n".join(lines) + "\n")
env = dict(os.environ, PROBE_IN=str(pin), PROBE_OUT=str(pout))
run = subprocess.run(["./obj_dir/Vpp_top_sim"], cwd=args.sim, env=env,
                     capture_output=True, text=True, timeout=3000)
rtl = [l.split() for l in pout.read_text().splitlines()]
assert len(rtl) == len(cases), (len(rtl), len(cases), run.stdout[-2000:])

out = []
out.append("probe stdout tail: " + run.stdout.strip().splitlines()[-1])
out.append("probe exit: %d" % run.returncode)
out.append("rows from the head feature: %d; reviewer extras: %d"
           % (n_rows, len(cases) - n_rows))
mism = 0
for i, ((label, frame, exp), (mrsp, mc, mr), r) in enumerate(
        zip(cases, model_rsp, rtl)):
    rhex = r[1]
    rbytes = None if rhex == "SILENCE" else bytes.fromhex(rhex)
    same = rbytes == mrsp
    if not same:
        mism += 1
    def desc(b):
        if b is None:
            return "SILENCE"
        st = b[16] >> 3
        cdl = ((b[16] & 7) << 8) | b[17]
        return "mt %d status %d cdl %d len %d" % (b[15] & 0xF, st, cdl, len(b))
    out.append("%s | %s | cmd cdl %d | RTL %s %s %s %s | model %s | %s" % (
        "MATCH" if same else "MISMATCH", label,
        ((frame[16] & 7) << 8) | frame[17], desc(rbytes), r[2], r[3], r[4],
        desc(mrsp), "expect " + exp))
    if not same:
        out.append("   cmd   " + lines[i])
        out.append("   rtl   " + rhex)
        out.append("   model " + (mrsp.hex() if mrsp else "SILENCE"))
out.append("TOTAL %d frames, %d byte-exact mismatches" % (len(cases), mism))
Path(args.out).write_text("\n".join(out) + "\n")
print("\n".join(out[-3:]))
sys.exit(1 if mism or run.returncode else 0)
