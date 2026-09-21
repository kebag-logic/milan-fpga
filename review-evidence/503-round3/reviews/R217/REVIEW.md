[R217] NEGATIVE - exact head ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4

Independent internal contract review of PR #503 / issue #500, round **R217-r3**. Assigned lenses applied: **RTL first, then Conformance and Robustness**. All were previously open. Tests and Docs were also applied to the executable evidence and claims implicated below. This review concerns the Proposed contract, with no product implementation, silicon, release or merge authorization implied.

The corrected transport-error classification, descriptor failure handling and binding-read deadline address substantial round-two defects. One MAJOR remains: listener preload can indefinitely retain restore ownership and prevent command service, contrary to the proposal's unconditional bounded-recovery claim. Its disclosure as a model omission does not resolve that claim. No assigned lens is clean.

**Authority and provenance.** Reconstructed the task from [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), issue #70, REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, the accepted SAVED_STATE_SNAPSHOT_OWNERSHIP and SAVED_STATE_FASTCONNECT contracts, and the pinned processor's F07.8/F07.9 and concrete interfaces. Read both round-two reviews ([R217](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5265143219), [R218](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5265158417)) and their [verbatim reports, fault sources and observations](https://github.com/kebag-logic/milan-fpga/tree/7d9da8773c8baec0f705b08cea8b9e04d8c00b27/review-evidence/503-round2). Read the [corrected response and published integration receipts](https://github.com/kebag-logic/milan-fpga/tree/d5899ee6aa9194dfe786777c7092074c10fffd8a/review-evidence/503-round3/author), the [integration decision](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758659924), and the [final manager REVIEW READY](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5760377435). Also examined open #501/#502 and the relevant public processor issues, including #15's undelivered recovery criterion. No private handoff, transcript, author checkout or private management receipt was used.

