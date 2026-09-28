[R389] POSITIVE - exact head 1a3c716f6e9fbc1c3227bce0a287ac943944fcbb

Round R389-3: composition acceptance for issue #595 / PR #614.

- Candidate tree: `22e5066f5c2012753938785121fdc2349f5553e0`.
- Train parent: `0ba810fea6a994e6dc8ba927c0c94c6fe24ae5a3`, with #577 / PR #612 and #395 / PR #605 queued ahead.
- PR source head: `11e4e1f2876c99e8f136d869c70674e077ddcf94`.
- Source reviews: [R388-2](https://github.com/kebag-logic/milan-fpga/pull/614#issuecomment-5868697340) POSITIVE and [R389-2](https://github.com/kebag-logic/milan-fpga/pull/614#issuecomment-5868698776) POSITIVE, both at the source head.

I wrote the verdict and the ledger below from my own pass, before reading any prior review report. Section 6 records how the prior findings stand at this head.

## Findings

None. No BLOCKER, MAJOR or MINOR is open under any lens.

## 1. Composition topology

| Check | Result | Receipt |
|---|---|---|
| Candidate parents | `0ba810fe` (train parent) and `11e4e1f2` (PR source) | `git log` |
| Automatic merge of parent and source | `git merge-tree --write-tree` rebuilds `22e5066f`, the candidate tree exactly, with no manual resolution | report text |
| Composed patch against source patch | `git diff 0ba810fe 1a3c716f` and `git diff 1fa2357f 11e4e1f2` have identical bodies, excluding `index` and `@@` lines: 384 lines each, 5 files | `receipts/composed.diff`, `receipts/source.diff` |
| Live dev `7a7582f0` | Merging it into the candidate gives the same tree, `22e5066f`. PR #610's head `6b76f2d8` is already in the train. | report text |
| Files shared with predecessors | `sw/builder/endstation_builder.py`: #577 (`a53682ed`). `sw/builder/test_builder.py`: #577 (`a53682ed`, `be6b48c1`) and #395 (`66001a30`, `09de469c`). `docs/ENDSTATION_BUILDER.md`: #577 (`be6b48c1`). No predecessor touches `README-parameters.md` or `test_declarations.py`. | `git log 1fa2357f..0ba810fe -- <files>` |
| Hunk overlap | None. In candidate line numbers: the #577 builder edits are at 72 (import) and 2311 to 2315 (the `validate_shipping_image` call in `_entity_model_image`). The #595 builder edits are at 1444 to 1447 (formats), 3187 to 3199 (`_mac48`), 3313 (`load_platform`) and 3670 to 3711 (`_declared_uint` and its callers). The #577 doc text is at 137 to 141, 213 to 214 and 579 to 587. The #595 doc text is at 887 to 895. | composed diff |

## 2. Semantic interaction evidence

**Stricter parsing and the image check run together without masking each other.** Receipts: `receipts/compose-probe.log` and `compose_probe.py`, run on a disposable copy of the candidate. The probe wraps `validate_shipping_image` to count calls.

- **A.** Each of the five tracked configurations loads. `_entity_model_image()` then calls the image check exactly once, and the image is accepted.
- **B.** The probe tries these non-string values: an unquoted MAC `020000000002`, a base-60 MAC `10:20:30:40:50:02`, an integer and a boolean `vendor_oui`, and an integer and a null `entity_capabilities`. Each gets the exact #595 message: `<field>: quote the hexadecimal value as a YAML string`. The image check is never reached.
- **B (formats).** A scalar talker `formats`, whether a quoted string, an integer or `7`, is refused with `streams.talkers[0].formats: must be a list of quoted hexadecimal strings`.
- **C.** The quoted spellings `"02-00-00-00-00-02"` and `"0x001BC5"` load, reach the image check, and are accepted.
- **D.** The probe combines a quoted OUI declaration with a packed image whose AUDIO_UNIT rate offset is damaged. The image check still refuses it, with `aem_desc.bin: L10_OFFSET: ...`.
- The #595 suite's capabilities round-trip, `test_declared_hex_string_contract`, now packs through the composed `_entity_model_image()`, so the #577 check runs inside it. It passes in `receipts/declarations.log`.

**Mutation controls in the composed tree.** Receipts: `receipts/mutants.log` and `mutants.py`. Each mutant was restored and the sha256 re-verified.

| Mutant | Killing check | Result |
|---|---|---|
| M1: `_mac48` rereads `str(v)` as hex | `test_declarations.py` | KILLED: "accepted 0x000000F42402" |
| M2: `_declared_uint` accepts YAML integers | `test_declarations.py` | KILLED: "accepted 0x123456" |
| M3: scalar `formats` falls back to the default | `test_declarations.py` | KILLED: the list-type message is missing |
| M4: #577 call to `validate_shipping_image` removed | gate 36b and schema-12 functions | KILLED: "empty rates accepted; missing L10_EMPTY" |
| M5: #577 `ImageCheckError` swallowed | gate 36b and schema-12 functions | KILLED: same message |

The unmutated controls and the restored controls both return rc 0.

**Artifacts: the five configurations are byte-identical to the train parent.** Receipts: `artifact_inventory.py`, `receipts/artifacts-parent.json` and `receipts/artifacts-cand.json`.

- The script runs `build()` into a scratch directory for each configuration. It also writes the `_entity_model_image()` set (`aem_desc.bin`, `aem_desc.json`, `aem_desc.map`), which passes through the #577 check.
- That gives 13 files per configuration (65 in total), plus the tracked `hdl/common/csr/gen/lwsrp_csr_defaults.svh` that `build()` rewrites.
- Parent and candidate hash to identical sha256 and size for all 66 entries, and `diff -r` over the raw bytes shows no difference.

**Gate inventory in the composed `test_builder.py`.**

- The module has 308 top-level definitions and no duplicate names.
- All 90 `test_*` functions are in the `__main__` run list. That includes the #395 `test_commercial_timing_grade`, the four #577 gate-36b functions, and the #595-edited `test_schema_12_refusals` and `test_schema_12_keys_reach_the_image`.
- #595 adds no gate number. It only requotes gate 25a and 25b fixtures (the `_schema_12_*` helpers), which #577 and #395 do not touch.

**YAML users outside the diff.**

- The tracked `configs/*.yaml` files and the `tb/verilator/pp_shadow/fixtures/*.yaml` files (changed by an earlier train member) contain no unquoted `mac_address`, `vendor_oui`, `entity_capabilities` or `formats` value.
- The fixtures override only `crf_output`, talkers without `formats`, and `emitter_srp_vid`.
- No other Python caller builds these keys as integers. `avdecc/*` reads the overlay, not the YAML.

## 3. Gates run on the candidate

All ran at `1a3c716f` in this clone unless a disposable copy is named. Every run returned rc 0. The receipt index is `receipts/gates.tsv`, with a log per gate.

- `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration`, 681 s.
  - Result: `ALL GATES PASS EXCEPT 1 NOT RUN`.
  - The one arm not run is gate 11, the utilization calibration. Its real report is not on disk.
  - The `--require-elaboration` verdict reports no toolchain skip.
  - Gate 1b adopted the provisioned SDK `riscv32-linux-gcc` (Buildroot 2026.05, 14.3.0).
  - The declaration suite (`[595 MAC]`, `[595 uint]`, `[595 formats]`), the timing-grade entries and all of gate 36b ran.
  - Gate 32 reports 112 loader keys, equal to 112 keys across 64 rows.
- `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>`, in a disposable copy at the candidate head, 350 s.
  - Result: `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`. The NOT RUN is the intended stand-down.
- `python3 sw/builder/test_firmware_compiler.py --selftest`.
- `python3 sw/builder/test_declarations.py`.
- `python3 scripts/pp_srcs.py --check --selftest`.
- With the pinned Markdown environment `md-venv-40cdefe08ebd`:
  - `scripts/docs_check.py`, both with Git and with `GIT_DIR=/dev/null`;
  - `scripts/check_em_dash.py --base 0ba810fe...`, which found 0 across 21 added lines in 2 pages;
  - `scripts/check_doc_style.py` and its `--selftest`;
  - `scripts/gen_toc.py` with `--selftest`, `--verify-anchors` and `--check`;
  - `scripts/check_doc_paths.py`.
- `python3 scripts/check_py_idiom.py` and `python3 scripts/measure_naming.py --check`.
- `python3 scripts/ci_events.py --check`: 1655 contract items. The composition changes no workflow file.
- `git diff --check 0ba810fe 1a3c716f`.
- Composition probe and mutation controls (section 2).
- Verilator identity: `$VALIDATION_TOOLS/verilator-v5.050/bin` reports `Verilator 5.050 2026-07-01 rev v5.050`, and `verilator_bin` has sha256 `51910d8d...`. Receipt: `receipts/verilator-identity.txt`. The assigned path under `$VALIDATION_STORAGE/372-manager-candidate1/` does not exist, so this equivalent 5.050 install was put first on PATH.

## 4. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #595 acceptance 1 to 5 and the assignment decisions; the composed `sw/builder/endstation_builder.py` at 1444 to 1447, 3187 to 3199, 3313 and 3670 to 3711; the #577 hook at 72 and 2311 to 2315. The composition touches this scope: both rule sets run in one loader and emitter path (probe A to D). Acceptance 4 is re-proved against the train parent (66/66 artifacts identical). | R389-3 | `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` |
| RTL | CLEAN | The composed diff has no HDL, constraint or Tcl file. The gitlinks (`protocol-processor` `c951a9ff`, `gptp-processor` `5dce647a`, `verilog-axis` `48ff7a7e`, `external` `efeb541a`) equal the parent's. `pp_srcs.py --check --selftest` covers the suite's derived read of `pp_adp_pkg`. The composition does not touch the RTL scope, so the lens is also covered by source reviews R388-2 and R389-2 at `11e4e1f2`. | R389-3 (inapplicability) with R388-2 and R389-2 (source) | `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` (source reviews: `11e4e1f2876c99e8f136d869c70674e077ddcf94`) |
| Robustness | CLEAN | `compose_probe.py` B and D: malformed and non-string values, including booleans, nulls, base-60 and octal forms, and scalar `formats`, are refused before emission; a damaged image after valid parsing is still refused. Mutants M1 to M5. The parsing order is load, then overlay, then pack, then check. | R389-3 | `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` |
| Tests | CLEAN | The composed `sw/builder/test_builder.py`: no duplicate definitions, 90/90 tests in the run list, gates 25a/25b/25c, 32, 36a, 36b and the timing grade all pass. The full bank, the absent bank, `test_declarations.py`, and five killed mutants. | R389-3 | `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` |
| Docs | CLEAN | The composed `docs/ENDSTATION_BUILDER.md`: #577 text at 137 to 141, 213 to 214 and 579 to 587; #595 text at 887 to 895. They are disjoint and consistent, and the builder-side check is described where #577 placed it. `sw/builder/README-parameters.md` at 70, 127 to 130 and 159 to 167. The `#entity-identity` anchor exists at README-parameters.md:148. The Markdown gates and `gate 32` (doc key map) are green. | R389-3 | `1a3c716f6e9fbc1c3227bce0a287ac943944fcbb` |

## 5. Limits and pending manager duties

- **Physical calibration was not run.** Gate 11's utilization report is absent. Field and hardware skips are not hardware proof.
- **The absent-compiler bank records its intended stand-down.** That is 0 actual compiler invocations, as designed.
- **The final current-dev candidate is the manager's.** Today, merging live dev `7a7582f0` into this candidate reproduces `22e5066f`, but the manager still owns that candidate at the merge turn.
- **Hosted acceptance is the manager's.** At the PR source head `11e4e1f2`, every executed hosted job I observed had passed. Verilator shards 1/5, 2/5 and 4/5 were still pending, and the physical gPTP context was skipped. No hosted run exists for this candidate head. I did not run act.
- **Pre-existing observation, not caused by this composition.** `docs/ENDSTATION_BUILDER.md` rows 0, 2a and 3a, and line 1046, cite `endstation_builder.py` line numbers. Those were already stale at dev `1fa2357f` (for example, `_vendor_oui` "line 3521" against the actual 3671 there). The composition shifts them further but does not create the drift.
- **`ci_events.py --selftest` was not run**, because no workflow file changed. `--check` passed.

## 6. Prior public findings on PR #614

I wrote the verdict and the ledger above before reading these reports. Sources: [R388-1](https://github.com/kebag-logic/milan-fpga/pull/614#issuecomment-5868119667), [R389-1](https://github.com/kebag-logic/milan-fpga/pull/614#issuecomment-5868161494), R388-2 and R389-2 (linked above). The two round-2 reviews raised no new finding. The re-check receipts are `prior_probe.py` and `receipts/prior-findings-probe.log`.

| Finding | Severity and lenses | Status at `1a3c716f` | Evidence at this head |
|---|---|---|---|
| R388-1 F1 = R389-1 F1: the declaration test named `protocol-processor/hdl/adp/pp_adp_pkg.sv` literally | MAJOR, Tests and RTL | **Resolved** | `scripts/pp_srcs.py --check --selftest` returns rc 0 on the composed tree (`receipts/pp-srcs.log`). The literal is absent from the composed `test_declarations.py`. The derived lookup's independent `ADP_ENTITY_CAPS_C` read still packs through the composed `_entity_model_image()`, and `test_declarations.py` returns rc 0. |
| R388-1 S2: summary lines said "quoted" | SUGGESTION, Docs | **Resolved (taken)** | `docs/ENDSTATION_BUILDER.md:887` reads "Hexadecimal declarations require YAML strings." It is the source's line 883, shifted by the #577 text. `sw/builder/README-parameters.md:70` reads "EUI-48 YAML string". |
| R388-1 S1 = R389-1 S1: lenient quoted MAC and hex shapes (separators stripped, signs, whitespace) | SUGGESTION, Robustness | **Retained, pre-existing, out of scope** | Behaviour is identical at the train parent and the candidate. `"2:0:0:0:0:2"` gives `0x000000200002`, `"-2"` gives `0x000000000002`, and `"+1BC5"` gives `0x001BC5`. The manager recorded it for the #495 checklist. A SUGGESTION does not affect coverage. |

No prior MINOR, MAJOR or BLOCKER is open at this head.

## 7. Receipt integrity

- After the in-clone bank, the clone still has HEAD `1a3c716f` and tree `22e5066f`.
  - The index equals the HEAD tree, and `git diff-index HEAD` is empty.
  - Every tracked blob hashes equal to its index entry, and no file mode has drifted.
  - The gitlinks are unchanged, and the submodule work trees are clean.
- I removed the ignored build outputs that the bank created, so the clone is back to its received state: 0 ignored or untracked entries (`receipts/integrity-final.txt`).
- All disposable trees are under `scratch/` and are not published. The mutant tree's source was restored, and its sha256 was verified at `0cb5b7f3...`, equal to the candidate's `endstation_builder.py`.
- I made no source edit, commit, push, GitHub write or merge.

R389-3 FINISHED
