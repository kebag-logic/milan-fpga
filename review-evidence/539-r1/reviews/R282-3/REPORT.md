[R282] POSITIVE - exact head 324eb343a870973b64706779d0183ae342dcb3d7

# R282-3 internal independent review: issue #539 / PR #547, round 3

- Head `324eb343a870973b64706779d0183ae342dcb3d7`, tree `84170bb655b0f547caf7826de541a467db655703`. Verified in the review clone; the index tree equals the head tree (`receipts/clone_integrity.txt`).
- Source base `26d855a9176d63625e6635a029a0c44e3d57ce9a`. The PR-owned delta is `f86c34fe..324eb343` (dev `f86c34fe` was merged at `0df54c1f`). Live dev at assignment: `9d3288107edc97fe13d894874a6ca6c7e00de1ba`.
- Round-3 delta `910b4fb5..324eb343`: 2 commits, 2 files, +2/-2.
  - `5c6d5f5b`: `tb/verilator/milan_dp/README.md:388`.
  - `324eb343`: one comment line, `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:302`.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #539 body and its seven comments (assignments, takeover, three REVIEW READY posts), `timestamp_counter.sv:100-110`, the PHC and servo instances in `milan_datapath.sv:2810-2830` and `:5524-5530`, the Step policy table in `docs/design/TIME_SYNC.md:85`, the round-3 delta, the PR-owned diff `f86c34fe..324eb343`, the PR body, and exact-head hosted check runs.
- The public evidence tree `review-evidence/539-r1` at `1363d132` holds only the round-1 author packet. I found no manager bank log for this head in it. Every result below comes from my own runs, with receipts in this packet.
- I read prior review findings only after my own pass over the diff. My verdict was drafted before I read them.

## Verdict

**POSITIVE.** There are no open findings at this head. All five lenses were applied at this head and are clean.

- Round-3 servo edit is comment-only. With comments stripped, the file is byte-identical at `910b4fb5` and `324eb343`. The simulator preprocessor output (`-E -P`) is also byte-identical.
- `README.md:388` now agrees with `GM_LOSS_RECOVERY.md:181`.
- No stale #539 gap wording remains in `tb/`, `docs/` or `hdl/`.
- The corrected margin figures are exact: 10.7x and 4.9x.
- The three servo harnesses pass at this exact head: 78/78, 8/8 and 113/113.

## Findings

None open. There is no new SUGGESTION.

### Prior findings at this head

| Prior finding | Status at `324eb343` | Evidence |
|---|---|---|
| R282-2 F1 = R283-2 F1, MINOR, Docs: `tb/verilator/milan_dp/README.md:388` said "its step guard gap is #539" | **RESOLVED** | Line 388 reads "The CRF servo. The MMCM DRP answers zero. `Vphc_step` grades its step discard (#539)." `GM_LOSS_RECOVERY.md:181` reads "The CRF servo: its DRP answers zero. `Vphc_step` grades its step discard (#539)." Same claim. `Vphc_step` is a real target (`tb/verilator/mmcm_servo/Makefile:10,45-47`), and it passed 113/113 here. The gap grep returns rc 1 at the head and matches line 388 at `910b4fb5`, which is the control (`receipts/stale_wording_grep.txt`, `receipts/readme_vs_gmloss.txt`). `sim_gmstep.cpp:16` ("the DRP answers zero; #539") claims no gap. It can stay, as both round-2 reviewers allowed. |
| R282-2 S1, SUGGESTION, RTL/Docs: "5x below" should be 4.9x | **RESOLVED** | `KL_mmcm_drp_servo.sv:302` reads "10.7x above the one and 4.9x below the other". 4096/384 = 10.667 and 20000/4096 = 4.883. The 384 ns bound is exact: the Q8.24 unsigned `incr` max of 255.99999994 ns plus the signed `adj` max of 127.99999994 ns is less than 384 ns. The 20 us figure is the Step policy's link-up step (`TIME_SYNC.md:85`). See `receipts/margin_arithmetic.txt`. |
| R282-1 F1 = R283-1 F1 (Tests), R282-1 F2 (Docs), R283-1 S1-S3 | Resolved at round 2. **Still resolved** at this head. | `sim_main.cpp` and `sim_phc_step.cpp` are unchanged since `910b4fb5`, and the servo logic is byte-identical. U10, U11 and U12 are in the 78/78 unit run (`receipts/mmcm_servo_suite.log`). The `GM_LOSS_RECOVERY.md:152,154,181` and `TIME_SYNC.md:147-148` rows are unchanged since round 2 and still match the RTL. |

## What was checked, and the result

1. **The round-3 servo edit is comment-only** (`receipts/comment_only_proof.txt`, `strip_comments.py`, `comment_only_proof.sh`).
   - The blobs differ: `8af6059e` becomes `9459a26b`.
   - The comment-stripped text is identical: sha256 `44395178...f605` at both commits.
   - Negative control: the stripper detects a real edit. Changing 4096 to 4095 changes the hash (`6d49dc7d...`).
   - With the pinned simulator's `-E -P`, the preprocessed output is also identical at both commits: sha256 `3f2b1ca6...c81a`, 536 lines (`receipts/preprocess_compare.txt`).
   - `git diff --name-only 910b4fb5 324eb343` lists only the two expected files.
