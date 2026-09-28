[R390] NEGATIVE - exact head cbbb5acc77e9e068c3313d78ed4c1e5e79299a71

# R390-3: independent internal review of processor PR #132 (issue #131, D3 lane 1), round 3

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Head reviewed | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71`, tree `63e8bbf1cb966049b4f405145f9e73fd2b03adc5` (verified in the review clone) |
| Delta | `2b38d68e..cbbb5acc`: five commits `f8d1a83`, `9d66095`, `58c5fe9`, `e94bea8`, `cbbb5ac` (19 files, +801/−103); base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` |
| Rulings | DR3a/DR4 ratification (parent issue 70 comment 5873060660) and its clarification (processor issue 131 comment 5876655419); round-3 assignment (issue 131 comment 5876934804); DR2a/DR2c and the DR2c-carrier rulings (parent issue 70 comments 5862405632, 5863247772, 5868716535) |
| Contract | parent `docs/design/SAVED_STATE_MATERIALIZATION.md` (sha256 `e26784e1…f077`, identical at `7a7582f0` and dev `b5c0f69d`), §§5, 6.1–6.4, 7 and the DR2/DR3a rows |
| Verdict | **NEGATIVE**: one MAJOR and two MINOR findings are open. All five lenses are UNCLEAN. Every round-2 finding of mine is resolved. |

## 1. How the review was reconstructed

1. The repository still has no AGENTS.md or CONTRIBUTING.md. The conventions come from `README.md`, `docs/README.md`, `hdl/README.md`, `docs/architecture/09_verification.md` §7 and the suite READMEs' mutation-record convention.
2. Issue #131 and PR #132:
   - the round-3 assignment (5876934804), the DR3a clarification (5876655419) and the author's round-3 review-ready note (5879510598);
   - the PR body, including its "Round 3" section and every "Parent-visible" list;
   - the manager's bank comments at `2b38d68e` (5876225160) and at this head (5880274287), and the R390-3 review-start comment (5879932577).
3. On parent issue 70: the DR rulings (5862405632), the DR2c-carrier ruling and its correction (5863247772, 5868716535), the DR3a ratification (5873060660), and the lane-2 scope record (5880276193).
4. The D3 contract, read from a read-only parent clone at dev `b5c0f69d`: §6.1 (the writer in service and its BACKOFF), §6.2 (the restore table: ABORT, ROLL-BACK, RE-LOCATE), §6.3 (the next-state functions), §6.4 (two managers, one port, the drain), §7 (the clear rule), and the DR3a row.
5. `git diff 2b38d68e..cbbb5acc`, read hunk by hunk:
   - the RTL: the writer's `expire_w`, `agg_past_w`, `proof_w` and `agg_o`; the shadow's `rs_agg_i` path; the engine and top wiring;
   - the new D3R14–D3R17 and D3O7 cases;
   - `d3_mutants.py`, the wrap and bench changes, and every documentation hunk.

   I also read the arbiter (`KL_pp_nvm_mgr_arb.sv`) and the port (`KL_pp_nvm_port.sv`), because the new binding-walk path ends in their drain.
6. Public executable evidence. `kebag-logic/milan-fpga@b657a2de` `review-evidence/pp131-r1` is the round-1 author packet only (§8). The hosted checks at this head: six runs completed with success (`receipts/hosted-checks-snapshot.txt`).
7. My own execution at the exact head, every run in disposable `git archive` copies under the packet's `scratch/`, using the simulator named in §7:
   - `tb/pp_top`, full (both builds): 7,875 checks, 0 failures (`receipts/pp_top-full-head.txt`). The D3 section has 120 checks.
   - Focused suites, all PASS: `acmp_nvm` 353, `nvm_port` 136, `desc_mem_guard` 78, `dyn_state` 118, `desc_store` 584, `lsn_admit` 18, `adp_engine` 533, `rx_validator` 437.
   - Documentation gates, all rc 0: `links` 967, `matrix`, `modmatrix`, `params` 26/26/26.
   - `--dr3a` reproduces the published figures: the per-byte device ends DEFAULTS 4 clocks after the bound.
   - The in-tree `d3_mutants.py`, from an exact-head copy with 8 jobs: **69 of 69 KILLED**, 3 goldens PASS. Every README "failing checks" figure equals my run (`readme-record-vs-run.txt`).
   - My round-2 probes and 15 mutants, rerun.
   - Three new reviewer mutants against the pre-proof path, and two new probe sets (E1, E2).
   - The parent's `nvm_cosim` quick loop and lint, in scratch parents (item 4, §3).
   - Focused re-counts of the parent's port-contract and naming ratchets.

