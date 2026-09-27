[R352] NEGATIVE - exact head 499b15f97eb0a469b7cd1308fbba7af3c64d1851

Round R352-1, internal independent review of PR #591 for issue #580.
Head `499b15f97eb0a469b7cd1308fbba7af3c64d1851`, tree `83b988d3b59a398a7d0cd1977194c50be92522da`, one commit on dev `682ecf0cb995473b72d5b4921088053ba753fc93`.
All five lenses were applied. Three are clean. One MINOR finding (F1) leaves `Tests` and `Docs` unclean, so the verdict is NEGATIVE.
The pin adoption itself (gitlink, ROM ledger, diagram, disposition, F7 wording, five-configuration equality) reproduces exactly. The defect is limited to the capture receipt's provenance field.

## Reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md (sections 2.1 and 2.2, submodule and verification rules), docs/README.md, the issue #580 body, the three [A10] scope comments (5854203161, 5854653164, 5854987837), the assignment 5856274975, the [A366] TAKEN and REVIEW READY comments, REQUIREMENTS.md REQ-VER-03/04, docs/reference/SUBMODULES.md, docs/reference/PP_DESCRIPTOR_OWNERSHIP.md, docs/DOC_GENERATION.md, tb/verilator/nvm_capture_cpu/README.md and scripts/check_nvm_capture.py. Then the diff `682ecf0c..499b15f9`, the processor history `870ff88a..16be6768`, and the public evidence tree `147cb4b8:review-evidence/580-r1`.
Prior public review findings on PR #591: none exist. At review time the PR had no inline comments, no reviews and only the two review-start comments. Nothing needs to be resolved or retained.

## Assigned verification points

| # | Point | Result | Receipt |
|---|---|---|---|
| 1 | Gitlink is `16be6768`; ledger rows re-recorded by the tool, keyed by pin, older rows kept; digest check passes | PASS. Index record `160000 16be6768f710e79450aace277abacd6c2c3336e5 0`. `ooc.sh --record-rom-digests` rewrites `syn/yosys/rom_digests.tsv` to byte-identical content (`git diff --exit-code` rc 0), and the diff has 0 deleted rows. `ooc.sh KL_chan_map_render` rc 0. Planted probes: removing the 16be6768 rows gives FATAL rc 2 (no recorded digest). A one-digit ucode digest change gives FATAL rc 2 (mismatch). | 02, 03, 04, 13 |
| 2 | SUBMODULES.md, pin text, diagram, PNG_MANIFEST.json (tool-generated), CHANGELOG describe 16be6768 | PASS. Running `submodule_boundaries.gen.py` in place changes nothing: drawio, svg, png and PNG_MANIFEST.json stay byte-identical. So the committed manifest equals tool output. `--check` and `--selftest` rc 0. `check_diagram_pngs.py` rc 0. I inspected the rendered PNG visually: pin `16be6768f710`, all labels and connectors present. SUBMODULES.md:25 and :64-69, SAVED_STATE_MATERIALIZATION.md:232-233 and CHANGELOG.md:36-45 name 16be6768. | 05, 15 |
| 3 | DUT_READER_DISPOSITIONS entry present with the reviewed text; `measure_test_evidence.py --check` passes | PASS. `scripts/measure_test_evidence.py:597-599` matches the assignment text exactly (AST comparison). `--check` rc 0 (0 <= 0 unexplained readers). Removing the entry gives rc 1, with the file reported `UNEXPLAINED`. I read the test (`protocol-processor/tb/desc_store/test_gen_desc_image.py:14-18,57-65,79-84,100-107`): it imports the generator by path, drives `build()` and the CLI on synthetic models, and reads back only its own outputs. The disposition is accurate. | 06 |
| 4 | PP_DESCRIPTOR_OWNERSHIP.md F7 rows state packer enforcement from 493e5e4b | PASS. `:59` (L2 row), `:168-169` (probe note) and `:245` (F7 row) state the refusal is enforced by the processor packer at `493e5e4b`, adopted through `16be6768`. The pinned packer refuses at `protocol-processor/hdl/aecp/desc/gen_desc_image.py:216-222`, after a 4-byte minimum at `:192-193`. Pinned test: 6 tests OK. A mutant with the refusal disabled fails 16 subtests. | 07 |
| 5 | measurements.json: only the recorded processor pin changed; checker never reads it | PASS as stated. The diff is one line (`measurements.json:304`). `check_nvm_capture.py` has no reference to `processor_pins` (grep rc 1). It reads `measured_for`, `product_firmware_sha256`, `harness_sha256`, `measurements` and `maxima` (`:58-94`). Head receipt rc 0. Planted all-zero processor pin: rc 0. Deleting `processor_pins`: rc 0. Planted firmware digest: rc 1 (`product firmware changed`). See F1 for what this implies about the field. | 10, 11 |
| 6 | Five configurations: AEM images and builder outputs byte-identical 870ff88a vs 16be6768 | PASS for all five, not just two. 65 files per pin (10 builder outputs plus aem.bin/map/json per configuration). Every name and sha256 is equal. All 65 sizes and digests equal the published REVIEW READY tables. Shipping images are packed by the processor packer (`avdecc/gen_aemi_image.py:80`, `sw/builder/endstation_builder.py:2240`), so all shipping bodies satisfy the new body/key refusal. | 08, 09 |
| 7 | pp_shadow and milan_dp default suites, check_port_contracts, docs gates pass; no RTL or firmware change | PASS. pp_shadow rc 0: 4 legs, 591+591+591+295 = 2,068 checks, 0 failures. milan_dp rc 0: 14 builds, all on Verilator 5.050, 0 `[FAIL]` lines, including render and grandmaster-step campaigns. `check_port_contracts.py` rc 0. The docs gate set is rc 0: docs_check, em-dash against base, doc style, gPTP docs, DOC_MAP, timesync, solution docs, submodule docs, diagram PNGs, feature status, module matrix, TOC check/selftest/anchors, doc paths, archive, bare-metal-only, `git diff --check`. The parent diff touches no `hdl/`, `sw/firmware`, `sw/litex`, `.sv/.v/.c/.h` path. Processor `870ff88a..16be6768` changes no HDL except the Python packer generator. | 13, 14, 15, 16 |

