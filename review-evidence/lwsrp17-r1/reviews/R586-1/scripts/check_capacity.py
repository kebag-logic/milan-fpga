# SPDX-License-Identifier: Apache-2.0
"""Check that every offered PDU in a transmit trace fits the caller's capacity.

Usage: check_capacity.py <trace>
"""
import sys

sends, calls = {}, {}
for line in open(sys.argv[1], encoding="ascii"):
    f = line.rstrip("\n").split("\t")
    key = (f[1], int(f[2]))
    if f[0] == "S":
        sends.setdefault(key, []).append(int(f[7]))
    else:
        calls[key] = int(f[5])
unmatched = [k for k in sends if k not in calls]  # a record longer than the shim buffer loses its newline
over = [(k, n, calls[k]) for k, lens in sends.items() if k in calls for n in lens if n > calls[k]]
print(f"opportunities: {len(calls)}; sends: {sum(map(len, sends.values()))}; unmatched: {unmatched}; over capacity: {len(over)}")
for (test, idx), n, cap in over[:20]:
    print(f"OVER {test}#{idx}: {n} octets > capacity {cap}")
sys.exit(int(bool(over)))
