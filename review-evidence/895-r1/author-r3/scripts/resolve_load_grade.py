#!/usr/bin/env python3
"""resolve_load_grade.py FILE: resolve the three conflict hunks of load_grade.py on #895's merge of #810's round 30
head. Each `#:` comment block is theirs' with ours' sentence appended (given below, rewrapped at 120 columns); each
cost-table entry is the larger of the two sides' (both define each cost as "the larger of that measurement and this
table's"), in theirs' layout; a key on one side only refuses. Prints every key whose two sides differ."""
import re
import sys
import textwrap

path = sys.argv[1]
text = open(path).read()
pat = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", re.S | re.M)
kv = re.compile(r"'([^']+)': (\d+)")
shape = re.compile(r"'(\d+x\d+/\d+if)': \{")
ADDED = {
    1: "and again with SRP's Talker declarations (#895), every group of arm A, the answering-every-port arm, the "
       "valid-destinations arm and arm B's aecp group, each cost the larger of that and this table's: MAAP's record, a "
       "range lost to a peer's ANNOUNCE that restarts the core, 90 to 115 and 130 to 150 us, AECP's timer slot at "
       "1x1/1if 60 to 65, a TICK at 8x8/2if 40 to 45; on their merge each cost is the larger of the two sides' (#895).",
    3: "Again so with SRP's Talker declarations (#895, the pin's legs above): beside the pin's moves, the polls' base "
       "155 to 160 and 285 to 290 us, and at 1x1/1if ACMP's owed frame 120 to 125 and the registrar walk 20 to 25; on "
       "their merge each cost is the larger of the two sides' (#895).",
}


def table(block):
    out, cur = {}, None
    for line in block.splitlines():
        m = shape.search(line)
        if m:
            cur = m.group(1)
        for k, v in kv.findall(shape.sub("", line)):
            out.setdefault(cur, {})[k] = int(v)
    return out


def comment(block):
    return [l for l in block.splitlines() if l.startswith("#:")]


def rewrap(lines, added):
    """Theirs' comment lines, its last sentence-ending line joined with the added sentence, rewrapped."""
    words = " ".join(l[2:].strip() for l in lines)
    tail = ""
    # A comment block that ends mid-sentence into the next block ("... 32x32/2if") keeps that tail last.
    m = re.search(r"\. (\S+)$", words)
    if m and not words.endswith("."):
        words, tail = words[:m.start() + 1], m.group(1)
    body = f"{words} {added}" + (f" {tail}" if tail else "")
    return ["#: " + l for l in textwrap.wrap(body, width=117, break_on_hyphens=False, break_long_words=False)]


hunks = list(pat.finditer(text))
assert len(hunks) == 3, len(hunks)
res, last, diffs = [], 0, []
for n, m in enumerate(hunks, 1):
    ours, theirs = m.group(1), m.group(2)
    a, b = table(ours), table(theirs)
    if {s: set(v) for s, v in a.items()} != {s: set(v) for s, v in b.items()}:
        sys.exit(f"REFUSED: hunk {n}: shapes or keys differ")
    cur = [None]

    def mx(km):
        k, v = km.group(1), int(km.group(2))
        w = max(v, a[cur[0]][k])
        if v != a[cur[0]][k]:
            diffs.append(f"hunk {n} {cur[0]} {k}: ours {a[cur[0]][k]}, theirs {v} -> {w}")
        return f"'{k}': {w}"

    lines = []
    tc = comment(theirs)
    if n in ADDED:
        lines += rewrap(tc, ADDED[n])
    else:
        lines += tc
    for line in theirs.splitlines():
        if line.startswith("#:"):
            continue
        s = shape.search(line)
        if s:
            cur[0] = s.group(1)
            head, rest = line[:s.end()], line[s.end():]
            line = head + kv.sub(mx, rest)
        else:
            line = kv.sub(mx, line)
        lines.append(line)
    res.append(text[last:m.start()])
    res.append("\n".join(lines) + "\n")
    last = m.end()
res.append(text[last:])
out = "".join(res)
if re.search(r"^(<<<<<<<|=======$|>>>>>>>)", out, re.M):
    sys.exit("REFUSED: markers remain")
for l in out.splitlines():
    if len(l) > 120:
        sys.exit(f"REFUSED: line over 120 columns: {l[:80]}")
open(path, "w").write(out)
print("\n".join(diffs))
print(f"{len(diffs)} keys differ")