The prior public findings on this PR are my R390-1/R390-2 findings (§4) and the other reviewer's R391-1/R391-2 findings (§9). I read R391-2 only after this verdict, the findings and the ledger (§6) were written.

## 2. Findings

### R390-3-F1: MAJOR. The aggregate's new binding-walk path can abort a read in the arbiter's issue cycle: the abort is lost, nothing drains the read, and the NVM port is wedged until reset with no alarm

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - `hdl/acmp/KL_acmp_nvm_shadow.sv:552-553`: `rs_tmo_w` now fires in `H_RS_STREAM` on `rs_stall_w && rs_agg_i`.
  - `:562`: that drives `nvm_abort_o`.
  - `:748`: the walk's read strobe `nvm_req_o` is **registered**, so it is presented in the first `H_RS_STREAM` cycle. No byte, done or err can be in hand in that cycle, so `rs_stall_w` is 1 there.
  - `hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:123`: the arbiter takes that strobe as `iss0_w`.
  - `:149-151`: it arms the drain only for `(own_r == O_M0) && m0_abort_i`. In the issue cycle `own_r` is still `O_NONE`.
  - `hdl/packet_engine/KL_pp_nvm_port.sv`, state `S_RHFWD`: the port then waits for `nvm_rready_i` with no exit on time. The walk, now in `H_RUN`, never raises it again.
  - Several places state the opposite ("an issued read goes to the drain"): `KL_acmp_nvm_shadow.sv:150-153` and `:541-544`, and `docs/architecture/07_memory_maps.md:615`.
- **Authority:**
  - D3 contract §5 rule 5 and §6.4: a read either manager abandons is DRAINED at the arbiter, never handed on.
  - The arbiter's own banner: an abandoned read is kept as the arbiter's own and ended only by its done or err.
  - The DR3a clarification (5876655419): at the bound the binding walk takes its own per-wait path. That path, at its own deadline, always meets an arbiter that already owns the read.
- **Evidence** (executed; `scripts/probe_r3.hpp` E1 and `scripts/run_probe_r3.sh`; receipt `probe-e1-lost-abort-head.txt`):
  - **Setup.** Every D3 record and every binding are saved. The device is slow per payload byte (12,422 clocks per byte, each wait inside the per-wait deadline), so the binding walk outlasts the bound. The previous binding record's done is held 6,055 clocks, so the 5th binding READ strobe lands on the first clock `agg_o` reads 1 (clock 1,000,000 of the harness loop).
  - **In that cycle:** strobe 1, `m0_abort` 1, arbiter owner NONE.
  - **Then:**
    - the restore itself ends DEFAULTS, cause 3, as ruled;
    - the drain never runs (0 drain cycles), and the port stays owned by the binding manager in `S_RHFWD`.
  - **Over the following 1,020 ms**, with the device fast again:
    - a SET is accepted, but the port is not idle for 100,000 of 100,000 cycles and the device sees 0 operations;
    - record 0x50 never persists, and `d3_unflushed_o` stays 1;
    - `nvm_alarm_o` stays 0, because no attempt ever starts without a grant.
  - **One clock either side** (the strobe one clock before `agg_o`, or one clock after it):
    - one clock before: the read is drained (3,005 drain cycles) and the SET persists;
    - one clock after: no read is issued, and the SET persists.
  - **Diagnosis check.** A disposable probe copy whose arbiter also arms the drain on `iss0_w && !m0_we_i && m0_abort_i` drains the aligned case and persists the SET (`probe-e1-arbiter-fix-probe.txt`). This was only to confirm the diagnosis; it is not a proposed patch.
  - **No suite grades it.** D3R14 lands the bound in a stalled mid-stream cycle; nothing aligns the bound with an issue cycle.
- **Impact:**
  - **When.** Any boot whose binding walk is still reading at the bound can hit it. It happens when a binding READ strobe lands on the bound's first fired clock, a one-clock coincidence.
  - **What happens.** On a healthy device the NVM port is quarantined until reset. Every later change of both producers is lost to the next power cycle.
  - **What is signalled.** Only pending (`pend_i`) is set; the reset-sticky alarm is not raised.
  - **Scope.** Round 3 introduced this path (`f8d1a83`). The per-wait path never fires in an issue cycle unless `RS_TMO_CYC_P` is 1.
