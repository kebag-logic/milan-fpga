#!/usr/bin/env python3
"""Reviewer probe: can T's raw no-op re-merge accept provably lost work?

T accepts a regular-blob path when `git merge-file -p tip ancestor source`
exits 0 and prints exactly the tip bytes.  This searches random small
histories over a repetitive alphabet for a crisp false acceptance:

  * the source INSERTS a unique line Z, T accepts, and the tip has no Z; or
  * the source DELETES the unique line D, T accepts, and the tip still has D.

Tips are derived from the source by random edits that sometimes drop Z or
restore D (lost work) and sometimes only touch other lines (retained work).
A "found" row is a counterexample; zero found is bounded evidence only.

    probe_merge_alignment.py <trials> <seed> <workers> <scratch-dir> <out.json>
"""
import concurrent.futures
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ALPHABET = ["a", "b", "c", "a", "b"]  # skewed: repeated lines are common


def edit(lines, rng, count):
    lines = list(lines)
    for _ in range(count):
        op = rng.choice(("ins", "del", "chg", "dup"))
        i = rng.randrange(len(lines) + 1)
        if op == "ins" or not lines:
            lines.insert(i, rng.choice(ALPHABET))
        elif op == "del":
            del lines[min(i, len(lines) - 1)]
        elif op == "chg":
            lines[min(i, len(lines) - 1)] = rng.choice(ALPHABET)
        else:  # duplicate a random slice elsewhere (repeated blocks)
            j = rng.randrange(len(lines))
            k = min(len(lines), j + rng.randint(1, 3))
            lines[i:i] = lines[j:k]
    return lines


def trial(seed, workdir):
    rng = random.Random(seed)
    anc = [rng.choice(ALPHABET) for _ in range(rng.randint(2, 9))]
    mode = rng.choice(("insert", "delete"))
    if mode == "delete":
        anc.insert(rng.randrange(len(anc) + 1), "D")
        src = [x for x in anc if x != "D"]
    else:
        src = list(anc)
        src.insert(rng.randrange(len(src) + 1), "Z")
    src = edit(src, rng, rng.randint(0, 2))          # other source work
    if mode == "insert" and "Z" not in src:
        return None
    if mode == "delete" and "D" in src:
        return None
    tip = edit(src, rng, rng.randint(0, 3))          # later tip work
    lost = rng.random() < 0.5
    if lost:
        if mode == "insert":
            tip = [x for x in tip if x != "Z"]
            if rng.random() < 0.5:                   # replace with lookalike
                tip.insert(rng.randrange(len(tip) + 1), rng.choice(ALPHABET))
        else:
            tip.insert(rng.randrange(len(tip) + 1), "D")
    enc = lambda xs: "".join(x + "\n" for x in xs).encode()
    files = [Path(workdir) / n for n in ("tip", "base", "src")]
    for f, data in zip(files, (enc(tip), enc(anc), enc(src))):
        f.write_bytes(data)
    p = subprocess.run(("git", "-c", "merge.conflictStyle=merge", "merge-file",
                        "-p", "-q", *map(str, files)), capture_output=True)
    accepted = p.returncode == 0 and p.stdout == enc(tip)
    work_lost = ("Z" not in tip) if mode == "insert" else ("D" in tip)
    return {"seed": seed, "mode": mode, "accepted": accepted, "work_lost": work_lost,
            "rc": p.returncode, "anc": anc, "src": src, "tip": tip}


def edit_keep(lines, rng, count, keep):
    """Random ins/chg/dup edits that never remove or change a `keep` line."""
    lines = list(lines)
    for _ in range(count):
        op = rng.choice(("ins", "chg", "dup"))
        i = rng.randrange(len(lines) + 1)
        if op == "ins" or not lines:
            lines.insert(i, rng.choice(ALPHABET))
        elif op == "chg":
            j = min(i, len(lines) - 1)
            if lines[j] not in keep:
                lines[j] = rng.choice(ALPHABET)
        else:
            j = rng.randrange(len(lines))
            k = min(len(lines), j + rng.randint(1, 3))
            lines[i:i] = [x for x in lines[j:k] if x not in keep]
    return lines


def neighbours(lines, token):
    return {(lines[i - 1] if i else None, lines[i + 1] if i + 1 < len(lines) else None)
            for i, x in enumerate(lines) if x == token}


def trial_v2(seed, workdir):
    """Crisp lost-work families.

    restore: the source deletes unique D; the tip restores D between the SAME
      neighbours it had in the ancestor (an in-place revert), plus other edits.
    partial: the source inserts unique Z1 and Z2; the tip keeps Z1, drops Z2.
    """
    rng = random.Random(seed)
    family = rng.choice(("restore", "partial"))
    anc = [rng.choice(ALPHABET) for _ in range(rng.randint(3, 10))]
    if family == "restore":
        i = rng.randrange(len(anc) + 1)
        anc.insert(i, "D")
        src = anc[:i] + anc[i + 1:]
        tip = edit_keep(anc, rng, rng.randint(0, 3), {"D"})
        lost = bool(neighbours(tip, "D") & neighbours(anc, "D"))
    else:
        src = list(anc)
        src.insert(rng.randrange(len(src) + 1), "Z1")
        src.insert(rng.randrange(len(src) + 1), "Z2")
        tip = edit_keep([x for x in src if x != "Z2"], rng, rng.randint(0, 3), {"Z1"})
        lost = "Z2" not in tip
    enc = lambda xs: "".join(x + "\n" for x in xs).encode()
    files = [Path(workdir) / n for n in ("tip", "base", "src")]
    for f, data in zip(files, (enc(tip), enc(anc), enc(src))):
        f.write_bytes(data)
    p = subprocess.run(("git", "-c", "merge.conflictStyle=merge", "merge-file",
                        "-p", "-q", *map(str, files)), capture_output=True)
    accepted = p.returncode == 0 and p.stdout == enc(tip)
    return {"seed": seed, "mode": family, "accepted": accepted, "work_lost": lost,
            "rc": p.returncode, "anc": anc, "src": src, "tip": tip}


def worker(args):
    start, count, scratch, version = args
    stats = {"trials": 0, "accepted": 0, "lost": 0, "found": []}
    run = trial_v2 if version == "v2" else trial
    with tempfile.TemporaryDirectory(dir=scratch) as d:
        for seed in range(start, start + count):
            r = run(seed, d)
            if r is None:
                continue
            stats["trials"] += 1
            stats["accepted"] += r["accepted"]
            stats["lost"] += r["work_lost"]
            if r["accepted"] and r["work_lost"]:
                stats["found"].append(r)
    return stats


def main():
    trials, seed, workers = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    scratch, out = Path(sys.argv[4]), Path(sys.argv[5])
    version = sys.argv[6] if len(sys.argv) > 6 else "v1"
    scratch.mkdir(parents=True, exist_ok=True)
    chunk = trials // workers
    jobs = [(seed + i * chunk, chunk, str(scratch), version) for i in range(workers)]
    with concurrent.futures.ProcessPoolExecutor(workers) as pool:
        parts = list(pool.map(worker, jobs))
    total = {k: sum(p[k] for p in parts) for k in ("trials", "accepted", "lost")}
    found = [f for p in parts for f in p["found"]]
    total.update(found=len(found), examples=found[:10], family=version,
                 git=subprocess.run(("git", "--version"), capture_output=True,
                                    text=True).stdout.strip(),
                 seeds=f"{seed}..{seed + chunk * workers - 1}")
    json.dump(total, open(out, "w"), indent=1)
    print({k: v for k, v in total.items() if k != "examples"})


if __name__ == "__main__":
    main()
