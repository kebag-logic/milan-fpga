[R283] POSITIVE - exact head 324eb343a870973b64706779d0183ae342dcb3d7

Issue #539 / PR #547, round R283-3 (external reviewer). Tree `84170bb655b0f547caf7826de541a467db655703`. Source base `26d855a9176d63625e6635a029a0c44e3d57ce9a`. Round-3 delta `910b4fb5f104ac35e8cc1723a70de0d05672895d..324eb343` (commits `5c6d5f5b`, `324eb343`).

Lenses applied at this head: Conformance, RTL, Robustness, Tests, Docs. All five are clean. No new finding of any severity. Both round-2 items are resolved.

## Summary

- The round-3 delta is 2 files, +2/-2: one line in `tb/verilator/milan_dp/README.md` and one comment line in `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`. No test, harness, Makefile, requirement or submodule changed (`receipt_comment_only_proof.txt`).
- **The comment-only proof holds.** Stripped of comments, `KL_mmcm_drp_servo.sv` is byte-identical at `910b4fb5` and at the head. Two independent methods show it:
  - a string-aware comment stripper: sha256 `6b8ef5b9...57b0` at both;
  - the pinned simulator's preprocessor (`-E -P`): sha256 `3f2b1ca6...c81a` at both; `cmp` rc 0.
  - A plain `//`-strip gives a different hash again, identical at both heads. The author's published hash (`d48be6f0...`) comes from yet another normalisation. The hash values depend on the method; the equality across heads does not.
