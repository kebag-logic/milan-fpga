# [A499] Lane C8 (descriptor model lint), round 2 handoff

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144,
branch `c8-descriptor-lint`. Issues #38, #39, #60, #89.
Assignment: issue #60 comment 5952457756. Reviews: R434-1 (PR #144 comment
5952440176) and R435-1 (PR #144 comment 5952441681). Design ruling: #60
comment 5948872196.

Start head: `e6cca1ff0114f10ea1a5d402d4aa7f45f2c986df`. Round-2 head:
`9610098a47ce070235df17c2846b48d29cc2ce53` (branch `c8-descriptor-lint`,
not pushed by this lane).

## Status

- 2026-10-02 14:40 CEST: TAKEN on #60 (comment 5952472116).
- Items 1 to 8: eight commits plus one record fix; the gate and `make check`
  rc 0 after each.
- Item 9: `main` 2ebd4fe8 merged with `--no-ff` as 69c7692; one conflict.
- Item 10: the five parent models at dev and PR #634's head; the parent
  consumer set of 16 at dev with both patches, all rc 0 at 9610098 (one
  idiom finding at 69c7692, fixed by 9610098).
- 16:19 CEST: `run_suites.sh` rc 0 at 9610098; the closing gates below are at
  that head. REVIEW READY posted on #60 with head 9610098 (comment 5954510064); the lane stops there.
- No STOP condition held: no port, parameter or register changes; the only
  parent change is the unchanged C8 patch: its two items (gate 36b's lint-off
  callers, the 8×8 waiver from its config) and its one docs row.
- PR-BODY.md: the R2 sentence corrected in place, the "Round 2" section
  appended; first line [A496] and the four Closes lines kept (each issue's
  acceptance is met in full).

## Commits (on e6cca1ff, in order)

| Commit | Item | Subject |
|---|---|---|
| de081ed | 1 | CRF format words: only the Milan word (R434-1 F1) |
| 0d9cfc5 | 2 | Ownership through every §7.2 count/base pair; CONTROL-only order (R434-1 F2, R435-1 F1) |
| c3062d0 | 3 | L5 per physical port (R435-1 F2) |
| ad88ecc | 4 | Digest: exactly the §6.2.2.8 exclusions (R435-1 F3) |
| 18d0ec0 | 5 | The gate: every refusal arm, the waiver scope, the plants, the suppression driver (R434-1 F4, R435-1 F4) |
| d7ece66 | 6 | L12 extents and 508 maximum, L8 IDENTIFY format, the "not linted" reasons (R435-1 F5) |
| fabaf0b | 7 | 47 to 46 in F01.5, 07 §3.3.1 and the store comment (R434-1 F3, R435-1 F6) |
| b13303f | 8 | S1 malformed checks, S2 strict and non-overlapping waivers, S3 import by path, R1 |
| a752561 | 5 (record) | The 60-plant campaign figure in the desc_store README |
| 69c7692 | 9 | Merge `main` 2ebd4fe8; 09 §8.4 stays main's, the lint's section is §8.5 |
| 9610098 | 10 | A docstring the parent's Python idiom gate requires (found by gate 2) |

## Findings and changes

Clauses below were read in the standards text: IEEE 1722.1-2021 §6.2.2.8,
§7.2 (general text, Table 7-1, §7.2.1 to §7.2.36 layouts), §7.3.3, §7.3.5.2,
§7.3.6 (Tables 7-121 to 7-130); Milan v1.2 §5.3.1 to §5.3.3.11, §7.2, §7.3,
§7.5.

"Fails without it" names the gate test that fails when the change is undone.
It comes from two runs: the round-2 gate against the round-1 lint
(`hdl/aecp/desc` at e6cca1ff: 28 failures and 12 errors), and the plant
campaign (each plant undoes one arm in a disposable copy).

| Finding | Change (file:line at 9610098) | Clause | Fails without it |
|---|---|---|---|
| R434-1 F1 (CRF) | `model_rules.py:563` `crf-format` refuses every CRF-family word other than 0x041060010000BB80; with L4 `current-format` the current format is then that word. Clause re-cited at `model_rules.py:156` | Milan v1.2 §7.3.2 (the format "shall be used"), §7.3.4 Table 7.1 (the word); §7.3.1 is the overview | `test_mutations` "CRF input lists the Milan word and 44.1 kHz, runs at 44.1 kHz" (R434-1 E13); plant `crf-any-milan` |
| R434-1 F2 (L1 counts) | Survey claims every §7.2 count/base pair: Unit Ports, CONTROLs and other multi-level children (`model_rules.py:71`, `:385`), Port CONTROLs, clusters and maps, and the CONTROLs of a JACK, AVB_INTERFACE, CONTROL_BLOCK or PTP_INSTANCE (`:88`, `:401`). `descriptor-counts` counts only unowned descriptors (`:475`) | IEEE §7.2.2 ("the counts of the top level descriptors"), §7.2.3 to §7.2.5, §7.2.7, §7.2.8, §7.2.13 to §7.2.15, §7.2.33, §7.2.35; §7.3.5.2 (an IDENTIFY may be a Jack's child) | `ConformingModelTest.test_jack_control_is_not_top_level` (R434-1 E10), `test_unit_signal_selector_is_not_top_level`; plants `count-owned-controls`, `no-jack-owner` |
| R435-1 F1 (L2 order) | `_rule_order` (`model_rules.py:523`) orders only CONTROL, by §7.2's walk: configuration first, then each Unit (AUDIO, VIDEO, SENSOR, by index) with its Stream, External and Internal Ports. JACK, AVB_INTERFACE, CONTROL_BLOCK and PTP_INSTANCE CONTROLs are outside the walk. No single-level order is kept: the store reads no child range (07 §3.3) and the microcode takes `number_of_maps` from the amap face (`gen_ucode.py` NMAPS, the only child count it reads) | IEEE §7.2 ("For descriptors which can appear at multiple levels of the hierarchy, such as the CONTROL descriptors...") | `test_single_level_ranges_have_no_order` (R435-1 probe B); the replacement negatives "the input port's CONTROL numbered before its unit's" and "a configuration-level CONTROL after a unit-owned one"; plants `order-all-ranges`, `order-no-control-arm` |
| R435-1 F2 (L5) | `_rule_interfaces` (`model_rules.py:641`) maps each `port_number` to its first index and refuses a later index that differs; a configuration without the port is not a finding. The move negative is now a true move (configuration 1 holds port 1 at index 1): the round-1 mutation changed index 0 from port 1 to port 2, which per-port comparison correctly accepts | Milan v1.2 §5.3.3.5 | `test_second_interface_optional_per_configuration` (probe C, and a third port at index 1); plants `iface-whole-map`, `iface-subset` |
| R435-1 F3 (digest) | `_structural` (`model_lint.py:203`) zeroes exactly the clause: `object_name` only in the 28 types that carry it (`NAMED`, `:72`; MATRIX_SIGNAL now hashed), the listed fields of ENTITY, AUDIO_UNIT, the streams, CLOCK_SOURCE, CLOCK_DOMAIN, AVB_INTERFACE, SIGNAL_SELECTOR, VIDEO_CLUSTER, SENSOR_CLUSTER and MEMORY_OBJECT (`SPANS`, `:78`), and in CONTROL, MIXER, MATRIX and SIGNAL_TRANSCODER value_details only the current subfields of the families the clause names for each (`VALUED`, `:94`; `value_family`, `:153`). The clause's ranges start at each family's UINT8 type, so an INT8 current value stays in the digest (fail-closed). entity_id and entity_model_id stay zeroed, stated as beyond the clause. milan_min's recorded digest is unchanged | IEEE §6.2.2.8; Tables 7-121 to 7-124, 7-126 | `IdentityTest.test_selector_structure_moves_the_digest` (R435-1 probe F, under a recorded digest), `test_exclusions_are_the_clause`; mutation "IDENTIFY reset_time edited under the recorded id"; plants `digest-whole-selector`, `digest-named-all`, `digest-int8-current` |
| R434-1 F4, R435-1 F4 (the gate) | `Mutation.detail` pins the arm of a multi-arm check (`lint_mutations.py`); 78 mutations over 56 checks; boundary positives, a short-descriptor test, waiver type and configuration scope tests; `tb/desc_store/lint_suppression.py` and `make -C tb/desc_store lint-suppression` | the ruling (5948872196) item 2; #60 item 2, #89 item 3 | Every one of the 13 round-1 survivors fails a named test (table below); 60 of 60 plants killed; 56 of 56 checks killed by suppression |
| R435-1 F5 (model shalls) | L12 (`model_rules.py:875`, `:890`): `descriptor-extent` for ENTITY, CONFIGURATION, AVB_INTERFACE, CLOCK_SOURCE, the Stream Ports, AUDIO_CLUSTER and AUDIO_MAP, and `descriptor-maximum` (508) for every type. L8 `identify-format` (`:755`). 07 §3.1's "Not linted" list now gives a reason per item and adds the gPTP source chain (§7.5.2 to §7.5.5), field values no rule names, and non-Milan types' extents | Milan v1.2 §5.3.3.1, .2, .5 to .10; §5.3.3.6 → §7.5.2; IEEE §7.2, §7.3.5.2 | `LintTest.test_fixed_extents` (R435-1 probe D), mutations "AUDIO_MAP 0 with 64 mappings, 520 octets" (probe I), "IDENTIFY maximum 1", the CONFIGURATION and AUDIO_MAP extent mutations; plants `no-format-rule`, `identify-format-off`; R435-1's `cluster-pad-rerec` is now killed |
| R434-1 F3, R435-1 F6 (46) | `01_overview.md:158` F01.5 ≤ 46; `07_memory_maps.md` §3.3.1 and `KL_aecp_desc_store.sv:105-109` 138 + 8·46 + 2·8 = 522 B, Annex C 520 B (comment only) | IEEE §7.2 (508 octets), Table 7-8 (`formats_offset` 138) | `git grep -E '(≤ ?|capped at |F ≤ |<= ?)47' -- docs hdl` is empty; `make check` and `lint_hdl.sh` rc 0 |
| R1 | `model_rules.py:297` `_family` cites §7.3.3 (Stream Formats) | IEEE §7.3.3 | (wording) |
| R2 | PR body: "No production caller of `build()` changes; gate 36b's test callers pass `lint=False` for its deliberate negatives and its index-walk and presence documents." | | (wording, PR-BODY Round 2) |
| S1 | `gen_desc_image.py:486` `_check_inputs`, `:507` `_model_ids_file`: malformed `adp` or `model_ids`, and a `--model-ids` file without `models`, are `ImageError` | | `test_malformed_checks_are_refused`, `test_model_ids_file_without_models`; plant `model-ids-unchecked` |
| S2 | `model_lint.py:228` `_typed` (no coercion), `:269` `_overlaps` (a waiver sharing a descriptor with an earlier one of its check is refused) | the ruling's "malformed is refused" | `test_malformed_waivers` (five typing cases), `test_overlapping_waivers_are_refused`; plants `waiver-coerced`, `overlap-allowed` |
| S3 | `gen_desc_image.py:130` loads `model_lint.py` by path; `model_lint.py:50` `beside()` loads `model_rules.py` by path. Nothing is added to `sys.path` or `sys.modules` | | `test_import_by_path_touches_no_search_path`; plant `lint-on-sys-path` |

The round-1 survivors (R434-1: 5; R435-1: 8; one shared) and the test each
now fails:

| Survivor | Fails |
|---|---|
| `waiver-ignores-type` = `waiver-anytype` | `WaiverTest.test_waiver_scope_is_its_type` |
| `waiver-anycfg` | `WaiverTest.test_waiver_scope_is_its_configuration` |
| `unique-per-map` | `test_mutations` "AUDIO_MAP 1 repeats AUDIO_MAP 0" |
| `order-no-control-arm` | `test_mutations` "a configuration-level CONTROL after a unit-owned one" |
| `layout-no-length` | `test_mutations` "output 8 bytes past its formats, offsets consistent" |
| `covers-ut-current` | The deleted condition was redundant: the comparison already keeps current's `ut` bit, so no test could kill that text. The arm is removed (`model_rules.py:322`), and the weakening it guarded (current's `ut` bit cleared too) fails `test_mutations` "input current_format carries ut, under a wider ut entry" |
| `cap45`, `rates7` | `LintTest.test_boundaries_pack` |
| `crf-ge1` | `test_mutations` "two INPUT_STREAM sources at the CRF input" |
| `aaf-ge1` | `test_mutations` "no CRF input, an INPUT_STREAM source at each AAF input" |
| `entity-cfg` | `test_mutations` "an ENTITY in configuration 1" |
| `iface-subset` | `ConformingModelTest.test_second_interface_optional_per_configuration` (re-planted on the per-port rule as an index-wise comparison) |

## Merge of main 2ebd4fe8 and the renumbering

- `git merge --no-ff 2ebd4fe8` at a752561: merge commit 69c7692, parents
  a752561 and 2ebd4fe8d31e88c44559e934bd624e1c50515ad5.
- One conflict, `docs/architecture/09_verification.md`: both sides added a
  §8.4 after §8.3. Resolved by keeping main's §8.4 (Notifications and
  identify) and renumbering the lane's to §8.5 (The descriptor model lint).
