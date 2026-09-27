[R341] NEGATIVE - exact head 4f746408a15f494c4b30bdc9add6d7295309dff9

# R341-1 external independent review: issue #573 / PR #585 (F1-F4 parent shipping-model refusals)

- Exact head: `4f746408a15f494c4b30bdc9add6d7295309dff9`, tree `432897b634f661042e67cf390513fae6356542ba`.
- Source base: `e0920d77162284d8da52ffaf13a973e451e44f90` (four commits, one per issue #573, #574, #575, #576).
- Round: R341-1, cleared context, external reviewer. Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 2.2, 3, 5, 6), docs/README.md, issue bodies #573-#576, the assignment comment on #573 (5853854503), the executor's TAKEN and REVIEW READY comments, the PR body, `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`, the diff `e0920d77..4f746408`, the published evidence tree `265f00ea:review-evidence/573-r1`, and the governing clauses read directly in Milan v1.2 and IEEE 1722.1-2021 (short excerpts in `receipts/spec_excerpts.txt`).

## Verdict summary

The four refusals exist, raise the named `ConfigError`, sit in the parent configuration path, and are exercised by the builder's own entry point (`sw/builder/test_builder.py` imports `test_declaration_contracts`, gate 40). All 14 published removed-check mutants and 14 reviewer mutants are killed. All five tracked configurations still build, and their 80 generated artifacts (builder outputs, AEM store, AEM image and the tracked generated header) are byte-identical at base and head, the Arty configurations included.

The verdict is NEGATIVE because four findings remain open:

- **R341-1-F1 (MAJOR).** The new format-count cap is 47. The authority it cites, IEEE 1722.1-2021 Table 7-8, sets 46. At 47 the builder accepts and emits a 514-octet STREAM descriptor, above the 508-octet maximum in IEEE 1722.1-2021 7.2.
- **R341-1-F2 (MINOR).** The new listener buffer floor can be bypassed by 32-bit wraparound. The loader accepts 4294968296 ns, and the packed STREAM_INPUT carries `buffer_length=1000`.
- **R341-1-F3 (MINOR).** The reserved model-ID refusal cites Milan v1.2 5.3.1 and IEEE 6.2.2.8. Neither clause states the zero/all-ones rule. Milan v1.2 5.3.3.1 (ENTITY) and 5.6.2 (ADPDUs) state it.
- **R340-F2 (MINOR), retained from the prior round and verified here.** `docs/ENDSTATION_BUILDER.md:443` still says zero and all-ones identities pass.

All five lenses are UNCLEAN at this head. RTL was first recorded CLEAN. After reading the prior round, this round attributed F2's 32-bit field truncation to RTL as well, and the change is disclosed in the prior-findings section.

## Findings

### R341-1-F1 - MAJOR - Conformance, Robustness, Tests, Docs - `sw/builder/endstation_builder.py:1197` (`MAX_STREAM_FORMATS = 47`); `sw/builder/test_declarations.py:104-107`; `sw/builder/README-parameters.md:126`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:62,241` - the format-count cap exceeds the cited IEEE 1722.1-2021 bound

- Authority/evidence:
  - IEEE 1722.1-2021 Table 7-8, `number_of_formats`, says "The maximum value for this field is 46 for this version of AEM", with `formats_offset` 138.
  - IEEE 1722.1-2021 7.2 says "The maximum length of a descriptor shall be 508 octets".
  - The value 47 belongs to IEEE 1722.1-2013, where `formats_offset` is 132 (132 + 8*47 = 508).
  - Milan v1.2 binds IEEE 1722.1-2021 as [ATDECC]. This repository packs the 2021 layout: `avdecc/aem_descriptors.py:295` writes `formats_offset` 138, and `AEM_LAYOUT_REV` records the move to 2021.
  - The code comment, the error message, the README and the matrix all cite "IEEE 1722.1-2021 Table 7-8" for 47. `receipts/spec_excerpts.txt` quotes both editions.
