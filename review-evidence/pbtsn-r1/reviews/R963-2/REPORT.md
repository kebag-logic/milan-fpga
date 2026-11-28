[R963] NEGATIVE - exact head 40c3111a060fc7b430112dc51222da77837169af

# R963-2 independent review: kebag-logic/tsn-c-stack PR #43 / issue #42 (AEM-01), round 2

- Reviewed head: `40c3111a060fc7b430112dc51222da77837169af`, tree `6368a4741bc3849a38fda74efe9c6acf13130103`, in a reviewer-isolated detached clone.
- Scope: this lane's commits from `79c4ba8`. The judged delta is `ef5e5ce..40c3111`: the merge `70a437f` of main `bf02d81` (PR #44), then `9d06d80`, `9e2a466`, `ee3c173`, `b03d499` and `40c3111`. `dev-linux` is out of scope.
- Rule for this later round: code the delta does not touch keeps its round-1 lens verdict unless the delta changes something it depends on.
- Order of work:
  1. Public scope: CONTRIBUTING, docs, issue #42 (body only, no comments), the PR body.
  2. The diff and its history.
  3. My own independent observations, recorded before I read any prior finding.
  4. The round-1 findings of both reviews (PR comments 7237707384 and 7237757332), each resolved below.
- No report of this round by another reviewer was read.

## Verdict

**NEGATIVE.** One MINOR finding is open (F1, Tests and Docs). There is no BLOCKER or MAJOR.

All ten round-1 findings are closed at their cause:
- internal F1 to F3;
- external F1 to F7.

So are both external residues and every round-1 suggestion the author took.

The head code is correct and every gate passes. F1 has two parts:
- One AAF reserved field has no refusal test: a planted defect there passes the whole kit.
- The PR body and CHANGELOG say the planted defects cover "every format field" and "field by field", and that is not true.

## Findings

### F1 - MINOR - Tests, Docs - one AAF reserved field is untested, and the "every format field" plant claim is overstated

- **Where:**
  - The predicate: `src/pbaem.c:53-54` (`pbaem_input_format_supported`).
  - The tests: `tests/test_pbaem.cpp:168-179` (`Pbaem.StreamFormats` refusals) and `tests/test_pbaem.cpp:227-241` (`Pbaem.AafFieldRefusals`).
  - The plants: `tests/mutations.json` (the 27 `pbaem-` plants).
  - The claims:
    - `CHANGELOG.md:5` ("Twenty-seven planted defects cover the model: its format refusals field by field").
    - PR body, "Tests" ("27 planted defects cover every format field").
    - Commit `9e2a466`'s subject ("Refuse each other AAF field").
- **Authority:**
  - CONTRIBUTING: "A regression needs a failing assertion and a runnable planted defect".
  - AEM-01 (`docs/requirements.json`): accept "each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU". Reserved bits set is not such a format.
  - The AAF stream-format layout as the generator documents it (milan-fpga `58f7673b` `avdecc/aem_descriptors.py:144-146`): ut is qword bit 52, so bits 53 to 55 are reserved.
  - Issue #42: "passes the repository's planted-defect campaign".
- **Evidence:** `receipts/format-field-probes.txt`, produced by `scripts/field_probes.sh` and `scripts/head_refusals.c`. Each probe drops one field from the comparison on line 54 in a scratch copy, then runs `pbaem_tests` and `entity_tests`. The unmodified baseline passes.

  | Probe (field dropped from the comparison) | Result | Planted defect at head |
  |---|---|---|
  | bit_depth, bits 32-39 | KILLED by "24-bit depth is refused" (`test_pbaem.cpp:176`) | none |
  | ut, bit 52 | KILLED by "the family entry is not a stream format" (`:177`) | none |
  | ut plus reserved, bits 52-55 | KILLED (same assertion) | none |
  | **reserved, bits 53-55** | **SURVIVED every test** | none |
  | reserved low bits 1-11 (bit 0 still compared) | SURVIVED (see S1) | `pbaem-ignore-reserved` drops all 12 bits and is caught |

  - At head the predicate refuses each of these formats on every AAF input: `0x0225…`, `0x0245…`, `0x0285…`, `…6800`, `…6002`, 24-bit and ut set.
  - Fields that do have a plant: the v bit, subtype, nsr, format code, channel count (zero and nine), samples_per_frame and the low reserved field.
  - So bit_depth and ut have assertions but no plant, and the 3-bit reserved field at bits 53 to 55 has neither.
