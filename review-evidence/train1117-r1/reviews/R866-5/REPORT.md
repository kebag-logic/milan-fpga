[R866] POSITIVE - exact head 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd

External independent delta review, R866-5, PR #945, tree `22335ec4d79d67a5b9a2e0e7ab480fd868be9bba`.

R866-4-F1 is RESOLVED. The complete final-source timing evidence remainder carried from R870-2-F2 (original ID R870-1-F2) is also RESOLVED for this train head. No open BLOCKER, MAJOR or MINOR remains in this review's scope. The separate current-dev merge-candidate validation is still required. One new wording residue and the retained residues/suggestions appear below.

## Scope and provenance

This is an evidence-only recheck at the unchanged R866-4 head. AGENTS.md, CONTRIBUTING.md, docs/README.md, all sixteen assigned issue contracts and relevant public decisions were reconstructed before the technical evidence pass. Authorities include REQUIREMENTS.md section 1, FR_NFR.md 3.4.1, the SRP/mailbox contracts, QSPI_FLASHBOOT.md, and #665's composition and final-measurement rulings. The full `cb96336d..8dc85884` diff and history were acquired; independent review concentrated on the named evidence delta and its dependencies. Unchanged code retains its previous lens coverage.

The independent delta verdict and five-lens ledger were written before reading other reviewers' reports. Prior public findings were then reconciled. No private author material, management checkout or other reviewer's local packet was read.

