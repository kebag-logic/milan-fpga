[R882] POSITIVE - exact head 7a92791973ccb57c01597a4b4387afbdbe5444ce

Round R882-2: an independent review, with cleared context, of the composition of issue #950/#954 and PR #961 on the merge-train candidate. Tree `3547b84c6da677de140ea615bcfbc81e011a1382`.

Verdict: the composed tree introduces no defect beyond the reviewed sources. All five lenses were applied at this head. No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and two SUGGESTIONs from the source round R881-1 are retained unchanged, because the composition does not touch them. This round found no new composition finding.

## 1. Scope and composition facts

Receipt: `receipts/composition.txt`.

- **Candidate structure.** The candidate `7a92791` is a merge with two parents:
  - `854bd723`, the live `dev-soft-core` tip and this PR's base branch, which carries the predecessor PRs #945 and #960;
  - `287ca1ee`, the PR source head, tree `e293283d`. Two POSITIVE source reviews were published at that head: R882-1 and R881-1.
- **Clean merge.** The candidate tree equals `git merge-tree --write-tree 854bd723 287ca1ee` exactly. There was no conflict resolution and no hand edit.
- **Fork point.** The source forked at `15168e14`, the flip train's head.
- **Patch identity.** `git diff 15168e14..287ca1ee` and `git diff 854bd723..7a92791` differ only in the `index` lines of two files. The composed patch is byte-for-byte the reviewed patch.
- **Files both sides changed.** As the brief stated, the PR and a predecessor both change exactly two files: `docs/design/SPLIT_CONTROL_MEMORY.md` and `sw/litex/test_ctrl_memory.py`. Each was changed by #960.
  - `SPLIT_CONTROL_MEMORY.md`: #960 changed line 5, the status line, now "the split placement ships since the flip".
  - `test_ctrl_memory.py`: #960 changed lines 615-624. `soc_argv` is now the all-fabric argv, through `with_placement(..., "all-fabric")`.
  - The PR's hunks are elsewhere in both files (lines 139-163, 307, 693-702, 3226-3239; and lines 18 and 343).
  - Of the PR's 19 files, only these two differ from the source head at the candidate.
