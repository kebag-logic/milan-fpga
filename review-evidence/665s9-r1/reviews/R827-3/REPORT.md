[R827] NEGATIVE - exact head a69fc0f597355a0a200ec5be6bb134b897e97ff5

Round R827-3, internal independent review of issue #870 / PR #889. This round reviews the composition only: dev-soft-core merge-train candidate `7a4871d5dbd386f39644734d2c3d7e437a21abf3` (tree `63b2a160`). Its first parent is `e282ecd2`, whose tree `466d464a` equals dev-soft-core `8b1bdfaf` after S7 (#874) and #823 (#880). Its second parent is the PR head `a69fc0f5` (tree `bc5cc0e0`), and the merge base is `1d6bf555`.

The verdict is NEGATIVE on one MINOR, F1. Every intent of both sides survives the composition apart from one: builder gate 23o, which is S9's check of the split recipe, does not hold the new builder artifact that #823 adds. Each other check, gate and lens is clean, with evidence below.

## 1. Composition identity

Receipt: `receipts/composition_identity.txt`.

- The candidate's tree is exactly the clean three-way merge of dev-soft-core `8b1bdfaf` and `a69fc0f5`. `git merge-tree --write-tree` gives `63b2a160` with exit 0, so the candidate has no conflict resolution and no manual edit.
- Each side's hunks were compared as bodies, with raw `diff-tree -U0` and headers stripped. For all seven files both sides changed, S9's hunks (base to head) equal the candidate's hunks against dev-soft-core, and #823/S7's hunks equal the candidate's hunks against the head. No hunk was lost and none was duplicated.
- Every file only one side changed has that side's blob at the candidate.
- All six gitlinks are the same at the head, at dev-soft-core and at the candidate.

## 2. Findings

### F1 - MINOR - Tests, Docs - `sw/builder/test_builder.py:23846`, `:23852-23853`, `:23878` (gate 23o) at `7a4871d5`; `docs/design/MAILBOX_SPLIT.md:1608-1610`

**The split recipe's `nvm_split.json` is not held by gate 23o.**

**Authority and evidence**

