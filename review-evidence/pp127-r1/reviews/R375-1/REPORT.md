[R375] NEGATIVE - exact head cf4e5c63ab12442c6c63d2bfe2bb64902674d55e

# R375-1: external independent review of processor PR #130 (issue #127)

- Head `cf4e5c63ab12442c6c63d2bfe2bb64902674d55e`, tree `2f66e2d9de82e1aca097db59a9b9f4a19cdb767d`. It is one commit on base `16be6768f710e79450aace277abacd6c2c3336e5`, which is the parent's current pin.
- Scope is issue #127: apply the own MSRP LeaveAll registrar event at the `sLA` transmit action, not at leavealltimer expiry. This fixes parent kebag-logic/milan-fpga#608, where 3 of 100 bench disconnects kept streaming.
- The review ran in a cleared context, in a detached clone. The clone was verified byte-exact at the end of the review: see `receipts/clone-integrity.txt`.

## Verdict summary

The RTL change is correct in every case I could construct:
- Timer expiry only records intent.
- The registrar aging and the `txLA!` walks happen on the encoder's slot-acceptance edge.
- A Listener Leave decoded before or on that edge clears IN.
- LV + rLv and #108 behave as before.
- Peer supersession, backpressure, reset, full tables and repeated expiries all behave as documented.

Against base RTL, my independent probe reproduces the #608 non-stop. At this head it is gone.

The verdict is NEGATIVE for two open items, both in the Tests lens:
- **F1 (MAJOR):** three parent consumer gates fail at this head, on the new test code. This is retained from the manager's bank evidence and confirmed by inspection.
- **F2 (MINOR):** four new RTL guards in the scope areas (peer supersession under backpressure, new intent during a canceled preparation, the join-start peer guard, and the sink-plane acceptance edge) can be deleted without any suite failure. My own probes catch all four.

## Reconstruction (order followed)

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. `git ls-files` shows neither. I used `README.md` and `docs/README.md` (the conventions and single-source rules) instead.
2. **Frozen scope.** From the issue #127 body and the assignment comment 5860872275:
   - Keep expiry intent pending.
   - Apply `sLA` consistently with applicant processing and encoder acceptance.
   - A Leave before the action sees IN.
   - LV + rLv is unchanged. #108 stays separate; only a peer LeaveAll superseding the pending own one must be handled.
   - Periodic declarations and the six-cycle no-storm test stay unchanged.
   - Proof: the phase-swept cases, both stream FSMs, all SRP suites green, every new check pinned by a killed mutant, restoring the expiry pulse must fail, and the parent harness must no longer reproduce a non-stop.
3. **Parent analysis.** #608: the body, the clue comment 5860814414 and the analysis/decision comment 5860869482. The decision reads the stop target as "within one PDU period of a withdrawal that reaches an IN registrar".
4. **Authorities.** 802.1Q-2014 §10.7.9 / Table 10-5 (`sLA`: LeaveAll events against all Applicant and Registrar state machines of the participant) and Table 10-4, as quoted in `docs/architecture/10_srp_engine.md` §6.5. Milan Δ13 (rLv on IN goes to MT). T-MRP-LEAVE is 5000 ms (F08.1).
5. **Diff and history.** I read `git diff 16be6768..cf4e5c63` in full: 14 files, +826/−64.
6. **Public evidence.** I read the evidence packet `kebag-logic/milan-fpga@88ed7be3/review-evidence/pp127-r1` only after my own RTL and test pass. I also read the manager's parent-gate comment on PR #130 (5861561819, posted after the review started).
7. **Prior review findings.** There are none on PR #130: zero reviews, zero inline comments, and only two review-start notices.

## Tool identity

The requested simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used `$VALIDATION_STORAGE/pp127-manager-cf4e5c63/pinned-tool-bin/verilator` instead:
- It is byte-identical to the `372-manager-r2` wrapper (sha256 `905795b9…`).
- It reports `Verilator 5.050 2026-07-01 rev v5.050`.

Details are in `receipts/tool-identity.txt`. The system `verilator` (5.052) was not used.

## Executed evidence (all in this packet)

