[R685] NEGATIVE - exact head c7e87c8c87494f3444000b46954648ba1a94dcb8

Internal cleared-context review R685-1 of issue #775 / PR #777. Reviewed tree `0b62e515c36a7c5c3781f7745c9a6f2a800878c2`, source base and live dev `a032c6d6e3775f145349d5a495c1e1ad12294936` (the base is an ancestor; live dev has not moved). Three one-line commits with no trailers: `0ee987f4`, `6ff2880a`, `c7e87c8c`. Twelve files.

This is a source review verdict. It is not merge authorization and not hardware acceptance.

**Why NEGATIVE.** One MINOR (F1) is open under Tests and Docs. The RTL is correct on both inputs, and every frozen acceptance criterion of #775 is met. But the test guide says the new AAF `[SQ]` cases grade that a discarded PDU "writes only prev_seq". They grade that on a locked, settled stream only.

On that stream, two defects in the new MON_STATE write-back cannot be seen:
- the reject sets the media_locked bit;
- the reject steps the settle count.

I planted each one in the engine and the lockstep reference together, the way an author would write a real defect into both copies. Each survived every avtp_rxmon leg. The CRF lane does grade the equivalent first-in-era case (`[SQ-d]`); the AAF lane does not.

## Reconstruction

Read in order:
- AGENTS.md, CONTRIBUTING.md (commit, comment, privacy and verification rules) and docs/README.md.
- Issue #775: its body, the assignment and ruling (issuecomment-6379902989), the executor's TAKEN and REVIEW READY.
- FR-STR-03, the compliance-matrix row for 4.4.2.2 / Table 5.6 and the testing-guide rows.
- PR #777's body.
- `git diff a032c6d6..c7e87c8c` and its history.
- The public receipt tree at `976fb2d3…/review-evidence/775-r1`.

**The ruling applied** (Milan v1.2 Table 5.6): an off-format Stream Data AVTPDU is a received PDU. Its sequence_num advances the input's sequence state. It counts only UNSUPPORTED_FORMAT and presents nothing. On CRF the first-PDU (have_seq_r) behaviour is kept. This review applies that recorded ruling and makes no new reading of the standard.

## Findings

### F1 - MINOR - Tests, Docs - an off-format PDU on an unlocked or settling AAF stream is ungraded, and the test guide claims more than `[SQ]` grades

- **Where:**
  - `tb/verilator/avtp_rxmon/sim_main_nx.cpp:1000-1075`: the `[SQ]` stream is locked and settled before the off-format PDU (`[SQ0]` at :1029).
  - `docs/testing/TESTING.md:617`: "counts UNSUPPORTED_FORMAT +1, presents nothing and writes only prev_seq".
  - `tb/verilator/avtp_rxmon/format_mutants.py:44-77`.
  - The RTL under test is `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1019`. That line writes the whole MON_STATE word back; only bits [7:0] are new.
- **Authority and evidence:**
  - Issue #775, assignment item 1: "Nothing else changes."
  - The ctx comment at :1016-1018 and the PR body say lock, settle, wire_chans and the mr reference keep their values.
  - AGENTS.md section 6, Tests lens: a test must be able to fail for the defect it claims to detect, and must not merely reproduce implementation assumptions.
  - Reviewer probes (`receipts/probes/SUMMARY.txt`, `receipts/probe_lock_settle/SUMMARY.txt`):
    - `lock_set`: the reject writes `{ram_q_r[31:13], 1'b1, ram_q_r[11:8], seq}`.
    - `settle_dec`: the reject decrements settle.
    - Planted in the engine only, each passes the NX harness (169/0). Only the lockstep compare against the reference copy fails.
    - Planted in the engine and the reference together, each passes NX 169/0, lockstep N=1 116/0 and N=8 119/0.
  - By contrast, these write-back mutants are caught: wire_chans, mr seed, settle restart, off-by-one, wrong stream address and no write.
  - On CRF the equivalent defect ("a reject seeds the cursor") is planted and caught by `[SQ-d1]` (`tb/verilator/crf_rx/sim_main.cpp:1623-1685`). The AAF lane has no off-format PDU first in an era, and none inside the settle window.
