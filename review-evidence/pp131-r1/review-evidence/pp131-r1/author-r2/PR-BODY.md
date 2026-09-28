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
