[R549] NEGATIVE - exact head 48f12dc14099a3630a98eb07e9ec790695a72bfb

Round R549-2, external independent review of issue #686 / PR #695.
Tree: `7ed2f048f73734f671ae6eb5e1a008544fa0d0d0`.

All five lenses have been applied independently. No new source defect was found in the assigned delta. One new MINOR evidence defect remains: four published orchestration scripts do not match the archive's SHA-256 manifest. Record regeneration nevertheless succeeds. The broader source-validation receipt portion of prior MAJOR R549-1-F4 also remains open. The independent verdict and ledger were written before consulting previous review findings; that consultation added the retained portion and updated the ledger below.

Public contract: [issue #686](https://github.com/kebag-logic/milan-fpga/issues/686), [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6047563934), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6050832603), [review start](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6050863946).

**R549-2-F1 | MINOR | Tests, Docs | published receipt manifest fails its advertised integrity check**

Artifact: archive `84add8ed571d376f8a1b39c3c6f71c4e80eed32a`, `review-evidence/686-r1/author-r2/resource-receipts/MANIFEST.sha256:70` (also lines 71, 156, 158).

- Authority/evidence: assignment 6047563934 requires reproducible public receipts. The receipt README advertises `sha256sum -c MANIFEST.sha256`. Of 186 listed files, four hashes disagree with the published bytes: `recipe/orchestration/ooc.sh` and `route.sh` in each of `r1-c7b69cd0` and `r2-48f12dc1`. The outer `review-evidence/686-r1/MANIFEST.json` records original/published hashes and path redactions, explaining all four discrepancies. See `receipts/archive-manifest-audit.log` and `receipts/resources.log`.
- Impact: the advertised archive-integrity verification fails. This does not invalidate the independently reproduced figures or imply altered RTL. The documented command cannot verify the published packet cleanly.
- Required outcome: regenerate these four checksum entries against the already redacted public bytes, preserve the provenance mapping, publish the corrected archive, and name its exact commit. Do not restore private paths.
- Verification: all listed files match their checksums, no receipt is unlisted, and regeneration of all three current records still returns equality. This changes a machine-checked generated artifact, so it is MINOR, not prose-only RESIDUE.

**R549-1-F4 (retained in part) | MAJOR | Conformance, RTL, Tests, Docs | broader source-validation receipts remain unavailable in the supplied public state**

Artifact: [archive 84add8ed, review-evidence/686-r1](https://github.com/kebag-logic/milan-fpga/tree/84add8ed571d376f8a1b39c3c6f71c4e80eed32a/review-evidence/686-r1); issue #686 and PR #695 public comments inventoried in `receipts/public-inventory.json`.

- Authority/evidence: [R549-1-F4](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6047415775) explicitly requested publication of the stated manager source-validation receipts as well as resource receipts. The resource portion is now reproduced and resolved. The supplied archive contains author summary documents, reviewer packets and resource-recipe receipts. The current issue has six comments (through 6050832603); the PR has six comments (through 6050863946), no submitted reviews and no inline comments. These contain summaries and starts, but no public location for the manager's full source static/builder/native bank receipts. The assignment reports those banks passed; this review does not dispute that statement.
- Impact: a cold reviewer still cannot inspect the reported broader exact-head execution evidence. Neither the focused reruns here nor the successful resource reconstruction prove those separate runs. No failed source bank is alleged.
- Required outcome: publish or link the exact-source manager bank logs/statuses and commit/tree association, or supply their already-public location. This is an evidence-publication duty; no extra source change or reviewer full-bank run is requested.
- Verification: inspect the linked commands, statuses and scope at this exact head, distinguishing source validation, current-dev candidate validation and skipped physical checks. The remaining portion retains the prior severity and all its lens labels; it is not cleared by the repaired resource portion.

Independent evidence:

- Reconstructed scope from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #686 and scope decisions 6029233665, 6043036997, 6047563934, then REQUIREMENTS.md section 1, FR-MAAP-01, the resource recipe and area budget. Read IEEE 1722-2016 Annex B directly: B.2.1, B.2.3, B.2.5-B.2.8, Table B.7 and notes, Table B.8, B.3.4, B.3.6.4-B.3.6.7. The four correction items are bounded scope; documented remaining deviations are not claimed resolved.
- Inspected the requested `e21c1ca0..48f12dc1` history and diff, then isolated `c7b69cd0..30fce4b0a` and `291710b1..48f12dc1` to distinguish review changes from imported dev work. `scripts/verify_merge.py` recreated the automatic merge and applied exactly four resource-file resolutions from dev. Its tree equals `e519e31f`'s tree. The final commit changes only those four resource-record artifacts.
- `scripts/run_focused.py REPO PACKET SIMULATOR --jobs 4`: clean harness 130 checks, zero failures; all 26 planted defects build successfully and exit 1 at their specified check. Maximum four simultaneous cases, four compiler workers each. `receipts/focused/` preserves build/run statuses and output.
- Harness [11] uses `02:00:00:00:AC:E1`, excludes at-once-to-timer intervals, and observes six distinct timer-to-timer probe intervals and three distinct announce intervals. Both zero-state mutations fail the required randomness checks. Harness [6a] stalls after two ANNOUNCE beats, injects a conflicting PROBE, checks all 60 completed bytes, checks no DEFEND and unchanged range; removing `!tx_busy_r` is killed by its named byte-integrity check. The own-empty-range mutation is killed. Supporting-change mutations carry item 0 and do not satisfy the four-item guard.
- `scripts/run_seed_probe.py REPO PACKET SIMULATOR`: 131,072 compiled reset/first-send cases cover all 65,536 folded MAC classes with both supplied-seed modes, every supplied offset and all count values. Reset never yields zero. The compiled LFSR visits all 65,535 nonzero states once and returns to `0xACE1`. The zero-seed mutation fails at fold `0xACE1`. The two MAC low words determine the seed; remaining bits and the provisioning offset cannot introduce zero. Both draw formulae stay strictly bounded throughout the state cycle. See `receipts/seed-probe.log`.
- `scripts/verify_resources.py REPO PACKET RECEIPT_ROOT`: using the audited public regeneration helper and exact-head `pp_resource_gate.py` parsers, all three current and all three round-1 records reproduce, including every identity field, rehashed input, figure and scope. All endpoint policies are unchanged from baseline F, flow identity includes `set_param synth.maxThreads 1`, and all three current records pass F's policy. Overall script exit 1 retains F1 even though all six individual regeneration commands exit 0.
- The standard PDF SHA-256 is `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c`. The scoped simulator reported version 5.050 before execution. `receipts/identity.txt` records these identities without local home paths.

| Current endpoint | LUT | FF | Other decisive evidence |
|---|---:|---:|---|
| route-1x1 | 50,391 | 54,263 | 15,788 slices, 87.5 BRAM tiles, WNS +0.241 ns, WHS +0.029 ns; route complete |
| ooc-1x1 | 23,179 | 19,779 | Every recorded figure equals baseline F; standalone timing is not a routed timing claim |
| ooc-8x8 | 30,135 | 27,380 | Every recorded figure equals baseline F; standalone timing is not a routed timing claim |

The route delta against F is +434 LUT, -11 FF and +54 slices, within +500/+600/+80. RAM/DSP deltas are zero; WNS/WHS meet +0.030/0 ns floors. Route status reports 100,934/100,934 routable nets complete, zero routing errors. These are receipt-based checks of the published `e519e31f` measurement, not a fresh physical implementation run. Published isolated MAAP area is 515 LUT / 278 FF against 637 / 268 (-122 / +10, within +40 / +40); that isolated synthesis was not rerun here. The routed hierarchy independently contains 429 LUT / 279 FF for `g_maap.maap_engine`.

Prior public findings were read only after the independent verdict and five-lens ledger were saved. The public findings are [R549-1](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6047415775) and [R548-1](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6047555468).

| Prior ID | Disposition at this head | Evidence |
|---|---|---|
| R549-1-F1 = R548-1-F3, including former R548 R1 | RESOLVED, all five lenses; manager's MAJOR severity ruling respected | `KL_maap.sv:141,292`; exhaustive reset/state probe; [11] and both killed zero-seed mutations; corrected `MAAP_FABRIC.md:85` |
| R548-1-F1 | RESOLVED, Tests and Robustness | [6a] at `sim_main.cpp:419`; `defend_rewrites_the_frame_on_the_wire` builds, fails the named byte check; clean control passes |
| R548-1-F2 | RESOLVED, Docs and Conformance | `MAAP_FABRIC.md:135` now distinguishes repeated PROBEs one to three from the fourth's immediate ANNOUNCE and compare_MAC consequence, matching Table B.7 |
| R549-1-F2 = R548-1-F4, including former R548 R2 | RESOLVED, Docs | `KL_maap.sv:222`, `MAAP_FABRIC.md:65`, current PR body explicitly keep requested_count and station MAC live; no all-fields snapshot promise |
| R549-1-F3 = R548-1-F5 | RESOLVED, Docs and Conformance | `MAAP_FABRIC.md:52,142`, module page and banner distinguish clipped random blocks from unvalidated supplied offsets; validation is listed for follow-up |
| R549-1-F4, retained by R548-1 | PARTIALLY RESOLVED; broader-bank receipt portion RETAINED above | All six resource records reproduce exactly, fixing the missing recipe/input/report portion. New F1 covers four stale public checksums. Broader manager source-bank receipts remain unlocated |
| R548-1-S1 | RESOLVED | Own-empty-range test and its killed supporting mutant |
| R548-1-S2 | RETAINED as optional SUGGESTION, Tests and Robustness | No new truncated-PDU gate test; current PR follow-up list explicitly records it. This is inherited and outside #686; it banks no new malformed-input proof |
| R548-1-S3 | RESOLVED | Supporting mutants use item 0; required-item guard excludes it |
| R548-1-S4 | RESOLVED for the two cited comments | `milan_datapath.sv:267,282` names 515/278 and the four-PROBE walk |

No new RESIDUE item is reported.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (retained F4 evidence portion) | `hdl/ieee1722/maap/KL_maap.sv:114,170,196,240,363`; Annex B and issue scope; `receipts/focused/clean.run.log`, `receipts/seed-probe.log`; public inventory | R549-2; source checks clean, F4 open | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| RTL | UNCLEAN (retained F4 evidence portion) | `hdl/ieee1722/maap/KL_maap.sv:141,202,222,292,355`; reset/transition enumeration; `receipts/merge.log`; resource regeneration; public inventory | R549-2; source checks clean, F4 open | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Robustness | CLEAN | `tb/verilator/maap/sim_main.cpp:333,419,445,480,557,586`; stalls, subsequent PDU, restart, empty/adjacent/disjoint ranges, disable/reset, every folded seed; killed mutations | R549-2 | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Tests | UNCLEAN | `tb/verilator/maap/sim_main.cpp:419,586`, `tb/verilator/maap/mutants.py:54,91`, differential and crflic changes; `receipts/focused/summary.json`; manifest F1 and public inventory | R549-2; F1 and retained F4 open | 48f12dc14099a3630a98eb07e9ec790695a72bfb |
| Docs | UNCLEAN | `docs/design/MAAP_FABRIC.md:52,65,85,135,142`, module page, `docs/reference/FR_NFR.md:167`, AREA_BUDGET, PR body; receipt README/manifest F1 and public inventory | R549-2; F1 and retained F4 open | 48f12dc14099a3630a98eb07e9ec790695a72bfb |

The source documentation now identifies live requested_count/source MAC, unvalidated supplied offsets, nonzero reset seeding, and the missed fourth PROBE's ANNOUNCE/compare_MAC consequence. No approval of broader Annex B completeness is implied.

Limits and manager duties:

- Full parent, processor, builder and synthesis banks were not rerun; the manager owns their exact-source evidence and hosted/local-replica acceptance. The read-only snapshot in `receipts/hosted-checks.json` contains completed successes, running jobs, and a skipped physical job; it is not a complete hosted acceptance verdict.
- Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. The measured merge imports dev `291710b1`. Live dev identified by the assignment: `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. This review does not validate that final candidate. The manager must construct and validate the current-dev candidate and satisfy the resource re-baseline rule for its changed shipping export.
- Physical calibration NOT RUN. Field skips and simulation provide no hardware proof. The manager retains post-merge reference-peer MAAP interop, explicit merge authorization, independent review completion, exact-candidate gates, containment, follow-up issues and final Issue/Project completion.
- Remaining scoped exclusions: compare_MAC in two other cells, DEFEND requested-range echo, B.3.6.1 address generator/seed, PortOperational!, undefended mid-frame PROBE, tagged input, supplied-seed validation and truncated-input coverage. These are not presented as newly fixed or generally compliant.
- Timer draws and the exercised sends satisfy the strict bounds. This does not prove wire deadlines under unbounded downstream backpressure, full malformed-frame handling, or arbitrary configuration changes during a frame. Line coverage and the broader differential were not rerun in this delta review.
- No source fixes, commits, pushes, GitHub writes, hardware operations or other-checkout edits were performed. Scratch builds/probes are under this packet's `scratch/` and excluded from publication. Tracked blob bytes, executable modes, complete index and all three required initialized gitlinks match the exact head (`receipts/tree-integrity.log`).

R549-2 FINISHED
