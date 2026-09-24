[R283] POSITIVE - exact head cf43b4716772582d0c77d40f1eeac5934a0cd9da

Round R283-4, composition review of issue #539 / PR #547, cleared context.
Candidate `cf43b4716772582d0c77d40f1eeac5934a0cd9da`, tree `e13a00368b65ae5d29559541467d5f07b4dc29c3`.
It merges the queued train (first parent `02648441`) with the PR source head `324eb343a870973b64706779d0183ae342dcb3d7` (second parent).
Their merge base is `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f`.
Scope: composition acceptance only. The two POSITIVE source reviews at `324eb343` are R282-3 (issuecomment-5811970603) and R283-3 (issuecomment-5811878819).

Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five are clean. There is no BLOCKER, MAJOR, MINOR or SUGGESTION.

## Summary

- **The merge is textual identity on both sides.**
  - `git merge-tree --write-tree 02648441 324eb343` reproduces the head tree `e13a0036` exactly.
  - The first-parent diff touches only the PR's nine paths.
  - For each path, the composed patch has the same hash as the PR's own patch `f86c34fe..324eb343`.
  - On the four shared paths, the second-parent side carries each predecessor's patch unchanged.
  - Receipts: `per_file_patch_equivalence.txt`, `overlap_predecessor_retention.txt`, `merge_tree_recompute.txt`.
