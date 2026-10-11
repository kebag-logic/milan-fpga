[R570] POSITIVE - exact head 8c3e892c2b7130d88d16fb6a26136856975e1ea9

# R570-6: internal independent delta review of PR #707 (issue #621)

- **Head under review:** `8c3e892c2b7130d88d16fb6a26136856975e1ea9`, tree `04f38ab729f09b4f1185f7f91416995868308ff8`.
- **Head shape:** a merge with parents `2cf985f3206dd519d80142fd2479afe24c3051f6` (the PR head that R570-5 and R571-5 reviewed POSITIVE) and dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0`. The merge base is `5603c353`.
- **Verdict basis:** no BLOCKER, MAJOR or MINOR is open at this head. This round adds one RESIDUE (R570-6-R1) and retains one carried RESIDUE (R570-5-R1 = R571-5-RES-1). Both are wording in the PR body only. All five lenses were applied, and all five are clean.
- **Context:** this round was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body, the manager's assignment and rulings on #621 and PR #707, the review-start comment, the merge diff and history, and executable evidence. Prior public findings were read only after my own pass over the delta.

## 1. What the delta is, established from Git

Receipt: `receipts/merge_delta.log` (script `check_merge_delta.sh`).

1. **Plain-merge equivalence.** I recomputed the merge of `2cf985f3` and `cfadd767` (`git merge-tree --write-tree`, Git 2.56.0), which gives tree `be5d9333`.
   - It conflicts in exactly three paths:
     - `docs/diagrams/PNG_MANIFEST.json`;
     - `docs/diagrams/submodule_boundaries.drawio`;
     - `docs/diagrams/submodule_boundaries.png`.
   - The head tree differs from that plain merge in exactly those three paths and no others.
   - `docs/diagrams/submodule_boundaries.svg` merged textually without a conflict. The head carries that auto-merge result unchanged.
2. **The generated files are the union of the two one-pin edits.**
   - The head's `.drawio` and `.svg` each differ from the PR side by one changed line only: the lwSRP pin `9197193e47a6` becomes `08ee86e812a0`, from dev's #711.
   - They differ from dev's side by one changed line only: the gPTP pin `5dce647ab5a0` becomes `7dda9c3b4d65`, from this PR.
3. **Manifest.**
   - The `submodule_boundaries.png` entry is new. It equals neither side, because both pins changed. The diagram gate verifies it (section 2).
   - The `timesync_chain.png` entry is byte-identical to the PR side.
   - `timesync_chain.drawio`, `.svg` and `.png` are this PR's blobs (`d271813b`, `ca6649c4`, `0a9ce460`), not dev's.
4. **Gitlinks at the head.**

   | Submodule | Pin | Source |
   |---|---|---|
   | `gptp-processor` | `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` | this PR, the reviewed donor head |
   | `third_party/lwSRP` | `08ee86e812a0eb5e1dc6cd61b494d8baf3491348` | dev, #711 |
   | `protocol-processor` | `2ad2f845dd583f8310075fa2380cb60a04fd091a` | unchanged |
   | `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` | unchanged |
   | `external` | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` | unchanged |

5. **PR-owned surfaces are unchanged by the merge.** None of these differs between `2cf985f3` and the head:
   - `tb/verilator/milan_dp`, `tb/verilator/milan_dp_gm_steps` and `tb/verilator/gptp_plane`;
   - `hdl/ieee8021as`, `gptp-processor`, `scripts/suite_shards.py` and `scripts/check_nvm_capture.py`;
   - `tb/verilator/nvm_capture_cpu`, and every page under `docs/design/` that this PR edits.
