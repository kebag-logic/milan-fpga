[R533] POSITIVE - exact head f74b9403b330ce316eeec6f724846f16def98443

Round R533-7, external independent delta review of issue #665 / PR #690. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains open in this review. One wording-only RESIDUE remains in the live PR body; it does not change the verdict or lens coverage.

The reviewed tree is `13e6c9d6e2dceb981c5c2976d85e07fbe287a996`. The round delta is the single commit after `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`. I reconstructed the repository contract, documentation map, frozen issue scope and decisions, requirements and interfaces, then the FC-base range `db9aa8c9b135b34ff3d070a979dee70440b37cc6..HEAD` and history. Imported dev changes were distinguished from this lane and its six-file round delta. Public author summaries were checked against code and new executable receipts. Prior public reviewer findings were read only after the independent pass and written verdict/ledger in `receipts/independent-verdict-ledger.md`. No private lane material or other checkout was used.

The controlling [round-7 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6040189958) permits a bounded discard of an unrecoverable receive record, counted separately, while preserving recoverable cases. The [F4 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), `REQUIREMENTS.md:23`, `docs/reference/FR_NFR.md:330`, and `docs/design/MAILBOX_SPLIT.md:110` remain the authorities. The public author archive at `80a75f9ac3a5bedc553c84440a90134d4c28ffb5` contains the round-7 HANDOFF and PR-BODY summaries; the additional round-7 raw/helper files those summaries name are not present there. I do not treat the summarized 99 invocations as independently executed evidence. This packet supplies the focused executions and twelve size reproductions used for this verdict.

[R533] PASS Conformance - `sw/firmware/ctrl/srp/srp_mbx.c:388`, `:415`, `:655`; `third_party/lwSRP/src/include/shish_lan/mrp.h:270`; `receipts/r532_hol_probe-if1.log`, `r532_hol_probe-if2.log`, `r532_flood_probe-if1.log`, `r532_flood_probe-if2.log` - The 1000 ms local recovery limit uses the original mailbox arrival, including initial queue delay. Only continuing allocation refusal expires. Successful retry takes precedence. Discard clears the record and increments `rx_discarded` once, without incrementing received or malformed. Later input and binding progress are demonstrated. The required HOL cases N=30/150 receive the later withdrawal by the first five-second sample, with no pending record and no active licence. N=30 fits without refusal at IF=2, a valid control. Both flood probes revoke in the successful push's service pass (`revoked_after_ms=0`, received +1, malformed=0). MSRP rapid Leave, original #608 LV deadline, MVRP scope, admission and selected wire differential remain passing.

[R533] PASS RTL - `sw/firmware/ctrl/srp/srp_mbx.h:65`, `srp_mbx.c:287`, `:599`, `:634`; `sw/firmware/ctrl/loop/ctrl_loop.c:119`; `sw/firmware/ctrl/app/ctrl_app_srp.c:8`; `receipts/mailbox.log` - Reviewed architecture, ownership, scheduling and backpressure despite no round-7 RTL change. One owned static receive record preserves bytes/interface/arrival; unsigned elapsed subtraction handles clock wrap. Reset and destroy cancel it appropriately, retries follow pending events/ticks/owed TX, and failed participant recreation also checks expiration. The ACMP-facing port can proceed after discard. The ADP/MAAP/SRP composition preserves its enables and single timer ownership. Hardware, configuration, register-map and placement paths have no lane delta against assigned dev `e21c1ca0`; the older FC-to-head HDL change is imported history. Both mailbox buses, two-interface variants, host model, cosimulation and five mailbox plants pass from a fresh tracked export.

[R533] PASS Robustness - `sw/firmware/ctrl/test/srp_rx_retry.cpp:42`, `:277`, `:307`, `:324`, `:337`, `:352`, `:374`; `receipts/r533_5_independent-if1.log`, `r533_5_independent-if2.log`, `r532_retry_probes-if1.log`, `r532_retry_probes-if2.log` - All seventeen recovery tests pass at each interface count, preserving the original eleven cases. They cover mixed and partially applied payloads, repeated refusal, cross-interface ordering, MVRP selection, reset fences, destruction, failed recreation, queued/retained clock wrap, and recovery exactly at expiration. A real-pool over-capacity record remains retained at 999 ms and is discarded once at 1000 ms; withdrawal and binding then progress. The unchanged independent four-case recovery probe and six-case retry probe pass at IF=1/2, without peer retransmission. Existing malformed input, shared-binding and lifecycle cases remain passing.

