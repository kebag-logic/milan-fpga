#!/usr/bin/env python3
"""One DIN action (this host; the caller holds the bench lock).

usage: run_din.py <name> <listen_s> <play_s> <raw_root>

1. Host: serve the DIN pattern (8 ch S32_LE; SoC channel c carries
   ((c + 1) << 16 | frame & 0xffff) << 8) over HTTP on the ECM address,
   generating it once under <raw_root>/din-src if absent.
2. Controller: slave-only gPTP, then din_listener.py (probe, MSRP Listener
   Ready, MVRP, tcpdump of every frame from the DUT MAC).
3. DUT console: talker, admission and slip samples before and after.
4. SoC console: `wget -O - | aplay -D hw:0,0` for <play_s> seconds.
5. Copy the pcap and the listener log back, check sizes and hashes, remove
   them on the controller. The SoC bridge legs are not touched here.
"""
import array
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import hostsrv  # noqa: E402

SOC = os.environ["SOC_CONSOLE"]          # SoC board serial console
DUT = os.environ["DUT_CONSOLE"]          # DUT serial console
CTL = os.environ["CTL_HOST"]             # controller host (ssh alias)
IFACE = os.environ["CTL_IFACE"]          # controller AVB interface
PTP4L = os.environ["PTP4L"]              # gPTP daemon on the controller
GPTP_CFG = os.environ["GPTP_CFG"]        # its gPTP profile
PORT = 18404
DUT_READS = ["mem_read 0x90000660 20", "mem_read 0x90000694 8", "mem_read 0x900006cc 12",
             "mem_read 0x900008d4 12"]
PATTERN_FRAMES = 48000 * 90

name, listen_s, play_s, raw_root = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
src_dir = Path(raw_root) / "din-src"
src_dir.mkdir(parents=True, exist_ok=True)
pattern = src_dir / "din-pattern.raw"
if not pattern.exists():
    period = array.array("I", [(((c + 1) << 16) | n) << 8 for n in range(65536) for c in range(8)])
    blob = period.tobytes()             # little-endian host: S32_LE
    with open(pattern, "wb") as f:
        left = PATTERN_FRAMES * 32
        while left > 0:
            f.write(blob[:left])
            left -= len(blob[:left])
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


def dut(tag):
    r = run(["python3", str(TOOLS / "console_read.py"), DUT, str(root / f"dut-{tag}.txt"), *DUT_READS], 60,
            capture_output=True, text=True)
    event("dut", tag=tag, rc=r.returncode)


def soc(tag, limit, cmd):
    r = run(["python3", str(TOOLS / "soccon.py"), SOC, str(root / f"soc-{tag}.log"), str(limit), cmd], limit + 30,
            capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


event("pattern", bytes=pattern.stat().st_size,
      sha256=hashlib.sha256(pattern.read_bytes()).hexdigest())
srv = hostsrv.FileServer(src_dir, PORT)
event("start", name=name, listen_s=listen_s, play_s=play_s)
lis = None
try:
    lis = subprocess.Popen(
        ["ssh", "-o", "BatchMode=yes", CTL,
         f"cd /tmp/a403 && sudo -n timeout {int(listen_s + 60)} python3 -B with_gptp.py {IFACE} {PTP4L} {GPTP_CFG} "
         f"/tmp/a403/{name}-gptp.log 20 {int(listen_s + 45)} -- python3 -B din_listener.py {IFACE} {listen_s} "
         f"/tmp/a403/{name}.pcap /tmp/a403/{name}-listener.jsonl"],
        stdout=open(root / "listener-stdout.txt", "w"), stderr=subprocess.STDOUT)
    event("listener-started")
    dut("before")
    time.sleep(16)
    dut("streaming")
    soc("play", play_s + 60,
        f"cat /proc/uptime; grep -E '^ *(95|107):' /proc/interrupts; "
        f"wget -q -O - http://{hostsrv.HOST}:{PORT}/din-pattern.raw | "
        f"aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {int(play_s)}; echo aplay_rc=$?; cat /proc/uptime; "
        f"grep -E '^ *(95|107):' /proc/interrupts; "
        f"ls /tmp; df -k /tmp | tail -1")
    dut("after-play")
finally:
    if lis is not None:
        try:
            lis.wait(listen_s + 90)
        except subprocess.TimeoutExpired:
            lis.terminate()
            lis.wait(10)
        event("listener-exit", rc=lis.returncode)
    r = ssh(f"sudo -n chown $(id -u) /tmp/a403/{name}.pcap; ls -l /tmp/a403/{name}.pcap; "
            f"sha256sum /tmp/a403/{name}.pcap; cat /tmp/a403/{name}-listener.jsonl; echo ====; "
            f"tail -30 /tmp/a403/{name}-gptp.log", 30, capture_output=True, text=True)
    (root / "controller-logs.txt").write_text(r.stdout + r.stderr)
    r = run(["scp", "-q", f"{CTL}:/tmp/a403/{name}.pcap", str(root / f"{name}.pcap")], 120)
    event("pcap-copied", rc=r.returncode,
          bytes=(root / f"{name}.pcap").stat().st_size if (root / f"{name}.pcap").exists() else None)
    if r.returncode == 0:
        ssh(f"sudo -n rm -f /tmp/a403/{name}.pcap", 20)
    dut("final")
    srv.close()
    event("end")