- **Impact:** if a later edit to the new write-back moved the lock or settle fields, every count-based check would stay green. Examples: a reject that locks an unlocked stream, so MEDIA_LOCKED is never counted for that era and the Table 5.6 LOCKED/UNLOCKED pair breaks; or a reject that shortens the settle window. The test guide's "writes only prev_seq" is then an unsupported claim. The shipping RTL at this head is correct: `{ram_q_r[31:8], cur_w.seq}` preserves bits 8-31.
- **Required outcome:** what the test guide says `[SQ]` proves must match what it grades. The natural outcome is an AAF `[SQ]` arm with an off-format PDU while the stream is unlocked (first in a fresh era) and one inside the settle window. Its count-based checks should show:
  - MEDIA_LOCKED counted at the first accepted PDU;
  - the settle window unshortened;
  - a format_mutants.py arm for each of the two defects, failing its named check.
- **Verification:** rerun `make -C tb/verilator/avtp_rxmon`, and rerun `scripts/probe_lock_settle.py` against the corrected head with both mutants planted in engine and reference. Both mutants must fail a named `[SQ]` check.

### F2 - RESIDUE - Docs - the ctx banner's list of N=1 deltas from the flat instrument omits #775

- **Where:** `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:88-99`, and the contract line at :15-22.
- **Evidence:** the banner lists the behavioural deltas of the shipping engine from `KL_avtp_rx_monitor`, including #762 and #765. The flat module's reject path (`hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:266-270`) still leaves `prev_seq_r` alone, so #775 is now a third delta. It is not listed. Line :15-22 also places "(a rejected PDU advances the sequence state ..., #775)" inside the flat module's per-PDU contract, and the flat module does not do that.
- **Impact:** a comment only. No code, test, measurement or conformance claim changes.
- **Exact fix:** at :97-98 change "and it does not compare the channel count with the current format (#765)." to "it does not compare the channel count with the current format (#765), and its format reject does not advance prev_seq (#775)."

### F3 - SUGGESTION (no verdict effect) - Tests - no AAF check that a reject leaves the 100 ms silence watchdog alone

A planted `sil_ms_r[ev_s_r] <= '0` on the reject survives the NX harness (`receipts/probes/SUMMARY.txt`, `aaf_reject_refreshes_silence`). This behaviour predates the change and #775 leaves it untouched; CRF has `validation_error_refreshes_timeout`. It is a candidate new issue, not part of this lane.

### Prior public findings

My verdict and ledger were written first. After that I read the PR's comments, submitted reviews (0) and inline threads (0).

One review was published during this round: [R686] POSITIVE, issuecomment-6381645752. It raised no finding at all, so there is nothing to resolve or retain.

F1 is new, and it disagrees with that review's Tests CLEAN. Its "wrap and state preservation" probe also runs on a locked, settled stream, so it cannot see F1's two mutants either.

## Lens results

[R685] PASS Conformance - `KL_avtp_rx_monitor_ctx.sv:1009-1021,1061`; `KL_crf_rx.sv:598-608`; `docs/reference/FR_NFR.md:271`; `receipts/focus/base-*.log` - both reject paths implement the ruling.
- AAF: prev_seq takes the PDU's sequence_num. That is what an accepted PDU writes, so the next PDU's expected value is seq+1.
- CRF: `exp_seq_r <= seq_i + 1`, mod 256, and `have_seq_r` is untouched.
- The anomaly flags stay gated by the format verdict: `iv_events` :594-605 and `w_ev_*` :400-409. A reject still raises UNSUPPORTED_FORMAT only.
- Head harnesses run against the base RTL fail the sequence checks: NX `[SQ2c]` got 1, `[SQ3c]`; CRF `[FMT-c1]`, `[SQ-b2]`, `[SQ-c2]` among 175; discontinuity `rejected marker never seeds the reference`. The head passes them. All frozen acceptance criteria are met.

