[R340] NEGATIVE - exact head 08374721d958b32ade38e7e62d25a7ccea215119

# R340-2: internal independent re-review of PR #585 (issues #573-#576), round 2

- Head `08374721d958b32ade38e7e62d25a7ccea215119`, tree `b852bb03617b6cdfda344ae8a791868ab0f3e835`. Base dev `e0920d77162284d8da52ffaf13a973e451e44f90`.
- Round 1 (R340-1) covered `4f746408` in full. This round judges the delta `4f746408..08374721`: five commits, one per item group of the round-2 assignment (issue 573 comment 5854262940). Each commit has a one-line subject with no body and no trailers (`receipts/delta.txt`).
- Files in the delta (added/removed lines): `avdecc/aem_descriptors.py` (+15/-3), `sw/builder/endstation_builder.py` (+17/-9), `sw/builder/test_declarations.py` (+104/-9), `sw/builder/README-parameters.md` (+10/-3), `docs/ENDSTATION_BUILDER.md` (+2/-1) and `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (+11/-9). No HDL, processor or submodule change. `git diff --check` is clean.
- Authorities: AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue #573-#576 scope, the round-2 decision comment, and the clause text. I extracted Milan v1.2 5.3.1, 5.3.3.1, 5.3.3.4, 5.3.3.6 and 5.6.2, and IEEE 1722.1-2021 7.2 and Table 7-8 (with the 2013 Table 7-8 for contrast), myself (`receipts/clause_check.txt`).
- Prior public findings were read only after my own pass over the delta. They are resolved below.

## Verdict summary

Every round-1 finding is closed at this head:
- R340-F1 = R341-1-F2: the buffer wrap.
- R341-1-F1: the format cap of 46.
- R340-F3 = R341-1-F3: the clause citation.
- R340-F2: the stale design-doc line.

Each new check is killed by its own mutant. The five configurations' 85 artifacts are byte-identical to `e0920d77`, and the second reviewer's independent artifact inventory also matches 80/80. The three Arty configurations still build.

Two new MINOR findings remain open, so the verdict is NEGATIVE:
- **R340-2-F1.** The fix for R341-1-S1 replaced one silent reinterpretation with another. An unquoted, unprefixed, all-digit hex EUI-64 is now taken as a decimal or YAML 1.1 octal integer, and emitted without refusal. For the all-decimal-digit case this is a regression from `4f746408`. The new README and matrix sentence says the opposite.
- **R340-2-F2.** A matrix experiment row edited in this round still presents 47 entries (514 octets) as the accepted Table 7-8 boundary.

## Findings

### R340-2-F1: MINOR: Conformance, Robustness, Tests, Docs: `sw/builder/endstation_builder.py:1331` (`_eui64`), `sw/builder/README-parameters.md:152`, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:196`, `sw/builder/test_declarations.py:80`: unprefixed unquoted hex EUI-64 values are silently reinterpreted

- **Authority/evidence:**
  - The round-2 decision (issue 573 comment 5854262940, item 5, R341-1 S1) says: "an unquoted YAML hex EUI-64 must parse to the value written, or be refused with a message telling the user to quote it. Never a silent reinterpretation. Test both."
  - `_eui64` accepts unprefixed hex text. `int(str(v), 16)` makes quoted `"1234567890123456"` resolve to `0x1234567890123456`.
  - At this head a YAML integer is now taken as-is (`n = v if type(v) is int else ...`). YAML 1.1 resolves an unprefixed all-digit scalar to a decimal integer, and a leading-zero scalar made only of the digits 0-7 to an octal integer.
  - `receipts/round2_probes_head.log`, on both `entity_model_id` and `model_id_pin`, with no `vendor_oui` declared:
    - Unquoted `1234567890123456` is **accepted** as `0x000462D53C8ABAC0`. The quoted form of the same text gives `0x1234567890123456`.
    - Unquoted `0012345670123456` is **accepted** as `0x000000A72EE0A72E`.
    - Prefixed `0x...` spellings, with or without underscores, now resolve correctly. That was the R341-1-S1 case, and it is fixed.
  - `receipts/round2_probes_prev_4f746408.log`: at the previous head the unquoted all-decimal-digit spelling resolved to the written `0x1234567890123456`. That spelling is a regression introduced by `08374721`. The octal spelling was wrong at both heads.
  - `README-parameters.md:152` ("Quoted and unquoted hexadecimal EUI-64 values retain their numeric value.") and `PP_DESCRIPTOR_OWNERSHIP.md:196` state the opposite.
  - The test (`test_declarations.py:80`) tries only the `0x`-prefixed spelling, quoted and unquoted. No refusal-with-quote case exists, which "Test both" asked for.
  - Mutant R2-11 (restoring the old reparse) is killed, so the prefixed case is pinned. Nothing pins the unprefixed case.
