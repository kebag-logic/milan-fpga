[A289]

Closes #544

## Status

Ready for independent review at local commit `77e9ca5ea9e04a7618c577ab511baec63b39dc05`.
All requested local gate commands exit 0.

## Description

Gate 1b previously accepted a macro overwriting the sampled identity
before its mismatch guard. It now enforces an absence rule in the expanded
boot unit, permitting only the two authorized complete rvalue shapes.
The automatic sample cannot escape anywhere in the unit.

Without compilation, it rejects replacement lists naming the sample
and direct substitutions into used macro parameters.
This covers both published hostile macros while allowing unused parameters.
Both modes have documented costs, including conservative read-only refusals.

## Round 2

The sample has automatic block storage with no explicit storage specifier.
A diagnostic copy gives it register storage to expose address-taking in any
spelling. Nested functions are refused to exclude implicit capture.
The original unit remains the census input.

Between the sampling read and guard, all assembly statements are refused.
The only sample uses permitted there are a complete `(unsigned long) id`
call argument and the complete statement `(void)(id & <integer-literal>);`,
as authorized by the [recorded decision](https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5824093785).
Assignments, wrappers and incomplete delimiter matches receive named refusals.

Without compilation, C03, C05, C13, the writer alias/apply forms and C16/C17
are explicitly NOT RUN identity protections. All seven accepted forgeries
are pinned in fixtures, refused with compilation, and named in the cost
table, prose and verdict COST line. The corrected header-paste disclosure
is restored.

The repository's legitimate corpus is unchanged, including the fifth fence.
The original reviewer probe sets also contain three rvalue controls outside
the authorized forms; their compiled refusals are documented conservative
costs. The per-case evidence distinguishes them from hostile bypasses.
Both unchanged public probe sets ran at this commit in four configurations.
All 220 case verdicts are recorded, including disconnected controls.

## How to reproduce

Insert `MILAN_FORGE(id)` before the identity mismatch guard, with
`#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)`.
Both modes must refuse it by the named identity-sample rule.
Removing only that mode's new check must let it pass.

## How to validate

The full builder bank passes in both modes.
With the pinned SDK: 348/348 mutations refused, 38/38 firmware cases accepted.
Without a compiler: 249/249 refused, 35/35 accepted.
Both accept 4/4 Makefile cases and elaborate 46/46 RTL variants.
All original mutation fixtures and legitimate cases remain unchanged.
The compiler identity rows now name the successor absence rule.
Required documentation, style, path, idiom and diff checks pass.
The existing resource-calibration report remains a declared NOT RUN.
Compiler-dependent instruments additionally declare NOT RUN without compilation.

## DoD

- Both published hostile macros receive named refusals in both modes.
- Removing each new check lets its hostile controls pass.
- Original mutation verdicts and accepted cases are preserved.
- Both modes have documented costs.
- The verifier `#else` deletion case remains accepted in both modes, unchanged.

Local validation does not claim independent review or hosted evidence.