- Every citation renumbered in the merge commit: 15 in
  `docs/00_MILAN_COMPLIANCE_REVIEW.md` (the REQ-ADP-003/004 and REQ-MDL-001
  to 011 rows, the GAP-08 table row and the GAP-08 finding text), 2 in `07_memory_maps.md` and 1 in
  `tb/desc_store/README.md` (anchor `#85-the-descriptor-model-lint-issues-38-39-60-89`).
  Main cites 09 §8.3 only, so no main citation moved.
- Auto-merged without conflict: `00_MILAN_COMPLIANCE_REVIEW.md`,
  `01_overview.md` (F01.5: main's P-EN-IDENTIFY-NOTIFICATION row beside this
  lane's ≤ 46), `integrator.md`, `tb/pp_top/README.md`.
- `git apply --check` on every campaign patch in the merged tree: 205 of 205
  apply (tb/adp_engine 28, tb/maap 27, tb/pp_top aecp_dispatch 35 and
  mutations 42, tb/srp_top 73).
- Re-measured (what the merge touches): `make check`, the full
  `run_suites.sh`, `lint_hdl.sh`, `gen_matrix.py --check`, the parent set.
  Not re-run: the RTL mutation campaigns and the yosys flow. The merge
  changes no RTL against either side's own measurement (the lane changes
  one comment), and main's lane measured its campaigns at 2ebd4fe8.