- Executable evidence:
  - `receipts/format_cap_length_head.txt`: at head, a talker with 47 final formats is accepted by `load_config`, the image packer accepts it, and the STREAM_OUTPUT descriptor is 514 octets with `number_of_formats` 47. At 46 formats it is 506 octets.
  - `receipts/bypass_probes_head.jsonl`: a listener with 46 declared formats reaches 47 after the derived family entry, and is accepted with `number_of_formats` 47.
  - The processor packer accepts both 47 and 48 (`scripts/audit_pp_descriptors.py` run at head, exit 0 in `receipts/focused_gates_head.txt`; its probes "47 formats at Table 7-8 cap" and "48 formats below line-buffer cap" both report `accepted`, and the raw JSON stays in unpublished scratch), so this builder check is the only guard.
  - Reviewer mutant R-M14, which sets the cap to 46, is "killed" by the test itself because `test_stream_format_contract` requires 47 final entries to be accepted (`receipts/mutants_head_4f746408.json`). The test therefore pins the non-conforming boundary rather than the clause.
- Impact: an accepted configuration can generate a STREAM descriptor that is non-conforming in two ways: `number_of_formats` is above the Table 7-8 maximum, and the descriptor is longer than the 508-octet maximum. The refusal the PR adds is documented as enforcing the Table 7-8 bound, so the documentation states a guarantee the code does not provide. No shipping image is affected, because every tracked list has one or two entries.
- Origin: the 47 figure predates this lane. It comes from the #509 ownership matrix ("47-format cap"), the processor contract (`protocol-processor/docs/architecture/07_memory_maps.md:86`, "N formats <= 47"), and the assignment text. AGENTS.md section 2 requires such a conflict between the task text and the normative requirement to be published for a decision, not settled privately. This review publishes it.
- Required outcome:
  - The parent cap matches the bound of the layout actually packed: 46 for IEEE 1722.1-2021, counted on the final list including derived listener entries. Alternatively, a maintainer decision is recorded publicly that explains why a different figure is conforming.
  - The README, the matrix L4 and F3 rows, and the code comment/message state the bound that is enforced.
  - The processor-owned statements (`07_memory_maps.md` L4 and the compliance review's REQ-MDL-003) are reported to their owner (processor issue 60), not edited in this lane.
- Verification:
  - Declaration controls accept 46 final entries in both directions and refuse 47. For a listener, 45 declared plus 1 derived is accepted, and 46 declared plus 1 derived is refused.
  - A mutant that raises the cap by one is killed.
  - The five-configuration artifact identity is re-shown.

### R341-1-F2 - MINOR - Conformance, RTL, Robustness, Tests - `sw/builder/endstation_builder.py:1382-1390` (`_stream_buffer_ns`); `avdecc/aem_descriptors.py:182-184,299` (`be32` masks to 32 bits); `sw/builder/test_declarations.py:77-86` - a listener buffer declaration can pass the floor and still emit a value below it

- Authority/evidence:
  - Milan v1.2 5.3.3.4 says: "In a STREAM_INPUT descriptor, the buffer_length field shall contain a valid value and this value shall be greater than or equal to 2126000 ns".
  - IEEE 1722.1-2021 Table 7-8 defines `buffer_length` as 4 octets.
  - `_stream_buffer_ns` checks only `type is int` and `>= 2126000`. `be32` silently applies `& 0xFFFFFFFF`.
  - `receipts/bypass_probes_head.jsonl`:
    - `buffer_length_ns=4294968296` is ACCEPTED, and the packed STREAM_INPUT has `buffer_length` 1000.
    - `4294967296` is ACCEPTED and packs as 0.
    - `8589934592` is ACCEPTED and packs as 0.
    - `4294967295` is accepted and packs unchanged.
  - The test has no upper-boundary control.
- Impact: the matrix and PR state that every listener buffer below the floor is refused before generation (#574). A declaration that passes the new check can still produce a STREAM_INPUT whose emitted `buffer_length` is below the Milan floor. That is a bypass of the refusal through an alternate value. It is rated MINOR only because the triggering declaration (above 4.29 s) is implausible in practice.
- Required outcome: a named `ConfigError` refuses a listener `buffer_length_ns` that the 32-bit `buffer_length` field cannot represent, with the bound derived from the field width, so no accepted listener declaration can emit a value below the floor. Talker behaviour stays unchanged, as the issue requires.
- Verification: declaration controls accept `4294967295` and refuse `4294967296` (and a wrapped value such as `4294968296`) at every listener index. A mutant removing the upper arm is killed.

### R341-1-F3 - MINOR - Conformance, Docs - `sw/builder/endstation_builder.py:1347`; `sw/builder/README-parameters.md:147`; `sw/builder/test_declarations.py:35,45`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:67` (L9 clause column) - the reserved model-ID rule cites clauses that do not state it

- Authority/evidence:
  - Milan v1.2 5.3.1 is "Introduction" of the Entity model. It states only that a changed static model reports a different Entity Model ID, which is the evolution rule.
  - IEEE 1722.1-2021 6.2.2.8 states uniqueness and evolution.
  - The rule "The entity_model_id field shall be a valid EUI-64 (neither all zeros nor all ones)" is in Milan v1.2 5.3.3.1 (ENTITY) and repeated in 5.6.2 (ADPDUs). See `receipts/spec_excerpts.txt`, lines 1416, 1457, 1461, 5365 and 5368 of the extraction.
  - CONTRIBUTING.md section 6 requires compliance references to cite the specification clause. The README line reads "Milan v1.2 5.3.1 reserves both endpoint values", which is not what that clause says.
- Impact: the user-visible refusal message and the parameter guide send a reader to a clause that does not contain the rule. A cold reviewer checking the citation finds no basis for the refusal there. Behaviour is correct.
- Required outcome: the refusal message, parameter guide and test docstring/comment cite Milan v1.2 5.3.3.1 (and 5.6.2 for the ADPDU field). The L9 row keeps 5.3.1 only for evolution, if at all.
- Verification: text check of the four locations, and the declaration run still passes. `_refused` matches the rule text "must not be zero or all ones", not the clause number.

### SUGGESTIONS (do not affect coverage)

- **R341-1-S1 - SUGGESTION - Robustness - `sw/builder/endstation_builder.py:1331-1338` (`_eui64`, pre-existing):** an unquoted YAML hex EUI-64 is parsed by YAML as an integer and then reparsed as hex digits of its decimal string. Unquoted `entity_model_id: 0x001BC50AC1000005` silently resolves to `0x7816474349535237` at both base and head (`receipts/bypass_probes_*.jsonl`). Not introduced by this PR, and the reserved-ID check still applies to the resolved number: unquoted `0x0` and `0` are refused at head. Worth a separate Issue.
- **R341-1-S2 - SUGGESTION - Conformance - `sw/builder/endstation_builder.py:4366-4367`:** the hash-derived arm is not passed through `_model_id`.
  - The all-ones result is unreachable, because `_vendor_oui` refuses the I/G bit.
  - Zero requires `vendor_oui: 0x000000` together with a 40-bit hash of zero, which is negligible but not excluded by construction.
  - Routing the resolved ID through one guard would make "every entity_model_id" true by construction.

## Per-issue verification at the exact head

| Issue | Required evidence (frozen) | Reviewer result |
|---|---|---|
| #573 F1 | Legal ID accepted; zero and all ones refused on literal and pinned forms; ENTITY/ADP equality | Met. `test_model_id_contract` accepts `...01`, `...FE` and a legal OUI ID on both keys. It compares ENTITY bytes at offset 12 of the packed image and the `MILAN_MODEL_ID_HI/LO` firmware constants, and refuses four endpoint cases with the named message. Author mutants 1-4 and R-M13 are killed. Clause citation is wrong (F3). |
| #574 F2 | 2126000 accepted, 2125999 refused; talkers unaffected; images unchanged | Met at the floor at all eight ax7101_8x8 listener indices, with non-integer, string and bool refused. Mutants R-M2..R-M5 are killed. Talkers accept 0/1/-5 unchanged from base. Upper wraparound bypass: F2. |
| #575 F3 | Count bound, AAF/CRF family, Milan CRF word; final list incl. derived entries; 48, mixed and altered each refused independently; inputs and outputs | Family and CRF word: met in both directions, each with its own message. Mutants R-M1 (validate-before-derivation), R-M6, R-M7, R-M9 and R-M10 are killed. The count is checked on the final list, and derivation is counted (R-M1 killed; 46 declared becomes 47 final, accepted). The bound value is wrong (F1). CRF with the sink disabled is also refused, which is stricter and has no shipping effect. |
| #576 F4 | INTERNAL+CRF accepted (either selected); CRF-only outputs refused; input-only preserved | Met. The AAF-output and CRF-output arms are each killed by their own case, and R-M11 (selection instead of availability) and R-M12 are killed. Default sources and `[crf, internal]` are accepted. `_load_clocking` still accepts CRF-only. |
| All | Named `ConfigError`, never assert; parent path; no processor change; no shipping change | Met. There are no `assert` statements in the new production code, and there is no gitlink or `protocol-processor/` change. The 80/80 artifacts are identical (`receipts/shipping_base_e0920d77.sha256` vs `receipts/shipping_head_4f746408.sha256`). |

## Reviewer-owned completion ledger (this round)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR, F3 MINOR open) | `endstation_builder.py:1197,1341-1348,1382-1414,4214-4226,4366-4371` against Milan v1.2 5.3.3.1, 5.3.3.4, 5.3.3.6, 5.6.2, 7.3.2/7.3.4 Table 7.1 and IEEE 1722.1-2021 7.2, 6.2.2.8, Table 7-8; `receipts/spec_excerpts.txt`, `format_cap_length_head.txt`, `bypass_probes_head.jsonl` | R341-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| RTL | UNCLEAN (F2 open: 32-bit `buffer_length` truncation at the descriptor-image field, `avdecc/aem_descriptors.py:182-184,299`; attribution added after reading R340-1, disclosed below) | `receipts/commit_files.txt` (the diff touches only the builder, its test and two docs; no `hdl/` file and no gitlink); `receipts/clone_integrity_final.txt` (gitlinks `0922e434` / `5dce647a` / `48ff7a7e` / `efeb541a` unchanged). Generated RTL inputs `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_table.svh` and `lwsrp_csr_defaults.svh` are byte-identical for all five configurations (`shipping_*.sha256`). `ADP_CRF_FMT_C` / `ADP_CRF_OUT_FMT_C` (`endstation_builder.py:3021-3031`) read the normalized clocking that `_crf_format` now constrains. No module or interface contract changes. | R341-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Robustness | UNCLEAN (F1 MAJOR, F2 MINOR open) | `receipts/bypass_probes_head.jsonl` and `bypass_probes_base.jsonl` (maxima, wraparound, derived entries, disabled CRF sink, default and reversed sources, YAML scalar forms, talker isolation); `mutants_head_4f746408.json` | R341-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR open) | `sw/builder/test_declarations.py:24-168` run through its own entry point (`receipts/head_test_declarations.txt`, exit 0). Wired at `sw/builder/test_builder.py:27557-27562`, and the hosted docs-check (`.github/workflows/docs.yml:205`) runs it. 28/28 mutants are killed, with a passing restored control (`mutants_head_4f746408.json`). R-M14 shows the test pins 47. There is no upper buffer boundary control. | R341-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Docs | UNCLEAN (F1 MAJOR, F3 MINOR, retained R340-F2 MINOR open) | `sw/builder/README-parameters.md:117-131,146-147`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:1-4,62,64,67,166-195,233-243`; `docs/ENDSTATION_BUILDER.md:436-448` (read after the prior round, R340-F2); PR body; `receipts/focused_gates_head.txt` (docs_check, doc_style, doc_paths, em-dash, TOC, anchors, py idiom, descriptor audit, store self-test: all exit 0) | R341-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |

No lens is covered clean by this round. A corrected head must be re-covered under every lens its change touches, and under every lens left unclean here.

Every other statement in the new README and matrix text matches the enforced behaviour: INTERNAL availability versus selection, CRF-only input loading, family separation, both CRF words, the derived-entry count, the integer floor, and the probe-table refusals. They were checked against the probes and mutants above.

## Prior public review findings on this PR

This round read the public review record on PR #585 only after the verdict and ledger above were written (`receipts/pr585_public_comments_after_verdict.txt`). The one prior review is the internal round R340-1 (`[R340] NEGATIVE`, same exact head). The PR has no GitHub reviews and no inline comments. Disposition at `4f746408` follows.

| Prior finding | Disposition at this head | Evidence |
|---|---|---|
| R340-F1 MAJOR (Conformance, RTL, Robustness, Tests): listener buffer floor bypassed by 32-bit truncation | **RETAINED, open.** Reproduced independently as R341-1-F2. R340's `2^32 + 2125999 -> 2125999` agrees with the same mask arithmetic, and this round's `2^32 + 2126000` packs as `2126000`. Severity: R340 rates it MAJOR and this round rated it MINOR independently. The higher rating governs the merge bar, and either rating leaves the same lenses unclean. **Lens update disclosed:** after reading R340-1, this round adds RTL to F2, because the RTL lens's width/truncation bullet applies to the 32-bit descriptor field the processor serves. RTL is therefore UNCLEAN in the ledger below, replacing the CLEAN entry written before the read. | `receipts/bypass_probes_head.jsonl` |
| R340-F2 MINOR (Docs): `docs/ENDSTATION_BUILDER.md:443` still says zero and all-ones identities pass | **RETAINED, open; verified at this head.** The line reads "Zero and all-ones identities also pass the numeric-width check.", but `_model_id` refuses both on both forms. This round's independent pass missed it. It adds to the Docs lens, which was already UNCLEAN. | `docs/ENDSTATION_BUILDER.md:443`; `receipts/bypass_probes_head.jsonl` (F1 rows); `receipts/head_test_declarations.txt` |
| R340-F3 MINOR (Conformance, Docs): clause for the reserved-model-ID rule unresolved | **RETAINED, open. Its open question is RESOLVED by clause text:** Milan v1.2 5.3.3.1 and 5.6.2 carry the rule, and 5.3.1 does not. The required change is now determinate (R341-1-F3). | `receipts/spec_excerpts.txt` |
| R340-S1 SUGGESTION (Tests): CRF-output arm is observable only as refusal precedence | Agreed, and it does not affect coverage. A full load always carries a talker. `test_declarations.py:166` calls the helper directly only for the no-output case. | `receipts/mutants_head_4f746408.json` (author "CRF output arm removed" is killed by message only) |
| R340-S2 SUGGESTION (Robustness): empty `media_clock_sources` raises `IndexError` | Verified at head. It predates the PR and does not affect coverage. | `receipts/r340_s2_check_head.txt` |
| R340-S3 SUGGESTION (Robustness): shadowed literal under a pin | Not re-probed by this round. It does not affect coverage. | none |

**New in this round and absent from R340-1:** R341-1-F1 (format cap 47 versus 46). R340-1's per-issue table accepted the 47 cap on the strength of `protocol-processor/docs/architecture/07_memory_maps.md:201`. That document's own worst case, `138 + 8*47 + 2*8 = 530 B`, is above the 508-octet descriptor maximum of IEEE 1722.1-2021 7.2.

## Real limits

- Clause reading used the locally held Milan v1.2 consolidated (20231130), IEEE 1722.1-2021 and 1722.1-2013 texts through a PDF text extraction. Only short excerpts are published.
- Not run, as the brief directs: the full parent, processor, gPTP, Yosys and builder banks, Docker/act, and the hosted replica. Only focused commands ran in disposable copies of this head and of base `e0920d77`.
- The artifact comparison covers each configuration's builder CLI output directory, `gen_aem_store --overlay` and `gen_aemi_image --overlay`, as 80 files. It does not include the builder's in-memory `sweep_opts` string, which the published author inventory counted separately (85).
- Hosted checks were read at one instant (`receipts/hosted_checks_4f746408.tsv`). Verilator shards 1, 2 and 4 of 5 were still in progress, and "Physical gPTP" was skipped. That is not execution evidence.
- No simulation was needed for this Python-only diff, so the scoped Verilator was not used and its identity was not checked.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The review clone ends at the exact head with the index equal to the HEAD tree, a clean worktree, clean submodules and unchanged gitlinks (`receipts/clone_integrity_final.txt`). All probes and mutations ran in disposable copies under `scratch/`, which is not published.
- This round did not verify a final current-dev candidate.

## Pending manager duties

- Publish this report and the conflict in F1 on the issue/PR for a maintainer decision (IEEE 1722.1-2021 cap 46 versus the matrix/assignment figure 47). Route the processor-owned "N <= 47" statements to processor issue 60.
- Hosted and act acceptance at the exact head, and the candidate-merge build against live `dev` at the merge turn.
- Route R341-1-F1..F3 and the retained R340-F2 to the executor. Optionally file R341-1-S1/S2 and the prior suggestions as new Issues.
- Re-review of the corrected head under all five lenses, all of which are UNCLEAN here.

R341-1 FINISHED
