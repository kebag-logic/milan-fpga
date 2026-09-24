#!/usr/bin/env python3
"""Build-box clock minus controller-host clock over one ssh session (issue 529, A231).
usage: a231_clock_offset.py <ssh_alias> [n]"""
import subprocess, sys, time
alias, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 15
p = subprocess.Popen(["ssh", "-o", "BatchMode=yes", alias, "while read l; do date +%s.%N; done"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
best = None
for _ in range(n):
    t0 = time.time(); p.stdin.write("x\n"); p.stdin.flush(); r = float(p.stdout.readline()); t1 = time.time()
    off, rtt = r - (t0 + t1) / 2, t1 - t0
    print(f"remote_minus_local_s={off:+.4f} rtt_s={rtt:.4f}")
    if best is None or rtt < best[1]:
        best = (off, rtt)
p.stdin.close(); p.wait()
print(f"BEST remote_minus_local_s={best[0]:+.4f} rtt_s={best[1]:.4f} at_local={time.strftime('%FT%TZ', time.gmtime())}")