- **Impact:**
  - A regression that accepts a format with a reserved bit set in 53 to 55 passes all 550 plants, coverage, both targets and the golden. The golden reads only the init defaults.
  - The round's own headline claim, that the format refusals are covered field by field, is wrong for three fields.
  - The head behaviour is correct. What is missing is the protection and an accurate statement of it.
  - This is graded MINOR, not RESIDUE, because the defect is a missing test plus a false test-coverage claim. It is not wording alone.
- **Required outcome:**
  1. In `Pbaem.AafFieldRefusals`, add a refusal on each AAF input of a format with a reserved bit set in 53 to 55, e.g. `0x0225022002006000` (bit 53). Give it its own plant, e.g. `pbaem-ignore-reserved-high`, which drops `UINT64_C(0x7) << 53` from both sides of the comparison.
  2. Register plants for the two fields that are asserted but not planted:
     - `pbaem-ignore-bit-depth`: drop `UINT64_C(0xff) << 32`. It is caught by "24-bit depth is refused".
     - `pbaem-ignore-ut`: drop `UINT64_C(1) << 52`. It is caught by "the family entry is not a stream format".
  3. Update `docs/TESTS.md` and the plant counts:
     - `docs/VERIFICATION.md:24` ("All 545 core plants");
     - `CHANGELOG.md:5` ("Twenty-seven");
     - the PR body ("27 planted defects", "all 550").
  4. Alternative to steps 2 and 3: narrow the claims to the fields actually planted. Step 1 is needed either way.
- **Verification:**
  - Rerun `scripts/field_probes.sh <clone> <work>`: every probe except the bit 1-11 probe (S1) is KILLED.
  - `python3 scripts/mutation.py --work <w> --jobs 16` catches the new plants by their named assertions.
  - `python3 scripts/test_inventory.py` and `python3 scripts/traceability.py --selftest` pass.

### Residue (wording only; does not affect the verdict)

- **RES-1 (evidence packet wording, not the PR).** The round-2 packet points readers at a receipts directory that does not exist under that name:
  - `review-evidence/pbtsn-r1/author-r2/REVIEW-READY.md` ("Receipts: `receipts/round2/`");
  - `round2/HANDOFF-r2.md` ("Receipts are in `../receipts/round2/`").

  The directory is `author-r2/receipts-round2/`. Exact fix: replace both with `receipts-round2/`.

### Suggestions (do not affect the verdict)

- **S1 (Tests), `tests/test_pbaem.cpp:238-239`.** The low reserved field is asserted only at bit 0, so a predicate that compares only bit 0 of the twelve passes (`receipts/format-field-probes.txt`). Adding `0x0205022002006800` (bit 11) next to `…6001` closes it at no cost.
- **S2 (Docs), `docs/POCKETBEAGLE.md:65`.** The golden's identity lists entity ID, MAC, name and firmware version. `entity_check_aem` (`examples/entity_roundtrip.c:290-297`) also sets `clock_identity` equal to the entity ID and leaves serial number and group name empty. Stating those three makes the identity complete for anyone who regenerates the golden.
- **S3 (Docs), `docs/POCKETBEAGLE.md:57`.** Regenerating needs milan-fpga `58f7673b` with its `protocol-processor` gitlink (`801ef228`): `gen_desc_image` lives there. A checkout without that submodule fails with `ModuleNotFoundError`. A half-sentence saying so would save the next reader a step.

## Round-1 findings: resolution at this head

