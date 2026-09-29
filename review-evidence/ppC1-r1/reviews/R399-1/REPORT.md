[R399] POSITIVE - exact head 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b

# R399-1: external independent review of processor PR #133 (lane C1: issues #29, #108, #64, #65)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #133, round R399-1.
- Exact head `81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b`, tree `de5b0878d1846d1f0e478d11f2995429ef8da6d7`.
- Source base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. Four commits: `6356352`, `45836ad`, `bff4417` and `81b8d6d`.
- **Review clone.** Detached at the exact head and never edited.
  - After the review it has no tracked, untracked or ignored changes.
  - The `ls-files -s` digest is recorded in `receipts/clone-integrity.txt`. It was re-verified at the end of the review in `receipts/clone-integrity-final.txt`: 322 entries, digest unchanged, clean porcelain including ignored files, `diff-index` rc 0.
  - The processor has no `.gitmodules` and no mode-160000 gitlinks.
- **Scratch copy.** All builds, mutants and probes ran in a `git archive` copy under `scratch/`. Its 322 tracked files are byte-identical to the head.
- **Verdict basis.** There is no open BLOCKER, MAJOR or MINOR finding. Three SUGGESTIONs (S1-S3) are recorded, and none of them blocks.

## 1. Reconstruction (what was read, in order)

1. **Contributor guidance.** The processor has no `AGENTS.md` or `CONTRIBUTING.md`. The conventions used were:
   - `README.md` and `docs/README.md` (ID registries, single-source rules, citation style);
   - the `hdl/` banners;
   - the tb READMEs.
2. **Frozen scope.**
   - Issue bodies: #108 (acceptance 1-3), #29 and its duplicate closure, #64 (acceptance 1-4) and #65 (acceptance 1-3).
   - The lane assignment on #108 (comment 5883702094): items 1-4, the #65 STOP conditions and the gates.
   - Issue #106: its body, the scope decisions (per-type receive routing), the reference-switch capture record, and the correction that created #108.
3. **Requirements and interfaces, as cited in the tree.**
   - 802.1Q-2014: Table 10-5 rLA!, 10.6, 10.7.4.3, and 10.7.5.20 b)1)/b)2) with its NOTE.
   - Milan v1.2: Table 4.3, 4.2.7.3, 4.3.2 and 4.4.1.
   - Architecture docs: 10 §6.2, §6.3 and §6.5, and 08 F08.1.
   - The integrator guide's `srp_active_o` row.
   - The `KL_pp_timer_service` arm/expiry contract.
   - The top-level arm-port priority mux (`hdl/top/protocol_processor_top.sv:2608`).
4. **Code and tests.**
   - `git diff c951a9ff..81b8d6d7`: all of `hdl/`, all tb changes, all 22 mutation patches and the docs.
   - `KL_srp_encoder`'s FSM in full (push blocking, drain snapshot, E_TXREQ), and `KL_srp_vlan` in full.
5. **Public evidence.**
   - milan-fpga `a6427910`, `review-evidence/ppC1-r1`: MANIFEST, HANDOFF.md and PR-BODY.md. The published SHA-256 values match the MANIFEST.
   - Branch `ppC1-review-evidence` at `95e6b511`: the author's processor, parent and attribution result lines, and the parent re-base diff.
   - Hosted check runs at the exact head.
   - Read-only parent files at live dev `57b8c867`:
     - `sim_crf_licence.cpp`;
     - `docs/traceability/ieee8021q.md`;
     - `docs/reference/MILAN_COMPLIANCE_MATRIX.md`;
     - the `protocol-processor` gitlink, which is still `c951a9ff`.
6. **Independence.**
   - No private author material, lane scratchpad or management directory was read.
   - A same-round internal report (R398-1) was posted on the PR during this review. It was not read.
   - PR #133 has no prior-round review findings: it has no reviews and no review comments, and its only comments are the two review-start notices. So no earlier finding needed to be resolved or retained.

## 2. Judgement per assigned item

