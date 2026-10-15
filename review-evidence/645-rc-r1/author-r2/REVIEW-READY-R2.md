[A620] REVIEW READY
Commit: `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c` (round 2 for PR #742, on `2639eecf`: `e0960932` harness, `fb5dd3da` docs; local, not pushed)

Answers R635-1 and R634-1 as ruled in the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-6193474559). The RTL does not change (`hdl/` byte-equal to `2639eecf`).

Changed:
- `tb/verilator/follow_ring/sim_main.cpp`: `kB17MarginLoUs = kB17[4].later_us - kTickUs` (9.427 us) and `kB17MarginHiUs = kB17[4].burst_us` (24.565 us), derived from cycle 5's replay row; the comments give the derivation and say B17's 10 us listing threshold bounds nothing.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md`: "A bind at INTERNAL" states the window's derivation, restates every `sweep-bind` count, and rewrites the arming-window limit (out-of-window slips per grid; the in-window one-pair dup, pre-existing on dev, #743); the test plan's `follow_ring` row says the same.

**R635-1-F1 = R634-1-F1.** B17's cycle 5 gives both edges from its own `c05.json`: below 24.565 us, the peak of its first burst, which slipped the ring; above 30.260 - 20.833 = 9.427 us, since the slip moved the ring one tick off its empty edge and its 30.260 us later burst slipped nothing. The other nine cycles' own bounds (above 6.74 to 9.24 us, below 24.97 to 29.31 us) all contain that window. The B17 summaries hold no per-PDU lateness under the 10 us listing threshold, so a measured pre-burst maximum could not be extracted; the later-burst bound is used. "Since nothing that late slipped it" is gone from the design, the harness and the PR body. The split moved from 169 / 151 to **177 / 143**: the 8 binds of `bind_j5_p05` (phase 0.3125, 0 to 5 us) prime 9.440 us at their lowest and now count inside. `sweep-bind` was rerun on both datapaths:

| `sweep-bind`, 320 binds | Dev's datapath | With the arm |
|---|---|---|
| Runs passing | 0 / 32 | 32 / 32 |
| The 177 in-window binds | each slips exactly one frame at its first burst | none moves `SLIP_LB` |
| The 143 outside | 43 one frame, 99 two, 1 a frame and a pair | 6 slip one frame before the ring acts, 0.13 to 2.13 ms after the first PDU |
| Arms / settle / render recentres | 0 / 0 / 0 | 320 / 320 / 320, firing 2,047.0 to 2,048.0 ticks after the arm |
| Slips after the ring acts | | 0 |

**R634-1-F2.** The arm stays as ruled. Finer grids, both datapaths, at the 9.427 us bound:

| Grid | In the window: one-pair dup (`SLIP_LB` +1) before the ring acts | Out of the window: one-frame slip before the ring acts |
|---|---|---|
| 32 phases, 0 to 5 us, ten cycles | 1 of 151 (cycle 7, phase 0.84375, 0.127 ms after the first PDU) | 19 of 169, four phases 0.78125 to 0.875, up to 2.50 ms |
| 128 phases of cycle 7, 0 and 0 to 5 us | 2 of 140 (phases 0.890625 and 0.9296875, 0.127 and 0.252 ms) | 6 of 116, up to 2.88 ms |

Every early slip in the three grids (6, 20 and 8 binds) is identical, in kind and to the microsecond, on dev's datapath: pre-existing, and the arm does not remove it. R634-1's 1 of 141 and 2 of 132 are the same three dups under the 10 us classification. `sweep-bind`'s 16 phases reach none of them. #743 owns the dup's mechanism; not investigated here. No slip after the ring acts in any of the 896 head binds.

**R634-1-S1.** The PR body cites `AREA_BUDGET.md:124`: 50,013 LUT, 11,973 over; +3 LUT is 0.025 % of it.

Validation, at `fb5dd3da`, Verilator 5.050, each rc 0 and unpiped:
- `make -C tb/verilator/follow_ring`: b8 48, pullin 18, bind 30 checks, 0 failures (tally 96 / 0, verdict rc 0); small pulls 10/10; settle control PASS at four rates.
- `make -C tb/verilator/follow_ring mutants`: 15/15 caught, each by its named check.
- `sweep-bind` (`sweep.py bind --jitter-us 0 5 --extra --dwell-s 0.5`): 32/32.
- `check_em_dash.py --base f6260253` (0 findings, 144 added lines), `git diff --check`, `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `gen_module_matrix.py --check`, `check_feature_status.py`, `check_gptp_docs.py`, `check_baremetal_only.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check` and `--selftest`. One `check_baremetal_only.py` attempt under the Markdown-only environment refused for a missing YAML module, rc 2; it is retained, and the rerun under the system interpreter is rc 0.
- The investigation grids exit as expected: the 32-phase and dense head grids rc 1 only on the in-window dup above, and the dev grids rc 1 on the reproduction.
- Not rerun, since nothing they read changed: the other ten suites, the physical gPTP leg, lint, xvlog, Yosys, the builder and the area synthesis. Round 1's receipts stand.

Acceptance criteria: the round 2 items 1 to 3 are met as above. #645's own acceptance stays the manager's post-merge bench repeat of B17's ten binds; read a `SLIP_LB` +1 dup within a bind's first 42.7 ms against #743.

Open risks/questions: none new. The in-window one-pair dup is unresolved and owned by #743. The PR body for round 2 is ready, including a Round 2 section, but not applied: no push and no PR edit from this lane.
