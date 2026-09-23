#!/usr/bin/env python3
"""Reviewer probe: exact in-place revert plus edits at a distance.

The source deletes (or inserts) one unique line.  The tip is the ANCESTOR
(an exact revert of that hunk) plus 1..3 random edits, every one at least
`gap` lines away from the reverted hunk, in repetitive content.  Any T
acceptance (`merge-file -p tip ancestor source` exits 0 with the tip bytes)
is a later reversion accepted despite unrelated distant edits.

    probe_revert_distance.py <trials> <seed> <gap> <scratch-dir> <out.json>
"""
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

ALPHABET = ["a", "b", "c", "a", "b"]


def far_edits(lines, rng, count, centre, gap):
    lines, centre = list(lines), centre
    for _ in range(count):
        choices = [i for i in range(len(lines) + 1) if abs(i - centre) >= gap]
        if not choices:
            break
        i = rng.choice(choices)
        op = rng.choice(("ins", "chg", "del"))
        if op == "ins" or i >= len(lines):
            lines.insert(i, rng.choice(ALPHABET))
            centre += i <= centre
        elif op == "chg":
            lines[i] = rng.choice(ALPHABET)
        else:
            del lines[i]
            centre -= i < centre
    return lines


def main():
    trials, seed, gap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    scratch, out = Path(sys.argv[4]), Path(sys.argv[5])
    scratch.mkdir(parents=True, exist_ok=True)
    found, accepted_total, n = [], 0, 0
    enc = lambda xs: "".join(x + "\n" for x in xs).encode()
    with tempfile.TemporaryDirectory(dir=scratch) as d:
        files = [Path(d) / name for name in ("tip", "base", "src")]
        for s in range(seed, seed + trials):
            rng = random.Random(s)
            anc = [rng.choice(ALPHABET) for _ in range(rng.randint(2 * gap + 1, 4 * gap + 6))]
            i = rng.randrange(len(anc) + 1)
            if rng.random() < 0.5:
                anc.insert(i, "D")
                src = anc[:i] + anc[i + 1:]
                mode = "delete"
            else:
                src = anc[:i] + ["Z"] + anc[i:]
                mode = "insert"
            tip = far_edits(anc, rng, rng.randint(1, 3), i, gap)
            if tip == anc:
                continue
            n += 1
            for f, data in zip(files, (enc(tip), enc(anc), enc(src))):
                f.write_bytes(data)
            p = subprocess.run(("git", "-c", "merge.conflictStyle=merge", "merge-file",
                                "-p", "-q", *map(str, files)), capture_output=True)
            if p.returncode == 0 and p.stdout == enc(tip):
                accepted_total += 1
                if len(found) < 10:
                    found.append({"seed": s, "mode": mode, "anc": anc, "src": src, "tip": tip})
    result = {"trials": n, "gap": gap, "accepted_reverts": accepted_total,
              "examples": found, "seeds": f"{seed}..{seed + trials - 1}",
              "git": subprocess.run(("git", "--version"), capture_output=True,
                                    text=True).stdout.strip()}
    json.dump(result, open(out, "w"), indent=1)
    print({k: v for k, v in result.items() if k != "examples"})


if __name__ == "__main__":
    main()