6. **Dev's RTL.** `hdl/` is byte-identical between dev `cfadd767` and the head (0 diff lines). Against dev, the PR touches only one file outside `docs`, `scripts`, `tb` and the gitlink: `syn/yosys/rom_digests.tsv`, which gains a row for `7dda9c3b` `gptp_ucode.hex` (`rom_digests.tsv:32`).
7. **Three overlap files auto-merged** (`docs/reference/SUBMODULES.md`, `docs/testing/TESTING.md` and `scripts/measure_test_evidence_readers.py`). I compared both sides' hunks against the base. Each side's additions survive at the head, and neither side's lines were lost:
   - `SUBMODULES.md` carries the PR's gPTP pin and donor-guide links and dev's lwSRP pin and its "PR #18" line.
   - `TESTING.md` carries the PR's `milan_dp_gm_steps` rows and dev's #657 render timing, M6 lockstep rows and M2 retained-CDC paragraph.
   - The readers file carries the PR's `phc_step.py` and `milan_dp_gm_steps/gmstep_mutants.py` dispositions and dev's two `lockstep_mutants.py` dispositions.

## 2. Executed evidence at this exact head

Every command ran against the exact head in this clone. Receipts are under `receipts/`.

### Documentation and diagram gates

Script: `run_gates.sh`. Receipts: `receipts/gates/*.log`, with rc in `*.rc`. The pinned Markdown renderer lock (`tools/markdown/requirements.txt`) was installed with `--require-hashes` into a private environment. Every gate below exits 0.

| Gate | Result line |
|---|---|
| `docs_check.py` | 0 findings across 204 md files and 1260 scrubbed text files; scrub self-test 23/23 |
| `check_em_dash.py --base cfadd767` | 0 findings over 278 added lines in 16 pages; arms 339/339 |
| `check_em_dash.py --base <merge-base>` | same; the merge base of dev and the head is `cfadd767` |
| `check_em_dash.py --selftest` | rc 0 |
| `gen_toc.py --check` | 144 pages carry an annotated contents list |
| `gen_toc.py --verify-anchors` | 472 cross-page fragment links reproduced |
| `gen_toc.py --selftest` | rc 0 |
| `check_doc_paths.py` | 962 cited paths resolve, 1 allowlisted |
| `ci_events.py --check` | 1749 contract items across 4 workflows and CI_WORKFLOWS.md |
| `ci_events.py --selftest` | rc 0 |
| `measure_test_evidence.py --check` | PASS: 67 <= 77, 10 <= 10, 0 <= 0, 3 <= 3; 62 default suites |
| `measure_test_evidence.py --selftest` | rc 0 |
| `check_submodule_docs.py` | OK, 5 exact gitlinks |
| `check_submodule_docs.py --selftest` | rc 0 |
| `check_diagram_pngs.py` | OK, 6 decoded, source-bound, review-pinned rasters |
| `check_diagram_pngs.py --selftest` | rc 0 |
| `submodule_boundaries.gen.py --check` | OK, 5 exact gitlinks, decoded PNG |
| `submodule_boundaries.gen.py --selftest` | rc 0 |
| `timesync_chain.gen.py --check` | OK (RTL, features, Gitlink, decoded PNG) |
| `timesync_chain.gen.py --selftest` | rc 0 |
| `DOC_MAP.gen.py --check`, `check_doc_style.py`, `check_gptp_docs.py`, `gen_module_matrix.py --check` | rc 0 each |

**Generators in write mode.** Both generators were run in write mode in place, and Git then showed no change. The committed `.svg`, `.drawio` and `.png` of both diagrams are exactly what the generators produce from the merged tree. Receipts: `receipts/regen_*_write.log` and `receipts/regen_*_status.txt`, both empty.

**Diagram viewed.** I viewed `docs/diagrams/submodule_boundaries.png`. Its five boxes read:
- `protocol-processor` pin `2ad2f845dd58`;
- `gptp-processor` pin `7dda9c3b4d65`;
- `third_party/verilog-axis` pin `48ff7a7e2ef7`;
- `external` pin `efeb541ae5fe`;
- `third_party/lwSRP` pin `08ee86e812a0`.

Each matches the gitlink in section 1.

### Other gates