| What | Result | Receipt |
|---|---|---|
| srp_top, srp_stream_fsms, srp_encoder, srp_decoder, srp_admission, pp_top at head (clean `git archive` extraction) | 1914/1914, 1215/1215, 556/556, 190/190, 991231/991231, 7751/7751, all rc=0 | `receipts/head-suite-*.log`, `head-suites-rc.txt` |
| srp_top at base | 1531/1531 | `receipts/base-suite-srp_top.log` |
| Six-cycle no-storm at head | per-cycle frames 4,3,3,3,3,2; F4 limits (≤4 per cycle, 6/6 ready) unchanged in source | `head-suite-srp_top.log` |
| `scripts/lint_hdl.sh` (pinned), `make links matrix modmatrix params` | rc=0 for all | `receipts/head-lint_hdl.log`, `head-make-*.log` |
| Author mutation campaign re-executed independently (5 controls, 36 mutants, pinned simulator, parallel disposable trees) | controls PASS; 36/36 KILLED with the expected named assertion; tag sets identical to the published `mutant-summary.log` | `receipts/author-mutants*` |
| Reviewer probe group (102 checks) at head | 102/102 PASS | `receipts/runs/head.r375.log` |
| Same probes against base RTL (counterfactual) | 20 FAIL: the #608 non-stop is reproduced | `receipts/runs/base.r375base.log` |
| 11 reviewer mutants × (full suite + probes) | see Tests lens | `receipts/reviewer-mutants-summary.txt`, `receipts/runs/r-*.log` |
| Hosted checks at the exact head | 6 check runs executed, all `success`: docs-gates, portability and suites, each under two triggers. None skipped. No legacy status contexts. | `receipts/hosted-check-runs.tsv` |

Scripts are in `scripts/`: `prepare_trees.sh`, `r375_run.py`, `r375_probes.inc` and `r375_author_mutants.py`.

## Lens: Conformance — CLEAN

**`sLA` placement.**
- `KL_srp_top.sv:1166-1169`: expiry sets only `la_msrp_pend_r`.
- `:1080-1091`: at the next MSRP join opportunity after the previous round completes, `la_wait_r` requests preparation.
- `KL_srp_encoder.sv:343-345`: the encoder's slot grant (or reuse of a reserved slot) is `la_prepare_done_o`, and `la_tx_o` is its uncanceled subset.
- `KL_srp_top.sv:327,530,613,363`: that one edge drives `leaveall_own_i` to both FSMs, `join_tick_i` to both walks, and the Domain re-declaration.
- `KL_srp_talker_fsm.sv:570` and `KL_srp_listener_fsm.sv:625`: the same-edge walk uses `txLA!`.

This matches Table 10-5 (`sLA` at the transmit opportunity; LeaveAll events to all Applicant and Registrar machines) and §10.8 NOTE 2: induced messages follow the LeaveAll, and the encoder flags the first vector of each type (`KL_srp_encoder.sv:429-433`).

**Listener Leave phase.** The probe `R1` anchors on the observed expiry strobe and the observed join opportunity, not on nominal milliseconds. At the head, Leaves decoded at +1 and +40 cycles after expiry, at the midpoint, at −2 and at 0 cycles from the action all clear IN, and ACTIVE stays 0 for the 2 s hold. A Leave at +2 cycles after the action is retained (LV + rLv). This holds for Ready and Ready Failed, on sources 0 and 7. At base, the same injections at +40 cycles through the action edge keep ACTIVE=1 with the registrar in LV.

**Preserved semantics.**
- LV + rLv is unchanged: registrar code outside the new edge is untouched, and the author mutants `*-strict-lv` are killed.
- #108 is unchanged: a peer LeaveAll does not re-arm or redraw the timer (`KL_srp_top.sv:1177-1182`; M4 is killed by `peer-restarts-timer`).
- Type scope is unchanged: received lanes are routed per type; only the pending own action is canceled by any MSRP lane; MVRP cannot cancel it (M1, `mvrp-supersedes-msrp`).

**Parent replay.** The published evidence shows that the unmodified parent harness at this head still exits 1: "OWN_LA race … ACTIVE stayed 1". Its helper waits for LV entry, which is now the `sLA` edge, and then sends the Leave before the flagged frame finishes on the wire.
- My probe measures that residual window as 457 cycles from `sLA` to the completion of the flagged frame on the TX BFM. That is 11 tb-ms at this bench's 40 cycles/ms, and microseconds at any real core clock.
- The #608 decision limits the stop target to a withdrawal that reaches an IN registrar. On that reading, the helper's case is the documented legitimate LV path, not the defect.
- The substance of the claim, that early-window Leaves now stop, is reproduced independently above.
- The parent harness source itself is not in any public branch I could reach, so I could not re-run it. See Limits, F4 and the manager duties.