[R685] PASS RTL - `KL_avtp_rx_monitor_ctx.sv:282-293,524-551,615-722,728-750,1009-1061,1238-1255`; `KL_crf_rx.sv:335-428,598-651`; `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:988-993,1045`; `receipts/gates/yosys-head-2tops.log`; `receipts/gates/lint-head.log` - the AAF path is correct.
- `M_PSEQ_S` is the tenth value of the 4-bit enum, and the walker keeps its `default`.
- The prefetch makes `ram_q_r` the stream's MON_STATE in `M_PDEC_S`. For s0 it is read in IDLE and again in PFRD3; for s>0 in PFRD3.
- `{ram_q_r[31:8], cur_w.seq}` preserves lock, settle, wire_chans, prev_mr, mr_seeded and the upper bits. `M_PSEQ_S` writes word 8 of `ev_s_r` once, on the engine-priority port; the window write waits on `lctx_wr_rdy_o`.
- The legacy and shadow mirrors see unchanged bits.
- No accept verdict, `dirty_p`, timestamp word, inc_list, tv/tnv, silence refresh or shadow update is added. The bundle in service and `ev_s_r` are stable through the extra cycle.
- A reject now takes 3 cycles (PDEC, PSEQ, IDLE) instead of 2. That is still shorter than the accepted walk, so ring pressure does not grow.
- A same-cycle bind still walks after the PDU and reads MON_STATE fresh.
- CRF: the reject branch changes only `exp_seq_r`. Settle reset, timeout, bind-rise and rate-break rules are unchanged. `rate_break_w` stays gated by `have_seq_r`. Only same-stream_id PDUs (`w_hit`) advance the cursor.
- The lockstep reference takes the same edit (`cur_r.seq`).
- Focused Yosys passes on the two changed tops: KL_avtp_rx_monitor_ctx cells=10991, KL_crf_rx cells=30776, tied-input and tap-purity gates PASS. Lint passes (89 <= 89; no finding in either changed file).
- Open risk (6): the flat `KL_avtp_rx_monitor` is instantiated only by `tb/verilator/avtp_rxmon/avtp_rxmon_wrap.sv:85` and `tb/verilator/aaf_audio_loop/aaf_audio_loop_wrap.sv:122`, and tsn_fuzz builds it as its DUT. It appears in the SoC and OOC source lists and as a standalone Yosys top, but nothing shipping instantiates it: `hdl/milan/milan_datapath.sv:7461` instantiates `KL_avtp_rx_monitor_ctx`. Searched across the parent and every initialized submodule. The risk is real only for the test instrument, and no shipping defect is left under this scope.

