#!/usr/bin/env python3
"""Lane B14 item 2 (#645 acceptance 3, #647 bench item): the source-switch repeat, lane B8's method.

usage: sw_b14.py setup    <name>
       sw_b14.py cycles   <name> <first> <count> <hold_aaf_s> <hold_crf_s> <hold_int_s>
       sw_b14.py teardown <name>
The caller holds the bench lock for the whole invocation (run_locked_b14.sh).

Lane B8's run_b8.py case SW, reduced to what this lane may touch. Kept from B8: the controller
agent (b8_ctl.py on the controller host, beside avdecc_ro.py), the binding rule (read both
formats; if they differ set the LISTENER's to the talker's and read it back; STOP if it does not
take it), B8's three binds (the DUT's AAF talker to the peer's STREAM_INPUT 0, the peer's CRF
talker to the DUT's STREAM_INPUT 1, the peer's AAF talker to the DUT's STREAM_INPUT 0), B8's
identity mappings on the DUT's STREAM_PORT_OUTPUT 0 where the as-found map lacks them, one
console poll every 0.5 s (console_poll_b8.py: servo, AAF meter, SLIP_LB, SLIP_TDM, RENDER_STAT,
CRF lock and rate) through every switch, GET_COUNTERS and GET_CLOCK_SOURCE marks per phase, and
the restore with read-back. Dropped: the SoC board (no tone, no McASP0 sampler; ruling
6094000332), the external capture (no tone in this lane). Added: the tap around each switch
(a capture from 3 s before the set to 17 s after it, copied back and removed from the tap host)
and the cycle structure the assignment asks for: per cycle INTERNAL->AAF (hold), AAF->CRF
(hold), CRF->INTERNAL (hold), so ten cycles give ten INTERNAL->AAF and ten AAF->CRF switches.
The binds stay in the devices between `cycles` invocations; `teardown` restores everything.

As found on this image the peer's STREAM_INPUT 0 already holds B8's first bind (the DUT's AAF
talker) and the peer's clock domain follows an input stream (the DUT's CRF on its STREAM_INPUT
8). The bind is kept and never unbound here. B8 ran with the peer's clock domain at INTERNAL; a
DUT following the peer while the peer follows the DUT would be a clock loop, so `setup` sets the
peer's CLOCK_SOURCE to 0 (read back) and `teardown` restores the as-found source (read back).

Environment (private): DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, TAP_HOST, TAP_IFACE.
"""
import hashlib
import json
import os
import shlex
import signal
import struct
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
DUT = os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
TAP, TAP_IF = os.environ["TAP_HOST"], os.environ["TAP_IFACE"]
DUT_EID = "020000fffe000001"
RAW = Path("/tmp/608-b14/raw/item2")
STATE = RAW / "state.json"
CTL_DIR = "/tmp/608-b14"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]
# the bench brief's filter, extended by the VLAN-tagged AVTP the streams use
TAP_FILTER = "ether[40:2]=0x22f0 or (ether[40:2]=0x8100 and ether[44:2]=0x22f0)"
CAP_PRE_S, CAP_S = 3.0, 20
DUT_READS = ["milan_status", "milan_nvm", "mem_read 0x90000738 4", "mem_read 0x90000748 8", "mem_read 0x900008d4 12",
             "mem_read 0x900008f8 8", "mem_read 0x900008e0 8", "mem_read 0x90000660 20", "mem_read 0x90000694 8",
             "mem_read 0x900006cc 12"]
RAWT, MONO_RAW = time.clock_gettime_ns, time.CLOCK_MONOTONIC_RAW
STATES = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
EID = {"dut": DUT_EID, "peer": PEER_EID}
# GET_COUNTERS at every mark: B8's six, plus the DUT's AVB_INTERFACE and the peer's two talkers
CTR = [("dut", 0x0024, 0), ("dut", 0x0006, 0), ("dut", 0x0006, 1), ("peer", 0x0005, 0),
       ("dut", 0x0005, 0), ("dut", 0x0005, 1), ("dut", 0x0009, 0), ("peer", 0x0006, 0), ("peer", 0x0006, 2)]