## Lens: RTL — CLEAN

- **Encoder** (`KL_srp_encoder.sv`):
  - The new `E_COLLECT` state and `preparing_r` are reset.
  - Pushes are open during collect (`:335-336`) but closed on the snapshot cycle (`:340-342`), so the drain count cannot race a push.
  - `drain_n_r` is re-snapshotted in `E_COLLECT` (`:600`), so the MVRP count loaded in the prepare branch (`:558`) is harmless.
  - The empty-table LeaveAll-only path is at `:607-614`.
  - `join_pend_r[0]` is not latched in collect (`:759`), because round completion owns that tick.
- **Top** (`KL_srp_top.sv`):
  - `la_cancel_r` is cleared when a new preparation starts (`:1084`).
  - It is stale-but-inert after a canceled acceptance, because `E_ALLOC` gates on `preparing_r` and the next preparation clears it.
  - Round completion bits are no longer reset by mid-round cadence ticks (`:1152`).
- **Lint:** `scripts/lint_hdl.sh` passes with zero tolerance on the pinned simulator.
- **Top-level ports:** unchanged (only `srp_top_wrap.sv` gained test-only ports).
- **pp_top:** passes 7751/7751.
- **TX BFM change:** the change in `tb/srp_top/sim_main.cpp:371-373` is justified by the RTL. `KL_pp_tx_slots.sv:164,250-255` starts only when `!run_r`, and `run_r` clears on the last-byte consume edge, so a request on that cycle would be dropped.

## Lens: Robustness — CLEAN

I probed each case at the head (`receipts/runs/head.r375.log`):
- **Peer at the join-start edge.** Six phases from −2 to +3 cycles relative to the join opportunity, covering −1, 0 and +1. The peer always supersedes when it precedes acceptance, and the registrar planes agree (R4).
- **Encoder-busy supersession.** Preparation is waiting while the encoder holds a TX request, and a peer LeaveAll arrives. It cancels, and no own flags or aging follow (R6).
- **New expiry during a canceled, still-blocked preparation.** The newer intent survives and is sent exactly once (R7).
- **Sink plane at the exact acceptance edge.** Talker Lv at −1 and 0 cycles clears IN; at +1 cycle LV is retained, for Ready and Ready Failed (R5).
- **Canceled reservation parking.** A reservation parked in `E_COLLECT` could delay MVRP drains. In the reachable stream configuration, the canceled round carried content and the encoder returned to idle (MVRP response 50 ms). VIDs are declared only by stream users (`KL_srp_vlan.sv:13-18`), whose walks produce MSRP content, so I found no MVRP starvation path (R3).

The author's M/N groups separately cover reset, allocation and TX stalls, full tables, coalesced expiries and renewal. I re-executed their mutants.

## Lens: Tests — UNCLEAN (F1, F2)

**What passes.**
- The phase-swept cases the issue asks for exist: before expiry, during the pending action, at acceptance, and after LV; Ready and Ready Failed; sources 0, 3 and 7; mismatched SID; malformed input; reset; allocation and TX delays.
- Restoring the expiry pulse fails:
  - the author's `expiry-event`: 81 failures;
  - my `r-expiry-pulse-restored`, which ORs the expiry strobe into both FSMs' `leaveall_own_i` on top of the new path: 88 failures across K2, K4, K5, K11, K12, L2, M7, M10, N1, N2, N11.
- All 36 author mutants are killed as published.

**Reviewer mutants.** Of 11:
- 5 are killed by the PR's suite: expiry-pulse-restored, la-only-emission-lost (M12), collect-blocks-pushes (22 failures), accept-edge-drain-lost (N10), reuse-without-action (M12).
- 4 survive the full 1914-check suite and are killed only by my probes. These are F2.
- 2 survive everything and are low impact. These are F3.

## Lens: Docs — CLEAN

- `docs/architecture/10_srp_engine.md:488-516`, the RTL banners (`KL_srp_top.sv:50-54`, `KL_srp_encoder.sv:44-48`), the port comments and the three testbench READMEs match the behaviour I observed.
- This includes the exact-edge receive priority on both planes (verified by my R5), the residual LV path ("The accepted action precedes serialization…"), and the #108 boundary.
- No other document describes the old expiry-time aging: I searched docs/guides, 02, 08 and 09.
- The single-source rules hold: timing values stay in F08.1, and the gates pass.
- F3(c) is a wording nit only.

