[A496]

Closes #38
Closes #39
Closes #60
Closes #89

Lane C8: descriptor model lint. Branch `c8-descriptor-lint` from `main`
03c842a7, three commits, head `e6cca1ff`. The design follows the ruling on
#60 (comment 5948872196):

- The lint runs by default inside `gen_desc_image.build()`, with an
  explicit `lint=False` / `--no-lint` opt-out.
- A waiver excuses one check and carries a reason naming its tracking
  issue. It is listed in the layout report and refused when stale.
- `example_milan_8.json` packs with the lint off. A new minimal Milan model
  is the positive case, and every negative case is one named mutation of it.

No port, parameter or register changes.

## Design

- `hdl/aecp/desc/model_lint.py` holds the API: `lint()`, waivers, report,
  digest. `hdl/aecp/desc/model_rules.py` holds the rules.
  - `build()` calls the lint after the existing layout checks, which keep
    their order and text, and before the image is rendered.
  - The rules read the packed bytes at IEEE 1722.1-2021 §7.2 wire offsets,
    and every variable part through the descriptor's own offset field.
- A refusal is an `ImageError` with one line per finding, for example
  `L10 rate-offset: cfg 0 AUDIO_UNIT 0: sampling_rates_offset 143; SET_SAMPLING_RATE reads the list at 144 (IEEE 1722.1-2021 §7.2.3, §7.4.21.1; 07 §3.1)`.
  The CLI exits 1 and writes no file.
- `build(..., lint=False)` / `--no-lint` is for layout vectors and
  deliberate negatives another checker must name. The report then says
  `semantic lint: off`.
- Waivers live in the packed document (`lint_waivers`), with one rule, one
  check, a configuration, a type, an optional index range, and a reason
  naming a tracking issue.
  - A malformed waiver is refused. So is a stale one: a descriptor of its
    scope is missing, or passes its check.
  - Every applied waiver is listed in the report.
- The report gives the values the integrator drives on `entity_model_id_i`,
  `talker_sources_i`, `listener_sinks_i` and `identify_index_i`, and the
  model digest. These stay integrator inputs.
  - `build(adp=...)` / `--adp-*` refuses a driven value that disagrees with
    the model.
  - `build(model_ids=...)` / `--model-ids` refuses a recorded
    entity_model_id whose digest moved.
  - The digest is SHA-256 with the IEEE 1722.1-2021 §6.2.2.8 exclusions,
    entity_id and entity_model_id zeroed.
- Models:
  - `hdl/aecp/desc/milan_min.json` (new) is a minimal Milan model: an AAF
    Talker and Listener, a CRF input, Base formats, one Stream Port per
    direction, INTERNAL and CRF clock sources, the primary IDENTIFY. It is
    recorded in `hdl/aecp/desc/model_ids.json`.
  - `example_milan_8.json` keeps its NOT A COMPLIANCE REFERENCE label, plus
    one line saying the lint is off for it. Its descriptors are unchanged.
  - The `tb/pp_top` fixture is built in C++, never through `build()`, and
    is documented as not a Milan model.

## Items

Every rule, its checks and clauses are listed in 07 §3.1. Each check has a
named negative case in `tb/desc_store/lint_mutations.py`: 56 mutations of
`milan_min.json` cover the 53 checks.

1. **#89, L10 and L6's list** (IEEE 1722.1-2021 §7.2.3, §7.2.32,
   §7.4.21.1, §7.4.23.1; Milan v1.2 §5.3.3.3, §5.3.3.6).
   - L10: AUDIO_UNIT `sampling_rates_offset` 144, `sampling_rates_count`
     1..8, length `144 + 4 × count`, `current_sampling_rate` a listed word.
   - L6: CLOCK_DOMAIN `clock_sources_offset` 76, count ≥ 1, length
     `76 + 2 × count`, the identity list 0..count-1, every entry an existing
     CLOCK_SOURCE.
   - One negative case each.
2. **#38, L9** (Milan v1.2 §5.3.1, §5.3.3.1, §5.6.2; IEEE 1722.1-2021
   §6.2.2.8, §7.2.1).
   - entity_model_id 0 and all-ones are refused (two negative images).
   - A driven `entity_model_id_i` that differs is refused.
   - An unrecorded id is refused, and so is a recorded id whose digest
     moved: one test edits `buffer_length` under the recorded id.
3. **#39, L11** (Milan v1.2 §5.3.3.1, §5.6.2). ENTITY
   `talker_stream_sources` / `listener_stream_sinks` must be the most
   STREAM_OUTPUTs / STREAM_INPUTs of any configuration.
   - The two-configuration negative image: configuration 1 has two talkers
     and the ENTITY says one.
   - The report prints the values, and driven ones are checked.
   - `integrator.md` §6 states the rule for both ports, and the rule for
     `entity_model_id_i`.