All author paths below are relative to [author-r7 at archive 9faf6fa8](https://github.com/kebag-logic/milan-fpga/tree/9faf6fa8a1f86f5cd27f93731eed9e4e5a426436/review-evidence/train1117-r1/author-r7). `check_evidence.py` verifies all 7,409 manifest entries for author-r6/r7. The complete comparison has 26 changed files: HANDOFF-r5.md, PR-BODY.md, INDEX.md, the named loaded-identity directory, the two four-file build directories and bench-images-8c5e2b4f.txt. Nothing else differs. Existing artifact lists and identity logs are unchanged. The archive commit is unsigned; this establishes published content integrity, not signer authentication.

## R866-4-F1: resolved at its cause

Authority: [the original finding](https://github.com/kebag-logic/milan-fpga/pull/945#issuecomment-7049051089), AGENTS.md sections 2/6/7, and the assigned product-to-gating identity requirement.

The new `receipts/step16/gating/loaded-identity/{1x1,8x8}.txt` receipts bind these full identities:

| Point | Gating ELF SHA-256 | Product ELF SHA-256 | File length |
|---|---|---|---:|
| 1x1/1if | `c873a0aa8b9c39a003d7a78616c83d6469935debb5bb1107ad477b900ee607fb` | `fe12a3f1efce3c85f591b046888fcb40809a64486c512e2f025e6914f5afe729` | 159,484 |
| 8x8/1if | `d67fd049a9d20b6522a635cb4aa7d6abc536e61ec036cc0c32485c64f69af0c4` | `c635596216d95671d9308f9f31b12db98c9f65747f5834b69f0df683756729b4` | 172,164 |

I read the comparison implementation and both complete comparison receipts. It compares every program header and segment's file bytes, then every SHF_ALLOC section by name, type, flags, VMA, LMA, length and actual byte equality. The receipts give both complete digests for .text, .rodata and .data. They also compare .bss and .stack metadata; these NOBITS sections have no file bytes and appropriately have no fabricated content digest.

The ROM comparison binds both links to the build's bank initialization: 31,608 words at 1x1, digest `1fd5bc472e531e73f1603208e5256625deb959bc06c6c976a9ab54a8228b6cfe`; 34,802 at 8x8, digest `ac014c6ab2c2dccac74d839d13a0444f3d5bafeb983a47d8af5f354c91f4ea78`.

Both manifests are now published with flashboot_layout.json, csr.csv and aem_desc.bin. Their actual content hashes match the existing artifact lists; each manifest's firmware hash/length matches its compared gating ELF. The product hashes match `receipts/step16/images/product-images.txt`. The full bitstream hashes agree across the artifact lists, bench list and comparison receipts:

- 1x1: `c7189218a128b71d632edc82157ea6f31b303383a6fe302d50265ad816332a28`, payload `4b00c4af97e56f66db63cfbed1b9bc4b0f7702da91fdfef373c5ff16847ba7b5`.
- 8x8: `7d90341299cc65e8c0da249139471a61019255132b66d5207ef9ffb4a5d0b773`, payload `88797768dbe54d39e254aa9b4daaf2d08ec60f355c248c1901b3a852a43a95df`.

The recorded payload recomputation matches each manifest, including FPGA part. Both identity-gate receipts pass.

The whole-file difference is accounted for: exactly 2,474 bytes at each point, all in nonloaded .symtab; section layouts agree. Both symbol tables contain the same 1,267 entries; 612 positions exchange same-address local/mapping symbols. No loaded section differs among the 43 input objects. `toolchains.txt` identifies the differing assembler/linker releases, 2.43.1 and 2.45.1, with GCC 14.3.0 at both. These receipts support the stated symbol-order explanation rather than merely assuming debug metadata caused the difference.

Independent execution: the published `verify_published.py` returns 0. Four disposable mutations independently return 1 with the expected named failure: manifest firmware hash, artifact-list bitstream hash, compared product hash, and manifest payload digest. `evidence-check.log` and the four plant logs record them. The original binary-level plants are also inspected: a flipped .rodata byte fails segments/loaded/not-loaded/ROM checks, and a zeroed bitstream digest fails the manifest check.

Limit: the original ELF/.bit files and object/build trees are not in this archive. The binary-level comparison and its two plants are inspected published executions; they were not freshly executed against absent binaries. The portable receipt verifier and four receipt mutations were freshly executed. This meets F1's requested public two-sided receipt without claiming a rebuild or new route.

## Step 14 timing remainder: resolved for the final source image

Authority: [R870-2's retained F2](https://github.com/kebag-logic/milan-fpga/pull/952#issuecomment-7014748818), FR_NFR.md 3.4.1, formal measurement completeness, and the public owner rulings preserved in `public-authority.txt`.

Step 14's merge `4b9f66c5` contains frozen #952 head `f09d82e0`. Both measurement heads, `92de01f7` and `8c5e2b4f`, descend from it. The final `8c5e2b4f..8dc85884` delta changes only SPLIT_CONTROL_MEMORY.md. Thus the measurements contain the changed hold-off instruction and its resulting layout; the pre-change sample is not used to clear the finding.

I checked CPU-TABLE-8c5e2b4f.md in full and the complete 8x8/1if section of CPU-TABLE-92de01f7.md against their survey receipts. `check_cpu.py` independently recomputes all 136 ordinary table rows using integer rounding of measured cycles plus 5%, upward to 5 us, and checks the separate long-notice and record-class results. Both points have 0/68 ordinary statements exceeded and no held record-class exceedance. Zero-valued inactive aggregate labels are not treated as executed paths: build_one, item.record and the separate long-notice evidence cover the active operations.

The inventories and execution logs supply 64/64 rc-zero parts at each point, including the recorded 8x8 resumptions: 241 groups at 1x1 and 240 at 8x8. They include initial Talker declarations, MAAP loss/hold initiation, held-Talker load, all eight declaration/withdrawal-notice phases, both answering variants and the declaring-output arm. Hold-off initialization and the affected SRP/Talker cost paths are therefore measured on code containing #952. Functional tests of the full nominal hold and latest-Leave behavior remain covered by the unchanged source tests and prior reviewed evidence; the short CPU cost windows are not claimed to be fresh 30-second hold-expiry tests.

The four 8x8/1if measurement-image hashes are identical through step15, `fb083864` and step16, and its consumed statements are unchanged. `cpu-check.log` records the full hashes. The 1x1 slice changed, so that point uses the complete new measurement, not an identity shortcut.

| Held acceptance at this head | Verified result |
|---|---|
| 1x1 every-source rows | R4 13.26/20; R5 73.88/90; R6 69.75/90; first notice 14.69/20 ms |
| 1x1 last notice / largest-command row | 127.31/130 ms, owner ceiling 140; R4L 203.48/238 ms |
| 1x1 protocol / transmit rows | ACMP 29.06/30; ADP 27.51/30; MAAP 27.61/30; tx 33.44/49; txL 47.88/49 ms |
| Load | 1x1 0.5114/0.70; 8x8/1if 0.7436/0.75 |
| 8x8/1if held transmit figure | 76.81 ms row covered by 77 ms, within the ruled 80 ms ceiling |
| SRP record cost | 1x1 24,662 cycles, 260/285 us; 8x8 34,803 cycles, 370/375 us |
| Reclaim cost | 1x1 1,767 cycles, 20/25 us; 8x8 995 cycles, 15/40 us |

Independent required-point flip checks and the load check return 0. The record-class self-test refuses 26/26 plants.

Existing limits remain explicit. At 8x8/1if, every-source rows are reported under #872, not held, by #665 comment 6972255348; their negative projected margins are not passes. Non-completing labelled records are reported by the unchanged record-class contract. The seven held-egress misses in each applicable backlog-owed leg remain misses under the accepted ledger. The 8x8 receipts also show four passes over the 2 ms share, two in each largest-notice-bearing arm; they retain the reported largest-command condition documented in SPLIT_CONTROL_MEMORY.md:3033,3150. There are zero refusals and zero of 388,313 passes over share at 1x1; 8x8 has four of 666,786, not zero. No blanket all-arms/all-bounds claim is made.

This closes the missing complete final-train-source measurement condition carried from R870-2. It neither manufactures a new R870 verdict nor supplies the manager's future current-dev candidate bank. Reuse at that turn requires demonstrated image identity; a changed candidate image requires the applicable remeasurement.

## Findings, residue and prior dispositions

**R866-5-R1 - RESIDUE - Docs - reviewer IDs in new helper comments.**
Artifacts: `receipts/step16/gating/loaded-identity/tools/loaded_identity.py:3`, `loaded_identity.sh:2`, `verify_published.py:3`.
Authority/evidence: the owner's source-comment rule forbids reviewer/round identifiers in newly added source commentary; these lines contain `R866-4-F1`.
Impact: explanatory wording only; no measurement, predicate, output verdict, clause claim or privacy rule changes.
Required exact fix: replace that token with `#665` in the shell/verifier headers; reduce `(#665; R866-4-F1)` to `(#665)` in loaded_identity.py. Keep the finding reference in the receipt README/handoff.
Verification: inspect a comment/docstring-only diff; retain identical executable behavior and receipt results.

The following previous residues are RETAINED. Their common authority is the owner's wording/comment convention; their impact is misleading or prohibited explanatory prose only. Verify each with a prose-only diff and unchanged executable predicates/constants.

| ID; severity; lenses | Artifact and evidence | Required exact outcome |
|---|---|---|
| R866-4-R1; RESIDUE; Docs | aecp_mbx.h:77; ctrl_loop.h:218,283,344; budget edit_rows.py:51, load_grade.py:219,273, notice_window.py:69, poll_grade.py:108, shape_costs.py:408,513, selftest_notice.py:115 still name the owner comment ID | Remove `issuecomment-7044585511` and redundant punctuation; retain #665, date, item 4 and behavior/reason |
| R866-4-R2; RESIDUE; Docs | PR-BODY.md opening and historical “final head”/pending paragraphs coexist with correct current Status | Say fourteen steps in the opening; label old final-head text as step-12 head 0839453f; remove or explicitly historicize the superseded sample/pending CPU paragraph |
| R866-1-R1; RESIDUE; Docs | test_plat_boot.cpp:91,95,116,119 remains unchanged | Remove B24, parenthetical PHY label list and L5/L6 prefixes from comments; preserve behavioral descriptions and tests |
| R866-1-R2 / R865-1-RES-2; RESIDUE; Docs | ctrl_split_hot.txt:14,19 still carries the two comment IDs | Remove the IDs; retain #665, dates, items and all ordered hot-list entries |
| R865-1-RES-1; RESIDUE; Docs | AREA_BUDGET.md:139,141 still describes the superseded current record/directive | Mark the record historical until the 2026-11-18 re-record; name ExtraTimingOpt as current, preserving historical figures and debt |
| R866-3-R1; RESIDUE; Docs | PR-BODY.md:472 still says the release comparison was last made at step 9 | Delete that obsolete sentence; preserve the later comparison's actual attribution |
| R871-2-R1; RESIDUE; Docs | declaring_outputs.py:296,323 retains `R872-1-F2` | Replace the docstring reference with #943; remove the reviewer possessive in the explanatory label |

R866-2-R1 remains RESOLVED: the current Status names the final head. R870-1-F1/F3 and its role/test-name residues remain resolved at their unchanged clause, layout and naming corrections. Step 13's R872-1-F1/F2 and R871-F1 remain resolved; this evidence delta changes none of their causes. Earlier PR #945 rounds have no other open blocking findings.

Retained optional suggestions, all nonblocking:

- **R869-1-SUG-1 - SUGGESTION - Conformance - srp_mbx.c:35-44.** The accepted nominal hold excludes two 15.5-second tolerance-edge intervals. Optional outcome: public retention of that policy or separately authorized tolerance-inclusive work. Verify policy disposition and, if changed, tests/image timing.
- **R869-1-SUG-2 - SUGGESTION - Docs - #951 conditional reference-device measurement.** No conflict-delay measurement is claimed. Optional outcome: record transfer or the decision to decline it before issue closure. Verify public disposition or a dated measurement.
- **R871-2-S1 - SUGGESTION - Tests - declaring_outputs.py:209-213.** A uniform address-base offset can escape this arm's check, while the product test pins the address. Optional outcome: derive the base from actual allocation; verify a shifted-base plant fails.
- **R871-2-S2 - SUGGESTION - Tests - declaring_outputs.py:188-199.** GET response values are decoded; SET responses are timed/counted through shared completion. Optional outcome: value-check SET responses too; verify a SET-only wrong-address/flags plant fails.

## Reviewer-owned coverage ledger

Each CLEAN result below applies the named lens to the evidence delta and retains unchanged R866-4 source coverage. Residue and optional suggestions do not unclean a lens.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #665/#894/#951 rulings; srp_mbx.c:32-46; both complete point CPU tables, survey/part receipts; local flip/load results | R866-5, unchanged source coverage from R866-4 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| RTL | CLEAN | Unchanged source/tree/gitlinks; loaded_identity.py ELF segments, allocation and ROM comparisons; manifests, layouts and identity receipts | R866-5 delta; R866-4 unchanged architecture coverage | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Robustness | CLEAN | Published byte-flip/digest controls; four independently rejected receipt mutations; unchanged hold/reset/latest-Leave test dependencies | R866-5 delta; R866-4 unchanged source coverage | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Tests | CLEAN | check_evidence.py/log; check_cpu.py/log; both comparison receipts; 128 part exits; image carry; record-controls.log; F1 and step14 F2 reconciliation | R866-5 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |
| Docs | CLEAN | HANDOFF-r5.md/PR-BODY.md delta; loaded-identity README/toolchains; manifest inventory; explicit prior residue dispositions | R866-5 | 8dc8588471a096bbe120bbec4c8c0f8ddf44d8cd |

## Reproduction and real limits

Extract only author-r6, author-r7 and MANIFEST.json from archive 9faf6fa8 beneath the packet's scratch directory. Run:

```sh
python3 -B check_evidence.py ARCHIVE_ROOT PACKET_DIR
python3 -B check_cpu.py ARCHIVE_ROOT/author-r7
python3 -B verify_checkout.py CHECKOUT
```

The additional executed commands are the two point-specific `flip_grade.py --check` calls, `load_grade.py --check`, `record_classes.py --selftest`, and `git diff --check cb96336d..HEAD`. All return 0. Raw results and expected nonzero plant receipts are listed in MANIFEST.sha256. All processes completed in the foreground. No full source banks, fresh synthesis/routes, simulator builds or hardware probes were run.

Checkout verification checks actual blob bytes, executable modes and the complete index, not status alone: all 1,941 candidate entries and all five required submodules pass. Pins remain gPTP `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, protocol processor `801ef2283ec793e35a2590fc6593c90313a64041`, lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`, TSN stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, and axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Optional external is uninitialized and unused. No candidate edit needed restoration.

Source gate evidence remains the author's published receipts. No manager source-head bank exists or is inferred. Some original large logs are digest/tail stubs; their omitted traces were not independently inspected. Physical calibration is NOT RUN. Field skips, model runs and earlier-image hardware observations are not final-head hardware proof.

Pending manager duties: publish this review and carry residue/optional dispositions; complete the independent review bar; build and validate the actual current-dev merge candidate with the required builder/native banks and link receipts. The source base cb96336d and supplied live dev e275d7950ef3385753e6a15d2e191ba855b171ed do not identify that future candidate. Accept hosted/local-replica evidence with executed and skipped jobs distinguished. Complete final-image physical obligations, obtain explicit merge authorization, prove post-merge containment, and then close/move the issues under the public contract. This review does not authorize merge.

No source fixes, commits, pushes, GitHub writes, author contact, delegated work, container orchestration or hardware actions occurred.

R866-5 FINISHED
