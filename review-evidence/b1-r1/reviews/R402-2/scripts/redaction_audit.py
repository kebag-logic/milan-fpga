#!/usr/bin/env python3
"""Audit the round-1 packet republished redacted under author-r2/r1/ against the original.

For every entry of author-r2/r1/REDACTION.json:
  * original_sha256 must equal the round-1 file at the original archive commit,
    either directly or through that archive's MANIFEST.json when its archiver
    path-redacted the file (an excluded binary the original archive never
    carried is checked for absence only);
  * published_sha256 must equal the republished file, directly or through the
    new archive's MANIFEST.json path-redaction record;
  * an unredacted entry must be byte-identical to the original;
  * a redacted entry must differ from the original ONLY where a <placeholder>
    stands, line by line, so no measured value was altered by the redaction.
The values the placeholders replaced are collected (never printed) and the
whole published archive tree is scanned for each of them, case-insensitively.

usage: redaction_audit.py <original-archive-b1-r1-dir> <new-archive-b1-r1-dir>
The original archive holds author/, the new one author-r2/r1/; the whole new
archive directory is the scanned tree.
"""
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PH = re.compile(r"<[a-z0-9-]+>")
FAILS = []


def check(cond, label):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        FAILS.append(label)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    old_root, new_root = map(Path, sys.argv[1:3])
    orig, pub, tree = old_root / "author", new_root / "author-r2" / "r1", new_root
    old_man = {x["file"][len("author/"):]: x for x in json.loads((old_root / "MANIFEST.json").read_text())
               if x["file"].startswith("author/")}
    new_man = {x["file"][len("author-r2/r1/"):]: x for x in json.loads((new_root / "MANIFEST.json").read_text())
               if x["file"].startswith("author-r2/r1/")}
    entries = json.loads((pub / "REDACTION.json").read_text())
    archiver = 0
    values = defaultdict(set)
    n_same = n_red = n_exc = 0
    for e in entries:
        o, p = orig / e["file"], pub / e["file"]
        if "excluded" in e:
            n_exc += 1
            if p.exists():
                check(False, f"excluded file present: {e['file']}")
            continue
        om, nm = old_man.get(e["file"]), new_man.get(e["file"])
        if not o.is_file() or om is None or sha(o) != om["published_sha256"] or om["original_sha256"] != e["original_sha256"]:
            check(False, f"original hash of {e['file']}")
            continue
        if not p.is_file() or nm is None or sha(p) != nm["published_sha256"] or nm["original_sha256"] != e["published_sha256"]:
            check(False, f"published hash of {e['file']}")
            continue
        archiver += om["original_sha256"] != om["published_sha256"] or nm["original_sha256"] != nm["published_sha256"]
        if not e["redacted"]:
            n_same += 1
            if om["path_redacted"] != nm["path_redacted"]:
                check(False, f"archiver path redaction differs between archives: {e['file']}")
            if o.read_bytes() != p.read_bytes():
                check(False, f"unredacted file differs: {e['file']}")
            continue
        n_red += 1
        ol, pl = o.read_text().splitlines(), p.read_text().splitlines()
        if len(ol) != len(pl):
            check(False, f"line count changed: {e['file']}")
            continue
        for a, b in zip(ol, pl):
            if a == b:
                continue
            parts = PH.split(b)
            names = PH.findall(b)
            if not names:
                check(False, f"line changed without a placeholder: {e['file']}")
                break
            rx = "".join(re.escape(s) + ("(.+?)" if i < len(names) else "") for i, s in enumerate(parts))
            m = re.fullmatch(rx, a)
            if not m:
                check(False, f"line differs outside its placeholders: {e['file']}")
                break
            for name, v in zip(names, m.groups()):
                # a span that already held a placeholder, or the null MAC, discloses nothing
                if not PH.fullmatch(v) and v != "00:00:00:00:00:00":
                    values[name].add(v)
    listed = {e["file"] for e in entries if "excluded" not in e}
    on_disk = {q.relative_to(orig).as_posix() for q in orig.rglob("*") if q.is_file()}
    check(listed == on_disk, f"REDACTION.json lists every file of the original archive ({len(on_disk)}), plus {n_exc} excluded")
    print(f"files the archiver path-redacted in either archive: {archiver}")
    extra = {q.relative_to(pub).as_posix() for q in pub.rglob("*") if q.is_file()} - listed - {"REDACTION.json", "MANIFEST.sha256"}
    check(not extra, f"no republished file outside the record (extra: {len(extra)})")
    print(f"entries: {len(entries)}; byte-identical {n_same}, redacted {n_red}, excluded {n_exc}")
    check(n_same + n_red + n_exc == len(entries) and not FAILS, "every entry accounted for; redactions touch placeholders only")
    for name in sorted(values):
        print(f"placeholder {name}: {len(values[name])} distinct original value(s)")
    hits = defaultdict(list)
    for q in sorted(tree.rglob("*")):
        if not q.is_file():
            continue
        low = q.read_bytes().lower()
        for name, vs in values.items():
            for v in vs:
                c = low.count(v.lower().encode())
                if c:
                    hits[name].append(f"{q.relative_to(tree).as_posix()} x{c}")
    for name in sorted(values):
        print(f"scan of the published tree for {name} originals: {len(hits[name])} files{': ' + ', '.join(hits[name]) if hits[name] else ''}")
    print(f"\nTOTAL fail={len(FAILS)} scan-hit-files={sum(len(v) for v in hits.values())}")
    sys.exit(1 if FAILS or hits else 0)


if __name__ == "__main__":
    main()
