#!/usr/bin/env python3
"""One DIN action with the talker's output map routed (this host; the caller
holds the bench lock).

usage: run_din3.py <name> <listen_s> <play_s> <raw_root>

run_din2.py plus one routing step. In this image STREAM_PORT_OUTPUT 0 has a
dynamic audio map (ADP_DMAP_OUT_MASK_C bit 0), so the capture crossbar feeds
the talker and an empty map sends digital silence on every stream channel.
Before the listener starts, eight identity mappings are added on
STREAM_PORT_OUTPUT 0 (stream 0 channel c <- cluster c; the generated CSRC
table puts clusters 0..7 on TDM input slots 0..7). They are removed in
`finally`, and the empty map is read back.

The sequence is otherwise run_din.py's, except for the pattern source. The SoC board
builds one 65,536-frame period of the DIN pattern in its own /tmp (awk | xxd)
and checks it against the SHA-256 of the period computed here from the rule;
aplay then reads that period in a loop. The ordinal is 16 bits wide, so the
looped period is byte-identical to the host pattern file run_din.py served.

1. SoC console: build and verify /tmp/a403-din.raw (abort on mismatch).
2. Controller: slave-only gPTP, then din_listener.py (probe, MSRP Listener
   Ready, MVRP, tcpdump of every frame from the DUT MAC).
3. DUT console: talker, admission and slip samples before and after.
4. SoC console: `while cat period; do :; done | aplay -D hw:0,0` for
   <play_s> seconds.
5. Copy the pcap and the listener log back, remove them on the controller,
   remove the period file on the SoC. The SoC bridge legs are not touched.

Environment: SOC_CONSOLE, DUT_CONSOLE, CTL_HOST, CTL_IFACE, PTP4L, GPTP_CFG.
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
OLD_TOOLS = Path(os.environ.get("A403_TOOLS", TOOLS))
SOC, DUT = os.environ["SOC_CONSOLE"], os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PTP4L, GPTP_CFG = os.environ["PTP4L"], os.environ["GPTP_CFG"]
DUT_READS = ["mem_read 0x90000660 20", "mem_read 0x90000694 8", "mem_read 0x900006cc 12",
             "mem_read 0x900008d4 12"]
PERIOD = "/tmp/a403-din.raw"
AWK = ("awk 'BEGIN{for(n=0;n<65536;n++){h=sprintf(\"00%02x%02x\",n%256,int(n/256));s=\"\";"
       "for(c=1;c<=8;c++)s=s h sprintf(\"%02x\",c);print s}}' | xxd -r -p > " + PERIOD)

name, listen_s, play_s, raw_root = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
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
    r = ssh(f"cd /tmp/a403 && sudo -n timeout {int(limit)} python3 -B avdecc_rw.py {args}", limit,
            capture_output=True, text=True)
    (root / f"ctl-{tag}.jsonl").write_text(r.stdout + r.stderr)
    event("ctl", tag=tag, rc=r.returncode)
    return r


def dut(tag):
    r = run(["python3", str(OLD_TOOLS / "console_read.py"), DUT, str(root / f"dut-{tag}.txt"), *DUT_READS], 60,
            capture_output=True, text=True)
    event("dut", tag=tag, rc=r.returncode)


def soc(tag, limit, cmd):
    r = run(["python3", str(OLD_TOOLS / "soccon.py"), SOC, str(root / f"soc-{tag}.log"), str(limit), cmd],
            limit + 30, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


period = array.array("I", [(((c + 1) << 16) | n) << 8 for n in range(65536) for c in range(8)])
if sys.byteorder != "little":
    period.byteswap()
digest = hashlib.sha256(period.tobytes()).hexdigest()
event("pattern-period", frames=65536, bytes=len(period) * 4, sha256=digest)
event("start", name=name, listen_s=listen_s, play_s=play_s)
lis = None
built = mapped = False
try:
    rc = soc("build", 180, f"cat /proc/uptime; {AWK}; echo build_rc=$?; cat /proc/uptime; "
                           f"wc -c < {PERIOD}; echo '{digest}  {PERIOD}' | sha256sum -c")
    built = True
    if rc != 0:
        raise SystemExit(f"period build or check failed on the SoC board (rc {rc})")
    ctl(f"getmap {IFACE} 0x000f 0", 10, "map-initial")
    mapped = True
    ctl(f"map {IFACE} add 0x000f 0 8", 10, "map-add")
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
        f"while cat {PERIOD}; do :; done | "
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
        r = ssh(f"sudo -n chown $(id -u) /tmp/a403/{name}.pcap; stat -c %s /tmp/a403/{name}.pcap; "
                f"sha256sum /tmp/a403/{name}.pcap; cat /tmp/a403/{name}-listener.jsonl; echo ====; "
                f"tail -30 /tmp/a403/{name}-gptp.log", 30, capture_output=True, text=True)
        (root / "controller-logs.txt").write_text(r.stdout + r.stderr)
        r = run(["scp", "-q", f"{CTL}:/tmp/a403/{name}.pcap", str(root / f"{name}.pcap")], 120)
        event("pcap-copied", rc=r.returncode,
              bytes=(root / f"{name}.pcap").stat().st_size if (root / f"{name}.pcap").exists() else None)
        if r.returncode == 0:
            ssh(f"sudo -n rm -f /tmp/a403/{name}.pcap", 20)
    if mapped:
        ctl(f"map {IFACE} remove 0x000f 0 8", 10, "map-remove")
        ctl(f"getmap {IFACE} 0x000f 0", 10, "map-final")
    if lis is not None:
        dut("final")
    if built:
        soc("cleanup", 30, f"rm -f {PERIOD}; ls /tmp")
    event("end")