- `lint_rtl.py --check` with the pinned Verilator 5.050: `LINT GATE: PASS (90 violation(s) <= ratchet 90)`.
- `pp_srcs.py --check`: rc 0.
- `check_nvm_capture.py`: "PASS: capture census, clocks, both timing arms and receipt agree". Its `receipt-opt-out` control reports "production bound applied despite a control field".
- `suite_shards.py --selftest`: PASS. The five-worker landmarks include `milan_dp_gm_steps: 3`.

### Focused suites on the merged tree

Script: `run_focused_suites.sh`. Receipts: `receipts/suites/`. Verilator identity: `receipts/suites/verilator_version.txt` reads "Verilator 5.050 2026-07-01 rev v5.050". The two suites ran concurrently with `make -j8`.

Dev's RTL changed under these harnesses: #640 M6 moved media context tables into LUT RAM, with counters read one column at a time. That is why I re-ran them.

**`tb/verilator/milan_dp_gm_steps`** (default `make`): rc 0, 9:47 wall.
- The clean leg reports `gmstep: checks: 190 failures: 0`.
- The #621 phase passes on both CRF steps, +10 ms and -10 ms, and on the INTERNAL steps. On each step:
  - one tu episode;
  - tu clears again;
  - one GPTP_GM_CHANGED;
  - CLOCK_DOMAIN UNLOCKED and LOCKED deltas of 0.
- The sweep driver catches all five acceptance controls by name, plus its positive check: `6 checks: 6 PASS, 0 FAIL`.

**`tb/verilator/gptp_plane`** (default `make`): rc 0, 9:06 wall.
- 29 checks: 29 PASS, 0 FAIL.
- `phc_step`: 62 checks, 0 failures.
  - The forward and backward steps, and all four arms that cross a step during an exchange, report `drops=0 outage_ns=0`.
  - `ARM liveness ... unanswered_at_drop=4` and `ARM unanswered crossing ... unanswered_at_drop=3`.
- The campaign passes 8 of 8:
  - `nocease-control` passes;
  - `stale-rate-window`, `crossing-exchange`, `never-rearm-measurement`, `liveness-not-marked`, `r571-no-liveness` and `credit-on-step` are each rejected by their named check.
- The ROM line reads 1016 of 1024 words.

### `milan_dp` split recipe and runner test

- `tb/verilator/milan_dp/test_sim_pool.py` passes 17 of 17 at the head (`receipts/test_sim_pool.log`).
- **Fault probe.** `probes/probe_gmstep_back_in_run.sh` re-adds `gmstep` as a prerequisite of `milan_dp`'s `run` (`Makefile:541`).
  - The test then fails `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` by name: 16 PASS, 1 FAIL, rc 1.
  - The Makefile was restored afterwards (`receipts/probe_gmstep_back_in_run.log`).

### Worker-3 headroom after the merge

The PR placed `milan_dp_gm_steps` on worker 3. Dev's #719 grew `chmap_capture` with a lockstep leg, and `chmap_capture` is also on worker 3.

- **Assignment.** The five-worker assignment is identical at `2cf985f3` and at the head (`receipts/shards_2cf985f3.txt`, `receipts/shards_head.txt`).
- **Hosted worker-3 durations** (`receipts/hosted_shard_durations.tsv`):
  - 671 s at base `5603c353`;
  - 672 s at dev `ac2c5e77`, before #719;
  - 737 s at dev `6bfeeb13`, after #719, so #719 adds about 66 s;
  - 1643 s at `2cf985f3`, with the split suite.
- **Projection.** The merged worker 3 is about 1709 s. That remains well below workers 1 and 2, which run 4283 to 4773 s.
- This is a projection, not a measurement. The manager owns the hosted confirmation.

### Hosted state at this head (snapshot, not acceptance)

Receipts: `receipts/hosted_runs_snapshot.tsv` and `receipts/hosted_jobs_snapshot.tsv`.

