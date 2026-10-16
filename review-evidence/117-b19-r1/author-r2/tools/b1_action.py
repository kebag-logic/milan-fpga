"""One bench action for lane B1: joined foreground measurements.

Derived from the PR #600 runner (action.py in this directory). The caller
holds the bench lock for the whole action. No process is detached; every
child has an explicit deadline. Endpoints are arguments, never embedded.

kinds:
  observe  measurements only
  cycle    measurements; after PRE s, OUT4 off for HOLD s, then on
  gm       sync the controller host's PHC to the current grandmaster as a
           slave-only port, offset it by GM_OFFSET s, then measurements;
           after PRE s a software grandmaster runs for HOLD s

usage: b1_action.py <name> <duration_s> <kind> <console> <controller> <ctl_if>
                    <tap_host> <tap_if> <strip_host> [HOLD] [PRE]
The GM kind reads the linuxptp directory and configs from /tmp/a438 on the
controller host (see gm_prep.sh).
"""
import concurrent.futures as cf
from pathlib import Path
import json, os, re, shlex, signal, subprocess, sys, termios, time, tty
sys.path.insert(0, str(Path(__file__).resolve().parent))
from console_poll import transact

name, duration, kind, port, controller, ctl_if, tap, tap_if, strip = sys.argv[1:10]
duration = int(duration)
HOLD = float(sys.argv[10]) if len(sys.argv) > 10 else 20.0
PRE = float(sys.argv[11]) if len(sys.argv) > 11 else 10.0
GM_OFFSET = os.environ.get("GM_OFFSET", "0.010")
assert kind in ("observe", "cycle", "gm")
root = Path("/tmp/b1-a438/raw") / name
root.mkdir(parents=True, exist_ok=False)
packet = Path(__file__).resolve().parent.parent / "bench" / name
stop = False
outlet_off = False
gm_running = False
last_console = 0.0
results = {}
CONSOLE = ["milan_status", "mem_read 0x90000110 4", "mem_read 0xf000181c 4",
           "mem_read 0x90000774 4", "mem_read 0x90000720 4", "mem_read 0x90000780 4",
           "mem_read 0x900008f8 4", "mem_read 0x90000750 4", "mem_read 0x90000764 4"]
for c in CONSOLE:
    assert c == "milan_status" or c.startswith("mem_read ")


def event(k, **kw):
    r = dict(t=time.time(), kind=k, **kw)
    with (root / "events.jsonl").open("a") as f:
        f.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(["timeout", str(int(limit)) + "s", *args], timeout=limit + 5, **kw)


def ssh(host, args, limit, **kw):
    return run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "-o",
                "StrictHostKeyChecking=no", host, shlex.join(args)], limit, **kw)


def offset(host, role, tag):
    for _ in range(3):
        t0 = time.time()
        r = ssh(host, ["timeout", "5s", "date", "+%s.%N"], 8, capture_output=True, text=True)
        t1 = time.time()
        if r.returncode:
            raise RuntimeError("clock read failed: " + role)
        event("clock", role=role, tag=tag, t0=t0, t1=t1, remote=float(r.stdout))


def outlets():
    r = ssh(strip, ["timeout", "8s", "powerstrip", "status"], 12, capture_output=True, text=True)
    parsed = dict(re.findall(r"OUT([0-6])\s+(ON|OFF)", r.stdout))
    return r.returncode, parsed, r.stdout


def status(tag, initial=None, out4=None):
    rc, parsed, text = outlets()
    event("outlets", tag=tag, rc=rc, output=text, parsed=parsed)
    assert rc == 0 and len(parsed) == 7, "outlet status unreadable"
    if initial is not None:
        others = {k: v for k, v in parsed.items() if k != "4"}
        assert others == {k: v for k, v in initial.items() if k != "4"}, "another outlet changed"
    if out4 is not None:
        assert parsed["4"] == out4, "OUT4 not " + out4
    return parsed


def power(value):
    global outlet_off
    assert value in ("on", "off")
    if value == "off":
        outlet_off = True
    event("power-command", value=value, outlet=4)
    r = ssh(strip, ["timeout", "8s", "powerstrip", value, "4"], 12, capture_output=True, text=True)
    event("power-result", value=value, rc=r.returncode, output=r.stdout + r.stderr)
    if r.returncode:
        raise RuntimeError("OUT4 command failed")
    if value == "on":
        outlet_off = False


def capture(host, iface, role):
    with (root / (role + ".pcap")).open("wb") as out:
        r = ssh(host, ["sudo", "-n", "timeout", "-s", "INT", str(duration) + "s", "tcpdump", "-U",
                       "-n", "-i", iface, "-w", "-"], duration + 10, stdout=out,
                stderr=subprocess.PIPE)
    log = r.stderr.decode(errors="replace").replace(iface, "<capture-interface>")
    (root / (role + "-capture.txt")).write_text(log)
    assert r.returncode in (0, 124), r.returncode
    assert (root / (role + ".pcap")).stat().st_size > 24
    return r.returncode


