[R434] NEGATIVE - exact head e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df

# R434-1: internal independent review of processor PR #144 (lane C8, descriptor model lint)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144, issues #38, #39, #60, #89.
- Exact head `e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df`, tree `6abcaef4b82fffccc3e46a8ac51a5448ce17e741`. Three commits on `main` `03c842a780064048b0a1a3de29214174a1c13934`.
- Round R434-1 (round 1). Review start: PR #144 comment 5951873102.
- Scope reconstructed from: README.md and docs/README.md (the repository has no AGENTS.md or CONTRIBUTING.md); the four issue bodies and their acceptance lists; #60 comment 5854263065 (the 47 to 46 cap), the assignment 5948562638, the design STOP 5948825547, the ruling 5948872196 and the review-ready note 5951843868; processor PR #142 (open, head `76b09ff0`) for its Milan 5.3.3.6 statement; then the diff `03c842a7..e6cca1ff` and its history; then the public evidence at milan-fpga `fec8f8ad` `review-evidence/ppC8-r1` (every published sha256 matches MANIFEST.json).
- Prior public review findings on PR #144: none. The PR carries only the two review-start comments and no review. The one prior finding relayed into #60 (comment 5854263065, the 46-format cap) is judged under F3 below. It is only partly resolved at this head.

## Verdict

NEGATIVE. The lint, the waiver mechanism, the ADP report, the digest, the gate and the parent patch do what the ruling asks, and every executable claim I re-ran held. Four MINOR findings stay open:

- F1: the CRF format check is looser than the obligation it implements.
- F2: one L1 check refuses a standard-conforming model.
- F3: the 46-format correction the PR claims "throughout" misses the single-source parameter table.
- F4: the gate leaves five arms of the lint unpinned. Two of them carry claims the docs make.

Issue verdicts:

| Issue | Acceptance items | Met at this head? |
|---|---|---|
| #38 | 1 L9 refusal of 0 and all-ones with negative images; 2 the value to drive emitted and checked; 3 recorded digest with a test that edits a descriptor; 4 integrator.md §6 | All four met. The digest is checked only when `model_ids` is passed, and only this repository's models are recorded. The ruling (5948872196) accepts both limits. |
| #39 | 1 max over all configurations, refused on mismatch, two-configuration negative; 2 values reported; 3 integrator.md §6 for both ports | All three met. |
| #89 | 1 L10 offset, count and length as named `ImageError`; 2 L6 identity list; 3 a negative per refusal in a gate CI runs; 4 example still packs | All four met. Item 4 is met with `--no-lint`, as the ruling allows. Item 3 is wired through `tb/desc_store` `make` in `run_suites.sh` and the `hdl` workflow's `suites` job. That hosted job was still in progress when I looked (below). |
| #60 | 1 refuse L1 to L8 violations; 2 one negative per rule in CI, example builds; 3 a negative per existing layout refusal; 4 one ticket for all REQ-MDL rows. Plus comment 5854263065: correct the processor's 47-format statements under this issue | **Not met in full.** Items 2 to 4 are met. Item 1 is met with two defects: F1 (the CRF arm of REQ-MDL-011 is looser than the row and the issue) and F2 (L1 `descriptor-counts` refuses a conforming model with a jack-owned CONTROL). The 46-cap correction is incomplete (F3). The PR closes #60 and should not, until F1 to F3 are resolved. |

## Findings

### F1: MINOR: `crf-format` accepts a CRF stream that lists, and runs at, a non-Milan CRF format

- **Lenses:** Conformance, Tests.
- **Where:** `hdl/aecp/desc/model_rules.py:475-476`. The check is `"CRF" in kind and CRF_MILAN not in words`. The `CHECKS` row is at `model_rules.py:88` ("a CRF stream lists 0x041060010000BB80").
- **Authority:**
  - Issue #60, REQ-MDL-011: "Missing check: every CRF stream lists exactly the Milan CRF format and sets CLASS_A."
  - Compliance row REQ-MDL-011: "CRF media-clock stream format 0x041060010000BB80".
  - The parent's own shipping checker independently requires every CRF word to equal `0x041060010000BB80`. It cites Milan v1.2 7.3.2 Table 7.1 (milan-fpga `sw/builder/endstation_builder.py` `_validate_stream_formats` at `cdf49d1a`).
