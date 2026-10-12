#!/usr/bin/env python3
# Lane B16c copy of lane B16b's run_b16.py (SHA-256 424234725a20...): modes bcrf and baaf added for the manager's
# ruling on the B16b STOP; every other mode is unchanged. The B16c changes, each stated in full:
#   * mode bcrf / baaf: mode b0's binds, captures and teardown, with lanes B9 and B10's following set (run_b9.py's
#     BCRF and BAAF): the DUT's CLOCK_DOMAIN set to CLOCK_SOURCE 1 (bcrf, the peer's CRF stream on STREAM_INPUT 1)
#     or 2 (baaf, the peer's AAF stream on STREAM_INPUT 0) after the binds, read back, refused unless read back;
#   * the ruling's exception, these two modes only: before the binds the peer's CLOCK_DOMAIN is set to its
#     CLOCK_SOURCE 0 (INTERNAL) with SET_CLOCK_SOURCE and read back with GET_CLOCK_SOURCE; the mode refuses to
#     start unless the peer reads CLOCK_SOURCE 1 (its STREAM_INPUT 8, the CRF input) and that input is bound to
#     the DUT's STREAM_OUTPUT 1, as found. Teardown: the DUT's clock source back to 0 (read back), the DUT's binds
#     undone, then the peer's clock source back to its as-found 1 (read back), so no closed loop forms at any step;
#   * lane B9's console poll (console_poll_b8.py, unchanged, 0.5 s, `file:` stop) from before the peer's set to
#     after both clock-source restores, and lane B9's wait for the servo's LOCKED (60 s, Poll.wait_state as in
#     run_b9.py); the window starts SETTLE_S (20 s) after the DUT's set, and not before LOCKED; the DUT's console
#     words of mode b0 are read before the poll and after it (the console is the poll's meanwhile);
#   * lane B9's tone monitor (ToneMon, unchanged: the tone source's playback status from /proc every 0.2 s,
#     passive); the mode refuses to start unless the tone plays (run_b9.py's check);
#   * lane B9's window marks: GET_COUNTERS of the DUT's CLOCK_DOMAIN 0, both DUT listeners, the peer's listener
#     STREAM_INPUT 0 and the peer's CLOCK_DOMAIN 0, and GET_CLOCK_SOURCE of both entities, at the window's start,
#     middle and 15 s before its end, and after it;
#   * the McASP playback check (the owner's music) also runs just before the peer's set, the binds and the DUT's
#     set (the ruling: before each change);
#   * SIGTERM runs the teardown (run_b9.py's handler), so a deadline restores the clock sources and binds;
#   * the poll's and the tone monitor's files stay in the raw directory; their summaries go to the events.
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
  mode bcrf     B16c, case B-CRF (lanes B9 and B10's BCRF): the peer's CLOCK_DOMAIN set to INTERNAL and read
                back (the ruling's exception), mode b0's two binds, then the DUT's CLOCK_DOMAIN set to
                CLOCK_SOURCE 1 and read back; the window, <seconds>, from 20 s after the set and not before the
                servo reads LOCKED; captures as mode b0. See the B16c header above.
  mode baaf     B16c, case B-AAF: as bcrf with the DUT's CLOCK_SOURCE 2 (the peer's AAF stream).

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
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
E = os.environ
CTL, IFACE, STAGE = E["CTL_HOST"], E["CTL_IFACE"], E["CTL_STAGE"]
PEER_EID, PEER_MAC = E["PEER_EID"], E["PEER_MAC"]
DUT_EID = "020000fffe000001"


def _term(signum, frame):
    # run_b9.py's handler: a deadline's SIGTERM runs the teardown below rather than ending the process mid-case
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
name, raw_root, MODE = sys.argv[1], sys.argv[2], sys.argv[3]
assert MODE in ("loop", "dirb", "dirbloop", "looptap", "dira", "b0", "bcrf", "baaf"), MODE
FOL = MODE in ("bcrf", "baaf")
DUT_SRC = {"bcrf": 1, "baaf": 2}.get(MODE)
PEER_INTERNAL, PEER_CRF_FOUND = 0, 1
PEER_SETTLE_S = 5.0
LOCK_WAIT_S = 60.0
DIRA = MODE in ("dira", "b0", "bcrf", "baaf")
DIRB = MODE in ("dirb", "dirbloop", "dira", "b0", "bcrf", "baaf")
B0 = MODE == "b0"
TWO = MODE in ("b0", "bcrf", "baaf")
TAP_S_B0 = 40
B0_SETTLE_S = 20.0
STATE_NAMES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
RAWT, MONO_RAW = time.clock_gettime_ns, time.CLOCK_MONOTONIC_RAW
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
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / "agent-stderr.txt", "a"),
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