4. **#60, L1 to L8**, with F07.2's cardinalities (Milan v1.2 §5.3.2 to
   §5.3.3.11, §6.3, §6.4, §7.3, §7.5; IEEE 1722.1-2021 §7.2, §7.2.1,
   §7.2.2, §7.2.6 Table 7-8).
   - L1: one parent and the minima, including Milan §5.3.3.8's cluster
     minimum per Stream Port.
   - L2: the order IEEE §7.2 walks the hierarchy.
   - L3: Base formats, rate-completeness, configuration uniformity, the CRF
     word.
   - L4: buffer_length, CLASS_A, no CRF+AAF mix, current_format, N ≤ 46,
     and the Table 7-8 layout.
   - L5: the interface index per port.
   - L6: clock-source construction and gPTP with a single interface.
   - L7: input maps, unique static mappings, mono clusters.
   - L8: the primary IDENTIFY at one index in every configuration, and
     `identify_index_i`.
   - The packer's existing refusals (index gap, duplicate, mixed names,
     ENTITY index 1, configuration gap) each gain a negative case.
   - The N cap is corrected from 47 to 46 throughout (#60 comment
     5854263065).
5. **The gate**: `tb/desc_store/test_gen_desc_image.py`, 32 tests. `make`
   in `tb/desc_store` runs it as `generator-check`, so `run_suites.sh` and
   the `hdl` workflow run it too.
   - Each mutation must be refused with its check, and must pack with the
     lint off.
   - A test holds the mutated checks equal to the check list.
   - Waiver tests:
     - removing the waiver brings back the L1 refusal;
     - the waiver kept on a fixed model is refused as stale;
     - past the descriptors, it is stale;
     - it excuses no other check or scope;
     - seven malformed waivers are refused.
   - Check-suppression proof: 53 of 53 checks, each suppressed alone, fail
     the gate.