- **Evidence:** `receipts/probe_edges.txt` E13. In `milan_min.json`, CRF input 1 is changed to list `[0x041060010000BB80, 0x041060010000AC44]` with `current_format` `0x041060010000AC44`. It packs with the lint on and no finding. The control E14 (AC44 only) is refused, so the check is reachable.
- **Impact:** A shipping model can advertise a CRF Media Clock Input running at a non-Milan CRF format (44.1 kHz base), and the default lint passes it. The check is weaker than the row it is credited to.
- **Required outcome:**
  - Refuse any CRF-family word other than `0x041060010000BB80` in a CRF stream's list. This also forces `current_format` to that word.
  - Add a named mutation for the mixed list.
  - Check the clause cited for `crf-format`. The lint cites Milan v1.2 §7.3.1, §7.3.4; the parent cites §7.3.2 Table 7.1.
- **Verification:** E13 refused with `L3 crf-format`. The gate and the suppression proof stay green.

### F2: MINOR: L1 `descriptor-counts` (and L2 `parent-order`) count a CONTROL owned by a JACK as top-level, so a conforming model is refused

- **Lenses:** Conformance, Tests.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:318-328`. `survey` claims CONTROL ranges only for AUDIO_UNIT, STREAM_PORT_INPUT/OUTPUT and AVB_INTERFACE.
  - `model_rules.py:389-390`. Every unclaimed CONTROL is counted as configuration-level.
  - `model_rules.py:450-457`. `parent-order` uses the same claims.
- **Authority:**
  - IEEE 1722.1-2021 §7.2.2: `descriptor_counts` gives the counts of the top-level descriptors.
  - §7.2.7: JACK_INPUT/JACK_OUTPUT own CONTROLs through `number_of_controls` and `base_control`. Other §7.2 owners, such as EXTERNAL_PORT and INTERNAL_PORT, have the same pair.
  - The lint's own design already treats an owned CONTROL as not top-level (`model_rules.py:390`).
- **Evidence:** `receipts/probe_edges.txt` E10. `milan_min.json` gains JACK_INPUT 0 with `number_of_controls` 1 and `base_control` 1, a CONTROL 1, and `descriptor_counts` listing JACK_INPUT 1 and CONTROL 1 (the top-level count). It is refused: `L1 descriptor-counts: cfg 0 CONFIGURATION 0: CONTROL 1; configuration 0 holds 2 at the top level`. The lint would accept only `CONTROL 2`, which mis-states the top-level count.
- **Impact:** The lint is on by default in `build()` for every consumer. A Milan model that gives a jack (or another owner outside the three the survey knows) a CONTROL is refused, or must carry a waiver for a lint defect. Milan permits jacks, and the parent plans JACK and EXTERNAL_PORT descriptors (ENDSTATION_BUILDER.md row 14, D5). The same `held` count also treats any descriptor of a `TOP_LEVEL` type as top-level whatever its parent. A SIGNAL_SELECTOR owned by an AUDIO_UNIT is one example.
- **Required outcome:** Do one of the following, and add a positive case to the gate:
  - Claim child ranges for every §7.2 owner with a `number_of_controls`/`base_control` pair (at least JACK_*, EXTERNAL_PORT_*, INTERNAL_PORT_*).
  - Or refuse an unsupported owner with its own named check and a clause, rather than mis-counting.
  - Or record the limit in 07 §3.1's "Not linted" list.
- **Verification:** E10 packs, or is refused with an explicit named check documented in 07 §3.1.

### F3: MINOR: the 46-format cap is not corrected in F01.5, though the PR states it was corrected "throughout"

- **Lenses:** Docs, Conformance.
- **Where:**
  - `docs/architecture/01_overview.md:158`, F01.5 (the single-source parameter table, docs/README §2): `P-N-FORMATS-MAX | 16 | ≤47 (IEEE 1722.1-2021 Table 7-8)`.
  - Secondary: `hdl/aecp/KL_aecp_desc_store.sv:105` ("N capped at 47 formats", attributed to Table 7-8).
  - Secondary: `docs/architecture/07_memory_maps.md:326` ("the field limits alone, F ≤ 47 formats").
- **Authority:**
  - #60 comment 5854263065: 47 is the IEEE 1722.1-2013 bound; the 2021 layout caps `number_of_formats` at 46; "the processor statements should be corrected under this issue".
  - The PR body: "The N cap is corrected from 47 to 46 throughout".
  - This head's own 07 §3.1 L4 and §3.2 say ≤ 46, and the lint enforces 46 (`model_rules.py:46`).
- **Impact:** The normative parameter table still states the 2013 cap and credits it to the 2021 table. It now contradicts 07 §3.1/§3.2 and the lint. This is a figure and a clause claim, not wording.
- **Required outcome:**
  - Set F01.5's range to ≤ 46, citing IEEE 1722.1-2021 §7.2's 508-octet maximum and Table 7-8's `formats_offset` 138.
  - Make the store comment and 07 §3.3.1 either say 46, or say plainly that 47 is the 2013 bound used only as sizing headroom. The 576-byte sizing conclusion holds either way.
- **Verification:** `git grep -n -E '(≤ ?|capped at |F ≤ )47'` over `docs/` and `hdl/` finds no 47 stated as the IEEE 1722.1-2021 format cap.

### F4: MINOR: five arms of the lint survive planted deletion, two of them behind claims in 09 §8.4 and the desc_store README

- **Lenses:** Tests, Docs.
- **Where:**
  - `tb/desc_store/test_gen_desc_image.py:323-338`: the waiver scope tests vary the check and the index, never the descriptor type.
  - `tb/desc_store/lint_mutations.py:249`: the `unique-mapping` case duplicates within one AUDIO_MAP.
  - `lint_mutations.py:201-203`: the `parent-order` case covers only the range arm.
  - `lint_mutations.py:229-230`: the `stream-layout` case covers only the redundancy-count arm.
  - The claims "it excuses no other check and no other scope" at `docs/architecture/09_verification.md:292` and `tb/desc_store/README.md:89`.
- **Evidence:** `receipts/planted_defects.txt` (`scripts/plant.py`, 29 plants, each in a disposable copy). The gate stays green (SURVIVED) for each of these:
  - `waiver-ignores-type`: a waiver's type is not compared. A STREAM_PORT_INPUT waiver would then excuse a STREAM_PORT_OUTPUT finding at the same index. The code is correct today (E6), but nothing pins it. This is the exact scope the parent's #584 waiver relies on.
  - `unique-per-map`: uniqueness is reset per AUDIO_MAP. Milan 5.3.3.9 and REQ-MDL-008 say "across all AUDIO_MAPs". The code is correct today (E12), but it is unpinned.
  - `order-no-control-arm`: the "configuration-level CONTROLs first" arm of L2 is deleted.
  - `layout-no-length`: the `stream-layout` body-length arm is deleted.
  - `covers-ut-current`: the "current_format carries no ut" arm of `_covers` is deleted.
- **Impact:** The 53/53 check-suppression proof is correct at check granularity, and I reproduced it. But a regression in these arms would pass CI. The waiver-type gap is the one the ruling's "names one check and a descriptor scope" depends on.
- **Required outcome:** Add a negative case (or a waiver test) for each of the five arms:
  - a STREAM_PORT_INPUT waiver with a cluster-less STREAM_PORT_OUTPUT at the same index;
  - a duplicate mapping across two output AUDIO_MAPs;
  - a configuration-level CONTROL after a unit-owned one;
  - a stream descriptor longer than `138 + 8·N` with consistent offsets;
  - a ut-carrying `current_format` covered only by a wider ut entry.
- **Verification:** Re-run `scripts/plant.py` for the five names. All are KILLED.

### Suggestions (do not affect the verdict)

- **S1 (Robustness).** Malformed checker inputs raise raw exceptions, not `ImageError`. A non-hex `model_ids` key gives `ValueError` (E4). A `--model-ids` file without `"models"` gives `KeyError`. A string `entity_model_id` in `adp` gives `ValueError` while formatting. All fail closed and write nothing. Converting them to `ImageError` would keep the documented refusal contract.
- **S2 (Robustness).** Waiver integers are coerced with `int()`, so `first: 0.7, last: 0.2` is accepted as `0..0` (E5). The coerced scope is printed in the report, so nothing is silent. Requiring JSON integers would make "malformed is refused" exact.
- **S3 (Conformance).** A `current_format` that carries the ut bit and is listed verbatim is accepted (E11). The parent's checker refuses ut in `current_format` (IEEE 1722-2016 Annex I.2.4, as it cites). Consider adding it to `current-format`.
- **S4 (Tests).** `test_mutations` asserts that the named check is present, not that it is the only one. 49 of 56 mutations trip only their check. The other 7 carry inherent cascades (`receipts/mutation_checks.txt`). An example is `sampling_rates_offset 143`, which also trips `current-rate`. Pinning each mutation's exact check set would document the cascades.

## Lens evidence

### Conformance

The 53 checks were read against IEEE 1722.1-2021 §7.2 wire offsets and the clauses they cite. I have no copy of the specifications here. Field offsets were checked against the §7.2 layouts as the repository documents them (07 §3.2). Base-format and ut decoding were checked against the parent's independent oracle `tests/steps/base_format_steps.py`, which is transcribed from Milan v1.2 Table 6.2 and IEEE 1722-2016 Annex I.2.4. The lint matches it.

- **Offsets:**
  - ENTITY: `entity_model_id` 12, stream counts 24/28, `configurations_count` 308, `current_configuration` 310.
  - CONFIGURATION: `descriptor_counts` 70/72.
  - AUDIO_UNIT: ranges 72..78, `current_sampling_rate` 136, offset 140, count 142, list at 144.
  - STREAM: `stream_flags` 72, `current_format` 74, `formats_offset` 82, `number_of_formats` 84, `buffer_length` 128, `redundant_offset` 132, `number_of_redundant_streams` 134, formats at 138.
  - AVB_INTERFACE: `port_number` 96, controls 98/100.
  - CLOCK_SOURCE: type 72, location 82/84.
  - STREAM_PORT: controls 8/10, clusters 12/14, maps 16/18.
  - AUDIO_CLUSTER: `channel_count` 84.
  - AUDIO_MAP: mappings 4/6.
  - CONTROL: `control_type` 82, values 94/96.
  - CLOCK_DOMAIN: list 72/74/76.
  - All consistent.
- **46-format cap:** `(508 − 138) // 8 = 46`. Correct, and enforced (`format-count`, mutation with 47 formats).
- **CRF format word:** `0x041060010000BB80` decodes to CRF_AUDIO_SAMPLE, interval 96, one timestamp per PDU, pull 0, base 48000. This matches Milan v1.2 Table 7.1 as the parent transcribes it. The check is looser than "exactly" (F1).
- **L6 against Milan 5.3.3.6 and PR #142:**
  - The lint requires exactly one INPUT_STREAM source per CRF input. With no CRF input, it requires exactly one at an AAF input. It places no count on AAF-input sources beside a CRF input.
  - This is PR #142's 07 L6 text word for word ("exactly one INPUT_STREAM per CRF-capable input (or on the single AAF input when no CRF input exists) … Beside the CRF input's source, one INPUT_STREAM source per AAF input is allowed").
  - Probes: E2 (CRF plus an AAF-input source) is accepted. E1 (no CRF, two AAF-input sources) is refused, consistent with PR #142's wording.
  - On real models: at milan-fpga PR #634 (both `57f4b742` and the current `d81198c2`), `ax7101_8x8` carries the ten-source shape (INTERNAL 0, CRF 1, AAF inputs 0..7 at 2..9). `arty_4x4` and `arty_8ch` carry six sources. All pass L6 (`receipts/parent_clock_sources.txt`, `receipts/parent_models_lint_634_*.txt`).
