# [A501] Lane C8 round 3: HANDOFF

Status: done. Items 1 to 3 committed and verified at 97f6eac; item 4 (parent) verified
with no parent change beyond the unchanged C8 patch. REVIEW READY posted on #60
(comment 5957709319) with head 97f6eace064901f223e13abed7026f96bc4df805.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144, branch
  `c8-descriptor-lint`. Start head `9610098a47ce070235df17c2846b48d29cc2ce53` (contains main
  `2ebd4fe8`; no merge this round). Remote confirmed:
  `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`.
- Head: `97f6eace064901f223e13abed7026f96bc4df805`. Three commits added, nothing amended,
  nothing pushed.
- Assignment: issue #60 comment 5956187186 (round 3), answering R434-2 (PR #144 comment
  5956171573) and R435-2 (comment 5956172864). TAKEN: #60 comment 5956192362.
- Parent: milan-fpga dev `cdf49d1a` (read-only checkout, never modified; `git status`
  empty before and after) and PR #634's head `d81198c2` (unchanged since round 2), fetched
  from `refs/pull/634/head` into a scratch bare repository.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `b92f762` | 1 | Accept the Milan v1.2 Annex C stream layout, redundancy tail included, beside Table 7-8 in L4 stream-layout, and list the redundant-pair rules as not linted (R434-2 F1, R435-2 F1) |
| `8b28ab4` | 2 | Pin every identify-format arm with a named mutation, the r and u flags, the 508-octet and Annex C boundaries, partial waiver overlap, the other CONTROL owners and a later interface, and test the digest field by field against 6.2.2.8 (R434-2 F2, R435-2 F2) |
| `97f6eac` | 3 | Load model_lint and model_rules through the packer's one loader so both loads share its None-spec guard (R435-2 S1) |

Item 4 (parent) needs no commit: no parent model packs differently, so the C8 patch is
unchanged.

## Findings: change, clause, the test that fails without it

### Item 1: F1, L4 `stream-layout` (R434-2 F1, R435-2 F1)

Clauses: Milan v1.2 §5.3.3.4 ("A PAAD-AE may use the extension ... as defined in Section C
for any of its Streams and shall use it for the Streams that are part of the redundant
pair"); Milan v1.2 Annex C Table C.1 (formats_offset 136, redundant_offset 136+8*N,
number_of_redundant_streams R, maximum 8, redundant_streams 2*R octets); IEEE 1722.1-2021
§7.2.6 Table 7-8 (formats_offset 138, redundant_offset 138+8*N, R maximum 8,
redundant_streams 2*R). Read from the standards' text this round.

