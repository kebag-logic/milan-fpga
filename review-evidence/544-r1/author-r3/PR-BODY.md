[A296]

Closes #544

## Status

Ready for independent review at local commit `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.
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

The preceding implementation established these protections.

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
were explicitly NOT RUN identity protections. Those accepted forgeries
are pinned in fixtures, refused with compilation, and named in the cost
table, prose and verdict COST line. The corrected header-paste disclosure
is restored.

The repository's legitimate corpus is unchanged, including the fifth fence.
The original reviewer probe sets also contain three rvalue controls outside
the authorized forms; their compiled refusals are documented conservative
costs. The per-case evidence distinguishes them from hostile bypasses.
Both original public probe sets ran at the preceding commit in four configurations.
All 220 case verdicts are recorded, including disconnected controls.

## Round 3

The new `boot-unit asm allowlist rule` checks the entire expanded unit,
including headers and uncalled helpers. Eleven frozen normalized forms
come from the production unit and its census headers. Literal contents,
operands, qualifiers and trailing attributes remain exact.
The fifth-fence fixture repeats an existing production form; no added
entry is needed for it.

W01-W03 cover corrupting helpers reached directly, through a macro,
and through a redefined diagnostic. Each is refused by the new rule,
and each passes with only that rule disconnected. The preceding
no-escape, interval-absence and interval-asm rules remain active.
Overlapping asm controls need both checks removed before they pass.

The gate does not read separately linked pinned library, BIOS or
startup objects. Their calling-convention compliance and register/memory
effects remain trusted, unproved. The page, cost table and COST line
state this boundary.

Without a compiler, macro-free source has only the source-text write-form
identity check. Every unmatched spelling is NOT RUN; this is an open
class. C09, C11 and the plain wrapper/asm fixtures are pinned accepted
without compilation and refused with it. The seven original examples,
A01-A10 and W01-W03 illustrate the class.

Both unchanged round-2 probe sets ran at this local head.
All 483 case verdicts across 25 configurations are recorded, including
individual disconnections of the preceding checks and the new allowlist.
W01-W03 and the previously accepted callee-asm probe are now refused.
The whole-unit policy also refuses the probe's asm output after the guard.
All compiler-free probe verdicts remain unchanged.

## How to reproduce

Insert `MILAN_FORGE(id)` before the identity mismatch guard, with
`#define MILAN_FORGE(x) ((x) = MILAN_ID_MAGIC)`.
Both modes must refuse it by the named identity-sample rule.
Removing only that mode's new check must let it pass.

## How to validate

The full builder bank passes in both modes.
With compilation: 351/351 mutations refused, 38/38 firmware cases accepted.
Without a compiler: 249/249 refused, 35/35 accepted.
Both accept 4/4 Makefile cases and elaborate 46/46 RTL variants.
All original mutation fixtures and legitimate cases remain unchanged.
The compiler identity rows now name the successor absence rule.
Required documentation, style, path, idiom and diff checks pass.
The existing resource-calibration report remains a declared NOT RUN.
Compiler-dependent instruments additionally declare NOT RUN without compilation.

## DoD

- Both published hostile macros receive named refusals in both modes.
- W01-W03 pass with only the new unit allowlist disconnected.
- Overlapping asm controls pass after both relevant checks are removed.
- Original mutation verdicts and accepted cases are preserved.
- Both modes have documented costs.
- The verifier `#else` deletion case remains accepted in both modes, unchanged.

Local validation does not claim independent review or hosted evidence.