def counters(ag, tag, who_idx=(("dut", 0), ("peer", 0)) + ((("dut", 1),) if TWO else ())):
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
    if TWO:
        st["fmt-dut-in-1"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=1))
    return st


def dut_read(tag):
    """Lane B9's DUT console words (read-only commands; the caller holds the bench lock)."""
    r = subprocess.run(["python3", "-B", str(TOOLS / "console_read.py"), E["DUT_CONSOLE"], str(dest / f"dut-{tag}.txt"),
                        *DUT_READS], capture_output=True, text=True, timeout=90)
    event("dut-read", tag=tag, rc=r.returncode)


POLL_FILE = raw / "poll-run.jsonl"   # about 0.4 KB per poll: kept outside the packet (run_b9.py)
POLL_STOP = raw / "poll.stop"


class Poll:
    """B16c: run_b9.py's Poll, unchanged but for the console's name: the one console poll of the case
    (console_poll_b8.py), read back here as it grows."""

    def __init__(self, max_s):
        self.p = subprocess.Popen(["python3", "-B", str(TOOLS / "console_poll_b8.py"), E["DUT_CONSOLE"], str(POLL_FILE),
                                   str(max_s), "0.5", f"file:{POLL_STOP}"])
        event("poll-start", file=POLL_FILE.name, max_s=max_s, period_s=0.5)
        self.rows = []
        self.fh = None
        self.buf = ""

    def refresh(self):
        if self.fh is None:
            if not POLL_FILE.exists():
                return
            self.fh = open(POLL_FILE)
        self.buf += self.fh.read()
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1)
            if line.startswith("{"):
                self.rows.append(json.loads(line))

    def wait_state(self, state, since_raw, max_s, tag):
        """First poll that started after since_raw and reads `state`; the interval from the poll
        before it is the resolution. Returns seconds (lo, hi) after since_raw, or None."""
        end = time.monotonic() + max_s
        while time.monotonic() < end:
            self.refresh()
            prev = None
            for r in self.rows:
                if r["raw0"] < since_raw:
                    continue
                if r.get("servo_state") == state:
                    lo = (prev["raw1"] - since_raw) / 1e9 if prev else 0.0
                    hi = (r["raw1"] - since_raw) / 1e9
                    event("servo-state", tag=tag, state=STATE_NAMES[state], s_lo=round(lo, 3), s_hi=round(hi, 3), poll_n=r["n"])
                    return lo, hi
                prev = r
            if self.p.poll() is not None:
                break
            time.sleep(0.2)
        event("servo-state", tag=tag, state=STATE_NAMES[state], s_lo=None, s_hi=None, timeout_s=max_s)
        return None

    def stop(self):
        POLL_STOP.touch()
        try:
            self.p.wait(15)
        except subprocess.TimeoutExpired:
            self.p.kill()
            self.p.wait(5)
        self.refresh()
        event("poll-end", rc=self.p.returncode, polls=len(self.rows))

    def summary(self, spans):
        """B16c: per named span (start, end on CLOCK_MONOTONIC_RAW), the servo states read, the first and
        last of each polled word, and the polls whose read failed."""
        out = {}
        for tag, (a, b) in spans.items():
            rows = [r for r in self.rows if r["raw0"] >= a and (b is None or r["raw1"] <= b)]
            st = {}
            for r in rows:
                k = STATE_NAMES.get(r.get("servo_state"), str(r.get("servo_state")))
                st[k] = st.get(k, 0) + 1
            words = sorted({k for r in rows for k in (r.get("words") or {})})
            first = {k: next((r["words"].get(k) for r in rows if (r.get("words") or {}).get(k)), None) for k in words}
            last = {k: next((r["words"].get(k) for r in reversed(rows) if (r.get("words") or {}).get(k)), None) for k in words}
            distinct = {k: len({r["words"].get(k) for r in rows if (r.get("words") or {}).get(k)}) for k in words}
            out[tag] = dict(polls=len(rows), servo=st, first=first, last=last, distinct=distinct,
                            failed=sum(1 for r in rows if any(v is None for v in (r.get("words") or {}).values())))
        return out


