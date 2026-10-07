[R533] NEGATIVE - exact head 500b8f64443777685e6a54049d933476710d26f0

Round R533-5, external independent delta review of issue #665 / PR #690.
Tree: b1b7d3b1b9dcf7d8f3f7f299365392ebc1f17ed8.
This independent verdict and ledger were written before reading prior review findings or reports.

**R533-5-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs | Transient receive exhaustion loses an accepted withdrawal**

Artifact: `sw/firmware/ctrl/srp/srp_mbx.c:373`; `sw/firmware/ctrl/loop/ctrl_loop.c:129`; `third_party/lwSRP/doc/integrator.md:215`; `sw/firmware/ctrl/test/srp_fixture.hpp:142`; PR #690 body, Round 5.
Authority/evidence: the new pin requires receive-payload retry after temporary propagation reservation fails. The adapter consumes the mailbox record before calling mrp_rx, counts every negative result as malformed, and retains no payload for retry. An existing registered Listener now needs temporary storage even for its withdrawal. In independent.cpp, establish Ready, exhaust the actual static pool, receive valid Lv, release every held block and service another 10 ms. Both interface configurations remain active, received=1, malformed=1, stops=0. The identical probe with the previous library pin stops correctly: active=0, received=2, malformed=0, stops=1. Milan 4.2.7.2.2, the F4 rapid-withdrawal contract and FR_NFR 3.4.1's prohibition on dropping accepted records apply. The four adjusted fixtures correctly preserve their post-receive allocation tests but do not cover this new receive-refusal obligation.
Impact: a valid withdrawal can be permanently lost locally after transient exhaustion; storage recovery does not revoke the talker's licence. This is a dependency-integration regression, distinct from the passing ordinary #608 LV case.
Required outcome: handle the new recoverable receive failure without losing the accepted payload or later attributes, preserving interface identity, ordering, lifecycle cancellation and bounded service. Add a receive-time exhaustion/recovery regression alongside the existing poll-time allocation tests. Do not label a valid transiently refused PDU as malformed. Correct the public Round 5 claim that "no production adapter change is needed" when recording the repair: this is a behavior claim contradicted by the probe, not wording-only residue.
Verification: the attached exact-head probe must pass at IF=1/2 without retransmission from the peer, and an appropriate retry-removal plant must fail it. Recheck mixed-attribute payloads, repeated refusal, link reset and cross-interface ordering, plus the unchanged coverage ratchet and existing SRP campaign.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | REQUIREMENTS.md:23; docs/reference/FR_NFR.md:332; srp_mbx.c:349; lwSRP integrator.md:215; independent.cpp | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| RTL | UNCLEAN, F1 | srp_mbx.c:342; ctrl_loop.c:122; mbx.c:132; lwSRP mrp_mad.c:534; production-scope diff | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Robustness | UNCLEAN, F1 | srp_mbx.cpp lifecycle/shared-binding/#608 cases; independent.cpp; receipts/head-probes-if1.log and head-probes-if2.log | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Tests | UNCLEAN, F1 | srp_fixture.hpp:142; srp_mbx.cpp:333; srp_mutants.py; fw_coverage.py; coverage.ratchet; receipts/campaign.log and probes.json | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |
| Docs | UNCLEAN, F1 | sw/firmware/ctrl/srp/README.md; docs/reference/SUBMODULES.md; docs/testing/CI_WORKFLOWS.md; .github/workflows/rtl-fast.yml; public author-r5/HANDOFF.md and PR body Round 5 no-adaptation claim; receipts/sizes.json and submodule-docs.log | R533-5 | 500b8f64443777685e6a54049d933476710d26f0 |

All five lenses were applied. None banks clean coverage while F1 remains open. The independently written initial verdict/ledger is retained in `receipts/independent-verdict-before-priors.md`. Docs was subsequently added to F1 after the live PR body's explicit no-adaptation claim was read. This report grants no merge approval.

**Scope and independent results**

Reconstructed the issue body, owner directives 5992455815/6008744385/6009661573, F4 assignment 6030279477, linked-size addition 6030870481 and round-5 assignment 6037276691, after AGENTS.md, CONTRIBUTING.md and the documentation index. Read REQUIREMENTS.md, FR_NFR 3.4.1/3.4.2, the mailbox contract/design and both adapter/library interfaces. Examined the required `db9aa8c9..500b8f64` history/delta, separating merged dev work from F4, then inspected the immediate `6f7deea1..500b8f64` delta and dependency `23d9a817..a4cbe41d` changes. Public author evidence was read after the independent source pass. No private author material or another current-round report was used.