- **Required outcome:**
  - A binding READ abandoned by the aggregate is drained whatever cycle it is abandoned in. For example:
    - the arbiter arms the drain on an abort presented with the issue (`iss0_w`);
    - or the walk does not take the aggregate path in the cycle its strobe is out, and takes it one cycle later, when the arbiter owns the read.
  - A named cycle-exact check: a binding READ strobe on the first clock of `agg_o`, graded as a drained read and a later SET that persists. It must fail under a mutant that restores the head's behaviour.
  - Keep the comments and 07 row true.
- **Verification:**
  - Rerun `scripts/run_probe_r3.sh` (E1) at the fix head. The aligned boot must show a drain and a persisted SET.
  - The new check must fail under its mutant.

### R390-3-F2: MINOR. The aggregate's expiry during the image proof, and on the proof's own clock, is ruled but ungraded: two reviewer mutants against the pre-proof path survive

- **Lens:** Tests.
- **Where:**
  - `hdl/aecp/KL_aecp_nvm_writer.sv:544` (`expire_w` gated by `proven_r`) and `:810` (`proof_w && agg_past_w`);
  - against the D3 section of `tb/pp_top` (D3R14 fires the bound only while the binding walk still runs).
- **Authority:**
  - The clarification: "It ends CLOSED only if the image cannot be proven".
  - The writer banner (`:62-73`) and 07 §5.3 ("the image proof under way … DEFAULTS once the image is proven, with no record read"; "a proof at or after it reads no record, whether the bound fired in a wait before it or lands on the proof's own cycle").
  - The round-3 focus: "expiry on the exact proof clock, expiry during the proof".
  - The 09 §7 rule that ruled behaviour is graded by a named check.
- **Evidence** (`scripts/r390_3_mutants.py`, `scripts/probe_r3.hpp` E2; receipts `r390-3-mutants.txt`, `probe-e2-*.txt`):
  - **E2 setup.** A late image is loaded after the store's reset walk, as D3O4 does, so the proof is a LOCATE that walks the store again (about 542 clocks). The binding walk is steered so the proof lands at a chosen offset from the bound.
  - **E2 at the head, all correct:**
    - the bound 271 clocks inside the LOCATE: DEFAULTS at the proof, cause 3, image valid, 0 D3 READs;
    - the proof on the bound's own clock: DEFAULTS, 0 READs;
    - the proof one clock before the bound: pass 0 starts, and the bound ends it DEFAULTS with its READ drained.
  - **`agg_closes_during_proof`** (the aggregate also aborts in `W_IMGLOC`):
    - it SURVIVES the D3 section (120/120);
    - under E2 the bound inside the LOCATE ends **CLOSED**, cause 3, with the image valid, AECP owned and ADP disabled. The entity stays dark until reset over a provable image, which is exactly what the clarification forbids.
  - **`proof_past_needs_fire`** (the proof-past rule keyed on the fired flag rather than the bound reached):
    - it SURVIVES the D3 section;
    - under E2 a proof on the bound's own clock starts pass 0 and issues 2 record READs past the bound (0 at the head).
  - My third mutant, `binding_agg_between_records_only`, is KILLED by D3R14.
- **Impact:** A regression that closes a provable image when the bound meets the proof passes every gate. So does one that reads records past the bound. The pre-proof path is graded on one of its three phases only.
- **Required outcome:** Named checks for:
  - a bound inside the image proof's LOCATE, which ends DEFAULTS with the image valid;
  - a proof on the bound's own clock, which reads no record.

  Each is killed by the matching mutant above.
- **Verification:** Rerun `r390_3_mutants.py agg_closes_during_proof proof_past_needs_fire` at the fix head: both KILLED by the new checks.

### R390-3-F3: MINOR. The PR body's pin-adoption list is incomplete, and its attribution of the `nvm_cosim` B1–B4 failures is inexact

- **Lens:** Docs.
- **Where:** The PR body, "Parent-visible changes in round 3 (pin adoption)" and the earlier rounds' lists.
- **Authority:**
  - The assignment's prefix rule ("No interface change beyond the declared ones"; every parent-visible change declared).
  - The manager's bank at this head (5880274287): the milan_dp items "join the list in this PR's 'Parent-visible for pin adoption' section".
  - The lane-2 scope record (5880276193).