6. **Docs**:
   - 07 §3.1 (the lint, the rules with their checks, L11, the "not linted"
     list, the #584 waiver), §3.2 and §3.3.1 (46 formats);
   - the REQ-MDL-001 to 011 and REQ-ADP-003/004 rows and GAP-08;
   - 09 §8.4 (new); 04's ADPDU sourcing rows; `integrator.md` §6;
   - the `tb/desc_store` and `tb/pp_top` READMEs.
7. **Parent-visible list**: below.

## Validation

At head `e6cca1ff`:

- `./scripts/run_suites.sh`: rc 0. 33 suites, 1,018,843 checks, 0 failing.
  - `desc_store` runs the new gate first (32 tests), then its 584 RTL
    checks.
  - `pp_top` 8,901 checks.
- These are all rc 0: `./scripts/lint_hdl.sh`, `make check` (diagrams,
  wavedrom, links, matrix, module matrix, parameters, staleness),
  `scripts/gen_matrix.py --check` and `git diff --check 03c842a7..HEAD`.
- Check-suppression proof: each of the 53 checks suppressed alone makes the
  gate fail, 53 of 53. The record is in `tb/desc_store/README.md` and
  09 §8.4.
- Not run: the RTL mutation campaigns, `nvm_port` figures and the yosys
  portability flow. No RTL, harness source or mutation patch changed.

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a`.
- Scratch copy setup: a `git archive` of dev, with `parent-c4-disposition.patch`
  and then `parent-adoption-c8-cdf49d1a.patch` applied, and
  `protocol-processor` at this branch with its gitlink recorded.

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held; the new Python is in the population |
| 3 | `xvlog_gate.py --check` | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (it needs a board implementation report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0, 9 RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 |

The five parent models packed through the lint, at dev `cdf49d1a` and at
PR #634's head `57f4b742`, both patches applied:

| Model | dev | PR #634 |
|---|---|---|
| `arty_current`, `arty_4x4`, `arty_8ch`, `ax7101_1x1_tdm8` | packed, no waiver | packed, no waiver |
| `ax7101_8x8` | packed only with its waiver, which the report lists (`L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived`) | the same |
| `ax7101_8x8`, waiver removed | refused: `L1 port-cluster-minimum` on STREAM_PORT_INPUT 0..7 | the same |

- Two callers were driven at both heads: the builder path, which also runs
  the parent's post-pack shipping checks, and the `gen_aemi_image.py` CLI.
  The SoC caller is gate 36b's SoC test.
- Each model's overlay ADP values (`entity_model_id`, talker sources,
  listener sinks) were passed as `adp=` and agree.


## Parent-visible list

- `gen_desc_image.build()` lints by default:
  `build(model, line_bytes=576, *, lint=True, adp=None, model_ids=None)`.
  - New CLI options: `--no-lint`, `--model-ids`, `--adp-entity-model-id`,
    `--adp-talker-sources`, `--adp-listener-sinks`, `--adp-identify-index`.
  - New refusal texts (`L<n> <check>: ...`, `lint waiver N ...`) and a new
    document key `lint_waivers`.
- The layout report gains a `semantic lint:` block (waivers, ADP values,
  digest). The parent writes it to `aem_desc.map`; no parent code reads it.
- New files beside the packer: `model_lint.py`, `model_rules.py` (imported
  from the packer's own directory), `milan_min.json`, `model_ids.json`.
- `tb/desc_store/test_gen_desc_image.py` stays the one dispositioned DUT
  reader there. It now also reads the two models and `model_ids.json`
  beside the generator. `tb/desc_store/lint_mutations.py` is new and reads
  nothing.
- `example_milan_8.json`: one comment line; DescriptorImage.MILAN_8 does
  not move.
- Text the parent cites changes: 07 §3.1, the compliance rows, 04, 09,
  `integrator.md` §6.
- `parent-adoption-c8-cdf49d1a.patch`, applied after
  `parent-c4-disposition.patch`, touches seven parent files:
  - Gate 36b: the 17 deliberate negatives pack with `lint=False` (the six
    accepted cases keep the lint on), and so do the index-walk and presence
    documents.
  - The `ax7101_8x8` waiver comes from `configs/endstation_ax7101_8x8.yaml`
    (`model_lint_waivers`, milan-fpga#584). It passes through the builder,
    the overlay (emitted only when declared), `aem_specs`, `aem_assemble`
    and `gen_aemi_image.model_to_document` into the document's
    `lint_waivers`. No production caller of `build()` changes; gate 36b's
    test callers pass `lint=False` for its deliberate negatives and its
    index-walk and presence documents.
  - `docs/ENDSTATION_BUILDER.md` §3 gains the row for the new config key,
    which the builder test's gate 32 requires for any accepted key.
- The parent's own L10/L6 checks (`sw/builder/aem_image_checks.py`) now
  duplicate the processor's. Removing them is for the parent's pin-adoption
  lane.

## What remains

- The parent's pin-adoption lane applies the adaptation patch when it moves
  the pin. It may then retire its duplicate L10/L6 checks.
- milan-fpga#584: when the 8×8 input pools gain clusters, the waiver
  becomes stale, the packer refuses it, and it must be removed from the
  config.
- Not linted, and named in 07 §3.1:
  - the formats a statically mapped output may list;
  - interface_flags and entity_capabilities bits;
  - Milan §7.2.2 and §7.2.3's CRF input and output obligations;
  - whether a rate list matches the Audio Unit.

## Round 2

[A499] answers the two round-1 reviews (R434-1: 4 MINOR, R435-1: 6 MINOR)
under the assignment on #60 (comment 5952457756). Nine commits on `e6cca1ff`,
the merge of `main` 2ebd4fe8 and one parent-gate fix; head `9610098`. No port,
parameter or register changes; one RTL comment changes (the 46 cap). The
rulings applied: conform to the standard, and keep a stricter check only
where the processor needs it, cited then as a processor restriction (07 §3.1).

### Findings

1. **CRF format** (R434-1 F1). L3 `crf-format` refuses every CRF-family
   word other than `0x041060010000BB80`; with L4 `current-format` the
   current format is then that word too. The clause is Milan v1.2 §7.3.2
   (the format "shall be used") and §7.3.4 Table 7.1 (the word); §7.3.1 is
   the overview. New negative: a CRF input listing the Milan word and
   44.1 kHz, running at 44.1 kHz (R434-1 E13).
2. **L1 counts and L2 order** (R434-1 F2, R435-1 F1).
   - The survey now reads every IEEE 1722.1-2021 §7.2 count/base pair: a
     Unit's Ports, CONTROLs and other multi-level children, a Port's
     CONTROLs, clusters and maps, and the CONTROLs of a JACK, AVB_INTERFACE,
     CONTROL_BLOCK or PTP_INSTANCE. An owned descriptor is not top-level, so
     `descriptor_counts` counts only the configuration's own (§7.2.2).
   - L2 orders CONTROL only, the multi-level type §7.2 names, in §7.2's walk:
     the configuration's CONTROLs, then each Unit's and its Ports'.
     Single-level types keep no order: the store reads no child range and
     the microcode takes `number_of_maps` from the integrator's amap face.
   - The cluster-order negative is replaced by two CONTROL-order negatives
     (a port's CONTROLs before its unit's; a configuration-level CONTROL
     after a unit-owned one).
   - New positives: a JACK's CONTROL (R434-1 E10), a Unit's SIGNAL_SELECTOR,
     a Unit's and its Port's CONTROLs, cluster ranges in either order
     (R435-1 probe B).
3. **L5** (R435-1 F2). Compared per physical port: a `port_number` keeps its
   index in every configuration that holds it, and a configuration without
   it is not a finding (Milan v1.2 §5.3.3.5). Probe C packs, and so does a
   third port at a shared index. The move negative is now a true move: the
   round-1 mutation replaced port 1 by port 2 at index 0, which the
   per-port rule rightly accepts.
4. **Digest** (R435-1 F3). Exactly IEEE 1722.1-2021 §6.2.2.8's exclusions:
   `object_name` only in the 28 types that carry one (MATRIX_SIGNAL is now
   hashed), the fields the clause lists per type, and in CONTROL, MIXER,
   MATRIX and SIGNAL_TRANSCODER value_details only the current subfields of
   the families it names (Tables 7-121 to 7-124, 7-126). The clause's
   ranges start at each family's UINT8 type, so an INT8 current value stays
   in the digest; that can only demand a new id. `entity_id` and
   `entity_model_id` stay zeroed, stated as beyond the clause. A selector's
   option change under a recorded digest is refused and its current change
   packs (R435-1 probe F). milan_min's recorded digest is unchanged.
5. **The gate** (R434-1 F4, R435-1 F4).
   - A mutation's `detail` names the arm of a check with several; every
     arm has one (78 mutations over 56 checks).
   - New: boundary positives (46 formats, 8 rates, a CRF input's source
     beside an AAF input's), a short-descriptor test, waiver tests where the
     finding differs from the waiver only by type and only by
     configuration (refused, waiver stale), a waiver naming a missing
     configuration.
   - Each of the 13 round-1 survivors fails a named test (table in
     `tb/desc_store/README.md`). One, `covers-ut-current`, deleted a
     redundant condition no test could see; the condition is gone and the
     weakening it guarded is killed.
   - `tb/desc_store/lint_suppression.py` (`make -C tb/desc_store
     lint-suppression`) re-runs the check-suppression proof: 56 of 56.
6. **Model shalls** (R435-1 F5). Linted with negatives: L12
   `descriptor-extent` (Milan v1.2 §5.3.3.1, .2, .5 to .9: each subset
   descriptor's IEEE §7.2 extent) and `descriptor-maximum` (§7.2's 508
   octets), and L8 `identify-format` (§5.3.3.10, IEEE §7.3.5.2). The rest
   is on 07 §3.1's "not linted" list, each with its reason: the gPTP source
   chain (§7.5.2 to §7.5.5), field values no rule names, and non-subset
   types' extents.
7. **46** (R434-1 F3, R435-1 F6). F01.5 `P-N-FORMATS-MAX` ≤ 46; 07 §3.3.1
   and the `KL_aecp_desc_store.sv` comment give 138 + 8·46 + 2·8 = 522 B and
   Annex C 520 B; 576 still covers both. No 47 is stated as a 2021 cap in
   `docs/` or `hdl/`.
8. **Residue and suggestions.** R1: `_family` cites §7.3.3. R2: the parent
   sentence above now reads "No production caller of `build()` changes;
   gate 36b's test callers pass `lint=False` ...". S1: a malformed `adp`,
   `model_ids` or `--model-ids` file is an `ImageError`. S2: waiver keys
   must have their JSON types (nothing is coerced), and a waiver sharing a
   descriptor with an earlier one of its check is refused. S3: the packer
   loads the lint, and the lint its rules, by file path; `sys.path` is
   untouched.

### Merge of `main`

- `main` 2ebd4fe8 (#139, C6) merged with `--no-ff` as `69c7692`.
- One conflict: both sides added a 09 §8.4. Main's §8.4 stays; the lint's
  section is now **09 §8.5**, and its 18 citations moved with it (the
  sections above still say §8.4).
- `git apply --check` on every campaign patch in the merged tree: 205 of
  205 apply.

### Validation (round 2)

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` at the merge `69c7692` | rc 0: 33 suites, 1,019,110 checks, 0 failing; `desc_store` 584, `pp_top` 9,151 |
| `./scripts/run_suites.sh` at `9610098` | rc 0: 33 suites, 1,019,110 checks, 0 failing |
| the gate (`make -C tb/desc_store`) | rc 0: 50 tests OK, then 584 RTL checks |
| check suppression (`lint-suppression`) | control passes; 56 of 56 checks killed |
| `./scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `git diff --check e6cca1ff..HEAD` | all rc 0 |
| the reviewers' planted defects, re-planted on the round-2 code (46), plus 14 on the round-2 arms | 60 of 60 killed |
| R435-1's 12 `milan_min.json` plants | 10 killed; the 2 disclosed fields survive |

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a` with
`parent-adoption-c4c6-ea3fb388.patch` and then
`parent-adoption-c8-cdf49d1a.patch`, the processor at `9610098`:

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (298 Python modules) |
| 3 | `xvlog_gate.py --check` | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (a board report not on this host); gate 36b's 6 accepted cases pack with the lint on |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

The first `check_py_idiom.py` run failed on one undocumented public
function, a nested test helper; `9610098` documents it.

The five parent models through the round-2 lint, at dev `cdf49d1a` and at
PR #634's head `d81198c2`, through the builder caller (with `adp=` from the
overlay) and the CLI caller:
- `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no
  waiver, and their driven ADP values agree.
- `ax7101_8x8` packs only with its #584 waiver, which the report lists.
  Without it, it is refused on exactly STREAM_PORT_INPUT 0..7
  (`L1 port-cluster-minimum`).
- `parent-adoption-c8-cdf49d1a.patch` is unchanged; no round-2 change needs
  it. At PR #634 its one `avdecc/aem_assemble.py` hunk needs its identical
  one-line port (context moved), as in round 1.

### Parent-visible (round 2)

- New refusals, which the parent's five models pass: `crf-format` (any
  non-Milan CRF word), owned descriptors leaving the top-level counts and
  the wider `child-exists` survey, CONTROL-only order, per-port L5,
  `identify-format`, L12's extents and 508 maximum, strict and
  non-overlapping waivers, `ImageError` for malformed checks.
- The report line reads `semantic lint: on (07 §3.1 rules L1 to L12)`.
- The digest moves for models with non-linear CONTROLs, MATRIX_SIGNAL,
  INT8 linear CONTROLs or non-Milan valued types; the parent records none.
- The packer no longer adds its directory to `sys.path`; the parent's
  callers add it themselves.
- Text the parent cites moves: 07 §3.1, 09 §8.5 (was §8.4), F01.5
  `P-N-FORMATS-MAX`, 07 §3.3.1.

### Issue acceptance

Every acceptance item of #38, #39, #60 and #89 is met at this head, and so
is #60's 46-cap correction (comment 5854263065): the four Closes lines
stand.

## Round 3

[A501] answers the two round-2 reviews, R434-2 and R435-2 (both NEGATIVE on
the same two MINORs, F1 and F2), under the assignment on #60 (comment
5956187186). Three commits on `9610098`, head `97f6eac`. No merge. No port,
parameter, register or RTL change.

### Findings

1. **F1, L4 `stream-layout` accepts Milan Annex C** (R434-2 F1, R435-2 F1).
   - Accepted: IEEE 1722.1-2021 Table 7-8 (formats at 138, no redundancy
     tail) and Milan v1.2 Annex C Table C.1 (formats at 136,
     `redundant_offset` 136 + 8N, then R two-octet `redundant_streams`:
     136 + 8N + 2R octets), within §7.2's 508 octets (L12) and the line
     bound. The redundancy tail is accepted because Milan §5.3.3.4 requires
     Annex C for the streams of a redundant pair.
   - The assignment writes the length as 136 + 8N + 8R. Table C.1 (and Table
     7-8) give `redundant_streams` 2·R octets, one descriptor index each, as
     07 §3.2 already states, so the lint takes 2R.
   - Still refused: a formats_offset other than 138 or 136 (a moved list), a
     `redundant_offset` or a length that disagrees with the formats and R, a
     redundancy tail in the Table 7-8 layout (§5.3.3.4 puts a redundant
     pair's streams in Annex C), and R above 8, the maximum both tables give.
     The last is a standard bound, added with its own negative.
   - Not linted (07 §3.1): the redundant-pair rules, which streams pair and
     the pair's consistency. The redundancy seam is processor #69 (wave 3).
   - New positives: every `milan_min` stream in Annex C (R = 0); a redundant
     pair of Stream Outputs in Annex C, each naming the other (R = 1); 8
     redundant streams, the cap's own value. The existing negatives stay,
     and four are added: a Table 7-8 tail of consistent length, 9 redundant
     streams, Annex C with Table 7-8's `redundant_offset`, and Annex C
     counting a redundant stream it lacks.
   - `example_milan_8.json` is still refused with the lint on (L1, L3, L8),
     no longer for its Annex C streams, and its test now requires that.
   - The 07 §3.1 L4 row, the 07 §3.2 Δ note and REQ-MDL-003's Arch cell cite
     Milan §5.3.3.4 and Annex C Table C.1 as accepted. `milan_min`'s
     recorded digest is unchanged (`6d7982fb…`), as is `model_ids.json`.
2. **F2, unpinned arms** (R434-2 F2, R435-2 F2).
   - `identify-format`: one named mutation per arm, eight in all (114
     octets, value type 3, `values_offset` 105, `number_of_values` 2,
     minimum 1, maximum 1, step 1, unit 1), each `detail` naming its arm.
   - The r/u mask stays: an IDENTIFY whose value type carries the r or the
     u flag packs (IEEE §7.3.6.1).
   - L12: a 508-octet descriptor packs, beside the 520-octet negative.
   - Waivers of AUDIO_CLUSTER 1..2 and 2..3 overlap in part: the second is
     refused, and cluster 3's finding stands.
   - The digest is now tested field by field, so the claim is literal:
     - `object_name` in every Table 7-1 type that has one;
     - the first and last octet of every fixed-offset field §6.2.2.8 names,
       with the structural octets beside them (CLOCK_DOMAIN
       `clock_source_index` and ENTITY `current_configuration` among them);
     - every value family's current values in each type the clause names it
       for (MIXER linear, SIGNAL_TRANSCODER, Bode, and CONTROL's whole UTF8,
       SMPTE, sample-rate, gPTP and vendor values among them).
     - The array `unit` and `string`, and MIXER's selector and array values,
       move the digest. The README and 09 §8.5 say exactly this.
   - R434-2 S1 is taken, so that its plants die too: CONTROLs owned by an
     AVB_INTERFACE, a CONTROL_BLOCK, a PTP_INSTANCE or an External Port pack,
     and so does an AVB_INTERFACE that first appears in configuration 1.
   - Correction to Round 2 item 5: at `9610098`, "every arm has one" did not
     hold for `identify-format` (1 of 8 arms). At this head it holds: 89
     mutations over 56 checks, and each of the lint's 84 refusal
     statements, replaced alone by `pass`, fails the gate.
3. **R435-2 S1, one guarded loader.** `gen_desc_image._beside` loads
   `model_lint.py` and binds itself as that module's `beside`, and
   `model_lint` loads `model_rules.py` through it. Both loads share its
   `None`-spec guard (`test_one_guarded_loader`). `model_lint.py` no longer
   loads on its own; every caller reaches it through the packer.

### Validation (round 3)

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` at `97f6eac` | rc 0: 33 suites, 1,019,110 checks, 0 failing; `desc_store` 584, `pp_top` 9,151 |
| the gate (`make -C tb/desc_store`) | rc 0: 58 tests OK, then 584 RTL checks |
| check suppression (`lint-suppression`) | control passes; 56 of 56 checks killed |
| `./scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `git diff --check 9610098..HEAD` | all rc 0 (41 tops; 1,050 links) |
| `git apply --check`, every campaign patch | 205 of 205 |
| R434-2 `plant_r2.py` and `plant_r435_titles.py`, R435-2 `r2_plants.py`, each run unchanged | 37 of 37, 8 of 8, 37 of 37 KILLED (at `9610098`: 17, 8, 27) |
| R434-2's round-1 `plant.py`, unchanged | 24 killed; 4 not applicable (targets rewritten in round 2, ported in `plant_r2.py` and killed); the expected-pass control green |
| each lint refusal statement replaced by `pass`, one per copy | 84 of 84 killed |
| R435-2 `r2_probes.py`, R434-2 `probe_r2.py` | 0 unexpected of 45; A1 and A2 (Annex C) pack, 508 packs, 509 refused |

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a` with
`parent-adoption-c4c6-ea3fb388.patch` and then
`parent-adoption-c8-cdf49d1a.patch`, the processor at `97f6eac`:

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (298 Python modules) |
| 3 | `xvlog_gate.py --check` | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (a board report not on this host); gate 36b as in round 2 |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

