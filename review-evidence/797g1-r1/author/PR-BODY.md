[A712]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN -- 47 of 47 documentation gates rc 0 at head `cb07597bc33106933c708a45f92c91f17a7a3e61`; builder-bank leg 8 of 8 gates pass (gate 32 included); 10 of 10 planted mutants refused -- `797-g1-define-end-station` -> `dev`.

## Linked Issue / roles

Relates to #797

Executor: `[A712]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Lane G1 of the documentation sweep (#797, issuecomment-6523632193): how the end-station YAML defines the FPGA solution, from the builder to the entity on the wire. Documentation and generators only; no RTL, builder, firmware or test behaviour changes.

| Piece | What it is |
|---|---|
| `docs/guides/DEFINING_THE_END_STATION.md` (new) | The guide: the model, what the builder generates and who reads it, when `entity_model_id` moves, resources, a worked example, and the workflow. It copies no value: numbers and names live in generated blocks or behind links. Joins `check_doc_style.py` `DOCUMENTS`; linked from `docs/README.md` and `docs/guides/README.md`. |
| `docs/diagrams/endstation_definition.gen.py` (new) | Generates the guide's nine blocks: the data flow (Mermaid), the artifact table, the 1x1 AEM descriptor tree (Mermaid, from the builder's overlay, counted against its census and the descriptor layer's CONFIGURATION counts), the model-ID resolution (Mermaid), the resource table, the worked-example runs and what they move, and the shape-to-suite table. Every consumer label is checked against the file that reads it, and every prose claim about a generated value is checked against the builder. |
| `sw/builder/gen_key_reference.py` + `sw/builder/key_reference.yaml` (new) | Generates the "Key reference" of `sw/builder/README-parameters.md`, the owner-named home. The key set is `test_builder.py` gate 32's loader recorder (114 keys). Need, default, limits and the refusing check are probed live against the builder. Clauses and contract rows come from `docs/ENDSTATION_BUILDER.md` section 3. An unknown-key table states, per mapping, whether an undeclared key is refused or dropped. The YAML holds only a one-line meaning and the probe values, and may not spell a number in its prose. |
| `sw/builder/README-parameters.md` | Gains the generated section; four hand value tables it duplicated become links (single source; the optional-blocks table had omitted `datapath_probes`). |
| CI | The existing "Entity shape gate" step runs both generators' `--check` and `--selftest` (template, canonical inventory, regenerated workflow). No new step, so no renumbering against PR #815 or R1. The command table gains the four argv patterns and digest pins for the two scripts. |
| Catalog and generation guide | Three diagram rows and the regeneration commands. |

Published conflicts and findings (detailed in the TAKEN comment and below):

- The assignment's "OVER refusal" does not exist at this head: OVER is a build-plan verdict and the builder exits 0. The guide shows that verdict, and the real refusal at 8x8 (235 writable names against 128 NAME records).
- Builder findings for new Issues, not fixed here: unknown keys dropped silently in 14 mappings; the CLI lists the sweep fragment as written when it is not; `entity.vendor_name` has no length check; 63- and 64-octet limits for the same AEM string field; an odd wire width passes `framer_wire_channels`; `int()` conversions raise an unhandled `ValueError`; `bool()` reads any value as a boolean.
- `docs/ENDSTATION_BUILDER.md` (design lane): stale key and row counts in its contents line, and stale cited line numbers in section 3.
- `ci/image/command-table.json` is stale at dev `1e80128f` (27 digest pins, one undeclared script, one unmodelled environment name), so `scripts/ci_tool_inventory.py --check` is red at base and here with the same first refusal. With that drift neutralised in a scratch copy, each new script is refused without its pin and passes with it.

## Authoritative references

- #797 issuecomment-6523632193 (G1), issuecomment-6522974767 (short paragraphs, gated), issuecomment-6523093123 (diagrams)
- IEEE 1722.1-2021 6.2.2.8 (a changed model needs a new `entity_model_id`; `object_name` is not model structure), 7.2 (descriptor hierarchy and 64-octet strings), 7.2.2 (CONFIGURATION descriptor counts), 7.2.8 (AVB_INTERFACE)
- IEEE 802.1AS-2011 8.4.3 (ingress and egress latency)
- Milan v1.2 clauses as cited per key by `docs/ENDSTATION_BUILDER.md` section 3
- `sw/builder/endstation_builder.py`, `sw/builder/test_builder.py` gate 32, `docs/ENDSTATION_BUILDER.md` section 3, `docs/design/AREA_BUDGET.md` (headroom target), `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/integration/BUILDING.md` (linked, not edited), `docs/diagrams/README.md`

## How to get into the same state

```sh
git fetch origin
git checkout 797-g1-define-end-station
git submodule update --init gptp-processor protocol-processor third_party/verilog-axis
python3 -m pip install pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 sw/builder/gen_key_reference.py --check
python3 sw/builder/gen_key_reference.py --selftest
python3 docs/diagrams/endstation_definition.gen.py --check
python3 docs/diagrams/endstation_definition.gen.py --selftest
python3 scripts/check_entity_shape.py --self-test
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_archive.py
python3 scripts/check_diagram_pngs.py
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_py_idiom.py
python3 sw/builder/test_builder.py --require-rv32 --gates test_all_configs_build,test_bad_configs_rejected,test_model_id_hashing,test_resource_verdicts,test_schema_12_keys_reach_the_image,test_schema_12_refusals,test_builder_doc_key_map,test_name_count_fits_the_nvm_name_block
git status --short
```

Expected result / pass criteria: every command exits 0; both generators print "fresh" and their self-tests report the stale page and every planted defect refused; `git status --short` prints nothing. To see a mutant bite, change a generated cell in either page and rerun its `--check` (rc 1), or change a builder default and rerun the key reference's `--check` (rc 2).

To run the worked example as the guide prints it, follow its "Worked example" section; it works on a copy outside the tree and ends with an empty `git status --short`.

## Known limitations / out of scope

- No builder, RTL or test change: the builder findings above need their own Issues.
- No FPGA implementation run, sweep or hardware: the resource section links the measured route rather than restating it.
- The three Mermaid diagrams were not rendered locally; review them in the preview.
- The key reference inherits gate 32's bound: a key read only on a loader branch no tracked configuration takes is not recorded. The page says so.
- The full builder bank does not fit one local foreground run; the leg covering gate 32, the configs, the schema keys, the model ID, the verdicts and the name capacity was run. CI runs the full bank in measured legs.
- `docs/DOCUMENTATION_AUDIT.md` (D0, PR #815) does not list the new guide yet; whichever lands second regenerates it.
- `docs/integration/BUILDING.md` is not edited; release lanes own it.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (G1 items 1 to 5, diagrams, style gate)
- [x] New or changed behavior has self-checking tests (both generators' `--selftest`; 10 planted mutants)
- [x] Required local verification bar passes (47 documentation gates rc 0 at the head)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
