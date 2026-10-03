#!/usr/bin/env python3
"""Value-blind scan for the external capture's private channel count and sample format.

The private values are derived inside this process from the masking commits' own diffs
(a removed line against its added line, where the added line carries the placeholder),
and are never printed. Output reports only counts, paths and booleans.

Usage: privacy_scan.py <repo> <page-head> <evidence-commit> <pr-body-file> [<extra-text-file> ...]
"""
import re
import subprocess
import sys

repo, head, evc = sys.argv[1], sys.argv[2], sys.argv[3]
pr_body, extras = sys.argv[4], sys.argv[5:]
EV = "review-evidence/629-b7-r1"
MASKS = ("d36de704456713fb89b39a59151b72015fa00c6d", "c6ad37e7d9163b5a85aef935a7d8e7f7f6686f7f")
PH = {"<capture-channels>": "ch", "<capture-format>": "fmt"}


def git(*a, binary=False):
    out = subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout
    return out if binary else out.decode("utf-8", "replace")


# 1. derive the private tokens from the masking diffs
vals = {"ch": set(), "fmt": set()}
for c in MASKS:
    diff = git("show", "--format=", "-U0", c, "--", f"{EV}/author")
    for hunk in diff.split("\n@@")[1:]:
        lines = hunk.split("\n")[1:]
        rem = [l[1:] for l in lines if l.startswith("-") and not l.startswith("---")]
        add = [l[1:] for l in lines if l.startswith("+") and not l.startswith("+++")]
        for r, a in zip(rem, add):
            if not any(p in a for p in PH):
                continue
            pat = re.escape(a)
            for p, g in PH.items():
                pat = pat.replace(re.escape(p), f"(?P<{g}_{{i}}>.+?)")
            k = 0
            while "{i}" in pat:
                pat = pat.replace("{i}", str(k), 1)
                k += 1
            m = re.fullmatch(pat, r)
            if not m:
                print(f"UNALIGNED hunk in {c[:8]}")
                continue
            for name, v in m.groupdict().items():
                vals[name.split("_")[0]].add(v)
print(f"derived: channel-count values={len(vals['ch'])} format values={len(vals['fmt'])} (values withheld)")
assert len(vals["ch"]) == 1 and len(vals["fmt"]) == 1, "expected exactly one value of each"
CH, FMT = next(iter(vals["ch"])), next(iter(vals["fmt"]))
assert CH.isdigit()

WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen", "twenty"]
chw = WORDS[int(CH)] if int(CH) < len(WORDS) else None
ch_alts = [re.escape(CH)] + ([chw] if chw else [])
ch_re = re.compile(
    r"(?i)(?:\b(?:%s)[\s-]*(?:ch\b|chan\b|channels?\b|channel\b)"
    r"|cap-all-(?:%s)ch|\bNCH\s*[,=:]?\s*(?:%s)\b|\bNCH\s*,[^=\n]*=\s*(?:%s)\b"
    r"|(?:-c|--channels(?:=|\s))\s*(?:%s)\b|channels?\s*[=:]\s*(?:%s)\b|\b(?:%s)\s+capture channels)"
    % ((("|".join(ch_alts)),) * 7))
fmt_re = re.compile(re.escape(FMT), re.I)
alsa_re = re.compile(r"(?i)\b[SU](?:8|16|20|24|32)(?:_[0-9]+)?_?(?:LE|BE)\b|\bFLOAT(?:64)?_?(?:LE|BE)\b")


def scan(label, text):
    ch_hits = len(ch_re.findall(text))
    fmt_hits = len(fmt_re.findall(text))
    alsa = alsa_re.findall(text)
    alsa_priv = sum(1 for a in alsa if a.lower() == FMT.lower())
    other = sorted({re.sub(r"[0-9]+", "<N>", a) for a in alsa if a.lower() != FMT.lower()})
    return ch_hits, fmt_hits, len(alsa), alsa_priv, other


rows = []
fails = 0


def record(label, text):
    global fails
    ch, fm, an, ap, other = scan(label, text)
    bad = ch or fm or ap
    fails += bool(bad)
    rows.append(f"{'FAIL' if bad else 'ok  '}\tch={ch}\tfmt={fm}\talsa_any={an}\talsa_private={ap}\tother_alsa_shapes={','.join(other) or '-'}\t{label}")


# 2. the page, the findings index and the diff at the head; the lane's commit messages
for p in ("docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md", "docs/findings/README.md"):
    record(f"head:{p}", git("show", f"{head}:{p}"))
_d = git("diff", "bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352", head).split("\n")
record("diff bbf704ec..head, added lines", "\n".join(l for l in _d if l.startswith("+") and not l.startswith("+++")))
_rm = scan("rm", "\n".join(l for l in _d if l.startswith("-") and not l.startswith("---")))
rows.append(f"info\tremoved-by-this-PR lines: ch={_rm[0]} fmt={_rm[1]} alsa_private={_rm[3]} (dev text this PR deletes)")
record("commit messages bbf704ec..head", git("log", "--format=%B", f"bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352..{head}"))
# 3. the PR body and any extra texts
record(f"file:{pr_body}", open(pr_body, encoding="utf-8").read())
for x in extras:
    record(f"file:{x}", open(x, encoding="utf-8", errors="replace").read())
# 4. every blob of the evidence tree at the pinned commit (paths included)
import os
SCAN_EV = os.environ.get("SCAN_EV", EV)
names = git("ls-tree", "-r", "--name-only", evc, SCAN_EV).split("\n")
names = [n for n in names if n]
path_hits = 0
for n in names:
    data = git("show", f"{evc}:{n}", binary=True).decode("utf-8", "replace")
    ch, fm, an, ap, other = scan(n, data + "\n" + n)
    if ch or fm or ap:
        rows.append(f"FAIL\tch={ch}\tfmt={fm}\talsa_private={ap}\tevidence:{n}")
        fails += 1
    elif an:
        rows.append(f"note\talsa_any={an}\tother_alsa_shapes={','.join(other)}\tevidence:{n}")
print(f"evidence blobs scanned at {evc[:8]}: {len(names)}")
for r in rows:
    print(r)
# 5. sanity: the scanner does find the values where they are known to be (history before masking)
pre = git("show", f"95448218b342c084efa28ac266ae9415bff4ecce:{EV}/author/tools/run_b7.py")
c, f, *_ = scan("positive control", pre)
print(f"positive control (run_b7.py at 95448218, pre-mask): ch_hits={c} fmt_hits={f} (both must be >0)")
pre2 = git("show", f"d36de704456713fb89b39a59151b72015fa00c6d:{EV}/author/RAW-ARTIFACTS.json")
c2, *_ = scan("positive control 2", pre2)
print(f"positive control (RAW-ARTIFACTS.json at d36de704, pre-name-mask): ch_hits={c2} (must be >0)")
ok = fails == 0 and c > 0 and f > 0 and c2 > 0
print("RESULT", "CLEAN" if ok else "NOT-CLEAN", f"fails={fails}")
sys.exit(0 if ok else 1)
