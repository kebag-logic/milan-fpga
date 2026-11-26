The source checkout must contain base `3009f9a2a2d69375211d8355490675879033d940` and head `af11b3ef631eb44cdc1730cfb31bedda95c33dc5`, with the latter checked out cleanly. Use an empty packet directory containing these scripts. All disposable data goes under its `scratch/` directory.

```sh
rtk proxy python3 fetch_evidence.py PACKET --jobs 4
rtk proxy python3 review_checks.py REPO PACKET --compiler-dir PINNED_COMPILER_DIRECTORY
rtk proxy python3 fault_probes.py PACKET
rtk proxy python3 timing_probe.py PACKET --jobs 2
rtk proxy python3 audit_receipts.py REPO PACKET
```

The compiler directory must provide version 5.050; verify its identity before running. GNU make, Python 3.12 or newer, the repository's documentation dependencies, and a Linux process interface are needed. The unreadable-transcript check requires an ordinary user whose file permissions are enforced.

The scheduling tests and documentation/interface/lint gates execute concurrently within one foreground driver. Each scheduling test uses at most four pass slots. The driver waits for every child and records each command's output and status. No real-engine build or full bank runs in this driver. The fault probes use disposable copies and restore nothing in the source checkout because they never edit it. A stopped later pass may have been terminated while running or prevented from starting; either satisfies the stop contract.

The recorded full scheduling runs returned nonzero at both layouts because inherited short-stub timing assumptions failed under the observed host load. The driver deliberately propagates those failures. Run the fault and timing probes as separate commands after inspecting that result; do not hide it with an unconditional success. The timing probe repeats only the existing budget and fail-fast groups, at both layouts, and records observed assertion failures without classifying them as new regressions.

`audit_receipts.py` recomputes the published packet hashes, the real-engine transcript normalization, and the matching mutation failure counts. Those are audits of the author's published executions, not independent executions of the real-engine pairs or the consumer-wide ratchets. Their immutable source is [the public packet](https://github.com/kebag-logic/milan-fpga/tree/dcfe275da410b7caf1f914697cd2dc68fbd5349f/review-evidence/gptp113-r1/author).

Only paths listed in MANIFEST.sha256, plus REPORT.md, are publishable. `scratch/` is deliberately excluded.