| Round-1 item | Status at 40c3111 | Evidence |
|---|---|---|
| internal F1 / external F3: AEM-01 traced to the import baseline | **Closed.** | <ul><li>`scripts/requirement_records.py` gains an `AEM-01` origin "tsn-c-stack issue 42".</li><li>`docs/requirements.json` carries `origin`.</li><li>`docs/REQUIREMENTS.md` says "AEM-01 originates from issue #42".</li><li>The `docs/TRACEABILITY.md` AEM-01 row links issue 42.</li><li>The traceability gate passes (`receipts/validate-gates.json`).</li></ul> |
| internal F2 / external F4: PCM32 refusals and the stream bound not killed by plants | **Closed** for every field and bound named in round 1. | <ul><li>Five refusals, each with its own plant: `pbaem-ignore-format-code`, `-ignore-samples-per-frame`, `-ignore-subtype`, `-ignore-subtype-high-bit`, `-ignore-reserved`.</li><li>`Pbaem.AbsentInputRefusesEverything` with `pbaem-absent-input-bound`.</li><li>All six are CAUGHT by their named assertions (`receipts/mutation-summary.txt`).</li><li>New, separate gap: F1.</li></ul> |
| internal F3 / external RES-1: RV32 gate says "three cores" | **Closed.** | <ul><li>`scripts/baremetal.py:39` says "all three cores and the AEM model".</li><li>`:90` names the entity and PocketBeagle AEM image checks.</li><li>Both smoke logs carry the new line (`receipts/rv32-smoke-summary.txt`).</li></ul> |
| external F1: Milan v1.2 clause numbers | **Closed.** | <ul><li>`src/pbaem.c:125, 190, 214, 231, 264, 301, 319` now cite IEEE 7.3.7 and Milan 5.3.3.4, 5.3.3.5, 5.3.3.6, 5.3.3.7 with 5.3.3.9, 5.3.3.10 with 5.3.12, and 5.3.3.11.</li><li>Each is exactly the correction round 1 required.</li><li>The generator's own comments corroborate 5.3.3.4 (streams) and 6.5 (ut).</li><li>Limit: no copy of the specification text was consulted this round.</li></ul> |
| external F2 / internal S7: LOCALE `en-EN` | **Closed.** | <ul><li>`src/pbaem.c:251` is `en-US`: ISO 639 `en`, ISO 3166-1 `US` (IEEE 1722.1-2021 7.2.11). The test is at `tests/test_pbaem.cpp:221`.</li><li>The golden CRC is `0xD891CD2F`. I reproduced it independently from the public generator with my own configuration; see Conformance.</li></ul> |
| external F5: identity only short strings and one model ID; held state | **Closed.** | <ul><li>`PbaemIdentity.FullWidthStringsAndModel` uses four unterminated 64-octet strings and model ID `0x0123456789abcdef`.</li><li>`Pbaem.InitResetsHeldState` re-initializes a model that held state.</li><li>Six plants: `pbaem-name/firmware/group/serial-truncated`, `-model-id-constant` and `-init-keeps-state`, all CAUGHT.</li></ul> |
| external F6: #41 exemption undocumented | **Closed, documented once.** | <ul><li>The merge `70a437f` resolves both conflicts to main's side.</li><li>`scripts/check_privacy.py` is byte-identical to `bf02d81`.</li><li>`docs/IMPORT.md:137` and `docs/VERIFICATION.md:43` name the #29 and #41 merges.</li><li>The lane's duplicate CHANGELOG line was dropped, so #44's line is the only one (`CHANGELOG.md:7`).</li><li>The self-test now iterates both exempt merges: "17 commit controls pass" (`receipts/privacy.log`). That also closes internal S3 and external S4.</li></ul> |
| external F7: POCKETBEAGLE.md cites what is not at the named place | **Closed.** | <ul><li>`docs/POCKETBEAGLE.md:53-58` says the 4x4 + CRF configuration is not yet published and that the published branches hold the earlier shape.</li><li>It names the generator at a pinned commit, and the facts it relies on are on the page.</li><li>The AECP, media and SRP rows are marked "Not yet published", and "Rows marked not yet published have no public evidence today".</li><li>The claim "milan-fpga at 58f7673b generates the image from them" holds: see Conformance.</li></ul> |
| external RES-2: "base format of 1 to 8 channels" | **Closed.** | The corrected wording is in REQUIREMENTS, requirements.json, the page (`:40-45`, with 6.2 and 6.5), the CHANGELOG and the PR body. |
| internal S1, S2, S4, S5, S6; external S1, S2 | **Taken.** | <ul><li>S1: the firmware-AECP attribution (`POCKETBEAGLE.md:47-48`).</li><li>S2: golden provenance (`:57-66`).</li><li>S4 and external S1: the PORTING section with the stack figure.</li><li>S5: `<cstdio>`.</li><li>S6: the published dumps are keyed by header. They are byte-identical to my header-keyed dump.</li><li>External S2: DEV-01.</li></ul> |
| external S3 (generator defaults) | Not taken, with a reason ("milan-fpga's to change"). | A suggestion. Accepted. |

