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
