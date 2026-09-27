[R340] NEGATIVE - exact head 4f746408a15f494c4b30bdc9add6d7295309dff9

# R340-1: internal independent review of PR #585 (issues #573, #574, #575, #576)

- Head `4f746408a15f494c4b30bdc9add6d7295309dff9`, tree `432897b634f661042e67cf390513fae6356542ba`, base dev `e0920d77162284d8da52ffaf13a973e451e44f90`, four commits (one per issue: `63818217` #573, `556901b5` #574, `82fa859b` #575, `4f746408` #576), all one-line with no trailers.
- Diff: `sw/builder/endstation_builder.py` (+65/-6), `sw/builder/test_declarations.py` (+156), `sw/builder/README-parameters.md` (+18), `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (+24/-21). There are no RTL, processor or submodule changes.
- Authorities: AGENTS.md, CONTRIBUTING.md and docs/README.md. The scope comes from the bodies of issues #573-#576, the assignment decision (issue 573 comment 5853854503), and the TAKEN and REVIEW READY comments. The ownership matrix has an F1-F4 "Follow-up allocation". The repository's clause authorities are `protocol-processor/docs/architecture/07_memory_maps.md` (L9, and the Table 7-8 cap at line 201), `04_adp_engine.md:73` and `00_MILAN_COMPLIANCE_REVIEW.md:306`.
- Prior public review findings on this PR: **none exist**. I checked after my own pass. The PR has only the two "REVIEW STARTED" comments, no reviews and no inline comments, so there is nothing to resolve or keep.

## Verdict summary

All four refusals exist as named `ConfigError`s in the parent configuration path. Each one is exercised by `test_declarations.py`, and that file runs first in `test_builder.py`'s main entry (line 27557). All 14 of the author's mutants and 16 of my own are killed. The five tracked configurations still build, and all 85 builder, AEM store and AEM image artifacts are byte-identical between `e0920d77` and `4f746408`.

The F2 floor can be bypassed, though. The check validates the declared integer, but the value packed into STREAM_INPUT `buffer_length` is taken modulo 2^32. So a declaration that passes the floor check can produce a generated descriptor below the Milan floor (R340-F1, MAJOR). There are also two MINOR findings: a stale authoritative doc sentence and an unresolved clause citation. All five lenses are therefore unclean.

## Findings

### R340-F1: MAJOR: Conformance, RTL, Robustness, Tests: `sw/builder/endstation_builder.py:1382-1390` (`_stream_buffer_ns`) with `avdecc/aem_descriptors.py:184,299`: the listener buffer floor is bypassed through 32-bit truncation

- **Requirement/evidence:** F2 (#574) and the assignment require every declared listener buffer to meet the Milan v1.2 5.3.3.4 floor, with "any path that bypasses a check" treated as a finding.
  - `_stream_buffer_ns` checks only `type is int and value >= 2126000`. It has no upper bound.
  - The STREAM_INPUT `buffer_length` field is 32 bits (IEEE 1722.1-2021 Table 7-8, offset 128). `be32()` packs it as `v & 0xFFFFFFFF`.
  - Receipt `receipts/buffer_wrap_head.json`, from `scripts/buffer_wrap_probe.py` on the `ax7101_8x8` configuration, listener 0:
    - Declared `4297093295` (2^32 + 2125999) is accepted by the loader and the image, and packs as **2125999**. That is the exact value #574 requires to be refused.
    - Declared `4294967296` is accepted and packs as **0**.
    - `4294967295` packs unchanged.
  - The full `builder.build()` plus `gen_aem_store.py` path also accepts the wrapped declaration (`receipts/buffer_wrap_build_head.log`).
  - The processor packer accepts 2125999, as the matrix records at `PP_DESCRIPTOR_OWNERSHIP.md:166`, so defence in depth does not catch it either.
- **Impact:** A configuration that passes the named floor refusal can ship a STREAM_INPUT that advertises a buffer below the Milan floor, or zero. The refusal checks a value that is not the one emitted. The #574 matrix and README claims ("every listener declaration below the Milan floor" is refused) do not hold for the generated image.
- **Lenses:**
  - Conformance: the Milan floor is violated in the output.
  - RTL: width and truncation at the descriptor-image interface field.
  - Robustness: maximum value with no boundary.
  - Tests: the upper and wrap boundary is untested; the tests stop at 2126001.
- **Required change:** A listener `buffer_length_ns` above the STREAM_INPUT field maximum (0xFFFFFFFF) must be refused by a named `ConfigError`. The field width should come from one source, not a new restated literal. Either way, the value that reaches the descriptor must equal the declared value.
- **Verification:** Add declaration tests where 0xFFFFFFFF is accepted and packs equal, and 2^32 and 2^32+2125999 are refused under the buffer rule. Add a mutant that removes the upper bound, and confirm it is killed. Rerun `scripts/buffer_wrap_probe.py`. The five-configuration artifact hashes must stay unchanged.

### R340-F2: MINOR: Docs: `docs/ENDSTATION_BUILDER.md:443`: the authoritative builder design doc still says reserved identities are accepted

- **Requirement/evidence:** Line 443, under "Why + the pin override", reads "Zero and all-ones identities also pass the numeric-width check." At this head `_model_id` (`endstation_builder.py:1341`) refuses both endpoints on both input forms (`receipts/probes_head.log`, F1 rows). The ownership matrix (`PP_DESCRIPTOR_OWNERSHIP.md:193`) now states the opposite. The PR updated the matrix and README-parameters but not this paragraph.
- **Impact:** Two authoritative documents contradict each other about F1. A cold reader of the builder design doc would conclude the gap is still open.
- **Required change:** `ENDSTATION_BUILDER.md` must describe the enforced F1 refusal, or defer to the matrix without asserting acceptance. Optionally, the parameter-table rows 9, 12 and 19 (lines 973, 977, 990) could name the new INTERNAL, CRF-word and floor refusals.
- **Verification:** Grep the docs for claims that zero or all-ones identities are accepted, and run the docs gates.

### R340-F3: MINOR: Conformance, Docs: `sw/builder/endstation_builder.py:1347`, `sw/builder/README-parameters.md:147`, `sw/builder/test_declarations.py:35,45`: the clause cited for the reserved-model-ID rule is unresolved

- **Requirement/evidence:** The refusal message, the parameter guide and the test comments all cite "Milan v1.2 5.3.1" for the "neither all zeros nor all ones" rule. The review focus for this round states that the rule is in Milan v1.2 **5.3.3.1** (the ENTITY descriptor clause). 5.3.3.1 is also the clause the matrix uses for the ENTITY-level ADP maxima (`PP_DESCRIPTOR_OWNERSHIP.md:69`). The 5.3.1 citation is inherited from the processor documents (`07_memory_maps.md:91`, `04_adp_engine.md:73`, `00_MILAN_COMPLIANCE_REVIEW.md:306`). The repository contains no specification text to settle it (the tracked `aem-and-aecp.pdf` is a historical design note). AGENTS.md section 2 requires such a conflict to be published and decided, not chosen privately.
- **Impact:** A user-facing refusal message and a parameter guide may send readers to the wrong clause. The builder has now copied the processor docs' citation into a new, normative-sounding refusal.
- **Required change:** Publish the clause text that carries the rule. Then cite the correct clause in the message, the README and the tests, or record why 5.3.1 is correct. Processor-document corrections, if any are needed, belong to the processor lane.
- **Verification:** A public decision with clause text, and a grep of the changed files for the resolved citation.

### Suggestions (non-blocking; no lens is left unclean by these)

- **R340-S1: SUGGESTION: Tests: `test_declarations.py:157-160`.** The CRF-output arm of `_validate_output_clock_sources` is only observable as refusal precedence. The full loader requires a talker, so any configuration with a CRF output and no INTERNAL is already refused by the AAF arm. The author's mutant "CRF output arm removed" is killed only because the refusal message changes to "needs at least one talker stream". A direct negative call, `_validate_output_clock_sources([], {"crf_output": True, "media_clock_sources": ["crf"]})` raising, would test that arm's behaviour on its own. My mutant R-F4c (checking listeners instead of talkers) is equivalent in the reachable space and is also killed only by message.
- **R340-S2: SUGGESTION: Robustness: `endstation_builder.py:3855`.** An empty `media_clock_sources` still raises `IndexError` (the eager `srcs[0]`), even when `default_source` is given (`receipts/probes_head.log`). An output configuration with no sources therefore never reaches the named F4 refusal. This predates the PR, the matrix L6 row already documents it, and no artifact is generated. It is a candidate for a new issue.
- **R340-S3: SUGGESTION: Robustness: `endstation_builder.py:4366-4371`.** When `model_id_pin` is present, a literal `entity_model_id` (including `0x0000000000000000`) is neither validated nor refused. It is silently shadowed, and the generated identity is the legal pin. This precedence behaviour predates the PR, and no reserved identity reaches the output. An ignored `clocking.crf_output.formats` key is tolerated the same way, and the default word ships. Both are candidates for an unknown-or-shadowed-key issue, not for this lane.

## Per-issue verification

| Issue | Required | Observed at 4f746408 |
|---|---|---|
| #573 F1 | 0 and all-ones refused on literal and pin; legal accepted; ENTITY/ADP equality | Refused on both forms: 0x0 short form, lowercase all-ones, and YAML int 0 (`probes_head.log`). YAML decimal all-ones is refused earlier as out of range. Legal 0x…01, 0x…FE and the shipped ID are accepted, and the test compares packed ENTITY[0] bytes 12..20 and `MILAN_MODEL_ID_HI/LO`, which firmware writes to `MILAN_ADP_MID_*` (`milan_baremetal.c:1371-1372`). The hash-derived path cannot produce either endpoint: with OUI 0 the sample gave 0x00000057FC6ABBC8. The clause citation is open (R340-F3). |
| #574 F2 | 2126000 accepted, 2125999 refused, every listener; talkers unaffected; non-integer refused | 2126000 and 2126001 are accepted and 2125999 is refused at all eight 8x8 listener indices. Null, float, string and bool are refused. The default is accepted. Talker values (1, "x") are ignored as before. **The upper bound is bypassed (R340-F1).** |
| #575 F3 | 47 cap on the final list including derived entries; AAF/CRF family; Milan CRF word; inputs and outputs | Listener: 46 declared (47 final) is accepted and 47 declared (48 final) is refused. Talker: 47 is accepted and 48 is refused. Mixed lists are refused at every arty_4x4 index and at the last 8x8 index, in both directions. The CRF word is exact-matched in both directions, case-normalised. Words that are never emitted (sink off, output off) are refused too: stricter, and harmless. The default path, the derived family entry and the alternate `formats` key cannot inject an invalid word. |
| #576 F4 | INTERNAL+CRF accepted; CRF-only outputs refused; input-only preserved | INTERNAL+CRF is accepted with either default. `[internal]` with the sink off is accepted. `[crf]` with outputs is refused on current and 8x8. `_load_clocking` still accepts CRF-only input clocking. The CRF-output arm is precedence-only (S1). Empty lists crash (S2, predates the PR). |

## Evidence (reviewer-run, this packet)

- `receipts/declarations_head.log`: `python3 sw/builder/test_declarations.py` at the exact head, rc 0 (F1-F4 lines plus gate 40).
- `receipts/artifacts_{base_e0920d77,head_4f746408}.json` and `receipts/artifacts_compare.txt`: `scripts/hash_artifacts.py` on disposable copies of each tree.
  - Five configurations × 17 artifacts: builder directory, the adp_shape copy, sweep_opts, `gen_aem_store.py` output and `gen_aemi_image.py` bin/map/json.
  - **85/85 identical** in sha256 and size. My base hashes agree with the author's public `before.json` on all 75 keys where the labels match.
  - Every configuration, including all three Arty configurations, builds at the head.
- `receipts/mutants_head.{log,json}`: `scripts/mutants.py` with `scripts/mutant_cases.json`. The author's 14 mutants were re-run, plus 16 of mine: off-by-one floor and cap, type check removed, validation before completion, top-nibble family, first-entry-only family and CRF word, unvalidated CRF input and output, selection-instead-of-availability, call site removed, and others. **30/30 killed.** The unmutated control passed afterwards, and the source was byte-restored (`identical: true`).
- `receipts/probes_{head,base}.{log,json}`: `scripts/probes.py`, 37 boundary, alternate-spelling and path cases, run at the head and at the base for contrast.
- `receipts/buffer_wrap_head.json` and `receipts/buffer_wrap_build_head.log`: the R340-F1 reproduction.
- `receipts/hosted_checks_4f746408.txt`: exact-head hosted contexts as observed, read-only. When observed, Verilator shards 1, 2 and 4 of 5 were in progress. The physical gPTP context was skipped, which is not hardware proof. The manager owns hosted and act acceptance.
- `receipts/clone_integrity.txt`: the review clone ends clean.
  - HEAD, tree and `write-tree` all equal `432897b6…`.
  - The index modes and blobs match the HEAD tree.
  - The worktree blob-list hash equals the HEAD blob-list hash.
  - Gitlinks: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `0922e434`, verilog-axis `48ff7a7e`.
  - All probes and mutations ran in `scratch/` copies.
- `receipts/environment.txt`: interpreter and library versions, and the scratch copy heads.

## Reviewer-owned completion ledger (round R340-1)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R340-F1 MAJOR, R340-F3 MINOR) | `endstation_builder.py:1341-1414, 1460, 1501, 3869-3873, 4214-4226, 4364-4371` against issue F1-F4 acceptance, Milan 5.3.3.4/5.3.3.6/7.3.2 as cited, Table 7-8 cap per `07_memory_maps.md:201`; probes and wrap receipts | R340-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| RTL | UNCLEAN (R340-F1 MAJOR: 32-bit field truncation at the descriptor-image interface) | diff touches no `.sv`/submodule; generated RTL headers (`adp_shape_defaults.svh`, `lwsrp_*.svh`, `aecp_aem_rom.svh`, `gptp_ucode.hex`) byte-identical for all five configurations; `aem_descriptors.py:184,299` field packing | R340-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Robustness | UNCLEAN (R340-F1 MAJOR) | 37 probes: non-integer, null, bool, string, YAML-int and short/lowercase spellings; defaults; derived listener entries; unused CRF words; alternate/shadowed keys; empty/reversed source lists; first and last stream indices | R340-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Tests | UNCLEAN (R340-F1 MAJOR: missing upper and wrap boundary) | `test_declarations.py:24-168` and wiring at `test_builder.py:27557`; 30/30 mutants killed plus the control; the precedence-only arm is noted in S1 | R340-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |
| Docs | UNCLEAN (R340-F2 MINOR, R340-F3 MINOR) | `PP_DESCRIPTOR_OWNERSHIP.md:1-8, 62, 64, 67, 173-194, 233-242` (claims match the probes); `README-parameters.md:117-148`; stale `ENDSTATION_BUILDER.md:443`; the PR body and the TAKEN/REVIEW READY evidence | R340-1 | 4f746408a15f494c4b30bdc9add6d7295309dff9 |

No lens is covered clean at this head. A fix commit that touches the builder, tests or docs must be re-covered under each affected lens.

## Real limits

- No Milan or IEEE specification text was available in the repository. Clause statements were checked against repository authorities and the review focus, not against the standards themselves (see R340-F3).
- The full parent, processor, gPTP, Yosys and builder banks were not run, by instruction. For those I relied on the manager's public source-bank evidence. I did not run Verilator, so the pinned tool identity was not needed and not checked. I did not use Docker or act.
- Physical calibration was NOT RUN. Hosted field skips are not hardware proof.
- This is source validation at the head. The final current-dev merge candidate was not built here.

## Pending manager duties

- Publish this report and the manifested receipts.
- Route R340-F1 to R340-F3 to the executor.
- Take the clause decision for R340-F3.
- Optionally file the suggestions as new issues.
- Own hosted and act acceptance at the exact head. The in-progress Verilator shards were not observed completing.
- Build and validate the merge candidate against live dev at the merge turn.
- Obtain the external review. A re-review of any corrected head must re-cover all five lenses.

R340-1 FINISHED