- **Impact:**
  - A configuration can emit an ENTITY/ADP `entity_model_id` other than the one written, with no refusal. This includes a `model_id_pin`, whose purpose is to preserve a deployed identity.
  - The literal and pin OUI cross-check only runs when `vendor_oui` is declared (`endstation_builder.py:4380`).
  - The same parser serves `srp.stream_dmac_base` and the `_fmt64` stream-format words, so the change in unquoted handling reaches those keys too. It is undocumented there.
  - No tracked configuration uses these spellings. All five artifact sets are unchanged.
- **Required outcome:** Every YAML scalar given for an EUI-64 identity must either resolve to the value of its written hex digits or be refused with a message telling the user to quote it. This includes unprefixed all-decimal-digit and YAML-1.1-octal-looking spellings. No spelling may resolve silently to a different number. The README and matrix sentences must state the rule that is enforced. The treatment of the other `_eui64` users (DMAC base, format words) must be stated or kept deliberately.
- **Verification:**
  - Declaration tests for unquoted `1234567890123456` and `0012345670123456` on both identity keys, each either equal to the written hex value or refused with the quote message.
  - A mutant that restores the current behaviour is killed.
  - Rerun `scripts/round2_probes.py`.
  - The five-configuration artifact identity is unchanged.

### R340-2-F2: MINOR: Conformance, Docs: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:166`: the processor L4 experiment row still names 47 entries as the accepted Table 7-8 boundary

- **Authority/evidence:**
  - IEEE 1722.1-2021 Table 7-8 caps `number_of_formats` at 46, and 7.2 caps a descriptor at 508 octets (`receipts/clause_check.txt`). The decision also fixed the cap at 46.
  - This round edited only the last cell of line 166. The row now reads "Accepted control or boundary: Buffer 2126000; 47-entry size 514 | One invalid change: Buffer 2125999; 48-entry size 522 | Both accepted; 576-byte buffer is not the 46-format cap".
  - A 47-entry, 514-octet STREAM descriptor is not a legal boundary under the cap the same document now states at line 62 (L4) and line 179. Line 179 lists 47 entries as a refused parent probe.
  - The row's measurement comes from `scripts/audit_pp_descriptors.py:210`, whose probe label is "47 formats at Table 7-8 cap". That label predates this PR, is outside the diff, and is cited by the matrix's own reproduction command at line 267.
- **Impact:** The ownership matrix contradicts itself about the Table 7-8 boundary. A cold reader of the experiment table would take 47 entries as the legal maximum. That is the 2013 figure this round was assigned to remove from the parent's statements.
- **Required outcome:** The row states the 2021 boundary. For example, 46 entries (506 octets) as the accepted control and 47 (514) as over the cap, both accepted by the processor packer. Alternatively, the row explicitly marks 47/514 as over the IEEE 1722.1-2021 cap. The stale probe label is relabelled, or routed as its own item.
- **Verification:** Read line 166 against lines 62 and 179 and against Table 7-8. Grep the parent docs and scripts for a 47 figure called the Table 7-8 cap. Run the docs gates.

### Suggestions (non-blocking; they do not leave any lens unclean)

- **R340-2-S1: SUGGESTION: Tests: `sw/builder/test_declarations.py:69-99, 254-261`.** Two correct head behaviours are not pinned by a test (`receipts/r2_mutants_head.log`):
  - A YAML boolean EUI-64 is refused. PROBE mutant R2-12 (`isinstance` admits `True` as ID 1) survives.
  - A null `media_clock_sources:` is refused with the named L6 message. PROBE mutant R2-17 (the guard matches only `[]`, so null crashes) survives.

  Both are correct at the head (`receipts/round2_probes_head.log`).