## Findings

### F1 - MINOR - Tests, Docs - `tb/verilator/nvm_capture_cpu/measurements.json:304` - capture receipt now records a processor pin it was never measured with

- **Authority/evidence.**
  - The measured SoC includes processor and parent RTL. `tb/verilator/nvm_capture_cpu/soc.py:24,62` subclasses `milan_soc.MilanSoC`, which instantiates `milan_datapath` and `KL_pp_shadow` (`sw/litex/milan_soc.py:499,528`). The traffic-ON arm drives AEM READ_DESCRIPTOR through the processor and counts its descriptor-memory reads (README:107-113).
  - README:136 says the receipt "identifies simulator version and input hashes".
  - `processor_pins` was introduced in 054e59b41 alongside that commit's re-measure. It recorded `0922e434`, the gitlink of both the receipt `base` (`831f94f4`) and 054e59b41.
  - At this head the receipt still says `base 831f94f4` (gitlink `0922e434`) but `processor_pins.protocol-processor = 16be6768`. The receipt now contradicts itself.
  - Between the measured and recorded pins, processor HDL changed: `KL_aecp_desc_store.sv`, `KL_aecp_engine.sv`, `protocol_processor_top.sv`, +25/-2. Since the receipt base, parent RTL on the measured path also changed: `KL_pp_shadow.sv`, `milan_datapath.sv`, `KL_nvm_backend.sv`, `milan_csr.sv`.
  - CHANGELOG.md:45 "Measured inputs remain unchanged" is true only of the checker's census and clock inputs.
  - Receipt 11 holds the full evidence.
- **Impact.**
  - A reader, or any future gate that reads this field, will conclude the published 8x8 maximum (24.30246 ms, against the 24.5 ms limit) was measured with the adopted processor. It was measured with `0922e434` and older parent RTL.
  - The checker cannot catch this (point 5 above), so no gate protects the field's meaning.
  - This turns a truthful stale record into a false current-looking one.
- **Scope conflict to publish.**
  - The assignment item 4 says "Refresh the recorded pin", and the executor did so literally. So the acceptance criterion is met, and the finding is not filed under `Conformance`.
  - Its re-measure condition was framed on the checker alone. The harness does take the processor RTL as a measured input.
  - Under AGENTS.md section 2 this conflict needs a recorded decision, not a private interpretation.
- **Required outcome.** The receipt's recorded pins must match what was measured. Any of these satisfies it:
  - re-measure per README at a base whose gitlink is `16be6768`, with the issue's 24.5 ms STOP rule; or
  - restore the measured-with pin and state separately (a distinctly named field or a README/CHANGELOG line) that the adopted pin postdates the measurement and which RTL changed since; or
  - another maintainer-recorded disposition.
- **Verification.** `git rev-parse <receipt base>:protocol-processor` equals `processor_pins.protocol-processor`, or a new measurement exists at the adopted pin. CHANGELOG wording matches whichever was chosen.

### S1 - SUGGESTION - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:5` - audit pin reads as current

"The processor pin is `990f9652...`" is in the present tense. The same page now cites `16be6768` adoption (`:245`). Line 168 disambiguates the probes only. Consider "The audit's processor pin was ...". The line predates this diff. Optional.

### S2 - SUGGESTION - Docs - `docs/reference/SUBMODULES.md:66-67` - processor PR references unlinked

"PR 124" and "PR 126" are processor-repository PRs. They are unlinked, and the parent repository has its own #124/#126. The #508 table on the same page links processor PRs. The #502 lines follow the same unlinked precedent. Optional.