[R685] PASS Robustness - `receipts/probes/SUMMARY.txt`; `sim_main_nx.cpp:1000-1075`; `crf_rx/sim_main.cpp:1623-1685`; `sim_discontinuity.cpp:130-200` - examined:
- a reject carrying mr, tu and a late or early timestamp;
- a gap of one after a reject (SEQ_NUM_MISMATCH +1 and no STREAM_INTERRUPTED, which proves the count runs from the reject's number);
- a CRF reject first in an era;
- a reject at stream 3 against the stream-0 address (the mutant is caught);
- a reject that writes nothing (caught);
- off-by-one (caught);
- mr seeding and delta movement on CRF (caught);
- bind and timeout ordering by inspection.

The only uncaught robustness-relevant classes are F1's, recorded under Tests and Docs, where the reviewer assigns them. Unchanged behaviour stays unchanged under these probes.

**Tests: UNCLEAN.** F1 above. What does hold:
- Head `make -C tb/verilator/avtp_rxmon`, rc 0: flat 97/0, NX 169/0, lockstep 116/0 and 119/0, `lockstep_mutants.py` 14/14, `format_mutants.py` 9/9.
- Head `make -C tb/verilator/crf_rx`, rc 0: unit 15714/0, discontinuity 2201/0, talker step 69/0, `mutants.py` 23/23. All five named controls fail their named checks.
- Every changed stimulus hunk only consumes a sequence number across a reject; no `ck()` expectation changed. That covers avtp_rxmon `[G5]` :337-348 and `[UF2]`-`[UF4]` :931-960, crf_rx `bad_pdu(seq++)` with the replica's `bad_pdu(seq)` :191-197, discontinuity :138,198, and milan_dp `[CTRS-CRF]` :7065, whose planned counts still hold because P2's loss is now counted from the last reject.

**Docs: UNCLEAN.** F1 above (the TESTING.md:617 claim). What does hold:
- FR-STR-03 (`FR_NFR.md:271`), the compliance matrix row (`MILAN_COMPLIANCE_MATRIX.md:192`) and TESTING.md :628 state the rule correctly.
- The new source comments carry behaviour with issue and requirement IDs. A scan of all 327 added lines found no bench lane label, lane name, review round, reviewer ID or issue-comment ID.
- docs_check.py, check_doc_paths.py, check_doc_style.py, check_hygiene.py and the sv, cpp and py idiom gates all return rc 0.
- F2 is RESIDUE and does not un-clean this lens.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #775 ruling; FR-STR-03; ctx:1009-1061; crf:598-608; base-RTL runs | R685-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| RTL | CLEAN | ctx FSM, write and read muxes, verdict, mirrors; crf engine; reference:988-1045; Yosys on 2 tops; lint; flat-instance census | R685-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Robustness | CLEAN | 13 reviewer mutants; `[SQ]`/`[FMT]`/discontinuity harnesses | R685-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Tests | UNCLEAN (F1) | both suites with their mutant drivers; lock/settle probe; stimulus hunks; milan_dp:7065; sweep receipts | R685-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |
| Docs | UNCLEAN (F1; F2 RESIDUE) | FR_NFR:271; matrix:192; TESTING:617/628; ctx banner; docs gates; comment-rule scan | R685-1 | c7e87c8c87494f3444000b46954648ba1a94dcb8 |

## Published source-head evidence (author executions, not a manager source bank)

- **Sweep:** shards 0-3 each return exit 0 at head c7e87c8c, with 15 + 16 + 17 + 16 = 64 PASS suites and 54,074 + 331,530 + 262,066 + 1,541,945 = 2,189,615 checks, 0 failures. The tsn_fuzz field campaigns and their freshness checks were declared SKIPPED (generator absent). They ran nothing.
- **Static gates:** 30 return rc 0 (`static-c7e87c8c/gates.tsv`), including check_em_dash at the base.
- **route-1x1:** `route-1x1-check.log` gives RESULT PASS, fully routed, against the 2026-10-23 record in `syn/ooc/pp_resource_baseline.json`, which the task names the eleventh. SLICE is 15833 against 15835 (-2), LUT +54, FF +10, RAMB and DSP unchanged, WNS 0.141 ns, WHS 0.019 ns. The +5-slice STOP is not reached. These are desk measurements, not physical calibration.
- **Docs gates under Make 4.3:** receipts present (`docs-c7e87c8c`, builder legs 0 and 1). The host runner gate and the no-git step were not run, as the executor declared.
- **Hosted, exact head** (snapshot `receipts/gates/hosted-checks-snapshot.txt`): rtl-fast, verilator-lint, docs-gates 0-2, docs-check-no-git and yosys-elaboration completed with success. Most Verilator and Yosys shards were still in progress or queued at the snapshot. Physical gPTP was skipped. Skipped contexts are not executed validation, and the manager owns hosted acceptance.

## Reviewer executions

These used the pinned simulator, verified as Verilator 5.050 rev v5.050. Builds and runs went into disposable copies under `scratch/`. The clone was never edited.

- `receipts/focus/`: the two head suites, plus the base-RTL NX and CRF harness runs. The base CRF unit binary was rerun directly after a reviewer path typo; see `base-crf_rx-unit-run.log`.
- `scripts/probe_mutants.py` gives `receipts/probes/`: 13 mutants, 9 AAF and 4 CRF. 10 were caught; 3 survived: `aaf_lock_set` and `aaf_settle_dec` (F1), and `aaf_reject_refreshes_silence` (F3).
- `scripts/probe_lock_settle.py` gives `receipts/probe_lock_settle/`: the engine-only and engine+reference arms.
- `receipts/gates/`: focused Yosys on the two changed tops (rc 0), lint (rc 0) and the docs, hygiene and idiom gates.
- `receipts/clone-integrity.txt`: HEAD, tree, an empty status and index diff, all 1,441 tracked blobs and their modes matching HEAD, and the six submodule gitlinks with their status (`external` is uninitialized, as at the start). A `scripts/__pycache__/` that the gate runs had created (ignored) was removed afterwards.

## Real limits

- I did not rerun the full sweep, the full Yosys bank, route-1x1, the docs workflow under Make 4.3 or milan_dp. For those, the executor's published receipts are the source-head evidence.
- Yosys ran on the two changed tops only, with a local sv2v v0.0.13 where the pin is v0.0.12. A base-tree Yosys run could not start from a non-git copy and is not published.
- check_em_dash could not run locally: its pinned renderer is not installed, and shared installs are not allowed. The executor's receipt shows rc 0.
- The flat test instrument and tsn_fuzz were not exercised.
- No hardware or bench run was made. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Carry F1 back to the executor. Then a re-review at the corrected head must cover Tests and Docs again, plus RTL if the RTL is touched.
- Carry F2 to the residue checklist.
- Decide whether F3 and the flat instrument's reject path become new issues.
- Build and validate the current-dev merge candidate with the builder and native banks, and link those receipts at the merge turn.
- Accept the hosted and local replica results.
- Reconcile any later public findings.
- Obtain the second independent positive, maintainer merge authorization, post-merge containment, and issue and project closure.

R685-1 FINISHED
