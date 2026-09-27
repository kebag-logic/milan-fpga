[R353] POSITIVE - exact head 01e18f6c4d01a545e8d927ac119187c9514dc40c

Round R353-2: external independent delta review of PR #591 for issue #580.

- **Head:** `01e18f6c4d01a545e8d927ac119187c9514dc40c`, tree `17de168ce12a5af81ba8a0f9d795290e071e7948`.
- **Parents:** `d02db63c367daf9adc7d709840bd81077e781d80` (lane) and `2a2a7bb655e528edc3087c88033cd3a47546feb4` (dev). The merge base is `682ecf0cb995473b72d5b4921088053ba753fc93`.
- **Delta covered:** `499b15f9..01e18f6c`. Round R353-1 was POSITIVE at `499b15f9`.
  - Round 2 at `d02db63c`: the capture re-measure and the documentation corrections.
  - Merge commit `01e18f6c`: dev `2a2a7bb6` (which carries #573/PR #585 and #587/PR #589), with the resolution of `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`.

All five lenses were applied at this head, and all five are CLEAN. There is no BLOCKER, MAJOR or MINOR finding. Two SUGGESTIONs (S1, S2) are recorded; they do not affect coverage. Receipts are named `receipts/<name>` below and listed in `MANIFEST.sha256`. In the receipts, `$CLONE` is the review clone, `$PACKET` is this packet directory, and `$MD_PYTHON` is the existing pinned Markdown interpreter.

## Reconstruction

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md (by reference from AGENTS.md).
2. The issue #580 body and all public comments:
   - the [A10] scope comments 5854203161, 5854653164 and 5854987837;
   - the assignment 5856274975;
   - the round-2 decision 5857045698 (re-measure; this corrects assignment item 4);
   - the merge-dev assignment 5857846388, including its resolution rule;
   - the executor TAKEN and REVIEW READY comments for rounds A366, A368 and A372.
3. Linked authorities:
   - `tb/verilator/nvm_capture_cpu/README.md`, `scripts/check_nvm_capture.py`, `recipe.py` and `run.py`;
   - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18;
   - processor #122 comment 5853884588 (read-only);
   - parent issue #584 (read-only);
   - the processor diff `0922e434..16be6768 -- hdl/`.
4. The diffs `499b15f9..d02db63c`, `682ecf0c..d02db63c`, `682ecf0c..2a2a7bb6`, `2a2a7bb6..01e18f6c` and `d02db63c..01e18f6c`.
5. The public evidence tree `147cb4b8:review-evidence/580-r1`. I used its `new-artifacts.json` as the reference table.

I read no private author material or lane scratchpad. I read prior public review reports only after the verdict and ledger were written; see the last section.

## Delta verification

### Part 1: round-2 re-measure (`d02db63c`)

| # | Check | Result | Receipt |
|---|---|---|---|
| 1a | `check_nvm_capture.py` at the head | PASS, rc 0. All seven built-in controls were detected. The four named `--mutation` runs (`bytes`, `records`, `clock`, `ignore-off-timing`) each gave rc 1. | `capture-check-head.log`, `capture-mutation-*.log` |
| 1b | Receipt rows recomputed with my own script, independent of `run.py`'s grader | PASS on every point below. | `receipt-audit.log` |
|  | Arm and row structure | 6 distinct arms, 16 rows each (indices 0..15). Every row has `ok=1`, `mismatches=0` and `open=0`. | |
|  | Census | 8x8 is 12634 B / 156 records; 1x1 is 3218 B / 53 records. | |
|  | Traffic counters | Every ON row has positive request, response and read counts. Every OFF row has zero. | |
|  | Maxima and margins | Recomputed exactly with rational arithmetic: 1x1 6.60642 ms (7.417028x); 8x8 at 50 MHz 24.30246 ms (2.016257x); 8x8 at 100 MHz 19.79024 ms (2.475968x). All equal the published values. | |
| 1c | 8x8 margin to the 24.5 ms bar | The 50 MHz contract maximum is 2,430,246 ticks at 100 MHz = 24.30246 ms. That is 0.19754 ms below 24.5 ms, so the STOP condition does not apply. Section 18 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1611-1630`) matches on every row. I recomputed the six per-arm floor ratios in its table (7.4170, 7.4371, 2.0163, 2.0197, 2.5784, 2.4760) from the rows. | `receipt-audit.log` |
| 1d | `processor_pins` against the measured tree | PASS on every point below. | `receipt-audit.log` |
|  | Base and tree | `base` `499b15f9` has tree `83b988d3`, which equals the receipt's `tree` (`measurements.json:3,310`). | |
|  | Pins | For `protocol-processor` `16be6768`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e`, the recorded pin equals the base gitlink and the head gitlink. | |
|  | Ancestry | `base` is an ancestor of the head. | |
| 1e | The measured product at `499b15f9` equals the head's product | PASS on every point below. | `delta-paths.txt`, `builder-outputs-*.json`, `compare-r1-head.log`, `capture-check-head.log` |
|  | Measured-path files | `499b15f9..01e18f6c` changes no file under `hdl/`, `sw/firmware/`, `sw/litex/`, `configs/` or the harness, and no gitlink. The only harness-directory change is `measurements.json` itself. | |
|  | Builder delta | The builder delta (`sw/builder/endstation_builder.py`, `avdecc/aem_descriptors.py`, from #573) adds refusal-only validators: `_model_id`, `_stream_buffer_ns`, `_validate_stream_formats`, `_crf_format` and `_validate_output_clock_sources`. | |
|  | Generated outputs | All 65 generated artifacts over the five configurations are byte-identical between `d02db63c` and the head. They include `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_*.svh`, `gptp_ucode.hex`, `soc_params.json` and the AEM image/map/JSON. All 65 equal the public round-1 table at pin `16be6768`. | |
|  | Firmware and harness | The firmware and harness hashes are gate-checked in 1a. | |
| 1f | The processor RTL change behind the re-measure | `0922e434..16be6768 -- hdl/` adds only the `name_wr_o` output (the same enable that already wrote the name lane) and the packer's body/key refusal. That is consistent with the cycle-identical rows the executor reported. I did not re-simulate (see limits). | processor diff (read) |
| 1g | Round-2 text changes | PASS on every point below. | diff read; focused docs gates |
|  | Changelog and submodule text | `CHANGELOG.md:36-49` and `SUBMODULES.md:64-70` state the re-measure, the #122 disposition and #584 ownership. | |
|  | Authorities | The #122 comment 5853884588 retains F07.2 `1..*` under Milan v1.2 §5.3.3.8. #584 is open and owns the D8 correction. The text matches both. | |
|  | Removed overclaim | The round-1 "Measured inputs remain unchanged" overclaim is gone. | |

### Part 2: merge commit (`01e18f6c`)

| # | Check | Result | Receipt |
|---|---|---|---|
| 2a | The merge is a clean union over all 932 tree entries (blob, mode and gitlink) | PASS. Every path equals the side that changed it relative to `682ecf0c`. The lane changed 13 paths and dev changed 11. The only path both sides changed differently is `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`. The control (lane head passed as the "merge") fails with 10 unclean paths, rc 1. | `merge-union.log`, `control-merge-union-lane-as-merge.log` |
| 2b | `git diff 2a2a7bb6 01e18f6c` equals #580's own changes | PASS. The `--stat` equals `git diff 682ecf0c d02db63c` line for line: 13 files, +89/-34. The patch texts are identical apart from index lines, except the conflict file. Its only differences are dev's own lines present as context, and shifted hunk offsets. | `lane-own-stat.txt`, `merge-vs-dev-stat.txt`, `lane-vs-merge-patch-diff.txt` |
| 2c | Resolution keeps every fact from both sides and adds no new claim | PASS, detailed in the next table. | `resolution-lines.log`, `control-resolution-lines-dev-as-merge.log` |
| 2d | Gitlink | `HEAD:protocol-processor` is `16be6768f710e79450aace277abacd6c2c3336e5`, which contains `493e5e4b`. The gptp-processor and verilog-axis gitlinks are unchanged. | `clone-integrity.log`, `receipt-audit.log` |
| 2e | `syn/yosys/rom_digests.tsv` against the merged tree | PASS on every point below. | `rom-ledger.log` |
|  | Regenerated images | I regenerated `ltn_rom.hex`, `ucode.hex` and `gptp_ucode.hex` from the checked-out pinned submodules, after verifying each checkout equals its gitlink. Each sha256 equals exactly one ledger row at its pin. | |
|  | Old rows | The `870ff88a` rows are retained with identical digests. | |
|  | Merge effect | Dev did not touch the ledger (2a). | |
| 2f | Focused gates at the head | Every gate below returned rc 0. | named receipts |
|  | Builder and evidence checks | `sw/builder/test_declarations.py`; `measure_test_evidence.py --check`; `check_port_contracts.py`. | |
|  | Docs checks | `docs_check.py`, `check_doc_style.py`, `check_submodule_docs.py`, `check_doc_paths.py`, `check_diagram_pngs.py`, `DOC_MAP.gen.py --check` and `submodule_boundaries.gen.py --check`. | |
|  | TOC and em-dash checks | `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py` against dev `2a2a7bb6` and against source base `682ecf0c`. | |
|  | Whitespace | `git diff --check` against dev and against the lane head. | |

#### Resolution detail (2c)

The line-level three-way audit found:

- no merge line present on neither side;
- 21 lane lines and 7 dev lines absent from the merge. Each of them was removed or replaced by the other side relative to the base. The one exception is the adjudicated line below;
- one adjudicated conflict line. Dev's "The original processor pin was `990f9652…`" is replaced by the lane's "The audit's processor pin was `990f9652…`". The merge-dev assignment rule directed exactly this. The pin value and dev's "original" framing survive at `:4` ("Original measurements were recorded at `7eb3b0d4…`").

The control (dev tip passed as the "merge") reports 14 dropped lines and fails with rc 1.

Each element of the assignment rule, checked at the head:

| Element | At head | Origin |
|---|---|---|
| #573 original-measurement framing | `PP_DESCRIPTOR_OWNERSHIP.md:4` | dev, verbatim |
| #573 F1-F4 enforcement sentence | `:6` | dev, verbatim |
| #580 audit-pin wording | `:5` | lane, verbatim |
| #573 enforced F1-F4 rows (#573-#576) | `:251-254` | dev, verbatim |
| #573 L4/L6/L9 rows, u32 pack sentences, probe tables, identity text, follow-up intro | `:38-39, :64, :66, :69, :170, :180-206, :245-246` | dev, verbatim |
| #580 F5 disposition row (processor #122 retains the minimum; parent #584 owns the D8 correction) | `:255` | lane, verbatim |
| #580 F7 row (enforced at `493e5e4b`, adopted through `16be6768`) | `:257` | lane, verbatim |
| #580 L1/L2 rows, cluster paragraph, audit-pin probe note, link definitions | `:61-62, :137-142, :173-174, :311-312` | lane, verbatim |
| F6, F8 and the rows below them | `:256, :258-261` | unchanged on both sides |

Nothing the merge introduced contradicts the text around it:

- The dev L4 probe row (`:170`, "47-entry size 514 … All accepted") is qualified by the lane note `:173` ("These probe results describe the recorded audit pin").
- The F-row cross-references `[F5]`, `[F7]` and `[F2/F3]` resolve to the merged table.
- The inherited `:186` 47-entry vs audit-script 48-entry mismatch exists on dev and is tracked on #495. Per the assignment, it is not a finding for this PR.

## Findings

### S1 - SUGGESTION - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:9-10, :81, :300-301` - two remaining present-tense references to the audit-time processor state

- **Authority/evidence.**
  - `:9-10` still says "Processor contract publication follows independent review in a separate change. No ownership transfer relies on that unpublished processor change." That publication is processor PR 126. This PR adopts it through `16be6768` (`SUBMODULES.md:67`, `CHANGELOG.md:40`).
  - `:81` names source `P` as the "pinned processor packer". Its `[packer]` link (`:301`) and `[memory-map]` link (`:300`) point at `990f9652`, which `:5` now calls the audit's pin. The current pin's packer adds the body/key refusal cited at `:62` and `:257`.
  - Both passages predate this delta. The merge left them unchanged, and the merge-dev assignment says to report such text, not rewrite it.
- **Impact.** A reader may take `990f9652` as the current packer, or processor ownership publication as still pending. Neither misstatement changes a rule allocation.
- **Suggested outcome (optional).** Use past tense or "audit-pin" wording at `:9-10` and `:81`, or leave it to the next edit of this page (for example #584's item 2).
- **Verification.** Read the text.

### S2 - SUGGESTION - Tests, Robustness, Docs - `scripts/check_nvm_capture.py:58-94`, `tb/verilator/nvm_capture_cpu/README.md:156` - the hosted capture gate does not bind the new provenance fields

- **Authority/evidence.** `check_receipt` reads `measured_for`, the firmware hash, the harness hashes, the arms and the maxima. It never reads `base`, `tree` or `processor_pins`. My probes on a disposable export of the head (`capture-probes.log`) show two things:
  - A bogus `processor_pins.protocol-processor`, and bogus `base` and `tree`, each still give PASS, rc 0.
  - A row above 24.5 ms, a row at exactly 24.5 ms with a stale summary, an edited maximum and a dropped OFF row each fail, rc 1.
  - README:156 ("Harness hashes prevent carrying evidence across measurement-path changes") is broader than what the gate enforces. The measured path includes parent and processor RTL, which no hash covers.
- **Impact.** A future pin or RTL bump could again carry timing across a changed measured product without a gate objecting. That is how round 1's provenance problem arose. It does not affect this head: 1d/1e above show the receipt describes the measured tree, and that tree's product equals the head's.
- **Suggested outcome (optional, separate Issue; outside #580's frozen scope).** Either compare `processor_pins` (and the base-tree relation) with the gitlinks in the gate, or narrow README:156 to what is enforced.
- **Verification.** The `processor-pins-bogus` probe fails the gate, or the README states the limit.

## Clean-lens results

```text
[R353] PASS Conformance - receipts/receipt-audit.log, merge-union.log, resolution-lines.log, rom-ledger.log, compare-r1-head.log; tb/verilator/nvm_capture_cpu/measurements.json:3,284-320; docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:4-6,61-62,251-257 - round-2 decision items (six arms x16 at the pin, receipt base/tree/pins, section 18, changelog, STOP bar) and the merge-dev resolution rule checked item by item against issue #580 comments 5857045698 and 5857846388; 8x8 24.30246 ms <= 24.5 ms; gitlink 16be6768; ROM ledger consistent with the merged tree.
[R353] PASS RTL - receipts/delta-paths.txt, rom-ledger.log, builder-outputs-head.json vs builder-outputs-d02db63c.json - delta 499b15f9..01e18f6c touches no hdl/, firmware, LiteX, config or gitlink path; the 65 generated artifacts including every generated .svh are byte-identical across the merge; regenerated ROM images match their ledger rows at 16be6768/5dce647a; processor hdl diff 0922e434..16be6768 read (name_wr_o output only, refusal in the Python packer).
[R353] PASS Robustness - receipts/capture-probes.log, capture-mutation-{bytes,records,clock,ignore-off-timing}.log, control-*.log - gate refuses over-bar, at-bar-stale-summary, edited-maximum and dropped-row receipts and all four named mutations; the builder delta is refusal-only and leaves shipping outputs unchanged; provenance non-binding recorded as S2 (SUGGESTION).
[R353] PASS Tests - receipts/capture-check-head.log, test-declarations.log, test-evidence-check.log, port-contracts.log, control-merge-union-lane-as-merge.log, control-resolution-lines-dev-as-merge.log - checker controls fire; merged declaration tests rc 0; evidence and port ratchets rc 0; each reviewer audit script is shown able to fail on a planted wrong merge.
[R353] PASS Docs - docs/reference/PP_DESCRIPTOR_OWNERSHIP.md (full merged text, 312 lines), docs/reference/SUBMODULES.md:64-70, CHANGELOG.md:36-49, docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591-1630; receipts/docs-check.log, doc-style.log, submodule-docs.log, doc-paths.log, diagram-pngs.log, doc-map-check.log, boundaries-diagram-check.log, gen-toc-*.log, em-dash-*.log, diff-check-*.log - every claim checked against processor #122 comment 5853884588, issue #584 and the receipt; merged text internally consistent; S1 (SUGGESTION) only.
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #580 decisions 5857045698 and 5857846388 against `measurements.json`, section 18, CHANGELOG, the merged ownership page, the gitlink and the ROM ledger; `receipt-audit`, `merge-union`, `resolution-lines`, `rom-ledger`, `compare-r1-head` | R353-2 | `01e18f6c4d01a545e8d927ac119187c9514dc40c` |
| RTL | CLEAN | `delta-paths.txt` (no RTL or gitlink change); 65 generated artifacts, `.svh` included, identical across the merge; ROM regeneration at `16be6768`/`5dce647a`; processor `hdl/` diff `0922e434..16be6768` | R353-2 | `01e18f6c4d01a545e8d927ac119187c9514dc40c` |
| Robustness | CLEAN (S2 SUGGESTION) | `capture-probes`, four named capture mutations, script controls, refusal-only builder delta | R353-2 | `01e18f6c4d01a545e8d927ac119187c9514dc40c` |
| Tests | CLEAN (S2 SUGGESTION) | `check_nvm_capture.py` plus its controls; `test_declarations.py`; `measure_test_evidence.py --check`; `check_port_contracts.py`; negative controls for each audit script | R353-2 | `01e18f6c4d01a545e8d927ac119187c9514dc40c` |
| Docs | CLEAN (S1, S2 SUGGESTION) | Full merged `PP_DESCRIPTOR_OWNERSHIP.md`; `SUBMODULES.md:64-70`; `CHANGELOG.md:36-49`; section 18; the linked authorities; focused docs gates | R353-2 | `01e18f6c4d01a545e8d927ac119187c9514dc40c` |

## Prior public review findings (read after the verdict and ledger above)

A draft REPORT.md holding this verdict and ledger was written before any prior report was read.

One disclosure: a first attempt to write that draft failed, and a search issued in parallel with it displayed two lines of R352-1. Those lines were its verdict line (already visible in the comment list) and a bare "Impact." header. No finding content was displayed before the draft existed.

| Prior finding | Head it was raised at | Disposition at `01e18f6c` | Evidence |
|---|---|---|---|
| R352-1 F1 (MINOR; Tests, Docs): the receipt recorded a pin it was not measured with | `499b15f9` | **Resolved.** The maintainer chose re-measure. `base` `499b15f9`, `tree` `83b988d3` and `processor_pins` describe one tree, which equals the head's product on the measured path. CHANGELOG `:46-49` states the re-measure, and the overclaim is removed. | 1b-1e |
| R352-1 S1 (SUGGESTION; Docs): `PP_DESCRIPTOR_OWNERSHIP.md:5` audit pin read as current | `499b15f9` | **Resolved.** `:5` now reads "The audit's processor pin was", and it survives the merge verbatim. Two similar residual references are raised as my S1. | 2c |
| R352-1 S2 (SUGGESTION; Docs): processor PR 124/126 unlinked | `499b15f9` | **Resolved.** `SUBMODULES.md:66-67` links both to the processor repository. | diff read |
| R353-1 S1 (SUGGESTION; Docs, Tests): `processor_pins` described a different tree from `base` | `499b15f9` | **Resolved.** Same subject as R352-1 F1. `measurements.json:320` now defines the three fields. | 1d |
| R353-1 S2 (SUGGESTION; Docs): cluster-minimum wording beside the adopted disposition | `499b15f9` | **Resolved.** `SUBMODULES.md:68-70`, `CHANGELOG.md:41-43` and `PP_DESCRIPTOR_OWNERSHIP.md:61,138-142,255` state the violation and #584 ownership. The "must disposition it under PP60" text is removed. | diff read; 2c |
| R352-2 S1 (SUGGESTION; Tests, Docs): the hosted capture gate cannot detect provenance drift | `d02db63c` | **Retained.** It is unchanged at this head. I found it independently, and it is my S2. | `capture-probes.log` |
| R352-2 S2 (SUGGESTION; Docs): `tb/verilator/milan_dp/README.md:570` "The adopted pin `0922e434`" reads as current | `d02db63c` | **Retained.** The line is unchanged at this head and is not in the delta. Optional. | read at head |

No prior finding changes the verdict above. There are no inline review comments on the PR.

## Real limits

- **No capture re-simulation.** This host has no product LiteX environment or cached CPU netlist, and installing or downloading one is outside scope. The re-measure is therefore checked through:
  - provenance (1d);
  - measured-path invariance (1e);
  - recomputation of all 96 rows (1b);
  - gate behaviour (1a, S2);
  - the processor RTL diff (1f).

  The cycle counts themselves rest on the executor's run and on the internal round's partial reproduction at `d02db63c`. That reproduction is public (R352-2 point 2), and I read it only after my verdict.
- **Simulator not used.** The assigned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. No probe needed a simulator, so none was used. RTL coverage rests on the absence of any RTL or gitlink delta, not on a new simulation.
- **Banks not run.** I did not run the full parent/PP/gPTP/Yosys/builder banks, `ooc.sh` (it invokes synthesis), act, the host CI runner or its self-test. The ROM ledger was checked by regenerating the three images with the pinned generators, not through `ooc.sh`.
- **Markdown interpreter.** The Markdown gates used an existing pinned interpreter, read-only. Nothing was installed.
- **Probe trees.** The probes ran on disposable exports under `scratch/`, which is unpublished. They were turned into throwaway repositories because the builder requires `git ls-files`. Nothing in the review clone was modified.
- **Hosted snapshot.** At 2026-09-27T17:12:23Z, exact head `01e18f6c` had 10 completed/success, 1 skipped (the physical gPTP nightly/manual context, which is not executed coverage) and 8 in progress: docs-check, elaborate, yosys-elaboration and Verilator shards 0-4 (`hosted-check-runs.tsv`). That is not final hosted evidence.
- **No hardware evidence.** Physical calibration was NOT RUN, field skips are not hardware proof, and no hardware was used. Capture numbers are CPU simulation evidence only.

## Clone restoration

`clone-integrity.log`, taken after all probes:

- HEAD is `01e18f6c`, tree `17de168c`, and the index tree equals the HEAD tree.
- Worktree and index both equal HEAD.
- All 928 tracked non-gitlink blobs re-hash to their index ids, with no mode mismatch and no assume-unchanged or skip-worktree flags.
- There are no untracked or ignored files.
- The gitlinks `protocol-processor` `16be6768`, `gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` equal their clean checkouts. `external` `efeb541a` is uninitialised, as at start.

## Pending manager duties

- Hosted exact-head acceptance: 8 contexts were still running at snapshot. The act replica is the manager's.
- The final current-dev candidate at the merge turn (source base `682ecf0c`, live dev `2a2a7bb6` at review time), and post-merge containment.
- Optionally, file S2 as a separate Issue. S1 and R352-2 S2 can ride a later docs change.
- The merge still requires two independent positive reviews at a head covering every lens, the full completion bar and explicit maintainer authorization.

R353-2 FINISHED
