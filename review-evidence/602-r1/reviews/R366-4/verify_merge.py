#!/usr/bin/env python3
"""Check that head = clean merge of dev into the lane + the conflict resolution
+ exactly the two authorised rewordings, and nothing else.

Usage: verify_merge.py CLONE
Exit 0 only when every assertion holds; every result is printed.
"""
import subprocess
import sys

BASE = "6d5ebd7357c1e468e446f18a61527c5be6118a04"
LANE = "6b2ebd1c435136966f84ffc16d28a80c7d6b9387"
DEV = "0eff6d2ee3818a6d2b1f1fdcd0084d81b28f247a"
MERGE = "b2f48e0c15732744c71eac90de136b86f099420e"
DOC1 = "45e6cf1a37358914b7ebc4c2e0d2b3905970bed3"
HEAD = "6c5ca18f12191a252447ec7c7c75363b851f2771"
CONFLICT = "docs/design/GM_LOSS_RECOVERY.md"
SOAK_FILES = ["tb/tools/torture_campaign.py", "tb/tools/torture_release_mutants.py",
              "tests/features/torture_campaign_plan.feature",
              "tests/steps/torture_release_steps.py"]
OLD3 = ["The current image still toggles `mr` on PHC steps.",
        "A soak containing one therefore fails the step-only check.",
        "This remains until #602's RTL change lands."]
NEW3 = ["A PHC-only re-base leaves `mr` unchanged.",
        "The existing `tu` path signals that gPTP discontinuity.",
        "It adds no step-only MEDIA_RESET increment."]

CLONE = sys.argv[1]
fails = 0


def git(*args: str, ok=(0,)) -> str:
    out = subprocess.run(["git", "-C", CLONE, *args], capture_output=True, text=True)
    if out.returncode not in ok:
        raise SystemExit(f"git {args} rc={out.returncode}: {out.stderr}")
    return out.stdout


def check(cond: bool, what: str) -> None:
    global fails
    fails += not cond
    print(f"[{'ok' if cond else 'FAIL'}] {what}")


def changed(a: str, b: str) -> set[str]:
    return set(git("diff", "--no-renames", "--name-only", a, b).split())


def entry(commit: str, path: str) -> str:
    return git("ls-tree", commit, "--", path).strip()


check(git("rev-parse", "HEAD").strip() == HEAD, "clone HEAD is the reviewed head")
check(git("rev-parse", f"{HEAD}^{{tree}}").strip() == "90653220be7a737e3239a56f5621554081c9a8c1",
      "head tree is 90653220")
check(git("rev-parse", f"{MERGE}^1", f"{MERGE}^2").split() == [LANE, DEV], "merge parents = lane, dev")
check(git("merge-base", LANE, DEV).strip() == BASE, "merge base is the lane base 6d5ebd73")
check(git("rev-parse", f"{HEAD}^").strip() == DOC1 and git("rev-parse", f"{DOC1}^").strip() == MERGE,
      "history is merge -> 45e6cf1a -> head, linear")
for c in (MERGE, DOC1, HEAD):
    msg = git("log", "-1", "--format=%B", c).strip()
    check("\n" not in msg, f"{c[:8]} message is one line with no trailers: {msg!r}")

auto = git("merge-tree", "--write-tree", "--name-only", LANE, DEV, ok=(0, 1)).splitlines()
auto_tree, conflicted = auto[0], [p for p in auto[1:] if p and not p.startswith("Auto-merging")
                                  and not p.startswith("CONFLICT")]
check(conflicted == [CONFLICT], f"reproduced merge conflicts only in {CONFLICT}: {conflicted}")
diff_auto = changed(auto_tree, MERGE)
check(diff_auto == {CONFLICT}, f"merge tree differs from the automatic merge only there: {sorted(diff_auto)}")
check(entry(MERGE, CONFLICT) == entry(LANE, CONFLICT),
      "conflict resolved to the lane's (#602) text byte for byte")
dev_side = git("diff", "--no-renames", BASE, DEV, "--", CONFLICT)
check(dev_side.count("\n+| ") == 1 and dev_side.count("\n-| ") == 1,
      "dev changed exactly one row of the recovery doc")
check("The current image still toggles" in dev_side and "until #602's RTL change lands" in dev_side,
      "that dev row is the pre-602 'current image still toggles' wording")

post = changed(MERGE, HEAD)
check(post == {"REQUIREMENTS.md", "docs/testing/TESTING.md"},
      f"after the merge only the two authorised files change: {sorted(post)}")
for commit, path, indent in ((DOC1, "docs/testing/TESTING.md", ""), (HEAD, "REQUIREMENTS.md", "  ")):
    d = git("diff", "-U0", f"{commit}^", commit)
    minus = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    plus = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")]
    check(changed(f"{commit}^", commit) == {path}, f"{commit[:8]} touches only {path}")
    check(minus == [indent + s for s in OLD3] and plus == [indent + s for s in NEW3],
          f"{commit[:8]} replaces exactly the three stale lines with the three post-602 lines")
    check(d.count("\n@@ ") + d.startswith("@@") <= 1 and d.count("@@ -") == 1, f"{commit[:8]} is one hunk")

lane_d, dev_d = changed(BASE, LANE), changed(BASE, DEV)
both = lane_d & dev_d
print(f"lane-only {len(lane_d - dev_d)}, dev-only {len(dev_d - lane_d)}, both {len(both)}: {sorted(both)}")
special = {CONFLICT, "REQUIREMENTS.md", "docs/testing/TESTING.md"}
for p in sorted(dev_d - lane_d - special):
    check(entry(HEAD, p) == entry(DEV, p), f"dev-only path equals dev at head: {p}")
for p in sorted(lane_d - dev_d - special):
    check(entry(HEAD, p) == entry(LANE, p), f"lane-only path equals lane at head: {p}")
for p in sorted(both - special):
    check(entry(HEAD, p) == git("ls-tree", auto_tree, "--", p).strip(),
          f"shared path equals the automatic three-way merge at head: {p}")
for p in SOAK_FILES:
    check(entry(HEAD, p) == entry(DEV, p), f"#593 soak file unchanged from dev: {p}")
for p in ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "external"):
    check(entry(HEAD, p) == entry(DEV, p), f"gitlink equals dev: {entry(HEAD, p)}")
gen = [p for p in git("ls-tree", "-r", "--name-only", HEAD).split()
       if "/gen/" in p or p.startswith("configs/generated/")]
diff_gen = [p for p in gen if entry(HEAD, p) != entry(DEV, p)]
check(not diff_gen and gen, f"{len(gen)} committed generated files equal dev's: {diff_gen}")
extra = changed(DEV, HEAD) - lane_d - special
check(not extra, f"head differs from dev only on lane paths: {sorted(extra)}")
print(f"\n{fails} failed assertion(s)")
sys.exit(1 if fails else 0)
