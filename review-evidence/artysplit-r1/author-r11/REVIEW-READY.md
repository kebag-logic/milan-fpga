[A829] REVIEW READY

Commit: `c0b625d1792e61b8e99944daea65b842e6b9dcde` (local, branch `arty-int-1127`; nothing pushed or posted).

Changed:
- `ea73a3f74`: the bare-metal gate's five findings, reworded with their meaning kept. Three were retired-stack `Linux` terms (section 15, `ctrl_loop.h`, the harness README); two were `CPU/sys` (`arty_grade.py`, `egress_ledger.py`).
- `22adb80ed`: the test-evidence ratchet's disposition for `egress_mii.py`'s read of the gasket parameter.
- `5469c8dc5`: the firmware coverage ratchet. An exclusion row for the `lat` command's infeasible line-end arc (seventeen rows now); the console recorded at 154/154 lines and 97/97 branches.
- `c0b625d17`: the register reference. The writable timestamp corrections' prose moved from the hand-edited generated page into `register_descriptions.json`, and the page regenerated.

Validation:
- Bare-metal gate at the head: 0 findings over 1,981 files; its self-test 867 arms.
- Every CI job a pull request runs, run locally at the head step for step, 67 jobs and 212 gate steps, all pass: docs 7, elaborate 5, rtl-fast 23, rtl-full 32.
- Every shipping product ELF is byte-identical to `640699e6`'s: Arty split `f17d1a9d…`, AX7101 8x8 `0f1450ac…`, AX7101 1x1 tdm8 `6e0a5412…`. `ctrl_loop.h` is comment-stripped identical.
- Round 10's census extract regrades identically at the head (159/159), and the 100 Mb/s egress row is again 505.738 us. No re-measurement was needed.
- Standalone gates at the head: 23/23.

Acceptance criteria: met.

Open risks/questions:
- The local CI is a step-for-step run of the workflow files, not an `act` replay, since the head is not pushed. The pinned tools stood in for the setup steps, and the hosted run remains mandatory.
- Three gate failures beyond the five reported were in this lane's earlier rounds: the test-evidence disposition, the console's coverage record, and the hand-edited register page. They would have failed hosted CI at `640699e6` too.
- Fourteen other `coverage.ratchet` rows carry stale totals from earlier merges, all at 100 % either way. The ratchet passes them, and they are left alone.
- Round 10's open questions stand: the rings-at-capacity 2.65 ms figure, the TX_TAIL premise, the +62 routed LUTs, and #977's integration.
