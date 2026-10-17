#!/usr/bin/env python3
"""Lane B21 round 3: unbind and rebind cycles of the as-found Direction A binding (this host; the
caller holds the bench lock). Lane B5's cycle: DISCONNECT_RX, a 2 s hold, the binding rule, CONNECT_RX,
then a dwell. It drives b8_ctl.py's agent on the controller host over one SSH session.

Binding rule (owner): before every bind, read the talker's (DUT STREAM_OUTPUT 0) and the listener's
(peer STREAM_INPUT 0) stream formats; if they differ, set the listener's to the talker's and read it
back; never set the talker's; never refuse the bind. Every cycle ends bound, the as-found state; a
failed bind stops the cycles and is retried once.

usage: restart_b21.py <out_dir> <cycles> <hold_s> <dwell_s>
Environment: CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

out, ncyc, hold, dwell = Path(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
CTL, IFACE, PEID, PMAC = (os.environ[k] for k in ("CTL_HOST", "CTL_IFACE", "PEER_EID", "PEER_MAC"))
DUT = "020000fffe000001"
log = open(out / "agent.jsonl", "w", buffering=1)
ev = open(out / "cycles.jsonl", "w", buffering=1)
limit = int(ncyc * (hold + dwell + 6) + 120)
p = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
                      f"cd /tmp/a625 && sudo -n timeout {limit} python3 -B b8_ctl.py agent {IFACE} {PEID} {PMAC}"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(out / "agent.err", "w"), text=True, bufsize=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    ev.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def readline():
    ln = p.stdout.readline()
    if not ln:
        raise SystemExit("agent ended")
    log.write(ln)
    return json.loads(ln) if ln.startswith("{") else {}


def cmd(**q):
    p.stdin.write(json.dumps(q) + "\n")
    p.stdin.flush()
    rows = []
    while True:
        r = readline()
        if r.get("type") == "done":
            return rows
        if r.get("cmd") or r.get("message_type") is not None or r.get("status") is not None:
            rows.append(r)


def fmt_of(rows):
    for r in rows:
        if r.get("format"):
            return r["format"]
    return None


def binding_rule(tag):
    t = fmt_of(cmd(op="fmt", who="dut", dir="out", idx=0))
    lf = fmt_of(cmd(op="fmt", who="peer", dir="in", idx=0))
    rec = dict(tag=tag, talker=t, listener=lf, set=None)
    if t and lf and t != lf:
        rows = cmd(op="setfmt", who="peer", idx=0, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in rows], after=fmt_of(cmd(op="fmt", who="peer", dir="in", idx=0)))
    event("binding-rule", **rec)
    return rec


def acmp(op):
    rows = cmd(op=op, t=DUT, tu=0, l=PEID, lu=0)
    main = rows[0] if rows else {}
    after = rows[1] if len(rows) > 1 else {}
    event(op, status=main.get("status"), t_tx=main.get("t_tx"), t_rx=main.get("t_rx"),
          rx_after=dict(status=after.get("status"), conn_count=after.get("conn_count"), flags=after.get("flags"),
                        stream_id=after.get("stream_id")))
    return main, after


while True:
    r = readline()
    if r.get("type") == "agent-ready":
        break
event("start", cycles=ncyc, hold_s=hold, dwell_s=dwell)
ok = True
try:
    cmd(op="rx", who="peer", idx=0)
    for c in range(1, ncyc + 1):
        event("cycle-start", cycle=c)
        acmp("unbind")
        time.sleep(hold)
        binding_rule(f"cycle-{c}")
        m, a = acmp("bind")
        if m.get("status") not in (0, "SUCCESS") or not a.get("conn_count"):
            event("bind-failed", cycle=c, status=m.get("status"))
            time.sleep(1.0)
            binding_rule(f"cycle-{c}-retry")
            m, a = acmp("bind")
            ok = m.get("status") in (0, "SUCCESS") and bool(a.get("conn_count"))
            event("bind-retry", cycle=c, ok=ok)
            if not ok:
                break
        time.sleep(dwell)
finally:
    rows = cmd(op="rx", who="peer", idx=0)
    event("final-rx-state", rows=[dict(status=r.get("status"), conn_count=r.get("conn_count"), flags=r.get("flags"),
                                        stream_id=r.get("stream_id"), talker=r.get("talker")) for r in rows])
    p.stdin.write(json.dumps(dict(op="quit")) + "\n")
    p.stdin.flush()
    try:
        p.wait(20)
    except subprocess.TimeoutExpired:
        p.terminate()
    event("end", ok=ok, agent_rc=p.returncode)