## Findings

### F1 — MAJOR — lenses: Tests
- **Where:**
  - `tb/srp_top/sim_main.cpp:334`, `:708`, `:810` (multi-declarator declarations).
  - `tb/srp_top/mutants.py:106` and `:114` (public `run`/`main`, unannotated and undocumented).
  - 14 lines of `tb/srp_top/mutants.py` over 120 characters (e.g. `:20`, `:24`, `:27`).
  - `tb/srp_top/mutants.py:110`: a host wall-clock `timeout=900`.
  - `tb/srp_top/mutants.py:121`: it reads the RTL sources.
- **Authority/evidence:** the manager's parent consumer gates at this head (PR #130 comment 5861561819, parent dev `931f396e` with the gitlink at `cf4e5c63`) report 8 of 11 passing and 3 failing:
  - C++ rule 11: multi-declarator 1 > ratchet 0.
  - Python rule 12: unannotated 2, undocumented 2, and over-long 14 > ratchet 0.
  - `measure_test_evidence.py --check`: wall-clock suites 4 > 3, and 1 unexplained DUT-source reader.

  I confirmed every cited construct by inspection. I did not run the parent banks, as instructed.
- **Impact:** the parent cannot adopt this pin; the issue's parent bar is unmet at this head.
- **Required outcome:** the three gates pass at a new head, with no ratchet increase. Use the named construct for C++; annotate and document the Python and wrap its lines; bound the tests by DUT cycles, not host time; and either explain the DUT-source reader in the evidence tool's terms or remove it.
- **Verification:** the manager re-runs the parent consumer gates on the new head (11/11). A reviewer confirms the constructs are gone.

### F2 — MINOR — lenses: Tests
- **Where:**
  - `hdl/srp/KL_srp_top.sv:730`: the cancel input includes the latched `la_cancel_r`.
  - `:1095`: `if (!la_cancel_r)` keeps a newer intent.
  - `:1082`: the join-start guard `!(|dec_la_msrp_w)`.
  - `hdl/srp/KL_srp_listener_fsm.sv:728-754`: receive-over-own-LeaveAll priority on the sink plane at the acceptance edge, which `docs/architecture/10_srp_engine.md:502-504` states generally.
  - The relevant tests are `tb/srp_top/sim_main.cpp:665-695` (L group: talker plane only) and `:697-792` (M group: peer only while allocation is blocked, or before preparation).
- **Authority/evidence:** issue #127 requires handling "both stream FSMs, … backpressure, … and a peer LeaveAll that supersedes the pending own one". Each of these single edits leaves the full srp_top suite at 1914/1914 PASS, and each is caught by a reviewer probe at the head:

  | Reviewer mutant | Caught by |
  |---|---|
  | `r-cancel-latch-dropped` (cancel = decode strobe only) | R6b: peer during encoder-busy preparation is ignored; own `sLA` follows the peer |
  | `r-cancel-consumes-new-intent` (always clear intent at acceptance) | R7c: an expiry during a canceled, blocked preparation is lost |
  | `r-join-start-guard-dropped` | R4d/R4e: a peer on the join-opportunity cycle does not cancel; own `sLA` re-ages the registrars |
  | `r-sink-receive-priority-lost` | R5b: a talker Lv on the acceptance edge is retained in LV |

  Logs: `receipts/runs/r-*.full.log` and `r-*.r375.log`.
- **Impact:** the RTL is correct today. But the `la_cancel_r` register this PR introduces is pinned by no test at all, and the other three guards protect exactly the re-aging and IN-clearing behaviour at the heart of #608. A regression there would reintroduce a Leave that lands in LV, and nothing would fail.
- **Required outcome:** add srp_top cases for:
  1. a peer LeaveAll while preparation waits behind an encoder that holds a TX request;
  2. a new own expiry while a canceled preparation is still blocked;
  3. a peer decoded on the join-opportunity cycle;
  4. a sink-plane Talker Lv at −1, 0 and +1 cycles around acceptance.

  Record each as a killed mutant in the campaign (`tb/srp_top/mutants.py` and the README table).
- **Verification:** the four reviewer mutants above (the edits are in `scripts/r375_run.py`) fail named new assertions in the PR's own suite, and the head stays green.

