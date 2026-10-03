#!/usr/bin/env python3
"""Lane B8, assignment item 4: the saved clock-source selection across one cold power cycle.

usage: pc_b8.py <name> pre|post
  (this host; the caller holds the bench lock; the power cycle itself is pc_cycle_b8.sh)

pre:  the as-found state (GET_CLOCK_SOURCE, formats, RX states, GET_COUNTERS) and the NVM
      status (`milan_nvm`); the binding rule, then the reference peer's AAF talker bound to the
      DUT's STREAM_INPUT 0 (the INPUT_STREAM source's input); SET_CLOCK_SOURCE 2 on the DUT's
      CLOCK_DOMAIN 0 (the DUT is the listener) and its read-back; the servo polled to LOCKED;
      `milan_nvm` read until the commit count has moved and nothing is dirty or in flight.
      The binding and the selection are left in place for the power cycle. On any failure the
      stage restores everything itself and the power cycle is not run.
post: after the boot: GET_CLOCK_SOURCE, the DUT's RX state and format, GET_COUNTERS and
      `milan_nvm`, before anything is sent to the DUT that changes it; the servo polled for
      LOCKED for 60 s with no action. If it does not lock, the RX state is read again and the
      binding rule and CONNECT_RX are applied, and the servo polled for 60 s more. Then the
      restore: SET_CLOCK_SOURCE to the as-found source and its read-back, the unbind, the
      listener format restored and read back, `milan_nvm` until the commits have landed.

Every step is an event in runs/<name>/events.jsonl; controller transactions in ctl.jsonl;
console reads in nvm-*.txt; servo polls (console_poll_b8.py) in poll-*.jsonl. Environment
(private): DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC.
"""
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
DUT = os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
DUT_EID = "020000fffe000001"
EID = {"dut": DUT_EID, "peer": PEER_EID}
RAWT = time.clock_gettime_ns
MONO_RAW = time.CLOCK_MONOTONIC_RAW
SRC_AAF = 2
CTR = [("dut", 0x0024, 0), ("dut", 0x0005, 0), ("dut", 0x0006, 0), ("peer", 0x0006, 0)]


def _term(signum, frame):
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
name, stage = sys.argv[1], sys.argv[2]
assert stage in ("pre", "post"), stage
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=True)
events = open(dest / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), mono_raw_ns=RAWT(MONO_RAW), stage=stage, kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def nvm(tag):
    """`milan_nvm` and `milan_status` (read-only); returns the parsed NVM fields."""
    path = dest / f"nvm-{stage}-{tag}.txt"
    r = subprocess.run(["python3", "-B", str(TOOLS / "console_read.py"), DUT, str(path), "milan_nvm", "milan_status"],
                       capture_output=True, text=True, timeout=60)
    txt = path.read_text(errors="replace") if path.exists() else ""
    f = {}
    m = re.search(r"slot A (\S+) seq (\d+), slot B (\S+) seq (\d+), authoritative (\S+), image seq (\d+)", txt)
    if m:
        f.update(slot_a=m.group(1), seq_a=int(m.group(2)), slot_b=m.group(3), seq_b=int(m.group(4)),
                 authoritative=m.group(5).rstrip(","), image_seq=int(m.group(6)))
    for k in ("dirty", "commit_busy", "pend", "valid", "backed"):
        m = re.search(rf"\b{k}=(\d+)", txt)
        if m:
            f[k] = int(m.group(1))
    m = re.search(r"commits ok=(\d+) failed=(\d+)", txt)
    if m:
        f.update(commits_ok=int(m.group(1)), commits_failed=int(m.group(2)))
    m = re.search(r"verdict=(\S+);", txt)
    if m:
        f["verdict"] = m.group(1)
    m = re.search(r"VERSION=([0-9a-fA-F]{8})", txt)
    if m:
        f["version"] = m.group(1)
    event("nvm", tag=tag, rc=r.returncode, file=path.name, **f)
    return f


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
             f"cd /tmp/a521 && sudo -n timeout 900 python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / f"agent-stderr-{stage}.txt", "w"),
            text=True, bufsize=1)
        self.log = open(dest / f"ctl-{stage}.jsonl", "a", buffering=1)
        line = ""
        for _ in range(3):
            line = self.readline()
            if '"agent-ready"' in line:
                break
        assert '"agent-ready"' in line, line

    def readline(self):
        line = self.p.stdout.readline()
        if not line:
            raise SystemExit("controller agent ended")
        self.log.write(json.dumps(dict(local_rx=round(time.time(), 6), line=json.loads(line))) + "\n")
        return line

    def cmd(self, **q):
        self.log.write(json.dumps(dict(local_tx=round(time.time(), 6), req=q)) + "\n")
        self.p.stdin.write(json.dumps(q) + "\n")
        self.p.stdin.flush()
        out = []
        while True:
            line = json.loads(self.readline())
            if line.get("type") == "done":
                return out
            if line.get("type") not in ("req",):
                out.append(line)

    def quit(self):
        try:
            self.p.stdin.write(json.dumps(dict(op="quit")) + "\n")
            self.p.stdin.flush()
            self.p.wait(15)
        except Exception:
            self.p.terminate()
            self.p.wait(10)
        event("agent-exit", rc=self.p.returncode)