- **Live `dev`.** Live `dev` `e275d795` (#942) is four commits ahead of the shared ancestor. It changes `AGENTS.md`, `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`, none of which this PR touches. Those commits are not in this candidate; the manager's current-dev candidate covers them.
- **Gitlinks.** All six are equal at the base, the source and the candidate (tsn-c-stack `715589c1`, lwSRP `08ee86e8`, the others as recorded).

Semantic interactions examined beyond the shared files. All come from #960, the flip to the split default with the split VERSION at major 3:

- **(a) Split images.** ENTITY `firmware_version` is now `3.<minor>.<rev>` (`avdecc/aem_descriptors.py`), so the image's AEM bytes and its CRC change.
- **(b) Test expectations.** `sw/firmware/ctrl/test/plat_bus.hpp:36` `kVersion` moved to `0x00030060`, and `test_plat.cpp`'s K1 line moved with it. This PR's new `test_plat_sinks.cpp` includes `plat_bus.hpp`.
- **(c) CPU budget harness.** `tb/verilator/ctrl_service_budget/build.py` gained `split_argv`, and the split config argv changed. Both feed the flash map and the SoC export that the PR's ledger and CPU-budget figures are measured on.
- **(d) Docs and registries.** `docs_inventory.json`, the TOC and anchors, and the em-dash gate's base all changed under #960.

## 2. Evidence produced at this head

Everything ran in this clone, or in a shared clone of the source under the review's scratch directory. Hosts were run with at most 16 jobs.

| Gate / probe | Result | Receipt |
|---|---|---|
| `plat_ledger.py --self-test` at the candidate | PASS, 0 findings, controls 9 of 9 as required. ROM 126,536 / 128,136 / 139,304 / 140,880 B; 45 / 46 / 58.5 / 63 RAMB36, equal to the PR's table at `SPLIT_CONTROL_MEMORY.md:693-702` | `receipts/plat_ledger_head.log` |
| `plat_ledger.py` at the source head | PASS, the same four figures | `receipts/plat_ledger_src.log` |
| Platform image comparison, candidate vs source, all 4 points | DATA-ONLY (see the table below) | `receipts/plat_images_compare.txt`, `plat_images_pl-*.sha256` |
| CPU-budget images: all 16 arms (8 arms at 1x1/1if, 8 at 8x8/1if), built through the harness's own `build.flash_map` and `build.firmware` | The source-head rebuild reproduces all 16 of the author's published `head` hashes (`image-hashes.txt` at `e223b05b`). Each candidate image is DATA-ONLY against its source image | `receipts/budget_images_{head,src}.log`, `budget_images_compare.txt` |
| `test_ctrl_memory.py` at the candidate, pinned LiteX (the gate that reads both sides' edits of the shared file) | rc 0. 223 `ok`, 0 failures, RESULT PASS. This includes the 58.5 entry by name and by symbols, refusal at 59.0, and the all-fabric-based SoC cases | `receipts/test_ctrl_memory_head.log` |
| `test_ctrl_firmware.py --require-rv32` at the candidate, every suite arm | rc 0, `test_ctrl_firmware: PASS`. 88 of 88 arms `[ok]`, including rv32, platrv32, plat (the K1 VERSION line), platboot at if1 and if2, platsinks at 8x8/1if and 1x1/1if (15 of 15 each: S13, S14, T1), and every AECP arm | `receipts/fw_arms_head.log` |
| Docs and registry gates at the candidate (`docs_gates.sh`, base `854bd723`) | 23 commands run, all rc 0, after three gates were rerun with the pinned renderer (details below the table) | `receipts/docs_head/*.log`, `rc.txt` |
| Restore check | HEAD and tree exact. Worktree, index and HEAD agree. Index blobs and modes equal the HEAD tree, and `write-tree` gives `3547b84c`. No untracked or ignored files in the superproject or any submodule; the caches the gates created were removed and are listed | `receipts/restore_check.txt`, `cleaned_ignored.txt` |

Docs and registry gate details:

- **Commands run:** `docs_check`, `check_feature_status`, `gen_toc --check` / `--verify-anchors` / `--selftest`, `check_em_dash --base 854bd723`, `check_doc_paths`, `check_doc_style`, `check_py_idiom`, `check_cpp_idiom`, `docs_inventory --check`, `DOC_MAP.gen --check`, `ci_events --check` / `--selftest`, `measure_naming`, `measure_test_evidence`, `measure_fail_fast`, `check_hygiene`, `check_todo_ownership`, `check_solution_docs`, `generate_ci_evidence_pins --check`, `ci_gate_workflows --check`, `gen_module_matrix --check`.
- **Renderer reruns:** three gates refused under the interpreter without `html5lib`, rc 2 with "renderer not installed". Rerun under the venv that matches `tools/markdown/requirements.txt` exactly, they passed:
  - TOC: 160 pages;
  - anchors: 755 links reproduced;
  - em-dash: 0 findings over 50 added lines;
  - TOC selftest: 1501 of 1501.
- **`ci_events --selftest`:** 2287 items, 5723 arms, PASS.

The image-comparison verdicts, from `compare_images.py`:

| Images | Section table | Symbol table (address, size, kind, name) | Differing bytes |
|---|---|---|---|
| 4 platform points and 16 CPU-budget arms | identical | identical | 6 each: one in `aecp_entity_image` (`0x33`→`0x32`, the `firmware_version` major, "3.96.0" against "2.96.0"), and five in one `lui`+`addi` pair that loads `AECP_ENTITY_CRC` (`ctrl_plat.c:46`, inlined into `main` in the harness images) |

So the composed images have the measured images' layout, symbols and instruction stream. They differ only in an immediate and one descriptor byte. Both come from #960's split major, not from this PR. The PR's ROM figures and its CPU-budget records therefore carry over to the composed tree:

- the plat ledger;
- 1x1/1if AECP 255 us, `load_grade.py:226,279`;
- the `flip_grade` rows.

The cycle counts were measured on images with the same layout and instruction stream, and the RV32 core's timing does not depend on immediate values. This is an argument from image identity, not a re-measurement (see section 5).

## 3. Findings

No new finding at this head. Prior public findings were read only after the independent pass above, and each is accounted for:

**RES-1 (R881-1) RESIDUE, Docs, `sw/firmware/ctrl/plat/README.md:85`. Retained.**
- The line still reads "Input 0 and the CRF input have no context here, and the core still does their waiting change again;". The file is byte-identical to the source head, and the composition does not touch it.
- Exact fix: "Input 0 and the CRF input have no context here: the core makes their waiting change's running check again once applied, and does it again only if it passes (#950);".

**RES-2 (R881-1) RESIDUE, Docs (comment rule of 2026-10-15), `sw/litex/ctrl_memory.py:353`. Retained.** This round found it independently before reading R881-1.
- The new reason-string clause "ROM debt of 2.5 RAMB36 owed to S14" is a new lane-label instance in source text. #746 tracks the older instances at `:273`, `:278`, `:283`, `:287`, `:306`, `:320` and `:347`.
- No figure or test reads it.
- Exact fix: end the clause "...by the same rule: ROM debt of 2.5 RAMB36 owed to the hybrid XIP move (#665 decision D3)".
- Verification: grep the delta's added source lines for lane names. This round's scan (`scratch/added_src.txt`, not published) found only this instance. The `S13`/`S14` strings in `test_plat_sinks.cpp` and `sink_mutants.py` are that file's own test-case numbering (S1 to S12 before them), not lane labels.

**SUG-1 (R881-1) SUGGESTION, Tests, `sw/firmware/ctrl/test/test_plat_sinks.cpp:1226`, `:1264`. Retained, optional.**
- The "keeps its format" assertions request the format already in force, so they cannot fail.
- The defect class is still killed by plant `again-refusal-done-again` in the core test.

**SUG-2 (R881-1) SUGGESTION, Tests/Robustness, `sw/firmware/ctrl/plat/ctrl_plat.c:104`. Retained, optional.**
- `srp.ifs[interface]` is not exercised at two interfaces by T1.
- It is correct by reading, and the acceptance (every output at 1x1/1if and 8x8/1if) is met.

**R882-1** published no findings.

**R881-1's hosted-evidence limit** was the source head's `elaborate-gates-4` `FAIL test_ctrl_memory`, with no log uploaded. It is not a finding. The composed `test_ctrl_memory.py` passes locally with 0 failures (above). Hosted acceptance stays with the manager.

**SUGGESTION (this round, optional), Docs/PR text, `docs/design/SPLIT_CONTROL_MEMORY.md:3226-3239` or the merge-turn record.** Neither the section nor the PR body says that the merged images report `firmware_version` 3.96.0. The CPU-budget re-measure it records ran on `c7cfba76` images reporting 2.96.0, which differ from the merged images only by that digit and the AEM CRC immediate. A one-line note in the manager's merge-turn record would let a later reader match image hashes without redoing this comparison. The section's statements name their heads and are true as written.

## 4. Lens results

```text
[R882] PASS Conformance - receipts/fw_arms_head.log (platsinks 8x8/1if and 1x1/1if 15/15 with S13, S14, T1; aecp-core/aecp-work/aecp-mailbox arms) and sw/firmware/ctrl/aecp/aecp.c:961, aecp_commands.c:140, ctrl_plat.c:104-107 (byte-identical to 287ca1ee) - #950/#954 acceptance re-executed on the composed tree; the only composed change in these images is #960's firmware_version major (IEEE 1722.1-2021 7.2.1 Table 7-2 offset 116), outside #950/#954's clauses (7.4.9, 8.2; Milan v1.2 Table 5.47)
[R882] PASS RTL - receipts/composition.txt (no HDL in the 19-file delta; milan_csr.sv's VERSION_SPLIT_MAJOR is #960's) and receipts/plat_images_compare.txt, budget_images_compare.txt - firmware state machine and widths unchanged from the reviewed source; composed images identical in sections, symbols and instructions except two lui/addi immediates and one descriptor byte
[R882] PASS Robustness - receipts/fw_arms_head.log (platboot if1/if2 52/52 each; platsinks both shapes incl. refusal, rebind and Listener join/leave paths; plat_ledger controls 9/9 in plat_ledger_head.log) - refusal, timeout and ledger-refusal paths hold on the composed tree; no artifact in this lens's scope changed by the composition
[R882] PASS Tests - sw/litex/test_ctrl_memory.py:18,343 against :615-624 (#960) via receipts/test_ctrl_memory_head.log (223 ok, 0 failures); test_plat_sinks.cpp built on plat_bus.hpp:36 kVersion 0x00030060 via fw_arms_head.log (88/88 arms) - the shared test file's two sides compose and pass; the new tests build and pass against #960's test fixtures
[R882] PASS Docs - docs/design/SPLIT_CONTROL_MEMORY.md:5 (#960) with :139-163, :307, :693-702, :3226-3239 (PR); receipts/docs_head/rc.txt (23 gates rc 0 incl. TOC/anchors/em-dash on the pinned renderer, docs_inventory, DOC_MAP) - figures match the composed plat_ledger exactly; the flip's "ships" wording and the PR's "(shipping)" labels agree; RES-1 and RES-2 retained as RESIDUE
```

## 5. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Only through #960's firmware_version digit in the images, outside #950/#954's clauses. The source conformance is otherwise unchanged | Composed platsinks S13/S14/T1 and AECP arms; `aecp.c:961`, `aecp_commands.c:140`, `ctrl_plat.c:104-107`; image byte comparison | R882-2 (composition); source lens R881-1 and R882-1 at `287ca1ee` | `7a92791973ccb57c01597a4b4387afbdbe5444ce` |
| RTL | CLEAN | No: no HDL in the PR, and the firmware sources are byte-identical to the source | `receipts/composition.txt`; 20 image comparisons | R882-2; source lens R881-1 and R882-1 at `287ca1ee` | `7a92791973ccb57c01597a4b4387afbdbe5444ce` |
| Robustness | CLEAN | No | Composed platboot if1/if2, platsinks, plat_ledger controls | R882-2; source lens R881-1 and R882-1 at `287ca1ee` | `7a92791973ccb57c01597a4b4387afbdbe5444ce` |
| Tests | CLEAN | Yes: `test_ctrl_memory.py` (shared file) and `plat_bus.hpp` (under the new test) | `test_ctrl_memory.py` 223 ok; firmware 88/88 arms; `plat_ledger --self-test` | R882-2 | `7a92791973ccb57c01597a4b4387afbdbe5444ce` |
| Docs | CLEAN (RES-1 and RES-2 are RESIDUE) | Yes: `SPLIT_CONTROL_MEMORY.md` (shared file), plus the TOC/anchor/inventory registries | 23 docs and registry gates; figure cross-check against the composed plat_ledger | R882-2 | `7a92791973ccb57c01597a4b4387afbdbe5444ce` |

## 6. Real limits

- **No CPU-budget re-measurement.** I did not re-run the CPU-budget harness (the native model or `record_classes`/`flip_grade` over parts) on the composed images. The carry-over of the 1x1/1if 255 us AECP record and the `flip_grade` rows rests on the image-layout identity above, plus the author's published receipts at `c7cfba76`/`287ca1ee`, whose image hashes this round reproduced.
- **Plants not re-run on the composed tree.** I did not run the `--self-test` planted-defect campaigns, including this PR's 13 plants, `fw_coverage.py --check`, the twin simulation, the boundary gates or the release (all-fabric) image identity check. The plants' anchor files are byte-identical to the source head, where the source reviews ran them. The full arm suite (above) did run.
- **No hosted evidence at this head.** The candidate `7a92791` is not on the remote (the check-runs API reports no commit). The manager owns hosted and act acceptance.
- **No manager bank inferred.** No manager source bank was run or inferred, and no builder or native bank was run. The current-dev candidate, live `dev` `e275d795`, adds #942's process docs. I checked that it does not overlap this PR; it was not composed here.
- **Host load.** The host's load average was 130 to 140 during the run, from other work. Timings in the receipts are not representative.
- **LiteX environment side effect.** While this round's SoC exports ran, files under `$HOME/litex-milan/pythondata-cpu-vexiiriscv` (generated CPU Verilog caches) were written. Other jobs on the host may also have written some of them. They are generator caches, so I left them in place.
- **No physical proof.** Physical calibration was NOT RUN, and field skips are not hardware proof. No hardware acceptance is claimed.

## 7. Pending manager duties

- Hosted and act acceptance at the merged head. That includes the source head's `elaborate-gates-4` `test_ctrl_memory` failure, which R881-1 reported without a log.
- The current-dev merge candidate with the builder and native banks, and its receipts on the PR.
- Carry RES-1 and RES-2 to the residue checklist.
- The executor's reported follow-up: SET_CONFIGURATION and SET_STREAM_INFO also wait without repeating their bound and running checks. That is outside #950's frozen acceptance and wants its own Issue if one is not filed.
- Post-merge bench proof, containment, and Issue/project closure.

## 8. Publishable files

Publishable files are this report and those listed in `MANIFEST.sha256`:

- the scripts `bg.sh`, `docs_gates.sh`, `budget_images.py`, `compare_images.py`, `fw_targeted.py`;
- `receipts/`.

`receipts/fw_targeted_head.partial.txt` records a narrower arm run. I stopped it once the full arm run had passed; the five arms it finished had passed. Home-directory paths in receipts are shown as `$HOME`. `scratch/` is not published.

R882-2 FINISHED
