#!/usr/bin/env python3
"""Lane B16 (new; lane B15's points_b15.py restructured: its Agent class, controller agent (b8_ctl.py),
binding rule, captures, tap fetch and teardown are lane B15's, unchanged unless stated here): one locked
action of the lane, the caller holding the bench lock.

usage: run_b16.py <name> <raw_root> <mode> [seconds]
  mode loop     step 2, the positive reference: the reference peer's own listener (its STREAM_INPUT 0,
                whose channels 0/1 the external capture records) is unbound from its as-found talker and
                bound to the peer's own STREAM_OUTPUT 0 under the binding rule (the listener adapts to the
                talker's format). The DUT is not bound. Captures: both taps and the external capture.
  mode dirb     step 4, Direction B end to end: the peer's STREAM_OUTPUT 0 to the DUT's STREAM_INPUT 0
                under the binding rule (the as-found input map must hold the four identity mappings; this
                tool edits no map); the peer's listener stays as found. Captures: both taps, the external
                capture and McASP0's recording of the DUT's TDM output (the caller stops the SoC board's
                to-host bridge leg around this action).
  mode dirbloop step 4 with the loopback of mode loop also in place, so the external capture witnesses the
                peer's talker while the DUT receives it (four points at once, as lane B15's pts1 meant).
  mode looptap  mode loop with both taps started before the unbind and the bind (added after run loop1, whose
                taps started after the bind and so held none of the bind's ACMP exchange), so the ACMP messages
                of the bind are on record.
  mode dira     B16b (added after the manager's ruling on the B16 STOP): lane B15's `dira`, the four-point
                capture with (d) a positive control of the whole observation chain. As mode dirb, and McASP0
                also plays lane B6's loop (b6_tone.py: 997 Hz on channel 0, 9,973 Hz on channel 1, -1 dBFS,
                eight channels S32_LE) into the DUT's TDM input while it records the DUT's TDM output. The
                DUT's as-found STREAM_PORT_OUTPUT 0 map (eight identity mappings, checked, not edited) puts
                the loop on the DUT's AAF talker, which the peer's STREAM_INPUT 0 receives as found (no bind
                or unbind of it) and renders to its digital output, (d). The loop is copied to the board,
                its SHA-256 checked there, and removed at the end. The board-side commands, the checks and
                the cleanup are lane B15's points_b15.py `dira`, with the board path /tmp/a603-loop.raw.
  mode b0       B16b step 4, case B0 (the DUT on INTERNAL; lane B9's run_b9.py B0 binds, this lane's
                captures): mode dira with lane B9's second Direction B bind, the peer's CRF talker
                (STREAM_OUTPUT 2) to the DUT's STREAM_INPUT 1, under the binding rule, before the AAF bind.
                No clock source is set. The window, <seconds>, starts at least 20 s after the last bind
                (lane B7's settle); McASP0 records and plays for the window, the external capture covers
                it, and the taps cover only its first TAP_S_B0 seconds (the THD+N grade is McASP0's; the
                taps prove (a) and (b) equal to (c) where they overlap). The DUT's console words of lane
                B9's run_b9.py (DUT_READS: servo, slip counters, AAF meter, CRF sink) are read before the
                binds and after the captures. GET_COUNTERS adds the DUT's STREAM_INPUT 1; the final
                read-back adds the DUT's STREAM_INPUT 1 format.

Changes against lane B15's points_b15.py:
  * the modes above; lane B15's `control` (both binds) is kept as `dirbloop`; `dira` was dropped in B16 and is
    restored in B16b as mode dira;
  * after every bind the listener's rx state (GET_RX_STATE) and its GET_COUNTERS are polled every 2 s for
    SETTLE_POLL_S, so whether the listener resolves the talker's stream ID and locks is timed (lane B15
    read the rx state once, right after the bind, and the counters before and after the captures only);
  * the talker's tx state (GET_TX_STATE) is read with the polls;
  * a precheck refuses to bind while the SoC board's McASP playback is open (the owner's music);
  * raw files carry the lane's own prefixes (/tmp/b16-* on the tap host, the staging from CTL_STAGE);
  * the final read-back also covers the DUT's STREAM_INPUT 1 and the peer's STREAM_INPUT 8, and compares the
    rx states without their flags word (lane B15 saw the peer's flags read 0x0002 right after a rebind and
    0x0082 later); the flags are still recorded;
  * McASP0's recording is given a 1 s buffer (arecord -B 1000000; lane B15's used arecord's default), so a
    late SSH read cannot overrun it; the recording's own log records any overrun (built for B16, first used
    in B16b).

Environment (private): CTL_HOST, CTL_IFACE, CTL_STAGE, PEER_EID, PEER_MAC, SOC_SSH, TAP_HOST, TAP_PEER_IF,
TAP_DUT_IF, CAP_CARD, CAP_NCH, CAP_FMT.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
E = os.environ
CTL, IFACE, STAGE = E["CTL_HOST"], E["CTL_IFACE"], E["CTL_STAGE"]
PEER_EID, PEER_MAC = E["PEER_EID"], E["PEER_MAC"]
DUT_EID = "020000fffe000001"
name, raw_root, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
assert MODE in ("loop", "dirb", "dirbloop", "looptap", "dira", "b0"), MODE
DIRA = MODE in ("dira", "b0")
DIRB = MODE in ("dirb", "dirbloop", "dira", "b0")
B0 = MODE == "b0"
TAP_S_B0 = 40
B0_SETTLE_S = 20.0
DUT_READS = ["milan_status", "milan_nvm", "mem_read 0x90000738 4", "mem_read 0x90000748 8", "mem_read 0x900008d4 12",
             "mem_read 0x900008f8 8", "mem_read 0x900008e0 8", "mem_read 0x90000660 20", "mem_read 0x90000694 8",
             "mem_read 0x900006cc 12"]
IDENT8 = "000f" + "0000" + "0000" + "0001" + "0008" + "0000" + "".join("0000%04x%04x0000" % (c, c) for c in range(8))
BOARD_LOOP = "/tmp/a603-loop.raw"
SECS = int(sys.argv[4]) if len(sys.argv) > 4 else 10
SETTLE_POLL_S = 12.0
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
TAPF = "ether[40:2]=0x22f0 or ether[44:2]=0x22f0"
IDENT4 = "000e000000000001000400000000000000000000000000010001000000000002000200000000000300030000"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            SSH + [CTL, f"cd {STAGE} && sudo -n timeout 600 python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / "agent-stderr.txt", "w"),
            text=True, bufsize=1)
        self.log = open(dest / "ctl.jsonl", "a", buffering=1)
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


def clk_of(rows, who):
    for r in rows:
        if r.get("what") == f"clock-{who}" and r.get("status") == "SUCCESS":
            return int(r["payload"][8:12], 16)
    return None


def rxs(rows):
    return {k: rows[0].get(k) for k in ("status", "conn_count", "stream_id", "talker", "talker_uid", "flags", "dmac")} if rows else None


def ctr_words(payload):
    """GET_COUNTERS payload: descriptor (4 octets), counters_valid, then 32 counters (IEEE 1722.1 7.4.42)."""
    if not payload:
        return None
    b = bytes.fromhex(payload)
    return [int.from_bytes(b[8 + 4 * i: 12 + 4 * i], "big") for i in range(32)] if len(b) >= 136 else None


def counters(ag, tag, who_idx=(("dut", 0), ("peer", 0)) + ((("dut", 1),) if B0 else ())):
    out = {}
    for who, idx in who_idx:
        rows = ag.cmd(op="counters", who=who, dtype=5, idx=idx)
        r = rows[-1] if rows else {}
        w = ctr_words(r.get("payload"))
        out[f"{who}-in-{idx}"] = w[:13] if w else None
        event("counters", tag=tag, who=who, dtype=5, idx=idx, status=r.get("status"), payload=r.get("payload"))
    return out


def poll_listener(ag, who, idx, tag):
    """Every 2 s for SETTLE_POLL_S: the listener's rx state, its counters (MEDIA_LOCKED, UNLOCKED, ...,
    FRAMES_RX) and the peer talker's tx state."""
    t0 = time.time()
    while True:
        rx = rxs(ag.cmd(op="rx", who=who, idx=idx))
        tx = rxs(ag.cmd(op="tx", who="peer", idx=0))
        rows = ag.cmd(op="counters", who=who, dtype=5, idx=idx)
        w = ctr_words((rows[-1] if rows else {}).get("payload"))
        event("listener-poll", tag=tag, listener=f"{who}-in-{idx}", dt=round(time.time() - t0, 3), rx=rx,
              peer_tx0=dict(conn_count=(tx or {}).get("conn_count"), stream_id=(tx or {}).get("stream_id")),
              media_locked=w[0] if w else None, media_unlocked=w[1] if w else None,
              frames_rx=w[11] if w else None)
        if time.time() - t0 >= SETTLE_POLL_S:
            return
        time.sleep(2.0)


