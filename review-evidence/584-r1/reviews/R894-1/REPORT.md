[R894] NEGATIVE - exact head 2b295a44d136275ccbf060fe4f36c42e573b6460

External independent review, round R894-1, issue #584 / PR #975. Tree `d18031d79799e3e765e05b82528cbcc40b0af332`. Reviewed the 17-commit delta from `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`, the reviewed flip head. All five lenses were applied. Two MAJOR and three MINOR findings remain open. This is not merge approval.

The descriptor correction satisfies the examined cluster-count, mono-channel and input-map rules. Focused serializer, mutation and added reset/boundary probes pass. Approval is withheld for an unresolved owner-scope deviation, missing shipping-shape mapping-to-wire coverage, contradictory current documentation and three receipt-index mismatches.

**Authorities and reconstruction**

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md, the issue's acceptance and public scope decisions, linked authorities, then the diff/history and public executable evidence. The supplied November 22 owner instruction governs the backing decision. Public scope/evidence: [TAKEN+DECISION](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7077045073), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7083459655), and [processor #122 disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588). Processor #122 retains the cluster minimum; a zero-row dynamic map does not authorize zero clusters.

Examined Milan v1.2 5.3.3.7–5.3.3.9 and 5.4.2.26–5.4.2.28; IEEE 1722.1-2021 7.2.13, 7.2.16, 7.2.19 and model-identity authority 6.2.2.8 / issue #495. Read ENDSTATION_BUILDER D1/D2/D7/D8/D10, PP_DESCRIPTOR_OWNERSHIP, CHANNEL_MAP_64 and the saved-state/control-memory contracts. No private author material, management material or another reviewer's report was used to construct this verdict and ledger.

