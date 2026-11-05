#!/usr/bin/env python3
"""Set the CPU affinity of a process and all its descendants (every thread), so children
spawned later inherit it. Only for CPUs this lane's unit holds.
Usage: widen_affinity.py <root-pid> <cpu-list>"""
import os
import subprocess
import sys

root, cpus = int(sys.argv[1]), sys.argv[2]
allowed = set(range(64, 80))
want = set()
for part in cpus.split(','):
    a, _, b = part.partition('-')
    want |= set(range(int(a), int(b or a) + 1))
assert want <= allowed, f'{cpus} is outside the lane booking 64-79'
children = {}
for entry in os.listdir('/proc'):
    if entry.isdigit():
        try:
            fields = open(f'/proc/{entry}/stat').read().rsplit(')', 1)[1].split()
        except OSError:
            continue
        children.setdefault(int(fields[1]), []).append(int(entry))
todo, seen = [root], []
while todo:
    pid = todo.pop()
    seen.append(pid)
    todo.extend(children.get(pid, []))
done = 0
for pid in seen:
    if subprocess.run(['taskset', '-a', '-cp', cpus, str(pid)], capture_output=True).returncode == 0:
        done += 1
print(f'{done} of {len(seen)} processes now on {cpus}')
