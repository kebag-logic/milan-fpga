[A360]

Closes #587.

## Status

Ready for independent review at `55079500483970ee244f12fa4c94401783f3df6f`. The #229 reference comment is updated by the manager after merge.

## Description

Re-measure integrated 8x8 synthesis and preserved-boundary attribution at the declared 50 MHz. Retain the 100 MHz figures as labelled history, alongside complete rankings and input/report hashes.

Default synthesis measures 68,047 LUTs, down 89 from 68,136, with -1.708 ns whole-design WNS. It remains 4,647 LUTs above capacity. Attribution measures 28,955 wrapper LUTs, down 534, with -1.700 ns internal WNS. The 1x1 results remain unchanged.

## How to reproduce

Follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` for the 8x8 export and synthesis endpoint. Repeat in a separate build directory with the wrapper boundary preserved. The configuration supplies the clock.

## How to validate

Both syntheses and boundary/load probes passed. All assigned baseline controls, mutation controls, documentation checks in both inventory modes, punctuation, contents, anchor, path and whitespace checks passed at the local head. Exact commands and receipts are in the handoff.

## Definition of done

Measurements, clock labels, source/image hashes, report hashes and the optimization reference update are complete. Independent review and publication remain pending. These are synthesis estimates; no placed fit or timing-closure claim is made.
