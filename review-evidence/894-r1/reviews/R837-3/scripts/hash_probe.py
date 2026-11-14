#!/usr/bin/env python3
"""Model of aecp_maps.c place(): count the slot visits (VISIT) an ADD of n distinct legal output keys
does in its build loop, for a geometry of S stream outputs of C channels (key = stream | channel << 16,
slot = (k + 9 * (k >> 16)) & 255, linear probing, no deletion). Reports the collision-free claim's
check and the worst case found by a greedy adversarial key choice, against 2(n + R) and n(n+1)/2."""
import itertools, sys

def slot(s, c):
    k = s | (c << 16)
    return (k + 9 * (k >> 16)) & 255

def visits(keys):
    table = {}          # slot -> key
    total = 0
    for key in keys:
        s = slot(*key)
        while True:
            total += 1
            if s not in table or table[s] == key:
                table.setdefault(s, key)
                break
            s = (s + 1) & 255
    return total

def distinct(S, C):
    seen = {}
    for s, c in itertools.product(range(S), range(C)):
        seen.setdefault(slot(s, c), []).append((s, c))
    return max(len(v) for v in seen.values())

def adversarial(S, C, n=63):
    keys = sorted(itertools.product(range(S), range(C)), key=lambda k: slot(*k))
    best = (0, None)
    for start in range(len(keys)):
        window = [keys[(start + j) % len(keys)] for j in range(n)]
        v = visits(window)
        if v > best[0]:
            best = (v, window[0])
    return best

for S, C in [(1, 8), (8, 8), (9, 28), (1, 256), (16, 8), (16, 32), (8, 32), (2, 32), (10, 8)]:
    most = distinct(S, C)
    n = min(63, S * C)
    v, _ = adversarial(S, C, n)
    print(f"streams {S:2d} x channels {C:3d}: keys per slot at most {most}; worst ADD of {n} distinct keys "
          f"(greedy window) {v} visits; 2(n+R) {2*n}; n(n+1)/2 {n*(n+1)//2}")
