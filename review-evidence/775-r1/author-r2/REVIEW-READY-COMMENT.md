[A666] REVIEW READY
Commit: c7e87c8c87494f3444000b46954648ba1a94dcb8 (branch 775-offformat-seq-advance, on dev a032c6d6; not pushed, the manager pushes and opens the PR)
Changed:
- AAF input, KL_avtp_rx_monitor_ctx.sv:1009-1020: a discarded off-format PDU writes back MON_STATE with only prev_seq replaced by its sequence_num, through a new one-cycle state M_PSEQ_S (:292, :638-642, :1061). Lock, settle, wire_chans and the mr reference are unchanged. There is no accept verdict, no timestamp word and no counter walk, and only the UNSUPPORTED_FORMAT flag is raised. The lockstep reference takes the same edit.
- CRF input, KL_crf_rx.sv:603-607: the rejected branch sets exp_seq_r <= seq_i + 1. have_seq_r is untouched, so only an accepted PDU seeds the cursor.
- Tests: avtp_rxmon [SQ] (22 checks) and crf_rx [SQ] (23 checks). One off-format PDU mid-stream carries a toggled mr, tu and a late timestamp. It counts UNSUPPORTED_FORMAT +1. Over the two following observation intervals SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP, EARLY_TIMESTAMP, STREAM_INTERRUPTED and MEDIA_UNLOCKED do not move. A gap of one after an off-format PDU counts SEQ_NUM_MISMATCH +1 and no STREAM_INTERRUPTED. On CRF, an AAF PDU first in an era seeds nothing.
- Stimulus that reused a sequence number across a reject now consumes one: avtp_rxmon [G5]/[UF], crf_rx, and the milan_dp [CTRS-CRF] event arm. No check or expectation changed.
- Docs: FR-STR-03, the compliance matrix row and the testing guide.
Validation (clean clones at the head):
- make -C tb/verilator/avtp_rxmon: rc 0. NX 169/0, lockstep 116/0 and 119/0, lockstep_mutants.py 14/14, format_mutants.py 9/9.
- make -C tb/verilator/crf_rx: rc 0. Unit 15714/0, discontinuity 2201/0, talker step 69/0, mutants.py 23/23.
- Planted controls, each failing its named check:
  - AAF no advance fails [SQ2c] SEQ_NUM_MISMATCH unchanged.
  - AAF whole MON_STATE fails [SQ2d] MEDIA_RESET unchanged.
  - AAF timestamp walk fails [SQ1d].
  - CRF no advance fails [SQ-b2].
  - CRF reject seeds fails [SQ-d1].
- The base RTL under the head's harnesses fails as the bench did: NX [SQ2c] got 1, crf_rx [SQ-b2]/[SQ-c2]/[FMT-c1].
- Full sweep as 4 parallel shards: rc 0, 64/64 suites, 2,189,615 checks, 0 failures.
- syn/yosys/run.sh: rc 0, 60/60 tops. lint_rtl.py --check: rc 0 (89 <= 89). 30 static gates: rc 0.
- Docs workflow gates under GNU Make 4.3: 42 run, rc 0, builder legs included. Not run: gate_42, which runs the candidate act_ci.py on the host, and the no-git step, whose two gates ran in place.
- route-1x1, one Vivado run under the exclusive lock after the sweep: routed, all constraints met, WNS +0.141 ns, WHS +0.019 ns. pp_resource_gate.py check --endpoint route-1x1: rc 0, PASS against the 2026-10-23 record: SLICE 15833 (-2), LUT +54, FF +10, RAMB and DSP unchanged. The STOP threshold (+5 slices) is not reached.
Acceptance criteria: met. Items 1-4 of the assignment and the issue's Required list are covered with the evidence above.
Open risks/questions:
- The flat test instrument KL_avtp_rx_monitor, which no shipping module instantiates, keeps its old reject path. Not assigned; a possible new issue.
- A gap or repeat on the discarded PDU itself counts nothing, per the ruling.
- No bench run here.
