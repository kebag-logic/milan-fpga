#!/usr/bin/env python3
"""R420-5: does the linked round-4 body hold rounds 1-4's validation sections
verbatim, with every figure R420-4's receipt listed as dropped?

usage: verify_linked_tables.py EVDIR R420_4_DROPPED_RECEIPT
EVDIR holds <ref>/<dir>__PR-BODY.md files and live-body.md (fetch_evidence.sh).

Checks, each printed with PASS/FAIL:
 A. Each round's "Validation" section (heading to the next heading of the same
    or a higher level) in the source body is byte-identical to the same
    section of the linked body (author-r4 at ca502628). Sources: the body
    that first carried the round (author, author-r2, author-r3, author-r4) and
    the last full body before condensing (author-r3 for rounds 1-3,
    author-r4 for round 4).
 B. R420-4's figure comparison (the same NUM regex as figures_dropped.py),
    per round section: every bare number of the source round section appears
    in the linked body's same round section. Expected: none missing.
 C. Every entry of R420-4's dropped-figures receipt ("[Round N] fig: ...ctx...")
    is found in the linked body's same round section, both as the bare figure
    and with its quoted context (the receipt's ... context ... string, minus
    the ellipses, must occur verbatim in that section, whitespace-normalised
    the same way the receipt was written: newlines -> spaces).
 D. Each condensed validation section of the live body opens (first non-empty
    line after the heading) with the pointer naming the same section, and the
    link definition points at author-r4/PR-BODY.md at commit ca502628...
"""
import re, sys, os, hashlib

NUM = re.compile(r"(?<![\w.`])\d{1,3}(?:,\d{3})+(?![\w])|(?<![\w.`])\d+(?:\.\d+)?(?![\w`])")
ev, receipt = sys.argv[1], sys.argv[2]
LINKED = os.path.join(ev, "ca502628", "author-r4__PR-BODY.md")
def body(ref, d): return open(os.path.join(ev, ref, f"{d}__PR-BODY.md")).read()
fails = 0
def report(ok, msg):
    global fails
    fails += (not ok)
    print(("PASS " if ok else "FAIL ") + msg)

def rounds(text):  # same split as R420-4's figures_dropped.py
    out, cur = {}, "Round 1"
    for line in text.splitlines(keepends=True):
        m = re.match(r"^## (Round 4b|Round 4|Round 3|Round 2)\b", line)
        if m: cur = m.group(1)
        out.setdefault(cur, []).append(line)
    return {k: "".join(v) for k, v in out.items()}

def section(text, heading):
    lines = text.splitlines(keepends=True)
    lvl = None
    for i, l in enumerate(lines):
        if l.rstrip("\n") == heading:
            lvl = len(heading) - len(heading.lstrip("#")); start = i; break
    if lvl is None: return None
    for j in range(start + 1, len(lines)):
        m = re.match(r"^(#+) ", lines[j])
        if m and len(m.group(1)) <= lvl: return "".join(lines[start:j])
    return "".join(lines[start:])

linked = open(LINKED).read()
print(f"linked body sha256 {hashlib.sha256(linked.encode()).hexdigest()}")
VAL = {"Round 1": "## Validation", "Round 2": "### Validation, round 2",
       "Round 3": "### Validation, round 3", "Round 4": "### Validation, round 4"}
FIRST = {"Round 1": "author", "Round 2": "author-r2", "Round 3": "author-r3", "Round 4": "author-r4"}
LAST = {"Round 1": "author-r3", "Round 2": "author-r3", "Round 3": "author-r3", "Round 4": "author-r4"}

print("== A. validation sections verbatim in the linked body")
for rnd, h in VAL.items():
    ls = section(linked, h)
    tables = sum(1 for l in (ls or "").splitlines() if l.startswith("|---") or l.startswith("|--"))
    rows = sum(1 for l in (ls or "").splitlines() if l.startswith("|"))
    for kind, d in (("first", FIRST[rnd]), ("last-full", LAST[rnd])):
        s = section(body("2a98e7d4", d), h)
        report(s is not None and ls is not None and s == ls,
               f"{rnd} '{h}': {kind} body {d} == linked ({len(s or '')} bytes, linked {len(ls or '')} bytes)")
    print(f"     linked section: {tables} table(s), {rows} table lines")

print("== B. R420-4 figure comparison, source round section -> linked round section")
for rnd, d in LAST.items():
    old, new = rounds(body("2a98e7d4", d))[rnd], rounds(linked)[rnd]
    have = set(NUM.findall(new))
    missing = sorted({n for n in NUM.findall(old) if n not in have})
    report(not missing, f"{rnd}: {len(set(NUM.findall(old)))} distinct figures in {d}, missing from linked: {missing}")
    # author-r3 ends the file after round 3; in the linked body one blank line
    # separates round 3 from "## Round 4". Allow exactly that separator.
    tail = new[len(old):] if new.startswith(old) else None
    report(tail in ("", "\n"), f"{rnd}: whole round section of {d} byte-identical to linked "
           f"({len(old)} bytes; linked adds {tail!r} as the separator before the next round)")

print("== C. every R420-4 dropped entry present in the linked body's round section")
lr = rounds(linked)
norm = {k: v.replace("\n", " ") for k, v in lr.items()}
n = bad = 0
for line in open(receipt):
    m = re.match(r"^\[(Round \w+)\] ([\d.,]+): \.\.\.(.*)\.\.\.$", line.rstrip("\n"))
    if not m: continue
    rnd, fig, ctx = m.groups()
    n += 1
    okf = fig in set(NUM.findall(lr.get(rnd, "")))
    okc = ctx in norm.get(rnd, "")
    if not (okf and okc):
        bad += 1; print(f"     MISSING [{rnd}] {fig} figure={okf} context={okc}")
report(n > 0 and bad == 0, f"{n} dropped entries checked, {bad} not found (figure and verbatim context)")

print("== D. live body pointers")
live = open(os.path.join(ev, "live-body.md")).read()
for rnd, h in VAL.items():
    s = section(live, h) or ""
    first = next((l for l in s.splitlines()[1:] if l.strip()), "")
    name = h.lstrip("# ")
    exp = (f'This round\'s tables, verbatim with every figure, are in the archived round-4 body, '
           f'section "{name}" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.')
    report(first == exp, f"{rnd}: '{h}' opens with the pointer naming \"{name}\"")
defs = re.findall(r"^\[c6-r1-r4-tables\]: (\S+)\s*$", live, re.M)
url = ("https://github.com/kebag-logic/milan-fpga/blob/ca50262850d156308a45ce5237e9adff64419f89/"
       "review-evidence/ppC6-r1/author-r4/PR-BODY.md")
report(defs == [url], f"one link definition, to {url}: {defs}")
uses = len(re.findall(r"\[full tables\]\[c6-r1-r4-tables\]", live))
report(uses == 4, f"reference used {uses} times (expected 4)")
print(f"TOTAL FAIL {fails}")
sys.exit(1 if fails else 0)
