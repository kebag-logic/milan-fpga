#!/usr/bin/env python3
"""Wait until every named file's last line matches rc=N (or the file exists, with --exists), up to a limit in seconds.
usage: waitfor.py SECONDS [--exists] FILE...; prints each file's status at the end."""
import pathlib, re, sys, time
args = sys.argv[1:]
limit = float(args.pop(0))
exists = '--exists' in args
files = [pathlib.Path(a) for a in args if a != '--exists']
end = time.time() + limit
def done(p):
    if not p.exists():
        return False
    if exists:
        return True
    t = p.read_text(errors='replace').rstrip().splitlines()
    return bool(t and re.fullmatch(r'rc=\d+', t[-1]))
while time.time() < end and not all(done(p) for p in files):
    time.sleep(5)
for p in files:
    t = p.read_text(errors='replace').rstrip().splitlines() if p.exists() else ['(absent)']
    print(p.name, t[-1][:120])
