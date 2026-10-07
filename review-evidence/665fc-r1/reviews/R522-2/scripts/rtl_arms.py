#!/usr/bin/env python3
"""Reviewer probe: plant the round-2 RTL arms of tb/verilator/mbx/mutants.py
(plus rx-subtype-ignored and reviewer-added boundary arms) in scratch copies,
through both adapters, and record EVERY failing check per arm.

usage: rtl_arms.py <exported-tree-root> <work-dir> [--jobs N]
"""
import sys, json, argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
ap.add_argument("tree"); ap.add_argument("work"); ap.add_argument("--jobs", type=int, default=8)
a = ap.parse_args()
here = Path(a.tree).resolve() / "tb/verilator/mbx"
sys.path.insert(0, str(here))
import os; os.chdir(here)
import mutants as m

ROUND2 = {"pkg-maap-defend-tuple-dropped", "rx-msg-type-off-by-one", "rx-classified-before-msg-type",
          "rx-tuple-msg-type-ignored", "rx-own-unicast-never-counted", "rx-defend-any-unicast",
          "rx-short-frame-never-classified", "rx-subtype-ignored"}
arms = [x for x in m.ARMS if x.name.removesuffix("-axil") in ROUND2]
# reviewer-added arms (not in the PR's table): boundary probes
EXTRA = [
    # a frame ending at byte 14 classified on the PREVIOUS frame's subtype
    ("rev-short-frame-stale-subtype", "KL_mbx_rx.sv",
     "subtype   = (cnt_r == 11'(MBX_SUBTYPE_BYTE_C)) ? rx_data_i : sub_r;", "subtype   = sub_r;"),
    # decided at byte 14 AND again at byte 15 (drain starts on the byte-14 verdict)
    ("rev-decided-twice", "KL_mbx_rx.sv",
     "assign cls_at_w = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) || (rx_last_i && cnt_r == 11'(MBX_SUBTYPE_BYTE_C));",
     "assign cls_at_w = (cnt_r == 11'(MBX_MSG_TYPE_BYTE_C)) || (cnt_r == 11'(MBX_SUBTYPE_BYTE_C));"),
    # the tuple's message_type taken from the stale per-frame register (0 at byte 15)
    ("rev-tuple-msg-from-register", "KL_mbx_rx.sv",
     "&& MBX_TUPLE_MSG_MASK_TBL_C[j][{1'b0, msg}]) begin", "&& MBX_TUPLE_MSG_MASK_TBL_C[j][{1'b0, msg_r}]) begin"),
    # the DEFEND tuple's mask widened to every type in the package
    ("rev-pkg-defend-mask-all", "KL_mbx_pkg.sv",
     "MBX_CH_MAAP_M1_MSG_MASK_C = 32'h00000004;", "MBX_CH_MAAP_M1_MSG_MASK_C = 32'h0000FFFF;"),
    # the DEFEND tuple's mask set to PROBE instead of DEFEND
    ("rev-pkg-defend-mask-probe", "KL_mbx_pkg.sv",
     "MBX_CH_MAAP_M1_MSG_MASK_C = 32'h00000004;", "MBX_CH_MAAP_M1_MSG_MASK_C = 32'h00000002;"),
]
for name, path, old, new in EXTRA:
    arms += [m.Arm(name, path, old, new, 0, "*"), m.Arm(name + "-axil", path, old, new, 1, "*")]

work = Path(a.work).resolve(); work.mkdir(parents=True, exist_ok=True)

def one(arm):
    rc, log = m.build_and_run(m.plant(arm, work), work / arm.name, arm.host)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    tally = [ln.strip() for ln in log.splitlines() if "checks:" in ln]
    needle_hit = arm.needle == "*" or any(arm.needle in ln for ln in fails)
    return {"arm": arm.name, "host": arm.host, "rc": rc, "needle": arm.needle, "needle_failed": needle_hit,
            "caught": rc == 1 and needle_hit and bool(fails), "tally": tally[-1] if tally else log[-400:],
            "fails": fails}

ctl = []
for host in (0, 1):
    rc, log = m.build_and_run(m.RTL, work / f"control-{host}", host)
    ctl.append({"host": host, "rc": rc, "tally": [l for l in log.splitlines() if "checks:" in l][-1:]})
with ThreadPoolExecutor(max_workers=a.jobs) as pool:
    res = list(pool.map(one, arms))
json.dump({"controls": ctl, "arms": res}, open(work / "rtl_arms.json", "w"), indent=1)
for c in ctl: print(f"control host {c['host']}: rc={c['rc']} {c['tally']}")
for r in res:
    print(f"[{'caught' if r['caught'] else 'ESCAPED'}] {r['arm']}: rc={r['rc']} {len(r['fails'])} fail(s); {r['tally']}")
    for f in r["fails"][:6]: print("     ", f)
