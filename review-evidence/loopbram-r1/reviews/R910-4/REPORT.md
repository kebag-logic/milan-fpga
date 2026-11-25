[R910] NEGATIVE - exact head 09201d35d7ea720b3ba205da185ba35c159ec24a

External independent review R910-4 of issue #979 / PR #987.
Tree: a3b3dca8a55b738e714ada4662a309a50118a481.

One MAJOR evidence gap and one MINOR documentation defect remain. The import fix, provisional timeout registration, planner integration and leaf interface adaptation pass the focused checks. No runtime defect in the unmodified loopback implementation was established.

**Scope and independence**

The exact head and [public review start](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7168575843) govern this report. The brief's three-commit range, 9acb9b82..c413d33a, is a strict subset of that head. Five subsequent first-parent commits add a documentation correction, merge dev-soft-core 5de21ff3, increase the worker count, register the firmware builder, and adapt the leaf interface. The full base-to-head diff and history were used to identify dependencies; untouched implementation retains prior coverage. See history.txt, requested-delta.diff, post-merge-delta.diff, delta-paths.txt and source-comparison.json.

The original source base is 3cda030c174b325e36c26af6420487ff91346d15. The PR currently targets dev-soft-core at 5de21ff3661436ea5598718aca36934361e35340; that commit is an ancestor of the reviewed head. This does not validate a future merge against live dev.