Public receipt paths below are relative to [author-r1/receipts at immutable evidence commit 4ee921e6](https://github.com/kebag-logic/milan-fpga/tree/4ee921e6bb38b753a83701cf89dfb6105739808d/review-evidence/584-r1/author-r1/receipts). They are author execution evidence, not independent reruns or manager source-bank results.

**Findings**

[R894] MAJOR Conformance, Docs — F1 — configs/endstation_ax7101_8x8.yaml:204, :222, :263; docs/ENDSTATION_BUILDER.md:744; PR description — The implemented backing needs an explicit owner disposition

- Authority/evidence: the owner decision supplied for 2026-11-22 10:00 says to back the model with the loopback lane and first TDM8 channel only. This head gives input port 0 TDM32 slot 0 and ports 1–7 logical unrouted destinations. No input cluster is backed by loopback; the 8x8 loopback fabric remains disabled. The author explains these facts but describes them as fulfillment of the owner's decision. That author interpretation does not establish approval of the deviation; the older unrouted-fallback approval does not settle the later instruction.
- Impact: fulfillment of the frozen product scope is unresolved. The difference affects delivered audio, not merely a channel name. This finding does not claim Milan requires a physical jack for every cluster.
- Required outcome: record the owner's disposition of the actual topology: no loopback-backed input cluster, loopback disabled in 8x8, and TDM32 slot 0 standing for the requested first TDM8 channel. Either approve that scope explicitly and align the decision/PR/docs, or deliver the requested backing. Do not name an unrouted cluster as loopback when input mappings cannot steer its clone feed.
- Verification: compare the authoritative disposition with the generated descriptor/projection tables, build parameters and observable mapping behavior. The executor's technical explanation alone does not close the scope decision.

[R894] MAJOR Tests, Robustness — F2 — tb/verilator/milan_dp/Makefile:841; tb/verilator/milan_dp/sim_nxn.cpp:10542; tb/verilator/tdm_render/master_bus_wrap.sv:45 — No executable proof of the new shipping mapping-to-wire path

- Authority/evidence: the repository requires self-checking changed behavior and practical integration coverage; TAKEN includes shipping loopback-off and loopback-on datapath legs. `nxn8` supplies `N_STREAMS=8` and `LOOPBACK_P=1`, but no physical render parameters. `SHAPE_8x8` is an include path. Defaults in hdl/milan/milan_datapath.sv:135, :145 and :195 leave bus slots, master and render slots zero; `g_tdm_render_parked` at :8663 drives `tdm_dout_o` low. The new assertions read map pages and render RAM key 2, not serialized media. The standalone bus wrapper writes the serializer bank directly, with epoch/freshness tied constant, bypassing the listener queue, mapping projection and datapath adapter. Existing `milan_dp_render` covers full-width TDM8, not eight listeners with a one-slot lane on TDM32. `static-and-provenance.txt` reproduces the parameter evidence.
- Impact: a defect in the one-slot adapter composition, bus binding or shipping feature-off path can pass the supplied tests while AECP responds correctly and the pin is silent or wrong. Unit mutations and synthesis/lint do not exercise this boundary.
- Required outcome: execute a self-checking datapath test with the 8x8 generated shape, loopback off, master TDM32 and one render slot. Drive identifiable received audio through the real mapping/queue/crossbar/adapter path; check slot 0's selected sample, zero slots 1–31, REMOVE-to-silence and no routing changes from unrouted ports. Cover reset/bind freshness there. Retain the loopback-on control. Exercise the product control face or establish the equivalence of the tested face.
- Verification: publish positive receipts and focused faults at the projection/adapter/bus-binding boundary that the new test detects. The reviewer unit epoch/reset probes pass but do not close this integration gap.

[R894] MINOR Docs — F3 — docs/design/SPLIT_CONTROL_MEMORY.md:313; PR description, Firmware memory row — Uniform memory-growth claim contradicts the measurements

- Authority/evidence: the preceding table and public firmware ledger/fixture/variant receipts distinguish the points. Product 8x8/2if SRAM grows 115,504 → 117,312 B: 1,808 B, not 1,744. Fixture 8x8/2if ROM grows 131,536 → 132,880 B: 1,344 B, not 1,336. The other two rows have the stated 1,336/1,744 deltas. `static-and-provenance.txt` reproduces this arithmetic.
- Impact: the budget explanation makes a false quantitative claim. The per-point caps need not change, but the measurement summary is unreliable.
- Required outcome: state the per-point deltas or correctly qualify the common delta, in the authoritative page and PR. Preserve the distinction between the representative fixture and its maximum variant allocation.
- Verification: recompute the prose's deltas from the published base/head image sizes. This changes a measurement claim and is MINOR, not wording-only RESIDUE.

[R894] MINOR Docs — F4 — docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:86; docs/ENDSTATION_BUILDER.md:1132; docs/design/SAVED_STATE_FORMAT_32X32.md:90 — Current summaries still describe the removed zero-cluster waiver

- Authority/evidence: ownership rule L1 still says zero-cluster 8x8 pools violate the minimum and #584 owns the correction, without identifying the new named refusal. Builder row 45 says the 8x8 YAML declares the waiver, though it no longer does. The saved-state page puts the regenerated 427-name census beside prose saying the board routes no physical audio and listener ports have no cluster until #584. That describes the old 11+12N model, not the displayed 11+13N model. F5 in the ownership document and builder D8 are updated, leaving the same current authorities inconsistent.
- Impact: a cold reader cannot consistently reconstruct the current cluster contract, enforcement or name census from the required entry points.
- Required outcome: update these current statements to one cluster per input port, the named minimum refusal and absence of the waiver. Label any retained history with its old head and separate it from current figures.
- Verification: reconcile all three locations with current YAML, generated descriptors, `cluster_layout` and the regenerated census. These model/conformance and figure claims are not wording-only RESIDUE.

[R894] MINOR Tests, Docs — F5 — public author-r1/receipts/INDEX.md, gates/ rows — Three execution-receipt hashes and sizes do not match publication

- Authority/evidence: hashing all 80 indexed blobs at `4ee921e6bb38b753a83701cf89dfb6105739808d` finds 77 matches and three mismatches. `gates/builder-leg-1.json` is 16,615 bytes, indexed as 16,621; `gates/builder-leg0.txt` is 50,272, indexed as 50,280; `gates/builder-leg1.txt` is 42,948, indexed as 42,954. Their SHA-256 values also differ. Actual/indexed hashes are in `static-and-provenance.txt`; `review_checks.py` reads immutable Git blobs directly.
- Impact: the supplied integrity index cannot authenticate these builder receipts. The immutable contents remain readable; this does not allege falsified results or invalidate independently rerun checks.
- Required outcome: publish a corrected index of the exact public bytes, identifying any intentional normalization before publication. Do not silently substitute different execution results.
- Verification: every indexed size/hash matches its published blob. Evidence identity is substantive, not RESIDUE.

**Independent lens results**

Conformance: regenerated all five tracked configurations in both placements. `configs-head.json` enumerates packed descriptors: every input/output port owns at least one cluster, every AUDIO_CLUSTER has channel_count 1 and every input port has zero AUDIO_MAP descriptors. The 8x8 has eight one-cluster input ports and 80 clusters total. Both-direction minimum refusals and guard mutants pass (`declarations.log`). Milan 5.3.3.8 permits an honestly named logical destination; IEEE 7.2.16's invalid signal fields are appropriate. Examined map storage, GET, non-empty REMOVE/re-add and invalid-list behavior against 5.4.2.26–28 in firmware and nxn8. F1 leaves Conformance UNCLEAN.

[R894] PASS RTL — hdl/ieee1722/aaf/KL_tdm_render_master.sv; hdl/milan/milan_datapath.sv:1158, :8663, :8736; tdm.log, tdm-mutants.log, narrow-epochs.log — Checked bus/lane widths, one-slot indexing, zero tail, frame scheduling, CDC/epoch/reset handling and master/slave composition. Framing follows the bus; storage follows the lane; narrow slave lanes remain refused. Tests pass for 1-of-32, 2-of-8, 8-of-8, capture-master 1-of-32 and the existing slave suite; all five serializer mutants are caught. Added 1-of-32, 3-of-8 and 7-of-32 probes pass epoch closure, closed-epoch commits, producer reset while serial clock is stopped, freshness reopening and zero tails. No concrete RTL implementation defect was found. This clean source/unit result does not claim F2's missing integration proof.

Robustness: checked zero-cluster refusals, malformed/invalid map lists, first/last input ports, unrouted projection isolation, narrow-slave refusal, minimum/non-power-of-two stored-lane widths, full-width compatibility, reset and epochs. `Inputs.*` passes at all tracked configurations. Unit reset probes pass; F2 leaves shipping integration under reset/bind and feature-off configuration insufficiently checked. UNCLEAN.

Tests: examined declaration checkers and planted guards, firmware Inputs and public mutation receipts, nxn8's old-shape negative control, serializer checkers and five caught mutants. Independently executed the focused checks below. Reviewed the source builder/firmware/native regression account with the head limits below. F2 and F5 remain open. UNCLEAN.

Docs: checked D1's corrected input-map wording, D2/D8 counts/projection, D10 names, output-loopback explanation, processor #122 disposition, identity and saved-state/memory figures. Main new prose honestly says unrouted maps are stored/returned/saved but change no route. Keeping `render_ports: first` opt-in preserves the `every` default's 32x32 TDM8 saved-state bound (907 names); public `decision/render-ports-evidence.txt` records a global change would give 690 names and alter the 1x1 layout artifact. That compatibility choice is justified here, without approving untracked multi-listener physical aliasing. No new prohibited bench/reviewer labels were identified in added source comments. F1/F3/F4/F5 leave Docs UNCLEAN.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | issue scope; Milan/IEEE clauses; endstation_builder.py; five packed models; generated projections; test_aecp.cpp; sim_nxn.cpp | R894-1 applied; no clean covering round | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| RTL | CLEAN | KL_tdm_render_master.sv; milan_datapath master/slave arms/adapter; tdm.log; tdm-mutants.log; narrow-epochs.log | R894-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Robustness | UNCLEAN: F2 | test_declarations.py; test_aecp.cpp; sim_nxn.cpp; epoch/reset probes; nxn8 recipe | R894-1 applied; no clean covering round | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Tests | UNCLEAN: F2, F5 | tdm_render; milan_dp/nxn8; firmware Inputs; builder guards; public gates receipts/index | R894-1 applied; no clean covering round | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Docs | UNCLEAN: F1, F3, F4, F5 | ENDSTATION_BUILDER D1/D2/D8/D10; PP_DESCRIPTOR_OWNERSHIP; saved-state/memory pages; PR; receipt index | R894-1 applied; no clean covering round | 2b295a44d136275ccbf060fe4f36c42e573b6460 |

**Independent receipts and reproduction**

All execution `.rc` files contain zero. All children were joined before foreground commands returned. Bounded builds used at most 16 jobs; disposable trees are only in this packet's `scratch/`. No source fixes were made.

| Execution | Receipt | Result |
|---|---|---|
| Cluster minimum/input-pool declarations | declarations.log | PASS including guard mutants |
| AECP Inputs at five configurations | aecp-inputs.log | Both tests pass at each configuration |
| Slave and four master/bus legs | tdm.log | PASS |
| Serializer mutations | tdm-mutants.log | 5/5 caught |
| Added epoch/reset and narrow widths | narrow-epochs.log | 262 checks 1-of-32, 70 checks 3-of-8, 262 checks 7-of-32; no failures |
| Base/head generation and packed census, both placements | configs-base.json, configs-head.json, config-comparison.txt | Non-8x8 artifacts identical; 8x8 identity rotates |
| Saved-state capture/format/record-space checks | check_nvm_capture.log, check_nvm_format_32x32.log, check_nvm_record_space.log | PASS |
| Entity shape | check_entity_shape.log | PASS |
| Service oracle/flash self-test | fw-service-oracle.log | 55 oracle/19 flash checks pass |
| Parameter/arithmetic and receipt identity audit | static-and-provenance.txt | F2/F3 reproduced; F5: 77/80 indexed receipts match |
| Tracked bytes/modes/index and submodule pins | tree-integrity.txt | PASS |

The comparison is focused generation, not a full builder bank: baseline builder and baseline changed YAML with unchanged production dependencies versus the exact head. Seventeen in-memory artifact fields compare byte-identical for the 1x1 TDM8 and all three Arty configurations in both placements; this does not claim new physical builds. 8x8 identity rotates `0x001BC5F6CB4A37D1` → `0x001BC5CFD464421E`; 1x1 remains `0x001BC5CD179523AB`. Declared `render_ports` affects the model hash; other identities stay unchanged.

Portable scripts: `run_focused.py`, `run_audits.py`, `audit_configs.py`, `compare_configs.py`, `probe_narrow_epochs.py`, `review_checks.py`, `verify_tree.py`. Supply the checkout path where required; `compare_configs.py` reads the packet JSONs. Set `REVIEW_VERILATOR` to the required compiler; `compiler-identity.txt` records verified 5.050. Normal build dependencies and initialized required submodules are needed; `review_checks.py` also needs the immutable evidence commit. These scripts intentionally do not run full banks or routing.

**Public evidence assessment and real limits**

- Bounds: public builder census records 19,520 → 20,800 bytes, 124 → 132 descriptors, 80 clusters, 115 writable names and a largest descriptor of 452 bytes against the 576-byte response bound. Independent generation/shape checks pass within the applicable bounds.
- Memory: firmware ledger/fixture/variant receipts support 59.0 product 8x8/1if, 64.0 platform 8x8/2if, 57.0 fixture 8x8/1if and 61.5 fixture 8x8/2if. Product 59.0 is recorded debt of 3.0 against 56 under the loose-ROM/BRAM rule, not below-budget status. F3 concerns the byte explanation, not those caps.
- Saved state: split evidence is the two-interface 8x8 harness at 100 MHz CPU/system, not a measured 1if product: 172 records, 28.88803 ms CPU over 66.78489 ms elapsed; longest step 1.03861 ms under 20 ms. The base was not rerun at that clock. Four all-fabric 8x8 arms were remeasured: maxima 14.53320/14.34644 ms at 50 MHz and 10.94370/10.92626 ms at 100 MHz, on/off respectively, below 24.5 ms. The 1x1 receipt is carried unchanged.
- Routes: route/TIMING.md and three signoff receipts report worst-corner setup/hold +0.123/+0.015 ns, +0.363/+0.036 ns and +0.207/+0.036 ns, all clearing #818's +0.030 ns setup/nonnegative hold floor. Best is AltSpreadLogic_high. Executions are at `92fd1635`, not final-head reroutes. `route/inputs-routed-vs-head.txt` compares 17 inputs with no differences to `2d29d45a`, under its documented comment/hash/binding normalizations. The later two commits affect docs/measurement receipts/service oracle, not those route inputs. This is carried route evidence by input equivalence, not hardware or current-dev candidate proof.
- Regression account: two builder legs at `2d29d45a` cover 113 gates in union with two NOT RUN cases. Firmware shards are at `3a6563ae`; later relevant differences were examined. Native sweep shards at `2d29d45a` contain 64 passes and one stale-image refusal in fw_service_budget. Its final-head receipt closes that suite with 55 oracle/19 flash checks. The 65-suite account thus combines carried executions and a final-head rerun, not 65 fresh final-head runs. F5 limits three builder index entries.
- Oracle: examined gen_oracle.py conversion/validation, changed 8x8 row, budget/service-8x8-all-oracle-row.md and unchanged 1x1 rows. The row derives from a populated all-fabric run at `b1d164ef`, with image/log/trace checks. Independently reran the final-head self-test; this is not a fresh long firmware trace. Split service grading carries stated-cost evidence; the 64-part 8x8 source measurement was not rerun. The pre-existing all-fabric console-listing duty overrun is separately owned, not a new finding here.
- No manager source bank ran at this exact head and none is inferred. Source evidence is the author's published receipts plus the listed independent checks. Hosted/act acceptance belongs to the manager; this review did not execute or certify those contexts. Calibration NOT RUN and field skips are not hardware proof. No hardware, full parent/processor/gPTP/Yosys/builder banks, source edits, commits, pushes, GitHub writes or subagents were used.

The final integrity check verifies tracked superproject bytes/modes, stage-0 index, tree and initialized required submodule bytes/indexes against their pins. The uninitialized legacy `external` gitlink is verified as a gitlink only. Disposable builds/probes remain under `scratch/`, excluded from publication.

**Prior public findings and pending manager duties**

This independent verdict and ledger were written before the final public-thread reconciliation. At 2026-11-22 18:34 UTC, the PR's merged discussion/review timeline contained only the two manager review-start comments (7083496180 and 7083502647), with no prior finding or verdict to resolve or retain. The issue refresh still ended at the author's REVIEW READY comment 7083459655, with no subsequent owner disposition or manager source-bank receipt. The old area/capture STOPs are historical task decisions, not prior review findings on this PR; their changed split-era treatment was examined above. `public-reconciliation.txt` records this bounded observation.

Published logs retain raw command/test output with local checkout, packet and compiler installation paths normalized for publication; no measurement, result or return code was altered. Original local outputs stay in excluded scratch storage. Publication hashes were computed after normalization.

The manager must obtain F1's scope disposition, arrange fixes/re-review of open findings, collect required independent positive reviews and a current lens ledger with no review in flight, and accept executed hosted/act evidence separately from skipped contexts. At merge, validate the candidate against then-current remote dev; supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` differs from this review's `dd163e41` source base. Publish candidate builder/native receipts when produced. Merge needs explicit maintainer authorization, followed by containment and issue closure/Done. None of these future duties is claimed complete.

R894-1 FINISHED