- **Completed, success:**
  - `docs-check-no-git`, `wire-accountability`, `changes`, `bdd-conformance`, `yosys-elaboration`, `verilator-lint` and `full-ci-gate`;
  - all four Yosys shards.
- **Skipped context:** "Physical gPTP (nightly and manual)". It is not hardware evidence.
- **Still running when snapshotted:**
  - `docs-check` and `firmware-unit`;
  - all five Verilator shards, and the `elaborate` and `rtl-fast` runs.

## 3. Findings

### R570-6-R1 - RESIDUE - Docs - PR #707 body: lines 31, 33 and 206 (live body, `receipts/pr707_body_snapshot.md`)

- **Wording now:**
  - Line 31 says "Parent head: `2cf985f3206dd519d80142fd2479afe24c3051f6`."
  - Line 33 says "Fourteen parent commits on `5603c353`".
  - Line 206, in "How to get into the same state", says `git checkout 2cf985f3206dd519d80142fd2479afe24c3051f6`.
  - Nothing in the body mentions the merge of dev `cfadd767`.
- **Fact:** the PR head is `8c3e892c2b7130d88d16fb6a26136856975e1ea9` (`receipts/pr707_closing_refs.json`, `headRefOid`). It is a merge of `2cf985f3` with dev `cfadd767`. It changes, relative to the plain merge, only the three generated diagram files (section 1).
- **Why RESIDUE:** the body's measurements were taken at `2cf985f3`, and they stay true of that tree. The defect is that the status prose does not name the current head or the merge. That changes no measurement, figure, verdict, test, code, generated artifact or clause claim, and touches no privacy rule.
- **Exact fix:**
  - Line 31 becomes: "Parent head: `8c3e892c2b7130d88d16fb6a26136856975e1ea9`, a merge of dev `cfadd767` into the round 4 head `2cf985f3`; only the generated submodule diagram and its PNG manifest entry were regenerated. The source evidence below was measured at `2cf985f3`."
  - Line 206's checkout becomes `git checkout 8c3e892c2b7130d88d16fb6a26136856975e1ea9`.
- **Verification:** read the live PR body.

### R570-5-R1 = R571-5-RES-1 - RESIDUE, retained - Docs - PR #707 body, Status section, lines 16-17

- **Still open.** Line 16 still says "hosted results at `f5d0fb0e` are the manager's to confirm". Line 17 still says "The round 4 head `2cf985f3` is local and unpushed."
- **Exact fix at this head:** replace both sentences with "The head `8c3e892c` (round 4 head `2cf985f3` merged with dev `cfadd767`) is pushed; hosted results at it are the manager's to confirm."

### No new BLOCKER, MAJOR, MINOR or SUGGESTION

**Observation, not a finding.** `docs/diagrams/submodule_boundaries.svg` merged textually without a conflict, while the matching `.drawio` and `.png` conflicted. A text merge of a generated file is not evidence by itself. Here, both `--check` and write-mode regeneration reproduce the committed bytes, so the merged `.svg` is exactly the generator's output.

## 4. Prior public findings, resolved or retained at this head

The merge changes no file in any of these findings' scope (section 1, item 5). Each status below was re-checked by execution at this head where it is executable.

