[A325]

Closes #567

## Status

Local author handoff at `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`. Independent review and publication remain pending.

## Description

Adopt processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d` from `990f96526bb89356c963a260ebbdcf2a77e6623a`. This brings processor PR 118's October MVU waiver and response tests, plus PR 119's complete parameter inventory and checker. Refresh current pin references, the generated submodule diagram and manifest, and the changelog. Remove the resolved MVU enable-parameter documentation conflict.

Processor HDL has the identical Git tree object at both pins. Parent RTL is unchanged. All 24 processor parameters agree across the declarations, guide and diagram; the parent's 14 explicit bindings are documented pass-throughs.

## How to reproduce

Initialize the three active submodules at their recorded gitlinks. Run the processor inventory checker from the parent root:

```sh
python3 protocol-processor/scripts/check-integrator-params.py
```

Regenerate the diagram with `python3 docs/diagrams/submodule_boundaries.gen.py`.

## How to validate

Run the assigned processor-shadow, builder (pinned SDK and absent RV32 compiler), NVM, documentation, CI-policy, traceability, source-list, lint, language, naming, port-contract and behavior gates. Inspect the generated diagram and direct print export. All assigned commands returned 0. SDK builder mode reports one NOT RUN arm for the absent calibration report; absent-compiler mode also skips its compiler-dependent instruments. Detailed author evidence accompanies the handoff; this body is not a review verdict.

## DoD

- [x] Target processor gitlink and current pin references updated.
- [x] Diagram and its manifest regenerated and visually inspected.
- [x] Processor parameter inventory and parent bindings agree.
- [x] No parent RTL change.
- [x] Assigned local commands returned 0, including both full builder modes.
- [ ] ROM-ledger acceptance conflict resolved publicly.
- [ ] Independent review completed.

Acceptance 2 leaves the ROM ledger unchanged because its processor sources did not change. However, the OOC checker requires rows for every exact pin, and the existing ledger has no `0922e434` rows. The [public conflict](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5844889430) needs an acceptance decision before OOC synthesis can accept this pin. No OOC pass or merge readiness is claimed.