2. **Stale wording** (`receipts/stale_wording_grep.txt`). At the head, `git grep -niE 'step guard gap|guard gap|gap is #539|#539.{0,40}gap|gap.{0,40}#539' -- tb docs hdl` returns rc 1, with no match. The same grep at `910b4fb5` hits README:388.
   - I reviewed every `#539` mention in `tb/ docs/ hdl/` at the head. Each describes the discard.
   - A wider sweep covered "step guard" and "servo ... gap" (`receipts/readme_vs_gmloss.txt`). It found only:
     - the 1024 ppm guard's own description;
     - archived `docs/history` lines;
     - `KL_media_grid_align.sv:21`, which is about the TDM/packet grid offset and is unchanged in this PR.
3. **Servo harnesses at the exact head** (`run_servo_suite.sh`, `receipts/mmcm_servo_suite.log`).
   - Method: a `git archive` export of `324eb343`, built with the pinned simulator 5.050 (`receipts/tool_identity.txt`) at 8 jobs.
   - Results: `KL_mmcm_drp_servo` 78/78, `rails` 8/8 and `phc_step` 113/113. make rc 0.
4. **Disposable probe on the margin the comment names** (`run_mutant_stepdet.sh`, `receipts/mutant_stepdet_24576.log`).
   - Probe: `STEP_DET_NS_C` raised from 4096 to 24576, above the 20 us link-up step. This was done in a scratch copy only.
   - Result: the step suite fails 23 of 113. The first failures are `[P1 +21000 ns]`: no discard counted, the integrator moved 10520, and LOCKED was lost.
   - So the "below the 20 us step" side of the margin is guarded by an executable check.
5. **Independent RTL read of the PR-owned servo diff** (`KL_mmcm_drp_servo.sv:54-77, 296-304, 446-462, 598-610, 650-670, 907`).
   - `ptp_jump_r` is registered on the same edge that stages `ptp_q_r`, so the verdict is aligned with the sample.
   - The 32-bit unsigned difference catches a backward step as a wrap.
   - The step is only counted inside an open window: `step_hit_w` is gated by `win_valid_r`.
   - The 7-bit tally sum saturates at 63, and cannot overflow: 63+2 = 65.
   - The step handling is placed after the tick and micro-sequence writes, so its writes win.
   - The per-cycle advance bound holds on the real wiring. The servo's `clk_i` is `axis_clk`, and the PHC is on `gtx_clk`, which is equal in every real instantiation (`milan_datapath.sv:2810-2811`). The PHC uses `INCR_WIDTH` 32 and `FRAC_WIDTH` 24 (`:2813-2816`).
6. **Docs gates at the head** (`receipts/doc_gates.txt`).
   - `git diff --check` from `910b4fb5` and from `26d855a9`: rc 0.
   - `check_em_dash --base 910b4fb5`: 0 findings.
   - `docs_check`: 0 findings over 165 md files.
   - `check_doc_style`: OK.
   - `check_doc_paths`: OK, 838 paths.
7. **PR body** (read-only). The Round 3 section and the findings table describe `5c6d5f5b` and `324eb343` accurately. The body carries `Closes #539`. The author's comment-stripped hash `d48be6f0...` uses a different normalisation from mine, and both show identity.

## Lens results

