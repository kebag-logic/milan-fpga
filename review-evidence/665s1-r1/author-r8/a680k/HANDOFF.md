STATUS: REVIEW READY (round 8 continuation 2, executor [A680k]): head `614635b7f9aed7c9138aef53d0b93ca6030ae31e`; every gate rc 0; nothing open

# #665 lane S1 ([A680k]): ruling 6463964028 on [A680j]'s two open questions

- Branch `665-s1-faces` (`origin` is `kebag-logic/milan-fpga`), from `dev-soft-core` `e76a755a`. Two commits on
  [A680j]'s `bdad673a` (one-line subjects, no body, no trailers), nothing pushed:
  - `124191ca` the control accepts cause 1 or 5; two self-test checks and four mutants; README rule; `scenario.py` docstring;
  - `614635b7` README only: at this head the control is caught with cause 5, and a clean image escapes it.
- Ruling: #665 issuecomment-6463964028 (item 1: option (a), with a planted control; item 2: #801, PR body).
  TAKEN: issuecomment-6463985214. REVIEW READY: issuecomment-6465783342. Earlier rulings and the round-8 assignment 6461128613 still in force.

## Work list

- [x] 1. The `as-built` control accepts an access fault of cause 1 or cause 5 (ruling item 1). No other change.
- [x] 1b. Planted control proving a clean image still refuses both: self-test checks (a clean boot and every other
  trap escape) with mutants, and a real 1x1 plant whose CPU decodes correctly (ESCAPED, no trap).
- [x] 2. `PR-BODY.md` states arm B's 1x1 T_svc miss (11.660 ms) and 8x8 ceiling (26.980 ms on if0), cause #801.
- [x] Gates (table below), all rc 0; REVIEW READY (`REVIEW-READY-COMMENT.md`)

## Changes (`git diff bdad673a 614635b7`, 5 files, +58 -8)

| File:line at `614635b7` | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/run.py:258-260` | `AS_BUILT_CAUSES = (1, 5)`, with its reason (#791: a fetch or a load meets the defect first) | ruling item 1, option (a) |
| `run.py:263-266` | `as_built_faults(refusals)`: trap refusals naming `TRAP <cycle> 0 <cause> ` with cause in `AS_BUILT_CAUSES`, the cause matched as a whole field, interrupt bit 0 | the rule as one function, so the self-test can plant it |
| `run.py:271-275` | `verdict` uses it; prints `CONTROL as-built caught|ESCAPED: an instruction or load access fault (cause 1 or 5)` | the printed rule names what it accepts |
| `selftest.py:34` | `import io` | silence `verdict`'s print in the checks |
| `selftest.py:667`, `:671-693` | `as_built_checks()`: synthetic boot-fault logs (`scenario.boot_fault_groups()`) through `grade.grade` and `run.verdict` with `cpu_regions='as-built'`; cause 1 and cause 5 caught; a clean boot, causes 2, 7 and 15, an interrupt numbered 5 and a bus error escape | the planted control's self-test half: a clean image refuses both |
| `selftest_mutants.py:401-408` | four mutants: cause 1 only (earlier rule), any trap, the cause's leading digit, caught whatever the boot does | each check can fail for the defect it names |
| `scenario.py:928-931` | `boot_fault_groups` docstring: a fetch (cause 1) or a load (cause 5); `run.verdict` names the cause | was "first fetch ... (cause 1)", false at this head |
| `README.md:674-676` | the control's rule: cause 1 or 5, either #791's defect; the self-test's two checks | docs |
| `README.md:681-683` | at this head caught with cause 5 (`TRAP ... 0 5 00000020`); the clean-image run escapes | was "escapes at this head", false now |

## Checks and planted mutants

| Check | Planted mutant | Failing words (`receipts/gates/harness-selftest.txt`) |
|---|---|---|
| `the as-built control is caught by an instruction access fault (cause 1) and by a load access fault (cause 5)` | `run.AS_BUILT_CAUSES = (1,)` (the earlier rule) | `MUTANT caught: ... ({1: 0, 5: 1})` |
| `the as-built control escapes on a clean boot and on a trap of any other cause` | `as_built_faults` takes any trap | `MUTANT caught: ... ({'': 1, 'TRAP 166 0 2 00000024': 0, 'TRAP 166 0 7 00000020': 0, ...})` |
| the same | the cause matched by its leading digit (`[15]` without the field's end) | `... 'TRAP 166 0 15 00000020': 0 ...` |
| the same | caught whatever the boot does | `... {'': 0, ...}` (the clean boot caught) |
| the real control on a clean image (`probes/plant-asbuilt-clean.diff`: the generator handed the regions' power-of-two cover under `--cpu-regions as-built`) | the plant is the clean image itself; the control must escape | rc 1: `1 groups graded, 0 refusals` / `CONTROL as-built ESCAPED: an instruction or load access fault (cause 1 or 5)`; 0 TRAP lines in its log; its PC trace reaches `aecp_image_load` (0xbbc4) at 7 ms; CPU netlist `VexiiRiscvLitex_1e5f104c...`, arm A's (`receipts/runs/plant-asbuilt-clean-1x1/`) |
| the real control at this head (`--cpu-regions as-built`, 1x1) | none | rc 0: `REFUSED boot-fault: ... ['TRAP 166 0 5 00000020', ...]` / `CONTROL as-built caught` (`receipts/runs/C-asbuilt/`; netlist `VexiiRiscvLitex_3432f054...`; ELF `fe939fff...` in both runs) |

## Gate table (head `614635b7f9aed7c9138aef53d0b93ca6030ae31e`; each receipt's `.head` or first line names it)

| Gate | Result | Receipt (`receipts/`) |
|---|---|---|
| harness self-test `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 91 PASS, 68 MUTANT caught, 0 ESCAPED, `self-test: 0 failures` | `gates/harness-selftest.txt` |
| the `as-built` control, 1x1, and its planted clean-image control (at `124191ca`; `614635b7` changes only the README) | caught rc 0; plant ESCAPED rc 1 (above) | `runs/C-asbuilt`, `runs/plant-asbuilt-clean-1x1` |
| docs workflow, 69 commands (`probes/docs_gates.sh`, incl. `check_em_dash.py --base`, `check_py_idiom.py`, `check_baremetal_only.py`) | 69 of 69 rc 0, 269 s | `gates/docs-gates.txt` |
| rtl-fast `firmware-boundary` steps (`probes/boundary_unit.sh`) | rc 0, 1,016 s: `ctrl_boundary: PASS`, 2,864 compiled sources of 3,094 invocations (as before); tree clean after | `gates/firmware-boundary.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050) | rc 0, 622 s, PASS: 775 of 885 (as before) | `gates/ctrl-boundary-only-verilator.txt` |
| `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12, CPUs 112-115, 116-119, 120-123, 124-127) | rc 0 each (4,700, 4,006, 5,297, 3,705 s): 15, 17, 16 and 16 suites pass (64 of 64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out; declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen absent). Equal to `bdad673a`'s | `sweep/sweep-614635b7/` (files over 200 KB in `large-files.txt`) |