### (1) `6356352`: a received LeaveAll restarts the leavealltimer and goes Passive (#29 = #108)

**The change.** `KL_srp_top.sv:1224-1232` implements Table 10-5 rLA! ("Start leavealltimer, Passive", in both states).
- **Start.** Any MSRP lane (`|dec_la_msrp_w`) or the MVRP lane sets that application's `need_draw_r`. That requests a fresh kind-3 draw (10-15 s), counted from the peer's LeaveAll.
- **Passive.** The same lanes drop the pending own action:
  - MSRP: `la_msrp_pend_r` is cleared and `la_cancel_r` is set;
  - MVRP: the new `la_mvrp_pend_r` is cleared.
- **Accepted sLA.** An own sLA that the arbiter has already accepted is never retracted, as documented.
- **Begin!** Reset arms both timers (`need_draw_r <= 2'b11`, `:1178`).
- **MVRP flag.** It now waits in `la_mvrp_pend_r` and rides the next MVRP drain with content (`:1194-1197`). Before, it was latched in the encoder and could not be dropped.

**Stale-expiry guard.** `la_rearm_w` (`:1020-1024`) ignores an expiry of the superseded deadline while the re-arm is outstanding.
- A genuine expiry disarms its slot, so the guard never swallows one. M10, P3 and P6 pin this.
- The guard is correct wherever the timer arm reaches `KL_pp_timer_service` within two clocks of being issued. That holds in tb/srp_top and in the product top when its arm queue is idle.
- S1 covers arm-path latencies above two clocks.

**Per-application interpretation: judged acceptable and consistent with #106.**
- #106 scoped the *aging* effect of a received LeaveAll per Attribute Type, for registrars and applicants.
- The LeaveAll state machine itself "operates on a per-application (not per-Attribute Type) basis", and its own LeaveAll must cover "each Attribute Type supported by the application". This is the 10.7.5.20 NOTE, as quoted in #106.
- For a machine with no type of its own, reading "the type associated with the state machine" (10.7.5.20 b)2)) as every type of the application is the literal reading.
- The reading keeps the two applications apart, per b)1).
- Against a conformant peer it gives exactly 10.6's one LeaveAll per cycle. The reference switch is such a peer: #106's capture shows it flagging all four MSRP types.
- The residual case of a peer that flags only some types is recorded as S3.

**Tests.**
- P1 is the F4-style probe: peer LeaveAlls at 1 Hz for 20 cycles.
  - No own MSRP LeaveAll is sent.
  - After the last peer LeaveAll, the own LeaveAll resumes 10-15 s later.
- P2 is the MVRP mirror of P1.
- The restart is pinned per lane (P3) and on the wire (Q4).
- The mutant that restores expiry-only re-draw, `expiry-only-redraw`, is killed by 15 checks (P1, P3). Its MVRP twin, `mvrp-expiry-only-redraw`, is killed by 6.

**Docs.**
- docs 10 §6.5 drops the deviation. It states the interpretation with 10.7.5.20 b)1)/b)2) and the NOTE, Table 10-5 and 10.6.
- `docs/10_RESOURCE_AND_EFFORT.md` item 11 and the F08.1 `T-MRP-LEAVEALL` row agree with the implementation.

**Result.** #108 acceptance is met. The parent re-base remains a pending manager duty.

### (2) `45836ad`: MRP timers graded in tb/srp_top against Milan Table 4.3 (#64)

**Method.** Every MRPDU is stamped with `now_ms_o` at its last byte. The grading reads the wire only, never DUT registers.

| Check | What is graded | Required | Measured |
|---|---|---|---|
| Q1 | joinTime: the ladder New, New, JoinMt | 180-240 ms apart | 200, 200 ms |
| Q2 | periodic re-joins: Talker JoinMt, Domain JoinIn and MVRP VID JoinIn | every 900-1500 ms | 9 of each at 1000 ms |
| Q3 | first own LeaveAll after arming (MSRP / MVRP) | ≥ 10 s | +14.2 / +10.6 s |
| Q3 | consecutive own LeaveAlls, no peer LeaveAll (MSRP / MVRP) | 10-15 s apart | 10.0-12.8 / 11.0-13.2 s |
| Q4 | next own LeaveAll after a peer LeaveAll (MSRP / MVRP) | ≥ 10 s | 11.0 / 14.5 s |

