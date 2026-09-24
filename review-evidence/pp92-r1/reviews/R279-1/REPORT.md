[R279] NEGATIVE - exact head 156c206cbaedf721f7caef5c94faa21876a28c32

# R279-1: external independent review of PR #109 (processor issues #92 and #93)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #109, branch `92-93-boot-restore`.
- Exact head `156c206cbaedf721f7caef5c94faa21876a28c32`, tree `a1c45f5e7949764ad008c04ff66ca3494db97a5e`. Verified in an isolated detached clone before and after every probe (`receipts/01-clone-identity-before.txt`, `receipts/04-clone-identity-after.txt`).
- Source base `fbc1f7156d711e5b7f511da8a16d9494256b017b`. Author head `3691340c`. Merge of main `09f9bf38` (PP #107) is `69a6eac2`. The five idiom commits `ad9d156`..`156c206` follow it.
- Reviewer role: external independent reviewer, cleared context. Public review start: PR #109 comment 5807226156.

## Verdict

**NEGATIVE.** Within the boot window, the product changes do what #92 and #93 ask. I found no RTL defect in the admission gate, the port's cause register, the walk deadline or the drain arbiter themselves:

- The #92 binding loss in the window is removed, and the pinned-wiring control reproduces it.
- The S1/S3/S4 behaviour matches the issue's acceptance.
- Every failing arm the author published, or that I reproduced, reddens a completed-scenario assertion.

The shadow's failed-walk path still loses saved bindings (F3, below).

Two MINOR findings from my own pass remain open, and each leaves a lens unclean:

- **F1 (Docs):** the operator and integrator guides still say an unwired NVM backend reports "done, no fail", like a successful restore. At this head it reports restore FAILED.
- **F2 (Tests):** the top-level `restore_done_o`/`restore_busy_o` composition this PR adds (the "no enable before the last preload's write and arm" contract) has no failing arm. Deleting either term leaves every suite green.

**F3 (MAJOR)** also stands. After a walk fails, for any cause and so also through the DEVICE and deadline routes this PR adds, one read-only GET_RX_STATE of a sink stored before the failure rewrites that sink's saved NVM record unbound. The next healthy boot does not restore it. My own pass missed this. The concurrent internal review (R278) published it while this round was running. I read that report only after this verdict and ledger were first written, then reproduced it independently with my own probe, for all three causes. It is recorded here as confirmed, not re-derived, and the ledger was updated for it (see "Order of work").

Six SUGGESTIONs are listed. They do not affect the verdict.

## Reconstruction order and sources (all public)

1. No `AGENTS.md` or `CONTRIBUTING.md` exists in the repository. Contributor rules come from `docs/README.md` and `.github/workflows/hdl.yml`:
   - single-source `F01.5`/`F08.1`;
   - one home per figure;
   - `make check`;
   - a CI-pinned simulator 5.050, with `lint`, `run_suites`, `gen_matrix --check`, the nvm_port figures gate and the yosys portability job.
2. The issue #92 and #93 bodies, the A10 assignment comments, the A218 REVIEW READY comments and the A225 idiom comment.
3. The PR #109 body and comments: at reconstruction, two review-start notes and no review findings.
4. Linked authorities, read at their pinned commits:
   - milan-fpga `docs/design/SAVED_STATE_FASTCONNECT.md` @2d8fd62 (sections 6 and 9, including the erased-record rule and the blank-flash responder);
   - `docs/design/SAVED_STATE_MATERIALIZATION.md` @2a2007c;
   - the T8 draft @c1ee27d;
   - Milan v1.2 5.3.8 as cited by the processor docs (5.3.8.2/5.3.8.3 bound state and binding parameters).
5. `git diff fbc1f71..156c206` and its history:
   - the merge is clean and file-disjoint;
   - the idiom commits touch `tb/` only (`receipts/02-history-checks.txt`).
6. Public executable evidence: milan-fpga @94ccff2 `review-evidence/pp92-r1` (the author, idiom-a225 and manager-r2 trees).

## Findings

### F1 - MINOR - Docs

**Location:**
- `docs/guides/operator.md:210-213`
- `docs/guides/integrator.md:224` (the first sentence of the NVM tie-off cell)
- secondary: `docs/guides/integrator.md:215-217` and the `docs/diagrams/21-integration-faces.svg` tie-off rule

**Authority/evidence:** this PR's own S1/S3 contract (07 §5.3 table, `hdl/top/protocol_processor_top.sv:431-437`). Both guides predate it and still read:

- operator.md: "a device whose NVM is blank — or whose integrator never wired a backend at all — publishes the same two bits as one that restored every sink".
- integrator.md: "a walk over an unbacked face raises `restore_done_o` with no `restore_fail_o`, exactly like a successful one".

Reviewer probe `scripts/probe_unwired.py` (`receipts/probe-unwired.log`) adds two cases to a scratch copy of `tb/acmp_nvm`:

- **P1**, a face that never grants: done=1 fail=1 blank=1 cause=3 at the deadline, with the port quarantined.
- **P2**, a face that answers every READ with err: done=1 fail=1 blank=1 cause=2.

The suite stayed 332/332 alongside the probes. The same integrator cell goes on to state the new rule ("an unbacked face must still answer ... as erased media"), so the cell contradicts itself. The §7 heading promise "it never wedges the control plane" no longer holds for a literal tie-off that also leaves `restore_go_i` low: the ACMP listener then never serves.

**Impact:**
- An operator bringing up a board with no backend reads control word 1 bit 3 (restore failed) while the guide says to expect done without fail.
- An integrator following the first sentence of the tie-off cell ties the face off expecting a success-shaped walk.
- This is exactly the consumer impact the manager flagged ("a blank device must deliver 0xFF; error/early-done now fails restore").

**Required outcome:** reword operator.md §6 and the integrator tie-off cell so both guides say the same three things:
- a face answering as erased media reads done, no fail, blank;
- a face that errs, or ends a header short, fails the walk (cause 2);
- a face that never answers fails at `T-NVM-RS-DEADLINE` (cause 3) and quarantines the port.

Also qualify the §7 "never wedges" sentence, or the figure-21 tie-off note, for `restore_go_i`.

**Verification:** re-read both guides against 07 §5.3's table. Optionally, keep a P1/P2-style case in `tb/acmp_nvm` that grades the unwired face's pins.

### F2 - MINOR - Tests

**Location:**
- `hdl/top/protocol_processor_top.sv:2498-2500`: `restore_done_o = nvm_walk_done_w && lsn_released_w` and `restore_busy_o = nvm_walk_busy_w || (nvm_walk_done_w && !lsn_released_w)`.
- `tb/pp_top/sim_main.cpp:8549` claims "The level itself is graded in S0".

**Authority/evidence:**
- 05 §5.1, table row "The release is the binding walk's end": "an entity enable gated on `restore_done_o` cannot precede the last preload's record write and discovery arm". The integrator guide step 3 says the same.
- Issue #93 S4: "`restore_done_o` ... takes it. No enable can therefore precede the last preload's record write and discovery arm."

Reviewer mutants on pp_top, the only suite that instantiates the top (the acmp_nvm wrap feeds the shadow's raw terminal into its gate, `tb/acmp_nvm/acmp_nvm_wrap.sv:403`):

| Mutant | Change | pp_top result |
|---|---|---|
| R1 | `restore_done_o = nvm_walk_done_w` | 1427/1427 PASS, SURVIVED |
| R2 | `restore_busy_o = nvm_walk_busy_w` | 1427/1427 PASS, SURVIVED |

Receipts: `receipts/mutants/R1.log`, `R2.log`. S0 checks only `done==1 && busy==0` long after the walk, and BW waits on the level without grading its cycle. In the shipped timing the shadow's terminal rises while the listener's A4 strobe is still up, so R1 does let the top's done precede the discovery arm. The property is real and cycle-observable, but no test sees it.

**Impact:** a correction line of this PR (its interface contract at the top) has no failing arm. The PR claims "Every correction's failing arm", and the suite comment says it is graded. A future edit can silently drop the ordering the integrator relies on.

**Required outcome:** grade the level in `tb/pp_top` cycle by cycle:
- `restore_done_o` implies the gate is released, and it is 0 in every cycle in which the walk's terminal is up but the gate still owns the faces;
- `restore_busy_o` covers that gap.

Either publish the gate's `own_o` (or `released_o`) as a wrap tap, or check against `dbg_walk_done_o` and the listener's A4 strobe. Correct the S0 comment.

**Verification:** R1 and R2 each redden a named pp_top check. The suite is green at the fixed head.

The concurrent R278 report records the same finding as its F2. The two reviews reached it independently: this finding and its R1/R2 receipts were written before that report was read.

### F3 - MAJOR - Conformance, RTL, Robustness, Tests, Docs (confirmed from the concurrent R278 F1)

**Location:**
- `hdl/acmp/KL_acmp_nvm_shadow.sv:314-315` (`c1_diff_w` compares a capture with the RAM image and `valid_r`).
- `hdl/acmp/KL_acmp_nvm_shadow.sv:580-584` (the atomic reject clears `valid_r` only; the stored fields stay in the shadow RAM).
- `hdl/acmp/KL_acmp_nvm_shadow.sv:516-523` (this PR routes a zero-byte DEVICE err, `rs_dev0_w`, and the deadline, `rs_tmo_w`, into that reject).
- Docs: `docs/architecture/07_memory_maps.md:388-392` ("A read-only command that arrives during the walk is answered from the restored image afterwards and changes nothing here"), `docs/architecture/05_acmp_engine.md:165-169`.
- Tests: `tb/acmp_nvm` N1-N3 and `tb/pp_top` BW3 never grade NVM after the post-failure GET of a stored sink.

**Authority:**
- Issue #92 objective and acceptance 1-2: a read-only GET_RX_STATE must not erase or replace a saved binding, and a subsequent reset restores the same binding.
- Milan v1.2 5.3.8 saved binding parameters.
- The PR's own 07 §5.3 text quoted above.

**Evidence:** reviewer probe `scripts/probe_failed_walk.py` (`receipts/probe-failed-walk.log`), my own code, independent of R278's scripts. In a scratch copy of `tb/acmp_nvm` (the real listener, gate, shadow, arbiter and port), sinks 0 and 7 are saved and the walk fails after sink 0 was stored:

| Cause | How the walk fails | After one read-only GET of sink 0 | Next healthy boot |
|---|---|---|---|
| 2 | device err on sink 3's header read | 1 erase + 1 write; sink 0's record no longer byte-exact; valid byte 0x03 → 0x00 | valid 0x80: sink 0 not restored |
| 3 | sink 3's header read held until 2,000 cycles after the abort | same | same |
| 1 | sink 7's payload torn after 5 bytes | same | same |

Before the GET, NVM still held sink 0 in every case. With the three failure cases appended the suite reads 335/341, and all six failures are the probe's own checks. The mechanism, read in the RTL: the reject leaves sink 0's restored fields in the RAM with valid 0. The released listener writes back its default, unbound record, and `c1_diff_w` sees the field difference as a live change. It then dirties the sink and flushes a valid=0 record over the saved one.

**Attribution:** causes 2 and 3 are new routes into the reject added by this PR (at the base, a zero-byte err was a per-record default and there was no deadline). The torn route (cause 1) predates it.

**Impact:** a transient device error, or a device silent for `T-NVM-RS-DEADLINE`, during a later record's read now causes the permanent loss of every earlier saved binding on the first read-only poll of that sink. That poll can be a GET held from the boot window or any later controller poll. This is the #92 defect class, reached through the paths #93 adds. It contradicts 07 §5.3 as landed.

**Required outcome:**
- After a failed walk of any cause, a listener write-back that only restates the default must not be persisted over saved records. For example, the reject could reconcile the RAM image of each rejected sink with the default, or the capture compare could ignore field-only differences between two unbound records.
- Alternatively, record an explicit owner decision that a failed walk forfeits saved bindings on first touch, and state it in 07 §5.3, 05 §5.1 and the operator guide.
- Fix the torn route by the same change, or split it to its own issue with a recorded decision.
- Add discriminating regressions for causes 1-3, each with a failing arm: acmp_nvm grading NVM bytes after the GET plus a healthy-reset round trip, and pp_top BW3 or a sibling grading NVM before any BIND.

**Verification:** `scripts/probe_failed_walk.py` is 341/341 at the fixed head. The new regressions redden with the correction removed. acmp_nvm, pp_top and the manager's banks stay green.

### SUGGESTIONS (do not affect the verdict)

- **S1 (Tests):** each work face's wiring at the top is graded only through the acmp_nvm wrap's transcription of it. Reviewer mutants R8 (talker valid bypassing the gate at `protocol_processor_top.sv:1820`), R9 (START/STOP valid, `:1832`) and R10 (expiry, `:1848`) leave pp_top 1427/1427 green. Only the transaction face and the whole-gate deletion are graded at the top (BW1/BW2). The issue accepts "the acmp_nvm suite's wrap, or pp_top", so this is not a finding. A BW case with a talker event, or a START/STOP, in the window would close it.
- **S2 (Tests):** a device err in the same cycle as done, or with done already seen, on a header that fails the gate is DEVICE in the RTL (`KL_pp_nvm_port.sv:394`, correct per S1 "error in any state"). No case pins it: reviewer mutant R6 (drop `!dev_err_i`) leaves nvm_port 136/136 green.
- **S3 (RTL/Robustness, latent):** `KL_pp_nvm_mgr_arb`: manager 0 reads busy in manager 1's grant cycle (`:166`), so a manager 1 that re-requests back to back starves manager 0. The walk still ends at its deadline, but binding flushes would wait. Reviewer mutant R5 (H_RS_REQ stall ignoring the done/err cycle) survives only because no case runs manager 1 back to back. Unreachable at this head (manager 1 is tied idle). State it in 02 §8.2, or give manager 0 a turn, before the saved-state writer lands.
- **S4 (Docs):** `docs/diagrams/20-rtl-dataflow.svg` gained the gate and arbiter, but the committed render `20-rtl-dataflow.png` (kept "so a wiki can show them", commit 2ca216e) still shows the old chain. The render checks clean visually (reviewer render).
- **S5 (Docs):** the shadow's port comment `KL_acmp_nvm_shadow.sv:131` still says `restore_fail_o` means "torn read-back". The banner and the top say torn, device or deadline.
- **S6 (RTL/Docs):** at the top, `restore_fail_o` and `restore_blank_o` are the shadow's levels. They can read 1 for up to four cycles while `restore_done_o` is still 0 and busy is 1 (side-port word 1 transiently fail=1, done=0). The guides say to read them after done, so this is harmless. Gating them with the release, or saying "valid with `restore_done_o`", would make the pins self-consistent.

## Lens evidence

### Conformance

- **#92 acceptance 1** (a read-only GET_RX_STATE anywhere in the window keeps the binding): graded by L05a-f and L05s (every presentation cycle, both sinks), L04 and pp_top BW1. The pinned-wiring control reproduces the recorded failure: `make pinned` gives 96 of 332 FAIL, including L05a "sink 0 holds 000000000000000000000000" (`receipts/focused-head/acmp_nvm_pinned.log`). **Met.**
- **#92 acceptance 2:** the real listener, gate, shadow, arbiter and port are graded in the wrap (reply byte-exact, preload take cycle, record, NVM, reset round trip); pp_top BW0-BW2 cover the real top. **Met.**
- **#92 acceptance 3:** L09, L10, L20-L22, pop == take on every face. **Met.**
- **#92 acceptance 4:** the discriminating regression without a timeout verdict: acmp_nvm LG01/pinned and pp_top LG01 (5 of 1,407 default build, BW1/BW2). **Met.**
- **#92 acceptance 5:** the contract is recorded in 05 §5.1 and 07 §5.3. The gates were re-run here (below).
- **#93 S1:** the port cause matches the table (DEVICE for grant/header/short/wait/payload/erase errors; UNFRAMED only on a whole header refused, or a bad commit header; 3 never produced). The shadow takes a zero-byte err as the default only on UNFRAMED; a zero-byte DEVICE err fails the walk (cause 2).
- **#93 S3:** the no-progress deadline covers H_RS_REQ and H_RS_STREAM. Expiry fails the walk (cause 3) and aborts only an issued read. The arbiter drains until the operation's own done or err and never ends it on time. #15 (port deadline/cancellation) is correctly left open and documented.
- **#93 S4:** the gate matches the issue's rules exactly:
  - hold both valid and ready on the transaction and talker faces;
  - mask the START/STOP valid and pass its completion;
  - refuse and count expiries;
  - release once, on terminal ∧ ¬pre_valid ∧ ¬busy ∧ ¬arm, one-way until reset.
- **Saved-state contract:** the processor's per-record default on 0xFF media (UNFRAMED) agrees with FASTCONNECT's blank-flash responder and erased-record rule. The parent consumer gates at dev 26d855a9, with the gitlink at 156c206c, pass (manager-r2: pp_shadow 371 checks, builder test, idiom and xvlog ratchets; one calibration arm NOT RUN).
- **Milan v1.2 5.3.8:** a restored binding enters PRB_W_AVAIL and arms discovery before any live command is served. A read-only command answers the restored binding, and a BIND/UNBIND issued later still wins.
- Conformance findings: none from my own pass (the docs contradiction is F1, under Docs). F3, confirmed afterwards, breaks #92's objective after a failed walk.

### RTL

Reviewed in full: `KL_pp_acmp_lsn_admit.sv`, `KL_pp_nvm_mgr_arb.sv`, and the diffs of `KL_acmp_nvm_shadow.sv`, `KL_pp_nvm_port.sv` and `protocol_processor_top.sv`, plus the listener's handshakes, the preload path and the START/STOP holder.

- **Port:** `refuse_w` equals exactly the port's two refusal transitions. `cause_r` is sampled on the transition into S_FIN and gated by err.
- **Shadow:**
  - `rs_stall_w` excludes rvalid, done and err, so no expiry coincides with a terminal or a byte. The count is consecutive and clears on progress.
  - Abort fires only in H_RS_STREAM, where manager 0 always owns the port.
  - A failed walk goes to H_RUN with `any_rec` cleared, so it reports blank.
  - The walk never re-enters H_WAIT.
- **Arbiter:** a manager-0 request always meets an idle port (grant-cycle term). A drain can end only on `end_w`. Reviewer mutant R11 (drain also ends on a not-busy port) is equivalent: `own_r != NONE` with busy low happens only in S_FIN.
- **Top:**
  - The gate's inputs add no combinational valid-to-ready path (the listener's readies do not depend on its own valid for the transaction face; the scoreboard candidate reads the masked ready).
  - The event router's non-TK events are trace-only, so a held TK event blocks no engine.
  - Lint zero-tolerance passes for all 39 files, including the three changed modules and the top (`receipts/gate-lint.log`).
- RTL findings: none from my own pass; S3 and S6 are suggestions. F3, confirmed afterwards: the atomic reject leaves the rejected sinks' RAM images inconsistent with `valid_r`, so the capture compare persists a default write-back.

### Robustness

- The walk always ends. The preload phase is bounded by the gate, and a silent device or an unwired face ends the walk at the deadline (probe P1). An err-answering face ends it at once (P2).
- A late device answer is drained (N5b/N5c). A never-answering device quarantines the port until reset, with changes reported pending: documented, and owned by #15.
- A boot without `restore_go_i` leaves the listener owned: documented (05 §5.1, integrator step 3) and accepted by the issue.
- Held ACMP heads keep their RX slots during the window. This is bounded by the walk and is the accepted producer-policy note.
- The 20 ms default sits in `F01.5`/`F08.1` only.
- Robustness findings: none from my own pass; S3 is latent. F3, confirmed afterwards: a transient device fault becomes permanent binding loss.

### Tests

Re-run here with the CI-pinned simulator (5.050 rev v5.050, `receipts/00-tool-identity.txt`), on an extract of the exact head (`receipts/focused-head/`):

| Suite | Result |
|---|---|
| acmp_nvm | 332/332 |
| acmp_nvm pinned control | 96 FAIL of 332 (the expected reproduction) |
| lsn_admit | 18/18 |
| nvm_port | 136/136 |
| pp_top | 1427/1427 (1,407 default + 20 fixture) |

- A225 neutrality: acmp_nvm, lsn_admit and nvm_port outputs are byte-identical at 69a6eac and 156c206 (`receipts/idiom-neutrality/`). The Python split moved all 218 removed lines verbatim into `pre_fix_forms.py`.
- The author's arms (public logs) all redden completed-scenario checks:
  - acmp_nvm LG01 96, LG02 55, LG03 40, LG02t 19, LG03t 7, LG04 5, LG05 12, LRdone 97, B01 16, BA1 13, B02 9, B04 128/325, BC1 9, B03 9, A01 1;
  - pp_top LG01 5, B01 2, B03 2.
- The nvm_port cause arms had no published logs. I reproduced them with identical counts: C1 10, C2 4, C3 6, C4 1 of 136 (`receipts/mutants-C*r.summary`).
- Reviewer mutants of my own:

| Mutant | Change | Result |
|---|---|---|
| R3 | stall count cumulative instead of consecutive | killed: N5a, N7a |
| R4 | deadline one cycle late | killed: N5b |
| R7 | short header named UNFRAMED | killed: T23c |
| R11 | drain also ends on a not-busy port | survived, equivalent |
| R5 | H_RS_REQ stall ignores the done/err cycle | survived, needs manager 1 (S3) |
| R6 | refusal ignores a same-cycle device error | survived (S2) |
| R1, R2 | top done/busy composition | survived (**F2**) |
| R8, R9, R10 | per-face top wiring | survived (S1) |

- Tests findings: F2, and F3's missing post-failure NVM grading.

### Docs

- 05 §5.1, 07 §5.3, 02 §8 and §8.2, `F01.5 P-NVM-RS-TMO-CYC`, `F08.1 T-NVM-RS-DEADLINE`, the integrator and operator guides, MODULE_MATRIX (45 modules, 0 untested) and the dataflow SVG were all read.
- Gates re-run, all OK (`receipts/gate-docs-lint.txt`): links 830 OK, matrix 115 REQ OK, `gen_matrix --check` OK, diagram lint 41 mermaid + 18 wavedrom OK, `make stale` rc 0.
- Docs findings: F1, and F3 (07 §5.3 "changes nothing here" is false after a failed walk); S4 and S5 are suggestions.

## Prior public review findings

At reconstruction, and at the start of this round (PR #109 comment 5807226156), the PR carried no review findings: two review-start comments, no reviews and no review comments. Issues #92 and #93 carry no review findings. No prior finding needs resolving or retaining.

### Order of work, and the concurrent report

1. My independent pass (diff, probes, mutants) produced F1, F2 and S1-S6. This report was then written with the verdict and the ledger, without F3.
2. Only then did I read the concurrent internal review report posted on the PR during this round (R278, NEGATIVE at the same head).
3. Its findings, resolved at this head:

| Concurrent finding | Disposition |
|---|---|
| **R278 F1 (MAJOR)** | Independently reproduced (`receipts/probe-failed-walk.log`, my own probe) and **retained** as F3 above. The ledger was updated for it. |
| **R278 F2 (MINOR)** | Same as my F2, reached independently. **Retained.** |
| **R278 S1 (SUGGESTION)** | Guard `RS_TMO_CYC_P >= 1`: `32'(RS_TMO_CYC_P - 1)` underflows at 0, so a `CLK_HZ_P` below 50 would silently disable the deadline. Agreed from reading `KL_acmp_nvm_shadow.sv:499` and `protocol_processor_top.sv:129`. Suggestion only. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | #92/#93 acceptance and S1/S3/S4; FASTCONNECT §6/§9; MATERIALIZATION; T8; Milan v1.2 5.3.8 as cited; pinned control; parent consumer evidence (manager-r2); probe FW | R279-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| RTL | UNCLEAN (F3) | `KL_pp_acmp_lsn_admit.sv`, `KL_pp_nvm_mgr_arb.sv`, `KL_acmp_nvm_shadow.sv` (including the capture compare and atomic reject), `KL_pp_nvm_port.sv`, `protocol_processor_top.sv` (gate, arbiter, done/busy, router), listener handshakes; lint 39/39 | R279-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Robustness | UNCLEAN (F3) | deadline/drain/quarantine paths; probes P1/P2 and FW causes 1-3; mutants R3/R4/R5/R11; boot-without-go and RX-slot holding | R279-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Tests | UNCLEAN (F2, F3) | acmp_nvm, pinned control, lsn_admit, nvm_port, pp_top re-runs; 19 author arms from logs plus 4 reproduced; 11 reviewer mutants; A225 output neutrality | R279-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |
| Docs | UNCLEAN (F1, F3) | 05 §5.1, 07 §5.3, 02 §8/§8.2, F01.5, F08.1, integrator and operator guides, MODULE_MATRIX, 20-rtl-dataflow.svg render, suite READMEs; docs gates | R279-1 | 156c206cbaedf721f7caef5c94faa21876a28c32 |

The ledger was first written with Conformance, RTL and Robustness CLEAN and Tests and Docs UNCLEAN (F2 and F1). It was updated after the independent reproduction of F3, per "Order of work".

## Real limits

- **Not run here** (manager-owned, or outside the permitted scope): the full `run_suites.sh` bank, yosys, the nvm_port `figures` gate, the parent consumer bank and hosted/act acceptance. For these I relied on the manager's public r2 receipts (donor-full: lint, run_suites, `make check`, `gen_matrix`, yosys, figures and `diff --check` all exit 0; parent-consumer all exit 0 with one calibration arm NOT RUN).
- **Hosted CI at the exact head:** two workflow runs (push and pull_request), each with docs-gates, suites and portability executed and succeeded. No job was skipped (`receipts/03-hosted-checks.txt`). The legacy commit-status API reports `pending` with zero contexts; it carries no result.
- **Parent consumer gitlink:** the parent consumer checkout that carries the gitlink is not in the permitted read set. Its gitlink is taken from the manager's public r2 record (parent head 1c28050c sets the processor to 156c206c). `$VALIDATION_STORAGE/pp92-manager-r1` holds evidence records only, and those are at the pre-idiom 69a6eac, where the idiom ratchets failed as the issue records.
- **Author mutant logs:** checked from the public logs, not re-executed, except the four nvm_port cause arms (reproduced) and the pinned control (re-run).
- **D3 terminal:** has no subject in the processor (there is no D3 writer). "Served before the D3 terminal" is graded only as "before the enable".
- **#15** (a port deadline or cancellation) remains open, by design.
- **Cost estimates** (issue #93 section "Cost") were not re-measured, by the author or here.
- **Physical:** calibration NOT RUN, and field skips are not hardware proof. No hardware was used.
- **Concurrent review:** a concurrent internal review report was published on the PR during this round, after it started. It is not a prior finding. It was not read before this verdict and ledger were first written; its MAJOR is included only after my own reproduction (see "Order of work").
- **F3 attribution:** attributing causes 2 and 3 to this PR rests on the diff (the new `rs_dev0_w`/`rs_tmo_w` terms in `rs_torn_w`), not on a base-tree execution. The base tree lacks the new modules, so it cannot run this bench.

## Pending manager duties

- Route F3 (MAJOR), F1 and F2 to the author lane. F3 may need an owner decision if the fix is to forfeit saved bindings rather than keep them. A fixed head needs a new review round.
- Build and gate the final current-dev candidate at the merge turn (source base fbc1f71, live dev 50e78097), including the full donor and parent banks and hosted/act acceptance.
- Record the consumer impact at the parent: device models must answer blank media as 0xFF, and err or early done now fails the restore.
- Keep #15 and #20 open. Carry S1-S6 forward as optional.

## Receipts (listed in MANIFEST.sha256)

- `receipts/00-tool-identity.txt`: simulator wrapper and binary identity.
- `receipts/01-clone-identity-before.txt`, `receipts/04-clone-identity-after.txt`: clone identity before and after.
- `receipts/02-history-checks.txt`: merge cleanliness, idiom scope, `diff --check`.
- `receipts/03-hosted-checks.txt`: hosted check runs at the exact head.
- `receipts/focused-head/`: the five focused runs.
- `receipts/gate-lint.log`, `receipts/gate-docs-lint.txt`: lint and docs gates.
- `receipts/idiom-neutrality/`: A225 output neutrality.
- `receipts/probe-unwired.log`: probes P1 and P2.
- `receipts/probe-failed-walk.log`: probe FW, causes 1-3 (F3).
- `receipts/mutants/*.log`, `receipts/mutants-*.summary`: reviewer mutants and reproductions.
- `scripts/run_one.sh`, `scripts/mutate.py`, `scripts/probe_unwired.py`, `scripts/probe_failed_walk.py`: portable scripts; each needs `PIN_VERILATOR` pointing at a 5.050 build.

R279-1 FINISHED
