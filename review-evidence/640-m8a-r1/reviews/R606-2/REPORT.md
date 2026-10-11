[R606] NEGATIVE - exact head 76605880a20005cbc2acad1b23ba2ccebde64ca8

# R606-2: internal cleared-context review of PR #721 (issue #640, Mark II lane M8a-1, plan L11a)

- **Head:** `76605880a20005cbc2acad1b23ba2ccebde64ca8`, tree `0d5e91af9d99c5c2f30e5c4aa1723f463dbe303d`.
  - Round 2 adds `be431eec`, `516d7fb8` and `76605880` on `08b90b68`.
  - `08b90b68` is round 1 (`5d532e9d`) plus a merge of dev `ac2c5e77`.
  - The lane's own diff is therefore `ac2c5e77..76605880`: 19 files.
- **Scope authority:**
  - assignment #640 comment 6100371426;
  - ruling 6101485877, which defines M8a-1: the memory map and instantiation behind `--ctrl-mailbox`, out-of-context mapping at four points under items 1-3, linked spans, measured ledger rows, three planted controls, and an all-fabric default that stays digest-identical;
  - round-2 assignment 6105011666;
  - owner decisions 5991591637 (D4) and 6081706413 (224 KB).
  - Boot, service checks and the route belong to M8a-2.
- **Verdict:** NEGATIVE. I applied all five lenses.
  - One BLOCKER and one MAJOR, both in the test wiring the round added. One MINOR in the ledger text.
  - The code under review (the memory map, the bank plan, `CtrlMemory`, the link script and reset entry, and the SoC hookup) is correct at this head. RTL and Robustness are covered clean.
- **Execution evidence:**
  - Source-head execution evidence is the author's published gate receipts plus the reviewer runs below.
  - No manager source bank ran at this head, and none is claimed or inferred.
  - Hosted contexts at this head are reported as observed. The manager owns hosted and act acceptance.

## What was reproduced at this head

Receipts are under `receipts/` and scripts under `scripts/`. `scripts/COMMANDS.md` gives the commands.

