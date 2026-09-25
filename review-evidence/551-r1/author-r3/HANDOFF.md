# [A312] Merge-dev handoff for #551 / PR #553

Status: assigned merge-dev round complete locally; all requested gates pass. Ready for full independent review.

Start: `babb8925030612e47c687b1fda1a1ce614988721`.
Requested dev tip: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
Origin verified: https://github.com/kebag-logic/milan-fpga.git.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5831903033.

## Scope

Merge dev, preserve both licence-gate behaviours, make unwarmed refusal a default passing fixture, run the pre-fix processor control locally, and update the assigned docs. No push or PR edits.

## Conflict resolutions

The merge produced five conflict hunks in three files. Original markers and both sides are retained in `merge-conflicts.diff`. Final references below name the merge commit.

1. `hdl/milan/milan_datapath.sv:6594`, original lines 6596-6638: retain the ACTIVE AND real-grant licence. Integrate dev's published-round window and current-declaration grant semantics. Keep Listener registration as a prerequisite.
2. `hdl/milan/milan_datapath.sv:6617` and `:6623`, original lines 6651-6699: retain the two-term assignment and closing-edge behavior; preserve dev's re-declaration grant retirement and published-round slope hold. Remove superseded ACTIVE-only/refused-emission claims.
3. `docs/reference/REGISTER_MAP.md:1108`, original lines 1108-1128: retain the two-term licence and Listener rule, qualify optimism as published rounds, and preserve the no-shaper boundary.
4. `docs/reference/REGISTER_MAP.md:1122` and `:1128`, original lines 1138-1174: retain per-index CSR bit distinctions; replace the obsolete residual with dev's current-TSpec evaluation and pending-round publication hold. Record that slope updates only at a published round.
5. `tb/verilator/milan_dp/README.md:26` and `:27`, original lines 26-32: keep dev's GET_STREAM_INFO notify-leg coverage and mutation entry; keep this lane's two-term licence entry and make changed-TSpec refusal a default required pass.

The merged processor gitlink is `990f96526bb89356c963a260ebbdcf2a77e6623a`; ancestry includes `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`. `git submodule update --init` completed successfully.

## Fixture and pre-fix control

- Fixed pin: `crflic` passes 415 checks, zero failures. Both unchanged and changed TSpec histories run by default, including the unwarmed refusal `[I]`. Reverse changed-TSpec admission `[J]` re-measures the latency requested in R296-1 F1 and the prior handoff.
- Measured added latency (same/changed histories agree): AAF phase 0/1 = 5/5 cycles; CRF = 3/5. At 100 MHz this is 30--50 ns; those cycle counts at 50 MHz represent 60--100 ns. Normal Listener Ready adds zero.
- The single local control temporarily repinned the existing processor submodule to `7a47f5788ff504f099a47ad4407c340771bb6bdb` (first parent of `a8f8ce81`), built the unchanged fixture into `/tmp`, and ran `--unwarmed-refusal` once. Build rc 0; fixture rc 1 with 34 total failures, exactly 28 in `[I]`. Six additional `[J]` checks expose the pre-fix ACTIVE re-rise/timing bookkeeping described in R297-1; no acceptance assertion was weakened. Each source/phase fails the same seven no-grant/no-licence/no-counter-pair/preserved-counter assertions. No refused-case PDU was observed in that schedule.
- `prefix_control.py` restores the original index gitlink and submodule in `finally`; it completed and verified the fixed HEAD and clean submodule. The temporary build was removed. No control pin or processor source edits are shipped.
- Receipts: `crflic.log`, `prefix_build.log`, `prefix_fixture.log`, `prefix-refusal-failures.txt`. The negative control's rc 1 is the expected defect evidence, not an acceptance-gate failure.

## Changed artifact references