**Grid argument.** The README says that grid alignment keeps the wire spacing inside 10-15 s. This is correct:
- the join grid is 200 ms;
- the draws are whole milliseconds;
- the range ends, 10000 and 15000 ms, are multiples of 200.

So an aligned spacing cannot fall outside [10000, 15000].

**Mutants.** The three required mutants are each red here and recorded in `tb/srp_top/README.md`:

| Mutant | Fails |
|---|---|
| `join-ms-400` | Q1, Q2 |
| `periodic-ms-3000` | Q2 |
| `draw-kind-0` | Q1-Q4 |

**Result.** #64 acceptance items 1-4 are met.

### (3) `bff4417`: MVRP join before the stream (#65)

**Design.** Three pieces:
- **Encoder.** `KL_srp_encoder.sv:781` strobes `tx_mvrp_o` when the TX arbiter accepts an MVRP MRPDU.
- **VLAN table.** `KL_srp_vlan.sv` keeps a `queued` and a `sent` bit per entry:
  - on the strobe, `sent |= queued` (`:208-211`);
  - `queued` is set when a New is handed over (`:286`) and when a re-join JoinIn is handed over (`:309`);
  - allocation and retirement clear both bits;
  - `vid_sent_o = active & sent` (`:329`).
- **Talker FSM.** `KL_srp_talker_fsm.sv:804-824` ANDs one more term into ACTIVE: some live, sent entry holds `vid_r[s]`.

**Soundness.** The claim "a push accepted before the drain started is in that MRPDU" was verified in the encoder:
- MVRP pushes are refused from E_ALLOC through E_TXREQ, and on the start cycle (`busy_app_w` and `start_tgt_w`, `:337-349`).
- `drain_n_r` snapshots the count at start.
- The table is cleared at commit.

Therefore no MVRP push can land on the strobe cycle, and every queued join is inside the MRPDU that was accepted. The VLAN FSM serializes user ops and re-join walks, so `free_ix_r` and `ridx_r` are stable wherever they are used.

**Stick-closed probe.** `scripts/probe_licence.py` adds a read-only wrapper output for `vid_ok_w`; the RTL is not changed. Results are in `receipts/probe-licence.txt` (8/8 checks pass):

| Case | Stimulus | Result |
|---|---|---|
| S0 | fresh declaration | the term rises after 200 ms |
| S1 | 45 s of own MSRP/MVRP LeaveAll cycles, plus a peer MVRP LeaveAll every 3 s | the term never drops |
| S2 | a co-user joins and leaves the same VID | the term never drops |
| S3 | withdraw and immediate re-declare on the same VID | 0 ms (the ops collapse) |
| S4 | VID 2 → 7 → 2 | 142 ms, then 150 ms |
| S5 | the TX arbiter refuses for 1 s | closed throughout; rises 0 ms after release |
| S6 | link down, then up | the term is held |
| S7 | VLAN table full | behavior recorded, see S2 below |

**Every listed risk case recovers within one T-MRP-JOIN:**
- a VID change;
- removal of the last user;
- reset;
- an MVRP LeaveAll followed by re-declaration;
- a Ready registered before the first MVRP MRPDU. In R1, ACTIVE rises one clock after the VID 2 New is accepted, at 200 ms.

Only VLAN-table overflow (S7) strands the licence. That case is outside the documented envelope; see S2.

**Tests.**
- Talker half: R1-R3 in srp_top, the VID term in srp_stream_fsms, and W1-W5 in srp_encoder.
- Listener half: R4.
  - A byte-exact MVRP VID 7 New.
  - JoinIn every 1000 ms.
  - A byte-exact Lv when the last user leaves.

