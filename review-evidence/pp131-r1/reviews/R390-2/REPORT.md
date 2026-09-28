[R390] NEGATIVE - exact head 2b38d68e704e8a62fbeae8171c9195ca93728488

# R390-2: independent internal review of processor PR #132 (issue #131, D3 lane 1), round 2

| Item | Value |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| Head reviewed | `2b38d68e704e8a62fbeae8171c9195ca93728488`, tree `d11f358f887845fd5a8d9a63984b64792e0dff0e` (verified in the review clone) |
| Delta | `e1ae468f..2b38d68e`: six commits `380a3e4`, `83e708a`, `b06130d`, `85b2f6f`, `2fbe792`, `2b38d68` (22 files, +1,335/−118); base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` |
| Rulings | DR3a/DR4 ratification (parent issue 70 comment 5873060660); AECP hold admission (processor issue 131 comment 5873580386); round-2 assignment (issue 131 comment 5873696947) |
| Contract | parent `docs/design/SAVED_STATE_MATERIALIZATION.md` at `7a7582f0` (sha256 `e26784e1…f077`), §§6.2, 6.3, 8.1, 15.2, 18.1 and the DR3a row |
| Verdict | **NEGATIVE**: one MAJOR and two MINOR findings are open. All five lenses are UNCLEAN. Every round-1 finding of mine is resolved. |

## 1. How the review was reconstructed

1. The repository still has no AGENTS.md or CONTRIBUTING.md. The conventions come from `README.md`, `docs/README.md`, `hdl/README.md`, `docs/architecture/09_verification.md` §7 and the suite README mutation-record convention.
2. Issue #131 and PR #132:
   - the round-2 assignment (5873696947), the AECP hold-admission ruling (5873580386) and the author's round-2 review-ready note (5875971493);
   - the PR body, including its "Round 2" section and the parent-visible declarations;
   - the manager's round-1 bank comment (5873371256) and the R390-2 review-start comment (5876007554);
   - the DR3a/DR4 ratification on parent issue 70 (5873060660).
3. The D3 contract §6.2 (the writer at boot), §6.3 (the terminals), §8.1 and the DR3a row, fetched read-only at `7a7582f0`.
4. `git diff e1ae468f..2b38d68e`: I read every RTL hunk (writer, engine, RX validator, top) line by line, the new D3 checks in `tb/pp_top/d3_phases.hpp`, the new driver `tb/pp_top/d3_mutants.py` in full, the bench changes, and every documentation hunk.
5. Public executable evidence: `kebag-logic/milan-fpga@b657a2de` `review-evidence/pp131-r1` holds round-1 (`e1ae468f`) material only. I found no round-2 evidence directory at that commit (see §8). I snapshotted the hosted checks at this head.
6. My own execution at the exact head. Every run used disposable `git archive` copies under the packet's `scratch/` and the Verilator 5.050 wrapper named in §7:
   - `tb/pp_top`, full (both builds): 7,859 checks, 0 failures. The D3 section: 104 checks, 0 failures.
   - Focused suites, all PASS: `acmp_nvm` 353, `nvm_port` 136, `desc_mem_guard` 78, `dyn_state` 118, `desc_store` 584, `lsn_admit` 18, `adp_engine` 533, `rx_validator` 437.
   - Documentation gates, rc 0: `links` 966, `matrix`, `modmatrix`, `params` 26/26/26.
   - `--dr3a` reproduces the published figures.
   - The in-tree `d3_mutants.py`, run from an exact-head copy with 8 jobs: 62 of 62 mutants KILLED, 3 goldens PASS.
   - My round-1 probes and mutants rerun, plus 11 new reviewer mutants and 4 new probe sets (§3).
   - Focused re-counts of the parent's port-contract and naming ratchets, using the parent's own parsers.

The prior public findings on this PR are my own R390-1 findings (§4) and the other reviewer's R391-1 findings (§9). I read R391-1 only after this verdict, the findings and the ledger (§6) were written.

## 2. Findings

### R390-2-F1: MAJOR. An aggregate expiry before the D3 walk starts ends CLOSED with a valid image: a slow but live device leaves the entity dark until reset

- **Lenses:** Conformance, RTL, Robustness, Tests, Docs.
- **Where:**
  - The counter can fire in any cycle whose state has no wait: `hdl/aecp/KL_aecp_nvm_writer.sv:546-548`. `W_WAITGO` is such a state (`:522-525`, `wait_w = 0`).
  - The firing is an abort, and an abort while `proven_r` is 0 goes to CLOSED (`:628-636`). `proven_r` is 0 throughout `W_WAITGO`: it is set only in `W_IMG`/`W_IMGLOC` (`:649-662`).
  - The writer banner states this path (`:58-70`, "before the image is proven, the binding walk still running included, CLOSED"). So do `docs/architecture/07_memory_maps.md:661` and `docs/architecture/08_timing.md:45`.
- **Authority:**
  - **The ratification (5873060660).** On expiry the counter "takes the D3 terminal path the walk would take on a per-wait timeout (roll back to DEFAULTS or CLOSED as the state requires)". Its motivation is that ADP must not stay gated for a slow device. The processor's own F08.1 row restates it as "a slow but live device must not hold AECP and the enable".
  - **D3 contract §6.2.** WAIT-GO has no restore wait and no abort. It leaves only at the binding walk's drained terminal. A per-wait timeout in that phase is the binding walk's own: that walk fails whole, releases the listener, and the D3 walk then runs, reaching COMPLETE or DEFAULTS.
  - **D3 contract §6.3.** CLOSED is reached by "an image not proven at the start; a roll-back that cannot validate the image, or whose memory debt outlasts the deadline; an abort during the roll-back". An image that was never examined is not an image the restore could not prove.
- **Evidence** (executed; `scripts/probe_r2d.hpp`, `scripts/run_probe_r2d.sh`; receipt `probe-slow-binding-walk-head.txt`):
  - **Setup.** Every D3 record and the eight sinks' binding records are saved. The device model withholds each header byte 2,100 cycles and each payload byte 19,001 cycles. This is the ruling's "device answering just inside every per-wait deadline", slow per byte rather than per grant.
  - **The binding walk is healthy.** Its longest wait is 19,002 of 20,001 cycles, so no per-wait deadline trips. It ends with cause 0 at clock 3,174,963.
  - **The D3 writer ends CLOSED at clock 1,000,001, exactly the bound, with `rs_cause_o` 3.** At that clock:
    - the descriptor image is valid (`dbg_img_valid_o` 1);
    - the D3 walk has never started (longest D3 wait 0).
  - **Afterwards:**
    - AECP stays owned and the ADP enable stays 0;
    - a READ_DESCRIPTOR goes unanswered, as it will until reset;
    - `restore_done_o` never rises.
  - **The same device over erased media** ends DEFAULTS at clock 1,000,544, rolled back.
  - **No suite grades it.** No check expects a CLOSED terminal with cause 3. D3R13's device slows only grants, so its binding walk ends at about 158,500 clocks and the bound always falls inside the D3 walk.
- **Impact:**
  - **Who is affected.** A live NVM device whose binding walk alone passes 1,000 ms. For example, about 4.5 ms per byte over eight saved bindings is enough.
  - **What happens.** The entity goes permanently dark for AVDECC control: no ADP and no AECP. The image is valid and the bindings were restored.
  - **It repeats.** It happens on every boot with the same device and media, so only erasing the media or replacing the device clears it.
  - **The guides say the opposite.** The integrator guide says such a device ends on defaults (F2), and the operator guide tells the operator to fix the image.
  - **It defeats the ruling's purpose.** This is the outcome the ratification introduced the aggregate to prevent. The aggregate was meant to shorten the wait for a slow device, not to make it permanent.
- **Required outcome.** Choose one:
  - **(a) Change it** so that an expiry before the D3 walk has proven the image never closes a provable image. For example: at the bound, a binding walk still running takes its own per-wait path (fails whole and releases the listener); the D3 walk then proves the image and ends DEFAULTS with cause 3; CLOSED only if the image cannot be proven.
  - **(b) STOP to the manager** with this evidence and obtain an explicit ruling that CLOSED is the intended terminal for an aggregate expiry before the D3 walk starts.

  Either way:
  - add a named control with a binding walk slowed per byte past the bound, killed by a mutant;
  - make every guide state the outcome (F2).
- **Verification:**
  - Rerun probe D1 at the fix head: the terminal is the ruled one (DEFAULTS with a valid image under (a)).
  - The new named check fails under its mutant.

### R390-2-F2: MINOR. The integrator and operator guides misstate the aggregate's terminals and what CLOSED means

- **Lens:** Docs.
- **Where:**
  - `docs/guides/integrator.md:404-407`: "a device slow enough to reach that bound ends the restore on defaults (`rs_cause_o` 3) rather than holding AECP and the enable". This is false in two cases:
    - an expiry before the image is proven (F1);
    - an expiry during a roll-back. In probe C2, a pass-1 abort 300 cycles before the bound ends CLOSED at the bound, cause 2, where the same abort 3,000 cycles earlier ends DEFAULTS (receipt `probes-head.txt`).
  - `integrator.md:91`: the `NVM_RS_AGG_CYC_P` row names "DEFAULTS, or CLOSED before the image is proven" and omits CLOSED during the roll-back.
  - `integrator.md:398-400`: `restore_closed_o` "means the descriptor image could not be proven (`rs_cause_o` 7) or a roll-back could not re-prove it … fix the image and reset". An aggregate CLOSED is neither.
  - `docs/guides/operator.md`:
    - `:232-240`: the restore-outcome table has no aggregate row;
    - `:246-249` and `:310`: they attribute CLOSED only to the image, with the remedy "fix the image load".
- **Authority:** The processor's own single-source statement of the terminals, `07_memory_maps.md:650-666` and `08_timing.md:45`. The `docs/README.md` single-source rules. The D3 contract §15.2 integrator-guide rows ("CLOSED without done"; "Include DR3a aggregate and per-wait budgets").
- **Impact:** Firmware written to the guide expects defaults and may not handle CLOSED. An operator who meets a CLOSED caused by a slow or faulting device is sent to fix an image that is valid.
- **Required outcome:** In both guides, state every terminal the aggregate can take, as 07 §5.3 lists them and as adjusted by F1's resolution. Also list CLOSED's causes including the aggregate: the outcome-table row, the CLOSED paragraph, the troubleshooting row and the bring-up step.
- **Verification:** Compare the text against the 07 §5.3 terminal table at the fix head.

### R390-2-F3: MINOR. The aggregate's span over the roll-back is ruled but not graded; a reviewer mutant survives

- **Lens:** Tests.
- **Where:** `KL_aecp_nvm_writer.sv:546` (`agg_live_w`), against the D3 section of `tb/pp_top`.
- **Authority:**
  - The contract's DR3a row: an aggregate "from accepted `PP_CTRL[1]` to COMPLETE, DEFAULTS or CLOSED, including rollback", ratified as enforced.
  - The round-2 focus: "from the accepted restore_go_i through both walks and the roll-back".
  - The head's own 07 and 08 text.
  - The 09 §7 and suite-README rule that ruled behaviour is graded by a named check.
- **Evidence** (`scripts/r390_2_mutants.py`, receipts `r390-2-mutants.txt`, `probes-mutant-agg_not_in_rollback.txt`):
  - **The mutant.** `agg_not_in_rollback` pauses the counter in `W_RB`/`W_RELOC`. It SURVIVES the D3 section (104/104).
  - **Probe C2, at the head.** A pass-1 device error at clock 999,701 starts a roll-back that straddles the bound; the head ends CLOSED at clock 1,000,001.
  - **Probe C2, under the mutant.** The same boot ends DEFAULTS at clock 1,000,247.
- **Impact:** A regression that stops counting in the roll-back, or that changes its terminal there, passes every gate.
- **Required outcome:** A named check for an aggregate bound that falls inside a roll-back, which the mutant fails. Its expected terminal follows F1's resolution.
- **Verification:** Rerun `r390_2_mutants.py agg_not_in_rollback` at the fix head: KILLED by the named check.

### Suggestions (they do not affect the verdict)

- **R390-2-S1 (RTL, Docs):** The admission leaves `RX_SLOTS_P − 1` slots to the other protocols, so `RX_SLOTS_P = 1` leaves none while AECP is held. No floor is stated or checked (`protocol_processor_top.sv:86`; F01.5 gives only the default). Add an elaboration check `RX_SLOTS_P >= 2`, or state the floor in F01.5 and the integrator guide.
- **R390-2-S2 (Tests):** The reviewer mutant `agg_ignores_in_hand` (the bound fires even with a grant, byte or answer in hand) survives the D3 section. Probe C1 forced a grant at each of the seven cycles around the bound. The head and the mutant both ended DEFAULTS at clock 1,000,001, drained, with a later SET persisting (`probes-head.txt`, `probes-mutant-agg_ignores_in_hand.txt`). I found no observable difference, so the guard looks equivalent in effect. Either grade it with a cycle-exact case, or say in the banner that it is defensive.

## 3. Round-2 assignment items verified

| Item | Result | Evidence |
|---|---|---|
| (1) The enforced 1,000 ms aggregate: `NVM_RS_AGG_CYC_P = CLK_HZ_P` from the accepted `restore_go_i`, through both walks and the roll-back, taking the per-wait path; a just-inside device ends at the bound | **met for a device slow per grant; F1 for one slow per byte in the binding walk; F3 for the ungraded roll-back span** | The constant is derived (`protocol_processor_top.sv:144`). The count starts the cycle `restore_go_i` first reads 1 and fires once. See the aggregate probes below this table. |
| (2) AECP hold admission: at most one AECP record while held; the rest dropped at the slot gate and counted in word 37; non-AECP latency unchanged; my GET_RX_STATE probes answered; the unbounded-gating mutant fails D3O5/D3O6; the three documentation corrections | **met** | The resident count and gate are at `protocol_processor_top.sv:2614-2655`, the validator gate at `KL_pp_rx_validator.sv:279-283`, and snapshot word 37 at `:4500-4502`. See the admission probes below this table. |
| (3) Each of my round-1 mutants is KILLED by a named check | **met** | `backoff_holds_dispatch` → `D3S10 backoff`; `disagree_one_direction` → `D3R4b`; `rollback_one_cycle` → `D3R4 strobe`; `backoff_derivation` → `D3S10 timing` and `D3S10 backoff` (my script, and the in-tree driver) |
| (4) `tb/pp_top/d3_mutants.py` runs from the tree; the suite READMEs carry the mutation records | **met** | 62/62 KILLED, 3 goldens PASS from an exact-head copy (`d3-mutants-from-tree.txt`). Each of the 62 mutants has a README row: 58 in `pp_top`, 3 in `acmp_nvm`, 1 in `rx_validator`. Every recorded "failing checks" count equals my run's (`readme-record-vs-run.txt`). |
| (5) Port contracts 111 ≤ 111; parameter unit naming | **met** | The parent's `sv_ports.declarations()` and `lint_rtl_policy` count 111 undocumented processor ports at base, 114 at `e1ae468f` and 111 at the head (`port-doc-count.txt`). The parent's `measure_naming.scan_text()` against its `naming.budget` finds 3 new identities at `e1ae468f` and 0 at the head (`naming-check.txt`). |
| (6) Parent-visible changes declared | **met** | See §5 |

Aggregate probes for item (1) (`scripts/probe_r2.hpp`, `scripts/probe_r2c.hpp`; receipts `probes-head.txt`, `dr3a-head.txt`):
- Every grant withheld one cycle inside the per-wait deadline:
  - over saved records, DEFAULTS at clock 1,000,001, whether `restore_go_i` is a 5-cycle pulse, held as a level, or pulsed again at 500 ms;
  - over erased media, the bound falls in pass 1 and the roll-back ends DEFAULTS at clock 1,000,544.
- After an aggregate DEFAULTS, the held command is answered byte-exact, a new one too, and the ADP enable rises.
- `--dr3a`: healthy restores ≤ 2,661 cycles, longest healthy wait 853, a silent device at 2 × the deadline, the just-inside device at the bound.
- The reviewer mutants `agg_removed`, `agg_one_late` and `agg_restarts_on_go` are KILLED by D3R13.

Admission probes for item (2) (receipts `probes-head.txt`, `probes-mutant-hold_unbounded.txt`, `r390-2-mutants.txt`, `mutant-hold_after_release-full-pp_top.txt`):
- **My round-1 probes at the head:**
  - in CLOSED, GET_RX_STATE is answered after each of 10 AECP commands and after 2,000 ms, where round 1 lost it from the 4th command on;
  - during the slowed restore with 6 AECP queued, it is answered at 167 cycles, before the terminal, where round 1 never answered it.
- **New tight-feed probes** (no inter-frame idle):
  - six AECP commands then a GET_RX_STATE: answered in 172 cycles, equal to the idle latency fed the same way; word 37 = 5;
  - eight back-to-back (AECP, GET_RX_STATE) pairs in CLOSED: 8 of 8 answered; word 37 = 7;
  - in the slowed restore, the held command is answered at the terminal and the 5 dropped ones never are;
  - after the terminal, two tight AECP commands are both answered and nothing more is counted.
- **Under the unbounded-gating mutant** every one of these fails as in round 1.
- **Reviewer mutants:**
  - `hold_until_any_terminal`, `hold_admits_two` and `residency_counts_acmp` are KILLED by D3O5/D3O6;
  - `hold_after_release` survives the D3 section but is KILLED by the full suite (W21dd2, W21ee, U11g);
  - `held_gate_ignores_da` survives. It only changes which counter an already-dropped non-local frame lands in, so I raise no finding.
- **Documentation:** `integrator.md` (the CLOSED row), `07_memory_maps.md` (the CLOSED terminal) and `03_packet_engine.md` rule (d) are corrected. V10 is added, and rule (e) states the boot-hold exception.

## 4. My round-1 findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R390-1-F1 (MAJOR, held AECP starves the shared ingress) | **RESOLVED** | The ruling is implemented. My two probes now answer every GET_RX_STATE. D3O5/D3O6 fail under the unbounded-gating mutant. The three documentation statements are corrected. |
| R390-1-F2 (MAJOR, the aggregate not implemented) | **RESOLVED** as required in round 1: counter, derivation, F01.5/F08.1/08 §2, the named control and removal mutants | The new F1 and F3 concern the implemented counter's pre-proof terminal and its roll-back grading. They are new findings, not a retention. |
| R390-1-F3 (MINOR, four ungraded rules) | **RESOLVED** | All four mutants are KILLED by named checks (§3 item 3). My G1/G2 probes still show the head's correct behaviour: a blank-then-whole abort with cause 5, and a READ_DESCRIPTOR in the backoff answered after 2,299 cycles. |
| R390-1-F4 (MINOR, negative controls not reproducible from the tree) | **RESOLVED** | The driver is in the tree, runs from it (62/62), and the records are in three READMEs; `09_verification.md:194-197` points to them. |
| R390-1-S1 (name three more parent-visible changes) | **TAKEN** | The PR body's round-2 section, "Also named (R390-1 S1)" |
| R390-1-S2 (state the 240 ms exception at rule (e)) | **TAKEN** | `03_packet_engine.md` rule (e) |

## 5. Parent-visible change audit

A diff of the top's port and parameter lists, made with the parent's own `sv_ports.declarations()` (`receipts/top-port-param-diff.txt`):

- **Round 2 (`e1ae468f..2b38d68e`):** exactly one new parameter, `NVM_RS_AGG_CYC_P`, and no port added, removed or resized.
- **Base to head:** the parameters `NVM_RS_AGG_CYC_P` and `NVM_RETRY_BACKOFF_CYC_P`, and the five outputs `restore_closed_o`, `restore_rb_o`, `rs_cause_o`, `restore_cause_o` and `d3_unflushed_o`.

All of these are declared in the PR body, together with:
- the per-wait default ceil(`CLK_HZ_P`/50);
- snapshot word 37 (the dropped-while-held counter, host word `0x20025`, 16-bit saturating);
- the admission behaviour and the aggregate terminals;
- the evidence-classifier disposition line for `tb/pp_top/d3_mutants.py`.

The writer's `DEB_TICKS_P` → `DEB_MS_P` rename is internal: the parent instantiates only the top. The only undeclared parent-visible behaviour is F1's permanent CLOSED for a slow binding walk.

## 6. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | ratification 5873060660, admission ruling 5873580386, D3 contract §§6.2, 6.3, 8.1 and the DR3a row, against the writer's aggregate, the top's admission and the validator gate | R390-2 | `2b38d68e704e8a62fbeae8171c9195ca93728488` |
| RTL | UNCLEAN (F1) | every RTL hunk of the delta: writer (`agg_*`, abort, `wait_w`), engine wiring, validator V10, top residency counter, derivations, snapshot word 37 | R390-2 | `2b38d68e704e8a62fbeae8171c9195ca93728488` |
| Robustness | UNCLEAN (F1) | slow-per-grant, slow-per-byte, level/repeated `restore_go_i`, forced-grant-at-bound and roll-back-straddle probes; tight-feed admission probes in CLOSED and in a slowed restore | R390-2 | `2b38d68e704e8a62fbeae8171c9195ca93728488` |
| Tests | UNCLEAN (F1, F3) | D3 section (104 checks) and full `tb/pp_top` (7,859); 8 focused suites; in-tree driver 62/62; 4 round-1 and 11 round-2 reviewer mutants; README record equality | R390-2 | `2b38d68e704e8a62fbeae8171c9195ca93728488` |
| Docs | UNCLEAN (F1, F2) | 01, 03, 05, 07, 08, 09 and diagram 21 diffs; integrator and operator guides; suite READMEs; `links`/`matrix`/`modmatrix`/`params` gates | R390-2 | `2b38d68e704e8a62fbeae8171c9195ca93728488` |

## 7. Real limits of this review

- **Tooling.** The requested simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`, which reports `Verilator 5.050 2026-07-01 rev v5.050` (hashes in `receipts/tool-identity.txt`). The system Verilator 5.052 was not used.
- **Parent gates.** The port-contract and naming results are focused re-counts over the processor tree, using the parent's parsers and budgets fetched read-only at `7a7582f0`. They are not the parent gates run in a scratch parent.
- **Not run:**
  - the full processor bank, `lint_hdl.sh`, Yosys/OOC, and `make check`'s `lint`/`wavedrom-check`/`stale`;
  - the parent consumer set, `pp_shadow`, xvlog, and the evidence classifier.
