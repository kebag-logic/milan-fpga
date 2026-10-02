#!/usr/bin/env python3
"""Regenerate ucode.hex from gen_ucode.py at several revisions and compare.

For each revision the generator is extracted with `git show`, executed as a
module (its own place() asserts on overlap), and its ROM words and occupancy
set are recorded. The report lists, per pair, the word ranges that differ, and
checks the two lane microprograms (E_IDNOTIF, E_SINFOUNS) word-for-word
between the round-3 lane head (at 2000/2016) and the merges (at 464/480).

usage: rom_compare.py <repo> <outdir>
"""
import hashlib
import importlib.util
import pathlib
import subprocess
import sys

REVS = {
    "lane_r3_9624ef4c": "9624ef4c452d708de68a901d5e645bdfa1f5d6f5",
    "main_16ea10ac": "16ea10ace6c755c91bb9e864b2b855acb240b09b",
    "merge_r4_651839e": "651839e1ce9d3a36adfbfae0297dd091a02a2def",
    "main_03c842a7": "03c842a780064048b0a1a3de29214174a1c13934",
    "head_95a78c0": "95a78c099ee5aa914521975355adc1dfef99d01c",
}


def load(repo, rev, outdir, name):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:hdl/aecp/ucode/gen_ucode.py"],
                         check=True, capture_output=True).stdout
    path = outdir / f"gen_ucode_{name}.py"
    path.write_bytes(src)
    spec = importlib.util.spec_from_file_location(f"g_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    hexpath = outdir / f"ucode_{name}.hex"
    hexpath.write_text("".join(f"{w:012x}\n" for w in mod.rom))
    return mod, hashlib.sha256(hexpath.read_bytes()).hexdigest()


def ranges(idx):
    out, start, prev = [], None, None
    for i in sorted(idx):
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            out.append((start, prev))
            start = prev = i
    if start is not None:
        out.append((start, prev))
    return ", ".join(f"{a}..{b}" if a != b else f"{a}" for a, b in out) or "none"


def body(mod, entry):
    occ = mod.occupied
    words, i = [], entry
    while i in occ:
        words.append(mod.rom[i])
        i += 1
    return words


def main():
    repo, outdir = sys.argv[1], pathlib.Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    mods = {}
    for name, rev in REVS.items():
        mod, sha = load(repo, rev, outdir, name)
        mods[name] = mod
        print(f"{name} {rev}: {len(mod.rom)} words, {len(mod.placed)} programs, "
              f"{len(mod.occupied)} occupied, sha256 {sha}")
    print()
    for a, b in (("main_16ea10ac", "merge_r4_651839e"), ("lane_r3_9624ef4c", "merge_r4_651839e"),
                 ("main_03c842a7", "head_95a78c0"), ("merge_r4_651839e", "head_95a78c0")):
        ma, mb = mods[a], mods[b]
        diff = [i for i in range(len(ma.rom)) if ma.rom[i] != mb.rom[i]]
        docc = [i for i in range(len(ma.rom)) if (i in ma.occupied) != (i in mb.occupied)]
        print(f"{a} vs {b}: words differ at {ranges(diff)}; occupancy differs at {ranges(docc)}")
    print()
    lane, head = mods["lane_r3_9624ef4c"], mods["head_95a78c0"]
    for nm in ("E_IDNOTIF", "E_SINFOUNS"):
        lb, hb = body(lane, getattr(lane, nm)), body(head, getattr(head, nm))
        print(f"{nm}: lane {getattr(lane, nm)} ({len(lb)} words) -> head {getattr(head, nm)} "
              f"({len(hb)} words); identical: {lb == hb}")
    for nm in ("E_IDNOTIF", "E_SINFOUNS"):
        e, n = getattr(head, nm), len(body(head, getattr(head, nm)))
        for other in ("main_16ea10ac", "main_03c842a7"):
            m = mods[other]
            clash = [i for i in range(e, e + n) if i in m.occupied]
            print(f"{nm} {e}..{e + n - 1} occupied in {other}: {clash or 'none'}")
    for other in ("main_16ea10ac", "main_03c842a7"):
        m = mods[other]
        for old in (2000, 2016):
            print(f"word {old} occupied in {other}: {old in m.occupied}")
    dl = head.E_DLKILL
    print(f"E_DLKILL {dl}..{dl + 1} in head occupied; in lane_r3 occupied: "
          f"{[i in lane.occupied for i in (dl, dl + 1)]}; lane bodies overlap it: "
          f"{bool(set(range(dl, dl + 2)) & set(range(464, 501)))}")
    # every program the head's two parents place is placed in the head at the same entry
    for p in ("merge_r4_651839e", "main_03c842a7"):
        missing = sorted(set(mods[p].occupied) - set(head.occupied))
        print(f"words occupied in {p} but not in head: {ranges(missing)}")


if __name__ == "__main__":
    main()
