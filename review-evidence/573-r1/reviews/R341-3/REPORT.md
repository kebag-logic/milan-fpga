[R341] POSITIVE - exact head 8c956234699b5dec5e6c9aeada651be667974e9b

# R341-3 external independent review: issue #573 / PR #585, round 3 (delta `08374721..8c956234`)

- Exact head: `8c956234699b5dec5e6c9aeada651be667974e9b`, tree `16767fc674e46e4f210feaf6e21dbeb096a76fe3`. Source base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
- Round: R341-3, cleared context, external reviewer. This is a delta review. R341-2 covered `08374721`; this round judges the three commits `9e47e48c`, `0d5820ae` and `8c956234` (`receipts/commit_log.txt`, `receipts/delta_diffstat.txt`). All five lenses were applied: Conformance, RTL, Robustness, Tests and Docs.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the round-3 assignment and decision (#573 comment 5854630094);
  - the executor's REVIEW READY (#573 comment 5854843470), the review-start comment (PR comment 5854921852) and the current PR body (`receipts/executor_manager_comments.txt`, `receipts/pr585_body.txt`);
  - the diff and history `08374721..8c956234`, in the context of `e0920d77..8c956234`;
  - the published author evidence `review-evidence/573-r1/author-r3/` on the evidence branch (read via the API: `gate-results.jsonl`, `evidence-summary.log`, and the builder-present and builder-absent log tails).
- Prior public review text was read only after this round's verdict and ledger were fixed (`receipts/verdict_before_prior_read.txt`, 10:19 UTC). That covers R340-2 (comment 5854625819) and the R340 scripts. The concurrent R340-3 report was not read.

## Verdict summary

Both round-2 MINOR findings are closed at this head, with executable evidence. The round-2 suggestion R341-2-S1 is taken and closed.

**R340-2-F1 = R341-2-F1 (YAML spelling of 64-bit values) is CLOSED.**

- `_eui64` (`sw/builder/endstation_builder.py:1329-1338`) refuses every non-string with `"{ctx}: quote the hexadecimal value as a YAML string"`, then parses the string as hexadecimal.
- All seven keys named in README-parameters reach it: `entity_model_id`, `model_id_pin`, `entity_id`, `srp.stream_dmac_base`, the AAF `formats` entries, `clocking.crf_format` and `clocking.crf_output.format`. They reach it directly or through `_fmt64`, `_model_id` and `_crf_format` (lines 1343, 1352, 1416, 1440, 2030, 3619, 4375, 4377 and 4379). A repository grep finds no other caller.
- The hash arm now passes a string (line 4379), so internal IDs keep the reserved-value guard.
- `receipts/hex_rule_head.jsonl` is this round's 143-row matrix over the eight YAML paths (the AAF format entry once each for talker and listener):
  - quoted `0x…`, quoted unprefixed and quoted underscored hex resolve to the written value;
  - for the identities, the overlay value equals the written value too;
  - unquoted `0x…`, `1234567890123456`, `0012345670123456`, `0`, `18446744073709551615`, `0x_1`, `null`, empty, `true`, `1.5`, `[]` and `{}` are all refused with the field-named quote message;
  - `hash-derived`, `mac-derived`, `maap` and `" MAAP "` still work.
- My round-2 script `scalar_spelling_probe.py`, rerun unchanged, reports every row as `equal: true` or refused with the quote message (`receipts/scalar_spelling_head.jsonl`).

**R340-2-F2 = R341-2-F2 (the 47-entry probe row) is CLOSED.**

- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:168` now names the 46-entry, 506-octet descriptor as the control. It names 47 entries (514 octets) as exceeding the 2021 cap, and attributes the packer's acceptance to processor issue 60 as defence-in-depth debt.
- `scripts/audit_pp_descriptors.py:210-211` labels "46 formats at 2021 Table 7-8 cap (506 octets)" and "47 formats above 2021 Table 7-8 cap (514 octets)". Both octet figures follow from `resize_list`: 138 + 8N.
- The audit exits 0. The 46, 47 and 48 rows are measured as accepted, with image sizes 6144, 6152 and 6160 (`receipts/audit_pp_descriptors_L4_head.txt`).

**R341-2-S1 (`be32` masking) is taken and CLOSED.**

- `avdecc/aem_descriptors.py:187-189` packs through `AEM_U32` without a mask.
- `-1`, `-(2^32)`, `2^32`, `2^32+2125999` and `2^64` raise. `0`, `1`, `2126000` and `0xFFFFFFFF` pack unchanged.
- A grep of the parent AEM generators finds no other u32 pack: other 4-octet encodings use `int.to_bytes`, which raises on overflow. So the new sentence at `PP_DESCRIPTOR_OWNERSHIP.md:38` is accurate.

**Artifacts and configurations.**

- The five tracked configurations are accepted, and their artifacts are byte-identical to `e0920d77`:
  - `shipping_base.sha256` = `shipping_head.sha256`, 80 files, identical to the round-2 inventory;
  - `r340_artifacts_base.json` = `r340_artifacts_head.json`, 85 artifacts.
- `arty_current`, `arty_4x4` and `arty_8ch` still build through the builder, AEM store and AEM image.

**Mutants.** Every applicable mutant is killed, and every restored control passes:

- R341-1 bank: 26/26 applicable;
- R341-2 bank: 10/10 applicable;
- R340-1 bank: 30/30;
- R340-2 bank: 14/14 applicable required;
- round-3 reviewer mutants: 15/15, including restored integer acceptance in three forms and restored `be32` masking.

**Suggestions.** Four new SUGGESTION items are recorded; none affects coverage. Two concern pre-existing behaviour outside the frozen scope and are new-Issue candidates. No finding at MINOR or above is open, so every lens is covered clean at this head.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### SUGGESTION items (do not affect coverage)

**R341-3-S1 - SUGGESTION - Tests - `sw/builder/test_declarations.py:129-133`: loader controls do not pin the resolved value for the destination and format fields**

- **Evidence:**
  - For the three identity fields, the loader-level control compares the resolved value with the written text.
  - For `srp.stream_dmac_base`, the two format entries and the two CRF words, it asserts only that loading succeeds. The value contract is asserted at parser level (`:116-117`) for the shared parser.
  - Three call-site mutants survive (`receipts/r3c_mutants_head.json`, `receipts/r3d_mutants_head.json`): R3-M16 (a bare quoted DMAC resolves to base+2, still multicast), R3-M17b (a bare quoted AAF word resolves to another AAF word) and R3-M18 (a bare quoted CRF word is replaced by the Milan word).
  - The head behaviour is correct (`receipts/hex_rule_head.jsonl`). Call-site bypasses of the string rule are killed (R3-M5, R3-M6, R3-M13, R3-M14 and R3-M15). No such spelling-dependent transform exists in the code.
- **Impact:** a future call-site change that altered only bare-spelled values of these fields would pass the declaration suite.
- **Optional outcome:** compare `cfg["srp"]["stream_dmac_base"]`, `cfg[side][0]["formats"][0]`, `crf_format` and `crf_output_format` with the written value for both spellings.
- **Verification:** R3-M16, R3-M17b and R3-M18 are killed.

**R341-3-S2 - SUGGESTION (new-Issue candidate) - Robustness - `sw/builder/endstation_builder.py:3174-3187` (`_mac48`), `:3652-3664` (`_declared_uint`, used by `entity.vendor_oui`): sibling hex parsers still reinterpret unquoted YAML integers**

- **Evidence** (`receipts/sibling_parser_base.jsonl` = `receipts/sibling_parser_head.jsonl`, byte-identical):
  - `_mac48` does `int(str(v), 16)`. So unquoted `platform.mac_address: 020000000002`, which YAML reads as an octal integer, silently becomes station MAC `0x002147483650`; quoted, it gives `0x020000000002`. Unquoted `0x020000000002` is refused only because its decimal text is out of range.
  - `_declared_uint` takes integers at face value. Unquoted `vendor_oui: 123456` becomes `0x01E240`; it is refused only incidentally, because the I/G bit is set.
  - The behaviour is identical at `e0920d77`. These parsers are outside the round-3 decision, which covers the `_eui64`/`_fmt64` keys, and outside #573-#576.
  - All tracked configurations quote `mac_address`.
- **Impact:** a hand-written configuration with an unquoted digit-only MAC silently changes the station MAC. That changes the `mac-derived` `entity_id`, the stream_id prefix and the gPTP identity.
- **Optional outcome:** a separate Issue applies the same string rule to `platform.mac_address` and the `_declared_uint` hex fields, or documents their YAML-integer semantics.
- **Verification:** `scripts/sibling_parser_probe.py` reports equality or a named refusal on every row.

**R341-3-S3 - SUGGESTION (new-Issue candidate) - Robustness - `sw/builder/endstation_builder.py:1439-1440`: a scalar `formats` value is iterated character by character**

- **Evidence** (`receipts/edge_probe_base.jsonl`, `receipts/edge_probe_head.jsonl`):
  - `formats: "0205022000806000"`, a string rather than a list, was accepted at `e0920d77` as sixteen one-digit format words.
  - At this head it is refused, but by the family rule ("must contain only AAF formats").
  - `formats: "0x0205…"` is refused as "'x' is not a hex EUI-64".
  - This is pre-existing, and the head is strictly safer.
- **Optional outcome:** refuse a non-list `formats` with a named message.
- **Verification:** the edge probe shows a list-type refusal.

**R341-3-S4 - SUGGESTION - Docs - PR #585 body ("Status") and the REVIEW READY comment: stale publication state**

- **Evidence:** the body says "This body is prepared for publication; the head remains unpushed". REVIEW READY says "(local, unpushed)". The PR head is `8c956234` and its hosted checks are running (`receipts/pr585_body.txt`, `receipts/hosted_checks_8c956234.tsv`).
- **Optional outcome:** refresh the Status paragraph at the next body edit.

## Prior findings: disposition at this head

| Prior finding | Disposition | Evidence at `8c956234` |
|---|---|---|
| R341-2-F1 = R340-2-F1 MINOR (Conformance, Robustness, Tests, Docs): unquoted digit-only hex EUI-64 silently reinterpreted | **CLOSED** | See the evidence list after this table. |
| R341-2-F2 = R340-2-F2 MINOR (Docs; also Conformance in R340-2): the probe row and label present 47 as the Table 7-8 boundary | **CLOSED** | `PP_DESCRIPTOR_OWNERSHIP.md:168` reads "46-entry size 506" as the control and "47-entry size 514 exceeds the 2021 cap" as the invalid change, with processor issue 60 attribution. `audit_pp_descriptors.py:210-211` labels are corrected and a 46-entry probe is added. Line 64 ("47-entry declarations now refuse") is consistent. A repository grep finds no other parent "47 … Table 7-8 cap" text. The audit exits 0 (`receipts/audit_pp_descriptors_head.log`). |
| R341-2-S1 SUGGESTION (Robustness): `be32` masks silently | **Taken; CLOSED** | `aem_descriptors.py:189`. `test_declarations.py:150-162` covers the negative and overflow cases and the legal endpoints. R3-M9 (mask restored) and R3-M10 (clamp) are killed. The five-configuration bytes are unchanged. |
| R340-2-S1 SUGGESTION (Tests): boolean EUI-64 and null `media_clock_sources` not pinned | **Boolean part now pinned** (`test_declarations.py:139` includes `true`; the R2-12 pattern no longer exists). **Null-source part remains optional:** the R2-17 PROBE mutant still survives (`receipts/r340_round2_mutants_head.json`), and the head behaviour is correct (`receipts/r340_round2_probes_head.log`). | Not a coverage item. |
| R340-2-S2 SUGGESTION (Docs): ENDSTATION_BUILDER parameter rows do not name the new refusals | **Unchanged and optional** (`docs/ENDSTATION_BUILDER.md` is not touched in this delta) | Not a coverage item. |
| Round-1 findings (R341-1-F1..F3, R340-F1..F3, the S items) | **Remain CLOSED** | The round-1 scripts reproduce at this head: `bypass_probes_head.jsonl` differs from round 2 only in the four unquoted-integer rows, which are now quote-refused. `format_cap_length_head.txt` accepts 46 (506 octets) and exits 1 on the named 47 refusal, as designed. `buffer_wrap_probe_head.txt` packs `0xFFFFFFFF` equal and refuses `2^32`. `r340_probes_head.log` has no crashes. The mutant banks are fully killed. |

Evidence for closing R341-2-F1:

- Code: `_eui64` at lines 1329-1338 (string-only, then `int(v, 16)`). `"model_id_pin" in ent` (line 4376) makes a declared null pin refuse, as the decision requires ("any non-string value is refused").
- Tests: `test_hex_scalar_contract` (`test_declarations.py:92-147`, wired at line 368) covers the eight YAML paths:
  - parser-level equality for `0x…`, digit-only, octal-looking and underscored strings;
  - loader acceptance of prefixed and unprefixed quoted values, with value equality for the identities;
  - the named quote refusal for ten non-string spellings, including every spelling the decision assigns.
- Mutants: R3-M1 (round-2 integer-at-face-value), R3-M2 (round-1 hex reparse) and R3-M3 (integers accepted only above 2^52) are killed, as are R3-M4 (message loses "quote"), R3-M5/M13/M14/M15 (bypass at `_fmt64` or the format, CRF or entity_id sites), R3-M6 (DMAC bypass), R3-M7 (null pin ignored), R3-M11 (digit-only text parsed as decimal) and R3-M12 (underscores refused). All are in `receipts/r3_mutants_head.json` and `receipts/r3b_mutants_head.json`.
- Docs:
  - `README-parameters.md:152-158` and `PP_DESCRIPTOR_OWNERSHIP.md:198-201` state the enforced rule. The false round-2 sentence ("Quoted and unquoted … retain their numeric value") is gone.
  - The tracked configurations and repository fixtures contain no unquoted value for these keys (grep of `configs/`, `docs/`, `sw/`, `scripts/` and `tests/`).
  - Programmatic writers such as `gen_divergent_shape.py` operate on already-normalised strings.

## Executable evidence (this packet)

- `receipts/head_test_declarations.txt`: the declaration suite passes at head, exit 0, and prints the new `[F1] eight hex fields` and `[u32]` lines.
- Round-2 scripts rerun unchanged:
  - `scalar_spelling_head.jsonl` and `scalar_spelling_base.jsonl`;
  - `r2_mutants_head.json`: 10/10 applicable killed. R2-M11 and R2-M12 target the replaced lines and report `applied: false`; they are replaced by R3-M8 and R3-M1/M2.
- Round-1 scripts rerun unchanged:
  - `bypass_probes_head.jsonl` and `format_cap_length_head.txt`;
  - `r341_round1_mutants_head.json`: 26/26 applicable killed. R-M8 and R-M14 target the removed literal, as in round 2.
  - `shipping_base.sha256` = `shipping_head.sha256` (80 files).
- R340 scripts, rerun unchanged after the verdict was fixed:
  - `r340_probes_head.{json,log}` and `buffer_wrap_probe_head.txt`;
  - `r340_round2_probes_head.{json,log}` (R340's `round2_probes.py`);
  - `r340_round1_mutants_head.{json,log}`: 30/30 killed, source restored;
  - `r340_round2_mutants_head.{json,log}`: 14/14 applicable required mutants killed. R2-11, R2-12 and R2-14 are not applied, and PROBE R2-17 survives, which is optional.
  - `r340_artifacts_base.json` = `r340_artifacts_head.json` (85 artifacts, identical to round 2).
  - Script sources are hashed in `r340_script_sources.sha256`.
- Round-3 reviewer probes and mutants:
  - `hex_rule_head.jsonl` (`scripts/hex_rule_probe.py`);
  - `sibling_parser_{base,head}.jsonl` (`scripts/sibling_parser_probe.py`);
  - `edge_probe_{base,head}.jsonl` (`scripts/edge_probe.py`);
  - `r3_mutants_head.json`: 12/12 killed;
  - `r3b_mutants_head.json`: 3/3 killed;
  - `r3c_mutants_head.json`: R3-M16 survives. R3-M17 is killed only incidentally and is superseded by R3-M17b;
  - `r3d_mutants_head.json`: R3-M17b and R3-M18 survive (S1);
  - in every run, the sources are restored and the control exits 0.
- `focused_gates_head.txt`, all exit 0:
  - Python idiom, naming, doc style, doc paths, and docs_check with and without Git;
  - the descriptor audit, the AEM store self-test and `git diff --check e0920d77 HEAD`;
  - em-dash against `e0920d77`, TOC check and anchor verification, run with the renderer pinned in `tools/markdown/requirements.txt`, installed hash-checked into a scratch environment.
- `commit_messages.txt`: the three commits are one line each, with no trailers.
- `hosted_checks_8c956234.tsv`: hosted runs read once, at 10:17 UTC.
  - Succeeded: rtl-fast, verilator-lint, yosys-elaboration, Yosys shards 0-3, Verilator shards 0 and 3, elaborate, docs-check, docs-check-no-git, full-ci-gate, bdd-conformance, wire-accountability and changes.
  - In progress: Verilator shards 1, 2 and 4.
  - Skipped: "Physical gPTP (nightly and manual)". A skip is not execution.
- `clone_integrity_final.txt`: the review clone is at the exact head. The index tree equals `16767fc6`, the index hash equals the pre-probe record (`pre_index_lsfiles.sha256`), the status is empty, and the gitlinks `efeb541a`, `5dce647a`, `0922e434` and `48ff7a7e` are unchanged. All probes and mutations ran in disposable copies under the unpublished `scratch/`.

## Reviewer-owned completion ledger (this round)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decision 5854630094, items 1-3, checked one by one against `sw/builder/endstation_builder.py:1329-1353,1414-1418,1439-1440,2024-2038,3618-3619,4368-4381` and `avdecc/aem_descriptors.py:183-189`. IEEE 1722.1-2021 Table 7-8 cap 46 and 7.2 maximum 508, as re-extracted in R341-2 (the clauses are unchanged; the 138 + 8N arithmetic is re-checked at `scripts/audit_pp_descriptors.py:164-174`). Receipts: `hex_rule_head.jsonl`, `scalar_spelling_head.jsonl`, `audit_pp_descriptors_L4_head.txt`, `format_cap_length_head.txt`, `buffer_wrap_probe_head.txt`, `r340_round2_probes_head.log`. | R341-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| RTL | CLEAN | Scope: `delta_diffstat.txt` and `commit_messages.txt` show no `hdl/`, `.sv`, `.svh` or `.hex` change in the delta, and no gitlink change (`clone_integrity_final.txt`). The one packing change is `aem_descriptors.py:189` (`be32`). Its width contract was checked by the packed-byte legal endpoints in `test_declarations.py:150-162` and the R3-M9/M10 kills. Generated RTL inputs (`adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_*.svh`, `gptp_ucode.hex`) and the AEM image are byte-identical to `e0920d77` for all five configurations (`shipping_*.sha256`, `r340_artifacts_*.json`). | R341-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Robustness | CLEAN (S2 and S3 are pre-existing, out-of-scope suggestions) | 143-row string-rule matrix including null, empty, bool, float, list, map, u64-max and malformed `0x_1` (`hex_rule_head.jsonl`); selectors `hash-derived`, `mac-derived`, `maap` and `" MAAP "`; declared null and empty pin; whitespace, sign, empty and 65-bit strings (`edge_probe_head.jsonl`); scalar `formats`; `be32` negative and overflow; sibling parsers at base and head (`sibling_parser_*.jsonl`); 37 R340 round-1 probes and the R340 round-2 probes, with no crash | R341-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Tests | CLEAN (S1 suggestion) | `sw/builder/test_declarations.py:92-162,368-369`, run through its entry point (`head_test_declarations.txt`). Mutants: 26/26 + 10/10 + 30/30 + 14/14 applicable, plus 15/15 round-3 required-behaviour mutants killed, with passing restored controls (`r341_round1_mutants_head.json`, `r2_mutants_head.json`, `r340_round1_mutants_head.json`, `r340_round2_mutants_head.json`, `r3_mutants_head.json`, `r3b_mutants_head.json`). Survivors are recorded (`r3c`, `r3d`, R2-17). | R341-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Docs | CLEAN (S4 suggestion) | `sw/builder/README-parameters.md:145-160`; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:35-40,64,168,193-201`; `scripts/audit_pp_descriptors.py:210-211`; `docs/ENDSTATION_BUILDER.md:958-960,978,1019` (no contradiction with the string rule); the `be32` docstring at `aem_descriptors.py:188`; the PR body and REVIEW READY at read time (`pr585_body.txt`, `executor_manager_comments.txt`); `focused_gates_head.txt` (all docs gates exit 0) | R341-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |

At this head, all five lenses are covered clean by R341-3. A later commit that touches any artifact in a lens's scope un-covers that lens. For example, `avdecc/aem_descriptors.py` or any generated-header input un-covers RTL, and the builder parser or its tests un-cover Conformance, Robustness and Tests.

## Real limits

- As the brief directs, these were not run: the full parent, processor, gPTP, Yosys and builder banks, Docker/act, the host act runner or its self-test, and hardware.
  - The full builder bank in both compiler modes at this head is the author's public evidence (`author-r3/builder-present.log`, `builder-absent.log`, rc 0). Gate 11 calibration is NOT RUN in both, and gate 1b's compiler census is NOT RUN in absent mode. It is not this round's evidence.
- The scoped Verilator was not used: this delta is Python and docs only, with byte-identical generated RTL inputs. Its identity was therefore not checked.
- "The Arty configurations still build" is verified as builder CLI, AEM store and AEM image generation succeeding byte-identically for the three Arty configurations. It is not verified as a bitstream or elaborate job. The hosted `elaborate` job at this head succeeded, but that belongs to the manager's acceptance.
- The hosted checks were read once, at 10:17 UTC, with Verilator shards 1, 2 and 4 still in progress.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- This round did not validate the final current-dev candidate: source base `e0920d77`, live dev `ac18b509`.
- Clause text was not re-extracted this round. The Table 7-8 and 7.2 excerpts are those recorded in R341-2 `receipts/spec_excerpts.txt`, and the delta changes no cited clause.

## Pending manager duties

- Publish this report.
- Hosted and act acceptance at the exact head, including the Verilator shards still in progress at read time, and the candidate-merge build against live `dev` at the merge turn.
- Optional new-Issue candidates:
  - R341-3-S2: the sibling parsers `_mac48` and `_declared_uint`;
  - R341-3-S3: scalar `formats`;
  - the remainder of R340-S3 (the ignored `crf_output.formats` key);
  - the optional R2-17 null-source test.
- Optional executor follow-ups: R341-3-S1 (loader value pins) and R341-3-S4 (the PR body Status paragraph).
- Processor-owned "N <= 47" acceptance remains with processor issue 60, as decided.
- Merge requires the second independent positive review and the full completion bar. No agent merge without explicit maintainer authorization.

R341-3 FINISHED
