#!/usr/bin/env python3
"""R372-4: structural proof that 895be307 is exactly the merge of 3b5603e3 and 1fa2357f
plus the two assigned conflict resolutions.  Read-only.

Usage: python3 -B check_merge_structure.py <repo>
"""
import difflib
import subprocess
import sys

REPO = sys.argv[1]
HEAD, BRANCH, DEV, BASE = ("895be30712acf8dd80956a5b954690859b080d87",
                           "3b5603e3d16a164c35329efeb633800fe4fe9f95",
                           "1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a",
                           "8bc97021f28fb7f729418d3a00851c84ea0b50fd")
FAIL = []


def git(*a, check=True):
    r = subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(r.stderr)
    return r


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def tree(c):
    out = {}
    for line in git("ls-tree", "-r", "-z", c).stdout.split("\0"):
        if line:
            meta, path = line.split("\t", 1)
            mode, _typ, sha = meta.split()
            out[path] = (mode, sha)
    return out


def show(c, p):
    return git("show", f"{c}:{p}").stdout


check(git("rev-parse", "HEAD").stdout.strip() == HEAD, f"checkout HEAD is {HEAD}")
check(git("rev-parse", f"{HEAD}^{{tree}}").stdout.strip() == "aaf645102ef01bb0480f6bddd34e287fbd54bd9d",
      "tree aaf64510")
check(git("rev-parse", f"{HEAD}^1").stdout.strip() == BRANCH and git("rev-parse", f"{HEAD}^2").stdout.strip() == DEV,
      "parents are 3b5603e3 (branch) and 1fa2357f (dev)")
check(git("merge-base", BRANCH, DEV).stdout.strip() == BASE, "merge base is 8bc97021")

m, d, p, b = (tree(c) for c in (HEAD, DEV, BRANCH, BASE))
both, bad = [], []
for path in sorted(set(m) | set(d) | set(p) | set(b)):
    dev_changed, br_changed = b.get(path) != d.get(path), b.get(path) != p.get(path)
    if dev_changed and br_changed:
        both.append(path)
    elif dev_changed and m.get(path) != d.get(path):
        bad.append(("dev-only path differs from dev", path))
    elif br_changed and m.get(path) != p.get(path):
        bad.append(("branch-only path differs from branch", path))
    elif not dev_changed and not br_changed and m.get(path) != b.get(path):
        bad.append(("untouched path differs from base", path))
check(not bad, f"every single-sided or untouched path (incl. modes and gitlinks) equals its source side: {bad}")
check(both == ["docs/findings/README.md", "sw/builder/test_builder.py", "sw/litex/milan_soc.py"],
      f"paths changed on both sides: {both}")
check(m["protocol-processor"] == d["protocol-processor"] == ("160000", "16be6768f710e79450aace277abacd6c2c3336e5"),
      "protocol-processor gitlink 16be6768 (dev's)")

mt = git("merge-tree", "--write-tree", "--name-only", BRANCH, DEV, check=False)
lines = mt.stdout.splitlines()
auto_tree, conflicted = lines[0], [x for x in lines[1:lines.index("")]] if "" in lines else lines[1:]
check(mt.returncode == 1 and conflicted == ["docs/findings/README.md", "sw/builder/test_builder.py"],
      f"git merge-tree recomputation conflicts exactly in {conflicted}")
auto = tree(auto_tree)
diffs = sorted(x for x in set(auto) | set(m) if auto.get(x) != m.get(x))
check(diffs == ["docs/findings/README.md", "sw/builder/test_builder.py"],
      f"recomputed merge differs from the published merge only in the two conflict files: {diffs}")
check(auto["sw/litex/milan_soc.py"] == m["sw/litex/milan_soc.py"], "milan_soc.py equals the clean auto-merge")


def rows(c):
    return [x for x in show(c, "docs/findings/README.md").splitlines() if x.startswith("| [")]


