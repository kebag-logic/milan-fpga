# [A256] HANDOFF: kebag-logic/milan-fpga #387, acceptance 3 (the datapath half)

Author lane A256. Assignment: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5814963103
Ruling implemented: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260 (items 1 and 2).
REVIEW READY posted: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816940740

| Item | Value |
|---|---|
| Branch | `387-media-rebase`, worktree `$LANES/387-media-rebase`. Local only: not pushed, no PR opened |
| Base | dev `59b816708852472da6ed4576386c30ebd5f8f839` |
| Head | `00d388d832189a93335935de7726b5e07dd6f0dc`, tree `6e279c35017d72528d1ea527aa83bee4efbee25a` |
| Commits | four one-line commits, no body, no trailers (below) |
| Working tree | clean (`receipts/final/status-final.txt` is empty) |
| Verdict of this lane | Acceptance 3 met digitally: gmstep 48/48 in the default sweep with its controls; the pending-restart merge implemented and graded. Acceptance 4 stays the manager's #117 bench step |

| Commit | Subject |
|---|---|
| `29036eb4` | Merge a restart request into one pending on the same stream in KL_media_clock_restart, graded by tkdiag T17 and its mutation arm |
| `f7948582` | Make a PHC step one counted media event: it toggles mr whatever the clock source, and the render stage re-centres on it alone |
| `f0e00c22` | Join the gmstep leg and its three acceptance controls to the milan_dp sweep, with the whole inventory as gmstep-mutants |
| `00d388d8` | Record the one-event media re-base and the pending-restart merge in the design pages, register map, test index and changelog |

Simulation evidence ran at `1dc93828` (the previous spelling of the docs commit). `git diff 1dc93828 00d388d8` is two table cells of `docs/design/GM_LOSS_RECOVERY.md` (the measured offsets widened to their 42-delay range). Every static gate, the docs gates and Yosys ran at `00d388d8`.

## Change list (file:line at the head)

### RTL