The round-5 parent change is 14 paths. Production adapter `.c`/`.h`, pool sizing and coverage ratchet are byte-identical to round 4. The pin and its build guard agree on `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. The only behavioral fixture change is the four post-RX exhaustion setups. Each is justified by the library's new temporary reservation and still detects its original adapter-poll defect; all four matching plants were caught. That preserves those tests, but does not discharge F1's separate receive-retry contract.

Conformance checks covered the MSRP-only Milan opt-in, ordinary IN withdrawal, #608's unchanged LV deadline, generic MVRP behavior, Class A Domain, shared Listener/VID ownership and selected processor-wire cases. The independent malformed-suffix and higher-version probes pass. New LV changed-value indication reaches adapter bookkeeping before poll, and its removal is detected. The pending-Flush API is not called by this end-station adapter: `reset_interface` destroys/recreates participants. Its owned snapshot and FIFO changes were reviewed against that lifetime boundary and the remeasured footprint; no independent bridge/topology campaign is claimed.

The RTL lens includes software/interface architecture. F4's scope against integrated dev `d51b373a` changes no HDL, mailbox YAML, builder, configuration, constraints, synthesis or shipping-selection inputs. The broader FC-base diff contains already merged dev work, including the AAF change; it is not incorrectly attributed to F4. Reviewed per-interface ownership, centisecond dispatch, immutable owed TX, mailbox commit order, reset fences, shared bindings and static allocation. The new receive-error boundary is the open architectural defect.

| Executed check | Result | Receipt |
|---|---|---|
| Focused adapter / selected wire differential / latency, IF=1 and IF=2 | 53 / 5 / 4 cases pass at each count | `receipts/suites.log`, `suites.rc` |
| Entire SRP mutation campaign, four compilation jobs | 70/70 named catches, rc 0; build failures do not count | `receipts/campaign.log`, `receipts/campaign/` |
| Complete firmware coverage measurement | 15 files at 100% lines/branches after existing exclusions; SRP 441/441 and 410/410, no SRP exclusion or new exclusion | `receipts/coverage.log`, `coverage.rc` |
| Independent head probes | Three positive cases pass; withdrawal/recovery fails at both counts | `receipts/head-probes-if1.log`, `head-probes-if2.log` |
| Previous-pin withdrawal control | Same test passes at IF=1/2 | `receipts/old-pin-withdraw-control-if1.log`, `old-pin-withdraw-control-if2.log` |
| Three independent dependency plants | All compile and fail their named positive test at IF=1/2, 6/6 catches | `receipts/probes.json`, individual plant logs |
| Public runtime reconstruction | All 57 input-file SHA-256 values match the published provenance | `receipts/runtime-inputs.json`, `runtime-fetch.log` |
| SDK reconstruction and linked measurement | Verified pinned archive; eight head/base links pass | `receipts/sdk.log`, `sizes.json`, `sizes.log` |
| Submodule documentation and generated diagram | Exact five gitlinks and decoded diagram pass | `receipts/submodule-docs.log` |
| Source scope, whitespace and exact restoration | No mismatch | `receipts/source-checks.json`, `integrity.json` |

The three independent plants remove atomic pre-validation, limit changed-value indication to IN (losing LV), and suppress higher-version unknown-message skipping. Their respective probes fail on licence side effects, missing callback bookkeeping, and loss of the following known Listener. The probe collector deliberately returns zero after collecting expected failures; each binary's actual result is in `probes.json` and its tally. Its zero is not an exact-head behavior pass. The first custom-probe build lacked the tally-label definition and failed to link; that setup attempt is not counted. The corrected probe source and all final diagnostics are retained.

**Linked composition**

These independent links exactly reproduce the four published round-5 spans. FC base `db9aa8c9b135b34ff3d070a979dee70440b37cc6` was exported into scratch and linked without SRP using the same harness and runtime. The reserved stack is 8192 bytes in every row; initialized data is zero. Pools below are included in BSS, not added again.

| Shape / IF | text | rodata | BSS | pool within BSS | linked span | FC base span | delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 / 1 | 28108 | 2846 | 15432 | 9920 | 54592 | 18752 | 35840 |
| 1x1 / 2 | 29084 | 2846 | 25708 | 19840 | 65840 | 19248 | 46592 |
| 8x8 / 1 | 28048 | 2846 | 30184 | 24032 | 69280 | 18752 | 50528 |
| 8x8 / 2 | 29028 | 2846 | 55212 | 48064 | 95296 | 19248 | 76048 |

Spans include alignment. The largest is about 72.7% of 128 KiB, before later-lane composition. The public round-4-to-round-5 increases are 624/624/624/640 bytes; this round independently rebuilt the new head and FC base, not the old round-4 links. These are reachable size fixtures, not booted images, whole-call-chain stack proofs or routed resource measurements. `sizes.json` includes section, storage, ELF/map and runtime hashes.

**Prior public findings at this head**

Read the eight prior R532/R533 review comments only after writing the independent verdict/ledger. The PR has no submitted formal reviews or inline review comments in the retrieved inventory. Public references and IDs are in `receipts/prior-inventory.json`; none of their verdicts substitutes for this round's execution.

| Prior item | Disposition and current evidence |
|---|---|
| R533-1-F1 / R532-1-F1, missing Milan immediate Leave | Original table/opt-in defect remains RESOLVED: immediate Listener/Talker and MVRP/#608 tests pass. The new exhaustion-specific failure is separately open as R533-5-F1; the overall rapid-withdrawal obligation is therefore not clean. |
| R533-1-F2 / R532-2-F1, link lifecycle and missing level recovery | RESOLVED, retained: attach-level and poll-level reconciliation, adjacent edges, stale-prefix fences and recovery tests pass; their plants are caught. |
| R533-1-F3 / R533-2-F1, shared StreamID and replacement | RESOLVED, retained: aggregate reconciliation, inherited Applicant state, consecutive replacement and both binding orders pass; corresponding plants are caught. |
| R533-1-F4, linked size | RESOLVED: independently reproduced all four new head spans and four FC-base links, with reachable SRP symbols and separate section/storage accounting. |
| R532-1-F2 parts 1/2, admission and ReadyFailed sensitivity | RESOLVED, retained: exact ceiling and strict Ready-to-ReadyFailed cases pass; overhead/ceiling/callback plants are caught in the 70-plant campaign. |
| R532-1-F2 part 3 / R533-2-F2, note-4/5 evidence | RESOLVED, retained: public PR #15 head `ced667d8` was fetched. Its production `src` diff against `a4cbe41d` is empty; both named integration tests and the three reversal mappings are present. Their upstream suites were not re-executed here; this public follow-up is not a pin finding under the assignment. |
| R532-2-F2, missing dependency inventory/diagram | SOURCE RESOLVED: updated pin, licence/ownership row and generated diagram pass the documentation gate. Hosted acceptance remains separate. |
| R532-2-F3, last never-eligible binding leaks VID | RESOLVED, retained: both unbind orders pass, with the original never-requesting setup preserved; `last-ineligible-vid-leaks` is caught. |
| R532-2-F4, three lifecycle/shared-VLAN test escapes | RESOLVED, retained: `reset-keeps-owed-domain`, `reset-keeps-sink-vlan` and `shared-ready-uses-first-vlan` are all caught. The first uses one of the legitimately restaged exhaustion fixtures. |
| R532-3-F1, cross-slot/cross-StreamID test gaps | RESOLVED, retained: both wire regressions pass; `joining-binding-loses-applicant` and `applicant-inherited-across-streams` are caught. |
| R532-3-F2, Domain-VID final-unbind gap | RESOLVED, retained: startup VID 2 and peer VID 7 cases pass; `final-unbind-withdraws-domain-vid` is caught; README states the exception. |
| R532-1-S1, upstream LeaveAll scope test | ADDRESSED, retained: pinned `integration_test.c` contains the per-message-type/per-port case; the parent Run-B differential passes. |
| R532-1-S2, generic LV/rJoin extra indication | RESOLVED by the new pin: `mrp_mad.c:354` and `:361` use REG_IND_NONE for ordinary LV recovery, while `:632` supplies changed-value indication. Upstream `review_test.c:288` checks no duplicate Join/map. Static inspection plus the independent changed-LV probe; no upstream suite replay claimed. |
| R532-1-S3, failed participant recreation | ADDRESSED, retained: partial creation releases both participants; retry and peer-interface service cases pass. |
| R532-2-S1, Milan option accidentally affecting MVRP | ADDRESSED, retained: composition test passes at both counts and its scope plant is caught. |
| R532-1-R1, TICK units | RESOLVED, retained: README distinguishes centisecond events from NOW_MS. |
| R532-1-R2, absent linked-size limitation | SUPERSEDED/RESOLVED: actual linked evidence exists; the obsolete object-only limitation must not be restored. |
| R532-2-R1, fetch wording | RESOLVED: current docs identify public main and anonymous HTTPS; the assigned pin was fetched successfully. |
| R532-3-R1, stale STOP/compiler-absent status | RESOLVED, retained: the stale STOP is gone; manager comment 6036186046 records the earlier compiler-absent rc 0 and expected non-execution of its compiler-dependent census. |
| R532-2-R2, publication tense | RETAINED as wording-only RESIDUE below. |

**R532-2-R2 | RESIDUE | Docs | Published PR still says its head awaits publication**

Artifact: PR #690 body, Status and How to get into the same state; captured in `receipts/pr-body.txt`.
Authority/evidence: PR metadata and review-start comment 6038107200 identify published head `500b8f64`, but the body says "REVIEW READY locally", "This new head awaits publication" and "After publication, set".
Impact: tense only; it changes no measurement, verdict, clause claim, test, code, generated artifact or privacy rule. This residue does not make a lens unclean.
Exact fix: change "Round 5 REVIEW READY locally:" to "Round 5 REVIEW READY:"; replace the two publication-status sentences with "Round 4 at `6f7deea15a9160761b30aaa93fe152f20d416695` received two positive reviews. PR #690 now publishes `500b8f64443777685e6a54049d933476710d26f0`; reviews of this head are recorded in its discussion."; replace "After publication, set" with "To inspect the published head, set".
Verification: reread the published PR body. Manager carries this exact edit on the residue checklist.

**Limits and pending manager duties**

The cited immutable round-5 public folder at archive `0fc49330` contains HANDOFF.md and PR-BODY.md, not their named ROUND5 raw-receipt files. Those pages are treated as author summaries. The earlier public runtime provenance was sufficient to reconstruct all 57 inputs; the decisive source/coverage/size/probe results above were independently executed. Publish the missing cited receipts or remove dangling receipt references. The supplied manager statement that full source static/builder and native banks passed is not a final current-dev candidate result.

This review did not run the prohibited full parent, processor, gPTP, synthesis or builder banks, container replication, host replication orchestrator/self-test, shared installs or hardware. It did not rerun the mailbox RTL suite, the 100 control plants, all target object arms or the upstream unit/behavior/reversal suites. The scoped HDL compiler's identity was checked as release 5.050; it was not needed for the focused source probes. No exact-head hosted-job snapshot was taken; hosted/local-replica acceptance remains the manager's, and no skipped context is counted as executed work.

Host timing retains the documented 100 ns/access, aggregate 1 ms CPU/preemption and 100 ns uncertainty assumptions. Positive timing cases and the 11 ms backpressure rejection pass; they prove neither target scheduling nor wire departure. Physical calibration was NOT RUN; field skips and source tests are not hardware proof. The reserved stack remains an assumption. ACMP composition, live MAAP/stream inputs, actual fabric licence output and physical acceptance remain scoped integration work.

The later merge with dev, now assigned as `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`, is not a finding here. The manager must fix/re-review F1, obtain the independent review bar, construct and validate the final candidate at the live dev tip, discharge hosted/local-replica and builder/compiler-absent obligations, obtain explicit merge authorization, and perform containment and issue/project completion. The later LICENSE-only upstream main `3626f1ea` and note-test PR #15 are not findings.

All campaigns remained foreground processes; independent runs were concurrent with at most sixteen compilation jobs. All source mutations used scratch copies. No source fix, commit, push, GitHub write, author contact, merge or other-checkout edit occurred. Final verification directly hashed 1169 parent blobs, 558 processor blobs, 104 gPTP blobs, 214 datapath-library blobs and 60 lwSRP blobs, checked file modes, complete stage-0 indexes and hidden flags, and verified all four required gitlinks. There were no mismatches or untracked source files. The optional external import remains uninitialized with its gitlink intact. No restoration edit was necessary.

Publish only REPORT.md and files listed in MANIFEST.sha256. Scratch is excluded. Scripts, exact reproduction instructions, diagnostics and exit receipts are included; absolute local roots in publishable logs are normalized, with original hashes retained in the receipt provenance.

R533-5 FINISHED