- **Evidence** (receipts `nvm_cosim/*`):
  1. **A second `nvm_cosim` PINMISSING is not declared.** `nvm_cosim`'s `cosim_top.sv` instantiates `KL_aecp_dyn_state`, which since round 1's `4dd37c2` has the output `wr_chg_o`. Lint at base: 84 warnings, 0 PINMISSING. At this head: 86 warnings, including PINMISSING `wr_chg_o` (`cosim_top.sv:194`) and `rs_agg_i` (`:257`); rc 0 in both. The body names only `rs_agg_i` and "85 to 86".
  2. **The B1–B4 root cause is not the one stated.** `cosim_top.sv` instantiates `KL_acmp_nvm_shadow` directly and passes `RS_TMO_CYC_P` derived from its clock, but not `RETRY_BACKOFF_CYC_P`. The shadow's default is 50,000,000 clocks: 500 ms at 100 MHz, but **50 s** at the cosim's 1 MHz model clock. The body attributes the 7/315 to "the ruled backoff outlasting the scenario window".
     - **(A)** Tying `rs_agg_i` and passing the top's derivation, ceil(`CLK_HZ_P`/2), at the cosim's clock: every `later_record_persists@end:0x21` and all three power-cycle restores pass. Two `last_verified_kept@end:0x20` checks then fail (B1, B4). The case's 1,500 ms give-up window is shorter than the debounce plus two 500 ms backoffs, so the third attempt lands after the fault is cleared and succeeds.
     - **(B)** A, plus that window lengthened to 2,000 ms: **315 of 315**.
     - Receipts: `quick-expA.txt`, `quick-expB.txt`, `expA-cosim_top.diff`, `expB-cosim_cases.diff`.
  3. **Harness and firmware items are not in the body.** The manager's bank found `milan_dp` and `milan_dp_render` failing because those harnesses never set PP_CTRL[1] while AECP is held from reset. The lane-2 record adds the firmware path that skips the restore walk. The body does not list either.
- **Impact:** The pin-adoption lane, working from the PR body, would tie `rs_agg_i` and still:
  - carry an undeclared PINMISSING;
  - miss the backoff connection that actually repairs B1–B4;
  - miss the harness and firmware obligations.
- **Required outcome:**
  - The PR body's parent-visible list names:
    - `KL_aecp_dyn_state.wr_chg_o` in `cosim_top.sv`;
    - `cosim_top.sv`'s `RETRY_BACKOFF_CYC_P` derived from its clock, as the top derives `NVM_RETRY_BACKOFF_CYC_P`;
    - the B1–B4 give-up window versus DR2c;
    - the PP_CTRL[1] harness and firmware obligations the manager recorded.
  - The B1–B4 attribution is stated as measured.

  This is a body edit; no source change is needed.
- **Verification:** Compare the PR body with this list and with the manager's scope record 5880276193.

### Suggestions (they do not affect the verdict)

- **R390-3-S1 (Docs):**
  - **The claim.** `integrator.md:430-432` says the terminal follows the bound "within two [per-wait deadlines] when a roll-back runs after it", so a bounded wait should "cover 1,000 ms plus 40 ms".
  - **What the RTL allows** (`KL_aecp_nvm_writer.sv` `W_RB`/`W_RELOC`), after the aggregate's pass-1 abort:
    - the debt wait may stall `NVM_RS_TMO_CYC_P` − 1 clocks after its two-cycle minimum;
    - the re-LOCATE may stall another `NVM_RS_TMO_CYC_P` − 1;
    - so the terminal can land 2 × `NVM_RS_TMO_CYC_P` plus a few clocks after the bound.
  - **Firmware's clock starts earlier.** Firmware starts its clock at its PP_CTRL[1] write, before the processor accepts it.
  - **Suggested wording.** Say "more than 1,040 ms", or give a margin. I derived this from the code; it is not executed.
- **R390-3-S2 (Conformance, for the manager):**
  - **The case.** D3R15's re-LOCATE arm puts the bound about 100 clocks into a healthy re-LOCATE. That LOCATE would prove the image some hundreds of clocks later. The arm grades CLOSED with the pass-1 cause.
  - **Why the head's reading is admissible.** The contract's §6.2 table has "ABORT during the roll-back → CLOSED", and the clarification's roll-back bullet defers to §6.3.
  - **Why it is in tension.** It conflicts with the clarification's headline, "an aggregate expiry never closes a provable image".
  - **Scope.** The window needs a pass-1 fault within one roll-back of the bound, and the author stated this reading for review.
  - **Suggested action.** An explicit manager confirmation (§8).
- **R390-2-S1 (RTL, Docs), carried:** No `RX_SLOTS_P >= 2` floor is checked or stated. At `RX_SLOTS_P = 1` the hold admission leaves no slot to the other protocols.

## 3. Round-3 assignment items verified

