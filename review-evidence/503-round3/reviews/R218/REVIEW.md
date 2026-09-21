[R218] NEGATIVE - exact head ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4

Independent external contract review of PR #503, issue #500, round R218/r3. Assigned lenses applied: **Docs first, then Tests**, followed by both across the corrected proposal. No previous clean coverage was banked. The finding below also applies to Conformance, RTL and Robustness; this review does not claim complete coverage of those other assignments.

The immutable full evidence reproduces exactly, including its 65 named mutant kills and eight process controls. The recurring-header, output-format and T8 contradictions have substantive corrections. However, the stage-1 contract still defers a descriptor recovery mechanism that its own acceptance requires. The complete prototype includes that mechanism, masking the staging gap. Both assigned lenses remain open.

This verdict concerns the Proposed contract and its evidence. It grants no product implementation approval, silicon validation, release approval or merge authorization.

Public authorities reconstructed: [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), [issue #70](https://github.com/kebag-logic/milan-fpga/issues/70), REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, docs/README.md, the accepted SAVED_STATE_SNAPSHOT_OWNERSHIP and SAVED_STATE_FASTCONNECT contracts, pinned processor F07.8/F07.9, public issues #501/#502 and processor issues #15/#20. Read the two round-two reviews ([R217](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5265143219), [R218](https://github.com/kebag-logic/milan-fpga/pull/503#pullrequestreview-5265158417)), their [verbatim reports, fault sources and observations](https://github.com/kebag-logic/milan-fpga/tree/7d9da8773c8baec0f705b08cea8b9e04d8c00b27/review-evidence/503-round2), the [corrected public response and receipts](https://github.com/kebag-logic/milan-fpga/tree/d5899ee6aa9194dfe786777c7092074c10fffd8a/review-evidence/503-round3/author), the [integration decision](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758659924) and final [manager REVIEW READY](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5760377435). The archived review bodies match their public review bodies. No private handoff, scratchpad, management receipt or transcript was read.

Artifact notation:

- `P` = [SAVED_STATE_MATERIALIZATION.md](https://github.com/kebag-logic/milan-fpga/blob/ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4/docs/design/SAVED_STATE_MATERIALIZATION.md), at the integrated candidate under review.
- `E` = [proposal-evidence](https://github.com/kebag-logic/milan-fpga/tree/fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293/design-evidence/500-materialization/proposal-evidence).
- `T` = [ticket drafts T1-T9](https://github.com/kebag-logic/milan-fpga/tree/fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293/design-evidence/500-materialization/tickets).
- `E`, `T`, the command/digest receipt and adapted reviewer probes were examined at immutable public commit `fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293`, fetched into a fresh disposable checkout. Processor citations refer to pin `424c688fa2205b934a7689a58f2aa766420f2326`.

[R218] MAJOR Conformance, RTL, Robustness, Tests, Docs - P:383,1287; T/T1-processor-stage1-dynamic-state-writer.md:81,99; T/T9-processor-descriptor-memory-response-isolation.md, Acceptance - R3-F1: stage 1 defers descriptor recovery needed for its finite-timeout acceptance

Requirement/evidence: T1 resets only `KL_aecp_dyn_state` on a pass-1 abort, waits for descriptor debt, then issues LOCATE to prove the image. Its item 7 explicitly assigns the descriptor-store rollback owner to T2. P's interface table and stage table make the same division; T2 introduces the descriptor reset/re-walk. Yet T1's descriptor-fault and recovery acceptance, and prerequisite T9's acceptance, require the store's own watchdog followed by a finite 5,000- or 16,000-cycle late burst to recover to proven defaults and command service. T9 adds the debt guard, but explicitly leaves the store's watchdog re-arm defect unchanged.

At the pinned `protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:938,959`, a response timeout leaves `tmo_r` at its limit. The next fetch errors immediately. Waiting for the outstanding burst alone does not re-arm that state. The complete prototype resets the descriptor store on rollback and therefore passes; the specified stage-1 reset scope does not provide that recovery.

Independent six-case reproduction used only stage-1 saved records: configuration `0x00 = 0000`, clock source `0x0a = 0001`, and offset `0x50 = 0016e360`. Every other record, including names and maps, was erased. Run the published V21, V21b and V20b scenarios against the freshly built baseline and the existing `R03_rollback_skips_desc_store` binary. That mutant changes exactly the relevant reset connection; it is used here as a controlled omission, not as evidence that the unchanged complete prototype is defective. Both builds retain S1, S2 and S3. All six scenarios completed with process exit 0; their assertion outcomes differ:

| Case | Complete prototype | Descriptor reset omitted as in stage-1 scope |
|---|---|---|
| V21: first post-application descriptor fetch delayed 5,000 cycles | DEFAULTS; done/fail/rolled-back = 1/1/1; terminal 8109; enable 8123 | CLOSED; done/fail/rolled-back = 0/1/0; terminal 7462; enable never |
| V21b: same, 16,000 cycles | DEFAULTS; terminal 19109; enable 19118 | CLOSED; terminal 18462; enable never |
| V20b: one descriptor error, then healthy memory | DEFAULTS; terminal 3107; enable 3113 | DEFAULTS; terminal 2758; enable 2768 |

For V21, request acceptance is cycle 2442, first late beat 7443, abort 6542, and rollback reset release 7454 in both builds. For V21b the corresponding late beat and release are 18443 and 18454. Debt has drained before either failed re-LOCATE. All default rows match in all six cases. The failure is unnecessary permanent closure and loss of command service after a finite recovered dependency, not an enabled partial restore. The ordinary-error control passes without the reset, distinguishing the subordinate watchdog case from generic failure handling.

Impact: an implementation lane following the explicit stage-1 owner split cannot meet the promised finite-timeout recovery with the demonstrated mechanism. The full model's later-stage descriptor reset is being used as stage-1 evidence. The allowance to enter CLOSED when an image cannot be proved is necessary containment, but it does not satisfy T9's separate positive requirement to recover to defaults after these finite delays. Recording the watchdog quirk under UNRESOLVED 14 does not reconcile these incompatible stage obligations.

Required change: make the descriptor recovery needed after its watchdog an explicit prerequisite of stage 1, with ownership consistent across P, T1, T2 and T9. It can be the demonstrated scoped descriptor reset/re-walk or another proved mechanism; merely draining debt is insufficient. Preserve hard-reset-only ownership of the guard's debt. Add stage-1-only evidence so the finite-delay acceptance does not depend on name materialization or a later owner's reset. Do not weaken the promised recovery to excuse this omission.

Verification: repeat the selector-only slot above with delays below the store watchdog, 5,000 and 16,000 cycles, a delay past the D3 recovery deadline, and the one-error control. Finite recoverable cases must reach proven DEFAULTS with command service; an unprovable image or excessive debt must remain CLOSED. Removing the stage-1 recovery mechanism must fail its own completed-scenario check. Check late beats across reset/re-walk and retain the existing DG01/DG02 tests. This is a remaining staging aspect of R217 R2-F2; it does not negate the corrected complete-prototype fault classification.

Prior-finding dispositions preserve original severities and every original lens label. “Corrected” below means the identified contract/evidence defect is corrected at this page and evidence head; it does not mean an unimplemented product feature exists.

| Prior finding | Original severity and lenses | Disposition at this head and evidence |
|---|---|---|
| R217 R2-F1 / R218 F1: repeated and balanced header failures | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Corrected in the proposal/model.** S1 distinguishes DEVICE from a whole UNFRAMED header; S1/S3 are stage-1 prerequisites. H1-H8, V18/V18b/V18c and genuine erased V10 reproduce. C01/C02/C03 and X01/X02 fail their named checks; B02/B04 independently distinguish binding failure from absence. Per-record identity alone is expressly rejected. The page no longer permits relying on the pinned port's ambiguous error. |
| R217 R2-F2: descriptor errors, watchdog and initial image failure | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Partially corrected; OPEN through R3-F1.** The complete prototype now aborts on fetch errors (cause 6), holds response debt across rollback, and keeps an unproven initial image CLOSED (cause 7). V20/V20b/V20c/V20d, V21/V21b/V21c/V21d, V22/V22b, V23 and V17 reproduce; V2b remains a distinct invalid-value refusal. DF01-DF03, IMG01, DG01/DG02 are killed. The staged descriptor-reset dependency remains inconsistent as reproduced above. |
| R217 R2-F3: unbounded binding walk and incompatible recovery promise | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Identified read-silence defect corrected in the proposal/model.** S3 bounds the binding read phase; either manager's abandoned read is drained without timed port release. W13/W13b/W13c/W15/W16/W14 and B01/B03/G05 discriminate terminal ordering, late containment and command service. Independent second-record faults suppress even the previously read binding's preload. The listener preload phase is explicitly outside the modeled deadline; integrated listener acceptance remains owed. |
| R218 F6: synthetic output judge presented as product behavior | MINOR; Tests, Docs | **Corrected.** The synthetic narrowing cases are labeled, including all 50 affected result cases. V1s_a/b/c use the transcribed shipping predicate: declared eight-channel output accepted, narrower output rejected as SET and saved replay. Value plus valid distinguishes replay even at the default value. Format trigger/replay mutants must fail both named synthetic and shipping controls, and the partial-kill process control rejects a mutant failing only one. |
| R218 F7: T8 promises reuse after permanent silence | MINOR; Docs | **Corrected.** Revised T8 separates finite late completion from indefinite physical-port quarantine and demonstrates commands on defaults. Processor issue #15 criterion 2 remains undelivered and its amendment unaccepted; T8 neither closes nor amends it. T8/T9 are proposed tickets to be filed after contract acceptance, before implementation, not completed prerequisites. |
| R218 F2 / R217 first-round F2: firmware timeout releases enable | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Original mechanism corrected and retained.** Hardware owns dispatch from reset and releases enable only at the terminal. W11/W12, W14, V17, K19, G05/R05/O01 and drain mutants reproduce. Late replies cannot resume restore after service starts. This does not clear R3-F1's separate finite descriptor recovery gap. |
| R218 F3: runner accepts survivors/crashes | MAJOR; Tests, Docs | **Corrected and retained.** Full/focused distinction, planned-case completeness, completed-scenario named killers, expected baseline failures, vacuity outcomes and actual CLI statuses are enforced. Eight process controls reproduced with diagnostics and exits `1,1,1,1,1,2,1,2`. |
| R218 F4: configuration replay deletion survives | MAJOR; Conformance, Tests, Docs | **Corrected and retained.** `RPL_cfg` fails `(0,0)` versus `(0,1)`; nine group-specific triggers and nine replays, both format and map directions, exact counts, unsaved defaults and cleared-first observations remain discriminating. Rate replay uses explicitly synthetic 1x1r2. |
| R218 F5: stages permit capacity/status defects | MAJOR; Conformance, Robustness, Tests, Docs | **Original release-contract defect corrected; product issues remain OPEN.** #501 blocks stage-3 implementation until a conforming allocation or accepted limit is decided; #502 must land before any stage is shippable. K16 is containment only. R3-F1 is an additional descriptor dependency, not a claim these issues are fixed. |
| R217 first-round F3: padding aliases/holes | MAJOR; Conformance, RTL, Robustness, Tests, Docs | **Correction retained.** V3a-V3g distinguish full eight-byte FF padding, alias indices, malformed tails, holes, out-of-range entries and empty sets before edits. P01/P02 fail their named verdict/edit checks. |
| R217 first-round F4: capacity/status staging | MAJOR; Conformance, RTL, Robustness, Docs | **Original release-contract correction retained**, with #501/#502 still open and the restrictions above. |
| R217 first-round F5: process success used as verdict | MINOR; Tests, Docs | **Correction retained**, by the same independently reproduced runner controls; its original MINOR severity is preserved separately from R218 F3. |

These dispositions do not assemble the other reviewer's covering ledger. The round-two reports' common first-round F1 history is carried by the recurring-header row; no prior clean lens is imported.

I independently support the proposed live-write amendment **in principle**, with the reconciliation P section 15.1 specifies. Accepted writes carry group/index identity and cover the interval before the later notification mark. The replacement acceptance is stronger at the group boundary: nine independently deleted triggers and replays, both format/map directions, configuration validity and IDENTIFY exclusion. Adoption still requires the public contract decision and reconciliation of FASTCONNECT sections 12.2/16, SNAPSHOT_OWNERSHIP D2 and processor F07.9 before implementation. This negative overall verdict does not silently amend those accepted rules. Unsettled debounce, product-clock deadline and value-rule implementation choices must also be settled before an affected implementation lane is Ready.

O1 and O3 remain separate. O1 reserves the sequential control-face strobe/base/length/map tuple writer to firmware. The additional arbitrated device-face producer and drain do not acquire that authority. O3 orders restore activity and entity enable. The new port cause, binding deadline and descriptor debt guard are explicitly proposed seams, not unchanged product modules. `run.py` checks amended sources against declared edits to the pinned originals. S1 terminal cause propagation, S2 accepted-request/terminal-response handshakes and hard-reset ownership, S3 read deadline, arbiter drain ownership and hardware enable gate were examined against the pinned interfaces. R3-F1 is the remaining mismatch in the stated stage ownership.

Whole-proposal Tests/Docs checks and limits:

- Cross-checked F07.8 allocation/framing, generated record space, selectors, field widths, offsets, formats, maps and name ordinals with the real owners and generated inputs. The 1x1 shape has 53 total / 49 D3 records and 38 names; 8x8 has 156 / 145 and 99 names. The 8x8 output-map allocation remains nine entries per port against 72 stream channels. Permanent pending is not a capacity solution.
- K1-K19 cover same-record taint, set-over-clear on acknowledgment, another record/group during a write, repeated changes, retry/alarm, program/latch ordering, binding grant collision, reset ownership and cuts before/after capture and acknowledgment. The grant-collision premise is reached. This does not repeat the entire accepted snapshot/ACK proof.
- The tracked product build has seven expected failures and four required passes. M13's stale-store control distinguishes naive readback from cleared-first proof. Each of the 65 mutants must fail every named check in a completed scenario; a crash or one-of-two partial kill cannot substitute. No published mutant survived the fresh full run. Those results cover the full prototype, not the missing stage-1 configuration.
- Synthetic 96 kHz, broader output-format ordering stimuli and nonempty reset-map sets remain explicitly qualified. The separate shipping output control is product-legal. The 8x8 input-map shape has no input clusters; its group control is at 1x1. Configuration validity proves the sole legal index, not multi-configuration support.
- IDENTIFY exclusion is executable. Lock and controller-registry exclusion is structural here, with integrated reset tests still owed. SUID/MCR have allocated records but no source and remain erased. Started/stopped belongs to binding persistence. The model does not prove all nine groups on silicon.
- Reviewed all 20 OOC rows, both recipes, proxy sources, parameter sets and arithmetic. The writer/arbiter estimates are 2,377 LUT / 888 FF at 1x1 and 3,116 / 1,109 at 8x8. Including S1/S2/S3 gives 2,493 / 925 and 3,228 / 1,146, zero RAMB36/DSP for those increments. S2 contributes 5 LUT/1 FF; S1 adds 4/2; the binding seam adds 107/34 and 103/34. These are differences of OOC syntheses, not integrated bounds. Candidate (a) excludes its arbiter; candidate (c) excludes firmware. The old 30-name backend calibration is 1,030 LUT / 468 FF, not the obsolete accepted-page row. No fresh synthesis is claimed here.
- Real microcode timing, product map phases 0-5 and GET hold, listener preload acceptance, the actual CDC/bridge timing and poison path, feature-disabled boot and board timing remain implementation evidence. Firmware changes 1 and 3 are compiled substitutions; change 2 is derived, not executed. The model's guard property does not validate the entire memory path. OOC measurements and model cycles do not establish placed area or a universally safe 20 ms product deadline. Issue #70's binding cold-cycle evidence does not establish items 1-8, started/controller coverage or soak.

Independent adjacent-transition work used an isolated copy of the stimulus harness, unchanged prototype RTL/firmware and the fresh V1a slots. Twenty-two completed scenarios were checked with 140 terminal-specific assertions, all satisfied: first-beat delays around 4093-4097 cycles, delays around the recovery deadline, initial-image delays, errors/silence on the second binding record, replies around its deadline, and mid-burst descriptor errors/stalls. Checks covered full default rows where promised, cause versus invalid-value refusal, image proof before enable, CLOSED holding dispatch/enable, no late restore writes, suppression of earlier binding preloads on a failed walk, and subsequent command/persistence behavior. CLOSED cases were checked for containment, not incorrectly required to enable. A silent second binding read reached its terminal at 20148, D3 terminal at 40807, enable at 40823; GET returned default value/valid and the later SET stayed pending with the port quarantined. The separate six-case stage comparison above exposed R3-F1. These are focused reviewer probes, not another full build/case set.

Executed commands/results use variables for reviewer-owned paths, with D3_OUT, OOC_OUT and TMPDIR explicitly set under the authorized scratch filesystem. The output tree was initially empty. A byte-identical sibling copy of the runner/evidence tree, at the same repository-relative depth, was used because a full run writes its results beside itself; tracked immutable evidence was preserved.

```sh
rtk proxy git status --porcelain=v1
rtk proxy git rev-parse HEAD
rtk proxy git submodule status
rtk proxy git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence
rtk proxy git merge-base --is-ancestor 2d8fd62fd986ea2d6a87d284e144f023034c0944 HEAD
rtk proxy git -C "$EVIDENCE_ROOT" fetch origin 500-design-evidence
rtk proxy git -C "$EVIDENCE_ROOT" checkout --detach fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293
rtk proxy git -C "$EVIDENCE_ROOT" submodule update --init --jobs 8 \
  third_party/verilog-axis protocol-processor gptp-processor

export TMPDIR="$SCRATCH/tmp" D3_OUT="$SCRATCH/d3" OOC_OUT="$SCRATCH/ooc"
rtk proxy taskset -c 80-95 python3 -B run.py prep
rtk proxy taskset -c 80-95 python3 -B run.py build --pool 1 --jobs 8
rtk proxy taskset -c 80-95 python3 -B run.py run --pool 8
rtk proxy taskset -c 80-95 python3 -B run.py controls --pool 8
```

All four evidence actions exited 0. Full result: `SUMMARY FULL builds 69, runs 312, checks 3462, verdict failures 0`. Fresh results match both published files byte-for-byte: results.txt SHA-256 `53da3c4e065d17904c5f18425521eec59650fad7851918657d1d4fcbf7ef17fa`; results.json SHA-256 `4e35e4f3b922bec470fb66c316319f25989afe6d66761e5e6897d4af248ba82a`. The process controls checked their required diagnostics as well as their exit statuses. Builds used CPUs 80-95 and at most eight jobs, with one build pool member. Each dependent execution waited for its predecessor; no background job or Docker/act was used.

R3-F1 can be reproduced after that build using the immutable runner's public Python API. Set its D3_OUT to a fresh probe directory before importing it; retain the full-run binaries separately as `FULL_OUT`. The following is the substantive probe, with `m` the imported immutable `run.py` module:

```python
s = m.prep_shape("1x1")
slots = m.crafted(s, "stage1-only", {
    0x00: bytes.fromhex("0000"),
    0x0a: bytes.fromhex("0001"),
    0x50: (1500000).to_bytes(4, "big"),
})
for name in ("base-1x1", "mut-R03_rollback_skips_desc_store"):
    b = m.Build(name, "1x1", binary=FULL_OUT / "build" / name / "obj/d3sim")
    for case in ("V21_desc_late_after_apply",
                 "V21b_desc_debt_outlasts_the_store",
                 "V20b_desc_error_once_after_apply"):
        r = m.run_case(b, s, case, slots=slots)
        g = m.Grade(r, s)
        assert r.rc == 0 and r.done
        print(name, case, r.obs["terminal"], g.boot(),
              g.mismatches(r.snaps["terminal"], {}))
```

Inspect done/fail/rolled-back/closed, command ownership and enable against the acceptance above. Successful process completion alone is not a passing recovery check. This probe requires no new RTL build and no product change.

The following 26 focused gates ran synchronously on the exact candidate as `rtk proxy taskset -c 80-95 python3 -B <command>`; every gate exited 0. `git diff --check 2d8fd62fd986ea2d6a87d284e144f023034c0944 HEAD` also passed.

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
scripts/check_em_dash.py --base 2d8fd62fd986ea2d6a87d284e144f023034c0944
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

Initial and completion identity checks agree: candidate and remote PR head `ab0fb23fd1a6376213a9d0e5aa61f4751ece00e4`; live remote dev `2d8fd62fd986ea2d6a87d284e144f023034c0944`, verified ancestor of the candidate; evidence branch `fc2e3a6211bdbca3c41718eb6e1b4b4c2a128293`. The four-file diff is documentation only. Required submodule pins in both checkouts are protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`; unused `external` remains uninitialized at `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`.

Independently verified all 59 published receipt digests and all 15 examined repository inputs against the current candidate: 14 inputs are byte-identical; `nvm_shape.py` differs in commentary only, with an identical Python syntax tree. The four candidate documentation blobs match the public integration receipt. Thus the earlier-base executable inputs were checked explicitly, not presumed current from an old green report. The historical pre-integration page commit `e67a586f` was unavailable to direct Git fetch; its receipt is not used as a substitute for reviewing the supplied integrated candidate. With Git replacement objects disabled, independent blob hashing checked 850 candidate blobs, 894 evidence blobs and 539 submodule blobs per checkout, with zero mismatches. Initial candidate tree was clean; all tracked sources remain byte-exact. Only the requested REVIEW.md is added to the candidate checkout.

Omissions: no product edits, full product native regression/lint/portability bar, full milan_dp rerun, actual AECP integration run, fresh OOC/calibration synthesis, Vivado, placement, hardware or power-cycle soak. The OOC recipe/rows showed no assigned-lens concern requiring another synthesis cell, so no Vivado lock was needed or acquired. The 15 archived reviewer-probe outputs/adaptations were inspected; they were not separately rerun as an additional historical probe bank. Their corresponding published cases were included in the full run, and adjacent stimuli were independently extended as described above. No privilege, subagents, push, public write or hosted-CI polling. The manager's deferred full native bar remains mandatory before ready/merge; this review does not waive it or claim complete CI evidence.

Reviewer-owned clean covering ledger: **no entries**. Tests and Docs remain open under R3-F1 at the exact page head above; unresolved MAJOR findings cannot bank either lens. No artifact-based per-lens PASS is asserted for a dirty assigned lens. Other reviewers' lenses are not banked here.

| Lens | Covering round | Exact page head |
|---|---|---|

R218 FINISHED