class ToneMon(threading.Thread):
    """B16c: run_b9.py's ToneMon, unchanged: the tone source's playback substream status every 0.2 s (read
    from /proc, passive)."""

    def __init__(self):
        super().__init__(daemon=True)
        self.f = open(raw / "tone-status.jsonl", "w")
        self.stop = False
        self.last = None

    def read(self):
        try:
            txt = open(E["TONE_PROC"]).read()
        except OSError as e:
            return dict(error=repr(e))
        r = {}
        for line in txt.splitlines():
            k, _, v = line.partition(":")
            if k.strip() in ("state", "trigger_time", "hw_ptr"):
                r[k.strip()] = v.strip()
        if not r:
            r["state"] = txt.strip()
        return r

    def run(self):
        while not self.stop:
            r = self.read()
            r["mono_raw_ns"] = RAWT(MONO_RAW)
            self.last = r
            self.f.write(json.dumps(r) + "\n")
            time.sleep(0.2)
        self.f.close()


def tone_summary():
    """B16c: the tone monitor's file reduced: reads, states, distinct trigger times, hw_ptr monotonic."""
    rows = [json.loads(x) for x in open(raw / "tone-status.jsonl") if x.startswith("{")]
    st = {}
    for r in rows:
        st[r.get("state")] = st.get(r.get("state"), 0) + 1
    hp = [int(r["hw_ptr"]) for r in rows if str(r.get("hw_ptr", "")).isdigit()]
    return dict(reads=len(rows), states=st, trigger_times=len({r.get("trigger_time") for r in rows if r.get("trigger_time")}),
                hw_ptr_monotonic=all(b >= a for a, b in zip(hp, hp[1:])), hw_ptr_reads=len(hp),
                first_raw_ns=rows[0]["mono_raw_ns"] if rows else None, last_raw_ns=rows[-1]["mono_raw_ns"] if rows else None)


def setclk(ag, who, src, tag):
    """run_b9.py's setclk: SET_CLOCK_SOURCE on CLOCK_DOMAIN 0, then the GET_CLOCK_SOURCE read-back."""
    rows = ag.cmd(op="setclk", who=who, src=src)
    st = next((r.get("status") for r in rows if r.get("cmd") == "SET_CLOCK_SOURCE"), None)
    back = clk_of(rows, who)
    event("set-clock", tag=tag, who=who, src=src, status=st, readback=back, ok=back == src)
    return st, back


MARK_CTR = (("dut", 0x0024, 0), ("dut", 0x0005, 0), ("dut", 0x0005, 1), ("peer", 0x0005, 0), ("peer", 0x0024, 0))


