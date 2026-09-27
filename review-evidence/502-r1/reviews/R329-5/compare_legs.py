#!/usr/bin/env python3
"""Compare pp_shadow check streams of two builds: values must match, labels may differ."""
import re, sys
LINE = re.compile(r'^\s*\[(PASS|FAIL)\]\s+(.*?)\s+got=(0x[0-9A-Fa-f]+)\s+exp=(0x[0-9A-Fa-f]+)\s*$')

def checks(path):
    out = []
    with open(path, errors='replace') as fh:
        for raw in fh:
            m = LINE.match(raw.rstrip('\n'))
            if m:
                out.append((m.group(1), m.group(2), m.group(3), m.group(4)))
    return out

def main(old, new):
    a, b = checks(old), checks(new)
    status = 0
    print(f"old {old}: {len(a)} checks; new {new}: {len(b)} checks")
    if len(a) != len(b):
        print("COUNT MISMATCH"); return 1
    renamed = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if (x[0], x[2], x[3]) != (y[0], y[2], y[3]):
            print(f"VALUE MISMATCH at {i}: {x} vs {y}"); status = 1
        elif x[1] != y[1]:
            renamed += 1
            print(f"label {i}: {x[1]!r} -> {y[1]!r}")
    print(f"verdict/got/exp identical at every position: {status == 0}; relabelled: {renamed}")
    return status

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
