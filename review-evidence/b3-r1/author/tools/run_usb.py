#!/usr/bin/env python3
"""One DOUT action captured on this host's USB Audio card through the SoC
board's bridge (this host; the caller holds the bench lock).

usage: run_usb.py <name> <talker_s> <capture_s> <raw_root>

The DUT side is the first-light DOUT method (run_dout.py) unchanged: a
software AAF talker on the controller host, DUT STREAM_INPUT 0 bound to it,
eight identity mappings on STREAM_PORT_INPUT 0. The difference is the capture
point. The SoC board's bridge is left running as found (its to-host leg
copies McASP0 receive to the USB Audio function), and this host records the
USB Audio card's capture endpoint for <capture_s> seconds, eight channels
S32_LE at 48 kHz. Nothing on the SoC board is started, stopped or changed:
the SoC console is used only for read-only bridge status samples.

1. Controller: slave-only gPTP, then the software AAF talker (aaf_talker.py).
2. Controller: bind DUT STREAM_INPUT 0, add the eight identity mappings.
3. DUT console: listener, parser, depacketizer and render-stage samples.
4. SoC console (read-only): bridge status and interrupt counts.
5. This host: arecord on the USB Audio card (sudo: the account is not in the
   audio group), with a hard deadline, then size and SHA-256.
6. SoC console (read-only): bridge status again.
7. finally: remove the mappings, unbind, verify the empty map, stop the
   talker and gPTP.

Environment: SOC_CONSOLE, DUT_CONSOLE, CTL_HOST, CTL_IFACE, PTP4L, GPTP_CFG,
TALKER_EID, USB_PCM (the ALSA device of the USB Audio card, e.g. hw:UAC2,0).
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SOC, DUT = os.environ["SOC_CONSOLE"], os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]  # passed through sudo
GM_ID = os.environ.get("GM_ID", "0000000000000000")
PTP4L, GPTP_CFG = os.environ["PTP4L"], os.environ["GPTP_CFG"]
TALKER = os.environ["TALKER_EID"]
USB_PCM = os.environ["USB_PCM"]
LISTENER = "020000fffe000001"
DUT_READS = ["mem_read 0x900006a4 4", "mem_read 0x900006b8 20", "mem_read 0x900006ec 4",
             "mem_read 0x900008b4 20", "mem_read 0x900008d4 12"]
SOC_STATUS = ("cat /proc/uptime; tdm8-uac2.sh status; echo UDC=$(cat /sys/class/udc/*/state); "
              "for s in /proc/asound/card*/pcm*/sub0/status; do echo \"== $s\"; head -3 $s; done; "
              "grep dma-controller /proc/interrupts; "
              "echo BAD=$(dmesg | grep -ciE 'self-detected|rcu_preempt detected|replenish|WARNING|teardown|"
              "refused to stop|Call trace|BUG:|Oops'); cat /proc/sys/kernel/tainted; cat /proc/uptime")

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
    r = ssh(f"cd /tmp/a453 && sudo -n env PEER_EID={PEER_EID} PEER_MAC={PEER_MAC} "
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
    r = run(["python3", str(TOOLS / "soccon.py"), SOC, str(root / f"soc-{tag}.log"), str(limit), cmd],
            limit + 30, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


event("start", name=name, talker_s=talker_s, capture_s=capture_s, pcm=USB_PCM)
talker = None
mapped = bound = False
raw = root / f"{name}.raw"
try:
    limit = talker_s + 40
    talker = subprocess.Popen(
        ["ssh", "-o", "BatchMode=yes", CTL,
         f"cd /tmp/a453 && sudo -n env GM_ID={GM_ID} timeout {int(limit)} python3 -B with_gptp.py {IFACE} {PTP4L} {GPTP_CFG} "
         f"/tmp/a453/{name}-gptp.log 20 {int(talker_s + 25)} -- python3 -B aaf_talker.py {IFACE} {talker_s} "
         f"/tmp/a453/{name}-talker.jsonl 0 /dev/ptp0"],
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
    soc("status-before", 40, SOC_STATUS)
    t0 = time.time()
    r = run(["sudo", "-n", "timeout", str(int(capture_s + 30)), "arecord", "-v", "-D", USB_PCM, "-c", "8",
             "-f", "S32_LE", "-r", "48000", "-t", "raw", "-d", str(int(capture_s)), str(raw)],
            capture_s + 40, capture_output=True, text=True)
    t1 = time.time()
    (root / "arecord.log").write_text(r.stdout + r.stderr)
    size = raw.stat().st_size if raw.exists() else None
    digest = hashlib.sha256(raw.read_bytes()).hexdigest() if raw.exists() else None
    event("arecord", rc=r.returncode, seconds=round(t1 - t0, 3), bytes=size, sha256=digest,
          expected_bytes=int(capture_s * 48000 * 32))
    soc("status-after", 40, SOC_STATUS)
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
    r = ssh(f"cat /tmp/a453/{name}-talker.jsonl; echo ====; cat /tmp/a453/{name}-gptp.log | tail -40", 20,
            capture_output=True, text=True)
    (root / "controller-logs.txt").write_text(r.stdout)
    dut("final")
    event("end")