- **Missing Milan 5.3.2/5.3.3 'shall's:**
  - None found beyond 07 §3.1's stated "Not linted" list (`entity_capabilities` and `interface_flags` bits, the §7.2.2/§7.2.3 CRF I/O obligations, rate-list truth).
  - L10's `rate-count` ≤ 8 is a processor limit (07 §3.1, SET_SAMPLING_RATE walk), correctly not credited to the standard.
  - Stricter than the standard: F2. Looser than the standard: F1, and S3 (`current_format` ut).

### RTL

- No RTL, harness source, port, parameter or register changed (`git diff --name-only 03c842a7..e6cca1ff`: no .sv/.v/.cpp/.hpp).
- `example_milan_8.json` packs to byte-identical images at base and head: sha256 `20356f59…`, 1880 bytes, checksum `0xBD79A61C` (`receipts/example_image_base_vs_head.txt`). The map gains only `semantic lint: off`.
- The `tb/desc_store` suite with pinned Verilator 5.050 (identity printed in `receipts/desc_store_suite.log`): rc 0, generator gate 32 tests OK, then 584 checks, 584 PASS, 0 FAIL.
- The pp_top fixture is untouched; only its README gains the "not a Milan model" note.
- Clean.

### Robustness (refusal path, waivers, digest)

