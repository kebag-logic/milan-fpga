#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gptp_sw_mutants.py - planted defects of gPTP in firmware that only the closed loop sees (#884), each caught by its
check of sim_main.cpp.

Each defect replaces one exact text of a firmware source in a scratch copy of sw/firmware/ctrl, builds the closed
loop on that copy (the Makefile's FW) and runs the one run that judges it; the run must print a [FAIL] line carrying
the named words. A text not found once, a run that passes, or a failure only elsewhere fails the campaign; the
unplanted firmware must pass every run first.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FW = HERE.parents[2] / "sw/firmware/ctrl"

#: (name, source under sw/firmware/ctrl, old text, new text, the run, the words its failing check must carry)
MUTANTS = (
    ("ingress-stamp-dropped", "gptp/gptp_mbx.c", "			gptp_port_ts(p, false, type, seq, stamp, true);",
     "			(void)seq;", "slave", "SLAVE if0 the PHC is within 100 ns of its grandmaster"),
    ("trailer-read-lsb-first", "gptp/gptp_mbx.c", "		stamp = (stamp << 8) | f->bytes[len + k];",
     "		stamp |= (uint64_t)f->bytes[len + k] << (8u * k);", "slave",
     "SLAVE if0 the PHC is within 100 ns of its grandmaster"),
    ("trailer-left-on-the-frame", "gptp/gptp_mbx.c", "	gptp_port_rx(p, f->bytes, len);",
     "	gptp_port_rx(p, f->bytes, f->len);", "slave", "SLAVE if1 a Pdelay_Req cut short by its last eight octets"),
    ("egress-stamp-dropped", "gptp/gptp_mbx.c",
     "		gptp_port_ts(&g->port[ev->interface], true, ev->ts_msg_type, ev->ts_seq, ev->ts_ns, ev->ts_ok);",
     "		(void)g;", "slave", "SLAVE if0 the measured link delay is its link's"),
    ("second-port-steers-first-phc", "gptp/gptp_mbx.c", "	g->phc.step(g->phc.ctx, port, delta_ns);",
     "	g->phc.step(g->phc.ctx, port & 0u, delta_ns);", "slave",
     "SLAVE if1 the PHC is within 100 ns of its grandmaster"),
    ("snapshot-not-kept", "gptp/gptp_mbx.c", "	g->snap[i] = *pub;", "	(void)pub;", "slave",
     "the snapshot holds the grandmaster it published"),
    ("notice-not-raised", "gptp/gptp_mbx.c", "			g->aecp.changed(g->aecp.ctx, i, ev);", "			(void)ev;",
     "slave", "the AVB_INFO and AS_PATH changes were raised"),
    ("path-answer-shifted", "gptp/gptp_mbx.c", "		out[k] = s->path[k];", "		out[k] = s->path[k + 1u];",
     "slave", "GET_AS_PATH is the snapshot's path"),
    ("publication-skips-gm", "gptp/gptp_mbx.c", "	w[0] = (uint32_t)pub->gm_id;", "	w[0] = 0u;", "slave",
     "the words the datapath takes are the snapshot's"),
    ("record-change-left-unpublished", "gptp/gptp_mbx.c",
     "	gptp_port_rx(p, f->bytes, len);\n	publish(g, f->interface);", "	gptp_port_rx(p, f->bytes, len);", "slave",
     "SLAVE the publication follows every port change"),
    ("event-change-left-unpublished", "gptp/gptp_mbx.c", "	publish(g, ev->interface);\n", "", "slave",
     "SLAVE the publication follows every port change"),
    ("tick-change-left-unpublished", "gptp/gptp_mbx.c", "		publish(the_gptp, i);", "", "slave",
     "SLAVE the publication follows every port change"),
    ("servo-sign", "gptp/gptp.c", "clamp64((p->srv.integ - kp * offset) >> 16, lim)",
     "clamp64((p->srv.integ + kp * offset) >> 16, lim)", "slave",
     "SLAVE if0 the PHC is within 100 ns of its grandmaster"),
    ("responder-t2-from-another-frame", "gptp/gptp.c", "gptp_ts_put(p->tx + F_BODY, p->rsp.t2);",
     "gptp_ts_put(p->tx + F_BODY, p->rsp.t2 + 1000u);", "slave",
     "SLAVE if0 the peer measures the link through the firmware's answers"),
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """One command in cwd, its output captured."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def one(work: Path, name: str, path: str | None, old: str | None, new: str | None, which: str,
        needle: str | None) -> tuple[str, bool, str]:
    """One arm under work/<name>: the unplanted firmware must pass `which`; a planted one must fail it with its
    needle's words. Returns the name, whether it did, and the line that says so."""
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    fw = d / "ctrl"
    shutil.copytree(FW, fw, ignore=shutil.ignore_patterns("test", "*.o"))
    if path is not None:
        src = fw / path
        text = src.read_text()
        if text.count(old) != 1:
            return name, False, f"REFUSED: its text is in {path} {text.count(old)} times, not once"
        src.write_text(text.replace(old, new))
    vl = os.environ.get("VERILATOR", "verilator")
    r = run(["make", "-s", f"VERILATOR={vl}", f"FW={fw}", f"MDIR={d / 'obj'}", f"RUN={which}", "run"], HERE)
    log = r.stdout + r.stderr
    if path is None:
        return name, r.returncode == 0 and "RESULT: PASS" in log, log
    fails = [ln for ln in log.splitlines() if "[FAIL]" in ln]
    if r.returncode == 0:
        return name, False, "SURVIVED: the run passed"
    hit = [ln for ln in fails if needle in ln]
    if not hit:
        return name, False, "MISSED: failed, not with its words:\n" + "\n".join(fails[:5]) + log[-400:]
    return name, True, "KILLED: " + hit[0].strip()


def main() -> int:
    """The baseline, then every planted defect in parallel; any survivor, miss or refusal fails the campaign."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build-dir", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    work = args.build_dir or Path(tempfile.mkdtemp(prefix="gptp-sw-mutants-"))
    name, ok, log = one(work, "baseline", None, None, None, "", None)
    print(f"baseline: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(log[-2000:])
        return 2
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        res = list(pool.map(lambda m: one(work, *m), MUTANTS))
    failed = 0
    for name, ok, log in res:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {log.splitlines()[0] if log else ''}")
        if not ok:
            failed += 1
            print("\n".join("      " + ln for ln in log.splitlines()[1:8]))
    print(f"== gptp in firmware, closed-loop planted defects: checks: {len(MUTANTS)}   failures: {failed} ==")
    print("RESULT: " + ("PASS" if failed == 0 else "FAIL"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