**Mutants: killed on both halves.**
- `licence-ignores-join`, `join-sent-at-handover` and `count-up-unsends`, each in srp_top and in the unit suites.
- `tx-strobe-any-app`.
- `listener-lane-cut`: `vu_sel_ls_w` forced to 0, the arm #65 acceptance requires.

**Result.** #65 acceptance items 1-3 are met. The published design evaluated both STOP conditions before implementation, and neither is met.

### (4) `81b8d6d`: parent C++ idiom fix

**The change.** Test code only, in `tb/srp_top/sim_main.cpp`:
- two functions are split out of long checks;
- a `Gaps` struct replaces two out-parameters.

**Behavior is unchanged:**
- srp_top reports 2149/2149 at both `bff4417` and `81b8d6d` (`receipts/suites/srp_top-at-bff4417.log`, `receipts/suites/srp_top.log`);
- the 19 RESTART, TIMER, JOIN and LEAVEALL_EXPIRY measurement lines are identical (same SHA-256);
- every mutant still fails on its named assertion.

**Not run here.** The parent's `check_cpp_idiom.py` belongs to the parent bank, which is out of scope for this review. The author's receipt reports rc 0.

### (5) Parent-visible list

**No interface change:**
- `protocol_processor_top.sv` changes only in comment lines (`:515-520`);
- `KL_srp_top`'s ports and parameters are unchanged;
- the new ports are internal to the encoder, the VLAN table and the talker FSM.

**Behavior that parents can see:**
- `srp_active_o` gains the Milan 4.3.2 term.
- The same term reaches side-port snapshot word 12, "per-source active" (`protocol_processor_top.sv:4297`), with the same meaning.
- The PR states the extra delay as "at most one T-MRP-JOIN". That bound leaves out TX-arbiter wait and VLAN-table overflow; see S2.

**Items the parent must re-base,** checked read-only at live dev `57b8c867`:
- `tb/verilator/milan_dp/sim_crf_licence.cpp:953,956` still assert `>= 4` for both the DUT's and the switch's LeaveAll MRPDUs.
- The author's attribution runs are public (`attr-results.jsonl`):

  | Processor | Parent | rc |
  |---|---|---|
  | base `c951a9ff` | unchanged | 0 |
  | head, with only the MSRP restart reverted | unchanged | 0 |
  | head | both counts re-based to `>= 3` | 0, full `milan_dp` |

**Parent docs to update at adoption:**
- `ieee8021q.md` MRP-5 still says "an open deviation, processor issue 108".
- `ieee8021q.md` MRP-4 describes ACTIVE's terms.
- `MILAN_COMPLIANCE_MATRIX.md` rows 4.2.7.1 and 4.2.7.3/4.4.1.

**Result.** The PR's list matches these items. As far as a read-only check can show, it is complete.

## 3. Lenses

**Conformance: CLEAN.**
- Table 10-5 rLA! (Start and Passive) is implemented per application, for both MSRP and MVRP.
- The interpretation is stated with its clauses and is compatible with #106.
- Milan Table 4.3 timers are graded on the wire.
- Milan 4.3.2 is enforced in the licence, and 4.4.1 is graded on the wire.
- The residual behavior with a peer that flags only some types is S3.

**RTL: CLEAN.**
- The encoder strobe and the VLAN `queued`/`sent` tracking agree with the encoder's push blocking.
- There is no same-cycle hazard between the strobe and a push.
- The `la_rearm_w` guard is correct at arm latencies of two clocks or less; S1 covers larger latencies.
- The zero-tolerance lint passes for every module.
- No top-level port changes.

**Robustness: CLEAN.**
- The licence stick-closed probe covers every listed case, and each recovers within one T-MRP-JOIN.
- The arm-latency sweep (S1) found no stale-expiry action at 0 or 2 clocks, which covers tb/srp_top and the idle product arm queue. At more than two clocks there is a window of about 4 clocks per event; it is negligible and harmless.
- VLAN-table overflow is outside the design envelope (S2).

