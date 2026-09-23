[R270] NEGATIVE - exact head fc155c3ca28b04c2220bf41ebea9214379210452

Round R270-1, internal cleared-context independent review of protocol-processor issue #106 / PR #107.
Head `fc155c3ca28b04c2220bf41ebea9214379210452`, tree `6bd2fef51217a82f281deb14f3f975e39a6efdc5`, base `fbc1f7156d711e5b7f511da8a16d9494256b017b` (two commits: `9370f8ab` transmit half, `fc155c3c` receive half).

Verdict: NEGATIVE on two open MINOR findings (F1 Tests, F2 Docs). Conformance, RTL and Robustness are covered clean at this head. The change itself is correct: nothing in this round found a defect in the RTL, and every conformance point I checked holds, including both of the author's calls for reviewers. What remains is one untested boundary of the new receive gate and one documentation contradiction.

## 1. Reconstruction order and inputs

1. Contribution rules: the donor has no AGENTS.md or CONTRIBUTING.md, so the parent's (kebag-logic/milan-fpga @ `759da623`) AGENTS.md sections 2, 6 and 7 and CONTRIBUTING.md section 6 apply. These set the lens definitions, the severity scale, the ledger rule, the em-dash rule and the role-naming rule. Donor docs: `README.md`, `docs/README.md`, `.github/workflows/hdl.yml`.
2. Issue #106: the body (the task and its frozen acceptance), and the comments in order. These are the ASSIGNMENT, TAKEN and DECISION (per-type scope) comments, REVIEW READY (transmit), the manager's scope DECISION adding the receive half (issuecomment-5798176959) and REVIEW READY (both halves).
3. Requirements quoted by the issue and PR: IEEE 802.1Q-2014 clauses 10.6, 10.7.5.20 (NOTE and b)2)), 10.7.9 Table 10-5, 10.8, 10.8.1.2, 10.8.2.6, 10.8.2.8 f/g and 10.8.2.10.1 NOTE. Milan v1.2 Table 4.3. Donor authority: `docs/architecture/10_srp_engine.md` sections 3, 6.4 and 6.5, and F10.9.
4. The diff `fbc1f715..fc155c3c` (16 files, +1325/-98), each commit separately, and the full files `hdl/srp/KL_srp_{encoder,decoder,top,talker_fsm,listener_fsm}.sv` and `srp_pkg.sv` at head.
5. Public evidence: milan-fpga `5e7eb309` `review-evidence/pp106-r1`. That covers the manager's `donor-full` and `parent-consumer` banks, the author's arm definitions (`mutate_rx.py`) and the Run B capture. The original capture is at `160debeb` (blob `bf2e79ee`). Also read: exact-head hosted checks on the donor.
6. Prior public review findings on PR #107: **none exist at this head**. The PR has one comment (the review-start notice), no reviews and no inline comments. Issue #106 has no reviewer findings. So there is nothing to resolve or retain. No other reviewer's report was read before this verdict and ledger were written.

## 2. Conformance judgement

**Transmit (`9370f8ab`).**
- The first VectorHeader of each of the four MSRP types carries LeaveAllEvent (`KL_srp_encoder.sv:153`, `:402-408`).
- Each type with no drained vector gets a LeaveAll-only message after the drained ones (`:409-417`, `:679-689`). That message has NumberOfValues 0, a zero FirstValue of the full AttributeLength, no packed events and AttributeListLength = AttributeLength + 4.
- This meets 802.1Q-2014 10.7.5.20 NOTE ("a LeaveAll Attribute for each Attribute Type supported by the application") and 10.8.2.8 f/g. MVRP has one type and is unchanged.
- Independent evidence:
  - The LeaveAll-only bytes are byte-identical to the bench AVB switch's own LeaveAll-only messages in the original Run B capture (10.429430 s, 93 B tail). See `receipts/compare-test-bytes.txt`.
  - The base encoder suite run on the head RTL differs only in the three E7 LeaveAll-shape checks, so frames without LeaveAll are unchanged (`receipts/diff-base-encoder-suite.txt`).
  - The largest possible LeaveAll MRPDU (12 lone Talker Failed entries plus three LeaveAll-only messages) is 528 B, byte-exact against the suite's packer. The elaboration bound is 558 B and the standard slot is 576 B (`receipts/probe-W-encoder-worst-case.txt`).