### F3 — SUGGESTION — lenses: Tests, Docs
- (a) `r-join-coalesce-dropped` (`KL_srp_top.sv:1152`, cadence ticks dropped during a blocked round) survives everything. The documented claim "Join ticks that arrive during a blocked round coalesce" (`10_srp_engine.md:506-507`) is only half pinned: N13 pins completion, not the coalesced tick. The impact is at most one T-MRP-JOIN of delay.
- (b) `r-mvrp-start-during-prepare` (`KL_srp_encoder.sv:332`) survives. The same-cycle MVRP/prepare arbitration is unpinned.
- (c) `tb/srp_stream_fsms/README.md:151-152` says "12 of 1215 FAIL", but the mutated runs total 1203 and 1211 checks, both in the published log and in my re-run.
- Consider pinning (a) and (b), or stating them as intended limits.

### F4 — SUGGESTION — lenses: Conformance
- **Where:** issue #127 Proof, "The parent analysis harness … must no longer reproduce a non-stop". Evidence: `author/parent-original-oracle.log` (rc=1 at this head) and `author/run_parent.py`, which depends on an unpublished `606-a392` directory and a `/tmp` file.
- **Suggestion:** record on the issue that the unmodified helper's LV-anchored race is the legitimate post-`sLA` LV path, under the #608 IN-registrar decision, and that the deadline-anchored oracle is the accepted proof. Publish the harness source so a third party can re-run it.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #127 scope/decisions; #608 analysis/decision; 802.1Q Table 10-4/10-5, §10.8 as quoted in 10 §6.5; RTL `sLA` path; probes R1 (head vs base), R4; author K/L/M results; parent replay logs | R375-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| RTL | CLEAN | full diff of `KL_srp_top.sv`, `KL_srp_encoder.sv`, both stream FSMs; `KL_pp_tx_slots.sv` handshake; `KL_srp_domain.sv`/`KL_srp_vlan.sv` interplay; lint (pinned); pp_top suite | R375-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Robustness | CLEAN | probes R3–R7 (join-start edge, parking/MVRP, encoder-busy cancel, new intent during a canceled preparation, sink edge); author M/N groups; reset/backpressure/full-table cases | R375-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | 6 SRP-related suites at head plus base srp_top; 36 author mutants and 5 controls re-executed; 11 reviewer mutants × full suite and probes; the `sim_main.cpp`/`mutants.py` diff; manager parent-gate comment | R375-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Docs | CLEAN (F3(c) suggestion only) | `10_srp_engine.md` §6.5 diff; RTL banners/port comments; srp_top/srp_encoder/srp_stream_fsms READMEs; searches of guides/02/08/09; `make links matrix modmatrix params` | R375-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |

## Real limits

- **Simulator path.** The requested path was absent; I used the byte-identical per-head wrapper (Verilator 5.050), as recorded above.
- **Parent harness.** Its source (`reproduce.cpp`, `run_reproduction.py`) is not in any public branch I searched, so I did not re-run it. The parent-replay conclusion rests on my own base-versus-head replay inside the processor's srp_top bench, plus the published logs.
- **Parent consumer gates, full banks, hosted/act acceptance.** Not run by me, as instructed. F1 relies on the manager's bank results, confirmed by source inspection.
- **Hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. No bench or CRF STREAM_STOP measurement was done.
- **Documentation gates.** `make lint`, `wavedrom-check` and `stale` were not run: they need diagram tooling or git metadata in the extraction. The PR changes no diagram or WaveDrom source, and the hosted docs-gates job passed at this head.
- **Scale of the residual window.** The 457-cycle `sLA`-to-wire window is measured on the tb's instant-accept TX BFM. Real arbiter or MAC contention lengthens it; that is the documented LV path.

## Pending manager duties

1. Resolve F1: re-run the parent consumer gates (11/11) at the next head, and then pin adoption with the CRF frame/STREAM_STOP integration regression required by the issue.
2. Rule on F4 (the proof item wording and the reinterpretation of the parent harness), and ideally publish the harness.
3. Build and gate the final current-dev candidate at the merge turn (source base `16be6768`, live dev `931f396e`), which is distinct from this source validation.
4. Own the hosted/act acceptance. The 6 hosted runs at this head executed and succeeded.
5. Schedule the bench re-measurement (100/100 disconnects stop, and STREAM_STOP counts each) for #608 acceptance 3.

R375-1 FINISHED