def fmt_of(rows):
    for r in rows:
        if r.get("status") == "SUCCESS" and r.get("cmd") in ("GET_STREAM_FORMAT", "SET_STREAM_FORMAT"):
            return r["payload"][8:24]
    return None


def clk(ag, tag):
    rows = ag.cmd(op="clk", who="dut")
    r = next((x for x in rows if x.get("what") == "clock-dut"), {})
    src = int(r["payload"][8:12], 16) if r.get("status") == "SUCCESS" else None
    event("clock-read", tag=tag, status=r.get("status"), source=src)
    return src


def rx(ag, tag, idx=0):
    rows = ag.cmd(op="rx", who="dut", idx=idx)
    r = rows[0] if rows else {}
    out = {k: r.get(k) for k in ("status", "conn_count", "stream_id", "talker_uid", "flags", "vlan")}
    out["talker_is_peer"] = r.get("talker") == PEER_EID
    event("rx-state", tag=tag, idx=idx, **out)
    return out


def counters(ag, tag):
    got = {}
    for who, dt, i in CTR:
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=i)
        r = rows[0] if rows else {}
        got[f"{who}-{dt:#06x}-{i}"] = r.get("payload") if r.get("status") == "SUCCESS" else r.get("status")
    event("counters", tag=tag, payloads=got)
    return got


def binding_rule(ag, tag):
    t = fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0))
    l0 = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
    rec = dict(tag=tag, talker="peer-out-0", listener="dut-in-0", talker_fmt=t, listener_fmt=l0, set=None,
               listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        s = ag.cmd(op="setfmt", who="dut", idx=0, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s], echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)