## Gates and suites (processor)

| Command | Head | Result |
|---|---|---|
| `./scripts/run_suites.sh` | 69c7692 (the merge) | rc 0: 33 suites, 1,019,110 checks, 0 failing. `desc_store` 584 after its `generator-check`; `pp_top` 9,151; main's `aecp_notify` 14 and `originator` 107 |
| `./scripts/run_suites.sh` | 9610098 | rc 0: 33 suites, 1,019,110 checks, 0 failing (`desc_store` 584, `pp_top` 9,151) |
| `make -C tb/desc_store` | 9610098 | rc 0: the gate (50 tests OK), then 584 RTL checks |
| `make -C tb/desc_store lint-suppression` | 9610098 | rc 0: control passes; 56 of 56 checks killed |
| `./scripts/lint_hdl.sh` | 9610098 | rc 0 (41 tops LINT OK) |
| `make check` | 9610098 | rc 0: 41 mermaid and 18 wavedrom blocks, 1,050 links, matrix 115 REQ rows / 17 GAPs, module matrix 94 rows / 0 untested, parameters 27 |
| `python3 scripts/gen_matrix.py --check` | 9610098 | rc 0 |
| `git diff --check e6cca1ff..HEAD` | 9610098 | rc 0 |
| `git apply --check`, every campaign patch | the merge tree | 205 of 205 apply |
| gate and `make check` after each item commit | de081ed to a752561 | rc 0 each time |