[R533] PASS Tests - `sw/firmware/ctrl/test/srp_mutants.py:575`, `srp_rx_retry.cpp:277`, `srp_latency.cpp:142`, `sw/firmware/gtest/coverage.ratchet:19`; `receipts/campaign/`, `new-if1/`, `coverage.log` - All 102 named SRP plants are detected at IF=2; all twelve new plants are also detected at IF=1. The bound-removal plant compiles and fails the retained-record, discard, received, licence and binding observables; a build failure is not accepted as a catch. Separate plants detect early/late expiry, incorrect counters, renewed arrival, missing initial/recreation expiry, expiry before successful recovery, and non-modular time. Coverage reproduces 469/469 SRP lines and 438/438 branches, with all nineteen measured files at 100% after unchanged exclusions. The ordinary adapter, composition, timing, debug and processor-derived wire suites pass at both counts.

[R533] PASS Docs - `sw/firmware/ctrl/srp/README.md:32`, `:76`, `:158`, `:203`, `:247`; `sw/firmware/ctrl/srp/srp_mbx.h:97`; `receipts/pr-body.md`, `sizes.json`, `size-attribution.json` - The README states every valid Class A Domain value is retained, uses pending-event wording, and explains original-arrival expiry, success precedence, distinct accounting and MRP refresh/aging. It preserves the 10 ms service-budget limitation and integration obligations. Twelve independently rebuilt links match the published head and historical figures. The public mailbox export recipe now reaches the complete gate with documented prerequisites. Documentation, dependency-inventory, idiom, generator and whitespace checks pass. The wording residue below is non-blocking under the owner's rule.

**R533-7-R1 | RESIDUE | Docs | Published checkout introduction still waits for publication**

Artifact: PR #690 body, “How to get into the same state,” line 106 in `receipts/pr-body.md`.
Authority/evidence: The body says “After the manager publishes the candidate, use this checkout recipe.” The live head, review-start comment and fetched branch already identify the published reviewed commit. The main Status section is corrected. This remaining introductory tense changes no command, measurement, verdict, test, generated artifact, conformance/clause claim or privacy rule.
Impact: stale publication wording only.
Required exact fix: replace “After the manager publishes the candidate, use this checkout recipe.” with “Use this checkout recipe.”
Verification: read the updated live PR body and retain the existing checkout commands. Carry this small remainder of R532-6-R1 / R533-6-R1 to the residue checklist.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue 665 assignment 6040189958; srp_mbx.c:388,415,655; README.md:90; HOL/flood and original recovery receipts | R533-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| RTL | CLEAN | f74b9403b330ce316eeec6f724846f16def98443^..f74b9403b330ce316eeec6f724846f16def98443 six-file diff; e21c1ca0..f74b9403b330ce316eeec6f724846f16def98443 hardware/config/placement paths unchanged; srp_mbx.h:65; ctrl_loop.c:119; mailbox receipt | R533-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Robustness | CLEAN | srp_rx_retry.cpp:42,277; expiry, wrap, link fencing, recreation, partial completion and cross-interface probes | R533-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Tests | CLEAN | srp_mutants.py:575; 102 IF=2 and 12 new IF=1 plants; coverage receipt; original and new probe receipts | R533-7 | f74b9403b330ce316eeec6f724846f16def98443 |
| Docs | CLEAN | srp/README.md:32,76,158; public PR body; author-r7/HANDOFF.md; independently rebuilt twelve sizes and attribution receipts | R533-7 | f74b9403b330ce316eeec6f724846f16def98443 |

**Executable receipts and reproduction**

All paths below are relative to this packet. `scripts/run_parallel.py <source>` runs four independent foreground-supervised groups, each with `--jobs 2`: suites, public probes, the full SRP campaign and the new IF=1 plants. The supervisor waits for its children. Coverage, size and mailbox runs were also foreground commands, with concurrent compilation limited to sixteen jobs. Every disposable source export, mutation, SDK extraction and build is under `scratch/`; it is not publishable.

| Execution | Result | Receipt |
| --- | --- | --- |
| Adapter / recovery / composition / timing / wire / debug | 53 / 17 / 2 / 5 / 5 / 3 cases pass at each interface count | `receipts/suites.json`, `srp_*-if*.log` |
| Required public probes | HOL N=30/150, flood, four recovery and six retry cases pass at IF=1/2 | `receipts/probes.json`, `r532_*-if*.log`, `r533_5_independent-if*.log` |
| Mutation controls | 102/102 at IF=2; 12/12 new controls at IF=1 | `receipts/campaign.json`, `new-if1.json`, corresponding log directories |
| Coverage | PASS, 19 files; no exclusion change | `receipts/coverage.log`, `coverage.rc` |
| Mailbox gate | 316/361 bus checks; IF=2 316/361 and model 316; cosimulation 13; five plants detected | `receipts/mailbox.log`, `mailbox.rc` |
| Size fixture | Twelve links reproduce published numbers | `receipts/sizes.json`, `*-symbols.txt`, `size-attribution.json` |
| Focused source/docs checks | Seven commands exit 0 | `receipts/static.json`, `static-*.log` |
| Integrity | Parent and four required dependencies match committed blobs, modes and complete indexes | `receipts/integrity.json`, `integrity.rc` |