- S9's gate 23o states that "every shape artifact it writes must be byte for byte the all-fabric build's" (`test_builder.py:23846`). The design page cites the gate for "Its shape artifacts are the all-fabric build's byte for byte" (`MAILBOX_SPLIT.md:1608-1610`). Issue #870's scope says the same: "The configs keep their shape; the recipe sets `control.placement: split`."
- The gate enforces this through a fixed tuple of eight path labels, `RECIPE_SHAPE_ARTIFACTS` (`:23852-23853`).
- #823 adds a ninth artifact. The builder now writes `nvm_split.json`, the model's layout 3 record space (`endstation_builder.py:2791`, `:5999`, `:6093-6098`). It is derived from the AEM overlay and the layout 3 declaration only.
- `milan_soc.py --ctrl-mailbox` reads that file to set the split store's record-count constants (`milan_soc.py:4911-4921`). It is the one builder artifact the split SoC itself consumes.
- The probe `scripts/probe_recipe_nvm_split.py`, at `7a4871d5`, with no file edited (`receipts/probes/recipe_nvm_split.candidate.log`), shows:
  - FACT: for all five configs the split recipe's `nvm_split.json` equals the all-fabric build's today. So the property holds, and Conformance is not affected.
  - PLANT: with `_derive_artifacts` patched so only the split recipe writes a different `nvm_split` (first block's count plus one), gate 23o PASSES ("not caught").
  - FIX-CHECK: with `nvm_split` added to the gate's labels in memory, the unplanted gate passes and the plant fails 23o.
- `receipts/probes/recipe_label_diff.candidate.log` shows the selection is deliberate. Across all five configs only `build_plan` and `soc_params` differ by placement, and those two are rightly outside the tuple. `nvm_split` is identical by design and belongs with the eight.

**Impact.** In the composed tree, the gate cited as proof that the split recipe keeps the config's shape cannot fail for a change to the split store's record space. A later edit that makes `nvm_split` depend on placement would ship a split store sized differently from the all-fabric model, and both gate 23o and the page would stay green. The gap exists only in the composition: S9's tree has no `nvm_split`, and dev-soft-core has no gate 23o.

**Required outcome.** Either:

- at the merge candidate, gate 23o holds `nvm_split.json` byte for byte with the other shape artifacts; or
- gate 23o and `MAILBOX_SPLIT.md:1608-1610` state that it is excluded, and why.

The fix may land on the PR branch or on the merge-train candidate. On S9's own tree, adding the label is inert, because both paths are absent and the gate's presence check treats that as equal.

**Verification.** Rerun `python3 -B scripts/probe_recipe_nvm_split.py` from a checkout of the fixed candidate. The PLANT line must read "caught", and gate 23o plus `test_builder.py --require-rv32` must stay green.

### S1 - SUGGESTION - Docs - `docs/design/MARK_II_AREA_PLAN.md:1051-1060`, `:1081`

S9's ledger tables give the split image's staging buffer as 3,344 / 13,264 B. These figures are dated: the images were "linked at `5d6d2835`", with KLJ2 firmware, so the statement is true as recorded.

In the composed tree the split's stage is KLJ3, 3,454 / 13,594 B (#823). #823's own size-fixture relink shows +704 to +712 B of `rom` and +352 to +576 B of `sram` per point.

`SPLIT_CONTROL_MEMORY.md:147-148` and `:179` already carry such a note for their KLJ2 figures. A one-line note under the area plan's two tables would stop a reader taking 13,264 B as the current stage: "Linked with KLJ2; the split's KLJ3 stage is 3,454 / 13,594 B (#823), [split control memory](SPLIT_CONTROL_MEMORY.md#5-fit)."

The routed-image figures are S9's measurement with KLJ2 firmware. They were not repeated on the composed firmware (section 7).

### S2 - SUGGESTION - Tests - `tb/verilator/ctrl_split_boot/run.py` (map-stability refusal); not in either side's delta

My first split boot run at the candidate was REFUSED: "the boot SoC's csr.csv depends on the image" (`receipts/candidate2/split_boot_1x1.log`).

- The two exports differ only in the ISA string's extension order: `rv32i2p0__zifencei_zicsr` against `rv32i2p0__zicsr_zifencei`.
- The product LiteX tree builds that string from a Python `set` (VexiiRiscv `isa_map`), so it depends on each process's hash seed. It does not depend on the image.
- With `PYTHONHASHSEED=0` both shapes pass (section 3).
- The README's run commands do not set a seed, and the author's endpoint exporter sets one.

Suggest a new Issue: make the comparison independent of the seed, by setting `PYTHONHASHSEED` in the child exports or by normalising the ISA string. This is not a defect of either side's delta.

### Comment rule

The merge adds no text of its own, so this round's delta has no new source comment and no RESIDUE.

### Wording

This round adds no new wording residue. Prior residue is carried in section 5.

## 3. Gates at the candidate

All gates ran from a checkout of `7a4871d5`, with real submodule checkouts at the pinned gitlinks. Toolchains:

- the pinned RV32 SDK, verified by `scripts/ci_rv32_sdk.py --verify-only` (bootlin riscv32-ilp32d glibc stable-2025.08-1, gcc 14.3.0);
- the product LiteX interpreter;
- the pinned Verilator 5.050 (rev v5.050, identity printed in `receipts/candidate2/env.txt`);
- the repository Markdown interpreter for the docs gates.

Receipts are in `receipts/candidate2/` (`*.log`, `*.rc`).

| Gate | Result |
|---|---|
| `sw/litex/test_ctrl_memory.py` (arm 8, the out-of-context mapper's override and its 3 mutants, included) | rc 0, `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS` |
| `test_builder.py --require-rv32 --gates` 23n/23o order: `test_control_placement_key`, `test_placement_recipe` (23o), `test_image_identity_gate` (23p), `test_nvm_firmware_shapes`, `test_name_count_fits_the_nvm_name_block` (38), `test_split_record_space_bounds_the_split_output` (39) | rc 0, `ALL GATES PASS` for the 6. Gate 23p: 2 good images and 1 bound-bitstream control pass, and 13 plants each fail by kind. Gate 39: 10/10 plants red |
| Full `test_builder.py --require-rv32` at the candidate (manager's bank, `665s9-candidate-0923/manager-builder/48.log`, hashed in `receipts/manager_candidate_receipts.sha256`) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, absent Arty build tree). Gates 23o, 23p and 39 present. Spot-checked, not rerun |
| Split boot simulation, `endstation_ax7101_1x1_tdm8`, `PYTHONHASHSEED=0` | rc 0, `ctrl_split_boot: PASS (0 finding(s))`, ready at 86.487 ms against 20,000 ms. The two grader FAILs are the README's no-datapath stand-ins |
| Split boot simulation, `endstation_ax7101_8x8`, `PYTHONHASHSEED=0` | rc 0, `PASS (0 finding(s))`, ready at 189.328 ms |
| `scripts/check_py_idiom.py` | rc 0 |
| `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e282ecd2`, `check_solution_docs.py`, `check_archive.py`, `check_hygiene.py --check`, `git diff --check e282ecd2 HEAD` | rc 0 each. These include both design pages' anchors, style and paths |

The split SoC export of the split boot run carries both sides together:

- #823's `milan_flash_journal_klj3_offset` (0xE4_0000) and `_size` (655,360);
- 71 `milan_nvm3_*` record constants;
- S9's removal of DDR3: no `ddrphy`, `sdram` or `ppmem` bank and no `main_ram`.

That export is disposable and not published. The rows were read in my session.

**All-fabric endpoint through the composition (AC2's intent).** The shipping 1x1 and 8x8 configs were exported all-fabric with `--no-compile-software` at dev-soft-core `8b1bdfaf` and at the candidate. Every file was compared with roots, timestamps and LiteX's hierarchy-tree lines normalised (`scripts/all_fabric_export.sh`, `scripts/export_compare.py`). Result: 21 of 21 identical for both shapes (`receipts/all_fabric/compare-*.json`). S9's delta leaves the all-fabric endpoint unchanged on top of S7 and #823 as well.

**Published executable evidence.** The tree `460db965:review-evidence/665s9-r1` was verified against its `MANIFEST.json`: 4,995 entries, 4,995 published files, 165 path-redacted, 0 mismatches (`receipts/evidence_manifest_verify.txt`, `scripts/verify_evidence_manifest.py`). The manager's candidate banks were spot-checked:

- builder bank: 48 commands, every one rc 0, `complete.json` exit 0;
- full native bank: 5 commands rc 0. These cover 5 suite shards with rc 0, protocol-processor at 1,030,922 checks with 0 failing, gptp-processor, and behave with 2,330 steps passed. `mbx` and `milan_dp` PASS.

## 4. The seven shared files at the candidate

- **`docs/design/MAILBOX_SPLIT.md`.** S7's #867 paragraph (`:2027-2035`, "`make srptx` holds them from that ring to the MAC") sits in Open items. It does not contradict S9's identity, recipe and timing sections, and the table of contents still reads correctly (`:45`). Anchors pass.
- **`docs/design/SPLIT_CONTROL_MEMORY.md`.** The pieces compose without contradiction:
  - S9's section 4 (no DDR3, no `main_ram`, the identity gate) and #823's KLJ3 stage notes (`:87`, `:97-98`, `:145-148`, `:177-179`, `:221-233`, `:328`) both stand.
  - S9's mapper override (`:352-359`) maps the platform image the preceding command links (`:339-341`), and it plans that image at the ledger point, which at the candidate expects the 13,594 B stage. The memory test's arm 8 passes on that ledger.
  - `:279` (13,264 B at `b8628704`) is #823's dated, unchanged platform figure: "The target platform's image was not linked again".
- **`sw/builder/endstation_builder.py`.** S9's `with_placement`, `--placement` and `_derive_artifacts(config_path, placement)` and #823's `aem_name_count`, `emit_nvm_split` and `nvm_split` output are independent. The split recipe writes `nvm_split.json` too, and it is identical to the all-fabric one (F1 FACT). Gate 23o does not hold it (F1).
- **`sw/builder/test_builder.py`.** S9 adds 23o and 23p, and #823 extends gate 39 at the end of the file. No gate ID or name collides. 23p's lines are unshifted (`:23727` the same at head and candidate).
- **`sw/litex/ctrl_memory_ledger.py`.** #823's `STAGE_1X1, STAGE_8X8 = 3454, 13594` (`:30`) feeds S9's `mapper_facts` (`:164`, `OWN[PLATFORM]`). The memory test's arm 8 and its 3 mutants pass on those values.
- **`sw/litex/milan_soc.py`.** #823's `journal_klj3` region, `split_constants` import and `--ctrl-mailbox` constants block (`:4911-4926`, `stage_bytes(_nvm_shape)` with its one-argument signature) sit beside S9's DDR3 removal, ident, manifest and identity gate. No caller of the old two-argument `stage_bytes` remains in the candidate.
- **`sw/litex/test_ctrl_memory.py`.** #823's stage constants and S9's eighth arm coexist, and the file passes.

## 5. Prior public findings on this PR

Every finding site below is byte-identical between `a69fc0f5` and the candidate: `check_image_identity.py`, `tb/verilator/mbx/{suite.hpp,mutants.py,README.md}`, `MARK_II_AREA_PLAN.md` and `KL_mbx_rx.sv` keep their head blobs, and `test_builder.py:23727` and `MAILBOX_SPLIT.md:137` are the same lines. So each earlier disposition carries.

| Finding (round) | Severity, lens | Status at this head, in the candidate |
|---|---|---|
| R827-1 F1: bound-bitstream branch without a positive control | MINOR, Tests | **Resolved**, retained so: 23p passes 1 bound-bitstream control at the candidate |
| R828-1 F1: manifest-ident rule without a plant | MINOR, Tests, Conformance | **Resolved**, retained so: the 23p plant "the manifest's ident changed" fails `FINDING manifest:` at the candidate (`builder_subset.log`) |
| R827-1 F2 and R828-1 F2: check ID `H0` reused | MINOR, Tests, Docs | **Resolved**: the new check is `U0` (`MAILBOX_SPLIT.md:137`) |
| R827-1 R1 and R828-1 R1: routed-net counts | RESIDUE, Docs | Resolved |
| R827-1 S1: bus-clock path headers | SUGGESTION, Docs | Taken |
| R827-1 S2: FSM default transition in `KL_mbx_rx.sv` | SUGGESTION, RTL, Robustness | Retained as SUGGESTION on #495, per the ruling |
| R828-1 S1 / R828-2 S-C: A5 against `axil-rdata-follows-port` | SUGGESTION, Tests | Retained, `mutants.py` unchanged |
| R828-2 S-A / R827-2 N1: check-ID prefixes shared before this PR | SUGGESTION, Tests, Docs | Retained |
| R828-2 S-B / R827-2 S-a: manifest-fields rule without a plant | SUGGESTION, Tests | Retained |
| R828-2 S-D / R827-2 N4: three stale byte counts in the executor's packet index | SUGGESTION, Docs | Retained |
| R828-2 RES-1 / R827-2 N3: PR body's expected final builder line | RESIDUE, Docs | Retained, fix as published. Note: the manager's candidate run prints `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 only), so the body should name each NOT RUN row rather than a fixed count |
| R828-2 RES-2: provenance claim covering 3 of 9 reports | RESIDUE, Docs | Retained, fix as published |
| R827-2 N2: gate 23p's docstring omits the bound-bitstream control (`test_builder.py:23727`) | RESIDUE, Docs | Retained. Exact fix: "gate 23p - the identity gate passes the two real images and a copy of the split one that binds its bitstream, and fails every planted one by its kind." |

## 6. Lens results

```text
[R827] PASS Conformance — 7a4871d5: receipts/composition_identity.txt; receipts/probes/recipe_nvm_split.candidate.log (FACT, 5 configs); receipts/all_fabric/compare-endstation_ax7101_{1x1_tdm8,8x8}.json (21/21); receipts/candidate2/builder_subset.log (23o, 23p, 38, 39) — the recipe (#870 scope, D2), the identity gate, D4's no-DDR3 split, #823's KLJ3 constants and journal and S7's transmit-path statement, all held together at the candidate; AC2's unchanged all-fabric endpoint holds against dev-soft-core
[R827] PASS RTL — hdl/milan/mailbox/KL_mbx.sv, KL_mbx_rx.sv (head blobs at 7a4871d5; the dev side changes no hdl/ file); 665s9-candidate-0923 full native bank (mbx and milan_dp PASS, shards rc 0); the split SoC export of receipts/candidate2/split_boot_* — S9's timing cuts and mapper reach the candidate unchanged, and S7's split benches elaborate and pass against them in the native bank
[R827] PASS Robustness — receipts/candidate2/{builder_subset,ctrl_memory}.log — refusals compose: --ctrl-mailbox --with-dram refused (23p), the split output over layout 3 refused with its figures (39, 10/10 plants), the mapper's override refused on another image and on a stray tag (arm 8 plus its 3 mutants), the stage-size refusal on the new 3,454/13,594 B stages
[R827] MINOR Tests — sw/builder/test_builder.py:23852-23853 at 7a4871d5 — F1: gate 23o cannot fail for a split recipe whose nvm_split.json differs
[R827] MINOR Docs — docs/design/MAILBOX_SPLIT.md:1608-1610 at 7a4871d5 — F1: the page cites gate 23o for every shape artifact, and the gate does not hold nvm_split.json
```

The Docs lens otherwise found nothing more. Both design pages pass every docs gate at the candidate. Their composed statements are coherent (section 4). S1 is optional.

## 7. Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 7 shared files at `7a4871d5`; recipe FACT probe; all-fabric 21/21 dev against candidate, 1x1 and 8x8; gates 23o, 23p, 38, 39; split SoC export rows | R827-3 | `a69fc0f597355a0a200ec5be6bb134b897e97ff5`, composed in `7a4871d5dbd386f39644734d2c3d7e437a21abf3` |
| RTL | CLEAN | `KL_mbx.sv` and `KL_mbx_rx.sv` blob identity head to candidate; dev side's 0 `hdl/` files; manager's candidate native bank (mbx, milan_dp); split SoC exports | R827-3 | `a69fc0f5...7ff5` in `7a4871d5...abf3` |
| Robustness | CLEAN | Refusal arms of 23p, 39 and memory test arm 8 plus mutants, and the stage-size rule, at the candidate | R827-3 | `a69fc0f5...7ff5` in `7a4871d5...abf3` |
| Tests | UNCLEAN (F1 open) | `test_builder.py` 23o/23p/39 at candidate; `test_ctrl_memory.py`; split boot 1x1 and 8x8; plant probe | R827-3 | `a69fc0f5...7ff5` in `7a4871d5...abf3` |
| Docs | UNCLEAN (F1 open) | `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` at candidate; docs gates; `MARK_II_AREA_PLAN.md:1051-1081` (S1) | R827-3 | `a69fc0f5...7ff5` in `7a4871d5...abf3` |

## 8. Limits and pending manager duties

**What this round ran, and what it relied on**

- No manager source bank runs at this exact head, and none is claimed. Source-head execution evidence is the author's published receipts, whose integrity this round verified. The full candidate builder and native banks are the manager's (`665s9-candidate-0923`). I spot-checked them and did not rerun them.
- I ran six builder gates, not the whole builder bank.
- The split boot simulation passed only with `PYTHONHASHSEED=0` (S2). My first run without a seed was REFUSED on the ISA-string order alone.
- The first gate attempt ran in a disposable extract without real submodule checkouts and refused for that reason (`receipts/candidate/`, not listed). It was rerun in a real checkout at the candidate (`receipts/candidate2/`).

**Not run**

- `make split`, `make twin` and `make srptx` in `tb/verilator/milan_dp` (S7's new split benches) are not in the manager's native bank, and I did not run them. Their composition with S9's `KL_mbx` RTL rests on the `milan_dp`/`mbx` suite passes, on the unchanged RTL blobs and on S7's own merge evidence.
- No route, Vivado run or out-of-context mapping was repeated on the composed firmware. S9's route and ledger figures are KLJ2-firmware measurements (S1).
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- Hosted evidence at the exact head: 68 check runs succeeded, including `rtl-fast`, `verilator-suites` and `yosys-portability`; 1 context, "Physical gPTP (nightly and manual)", was skipped (`receipts/hosted_checks_exact_head.tsv`). Hosted and act acceptance are the manager's.

**Manager duties**

- Build and validate the current-dev merge candidate at the merge turn. The source base is `1d6bf555` and live dev is `fa6c094b`.
- Carry the RESIDUE checklist in section 5.
- Re-run F1's probe on the fixed candidate.

**State of my clone**

My clone was switched to the candidate and to dev-soft-core for these probes, then restored to `a69fc0f5`. HEAD, the index tree, the `ls-files -s` digest, the submodule status and the clean status all match the pre-probe record (`receipts/restore/`). Every submodule is at its gitlink with no tracked or untracked change. Ignored build outputs from the gates remain: `__pycache__`, `sw/builder/out/`, and `configs/generated/{ltn_rom,ucode}.hex`. The disposable candidate worktree was removed.

## 9. Receipts

Every published file is listed in `MANIFEST.sha256`. Home-directory paths in the receipts are redacted to `<home>`. The scripts are portable and take their checkout and tools as arguments:

- `run_candidate_gates.sh`
- `builder_pinned_cc.py`
- `run_split_boot.sh`
- `probe_recipe_nvm_split.py`
- `all_fabric_export.sh`
- `export_compare.py`
- `verify_evidence_manifest.py`

R827-3 FINISHED
