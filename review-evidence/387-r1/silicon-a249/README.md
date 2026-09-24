# Issue 387 bench packet, A249, 2026-09-24 (private)

Dev silicon check of the #540 gPTP pin (`e5dcea6e`) on the dev `3d2f3e31` image: identity,
gPTP lock, a 900 s steady-state soak, and three la_avdecc enumerations. HANDOFF.md is the
report. Every file is hashed in MANIFEST.sha256; verify with `sha256sum -c MANIFEST.sha256` from
this directory.

| Path | What |
|---|---|
| identity/ | console CRC readback transcript, grader log, reference CRC table (`3d2f3e31` and `c593cbef` seeds), origin, lock window |
| bench/census-start.jsonl, bench/census-start-vs-a237-final.txt | start census, and its comparison with A237's end census |
| bench/enum1/, bench/enum2/ | la_avdecc enumerations 1 and 2 (#529 step-2 shape): enumerator log, entity dumps, counters probe logs, controller-port capture |
| bench/soak/ | 900 s soak: tap capture, controller-port capture, console transcript (1 s), controller GET_AVB_INFO/GET_AS_PATH and GET_COUNTERS logs (1 s), graders, receipts, analysis |
| bench/baseline-a237/ | the wire analysis of A237's capture from this morning (previous image, previous pin) |
| bench/final/ | end census and comparison, enumeration 3, final console read, grader |
| bench/clock-*.jsonl, deploy-pw1-verify.txt, *-tmp-before-cleanup.txt, cleanup.txt | clock offsets, deployment check, remote cleanup |
| tools/ | every script and binary used, with the orchestration scripts `run_*.sh` |
