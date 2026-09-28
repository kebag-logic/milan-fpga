# Lane 0 handoff

Author: [A401]. Reviewers: [R380] internal; [R381] external.
Issue: https://github.com/kebag-logic/milan-fpga/issues/70
Assignment: https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862193501
Branch: `70-d3-contract`.
Base: `c07232228c12b72805dd20e6852bf93f25794da0`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Processor pin verified: `16be6768f710e79450aace277abacd6c2c3336e5`.
The read-only processor repository root was verified before further Git reads.
Status: REVIEW READY; all required gates passed at the continuation head.
Starting head: `0309a9eec3c1fa06c6338def6638e307e99bdfc1`. Local commit; not pushed.
Ruling: https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862405632
Register, acceptance and child contracts now reflect the ruling.
Continuation head: `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769`. Separate one-line local commit; not pushed.
All nine validation commands returned 0 at that head. Worktree clean.
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862203548

## Scope and evidence

Documentation and contract adoption only; no implementation is claimed.
The continuation updates D3, FASTCONNECT and snapshot cross-references.
The complete lane also includes the documentation index from the first commit.
The issue body and complete comment history were read, including owner decisions.
The permitted desk analysis and processor pin were checked read-only.
All ten register rows are RULED, with exact selected-option text.
Options, consequences and the adopted proposed defaults remain recorded.
Lane 1 measures both DR3a deadline candidates.
The manager ratifies or revises both before lane 2 implements.
DR4 limits shipping area acceptance to 1x1 TDM8.
The 8x8 retains synthesis diagnostics and its open, blocked post-place obligation.
That obligation is not waived; 8x8 remains non-shipping until it fits (#584/#229).
No acceptance checkbox was marked complete by this adoption.
Processor F07.9 still needs the listed later-lane edits.

The following sections reproduce the reconciled contract for handoff convenience.
The committed repository documents remain authoritative after review.
Relative document links below resolve from `docs/design` in the lane.

## 17. Acceptance reconciliation

FASTCONNECT section 16 remains the product acceptance checklist.
This table maps every line, in its existing group order.
D3 rules have one home here; media rules retain theirs.
No checkbox changes merely because the contract is accepted.

| Acceptance line | Normative home | D3 application and remaining evidence |
|---|---|---|
| Namespace 1: complete record-space gate | FASTCONNECT 4.2/4.4 | Sections 3.1/18 use the same shape-derived population. Lane 5 reruns the gate and all registered controls. |
| Namespace 2: every writable-name ordinal encoded/decoded | FASTCONNECT 4.2 | Sections 3.1/8.5; lane 3 covers every ordinal, including both ENTITY names. |
| Namespace 3: index/ordinal disagreement mutation | FASTCONNECT 16, namespace | Sections 8.2/18.3 require the mutation to fail actual replay. |
| Namespace 4: empty name survives | D3 8.3/8.5 | Lane 3 distinguishes a saved empty name from image defaults and erased spans. |
| Namespace 5: IDs inside their group blocks | FASTCONNECT 4.2 | Sections 3.1/8.3 bind writer and replay selection to those IDs. |
| Container 1: independent golden images | FASTCONNECT 6.3 | Preserve existing host evidence; lanes 2-5 add actual materialized records. |
| Container 2: each refusal applies zero records | FASTCONNECT 6.2 | Section 8.6 additionally contains faults during the later device walk. Container validation alone does not prove replay. |
| Container 3: ascending IDs and offset agreement | FASTCONNECT 6.1 | All child lanes use the allocation; lane 5 checks independent encoders/decoders. |
| Container 4: omitted mandatory record refused | FASTCONNECT 6.2, rule 12 | Lane 5 removes each span with CRC recomputed. An erased span remains present. |
| Status 1: backed with/without writer | FASTCONNECT 9.1/9.2 | D3 7.1 hands producer pending to backend ownership; backing alone never proves saved values. |
| Status 2: answered once, then stops | FASTCONNECT 9.2/9.4 | Lane 5 checks revocation with unsaved D3 work. |
| Status 3: erase/program/verify failure | FASTCONNECT 9.2 | Preserve independent verdicts; lane 5 forbids ACK and false durability. |
| Status 4: reachable status combinations | FASTCONNECT 9.3; snapshot 6.1 | Lane 5 observes combined D3, binding and backend ownership. |
| Status 5: recovery with outstanding work | FASTCONNECT 9.2 | Snapshot acknowledgement identity remains authoritative. D3 7.1 cannot clear later work. |
| Status 6: healed outage and later commit | FASTCONNECT 9.2 | Lane 5 checks the actual recovery state, not a masked stale bit. |
| Status 7: late verified completion | FASTCONNECT 9.2 | Snapshot identity decides retirement. A late slot never restores backing by itself. |
| Status 8: legal flash operation and heartbeat | FASTCONNECT 9.4 | Lanes 2/5 refresh service and physical timing on the composed firmware. |
| Status 9: timeout at erase/program/readback | FASTCONNECT 9.2/9.4 | Lane 5 injects each phase separately and checks its verdict. |
| Status 10: cut during either debounce | D3 7.1/7.2 | Producer pending covers unmaterialized work; backend dirty covers committable work. DR2a sets both windows and requires measured normal-load durability. |
| Status 11: blank restore is honest | D3 8.7 | Combined blank requires done, no failure, and neither walk validating a record. Host blank evidence is not physical proof. |
| Saved set 1: eight items and complete binding state | D3 8.2/18 | Clear stores first; restore values and valid flags; read every generated index. Lane 2 adds restored-PTOF consumers; lane 5 closes the complete physical inventory. |
| Saved set 2: volatile exclusions | D3 9 | Lock and owner clear, registry empties, IDENTIFY becomes zero. Populate them before the same save/reset/restore cycle. |
| Saved set 3: cut at every commit stage | FASTCONNECT 7 | Snapshot ownership protects the captured image. Lane 5 accepts complete old/new committed snapshots, never mixed restored state. |
| Trigger 1: former eight-mark deletion line | D3 3.1/7.2/8.2 | Nine independent live-trigger and replay deletions. Separate input/output formats and maps; all user names share one group. |
| Trigger 2: former SET_CONTROL mark-absence line | D3 3.1/9 | Add IDENTIFY to persistence and require failure. Completion-mark presence is not the persistence oracle. |
| Area 1: 1x1 shipping area; blocked 8x8 post-place | D3 15.1 DR4; FASTCONNECT 8.3/16 | Apply stage budgets, matched heads and corrected #607 constraints to 1x1 TDM8. Retain 8x8 synthesis diagnostics; post-place remains open and blocked, not waived. The 8x8 stays non-shipping until it fits (#584/#229). The 781-LUT figure is historical backend evidence only. |

The following accepted rules complete the materialization contract:

| Rule | Sole materialization home | FASTCONNECT cross-reference |
|---|---|---|
| Coherent latch; taint; group/index clear; change wins done | Sections 6.1/6.3/7.1 | Section 16 introduction |
| Verified AEM and always-started cold walk | Sections 5.3/8.1 | Sections 10/16 |
| Store-local rollback and hard-reset-only debt | Section 8.6 | Sections 10/16 |
| Combined enable and three distinct service releases | Section 8.1 | Sections 9.3/10/16 |
| Per-wait deadline; DEFAULTS versus CLOSED; no timed port reuse | Section 8.8 | Sections 9.3/10/16 |
| Product deadline values and operational choices | Section 15.1, RULED; DR3a measurement/ratification still required | Sections 14/15/16 |

### 15.1 Manager decision register

Every row is **RULED** by the [manager decision](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862405632).
The selected-option column reproduces that ruling exactly.
The manager adopted each proposed default, subject to stated qualifications.
The rulings apply to lanes 1-5 unless stated otherwise.
DR3a requires lane 1 measurements before lane 2 implements.
The manager must then ratify or revise both deadline numbers.
Existing requirements and outstanding implementation evidence remain binding.

| ID and status | Options and consequences | Selected option (manager ruling) | Adopted default and required evidence |
|---|---|---|---|
| DR1a: #15 closure prerequisite. **RULED** | Require reusable service after silence: needs acknowledged cancellation/reset. Alternatively, explicitly accept reset-required persistence failure for #70. That leaves processor #15 open and requires a public acceptance amendment. | #15's unchanged criterion (bounded error, busy release, a later successful operation; late responses never reassigned) is required before **full** #70 closure. Contract work and lanes 1-4 may proceed meanwhile. DEFAULTS service is never counted as reusable persistence. | Require #15's unchanged criterion before full #70 closure. Contract work and lanes 1-4 may proceed meanwhile. Demonstrate bounded error, busy release, and a later successful operation; reject late-response reassignment. Never equate DEFAULTS service with reusable persistence. |
| DR1b: #20 reconciliation. **RULED** | Reconcile the existing issue against landed DEVICE/UNFRAMED semantics. Alternatively, implement its original manager-only err/done split, which misclassifies erased headers. | Keep the landed cause interface. The processor reviewer reconciles #20 at the selected pin, and #20 stays open until its own review. | Retain the landed cause interface. Have the processor reviewer reconcile #20 and rerun its acceptance at the selected pin. Prove zero-byte DEVICE failure, clean blank defaults, and existing A2/F4/G2 behavior. Keep #20 open until its own review and containment. |
| DR2a: debounce and loss. **RULED** | A first-change window bounds coalescing under continued traffic. Restarting a quiet-period timer coalesces longer bursts but can postpone saving indefinitely. Per-command writes increase wear. | 500 ms producer and 1,000 ms firmware first-dirty windows. Each lane that implements a writer publishes a measured acceptance-to-durable time under normal load. No unconditional durability promise. | Use 500 ms producer and 1,000 ms firmware first-dirty windows. Drain one eligible burst per producer window. Measure command sweeps, final-value convergence and erases. Cuts before verified promotion may lose unsaved changes; the last verified snapshot survives. Each lane implementing a writer publishes measured normal-load acceptance-to-durable time, separately from failure/backpressure. No unconditional 1.5-second durability promise. |
| DR2b: identical writes. **RULED** | Conservative live-write/phase-5 triggers can rewrite identical values. Change-qualified triggers suppress wear but need exact comparisons, including validity and full name/map content. | Suppress only proven unchanged persisted projections. Every real accepted write persists, and a mutant that loses a real change is killed. | Suppress only proven unchanged persisted projections. A default-valued scalar becoming valid still changes that projection. Preserve every actual accepted write, including writes before a later command abort. Prove repeated identical names/maps/scalars cause no new flash erase after convergence; mutate the comparison to lose a real change. |
| DR2c: retries and alarms. **RULED** | Bounded immediate retries minimize recovery delay but repeat pressure. Backoff lowers pressure but lengthens the loss window. Automatic forgiveness risks clearing evidence of an abandoned change. | At most 3 write attempts per record, 500 ms apart, and at most 3 firmware transaction attempts per work set, 1,000 ms apart. The alarm stays until reset; a failed slot is never ACKed. | Use at most three write attempts per record, relatching each time, separated by 500 ms. Specify attempts versus retries explicitly. Use at most three firmware transaction attempts per unchanged captured work set, separated by 1,000 ms. After exhaustion, keep the alarm until reset. Never ACK a failed slot or forgive producer loss on heartbeat. These limits do not solve an operation that never ends; DR1a governs that case. Measure error bursts and erase amplification. |
| DR3a: boot/recovery budgets. **RULED** | Reuse a 20 ms per-wait prototype value without measurement, or derive clocks from worst supported product latency and impose a separate aggregate budget. Only the latter measures whole-boot service. | 20 ms per wait as the initial candidate and a 1,000 ms aggregate from `PP_CTRL[1]` to a terminal state. Lane 1 measures; **the manager ratifies or revises both numbers before lane 2 implements**. | Use 20 ms as the initial per-wait candidate, then prove it exceeds the image walk and largest record transaction. Record `ceil(core_hz * timeout_ms / 1000)` and clock ratios. Use an initial 1,000 ms aggregate budget from accepted `PP_CTRL[1]` to COMPLETE, DEFAULTS or CLOSED, including rollback. Lane 1 measures; the manager ratifies or revises both numbers before lane 2 implements. Firmware's wait never overrides fabric enable. Release deadlines remain REQUIREMENTS section 8, including the provisional 30-second restoration ceiling. |
| DR3b: boot failures and restart premise. **RULED** | Prove CPU-only restart retains the window and ownership under O4, or couple every CPU reset to a fabric reset. The former needs physical retention evidence; the latter loses live volatile state and reruns cold initialization. | Coupled CPU and fabric resets until O4 retention is physically proven. AEM is loaded and CRC-checked before descriptor-dependent restore, and every cold path reaches a terminal state. | Couple CPU and fabric resets until O4 retention is physically proven. Preserve O1's sole control writer, O2's fabric-to-CPU reset, and O3's admission order. Load and CRC-check AEM before descriptor-dependent restore. On a shape failure, disable persistence but start the failure/default walk when fabric identity is valid. On an unprovable AEM image, reach CLOSED. Prove all cold paths reach a terminal; never bypass restore on a firmware timeout. No runtime reload may erase producer ownership. |
| DR4: area and comparison. **RULED** | Retain both-shape post-place acceptance, which blocks 8x8 delivery until it fits; or explicitly narrow shipping acceptance to 1x1 while retaining 8x8 synthesis diagnostics and its blocked placement obligation. | **Shipping area acceptance for D3 is narrowed to the 1x1 TDM8.** It uses the stage budgets, the matched-head method and #607's corrected constraints. The 8x8 keeps synthesis diagnostics, and its post-place obligation stays open and blocked. It is **not waived**: the 8x8 remains non-shipping until it fits (#584/#229). | Use the stage budgets below for 1x1 TDM8 shipping area acceptance. Retain 8x8 synthesis diagnostics; its post-place obligation remains open and blocked, not waived. The 8x8 remains non-shipping until it fits (#584/#229). Measure matched before/after heads, generated inventory, clocks, device, directives, seeds and corrected #607 constraints. Include LUTRAM, FF, BRAM, DSP, WNS and firmware size. The historical 781-LUT backend figure is not a D3 budget. |
| DR5: inventory and migration. **RULED** | Reject incompatible old images with explicit defaults, or implement a versioned migration with an independently verified converter. Silent reinterpretation can restore another field's bytes. | Keep the current exact inventory and flat IDs; SUID/MCR spans stay deliberately erased. Incompatible images are refused under KLJ2 rules, and any future growth needs a public migration decision. | Retain the current exact inventory and flat IDs. Keep SUID/MCR spans deliberately erased. Preserve compatible binding-plus-erased images without a layout change. Refuse incompatible identity, shape or layout by existing KLJ2 rules; never erase old slots merely on refusal. A future added source, descriptor/name growth or layout change needs a public migration/default decision and new goldens. #584 remains separately parked. |
| DR6: final-image sequencing. **RULED** | Compose merged dependencies before measurement, or measure intermediate heads and repeat all affected evidence later. The latter costs reruns and cannot qualify the final image. | Lane order 1 to 5. Lanes 2-5 follow PR #609, PR #603, #607 and the merged revisions of processor PRs #129/#130, with actual merge and pin identities recorded. Final evidence names one composed image. | Follow the manager's lane order 1 through 5. Lanes 2-5 follow firmware PR #609, #602/PR #603, #607 and the selected merged processor #129/#130 revisions. Record the actual merge/pin identities before integration. Reconcile any exclusion publicly; open PR heads are not prerequisites satisfied. Final service, capture, area and cold-cycle evidence all name the same composed image. |

DR3b's source evidence is at parent `c0723222`:

- `sw/firmware/milan_baremetal/milan_baremetal.c:1254` returns on shape mismatch.
  That return precedes the restore strobe and service installation.
- `sw/firmware/milan_baremetal/milan_baremetal.c:1438` begins `milan_init`.
  It calls `nvm_boot` before `load_aem_image`.
- [Snapshot section 7](SAVED_STATE_SNAPSHOT_OWNERSHIP.md#7-the-writer-sequence) owns O1-O4.
  Its section 20 retains the unproven restart and ordering premises.
- The [capture receipt](../../tb/verilator/nvm_capture_cpu/measurements.json) remains conditional.
  Changing firmware, census, clocks or measured paths requires remeasurement.
  The 24.5 ms acceptance and 49 ms floor remain unchanged.
  Increasing the hold cannot conceal a failed capture measurement.

The current inventory is retained, not expanded by DR5.
FASTCONNECT section 4.2 remains the sole allocation authority.
The following maps requirements to live owners and implementation stages.

| Required item | Complete population | Live owner / lane |
|---|---|---|
| 1: configuration | Current CONFIGURATION, including default value and validity | Dynamic store / lanes 1-2 |
| 2: sampling rates | Every declared AUDIO_UNIT | Dynamic store / lanes 1-2 |
| 3: formats | Every STREAM_INPUT and STREAM_OUTPUT, independently; applicable CRF rows included | Dynamic store / lanes 1-2 |
| 4: presentation offset | Every STREAM_OUTPUT, including declared CRF | Dynamic store and timestamp consumers / lanes 1-2 |
| 5: mappings | Every STREAM_PORT_INPUT and STREAM_PORT_OUTPUT; mutable sets and static defaults distinguished | Parent map/owner/crossbar state / lane 4 |
| 6: clock source | Every CLOCK_DOMAIN's selected source and validity | Dynamic store / lanes 1-2 |
| 7: ENTITY names | Both entity_name and group_name, distinct ordinals | Descriptor store / lane 3 |
| 8: other user names | All generated writable ordinals: CONFIGURATION, AUDIO_UNIT, STREAM_INPUT/OUTPUT, AVB_INTERFACE, CLOCK_SOURCE, CLOCK_DOMAIN, CONTROL and AUDIO_CLUSTER | Descriptor store / lane 3 |
| Binding state | Every STREAM_INPUT: bound state, talker identity, source index, requesting controller and started/stopped projection | Binding manager / lane 5 complete proof |
| Reserved SUID/MCR | Existing allocated spans, entirely erased; no new mutable source | Existing KLJ2 erased representation / all lanes |
| Volatile exclusions | Lock and owner, registered-controller list, IDENTIFY value | Excluded under section 9 / every reset proof |

Shipping models may have only one legal scalar value.
Such rows require cleared-first validity proof as well as readback.
No synthetic alternative value becomes a shipping declaration.

Ruled D3 stage ceilings for 1x1 TDM8 shipping area acceptance:

| Stage / lanes | Incremental LUT-equivalents / FF | Cumulative LUT-equivalents / FF | New BRAM / DSP |
|---|---|---|---|
| Scalar core / 1-2 | 2,500 / 1,400 | 2,500 / 1,400 | 0 / 0 |
| Names / 3 | 750 / 400 | 3,250 / 1,800 | 0 / 0 |
| Maps / 4 | 1,250 / 600 | 4,500 / 2,400 | 0 / 0 |

These stop-and-review ceilings require measured affordability.
They reserve integration margin above section 12's historical full prototype.
Already-landed prerequisite costs belong in the before baseline.
Each comparison includes processor and parent glue costs together.
Firmware text/data/bss growth is reported separately against image capacity.
A budget exceedance needs a ruling, never an unexplained allowance.
The 8x8 retains synthesis diagnostics.
Its post-place obligation stays open and blocked, not waived.
It remains non-shipping until it fits (#584/#229).

### 15.2 Processor F07.9 edit table

All paths below are relative to the processor repository.
These are later-lane obligations; lane 0 edits none of them.
Apply them before or with the scalar implementation's reviewed pin.

| File | Section or artifact at `16be6768` | Required change |
|---|---|---|
| [docs/architecture/07_memory_maps.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/07_memory_maps.md) | 5.3, F07.9 runtime, lines 447-458 | Replace COMMIT/NVM_MARK selection with section 3.1's accepted live-write groups. Show latch ownership, group/index selection, taint, change-wins-done, and alarm on abandoned work. Cite the ratified DR2 parameters. |
| [docs/architecture/07_memory_maps.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/07_memory_maps.md) | 5.3, F07.9 boot, lines 459-475 | Show verified AEM, drained binding terminal, D3 image proof, both passes, validation and valid-bit apply. Draw COMPLETE, DEFAULTS and CLOSED. Keep listener release, AECP release and combined ADP enable distinct. |
| [docs/architecture/07_memory_maps.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/07_memory_maps.md) | 5.3 failure table and following paragraphs | Preserve DEVICE/UNFRAMED and per-walk atomicity. Add D3 rollback of both stores, then maps. Debt survives local reset. Distinguish raw binding blank from combined `done && !fail` blank; a failed product restore is never blank. Preserve completed bindings on D3 rollback. |
| [docs/architecture/07_memory_maps.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/07_memory_maps.md) | 5.1/5.2/5.4, F07.8 inventory and open choices | Retain one record per group/index, flat names and erased SUID/MCR reservations. Adopt #501 map lengths without reviving name banks. Record ratified migration and wear decisions, with exact inventory references. |
| [docs/architecture/02_interfaces.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/02_interfaces.md) | 8.1/8.2, lines 538-572 | Assign manager 1 to the processor D3 writer. Replace integrator-owned group wording. Document D3 unflushed, combined alarms/verdicts, owner/rollback/debt and image-valid interfaces. Marks remain completion notifications. Retain the one device initiator and drain rule. |
| [docs/architecture/06_aecp_engine.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/06_aecp_engine.md) | 4/5 and state/name/format/map interfaces | Document command-side snooping, dispatch ownership from reset, coherent name capture, real map read/apply faces and shared semantic validation. Exclude restore writes and IDENTIFY values. Distinguish persisted CONTROL names. |
| [docs/architecture/05_acmp_engine.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/05_acmp_engine.md) | 5.1 boot admission | Cross-reference the D3 order without reimplementing #109. Preserve saved bindings after failed walks and read-only polling. D3 rollback never resets the listener or its admission gate. |
| [docs/architecture/08_timing.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/08_timing.md) | 2, T-NVM-DEBOUNCE and T-NVM-RS-DEADLINE | Separate producer debounce, firmware debounce, per-wait clocks, aggregate restore budget and media deadlines. Record ruled DR2 values and their measurement anchors. Label DR3a's numbers initial candidates until lane 1 measures and the manager ratifies or revises both before lane 2 implements. Never claim quarantine satisfies #15. |
| [docs/architecture/09_verification.md](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/16be6768f710e79450aace277abacd6c2c3336e5/docs/architecture/09_verification.md) | 3, NVM; 8, suite evidence | Add cleared-first checks, nine trigger/replay controls, volatile exclusions, transport/value distinction, debt and rollback faults, and real-command integration. Reconcile existing #18/#19/#21 tests before adding missing cases. |

F07.9 is inline Mermaid in the memory-map document.
Any associated generated render follows its processor generation rules.
The authoritative source changes first; no generated copy is hand-edited.

## 18. Child-lane contracts

These are reviewable contracts, not new assignments or issues.
The manager assigns an executor and independent reviewers before activation.
Each repository gets its own issue, branch and review object.
The [lane order](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862191328) is mandatory.
Section 15.1 records the manager's rulings for all five lanes.
DR3a requires lane 1 to measure both deadline candidates.
The manager ratifies or revises both before lane 2 implements.
Later lanes inherit those ratified limits and remeasure changed paths.
DR4 limits shipping area acceptance to 1x1 TDM8.
Each lane retains 8x8 synthesis diagnostics.
The 8x8 post-place obligation remains open and blocked, not waived.
The 8x8 remains non-shipping until it fits (#584/#229).
Every writer lane measures normal-load acceptance-to-durable time under DR2a.
DR2b/DR2c require unchanged-projection controls, bounded attempts and sticky alarms.

Every lane publishes exact heads, commands, exits and input identities.
Required repository gates remain mandatory for its actual change scope.
Prototype results never substitute for tests of the implemented path.
Shipping values follow the verified model; synthetic values are labelled.
Where only one value is legal, check restored validity too.

### 18.1 Lane 1: processor core and scalars

**Acceptance.** Implement configuration, rates, both formats, clock source and PTOF.
Use the existing arbiter, S1/S3/S4 and S2 guard.
Add command-side triggers and taint-safe whole-record retirement.
Hold AECP ownership from reset through the D3 terminal.
Implement both passes, semantic validation and combined restore outputs.
Stage 1 rolls back dynamic and descriptor stores together.
Debt survives local rollback; watchdog recovery precedes the re-LOCATE.
Apply the processor documentation table in section 15.2.
Measure DR3a's initial 20 ms per-wait candidate.
Measure its 1,000 ms aggregate from accepted `PP_CTRL[1]`.
Include both walks and rollback to COMPLETE, DEFAULTS or CLOSED.
Record product clocks, worst supported latency and cycle conversions.
Submit both numbers for manager ratification before lane 2 implements.

**Validation.** Extend processor [tb/pp_top](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/tree/16be6768f710e79450aace277abacd6c2c3336e5/tb/pp_top) with real AECP commands.
Exercise all declared scalar indices through retained-media reset and readback.
Check cleared values and validity before any restore application.
Run processor [tb/nvm_port](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/tree/16be6768f710e79450aace277abacd6c2c3336e5/tb/nvm_port), [tb/acmp_nvm](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/tree/16be6768f710e79450aace277abacd6c2c3336e5/tb/acmp_nvm) and descriptor-guard suites.
Reconcile #18/#19/#21's existing controls before adding missing cases.
Re-run the processor's full required gates at its final head.

**Negative controls.** Delete each scalar trigger and replay independently.
Keep a store uncleared; ignore valid flags; clear by group/index alone.
Drop taint or same-edge precedence; count restore writes as changes.
Collapse DEVICE into blank; omit descriptor rollback or debt hold.
Release AECP/ADP early; release quarantine by time alone.
Exercise zero, boundary, corrupt, refused and indefinitely delayed inputs.

**Prerequisites and physical remainder.** Apply the ruled DR1-DR5 choices.
DR1a permits lanes 1-4 before #15's full-closure evidence.
DR1b retains the cause interface and processor-reviewer reconciliation of #20.
Report lane 1's contribution to DR4's scalar-stage budget.
Lane 2 completes the matched 1x1 post-place comparison.
Retain 8x8 synthesis diagnostics and its blocked post-place obligation.
Coordinate shared processor tests/docs with #129/#130.
No processor-only test closes product cold-cycle or PTOF acceptance.
Lane 2 owns that targeted scalar physical proof.
Lane 5 retains the full saved-set release campaign.

### 18.2 Lane 2: parent scalars and restored PTOF

**Acceptance.** Adopt lane 1's reviewed, contained processor pin.
Wire D3 ownership, verdicts and pending into the real parent.
Retire scalar sticky pending only after its record owner accounts.
Implement the three firmware boot changes in section 5.3.
Exercise shape mismatch, bad AEM and disabled-writer boot paths.
Preserve O1-O3; couple CPU and fabric resets under DR3b.
CPU-only restart requires physical proof of O4 retention.
Grade every cold path against DR3a's manager-ratified deadlines.
Update actual boot/status documentation when implementation changes it.

Save legal PTOF values, including zero and a non-default offset.
After reset, prove the rows and valid flags cleared.
Restore solely from retained flash, without controller SET repair.
Check GET_STREAM_INFO and addressed AAF/CRF presentation timestamps.
Check first/last declared outputs and untargeted rows independently.
Erased or rejected PTOF rows retain the generated factory default.
The 2 ms factory rule remains unchanged.

**Validation.** Extend parent `tb/verilator/milan_dp` and `pp_shadow` real paths.
Compose shipping firmware and RTL in `tb/verilator/nvm_cosim`.
Run `sw/firmware/nvm_hosttest/test_nvm_firmware.py` for boot failures.
Refresh capture and service receipts against the composed firmware.
Run the implementation's full local gates and matched area comparison.

**Negative controls.** Delete PTOF replay and its validity write separately.
Swap an output index; disconnect the timestamp consumer.
Restore before AEM; return early on shape failure.
Enable at firmware timeout; accept a wrong capture identity.
Suppress scalar pending while materialization is unfinished.
Each must fail a named value, ordering or durability assertion.

**Dependencies and physical result.** Follow DR6 and lane 1.
Wait for manager ratification or revision of both DR3a numbers.
That ruling must precede lane 2 implementation.
Complete DR4's scalar-stage 1x1 TDM8 area acceptance.
Retain 8x8 diagnostics; its post-place obligation stays open and blocked.
Observe #602's final media-reset rule when grading timestamps.
Use #607's corrected constraints for timing evidence.
Prove one targeted 1x1 cold cycle covering every scalar group.
Read back through real commands and observe restored PTOF on wire.
Record all image identities, deadlines and volatile-reset observations.
Full cut-during-commit and release campaigns remain lane 5's.

### 18.3 Lane 3: every user name

**Acceptance.** Add coherent eight-lane capture and replay after image readiness.
Cover both ENTITY names and every generated writable-name ordinal.
Include CONTROL names without persisting IDENTIFY values.
Preserve empty strings and full 64-byte names exactly.
Keep descriptor debt and rollback protection from lane 1.
Transfer name pending only when its writer owns every change.
Adopt the processor change in a separate reviewed parent lane.

**Validation.** Run real SET_NAME/GET_NAME across the generated inventory.
Compare saved bytes with an independent ordinal/name oracle.
Reset names to image defaults before replay and verify every ordinal.
Exercise changes during capture, descriptor healing and failed restoration.
Run affected processor/parent suites and required local gates.

**Negative controls.** Delete name trigger/replay; swap ordinal and record ID.
Treat empty strings as absent; capture mixed old/new lanes.
Replay before image initialization; omit descriptor rollback or debt protection.
Clear pending while another name remains unsaved.
Require each control to fail its named name-value assertion.

**Dependencies and physical result.** Follow lanes 1-2 and DR6.
Apply DR2b's unchanged-projection rule and DR5's fixed inventory.
Remeasure changed restore paths against the ratified DR3a budgets.
Meet DR4's names-stage 1x1 TDM8 area ceilings.
Retain 8x8 diagnostics and its open, blocked post-place obligation.
Any #584 name growth needs its separate authorization and new measurements.
Cold-cycle all writable names, including both ENTITY names and empty names.
This targeted proof does not close lane 5's combined campaign.

### 18.4 Lane 4: both map directions

**Acceptance.** Implement capture/apply over the actual parent map interfaces.
Consume #501's per-port capacity in processor buffers and framing.
Persist input and output ports independently, including empty sets.
Preserve static-map defaults without inventing mutable static state.
Apply section 8.4's coupled format/map validation transaction.
Rollback maps, output ownership and crossbar effects with scalar formats.
Transfer remaining map pending only after real materialization accounts.

**Validation.** Use actual phases 0-5 and retained-flash integration.
Exercise first/last port, legal maximum and over-capacity refusal.
Check duplicate/conflicting keys, UNUSED entries, holes and malformed records.
Distinguish 72 reserved output slots from 64 legal AAF keys.
CRF allocation does not legalize CRF audio mappings.
Run record-space, backend, map, processor and datapath gates.
Refresh inventory-dependent capture and area evidence.

**Negative controls.** Delete each directional trigger and replay independently.
Use old output lengths; truncate the set; confuse directions.
Accept padding by one byte; leave holes; skip final format validation.
Drop output-owner/crossbar rollback; abort inside each edit phase.
Suppress actual-change pending or invent changes from refused edits.
Require value, routing and ownership failures, not timeout-only detection.

**Dependencies and physical result.** Follow lanes 1-3 and DR6.
DR2b governs unchanged edits; DR5 preserves the inventory.
Remeasure both passes and rollback against ratified DR3a budgets.
Meet DR4's maps-stage 1x1 TDM8 area ceilings.
Retain 8x8 synthesis diagnostics.
Cold-cycle ADD/REMOVE results on both mutable directions.
Verify GET_AUDIO_MAP and actual audio routing after automatic restore.
The 8x8 post-place obligation remains open and blocked, not waived.
Lane 5 still owes the combined saved-set fault campaign.

### 18.5 Lane 5: complete fault campaign and release bench

**Acceptance.** Prove section 17's shipping obligations with executable evidence.
Use DR4's 1x1 TDM8 area scope and cumulative ceilings.
Retain 8x8 synthesis diagnostics and the open, blocked post-place obligation.
It is not waived; 8x8 stays non-shipping until it fits.
Verify the composed image against manager-ratified DR3a budgets.
Record lane 1 measurements and the pre-lane-2 ratification ruling.
Follow lanes 1-4 and DR6's merged-dependency sequence.
Inventory every generated persisted field and index, including applicable CRF.
Include bound/unbound state, source/talker/controller parameters and started/stopped state.
Populate lock, locking owner, registrations and IDENTIFY before reset.
Prove those volatile states clear while persistent state returns.

Compose the real processor, parent, firmware and retained flash model.
Prove clearing before replay, then rerun the model-driven command graders.
Inject cuts/errors at erase, program, verify, capture, ACK and restore.
Include every binding/D3 record type and both restore passes.
Check old/new committed snapshots, late responses and clean first boot.
Reconcile processor #18/#19/#21's standing-variant evidence at the final pin.
Resolve DR1a/#15 and DR1b/#20 before claiming full closure.

**Negative controls.** Delete every trigger and replay group independently.
Omit mandatory spans; preserve uncleared stores; ignore validity.
Persist lock/registry/IDENTIFY; default empty names; mismatch maps/formats.
Misclassify DEVICE, release debt early, or ACK the wrong capture.
Flash an unattested capture; mutate clear precedence or failed-slot handling.
Every control must finish and fail its intended assertion.

**Physical result.** Follow [REQ-VER-06](../../REQUIREMENTS.md#8-verification-and-release-acceptance).
Use [TESTING section 6d](../testing/TESTING.md#6d-unattended-campaign-vehicle)'s campaign vehicle.
Complete seven continuous days with the reference peer.
Include both directions, CRF and every declared stream index.
Complete 200 cold cuts: 160 idle and 40 during commits.
Restore all eight item groups and the complete binding inventory.
No controller repair may count as automatic recovery.

T0 is the host-timestamped outlet ON command.
First ENTITY_AVAILABLE must precede T0 plus twenty seconds.
Its `valid_time` is 10; boot consumes that window.
Automatic AVTP restoration has the existing provisional thirty-second ceiling.
Ratification uses #397/#75 measurements; larger bounds remain ineligible.
After automatic restoration, test controller reconnect separately below one second.
The full counter, uncertainty and observation rules remain REQ-VER-06's.

Retain matched bitstream/firmware hashes, journal images and decoded state.
Keep UART, wire captures, timestamps, counters and temperature observations.
Physical ordering, flash identity and restart premises need direct evidence.
Simulation timings and historical bind/unbind proof cannot replace these results.
Newly discovered implementation defects receive separate public work items.
No final success is claimed while those acceptance defects remain.

## Gate table

Every row ran at committed head `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769`.
The first eight rows are the required assignment gates.
The last row additionally checks the complete committed delta.
Each command had a 600-second timeout and returned 0.
Use the existing temporary environment at `/tmp/70-d3-docs-venv`.
It carries the hash-locked Markdown dependencies and PyYAML 6.0.3.
Every command runs in the foreground without a pipeline.

| Command | Exit | Captured output |
|---|---|---|
| `python3 scripts/docs_check.py` | 0 | [docs-check.log](docs-check.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths.log](doc-paths.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc.log](toc.log) |
| `python3 scripts/check_em_dash.py --base c07232228c12b72805dd20e6852bf93f25794da0` | 0 | [em-dash.log](em-dash.log) |
| `python3 scripts/check_baremetal_only.py --check` | 0 | [baremetal.log](baremetal.log) |
| `python3 scripts/ci_scope.py --selftest` | 0 | [ci-scope.log](ci-scope.log) |
| `git diff --check` | 0 | [diff-check.log](diff-check.log) |
| `git diff --check c07232228c12b72805dd20e6852bf93f25794da0 HEAD` | 0 | [committed-diff-check.log](committed-diff-check.log) |

The [contract check](contract-check.log) confirms all ten exact selections,
all 26 unchanged checkbox states and mappings, and DR3a/DR4 in every child contract.
The [gate results](gate-results.json) record each command, head, exit and duration.
Git emitted a commit-graph availability warning; its checks returned 0.
No source change, push, pull request operation, merge or hardware work occurred.

## Review handoff

Independent [R380]/[R381] review remains required at the new head.
All register choices are ruled; DR3a retains its later measured ratification.
Lane 0 does not claim to finish issue #70.
Implementation, physical evidence and dependency closure remain explicit above.
No pull request was created; PR-BODY.md is the prepared review description.

REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862516082