def bind_rule(ag, talker, listener, sets):
    """The owner's binding rule: the listener adapts. talker/listener = (who, idx)."""
    t = fmt_of(ag.cmd(op="fmt", who=talker[0], dir="out", idx=talker[1]))
    l0 = fmt_of(ag.cmd(op="fmt", who=listener[0], dir="in", idx=listener[1]))
    rec = dict(talker=f"{talker[0]}-out-{talker[1]}", listener=f"{listener[0]}-in-{listener[1]}", talker_fmt=t,
               listener_fmt=l0, set=None, listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        s = ag.cmd(op="setfmt", who=listener[0], idx=listener[1], fmt=t)
        sets.append((listener, l0))
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s], echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who=listener[0], dir="in", idx=listener[1]))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)
    eid = {"dut": DUT_EID, "peer": PEER_EID}
    rows = ag.cmd(op="bind", t=eid[talker[0]], tu=talker[1], l=eid[listener[0]], lu=listener[1])
    main = next((r for r in rows if r.get("what") == "bind"), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event("bind", talker=rec["talker"], listener=rec["listener"], status=main.get("status"),
          conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
    if main.get("status") != 0:
        raise SystemExit(f"bind failed: {main}")


def unbind(ag, talker_eid, tu, listener, tag):
    eid = {"dut": DUT_EID, "peer": PEER_EID}
    rows = ag.cmd(op="unbind", t=talker_eid, tu=tu, l=eid[listener[0]], lu=listener[1])
    main = next((r for r in rows if r.get("what") == "unbind"), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event("unbind", tag=tag, talker=talker_eid, tu=tu, listener=f"{listener[0]}-in-{listener[1]}",
          status=main.get("status"), conn_count=after.get("conn_count"))
    return main.get("status")


def mcasp_playback_closed():
    r = subprocess.run(SSH + [E["SOC_SSH"], "head -1 /proc/asound/card0/pcm0p/sub0/status; "
                              "ps -o pid,args | grep -E '[a]play|[p]lay-folder|[a]udio2tdm|[f]lac2tdm' || true"],
                       capture_output=True, text=True, timeout=30)
    out = r.stdout.strip()
    event("mcasp-playback-check", rc=r.returncode, out=out)
    return r.returncode == 0 and out.splitlines()[0].strip() == "closed" and len(out.splitlines()) == 1


def start_captures(mcasp, tap_s=None, only_tap=False, procs=None):
    procs = {} if procs is None else procs
    tap_s = SECS + 14 if tap_s is None else tap_s
    if "tap" in procs:
        pass
    else:
        start_tap(procs, tap_s)
        if only_tap:
            event("tap-started-early", seconds=tap_s)
            return procs
    time.sleep(2.0)
    procs["extcap"] = (subprocess.Popen(["sudo", "-n", "arecord", "-D", f"hw:{E['CAP_CARD']},0", "-f", E["CAP_FMT"], "-r", "48000",
                                         "-c", E["CAP_NCH"], "-t", "raw", "-d", str(SECS + 6), str(raw / "extcap.raw")],
                                        stdout=open(dest / "extcap.txt", "w"), stderr=subprocess.STDOUT), time.time())
    if mcasp:
        time.sleep(2.0)
        soc = (f"cat /proc/uptime 1>&2; arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -B 1000000 -d {SECS}; "
               f"echo arecord_rc=$? 1>&2; cat /proc/uptime 1>&2")
        if DIRA:
            # lane B15's dira: lane B6's McASP0 playback of the loop, started 2 s before the recording, ending by itself
            soc = (f"cat /proc/uptime 1>&2; {{ while cat {BOARD_LOOP}; do :; done | aplay -D hw:0,0 -t raw -c 8 -f S32_LE "
                   f"-r 48000 -d {SECS + 6}; echo aplay_rc=$?; }} > /tmp/a603-aplay.log 2>&1 < /dev/null & AP=$!; sleep 2; "
                   f"grep -E '^(state|hw_ptr)' /proc/asound/card0/pcm0p/sub0/status 1>&2; "
                   f"arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -B 1000000 -d {SECS}; echo arecord_rc=$? 1>&2; "
                   f"wait $AP; cat /tmp/a603-aplay.log 1>&2; cat /proc/uptime 1>&2")
        procs["mcasp"] = (subprocess.Popen(SSH + [E["SOC_SSH"], soc], stdout=open(raw / "mcasp-all.raw", "wb"),
                                           stderr=open(dest / "soc-record.log", "w")), time.time())
    event("captures-started", started={k: round(v[1], 3) for k, v in procs.items()})
    return procs


def start_tap(procs, tap_s):
    tap = (f"sudo -n timeout {tap_s} tcpdump -i {E['TAP_PEER_IF']} -w /tmp/b16-{name}-peer.pcap '{TAPF}' 2> /tmp/b16-{name}-peer.err & "
           f"sudo -n timeout {tap_s} tcpdump -i {E['TAP_DUT_IF']} -w /tmp/b16-{name}-dut.pcap '{TAPF}' 2> /tmp/b16-{name}-dut.err & "
           f"wait; cat /tmp/b16-{name}-peer.err /tmp/b16-{name}-dut.err; ls -l /tmp/b16-{name}-*.pcap")
    procs["tap"] = (subprocess.Popen(SSH + [E["TAP_HOST"], tap], stdout=open(dest / "tap.txt", "w"),
                                     stderr=subprocess.STDOUT), time.time())


def wait_captures(procs):
    for k in ("mcasp", "extcap", "tap"):
        if k not in procs:
            continue
        p, t0 = procs[k]
        try:
            rc = p.wait(timeout=SECS + 60)
        except subprocess.TimeoutExpired:
            p.terminate()
            rc = p.wait(10)
        event("capture-done", what=k, rc=rc, seconds=round(time.time() - t0, 3))


def fetch_taps():
    got = {}
    for side in ("peer", "dut"):
        src = f"/tmp/b16-{name}-{side}.pcap"
        dst = raw / f"tap-{side}.pcap"
        r = subprocess.run(["scp", "-q", f"{E['TAP_HOST']}:{src}", str(dst)], timeout=120)
        got[side] = dict(rc=r.returncode, bytes=dst.stat().st_size if dst.exists() else None,
                         sha256=sha(dst) if dst.exists() else None)
    r = subprocess.run(SSH + [E["TAP_HOST"], f"sudo -n rm -f /tmp/b16-{name}-peer.pcap /tmp/b16-{name}-dut.pcap "
                              f"/tmp/b16-{name}-peer.err /tmp/b16-{name}-dut.err; ls /tmp/b16-* 2>&1"],
                       capture_output=True, text=True, timeout=60)
    event("taps-fetched", files=got, tap_host_after=r.stdout.strip(), rm_rc=r.returncode)


def state(ag):
    st = {}
    st["fmt-dut-in-0"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
    st["fmt-peer-out-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0))
    st["fmt-peer-in-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=0))
    st["clk-dut"] = clk_of(ag.cmd(op="clk", who="dut"), "dut")
    st["clk-peer"] = clk_of(ag.cmd(op="clk", who="peer"), "peer")
    st["rx-dut-0"] = rxs(ag.cmd(op="rx", who="dut", idx=0))
    st["rx-dut-1"] = rxs(ag.cmd(op="rx", who="dut", idx=1))
    st["rx-peer-0"] = rxs(ag.cmd(op="rx", who="peer", idx=0))
    st["rx-peer-8"] = rxs(ag.cmd(op="rx", who="peer", idx=8))
    rows = ag.cmd(op="map", act="get", dtype=0x000E, didx=0)
    st["map-dut-in"] = rows[-1].get("payload") if rows else None
    if DIRA:
        rows = ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
        st["map-dut-out"] = rows[-1].get("payload") if rows else None
    if B0:
        st["fmt-dut-in-1"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=1))
    return st


def dut_read(tag):
    """Lane B9's DUT console words (read-only commands; the caller holds the bench lock)."""
    r = subprocess.run(["python3", "-B", str(TOOLS / "console_read.py"), E["DUT_CONSOLE"], str(dest / f"dut-{tag}.txt"),
                        *DUT_READS], capture_output=True, text=True, timeout=90)
    event("dut-read", tag=tag, rc=r.returncode)


ag = None
found = {}
sets = []
binds = []
procs = None
peer_unbound = None
try:
    if not mcasp_playback_closed():
        raise SystemExit("WAIT: the SoC board's McASP playback is open (the owner's music); nothing changed")
    ag = Agent()
    found = state(ag)
    event("as-found", **found)
    if (found["rx-dut-0"] or {}).get("conn_count"):
        raise SystemExit("the DUT's STREAM_INPUT 0 is already bound: not this lane's as-found state, nothing changed")
    if DIRB and (found["map-dut-in"] or "")[:len(IDENT4)] != IDENT4:
        raise SystemExit("STOP: the DUT's STREAM_PORT_INPUT 0 does not hold the four identity mappings; this tool edits no map")
    if DIRA:
        pr = found["rx-peer-0"] or {}
        event("dira-check", map_dut_out=found["map-dut-out"], peer_in_0=pr)
        if (found["map-dut-out"] or "")[:len(IDENT8)] != IDENT8 or pr.get("talker") != DUT_EID or pr.get("conn_count") != 1:
            raise SystemExit("STOP: dira needs the as-found eight identity mappings on the DUT's STREAM_PORT_OUTPUT 0 and the "
                             "peer's STREAM_INPUT 0 bound to the DUT's AAF talker; nothing changed")
        loop = raw / "b6-loop.raw"
        r = subprocess.run(["python3", "-B", str(TOOLS / "b6_tone.py"), str(loop)], capture_output=True, text=True, timeout=60)
        lsha = sha(loop)
        r2 = subprocess.run(["scp", "-q", str(loop), f"{E['SOC_SSH']}:{BOARD_LOOP}"], timeout=60)
        r3 = subprocess.run(SSH + [E["SOC_SSH"], f"sha256sum {BOARD_LOOP}"], capture_output=True, text=True, timeout=30)
        event("loop-staged", tone_rc=r.returncode, bytes=loop.stat().st_size, sha256=lsha, scp_rc=r2.returncode,
              board=r3.stdout.strip())
        if not r3.stdout.startswith(lsha):
            raise SystemExit("the loop on the board does not match")
    if MODE == "looptap":
        procs = start_captures(mcasp=False, tap_s=int(SETTLE_POLL_S + SECS + 30), only_tap=True)
        time.sleep(3.0)
    if MODE in ("loop", "dirbloop", "looptap"):
        pr = found["rx-peer-0"] or {}
        if pr.get("conn_count"):
            unbind(ag, pr["talker"], int(pr["talker_uid"]), ("peer", 0), "loop-unbind-as-found")
            peer_unbound = pr
        bind_rule(ag, ("peer", 0), ("peer", 0), sets)
        binds.append((PEER_EID, 0, ("peer", 0)))
        poll_listener(ag, "peer", 0, "after-loop-bind")
    if B0:
        if (found["rx-dut-1"] or {}).get("conn_count"):
            raise SystemExit("the DUT's STREAM_INPUT 1 is already bound: not this lane's as-found state, nothing changed")
        if found["clk-dut"] != 0:
            raise SystemExit("B0 needs the DUT on INTERNAL as found; nothing changed")
        dut_read("before-binds")
        bind_rule(ag, ("peer", 2), ("dut", 1), sets)
        binds.append((PEER_EID, 2, ("dut", 1)))
    if DIRB:
        bind_rule(ag, ("peer", 0), ("dut", 0), sets)
        binds.append((PEER_EID, 0, ("dut", 0)))
        t_last_bind = time.time()
        poll_listener(ag, "dut", 0, "after-dut-bind")
    if B0:
        rx1 = rxs(ag.cmd(op="rx", who="dut", idx=1))
        rows = ag.cmd(op="counters", who="dut", dtype=5, idx=1)
        w = ctr_words((rows[-1] if rows else {}).get("payload"))
        event("listener-read", listener="dut-in-1", rx=rx1, media_locked=w[0] if w else None,
              media_unlocked=w[1] if w else None, frames_rx=w[11] if w else None)
        clk = clk_of(ag.cmd(op="clk", who="dut"), "dut")
        event("clock-read", who="dut", source=clk)
        if clk != 0:
            raise SystemExit("the DUT's clock source is not INTERNAL after the binds")
        time.sleep(max(0.0, B0_SETTLE_S - (time.time() - t_last_bind)))
    counters(ag, "before")
    procs = start_captures(mcasp=DIRB, procs=procs, tap_s=TAP_S_B0 if B0 else None)
    wait_captures(procs)
    counters(ag, "after")
    if B0:
        event("clock-read", who="dut", source=clk_of(ag.cmd(op="clk", who="dut"), "dut"))
        dut_read("after-captures")
    if MODE in ("loop", "dirbloop", "looptap"):
        poll_listener(ag, "peer", 0, "after-captures")
finally:
    event("teardown")
    if ag is not None:
        try:
            for t_eid, tu, lis in reversed(binds):
                unbind(ag, t_eid, tu, lis, "teardown")
            time.sleep(1.0)
            for lis, f0 in reversed(sets):
                s = ag.cmd(op="setfmt", who=lis[0], idx=lis[1], fmt=f0)
                event("format-restore", listener=f"{lis[0]}-in-{lis[1]}", fmt=f0, status=[r.get("status") for r in s])
            if peer_unbound:
                t_eid, tu = peer_unbound["talker"], int(peer_unbound["talker_uid"])
                tf = fmt_of(ag.cmd(op="fmt", who="dut" if t_eid == DUT_EID else "peer", dir="out", idx=tu))
                lf = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=0))
                event("format-check", ok=tf == lf, talker=f"{t_eid}-out-{tu}", listener="peer-in-0", talker_fmt=tf,
                      listener_fmt=lf, set=None, note="the as-found bind, restored")
                rows = ag.cmd(op="bind", t=t_eid, tu=tu, l=PEER_EID, lu=0)
                main = next((r for r in rows if r.get("what") == "bind"), {})
                after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
                event("rebind-as-found", status=main.get("status"), conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
                time.sleep(3.0)
            fin = state(ag)
            norm = lambda d: {k: ({kk: vv for kk, vv in v.items() if kk != "flags"} if isinstance(v, dict) else v) for k, v in d.items()}
            diff = [k for k in fin if json.dumps(norm(fin)[k], sort_keys=True) != json.dumps(norm(found).get(k), sort_keys=True)]
            event("final", equal_to_found=not diff, differ=diff, **fin)
        except BaseException as e:
            event("teardown-error", error=repr(e))
        ag.quit()
    if procs is not None:
        try:
            fetch_taps()
        except BaseException as e:
            event("fetch-error", error=repr(e))
    if DIRA:
        try:
            r = subprocess.run(SSH + [E["SOC_SSH"], f"rm -f {BOARD_LOOP} /tmp/a603-aplay.log; ls /tmp; "
                                      f"ps -o pid,args | grep -E '[a]play|[a]record'; "
                                      f"grep -E '^(state|closed)' /proc/asound/card0/pcm0p/sub0/status"],
                               capture_output=True, text=True, timeout=30)
            event("board-cleanup", rc=r.returncode, out=r.stdout.strip())
        except BaseException as e:
            event("board-cleanup-error", error=repr(e))
    for f in sorted(raw.glob("*")):
        event("raw", file=f.name, bytes=f.stat().st_size, sha256=sha(f))
    event("end")