- **Refusal path:**
  - Every lint refusal is one `ImageError` line: `L<n> <check>: cfg C TYPE I: detail (clause)`.
  - The CLI prints it, exits 1 and writes neither file. This is tested by `CommandLineTest.test_refusal_writes_nothing`, and the planted `cli-writes-first` is KILLED.
  - The existing layout refusals keep their text (the diff changes none) and their order: the lint runs after configuration density. `LayoutRefusalTest` runs each with the lint on and off. The planted `lint-runs-before-layout` is KILLED.
- **Waivers:**
  - A waiver names one check, one configuration, one type and an inclusive index range.
  - A rangeless waiver on a per-descriptor check is refused as stale (E7). A waiver of one type does not excuse another type (E6).
  - The reason must match `repo#N`. Malformed and stale waivers are refused, and applied waivers are listed with their reason.
  - There is no rule-wide or silent waiver. With the lint off, waivers are counted as "not evaluated" in the report.
  - Minor coercion leniency: S2. Raw exceptions on malformed checker inputs: S1. Both fail closed.
- **Digest:**
  - SHA-256 over (cfg, type, index, length, body). It zeroes `object_name`, ENTITY `entity_id`/`entity_model_id`/`available_index`/`association_id`/`entity_name`/`firmware_version`/`group_name`/`serial_number`/`current_configuration`, `current_sampling_rate`, `current_format`, the CLOCK_DOMAIN current source, CLOCK_SOURCE flags and identifier, AVB_INTERFACE MAC and gPTP dataset fields, and CONTROL current values.
  - These are the §6.2.2.8 run-time and per-unit exclusions as the code documents them; I could not compare them against the clause text (limits).
  - Renaming a bound `object_name` keeps the gate green (`scripts/rename_probe.sh`). Changing AUDIO_CLUSTER `format` or `buffer_length` moves the digest and is refused (planted `min-cluster-format`, `min-buffer-2125999`, and mutation `model-digest`).