| Claim | Reviewer evidence | Result |
|---|---|---|
| Four linked split images | The pinned SDK, installed fresh and verified (archive sha256 `d42680e9...`). `ctrl_srp_image.py --with-aecp --layout split` and `--layout flat` at four points (`fit_reproduction.txt`, `elf_reviewer.sha256`) | All four split ELFs are **byte-identical** to the author's `evidence-m81/elf.sha256`. Needs are 95,032+45,520, 96,320+56,880, 108,680+86,080 and 110,056+112,208 B. Planned tiles are 35.0 / 38.0 / 48.5 / 54.5. Flat spans are 140,400 / 153,056 / 194,224 / 221,728, so the byte floors are 35 / 38 / 48 / 55. |
| Link script and reset entry on the real images | `readelf` and `nm` of the largest image (`fit_reproduction.txt`) | Entry `0x0` with `_start` first. `.data` LMA is word-aligned (the 1x1 LMAs are `0x17300` and `0x17808`). `_fbss` is 16-aligned and `_ebss` 4-aligned. `_stack_top` equals the sram need. There is no `__global_pointer$` and no orphan section. |
| As mapped | The author's `ctrl_memory_ooc.tsv` and `s8i2_rom_utilization.rpt`, recomputed | 33/2, 37/1, 46/2 and 52/2 RAMB36/RAMB18, i.e. 34.0 / 37.5 / 47.0 / 53.0 tiles. LUT cells are 212 / 89 / 307 / 328. `s8i2_rom` LUT primitives are 118+59+40+9+4+1 = 231, and its Slice LUTs are 220. Vivado was not re-run. |
| Ledger arithmetic | Hand check against the table rows | 87.5-6.5+6-18+53+2 = 124, then 113 after the -11 release, which is 8.5 under 121.5. With every bank in block RAM: 125.5 and 114.5. At 56 tiles: 116, leaving 5.5. Keeping the BIOS: 142 and 131. All correct, except the stale lines in F3. |
| All-fabric default is digest-identical | AX7101 1x1 and 8x8 shipping argv, exported without Vivado from a dev `ac2c5e77` tree and from the head, with `PYTHONHASHSEED=0` (`scripts/export_soc.py`, `scripts/compare_exports.py`, `digest-default-*.txt`, `exports_summary.txt`) | 22 files each side. 21 are equal after removing paths, dates and the comment-only hierarchy block. The 22nd, `litex.log`, differs only in run stamps, stdout interleaving and hierarchy order. Both sides use the CPU netlist `VexiiRiscvLitex_f5f08b17...`. |
| Split export: no BIOS, banks, CSR map | Head split exports at 1x1 (s1i1 image) and 8x8 (s8i2 image) against base `--ctrl-mailbox` exports (`digest-basembx-vs-headsplit-*.txt`, `exports_summary.txt`) | `csr.csv` and `csr.json` differ only in `rom` (131,072 to 229,376) and `sram` (8,192 to 229,376). The Verilog holds `rom_bank*` and `sram_bank*` exactly as planned, with no BIOS `rom`/`sram`. `libmilan_baremetal` is not linked. The region decode is `adr[29:16]` (256 KiB window). Both shapes use one CPU netlist, `dd10544c...`. |
| Lane test, with the firmware data packages importable | `test_ctrl_memory.py` under the pinned SDK (`test_ctrl_memory_with_picolibc.log`) | 109 checks `ok`, 0 failures, `RESULT: PASS`. All 40 mutants are caught. The twelve R607-1 mutants and R606-1's `main()`-stage mutant are each caught by a named failure. |
| Lane test in the pinned elaborate interpreter | Same test, interpreter from `litex_pins.txt` only (`test_ctrl_memory_no_picolibc_local_cc.log`, `sims_ci_env_test_ctrl_memory.log`, `env_litex_interpreter.txt`) | **FAIL**: `the split build exports (rc 1, ImportError: pythondata-software-picolibc module not installed!...)` (finding F2). |
| LiteX aggregate (pinned Verilator 5.050) | `run_litex_sims.sh` in both interpreters (`run_litex_sims_*.log`) | Without the packages: **7 run, 6 passed, 1 failed (`test_ctrl_memory`)**, rc 1. With them: 7/7, rc 0. |
| Change classifier | `scripts/ci_scope.py --selftest` at head and at `ac2c5e77` (`ci_scope_selftest_*.log`, `ci_scope_classification.txt`) | Head **rc 1**: `FAIL gate-read page docs/design/SPLIT_CONTROL_MEMORY.md (named at sw/litex/test_ctrl_memory.py:81) is relevant`. Base rc 0. A change to that page alone classifies as `false` (finding F1). |
| Hosted, exact head | Check runs and job logs (`hosted_checks_76605880.tsv`, `hosted_excerpts_76605880.txt`) | `changes`, `elaborate` and `full-ci-gate` **fail** in their scope step on the same classifier line. `rtl-fast`, `verilator-suites` and `yosys-portability` fail in their aggregators: `CHANGES_RESULT: failure`, and "found 0" shard directories. Every Verilator and Yosys shard, `verilator-lint`, `yosys-elaboration` and `firmware-unit` is **skipped**. So **no RTL, Verilator, Yosys or LiteX gate executed on this head**. `bdd-conformance`, `wire-accountability` and `docs-check-no-git` succeeded. `docs-check` was still in progress when recorded. `Physical gPTP` was skipped, which is not hardware proof. |
| ELF edge cases | `scripts/probe_elf_edges.py` (`probe_elf_edges.log`) | See S1 and S2. |

## Findings

### R606-2-F1 - BLOCKER - Tests, Docs, Conformance - `scripts/ci_scope.py:64-71` (`GATE_READ_DOCS`) against `sw/litex/test_ctrl_memory.py:81`, `:824-836` - the new gate-read page is not registered, so the change classifier fails on every head

