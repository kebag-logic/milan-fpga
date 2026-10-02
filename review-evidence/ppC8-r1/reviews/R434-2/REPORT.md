[R434] NEGATIVE - exact head 9610098a47ce070235df17c2846b48d29cc2ce53

# R434-2: internal independent review of processor PR #144 (lane C8, descriptor model lint), round 2

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. PR #144 serves issues #38, #39, #60 and #89.
- Exact head `9610098a47ce070235df17c2846b48d29cc2ce53`, tree `949cb1b0144445fcdb061562af371f5588f9a5fe`.
  - It has nine item commits on the round-1 head `e6cca1ff`.
  - Then comes the `--no-ff` merge `69c7692` of `main` `2ebd4fe8d31e88c44559e934bd624e1c50515ad5` (PR #139, C6).
  - Last is one parent-gate fix, `9610098`.
- Review start: PR #144 comment 5955472093.
- Scope was reconstructed in this order:
  - README.md and docs/README.md (the repository has no AGENTS.md or CONTRIBUTING.md);
  - issue #60's body and acceptance;
  - the #60 comments: the 46-cap report 5854263065, the assignment 5948562638, the STOP 5948825547, the ruling 5948872196, the round-2 assignment 5952457756 with its rulings, and the review-ready note 5954510064;
  - the PR body, including its Round 2 section;
  - the diff `2ebd4fe8..9610098a` and its history;
  - then the public evidence:
    - milan-fpga `fec8f8ad` `review-evidence/ppC8-r1`;
    - the author-r2 packet at the `ppC8-review-evidence` archive `36f0c67165783eb00d4a77381318cf5ad68cfa7a`. Every author-r2 sha256 matches that MANIFEST.json, and `parent-adoption-c8-cdf49d1a.patch` is `aa5a88eb…`, byte-identical to round 1.
- Order of work:
  - My own verdict and ledger were fixed before I opened the other reviewer's round-1 report. A first write of that draft failed on a tool precondition. I completed it after seeing only that report's finding titles, and they changed nothing.
  - I read the prior public findings (R434-1 and R435-1) after my independent pass over the diff. They are resolved below.

## Verdict

NEGATIVE. Every R434-1 and R435-1 finding is closed at this head, and I re-ran every executable claim I could. The lint does not refuse any of the five parent models, at dev or at #634, beyond the reported #584 waiver.

Two MINOR findings are open:

- **F1 (Conformance, Docs):** L4 `stream-layout` refuses a stream descriptor in Milan v1.2 Annex C Table C.1 layout. The repository's own REQ-MDL-003 row and 07 §3.2 Δ note call that layout a permitted "may" for any stream. The check cites Milan §5.3.3.4 and IEEE Table 7-8 as its authority, not a stated processor restriction, and the processor does not need it. The round-2 ruling (5952457756) forbids exactly this. The finding is new in this round. The code dates from `e6cca1ff`, and the round-2 ruling brings it into scope.
- **F2 (Tests, Docs):** several arms that round 2 added survive planted deletion, while the PR body and README say "every refusal arm is pinned":
  - 8 of the 9 L8 `identify-format` arms, including the 113-octet length;
  - the L12 508-octet accept boundary;
  - partial waiver overlap.
  - The README and 09 §8.5 also say the §6.2.2.8 exclusions are proven "field by field". Five exclusions can be deleted with the gate green.

The issue acceptance is otherwise met:

- #38, #39 and #89 are met in full, as in round 1, and nothing in round 2 regresses them.
- #60 items 1 to 4 and the 46-cap correction are met.
  - F1 does not stop L1 to L8 refusing violating models. It refuses one more conforming model than the standard allows.
  - So `Closes #60` is not blocked by an acceptance gap. It is blocked only through this NEGATIVE verdict.

## Findings

### F1: MINOR: L4 `stream-layout` refuses the Milan v1.2 Annex C stream layout, which the repository states is permitted, and cites the standard for it

- **Lenses:** Conformance, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:163-164`. The `CHECKS["stream-layout"]` clause reads "Milan v1.2 §5.3.3.4; IEEE 1722.1-2021 §7.2.6 Table 7-8", with the text "formats at 138, no redundancy tail".
  - `model_rules.py:623-638` (`_stream_layout`). It requires `formats_offset` = 138, `redundant_offset` = 138 + 8N and length = 138 + 8N.
  - `docs/architecture/07_memory_maps.md:184`, the L4 row: "the Table 7-8 layout with no redundancy tail (REQ-MDL-003)". The clause column is "Milan §5.3.3.4; IEEE 1722.1-2021 §7.2, Table 7-8". No processor restriction is stated.
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:448`, REQ-MDL-003, which credits "packer model lint L4 stream-layout".
- **Authority:**
  - The round-2 ruling (#60 comment 5952457756): "The default is to conform to the standard; strictness beyond the standard is kept only where the processor needs it, and then it is cited as a processor restriction (07 §3.1), never as the standard."
  - The repository's own reading of Milan v1.2 §5.3.3.4 in 07 §3.2's Δ note (`07_memory_maps.md:250-253`): "Milan v1.2 Annex C Table C.1 is a second normative layout: `formats` at 136, no `timing` field … §5.3.3.4 says 'A PAAD-AE may use the extension … for any of its Streams and shall use it for the Streams that are part of the redundant pair'."
  - REQ-MDL-003 (`00:448`): "Milan Annex C Table C.1 (formats at 136, no `timing`) is a **may** for any Stream".
  - The processor does not need Table 7-8:
    - The Δ note (`07:242-244`) says the processor "reads only `current_format` (@74, the same offset in both layouts)".
    - §3.3 takes every length from the index map.
    - `format-count`'s cap of 46 holds in both layouts.
- **Evidence:**
  - `receipts/r2_probes.txt` A1. In milan_min, STREAM_OUTPUT 0 is rewritten in Annex C layout: formats at 136, no `timing`, 136 + 8N octets, R = 0. The default lint refuses it:
    - `L4 stream-layout: cfg 0 STREAM_OUTPUT 0: formats_offset 136, not 138`;
    - `redundant_offset 144, not 146`;
    - `is 144 bytes; 1 formats make 146`.
  - The control A1b (Table 7-8) packs.
  - The gate itself pins this behaviour. `LintTest.test_example_is_a_layout_vector` (`tb/desc_store/test_gen_desc_image.py:262-267`) requires `example_milan_8.json` to be refused with `L4 stream-layout`. That file is the repository's deliberate Annex C vector (`07:258-263`).
- **Impact:**
  - The lint runs by default for every consumer of the packer (#89). A consumer whose Milan model uses the Annex C layout that §5.3.3.4 permits is refused under a clause that permits it. The consumer must either opt out of the whole lint or carry a waiver that tracks no real defect.
  - The parent emits Table 7-8, so the parent is unaffected.
  - This is a conformance and clause claim, not wording.
- **Required outcome:** do one of the following.
  - (a) Accept the Annex C layout in `stream-layout`: `formats_offset` 136, `redundant_offset` 136 + 8N, length 136 + 8N + 2R, R = 0 on this non-redundant PAAD. `format-count` is unchanged. Add a positive case, and keep the Table 7-8 negatives.
  - (b) Keep Table 7-8 only, as a stated processor or design restriction with its reason. In that case:
    - cite it in 07 §3.1 L4 and in `CHECKS["stream-layout"]` as 07 §3.1, not as Milan §5.3.3.4 / IEEE Table 7-8;
    - add it to REQ-MDL-003's arch cell.
- **Verification:**
  - (a) Probe A1 packs, and the existing `stream-layout` mutations are still refused.
  - (b) A1's refusal text cites the 07 §3.1 restriction.
  - In both cases the gate and `make -C tb/desc_store lint-suppression` stay green.

### F2: MINOR: round-2 refusal arms are unpinned (L8 `identify-format`, the L12 accept boundary, partial waiver overlap), against "every refusal arm is pinned"; the digest's "field by field" claim is broader than its tests

- **Lenses:** Tests, Docs.
- **Where:**
  - `hdl/aecp/desc/model_rules.py:104-106` and `:755-768` (`IDENTIFY_FORMAT`, `_identify_format`). The only negative is `tb/desc_store/lint_mutations.py:445` ("IDENTIFY maximum 1").
  - `model_rules.py:101`, `:883` (`DESCRIPTOR_MAX`). The positive is `test_gen_desc_image.py:289-301`, which reaches 506 octets at most. The negative is `lint_mutations.py:485`, at 520 octets.
  - `hdl/aecp/desc/model_lint.py:269-276` (`_overlaps`). The test is `test_gen_desc_image.py:517-525`, which uses identical scopes only.
  - Claims:
    - the PR body Round 2 §5: "every arm has one (78 mutations over 56 checks)";
    - #60 comment 5954510064: "every refusal arm is pinned (78 mutations over 56 checks)";
    - `tb/desc_store/README.md:81` ("Where a check has several arms, the mutation's `detail` names the arm");
    - `README.md:109` and `docs/architecture/09_verification.md:314` ("field by field").
- **Authority:**
  - The round-2 assignment item 5 (5952457756): "pin every refusal arm".
  - The focus for this round: L12 and the L8 IDENTIFY check "neither may refuse a conforming model".
- **Evidence:**
  - `receipts/r2_plants.txt` (`scripts/r2/plant_r2.py`, 37 plants, one per disposable copy, the whole gate run on each).
  - 17 are KILLED, including all four round-1 plants ported to the round-2 code. These SURVIVE:
    - **`identify-format`.** Each of these can be deleted alone: the 113-octet length (`N-identify-no-length`), `control_value_type`, `values_offset`, `number_of_values`, `minimum`, `step` and `unit`. Probe A3 (`receipts/r2_probes.txt`) shows the head refuses every one of them correctly, so the code is right and only unpinned.
    - **L12 maximum.** `N-max-refuses-507-508` survives. That is a regression which refuses a conforming 507- or 508-octet descriptor. Probe A2 shows the head accepts 506, 507 and 508 and refuses 509.
    - **Overlap.** `N-overlap-identical-only` survives: overlap refused only for identical ranges. Probe A4b shows the head refuses waivers 0..1 then 1..1.
    - **Digest exclusions.** The gate stays green when each of these is removed: CLOCK_DOMAIN `clock_source_index` (`N-digest-keeps-domain-current`), ENTITY `current_configuration`, BODE_PLOT current values, MIXER linear current, SIGNAL_TRANSCODER current. Over-inclusion would refuse an unchanged structure under a recorded id (L9 `model-digest`). The first two are fields the store's overlay rewrites at run time (07 §3.3). Probe A6 shows the head excludes both correctly.
- **Impact:**
  - A regression in the new IDENTIFY format check, in the 508-octet boundary (the conformance edge the focus names), or in the overlap refusal passes the gate that CI runs.
  - The docs and PR body claim more than the gate proves.
  - The 56-of-56 suppression proof is correct at check granularity. I reproduced it twice, but it cannot see arm-level weakening.
- **Required outcome:**
  - one negative per `identify-format` arm: the length, and each `IDENTIFY_FORMAT` field. A table-driven subtest is enough;
  - a positive at exactly 508 octets, beside the 520 negative;
  - a partial-overlap waiver negative;
  - either gate cases for the remaining exclusions (at least `clock_source_index` and `current_configuration`), or "field by field" narrowed in the README and 09 §8.5 to the fields the test edits.
- **Verification:** re-run `scripts/r2/plant_r2.py` for the names above. Each is KILLED, or the docs claim matches the cases that remain.

### Suggestions (do not affect the verdict)

- **S1 (Tests, Conformance):** add positives for the round-2 ownership survey beyond JACK and the Unit/Port walk:
  - CONTROLs owned by an AVB_INTERFACE, a CONTROL_BLOCK, a PTP_INSTANCE or an External/Internal Port;
  - an AVB_INTERFACE that first appears in a later configuration.
  - The head is correct (probes A5, A7a to A7c). The plants `N-owners-no-avb`, `N-owners-no-ptp`, `N-owners-no-control-block`, `N-unit-no-ext-port-ranges` and `N-l5-missing-port-finding` survive.
- **S2 (Conformance):** `identify_index_i` is reported as the lowest index that holds an IDENTIFY in every configuration (`model_rules.py:782-783`). That could be a unit-level IDENTIFY rather than the configuration-level primary. Consider preferring top-level (unclaimed) IDENTIFY CONTROLs for the reported value.
- **S3 (Tests):** an IDENTIFY with the `r` flag set is accepted by the 0x3FFF mask (probe A3). The mask is unpinned (`N-identify-no-mask`). A positive would pin the stated "without the r and u flags" behaviour.
- R434-1 S3 and S4 are carried unchanged, still not adopted:
  - a `ut`-carrying `current_format` listed verbatim is accepted (E11);
  - mutations pin their named check, not their exact check set.

## Prior public findings at this head

| Finding (round 1) | Original severity | Status at 9610098a | Evidence at this head |
|---|---|---|---|
| R434-1 F1 CRF word looser than "exactly" | MINOR | CLOSED | `crf-format` refuses every non-Milan CRF word (`model_rules.py:563-567`), cited Milan v1.2 §7.3.2, §7.3.4 Table 7.1. E13 and E14 are refused (`receipts/r1_probe_edges_rerun.txt`). The mutation "CRF input lists the Milan word and 44.1 kHz, runs at 44.1 kHz" exists. The plant `N-crf-only-current` is KILLED by it. |
| R434-1 F2 JACK-owned CONTROL counted top-level | MINOR | CLOSED | `CONTROL_OWNERS` and `UNIT_RANGES` (`model_rules.py:71-89`). E10 packs. `ConformingModelTest.test_jack_control_is_not_top_level`. The plant `N-owners-no-jack` is KILLED. |
| R434-1 F3 47 not corrected in F01.5 | MINOR | CLOSED | F01.5 reads ≤46 (`01_overview.md:158`). The store comment and 07 §3.3.1 give 522 B / 520 B. My round-1 verification grep `(≤ ?\|capped at \|F ≤ )47` over `docs/` and `hdl/` is empty. |
| R434-1 F4 five unpinned arms | MINOR | CLOSED | All five, re-planted unchanged, or ported where the text moved (`receipts/r1_plants_rerun.txt`, `receipts/r2_plants.txt`), now fail a named test: `waiver-ignores-type` fails `WaiverTest.test_waiver_scope_is_its_type`; `unique-per-map` fails the mutation "AUDIO_MAP 1 repeats AUDIO_MAP 0"; `order-no-control-arm` (ported) fails "a configuration-level CONTROL after a unit-owned one"; `layout-no-length` fails "output 8 bytes past its formats, offsets consistent"; `covers-ut-current` (ported: current's `ut` bit cleared) fails "input current_format carries ut, under a wider ut entry". |
| R434-1 S1 / S2 | SUGGESTION | ADOPTED | E4 is now an `ImageError`. E5/E5b are refused as non-integer. |
| R434-1 S3 / S4 | SUGGESTION | not adopted (carried above) | E11 is still accepted. |
| R435-1 F1 L2 orders single-level types | MINOR | CLOSED | L2 orders only CONTROL (`model_rules.py:523-545`). Probe B is `ConformingModelTest.test_single_level_ranges_have_no_order`. Two CONTROL-order negatives exist. The no-store/microcode-reader claim is checked: GET_AUDIO_MAP takes NMAPS from the amap gather (`gen_ucode.py:335, :937`). |
| R435-1 F2 L5 refuses an interface subset | MINOR | CLOSED | L5 is per `port_number` (`model_rules.py:641-655`). Probe C packs (`test_second_interface_optional_per_configuration`). The true-move negative exists. My ported `iface-count-only` is KILLED. |
| R435-1 F3 digest exclusions | MINOR | CLOSED | Exclusions per type and per value family (`model_lint.py:68-213`). A selector option change is refused and its current change packs (`test_selector_structure_moves_the_digest`). MATRIX_SIGNAL is hashed. milan_min's recorded digest `6d7982fb…` is unchanged from round 1. Gaps in pinning are under F2 above. |
| R435-1 F4 eight surviving plants | MINOR | CLOSED | I re-created each from that review's survivor titles only (`scripts/r2/plant_r435_titles.py`, `receipts/r435_titles_plants.txt`). All 8 are KILLED by named tests (`test_boundaries_pack`, the CRF/AAF "exactly one" mutations, the waiver type and configuration scope tests, "an ENTITY in configuration 1", the port-move mutation). |
| R435-1 F5 unlisted model shalls | MINOR | CLOSED | L12 `descriptor-extent` and `descriptor-maximum` and L8 `identify-format` were added. 07 §3.1's "not linted" list now names the gPTP chain, unnamed fields and non-subset extents. L12 refuses any length of a fixed-size subset type other than its §7.2 extent, which covers its probe D sizes (`test_fixed_extents` pins +2 octets per type). Its 520-octet AUDIO_MAP is refused (mutation). |
| R435-1 F6 47 in three places | MINOR | CLOSED | As R434-1 F3. |
| R435-1 R1 / R2 | RESIDUE | CLOSED | `_family` cites §7.3.3 (`model_rules.py:298`). The PR body sentence now reads "No production caller of `build()` changes; …". |
| R435-1 S1 to S4 | SUGGESTION | ADOPTED | Malformed `model_ids` / `adp` → `ImageError` (`IdentityTest.test_malformed_checks_are_refused`). Strict waiver types and the overlap refusal (`WaiverTest`). The lint is loaded by path (`CommandLineTest.test_import_by_path_touches_no_search_path`). The committed driver `lint_suppression.py`. |

## Lens evidence

### Conformance

- **Wire offsets.** The offsets the rules read were checked against the IEEE 1722.1-2021 §7.2 layouts, and all are consistent:
  - ENTITY 12/24/28/308/310; CONFIGURATION 70/72/74;
  - AUDIO_UNIT ranges 72..134, 136/140/142/144;
  - STREAM 72/74/82/84/128/132/134/138; AVB_INTERFACE 96/98/100;
  - CLOCK_SOURCE 72/82/84; STREAM_PORT 8..18; AUDIO_CLUSTER 84;
  - AUDIO_MAP 4/6/8; CONTROL 80/82/94/96/104;
  - JACK 74/76; CLOCK_DOMAIN 70/72/74/76.
- **L12 extents.** ENTITY 312, CONFIGURATION 74 + 4n (offset 74), AVB_INTERFACE 102, CLOCK_SOURCE 86, STREAM_PORT 20, AUDIO_CLUSTER 90, AUDIO_MAP 8 + 8n (offset 8). Each agrees with the §7.2 field sums.
  - 508 = 524 (AECP cdl maximum) − 12 − 4 (READ_DESCRIPTOR header).
  - The five parent models pass L12 at both heads. A 508-octet descriptor packs and 509 is refused (A2).
  - L12 refuses no conforming model I could construct.
- **L8 `identify-format`.**
  - It requires one CONTROL_LINEAR_UINT8 value (`r`/`u` masked), `values_offset` 104, `number_of_values` 1, minimum 0, maximum 255, step 255, unit 0, and 113 octets (104 + 9).
  - That is the IEEE §7.3.5.2 IDENTIFY definition as the repository states it (Milan v1.2 §5.3.3.10).
  - It checks no default, current or string, so it is no stricter than the clause.
  - The parent IDENTIFY controls pass at both heads.
- **Digest.** Exclusions per type (`SPANS`), `object_name` in the 28 named types, and value-family current subfields (Tables 7-122 to 7-124, 7-126). The span arithmetic was checked against those value-detail layouts (5V + 4 per linear entry, selector current first, array current after 4V + 4).
- **Parent models** (`receipts/parent_models_lint_dev.txt`, `receipts/parent_models_lint_pr634_d81198c2.txt`):
  - The setup is milan-fpga dev `cdf49d1a` and PR #634 head `d81198c2`. `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch` were applied. At #634, the one `aem_assemble.py` hunk was ported by its identical one-line edit, as disclosed (`receipts/parent_patch_apply.txt`).
  - The processor is at this head; gPTP is at its gitlink `5dce647a`.
  - `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no waiver, and the reported ADP counts equal each overlay's `entity_counts`.
  - `ax7101_8x8` packs only with `L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: kebag-logic/milan-fpga#584…`. Without the waiver it is refused on exactly those 8 ports.
- **Round-1 probes re-run** (`receipts/r1_probe_edges_rerun.txt`):
  - E1 is refused and E2 accepted. That matches the L6 text.
  - E10 and E12 are as required. E13 and E14 are refused.
- **Unclean:** F1.

### RTL

- `git diff 2ebd4fe8..9610098a` touches one RTL file, `KL_aecp_desc_store.sv`, and only its comment (46 formats, 522 B / 520 B). No port, parameter or register changed.
- The merge's RTL comes from `main` (C6) and is not this PR's delta.
- `tb/desc_store` with pinned Verilator 5.050 (identity in `receipts/tool_identity.txt`): rc 0. The gate runs first, then 584 checks, 584 PASS (`receipts/desc_store_make.log`).
- `example_milan_8.json` packs to a byte-identical image at main `2ebd4fe8` and at head (`--no-lint`): sha256 `20356f59…`, 1880 bytes. The map gains only `semantic lint: off` (`receipts/example_image_and_milan_min.txt`).
- Clean.

### Robustness

- A malformed `adp` value or `model_ids` key or digest, and a `--model-ids` file without `models`, each raise `ImageError`. The CLI exits 1 and writes nothing (tests, plus E4).
- Waiver keys are strictly typed (E5, E5b, the 14 malformed cases).
- Overlap is refused for identical and partial scopes (A4a, A4b).
- The lint is loaded by path, and `sys.path` is untouched (test).
- The lint runs after the layout refusals. The ported plants `P-cli-writes-first` and `lint-runs-before-layout` are KILLED.
- Short descriptors become findings, not exceptions (`test_short_descriptor`). Every list read is bounds-checked before `unpack_from`.
- Clean. The arm-pinning gaps are counted under Tests (F2).

### Tests

- Gate: 50 tests OK (`receipts/gate.log`).
- `make -C tb/desc_store lint-suppression`: the control passes, and 56 of 56 checks are killed (`receipts/make_lint_suppression.log`, `receipts/lint_suppression.log`).
- An independent port of my round-1 suppression probe gives the same result: the control passes and 56/56 are KILLED (`receipts/r2_suppression_independent.txt`). The unchanged round-1 script no longer applies, because the lint is now loaded by path (`receipts/r1_suppress_unchanged.txt`).
- Round-1 plants re-run unchanged (`receipts/r1_plants_rerun.txt`):
  - 23 are KILLED;
  - 4 are BADPLANT, because their target text was rewritten. All four were ported and are KILLED (`receipts/r2_plants.txt`, `P-*`).
  - The entity-id control stays green, as expected.
  - The single-copy rename control now trips the packer's existing name-binding refusal. Round 1 ran it as the both-copies rename, `rename_probe.sh`, which stays green (`receipts/r1_rename_probe_rerun.txt`).
- Round-2 plants: 37 in total, 17 KILLED and 20 SURVIVED (F2, S1, S3).
- The other reviewer's eight F4 survivors, re-created from their titles: 8 of 8 KILLED.
- Unclean: F2.

### Docs

- **The merge.** It had one conflict. Main's 09 §8.4 (notifications and identify) stays. The lint's section is §8.5, with anchor `#85-the-descriptor-model-lint-issues-38-39-60-89`.
  - There are 18 `§8.5` citations, and every `09_verification.md#85-…` link resolves.
  - No lint citation of §8.4 remains anywhere in `docs/`, `tb/`, `hdl/` or `scripts/`.
  - `make check` rc 0: diagrams, wavedrom, 1050 links, the matrix, the module matrix and params (`receipts/make_check.log`). `gen_matrix.py --check` rc 0.
  - `git diff --check` is clean over `2ebd4fe8..` and `e6cca1ff..`.
  - `git apply --check` on all 205 campaign patches in the merged tree: 205 of 205 (`receipts/campaign_patches_apply_check.txt`).
- The 46-cap is consistent across F01.5, 07 §3.1, §3.2 and §3.3.1, REQ-MDL-003 and the store comment.
- 07 §3.1's L12 and L8 rows and the "not linted" list match the code.
- Unclean: F1 (the L4 row and REQ-MDL-003 cite the standard for a stricter check) and F2 (the "field by field" and "every arm" claims).

## Reviewer ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `model_rules.py` and `model_lint.py` against IEEE 1722.1-2021 §7.2 offsets and extents and the cited Milan v1.2 clauses; L12, L8 `identify-format`, the digest exclusions; probes A1-A7 and E1-E14; the five parent models at dev `cdf49d1a` and PR #634 `d81198c2` | R434-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| RTL | CLEAN | diff file list (one RTL comment); `tb/desc_store` 584/584 with pinned Verilator 5.050; example image byte-identical to main `2ebd4fe8` | R434-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Robustness | CLEAN | `gen_desc_image.py` `_check_inputs`, `_model_ids_file` and the CLI; `model_lint.py` `_typed`, `_parse_waiver`, `_overlaps`, `_apply`, `beside`; probes E3-E9 and A4 | R434-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Tests | UNCLEAN (F2) | `test_gen_desc_image.py` (50 tests), `lint_mutations.py` (78 mutations), `lint_suppression.py`; 56/56 twice; 29 round-1 plants, 37 round-2 plants, 8 re-created R435-1 plants | R434-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |
| Docs | UNCLEAN (F1, F2) | 07 §3.1/§3.2/§3.3.1, 01 F01.5, 00 REQ-MDL-003, 09 §8.4/§8.5 and its 18 citations, `tb/desc_store` README, the store comment, the PR body's Round 2 section; `make check`, `gen_matrix --check`, campaign-patch apply | R434-2 | 9610098a47ce070235df17c2846b48d29cc2ce53 |

## Real limits

- No copy of IEEE 1722.1-2021 or Milan v1.2 was available. Clause and offset judgements rest on the §7.2 field layouts and on the repository's own clause text: 07 §3.2's Δ note and REQ-MDL-003 for F1, and 07 §3.1 for L8.
- Not confirmed against the clause text:
  - the §6.2.2.8 exclusion list and its "from UINT8" range reading;
  - the SIGNAL_TRANSCODER value offsets (80/82/84);
  - the §7.2.2 top-level type list (`TOP_LEVEL`);
  - IDENTIFY step 255.
- Not run, by assignment:
  - `run_suites.sh`, `lint_hdl.sh`, the RTL mutation campaigns and the yosys flow;
  - the parent consumer set of 16, the donor bank of 9 and the parent builder test.
  - I ran only the `tb/desc_store` suite, the docs gates, the campaign-patch apply check and my own model packing.
- Hosted CI at this head (`receipts/hosted_checks_9610098a.txt`):
  - `docs-gates` and `portability` succeeded in both runs, 37025871144 and 37025875967.
  - `suites` was still in progress when I looked. It is not evidence here.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance of the exact head, including the `suites` job.
- The parent consumer set (16) and the donor bank (9) at this head, with `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-c8-cdf49d1a.patch`.
- The final current-dev candidate at the merge turn: source base `2ebd4fe8`, live dev `cdf49d1a`.
- `Closes #60` (and the merge) wait for F1 and F2.

## Restore check

- The review clone is at `9610098a47ce070235df17c2846b48d29cc2ce53`; `write-tree` equals tree `949cb1b0144445fcdb061562af371f5588f9a5fe`.
- `status --porcelain --ignored`, `diff-index HEAD` and `diff-files` are empty.
- The index equals the HEAD tree in mode, blob and path for every entry.
- The repository records no gitlinks (mode 160000: 0), so there are no submodule pins to verify (`receipts/restore_check.txt`).
- Every probe ran in copies under `scratch/`, which is not published.

R434-2 FINISHED
