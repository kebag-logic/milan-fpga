#!/usr/bin/env python3
"""One #451 timing action (this host; the caller holds the bench lock).

usage: run_timing.py <name> <talker_s> <capture_s> <raw_root>

Lane B4 copy of run_dout.py (lane B3, from first light). The DUT side, the
controller side and the finally block are unchanged. Only the SoC board's
capture differs, because a capture of at least 10 minutes (921.6 MB) is
larger than the SoC board's temporary storage:

1. Controller: slave-only gPTP, then the software AAF talker (aaf_talker.py).
2. Controller: bind DUT STREAM_INPUT 0 to the talker, add eight identity
   mappings on STREAM_PORT_INPUT 0 (stream channel c -> cluster c).
3. DUT console: listener, parser, depacketizer and render-stage samples.
4. SoC console: one direct `arecord -v -D hw:0,0` of <capture_s>, streamed
   while it records over TCP (bash /dev/tcp) to a receiver bound to the ECM
   address of this host, which hashes it. While it records, the McASP0
   capture substream's hw_params and sw_params are read once and its status
   (hw_ptr, tstamp, CLOCK_MONOTONIC) every 5 s, from /proc only. arecord's
   stderr (setup, any overrun) goes to a small file on the SoC board, which
   is printed and removed.
5. finally: remove the mappings, unbind, verify empty map and unbound state,
   stop the talker and gPTP. The SoC bridge legs are not touched here.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
SOC = os.environ["SOC_CONSOLE"]          # SoC board serial console
DUT = os.environ["DUT_CONSOLE"]          # DUT serial console
CTL = os.environ["CTL_HOST"]             # controller host (ssh alias)
IFACE = os.environ["CTL_IFACE"]          # controller AVB interface
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]  # passed through sudo
GM_ID = os.environ.get("GM_ID", "0000000000000000")
PTP4L = os.environ["PTP4L"]              # gPTP daemon on the controller
GPTP_CFG = os.environ["GPTP_CFG"]        # its gPTP profile
TALKER = os.environ["TALKER_EID"]         # the software endpoint id aaf_talker.py derives
LISTENER = "020000fffe000001"
PORT = 18468
DUT_READS = ["mem_read 0x900006a4 4", "mem_read 0x900006b8 20", "mem_read 0x900006ec 4",
             "mem_read 0x900008b4 20", "mem_read 0x900008d4 12"]

name, talker_s, capture_s, raw_root = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
root = Path(raw_root) / name
root.mkdir(parents=True, exist_ok=False)
events = open(root / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(args, timeout=limit + 5, **kw)


def ssh(cmd, limit, **kw):
    return run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL, cmd], limit, **kw)


def ctl(args, limit, tag):
    r = ssh(f"cd /tmp/a468 && sudo -n env PEER_EID={PEER_EID} PEER_MAC={PEER_MAC} "
            f"timeout {int(limit)} python3 -B avdecc_rw.py {args}", limit,
            capture_output=True, text=True)
    (root / f"ctl-{tag}.jsonl").write_text(r.stdout + r.stderr)
    event("ctl", tag=tag, rc=r.returncode)
    return r


def dut(tag):
    r = run(["python3", str(TOOLS / "console_read.py"), DUT, str(root / f"dut-{tag}.txt"), *DUT_READS], 60,
            capture_output=True, text=True)
    event("dut", tag=tag, rc=r.returncode)
    return r.returncode


def soc(tag, limit, cmd):
    r = run(["python3", str(TOOLS / "soccon.py"), SOC, str(root / f"soc-{tag}.log"), str(limit), cmd], limit + 30,
            capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


import hostsrv
rx = hostsrv.TcpReceiver(root, PORT, f"{name}.raw", lambda **kw: event("upload", **kw))
event("start", name=name, talker_s=talker_s, capture_s=capture_s)
talker = None
mapped = bound = False
try:
    limit = talker_s + 40
    talker = subprocess.Popen(
        ["ssh", "-o", "BatchMode=yes", CTL,
         f"cd /tmp/a468 && sudo -n env GM_ID={GM_ID} timeout {int(limit)} python3 -B with_gptp.py {IFACE} {PTP4L} {GPTP_CFG} "
         f"/tmp/a468/{name}-gptp.log 20 {int(talker_s + 25)} -- python3 -B aaf_talker.py {IFACE} {talker_s} "
         f"/tmp/a468/{name}-talker.jsonl 0 /dev/ptp0"],
        stdout=open(root / "talker-stdout.txt", "w"), stderr=subprocess.STDOUT)
    event("talker-started")
    dut("before")
    time.sleep(16)
    ctl(f"bind {IFACE} {TALKER} 0 {LISTENER} 0", 10, "bind")
    bound = True
    ctl(f"map {IFACE} add 0x000e 0 8", 10, "map-add")
    mapped = True
    for i in range(3):
        time.sleep(2)
        dut(f"active-{i}")
    soc("capture", capture_s + 90,
        f"S=/proc/asound/card0/pcm0c/sub0; E=/tmp/a468-arecord.err; cat /proc/uptime; "
        f"arecord -v -D hw:0,0 -c 8 -f S32_LE -r 48000 -t raw -d {int(capture_s)} 2>$E "
        f">/dev/tcp/{hostsrv.HOST}/{PORT} & A=$!; sleep 3; echo HWP; cat $S/hw_params; echo SWP; cat $S/sw_params; "
        f"while [ -d /proc/$A ]; do echo \"U $(cat /proc/uptime)\"; cat $S/status; sleep 5; done; "
        f"wait $A; echo arecord_rc=$?; cat /proc/uptime; echo ERR; cat $E; rm -f $E; ls /tmp; df -k /tmp | tail -1")
    rx.close(30)
    dut("after-capture")
finally:
    if mapped:
        ctl(f"map {IFACE} remove 0x000e 0 8", 10, "map-remove")
    if bound:
        ctl(f"unbind {IFACE} {TALKER} 0 {LISTENER} 0", 10, "unbind")
    ctl(f"getmap {IFACE} 0x000e 0", 10, "map-final")
    if talker is not None:
        try:
            talker.wait(max(5, talker_s + 45))
        except subprocess.TimeoutExpired:
            talker.terminate()
            talker.wait(10)
        event("talker-exit", rc=talker.returncode)
    r = ssh(f"cat /tmp/a468/{name}-talker.jsonl; echo ====; cat /tmp/a468/{name}-gptp.log | tail -40", 20,
            capture_output=True, text=True)
    (root / "controller-logs.txt").write_text(r.stdout)
    dut("final")
    rx.close(1)
    event("end")
