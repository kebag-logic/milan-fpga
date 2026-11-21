[R877] NEGATIVE - exact head 4ceba3d40e3b94e9bda2407e64ef906c283b63a4

# Round R877-1: internal cleared-context review of PR #959 (issue #948)

- Head: `4ceba3d40e3b94e9bda2407e64ef906c283b63a4`, tree `62b09e5c2b550349fee753f4f3d2275422c05e20` (clone verified, `receipts/clone_integrity.txt`).
- Source base: `15168e14a1fe709b9ab5336acd6daf54e4d6e0a4` (the flip train head). Reviewed delta: `git diff 15168e14..4ceba3d4`, 13 commits, 25 files.
- Scope and acceptance come from: the issue body; the ruling of 2026-11-21 (#948 issuecomment-7061889923: fan-out, not refusal; failing test first with two and then three inputs and an unbind; the RTL suites and the twin; CPU budget rows unchanged; fit and timing at 1x1/1if and 8x8/1if on best of three directives, STOP if 8x8 does not fit or close); the TAKEN and REVIEW READY comments; and the PR body.
- Authorities: IEEE 1722.1-2021 8.2; Milan v1.2 5.3.8.10 / Table 5.6, 5.3.8.7, 4.4.2.2.
- Prior public review findings on this PR: none existed when this round started. The only PR comments were the two review-start notices, so nothing is carried over.

## Verdict summary

One MINOR finding (Tests, Robustness) is open, so the verdict is NEGATIVE. Conformance, RTL and Docs are covered clean at this head. One RESIDUE and one SUGGESTION are recorded; neither affects the verdict.

The fan-out works and is well tested on every axis the ruling names:
- The parser reports the full match vector.
- The engine serves one bundle to each bound context, in order, with per-context format compare, sequence state and counters.
- The depacketizer stores the frame once and makes one pass per accepting input, tuser that input.
- The clock meter follows the followed input's match bit.

What is open: the per-input Milan 5.3.8.7 stop gate on a shared stream is claimed in the RTL comment and the PR text, but no test can fail on it. A planted shared-gate defect passes the whole 8x8 datapath suite.

## Findings

### F1 - MINOR - Tests, Robustness - `hdl/milan/milan_datapath.sv:7901-7904` (`avtprx_deliver_w`); `tb/verilator/milan_dp/sim_nxn.cpp:8144-8246` ([FAN]); `tb/verilator/avtp_rxmon/avtp_rxmon_nx_wrap.sv:10`; `tb/verilator/milan_dp/twin_split.cpp` (`--fanout`) - no test can fail if a stopped input's 5.3.8.7 discard also discards the PDU for the inputs sharing its stream

- **Requirement / evidence:**
  - Milan v1.2 5.3.8.7: a stopped Stream Input discards the PDUs it receives. This PR moves that gate onto the depacketizer's done mask, input by input. The comment at `milan_datapath.sv:7901-7902` and the PR Description ("a stopped input's share is discarded and the others receive") both claim the per-input behaviour.
  - No test stops one input while another input bound to the same stream keeps receiving:
    - `sim_fanout` drives every input started (the wrap says so at line 10).
    - `sim_nxn` [FAN] and `twin_split --fanout` never STOP.
    - The existing 5.3.8.7 sections (`sim_nxn.cpp:8481-8575`, `8600-8640`) stop STREAM_INPUT 0 with only its own stream on the wire.
  - Executable proof: I planted a shared gate (`receipts/probeB.diff`) in which a stopped input among a PDU's accepting inputs discards the PDU for all of them. The 8x8 datapath suite (`build-nxn8`/`exec-nxn8` recipe, same flags, mutated `milan_datapath.sv`) still passes: `checks: 4027 failures: 0` (`receipts/probeB_nxn8.log`).
  - The RTL at the head is correct by inspection: a bitwise `& ~stopped`. The gap is the evidence, not the gate.
- **Impact:** a regression of the gate is invisible to every suite. The likeliest form is reusing the existing single-index `avtprx_stopped_w` on the whole mask, or gating on any stopped input. On the bench, a controller's STOP_STREAMING on one input would then silence every other input sharing the talker stream, which breaks 5.3.8.7 and the ruling's "each input its own ... render path".
- **Required outcome:** a self-checking test with at least two inputs bound to one stream (any of `sim_nxn` [FAN], `twin_split --fanout`, or a stop-capable `sim_fanout` wrap) where:
  - one input is STOPPED (STOP_STREAMING over AECP where the harness has the processor) and the other keeps receiving every PDU (its DEPKT tally / its share of the depacketizer's output);
  - the stopped input receives nothing while its FRAMES_RX still counts (Table 5.6: received on this Stream Input);
  - START restores the stopped input's share.

  The shared-gate plant must fail that test, as a named mutant or plant beside the existing ones.
- **Verification:** the new check passes at the fixed head, and the plant in `receipts/probeB.diff` (or its equivalent in the suite's plant mechanism) is caught by name.

### R1 - RESIDUE - Docs - `docs/testing/TESTING.md:706` (the `tb/verilator/avtp_rxmon` row) - a missing sentence break

- **Evidence:** the appended text reads "... the lockstep compare cannot see a defect in both copies, and passes Its fan-out leg (`make fanout`, #948) ...".
- **Impact:** wording only. No measurement, figure, verdict, test, code, generated artifact or clause claim changes, and no privacy rule is touched.
- **Exact fix:** replace "and passes Its fan-out leg" with "and passes. Its fan-out leg".

### S1 - SUGGESTION - RTL - `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:187,228,283,296` - state why the frame store, its read pipeline data registers and the two small queues carry no reset

- `fmem_r`, `qa_r`/`qb_r`, `rq_msk_r` and `idxq_r` are not reset. Their validity is carried by reset flags and pointers (`va_r`/`vb_r`, `rq_*_r`, `idxq_*_r`), so behaviour is correct.
- CONTRIBUTING 1 says every register is reset, and the paired engine states its exception (`KL_avtp_rx_monitor_ctx.sv:314-315`, "No reset ON PURPOSE"). One comment line here would make the exception explicit.

## Lens results (each applied independently at the exact head)

| Lens | Result | Artifact examined, and against what |
|---|---|---|
| Conformance | PASS | See below |
| RTL | PASS | See below |
| Robustness | UNCLEAN (F1) | See below |
| Tests | UNCLEAN (F1) | See below |
| Docs | PASS (R1 residue, no MINOR+) | See below |

**[R877] PASS Conformance**
- Artifacts: `hdl/ieee1722/avtp/avtp_stream_parser.sv:192-205,255`; `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:444-447,477-512,981-1103`; `hdl/milan/milan_datapath.sv:7488-7489,7903-7904,8022-8025`.
- Checked against IEEE 1722.1-2021 8.2, Milan v1.2 5.3.8.10 / Table 5.6, 4.4.2.2 and 5.3.8.7:
  - The parser registers every enabled matching entry (`match_vec_o`) with the parse pulse.
  - The engine enqueues on `match_vec_i & bound_i != 0`. It serves the one bundle to each context lowest first, and every context runs its own FMT read, PDEC verdict (off-format: UNSUPPORTED_FORMAT and prev_seq advance, no accept), MON_STATE, counters and tv/tnv flops.
  - Every bundle ends in exactly one `pdu_done_p_o`, with the accept mask on both PDEC exits.
  - The stop gate masks `done_mask & ~stopped` per input, so a stopped input still counts FRAMES_RX (the engine is upstream of the gate).
  - The meter sees the followed input's bit.
- Acceptance: the ruling's gates are met. Fan-out was proven failing-first by plant (below). The suites and the twin are green. No `sw/` file is in the delta and the 12 budget images equal the train record (author receipts `review-evidence/948-r1/author-r1/receipts/budget/images-at-73f1113b.txt` and `images-train-record-15168e14.txt`, compared byte for byte in this round). #818's floor is met on all six routes.

**[R877] PASS RTL**
- Artifacts: `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:142-350,405-447` and `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:308-324,924-936,981-1113`.
- Checked:
  - Single clock, one synchronous reset (`axis_resetn`) shared by parser, engine and depacketizer, so no verdict can be orphaned by a split reset. No CDC.
  - Ring capacity: at most 2 waiting plus 1 in service. A new slot never equals `cur_idx_r`, and `pcont_w` holds `cur_idx_r`.
  - The enqueue-to-frame association: the parser fires on beat 7, `pdu_enq` lands 2 cycles later, and the next frame cannot pass its own beat 7 sooner than 8 cycles.
  - Same-cycle alloc and fate on one entry: the later non-blocking write wins, as intended.
  - Retirement is in order, and the read side waits for the mask before popping a header beat.
  - Rewind restarts at `fs_r` with the pipeline flushed. Release frees `pn_r + 1` words.
  - Widths: `lowest()` 4-bit `rs_r` for N <= 16; `aaf_follow_idx_r` can index `avtprx_vec_w` out of range only with a clock-source table the builder never emits.
  - Comment rule: no lane, round, reviewer or comment ID was added in the delta (scan of added lines).
- Yosys at the head (local sv2v v0.0.13, Yosys 0.66) on the three touched tops: PASS, cells 3036 / 10916 / 53546, equal to the author's head figures. Tied-input and tap-purity checks PASS (`receipts/yosys_touched.log`). Lint ratchet 89 <= 89 (`receipts/docs_gates.log`).

**[R877] MINOR Robustness (F1 open; not covered clean)**
- Artifacts: as RTL above, plus the probes.
- Probe A (`receipts/probeA.diff`, `receipts/probeA_events.txt`) instruments the depacketizer under `sim_fanout`. Across [FO1]-[FO10] the verdict queue peaks at 3 of 4 entries and the read queue at 7, with no overflow, no done-without-enqueue, no done-pointer overtaking, and no read-queue underflow. The 4-entry bound is also argued above.
- Malformed, short and overflow paths are covered by [FO8]-[FO10]. Reset during activity shares one reset. The repeated-commands case is the unbind in [FO3] and [FAN].
- Configuration-dependent behaviour (a stopped input on a shared stream) is not exercised: F1.

**[R877] MINOR Tests (F1 open; not covered clean)**
- Artifacts: `tb/verilator/avtp_rxmon/sim_fanout.cpp`, `fanout_mutants.py`, `tb/verilator/milan_dp/sim_nxn.cpp` [FAN], `twin_split.cpp --fanout`, `twin_fanout_plant.py`, `tb/verilator/milan_dp_mclk/sim_mclk.cpp --shared`, `mclk_mutants.py`.
- Each runs at the head with the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`); per-suite results are in the receipts table below.
- Failing first: the base defect is reproduced as a plant (each PDU to the highest matching entry). It is caught in `fanout_mutants` (mutant 1), `twin-fanout-plants` (4 of 4 words) and `mclk_mutants` (19). The author's base-RTL receipts were read, not rerun.
- Every plant fails its named check. The stop-gate claim has no failing test: F1.

**[R877] PASS Docs**
- Artifacts: `docs/fpga/DATAPLANE_WALKTHROUGH.md:172-175`, `docs/fpga/FPGA_DESIGN.md:269,297`, `docs/testing/TESTING.md:706`, `tb/verilator/milan_dp/README.md:1850-1885`, `tb/verilator/milan_dp_mclk/README.md:57-91`, `scripts/measure_test_evidence_readers.py`, `docs/DOCUMENTATION_AUDIT.md`.
- Checked against the RTL behaviour and Table 7-157 (TIMESTAMP_VALID @24, FRAMES_RX @44).
- Gates at the head, all rc=0: `docs_check.py`, `check_doc_paths.py`, `docs_inventory.py --check` (fresh), `check_rtl_source_lists.py`, `check_soc_sources.py`, `measure_naming.py --check`, `check_port_contracts.py`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, the sv/cpp/py idiom gates, and `lint_rtl.py --check`.
- `check_em_dash.py` could not run (its pinned renderer is not installed here). By hand: no U+2014 in any added line.
- The PR body and the REVIEW READY figures match the fetched receipts.
- One wording defect: R1.

## Route and area claim (focus item 3), verified by diff and receipt

- `git diff e8a877a0..4ceba3d4 -- hdl/` and `git diff c2e5e5bd..4ceba3d4 -- hdl/` change only comments in `milan_datapath.sv` (two hunks). Parser, engine and depacketizer are byte-identical to the routed commit, so the six routes at `e8a877a0` and the sweep at `c2e5e5bd` stand for the head's RTL.
- Test files changed after `c2e5e5bd` are the `milan_dp_mclk` files only. This round reran that suite at the head: 36 of 36.
- The fetched route receipts (`review-evidence/948-r1/author-r1/receipts/fit/*`) match the PR table on every cell:
  - 8x8/1if ExtraTimingOpt: Slow WNS +0.332 / WHS +0.100, Fast +1.641 / +0.036.
  - 1x1/1if ExtraTimingOpt: +0.317 / +0.096, Fast +1.636 / +0.029.
  - #818's floor (WNS >= +0.030, WHS >= 0) holds at every corner of all six builds. The stricter both-+0.030 floor misses at 1x1 Fast hold (+0.028/+0.029), as the author discloses.
- Area deltas at ExtraPostPlacementOpt against the train's gating build (8c5e2b4f):
  - 8x8: +1,292 LUT, +83 FF, slices -39 (-267 at ExtraTimingOpt), RAMB18 33 -> 32.
  - 1x1: -171 LUT, +32 FF, slices -22, RAMB18 36 -> 35.
- The touched modules sum to the stated +151 LUT / +119 FF (8x8: depkt +101/+57, monitor +8/+41, parser +42/+21) and +141 / +48 (1x1).
- The rest of the 8x8 LUT move is in `KL_mbx_cdc/u_edit` (+1,700) and `milan_datapath/csr` (-1,196), neither of which the delta touches. The receipts show the move lies outside the touched modules. The cross-boundary-attribution explanation (and 8 vs 16 threads) is plausible but not independently provable from receipts; it changes no gate.

## Receipts run in this round (all at the exact head, scoped Verilator 5.050)

| Receipt | Command | Result |
|---|---|---|
| `receipts/rxmon_all.log` | `make -C tb/verilator/avtp_rxmon` (whole suite) | rc=0. Flat 97/0, NxN stack 218/0, lockstep N=1 116/0 and N=8 119/0, the lockstep/format/ctxfmt mutant drivers all PASS, CTXFMT 96/0, FANOUT N=8 239/0, `fanout_mutants.py` 13 checks 13 PASS (12 mutants + control) |
| `receipts/nxn8.log` | `make -C tb/verilator/milan_dp build-nxn8 exec-nxn8` | `checks: 4027 failures: 0`, every [FAN] check ok |
| `receipts/twin_fanout.log` | `make -C tb/verilator/milan_dp twin-fanout twin-fanout-plants` | `fanout: 0 failed`; 4 of 4 plant words caught |
| `receipts/twin.log` | `make -C tb/verilator/milan_dp twin` (1x1, unchanged default `N_STREAMS_P = 1`) | `twin: 0 finding(s)` |
| `receipts/mclk_all.log` | `make -C tb/verilator/milan_dp_mclk` | legs PASS; `36 checks: 36 PASS, 0 FAIL`, mutants 9 and 19 caught |
| `receipts/small_suites.log` | `make` in `avtp_parser`, `avtp_stream`, `aaf_audio_loop` | all rc=0 (`aaf_audio_loop` 10/0, single-binding depacketizer path) |
| `receipts/yosys_touched.log` | `syn/yosys/run.sh --top` the three touched tops | PASS |
| `receipts/docs_gates.log` | `scripts/gates.sh` (focused docs and quality gates) | all rc=0 except the em-dash gate, which could not run (no renderer) |
| `receipts/probeA_*` | `sim_fanout` with an instrumented depacketizer copy | 239/0, occupancy events above |
| `receipts/probeB_*` | 8x8 datapath suite with the shared stop-gate plant | 4027/0: the plant survives (F1) |
| `receipts/clone_integrity.txt` | tracked bytes, index tree, flags, gitlinks after probes | HEAD tree = index tree = `62b09e5c...`, 0 modified, 0 untracked, 0 skip/assume flags, gitlinks at their pins, submodule worktrees clean |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | parser `avtp_stream_parser.sv:192-205,255`; engine `KL_avtp_rx_monitor_ctx.sv:444-447,477-512,981-1103`; gate/meter wiring `milan_datapath.sv:7488-7489,7903-7904,8022-8025`; ruling acceptance vs receipts | R877-1 | 4ceba3d40e3b94e9bda2407e64ef906c283b63a4 |
| RTL | CLEAN | `KL_aaf_rx_depacketizer.sv:142-447`; `KL_avtp_rx_monitor_ctx.sv:308-324,924-1113`; `avtp_stream_parser.sv`; `milan_datapath.sv` delta; Yosys/lint receipts | R877-1 | 4ceba3d40e3b94e9bda2407e64ef906c283b63a4 |
| Robustness | UNCLEAN (F1 open) | the same RTL; probe A; [FO8]-[FO10]; the stop gate on a shared stream (probe B) | R877-1 | 4ceba3d40e3b94e9bda2407e64ef906c283b63a4 |
| Tests | UNCLEAN (F1 open) | `sim_fanout.cpp`, `fanout_mutants.py`, `sim_nxn.cpp` [FAN], `twin_split.cpp --fanout`, `twin_fanout_plant.py`, `sim_mclk.cpp --shared`, `mclk_mutants.py`, wraps, Makefiles; all rerun | R877-1 | 4ceba3d40e3b94e9bda2407e64ef906c283b63a4 |
| Docs | CLEAN (R1 residue only) | `DATAPLANE_WALKTHROUGH.md`, `FPGA_DESIGN.md`, `TESTING.md:706`, `milan_dp/README.md`, `milan_dp_mclk/README.md`, `DOCUMENTATION_AUDIT.md`, evidence-reader table, PR body | R877-1 | 4ceba3d40e3b94e9bda2407e64ef906c283b63a4 |

A fix for F1 that touches only tests un-covers Tests and Robustness for re-review. If it touches RTL or docs, those lenses are un-covered as well.

## Real limits of this round

- Not run here, by scope or rule:
  - the full Verilator sweep (`run_all_suites.sh`) and the full Yosys, firmware, PP and gPTP banks;
  - Vivado fit and timing: route figures are the author's receipts, checked against the RTL diff, not re-routed;
  - the firmware gate and CPU budget image builds (no `sw/` delta; image equality is the author's receipt);
  - `tsn_fuzz`'s generator campaign;
  - the twin's plant targets (`twin-plants`, `twin-maps`, `twin-maps-plants`).
- The em-dash gate could not execute (missing pinned renderer); it was replaced by a byte search of the added lines.
- Failing-first at the literal base RTL was not rebuilt. The base defect was reproduced as the one-index plant in three harnesses, and the author's base-RTL logs were read.
- Local sv2v is v0.0.13, not CI's v0.0.12; Yosys cell counts nevertheless equal the author's.
- Hosted contexts at the head were mostly queued or in progress at review time. No hosted verdict is inferred, and none is claimed.
- Physical calibration NOT RUN. Field and bench proof (the 8x8 bench case) is the manager's after merge, and no skip here is hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred.

## Pending manager duties

- Hosted and act acceptance at the exact head, and exact-head `verilator-suites` / `yosys-portability` evidence.
- The current-dev merge-candidate validation (builder and native banks) against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Carry R1 to the residue checklist.
- Route F1 back to the lane and schedule re-review of Tests and Robustness (plus any lens the fix touches) at the new head.
- Bench proof of the 8x8/1if shared-stream case after merge.
- Post-merge containment per CONTRIBUTING.

R877-1 FINISHED