**Receive (`fc155c3c`).**
- The decoder strobes one lane per AttributeType: `la_msrp_o[type-1]` and `la_mvrp_o` (`KL_srp_decoder.sv:205-210`, `:402-409`). Each lane fires once per MRPDU and re-arms at every MRPDU's first byte (`:334`).
- `KL_srp_top` routes the lanes as follows:
  - Domain lane to the Domain participant only (`KL_srp_top.sv:347`).
  - The other MSRP lanes to both stream FSMs (`:511`, `:594`), where each machine selects its own type (`KL_srp_talker_fsm.sv:416-421`, `:630`; `KL_srp_listener_fsm.sv:413-420`).
  - MVRP lane to VLAN only (`:405`).
- This matches 10.8.2.6 and 10.7.5.20 b)2). An own LeaveAll still ages every registrar (10.7.9).
- Once per MRPDU is the literal reading of rLA!, which is an event of receiving an MRPDU that contains a LeaveAll of the type.
- Decoder events and lane strobes are both registered decoder outputs and are at least two cycles apart. No FSM arbitration can therefore reorder a lane against its own vector's events.

**Evidence the issue's decision rests on, re-derived** (`receipts/runb-msrp-check.txt`, from the original capture: sha256 `febe8a16...`, git blob `bf2e79ee`).
- There are 189 MSRP frames and 18 LeaveAll MRPDUs.
- The DUT's 9 LeaveAll MRPDUs flag Domain only.
- The bench AVB switch re-declares Domain 0.3-3.8 ms after each of them (9 of 9). It sends no Listener re-declaration as a LeaveAll reply.
- The switch's own 9 LeaveAll MRPDUs flag every MSRP type.
- The published copy is path-redacted (sha256 `9c2144ec...`, disclosed in the packet MANIFEST). It differs in 7 records, none of them MSRP.
- The decoder suite's 109-byte transcription (test P) equals the switch's MRPDU at 47.029619 s byte for byte.

**The author's two calls for reviewers.**
- *Applicants routed per type too*: accepted. 10.7.5.20 b)2) scopes rLA! for the Applicant, Registrar and LeaveAll state machines alike.
- *The unflagged-vector-first layout falls back to wire (DLSDU) order*: accepted as conformant.
  - 10.8 requires Messages in a PDU to be processed in DLSDU order, and the LeaveAllEvent is carried in a VectorAttribute.
  - For every layout a conformant sender produces (10.6, 10.8 NOTE 2), the result equals the scope decision's "before that MRPDU's attribute events".
  - The bench AVB switch never sends the other layout.
  - The head RTL does exactly what docs 10 section 6.5 lines 390-393 state (probe Z1/Z2 below). The suite does not pin it, which is F1.
  - The manager should record acceptance of this reading against the scope decision's literal wording (section 7).

**Failing arms and the two changed `srp_top` stimuli** (`receipts/replay-arms.txt`, `receipts/mutation-probes-author-arm-replays.txt`).

Author arms replayed, with the author's published count:

| Arm | What it plants | FAIL here | Author's count |
|---|---|---|---|
| M0 | base encoder | 146 | 146 |
| RX0-dec | first-commit decoder | 19 | 19 |
| RX0-top | first-commit receive side | 5 (F5a/b/c) | 5 |
| D2 | once-per-MRPDU gate removed | 8 | 8 |
| T2 | talker registrar deaf to the Listener lane | 16 | 16 |
| P2, own variant | Domain takes no received lane | 2 (F4, F5b) | 1: the author's P2 routes the Listener lane to Domain instead; both fail |

