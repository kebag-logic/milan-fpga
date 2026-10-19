[A652] REVIEW READY
Commit: d30a208d44d5868cc356e6a8b7abc89b062ca9bd (branch `761-762-mr-interrupt`, three commits on the PR #767 head `eef90b42`, no rebase, no amend). The new commits are for the manager to push; PR #767 is not edited.
Changed (round 3, answering R663-2 under the round-3 assignment, #767 comment 6274405031):
- R663-2-F1 (`336a6f6a`): `[762-DP]` in `tb/verilator/milan_dp/sim_nxn.cpp` is the integrated case. It runs on every broad `sim_nxn` leg, the shipping Arty shape `obj_nxn4c` included, on AAF Stream Input 0. STOP_STREAMING and START_STREAMING arrive over the wire, and every count is read with `GET_COUNTERS(STREAM_INPUT, 0)`. While the input is stopped, a gap of two lost PDUs moves SEQ_NUM_MISMATCH +1 (live) and STREAM_INTERRUPTED +0. A silence that expires while stopped moves MEDIA_UNLOCKED +1 (live) and STREAM_INTERRUPTED +0. After START and a relock past the settle window, the same gap counts STREAM_INTERRUPTED +1. The silence is the monitor's own watchdog, advanced to 3 ms short of its limit as the `[CTRS-CRF]` arm does; the expiry and every count after it run for real (Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20, 5.3.8.10 Table 5.6).
- R663-2-F2 (`cb65d9d7`): both port comments, as written in the review (`KL_avtp_rx_monitor_ctx.sv:152`, `milan_datapath.sv:6307`).
- `d30a208d`: the milan_dp README paragraph for `[762-DP]`.
- R663-2-F3: the PR body's status lines are corrected in the lane's PR-BODY.md: hosted state at the head, reviewers `[R663]` (internal) and `[R664]` (external). The PR itself is not edited. R663-2-S1 is not assigned and not taken.
- No RTL logic change: both RTL edits are comments. So route-1x1 was not re-run.
Planted mutants at `milan_datapath.sv:6308`, each rebuilt through `build-nxn4c` and run; every failing check in the leg is listed:
- port tied to `'0`: fails `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` (each got 1).
- wrong vector, sink 1's level `acmpl_stopped_v_w[N_STREAMS:1]`: the same two checks.
- wrong vector, the bound level `acmpl_bound_v_w[N_STREAMS-1:0]`: fails `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` (got 0).
- clean control: 1,981 checks, 0 failures.
Validation (head d30a208d, clean clone, CPython 3.12.3 CI build, Verilator 5.050; all rc 0 unless stated):
- `make -C tb/verilator/milan_dp`: rc 0, 0 failures on every leg. `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981 checks, each +13 for `[762-DP]`. notify 423, crflic 416, dynmap 162, prune 33.
- `make -C tb/verilator/avtp_rxmon`: flat 97, stack 121, lockstep 116 (N=1) and 119 (N=8), 0 failures; `lockstep_mutants.py` 14/14.
- docs gate_50, all fourteen commands: rc 0 (`shard 0/35 refused`, 34 driver cases).
- 80 of the 82 other docs-workflow gate commands are rc 0. The same two host-only self-tests as rounds 2 and 2b fail, on files unchanged since the base. `act_ci.py --selftest` gives the same 31 failure lines as round 2b. The git-absent case of `check_todo_ownership.py --selftest` fails under this host's CPython 3.12.3 build and gives 45/45 under the host Python.
- Builder bank: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, needs a local mf48 tree).
- Hosted at `eef90b42`: every check run succeeded, including `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check` and `docs-gates-0/1/2`; the nightly physical gPTP job was skipped. The new commits have no hosted run or act replica yet, because they are not pushed.
Acceptance criteria: met, with #762 read under the scope ruling and its extension. #761 is unchanged since round 1. The AAF half of the stopped-input rule is now graded at the datapath's GET_COUNTERS face, and the CRF half was already graded there.
Open risks/questions:
- A followed AAF stream's return still raises no restart; the ruling keeps it as is.
- R663-1-S1 and R663-2-S1 are suggestions and are not taken.