- **Authority/evidence:**
  - Round 2 made `docs/design/SPLIT_CONTROL_MEMORY.md` section 3 a gate input: `registry_arms` requires its rule table to equal `ctrl_memory.RULES`.
  - `docs/testing/CI_WORKFLOWS.md:60-66` and `:93-97` require a page that a gated module reads to stay RTL-relevant. `scripts/ci_scope.py --selftest` derives that list and "refuses a table that differs from it".
  - `GATE_READ_DOCS` does not list the page, and the policy page's list of gate-read pages does not name it either.
  - Local result (`ci_scope_selftest_head.log`): rc 1, `selftest: 1 FAILURE(S)`. At `ac2c5e77` it is rc 0.
  - The same failure is the first failing step of the hosted `changes`, `elaborate` and `full-ci-gate` jobs at this head (`hosted_excerpts_76605880.txt`). `rtl-fast`, `verilator-suites` and `yosys-portability` fail in turn, and no RTL gate ran.
  - Semantically, `ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` prints `false`. An edit to that table alone would therefore skip `elaborate`, the only job that runs the test reading it. `docs-check` does not run `test_ctrl_memory`.
  - The author's round-2 gate table does not list `ci_scope.py --selftest`.
- **Impact:**
  - The exact head has no successful `rtl-fast` and no executed exhaustive evidence, which AGENTS.md section 7 requires.
  - Merged as is, the classifier self-test would fail for every later pull request.
  - The rule table could drift from `RULES` through a docs-only change that no gate runs.
- **Required outcome:**
  - `scripts/ci_scope.py --selftest` passes at the head.
  - A change touching only `SPLIT_CONTROL_MEMORY.md` classifies as RTL-relevant (or its reader runs in `docs-check`).
  - `CI_WORKFLOWS.md`'s list of gate-read pages names this reader.
- **Verification:**
  - `python3 -I scripts/ci_scope.py --selftest` returns rc 0.
  - `python3 -I scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` prints `true`.
  - The hosted `changes` and `elaborate` scope steps pass on the new head.

### R606-2-F2 - MAJOR - Tests, Docs - `sw/litex/test_ctrl_memory.py:582-626` (`soc_child`, `soc_case`), `:629-655` (`split_export`); `docs/testing/CI_WORKFLOWS.md:1184-1190` - the new SoC arm cannot pass in the interpreter the hosted job installs

- **Authority/evidence:**
  - The SoC arm runs `milan_soc.main()` with LiteX's real `Builder.build`. For any CPU SoC, `Builder._generate_includes` resolves `get_data_mod("software", "picolibc")` and `compiler_rt`, even with `--no-compile-software`.
  - `elaborate.yml:160-164` installs only PyYAML and `sw/litex/litex_pins.txt`. LiteX's own `Requires-Dist` does not pull those packages.
  - The repository already says so: `sw/builder/test_shipping_clock_constraints.py:20-27` describes "LiteX's firmware data packages, which the pinned elaborate install lacks". That test overrides `_generate_includes(with_bios=False)` for exactly this reason (`:65-73`).
  - In a `litex_pins.txt`-only interpreter (`env_litex_interpreter.txt`) with the pinned SDK and Verilator 5.050:
    - `test_ctrl_memory` fails with `the split build exports (rc 1, ImportError: pythondata-software-picolibc module not installed! ...)`;
    - the aggregate reports `simulations: 7 passed: 6 failed: 1`, rc 1 (`run_litex_sims_ci_env.log`, `sims_ci_env_test_ctrl_memory.log`).
  - In that interpreter two of the eight SoC mutants are "caught" only by the same ImportError, not by the property they target: `main() staging check removed` and `shipping firmware linked` (`test_ctrl_memory_no_picolibc_local_cc.log`).
  - With the packages importable, the same test passes and every SoC mutant is caught by its property (`test_ctrl_memory_with_picolibc.log`, `run_litex_sims_with_picolibc.log`). So the author's 7 of 7 is environment-dependent.
  - The hosted job cannot show this yet, because F1 stops it first.
  - The new `CI_WORKFLOWS.md` paragraph says the arm needs "the PyYAML this job installs" and omits this dependency.
- **Impact:** once F1 is fixed, the hosted `elaborate` LiteX aggregate goes red at this code. Any interpreter that does have the packages reports kills of the round-2 item 2 controls that a CI interpreter cannot reproduce.
- **Required outcome:**
  - The SoC arm passes, with its mutants killed by their named property, in the interpreter `elaborate.yml` installs. That is achieved either by not resolving the firmware data packages (as the sibling test does) or by provisioning them in the job and the pins.
  - `CI_WORKFLOWS.md` states the arm's real requirements.
