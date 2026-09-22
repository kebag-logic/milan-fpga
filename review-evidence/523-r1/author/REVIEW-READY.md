[A182] REVIEW READY

Commit: b5ce20eca8b59709ec5bc6115e5e15bfc312f283
Tree: bfde1313250ae84105754af4b150325f55f5ef33
Base: 483a133ed08867ea0d300d2b4a027b5b48a4282f
Branch: 523-isolate-mutation-cancellation. Source is clean, four local commits, unpublished; remote branch still names the base.

Changed: gPTP shadow mutations now use verified private source/build copies, including required pinned dependencies. The outer sweep latches INT/TERM, stops/reaps owned descendants, preserves attributable partial logs and exits 130/143 without a completed summary or later suite. Both production-driver handshake tests are owned by normal entry points. Supporting process-policy contexts have exact-file/context positive and refusal controls; no global mask, budget, product/pin or ordinary-pool change.

Validation on this exact head:
- python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py: exit 0, including normal/repeat, named synthetic detection, survivor/build failure, dirty/index/path/pin refusal, INT/TERM/KILL, unsafe controls and nested real-driver cancellation.
- python3 scripts/test_suite_cancellation.py: exit 0, including preflight/command/transition signals, next-suite sentinel, partial logs, reaped identities, stubborn detached descendants, foreign sibling, ordinary-red continuation, masked verdict and timeout UNKNOWN.
- make -C tb/verilator/gptp_shadow with the verified scoped Verilator 5.050 selector and VERILATOR_JOBS=8: exit 0, 309/309 baseline checks, all nine real detections, zero campaign failures, six unchanged unobservable notes. Existing alternate-failed-check reporting for three controls is preserved, not reinterpreted.
- All 24 focused idiom/docs/evidence/fail-fast/bare-metal and lifecycle commands: exit 0. The actual complete log passes the normal verdict and tally tools: 309 checks, zero in-suite failures.
- Full before/after tracked bytes, kinds, modes, index and three-pin snapshots are identical. Original mutation-table ASTs, source harness, tally, 55 default suites, one physical suite and shard partition are preserved. Additional signal probes returned 130/143 in about 2.17 seconds with recorded child identities absent, no next suite and no completed summary.

Acceptance: 1-3 implemented and exercised; the author-owned part of 4 passes. Factual HANDOFF, proposed PR body, exact command/environment/exit receipts, failed probes, original public evidence, reproduction scripts and checksums are retained in the manager handoff directory. The public original-manifest discrepancy is separately recorded in https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5783883413; it is not claimed as a passing checksum check.

Remaining manager/external bar: full parent/processor/Yosys/builder banks, trusted serial act, required hosted contexts, PR/source publication, current-dev composition and candidate validation, independent R256/R257 reviews and clean lens ledger, maintainer-authorized merge and post-merge containment. This is implementation evidence, not review approval. A182 stops at this source.