BINDS = [(("dut", 0), ("peer", 0), "dut-aaf"), (("peer", 2), ("dut", 1), "peer-crf"), (("peer", 0), ("dut", 0), "peer-aaf")]
B8_MAPS = [(0, c, c, 0) for c in range(8)]


def _term(signum, frame):
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
mode, name = sys.argv[1], sys.argv[2]
assert mode in ("setup", "cycles", "teardown"), mode
raw = RAW / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "item2" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), mono_raw_ns=RAWT(MONO_RAW), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(args, timeout=limit + 5, **kw)


def dut(tag):
    r = run(["python3", "-B", str(TOOLS / "console_read.py"), DUT, str(dest / f"dut-{tag}.txt"), *DUT_READS], 90,
            capture_output=True, text=True)
    event("dut", tag=tag, rc=r.returncode)


class Poll:
    """B8's one console poll of an invocation, read back as it grows."""

    def __init__(self, max_s):
        self.file, self.stopf = raw / "poll.jsonl", raw / "poll.stop"
        self.p = subprocess.Popen(["python3", "-B", str(TOOLS / "console_poll_b8.py"), DUT, str(self.file),
                                   str(max_s), "0.5", f"file:{self.stopf}"])
        event("poll-start", max_s=max_s, period_s=0.5)
        self.rows, self.fh, self.buf = [], None, ""

    def refresh(self):
        if self.fh is None:
            if not self.file.exists():
                return
            self.fh = open(self.file)
        self.buf += self.fh.read()
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1)
            if line.startswith("{"):
                self.rows.append(json.loads(line))

    def wait_state(self, state, since_raw, max_s, tag):
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
                    event("servo-state", tag=tag, state=STATES[state], s_lo=round(lo, 3), s_hi=round(hi, 3), poll_n=r["n"])
                    return lo, hi
                prev = r
            if self.p.poll() is not None:
                break
            time.sleep(0.2)
        event("servo-state", tag=tag, state=STATES[state], s_lo=None, s_hi=None, timeout_s=max_s)
        return None

    def stop(self):
        self.stopf.touch()
        try:
            self.p.wait(15)
        except subprocess.TimeoutExpired:
            self.p.kill()
            self.p.wait(5)
        self.refresh()
        event("poll-end", rc=self.p.returncode, polls=len(self.rows))


