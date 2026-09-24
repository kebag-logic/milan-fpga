[A287] REVIEW READY

Local head: `4f6185ce97e31f3bdacc090ec1ab7ede32456d2e` on `113-latency-notify`.

Round 2 implements assignment items 1–4 for R310-1 F1 and R311-1 F1: response-level walking-one and walking-zero sequences isolate all 32 bits, with exactly one notification per change and silence on every unchanged repeat. Six comparator-truncation mutants are retained in the existing runner and fail named checks. Coverage wording is corrected; no RTL changed.

Validation:
- Every processor workflow gate returns rc 0, including the full bank, lint, portability, documentation and historical figure gates.
- Full bank: 33 suites, 1,009,045 original + 5,568 added = 1,014,613 checks, zero failures. Other suite counts are unchanged. Processor top: 7,642; focused GI: 6,182.
- All 20 retained mutants are caught by named checks; golden and restored controls pass. Both reviewers' unchanged original scripts catch all eight truncation probes at this head; both golden controls pass.
- Parent base `573f0052a0e4412e81f0845438fcec2086ce5d55`, local candidate `399cb14f75ad1c73995bca4a0adebfab607dd640`: all seven commands return rc 0; consumer 371 checks, zero failures. The four existing front-end findings and the unrun historical calibration arm remain documented.

`HANDOFF.md`, the full updated `PR-BODY.md`, and complete receipts are in the assigned `pp113-a287` output directory. Both checkouts are clean. Temporary review archives and exports were deleted. No push, PR edit, merge or hardware action occurred. Ready for delta reviews at the local head.