def watch():
    with (root / "controller.jsonl").open("wb") as out:
        r = ssh(controller, ["sudo", "-n", "timeout", str(duration + 3) + "s", "python3", "-B",
                             "/tmp/a438/a438_controller.py", ctl_if, "watch", str(duration)],
                duration + 10, stdout=out, stderr=subprocess.PIPE)
    (root / "controller-errors.txt").write_bytes(r.stderr)
    assert r.returncode == 0, r.returncode
    return r.returncode


def console():
    global last_console
    end = time.monotonic() + duration
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        with (root / "console.jsonl").open("w", buffering=1) as out:
            while time.monotonic() < end and not stop:
                start = time.monotonic()
                for cmd in CONSOLE:
                    t0, t1, raw = transact(fd, cmd)
                    out.write(json.dumps(dict(t=t0, end=t1, cmd=cmd, raw=raw)) + "\n")
                    assert "litex" in raw, "console prompt missing"
                    if cmd == "milan_status":
                        last_console = time.monotonic()
                time.sleep(max(0, min(.25 - (time.monotonic() - start), end - time.monotonic())))
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, saved)
        os.close(fd)
    return 0


def gm_prep():
    """Slave-only sync of the controller PHC to the current GM, then +GM_OFFSET."""
    with (root / "ptp4l-slave.log").open("wb") as out:
        r = ssh(controller, ["sudo", "-n", "timeout", "-s", "INT", "40s", "/tmp/a438/lptp/ptp4l",
                             "-f", "/tmp/a438/slave.cfg", "-i", ctl_if, "-m"], 50, stdout=out,
                stderr=subprocess.STDOUT)
    event("gm-prep-slave", rc=r.returncode)
    text = (root / "ptp4l-slave.log").read_text(errors="replace")
    rms = [int(m) for m in re.findall(r"rms\s+(\d+)\s+max", text)]
    mx = [int(m) for m in re.findall(r"max\s+(\d+)\s+freq", text)]
    event("gm-prep-converged", last_rms_ns=rms[-5:], last_max_ns=mx[-5:])
    assert len(rms) >= 5 and all(v < 1000 for v in mx[-5:]), "controller PHC did not converge"
    r = ssh(controller, ["sudo", "-n", "/tmp/a438/lptp/phc_ctl", ctl_if, "freq", "adj", GM_OFFSET,
                         "cmp"], 15, capture_output=True, text=True)
    event("gm-prep-offset", rc=r.returncode, offset_s=GM_OFFSET, output=r.stdout + r.stderr)
    assert r.returncode == 0


def gm_run():
    global gm_running
    gm_running = True
    event("gm-start", hold_s=HOLD)
    with (root / "ptp4l-gm.log").open("wb") as out:
        r = ssh(controller, ["sudo", "-n", "timeout", "-s", "INT", str(int(HOLD)) + "s",
                             "/tmp/a438/lptp/ptp4l", "-f", "/tmp/a438/gm.cfg", "-i", ctl_if, "-m"],
                HOLD + 15, stdout=out, stderr=subprocess.STDOUT)
    gm_running = False
    event("gm-end", rc=r.returncode)
    return r.returncode


def stopping(sig, frame):
    global stop
    stop = True


signal.signal(signal.SIGTERM, stopping)
signal.signal(signal.SIGINT, stopping)
try:
    for host, role in [(controller, "controller"), (tap, "tap"), (strip, "power")]:
        offset(host, role, "before")
    initial = status("before", out4="ON")
    if kind == "gm":
        gm_prep()
    with cf.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(console): "console", pool.submit(watch): "controller",
                   pool.submit(capture, tap, tap_if, "tap"): "tap",
                   pool.submit(capture, controller, ctl_if, "controller-wire"): "controller-wire"}
        if kind in ("cycle", "gm"):
            time.sleep(PRE)
            assert time.monotonic() - last_console < 1, "console preflight failed"
            assert all(not f.done() for f in futures), "measurement exited before the action"
            assert (root / "tap.pcap").stat().st_size > 24, "tap not recording"
        if kind == "cycle":
            try:
                power("off")
                status("off", initial=initial, out4="OFF")
                start = time.monotonic()
                while time.monotonic() - start < HOLD and not stop:
                    if time.monotonic() - last_console > 2:
                        raise RuntimeError("DUT console lost during the outage")
                    time.sleep(.1)
            finally:
                if outlet_off:
                    power("on")
            status("on", initial=initial, out4="ON")
        if kind == "gm":
            futures[pool.submit(gm_run)] = "gm"
        for f in cf.as_completed(futures):
            results[futures[f]] = f.result()
    if stop:
        raise RuntimeError("action interrupted")
finally:
    if outlet_off:
        for attempt in range(3):
            try:
                power("on")
                break
            except Exception:
                event("restore-retry", attempt=attempt)
    event("finished", results=results, outlet_off=outlet_off)
    (root / "results.json").write_text(json.dumps(results, indent=2) + "\n")
for host, role in [(controller, "controller"), (tap, "tap"), (strip, "power")]:
    offset(host, role, "after")
status("after", initial=initial, out4="ON")
packet.mkdir(parents=True, exist_ok=True)
for f in root.iterdir():
    if f.is_file() and f.stat().st_size <= 200000:
        (packet / f.name).write_bytes(f.read_bytes())
print("ACTION_COMPLETE " + name, flush=True)
