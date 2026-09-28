[A422] STOP
Branch: `590-592-599-firmware`, merge head `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` (tree `9ce926b9`). Local only, not pushed.
Merge: `9e3df3ed` merges dev `7a7582f0` into `93262f25`. The subject is one line; there is no body and no trailer. The processor gitlink stays `16be6768`.
Conflict: only `docs/integration/BAREMETAL_FIRMWARE.md`. Both lanes' text is kept unchanged: #610's D3 DR2a clause and retry paragraph, and this PR's runtime, capture and PHY paragraphs. The page differs from each parent by exactly the other lane's change.
Clean merges: `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` §18/§20 item 6 have no contradiction between the receipt figures and the D3 text. `test_builder.py` has disjoint hunks and no gate collision.
Stale statements: `1f039cfe` rewords `BOARD_PORTING_AX7101.md` (MAC_STATUS "until a driver writes it") and the `docs/findings/README.md` #397 row ("architecture decision ... open"). The searches and the residuals not reworded are in the handoff.

STOP reason: a round-3 gate fails at the merge head.
- Gate: `tb/verilator/fw_service_budget/run.py … --regrade` on all 15 kept round-3 native service runs. Each returns rc 1 with `stale or unbound build; rebuild` (`run.py:615`).
- In all 15 kept builds, exactly three bound inputs differ, and the merge brought all three:
  - `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`, from #597 (`N_CONTROL_P` wired into the processor shadow);
  - `sw/litex/milan_soc.py`, from #596 (clock-contract CLI refusal).
- The harness is correctly refusing to carry round-3 service evidence onto changed RTL/SoC. The same logs regrade rc 0 at `93262f25`.

Other gates at `1f039cfe`: all rc 0.
- Full builder bank, compiler present: 953 s, `EXCEPT 1 NOT RUN`, gate 11 as before.
- Full builder bank, compilers absent: 663 s, `EXCEPT 2 NOT RUN`, as before.
- Host self-test, `check_nvm_capture`, kept capture oracles (96 captures), `run.py --self-test` (47 checks), CI scope.
- Docs gates with the pinned Markdown environment; `check_em_dash --base 7a7582f0` finds 0 over 555 added lines.
- Source checks and `git diff --check 7a7582f0`.
- Reviewer probes graded 0; the phase, disabled-writer and edge-cross logs are byte-identical to round 3.
- `check_nvm_capture` does not bind RTL, so it passes even though the capture was also measured on pre-merge RTL.

Decision needed:
- (a) Re-run the 15 native service runs at the merge head and regrade. Round 3 needed about 39,000 s of runs.
- (b) Accept the round-3 regrade at `93262f25` plus the recorded drift for this merge.

Executor's recommendation: (a), because #597 changes the processor-shadow instance the harness simulates.
