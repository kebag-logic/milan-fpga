#!/usr/bin/env python3
"""Remove each correction in a disposable export and require its owning arm to go red.

Usage: mutation_controls.py CHECKOUT REVISION OUT_DIR
Exports REVISION (git archive, no submodules needed: fixtures build their own
pinned dependencies) once per mutation, applies exactly one textual removal
(asserted to match once), then runs each named arm of the committed tests in its
own process. The unmutated export must pass every arm (baseline). Writes
OUT_DIR/mutation-controls.json and one log per (mutation, arm). Exit 0 only when
the baseline is green and every mutation turns every one of its arms red.
"""
import json
import subprocess
import sys
import tarfile
import io
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REDIRECTS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
             "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE", "GIT_CONFIG_PARAMETERS",
             "GIT_CONFIG_COUNT", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM")
OWNER = "scripts/owned_process.py"
INPUTS = "tb/verilator/gptp_shadow/private_inputs.py"
FACILITY_CHECK = '''    missing = [name for name, present in (
        ("prctl", prctl is not None),
        ("os.pidfd_open", hasattr(os, "pidfd_open")),
        ("signal.pidfd_send_signal", hasattr(signal, "pidfd_send_signal"))) if not present]
'''
REDIRECT_BLOCK = '''    redirects = sorted(name for name in os.environ if name in REDIRECTS)
    if redirects:
        raise InputRefused(f"Git environment redirects the checkout: {', '.join(redirects)}")
'''
OLD_ALLOWLIST = '''    allowed = {"GIT_NO_REPLACE_OBJECTS", "GIT_CONFIG_NOSYSTEM", "GIT_TERMINAL_PROMPT", "GIT_PAGER"}
    overrides = sorted(name for name in os.environ if name.startswith("GIT_") and name not in allowed)
    if overrides:
        raise InputRefused(f"Git environment overrides are not accepted: {', '.join(overrides)}")
'''
RECORD_PARSE = '''        metadata, tab, name = row.partition("\\t")
        fields = metadata.split(" ")
        if not tab or not name or len(fields) != 3 or not all(fields):
            raise InputRefused(f"unreadable Git identity record: {row[:120]!r}")
        mode, second, third = fields
'''
OLD_RECORD_PARSE = '''        metadata, name = row.split("\\t", 1)
        mode, second, third = metadata.split()
'''
BROAD_SCOPE = '''    names |= {name for name in _git(repo, owner, "ls-files", "-z", "--", "hdl", "tb/common",
                                    "tb/verilator/gptp_shadow").split("\\0") if name}
    return names
'''
PIN_CHECK = '''        if mode != "160000" or _git(root, owner, "rev-parse", "HEAD").strip() != revision:'''

SIGNAL_ARMS = [f"sweep:hard_stop:{how}" for how in ("KILL", "HUP", "HUP-group")]
FACILITY_ARMS = [f"{runner}:unsupported:{mode}" for runner in ("sweep", "lifecycle")
                 for mode in ("no-prctl", "no-pidfd-open", "no-pidfd-signal")]

#: (id, finding, file, old text, new text, arms that must go red)
MUTATIONS = [
    ("F1-commands-outlive-owner", "R256-2 F1 / R257-1 F1", OWNER,
     "preexec_fn=self._die_with_owner,", "", SIGNAL_ARMS + ["lifecycle:interrupted:SIGKILL"]),
    ("F3b-no-facility-resolution", "R257-1 F3", OWNER, FACILITY_CHECK, "    missing = []\n", FACILITY_ARMS),
    ("F2-original-allowlist", "R256-2 F2 / R257-1 F2", INPUTS, REDIRECT_BLOCK, OLD_ALLOWLIST,
     ["lifecycle:accepted:presentation", "lifecycle:accepted:scrubbed"]),
    ("F2-git-variables-reach-identity-commands", "R256-2 F2 / R257-1 F2", INPUTS,
     "--literal-pathspecs\", \"-C\", str(root), *args], env=env)",
     "--literal-pathspecs\", \"-C\", str(root), *args], env=None)", ["lifecycle:accepted:scrubbed"]),
] + [
    (f"F2-redirect-{name}-accepted", "R256-2 F2 / R257-1 F2", INPUTS, f'"{name}",', "",
     [f"lifecycle:refusal:git-env-{name}"]) for name in REDIRECTS
] + [
    ("F3-directory-scope-population", "R256-2 F3", INPUTS, "                pending.append(header)\n    return names\n",
     "                pending.append(header)\n" + BROAD_SCOPE,
     ["lifecycle:accepted:unrelated", "lifecycle:interrupted:SIGTERM"]),
    ("F3-no-include-walk", "R256-2 F3", INPUTS, "    pending = sorted(names)\n", "    pending = []\n",
     ["lifecycle:refusal:dirty-header", "lifecycle:interrupted:SIGTERM"]),
    ("F3-targets-need-not-be-inputs", "R256-2 F3", INPUTS,
     "    if absent:\n        raise InputRefused(f\"mutation target or anchor is not a build input: {', '.join(absent)}\")\n",
     "", ["lifecycle:refusal:undeclared-target"]),
    ("F4-copied-dependency-accepted", "R256-2 F4", INPUTS, PIN_CHECK, '        if mode != "160000":',
     ["lifecycle:refusal:copied-dependency"]),
    ("F5-stderr-parsed-as-records", "R256-2 F5", INPUTS,
     "status, output = owner.run(argv, cwd=cwd, env=env, stderr=diagnostics)",
     "status, output = owner.run(argv, cwd=cwd, env=env)", ["lifecycle:accepted:git-stderr"]),
    ("F5-unreadable-record-crashes", "R256-2 F5", INPUTS, RECORD_PARSE, OLD_RECORD_PARSE,
     ["lifecycle:refusal:git-garbage"]),
    # Optional reviewer suggestions (R256-2 S1, R257-1 S3): each guard is now
    # load-bearing under its own named arm, because refusals assert their reason.
    ("S-no-directory-link-check", "R256-2 S1 / R257-1 S3", INPUTS,
     "        if linked:\n            raise InputRefused(f\"input directory is missing or linked: {current}\")\n", "",
     ["lifecycle:refusal:parent-link", "lifecycle:refusal:dependency-link"]),
    ("S-no-index-comparison", "R257-1 S3", INPUTS,
     "    if expected != indexed:\n        raise InputRefused(f\"index differs from {revision}: {root}\")\n", "",
     ["lifecycle:refusal:staged", "lifecycle:refusal:untracked"]),
]

