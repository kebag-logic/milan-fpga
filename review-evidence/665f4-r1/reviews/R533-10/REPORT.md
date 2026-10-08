[R533] NEGATIVE - exact head 82a79638405c3365e4078da471be56758f8dd679

R533-10 external independent review of issue #665 / PR #690. Two MAJOR findings remain in the new SRP-to-ACMP feedback. Initial registration, invalid-VID parking, and the strengthened bounds checks work, but a settled listener can report an obsolete registration type or miss a real withdrawal. The four affected lenses are UNCLEAN. No new MINOR, RESIDUE or SUGGESTION is filed.

Tree: `f09d67734ca6ccab67a2482d884331c6b4d2056c`. Reconstructed AGENTS/CONTRIBUTING, `docs/README.md`, the issue and frozen public decisions, linked requirements/interfaces, then the source-base diff `d8b355fe0f41d49dca6cae1cd8b3826e2edde364..82a79638405c3365e4078da471be56758f8dd679` and history. The focused delta is `edeef61c5a0cc6c18caa61db4019a8e378baf366..82a79638405c3365e4078da471be56758f8dd679`: `da36eb15f38d23aa4cddc9183e62e0a94f339dd9` and `82a79638405c3365e4078da471be56758f8dd679`. All five lenses were independently applied and an initial verdict and ledger written before reading prior public findings. The subsequent reconciliation below includes both round-9 verdicts and their earlier finding dispositions.

