[R606] POSITIVE - exact head ce10328c3d89d81509e47836fa4a48b22ecdbc20

# R606-3: internal cleared-context review of PR #721 (issue #640, Mark II lane M8a-1), round 3

- **Head:** `ce10328c3d89d81509e47836fa4a48b22ecdbc20`, tree `783d10c5ae40dad516d52e1fbf77b0e25680e4a3`.
  - Round 3 adds five one-line commits on the round-2 head `76605880`, with no rebase: `22caf735`, `087df144`, `4a2608cd`, `4a57b41d`, `ce10328c`. The first parent of `22caf735` is `76605880a20005cbc2acad1b23ba2ccebde64ca8` (`receipts/commit_shape.txt`).
  - The delta `76605880..ce10328c` touches 8 files: `scripts/ci_scope.py`, `sw/litex/ctrl_memory.py`, `sw/litex/test_ctrl_memory.py`, and five pages under `docs/`.
  - **Nothing under `hdl/`, `tb/` or `syn/` changed since `76605880`**, and no gitlink changed. All five gitlinks are identical at `e8454e27`, `76605880` and the head.
- **Scope authority:**
  - assignment #640 comment 6100371426;
  - ruling 6101485877, which defines M8a-1;
  - round-3 assignment 6107088105, items 1-5, which answers R606-2 (#721 comment 6107064124) and R607-2 (#721 comment 6107065061);
  - the author's REVIEW READY, #640 comment 6107961867.
- **Verdict:** POSITIVE. I applied all five lenses to the delta at this head and found no BLOCKER, MAJOR or MINOR.
  - Every prior finding the round-3 assignment names is resolved by construction and by execution at this head.
  - One RESIDUE (PR-body wording) and three optional SUGGESTIONs are recorded below.
- **Execution evidence:**
  - Source-head execution evidence is the author's published gate receipts plus the reviewer runs below.
  - No manager source bank ran at this exact head, and none is claimed or inferred.
  - Hosted `rtl-fast` is **success** at this exact head, and its jobs executed (details below). The manager owns hosted and act acceptance.

My independent pass over the delta was written down before I read either round-2 report.

## What was run at this head

Commands are in `scripts/COMMANDS.md`. The LiteX interpreter is a CPython 3.12.13 venv holding only PyYAML and `sw/litex/litex_pins.txt` (`receipts/venv_freeze.txt`). It has **no `pythondata_software_*` package**. It was prepared as `elaborate.yml` prepares it: `scripts/ci_litex_env.py`, then `sw/litex/patches/apply.sh`, which applied 5 patches. Verilator is the scoped 5.050, `rev v5.050` (`receipts/verilator_identity.txt`). The RV32 compiler is the one `fw_rv32.compiler()` finds.

| Gate / probe | Result | Receipt |
|---|---|---|
| `python3 -I scripts/ci_scope.py --selftest` | rc 0, `selftest: PASS` | `ci_scope_selftest.*` |
| `ci_scope.py` on `docs/design/SPLIT_CONTROL_MEMORY.md`, read from stdin and from argv | `true`, `true` | `ci_scope_classify.*` |
| Control: the same selftest at `76605880` | rc 1, `FAIL gate-read page docs/design/SPLIT_CONTROL_MEMORY.md (named at sw/litex/test_ctrl_memory.py:81) is relevant` | `control_76605880_ci_scope_selftest.*` |
| `scripts/ci_events.py --check` and `--selftest` | rc 0 and rc 0. The check covers 1,749 contract items; the selftest passes 2,374 arms | `ci_events_*.*` |
| `test_ctrl_memory.py`, pins-only interpreter | rc 0, **123 checks `ok`, 0 failures, `RESULT: PASS`, 44 of 44 mutants caught**. No `ImportError` and no `not graded` | `test_ctrl_memory.*` |
| `run_litex_sims.sh --selftest`, then the aggregate | rc 0, 10 of 10 checks PASS. Then rc 0, **`simulations: 7 passed: 7 failed: 0 skipped: 0`** | `litex_sims_*.*` (the member log is `litex_sims_member_test_ctrl_memory.log`) |
| Control: the SoC child's `_generate_includes` hook removed (`control_no_include_hook.diff`) | rc 1. `the split build exports (rc 1, ImportError: pythondata-software-picolibc ...)`, and **all six SoC mutants `not graded`** | `control_no_include_hook.*` |
| The external round's `probe_load_soc.py`, unmodified | Refused: `reset entry: no load segment carries the first word at the reset address 0x00000000, so rom would hold none there`. `verilog_count` is 0, and no `.v` or `.init` file was written. Exit rc 1 is the probe's own "reproduced" assertion failing, so the defect no longer reproduces. The original first word is still `10003117` | `r607-2_probe_load_soc.*` |
| The external round's `probe_elf_loads.py`, unmodified | Head: `reset-segment-empty REFUSED entry bytes`, `reset-segment-short REFUSED load coverage`, `no-load-segments REFUSED entry bytes`, and every header cut refused as `elf truncated`. At `76605880`, empty and short are both `ACCEPTED`, with first words `[0, 0]` and `[403769859, 0]` | `r607-2_probe_elf_loads.*`, `control_76605880_r607-2_probe_elf_loads.*` |
| Reviewer probe `probe_segments.py`: 10 program-header layouts of the suite's GOOD image (abutting, reversed order, 4-byte hole, overlap, 2-byte reset piece with and without a following piece, paddr +4, every segment 1 byte short, `.data`'s segment dropped) | Head: **10 of 10 as expected**. Accepted layouts give `rom_words` equal to GOOD's; the hole and short layouts are refused by `load coverage`; the missing reset word is refused by `entry bytes`. At `76605880`, **5 unexpected**: the hole, the bare 2-byte piece and the short layout are accepted with wrong words | `probe_segments_head.*`, `control_76605880_probe_segments.*` |
| Four shipped split images, relinked independently by `ctrl_srp_image.py --with-aecp --layout split` at 1x1/8x8 x 1/2 interfaces, then planned with the head's and with `76605880`'s `ctrl_memory.py` (`scripts/plan_images.py`) | All four links rc 0. **Plans are identical** between the two trees. **The rom-word sha256 and the plan JSON equal the author's `rom-digest-after.txt` at all four points.** The rom words equal the toolchain's `objcopy -O binary` at all four. The ELF bytes differ from the author's (different runtime build), and the loaded bytes do not | `fit/*` |
| Doc gates: `docs_check.py`; `check_em_dash.py` against `76605880` and against `e8454e27`; `gen_toc.py --check`; `check_doc_style.py`; `git diff --check 76605880 HEAD` | All rc 0. `docs_check` reports 0 findings. The em-dash checks report 0 over 38 and 0 over 1,501 added lines | `docs_check.*`, `em_dash_*`, `gen_toc_check.*`, `doc_style.*`, `diff_check.*` |
| Trial merge with live `dev` `6bfeeb13`, no checkout | Clean (`git merge-tree` rc 0) | `merge_tree_vs_live_dev.txt` |
| Final clone state | 1,278 tracked files re-hashed with 0 mismatches. Modes match, the index tree equals `783d10c5...` and status is empty. Five gitlinks are unchanged, and the three populated submodules are clean at their gitlinks | `final_clone_verification.txt` |