- **R340-2-S2: SUGGESTION: Docs: `docs/ENDSTATION_BUILDER.md:958, 974, 978, 991`.** Parameter-table rows 2, 9, 12 and 19 still do not name the new refusals: the reserved identity, the empty or CRF-only sources with outputs, the CRF word, and the buffer floor and width. The decision made this optional.

## Round-1 findings: disposition at 08374721

| Finding | Status | Evidence |
|---|---|---|
| R340-F1 MAJOR = R341-1-F2: buffer floor bypassed by 32-bit truncation | **CLOSED** | `endstation_builder.py:1388-1391` refuses `> UINT32_MAX`. `UINT32_MAX` is derived once from the `AEM_U32` struct that `be32` packs with (`aem_descriptors.py:182-189`). My unchanged `buffer_wrap_probe.py` gives: `0xFFFFFFFF` packs equal; 2^32 and 2^32+2125999 are refused with a named `ConfigError` (`receipts/buffer_wrap_head.json`). The second reviewer's `bypass_probes.py` refuses 4294967296, 4294968296, 4297093296 and 8589934592 (`receipts/r341_bypass_probes_head.jsonl`). The tests read offset 128 of the packed image at all eight listener indices (`test_declarations.py:114-139`) and refuse both wrap values (`:141-144`). Mutants R2-01..R2-05 are killed. |
| R341-1-F1 MAJOR: format cap 47 is the 2013 figure | **CLOSED in code and tests; one stale doc row remains (R340-2-F2)** | `aem_descriptors.py:273-276` derives `(508 - 138) // 8 = 46` in one source. `d_stream` uses the same `STREAM_FORMATS_OFFSET` (`:307, :314`). The builder imports it (`endstation_builder.py:124`) and restates no literal. Tests (`test_declarations.py:169-187`): talker 46 is accepted, listener 45+1 derived is accepted, and a packed body of 506 octets has `number_of_formats` 46. 47 and 46+1 are refused, in both directions. My probes and the second reviewer's probes agree. Mutants R2-06..R2-10 (cap +1, cap -1, 516-octet maximum, restated 47, shifted offset) are killed. The clause check confirms 46 and 508 for 2021 and 47 for 2013. |
| R340-F3 = R341-1-F3: clause for the reserved-ID rule | **CLOSED** | The message (`endstation_builder.py:1345`), `README-parameters.md:153-154`, the test comments (`test_declarations.py:36, 46`) and the matrix L9 row (`PP_DESCRIPTOR_OWNERSHIP.md:67`) cite Milan v1.2 5.3.3.1 and 5.6.2, and keep 5.3.1 for evolution only. I verified this against the clause text. No zero/all-ones rule is attributed to 5.3.1 or 6.2.2.8 anywhere else in the changed files. |
| R340-F2 MINOR: `ENDSTATION_BUILDER.md:443` | **CLOSED** | Lines 443-444 now state the enforced refusal and its clauses. |
| R340-S1: CRF-output arm observable only by precedence | **CLOSED (taken)** | `test_declarations.py:236-244` calls `_validate_output_clock_sources([], clocking)` directly. A576-14 and R2-18 are now killed by "CRF output accepted without INTERNAL". |
| R340-S2: empty `media_clock_sources` raises `IndexError` | **CLOSED (taken)** | `endstation_builder.py:3841-3844` raises a named L6 error citing Milan 5.3.3.6. I verified 5.3.3.6 requires at least one CLOCK_SOURCE per domain. `[]`, null and `""` are refused, and `[internal]` is accepted (`receipts/round2_probes_head.log`). R2-16 is killed. |
| R340-S3: shadowed literal under a pin | **CLOSED (taken)** | `endstation_builder.py:4373` validates the literal first. Zero, all-ones and malformed literals are refused under a legal pin, and a legal literal plus a pin still emits the pin. R2-13 and R2-15 are killed. |
| R341-1-S1: unquoted YAML hex EUI-64 reinterpreted | **Partially done; new R340-2-F1** | The prefixed spelling is fixed and pinned (R2-11 killed). The unprefixed all-digit spelling regressed, and the octal spelling is still reinterpreted. |
| R341-1-S2: hash-derived arm bypasses the guard | **CLOSED (taken)** | `endstation_builder.py:4377`. The test patches `derive_model_id` to both endpoints (`test_declarations.py:96-99`). R2-14 is killed. |

