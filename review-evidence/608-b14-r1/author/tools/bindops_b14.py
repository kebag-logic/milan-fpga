#!/usr/bin/env python3
"""Lane B14: one bind or unbind, with read-back, through the controller agent (b8_ctl.py).

usage: bindops_b14.py <out_dir> <tag> bind|unbind|state|maps <talker_who> <talker_idx> <listener_who> <listener_idx>
`maps` reads (only) GET_AUDIO_MAP of the DUT's STREAM_PORT_INPUT 0 and STREAM_PORT_OUTPUT 0 as well.
The caller holds the bench lock (run_locked_b14.sh). `bind` applies the owner's binding rule first
(read the talker's and the listener's stream formats; on a difference set the LISTENER's to the
talker's and read it back; stop if it does not take it). Every step is one JSON line in
<out_dir>/<tag>.jsonl; the agent's raw transcript stays under /tmp/608-b14/raw.
Environment (private): CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
DUT_EID = "020000fffe000001"
EID = {"dut": DUT_EID, "peer": PEER_EID}
out, tag, op = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
tw, ti, lw, li = sys.argv[4], int(sys.argv[5]), sys.argv[6], int(sys.argv[7])
assert op in ("bind", "unbind", "state", "maps") and tw in EID and lw in EID
out.mkdir(parents=True, exist_ok=True)
log = open(out / f"{tag}.jsonl", "a", buffering=1)
raw = open(Path("/tmp/608-b14/raw") / f"bindops-{tag}.jsonl", "a", buffering=1)


def emit(**kw):
    r = dict(t=round(time.time(), 6), **kw)
    log.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


p = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
                      f"cd /tmp/608-b14 && sudo -n timeout 60 python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)


def readline():
    line = p.stdout.readline()
    if not line:
        raise SystemExit("controller agent ended")
    raw.write(line)
    return json.loads(line)


def cmd(**q):
    p.stdin.write(json.dumps(q) + "\n")
    p.stdin.flush()
    rows = []
    while True:
        r = readline()
        if r.get("type") == "done":
            return rows
        if r.get("type") != "req":
            rows.append(r)


def fmt(who, d, i):
    for r in cmd(op="fmt", who=who, dir=d, idx=i):
        if r.get("status") == "SUCCESS":
            return r["payload"][8:24]
    return None


def rx():
    r = (cmd(op="rx", who=lw, idx=li) or [{}])[0]
    t = r.get("talker")
    return dict(conn_count=r.get("conn_count"), talker={DUT_EID: "dut", PEER_EID: "peer"}.get(t, t),
                talker_uid=r.get("talker_uid"), flags=r.get("flags"))


try:
    while '"agent-ready"' not in json.dumps(readline()):
        pass
    emit(kind="before", listener=f"{lw}-in-{li}", rx=rx())
    if op == "bind":
        tf, lf = fmt(tw, "out", ti), fmt(lw, "in", li)
        rec = dict(talker_fmt=tf, listener_fmt=lf, set=None)
        if tf is None or lf is None:
            emit(kind="format-check", ok=False, **rec)
            raise SystemExit("format read failed")
        if tf != lf:
            s = cmd(op="setfmt", who=lw, idx=li, fmt=tf)
            rec["set"] = [r.get("status") for r in s]
            rec["listener_after"] = fmt(lw, "in", li)
            if rec["listener_after"] != tf:
                emit(kind="format-check", ok=False, **rec)
                raise SystemExit("STOP: the listener did not take the talker's format")
        emit(kind="format-check", ok=True, **rec)
    if op in ("bind", "unbind"):
        rows = cmd(op=op, t=EID[tw], tu=ti, l=EID[lw], lu=li)
        main = next((r for r in rows if r.get("what") == op), {})
        emit(kind=op, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", status=main.get("status"))
        time.sleep(1.0)
    emit(kind="after", listener=f"{lw}-in-{li}", rx=rx())
    if op == "maps":
        for dt in (0x000E, 0x000F):
            for r in cmd(op="map", act="get", dtype=dt, didx=0):
                if r.get("cmd") == "GET_AUDIO_MAP":
                    b = bytes.fromhex(r.get("payload", ""))
                    n = int.from_bytes(b[8:10], "big") if r.get("status") == "SUCCESS" else 0
                    maps = [[int.from_bytes(b[12 + 8 * k + 2 * j:14 + 8 * k + 2 * j], "big") for j in range(4)] for k in range(n)]
                    emit(kind="audio-map", descriptor_type=f"{dt:#06x}", descriptor_index=0, status=r.get("status"),
                         number_of_maps=int.from_bytes(b[6:8], "big") if len(b) >= 8 else None, mappings=maps, payload=r.get("payload"))
finally:
    try:
        p.stdin.write(json.dumps(dict(op="quit")) + "\n")
        p.stdin.flush()
        p.wait(15)
    except Exception:
        p.terminate()