| Change | Where |
|---|---|
| `ANNEX_C_OFFSET = 136`, `REDUNDANT_MAX = 8` | `hdl/aecp/desc/model_rules.py:112-113` |
| `CHECKS["stream-layout"]` cites Milan §5.3.3.4, Annex C Table C.1 and IEEE Table 7-8; text "Table 7-8 (formats at 138, no redundancy tail) or Annex C (formats at 136, at most 8 redundant streams), offsets agreeing with the length" | `model_rules.py:165-167` |
| `_stream_layout`: formats_offset 138 or 136; redundant_offset = formats end; a tail only in Annex C; R <= 8; length = formats end + 2R | `model_rules.py:626-652` |
| helpers `annex_c()` and `redundant_outputs()` | `tb/desc_store/lint_mutations.py:131-153` |
| four new negatives (Table 7-8 tail with consistent length; Annex C R = 9; Annex C with Table 7-8's redundant_offset; Annex C counting a stream it lacks); every existing negative kept | `lint_mutations.py:423-435` |
| positives: every stream in Annex C (R = 0); a redundant output pair in Annex C (R = 1) | `tb/desc_store/test_gen_desc_image.py:442` `ConformingModelTest.test_annex_c_layout` |
| positive at the cap: 8 redundant streams (added in item 2's commit) | `test_gen_desc_image.py:291` `LintTest.test_boundaries_pack` |
| `example_milan_8.json` refused, not for stream-layout | `test_gen_desc_image.py:263` `LintTest.test_example_is_a_layout_vector` |
| L4 row; "not linted": the redundant-pair rules, "the redundancy seam is processor #69 (wave 3)"; Δ note | `docs/architecture/07_memory_maps.md:184`, `:212-214`, `:259-262` |
| REQ-MDL-003 Arch cell | `docs/00_MILAN_COMPLIANCE_REVIEW.md:448` |
| 09 §8.5 rows, `tb/desc_store` README | `docs/architecture/09_verification.md`, `tb/desc_store/README.md` |

Fails without it (`model_rules.py` put back at 9610098, new tests kept): ERROR
`test_annex_c_layout`; FAIL `test_example_is_a_layout_vector`; FAIL `test_mutations` for
the four new mutations (`$VALIDATION_STORAGE/c8-a501/without.sh f1-rules`). Boundary plants on
the new code (`scripts/f1_plants.py`): 9 of 9 killed (Annex C refused, formats end fixed at
138, REDUNDANT_MAX 7 and 9, the tail left out of the length, 8-octet tail entries, the
Table 7-8 tail accepted, an Annex C tail refused, ANNEX_C_OFFSET 137).

Readings, disclosed in the PR body:
- The assignment writes the Annex C length as 136 + 8N + 8R. Table C.1 and Table 7-8 give
  redundant_streams as 2*R octets (descriptor indices), as 07 §3.2 already said. The lint
  uses 2R.
- R <= 8 is refused above 8, the maximum both tables state. It is a standard bound, not a
  processor restriction, and has its own negative. The assignment's "any R the line bound
  and L12 allow" is otherwise met: no other R limit.
- A Table 7-8 descriptor with R > 0 stays refused, now cited as Milan §5.3.3.4 (a
  redundant pair's streams use Annex C) instead of "non-redundant PAAD".

`milan_min`'s recorded digest `6d7982fbd1657a88838ff40bbe0746eaa8600e5be7bebae670e1de0c6f46ae20`
is unchanged (`IdentityTest.test_record_is_current` passes; `model_ids.json` untouched).

### Item 2: F2, unpinned arms (R434-2 F2, R435-2 F2)

| Change | Where | Fails without it |
|---|---|---|
| one mutation per `identify-format` arm (8): 114 octets, value type 3, values_offset 105, number_of_values 2, minimum 1, maximum 1, step 1, unit 1 | `lint_mutations.py:482-498` | each R434-2 `N-identify-no-*` and R435-2 `id-*` plant fails `test_mutations` on the mutation naming its arm |
| an IDENTIFY with the r or u flag packs (IEEE §7.3.6.1: value_type is the low 14 bits) | `test_gen_desc_image.py:399` `test_identify_value_type_flags` | `N-identify-no-mask`, `id-no-mask` |
| a 508-octet descriptor packs (IEEE §7.2) | `test_gen_desc_image.py:291` `test_boundaries_pack` | `N-max-refuses-507-508`, `l12-max-507` |
| partial waiver overlap refused | `test_gen_desc_image.py:600` `test_partly_overlapping_waivers_are_refused` | `N-overlap-identical-only` |
| digest, object_name over every type 0x01..0x28 | `test_gen_desc_image.py:806` `test_object_name_is_the_clause` | (a NAMED change) |
| digest, every fixed-offset §6.2.2.8 field, first and last octet, and its neighbours (`FIXED_EXCLUSIONS`, `:633`) | `test_gen_desc_image.py:820` `test_fixed_exclusions_are_the_clause` | `N-digest-keeps-domain-current`, `N-digest-keeps-current-config` |
| digest, every value family per type (`VALUE_EXCLUSIONS`, `:673`): array unit and string, MIXER linear/selector/array, SIGNAL_TRANSCODER, MATRIX, Bode, whole values | `test_gen_desc_image.py:835` `test_exclusions_are_the_clause` | `N-digest-keeps-bode`, `N-digest-mixer-no-linear`, `N-digest-transcoder-off`, `dig-array-off`, `dig-mixer-all` |
| CONTROLs of AVB_INTERFACE, CONTROL_BLOCK, PTP_INSTANCE, External Port (R434-2 S1) | `test_gen_desc_image.py:363` `test_other_control_owners` | `N-owners-no-avb`, `-ptp`, `-control-block`, `N-unit-no-ext-port-ranges` |
| an AVB_INTERFACE first in configuration 1 (R434-2 S1) | `test_gen_desc_image.py:409` `test_interface_first_in_a_later_configuration` | `N-l5-missing-port-finding` |
| README and 09 §8.5: "field by field" made literal, the round-3 records | `tb/desc_store/README.md`, `09_verification.md` | (docs) |

Clauses: IEEE 1722.1-2021 §6.2.2.8 (exclusion list), Tables 7-121 to 7-126 (value
layouts), §7.2.22, §7.2.24, §7.2.25, §7.2.31 (where CONTROL, MIXER, MATRIX and
SIGNAL_TRANSCODER keep their value fields), §7.3.5.2 and §7.3.6.1 (IDENTIFY and the r/u
flags), §7.2 (508), §7.2.8, §7.2.15, §7.2.33, §7.2.35 (control owners); Milan v1.2
§5.3.3.5, §5.3.3.10.

Plant campaigns, each reviewer script run unchanged from its read-only packet
(`scripts/run_plants.sh`; receipts `receipts/plants_*`):

| Script | at 9610098 | at 97f6eac |
|---|---|---|
| R434-2 `scripts/r2/plant_r2.py` (37) | 17 KILLED, 20 SURVIVED | 37 KILLED |
| R434-2 `scripts/r2/plant_r435_titles.py` (8) | 8 KILLED | 8 KILLED |
| R435-2 `scripts/r2_plants.py` (37) | 27 KILLED, 10 SURVIVED | 37 KILLED |
| R434-2 `scripts/r1/plant.py` (29, round 1) | 24 KILLED, 4 BADPLANT, 1 expected-pass green | the same |

The round-1 script's four BADPLANTs (`iface-count-only`, `order-no-control-arm`,
`covers-ut-current`, `cli-writes-first`) target text round 2 rewrote; R434-2 ported each to
`plant_r2.py` (`P-*`), and all four are killed. `min-new-entity-id(expect-pass)` is the
reviewer's own control and is meant to stay green. The named failing test for each of
R435-2's plants is in `receipts/plants_r435_named_tests.txt`; R434-2's scripts print theirs.

Arm deletion (`scripts/arm_plants.py`): each `ctx.bad(...)` of `model_rules.py`, and each
`raise ValueError`, `refusals`/`problems`/`stale.append` of `model_lint.py`, replaced alone
by `pass`: 84 of 84 killed (`receipts/arms_head_97f6eac.txt`).

Reviewer probes at the head: R435-2 `r2_probes.py` "0 unexpected of 45" (A1, A2 now pack);
R434-2 `probe_r2.py`: A1 accepted, 506/507/508 accepted, 509 refused, A3 arms refused, A3
r-flag accepted, A4 overlaps refused, A5 to A7 accepted.

Not taken (not in the assignment): R434-2 S2 (prefer a top-level IDENTIFY for the
reported index) and the carried R434-1 S3/S4.

### Item 3: R435-2 S1, one guarded loader

| Change | Where |
|---|---|
| `_beside(name)`: spec by path, `None`-spec guard, binds itself as the module's `beside`, runs it | `hdl/aecp/desc/gen_desc_image.py:131-145` |
| `model_lint` declares `beside: Callable[[str], ModuleType]` and loads `model_rules` through it; its own loader is gone | `hdl/aecp/desc/model_lint.py:47-51` |
| test: `model_lint.beside is _beside`; a `None` spec raises `ImportError` naming the file | `test_gen_desc_image.py:903` `CommandLineTest.test_one_guarded_loader` |

Fails without it (both files put back at 8b28ab4): ERROR `test_one_guarded_loader`.
`test_import_by_path_touches_no_search_path` still passes (no sys.path change, no
`model_lint`/`model_rules` module registered). Consequence, disclosed: `model_lint.py`
loaded on its own raises NameError for `beside`; no caller does that (the tests,
`lint_suppression.py`, the reviewers' probes and the parent all reach it through
`gen_desc_image`).

## Gates

| Command | Head | Result |
|---|---|---|
| `python3 -B tb/desc_store/test_gen_desc_image.py` | after each item | rc 0: 51, 57, 58 tests |
| `make -C tb/desc_store lint-suppression` | 97f6eac | rc 0: control passes; 56 of 56 checks killed |
| `make check` | after each item and 97f6eac | rc 0: 41 mermaid + 18 wavedrom, 1,050 links, 115 REQ / 17 GAP, 94 module rows / 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | 97f6eac | rc 0 |
| `git diff --check 9610098..HEAD` | 97f6eac | rc 0 |
| `git apply --check`, every campaign patch | 97f6eac export | 205 of 205 (adp_engine 28, maap 27, pp_top dispatch 35 and mutations 42, srp_top 73) |

## Processor suites

| Command | Head | Result |
|---|---|---|
| `./scripts/run_suites.sh` (exported tree) | 97f6eac | rc 0: 33 suites, 1,019,110 checks, 0 failing; `desc_store` 584 (after the gate), `pp_top` 9,151. The log is byte-identical to round 2's (sha256 94f85d05…) |
| `./scripts/lint_hdl.sh` (exported tree) | 97f6eac | rc 0: 41 tops LINT OK |

Verilator 5.052 (this host). Not run, with the reason: the RTL mutation campaigns,
`nvm_port` figures and the yosys flow; round 3 changes no RTL, harness source or mutation
patch.

## Parent consumer set (16)

milan-fpga dev `cdf49d1a`, scratch copy `$VALIDATION_STORAGE/c8-a501/parent-dev`:
- a `git archive` of the read-only checkout (tree 904f3079, equal to the checkout's), its
  gitlinks recorded;
- `gptp-processor` 5dce647a and `third_party/verilog-axis` 48ff7a7e cloned at their pins
  from fresh scratch bare clones of their upstreams;
- `parent-adoption-c4c6-ea3fb388.patch`, then `parent-adoption-c8-cdf49d1a.patch`, applied
  with `git apply --index`;
- `protocol-processor` a clone of this branch at 97f6eac, its gitlink recorded,
  `git submodule init` run (`scripts/mkparent.sh`). The trusted checkout was not touched.

| # | Gate | Result at 97f6eac |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held; 298 Python modules, 0 undocumented and 0 unannotated public functions, long function 9 <= 9, long module 10 <= 10, too many parameters 7 <= 7, over-long line 0 |
| 3 | `xvlog_gate.py --check` (alone, after every other build) | rc 0: 4 findings == ratchet, none new |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a board utilisation report not on this host). Gate 36b's lines are identical to round 2's (its accepted cases pack with the lint on); gate 32: 113 loader keys == 113 across 65 rows |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: 49 literal-bound, 59 without a rationale (lowerable by 3, as before) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0: 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `docs_check.py` | rc 0, 0 findings across 185 md files |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

The light gates ran while the processor suites ran; the builder test ran beside the heavy
builds; xvlog ran last, alone. Another lane's `milan_dp` build was running on the host at
the same time (not this lane's).

## Parent models packed

Five tracked configs, through the builder caller (`endstation_builder._entity_model_image`,
with the parent's post-pack checks), again through `build()` with `adp=` from the overlay,
then without the waiver; and through `avdecc/gen_aemi_image.py` (the CLI caller). The
processor is at 97f6eac at both heads; `gptp-processor` 5dce647a, `verilog-axis` 48ff7a7e.

| Model | dev cdf49d1a | PR #634 d81198c2 |
|---|---|---|
| `endstation_arty_current` | packed, 0 waivers, driven ADP values agree | the same |
| `endstation_arty_4x4` | packed, 0 waivers | the same |
| `endstation_arty_8ch` | packed, 0 waivers | the same |
| `endstation_ax7101_1x1_tdm8` | packed, 0 waivers | the same |
| `endstation_ax7101_8x8` | packed only with its waiver, listed: `L1 port-cluster-minimum: cfg 0 STREAM_PORT_INPUT 0..7: 8 finding(s) waived; reason: kebag-logic/milan-fpga#584` | the same |
| `endstation_ax7101_8x8`, waiver removed | refused: 8 lines, `L1 port-cluster-minimum` on STREAM_PORT_INPUT 0..7 | the same |
| `endstation_ax7101_8x8`, waiver widened to 0..8 | refused as stale: STREAM_PORT_INPUT 8 does not exist | the same |

The `pack_models.py` output is byte-identical to round 2's at both heads, model digests
included (`receipts/pack-*-97f6eac.txt`). No model packs differently, so
`parent-adoption-c8-cdf49d1a.patch` is unchanged (sha256
aa5a88eb8e04e5ce0d44ec65973e88215860a9ea5317255016409442000ad209).
`parent-adoption-c4c6-ea3fb388.patch` (sha256
67bcd69852e5d090abc635e8dd66e5159667847ebf83d85aba9599d7cff7bd7c) is applied first,
unchanged. At #634 the C8 patch's one `avdecc/aem_assemble.py` hunk was ported by its
identical one-line edit (context moved, as in rounds 1 and 2); its other six files apply.

## Parent-visible list (round 3)

- L4 `stream-layout` now accepts Milan Annex C streams (formats at 136, R <= 8 two-octet
  redundant_streams). Its CHECKS clause and text change, and two refusal texts change: a
  Table 7-8 tail now reads "number_of_redundant_streams N in the Table 7-8 layout; a
  redundant pair's streams use Annex C", and a moved list "formats_offset X, not 138
  (Table 7-8) or 136 (Annex C)". New refusal: R above 8. The five parent models pass.
- `model_lint.py` has no loader of its own: it loads only through `gen_desc_image`, whose
  `_beside` it shares. The parent reaches the lint only through `gen_desc_image`.
- Text the parent cites moves: 07 §3.1 (L4 row, the "not linted" list gains the
  redundant-pair rules), 07 §3.2 Δ note, REQ-MDL-003, 09 §8.5, `tb/desc_store` README.
- No parent model packs differently; no digest moves; the C8 patch is unchanged.

## Scratch evidence

Small receipts and the scratch scripts are in this directory (`receipts/`, `scripts/`):
plant campaigns at 9610098 and 97f6eac, the arm and boundary campaigns, both reviewers'
probes, the parent packing and CLI logs, the parent gate logs and rc files, the suite,
HDL-lint, `make check`, gate and suppression logs.

Large logs stay under `$VALIDATION_STORAGE/c8-a501/`:

| File | Bytes | sha256 |
|---|---|---|
| `gates-dev/test_builder.log` | 99916 | c5491cd6a77280cb10ae8fe7541a6c921028c34dfd228b36a40ff566c4e8ca92 |
| `gates-dev/pp_shadow.log` | 293780 | 9081017ce7b0d7fa533f0f95e62027dd5e61cdd34a082521a83392b94eb1a222 |
| `gates-dev/milan_dp.log` | 1963088 | 3cfbd28c0976a03bdbda784f18a78f5d19f31d5a632223f21579d0e859044c12 |
| `gates-dev/milan_dp_render.log` | 153544 | de269388ef4cb17d1073a45c14d0690244b7ded3597cfaec7f39d816763db309 |
| `suites/run_suites.log` | 1746 | 94f85d0500278ffbbd65118995389da0860e165812cc8969f3d9e37bc8117cf2 |
| `lint_hdl.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |

Scratch trees (not in the output directory): `suites/tree` and `arms/tree` (exports of
97f6eac), `parent-dev`, `parent-pr634`, `src/` (bare clones), `campaign/` work copies
(removed after each plant).
