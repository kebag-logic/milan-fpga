[R353] POSITIVE - exact head 499b15f97eb0a469b7cd1308fbba7af3c64d1851

# R353-1 external independent review: issue #580 / PR #591

- Head: `499b15f97eb0a469b7cd1308fbba7af3c64d1851`, tree `83b988d3b59a398a7d0cd1977194c50be92522da`. One commit, parent dev `682ecf0cb995473b72d5b4921088053ba753fc93`.
- Reviewer: [R353], external. Cleared context, own detached clone.
- Scope: rebuilt from the #580 body, the three [A10] scope comments, the [A10] assignment (issuecomment-5856274975), [A366] TAKEN / REVIEW READY, AGENTS.md, CONTRIBUTING.md, REQUIREMENTS.md REQ-VER-03/04, `docs/reference/SUBMODULES.md`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`, the capture README/checker, the processor diff `870ff88a..16be6768`, the parent diff, and the public evidence tree `147cb4b8:review-evidence/580-r1`.
- Prior public findings: PR #591 had no review findings when this pass finished (only the two review-start notes). There is nothing to resolve or retain.
- Result: 0 BLOCKER, 0 MAJOR, 0 MINOR, 2 SUGGESTION. All five lenses are covered clean at the exact head.

## Verification of the assigned points

