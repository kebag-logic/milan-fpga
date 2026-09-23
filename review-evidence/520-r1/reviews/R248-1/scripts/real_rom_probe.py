#!/usr/bin/env python3
"""Real-gate generated-ROM probe for #520, independent of the lane's wrapper.

The ROM change is made the way it happens in practice: a GENERATOR-ONLY change
inside a disposable tree copy (RTL, sv2v inputs, program, tools unchanged).
  gptp : gen_gptp_ucode.py is wrapped to pass a different --mac default
  ltn  : gen_ltn_rom.py is wrapped to rewrite one transition word (valid hex)
  ucode: gen_ucode.py is wrapped to rewrite the last hex word (valid hex)

Two trees are driven with identical steps:
  HEAD tree : exact head bytes
  BASE tree : exact head bytes with syn/yosys/run.sh and result_cache.py
              restored to the base commit (the pre-fix cache)

Every run is the shipping syn/yosys/run.sh on one real ROM-dependent top.
Receipts: per-step exit, PASS cells, "(result cache)" marker, refusal note,
wall time, and every cache record's text; an independent re-implementation of
the documented bundle framing is compared with each recorded rom_sha256.

usage: real_rom_probe.py HEAD_TREE BASE_TREE WORK TOP IMAGE [--head-only]
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

GEN = {
    "gptp": "gptp-processor/hdl/ucode/gen_gptp_ucode.py",
    "ltn": "protocol-processor/hdl/acmp/rom/gen_ltn_rom.py",
    "ucode": "protocol-processor/hdl/aecp/ucode/gen_ucode.py",
}
ALL_GENS = [("ltn_rom.hex", GEN["ltn"]), ("ucode.hex", GEN["ucode"]), ("gptp_ucode.hex", GEN["gptp"])]
WRAP = {
    "gptp": '''import os, sys
real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_gptp_ucode.real.py")
os.execv(sys.executable, [sys.executable, real, *sys.argv[1:], "--mac", "0x02A1B2C3D4E6"])
''',
    "ltn": '''import os, subprocess, sys
real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_ltn_rom.real.py")
rc = subprocess.run([sys.executable, real, *sys.argv[1:]]).returncode
if rc:
    sys.exit(rc)
out = sys.argv[sys.argv.index("-o") + 1]
text = open(out).read()
assert text.count("\\n00100129 ") == 1, "anchor word not unique"
open(out, "w").write(text.replace("\\n00100129 ", "\\n00100128 "))
''',
    "ucode": '''import os, re, subprocess, sys
real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_ucode.real.py")
rc = subprocess.run([sys.executable, real, *sys.argv[1:]]).returncode
if rc:
    sys.exit(rc)
out = sys.argv[sys.argv.index("-o") + 1]
lines = open(out).read().split("\\n")
idx = max(i for i, l in enumerate(lines) if re.fullmatch(r"[0-9A-Fa-f]+", l.strip()))
word = lines[idx].strip()
lines[idx] = word[:-1] + ("0" if word[-1] != "0" else "1")
open(out, "w").write("\\n".join(lines))
''',
}
PASS_RE = re.compile(r"^\s+\[PASS\]\s+(\S+)\s+cells=(\d+)(\s+\(result cache\))?\s*$", re.M)
NAMES = ("gptp_ucode.hex", "ltn_rom.hex", "ucode.hex")


def independent_digest(directory: Path) -> str:
    """The README/CI_WORKFLOWS framing, written from the prose, not the code."""
    blob = b""
    for name in sorted(NAMES):
        data = (directory / name).read_bytes()
        blob += name.encode("ascii") + b"\x00" + len(data).to_bytes(8, "big") + data
    return hashlib.sha256(blob).hexdigest()


class Tree:
    def __init__(self, root: Path, work: Path, label: str, top: str) -> None:
        self.root, self.work, self.label, self.top = root, work / label, label, top
        self.work.mkdir(parents=True, exist_ok=True)
        self.steps: list[dict] = []

    def run(self, step: str, flags: list[str]) -> dict:
        cmd = [str(self.root / "syn/yosys/run.sh"), "--top", self.top, "--no-structural",
               "--results", str(self.work / f"{step}.results"), *flags]
        start = time.monotonic()
        proc = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        (self.work / f"{step}.log").write_text(out)
        m = PASS_RE.search(out)
        rec = {"step": step, "flags": [f.replace(str(self.work.parent), "<work>") for f in flags],
               "exit": proc.returncode, "cells": int(m.group(2)) if m else None,
               "cache_hit": bool(m and m.group(3)),
               "refused_note": next((l.strip() for l in out.splitlines() if "cache entry refused" in l), ""),
               "seconds": round(time.monotonic() - start, 2)}
        self.steps.append(rec)
        print(f"[{self.label}] {step}: {rec}", flush=True)
        return rec

    def generated(self, tag: str) -> dict:
        d = self.work / f"roms-{tag}"
        d.mkdir(exist_ok=True)
        for name, gen in ALL_GENS:
            subprocess.run([sys.executable, str(self.root / gen), "-o", str(d / name)],
                           check=True, capture_output=True)
        return {"dir": d.name, "digest": independent_digest(d),
                "sha256": {n: hashlib.sha256((d / n).read_bytes()).hexdigest() for n in NAMES}}

    def swap(self, image: str, on: bool) -> None:
        gen = self.root / GEN[image]
        real = gen.with_name(gen.stem + ".real.py")
        if on:
            gen.rename(real)
            gen.write_text(WRAP[image])
        else:
            gen.unlink()
            real.rename(gen)


def records(cache: Path) -> dict:
    if not cache.is_dir():
        return {}
    return {e.name: (e / "record").read_text() for e in sorted(cache.iterdir()) if (e / "record").is_file()}


def ro(path: Path, on: bool) -> None:
    for p in [path, *path.rglob("*")]:
        mode = p.stat().st_mode
        p.chmod(mode & ~0o222 if on else mode | stat.S_IWUSR)


def tree_bytes(path: Path) -> dict:
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob("*")) if p.is_file()}


def main(argv: list[str]) -> int:
    head_root, base_root, work, top, image, *rest = argv
    head_root, base_root = str(Path(head_root).resolve()), str(Path(base_root).resolve())
    work = Path(work).resolve()
    head_only = "--head-only" in rest
    out: dict = {"top": top, "image": image}
    trees = [Tree(Path(head_root), work, "head", top)]
    if not head_only:
        trees.append(Tree(Path(base_root), work, "base", top))
    for t in trees:
        cache = t.work / "cache"
        t.run("A-cold", ["--cache", str(cache)])
        t.run("B-warm", ["--cache", str(cache)])
        out[f"{t.label}-roms-original"] = t.generated("original")
        seed = t.work / "seed"
        shutil.copytree(cache, seed)
        ro(seed, True)
        seed_before = tree_bytes(seed)
        t.swap(image, True)
        try:
            out[f"{t.label}-roms-changed"] = t.generated("changed")
            t.run("D-changed-cached", ["--cache", str(cache)])
            if t.label == "head":
                t.run("E-changed-uncached", [])
                t.run("F-changed-warm", ["--cache", str(cache)])
                t.run("G-changed-seed-only", ["--cache", str(t.work / "empty-head"), "--cache-seed", str(seed)])
        finally:
            t.swap(image, False)
        if t.label == "head":
            t.run("H-original-again", ["--cache", str(cache)])
            # foreign: the genuine changed-ROM entry planted at the original key
            recs = records(cache)
            orig_key = next(k for k, v in recs.items()
                            if f"rom_sha256={out['head-roms-original']['digest']}" in v)
            chg_key = next(k for k, v in recs.items()
                           if f"rom_sha256={out['head-roms-changed']['digest']}" in v)
            foreign = t.work / "foreign"
            foreign.mkdir()
            shutil.copytree(cache / chg_key, foreign / orig_key)
            t.run("I-foreign-entry-at-original-key", ["--cache", str(foreign)])
        out[f"{t.label}-seed-unchanged"] = tree_bytes(seed) == seed_before
        ro(seed, False)
        out[f"{t.label}-records"] = records(cache)
    if not head_only:
        head, base = trees
        # genuine schema-1 entries produced by the pre-fix code
        s1 = work / "schema1-seed"
        shutil.copytree(base.work / "cache", s1)
        ro(s1, True)
        head.run("J-schema1-seed", ["--cache", str(head.work / "empty-head-2"), "--cache-seed", str(s1)])
        ro(s1, False)
        planted = work / "schema1-planted"
        planted.mkdir()
        orig_key = next(k for k, v in out["head-records"].items()
                        if f"rom_sha256={out['head-roms-original']['digest']}" in v)
        (s1_entry,) = [e for e in s1.iterdir() if e.is_dir()]
        shutil.copytree(s1_entry, planted / orig_key)
        head.run("K-schema1-entry-at-current-key", ["--cache", str(planted)])
        out["schema1-record"] = (s1_entry / "record").read_text()
    for t in trees:
        out[f"{t.label}-steps"] = t.steps
    for t in trees:
        for key, text in out.get(f"{t.label}-records", {}).items():
            m = re.search(r"^rom_sha256=([0-9a-f]{64})$", text, re.M)
            if m:
                out.setdefault("digest-crosscheck", []).append(
                    {"tree": t.label, "key": key[:12], "rom_sha256": m.group(1),
                     "matches_independent_original": m.group(1) == out[f"{t.label}-roms-original"]["digest"],
                     "matches_independent_changed": m.group(1) == out[f"{t.label}-roms-changed"]["digest"]})
    text = json.dumps(out, indent=2).replace(str(work), "<work>")
    (work / f"probe-{top}-{image}.json").write_text(text + "\n")
    print(f"wrote probe-{top}-{image}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
