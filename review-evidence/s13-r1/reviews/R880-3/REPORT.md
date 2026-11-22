[R880] POSITIVE - exact head dd163e41438acb86e0c4d4e76df90f3f91ace1c0

External independent review of issue #665 / PR #960, round R880-3.
Tree: `0e7909a8d02c4123c604c4a168a8b0cbfdd94e7e`.
Source base: `59b09884` (`dev-soft-core`). Delta base: `9413958c66c0dcd632b3e0e7ac44505314fed41a`.

All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains from this review. The retained identity-publication finding is resolved. The complete public packet supports carrying the bench and CPU evidence by identity; a full CPU re-measure is not required for this delta. One wording-only RESIDUE is recorded below.

The review used the repository contract, documentation index, issue body and public scope decisions, requirements and interface authorities, the base-to-head diff and four-commit delta, then public executable evidence. Prior public findings were reconciled after the independent diff pass. No other reviewer's current-round report or private author material was used. No source fix, commit, push, GitHub write, hardware operation or merge was performed.

**Public basis and scope**

- [Review start](https://github.com/kebag-logic/milan-fpga/pull/960#issuecomment-7073282855).
- [Frozen flip plan, item 6](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6799253003), [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7065258935), and [round-3 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7073088228).
- `REQUIREMENTS.md` sections 1 and 8; `docs/reference/FR_NFR.md:328-330`; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 7; `docs/design/MAILBOX_SPLIT.md:1804-1813`; public decisions on retained all-fabric builds, mandatory 8x8/1if, optional 2if, timing floors and 1x1 service bounds.
- Immutable [evidence publication](https://github.com/kebag-logic/milan-fpga/tree/c06e28ade922988b601abf8b6e6945bd5c890790/review-evidence/s13-r1), specifically `author-r3/receipts/`. The identity packet is `author-r3/receipts/identity/`.

`receipts/delta-paths.txt`, `delta.diff` and `history.txt` confirm four commits and seven changed paths: six documentation pages and `syn/resmap/soc_sweep.py`. The executable delta adds verification wiring and corrects assignment spacing. It changes no product RTL, firmware, config, builder, CPU-budget statement, submodule pin or image input. Previous clean results for untouched implementation remain applicable; each lens was applied to the changed artifacts and repaired evidence dependency.

**Identity finding: complete and replayable**

`independent_compare.py` imports no packet comparison code. It verified all 230 inner-manifest entries, exact file population, all 36 decompressed-content hashes and all 254 published round-3 receipt hashes in the outer publication manifest. No listed identity operand is missing or altered. The unmodified published `tools/replay.py .` returns 0 and ends `== RESULT: ALL CLAIMS HOLD` (`receipts/replay.txt`).

The five `binding.json.reencoded` entries match the round-2 manifest's old compressed digests, the round-3 manifest's new digests, and the decompressed digests in `MANIFEST.content.sha256`. Both old xz byte streams were independently reconstructed at preset 9 and match the old digests. Their content hashes equal the already-published round-1 cell hashes (`receipts/published-r1-cell-hashes.txt`). The three gzip files have explicit old/new/content provenance; their original compressed files were absent from round 2's publication. No claim is made to have recovered their original gzip header metadata. The newly published decompressed logs were compared in full.

| Independent comparison | 1x1/1if | 8x8/1if |
|---|---:|---:|
| Cell name/type/placement records equal | 86,465 | 109,093 |
| Complete route records byte-identical | 95,172 | 119,085 |
| INIT bits changed | 22 in 8 cells | 15 in 14 cells |
| JSON group pairs byte-identical | 7 | 6 |
| Differing raw-log lines | 4 | 4 |

Every changed cell is a CSR defaults ROM or platform ROM bank. All thirteen JSON pairs are byte-identical, without excluded leaves. Both complete `aecp-outputs` log pairs are equal. Across all thirteen raw-log pairs, the only eight differing lines are a WIRE line and a PASS mailbox-word line in `aecp` and `aecp-held` at each shape. Decoding those bytes identifies `2.96.0\0` becoming `3.96.0\0`, at payload offset 158 and mailbox stream offset 170. All other line content, ordering and counts agree. See `receipts/independent-compare.txt`.

The replay's bitstream, ELF, ROM, export-metadata and sixteen harness-image comparisons were inspected against their actual output:

- 1x1 `.bit`: 103 changed bytes = design-name text 71, date 1, time 5, configuration CRC 4, frame data 22. Frame data changes 22 bits in seven frames.
- 8x8 `.bit`: 93 changed bytes = design-name text 69, date 1, time 4, configuration CRC 4, frame data 15. Frame data changes 15 bits in seven frames.
- Platform and harness ELF pairs differ in six loaded bytes only: the firmware-version character and the instruction pair loading its descriptor-image CRC. Layout, other file bytes and harness group partitions agree. ROM banks match the ELF load segments.
- Export differences are the descriptor CRC/hash, version and image hashes, payload hashes and the named generated timestamp. No additional behavioral field differs. The `.bit` design-name digests and build date/time are header metadata, not loaded firmware.
- Exact-head author receipts bind the two flip exports' 19 and 16 inputs to the built images and all sixteen harness head images to the exact-head rebuilds. The source-path delta independently confirms their inputs are untouched since round 2.

The unmodified `tools/rmutants.py` returns 0: grader self-check 4/4, unplanted replay passes, and 13/13 plants reach RESULT with their own named FAIL marker (`receipts/rmutants.txt`). An unrelated failure alone is not counted. The outside-version digit plant fails as NOT ANCHORED. The removed operand fails by name without a traceback. These close the publication defect and requested grading/refusal improvements at their causes.

**Prior finding reconciliation**

| Prior ID | Disposition at this head | Evidence at its cause |
|---|---|---|
| R880-1-F2 = R880-2-F1 = R879-2-F1 | RESOLVED | Complete published population and hashes; unmodified replay; thirteen named plants; independent complete cell/route/INIT and JSON/raw-log comparisons above. |
| R880-2-F2 | RESOLVED | PR body fetches full `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` and asserts HEAD. Exact-SHA fetch and FETCH_HEAD/HEAD assertions pass (`pr-fetch.txt`, `pr-fetch.rc`; body in `public-scope.json`). |
| R880-2-S1 | IMPLEMENTED | `identity/tools/rmutants.py:26-40,149-179`: passing unplanted control precedes grading; each plant requires nonzero exit, RESULT and its marker; unrelated-only output fails the synthetic control. |
| R879-2-S1 | IMPLEMENTED | `soc_sweep.py:253-304,371` runs prepare/export wiring. Independent probes omit builder placement, bypass image refusal, force split export, use the wrong image root and omit the include flag: all five fail at their named check; unplanted control passes. |
| R879-2-S2 | IMPLEMENTED | `identity/tools/replay.py:478-532` derives version strings from arm images and anchors WIRE/mailbox differences; named plant and independent decoded-log comparison pass. |
| R879-2-S3 | IMPLEMENTED | `identity/tools/replay.py:85-94,534-543` refuses absent operands by name; the thirteenth plant reaches RESULT and is caught. |
| R879-2-S4/S5 | APPLIED | `soc_sweep.py:135` restores `env = {`; `MILAN_COMPLIANCE_MATRIX.md:4-7` keeps one bench-evidence pointer. |
| R879-2-R1 / R880-2-R1 | APPLIED | `ENDSTATION_BUILDER.md:3-4`, `INTEGRATION_GUIDE.md:3-4`, `FR_NFR.md:109,173`, `FPGA_DESIGN.md:313`, `TESTING.md:731`. Allocator labels now say all-fabric; normative status and clause text are unchanged. |
| R880-1-F1 | REMAINS RESOLVED | `soc_sweep.py:65-80,105-121,133`; all-fabric plan; independent wiring/refusal probes. Exact-head author `f1/rsweep-dd163e41.txt` records ship/axilite accepted with zero platform images, six expected refusals, and split refused before export. |
| R880-1-F3 | REMAINS RESOLVED | Replay parses both headers by field; counts above distinguish design text, dates, times, CRC and frame bytes. No changed dependency invalidates the earlier independent parsing. |
| R880-1-F4 | REMAINS RESOLVED | `MAILBOX_SPLIT.md:1808-1813` names the firmware-version exception and both artifacts, matching builder gate 23o. Untouched this round. |
| R879-F1 | REMAINS RESOLVED | `register_page.py:519,652,714` and generated `REGISTER_MAP.md` label all-fabric provenance and point to the split map. Fresh generation and 61/61 controls pass. Public split-map follow-up remains a manager duty. |
| R879-F2 | REMAINS RESOLVED | README split prerequisite/ROM boot/major 3 and explicitly all-fabric pipeline remain unchanged. The round-3 author diagram check passes; earlier rendered-file identity stands. |
| R879-S1 | REMAINS RESOLVED | `ctrl_service_budget/build.py:355,382` retains one harness image argument. Unchanged; author exact-head checks and both argument plants pass, and rebuilt image hashes bind the evidence. |
| R880-1-R1 / R879-R1 | REMAIN APPLIED | Corrected overview, mailbox and compliance wording remains intact. This round removes the remaining labels listed above. |

**New wording residue**

R880-3-R1 | RESIDUE | Docs | `author-r3/receipts/INDEX.md:1`.

Authority/evidence: the round-3 receipt index is headed `# Receipts index, round 2`, although its entries identify `dd163e41` and the round-3 packet. Impact: stale presentation label only; no measurement, figure, test, verdict, generated product artifact, clause claim or privacy rule changes. Exact required fix: replace that heading with `# Receipts index, round 3` in the next publication. Verification: inspect the heading; preserve all receipt entries and hashes. This does not make Docs unclean.

No new prohibited lane/reviewer/comment identifier was found in added source comments.

**Lens results and reviewer-owned ledger**

[R880] PASS Conformance - `REQUIREMENTS.md:27-36`, `FR_NFR.md:328-330`, split architecture section 7, identity packet and `receipts/independent-compare.txt` - frozen flip scope preserved; repaired evidence supports identity carry at both required shapes. Both scoped flip-grade commands return PASS.

[R880] PASS RTL - `hdl/common/csr/milan_csr.sv:2002`, `hdl/milan/milan_datapath.sv:2850`, `receipts/delta-paths.txt`, both routed cell/net dumps - no changed RTL or image inputs; prior clean RTL result carries, reinforced by complete independent placement/route/INIT comparison.

[R880] PASS Robustness - `soc_sweep.py:105-121,133,253-304`, `receipts/wiring-probes.txt`, identity refusal controls - all-fabric remains independent of an absent split image; missing-image refusal and placement forwarding are exercised; absent evidence fails closed by name.

[R880] PASS Tests - `identity/tools/replay.py`, `identity/tools/rmutants.py`, `soc_sweep.py:371`, `receipts/replay.txt`, `rmutants.txt`, `independent-compare.txt`, `wiring-probes.txt` - controls pass before plants; thirteen operand defects and five independent wiring defects fail their intended checks; complete comparisons exclude no group or JSON field.

[R880] PASS Docs - six documentation paths in `receipts/delta-paths.txt`, PR checkout recipe, public manifests and documentation receipts - placement labels and checkout corrected; evidence replayable; focused exact-head documentation gates pass. R880-3-R1 is wording-only residue.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #665 decisions; REQUIREMENTS s1; NFR-SCOUT-01/02/03; split s7; shipping/harness identity operands; scoped flip checks | R880-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| RTL | CLEAN | CSR/datapath VERSION chain; four-commit path diff; complete cell, route, INIT and ROM comparisons | R880-3, carrying untouched R880-2/R880-1 results | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Robustness | CLEAN | Sweep prepare/export wiring and refusals; five plants; missing-operand and outside-version controls | R880-3, carrying untouched R880-2 runtime coverage | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Tests | CLEAN | Published replay and thirteen plants; independent complete comparisons; sweep control and five plants; author receipts | R880-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |
| Docs | CLEAN | Six changed pages; PR recipe; public manifests/index; docs gates; generated register reference | R880-3 | dd163e41438acb86e0c4d4e76df90f3f91ace1c0 |

**Verification and limits**

Reviewer executions: public replay, thirteen operand plants, independent comparison, sweep self-test, five in-memory wiring probes, both scoped flip-grade checks, exact-SHA fetch, and twelve focused documentation checks. The register checks initially refused because this environment lacked the pinned renderer. After installing that dependency only into disposable scratch, the reference is fresh and its self-test passes 61/61. Initial and corrected receipts are retained; environment refusal is not counted as a pass. No full implementation bank was rerun.

The author publishes source receipts at the exact head. Its docs-workflow transcript reports 99 successful commands and four CI-environment failures; the latter are not executed-pass evidence. Unchanged full-bank evidence carries under the delta rule. There is no manager source bank at this head, and none is inferred. Hosted/act acceptance was not independently executed or certified here.

The archive is verified by immutable Git identity and SHA-256 manifests. Its commit reports no Git signature, so no cryptographic signer attestation is claimed. Routed checkpoint dumps were compared; the large checkpoint binaries themselves are not in the packet. Rebuilt-image receipts were inspected, not reproduced through a full build. Gzip provenance has the limit stated above. These limits do not conceal a remaining comparison gap in the published operands.

Physical calibration is NOT RUN here. Field skips are not hardware proof. Physical qualification, deferred release soak/power obligations, optional 2if debt and the ruled #954 follow-up are not cleared by these checks. The previously recorded distinction between the default flip and NFR-SCOUT-02's final processor deletion remains an owner/documentation duty, not a newly altered requirement in this delta.

`receipts/checkout.txt` verifies exact tracked blobs, executable/symlink modes and index entries: 1,935 superproject files and all initialized dependency files. Required gitlinks remain protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`, gPTP processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, and stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`. The additional lwSRP checkout verifies. The external gitlink remains uninitialized and untouched. The working tree is clean.

**Pending manager duties**

Publish this report and only manifest-listed receipts; carry R880-3-R1 to the residue checklist. Obtain the other independent exact-head verdict and finish the review ledger. Open/link the promised split-register-map follow-up and retain existing owner decisions and physical/deferred obligations. Validate the final current-dev candidate against the live base identified for this merge turn (`e275d7950ef3385753e6a15d2e191ba855b171ed`), including builder/native banks, and publish its own receipts. Complete required hosted/local acceptance, obtain explicit merge authorization and perform post-merge containment. This source-head review neither validates that future candidate nor closes issue #665.

Portable scripts and raw receipts are listed in `MANIFEST.sha256`. `scratch/` is disposable and must not be published.

R880-3 FINISHED
