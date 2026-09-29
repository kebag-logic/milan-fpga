"""One locked foreground capture and controller action for lane B2, with joined children.

Derived from the #75 runner (action.py in the PR #604 packet). The caller holds
the bench lock for the whole action; every child has an explicit deadline and
is joined before return. Only the DUT-talker pair is used: DUT Stream Output 1
(stream 0200000000010001) to the reference peer's Stream Input 8.

modes:
  bind    fresh first bind (#606). Pre-capture at least PRE_BIND s and until a
          DUT MSRP LeaveAll has crossed the tap, refuse if the DUT declared the
          target Talker Advertise meanwhile, then CONNECT_RX and time the
          response to the first valid CRF PDU (30 s cap, then 3 s more).
  unbind  DISCONNECT_RX, then capture until the DUT withdraws the target
          Talker Advertise (Lv) and SETTLE s more (40 s cap).
  observe the bind pre-window only, with no controller transaction.
  cycle   #608/#75 cycle: 3 s pre-capture, stream must be flowing, then
          DISCONNECT_RX, 2 s, CONNECT_RX, first valid PDU (30 s cap), 3 s more.

usage: b2_action.py <name> <mode> <console> <controller> <ctl_if> <tap_host> <tap_if>
Raw captures go to /tmp/b2-a440/raw/<name>/tap.pcap, never into the packet.
"""
import hashlib, json, os, shlex, signal, struct, subprocess, sys, threading, time
from pathlib import Path

name, mode, port, controller, ctl_if, tap, tap_if = sys.argv[1:8]
assert mode in ("bind", "unbind", "cycle", "observe")
PRE_BIND, SETTLE = 16.0, 10.0
packet = Path(__file__).resolve().parent.parent
root = Path("/tmp/b2-a440/raw") / name
root.mkdir(parents=True, exist_ok=False)
dest = packet / ("bind" if mode in ("bind", "unbind", "observe") else "cycles") / name
dest.mkdir(parents=True, exist_ok=False)
SID = "0200000000010001"
WIREPORT = 3  # frames the DUT sent
events, wire, msrp_events, errors = [], [], [], []
first = None
capture = None
stopping = False
EV = ["New", "JoinIn", "In", "JoinMt", "Mt", "Lv"]
TYPES = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
ALEN = {1: 25, 2: 34, 3: 8, 4: 4}
CONSOLE = ["milan_status", "mem_read 0x90000930 4", "mem_read 0x90000720 4",
           "mem_read 0x90000750 4", "mem_read 0x90000764 4", "mem_read 0x90000774 4",
           "mem_read 0x90000110 4"]


def event(kind, **kw):
    r = dict(t=time.time(), kind=kind, **kw)
    events.append(r)
    with (dest / "events.jsonl").open("a") as f:
        f.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(["timeout", str(limit) + "s", *args], timeout=limit + 2, **kw)


def sshargs(host, args):
    return ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", host, shlex.join(args)]


def controller_action(which, limit=15):
    r = run(sshargs(controller, ["sudo", "-n", "timeout", str(limit - 3) + "s", "python3", "-B",
                                 "/tmp/b2a440_reconnect.py", ctl_if, which, "talker"]),
            limit, capture_output=True, text=True)
    (dest / (which + ".jsonl")).write_text(r.stdout)
    (dest / (which + "-errors.txt")).write_text(r.stderr.replace(controller, "<controller-host>"))
    event("controller", action=which, rc=r.returncode)
    assert r.returncode == 0, "controller action failed: " + which
    return [json.loads(s) for s in r.stdout.splitlines()]


