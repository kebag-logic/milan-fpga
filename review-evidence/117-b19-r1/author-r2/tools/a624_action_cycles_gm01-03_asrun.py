"""One bench action for lane B19: joined foreground measurements.

Lane B1's b1_action.py (itself derived from the PR #600 runner). Lane B19 changes:
the raw and staging directories; the tap capture keeps 160 octets of every frame
and drops only the AAF PDUs (the music streams), so gPTP, CRF, MSRP and AVDECC stay;
the controller watcher polls the lane's stream set ("all" or "music" pairs, from the
environment variable PAIRS); a "dutcycle" kind switches OUT0 (the DUT) once for the
first-reach measurement, with a passive console log across the boot; the outlet
checks compare every outlet but the switched one with the start. The caller
holds the bench lock for the whole action. No process is detached; every
child has an explicit deadline. Endpoints are arguments, never embedded.

kinds:
  observe  measurements only
  cycle    measurements; after PRE s, OUT4 off for HOLD s, then on
  dutcycle measurements; after PRE s, OUT0 off for HOLD s, then on (once per lane)
  gm       sync the controller host's PHC to the current grandmaster as a
           slave-only port, offset it by GM_OFFSET s, then measurements;
           after PRE s a software grandmaster runs for HOLD s

usage: a624_action.py <name> <duration_s> <kind> <console> <controller> <ctl_if>
                    <tap_host> <tap_if> <strip_host> [HOLD] [PRE]
The GM kind reads the linuxptp build and configs from /tmp/a624 on the
controller host.
"""
import concurrent.futures as cf
import select
from pathlib import Path
import json, os, re, shlex, signal, subprocess, sys, termios, time, tty
sys.path.insert(0, str(Path(__file__).resolve().parent))
from console_poll import transact

name, duration, kind, port, controller, ctl_if, tap, tap_if, strip = sys.argv[1:10]
duration = int(duration)
HOLD = float(sys.argv[10]) if len(sys.argv) > 10 else 20.0
PRE = float(sys.argv[11]) if len(sys.argv) > 11 else 10.0
GM_OFFSET = os.environ.get("GM_OFFSET", "0.010")
assert kind in ("observe", "cycle", "dutcycle", "gm")
OUTLET = 0 if kind == "dutcycle" else 4
PAIRS = os.environ.get("PAIRS", "all")
assert PAIRS in ("all", "music")
SNAP = 160
# drop AAF (subtype 0x02) behind the 28-octet tap envelope, tagged or not; keep everything else
TAP_FILTER = ("not ((ether[40:2]=0x22f0 and ether[42]=0x02) or "
              "(ether[40:2]=0x8100 and ether[44:2]=0x22f0 and ether[46]=0x02))")
root = Path("/tmp/a624/raw") / name
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
    o = str(OUTLET)
    if initial is not None:
        others = {k: v for k, v in parsed.items() if k != o}
        assert others == {k: v for k, v in initial.items() if k != o}, "another outlet changed"
    if out4 is not None:
        assert parsed[o] == out4, "OUT%s not %s" % (o, out4)
    return parsed


def power(value):
    global outlet_off
    assert value in ("on", "off") and OUTLET in (0, 4)
    if value == "off":
        if OUTLET == 0:
            guard = Path("/tmp/a624/priv/out0-used")
            assert not guard.exists(), "OUT0 was already switched once in this lane"
            guard.write_text(name + "\n")
        outlet_off = True
    event("power-command", value=value, outlet=OUTLET)
    r = ssh(strip, ["timeout", "8s", "powerstrip", value, str(OUTLET)], 12, capture_output=True, text=True)
    event("power-result", value=value, rc=r.returncode, output=r.stdout + r.stderr)
    if r.returncode:
        raise RuntimeError("OUT%d command failed" % OUTLET)
    if value == "on":
        outlet_off = False


def capture(host, iface, role):
    with (root / (role + ".pcap")).open("wb") as out:
        extra = ["-s", str(SNAP), TAP_FILTER] if role == "tap" else []
        r = ssh(host, ["sudo", "-n", "timeout", "-s", "INT", str(duration) + "s", "tcpdump", "-U",
                       "-n", "-i", iface, "-w", "-", *extra], duration + 10, stdout=out,
                stderr=subprocess.PIPE)
    log = r.stderr.decode(errors="replace").replace(iface, "<capture-interface>")
    (root / (role + "-capture.txt")).write_text(log)
    assert r.returncode in (0, 124), r.returncode
    assert (root / (role + ".pcap")).stat().st_size > 24
    return r.returncode


def watch():
    with (root / "controller.jsonl").open("wb") as out:
        r = ssh(controller, ["sudo", "-n", "timeout", str(duration + 3) + "s", "python3", "-B",
                             "/tmp/a624/a624_controller.py", ctl_if, "watch", str(duration), PAIRS],
                duration + 10, stdout=out, stderr=subprocess.PIPE)
    (root / "controller-errors.txt").write_bytes(r.stderr)
    assert r.returncode == 0, r.returncode
    return r.returncode


