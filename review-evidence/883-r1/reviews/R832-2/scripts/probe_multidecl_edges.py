#!/usr/bin/env python3
"""Edge-case probe of check_cpp_idiom.py's MULTI_DECL_RE at a checkout.

Usage: python3 -I probe_multidecl_edges.py <checkout>

Read-only. Prints, for each one-line C++ declaration, how many declarators it
really has, the head verdict (1 = finding) and whether the verdict is the
right one; rows marked LIMIT are outside the rule's documented one-line,
three-deep scope and are reported, not scored. Ends with a timing check on
long comma-heavy lines that never match.
"""
import importlib.util
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cci", root / "scripts" / "check_cpp_idiom.py")
cci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cci)
RE = cci.MULTI_DECL_RE

# (line, real declarator count, in documented scope?)
CORPUS = [
    ("int a{}, b{};", 2, True),
    ("int a[2] = {}, b = 0;", 2, True),
    ("char s[] = {\"a,b\"}, t = 0;", 2, True),
    ("const char *s[2] = {\"a,b\", \"c,d\"};", 1, True),
    ("static const uint8_t t[2][3] = {{1, 2, 3}, {4, 5, 6}};", 1, True),
    ("  uint32_t m[2][2] = {{0, 0}, {0, 0}}, n = 1;  ", 2, True),
    ("int a[2] = {f(1, 2), 3};", 1, True),
    ("int a[2] = {f(1, 2), 3}, b = 0;", 2, True),
    ("int c[1][1][2] = {{{1, 2}}}, d[1][1][2] = {{{3, 4}}};", 2, True),
    ("int x = {1}, y = {2}, z = {3};", 3, True),
    ("WData w[2] = {0, 0}, v = 0;", 2, True),
    ("for (int i = 0, j = 1; i < j; ++i) {", 2, True),  # for-init, excluded by design
    ("g(a, b);", 0, True),
    ("int d[1][1][1][2] = {{{{1, 2}}}};", 1, False),
    ("int d[1][1][1][2] = {{{{1, 2}}}}, e = 0;", 2, False),
    ("int a[2] = {0,", 1, False),
]
print(f"{'real':>4} {'head':>4}  verdict  line")
bad = 0
for line, real, scoped in CORPUS:
    got = 1 if RE.search(line + "\n") else 0
    if line.startswith("for ") or line.startswith("g("):
        want = 0
    else:
        want = 1 if real > 1 else 0
    if not scoped:
        tag = "LIMIT" if got != want else "ok"
    else:
        tag = "ok" if got == want else "WRONG"
        bad += tag == "WRONG"
    print(f"{real:>4} {got:>4}  {tag:<7}  {line}")
print(f"in-scope wrong verdicts: {bad}")

for n in (200, 2000, 5000):
    for body in ("int a" + ", x" * n,
                 "int a = " + "{1, {2, {3, 4}}}, " * n,
                 "int a = {" + "1, " * n):
        t = time.perf_counter()
        RE.search(body + "\n")
        dt = time.perf_counter() - t
        print(f"timing n={n:<5} len={len(body):<7} {dt * 1000:9.1f} ms  {body[:24]!r}")
