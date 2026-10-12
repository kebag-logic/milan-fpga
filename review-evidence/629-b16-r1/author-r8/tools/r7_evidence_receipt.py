#!/usr/bin/env python3
"""Lane B16, round 7: where the lane packet is published, reduced from the evidence branch's manifest.

usage: r7_evidence_receipt.py <repo> <evidence commit> <page commit> <out.json>

Round 6's r6_evidence_receipt.py, unchanged but for its name, this paragraph and its note: run at the
evidence commit b616e7ea, it reads author-r1/ to author-r6/, checks the section's hash rows at the page
commit e91a62ee against author-r6/, and compares author-r6/ with round 6's own MANIFEST.sha256.

Round 6's docstring follows.

Round 4's r4_evidence_receipt.py with three changes (round 6, R624-5-F3): it reads every author directory
the evidence commit holds, author-r1/ to author-r5/ at a73ce5c4; it checks the section's hash rows at the
page commit against the newest of them, author-r5/; and it compares each author-r5/ file's original SHA-256
in MANIFEST.json with the round's own MANIFEST.sha256, published in author-r5/.

Reads from the repository's object store only, so the evidence branch must be fetched:
  * review-evidence/629-b16-r1/MANIFEST.json at the evidence commit: its size and SHA-256, its entries per
    directory, the path-redacted files per directory, and whether any entry's two hashes differ without
    the path_redacted flag (or agree with it);
  * per author directory (author-r1/, author-r2/, author-r3/), the commit that last changed it at or before
    the evidence commit, and the page commit its subject names ("... at <commit>");
  * the findings page at the page commit, and every hash row of lane B16's section there that names a
    packet file (`| `<path>` ... | <bytes> | `<sha256>` |`): the row's bytes and SHA-256 beside the
    manifest's original and published SHA-256 for author-r3/<path>, the published blob's own size and
    SHA-256, and whether the file is path-redacted.
It refuses a manifest entry list with a duplicate file. Nothing on the bench is read or written.
"""
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter

REPO, EVC, PAGEC, OUT = sys.argv[1:5]
BASE = "review-evidence/629-b16-r1"
PAGE = "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
SECTION = "## Dev 5603c353, 2026-10-12: lane B16"
EV_ROW = re.compile(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|$")


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], check=True, capture_output=True).stdout


def blob(commit, path):
    return git("cat-file", "blob", f"{commit}:{path}")


def main():
    evc = git("rev-parse", "--verify", f"{EVC}^{{commit}}").decode().strip()
    pagec = git("rev-parse", "--verify", f"{PAGEC}^{{commit}}").decode().strip()
    raw = blob(evc, f"{BASE}/MANIFEST.json")
    man = json.loads(raw)
    files = [x["file"] for x in man]
    assert len(files) == len(set(files)), "duplicate manifest entry"
    by = {x["file"]: x for x in man}
    dirs = sorted(Counter(f.split("/")[0] for f in files).items())
    red = {d: sorted(x["file"] for x in man if x["file"].split("/")[0] == d and x["path_redacted"]) for d, _ in dirs}
    flag_agrees = all((x["original_sha256"] != x["published_sha256"]) == bool(x["path_redacted"]) for x in man)

    archives = {}
    authors = [d for d, _ in dirs if re.fullmatch(r"author-r\d", d)]
    last = authors[-1]
    for d in authors:
        h, s = git("log", "-1", "--format=%H%x00%s", evc, "--", f"{BASE}/{d}").decode().strip().split("\0")
        archives[d] = dict(commit=h, subject=s, page_commit=re.search(r" at ([0-9a-f]{8})$", s).group(1))

    doc = blob(pagec, PAGE).decode().splitlines()
    s = next(i for i, x in enumerate(doc) if x.startswith(SECTION))
    e = next((i for i in range(s + 1, len(doc)) if doc[i].startswith("## ")), len(doc))
    rows = []
    for i in range(s, e):
        m = EV_ROW.match(doc[i].strip())
        if not m:
            continue
        path, nbytes, digest = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
        ent = by.get(f"{last}/{path}")
        pub = blob(evc, f"{BASE}/{last}/{path}") if ent else b""
        r = dict(line=i + 1, file=path, row_bytes=nbytes, row_sha256=digest, in_manifest=ent is not None,
                 original_sha256=ent and ent["original_sha256"], published_sha256=ent and ent["published_sha256"],
                 path_redacted=ent and ent["path_redacted"], blob_bytes=len(pub), blob_sha256=hashlib.sha256(pub).hexdigest())
        r["all_equal"] = bool(ent) and digest == ent["original_sha256"] == ent["published_sha256"] == r["blob_sha256"] \
            and nbytes == len(pub)
        rows.append(r)

    # round 6: the newest directory's files against that round's own MANIFEST.sha256, published beside them
    own = {p.removeprefix("./"): h for h, p in (x.split("  ", 1) for x in blob(evc, f"{BASE}/{last}/MANIFEST.sha256").decode().splitlines() if x)}
    mine = {x["file"][len(last) + 1:]: x for x in man if x["file"].startswith(last + "/")}
    own_cmp = dict(files=len(mine), listed=len(own), equal=sum(1 for f, x in mine.items() if own.get(f) == x["original_sha256"]),
                   unlisted=sorted(f for f in mine if f not in own and f != "MANIFEST.sha256"),
                   missing=sorted(f for f in own if f not in mine))
    out = dict(
        note="Lane B16 round 7: the published packet's location, reduced from the evidence branch; offline, no bench action",
        evidence_branch="629-b16-review-evidence", evidence_commit=evc, manifest=f"{BASE}/MANIFEST.json",
        manifest_bytes=len(raw), manifest_sha256=hashlib.sha256(raw).hexdigest(), manifest_entries=len(man),
        entries_per_dir=dict(dirs), path_redacted_per_dir={d: len(v) for d, v in red.items()},
        path_redacted_author=sum(len(v) for d, v in red.items() if d.startswith("author-")),
        path_redacted_files=red, hashes_differ_exactly_when_redacted=flag_agrees, archives=archives,
        rows_checked_against=f"{last}/", own_manifest=own_cmp,
        page_commit=pagec, page_rows=dict(rows=len(rows), in_manifest=sum(r["in_manifest"] for r in rows),
                                          all_equal=sum(r["all_equal"] for r in rows),
                                          path_redacted=sum(bool(r["path_redacted"]) for r in rows)),
        rows=rows)
    with open(OUT, "w") as f:
        f.write(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("evidence_commit", "manifest_sha256", "manifest_entries", "entries_per_dir",
                                          "path_redacted_per_dir", "hashes_differ_exactly_when_redacted", "page_rows")}))
    print(json.dumps(dict(archives={d: (a["commit"][:8], a["page_commit"]) for d, a in archives.items()}, own_manifest=own_cmp)))
    return 0 if flag_agrees and out["page_rows"]["all_equal"] == len(rows) and own_cmp["equal"] == own_cmp["files"] - (
        "MANIFEST.sha256" in mine) and not own_cmp["missing"] else 1


if __name__ == "__main__":
    sys.exit(main())
