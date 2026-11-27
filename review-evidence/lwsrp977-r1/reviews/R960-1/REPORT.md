[R960] NEGATIVE - exact head 73007b4807977517045e8aa485c61ebb8f5ee843

Full review of [lwSRP PR #22](https://github.com/kebag-logic/lwSRP/pull/22): all 20 commits against base d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b.
Verified tree: eeb3e733b50398a056f5b52325168959c280f45f.

Five MINOR findings remain open. Tests and Docs are UNCLEAN. One additional wording finding is RESIDUE and does not affect the verdict.
No production protocol counterexample was found in the reviewed paths or executed checks. Passing those checks does not satisfy the missing coverage and evidence requirements below.

## Scope and authorities

Read the supplied AGENTS instructions, CONTRIBUTING.md, README.md, all five doc/ guides, and doc/tools/README.md.
The clone contains no repository AGENTS.md or docs/README. The parent [documentation index](https://github.com/kebag-logic/milan-fpga/blob/94f4d3475ae1d7c45655ea73e6dfa4442ac5e4eb/docs/README.md) establishes requirements and interfaces before implementation and executable evidence.
Its linked requirements, FR_NFR register, mailbox contract, memory document and submodule boundaries were consulted. Older parent text was not allowed to override later public issue rulings.

The frozen acceptance is [issue #977](https://github.com/kebag-logic/milan-fpga/issues/977): profile registration, preserve a separate registration cost term, fit records within their slices, and retain the owner bounds.
The [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7091882145) selects the MRP transmit-opportunity rate, includes work-pass and transmit-build bounds, and permits the documented one-port reservation-refusal difference.
The [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7160202807) raises only the 8x8/1if load ceiling to 0.76; 1x1/1if remains 0.70.
The [timing ruling](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7180135694) and [LINK_UP decision](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7210516620) govern parent integration, not permission to change MRP semantics here.

Protocol authorities: IEEE 802.1Q-2018 clause 10, including Tables 10-3/10-4, 10.7 timers and 10.8 encoding; clause 35.2; Milan v1.2 4.2.7.
For the requested zero-count boundary, the [IEEE clarification](https://www.802-1.org/items/163) retains a correctly sized FirstValue while omitting packed events when NumberOfValues is zero.
The public identity, callback, serialization, timer and retry contracts were read in src/include/shish_lan/mrp.h, src/ports/timer.h and the integrator guide.

The full diff and history were independently examined before the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/94f4d3475ae1d7c45655ea73e6dfa4442ac5e4eb/review-evidence/lwsrp977-r1/author).
All 18 downloaded files match the publication manifest: receipts/public-hashes.json.
INDEPENDENT-VERDICT.md records the independent verdict and ledger before earlier public findings were fetched.

## Findings

### R960-1-F1 — MINOR — Tests

**Artifacts:** src/core/mrp_mad.c:1777; tests/differential/mad_trace.c:183, :380, :413; tests/check_differential.py:198.

The empty-type-word shortcut lacks a killing test for reaching a later occupied word. The supplied applications and differential test application use only the first type word.
Replacing type |= 31u with type = 255u incorrectly ends the scan at the first empty remainder. It compiles and produces identical complete traces for all 200 seeds, 3,000 steps each, in both profiles with every end-station switch enabled.
An independent probe declaring types {1,64,129,224,255} passes on head and base, but fails five assertions with this fault in each profile.

**Authority/evidence:** acceptance requires a killing test for every new path. type_word_control.py, boundary_probe.c, receipts/type-word-control.json and its raw logs reproduce the survivor and independent detection.

**Impact:** a regression dropping later Messages can pass the published gate. This is a demonstrated coverage defect, not a claim that this head drops those Messages.

**Required outcome:** retain a sparse multiword test and a mutation that skips later occupied words. Cover word boundaries, empty intervening words and type 255 with LWSRP_LEAN_TX alone and in the combined build.

**Verification:** original builds pass; the demonstrated fault compiles and fails a behavioral assertion in both profiles.

### R960-1-F2 — MINOR — Tests, Docs

**Artifacts:** tests/check_reversals.py:405–410 and :457; doc/tester.md:212; PR #22 Evidence/Reversals row; published lwsrp-rev-*.txt receipts.

The reversal runner selects 110 cases with scale OFF and four with scale ON, but always prints the entire 114-case table length. The PR consequently says “114 reversals each,” including the four-case runs.
The tester guide also partitions 36 differential defects into ten timer, five bucket, eleven ordering and twelve end-station defects. There are ten end-station defects, not twelve; its next sentence enumerates 2 + 1 + 4 + 3.

**Authority/evidence:** executed evidence must distinguish selected and skipped work. receipts/reversal-counts.json records 114 listed, 110 selected OFF and four selected ON. Public key-run logs contain four KILLED lines. Both independent differential campaigns kill the actual 36 cases.

**Impact:** individual execution counts are overstated and the mutation inventory is contradictory. These are measurement claims, not wording-only residue.

**Required outcome:** report selected/executed/killed/skipped counts separately; correct the PR and summaries to 110 ordinary plus four key cases per profile; change “twelve” to “ten.” Keep the separate sanitizer control separate from the 36.

**Verification:** both selections and profiles reconcile with individual result lines; differential category totals add to 36.

### R960-1-F3 — MINOR — Docs

**Artifacts:** PR #22 Why and Review notes (“the default objects are main's”); src/core/mrp_mad.c:1205.

The unqualified default-object identity claim fails for an unoptimized build. With all new switches unset, the ten source translation units give 29 matching object comparisons out of 30 across -O0, -O2 and -Os.
Only src/core/mrp_mad.c at -O0 differs. The default arm introduces the local kept variable for the snapshot copies. This affects the documented Debug configuration, which supplies no optimization setting.

**Authority/evidence:** the PR makes a literal binary claim. run_probes.py and receipts/default-objects.json provide per-object hashes. Debug information and differing source-path strings are unnecessary to reproduce the difference.

**Impact:** equal protocol traces and optimized objects do not establish the broader binary claim. No protocol mismatch was observed.

**Required outcome:** preserve default object identity for the promised builds, or accurately limit the binary claim to verified build conditions while keeping behavioral equivalence distinct.

**Verification:** compare base/head bytes under identical flags, including the unoptimized configuration, and publish the conditions of any retained binary claim.

### R960-1-F4 — MINOR — Docs

**Artifact:** exact-head release-note inventory; no CHANGELOG exists in the lwSRP tree. The public parent PR #993 head's CHANGELOG also does not inventory this option set.

The integrator guide documents the switches, but the requested CHANGELOG coverage is absent.

**Authority/evidence:** review acceptance explicitly requires guides and CHANGELOG to state each option. receipts/scope.json records the empty inventory; [parent release notes inspected](https://github.com/kebag-logic/milan-fpga/blob/095995243bc354b8a41755f3fdfae343511cc668/CHANGELOG.md).

**Impact:** release readers lack the required record of opt-in behavior, configuration consistency requirements and the one-port exception.

**Required outcome:** add an entry naming LWSRP_ATTR_KEY, LWSRP_ATTR_BUCKETS, LWSRP_TIMER_SLOTS, LWSRP_TX_MERGE, LWSRP_ONE_PORT_MAP, LWSRP_LEAN_VALIDATE, LWSRP_RAPID_REPLACE, LWSRP_LEAN_COPY and LWSRP_LEAN_TX. State defaults, SCALE selection, direct end-station definitions and the policy/allocation exception.

**Verification:** reconcile every switch with the guide and compile definitions; identify the release/change and governing issue.

### R960-1-F5 — MINOR — Docs

**Artifact:** tests/__pycache__/check_reversals.cpython-314.pyc; 35,464 bytes; added blob f431fd265a869740bf141cbe2453fb4e9e51d36b.

The delta tracks an interpreter-generated cache instead of reviewable source.

**Authority/evidence:** CONTRIBUTING.md:44 excludes generated assets. receipts/scope.json and receipts/integrity.json record the file and exact blob.

**Impact:** the published tree contains a redundant, version-specific generated test artifact. No private absolute-path marker was found in the bytes; no runtime failure is attributed to this file.

**Required outcome:** remove the tracked cache and prevent its reintroduction through ignore or packaging rules.

**Verification:** the delta and tracked inventory contain no Python caches; source tests remain runnable.

### R960-1-F6 — RESIDUE — Docs

**Artifacts:** new option-contract comments in src/core/mrp_mad.c:20, :36, :44, :61, :74, :88; src/core/mrp_pdu.c:21; src/include/shish_lan/mrp.h:27; src/ports/timer.h:28.

These comments explain behavior and reason but omit the governing issue ID. No newly introduced bench labels, review rounds, reviewer IDs or issue-comment IDs were found in the reviewed production-source comments.

**Authority:** supplied owner comment rule, 2026-10-15.

**Exact wording fix:** add “Issue: kebag-logic/milan-fpga#977.” to these option-contract blocks. Retain or add the existing requirement references: lookup/state preservation, clause 10.7; wheel, 10.7.11; Message ordering, 10.8.2; MAP, 10.3; validation, 10.8.3; replacement, 35.2.6 and Milan 4.2.7.2.2; copies, 10.7.8/35.2.2; lean transmit, Table 10-3/10.8.2.

**Impact/outcome:** comment traceability only. Change no behavior, figures, tests or conformance claims. The manager may carry this on the residue checklist.

**Verification:** inspect the comments for issue/requirement references and prohibited labels. This item leaves no lens unclean by itself.

## Independent executable evidence

| Check | Result | Receipt |
| --- | --- | --- |
| Full differential, generic and Milan | Each: 2 drivers, 22 builds, 200 seeds; all 36 mutants detected; zero problems | receipts/differential-off.{json,log,rc}; differential-on.{json,log,rc} |
| One-port accounting | Each affected MAD configuration: 177 equal normalized traces; 23 allocation-refusal seeds excluded | Differential JSON rows |
| Unit configurations | Default 27,199; Milan 27,187; scale 27,227; Milan+scale 27,215; key-only 27,227 passes; all rc 0 | receipts/unit-*.log; receipts/units.json |
| Independent wire/type boundaries | Base and eleven head configurations, each in both profiles: 24 builds/runs pass | receipts/boundaries.json; boundary-*.log |
| Empty LeaveAll | All four MSRP types: zero values; full FirstValue; no packed events; correct lengths/EndMarks; arbitrary ignored FirstValue accepted; truncation rejected before callbacks | boundary_probe.c and boundary logs |
| Sparse-type fault | Survives 200 supplied seeds per profile; independent test fails five assertions per profile after compilation | receipts/type-word-control.json and logs |
| Lean validation memory check | Both profiles: 200 clean head seeds; decoder control reports uninitialized read at seed 4, exit 86 | receipts/memory.json; memory-*.log |
| Default objects | All ten sources identical at -O2 and -Os; nine identical at -O0 | receipts/default-objects.json |
| Freestanding/embedded checks | rc 0; embedded check exercises both profiles | receipts/freestanding.{log,rc} |
| Documentation checks | Sentence, reference and reference self-test rc 0; 413 local links pass; 22 external URLs explicitly skipped locally | receipts/docs.{log,rc}; local-links.{log,rc} |
| Public hashes | 18 of 18 match the frozen publication | receipts/public-hashes.json |

Independent boundary configurations: default, key-only, timer-only, buckets-only, merge-only, each of the five end-station switches alone, and the combined set.
Memory-control diagnostics were retained, attributing detection to the planted read rather than merely a nonzero exit.
The differential checks return codes and trace digests. Excluded one-port refusal seeds are not behavioral comparisons.

## Reviewer-owned five-lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | State tables, gated event delivery, both Message writers, codec, MSRP/MVRP keys, authorized exception; differential/unit/LeaveAll probes | R960-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| RTL | CLEAN | Complete 20-file delta has no RTL; CMake host/embedded branches, callback/timer layouts, consistent compile-definition contract; public parent gitlink | R960-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Robustness | CLEAN | Timer order/rearming/wrap; bucket lifecycle/reclaim; reservation failure/rollback; stable merge/ties and failed-build prefixes; bounded reversal; memory diagnostics | R960-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Tests | UNCLEAN | Both trace drivers and 36 mutation rules; reversal selection and raw results; independently demonstrated sparse-word survivor; F1/F2 | R960-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Docs | UNCLEAN | CONTRIBUTING, README, five guides, PR/evidence, binary claims, release notes and generated-file inventory; F2–F5 open; F6 nonblocking | R960-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |

Each optimization was independently considered. Keys/buckets preserve examined identity, collisions, replacement order and reclamation. Timers preserve same-tick callback order, rearming, whole wheel turns and counter wrap. Message checks cover stable ordering, ascending/descending shortcuts, failed encodings, subtype bytes and zero-count LeaveAll vectors. One-port suppression retains its authorized allocation/policy exception. Lean validation, rapid replacement, bounded rollback copies and lean tx! preserve examined states and output bytes. Finite evidence is not exhaustive conformance.

## Earlier findings and hosted evidence

After writing the independent verdict/ledger, the PR discussion, submitted reviews and review threads were fetched. There were two review-start notices, zero submitted reviews, zero review threads and no public FINDINGS to resolve or retain. See receipts/prior-findings.json. No other reviewer's report was read.

The exact-source-head query returned no pull-request-triggered workflow runs and no commit status entries. Empty results are neither successful execution nor skipped-job receipts and do not establish the absence of every possible check context. See receipts/public-hosted.json.
Source-head execution evidence here is the author's published gate receipts plus the independent runs above. No manager source bank is claimed or inferred.

Public parent PR #993 at 095995243bc354b8a41755f3fdfae343511cc668 pins third_party/lwSRP to this exact head. The isolated lwSRP repository itself has no submodule gitlinks.

## Limits, integrity and pending manager duties

No source edits, commits, pushes, GitHub writes, parent banks, synthesis, hardware access or delegation were performed.
Builds and fault copies stayed under the packet's scratch/ directory. Foreground supervisors ran independent checks concurrently and joined their children before returning. Unit builds shared a single 16-job build pool. No heavy hardware build ran.
The original checkout needed no restoration: tracked blob bytes, executable modes and index match the required head. receipts/integrity.json lists every tracked blob, no discrepancies, an empty index diff, no gitlinks and clean status.

The full IEEE and Milan publications were not independently retrieved. This is a change-focused review against cited requirements, interface contracts, the baseline and the specific public IEEE encoding clarification. Existing documented limitations are not promoted into guarantees.
The random campaigns are finite and exclude documented one-port refusal seeds. No hardware calibration, target interoperability, full option-combination enumeration or exhaustive state-space proof follows.
Published reversal/equivalence campaigns were inspected as author evidence; independent executions are precisely those above. External-link crawling and graph rendering were not independently repeated.

The manager owns hosted/act acceptance and the final current-dev candidate, including builder/native banks and linked receipts after publication. The supplied live-dev reference is e275d7950ef3385753e6a15d2e191ba855b171ed; source review against d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b is distinct from that candidate. This report grants no candidate acceptance.
Physical calibration is NOT RUN. Field skips and historical route/integration summaries are not hardware proof.
The five open MINOR findings require correction and review before a positive verdict. The manager retains F6 on the residue checklist.

Portable scripts and raw receipts are enumerated in MANIFEST.sha256. Disposable scratch/ trees are excluded from publication.

R960-1 FINISHED