**Tests: CLEAN.**
- Suites at the head, all with 0 FAIL:

  | Suite | Checks |
  |---|---|
  | srp_top | 2149 |
  | srp_stream_fsms | 1219 |
  | srp_encoder | 581 |
  | pp_top | 7751 |

- The full srp_top mutant campaign:
  - 10 of 10 controls pass;
  - 72 of 72 arms are KILLED by their named assertions;
  - assertion coverage is 63/63 (K L M N O P Q R), computed as the union of 8 chunks.
- Every required mutant is red.

**Docs: CLEAN.**
- Read against the code:
  - docs 10 §6.2, §6.3 and §6.5;
  - 08 F08.1;
  - `10_RESOURCE_AND_EFFORT.md` item 11;
  - the integrator guide;
  - the RTL banners;
  - the tb READMEs, whose tallies and mutant tables match what was measured.
- `make check` and `gen_matrix --check` pass.
- S2 and S3 suggest wording that would be more precise.

## 4. Findings

There are no BLOCKER, MAJOR or MINOR findings.

### S1: SUGGESTION. Lenses: Robustness, RTL, Docs

**Where:**
- `hdl/srp/KL_srp_top.sv:1016-1024`: `la_rearm_w` and its comment "Until that arm lands ...";
- `docs/architecture/10_srp_engine.md:600-603`;
- `hdl/top/protocol_processor_top.sv:2608-2700`: the arm queues, with fixed priority listener > talker > ADP > SRP.

**Authority.**
- Table 10-5 rLA! (Passive).
- `KL_pp_timer_service`'s arm shadow, which covers the arm cycle and the next one.

**Evidence.** `scripts/probe_arm_race.py` sweeps a peer MSRP LeaveAll across 83 clock offsets around the own expiry. The arm path is delayed N clocks before it reaches the timer service. Results are in `receipts/probe-armrace/`:

| Arm delay N | Offsets that produce an own LeaveAll |
|---|---|
| 0 (tb as-is) | 0 |
| 2 (the idle top-level queue) | 0 |
| 3 | 4 (offsets -11 to -8) |
| 4 | 4 (offsets -11 to -8) |
| 8 | 5 (offsets -14 to -10) |
| 16 | 5 (offsets -22 to -18) |

**Cause.** `la_rearm_w` falls when the cadence arm is *issued*, not when it lands in the timer. With more than two clocks of queueing, a superseded deadline can expire in that gap. It is then treated as a genuine expiry.

**Impact: negligible and harmless.**
- It needs two coincidences:
  - the peer LeaveAll falls inside a window of a few clocks in the old deadline's millisecond;
  - a higher-priority arm face contends at the top level. It cannot happen when the queue is idle.
- The effect is one own LeaveAll just after the peer's, which is the pre-#108 behavior. The timer is still restarted.

**Suggested outcome.** Either make the guard independent of latency, or document the assumption:
- for example, treat a LeaveAll-slot expiry as stale while `now_ms_i` is still before the intended deadline `cad_dl_r[slot]`;
- or state the at-most-two-clock arm-path assumption in the comment and in §6.5.

**Verification.** With the fix, the delayed-arm probe reports 0 offsets at N = 3, 4, 8 and 16, and M10, P3 and P6 stay green.

### S2: SUGGESTION. Lenses: Robustness, Docs

**Where:**
- The PR body's parent-visible list: the licence "differs from before only when a Listener Ready registers before that VID's first MVRP MRPDU, and then by at most one T-MRP-JOIN";
- `docs/architecture/10_srp_engine.md:239-249`;
- `hdl/srp/KL_srp_vlan.sv:263-265`: `user_err` when the table is full;
- `hdl/top/protocol_processor_top.sv:2323`: the `dbg_vlan_err_o` strobe is left unconnected.

**Authority.** Milan 4.3.2.

