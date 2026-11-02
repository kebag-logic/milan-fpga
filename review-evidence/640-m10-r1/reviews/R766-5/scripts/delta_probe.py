#!/usr/bin/env python3
"""Style and anchor probe for the changed lines of one Markdown page.

Usage: delta_probe.py REPO PAGE BASE_PAGE_FILE LINE [LINE ...]

Style: runs REPO/scripts/check_doc_style.py's analyze() on the page at head
and on BASE_PAGE_FILE and reports findings new at head.  A control plants an
11-word sentence on the first named prose line and must be caught.
Anchors: computes GitHub heading slugs for the page and checks every in-page
"#fragment" on the named lines; a mutant fragment must be reported MISSING.
Reads only; writes nothing to REPO.
"""
import importlib.util
import re
import sys
from collections import Counter


def slugs(text):
    seen, out = Counter(), set()
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m:
            continue
        s = m.group(2).lower()
        s = re.sub(r"[^\w\- ]", "", s)
        s = s.replace(" ", "-")
        n = seen[s]
        seen[s] += 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def main():
    repo, page, base_page = sys.argv[1:4]
    lines = [int(x) for x in sys.argv[4:]]
    spec = importlib.util.spec_from_file_location("cds", f"{repo}/scripts/check_doc_style.py")
    cds = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    sys.modules["cds"] = cds
    spec.loader.exec_module(cds)
    text = open(f"{repo}/{page}", encoding="utf-8").read()
    rows = text.splitlines()
    rc = 0

    base = open(base_page, encoding="utf-8").read()
    key = lambda f: (f.reason, " ".join(f.text.split()))
    before = Counter(key(f) for f in cds.analyze(base))
    after = Counter(key(f) for f in cds.analyze(text))
    new = after - before
    print(f"style: {sum(after.values())} findings at head, {sum(before.values())} at base; "
          f"new at head: {sum(new.values())}")
    for k in new:
        print("   NEW", k[0], k[1][:120])
        rc = 1
    prose = [n for n in lines if not rows[n - 1].startswith("|")]
    if prose:
        n = prose[0]
        mut = rows[:]
        mut[n - 1] = "One two three four five six seven eight nine ten eleven."
        planted = Counter(key(f) for f in cds.analyze("\n".join(mut) + "\n")) - after
        print(f"style control (11-word sentence planted at :{n}): "
              f"{'caught' if planted else 'NOT CAUGHT'}")
        rc |= 0 if planted else 1

    have = slugs(text)
    for n in lines:
        for frag in re.findall(r"\]\(#([^)\s]+)\)", rows[n - 1]):
            ok = frag in have
            print(f":{n} #{frag} {'resolves' if ok else 'MISSING'}")
            rc |= 0 if ok else 1
    ctl = "firmware-and-block-ram-ledgerx"
    print(f"anchor control #{ctl}: {'MISSING (as required)' if ctl not in have else 'RESOLVES (control failed)'}")
    rc |= 0 if ctl not in have else 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