Not run, with the reason: the RTL mutation campaigns (`srp_top`, `maap`,
`adp_engine`, `pp_top` aecp, dispatch, D3, ACMP and notify), `nvm_port`
figures and `syn/yosys/run.sh`. Round 2 changes one RTL comment and no
harness source or mutation patch, and the merge changes neither side's RTL
against its own measurement (main's lane measured its campaigns at 2ebd4fe8).

Scratch campaigns at 9610098 (not in the tree):
- Plants: 60 of 60 killed (`plant_campaign.py`: 46 round-1 reviewer plants
  re-planted, 14 on the round-2 arms).
- R435-1's 12 `milan_min.json` plants re-run with its own script: 10 killed;
  the 2 disclosed fields (`interface_flags`, `entity_capabilities`) survive.
- The round-2 gate on the round-1 lint (`hdl/aecp/desc` at e6cca1ff): 28
  failures and 12 errors, each a round-2 behaviour.
- Arm coverage (`arm_coverage.py`): every `ctx.bad()` site of `model_rules.py`
  is reached by the gate.

## Parent consumer set

milan-fpga dev `cdf49d1a`, scratch copy `$VALIDATION_STORAGE/c8-a499/parent-dev`:
- a `git archive` of the read-only checkout (tree 904f3079, equal to the
  checkout's), its four gitlinks recorded;
- `gptp-processor` 5dce647a and `third_party/verilog-axis` 48ff7a7e cloned
  at their pins (from scratch bare clones of their upstreams);
- `parent-adoption-c4c6-ea3fb388.patch`, then
  `parent-adoption-c8-cdf49d1a.patch`, applied with `git apply --index`;
- `protocol-processor` a clone of this branch at 9610098, its gitlink
  recorded, `git submodule init` run. The trusted checkout was not touched.

| # | Gate | Result at 9610098 |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held; 298 Python modules. The first `check_py_idiom` run (at 69c7692) failed: one undocumented public function, a nested test helper. 9610098 documents it |
| 3 | `xvlog_gate.py --check` (alone) | rc 0: 4 findings == ratchet, none new |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a board utilisation report not on this host). Gate 36b: 67 lines, its 6 accepted cases pack with the lint on, the 17 negatives are named by the parent's checker; gate 32: 113 loader keys == 113 across 65 rows |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 49 literal-bound (48 in round 1; the C4C6 patch's `identify_button_i` tie-off carries its rationale), 59 without a rationale (lowerable by 3, as before) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT readers (the new `lint_suppression.py` reads no hdl/ path), 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