**Evidence,** from `receipts/probe-licence.txt`:
- **S5.** While the TX arbiter refuses, the licence keeps waiting. That is correct behavior, but it falls outside the stated bound.
- **S7.** With four other VIDs held (N_VIDS_P = 4):
  - the talker's user++ is refused and lost;
  - the licence stays closed even after a slot frees;
  - only a re-declaration recovers it, after 149 ms.
- Before this PR, the same case streamed without the MVRP join.
- Neither outcome is signalled at the top level.

**Impact.** S7 is outside the documented envelope, which is one steady VID plus one more during a Domain change. The parent-visible statement is narrower than the real behavior, which matters to an integrator.

**Suggested outcome:**
- in the parent-visible list and in §6.2, state that the bound is one T-MRP-JOIN plus any TX-arbiter wait;
- state there that a VLAN-table overflow holds the licence closed until re-declaration;
- optionally, connect the VLAN error so that it is visible.

**Verification.** Read the updated docs and PR text, and re-run the probe to confirm the behavior is unchanged.

### S3: SUGGESTION. Lenses: Conformance, Docs

**Where:**
- `docs/architecture/10_srp_engine.md:587-599`;
- `docs/architecture/10_srp_engine.md:610-612`: "one LeaveAll per cycle serves both ends";
- `hdl/srp/KL_srp_top.sv:1224-1228`;
- `tb/srp_top` P3, which pins that a Domain-only lane restarts the MSRP timer.

**Authority:**
- 10.7.5.20 b)2) and its NOTE;
- 10.6: "suppressing multiple LeaveAll messages";
- #106's per-type receive scoping, under which a received LeaveAll ages only the types it flags.

**Impact.** Suppression works per application, but aging works per type.
- Consider a peer that flags LeaveAll on only some MSRP types, as this processor did before #106. Its LeaveAll restarts this station's whole MSRP timer.
- Registrars of the types it did not flag are then aged only in the cycles this station still wins:
  - with conformant peer timing, that is about every other cycle rather than every 10-15 s;
  - if the peer's LeaveAll period is under 10 s, it is never.
- The bench is unaffected, because the reference switch flags all four types.

**Suggested outcome:**
- state this caveat in §6.5;
- optionally, restart only when the received MRPDU flagged every type the application supports.

**Verification:**
- read the docs;
- if the RTL option is taken, extend P3 with a partial-type peer and check that the own LeaveAll cycle continues.

## 5. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv` (rLA!, Begin!, expiry and MVRP-flag paths); the `KL_srp_talker_fsm.sv` licence; `KL_srp_vlan.sv`; the `KL_srp_encoder.sv` strobe; 802.1Q-2014 Table 10-5, 10.6, 10.7.4.3 and 10.7.5.20; Milan Table 4.3, 4.2.7.3, 4.3.2 and 4.4.1; #106's decisions and capture record | R399-1 | 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b |
| RTL | CLEAN | the `hdl/` diff (encoder, talker FSM, top, VLAN, pp top); the encoder FSM and VLAN in full; the timer service's arm/expiry logic; the top-level arm mux; lint_hdl rc 0 | R399-1 | 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b |
| Robustness | CLEAN | probe_licence (S0-S7, 8/8); probe_arm_race (arm delays 0, 2, 3, 4, 8 and 16 × 83 offsets); the stick-closed cases from the assignment; reasoning on E_COLLECT and arbiter wait | R399-1 | 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b |
| Tests | CLEAN | srp_top 2149, srp_stream_fsms 1219, srp_encoder 581 and pp_top 7751, all 0 FAIL; the full srp_top campaign (10 controls, 72/72 KILLED, coverage 63/63); the test source for P1-P6, Q1-Q4, R1-R4, W1-W5 and the VID-term checks; srp_top at `bff4417` matches the head | R399-1 | 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b |
| Docs | CLEAN | docs 10 §6.2, §6.3 and §6.5; 08 F08.1; `10_RESOURCE_AND_EFFORT.md` item 11; the integrator guide; the RTL banners; the tb READMEs; `make check` and `gen_matrix --check` rc 0; the PR's parent-visible list checked against parent files at `57b8c867` | R399-1 | 81b8d6d7c4e2d90c5ab0f2e772a0991166945c3b |

