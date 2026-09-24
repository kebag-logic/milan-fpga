[A245] REVIEW READY

Head: `4f525eb55b310d6b9bc2f1a000254cb2dd483665` on `94-desc-mem-guard` (local only).

Guard integrated; `debt_o` published as the D3 interface. The original wrong-byte reproduction and hold-deleted mutant both fail the completed isolation assertion; the guarded case passes. All CI gates and the full simulation bank are green: 32 suites, 15,894 checks. OOC area: 4 LUTs, 1 FF against T9's 5 LUTs, 1 FF.

Handoff and PR text: `$MANAGEMENT/2026-09-23/pp94-a245/HANDOFF.md` and `PR-BODY.md`. D3 rollback remains deferred under the assignment.