The initial probe supervisor had a receipt-parser error: it assumed received=2 even when IF=2 N=30 completed normally. The C++ probes passed. The corrected predicate requires exactly one additional received withdrawal relative to each case's initial count, plus pending=0 and active=0 by the first five-second sample; the complete probe group then passed. An initial historical-size export also lacked a generator import; the corrected launcher uses the fixed current shape generator and historical fixture/source population, and all twelve links were rerun. These setup failures remain in `receipts/development.txt` and the initial logs; they are not product failures or passing invocations. `receipts/execution.json` preserves the initial supervisor result; `receipts/probes.rc` records the successful rerun.

To reproduce the remaining groups, run the repository coverage command with `--check --jobs 4 --keep <packet>/scratch/coverage`; install the pinned SDK into `<packet>/scratch/sdk` with `scripts/ci_rv32_sdk.py`; then run this packet's `scripts/fetch_runtime.py`, `scripts/sizes.py <source>` and `scripts/summarize_sizes.py`. Run `scripts/mailbox.py <source> --hdl <pinned-5.050-binary>` for the tracked export and complete `make -j16 VBUILD_JOBS=2` mailbox gate. Set `TMPDIR=<packet>/scratch` and `PYTHONDONTWRITEBYTECODE=1`. `scripts/static.py <source>` and `scripts/integrity.py <source>` provide the other checks.

**Linked memory evidence**

Bytes below use the same pinned RV32I/ILP32 compiler, verified runtime inputs and section recipe. Fifty-seven public runtime source/dependency digests were verified. The R5/current dependency production-source diff is empty. Historical control sources and the R5 fixture were exported from their own commits; base excludes absent MAAP/SRP. Initialized data is zero. BSS already includes the arena; do not add it twice. Every span includes alignment and an 8192-byte reserved stack, not a whole-call-chain proof.

| Shape / IF | Text | Read-only | BSS | Arena within BSS | Head span | FC-base span | R5 span | Delta FC base | Delta R5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 33560 | 2846 | 18072 | 9920 | 62688 | 18752 | 54592 | +43936 | +8096 |
| 1x1 / 2 | 34792 | 2846 | 29424 | 19840 | 75264 | 19248 | 65840 | +56016 | +9424 |
| 8x8 / 1 | 33500 | 2846 | 32824 | 24032 | 77376 | 18752 | 69280 | +58624 | +8096 |
| 8x8 / 2 | 34744 | 2846 | 58928 | 48064 | 104720 | 19248 | 95296 | +85472 | +9424 |

Symbol/map attribution confirms the R5-to-head BSS growth: `image_app` +1104/+2172 bytes for the MAAP composition, `image_allocation` +8/+16, and `image_srp` +1528 for the shared retained record, independent of shape/interface count. Arenas are unchanged. For 1x1, non-SRP text growth from MAAP and its composition is 5036/5368 bytes; the adapter contributes a further 416/340. Required ADP, MAAP, SRP, binding, receive/transmit and storage symbols survive linking. These are linked-size fixtures without a board reset entry or connected fabric licence port, not booted images or routed resource measurements.

**Prior public findings reconciled at this head**