## Evidence by lens

### Conformance: CLEAN

- **Delta examined:**
  - the seven clause comments in `src/pbaem.c`;
  - the LOCALE identifier;
  - the AEM-01 text and origin in REQUIREMENTS, requirements.json and TRACEABILITY;
  - the formats table and the clause table in `docs/POCKETBEAGLE.md`;
  - DEV-01.
- **Golden regenerated independently** (`receipts/aem-golden-regeneration.txt`):
  - I wrote my own end-station configuration, `scripts/reviewer_pb2_4x4.yaml`, from the facts on the page alone, with `entity.locale: en-US`.
  - I ran it through the public generator at milan-fpga `58f7673b8c57a80230e716bc1774ff9cc2f71ddc`, with its `protocol-processor` gitlink `801ef2283ec793e35a2590fc6593c90313a64041`, using `scripts/regen_aem.py`.
  - Result: 84 descriptors, 8105 octets, CRC-32 `0xd891cd2f`, hash-derived model ID `0x001bc5c52e47a158`.
  - This is byte-identical, all 84 rows, to my own dump of the head model (`scripts/dump_pbaem.c`, the golden's identity; `receipts/aem-pbaem-head.txt`).
  - It is also byte-identical to the author's published firmware and model dumps.
- **Control:** the same configuration without `entity.locale` yields the generator default `en-EN`. That is CRC `0x1e668fba`, the round-1 golden, with the model ID unchanged and only the LOCALE row different. This supports the page's statement that the model ID "depends on the shape, not on the strings".
- **Merge correctness:** `70a437f` takes main's text in both conflicted files. `check_privacy.py` equals `bf02d81`. The only lane-side difference from main in the merged files is the `src/pbaem.c` coverage-ratchet row.
- **Unchanged code** keeps its round-1 verdict: every descriptor writer against IEEE 1722.1-2021 7.2 and the format words against Milan 6.2, 6.4 and 7.3.2. The delta changes only one string constant and comments in `src/pbaem.c`.

### RTL: CLEAN

- The delta contains no HDL, constraint or RTL file. It holds 2 `.c`, 1 `.cpp`, 3 `.py`, 9 `.md`, 2 `.json` and 1 ratchet file.
- Hardware-facing artifact examined instead: the RV32 freestanding build.
  - `scripts/baremetal.py --jobs 4`: Debug and Release, rc 0, executed under QEMU (`receipts/rv32-results.json`, `receipts/baremetal.log`).
  - Core imports are within the allowed set: `memcpy`, `memset`, `__mulsi3`, `__udivsi3`, `__umodsi3`, plus the port hooks. No symbol is left unresolved.
  - The smoke image runs the PocketBeagle AEM golden check (`receipts/rv32-smoke-summary.txt`).

### Robustness: CLEAN

- The delta adds no new input path.
- The one guard before an array write (`src/pbaem.c:47`) now has a test and a plant (`pbaem-absent-input-bound`, CAUGHT).
- A refused set on the absent input leaves the model byte-for-byte unchanged (`Pbaem.AbsentInputRefusesEverything`).
- At head the predicate refuses every malformed format I probed, on every AAF input (`receipts/format-field-probes.txt`). F1 concerns the tests for this, not the code.
- Gates that passed: address and undefined-behaviour sanitizers, static analysis (clang-tidy 18.1.3), boundary and conditionals (`receipts/validate-gates.json`).

### Tests: UNCLEAN (F1)

- **Examined:**
  - the four new tests in `tests/test_pbaem.cpp:227-298`;
  - the 12 new `pbaem-` plants in `tests/mutations.json`;
  - `docs/TESTS.md` (all 27 plants listed against their tests, with line anchors matching the file);
  - the coverage ratchet.
- **Executed:**
  - `validate.py --jobs 3 --graphs`: 28 of 28 gates rc 0 (`receipts/validate-gates.json`, `receipts/validate-console.log`).
  - The full campaign caught 550, with 0 escaped and 0 errors, and all 27 `pbaem-` plants were CAUGHT (`receipts/mutation-summary.txt`).
  - Coverage: `src/pbaem.c` 224/224 lines and 101/101 branches, 100 % (`receipts/coverage.log`).
  - The RV32 gate passed.
- **My own probes:** five field probes, of which three were KILLED and two SURVIVED. One survivor is F1 and the other is S1.

### Docs: UNCLEAN (F1)

- **Examined:**
  - `docs/POCKETBEAGLE.md` (every changed sentence against the code, the golden and the regenerated image);
  - `docs/PORTING.md` (new section against `include/pbaem.h`);
  - `docs/DEVIATIONS.md`, `docs/IMPORT.md`, `docs/REQUIREMENTS.md`, `docs/requirements.json`, `docs/TESTS.md`, `docs/TRACEABILITY.md`, `docs/VERIFICATION.md`;
  - `CHANGELOG.md` and the PR body.
- **Checked true:**
  - 545 + 5 = 550 plants, against the campaign.
  - 8105 octets and CRC `0xD891CD2F`, against my dump.
  - The golden identity, against `examples/entity_roundtrip.c:290-297`.
  - The stack statement, consistent with round 1's measurement.
  - "17 commit controls" and "5 rendered" graphs, against my run.
- **Overstated:** the "every format field" and "field by field" claims (F1).
- **Comment rule:** no new source comment in the delta carries a bench label, lane name, review round, reviewer ID or issue-comment ID. The delta's comments are clause references, `REQ: AEM-01` and, from main via #44, the `check_privacy.py` comment stating the exemption's reason. The new plant entries and test messages carry no labels either.

## Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/pbaem.c` clause comments and LOCALE; AEM-01 record and origin; `docs/POCKETBEAGLE.md` formats and clause table; DEV-01; merge `70a437f` resolution; golden regenerated from the public generator with a reviewer configuration, plus the locale control | R963-2 (unchanged descriptor writers: R963-1) | `40c3111a060fc7b430112dc51222da77837169af` |
| RTL | CLEAN | No HDL in the delta; RV32 Debug and Release freestanding build, imports, unresolved symbols, QEMU smoke with the AEM golden | R963-2 | `40c3111a060fc7b430112dc51222da77837169af` |
| Robustness | CLEAN | `src/pbaem.c:45-73` guards; absent-input refusal and model integrity; head refusal of probed malformed formats; sanitizer, static-analysis, boundary and conditionals gates | R963-2 | `40c3111a060fc7b430112dc51222da77837169af` |
| Tests | UNCLEAN (F1) | `tests/test_pbaem.cpp`, `tests/mutations.json` (27 `pbaem-` plants), `docs/TESTS.md`, coverage ratchet; full `validate.py` run, 550/550 campaign; 5 reviewer field probes and the head refusal check | R963-2 | `40c3111a060fc7b430112dc51222da77837169af` |
| Docs | UNCLEAN (F1) | POCKETBEAGLE, PORTING, DEVIATIONS, IMPORT, REQUIREMENTS, requirements.json, TESTS, TRACEABILITY, VERIFICATION, CHANGELOG, PR body; comment rule over every added line | R963-2 | `40c3111a060fc7b430112dc51222da77837169af` |

## Evidence inspected, not re-run

- **Author round-2 packet:** `review-evidence/pbtsn-r1/author-r2` on the evidence branch at `898af93474e91e3d73bc92df0bf975bd72720515`.
  - All 14 files match the `published_sha256` entries of `review-evidence/pbtsn-r1/MANIFEST.json`, and each equals its original (`receipts/author-r2-manifest-check.txt`).
  - The packet is hash-listed, not cryptographically signed.
  - The pinned packet commit `2a261083` holds only the round-1 packet. The round-2 packet is at the evidence branch tip.
- **Author receipts:** they claim 27 of 27 gates, 550 caught and RV32 rc 0. My own run at this head agrees.
- **Hosted, exact head** (`receipts/hosted-check-runs.txt`):
  - two workflow runs, each with an executed `quality` job and an executed `bare-metal` job, all four `success`;
  - no job was skipped;
  - the legacy combined status is `pending` with no status contexts.
  - Hosted and act acceptance belong to the manager.

## Real limits

- **Compilers:** GCC 16.2.1 and Clang 23.1.5 for the C++ builds, plus pinned Clang 18.1.3 (compiler-token gate), clang-tidy 18.1.3 and GoogleTest 1.14.0 (`receipts/environment.txt`).
  - These are not the CI's Ubuntu 24.04 images.
  - Branch counts differ by compiler: `pbaem.c` shows 101/101 here against the ratchet's 103/103 from the CI toolchain. Both are 100 %, and the coverage gate passes.
- **Job cap:** `validate.py` ran with `--jobs 3` beside `baremetal.py --jobs 4` to stay within 16 parallel jobs.
- **Clause numbers:** checked against the round-1 table, the code, the docs and the generator's comments. No copy of the IEEE 1722.1-2021 or Milan v1.2 text was consulted this round.
- **Board side:** I did not examine the board support repository, the bridge AECP log in the packet, or the board-side locale patch the packet mentions. The page's statement that its published branches hold the earlier shape rests on the round-1 external evidence.
- **Unpublished configuration:** the author's generator configuration is not published. The golden is reproduced from my own configuration, which is evidence that the stated facts determine the image. It is not evidence about the author's file.
- **Not claimed:**
  - No manager source bank ran at this head, and none is claimed or inferred.
  - Physical calibration: NOT RUN.
  - No hardware, no field run, no Docker/act.

## Pending manager duties

- Carry F1 to the author. Carry RES-1 to the residue checklist; it concerns the evidence packet's wording, not the PR.
- Build and validate the current-dev merge candidate at the merge turn: source base `79c4ba8`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks. Link its receipts on the PR.
- Own hosted and act acceptance at the head that is finally merged.
- Publish this packet: `REPORT.md` and the files in `MANIFEST.sha256`.

## Packet

Reviewer scripts are portable and take their paths as arguments:
- `scripts/env.sh`: needs `TOOLS`.
- `scripts/run_gates.sh`
- `scripts/field_probes.sh`
- `scripts/head_refusals.c`
- `scripts/dump_pbaem.c`
- `scripts/regen_aem.py`
- `scripts/reviewer_pb2_4x4.yaml`

Raw receipts are under `receipts/`. The list with hashes is in `MANIFEST.sha256`. After the probes, the clone was verified at exact head bytes (`receipts/clone-restore-check.txt`):
- index equals the tree;
- every tracked blob and mode matches;
- there are no gitlinks and no untracked files.

R963-2 FINISHED