def acmp(ag, op):
    rows = ag.cmd(op=op, t=PEER_EID, tu=0, l=DUT_EID, lu=0)
    main = next((r for r in rows if r.get("what") == op), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event(op, talker="peer-out-0", listener="dut-in-0", status=main.get("status"),
          conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
    return main.get("status") == 0


def setclk(ag, src, tag):
    rows = ag.cmd(op="setclk", who="dut", src=src)
    st = next((r.get("status") for r in rows if r.get("cmd") == "SET_CLOCK_SOURCE"), None)
    back = next((int(r["payload"][8:12], 16) for r in rows if r.get("what") == "clock-dut" and r.get("status") == "SUCCESS"),
                None)
    event("set-clock", tag=tag, src=src, status=st, readback=back, ok=back == src)
    return back


def poll_locked(tag, max_s):
    """console_poll_b8.py until two polls after the first LOCKED, or max_s; returns the seconds
    from the start of polling to the first LOCKED poll as (lo, hi), or None."""
    path = dest / f"poll-{stage}-{tag}.jsonl"
    t0 = RAWT(MONO_RAW)
    event("poll-start", tag=tag, max_s=max_s)
    r = subprocess.run(["python3", "-B", str(TOOLS / "console_poll_b8.py"), DUT, str(path), str(max_s), "0.5", "locked"],
                       timeout=max_s + 20)
    rows = [json.loads(l) for l in open(path) if l.startswith("{")] if path.exists() else []
    prev = None
    got = None
    for x in rows:
        if x.get("servo_state") == 4:
            got = ((prev["raw1"] - t0) / 1e9 if prev else 0.0, (x["raw1"] - t0) / 1e9)
            break
        prev = x
    states = []
    for x in rows:
        s = x.get("servo_state")
        if not states or states[-1][0] != s:
            states.append((s, round((x["raw1"] - t0) / 1e9, 3)))
    event("poll-end", tag=tag, rc=r.returncode, polls=len(rows), locked_s=got, state_changes=states)
    return got


def nvm_settled(tag, before, max_s=30):
    """milan_nvm every 3 s until the commit count has moved past `before` with nothing dirty
    or in flight, or max_s."""
    end = time.monotonic() + max_s
    k = 0
    f = {}
    while time.monotonic() < end:
        f = nvm(f"{tag}-{k}")
        k += 1
        if f.get("commits_ok", -1) > before and f.get("dirty") == 0 and f.get("commit_busy") == 0:
            break
        time.sleep(3.0)
    return f


pre_path = dest / "pre-found.json"
ag = None
try:
    ag = Agent()
    if stage == "pre":
        found = dict(clk=clk(ag, "as-found"), fmt_dut_in0=fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0)),
                     fmt_peer_out0=fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0)),
                     rx0=rx(ag, "as-found", 0), rx1=rx(ag, "as-found", 1))
        event("as-found", **found)
        if found["clk"] != 0 or (found["rx0"] or {}).get("conn_count") or (found["rx1"] or {}).get("conn_count"):
            raise SystemExit("not the recorded as-found state: nothing changed")
        pre_path.write_text(json.dumps(found))
        counters(ag, "as-found")
        n0 = nvm("as-found")
        changed = False
        try:
            binding_rule(ag, "pre")
            changed = True
            if not acmp(ag, "bind"):
                raise SystemExit("bind failed")
            if setclk(ag, SRC_AAF, "pre") != SRC_AAF:
                raise SystemExit("clock source set refused or not read back")
            lk = poll_locked("lock", 60)
            if lk is None:
                raise SystemExit("the servo did not read LOCKED within 60 s")
            clk(ag, "pre-locked")
            counters(ag, "pre-locked")
            n1 = nvm_settled("pre-saved", n0.get("commits_ok", 0))
            event("pre-done", commits_before=n0.get("commits_ok"), commits_after=n1.get("commits_ok"),
                  image_seq_before=n0.get("image_seq"), image_seq_after=n1.get("image_seq"))
            if not (n1.get("dirty") == 0 and n1.get("commit_busy") == 0):
                raise SystemExit("the NVM did not settle: no power cycle")
            print("PRE_OK")
        except BaseException as e:
            event("pre-failed", error=repr(e))
            if changed:
                setclk(ag, 0, "pre-restore")
                acmp(ag, "unbind")
                time.sleep(2.0)
                ag.cmd(op="setfmt", who="dut", idx=0, fmt=found["fmt_dut_in0"])
                event("format-final", fmt=fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0)),
                      as_found=found["fmt_dut_in0"])
                rx(ag, "pre-restore", 0)
            raise
    else:
        found = json.loads(pre_path.read_text())
        held = clk(ag, "post-boot")
        event("selection-held", source=held, expected=SRC_AAF, ok=held == SRC_AAF)
        fmt0 = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
        event("format-post-boot", fmt=fmt0)
        r0 = rx(ag, "post-boot", 0)
        counters(ag, "post-boot")
        nb = nvm("post-boot")
        lk = poll_locked("relock-noaction", 60)
        rebound = False
        if lk is None:
            rx(ag, "before-rebind", 0)
            binding_rule(ag, "post-rebind")
            acmp(ag, "bind")
            rebound = True
            lk = poll_locked("relock-after-rebind", 60)
        event("relock", locked_s=lk, rebind_needed=rebound)
        clk(ag, "post-locked")
        rx(ag, "post-locked", 0)
        counters(ag, "post-locked")
        time.sleep(5.0)
        # restore: the as-found source with its read-back, the unbind, the listener format
        back = setclk(ag, found["clk"], "restore")
        acmp(ag, "unbind")
        time.sleep(2.0)
        f_now = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
        if f_now != found["fmt_dut_in0"]:
            s = ag.cmd(op="setfmt", who="dut", idx=0, fmt=found["fmt_dut_in0"])
            event("format-restore", fmt=found["fmt_dut_in0"], status=[x.get("status") for x in s])
        f_end = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
        event("format-final", fmt=f_end, as_found=found["fmt_dut_in0"], equal=f_end == found["fmt_dut_in0"])
        clk(ag, "final")
        rx(ag, "final", 0)
        rx(ag, "final", 1)
        counters(ag, "final")
        nvm_settled("post-restore", nb.get("commits_ok", 0))
        print("POST_DONE")
finally:
    if ag is not None:
        ag.quit()
    event("end")
