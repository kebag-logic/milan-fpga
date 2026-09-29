[A418] D3 lane 1: processor core and scalar records

Closes #131

Implements section 18.1 of the parent saved-state materialization contract (milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` at `7a7582f0`), with table 15.2, rulings DR1a-DR6 and the DR2c-carrier correction, in the assigned commit order:

1. `66267d9` The D3 writer (`KL_aecp_nvm_writer`, inside `KL_aecp_engine`) is manager 1 of the landed `KL_pp_nvm_mgr_arb`. It holds AECP dispatch from reset to its restore terminal (for ever in CLOSED) and takes the state bus only then and for a one-row latch in service. It proves the descriptor image first; an unprovable image ends CLOSED (cause 7).
2. `4dd37c2` Scalar records (configuration, sampling rates, clock sources, both stream formats, presentation offsets), one per row, F07.8 framed. The trigger is the dynamic-state store's accepted write that changes `{value, valid}` (DR2b), taken on the µCPU's side of the bus: restore writes and IDENTIFY never trigger, and completion marks select nothing. Group and index clear, taint, change wins the done edge, first-dirty debounce.
3. `5e1476d` Restore in two agreeing passes with the SET programs' value rules and the integrator's format judge; UNFRAMED is blank, DEVICE/torn/deadline/descriptor faults abort. Combined top verdicts; ADP sees `entity_enable_i && restore_done_o`.
4. `505524e` A pass-1 abort resets both AECP stores together, held while the descriptor guard owes a burst (the guard keeps the hard reset only), then re-proves the image: DEFAULTS or CLOSED. Restored bindings stay restored.
5. `f72a2d2` DR2c for both producers: three attempts per record, `NVM_RETRY_BACKOFF_CYC_P = ceil(CLK_HZ_P / 2)` (500 ms) between them with a fresh latch, reset-sticky alarm.
6. `39789f9`, `81c8a5f`, `e1ae468` All 37 rows of table 15.2 (docs, guides, diagrams 20/21/23/24 with PNG exports, RTL banners, suite READMEs, compliance review, `gen_ucode.py` comments with a byte-identical ROM) and the statement-by-statement contract sweep: 624 matching lines, 276 rewritten, every other one with a location-specific scope reason. Suite additions: the volatile set across a saved-set cycle, a device error on every read of a saved record, and a printed DR2a/DR3a measurement mode; the dyn_state suite's tracked shape tally is regenerated.

**Parent-visible changes (pin adoption)**
- New ports: `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`, `restore_cause_o[1:0]`, `d3_unflushed_o`. New parameter: `NVM_RETRY_BACKOFF_CYC_P`.
- `restore_done_o`/`busy`/`fail`/`blank` combine both walks (blank never with fail); `nvm_alarm_o` is either producer's; ADP takes the restore-released enable while the side-port lock keeps the requested one; AECP is held from reset to the D3 terminal; manager 1 now reads and writes records `0x00`, `0x02+`, `0x0A+`, `0x30+`, `0x40+`, `0x50+`.
- Parent glue: `pend_i = (|nvm_unflushed_o) | d3_unflushed_o` (`aecp_dyn_dirty_o` diagnostic only), `alarm_i` from `nvm_alarm_o`, combined restore status. Firmware must load and CRC-check the AEM before `PP_CTRL[1]`, or the restore ends CLOSED.

**Evidence**
- `tb/pp_top` section D3 on real AECP commands (86 checks: D3O ownership, D3S service, D3R restore/roll-back/CLOSED), `tb/acmp_nvm` E8-E11, `tb/dyn_state` H. Mutation campaign: 47 mutants covering every section 18.1 negative control (each scalar trigger and replay, uncleared store, ignored validity, group/index clear, taint and same-edge, restore writes as changes, DEVICE vs blank, roll-back and debt, early AECP/ADP release, quarantine released by time, backoff, fourth attempt, alarm forgiveness, IDENTIFY), each killed by its named assertion; goldens pass.
- DR3a (submitted for ratification, not ratified here): every measured path is far inside both candidates (healthy restores at most 2,661 cycles, 53 µs at 50 MHz; longest healthy single wait 853 cycles; silent device 2 x the per-wait deadline). The processor bounds each wait only; a device answering each wait just inside 20 ms could stretch the D3 walk over about 970 waits, so the 1,000 ms aggregate is a measured budget unless the manager rules an aggregate counter.
- DR2a (producer share): acceptance to window done = the 500 ms debounce + 28 cycles.
- DR4: 1x1 out-of-context synthesis +1,076 LUT / +614 FF / 0 BRAM / 0 DSP against the 2,500 / 1,400 scalar-core ceiling (lanes 1-2); 8x8 diagnostic +1,270 / +674. Post-place and firmware size are lane 2's; the 8x8 post-place obligation stays open and blocked.
- Gates at the head: every processor suite and entry point rc 0; parent xvlog, C++ and Python idiom gates rc 0; the parent evidence classifier reports exactly the single finding the base head already had (`tb/acmp_talker/retry_mutants.py`, from #129) and nothing from this lane's files.

Not in this lane: names and maps (lanes 3-4), parent glue and physical scalar/PTOF proof (lane 2), the full fault campaign (lane 5), #15 reusable service (DR1a), #20 (DR1b).

## Round 2

[A425], head `2b38d68`, addressing R390-1 and R391-1 in the assigned order, with the AECP hold-admission ruling (#131, 5873580386) and the DR3a/DR4 ratification (kebag-logic/milan-fpga#70, 5873060660):

1. `380a3e4` **DR3a aggregate, enforced.** The D3 writer counts from the accepted restore start (`restore_go_i`, `PP_CTRL[1]`) through the binding walk, both passes and the roll-back. At `NVM_RS_AGG_CYC_P` = `CLK_HZ_P` clocks (1,000 ms) it takes the per-wait deadline's path in the state it is in (cause 3; a READ in hand drained): CLOSED before the image is proven, DEFAULTS in pass 0, the roll-back in pass 1, CLOSED during it. One conversion and one rounding rule for every NVM time (R391-1 S1): ceil(`CLK_HZ_P` x t / 1000), so the per-wait default becomes ceil(`CLK_HZ_P` / 50). The bench now runs the top at a nominal 1,000,001 Hz with no NVM deadline override, so it times the top's own derivations. D3R13: a device granting every request 200 cycles inside the per-wait deadline ends DEFAULTS at exactly the 1,000,001st clock from the accepted start (pass 0), or rolls back within one deadline of it (pass 1).
2. `83e708a` **AECP hold admission.** While the writer holds AECP (reset to COMPLETE/DEFAULTS, for ever in CLOSED) at most one AECP record occupies the shared ingress; every further AECP frame is dropped at its slot gate and counted (snapshot word 37), unanswered. D3O5 (CLOSED, six AECP commands) and D3O6 (slowed restore, six queued): every GET_RX_STATE answered in the 168 cycles it takes with AECP idle; the held command answered at the release. The unbounded-gating mutant fails both. `integrator.md`, `07_memory_maps.md` and `03_packet_engine.md` rule (d) corrected; rule (e) states the boot-hold exception.
3. `b06130d` D3S10 on the derived 500,001-clock backoff (timing, and no ownership while it runs: a READ_DESCRIPTOR in it is answered before the retry); D3R4b blank-then-whole disagreement; the two-cycle roll-back strobe.
4. `85b2f6f` D3R5b pass-1 read drained and the later SET persisting; D3R8b a silent format judge ended by the per-wait deadline; D3R3b the rate walk to the eighth entry and refused past it (a ten-rate image).
5. `2fbe792` `tb/pp_top/d3_mutants.py` in the tree: 62 mutants (the 47 of round 1 and every round-2 control), each killed by its named checks from the tree; mutation records in the `pp_top`, `acmp_nvm` and `rx_validator` READMEs.
6. `2b38d68` `//!` contracts on the writer's `sb_rvalid_i`, `sb_rdata_i`, `sb_err_i` (port-doc gate 111 <= 111); units stated for the new boundary parameters (the writer's debounce is now `DEB_MS_P`; the `_CYC_P` comments name clock cycles); naming gate PASS.

**Parent-visible changes in round 2 (pin adoption)**
- New top parameter `NVM_RS_AGG_CYC_P` (default `CLK_HZ_P`, 1,000 ms). No new top port.
- `NVM_RS_TMO_CYC_P` default ceil(`CLK_HZ_P` / 50) (unchanged at 50 and 100 MHz).
- New snapshot word 37 (host word 0x20025): [15:0] AECP frames dropped at the slot gate while held.
- Behaviour: the AECP hold admission above; a restore can end on the aggregate (`rs_cause_o` 3, DEFAULTS or CLOSED). Firmware's bounded wait should allow 1,000 ms plus a roll-back.
- Also named (R390-1 S1): the binding alarm follows at least 2 x `NVM_RETRY_BACKOFF_CYC_P` of backoff; the side-port control word 1 reads busy 0, done 0, fail 1 in CLOSED; `NVM_RS_TMO_CYC_P` bounds every D3 wait.
- Parent evidence classifier: a disposition line for `protocol-processor/tb/pp_top/d3_mutants.py` ("mutation campaign; it plants one D3 saved-state defect from its own table into an isolated copy and requires every named check to fail in a completed run; no expected value is read from the text"), as #129's `retry_mutants.py` needed.

**Evidence at `2b38d68`**
- Every processor suite: 33 suites, 1,016,000 checks, 0 failing (pp_top 7,859, rx_validator 437); lint, `make check`, module matrix, Yosys, `srp_top` mutants and `nvm_port` figures rc 0; the D3 campaign 62 of 62 KILLED, goldens PASS.
- Parent consumer set (scratch parent at `7a7582f0`, gitlink at the head): C++ and Python idiom, xvlog (4 == ratchet), RTL source lists, `pp_srcs`, the builder tests, port contracts and naming rc 0. `pp_shadow` rc 2 on the five round-1 ports only (declared above in round 1); the evidence classifier rc 1 on `retry_mutants.py` (unexplained at this parent pin already) and the new driver, rc 0 with both dispositions added.
- The reviewers' own scripts at the head: every GET_RX_STATE answered in CLOSED and during a slowed walk, the slow-but-inside device ends at the aggregate, and all eleven reviewer mutants are killed.
- DR3a at the ratified values: healthy restores end within 2,661 cycles (53 µs at 50 MHz); a silent device at 2 x the per-wait deadline; a device answering every wait just inside it at exactly 1,000 ms.
- DR4, one instrument (1x1, out-of-context): lane 1 +1,021 LUT / +560 FF / 0 BRAM / 0 DSP against the 2,500 / 1,400 ceiling (round 2 adds +48 / +120); 8x8 +795 / +455. Post-place stays lane 2's.
- Section 15.2: all 37 rows applied (18 updated this round); the named sweep has 658 matching lines, 311 by this lane, the rest with scope reasons, 0 unreviewed.

## Round 3

[A429], head `cbbb5ac`, addressing R390-2 and R391-2 in the assigned order, with the clarification of the DR3a aggregate (#131, 5876655419: an aggregate expiry never closes a provable image):

1. `f8d1a83` **The aggregate never closes a provable image.** Before the image is proven the aggregate aborts nothing: the writer's new `agg_o` makes a binding walk still reading take its own per-wait path (`KL_acmp_nvm_shadow` input `rs_agg_i`: at once where no read is issued, in a stalled cycle otherwise, so a byte in hand is never orphaned and an issued read goes to the drain); it fails whole (`restore_cause_o` 3) and releases the listener, and the D3 walk then proves the image, reads no record and ends DEFAULTS (`rs_cause_o` 3). CLOSED only if the image cannot be proven (cause 7). After the proof and in the roll-back the path is unchanged. D3R14 runs the reviewers' probe D1 device (each header byte 2,100 clocks apart, each payload byte 19,001, every binding saved): DEFAULTS by clock 1,000,005 against the bound's clock 1,000,001, image valid, AECP answering, the enable released to ADP, the drained READ ending and a later SET persisting; with the image refused, CLOSED cause 7. Killed: `agg_closes_before_proof` (the pre-walk close), `binding_walk_ignores_aggregate`, `proof_reads_records_past_bound`. 07 section 5.3, 08 section 2, 01 F01.5, 03 rule (e) and the port comments state the path.
2. `9d66095` **Both guides** state every terminal the aggregate can take (DEFAULTS while the binding walk reads or in pass 0, a roll-back to DEFAULTS in pass 1, CLOSED only inside a roll-back another fault started) and both causes of CLOSED (`rs_cause_o` 7, the image; any other cause, a pass-1 roll-back that could not prove it again): the integrator's parameter row and bring-up step 3 (wait 1,000 ms plus 40 ms), the operator's outcome table, CLOSED paragraph and troubleshooting row, and diagram 23's step 3 (PNG re-rendered and inspected). The integrator guide's section 4.1 no longer calls the D3 writer's debt hold deferred.
3. `58c5fe9` **The aggregate's span over the roll-back** (D3R15): with the device's grants steered so a pass-1 fault lands a set distance before the bound, the bound falls inside the roll-back's debt wait (cause 6) and inside its re-LOCATE (cause 2), and each ends CLOSED on the bound's own clock. `agg_not_in_rollback` (the reviewer's own edit) is KILLED by both arms.
4. `e94bea8` **Inert after the terminal, never fired with an event in hand**: D3R16 observes a COMPLETE, a rolled-back DEFAULTS and a CLOSED restore two per-wait deadlines past the bound (verdicts, ownership and rows, a later SET included, unchanged; no roll-back strobe); D3R17 lands the writer's arbiter grant on the bound's own clock, and the aggregate waits a clock, ends DEFAULTS and drains that READ, after which a later SET persists. `agg_not_stopped_at_terminal` and `agg_fires_with_event_in_hand` (the reviewer's own edits) are KILLED.
5. `cbbb5ac` **Taken, R391-2 S1**: D3O7 grades the admission's resident-count return: in CLOSED the optional external drain steals the held AECP command and returns its slot, and of the next two commands one is held and only the other dropped. `resident_never_returned` is KILLED.

Every new mutant is in `tb/pp_top/d3_mutants.py` with a README row (69 in all).

**Parent-visible changes in round 3 (pin adoption)**
- No top port or parameter is added or changed.
- Behaviour: an aggregate expiry while the binding walk still reads now ends the binding walk failed (`restore_cause_o` 3, every binding at its default) and the D3 walk DEFAULTS (`rs_cause_o` 3, done, fail, AECP and the enable released), where round 2 ended CLOSED. CLOSED now means an unprovable image (cause 7) or a pass-1 roll-back that could not prove it again (the pass-1 cause).
- `KL_acmp_nvm_shadow` gains the input `rs_agg_i` inside the top. The parent's `tb/verilator/nvm_cosim/cosim_top.sv` instantiates that module directly: its lint gains one `PINMISSING` warning (rc 0; 85 to 86 warnings); tie `.rs_agg_i (1'b0)` there.
- Found this round, not introduced by it: the parent's `nvm_cosim` quick loop fails 7 of 315 checks (B1 to B4 `later_record_persists` and three power-cycle restores) from round 1's `f72a2d2` (the binding manager's DR2c backoff) on; it passes 315 of 315 at base `c951a9ff` and at `505524e`, and fails identically at `2b38d68` and at this head. It is outside the consumer set; the pin-adoption lane reconciles those cases with DR2c.
- Carried from rounds 1 and 2: the five round-1 ports (`pp_shadow` PINMISSING, unchanged), `NVM_RS_AGG_CYC_P`, the ceil per-wait default, snapshot word 37, and the evidence-classifier disposition line for `protocol-processor/tb/pp_top/d3_mutants.py`.

**Evidence at `cbbb5ac`**
- Every processor suite: 33 suites, 1,016,016 checks, 0 failing (pp_top 7,875); lint, `make check`, module matrix, Yosys, `nvm_port` figures and `srp_top` mutants rc 0; the D3 campaign 69 of 69 KILLED, goldens PASS.
- Parent consumer set (scratch parent at `7a7582f0`, gitlink at the head): 9 of 11 rc 0. `pp_shadow` rc 2 on the five round-1 ports only (20 warnings, as the manager's receipt at `2b38d68`); the evidence classifier rc 1 on `retry_mutants.py` (explained at the parent's dev pin) and `d3_mutants.py`, rc 0 with both disposition lines and nothing else.
- The reviewers' own scripts at the head: R390-2's 15 mutants, 13 KILLED on the D3 section (`agg_not_in_rollback` and `agg_ignores_in_hand` now among them; `hold_after_release` KILLED by the full suite as before; `held_gate_ignores_da` without effect, as R390-2 judged); R391-2's 15 of 15 KILLED; probe D1 and P8 case A now end DEFAULTS at clock 1,000,005; P6 differs from its round-2 oracle in exactly the 452 pre-proof expiries, now DEFAULTS.
- DR3a at the ratified values, unchanged except the new path: the per-byte device ends DEFAULTS 4 clocks after the bound. DR4, same-instrument 1x1 out-of-context synthesis: lane 1 +1,030 LUT / +559 FF / 0 BRAM / 0 DSP (round 3 adds +9 / -1); 8x8 +1,067 / +585. Post-place stays lane 2's.
- Section 15.2: all 37 rows applied (15 updated this round); the named sweep has 681 matching lines, 334 by this lane, the rest with scope reasons, 0 unreviewed.

## Round 4

[A432], head `8457258`, addressing R390-3 and R391-3 in the assigned order, with the ruling on the parent `nvm_cosim` B1-B4 (#131, 5880658258):

1. `014e679` **An abort in the arbiter's issue cycle is drained (R390-3 F1).** `KL_pp_nvm_mgr_arb` arms the drain on an abort presented together with a READ strobe in the cycle it issues that READ (the owner still `O_NONE`), for either manager, with no port change. The binding walk meets this case: its strobe is registered, so it is out in its first `H_RS_STREAM` clock, and the aggregate's `agg_o` can first read 1 on that clock. The D3 writer never presents both (its request is `W_RQ`'s or the service's, its abort `W_RD`'s), so `tb/acmp_nvm` N10 drives manager 1 through the case. D3R18 lands the fifth binding READ strobe on `agg_o`'s first clock: the arbiter drains the READ from the next clock, the restore ends DEFAULTS, and once the device ends the READ the port is idle and a later SET persists. Under the head's arbiter both checks fail: D3R18 sees no drain, the port busy 100,000 of 100,000 clocks and no WRITE; N10 sees no drain, and neither the walk nor manager 1's next READ is served. R390-3's E1 probe at this head: the aligned boot drains its READ and the later SET persists. The binding manager's comments, 07 section 5.3's row and 02 section 8.2 state the issue-cycle drain.
2. `8610ab3` **Every pre-proof variant graded (R390-3 F2, R391-3 F2).**
   - D3R19: the image is loaded after reset and proven by the writer's LOCATE after the bound. The restore ends DEFAULTS, cause 3, 546 clocks after the bound, with no D3 record READ. With the bound 271 clocks inside that LOCATE: DEFAULTS, image valid, AECP released.
   - D3R20: a proof on the bound's own clock, in `W_IMG` and in `W_IMGLOC` with the answer in hand, ends DEFAULTS on the next clock with no record READ.
   - D3R21: a binding byte in the manager's hand on the expiry clock. The walk fails whole at its next waiting clock (cause 3 registered two clocks after the bound), and the restore ends DEFAULTS.
   - Killed by these checks: `agg_closes_during_proof`, `proof_past_needs_fire`, `proof_default_only_from_img`, `proof_past_bound_needs_fired` and `agg_o_pulse`, and the head's arbiter (`drain_misses_issue_cycle` in `tb/pp_top`, `drain_misses_issue_cycle_m1` in `tb/acmp_nvm`). `d3_mutants.py` now holds 76 controls, and every README count is re-measured.
3. **The parent-visible list (R390-3 F3 = R391-3 F1)** was consolidated here, with the measured `nvm_cosim` attribution; round 5 corrects it and keeps it once, in the Round 5 section. It needs no source change.
4. `8457258` **Suggestions taken (R391-3 S1-S3).**
   - The firmware's wait: 1,000 ms plus two per-wait deadlines plus a few clocks, with 1,060 ms a stated margin. 07 section 5.3, 08 and the writer banner now say the terminal comes within one per-wait deadline plus a few clocks, or two after a roll-back.
   - The integrator's `NVM_RS_AGG_CYC_P` row names both CLOSED cases a roll-back gives. 07 section 5.3 gains the image proof's own per-wait deadline: CLOSED, cause 3, no roll-back, reachable only with a misconfigured deadline. Both guides mention it.
   - `KL_acmp_nvm_shadow`'s banner states that a direct instantiator derives `RETRY_BACKOFF_CYC_P` and `RS_TMO_CYC_P` from its own clock. Comment only.

**Evidence at `8457258`**
- Every processor suite passes: 33 suites, 1,016,031 checks, 0 failing (`tb/pp_top` 7,888, `tb/acmp_nvm` 355). Lint, `make check`, the module matrix, Yosys, `nvm_port` figures and `srp_top` mutants return rc 0. The D3 campaign kills 76 of 76, goldens PASS.
- The reviewers' own scripts at the head:
  - R390-3's 18 mutants: `agg_closes_during_proof` and `proof_past_needs_fire` are KILLED, as are the other 14 that fail the D3 section. `hold_after_release` passes the D3 section (the full suite killed it in rounds 2 and 3; not rerun here), and `held_gate_ignores_da` has no effect, both as R390-2 judged.
  - R391-3's 20 mutants: 19 fail the D3 section, including `agg_o_pulse`, `proof_past_bound_needs_fired` and `proof_default_only_from_img`. `bind_agg_ignores_byte_in_hand` passes, as that reviewer judged it equivalent in effect.
  - E1 aligned: the READ is drained and the later SET persists. E2 matches the reviewer's head readings. D1's five arms match that reviewer's golden (+4, +545, +44, +4,105, +545).
- Parent consumer set (scratch parents at dev `b5c0f69d`, gitlink at the head, the manager's 15 commands):
  - Gitlink only: 10 of 15 rc 0. `pp_shadow` stops on the round-1 PINMISSING, the classifier on `d3_mutants.py`, `nvm_cosim` quick at 308/315, `milan_dp` at `gmstep`/`gptp`, `milan_dp_render` at T8.
  - With every edit round 4 declared applied (the list as corrected in round 5 is below): **15 of 15 rc 0**.
    - `nvm_cosim` quick 315/315, with 0 PINMISSING.
    - `pp_shadow` 0 failures in four builds.
    - `milan_dp`: `gmstep` 103/103, `gptp` and `gptp-lat` 181/181, every pool leg and both mutation campaigns green.
    - `milan_dp_render` 65/65 and 152/152.
  - Starting the walk in the three `milan_dp` harnesses, as the bank note scoped it, is necessary but not sufficient. It lets `make` reach the pool legs, which then need the `sim_nxn.cpp` and image-less edits (in the list below).
- DR3a: unchanged on every earlier path. The new paths, in clocks after the bound: a binding READ abandoned in its issue clock ends DEFAULTS +4 from `agg_o`'s first clock (probe E1); D3R19 +546 and +272; D3R20 +1; D3R21 +5.
- DR4, same-instrument 1x1 out-of-context synthesis: lane 1 is +1,031 LUT / +559 FF / 0 BRAM / 0 DSP; round 4 adds +1 LUT, the arbiter's drain term. The 8x8 diagnostic is +842 / +502 (round 4 -225 / -83, synthesis variation outside the changed modules). Post-place stays lane 2's.
- Section 15.2: all 37 rows applied, 11 updated this round. The named sweep has 703 matching lines, 356 by this lane and the rest with scope reasons, 0 unreviewed.

## Round 5

[A435], head `9dce84e`, addressing R390-4 and R391-4 in the assigned order. There is no RTL change. Items 1, 2 and 4 change the parent-visible list and its scratch edit script only; item 3 is the one commit.

1. **The nightly gPTP harness (R390-4 F1).** `milan_dp`'s `ax1x1gptp` (`sim_ax1x1gptp.cpp`, run nightly by `milan_dp_gptp`) serves its AEM image and grades GET_AVB_INFO and GET_AS_PATH, but never starts the restore walk. It joins the `PP_CTRL[1]` harness obligation below, which states that it is outside the consumer set. Measured in a scratch parent at dev `eaa88a32` with the edits: `make -C tb/verilator/milan_dp ax1x1gptp` rc 0, 139 checks, 0 failures (the harness's 137 plus the walk check on each of its two boots), 17.0 s simulated in 3,277 s of wall time on a loaded host. With every edit but this one (at `8457258`, the same RTL), it fails 15 of 137: every GET_AVB_INFO and GET_AS_PATH check, each unanswered.
2. **The wedged-memory arm in the timed leg (R391-4 F1).** The declared `sim_nxn.cpp` edit now runs `prove_a_wedged_response_memory_reports_and_heals()` inside the image arm, after the restore and before the `NOTIFY_TIMED_TB` return, in every leg. `notify`, the shipping 1x1 shape, prints its six `[AECP-WTMO]` checks and passes 378 of 378; R391-4's own `parent_scratch.sh` shows the same. The list now states that the `[AECP]` no-descriptor-memory degrade arm (5 checks) is retired in every `sim_nxn` leg, and why: with no image, AECP is held from reset (section 8.1). Two hold checks replace it.
3. `9dce84e` **The arbiter's own contract (R390-4 S1 = R391-4 S1, taken).** `tb/acmp_nvm` N11 drives manager 1 as N10 does:
   - N11a: a manager-1 WRITE presented with its abort, held from its strobe to the write's end, is issued as a commit and never drained. Manager 1 streams every byte and sees its done, and the device holds the record byte-exact.
   - N11b: manager 1 presents its abort, alone, in the issue cycle of each of the walk's eight READs. None is drained, and the walk completes as saved.
   - N11c: after a completed manager-1 WRITE, a manager-1 READ abandoned in its issue cycle is drained from the next cycle, and manager 1's next READ completes.
   - The head's arbiter passes all three, as its banner states, so the STOP condition does not apply.
   - The reviewers' `issue_arm_cross_intent` (N11b), `issue_arm_ignores_we` and `issue_arm_write_too` (N11a) and `issue_arm_stale_we` (N11a, N11c) join `d3_mutants.py`. So does `owned_arm_write_too`, the owned half of the same banner rule, which N11a's held abort grades. All five are KILLED, with README rows. `tb/acmp_nvm` now has 359 checks, and the driver holds 81 controls. The wrap gains four taps: the arbiter's issue and its intent, and the binding manager's strobe and its intent.
4. **The scratch-parent refinements (R390-4 S2, taken).**
   - (a) The image-less legs' walk check names the terminal they reach, CLOSED (busy 0, done 0, fail 1).
   - (b) The timed leg's `[AECP-WTMO]` arm is item 2.
   - (c) `cosim_top.sv` terminates `wr_chg_o` on a named no-connect, like the store's other unused outputs. A new output costs one lint warning either way: 85 against the base's 84, rc 0.

**Parent-visible for pin adoption.** Round 5 consolidated and corrected the list; round 6 carries it, with its own additions, in the Round 6 section below.

**Evidence at `9dce84e`**
- Every processor suite passes: 33 suites, 1,016,035 checks, 0 failing (`tb/pp_top` 7,888, `tb/acmp_nvm` 359). Lint, `make check`, the module matrix, Yosys, `nvm_port` figures, `git diff --check` and `srp_top` mutants return rc 0. The D3 campaign kills 81 of 81, goldens PASS, and every README count equals the run.
- The reviewers' own scripts at the head:
  - R390-4's four issue-cycle mutants: `issue_arm_cross_intent` and `issue_arm_ignores_we` still pass the D3 section, and are now KILLED by `tb/acmp_nvm` (N11b, N11a). `issue_arm_one_clock_late` and `issue_arm_m1_dropped` stay KILLED. The arbiter unit probe passes 9 of 9. The arbiter monitor over `tb/acmp_nvm` now counts the inputs round 4 found at 0: a WRITE strobe with an abort, manager 0's READ issued with manager 1's abort (8), an abort while a WRITE is owned.
  - R391-4's six issue-cycle mutants on `tb/acmp_nvm`: `issue_arm_stale_we`, `issue_arm_cross_intent` and `issue_arm_write_too` now fail N11. `issue_arm_m0_only` and `issue_arm_one_clock_late` fail N10 and N11c. `issue_arm_m1_only` passes that suite, as in round 4, and D3R18 kills it.
  - E1/E2 and D1 are identical, line for line, to each reviewer's own round-4 receipt at the previous head. R391-4's `parent_scratch.sh` with this round's edits shows `notify` at 378 of 378 with its six `[AECP-WTMO]` checks.
- Parent consumer set (scratch parent at dev `eaa88a32`, gitlink at the head, every edit in the consolidated list applied): **16 of 16 rc 0**, the manager's sixteen commands.
  - `nvm_cosim` quick 315/315, and its lint 0 PINMISSING.
  - `pp_shadow` 0 failures in four builds.
  - `milan_dp`: `gmstep` 103, `gptp` and `gptp-lat` 181, every pool leg (the image-less legs naming CLOSED, `notify` 378 and the four `nxn` legs each with six `[AECP-WTMO]` checks), and both mutation campaigns green.
  - `milan_dp_render` 65/65, 152/152 and 5/5.
  - And, outside the set, `ax1x1gptp` 139 of 139. `milan_dp_gptp`'s own `verify_abort.py` controls pass 40 of 40.
- DR3a: `--dr3a` is byte-identical to round 4's; no file under `hdl/` changed.
- DR4, same-session 1x1 out-of-context synthesis of base and head: lane 1 is +1,031 LUT / +559 FF / 0 BRAM / 0 DSP; round 5 adds 0. Post-place stays lane 2's.
- Section 15.2: all 37 rows applied, 3 updated this round (09 section 8.2, the `acmp_nvm` and `pp_top` READMEs). The named sweep has 704 matching lines, 357 by this lane and the rest with scope reasons, 0 unreviewed.

## Round 6

[A442], head `9b4da6b`, addressing R390-5 F1 = R391-5 S1 in one commit and carrying R391-5 S2 for the pin-adoption lane. There is no RTL change: `git diff 9dce84e 9b4da6b -- hdl syn scripts .github Makefile` is empty.

1. `9b4da6b` **The owned half of the owner-matched drain (R390-5 F1 = R391-5 S1).** `tb/acmp_nvm` N11d holds manager 1's abort, alone, in every cycle manager 0 owns each of the walk's eight READs. Ownership runs from the cycle after the READ's issue through the port's done or err, which the wrap now publishes as `arb_end_o` (a test-bench tap). The abort is never presented in the READs' issue cycles, which N11b grades, so each check grades one term of the rule.
   - Non-vacuity: at the head the abort is present in 168 of the 168 owned cycles (at least 12 of them before each READ's end, where an armed drain would take effect) and in none of the 8 issue cycles. None is drained, and the walk completes as saved with nothing written.
   - The reviewers' edits `owned_arm_cross_intent` (both owned terms take either abort) and `cross_own_m1_drains_m0` (manager 0's owned term takes manager 1's abort) join `d3_mutants.py` with README rows. N11d alone kills each, with 1 failing check: the walk's first READ is drained, and the binding walk fails on its per-wait deadline. `issue_arm_cross_intent` still fails N11b alone.
   - `tb/acmp_nvm` now has 360 checks, and the driver holds 83 controls.
2. **Docs.** The row in `docs/architecture/09_verification.md` section 8.2 now names what the tree grades: manager 1's half of each rule (N11a; N11b in the issue cycle and N11d while owned; N11c). It states that the manager-0 halves are ungraded by construction.
   - The `tb/acmp_nvm` README lists the five manager-0 inputs that R391-5 S1 counts, and why no in-tree bench presents them. The binding manager raises its abort only while its own READ is strobed or owned. Its issue-cycle abort needs an aggregate expiry, which falls only inside the restore walks, where both managers only read.
   - It names the out-of-tree probes. R390-4's arbiter unit probe kills three of the five (cases F and B). No probe kills `cross_own_m0_drains_m1` or `write_own_m0_only`. R391-5's monitor finds none of the five presented with both real managers.
3. **The parent-visible list** below carries R391-5 S2 (the order in `sim_nxn.cpp` after the moved `[AECP-WTMO]` arm) and the arbiter's ungraded manager-0 inputs. The scratch edit script is unchanged.

**Parent-visible for pin adoption: rounds 1-6, consolidated**

This list replaces round 5's and carries it unchanged, apart from round 6's two additions: the arbiter inputs the binding manager never presents (R391-5 S1), and, in the `sim_nxn.cpp` legs, the word-36 check order and the stale comments the moved `[AECP-WTMO]` arm leaves (R391-5 S2). Round 5 added the nightly gPTP harness, corrected the `sim_nxn.cpp` edit so the timed leg keeps its wedged-memory arm, named the retired degrade arm, and took the reviewers' two scratch refinements. The processor side has no change in rounds 5 and 6.

Top ports, parameters and status (parent instance in `hdl/milan/KL_pp_shadow.sv`):
- Round 1: new outputs `restore_closed_o`, `restore_rb_o`, `rs_cause_o[2:0]`, `restore_cause_o[1:0]`, `d3_unflushed_o`. `pp_shadow` lint reports them PINMISSING until they are connected.
- Round 1, the glue: `pend_i = (|nvm_unflushed_o) | d3_unflushed_o` (`aecp_dyn_dirty_o` is diagnostic only), `alarm_i` from `nvm_alarm_o`, and the combined restore status with CLOSED, roll-back and both causes.
- New parameters: `NVM_RETRY_BACKOFF_CYC_P` (round 1; ceil(`CLK_HZ_P` / 2), 500 ms) and `NVM_RS_AGG_CYC_P` (round 2; `CLK_HZ_P`, 1,000 ms). `NVM_RS_TMO_CYC_P` now defaults to ceil(`CLK_HZ_P` / 50) (round 2; unchanged at 50 and 100 MHz). Keep all three derived from the clock.
- Snapshot word 37 (round 2), host word 0x20025: [15:0] AECP frames dropped at the slot gate while held.

Behaviour the parent sees:
- Round 1: `restore_done_o`, busy, fail and blank combine both walks (blank never with fail), and `nvm_alarm_o` is either producer's.
- Round 1: ADP takes `entity_enable_i && restore_done_o`; the side-port lock keeps the requested enable.
- Round 1: AECP is held from reset to the D3 terminal, and for ever in CLOSED. Round 2 adds the admission: one AECP record held, every further one dropped and counted.
- Round 1: manager 1 (the D3 writer) reads and writes records `0x00`, `0x02+`, `0x0A+`, `0x30+`, `0x40+` and `0x50+` on the shared device face.
- The terminals: COMPLETE, DEFAULTS or CLOSED.
  - CLOSED means an unprovable image (`rs_cause_o` 7) or a roll-back that could not prove it again (the pass-1 cause). Round 4 adds a third case: cause 3 with no roll-back, only with a deadline set below the image walk.
  - An aggregate expiry never closes a provable image (round 3).
- Round 2 notes: the binding alarm follows at least 2 x `NVM_RETRY_BACKOFF_CYC_P` of backoff; side-port control word 1 reads busy 0, done 0, fail 1 in CLOSED; `NVM_RS_TMO_CYC_P` bounds every D3 wait.
- Round 4: the arbiter drains a READ abandoned in its issue cycle. There is no port change, and a parent that ties manager 1 off (`nvm_cosim`) sees no difference.
- Round 5: nothing new (no RTL change).
- Round 6: nothing new (no RTL change). For a parent that adds a manager to `KL_pp_nvm_mgr_arb` or replaces either one: the processor grades the arbiter's rules for manager 1's half (`tb/acmp_nvm` N10 and N11a-d) and the binding walk's issue-cycle drain (`tb/pp_top` D3R18). Five manager-0 inputs stay ungraded by construction, because the binding manager aborts only the READ it strobes or owns: its abort in manager 1's issue cycle, its abort while manager 1 owns a READ, its WRITE strobe presented with an abort, its abort while it owns a WRITE, and its READ abandoned in its issue cycle after a WRITE (R391-5 S1 counts them; the `tb/acmp_nvm` README lists them). Whatever makes manager 0 present one of them must grade it first. Out of tree, R390-4's arbiter unit probe kills three of the five, and R391-5's monitor finds none of them presented with both real managers.

Firmware:
- Round 1: load and CRC-check the AEM before `PP_CTRL[1]`, or the restore ends CLOSED.
- The bounded wait for the terminal is 1,000 ms plus two per-wait deadlines plus a few clocks (round 4 wording; 1,060 ms a margin). The parent's `MILAN_NVM_RESTORE_TIMEOUT_MS` = 3,000 already covers it.
- Every boot path that enables the entity starts the restore walk (the manager's bank note 5880274287; parent #70 5880276193 item 2). Today `nvm_boot()` returns before `nvm_restore_walk()` when the record set does not match the generated shape ("persistence disabled"). Since round 1 that leaves AECP held and the entity uncontrollable. That path must run the walk blind, as the refused-window path does, with a host test. No consumer-set gate exercises it, so the scratch demonstration below does not apply it.

Parent harnesses. The consumer set found every one of these but `ax1x1gptp`, which it does not build. Each edit below is applied in a scratch parent at dev `eaa88a32` only (the edit script is in this round's packet), and each is measured:
- **`PP_CTRL[1]` harness obligation** (5880274287, 5880276193 item 1). Every parent harness that exercises AECP starts the boot restore walk before its first AECP command, as `sim_aclk.cpp` `start_the_boot_restore_walk` does:
  - `milan_dp` `gmstep` (`sim_gmstep.cpp`), and `gptp` and `gptp-lat` (`sim_gptp.cpp`);
  - `milan_dp` `ax1x1gptp` (`sim_ax1x1gptp.cpp`), the nightly physical gPTP harness that `milan_dp_gptp` runs (round 5, R390-4 F1). It is **outside the consumer set**: the default `milan_dp` sweep does not build it. It serves the built AEM image from reset and grades GET_AVB_INFO (once before acquisition) and GET_AS_PATH, but never wrote `PP_CTRL[1]`. The walk starts after its image is served and before its first AECP command: at the top of `configure()`, which follows every reset, as `nvm_boot()` runs on every boot, graded by a `[BOOT] PP_STAT[2] the restore walk sequenced` check. Measured in a scratch parent at dev `eaa88a32` with every edit in this list: `make -C tb/verilator/milan_dp ax1x1gptp` rc 0, 139 checks, 0 failures, 17.0 s simulated, 3,277 s of wall time on a loaded host (the nightly suite's budget is 5,400 s). With every edit but this one (measured at `8457258`, whose RTL this head keeps): 15 of 137 fail, every GET_AVB_INFO and GET_AS_PATH check, each unanswered. The suite's own controls (`verify_abort.py`: setup abort, no-TX and no-Pdelay accounting) pass with the edit, 40 of 40, so the whole `milan_dp_gptp` suite is green.
- **`milan_dp` pool legs.** They run only once `gmstep` and `gptp` pass: until then `make` stops at those failures, which is why the manager's bank did not see these.
  - The image-less benches (`sim_main.cpp`: the main, `nolpf` and `ax1x1` legs; `sim_aclk.cpp`: `aclk`) start the walk only to release the listener. With no AEM image in place the restore ends CLOSED (PP_STAT busy 0, done 0, fail 1), which releases the listener and holds AECP. Their wait must end on either terminal, and their check names the one they reach: "PP_STAT the restore walk ended CLOSED (no AEM image: busy 0, done 0, fail 1)" (round 5, R390-4 S2a). Without the edit each fails its one walk check.
  - The `sim_nxn.cpp` legs (`notify`, `nxn`, `nxndv`, `nxn8`, `nxn4c`) served AECP with no descriptor image and let the image arrive later. AECP is now held from reset until the restore, and the restore needs the image in place before `PP_CTRL[1]` (round 1).
    - They must start the walk once the descriptor memory answers.
    - The `[AECP]` no-descriptor-memory degrade arm (`prove_read_descriptor_degrades_with_no_descriptor_memory()`, 5 checks: READ_DESCRIPTOR answered BAD_ARGUMENTS) is **retired in every `sim_nxn.cpp` leg**. With no image, AECP is held from reset (contract section 8.1), and a CLOSED restore keeps holding it, so the command that arm grades is never answered. Two hold checks replace it: READ_DESCRIPTOR held and unanswered before the restore, then answered at the release (the hold admission, 5873580386).
    - The wedged-response-memory arm (`prove_a_wedged_response_memory_reports_and_heals()`, 6 `[AECP-WTMO]` checks) needs AECP released. It runs inside the image arm, after the restore, in every leg, and before the timed `notify` leg's `NOTIFY_TIMED_TB` return (round 5, R391-4 F1). So `notify`, the shipping 1x1 shape, keeps its six checks. Its heal now answers SUCCESS.
    - **The order the moved arm leaves (round 6, R391-5 S2).** At base the untimed legs ran the degrade arm and `[AECP-WTMO]` before the image arm, so the last check of `grade_the_first_descriptors_on_the_wire()`, "[AECP-IMG] the response buffer reports no fault (word 36)", also showed that the response master's fault clears after a heal. With the arm after that function, the word-36 check runs before the wedge and no longer shows it. The real edit must read word 36 again after the arm, or keep the arm where it is and add a word-36 read to its heal. Three harness comments describe the old order and must be refreshed: "parked in S_BAD with FAULT_TIMEOUT from the two sections above" and "[AECP-WTMO] already moved the error counter" (the two that R391-5 names), and "[AECP-WTMO] added one deliberately" beside the voided-response delta check (the same kind, found in round 6). In the scratch `sim_nxn.cpp` at dev `eaa88a32` with the edits: the arm's call `:2484`, the word-36 check `:2609-2610`, the comments `:2547-2549`, `:2560-2562` and `:2605-2607`. The heal stays graded in three places, as R391-5 notes: the arm's own SUCCESS heal in every leg, `pp_shadow` `[N]`, and the processor's `tb/resp_buf` R10. The scratch edit script is byte-identical to round 5's, so the legs measure as they did there.
    - Measured: `notify` 378 of 378 with the six `[AECP-WTMO]` checks (R391-4 measured 381 at base `c951a9ff`: 5 degrade checks retired, 2 hold checks added); `nxn` 1,841 of 1,841 (R391-4: 1,844 at base), and `nxndv`, `nxn8` and `nxn4c` pass, each with its six `[AECP-WTMO]` checks. Without these edits `notify` fails 210 of 310 checks, and the four `nxn` legs fail hundreds and then crash (rc 139) on unanswered AECP.
- **`milan_dp_render` T8 REMOVE.** This harness already starts the walk. Its T8 opens the collection 639 axis cycles after the REMOVE's answer, less than one commit-to-pin bound. Since the boot restore also runs the D3 walk, the leg reaches T8 272 axis cycles later (measured against the processor at `c951a9ff`, with every other interval identical). One frame committed before the removal is then decoded with the removed slots still carrying data, which fails both T8 checks. T8 must wait out one commit-to-pin bound (`kFrameAxis + kCdcFloorAxis + kBitAxis`) before collecting.
- **`pp_shadow`.** Its sim runs only once the round-1 ports are connected; until then lint stops it with 20 PINMISSING.
  - The pending phases (K, K10, K12) enable the entity without the walk. They must start it before the enable and wait for its terminal. Nothing answers behind the backend's configured window in that bench, so the walk ends on two per-wait deadlines, about 4.0 M clocks at its 100 MHz.
  - M2 must start the walk after its memory handover (the firmware's order). The D3 writer's LOCATE then proves the image the store parked on.
  - P3's "no record was validated" must expect blank 0: the combined `restore_blank_o` never reads 1 with fail (round 1).
  - Without these edits: K, K10, K12, M2 and P3 fail 80 of 590 checks per build.
- **`nvm_cosim` `cosim_top.sv`**, which instantiates internal modules directly:
  - `.rs_agg_i (1'b0)` on `KL_acmp_nvm_shadow` (round 3);
  - `wr_chg_o` on `KL_aecp_dyn_state` (round 1's `4dd37c2`; a second PINMISSING), on a named no-connect `wr_chg_nc_w`, the file's convention for the store's other unused outputs (round 5, R390-4 S2c). A new output costs one lint warning either way (one more UNUSEDSIGNAL, or a PINCONNECTEMPTY for `()`): lint 85 warnings against the base's 84, rc 0, 0 PINMISSING;
  - `RETRY_BACKOFF_CYC_P` derived from its clock as the top derives `NVM_RETRY_BACKOFF_CYC_P`, `(CLK_HZ_P / 2) + (CLK_HZ_P % 2)` (round 1's `f72a2d2`);
  - `RS_TMO_CYC_P` moved to the top's ceil derivation (round 2; identical at the suite's 1 MHz);
  - `KL_pp_nvm_mgr_arb` has no port change.
- **`nvm_cosim` B1-B4 give-up window**: 1,500 to 2,000 ms of model time, past the 500 ms debounce, both 500 ms backoffs and the attempts. Measured 315 of 315 with the `cosim_top.sv` edits.
- **The B1-B4 attribution**, as measured in round 4 in a scratch parent at dev `b5c0f69d` (both reviewers reproduced it at `eaa88a32`):
  - The failures do not come from the ruled 500 ms. They come from `cosim_top.sv` leaving `RETRY_BACKOFF_CYC_P` at its 100 MHz module default of 50,000,000 clocks, which is 50 s at the suite's 1 MHz.
  - Only the pins tied: 308 of 315. B1-B4 fail `later_record_persists@end:0x21`, and the power cycles after B1, B2 and B4 fail `restores_last_verified`. The later record waits behind the backed-off one, reported pending (`pend` 1), and is never lost (the ruling).
  - Adding the derived backoff: 311 of 315. B1 and B4 fail `last_verified_kept@end:0x20` with their two restores: the third attempt lands after the case's 1,500 ms fault window closes and succeeds, so the case's give-up premise breaks.
  - Adding the 2,000 ms window: 315 of 315.
- **Evidence classifier**: add `DUT_READER_DISPOSITIONS["protocol-processor/tb/pp_top/d3_mutants.py"]` = "mutation campaign; it plants one D3 saved-state defect from its own table into an isolated copy and requires every named check to fail in a completed run; no expected value is read from the text" (round 2).

Lane 2 keeps DR4 post-place and the 8x8 obligation (open, not waived).

**Evidence at `9b4da6b`**
- Every processor suite passes: 33 suites, 1,016,036 checks, 0 failing (`tb/pp_top` 7,888, `tb/acmp_nvm` 360). Lint, `make check`, the module matrix, Yosys, `nvm_port` figures, `git diff --check` and `srp_top` mutants return rc 0. The D3 campaign kills 83 of 83, goldens PASS, and every README count equals the run.
- The reviewers' own round-5 scripts at the head:
  - R390-5's `r5_extra_mutants.py` on `tb/acmp_nvm`: `r5_owned_cross_m0_only` and `r5_owned_cross_both` are KILLED by N11d, and `r5_issue_cross_m0_only` by N11b. `r5_issue_cross_m1_only` and `r5_owned_cross_m1_only` pass: they are manager-0 halves, now listed as ungraded by construction.
  - R390-5's R5P probe still plants on the head and passes (361 of 361). Under `r5_owned_cross_m0_only`, R5P and N11d both fail, and the unmodified in-tree harness now fails N11d. The arbiter unit probe's output is byte-identical to that reviewer's round-5 receipt (9 of 9 at the head).
  - R391-5's `run_r391_5.sh ... acmp` over its 16 edits: `cross_own_m1_drains_m0` now fails N11d, and every other count equals that reviewer's receipt. Six edits still pass `tb/acmp_nvm`: the five manager-0 halves the README lists, and `issue_arm_m1_only`, which D3R18 kills in `tb/pp_top`. Its monitor over `tb/acmp_nvm` sees only manager-1 inputs. Its `check_readme_counts.py` on this head's campaign reports 86 entries and 0 problems.
- Parent consumer set (scratch parent at dev `eaa88a32`, gitlink at the head, the unchanged edit script): **16 of 16 rc 0**, the manager's sixteen commands, and every reading equals round 5's. That includes `nvm_cosim` quick 315/315 (lint 0 PINMISSING), `pp_shadow` 0 failures in four builds, `milan_dp` with `notify` at 378 and 30 `[AECP-WTMO]` passes, and `milan_dp_render` 65/65, 152/152 and 5/5. `ax1x1gptp` was not rerun, because no file it builds changed since round 5 (139 of 139).
- DR3a: `--dr3a` is byte-identical to rounds 4 and 5; no file under `hdl/` changed.
- DR4: no synthesized file changed, so lane 1 stays at +1,031 LUT / +559 FF / 0 BRAM / 0 DSP (round 5's same-session 1x1 measurement); round 6 adds 0. Post-place stays lane 2's.
- Section 15.2: all 37 rows applied, 3 updated this round (09 section 8.2, the `acmp_nvm` and `pp_top` READMEs). The named sweep has 705 matching lines, 358 by this lane and the rest with scope reasons, 0 unreviewed.