- `tb/verilator/milan_dp/sim_crf_licence.cpp:1078`: void CrfLicenceHarness::grant_case
- `tb/verilator/milan_dp/sim_crf_licence.cpp:1165`: void CrfLicenceHarness::phase_real_grant
- `tb/verilator/milan_dp/sim_crf_licence.cpp:1197`: int CrfLicenceHarness::run
- `hdl/milan/KL_pp_shadow.sv:639`: //! Raw per-source grant, excluding optimism.
- `docs/reference/FR_NFR.md:220`: > Refused re-declarations cannot
- `docs/reference/EGRESS_QUEUE_MAP.md:77`: The shipping licence now requires
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:179`: | 5.3.7.3 | talker transmit licence
- `docs/traceability/ieee8021q.md:96`: | Q-9 |
- `docs/traceability/ieee8021q.md:97`: | Q-10 |
- `CHANGELOG.md:85`: ## Unreleased - licence and LeaveAll scope
- `tb/verilator/milan_dp/README.md:442`: Measured ACTIVE-to-licence latency
- `tb/verilator/milan_dp/README.md:468`: | the pre-#112 processor

## Gate summary

- Full behaviour suite: 14 features, 344 scenarios and 1739 steps passed; none failed or skipped.
- Licence leg: 415 checks, zero failures, including required changed-TSpec refusal and reverse admitted history.
- Licence campaign: 7/7; all six mutants caught, including all three real-grant removals.
- Default sweep: 14 simulation legs passed; built-in render controls 6/6 and grandmaster-step controls 4/4.
- Every requested static gate returned 0. Both documentation inventory modes ran.
- Expected local pre-fix control: build 0, fixture 1; 34 total failures, including the 28 targeted unwarmed-refusal failures. Fixed pin restored and clean.

## Regenerated files

Ran `python3 docs/traceability/gen_module_matrix.py`: rc 0, 14 artifacts considered, 69 modules, zero untested. No generated blob changed relative to the automatic merge. `regenerated-files.txt` lists all 14 artifacts. The existing `docs/traceability/MODULE_MATRIX.md` and `hdl/milan/README-tests.md` keep the `KL_pp_shadow` 34.3/34.4 mapping. `gen_toc.py --check` passed; no TOC regeneration was needed.

## Validation

Every gate runs in the foreground without a pipeline. Commands below use repository root, except `behave` in `tests`. Raw commands, working directories, exit codes and durations are in `gates.jsonl`. The negative control is recorded separately above.

| Gate | Command | Result | Evidence |
|---|---|---|---|
| Full behaviour suite | `behave --no-capture -f plain` | rc 0 | `behave.log` |
| Licence leg | `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8` | rc 0 | `crflic.log` |
| Licence mutation campaign | `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8` | rc 0 | `crflic_mutants.log` |
| Default datapath sweep | `make -C tb/verilator/milan_dp VERILATOR_JOBS=8` | rc 0 | `milan_dp_default.log` |
| Documentation, Git inventory | `python3 scripts/docs_check.py` | rc 0 | `docs_git_final.log` |
| Documentation, filesystem inventory | `env GIT_DIR=/tmp/551-a312-no-git-absent python3 scripts/docs_check.py` | rc 0 | `docs_no_git_final.log` |
| Added-line em dash | `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | rc 0 | `em_dash_final.log` |
| Documentation style | `python3 scripts/check_doc_style.py` | rc 0 | `doc_style_final.log` |
| Contents | `python3 scripts/gen_toc.py --check` | rc 0 | `gen_toc.log` |
| Cited paths | `python3 scripts/check_doc_paths.py` | rc 0 | `doc_paths.log` |
| Generated matrices | `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 | `module_matrix.log` |
| Syntax analysis | `python3 scripts/xvlog_gate.py --check` | rc 0 | `xvlog.log` |
| RTL source lists | `python3 scripts/check_rtl_source_lists.py` | rc 0 | `rtl_source_lists.log` |
| Python idiom | `python3 scripts/check_py_idiom.py` | rc 0 | `py_idiom.log` |
| C++ idiom | `python3 scripts/check_cpp_idiom.py` | rc 0 | `cpp_idiom.log` |
| Whitespace | `git diff --check` | rc 0 | `diff_check.log` |

Initial attempts: `em_dash.log` judged the pre-merge HEAD (the script reads committed HEAD), and `doc_style.log` found three overlong changelog sentences. The merge commit and the shortened sentences are covered by the successful final receipts above. No unrelated dev text was edited to address those pre-merge diagnostics.

Syntax analysis actually ran: zero first-party findings and four unchanged pinned-processor findings at the existing ratchet. The filesystem documentation run explicitly skips its Git inventory-parity arm only.

The committed delta also passes `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD` (`committed_diff_check.log`).

Gate environment: pinned simulator 5.050 from the existing shared prefix and the existing hash-locked Markdown environment, both outside the output directory. No toolchains, SDK copies, virtual environments, installed packages or source-tree exports are stored in the output directory.

## Final state

Head: `9eee43831d487a52637d34d87a727f6e174e7cab`.
Parents: `babb8925030612e47c687b1fda1a1ce614988721`, `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
Subject: `Merge dev into 551-licence-real-grant`; no body or trailers.

The only non-comment RTL difference from dev in the two touched modules is the intended ACTIVE AND per-source real-grant assignment (`rtl-token-delta.txt`). Automatic dev changes, including #508 boot and GET_STREAM_INFO handling and #387 media behavior, remain intact.

The mutation campaign passed 7/7 (all six mutants caught, including all three real-grant removals). The default sweep passed all 14 simulation legs, render controls 6/6 and grandmaster-step controls 4/4 (1420.09 seconds). Independent full review by [R296] and [R297], publication, hosted/local workflow evidence and final merge validation remain for the next authorized round. This handoff claims implementation and local gate evidence, never reviewer approval. No push, PR creation/edit, merge into dev, sub-agent, additional checkout, hardware action or processor source edit was performed.
Reviewers: [R296] and [R297], full review required at new head.

Final audit: `final-state.txt` confirms the expected branch, exact two-parent merge, clean worktree/index and clean submodules at the merged gitlinks. `versions.txt` records the existing gate environment. Logs and helper scripts are evidence only; no SDK, package installation or source-tree export is in this directory.

Public review-ready comment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5832433228
