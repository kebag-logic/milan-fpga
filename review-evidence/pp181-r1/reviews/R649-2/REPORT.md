[R649] POSITIVE - exact head c5afc0a42f200af01dd83e67b579dc3badc42601

Independent external review of issue #181 / PR #187, round R649-2. Exact tree: `90ca8e745ab0842df12e7a98b3f99e002c50bab6`. All five lenses are CLEAN. The prior receipt and occupancy-check findings are closed; the exact comment-traceability residue is applied. Three requested fault controls fail named in-tree checks in this reviewer's replay. No new BLOCKER, MAJOR or MINOR source finding remains. This is source-review approval, not merge-candidate or hardware acceptance.

Authority and reconstruction

The checkout and its searched ancestors contain no applicable AGENTS.md or CONTRIBUTING.md. The supplied workspace instructions and `docs/README.md` govern the review. Reconstruction followed repository guidance, then the [frozen issue and scope decisions](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/181), the [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/187#issuecomment-6249816230), and the [item-1 ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/181#issuecomment-6249065327), before the diff/history and executable evidence. Item 1 is “the cone no longer limits the shipping timing gate”; depth-halving is expressly superseded. No latency or protocol change is authorized.

Authorities examined: `docs/00_MILAN_COMPLIANCE_REVIEW.md:466` (REQ-NOT-001–005), `:541` (REQ-REU-001); `docs/architecture/02_interfaces.md:476` (F02.6 sticky event, first argument, coalescing and acknowledge); `03_packet_engine.md:224`; `06_aecp_engine.md:931` and `:998` (notification delivery and queue admission); `08_timing.md:155` and `:177` (response/service bounds and measured fan-out); `09_verification.md:307` (notification evidence); and the parent's published shipping recipe/resource-gate implementation at `7d79ffb2`. Specification clauses are the repository's cited Milan v1.2 §5.4.5 and IEEE 1722.1-2021 §7.5.2 interpretations; copyrighted specification texts were not independently authenticated.

The requested `08ae0013..c5afc0a4` diff and the incremental `42eb9aef..c5afc0a4` diff are preserved. The merge calculation for `42eb9aef` plus `08ae0013` reproduces `2cacc920`'s tree, `0e779022ea9b5c556d6a0f1207315f91a589d25b`. The two following commits are `a0a57895` (comment traceability) and `c5afc0a4` (checks). Both changed RTL modules differ from round 1 only in comments. Main's #176 engine, command/field tables, generator, checker, decode suite and top-level response tests are byte-identical at this head. The #181 diff changes no module port/parameter list, register map or top-level interface. Main's acceptance of exactly cdl 60/96 SET_STREAM_INFO, 2021-form responses and refusal cases therefore survives the merge alongside the timing cut. See `receipts/checkout-integrity.json`.

Evidence and execution

The public packet is fixed at [evidence commit 57275d0c](https://github.com/kebag-logic/milan-fpga/tree/57275d0ca1f124b4db8f6f4dab083cb2be204254/review-evidence/pp181-r1). I verified 301 selected round-2 files against both their Git blob identities and the published SHA256 manifest, then 54 additional historical-measurement/prior-mutant files against that manifest. The receipt index and HANDOFF distinguish `c5afc0a4`, base `08ae0013`, pre-commit development checks and historical `16c89c53` measurements. This is published-byte verification: the evidence commit metadata says **unsigned**, so no cryptographic signature verification is claimed. No separately signed attestation was supplied.

The round-2 proof source copies of both changed modules are byte-identical to HEAD. The receipt scripts, command files and result logs establish:

- Router equivalence at 1/5/8/16/29 sources: 91/205/286/505/859 points proven, zero unproven. The five faulty controls leave respectively 6/2/8/6/6 unproven points and return nonzero.
- Occupancy induction succeeds at 1x1, default shape and two-interface/identify shape. N1/N2/N3/N4/N6/N7 fail. N5 correctly passes this state invariant because it changes a reader; CQ1b/CQ2b detect it separately.
- Processor gates return zero at base and head. Published suite totals are 1,030,000 / 1,030,013, zero failing; the notification suite grows 67 to 80. Published head campaign totals include notification 109/109, D3 110/110, ACMP 51/51 and elaboration controls 160/160. The shared campaign records retain their results after source-line normalization. These are author executions, not reviewer reruns or manager source-bank results.

I replayed only the focused occupancy campaign, using the verified pinned simulator 5.050 and three concurrent mutation arms, capped at four compiler workers each. The unmutated three-build control passes **76 checks** (51 + 5 + 20). The four additional cancellation-run checks are covered by the published 80-check suite, not by this local `make run` control. All mutant builds succeed; each execution returns 2 through make, finishes its test tally, and fails the expected checks:

| Prior mutant / current arm | Reviewer-observed named failure |
|---|---|
| N4 / `occupancy_cleared_beside_push` | CQ1: 2 jobs instead of 3; OC1: 40 differing edges |
| N5 / `occupancy_not_busy` | CQ1b: 2 clocks low; CQ2b: 17 clocks low |
| N7 / `occupancy_pop_clears` | CQ2: 3 jobs instead of 26; OC1: 36 differing edges |

The public assignment attributes these N labels to R648-1. I matched the original published mutant diffs to the in-tree replacements; their effects are identical. `receipts/occupancy/results.json`, the four raw logs, campaign log/rc and `scripts/probe.sh` preserve this replay. None is a build-failure kill.

Physical receipt audit

The timing-query scripts select actual count/select cells, including register-enable endpoints, and log nonempty source/destination sets; “no path” is not an empty-name-query result. The OOC recipe is unchanged. These are the round-2 report figures:

| Measurement | 1x1 base | 1x1 head | 8x8 base | 8x8 head |
|---|---:|---:|---:|---:|
| count → select | 22 levels, −2.653 ns | no path | 33 levels, −8.930 ns | no path |
| count → occupancy | — | 3 levels, +7.716 ns | — | 2 levels, +7.909 ns |
| occupancy → select | — | 19 levels, −0.367 ns | — | 21 levels, −1.741 ns |
| overall OOC WNS | −4.819 ns | −4.819 ns | −10.720 ns | −5.844 ns |

The route chain records parent `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd`, the exact processor gitlink `c5afc0a42f200af01dd83e67b579dc3badc42601`, and application of #760's patch with SHA256 `003e49859d84a36189f0edb0ee629948dc9179cdeccda2d4549c91aeefeedf5b`. It records successful application, route and removal. The published route driver differs from its historical version only in a comment and SDK location; synthesis/implementation arguments and gate invocation are unchanged. Parent recipe and emitted implementation commands were spot-checked.

`route-head760/route-1x1-check.log`, `route.out`, route-status and cone reports agree: **WNS +0.220 ns; WHS +0.029 ns; gate rc 0, RESULT: PASS; complete routing with no unrouted net/error**. Resources are LUT 49,806; FF 52,406; SLICE 15,668; RAMB36 74; RAMB18 25; DSP 14. The worst setup path is inside `u_aecp`, micro-sequencer to `u_d3`, 34 levels. Count → select has no path; count → occupancy has 2 levels/+16.795 ns; occupancy → select has 22 levels/+3.510 ns. The result meets the +0.030 ns floor and the replacement ruling.

The historical OOC table was also checked against the newly public historical reports: base count-cone 22/32 levels, residual occupancy paths 22/22, and OOC WNS −5.416/−11.482/−6.045 ns. Historical routed +0.016 (failure), +0.181 and +0.144 ns (passes) are present in raw gate outputs. They remain historical results, not measurements of `c5afc0a4`. Extracts and the driver comparison are in `receipts/`.

Limits: I did not rerun physical implementation or the formal bank. Large formal logs are published as selected excerpts plus full-log hashes; the omitted full bytes were not authenticated here. #760's source head is explicitly “not pushed” in its public STOP comment and its commit API lookup returns 404. Consequently its inclusion is established by the published execution/composition receipt, not by an independent byte comparison of that unpublished parent patch. This does not replace the manager's final adoption reroute. The optional publication improvement below records this limit.

Prior findings: explicit dispositions

The independent delta verdict and ledger were written before reading the other reviewer's findings (`receipts/independent-verdict-before-prior-findings.md`). Public prior FINDINGS were read only after the independent diff pass. No current-round peer report or private material was read. The PR has no submitted or inline reviews in the captured API responses; the two round-1 conversation findings are reconciled here.

| Finding | Original severity and lenses | Disposition at this head; verification |
|---|---|---|
| R649-1-F1 (published as R649-F1) | MAJOR; Conformance, RTL, Tests, Docs | CLOSED. Its cause was missing public execution/measurement receipts. Commands, head index, OOC/routed reports, source/proof inputs, control results and gate logs now exist and were audited as above. Parent-patch replay limit is expressly retained. |
| R649-1-F2 (published as R649-F2) | RESIDUE; Docs | CLOSED. `KL_aecp_notify.sv:426` now says `(issue #181; REQ-NOT-001, REQ-NOT-002)`; `KL_pp_event_router.sv:110` says `(issue #181; REQ-REU-001, F02.6)`, exactly the requested substitutions. Published identifier/documentation gate passes. |
| R648-1-F-1 | MINOR; Tests, Docs | CLOSED by the same public receipt audit, including historical figures and the new exact-head measurements. |
| R648-1-F-2 | MINOR; Robustness, Tests | CLOSED. OC1 samples the two state values after each clock edge in every harness and closes every run, including early identify failure. CQ fills 16 waiting entries behind an active round, exercises push beside pop and ordered requester-excluding delivery. CQ1b/CQ2b isolate the busy term. Original N4/N5/N7 now fail named in-tree checks in published and reviewer executions. |
| R648-1-RES-1 | RESIDUE; Docs | CLOSED. The live PR's first paragraph contains the exact requested “Closes #181. Under … ruling …” replacement. Later Round 2 sections clearly identify the new measurements. |
| R648-1-S-1 | SUGGESTION; Docs | RETAINED below; unchanged introductory router wording. |
| R648-1-S-2 | SUGGESTION; Tests, Docs | RETAINED below; unchanged idle-output test limitation and historical table wording. |

Retained and additional suggestions

**R648-1-S-1 — SUGGESTION — Docs.** Artifact: `hdl/packet_engine/KL_pp_event_router.sv:104`. Evidence/authority: the opening scan sentence says “delivered”, while the implementation and immediately following paragraph use the presented event under F02.6. Impact: the first sentence alone is imprecise; the full comment explains the behavior correctly. Optional outcome: replace it with “Grant from the REGISTERED pending set minus the presented event (it leaves on its delivery); base = one past the presented source (or the idle pointer).” Verification: comment-only inspection against `valid_r`, `pend_after_w`, `base_w` and the unchanged load enable.

**R648-1-S-2 — SUGGESTION — Tests, Docs.** Artifacts: router `sel_next_w` at `hdl/packet_engine/KL_pp_event_router.sv:147`, the published R5 equivalence log, `tb/event_router`, and `syn/ooc/README.md:261`. Evidence: clearing select when no grant is found is caught by the equivalence proof; the existing suite does not pin idle source/payload outputs. Their validity-qualified contract does not establish a new obligation here. Optional outcome: if idle values are intended contractual outputs, add an in-tree check and require R5 to fail it. Separately replace “Worst path from `cmdq_count_r`” with “Worst (least-slack) path from `cmdq_count_r`”; this explains why that row can have fewer levels than the next row. Verification: intended idle contract plus a named R5 failure, or the wording-only table edit with unchanged figures.

**R649-2-S1 — SUGGESTION — Tests, Docs.** Artifacts: `author-r2/receipts-r2/RECEIPTS.md` identities, `route-head760/chain.txt`, and public #760 STOP comment 6241681577. Evidence: the parent perturbation is identified by an unpublished commit and patch digest; the commit lookup returns 404 and no standalone #760 patch was found in the packet inventory. Impact: the route figures can be audited from published reports, but an outside reader cannot independently reconstruct that parent perturbation from its commit today. Optional outcome: publish the exact already-recorded patch beside the route receipt, or make the immutable source commit available. Verification: its diff bytes hash to `003e49859d84a36189f0edb0ee629948dc9179cdeccda2d4549c91aeefeedf5b` and apply to the recorded parent. No change to the measured result or source verdict is requested.

Independent lens conclusions and ledger

Conformance: notification class/content, requester exclusion and per-controller sequence rules remain unchanged; CQ's independent expected-job sequence grades them under backlog. F02.6 holding/coalescing semantics remain unchanged. No added clock latency is introduced, so existing service bounds and round-1 measured timing coverage carry forward. The accepted shipping-cone criterion is met by the published physical receipt.

RTL: reset clears count and flag; accepted push sets the flag; pop without push uses pre-edge count != 1; accepted simultaneous push/pop holds count and retains the push's set flag. At full count, rejected push does not suppress a valid pop. Router speculative scan is equivalent whenever loaded: on delivery valid equals deliver, and from idle both are zero; under backpressure its result is unused. Empty-grant select holds. Formal receipt controls cover these distinctions. Main's imported engine logic is unmodified by the cut.

Robustness: new CQ/OC directly cover backlog, full queue, simultaneous push/pop and busy between rounds. Reset-set controls exercise all five run endings. Unchanged round-1 full/overflow/reset/refill, held-router, saturation, fairness and conservation coverage keeps its prior CLEAN verdict; no affected dependency invalidates it. The exact-head published integration and guard campaigns cover the merged engine dependency.

Tests: monitor sampling is after evaluation of each rising edge, mismatch counting is conditional on inequality, and test completion requires OC1. All three builds receive `occupancy.vlt`. Every new check has a named planted failure; the independent control and three requested mutations confirm the key closure. Source reading is used only to expose the two state values; emitted jobs and busy are graded independently. Published and reviewer executions remain clearly separated.

Docs: the architecture and bench records describe the implemented occupancy invariant, queue sequence and gate coverage; requirement IDs are repaired. Historical synthesis figures are not relabeled as current measurements. No new prohibited review/lane identifier was found in source comments; CQ/OC are test-section names. The retained wording suggestions do not alter a measurement, test or conformance claim.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/ruling; REQ-NOT-001–005; F02.6; CQ expected jobs; merged #176 identity; routed gate | R649-2; unchanged service coverage from R649-1 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| RTL | CLEAN | Queue writers/readers; full router; merge-tree/inherited files; exact proof inputs/results; OOC/routed queries | R649-2; unchanged logic from R649-1 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Robustness | CLEAN | CQ/OC and all harness exits; N4/N5/N7 replay; public N1–N7/reset controls; inherited boundary probes | R649-2 delta plus R649-1 unaffected coverage | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Tests | CLEAN | Bench/Makefile/config/mutant driver; local 76-check control and three kills; published 80-check suite, gates/campaigns/proofs | R649-2 | c5afc0a42f200af01dd83e67b579dc3badc42601 |
| Docs | CLEAN | docs/README; architecture 02/03/06/08/09; OOC table; comments; live PR; head-indexed public receipts | R649-2; historical figures checked separately | c5afc0a42f200af01dd83e67b579dc3badc42601 |

Limits and pending manager duties

The author's parent consumer results are **not all rc 0**. At both base and head, `check_submodule_docs`, `measure_test_evidence` and its self-test return 1. Logs show the staged gitlink's stale documented pin/diagram and three pre-existing source-reader dispositions missing in the parent (`tb/aecp_cmds/mutants.py`, `tb/elab_guards/guards.py`, `tb/elab_guards/mutants.py`). The tables and causes match; this is inherited adoption work, not an unreported processor regression. The literal all-zero parent completion bar is still pending, not waived by this review.

At the captured exact-head hosted snapshot, runs 39146743313 and 39146740703 have successful completed documentation and portability jobs; suites remain in progress. The cached compiler-build setup step is skipped. It is not an executed validation job, and no completed hosted bank is inferred. Metadata is preserved under `public/hosted-*`.

There is **no manager source bank at this exact head**. The manager owns hosted/act acceptance and the final current-dev candidate builder/native banks at the merge turn, source base `08ae0013`, live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`, and publication of those receipts. It also owns parent consumer closure and remeasurement on the adopted image under the item-1 ruling. Two independent positive reviews and the remaining completion bar still govern merge. Physical calibration is **NOT RUN**; field skips and simulation are not hardware proof.

No full bank, physical implementation, hardware operation, source fix, commit, push, merge, contact or GitHub write was performed. Commands ran in foreground sessions; the focused driver's worker children were joined before return. All disposable trees stayed under this packet's excluded `scratch/`. The exact head/tree, all **633 tracked blob bytes and modes**, and the index are verified; status is clean. This processor checkout has **no submodule gitlinks**. The parent receipt's staged gitlink names the exact reviewed head. No source restoration was necessary because probes used copies.

`MANIFEST.sha256` lists every publishable receipt and script with packet-relative paths; `scratch/` is excluded. The report and ledger supersede the initial placeholder.

R649-2 FINISHED
