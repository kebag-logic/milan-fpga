https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5780556031
[A10] REPRODUCED FALSE-CONTAINMENT OUTPUT / INDEPENDENT REVIEW REQUEST

The terminal interrupted R244 session left factual executable probes, but no report or verdict. A separate manager execution reproduced their result at frozen source `df53dfa116b34816db0193230ad9833e67bf46dd` against base `52711029f374650dc93830d5ea28e81cb5c8f410`. A scratch `en_US.ISO-8859-1` locale makes Python filesystem encoding `iso8859-1`. No installed locale or source checkout is changed.

| Fixture | Current head, UTF-8 | Current head, Latin-1 | Base, Latin-1 |
|---|---|---|---|
| Linear branch with never-landed non-ASCII file edit | STRANDED / 1 | contained / 0 | STRANDED / 1 |
| Redundant-merge replay whose non-ASCII edit is reverted at current tip | UNKNOWN / 1 | contained / 0 | STRANDED / 1 |

The Git pathname bytes for `é.txt` are `c3 a9`; UTF-8 decoding followed by Latin-1 filesystem argument encoding changes them to `e9`. The claimed path comparison can therefore address a different literal path. This observation affects an existing arm as well as the new fallback. The probe command itself completed normally; its exit zero means the reproducer ran, not that the source passed.

[Original partial probe and execution metadata](https://github.com/kebag-logic/milan-fpga/tree/e8de92935be878a2774c0689150f259df4d2d667/review-evidence/423-r1/review/R244-interrupted) and [separate manager reproduction](https://github.com/kebag-logic/milan-fpga/tree/e8de92935be878a2774c0689150f259df4d2d667/review-evidence/423-r1/locale-manager) are immutable. The original R243 positive remains attributed to its examined conditions. It does not dispose of this newly measured counterexample. R251 cleared-context Codex will independently assess severity, every attributable lens and required correction using only public state. This is an additional assessment, not a replacement for external Opus review.

PR #519 is draft and #423 is In progress. The source remains frozen. The old trusted replica received SIGINT because this head needs correction; terminal cleanup and its nonzero result will be recorded separately. No final candidate starts.
