[A294] Round 4 handoff for PR #554 / issue #546

Assignment: https://github.com/kebag-logic/milan-fpga/issues/546#issuecomment-5824704845

Merge head: `f5532c4c3f94a516b748cc4627dc5f78d05fa73e`.
First parent: `0c61d458941088f3847513b7c6fe6589c75b4270`.
Second parent: `c266432dcb0cdd464205823a3d82cad260eedde2`.
Commit message: `Merge dev into 546-crf-talker-step`.

## Scope and resolution

Fetched `dev` with `git fetch origin dev`; the fetched tip was the assigned second parent.
Merged that exact commit with an explicit merge commit. One file conflicted, in two hunks:
`docs/design/GM_LOSS_RECOVERY.md`.

The resolved document is the dev version with the author parent's media-grid-aligner
and CRF-servo rows, plus both author-parent `crf_rx` verification rows.
The landed render, outgoing `mr`, MEDIA_RESET, pending-restart, gmstep and tkdiag
rows are retained verbatim from dev. In particular, the gmstep row keeps
"three negative controls in the sweep". The receiver wording retains both tu-edge
and timestamp-jump invalidation, 256 clean intervals before resuming, and held lock
and integrator. The local-slew follow-up remains #545.

`git show --remerge-diff --format= --name-only HEAD` names only the recovery document.
No other manual content change was made. The merge is local and has not been pushed.
No PR edit, additional checkout, sub-agent, or hardware action was performed.

Updated the required submodules with:

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

All three match the merged gitlinks:

| Submodule | Commit |
|---|---|
| `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| `protocol-processor` | `09f9bf3846511f8388d995126502ed92eaa65213` |
| `gptp-processor` | `e5dcea6e351abff18a27a00f8e345f3251bdbd8f` |

## Auto-merged overlap check

The changes were compared against each parent and checked in the resulting source.
The two complete comparisons are [from the author parent](overlaps-from-author.patch)
and [from dev](overlaps-from-dev.patch). No overlap required an edit.

| Artifact at the merge head | Semantic agreement |
|---|---|
| `docs/reference/REGISTER_MAP.md:127,841` | The landed text gates only CRF restart triggers by CRF selection; a local PHC step reaches every running output. The receiver's `CRF_RATE` row independently retains the last clean rate during refill, with internal sample validity and no new CSR bit. |
| `docs/testing/TESTING.md:166,267,463,501` | The 3600-second `milan_dp` deadline, gmstep controls and tkdiag pending-restart tests remain from dev. The receiver row retains talker-only and both-end steps, 600 ms lag and the default validity/refill controls. These describe separate retained targets. |
| `scripts/measure_test_evidence.py:597,614,645,722` | The receiver-and-servo mutation disposition coexists with the landed gmstep and restart-engine dispositions. The runner contract uses 1800/3600/5400 seconds, matching `scripts/run_all_suites.sh:245`; the check and self-test validate that merged contract. |
| `docs/design/TIME_SYNC.md:147,167,266` | Receiver history invalidation and the full 256-interval refill remain. Render re-centering uses a PHC step/settime or settled source change; GM identity alone does not trigger it. Remote receiver validity and local PHC guards remain separate. |
| `hdl/milan/milan_datapath.sv:1725,3111,5502,5561,6029` | Relative to dev, the file adds exactly the receiver-validity wire and its producer/consumer connections. The landed PHC-step restart expression and render trigger are unchanged. There is one validity declaration, one receiver output connection and one servo input connection; no duplicate pins or competing drivers were introduced. |

## Gates

All 15 assigned command invocations returned **0** at the merge head.

| Command | Mode | Exit | Seconds | Result / log |
|---|---|---:|---:|---|
| `make -C tb/verilator/crf_rx` | merged worktree | 0 | 641.48 | Main: 13,836 checks; discontinuity: 1,658; connected: 69; mutation campaign: 8. All zero failures. [log](crf_rx.log) |
| `make -C tb/verilator/mmcm_servo` | merged worktree | 0 | 365.19 | Unit: 85 checks; rails: 8; PHC step: 113. All zero failures. [log](mmcm_servo.log) |
| `python3 scripts/measure_test_evidence.py --check` | merged worktree | 0 | 7.83 | Ratchet passes; runner contract OK; zero unexplained source readers. Existing budgets unchanged. [log](measure_test_evidence_check.log) |
| `python3 scripts/measure_test_evidence.py --selftest` | merged worktree | 0 | 5.94 | 101/101 checks pass. [log](measure_test_evidence_selftest.log) |
| `python3 scripts/docs_check.py` | Git inventory | 0 | 4.19 | Git inventory: zero findings; 165 Markdown files and 864 scrubbed text files; 23/23 scrub controls. [log](docs_check_git.log) |
| `python3 scripts/docs_check.py` | no Git | 0 | 4.03 | Filesystem inventory: zero findings; same 165/864 files; 22/22 scrub controls. Inventory parity is explicitly skipped because Git is absent. [log](docs_check_no_git.log) |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` | merged worktree | 0 | 3.12 | Zero findings over 81 added lines in 7 Markdown pages; 339/339 controls. [log](check_em_dash.log) |
| `python3 scripts/check_doc_style.py` | merged worktree | 0 | 0.07 | 22 current documents pass. [log](check_doc_style.log) |
| `python3 scripts/gen_toc.py --check` | merged worktree | 0 | 2.45 | 107 contents lists current; 17 pages below the section threshold. [log](gen_toc.log) |
| `python3 scripts/check_doc_paths.py` | merged worktree | 0 | 0.11 | 841 cited paths resolve; one allowlisted. [log](check_doc_paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | merged worktree | 0 | 0.96 | Current: 69 modules, zero untested; 5/5 generator controls. [log](module_matrix.log) |
| `python3 scripts/xvlog_gate.py --check` | merged worktree | 0 | 136.37 | Analysed 72 first-party and 48 pinned-processor files. Zero first-party findings; four existing processor findings match the ratchet. [log](xvlog_gate.log) |
| `python3 scripts/check_cpp_idiom.py` | merged worktree | 0 | 1.25 | 151 first-party translation units; all checks at zero or within budget. [log](check_cpp_idiom.log) |
| `python3 scripts/check_py_idiom.py` | merged worktree | 0 | 3.42 | All checks at zero or within the existing budgets. [log](check_py_idiom.log) |
| `git diff --check` | merged worktree | 0 | 0.04 | No whitespace errors; final worktree is clean. [log](git_diff_check.log) |

Connected-run evidence: LOCKED was retained, no receiver re-lock was counted, and
the maximum integrator movement was 0.020 ppm. Each discriminating talker-only
or 600 ms-lag case crossed one servo boundary inside invalid history. The quiet
control observed 550 post-edge artifacts but zero sampled invalidity. Both servo
validity mutants were rejected by the required named U13 failures.

Machine-readable exits and durations: [gates.json](gates.json).

Each command ran in the foreground, without a pipeline, with its own 7200-second
outer timeout and a recorded exit status. Logs are adjacent to this file.
The pinned documentation dependencies were installed in a temporary environment
outside the output directory. The no-Git mode used an archive of the exact merge
head under `/tmp`, without Git metadata, and the same `docs_check.py` command.
That temporary export was removed after validation. No toolchain, SDK, virtual
environment or tree export was placed in the output directory.

## Resolved hunks, before and after

The following remerge diff shows both original conflict sides on removed lines
and the committed union on added/context lines. Parent and resolved snapshots
are also saved as [author before](gm-before-author.md), [dev before](gm-before-dev.md),
[conflicted merge](gm-conflicted.md) and [resolved after](gm-resolved.md).

```diff
diff --git a/docs/design/GM_LOSS_RECOVERY.md b/docs/design/GM_LOSS_RECOVERY.md
remerge CONFLICT (content): Merge conflict in docs/design/GM_LOSS_RECOVERY.md
index ef54a2c8f..71c79e7ac 100644
--- a/docs/design/GM_LOSS_RECOVERY.md
+++ b/docs/design/GM_LOSS_RECOVERY.md
@@ -148,23 +148,13 @@ Issue #387 decided its media reaction.
 | Element | Decided reaction to one step | This tree |
 |---|---|---|
 | `tu` | Rises on the step; clears after at least 0.25 s of holdover | Yes: `KL_ptp_clock_validity` takes the plane's step pulse |
-<<<<<<< 0c61d4589 (Shorten the CRF clock-bound citation sentences)
-| Render setpoint stage (#386) | Re-centres in "one bounded, counted event" (decision part b) | Yes, at the next PDU end, counted in its recentre tally; a grandmaster identity change also re-centres it |
+| Render setpoint stage (#386) | Re-centres in "one bounded, counted event" (decision part b) | Yes: `render_recentre_p_w` takes the step (`media_rebase_p_w`), and the stage re-centres at the next PDU end, counted in its recentre tally. A grandmaster identity change is no longer a trigger of its own. The gmstep leg counts one re-base, 132 cycles after the plane's step pulse at each of its 42 feed delays |
 | Media grid aligner's phase reference | "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event" (decision part b) | No re-centre: `KL_media_grid_align.sv` has no PHC or step input. Under CRF selection a step reaches it only through the CRF-steered grid. The CRF servo discards the window a local PHC step lands in (#539); the receiver excludes talker-step rate samples (#546). A policy-legal local slew remains tracked by #545. By [owner decision on #387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282) the aligner gets no re-centre of its own: part b is met by keeping the step out of its reference, #539 isolating it at the servo and #545 and #546 closing the remaining paths. Option B, an explicit counted re-lock, is revisited only if #545 or #546 cannot close its path |
 | Packet NCO | Not named by the decision | No PHC or step input |
 | CRF servo | Keeps its window guard | Yes: `KL_mmcm_drp_servo` discards the window a local PHC step lands in, trim and integrator held, and counts it in `MCSRV_STAT[15:10]` (#539). It still discards a window above 1024 ppm. The receiver invalidates rate history on tu transitions or timestamp jumps (#546). After 256 clean intervals, sampling resumes; lock and integrator hold meanwhile. A policy-legal local 100 us slew remains tracked by #545 |
-| Outgoing `mr` (IEEE 1722-2016 4.4.4.3) | Toggles once | Not yet: `mcr_restart_p_w` ignores the step |
-| Talker MEDIA_RESET (Milan Table 5.4) | Counts that one toggle | Not yet: no toggle to count |
-| A step while an `mr` restart is pending | Merges with it: exactly one restart, never a cancellation, and the step's MEDIA_RESET is still counted (ruling 5802264260 item 2) | Not yet: `KL_media_clock_restart` flips its target once per request, so a second request before the first reaches the wire cancels it |
-=======
-| Render setpoint stage (#386) | Re-centres in "one bounded, counted event" (decision part b) | Yes: `render_recentre_p_w` takes the step (`media_rebase_p_w`), and the stage re-centres at the next PDU end, counted in its recentre tally. A grandmaster identity change is no longer a trigger of its own. The gmstep leg counts one re-base, 132 cycles after the plane's step pulse at each of its 42 feed delays |
-| Media grid aligner's phase reference | "the render elastic stage (#386) and the media grid aligner's phase reference re-centre in one bounded, counted event" (decision part b) | No re-centre: `KL_media_grid_align.sv` has no PHC or step input. Under CRF selection a step reaches it only through the CRF-steered grid. The CRF servo discards the window a local PHC step lands in (#539); what still reaches that grid is a policy-legal slew (#545) and the talker's own step (#546). By [owner decision on #387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282) the aligner gets no re-centre of its own: part b is met by keeping the step out of its reference, #539 isolating it at the servo and #545 and #546 closing the remaining paths. Option B, an explicit counted re-lock, is revisited only if #545 or #546 cannot close its path |
-| Packet NCO | Not named by the decision | No PHC or step input |
-| CRF servo | Keeps its window guard | Yes: `KL_mmcm_drp_servo` discards the window a local PHC step lands in, trim and integrator held, and counts it in `MCSRV_STAT[15:10]` (#539). It still discards a window above 1024 ppm. A policy-legal 100 us slew still moves its integrator (#545), and so does the talker's own step (#546) |
 | Outgoing `mr` (IEEE 1722-2016 4.4.4.3) | Toggles once | Yes: `mcr_restart_p_w` takes the step whatever the media clock source. The gmstep leg, under CRF selection, sees one toggle, first sent 75 to 116 cycles after the step pulse over its 42 feed delays. On an INTERNAL media clock the `milan_dp` option-off legs (`obj_dir`, `obj_nolpf`, `obj_ax1x1`) grade `mr` against every PHC step the harness issues, a CLKV adjtime and then a software settime; a control that gates the step's toggle by CRF selection fails them |
 | Talker MEDIA_RESET (Milan Table 5.4) | Counts that one toggle | Yes: `KL_talker_diag_ctx` counts the `mr` bit each PDU carried. The gmstep leg reads one, and none between the commit and the step. The option-off legs read one for the software settime, and a control whose settime does not toggle `mr` fails them |
 | A step while an `mr` restart is pending | Merges with it: exactly one restart, never a cancellation, and the step's MEDIA_RESET is still counted (ruling 5802264260 item 2). Pending lasts until a PDU at the new level has gone out ([ruling on #387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5818091077)) | Yes: `KL_media_clock_restart` keeps a stream pending while the request waits for the hold of the stream's previous toggle, and after the stream adopts the new level until its first PDU at that level. A second request in either part merges. A request after that first PDU is a new restart, sent once the first has held eight PDUs. The engine sees a PDU on its transmitted-PDU feed, the one the hold and MEDIA_RESET count, so a request between that first PDU's launch and its report still merges. `tkdiag` T17 grades the merge in both parts, one toggle and one MEDIA_RESET per stream; T18 grades the new restart after the first PDU, two of each |
->>>>>>> c266432dc (Merge PR #555: Make a PHC step one counted media event: toggle mr, count MEDIA_RESET, re-base once, and merge a pending restart)
 | Licensed streams | Keep streaming (REQ-PTP-08) | Yes: `tu` gates no emission |
 
 The render stage is timed from accept, not presentation time.
@@ -241,14 +231,10 @@ Legacy writes remain acknowledged and ineffective.
 | `gptp_shadow` | Atomic state and immediate discontinuity |
 | `clkvalid` | Holdover, steps, and option-off values |
 | `milan_dp` | Public CSR and protocol consumers |
-<<<<<<< 0c61d4589 (Shorten the CRF clock-bound citation sentences)
-| `milan_dp` gmstep | One 1.5 s grandmaster step under CRF selection: `tu`, the render re-base and law, `mr`, MEDIA_RESET, stream continuity (not yet in the sweep) |
+| `milan_dp` gmstep | One 1.5 s grandmaster step under CRF selection: `tu`, the render re-base and law, `mr`, MEDIA_RESET, stream continuity; three negative controls in the sweep |
 | `crf_rx` talker_step | Connected receiver and servo: +/-150 us talker-only steps and steps at both ends. The 600 ms listener lag and talker-only cases require a boundary inside crossing history; the 100 ms lag checks guard interaction. Sampled validity, continuous LOCKED state, held integrator and fresh rate recovery; quiet traffic cannot satisfy withholding |
 | `crf_rx` discontinuity | Both tu edges, unmarked steps, refill boundaries and isolated detector mutants |
-=======
-| `milan_dp` gmstep | One 1.5 s grandmaster step under CRF selection: `tu`, the render re-base and law, `mr`, MEDIA_RESET, stream continuity; three negative controls in the sweep |
 | `tkdiag` | A restart request on a pending one merges: one toggle, never a cancellation (T17). Pending ends at the first PDU at the adopted level (T18) |
->>>>>>> c266432dc (Merge PR #555: Make a PHC step one counted media event: toggle mr, count MEDIA_RESET, re-base once, and merge a pending restart)
 | `media_grid_align` | Alignment, watchdog, and recovery |
 | `tsn_fuzz` | Storms, malformed pairs, drought recovery |
 
```

## Handoff state

Assigned round-4 items 1-3 are complete. All required command exits are zero.
`git status --short` and `git diff --name-only HEAD` are empty after validation.
The final public handoff text is [REVIEW-READY.md](REVIEW-READY.md).
Publication of the local merge head and the independent merge-delta review remain pending.

[PR-BODY.md](PR-BODY.md) contains the full current PR description retrieved with
`gh pr view 554 --json body`, updated for this round. It is a local replacement
body for publication; the live PR was not edited.

The assignment calls for one independent merge-delta review by [R302].
The external round-3 positive at the ancestor remains as recorded in the
assignment. This handoff supplies author evidence and does not issue a review
verdict or a reviewer-owned coverage ledger.