power_event = {}


def console():
    global last_console
    end = time.monotonic() + duration
    if kind == "dutcycle":
        return console_boot(end)
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


def console_boot(end):
    """Poll as usual; from the OUT0 off command read passively (every byte, timed) until the
    boot prompt has come back after the on command, then poll again."""
    global last_console
    fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    saved = termios.tcgetattr(fd)
    passive = booted = False
    try:
        tty.setraw(fd)
        attrs = termios.tcgetattr(fd)
        attrs[4] = attrs[5] = termios.B115200
        termios.tcsetattr(fd, termios.TCSANOW, attrs)
        with (root / "console.jsonl").open("w", buffering=1) as out, (root / "console-boot.jsonl").open("w", buffering=1) as boot:
            while time.monotonic() < end and not stop:
                if "off" in power_event and not passive and not booted:
                    passive, seen = True, ""
                    event("console-passive")
                if passive:
                    try:
                        ready, _, _ = select.select([fd], [], [], .05)
                        data = os.read(fd, 4096) if ready else b""
                    except BlockingIOError:
                        data = b""
                    except OSError as e:
                        # the adapter went away with the board's power: reopen it when it returns
                        event("console-error", error=str(e))
                        try:
                            os.close(fd)
                        except OSError:
                            pass
                        while not stop and time.monotonic() < end:
                            time.sleep(.2)
                            try:
                                fd = os.open(port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
                                tty.setraw(fd)
                                attrs = termios.tcgetattr(fd)
                                attrs[4] = attrs[5] = termios.B115200
                                termios.tcsetattr(fd, termios.TCSANOW, attrs)
                                event("console-reopened")
                                break
                            except OSError:
                                continue
                        data = b""
                    if True:
                        if data:
                            boot.write(json.dumps(dict(t=time.time(), data=data.decode("latin-1"))) + "\n")
                            if "on" in power_event:
                                seen += data.decode("ascii", errors="replace")
                    if "on" in power_event and "litex" in seen and seen.rstrip().endswith(">"):
                        time.sleep(.3)
                        passive, booted = False, True
                        event("console-polling")
                    continue
                start = time.monotonic()
                for cmd in CONSOLE:
                    t0, t1, raw = transact(fd, cmd)
                    out.write(json.dumps(dict(t=t0, end=t1, cmd=cmd, raw=raw)) + "\n")
                    if "litex" not in raw:
                        break
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
        r = ssh(controller, ["sudo", "-n", "timeout", "-s", "INT", "40s", "/tmp/a624/lptp/ptp4l",
                             "-f", "/tmp/a624/slave.cfg", "-i", ctl_if, "-m"], 50, stdout=out,
                stderr=subprocess.STDOUT)
    event("gm-prep-slave", rc=r.returncode)
    text = (root / "ptp4l-slave.log").read_text(errors="replace")
    rms = [int(m) for m in re.findall(r"rms\s+(\d+)\s+max", text)]
    mx = [int(m) for m in re.findall(r"max\s+(\d+)\s+freq", text)]
    event("gm-prep-converged", last_rms_ns=rms[-5:], last_max_ns=mx[-5:])
    assert len(rms) >= 5 and all(v < 1000 for v in mx[-5:]), "controller PHC did not converge"
    r = ssh(controller, ["sudo", "-n", "/tmp/a624/lptp/phc_ctl", ctl_if, "freq", "adj", GM_OFFSET,
                         "cmp"], 15, capture_output=True, text=True)
    event("gm-prep-offset", rc=r.returncode, offset_s=GM_OFFSET, output=r.stdout + r.stderr)
    assert r.returncode == 0


def gm_run():
    global gm_running
    gm_running = True
    event("gm-start", hold_s=HOLD)
    with (root / "ptp4l-gm.log").open("wb") as out:
        r = ssh(controller, ["sudo", "-n", "timeout", "-s", "INT", str(int(HOLD)) + "s",
                             "/tmp/a624/lptp/ptp4l", "-f", "/tmp/a624/gm.cfg", "-i", ctl_if, "-m"],
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
        if kind in ("cycle", "dutcycle", "gm"):
            time.sleep(PRE)
            assert time.monotonic() - last_console < 1, "console preflight failed"
            assert all(not f.done() for f in futures), "measurement exited before the action"
            assert (root / "tap.pcap").stat().st_size > 24, "tap not recording"
        if kind in ("cycle", "dutcycle"):
            try:
                power_event["off"] = time.time()
                power("off")
                status("off", initial=initial, out4="OFF")
                start = time.monotonic()
                while time.monotonic() - start < HOLD and not stop:
                    if kind == "cycle" and time.monotonic() - last_console > 2:
                        raise RuntimeError("DUT console lost during the outage")
                    time.sleep(.1)
            finally:
                if outlet_off:
                    power("on")
                    power_event["on"] = time.time()
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