- The arms are real and fail for the property each one claims.
- STIM-old: the head RTL under the pre-change F2/F4 stimuli fails exactly 5 checks: F2 four times, F4 once. These are the per-application reading.
- RX0-top shows that the new stimuli pass under the previous routing, and that F5 separates the two routings.
- The stimulus change is therefore forced by the conformant routing and weakens no assertion. F5b now covers the Domain-only case that F2 used to exercise.

**Donor gates.**
- The manager's `donor-full` bank at this head exits 0 on every command:
  - lint: every module OK;
  - `run_suites`: 30 suites, 15,436 checks, 0 failing;
  - `make check`, `gen_matrix --check`, Yosys (32 tops plus Xilinx) and the nvm_port figures: OK.
  - Its whitespace step checked the wrong range (section 7).
- Hosted `hdl`, push and pull_request runs: `suites`, `docs-gates` and `portability` all executed and succeeded at the exact head. No context was skipped (`receipts/hosted-checks.txt`).
- Reviewer re-runs:
  - SRP-family suites at head under the pinned simulator: 556/150/1068/252, 0 FAIL;
  - scoped zero-tolerance lint of the five changed modules: OK;
  - links, matrix and module matrix: OK;
  - `git diff --check fbc1f715..fc155c3c`: clean.

**Out of scope, disclosed.** The own leavealltimer does not restart on a received LeaveAll. 802.1Q-2014 Table 10-5 maps rLA! to "Start leavealltimer, Passive", and 10.6 says the same in prose.
- This behavior predates the PR and is unchanged by it.
- The maintainer's scope decision keeps it, and docs 10 section 6.5 lines 402-411 record it as an open deviation.
- It is not a finding against this head, because the frozen acceptance of #106 does not cover the timer. The decision's premise ("as the standard's timer rules require") is contradicted by the clauses it asked to be stated, so an owner re-decision is pending (section 7).

## 3. Findings

### F1

`[R270] MINOR Tests - hdl/srp/KL_srp_decoder.sv:334,405-406 with tb/srp_decoder/sim_main.cpp (tests L, P, Q, R, S) - the once-per-MRPDU gate's two boundaries are unpinned`

- **Severity:** MINOR.
- **Lenses:** Tests.
- **Authority/evidence.** The parent AGENTS.md Tests lens requires that each new test can fail for its defect and that negative and boundary behavior is covered. Docs 10 section 6.5 lines 375-377 and 390-393, and the decoder banner lines 41-54, define the gate's behavior. Two single-point mutants of the new gate pass every donor check (`receipts/mutation-probes.txt`):
  - **X1**: the gate is armed by any VectorHeader of the type, so a flagged vector that follows an unflagged one of its type in the same MRPDU is silently dropped. This is the documented DLSDU-order layout, the author's call #2. Result: srp_decoder 150/150 PASS and srp_top 252/252 PASS.
  - **X7**: the gate is cleared only by a well-formed dual EndMark, so a LeaveAll in the MRPDU after a malformed or discarded one is dropped. Result: srp_decoder 150/150 PASS.
- **Head behavior is correct.** Three reviewer checks (`receipts/probe-Z-decoder-gate-boundaries.txt`) pass on the head (156/156). Z1 is `[L JoinIn][L LA JoinIn]` and must give `E3 L3 E3`. Z2 is `[L JoinIn][D LA][L LA n=0]` and must give `E3 L4 E4 E4 L3`. Z3 is a flagged vector truncated mid-FirstValue, then a good Listener LeaveAll MRPDU. The same checks fail on X1 (3 FAIL) and on X7 (1 FAIL).
- **Impact.** Suppose a later change drops a peer's LeaveAll in either case. The 10.7.5.20 b) rLA! event would not occur, registrations of that type would stay IN through a LeaveAll cycle they should have aged in, and every gate would stay green. The reading reviewers were asked to accept (call #2) is asserted only in prose.
- **Required outcome.** Decoder tests that pin both boundaries with full strobe timelines:
  - the lane fires at a flagged VectorHeader that follows an unflagged one of its type, in the same message and in a later message;
  - the lane re-arms after a malformed or discarded MRPDU.
  - Each is shown to fail under an X1-class and an X7-class mutant respectively.
