[A286]

Closes #544

## Status

Ready for independent review at `b068763c849a18096b0f46cf9b18e0f904e4d708`.
All requested local gates exit 0.

## Description

Gate 1b previously accepted a macro overwriting the sampled identity
before its mismatch guard. It now checks writes in the expanded
boot unit and names the single-store rule when refusing them.

Without compilation, it rejects replacement lists naming the sample
and direct substitutions into used macro parameters.
This covers both published hostile macros while allowing unused parameters.
Both modes have documented costs, including conservative read-only refusals.

## How to reproduce

Insert `MILAN_FORGE(id)` before the identity mismatch guard, with
`#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)`.
Both modes must refuse it by the named identity-sample rule.
Removing only that mode's new check must let it pass.

## How to validate

The full builder bank passes in both modes.
With the pinned SDK: 304/304 mutations refused, 38/38 firmware cases accepted.
Without a compiler: 249/249 refused, 35/35 accepted.
Both accept 4/4 Makefile cases and elaborate 46/46 RTL variants.
All original mutation rows, reason pins and legitimate cases remain unchanged.
Required documentation, style, path, idiom and diff checks pass.
The existing resource-calibration report remains a declared NOT RUN.
Compiler-dependent instruments additionally declare NOT RUN without compilation.

## DoD

- Both published hostile macros receive named refusals in both modes.
- Removing each new check lets its hostile controls pass.
- Original mutation verdicts and accepted cases are preserved.
- Both modes have documented costs.
- R273-S3 remains accepted in both modes; its behavior is unchanged.

Local validation does not claim independent review or hosted evidence.
