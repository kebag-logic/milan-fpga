[R218] NEGATIVE - exact head d0256846dd0138e727386ae42e43710c332f2a23

Independent external contract review of PR #503, issue #500, round R218/r1. Assigned lenses applied: **Tests first, then Docs**. Neither is clean. Findings also carry Conformance, RTL and Robustness where applicable; this review does not claim complete coverage of those other assigned review responsibilities.

The published run is reproducible, but it does not establish the proposed restore guarantees. A second-pass read failure leaves an earlier record applied; a delayed read permits entity enable before restore completes; deleting configuration replay survives the original 1x1 plan. The runner also returns success when a named mutant survives. The stage contracts need explicit restrictions around the open capacity and pending-status defects.

This verdict concerns the Proposed contract and its executable evidence. It is not a product implementation verdict, silicon evidence, or authorization to implement or merge.

Public authorities examined: [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), the [manager REVIEW READY comment](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5756529970), [issue #70](https://github.com/kebag-logic/milan-fpga/issues/70), REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, docs/README.md, SAVED_STATE_SNAPSHOT_OWNERSHIP sections 6.1/7/11/13/20, SAVED_STATE_FASTCONNECT sections 4/6/9/12/16, and processor F07.8/F07.9. Also examined public issues #501/#502/#495 and processor issues #15/#61/#63/#83, the four-file PR diff and four-commit history, and the public ticket drafts. No private handoff, management receipt, scratchpad or transcript was read.

Artifact notation below:

- `P` = `docs/design/SAVED_STATE_MATERIALIZATION.md` at the exact page head above.
- `E` = [design-evidence/500-materialization/proposal-evidence](https://github.com/kebag-logic/milan-fpga/tree/a21b165ac1c671d10cba7255beaf75cea0f81d18/design-evidence/500-materialization/proposal-evidence) at immutable evidence commit `a21b165ac1c671d10cba7255beaf75cea0f81d18`.
- `T` = [public ticket drafts](https://github.com/kebag-logic/milan-fpga/tree/242d120a704215fbfbcaa1be4b4263f5f25babc0/design-evidence/500-materialization/tickets) at `242d120a704215fbfbcaa1be4b4263f5f25babc0`. The newer branch tip was used only for these drafts.
- Product source citations refer to page head `d0256846dd0138e727386ae42e43710c332f2a23`; processor sources refer to pin `424c688fa2205b934a7689a58f2aa766420f2326`.

[R218] MAJOR Conformance, RTL, Robustness, Tests, Docs - P:617; E/prototype/KL_aecp_nvm_writer.proto.sv:675 - F1: Two passes do not make a torn restore atomic

Requirement/evidence: P sections 3.7, 8.6 and 13 promise that a torn D3 stream applies nothing. `R_RS` goes directly to `R_FIN` on a partial read error in either pass. `R_APPLY` has already written earlier records in pass 1, and `R_FIN` does not undo them. The published V11 fault is active from the beginning, so it always aborts pass 0 before any application.

Independent reproduction: keep the original V11 image, prototype, firmware and grader. In the scratch copy of `E/harness/d3_bridge.cpp:117`, arm its existing read fault only after `d3_rs_applied_o != 0`. This changes only when the fault arrives. The original `torn_walk_applies_nothing@boot` check fails:

```text
ptof0 valid 1 (its record was read whole before the torn one),
restore fail 1, D3 fail 1, applied 1
```

The entity is subsequently enabled. M16's first-pass counterexample therefore proves the need for some protection, but does not prove the proposed protection sufficient.

Impact: an implementation following the proposed state machine can expose a partially restored entity despite the stated all-or-nothing contract. The second pass is another fallible read, not a guarantee about future reads.

Required change: specify and demonstrate a mechanism that enforces the promised failure outcome for errors during either pass, including restoration of defaults before release if that is the chosen mechanism. Update the state machine, cost qualifications and T1 acceptance consistently. Do not accept the present design on a promise to repair the second pass later.

Verification: inject errors after earlier records have been applied in pass 1, at multiple record and payload positions, as well as in pass 0. Require the terminal failure/default state and zero surviving partial restore before enable. Retain V11 and its named mutant as separate controls.

[R218] MAJOR Conformance, RTL, Robustness, Tests, Docs - P:493; P:701; sw/firmware/milan_baremetal/milan_baremetal.c:1165 - F2: The timeout path violates restore-before-enable

Requirement/evidence: P section 8.1 orders both walks before enable, section 8.1 says no advertisement precedes the restored values, and section 11 says the firmware's bounded wait keeps the entity available and the order is proved. The unchanged `nvm_restore_walk()` breaks out after `MILAN_NVM_RESTORE_TIMEOUT_MS` (3000), without aborting or draining D3. `milan_init()` then calls `entity_advertise()`. The proposed writer and pinned port have no cancellation contract for this path. Processor issue #15 remains open.

Independent reproduction: run V1b using V1a's genuinely committed slots and the unchanged prototype/firmware. Change only the scratch memory model: delay one read response, after an earlier record was applied, by 3,100,000 model cycles. The original ordering check fails:

```text
enabled at 3000105, D3 restore done at 3107345,
restore done at 3107345
```

The firmware reports `the restore walk did not sequence in time` and then `walk done=0 fail=0 blank=0 backed=1`; D3 later finishes and changes the remaining state. G02 tests an early done indication, not this existing timeout path.

Impact: the proposed O3/boot-order guarantee fails under delayed or silent service. A finite timeout returning to its caller does not stop a late restore from modifying an enabled entity. Permanent silence can also leave D3 owning the state bus indefinitely.

Required change: settle the timeout and terminal-failure contract before implementation. Enable must follow either the completed restore or a completed, safe abort/default transition that prevents late application. State the dependency on any required port timeout/abort work. Align the one-reorder firmware claim, O3 explanation, alternatives and T1/T4 with that decision.

Verification: retain the delayed-read counterexample, add silence and late-completion cases, and check enable, restore verdicts, state-bus ownership and absence of post-enable restore writes. Apply the checks to all relevant read faces, rather than only the normal two/three-cycle memory model.

[R218] MAJOR Tests, Docs - E/run.py:1098; E/run.py:1165; P:114 - F3: The runner accepts surviving mutants and failed scenarios

Requirement/evidence: the page says the runner refuses success unless the tracked checks have their expected outcomes. The README and run.py also say every mutant must be killed or the run fails. `report()` increments `fail`, prints it and writes the results, but returns no status; `main()` unconditionally returns 0 after `report(allres)`.

Independent reproduction through the original CLI: in a separate output tree, substitute the known-good `base-1x1` binary for `mut-M01_taint_ignored`, making that planted mutation deliberately ineffective. Run `python3 -B run.py run mut-M01_taint_ignored --pool 1`. Real K2 stimulus and the original named grader produce:

```text
MUTANT M01_taint_ignored: SURVIVED by K2_change_during_record_write : no_durable_claim_over_unsaved
SUMMARY runs 1, checks 7, verdict failures 1
process exit: 0
```

An additional CLI control substituted `/usr/bin/false` for the M06 binary. No scenario ran. The result recorded `case_completed -- rc 1, done False`, but missing observations also failed `identify_never_persisted`, which the runner accepted as the required kill:

```text
MUTANT M06_identify_is_a_change: KILLED by K14_identify_is_not_persisted : identify_never_persisted
SUMMARY runs 1, checks 4, verdict failures 0
process exit: 0
```

Impact: shell callers can accept a surviving mutant, unexpected baseline failure or broken vacuity control as success; even inspecting a zero-failure summary is insufficient when a failed scenario counts as a kill. This does not invalidate the manually inspected published run, which reproduced exactly; it invalidates the claimed executable refusal behavior.

Required change: propagate verdict failures to a nonzero CLI exit, retaining the diagnostic results. Require successful scenario completion and the expected behavioral diagnostic before counting a mutant killed. Require expected builds/cases where a full-run claim is made, so an empty selection cannot establish it.

Verification: execute the actual CLI with an ineffective named mutant, a binary that fails before the scenario, an unexpected baseline result, and a violated tracked/control expectation. Each must fail the process for its named reason; the genuine complete run must still pass.

[R218] MAJOR Conformance, Tests, Docs - P:530; P:867; E/run.py:778 - F4: Configuration replay can be deleted without invalidating the evidence

Requirement/evidence: the page includes configuration in the persistent set and cites V1b for it. Processor issue #63 expressly requires replay into SEL_CFG with its valid flag. V1b reads `post.cfg`, but its grader never checks that result. `restore_counts@boot` permits any applied-plus-blank count less than or equal to the record count, so it also accepts a missing application. The cleared-first check only checks five scalar index-zero flags; it is not the claimed check of every restorable row.

Independent mutant: in a scratch prototype copy, change the first branch of `R_APPLY` at line 791 to skip only `G_CFG` and go to `R_ADV`. Leave every write trigger, other replay path, harness and grader unchanged. Run the entire original 1x1 base plan:

```text
SUMMARY runs 43, checks 253, verdict failures 0
configuration valid before restore: 0
configuration valid after restore:  0
configuration payload in saved slot: 0000
```

This is a surviving behavioral mutant, independently of F3's exit-code bug. Both shipped shapes have one configuration, so GET returning the default zero cannot distinguish missing replay. Also, `set_everything()` skips sampling-rate writes when the image has only one supported rate, as both shipped shapes do. A refusal test for an invalid rate does not establish valid-rate persistence.

Impact: the evidence can report success with a missing required group's restore. The configuration traceability and universal cleared-first language claim more coverage than the graders implement.

Required change: grade the actual restored value and valid flag for every group claimed covered, including configuration and a legal sampling-rate write. Make omissions and supported-shape limits explicit. Extend cleared-first coverage to the state actually claimed, including names/maps and relevant indices, with independently observable defaults. Preserve per-group trigger-deletion acceptance when changing the mark contract.

Verification: the configuration-only replay deletion must fail a configuration-specific check. Exercise a valid rate save/replay despite the single-rate shipping shape, and a non-default configuration where the supported test model permits one. Retain the stale-store control, and check actual application rather than only inequality-based totals.

[R218] MAJOR Conformance, Robustness, Tests, Docs - P:660; P:823; T/T3-processor-stage3-channel-maps.md - F5: Open defects are described but the stage release conditions do not consistently exclude them

Requirement/evidence: [issue #501](https://github.com/kebag-logic/milan-fpga/issues/501) explicitly says permanently pending accepted mappings do not meet Milan 5.3.10.1 and requires a conforming allocation or accepted-mapping limit. P rule 8, section 10's independently shippable stage 3 and T3 acceptance instead allow a legal oversized set to remain unwritten indefinitely. K16 grades retention of pending and eventual convergence only after shrinking; it does not establish persistence of the accepted oversized set. T4 says T5 must decide capacity before stage 3 *claims* 8x8 persistence, but the page does not make conforming resolution a prerequisite to shipping that affected stage.

Similarly, [issue #502](https://github.com/kebag-logic/milan-fpga/issues/502) records an actual durable-looking interval after live map/name writes. P section 10 calls stages independently shippable while section 15.7 leaves that defect until stages 2 and 3. T4 deliberately retains the mark-derived sticky source for unfinished classes. No explicit release condition requires the standalone pending correction before those intermediate stages ship.

Impact: completing the written stage tests can still leave accepted state unpersistable or falsely reported durable. Filing #501/#502 does not resolve either defect or earn clean coverage for these proposed release conditions.

Required change: reconcile P and T1-T4 with the strengthened public issue contracts. Make conforming capacity a prerequisite to the affected map stage, and make truthful pending status a prerequisite to any stage declared shippable. State which stages/shapes remain blocked and which limited work may proceed. This documentation PR need not implement the fixes; it must not authorize a nonconforming stage or count deferred findings as clean.

Verification: review the dependency/acceptance text, then require capacity and one-over-capacity tests against decoded journal data and cleared-first restore, plus real program/glue status checks from the first accepted write through the mark for each still-unmaterialized class. Shrink-to-fit and a sticky flag alone cannot establish those properties.

The live-write trigger change is reasonable as an explicit amendment: accepted live writes can assert pending before the later mark, and state-bus selector plus descriptor index identifies the record. The inspected SET_NAME and map programs support the ordering rationale. O1 remains one sequential control-face master; adding an arbitrated producer behind the existing device port does not itself violate O1. O3 requires a separate restore-order argument, and F2 prevents accepting that argument as written. The old mark-deletion acceptance must be explicitly replaced by per-group trigger-deletion coverage, including both stream-format directions, without weakening the volatile-state refusals. This assessment does not ratify the full page while the findings remain open.

Other examined evidence and boundaries:

- The original full run reproduced 27 builds, 121 runs, 778 checks, all 24 named mutant detections, the M13 stale-store control, K15's g3 collision premise, and the seven required tracked failures/four required tracked-pass rules. Reproduced `results.txt` SHA-256 is `0b112180e3770dc410e916327411f5852b887598bb2164e84fea99dd2beb49e2`, identical to the published artifact.
- Inspected dirty/set/clear/taint and retry-exhaustion/alarm priority, same-edge completion, group/index isolation, repeated writes, coalescing, oversized maps, and cuts in debounce/write/before commit/after acknowledgement. K1-K19 support the specific tested orderings. No new exhaustive sweep of flash-verification/ACK races is claimed; that mechanism remains the accepted snapshot contract's responsibility.
- Inspected F07.8 framing, KLJ2 ordering and erased spans, record-space generation, scalar widths and selectors, name ordinals, map framing/capacity, format/map fallback, image-before-name ordering, invalid value/CRC refusal, and the named mutant rules. The microprogram, map edit plane and format judge are models, as the page states. Invalid clock/offset boundaries, every frame field, empty-name replay and every index are not all independently exercised by this proposal's cases.
- IDENTIFY has an executable refusal control. Lock and controller-registry exclusion is a structural argument, with implementation-level restore tests still owed. Started/stopped belongs to binding. Allocated system-unique-id/media-clock-reference records remain source-less and erased; no persistence proof for them is claimed.
- Reviewed both OOC scripts, proxy RTL, committed cell rows and arithmetic. The writer-plus-arbiter sums are 2,312 LUT/802 FF at 1x1 and 2,925 LUT/927 FF at 8x8, with zero block RAM in those rows. Candidate (a) is replication plus a shadow proxy, omitting its arbiter; candidate (c) omits firmware and integration costs. The page's corrected measurement/estimate qualifications are appropriate. Neither those rows nor model-cycle timings establish integrated area or latency guarantees, especially for a revised restore/abort design.
- Checked the command record digests against the fresh public checkout: all 38 present files matched. Its 39th entry, `ooc/abc.history`, is absent from the immutable Git tree and has the empty-file digest. Thus the public checkout supports 38 file matches, not literal reproduction of all 39 listed files without generating that incidental file.

Commands and results, using reviewer-owned disposable paths represented by variables:

```sh
git status --porcelain=v1
git rev-parse HEAD
git submodule status
git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence
git merge-base --is-ancestor 07294a76e833f1831d9fcbceb8123b8380c4ae76 HEAD

git clone --no-checkout --single-branch --branch 500-design-evidence \
  https://github.com/kebag-logic/milan-fpga.git "$EVIDENCE_ROOT"
git -C "$EVIDENCE_ROOT" checkout --detach a21b165ac1c671d10cba7255beaf75cea0f81d18
git -C "$EVIDENCE_ROOT" submodule update --init --jobs 8 \
  third_party/verilog-axis protocol-processor gptp-processor

export TMPDIR="$SCRATCH/tmp" D3_OUT="$SCRATCH/d3" OOC_OUT="$SCRATCH/ooc"
taskset -c 80-95 python3 -B run.py prep
taskset -c 80-95 python3 -B run.py build --pool 1 --jobs 8
taskset -c 80-95 python3 -B run.py run --pool 8
```

The evidence runner was executed from a byte-identical disposable copy at the same repository-relative depth because it rewrites results beside itself. The initial D3 output tree was empty. All three commands exited 0, and the full summary was inspected independently of that status. Tool versions: Verilator 5.052, sv2v 0.0.13, Python 3.14.7; installed Yosys reports 0.66. Builds used one pool member and at most eight jobs, pinned to CPUs 80-95. No OOC synthesis command was executed.

Reviewer-only probes used separate scratch build/output directories with at most eight build jobs. F1 and F2 changed only the indicated C++ memory fault model. F4 changed only a disposable prototype copy. Their original graders produced the results quoted above. F3 was repeated through the unmodified CLI using both deliberate binary substitutions, with the results quoted above. No tracked product or evidence source was changed by these probes.

The following 22 focused gates ran on the exact page checkout as `python3 -B <command>`, synchronously under `taskset -c 80-95`; every command exited 0:

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
```

Initial and completion identity checks: page HEAD and remote PR head both `d0256846dd0138e727386ae42e43710c332f2a23`; live remote dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor of the page head. Required submodules are exactly protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused `external` submodule remains uninitialized at recorded pin `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`. Initial tree was clean; completion retains byte-exact tracked files and only the requested untracked REVIEW.md in the page checkout. Independent Git blob hashing checked 850 page-tree blobs, 875 evidence-tree blobs and 539 submodule blobs per checkout, with zero mismatches and replacement objects disabled.

Omissions: no product implementation, real AECP integration run, full milan_dp regression, exhaustive RTL suite, full lint/elaboration/portability gate, fresh OOC/calibration synthesis, Vivado, placement, hardware, power-cycle soak, Docker/act, hosted-CI polling, privilege, subagents, push or public write. The committed cost recipe and rows were inspected; fresh OOC was unnecessary to establish the assigned-lens findings, so no Vivado lock was acquired. No claim of silicon proof, full CI completion or release readiness is made.

Reviewer-owned coverage ledger. There are **no clean covering entries** from this round and consequently no per-lens PASS lines. The table records the open state rather than banking coverage. Re-review must name the corrected page head and supporting immutable evidence.

| Lens | Covering round | Exact page head |
|---|---|---|
| Tests | OPEN: R218/r1 applied; F1-F5 unresolved | d0256846dd0138e727386ae42e43710c332f2a23 |
| Docs | OPEN: R218/r1 applied; F1-F5 unresolved | d0256846dd0138e727386ae42e43710c332f2a23 |

R218 FINISHED