RUNNER = r'''
import pathlib, signal, sys, tempfile
sys.path.insert(0, "scripts")
sys.path.insert(0, "tb/verilator/gptp_shadow")
from owned_process import OwnedProcesses
import {module} as t
arg = {arg!r}
if arg.startswith("SIG"):
    arg = getattr(signal, arg)
with tempfile.TemporaryDirectory(prefix="mutation-arm-") as scratch:
    with OwnedProcesses():
        with OwnedProcesses():
            t.{function}(pathlib.Path(scratch).resolve(), arg)
print("ARM PASS")
'''


def export(checkout, revision, target):
    data = subprocess.run(["git", "-C", str(checkout), "archive", revision], capture_output=True, check=True).stdout
    target.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target, filter="tar")


def run_arm(tree, arm, log):
    runner, function, arg = arm.split(":")
    module = {"sweep": "test_suite_cancellation", "lifecycle": "test_mutant_lifecycle"}[runner]
    code = RUNNER.format(module=module, function=function, arg=arg)
    with log.open("wb") as output:
        try:
            status = subprocess.run([sys.executable, "-c", code], cwd=tree, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=240).returncode
        except subprocess.TimeoutExpired:
            status = "timeout"
    return status


def main():
    checkout, revision, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    trees = out / "trees"
    jobs = []
    baseline_arms = sorted({arm for *_rest, arms in MUTATIONS for arm in arms})
    base_tree = trees / "baseline"
    export(checkout, revision, base_tree)
    jobs += [("baseline", arm, base_tree) for arm in baseline_arms]
    applied = {}
    for ident, finding, path, old, new, arms in MUTATIONS:
        tree = trees / ident
        export(checkout, revision, tree)
        text = (tree / path).read_text()
        count = text.count(old)
        applied[ident] = dict(finding=finding, file=path, matches=count)
        if count != 1:
            continue
        (tree / path).write_text(text.replace(old, new, 1))
        jobs += [(ident, arm, tree) for arm in arms]
    logs = out / "logs"
    logs.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {(ident, arm): pool.submit(run_arm, tree, arm, logs / f"{ident}--{arm.replace(':', '-')}.log")
                   for ident, arm, tree in jobs}
    results = {key: future.result() for key, future in futures.items()}
    report = dict(revision=revision, baseline={arm: results[("baseline", arm)] for arm in baseline_arms},
                  mutations=[])
    ok = all(status == 0 for status in report["baseline"].values())
    for ident, finding, path, _old, _new, arms in MUTATIONS:
        arm_status = {arm: results.get((ident, arm), "not applied") for arm in arms}
        red = applied[ident]["matches"] == 1 and all(status not in (0, "not applied") for status in arm_status.values())
        ok = ok and red
        report["mutations"].append(dict(id=ident, finding=finding, file=path, applied=applied[ident]["matches"] == 1,
                                        arms=arm_status, all_arms_red=red))
    report["verdict"] = "PASS" if ok else "FAIL"
    (out / "mutation-controls.json").write_text(json.dumps(report, indent=1) + "\n")
    for row in report["mutations"]:
        print(f"{'RED ' if row['all_arms_red'] else 'MISS'} {row['id']:48s} {row['arms']}")
    print("baseline:", report["baseline"])
    print("verdict:", report["verdict"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
