[A533]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN: every local gate this change touches is rc 0 at the head. The builder bank ends `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: no Arty `mf48` build tree on this host); 33 docs, ratchet and resmap gates; 9 builder-consumer gates, including the record-space gate and its 19 negative controls; the `nvm_backend` (751 checks), `nvm_cosim` (465) and `fw_service_budget` (52) suites. The full Verilator sweep (59/59 suites, 2,148,513 checks) and Yosys portability (55/55 tops) ran at `d33bdc3d`; no RTL, testbench, builder or configuration file changed after it. `652-builder-names` -> `dev`, head `2f0f59291080aeab934e0d72e124fb448c105e12`.

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
| `syn/resmap/` | `yosys_sweep.py shapes` records every builder outcome; a refusal is a refused point with its refusal line, and any outcome the plan does not expect (a crash, an unexpected refusal, an expected refusal that builds) fails the step. The two 235-name variants are `"expect": "refused"`; `run` does not price them, `summary` records them, the models count them as refused, and the refusals table says who refused each point. Self-test arms for each. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md` | The refusals and datapath-marginals tables regenerated through `resmap_tables.py --write` (the two points are refused by the builder and no longer priced); the 24 other tables and every fit are unchanged; prose restated. |
| `scripts/check_nvm_record_space.py`, `scripts/nvm_contract.py` | Check 14: every figure in the saved-state design's section 4.2 allocation table is checked against the inventory the gate derives for the two shapes its columns name; a planted stale count is a negative control. |
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
3. Tracked configurations build unchanged: met; every artifact of all five
   tracked configurations regenerates byte-identically against the base
   (120 files, re-run at the head; `git status` stays clean after regeneration).
4. Ruling item 2: the `shapes` step records a builder refusal fail-closed with
   its line; the two variants are refused-by-builder points; the page's two
   refused-point tables were regenerated through the generator and every
   table equals a fresh generation.
5. Ruling item 3: section 4.2's counts are the current ones, checked by the
   record-space gate against its derivation.

## Authoritative references

- #652 acceptance, its lane comment, and the ruling on the executor's STOP in the #652 thread.
- #649 (PR #650) findings: `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`, "Guard refusals".
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2: one record per writable-name ordinal, NAME block `0x80..0xFF`, 128 ordinals.
- `hdl/milan/KL_nvm_backend.sv` elaboration contract (`g_refuse_names`).
- `docs/ENDSTATION_BUILDER.md` D8 and section 4.

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
python3 scripts/check_nvm_record_space.py --self-test        # includes stale_allocation_table
for t in yosys_sweep resmap_models resmap_tables resmap_map soc_sweep; do python3 syn/resmap/$t.py --selftest; done
python3 syn/resmap/yosys_sweep.py --work "$(mktemp -d)" shapes   # 7 built, 2 refused as expected, rc 0
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
- `scripts/nvm_contract.py` `ALLOC["NAME"] = (0x80, 128)` restates the NAME block for the record-space gate's own check 3; it predates #652 and is not changed here.
- The capacity is a decimal literal beside `ID_NAME_C = 'h80`; their sum filling the 8-bit id space is unchecked, as it was with the old literal.
- No shipped or tracked shape reaches the 16-bit AEM ROM ceiling through the NAME block; gate 24a (e) still exercises that path with the capacity planted.

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