def mark(ag, tag):
    """B16c: run_b9.py's window mark: GET_COUNTERS (read-only) and both entities' GET_CLOCK_SOURCE."""
    got = {}
    for who, dt, i in MARK_CTR:
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=i)
        r = rows[-1] if rows else {}
        w = ctr_words(r.get("payload"))
        got[f"{who}-{dt:#06x}-{i}"] = w[:13] if w else r.get("status")
    clk = {who: clk_of(ag.cmd(op="clk", who=who), who) for who in ("dut", "peer")}
    event("mark", tag=tag, mono_raw_ns=RAWT(MONO_RAW), counters=got, clock=clk)
    return clk


def music_check(tag):
    ok = mcasp_playback_closed()
    event("music-check", tag=tag, closed=ok)
    if not ok:
        raise SystemExit(f"WAIT: the SoC board's McASP playback is open before {tag} (the owner's music)")


ag = None
found = {}
sets = []
binds = []
procs = None
peer_unbound = None
tm = None
pl = None
clk_changed = []    # B16c: (who, as_found) in the order set
marks_raw = {}      # B16c: CLOCK_MONOTONIC_RAW ns of the case's steps, for the poll's spans
try:
    if not mcasp_playback_closed():
        raise SystemExit("WAIT: the SoC board's McASP playback is open (the owner's music); nothing changed")
    if FOL:
        # run_b9.py's check: the Direction B tone must be playing before anything changes
        tm = ToneMon()
        tm.start()
        time.sleep(1.2)
        tone0 = dict(tm.last or {})
        time.sleep(1.0)
        tone1 = dict(tm.last or {})
        playing = (tone0.get("state") == "RUNNING" and tone1.get("state") == "RUNNING"
                   and tone0.get("trigger_time") == tone1.get("trigger_time")
                   and tone0.get("hw_ptr") != tone1.get("hw_ptr"))
        event("tone-check", playing=playing, state=tone1.get("state"))
        if not playing:
            raise SystemExit("the Direction B tone is not playing: nothing changed")
    ag = Agent()
    found = state(ag)
    event("as-found", **found)
    if (found["rx-dut-0"] or {}).get("conn_count"):
        raise SystemExit("the DUT's STREAM_INPUT 0 is already bound: not this lane's as-found state, nothing changed")
    if DIRB and (found["map-dut-in"] or "")[:len(IDENT4)] != IDENT4:
        raise SystemExit("STOP: the DUT's STREAM_PORT_INPUT 0 does not hold the four identity mappings; this tool edits no map")
    if FOL:
        p8 = found["rx-peer-8"] or {}
        event("fol-check", clk_dut=found["clk-dut"], clk_peer=found["clk-peer"], peer_in_8=p8)
        if (found["rx-dut-1"] or {}).get("conn_count"):
            raise SystemExit("the DUT's STREAM_INPUT 1 is already bound: not this lane's as-found state, nothing changed")
        if found["clk-dut"] != 0:
            raise SystemExit("the DUT is not on INTERNAL as found; nothing changed")
        if (found["clk-peer"] != PEER_CRF_FOUND or p8.get("talker") != DUT_EID or str(p8.get("talker_uid")) != "1"
                or p8.get("conn_count") != 1):
            raise SystemExit("STOP: the peer is not on CLOCK_SOURCE 1 with its STREAM_INPUT 8 bound to the DUT's "
                             "STREAM_OUTPUT 1, as found; nothing changed")
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
    if FOL:
        dut_read("before-binds")
        pl = Poll(SECS + 240)
        time.sleep(2.0)
        marks_raw["poll-start"] = RAWT(MONO_RAW)
        mark(ag, "before-peer-set")
        music_check("the peer's clock-source set")
        # the ruling's exception: the peer's CLOCK_DOMAIN to INTERNAL, read back
        clk_changed.append(("peer", found["clk-peer"]))
        marks_raw["peer-set"] = RAWT(MONO_RAW)
        st, back = setclk(ag, "peer", PEER_INTERNAL, "peer-internal")
        if back != PEER_INTERNAL:
            raise SystemExit(f"STOP: the peer's clock-source set was refused or not read back ({st}, {back})")
        time.sleep(PEER_SETTLE_S)
        mark(ag, "after-peer-set")
        music_check("the binds")
    if B0:
        if (found["rx-dut-1"] or {}).get("conn_count"):
            raise SystemExit("the DUT's STREAM_INPUT 1 is already bound: not this lane's as-found state, nothing changed")
        if found["clk-dut"] != 0:
            raise SystemExit("B0 needs the DUT on INTERNAL as found; nothing changed")
        dut_read("before-binds")
    if TWO:
        bind_rule(ag, ("peer", 2), ("dut", 1), sets)
        binds.append((PEER_EID, 2, ("dut", 1)))
    if DIRB:
        bind_rule(ag, ("peer", 0), ("dut", 0), sets)
        binds.append((PEER_EID, 0, ("dut", 0)))
        t_last_bind = time.time()
        poll_listener(ag, "dut", 0, "after-dut-bind")
    if TWO:
        rx1 = rxs(ag.cmd(op="rx", who="dut", idx=1))
        rows = ag.cmd(op="counters", who="dut", dtype=5, idx=1)
        w = ctr_words((rows[-1] if rows else {}).get("payload"))
        event("listener-read", listener="dut-in-1", rx=rx1, media_locked=w[0] if w else None,
              media_unlocked=w[1] if w else None, frames_rx=w[11] if w else None)
        clk = clk_of(ag.cmd(op="clk", who="dut"), "dut")
        event("clock-read", who="dut", source=clk)
        if clk != 0:
            raise SystemExit("the DUT's clock source is not INTERNAL after the binds")
    if B0:
        time.sleep(max(0.0, B0_SETTLE_S - (time.time() - t_last_bind)))
    if FOL:
        music_check("the DUT's clock-source set")
        # lanes B9 and B10's case set, on the DUT as the listener, read back
        clk_changed.append(("dut", found["clk-dut"]))
        t_set = RAWT(MONO_RAW)
        t_set_mono = time.monotonic()
        marks_raw["dut-set"] = t_set
        st, back = setclk(ag, "dut", DUT_SRC, MODE)
        if back != DUT_SRC:
            raise SystemExit(f"the DUT's clock-source set was refused or not read back ({st}, {back})")
        lk = pl.wait_state(4, t_set, LOCK_WAIT_S, MODE)
        if lk is None:
            raise SystemExit("the DUT's media-clock servo did not read LOCKED within 60 s")
        while time.monotonic() < t_set_mono + B0_SETTLE_S:
            time.sleep(0.2)
        mark(ag, "window-mark-0")
    counters(ag, "before")
    procs = start_captures(mcasp=DIRB, procs=procs, tap_s=TAP_S_B0 if TWO else None)
    if FOL:
        off = RAWT(MONO_RAW) - time.time() * 1e9
        t_mc = procs["mcasp"][1] + 2.0      # the board plays 2 s before it records (mode dira)
        marks_raw["window-start"] = int(t_mc * 1e9 + off)
        marks_raw["window-end"] = int((t_mc + SECS) * 1e9 + off)
        for k, m in enumerate((SECS / 2, SECS - 15)):
            while time.time() < t_mc + m:
                time.sleep(0.2)
            mark(ag, f"window-mark-{k + 1}")
    wait_captures(procs)
    counters(ag, "after")
    if FOL:
        mark(ag, "after-captures")
    if B0:
        event("clock-read", who="dut", source=clk_of(ag.cmd(op="clk", who="dut"), "dut"))
        dut_read("after-captures")
    if MODE in ("loop", "dirbloop", "looptap"):
        poll_listener(ag, "peer", 0, "after-captures")