Page references mean `docs/design/SAVED_STATE_MATERIALIZATION.md` at the exact head above. `E/` means `design-evidence/500-materialization/proposal-evidence/`; `T/` means its sibling `tickets/`. Both refer to public immutable commit [fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293](https://github.com/kebag-logic/milan-fpga/tree/fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293/design-evidence/500-materialization), fetched into an independent disposable checkout. These are the revised tickets linked by the current page, not their earlier versions.

The page checkout was initially clean. Initial and completion checks found remote PR head `ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4`, remote `dev` `2d8fd62fd986ea2d6a87d284e144f023034c0944`, and evidence branch `fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293`. The supplied live base is an ancestor of the candidate. The candidate changes four documentation files only. Initialized pins in both checkouts are processor `424c688fa2205b934a7689a58f2aa766420f2326`, gPTP `c1b617435824929a790739ea8585c3fe1a328cc0`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`; the unused external pin remains uninitialized at `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`.

Independently verified all 59 immutable digests and all four integrated documentation blobs. The blobs equal the published pre-integration page `e67a586f92506c8623079c341e4f56a9c5ae165a`. Of 15 examined repository inputs, only `scripts/nvm_shape.py` differs at the integrated candidate: comments only, with equal parsed Python ASTs. The other inputs match byte-for-byte. The executable receipt names ancestor `bf88b71f22d225ac3671317ab6cc720c41c76d4e`; subsequent evidence commits add receipt prose only. Thus the inspected historical measurements have traceable inputs, but are not fresh integrated measurements. Direct Git blob checks also found no tracked-byte differences in either checkout or its initialized submodules.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:1432 - R3-F1: Unbounded listener preload still defeats the promised command-recovery bound

Requirement/evidence: This continues the availability part of **R217 R2-F3**, preserving its severity and all five lens labels. Accepted `SAVED_STATE_FASTCONNECT.md:1122` requires continued AECP/SET service when persistence wedges. The proposal goes further: page line 248 says every restore wait of both walks is bounded; line 1432 bounds pre-terminal command waiting by the two deadlines plus the walks; section 15 item 13 repeats that claim. Reset-owned dispatch prevents any AECP program until the binding walk and D3 restore reach their terminal.

The proposed S3 timer watches only `H_RS_REQ` and `H_RS_STREAM` (`E/prototype/KL_acmp_nvm_shadow.amended.proto.sv:491`). `H_RP_DRIVE` at line 771 advances only on `pre_ready_i` or a live touch. It has no deadline or alternative exit. The pinned listener's `pre_ready_o` (`protocol-processor/hdl/acmp/KL_pp_acmp_listener.sv:484`) is deasserted by pending START/STOP work, transactions, timer work or talker events; preloading has lower priority. No proposed integration prerequisite establishes a bound on that interference. T8 explicitly leaves preload unwatched. The page acknowledges this at lines 1205, 1534 and 1679, while retaining the unconditional recovery claims.

The immutable harness hides this transition: `E/harness/d3_top.sv:554` ties `pre_ready_i` high, and line 582 reports every `pre_valid` as taken. W13 and B01 therefore establish bounded binding **reads**, not the whole walk. Their successful verdicts do not cover preload arbitration.

Independent reproduction connected the amended manager to the **unchanged pinned listener**, using that repository's existing preload-backpressure lever (`protocol-processor/tb/acmp_nvm/acmp_nvm_wrap.sv:211`): a continuously presented droppable talker event, sink `0xffff`, has priority while leaving the restored sink untouched. Only a scratch harness and scenarios changed; all writer/arbiter/port/binding/descriptor RTL and firmware remained unchanged. The seed was V1a's saved 1x1 slots. This is an interface-level scheduling counterexample, not a claim that a particular conforming network packet stream was reproduced. The proposal needs either an enforceable integration assumption excluding this interference or a bounded handling mechanism.

| Listener stimulus | Binding / D3 terminal | Entity and command result |
|---|---|---|
| Ready control | Binding 177; D3 7605; preload 174 | Enable 7613; GET returns offset 1500000, valid 1 |
| Backpressure held throughout observation | Neither terminal; neither failure nor CLOSED; port idle; ownership stays asserted | Entity disabled; firmware requests enable at 3000074; subsequent GET waits 2000068 cycles and produces no answer |
| Same interference released at cycle 100000 | Preload 100000; binding 100003; D3 107431 | Enable 107438; GET returns the saved value and valid bit |

The finite case demonstrates that recovery follows the arbitrarily chosen preload release, not either 20000-cycle deadline. The held case is consistent with the RTL's absent exit: keeping readiness low and the sink untouched can hold that state indefinitely. The persistence device is healthy and the port is idle, so quarantine of an unresponsive device does not explain this hold. All three processes exited zero and completed their scenarios; the held scenario nevertheless violates the claimed property. [Reviewer source, observations and assertion checker](REVIEW-evidence/README.md) accompany this report.

Impact: The proposed integration can hold the entity and every queued AECP command indefinitely without a failure terminal. The contract has not settled ownership and recovery for the last phase of a mandatory dependency. An on-chip handshake is not itself a latency bound, and listing this omission does not close R2-F3.

Required change: Settle the preload scheduling/recovery contract at the first affected stage. Either prove and enforce bounded listener acceptance through concrete ownership/arbitration prerequisites, or specify bounded failure and safe recovery of the entire binding preload phase. Account for failure after earlier sinks have been applied and for late preload/discovery effects before releasing commands. Align the page, T1/T4/T8 and executable evidence. Do not simply release untagged ownership on a timer, assume partial bindings are defaults, or waive FASTCONNECT 9.3. If changing an accepted requirement is necessary, obtain its explicit reconciliation before declaring conformance.

Verification: Use the actual listener readiness path. Exercise finite and persistent interference, higher-priority work, first and later sink preloads, acceptance immediately around the chosen boundary, and no late preload/discovery action after a recovery terminal. Demonstrate bounded manager recovery and usable GET/SET service under the declared conditions. A discriminating mutant must break that bound or containment. Include any added integration mechanism in the cost accounting; do not infer whole-walk coverage from a read-timeout mutant.

**Round-two dispositions at this exact page head.** “Resolved for the proposal” below means the contract now specifies a concrete prerequisite and its prototype demonstrates the stated mechanism. It does not mean the pinned product was fixed or an implementation ticket is complete.

| Prior finding | Original severity and all lenses | R217-r3 disposition and evidence |
|---|---|---|
| R217 R2-F1 / R218 F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | RESOLVED for the proposal. S1 distinguishes DEVICE/short-header failures from completed UNFRAMED headers; genuine blank controls remain successful. The D3 passes compare record identities as well as propagating errors, so neither recurring header errors nor balanced losses become absence. H1-H8, V18/V18b/V18c and selected C01-C03/X01-X02 mutants reproduce the distinctions. T8 is a prerequisite from stage 1. The pinned port is still unamended. |
| R217 R2-F2 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED for the proposal. Descriptor errors and the store's 4096-cycle timeout after prior application now abort with cause 6; failed initial/default-image proof reaches CLOSED with cause 7. S2 retains response debt across local resets, blocks a new request until the old burst terminates, and requires proved defaults before enable. V20-V23, V17, selected DF01-DF03/IMG01/DG01-DG02, and the independent adjacent timing probes below support this. T9 is a stage-1 prerequisite. |
| R217 R2-F3 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | PARTLY CORRECTED, OPEN as R3-F1. S3 bounds silent binding reads; W13/W13b/W13c/W15/W16 and B01-B04 exercise failure, late-response drain and command recovery. T8 no longer promises timer-based reuse of an untagged port. Whole-walk/dispatch availability is still not established because preload can wait indefinitely. |
| R218 F6 | MINOR; Tests, Docs | Correction independently corroborated. Synthetic narrowed-output ordering cases are labelled. V1s_a/V1s_b check a product-legal output value AND valid bit through save/replay using the shipping format judge; V1s_c refuses unsupported narrower output. RPL_fmto and TRG_fmto are discriminating. This does not make the synthetic cases product-legal. External disposition belongs to that reviewer. |
| R218 F7 | MINOR; Docs | Ticket contradiction corrected: T8 distinguishes manager/command recovery from persistence-port reuse, permits permanent quarantine for a device that never terminates, and explicitly leaves processor issue #15 criterion 2 undelivered and unamended. This correction does not close R217 R2-F3 or issue #15. External disposition belongs to that reviewer. |

The independent descriptor probes extended the named cases to adjacent transitions. A 4094-cycle delayed response completed normally. Delays 4095, 4096 and 4097 caused failure 6, rollback and enable only after defaults, with the recovered offset value/valid both zero. Delays 24090, 24098 and 24100 left the burst terminal outstanding at the rollback deadline: CLOSED remained asserted, ownership retained, no enable or GET answer. A first returned beat before the deadline did not falsely discharge the whole burst debt. These are focused safety observations, not a complete CDC/reset proof. The disclosed descriptor-store watchdog re-arm limitation remains a truthful dependency error; it is not treated as valid data or claimed fixed by this review.

**Earlier corrections retained, with original severities and labels.** Both round-two reports were reconstructed before assessing these dispositions; no round-one lens is banked.

| Prior finding | Original severity and all lenses | Current disposition |
|---|---|---|
| R217 F1 / R218 F1, round one | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | Original payload partial-restore triggers remain corrected by pass-zero validation and whole-D3 rollback. V11b-V18 and M13 retain discriminating controls. The later header/descriptor generalizations are addressed as R2-F1/R2-F2 above. |
| R217 F2 / R218 F2, round one | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each | Original unsafe early-enable triggers remain corrected: reset ownership, terminal-gated enable and drains contain late responses. The broader availability part remains OPEN under R3-F1. |
| R217 F3 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | Padding-alias defect remains RESOLVED for the proposal: V3a-V3g distinguish complete eight-byte padding, holes, malformed tails, invalid indices and a valid empty map; P01/P02 are detected. |
| R217 F4 | MAJOR; Conformance, RTL, Robustness, Docs | Stage-prerequisite defect remains RESOLVED. Stage 3 is gated on a conforming #501 capacity decision; every shippable stage is gated on #502. Neither underlying defect is resolved. K16 remains containment-only. |
| R217 F5 | MINOR; Tests, Docs | Process-verdict defect remains RESOLVED. The eight CLI controls enforce required nonzero exits and diagnostics; a crash/incomplete case does not count as a kill, and a surviving mutant makes the verdict fail. |
| R218 F3 | MAJOR; Tests, Docs | Same process-verdict correction independently corroborated, including the crash and partial-kill controls. External disposition remains that reviewer's. |
| R218 F4 | MAJOR; Conformance, Tests, Docs | Group-specific trigger/replay checks, configuration valid state and synthetic-rate labelling remain present. All nine trigger/replay deletion definitions and published diagnostics were inspected; cfg/rate/output controls were included in the fresh selection. Output-format legality is qualified as described for R218 F6. |
| R218 F5 | MAJOR; Conformance, Robustness, Tests, Docs | Same #501/#502 stage restrictions independently verified. No underlying defect or external review is closed by this report. |

**Whole-contract assessment beyond the counterexample.** O1 remains the sole sequential control-face master for strobes/base/length/map tables. D3 introduces no competing O1 master. O3 separately orders binding restore, D3 restore and materialization at the device face. The arbiter gives binding priority at an idle tie, includes the D3 grant cycle in binding busy, and retains the selected owner through completion or drain. The pinned modules, amended port/binding prototypes, firmware substitutions and parent glue are distinguished; the amended prototypes are evidence of PROPOSED seams, not unchanged product interfaces.

Clear/taint has meaningful record identity. A new change during a write taints the captured value; retries latch afresh; a change on the completion edge wins over clear; an unrelated record cannot clear the target's pending bit. Pending transfers to backend dirty before the producer acknowledgement can hide the work. Give-up is not success: the sticky alarm revokes the durability claim. K1-K19, M01/M03/M05 and the inspected arbitration mutants support repeated writes, multiword names, interleavings and power cuts before/after logical completion and physical acknowledgement. Inherited snapshot epoch/identity and O2/O4 rules still apply; this review does not re-prove the physical A/B machinery.

Record allocation and framing were checked against FASTCONNECT 4.2 and processor F07.8/F07.9: one group/index record, big-endian framing, explicit payload lengths and record identity, no alternative namespace hidden in the writer. The prototype has 49 D3 record positions at 1x1 and 145 at 8x8; those are not a claim that every shipping output map fits its payload. #501 remains a real capacity gap, including the 8x8 fan-out case. #502 remains a real pending-status mark-tail gap. The explicit stage gates honestly prevent these gaps being waived; filing the issues did not repair them. T8/T9 are proposed ticket contracts to be filed after contract acceptance and before implementation, not already implemented prerequisites.

The persistent set retains all nine groups: configuration, rate, clock source, both format directions, presentation offset, both map directions, and names. Selectors and lengths were traced to the actual dynamic/descriptor faces; configuration 0 has a separate valid bit, empty names remain values, and format/map coupling can revert a refused pair to proved defaults. Synthetic rate choices do not imply a shipped multi-rate configuration. Binding owns saved started state; the retired selector is not another persistent owner. Identify, lock and registration state are excluded; structural exclusions are not passed off as exhaustive volatile-state tests. Reserved SUID/MCR positions have no invented producer. The synthetic atomic map edit/default model is explicitly narrower than the real phase-0-through-5 map interface and its empty reset state.

The live-write trigger is an explicit **proposed normative amendment**. I accept its technical direction for materializing the accepted live group/index state and avoiding ambiguous or missing marks, subject to the stated proposal/adoption boundary. I do not silently reinterpret existing mark-based requirements. Before implementation adoption, the accepted FASTCONNECT mark contract, SNAPSHOT_OWNERSHIP D2, processor F07.9 and affected issue criteria must be reconciled through a recorded decision and consistent updates. Restore writes must not trigger new dirty work, volatile writes must remain excluded, and accepted live changes must retain truthful pending/durability status. This assessment is not acceptance of the whole page while R3-F1 is open.

Restore dependency analysis included descriptor image proof, legality lookups, dynamic state, names, both maps, output-format judgment, binding preloads and port completion. S1 reports a cause at the actual terminal; S2 accounts for an accepted burst until last/error, rather than assuming a local owner reset erases an external response. Its hard-reset domain and placement relative to the actual descriptor bridge/CDC remain implementation prerequisites. Failed proof cannot enable the entity; transport failures are distinct from well-read invalid values. Existing response-debt containment is coherent in the examined prototype; preload scheduling is the missing dependency identified above.

**Cost and model limits.** Inspected the committed OOC recipe, proxy definitions, calibration and measurement rows for both shapes. Writer plus arbiter costs are 2377 LUT / 888 FF at 1x1 and 3116 / 1109 at 8x8. The proposed additional seams are included: port +4 LUT / 2 FF; binding +107 / 34 at 1x1 and +103 / 34 at 8x8; descriptor guard +5 / 1. Their arithmetic totals are 2493 LUT / 925 FF and 3228 / 1146, with zero additional BRAM/DSP in those measured cells. These are differences/sums of OOC syntheses, not integrated upper bounds, placed timing, board latency or silicon proof. The alternative area proxies do not include all firmware/integration costs. The older backend table/calibration difference is disclosed rather than silently substituted.

The executable model uses a single clock, accelerated firmware timing and synthetic interfaces; two firmware substitutions execute, while the all-boot-path substitution remains a derived implementation obligation. Map-phase timing, real memory timing and preload arbitration are not integrated by the baseline harness. Shipping output-format tests are distinct from its synthetic ordering campaign. Honest qualification supports using these measurements for design comparison; it does not establish the unqualified whole-walk bound.

**Commands and fresh results.** All builds/runs were synchronous, on CPU set 64-79, with at most eight build jobs. `D3_OUT`, `OOC_OUT` and temporary/build paths were explicitly private scratch under `/data`. Portable commands, exact build selection, raw focused verdicts and independent observations are in [REVIEW-evidence](REVIEW-evidence/README.md).

```text
python3 -B run.py prep
python3 -B run.py build <29 names in selected-builds.txt> --pool 1 --jobs 8
python3 -B run.py run <same 29 names> --pool 8
python3 -B run.py controls --pool 8
python3 -B probe_preload.py
python3 -B assert_review_observations.py <adjacent-probes.json>
```

The immutable fresh selection is **FOCUSED: 29 builds, 243 runs, 2420 checks, zero verdict failures**. It includes both main shapes, the synthetic-rate shape, the tracked negative control and 25 selected mutants. Each selected kill has a completed scenario and the required diagnostic; none survived. All eight process controls returned their expected exits/diagnostics. The additional reviewer build ran ten scenarios; seven explicit observation assertions pass, including assertions that reproduce R3-F1. Process success alone is not a conformance verdict. The published full 69-build / 312-run / 3462-check / 65-mutant campaign was inspected, not freshly reproduced in full.

Eighteen sequential candidate docs/interface commands exited zero (each Python entry below was run with `python3 -B`); their exact arguments and exits are retained in `REVIEW-evidence/gates.json`:

```text
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_doc_paths.py
scripts/check_solution_docs.py
scripts/check_feature_status.py
scripts/check_submodule_docs.py
docs/traceability/gen_module_matrix.py --check
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
scripts/check_archive.py
scripts/check_hygiene.py --check
scripts/check_todo_ownership.py
scripts/check_em_dash.py --base 2d8fd62fd986ea2d6a87d284e144f023034c0944
scripts/check_nvm_record_space.py
scripts/check_nvm_record_space.py --self-test
scripts/check_port_contracts.py
scripts/check_rtl_source_lists.py
scripts/check_soc_sources.py
```

`git diff --check` against the supplied live base also passed. Head/base/branch identity, ancestry, submodule pins and tracked-source integrity were rechecked at completion. Only this report and its accompanying review artifacts were added; tracked sources remain byte-exact.

Omissions: no full product native bar, full milan_dp rerun, hosted-CI polling, Docker/act, hardware, privilege, push, public write or subagent. No fresh OOC cell was necessary for the identified handshake defect; the committed recipe/results were inspected, and Vivado was not invoked. Thus no shared Vivado lock was acquired. No integrated placement/timing, silicon persistence claim or complete reset/CDC proof is made. The deferred full native bar and required hosted/merge gates remain mandatory before ready/merge; their scheduling after positive contract reviews is not a waiver. Issue #70's hardware evidence remains owed.

**Reviewer-owned covering ledger.** Prepared here for publication; no public write was performed. There are **no clean entries** at this head. Conformance, RTL and Robustness remain open under R3-F1; Tests and Docs are also implicated. No artifact-based PASS line is justified for an assigned lens, and no earlier round is banked. Resolving other findings, or deferring R3-F1, cannot clear those lenses.

| Lens | Covering round | Exact page head |
|---|---|---|

R217 FINISHED
