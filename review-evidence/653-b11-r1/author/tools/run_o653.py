#!/usr/bin/env python3
"""Lane B11 (#653, new): one controller session of o653_probe with a tap capture around every
cycle. The caller holds the bench lock for the whole run (one locked action) and nothing
started here outlives it.

usage: run_o653.py <session> <plan>      plan: a comma list of cycles, each <tag>:<kind>[:ctl]
       kind aaf = the peer's AAF talker (STREAM_OUTPUT 0) to the DUT's STREAM_INPUT 0
       kind crf = the peer's CRF talker (STREAM_OUTPUT 2) to the DUT's STREAM_INPUT 1
       ctl      = the control: the probe sends its own GET_COUNTERS before the unbind
Endpoints come from the environment (the private file named by B11_ENV, sourced by the caller).

Sequence:
  1. tap capture <session>-enum starts; the probe starts on the controller host (sudo, under
     timeout) and enumerates both entities; the capture stops when both are online.
  2. per cycle: tap capture <session>-<tag> starts (tcpdump on a pty, ended with Ctrl-C), the
     probe runs the cycle (binding rule, bind, MEDIA_LOCKED wait, hold, [control GET_COUNTERS],
     unbind, post window, library snapshot), the capture stops.
  3. tap capture <session>-quit starts; the probe quits (session destroyed, then the
     deregistration); the capture stops.
  4. the pcaps are copied here, hashed on both hosts, and removed from the tap host; no tcpdump
     and no probe may be left running.
The hold before the unbind varies by cycle (2.0 to 3.0 s) so the unbind lands at different
phases of the DUT's one-per-second counters push.
Raw files (probe and driver logs, pcaps) go to B11_RAW; nothing here goes to the packet.
"""
import hashlib
import json
import os
import queue
import select
import subprocess
import sys
import threading
import time

E = os.environ
SESSION, PLAN = sys.argv[1], sys.argv[2]
RAW = E["B11_RAW"]
DUT, PEER = "020000fffe000001", E["PEER_EID"]
SESSION_PROGID, AUX_PROGID = 0x0B11, 0x0B12
BUDGET_S = 450
KIND = {"aaf": (0, 0, 2500), "crf": (2, 1, 3000)}  # talker STREAM_OUTPUT, listener STREAM_INPUT, post window ms
FILTER = "ether[40:2]=0x22f0 or ether[44:2]=0x22f0"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]
T0 = time.time()
dlog = open(f"{RAW}/{SESSION}-driver.jsonl", "a")


def log(**kw):
    kw = dict(t=round(time.time(), 6), **kw)
    dlog.write(json.dumps(kw) + "\n")
    dlog.flush()
    print(json.dumps(kw), flush=True)


