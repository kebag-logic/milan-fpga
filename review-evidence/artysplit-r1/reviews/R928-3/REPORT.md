[R928] NEGATIVE - exact head 011aaa6f080321e0a89f915720ebb3ee14807a16

External independent review R928-3 of [PR #1004](https://github.com/kebag-logic/milan-fpga/pull/1004), relating to [#878](https://github.com/kebag-logic/milan-fpga/issues/878). Tree: `5b11a07de8c4f69999277424aa8d9b704c297a96`. All five lenses were applied. The original census publication finding remains open, and two boundary defects were found in the new extractor. No firmware or RTL regression is asserted.

**Scope and authority**

The review reconstructed repository instructions, the documentation map, frozen acceptance and public scope decisions, requirements/interfaces, the original-base diff/history, and published execution evidence. The independent delta verdict and ledger were written before reading prior reviewers' findings. This round concentrates on `4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1..011aaa6f080321e0a89f915720ebb3ee14807a16`; unchanged code retains prior coverage under the requested later-round rule.

The delta is 13 files and five commits. Configuration values and the four existing Python helpers' ASTs are unchanged. There is no RTL, compiled firmware, scheduler-row, image or submodule-pin change. The two functional tooling changes are `census_extract.py` and the regrader's part-limit handling. `receipts/source-integrity.log` records these checks.

The [acceptance ruling](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7153532537) permits this PR to merge on its own gates, accepts endpoint counters as the item-5 capture substitute, and keeps #878 open for the offset measurement through #1007. The [80 MHz](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097204685), [shape](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7096503672), and [held-egress](https://github.com/kebag-logic/milan-fpga/issues/878#issuecomment-7097474930) rulings remain unchanged. REQUIREMENTS.md, FR_NFR.md 3.4.1, the clock/register authorities, `ctrl_loop.h` THE SHAPES and SPLIT_CONTROL_MEMORY.md section 15 supply the relevant contracts.

In this report **P** is [the evidence packet at 7ae7427b](https://github.com/kebag-logic/milan-fpga/tree/7ae7427b0d5a021db3387fa50833abde7bf18a82/review-evidence/artysplit-r1), **E8** is `P/author-r8/receipts`, and **E7** is `P/author-r7/receipts`. Local receipt links are relative to this report.

**R928-3-F1 - MAJOR - Conformance, Tests, Docs - published observation bytes disagree with the extract's integrity records**

Artifact: `E8/census-extract/census/answering-later/notice-retried-0/{manifest.json,observations.log}`, `E8/FILES.tsv.part0001.txt`, `E8/census-extract/FILES.json`, `P/MANIFEST.json`; PR “Reproduce and inspect”.

Authority/evidence: the prior R928-2-F1 requires an accessible, hash-bound census that the current regrader can reproduce. All 820 round-8 files match the outer publication manifest. However, 27 observation parts across 24 cases differ from their inner recorded hashes. The outer manifest explicitly records the transformations and their original/published hashes; the inner case manifests, census mapping and FILES inventory still identify the original bytes.

For the first failure, the recorded observation hash is `c0b0d98f768a9741d075a873a62246bc8db056a110c14da3e0e91baed7e0632b`; the published hash is `b53f5b6342e055e4d98f2bc162f02e35f7dae8666d33d0171e037300f01eb9cb`. Both lengths are 8,042,329 bytes. This is a publication mismatch, not a failed download: the downloaded bytes also match the published Git blob.

The unmodified current `receipt_regrade.py` reproduces the first 16 grades, then exits 1 with `part integrity failure: observations.log`. The prescribed copy without `srp-bound` fails at the same earlier case. It never reaches the disposition refusal. Neither run reproduces the advertised 147-case/cross-case result from the published packet.

A diagnostic changed only integrity metadata in a disposable copy to bind the actual published bytes. It reproduced 146 complete grades, then refused `valid-destinations/srp-talker`: `passes.polls.passes` is 160455 instead of the recorded 160456. A focused replay captured that single differing field. Thus updating hashes alone is insufficient. The specific transformed byte responsible was not isolated.

Impact: the published inputs fail both integrity and complete-grade reproduction; the required cross-case and negative-control proofs remain unavailable through the documented commands. This retains R928-2-F1/R928-1-F1 and adds a demonstrated grade mismatch, hence MAJOR. It does not establish a firmware execution defect.

Required outcome: publish a consistent packet after any necessary privacy transformations. Bind the actual public parts, assembled observations, case manifests and census to one another, update the inventories, and retain an explicit original-to-published transformation record. Preserve every grading-relevant observation and the original measured grade; do not merely replace the expected poll count or weaken comparison. Do not describe transformed observation bytes as unchanged originals. Replay the downloaded final publication before claiming it reproduces the qualification.

Verification: the unmodified current regrader must reproduce all 147 grades and the cross-case step from the published archive; the missing-`srp-bound` copy must reach and fail the named disposition condition. See [inventory mismatches](receipts/inventory-mismatches.json), [publication transformations](receipts/published-transforms.json), [replay](receipts/regrade.log), [control](receipts/missing-bound.log), and [packet audit](receipts/packet-audit.log).

**R928-3-F2 - MINOR - Robustness, Tests, Docs - the extractor rejects a part at its own documented maximum**

Artifact: `tb/verilator/ctrl_service_budget/census_extract.py:58`, `:120`; `receipt_regrade.py:46` and `:192`.

Authority/evidence: `parts()` documents and emits parts of at most 14,000,000 bytes. `case()` immediately calls `regrade(..., limit=PART_LIMIT)`, whose reader rejects `len(data) >= limit`. The CLI regrader correctly uses the declared inclusive maximum plus one, but the extractor's own validation does not.

The portable probe uses a real published case with ignorable diagnostic lines. At 13,999,999 observation bytes, `case()` reproduces the complete original grade. At 14,000,000 bytes it raises `part integrity failure`, before grading. A 14,000,001-byte input also emits a first part of exactly 14,000,000 bytes and triggers the same mismatch. The supplied census's largest part is 13,999,999 bytes, so this does not explain F1.

Impact: valid inputs can fail extraction solely because a newline lands exactly at the advertised limit.

Required outcome: use one consistent inclusive/exclusive part-size contract in the writer, `case()`, CLI and documentation. Add a control exercising an exact-limit part and a multi-part input with an exact-limit first part.

Verification: [probe_extract.py](probe_extract.py) and [boundary receipt](receipts/extractor-boundaries.log); both valid boundary cases must round-trip and reproduce their grades.

**R928-3-F3 - MINOR - Robustness, Tests - an overlong observation line prevents forward progress**

Artifact: `tb/verilator/ctrl_service_budget/census_extract.py:63-71`.

Authority/evidence: malformed-input handling belongs to the Robustness lens. If no newline occurs in the candidate part, `rfind()` returns -1 and the next `end` becomes zero. `start` therefore remains zero on the first iteration. The writer repeats empty numbered parts indefinitely instead of refusing the input. The bounded probe intercepts writes and stops after three calls; the actual writer emits lengths `[0, 0, 0]` for a 14,000,001-byte line.

Impact: malformed input can cause unbounded file creation and consume storage/inodes. No overlong line was found in the published corpus, and the probe did not allow unbounded writes.

Required outcome: reject a line that cannot fit the supported part format, or partition it with a supported lossless rule. Every nonempty-input iteration must advance. Add a missing-newline/overlong-line control, including after an already emitted part.

Verification: [probe_extract.py](probe_extract.py) and [boundary receipt](receipts/extractor-boundaries.log); the operation must terminate with a bounded result or explicit refusal.

**Prior finding dispositions**

Prior public rounds: [R928-2](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7210527623), [R927-2](https://github.com/kebag-logic/milan-fpga/pull/1004#issuecomment-7210534024). Earlier closed findings are retained only where the delta leaves their artifacts and dependencies unchanged.

| Prior finding | Disposition at this head | Cause-level evidence |
|---|---|---|
| R928-2-F1; retained R928-1-F1 census portion | PARTLY RESOLVED; replay retained as F1 | All 762 extract files are now accessible; paired identities are supplied. The publication has 27 stale inner hashes and the documented replay stops after 16 cases. |
| R928-2-F2, routed-total comparison | CLOSED | Both routed reports say `Physopt postRoute`, identify retained checkpoint/bitstream hashes, and report 33,015 LUT, 40,369 FF, 13,791 slices and 78 BRAM. LUT delta is 0, within the approximately 50-LUT band. |
| R927-2-F1, unowned Arty registration debt | CLOSED as raised | [#1022](https://github.com/kebag-logic/milan-fpga/issues/1022) explicitly owns `arty-1x1` measurement and derivation after #977. Section 15 cites it. The no-disposition receipt is published and its derivation reproduces byte for byte. This tracks the debt; it does not discharge it. |
| R927-2-F2, superseded qualification pointer | CLOSED | README:208-211 cites `076e7cc7c4f560605b3421be531a044dacafb17e7e99251ef5bbf4b65eb9a09e`, 147 groups; its model equals current `arty_grade.py`. The 145-case receipt is explicitly historical. |
| R928-1-F2 and R927-1-RS2, source chronology | CLOSED, carried | Previously corrected comments remain unchanged. No new prohibited source-comment chronology was found in this delta. |
| R928-1-F3 / R927-1-F1, acceptance and issue closure | CLOSED as scope findings, carried | Public acceptance ruling remains authoritative; the current PR says “Relates to #878”. Offset work remains open. |
| R927-1-F2/F3, inventory and idiom | CLOSED | Both focused gates pass again. Existing helper ASTs are unchanged. |
| R927-1-F4/F5, MII guard and console truncation | CLOSED, carried | Their firmware, host tests, mutation cases and interface contracts are unchanged since R928-2's focused tests and plants. |
| R927-1-F6, qualification hash | CLOSED | Current published qualification hash and owner model verify; the later pointer defect is also closed above. |

**Residues and suggestions**

R928-2-RS1 and R927-2-SG8 are closed: fixture comments no longer contain lane/round labels, and their AST/value-bearing code is unchanged. R927-1-RS1/RS3/RS4/RS5 are closed by the calibration-comment removal, decision links, both VERSION values and S25FL128S comment. R927-2-RS-A/RS-B/RS-C and R927-1-RS6 are closed in the CHANGELOG/current PR. RS-D is corrected in the current PR and round-8 index, with one historical wording residue below.

**R928-3-RS1 - RESIDUE - Docs - retained R927-2-RS-D in the historical index.** Artifact: `E7/INDEX.md:128-130` still says “ELF, flash image and stimulus is identical”. Authority/evidence: paired inventory has `flash_image: [null, null]` and `xip: [false, false]`; `build.py:906-921` emits a separate image only for XIP. Impact: the old wording suggests an additional comparison, although the current explanation is correct. Exact fix: replace that phrase with “ELF and stimulus are identical; these non-XIP variants produce no separate flash image”. Verification: inspect the corrected explanatory text; no recorded measurement or grade changes. This residue does not unclean a lens.

| Optional item | Disposition / evidence / suggested verification |
|---|---|
| R928-2-SG1, four EOF blank lines | CLOSED; original-base `git diff --check` passes. |
| R927-2-SG3/SG6, row selection and ROM headroom | CLOSED; section 15 states pace/queued/slice ordering and 1,404 bytes before another ROM bank. |
| R927-2-SG1, timing tie-break (Tests) | RETAINED optional; unchanged regrader chooses by directive-name tie-break. Align it with the image grader or compare selected payload identity. Both previously reviewed tied directives identify one payload. |
| R927-2-SG2, general receipt controls (Robustness, Tests) | RETAINED optional beyond the concrete required F2/F3 controls. A compact self-test can exercise escape, hash, grade, native-status and owner-model refusals. |
| R927-2-SG4, complete second-step build records (Tests) | Paired executable/ELF/stimulus inventory is now supplied. Full per-step `build.json`/input records remain an optional provenance improvement; compare them with the published identities if added. |
| R927-2-SG5, derivation recipes (Tests, Docs) | RETAINED optional; recipes remain external to the source tree. Consider making the cost census and derivation a versioned in-tree entry point, preserving reproduced output. |
| R927-1-SG1 / R927-2-SG7, signed-width guard (RTL, Robustness) | RETAINED optional; `KL_gptp_txret.sv:310` is unchanged and no present overflow was found. An elaboration guard could bound the parameter plus runtime correction. |
| R927-1-SG3 / R927-2-SG7, old inventory description (Docs) | RETAINED optional; `scripts/docs_inventory.json:236` retains retired/83.333 MHz wording. Update its description and regenerate/check the audit together if adopted. |
| R927-1-SG4 / R927-2-SG7, harness config naming (Tests, Docs) | RETAINED optional; the harness still names `endstation_arty_current`. Current shape and 80 MHz clock agree. Directly naming the split config would simplify provenance; preserve generated-input checks. |
| R927-1-SG2, retry accounting | CLOSED, carried; no relevant firmware delta. |

These suggestions do not affect clean coverage.

**Evidence and checks**

The 762-file extract totals 1,434,762,896 bytes. Its 759 case-file mappings reference 22,600 source inventory entries; all source references match the prior FILES inventory. All 147 case-manifest hashes verify. The paired receipt contains eight executable/ELF pairs and 147 stimulus pairs; each pair agrees, every stimulus's downloaded bytes agree, and case manifests bind the corresponding executable/ELF digests. This checks the published inventory, not independently rebuilt binaries. `flash:null` is correct for these non-XIP builds.

The no-disposition derivation produces exactly the published JSON bytes, SHA256 `3b35c7b0610da5215ffaf5a52120b697da24355c4df80ddf000069cf26fb2a91`: 52 candidates, all with owner-bound findings, zero qualified choices, minimum finite last notice 225.54 ms, load 0.6205560614. This replays the arithmetic from published merged maxima; it does not remeasure omitted cost spans. [Claim checks](receipts/claim-checks.json) also record routed totals and the qualification comparison.

The installed owner model remains load 0.5004771140, ACMP 29.77 ms, txL 48.82 ms and last notice 117.47 ms, against 0.70/30/49/140. Its row remains slice 1250 us, pace 10 ms, queued bound 125 ms and transmit bound 35 ms. The [#969 disposition](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252) remains conditional; `kept_grade.Disposition` and the regrader's cross-case body are unchanged by this delta except for the new part-limit argument. All 32 focused kept-grade controls pass.

The supplemental hash-rebinding diagnostic is deliberately not repaired evidence: observation bytes and expected grades were untouched, while only part/whole/manifest/census hashes changed in a disposable copy. The current regrader passed 146 grades and failed the last case before cross-case qualification. [Grade differences](receipts/grade-differences.json) isolate the poll-pass count (160456 recorded, 160455 reproduced). [Diagnostic replay](receipts/rebound.log) and [its preparation](receipts/rebound-prepare.log) preserve the result. Neither this diagnostic nor the original integrity failure verifies the intended missing-bound refusal.

| Executed check | Result | Receipt |
|---|---|---|
| Original published extract replay | Exit 1 after 16 complete grades; integrity refusal | `receipts/regrade.log`, `.rc` |
| Original extract minus `srp-bound` | Exit 1 at the same integrity refusal; intended control not reached | `receipts/missing-bound.log`, `.rc` |
| Hash-rebound diagnostic / focused differing case | Both exit 1; 146 grades reproduce, then one poll-count field differs | `receipts/rebound.log`, `receipts/grade-differences.json` |
| Inner inventory audit | Exit 1; 27 mismatches | `receipts/packet-audit.log`, `.rc` |
| Outer publication manifest | All 820 round-8 files match | `receipts/outer-manifest-check.txt` |
| Extractor boundary probes | Exact-limit failure and non-progress reproduced | `receipts/extractor-boundaries.log` |
| No-disposition arithmetic | Exit 0; byte-identical NO QUALIFIED MODEL receipt | `receipts/no-disposition-derived.json`, `.rc` |
| Owner model / kept controls | Exit 0 / 32 checks pass | `receipts/owner-model.log`, `receipts/kept-controls.log` |
| Documentation check, inventory, Python idiom | All exit 0 | Corresponding logs and `.rc` files in `receipts/` |
| Tracked bytes/modes/index and required gitlinks | PASS | `receipts/source-integrity.log` |

Here `$SOURCE` is the exact-head checkout and `$PACKET` contains this report. Portable reproduction entry points (run from the source checkout; choose fresh scratch destinations for the preparation scripts):

```sh
python3 -B "$PACKET/fetch_public.py" "$PACKET/scratch"
python3 -B "$PACKET/audit_packet.py" "$SOURCE" "$PACKET/scratch"
TMPDIR="$PACKET/scratch" python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$PACKET/scratch/author-r8/receipts/census-extract"
python3 -B "$PACKET/prepare_missing_bound.py" "$PACKET/scratch/author-r8/receipts/census-extract" "$PACKET/scratch/control-new"
TMPDIR="$PACKET/scratch" python3 -B tb/verilator/ctrl_service_budget/receipt_regrade.py "$PACKET/scratch/control-new"
python3 -B "$PACKET/probe_extract.py" "$SOURCE" "$PACKET/scratch/boundary-new" "$PACKET/scratch/author-r8/receipts/census-extract"
python3 -B "$PACKET/check_source.py" "$SOURCE"
```

`prepare_diagnostic.py` and `diagnose_grade.py` reproduce the explicitly labelled supplemental probe. `fetch_public.py` reads only the pinned packet's author evidence and metadata, and excludes reviewers' report contents.

The author's round-8 gate receipts identify this exact head. Their source firmware/native execution evidence remains at `74f942be5`, with unchanged inputs for those gates. No manager source bank exists at this head, and none is inferred. The prior timing-report coverage carries because neither image inputs nor timing parser changed; this round independently resolves the separate routed-resource comparison from both post-route reports.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | #878 acceptance/rulings; #969; #1022; FR_NFR 3.4.1; `ctrl_loop.h:402`; section 15; published qualification and failed original replay | R928-3 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| RTL | CLEAN | Delta and AST/YAML invariance; required gitlinks; E8 paired identity; both `route-utilization/*-route-utilization.rpt:10,35`; checkpoint/image bindings; carried unchanged clock/CDC/interface coverage from R928-2 | R928-3 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Robustness | UNCLEAN: F2, F3 | `census_extract.py:58-74,120`; reader limits; real-case exact-boundary and bounded malformed-line probes; kept-grade controls | R928-3 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Tests | UNCLEAN: F1, F2, F3 | Current regrader; 147 manifests; inventories; original and control replays; extractor probes; paired identities; derivation replay | R928-3 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |
| Docs | UNCLEAN: F1, F2 | Changed README/section 15/guides/comments; PR reproduction claims; inner/outer manifests; part-size contract; focused documentation gates | R928-3 | `011aaa6f080321e0a89f915720ebb3ee14807a16` |

**Real limits and pending manager duties**

- The original publication does not pass the full replay or intended missing-group control. A local diagnostic is not repaired public evidence.
- Public hash/Git-blob bindings were checked. The evidence commit's API verification status is `unsigned`; no cryptographic signature validation is claimed.
- No firmware, RTL, full native/build banks, synthesis, route, hardware, local workflow replica or host orchestrator was run. No source fix, commit, push, external comment or merge was performed. No other current reviewer report or private author material was used.
- Physical calibration is NOT RUN. Field skips are not hardware proof. Bench reports concern the earlier `248d85c1` image, not the current routed image. The manager's offset/capture disposition remains exactly as published.
- The manager owns corrected evidence publication, re-review of fixes, hosted/executed-versus-skipped context acceptance and the local replica. No hosted-green claim is made here.
- The separately running integration delta needs its own review. Before merge, the manager must validate the candidate against the then-current target; the supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`, distinct from source comparison base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. Required builder/native candidate banks remain pending.
- Two independent positive reviews, reviewer-owned clean coverage, no in-flight review, maintainer authorization and post-merge containment remain required. Keep #878 open for its offset line and #1022 open for the owed registration work. Carry RS1 to the residue checklist.
- Final integrity verification compares every parent tracked blob/mode and index entry to HEAD, plus all five required initialized submodules. The external submodule's gitlink is unchanged; its checkout is uninitialized and was not required for these checks. All disposable inputs/probes remain under `scratch/` and are excluded from publication.

R928-3 FINISHED