## Evidence (reviewer-run, this packet)

- **Declaration suite.** `receipts/declarations_head.log` is `python3 -B sw/builder/test_declarations.py` at the exact head, rc 0. It includes the new `[F1] quoted/unquoted...` line and gate 40.
- **Round-1 scripts, rerun unchanged.** Their sha256 matches both round-1 manifests.
  - My `probes.py` (`receipts/probes_{head,prev_4f746408}.{log,json}`) was run at the head and at `4f746408` for contrast. The only changes are the intended ones: the shadowed zero literal, the wrap values, 47-final formats and the empty source lists are now refused. The unquoted integer CRF word, being equal to the Milan word, is now accepted.
  - My `buffer_wrap_probe.py`: see the R340-F1 row above.
  - My `mutants.py` with `mutant_cases.json`: **30/30 killed**, the control passes, and the source was restored identically (`receipts/r340_mutants_head.{log,json}`).
  - The second reviewer's `run_mutants.py`: 12/12 applicable mutants killed, and the restored control is rc 0 (`receipts/r341_mutants_head.json`). R-M8 and R-M14 are "not applied", because the literal `MAX_STREAM_FORMATS = 47` they patch no longer exists. Their intent is covered by R2-06, R2-07 and R2-09.
  - The second reviewer's `bypass_probes.py` (`receipts/r341_bypass_probes_head.jsonl`), rc 0.
  - The second reviewer's `format_cap_length.py` (`receipts/r341_format_cap_length_head.txt`) prints the accepted 46-entry, 506-octet boundary. It then exits 1 on the uncaught named refusal of 47, which is the required behaviour. The script has no refusal handler, so rc 1 is the expected outcome here, not a defect.
- **New in this round.**
  - `scripts/mutants_r2.py` with `scripts/mutant_cases_r2.json` (`receipts/r2_mutants_head.{log,json}`): 16/16 required mutants are killed. The two PROBE mutants survive, as reported in S1. The control passes, and both mutated sources were restored identically.
  - `scripts/round2_probes.py` (`receipts/round2_probes_{head,prev_4f746408}.{log,json}`): YAML spellings, the pin and literal precedence, the DMAC base, and empty sources.
- **Artifact identity.**
  - My `hash_artifacts.py` (`receipts/artifacts_{base_e0920d77,head_08374721}.json`, `receipts/artifacts_compare.txt`): 5 configurations × 17 artifacts, **85/85 identical** in sha256 and size. This covers `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_*.svh`, `gptp_ucode.hex`, the overlay, and the store and image outputs. The head also equals my round-1 `4f746408` receipt.
  - The second reviewer's `shipping_identity.sh` through the builder CLI: **80/80 identical** (`receipts/r341_shipping_*.sha256`, `receipts/r341_shipping_compare.txt`).
  - All three Arty configurations build. No tracked configuration is refused, so the STOP rule did not trigger.
- **Focused docs and idiom gates** (`receipts/docs_gates_head.txt`): `check_doc_paths` OK, `check_doc_style` OK, `check_py_idiom` rc 0. `check_em_dash` and `gen_toc --check` could not run (rc 2) because their pinned Markdown renderer is not installed, and installs are out of bounds. The delta diff contains no em dash.
- **Hosted contexts.** `receipts/hosted_checks_08374721.tsv` was read-only at 11:21 local time.
  - Completed with success: `changes`, `full-ci-gate`, `verilator-lint`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, Yosys shards 0-3, and Verilator shard 3/5.
  - In progress: `docs-check`, `elaborate`, `yosys-elaboration`, and Verilator shards 0, 1, 2 and 4.
  - Physical gPTP was skipped, which is not hardware proof.
- **Clone integrity** (`receipts/clone_integrity.txt`, `scripts/clone_integrity.sh`):
  - HEAD, tree and `write-tree` equal the expected values, and the porcelain is empty.
  - The index modes and blobs equal the HEAD tree (917 entries).
  - The worktree blob bytes equal the HEAD blobs.
  - Gitlinks: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `0922e434`, verilog-axis `48ff7a7e`.
  - Every probe, mutant and build ran in disposable copies under `scratch/`.