- `tb/verilator/milan_dp/README.md:388` now reads the same as `docs/design/GM_LOSS_RECOVERY.md:181`: the DRP answers zero, and `Vphc_step` grades the step discard (#539). `Vphc_step` is a real target (`tb/verilator/mmcm_servo/Makefile:47`).
- No stale wording remains anywhere in the tree at this head. Searched: "step guard gap", "guard gap", "108 to 524" and "integrates ..." forms. Every `#539` mention in `tb/`, `docs/` and `hdl/` describes the fix (`receipt_stale_wording_sweep.txt`, `receipt_whole_tree_grep.txt`).
- The servo harnesses re-run at this head give 78/78 (unit), 8/8 (rails) and 113/113 (silicon-scale step). These are the round-2 counts (`receipt_servo_suite.txt`).

## Findings

None. There is no BLOCKER, MAJOR, MINOR or SUGGESTION at this head.

## Prior public findings: resolved or retained at this head

These were read only after this round's own pass over the delta.

- **R282-2 F1 = R283-2 F1 (MINOR, Docs), `tb/verilator/milan_dp/README.md:388`: RESOLVED.**
  - The required outcome was a line stating the current fact, consistent with `GM_LOSS_RECOVERY.md:181`. The line at the head is: "The CRF servo. The MMCM DRP answers zero. `Vphc_step` grades its step discard (#539)." This is the same claim as `:181`.
  - `git grep -n -i "step guard gap"` over the whole head: rc 1.
  - The sibling pointer `sim_gmstep.cpp:16`, "(the DRP answers zero; #539)", claims no gap. R283-2 allowed it to stay, and it is unchanged.
- **R282-2 S1 (SUGGESTION, RTL, Docs), `KL_mmcm_drp_servo.sv:302`: RESOLVED.**
  - The comment now reads "10.7x above the one and 4.9x below the other".
  - 4096 / 384 = 10.667 and 20000 / 4096 = 4.883, so both figures are correct to one decimal.
  - The 384 ns bound was re-checked against `hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv:100-101,109-110,144-145`: an unsigned Q8.24 `incr_i` in 32 bits is below 256 ns, and a signed Q8.24 `adj_i` lies in [-128, 128) ns.
  - The same-clock premise also holds: `milan_datapath.sv:2811-2833` has `gtx_clk == axis_clk`, and the servo `clk_i` is `axis_clk` at `:5525`.
- **Round 1 (R282-1 F1/F2/S1/S2, R283-1 F1/S1-S3):** round 2 recorded all of them as resolved. The round-3 delta touches no test, harness or file those findings named, apart from the one comment line above. Nothing regresses.

## Lens results (clean lenses in findings format)

```text
[R283] PASS Conformance - issue #539 acceptance 1-3; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv (comment-free bytes identical to 910b4fb5, receipt_comment_only_proof.txt); receipt_servo_suite.txt (Vphc_step 113/113) - the acceptance evidence covered at 910b4fb5 (locked 150 us step reproduced pre-fix; 21 us to +/-1 s each leave the integrator within one clean window, LOCKED held, one discard; failing arms for the step discard, the guard and the rate path) carries unchanged, because the servo logic, sim_phc_step.cpp and sim_main.cpp are byte-identical; the step suite re-run at this head confirms it
[R283] PASS RTL - KL_mmcm_drp_servo.sv:296-304,446-462 against timestamp_counter.sv:100-101,109-110,144-145 and milan_datapath.sv:2811-2833,5524-5529; receipt_comment_only_proof.txt - the only RTL-file change is the margin comment at :302; the comment-free source and the preprocessed source are identical to 910b4fb5; the comment's figures (10.7x, 4.9x) and its incr + adj < 384 ns premise are true for the 32-bit Q8.24 PHC clocked with the servo; no port, parameter or instance change
[R283] PASS Robustness - KL_mmcm_drp_servo.sv:451-462,650-670 (logic unchanged since 910b4fb5); receipt_servo_suite.txt (unit U10-U12, step P1-P4) - the reset, saturation, ordering, repetition, backward-step and feature-disabled behaviour covered at 910b4fb5 is unchanged, because no logic byte moved; the U10 storm, U11 re-base, U12 streak/open-window/saturation/IDLE arms and the P1 both-sign sweep pass at this head
[R283] PASS Tests - tb/verilator/mmcm_servo/{sim_main.cpp,sim_phc_step.cpp,Makefile} (unchanged 910b4fb5..head, receipt_comment_only_proof.txt); receipt_servo_suite.txt (78/78, 8/8, 113/113, 0 failures, pinned Verilator 5.050, 8 build jobs) - no test changed in round 3, so the round-2 mutant kills (17-18 mutants, 0 survivors) still apply to identical harness and RTL logic; the counts reproduce at this head
[R283] PASS Docs - tb/verilator/milan_dp/README.md:385-392; docs/design/GM_LOSS_RECOVERY.md:152,154,181; docs/design/TIME_SYNC.md:147; docs/reference/REGISTER_MAP.md:1942; docs/testing/TESTING.md:481; tb/verilator/milan_dp/sim_gmstep.cpp:14-18; KL_mmcm_drp_servo.sv:54-77,296-303; PR #547 body (round-3 section and the resolution table rows :130-131); receipt_stale_wording_sweep.txt, receipt_whole_tree_grep.txt, receipt_doc_gates.txt - README:388 matches GM_LOSS_RECOVERY:181; no line in tb/, docs/ or hdl/ states an open #539 gap; the servo header's "100 us to 524 us" (:55) is the motivation for the fix, not a stale claim; docs_check (0 findings, 165 md), check_em_dash --base f86c34fe (0/9 lines) and --base 910b4fb5 (0/1), check_doc_style, gen_toc --check, check_doc_paths, check_sv_idiom, check_rtl_source_lists and git diff --check from 26d855a9 and 910b4fb5 all rc 0; both round-3 commit subjects are one line
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #539 acceptance 1-3; `KL_mmcm_drp_servo.sv` comment-free identity; `Vphc_step` 113/113 at head | R283-3 (depth from R283-2, carried by the comment-only proof) | `324eb343a870973b64706779d0183ae342dcb3d7` |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:296-304,446-462`; `timestamp_counter.sv:100-101,109-110,144-145`; `milan_datapath.sv:2811-2833,5524-5529`; stripped/preprocessed identity | R283-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Robustness | CLEAN | `KL_mmcm_drp_servo.sv:451-462,650-670` (logic unchanged); U10-U12, P1-P4 at head | R283-3 (depth from R283-2, carried by the comment-only proof) | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Tests | CLEAN | `sim_main.cpp`, `sim_phc_step.cpp`, `Makefile` unchanged since `910b4fb5`; 78/78, 8/8, 113/113 at head | R283-3 (mutant depth from R283-2, harness and logic unchanged) | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Docs | CLEAN | `milan_dp/README.md:385-392`; `GM_LOSS_RECOVERY.md:152,154,181`; `TIME_SYNC.md:147`; `REGISTER_MAP.md:1942`; `TESTING.md:481`; `sim_gmstep.cpp:14-18`; PR body; doc gates | R283-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |

## Hosted evidence at this head (read-only snapshot, 2026-09-24T09:51:34Z)

`receipt_hosted_checks_snapshot.txt` shows the following:

- Completed success: `rtl-fast`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, Yosys shards 0-3/4 and Verilator shard 3/5.
- Still in progress at the snapshot: Verilator shards 0, 1, 2 and 4/5, and `docs-check`.
- Skipped by design, which is not an executed job: `Physical gPTP (nightly and manual)`.

This reviewer does not accept hosted results; the manager does.

## Real limits

- This round did not re-run the mutation campaign. Its Tests and Robustness depth relies on R283-2's mutant kills at `910b4fb5`. That depth carries here because the harness files and the comment-free servo logic are byte-identical, and this round shows the identity, but no mutant was re-executed at this head.
- Not run by this reviewer:
  - `mmcm_servo_autorepair`, the `milan_dp` legs (`aclk`, `tdm8render`, `gmstep`), `xvlog_gate`, `lint_rtl`, synthesis/area, and the full parent/PP/gPTP/Yosys/builder banks (out of scope for this round);
  - act, Docker and hardware (not allowed).
- Physical calibration and hardware behaviour are NOT RUN. Simulation and skipped physical contexts are not hardware proof.
- The final current-dev candidate was not validated: source base `26d855a9`, live dev `9d3288107edc97fe13d894874a6ca6c7e00de1ba`. This review is source-head evidence only.
- The public review-evidence tree at `1363d132` holds round-1 material. This round did not use it as evidence for this head.

## Pending manager duties

- Accept or reject the exact-head hosted contexts once the in-progress Verilator shards and `docs-check` finish, and record act evidence per the CI workflow policy.
- Build and validate the candidate merge result against live `dev` at the merge turn, then run post-merge containment.
- Confirm the second independent positive (internal R282-3) before merge. Merge only with explicit maintainer authorization.
- Close #539 through `Closes #539` and move it to Done. #545 and #546 stay open as separate work; they are outside #539's frozen acceptance.

## Receipts

All receipts and scripts are listed in `MANIFEST.sha256`. The scripts take the clone path and the simulator path as arguments. Host paths in receipts are replaced by `<VERILATOR_PREFIX>`, `<PINNED_VERILATOR>` and `<PACKET>`. After the probes, the clone was verified exact:

- HEAD, tree and index all equal the head;
- 875 tracked blobs match in bytes and mode;
- there are no untracked files;
- the gitlinks are `external` `efeb541a`, `gptp-processor` `e5dcea6e`, `protocol-processor` `424c688f` and `third_party/verilog-axis` `48ff7a7e` (`receipt_clone_integrity.txt`).

R283-3 FINISHED