| # | Claim | Result | Evidence (packet paths) |
|---|---|---|---|
| 1 | Gitlink is `16be6768`, recorded with `ooc.sh --record-rom-digests`, rows keyed by pin, older rows kept, digest check passes | **Holds.** The gitlink is `160000 16be6768...` at stage 0. It contains `870ff88a` and `493e5e4b`, and it equals the public processor `main` (compare: identical, 0/0). Re-running `ooc.sh --record-rom-digests` in place leaves `syn/yosys/rom_digests.tsv` byte-unchanged, so the committed ledger is exactly tool output. base->head adds only lines 13-14 and removes 0 rows (41->43, sorted). `ooc.sh KL_chan_map_render` rc 0. Probes: a corrupted `16be6768` ucode digest gives rc 2 "content digest mismatch"; removing the `16be6768` rows gives rc 2 "no recorded content digest". | `receipts/identity.txt`, `rom-record-rerun.log`, `rom-ledger-diff.txt`, `rom-check.log`, `probe-rom-A-wrong-digest.log`, `probe-rom-B-rows-removed.log` |
| 2 | SUBMODULES.md, pin text, regenerated diagram, PNG_MANIFEST.json (tool-generated) and CHANGELOG describe `16be6768` | **Holds.** Write-mode `submodule_boundaries.gen.py` regenerates `.drawio`, `.svg` and `.png` byte-identical to HEAD, and leaves `PNG_MANIFEST.json` unchanged (`git status` clean). `--check` and `--selftest` rc 0. Rendered PNG inspected: "pin 16be6768f710". `check_submodule_docs` (and selftest) and `check_diagram_pngs` rc 0. | `diagram-check.log`, `diagram-selftest.log`, `diagram-regenerate.log`, `diagram-regenerate-compare.txt`, `check_submodule_docs*.log`, `check_diagram_pngs.log` |
| 3 | `DUT_READER_DISPOSITIONS` entry present with the reviewed text; `measure_test_evidence.py --check` passes | **Holds.** `scripts/measure_test_evidence.py:597-599` matches the assigned text exactly. `--check` rc 0 (0 <= 0 unexplained readers). Removing the entry gives rc 1, "1 unexplained DUT-source reader(s) > ratchet 0". I read `protocol-processor/tb/desc_store/test_gen_desc_image.py`: it loads the generator by path, and its only reads are its own temporary `image.bin`/`image.map`. The disposition wording is accurate. | `disposition-text.txt`, `test-evidence.log`, `probe-disposition-removed.log` |
| 4 | PP_DESCRIPTOR_OWNERSHIP.md F7 rows state packer enforcement from `493e5e4b` | **Holds.** Lines 59, 168-169 and 245 state it. Processor packer test at the pin: 6/6 OK. Removing the one refusal condition in a scratch copy fails 16 refusal subtests while the legal subtests still pass. A parent-level probe on all five shipping documents alters only a body's own type or index bytes: every case is **accepted at `870ff88a`** and **refused at `16be6768`** with the directory-key diagnostic, and pristine documents pack to the shipped `aem.bin` at both pins. The parent's AEM path (`avdecc/gen_aemi_image.py:422` -> `image.build`) therefore reaches the new refusal. | `packer-tests.log`, `probe-packer-refusal-removed.log`, `parent-bodykey-probe.log`, `scripts/parent_bodykey_probe.py` |
| 5 | measurements.json: only the recorded processor pin changed; `check_nvm_capture.py` never reads it | **Holds.** The base->head diff is line 304 only (`0922e434` -> `16be6768`). The checker reads `measured_for`, `product_firmware_sha256`, `harness_sha256`, `measurements` and `maxima` (`scripts/check_nvm_capture.py:60-93`), and no parent code reads `processor_pins`. Pass rc 0. Planting all-zero/all-f pins still passes (rc 0). Planting a different firmware digest fails (rc 1, "product firmware changed; remeasure the copy"). The census's only processor input is `KL_acmp_nvm_shadow` RTL parameters, and no processor `.sv` changed between pins. | `capture.log`, `probe-capture-pin-planted.log`, `probe-capture-pin-planted-row.txt`, `probe-capture-firmware-digest.log`, `capture-reader-analysis.txt` |
| 6 | All five configurations' AEM images and builder outputs byte-identical between `870ff88a` and `16be6768` | **Holds for all five, not just two.** Exported trees: old = parent `682ecf0c` + processor `870ff88a`; new = parent `499b15f9` + processor `16be6768`. gPTP and axis are at their unchanged gitlinks. All 20 generator commands rc 0. 65 files (10 builder outputs + `aem.bin`/`.map`/`.json` per configuration) are byte-equal (sha256 and `cmp`). All 65 digests appear in the author's published `new-artifacts.json`. | `scripts/pin_equality.sh`, `pin-equality.log`, `pin-equality-old.sha256`, `pin-equality-new.sha256`, `pin-equality-rcs.txt`, `pin-equality-inputs.txt`, `pin-equality-vs-published.txt` |
| 7 | pp_shadow and milan_dp default suites, `check_port_contracts`, docs gates pass; no RTL change beyond the gitlink, no firmware change | **Holds.** Both suites ran under Verilator 5.050. pp_shadow: rc 0, 4 legs, 2,068 checks, 0 failures. milan_dp: rc 0, 14 normal legs, 11,196 checks, 0 failures, plus the render (6/6) and GM-step (4/4) mutation campaigns. `check_port_contracts` rc 0. Docs gates rc 0: `docs_check`, `check_doc_style`, `gen_toc --check`/`--verify-anchors`, `check_em_dash --base 682ecf0c`, `check_doc_paths`, `check_archive`, `check_solution_docs`, `check_gptp_docs`, `check_feature_status`, `check_rtl_source_lists`, `check_baremetal_only --check`, the module-matrix traceability check, and `git diff --check`. The parent diff touches no `hdl/`, `sw/firmware/`, `.sv/.v/.svh` or CSR path. The processor delta changes no `.sv/.v/.svh/.hex` or ROM generator: only `gen_desc_image.py` (+11), tests and docs. | `pp-shadow.log`, `milan-dp.log`, `milan-dp-tally.txt`, `port-contracts.log`, docs gate logs, `diff-check.log`, `identity.txt` |

## Findings

### S1: SUGGESTION. Docs, Tests. `tb/verilator/nvm_capture_cpu/measurements.json:2-3,303-305`: the receipt's pin field now describes a different tree from its `base`

- **Authority/evidence:** `processor_pins` was added by `054e59b4` in the same remeasurement that set `"date": "2026-09-26"` and `"base": "831f94f4..."`. `git rev-parse 831f94f4:protocol-processor` is `0922e434`, so the field recorded the measurement-time pin. After this change the field reads `16be6768`, a commit dated 2026-09-27, while `base`/`date` still name the measurement tree. Neither the receipt nor the README (`tb/verilator/nvm_capture_cpu/README.md:136`, "identifies simulator version and input hashes") defines the field.
- **Why not higher:** the frozen assignment explicitly ordered the refresh unless the checker treats the pin as a measured input. It does not (point 5 above). The measured inputs are also demonstrably unchanged (point 6), and the change is disclosed publicly (`CHANGELOG.md:44-45`, the REVIEW READY capture decision).
- **Impact:** a later reader of the receipt alone could take `processor_pins` as the measurement pin and not see that the capture was never re-run at `16be6768`.
- **Suggested outcome:** optional. State in the receipt or README that `processor_pins` names the pins the receipt was last validated against, as distinct from `base`, the measurement tree.
- **Verification:** reading the receipt and README.

