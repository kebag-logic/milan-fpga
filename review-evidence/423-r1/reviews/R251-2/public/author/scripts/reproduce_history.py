"""Verify public PR62 patch pairs, topology, current paths and CLI verdicts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
checkout = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(checkout / "scripts"))
import check_merge_containment as mc
import merge_containment_replay as proof
from merge_containment_selftest_scratch import quiet_git

head = "3db86812096830fada2f5f276fa5f4d9f37d1d14"
pr61 = "9790ac736e6d10301ad814ffdf73dbe37b59768b"
merge = "f27b45500cb02a5277b5cb32cef408658c1f914e"
targets = ("f0f1c055ee5226f08e656c27cb1bf4c355be11ae", "c1b617435824929a790739ea8585c3fe1a328cc0")
pairs = ((head, "5602e70bb4cf70c2e0e39e846e26925e27659e32", "fa20a2516a4d866a859506c5396779fb98bbafe943e4de2651e9ec252bca996f"),
         (pr61, "20927af74752620b2ad0f973e8be3203994b5547", "d3d164b309e376ea06a3734e8452dd5668c4721d0462dc0656af05d6b3c155b3"))
os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
os.chdir(root / "donor.git")

def git(*args):
    p = subprocess.run(("git", "--no-replace-objects", *args), capture_output=True, check=True)
    return p.stdout

def cli(checker, branch, target):
    command = [sys.executable, "-B", "-I", str(checker), "--no-fetch", "--base", target, branch]
    p = subprocess.run(command, capture_output=True, text=True)
    word = p.stdout.strip().split()[0] if p.stdout.strip() else "no verdict"
    return dict(command=command, exit=p.returncode, word=word, stdout=p.stdout, stderr=p.stderr)

record = dict(patches=[], targets=[])
for source, replay, expected_hash in pairs:
    patches = []
    for commit in (source, replay):
        parent = git("rev-parse", commit + "^").decode().strip()
        patches.append(git("diff", "--no-ext-diff", "--no-textconv", "--no-renames", parent, commit))
    assert patches[0] == patches[1]
    digest = hashlib.sha256(patches[0]).hexdigest()
    assert digest == expected_hash
    assert mc._verbatim_patch_id(source) == mc._verbatim_patch_id(replay)
    record["patches"].append(dict(source=source, replay=replay, sha256=digest,
                                  patch_id=mc._verbatim_patch_id(source)[0]))
for target in targets:
    assert proof._redundant_merge_shape(head, target, mc._git)
    assert mc._linear_patches_contained(head, target) == (True, None)
    ancestor = git("merge-base", "--all", head, target).decode().strip()
    unproved = proof._retained_at_tip(head, target, mc._git)
    assert unproved == ["'tb/tsngen/mutants.py'", "'tb/verilator/gaskets/mutants.py'"]
    paths = git("diff", "--name-only", "--no-renames", "-z", ancestor, head).decode().strip("\0").split("\0")
    per_path = {}
    for path in paths:
        entries = [proof._tree_entry(commit, path) for commit in (ancestor, target, head)]
        per_path[path] = dict(entries=entries, retained=proof._entry_retained(*entries))
    original = cli(root / "baseline/check_merge_containment.py", head, target)
    candidate = cli(checkout / "scripts/check_merge_containment.py", head, target)
    linear = cli(checkout / "scripts/check_merge_containment.py", pr61, target)
    assert (original["exit"], original["word"]) == (1, "STRANDED")
    assert (candidate["exit"], candidate["word"]) == (1, "UNKNOWN")
    assert (linear["exit"], linear["word"]) == (0, "contained")
    record["targets"].append(dict(target=target, merge_base=ancestor,
                                   merge_parents=git("rev-list", "--parents", "--max-count=1", merge).decode().strip(),
                                   paths=per_path, unproved=unproved, baseline=original, production=candidate, linear=linear))
(root / "receipts/pr62-history.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))

probe_root = root / "probe-scratch"
probe_root.mkdir(exist_ok=True)
probe = root / "public/published-fixture-6181e900/probe/probe_ff_merge.py"
command = [sys.executable, "-B", str(probe), str(checkout / "scripts/check_merge_containment.py")]
with quiet_git():
    p = subprocess.run(command, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=str(probe_root),
                                GIT_AUTHOR_DATE="@1790000000 +0000", GIT_COMMITTER_DATE="@1790000000 +0000"), check=True)
probe_record = json.loads(p.stdout)
os.chdir(probe_record["fixture"])
for row in probe_record["cases"]:
    assert row["current_verdict"][0] is None
    assert row["existing_linear_proof"] == [True, None]
    row["cli"] = cli(checkout / "scripts/check_merge_containment.py", row["candidate"], row["base"])
    assert (row["cli"]["exit"], row["cli"]["word"]) == (1, "UNKNOWN")
(root / "receipts/published-probe.json").write_text(json.dumps(probe_record, indent=2) + "\n")
print("PR62 at both public targets remains UNKNOWN; PR61 remains contained.")
print("Both unchanged public probe cases remain UNKNOWN through the real CLI.")