| Item | Result | Evidence |
|---|---|---|
| (1) `f8d1a83`: before the proof the aggregate aborts nothing. A binding walk still reading takes its own per-wait path through `rs_agg_i`, fails whole and releases the listener (`restore_cause_o` 3, every binding at its default, nothing preloaded). The D3 walk proves the image, reads no record and ends DEFAULTS cause 3. CLOSED only for an unprovable image (7) or a pass-1 roll-back that cannot prove it again | **met in the terminals; F1 for the binding walk's issue cycle; F2 for the ungraded proof edges** | See the item (1) edges below this table. |
| (2) `9d66095`: both guides state every aggregate terminal and both CLOSED causes, matching 07 §5.3 | **met** | See the item (2) detail below this table. |
| (3) D3R15, D3R16/D3R17, D3O7 kill `agg_not_in_rollback`, `agg_not_stopped_at_terminal`, `agg_fires_with_event_in_hand`, `resident_never_returned`; 69 of 69 KILLED; one mutant of my own against the pre-proof path | **met; F2 for my own mutants** | See the item (3) detail below this table. |
| (4) PARENT CONSEQUENCE: `nvm_cosim` quick 7/315 from `f72a2d2` on. Prove or refute that no write is lost | **reproduced; no write is lost; the contract admits the loss the head's harness shows, and it is signalled as pending** | See the item (4) detail below this table. |
| (5) DR4 lane 1 +1,030 LUT / +559 FF / 0 BRAM; the pin-adoption changes listed completely in the PR body | **DR4 declared as required (not re-measured, §7); the list is incomplete: F3** | See the item (5) detail below this table. |

**Item (1) edges.**
- **Probe D1** (my round-2 per-byte device, every binding saved): DEFAULTS at clock 1,000,005 against the bound's 1,000,001. Binding cause 3, AECP released, ADP enabled, a READ_DESCRIPTOR answered (`probe-d1-slow-binding-walk-head.txt`). Round 2 ended CLOSED here.
- **The same device over erased media:** DEFAULTS at clock 1,000,544, rolled back, as in round 2.
- **Expiry during the proof, and on the exact proof clock:** correct at the head (E2, see F2).
- **Expiry with an event in hand:**
  - in the D3 walk, D3R17 grades it, and my probe C1 is unchanged: seven forced grants around the bound all end DEFAULTS at clock 1,000,001, drained, with a later SET persisting;
  - in the binding walk, the path fires only in a stalled cycle. Mid-stream that is correct, but the issue cycle is always stalled: F1.
- **A pre-proof expiry followed by an unprovable image:** D3R14's refused arm ends CLOSED cause 7. The aggregate aborted nothing, so the image fault is the first abort and names the restore. I agree with the author's reading.
- **The firmware bounded wait of 1,000 ms plus 40 ms:** the pre-proof path ends within one per-wait deadline of the bound (the proof's own LOCATE); a pass-1 roll-back within two, plus a few clocks (S1). The binding walk's preload phase cannot stretch it: the admission gate takes a preload the cycle it is presented.
- **The roll-back:** probe C2 is unchanged. A pass-1 error 300 clocks before the bound ends CLOSED at the bound, cause 2; 3,000 clocks before, it ends DEFAULTS rolled back (S2).

**Item (2) detail.**
- **Integrator guide:**
  - the parameter row lists the terminals: the binding walk still reading, pass 0, pass 1, and CLOSED only for the image or inside a roll-back;
  - step 3 has the CLOSED paragraph with two causes (7; the pass-1 cause 1, 2, 3, 5 or 6 with `restore_rb_o` 0) and the aggregate list;
  - §4.1 no longer calls the debt hold deferred.
- **Operator guide:** the outcome table has two aggregate DEFAULTS rows and two CLOSED rows; the CLOSED paragraph and the troubleshooting row give both causes and state "a slow device alone ends on defaults, never here".
- **Consistency:** all of this agrees with the 07 §5.3 table at this head, including the roll-back row's "the pass-1 abort's" cause.
- **Diagram 23:** changed with its PNG. I did not re-render it.
- **Gates:** `links`, `matrix`, `modmatrix` and `params` pass.

**Item (3) detail.**
- **The in-tree driver, from an exact-head copy:** 69 of 69 KILLED, with the named checks: D3R15 both arms, D3R16 three arms, D3R17 two checks, D3O7 (`d3-mutants-from-tree.txt`).
- **My R390-2 mutants at this head** (`r390-3-mutants.txt`):
  - `agg_not_in_rollback` is KILLED by D3R15, and `agg_ignores_in_hand` by D3R17;
  - the other 11 KILLED on the D3 section as before;
  - `hold_after_release` is KILLED by the full suite (W21dd2, W21ee, U11g), as in round 2;
  - `held_gate_ignores_da` has no effect, as judged in round 2.
- **My own round-3 mutants:** `binding_agg_between_records_only` is KILLED by D3R14; `agg_closes_during_proof` and `proof_past_needs_fire` SURVIVE (F2).

**Item (4) detail.**
- **Scratch parents.** Dev `b5c0f69d`, with the processor and gPTP submodules checked out from their sources at the named revisions. Never committed.
- **Reproduced.**
  - Base `c951a9ff`: 315/315.
  - This head: 308/315. The seven failures are exactly B1–B4 `later_record_persists@end:0x21` and `R_power_cycle~B1/B2/B4` `restores_last_verified`.
  - In those runs, at the `end` snapshot, `pend` is 1 and `mgr_dirty` is 3. The later change is **reported pending, never durable**, when the power cycle takes it (`B-obs-cbbb5acc.txt`).
- **Extended past the backoff, with the shipped wrapper's own 50 s default** (only `rs_agg_i` tied; the B cases' give-up window lengthened from 1,500 ms to 101,000 ms of model time): **315/315**. Every later record persists and restores after the power cycle (`quick-expC.txt`, `expC.diff`, `B-obs-expC.txt`).
- **With the ruled 500 ms at the cosim's clock:** see F3 (A: 311/315; B: 315/315).
- **No write is lost.** A change made during another record's backoff is delayed, not dropped.
- **The contract question.** The ruled contract admits losing a change to a power cycle while it is still pending:
  - DR2a: "No unconditional durability promise".
  - §7: a dirty bit clears only on the done of the WRITE that carries it.
  - §6.1: BACKOFF waits 500 ms before re-acquiring the same record, three attempts in all. Another record's change therefore waits at most two backoffs plus the attempts, about 1 s at the product clock.
  - Throughout that wait `pend_i` stays 1, so no durability is ever claimed.