- **Four files are shared with predecessors.** The review-start set was left empty (`{}`), but the PR shares four files with the queued predecessors:
  - `docs/design/TIME_SYNC.md` (#511, `b38634f4`);
  - `docs/reference/REGISTER_MAP.md` (the #530 / #536 lwSRP and CRF-talker rows: `8eca7031`, `c08d7c09`, `03f26b19`, `35f2a54b`, `8ffd6c61`);
  - `docs/testing/TESTING.md` (`8eca7031`);
  - `tb/verilator/milan_dp/README.md` (`8eca7031`, `c593cbef`).

  Each predecessor hunk sits in a different region: the TIME_SYNC GM bullet list, the `0x750`/`0x764`/lwSRP rows, and other suite rows. None of them touches the loop table, the `0x8F8` row, the `mmcm_servo` row or the gmstep "does not grade" list that this PR edits. Receipts: `overlap_files.txt`, `pr_side_files.txt`, `predecessor_side_files.txt`.
- **No predecessor changes a semantic neighbour of this PR.**
  - No line the predecessors added mentions #539, the servo, `MCSRV`, the 1024 ppm guard, #545 or #546. The one regex hit is a hex colour in a diagram (`predecessor_servo_mentions.txt`).
  - The servo suite's inputs (`KL_mmcm_drp_servo.sv`, `cdc_pulse.sv`, `cdc_handshake.sv`, the `mmcm_servo` Makefile and both harnesses, `rails_wrap.sv`) have the same blob IDs as at `324eb343` (`servo_input_blobs.txt`).
  - Predecessors did change `milan_datapath.sv`, the servo's parent. None of their added or removed lines touches the servo instance, `mcsrv_stat_w` or `ptp_now` wiring, and the servo's port list is unchanged.
  - The pinned protocol processor moved `424c688f -> 09f9bf38`. It has no reference to the servo's status word.
- **Live dev is already inside this tree.** `git merge-tree --write-tree cf43b471 9d328810` returns `e13a0036`, the candidate's own tree. Live dev's only commit missing from the candidate is the #543 merge commit itself, whose content the train carries as issue 542 (`topology.txt`).

## Findings

None. No BLOCKER, MAJOR, MINOR or SUGGESTION at this head.

## Prior public review findings: resolved or retained at this head

Read after my own pass over the diff, the gates and the probes. The issue's manager assignment comments name these findings. I read those comments as part of the required public-scope reconstruction, before my diff pass.

| Finding | Status at `cf43b471` | Evidence (`receipts/prior_findings_at_head.txt`) |
|---|---|---|
| R283-1 F1 = R282-1 F1, MINOR, Tests (and Docs for R282-1): U11 could not fail for the re-base; the U10 storm claim | RESOLVED | `sim_main.cpp:502` requires the 33-tick gap. The unit harness passes 78/78 on the candidate. The re-base mutant was killed by the source rounds, and the file is byte-identical here |
| R282-1 F2, MINOR, Docs: `GM_LOSS_RECOVERY.md` stated the #539 defect as current | RESOLVED | `git grep "108 to 524" -- docs/design tb` finds no match (rc 1). `GM_LOSS_RECOVERY.md:154` states the discard |
| R283-1 S1/S2 = R282-1 S1, SUGGESTION, Tests: streak restart, open-window rule, saturation | RESOLVED | U12 arms in `sim_main.cpp` (header :26); the unit harness passes |
| R283-1 S3 = R282-1 S2, SUGGESTION, RTL/Docs: advance bound is `incr + adj` | RESOLVED | `KL_mmcm_drp_servo.sv:300` "below 384 ns" |
| R282-2 F1 = R283-2 F1, MINOR, Docs: `milan_dp/README.md` "step guard gap" | RESOLVED | `git grep "step guard gap" -- tb docs` finds no match (rc 1). README `:481` states the same claim as `GM_LOSS_RECOVERY.md:181` |
| R282-2 S1, SUGGESTION, RTL/Docs: margin is 4.9x | RESOLVED | `KL_mmcm_drp_servo.sv:302` "10.7x above the one and 4.9x" |

Line numbers moved on the candidate: README 388 -> 481, REGISTER_MAP 1942 -> 1963 and TIME_SYNC 147 -> 148, because of predecessor text above them. The content is byte-identical.

## Lens results (clean lenses in findings format)

[R283] PASS Conformance - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` (blob `9459a26b` = PR head); `receipts/mmcm_servo_run.log` (phc_step 113/113); `receipts/milan_dp_aclk.log` - Issue #539 acceptance 1-3 rests on the servo and `Vphc_step`, and the composition leaves both byte-identical. On the composed tree, `Vphc_step` passes 113/113, including P1's 21 us to 1 s sweep, both signs. The composed datapath's CRF leg (`aclk`, 139/139) reads `A_MCSRV_STAT = 0x00000033`: ACQUIRE, MMCM locked, `[15:10]` = 0, so there is no false step discard. The author reported the same value for round 1 on the old base.

[R283] PASS RTL - `KL_mmcm_drp_servo.sv:293-305,443-462,647-670` unchanged by composition; `git diff f86c34fe 02648441 -- hdl` (no servo, `mcsrv_stat_w` or `ptp_now` line); `receipts/gates/lint_check.log` - The one RTL interaction surface is the predecessors' edit to `milan_datapath.sv`, and it does not reach the servo instance or its inputs. Checked with pinned Verilator 5.050 on the candidate: `lint_rtl.py --check` PASS (90 <= 90; `hdl/ieee1722/crf` 4 <= 4, `hdl/ieee1722/avtp` 49 <= 49, `hdl/milan` 2 <= 2); `check_rtl_source_lists`, `check_soc_sources`, `pp_srcs --check`, `check_sv_idiom`, `measure_naming --check` and `check_port_contracts` all rc 0; `milan_dp` `aclk` elaborates and runs the full composed datapath under `-Wall`.

[R283] PASS Robustness - `receipts/mutants/mutants_summary.txt`; `receipts/mmcm_servo_run.log` (U10-U12, P2-P4) - The composition adds no input, state or configuration path to the servo. On the composed tree, disposable mutants of the step guard are still killed: detector off (`step_hit_w = 0`), step not tallied, and detector threshold raised to 1 ms. Each makes `Vphc_step` exit 1 (RESULT: FAIL). The scratch file was restored to blob `9459a26b` after each one. The feature-disabled path (servo IDLE when CRF is not selected) is unchanged, and `aclk` exercises the enabled one.

[R283] PASS Tests - `tb/verilator/mmcm_servo/{Makefile,sim_main.cpp,sim_phc_step.cpp}` (blobs = PR head); `receipts/mmcm_servo_run.log`; `receipts/gates/{suite_shards_st,test_evidence,test_evidence_st,cpp_idiom}.log`; `receipts/test_evidence_ratchet_by_commit.txt` - `make run` passes on the candidate with 0 failures in every harness: unit 78/78, rails 8/8, phc_step 113/113. The suite inventories and ratchets that predecessors changed or that read `tb/` pass on the composed tree: `suite_shards --selftest` (the `mmcm_servo` landmark is still owner 2), `measure_test_evidence --check` (74 <= 77, identical at parent `02648441` and at the head, so the result is composition-neutral) with `--selftest`, and `check_cpp_idiom`.

[R283] PASS Docs - `docs/design/TIME_SYNC.md:76,148-149`; `docs/reference/REGISTER_MAP.md:1963`; `docs/testing/TESTING.md:482`; `tb/verilator/milan_dp/README.md:480-481`; `docs/design/GM_LOSS_RECOVERY.md:152,154,181`; `receipts/gates/*.log` - The four shared pages keep both sides' text, and the `#step-policy` link resolves to `### Step policy` at `TIME_SYNC.md:76`. The #437/#516 renderer and em-dash gates, which came in with the predecessors, judge this PR's lines on the candidate under the hash-locked renderer lock (cmarkgfm 2025.10.22, html5lib 1.1):
- `check_em_dash --base 02648441`: 0 findings over 9 added lines in 5 pages;
- `--base f86c34fe`: 0 findings over 610 lines in 23 pages;
- `--selftest`: rc 0;
- `gen_toc --check`: OK over 107 pages;
- `--verify-anchors`: 163 links reproduced.

  These also pass: `docs_check` (0 findings, 165 md, 857 scrubbed files), `check_doc_style`, `check_gptp_docs`, `check_feature_status` and its self-test, `gen_module_matrix --check`, `check_doc_paths`, `check_solution_docs`, `check_submodule_docs`, `check_archive`, `check_hygiene --check`, `ci_events --check` (1647 items) and `--selftest`. No predecessor text about #539 or the servo becomes stale (`grep_539_candidate.txt`).

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | servo RTL and `Vphc_step` byte-identical to source; phc_step 113/113 and `aclk` 139/139 on the candidate | R283-4 (composition); source coverage R282-3 and R283-3 | `cf43b471` (composition); `324eb343` (source) |
| RTL | CLEAN | predecessor `hdl` diff vs servo instance and wiring; `lint_rtl --check`, source-list, idiom and port gates; `aclk` elaboration | R283-4; source R282-3, R283-3 | `cf43b471`; `324eb343` |
| Robustness | CLEAN (composition does not touch its scope; re-probed) | 3 mutants killed on the candidate; U10-U12 and P2-P4 pass | R283-4; source R282-3, R283-3 | `cf43b471`; `324eb343` |
| Tests | CLEAN | `mmcm_servo` 78/8/113; `suite_shards`, `measure_test_evidence`, `check_cpp_idiom` | R283-4; source R282-3, R283-3 | `cf43b471`; `324eb343` |
| Docs | CLEAN | 4 shared pages, both sides retained; the documentation and CI-contract gates listed above, including the #437/#516 renderer gates | R283-4; source R282-3, R283-3 | `cf43b471`; `324eb343` |

The composition touches the lenses' scope only through the shared-file and semantic-neighbour surfaces listed above. Each surface was applied and found clean at `cf43b471`. For the unchanged servo logic and harness depth, the source rounds R282-3 and R283-3 at `324eb343` stand. Nothing in any lens's scope differs between that head and this candidate: the per-path patch hashes are identical.

## Real limits

- **Not run:**
  - Full parent, protocol-processor, gPTP and Yosys banks, and the builder bank. The manager reports them as passed at this head; I did not reproduce them.
  - `mmcm_servo_autorepair` and the `milan_dp` `gmstep` and `crflic` legs.
  - `gen_toc --selftest`, `docs_check` in a no-git export, and `xvlog_gate` (no Vivado on this host).
  - act, Docker and the host runner.
- **The candidate has no hosted runs.** `cf43b471` is not on the remote (the check-runs API answers 422 for it), so it has no hosted evidence. The hosted contexts at the source head `324eb343` all concluded success, except `Physical gPTP (nightly and manual)`, which was skipped (`hosted_checks_324eb343.tsv`). A skipped context is not execution.
- **Tooling.**
  - The renderer lock was installed with `--require-hashes` into a disposable venv under the packet's scratch directory. `pyyaml` 6.0.3 was added there, unpinned, as the workflow does.
  - All builds used pinned Verilator 5.050, verified by `--version` and binary hash in `tool_identity.txt`. The servo Makefile's `-j 0` compiles at most 7 generated units. `aclk` built with `VERILATOR_JOBS=4`. At most 8 jobs ran at once.
- **No hardware.** Physical calibration was NOT RUN. No simulation here is hardware proof.
- **Evidence tree.** `review-evidence/539-r1` at `1363d132` holds only the round-1 author packet (`author/`, 324 manifest entries). I read only its manifest and used no author file.
- **Clone integrity.** Gates ran read-only in the review clone. Probes ran in a scratch copy. After the probes, HEAD, HEAD tree, index tree, tracked blob bytes and modes of the PR's paths, the four gitlinks and the submodule worktrees all match the exact head, and nothing is untracked, ignored or flagged (`clone_integrity_after.txt`).

## Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. Live dev `9d328810` merges into this candidate as a tree no-op (`e13a0036`), so the expected final tree is this one. The manager still has to confirm that at the time of merge.
- Hosted and act acceptance on the exact merge head.
- Post-merge containment (`check_merge_containment.py`), `check_merge_review_integrity.py`, and closing and moving #539.
- Out of #539 scope, left open by the source: the slew path (#545) and the talker-step path (#546).

## Receipts

Every published file is listed in `MANIFEST.sha256`. Scripts: `scripts/run_gates.sh <clone> <python-with-lock> <out>` and `scripts/mutate_servo.sh <scratch-copy> <verilator> <out>`. Host paths in receipts are replaced by `$PACKET`, `$CLONE`, `$PINNED_TOOL_BIN`, `$PINNED_IMAGE_ROOT` and `$HOME`.

R283-4 FINISHED