- **Probe models.** The slow-per-byte device of F1 is a reviewer knob added to a disposable copy of the bench's device model; the tree is unchanged. Non-AECP latency under the hold was measured at the top for ACMP only. ADP and MAAP pass-through under the hold is graded at the validator (F28).
- **No hardware.** No physical calibration or hardware was used. Field skips are not hardware proof.
- **Hosted checks.** At 18:54Z: `docs-gates` and `portability` had completed successfully in two runs each; both `suites` jobs were still in progress. Hosted acceptance is the manager's.

## 8. Pending manager duties

- The donor full bank and the parent consumer gates at this head, and the final current-dev candidate (source base `c951a9ff`, live dev `7390b436`) at the merge turn.
- The public evidence at `b657a2de` is round-1 material. Publishing the round-2 bank evidence for this head remains with the manager.
- A ruling if F1 is resolved by option (b).
- The parent pin-adoption lane: connect the five round-1 ports, adopt `NVM_RS_AGG_CYC_P` and snapshot word 37, and add the classifier disposition for `d3_mutants.py`.
- DR4 post-place and the 8x8 post-place obligation stay with lane 2 (open, not waived).

## 9. Prior public findings of the other reviewer (R391-1), resolved or retained at this head

I read these after §§2-6 were written. Reading them changed no finding and no ledger entry.

