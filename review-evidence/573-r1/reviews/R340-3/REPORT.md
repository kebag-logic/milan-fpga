[R340] POSITIVE - exact head 8c956234699b5dec5e6c9aeada651be667974e9b

# R340-3: internal independent re-review of PR #585 (issues #573-#576), round 3

- Exact head: `8c956234699b5dec5e6c9aeada651be667974e9b`, tree `16767fc674e46e4f210feaf6e21dbeb096a76fe3`. Source base: `e0920d77162284d8da52ffaf13a973e451e44f90`.
- Round: R340-3, cleared context, internal reviewer. This is a delta review: round R340-2 covered `08374721`, and this round judges the three commits `9e47e48c`, `0d5820ae` and `8c956234`. All five lenses were applied at the exact head: Conformance, RTL, Robustness, Tests and Docs.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the round-3 assignment and decision (#573 comment 5854630094) and the executor's REVIEW READY (#573 comment 5854843470);
  - the live PR body (`receipts/pr_body_at_review.md`);
  - `git diff e0920d77..8c956234` and the per-commit history (`receipts/docs_gates_and_delta.txt`);
  - the public evidence tree `265f00ea:review-evidence/573-r1`, which holds round-1 evidence only;
  - the exact-head hosted check list.
- Prior findings: this round's verdict and ledger were fixed before any prior finding text was read (`receipts/verdict_before_prior_read.txt`).

## Verdict summary

Both round-2 MINORs are closed at this head, and R341-2-S1 is implemented as decided.

**Quoted-string rule.** Every 64-bit hex key read through `_eui64`/`_fmt64` must now be a YAML string (`endstation_builder.py:1329-1338`).
- Across eight fields, a quoted value with or without `0x`, and with or without underscores, resolves to its written hex value.
- Every YAML number, boolean, null, float, list and map is refused, and the message names the field and says to quote it.
- The eight fields are both identity keys, `entity_id`, `srp.stream_dmac_base`, talker and listener format words, `crf_format` and `crf_output.format`.

**Probe row and label.** The matrix row now reads 46 entries (506 octets) as the legal boundary and 47 (514 octets) as above the 2021 cap; the audit label agrees (`PP_DESCRIPTOR_OWNERSHIP.md:168`, `audit_pp_descriptors.py:210-212`).

**be32.** `be32` refuses values outside u32 instead of masking them (`aem_descriptors.py:187-189`).

**Artifacts.** The five tracked configurations produce byte-identical artifacts to `e0920d77`:
- 85/85 per-artifact hashes;
- 80/80 files through the builder CLI plus the AEM store and image generators.

The three Arty configurations still build through the builder.

**Mutation.** All 17 round-3 mutants are killed. Every applicable round-2 mutant is still killed.

No BLOCKER, MAJOR or MINOR is open. Five SUGGESTIONs follow. Two of them (S2, S4) describe defects that predate this lane, sit outside its decided scope and are not in its diff. They are candidates for new Issues and do not affect coverage.

## Round-2 findings: disposition at 8c956234

| Round-2 item | Status | Evidence at this head |
|---|---|---|
| R340-2-F1 = R341-2-F1 MINOR: unprefixed unquoted hex EUI-64 silently reread as YAML decimal/octal | **CLOSED** | **Code:** `_eui64` refuses every non-string with `"{ctx}: quote the hexadecimal value as a YAML string"` and parses strings with base 16 only (`endstation_builder.py:1329-1338`). `_model_id` and `_fmt64` share it. The hash arm now passes a string (`:4379`), and an explicit `model_id_pin:` null is judged rather than ignored (`:4376`).<br>**My unchanged `round2_probes.py`** (sha256 `7710387e…` equals the round-2 manifest; `receipts/round2_probes_head.log`): on both identity keys, unquoted `0x…`, `0x…` with underscores, `1234567890123456`, `0012345670123456`, `18446744073709551615` and `true` are all refused with the quote message. Quoted `"0x001BC50AC1000005"`, `"1234567890123456"` and `"0012345670123456"` each resolve to the written hex digits. Unquoted `stream_dmac_base: 0x91E0F000FE01` is refused with the quote message. At `08374721` the same script shows the old reinterpretations (`receipts/round2_probes_prev_08374721.log`).<br>**My `round3_probes.py`** (`receipts/round3_probes_head.log`, 172 rows, 0 failed): across all eight fields, three quoted spellings resolve to the written value. Ten non-string spellings are refused with a field-named quote message: prefixed, `1234567890123456`, `0012345670123456`, an octal-looking legal value, `true`, `null`, empty, `1.5`, `[]` and `{}`. Quoted `""`, `"0x"` and `"-0x1"` are refused. Quoted `"1234567890123456"` resolves to `0x1234567890123456` on all three identity keys.<br>**Tests:** `test_declarations.py:92-147` covers the four keys the decision names and four more. Mutants R3-M1..M3 are killed; they restore integer acceptance, accept non-bool integers, and stringify then reread.<br>**Docs:** `README-parameters.md:152-158` and `PP_DESCRIPTOR_OWNERSHIP.md:198-201` state the enforced rule. |
| R340-2-F2 = R341-2-F2 MINOR: matrix probe row and audit label presented 47 formats as the legal Table 7-8 boundary | **CLOSED** | `PP_DESCRIPTOR_OWNERSHIP.md:168` has 46 entries at 506 octets as the accepted control, and 47 entries at 514 octets as "exceeds the 2021 cap". The result reads "All accepted", recorded as PP60 defence-in-depth debt. The audit script adds a 46-entry probe and relabels 47 as "above 2021 Table 7-8 cap (514 octets)" (`audit_pp_descriptors.py:210-212`). My run of the audit at head gives 46, 47 and 48 all accepted by the packer, at image sizes 6144, 6152 and 6160 (`receipts/audit_pp_descriptors_head.json`), which matches the row. The arithmetic comes from the source constants: `MAX_STREAM_FORMATS = (508-138)//8 = 46`, 46→506, 47→514 and 48→522 (`receipts/format_cap_arith.txt`). No other parent text calls 47 the cap. |
| R341-2-S1 SUGGESTION: `be32` masks out-of-range u32 silently | **Taken for be32 (as decided)** | `aem_descriptors.py:187-189` packs without a mask, so the struct range check raises. `be32` of -1, 2^32 and 2^32+2125999 raises; 0, 1 and 0xFFFFFFFF pack unchanged (`receipts/round3_probes_head.log`). Mutants R3-M15..M17 (restored mask, clamp, and mask on overflow only) are killed by `test_aem_u32_contract` (`test_declarations.py:150-163`). `be16` and `be64` still mask. The decision did not include them, so this remains an optional item. |
| R340-2-S1 SUGGESTION: bool EUI-64 and null `media_clock_sources` unpinned | **Bool half closed; null half retained (optional)** | `true` and `null` are now in the test's refusal spellings for every hex field. The null-sources PROBE mutant R2-17 still survives (`receipts/r2_mutants_head.log`), and the executor reports this openly. |
| R340-2-S2 SUGGESTION: `ENDSTATION_BUILDER.md` parameter rows 2/9/12/19 | **Retained (optional)** | This delta does not touch that file. |

## Findings

No BLOCKER, MAJOR or MINOR.

### Suggestions (non-blocking; they do not leave any lens unclean)

- **R340-3-S1: SUGGESTION: Conformance, Docs: `sw/builder/endstation_builder.py:1333`, `sw/builder/README-parameters.md:155`.** The decision says quoted text is "hexadecimal, with an optional 0x prefix and optional underscores". Base-16 integer parsing also accepts:
  - a leading `+`;
  - surrounding whitespace;
  - `0X`;
  - non-ASCII decimal digits, such as fullwidth digits.

  All four are value-preserving. Every such spelling resolves to the hex value of its digits on all eight fields (`receipts/round3_probes_head.log`, rows marked `None`), so nothing is silently reinterpreted. A strict ASCII pattern, or one README sentence, would make the enforced rule and the documented rule identical.
- **R340-3-S2: SUGGESTION (new-Issue candidate, outside this lane's decided scope): Robustness, Conformance: `sw/builder/endstation_builder.py:3174-3177` (`_mac48`).** `platform.mac_address` is not read through `_eui64`. It converts a YAML integer to text and rereads the decimal digits as hex, and both results are accepted:
  - unquoted `0x000000F42402` resolves to `0x000016000002`;
  - unquoted `10:20:30:40:50:02` is a YAML 1.1 base-60 integer and resolves to `0x008041827002`.

  Behaviour is identical at `e0920d77` (`receipts/round3_extra_probes_{head,base}.log`). The station MAC feeds the mac-derived `entity_id` and the stream_id, and the `_mac48` docstring advertises the unquoted `0x` form. This is the same defect class as round-2 F1. The frozen decision scoped the rule to `_eui64`/`_fmt64` keys and the diff does not touch `_mac48`, so under AGENTS section 4 this is new work, not a lane defect. Required outcome if taken: the same quoted-string rule, in a new Issue.
- **R340-3-S3: SUGGESTION: Tests, Docs: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:181` vs `scripts/audit_pp_descriptors.py:263`.** The matrix says the reachable parent YAML probes demonstrate that 47 AAF output entries are refused. The audit's config probe measures 48 (`receipts/audit_pp_descriptors_head.json`: "format count 48 exceeds 46"). The 47-entry refusal is true: the test is `test_declarations.py`, and my probe gives "format count 47 exceeds 46" (`receipts/round3_extra_probes_head.log`). Setting the audit probe to 47 would make the row trace to its receipt. This item predates the delta.
- **R340-3-S4: SUGGESTION (new-Issue candidate, pre-existing): Robustness: `sw/builder/endstation_builder.py:1439-1440`.** When `formats:` is a scalar rather than a list, the result is still a refusal (non-zero exit, no silent acceptance), but the messages are poor:
  - an unquoted YAML integer crashes with `TypeError: 'int' object is not iterable` instead of a named `ConfigError`;
  - a quoted string is iterated character by character.

  The behaviour is identical at `e0920d77`, `08374721` and the head (`receipts/formats_scalar.txt`).
- **R340-3-S5: SUGGESTION: Docs: `docs/ENDSTATION_BUILDER.md:1019`.** "Numeric values feed the legacy `LWSRP_DMAC_LO/HI` scratch words" uses "numeric" to mean a concrete address rather than the `maap` selector. Under the new rule a YAML number is refused, so "concrete (quoted hex) addresses" would avoid misreading. This line predates the lane.

## Evidence (reviewer-run, this packet)

- **Declaration suite at the exact head** (`receipts/declarations_head.log`): `python3 -B sw/builder/test_declarations.py` returns rc 0 in 3 s. It includes the lines `[F1] eight hex fields…` and `[u32] zero/maximum pack unchanged…`.
- **Round-3 mutation bank** (`scripts/mutants_r2.py` unchanged, `scripts/mutant_cases_r3.json`, `receipts/r3_mutants_head.{log,json}`): 17/17 mutants are killed. They restore integer acceptance (three variants), drop "quote" or the field name from the message, and ignore a null pin. Others:
  - an integer on the hash arm;
  - a stringify mutant at each of the dmac, format, `entity_id` and CRF sites;
  - decimal reading of digit-only strings;
  - a required `0x`;
  - refused underscores;
  - three `be32` variants.

  The unmutated control passes, and both mutated sources are restored byte-identically.
- **Round-2 bank, unchanged** (`receipts/r2_mutants_head.log`): all 14 applicable KILLED-expectation mutants are killed. R2-11, R2-12 and R2-14 are NOT-APPLIED because the code they mutated was replaced; R3-M1..M3 and M7 cover those behaviours. R2-17 is the known PROBE survivor.
- **Artifact identity** (`scripts/hash_artifacts.py`, `scripts/shipping_identity.sh`, both unchanged from round 2; `receipts/artifacts_compare.txt`): base `e0920d77` and head were built in disposable clean clones. Result: 85/85 per-artifact sha256 equal and 80/80 CLI files identical. This covers all five configurations, including the generated SV headers, AEM ROM, AEM image, gPTP microcode and LWSRP tables. Both clones were clean afterwards (`receipts/environment.txt`).
- **Descriptor audit at head** (`receipts/audit_pp_descriptors_head.{log,json}`): rc 0, 5 configurations measured, L4 rows as stated above.
- **Docs and idiom gates** (`receipts/docs_gates_and_delta.txt`): `check_doc_paths` OK, `check_doc_style` OK, `check_py_idiom` rc 0, `git diff --check e0920d77..HEAD` clean.
  - `check_em_dash` and `gen_toc --check` could not run (rc 2) because their pinned Markdown renderer is not installed, and installs are out of bounds.
  - By hand: the 103 added lines contain no non-ASCII character and no new heading.
- **Commits:** all three are one-line subjects with no body or trailers.
- **Hosted contexts** (`receipts/hosted_checks_8c956234.tsv`, read-only, 12:06 local): the checks were read at the exact head.
  - Completed with success: `verilator-lint`, Yosys shards 0-3, `changes`, `full-ci-gate`, `bdd-conformance`, `wire-accountability` and `docs-check-no-git`.
  - Still in progress: Verilator shards 0-4, `yosys-elaboration`, `elaborate` and `docs-check`.
  - `Physical gPTP` is skipped, which is not an executed job.
- **Clone integrity after all probes** (`receipts/clone_integrity.txt`):
  - HEAD, tree and write-tree equal the expected values, and porcelain is empty including submodules;
  - index modes and blobs equal the HEAD tree across 917 entries, and worktree blob bytes equal the HEAD blobs;
  - the gitlinks are `external` efeb541a (uninitialised), `gptp-processor` 5dce647a, `protocol-processor` 0922e434 and `third_party/verilog-axis` 48ff7a7e, all unchanged from `e0920d77`.

## Reviewer-owned completion ledger (round R340-3)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `endstation_builder.py:1329-1353, 1414-1418, 1439-1440, 2027-2037, 3619, 4371-4381` against decision 5854630094 items 1-3. `aem_descriptors.py:183-189, 273-276` against the 2021 Table 7-8 arithmetic (`format_cap_arith.txt`). Probe logs: `round2_probes_head.log`, `round3_probes_head.log` (172 rows), `round3_extra_probes_head.log`. Artifact identity: `artifacts_compare.txt`. | R340-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| RTL | CLEAN | The delta has no HDL. `aem_descriptors.py:187-189` is a generated-header input, so it un-covered R340-2's RTL coverage; it is re-covered here. At the head, every generated SV/hex artifact is byte-identical to base for all five configurations: `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_csr_defaults.svh`, `lwsrp_table.svh`, `gptp_ucode.hex` and `aem_desc.bin` (`artifacts_compare.txt`, `shipping_*_*.sha256`). | R340-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Robustness | CLEAN | `round3_probes_head.log`: 20 spellings × 8 fields, including null, empty, float, list, map, empty string, `0x`, negative and value-preserving leniencies. `be32` covers negative, 2^32, 2^32+2125999 and bool. Also: the `maap` selector (`round3_extra_probes_head.log`), an explicit null pin (`:4376`), and the hash arm as a string (`:4379`). Out-of-scope pre-existing items are S2 and S4. | R340-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Tests | CLEAN | `test_declarations.py:67-163, 366-371` run through its entry point (`declarations_head.log`). Round-3 mutants 17/17 killed (`r3_mutants_head.log`); round-2 bank 14/14 applicable killed-expectation mutants killed, 1 known PROBE (`r2_mutants_head.log`). | R340-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |
| Docs | CLEAN | `README-parameters.md:149-160`. `PP_DESCRIPTOR_OWNERSHIP.md:36-42, 152-201`. `audit_pp_descriptors.py:196-265` together with its head run. `ENDSTATION_BUILDER.md:958, 1019` (unchanged). The PR body (`pr_body_at_review.md`, with Round 3). REVIEW READY 5854843470. `docs_gates_and_delta.txt`. | R340-3 | 8c956234699b5dec5e6c9aeada651be667974e9b |

All five lenses are covered clean at the exact merge-candidate head. A later commit that touches any artifact in a lens's scope un-covers that lens.

## Real limits

- This is a delta review. The earlier lane content was covered at `08374721` (R340-2) and `4f746408` (R340-1). This round re-verified it through artifact identity and the unchanged round-2 scripts and banks, not by re-reading every earlier line.
- I ran no full parent, PP, gPTP, Yosys or builder bank, no act runs and no hardware. Physical calibration was NOT RUN, and skipped field or physical contexts are not hardware proof. The scoped Verilator was not used, because the delta has no RTL; generated SV was compared byte-for-byte instead.
- `check_em_dash` and `gen_toc --check` were not executed by this reviewer (renderer absent). The public evidence tree `265f00ea` holds round-1 gate results only, so I have not seen exact-head receipts for these two gates. The by-hand check found no non-ASCII character and no heading change.
- I re-extracted no clause text this round. The delta changes no protocol behaviour, the 46/506/508 arithmetic comes from the source constants, and round R340-2 verified the clause text.
- Mutation covered `test_declarations.py` only.
- Hosted checks were read at 12:06 local time with several jobs still running.

## Pending manager duties

- Accept the exact-head hosted `verilator-suites`, `yosys-portability`, `elaborate`, `docs-check` and `rtl-fast` verdicts, and the act replica, once they complete.
- Provide or confirm exact-head `check_em_dash` and `gen_toc --check` results.
- Build and validate the final candidate on live `dev` `ac18b50968b12efe4d15c0a06301264b35656b31` at the merge turn, and run post-merge containment.
- Obtain the second independent positive review and its ledger. Merge only with explicit maintainer authorization.
- Optionally route S1, S3 and S5. File new Issues for S2 (`platform.mac_address` reinterpretation) and S4 (non-list `formats` crash) if the maintainer agrees.

R340-3 FINISHED
