[A652] REVIEW READY
Commit: eef90b4238b6c19b679b44adc6f09362809be153 (branch `761-762-mr-interrupt`, one commit on round-2 head `2cd2750d`). The branch is local; it is not pushed, and PR #767 is not edited.
Changed (round 2b, under the extended #762 scope ruling, comment 6265746720):
- `KL_avtp_rx_monitor_ctx` (AAF inputs): a sequence gap of two or more lost PDUs counts STREAM_INTERRUPTED only while the input is started (`&& !stopped_i[ev_s_r]` on the gap term). The stopped state is read at the PDU's accept verdict, the gap's one boundary. SEQ_NUM_MISMATCH is unchanged. The engine delta is one widened condition and a comment.
- `KL_crf_rx` (CRF input): the same rule, `w_ev_si_w` gains `&& !stop_i`, read on the gap PDU's own accept edge.
- The lockstep reference and the CRF harness's C++ replica carry the same line, so the cycle and per-PDU comparisons stay exact; the rule is graded by count.
- `REGISTER_MAP.md`, the compliance matrix (5.4.2.25) and `TESTING.md` state the gap rules with Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20 and Table 5.6, and link the extended ruling.
- No register map, top-level port or parameter change.
New count-graded checks, each with planted mutants in the engine AND the reference (AAF) or replica (CRF):
- AAF `[SI]`: a started gap counts once; a stopped gap counts nothing, nor a second one, and unlocks nothing (its SEQ_NUM_MISMATCH still moves: liveness); after START a gap counts again; at N=8 another input's STOP leaves the gap counted. A sweep lands a STOP, and a START, on every edge from 4 before to 20 after a gap PDU's pulse, idle and with the walker occupied; the gap counts once exactly when the input is started on the edge its accept verdict rises. Mutants `stopped gap`, `sticky stop` (START never re-arms the gap) and `gap stop late` (state read one cycle after the verdict, caught only by the sweep), at N=1 and N=8.
- CRF `[762-SG]`: started gap +1; stopped gaps +0, unlock nothing, one SEQ_NUM_MISMATCH interval; after START +1; a STOP or START on the gap's own edge decides it, one an edge later does not. Mutants `stopped_gap_interrupts` and `sticky_stop_gap`; only the `[762-SG]` count checks fail under them, no replica compare.
Validation (head eef90b42, clean clones, CPython 3.12.3 CI build, Verilator 5.050; all rc 0 unless stated):
- docs gate_50, all fourteen commands: rc 0 (`shard 0/35 refused`, 34 driver cases).
- 63-suite sweep, five shards in two clean clones: 63/63 suites, 2,188,354 checks, 0 failures, 0 timeouts, no re-runs; the shard union equals `--list`. Inside it: mclk 34/34, lockstep mutants 14/14, crf_rx mutants 18/18.
- avtp_rxmon: flat 97, N=4 stack 121, lockstep 116 (N=1) and 119 (N=8) checks, 0 failures; `lockstep_mutants.py` 14/14. crf_rx: 15,202 + 2,201 + 69 checks, 0 failures; mutants 18/18. milan_dp (all shapes): 0 failures.
- gm-step full mutant campaign: 22/22.
- Yosys 58/58. xvlog 0 findings. Builder bank: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, needs a local mf48 tree). Lint ratchet and every other docs-workflow gate (82 commands) rc 0, except the same two host-only self-tests as round 2 on files unchanged since the base: `act_ci.py --selftest` (identical failure lines) and the git-absent case of `check_todo_ownership.py --selftest` (45/45 under the host Python).
- route-1x1 (recipe unchanged, Vivado 2026.1, xc7a100tfgg484-2, default seed): `pp_resource_gate.py check --endpoint route-1x1` rc 0; LUT 49,597 (-16 vs the record), FF 52,400, SLICE 15,680, WNS +0.189 ns, WHS +0.014 ns, fully routed; worst setup path in the SoC CPU, worst hold path in the TDM render FIFO.
Acceptance criteria: met, with #762 read under the scope ruling and its extension. #761 unchanged from round 1. #762: a silence or a sequence gap on a started input counts once; on a stopped input neither counts; after START both count again; STOP with live traffic counts nothing; an Unbind never counts, and one after the silence's expiry leaves it counted. Each rule has count-graded cases in both engines with planted mutants. Hosted docs-gates and act were not run: the head is not pushed.
Open risks/questions:
- A followed AAF stream's return still raises no restart; the ruling keeps it as is (#761 and IEEE 1722-2016 4.4.4.3 name the CRF only).
- R663-1-S1 (a dynamic ungated-edge row for the mclk suite) is not taken; the builder's exact-initializer pin still refuses that edit.
