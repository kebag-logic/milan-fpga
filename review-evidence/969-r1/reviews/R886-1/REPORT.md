[R886] NEGATIVE - exact head f863258d2a455697d85a5ab48813be8f0783e2d4

Round R886-1, external independent review of issue #969 / PR #971. All five lenses were applied. One MAJOR and two MINOR findings remain open. No clean completion ledger is granted.

Examined tree: `b3eb9ddc12c32518963a7f61f1774929894f01be`. Scope is the delta from `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`, the reviewed flip head, to the exact head above; it is not the PR's recorded base diff. The clone and five required submodules retain their exact tracked bytes, modes, indexes and gitlinks (`tree-integrity.json`). No source changes or GitHub writes were made.

Authority and independence

I read AGENTS.md / CONTRIBUTING.md, docs/README.md, the [issue and public scope decisions](https://github.com/kebag-logic/milan-fpga/issues/969), linked requirements and interfaces, then the source delta and history, before examining executable evidence. Authorities include REQUIREMENTS.md, the SRP integration contract, lwSRP's filter/allocation and callback contracts, Milan v1.2 5.3.8.5, 5.5.3.5.18 step 4 and Tables 5.9/5.10 as cited in the public task, the latest-kind decision in #925, the walk schedule in #930, the memory exceptions under #665, and #818's timing floor. I checked those clause interpretations against the public decisions and implementation; I did not independently obtain and reread the complete licensed standards.

Source evidence is the author's [immutable packet](https://github.com/kebag-logic/milan-fpga/tree/4ce6f35f305451ce9ac383e65348f2ea38c872e2/review-evidence/969-r1/author-r1) and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7080057766), together with public coordination comments. All 58 files in that packet were downloaded and checked against its published SHA-256 manifest. `evidence-download-verification.txt`, `evidence-manifest.json` and `published-gate-extracts.txt` record the audit.

After my independent source pass I fetched the PR's public comments. The snapshot contained the two review-start comments, including [this review's start](https://github.com/kebag-logic/milan-fpga/pull/971#issuecomment-7080105856), and no prior public findings requiring resolution. No other reviewer's report or private author material was read.

Findings

**R886-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs**

Artifact: `sw/firmware/ctrl/srp/srp_mbx.c:944` (`count_kept`), `:460` (`keep_talker`), `:1266` (`reset_interface`); reviewer `probes.cpp` and `probe-{1x1,8x8}-head.log`.

Authority/evidence: #969 promises retention up to `SRP_KEPT_TALKERS`, so a declaration preceding its binding can produce the Listener after the successful probe. `count_kept` refreshes after returned blocks only when the cached count is already at the bound. A stale count below the bound therefore survives reclamation. Reset destroys the participant but also leaves that count untouched. A receive refresh happens once before the entire PDU; reaching the bound partway through a vector does not trigger another refresh.

The independent probe first keeps one unrelated Talker, then either resets the interface or leaves and reclaims that Talker. It offers a single legal vector containing exactly `CTRL_SRP_SINKS` new Advertise attributes, then binds every input. At 1x1/1if, input 1 fails; at 8x8/1if, input 8 fails. Its desired, declared and feedback kinds remain zero, and its Listener is absent from the next transmitted MRPDU. Both reset and reclaim variants fail at both shapes. The same full vector in a fresh registrar passes. Each head probe run reports five tests, three passes, two failures.

Impact: a now-empty registrar admits only N-1 of N in-bound Talkers. The last declaration is silently filtered before allocation; when the binding settles, there is no registration to replay. The original quiet-applicant failure can recur until another declaration arrives. This is not the documented past-the-bound allowance. The adjacent comment's assertion that an overestimate below the bound is all admission needs is false for a multi-attribute receive.

Required outcome: refresh/invalidate admission accounting sufficiently after reset and reclamation that a legal in-bound vector is not rejected because of obsolete occupancy. Preserve the fixed storage bound, bound-stream priority, callback non-reentrancy and unbound walk policy. Correct the explanatory invariant and add regression coverage for partial occupancy followed by reset/reclaim and a full vector.

Verification: both failing probes must pass at 1x1/1if and 8x8/1if on every input, alongside the fresh-vector, flood and UNBIND/BIND controls. A regression plant must expose this stale-count path. Recheck retained-kind, pool and walk behavior and the relevant cost evidence after the fix.

**R886-1-F2 - MINOR - Tests, Docs**

Artifact: `sw/firmware/ctrl/test/test_ctrl_firmware.py:232`, `sw/firmware/ctrl/test/srp_early_mutants.py`; PR #971's planted-defect description and issue #969 REVIEW READY; published `receipts/firmware-gate-4c5018eb-shard3.log.gz`.

Authority/evidence: the published claim says the eleven early-Talker plants run at both interface counts and at 8x8/1if. The 8x8 campaign selects only the Listener and reclaim prefixes. It excludes `feedback-early-*`; those plants have no per-defect 8x8 entity override. The published shard contains 22 early-plant results, two per plant, from the two 1x1 campaigns, not 33 across the claimed three points.

Impact: the documented reproducible gate does not provide its claimed 8x8 mutation coverage. A future regression can lose that shape's coverage while all four shards remain green. My separate focused run caught all eleven plants at 8x8/1if, but does not repair the repository's gate selection or its historical receipt.

Required outcome: include the early-Talker plants in the 8x8/1if campaign and publish the resulting receipt; correct the existing evidence claim to distinguish the old gate from the added run. If the intended gate scope is changed instead, obtain the public scope decision and state that scope accurately.

Verification: campaign selection must visibly include all eleven at 1x1/1if, 1x1/2if and 8x8/1if, with each plant refused by its intended assertion. The updated shard should show 33 early-plant results with unambiguous shape attribution.

**R886-1-F3 - MINOR - Docs**

Artifact: `sw/litex/ctrl_memory_ledger.py:10`; `docs/design/SPLIT_CONTROL_MEMORY.md:189` and `:190`, compared with `sw/litex/ctrl_memory_ledger.py:60` and `:163`-`:169`.

Authority/evidence: the executable ledger now holds the two-interface platform at 63.5 RAMB36. Its introductory description still calls that point 63.0. The authoritative document describes the platform widening plant as 63.5 and the fixture's cross-entry plant as 63.0; the executable plants now use 64.0 and 63.5 respectively. The reviewed change updates these ledger values without making these descriptions agree.

Impact: a reader cannot reconstruct the current accepted point and planted boundary from the authoritative prose. These are numeric measurement/test claims, not purely stylistic residue. The executable ledger and its tests themselves pass.

Required outcome: change the current platform value in the introduction to 63.5; describe the platform widening plant as 64.0 and the fixture's platform-value plant as 63.5. Preserve correctly labelled historical values.

Verification: compare those descriptions with `OWN` and `edits` in `ctrl_memory_ledger.py`, then rerun documentation checks. This finding does not request changing executable limits.

Independent results and source evidence

| Check | Result and practical scope |
| --- | --- |
| Failing first at the reviewed base | `run_focused.py` uses current tests with the exact base `srp_mbx.c/.h` in disposable copies; it does not claim a complete historical build. At each required shape, the selected adapter suite reports 7 failures/21 tests and the platform suite 2 failures/14 tests. Saved-binding restore and BIND while bound fail; binding-first controls pass. |
| Head adapter and platform suites | At each of 1x1/1if and 8x8/1if: adapter 95/95, platform 14/14, Listener differential 8/8. Platform tests exercise every input, both Talker kinds, saved state, successful ACMP probe and GET_STREAM_INFO REGISTERING/REGISTERING_FAILED. |
| UNBIND/BIND control | The independent every-input adapter control passes on both base and head at both shapes. This is an adapter control, not an independent hardware ACMP run. |
| Additional boundary probes | Fresh full vector passes; below-bound reset and reclaim fail as F1; 1,000 unbound offers at the admitted receive rate preserve the storage bound and cause no snapshot walks or pool refusals, then every bound input declares. |
| Eleven early-Talker plants | All caught at 1x1/1if, 1x1/2if and 8x8/1if in my focused campaigns. `plant-logs/` contains the 33 individual receipts. F2 concerns the repository's published gate selection. |
| Light gates rerun at this head | Both flip graders, load and shape-cost graders, memory tests, documentation check and added-line punctuation check return zero. These are graders and focused tests, not new CPU timing measurements or full build banks. |
| Author's four firmware shards | Published at 4c5018eb: 88 suite arms, 827 control plants, 385 AECP plants and 565 SRP plants, all reported successful. Examined the later delta and final-head identity receipt: platform loadable bytes at 1x1/1if and 8x8/1if equal 4c5018eb. F2 limits the plant-coverage claim. |
| Coverage | Published final-head check passes for 40 files. SRP reports 854/854 lines and 773/776 raw branches; three documented exclusions yield the reported 100% effective branch figure. Coverage does not detect F1's missing vector scenario. |
| Memory | Published platform points: 45.5, 46, 58.5 and 63.5 RAMB36, respectively 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. The two 8x8 product points use their own exceptions. The separate 8x8/1if size-fixture build in the receipt succeeds under its unoverridden 56-RAMB36 budget; this is not the 58.5 product image. My memory test rerun passes, including refusal plants. |
| Twin and plants | Examined the published twin, twin-plants and map-leg receipt: normal checks pass and intended defects are caught. No independent full twin bank is claimed. |
| CPU and hot list | Published five-group comparison at 954e5572 covers SRP, ACMP command, fixture, backlog and backlog-owed at both shapes: zero passing cases over share and the same seven owed backlog misses as base. It is not a complete final-head measurement bank. The final-head hot-list receipt reports no hot function moved or resized. My graders pass: 1x1 last 127.31/130 ms, ACMP 29.06/30 ms, txL 47.88/49 ms; 8x8 transmit 76.81/77 ms, load 0.744/0.75. |

Cause and architectural checks

The original cause is supported by execution and code: the base `interested_msrp` rejects an unbound StreamID before `third_party/lwSRP/src/core/mrp_mad.c:998` reaches allocation. A quiet Talker consequently has nothing registered when the binding later settles. This agrees with the public Table 10-3 explanation; the control that unbinds and rebinds an already registered stream works.

The intended fix uses the existing medium-block pool, sets `SRP_KEPT_TALKERS = CTRL_SRP_SINKS`, and statically checks that kept plus domain blocks fit the fixed allowance (`srp_mbx.h:136`, `srp_mbx.c:29`). The filter admits bound streams independently of the kept bound; unbound excess is intentionally filtered. Counting occurs outside callbacks. I checked `srp_held` selection and latest-kind/fallback behavior against #925, the declaration/feedback path into ACMP, and the unchanged Listener schedule against #930. Existing positive, boundary, latest-kind, ended-registration and past-bound tests pass, subject to F1. No RTL, CDC, mailbox contract or required dependency pin changes occur in this delta; the RTL lens also covers the changed firmware architecture and resource/accounting invariants, where F1 applies.

New source comments were checked for the owner's behavior/reason and public-reference rule. No new prohibited bench-lane/reviewer/comment identifier was found. Test-case identifiers were evaluated as test identifiers, not assumed to be bench labels. No RESIDUE finding is used to downgrade a numeric or behavioral claim.

Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN - F1 | Issue #969 acceptance; #925 decision; `srp_mbx.c` filter, held-kind and binding paths; `test_plat_sinks.cpp` early cases; independent vector probes | R886-1 applied; no clean coverage | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| RTL | UNCLEAN - F1 | Full scoped diff; `srp_mbx.c:29,460,944,1266`; `srp_mbx.h` pool/layout bounds; unchanged interface and dependency contracts | R886-1 applied; no clean coverage | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Robustness | UNCLEAN - F1 | `probes.cpp`; reset/reclaim/flood logs; existing malformed, leave, latest-kind, bound and ordering tests in `srp_mbx.cpp`; Listener differential | R886-1 applied; no clean coverage | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Tests | UNCLEAN - F1, F2 | Failing-first receipts; `test_ctrl_firmware.py:232`; early/control plants; 33 independent plant receipts; four published shards and coverage | R886-1 applied; no clean coverage | f863258d2a455697d85a5ab48813be8f0783e2d4 |
| Docs | UNCLEAN - F1, F2, F3 | `srp_mbx.c:944` rationale; SRP/platform READMEs; SPLIT_CONTROL_MEMORY; ledger docstring; public acceptance/evidence claims; docs checks | R886-1 applied; no clean coverage | f863258d2a455697d85a5ab48813be8f0783e2d4 |

Limits and pending manager duties

The two published routes meet #818's WNS >= +0.030 ns and WHS >= 0 at every listed corner: worst +0.437/+0.017 ns at 1x1/1if and +0.058/+0.036 ns at 8x8/1if, zero route errors. They routed **f6f83166**, before the 24-byte removal in b56664fe. Their bank dimensions match the final images, but their ROM bytes do not. I do not promote those receipts into exact-f863 timing proof. The record explicitly identifies that provenance; current-candidate timing/acceptance remains for the manager. The other two placement directives were not run. No new route was run in this review.

`hosted-snapshot.json` records an observation, not an overall accepted CI verdict. It includes executed successful wire-accountability, docs-check-no-git and lint jobs, with other jobs still queued/running. Physical calibration was skipped/NOT RUN; field skips are not hardware proof. Hosted and local-replica acceptance belong to the manager. There is no manager source-bank execution at this head, and none is inferred from coordination comments.

After findings are fixed, the corrected head needs independent re-review and refreshed affected evidence. The manager must validate the actual then-current dev merge candidate, run the required builder/native banks and publish receipts, finish hosted/local acceptance and candidate containment, and perform the bench rerun after an authorized merge. The supplied live-dev reference was `e275d7950ef3385753e6a15d2e191ba855b171ed`; it is not a claim that a candidate against that tip was built here. This report neither authorizes merge nor claims completion of issue #969.

Reproduction and packet

The packet scripts accept `CHECKOUT PACKET` and put disposable builds under `PACKET/scratch/`. Run `run_focused.py`, then `run_probes.py`; `run_plants.py` runs the three focused mutation campaigns. Run these drivers sequentially relative to each other; each driver joins its own concurrent work before exiting. Compiler concurrency within a driver is at most sixteen. `run_small_gates.py` takes explicit `--litex-python` and `--markdown-python` interpreters; raw command receipts identify the checks. `verify_tree.py CHECKOUT` hashes tracked blobs, verifies executable/symlink modes and index records, and checks required submodules.

Nonzero base-suite receipts are the intended failing-first result. Nonzero head probe receipts are the open defect, not a harness error. Receipt bodies preserve test output and exit status; local path prefixes are replaced by public-safe placeholders, with unredacted originals retained only in unpublished scratch. `MANIFEST.sha256` lists all publishable files with relative paths. Scratch trees and unlisted discovery snapshots are not publication artifacts.

R886-1 FINISHED