- No port, parameter or register changed for the ADP report; the values stay integrator inputs.

### Tests

- Gate at head: 32 tests OK (`receipts/gate_head.log`, and again inside `receipts/desc_store_suite.log`).
- The check-suppression proof, reproduced independently by dropping one check's findings at the recorder (`scripts/suppress_one_check.py`): control 32/32 pass; **53/53** suppressions fail the gate (`receipts/suppression_proof.txt`).
- Mutation exclusivity: 49 of 56 mutations trip only their named check; 7 carry cascades (S4).
- The reviewer plant campaign: 29 plants in total.
  - 22 lint and model plants are KILLED.
  - Expected-pass controls: a new `entity_id`, and a rename of both bound name copies. Both stay green.
  - 5 SURVIVED (F4).
- CI wiring: `tb/desc_store/Makefile` `run: generator-check image.bin`. `run_suites.sh` runs `make` in every `tb/*/` and the `hdl` workflow's `suites` job runs `run_suites.sh`.
- Unclean through F1, F2 (missing negative/positive cases) and F4.

### Docs

- 07 §3.1's new section, the L1 to L11 table with its 53 checks, 09 §8.4, 04's ADPDU rows, integrator.md §6, the compliance rows and both READMEs agree with the code and with my runs.
- Two exceptions:
  - F3: F01.5 and two secondary 47s.
  - F4: the "no other scope" claim is broader than its test.
- `example_milan_8.json` keeps its NOT A COMPLIANCE REFERENCE label and gains the one line the ruling asks for.
- Unclean through F3 and F4.

### Parent patch (`parent-adoption-c8-cdf49d1a.patch`, sha256 `aa5a88eb…`)

- Applied after `parent-c4-disposition.patch` to a `git archive` of milan-fpga dev `cdf49d1a`, with the processor at this head recorded as the gitlink (`scratch` setup in `receipts/parent_setup.txt`).
- `lint=False` appears only where the ruling allows:
  - gate 36b's 17 deliberate negatives (`lint=reason is None`, so the six accepted cases keep the lint on);
  - the ENTITY-less index-walk and presence documents.
