[R217] NEGATIVE - exact head d0256846dd0138e727386ae42e43710c332f2a23

Independent internal contract review of PR #503 / issue #500, round R217-r1. Assigned lenses: Conformance, RTL, Robustness. Applied RTL/state ownership first, then Conformance and Robustness; applied Tests and Docs to the evidence and claims implicated below. No prior clean coverage was available for these assigned lenses. This verdict concerns the proposed contract and its executable evidence. It neither approves product implementation nor grants merge permission.

Authority reconstructed from [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), the [public review-ready comment](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5756529970), issue #70, REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, SAVED_STATE_SNAPSHOT_OWNERSHIP.md, SAVED_STATE_FASTCONNECT.md, and the pinned processor's F07.8/F07.9 contracts and RTL. Also examined public issues #501/#502 and processor issues #15/#61/#83. No private handoff or transcript was used.

The page references below are `docs/design/SAVED_STATE_MATERIALIZATION.md` at the exact head above. Evidence references are relative to `design-evidence/500-materialization/proposal-evidence/` at immutable commit [a21b165ac1c671d10cba7255beaf75cea0f81d18](https://github.com/kebag-logic/milan-fpga/tree/a21b165ac1c671d10cba7255beaf75cea0f81d18/design-evidence/500-materialization). Public ticket drafts were read separately at evidence-branch tip `242d120a704215fbfbcaa1be4b4263f5f25babc0`; that tip was not substituted for executable evidence.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:617 - F1: Two passes do not make restore all-or-nothing

Requirement/evidence: Section 8.6 and the consequence at line 759 promise that a torn stream applies nothing. In `prototype/KL_aecp_nvm_writer.proto.sv:675`, an error on either pass goes directly to R_FIN. Pass 1 has already applied earlier records and has no rollback. The published V11 fault is present before boot, so it always stops pass 0; killing M16 only establishes that limited case.

Independent reproduction kept all RTL and firmware unchanged. Starting from V11's valid slot, allow the first header and payload reads of record 0x80 to complete, then arm the same read error at payload byte 16. The first-pass control reports `ptof0 valid 0, restore fail 1, D3 fail 1, applied 0`. The second-pass fault reports **`ptof0 valid 1, restore fail 1, D3 fail 1, applied 1`**. The existing `torn_walk_applies_nothing@boot` check fails.

Impact: A transport failure publishes a partially restored configuration despite the contract's whole-walk guarantee. An earlier format can also remain applied without the later map consistency check, which is reached only after all map reads.

Required change: Specify a restore transaction that contains failures during the applying pass, including already applied values and format/map consistency. Demonstrate that mechanism before claiming the property. A successful earlier read is not a guarantee about a later transport operation.

Verification: Inject faults independently on each pass, early and late, with prior non-default scalar, format, map and name records. Verify the declared rollback/default policy and entity visibility, not just restore_fail.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:701 - F2: Firmware timeout enables the entity without containing the restore

Requirement/evidence: Sections 3/8.1 require restore before enable and claim O3 is preserved. Line 701 instead relies on a bounded firmware wait to keep the entity available. The unchanged `sw/firmware/milan_baremetal/milan_baremetal.c:1173` breaks out on timeout and subsequently advertises; it neither aborts the D3 writer nor releases its state bus. The prototype holds `own` from R_ACQ until R_FIN. Both the port and the backend can wait indefinitely for a missing memory response. Processor issue #15 remains open, and T1 explicitly excludes port changes.

Independent reproduction delayed one accepted D3 memory read by 3,500,000 model cycles. The actual host-compiled firmware's timeout is 3,000 ms. It printed the timeout and enabled the entity at **cycle 3,000,074**, with `restore_done=0`, `restore_fail=0`. The late response subsequently allowed **two records to apply**, and restore completed at **cycle 3,505,888**. Normal V1b/G02 coverage does not exercise this path.

Impact: Restore changes live state after enable, contradicting the ordering guarantee. Permanent silence leaves the writer owning the bus indefinitely and prevents ordinary AECP state access; timing out the CPU's wait does not make that plane available.

Required change: Decide and specify timeout/abort containment, ownership release, handling of late responses and partial restore, and the conditions under which entity enable is allowed. Make any necessary processor/parent dependency an explicit prerequisite. Naming the existing timeout issue or relying on a later integration fix does not establish this contract.

Verification: Exercise silence and responses immediately before/after the deadline, on both walks and both D3 passes. Assert terminal status, bounded ownership, no post-enable restore writes, and usable command processing after the declared recovery.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:553 - F3: Invalid map entries can bypass the promised value refusal

Requirement/evidence: Section 8.3 requires a framed map to pass the SET program's value rule, otherwise retaining the reset set. `prototype/KL_aecp_nvm_writer.proto.sv:846` describes unused entries by their first byte pair, but line 854 checks only `bs_rd_w != 8'hFF`. Consequently an invalid stream index with high byte 0xff is treated as padding instead of reaching the map judge.

Independent reproduction used the unchanged baseline-1x1 binary and a correctly framed/CRC-closing KLJ2 slot containing one output mapping `{stream=0xff00, channel=0, cluster=0, cluster_channel=0}`, followed by the ordinary 0xff padding. It reported **`refused 0, applied 1`**, replacing the model's nonempty reset set with an empty set. The same test with invalid stream index `0x0100` correctly reports **`refused 1, applied 0`** and retains the reset set. The existing V3 default-preservation check fails for 0xff00.

Impact: Malformed values alias the valid empty-map encoding and are reported as successfully restored. The different shipping reset set does not make the invalid index legal or validate the refusal claim.

Required change: Define the exact unused-entry encoding and validate every non-padding entry without this alias. The prototype/evidence supporting the proposed refusal rule must implement that distinction.

Verification: Cover 0xfeff, 0xff00, 0xfffe, the exact padding sentinel, malformed sentinel tails and holes, ordinary out-of-range indices, and a valid empty set. Check refusal/application counts and preserved defaults as well as decoded maps.

[R217] MAJOR Conformance, RTL, Robustness, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:197 - F4: Permanent pending is still an accepted Stage 3 outcome

Requirement/evidence: REQUIREMENTS.md section 1, issue #70 and Milan 5.3.10.1 require accepted output mappings to persist. Rule 8, the independently shippable Stage 3 at line 670 and UNRESOLVED 2 explicitly permit an accepted 8x8 set to remain unwritten indefinitely. K16 reproduces 10 mappings against a 9-entry record. This is also consistent with the actual parent key: `milan_datapath.sv:4106` uses stream/channel rather than cluster as the output key. Honest pending status prevents a false durability claim; it does not satisfy persistence.

The public T4 draft says T5 must decide the record before Stage 3 *claims* 8x8 persistence. That qualification is useful, but the page and T3 still specify permanent non-materialization as acceptable implementation behavior. Issue #501 explicitly says permanent pending is not an accepted resolution. No conforming allocation or command-visible limit has been decided.

Impact: A lane can implement the prescribed Stage 3 and pass its prescribed oversized-set check while losing a legal accepted mapping on every cold boot.

Required change: Gate Stage 3 implementation/release on #501's conforming decision, or explicitly restrict and freeze the stage's authorized scope until that decision is made. Update the allocation, capacity checks and protocol consequences together. Retain pending-and-skip as failure containment if useful, without counting it as fulfilled persistence.

Verification: Save and decode the maximum legal accepted set and the boundary/one-over-capacity cases, prove cleared-first restore, and grade any command refusal required by the chosen capacity policy. #501 remains open under these lenses.

[R217] MINOR Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:116 - F5: The evidence runner does not fail its process verdict

Requirement/evidence: The page says the runner refuses success unless the required controls fail. In `run.py:1098` main calls `report(allres)` and returns 0. `report` counts unexpected results and surviving mutants, prints `verdict failures N`, then returns normally even when N is nonzero.

Executed process-verdict control: supplied the healthy baseline executable under M01's expected build name in separate scratch and invoked the actual runner main for that mutant. It printed **`MUTANT M01_taint_ignored: SURVIVED`**, **`SUMMARY runs 1, checks 7, verdict failures 1`**, and returned **0**. This deliberately constructed survivor tests verdict propagation; it is not a claim that the published M01 mutation survived.

Impact: An exit-zero command record can coexist with a surviving mutant or failed baseline property. This does not invalidate the named results independently inspected in this review, but the process exit status cannot serve as their gate.

Required change: Propagate a nonzero verdict-failure count to the runner's exit status, and qualify the current success/refusal claim until that is done.

Verification: A deliberately surviving mutant, a failed baseline check and an absent required tracked control must each produce the expected diagnostic and a nonzero process exit. The healthy run must still exit zero.

Contract decisions and limits examined:

- **Live-write trigger:** I support replacing mark-driven persistence with accepted live-write triggers in principle. The actual SET_NAME and map microprograms put their marks after the write, and a class-1 mark alone does not identify format versus offset. O1 remains the sole sequential control-face master; this writer is a second manager behind the one device-face port, requiring the separate arbiter. The grant-cycle busy term is meaningful and its targeted mutant was detected. This is not acceptance of the complete contract while F1-F4 remain open. Amend the accepted mark-based wording, F07.9 and affected public acceptance criteria explicitly when the decision is adopted; do not silently waive them.
- **Clear/taint:** Inspected the per-record group-and-index match, set-over-clear priority, fresh latch after retry, taint through the write, and the relay from pending to backend dirty before acknowledgement. Focused runs cover repeated changes, same-edge completion, other-record changes, write errors and reset/power cuts before and after acknowledgement. Retry exhaustion additionally clears pending under a sticky alarm; that exception is present in the equations even though rule 4's prose says "only" successful write.
- **Persistent groups and ownership:** Checked selectors 0-5, formats/maps coupling, the descriptor image/heal walk before names, empty names, record IDs/lengths and the existing state/edit/gather interfaces. Lock and controller registration have no record or trigger; Identify selector 7 is excluded. Started/stopped remains in the binding record. SUID/MCR remain allocated but unimplemented, not silently credited as persistent. Concrete processor, parent glue and firmware responsibilities are stated in T1-T4.
- **#502:** The page honestly records the live-write-to-mark status window and proposes its removal in stages 2/3; the tracked controls reproduce it. Filing #502 is not closure. Earlier stages cannot claim that all pending-status gaps are fixed, and actual microprogram/glue validation remains required for its closure.
- **Cost:** Inspected the immutable OOC recipe, its accounting/calibration and the 1x1/8x8 rows: writer plus arbiter 2,312 LUT/802 FF and 2,925 LUT/927 FF, respectively, with no BRAM in those prototypes. Alternative (a) is a replication estimate; (c) is a fabric proxy excluding firmware. These are not integrated bounds. The atomic C++ edit model, synthetic nonempty reset maps, more permissive modeled output-format support, omitted real microprogram timing and omitted product map-read timing limit the claimed integration evidence. No silicon, timing-closure or full implementation result is inferred.

Commands and independently observed results:

All execution used CPUs 64-79, one build at a time with at most eight jobs, explicit private `$D3_OUT` and `$OOC_OUT` beneath the review scratch directory, and temporary outputs beneath that directory. The evidence was fetched from the public branch into a disposable detached checkout. Its tracked files were never edited; fault stimuli were made in a separate harness copy.

```text
git status --porcelain=v1
git rev-parse HEAD
git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence
git merge-base --is-ancestor 07294a76e833f1831d9fcbceb8123b8380c4ae76 d0256846dd0138e727386ae42e43710c332f2a23
git submodule status --recursive
git submodule foreach --recursive "git status --porcelain=v1"
```

Initial and completion checks matched: page head `d0256846dd0138e727386ae42e43710c332f2a23`; live dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor of the page; evidence checkout `a21b165ac1c671d10cba7255beaf75cea0f81d18`. Initialized pins: processor `424c688fa2205b934a7689a58f2aa766420f2326`, gPTP `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external submodule stayed uninitialized at its recorded pin. Direct Git-blob hashing also matched every tracked file in both superprojects and all three initialized submodules. The candidate initially contained no untracked files; REVIEW.md is the sole review output added to it.

The focused driver imported the immutable `run.py`, called `prep_shape`, then `do_build(..., jobs=8)` and `execute` sequentially for base-1x1, base-8x8, tracked-1x1, and mutants M01/M03/M05/M13/M16/A01/G02. It redirected `report` to scratch to preserve committed results. **10 builds, 101 runs, 635 checks, zero unexpected verdict failures**; all seven selected mutants detected by their named checks, K15's collision reached at g3, and the stale-store control behaved as required. Available command-record digests: 38 matched; the listed empty `ooc/abc.history` is absent from the immutable checkout. The other 17 mutants were inspected in the committed source/results, not independently rebuilt.

Independent probes used the same public `crafted`, `run_case` and `grade_run` helpers. Reproduction stimuli:

```text
F1: V11's ordinary slot; arm read_fault(0x80, 24, -1) only after
    evlog.ops contains two completed READ operations for record 0x80.
    Compare with the original fault armed before boot.
F2: Same slot; the first accepted backend memory read while own_o=1
    returns after 3,500,000 cycles instead of 2. Run host_boot(),
    inspect status at return, then idle another 600 ms and inspect again.
F3: V3; crafted output-map record 0x70 uses map_bytes([(index,0,0,0)],17)
    for index 0x0100 and 0xff00; all other records remain erased.
```

F1 and F3 fail the existing named graders on the unchanged prototype; F2 violates the explicit enable ordering. These are independent counterexamples, not planted implementation mutants or failed builds.

The following synchronous documentation/record-space checks all exited 0:

```sh
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_solution_docs.py
python3 -B scripts/check_feature_status.py
python3 -B scripts/check_submodule_docs.py
python3 -B docs/traceability/gen_module_matrix.py --check
python3 -B scripts/gen_toc.py --verify-anchors
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_archive.py
python3 -B scripts/check_hygiene.py --check
python3 -B scripts/check_em_dash.py --base 07294a76e833f1831d9fcbceb8123b8380c4ae76
python3 -B scripts/check_nvm_record_space.py
python3 -B scripts/check_nvm_record_space.py --self-test
```

Omissions: no full milan_dp or exhaustive RTL regression for this docs-only diff; no new OOC synthesis, Vivado, hardware, Docker/act, hosted-CI polling, privilege use, subagents, push or public write. No shared Vivado resource was used or lock required. The existing OOC recipes/results were inspected, not independently remeasured. No claim is made for silicon persistence, every record's integration wiring, actual microprogram timing, or a complete external Tests/Docs review.

Reviewer-owned coverage ledger. None of the assigned lenses is clean, so no per-lens PASS or covering round is banked. Tests and Docs also have the findings above and are not cleared by the passing mechanical gates.

| Lens | Covering round | Exact page head examined |
|---|---|---|
| Conformance | OPEN; R217-r1 findings F1-F4 | d0256846dd0138e727386ae42e43710c332f2a23 |
| RTL | OPEN; R217-r1 findings F1-F4 | d0256846dd0138e727386ae42e43710c332f2a23 |
| Robustness | OPEN; R217-r1 findings F1-F4 | d0256846dd0138e727386ae42e43710c332f2a23 |

This is a reviewer-owned local ledger for publication or explicit reviewer acceptance; no public publication was performed. Deferred issues do not close these findings. A revised contract and corrected executable evidence require re-review at their new exact heads.

R217 FINISHED
