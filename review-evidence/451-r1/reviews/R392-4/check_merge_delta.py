#!/usr/bin/env python3
"""Reviewer check for the PR #616 merge of dev (R392-4).

Usage: check_merge_delta.py REPO HEAD DEV LANE BASE
Reads only committed objects via git; writes nothing. Prints PASS/FAIL lines
and exits non-zero on any FAIL.
"""
import re
import subprocess
import sys

REPO, HEAD, DEV, LANE, BASE = sys.argv[1:6]
FAILS = []


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], check=True,
                          capture_output=True, text=True).stdout


def show(rev, path):
    return git("show", f"{rev}:{path}").splitlines()


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        FAILS.append(msg)


def changed_lines(a, b, path):
    out = git("diff", "-U0", a, b, "--", path)
    minus = [l[1:] for l in out.splitlines()
             if l.startswith("-") and not l.startswith("---")]
    plus = [l[1:] for l in out.splitlines()
            if l.startswith("+") and not l.startswith("+++")]
    return minus, plus


def row(lines, key):
    hits = [l for l in lines if l.startswith("| " + key + " |")]
    return hits


# (3) net change against dev and gitlinks
names = git("diff", "--name-status", DEV, HEAD).split("\n")
names = [n for n in names if n]
expect = ["A\tdocs/findings/451_TDM8_FIRST_LIGHT.md",
          "M\tdocs/findings/README.md",
          "M\tdocs/litex/CLOCK_DOMAINS.md",
          "M\tdocs/reference/MILAN_COMPLIANCE_MATRIX.md"]
check(names == expect, f"dev..head touches exactly the four PR files: {names}")
lane_names = [n for n in git("diff", "--name-status", BASE, LANE).split("\n") if n]
check(lane_names == expect, "lane's own diff (base..lane) is the same four files")
for p in ["docs/findings/451_TDM8_FIRST_LIGHT.md", "docs/findings/README.md",
          "docs/litex/CLOCK_DOMAINS.md", "docs/reference/MILAN_COMPLIANCE_MATRIX.md"]:
    lm, lp = changed_lines(BASE, LANE, p)
    hm, hp = changed_lines(DEV, HEAD, p)
    check((lm, lp) == (hm, hp),
          f"{p}: changed lines dev..head == base..lane (-{len(hm)} +{len(hp)})")
def blob(rev, path):
    try:
        return git("rev-parse", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return None


check(blob(HEAD, "docs/findings/451_TDM8_FIRST_LIGHT.md") is not None and
      blob(HEAD, "docs/findings/451_TDM8_FIRST_LIGHT.md") ==
      blob(LANE, "docs/findings/451_TDM8_FIRST_LIGHT.md"),
      "finding page blob unchanged from the reviewed lane head")
# merge side: head vs lane equals base vs dev
check(git("diff", "--numstat", LANE, HEAD) == git("diff", "--numstat", BASE, DEV),
      "numstat lane..head == numstat base..dev (merge brought dev only)")
for p in [l.split("\t")[-1] for l in git("diff", "--numstat", BASE, DEV).splitlines()]:
    try:
        a = git("diff", "-U0", LANE, HEAD, "--", p)
        b = git("diff", "-U0", BASE, DEV, "--", p)
    except subprocess.CalledProcessError:
        continue
    strip = lambda s: [l for l in s.splitlines()
                       if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    if strip(a) != strip(b):
        check(False, f"merge side differs from dev side for {p}")
print("INFO merge-side per-file changed-line comparison complete")


def gitlinks(rev):
    return sorted(l for l in git("ls-tree", "-r", rev).splitlines()
                  if l.startswith("160000"))


check(gitlinks(HEAD) == gitlinks(DEV), "all gitlinks at head equal dev's")
pp = [l for l in gitlinks(HEAD) if l.endswith("\tprotocol-processor")]
check(len(pp) == 1 and "c951a9ff0cb5851fb159d33e966e5a2a9a188fe3" in pp[0],
      f"protocol-processor gitlink is c951a9ff: {pp}")

# (1) compliance matrix rows
M = "docs/reference/MILAN_COMPLIANCE_MATRIX.md"
hm, dm, lm = show(HEAD, M), show(DEV, M), show(LANE, M)
for key in ["4.4.4.3", "5.4.2.15 / .16", "5.3.11.1", "7.4.42.2"]:
    h, d = row(hm, key), row(dm, key)
    check(len(h) == 1 and h == d, f"matrix row {key} equals dev's")
r4443 = (row(hm, "4.4.4.3") or [""])[0]
check("issues/602#issuecomment-5859297355" in r4443, "4.4.4.3 keeps the #602 ruling link")
r445 = row(hm, "4.4.4.5 / .9")
check(len(r445) == 1 and r445 == row(lm, "4.4.4.5 / .9"),
      "4.4.4.5 / .9 row equals the lane's")
check(len(r445) == 1 and "../findings/451_TDM8_FIRST_LIGHT.md" in r445[0],
      "4.4.4.5 / .9 keeps the first-light link")
check(len(hm) == len(dm) and sum(a != b for a, b in zip(hm, dm)) == 1,
      "matrix differs from dev by exactly one line")
check(sum(a != b for a, b in zip(hm, lm)) == 4 and len(hm) == len(lm),
      "matrix differs from lane by exactly dev's four lines")
check(not any(re.match(r"^(<<<<<<<|=======|>>>>>>>)", l) for l in hm),
      "no conflict markers in matrix")

# (2) findings index
I = "docs/findings/README.md"


def index_rows(lines):
    return [l for l in lines if l.startswith("| [")]


hi, di, li = index_rows(show(HEAD, I)), index_rows(show(DEV, I)), index_rows(show(LANE, I))
check(len(hi) == len(set(hi)), f"index has no duplicate row ({len(hi)} rows)")
check(set(hi) == set(di) | {li[0]}, "index rows = dev rows + the #451 row")
check(bool(hi) and li[0].startswith("| [451_TDM8_FIRST_LIGHT.md]") and hi[0] == li[0],
      "#451 row first, as on the lane")
check(hi[1:] == di, "dev's rows follow in dev's order")
lane_rest = [r for r in li[1:]]
dev_order_ok = all(r in di or "397_SERVICE_BUDGET" in r for r in lane_rest)
check(dev_order_ok, "every other lane row is present in dev (only #397 was reworded by dev)")

# CLOCK_DOMAINS
C = "docs/litex/CLOCK_DOMAINS.md"
hc = show(HEAD, C)
_, dev_added = changed_lines(BASE, DEV, C)
_, lane_added = changed_lines(BASE, LANE, C)
check(all(l in hc for l in dev_added), f"CLOCK_DOMAINS keeps dev's {len(dev_added)} added lines")
check(all(l in hc for l in lane_added) and len(lane_added) == 1,
      "CLOCK_DOMAINS keeps this PR's line")
check(not any(l == "- The example configuration exposes capture, not physical TDM rendering."
              for l in hc), "the superseded capture-only line is gone")

sys.exit(1 if FAILS else 0)