The five parent models through the round-3 lint, at dev `cdf49d1a` and at
PR #634's head `d81198c2`, through the builder caller (with `adp=` from the
overlay) and the CLI caller:
- `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no
  waiver, and their driven ADP values agree.
- `ax7101_8x8` packs only with its #584 waiver, which the report lists.
  Without it, it is refused on exactly STREAM_PORT_INPUT 0..7
  (`L1 port-cluster-minimum`). Widened to 0..8, the waiver is refused as
  stale.
- The packing output is byte-identical to round 2's at both heads, model
  digests included. No model packs differently, so
  `parent-adoption-c8-cdf49d1a.patch` is unchanged (sha256 `aa5a88eb…`). At
  PR #634 its one `avdecc/aem_assemble.py` hunk still needs its identical
  one-line port (context moved).

### Parent-visible (round 3)

- L4 `stream-layout` accepts Milan Annex C streams (formats at 136, R ≤ 8
  two-octet `redundant_streams`). Its clause and requirement text change, and
  so do two refusal texts: a Table 7-8 tail ("... in the Table 7-8 layout; a
  redundant pair's streams use Annex C") and a moved list ("formats_offset X,
  not 138 (Table 7-8) or 136 (Annex C)"). New refusal: R above 8. The
  parent's five models pass.
- `model_lint.py` has no loader of its own and loads only through
  `gen_desc_image`, as every caller, the parent's included, already does.
- Text the parent cites moves: 07 §3.1 (the L4 row; the "not linted" list
  gains the redundant-pair rules), the 07 §3.2 Δ note, REQ-MDL-003, 09 §8.5.
- No digest moves for the parent's models; the C8 patch is unchanged.

### What remains (round 3)

- The redundant-pair rules (which streams pair, and the pair's consistency)
  are not linted; the redundancy seam is processor #69 (wave 3).
- R434-2 S2 (prefer a top-level IDENTIFY for the reported index) and the
  carried R434-1 S3/S4 are not taken; the assignment did not ask for them.
- The PR title's "L1 to L11" (R435-2 R1) was the manager's to fix.

### Issue acceptance (round 3)

Every acceptance item of #38, #39, #60 and #89 is still met at `97f6eac`, and
so is #60's 46-cap correction: the four Closes lines stand.

## Round 4

[A504] merges `main` `631eeb34` (PR #142, P141) under the assignment on #60
(comment 5958629222). R434-3 and R435-3 were POSITIVE at `97f6eac`. Two
commits on `97f6eac`, head `bd86f64`: the `--no-ff` merge `3bfc7c6`, then
L6's positive case. No rule changes, and no port, parameter, register or RTL
change.

### Merge of `main`

- `main` `631eeb34` is merged with `--no-ff` as `3bfc7c6`, keeping both
  sides. P141's work merged without conflict: its `tb/pp_top` section D3C
  with six controls and two `sclks-*` patches, the 06 §6.4 and E_SCLKS
  comment credits, 09 §8.2's D3C row and the `tb/pp_top` README. Apart from
  the lane's own README note (the fixture image is not linted), 06,
  `hdl/aecp/ucode` and `tb/pp_top` equal main's.
- Two conflicts, both in rows that P141 restated:
  - **07 §3.1 L6** (`07_memory_maps.md:186`) takes main's statement whole:
    - Milan v1.2 §5.3.3.6's set is a minimum;
    - one INPUT_STREAM source per AAF input is allowed beside the CRF
      input's (IEEE 1722.1-2021 §7.2.9.2, Table 7-17);
    - the consumer's order is INTERNAL 0, CRF 1, AAF input k at 2 + k
      (milan-fpga D1);
    - the identity list may hold up to Table 7-61's 216 entries, and is
      §7.2.32's membership test;
    - BAD_ARGUMENTS is credited to Table 7-141, carrying the current index
      (§7.4.23.1);
    - main's clause column.

    The lint's side keeps the list's place and length (at 76,
    `76 + 2 × count`) and its Checks column. It adds two facts: neither the
    processor nor the lint reads an order, and 76 + 2 × 216 is §7.2's 508
    octets, so L12's `descriptor-maximum` bounds the list. A probe confirms
    the bound: 216 sources pack, and 217 (510 octets) are refused by
    `descriptor-maximum`.
  - **REQ-MDL-005** (`00_MILAN_COMPLIANCE_REVIEW.md:450`): main's clause and
    requirement text. The Arch cell reads "the processor's range check over
    L6's identity list; packer model lint L6, which accepts that set and
    reads no order (defence in depth)". Doc and Ver stay `07 §3.1, 09 §8.5`
    and `DIR`.
- One more line, so that L6 and the check implementing it cite the same
  clause: `domain-source-identity` in `CHECKS` (`model_rules.py:174`) now
  credits IEEE 1722.1-2021 §7.2.32, not §7.4.23.1, as main's L6, 06 §6.4 and
  the E_SCLKS comment do. Only the parenthesis of that refusal changes.
- `git apply --check` on every campaign patch in the merged tree: 207 of
  207 apply (adp_engine 28, maap 27, pp_top dispatch 37 and mutations 42,
  srp_top 73; main added the two `sclks-*` patches).

### L6 accepts main's statement

No rule changes, because the lint already accepted main's L6:
- `crf-input-source` requires exactly one INPUT_STREAM source per CRF input.
- `aaf-input-source` requires, with no CRF input, exactly one source at the
  AAF inputs.
- `internal-source` requires an INTERNAL source where a Stream Output exists.
- Beside a CRF input, the lint sets no count for an AAF input, as §5.3.3.6
  sets none, and it reads no class order.

The new positive case is
`ConformingModelTest.test_a_source_per_aaf_input_beside_crf`
(`test_gen_desc_image.py:455`):
- The model is `milan_min` with eight AAF inputs: STREAM_INPUT 0 and 2..8,
  with STREAM_INPUT 1 as the CRF input.
- Its one CLOCK_DOMAIN lists ten sources: INTERNAL 0, CRF 1 and AAF input k
  at 2 + k. That is the 8x8 shape P141's D3C grades.
- It packs with the lint on and no waiver.

Five stricter L6 readings were planted, one per copy:
- `clock_sources_count` capped at 8;
- the same count capped at 9;
- at most one AAF source beside a CRF input;
- no AAF source beside a CRF input;
- at most two INPUT_STREAM sources.

The merge commit's gate kills 1 of the 5. With the new test, it kills all 5.
The `tb/desc_store` README records the plants, and 09 §8.5 and the README
list the case.

### Validation (round 4)

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` at `bd86f64` | rc 0: 33 suites, 1,019,127 checks, 0 failing; `desc_store` 584, `pp_top` 9,168. Against round 3, only `pp_top` moves: +17, main's D3C checks |
| the gate (`make -C tb/desc_store`) | rc 0: 59 tests OK, then 584 RTL checks |
| check suppression (`lint-suppression`) | control passes; 56 of 56 checks killed (the log equals round 3's apart from its directory) |
| `./scripts/lint_hdl.sh`, `make check`, `gen_matrix.py --check`, `git diff --check 97f6eac..HEAD` and `631eeb34..HEAD` | all rc 0 (41 tops; 1,050 links; 115 REQ rows, 17 GAP findings) |
| `git apply --check`, every campaign patch | 207 of 207 |
| R434-3's scripts, unchanged: `plant_r3.py`, `plant_r2.py`, `plant_r435_titles.py` | 40 of 40, 37 of 37, 8 of 8 KILLED |
| R434-3's round-1 `plant.py`, unchanged | 24 killed; 4 not applicable, as in round 3; the expected-pass control green |
| R435-3's `r3_plants.py` and `r2_plants.py`, unchanged | 15 of 16 and 37 of 37 KILLED. The survivor, `g-own-loader`, is R435-3's S1 suggestion (not taken; see below) |
| the five stricter L6 readings | 5 of 5 killed (1 of 5 without the new test) |

The RTL mutation campaigns were not re-run. The merge changes no RTL, harness
source or campaign patch beyond main's own, which P141 measured at main. The
lane's delta against `631eeb34` is the same 19 files as against `2ebd4fe8`.

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a` with
`parent-adoption-c4c6-ea3fb388.patch` and then
`parent-adoption-c8-cdf49d1a.patch`, the processor at `bd86f64`:

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (298 Python modules) |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet, pinned at `protocol-processor@bd86f646` |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (a board report not on this host); gate 36b's lines equal round 3's |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0 |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS (re-run alone; see below) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

The first `milan_dp` run, started beside `test_builder.py`, failed (rc 2):
`milan_csr.sv` could not find `gen/lwsrp_csr_defaults.svh`. The builder
test's gates 23j and 23k take that tracked file away and put it back while
they run; its mtime is 36 s after the failure. That run is recorded as a
clash between two gates of this run, not a finding. Re-run alone after the
builder test, `milan_dp` passes.

The five parent models through the round-4 lint, at dev `cdf49d1a` and at
PR #634's head `0b066b6e`, through the builder caller (with `adp=` from the
overlay) and the CLI caller:
- At `0b066b6e` every model carries #629's clock sources, one INPUT_STREAM
  per AAF input beside the CRF input's, in the order INTERNAL 0, CRF 1, AAF
  input k at 2 + k:
  - `arty_current` and `ax7101_1x1_tdm8` have 3 sources;
  - `arty_4x4` and `arty_8ch` have 6;
  - `ax7101_8x8` has 10, the new positive case's shape.

  At `cdf49d1a` each model has 2.
- `arty_current`, `arty_4x4`, `arty_8ch` and `ax7101_1x1_tdm8` pack with no
  waiver, and their driven ADP values agree, at both heads.
- `ax7101_8x8` packs only with its #584 waiver, which the report lists.
  Without it, it is refused on exactly STREAM_PORT_INPUT 0..7
  (`L1 port-cluster-minimum`). Widened to 0..8, the waiver is refused as
  stale.
- The packing output is byte-identical to round 3's at both heads, model
  digests included (round 3's #634 head `d81198c2` already carried the
  sources). No model packs differently, so
  `parent-adoption-c8-cdf49d1a.patch` is unchanged (sha256 `aa5a88eb…`),
  and so is the C4 + C6 patch (`67bcd698…`). At PR #634 the C8 patch's one
  `avdecc/aem_assemble.py` hunk still needs its identical one-line port.

### Parent-visible (round 4)

- No parent model packs differently, no digest moves, and both patches are
  unchanged. Every model at PR #634 `0b066b6e`, with #629's clock sources,
  packs under the lint.
- One refusal text changes: `L6 domain-source-identity` now ends
  "(IEEE 1722.1-2021 §7.2.32; 06 §6.4)" instead of "(IEEE 1722.1-2021
  §7.4.23.1; 06 §6.4)". No parent file quotes it.
- Text the parent cites moves: the 07 §3.1 L6 row and REQ-MDL-005 (main's
  restatement plus the lint's columns), 09 §8.5, and the `tb/desc_store`
  README. The parent's own L6 (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`)
  can follow the processor's L6; it is already on the
  `MEDIA_CLOCK_FOLLOWING.md` documentation list.
- Processor totals at this head: `pp_top` 9,168 checks and the sweep
  1,019,127, both main's (P141) plus this lane's unchanged figures.

### What remains (round 4)

- R435-3 S1 (pin that `model_rules` loads through the shared loader) is not
  taken: the assignment is merge-only. R434-2 S2 and R434-1 S3/S4 are still
  open, and so are the redundant-pair rules (processor #69).

### Issue acceptance (round 4)

Every acceptance item of #38, #39, #60 and #89 is still met at `bd86f64`,
and so is #60's 46-cap correction: the four Closes lines stand.