class Agent:
    def __init__(self, life_s):
        self.p = subprocess.Popen(
            SSH + [CTL, f"cd {CTL_DIR} && sudo -n timeout {life_s} python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(raw / "agent-stderr.txt", "w"), text=True, bufsize=1)
        self.log = open(raw / "ctl.jsonl", "a", buffering=1)
        self.n = 0
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

    def sync(self, k=3):
        best = None
        for _ in range(k):
            self.n += 1
            t0 = time.time()
            self.p.stdin.write(json.dumps(dict(op="sync", n=self.n)) + "\n")
            self.p.stdin.flush()
            line = json.loads(self.readline())
            t1 = time.time()
            assert line.get("type") == "sync" and line.get("n") == self.n, line
            s = dict(n=self.n, rtt_ms=round((t1 - t0) * 1e3, 3), offset_ms=round((line["rt"] - (t0 + t1) / 2) * 1e3, 3))
            if best is None or s["rtt_ms"] < best["rtt_ms"]:
                best = s
        event("sync", **best)

    def quit(self):
        try:
            self.p.stdin.write(json.dumps(dict(op="quit")) + "\n")
            self.p.stdin.flush()
            self.p.wait(15)
        except Exception:
            self.p.terminate()
            self.p.wait(10)
        event("agent-exit", rc=self.p.returncode)


class Capture:
    """One tap capture of fixed length on the tap host, the brief's command form."""

    def __init__(self, label):
        self.name = f"608-b14-{label}.pcap"
        self.path = "/tmp/" + self.name
        cmd = shlex.join(["sudo", "-n", "timeout", str(CAP_S), "tcpdump", "-i", TAP_IF, "-s", "256", "-U", "-w",
                          self.path, TAP_FILTER])
        self.p = subprocess.Popen(["timeout", "-k", "3", str(CAP_S + 20)] + SSH + [TAP, cmd + " 2>&1"],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.buf = b""
        end = time.monotonic() + 12
        while time.monotonic() < end:
            b = self.p.stdout.read1(4096) if hasattr(self.p.stdout, "read1") else os.read(self.p.stdout.fileno(), 4096)
            if not b:
                break
            self.buf += b
            if b"listening on" in self.buf:
                break
        self.ok = b"listening on" in self.buf
        event("capture-start", file=self.name, ok=self.ok, seconds=CAP_S)
        if not self.ok:
            raise SystemExit("tap capture did not start")

    def finish(self):
        out, _ = self.p.communicate(timeout=CAP_S + 25)
        self.buf += out or b""
        summary = [s for s in self.buf.decode(errors="replace").splitlines() if "packet" in s]
        h = None
        try:
            remote = run(SSH + [TAP, f"sha256sum {self.path}; stat -c %s {self.path}"], 30, capture_output=True, text=True)
            rh, rsize = remote.stdout.split()[0], int(remote.stdout.split()[-1])
            local = RAW / "pcap" / self.name
            local.parent.mkdir(exist_ok=True)
            run(["scp", "-q", "-o", "BatchMode=yes", f"{TAP}:{self.path}", str(local)], 120)
            hsh = hashlib.sha256()
            with open(local, "rb") as f:
                for blk in iter(lambda: f.read(1 << 22), b""):
                    hsh.update(blk)
            h = hsh.hexdigest()
            if h == rh:
                run(SSH + [TAP, f"sudo -n rm -- {self.path}"], 20)
            event("capture-end", file=self.name, rc=self.p.returncode, summary=summary, bytes=rsize, sha256=h,
                  remote_equal=h == rh, removed_from_tap=h == rh)
        except Exception as e:
            event("capture-end", file=self.name, rc=self.p.returncode, summary=summary, error=repr(e))


def fmt_of(rows):
    for r in rows:
        if r.get("status") == "SUCCESS" and r.get("cmd") in ("GET_STREAM_FORMAT", "SET_STREAM_FORMAT"):
            return r["payload"][8:24]
    return None


def clk_of(rows, what):
    for r in rows:
        if r.get("what") == what and r.get("status") == "SUCCESS":
            return int(r["payload"][8:12], 16)
    return None


def map_of(rows):
    """GET_AUDIO_MAP response: (payload hex, [(stream_index, stream_channel, cluster_offset, cluster_channel)])."""
    for r in rows:
        if r.get("cmd") == "GET_AUDIO_MAP" and r.get("status") == "SUCCESS":
            b = bytes.fromhex(r["payload"])
            n = struct.unpack(">H", b[8:10])[0]
            return r["payload"], [struct.unpack(">4H", b[12 + 8 * k:20 + 8 * k]) for k in range(n)]
    return None, None


def binding_rule(ag, talker, listener, tag, st):
    (tw, ti), (lw, li) = talker, listener
    t = fmt_of(ag.cmd(op="fmt", who=tw, dir="out", idx=ti))
    l0 = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
    rec = dict(tag=tag, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", talker_fmt=t, listener_fmt=l0, set=None,
               listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        if not any(w == lw and i == li for w, i, _ in st["fmt_set"]):
            st["fmt_set"].append([lw, li, l0])
            save(st)
        s = ag.cmd(op="setfmt", who=lw, idx=li, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s])
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)


def acmp(ag, op, talker, listener):
    (tw, ti), (lw, li) = talker, listener
    rows = ag.cmd(op=op, t=EID[tw], tu=ti, l=EID[lw], lu=li)
    main = next((r for r in rows if r.get("what") == op), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event(op, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", status=main.get("status"),
          conn_count=after.get("conn_count"), flags=after.get("flags"))
    return main.get("status") == 0


def setclk(ag, src, tag):
    rows = ag.cmd(op="setclk", who="dut", src=src)
    st = next((r.get("status") for r in rows if r.get("cmd") == "SET_CLOCK_SOURCE"), None)
    back = clk_of(rows, "clock-dut")
    event("set-clock", tag=tag, src=src, status=st, readback=back, ok=back == src)
    return back


def counters(ag, tag):
    got = {}
    for who, dt, i in CTR:
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=i)
        r = rows[0] if rows else {}
        got[f"{who}-{dt:#06x}-{i}"] = r.get("payload") if r.get("status") == "SUCCESS" else r.get("status")
    event("counters", tag=tag, payloads=got)


def clock_read(ag, tag):
    src = clk_of(ag.cmd(op="clk", who="dut"), "clock-dut")
    event("clock-read", tag=tag, source=src)
    return src


def rx_row(ag, who, i):
    rows = ag.cmd(op="rx", who=who, idx=i)
    r = rows[0] if rows else {}
    t = r.get("talker")
    return dict(conn_count=r.get("conn_count"), talker={DUT_EID: "dut", PEER_EID: "peer"}.get(t, t),
                talker_uid=r.get("talker_uid"), flags=r.get("flags"))


def rx_count(ag, who, i):
    return rx_row(ag, who, i)["conn_count"]


def setclk_who(ag, who, src, tag):
    rows = ag.cmd(op="setclk", who=who, src=src)
    st = next((r.get("status") for r in rows if r.get("cmd") == "SET_CLOCK_SOURCE"), None)
    back = clk_of(rows, f"clock-{who}")
    event("set-clock", tag=tag, who=who, src=src, status=st, readback=back, ok=back == src)
    return back


def save(st):
    STATE.write_text(json.dumps(st, indent=1) + "\n")


def sleep_until(t):
    while time.monotonic() < t:
        time.sleep(0.1)


event("start", mode=mode, argv=sys.argv[1:])
ag = pl = None
try:
    if mode == "setup":
        assert not STATE.exists(), "a setup is already recorded"
        dut("before")
        ag = Agent(400)
        ag.sync(5)
        found = {}
        for who, d, i in (("peer", "in", 0), ("dut", "in", 0), ("dut", "in", 1), ("dut", "out", 0), ("dut", "out", 1),
                          ("peer", "out", 0), ("peer", "out", 2)):
            found[f"fmt-{who}-{d}-{i}"] = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=i))
        for who in ("peer", "dut"):
            found[f"clk-{who}"] = clk_of(ag.cmd(op="clk", who=who), f"clock-{who}")
        for who, i in (("peer", 0), ("peer", 8), ("dut", 0), ("dut", 1)):
            found[f"rx-{who}-{i}"] = rx_row(ag, who, i)
        for who, i in (("dut", 0), ("dut", 1), ("peer", 0), ("peer", 2)):
            ag.cmd(op="tx", who=who, idx=i)
        for dt in (0x000E, 0x000F):
            found[f"map-dut-{dt:#06x}-0"] = map_of(ag.cmd(op="map", act="get", dtype=dt, didx=0))
        event("as-found", **found)
        counters(ag, "as-found")
        if any(found[f"rx-dut-{i}"]["conn_count"] for i in (0, 1)):
            raise SystemExit("a DUT listener this item uses is already bound: nothing changed")
        p0 = found["rx-peer-0"]
        kept = []
        if p0["conn_count"]:
            # B8's first bind (the DUT's AAF talker to the peer's STREAM_INPUT 0) found in place: kept, not re-bound
            if (p0["talker"], p0["talker_uid"]) != ("dut", 0):
                raise SystemExit("the peer's STREAM_INPUT 0 is bound to another talker: nothing changed")
            kept.append("dut-aaf")
        if found["clk-dut"] != 0:
            raise SystemExit(f"the DUT's clock source is {found['clk-dut']}, not INTERNAL: nothing changed")
        st = dict(found=found, fmt_set=[], binds=[], kept=kept, map_added=[], clk_peer_set=False, setup_name=name)
        save(st)
        if found["clk-peer"] != 0:
            # B8's method runs with the peer's clock domain at INTERNAL; as found it follows an input stream
            # (the DUT's own CRF), which with the DUT following the peer would close a clock loop. Restored at teardown.
            st["clk_peer_set"] = True
            save(st)
            if setclk_who(ag, "peer", 0, "peer-internal") != 0:
                raise SystemExit("the peer's clock source did not read back INTERNAL")
        _, cur = found["map-dut-0x000f-0"]
        cur = [tuple(m) for m in (cur or [])]
        missing = [m for m in B8_MAPS if m not in cur]
        if missing and len(missing) != len(B8_MAPS):
            raise SystemExit(f"STREAM_PORT_OUTPUT 0 holds part of B8's mappings ({len(B8_MAPS) - len(missing)} of 8): decision needed")
        if missing:
            rows = ag.cmd(op="map", act="add", dtype=0x000F, didx=0, n=8)
            payload, after = map_of(rows)
            st["map_added"] = [list(m) for m in missing]
            save(st)
            event("map-add", status=[r.get("status") for r in rows], readback=payload)
        else:
            event("map-add", skipped="the as-found map already holds B8's mappings")
        for talker, listener, tag in BINDS:
            if tag in kept:
                event("bind-kept", tag=tag, talker=f"{talker[0]}-out-{talker[1]}", listener=f"{listener[0]}-in-{listener[1]}")
                continue
            binding_rule(ag, talker, listener, tag, st)
            ok = acmp(ag, "bind", talker, listener)
            if not ok:
                raise SystemExit(f"{tag} bind failed")
            st["binds"].append([list(talker), list(listener), tag])
            save(st)
            time.sleep(1.0)
        time.sleep(5.0)
        counters(ag, "after-binds")
        clock_read(ag, "after-binds")
    elif mode == "cycles":
        first, count = int(sys.argv[3]), int(sys.argv[4])
        holds = dict(aaf=float(sys.argv[5]), crf=float(sys.argv[6]), int=float(sys.argv[7]))
        st = json.loads(STATE.read_text())
        assert len(st["binds"]) + len(st["kept"]) == len(BINDS), "binds not in place"
        budget = count * (holds["aaf"] + holds["crf"] + holds["int"] + 60) + 60
        ag = Agent(int(budget + 120))
        ag.sync(3)
        for (tw, ti), (lw, li), tag in st["binds"]:
            n = rx_count(ag, lw, li)
            event("rx-check", listener=f"{lw}-in-{li}", conn_count=n)
            if not n:
                raise SystemExit(f"bind {tag} not in place")
        n = rx_count(ag, "peer", 0)
        event("rx-check", listener="peer-in-0", conn_count=n)
        if not n:
            raise SystemExit("the DUT's AAF talker is not bound to the peer")
        src0 = clock_read(ag, "invocation-start")
        if src0 != 0:
            raise SystemExit(f"the DUT's clock source is {src0}, not INTERNAL, at the start of a cycle")
        if clk_of(ag.cmd(op="clk", who="peer"), "clock-peer") != 0:
            raise SystemExit("the peer's clock source is not INTERNAL at the start of a cycle")
        pl = Poll(budget + 60)
        time.sleep(2.0)
        for k in range(first, first + count):
            for ph, src in (("aaf", 2), ("crf", 1), ("int", 0)):
                tag = f"c{k:02d}-{ph}"
                counters(ag, f"{tag}-before")
                clock_read(ag, f"{tag}-before")
                cap = Capture(f"sw-{tag}") if ph != "int" else None
                if cap:
                    time.sleep(CAP_PRE_S)
                ag.sync(3)
                event("switch", tag=tag, src=src)
                t_set, t_set_m = RAWT(MONO_RAW), time.monotonic()
                if src == 2:
                    st.setdefault("clk_changed", True)
                    save(st)
                back = setclk(ag, src, tag)
                if back != src:
                    raise SystemExit(f"clock source set refused or not read back ({back})")
                if src:
                    lk = pl.wait_state(4, t_set, 60.0, tag)
                    if lk is None:
                        raise SystemExit(f"{tag}: the servo did not read LOCKED within 60 s")
                    t0 = time.monotonic()
                    counters(ag, f"{tag}-locked")
                    clock_read(ag, f"{tag}-locked")
                    sleep_until(t0 + 8.0)
                    counters(ag, f"{tag}-settled")
                else:
                    pl.wait_state(0, t_set, 10.0, tag)
                    t0 = time.monotonic()
                if cap:
                    cap.finish()
                sleep_until(t0 + holds[ph] / 2)
                counters(ag, f"{tag}-mid")
                sleep_until(t0 + holds[ph] - 2.0)
                counters(ag, f"{tag}-end")
                clock_read(ag, f"{tag}-end")
                sleep_until(t0 + holds[ph])
                event("phase-end", tag=tag, set_to_end_s=round(time.monotonic() - t_set_m, 3))
            event("cycle-end", cycle=k)
    else:
        st = json.loads(STATE.read_text())
        found = st["found"]
        ag = Agent(300)
        ag.sync(3)
        counters(ag, "teardown-start")
        if clock_read(ag, "teardown-start") != found["clk-dut"]:
            setclk(ag, found["clk-dut"], "restore")
        for talker, listener, tag in reversed(st["binds"]):
            acmp(ag, "unbind", tuple(talker), tuple(listener))
        time.sleep(2.0)
        if st.get("clk_peer_set"):
            setclk_who(ag, "peer", found["clk-peer"], "peer-restore")
        for who in ("peer", "dut"):
            event("clock-final", who=who, source=clk_of(ag.cmd(op="clk", who=who), f"clock-{who}"),
                  as_found=found[f"clk-{who}"])
        for who, i, f in st["fmt_set"]:
            s = ag.cmd(op="setfmt", who=who, idx=i, fmt=f)
            event("format-restore", who=who, idx=i, fmt=f, status=[r.get("status") for r in s])
        final = {}
        for key in [k for k in found if k.startswith("fmt-")]:
            _, who, d, i = key.split("-")
            final[key] = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=int(i)))
        if st["map_added"]:
            rows = ag.cmd(op="map", act="remove", dtype=0x000F, didx=0, n=8)
            event("map-remove", status=[r.get("status") for r in rows])
        for dt in (0x000E, 0x000F):
            final[f"map-dut-{dt:#06x}-0"] = map_of(ag.cmd(op="map", act="get", dtype=dt, didx=0))
        for who, i in (("peer", 0), ("peer", 8), ("dut", 0), ("dut", 1)):
            final[f"rx-{who}-{i}"] = rx_row(ag, who, i)
        for who in ("peer", "dut"):
            final[f"clk-{who}"] = clk_of(ag.cmd(op="clk", who=who), f"clock-{who}")
        for who, i in (("dut", 0), ("dut", 1), ("peer", 0), ("peer", 2)):
            ag.cmd(op="tx", who=who, idx=i)
        cmp = {k: dict(as_found=found.get(k), final=v, equal=json.dumps(v) == json.dumps(found.get(k))) for k, v in final.items()}
        event("restore-compare", rows=cmp, all_equal=all(v["equal"] for v in cmp.values()))
        counters(ag, "final")
        st["torn_down"] = True
        save(st)
        STATE.rename(RAW / f"state-{name}.json")
finally:
    if pl is not None:
        time.sleep(1.0)
        pl.stop()
    if ag is not None:
        ag.quit()
    if mode == "teardown":
        dut("after")
    for f in sorted(raw.rglob("*")):
        if f.is_file():
            event("raw-file", file=str(f.relative_to(raw)), bytes=f.stat().st_size,
                  sha256=hashlib.sha256(f.read_bytes()).hexdigest())
    event("end")