| R391-1 finding | Status at this head | Evidence (mine) |
|---|---|---|
| F1 (MAJOR, the DR3a aggregate not implemented) | **RESOLVED** as that finding required: a counter from the accepted start, derived from `CLK_HZ_P`, taking the per-wait path, with the named control and a removal mutant | The P5-style stimulus (every grant just inside) ends at the bound (§3). F01.5, F08.1, 08 §2, 01 and 03 rule (d) and the integrator guide state the ratified values. The `params` gate passes 26/26/26. F1 and F3 of this report are new findings on the implemented counter. |
| F2 (MAJOR, held AECP exhausts the RX slots) | **RESOLVED** | In CLOSED, GET_RX_STATE is answered after 10 interleaved and 6 tight AECP commands, and after 8 tight (AECP, GET) pairs. During a stretched walk it is answered with 6 queued. See §3. An AECP frame for another entity id is held or dropped within the same one-record share. The documents state what is kept and what is dropped and counted (03 V10 and rule (d), operator word 37). 05 and diagram 23 ("ACMP still answers") now hold. |
| F3 (MINOR, four delayed and boundary behaviours unguarded) | **RESOLVED** | The in-tree driver's `pass1_read_not_drained`, `judge_wait_unwatched`, `rate_walk_stuck_on_first_lane` and `rate_walk_unbounded` are KILLED in my from-tree run by `D3R5b`, `D3R8b`, `D3R3b entry 7` and `D3R3b entry 8`. I did not run that reviewer's own script. |
| F4 (MINOR, port-contract ratchet and naming gate) | **RESOLVED** | 111 ≤ 111 undocumented ports, and 0 new naming identities at the head, both counted with the parent's own parsers (§3 item 5). |
| S1 (one conversion, two roundings) | **TAKEN** | `NVM_RS_TMO_CYC_P` is ceil(`CLK_HZ_P`/50) (`protocol_processor_top.sv:136-137`). F01.5 (`01_overview.md:176`) and 08 §2 state that single conversion. |

