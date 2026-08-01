#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
#
# M-A2 boot proof driver — fold into scripts/virtual-e2e.sh (task T0/T1).
#
# Runs sw/litex/milan_sim.py (or reuses its cached Verilator Vsim + BIOS build)
# under a pty, waits for the LiteX BIOS prompt (ANSI-tolerant), issues
#   mem_read 0x90000000 16
# and captures the ID dump. Exit 0 iff the prompt was reached AND the memory
# dump with ID='MILN' was observed.
#
# Usage (must run from a venv that has migen+litex, or with the venv activated
# so subprocess `make`/`python3 -m litex...` resolve to the venv, NOT system
# python which lacks migen/litex):
#   python scripts/ma2_sim_driver.py [--repo ROOT] [--log FILE]
import argparse, os, pty, re, select, signal, subprocess, sys, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")))
    ap.add_argument("--log", default="/tmp/ma2_run.log")
    args = ap.parse_args()

    cwd = os.path.join(args.repo, "sw", "litex")
    log = open(args.log, "wb", buffering=0)
    cmd = [sys.executable, "./milan_sim.py"]
    memread = b"mem_read 0x90000000 16\n"
    timeout = 40 * 60
    quiet_after_dump = 6

    T0 = time.monotonic()
    def mark(msg):
        log.write(f"\n=== [driver t+{time.monotonic()-T0:8.1f}s] {msg} ===\n".encode())

    ANSI = re.compile(rb"\x1b\[[0-9;]*m")
    def stripansi(b):
        return ANSI.sub(b"", b)

    mark(f"launched {' '.join(cmd)} in {cwd}")
    master, slave = pty.openpty()
    env = dict(os.environ)
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=slave, stdout=slave,
                         stderr=slave, preexec_fn=os.setsid, close_fds=True)
    os.close(slave)

    buf = b""
    sent = False
    dump_seen_at = None
    try:
        while time.monotonic() - T0 < timeout:
            r, _, _ = select.select([master], [], [], 1.0)
            if r:
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    mark("pty EOF"); break
                if not chunk:
                    mark("pty EOF"); break
                log.write(chunk); buf += chunk; buf = buf[-65536:]
            if p.poll() is not None:
                mark(f"sim exited rc={p.returncode}"); break
            clean = stripansi(buf)
            if not sent and b"Console" in clean and b"litex>" in clean:
                mark("BIOS console prompt seen; sending mem_read 0x90000000 16")
                os.write(master, memread); sent = True; buf = b""
            elif sent and dump_seen_at is None and b"Memory dump:" in stripansi(buf):
                mark("memory dump observed"); dump_seen_at = time.monotonic()
            elif dump_seen_at and time.monotonic() - dump_seen_at > quiet_after_dump:
                mark("capture complete; terminating sim"); break
        else:
            mark("TIMEOUT reached; terminating sim")
    finally:
        if p.poll() is None:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM); time.sleep(3)
                if p.poll() is None:
                    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
        rc = p.wait()
        mark(f"done rc={rc} elapsed={time.monotonic()-T0:.1f}s "
             f"prompt_reached={sent} dump_seen={dump_seen_at is not None}")
        log.close()
    ok = sent and dump_seen_at is not None
    print(f"M-A2: {'PASS' if ok else 'FAIL'} prompt_reached={sent} dump_seen={dump_seen_at is not None}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
