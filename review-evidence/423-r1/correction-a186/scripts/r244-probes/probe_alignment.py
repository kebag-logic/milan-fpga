"""Bounded randomized probe of the raw no-op re-merge used by retention (T).

Construction (deterministic seeds): O is random lines over a small alphabet
(heavy repetition), S applies one source hunk to O, and T is built from S by
REVERTING that hunk exactly and then applying one further random edit
located strictly outside the reverted region (no overlap by construction).
By construction the source's work is absent at T. The probe counts how often
`git merge-file -p T O S` is clean AND byte-equal to T (the T acceptance
condition), and classifies each such acceptance:
  bytes-consistent : T is also obtainable as S plus one edit (the bytes are
                     ambiguous; a byte-level criterion cannot tell them apart)
  other            : neither - would be a true mis-merge worth reporting
Usage: probe_alignment.py <cases> <workers> <tmpdir>
"""
import random
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ALPHA = ["a\n", "b\n", "c\n"]


def edit(rng, lines, lo=0, hi=None):
    """One random replace/insert/delete of 1-2 lines at [lo, hi)."""
    hi = len(lines) if hi is None else hi
    if hi <= lo:
        return None
    i = rng.randrange(lo, hi + 1)
    kind = rng.choice(("ins", "del", "rep"))
    n = rng.choice((1, 2))
    new = [rng.choice(ALPHA + ["X\n", "Y\n"]) for _ in range(n)]
    if kind == "ins":
        return lines[:i] + new + lines[i:], (i, i)
    if i + n > hi:
        return None
    if kind == "del":
        return lines[:i] + lines[i + n:], (i, i + n)
    return lines[:i] + new + lines[i + n:], (i, i + n)


def one_edit_away(src, dst):
    """True when dst = src with one contiguous replace/insert/delete."""
    p = 0
    while p < min(len(src), len(dst)) and src[p] == dst[p]:
        p += 1
    q = 0
    while (q < min(len(src), len(dst)) - p and src[-1 - q] == dst[-1 - q]):
        q += 1
    return True  # any pair differs by one contiguous block


def contains_as_extension(s, t, hunk):
    """Is T = S with one edit that does not overlap S's changed hunk?"""
    lo, hi = hunk
    # try all single contiguous edits of S outside [lo, hi) producing T
    n, m = len(s), len(t)
    for i in range(n + 1):
        for j in range(i, n + 1):
            if not (j <= lo or i >= hi) and not (i == j and (i <= lo or i >= hi)):
                continue
            pre, post = s[:i], s[j:]
            if len(pre) + len(post) > m:
                continue
            if t[:len(pre)] == pre and (not post or t[m - len(post):] == post):
                return True
    return False


def case(seed, tmp):
    rng = random.Random(seed)
    o = [rng.choice(ALPHA) for _ in range(rng.randrange(4, 12))]
    r = edit(rng, o)
    if r is None:
        return None
    s, (lo, hi) = r
    # the S hunk occupies [lo, lo + (len(s) - len(o)) + (hi - lo)) in S
    s_hi = lo + (len(s) - len(o)) + (hi - lo)
    t0 = list(o)  # exact revert of the only source hunk
    # one further edit strictly outside the reverted O region [lo, hi)
    side = rng.choice(("before", "after"))
    r2 = edit(rng, t0, 0, max(lo - 1, 0)) if side == "before" else edit(rng, t0, min(hi + 1, len(t0)), len(t0))
    if r2 is None:
        return None
    t = r2[0]
    if t == s or t == o:
        return None
    d = Path(tmp)
    for name, data in (("t", t), ("o", o), ("s", s)):
        (d / name).write_text("".join(data))
    p = subprocess.run(("git", "-c", "merge.conflictStyle=merge", "merge-file", "-p", "-q",
                        str(d / "t"), str(d / "o"), str(d / "s")), capture_output=True)
    if p.returncode != 0 or p.stdout != "".join(t).encode():
        return "refused"
    return ("bytes-consistent" if contains_as_extension(s, t, (lo, s_hi)) else "other",
            "".join(o), "".join(s), "".join(t))


def chunk(args):
    start, count = args
    out = {"refused": 0, "skipped": 0, "bytes-consistent": 0, "other": 0, "examples": []}
    with tempfile.TemporaryDirectory() as tmp:
        for seed in range(start, start + count):
            res = case(seed, tmp)
            if res is None:
                out["skipped"] += 1
            elif res == "refused":
                out["refused"] += 1
            else:
                out[res[0]] += 1
                if res[0] == "other" and len(out["examples"]) < 3:
                    out["examples"].append((seed,) + res[1:])
    return out


def main():
    total, workers = int(sys.argv[1]), int(sys.argv[2])
    per = total // workers
    agg = {"refused": 0, "skipped": 0, "bytes-consistent": 0, "other": 0, "examples": []}
    with ProcessPoolExecutor(workers) as pool:
        for part in pool.map(chunk, [(k * per, per) for k in range(workers)]):
            for key in ("refused", "skipped", "bytes-consistent", "other"):
                agg[key] += part[key]
            agg["examples"] += part["examples"]
    print({k: v for k, v in agg.items() if k != "examples"})
    for ex in agg["examples"][:6]:
        print("EXAMPLE seed=%d\n O=%r\n S=%r\n T=%r" % ex)


if __name__ == "__main__":
    main()