- **Verification:**
  - In a `litex_pins.txt`-only interpreter, `test_ctrl_memory.py` prints `RESULT: PASS`, and `run_litex_sims.sh` gives 7/7.
  - The `main() staging check removed` and `shipping firmware linked` mutants are caught by the stage-size and no-shipping-firmware checks, not by an ImportError.

### R606-2-F3 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:842`, `:869-871`; `docs/design/AREA_BUDGET.md:269`, `:278-280` - the partial-placement figure and the "above 50 firmware tiles" basis still carry the superseded ledger

- **Authority/evidence:**
  - "With the same 50-tile hold, the pre-release estimate becomes 126.5. That is five tiles over the ceiling" (plan) and "Its same 50-tile hold gives 126.5" (budget) are the old `120.5 + 6`.
  - 120.5 used the estimated -18.5 reuse row and the 50-tile allocation. This PR replaced those rows with the measured -18 and the ruled, measured +53 (limit 56).
  - From the PR's own rows, the partial-placement pre-release total is 124 + 6 = **130**: 8.5 over the ceiling at the measured 53. Even at a hypothetical 50-tile hold it is 127, not 126.5.
  - "What gives way above 50 firmware tiles" (plan `:842`, budget `:269`) still names the superseded 50-tile basis. The ruled limit is 56 as mapped, and the measured allocation is 53.
  - This is the same class as R606-1-F4 and R607-1-F2 (fixed for the 56-tile sentences). These lines were not covered by those findings.
- **Impact:** the authoritative ledger understates the partial placement's overrun by 3.5 tiles. The next lane that prices M0s's partial route starts from the wrong figure.
- **Required outcome:** the partial-placement sentence in both documents is derived from the current rows (or explicitly labelled with the basis it uses), and the give-way heading names the ruled basis.
- **Verification:** each figure re-derives from the ledger table rows in the same document, and the doc gates stay green.

## Residue (wording only; the manager carries these; they do not affect the verdict or lens coverage)

- **R606-1-R1 (retained, unchanged at this head):** `docs/design/AREA_BUDGET.md:263` and `docs/design/MARK_II_AREA_PLAN.md:832` call the 124-tile total "measured", but it includes M2's +2 allowance, which the plan records as unused. Exact fix:
  - AREA_BUDGET: "With M2's unused +2 allowance, the ledger is 2.5 tiles over 121.5 before conditional reclamation."
  - plan: "Before the conditional release, with M2's unused +2 allowance, the total is 2.5 tiles over 121.5."

## Suggestions (optional)