def console(which):
    r = run(["python3", "-B", str(packet / "tools/console_read.py"), port,
             str(dest / ("console-" + which + ".txt")), *CONSOLE], 10, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    text = (dest / ("console-" + which + ".txt")).read_text()
    assert "SYNC=1 ASCAPABLE=1 TU=0" in text, "DUT health changed"


def read_exact(stream, n):
    b = bytearray()
    while len(b) < n:
        v = stream.read(n - len(b))
        if not v:
            break
        b.extend(v)
    return bytes(b)


def msrp(p, ns, sender):
    """Decode one MSRPDU into events; raises on a malformed PDU."""
    assert p and p[0] == 0, "MSRP version"
    o = 1
    while o + 2 <= len(p) and p[o:o + 2] != bytes(2):
        typ, alen = p[o:o + 2]
        length = int.from_bytes(p[o + 2:o + 4], "big")
        o += 4
        end = o + length
        assert typ in TYPES and alen == ALEN[typ] and end <= len(p), "message shape"
        while o + 2 <= end and p[o:o + 2] != bytes(2):
            h = int.from_bytes(p[o:o + 2], "big")
            o += 2
            n, la = h & 8191, h >> 13
            fv = p[o:o + alen]
            o += alen
            ne, nf = (n + 2) // 3, ((n + 3) // 4 if typ == 3 else 0)
            ep, fp = p[o:o + ne], p[o + ne:o + ne + nf]
            o += ne + nf
            if la:
                msrp_events.append(dict(ns=ns, sender=sender, type=TYPES[typ], event="LeaveAll", sid=None, listener=None))
            for k in range(n):
                ev = (ep[k // 3] // (36, 6, 1)[k % 3]) % 6
                sid = (fv[:6] + ((int.from_bytes(fv[6:8], "big") + k) & 65535).to_bytes(2, "big")).hex() if typ in (1, 2, 3) else None
                lv = (fp[k // 4] // (64, 16, 4, 1)[k % 4]) % 4 if typ == 3 else None
                msrp_events.append(dict(ns=ns, sender=sender, type=TYPES[typ], event=EV[ev], sid=sid, listener=lv))
        assert o + 2 == end and p[o:o + 2] == bytes(2), "attribute endmark"
        o = end


def reader():
    global first
    try:
        with (root / "tap.pcap").open("wb") as out:
            head = read_exact(capture.stdout, 24)
            out.write(head)
            out.flush()
            assert len(head) == 24 and head[:4] in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"), "bad pcap header"
            nano = head[:4] == b"\x4d\x3c\xb2\xa1"
            while True:
                h = read_exact(capture.stdout, 16)
                if not h:
                    break
                assert len(h) == 16, "truncated record"
                sec, frac, n, _orig = struct.unpack("<4I", h)
                pkt = read_exact(capture.stdout, n)
                assert len(pkt) == n, "truncated frame"
                out.write(h + pkt)
                out.flush()
                if len(pkt) < 42:
                    continue
                tag, _, wp = struct.unpack("<3I", pkt[:12])
                if tag != 6 or wp not in (2, 3):
                    continue
                host = sec * 10**9 + frac * (1 if nano else 1000)
                lo = struct.unpack("<I", pkt[16:20])[0]
                if first is None:
                    first = (host, lo)
                ns = lo - first[1] + round(((host - first[0]) - (lo - first[1])) / (1 << 32)) * (1 << 32)
                fr = pkt[28:]
                et = int.from_bytes(fr[12:14], "big")
                o, vlan = 14, None
                if et == 0x8100:
                    tci = int.from_bytes(fr[14:16], "big")
                    vlan = (tci >> 13, tci & 4095)
                    et = int.from_bytes(fr[16:18], "big")
                    o = 18
                pl = fr[o:]
                r = dict(ns=ns, port=wp, et=et, seen=time.monotonic())
                if et == 0x22EA:
                    try:
                        msrp(pl, ns, "DUT" if wp == 3 else "bridge")
                    except (AssertionError, IndexError) as e:
                        errors.append("msrp decode: " + str(e))
                if et == 0x22F0 and len(pl) >= 12:
                    r["sub"] = pl[0]
                    if pl[0] == 0xFC and len(pl) >= 56:
                        r.update(mt=pl[1] & 15, status=pl[2] >> 3, seq=int.from_bytes(pl[48:50], "big"),
                                 controller=pl[12:20].hex())
                    if pl[0] == 4:
                        r.update(sid=pl[4:12].hex(), valid=(len(pl) >= 28 and pl[1] & 0xF0 == 0x80 and pl[3] == 1
                                                            and int.from_bytes(pl[12:16], "big") == 48000
                                                            and pl[16:20] == bytes.fromhex("00080060") and vlan == (3, 2)))
                wire.append(r)
    except Exception as e:
        errors.append(str(e))


def stop_capture():
    if capture is None:
        return
    if capture.poll() is None:
        try:
            capture.stdin.write(b"stop\n")
            capture.stdin.flush()
        except BrokenPipeError:
            pass
    capture.wait(timeout=10)
    thread.join(timeout=5)
    assert not thread.is_alive(), "capture reader did not exit"
    capture.stdin.close()
    capture.stdout.close()


def signal_stop(signum, frame):
    global stopping
    stopping = True


def wait(seconds, until=None):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        assert not errors, errors
        if stopping:
            raise RuntimeError("interrupted")
        if until is not None and until():
            return True
        time.sleep(0.05)
    return False


def target_ta_declared(since_ns):
    return any(e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID
               and e["event"] in ("New", "JoinIn", "JoinMt") and e["ns"] >= since_ns for e in msrp_events)


signal.signal(signal.SIGTERM, signal_stop)
signal.signal(signal.SIGINT, signal_stop)
result = dict(name=name, mode=mode, stream_id=SID, status="INCOMPLETE")
cap_seconds = {"bind": 70, "unbind": 50, "cycle": 45, "observe": 40}[mode]
try:
    console("before")
    controller_action("snapshot")
    (dest / "snapshot-before.jsonl").write_text((dest / "snapshot.jsonl").read_text())
    err = (dest / "capture.txt").open("wb")
    args = sshargs(tap, ["sudo", "-n", "timeout", "-k", "3s", str(cap_seconds + 5) + "s", "python3", "-B",
                         "/tmp/b2a440_capture.py", tap_if, str(cap_seconds)])
    capture = subprocess.Popen(["timeout", "-k", "3s", str(cap_seconds + 9) + "s", *args],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err)
    thread = threading.Thread(target=reader)
    thread.start()
    wait(3)
    assert wire, "no tapped frames"
    t_start = wire[0]["ns"]
    if mode in ("bind", "observe"):
        # Fresh state: at least PRE_BIND s of tap, including one DUT MSRP LeaveAll
        # (after which a declaring applicant re-declares), and no target TA declaration.
        dut_la = lambda: any(e["sender"] == "DUT" and e["event"] == "LeaveAll" for e in msrp_events)
        wait(PRE_BIND + 2, until=lambda: (wire[-1]["ns"] - t_start) / 1e9 >= PRE_BIND)
        wait(12, until=dut_la)
        result["pre_window_s"] = (wire[-1]["ns"] - t_start) / 1e9
        result["pre_window_dut_leaveall"] = dut_la()
        result["pre_window_dut_msrp_events"] = sum(e["sender"] == "DUT" for e in msrp_events)
        result["pre_window_target_ta_declared"] = target_ta_declared(t_start)
        if result["pre_window_target_ta_declared"] or not result["pre_window_dut_leaveall"]:
            result["status"] = "NOT_FRESH"
            raise RuntimeError("fresh-state check failed; no bind issued")
    if mode == "observe":
        result["status"] = "OBSERVED"
    if mode == "cycle":
        assert any(r.get("valid") and r.get("sid") == SID and r["port"] == WIREPORT
                   and time.monotonic() - r["seen"] < 1 for r in wire), "stream not flowing before cycle"
    rows = controller_action(mode) if mode != "observe" else []
    if mode == "observe":
        pass
    elif mode in ("bind", "cycle"):
        tx = next(r for r in rows if r.get("kind") == "transaction" and r["mt"] == 6)
        seq = tx["seq"]
        result["seq"] = seq
        ackf = lambda: next((r for r in wire if r.get("mt") == 7 and r.get("seq") == seq
                             and r.get("controller") == tx["response"]["controller"] and r.get("status") == 0), None)
        state = {}

        def done():
            ack = ackf()
            av = next((r for r in wire if ack and r.get("valid") and r.get("sid") == SID
                       and r["port"] == WIREPORT and r["ns"] >= ack["ns"]), None)
            if av and "seen" not in state:
                state["seen"] = time.monotonic()
            return "seen" in state and time.monotonic() - state["seen"] >= 3
        wait(30, until=done)
        ack = ackf()
        av = next((r for r in wire if ack and r.get("valid") and r.get("sid") == SID
                   and r["port"] == WIREPORT and r["ns"] >= ack["ns"]), None)
        result["response_ns"] = ack["ns"] - t_start if ack else None
        result["first_avtp_ns"] = av["ns"] - t_start if av else None
        result["latency_s"] = (av["ns"] - ack["ns"]) / 1e9 if ack and av else None
        result["status"] = "PASS" if result["latency_s"] is not None and result["latency_s"] < 1 else "FAIL"
        assert ack, "successful response absent from tap"
        if mode == "cycle":
            dis = next(r for r in rows if r.get("kind") == "transaction" and r["mt"] == 8)
            dr = next(r for r in wire if r.get("mt") == 9 and r.get("seq") == dis["seq"]
                      and r.get("controller") == dis["response"]["controller"])
            cc = next(r for r in wire if r.get("mt") == 6 and r.get("seq") == seq
                      and r.get("controller") == tx["response"]["controller"])
            result["disconnect_response_ns"] = dr["ns"] - t_start
            result["connect_command_ns"] = cc["ns"] - t_start
            result["disconnect_hold_s"] = (cc["ns"] - dr["ns"]) / 1e9
            result["hold_pdus_live"] = sum(bool(r.get("valid")) and r.get("sid") == SID and r["port"] == WIREPORT
                                           and dr["ns"] + 500000000 <= r["ns"] < ack["ns"] for r in wire)
    else:
        dis = next(r for r in rows if r.get("kind") == "transaction" and r["mt"] == 8)
        dr = None
        wait(3, until=lambda: any(r.get("mt") == 9 and r.get("seq") == dis["seq"] for r in wire))
        dr = next(r for r in wire if r.get("mt") == 9 and r.get("seq") == dis["seq"]
                  and r.get("controller") == dis["response"]["controller"])
        lvf = lambda: next((e for e in msrp_events if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise"
                            and e["sid"] == SID and e["event"] == "Lv" and e["ns"] >= dr["ns"]), None)
        wait(40, until=lambda: lvf() is not None)
        lv = lvf()
        result["disconnect_response_ns"] = dr["ns"] - t_start
        result["dut_ta_lv_after_response_s"] = (lv["ns"] - dr["ns"]) / 1e9 if lv else None
        if lv:
            wait(SETTLE)
        result["ta_redeclared_after_lv"] = target_ta_declared(lv["ns"] + 1) if lv else None
        result["status"] = "SETTLED" if lv and not result["ta_redeclared_after_lv"] else "FAIL"
    result["capture_span_s"] = (wire[-1]["ns"] - t_start) / 1e9
    console("after")
    controller_action("snapshot")
    (dest / "snapshot-after.jsonl").write_text((dest / "snapshot.jsonl").read_text())
finally:
    try:
        stop_capture()
    finally:
        if "err" in globals():
            err.close()
        result["capture_rc"] = capture.returncode if capture else None
        result["errors"] = errors
        (dest / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        if (root / "tap.pcap").exists():
            b = (root / "tap.pcap").read_bytes()
            (dest / "raw-artifacts.json").write_text(json.dumps(
                [dict(path=name + "/tap.pcap", size=len(b), sha256=hashlib.sha256(b).hexdigest())], indent=2) + "\n")
    event("complete", **result)
assert not errors, errors
assert result["capture_rc"] == 0, result