- **Verification.** srp_decoder passes at the new head. `scripts/mutation_probes.py <clone> <new head> <scratch> <verilator dir> X1 X7` reports FAIL for both.

### F2

`[R270] MINOR Docs - docs/10_RESOURCE_AND_EFFORT.md:554-557 against docs/architecture/10_srp_engine.md:402-411 and hdl/srp/KL_srp_top.sv:71-74 - the doc set contradicts itself on received-LeaveAll timer restart`

- **Severity:** MINOR.
- **Lenses:** Docs.
- **Authority/evidence.**
  - `10_RESOURCE_AND_EFFORT.md:554-557` lists, among the consumer's defects "where this spec is right", that it has "no restart or Passive behaviour on a received LeaveAll (802.1Q Table 10-5)".
  - This PR's section 6.5 text and the `KL_srp_top` banner now state that this processor does **not** restart its leavealltimer on a received LeaveAll, and call that an open deviation from the same Table 10-5.
  - The PR body ("Open, for the owner", item 1) acknowledges the contradiction and leaves it.
  - The parent AGENTS.md section 7 requires that "authoritative documentation is current". Its Docs lens requires that changed contracts are reflected in the docs.
- **Impact.** A reader comparing this spec with the consumer, or checking Table 10-5 conformance, gets opposite answers from two documents at the same head. The claim predates the PR, but the PR's own section 6.5 text is what now contradicts it.
- **Required outcome.** `10_RESOURCE_AND_EFFORT.md` no longer credits this spec with restart or Passive on a received LeaveAll. The 10-15 s randomisation claim may stay. For example, the sentence could point to 10 section 6.5 for the open deviation.
- **Verification.** Read the edited lines against 10 section 6.5. Run `python3 scripts/check-links.py` and `make check`.

### Suggestions (do not affect the verdict)

**S1**

`[R270] SUGGESTION Tests - hdl/srp/KL_srp_top.sv:347, tb/srp_top/sim_main.cpp F5 - the Domain row of the routing table has no negative check`

- Mutant X2 (the Domain participant takes every MSRP lane) passes srp_top 252/252.
- Consequence: a spurious Domain JoinIn after a non-Domain LeaveAll. This is harmless on the wire, which is why it is only a suggestion.
- F5c could assert that no Domain re-declaration follows a Listener-only LeaveAll before the next periodic.

**S2**

`[R270] SUGGESTION Docs - docs/architecture/10_srp_engine.md:409-410 - the timer deviation needs a live tracker`

- The text says the deviation is "recorded there [issue #106] as open".
- #106 closes on this PR's merge ("Closes #106"), and its scope decision records the opposite premise.
- Parent AGENTS.md: "Newly discovered work becomes another public Issue". A new public issue, referenced from section 6.5, would keep the deviation visible.

**S3**

`[R270] SUGGESTION Docs - hdl/srp/KL_srp_encoder.sv:149-152, docs/architecture/10_srp_engine.md:343-344 - state the clause's criterion`

- The constant `4'b1111` is justified by elaboration shape ("every legal elaboration has at least one sink and one source") and by "every type the participant registers".
- The Domain type has no registrar here (section 6.5 table). The criterion that makes `4'b1111` correct is 10.7.5.20 NOTE's "each Attribute Type supported by the application".

