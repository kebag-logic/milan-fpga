#!/usr/bin/env python3
"""Shared input check for the round-2 extraction scripts (PR #620, lane B1).

Every script reads raw captures from the retained raw root (a directory laid
out like the lane's raw index: <action>/<file> plus a few top-level files).
Before it extracts anything, it hashes each input and matches it:

  * against the findings pages' raw-artifact rows (action, file, bytes,
    SHA-256), when the file has a page row; and
  * against the round-1 raw index r1/RAW-ARTIFACTS.json in this packet,
    for every file.

A mismatch or a missing input stops the script with exit status 2. No
network, no bench access, no private value is printed.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PAGES = ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md")
ROLE_NAMES = {"alignment port log": "ptp4l-slave.log", "grandmaster port log": "ptp4l-gm.log"}
ROW_RE = re.compile(
    r"^\| (\w[\w-]*) \| (`[^`]+`|alignment port log|grandmaster port log) \| (\d+) \| `([0-9a-f]{64})` \|$",
    re.M)
PACKET = Path(__file__).resolve().parent.parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def page_rows(repo):
    """{relpath: (page, line, bytes, sha256)} from both pages' raw-artifact rows."""
    rows = {}
    for page in PAGES:
        text = (Path(repo) / page).read_text()
        for m in ROW_RE.finditer(text):
            action, art, size, digest = m.groups()
            name = ROLE_NAMES.get(art, art.strip("`"))
            line = text.count("\n", 0, m.start()) + 1
            rows[f"{action}/{name}"] = (Path(page).name, line, int(size), digest)
    return rows


def raw_index():
    d = json.loads((PACKET / "r1" / "RAW-ARTIFACTS.json").read_text())
    return {f["path"]: (f["bytes"], f["sha256"]) for f in d["files"]}


class Inputs:
    """Hash-check inputs once and print one INPUT line per file."""

    def __init__(self, raw_root, repo):
        self.raw = Path(raw_root)
        self.rows = page_rows(repo)
        self.index = raw_index()
        self.checked = {}

    def path(self, rel):
        if rel in self.checked:
            return self.checked[rel]
        p = self.raw / rel
        if not p.is_file():
            print(f"MISSING INPUT {rel}")
            sys.exit(2)
        size, digest = p.stat().st_size, sha256(p)
        idx = self.index.get(rel)
        if idx is None or idx != (size, digest):
            print(f"INPUT {rel} {size} {digest} index MISMATCH")
            sys.exit(2)
        row = self.rows.get(rel)
        if row is not None:
            if (row[2], row[3]) != (size, digest):
                print(f"INPUT {rel} {size} {digest} page row {row[0]}:{row[1]} MISMATCH")
                sys.exit(2)
            where = f"page row {row[0]}:{row[1]}"
        else:
            where = "no page row"
        print(f"INPUT {rel} {size} {digest} index ok, {where}")
        self.checked[rel] = p
        return p


def jsonl(path):
    with open(path) as f:
        return [json.loads(x) for x in f if x.strip()]


def status_fields(raw):
    """KEY=VALUE pairs of one milan_status answer."""
    return dict(re.findall(r"(\w+)=(\S+)", raw))


SWITCH_GM = "3cc0c6fffefe0210"  # public on the #387 page and in #117


def gm_role(gm):
    """Never print a host's clock identity: name the role instead."""
    if gm == SWITCH_GM:
        return "switch"
    if gm == "020000fffe000001":
        return "DUT"
    return "software-GM"