| Finding | Severity | Status at `8c3e892c` | Evidence (this round) |
|---|---|---|---|
| R570-1-F1 = R571-1-F1: test-evidence ratchet | BLOCKER / MAJOR | RESOLVED | `measure_test_evidence.py --check` and `--selftest` rc 0. Both sides' reader dispositions survive the auto-merge |
| R570-1-F2: a receipt arm escapes the production bound | MINOR | RESOLVED | `check_nvm_capture.py` rc 0. Its `receipt-opt-out` control applies the bound |
| R570-1-F3 = R571-1-F3: capture page figures | MINOR | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `measurements.json` are byte-identical to `2cf985f3`, where R570-5 verified them |
| R570-1-F4 = R571-1-F2: an answered crossing earns liveness credit | MINOR | RESOLVED | `unanswered_at_drop=4`. `liveness-not-marked` and `r571-no-liveness` are rejected by name |
| R570-1-F5: auto-close of #621 | MINOR | RESOLVED | `closingIssuesReferences` is `[]`. The body says "Relates to #621" (line 54) |
| R571-2-F1: an unanswered crossing earns no credit | MINOR | RESOLVED | `unanswered_at_drop=3`. `credit-on-step` is rejected by name, and `nocease-control` passes |
| R570-4-F1: the runner tests encode the removed step | MINOR | RESOLVED | `test_sim_pool.py` passes 17/17, and the `gmstep`-prerequisite plant fails it by name |
| R570-1-R1 / R571-1-R1, R570-4-R1 | RESIDUE | Superseded by R570-5-R1 | - |
| R571-2-RES-1, R571-2-RES-2 | RESIDUE | RESOLVED | The lines are unchanged since R570-5 and R571-5 confirmed them |
| R570-5-R1 = R571-5-RES-1 | RESIDUE | RETAINED | Section 3 gives the updated exact fix |
| R570-1-S1..S5, R571-1-S1..S3, R570-2-S1 = R571-2-S1, R571-2-S2, R570-3-S1, R571-3-S1, R570-4-S1, R571-4-S1..S3, R571-5-S1 | SUGGESTION | Carried, no lens effect | Not reopened. The R570-1-S3 ROM fill is still 1016 of 1024 words |

## 5. Lens results (clean-lens lines)

```text
[R570] PASS Conformance - receipts/suites/milan_dp_gm_steps.log (#621 phase: one tu episode, one GPTP_GM_CHANGED, CLOCK_DOMAIN deltas 0 per step); receipts/suites/gptp_plane.log (phc_step 62/0: drops=0 across forward, backward and four crossing arms; unanswered_at_drop=4 and =3 per IEEE 802.1AS-2020 11.2.19 allowedLostResponses); receipts/merge_delta.log (gptp-processor gitlink 7dda9c3b is the reviewed donor head) - the issue's item 1-2 acceptance and the assignment's item 3 counter checks hold on the merged tree, with dev's RTL underneath
[R570] PASS RTL - receipts/merge_delta.log (hdl/ byte-identical dev cfadd767 -> head, 0 lines; the PR's only non-doc/test change against dev outside the gitlink is syn/yosys/rom_digests.tsv:32); gptp-processor 5dce647a..7dda9c3b touches only the ucode generator, ucode images and docs; receipts/gates/lint_rtl_check.log (90 <= 90); receipts/gates/pp_srcs_check.log - the merge introduces no RTL of its own, and the PR's microcode change builds and elaborates against dev's merged RTL in both focused suites
[R570] PASS Robustness - receipts/suites/gptp_plane.log (silence after an answered and an unanswered crossing, step before t1, deferred t1, response before step; nocease control); receipts/suites/milan_dp_gm_steps.log (both step signs, CRF and INTERNAL sources, CRF control and coincident step); receipts/hosted_shard_durations.tsv and receipts/shards_head.txt (worker-3 assignment unchanged; projected ~1709 s after #719's +66 s) - the failure and timeout paths still behave on the merged tree, and the runtime split keeps its headroom
[R570] PASS Tests - receipts/suites/gptp_plane.log (6 planted defects rejected by name, campaign 8/8); receipts/suites/milan_dp_gm_steps.log (5 acceptance controls caught by name); receipts/test_sim_pool.log (17/17) and receipts/probe_gmstep_back_in_run.log (plant caught, rc 1); receipts/gates/mte_*.log; receipts/gates/check_nvm_capture.log; receipts/suite_shards_selftest.log - the PR's tests still pass and still fail on their planted defects at the merged head
[R570] PASS Docs - receipts/gates/*.log (24 doc and diagram gates rc 0, including em-dash against cfadd767, TOC check and anchors, doc paths, ci_events, test-evidence ratchet, submodule docs, diagram PNGs and both generators' --check and --selftest); receipts/regen_*_status.txt (write-mode regeneration reproduces the committed bytes); docs/diagrams/submodule_boundaries.png viewed (five pins equal the gitlinks); auto-merged SUBMODULES.md, TESTING.md and measure_test_evidence_readers.py keep both sides; the PR body's stale head wording is RESIDUE only (R570-6-R1, R570-5-R1)
```