- The ax7101_8x8 waiver is sourced from `configs/endstation_ax7101_8x8.yaml` (`model_lint_waivers`, reason naming milan-fpga#584). It passes through the builder, overlay, `aem_specs`, `aem_assemble` and `model_to_document`. It is emitted only when declared, so other overlays stay byte-identical.
- One docs row is added in `docs/ENDSTATION_BUILDER.md` §3 (row 45, 71 to 72 rows), manager-accepted.
- The five models through the real lint (`receipts/parent_models_lint.txt`), at dev and at PR #634's `57f4b742` and `d81198c2` (the single `aem_assemble.py` hunk ported by its identical one-line edit, because the context moved):
  - `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no waiver.
  - `ax7101_8x8` packs with the waiver listed (`L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived`).
  - With the waiver removed, `ax7101_8x8` is refused on exactly those 8 ports.
- The reported ADP values equal each overlay's `entity_counts`.
- The parent's `sw/builder/test_builder.py` with both patches: rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`. The one arm not run is gate 11, which needs a board utilization report that is not on this host, the same arm the author reports. Gate 36b's lines show the 6 accepted cases packed with the lint on and the 17 negatives named by the parent's own checker (`receipts/parent_test_builder.log`). A first run stopped at gate 1b on a missing `third_party/verilog-axis` source, because my scratch copy had that submodule empty. With it populated, the rerun passed (`receipts/parent_setup.txt`).

## Reviewer ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | `model_rules.py` 53 checks against IEEE 1722.1-2021 §7.2 offsets and the cited Milan v1.2 clauses; L6 against PR #142's text; probes E1 to E14; parent models at dev and PR #634 | R434-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| RTL | CLEAN | diff file list (no RTL); example image base-vs-head bytes; `tb/desc_store` RTL suite (584/584) with pinned Verilator 5.050; pp_top fixture unchanged | R434-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Robustness | CLEAN (S1, S2 only) | `gen_desc_image.py` build/CLI refusal path and ordering; `model_lint.py` waivers (E5 to E9), digest exclusions; planted `cli-writes-first`, `lint-runs-before-layout`, `waiver-never-stale`, `reason-any-text` | R434-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Tests | UNCLEAN (F1, F2, F4) | `test_gen_desc_image.py`, `lint_mutations.py`; gate run; 53/53 suppression proof; mutation exclusivity; 29-plant campaign; CI wiring | R434-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |
| Docs | UNCLEAN (F3, F4) | 07 §3.1/§3.2/§3.3.1, 01 F01.5, 04 ADPDU rows, 09 §8.4, integrator.md §6, compliance rows, desc_store and pp_top READMEs, `example_milan_8.json` header, PR body | R434-1 | e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df |

## Real limits

- No copy of IEEE 1722.1-2021 or Milan v1.2 was available. Clause and offset judgements rest on:
  - the repository's own layout tables;
  - the parent's independently transcribed oracles (Milan v1.2 Table 6.2 and 7.1, IEEE 1722-2016 Annex I.2.4);
  - the issue and PR #142 texts.
- The §6.2.2.8 exclusion list, the IEEE §7.2.2 "top level" reading behind F2, and the CRF subclause numbering in F1 should be confirmed against the PDFs.
- Processor banks I did not run (the manager ran them at this head): the full `run_suites.sh`, `lint_hdl.sh`, `make check`, `gen_matrix.py --check`, mutation campaigns and the yosys flow.
- Parent sets I did not run: the parent consumer set of 16 and the donor bank of 9. I ran only the parent builder test, plus my own model packing.
- Hosted CI at this head (run 37003999706, push):
  - `docs-gates` and `portability` completed with success.
  - `suites`, which runs the gate, was in progress at review time. It is not evidence here.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- The builder test's gate 11 (board utilization report) did not run. This review does not cover it.

## Pending manager duties

- Hosted/act acceptance of the exact head, including the `suites` job.
- The parent consumer set (16) and donor bank (9) at this head with both patches.
- The final current-dev candidate at the merge turn (source base `03c842a7`, live dev `cdf49d1a`).
- The PR's `Closes #60` should wait for F1 to F3.

## Restore check

The review clone is at `e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df`, tree `6abcaef4b82fffccc3e46a8ac51a5448ce17e741`. Working tree and index equal HEAD, and nothing is untracked. The processor repository has no gitlinks, so there are no submodule pins to verify. Every probe ran in copies under `scratch/`.

R434-1 FINISHED
