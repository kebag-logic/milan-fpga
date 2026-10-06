#!/usr/bin/env python3
"""Probe (R506-1): each base check's condition next to the head assertion that
carries its words, normalised (whitespace, static_cast, 1u/1 suffixes), for a
reader to compare. Prints only the pairs whose normalised texts differ.
Usage: port_conditions.py <repo> <base> <head>"""
import re, subprocess, sys
repo, base, head = sys.argv[1:4]
def show(rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True).stdout
def args_after(text, start):
    depth, i = 1, start
    while depth and i < len(text):
        c = text[i]
        if c == '"':
            i += 1
            while text[i] != '"':
                i += 2 if text[i] == "\\" else 1
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        i += 1
    return text[start:i - 1]
def norm(s):
    s = re.sub(r"static_cast<[^>]*>", "", s)
    s = re.sub(r"\(\s*(?:uint\d+_t|unsigned|int|bool)\s*\)", "", s)
    s = re.sub(r"(\d)u\b", r"\1", s)
    s = s.replace("nullptr", "NULL").replace("true", "1").replace("false", "0")
    return re.sub(r"[\s()]", "", s)
pairs = {"sw/firmware/ctrl/test/test_adp.c": "sw/firmware/ctrl/test/test_adp.cpp",
         "sw/firmware/ctrl/test/test_port_loop.c": "sw/firmware/ctrl/test/test_port_loop.cpp"}
call = re.compile(r'\b(check|check_eq|bound)\(\s*"((?:[^"\\]|\\.)*)"\s*,')
for old, new in pairs.items():
    src, dst = show(base, old), show(head, new)
    diff = 0
    for m in call.finditer(src):
        kind, words = m.group(1), m.group(2)
        cond = args_after(src, m.end())
        if kind == "bound":
            continue
        at = dst.find(f'"{words}"')
        # the assertion statement that ends with this message
        stmt_start = max(dst.rfind(";", 0, at), dst.rfind("{", 0, at), dst.rfind("}", 0, at)) + 1
        stmt = dst[stmt_start:at]
        e = re.search(r"(EXPECT|ASSERT)_(\w+)\(", stmt)
        if e is None:
            print(f"{old}: no assertion before {words!r}: {stmt.strip()[:160]}"); diff += 1; continue
        got = args_after(stmt, e.end())
        want = norm(cond) if kind == "check" else norm(cond.replace(",", "==", 1))
        have = norm(got.replace(",", "==", 1) if e.group(2) in ("EQ",) else got)
        if e.group(2) == "FALSE":
            have = "!" + have
        if want != have:
            diff += 1
            print(f"--- {words}\n    base {kind}: {cond.strip()[:200]}\n    head {e.group(0)}{got.strip()[:200]})")
    print(f"{old}: {diff} pairs differ after normalisation")