Carried from [A680j]'s `bdad673a` receipts (`665s1-a680j/receipts/`), because the diff touches none of their inputs
(only the harness's `run.py` on the `as-built` path, its self-test files, a docstring and the README): the firmware
self-test shards, `fw_coverage.py --check`, `test_ctrl_nvm.py`, `test_builder.py`, `test_ctrl_memory.py`,
`gen_mailbox.py --check`, the linked images, the docs CI self-tests, the arm A and B legs and `slow-adp-rx`.

## Process notes

- CPUs: control runs and gates on this session's 64-79 in their own units (MemoryMax 4-8 G, peak 1.5 G); the sweep
  on 112-115, 116-119, 120-123, 124-127 (`cpu_ranges.py pick`, MemAvailable 33 GB at launch). No Vivado.
- Scratch: `$VALIDATION_STORAGE/scratch/665s1-a680k-work/` (builds, logs, sweep, SDK destination `sdk-r9`); the plant ran in
  [A680j]'s scratch worktree `665s1-a680j-work/plant`, moved to `124191ca` (detached; it was at `0eda061a`), the plant reverted after (status clean). Sweep clones
  `$LANES/665s1-a680k-shard{0..3}`.

## Receipts

`receipts/INDEX.md` is generated by `probes/collect_receipts.py` from the files present, host paths replaced by
placeholders; files over 200 KB are listed by sha256 and size in `receipts/large-files.txt`, not copied.
Scripts under `probes/`: `env.sh`, `leg.sh`, `unit.sh`, `controls.sh`, `plant-asbuilt-clean.diff`, `gate_unit.sh`,
`run_gate.sh`, `docs_gates.sh`, `docs_unit.sh`, `boundary_unit.sh`, `firmware_boundary.sh`, `behave_unit.sh`,
`pc_trace.py`, `collect_receipts.py`, `prbody_edit.py` (writes `PR-BODY.md` from [A680j]'s).
