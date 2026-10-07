[R521] POSITIVE - exact head 5428b044176f95248e6916dc00dd89c0df154078

External independent source review, round R521-1, issue #682 / PR #692.
Tree: `4a12e8029325593169fa91dbbf855dc3d5efee9d`.
Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
All five lenses were applied independently. No BLOCKER, MAJOR or MINOR finding remains from this review. No source fix, commit, push, GitHub write or hardware action was performed. This verdict does not authorize merge or discharge manager-owned acceptance.

Scope and authorities

The review reconstructed the repository contract, documentation index, [frozen issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/682), [assignment](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6018127147), [render ruling](https://github.com/kebag-logic/milan-fpga/issues/682#issuecomment-6028334443), linked processor PRs 156/159/160/161/162/164, interface contracts and source history before examining executable evidence. The normative resource authority is `docs/reference/FR_NFR.md:464`; the retained owner decision is [issue #234 comment 5967924270](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270). Timing acceptance follows `docs/integration/BUILDING.md:535` and the full section-5 coverage qualifications.

Public evidence was read at immutable [evidence commit 8d4e0732](https://github.com/kebag-logic/milan-fpga/tree/8d4e0732588d09f1f94f41aea7c7c39110da09a2/review-evidence/682-r1). `audit_evidence.py` independently verifies all 130 published payload hashes against its publication manifest. The author receipts are evidence, not an independent verdict. No private author directory or other reviewer's report supplied this review's conclusions.

Acceptance results

| Item | Result at reviewed source | Evidence |
|---|---|---|
| 1. Pin and required adaptations | Met | Gitlink is `2ad2f845dd583f8310075fa2380cb60a04fd091a`. Both public adoption patches replay onto source base and produce the exact final parent blobs. No parent production RTL changes occur in the lane delta. |
| 2. Resource baseline and declaration warnings | Met under the recorded owner policy | All three public combination-F records exactly equal the committed baseline. Policy tolerances, floors and ceilings equal dev. Each synthesis receipt records zero processor Synth 8-6901 warnings across 46 directly read sources, separately retaining one parent warning. |
| 3. Capture conditional remeasurement | Met | The product firmware digest is unchanged; fresh `check_nvm_capture.py` passes source, census, clock, both traffic arms and row-to-summary checks. The retained 8x8 maximum is 13.86484 ms against 24.5 ms. |
| 4. Source gates, render differential and image | Met within the public ruling and receipt limits below | Retained complete sweep is 60/60 at its actual ancestor; affected final-head gates have 75 successful public command receipts, including 49 documentation workflow steps. Render is explicitly **unchanged from dev; #657**, not 32/32. All three routes meet the timing thresholds; only the selected route has complete-image evidence. |
| 5. Post-merge hardware | Not graded | Manager-owned withdrawal cycles, default-map read and stream/counter soak. |

[R521] PASS Conformance - `docs/reference/SUBMODULES.md:158`, processor `hdl/aecp/KL_aecp_notify.sv:1253`, processor `hdl/srp/KL_srp_listener_fsm.sv:769`, `syn/ooc/pp_resource_baseline.json`, and the frozen issue/rulings - All parent-visible items are accounted for.

The pin delta has six first-parent integration merges. Notification spacing retains a descriptor index, resets it, latches it on the counter-round claim and advances the stamp through the waiting send. Mid-round held DEREGISTER cannot overwrite an active round. Both SRP registrar FSMs now handle expiry before a simultaneous Lv/LeaveAll, while registering New/Join renews IN. The declaration-order edits move existing declarations without changing expressions. C11 changes interface documentation and gates; #42 adds Domain/link notification tests, leaving mapping words integrator-owned. The full processor top is byte-identical across pins, so there is no added port, parameter, register or required parent binding. The source audit records its hash.

The parent patch at `tb/verilator/milan_dp/sim_nxn.cpp:970` completes a frame already underway, bounded by 2,048 extra cycles. It neither relaxes an assertion nor drains arbitrary subsequent frames. The other patch removes exactly the two repaired declaration-order entries in `scripts/xvlog.budget:33`. Both match their upstream-required patch bytes after contextual application. Counter spacing remains measured at grant; the disclosed post-grant MAC-stall limitation is not converted into a wire-gap guarantee.

[R521] PASS RTL - `hdl/milan/KL_pp_shadow.sv:824`, `hdl/milan/KL_pp_shadow.sv:1177`, `hdl/milan/milan_datapath.sv:7899`, processor notification and SRP deltas, and `syn/ooc/pp_baseline.py:559` - Parent boundaries and the added flow option preserve their contracts.

The wrapper still admits complete control frames through its frame FIFO before byte serialization, drops oversize/full frames, counts loss and binds the unchanged top explicitly. The new notification register has an explicit reset and uses the existing descriptor-index width. The registrar priority changes preserve cancellation of obsolete timers on renewal. No parent clock/reset or CDC wiring changes. The measurement helper's opt-in worker setting adds only its leading synthesis parameter; default scripts are unchanged. Its focused self-test and 34 negative controls pass, including both new worker-cap controls.

All three lane dev merges reproduce the committed trees exactly with conflict-free `git merge-tree`. The final merge imports exactly 24 paths; every one is byte/mode-identical to dev. The lane does not edit the imported MAAP firmware. These checks are independent calculations, recorded in `source-audit.json`, not reliance on merge messages.

[R521] PASS Robustness - processor `tb/aecp_notify/sim_main.cpp:482`, processor `tb/srp_stream_fsms/sim_main.cpp`, parent `tb/verilator/milan_dp/sim_nxn.cpp:970`, and `syn/ooc/pp_resource_gate.py:310` - Waiting, expiry collision, reset, frame-boundary and policy refusal behavior was exercised.

Fresh focused notification tests pass 45/45; the SRP suite passes 1,347/1,347. Substituting the previous pin's notification RTL into the current tests produces five named TW/DR failures. Substituting both previous registrar FSMs produces sixteen SC1 collision failures spanning both planes, peer/own LeaveAll, variants and first/last contexts. These are expected failing controls in disposable copies. They establish that the new tests distinguish the fixed behavior from the old behavior.

Nine direct resource-policy probes pass their expected dispositions: unchanged data is accepted; excessive LUT/slice/RAMB36 use, BRAM reserve violation, setup/hold floor violations and an unrouted net are refused; removing the recorded worker setting is NOT COMPARABLE. These supplement the committed policy check without a new implementation run.

[R521] PASS Tests - `tb/verilator/milan_dp/Makefile:494`, processor focused suites, `tb/verilator/milan_dp_render/tdm8_render_mutants.py:524`, and the public per-leg receipts - Tests detect the adopted changes, and reused evidence is bound to unchanged inputs.

The real parent notification seam passes 421 checks. Removing only the added drain-loop condition produces exactly the expected `[NOTIFY-CRF] ...nor to A` failure, got 1 / expected 2, at 421 checks / 1 failure. The disposable source is restored afterward. `behavior-probes.json` and `drain-probe.json` distinguish these deliberate failures from clean runs.

The render proof was independently reconstructed using a temporary index at measured parent `342f20ef1fb29167c388b6f1fa3bc9851c3876e3`. Reversing the two public patches and replacing only the gitlink yields tree `55eaf2478515d3bc25b71ae5733ac3aea53ad8ef`. The exact diff is 1,917 bytes, SHA-256 `0871c0da9905ce89ff5b9850211b287cb5f56263ef9a16b2880144b76c7a21b3`, matching the public record. Its changed paths are exactly the gitlink, syntax budget and harness patch.

All 32 ordered leg records match on name, mode, return code, byte count, stdout hash, count lines and failing assertions. Regrading their required assertions yields 28/32 on both pins. Failed legs are indices 2, 8, 9 and 15: clean epoch, its two arrival-skew controls, and the surviving uncounted-repeat mutant. The first three each have the same four T30 recentre failures, 127 checks / 4 failures; the survivor has 58 checks / 0 failures. Both actual clean-epoch files are 3,746 bytes and hash to `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b`.

The reverted measurement's render source list, headers, harness/recipes, configuration and dependency pins also match source dev `e21c1ca0`. The adopted measurement's corresponding scopes match the reviewed head. Thus the four failures are the already tracked #657 cases at the reviewed dev inputs. The older #657 issue's 114-check output and earlier hash are historical; they are not falsely claimed identical to this later 127-check run. The 28 passing campaign cases do not establish validity of the failing epoch mode. The public ruling permits this differential for this adoption only.

The 60-suite source sweep remains evidence at `591a5752e6a587b28b501e2d02d6a9d0293f3ba2`, never relabelled as a final-head run. The 24-path import and dependency-scope comparisons support retention; the changed mailbox/firmware/documentation consumers have fresh receipts. Four field skips remain visible in that sweep; the separate field rerun records 899 checks with no failures/skips. The earlier 59/60 run and cancelled first-round run are not accepted sweep evidence. Full parent, processor, time-plane, synthesis and builder banks were not rerun by this reviewer.

[R521] PASS Docs - `docs/reference/SUBMODULES.md:158`, `docs/design/AREA_BUDGET.md:100`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:28`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:105`, boundary diagram assets and PR #692 body - Current claims match source and receipts, with material limitations stated.

Port and naming records, the ROM ledger and boundary assets reproduce the committed bytes twice in a disposable registered clone. The independent census is parent 2,079, processor 1,759 and time-plane 125 ports, with unchanged ratchets. Both current processor ROM hashes match the previous pin's rows. The boundary PNG was visually inspected; it identifies the current pin and wrapper legibly. The submodule table and diagram gates pass.

Combination F and timing

| Endpoint | LUT | FF | Slice | BRAM tiles | DSP | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---:|
| Shipping route 1x1 | 49,957 | 54,274 | 15,734 | 87.5 | 14 | +0.124 / +0.031 |
| Standalone 1x1 | 23,179 | 19,779 | Not gated | 17.5 | 8 | -3.562 / +0.159 |
| Standalone 8x8 | 30,135 | 27,380 | Not gated | 23.5 | 8 | -2.278 / +0.159 |

Standalone timing lacks I/O constraints and is not integrated timing acceptance. The route uses 78.80% LUT, 11,917 above the 38,040 target, and leaves 116 slices. The 60% objective remains unmet, explicitly retained by the owner decision; #640 owns the redesign. The required #232/#230/#639 work is already contained in the preceding `ead80360` pin: commits `c050d971`, `07b1469d` and `ead80360` are ancestors of that second adoption. This third adoption does not bypass the ordering rule. The resource policy is unchanged; combination F's rebaseline records the merged parent packetizer input and the already recorded synthesis worker setting.

| Route | Slow 0C and 85C WNS / WHS | Fast 0C and 85C WNS / WHS | Complete image claimed |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.124 / +0.059 | +1.246 / +0.031 | Yes, selected |
| AltSpreadLogic_high | +0.090 / +0.040 | +1.642 / +0.011 | No |
| ExtraTimingOpt | +0.055 / +0.057 | +1.588 / +0.020 | No |

Every corner meets +0.03 ns setup / 0 ns hold; all TNS/THS values are zero. All three routing-status receipts report complete routing and zero routing errors. The selected implementation has no emitted critical warning or rejected constraint in its receipt. Alternative logs retain pre-final Route 35-39 warnings. Positive slack does not clear the selected route's 46 no-input-delay entries, 87 no-output-delay entries or ten CDC-10 diagnostics.

The selected bitstream is recorded as 3,825,992 bytes with SHA-256 `613a670a15dc7dce29c9cce0a1fc75527229575f7b43968dce6a444ffc80a8bc`; the manifest binds it and the 7,512-byte AEM and regenerates identically. Offline image preflight returns zero. The schema's `complete:false` is the repository's bare-metal layout convention, not evidence that physical acceptance ran. All 37 complete-image artifact entries match the exact-head 185-artifact retention receipt. The published recipes, per-corner data, image bindings and report hashes are mutually consistent and provide replay identities. Raw implementation artifacts were not opened or rerun by this reviewer.

Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/rulings; pin delta; parent patches; resource/capture records; render and timing acceptance evidence | R521-1 | 5428b044176f95248e6916dc00dd89c0df154078 |
| RTL | CLEAN | Processor notification/SRP/declaration changes; parent wrapper/datapath; baseline helper; computed merges and 24 imported paths | R521-1 | 5428b044176f95248e6916dc00dd89c0df154078 |
| Robustness | CLEAN | Notification TW/DR, registrar SC1, frame-drain controls, reset/index review, resource-policy refusals | R521-1 | 5428b044176f95248e6916dc00dd89c0df154078 |
| Tests | CLEAN | 421-check parent seam; 45-check notification and 1,347-check registrar suites; old-RTL controls; 34 helper mutants; all 32 render leg receipts and source closure | R521-1 | 5428b044176f95248e6916dc00dd89c0df154078 |
| Docs | CLEAN | SUBMODULES; area baseline/budget; measurement recipe; regenerated records/diagram; PR body and immutable public evidence | R521-1 | 5428b044176f95248e6916dc00dd89c0df154078 |

Findings and prior-findings reconciliation

No new findings. After writing this verdict and ledger, the reviewer checked PR #692 issue comments, formal reviews and inline comments. The thread contains only the two manager review-start comments; there are no prior public reviewer findings to resolve or retain. `prior-findings-inventory.json` records that inventory. No other reviewer report was read.

Limits and pending manager duties

- This is an adoption review of the stated source head, not a universal compliance or hardware verdict. The known #657 exception, 60% LUT shortfall, post-grant stall limitation and timing coverage diagnostics remain disclosed under their existing authorities.
- Physical calibration NOT RUN, field skips and successful offline image preflight are not hardware proof. Hardware acceptance 5 is not graded.
- Large archived measurements were reused only where their public source closure was independently checked. The public packet contains structured receipts and hashes, not all raw implementation reports. This review did not rehash the private implementation binaries/checkpoints. Full-bank results are attributed to their recorded heads and authors.
- The read-only hosted snapshot records successful exact-head `rtl-fast`, successful synthesis shards and several other jobs, while exhaustive simulation shards, documentation and elaboration were still in progress. The physical job was skipped. A skipped context is not an executed hardware test. Protected hosted contexts and local workflow-replica acceptance remain the manager's duty.
- Live dev was rechecked as `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`; it is an ancestor of the reviewed source head. The manager must finish all hosted/local obligations, collect the other independent verdict, validate the final current-dev candidate, obtain merge authorization, perform containment and hardware acceptance, then close the issue and move it to Done. None is discharged by this source verdict.
- One reviewer launch used an unsupported compiler concurrency spelling and failed before compilation; it was corrected to the supported four-worker form. The failed launch receipts remain separate. Final behavioral probes used at most two concurrent builds and four compilation workers per build. All processes ran under foreground supervisors and were collected to completion.
- Exact original checkout blobs, modes, index tree and the three required initialized submodule pins are verified in `source-audit.json`. The unused historical submodule remains uninitialized. Disposable builds and mutated copies stay under `scratch/` and are excluded from publication.

Reproduction and receipts

From the exact candidate with its three required submodules initialized, fetch public evidence commit `8d4e0732588d09f1f94f41aea7c7c39110da09a2`, then run `audit_sources.py` and `audit_evidence.py`. Run `run_focused.py static --verilator <pinned-5.050>` and `run_focused.py units --verilator <pinned-5.050>`, followed by `probe_behavior.py <pinned-5.050>`, `probe_records.py` and `probe_drain.py <pinned-5.050>`. Run from the candidate root; scripts place disposable data beside themselves under `scratch/`. They require the repository's documented dependencies. No command starts a detached job. Each campaign driver waits for every subprocess.

`MANIFEST.sha256` enumerates all publishable scripts, audit results and raw receipts. Paths in logs are replaced by neutral placeholders before hashing; no behavioral output is removed. Only manifest-listed files and this report are publishable.

R521-1 FINISHED