- **S1 (Robustness):** `check_map` accepts a loaded section that runs in `sram` outside the `[_fdata, _edata)` range the reset entry copies. A writable orphan section would never be initialised (`probe_elf_edges.log`: `loaded sram section outside the startup copy: ACCEPTED`). The same holds for NOBITS outside `[_fbss, _ebss)`. The shipped images have no such section. Checking those ranges against the linker symbols would close the gap.
- **S2 (Robustness):** `read_elf` still raises unnamed errors for some malformed inputs that are not truncations: `e_shstrndx` or a symtab `sh_link` out of range (IndexError), and a symtab `sh_entsize` of 0 (ValueError). The build stops (fail-closed), but without a rule name.
- **S3 (retained from R606-1-S1):** `ctrl_split_start.S` sets no `mtvec`. Before the firmware installs one, a trap (for example the hole's `err`) goes to the reset default.
- **S4 (retained from R606-1-S2):** `CtrlMemory` slices `words[first:first + depth]`, so `rom_words` longer than the planned banks would be truncated silently. An assertion in `add_ctrl_memory` would close that.
- **S5 (retained, pre-existing, the manager's separate Issue per 6105011666):** `ctrl_image_runtime.py` needs `-fno-stack-protector` with the pinned SDK. Without it, `__umoddi3` needs `__stack_chk_guard`. I reproduced this again; my runtime used that flag only, and the images match the author's bytes.

## Prior public findings on this PR: resolved or retained at this head

| Finding | Status at `76605880` | Evidence |
|---|---|---|
| R606-1-F1 writable data in `rom` | Resolved | Rule `writable in rom` (`ctrl_memory.py:85-86,271-273`). The link-script plant `} > rom` is refused by that rule, and the mutant is caught (`test_ctrl_memory_with_picolibc.log`). |
| R606-1-F2 hole graded at one address | Resolved | 47 addresses up to word `0xFFFF` in both regions, at the largest sram banks. 215 alias cells unchanged. Back-to-back after err. The `decode one bit short`, `hole compares one bit short`, `hole starts a word late` and `err held a second cycle` mutants are caught. |
| R606-1-F3 SoC hookup untested | Resolved in substance; superseded by R606-2-F2 | The SoC arm exists and catches the `main()`-stage mutant, but only where the firmware data packages import. |
| R606-1-F4 / R607-1-F2 56-tile sentences, `AREA_BUDGET.md:382` | Resolved | 116 and 5.5 in both documents (`MARK_II_AREA_PLAN.md:861-862`, `AREA_BUDGET.md:265`). `:382` states the ruled limit. The lane row names 56. The same class remains open elsewhere as R606-2-F3. |
| R606-1-F5 231-LUT attribution | Resolved | `SPLIT_CONTROL_MEMORY.md:157-163` and `MARK_II_AREA_PLAN.md:821` give the `rom` region, decode and multiplexer included, in LUT cells, and 220 Slice LUTs. Matches the TSV and report. |
| R606-1-R1 "measured" 2.5 over | Retained as residue | Text unchanged. |
| R606-1-R2 PR body stale | Resolved | The body names `76605880`, `08b90b68` and the dev merge, and says 7 of 7. |
| R607-1-F1 five surviving mutants | Resolved (with the packages importable) | All twelve are caught by named failures. Boundary 56.0 accepted and 56.5 refused. |
| R607-1-F3 PR body | Resolved | As R606-1-R2. |
| R607-1-R1, R607-1-R2 | Resolved | Exact texts at `SPLIT_CONTROL_MEMORY.md:150`, `:139`, `:157-158` and `MARK_II_AREA_PLAN.md:821`. |
| R607-1-S1 | Addressed | By the SoC arm; see R606-2-F2. |
| R607-1-S2 truncated ELF | Addressed for truncation | Rule `elf truncated`. Other malformed indices remain unnamed (S2). |
| R607-1-S3 runtime stack protector | Retained, pre-existing | S5. |
| R606-1-S1, R606-1-S2 | Retained | S3, S4. |
| R606-1-S3 | Addressed for truncation | See S2. |

## Lens coverage (reviewer-owned ledger)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling 6101485877 items 1-4 and M8a-1 deliverables, and round-2 assignment 6105011666 items 1-4, against:<br>- `ctrl_memory.py:47-52,74-94,126-127,253-292`;<br>- `milan_soc.py` CtrlMemory/add_ctrl_memory, `MilanSoC` BIOS suppression, `main()` pairing and staging;<br>- four byte-identical relinks (`fit_reproduction.txt`);<br>- the TSV and utilization reports;<br>- ledger rows (`MARK_II_AREA_PLAN.md:805-811`, `AREA_BUDGET.md:238-244`);<br>- the default digest at both shapes;<br>- the split export and CSR map;<br>- the three planted controls through `main()`;<br>- `SPLIT_CONTROL_MEMORY.md` §4.<br>The issue acceptance "every ... check passes" fails on the classifier self-test (F1). | R606-2 | `76605880a20005cbc2acad1b23ba2ccebde64ca8` |
| RTL | CLEAN | - `milan_soc.py` `CtrlMemory` (`low` = 16; bank select `a[s:low] == f >> s` with largest-first alignment; hole `a[:low] >= first`; one-cycle err with reset);<br>- exported `alinx_ax7101.v`: region `adr[29:16]`, bank memories as planned, hole err register reset (`exports_summary.txt`);<br>- CPU regions 229,376 B rx/rwx and one netlist for both shapes;<br>- `ctrl_split.ld` and `ctrl_split_start.S` against the real images' LMA and symbol alignment;<br>- `pp_mem_gate` (`milan_soc.py:2387-2411`) for the DDR3 statement.<br>Timing is M8a-2, as ruled. | R606-2 | `76605880a20005cbc2acad1b23ba2ccebde64ca8` |
| Robustness | CLEAN | - `ctrl_memory.read_elf` and `check_map`: malformed, truncated and foreign ELF, entry, regions, overlaps, NOBITS/writable in rom, budget boundary 56.0/56.5, stage symbol and size (test arms plus `probe_elf_edges.log`);<br>- feature-off default digest;<br>- flag pairing both ways;<br>- CPU-reset re-entry (copy and clear from linker symbols);<br>- configuration by shape (1x1/8x8 staging).<br>Only SUGGESTIONs S1 and S2. | R606-2 | `76605880a20005cbc2acad1b23ba2ccebde64ca8` |
| Tests | UNCLEAN (F1, F2) | - `sw/litex/test_ctrl_memory.py`, all seven arms and 40 mutants, in two interpreters;<br>- `scripts/run_litex_sims.sh` aggregate in both (pinned Verilator 5.050);<br>- `scripts/ci_scope.py --selftest` at head and base;<br>- hosted exact-head check runs and logs. | R606-2 | `76605880a20005cbc2acad1b23ba2ccebde64ca8` |
| Docs | UNCLEAN (F1, F2, F3) | - `docs/design/SPLIT_CONTROL_MEMORY.md` (all sections, against the exports, the TSV and the test);<br>- `MARK_II_AREA_PLAN.md:39,432,596,766-880,1046`;<br>- `AREA_BUDGET.md:218-285,379-386`;<br>- `MAILBOX_SPLIT.md:825-830`;<br>- `CI_WORKFLOWS.md:60-125,1181-1191`;<br>- `TESTING.md:697-714`;<br>- `LITEX_SOC.md`, `ARCHITECTURE_HW_SW_SPLIT.md:181`, `docs/README.md:79`, `sw/firmware/ctrl/README.md:354-359`;<br>- the PR body. | R606-2 | `76605880a20005cbc2acad1b23ba2ccebde64ca8` |

## Real limits

- **Vivado was not re-run.** The as-mapped RAMB36/RAMB18/LUT figures are the author's single out-of-context run. I re-derived their arithmetic and consistency from the published TSV and reports, and showed that the mapped inputs (the ELFs) are byte-identical.
- **CI interpreter.** The CI-equivalent interpreter is a copy of a `litex_pins.txt` install, with the repository's patch series re-applied. It is not the hosted runner itself. Its package set and the workflow's install step are recorded in `env_litex_interpreter.txt`. The hosted outcome of F2 is not observable at this head, because F1 stops the job first.
- **Firmware data packages.** For the passing runs, they came from a local checkout through `PYTHONPATH`, not from a pinned install.
- **Runtime build.** It used `-fno-stack-protector` (S5). The resulting ELFs match the author's bytes.
- **Not run:** M8a-2 items (the split boot, `check_nvm_capture.py`, `nvm_cosim`, `nvm_capture_cpu`, the route), and no parent, PP, gPTP, Yosys or builder bank. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone state.** `third_party/lwSRP` was initialised at its recorded gitlink. After all probes, all 1,278 tracked files were re-hashed against the index with 0 mismatches. The index tree equals `0d5e91af...`, `git status --porcelain` is empty, and the five gitlinks are unchanged (`final_tree_verification.txt`).

## Pending manager duties

- Hosted and act acceptance on the next head. At this head no RTL gate executed (F1).
- At the merge turn: validate the current-dev merge candidate (builder and native banks) and publish its receipts.
- Carry R606-1-R1 to the residue checklist.
- Track S5 as its own Issue, per 6105011666.
- Coordinate with F-INT PR 2 (#704):
  - `--ctrl-mailbox` now requires `--ctrl-firmware`;
  - the split build links no shipping firmware;
  - `CtrlMemory` sits on the CPU bus path that M8a-2's route measures.
- Check the external round, and re-review F1-F3 at the new head.

R606-2 FINISHED