Public scope: [issue #665](https://github.com/kebag-logic/milan-fpga/issues/665), [round-10 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6048644347), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6049231637), and [review start](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6049245400). Evidence was read at [published commit 8ba25cb0](https://github.com/kebag-logic/milan-fpga/tree/8ba25cb06ac3f67c499a22179fc7960f67aeb3e3/review-evidence/665f4-r1), including `author-r10`. No private author material or another current-round report supplied this verdict.

**R533-10-F1 — MAJOR — Conformance, RTL, Robustness, Tests — a settled listener reports stale REGISTERING_FAILED after the registration type changes.**

Artifacts: `sw/firmware/ctrl/app/ctrl_app_srp.c:80-86`; `sw/firmware/ctrl/acmp/acmp.c:832-850,1116-1130`; `sw/firmware/ctrl/srp/srp_mbx.c:483-496`; `sw/firmware/ctrl/test/srp_binding.hpp:245-306`; [executed IF=1 probe](receipts/independent-wire-if1.log), [IF=2 probe](receipts/independent-wire-if2.log), and [portable probe source](scripts/independent_feedback.hpp).

Authority/evidence: the frozen assignment requires per-sink registration changes, including Failed. Milan v1.2 5.5.3.5.44 / Table 5.39 requires GET_RX_STATE_RESPONSE to report the current Failed registration. Table 5.23 states the flag's meaning. IEEE 802.1Q-2018 35.2.6 permits replacement through JoinIn/JoinMt and gives Failed precedence for conflicting New registrations. The exact local standards editions are identified by hash in `receipts/standards-identity.json`.

The new delivery guard invokes `acmp_tk_registered` only in SETTLED_NO_RSV. After the listener reaches SETTLED_RSV_OK, a nonzero-to-nonzero SRP change is ignored. The independent tests use real mailbox frames and GET_RX_STATE commands, with two distinct sink identities. On both interface counts:

| Received change | SRP's resulting `desired` | ACMP `tk_failed` | Actual GET_RX_STATE flags | Required Failed bit |
|---|---:|---:|---:|---:|
| Advertise, then conflicting Failed New | 1 (Failed) | 0 | `0x0002` | set (`0x0040`) |
| Failed, then Advertise JoinIn replacement | 2 (Advertise) | 1 | `0x0042` | clear |

Both sinks reproduce this at IF=1; at IF=2 the sinks use ports 0 and 1. The assertions verify that SRP accepted the changed registration, and the response check observes the actual outgoing ACMP frame. The replacement probe permits a correctly initiated withdrawal/reprobe with SRP stopped; it does not require an invalid repeat state-machine event.

Impact: the controller receives incorrect current reservation failure status for the lifetime of the settled binding. A recovered registration can remain reported failed; an actual Failed registration can remain reported healthy. Existing first-registration tests and 100% branch coverage do not detect either sequence.

Required outcome: propagate the current registration type through the serialized composition contract after settlement, preserving the sink and interface. Honor any withdrawal/reprobe required by replacement. Repeated unchanged registration must remain idempotent. Do not simply replay EVT_TK_REGISTERED in SETTLED_RSV_OK: Milan Table 5.30 marks that event/state combination impossible. Choose a valid status/event contract without synchronous callback reentry.

Verification: both replacement directions must produce correct observable state and GET_RX_STATE flags at IF=1/2; add standing tests and discriminating plants for loss of each update, alongside unchanged-registration and per-interface controls. The existing `R533FailedReplacementUpdatesReportedRegistration` and `R533AdvertiseReplacementClearsReportedFailure` must pass on the corrected head.

**R533-10-F2 — MAJOR — Conformance, RTL, Robustness, Tests — the post-poll snapshot erases a withdrawal followed by same-pass re-registration.**

Artifacts: `sw/firmware/ctrl/app/ctrl_app_srp.c:78-86`; `sw/firmware/ctrl/srp/srp_mbx.c:72-84,483-510,634-681`; `sw/firmware/ctrl/loop/ctrl_loop.c:119-160`; the same independent probe source and IF=1/2 receipts above.

Authority/evidence: Milan Table 5.29 defines the registered-to-unregistered transition event. Milan 5.5.3.5.48 requires a settled listener to stop SRP and reprobe on that event; 4.2.7.2.2 gives MSRP the immediate IN/Leave behavior. The frozen assignment includes withdrawal delivery, serialized under #678. Serialization must preserve this observable transition.

Starting from a settled Advertise, the probe queues a valid MSRP Lv and a New registration for the same stream before loop service. The loop receives both records before the feedback poll. The adapter's final `desired` is again 2, so the delivery code sees only a registered snapshot. ACMP remains state 7 (SETTLED_RSV_OK), and the old SRP binding remains active. This occurs for both sinks at IF=1 and both configured ports at IF=2. The test verifies that exactly two SRP records were received. Its paired positive control puts the same Lv in a separate pass: ACMP correctly enters PRB_W_AVAIL and SRP becomes unbound.

Impact: a real loss of Talker registration can be silently skipped whenever renewal or replacement is consumed in the same pass. The prescribed teardown and reprobe are omitted, leaving a stale settled binding. A boolean final snapshot cannot distinguish continuous registration from loss followed by recovery.

Required outcome: retain the per-sink/per-interface withdrawal transition until the composition consumes it, even if a later receive or timer/RX sequence restores registration. Deliver the resulting protocol action outside library/port callbacks, preserve ordering, and retire obsolete feedback when ACMP supersedes the binding. This finding concerns an event that happened, not repeated notification of an unchanged state.

Verification: `R533WithdrawalBeforeReregistrationStillReprobes` must pass at IF=1/2 while `R533SeparatePassWithdrawalDoesReprobe` stays green. Add standing discriminating plants for dropping the retained transition, plus isolation and supersession checks. Cover expiration followed by fresh receive before delivery as another source of the same event-loss risk; that variant was identified statically, not executed here.

**Round-10 acceptance and prior round-9 disposition at this head.**

| Assigned item | Disposition | Exact-head evidence |
|---|---|---|
| R532-9-F1: initial Advertise/Failed/withdrawal feedback, healthy listener beyond TMR_NO_TK, no reentry, per interface | Original missing-wiring and 10 s timeout failure resolved; broader registration-change acceptance remains OPEN through R533-10-F1/F2 | Original `probe_tk_registered.hpp` passes IF=1/2 beyond 12 s. Native registration, Failed, withdrawal, repeated-registration and isolation cases pass. All six `feedback-*` plants are caught at each count. `ctrl_app_srp.c:50-91` delivers after SRP returns. The new type-change and coalesced-withdrawal probes fail. |
| R532-9-F2: visible parking of permanent VID refusals, retirement of an old accepted binding, sleep, replacement/unbind, transient retry | RESOLVED | `ctrl_app_srp.c:37-76`, `ctrl_app.h` request state, `srp_binding.hpp`. Original `probe_invalid_vid.hpp` passes IF=1/2. VID 0, 4095 and 65535 park; the old binding is retired, including refusal/retry; replacement clears parking. `binding-invalid-retries`, `binding-invalid-upper-bound`, `binding-park-never-clears` and `binding-park-keeps-old` are caught at both counts. Transient receive/transmit refusal tests still pass. |
| R532-9-F3: each poll/pass term reached independently, eight formerly escaping plants | RESOLVED | `srp_app.cpp:145-230`, `srp_cost_probe.hpp`, `srp_bounds.h`, `srp_mutants.py`; native measurements and `prior-bounds-if*.json`. All effective original plants fail named executed assertions. Replacing MBX_N_IF with 1 is equivalent at IF=1 and correctly passes there; it fails at IF=2. The standing interface-count understatement is discriminating and caught at both counts. |
| R532-9-S1/S2 | ADDRESSED | Header indentation/comment and the `without_delivery` helper are present. |

The retained portion of R532-9-F1 is not relabeled as target integration or deferred to another issue. Its original documentation omission is corrected: the composition now owns both directions and the snapshot/serialization contract is documented. The two current defects are behavior and missing-sequence-test defects under the four lenses named above. The current bounds figures and measurement descriptions are supported; no separate documentation defect was found.

**Independent validation.** Commands and return codes are retained in the execution JSON files; child `.rc` files determine results. `run_group.py` waits for all children and does not turn intentionally failing probes into a group-level failure. Expected plant/probe failures are explicitly distinguished from clean controls.

| Work executed | Result and receipts |
|---|---|
| Six native suites at IF=1 and IF=2 | 118 tests pass at each count: adapter 53, retained RX 17, SRP composition/bounds 5, four-module composition 33, latency 5, walk 5. `native-if*.log` and `native-group-execution.json`. |
| Selected standing mutations | 46/46 caught at each count, 92 total. Binding, feedback, four-module wiring, bound terms and added real reads. `plants-if*.log`, individual `plants-if1/` and `plants-if2/` logs. Each campaign receives `--jobs 4`. |
| Original round-9 executable probes | Healthy Talker and invalid-VID probes pass both counts. Eight bound-plant kinds rerun at both counts: 15 discriminating failures, one explicit IF=1 equivalent pass, and two pristine controls pass. `prior-if*.log`, `prior-bounds-if*.json`, individual original-plant logs; imported probe hashes recorded. Build refusals are not accepted as catches by the new driver. |
| Independent current-round wire probes | Four tests per count: three fail for F1/F2 and the separate-pass withdrawal control passes. Final `independent-wire-if*.log` only. No production patch was used. |
| Coverage checker | PASS, all 22 files at 100% after unchanged exclusions. `ctrl_app_srp.c`: 75/75 lines, 60/60 branches; `srp_mbx.c`: 469/469 lines, 438/438 branches without exclusions. `coverage.log`. This is coverage of the executed paths, not proof of temporal sequence completeness. |
| AddressSanitizer controls | Both compiler families: pristine A0/core/adapter passes, relaxed-source-limit A0 plant fails the named assertion with no sanitizer memory report; SRP and four-module suites pass at IF=1/2. Twelve expected outcomes all met; instrumentation confirmed in all five binaries per compiler. `asan-results.json`, instrumentation JSON and twelve raw logs. Leak detection was disabled; address checking remained enabled. |
| Linked image fixtures | Four fresh RV32I/ILP32 links reproduce every reported section, static-storage figure, RAM span and final ELF hash. `images.log`, `image-comparison.json`, `runtime-provenance.json`, `public-round10-sizes.json`. SDK extracted only under scratch. |
| Focused documentation/interface checks | Eleven commands pass: mailbox generator, docs, style, paths, C++/Python idioms, submodule ownership, diagram source/PNG checks, em-dash renderer and diff whitespace. `docs-group-execution.json` and `docs-*.log`. |
| Public evidence binding | Verified 13 changed-file hashes against this checkout, and all 108 retained logs against the public receipt hashes across 110 recorded invocations. Two full logs are not retained; no independent execution claim is made for those banks. `public-evidence-audit.json`. |

The first expanded probe had an assertion-macro bracing build error; it was corrected in the reviewer-only header before the final executed run. The first sanitizer receipt script inspected only undefined symbols, missing the statically linked runtime. It was corrected to inspect the full symbol table and all twelve runs were repeated successfully. Neither construction error is counted as a product failure. `receipts/probe-construction.txt` records this accounting.

The SRP fixed poll allowance is four reads per interface across separately measured alternatives. The real `send_pdu` path costs 383 accesses per maximum transmit; two calls per interface yield poll bounds 770/1540. Eight event records cost 56 accesses; two maximum RX records and callbacks cost 770; total SRP pass bounds are 1596/2366. Real extra poll/send reads are caught. The four-module algebraic total is 3192/4041, including a conservative 64-access feedback allowance (four per possible sink). These are mailbox-access envelopes; alternative maxima are not claimed as one simultaneous trace or CPU/target timing.

| Linked shape | Interfaces | text | rodata | BSS | Reserved stack | RAM span |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 | 1 | 45016 | 2878 | 23432 | 8192 | 79536 |
| 1x1 TDM8 | 2 | 46356 | 2878 | 34792 | 8192 | 92240 |
| 8x8 | 1 | 44956 | 2878 | 38184 | 8192 | 94224 |
| 8x8 | 2 | 46324 | 2878 | 64296 | 8192 | 121712 |

All data sections are zero. Round-9-to-10 span deltas are +752/+752/+736/+752 bytes; BSS is unchanged. Runtime archive/map hashes can vary with build paths; the four linked ELF hashes themselves match the published round-10 images exactly. Stack reservation is not a measured call-chain bound. The default build and shipping image remain outside this opt-in fixture.

**Earlier public findings explicitly reconciled.** Baseline sources are [R532-9](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6048639631), [R533-9](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6048464296), and the earlier public disposition tables they carry. “Retained resolved” below means the remedy remains in the exact-head artifacts examined; it does not assert a fresh execution of every historical campaign.

| Prior finding(s) | Disposition at this head and examined evidence |
|---|---|
| R533-8-F1 | RESOLVED, retained: ACMP-to-SRP intent ownership, serialization, cancellation, retries, identity and interface isolation in `ctrl_app_srp.c` and `srp_binding.hpp`; native cases and binding plants rerun. Reverse feedback defects are the two findings above. |
| R532-8-F1 | SOURCE/TEST defect RESOLVED: `test_acmp.cpp:208-221` owns the extra byte; current A0 sanitizer controls/plant confirm the named assertion, without an overflow. Hosted acceptance remains a manager duty. |
| R532-8-F2 | RESOLVED, strengthened by the R532-9-F3 repair: actual callback/record measurements, seven standing bounds plants and current per-term checks run at both counts. |
| R532-8-F3 | RESOLVED: `maap/README.md:134`, the three-module test and mutation name the 1580/1659 `CTRL_APP_THREE_PASS_MAX`; current four-module totals are separately 3192/4041. |
| R532-8-F4 | RESOLVED: `ctrl/README.md` limits its mutation claim to exact-mask, SRP-only-wake and algebraic-bound checks; six `four-way-*` plants caught per count. |
| R533-1-F1; R532-1-F1 | RESOLVED, retained: immediate MSRP leave and original #608 LV deadline in the unchanged public dependency/adapter, `srp_mbx.cpp` and `srp_walk.cpp`; current native suites pass. This does not clear the later composition event-loss finding F2. |
| R533-1-F2; R532-2-F1 | RESOLVED, retained: attach/poll link-level recovery, lifecycle fencing and recreation in `srp_mbx.c` and native lifecycle tests. |
| R533-1-F3; R533-2-F1; R532-2-F3/F4; R532-3-F1/F2 | RESOLVED, retained: shared StreamID reconciliation, replacement-state inheritance, final-user VLAN and Domain ownership in `srp_mbx.c`, current native shared-binding cases. |
| R532-1-F2 parts 1/2 | RESOLVED, retained: admission ceiling and strict Ready-to-ReadyFailed callback cases in `srp_mbx.cpp`; current native tests pass. |
| R532-1-F2 part 3; R533-2-F2 | RESOLVED, retained statically: public exact lwSRP pin, `tests/unit/integration_test.c` note-4/5 cases and `tests/check_reversals.py`; upstream full profiles were not rerun. |
| R532-2-F2 | RESOLVED, retained: public gitlink, `SUBMODULES.md`, `THIRD_PARTY.md` and generated boundary diagram; current ownership/docs checks pass. |
| R533-5-F1; R532-5-F1; R532-6-F1 | RESOLVED, retained: complete retained receive, recoverable retry and original-arrival 1000 ms expiration. All 17 `srp_rx_retry.cpp` cases rerun at IF=1/2. |
| R533-1-F4; R532-6-F2 | RESOLVED: historical base comparisons remain public; four current linked images and their round-9 deltas reproduced above. |
| R533-6-F1 | RESOLVED, retained statically: the mailbox export recipe names existing paths and includes NVM headers. No round-10 mailbox/RTL change; the mailbox bank was not rerun here. |
| R532-1-R1/R2; R532-2-R1; R532-3-R1; R532-5-R2; R532-7-R1 | RESOLVED, retained: tick units, linked-size scope, public fetch status, merged-note wording, and “completes or expires” in current docs. |
| R532-2-R2; R532-5-R1; R532-6-R1; R533-6-R1; R533-7-R1; R533-8-R1 | RESOLVED, retained: current PR body publication status and “Use this checkout recipe.” |
| R532-8-R1/R2 | RESOLVED, retained: the current composition description includes SRP attachment; the 256-byte pool describes the separate historical fixture. |
| R532-1-S1..S3; R532-2-S1; R532-5-S1/S2; R532-6-S1; R532-7-S1 | Prior addressed/optional disposition retained; unchanged affected behavior/docs, current relevant native tests. No new blocking finding asserted under these historical suggestions. |
| R532-8-S1/S2/S3 | S2 addressed by the MAAP prerequisite. Historical F6 naming and historical size-table suggestions remain optional; neither is counted as a clean-lens defect. |

**Reviewer-owned ledger.** The complete head is repeated deliberately. CLEAN applies only to the artifacts and scope actually examined here; no earlier round's coverage is silently transferred over changed artifacts.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F2 | Issue #665 frozen F4/round-10 scope; FR_NFR 3.4.1/3.4.2; Milan Tables 5.29/5.30/5.39 and 5.5.3.5.36/.42/.44/.48; `ctrl_app_srp.c:37-91`, `acmp.c:832-850,1116-1146`, `srp_mbx.c:483-510`; wire probes | R533-10; no clean covering round | 82a79638405c3365e4078da471be56758f8dd679 |
| RTL | UNCLEAN — F1, F2 | Source-base/delta RTL and contract diff, `MAILBOX_SPLIT.md`, `ctrl_app.h/_srp.c`, `ctrl_loop.c:119-160`, `srp_mbx.h/.c`, ACMP callback/state contract; no changed RTL, reset or CDC primitive in this delta | R533-10; no clean covering round | 82a79638405c3365e4078da471be56758f8dd679 |
| Robustness | UNCLEAN — F1, F2 | `srp_binding.hpp`, `srp_rx_retry.cpp`, `srp_mbx.cpp`, invalid-VID retirement/retry paths, failed/healthy replacements and paired same-pass/separate-pass withdrawal probes at IF=1/2 | R533-10; no clean covering round | 82a79638405c3365e4078da471be56758f8dd679 |
| Tests | UNCLEAN — F1, F2 | `srp_app.cpp`, `srp_cost_probe.hpp`, `srp_mutants.py`, `test_acmp.cpp`, campaign drivers/ratchet, native/plant/coverage/sanitizer receipts and independent wire probes; missing temporal sequences demonstrated | R533-10; no clean covering round | 82a79638405c3365e4078da471be56758f8dd679 |
| Docs | CLEAN | `ctrl/README.md:126-159`, `srp/README.md:53-84,230-245,294-305`, `maap/README.md:134`, `MAILBOX_SPLIT.md:715-749`, header comments, public scope/PR/evidence, linked size fixtures; supported ownership, bound and image claims with explicit limits | R533-10 | 82a79638405c3365e4078da471be56758f8dd679 |

[R533] PASS Docs — the exact-head README/design/public-evidence artifacts named in the ledger — checked changed ownership, parking, serialization, measured bounds, image figures and remaining target duties against code, public decisions and executable receipts. No open wording, measurement or clause-attribution defect is banked under this lens. This is not approval of the two behavior defects.

**Real limits and pending manager duties.**

This is source validation at the published head, not validation of a final merge against current dev. Full parent/PP/gPTP, synthesis, builder and full mutation banks were not rerun. The manager's public static/builder/native evidence was examined and hash-bound where retained. The builder's recorded earlier implementation head is disclosed in `ROUND10-SOURCE.json`; the final delta changes a header comment, tests and ratchet, not its production inputs. Current independent image links use the final reviewed source.

No hardware was accessed; physical calibration was NOT RUN. Field skips provide no hardware proof. Access-count envelopes omit CPU work/external-port cost; the retained-RX exhaustion policy can still exceed the 10 ms service budget as already documented. Images were linked, not booted. No HDL simulator was invoked in this round, so no new HDL execution or pinned-simulator result is claimed.

The exact-head check-run and workflow-run API snapshots returned zero records (`hosted-snapshot.json`, `hosted-checks.json`, `hosted-runs.json`). There is therefore no executed hosted-job success, skipped context, or aggregate hosted verdict claimed by this reviewer. Hosted/trusted local-replica acceptance remains manager-owned. A skipped physical job, if present in later evidence, must remain separate from executed proof.

Final integrity checks read and hashed all 1210 parent blobs, checked their modes and all 1215 index entries, and verified required submodule heads plus all tracked bytes/modes/index entries: gPTP `5dce647a`, PP `ead80360`, lwSRP `9197193e`, and verilog-axis `48ff7a7e`. The `external` gitlink was verified and remains uninitialized. lwSRP was initialized at its exact public pin for these tests. No tracked source bytes were edited; all added tests and plants were made in disposable scratch copies. `final-integrity.json` is authoritative for these checks. Foreground orchestrators joined their children; no review jobs remain running.

The manager must publish this packet, arrange fixes and corrected-head independent re-review of F1/F2 and affected lenses, complete hosted/local-replica acceptance, then build and validate the final candidate against live dev (assignment tip `291710b180ca9196780a6d17f2517957c9bcb89c`, distinct from source base `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`). Maintainer merge authorization, the remaining independent verdict/ledger, post-merge containment and issue/project completion remain pending. This review supplies no merge authorization.

`REPRODUCE.md` describes the portable scripts and expected return codes. Every publishable receipt and script is listed in `MANIFEST.sha256`; scratch is excluded. Logs retain executed diagnostics with local path prefixes normalized for publication; original and published hashes are recorded in `receipts/publication.json`. Construction attempts are disclosed but are not used as product-failure receipts.

R533-10 FINISHED