| Prior finding | Disposition and evidence at this head |
| --- | --- |
| R532-6-F1, unbounded retained input | RESOLVED across Conformance, RTL, Robustness, Tests and Docs. Original-arrival bound, distinct once-only discard, required HOL/flood probes, binding progress, preserved recoveries and detected bound-removal plants. |
| R532-6-F2, missing linked-size deltas | RESOLVED across Conformance and Docs. Live body and public handoff give both deltas and attribution; the twelve new links and maps reproduce them. |
| R533-6-F1, broken mailbox recipe | RESOLVED across Tests and Docs. Nonexistent archive input/helper removed; fresh tracked export and the complete gate pass with bounded job settings. |
| R532-6-S1 | ADDRESSED. README uses “pending events” and names every valid Class A Domain value. |
| R533-5-F1 / R532-5-F1, lost recoverable Leave | RESOLVED, retained. Unchanged four-case recovery probe, six retry probes and all seventeen lane recovery cases pass at both counts; retry-removal controls are detected. |
| R533-1-F1 / R532-1-F1, Milan immediate Leave | RESOLVED, retained. Immediate Listener/Talker, MVRP scope and original #608 deadline cases/plants pass. |
| R533-1-F2 / R532-2-F1, link lifecycle | RESOLVED, retained. Attach/poll level, adjacent edges, stale prefix, cancelled DOWN and reattach cases/plants pass. |
| R533-1-F3 / R533-2-F1, shared StreamID/rebind | RESOLVED, retained. Aggregate declaration, both binding orders, inherited state and consecutive replacements pass; plants detected. |
| R533-1-F4, linked composition | RESOLVED, retained. Reachable composition, sections, storage and FC-base comparisons independently reproduced. |
| R532-1-F2 parts 1/2, admission / ReadyFailed | RESOLVED, retained. Exact ceiling and strict callback cases pass; discriminating plants detected. |
| R532-1-F2 part 3 / R533-2-F2, notes 4/5 | RESOLVED, retained. Pinned `tests/unit/integration_test.c:327,352` and `tests/check_reversals.py:74,185` contain the two tests and three controls. Pin and dependency tests are unchanged from round 6; this round does not claim a new upstream-suite execution. |
| R532-2-F2, dependency inventory | RESOLVED in source, retained. Correct exact pin, license/ownership/fetch inventory, submodule and docs checks pass. Hosted acceptance is separate. |
| R532-2-F3, last never-eligible VID | RESOLVED, retained. Both unbind orders and `last-ineligible-vid-leaks` pass/detect as appropriate. |
| R532-2-F4, lifecycle/shared-VLAN test gaps | RESOLVED, retained. `reset-keeps-owed-domain`, `reset-keeps-sink-vlan`, `shared-ready-uses-first-vlan` are detected. |
| R532-3-F1, inheritance test gaps | RESOLVED, retained. Cross-slot and cross-StreamID cases pass; inheritance plants detected. |
| R532-3-F2, final-unbind Domain VID | RESOLVED, retained. Both Domain-VID cases pass; guard plant detected; README states exception. |
| R532-1-S1, LeaveAll scope | ADDRESSED, retained. Pinned per-type/per-port upstream test remains; selected Run-B wire case passes. |
| R532-1-S2, generic LV extra Join | RESOLVED, retained. Ordinary LV rows suppress indication; changed-value case remains covered by the unchanged independent probe. |
| R532-1-S3, recreation guard | ADDRESSED, retained. Failed creation releases participants and retries; new deadline case passes. |
| R532-2-S1, Milan leaking into MVRP | ADDRESSED, retained. Dedicated scope case and plant pass/detect at this head. |
| R532-1-R1 / R532-1-R2 | RESOLVED, retained. TICK units corrected; object-only limitation superseded by actual linked evidence. |
| R532-2-R1 / R532-3-R1 | RESOLVED, retained. Public exact-pin fetch works; STOP/compiler-absent wording is superseded by current scope and manager duties. |
| R532-2-R2 / R532-5-R1 / R532-6-R1 / R533-6-R1 | Main publication status corrected. The conditional checkout introduction is retained only as R533-7-R1 RESIDUE above. |
| R532-5-R2 | RESOLVED, retained. README records merged public PR #15 at 9197193e. |
| R532-5-S1 / R532-5-S2 | ADDRESSED, retained. Timer-destruction wording agrees with source; future-version/whole-invalid-PDU adapter cases and plants pass/detect. |

**Limits and pending manager duties**

The bound is checked at an eligible receive attempt. Pending events, ticks and owed output precede that attempt; independent permanent TX blockage is not a finite-delivery guarantee. Expiration intentionally discards the remaining refused work while earlier applied attributes remain for MRP refresh/aging. The one-second recovery policy does not establish compliance with the separate 10 ms service budget under exhaustion. Timing tests preserve original arrival/deadline and reject an eleven-millisecond stall; their mailbox-access and CPU allowance is a conditional host envelope. Target scheduling, target execution and wire-departure timing remain unproven.

The full parent, processor, gPTP, synthesis and builder banks were not run. The supplied manager source-bank passes are reported evidence, distinct from the executions in this packet and from the final current-dev candidate. The selected processor-wire differential is not a full processor-suite run. The exact-head hosted snapshot in `receipts/hosted.json` has successful executed checks and four synthesis shards, with firmware, documentation, elaboration and simulation work still running at capture; aggregate acceptance is not claimed. Physical gPTP was skipped. Physical calibration was NOT RUN, and field skips are not hardware proof.

The manager owns the remaining independent review, residue correction, hosted/local-replica acceptance, construction and full validation of the merge candidate against live dev, explicit maintainer merge authorization, containment and appropriate issue/project closure. F3 binding composition, live MAAP/stream updates, the fabric licence connection and target release validation remain the documented integration work. This source-head review grants no merge authorization.

No source fixes, commits, pushes, GitHub writes, author contact, delegated agents, container runner, privileged operation, shared installation or hardware operation occurred. Final integrity verifies 1185 parent blobs and 936 dependency blobs, file modes, complete indexes, required gitlinks and no hidden index flags or untracked files. The optional external dependency remains uninitialized with its gitlink unchanged. Publish REPORT.md and only the files listed in MANIFEST.sha256. Scratch is never published. Normalization changes only local path prefixes; original and published digests are retained.

R533-7 FINISHED