## 4. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #106 body and both decisions. `KL_srp_encoder.sv:149-154,402-417,531-712`. `KL_srp_decoder.sv:205-210,331-335,391-409`. `KL_srp_top.sv:347,405,511,594`. `KL_srp_talker_fsm.sv:408-421,619-631`. `KL_srp_listener_fsm.sv:400-420,691-697`. Checked against 802.1Q-2014 10.6, 10.7.5.20, 10.7.9, 10.8, 10.8.1.2, 10.8.2.6 and 10.8.2.8 f/g. The Run B capture decode (`receipts/runb-msrp-check.txt`, `receipts/compare-test-bytes.txt`, `receipts/diff-base-encoder-suite.txt`). Calls #1 and #2 accepted. | R270-1 | `fc155c3ca28b04c2220bf41ebea9214379210452` |
| RTL | CLEAN | The five changed modules plus `srp_pkg.sv:70-76`. Checked: widths end to end (4-bit lanes, scoped lint clean in `receipts/lint-changed.txt`); lane index = type-1, guaranteed by `len_ok_w`; reset values of `la_done_r`, `la_act_r` and `la_seen_r`; the encoder FSM arcs `E_VFV->E_MSGCLOSE` (NoV 0) and the `E_PATCH` append loop; `WORST_BYTES_C`, 558 B against a measured 528 B (`receipts/probe-W-encoder-worst-case.txt`); the pending-latch/start-cycle ordering; no CDC touched. Yosys OK in manager `donor-full/07.log` and in hosted `portability`. | R270-1 | `fc155c3ca28b04c2220bf41ebea9214379210452` |
| Robustness | CLEAN | Malformed and truncated input: the gate re-arms after a malformed MRPDU (probe Z3 passes at head). Unusual ordering: unflagged-first layouts in DLSDU order (probes Z1/Z2 pass at head). Maximum frame (probes W1-W3). Mid-drain and start-cycle LeaveAll (L5/L6). Repeated flags in one MRPDU (S). Reset of the new state. Parent consumer: no direct instantiation of the changed modules at `759da623` (`receipts/parent-consumer-scan.txt`). | R270-1 | `fc155c3ca28b04c2220bf41ebea9214379210452` |
| Tests | UNCLEAN (F1 open; S1) | `tb/srp_{encoder,decoder,stream_fsms,top}/sim_main.cpp` and their READMEs; head tallies 556/150/1068/252 (`receipts/head-srp-suites.txt`); author arm replays; 6 own mutants (X3, X4, X5 caught; X1, X2, X7 survive); boundary probes Z1-Z3. | R270-1 | `fc155c3ca28b04c2220bf41ebea9214379210452` |
| Docs | UNCLEAN (F2 open; S2, S3) | `docs/architecture/10_srp_engine.md:307-411`; the `KL_srp_top`/`KL_srp_decoder`/`KL_srp_encoder` banners; the tb READMEs (counts match the measured tallies); `docs/10_RESOURCE_AND_EFFORT.md:554-557`; docs gates re-run (`receipts/docs-gates-head.txt`); PR/issue evidence sufficiency. | R270-1 | `fc155c3ca28b04c2220bf41ebea9214379210452` |

Clean-lens lines:

- `[R270] PASS Conformance - KL_srp_encoder.sv:402-417,679-689; KL_srp_decoder.sv:205-210,402-409; KL_srp_top.sv:347,405 - per-type LeaveAll on transmit and receive against 802.1Q-2014 10.7.5.20 NOTE/b)2), 10.8.2.6, 10.8.2.8 f/g, 10.8; LeaveAll-only bytes equal the bench AVB switch's captured bytes`
- `[R270] PASS RTL - the five changed modules and srp_pkg.sv:70-76 - widths, lane indexing, reset, FSM arcs, the slot bound (528 B measured against 558 B bound and 576 B slot); scoped lint and Yosys clean`
- `[R270] PASS Robustness - probes Z1-Z3 and W1-W3 at head; L5/L6/S tests; parent consumer scan - malformed, reordered, maximum-size, mid-drain and repeated-flag cases behave as documented`

## 5. Receipts (all under this packet, listed in `MANIFEST.sha256`)

