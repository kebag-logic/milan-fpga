[R218] NEGATIVE - exact head 40d14d92bfcf3823ed7b227537630f444b1f4f73

Independent external contract review of PR #503, issue #500, round R218/r2. Assigned lenses applied: **Docs first, then Tests**, followed by rechecking both against the complete corrected proposal. Neither lens is clean. Findings also carry Conformance, RTL and Robustness where applicable; this review does not claim complete coverage of those other review assignments.

The published evidence reproduces exactly, and the original payload-error, timeout, runner and configuration-replay counterexamples have meaningful corrections. Nevertheless, a header-read error recurring in both passes still causes a partial restore reported as success. The page discloses this defect but permits the first implementation stage without its resolution, contradicting its unconditional failure/default contract. Two further evidence/documentation inconsistencies remain below.

This is a verdict on the Proposed contract and executable evidence. It grants no product implementation approval, silicon validation or merge authorization.

Public authorities examined: [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), its [staging decision](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5756923522), [issue #70](https://github.com/kebag-logic/milan-fpga/issues/70), REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, docs/README.md, the accepted SAVED_STATE_SNAPSHOT_OWNERSHIP and SAVED_STATE_FASTCONNECT contracts, and pinned processor F07.8/F07.9. Read both [archived first-round reviews and reproductions](https://github.com/kebag-logic/milan-fpga/tree/597bc777c652f709634e5c14afef6d853fc5b713/review-evidence/503-round1), the [public revision response](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758107685), [REVIEW READY claim](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758113383), [validation/scheduling clarification](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758113695), public issues #501/#502 and relevant processor issues #15/#20/#61/#63/#83. Reconstructed the four-file documentation diff and public commit history. No private handoff, management receipt, scratchpad or transcript was read.

Artifact notation:

- `P` = [SAVED_STATE_MATERIALIZATION.md](https://github.com/kebag-logic/milan-fpga/blob/40d14d92bfcf3823ed7b227537630f444b1f4f73/docs/design/SAVED_STATE_MATERIALIZATION.md) at the exact page head above.
- `E` = [proposal-evidence](https://github.com/kebag-logic/milan-fpga/tree/ca8cb5943f885c22aec397ff75059e2d4791f4fb/design-evidence/500-materialization/proposal-evidence).
- `T` = [ticket drafts T1-T8](https://github.com/kebag-logic/milan-fpga/tree/ca8cb5943f885c22aec397ff75059e2d4791f4fb/design-evidence/500-materialization/tickets).
- Both `E` and `T`, and their command/digest receipt, were read at immutable public commit `ca8cb5943f885c22aec397ff75059e2d4791f4fb`, freshly fetched into a disposable checkout. Product citations refer to the page head; processor citations refer to pin `424c688fa2205b934a7689a58f2aa766420f2326`.

[R218] MAJOR Conformance, RTL, Robustness, Tests, Docs - P:835, P:1133, P:1313; E/prototype/KL_aecp_nvm_writer.proto.sv:738 - F1 remains open: recurring header errors bypass the restore transaction

Requirement/evidence: P section 3 rule 7 and section 13 promise that a transport failure in either pass produces complete defaults with restore failure. Section 8.6 compares only the numbers of fully read records. At the pinned port, a device error during header acquisition and an unframed/erased header both produce an error with zero forwarded bytes. The prototype's `R_RS` treats zero bytes as blank. The same failure in both passes therefore leaves the counts equal. P section 15 item 5 correctly admits this, but T1 explicitly excludes port changes and makes processor issue #15 optional. T8 is a draft addendum, not a prerequisite or an implemented distinction.

Independent reproduction used V1a's genuinely committed 1x1 slots, unchanged published RTL/firmware/graders, and the V18 stimulus with `read_fault(0x50, 0, -1, 1)` changed to `read_fault(0x50, 0, -1)`: the same header-lane memory response fails in both passes. The scenario completes normally; inspection of the actual checks, rather than its process status, gives:

```text
applied 9, refused 0, blank 40 of 49
0x50 live (0, 0), saved (1500000, 1)
9 other D3 records differ from their defaults
D3 done 1, fail 0, rolled back 0, closed 0, cause 0
restore terminal 7527; entity enabled 7538; abort 0; rollback 0
rolled_back_to_defaults@terminal: FAIL
rollback_premise@terminal: FAIL
```

The original V18 pass-1-only fault and an adjacent pass-0-only fault both roll back correctly, with cause 5 and zero records off defaults. An additional split-header stimulus also rolls back; it is not evidence of an equal-count failure. The repeated-header result above is sufficient: no mutant is needed, and the unchanged baseline itself violates the claimed guarantee. The original R218 payload fault, armed only after an earlier application, now correctly rolls back; that narrower correction does not close this finding.

Impact: an implementation following the proposed contract can enable an entity containing some saved values and some defaults while reporting no restore failure. A persistent fault is neither an erased record nor a successful restore. Disclosure and a follow-up ticket do not reconcile this with the universal transaction claim or earn clean coverage.

Required change: specify and demonstrate a concrete way to distinguish failed header acquisition from valid absence, or an equivalent mechanism that enforces the promised failure/default outcome. Make that resolution a prerequisite for every implementation stage that relies on this transaction, beginning with stage 1; reconcile P, T1/T4 and the owning processor ticket. Merely comparing record identities in the two passes would still miss a record lost in both. Do not approve a silent exception to the failure contract. Reassess area/latency measurements if the resolution changes the measured mechanisms.

Verification: retain errors early/late in both passes after prior applications; add recurring header errors on saved records, including a sole saved record and several group positions, with genuine erased-record controls. Require an honest failure verdict, complete defaults or the specified contained terminal, no late application, and meaningful named mutations of the new distinction.

[R218] MINOR Tests, Docs - P:680, P:775, P:1185; E/harness/d3_bridge.cpp:228; hdl/milan/milan_datapath.sv:4539 - F6: the output-format oracle admits synthetic behavior without identifying that boundary

Requirement/evidence: the page describes V1a as changing every group the shipped shape can express, and section 8.3 says replay follows the SET program's integrator judgment. The harness's `fmt_supported` admits narrower 1/2/4/6/8-channel AAF formats in either direction. V1a narrows output 0 from its generated eight channels to four; V6a/V6b use two. The pinned product explicitly accepts an output only when its channel count equals that output's generated count, because talker adaptation does not exist. The 1x1 generated default is `0205022002006000`; V1a stores `0205022001006000`. Those are eight and four channels respectively. The real predicate rejects the latter. Section 14 calls the judge a model, but does not disclose this material expansion of its legal domain, as it does for synthetic rates and reset maps.

Impact: these runs discriminate prototype replay and format/map ordering, but do not establish product-legal non-default output-format persistence. Calling the shape shipped does not make this stimulus legal. The nine replay mutants are real detections; their integration applicability is overstated for this group.

Required change: label the narrowing cases and judge behavior explicitly as synthetic. Add a product-legal output-format save/replay control with the actual supported-format predicate, checking its value and valid flag so replay deletion remains discriminating even when only the default format is legal. Preserve the synthetic ordering tests as separately qualified evidence; do not expand the product's accepted formats to make the test pass.

Verification: the shipped eight-channel output accepts its declared format and refuses the narrower alternatives; deleting output-format replay fails the legal case's own check. Document which ordering claims rely on the synthetic broader judge.

[R218] MINOR Docs - T/T8-processor-issue-15-port-deadline.md:27,43 - F7: permanent-silence recovery contradicts mandatory quarantine

Requirement/evidence: T8 item 2 requires keeping the port busy and quarantined until the device terminates, explicitly forever if it never does. Its final paragraph then says a permanently silent device would stop holding the port. No cancellation acknowledgment, device reset, response tagging or other safe release mechanism is specified. P sections 6.4, 8.8 and 15 correctly describe permanent drain. Public processor issue #15 still distinguishes timeout notification from reusable-port recovery; its product choices and criterion-2 amendment have not been accepted.

Impact: the implementation ticket promises a liveness result its own required mechanism cannot provide. A later lane could mistake bounded manager notification for safe reuse of an untagged port.

Required change: make T8's claimed result consistent with indefinite quarantine, or settle and specify the additional safe-recovery contract and its dependency. Do not characterize a timeout pulse alone as releasing a permanently silent device.

Verification: review the corrected ticket against the pinned untagged interface and demonstrate separate cases for finite late completion and permanent silence. Until an independent safe release exists, the latter must remain unavailable rather than accepting another operation.

Every R218 first-round finding has the following disposition. The original severity and all original lens labels are preserved; resolution here concerns the contract deficiency identified, not unimplemented product functionality.

| Prior finding | Original severity and lenses | Round-two disposition and evidence |
|---|---|---|
| F1: non-atomic restore | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **OPEN**, as above. The exact original payload trigger now produces abort cause 2, rollback at 2850, terminal at 3507, enable at 3518 and complete defaults. V12-V16, V18 and owner-reset mutants add meaningful coverage, but recurring header errors still violate the universal claim. |
| F2: enable on firmware timeout | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Original defect corrected in the proposal/model.** Repeated the original first read delayed after any prior application by 3,100,000 cycles. Read held from 3297 to 3103297; D3 abort 23296, rollback 23297, terminal 23954, enable 23963. All defaults restored, `own=0`, no late restore writes. The port remains busy at that terminal and drains until its real completion; a subsequent GET and SET work and persist after drain. P 5.1/5.3, T1/T4 specify new dispatch ownership, soft resets, abort/drain and hardware enable gating. W1-W15, K19 and the named timeout/gate/drain mutants reproduced. This does not claim bounded binding restore or reusable service from a permanently silent port. |
| F3: runner accepts survivors/crashes | MAJOR; Tests, Docs | **Corrected.** Fresh full run plus all seven real CLI controls reproduced expected exits `1,1,1,1,1,2,2` and named diagnostics. A healthy binary substituted for M01 survives and fails the process; a pre-scenario crash substituted for M06 is NOT COMPLETED and cannot count as a kill. Full/focused selection, missing builds, unexpected baseline results, tracked outcomes and vacuity controls are enforced. |
| F4: configuration replay deletion survives | MAJOR; Conformance, Tests, Docs | **Original missing checks corrected.** `RPL_cfg` fails its own `value_restored:0x00` check, including valid flag `(0,0)` versus `(0,1)`. All nine trigger and nine replay deletions have group-specific killers. Every row/index, name and map reset is observed; unsaved defaults and exact counts are graded. `RPL_rate` runs at synthetic 1x1r2. The builder has only configuration 0 and the shipped shapes only one rate; no nonexistent product configuration is claimed. F6 separately qualifies the output-format evidence. |
| F5: staging permits open capacity/status defects | MAJOR; Conformance, Robustness, Tests, Docs | **Release-contract defect corrected; #501/#502 themselves remain OPEN.** P section 10 and T1-T6 enforce a conforming capacity resolution before stage-three implementation/release, and corrected pending for every still-unmaterialized class before ANY shippable stage. Limited earlier implementation is distinguished from release. K16 is explicitly containment only, not accepted-map persistence. This review does not clear either product issue. |

Also checked the other public review without changing its severities or labels. R217 F1/F2 were MAJOR under Conformance, RTL, Robustness, Tests, Docs; the F1 continuation above prevents treating their common transaction claim as resolved. R217 F3 was MAJOR under all five lenses: V3a-V3g now distinguish exact eight-byte `FF` padding, aliases, holes, malformed tails, out-of-range entries and an empty set; P01/P02 are killed by the named result/edit checks. R217 F4 was MAJOR under Conformance, RTL, Robustness, Docs: the strengthened staging conditions are present, while #501/#502 remain unfixed. R217 F5 was **MINOR**, Tests, Docs; the corrected runner evidence addresses its mechanism as well as R218's independently MAJOR finding. These observations do not replace that reviewer's verdict or ledger.

The proposed live-write amendment is explicit and technically justified: the accepted state-bus write carries group/index identity and permits pending before the later mark; a notification mark alone cannot identify every record or cover its preceding tail. P section 15 and T1 name the FASTCONNECT section 16/F07.9 edits, D2 retirement and replacement obligations. Nine independent trigger deletions plus nine replay deletions preserve stronger group-specific evidence, including both format directions and IDENTIFY exclusion. The accepted documents are not silently rewritten by this page. Recording the amendment through the required independent contract decision remains a prerequisite; this negative verdict does not ratify the whole proposal or waive the accepted wording.

O1 and O3 are distinct. Firmware remains the sole sequential control-face writer; the D3 producer and drain operate through the arbitrated device face and do not acquire control-face authority. O3 orders the binding and D3 restore walks before enable, separately from O1. New reset ownership, dispatch gating, local owner resets, descriptor re-walk proof and hardware enable gating are specified integration seams, not existing pinned product features. The corrected prototype executes them. A failed recovery image walk reaches CLOSED with enable held; this is containment, not successful boot. A silent binding walk can remain unbounded and hold dispatch/enable indefinitely. A D3-abandoned read can drain forever and leave subsequent changes permanently pending. Those limitations are stated in P, are consistent with the pinned interface's missing cancellation facility, and are not bounded-boot or port-recovery evidence. T8's conflicting future claim is F7. Header ambiguity is different: it permits an enabled partial restore falsely reported successful, hence the stronger prerequisite required by F1.

Other evidence inspected and its limits:

- F07.8 framing/allocation, KLJ2 erased spans, selectors, sizes, names, map padding/capacity and format/map fallback were cross-checked with generated record space and pinned owners. Invalid-record refusal is per record; transport rollback is a separate property. The #501 output-map capacity mismatch remains a real defect; pending-and-skip does not solve it.
- K1-K19 exercise taint, set-over-clear, same-edge completion, group/index isolation, repeated changes, retry/alarm, grant collision, reset ownership, and cuts in debounce/write/before commit/after acknowledgment. K15's collision premise is reached. This is not a new exhaustive sweep of the accepted snapshot capture/ACK identity protocol.
- M13's stale-store control passes naive read-back and fails cleared-first checks; both outcomes are required. The tracked glue has seven expected failures and four required passes. All 51 mutant kills require a completed scenario and its named check. These controls support their particular claims, not the omitted recurring-header case.
- 1x1r2's 96 kHz rate is a synthetic builder-supported, planned value. Nonempty reset map sets are synthetic; shipped dynamic ports reset empty. The 8x8 input-map group has no corresponding clusters, so its executable replay control is at 1x1. Configuration validity proves application of the sole legal index, not multi-configuration support. F6 identifies the additional output-format qualification needed.
- IDENTIFY has an executable exclusion control. Lock and controller-registry exclusion is structural here; integrated volatile-state reset checks remain owed. Allocated SUID/MCR records have no source and remain erased. The real microprogram timing, product map phases/GET hold and persistence-disabled boot path are not executed by this model; firmware changes 1 and 3 are compiled substitutions, change 2 is not modeled.
- Inspected both OOC recipes, proxy RTL, all 16 published rows, calibration inputs and arithmetic. Revised writer-plus-arbiter measurements/estimates are **2,311 LUT / 862 FF at 1x1**, **2,876 LUT / 987 FF at 8x8**, with zero RAMB36/DSP in those prototype rows. The added watchdog, counters, transaction flags and drain account for 60 more FF. Candidate (a) omits its arbiter; candidate (c) omits firmware and integration costs. The corrected backend calibration is 1,030 LUT / 468 FF for the older 30-name parameter set. Source digests match the revised immutable tree. These are published OOC results inspected here, not fresh synthesis measurements by this reviewer. Integration estimates and 1 MHz model timings do not establish placed area, board latency or a universally valid 20 ms product deadline. The model has instantaneous instruction execution and two/three-cycle memory responses.

Executed commands and results use variables for reviewer-owned disposable paths. The initial output tree was empty; D3_OUT, OOC_OUT and TMPDIR were explicitly set under the authorized scratch filesystem. The runner was copied byte-for-byte to a sibling directory at the same repository-relative depth because a full run rewrites results beside itself; immutable evidence sources were preserved.

```sh
rtk proxy git status --porcelain=v1
rtk proxy git rev-parse HEAD
rtk proxy git submodule status
rtk proxy git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence
rtk proxy git merge-base --is-ancestor 07294a76e833f1831d9fcbceb8123b8380c4ae76 HEAD

rtk proxy git -C "$EVIDENCE_ROOT" fetch origin 500-design-evidence
rtk proxy git -C "$EVIDENCE_ROOT" checkout --detach ca8cb5943f885c22aec397ff75059e2d4791f4fb
rtk proxy git -C "$EVIDENCE_ROOT" submodule update --init --jobs 8 \
  third_party/verilog-axis protocol-processor gptp-processor

export TMPDIR="$SCRATCH/tmp" D3_OUT="$SCRATCH/d3" OOC_OUT="$SCRATCH/ooc"
rtk proxy taskset -c 80-95 python3 -B run.py prep
rtk proxy taskset -c 80-95 python3 -B run.py build --pool 1 --jobs 8
rtk proxy taskset -c 80-95 python3 -B run.py run --pool 8
rtk proxy taskset -c 80-95 python3 -B run.py controls --pool 8
```

All four evidence commands exited 0. Result: `SUMMARY FULL builds 55, runs 230, checks 2524, verdict failures 0`. Both generated result files are byte-identical to the published files: results.txt SHA-256 `2537596f56a0cdbbaef80286d9664d47e7e5c1da50e1fe729d3665bb011bdc86`; results.json SHA-256 `3806a7df050b5a31239f808203b1236f7d30e9a81d58df240ce97bd08712ebcd`. All seven runner controls found their required diagnostics. Every command completed before its dependent step; builds used one pool member and at most eight jobs on CPUs 80-95.

Reviewer-only probes used a separate copied harness and output tree with the original prototype and graders. For F1's repeat case, copy `E/harness`, replace the one V18 `read_fault` call as quoted above, import `E/run.py`, redirect its `HARNESS` and `STUBS` to that copy, and call `prep_shape('1x1')`, `do_build(Build('reviewer-headers', '1x1'), shape, 8)`, then `run_case(build, shape, 'V18_header_error_pass1', 'repeat', slots)`. Here `slots` are the two `cut-slot*.bin` files from the fresh `base-1x1/V1a_set_everything` run. Call `grade_run` with `cut_slots` decoded from those same files; inspect `rolled_back_to_defaults@terminal`, terminal rows and boot events. The probe scenario's exit 0 is not an approval. The original F1 reproduction additionally delays fault eligibility until `d3_rs_applied_o != 0`; the original F2 arms the first memory read after that same condition for 3,100,000 cycles. Only disposable stimulus sources changed.

The following 26 focused gates ran synchronously on the exact page checkout as `rtk proxy taskset -c 80-95 python3 -B <command>`; every gate exited 0. `git diff --check` also passed.

```text
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_solution_docs.py
scripts/check_doc_paths.py
scripts/check_archive.py
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
docs/traceability/gen_module_matrix.py --check
scripts/check_feature_status.py
scripts/check_submodule_docs.py
scripts/check_hygiene.py --check
scripts/check_todo_ownership.py
scripts/check_em_dash.py --base 07294a76e833f1831d9fcbceb8123b8380c4ae76
scripts/check_nvm_record_space.py
scripts/check_nvm_record_space.py --self-test
scripts/check_port_contracts.py
scripts/check_rtl_source_lists.py
scripts/check_soc_sources.py
scripts/check_cpp_idiom.py
scripts/check_py_idiom.py
scripts/check_sv_idiom.py
scripts/check_sh_idiom.py
scripts/ci_scope.py --selftest
scripts/measure_naming.py --check
scripts/measure_fail_fast.py --check
scripts/measure_test_evidence.py --check
```

Initial and completion identity checks: page HEAD and remote PR head both `40d14d92bfcf3823ed7b227537630f444b1f4f73`; live remote dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor of the page head; evidence branch head `ca8cb5943f885c22aec397ff75059e2d4791f4fb`. Required submodule pins in both checkouts: protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Unused `external` remains uninitialized at `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`. Initial tree was clean. At completion all tracked sources remain byte-exact; only this requested REVIEW.md is untracked in the page checkout. Independent blob hashing, with Git replacement objects disabled, checked 850 page blobs, 884 evidence blobs and 539 submodule blobs per checkout with zero mismatches. All 48 revised receipt digests resolve to immutable published files and match: 34 evidence/ticket files plus 14 repository inputs. The old absent `abc.history` entry is gone.

Omissions: no product changes, actual AECP integration run, full milan_dp rerun, full native regression/lint/portability gates, fresh OOC/calibration synthesis, Vivado, placement, hardware or power-cycle soak. The inspected recipe/rows showed no assigned-lens concern requiring a synthesis repeat, so no Vivado lock was acquired. No Docker/act, privilege, subagents, push, public write or hosted-CI polling. Public fast-check/scheduling claims do not substitute for the independently continuing mandatory gates. This review makes no claim of full CI completion, product release readiness or silicon proof.

Reviewer-owned coverage ledger: **no clean covering entries** are banked at this head, so there are no per-lens PASS lines. The table records open coverage, not approval. F1 remains open under all five original labels; F6/F7 also prevent clean assigned-lens coverage. Re-review must name the corrected page head and immutable supporting evidence.

| Lens | Covering round | Exact page head |
|---|---|---|
| Tests | OPEN: R218/r2 applied; F1 and F6 open | 40d14d92bfcf3823ed7b227537630f444b1f4f73 |
| Docs | OPEN: R218/r2 applied; F1, F6 and F7 open | 40d14d92bfcf3823ed7b227537630f444b1f4f73 |

R218 FINISHED