**Hosted at this exact head** (`hosted_runs_ce10328c.txt`, `hosted_elaborate_excerpt.txt`):

- `rtl-fast` succeeded. Its jobs executed rather than skipped: `changes`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration` (15 min), `firmware-unit` (37 min) and the `rtl-fast` aggregator.
- `elaborate` succeeded. Its log shows the classifier selftest passing, with `gate-read page docs/design/SPLIT_CONTROL_MEMORY.md ... is relevant`. It also shows `run_litex_sims selftest: 10 checks: 10 PASS`, `PASS test_ctrl_memory` and `simulations: 7 passed: 7`.
- In that job, `test_builder.py` reports `ALL GATES PASS EXCEPT 4 NOT RUN`. Those four are runner-environment arms in gates 1b, 11 and 38, none of them in this lane.
- `docs` succeeded: `docs-check`, `wire-accountability` and `docs-check-no-git`.
- `rtl-full` was still in progress at 11:03:40Z. `full-ci-gate`, Yosys shards 0-3 and Verilator shards 0 and 3 had succeeded; Verilator shards 1, 2 and 4 were running.
- `Physical gPTP` was skipped, which is not hardware proof.

## Findings at this head

No BLOCKER, MAJOR or MINOR.

### R606-3-R1 - RESIDUE - Docs - PR #721 body, "Status", second bullet - stale live-dev statement

- **Evidence:** the body, last updated 2026-10-11T10:48:57Z (`receipts/pr-body-as-examined.md`), says "The live `dev` tip is still `ac2c5e77`." `dev` moved to `6bfeeb13` (Merge PR #719, M6) at 10:35:37Z, 13 minutes before that update (`git ls-remote origin refs/heads/dev`).
  - This is wording in a PR body only. It changes no measurement, figure, verdict, test, code or claim about a clause.
  - The merge candidate is the manager's, built against live `dev` in any case. The trial merge is clean.
  - M6 adds no block-RAM tile, so it does not move this PR's ledger figures.
- **Exact fix:** replace that sentence with "The live `dev` tip is now `6bfeeb13` (M6, PR #719); the manager validates the current-dev merge candidate at the merge turn."

### Suggestions (optional; they do not affect the verdict or lens coverage)

- **S-a (Tests):** `mutant_arms` reports the first red check without requiring it to be the mutant's own property.
  - The `BIOS ROM built` and `BIOS SRAM built` mutants are killed by an `AssertionError` raised in the 8x8-stage case (`test_ctrl_memory.log`). LiteX's `add_module` asserts `not hasattr(self, name)` (`litex/gen/fhdl/module.py:88`, called from `milan_soc.py:2751`). It refuses the second module named `rom`/`sram` before the `no BIOS memory` export check is reached (`receipts/mutant_bios_rom_traceback.txt`).
  - That kill is a real product failure and does not depend on the environment, so it is not a defect. Matching each kill to its `PROPERTIES` text would make "caught by its own property" machine-checked.
- **S-b (Robustness):** `load coverage` checks that load bytes cover a section by address. It does not check that the segment's file bytes equal the section's own bytes.
  - A linker never produces such a mismatch; only a hand-edited ELF could disagree. `rom_words` programs the segment bytes, and the linked-probe check against `objcopy -O binary` pins the real path.
- **S-c (Tests):** the link arm derives `objcopy` by replacing `gcc` in the compiler's name (`test_ctrl_memory.py:579`). A compiler whose name lacks `gcc` would run the compiler as `objcopy`. The arm would then fail closed, but without saying why.
- R606-2's S1-S4 remain optional and unchanged. S5 (the runtime's `-fno-stack-protector`) remains the manager's separate Issue; I reproduced it again, and my runtime build used only that flag (`receipts/runtime_tool.diff`).

## Prior public findings on this PR: resolved or retained at this head

| Finding | Status at `ce10328c` | Evidence |
|---|---|---|
| R606-2-F1 BLOCKER: gate-read page unregistered | **Resolved** | `scripts/ci_scope.py:69` adds the page to `GATE_READ_DOCS`, and `:289` adds a classification case. Selftest rc 0 at the head and rc 1 at `76605880`, naming the page. The page classifies `true`. `CI_WORKFLOWS.md:76` says seven pages, which matches the 7 entries, and `:94-97` names `test_ctrl_memory.py` as the reader. The hosted `changes`, `elaborate` and `full-ci-gate` scope steps pass. |
| R606-2-F2 MAJOR: SoC arm needs firmware data packages | **Resolved** | The finder at `test_ctrl_memory.py:629-636` refuses `pythondata_software_*`. The hook at `:650-667` calls LiteX's own `_generate_includes` with `with_bios=False`; LiteX's `builder.py:299-310` shows this omits only `variables.mak`, `output_format.ld` and `regions.ld`. The pins-only interpreter gives PASS, 7 of 7 locally and hosted. `main() staging check removed` is killed by the stage-size control exporting (`rc 0`), and `shipping firmware linked` by `the split build adds no shipping firmware`. No SoC mutant is killed by an `ImportError`. Mutants are graded only against green arms (`:928-938`, `:979-985`); the hook-removed control shows the six SoC mutants `not graded`. Product `milan_soc.py` is unchanged in the delta. `CI_WORKFLOWS.md:1193-1199` and `TESTING.md:711-712` state the real requirement. The published author HANDOFF (R3.3) justifies not provisioning the packages. |
| R606-2-F3 MINOR: partial-placement figure and give-way basis | **Resolved** | `AREA_BUDGET.md:279` and `MARK_II_AREA_PLAN.md:870-871` give `124 + 6 = 130`, 8.5 over 121.5. That re-derives from the table: 87.5-6.5+6-18+53+2 = 124; +6 retained AECP = 130; 130-121.5 = 8.5. `AREA_BUDGET.md:269` and `MARK_II_AREA_PLAN.md:842` name the ruled 56-tile allocation. The other figures recheck: 113 / 8.5, 114.5 / 7, 116 / 5.5, 142 / 131. |
| R606-1-R1 RESIDUE | **Applied verbatim** | `AREA_BUDGET.md:263` and `MARK_II_AREA_PLAN.md:832` match the exact texts. |
| R607-2-F1 MINOR: ROM bytes from unvalidated `p_filesz` | **Resolved** | `_carried` (`ctrl_memory.py:246-252`) is a greedy cover over segments sorted by paddr, and it is correct for abutting, reversed and overlapping segments (`probe_segments_head.log`). `entry bytes` now also requires the reset word in the load bytes (`:272-274`). The new `load coverage` rule (`:84`, `:283-285`) is in `RULES` and in the doc table (`SPLIT_CONTROL_MEMORY.md:77`, `:89-91`). The regressions cover unit ELFs, the genuinely linked probe and the real SoC build (refused before any `.v` or `.init`). The four new mutants are each caught by name. The external round's probes no longer reproduce. The four valid images are byte-identical in plan and rom words. |
| R606-2 S1-S4, S5; R607-1-S3 | Retained, optional or separate | As above. |

## Lens coverage (reviewer-owned ledger)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 assignment 6107088105 items 1-5 against:<br>- `scripts/ci_scope.py:64-75,289`;<br>- `ctrl_memory.py:84,246-252,272-285`;<br>- `test_ctrl_memory.py:629-667,723,739`;<br>- the ledger lines `AREA_BUDGET.md:263,269,279` and `MARK_II_AREA_PLAN.md:832,842,870-871`, re-derived from the table rows;<br>- the R607-2 probes, unmodified;<br>- the four relinked images, whose plan and rom-word digests equal the author's;<br>- the hosted `elaborate`/`rtl-fast` exact-head logs. | R606-3 | `ce10328c3d89d81509e47836fa4a48b22ecdbc20` |
| RTL | CLEAN | - `git diff 76605880..ce10328c -- hdl tb syn` is empty, and all five gitlinks are unchanged;<br>- product `sw/litex/milan_soc.py` (`CtrlMemory`, `add_ctrl_memory:2740-2760`) is unchanged in the delta;<br>- the ROM initialisation path `ctrl_memory.rom_words` is unchanged. Its output at all four shipped points equals `objcopy -O binary` and the author's digests (`fit/plan_head.txt`);<br>- a refused export writes no `.v` or `.init` (`r607-2_probe_load_soc.log`, the SoC arm's `inits == []` check). | R606-3 | `ce10328c3d89d81509e47836fa4a48b22ecdbc20` |
| Robustness | CLEAN | `ctrl_memory.check_map` and `_carried` under:<br>- empty, short, shifted, holed, overlapping, reordered and dropped PT_LOAD layouts (`probe_segments_head.log`, with control at `76605880`);<br>- header cuts and a zero program-header count (`r607-2_probe_elf_loads.log`);<br>- the SoC child in an interpreter lacking the firmware packages;<br>- the hook-removed environment-failure control.<br>Only S-b. | R606-3 | `ce10328c3d89d81509e47836fa4a48b22ecdbc20` |
| Tests | CLEAN | - `sw/litex/test_ctrl_memory.py` at the head: 123 checks, 44 of 44 mutants with kill reasons read one by one (`test_ctrl_memory.log`);<br>- green-arm gating, shown to fail closed by the hook-removed control;<br>- `run_litex_sims.sh` selftest and the 7-of-7 aggregate;<br>- `ci_scope.py --selftest` at the head and at `76605880`;<br>- `ci_events.py --check`/`--selftest`;<br>- the hosted exact-head `elaborate` 7 of 7.<br>Only S-a and S-c. | R606-3 | `ce10328c3d89d81509e47836fa4a48b22ecdbc20` |
| Docs | CLEAN | - `SPLIT_CONTROL_MEMORY.md:62-110` against `RULES` and the test;<br>- `CI_WORKFLOWS.md:76-101,1190-1200` against `GATE_READ_DOCS` and LiteX `builder.py`;<br>- `TESTING.md:697-720`;<br>- the `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` ledger sections;<br>- the `docs_check`, em-dash, TOC, doc-style and `diff --check` gates;<br>- the PR body and REVIEW READY 6107961867.<br>One RESIDUE (R606-3-R1). | R606-3 | `ce10328c3d89d81509e47836fa4a48b22ecdbc20` |

## Real limits

- **Vivado was not re-run.** The as-mapped RAMB figures are the author's single out-of-context run. Their mapping inputs are unchanged here: the plans and rom words of the four images are identical to the author's, and nothing under `syn/` changed.
- **Interpreter.** The CI-equivalent interpreter is a fresh local venv from `litex_pins.txt` with the patch series applied. It is not the hosted runner itself, but the hosted `elaborate` log at this head agrees: 7 of 7, `test_ctrl_memory` PASS.
- **Runtime.** The four-image relink used firmware runtime archives built from a local picolibc and compiler-rt data checkout with `-fno-stack-protector` (S5). The ELF bytes therefore differ from the author's, but the loaded bytes, plans and rom words match the author's exactly.
- **Not run:** `test_builder.py` locally (its hosted `elaborate` run is green), the M8a-2 items (split boot, `check_nvm_capture.py`, `nvm_cosim`, `nvm_capture_cpu`, route), and no parent, PP, gPTP, Yosys or builder bank. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted `rtl-full`** (the exhaustive Verilator shards 1, 2 and 4) was still in progress when observed.
- **Clone.** Ignored build outputs (`__pycache__/`, `configs/generated/*.hex`, `sw/builder/out/`) exist in the clone and are not tracked. Probe trees were archive copies under the unpublished `scratch/`.

## Pending manager duties

- Hosted and act acceptance at this head, including `rtl-full` completing (`verilator-suites`, `yosys-portability`).
- At the merge turn: build and validate the current-dev merge candidate against live `dev` `6bfeeb13` (builder and native banks), publish its receipts, and check post-merge containment. The source base is `e8454e27`. A trial merge is textually clean, and M6 adds no tile.
- Carry R606-3-R1 to the residue checklist.
- Track S5 as its own Issue, per 6105011666.
- Settle the external round at this head before merge. M8a-2 (boot, service checks, route) follows F-INT PR 2.
- No merge authorization is implied by this report.

R606-3 FINISHED
