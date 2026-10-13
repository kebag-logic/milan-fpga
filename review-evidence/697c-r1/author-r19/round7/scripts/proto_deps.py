"""Round-7 design prototype: replay a dependency pass (-M -MF, -H) for each recorded compile whose source still
exists, and report what the proposed rules would find on the clean tree. Scratch only; not the gate."""
import collections
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CAP, ROOT = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
STACK = ROOT / "third_party/tsn-c-stack"
DROP2 = {"-o", "--output", "-MF", "-MT", "-MQ", "-MJ"}
DROP1 = {"-M", "-MM", "-MD", "-MMD", "-MP", "-MG", "-P"}


def dep_args(args):
    out, i = [], 0
    while i < len(args):
        a = args[i]
        if a in DROP2:
            i += 2
            continue
        if a in DROP1 or (a.startswith("-o") and len(a) > 2) or re.fullmatch(r"-d[A-Z]+", a) or \
                (a[:3] in ("-MF", "-MT", "-MQ") and len(a) > 3):
            i += 1
            continue
        out.append(a)
        i += 1
    return out


def parse_deps(text):
    text = text.replace("\\\n", " ")
    rule = text.split(":", 1)[1] if ":" in text else ""
    words, cur, i = [], "", 0
    while i < len(rule):
        c = rule[i]
        if c == "\\" and i + 1 < len(rule) and rule[i + 1] in " #":
            cur += rule[i + 1]
            i += 2
            continue
        if c == "$" and rule[i + 1:i + 2] == "$":
            cur += "$"
            i += 2
            continue
        if c.isspace():
            if cur:
                words.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    if cur:
        words.append(cur)
    return words


def tree_of(err):
    return [(len(m[1]), m[2]) for m in re.finditer(r"^(\.+) (.*)$", err, re.M)]


def where(p):
    p = Path(p)
    if p.is_relative_to(STACK):
        return "public" if p.is_relative_to(STACK / "include") else "stack"
    if p.is_relative_to(ROOT):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith("sw/firmware/"):
            parts = rel.split("/")
            if parts[2] == "gtest" or "host" in parts[3:-1] or "test" in parts[3:-1]:
                return "equipment"
            return "firmware"
        return "checkout"
    return "outside"


recs = [json.loads(l) for l in open(CAP / "records.jsonl")]
seen = set()
counts = collections.Counter()
findings = collections.Counter()
work = Path(tempfile.mkdtemp(dir=os.environ.get("TMPDIR")))
for r in recs:
    if "bypass" in r or len(r["sources"]) != 1:
        continue
    src, lang, _ = r["sources"][0]
    if lang not in ("c", "c++") or not src.startswith(str(ROOT)):
        continue
    key = (tuple(r["args"]), r["cwd"])
    if key in seen:
        continue
    seen.add(key)
    dep = work / "d"
    real = r["real"]
    res = subprocess.run([real, *dep_args(r["args"]), "-M", "-MF", str(dep), "-H"], cwd=r["cwd"],
                         capture_output=True, text=True, env={**os.environ, "LC_ALL": "C"})
    if res.returncode:
        counts["failed"] += 1
        findings[("FAILED", where(src), res.stderr.strip().splitlines()[-1][:160] if res.stderr.strip() else "")] += 1
        continue
    words = [str((Path(r["cwd"]) / w).resolve()) for w in parse_deps(dep.read_text())]
    tree = [(d, str((Path(r["cwd"]) / p).resolve())) for d, p in tree_of(res.stderr)]
    counts["ok"] += 1
    side = where(src)
    if side in ("stack", "public"):
        side = "stack"
    stackp = [w for w in words if where(w) == "stack"]
    if side == "firmware":
        for w in stackp:
            findings[("fw-compile", Path(src).relative_to(ROOT).as_posix(), Path(w).relative_to(ROOT).as_posix())] += 1
    if side == "stack":
        own = {p for _, p in tree}
        for w in own:
            k = where(w)
            if k not in ("stack", "public", "outside"):
                findings[("stack-own", Path(src).name, w)] += 1
            if k == "outside" and not w.startswith(("/usr/", "$VALIDATION_TOOLS")):
                findings[("stack-own-outside", Path(src).name, w)] += 1
    # edges
    stackf = [str(ROOT / "x")]
    parents = [src]
    for d, p in tree:
        parents = parents[:d]
        inc = parents[-1]
        parents.append(p)
        ki, kp = where(inc), where(p)
        if ki == "firmware" and kp == "stack":
            findings[("edge-fw", Path(inc).relative_to(ROOT).as_posix(), Path(p).relative_to(ROOT).as_posix(), side)] += 1
        if ki in ("stack", "public") and kp not in ("stack", "public", "outside"):
            findings[("edge-stack", inc, p)] += 1
    counts[side] += 1
print(counts)
for k, v in sorted(findings.items(), key=lambda x: -x[1])[:80]:
    print(v, k)
