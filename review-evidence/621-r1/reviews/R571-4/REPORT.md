[R571] POSITIVE - exact head f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1

External independent review R571-4 of milan-fpga PR #707 (issue #621).

- Parent head: `f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1`, tree `f0f6817a7ded140dd22e14cd997c1c123bb02e1e`.
- Source base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Gitlinks: `gptp-processor` `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (donor PR Mister-M-alt/FPGA-gPTP #77, open, same head), `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`.

This round reviews the whole lane `5603c353..f5d0fb0e` against the issue's acceptance. Its focus is the runtime-round delta `83239549..f5d0fb0e`: three commits, `9182cee7`, `0e3eef5b` and `f5d0fb0e`.

Verdict basis:
- No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head.
- All five lenses were applied at this head, and all five are clean.
- Every earlier public finding on this PR is resolved and stays resolved (see the prior-findings table).
- This round adds three SUGGESTIONs. None of them affects a lens.

## Reconstruction

I read the sources in this order:
1. AGENTS.md, with CONTRIBUTING.md through its references.
2. The issue #621 body and every manager comment on the issue: the assignment 6084306147 and its correction, the capture rulings 6087415319 to 6089776382, the round 2 and round 3 assignments, and the runtime-round assignment 6101380300.
3. The PR #707 body (`closingIssuesReferences` is `[]`; the body says "Relates to #621").
4. The donor diff `5dce647a..7dda9c3b`: `hdl/ucode/gen_gptp_ucode.py`, `docs/INTEGRATION.md` and `docs/SOURCE_EVIDENCE.md`.
5. The parent diff `5603c353..f5d0fb0e` (38 files) and the delta `83239549..f5d0fb0e` (12 files).
6. The exact-head hosted check runs and the hosted shard 3 and 4 job logs.

I finished my own pass over the diff and my own executions before I read the earlier review comments (R570-1..3, R571-1..3). I read them only to resolve their findings.

## Scope taken from the acceptance

| Source | Item | Status at this head | Evidence |
|---|---|---|---|
| Issue scope 1 and assignment 1 | Reproduce in simulation: a ±10 ms grandmaster-driven step through the takeover path, a port that holds asCapable, the 2 s loss and its cause | MET | The head regression with the base donor generator `5dce647a` fails 14 of 62 checks, rc 1 (`receipts/phc_step_base_generator.run.log`). Every step placement shows `RETURN outage_ns=2000001250` or `2000001750`, with the loss 0.79 ms to 1.0 s after the step; the bench reported 0.22 to 0.97 s. The published delay goes bad: -3466 and 4545 ns from the contaminated rate window, ±5 ms on crossing exchanges. The cause is the neighbour-rate window and the crossing exchange spanning the servo's PHC step |
| Issue scope 2 and assignment 2 | Fix: asCapable and a valid delay survive a step; a planted defect fails the test | MET | Donor `gen_gptp_ucode.py:836-838` (the step clears `S_NR3` and sets `S_PDSTEP`), `:1298` (each request clears `S_PDSTEP`), `:1727-1737` (PDEPOCH gives liveness credit only and skips PDPAIR). The `gptp_plane` suite passes at the head: `run` 29/29, `phc_step` 62/62, campaign 8/8. Six planted defects are rejected by name, and the `nocease-control` arm passes (`receipts/gptp_plane_suite.log`) |
| Assignment 3 | Effects: media, `tu`, GPTP_GM_CHANGED, CLOCK_DOMAIN | MET | The full gmstep leg passes 190/190 at the head (`receipts/gm_steps_suite.log`). Its #621 phase covers +10 ms and -10 ms under CRF and then INTERNAL selection. It grades asCapable held every cycle, a valid delay every cycle, one `tu` episode, one GPTP_GM_CHANGED, the CLOCK_DOMAIN deltas (0 under CRF, 1/1 at INTERNAL), no `mr` change, no MEDIA_RESET and the talker licence (`sim_gmstep.cpp:952-1008`) |
| Issue scope 3 | Five-step bench repeat | NOT IN THIS LANE | The assignment moves it to a later bench lane. The PR does not close #621 |
| Runtime round 1 | Native per-leg measurement at base and head | MET (author's measurement) | `tb/verilator/milan_dp_gm_steps/README.md:57-111` |
| Runtime round 2 | `milan_dp` within 60% of 4800 s on hosted, with no coverage removed. The new suite runs on every PR, on a shard with headroom, with an ownership proof | MET | Hosted shard 4/5 at this head: `milan_dp` PASS, 11955 checks, window 1811.5 s = 37.7%. Hosted shard 3/5: `milan_dp_gm_steps` PASS, window 946.0 s = 52.6% of its 1800 s default (`receipts/hosted_shard_3_4_summary.txt`). My native run: `milan_dp` rc 0, 11955 checks, 1842.4 s. The suite is in the default partition, owned by worker 3/5 and pinned as a landmark at `suite_shards.py:189` (`receipts/shards.log`). The coverage argument is in the Tests lens |
| Runtime round 3 | No change to RTL, the donor or any graded expectation; gitlink `7dda9c3b` | MET | The delta touches no `hdl/`, `syn/`, `configs/` or submodule path. In `sim_gmstep.cpp` it changes only argument parsing and the phase gate (`:1286-1287`, `:1301-1332`). `CONTROLS` and every check call are unchanged |
| Runtime round 4 | Native per-leg times at the new head | MET (author's measurement) | README `:78-99`. My own runs are in the Tests lens |

## Findings

There is no BLOCKER, MAJOR, MINOR or RESIDUE.

### R571-4-S1 - SUGGESTION - lenses: Docs - `docs/testing/RUNNING_TESTS.md:84`, `tb/verilator/README.md:18`

- **Title:** the stated default-suite counts were already stale at the base, and this lane's new suite moves the real count again.
- **Evidence:**
  - At base `5603c353`, `tb/verilator` has 62 suite directories with a Makefile. One is the physical `milan_dp_gptp`, so the default selection is 61.
  - At the head the real count is 62 (`suite_shards.py --shard 0/1` lists 62, `receipts/shards.log`).
  - `RUNNING_TESTS.md:84` says "60 suites" and `tb/verilator/README.md:18` says "55 default suites", at the base and at the head.
- **Why SUGGESTION, not a finding against this head:** both sentences were false before this lane, and the lane edits neither line. The truth value of each is the same at base and head. Under AGENTS.md section 4, a defect found next to the change is new work.
- **Option:** state the count as 62, or point to `scripts/run_all_suites.sh --list` instead of a number, through the residue checklist or its own issue.

### R571-4-S2 - SUGGESTION - lenses: Docs - `tb/verilator/milan_dp_gm_steps/README.md:105-111`, `docs/testing/CI_WORKFLOWS.md:289-305`

- **Title:** the hosted windows at this head can replace the projections.
- **Evidence:** both pages project `milan_dp` at 2323 to 2750 s and the new suite at about 909 s, 50.5%. They say "Hosted runs confirm or replace these figures". Hosted at this head took 1811.5 s for `milan_dp` (37.7%) and 946.0 s for `milan_dp_gm_steps` (52.6%).
- **Why SUGGESTION:** the pages label the figures as projections and defer to hosted, and both hosted values are within the bound that was required.
- **Option:** record the exact-head hosted windows (shard 4 job 114339716063, shard 3 job 114339716133) next to the projections.

### R571-4-S3 - SUGGESTION - lenses: Tests - `tb/verilator/milan_dp_gm_steps/Makefile:30-32`

- **Title:** nothing in the sweep fails if the full leg stops running.
- **Evidence:**
  - The #621 phase's 86 checks run in the sweep only through the first line of `run`, `$(MAKE) -C ../milan_dp gmstep`.
  - If that line were dropped, the driver would still pass: its positive control rebuilds a missing binary, and in the sweep it runs with `--no-small-steps`. The suite would then report 6/6, and no gate compares check counts.
- **Why SUGGESTION:** before the split, `milan_dp`'s `run` had the same exposure through its `gmstep` prerequisite, and this property is general to every suite. The current recipe does run the full leg: 190 checks, on hosted shard 3 as well.
- **Option:** have the default driver run require an existing, fresh full-leg transcript, or add a check-count floor for this suite.

## Lens results

```text
[R571] PASS Conformance - gptp-processor gen_gptp_ucode.py:836-838,1298,1473-1497,1727-1737 (7dda9c3b); sim_phc_step.cpp:59-75,291-313; sim_gmstep.cpp:952-1008; receipts/phc_step_base_generator.run.log, gptp_plane_suite.log, gm_steps_suite.log - I checked the fix against IEEE 802.1AS-2020 11.2.2, 11.2.19.3.3, 11.2.19.3.4 and 11.2.20, and against the issue's acceptance. A step re-seeds the neighbour-rate window. A completed crossing exchange gives liveness only (lost count reset, no delay or ladder change). An unanswered request still goes to the loss judge at LOST_N_C+1. The base generator reproduces the bench's 2.0 s outage at every placement. The head passes all six placements, with no loss and no invalid delay. The effects in assignment item 3 hold under CRF and INTERNAL. Runtime-round items 1-4 are met, and hosted milan_dp takes 37.7% of its 4800 s limit.
[R571] PASS RTL - git diff 5603c353..f5d0fb0e over hdl/, syn/ (only rom_digests.tsv: +1 row for 7dda9c3b), configs/ and the gitlinks; donor gen_gptp_ucode.py:269-271,1353,1811-1829 - the lane changes no parent RTL. The donor microcode change is reviewed above. S_NR4 is read only behind a nonzero S_NR3 (:1811-1815), so dropping it from the init list is safe. S_PDSTEP is cleared before every request (:1298), so a warm or cold reset cannot leave a stale flag that affects a completed exchange. The runtime delta changes no RTL, donor or gitlink.
[R571] PASS Robustness - sim_gmstep.cpp:1301-1332; gmstep_mutants.py:57,95,280-286,355-391; receipts/probe_short_leg.log; sim_phc_step.cpp:315-389 - eight malformed command lines each exit 2: no image, the flag alone, an unknown option, the flag twice, three positionals, a negative delay, a delay of 10^6 and a missing image. The flag before or after the delay gives the same transcript. The driver forwards the flag only to the leg that has it (option-off has none). Each suite runs alone in its own sweep, so they never share tb/verilator/milan_dp concurrently. The step campaign keeps the silent-peer, excessive-delay and unanswered-crossing failure paths.
[R571] PASS Tests - receipts/gm_steps_suite.log, milan_dp_suite.log.gz, gptp_plane_suite.log, probe_short_leg.log, short_leg/*, suite_tally.txt, hosted_shard_3_4_summary.txt - the new suite passes at the head: the full leg 190/190, then the positive control and the 5 acceptance controls, each caught by its named check. The short leg is exactly the full transcript minus one contiguous block of 86 checks (58 "621:" and 28 licence checks, lines 51-136), and none of the five named checks lies in that block. milan_dp passes without the leg (11955 checks, 15 tallies). The tallies (11955 + 196) match the author's split. The issue-level campaign rejects the base generator with 14 failures.
[R571] PASS Docs - tb/verilator/milan_dp_gm_steps/README.md:18-48; milan_dp/README.md:81,900-936,1384-1386; tb/verilator/README.md:62,64; docs/testing/TESTING.md:278,388-391,599; CI_WORKFLOWS.md:284-305; GM_LOSS_RECOVERY.md:230-239,275; measure_test_evidence_readers.py:142-147; GPTP_PLANE.md:97-166; PR #707 body - the README's phase table matches sim_gmstep.cpp. The checks lie at :875 (media), :1134 and :1163 (GM change) and :1186 (CRF restart). The "32 coincident-restart delays" matches kPhases = 32. The disposition's "for five, its option-off leg" matches the five option-off CONTROLS. The cited dev windows agree with the hosted jobs (shard 3 at 459-680 s, receipts/dev_shard_jobs.txt). No live reference to milan_dp/gmstep_mutants.py or `make -C tb/verilator/milan_dp gmstep-mutants` remains outside the historical CHANGELOG. The PR body has no closing keyword. S1 and S2 are optional.
```

## Prior findings at this head

| Finding | Severity | Status | Evidence at this head |
|---|---|---|---|
| R570-1-F1 = R571-1-F1 (hosted `docs-check` red) | BLOCKER / MAJOR | RESOLVED | The disposition for `phc_step.py` is present. `measure_test_evidence.py --check` and `--selftest` rc 0 (`receipts/static_*measure_test_evidence*`). Hosted `docs-check` succeeded at this head |
| R570-1-F2 (receipt arm escapes the production bound) | MINOR | RESOLVED | `check_nvm_capture.py` rc 0 at this head. The runtime delta does not touch it |
| R570-1-F3 = R571-1-F3 (stale capture figures) | MINOR | RESOLVED | The runtime delta does not touch `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` or `measurements.json` |
| R570-1-F4 = R571-1-F2 (liveness credit after an answered crossing) | MINOR | RESOLVED | `asCapable falls at the fourth unanswered request after a crossing exchange` passes at the head (`unanswered_at_drop=4`), and both deletion plants are rejected (`receipts/gptp_plane_suite.log`) |
| R570-1-F5 (auto-close of #621) | MINOR | RESOLVED | `closingIssuesReferences` is `[]`, and the body says "Relates to #621" |
| R571-2-F1 (no credit for an unanswered crossing) | MINOR | RESOLVED | The unanswered-crossing check passes (`unanswered_at_drop=3`), and `credit-on-step` is rejected by name |
| R571-1-R1, R571-2-RES-1, R571-2-RES-2 | RESIDUE | RESOLVED | Unchanged since R571-3 confirmed them. The delta does not touch those lines |
| R571-3-S1, R570-3-S1, R570-2-S1 / R571-2-S1, R570-1-S1..S5, R571-1-S1..S3 | SUGGESTION | carried | No lens effect. None is affected by the runtime delta |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Donor `gen_gptp_ucode.py:836-838,1298,1473-1497,1727-1737`; `sim_phc_step.cpp`; `sim_gmstep.cpp:952-1008`; issue body and assignments; base-generator reproduction; hosted shard 3 and 4 windows | R571-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| RTL | CLEAN | `git diff 5603c353..f5d0fb0e` over RTL, syn, configs and gitlinks; `rom_digests.tsv`; donor scratch-cell readers `:269-271,1353,1811-1829` | R571-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Robustness | CLEAN | `sim_gmstep.cpp:1301-1332`; `gmstep_mutants.py:57-95,280-391`; `probe_short_leg.log`; the step campaign's failure arms | R571-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Tests | CLEAN (S3 suggestion only) | `gm_steps_suite.log`; `milan_dp_suite.log.gz`; `gptp_plane_suite.log`; `short_leg/*`; `suite_tally.txt`; `phc_step_base_generator.*`; hosted summaries | R571-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |
| Docs | CLEAN (S1, S2 suggestions only) | New suite README; `milan_dp` README; `tb/verilator/README.md`; `TESTING.md`; `CI_WORKFLOWS.md`; `GM_LOSS_RECOVERY.md`; `GPTP_PLANE.md`; test-evidence disposition; PR body | R571-4 | f5d0fb0e1d9868c91ae2388cb2a51b05653df5a1 |

## Commands and receipts

- **Simulator:** `pinned-verilator-5.050/verilator --version` reports `Verilator 5.050 2026-07-01 rev v5.050`. It was first on `PATH` for every build.
- **Suites:** three ran concurrently. The two in the clone were `make -C tb/verilator/milan_dp_gm_steps VERILATOR_JOBS=6` (rc 0, 596.6 s) and `make -C tb/verilator/gptp_plane` (rc 0, 574.8 s). `milan_dp` ran in a disposable copy: `make -C tb/verilator/milan_dp VERILATOR_JOBS=4` (rc 0, 1842.4 s). `suite_tally.py --verdict` rc 0 on each log.
- **Short-leg probe:** `scripts/probe_short_leg.sh`, rc 0. The 8 malformed calls exit 2. Short leg: 104 checks, equal to the full 190 minus lines 51-136.
- **Issue reproduction:** `phc_step.py --generator <base 5dce647a generator>`, rc 1 as required, 14/62 failures. The generator hashes are in `receipts/generator_sha256.txt`.
- **Static gates, rc 0:** `measure_test_evidence.py --check` and `--selftest`, `ci_events.py --check` and `--selftest`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_hygiene.py --check`, `check_nvm_capture.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `suite_shards.py --selftest`, `git diff --check 5603c353 HEAD`.
- **Static gates, not judged locally (rc 2):** `check_em_dash.py --base` and `gen_toc.py --check` need the pinned Markdown renderer, which this host lacks, and a shared install is not allowed. A raw scan of the added Markdown lines finds 0 U+2014. Hosted `docs-check` succeeded at this head.
- **Full reproduction:** `scripts/run_review.sh <clone> <packet> <verilator>`.
- **Path sanitization:** host-specific paths in the receipts are replaced by `$PINNED_VERILATOR_PREFIX`, `$PACKET`, `$CLONE` and `$HOME_PATH`. `milan_dp_suite.log` is gzip-compressed.

## Real limits

- No full sweep, Yosys bank, lint ratchet, vendor stage, capture-SoC campaign or builder bank was run here. Their figures in the PR body are the author's, from `e0ee38f9`. Rounds 2, 3 and the runtime round change no input to them except as stated.
- I did not run the explicit `gmstep-mutants` campaign (20 controls on the whole leg). Its `CONTROLS` table is byte-unchanged since `83239549`, where the author reports it caught all 20. The sweep's 5 controls were run here.
- My native times come from one loaded host with concurrent jobs. They are not hosted evidence.
- Hosted checks at this head, as read (`receipts/hosted_check_runs.tsv`):
  - Completed with success: `docs-check`, `elaborate`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0, 3 and 4.
  - Still in progress when I read them: Verilator shards 1/5 and 2/5, and `firmware-unit`.
  - Skipped: Physical gPTP, which is not hardware evidence.
- No manager source bank exists at this head, and none is claimed or inferred.
- Physical calibration was NOT RUN. Simulation results and field skips are not hardware proof.
- Clause readings come from the cited clause numbers and the donor's comments. This packet does not reproduce the standard's text.

## Pending manager duties

- Confirm hosted Verilator shards 1/5 and 2/5 and `firmware-unit` at this exact head, and own hosted and act acceptance.
- Validate the current-dev merge candidate (source base `5603c353`, live dev `1fb0ed9a`) with the builder and native banks, and link the receipts.
- Land donor PR Mister-M-alt/FPGA-gPTP #77 (head `7dda9c3b`) under the donor bar before the parent pin merges.
- Keep #621 open for the physical five-step bench repeat.
- Decide on S1, S2 and S3 and on the carried suggestions.

## Restore check

`receipts/restore_check.txt` shows the clone restored after all probes:
- HEAD is `f5d0fb0e…` with tree `f0f6817a…`, and the index tree equals it.
- The worktree equals HEAD in bytes and modes.
- `git status --porcelain --ignored --untracked-files=all` is empty.
- The gitlinks are `7dda9c3b`, `2ad2f845` and `48ff7a7e`, and each submodule's checkout is at its gitlink with nothing dirty or ignored.
- Only build artifacts that my runs generated were removed.
- The `milan_dp` run and the base-generator campaign used copies under the scratch directory.

R571-4 FINISHED
