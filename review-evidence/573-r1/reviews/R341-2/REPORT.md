[R341] NEGATIVE - exact head 08374721d958b32ade38e7e62d25a7ccea215119

# R341-2 external independent review: issue #573 / PR #585, round 2 (delta `4f746408..08374721`)

- Exact head: `08374721d958b32ade38e7e62d25a7ccea215119`, tree `b852bb03617b6cdfda344ae8a791868ab0f3e835`. Source base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
- Round: R341-2, cleared context, external reviewer. This is a delta review. Round R341-1 covered `4f746408` in full; this round judges the five commits `2a15d68b`, `71b614ba`, `d20eeb89`, `5cf31b2c` and `08374721`. All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #573-#576 issue bodies and the round-2 assignment and decision (#573 comment 5854262940);
  - the executor's REVIEW READY comment (5854525373) and the current PR body;
  - the diff and history `e0920d77..08374721`;
  - the published evidence tree `265f00ea:review-evidence/573-r1`;
  - clause text this round re-extracted from Milan v1.2 (20231130) and IEEE 1722.1-2021 (`receipts/spec_excerpts.txt`).
- The prior public review (R340-1) was read only after this round's verdict and ledger were fixed (`receipts/verdict_before_prior_read.txt`).

## Verdict summary

Every round-1 finding is closed at this head, with executable evidence:

- **Format cap.** The cap is now 46. It is derived in one place (`avdecc/aem_descriptors.py:273-276`) from the 2021 layout: descriptor maximum 508, formats at 138, 8-octet entries. It is not restated anywhere else.
- **Listener buffer.** Listener buffers above the packed u32 maximum are refused. `0xFFFFFFFF` packs equal; `2^32`, `2^32+2125999`, `4294968296` and `2^33` are refused.
- **Clause citations** now name Milan v1.2 5.3.3.1 and 5.6.2.
- **ENDSTATION_BUILDER.md:443** is corrected.

Other results at this head:

- The rerun round-1 scripts all give the expected results.
- Both round-1 mutant banks are fully killed: 30/30, and 26/26 of the applicable cases. All 12 round-2 reviewer mutants are killed.
- No tracked configuration is refused. All five configurations' artifacts are byte-identical to `e0920d77`: 80/80 and 85/85 files across two independent inventories, the three Arty configurations included.

The verdict is NEGATIVE because two MINOR findings are open:

- **R341-2-F1 (MINOR):** unquoted hex EUI-64 scalars made only of digits are still silently reinterpreted. For some spellings this is newly wrong at this head, and the documentation now says it cannot happen.
- **R341-2-F2 (MINOR):** the matrix's Processor L4 probe row, edited in this delta, and the parent audit probe it cites still present 47 as the Table 7-8 boundary.

## Findings

### R341-2-F1 - MINOR - Conformance, Robustness, Tests, Docs - `sw/builder/endstation_builder.py:1331` (`_eui64`); `sw/builder/README-parameters.md:152`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:196`; `sw/builder/test_declarations.py:69-86` - an unquoted hex EUI-64 made only of digits is silently reinterpreted