## 6. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_dp_gm_steps` #621 phase counters; `gptp_plane` `phc_step` arms and liveness thresholds; donor gitlink | R570-6 | `8c3e892c2b7130d88d16fb6a26136856975e1ea9` |
| RTL | CLEAN | dev-to-head `hdl/` identity; `rom_digests.tsv`; donor delta scope; lint ratchet; `pp_srcs --check`; both focused builds | R570-6 | `8c3e892c2b7130d88d16fb6a26136856975e1ea9` |
| Robustness | CLEAN | crossing, silence, deferred and cease arms; both step signs and sources; worker-3 assignment and hosted-duration projection | R570-6 | `8c3e892c2b7130d88d16fb6a26136856975e1ea9` |
| Tests | CLEAN | `phc_step` campaign 8/8; gmstep sweep 6/6; `test_sim_pool.py` 17/17 plus plant; ratchet; capture gate; shard self-test | R570-6 | `8c3e892c2b7130d88d16fb6a26136856975e1ea9` |
| Docs | CLEAN (RESIDUE R570-6-R1 and R570-5-R1 = R571-5-RES-1 only) | 24 doc and diagram gates; write-mode regeneration; viewed PNG; three auto-merged overlap files; dev's merged doc pages; PR body | R570-6 | `8c3e892c2b7130d88d16fb6a26136856975e1ea9` |

## 7. Real limits

- **Not run here:** the full parent sweep, the protocol-processor and gPTP banks, Yosys, the builder bank, Vivado and act. This round executed only the docs and diagram gates, lint, two focused suites, the runner test and one probe.
- **No manager source bank exists at this exact head, and none is claimed.** Source-head execution evidence for the PR's earlier heads is the author's published gate receipts.
- **Hosted contexts were in progress** at snapshot time, and their acceptance is the manager's. The skipped "Physical gPTP" context is not hardware evidence.
- **Physical calibration and the five-step bench repeat (issue item 3): NOT RUN.** No simulation result here is hardware proof.
- **Projection, not measurement.** The worker-3 figure is derived from four hosted runs. Hosted run-to-run variance on these workers is several hundred seconds.
- **Yosys guard not exercised here.** Dev's new elaboration guard (`syn/yosys/enforce_elaboration.py`) was not run in this round. The donor RTL is unchanged between `5dce647a` and `7dda9c3b`; only microcode differs.
- **Both focused suites shared the host.** Their wall times are not comparable to native single-suite times.

## 8. Pending manager duties

- Confirm the hosted required contexts at `8c3e892c`, including the five Verilator shards and `milan_dp`'s and worker 3's durations against the 60 % target.
- Build and gate the current-dev candidate merge at the merge turn (builder and native banks).
- Carry R570-6-R1 and R570-5-R1 = R571-5-RES-1 to the residue checklist.
- Keep #621 open for the later physical repeat. The body says "Relates to #621", and `closingIssuesReferences` is `[]`.
- Run post-merge containment.

## 9. Restore

- After the suites and the probe, every build output and cache was removed.
- `verify_restore.sh` confirmed the restore (`receipts/verify_restore.log`, `RESULT: RESTORED`):
  - the index tree equals the HEAD tree `04f38ab7`;
  - all 1284 tracked entries hash to their index blobs with their index modes;
  - `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are checked out at their gitlinks with nothing extra;
  - the superproject has no untracked, ignored or modified entry.
- No source edit, commit, push or GitHub write was made.

R570-6 FINISHED