`parent-adoption-c8-cdf49d1a.patch` is unchanged (sha256
aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209): no
round-2 change needs it. It still touches seven files: the two gate-36b
callers, the waiver's five-file path and the one `ENDSTATION_BUILDER.md` row.
`parent-adoption-c4c6-ea3fb388.patch` (sha256
67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c) is the
input, applied first and unchanged.

## Parent models packed

Five tracked configs, through the builder caller
(`endstation_builder._entity_model_image`, which also runs the parent's
post-pack shipping checks), again through `build()` with `adp=` taken from
the overlay, and through `avdecc/gen_aemi_image.py` (the CLI caller). The
processor is at 9610098 for both heads.

| Model | dev cdf49d1a | PR #634 head d81198c2 |
|---|---|---|
| `endstation_arty_current` | packed, 0 waivers; driven values agree (0x001BC50AC1000005, 1, 2) | packed, 0 waivers; driven values agree |
| `endstation_arty_4x4` | packed, 0 waivers (talkers 5, listeners 5) | packed, 0 waivers |
| `endstation_arty_8ch` | packed, 0 waivers (5, 5) | packed, 0 waivers |
| `endstation_ax7101_1x1_tdm8` | packed, 0 waivers (2, 2) | packed, 0 waivers |
| `endstation_ax7101_8x8` | packed only with its waiver, reported: `waiver L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: kebag-logic/milan-fpga#584: ...` (9, 9) | the same |
| `endstation_ax7101_8x8`, waiver removed | refused: 8 lines, all `L1 port-cluster-minimum` (STREAM_PORT_INPUT 0..7) | the same |

