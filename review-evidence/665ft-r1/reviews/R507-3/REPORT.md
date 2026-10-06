[R507] POSITIVE - exact head 6ca834a782a1bd5574d44998c8e214cf16df3441

External independent review R507-3, issue #665 / PR #675, lane FT. All five lenses are CLEAN within the assigned scope. R506-2 F1, F2 and F3 are resolved. No BLOCKER, MAJOR or MINOR remains in this review. One inherited prose RESIDUE remains. This source-review verdict does not authorize merging or certify hardware.

Tree: `79a9a6b116e9b839e744af76960a10588381a1bb`. Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`. The previous accepted head is `e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7`. This round reviews its three-commit delta (`7a2686ae`, `89b02c7f`, `6ca834a7`): six test/documentation files. The prior R507-2 determinations stand where that delta changes no examined artifact.

Reconstruction followed the assigned order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the issue body and frozen public decisions; requirements and interface authorities; base-to-head inventory/history and the complete round-three diff; then public execution evidence. Governing decisions are the [unit-test directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385), [FT assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6009234414), [round-two assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6012062072), and [round-three assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6014362247). The [review start](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6015367115) fixes this head. Authorities examined include REQUIREMENTS.md ownership/verification, MAILBOX_SPLIT.md, the saved-state store contract, `nvm_klj2.h:106`, the ADP port contract and [#678's ruling](https://github.com/kebag-logic/milan-fpga/issues/678).

The independent pass, probes, initial verdict and five-lens ledger were written before reading prior public review findings. Subsequent reconciliation used their published PR comments. No private author material, private review packet, or other checkout was read. The PR has no formal reviews or inline review comments at the API snapshot; prior findings are conversation comments.

**Round-three resolutions**

| Finding | All recorded lenses | Disposition at this head |
|---|---|---|
| R506-2 F1, exact loaded-header boundary | Conformance, Robustness, Tests | RESOLVED. `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:111` reseals a copy whose selected record claims a payload past the container end. One byte before the header ends returns REC; the exact header end returns the header's own LEN verdict, proving the guard passed. This repeats for every record. Lines 125 and 127 distinguish REC before the last framed payload end from OK at that end. All five shape controls pass. All four mutations at `nvm_mutants.py:149` fail the named test at the intended boundary assertion. See `receipts/codec.log` and `receipts/codec/`. |
| R506-2 F2, ADP exclusion premise and reach | Conformance, Tests, Docs | RESOLVED. `sw/firmware/gtest/README.md:216` distinguishes nine header-justified rows from five ADP rows; line 262 explicitly bases those five on #678's no-callback ruling until its header/guard follow-up lands. The following paragraphs identify every violating port, row, arc and resulting state, and limit the 100% claim accordingly. Independent public-call probes reach all claimed items, including row 5 through a reentrant link port. `adp_mbx.c:16` implements ports through the mailbox; `:88` delivers expiry from later event dispatch. No firmware guard is claimed to exist yet. |
| R506-2 F3, unplanted listener behaviors | Tests, Docs | RESOLVED. `sw/firmware/gtest/tally_cases.cpp:29`, `:59`, `:63`, `:67`, `:91`, and `:104` add the global environment, SIGBUS/FPE/ILL, disabled suite and teardown cases. `tally_selftest.py:79` records their expected counts; its DEFECTS table plants failures in the corresponding paths. All 18 controls pass; all 18 listener defects are caught. Omitting either the suite-failure count or program-failure count produces a false 1/0 PASS tally which the self-test explicitly rejects. Raw logs and per-mutation grading are under `receipts/tally/`. |
| R506-2 S1, explain omitted erased-record case | Docs | RESOLVED as a documentation suggestion. `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:86` names the omitted exact-header erased-record case and #677. This resolves disclosure, not the underlying memory defect. |

The ADP probes compile unmodified `adp.c` and use public entry points. Separate scenarios produce these nonzero gcov items: row 1 arc 2/2; row 2 arc 2/2; row 3 arc 4/4; row 4 arcs 2/4 and 4/4 with one stray expiry; row 5 arcs 2/4 and 4/4 with the owed flag cleared. Timer scenarios assert WAITING/NONE or DELAY/NONE. Link-port scenarios first assert DOWN with AVAILABLE owed, then poll with enable set or cleared. `receipts/adp/arcs.json` and six raw compressed gcov JSON receipts retain the measurements. These counterexamples violate #678's permitted port behavior; they validate the README's conditional explanation, not production correctness under reentrant callbacks.

**Earlier public findings**

Source records: [R507-1](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6012056114), [R506-1](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6011948437), [R507-2](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6014209924), and [R506-2](https://github.com/kebag-logic/milan-fpga/pull/675#issuecomment-6014356451). Identifiers and body digests are in `receipts/prior-findings-provenance.json`. Labels retain the original and overlapping lenses already recorded by the reviewers.

| Finding | Lenses | Disposition |
|---|---|---|
| R507-1 F1, reachable loaded-prefix exclusion | Conformance, Robustness, Tests, Docs | RESOLVED, including the exact-end strengthening above. The exclusion remains absent and the direct public test remains present. |
| R507-1 F2 and R506-1 S1, exclusion item identity | Conformance, Robustness, Tests, Docs; Tests, Docs for S1 | RESOLVED at R507-2 and unchanged. `fw_coverage.py:278` and `:317`, its self-test, and the ratchet have identical bytes to the reviewed head. Exact statement/arc/line binding and compensating-swap refusal remain. The current hosted job reports 28 coverage controls passing. |
| R506-1 F1, reachable pool guard excluded | Conformance, Robustness, Tests, Docs | RESOLVED at R507-2 and unchanged. `test_port_loop.cpp:229`, its two pool mutations and ratchet are outside this delta. The pool exclusion remains absent. |
| R506-1 F2, tally numbers not independently asserted | Conformance, Robustness, Tests, Docs | RESOLVED and strengthened here. `tally_wrong` compares exact counts and RESULT through the sweep scanner; all 18 cases and 18 defective listeners are executed, including false PASS tally lines. |
| R506-1 F3, version printing | Docs | RESOLVED at R507-2 and unchanged. Controller/coverage entry points retain version printing; current local and hosted receipts identify their compilers and test libraries. |
| R506-1 S2, inherited test-control environment | Robustness | RESOLVED at R507-2 and unchanged. `fw_gtest.py:85` drops `GTEST_*`; the disabled-test environment control passes again. |
| R506-1 R1, carried by R507-2 and R506-2 | Docs | RETAINED AS RESIDUE below. The body now attributes round-two evidence correctly, but its current-head no-run sentence is stale. |

**Independent execution and public evidence**

The three focused campaigns ran concurrently from an awaited foreground driver, without shell-background jobs. At most eleven compiler workers were possible. Builds, fixtures and mutations stayed under packet `scratch/`. Local compilation used gcc/gcov 16.2.1 and GoogleTest/GoogleMock 1.18.0. The specified 5.050 simulator identity was checked; no simulator build was needed for this delta.

| Receipt | Result and scope |
|---|---|
| `receipts/codec.log`, `codec.rc`, `codec/` | PASS. Tracked boot and codec tests at five shapes: 37 tests each, 185 total. Four boundary-mutated copies each exit 1 and identify `NvmCodec.codec_loaded_prefix`. Their rc 1 files are expected fault controls. |
| `receipts/tally.log`, `tally.rc`, `tally/` | PASS. All 18 controls agree with exact tallies and sweep verdicts; all 18 listener defects violate their intended case expectations. Individual raw logs contain intentional crashes, assertions and false PASS tallies being detected. |
| `receipts/adp.log`, `adp.rc`, `adp/` | PASS. Six public-call scenarios reproduce five exclusion rows, seven excluded arcs and the documented resulting states. |
| `receipts/docs-check.log`, `docs-check.rc` | PASS. Zero findings; 23/23 scrub controls and 4/4 routing controls. |
| `receipts/source-inventory.txt`, `round3.diff` | Exact three-commit/six-file delta; full source-range whitespace check passes. RTL, mailbox bench, gitlinks, shipping configuration, CI, coverage implementation/ratchet and listener implementation remain unchanged since R507-2. |
| `receipts/tree-integrity.json`, `tree-integrity.rc` | PASS. Raw blob bytes, modes, complete stage-zero indexes and required submodule registration/pins verified after probes. |

Reproduce with `python3 -B scripts/run_focused.py CHECKOUT FRESH_PACKET`, with these scripts under `FRESH_PACKET/scripts/`. The driver concurrently runs codec, tally and ADP modes of `focused.py`. `python3 -B scripts/verify_tree.py CHECKOUT` performs the identity audit. An initial reduced codec probe omitted the tally-label translation unit and did not link; the corrected probe includes the tracked boot test defining it. All reported codec verdicts are from successful corrected builds.

The [published round-one evidence](https://github.com/kebag-logic/milan-fpga/tree/b7eb2edc01e87810ff3e01629af0c9bc4a9438f1/review-evidence/665ft-r1) describes `27433e47`, not this head. Its inspected HANDOFF hash matches the published manifest (`receipts/public-evidence-provenance.json`). The [round-three REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6015346011) reports the complete source banks, 76 controller mutants, 106 NVM mutants, 434 NVM tests, coverage with/without the optional dependency, and the 48-command builder bank. Those public claims remain manager acceptance inputs, distinct from this review's focused reruns.

At **2026-10-06 11:42:33 UTC**, exact-head `firmware-unit` job **112247900469** in [run 37457222400](https://github.com/kebag-logic/milan-fpga/actions/runs/37457222400) had executed and passed. Its log reports 18 tally controls, 434 NVM tests, 28 coverage controls and coverage PASS for 14 files with gcc/gcov 13.3.0 and test libraries 1.14.0. The controller RV32 arm explicitly skipped for lack of its compiler; that is not a passed RV32 build. Four synthesis shards and one exhaustive simulation shard had passed; other required jobs were running. The physical job was skipped. `receipts/hosted-snapshot.json` preserves job/step status; `hosted-firmware-unit-excerpt.txt` records selected original log lines and the complete log digest. These observations do not grant hosted acceptance.

**Remaining finding**

[R507] RESIDUE Docs - R507-3-R1 (retains R506-1 R1 / R507-2 R1 / R506-2 R1) - PR #675 body, Status and Known limitations - Current-head hosted-status sentence is stale.

Authority/evidence: `receipts/pr-body.txt` says the round-three head has no hosted run. The dated snapshot and executed job above show one. Impact: descriptive prose only; no measurement, figure, verdict, test, generated artifact, conformance/clause claim or privacy rule changes. Required outcome / exact fix: replace both current-head no-run sentences with: "At the 2026-10-06 11:42:33 UTC snapshot, hosted run 37457222400 at 6ca834a7 had passed firmware-unit (job 112247900469); other required jobs were still running. The manager owns hosted and local-replica acceptance." Verification: compare the revised sentences with that snapshot, or use a newer explicitly dated exact-head observation. This residue leaves Docs CLEAN.

**Reviewer-owned lens results and ledger**

[R507] PASS Conformance - #665 assignment 6014362247; `sw/firmware/ctrl_nvm/nvm_klj2.h:106`; `test_nvm_codec.cpp:111`; `sw/firmware/gtest/README.md:216` - Exact loaded boundaries are distinguished, the listener proof covers its stated paths, and ADP coverage is expressly conditional on the published port rule. No product requirement or firmware behavior changes.

[R507] PASS RTL - `receipts/source-inventory.txt`; `sw/firmware/ctrl/adp/adp.c:180`; `adp_mbx.c:16`; `receipts/tree-integrity.json` - No RTL, clock/reset/CDC, production interface, state-machine, bench or gitlink change occurs. ADP call ordering and deferred adapter dispatch substantiate the documentation. R507-2's unchanged implementation and real mailbox-wiring evidence remain applicable.

[R507] PASS Robustness - `test_nvm_codec.cpp:90`; `tally_cases.cpp:29`; `scripts/adp_probe.c`; `receipts/{codec,tally,adp}.log` - Short prefixes, both boundary-error directions, all handled fatal signals, teardown/global failures, disabled suites and callback counterexamples are exercised. The omitted erased-record memory case is explicitly delimited below.

[R507] PASS Tests - `nvm_mutants.py:149`; `tally_selftest.py:79`; its `tally_wrong` and DEFECTS definitions; `receipts/codec/`; `receipts/tally/` - Controls pass, four boundary defects fail their intended assertions, and eighteen listener defects fail their intended expectations, including incorrect numbers despite independent failure markers. Accepted migration and coverage-gate artifacts remain unchanged.

[R507] PASS Docs - `sw/firmware/gtest/README.md:50`, `:262`; `sw/firmware/ctrl_nvm/README.md:442`; `test_nvm_codec.cpp:86`; public evidence and `receipts/docs-check.log` - Tally counts, exclusion premises, row/arc reach, mutation count and omitted case match execution. The stale hosted-status sentence is separately recorded as RESIDUE.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen FT/round-three scope; KLJ2 public contract and boundary assertions; conditional ADP coverage | R507-3 delta; R507-2 unchanged scope retained | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| RTL | CLEAN | Source inventory, unchanged RTL/bench/gitlinks, ADP state/port ordering, raw-tree audit | R507-3 delta; R507-2 unchanged scope retained | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Robustness | CLEAN | Five-shape codec/boot tests, four boundary defects, fatal/teardown/global/disabled tally cases, six callback probes | R507-3 delta; R507-2 unchanged scope retained | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Tests | CLEAN | Codec test/mutant diff; tally cases/self-test; raw positive/negative receipts; unchanged coverage gate | R507-3 delta; R507-2 unchanged scope retained | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Docs | CLEAN | Both README deltas, conditional row/arc claims, omitted-case comment, public evidence, R1 residue | R507-3 delta; R507-2 unchanged scope retained | 6ca834a782a1bd5574d44998c8e214cf16df3441 |

**Real limits and pending manager duties**

The pre-existing erased-record read past `loaded` in [#677](https://github.com/kebag-logic/milan-fpga/issues/677) remains open. Full backing buffers and a correct REC verdict do not prove memory safety. This assigned round judges the boundary-test correction and disclosure; it does not approve or resolve that defect. The standing round-two scope determination remains unchanged. #678's no-callback rule is now decided publicly, but its port-header changes and runtime guards remain follow-up work. Neither issue is called fixed merely because it has a separate ticket. The pre-existing controller RV32 SDK limitation remains #679.

No full parent, processor, gPTP, synthesis or builder bank was rerun. No RV32 build, optional external protocol arm, complete 106/76 mutation campaigns, local workflow replica, container orchestration or hardware run was performed by this reviewer in round three. Complete source-bank acceptance remains manager-owned. Physical calibration was **NOT RUN**. Model-time bounds, field skips and a skipped physical job are not hardware proof.

Source validation against `423ac5d910d09ab189b3acc39ae3ae1d10d50b19` is distinct from a live-dev merge candidate. The supplied live-dev reference is `bd884631684ccf5060339efa92263d5c3e5c262c`; the manager must use the actual remote tip at the merge turn, validate that candidate, accept mandatory hosted/local evidence, obtain the second independent positive review, confirm no review remains in flight, carry R1 to the residue checklist, and obtain explicit maintainer merge authorization. Publication, post-merge containment, appropriate issue/lane closure and project completion remain manager duties. #665 has later lanes, so FT completion alone does not complete its whole program.

The final audit verifies **1135** parent blobs and **558 / 104 / 214** required submodule blobs, all tracked modes and complete indexes, with zero mismatches. Required gitlinks remain protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The optional external gitlink stays uninitialized. No tracked source was edited; no GitHub write, commit, push or merge occurred. Only REPORT.md and files enumerated in MANIFEST.sha256 are publishable; `scratch/` is excluded.

R507-3 FINISHED
