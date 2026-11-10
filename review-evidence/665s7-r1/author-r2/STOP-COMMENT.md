[A757] STOP
Head: `2131eff48066da1e3bbeb6b417ea0655fa7c7741` (two commits on `5fb6904f`; nothing pushed)

Round 2 on PR #874 (ruling issuecomment-6763709522, items 1 and 2; R814-1 F-1 and F-2). Everything in both items is done except one line of item 1, which needs a decision.

**The line.** Item 1 says: "Derive `SVC_MS` from the one source the firmware budget uses, not from a literal." At base `1d6bf555` no such source gives 20 ms for SRP:
- `tb/verilator/ctrl_service_budget/scenario.py:91`, `:99` (the CPU budget harness, which `nvm_split_target` imports): `T_SVC_MS = 10.0` ("proposed") and `CEILING_MS['srp'] = 18.0`.
- `tb/verilator/ctrl_service_hooks/hooks.py:44`, `:84`: SRP graded at min(20, 18) = 18 ms. Its docstring, `:9-12`, says the 2026-11-06 bounds "grade nothing, until #810 brings them".
- `docs/reference/FR_NFR.md:333`: T_svc = 10 ms, proposed.

The 20 ms values are only on S2b's branch. Derived here, `SVC_MS` would be 10 or 18 ms. Both are tighter than item 3's 20 ms, and 18 ms is what F-1 refused. Changing that source is S2b's change, and it would move S2's harness, the hooks and the NVM target's bounds.

So `tb/verilator/milan_dp/srptx_grade.py:64` is `SVC_MS = 20`, citing #867 item 3 and the 2026-11-06 ruling. Every bound and the `[608]` window derive from it. The decision needed is one of:
- (a) accept that literal until #810 lands, with the switch to the budget source as a merge residue (recommended);
- (b) derive from `scenario.py` now, at 10 ms, which fails item 3 and this round's controls;
- (c) bring S2b's bound change into this lane.

**Done.**
- **F-1 (`0d8e89bc`).**
  - Every `[TIME]` bound and the `[608]` window are at 20 ms: 220 ms Join follow-up, 280 ms rate window, 9,780 to 15,220 ms LeaveAll.
  - `join-late-in-t-svc` is now `join-late-past-t-svc`: 221 ms, refused by `followed at ms 222, past JoinTime + T_svc (220 ms`. The control `join-late-within-t-svc` at 219 ms grades clean.
  - The plants hold item 3's 20 ms apart from the grade's. Re-derived at 18 ms the grade fails all 3 controls; at 22 ms, 5 plants escape; only 20 ms passes.
- **F-2 (`2131eff4`).**
  - The Join-timer interval that `measure_time` computes is graded on both sides. The bound is JoinTime's range in Milan v1.2 Table 4.3 (`FR_NFR.md` 3.4.1: 180 to 240 ms), widened by T_svc on each side (160 to 260 ms), as LeaveAll is; IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7.
  - New plants: 159 ms and 261 ms, each with a control 1 ms inside.
  - New code arms: lwSRP Join timers of 10 and 15 cs (MSRP at 1/100/200 and 1/150/300 ms). Each is refused three times by `ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms`. With the new check off, each grades with 0 findings, and so do the two new plants.
  - R814-1's 17 cs arm (170 ms) is inside 160 to 260 ms and is not refused. It is recorded, not committed.

**Exit check (not triggered).** Every Join-timer interval of the unplanted runs is inside 160 to 260 ms:

| Scenario | MSRP | MVRP |
|---|---|---|
| wire | N 104, 198.989 to 200.000 ms | N 104, 198.989 to 200.015 ms |
| hold | N 34, 198.989 to 200.000 ms | N 32, 198.989 to 200.000 ms |
| licence | N 8, 198.989 to 200.000 ms | N 5, 198.989 to 200.000 ms |

The measured blocks of all three reports equal round 1's.

**Gates at the head**, clean clones, rc 0:
- `make srptx`: 0 findings in each scenario;
- `srptx-plants`: 25 of 25 refused, 3 of 3 controls clean;
- `srptx-mutants`: 12 of 12 refused, after clean controls;
- every `run:` step of the nine docs-workflow jobs;
- rtl-fast `changes`, `firmware-boundary` and `firmware-verilator`: 120 steps across all twelve jobs, all rc 0, and 11 that cannot run here, each with its reason; `ctrl_boundary: PASS` with 183 pin controls;
- `git diff --check 1d6bf555`.

The full sweep, the firmware self-test, the mutant drivers, S2's harness, `test_builder.py`, `behave`, and the rtl and elaborate workflows were not run here. They run once on the final head. The round 2 change touches only the three `srptx_*.py` scripts and two READMEs, and none of those gates reads them.

Item 5 (#608 in the production composition) stays owed, and the fixture is untouched.
