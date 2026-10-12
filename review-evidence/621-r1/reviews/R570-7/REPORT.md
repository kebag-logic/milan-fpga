[R570] POSITIVE - exact head 733fdaa2637af2f527c4bc7d607c861c14ff4b3c

# R570-7: composition review of the issue #621 / PR #707 merge-train candidate

- **Head under review:** `733fdaa2637af2f527c4bc7d607c861c14ff4b3c`, tree `e25f482943bedb5b9e287a934f063b980dff93bf`.
- **Shape:** a merge with parents dev `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8` (F-INT PR #704 and M5 PR #722 on top of `cfadd767`) and the PR #707 source head `8c3e892c2b7130d88d16fb6a26136856975e1ea9`. The merge base is `cfadd767`.
- **Scope:** composition acceptance only. The source head `8c3e892c` already holds two independent POSITIVE source reviews: [R571-6](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6113099415) and [R570-6](https://github.com/kebag-logic/milan-fpga/pull/707#issuecomment-6113191682).
- **Verdict basis:** the composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR is open. All five lenses were applied, and all five are clean. Two wording RESIDUEs in the PR body are retained from the source rounds.
- **Context:** reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and the manager's rulings on #621, the review-start comment, the `c20c85bd..733fdaa2` diff and history, the hosted runs, and the public evidence at `02d43fb7` (`review-evidence/621-r1/MANIFEST.json`). Prior public findings were read only after my own pass over the composition.

## 1. What the composition is, established from Git

Receipts: `receipts/overlap/merge_identity.txt`, `receipts/overlap/pr_files_vs_candidate.txt`, `receipts/overlap/dev_files_vs_candidate.txt`, `receipts/overlap/SUMMARY.txt`.

1. **Plain merge.** `git merge-tree --write-tree c20c85bdd 8c3e892c2` gives tree `e25f4829`, with no conflict. That is the candidate's tree, so the candidate commit carries no resolution of its own.
2. **Files both sides change.** The PR side changes 40 paths against `cfadd767`, and dev changes 73. Exactly two are changed by both, matching the manager's note:
   - `docs/testing/CI_WORKFLOWS.md`: F-INT's `publication-census` hunks (job list, docs-only exclusion, the census paragraph) and the PR's #621 split paragraph (`milan_dp_gm_steps` on worker 3/5);
   - `scripts/measure_test_evidence_readers.py`: M5's `tb/verilator/csr/lock_mutants.py` disposition, and the PR's `gptp_plane/phc_step.py` and moved `milan_dp_gm_steps/gmstep_mutants.py` dispositions.
3. **Both sides land intact.** Every other PR file is byte-identical to the PR head, and every other dev file is byte-identical to dev. In the two shared files, all 18 + 19 added CI-page lines and all 5 + 16 added registry lines are present. None of the lines either side removed came back.
4. **Semantic interactions examined**, beyond the textual overlap:
   - **Shared worker.** Worker 3/5 hosts both the PR's new `milan_dp_gm_steps` and M5's grown `csr` suite (lockstep legs plus `lock_mutants.py`).
   - **RTL under the PR's tests.** The PR's #621 checks now run on M5's `milan_csr.sv` and F-INT's `KL_mbx.sv`.
   - **Donor microcode in F-INT's census.** F-INT's publication census regenerates `gptp_ucode.hex` from the donor generator at the PR's pin `7dda9c3b`.
   - **Suite inventory and shard assignment.**
   - **The test-evidence registry and its armed-suite list.**
   - **The CI event contract, against the merged `rtl-fast.yml`.**
   - **The capture receipt**, beside dev's SoC changes.

## 2. Executed on the candidate

All runs used disposable copies of the exact head under the packet's `scratch/`, or read-only gates in the clone. Concurrency was 16 jobs or fewer.

### Gates (`gates.sh`, `gates_renderer.sh`; `receipts/gates-c20c85bd/`)

All 44 gates exit 0 (`SUMMARY.txt`). Among them:

- `docs_check.py`;
- `check_em_dash.py --base c20c85bd` (0 findings over 278 added lines in 16 pages; 339/339 arms). This is the base that the hosted PR event derives as `merge-base HEAD dev`;
- `gen_toc.py --selftest` (1501/1501), `--verify-anchors` (480 links) and `--check` (144 pages);
- `ci_events.py --check` (1821 contract items across 4 workflow files and `CI_WORKFLOWS.md`) and `--selftest` (2530 arms);
- `measure_test_evidence.py --check`: PASS, 0 unexplained readers, 35 of 101 armed, with `csr`, `gptp_plane` and `milan_dp_gm_steps` all armed. Its `--selftest` passes 105/105;
- `suite_shards.py --selftest`, `check_nvm_capture.py` (including the `receipt-opt-out` control), `check_doc_paths.py`, `check_submodule_docs.py`, both diagram generators' `--check`/`--selftest`, the idiom and hygiene gates, and `git diff --check c20c85bd HEAD`.

The pinned renderer (cmarkgfm 2025.10.22, html5lib 1.1) was used for the TOC, em-dash and docs gates.

### Composition probes (`probes.sh`; `receipts/probes/`)

Each probe ran on a disposable copy with exact bytes restored afterwards (`final-status.txt` empty).

| Plant | Gate | Result |
|---|---|---|
| Drop M5's `csr/lock_mutants.py` disposition | `measure_test_evidence.py --check` | caught, rc 1, "1 unexplained DUT-source reader" |
| Drop the PR's `gptp_plane/phc_step.py` disposition | same | caught, rc 1 |
| Drop the PR's `milan_dp_gm_steps/gmstep_mutants.py` disposition | same | caught, rc 1 |
| Move `milan_dp_gm_steps` off worker 3 in the landmarks | `suite_shards.py --selftest` | caught, rc 1 |
| Drop F-INT's `publication-census` job bullet from the CI page | `ci_events.py --check` | not caught, rc 0 (Observation O1) |

So both sides' registry entries are load-bearing in the composed file.

### Focused suites (`run_suites.sh`, pinned Verilator 5.050 `rev v5.050`; `receipts/suites/`, `receipts/suites-csr/`)

| Suite | Result on the candidate | Wall |
|---|---|---|
| `milan_dp_gm_steps` | rc 0, 196 checks, 0 failures, 2 tallies | 581 s against 1800 s |
| `gptp_plane` | rc 0, 99 checks, 0 failures, 3 tallies | 582 s |
| `csr` (M5) | rc 0 | 139 s |

- **`milan_dp_gm_steps`.** The clean leg gives 190 = 104 + 86, as published. All 58 `621:` checks pass, both step signs under CRF and INTERNAL selection: asCapable held every cycle, valid link delay every cycle, one tu episode, one GPTP_GM_CHANGED, CLOCK_DOMAIN deltas 0, no MEDIA_RESET, no mr change. The positive control passes, and all five acceptance controls are caught by name (6/6).
- **`gptp_plane`.** `phc_step` gives 62/0, with `unanswered_at_drop=4` and `=3`. Its campaign is 8/8: the nocease control passes, and all six planted defects are rejected by name.
- **`csr` (M5).** Lockstep 1x1 and 8x8 pass, and `lock_mutants.py` gives 8/8.
- `suite_tally.py` reports `receipts/suites/suite_tally.txt` with 0 in-suite failures.
- `test_sim_pool.py` passes 17/17 (`receipts/test_sim_pool.log`).

### F-INT's census on the composed tree (`receipts/publication_census_*.log`)

The census ran with pinned sv2v v0.0.12, sha256-verified against `rtl-fast.yml`, and Yosys 0.66.

- `publication_census.py --check --jobs 12`: rc 0, 6 shapes, 234 checks, 0 failures.
- `--selftest --jobs 12`: rc 0, "mutations: 0 of 31 rule(s) no arm proves".

### Shard assignment and hosted durations (`receipts/shards/`, `receipts/hosted/`)

- **Assignment.** The suite inventory and the five-worker assignment are identical at the PR head and at the candidate. Worker 3 holds `adp_tx avtp_parser chmap_capture classifier csr link_guard media_grid_align milan_dp_gm_steps nvm_backend tcam tdm tdm_render tkdiag`, and worker 4 holds `milan_dp` alone.
- **Hosted worker-3 jobs** (`shard_durations.tsv`, `rtl_full_runs.tsv`):
  - 1216 s at the PR head `8c3e892c` (run 38169468651);
  - 717 s at M5's head `2bef9e50`, `csr` grown;
  - 747 s at dev `09c7231e`.
- **Projection.** M5's whole `csr` suite takes 139 s natively here, so the composed worker 3 projects to at most about 1.4 ks of its 120-minute job limit. That is still the least-loaded hashed worker: the others took 1561 to 6640 s across those runs.

### Restore (`verify_restore.sh`; `receipts/verify_restore.log`)

`RESULT: RESTORED`:

- HEAD, the HEAD tree and the index tree equal `733fdaa2` / `e25f4829`;
- all 1295 tracked entries match their index blobs and modes;
- the superproject has no untracked, ignored or modified entry. The gates' own `__pycache__` directories were removed;
- `gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e` are at their gitlinks and clean.

## 3. Findings

No BLOCKER, MAJOR, MINOR or SUGGESTION is attributable to the composition.

### R570-6-R1 - RESIDUE, retained - Docs - PR #707 body: lines 31, 33 and 206 (`receipts/pr707_body_snapshot.md`)

- **Still open.**
  - Line 31 names `2cf985f3` as the parent head.
  - Line 33 says "Fourteen parent commits on `5603c353`".
  - Line 206 checks out `2cf985f3`.
- **Fact:** the live head is `8c3e892c` (`headRefOid`).
- **Wording only.** No measurement, figure, verdict, test, code, generated artifact or clause claim changes.
- **Exact fix (unchanged from R570-6):**
  - Line 31 becomes "Parent head: `8c3e892c2b7130d88d16fb6a26136856975e1ea9`, a merge of dev `cfadd767` into the round 4 head `2cf985f3`; only the generated submodule diagram and its PNG manifest entry were regenerated. The source evidence below was measured at `2cf985f3`."
  - Line 206 becomes `git checkout 8c3e892c2b7130d88d16fb6a26136856975e1ea9`.
- **Verification:** read the live body.

### R570-5-R1 = R571-5-RES-1 - RESIDUE, retained - Docs - PR #707 body, Status section, lines 16-17

- **Still open.** Line 16 says "hosted results at `f5d0fb0e` are the manager's to confirm", and line 17 says "The round 4 head `2cf985f3` is local and unpushed."
- **Exact fix:** replace both sentences with "The head `8c3e892c` (round 4 head `2cf985f3` merged with dev `cfadd767`) is pushed; hosted results at it are the manager's to confirm."

### Observations (not findings; no lens effect; not attributable to this composition)

- **O1.** `ci_events.py --check` does not police F-INT's `publication-census` bullet in the `CI_WORKFLOWS.md` job list (probe above). The composition leaves the bullet intact (section 1, item 3). Gate coverage of that prose is dev's property, not this PR's.
- **O2.** `measure_test_evidence.py --check` notes "the mutation ratchet can be lowered to 66" (77 recorded). This is informational, and the gate passes. The count reflects suites armed on both sides, and lowering the ratchet is optional maintenance.
- **O3.** The capture receipt `tb/verilator/nvm_capture_cpu/measurements.json`, byte-identical to the PR head, records its measurement tree `034e2e30`, which predates M5's `milan_csr.sv` and F-INT's `KL_mbx.sv`/`milan_soc.py`.
  - `check_nvm_capture.py` binds the receipt to the product firmware and the harness only. Neither changes in the composition, and the gate passes.
  - Dev's own receipt stood in the same relation to those changes before this PR.
  - The capture campaign was not rerun here (section 7).

## 4. Prior public findings, resolved or retained at this head

The composition changes none of the PR's files except the two shared files above (section 1, item 3). Each status below was re-checked by execution on the candidate where it is executable.

| Finding | Status at `733fdaa2` | Evidence (this round) |
|---|---|---|
| R570-1-F1 = R571-1-F1 (test-evidence ratchet) | RESOLVED | `measure_test_evidence.py --check`/`--selftest` rc 0; the three dispositions are load-bearing (probes) |
| R570-1-F2 (receipt arm escapes the production bound) | RESOLVED | `check_nvm_capture.py` rc 0, `CONTROL receipt-opt-out` |
| R570-1-F3 = R571-1-F3 (capture page figures) | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `measurements.json` are byte-identical to `8c3e892c` |
| R570-1-F4 = R571-1-F2, R571-2-F1 (crossing liveness credit) | RESOLVED | `gptp_plane` `unanswered_at_drop=4` and `=3`; `liveness-not-marked`, `r571-no-liveness` and `credit-on-step` are rejected by name |
| R570-1-F5 (auto-close of #621) | RESOLVED | `closingIssuesReferences` is empty; the body says "Relates to #621" (line 54) |
| R570-4-F1 (runner tests encode the removed step) | RESOLVED | `test_sim_pool.py` 17/17 on the candidate |
| R570-6-R1; R570-5-R1 = R571-5-RES-1 | RESIDUE, RETAINED | Section 3 |
| Earlier RESIDUEs (R570-1-R1, R571-1-R1, R570-4-R1, R571-2-RES-1, R571-2-RES-2) | Superseded or resolved, as R570-6 recorded | Not reopened |
| R570-1-S1..S5, R571-1-S1..S3, R570-2-S1 = R571-2-S1, R571-2-S2, R570-3-S1, R571-3-S1, R570-4-S1, R571-4-S1..S3, R571-5-S1 | SUGGESTION, carried | No lens effect |

## 5. Lens results (clean-lens lines)

Each lens is in the composition's scope: the PR's checks now run on dev's merged RTL, and its tests, docs and registries share files and workers with F-INT and M5. So each lens was applied here, not carried from the source reviews.

```text
[R570] PASS Conformance - receipts/suites/milan_dp_gm_steps.log (58 `621:` checks: asCapable held and link delay valid every cycle, one tu episode, one GPTP_GM_CHANGED, CLOCK_DOMAIN deltas 0, no MEDIA_RESET, both step signs, CRF and INTERNAL); receipts/suites/gptp_plane.log (phc_step 62/0, unanswered_at_drop=4/=3 per IEEE 802.1AS-2020 11.2.19 allowedLostResponses) - issue #621 items 1-2 and the assignment's counter checks hold with M5's milan_csr.sv and F-INT's KL_mbx.sv underneath
[R570] PASS RTL - receipts/overlap/merge_identity.txt and dev_files_vs_candidate.txt (plain conflict-free merge; no hdl/ path changed by both sides; the PR changes no hdl/); receipts/publication_census_check.log and _selftest.log (F-INT's census elaborates milan_datapath in 6 shapes with the PR's donor microcode: 234/0, 0 of 31 rules unproved); receipts/suites-csr/csr.log (M5 lockstep 1x1/8x8 and lock_mutants 8/8); both datapath builds in receipts/suites/ - the composed RTL elaborates and simulates with both sides' changes
[R570] PASS Robustness - receipts/shards/candidate_shard*.txt vs prhead_shard*.txt (identical assignment; milan_dp alone on worker 4); receipts/hosted/shard_durations.tsv (worker 3: 1216 s at the PR head, 717 s at M5's head) plus csr 139 s native - the shared worker stays far under its 120-minute limit; the #621 failure arms (silence after answered and unanswered crossings, nocease control) behave on the merged tree
[R570] PASS Tests - receipts/probes/SUMMARY.txt (each side's reader disposition and the worker-3 landmark are load-bearing in the composed files); receipts/gates-c20c85bd/test_evidence*.log (0 unexplained readers, 105/105); receipts/suites/* (5 acceptance controls and positive control, phc_step campaign 8/8); receipts/test_sim_pool.log (17/17) - both sides' tests still pass and still fail on their planted defects at the candidate
[R570] PASS Docs - receipts/overlap/SUMMARY.txt (CI_WORKFLOWS.md: both sides' hunks intact, the split paragraph and F-INT's census text coexist); receipts/gates-c20c85bd/SUMMARY.txt (44 gates rc 0, among them docs_check, em-dash vs c20c85bd, TOC check/anchors/selftest, ci_events --check/--selftest against the merged rtl-fast.yml, doc paths, submodule docs, diagram generators) - the PR body's stale head wording is RESIDUE only (R570-6-R1, R570-5-R1)
```

## 6. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_dp_gm_steps` #621 phase (58 checks) and controls; `gptp_plane` `phc_step` arms and thresholds, on the composed RTL | R570-7 | `733fdaa2637af2f527c4bc7d607c861c14ff4b3c` |
| RTL | CLEAN | merge identity; per-side blob identity; census `--check`/`--selftest` (6 shapes); `csr` lockstep; both datapath builds | R570-7 | `733fdaa2637af2f527c4bc7d607c861c14ff4b3c` |
| Robustness | CLEAN | shard assignment PR head vs candidate; hosted worker durations; `csr` native time; #621 failure arms | R570-7 | `733fdaa2637af2f527c4bc7d607c861c14ff4b3c` |
| Tests | CLEAN | registry and landmark probes; test-evidence ratchet and self-test; gmstep 6/6; `phc_step` 8/8; `lock_mutants` 8/8; `test_sim_pool` 17/17 | R570-7 | `733fdaa2637af2f527c4bc7d607c861c14ff4b3c` |
| Docs | CLEAN (RESIDUE R570-6-R1 and R570-5-R1 = R571-5-RES-1 only) | the two shared files line by line; 44 doc and static gates; live PR body | R570-7 | `733fdaa2637af2f527c4bc7d607c861c14ff4b3c` |

Source-side coverage of the PR's own content is R571-6 and R570-6 at `8c3e892c`. The candidate carries every PR file byte-identical except the two shared files reviewed here.

## 7. Real limits

- **Not run here:**
  - the full parent sweep, including `milan_dp` (about 35 minutes natively);
  - the protocol-processor and gPTP banks;
  - the Yosys and builder banks;
  - Vivado and act.
- **Hosted acceptance is not claimed.**
  - The candidate has no hosted run.
  - Dev's own `rtl-full` push run at `c20c85bd` (38190325540) was still in progress.
- **No manager bank is claimed.** None exists at this exact head.
- **The census used the distribution's Yosys 0.66 build**, not the hosted from-source v0.66 build. The census accepted its version string.
- **The capture campaign (`nvm_capture_cpu/run.py`) was not rerun on the candidate** (O3).
- **Wall times are not native single-suite times.** The two focused suites ran concurrently, and `csr` overlapped them partly. The worker-3 figure is a projection from hosted runs whose variance runs to several hundred seconds.
- **Physical calibration and issue item 3, the five-step bench repeat, were NOT RUN.** The skipped "Physical gPTP (nightly and manual)" hosted context is not hardware evidence.

## 8. Pending manager duties

- Build and gate the current-dev candidate at the merge turn (builder and native banks), and confirm the hosted required contexts on the merge result. That includes `milan_dp` and worker 3's durations against the 60 % target.
- Carry R570-6-R1 and R570-5-R1 = R571-5-RES-1 to the residue checklist.
- Keep #621 open for the later physical repeat. The body says "Relates to #621".
- Run post-merge containment.

No source edit, commit, push or GitHub write was made.

R570-7 FINISHED