## 10. Receipts and reproduction

- Every publishable file is listed in `MANIFEST.sha256`. Paths are relative to the packet.
- **Clone integrity** (`receipts/clone-integrity.txt`), after all probes:
  - HEAD and tree verified;
  - porcelain status (ignored and untracked included), `diff-index` and worktree diff all empty;
  - 0 worktree blobs differ from the index;
  - 0 gitlinks and no `.gitmodules` (the repository has no submodules);
  - `ls-files -s` sha256 `b0ceb326…6954`.

  No probe touched the review clone.
- **Reproduce**, with `<clone>` the review clone and `<V>` the simulator:
  - Full suite: `tb/pp_top` `make VERILATOR=<V>` in a `git archive` copy; then `--d3-only` and `--dr3a`.
  - Focused suites: `scripts/run_focused_suites.sh <clone> <out> <V>`.
  - Reviewer mutants: `python3 scripts/r390_2_mutants.py <clone> <scratch> <V> [name …]`.
  - Reviewer probes (round-1 and round-2): `scripts/run_probes.sh <packet> <archive-copy> <V> [--probe-hol --probe-hol-restore --probe-gaps --probe-r2 --probe-r2c]`, on a fresh copy per run.
  - F1's probe: `scripts/run_probe_r2d.sh <packet> <archive-copy> <V>`.
  - The in-tree driver: `python3 tb/pp_top/d3_mutants.py --output <dir> --verilator <V> --jobs 8` from an exact-head copy, with `TMPDIR` under `scratch/`.
  - Parent-ratchet re-counts: `python3 scripts/port_doc_count.py <parent-scripts> <clone> <revs…>` and `python3 scripts/naming_check.py <parent-scripts> <clone> <revs…>`, where `<parent-scripts>` holds `sv_ports.py`, `lint_rtl_policy.py`, `measure_naming.py`, `code_quality_scope.py`, `naming.budget` and `port_docs.budget` from `milan-fpga@7a7582f0` (hashes in the receipts).

R390-2 FINISHED