## 6. Executed evidence (this packet)

- **Simulator.** Verilator 5.050, the CI pin.
  - The specified wrapper path did not exist at review time.
  - A private wrapper onto an identical 5.050 install was used instead.
  - Its version and binary SHA-256 are in `receipts/verilator-identity.txt`.
- **Suites** (`receipts/suites/*.log`): srp_top, srp_stream_fsms, srp_encoder and pp_top, all rc 0 with the tallies above. srp_top was also run at `bff4417`.
- **Static gates** (`receipts/static-rc.txt`, `lint_hdl.log`, `make_check.log`, `gen_matrix.log`): all rc 0.
- **Mutants.**
  - The lane's 16 new arms (`receipts/mutants/`): all KILLED, with failing-check counts equal to the README tables.
  - The full campaign (`receipts/mutants-full/`): 72 arms KILLED, 0 UNPROVEN, 10 controls pass.
- **Probes.**
  - Receipts: `receipts/probe-armrace/` and `receipts/probe-licence.txt`.
  - Scripts: in `scripts/`. `scripts/run_focused.sh` reproduces all of the above.
- **Public records.**
  - `receipts/evidence/`: the MANIFEST, HANDOFF and PR-BODY files, with hashes verified, plus the author's result lines.
  - `receipts/issue*.json` and `receipts/pr133.json`: fetched at the start of the review.
  - `receipts/hosted-check-runs.txt` and `receipts/hosted-check-runs-final.txt`.

## 7. Hosted checks at the exact head

These are observations only; hosted acceptance belongs to the manager. There are two runs: 36535843514 (push) and 36535848026 (pull_request).

**Completed with success in both runs:**
- `docs-gates`;
- `portability`.

**`suites`, as last observed at 08:06 UTC** (`receipts/hosted-check-runs-final.txt`; the earlier 07:51 snapshot is `receipts/hosted-check-runs.txt`):

| Step | pull_request run 36535848026 | push run 36535843514 |
|---|---|---|
| "Build Verilator v5.050" | skipped (cache hit) | skipped (cache hit) |
| "Lint (zero tolerance) + every suite" | success | success |
| "SRP LeaveAll mutation campaign" | success | success |
| "Traceability matrix no-drift + untested budget 0" | success | success |
| "nvm_port README figures agree with the tree" | success | still in progress |
| Job conclusion | **success** (completed 07:59:30Z) | still in progress |

The only skipped step is the Verilator build, which was skipped on a cache hit. None of these hosted results was used in place of a local run.

## 8. Limits and pending manager duties

**Not run by this review:**
- the parent consumer bank, the donor full bank, the gPTP bank, the Yosys bank and the builder. Where this report cites their results, they come only from the author's public receipts;
- hosted or act runs;
- hardware calibration.

**Not proven here.** The field effects are evidence for parent #76:
- the DUT's LeaveAll cadence against the reference switch;
- first-bind latency (parent #606).

**Source limit.** The 802.1Q and Milan PDFs are not distributed. Clause text is taken as quoted in the tree and in #106.

**Manager duties at the merge turn:**
- build the final current-dev candidate at live dev `57b8c867`, whose gitlink is still `c951a9ff`;
- run the parent consumer set, including:
  - re-basing `milan_dp` `obj_crflic` phase [C] (`sim_crf_licence.cpp:953,956`, from `>= 4` to `>= 3`);
  - the parent doc updates (ieee8021q MRP-4/5/6/7 and the compliance matrix rows);
- run the parent's `check_cpp_idiom.py` on `81b8d6d`;
- complete hosted/act acceptance, including the push run's `suites` job, which was still in progress at 08:06 UTC.

R399-1 FINISHED