### S2: SUGGESTION. Docs. `docs/reference/SUBMODULES.md:68`, `CHANGELOG.md:41`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:58,134-137,243`: cluster-minimum wording beside the adopted disposition

- **Authority/evidence:** the adopted processor text (`protocol-processor/docs/architecture/07_memory_maps.md` section 3.1 at `16be6768`) records the #122 disposition. It retains F07.2's minimum, says the parent's D8 zero-cluster 8x8 input pools conflict with Milan 5.3.3.8, and hands the correction to milan-fpga#584.
  - This PR's new lines say "Milan 5.3.3.8's cluster minimum remains required" but do not say the parent 8x8 currently violates it.
  - The parent ownership page still says the processor contract change "must disposition it under PP60" and still assigns F5 to the processor.
- **Why not a finding against #580:** issue #584 acceptance item 2 explicitly owns updating `PP_DESCRIPTOR_OWNERSHIP.md` with the #122 disposition. #580's frozen scope limits the ownership-page edit to the F7 rows. The statements are not false at this head, only incomplete.
- **Suggested outcome:** optional. Add a pointer to #584 beside the new cluster-minimum sentence, or leave it to #584.
- **Verification:** reading the text.

## Clean-lens results

```text
[R353] PASS Conformance - issue #580 body + [A10] comments 5854203161/5854653164/5854987837/5856274975 vs diff 682ecf0c..499b15f9; syn/yosys/rom_digests.tsv:13-14; scripts/measure_test_evidence.py:597-599; docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59,168-169,245; tb/verilator/nvm_capture_cpu/measurements.json:304; receipts/pin-equality* - every assigned scope item and the "no RTL/firmware/CSR change" constraint checked item by item; F7 enforcement verified at processor and parent level (receipts/parent-bodykey-probe.log); REQ-VER-03/04 gates rerun.
[R353] PASS RTL - git diff --name-only 682ecf0c..499b15f9 (no hdl/, .sv/.v/.svh, firmware or CSR path) and protocol-processor diff 870ff88a..16be6768 (no .sv/.v/.svh/.hex or ROM generator; only hdl/aecp/desc/gen_desc_image.py +11 packer lines); ROM ledger rerun and digest check (receipts/rom-*.log); check_port_contracts, check_rtl_source_lists; pp_shadow 2,068/0 and milan_dp 11,196/0 under Verilator 5.050 - the processor RTL and ROM images consumed by KL_pp_shadow are unchanged, and the wrapper and datapath still elaborate and pass at the new pin.
[R353] PASS Robustness - protocol-processor/hdl/aecp/desc/gen_desc_image.py:216-222 at 16be6768 (body type/index vs directory key, both input forms); receipts/parent-bodykey-probe.log (type-only and index-only high-byte mismatches on all five shipping documents refused at 16be6768, accepted at 870ff88a, pristine images unchanged); receipts/probe-rom-*.log (wrong and missing ledger rows refused rc 2); receipts/probe-capture-*.log (firmware digest change refused, pin-only change correctly inert).
[R353] PASS Tests - protocol-processor/tb/desc_store/test_gen_desc_image.py at 16be6768 (6/6; 16 refusal subtests fail with the refusal removed: receipts/probe-packer-refusal-removed.log); scripts/measure_test_evidence.py --check (removal of the new disposition reddens it: receipts/probe-disposition-removed.log); scripts/check_nvm_capture.py (pin plant inert, firmware plant fails); ooc.sh digest arms; pp_shadow and milan_dp default suites incl. both mutation campaigns - each check in scope can fail for the defect it guards, and the regressions stay green.
[R353] PASS Docs - docs/reference/SUBMODULES.md:25,57-73; CHANGELOG.md:11,36-46; docs/design/SAVED_STATE_MATERIALIZATION.md:232-233; docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:59,168-169,245; docs/diagrams/submodule_boundaries.{drawio,svg,png} + PNG_MANIFEST.json (byte-identical write-mode regeneration, PNG visually inspected); docs gates rc 0 with the pinned renderer - the text matches the verified facts; S1/S2 are optional clarity suggestions only.
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #580 scope + assignment vs full parent diff; ROM ledger; disposition text; F7 rows; capture receipt; five-configuration equality (65 files); REQ-VER-03/04 gates | R353-1 | `499b15f97eb0a469b7cd1308fbba7af3c64d1851` |
| RTL | CLEAN | parent diff (no RTL/firmware/CSR); processor delta `870ff88a..16be6768` (no RTL/ROM change); ooc.sh digests; port contracts; RTL source lists; pp_shadow + milan_dp suites under Verilator 5.050 | R353-1 | `499b15f97eb0a469b7cd1308fbba7af3c64d1851` |
| Robustness | CLEAN | body/key refusal at the processor and parent level (five configurations, type and index); ledger wrong/missing-row refusals; capture checker planted inputs | R353-1 | `499b15f97eb0a469b7cd1308fbba7af3c64d1851` |
| Tests | CLEAN | packer unit test + removal probe; test-evidence ratchet + removal probe; capture checker probes; suite tallies and mutation campaigns | R353-1 | `499b15f97eb0a469b7cd1308fbba7af3c64d1851` |
| Docs | CLEAN (S1, S2 optional) | SUBMODULES.md, CHANGELOG.md, SAVED_STATE_MATERIALIZATION.md, PP_DESCRIPTOR_OWNERSHIP.md, diagram trio + manifest, docs gates | R353-1 | `499b15f97eb0a469b7cd1308fbba7af3c64d1851` |

## Restoration

- All probes were restored.
- `receipts/verify-tracked-bytes.log`: 926 tracked blobs match HEAD by recomputed blob id and mode, and all initialised gitlinks equal their recorded commits. `external` is uninitialised, as CONTRIBUTING allows.
- `receipts/final-state.txt`: index equals HEAD (`write-tree` = `83b988d3`), with no assume-unchanged or skip-worktree flags.
- The `protocol-processor` checkout is clean at `16be6768`.

## Real limits

- **Assigned Verilator path missing.** `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. The suites ran through a scratch wrapper to the same Verilator 5.050 install (`verilator --version` = "5.050 2026-07-01 rev v5.050"; `verilator_bin` sha256 in `receipts/identity.txt`), matching the workflows' `VERILATOR_VERSION: v5.050`.
- **Suite parallelism.** Both suites ran with CPU affinity 0-7, and milan_dp additionally with `VERILATOR_JOBS=8`, to respect the 8-job limit. This changes compile parallelism only; the targets and flags are otherwise the defaults.
- **Renderer-dependent docs gates.** The system interpreter lacks the pinned Markdown renderer (rc 2, logs kept; see `receipts/NOTES.txt`). The gates were rerun with an existing interpreter whose renderer packages match `tools/markdown/requirements.txt` versions. The hash-level wheel identity was not re-verified; the renderer's own release refusal still applies.
- **Not run (manager-owned or disallowed):**
  - the full builder bank in either compiler mode;
  - the full parent/PP/gPTP/Yosys banks;
  - `run_all_suites.sh` and `syn/yosys/run.sh`;
  - act/Docker;
  - the processor's own suites beyond `test_gen_desc_image.py`;
  - xvlog/Vivado.

  Builder-bank evidence at this head is the author's and manager's public evidence only.
- **Scope of point 6.** This is source validation, not the final current-dev candidate merge result.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof. The capture timings are retained simulation evidence (8x8/50 MHz maximum 24.30246 ms) and were not re-measured.
- **Hosted checks (polled 2026-09-27T15:05Z).** 16 completed success; `Physical gPTP (nightly and manual)` skipped (not an executed job); `Verilator shard 1/5` and `4/5` still in progress. The `verilator-suites`/`yosys-portability` aggregate contexts were not yet present. These are observations only; hosted and act acceptance belong to the manager.

## Pending manager duties

- Confirm the exact-head hosted `verilator-suites` and `yosys-portability` aggregates conclude successfully, including the in-progress Verilator shards.
- Complete act-first local replication at the exact head.
- Build and validate the current-dev candidate merge result (base `682ecf0c`), and run post-merge containment.
- Obtain the second independent positive review ([R352]) and a maintainer merge authorization.
- Decide whether S1/S2 are taken up here, in #584, or not at all. Neither blocks.

R353-1 FINISHED
