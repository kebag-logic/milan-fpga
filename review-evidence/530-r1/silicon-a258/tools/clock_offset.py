#!/usr/bin/env python3
"""Remote-minus-local clock offset over one ssh session (issue 117, A202).

The build box is not NTP-synchronized, and each bench host stamps its own
artifacts (tap pcap host times, controller-host JSON, power-strip host log).
This puts them on the build-box timeline. One ssh session is opened; the
remote side answers each line on stdin with its time.time(). For every
exchange the local send/receive times bracket the remote stamp, so
offset = remote - (t_send + t_recv) / 2 with an error of at most rtt / 2.
The sample with the smallest round trip is reported.

usage: clock_offset.py <host> [<n>]   (prints one JSON line)
"""
import json
import statistics as st
import subprocess
import sys
import time

REMOTE = ("python3 -u -c 'import sys,time\n"
          "for l in sys.stdin:\n"
          "    print(repr(time.time()), flush=True)'")


def main() -> int:
    host = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    p = subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no", host, REMOTE],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    samples = []
    try:
        # warm-up exchange: the first answer includes interpreter start-up
        p.stdin.write("w\n")
        p.stdin.flush()
        p.stdout.readline()
        for _ in range(n):
            t0 = time.time()
            p.stdin.write("x\n")
            p.stdin.flush()
            r = float(p.stdout.readline())
            t1 = time.time()
            samples.append((t1 - t0, r - (t0 + t1) / 2, t0))
            time.sleep(0.02)
    finally:
        p.stdin.close()
        p.wait(timeout=10)
    samples.sort()
    best = samples[0]
    out = dict(host=host, n=len(samples), local_t=round(best[2], 6), rtt_ms=round(best[0] * 1e3, 3),
               offset_s=round(best[1], 6),
               offset_s_median_best5=round(st.median(s[1] for s in samples[:5]), 6),
               offset_s_spread_best5=round(max(s[1] for s in samples[:5]) - min(s[1] for s in samples[:5]), 6))
    print(json.dumps(out, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
