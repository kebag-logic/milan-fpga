#!/usr/bin/env python3
"""Replay the recorded contract-feature frames through the pinned RTL probe
and compare each RTL answer with the offline model's answer, byte for byte.

Usage: rtl_vs_model.py <frames.jsonl> <Vpp_top_sim> <out-prefix> [min_line max_line]

Only the addressing differs between the two worlds: the model's own MAC and
entity_id are rewritten to the pp_top harness's (0A-0B-0C-0D-0E-0F,
0x123456789ABCDEF0) on the way in, and the RTL's are rewritten back on the
way out. Every other octet of both answers is compared, including the
Ethernet padding.
"""
import json
import os
import subprocess
import sys

MODEL_MAC = bytes.fromhex("001b92001122")
MODEL_EID = bytes.fromhex("001b92fffe001122")
PP_MAC = bytes.fromhex("0a0b0c0d0e0f")
PP_EID = bytes.fromhex("123456789abcdef0")

frames_path, sim, prefix = sys.argv[1:4]
lo, hi = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 10**9)
recs = [json.loads(l) for l in open(frames_path, encoding="utf-8")]
sel = [(i, r) for i, r in enumerate(recs) if lo <= r["line"] <= hi]


def to_pp(f):
    f = bytearray(f)
    assert f[0:6] == MODEL_MAC and f[18:26] == MODEL_EID, "unexpected addressing"
    f[0:6] = PP_MAC
    f[18:26] = PP_EID
    return bytes(f)


def from_pp(f):
    f = bytearray(f)
    if f[6:12] == PP_MAC:
        f[6:12] = MODEL_MAC
    if f[18:26] == PP_EID:
        f[18:26] = MODEL_EID
    return bytes(f)


inp = prefix + ".in"
with open(inp, "w", encoding="utf-8") as fh:
    for i, r in sel:
        fh.write("f%03d %s\n" % (i, to_pp(bytes.fromhex(r["frame"])).hex()))
env = dict(os.environ, R280_PROBE_IN=os.path.abspath(inp))
simdir = os.path.dirname(os.path.dirname(os.path.abspath(sim)))
p = subprocess.run([os.path.abspath(sim)], cwd=simdir, env=env,
                   capture_output=True, text=True, timeout=3000)
open(prefix + ".sim.log", "w", encoding="utf-8").write(p.stdout + p.stderr)
rtl = {}
for line in p.stdout.splitlines():
    parts = line.split()
    if len(parts) >= 3 and parts[0] == "R280" and parts[1].startswith("f"):
        rtl[parts[1]] = None if parts[2] == "NONE" else bytes.fromhex(parts[3])
assert "R280 probe done" in p.stdout, "probe did not finish: exit %d" % p.returncode

match = mismatch = 0
out = []
for i, r in sel:
    key = "f%03d" % i
    model = None if r["model"] is None else bytes.fromhex(r["model"])
    got = rtl.get(key, b"MISSING")
    got_m = got if got in (None, b"MISSING") else from_pp(got)
    ok = got_m == model
    match += ok
    mismatch += not ok
    f = bytes.fromhex(r["frame"])
    desc = "mt=%d cdl=%d @22..=%s" % (f[15] & 15, ((f[16] & 7) << 8) | f[17],
                                      f[36:46].hex())
    if model is not None:
        desc += " -> model mt=%d st=%d cdl=%d" % (
            model[15] & 15, model[16] >> 3, ((model[16] & 7) << 8) | model[17])
    else:
        desc += " -> model NONE"
    out.append("%s %s line %d %s | %s" % (key, "MATCH" if ok else "MISMATCH",
                                         r["line"], desc, r["scenario"][:90]))
    if not ok:
        out.append("   model %s" % (None if model is None else model.hex()))
        out.append("   rtl   %s" % (None if got_m in (None, b"MISSING") else got_m.hex()
                                    if got_m != b"MISSING" else "MISSING"))
out.append("frames %d  match %d  mismatch %d  sim exit %d"
           % (len(sel), match, mismatch, p.returncode))
open(prefix + ".txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out[-3:]))
sys.exit(0 if mismatch == 0 else 1)
