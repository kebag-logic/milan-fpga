[R606] NEGATIVE - exact head 8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d

# R606-4: internal cleared-context review of PR #721 (issue #640, Mark II lane M8a-1), round 4

- **Head:** `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d`, tree `9c57147d7f2535836e260540372cac0cae7d7049`.
  It is a two-parent merge: first parent `ce10328c` (the round-3 head, POSITIVE in R606-3 and R607-3), second parent dev `c6bd08c6` (M6 #719, lwSRP #718, F-INT #704, M5 #722, gPTP #707 since the lane's last dev merge `ac2c5e77`).
- **Scope authority:** assignment #640 comment 6100371426; ruling 6101485877 (224 KB binding, up to 56 RAMB36 as mapped; M8a-1 = memory map and instantiation behind `--ctrl-mailbox`, fit at four points, measured ledger rows, three planted controls, all-fabric default digest-identical); the R606-4 start comment on #721 (6117944457).
- **Verdict:** NEGATIVE, on one MINOR (F1). The merge itself is exactly the automatic merge plus the documented conflict resolution, and every executed gate passes at this head. But the merged firmware is larger, so the fit figures this PR documents as M8a-1's measurement no longer describe the images its own reproduce commands link at this head.
- **Execution evidence:** the reviewer runs below, at this exact head. No manager source bank ran at this head, and none is claimed or inferred. Physical calibration was not run, and skipped field/physical contexts are not hardware proof.

My independent pass, the verdict and the ledger were written before I read any prior review finding on this PR.

## 1. The merge is mechanical, apart from the one stated resolution

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree ce10328c c6bd08c6` | One conflict, `docs/ARCHITECTURE_HW_SW_SPLIT.md`; the other seven jointly changed files (`milan_soc.py`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `MAILBOX_SPLIT.md`, `CI_WORKFLOWS.md`, `TESTING.md`, `sw/firmware/ctrl/README.md`) auto-merge | `receipts/remerge_mergetree.txt` |
| That automatic tree against the head tree | Only `docs/ARCHITECTURE_HW_SW_SPLIT.md` differs, by exactly the three conflict-marker lines; both sentences are kept (`:192-193`). No other path, mode or gitlink differs | `receipts/remerge_vs_head.diff`, `remerge_vs_head_stat.txt` |
| `git diff c6bd08c6 HEAD` against the lane's own `ac2c5e77..ce10328c` | The same 20 files, 2,017 insertions / 70 deletions. 19 of 20 files are patch-identical (`git patch-id --verbatim`); the 20th is the resolved page, whose lane line is byte-identical with dev's sentence now beside it. Nothing under `hdl/`, `tb/`, `syn/yosys`, `configs/`, `sw/mailbox/` or any gitlink differs from dev | `receipts/patchid_lane_vs_head.txt`, `head_vs_dev_stat.txt` |
| `milan_soc.py` hunks | Dev's only change since `ac2c5e77` is F-INT's, inside `CtrlMailbox` (`:2637-2704`: the publication ports named and left unread). M8a's hunks are the import, `CtrlMemory`/`add_ctrl_memory`, the BIOS-size branch, the flag pairing, the stage check and the shipping-firmware skip. The hunks are disjoint; M2's changes were already in the lane's base `ac2c5e77` | `git diff ac2c5e77 c6bd08c6 -- sw/litex/milan_soc.py` |

The resolved paragraph reads coherently: "It also selects M8a-1's firmware block RAM, with no BIOS." (the `--ctrl-mailbox` switch) followed by F-INT's "The publication block's outputs remain unread until the placement switch selects them."

## 2. What was run at this head

Environment, all disposable under `scratch/`: a CPython 3.12.3 LiteX interpreter holding only `sw/litex/litex_pins.txt` and PyYAML, prepared by `scripts/ci_litex_env.py` and `sw/litex/patches/apply.sh` (5 patches), with **no** `pythondata_software_*` package; a CPython 3.12.3 docs interpreter holding only the docs job's hash-locked and named installs; the pinned RV32 SDK installed fresh and verified by `scripts/ci_rv32_sdk.py`; sv2v v0.0.12 from its pinned release digest; the scoped Verilator 5.050 (`rev v5.050`). `receipts/tool_identity.txt`, `*_venv_freeze.txt`, `sdk_verify.txt`.

| Gate / probe | Result | Receipt |
|---|---|---|
| `scripts/run_litex_sims.sh --selftest`, then the aggregate | rc 0; rc 0, `simulations: 7 passed: 7 failed: 0 skipped: 0` | `receipts/litex/sims_*` |
| `test_ctrl_memory` (aggregate member, pins-only interpreter, RV32 SDK present) | `0 failure(s)`, `RESULT: PASS`; **44 of 44 mutants `[ok  ]`**, each killed by a named check; the link arm ran (probe rom words equal `objcopy -O binary`); the SoC arm exported the split 1x1 SoC through the merged `milan_soc.py`, refused the four planted controls and both lone flags before any Verilog, and found no BIOS ROM/SRAM and no shipping firmware | `receipts/litex/sims/test_ctrl_memory.log` |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: the bench build tree is absent, the same recorded reason as the author's) | `receipts/litex/test_builder_elab.*` |
| The same gate, first run, overlapping the docs job's `test_builder.py` in the same clone | rc 1, `refusing to build: regenerating ... would rewrite tracked generated file(s)`. The two builder runs regenerated shared tracked files concurrently in one tree; CI never shares a checkout between jobs. Rerun alone: rc 0 (above). The clone was clean afterwards. Recorded as a reviewer-environment artifact, not a finding | `receipts/litex/test_builder_elab_run1_concurrent.*` |
| `docs.yml`, every `docs-check` command in order, `wire-accountability`, and `docs-check-no-git` on the tree exported without `.git` (84 + 2 commands) | **86 of 86 rc 0.** Not run: the install steps (done once beforehand), and `act_ci.py --selftest` (outside this review's remit). Highlights: `docs_check` 0 findings over 205 pages; `check_em_dash.py --base c6bd08c6` 0 findings over 318 added lines; `ci_events.py --check` OK, 1,821 contract items, `--selftest` PASS (2,530 arms); `ci_scope.py --selftest` PASS and `docs/design/SPLIT_CONTROL_MEMORY.md` classifies `true`; Python idiom, hygiene, TODO, fail-fast, test-evidence and shell ratchets PASS; `gen_toc.py --check`/`--verify-anchors`, `check_doc_paths.py` OK; `test_builder.py --require-rv32` `ALL GATES PASS EXCEPT 16 NOT RUN` (the LiteX arms that job has no interpreter for); `pp_resource_gate.py check-baseline` PASS; `git diff --check c6bd08c6 HEAD` clean | `receipts/docs/*` |
| All-fabric default: gateware export (no Vivado, no software) of both AX7101 shipping configs at the head and at dev `c6bd08c6` (disposable clone with its own pinned submodules), argv from the end-station builder, compared after normalising only timestamps, output and tree paths and LiteX's hierarchy comment | **1x1: 12 files, 0 differ. 8x8: 12 files, 0 differ.** (Gateware and generated headers only; no BIOS was compiled on either side) | `receipts/exports/digest-default-*`, `scripts/soc_export.py`, `scripts/export_digest.py` |
| Split exports at the head with the head's own linked images (1x1 one interface; 8x8 two interfaces) | Both rc 0. `KL_mbx_wb` carries F-INT's 11 `pub_*_o` ports, unread; `rom`/`sram` are the image's banks (2+4 and 5+5); no BIOS ROM. The SoC build plans 35.5 and **55.0** RAMB36 (budget 56) | `receipts/exports/head-split-*` |
| The four fit points linked by `ctrl_srp_image.py --with-aecp`, split and flat, at `ce10328c` and at the head, same runtime, then `ctrl_memory.py plan` | All 16 links and 8 plans rc 0. **At `ce10328c` my four split ELFs are byte-identical to the author's published ones** (`elf.sha256` in the author's round-3 evidence), so the runtime reproduces exactly. At the head every image is larger (table in F1) | `receipts/fit/*`, `receipts/fit_plans_lane_vs_head.txt`, `fit_head_summary.txt`, `scripts/link_points.sh` |

The runtime archives were built by `sw/firmware/ctrl/test/ctrl_image_runtime.py` with one added flag, `-fno-stack-protector` (`scripts/ctrl_image_runtime_nossp.py`): without it the SDK's default stack protector leaves `__stack_chk_*` unresolved in `libcompiler_rt.a`. This is the separately assigned runtime item (R606-2-S5), not new.

**Hosted at this exact head** (`receipts/hosted_runs_8ab2b539.txt`, inspected 2026-10-12 about 05:50 UTC): `rtl-fast` success, with all six jobs executed (`changes`, `bdd-conformance`, `verilator-lint`, `yosys-elaboration`, `publication-census`, `firmware-unit`); `elaborate` success; `docs` success (`docs-check`, `wire-accountability`, `docs-check-no-git`). `rtl-full` was in progress: `full-ci-gate`, Yosys shards 0-3 and Verilator shards 0, 3 and 4 succeeded, Verilator shards 1 and 2 were running. `Physical gPTP` was skipped. No exhaustive aggregate success is inferred. The manager owns hosted and act acceptance.

## 3. Findings at this head

### R606-4-F1 - MINOR - Conformance, Docs - the documented M8a-1 fit is not the fit of the firmware at this head

- **Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:146-149` (fit table), `:152` (bank fill 96.6 to 99.6 percent), `:155` (planned 54.5; "its image can grow 6 KiB (1.5 tiles) before it is refused"), `:160` (which ROM bank Vivado puts in logic), `:168` ("at most 1.5 tiles"); `docs/design/MARK_II_AREA_PLAN.md:811,822-824,829,836,872`; `docs/design/AREA_BUDGET.md:232,246,259-261,268,283,388`; PR #721 body ("Linked spans", "Block RAM as mapped", "Headroom at the largest point is 1.5 RAMB36 (6 KiB)").
- **Authority:** ruling 6101485877 makes the linked spans, the four-point mapping and "the ledger rows with measured values" M8a-1's acceptance, and binds the 56-RAMB36 budget. `SPLIT_CONTROL_MEMORY.md` section 5 presents its table as "the full F0-F5/F1 composition" without naming the revision it linked, and section 6 gives the commands that reproduce it.
- **Evidence:** those commands, run at this head, give different figures. Dev's F-INT publication writers (`mbx`, `acmp`, `acmp_mbx`, `srp_mbx`, `maap_mbx`) and lwSRP `08ee86e8` (`mrp_mad`) add 1,792 bytes of `.text` and 264 of `.bss` at the largest point (`receipts/fit/object_growth_8x8_i2.txt`):

  | Point | `rom` + `sram` need at `ce10328c` (= documented) | at this head | Planned RAMB36, documented -> head | Bank fill at head |
  |---|---:|---:|---|---|
  | 1x1, one interface (shipping) | 95,032 + 45,520 | 96,624 + 45,776 | 35.0 -> **35.5** (rom banks 64+16+8+4+2 KiB -> 64+32 KiB) | 98.3 / 97.2 % |
  | 1x1, two interfaces | 96,320 + 56,880 | 98,056 + 57,152 | 38.0 -> 38.0 | 99.7 / 99.7 % |
  | 8x8, one interface | 108,680 + 86,080 | 110,344 + 86,336 | 48.5 -> 48.5 | 99.8 / 98.0 % |
  | 8x8, two interfaces (largest) | 110,056 + 112,208 | 111,848 + 112,464 | 54.5 -> **55.0** (rom gains a 2 KiB bank) | 99.3 / 99.8 % |

  The flat spans grow to 142,256 / 155,056 / 196,144 / 223,776 B; the byte floors (35/38/48/55) are unchanged. The real SoC build accepts both merged images it was given (35.5 and 55.0 against 56), so nothing is refused today.
- **Impact:** the page and both ledgers state the split image's margin as 6 KiB (1.5 tiles) at the largest shape; at this head it is 4 KiB of granules (1.0 tile; 5,064 B including bank slack), a third less after one dev merge. The as-mapped 53 tiles, the 231 LUT cells and the logic-bank attribution are Vivado figures of images no longer in the tree (the shipping image no longer has the 512-word ROM bank `:160` names; the largest gains one), so the ledger's 124/113 and 125.5/114.5 rest on an earlier image (planned at this head: 126 and 115, still within 121.5 after the release). A reader of the merged contract cannot reproduce its table from its own recipe.
- **Required outcome:** at the PR's head, the fit section, both ledgers and the PR body either carry the merged firmware's figures (relinked at the head; Vivado re-mapping, or the planned figures with as-mapped marked pending), or name the revision their measurement linked and state, beside it, the head's planned figures and margin (35.5 / 38.0 / 48.5 / 55.0; 1.0 tile, 4 KiB). The `:160` bank attribution and the `:168` and ledger "1.5 tiles" statements follow whichever is chosen.
- **Verification:** `scripts/link_points.sh` (or section 6's commands) at the new head reproduces every documented figure, or the documented figures are explicitly attributed to the revision whose links reproduce them; docs gates stay green.

### R606-4-R1 - RESIDUE - Docs - PR #721 body, Status (retains R606-3-R1 and R607-3-R1)

- **Evidence:** the body still says "REVIEW READY for M8a-1 round 3, head `ce10328c...`" and "The live `dev` tip is still `ac2c5e77`." The head is `8ab2b539` and live dev is `c6bd08c6` (`git ls-remote`). Wording only: no measurement, figure, verdict, test, code or clause claim.
- **Exact fix:** replace that Status bullet's last sentence with "Round 4's head `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` merges dev `c6bd08c6` into `ce10328c`, keeping both sentences in `docs/ARCHITECTURE_HW_SW_SPLIT.md`; the manager validates the current-dev merge candidate at the merge turn." Keep every historical head and gate result as it is.

### R606-4-S1 - SUGGESTION - Tests, Robustness - headroom erosion is seen only when a split image is built

- `test_ctrl_memory.py` grades the plan with synthetic ELFs and a small linked probe, so no standing gate links the largest shape's real image and plans it. F1's 2 KiB loss per dev merge would only surface at a split export, as a `budget` refusal. Optionally, a gate in the firmware or LiteX job could link the largest point with `ctrl_srp_image.py --layout split` and report its planned tiles and margin. Not required for M8a-1; the refusal by name is the documented protection.

### Observation, outside this PR

`MARK_II_AREA_PLAN.md:839` and `AREA_BUDGET.md:271` say "Unpriced ... M6/M7 ... conversions", while dev's M6 section (`MARK_II_AREA_PLAN.md:925-969`, `AREA_BUDGET.md:208`) now records M6 as measured with no block-RAM tile. Both sentences are dev's text at `c6bd08c6` and this PR does not change them, so this is not a finding here; the manager may route it to the plan's owner.

## 4. Prior public findings on this PR, at this head

| Prior ID, severity, lenses | Status at `8ab2b539` | Evidence |
|---|---|---|
| R606-1-F1..F5, R607-1-F1..F3, R607-1-S1, R607-1-S2 (resolved by round 2/3) | **Resolved, preserved** | Their artifacts (`ctrl_memory.py`, `test_ctrl_memory.py`, `milan_soc.py`'s M8a hunks, `ctrl_split.ld`/`_start.S`, `ctrl_srp_image.py`) are patch-identical to `ce10328c`; the 44-mutant suite, the SoC arm, the link arm and the aggregate pass here (section 2) |
| R606-2-F1 BLOCKER (gate-read page) | **Resolved, preserved** | `scripts/ci_scope.py:69` registers the page; `ci_scope.py --selftest` PASS and the page classifies `true`, in both campaigns; `CI_WORKFLOWS.md` "Seven pages" matches 7 `GATE_READ_DOCS` entries after the merge |
| R606-2-F2 MAJOR (SoC arm and firmware data packages) | **Resolved, preserved** | Pins-only interpreter with no `pythondata_software_*`: aggregate 7/7, 44/44 |
| R606-2-F3 MINOR, R606-1-R1 RESIDUE (ledger texts) | **Resolved, preserved** | `AREA_BUDGET.md:267,273,283` and `MARK_II_AREA_PLAN.md:834,844,872` unchanged by the merge and arithmetically consistent with the rows (124, 113, 114.5, 116, 130, 142/131 recomputed) |
| R607-2-F1 MINOR (load coverage) | **Resolved, preserved** | `load coverage` and `entry bytes` arms and their mutants pass at this head; the SoC build refuses the emptied reset segment before any Verilog |
| R607-1-R1 RESIDUE ("three mapped tiles versus 1.5 planned / 6 KiB") | **Superseded by F1** | The sentence it fixed (`SPLIT_CONTROL_MEMORY.md:155`) is now numerically stale at this head |
| R606-3-R1 and R607-3-R1 RESIDUE (PR body, live dev tip) | **Retained** as R606-4-R1 | Body unchanged; exact fix updated for this head |
| R606-2-S1..S4, R606-3-S-a, S-b, S-c (SUGGESTION) | **Retained, optional, unchanged** | Their artifacts are patch-identical to `ce10328c` |
| R606-2-S5 (runtime stack protector, separate assignment) | **Retained, separate** | Reproduced again here (section 2) |

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Ruling 6101485877 items against: the four points linked and planned at this head and at `ce10328c` (`receipts/fit/*`); the real SoC build's plan of the merged images (`receipts/exports/head-split-*`); `SPLIT_CONTROL_MEMORY.md:140-168`; ledger rows `MARK_II_AREA_PLAN.md:805-842`, `AREA_BUDGET.md:229-283`; default digest at this head against dev (12+12 files, 0 differ); the three planted controls and the reset-segment control through `main()` (`test_ctrl_memory.log:69-83`) | R606-4 | `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` |
| RTL | CLEAN | `milan_soc.py` merged hunks (`CtrlMailbox` `:2637-2704` with F-INT's ports; `CtrlMemory` `:2729`, `add_ctrl_memory` `:2759-2776`) shown disjoint by `merge-tree`; split exports at this head: `KL_mbx_wb` with 11 unread `pub_*_o` ports, banked `rom`/`sram` with `err` hole decode, no BIOS ROM (`receipts/exports/head-split-*`); default exports equal dev's; `git diff c6bd08c6 HEAD -- hdl tb syn/yosys configs sw/mailbox` empty and gitlinks equal; `test_builder.py --require-elaboration` PASS | R606-4 | `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` |
| Robustness | CLEAN | Flag pairing and planted refusals through the merged `main()` (`test_ctrl_memory.log:70-75`); merged largest image accepted at 55.0 against the 56 boundary and the 56.0/56.5 boundary arms passing; no other caller of `--ctrl-mailbox` in the tree that the pairing rule would break (search of `*.py`, `*.sh`, `*.yml`, `*.yaml`, `Makefile`, `*.tcl`); all-fabric default unchanged | R606-4 | `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` |
| Tests | CLEAN | `test_ctrl_memory.py` at this head: 0 failures, 44/44 mutants each with its named kill; aggregate selftest and 7/7; elaboration gate and docs-job builder gate; `ci_scope`, `ci_events`, Python-idiom and test-evidence ratchets; the test's simulated sram banks (64, 32, 8, 4, 2 KiB) still equal the merged largest image's. Only S1 (optional) | R606-4 | `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` |
| Docs | UNCLEAN (F1) | Conflict resolution `ARCHITECTURE_HW_SW_SPLIT.md:189-195`; lane paragraphs in `MAILBOX_SPLIT.md:1136-1141`, `CI_WORKFLOWS.md:78-99,1223-1234`, `TESTING.md:700-722`, `sw/firmware/ctrl/README.md:367-372` read in merged context; `SPLIT_CONTROL_MEMORY.md` section 5 against the head's links; both ledgers; PR body; 86 docs-job commands rc 0. R1 is RESIDUE and does not leave the lens unclean | R606-4 | `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` |

## 6. Real limits and pending manager duties

- No Vivado run: the as-mapped figures at this head are unknown; F1's planned figures are `ctrl_memory.plan`'s, and the split exports were not synthesised.
- No full parent, processor, gPTP, Yosys or builder bank, no `run_all_suites.sh`, no firmware host suites or coverage ratchet, and no `act` run. `rtl-fast` (including `firmware-unit` and `publication-census`) executed and succeeded on this exact head; `rtl-full` was still running when inspected.
- The default-export digest compares gateware and generated headers without a compiled BIOS (the pins-only interpreter cannot compile it); the BIOS sources are not in this PR's delta.
- The runtime used for the links adds `-fno-stack-protector` to the repository's runtime script (R606-2-S5); at `ce10328c` it reproduces the author's four ELFs byte for byte.
- M8a-2 (boot, service checks, integrated route) remains out of scope.
- **Manager:** build and gate the current-dev merge candidate at the merge turn (source base `c6bd08c6`, live dev `c6bd08c6` at review time) and link its receipts; own hosted and act acceptance (`rtl-full` pending at inspection); carry R606-4-R1 to the residue checklist; route the outside-PR observation if wanted.

## 7. Clone state after the probes

The clone is at the exact head: 1,301 tracked files re-hashed with 0 mismatches and correct modes, the index tree equals `9c57147d...`, status is empty, no assume-unchanged or skip-worktree flag, the five gitlinks are unchanged, and the four populated submodules are clean at their gitlinks (`third_party/lwSRP` was initialised at its pin for the image links). `receipts/restore_verify.txt`.

Paths in receipts are written as `$PACKET` (this packet), `$CLONE` (the reviewed clone) and `$HOME`. Every published receipt is listed in `MANIFEST.sha256`.

R606-4 FINISHED
