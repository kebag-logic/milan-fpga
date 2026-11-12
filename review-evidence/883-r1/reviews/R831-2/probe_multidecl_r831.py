#!/usr/bin/env python3
"""Independent probe of check_cpp_idiom.py's multi-declarator rule.

Usage: python3 -I probe_multidecl_r831.py <path/to/check_cpp_idiom.py>

1. Oracle: counts declarators on one line by splitting on commas at brace,
   paren and angle depth 0 (after the declaration introducer), and compares
   real>1 with the rule's count on every corpus row.
2. Mutants: rebuilds the rule with earlier `_DECL_TEXT` bodies and reports
   which selftest-equivalent arms each one fails.
3. Timing: a long pathological line must scan in bounded time.
Exit status 0 only when every in-scope row agrees and every mutant is caught.
"""
import importlib.util
import re
import sys
import time

spec = importlib.util.spec_from_file_location("cci", sys.argv[1])
cci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cci)

BASE_E18 = r"(?:[^;(){}\n]|\{[^{}\n]*\})*"            # e18c8225: one level only
NO_BRACE = r"[^;()\n]*"                                 # before #495: braces ignored
TWO_DEEP = r"(?:[^;(){}\n]|\{(?:[^{}\n]|\{[^{}\n]*\})*\})*"


def oracle(line: str) -> int:
    """Declarators on a one-line declaration: top-level commas + 1."""
    m = re.match(rf"^[ \t]*{cci._DECL_TYPE}[ \t]+", line)
    if not m or not line.rstrip().endswith(";"):
        return 0
    depth = 0
    n = 1
    for ch in line[m.end():]:
        if ch in "{(<[":
            depth += 1
        elif ch in "})>]":
            depth -= 1
        elif ch == "," and depth == 0:
            n += 1
    return n


# (line, in_scope): in_scope False marks rows outside the rule's documented
# bound (four braces deep, parenthesised initialisers, template commas);
# they are reported, not graded.
CORPUS = [
    ("static long fails = 0, checks = 0;", True),
    ("static long fails = 0;", True),
    ("uint32_t adp_last_aidx[4] = {0, 0, 0, 0};", True),
    ("uint32_t a[2] = {0, 0}, b = 1;", True),
    ("int a{1}, b{2};", True),
    ("int m[2][2] = {{1, 2}, {3, 4}};", True),
    ("int m[2][2] = {{1, 2}, {3, 4}}, b = 0;", True),
    ("int n = 1, m[2][2] = {{0, 0}, {0, 0}};", True),
    ("int c[1][1][2] = {{{1, 2}}};", True),
    ("int c[1][1][2] = {{{1, 2}}}, d = 0;", True),
    ("int a = 0, b[2][2] = {{1, 2}, {3, 4}}, c = 5;", True),
    ("int m[2][2] = {{1, 2}, {3, 4}}, n[2][2] = {{5, 6}, {7, 8}};", True),
    ("  static const uint8_t t[2][3] = {{1, 2, 3}, {4, 5, 6}};", True),
    ("  static const uint8_t t[2][3] = {{1, 2, 3}, {4, 5, 6}}, *p = 0;", True),
    ("int x{}, y{};", True),
    ("int x = {}, y = {};", True),
    ("int m[2][2] = {{}, {}};", True),
    ("int m[2][2] = {{}, {}}, k;", True),
    ("CData v[2] = {1, 2};", True),
    ("CData v[2] = {1, 2}, w = 3;", True),
    ("int *p = 0, *q = 0;", True),
    ("unsigned s = {1}, t;", True),
    ("int c[1][1][1][2] = {{{{1, 2}}}};", False),
    ("int c[1][1][1][2] = {{{{1, 2}}}}, d = 0;", False),
    ("int a(1), b(2);", False),
    ("auto p = std::pair<int, int>{1, 2};", False),
]


def rule_count(pattern: re.Pattern, line: str) -> int:
    return len(pattern.findall(cci.blank_non_code(line + "\n")))


def build(text_body: str) -> re.Pattern:
    return re.compile(rf"^[ \t]*{cci._DECL_TYPE}[ \t]+\**[A-Za-z_]\w*{text_body},{text_body};[ \t]*$",
                      re.M)


def grade(pattern: re.Pattern, label: str) -> int:
    bad = 0
    for line, scoped in CORPUS:
        want = 1 if oracle(line) > 1 else 0
        got = rule_count(pattern, line)
        tag = "agree" if got == want else ("DISAGREE" if scoped else "out-of-bound")
        if got != want and scoped:
            bad += 1
        print(f"{label:9s} {tag:12s} real={oracle(line)} rule={got} want={want} | {line}")
    return bad


rc = 0
head_bad = grade(cci.MULTI_DECL_RE, "head")
print(f"head: {head_bad} in-scope disagreement(s)")
rc |= head_bad != 0
for name, body in (("base-e18", BASE_E18), ("no-brace", NO_BRACE), ("two-deep", TWO_DEEP)):
    bad = grade(build(body), name)
    print(f"mutant {name}: {bad} in-scope disagreement(s) -> {'CAUGHT' if bad else 'SURVIVED'}")
    rc |= bad == 0

for line in ("int a = " + "{" * 3000 + ";", "int a = " + "{0, " * 3000 + ";",
             "int a = 0" + ", b" * 5000 + " x", "int a = " + ", " * 5000):
    t0 = time.monotonic()
    rule_count(cci.MULTI_DECL_RE, line)
    dt = time.monotonic() - t0
    print(f"timing len={len(line)} {dt:.3f}s")
    rc |= dt > 5.0
print("PROBE", "PASS" if rc == 0 else "FAIL")
sys.exit(rc)