## Reviewer-owned completion ledger (round R340-2)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R340-2-F1 MINOR, R340-2-F2 MINOR) | `endstation_builder.py:1329-1346, 1380-1400, 3840-3844, 4366-4380` and `aem_descriptors.py:182-189, 272-276, 307, 314` against the round-2 decision items 1-5, Milan v1.2 5.3.3.1/5.3.3.4/5.3.3.6/5.6.2 and IEEE 1722.1-2021 7.2/Table 7-8 (`receipts/clause_check.txt`); `receipts/round2_probes_head.log`, `buffer_wrap_head.json` | R340-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| RTL | CLEAN | The diff touches no `.sv`, processor or submodule file (`receipts/delta.txt`). `aem_descriptors.py:182-189`: `be32` via `AEM_U32.pack(v & UINT32_MAX)` is equivalent to the previous `>I` and `0xFFFFFFFF` mask. `:307, :314`: `formats_offset` and `redundant_offset` are unchanged in value. The declared buffer now equals the packed Table 7-8 offset-128 u32 (`buffer_wrap_head.json`; the test at `test_declarations.py:114-139`). The generated RTL headers (`adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_csr_defaults.svh`, `lwsrp_table.svh`, `gptp_ucode.hex`) are byte-identical for all five configurations (`artifacts_compare.txt`). | R340-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Robustness | UNCLEAN (R340-2-F1 MINOR) | `receipts/round2_probes_head.log`: 11 YAML spellings × 2 identity keys, the shadowed and malformed literal, the DMAC base, and null, empty and `""` sources. `probes_head.log` (37 cases). `r341_bypass_probes_head.jsonl`: wrap values, 45+1 and 46+1 formats, talker isolation. | R340-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Tests | UNCLEAN (R340-2-F1 MINOR: unprefixed spellings and the refusal case untested) | `test_declarations.py:69-261` run through its own entry point (`declarations_head.log`). Mutants: 30/30, 12/12 applicable, and 16/16 required round-2 mutants killed, with 2 PROBE survivors reported as S1 (`r340_mutants_head.log`, `r341_mutants_head.json`, `r2_mutants_head.log`). | R340-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Docs | UNCLEAN (R340-2-F1 MINOR, R340-2-F2 MINOR) | `README-parameters.md:117-154`, `ENDSTATION_BUILDER.md:439-448, 958-991`, `PP_DESCRIPTOR_OWNERSHIP.md:62, 64, 67, 150-200, 238-243`, `scripts/audit_pp_descriptors.py:210`, `receipts/docs_gates_head.txt`, the REVIEW READY comment 5854525373 | R340-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |

RTL is covered clean at this head. A later commit that touches `avdecc/aem_descriptors.py` or any generated-header input un-covers it. The other four lenses must be re-covered at a head that closes R340-2-F1 and R340-2-F2.

## Real limits

- The standards texts are local copies (hashes in `receipts/environment.txt`). The receipts contain only one-line quotes, and the extractions stay in unpublished scratch.
- The full parent, processor, gPTP, Yosys and builder banks were not run, by instruction.
- The public evidence tree linked for this round (`265f00ea…/review-evidence/573-r1`) is the round-1 packet for `4f746408`. I found no published exact-head (`08374721`) bank receipts. The REVIEW READY comment asserts them, and the author says its round-2 packet is awaiting coordinator publication. My conclusions rest on my own reruns listed above.
- The em-dash and table-of-contents gates were not runnable here (missing pinned renderer).
- Verilator was not used, because the diff has no HDL, so its identity was not checked. Docker and act were not used.
- Physical calibration was NOT RUN. Hosted field skips are not hardware proof. Several hosted contexts were still in progress when observed.
- This is source validation at the head. The final current-dev merge candidate was not built.

## Pending manager duties

- Publish this report and the manifested receipts.
- Route R340-2-F1 and R340-2-F2 to the executor. The suggestions are optional.
- Publish the round-2 author evidence for `08374721`.
- Own hosted and act acceptance at the exact head. `docs-check`, `elaborate`, `yosys-elaboration` and four Verilator shards were in progress when observed.
- Obtain the external round-2 review.
- Build and validate the merge candidate against live dev at the merge turn.
- Re-cover Conformance, Robustness, Tests and Docs on the corrected head. Re-cover RTL too if the correction touches its scope.

R340-2 FINISHED
