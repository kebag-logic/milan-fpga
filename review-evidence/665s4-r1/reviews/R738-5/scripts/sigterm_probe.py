#!/usr/bin/env python3
"""sigterm_probe.py CHECKOUT MODE DELAY: run the firmware boundary gate as the kept attempt did and, DELAY seconds after
test_ctrl_firmware.py starts, send SIGTERM to that one PID (MODE=pid) or to the gate's whole process group (MODE=group).
Prints what the gate printed and its exit status, to compare with the kept log's shape."""
import os, signal, subprocess, sys, time
from pathlib import Path

checkout, mode, delay = sys.argv[1], sys.argv[2], float(sys.argv[3])
gate = subprocess.Popen([sys.executable, '-B', 'sw/firmware/ctrl/test/ctrl_boundary.py', '--require-rv32', '--selftest',
                         '--without', 'verilator'], cwd=checkout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, start_new_session=True)


def driver() -> int | None:
    """The pid of the gate's test_ctrl_firmware.py child, if it has started."""
    for entry in Path('/proc').iterdir():
        if entry.name.isdigit():
            try:
                argv = (entry / 'cmdline').read_bytes().split(b'\0')
                stat = (entry / 'stat').read_text().rsplit(')', 1)[1].split()
            except OSError:
                continue
            if int(stat[1]) == gate.pid and any(a.endswith(b'test_ctrl_firmware.py') for a in argv):
                return int(entry.name)
    return None


found = None
while found is None and gate.poll() is None:
    found = driver()
    time.sleep(0.2)
print(f'probe: driver pid {found}, gate pid {gate.pid}, same process group {os.getpgid(found) == gate.pid}', flush=True)
time.sleep(delay)
if mode == 'pid':
    os.kill(found, signal.SIGTERM)
else:
    os.killpg(gate.pid, signal.SIGTERM)
print(f'probe: SIGTERM sent to the {mode}', flush=True)
out, _ = gate.communicate(timeout=120)
print(out)
print(f'probe: gate exit status {gate.returncode}')