Context was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/979), its [option-B ruling](https://github.com/kebag-logic/milan-fpga/issues/979#issuecomment-7096503041), REQUIREMENTS.md REQ-VER-01..04, docs/design/INPUT_MAPPED_LOOPBACK.md, the relevant module/interface contracts, and the [#818 routing rule](https://github.com/kebag-logic/milan-fpga/issues/818). The unchanged Milan/IEEE mapping interpretation retains R910-3's coverage; this round does not claim a fresh full standards audit.

All five lenses were applied independently. An initial verdict and ledger were written before reading another reviewer's prior public findings. Only historical public findings were then reconciled; no concurrent review report, private implementation material or management source bank was read. No GitHub writes occurred.

**R910-4-F1 - MAJOR - Conformance, RTL, Tests - current enabled routing acceptance is unproved after the dev merge**

Artifacts: hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv:20; hdl/milan/milan_datapath.sv:8048; merge 7049c524c45e0f3d1e6ba17b93208c0bb4e59a85; docs/design/INPUT_MAPPED_LOOPBACK.md:397; public author-r7/PR-BODY.md:66-72; source-comparison.json.

Authority/evidence: #979 requires both shapes routed at #818's floor. The design authority requires source-bound measurements, best-of-three selection, setup at least +0.030 ns and nonnegative hold at every signoff corner. The only published enabled routes predate the merged dev changes; the current PR explicitly acknowledges that limit. The merge changes four synthesized receive-path files, including the depacketizer, context monitor, parser and their parent connections. It also changes other build inputs. These are dependencies of the enabled integrated implementation even though the loopback queue/capture source itself is unchanged.

The historical 8x8 result (+0.223 ns setup, +0.036 ns hold) and 1x1 result (+0.124/+0.036 ns) remain valid evidence for their recorded sources. They are not measurements of the reviewed composition. No current enabled route or physical-input equivalence proof is present in author-r7. R910-3's positive verdict remains valid at 9acb9b82; it does not bank changed physical dependencies at 09201d35.

Impact: the mandatory routing result for the current enabled 1x1 and 8x8 implementations is unknown. Simulation, disabled firmware/image equality against dev, and historical mailbox critical paths cannot establish current placement/routing slack. This finding does not assert that either current shape fails timing.

Required outcome: publish source-bound routing/resource receipts for both enabled shapes at this implementation or the final reviewed candidate, using the unchanged recipe and bounds. A final-candidate measurement can satisfy this once; a duplicate source-head route is unnecessary. Alternatively, publish an explicit acceptance change. S14 overflow permission alone does not waive routing.

Verification: identify source inputs, configuration, selected directive, LUT/FF/BRAM/slices/DSP, all signoff corners and routing status. The selected result must meet +0.030 ns setup and 0 ns hold throughout, with the ordinary enabled-8x8 allocation refusal retained. Independently re-review those receipts. This carries forward the cause addressed by R910-2-F2 / R909-2-N2, newly uncovered by changed dependencies rather than reversing their historical closure.

**R910-4-F2 - MINOR - Docs - handoff attributes an external approval to an unreviewed head**

Artifact: [author-r7/REVIEW-READY.md:5](https://github.com/kebag-logic/milan-fpga/blob/73eaef87e14c2d299d0f63fda15c3251c0ca1512/review-evidence/loopbram-r1/author-r7/REVIEW-READY.md#L5).

Authority/evidence: AGENTS.md banks review coverage against the exact reviewed commit. The handoff says R909-5 and R910-3 were both POSITIVE at 1516b2ffe321337858389ec8e42897f8a80644bb. The [actual R910-3 verdict](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7137772914) names 9acb9b828b29aba71bd51303a4836f86c2278267. R909-5 names 1516b2ff.

Impact: the handoff falsely suggests independent external coverage of commits that R910-3 never reviewed. This is a verdict/head claim, explicitly excluded from wording-only RESIDUE.

Required outcome: replace the parenthetical with “R909-5 POSITIVE at 1516b2ffe321337858389ec8e42897f8a80644bb; R910-3 POSITIVE at 9acb9b828b29aba71bd51303a4836f86c2278267.” Publish the correction with the evidence rather than altering a historical reviewer verdict.

Verification: both reviewer/head pairs agree with their public verdict lines, and no completion ledger uses the incorrect attribution.

**Requested fix verification**

| Check | Result | Evidence |
|---|---|---|
| Hosted import failure | Confirmed at cause | Jobs 138601303963 and 138602447405 check out with submodules:false, then fail test_builder.py --list with exit 2. hosted-log-excerpts.json retains timestamped excerpts. |
| Independent no-submodule reproduction | Old head exits 2; c413d33a and 09201d35 exit 0 | old-list.log, fixed-list.log, head-list.log and their rc receipts. No processor contents were copied into the exported probes. |
| Inventory identity | Exactly 114 names, byte-identical | SHA256 acc4d933d03afea09650fdd05df5400900fc1bf09960225b6980e01ef519c7fc. Compared both fresh outputs with the published old-with-submodule payload, excluding only its added provenance header. |
| Import placement and execution | Correct; focused builder test passes | test_input_loopback.py:15-35 matches the established local-import pattern in test_declarations.py:41/:437. Assertions and fixtures were retained. head-builder-focused.log. |
| Provisional contract at c413d33a | PASS | Both suites have their own 300 s timeout arms and provisional 300 s figures. fixed-planner.log; all 19 listings exit 0, 85 unique units, each new suite exactly once. |
| Contract at current head | PASS | head-planner.log; all 27 listings exit 0, 96 unique units. New suites belong to workers 14/15. Largest regular projection is 1275 s against 1276 s; continuous media-clock exception is 1530/2160 s. |
| Runner contract falsification | PASS | Removing either timeout arm or changing either to 301 s is rejected. probe-summary.log. measure_test_evidence.py self-test passes 105/105. |
| Generated workflows | PASS | ci_suite_workflows.py --check and ci_gate_workflows.py --check, with raw log/rc receipts. No workflow was executed locally. |
| Leaf adaptation at exact head | Independently PASS at both shapes | leaf.log: 8x8 79,587 checks, 468 packets; 1x1 76,017 checks, 447 packets; zero failures. Verified supplied executable reports version 5.050. |
| Published parent campaign | 17 successful expected-outcome records | Two controls and fifteen built runtime-failure plants; current campaign source enforces the named sample or per-stream assertions. receipt-audit.json and the published campaign summary. Individual parent runtime logs were not republished in author-r7, and this round did not rerun the campaign. |
| Firmware builder registration | Correct category and commands | ctrl_configs.py:140; input_loopback_dp/run.py compiles five AECP C sources into its linked library. Both shapes are registered as build-only and requiring the simulator. Published capture judge passes 202 controls; removing the entry restores the named text-cross-check refusal. |
| Current default builder/firmware identity | Published author evidence, verified packet | Both shapes' 12 builder artifacts and descriptor images equal dev; all twelve composition firmware load images equal dev. This is not a fresh proof of current whole-FPGA netlist or bitstream identity. |

The leaf adaptation supplies N_STREAMS_P, uses the flat monitors' accept vector as the completed mask, and asserts enqueue/done together. This matches the current depacketizer's queued/completed verdict contract and the repository's flat-monitor wrappers. Production parent wiring uses the context monitor's separate verdicts. The two independent leaf runs exercise the adaptation at both approved sizes; no new reset domain, map ownership or buffer-validity rule is introduced.

The new 300 s arms are a coherent implementation of the planner's provisional rule, consistent with reboot_ctrl. Registering the old default 1800 s arm cannot satisfy either regular-worker budget. The current extra worker follows the documented add-a-worker outcome without reducing either timeout. Measured hosted windows remain owed to the later round specified in the brief.

**Hosted evidence**

At c413d33a, docs run 45459575153 succeeded, including docs-check job 138705737874. Elaborate run 45459575049 has an overall cancelled result, but all five gate jobs and its elaborate aggregate 138701767114 succeeded. Thus the two original aggregate failure paths demonstrably pass after the import fix.

The other required results were not all green. rtl-fast 45459574928 was cancelled. In rtl-full 45459575001, all 19 suite workers and all four portability workers were cancelled; the downstream unions and aggregates failed for missing/cancelled worker evidence. The suite aggregate reports 4 of 19 directories, and portability reports 0 of 4. These logs support cancellation fallout, not an executed loopback or portability defect. Cancellation is not a pass and does not establish the initiating cancellation cause. The physical job was skipped.

For 09201d35, hosted-head-snapshot.json records the observation time and jobs from runs 45657606171, 45657606201, 45657606423 and 45657606190. Docs and elaboration were in progress; substantial fast/full work remained queued or running. wire-accountability, docs-check-no-git, bdd-conformance and Verilator preflight had successful executed jobs. Physical gPTP was skipped. No final required-context acceptance or measured hosted loopback window is claimed. The manager owns hosted/local-replica acceptance; this review did not wait for it or execute a replica.

**Prior public finding reconciliation**

Historical [external R910-3](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7137772914) and [internal R909-5](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7142170551) dispositions were checked against the earlier finding texts and current changed dependencies. Earlier positive coverage is retained only for unchanged causes.

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R910-1-F1; R909-1-F3 | Resolution retained | Real enabled parent mapping-store/AECP integration and both-shape connection plants are unchanged. Published current-dependency parent campaign has passing controls and detected plants. |
| R910-2-F1 | Resolution retained | sim_main.cpp:600-647 still grades delivery/completeness per stream in both phases. All nine held-output cases remain in the 17-case campaign and require four named failures. |
| R910-2-F2; R909-2-N2 | Historical closure retained; current coverage lost under F1 | Changed synthesized receive/parent dependencies invalidate transfer of the old route evidence. |
| R909-1-F1 | Resolution retained | No regression to repaired queue/parent mutation anchors. Queue/capture sources are unchanged; imported driver changes use the staging helper. Published queue result includes the 28-control campaign; no new full campaign rerun claimed. |
| R909-1-F2 | Prior optional-path correction retained | Disabled generate branches, original ports/instance boundaries and mapping writer are unchanged. Current author default artifacts/load images equal dev. Old canonical netlist results are historical; current integrated physical equivalence is not inferred. |
| R909-1-F4 | Permitted documentation outcome retained | Five guards remain explicitly untested in isolation in the leaf README, design and parameter contract. No isolated mutation guarantee is claimed. |
| R909-1-F5/F6 | Resolution retained | Unchanged eight-page retention, lead >2 refusal and derived timestamp window; current published leaf bounds reports both shapes' control/inside/outside/lead3 outcomes. |
| R909-1-F7 | Resolution retained | Queue/capture contract banners and packed-field parameter documentation remain unchanged. |
| R909-2-N1; R909-3-N1 | RESOLVED | Both suites are registered, provisional and tied to their 300 s arms; independent planner and listing evidence above. Hosted replacement remains a scheduled follow-up obligation, not a completed measurement. |
| R909-2-N3 | Resolution retained | TESTING.md:381 still registers parent controls and explicit mutation campaign with affected artifacts. |
| R909-4-N1 | RESOLVED | CI_WORKFLOWS.md:687-688 now lists both loopback budgets and reboot_ctrl, matching the driver and provisional set. |
| R909-1-R1/R2/R3; R910-1-R1; R909-2-R1; R909-4-R1 | Corrections retained | Design attribution/public pointer/fresh-measurement wording, builder row order, bind-only guard qualification and selector-docstring wording remain corrected. |
| R909-1-S1; R909-2-S1/S2 | Addressed, retained | Split NAME capacity disclosure, both-shape connection plants and canonical-input reproducibility limit remain. |
| R909-2-S3/S4 | Optional, unadopted | Release-clock parent execution and the unused one-past map read remain outside proven claims. |
| R909-3-S1/S2/S3; R910-3-S1 | Optional, retained | One-packet completeness margin, bounded standalone waits, durable historical placement sensitivity and parser-range controls remain unchanged suggestions. |
| R909-4-S1 | Optional, retained | Old cold-run wall times/CPU mask/load claims are not newly authenticated by make logs. Current author summary timings and this review's executions are distinct evidence. |
| R909-4-S2 | Optional, retained | A permanent no-submodule inventory regression remains useful; this review provides a portable probe, not a source fix. |
| R909-4-S3 | Addressed for this publication | Top-level MANIFEST.json includes post-normalization hashes; all 223 selected published files verify. Original nested pre-normalization hashes are not mistaken for published-byte hashes. |
| R909-5-S1/S2 | Optional, retained | Clarify cold runs as timeout margin rather than the planner figure's derivation; remove the stale numbered-step reference. The latter predates the PR, so it is not a newly introduced defect. |

**Retained RESIDUE: R909-5-R1 - Docs**

Artifact: docs/testing/CI_WORKFLOWS.md:680-682.
Authority/evidence: the preamble says measured hosted worst case plus margin sets every named entry, while the immediately following rows correctly identify provisional entries.
Impact: wording inconsistency only; the rows and executable figures are already correct.
Exact fix: “The measured hosted worst case plus a stated margin sets each named entry, except a provisional one, which keeps its own arm until its hosted window is measured:”
Verification: retain every numeric row and check; read the corrected preamble and run the normal documentation checks. This residue does not unclean a lens.

No new prohibited lane/reviewer/round/comment identifiers were found in this change's source-comment additions. Findings prose may name review identities. The stale “step 3” parenthetical in suite_shards.py:151 is the existing R909-5-S2 suggestion: change it to “the module docstring's new-suite contract” during a suitable edit.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #979 ruling; INPUT_MAPPED_LOOPBACK.md:397-411; focused builder contract; changed route inputs and F1 | R910-4 | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| RTL | UNCLEAN | Depacketizer verdict contract; milan_datapath receive wiring; loopback_wrap.sv:64-70; independent both-shape leaf logs; F1 physical gap | R910-4 | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Robustness | CLEAN | Old/fixed no-submodule controls; timeout deletion/value rejection; leaf reset/invalidation/absence scenarios; retained guard bounds; parent campaign records | R910-4 | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Tests | UNCLEAN | 114-name byte identity; 19/27 shard listings; planner and 105-arm evidence self-tests; current leaf; firmware builder capture; mandatory routing evidence F1 | R910-4 | 09201d35d7ea720b3ba205da185ba35c159ec24a |
| Docs | UNCLEAN | CI policy budget/projection tables; TESTING.md:468-479; source comments; public packet and PR; incorrect exact-head approval attribution F2 | R910-4 | 09201d35d7ea720b3ba205da185ba35c159ec24a |

[R910] PASS Robustness - probe-summary.log, leaf.log, receipt-audit.json, tb/verilator/input_loopback_dp/sim_main.cpp:600-647 - applied missing-dependency, timeout, invalidation and per-stream delivery checks; no open finding under this lens.

**Integrity, reproduction and limits**

The public evidence commit is [73eaef87](https://github.com/kebag-logic/milan-fpga/tree/73eaef87e14c2d299d0f63fda15c3251c0ca1512/review-evidence/loopbram-r1). All 223 selected author-r6/r6b/r7 files match their published SHA256 values. GitHub reports that commit unsigned, so this review verifies content checksums and pinned-publication provenance, not a cryptographic signature. The initial evidence fetch obtained the parent object but recursively requested unavailable unrelated submodule objects; those failures were not used as evidence or followed by checkout changes.

verify_packet.py reproduces the packet checks and receipt audit. probe.py runs the focused no-submodule, planner, inventory, generator and timeout-contract probes from this exact checkout, with disposable exports under packet/scratch. It reuses matching command/exit receipts when present; use a fresh packet directory for fresh execution. execution-identity.json records the independent leaf command and verified executable identity. Use the supplied executable as SIMULATOR and an absolute PACKET path. Maximum compiler concurrency was sixteen. Commands remained foreground; no detached work remains.

verify_checkout.py directly verified 1,983 parent blobs and initialized submodule contents, modes, index and pinned heads: gptp-processor 120 blobs, protocol-processor 868, lwSRP 67, tsn-c-stack 100 and verilog-axis 214. The external gitlink is intentionally uninitialized. checkout-integrity.json records exact pins and clean tracked status. No product-source edits occurred and no restoration was needed.

No full parent/processor/gPTP/portability/builder bank, physical implementation, hardware operation, Docker/local-replica execution, commit, push, merge or GitHub write was performed. Published source-head receipts are author evidence. No manager source bank at this head is claimed or inferred. Physical calibration is NOT RUN; field skips, implementation routing and simulation are not hardware proof. Five isolated defensive guards and release-clock parent execution retain their explicit limits.

Manager duties: resolve F1/F2 and obtain exact-head re-review; carry the retained residue and optional suggestions; complete hosted/local-replica and full local-gate acceptance; collect the independent internal verdict and verify no review remains in flight. Build and validate the final current-dev candidate with builder/native bank receipts at merge time. The brief supplies live dev e275d7950ef3385753e6a15d2e191ba855b171ed, but the actual live tip at that turn is authoritative. Source validation does not establish that later composition. Retain enabled-8x8 S14 debt and allocator refusal, unchanged owner memory/service bounds, explicit merge authorization, post-merge containment and issue/project completion.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. scratch/ is excluded.

R910-4 FINISHED