except BaseException as e:
    event("abort", error=repr(e))
    raise
finally:
    signal.signal(signal.SIGTERM, signal.SIG_IGN)   # B16c: a second deadline signal does not cut the restore short
    event("teardown")
    if ag is not None:
        # B16c: each restore step on its own, so one failure skips none of the others; a step that finds the
        # controller agent ended starts a new one and runs again (once). The DUT's clock source first, read back;
        # then the binds; then the peer's clock source, read back (no closed loop at any step)
        def step(a, stage, fn):
            for attempt in (1, 2):
                try:
                    if a.p.poll() is not None:
                        event("agent-restart", stage=stage, attempt=attempt)
                        a = Agent()
                    fn(a)
                    return a
                except BaseException as e:
                    event("teardown-error", stage=stage, attempt=attempt, error=repr(e))
                    try:
                        a.p.wait(timeout=3)     # an agent that ended is reaped here and restarted on the retry
                    except subprocess.TimeoutExpired:
                        return a                # alive: the error is not the agent's end; recorded, not retried
            return a

        for w, src0 in clk_changed:
            if w == "dut":
                ag = step(ag, "clock-dut", lambda a, s0=src0: setclk(a, "dut", s0, "restore"))

        def unbind_all(a):
            while binds:
                t_eid, tu, lis = binds[-1]
                unbind(a, t_eid, tu, lis, "teardown")
                binds.pop()
            time.sleep(1.0)

        ag = step(ag, "unbind", unbind_all)
        for w, src0 in clk_changed:
            if w == "peer":
                ag = step(ag, "clock-peer", lambda a, s0=src0: setclk(a, "peer", s0, "restore"))
        marks_raw["restored"] = RAWT(MONO_RAW)

        def rest(a):
            for lis, f0 in reversed(sets):
                s = a.cmd(op="setfmt", who=lis[0], idx=lis[1], fmt=f0)
                event("format-restore", listener=f"{lis[0]}-in-{lis[1]}", fmt=f0, status=[r.get("status") for r in s])
            if peer_unbound:
                t_eid, tu = peer_unbound["talker"], int(peer_unbound["talker_uid"])
                tf = fmt_of(a.cmd(op="fmt", who="dut" if t_eid == DUT_EID else "peer", dir="out", idx=tu))
                lf = fmt_of(a.cmd(op="fmt", who="peer", dir="in", idx=0))
                event("format-check", ok=tf == lf, talker=f"{t_eid}-out-{tu}", listener="peer-in-0", talker_fmt=tf,
                      listener_fmt=lf, set=None, note="the as-found bind, restored")
                rows = a.cmd(op="bind", t=t_eid, tu=tu, l=PEER_EID, lu=0)
                main = next((r for r in rows if r.get("what") == "bind"), {})
                after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
                event("rebind-as-found", status=main.get("status"), conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
                time.sleep(3.0)
            if FOL:
                time.sleep(3.0)
                mark(a, "after-restore")
            fin = state(a)
            norm = lambda d: {k: ({kk: vv for kk, vv in v.items() if kk != "flags"} if isinstance(v, dict) else v) for k, v in d.items()}
            diff = [k for k in fin if json.dumps(norm(fin)[k], sort_keys=True) != json.dumps(norm(found).get(k), sort_keys=True)]
            event("final", equal_to_found=not diff, differ=diff, **fin)

        ag = step(ag, "formats-final", rest)
        ag.quit()
    if pl is not None:
        try:
            time.sleep(3.0)
            pl.stop()
            pts = sorted(marks_raw.items(), key=lambda kv: kv[1])
            spans = {f"{a}..{b}": (ta, tb) for (a, ta), (b, tb) in zip(pts, pts[1:])}
            if pts:
                spans[f"{pts[-1][0]}..poll-end"] = (pts[-1][1], None)
            event("poll-summary", marks_raw=marks_raw, spans=pl.summary(spans))
        except BaseException as e:
            event("poll-error", error=repr(e))
        try:
            dut_read("final")
        except BaseException as e:
            event("dut-read-error", error=repr(e))
    if tm is not None:
        try:
            tm.stop = True
            time.sleep(0.5)
            event("tone-summary", **tone_summary())
        except BaseException as e:
            event("tone-summary-error", error=repr(e))
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
