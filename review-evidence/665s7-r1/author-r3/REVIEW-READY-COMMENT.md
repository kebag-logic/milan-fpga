[A757] REVIEW READY
Commit: `2128daad26b932feeed1ef2bde8f2774e8a51a31` (one commit on round 2's `2131eff4`; no merge, rebase, force or amend; nothing pushed)

Changed: the round 3 ruling (PR #874 issuecomment-6766550989), items 1 to 4. Item 5 (#608 in production) stays owed, and the fixture is untouched.
- **Item 1, attribution by what lwSRP did.**
  - The bench (`srptx.hpp`, `poll()`) marks each MRPDU at lwSRP's boundary, with no lwSRP or adapter edit. It records whether the MRPDU was sent at lwSRP's first transmit poll after its Join timer expired. A Join expiry only clears `join_wait` (`mrp_mad.c:854`, `:1421`, `:1539-1540`), so that poll sends what the timer held or finds nothing. With the Join timer stopped, it also records the last poll that sent nothing.
  - `srptx_grade.py` grades the Join interval only for the first kind, with no time window (`join_intervals`, `causes`). A LeaveAll frame the Join timer held counts too. `measure_time`'s JoinTime figures use the same attribution.
  - A frame sent after a Join expiry that found nothing is a requested transmit opportunity. It is graded within JoinTime + T_svc (220 ms) of lwSRP's last idle poll (`docs/reference/FR_NFR.md` 3.4.1, Milan v1.2 4.2.7.1.1, IEEE 802.1Q-2018 10.7.4.1).
  - The new rule's plant `requested-late` (221 ms) is refused by its own words, and its control at 219 ms grades clean.
- **Item 2.** `join-early-past-t-svc`, `join-interval-late`, and the 10 cs and 15 cs arms are still refused by their own words.
- **Item 3.** `make srptx` runs R813-2's case as two committed controls: the licence scenario with the peer's LeaveAll at ms 16280 and at ms 16240 (`--peer-leave-all-ms`). Both grade clean, and `srptx-plants` requires each to hold its case.
- **Item 4.**
  - The PR body's status no longer reads as stopped.
  - `ATTRIBUTE_MS`'s comment now says it serves the periodic and LeaveAll measurement only.
  - The grade's two garbled phrases are fixed.
  - The README's rate window reads "1.5 x JoinTime less T_svc (280 ms)".
- **Files:** `tb/verilator/milan_dp/srptx.hpp`, `twin_split.cpp`, `srptx_grade.py`, `srptx_plants.py`, `Makefile`, `README.md`, and `sw/firmware/ctrl/srp/README.md`.

Validation, at the head, on clean clones, all rc 0:
- `make -C tb/verilator/milan_dp srptx`: 0 findings in wire, hold, licence, licence-16280 and licence-16240.
- `make -C tb/verilator/milan_dp srptx-plants`: `26 of 26 refused; 4 of 4 controls inside their bound clean; 2 of 2 off-grid controls clean with their requested transmit opportunity`.
- `make -C tb/verilator/milan_dp srptx-mutants`: `12 of 12 refused`.
- R813-2's `scripts/request_probe.py tb/verilator/milan_dp WORK 280 240`, unchanged: 0 findings at both offsets. R814-1's code probe, unchanged: `join-10cs` refused (15 findings), `join-15cs` refused (16).
- The ablation: the grade at `2131eff4` refuses the 16280 control by F-1's words. Without the requested rule, `requested-late` escapes. Without the bench's Join record, the two Join plants escape.
- Every Join timer interval of the five runs is 198.958 to 200.024 ms. Every requested opportunity left at most 1.03 ms after lwSRP's last idle poll.
- `make twin`: the split capture is byte-identical to round 1's. `twin-plants` passes.
- Every `run:` step of every job a ready pull request to `dev-soft-core` triggers (docs, elaborate, rtl-fast, rtl; 69 job instances): 546 ran, 0 failed. 86 cannot run on this host and are listed with reasons. That covers:
  - the firmware self-test, 4 shards: `test_ctrl_firmware: PASS`, control mutants 570 of 570 caught;
  - `fw_coverage.py --check`: PASS;
  - every firmware mutant campaign;
  - `ctrl_boundary: PASS` with and without Verilator (firmware-boundary in the LiteX venv);
  - `behave`: 508 scenarios passed;
  - elaborate, the 19 Verilator shards with their unions, and the Yosys shards and portability.
- The full sweep, 4 shards, each on its own unit: 65 suites passed, 0 failed, 0 timed out; 2,192,910 checks.
- `test_builder.py --require-rv32`: all gates pass except 2 that cannot run here, as in round 1. S2's harness at 1x1/1if and 8x8/2if: 0 refusals. `make split`, `split-mutants` (26 of 26), `split-cdc` and `split_parallel.py --selftest` pass.
- `git diff --check` against `1d6bf555` and against `2131eff4`: clean.

Attempts before these results, each recorded with its cause, none a defect of the change:
- Wall-clock timeouts under host load (UNKNOWN, 0 failures):
  - `elaborate-gates-1`'s LiteX `test_soc_timing_cuts`. It passed with the clock raised, and on a dedicated unit.
  - `media_phase` and `mmcm_servo` in two replay shards. Each passed on a rerun and in the full sweep.
- One #833-class cancellation-control failure, re-run once, with both results kept.
- A census job I stopped for memory.
- Jobs killed by a host restart, each re-run from a fresh start.

Acceptance criteria: items 1 to 4 and 6 to 7 are met with the evidence above. Item 3 is now graded with the attribution the ruling asks for. Item 5 holds only under the published fixture and stays owed, so the PR body says "Relates to #867" and does not close it.

Open risks/questions:
- The requested rule's bound is lwSRP's last idle poll. So it holds the path from that poll to the wire (the adapter's polling, the ring, `KL_mbx_tx`, `ctl_tx_mux`), not lwSRP's own scheduling, which the boundary cannot show. It has a capture plant and a control, and no code arm.
- Periodic and LeaveAll frames keep their 100 ms window, which serves the measurement only.
