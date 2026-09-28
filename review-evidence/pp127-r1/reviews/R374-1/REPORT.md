[R374] NEGATIVE - exact head cf4e5c63ab12442c6c63d2bfe2bb64902674d55e

# R374-1: internal independent review of processor PR #130 (issue #127)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #130, issue #127
- Exact head: `cf4e5c63ab12442c6c63d2bfe2bb64902674d55e`, tree `2f66e2d9de82e1aca097db59a9b9f4a19cdb767d`
- Base: `16be6768f710e79450aace277abacd6c2c3336e5` (the parent's current pin). One commit.
- Review round: R374-1, the first review of this PR. Cleared context, own detached clone.
- Reconstructed from: README.md and docs/README.md (the repository has no AGENTS.md or CONTRIBUTING.md); issue #127 body and the assignment comment 5860872275; the parent analysis kebag-logic/milan-fpga#608 with its clue and analysis comments; `docs/architecture/10_srp_engine.md` §6.5; the full diff and history; the author evidence packet at kebag-logic/milan-fpga@88ed7be3 `review-evidence/pp127-r1`; the manager's parent-consumer-gate comment on PR #130 (5861561819).
- Independence: I did not read the same-round external report on PR #130, private author material, lane scratchpads, or the management tree. No prior-round review findings exist on this PR, so none need resolving or retaining.

## Verdict

**NEGATIVE.** The RTL change is correct. At this head, the own MSRP LeaveAll ages the registrars only at the `sLA` edge (slot-reservation acceptance), and both applicant walks start with `txLA!` on that same edge. A Listener Leave decoded before or on that edge clears IN. I reproduced the parent's non-stop on the base RTL and confirmed it is gone at head up to the `sLA` clock. LV + rLv and #108 behaviour are unchanged. All SRP suites, the processor-top suite and lint pass.

The verdict is NEGATIVE for two open findings in the Tests lens:

- **F1 (MAJOR).** The manager's parent consumer gates fail 3 of 11 at this head, on the new test code. The parent cannot adopt the pin until they pass.
- **F2 (MINOR).** Three of my planted mutants in the new supersession and intent logic survive the full 1914-check suite. My own probes kill each one, and head passes those probes, so the behaviour is right but the committed tests do not pin it.

## Findings

### F1 - MAJOR - Tests - the new test code fails three parent consumer gates

- **Where:**
  - `tb/srp_top/sim_main.cpp:334` (`std::vector<uint64_t> la_cycles, rx_cycles, prep_cycles, peer_la_cycles, expiry_cycles;`), plus further multi-declarators at `:708` and `:810`.
  - `tb/srp_top/mutants.py:106` and `:114` (`def run(...)` and `def main()` have no annotations or docstrings), and 22 lines over 100 characters.
  - `tb/srp_top/mutants.py:110` (`timeout=900`, a host wall-clock deadline).
  - `tb/srp_top/mutants.py:121` and `:144` (reads DUT sources and is not classified).
- **Authority and evidence:** manager comment 5861561819 reports parent dev `931f396e` with the gitlink at `cf4e5c63`: 8 of 11 consumer gates pass, 3 fail. The three are C++ rule 11 (multi-declarator 1 > ratchet 0), Python rule 12 (unannotated 2, undocumented 2, over-long 14, each > ratchet 0), and `scripts/measure_test_evidence.py --check` (4 wall-clock suite files > ratchet 3, with the new one being `tb/srp_top/mutants.py`; 1 unexplained DUT-source reader > 0). I checked the cited constructs at the lines above. The rules are in the parent's `docs/development/CODE_QUALITY.md` (Rule 11, Rule 12) and its "Suite files using host wall-clock/process deadlines" ratchet. The assignment's parent bar says the manager runs these gates for pin adoption.
- **Impact:** the parent cannot move its pin to this head, so the #608 fix does not reach the consumer.
- **Required outcome:** make the new test code conform: one declarator per declaration; annotated and documented Python functions within the line limit; no host wall-clock deadline in a suite file, or a classification the parent accepts; the DUT-source reader classified as a mutation tool the way the parent inventory requires.
- **Verification:** the manager re-runs the parent consumer gates at the new head and all 11 pass.

### F2 - MINOR - Tests - three new supersession/intent decisions survive mutation

Each mutant below changes one line of the new logic, builds, and passes the full `tb/srp_top` suite (`1914 checks: 1914 PASS, 0 FAIL`). A reviewer probe kills each one, and head passes that probe. Receipts are in `receipts/mutants/`, and the probes are in `scripts/r374_probe.cpp.inc`.

| Mutant | Edit | Author suite | Killed by | Head |
|---|---|---|---|---|
| `my-join-edge-peer` | `hdl/srp/KL_srp_top.sv:1082` drops `&& !(\|dec_la_msrp_w)` | 1914/1914 PASS | R4 (peer lane on the join-cadence clock, delta 0: own sLA and flagged frame appear) | R4 2/2 PASS |
| `my-cancel-eats-new-intent` | `KL_srp_top.sv:1095` `if (!la_cancel_r)` removed | 1914/1914 PASS | R3 (cancel, then a newer expiry while allocation is blocked: no own sLA) | R3 1/1 PASS |
| `my-reuse-flags-ignore-cancel` | `hdl/srp/KL_srp_encoder.sv:597` `la_act_r <= 1'b1` | 1914/1914 PASS | R5 (peer lane on the reuse-acceptance clock of a retained reservation: LeaveAll flags on the wire with no sLA) | R5 5/5 PASS |

- **Authority:**
  - The assignment's proof bar: every new check is pinned by a killed mutant, and reviewers plant their own.
  - The design claims these behaviours: `10_srp_engine.md:509-510` ("supersedes the pending own action, including on the preparation-acceptance edge") and `KL_srp_top.sv:1093-1094` ("A canceled preparation must not consume a newer timer intent").
- **Impact:** a regression in any of these would put LeaveAll flags on the wire after a peer's LeaveAll, or with no local registrar event, or would skip one own LeaveAll cycle (10 to 15 s). The committed suite would stay green.
- **Required outcome:** add committed `srp_top` cases for the three phases (peer lane at the join-cadence clock -1/0/+1 with pending intent; cancel followed by a newer expiry before acceptance; peer lane at the reuse-acceptance clock of a retained empty reservation). Add the three mutants to `tb/srp_top/mutants.py` and show them KILLED by the named assertions.
- **Verification:** `python3 tb/srp_top/mutants.py --output <dir>` reports the three new arms KILLED. Rebuild each of these edits in a scratch copy and check that the committed suite fails.

### F3 - SUGGESTION - Robustness, Docs - a canceled empty reservation holds a shared TX slot and stalls MVRP drains

- **Where:** `hdl/srp/KL_srp_encoder.sv:592-604` (E_COLLECT waits until MSRP content arrives, `start1_w` needs E_IDLE) and `docs/architecture/10_srp_engine.md:512`.
- **Evidence:** probe R2, scenario 1 (only the Domain is declared; a peer Listener-only LeaveAll cancels a blocked own action). The encoder stays in E_COLLECT for 654 ms, until the periodic Domain refresh at the 1 s boundary. With a stream declared, the walk supplies content and the dwell is 0 ms. While the reservation is held, the encoder keeps one of the four standard TX slots that all engines share (`KL_pp_tx_slots` `TX_STD_SLOTS_P = 4`), and MVRP drains cannot start. With the link down, the hold lasts until the next own action (M12).
- **Suggested outcome:** document the bound. It is at most about one T-MRP-PERIODIC plus one T-MRP-JOIN while the link is up, and it takes one shared standard slot. Alternatively, release the handle when a canceled round is empty.

### F4 - SUGGESTION - Tests - the parent replay harness sources are not published

- **Where:** evidence `review-evidence/pp127-r1/author/run_parent.py`. It copies `reproduce.cpp` and `run_reproduction.py` from a lane directory that is not public. Only their hashes (`a509453e...`, `d7ecb4ce...`), the adapted-oracle patch and the logs are published.
- **Evidence:** the exact-harness replay cannot be re-run from public material. I reproduced the claim independently instead (probe R1, see Conformance). The numbers match the author's logs: deadline 14096 ms, sLA at 14200 ms.
- **Suggested outcome:** publish the two harness files with their recorded hashes alongside the evidence, or the manager attests to them.

### F5 - SUGGESTION - Tests, Docs - join-tick coalescing during a blocked preparation is not pinned

- **Where:** `hdl/srp/KL_srp_top.sv:1152` (`|| la_wait_r`) and `10_srp_engine.md:506-507`.
- **Evidence:** `my-drop-join-during-wait` passes 1914/1914 and all reviewer probes. The effect is only an extra ordinary round after the LeaveAll round, so the mutant is nearly equivalent.
- **Suggested outcome:** pin the claim with a test, or reword the sentence to what is observable.

## Lens evidence

### Conformance: CLEAN

- **The sLA edge.** Timer expiry now sets intent only (`KL_srp_top.sv:1167`). The single `sLA` strobe is `la_tx_o` (`KL_srp_encoder.sv:345`), asserted when slot allocation is granted to a prepared round, or when a retained reservation is reused. That one edge does three things:
  - ages every registrar of both stream FSMs;
  - starts both walks with `txLA!` (same-edge `wtxla_r <= laown_pend_r || leaveall_own_i`, talker `:570`, listener `:625`);
  - drives the Domain re-declaration.

  This matches 802.1Q-2014 §10.7.9 / Table 10-5, where sLA happens at the tx opportunity and generates LeaveAll events against all Applicant and Registrar machines of the participant.
- **Receive priority.** The registrar keeps its receive priority (`KL_srp_talker_fsm.sv:686-704`): a registering event, then Leave, then LeaveAll.
- **LV + rLv unchanged.** Rule `:697` (rLv on LV is -x-) is unchanged, and so is Δ13 on IN.
- **#108 unchanged.** Peer supersession clears only the unaccepted intent. It neither re-arms the timer nor draws a new one (`:1177-1182`). Author M4 covers this and my run passes it.
- **Type scope unchanged.** Receive routing per type is unchanged. Any MSRP lane cancels the per-application own action, and MVRP cannot (author M1-M3).
- **Parent claim reconstructed (probe R1).** Base RTL and head RTL were run under the same testbench. Sources 0/3/7 declare Ready, and a Listener Leave for source 0 arrives at deadline+offset, followed by a 2 s hold:

  | Offset from expiry | Base 16be6768 | Head cf4e5c63 |
  |---|---|---|
  | -3 to -1 ms | IN, stops | IN, stops |
  | 0 ms | LV, **non-stop** | IN, stops |
  | +1 to +103 ms | LV, **non-stop** | IN, stops |
  | +104 ms (Leave decoded on the sLA clock at 14200 ms) | LV, non-stop | LV, non-stop (legitimate crossing) |
  | +105 to +200 ms | LV, non-stop | LV after sLA, non-stop (LV + rLv retained by decision) |

  The defect window was [expiry, next join tick], 104 ms in this seed and up to 200 ms in general. At head it collapses to Leaves that land after sLA. In the testbench's compressed time (1 ms = 40 clocks) the frame reaches the wire 6 ms after sLA, which is a few hundred clocks. The original parent helper still reports a non-stop (evidence `parent-original-oracle.log`) because it waits for LV. At head that means waiting for sLA, so it exercises the retained LV + rLv case that #608's decision leaves as documented. This is the reading the manager recorded on #608 ("within one PDU period of a withdrawal that reaches an IN registrar"). The manager should confirm that it satisfies proof item (5).

### RTL: CLEAN

- **Top.** I read `KL_srp_top.sv:1078-1114` and `:1148-1182` in full. `la_wait_r` is set only when `!rnd_act_r`, so the previous round's walks are complete and the FSMs are in W_IDLE when the same-edge join arrives. Round completion bits are cleared only at the start of a round. The high-water drain covers a table already full on the acceptance edge (`:1111-1114`).
- **Encoder.** MSRP pushes are blocked in E_ALLOC and accepted in E_COLLECT. The snapshot edge blocks pushes through `start_tgt_w`. Only the first frame of a split round carries the flags, and it carries LeaveAll-only vectors for all four types. An empty-with-flags round emits LeaveAll-only messages. An empty-without-flags E_HDR→E_PDUEND path is unreachable.
- **Combinational path.** The new path runs alloc_gnt (registered in `KL_pp_tx_slots`) → `la_tx_o` → registrar next-state. It is shallow and has no loop.
- **Reset.** Reset clears all new state.
- **Lint.** `scripts/lint_hdl.sh` with the pinned simulator: rc 0 on every module (`receipts/head-lint.log`).
- **Testbench handshake.** The testbench change (`sim_main.cpp` "serializer returns to idle") matches the RTL. `KL_pp_tx_slots` `ser_start_w` requires `!run_r`, and `run_r` clears on the edge that consumes the last byte.

### Robustness: CLEAN (F3 is a SUGGESTION)

- **Backpressure.** Allocation stalls (K9, L, M), TX stalls (N1-N4), full and already-full tables (N6, N9-N10), coalesced expiries (N11-N12) and asymmetric walks (N13) all pass.
- **Liveness.** No new state can wedge. `la_wait_r` clears only on acceptance, which needs a slot, the same as before for any drain.
- **Reuse edge.** Probe R5 confirms a peer on or before the reuse edge supersedes, and that wire flags always match `sLA` strobes.
- **Canceled empty reservation.** It is held for a bounded time (F3).

### Tests: UNCLEAN (F1, F2)

All suites were run under the pinned simulator, with builds capped at 8 jobs:

| Suite at head | Result |
|---|---|
| `tb/srp_top` | 1914/1914 |
| `tb/srp_stream_fsms` | 1215/1215 |
| `tb/srp_encoder` | 556/556 |
| `tb/srp_decoder` | 190/190 |
| `tb/pp_top` | 7751/7751 |

- **Periodic-declaration and six-cycle no-storm checks.** Unchanged and passing. The counts are 4, 3, 3, 3, 3, 2, within the unchanged limits of 18 total and 4 per cycle (`receipts/head-srp_top.log`).
- **Phase-sweep coverage.** The required phases are all present and pass:
  - before expiry, during the pending own transmission, at acceptance (-8..+5 clocks), and after LV entry;
  - Ready and Ready Failed; sources 0, 3 and 7;
  - mismatched and malformed SID, reset, and delayed allocation or TX.
- **Author campaign subset** (controls, `expiry-event`, `round-completion-lost`, `repeated-expiry-queued`): the controls pass and all three arms are killed. `expiry-event` fails 81 checks, as claimed (`receipts/author-mutants-subset.log`).
- **My mutants.**
  - Killed: `my-expiry-pulse` (the timer-expiry registrar pulse added back beside sLA: 88 failures, K2/K4/K11/K12/L2/M/N), `my-edge-cancel-lost` (M6/M7), `my-la-outranks-leave` (L2), `my-no-walk-at-sLA` (24 failures).
  - Surviving: the three in F2 and the near-equivalent in F5.
- **Hosted CI at this exact head.** Six check runs executed and completed with success: docs-gates, portability and suites, twice each. None were skipped.

### Docs: CLEAN (F3, F5 are SUGGESTIONS)

- `10_srp_engine.md` §6.5 "Own transmit action" matches the RTL: intent, reservation-edge sLA, collection, split drains, receive priority, supersession on the acceptance and reuse edges, and #108 unchanged.
- The port comments in both FSMs and the encoder header are updated.
- The README tallies (1914, 1215) match my runs.
- F10.9 and `08_timing.md` stay accurate.
- No stale "ages at expiry" wording remains in `docs/`, `hdl/` or `tb/`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_srp_top.sv`, `KL_srp_encoder.sv`, `KL_srp_talker_fsm.sv`, `KL_srp_listener_fsm.sv` against 802.1Q-2014 §10.7.9/Table 10-5, Table 10-4, Δ13, #108 and the #608 decision; probe R1 on base vs head (`receipts/probe-base-r374r1.log`, `receipts/probe-head-r374r1.log`) | R374-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| RTL | CLEAN | full diff of 5 HDL/doc files; `KL_pp_tx_slots.sv` serializer handshake; lint (`receipts/head-lint.log`) | R374-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Robustness | CLEAN | backpressure/full-table/reset/reuse paths; probes R2-R5 (`receipts/final-probe-head-*.log`) | R374-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | `tb/srp_top/sim_main.cpp`, `srp_top_wrap.sv`, `mutants.py`, `tb/srp_stream_fsms/sim_main.cpp`; 5 suites; 8 reviewer mutants (`receipts/mutants/`); author campaign subset; manager consumer-gate comment 5861561819; hosted check runs (`receipts/head-check-runs.json`) | R374-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |
| Docs | CLEAN | `docs/architecture/10_srp_engine.md` §6.5, the `tb/srp_top`, `tb/srp_stream_fsms` and `tb/srp_encoder` READMEs, RTL header comments, `08_timing.md`, F10.9 | R374-1 | cf4e5c63ab12442c6c63d2bfe2bb64902674d55e |

## Real limits

- **Simulator path.** The assigned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the byte-identical wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` (sha256 `905795b9...`, the same bytes as the pp127 manager wrapper), which reports Verilator 5.050 rev v5.050. The underlying binary hashes are in `receipts/tool-identity.txt`.
- **Parent replay.** The exact parent harness was not re-run because its sources are not public (F4). The claim was reproduced by an independent reconstruction in the processor testbench instead.
- **Out of scope for me.** I did not run the full parent, processor, gPTP, Yosys or builder banks, the parent consumer gates, `srp_admission` or the other unchanged suites, act, or hardware. Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Probe timing.** The reviewer probes use the testbench's compressed time (1 ms = 40 clocks). Real-time windows between sLA and the wire are shorter in hardware.
- **Same-round report.** I did not consult the same-round external report.

## Pending manager duties

1. Re-run the parent consumer gates after F1 is fixed. Adopt the pin with the CRF frame/STREAM_STOP integration regression that #127 specifies.
2. Decide whether the original parent helper's retained-LV non-stop satisfies proof item (5) under the #608 decision. Publish or attest the parent harness sources (F4).
3. Build the final current-dev candidate at the merge turn (source base 16be6768, live dev 931f396e). Own hosted/act acceptance.

## Reproduction

The scripts are in `scripts/`. Run them from this packet directory. Set `VERILATOR` to override the pinned wrapper.

- A suite: `scripts/run_suite.sh <tree> srp_top [group]`.
- Probes:
  1. Install them into a copy of the tree: `python3 scripts/install_probe.py <tree>`.
  2. Run the groups `r374r1` through `r374r5`.
  3. For the base-RTL comparison, build the tree with `python3 scripts/make_base_probe.py <base> <head> <dst>`.
- Mutants: `python3 scripts/r374_mutants.py <head-tree> <out> [names]`.

After all probes, the review clone was verified identical to the exact head (`receipts/clone-integrity.txt`):

- HEAD is `cf4e5c63...`, and both the HEAD tree and the index tree are `2f66e2d9...`;
- every one of the 250 tracked blobs and modes matches, and there are no untracked or ignored files;
- the repository has no submodule gitlinks.

R374-1 FINISHED