class Cap:
    def __init__(self, name):
        self.name = name
        self.remote = f"/tmp/b11-a535-{SESSION}-{name}.pcap"
        cmd = f'sudo -n timeout -s INT 120 tcpdump -U -i {E["TAP_IFACE"]} -w {self.remote} "{FILTER}"'
        self.p = subprocess.Popen(SSH + ["-tt", E["TAP_HOST"], cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        self.buf = b""
        t = time.time()
        while time.time() - t < 15:
            r, _, _ = select.select([self.p.stdout], [], [], 0.2)
            if r:
                b = os.read(self.p.stdout.fileno(), 4096)
                if not b:
                    break
                self.buf += b
                if b"listening on" in self.buf:
                    break
        self.ok = b"listening on" in self.buf
        log(ev="cap_start", cap=name, ok=self.ok, after_s=round(time.time() - t, 3))

    def stop(self):
        time.sleep(0.3)
        t = time.time()
        try:
            self.p.stdin.write(b"\x03")
            self.p.stdin.flush()
            out, _ = self.p.communicate(timeout=10)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            self.p.kill()
            out, _ = self.p.communicate()
        txt = (self.buf + out).decode(errors="replace").replace("\r", "")
        summary = [ln for ln in txt.splitlines() if "packet" in ln]
        log(ev="cap_stop", cap=self.name, rc=self.p.returncode, after_s=round(time.time() - t, 3), summary=summary)


class Probe:
    def __init__(self):
        cmd = (f"cd /tmp/a535 && sudo -n timeout 540 ./o653_probe {E['CTL_IFACE']} {DUT} {PEER} "
               f"{SESSION_PROGID} {AUX_PROGID}")
        self.out = open(f"{RAW}/{SESSION}-probe.jsonl", "a")
        self.err = open(f"{RAW}/{SESSION}-probe.stderr", "a")
        self.p = subprocess.Popen(SSH + [E["CTL_HOST"], cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=self.err, text=True, bufsize=1)
        self.q = queue.Queue()
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        for line in self.p.stdout:
            self.out.write(line)
            self.out.flush()
            try:
                self.q.put(json.loads(line))
            except ValueError:
                pass
        self.q.put(None)

    def send(self, s):
        self.p.stdin.write(s + "\n")
        self.p.stdin.flush()

    def wait_for(self, pred, timeout):
        end = time.time() + timeout
        while time.time() < end:
            try:
                ev = self.q.get(timeout=max(0.05, end - time.time()))
            except queue.Empty:
                break
            if ev is None:
                return None
            if pred(ev):
                return ev
        return None


def main():
    log(ev="run_start", session=SESSION, plan=PLAN)
    cap = Cap("enum")
    if not cap.ok:
        cap.stop()
        log(ev="abort", why="tap capture did not start")
        return 3
    pr = Probe()
    on = pr.wait_for(lambda e: e.get("ev") == "both_online", 120)
    cap.stop()
    log(ev="online", ok=bool(on and on.get("ok")))
    results = []
    if on and on.get("ok"):
        for i, item in enumerate(PLAN.split(",")):
            parts = item.split(":")
            tag, kind, ctl = parts[0], parts[1], int(len(parts) > 2 and parts[2] == "ctl")
            if time.time() - T0 > BUDGET_S:
                log(ev="skip", tag=tag, why="budget")
                results.append(dict(tag=tag, result="SKIPPED_BUDGET"))
                continue
            t_out, l_in, post = KIND[kind]
            hold = 2000 + (i * 137) % 1000
            cap = Cap(tag)
            if not cap.ok:
                cap.stop()
                log(ev="skip", tag=tag, why="tap capture did not start")
                results.append(dict(tag=tag, result="SKIPPED_NO_CAPTURE"))
                continue
            pr.send(f"cycle {tag} {t_out} {l_in} {ctl} {hold} {post} 10000")
            end = pr.wait_for(lambda e: e.get("ev") == "cycle_end" and e.get("tag") == tag, 10 + hold / 1000 + post / 1000 + 20)
            cap.stop()
            results.append(dict(tag=tag, kind=kind, control=bool(ctl), hold_ms=hold, post_ms=post,
                                result=end.get("result") if end else "NO_CYCLE_END"))
            log(ev="cycle", **results[-1])
            if not end:
                break
    cap = Cap("quit")
    pr.send("quit")
    ex = pr.wait_for(lambda e: e.get("ev") == "exit", 40)
    cap.stop()
    try:
        pr.p.stdin.close()
        pr.p.wait(timeout=20)
    except subprocess.TimeoutExpired:
        pr.p.kill()
    log(ev="probe_exit", exit_seen=bool(ex), rc=pr.p.returncode)
    # pcaps: copy, hash both ends, remove from the tap host
    r = subprocess.run(SSH + [E["TAP_HOST"], f"cd /tmp && sha256sum b11-a535-{SESSION}-*.pcap"], capture_output=True,
                       text=True, timeout=30)
    remote = dict(reversed(ln.split()) for ln in r.stdout.splitlines() if ln.strip())
    r2 = subprocess.run(["scp", "-q", "-o", "BatchMode=yes", f"{E['TAP_HOST']}:/tmp/b11-a535-{SESSION}-*.pcap", RAW + "/"],
                        capture_output=True, text=True, timeout=120)
    hashes = {}
    for name, h in remote.items():
        local = os.path.join(RAW, name)
        lh = hashlib.sha256(open(local, "rb").read()).hexdigest() if os.path.exists(local) else None
        hashes[name] = dict(remote=h, local=lh, equal=(h == lh), bytes=os.path.getsize(local) if lh else None)
    log(ev="pcaps", scp_rc=r2.returncode, files=hashes)
    if hashes and all(v["equal"] for v in hashes.values()):
        r3 = subprocess.run(SSH + [E["TAP_HOST"], f"sudo -n rm -f /tmp/b11-a535-{SESSION}-*.pcap; ls /tmp/b11-a535-* 2>&1; "
                                                 "pgrep -af tcpdump; echo PGREP_RC=$?"],
                            capture_output=True, text=True, timeout=30)
        log(ev="tap_cleanup", out=r3.stdout.strip())
    r4 = subprocess.run(SSH + [E["CTL_HOST"], "pgrep -af '[o]653_probe'; echo PGREP_RC=$?"], capture_output=True, text=True,
                        timeout=30)
    log(ev="ctl_check", out=r4.stdout.strip())
    log(ev="run_end", results=results, elapsed_s=round(time.time() - T0, 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