- **Authority/evidence:**
  - The frozen round-2 decision (#573 comment 5854262940, item R341-1 S1) says: "an unquoted YAML hex EUI-64 must parse to the value written, or be refused with a message telling the user to quote it. Never a silent reinterpretation. Test both."
  - The builder's EUI-64 parser reads a string as hexadecimal with or without `0x`, so bare hex such as `001BC50AC1000005` is an accepted spelling.
  - The new line 1331, `n = v if type(v) is int else int(str(v), 16)`, takes any YAML integer at its YAML value. YAML resolves an unquoted run of digits as decimal, or as octal when it has a leading `0`.
  - `receipts/scalar_spelling_head.jsonl` shows the result at this head, the same for `entity_model_id`, `model_id_pin` and `entity_id`:

    | Written text | Quoted resolves to | Unquoted resolves to |
    |---|---|---|
    | `1000000000000005` | `0x1000000000000005` | `0x00038D7EA4C68005` |
    | `0010000000000001` | `0x0010000000000001` | `0x0000008000000001` |
    | `10` | `0x10` | `0x0A` |

  - None of these is refused.
  - At base (`receipts/scalar_spelling_base.jsonl`), `1000000000000005` and `10` resolved correctly quoted and unquoted. The head fixes the `0x` spelling but introduces this mismatch.
  - The same parser also serves `_fmt64`: the stream `formats`, `crf_format` and `crf_output.format` words (lines 1414 and 1438), `entity.entity_id` (line 3617) and `srp.stream_dmac_base` (line 2028).
  - The new controls (`test_declarations.py:80`) exercise only the `0x001BC50AC1000005` spelling.
  - README-parameters.md:152 says "Quoted and unquoted hexadecimal EUI-64 values retain their numeric value", and matrix line 196 and the PR body make the same claim. For these spellings the claim is false.
- **Impact:**
  - A configuration that writes an identity or format word as an unquoted digit-only hex value silently emits a different `entity_model_id`, `entity_id` or format word in ENTITY, ADP and the firmware constants.
  - This is the "silent reinterpretation" the decision forbids.
  - The value passes the reserved-value guard, so no refusal reveals it.
  - Tracked configurations quote every such value and are unaffected (`receipts/shipping_*.sha256`). That is why this is MINOR.
- **Required outcome:** every YAML scalar accepted by the EUI-64 parser must either resolve to the hexadecimal value of its written text, identical quoted and unquoted, or be refused with a named `ConfigError` telling the user to quote it. This covers at least `entity_model_id` and `model_id_pin`, and the other fields sharing the parser. Examples of the remedy are a loader that preserves these scalars' text, or refusing YAML integers that are not provably `0x`-spelled. The README and matrix sentences must then state what is enforced.
- **Verification:**
  - Declaration controls for the three spellings above, quoted and unquoted, show equality or the named refusal.
  - A mutant that restores the current integer-at-face-value branch is killed.
  - `scripts/scalar_spelling_probe.py` in this packet reports `equal: true` or a refusal for every row.
  - The five-configuration artifact identity is re-shown.

### R341-2-F2 - MINOR - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:166` (Processor L4 probe row); `scripts/audit_pp_descriptors.py:210` - the probe table still presents 47 formats as the accepted Table 7-8 boundary

- **Authority/evidence:**
  - The decision fixes the cap at 46 (IEEE 1722.1-2021 Table 7-8: "The maximum value for this field is 46 for this version of AEM"; 7.2: "maximum length of a descriptor shall be 508 octets").
  - It requires the matrix L4 rows to state the enforced bound.
  - This delta edited row 166 only in its result column, to "576-byte buffer is not the 46-format cap". The row's "Accepted control or boundary" column still reads "47-entry size 514", and its "One invalid change" column reads "48-entry size 522".
  - The parent audit probe that produces the row is still labelled `"47 formats at Table 7-8 cap"`, and at this head it reports `accepted` (`receipts/audit_pp_descriptors_L4_head.txt`).
  - Line 62 of the same document now says 47-entry declarations refuse.
- **Impact:**
  - The row is internally inconsistent and contradicts line 62.
  - A cold reader is told that a 514-octet, 47-format STREAM descriptor is the legal boundary and that 48 is the first invalid change. Both are non-conforming under the 2021 layout.
  - The parent-owned script also labels the 2013 figure as the Table 7-8 cap.
  - The processor-owned "N <= 47" wording is correctly left to processor issue 60. This row and the probe label are parent-owned.
- **Required outcome:**
  - The row names the 46-entry, 506-octet descriptor as the boundary, and 47 as an invalid change that the processor packer accepts. Alternatively, it attributes 47 explicitly to the processor contract under processor issue 60, and not to Table 7-8.
  - The parent probe label no longer calls 47 the Table 7-8 cap.
- **Verification:** a text check of both locations. The descriptor audit and the docs gates exit 0.

### SUGGESTION (does not affect coverage)

- **R341-2-S1 - SUGGESTION - Robustness - `avdecc/aem_descriptors.py:187-189` (`be32`):** every other AEM u32 field is still truncated silently by the `& UINT32_MAX` mask. The listener buffer is now bounded before it reaches this point, so nothing shipping is affected. A range check that raises inside `be32`, `be16` and `be64` would make any future caller's overflow visible.

## Round-1 findings: disposition at this head

| Round-1 finding | Disposition | Evidence at `08374721` |
|---|---|---|
| R341-1-F1 MAJOR (Conformance, Robustness, Tests, Docs): 47 is the 2013 cap; the 2021 layout caps `number_of_formats` at 46 | **CLOSED** | See the evidence list after this table. |
| R341-1-F2 = R340-F1 MAJOR (Conformance, RTL, Robustness, Tests): listener floor bypassed by 32-bit truncation | **CLOSED** | `endstation_builder.py:1388-1391` refuses values above `UINT32_MAX`. The bound is imported from `aem_descriptors.py:183-184`, where it is derived from the `>I` encoding that `be32` uses. `receipts/buffer_wrap_probe_head.txt` is R340's script, rerun unchanged. It reports 2126000 and `0xFFFFFFFF` accepted and packed equal, 2125999 refused under the floor, and `2^32` and `2^32+2125999` refused under the width rule. `bypass_probes_head.jsonl`: `4294968296`, `4297093296` and `8589934592` are refused, and talkers are unchanged. The declaration test reads the packed STREAM_INPUT field at offset 128 at all eight listener indices. Mutants R2-M4 (bound removed), R2-M5 (exclusive), R2-M6 (+1), R2-M7 (talkers too) and R2-M8 (bound 2^32) are killed. |
| R341-1-F3 = R340-F3 MINOR (Conformance, Docs): reserved model-ID clause | **CLOSED** | The clause text was re-extracted this round: Milan v1.2 5.3.3.1 and 5.6.2 carry "neither all zeros nor all ones", and 5.3.1 carries only evolution (`receipts/spec_excerpts.txt`). The refusal message (`endstation_builder.py:1345`), `README-parameters.md:153-154`, the test docstring and comment (`test_declarations.py:36,46`), the matrix L9 row (`PP_DESCRIPTOR_OWNERSHIP.md:67`, "5.3.3.1/5.6.2 validity, 5.3.1 evolution") and `ENDSTATION_BUILDER.md:444` all cite them correctly. |
| R340-F2 MINOR (Docs): `ENDSTATION_BUILDER.md:443` said reserved IDs pass | **CLOSED** | Lines 443-444 now describe the enforced refusal. A grep of `docs/` and `sw/` finds no remaining acceptance claim. |
| R340-S1 SUGGESTION (Tests): CRF-output arm observable only by precedence | Taken; closed | `test_declarations.py:236-244` calls `_validate_output_clock_sources` directly. The round-1 mutant "CRF output arm removed" is now killed with "CRF output accepted without INTERNAL" in both banks. |
| R340-S2 SUGGESTION (Robustness): empty `media_clock_sources` raised `IndexError` | Taken; closed | `endstation_builder.py:3841-3844` raises a named L6 refusal citing Milan 5.3.3.6. R340's probes move from `crashed:IndexError` to refused, `[internal]` is still accepted (`r340_probes_head.log`), and R2-M9 is killed. |
| R340-S3 SUGGESTION (Robustness): literal shadowed by a pin | Taken for the assigned part; closed | `endstation_builder.py:4373` validates the literal first. The zero literal under a legal pin is now refused (`r340_probes_head.log`), and R2-M10 is killed. The note's secondary remark, that an ignored `crf_output.formats` key is tolerated, was outside the decision. It is unchanged and remains a candidate issue. |
| R341-1-S1 SUGGESTION (Robustness): unquoted YAML hex EUI-64 reparsed | Taken for the `0x` spelling (`bypass_probes_head.jsonl`: unquoted `0x001BC50AC1000005` resolves to itself; R2-M12 is killed) | **Not met for digit-only spellings**, and those regressed: see **R341-2-F1**. |
| R341-1-S2 SUGGESTION (Conformance): hash arm outside the guard | Taken; closed | `endstation_builder.py:4377`. The test patches `derive_model_id` to both endpoints and gets the named refusal. R2-M11 is killed. |

Evidence for closing R341-1-F1:

- `aem_descriptors.py:272-276` derives `MAX_STREAM_FORMATS = (508 - 138) // 8 = 46`. `d_stream` now packs `formats_offset` and `redundant_offset` from the same constants (lines 307 and 314).
- The builder imports the cap (`endstation_builder.py:124`) and no longer restates a literal. A repository grep finds no other parent definition.
- `receipts/format_cap_length_head.txt` is this reviewer's round-1 script, rerun unchanged. It prints 46 final entries accepted, 506 octets, offset 138 and N=46. It then exits 1 on the named `ConfigError` for 47, "format count 47 exceeds 46". The script has no refusal handler, so exit 1 at 47 is the corrected behaviour and not a failure.
- `bypass_probes_head.jsonl`: a listener with 45 declared entries plus 1 derived is accepted with N=46. With 46 declared plus 1 derived it is refused.
- `r340_probes_head.log`: a talker with 47 entries is refused.
- Mutants R2-M1 (cap+1 at the use site), R2-M2 (maximum 516, giving 47) and R2-M3 (2013 offset 132) are killed.
- The README (`README-parameters.md:128`), matrix L4 row 62, F3 row 243, the probe row 179, the code comment and the message all say 46. The one remaining 47 is in row 166; see R341-2-F2.

## Executable evidence (this packet)

- `receipts/head_test_declarations.txt`: `sw/builder/test_declarations.py` passes at head, exit 0.
- Round-1 scripts rerun unchanged against a disposable copy of the exact head:
  - `bypass_probes_head.jsonl`;
  - `format_cap_length_head.txt`;
  - `buffer_wrap_probe_head.txt`;
  - `r340_probes_head.json` and `.log` (37 probes; the changes from round 1 are the closed items above, plus unquoted `0x` CRF words now accepted correctly);
  - `r341_round1_mutants_head.json`: 26/26 applicable cases killed. R-M8 and R-M14 target the removed literal, report `applied: false`, and are replaced by R2-M1..M3. The restored control exits 0.
  - `r340_round1_mutants_head.json` and `.log`: 30/30 killed, the control passes, and the source is restored byte-identical.
- `r2_mutants_head.json`: 12/12 round-2 reviewer mutants killed across `endstation_builder.py` and `aem_descriptors.py`. Both files are restored and the control exits 0. The script and cases are `scripts/run_mutants_r2.py` and `scripts/reviewer_mutants_r2.json`.
- Artifact identity:
  - `shipping_base.sha256` equals `shipping_head.sha256` (80 files: builder CLI output, AEM store, AEM image, and tracked generated headers).
  - `r340_artifacts_base.json` equals `r340_artifacts_head.json` (85 artifacts).
  - All five tracked configurations are accepted, including `arty_current`, `arty_4x4` and `arty_8ch`.
- `focused_gates_head.txt`, all exit 0:
  - Python idiom, doc style, doc paths and docs_check;
  - em-dash against `e0920d77` and TOC check/anchors, both with the pinned renderer;
  - descriptor audit and AEM store self-test.
- `scalar_spelling_base.jsonl` and `scalar_spelling_head.jsonl`: the R341-2-F1 reproduction (`scripts/scalar_spelling_probe.py`).
- `hosted_checks_08374721.tsv`: hosted runs read at one instant (09:20 UTC).
  - Succeeded: Yosys shards 0-3, verilator-lint, bdd-conformance, wire-accountability, full-ci-gate and docs-check-no-git.
  - In progress: Verilator shards 0, 1, 2 and 4, yosys-elaboration, elaborate and docs-check.
  - Skipped: "Physical gPTP". A skip is not execution.
- `clone_integrity_final.txt`: the review clone is at the exact head. The index tree equals `b852bb03`, the index hash equals the pre-probe record, the worktree and submodules are clean, and the gitlinks `efeb541a`, `5dce647a`, `0922e434` and `48ff7a7e` are unchanged.

## Reviewer-owned completion ledger (this round)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R341-2-F1 MINOR open) | Checked against Milan v1.2 5.3.3.1, 5.3.3.4, 5.3.3.6 and 5.6.2 and IEEE 1722.1-2021 7.2 and Table 7-8, re-extracted (`receipts/spec_excerpts.txt`), and against decision 5854262940 item by item. Code: `avdecc/aem_descriptors.py:182-189,272-276,307,314`; `sw/builder/endstation_builder.py:124,1329-1346,1385-1403,3840-3844,4368-4380`. Receipts: `bypass_probes_head.jsonl`, `buffer_wrap_probe_head.txt`, `format_cap_length_head.txt`, `r340_probes_head.log`, `scalar_spelling_head.jsonl`. | R341-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| RTL | CLEAN | Scope and bytes: `receipts/delta_diffstat.txt` (no `hdl/`, `.sv` or gitlink change in the delta); `clone_integrity_final.txt` (gitlinks unchanged); `shipping_base.sha256` = `shipping_head.sha256` (generated RTL inputs `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_table.svh`, `lwsrp_csr_defaults.svh` and `gptp_ucode.hex` byte-identical for all five configurations). Widths: the `be32` refactor at `aem_descriptors.py:183-189` keeps the same `>I` encoding and mask. The listener `buffer_length` 32-bit field can no longer truncate (`buffer_wrap_probe_head.txt`; R2-M8 killed). The 46-format STREAM descriptor is 506 octets, within the 508 maximum (`format_cap_length_head.txt`). The round-1 truncation attribution under this lens is closed. | R341-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Robustness | UNCLEAN (R341-2-F1 MINOR open) | Maxima and wrap (`bypass_probes_head.jsonl`, `buffer_wrap_probe_head.txt`); derived entries at 45+1 and 46+1; empty, null and `[internal]` source lists; shadowed literal; hash-arm endpoints; talker isolation (0, -5, 2^32, string); YAML scalar spellings quoted and unquoted at base and head (`scalar_spelling_*.jsonl`); 37 R340 probes (`r340_probes_head.log`) | R341-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Tests | UNCLEAN (R341-2-F1 MINOR open: the scalar controls cover only the `0x` spelling, so the digit-only regression passes) | `sw/builder/test_declarations.py:35-125,127-205,229-262,301-306` run through its entry point (`head_test_declarations.txt`, exit 0; wired as builder gate 40). 30/30 + 26/26 + 12/12 mutants killed with passing restored controls (`r340_round1_mutants_head.json`, `r341_round1_mutants_head.json`, `r2_mutants_head.json`). Packed-byte assertions read the image directory independently (offset 128; offsets 82/84 and length 506). | R341-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |
| Docs | UNCLEAN (R341-2-F1 MINOR and R341-2-F2 MINOR open) | `sw/builder/README-parameters.md:117-156`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:62,64,67,166,179,193-197,241-243`; `docs/ENDSTATION_BUILDER.md:436-448`; code comments at `aem_descriptors.py:182,272`; the PR body at read time; `receipts/audit_pp_descriptors_L4_head.txt`; `focused_gates_head.txt` (all docs gates exit 0) | R341-2 | 08374721d958b32ade38e7e62d25a7ccea215119 |

At this head, RTL is covered clean by R341-2. Conformance, Robustness, Tests and Docs are not.

A corrected head must re-cover every lens whose scope its change touches:

- Conformance, Robustness, Tests and Docs for F1;
- Docs for F2;
- RTL as well, if the change reaches any descriptor-packing code.

## Real limits

- The clause text comes from a local PDF text extraction of Milan v1.2 (20231130) and IEEE 1722.1-2021. Only short excerpts are published.
- As the brief directs, these were not run: the full parent, processor, gPTP, Yosys and builder banks, Docker/act, the host act runner and hardware. The manager's full source banks at this head are their public evidence, not this round's.
- "The Arty configurations keep building" is verified here as builder, store and image generation succeeding byte-identically for all three Arty configurations. It is not verified as a bitstream or elaborate job.
- This Python-only delta needed no simulation, so the scoped Verilator was not used and its identity was not checked.
- The hosted checks were read once, at 09:20 UTC, while several jobs were still in progress.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- This round did not validate the final current-dev candidate.
- All probes and mutations ran in disposable copies under the unpublished `scratch/`.

## Pending manager duties

- Publish this report.
- Route R341-2-F1 and R341-2-F2 to the executor. R341-2-S1 and the remainder of R340-S3 (the ignored `crf_output.formats` key) are optional new-Issue candidates.
- Hosted and act acceptance at the exact head of any corrected commit, and the candidate-merge build against live `dev` at the merge turn.
- Processor-owned "N <= 47" wording remains with processor issue 60, as decided.
- A re-review of the corrected head under every lens left unclean here.

R341-2 FINISHED
