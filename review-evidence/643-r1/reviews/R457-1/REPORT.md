[R457] NEGATIVE - exact head 98729742b71d5088f250440eb46085daf1c0cbdb

# R457-1: external review of #643 / PR #648

- **Head under review:** `98729742b71d5088f250440eb46085daf1c0cbdb`, tree `174b326e6fcf29ff695a9376ab84ef3c045e4440`. Base is dev `5fabb46e767c9308ab2580916237f43577698c6e`. Processor pin `631eeb34`.
- **Round:** R457-1, external, cleared context. It ran from the [review start](https://github.com/kebag-logic/milan-fpga/pull/648#issuecomment-5974449769).
- **Context reconstructed from:**
  - `AGENTS.md`;
  - #643's body, the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5972861856), the [item 1 STOP](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973437153), the [ruling 5973450039](https://github.com/kebag-logic/milan-fpga/issues/643#issuecomment-5973450039) and REVIEW READY;
  - the PR #648 body;
  - `docs/design/TIME_SYNC.md` "Listener render latency" and `docs/design/MEDIA_CLOCK_FOLLOWING.md` "Simulation";
  - `hdl/ieee1722/aaf/KL_render_setpoint.sv` and the `milan_datapath.sv` aligner, settle and render-stage instances;
  - the diff `5fabb46e..98729742` and its two commits;
  - the public evidence tree `review-evidence/643-r1` at `531abe2b`.

## Verdict in one paragraph

The test-only fix does what the ruling asked, at its 18 standing phases and with both processors. I reproduced the following independently:

- The default target is rc 0 at both processors: 226/0, 65/0 and leg defects 5/5.
- The A2-a planted defect fails all 18 per-phase settled checks plus the ceiling check, at both processors.
- The harness's PDU-end instant matches the render stage's own `pdu_end_w` on every cycle.

The verdict is NEGATIVE because of F1, the stated tie rule. Its premise is "one cycle of feed jitter", and the measurements below contradict it:

- At a measured tie phase the pop moves 3 to 4 cycles against the PDU end.
- So the sound design FAILS the graded law at +2,025 in 4 of 5 trials, depending on the run's history.
- A planted one-event setpoint defect PASSES the fill and band checks at +2,025 and +2,026, while it fails all 18 standing phases.

The tie rule is inert at the standing phases (0 ties there; no pop lands within 8 cycles of any graded PDU end). So the shipped suite is green for the right reason today. But the rule, and the docs and PR body that state it, do not hold at a tie. F2 is a stale measured-result sentence in `TIME_SYNC.md`.

## Findings

### F1: MINOR. Lenses: Conformance, Tests, Robustness, Docs. The tie rule's one-cycle premise is false at a real tie: a sound design fails and a setpoint defect passes

- **Where:**
  - `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:664`: the tie window is `after == 1 || after == 2`.
  - `:3077-3083`: the rule's statement.
  - `:3110-3113`: `tie_ok`.
  - `:177`: the 64-cycle slack.
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1366-1370`: "One cycle of feed jitter moves a pop across that boundary ... toward its side only".
  - `tb/verilator/README.md:63`: "a pop within one cycle of the PDU's last beat".
  - The PR #648 body, Known limitations: "A one-cycle scan from +2,010 to +2,045 found ties at +2,025 and +2,026 only; at +2,026, 11 of 124 PDUs read 15 and pass only by the rule".
- **Authority:**
  - The ruling accepted "the tie rule for a pop coinciding with the PDU end within one cycle of feed jitter".
  - This round's focus requires that the tie rule cannot mask a real defect.
  - `AGENTS.md` section 6 Tests: "Each new test can fail for the defect it claims to detect". Robustness: boundary values.
- **Evidence:** all runs use the head harness. The probe adds `public_flat_rd` to three `KL_render_setpoint` nets, with no logic change, and reads `LAW_PHASES`. With the standard phases, its `[LAW]` lines are byte-identical to the unmodified clean `--law-only` binary's (`receipts/probe-std.log` against `receipts/law-head-clean.leg.log`).
  - **The pop spread at a tie is 3 to 4 cycles, not 1.** `receipts/probe-tiehist.log` histograms, per graded PDU, the pop pulse's offset from the end beat. At +2,023 the offsets are +3..+6; at +2,025, +1..+3 and +2..+4; at +2,028, -1..+1.
  - **The sound design fails at +2,025.** A pulse at +3 is a pop taken 2 cycles after the end. It reads 15 with `tie_pop = 0`, so the fill check fails:

    | Run | PDUs failing | Where |
    |---|---|---|
    | `tiehist` | 17 of 124 | second +2,025 |
    | `tiehist` | 30 of 124 | third +2,025 |
    | `tiealone` | 54 of 124 | +2,025 run alone |
    | `tie` | 30 of 124 | +2,025, first probe build |

    The first +2,025 in `tiehist` passed, because its snap landed on the other side. The verdict at a tie phase therefore depends on the run's history: this is the pass-or-fail-with-phase defect #643 exists to remove, moved to a narrower window.
  - **A real defect is masked at a tie.** `receipts/probe-sp-std.log` runs `RENDER_ALLOW_EVT_C = 1` (setpoint 7, target 13; `scripts/probe-setpoint-minus-one.patch`).
    - It fails fill and band at all 18 standing phases: 36 failures, fill 13, delays 7.035..7.974 ticks.
    - At +2,025 it passes both checks: fill 13..14, 121 PDUs under the rule, delay 8.001 ticks.
    - At +2,026 it passes both checks: fill 13..14, 124 PDUs under the rule, delay 8.001 ticks.
    - At a tie the band cannot separate setpoint 7 (8.001 ticks, inside only by the pulse register) from setpoint 8 (9.001 ticks, inside only by the slack). The tie rule then admits both fills.
  - **The PR body's tie-scan statement does not reproduce.** Ties (`tie_pop != 0`) appear at +2,024..+2,028 (`receipts/probe-tie.log`, `probe-tiehist.log`), not only at +2,025 and +2,026, and +2,025 fails as above.
  - **The standing sweep is unaffected today.** In `receipts/probe-stdhist.log`, every graded PDU at all 18 standing phases has no stream-0 pop within -6..+8 cycles of its end, and reads fill 14. The nearest pop is about 56 cycles from a tie: delays 8.035..8.973 ticks, matching the suite logs.
- **Impact:**
  - The documented rule claims a property it lacks. "Toward its side only" and "one cycle of feed jitter" are false at a tie.
  - A standing phase is about 56 cycles from a tie. A change in the RX-to-end latency of that order puts it on one. The suite would then either go red on a sound design, depending on history, or pass a design one event off the setpoint at that phase.
  - Neither is visible from the suite's output today, because the rule never fires.
- **Required outcome:** no graded phase may pass a design whose fill is one event off the setpoint, and none may fail the sound design, because a pop lies within the measured jitter of the PDU end. Either form satisfies this:
  - the rule covers the measured spread and a tie phase is part of the standing proof; or
  - a graded phase that sees a pop inside a stated window of its PDU ends fails as not gradable instead of applying a rule.

  In both cases the suite comment, `MEDIA_CLOCK_FOLLOWING.md`, the suite README row and the PR body must state the measured spread, not one cycle, and the tie-scan evidence must be corrected. If changing the accepted rule needs a ruling, publish that conflict.
- **Verification:** rerun `scripts/reproduce.sh` step 5:
  - `probe-tiehist` and `probe-tiealone`: no history-dependent failure at +2,025 of the sound design, or a loud "not gradable" verdict;
  - `probe-sp-std`: setpoint 7 not passing at any graded phase;
  - `probe-stdhist`: the standing sweep unchanged.

### F2: MINOR. Lens: Docs. `TIME_SYNC.md` still reports a measurement the suite no longer takes

- **Where:** `docs/design/TIME_SYNC.md:451`: "The fill at accept stays the setpoint. Every first event stays inside the law band." This sits in the passage that reports T30's live CRF selection measurements.
- **Authority:**
  - This PR moves the T30 CRF LAW to the PDU-end instrument (`sim_tdm8_render.cpp:3084-3136`, called at `:3226-3228`). The executor lists it as an interpretation to confirm, and I confirm the move.
  - The executor's own item 1 data shows that a fill read at accept depends on the feed's phase (mechanism 3).
  - `AGENTS.md` section 6 Docs: "Changed contracts are reflected in authoritative docs".
- **Impact:** an authoritative page states, as measured evidence, a reading that no suite takes any longer and that is not phase-invariant. It is a measurement claim, so it is not RESIDUE.
- **Required outcome:** the sentence states what T30 CRF now grades. For example: "At every PDU end the fill stays the setpoint plus that PDU (14 events). Every first event stays inside the law band from its PDU end." Alternatively, cite the grading instant in `MEDIA_CLOCK_FOLLOWING.md`.
- **Verification:** read `TIME_SYNC.md` at the corrected head against `prove_the_setpoint_law_still_holds`, and run the docs gates.

### S1: SUGGESTION. Lens: Tests. Grade the exact PDU count per phase

`sim_tdm8_render.cpp:3128` keeps `n >= 100`. `[LAW]` knows each phase grades exactly 124 PDUs: 144 sent, 16 prefill and 4 trailing. So up to 24 PDUs per phase could drop out of grading silently, and stating 124 costs nothing.

### S2: SUGGESTION. Lenses: Tests, Docs. The A2-a arm proves the settle gate, not the law grading

In `receipts/law-head-a2a.leg.log` and `law-c4-a2a.leg.log`, the 19 failures are the ceiling check plus 18 "held its settled report" checks. Every per-phase fill and band check still passes with A2-a removed, because each phase anchors its feed on an observed media tick. That is what the ruling specified, and the docs row says "fail their settled check", which is accurate. A future reader should not take it as evidence that the law checks see misalignment.

### S3: SUGGESTION. Lens: Tests. The same accept-pulse instrument remains in `milan_dp`

This is new work, for a new Issue. `tb/verilator/milan_dp/render_mutants.py:100` and `test_render_phase_observation.py:79-85` name checks "fill at accept = setpoint". #643's mechanism 3 shows that reading depends on the feed's phase. This is not in #643's scope.

## Lens coverage at this head

| Lens | Result | Artifacts examined at `98729742` |
|---|---|---|
| Conformance | UNCLEAN (F1) | Every acceptance item checked against #643 items 1 to 3 and ruling 5973450039, with the results below. F1 is open because at a tie phase the graded law admits a design one event short of the declared setpoint. |
| RTL | CLEAN | Diff under `hdl/` and every submodule: 0 lines. The harness taps are already public: `lb_tap_*`, `rsp_fill_w`, `rsp_pop_p_w`, `mga_engaged_w`, `mga_err_w`, `media_tick_p`, `int_clk_selected_r`. `lb_tap_tvalid_w = dpkt tvalid && tready` under `-GLOOPBACK_P=1` (`milan_datapath.sv:6142-6146`, suite Makefile `:95`) is the same accepted beat as the stage's `s_tvalid_i` (`:6472`), so the harness end equals `pdu_end_w = s_ok_w && s_tlast_i` (`KL_render_setpoint.sv:305`, `:534`). Probe: 0 instant mismatches over 18 x 144 + 15 x 144 PDU ends. The fill read one cycle later equals `fill_end_w` except at the snap PDU (id 2, 18 -> 14, ungraded). `kSettleErrCycles` 32 equals `SRC_SETTLE_ERR_C` at 100 MHz (`:6264`); 2,048 and 32,768 equal `:6265-6266`. |
| Robustness | UNCLEAN (F1) | Ceiling failure: A2-a waits 32,768 ticks and fails. Stopped-grid guards: `:3268-3272` and `:3300-3303`, plus the phase's tick floor `:3323-3324`. The hold check catches a moving grid (`probe-nodwell`: report met at the boot crossing after 4,366 ticks, then 14 phases fail holding). The tie boundary is F1. |
| Tests | UNCLEAN (F1) | The planted arm is caught 18/18 plus the ceiling at both processors, through the campaign's own `plant/build/run_leg/verdict` (`scripts/law_arm.py`). The tuple verdict refuses 17/18, 1/18 and an rc-0 mask, and `LAW_PHASES == kLawPhases` (`receipts/verdict-tuple-test.log`). The `--law-only` control passes at both. Setpoint-7 probe: F1. S1 and S2 are suggestions. |
| Docs | UNCLEAN (F1, F2) | The `MEDIA_CLOCK_FOLLOWING.md:1329` row and `:1355-1384` (instant, tie rule, #647, boot pull-in: the boot claim confirmed by `probe-nodwell`); `TESTING.md:285-287`, `:521`, `:523`; `tb/verilator/README.md:63`; Makefile `:33-38`; `TIME_SYNC.md:451` (F2). Docs gates rc 0 (`receipts/docs-gates.log`): `docs_check`, `check_em_dash --base 5fabb46e` (0 findings over 38 added lines), `check_doc_style`, `check_doc_paths`, `gen_toc --check` and `--verify-anchors`. |

The RTL clean result, in findings format:

```text
[R457] PASS RTL - hdl/ (0-line diff 5fabb46e..98729742), milan_datapath.sv:6142-6146/:6472, KL_render_setpoint.sv:533-534, probe receipts/probe-stdhist.log + probe-tiehist.log - the harness's PDU-end beat and fill read are the stage's own pdu_end_w and fill_end_w on every cycle; no RTL or submodule gitlink changed; the settle constants match SRC_SETTLE_*_C at 100 MHz
```

## The focus items, verified

| Item | Result | Evidence |
|---|---|---|
| `[LAW]` waits for the settled report (engaged, \|err\| <= 32, 2,048 ticks) within 32,768 ticks, and fails without it | Yes | `:3256-3283`. Full leg waits 0 ticks (8,626 running). `--law-only` waits 4,014 (head) and 4,013 (c4). A2-a: waits 32,768 and fails the ceiling check. |
| 18 phases (16 over one tick plus +927 and +1,156), fresh streams at the INTERNAL grid cadence 52/391 | Yes | `:187-195`, `:3291-3325`. Each phase: 4-slot gap, tick anchor, 16 prefill PDUs and 124 graded; 888 to 889 ticks each. |
| Per phase: settled hold, fill 14 at every PDU end, first event in (8, 9] ticks plus 64 cycles | Yes | Both suites: every phase 124 PDUs, fill 14..14, 0 ties, 0 ticks outside the band. Delays 8.035..8.973 ticks at head; c4 within 1 to 2 cycles of head. |
| The grading instant is the beat `pdu_end_w` is made of | Yes | RTL row above; 0 mismatches. |
| The tie rule cannot mask a real defect | **No, per phase**; yes for the standing sweep today | F1. |
| The A2-a-removed mutant fails all 18 | Yes | 88 checks, 19 failures, at both processors. |
| T30 keeps its pin and A2-a checks | Yes | The diff removes only the INTERNAL `prove_the_setpoint_law_still_holds` call. `decode_and_grade_a_window`, `report_a_window` and `prove_the_aligned_window_is_the_acceptance_state(intr, crf)` are unchanged (`:3183-3241`). The T30 INTERNAL window logs as before. |
| The CRF law moved with the instrument without weakening | Yes, except at a tie (F1) | The fill check at the end is an exact pointer difference, so the reference's 28-to-48-cycle upper-band shift admits nothing the fill check would not reject. CRF window: 292 PDUs, fill 14..14, 0 ties at both processors. |
| Both processors | Yes | `631eeb34`: rc 0, 226/0, 65/0, 5/5, 687.4 s cold. `c4cb84ff` scratch parent (gitlink set, c8 `bbf704ec` then p2-p1 `1269cdaf` applied, never committed): rc 0, same counts, 710.1 s cold. |
| Wall time stated | Yes | Makefile `:33-38` and `TESTING.md:285-287`: 663.8 s against 560.0 s, 1,049 s at 1.58x. My 687.4 and 710.1 s ran on a host at load average about 40 to 47 from unrelated work: consistent, and 1,122 s at 1.58x, inside 1,800 s. |

## Prior public review findings

None: when this round started, the PR had no review and no findings, only the two start notices 5974449333 and 5974449769. Nothing is carried or resolved.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #643 items 1 to 3; ruling 5973450039; `sim_tdm8_render.cpp:3243-3325`, `:3084-3136`; suite and probe receipts | R457-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| RTL | CLEAN | `hdl/` 0-line diff; gitlinks; `milan_datapath.sv:5902-5932, 6142-6146, 6255-6311, 6472`; `KL_render_setpoint.sv:305, 454, 487-499, 533-534, 678-683`; instant probe | R457-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Robustness | UNCLEAN (F1) | Wait, ceiling and guards `:3256-3283`, `:3291-3325`; `probe-nodwell`; A2-a arm; tie probes | R457-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Tests | UNCLEAN (F1) | `tdm8_render_mutants.py` diff; `law_arm.py` at both processors; `verdict_tuple_test.py`; setpoint-7 probe; suites at both processors | R457-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |
| Docs | UNCLEAN (F1, F2) | `MEDIA_CLOCK_FOLLOWING.md:1329, 1355-1384`; `TIME_SYNC.md:361-451`; `TESTING.md:282-287, 518-523`; `tb/verilator/README.md:63`; Makefile header; PR body; docs gates | R457-1 | `98729742b71d5088f250440eb46085daf1c0cbdb` |

## Real limits

- **Not run:**
  - the full `tdm8render-mutants` campaign, and therefore the four pre-existing failing arms and the `make -C` campaign-form defect the executor reports;
  - Yosys;
  - any parent, PP, gPTP or builder bank;
  - act;
  - hardware.

  The A2-a arm and its control did run, through the campaign's own functions.
- **The c4cb84ff tree** carried the two adoption patches. I did not rerun the tie and setpoint-7 probes on it. F1 concerns harness logic, and the standing results at c4 match head within 1 to 2 cycles.
- **The tie probes are history-dependent by nature**, which is the finding. The exact failing counts depend on the phase sequence of each run, and each receipt states its sequence.
- **Probe build differences:** `probe-std`, `probe-tie`, `probe-nodwell` and `probe-sp-std` came from a first probe build, which had the identity counters only. `probe-stdhist`, `probe-tiehist` and `probe-tiealone` came from the final `scripts/probe-instrument.patch`, which adds the offset histogram and the mismatch id. The two builds' `[LAW]` lines are identical where they overlap. The "fill_end_w mismatch" probe check counts the snap PDU (id 2, ungraded, 18 -> 14) in every phase. It is a probe artefact, not a harness defect.
- **Redaction:** home-directory paths in `receipts/suite-*.log` are replaced by placeholders. Physical calibration was NOT RUN, and skipped field contexts are not hardware proof.
- **Hosted state:** `receipts/hosted-snapshot.tsv` is a read-only snapshot. Some Verilator shards, `elaborate` and `docs-check` were still in progress, and the physical gPTP context was skipped. The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report and its manifest.
- Carry F1 and F2 to the executor. F1's required outcome may need a ruling, because the ruling accepted the tie rule as stated.
- Re-review at the corrected head under Conformance, Robustness, Tests and Docs.
- Exact-head hosted `verilator-suites` and `yosys-portability`.
- The current-dev candidate build at the merge turn.
- S3 as a possible new Issue.

## Clone state after probes

All probes ran in copies under the scratch directory. The review clone is at `98729742`:

- worktree equals the index equals HEAD, with no untracked or ignored files;
- the index's (mode, blob, path) set hashes the same as `HEAD`'s tree (`547773827e03...`);
- gitlinks: protocol-processor `631eeb34`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`, external `efeb541a` (`receipts/clone-state.txt`).

Two `__pycache__` directories that my offline verdict test created were removed.

R457-1 FINISHED
