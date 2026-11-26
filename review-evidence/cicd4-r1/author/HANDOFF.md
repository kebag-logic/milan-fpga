# [A839] CICD improvement, round 4 (#1008): handoff

**Status (2026-11-26, CET): REVIEW READY at `5b5b076514` (lane `1008-ci-30min`). Partial: the PR body
says "Relates to #1008".** Nothing pushed, nothing posted.
**ETA:**
- Nothing of mine is running. The last unit, `milan-cicd4-a839-gates3`, ended with 39 of 39 gates at rc 0
  (`receipts/gates/summary`).
- The rest of #1008 is in "Open" below: roughly one more round.

## Head

`$LANES/cicd-1008`, branch `1008-ci-30min` from dev-soft-core `c34e7d8b06`. Eight commits, each with a
one-line subject and no trailer:

1. `964398a0` `--campaign-shard` and its dispatch proof (`campaign_cases`).
2. `3fbfa3bc` census legs and judge (`census_legs.py`; `census_selftest.jobs_for` factored out).
3. `92652448` `gptp_shadow` re-keyed to 517 s.
4. `cfa15fea` the generator, contract and self-test changes:
   - generator: `ci_fast_legs.py`, the shared Yosys restore and the docs workers;
   - contract: `check_fast_legs` and its arms;
   - self-test: `ci_fast_legs_selftest.py`;
   - the regenerated workflows.
5. `ab11a1d2` AECP and SRP legs (two each).
6. `530149b5` the policy page (`docs/testing/CI_WORKFLOWS.md`).
7. `f7d7fe5d` code-quality fixes (the idiom gate).
8. `5b5b0765` the fast-leg contract arms run against the generated graph, in a stage of their own.
   At `f7d7fe5d` the event self-test stopped with `KeyError: 'publication-census-legs'`: the arms ran on the
   template projection, where the legs do not exist. That log is kept as `receipts/gates-f7d7fe5d-*`.

The untracked `dispatch-build/` in the lane is written into the working directory by the existing #716 dispatch
proof (`test_ctrl_firmware_shards.inventory`). It is not part of the change and was left alone.

## What the previous session of this key left, and what I did with it

The earlier session's uncommitted work was saved first, to
`$VALIDATION_STORAGE/cicd4-a839/prev/{tracked.patch,untracked.tar}`. I kept its design:
- the generator-side legs, so the templates keep the complete commands;
- the campaign shard;
- the census legs;
- the unit matrix.

I fixed or changed the following:
- **Failing self-tests:** the fast-tool job-order assertion and the census budget owner.
- **Aggregate shell:** the pair the generator added had a broken indent.
- **Census Yosys:** each census leg would have rebuilt Yosys on a cache miss. The legs now restore
  `yosys-tool`'s exact tree, and the generator refuses a recipe that differs.
- **Docs layout:** five workers, not six; the contract gates share worker 3 with the firmware controls.
- **`gptp_shadow` re-key:** the earlier figure of 672 s came from run 45735453538, which is at the #1013 lane's
  gptp-processor pin 3ce71b76. The base's pin is 1213ac5b, whose two runs give 478 s and 517 s.
- **Added this round:**
  - the AECP and SRP legs;
  - the dispatch proof for campaign legs;
  - the contract items and arms;
  - the policy text;
  - the local verdict-identity runs and the planted failures.

## Results

- **Gates:** 39 of 39 rc 0 in a clean clone at `5b5b0765` (`receipts/gates/summary`). The event self-test passes
  2390 contract items and 6161 arms, the 22 fast-leg arms among them. The generator, leg, dispatch and suite
  self-tests pass, and so do the code-quality, documentation and TOC gates.

- **Budget:** each divided job's slowest leg projects at most 1276 s hosted, which is at most 1800 s at 1.41×.
  See the table in `PR-BODY.md`, from `receipts/tools/project.py`.
- **Verdict identity** against serial hosted run 45657606423, whose `sw/`, `hdl/`, `configs/` and submodules equal
  the base's (`receipts/identity/`):
  - control: 844 of 844 identical;
  - AECP: 398 of 398;
  - SRP: 662 of 662 defect verdicts, and each leg's two pin-control lines equal the serial run's;
  - census: 22 check lines and 222 arm and rule lines identical, one only by a Yosys heap address.
- **Planted failures:**
  - 7 in the real census receipts, each refused;
  - a failure and a cancellation of each of the five divided jobs fail the generated required-context shell;
  - 22 contract arms.
- **Profiles** (`receipts/profile4/`):
  - control leg: 88% of its CPU is compilation (C 56%, C++ 32%) and under 2% is running tests;
  - census leg: Python 34%, sv2v 40%, Yosys 26%.
  - Both are spread over many tool runs with no single hot spot, so splitting is the lever.
- **Runner-minutes** (means over the 20 runs, watchers included):
  - rtl-fast 263.9 → about 269.2;
  - docs 91.2 → about 94.5.

## For the manager

- **Which bound I used.** I read the bound as the issue states it: a hosted window of at most 1276 s, which is 30
  minutes at 1.41×. The prompt's "projection (x1.41) exceeds 1276 s" could also be read as "1.41 × hosted ≤ 1276".
  That would be a 905 s hosted bound, and most fast jobs would then be over it. Say if you meant that.
- **#1013's pin.** If #1013's pin (3ce71b76) lands first, `gptp_shadow` measured 672 s there in run 45735453538.
  That lane should re-key with its own two runs.
- **Hosted evidence.** Acceptance 1 of #1008 needs two hosted runs, so it can only be shown after a push. The
  first run after any workflow change rebuilds Verilator in every Verilator job, because that key binds the
  workflow files (see "Open").

## Open (#1008 stays open)

1. A Verilator tool job, like `yosys-tool`, for rtl-fast, rtl-full and elaborate. Until then a workflow edit
   rebuilds Verilator inside timed jobs:
   - `firmware-verilator`: 1630 s;
   - `elaborate-gates-4`: 1422 s;
   - rtl-full shards: up to 1702 s on the miss runs, and at most 1253 s without a miss.
2. `test_baremetal_profile_contract`: up to 1157 s alone. It sets `elaborate-gates-0` (1343 s), and with builder
   leg 1 (1300 s) `elaborate-gates-1` (1453 s).
3. rtl-full `Yosys shard 0/4`: 1451 s, dominated by one portability item.
4. `docs-gates-1`: measured at most 1111 s, but 1302 s by the component-maxima rule.

## Said plainly

- **Commits the legs ran at.** The control legs ran at `3fbfa3bc`, the census, AECP and SRP legs at `530149b5`.
  After `3fbfa3bc` the firmware driver changed only on its SRP path and in the phase check of `--campaign-shard`,
  and the control phase's dispatch proof is re-run by `ci_fast_legs_selftest` at the head. Nothing in `sw/`
  changed after `530149b5`.
- **Not run:**
  - an act replay;
  - a hosted injected failure;
  - a local run of `firmware-unit`'s legs. Their commands are the template's, byte for byte, which the self-test
    holds.
- **Local timing.** The host was loaded (load 70-100). The local legs ran about 3.5× slower per mutant than the
  hosted runner, so I used them only for shares, not for absolute figures.
- **Removals.** Every `rm` is logged first in `disk-cleanup.log`, with the reason:
  - the earlier session's partial build directories and empty perf files;
  - three of my own failed starts, each a few seconds long (PATH order, the unpinned sv2v, the perf buffer).
- **Scratch:** `$VALIDATION_STORAGE/cicd4-a839` is about 3-5 GB; `/data` had 31 GB free at the last check.

REVIEW READY 5b5b076514