- Each report says `semantic lint: on (07 §3.1 rules L1 to L12)`. Every
  model passes the round-2 rules: L12's extents (ENTITY 312, CONFIGURATION
  106, AVB_INTERFACE 102, CLOCK_SOURCE 86, ports 20, clusters 90, maps
  8 + 8n), the 508 maximum (STRINGS is 452), L8's IDENTIFY format
  (LINEAR_UINT8, 0/255/255, unitless, 113 octets), the per-port L5 and the
  new top-level counts.
- PR #634 is fetched from `refs/pull/634/head` into a scratch bare repository
  (head d81198c2). `parent-adoption-c4c6-ea3fb388.patch` applies. The C8
  patch's one `avdecc/aem_assemble.py` hunk does not: #634 adds
  `CRF_CLKSRC`/`CLKSRC_TABLE` lines above its context. It was ported by its
  identical one-line edit (`LINT_WAIVERS=spec.get("lint_waivers", [])`), the
  other six files applying unchanged. This is the patch's context, not a
  round-2 change; the pin-adoption lane meets it when it rebases.

Scratch evidence (under `$VALIDATION_STORAGE/c8-a499/`):

| File | Bytes | sha256 |
|---|---|---|
| `plants/plant_campaign.py` | 11678 | d350ee63606531191e64a896e9f12feadec509c426a8470435e8a1e2cb77d656 |
| `plants/campaign-9610098.txt` | 7169 | 88e9652acb0a11b476050f3b0e62cd1a558f9269d72a787f6b5100d4bd3faf22 |
| `logs/suppression-9610098.log` | 8612 | bbed7a22b981b0445bca0e0da70a12f5fdbacb7cfd85ba9ccc7ff240f7e86878 |
| `plants/minplants-item8.txt` | 1312 | d5d5491cac772a7e6c9eb4623470e04afef580d51b9a67aaeea6b46097b441d3 |
| `oldlint/gate-new-on-old.log` | 50046 | b7f383f8b23eb63757408a5ec8a4c547644a4a32ea1dc39fa8db4d8facc93864 |
| `arm_coverage.py` | 1311 | 68f826e45d7c8f908e0ede1ac7d8bab484b83091ae786a4dceef18af712d6d22 |
| `logs/apply-check-merge.txt` | 37 | 2be2baa41e10f1aa54e4e7f82b72d6a3375a3af39388cb33bb5ba1e34a975b98 |
| `logs/run_suites-69c7692.log` | 1746 | 94f85d0500278ffbbd65118995389da0860e165812cc8969f3d9e37bc8117cf2 |
| `logs/run_suites-9610098.log` | 1746 | 94f85d0500278ffbbd65118995389da0860e165812cc8969f3d9e37bc8117cf2 |
| `mkparent.sh` | 2189 | 788f75b5d0ac4ae51f49da4aab874b80e84afe2ea750c947d6c4013124fc8885 |
| `repin.sh` | 608 | b0e24a393a61d0de57b8c4c5a89b3c9b5c77bcfda6e62e9a55bd9a553652c8cd |
| `run_light_gates.sh` | 840 | 393b618f67b4c4c96f43710e56266a3f6925af583036ade797028d8daf9f1505 |
| `run_heavy_gates.sh` | 579 | cb050e05772d26469e7429084e42fd934ab3c0477ab128a041816499b0a6a8f8 |
| `setup_sources.sh` | 806 | 4701bc458a105cde10019b7d0e468a9c6776adcd963dc991ca1cf62335cfc066 |
| `dump_docs.py` | 1235 | 7e5c7ed96fdcb874dd1a9e31003cdcddc94fc124a5471f0ac2fe96115cd8626d |
| `lint_parent_docs.py` | 985 | 6fb5fe6eb32ef92ed42f962eb865c45306bb66b2931dbefd6945705069942716 |
| `pack_models.py` | 2486 | a781c378dd124bb4037c1eedc5fa93dfbed31375cf8d0514544e9972e419958c |
| `pack_cli.sh` | 822 | 9ffb1e17bcbbe3baf19b537c9b2abf81b561a6bf1b86e65fb3e67656233bc212 |
| `logs/pack-dev-9610098.txt` | 4680 | dd3aec2065d54197b1c5f5e8d5d4a1b412a1d2282b2ca1192fc9d96b8cfa9d16 |
| `logs/pack-pr634-9610098.txt` | 4682 | f462fba76f1840b277e04d5e5a9dd422fa27d2b6df664b4b44296a3a305047d4 |
| `gates-dev/test_builder.log` | 99916 | 3c0fade8b55126d3e8420e139d957ec07f39eb2ffe7f803687c7f8cf7b94f16e |
| `gates-dev/pp_shadow.log` | 293769 | 2da4a0bb7e69c9850be72dda8423afe84db9f8360223fa31ad222a67ca0d392d |
| `gates-dev/milan_dp.log` | 1963084 | ab0b7edacf86043e6d43361605cdc1164690e9b7cbd5bd411ea0ae658b29bc00 |
| `gates-dev/milan_dp_render.log` | 153544 | 3211ab2f722360c466abb28e8b0aa0813a0618296a3c13d3fdf41992329d63aa |
| `gates-dev/xvlog_gate.log` | 1320 | f2f5dd081171f5c4c7cdf4fa8d1317965ba392be0d2c195241aa0aab47adc0d3 |
| `gates-dev/check_py_idiom.log` | 461 | 67244e8fbe70cc64d169fa07231ee7c8e1a9b0b644f48e5fea8d9d891bc7a181 |
| `gates-dev/measure_test_evidence.log` | 12577 | b8fcdff852cf5f6b1631027cdce5acd65bf220872a8b39688390a88d4ed9f314 |