- `scripts/run_srp_suites.sh` runs the SRP-family suites in a disposable `git archive` export, with the build capped at 8 jobs. Receipt: `receipts/head-srp-suites.txt`.
- `scripts/lint_changed.sh`: `receipts/lint-changed.txt`.
- `receipts/diff-check.txt` is `git diff --check` over the PR range. `receipts/docs-gates-head.txt` holds the links, matrix and module-matrix gates.
- `scripts/runb_msrp_check.py` and `scripts/compare_test_bytes.py`: `receipts/runb-msrp-check.txt` and `receipts/compare-test-bytes.txt`.
- `scripts/probe_encoder_worst_case.py`: `receipts/probe-W-encoder-worst-case.txt`.
- `scripts/mutation_probes.py`: `receipts/mutation-probes.txt` (X1-X5, X7) and `receipts/mutation-probes-author-arm-replays.txt` (D2, P2, T2).
- `scripts/probe_decoder_gate_boundaries.py`: `receipts/probe-Z-decoder-gate-boundaries.txt`.
- `scripts/replay_arms.py`: `receipts/replay-arms.txt` (M0, RX0-dec, RX0-top, STIM-old).
- `receipts/diff-base-encoder-suite.txt`, `receipts/hosted-checks.txt` and `receipts/parent-consumer-scan.txt`.
- `scripts/verify_clone.sh`: `receipts/clone-integrity.txt`.

The simulator is the manager-provided scoped wrapper. It reports `Verilator 5.050 2026-07-01 rev v5.050`, the CI pin. The host default (5.052) was not used.

Clone integrity after all probes (`receipts/clone-integrity.txt`):
- HEAD, tree and index tree all equal the head;
- all 224 tracked entries match their recorded blob and mode;
- no gitlinks are recorded and the donor has no `.gitmodules`, so no submodule gitlink was required;
- no untracked or ignored files exist.

Every probe ran in a disposable export under the packet's `scratch/`, never in the clone.

## 6. Real limits

- The specification PDFs are not in either repository. Clause wording was judged against the text quoted by the issue, PR and docs, together with the reviewer's knowledge of the 802.1Q-2014 clause structure (Table 10-4 and Table 10-5 rows, 10.7.5.20), not re-read from the standard.
- By rule, no full banks were run: no full donor `run_suites`, no Yosys, no nvm figures and no parent banks. For those, this round relies on the manager's public `donor-full`/`parent-consumer` receipts and the exact-head hosted runs.
- No hardware was used, and physical calibration was NOT RUN. The parent builder's gate 11 (calibration) is reported NOT RUN in manager `parent-consumer/06.log`. The capture analysed is the historical pre-change Run B, not a post-change silicon run. Field skips are not hardware proof.
- The #530 end-to-end harness was not rerun at `fc155c3c`, by the author or by this round. The author ran it at `9370f8ab`. The receive-side mechanism is covered in the donor only by `srp_top` F5.
- The mutants are single-point textual changes, a sample and not an exhaustive set. Of the author's 15 receive-side arms, 4 were replayed exactly (RX0-dec, RX0-top, D2, T2) plus a variant of P2; the rest rely on their published logs.
- The capture analysis re-derived the transcriptions and the per-type scoping pattern. It did not re-derive the burst-end timing table of the DECISION comment.

## 7. Pending manager duties

1. Build and validate the final current-dev candidate at the merge turn: source base `fbc1f715`; parent live dev `759da623`. The parent consumer gates with the gitlink staged at `fc155c3c` are already public and all exit 0 (xvlog 4 findings = ratchet; pp_shadow 371/0). Builder gate 11 is NOT RUN.
2. The `donor-full` bank's step 09 ran `git diff --check f70ba36e..e0c43b03`, which is PR #103's range, not this PR's. This round's receipt over `fbc1f715..fc155c3c` is clean. Use the PR range in the final bank.
3. Record the manager's acceptance, or not, of call #2 against the literal wording of the scope decision (issuecomment-5798176959). Obtain an owner re-decision on the leavealltimer no-restart deviation, whose stated premise the cited clauses contradict, and give it a live tracker (S2).
4. At parent adoption, `docs/traceability/ieee8021q.md` row MRP-5 ("on rx/tx LeaveAll, all registrations enter leave-pending") will describe per-application receive semantics that this head replaces.
5. Issue acceptance outside source: the parent adopts the exact reviewed head, and a #530 silicon rerun shows a bound CRF talker streaming continuously across LeaveAll cycles. Hosted/act acceptance is owned by the manager.
6. A new head answering F1/F2 un-covers Tests and Docs, and any lens whose artifacts it touches. It needs a re-review at that head.

R270-1 FINISHED
