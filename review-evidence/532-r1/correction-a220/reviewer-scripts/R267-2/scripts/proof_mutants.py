#!/usr/bin/env python3
"""Reviewer mutation probe for scripts/act_slot_proof.sh (round R267-2, PR #533).

Each mutant is one exact, single-occurrence text replacement applied to a
private copy of the proof script under SCRATCH. The copy's own offline
`--selftest` is then run inside a network-less user namespace
(`unshare --user --map-current-user --net`), one mutant at a time. A mutant
is KILLED when that self-test exits non-zero and SURVIVED when it passes.
The tracked script in the clone is never modified.

usage: proof_mutants.py CLONE SCRATCH
"""
import pathlib
import shutil
import subprocess
import sys

MUTANTS = [
    # (id, description, old, new)
    ("P00", "no-op control: a comment word changes",
     "# Live proof for parallel act replay slots (#532).",
     "# Live proof for parallel act replay slots (#532) [mutant].", ),
    ("P01", "isolation: the slot's internet reachability is no longer required",
     '[ "$inside" = "container=refused published=refused internet=reached " ]',
     '[[ "$inside" == "container=refused published=refused "* ]]'),
    ("P02", "slot-0 collision: any refusal counts, not act's global names",
     'collide 0 "act-toolcache|already exist"',
     'collide 0 "REFUSED"'),
    ("P03", "complete: a run that printed every PASS counts whatever its exit status",
     '[ "$actual" = "exit 0$expected" ]',
     '[ "${actual#exit ?}" = "$expected" ]'),
    ("P04", "complete: a run whose FAILED line is followed by any exit status counts",
     'if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi',
     'if [ "${actual#exit ?}" = "$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi'),
    ("P05", "verify_runner: the recorded digest is not compared",
     'if [ "$actual" != "$sha" ] || [ -n',
     'if false || [ -n'),
    ("P06", "verify_runner: a writable runner install is accepted",
     '[ -n "$(find "$runner" -maxdepth 0 -perm /0222)" ]',
     'false'),
    ("P07", "verify_runner: a non-empty log directory is accepted",
     'if [ -n "$(ls -A "$logs")" ]; then',
     'if false; then'),
    ("P08", "isolation: the host-side reachability of both targets is not required (expected KILLED)",
     '&& [ "$outside" = "container=reached published=reached " ]; then',
     '; then'),
    ("P09", "overlap: neither run is required to be still unended (expected KILLED)",
     '&& ! ended parallel-a && ! ended parallel-b; then',
     '; then'),
    ("P10", "collide: a rival refused after the holder ended still counts (expected KILLED)",
     'if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \\',
     'if [ "$rival_status" = 2 ] \\'),
    ("P11", "remove_target: a surviving target network is not reported",
     'if [ -n "$containers$networks" ]; then',
     'if [ -n "$containers" ]; then'),
    ("P12", "parse_arguments: slot A may equal slot B or be slot 0",
     'if [ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]; then',
     'if false; then'),
    ("P13", "interrupt gate: the runner's PASS line is not required",
     "&& grep -q '^interrupt-selftest: PASS ' \"$log\" \\\n",
     ""),
]


def main() -> int:
    clone = pathlib.Path(sys.argv[1]).resolve()
    scratch = pathlib.Path(sys.argv[2]).resolve()
    source = (clone / "scripts" / "act_slot_proof.sh").read_text(encoding="utf-8")
    results = []
    for ident, described, old, new in MUTANTS:
        count = source.count(old)
        if count != 1:
            print(f"{ident} NOT-APPLIED ({count} matches): {described}", flush=True)
            results.append((ident, "NOT-APPLIED"))
            continue
        workdir = scratch / "proof-mutants" / ident
        if workdir.exists():
            shutil.rmtree(workdir)
        (workdir / "tmp").mkdir(parents=True)
        mutated = workdir / "act_slot_proof.sh"
        mutated.write_text(source.replace(old, new, 1), encoding="utf-8")
        run = subprocess.run(
            ["unshare", "--user", "--map-current-user", "--net", "--",
             "bash", str(mutated), "--selftest"],
            env={"PATH": "/usr/bin:/bin", "TMPDIR": str(workdir / "tmp"), "LC_ALL": "C.UTF-8"},
            capture_output=True, text=True, timeout=900,
        )
        (workdir / "selftest.out").write_text(run.stdout + run.stderr, encoding="utf-8")
        verdict = "KILLED" if run.returncode != 0 else "SURVIVED"
        failing = [line.strip() for line in run.stdout.splitlines() if line.startswith("  FAIL")]
        print(f"{ident} {verdict} (selftest rc {run.returncode}): {described}", flush=True)
        for line in failing:
            print(f"     {line}", flush=True)
        results.append((ident, verdict))
    print("SUMMARY " + " ".join(f"{i}={v}" for i, v in results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
