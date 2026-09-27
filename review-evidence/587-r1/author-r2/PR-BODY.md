[A365]

Closes #587.

## Status

Round 2 is published at `ce65430125a3c800138d5206dd481ba060cb2328` and is under independent re-review.

## Description

Record the integrated 8x8 baseline at the configuration's declared 50 MHz. Keep the original 100 MHz measurements as labelled history, with the complete rankings and input/report hashes.

| Measurement | Historical 100 MHz | Declared 50 MHz | Change |
|---|---:|---:|---:|
| Default whole-design LUTs | 68,136 | 68,047 | -89 |
| Default whole-design WNS | -11.331 ns | -1.708 ns | +9.623 ns |
| Attribution wrapper LUTs | 29,489 | 28,955 | -534 |
| Attribution wrapper internal WNS | -10.846 ns | -1.700 ns | +9.146 ns |

The default remains 4,647 LUTs above device capacity. The 1x1 results retain their original values.

## Round 2

- Fix R350-1 F1 / R351-F1: normalize the checkout root to the literal `$REPO` token, alongside `$BUILD`. This covers all three ROM pathname parameters. The rule now specifies comment removal and UTF-8 hashing precisely.
- Two fresh exports reproduce the committed digest `38f6c8dd93ba018d009875412b82dd9f34e2149244eda20ab1e2f81d3f85f575` with the unchanged public reviewer script.
- Address R350-1 F2 / R351-S1: label historical figures and provenance with 100 MHz and processor pin `990f9652`; identify the 50 MHz rerun's pin as `0922e434`.
- Address R351-S2: add the 50 MHz rerun to the area-budget pointer.

Round 2 makes documentation and evidence changes only. It performs no synthesis re-measurement. Original measurement values, source/image/report hashes and ranking values remain intact.

## Authoritative references

- [Issue #587](https://github.com/kebag-logic/milan-fpga/issues/587) and [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/587#issuecomment-5856241447).
- [Original baseline decision](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5844867171) and [attribution decision](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5846064333).
- [Baseline recipe](docs/testing/PP_SHADOW_BASELINE_RECIPE.md), [baseline findings](docs/findings/PP_SHADOW_BASELINE.md) and [input manifest](docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json).
- [Internal review](https://github.com/kebag-logic/milan-fpga/pull/589#issuecomment-5856181980) and [external review](https://github.com/kebag-logic/milan-fpga/pull/589#issuecomment-5856239199).

## How to reproduce

Follow the recipe's 8x8 export and synthesis endpoints at the declared clock, with separate default and preserved-boundary attribution directories. To check round 2 alone, export fresh generated tops and apply the manifest's normalization. The [unchanged public normalizer](https://github.com/kebag-logic/milan-fpga/blob/fd86bc2c2938e44bc46705999a665ed21e76e4a2/review-evidence/587-r1/reviews/R350-1/scripts/normalized_verilog.py) takes the generated top, checkout root and literal `$REPO` token. Both exports must yield the digest above.

## How to validate

All assigned baseline self-tests, mutation controls, documentation checks in both inventory modes, punctuation, style, contents, anchors, paths and whitespace checks pass with rc 0 at this head. All 28 enforcement-removal mutants are killed.

The unchanged public figure, ranking, historical-value and input checks also pass. The page checker reports 124 comparisons without mismatch; all 76 numeric rows from the prior head survive. Source/image verification matches 130 default records and 131 attribution records, with only the three expected path-bearing generated-file differences per export. The handoff contains exact commands and receipts.

## Known limitations

These are synthesis estimates. The design still exceeds LUT capacity and has negative setup slack; no placed fit or timing closure is claimed. The manager updates the #229 reference comment after merge. Independent review must assess the corrected head.

## Definition of done

- [x] Measurements, clock/pin labels, rankings and input/report hashes are recorded.
- [x] Assigned round 2 changes and local gates are complete.
- [x] Round 2 published.
- [ ] Internal and external reviewers re-cover the changed documentation.
- [ ] Exact-head hosted/local-replica and candidate-merge validation are accepted.
- [ ] Manager updates the #229 reference comment after merge and completes containment.