rb, rp, rd, rm = rows(BASE), rows(BRANCH), rows(DEV), rows(HEAD)
check(set(rm) == set(rp) | set(rd) and len(rm) == len(set(rm)), "findings rows = union of both sides, no duplicate")
for name, side in (("branch", rp), ("dev", rd)):
    idx = [rm.index(r) for r in side]
    check(idx == sorted(idx), f"findings: {name} relative row order preserved")
new = [r for r in rm if r not in rb]
check(len(new) == 2 and rm.index(new[0]) == 0 and rm.index(new[1]) == 1
      and rm[2:] == rb, "findings: both new current records lead the unchanged base rows (newest-first block)")
text_m, text_d = show(HEAD, "docs/findings/README.md"), show(DEV, "docs/findings/README.md")
ops = [o for o in difflib.SequenceMatcher(None, text_d.splitlines(), text_m.splitlines(), autojunk=False).get_opcodes()
       if o[0] != "equal"]
check(len(ops) == 1 and ops[0][0] == "insert" and ops[0][2] - ops[0][1] == 0 and ops[0][4] - ops[0][3] == 1,
      "findings README = dev + exactly one inserted row")

tm, td = show(HEAD, "sw/builder/test_builder.py").splitlines(), show(DEV, "sw/builder/test_builder.py").splitlines()
tp, tb = show(BRANCH, "sw/builder/test_builder.py").splitlines(), show(BASE, "sw/builder/test_builder.py").splitlines()
added_by_branch = [ln for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, tb, tp, autojunk=False).get_opcodes()
                   if tag != "equal" for ln in tp[j1:j2]]
ops = [o for o in difflib.SequenceMatcher(None, td, tm, autojunk=False).get_opcodes() if o[0] != "equal"]
inserted = [ln for tag, i1, i2, j1, j2 in ops for ln in tm[j1:j2]]
removed = [ln for tag, i1, i2, j1, j2 in ops for ln in td[i1:i2]]
dev_loop = "    for fn in (test_baremetal_clock_contract, test_gptp_rom_clock, test_extra_sweep_clocks, test_tap_clock_docs,"
check(removed == [dev_loop], f"test_builder: only dev's loop-head line was re-flowed: {removed}")
check(sorted(inserted) == sorted(added_by_branch[:-1] + ["               test_baremetal_clock_contract, "
                                                          "test_gptp_rom_clock, test_extra_sweep_clocks, "
                                                          "test_tap_clock_docs,"]),
      "test_builder: inserted lines = the branch's added lines + dev's four entries re-flowed")
loop = next(i for i, ln in enumerate(tm) if ln.startswith("    for fn in ("))
seq = []
for ln in tm[loop:]:
    seq += [t.strip(" ,():") for t in ln.replace("for fn in (", "").split(",") if t.strip(" ,():")]
    if ln.rstrip().endswith("):"):
        break


def loop_of(lines):
    i = next(k for k, ln in enumerate(lines) if ln.startswith("    for fn in ("))
    out = []
    for ln in lines[i:]:
        out += [t.strip(" ,():") for t in ln.replace("for fn in (", "").split(",") if t.strip(" ,():")]
        if ln.rstrip().endswith("):"):
            return out


sp, sd = loop_of(tp), loop_of(td)
check(len(seq) == len(set(seq)), f"test_builder: {len(seq)} loop entries, no duplicate")
check(set(seq) == set(sp) | set(sd), "test_builder: loop = union of both sides' entries")
check(seq[0] == "test_commercial_timing_grade" and seq[1:5] == sd[:4] and seq[5:] == sp[1:] == sd[4:],
      "test_builder: branch entry first (as on branch), dev's four next (as on dev), common tail unchanged")
defs = [ln for ln in tm if ln.startswith("def test_commercial_timing_grade")]
check(len(defs) == 1, "test_builder: test_commercial_timing_grade defined once")
print(f"RESULT {'PASS' if not FAIL else 'FAIL'} failures={len(FAIL)}")
sys.exit(1 if FAIL else 0)