- **Why the window looks so long here.** Only the harness wrapper, which bypasses the top's derivation, stretches that window to 100 s. The top passes ceil(`CLK_HZ_P`/2) (`protocol_processor_top.sv:151`, `:2557-2560`).

**Item (5) detail.**
- **DR4.** The PR body states lane 1 at +1,030 LUT / +559 FF / 0 BRAM / 0 DSP (round 3 +9/−1), inside the 2,500/1,400 ceiling. The 8x8 figures are diagnostic, and post-place is lane 2's.
- **The declared items.** The `rs_agg_i` tie, the five round-1 ports, `NVM_RS_AGG_CYC_P`, `NVM_RETRY_BACKOFF_CYC_P`, snapshot word 37 and the classifier row are declared.
- **The missing items:** F3.

## 4. My earlier findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R390-2-F1 (MAJOR, a pre-walk aggregate expiry ends CLOSED over a valid image) | **RESOLVED** | Option (a), as clarified. Probe D1 ends DEFAULTS at 1,000,005 with AECP released and ADP enabled. The named control D3R14 kills the pre-walk-close mutant (my run). F1 and F2 are new findings on the new path. |
| R390-2-F2 (MINOR, the guides misstate the aggregate terminals and CLOSED) | **RESOLVED** | §3 item (2) |
| R390-2-F3 (MINOR, the roll-back span ungraded) | **RESOLVED** | `agg_not_in_rollback` is KILLED by D3R15 (both arms), in the in-tree driver and in my own script |
| R390-2-S1 (RX_SLOTS_P floor) | **not taken**; carried as a suggestion | `protocol_processor_top.sv:86`, no elaboration check |
| R390-2-S2 (grade or state the in-hand guard) | **TAKEN** | D3R17 lands the writer's grant on the bound's own clock; `agg_ignores_in_hand` is KILLED |
| R390-1-F1…F4, S1, S2 | **still RESOLVED/TAKEN** | My round-1 probes (hold admission, G1/G2) give output identical to round 2 (`probes-r2-head.txt`), and the round-1 mutants are still KILLED |

## 5. Parent-visible change audit

