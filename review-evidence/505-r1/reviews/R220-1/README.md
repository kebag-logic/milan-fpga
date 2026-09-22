# R220 round 1 evidence for PR #505 (issue #407)

Exact head: `6af65a151663e1301f1983a6c9d22650a0b35da9`.
Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
Candidate tree: `9983ea19387ff054aa5baf7bd881cd24e46176bc`.

The report is `R220-505-r1-REPORT.md` in this directory.

## Contents

- `pr505-full.diff`: the raw `git diff` from the base to the head.
- `SHA256SUMS`: the hashes of every file here except itself.
- `logs/`: every R220 command output cited by the report.
- `probes/`: the R220 probe scripts that produced those logs.
- `public-state/`: read-only snapshots of the GitHub state:
  - issue #407 and its comments;
  - PR #505 and its comments;
  - scratch PR #506, its commits and its diff against the candidate;
  - hosted check runs at the head, taken at 05:19 UTC.

## Scope of the probes

Every probe loads `scripts/ci_events.py` as a module. It then either mutates
in-memory parsed worlds, or runs the checker with `--root` against scratch
copies of the five contract files outside the tracked tree. Weakened
comparators (the M0 to M10 and M5b mutants) are monkeypatched in memory
only. No tracked file, submodule or index entry was edited.

## Reproduce

Two shell variables are used below:

- `REPO` is a clean checkout at the exact head, with its submodules at their
  gitlinks.
- `SCRATCH` is any empty directory.

1. Build the scratch copies:

   ```sh
   cd "$REPO"
   for t in head base; do
     rev=HEAD; [ $t = base ] && rev=b17580b91deb11f3441dfc5d7f9fafe539d929b8
     for f in .github/workflows/rtl.yml .github/workflows/rtl-fast.yml \
              .github/workflows/docs.yml .github/workflows/elaborate.yml \
              docs/testing/CI_WORKFLOWS.md scripts/ci_events.py; do
       mkdir -p "$SCRATCH/$t/$(dirname $f)"
       git show $rev:$f > "$SCRATCH/$t/$f"
     done
   done
   ```

2. Run the head's own gates:

   ```sh
   python3 scripts/ci_events.py --check
   python3 scripts/ci_events.py --selftest
   python3 probes/tally_selftest.py <selftest log>
   ```

3. Run the independent probes. Each takes the repository root as its
   argument.
   - Pass `.` from `$REPO` to `independent_census.py`,
     `vacuity_and_mutants.py`, `full_selftest_under_mutant.py
     {real|prefix|sorted|removed}`, `nonlast_mutants.py`,
     `m5b_accepts_ac5.py`, `m5b_exposure.py`, `nonlast_census.py` and
     `robustness.py`.
   - `arm_preservation.py`, `ast_compare.py` and `whitespace_overwrite.py`
     read `/tmp/r220-pristine/{base,head}`. Edit that path to your
     `$SCRATCH`.
   - `ac5_receipts.py` takes the extracted public evidence directory
     `review-evidence/505-r1` from commit
     `6fdc390cc703cb68438698329c5bc290d8a1c471`.

The native AC5 analogue, the shape-gate probe and the maintenance simulation
used shell edits on scratch copies. The exact edits are recorded at the top
of `logs/native-ac5-analogue.log`, `logs/shape-gate-pin-probe.log` and
`logs/maintenance-sim.log`, and in the report.

## Not run by R220

The following were not run: Docker/act, hardware, a full RTL, processor or
BDD sweep, dependency installation, commits, pushes and public writes.

The AC5 act results belong to the manager's receipts. R220 re-read the raw
logs and checked their published hashes.
