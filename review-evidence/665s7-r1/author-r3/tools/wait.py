"""wait.py SECONDS [--free N] [--file PATH PATTERN]...: return when N half-8 CPU ranges are free (cpu_ranges.py
show), or when every PATH holds PATTERN, or after SECONDS; prints what it saw. A foreground poll with no sleep
command."""
import re
import subprocess
import sys
import time

limit, args = float(sys.argv[1]), sys.argv[2:]
free, files = None, []
while args:
    if args[0] == "--free":
        free, args = int(args[1]), args[2:]
    else:
        files.append((args[1], args[2]))
        args = args[3:]
end = time.time() + limit
while True:
    seen = []
    ok_files = files and all(re.search(pat, open(p, errors="replace").read()) if __import__("os").path.exists(p)
                             else False for p, pat in files)
    show = subprocess.run([sys.executable, "$MANAGEMENT/2026-09-23/cpu_ranges.py", "show"],
                          capture_output=True, text=True).stdout.strip() if free else ""
    half = re.search(r"half8 \[(.*)\]", show)
    n_free = len([x for x in half.group(1).split(",") if x.strip()]) if half else 0
    if (free and n_free >= free) or ok_files or time.time() > end:
        print(time.strftime("%T"), "files" if ok_files else "", f"free half8: {n_free}" if free else "", show[:300])
        break
    time.sleep(20)
