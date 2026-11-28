#!/usr/bin/env python3
"""privacy_probes.py REPO WORK: base/head privacy gate runs, real-commit probes in a disposable clone,
hash-seed independence of the self-test, and planted defects in copies of the head gate (each must fail --selftest
or the history run). Read-only on REPO; everything is written under WORK."""
import os, shutil, subprocess, sys
from pathlib import Path
repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
BASE, HEAD = "5a07d9b7d87298f04b15aa28f0304ec88b0aef81", "a8551cdd3cf715c52cca164a57d6d7f022e62c00"
shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
clone = work / "clone"
def sh(*a, cwd=None, env=None):
    r = subprocess.run(a, cwd=cwd, env=env, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()
sh("git", "clone", "-q", "--no-local", str(repo), str(clone))
fails = []
def expect(label, rc, out, want_rc):
    ok = (rc == 0) == (want_rc == 0)
    print(f"{'OK ' if ok else 'BAD'} {label}: rc {rc} (want {'0' if want_rc == 0 else 'nonzero'})\n    " + out.replace("\n", "\n    "))
    if not ok: fails.append(label)
def gate(script, *args, cwd=clone, env=None):
    return sh(sys.executable, "-I", str(script), *args, cwd=cwd, env=env)
head_gate = work / "head_check_privacy.py"; base_gate = work / "base_check_privacy.py"
head_gate.write_bytes(subprocess.check_output(["git", "show", HEAD + ":scripts/check_privacy.py"], cwd=repo))
base_gate.write_bytes(subprocess.check_output(["git", "show", BASE + ":scripts/check_privacy.py"], cwd=repo))
# The gate resolves ROOT from its own path, so each run uses a copy placed at clone/scripts/check_privacy.py.
target = clone / "scripts/check_privacy.py"
def run_as(src, *args, env=None):
    shutil.copyfile(src, target)
    try:
        return gate(target, *args, env=env)
    finally:
        sh("git", "checkout", "-q", "--", "scripts/check_privacy.py", cwd=clone)
print("== 1. base and head")
sh("git", "checkout", "-q", "--detach", BASE, cwd=clone)
expect("base gate on base history (the defect)", *run_as(base_gate), 1)
expect("base self-test", *run_as(base_gate, "--selftest"), 0)
expect("head gate on base history (exemption alone repairs main)", *run_as(head_gate), 0)
sh("git", "checkout", "-q", "--detach", HEAD, cwd=clone)
expect("head gate on head history", *gate(target), 0)
expect("head self-test", *gate(target, "--selftest"), 0)
print("== 2. self-test independent of set order")
for seed in ("0", "1", "2", "3", "12345", "random"):
    env = dict(os.environ, PYTHONHASHSEED=seed)
    rc, out = sh(sys.executable, str(target), "--selftest", cwd=clone, env=env)
    expect(f"head self-test PYTHONHASHSEED={seed}", rc, out, 0)
print("== 3. real commits on top of head, in the disposable clone")
def commit(msg, name, email):
    env = dict(os.environ, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email)
    sh("git", "commit", "-q", "--allow-empty", "-m", msg, cwd=clone, env=env)
    return sh("git", "rev-parse", "HEAD", cwd=clone)[1]
for label, msg, who, want in (
        ("one-line holder commit", ["Probe subject"], ("hackerman-kl", "hackerman-kl@kebag-logic.com"), 0),
        ("two-paragraph holder commit (non-exempt)", ["Probe subject", "Body"], ("hackerman-kl", "hackerman-kl@kebag-logic.com"), 1),
        ("one-line foreign identity commit", ["Probe subject"], ("someone", "a@b.c"), 1)):
    sh("git", "checkout", "-q", "--detach", HEAD, cwd=clone)
    args = []
    for m in msg:
        args += [m]
    env = dict(os.environ, GIT_AUTHOR_NAME=who[0], GIT_AUTHOR_EMAIL=who[1], GIT_COMMITTER_NAME=who[0], GIT_COMMITTER_EMAIL=who[1])
    cmd = ["git", "commit", "-q", "--allow-empty"] + sum((["-m", m] for m in msg), [])
    sh(*cmd, cwd=clone, env=env)
    expect("history + " + label, *gate(target), want)
sh("git", "checkout", "-q", "--detach", HEAD, cwd=clone)
print("== 4. planted defects in copies of the head gate")
src = head_gate.read_text()
rule = 'commit not in TWO_LINE_MERGES and len([line for line in lines[2:] if line.strip()]) != 1'
plants = [
    ("drop the #41 exemption", '"d7e6a2a19a57a8277cd26042557a8c99f2ee5496", "5a07d9b7d87298f04b15aa28f0304ec88b0aef81"}', '"d7e6a2a19a57a8277cd26042557a8c99f2ee5496"}', "history"),
    ("drop the #29 exemption", '{"d7e6a2a19a57a8277cd26042557a8c99f2ee5496", ', '{', "history"),
    ("#41 exemption typed one digit off", '5a07d9b7d87298f04b15aa28f0304ec88b0aef81"}', '5a07d9b7d87298f04b15aa28f0304ec88b0aef80"}', "history"),
    ("no one-line rule", rule, 'False', "selftest"),
    ("exemption by 7-digit prefix", 'commit not in TWO_LINE_MERGES', 'commit[:7] not in {m[:7] for m in TWO_LINE_MERGES}', "selftest"),
    ("exemption also skips identity", 'if commit != OWNER_SQUASH and not identity_ok(lines):', 'if commit != OWNER_SQUASH and commit not in TWO_LINE_MERGES and not identity_ok(lines):', "selftest"),
    ("all-zero commit exempted", 'TWO_LINE_MERGES = {', 'TWO_LINE_MERGES = {"' + "0" * 40 + '", ', "selftest"),
    ("any 'Merge' subject exempted", 'commit not in TWO_LINE_MERGES and', '(commit not in TWO_LINE_MERGES and not lines[2:3] == ["Merge"]) and', "selftest"),
    ("self-test near miss uses the exact merge", 'near = merge[:-1] + ("0" if merge[-1] != "0" else "1")', 'near = merge', "selftest"),
    ("self-test drops the exemption loop", 'for merge in sorted(TWO_LINE_MERGES):', 'for merge in sorted(TWO_LINE_MERGES)[:0]:', "selftest-count"),
    ("self-test checks only the first exempt merge", 'for merge in sorted(TWO_LINE_MERGES):', 'for merge in sorted(TWO_LINE_MERGES)[:1]:', "selftest-count"),
    ("one-line rule counts blank lines (pre-existing line, outside the delta)", 'if line.strip()]) != 1', ']) != 1', "info-both"),
]
for name, a, b, kind in plants:
    assert src.count(a) == 1, name
    p = work / ("plant-" + name.replace(" ", "_").replace("'", "").replace("#", "") + ".py")
    p.write_text(src.replace(a, b, 1))
    if kind == "history":
        expect(f"plant [{name}] head history run refuses", *run_as(p), 1)
    else:
        rc, out = run_as(p, "--selftest")
        if kind == "info-both":
            hrc, hout = run_as(p)
            print(f"INFO plant [{name}] self-test: rc {rc}: {out}; history run: rc {hrc}: {hout.splitlines()[-1]}")
            continue
        if kind == "selftest-count":
            # The self-test cannot fail on its own shrinkage; record the count so the 17 controls are pinned by review.
            print(f"INFO plant [{name}] self-test: rc {rc}: {out}  (count drops below 17: detectable only by the recorded count)")
        else:
            expect(f"plant [{name}] self-test refuses", rc, out, 1)
print("RESULT " + ("all probes as expected" if not fails else "unexpected: " + "; ".join(fails)))
sys.exit(bool(fails))
