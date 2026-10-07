#!/usr/bin/env python3
"""R532-1 reviewer mutation probe: plant one defect per copy, run the SRP suites, name what fails.

usage: r532_mutants.py CLONE WORK FIRST LAST [WORKERS]
Each defect replaces exactly one site (refused otherwise) in a private copy of
sw/firmware/ctrl or of lwSRP's src/, then runs srp_mbx, srp_latency and srp_walk
at two interfaces through the PR's own arm_srp. A defect is caught when a suite
exits non-zero with a named [FAIL] that is not a build error.
"""
import os, re, shutil, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
CLONE = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(CLONE / "sw/firmware/ctrl/test"), str(CLONE / "sw/firmware/gtest")]
import srp_arms, fw_gtest  # noqa: E402
from ctrl_build import Tree, CTRL, Refusal  # noqa: E402
srp_arms.lwsrp_pin = lambda p: "probe"   # the mutated lwSRP copy is not a git checkout
SUITES = ("srp_mbx.cpp", "srp_latency.cpp", "srp_walk.cpp")
# (name, root 'ctrl' or 'lwsrp', relative path, old, new)
DEFECTS = [
 ("A01-overhead-no-tag", "ctrl", "srp/srp_mbx.c", "max_frame_size + 22u", "max_frame_size + 18u"),
 ("A02-priority-shift", "ctrl", "srp/srp_mbx.c", "(i->domain.priority << 5)", "(i->domain.priority << 4)"),
 ("A03-failure-codes-swapped", "ctrl", "srp/srp_mbx.c", "allocated ? 1 : 2", "allocated ? 2 : 1"),
 ("A04-msrp-da-unchecked", "ctrl", "srp/srp_mbx.c", "da == 0x0180c200000eull", "(da == 0x0180c200000eull || 1)"),
 ("A05-domain-vid-4095", "ctrl", "srp/srp_mbx.c", "d->vid < 4095", "d->vid <= 4095"),
 ("A06-bind-vid-4095", "ctrl", "srp/srp_mbx.c", "vid == 0 || vid >= 4095", "vid == 0 || vid > 4095"),
 ("A07-domain-change-keeps-vlan-sent", "ctrl", "srp/srp_mbx.c",
  "    if (i->domain.vid != i->next_domain.vid) {\n        i->vlan_sent = false;", "    if (0) {\n        i->vlan_sent = false;"),
 ("A08-listener-cb-no-stop", "ctrl", "srp/srp_mbx.c", "                i->stop_owed[n] = true;", "                (void)0;"),
 ("A09-readyfailed-cb-not-ready", "ctrl", "srp/srp_mbx.c", "declaration == MSRP_LISTENER_DECL_READY ||\n                               declaration == MSRP_LISTENER_DECL_READY_FAILED", "declaration == MSRP_LISTENER_DECL_READY"),
 ("A10-link-not-required", "ctrl", "srp/srp_mbx.c", "bool active = link && i->vlan_sent", "bool active = i->vlan_sent"),
 ("A11-admission-90pct", "ctrl", "srp/srp_mbx.c", "link_rate_bps * 3u / 4u", "link_rate_bps * 9u / 10u"),
 ("A12-ifg-preamble-dropped", "ctrl", "srp/srp_mbx.c", "(size + 20u)", "(size + 0u)"),
 ("P01-loop-ready-ignored", "ctrl", "loop/ctrl_loop.c", "if (l->rx[ch].ready != NULL && !l->rx[ch].ready(l->rx[ch].ctx))", "if (0)"),
 ("L01-threepacked-216", "lwsrp", "core/mrp_pdu.c", "ev[k] > 215u", "ev[k] > 216u"),
 ("L02-msrp-da-0x21", "lwsrp", "modules/msrp.c", "0x00u, 0x00u, 0x0Eu", "0x00u, 0x00u, 0x21u"),
 ("L03-talker-da-not-incremented", "lwsrp", "modules/msrp.c", "        increment_stream(t->dest_mac, 6, offset);\n", ""),
 ("L04-leaveall-draw-wide", "lwsrp", "core/mrp_mad.c", "% (ps->leaveall_cs / 2u - 1u)", "% (ps->leaveall_cs / 2u + 100u)"),
 ("L05-leaveall-all-types", "lwsrp", "core/mrp_mad.c", "        if (a->attr_type == attr_type) {\n            deliver_event(rc->app, rc->ps, a, MRP_EVENT_RLA", "        if (a->attr_type == attr_type || 1) {\n            deliver_event(rc->app, rc->ps, a, MRP_EVENT_RLA"),
 ("L06-lv-rlv-restarts-timer", "lwsrp", "core/mrp_mad.c",
  "        _RE(REG_IND_NONE, REG_TIMER_START, MRP_REG_STATE_LV), /* IN: Start leavetimer; LV */\n        _RX,                                /* LV: -x-                  */",
  "        _RE(REG_IND_NONE, REG_TIMER_START, MRP_REG_STATE_LV), /* IN: Start leavetimer; LV */\n        _RE(REG_IND_NONE, REG_TIMER_START, MRP_REG_STATE_LV),"),
 ("L07-ignore-subtype-registers", "lwsrp", "core/mrp_pdu.c", "                    if (decl[k % 4u] == 0) {\n                        continue;", "                    if (0) {\n                        continue;"),
 ("L08-an-note8-removed", "lwsrp", "core/mrp_mad.c", "    if (ev == MRP_EVENT_TX && ai->appl == MRP_APPL_STATE_AN &&\n        ai->reg != MRP_REG_STATE_IN) {", "    if (0) {"),
 ("L09-reclaim-lv", "lwsrp", "core/mrp_mad.c", "        if (a->reg == MRP_REG_STATE_MT &&\n            (a->appl", "        if (a->reg != MRP_REG_STATE_IN &&\n            (a->appl"),
 ("L10-refused-send-commits", "lwsrp", "core/mrp_mad.c", "    ps->in_send = false;\n    if (r != 0) {\n        return r;\n    }", "    ps->in_send = false;\n    (void)r;"),
 ("L11-p2p-note4-ignored", "lwsrp", "core/mrp_mad.c", "    if ((p2p && ev == MRP_EVENT_RJOININ &&", "    if ((0 && ev == MRP_EVENT_RJOININ &&"),
 ("L12-endmark-optional", "lwsrp", "core/mrp_mad.c", "        pdu[off++] = 0; pdu[off++] = 0;\n        ps->prepared_pdu = pdu;", "        ps->prepared_pdu = pdu;"),
]
def one(args):
    work, d = args
    name, root, rel, old, new = d
    w = Path(work) / name
    shutil.rmtree(w, ignore_errors=True); w.mkdir(parents=True)
    src = w / "ctrl"; lw = w / "lwSRP"
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(CLONE / "third_party/lwSRP/src", lw / "src")
    target = (src if root == "ctrl" else lw / "src") / rel
    if name != "CONTROL":
        text = target.read_text()
        if text.count(old) != 1:
            return name, "REFUSED", f"{text.count(old)} planting sites", {}
        target.write_text(text.replace(old, new))
    results = {}
    for suite in SUITES:
        try:
            out = srp_arms.arm_srp(Tree(src, w / "build", w / "reuse", fw_gtest.Build(jobs=2)), lw, 2, test=suite)
            fails = sorted(set(re.findall(r"^\s*\[FAIL\] ([\w.]+):", out.log, re.M)))
            results[suite] = (out.rc, fails)
            (w / f"{suite}.log").write_text(out.log)
        except Refusal as e:
            results[suite] = ("BUILD", [str(e)[:200]])
    caught = any(rc == 1 and f for rc, f in results.values())
    built = all(rc != "BUILD" for rc, f in results.values())
    verdict = ("CAUGHT" if caught else "ESCAPED") if built else "BUILD-ERROR"
    if name == "CONTROL":
        verdict = "CONTROL-PASS" if all(rc == 0 for rc, f in results.values()) else "CONTROL-FAIL"
    shutil.rmtree(w / "build", ignore_errors=True)
    return name, verdict, "", results
if __name__ == "__main__":
    work, first, last = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    chosen = ([("CONTROL", "ctrl", "", "", "")] if first == 0 else []) + DEFECTS[max(first - 1, 0):last]
    with ProcessPoolExecutor(workers) as ex:
        for name, verdict, why, results in ex.map(one, [(work, d) for d in chosen]):
            detail = "; ".join(f"{s}: rc={rc} {','.join(f) if f else ''}" for s, (rc, f) in results.items())
            print(f"[{verdict}] {name} {why} {detail}", flush=True)
