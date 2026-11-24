[R910] POSITIVE - exact head 9acb9b828b29aba71bd51303a4836f86c2278267

External independent delta review R910-3 of issue #979 / PR #987.
Tree: `fd76b3610f374ccf589e220ef60e83d84a71f6e1`.
Implementation base: `3cda030c174b325e36c26af6420487ff91346d15`.
Delta: `dc78aedae34c25a97125ecd6816a1f645db5575f..9acb9b828b29aba71bd51303a4836f86c2278267`, seven commits, 18 files.

All five lenses are CLEAN for this source delta. The delivery, planner, registry and routing findings are resolved at their causes. One optional parser-hardening suggestion follows. No new BLOCKER, MAJOR, MINOR or RESIDUE remains. This is source-review approval, not merge authorization or evidence that the final candidate passed its gates.

The review reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [issue and topology ruling](https://github.com/kebag-logic/milan-fpga/issues/979#issuecomment-7096503041), REQUIREMENTS.md, the input-mapping and descriptor contracts, and [#818](https://github.com/kebag-logic/milan-fpga/issues/818). The full base-to-head diff supplied dependency context; unchanged product code retains the preceding review's verdict under the requested delta policy. `independent-pass.md` records this review's independent verdict and ledger before earlier public findings were read. No private author material, another current review report or private management directory was read.

**Binding and verification**

`packet-verification.json` proves the seven commits and changed-file inventory. No non-Markdown `hdl/` file, any `sw/` or `configs/` file, workflow, or any of the six gitlinks changed. The only `hdl/` changes are three README files. The firmware/builder tree remains `374e7a0cda1737a4c346052d405405cbc80a6372`; configurations remain `645784f4fa209c130642a2955bae930b97b82957`. The overall `hdl/` tree changes because its documentation changes; it is not called tree-identical.

Evidence comes from [public commit 0f09f6ee](https://github.com/kebag-logic/milan-fpga/tree/0f09f6eeb886aa832b4401026be0d2c91dcdcb29/review-evidence/loopbram-r1), abbreviated `E/` below. All 1,148 round-4/5 files match the published SHA-256 manifest. All 426 round-5 receipt hashes match the inner-to-outer publication chain. Publication-normalized files are judged against their published hashes. The commit has no cryptographic signature header: this verifies Git object identity and manifests, not signer authentication.

`receipt-audit.json` checks all 17 parent-campaign runtime outcomes, twelve 8x8 timing-corner summaries against report text, both reconstructed disabled canonical payloads and all 43 docs replay steps. These are independently inspected author receipts, not independently rerun full banks. No manager source bank is claimed.

**R910-3-S1 - SUGGESTION - Robustness, Tests, Docs - extend numeric range checking in the changed test-control parser.**

Artifact: `tb/verilator/input_loopback/sim_main.cpp:21-30`; `E/author-r5/REVIEW-READY.md`, C/C++ idiom row; `env-parser.json` and `probe_env.py`.

Authority/evidence: the new helper checks token syntax but neither `ERANGE` nor representability as `int`. Compiling that exact helper gives `4294967296 -> 0`, `2147483648 -> -2147483648`, and a decimal exceeding `long` range -> `-1` on this host. Malformed `abc` and `1000x` correctly exit 2; unset and `1000` correctly return 0 and 1000. The handoff's “bounded strtol” description is stronger than the implementation.

Impact: an ad hoc oversized control can silently select another injected offset, including zero. The published bounds campaign uses fixed small values and is unaffected. This is optional hardening of unsupported test-control inputs, not an observed product defect or invalidation of the measured boundaries. It is not wording-only residue.

Suggested outcome: reject range errors and values outside the intended control domain before narrowing; keep that domain safe for subsequent multiplication. Describe the current conversion as syntax-checked until numerical bounds exist. Verification: retain unset/normal/malformed controls and add overflowing decimals that exit nonzero rather than wrap.

**Prior finding reconciliation**

Earlier findings were read from the [previous external round](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7125295409), [previous internal round](https://github.com/kebag-logic/milan-fpga/pull/987#issuecomment-7125672573), and their cited first-round findings after the independent pass. Original lens assignments are retained.

| Prior finding and lenses | Disposition | Cause-level evidence at this head |
|---|---|---|
| R910-2-F1 MAJOR, Conformance/Tests | RESOLVED | Parent `sim_main.cpp:487-524,594-647` counts words and packets per stream. Both phase endpoints require at least 16 packets, delivery within 48 words, and current plus peak backlog at most 48 words. The edit phase is graded before reset discards queues. Existing sample, silence, mapping and deadline assertions remain. |
| R909-2-N1 BLOCKER, Tests/Docs | Cause RESOLVED; complete-bank acceptance remains with manager | `suite_shards.py:111-112` registers measured 38/107 seconds. Independent planner self-test and all 19 driver listings pass, with one owner per new suite. Author driver shards 15/16 pass including preflight/tally. The PR now discloses the unrun complete serial sweep. Two shards are not called a complete-sweep pass. |
| R910-2-F2 MAJOR, Conformance/RTL/Tests; R909-2-N2 MINOR, Conformance/RTL | RESOLVED | Source-identical enabled 8x8 export and three recipes now exist; selected AltSpreadLogic_high meets every #818 corner. The round-4 enabled 1x1 route remains applicable because its implementation inputs are unchanged. Scripts, source binding, corner reports, resources and debt were examined. |
| R909-2-N3 MINOR, Tests/Docs | RESOLVED | `TESTING.md:354` registers parent controls/plants and triggers covering map writers, invalidation, talker enable, packed fields and harness changes. |
| R909-1-F1 BLOCKER, Tests/Docs | Prior resolution retained; delta checked | Queue anchor wrapping preserves the literal. `gates--anchors.log.txt` ends `ANCHORS INTACT 0`; queue log reports 28/28 including bind wipe. The corrected PHC-reset anchor is untouched. Current source-gate receipts replace the original mismatched evidence. |
| R909-1-F2 MAJOR, Conformance/RTL/Tests | Prior resolution retained; hashes rechecked | Enabled-only state/ports are untouched. Reassembled complete-release canonical payloads match published base/head hashes at both shapes; no implementation input subsequently changed. This is canonical structural identity, not raw bitstream identity. |
| R909-1-F3 MAJOR, Tests/Conformance; R910-1-F1 MAJOR, Tests | RESOLVED including the retained concurrency gap | Generated enabled parent shapes exercise production command handling, real map transactions, ADD/REMOVE/replacement, rejected/no-op edits, GET pages, clipping and in-copy edits. All destinations/talkers participate; delivery is now mandatory per stream. Both shapes have built, failing connection plants. |
| R909-1-F4 MINOR, Tests/Robustness/Docs | Prior permitted documentation outcome retained | Leaf README final section, design final paragraph and parameter contract identify bind-only flush, one-shot claim, expiry, backlog and age as untested in isolation. This follows the finding's explicitly allowed outcome; no mutation-proof claim or deferred defect is substituted. |
| R909-1-F5 MINOR, RTL/Robustness | Prior resolution retained | Queue `:782` refuses enabled lead >2; eight pages/full claimed address remain. Both lead-3 refusals and both built retention-plant sample failures are in the current receipts. |
| R909-1-F6 MINOR, RTL/Robustness/Tests | Prior resolution retained | Queue `:815-850` derives four clock cycles, 1000 ppm over K+1 periods and rounding. Both-shape 84 ns inside cases pass; 87 ns outside cases fail samples. Parser syntax changes leave these small values unchanged. |
| R909-1-F7 MINOR, Docs/RTL | Prior resolution retained | Capture `:338-346`, queue copy/clock-loss/flush banners and packed-field parameter table retain the enabled contract. Parent measured walk remains 89/873 cycles. |
| R909-2-R1 RESIDUE, Docs | RESOLVED | Leaf README now qualifies bind flush as combined with map invalidation and points to the untested bind-only term. |
| R909-1-R1/R2/R3 and R910-1-R1 RESIDUE, Docs | Prior corrections retained | Design attribution/off-tree pointers remain corrected; fresh-measurement sentence links PR #987; builder row 16g remains after 16e. |
| R909-1-S1 SUGGESTION, Docs | Addressed, retained | PR and builder documentation disclose split layout-3 NAME capacity instead of the absent all-fabric 128-record bound. |
| R909-2-S1 SUGGESTION, Tests | Adopted | Two connection plants now run at 1x1 as well as 8x8. |
| R909-2-S2 SUGGESTION, Docs/Tests | Addressed | Handoff explicitly states that canonical hashes require identical export inputs because those inputs name the CPU wrapper. |
| R909-2-S3 SUGGESTION, Tests; S4 SUGGESTION, RTL | Optional, unadopted | Parent release-clock execution remains unclaimed. Queue `:821` still performs an unused one-past map read at copy completion. Neither suggestion blocks coverage. |

No new source-comment lane/reviewer/round label was found in the added lines.

**Execution and physical evidence**

The independently rebuilt talker-7 plant is exactly `.stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h7f))`. With verified pinned version 5.050 it builds and exits 1, failing `WIRE_STREAM_DELIVERY` and `WIRE_STREAM_COMPLETE` for stream 7 in both `edits` and `clipped`. Stream 7 captures 3,088/1,160 words and delivers zero. The other seven streams deliver 64/24 packets each; the aggregate is still 616. See `talker7.json`, `talker7.log` and the complete path-normalized `talker7.full.log.gz`.

The published parent campaign has two controls and fifteen plants. Controls pass 16,173/122,549 checks. Each 8x8 talker 0-7 and the 1x1 talker is suppressed separately; each log contains all four required delivery/completeness failures. Four connection and two retention plants build and fail `PARENT_SAMPLE`. `audit_receipts.py` checks runtime text, not just `passed` flags.

Cold measurements are 23.811083137/67.651153567 seconds, scaled by 1.58 and rounded upward to 38/107. Second measurements at `128909ef` are 22.097158127/59.625621893 seconds. Later changes add no workload. Hosted measurement windows remain owed. The maximum predicted worker is 1,615 seconds against 1,620; new-suite workers predict 1,508/1,507. These are below 30 minutes. The actual `.github/workflows/rtl.yml:144` timeout is 45 minutes for ordinary workers, 60 for worker 18, rather than 30; the 1,620-second prediction ceiling is stricter. Author local shards took 2,112.9/2,022.2 seconds, not hosted measurements.

Driver shard 15 passes 8/8 suites with 662,439 checks; shard 16 passes 9/9 with 356,128, both with complete accounting. The leaf now emits the tally's recognized `N checks, M failures` while preserving its verdict. All seven repaired gate causes were inspected: Python annotations/wrapping; C/C++ declarations/parser syntax; source-reader dispositions/process deadlines; traceability; Contents; documentation inventory; sweep tally. The published 43-step docs replay has zero failures; its stated skips are not executed jobs. Source-bank receipts report builder union 114 entries, portability 63 tops, queue 28/28, coherence 42/42 and render campaign union 32/32. These remain author source evidence.

Enabled 8x8 uses `endstation_ax7101_8x8`, input loopback on and legacy loopback off; `xc7a100t-fgg484-2`, commercial Slow/Fast at 0/85 C. Scripts use AreaOptimized_high synthesis, ExploreArea optimization and three placements from one post-opt checkpoint, then AggressiveExplore physical optimization/routing. No randomized seed sweep is claimed.

| Placement | Worst setup ns | Worst hold ns | LUT | FF | RAMB36/RAMB18 | #818 |
|---|---:|---:|---:|---:|---|---|
| ExtraPostPlacementOpt | +0.008 | +0.036 | 48,883 | 54,671 | 94/34 | Misses +0.030 setup floor |
| AltSpreadLogic_high, selected | +0.223 | +0.036 | 48,901 | 54,672 | 94/34 | PASS |
| ExtraTimingOpt | +0.003 | +0.036 | 48,960 | 54,671 | 94/34 | Misses +0.030 setup floor |

Selected slow corners are +0.223/+0.102 ns; fast corners +1.436/+0.036 ns, setup/hold. All twelve reports show zero setup/hold failing endpoints. Selected resources include 15,774 slices, 111 BRAM tiles and 11 DSPs. Published routing status records 96,133/96,133 nets routed and no routing errors. Enabled 1x1 retains the unchanged round-4 +0.124/+0.036 ns worst-corner result.

Placement sensitivity must remain recorded and already is in the PR body/handoff. The three worst setup paths are in the mailbox: pending event to counter-seen, receive header-read to register-read data, and pending event to asynchronous count. Report sections show 76-81% routing delay. Only one placement qualifies; #818 permits selecting that best-of-three result. The default placement itself is not qualified.

Enabled 8x8 control memory remains 70.5 tiles: +11.5 over the 59-tile ledger and +14.5 over default 56. The ordinary allocator still refuses it; measurement export does not relax the guard. The explicit #979 ruling makes this S14 debt. Enabled 1x1 remains 47.0 tiles. No owner ceiling or service limit changes.

Disabled canonical payloads reconstruct to `18af89e620ea88ee2a745550bd25b1645702cec071bcba36decced2b5376d9af` (1x1) and `fe344bba8709f7b8e72075b38aa81619c316c2207f948e0adaea1540e36da767` (8x8). Published base/head utilization remains 33,792 LUT / 42,649 FF / 80 tiles and 45,199 LUT / 53,086 FF / 99 tiles, respectively, with 11 DSPs each. Exact canonical hashes require identical export inputs. Raw generated text, debug sections and FPGA bitstream identity are not claimed.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #979 ruling; INPUT_MAPPED_LOOPBACK.md:369-445; per-stream parent completion; source-bound twelve-corner #818 audit; retained mapping contract | R910-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| RTL | CLEAN | packet-verification.json implementation/gitlink identity; queue/capture enabled branches and banners; canonical payloads; route scripts/reports and unchanged allocator refusal | R910-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Robustness | CLEAN | input_loopback_dp/sim_main.cpp:594-647 phase/reset ordering; nine held-output logs; both-shape connection plants; lead/window receipts; explicitly limited guard claims | R910-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Tests | CLEAN | suite_shards.py:111-112; planner-selftest.log; shard-listings.json; talker7 probe; 17 campaign logs; shards 15/16; seven gate repair causes | R910-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Docs | CLEAN | TESTING.md:354,441-445; suite READMEs; source-reader dispositions; generated inventories/Contents; PR sensitivity statement; 43-step replay | R910-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |

**Limits, reproduction and pending duties**

Independent execution was limited to planner self-test, 19 listings, one parent fault build/run, extracted-parser probe, receipt/hash audits and direct checkout verification. No full parent/processor/gPTP/portability/builder banks, physical implementation, hardware operation, workflow replica, source edit, commit, push or GitHub write occurred. Disposable files are exclusively below this packet's `scratch/`. Fetching the evidence commit succeeded; recursive fetches of unrelated evidence-branch submodule objects failed and were not used.

`checkout-integrity.json` directly verifies 1,958 superproject blobs and 214/868/115/100 blobs in the four required submodules against HEAD bytes/modes, matching indexes and gitlinks. Tracked status is empty. No product-file restoration was needed.

Reproduce with `check_packet.py <checkout> <packet>` and `audit_receipts.py <packet>` after extracting only `author-r4`, `author-r5` and the manifest from the pinned public evidence commit under `<packet>/scratch/review-evidence/loopbram-r1`; copy the manifest to `<packet>/scratch/public-manifest.json`. The fault probe is `probes.py <checkout> <packet> --verilator <pinned-5.050-executable>`; it uses at most 16 build jobs and expects runtime failure. `probe_env.py` and `verify_checkout.py` take `<checkout> <packet>`. Planner commands are `python3 scripts/suite_shards.py --selftest` and `scripts/run_all_suites.sh --ci-pieces --shard i/19 --list`, i=0..18.

Physical calibration remains NOT RUN; field skips and desk gates are not hardware proof. Five isolated guards, release-clock parent execution and canonical-name reproducibility retain their stated limits. No exact-head hosted job was independently inspected here; skipped contexts are not counted as execution.

The manager owns hosted/workflow-replica acceptance, reconciliation of complete local-gate requirements, the other independent positive review, confirmation that no review remains in flight, and current-dev candidate validation with builder/native bank receipts. Reviewed source base is `3cda030c17`; supplied live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`. Build the final candidate from the live base at merge time: these source receipts do not prove it. Explicit merge authorization, post-merge containment, debt/documentation retention and issue/project completion remain separate duties.

R910-3 FINISHED
