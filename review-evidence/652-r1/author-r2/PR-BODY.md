[A533]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — R478-1 F1 and R479-1 F1 answered, S2 taken, S1 judged, S3 open, dev merged.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN: every local gate this change touches is rc 0 at the head `d5e743440a56c77c43241879226b851abb3c62ac`. Round 2 merged dev `c0280fc0` (`--no-ff`).
- **Builder bank:** `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: no Arty `mf48` build tree on this host). Gate 24a (d) and (e) turn 2/2 planted controls red each; gate 38 turns 9/9 red.
- **Read-only gates:** 33 docs, ratchet and resmap gates, the Python idiom ratchet among them (`long module: 10 <= 10`).
- **Builder consumers:** 9 gates, including the record-space gate and its 21 negative controls.
- **Suites:** `nvm_backend` (751 checks, 4 negative controls red) and `nvm_cosim` (465 checks, 39/39 mutants killed).
- **Resource map:** the real `shapes` step (7 built, 2 refused as expected) and three planted plans (each rc 1).
- **Mutation campaign:** 19/19 planted-defect verdicts as expected, R478-1's r3 and r11 among them.
- **Byte identity:** every artifact of all five tracked configurations (120 files) regenerates with a sha256 manifest identical to the round-1 base's, and `git status` stays clean.

The full Verilator sweep (59/59 suites) and Yosys portability (55/55 tops) ran at `d33bdc3d`. No RTL, testbench, builder or configuration file of this lane changed after it. The RTL and testbench changes the dev merge brought (the CRF unbind of #653/#655) were validated in their own lane and are not re-run here; the candidate-merge validation stays with the merge step.

`652-builder-names` -> `dev`.

## Linked Issue / roles

Closes #652
Relates to #649

Executor: `[A533]`
Internal cleared-context reviewer: `[R478]`
External reviewer: `[R479]`

## Description

The builder accepted a configuration whose AEM model has more writable names
than the saved-state backend's NAME block holds (the 8x8 TDM8 variant: 235
against 128), so the refusal surfaced only at synthesis (`KL_nvm_backend`'s
elaboration guard, Vivado `Synth 8-6058`). It is now refused when the
configuration is generated, before any file is written, naming both figures
and the RTL declaration the capacity is read from. The executor's STOP on the
D8 builder contract was ruled "refuse at generation" with two follow-ups
(the #652 thread), which this PR also carries.

| Piece | Change |
|---|---|
| `hdl/milan/KL_nvm_backend.sv` | The NAME capacity is one named declaration, `localparam int unsigned N_NAME_MAX_C = 128;` (ids `0x80..0xFF`), and `g_refuse_names` bounds `N_NAME_P` by it. No port, register, parameter or default changes; the elaborated message is byte-identical. |
| `sw/builder/endstation_builder.py` | `nvm_name_capacity()` reads exactly one live decimal `N_NAME_MAX_C` declaration (zero or two refuse) with its `path:line`; `_adp_name_entries()` refuses a count above it inside the write-free derivation pass. |
| `sw/builder/test_builder.py` | Gate 38: 128 names built, 129 and 235 refused before any write naming both figures; counts graded independently; nine planted defects. Gate 24a: (d) at 8 routed capture channels (123 names, same subject); (e) the over-wide pool refused by the name count, its 16-bit ROM ceiling checked on its own overlay and, with the capacity planted at its count, through the build; each with planted controls. |
| `syn/resmap/yosys_sweep.py`, `syn/resmap/sweep_plan.json` | `shapes` records every builder outcome in `outcomes.json`; a refusal is a refused point with its refusal line. The two 235-name variants are `"expect": "refused"` with the cause their line must carry pinned. An unexpected refusal, a refusal for another cause, an expected refusal that builds, and a crash each fail the step. `run` does not price a refused point; `summary` records it. `generate_shapes()` is the step's loop, callable on a synthetic tree. |
| `syn/resmap/yosys_sweep_selftest.py` | The sweep's builder-refusal arms, run by `yosys_sweep.py --selftest` against the running module: the outcome classifier; the real builder's refusal of both pinned variants, carrying the pinned cause; the step's verdict through a stand-in builder (every outcome expected gives rc 0, each of the four surprises gives rc 1); a refused point through `run` and `summary`. The plan arms stay in the sweep: each malformed expectation or cause must be refused with its own message. |
| `syn/resmap/resmap_models.py`, `syn/resmap/resmap_tables.py` | The models count a builder-refused point as refused and give it no marginal. `guards.by_builder` names the builder-refused points and is absent when there are none. An end-to-end `build()` arm holds both cases. The refusals table says who refused each point; its arm reads a hand-made `by_builder`. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | The refusals and datapath-marginals tables regenerated through `resmap_tables.py --write` (the two points are refused by the builder and no longer priced); the 24 other tables and every fit are unchanged; prose restated. |
| `scripts/check_nvm_record_space.py`, `scripts/nvm_allocation_table.py`, `scripts/nvm_contract.py` | Check 14, in its own module: every figure in the saved-state design's section 4.2 allocation table is checked against the inventory the gate derives for the two shapes its columns name. A row without one cell per header column is a finding. Three planted controls: a stale count, a dropped figure and an extra cell. |
| `docs/design/SAVED_STATE_FASTCONNECT.md` | Section 4.2 at the current shapes (names 39 and 107, records 54 and 164, highest ids `0xA6` and `0xEA`), bound by check 14. |
| `docs/ENDSTATION_BUILDER.md` | D8: the NAME block refuses the stress shape first, naming both figures; the 16-bit ROM ceiling is the second limit. Section 4: the refusal and its source. |

The refusal for the 8x8 TDM8 variant:

```text
CONFIG ERROR: this AEM model has 235 writable names and the saved-state backend holds 128 NAME records (N_NAME_MAX_C, hdl/milan/KL_nvm_backend.sv:247): each writable name is one saved record, so KL_nvm_backend would refuse this shape at elaboration. The model is 107 over: remove named descriptors (streams, clusters or clock sources)
```

Acceptance (#652, its lane comment and the ruling):

1. Refused at generation time, both figures named, the capacity read from the
   RTL declaration and never mirrored: met (gate 38; the builder holds no copy
   of 128). The D8 contract is restated to match and gate 24a holds it.
2. Boundary test with a planted control per check: met (gate 38: 128
   accepted, 129 and 235 refused, nine controls; gate 24a (d) and (e): two
   controls each).
3. Tracked configurations build unchanged: met. Every artifact of all five
   tracked configurations regenerates byte-identically against the base
   (120 files; re-run at the round-2 head; `git status` stays clean after
   regeneration).
4. Ruling item 2: the `shapes` step records a builder refusal fail-closed with
   its line; the two variants are refused-by-builder points; the page's two
   refused-point tables were regenerated through the generator and every
   table equals a fresh generation. Round 2 holds the step's verdict and the
   `by_builder` producer with self-test arms, and pins the refusal's cause.
5. Ruling item 3: section 4.2's counts are the current ones, checked by the
   record-space gate against its derivation, including a row that lost or
   gained a figure.

## Round 2

Answers R478-1 (PR #660 comment 5984662963) and R479-1 (comment 5984636580),
per the assignment in the #652 thread (comment 5984666082).

| Commit | Item | Change |
|---|---|---|
| `ef236411` | 5 | Merge dev `c0280fc0` (`--no-ff`). None of dev's 12 files overlaps this lane. |
| `b71979dc` | 1 | R479-1 F1. Check 14 refuses a section 4.2 row whose cell count is not the header's, naming the column with no figure or the cells past the last. It used to compare the shorter list. Planted controls `short_allocation_row` and `long_allocation_row` sit beside `stale_allocation_table`. |
| `694e2b18` | 2 | R478-1 F1. `generate_shapes()` is the `shapes` loop, callable without an export. A stand-in-builder arm gives rc 0 when every outcome is the expected one, and rc 1 on an unexpected refusal, an expected refusal that builds, and a crash. A `resmap_models.py` arm runs `build()` end to end: `guards.by_builder` names the builder-refused point and is absent when there is none. |
| `94a12eb8` | 3 | R479-1 S2. Both expected refusals pin `"cause": "writable names and the saved-state backend holds"`. A refusal without it fails the step. `load_plan` refuses an expected refusal with no cause and a cause on a built variant. The real builder's line is read for both variants, and the stand-in has a foreign-cause control. |
| `d5e74344` | 2, 3 | Each plan-validation arm requires its own refusal message. Without this, the cause check refused the expectation arm's plan, and a removed expectation check went unnoticed. My own mutation run found it. |

**Two modules moved, and why.** The Python idiom gate holds modules over
1,000 lines to a ratchet of 10 that may only go down. `check_nvm_record_space.py`
(998 lines) and `yosys_sweep.py` (995) would have crossed it. So this PR's
own code moved out, along seams the tree already uses:

- check 14 to `scripts/nvm_allocation_table.py`, as `nvm_map_checks.py` does
  for #501;
- the sweep's builder-refusal arms to `syn/resmap/yosys_sweep_selftest.py`,
  as `check_rtl_source_lists_selftest.py` does.

The arms receive the running module, so a defect planted in memory is what
they exercise. The r3 and r11 anchors are unmoved.

**The bar.** R478-1's `scripts/mutate_module.py`, used unchanged:

- r3 (`failures += outcome != expected` -> `failures += outcome == "failed"`)
  turns `yosys_sweep.py --selftest` red: "an unexpected refusal exited 0, not
  1" and "an expected refusal that builds exited 0, not 1".
- r11 (`result["guards"]["by_builder"] = builder` -> `pass`) turns
  `resmap_models.py --selftest` red: "with a builder-refused point,
  guards.by_builder is None".
- The unmutated self-tests stay green.

Across 18 mutants and one unmutated control, every verdict is as expected
(19/19).

**Before and after.** Under `2f0f5929`'s code, run in memory under its real
path, each planted input passed:

- the page row with its 8x8 figure dropped: rc 0;
- the same row with an extra cell: rc 0;
- the plan with a foreign cause: rc 0.

At the head each gives rc 1.

**S1, no change.** `scripts/nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)` is
the record-space gate's independent expectation of the section 4.2 design
contract, not a builder mirror. It predates #652. The builder holds no copy of
128 and reads `N_NAME_MAX_C`. Gate 38 pins `_NAME_BLOCK_RECORDS = 128` on its
own.

**S3, open.** See Known limitations.

## Authoritative references

- #652 acceptance, its lane comment, the ruling on the executor's STOP, and the round-2 assignment, all in the #652 thread.
- R478-1 and R479-1 on PR #660; their packets on branch `652-review-evidence`.
- #649 (PR #650) findings: `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`, "Guard refusals".
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2: one record per writable-name ordinal, NAME block `0x80..0xFF`, 128 ordinals.
- `hdl/milan/KL_nvm_backend.sv` elaboration contract (`g_refuse_names`).
- `docs/ENDSTATION_BUILDER.md` D8 and section 4.
- `docs/development/CODE_QUALITY.md` Rule 12 (the long-module ratchet).

## How to get into the same state

```sh
git fetch origin
git checkout 652-builder-names
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install pyyaml numpy
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt   # em-dash and contents gates
# Verilator 5.050 on PATH for gate 38's RTL arm and the nvm suites
```

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32          # gates 24a and 38 print their controls
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test        # 21 controls; short_allocation_row, long_allocation_row, stale_allocation_table
for t in yosys_sweep resmap_models resmap_tables resmap_map soc_sweep; do python3 syn/resmap/$t.py --selftest; done
python3 syn/resmap/yosys_sweep.py --work "$(mktemp -d)" shapes   # 7 built, 2 refused as expected, rc 0
python3 scripts/check_py_idiom.py                            # long module: 10 <= 10
python3 scripts/docs_check.py
make -C tb/verilator/nvm_backend && make -C tb/verilator/nvm_cosim
```

