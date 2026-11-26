# #970 round 8: #1015 the firmware-boundary CI fix — handoff

**Status (11-26): REVIEW READY at `35d29eb71d2cc76717a4550787ef53ff2b72181f`** (branch `970-discovery`, worktree
`$VALIDATION_STORAGE/adp970-a847`). Committed on `57f32b28`, not pushed. Nothing was posted or flashed, and the bench
was not touched.

**ETA:** nothing pending on this side.

## 1. The failure and the fix

- **The failure:** the hosted rtl-fast job `firmware-boundary` (run 45814568764, job 140054650541) failed at
  `57f32b28` with exactly one refusal:
  - "`tb/verilator/ctrl_service_budget/model_counts.py` names the firmware's tree and is a program, and is neither a
    known builder ... (OUTSIDE) or compiles only in a suite (SUITES)".
  - The job stopped there, so its self-test never ran.
  - Log: `receipts/r8/hosted-boundary-57f32b28.log`.
- **Why it was refused:**
  - The file's text names `sw/firmware/ctrl/adp/adp_mbx.h`, so the check treats it as naming the firmware's tree.
  - It has a `__main__` block, so the check treats it as a program.
  - It is in no table.
  - In fact it reads the header as text and compiles nothing.
- **The fix:** commit `35d29eb7`, one file, +2 lines. It adds an `ctrl_configs.OUTSIDE` entry beside its neighbours
  in the harness: `"tb/verilator/ctrl_service_budget/model_counts.py": "holds scenario.py's ADP model counts to the
  counts adp_mbx.h states, read as text; it compiles nothing"`. No other file changed.

## 2. Validation at the committed tree

**CI's two captures, made the way `firmware-boundary-capture` makes them:**
`ctrl_boundary.py --require-rv32 --without verilator --leg {0,1}/2 --capture-out <dir>`, with the pinned RV32 SDK.

| Leg | Compiler invocations | Builder runs | rc |
|---|---|---|---|
| 0 | 1,888 | 1 | 0 |
| 1 | 1,716 | 6 | 0 |

**CI's judging command:** `ctrl_boundary.py --require-rv32 --selftest --without verilator --capture <leg 0>
--capture <leg 1>` reports **`ctrl_boundary: PASS`**, rc 0.

- 4,085 compiled sources of 4,380 recorded invocations, with 0 findings.
- 112 boundary, 192 pin and 4 figure controls, 0 misbehaved (308 of 308 `[ok]`).
- Its own planted cases of an unclassified program naming the tree are still refused by name: unclassified copies of
  `test_ctrl_memory.py`, `ctrl_memory.py` and `milan_soc.py`, the F5 builder removed from the registry, and a dropped
  builder.

**Negative control, in memory** (`receipts/r8/outside_control.py`, rc 0; no file edited):

| Case | Result |
|---|---|
| with the new entry | `model_counts.py` is not refused |
| entry removed | it is refused with the hosted job's sentence, word for word |
| a planted `tb/verilator/ctrl_service_budget/planted_counts.py` with a `__main__` block that names `sw/firmware/ctrl` | refused by name |

**Python idiom gate:** rc 0.

## 3. Other files of this PR that name the firmware's tree

I checked every Python module and Makefile this PR adds or changes against `4df125b8` (26 paths).

| File | Names the tree? | Classified as |
|---|---|---|
| `tb/verilator/ctrl_service_budget/model_counts.py` | yes | OUTSIDE (this round) |
| `tb/verilator/ctrl_service_budget/scenario.py` | yes | OUTSIDE, already |
| `sw/firmware/ctrl/test/ctrl_mutants.py` | yes | SUITES, already |
| `adp_first_mutants.py`, `run.py`, `hooks.py` | no | not builders by text |

The full CI run above judged all of them, with 0 findings.

Logs: `receipts/r8/` (index in `receipts/INDEX.md`).

Branch head: `35d29eb71d2cc76717a4550787ef53ff2b72181f`.