Observation, not a finding against this diff: `ooc.sh --record-rom-digests` installs the ledger through `mktemp`, leaving the worktree file at mode 0600. Git records only the exec bit, so tracked state is unaffected. I restored the mode to 0644.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #580 body and the 4 [A10] comments against: gitlink index record; `syn/yosys/rom_digests.tsv:13-14` (re-recorded by tool, 0 deletions); SUBMODULES.md:25,64-73; diagram/manifest regeneration; `measure_test_evidence.py:597-599`; PP_DESCRIPTOR_OWNERSHIP.md:59,168-169,245; `measurements.json:304` plus `check_nvm_capture.py:32-94`; 5x13 artifact sha256 at both pins (receipts 02-13) | R352-1 | 499b15f97eb0a469b7cd1308fbba7af3c64d1851 |
| RTL | CLEAN | Parent diff has no RTL/firmware/CSR path (receipt 13); processor `870ff88a..16be6768` changes only `hdl/aecp/desc/gen_desc_image.py:28-40,216-222` in `hdl/`; ROM images identical (ooc digests equal 870ff88a rows); `ooc.sh KL_chan_map_render` rc 0; pp_shadow 2,068 checks and milan_dp 14 builds on Verilator 5.050 (receipts 03, 14) | R352-1 | 499b15f97eb0a469b7cd1308fbba7af3c64d1851 |
| Robustness | CLEAN | Planted ledger faults refused, rc 2 x2 (receipt 04); capture checker firmware fault refused, pin fault ignored as documented (receipt 10); disposition removal refused (receipt 06); packer refusal mutant fails 16 subtests, short body refused before comparison at `gen_desc_image.py:192-193` (receipt 07); all five shipping configurations pass the new refusal (receipt 08) | R352-1 | 499b15f97eb0a469b7cd1308fbba7af3c64d1851 |
| Tests | UNCLEAN (F1) | `test_gen_desc_image.py` read and mutation-checked; `measure_test_evidence.py --check`; suites and gates rc 0; capture receipt provenance vs harness scope `soc.py:24,62`, README:85-113,136 (receipt 11) | R352-1 | 499b15f97eb0a469b7cd1308fbba7af3c64d1851 |
| Docs | UNCLEAN (F1) | CHANGELOG.md:11,36-45; SUBMODULES.md:25,57-73; SAVED_STATE_MATERIALIZATION.md:229-233; PP_DESCRIPTOR_OWNERSHIP.md:1-5,59,160-175,238-250; drawio/svg/png/manifest; docs gate set rc 0 (receipts 05, 15, 16) | R352-1 | 499b15f97eb0a469b7cd1308fbba7af3c64d1851 |

Tests and Docs become clean when F1 is fixed or dispositioned and re-reviewed at a head that includes the fix. A later commit touching any artifact in another lens's scope un-covers that lens.

## Real limits

- Allowed scope only. I did not run the full parent/processor/gPTP/Yosys/builder banks, act, the host CI runner or its self-test. The builder bank in both compiler modes is manager and author evidence (`147cb4b8:review-evidence/580-r1/author/builder-*.log`); I did not reproduce it. The five-configuration comparison used the builder entry point per configuration.
- Simulator: the assigned pinned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` did not exist. I used the lane-580 manager's pinned launcher prefix after verifying it reports `Verilator 5.050 2026-07-01 rev v5.050` (binary digests in receipt 00). A private launcher capped `-j 0` build parallelism to 8. Other lanes loaded the shared host concurrently.
- Two Markdown gates need the pinned renderer, which the system Python lacks. I ran them with the existing pinned Markdown environment, without installing anything (receipt 16).
- The five-configuration comparison temporarily checked out the processor submodule at `870ff88a` in this clone and then returned it to `16be6768`. The comparison is same-tree, as in the author's method.
- The milan_dp run outlived the tool's ten-minute foreground bound and was awaited to completion (rc 0, 1457 s). No other job ran in the clone meanwhile.
- Full suite logs contain local install paths and are not published. Their sha256 values are in receipts 14.
- Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.
- Hosted snapshot at review time (receipt 12): 15 success, 1 skipped (physical gPTP), 4 still in progress (docs-check, Verilator shards 1, 2 and 4). That is not final hosted evidence.

## Clone restoration

After all probes (receipt 17): HEAD `499b15f9`, tree `83b988d3`, index tree equal to HEAD tree, `git diff HEAD` rc 0 after a full refresh. Every tracked blob re-hashes to its index id. There are no exec-bit mismatches and no assume-unchanged or skip-worktree flags. Gitlinks: protocol-processor `16be6768`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, all checked out clean. `external` is uninitialised, as at start. The only extra files are 30 ignored build outputs, none tracked.

## Pending manager duties

- Record a decision on F1's scope conflict (receipt provenance vs assignment item 4). Then have the fix re-reviewed for Tests and Docs.
- Hosted exact-head contexts and the act replica, which the manager owns. Four hosted jobs were still in progress at snapshot.
- Candidate merge validation against live dev (source base `682ecf0c`), and the separate source bank.
- The external review (R353) is independent of this one. The merge still needs two positive reviews, the full completion bar and maintainer authorization.

R352-1 FINISHED