```text
[R282] PASS Conformance - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:446-462,650-670; receipts/mmcm_servo_suite.log (phc_step 113/113) - #539 acceptance 1-3 unaffected at 324eb343: the servo logic is byte-identical to 910b4fb5 once comments are stripped (receipts/comment_only_proof.txt, preprocess_compare.txt); the silicon-scale step sweep 21 us to +/-1 s passes at this exact head; the 4096 ns threshold lies between the 384 ns legitimate advance and the 20 us Step-policy link-up step (TIME_SYNC.md:85, receipts/margin_arithmetic.txt)
[R282] PASS RTL - KL_mmcm_drp_servo.sv:296-304,446-462,598-610,650-670 against timestamp_counter.sv:100-110 and milan_datapath.sv:2810-2816,5524-5530 - round-3 edit is comment line 302 only (hash-identical comment-free text and preprocessor output); detector alignment, wrap handling, open-window gating, tally saturation and write precedence re-read at this head; clock equality gtx_clk == axis_clk makes the incr+adj per-cycle bound hold
[R282] PASS Robustness - KL_mmcm_drp_servo.sv:446-462,650-670; receipts/mmcm_servo_suite.log (U10 storm, U11 re-base, U12 streak/open-window/saturation/IDLE-clear), receipts/mutant_stepdet_24576.log - both signs, backward wrap, step with no window open, repeated steps and saturation are exercised and pass at this head; the threshold-above-20us probe fails 23 checks, so the margin has an executable guard
[R282] PASS Tests - tb/verilator/mmcm_servo/sim_main.cpp, sim_phc_step.cpp, Makefile (unchanged since 910b4fb5); receipts/mmcm_servo_suite.log 78/78, 8/8, 113/113 at 324eb343 - the harnesses that grade the servo pass at the exact head; round-1 test findings stay resolved (U10/U11/U12 present and passing); a fresh disposable mutant fails the step suite
[R282] PASS Docs - tb/verilator/milan_dp/README.md:388 vs docs/design/GM_LOSS_RECOVERY.md:181; KL_mmcm_drp_servo.sv:302; receipts/stale_wording_grep.txt, readme_vs_gmloss.txt, doc_gates.txt, margin_arithmetic.txt - README:388 states the post-#539 behaviour identically to GM_LOSS_RECOVERY.md:181; no stale #539 gap wording in tb/ docs/ hdl/ (control hit at 910b4fb5); the 10.7x/4.9x figures are exact; docs gates clean; PR body current
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_mmcm_drp_servo.sv:446-462,650-670`; `phc_step` 113/113; comment-only and preprocess proofs; `TIME_SYNC.md:85` | R282-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:296-304,446-462,598-610,650-670,907`; `timestamp_counter.sv:100-110`; `milan_datapath.sv:2810-2816,5524-5530`; comment-free hash and `-E -P` identity | R282-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Robustness | CLEAN | Unit U10-U12 and step suite P1-P4 at this head; threshold probe (23 failures) | R282-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Tests | CLEAN | `tb/verilator/mmcm_servo/{sim_main.cpp,sim_phc_step.cpp,Makefile}`; 78/78, 8/8, 113/113 | R282-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |
| Docs | CLEAN | `tb/verilator/milan_dp/README.md:387-388`; `GM_LOSS_RECOVERY.md:152,154,181`; `TIME_SYNC.md:147-148`; `REGISTER_MAP.md` `0x8F8`; `TESTING.md` mmcm_servo row; servo comment `:302`; PR body; docs gates | R282-3 | `324eb343a870973b64706779d0183ae342dcb3d7` |

Each lens was applied at this exact head in this round. None depends on carrying earlier coverage forward.

## Limits (what this round did not do)

- **Simulation runs.** I ran only the `tb/verilator/mmcm_servo` harnesses. I did not run:
  - `mmcm_servo_autorepair`, `milan_dp` (`aclk`, `gmstep`) or `milan_dp_render`;
  - the full parent, PP or gPTP banks;
  - Yosys, the builder, `lint_rtl`, `xvlog_gate`, `check_sv_idiom` or `check_cpp_idiom`.

  For round 3 these rest on two facts: the servo logic is byte-identical to `910b4fb5`, and no harness changed. For the full source banks they rest on the manager's reported pass. I did not find that pass as a public log in `review-evidence/539-r1` at `1363d132`.
- **Mutation.** I did not re-run the full round-1 and round-2 mutant sets. The RTL logic and harnesses are identical to `910b4fb5`, where those sets were published. I ran one fresh probe.
- **Hosted checks at this head** (`receipts/hosted_checks.txt`, read 2026-09-24T09:55:54Z):
  - Passed: `rtl-fast`, Verilator shards 0, 2 and 3, all four Yosys shards, `yosys-elaboration`, `verilator-lint`, docs, `bdd-conformance` and `elaborate`.
  - In progress: Verilator shards 1/5 and 4/5.
  - Skipped, not executed: "Physical gPTP (nightly and manual)". That skip is not hardware proof.
- **Hardware.** Physical calibration was NOT RUN, and no hardware was touched.
- **Redaction.** One receipt (`mmcm_servo_suite.log`) has the local simulator install prefix replaced by `<PINNED_TOOL_PREFIX>`. Nothing else was edited.

## Pending manager duties

- Confirm that hosted Verilator shards 1/5 and 4/5 finish green at `324eb343`. Also confirm the protected contexts and the act replica. Hosted and act acceptance belong to the manager.
- Build and validate the final current-dev candidate merge: source base `26d855a9`, live dev `9d3288107edc97fe13d894874a6ca6c7e00de1ba`. This source-head review does not cover that result.
- Obtain the second independent positive review (R283-3) and assemble the full completion bar. That includes post-merge containment and the maintainer's merge authorization.
- Publish the source-bank logs for this head, if they are to be cited as public evidence.

## Clone integrity after probes

All probes ran in `scratch/` exports; the review clone was never edited. At the end, HEAD is `324eb343`. `git status` is empty, including untracked files. The index and worktree equal HEAD, and `git write-tree` gives `84170bb6...` = the head tree. The gitlinks match HEAD:

- `external` `efeb541a`
- `gptp-processor` `e5dcea6e`
- `protocol-processor` `424c688f`
- `third_party/verilog-axis` `48ff7a7e`

See `receipts/clone_integrity.txt`.

R282-3 FINISHED
