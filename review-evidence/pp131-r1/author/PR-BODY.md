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