## Parent-visible list

Round 1's list stands (PR-BODY), with these round-2 changes:
- New refusals the parent's models pass but a future model could meet:
  - L3 `crf-format`: any CRF-family word other than 0x041060010000BB80;
  - L1 `descriptor-counts` now leaves owned descriptors out of the top-level
    count (a JACK's CONTROL, a Unit's SIGNAL_SELECTOR), and `child-exists`
    reads the ranges of Units, Ports, JACKs, AVB_INTERFACEs, CONTROL_BLOCKs
    and PTP_INSTANCEs;
  - L2 orders CONTROL only; L5 compares per physical port;
  - L8 `identify-format`; L12 `descriptor-extent` and `descriptor-maximum`;
  - waivers: keys must have their JSON types, and a waiver sharing a
    descriptor with an earlier one of its check is refused;
  - a malformed `adp` or `model_ids`, or a `--model-ids` file without
    `models`, is an `ImageError` (was a raw exception).
- The report's first lint line reads `semantic lint: on (07 §3.1 rules L1
  to L12)`. The parent writes it to `aem_desc.map`; no parent code reads it.
- The model digest changes for a model that carries a non-linear CONTROL,
  a MATRIX_SIGNAL, an INT8 linear CONTROL or a non-Milan valued type. The
  parent records no digest; milan_min's recorded digest is unchanged.
- The packer no longer adds its directory to `sys.path`: it loads
  `model_lint.py`, and that loads `model_rules.py`, by file path. The
  parent's callers already put the directory on `sys.path` themselves, and
  no parent file imports `model_lint` or `model_rules`.
- New file `tb/desc_store/lint_suppression.py`: no reader of hdl/ (the
  parent's evidence gate counts 0 unexplained readers).
- Cited text moves: 07 §3.1 (L1, L2, L3, L5, L8, L12 rows, the digest, the
  "not linted" list), 09 §8.5 (was §8.4), F01.5 `P-N-FORMATS-MAX` ≤ 46,
  07 §3.3.1 (522 B, 520 B), and the compliance rows that cite them.
- For the pin-adoption lane: the C8 patch's `aem_assemble.py` hunk needs its
  one-line port at PR #634's head; the parent's own L10/L6 checks still
  duplicate the processor's (round 1's note).
