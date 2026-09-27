[A349]

Closes #502.

## Status

Round 3 at `867a2e38a4e3231545a0a24b97d1e5612a6659fe`. All assigned local gates pass; independent re-review pending.

## Description

Persistence status becomes pending on the first accepted live name or map write. It stays pending through command completion and snapshot acknowledgement until reset; these groups still have no record writer.

Names use the accepted write export at processor pin `870ff88a`. Maps use the parent's original input-change and output-change comparisons, shared between its original priority branches and the qualified shadow pulse. An unchanged duplicate succeeds without changing the map or setting pending. All signals share the backend clock and reset.

The pin's ROM ledger, boundary diagram and pin documentation remain included. Round 2 changes no firmware, CSR layout, configuration or submodule pin.

## Reproduce

Start from a durable baseline and issue SET_NAME or ADD/REMOVE_AUDIO_MAPPINGS. Pending must assert on the first live storage change, before the later completion mark. Repeat an existing mapping from a fresh durable baseline: SUCCESS, unchanged map, pending clear.

## Validate

The following results were recorded at round-2 head `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`. Round-3 results are recorded separately below.

K10 checks eight changed name lanes, an unchanged boot name, repeated identical names and GET_NAME readback. K12 separately checks ADD, REMOVE of a preloaded mapping, and duplicate ADD from durable baselines. The dynamic fixture covers port 0 in both directions, using stream 0, channel 0 and cluster 0. Record-validation refusals use an out-of-range stream and require status 7, an empty map and pending clear. Static output refusal occurs before record validation. Zero-record commands, reset, mark groups and snapshot acknowledgement remain covered.

The observer reads live name RAM and map storage across every watched edge. Storage changes begin the unsaved interval. Control-face preloads establish baselines and make no persistence claim.

Focused results: 575 + 575 + 575 + 263 checks, zero failures. The late-mark control detects K10 and K12 regressions, including REMOVE. Unchanged reviewer scripts and the recorded anchor adapter were rerun. The duplicate probe shows pending clear; wrong-phase and ADD-only mutations fail named refused-record and REMOVE checks. Stale anchors are explicit refusals, never mutation kills.

The independent reviewer oracle reports 138 total checks in its static leg and 193 total checks in its dynamic leg, with zero failures in either. All 10 static and 14 dynamic explicit oracle assertions pass. The two totals do not describe a pass fraction.

The default sweep ran all 55 suites and all default chunks at the round-2 head: 55 passed, 0 failed, 0 timed out. Exact tally: suites: 55   passed: 55   failed: 0   timed out: 0; checks: 2125319   in-suite failures: 0.

The sweep explicitly skips the unavailable AAF/AVTP and gPTP/802.1AS field campaigns and their two freshness checks. These four declared skips contribute zero checks and provide no field or hardware evidence.

Both full builder modes return zero with elaboration required. Present mode also requires RV32 compilation. Both explicitly omit the unavailable historical placement-calibration fixture; absent mode additionally omits compiler-dependent instruments.

The same OOC recipe measures datapath LUT total 98016 at `220c9d56` and 96166 at the delivered minimal form, saving 1850. Shadow LUT total is unchanged at 66982. FF, LUTRAM, RAM and DSP counts are unchanged; datapath CARRY4 increases by one. Against the earlier `104c8a54` baseline, datapath LUT total decreases by 1126 and shadow LUT total increases by 80. No timing claim.

## Round 3

The changelog and pin history now identify the parent's actual map write as the pending trigger. Unchanged records raise nothing. The ownership table uses matching wording.

K12 now refuses a two-record ADD after the first record claims a key. Each direction starts durable and requires status 7, an unchanged map and both pending bits clear.

The default target passes 591 + 591 + 591 + 295 checks, zero failures. The late-mark mutation target passes. The unchanged internal reviewer script kills P4 in both legs through `K12 partial refusal input/output sticky_pending_PP_STAT` and `sticky_pending_PP_NVM_STAT`: two failures in the static leg, four in the dynamic leg.

Lint, test evidence and all assigned documentation gates pass, including Git and no-Git documentation checks. Both public round-2 parent-pulse mutation scripts ran unchanged against an archive of this commit. All 24 legs produced the expected results, with no build failures or refused anchors. The unchanged multi-record probe passes 327 checks on shipping RTL and detects P4.

Round 3 changes tests and documentation only. The full sweep, builder and synthesis measurements above remain round-2 evidence; they were not repeated for this revision.

## Definition of done

The round-2 implementation is retained. All four round-3 assignment items are addressed and all assigned local gates pass. Independent reviews, publication, hosted checks and merge authorization remain separate. This change makes no additional flash-restoration or hardware claim.
