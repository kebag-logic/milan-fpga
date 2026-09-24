# [A253] GET_STREAM_INFO internal selectors

Status: implementation committed; all processor CI gates and the CI-pinned mutation run pass. Parent source-list and consumer simulation pass in the designated checkout. Its three pin-guarded commands still refuse the unchanged parent index. All five commands pass in an isolated copy of the identical parent tree with the candidate gitlink staged, without touching the designated parent's index.

Branch: `43-49-gsi-internal`
Base: `939c143333d11e2378a514f1c7b6abd4c3259bfd`
Head: `5771578784c77e945980c78faa52f3e54bcf5e2d`. Two local commits, each a one-line subject with no body/trailers: 0452c492 implements the lane; 57715787 adds the mutant runner's required type annotations. Production RTL, docs and C++ tests are unchanged by the second commit; processor/synthesis evidence therefore covers identical final source bytes.

Authority: [#43](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43), [#49](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/49), [decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5813138046), [parent #508](https://github.com/kebag-logic/milan-fpga/issues/508).

Read both issues and the decision, parent #508, Milan v1.2 §§5.3.8.6, 5.3.8.8, 5.4.5.2/Table 5.22, F02.10/F06.13, the gather/microcode path, SRP listener/talker failure records and ACMP listener commits. No AGENTS.md or CONTRIBUTING.md exists in the processor tree. Applied the supplied RTK instructions, hdl/README.md, docs/README.md, docs/guides/hdl-engineer.md, and parent AGENTS.md/CONTRIBUTING.md. No private transcripts consulted.

## Result and interface

Input selectors 5 and 7 are answered inside protocol_processor_top, with no external request; external wait/data are ignored for them. Selector 4 still asks for the destination MAC but replaces the failure-code byte internally. Other words and validity flags retain existing ownership. No new top-level parameter, port, or parent instantiation connection.

The failure pair and probing byte are sampled together when selector 0 is accepted and held through the gather. An eight-bit per-sink view copies committed listener record writes, with no independent state transitions. Changed committed status and changed registered FailureInformation trigger the existing notification path. A missing descriptor returns the full zero body without consulting live state.

Protocol clarification: the assignment's “PASSIVE after bind” is tested after the actual no-talker timeout/backoff. A new BIND_RX starts ACTIVE (Milan 5.5.3.5.3); unanswered probes and backoff with no discovered talker lead to PASSIVE (5.5.3.5.29). The existing state machine is preserved and both transitions are graded.

## Field lineage

Offsets start at the AECPDU; Ethernet offsets include its 14-byte header.

| State owner → published view | Selector → field | Response byte | Notification |
| --- | --- | --- | --- |
| SRP listener fcode_r[sink], gated by FAILED → KL_srp_top.snk_fail_code_o | 4, bits 15:8 | AECPDU 58 / Ethernet 72 | registration, changed failure, replacement, withdrawal |
| SRP listener fsysid_r[sink], gated by FAILED → KL_srp_top.snk_fail_bridge_o | 5, full 64 bits | AECPDU 60..67 / Ethernet 74..81 | same as code |
| KL_pp_acmp_listener committed acmp_rec_t.pbsta → record write bus → status view | 7, bits 31:29 | AECPDU 76 bits 7:5 / Ethernet 90 | changed committed status |
| KL_pp_acmp_listener committed acmp_rec_t.acmpsta → same write bus/view | 7, bits 28:24 | AECPDU 76 bits 4:0 / Ethernet 90 | changed committed status |

Ownership is documented in F02.10/F06.13, linked from the integration guide. SRP failure-refresh event semantics are documented in section 10.

## Response tests

Retained test: tb/pp_top/gsi_internal.hpp, run by `make -C tb/pp_top gsi-internal` and normal pp_top. Eight hardware sinks; two descriptor-backed sinks. Values originate in wire-driven ADP/ACMP/MSRP and real timer expiry, never record pokes/status injection.

| Named scenario | Proof | Result |
| --- | --- | --- |
| GI RESET / RESET-LIVE | Both sinks zero, including reset from COMPLETED/Failed | PASS, solicited (reset clears controller registration) |
| GI BIND-ACTIVE / BIND-TIMEOUT / PASSIVE | Actual bind sequence, exact second probe, PASSIVE with acmpsta zero | PASS, solicited + unsolicited |
| GI ACTIVE / TIMEOUT / RETRY-CLEAR | Discovery, double timeout → ACTIVE/acmpsta 7, next probe clears status | PASS, solicited + unsolicited |
| GI COMPLETED / DISABLED | Successful real probe response settles; unbind disables; acmpsta zero outside ACTIVE | PASS, solicited + unsolicited |
| GI FAILED-0 / FAILED-1 / DISTINCT-0/1 | Sink 0 code 7 / B17D23456789ABCD; sink 1 code 11 / 9EAF1029384756C2; full-width correct-sink values | PASS |
| GI FAILED-REFRESH / unchanged Failed | Changed code/upper bridge bits notify; identical refresh silent | PASS |
| GI ADVERTISE / WITHDRAWAL / WITHDRAWAL-PROBING | Failure pair clears on replacement/withdrawal; SRP and probing events observed | PASS, solicited + unsolicited |
| GI MISSING / MISSING-UNBIND | Hardware sink 2 ACTIVE but absent from image: NO_SUCH_DESCRIPTOR, zero body | PASS, solicited + unsolicited |
| GI repeat bind / final / internal seam | No fabricated transition/duplicate; poisoned/stalled old selector path never requested | PASS |

Focused golden/restored runs: **416 checks, zero failures** each, in mutants-pinned/golden-run.log and mutants-pinned/restored-run.log. All 94 response bytes are compared, including status, index, sequence, u bit, unrelated external words and reserved bytes.

Legacy fixtures explicitly retire an earlier service-only listener, wait for the absent peer to become PASSIVE before registry checks, and refresh source address freshness with real probes before streaming-output checks. Newly observable status changes are isolated from unrelated notification counts; production timers and response checks are not disabled.

## Mutants

Retained runner: `python3 tb/pp_top/gsi_mutants.py --output <artifact-directory>`. It uses a temporary source copy, requires compilation success and a completed failing simulation with the named check, restores after each mutation, and runs golden/restored controls.

| Mutation | Required failing check | Build rc | Run rc |
| --- | --- | --- | --- |
| failure-code-zero | GI FAILED-0 solicited: failure code | 0 | 1 |
| failure-bridge-zero | GI FAILED-0 solicited: full failure bridge | 0 | 1 |
| pbsta-zero | GI PASSIVE solicited: pbsta | 0 | 1 |
| acmpsta-zero | GI TIMEOUT solicited: acmpsta | 0 | 1 |
| wrong-sink | GI DISTINCT-0 solicited: full failure bridge | 0 | 1 |
| integrator-path | GI internal seam: selectors 5/7 never requested | 0 | 1 |
| missing-descriptor-leak | GI MISSING solicited: pbsta | 0 | 1 |
| status-notification-zero | GI PASSIVE unsolicited: complete Milan response | 0 | 1 |
| golden / restored | 416 checks, zero failures each | 0 | 0 |

Runner rc 0; all eight detected. Evidence: mutants-pinned/results.json and per-variant logs. All eight mutants and both controls also pass the required verdicts with workflow-pinned Verilator 5.050 (mutants-pinned.log, runner rc 0). The earlier 5.052 run remains under mutants/. Tools are outside this output directory.

## Processor gates

Commands run foreground; statuses captured directly without piping gates. Full commands/durations: gates.jsonl. Earlier failed development runs remain as history and are not counted as passing evidence.

| Gate | rc | Evidence |
| --- | --- | --- |
| make check (docs lint, links, matrices, wavedrom, staleness) | 0 | docs-check.log: 41 mermaid, 18 wavedrom, 840 links, 115 REQ rows, 92 module rows, zero untested |
| ./scripts/lint_hdl.sh, pinned 5.050 | 0 | lint-pinned.log |
| ./scripts/run_suites.sh, pinned 5.050 | 0 | full-suites.log: 16,317 checks, zero failures; pp_top 1,876 checks |
| git fetch --no-tags origin refs/pull/13/head | 0 | completed before figure gate |
| make -C tb/nvm_port figures, pinned 5.050 | 0 | nvm-figures.log: all measured figures agree |
| ./syn/yosys/run.sh | 0 | yosys.log, all tops plus six-RAMB36 engine guard |
| Full-processor OOC baseline / candidate | 0 / 0 | area-base.log / area-candidate.log and report directories |
| gsi_mutants.py, pinned 5.050 | 0 | mutants-pinned.log / mutants-pinned/results.json |
| Unchanged top declaration / git diff --check | 0 / 0 | interface.log / whitespace.log |

Pinned tool build initially lacked help2man; after installing the prerequisite, 5.050 installation completed rc 0 (ci-toolchain-install.log). No toolchain, SDK, or virtual environment is stored in this output directory.

## Area delta

Same syn/ooc/protocol_processor_ooc.tcl recipe, default eight-input/eight-output shape, xc7a100tfgg484-2, 10 ns constraint, Vivado 2026.1. Baseline is the assigned base in an isolated detached checkout; candidate contains final production RTL. Synthesis estimates only, not routed timing or hardware results.

| Resource | Base | Candidate | Delta |
| --- | ---: | ---: | ---: |
| Slice LUTs | 28,092 | 28,732 | +640 (+2.28%) |
| LUT as logic | 26,886 | 27,526 | +640 |
| LUT as memory | 1,206 | 1,206 | 0 |
| Slice registers | 30,354 | 31,138 | +784 (+2.58%) |
| Block RAM tiles | 24 | 24 | 0 |

Both have 23 RAMB36 and two RAMB18. Internal bridge use retains previously unused per-sink bridge state; the status view and sample add state and selection logic. Reports: area-{base,candidate}/util.rpt, util_hier.rpt, timing.rpt, vivado.log.

## Parent consumer gates

Checkout: $LANES/pp94-parent-consumer. Initial parent working tree clean; processor gitlink and checkout both 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f.

| Gate | rc | Evidence |
| --- | --- | --- |
| Prescribed fetch + detached candidate checkout | 0 | parent-checkout-final.log |
| python3 scripts/check_cpp_idiom.py | 2 (pin mismatch) | parent-cpp-final.log |
| python3 scripts/check_py_idiom.py | 2 (pin mismatch) | parent-python-final.log |
| python3 scripts/xvlog_gate.py --check | 2 (pin mismatch) | parent-xvlog-final.log |
| python3 scripts/check_rtl_source_lists.py | 0 | parent-source-lists-final.log: 106 files, 4/4 consumer lists complete |
| make -C tb/verilator/pp_shadow -j8 | 0 | parent-shadow-final.log: 371 checks, zero failures |

The C++, Python and xvlog gates require the parent index gitlink to equal checkout HEAD (xvlog authority: scripts/xvlog_gate.py, _index_pin / tree_state). A detached checkout alone cannot meet that guard. A temporary index exception was requested, but no permission has been received and the designated parent's index has NOT changed. The three rc 2 entries above are real setup refusals, not passing checks.

Independent reproduction uses $VALIDATION_STORAGE/pp43-a253-parent-validation, a local clone of the identical parent HEAD 3eaee03f0c50522c4e4da8e12c771ec130a8c2f9. Only the candidate processor gitlink is staged in that disposable copy. There is no parent commit or push. parent-integrity.log proves matching parent HEAD/content, the original index unchanged, clean processor checkouts at the final head, and no author-lane dirt.

| Same-parent-tree isolated check at final head | rc | Evidence |
| --- | --- | --- |
| check_cpp_idiom.py | 0 | parent-isolated-cpp-final.log |
| check_py_idiom.py | 0 | parent-isolated-python-final.log |
| xvlog_gate.py --check | 0 | parent-isolated-xvlog-final.log: four existing banked findings, no new findings |
| check_rtl_source_lists.py | 0 | parent-isolated-source-lists-final.log |
| make -C tb/verilator/pp_shadow -j8 | 0 | parent-isolated-shadow-final.log: 371 checks, zero failures |

The isolated Python gate first exposed four missing annotations in the new runner. The second processor commit fixes them; the final gate reports zero unannotated public functions. The final-head HDL run passes with four existing banked findings and no new findings.

This reproduction does not turn the designated checkout's rc 2 refusals into rc 0. Requiring all five commands to pass in that exact checkout requires authorizing its indexed gitlink update, which conflicts with the original checkout-only restriction.

## Final head and review notification

Head is committed and processor gates pass. The designated parent index remains unchanged. The isolated consumer results are additional evidence, with the exact-checkout limitation recorded above. PR-BODY.md is the completed review description. No push, PR operations, parent commits, sub-agents, or hardware work.

Review notification posted on issue #43 with final head and the explicit exact-checkout limitation: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5813813612
