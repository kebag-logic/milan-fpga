[R217] NEGATIVE - exact head 40d14d92bfcf3823ed7b227537630f444b1f4f73

Independent internal contract review of PR #503 / issue #500, round R217-r2. Assigned lenses applied: **RTL first, then Conformance and Robustness**. None had clean coverage from round one. Tests and Docs were also applied to the executable evidence and claims implicated below; this does not substitute for the independent external review. This verdict concerns the Proposed contract only. It grants no product implementation, silicon, release or merge approval.

The original payload-error rollback, early-enable, malformed-map and process-verdict reproductions have substantial corrections. The contract still permits transport failures to end as a successful partial restore, including a descriptor-memory failure outside the disclosed NVM-header limitation. Its stage prerequisites also leave the binding-walk availability defect open. No assigned lens is clean.

Public authority reconstructed from [issue #500](https://github.com/kebag-logic/milan-fpga/issues/500), its [O1/O3 clarification](https://github.com/kebag-logic/milan-fpga/issues/500#issuecomment-5755853228), issue #70, REQUIREMENTS.md, CONTRIBUTING.md, AGENTS.md, the accepted SAVED_STATE_SNAPSHOT_OWNERSHIP and SAVED_STATE_FASTCONNECT contracts, and the pinned processor's F07.8/F07.9 and relevant RTL. Read both [verbatim round-one reviews and reproductions](https://github.com/kebag-logic/milan-fpga/tree/597bc777c652f709634e5c14afef6d853fc5b713/review-evidence/503-round1), the [public response](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758107685), [review-ready claim](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758113383), and [manager validation/scheduling](https://github.com/kebag-logic/milan-fpga/pull/503#issuecomment-5758113695). Also read open issues #501/#502 and processor issues #15/#61/#63/#83. No author checkout, private handoff, management receipt or transcript was used.

Page references below mean `docs/design/SAVED_STATE_MATERIALIZATION.md` at the exact head above. Evidence references beginning `E/` mean `design-evidence/500-materialization/proposal-evidence/` in immutable public commit [ca8cb5943f885c22aec397ff75059e2d4791f4fb](https://github.com/kebag-logic/milan-fpga/tree/ca8cb5943f885c22aec397ff75059e2d4791f4fb/design-evidence/500-materialization). Ticket references mean its sibling `tickets/` directory at that same commit, including the corrected T3. Processor references mean pin `424c688fa2205b934a7689a58f2aa766420f2326`.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:835 - R2-F1: Header errors still produce a successful partial restore; equal counts do not prove pass agreement

Requirement/evidence: Section 8.6 and section 13 promise a complete restore or defaults with failure for a transport failure in either pass. Section 15 item 5 discloses a counterexample but neither resolves it nor makes the needed interface change a prerequisite. The pinned `KL_pp_nvm_port.sv:284` and `:302` collapse a device error during header collection and an unframed header into the same zero-byte error. `E/prototype/KL_aecp_nvm_writer.proto.sv:775` treats that outcome as blank. Its comparison at line 739 checks only the two counts, not which records each pass read.

Independent execution kept every RTL module and the firmware unchanged, starting from V1a's genuinely committed 1x1 slots:

| Fault stimulus | Applied / refused / blank | Offset 0 value, valid | Restore fail / rolled back | Entity |
|---|---|---|---|---|
| Control, no fault | 10 / 0 / 39 | 1500000, 1 | 0 / 0 | enabled |
| `read_fault(0x50, 0, -1)` in both passes | 9 / 0 / 40 | 0, 0 | 0 / 0 | enabled at 7538 |
| `read_fault(0x30, 0, -1, 0)` and `read_fault(0x50, 0, -1, 1)` | 9 / 0 / 40 | 0, 0 | 0 / 0 | enabled at 7523 |
| Header error on 0x50 in pass 0 only | 10 / 0 / 39, before rollback | 0, 0 after rollback | 1 / 1, cause 5 | enabled after defaults |

The second failing row needs no error recurring at the same address: different missing records balance the counters. In both failures, other saved rows and names remain applied and the status is `done=1, fail=0, backed=1, dirty=0, stale=0, pend=0`. The immutable slot is intact. The original second-pass payload fault now rolls back; that narrower correction does not establish the advertised transaction property.

Impact: A readable, valid saved value is silently replaced by its default while the entity reports successful restoration of a mixture. This is a blocking contract weakness even though the same-header case is disclosed. A deferred T8 does not satisfy the transaction guarantee.

Required change: Make reliable transport-error classification a prerequisite of the first affected D3 stage, with concrete port/writer integration semantics. A count comparison alone cannot resolve this ambiguity; even record-identity comparison cannot identify an error repeated in both passes. Every actual transport failure must reach the declared failure/default or closed outcome. Align sections 3/6/8/13/15 and T1/T8 with that prerequisite.

Verification: Retain payload faults in both passes; add recurring header errors, errors at different record IDs balancing the counts, and single-pass header errors. Require a failure verdict and the declared whole-walk recovery, with valid blank/unframed records still exercising the separately specified refusal path. No partial restore may be classified COMPLETE because two counts happen to match.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:426 - R2-F2: Descriptor-memory errors and timeouts bypass the restore transaction

Requirement/evidence: Restore depends on the descriptor store for the image walk and the sampling-rate/clock-source legality checks. The pinned `KL_aecp_desc_store.sv:960` returns a state-bus error for a failed descriptor fetch; line 980 does the same for its 4,096-cycle timeout. The proposed writer's `R_AUX` at `E/prototype/KL_aecp_nvm_writer.proto.sv:830` counts that error as a refused value and continues, without aborting. Its initial `R_IMGW` at line 729 also continues with `img_bad_r`, allowing FINISH/COMPLETE without a validated image. The D3 20,000-cycle watchdog cannot contain a shorter subordinate timeout that has already returned an error treated as normal progress.

Independent adjacent probes used the same committed slots and unchanged RTL:

- After configuration replay first increments `rs_app`, make the descriptor memory return an error. The saved clock source 1 remains `(0, valid=0)`; nine other records apply, one is refused, and restore ends `done=1, fail=0, rolled_back=0`, with entity enable at cycle 6638.
- Delay the first descriptor-memory request after that application by 5,000 cycles. The actual pinned store times out at 4,096. The writer again reports nine applied, one refused, `fail=0`, and enables at 10733. This is a descriptor timeout, not the tested NVM read timeout.
- Fail descriptor reads from before boot. No image is validated: `desc_valid=0`, all ten framed saved records are refused, yet restore ends `done=1, fail=0, blank=0` and enables at 5003. This is not the CLOSED terminal promised when the default image cannot be proven after rollback.

Impact: A transient failure reading the rules is confused with a saved value failing those rules. A missing factory walk is also allowed to look like a successful restore. The value's validity was never established, and the claimed complete/default transaction does not cover all of its actual dependencies.

Required change: Specify error and timeout handling for descriptor/image/state-bus dependencies as part of the transaction. A valid saved value must not be refused merely because its descriptor fetch failed. Require proven defaults before enabling a failed restore; if the factory image cannot be validated, use an explicit failure/closed outcome. Define any new status or reset/response-isolation seams needed at the pinned descriptor interface and carry them into T1/T2/T4. T8's NVM-port change alone cannot fix this path.

Verification: Exercise a descriptor error and the store's own timeout after prior values have applied, initial image-walk failure, rollback-walk failure, and late descriptor responses around local reset/re-walk. Check all owners, the failure cause, enable ordering and subsequent command service. Keep valid-record/invalid-value tests separate from transport failures. The present V17 proves failure during the rollback walk only.

[R217] MAJOR Conformance, RTL, Robustness, Tests, Docs - docs/design/SAVED_STATE_MATERIALIZATION.md:1019 - R2-F3: The stages still permit an unbounded binding-walk hold, and T8 promises incompatible recovery

Requirement/evidence: The original F2 required bounded ownership and command service on the declared recovery path, including both walks. The accepted FASTCONNECT section 9.3 (`:1122`) requires continued AECP/SET service when persistence wedges; F07.9 carries bounded failure handling. Processor issue #15 explicitly records the silent-device wedge as an open defect. The new reset-owned dispatch gate makes a silent binding read hold the entity and all AECP dispatch indefinitely. Section 10 and T1/T4 expressly permit shipping without that dependency; they do not propose an accepted amendment to the availability contract.

Reproduced W13: `restore done 0, entity enabled 0, firmware asked at 3000074 and reported the timeout True, own 1, a GET answered None`. This is correctly described as fail-closed, and it fixes early enable. It does not close the availability/ownership part of F2 or establish bounded boot recovery. W1/W4/W7 separately reproduce a D3 default terminal with a permanently drained port and a later SET pending; that is containment, not restored persistence service.

T8 is internally contradictory: lines 27-32 require the untagged port to stay quarantined until the device terminates, explicitly forever for a permanently silent device; lines 43-45 then promise that such a device will stop holding the port. The pinned interface supplies no cancellation acknowledgement, transaction identity or independently specified device reset that makes the latter conclusion follow.

Impact: The proposed release contract allows a known unresolved service defect, while its follow-up ticket claims a recovery its own protocol cannot provide. Relocating the defect or printing a timeout does not resolve it. I do not accept indefinite pre-enable dispatch ownership as resolution of the prior finding.

Required change: Make bounded binding-walk failure/default containment an explicit prerequisite for an affected shippable stage, or obtain a separate authoritative change to that availability requirement before claiming conformance. Specify how binding replay and late responses are contained before releasing commands. Correct T8: retaining quarantine on a permanently failed device can be honest containment, but a claim of reusable port service needs a concrete cancellation/reset completion contract. Do not release untagged ownership merely because a timer expired.

Verification: Silence and responses immediately before/after the binding deadline; no late preload or restore write after enable; a truthful failure terminal and usable AECP after safe recovery. Check port quarantine and recovery separately, including a device that never terminates. A test that expects a GET never to answer proves fail-closed safety only.

**Round-one dispositions, preserving the original severities and labels.**

| Prior finding | Original severity and lenses | R217-r2 disposition at this head |
|---|---|---|
| R217 F1; R218 F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each reviewer | Original payload triggers corrected: first pass applies nothing; original second-pass injection leaves offset valid 0, all rows reset, failure 1, rollback 1. V11b/V12-V16 and selected rollback mutants corroborate both shapes. The general transaction finding remains OPEN under R2-F1/R2-F2. |
| R217 F2; R218 F2 | MAJOR; Conformance, RTL, Robustness, Tests, Docs, for each reviewer | Original early-enable counterexamples corrected. W11: D3 terminal 20781, enable 20798, response at 3500781 drained; no late restore write and the later SET persists. W12 similarly rolls back before enable. W2/W3/W5/W6 cover adjacent deadlines. Availability/dependency coverage remains OPEN under R2-F2/R2-F3. |
| R217 F3 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED for this proposal. Exact eight-byte padding and hole refusal are implemented in the prototype. V3a-V3g reproduce the requested aliases, malformed tails, holes, ordinary invalid index and valid empty set with exact counts/defaults. P01/P02 are independently detected. |
| R217 F4 | MAJOR; Conformance, RTL, Robustness, Docs | Contract prerequisite defect RESOLVED: section 10 and exact T1-T6 drafts consistently gate stage-three implementation/release on a conforming #501 decision, and every shippable stage on #502. This is a scope restriction, not resolution of #501/#502; both remain OPEN, and K16 remains containment-only. |
| R217 F5 | MINOR; Tests, Docs | RESOLVED. Actual CLI controls return required nonzero exits and diagnostics for survivors, failed baseline/control expectations, incomplete scenarios and missing builds. |
| R218 F3 | MAJOR; Tests, Docs | Response independently corroborated by all seven process controls, including the crashed mutant. Its original severity is unchanged; external disposition remains that reviewer's. |
| R218 F4 | MAJOR; Conformance, Tests, Docs | Response corroborated: every claimed group's value/valid or payload has a discriminating replay check; exact counts and all-row/default snapshots replace the weak totals. RPL_cfg and RPL_rate independently fail their specific checks; all nine trigger/replay deletion definitions and published diagnostics were inspected. External disposition remains that reviewer's. |
| R218 F5 | MAJOR; Conformance, Robustness, Tests, Docs | Same prerequisite correction as R217 F4 independently verified; neither underlying issue is closed. External disposition remains that reviewer's. |

**Other contract assessments.**

O1 is correctly limited to the sole sequential control-face master. The proposed writer and drain do not write the snapshot control tuple. O3 separately orders the binding walk, D3 restore and subsequent materialization. The manager-face arbiter retains ownership through completion/drain, gives binding priority at an idle tie, and covers the D3 grant cycle in binding busy. K13/K15 and A01 reproduce that load-bearing collision. The D3 enable gate and drain are concrete improvements; they are not evidence for the unresolved paths above.

The clear/taint design has meaningful group-and-index identity, fresh latching on retry, set priority on the completion edge, and a relay from pending to backend dirty before acknowledgement. K1-K19 and selected M01/M03/M05 controls cover repeated changes, multiword names, concurrent records, arbitration, retry, cuts inside debounce/write/before commit/after acknowledgement, and waiting commands. Rule 4 now explicitly includes give-up under a sticky alarm, matching the equations; that exception is not successful materialization. Existing snapshot identity/epoch and O2/O4 obligations remain inherited, not re-proved exhaustively here.

I support the **explicit live-write amendment in section 15 item 1** as the proposed trigger choice: accepted writes identify the record and eliminate the name/map mark tail; quiescent latching prevents saving an unfinished command. The replacement obligations cover nine groups, both format directions and both map directions separately, plus IDENTIFY exclusion. Adoption must be recorded and the accepted FASTCONNECT/D2/F07.9 wording and affected implementation acceptance contracts reconciled before landing that behavior. This negative overall verdict does not silently adopt or waive the existing wording.

Framing/allocation inspection covered F07.8 big-endian headers and CRC16, KLJ2 validation and erased spans, IDs, per-group payload widths, name ordinals and 64-byte names. The record-space gates pass, but do not resolve output-map representability: the actual output key in `milan_datapath.sv:4106` is stream/channel, so ten legal mappings still outgrow a nine-entry 8x8 record. The new stage restrictions honestly block that implementation. Empty names remain values, not erased records. Lock/registry have no trigger or record; IDENTIFY is excluded and K14 exercises it. Started/stopped stays with binding; allocated SUID/MCR records have no source and gain no persistence claim.

Persistent-group dependencies were traced through the actual dynamic store, descriptor store, engine state bus and dispatch, format gather face, parent edit/read faces, map reset owners, port and memory bridge. Names depend on a completed factory walk; rates and clock sources depend on successful descriptor reads; formats and maps depend on each other's accepted values. Resetting the relevant owners is a plausible rollback mechanism when its image proof succeeds. New soft resets, dispatch hold-off, enable gate and parent map reset are specified integration work, not existing product seams. The descriptor failure counterexamples prevent accepting their current failure contract as complete.

The evidence is not product timing. The map plane and microprograms are behavioral models; the edit model is atomic and the real map read has additional hold timing. Reset maps are synthetically nonempty; shipping maps reset empty. Also, the model accepts narrowed output formats, whereas the actual `milan_datapath.sv:4578` verdict accepts only each output's declared channel count. Those non-default output-format/coupling values are synthetic test stimuli, not product-legal SET evidence. The synthetic 1x1r2 rate list proves replay of 96000 but is not a shipped configuration. Configuration 0 replay is distinguished by its valid flag; no builder-emitted configuration makes index 1 legal. These limits do not excuse missing replay, and no product support is inferred from them.

Inspected both immutable OOC scripts, parameter rows, proxies, accounting and revised digests. The revised writer-plus-arbiter measurements are 2311 LUT / 862 FF at 1x1 and 2876 LUT / 987 FF at 8x8, zero BRAM/DSP in these prototypes. The added transaction/watchdog/drain mechanisms were remeasured in the published revision; the rows account for 60 additional flops. The replication alternative omits its arbiter; the firmware alternative omits firmware and integration cost. These are estimates, not integrated bounds. The 20 ms value is a per-wait no-progress proposal, not a whole-boot or successful-service deadline. Correcting the newly identified mechanisms can change area/latency and must update affected measurements before reusing these figures. No new OOC run was necessary to establish this verdict.

**Independent execution and results.**

All builds/runs used CPUs 64-79, one build pool, at most eight build jobs, and explicit private scratch paths under `/data` through `TMPDIR`, `D3_OUT` and `OOC_OUT`. Evidence was fetched from the public repository into a disposable detached checkout, with the three required submodules initialized. Focused output and reviewer fault-harness copies stayed outside tracked trees. Commands were run synchronously to completion; no background job remains.

```sh
git status --porcelain=v1
git rev-parse HEAD
git ls-remote origin refs/heads/dev refs/pull/503/head refs/heads/500-design-evidence
git merge-base --is-ancestor 07294a76e833f1831d9fcbceb8123b8380c4ae76 HEAD
git submodule status --recursive
git submodule foreach --recursive 'git status --porcelain=v1'

git clone --no-checkout https://github.com/kebag-logic/milan-fpga.git "$EVIDENCE_ROOT"
git -C "$EVIDENCE_ROOT" checkout --detach ca8cb5943f885c22aec397ff75059e2d4791f4fb
git -C "$EVIDENCE_ROOT" submodule update --init --jobs 8 \
  third_party/verilog-axis protocol-processor gptp-processor
```

From the public evidence directory, with the scratch variables set:

```sh
builds=(base-1x1 base-8x8 base-1x1r2 tracked-1x1
  mut-M01_taint_ignored mut-M03_clear_wins_same_edge
  mut-M05_latch_ignores_program mut-M13_restore_applies_nothing
  mut-A01_grant_cycle_not_busy mut-R01_no_rollback
  mut-R03_rollback_skips_desc_store mut-P01_padding_by_first_byte
  mut-P02_padding_holes_not_refused mut-G05_enable_not_released_by_restore
  mut-D01_abandoned_read_not_drained mut-RPL_cfg mut-RPL_rate)
taskset -c 64-79 python3 -u -B run.py build "${builds[@]}" --pool 1 --jobs 8
taskset -c 64-79 python3 -u -B run.py run "${builds[@]}" --pool 1
taskset -c 64-79 python3 -u -B run.py controls --pool 1
```

Observed: **17 builds, 175 runs, 1565 checks, zero unexpected verdict failures; all 13 selected mutants detected in completed runs. Seven of seven process controls passed**, with required exits 1/1/1/1/1/2/2. The stale-store control and grant-cycle premise were reached. The other 38 mutants were inspected in the published definitions/results, not independently rebuilt. An initial build selection misspelled R03's name and was correctly refused with exit 2 before builds; the commands above use the corrected name.

Reviewer probes used a separate harness copy with unchanged prototype, pinned modules and firmware. `probes.py` reproduces the original F1 trigger by arming the 0x80 payload fault only after its two pass-zero device reads complete. It also runs the header stimuli in R2-F1 and descriptor stimuli in R2-F2. For descriptor errors, the cycle callback sets `desc_mem_fail` when `levels().rs_app` first becomes nonzero. For the timeout, only the first subsequent accepted descriptor-memory request gets `drd.delay=5000`. The initial-image case sets `desc_mem_fail` before `boot()`. Results include all row/name/map snapshots and terminal/status events. `check_probes.py` independently asserts the fixed original rollback outcomes and the five failing adjacent outcomes reported above. All nine final probe runs completed; their V1a seed also completed. An initial reviewer-only C++ probe build referenced an unavailable observation symbol and was corrected to the public `levels()` helper before execution; no product/evidence source was changed.

The archived V11 grader still requires zero historical applications, so it reports failure when used on the original second-pass trigger even though rollback now clears the row. That is not reported as a new defect: the revised contract explicitly permits hidden transient applications, and the independent terminal snapshots plus V11b grade their removal. The counterexamples above instead assert surviving partial state and incorrect success verdicts.

All 14 following checks exited 0 on the exact page checkout:

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

All **48 revised receipt hashes** match both disk bytes and immutable Git blobs: 34 evidence files and 14 repository inputs, with submodule files checked against their pinned trees. The missing incidental file from round one is no longer claimed. Direct blob hashing with replacement objects disabled also matched all 850 page-tree blobs, 884 evidence-tree blobs, and all 539 initialized submodule blobs in each checkout.

Initial and completion checks agree: exact page/remote PR head `40d14d92bfcf3823ed7b227537630f444b1f4f73`; live remote dev `07294a76e833f1831d9fcbceb8123b8380c4ae76`, an ancestor; evidence checkout/remote evidence branch `ca8cb5943f885c22aec397ff75059e2d4791f4fb`. Pins: processor `424c688fa2205b934a7689a58f2aa766420f2326`, gPTP `c1b617435824929a790739ea8585c3fe1a328cc0`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external submodule remains uninitialized at its recorded pin. The initial tree was clean. Tracked page, evidence and submodule sources remain byte-exact; `REVIEW.md` is the sole added file in the page checkout.

Omissions: no full milan_dp, exhaustive RTL regression, full native candidate-merge gate, fresh OOC/calibration synthesis, Vivado, placement, silicon/power cuts, Docker/act, hosted-CI polling, privilege, subagents, push or public write. No shared Vivado resource was used or lock needed. Real microprogram/glue timing, empty-name replay, every frame-field mutation, all invalid clock/offset boundaries and new reset/bridge integration remain implementation evidence obligations. Mechanical gate success and the manager's independently continuing gates do not resolve these contract findings.

**Reviewer-owned coverage ledger.** No assigned lens has a clean covering round at the corrected head. Accordingly no per-lens PASS line is issued. Tests and Docs also retain the applicable findings above. Resolved reproductions do not bank an entire formerly dirty lens, and open defects are not cleared by follow-up tickets.

| Lens | Covering round | Exact page head |
|---|---|---|
| Conformance | OPEN; R217-r2 applied, R2-F1/R2-F2/R2-F3 unresolved | 40d14d92bfcf3823ed7b227537630f444b1f4f73 |
| RTL | OPEN; R217-r2 applied, R2-F1/R2-F2/R2-F3 unresolved | 40d14d92bfcf3823ed7b227537630f444b1f4f73 |
| Robustness | OPEN; R217-r2 applied, R2-F1/R2-F2/R2-F3 unresolved | 40d14d92bfcf3823ed7b227537630f444b1f4f73 |

This ledger is authored and explicitly accepted by the independent reviewer R217. It is a local review artifact; no public publication was performed. A corrected contract and immutable evidence require independent re-review at their new exact heads.

R217 FINISHED
