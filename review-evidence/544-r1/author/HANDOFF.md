[A286]

Closes #544

Status: implementation complete and ready for independent review.
Branch: `544-macro-sample`
Base: `ffcbd33de70278ae34b533dcbadde0b36c8cba13`
Head: `b068763c849a18096b0f46cf9b18e0f904e4d708`
The worktree is clean. The commit subject is one line.

Gate 1b protects the expanded identity sample before its mismatch guard.
It refuses assignment, compound assignment, increment, decrement,
address-taking and memory/string destinations through named rules.
The compiler-free rule rejects replacement lists naming the sample.
It also rejects direct calls substituting it into used parameters.
Unused parameters remain accepted.
Both modes have cost-table rows describing conservative refusals.

The original table definitions, additions, accepted-case updates and rejection
grader remain unchanged and ordered: all 15 statements are preserved.
Every original mutation verdict and legitimate case still passes.
The existing floors were 280/280 and 222/222.

| Mode | Mutations refused | Firmware cases accepted | Makefile cases accepted | RTL variants elaborated | Exit |
|---|---|---|---|---|---|
| Pinned SDK | 304/304 | 38/38 | 4/4 | 46/46 | 0 |
| Compiler absent | 249/249 | 35/35 | 4/4 | 46/46 | 0 |

Both published hostile macro forms receive named refusals in both modes.
Removing only the corresponding new check lets them pass.
The literal-reference hostile macro has the same control result.
The compiler-free audit records zero firmware compiler invocations.
All required static gates exit 0 at this head.
The em-dash gate uses the assigned base.
Both documentation inventory modes pass without exporting a tree.
Exact commands and receipts are in [VALIDATION.md](VALIDATION.md).
Machine-readable results are in `builder-results.json` and `static-results.json`.
The final SDK run's input hashes still match the committed files.

R273-S3 remains accepted in both modes, unchanged from the base.
The missing verifier arm was not fixed.
The existing resource-calibration report is unavailable and declares NOT RUN.
Compiler absence also declares the compiler-dependent instruments NOT RUN.
Those skips are not claimed as coverage.

The published hostile macros name `x` in their bodies and `id` at calls.
A literal-only fallback was measured insufficient.
The used-parameter interpretation implements the explicit hostile-case requirement.
It is recorded in [the issue update](https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5822819158).
The fallback checks local definitions and direct calls, without general expansion.
Read-only uses through used parameters incur the documented conservative cost.

Public handoff: `[A286] REVIEW READY` on issue #544 for this head.
The internal reviewer is [R316]; the external reviewer is [R317].
Independent review and subsequent publication remain with the assigned roles.
No push, PR creation, PR edit, merge, hardware or delegated work occurred.
Both temporary public-evidence scratch locations were removed.