Expected result / pass criteria: every command exits 0. The bank ends
`ALL GATES PASS EXCEPT 1 NOT RUN` on a host without the Arty `mf48` build
tree (gate 11). Re-deriving the #649 page's tables needs that lane's
published inputs (its findings page, "Reproducing"); with them,
`resmap_tables.py ... --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`
reports every table equal.

## Known limitations / out of scope

- The two eight-stream TDM8 sweep points are refused by the builder and no longer priced; their Yosys receipts on the #649 page are that lane's runs and stay as recorded. The regenerated tables reuse #649's point records for the other 57 points, whose shapes this head generates byte-identically; nothing was re-priced.
- `scripts/nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)` stays as the record-space gate's own expectation (Round 2, S1). Both reviewers note a residual drift path: the RTL capacity and gate 38's pin moving together without `ALLOC`. It is not closed here.
- **Open (R479-1 S3, R478-1 S3):** the capacity is a decimal literal beside `ID_NAME_C = 'h80`; their sum filling the 8-bit `record_id` space is unchecked, as it was with the old literal. An elaboration-time guard would close it.
- No shipped or tracked shape reaches the 16-bit AEM ROM ceiling through the NAME block; gate 24a (e) still exercises that path with the capacity planted.
- The refusals table's self-test arm reads a hand-made `by_builder`; the producer is held by the `resmap_models.py` arm, not by an arm through both.
- Not run in this lane: hosted CI and the `act` replica (nothing pushed), the full Verilator sweep and Yosys portability since `d33bdc3d` (see Status).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