| Where | Change | Why |
|---|---|---|
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv:179` | `tgt_r` is per talker (`[N_TALKERS_P-1:0]`), not one engine-wide bit | whether a request is pending is a property of one stream's hold, so a shared target cannot both merge on one stream and restart on another |
| `KL_media_clock_restart.sv:205` | a request sets `tgt_r <= ~mr_o` instead of `tgt_r <= ~tgt_r` | a request asks for the complement of the level the stream stamps; a second request while one is pending (`tgt_r != mr_o`) asks for the same thing, so it merges and can never cancel (ruling item 2) |
| `KL_media_clock_restart.sv:217,220-221` | the adopt and track paths index `tgt_r[t]` | follows the vector |
| `KL_media_clock_restart.sv:55-83`, `:124-128`, `:141-145`, `:115` | banner "A PENDING RESTART ABSORBS A SECOND REQUEST", the summary line, the `restart_p_i` port doc | records the merge, the per-stream target, and that streams may end on opposite levels (10.4.3: only the mr of the stream a Listener recovers from is valid) |
| `hdl/milan/milan_datapath.sv:3110` | `wire media_rebase_p_w = eff_ptp_adjust_w \| cfg_ptp_cmd_load;` | the PHC step: the plane's `phc_step_we_o` (CLKV software adjtime when the plane is off) or a software settime. A214's patch |
| `milan_datapath.sv:3111-3113` | `mcr_restart_p_w` = the CRF-gated triggers OR `media_rebase_p_w`, ungated | decision 5606198212 part b / 5794731090: every step is one `mr` toggle and one MEDIA_RESET, whatever the clock source. A214's patch |
| `milan_datapath.sv:6026-6028` | `render_recentre_p_w = media_rebase_p_w \| src_recentre_p_r`, on two lines | the identity trigger `gm_recentre_p_r` is gone from the render stage (one counted event, not two). The second line keeps the `       \| src_recentre_p_r;` anchor that `render_mutants.py` and `tdm8_render_mutants.py` plant their clock-source control on |
| `milan_datapath.sv:3071-3074`, `:3099-3109`, `:3118-3124`, `:5937-5940`, `:6017-6025` | comments | the CRF gate no longer covers every request; the "one TARGET, never opposite levels" note becomes "one engine, every request reaches every stream, pending is per stream"; `gm_recentre_p_r` now feeds only `KL_i2s_playback` |
| `hdl/ieee1722/crf/KL_crf_tx.sv:54-59`, `:150-152` | comments only | the same "never on opposite levels" note, corrected |

### Tests

| Where | Change |
|---|---|
| `tb/verilator/tkdiag/sim_main.cpp:641-704`, `:732` | new T17 (7 checks), run last: two talkers whose holds disagree; a disruption stamps at once on one and is pending on the other; a step on top. The pending talker puts exactly one toggle on the wire (never none) and its MEDIA_RESET counts one; the other gets its second toggle after its own hold and counts two |
| `tkdiag/sim_main.cpp:145-161`, `:100-103` | helpers `restart_request()`, `send_at_level()` (the harness plays the packetizer: each PDU carries the level the engine grants), and their wire tally; T15's comment (`:504-506`) corrected |
| `tb/verilator/tkdiag/Makefile:20-39` | `MCR_SRC` and `TKDIAG_MDIR` overridable; `build` split out; `run` runs the harness then `mcr_mutants.py` |
| `tb/verilator/tkdiag/mcr_mutants.py` (new) | two engine mutants, each must fail its named T17 check; crflic_mutants.py idiom (suite_tally verdict, no host deadline, SIGTERM cleanup) |
| `tb/verilator/milan_dp/sim_main.cpp:113`, `:560`, `:1034`, `:973-979` | `phc_steps_issued` counts the PHC steps the harness commands; "ownerless frame keeps tv=1" grades every header bit of that byte but `mr` (`& 0xF7`), and a new check grades `mr` against the parity of the steps issued. See "Existing check changed" below |
| `tb/verilator/milan_dp/sim_nxn.cpp:3104-3109` | the `[CTRS-OUT]` q2 injection flips every context's target (the target is a vector now) |
| `tb/verilator/milan_dp/gmstep_mutants.py` (new) | nine controls; the default run plants the three the acceptance names, `--all` plants nine; prints every check each control broke |
| `tb/verilator/milan_dp/Makefile:429`, `:525-526`, `:334-335`, `:14-17`, `:310-319`, `:197` | `run` depends on `gmstep` and ends with `python3 gmstep_mutants.py`; new explicit `gmstep-mutants` target; header and gmstep comment |
| `tb/verilator/milan_dp/sim_gmstep.cpp:14-19` | banner: the pending-restart arm is tkdiag T17 (comment only; the 48 checks are unchanged) |
| `scripts/measure_test_evidence.py:610-613`, `:641-643` | DUT-reader dispositions for the two runners |

### Docs

| Where | Change |
|---|---|
| `docs/design/GM_LOSS_RECOVERY.md:151,155-157` | render, `mr`, MEDIA_RESET and pending-merge rows "Not yet" -> "Yes" with the gmstep and T17 evidence |
| `GM_LOSS_RECOVERY.md:164-170`, `:187`, `:190-198`, `:224-225` | "counts two re-bases" -> one; pending restart graded by T17; the sweep controls; verification rows |
| `docs/design/TIME_SYNC.md:195` | render table "Recentre" row: the step and settime, no identity trigger; the step is also one `mr` toggle |
| `docs/reference/REGISTER_MAP.md:124-131` | the CRF selection gates only the CRF `mr` triggers; a step toggles `mr` on every running Stream Output, counted by its MEDIA_RESET |
| `docs/testing/TESTING.md:267`, `:501` | explicit-campaign row for `gmstep-mutants`; tkdiag row names T17 and `mcr_mutants.py` |
| `tb/verilator/milan_dp/README.md:4`, `:29`, `:42`, `:470-497`, `:504`, `:513`, `:742-752` | thirteen elaborations; `obj_gmstep` row; the sweep paragraph and control table; the pending-restart bullet; timing; check-count rows (231/231/228, gmstep 48) |
| `CHANGELOG.md:11`, `:30-49` | "Unreleased - one media event per PHC step" |

Deliberately NOT touched: the grid-aligner and CRF-servo rows of `GM_LOSS_RECOVERY.md` and the matching README bullets. Owner decision 5810378282 puts the aligner row in #539's PR, and open PR #547 (#539) rewrites exactly those rows. The aligner decision is unchanged.

## Decisions and interpretations (published in the PR body)

1. **"Pending" means requested and not yet stamped.** A request is pending on a stream while the stream's previous toggle has not held its eight PDUs. A request that lands after the stream stamped the earlier one is a new restart: its toggle follows once the earlier toggle has held eight PDUs (T12 already grades this). Merging it too would swallow a restart the stream's listeners have not been told about.
2. **The target became per stream.** With one shared target, a request can be pending on the CRF output (8 PDUs at 500/s) while already stamped on an AAF talker (8 PDUs at 8000/s); a shared target cannot merge the first and restart the second. T17's second mutant (a shared target that merges whenever any stream is pending) shows the cost: the AAF talker loses the step's toggle. Consequence: two streams can end on opposite `mr` levels; the old "two outputs never on opposite levels" comment is removed in three places.
3. **The step's toggle is not gated by clock-source selection** (A214's patch; decision part b and 5794731090 say every step). The CRF disruption and echo stay gated.
4. **What counts as a step**: `eff_ptp_adjust_w | cfg_ptp_cmd_load`, the same set that already raised `tu` and re-centred the render stage: the plane's step (CLKV software adjtime when the plane is off) and a software settime.
5. **`KL_i2s_playback` (Arty I2S element) still re-centres on the GM identity** (A214 open item 4): the decision names the render stage and the aligner only. On the AX shape `gm_recentre_p_r` now has no reader and synthesis drops it.
6. **The pending-restart arm is in tkdiag, not gmstep.** gmstep stays at the 48 checks the acceptance names; its scenario has no restart pending at the step. T17 drives the restart engine and the MEDIA_RESET counter PDU by PDU on one chain.

## Existing check changed (Tests lens, flagged for the reviewer)

`sim_main.cpp` "CLKV: ownerless frame keeps tv=1" compared the whole AVTP byte 1 to `0x81`, so it also asserted `mr = 0`. The leg's section 7 issues one CLKV adjtime (plane off) before that check; under the decision that is a PHC step, and the byte read `0x89` (first sweep run, `receipts/wip/sweep.log`, legs obj_dir, obj_nolpf, obj_ax1x1, one failure each). The check now masks only `mr` and still grades sv, version, gv and tv; a new check grades `mr` against the parity of the PHC steps the harness itself commanded (`phc_steps_issued`), not against a DUT read. Counts: obj_dir and obj_nolpf 230 -> 231, obj_ax1x1 227 -> 228.

## Tests (at `1dc93828`, Verilator 5.050 pinned build, 8 jobs)

| Leg | Result | Receipt |
|---|---|---|
| gmstep on dev `59b81670` (before) | 44/48, the four decided-behaviour failures (2 re-bases, 0 `mr` toggles, 0 MEDIA_RESET) | `receipts/gmstep-dev-base.log` |
| gmstep at head, feed delay 0 (in the sweep) | **48/48**; one re-base at step pulse +132 cycles; one `mr` toggle at +116 | `receipts/final/sweep.log` [12/47] |
| gmstep at head, feed delays 0..41 | **48/48 at all 42**; fill after push 14 at all; fill at accept 9 (35), 10 (6), 9..10 (1); re-base +132 at all; toggle +75..+116 | `receipts/final/feed-delay/` |
| tkdiag (T1-T17) | **90/90**; then `mcr_mutants.py` 3/3 (clean + 2 mutants) | `receipts/final/tkdiag.log` |
| tkdiag against the dev `KL_media_clock_restart.sv` | 88/90: fails exactly "T17 talker 1 puts exactly ONE toggle on the wire, never none" (got 0) and "T17 ... and talker 1's MEDIA_RESET counts that one" (got 0) | `receipts/final/tkdiag-dev-engine.log` |
| `make -C tb/verilator/milan_dp` (`run`, from `make clean`) | **all 47 recipe commands rc 0**; 9775 checks, 0 failures by `suite_tally.scan`; `log_reports_failure`: none | `receipts/final/sweep.log`, `sweep-state.txt`, `run-recipe.txt` |
| of which: gptp, gptp-lat | 181/181 each | |
| of which: obj_dir, obj_nolpf, obj_ax1x1 | 231/0, 231/0, 228/0 | |
| of which: notify, crflic, nxn, nxndv, nxn8, nxn4c, prune, aclk | 146/0, 85/0, 1708/0, 1710/0, 3136/0, 1708/0, 33/0, 139/0 | |
| of which: `render_mutants.py` | 6/6 (its "clock-source trigger dropped" control still plants on the two-line trigger) | |
| of which: `gmstep_mutants.py` (sweep subset) | 4/4 (clean + 3), 146.9 s | |
| `make gmstep-mutants` (all nine) | 10/10 (clean + 9), 372 s | `receipts/final/gmstep-mutants-all.log` |

The full `run` recipe is longer than this session's 10-minute foreground limit, so it was executed as its own `make -n run` listing (`run-recipe.txt`, 47 commands after `make clean`), command by command in order, in five chunks, each command's exit code recorded (`sweep-state.txt`). Nothing was skipped or reordered.

## Mutants (each must fail a named check by the harness's own verdict)

| Control | Planted in | Named check | Every check it broke | Runs in |
|---|---|---|---|---|
| the step does not toggle `mr` | datapath | restart: the outgoing mr toggles exactly once | + the talker's MEDIA_RESET counts exactly one | sweep |
| the identity re-bases the render stage as well as the step (double re-base) | datapath | render: the GM change is one counted re-base event | + every counted re-base lands at a PDU end right after the step | sweep |
| the step does not re-centre the render stage (ruling item 1) | datapath | render: the GM change is one counted re-base event | that one | sweep |
| a request flips the target, cancelling a pending restart (the dev engine's rule) | `KL_media_clock_restart` | T17 talker 1 puts exactly ONE toggle on the wire, never none | + T17 ... and talker 1's MEDIA_RESET counts that one | tkdiag default target |
| one shared target that merges while any stream is pending | `KL_media_clock_restart` | T17 talker 0 had stamped the disruption: the step is its 2nd toggle | + T17 ... and talker 0's MEDIA_RESET counts both | tkdiag default target |
| the render re-base keyed to the identity, not the step | datapath | render: every counted re-base lands at a PDU end right after the step | that one | gmstep-mutants |
| `tu` reaches the talkers four cycles late | clock validity | tu: set in the first cycle the bank names GM B | that one | gmstep-mutants |
| the plane's step does not re-arm the holdover | datapath | tu: held at least the 0.25 s holdover after the step | that one | gmstep-mutants |
| `tu` stops the talker | datapath | licence: the talker never pauses beyond four of its intervals | 5 (tu graded inside hold, pause, rate, toggle window, MEDIA_RESET) | gmstep-mutants |
| the GM change stops the talker for good | datapath | licence: the talker never pauses beyond four of its intervals | 6 (both tu grading counts, pause, rate, toggle, MEDIA_RESET) | gmstep-mutants |
| the step's re-centre snaps one event off | render stage | render: every PDU push leaves the target fill across the event | that one | gmstep-mutants |

## Gates (all rc 0; each run to its own log, never piped)

| Gate | Head | Result | Receipt |
|---|---|---|---|
| milan_dp `run` sweep | `1dc93828` | 47/47 commands rc 0, 9775 checks 0 failures | `final/sweep.log` |
| tkdiag (touched suite) | `1dc93828` | 90/90, mutants 3/3 | `final/tkdiag.log` |
| `python3 scripts/docs_check.py` | `00d388d8` | 0 findings (git ls-files) | `final/gate-docs_check.log` |
| same, no git (`git archive` extract), plus `check_feature_status.py` | `00d388d8` | 0 findings; 0 findings | `final/gate-*-nogit.log` |
| `check_em_dash.py --base 59b81670...` | `00d388d8` | 0 findings over 89 added lines in 6 pages | `final/gate-em_dash.log` |
| `check_doc_style.py` | `00d388d8` | OK (22 documents) | |
| `gen_toc.py --check` | `00d388d8` | OK | |
| `check_doc_paths.py` | `00d388d8` | OK (841 paths) | |
| `check_gptp_docs.py` (+ `--with-submodule`) | `00d388d8` | OK, OK | |
| `xvlog_gate.py --check` (Vivado found; 120 files analysed) | `00d388d8` | PASS, 4 findings == ratchet, 0 under `hdl/` | `final/gate-xvlog_gate.log` |
| `check_rtl_source_lists.py` | `00d388d8` | OK | |
| `check_cpp_idiom.py`, `check_py_idiom.py` | `00d388d8` | OK, every ratchet unchanged | |
| `lint_rtl.py --check` | `00d388d8` | PASS, 90 <= 90 | |
| `measure_test_evidence.py --check` | `00d388d8` | PASS; unarmed suites 74 -> 73 (tkdiag now armed; budget 77 not lowered) | |
| `git diff --check 59b81670 HEAD` | `00d388d8` | clean | |
| Yosys `--top KL_crf_tx`; `--top milan_datapath` elaborate and full | `00d388d8` | PASS 2726 cells; PASS; PASS 1,632,236 cells, tied-input and tap-purity PASS | `final/yosys-*.log` |

## Not run, and why

- The other 52 Yosys tops: none reads an edited file (`run.sh --emit` over all 54).
- The hosted CI, `act_ci.py`, and `scripts/run_all_suites.sh` as a whole: out of this lane (no push; the 10-minute foreground limit).
- `milan_dp_gptp` (physical 50 MHz leg) and the `milan_dp_render` suite: not touched and their sources do not read the edited restart engine differently; not run.
- Hardware: not allowed.

## Open risks and questions

1. **Sweep wall clock.** This change adds about 182 s of the 1367 s measured here (gmstep build 11.6 s, leg 23.6 s, three controls 146.9 s). At the documented 1.58x hosted slowdown that is about 290 s on top of the #444 hosted worst case of about 1815 s, against the 2700 s budget: roughly 595 s of margin left instead of 885 s. The deadline is not raised; the other six controls are the explicit `gmstep-mutants` target. The `run_all_suites.sh` margin comment is a hosted measurement and is not edited here.
2. **Lane conflict with PR #547 (#539).** It rewrites the aligner and CRF-servo rows adjacent to the rows this change turns to "Yes", and the README bullet next to the pending-restart bullet. Whichever lands second resolves a textual conflict; the contents do not overlap.
3. **Per-stream target** (decision 2 above) replaces a documented design note. The reviewer should confirm the reading of ruling item 2 that it rests on.
4. The `gmstep` scenario never has a restart pending at the step; the merge is graded on the engine (T17), and the datapath wiring of the step into `restart_p_i` by gmstep. No datapath-level leg drives a CRF disruption and a step inside one hold.

## Acceptance (issue #387)

| # | State |
|---|---|
| 1 | Met before this lane |
| 2 | Met (PR #540); the rows this lane owned are now "Yes" |
| 3 | **Met digitally**: gmstep 48/48 in the default sweep with its controls; ruling item 1's negative control (no step re-centre) fails the one-counted-event check; ruling item 2's merge in the engine, T17 and two mutants |
| 4 | The manager's #117 bench step after merge |
| 5 | Verilator and Yosys gates above; no ROM changes in this lane |

## Packet

- `PR-BODY.md`: proposed PR text ("[A256]", "Closes #387").
- `receipts/final/`: every log at the heads named above; `receipts/gmstep-dev-base.log`: the dev leg; `receipts/wip/`: the first sweep (with the three `sim_main` failures that led to the check change) and earlier intermediate runs.
- `MANIFEST.sha256`.