- **Top ports and parameters.** The parent's `sv_ports` parser finds 1,741 ports at this head, 3 more than at `2b38d68e`: the engine's `d3_agg_o`, the writer's `agg_o` and the shadow's `rs_agg_i`. All three are documented, and no top port or parameter changed in round 3.
- **Ratchets.**
  - Undocumented processor ports: 111 at base, at `2b38d68e` and at this head (≤ the budget's 111).
  - Naming: 22 candidates, 0 outside the budget (`port-doc-count.txt`, `naming-check.txt`, with the parent's scripts from `b5c0f69d`).
- **Declared in the PR body:** the aggregate terminals, `rs_agg_i` for `nvm_cosim`, and the earlier rounds' items.
- **Not declared:** the items in F3.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | clarification 5876655419 and ratification 5873060660; D3 contract §§5, 6.1–6.4, 7; DR2a/DR2c rulings; the writer's pre-proof path, the shadow's `rs_agg_i` path, the arbiter drain; `nvm_cosim` against DR2c | R390-3 | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` |
| RTL | UNCLEAN (F1) | every RTL hunk of the delta (writer `expire_w`/`agg_past_w`/`proof_w`/`agg_o`, shadow `rs_tmo_w`/`nvm_abort_o`, engine and top wiring), plus the arbiter and port they drive | R390-3 | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` |
| Robustness | UNCLEAN (F1) | E1 issue-cycle alignment with ±1 controls and a diagnosis probe; E2 bound inside and on the proof; D1 per-byte device; the C1/C2/A/B/G probe sets; nvm_cosim extended past the backoff | R390-3 | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` |
| Tests | UNCLEAN (F1, F2) | full `tb/pp_top` 7,875 and D3 section 120; 8 focused suites; in-tree driver 69/69; 15 round-2 and 3 round-3 reviewer mutants; README record equality 69/69; nvm_cosim quick at base, head and three scratch variants | R390-3 | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` |
| Docs | UNCLEAN (F1, F3) | 01, 03, 07, 08, 09 and diagram 23 diffs; integrator and operator guides against 07 §5.3; shadow and writer banners; suite READMEs; PR body parent-visible lists; `links`/`matrix`/`modmatrix`/`params` gates | R390-3 | `cbbb5acc77e9e068c3313d78ed4c1e5e79299a71` |

## 7. Real limits of this review

- **Tooling.** The requested simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used the same pinned Verilator 5.050 image as in round 2, through `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` (hashes in `receipts/tool-identity.txt`). The system 5.052 was not used; `nvm_cosim` ran with the same pinned binary first on its `PATH`.
- **Parent runs.** They were focused runs of `nvm_cosim` quick and lint in scratch parents at dev `b5c0f69d`, whose submodules I checked out from their sources. These are not the manager's consumer bank.
  - I did not run `milan_dp`, `milan_dp_render`, `pp_shadow`, xvlog or the evidence classifier. F3's harness and firmware items rest on the manager's bank (5880274287) and scope record.
- **Not run in the processor:** the full processor bank, `lint_hdl.sh`, Yosys/OOC (DR4 is not re-measured), and `make check`'s `lint`/`wavedrom-check`/`stale`.
- **Probe models.**
  - E1 and E2 add knobs to disposable bench copies: a hold on one payload READ's done, and debug taps. D1 uses the head's native per-byte knobs. The tree is unchanged.
  - S1's worst case is derived from the code, not executed.
- **No hardware.** No hardware or physical calibration was used. Field skips are not hardware proof.
- **Hosted checks.** At 23:23Z the six check runs at this head had completed with success (`docs-gates`, `portability`, `suites`, two each). The combined status has no contexts. Hosted acceptance is the manager's.

## 8. Pending manager duties

- **Merge-turn builds.** The donor full bank and the parent consumer bank at this head are published (5880274287). The final current-dev candidate (source base `c951a9ff`, live dev `b5c0f69d`) is built at the merge turn.
- **Evidence.** The public evidence at `b657a2de` `review-evidence/pp131-r1` is round-1 author material. Publishing the exact-head evidence remains with the manager.
- **Rulings:**
  - on S2 (a bound inside a healthy re-LOCATE ends CLOSED);
  - on the `nvm_cosim` reconciliation (5880276193 item 3), for which §3 item (4) and F3 give the measured causes: the wrapper's backoff parameter and the give-up window.
- **Lane 2 (pin adoption):**
  - the five round-1 ports, `NVM_RS_AGG_CYC_P` and `NVM_RETRY_BACKOFF_CYC_P`;
  - snapshot word 37;
  - the `d3_mutants.py` classifier row;
  - `rs_agg_i` and `wr_chg_o` in `cosim_top.sv`, and its `RETRY_BACKOFF_CYC_P`;
  - the PP_CTRL[1] harness and firmware items;
  - DR4 post-place, and the 8x8 obligation (open, not waived).

## 9. Prior public findings of the other reviewer, resolved or retained at this head

I read R391-2 (5876927371) only after §§2–6 were written; for R391-1 I rely on my round-2 disposition, rechecked here. Reading them changed no finding and no ledger entry. R391-2 F1's orphaned-READ concern is on the writer's `W_RQ` path, which D3R17 now grades. My F1 is a different path: the binding walk's issue cycle.

| Finding | Status at this head | Evidence (mine) |
|---|---|---|
| R391-2 F1 (MINOR, post-terminal inertness and no-event-in-hand firing unguarded) | **RESOLVED** | `agg_not_stopped_at_terminal` is KILLED by D3R16 (COMPLETE, DEFAULTS, CLOSED arms), and `agg_fires_with_event_in_hand` by D3R17, in my in-tree run. My own equivalent `agg_ignores_in_hand` is KILLED by D3R17. |
| R391-2 F2 (MINOR, a WAIT-GO expiry ends CLOSED; the integrator guide says defaults) | **RESOLVED** by the clarification's option (a) | The per-byte device (probe D1, the same shape as that reviewer's P8 case A) ends DEFAULTS at 1,000,005, AECP released, ADP enabled. The guides and 07/08 state the new terminals (§3 item 2). My F1 and F2 are new findings on the new path. |
| R391-2 S1 (the resident count's decrement ungraded) | **TAKEN** | D3O7; `resident_never_returned` is KILLED in my in-tree run |
| R391-1 F1 (MAJOR, the aggregate not implemented) | **still RESOLVED** | The counter, the derivation and D3R13 are unchanged in effect: `agg_removed`, `agg_one_late` and `agg_restarts_on_go` are KILLED, and `no_aggregate_deadline` is KILLED in the in-tree run |
| R391-1 F2 (MAJOR, held AECP exhausts the RX slots) | **still RESOLVED** | My hold-admission probes give the same output as in round 2. D3O5/D3O6/D3O7 kill the admission mutants. |
| R391-1 F3 (MINOR, four delayed or boundary behaviours unguarded) | **still RESOLVED** | `pass1_read_not_drained`, `judge_wait_unwatched`, `rate_walk_stuck_on_first_lane` and `rate_walk_unbounded` are KILLED in my in-tree run |
| R391-1 F4 (MINOR, port-contract ratchet and naming) | **still RESOLVED** | 111 ≤ 111; 0 new naming identities (§5) |
| R391-1 S1 (one conversion, two roundings) | **still TAKEN** | `NVM_RS_TMO_CYC_P` is ceil(`CLK_HZ_P`/50), unchanged |

## 10. Receipts and reproduction

- Every publishable file is listed in `MANIFEST.sha256`. Paths are relative to the packet, and host paths inside receipts are replaced by `<packet>`, `<clone>` and `<V>`.
- **Clone integrity** (`receipts/clone-integrity.txt`), after all probes:
  - HEAD and tree verified;
  - porcelain status (ignored and untracked included), `diff-index` and worktree diff all empty;
  - 0 blobs and 0 modes differ from the index;
  - 0 gitlinks and no `.gitmodules` (the repository has no submodules);
  - `ls-files -s` sha256 `bceb6da4…452b`.

  One ignored bytecode cache, written when I imported `d3_mutants.py` from the clone, was removed before the check.
- **Reproduce**, with `<clone>` the review clone, `<V>` the simulator, and `<copy>` a fresh `git archive` copy per run:
  - Full suite: `make VERILATOR=<V>` in `<copy>/tb/pp_top`; then `--dr3a`.
  - Focused suites: `scripts/run_focused_suites.sh <clone> <out> <V>`.
  - In-tree driver: `python3 tb/pp_top/d3_mutants.py --output <dir> --verilator <V> --jobs 8` from a copy.
  - Reviewer mutants: `python3 scripts/r390_3_mutants.py <clone> <scratch> <V> [name …]`.
  - E1 and E2: `scripts/run_probe_r3.sh <packet> <copy> <V>` (`PROBE_E2_ONLY=1` for E2 alone). E2 on a mutant: run it on that mutant's copy.
  - D1: `scripts/run_probe_r2d.sh <packet> <copy> <V>`.
  - Round-1/2 probes: `scripts/run_probes.sh <packet> <copy> <V>`.
  - `nvm_cosim`:
    - in a scratch parent at `b5c0f69d` with `protocol-processor` checked out at the revision and `gptp-processor` at its gitlink, run `make quick` and `make lint` in `tb/verilator/nvm_cosim` with `<V>` first on `PATH`;
    - apply `receipts/nvm_cosim/exp*.diff` for the variants.
  - Ratchets: `python3 scripts/port_doc_count.py <parent>/scripts <clone> <revs…>`; `python3 scripts/naming_check.py <parent>/scripts <clone> <revs…>`.

R390-3 FINISHED
