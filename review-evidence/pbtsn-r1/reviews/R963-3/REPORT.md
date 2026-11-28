[R963] POSITIVE - exact head ebaac61dfa3c83f9c6663ce1c361bf79f395f704

# R963-3 independent review: kebag-logic/tsn-c-stack PR #43 / issue #42 (AEM-01), round 3

- Reviewed head: `ebaac61dfa3c83f9c6663ce1c361bf79f395f704`, tree `e241f4d87493070283030f71a2c495998b9151c5`, in a reviewer-isolated detached clone.
- Scope: a narrow re-review. The judged delta is `40c3111..ebaac61`, two commits:
  - `9a0de3c`: tests, plants and plant counts.
  - `ebaac61`: the PocketBeagle page.
- What is judged:
  - My round-2 finding F1, at its cause.
  - The plant-coverage claim in the docs and the PR body.
  - The residues and suggestions from round 2.
  - That the descriptors, the golden CRC `0xd891cd2f` and the model ID are unchanged.
- Rule for this later round: code the delta does not touch keeps its round-2 lens verdict unless the delta changes something it depends on. The delta touches no file under `src/`, `include/`, `examples/`, `configs/`, `scripts/`, `cmake/` or `CMakeLists.txt` (`receipts/model-unchanged.txt`).
- Order of work:
  1. AGENTS/CONTRIBUTING rules, the issue's frozen acceptance and the PR body.
  2. The delta and its history.
  3. The author's round-3 packet.
  4. My own gate run, the mutation campaign, the RV32 gate and falsification probes.
  5. My verdict and the ledger below.
  6. Only then, the other reviewer's prior findings. They are resolved in their own section.

## Verdict

**POSITIVE.**
- No BLOCKER, MAJOR or MINOR finding is open.
- My round-2 F1 is closed at its cause.
- Four RESIDUE items remain. Each is wording only, and each comes with its exact fix:
  - two are in the evidence packet;
  - one is in the CHANGELOG and the PR body;
  - one is in the PocketBeagle page.
- Two SUGGESTIONS follow. Neither affects the verdict.

## Round-2 findings: resolution at this head

| Round-2 item | Status at ebaac61 | Evidence |
|---|---|---|
| **F1 (MINOR, Tests, Docs)**: bits 53 to 55 of the AAF format word are refused by the code but tested by nothing, and "every format field" / "field by field" overstates the plants. | **Closed.** All three steps of the required outcome were taken. | <ul><li>Step 1: `tests/test_pbaem.cpp:242-247` refuses `0x0225…`, `0x0245…` and `0x0285…` on each AAF input, each under its own message. Each has its own plant: `pbaem-ignore-reserved-bit-53`, `-54` and `-55` (`tests/mutations.json:8898`, `:8911`, `:8924`). Each plant drops one bit from both sides of the comparison. This is finer than the one 3-bit plant round 2 asked for.</li><li>Step 2: `pbaem-ignore-bit-depth` (`:8937`) and `pbaem-ignore-ut` (`:8950`) are registered. They are caught by "24-bit depth is refused" (`test_pbaem.cpp:176`) and "the family entry is not a stream format" (`:177`).</li><li>Step 3: counts are 551 core plants (`docs/VERIFICATION.md:24`) and Thirty-three (`CHANGELOG.md:5`). The PR body says 33 and 556. `docs/TESTS.md` lists all six new plants. All of these match `tests/mutations.json`: 556 plants, of which 533 are `src/`, 18 are `include/` and 5 are generated configuration plants; 33 are `pbaem-`.</li><li>Verification as round 2 required it. My own campaign: 556 of 556 CAUGHT, and each of the six new plants was caught by its own named needle (`receipts/mutation-summary.txt`). The campaign grades a catch only when the needle appears in the failure (`scripts/mutation.py:108`, `:225`). The test-inventory and traceability gates pass (`receipts/validate-gates.json`). My round-2 probe survivor, bits 53 to 55 dropped together, is now KILLED by the three new assertions (`receipts/format-field-probes.txt`).</li></ul> |
| **S1 (Tests)**: the low reserved field is asserted only at bit 0. | **Taken.** | <ul><li>`tests/test_pbaem.cpp:240` refuses `…6800` (bit 11). The plant is `pbaem-ignore-reserved-bit-11`, CAUGHT.</li><li>A loop at `:248-254` refuses every one-bit change of a valid 8-channel format outside the channel count.</li><li>My round-2 survivor, bits 1 to 11 dropped, is now KILLED. Dropping bits 1 to 10, bit 5 alone, bit 32, bit 47 or bit 57 is KILLED by the loop's assertion.</li></ul> |
| **S2 (Docs)**: the golden's identity is incomplete. | **Taken.** | `docs/POCKETBEAGLE.md:65` now states the clock identity equal to the entity ID, and an empty serial number and group name. That matches `examples/entity_roundtrip.c:291-297`: `memset` to zero, then `clock_identity = entity_id`, name and firmware only. |
| **S3 (Docs)**: regeneration needs the generator's submodule. | **Taken.** | <ul><li>`docs/POCKETBEAGLE.md:58` names the `protocol-processor` submodule at `801ef228`.</li><li>milan-fpga `58f7673b` records that gitlink, `801ef2283ec793e35a2590fc6593c90313a64041`.</li><li>That submodule commit holds `hdl/aecp/desc/gen_desc_image.py` (`receipts/pocketbeagle-page-checks.txt`).</li></ul> |
| **RES-1 (packet wording)**: the round-2 packet names `receipts/round2/`, but the directory is `receipts-round2/`. | **Retained as RES-1.** The packet says it was fixed. The published files still carry the old text. | See RES-1 below and `receipts/packet-pointer-check.txt`. |

## Findings

No open BLOCKER, MAJOR or MINOR finding.

### Residue (wording only; does not affect the verdict)

- **RES-1 - RESIDUE - Docs (evidence packet, not the PR) - retained from round 2.**
  - **Where:** milan-fpga `pbtsn-review-evidence` at `6aff8627f3a656def30294ed1c2d23f8f4853bab`:
    - `review-evidence/pbtsn-r1/author-r2/round2/HANDOFF-r2.md:21` ("Receipts are in `../receipts/round2/`");
    - `review-evidence/pbtsn-r1/author-r2/REVIEW-READY.md:40` ("Receipts: `receipts/round2/`").
  - **Evidence:**
    - The directory that exists is `author-r2/receipts-round2/`.
    - The round-3 packet claims the fix was made (`author-r3/REVIEW-READY.md:10`, `author-r3/round3/HANDOFF-r3.md:17`).
    - Commit `6aff862` changes no `author-r2/` file (`receipts/packet-pointer-check.txt`).
  - **Impact:** a reader following the pointer finds nothing. No measurement or verdict depends on it.
  - **Exact fix:** in both lines, replace `receipts/round2/` with `receipts-round2/`. Or drop the round-3 claim that it was fixed.
  - **Verification:** `git show <commit>:review-evidence/pbtsn-r1/author-r2/round2/HANDOFF-r2.md | grep receipts` shows `../receipts-round2/`.

- **RES-2 - RESIDUE - Docs (evidence packet, not the PR) - new.**
  - **Where:**
    - `author-r3/REVIEW-READY.md:35` ("Receipts: the round 3 section of `receipts/INDEX.md`");
    - `author-r3/round3/HANDOFF-r3.md:29` ("see the round 3 section of `../receipts/INDEX.md`");
    - `author-r3/REVIEW-READY.md:10` ("receipts are listed in `receipts/INDEX.md`").
  - **Evidence:**
    - `author-r3/` has no `receipts/` directory.
    - The only `INDEX.md` in the packet is the round-1 `author/receipts/INDEX.md`, and it has no round-3 section.
    - The round-3 receipts are in `author-r3/receipts-round3/` (`receipts/packet-pointer-check.txt`).
  - **Impact:** the pointer leads nowhere. The receipts themselves are published and match `MANIFEST.json` (`receipts/author-r3-manifest-check.txt`).
  - **Exact fix:** replace each pointer with `receipts-round3/` (from `round3/`, `../receipts-round3/`). Or add the round-3 section to `author/receipts/INDEX.md`.
  - **Verification:** each named path exists at the evidence commit.

- **RES-3 - RESIDUE - Docs, Tests (prose only) - the plant-coverage sentence leaves out a third of what the plants cover.**
  - **Where:**
    - `CHANGELOG.md:5`: "Thirty-three planted defects cover the model: each field of the AAF format word (…), the CRF input, the absent sixth input, full-width identity strings, the caller's model ID and a model that held earlier state."
    - PR body, "Tests": "Others cover the CRF input, the absent input, full-width identity strings, the caller's model ID and re-initialization."
  - **Evidence:**
    - The count, 33, is right (`tests/mutations.json`).
    - Every field the sentence names has a plant, and each is CAUGHT.
    - Eleven of the 33 plants cover subjects that neither text names:
      - `pbaem-short-write` and `pbaem-absent-index` (descriptor bounds);
      - `pbaem-clock-identity`;
      - `pbaem-cluster-signal`, `pbaem-output-port-base` and `pbaem-input-port-map` (cluster, port and map layout);
      - `pbaem-family-dropped` (the listed family format);
      - `pbaem-output-buffer`;
      - `pbaem-clock-bound` and `pbaem-crf-source-location` (clock sources);
      - `pbaem-identify-value`.
    - The CHANGELOG list also omits the subtype octet's high bit, which the PR body names.
  - **Why RESIDUE, not MINOR:**
    - The sentence understates and claims nothing false.
    - The figure is correct.
    - No test, plant or verdict depends on it.
    - The round-2 overstatement ("field by field" for fields with no plant) is gone.
  - **Exact fix (CHANGELOG):** "Thirty-three planted defects cover the model: each field of the AAF format word (subtype and its high bit, rate, the up-to bit, reserved bits 53, 54 and 55 one by one, format code, bit depth, channel count, samples per frame and the low reserved bits), the listed format family, the CRF input, the absent sixth input, the descriptor bounds and short write, the clock identity, the cluster, port and map layout, the output buffer, the clock-source bound and location, the IDENTIFY value, full-width identity strings, the caller's model ID and a model that held earlier state."
  - **Exact fix (PR body):** "Others cover the listed format family, the CRF input, the absent input, descriptor bounds and short writes, the clock identity, the cluster, port and map layout, the output buffer, clock sources, the IDENTIFY value, full-width identity strings, the caller's model ID and re-initialization."

- **RES-4 - RESIDUE - Docs - `docs/POCKETBEAGLE.md:55`, an unclear antecedent.**
  - **Text:** "Of its published branches, only `pb2-aecp-1` holds an end-station configuration, the earlier one-input shape."
  - **Problem:** the nearest antecedent of "its" is the configuration in line 54, not the repository.
  - **The claim itself holds:**
    - Of the five public branches of `kebag-logic/ti-sitara-am65x-bsp`, only `pb2-aecp-1` has an end-station configuration file: `milan-linux/config/endstation_pb2_bridge.yaml`.
    - That file declares one AAF input, one CRF input and one AAF output (`receipts/pocketbeagle-page-checks.txt`).
    - The check was a scan by file name.
  - **Exact fix:** "Of the board support repository's published branches, only `pb2-aecp-1` holds an end-station configuration, in the earlier one-input shape."

### Suggestions (do not affect the verdict)

- **S1 (Tests) - `tests/mutations.json:8885`, the plant `pbaem-ignore-reserved-bit-11`.**
  - It drops bits 1 to 11 (`~UINT64_C(0xffe)`), not bit 11 alone. The packet says so; the name and `docs/TESTS.md` do not.
  - Fix: rename it `pbaem-ignore-reserved-bits-1-11`, or narrow it to `UINT64_C(1) << 11` so the name is literal.
  - It is caught either way: my probe of bits 1 to 11 is KILLED.
- **S2 (Tests) - `tests/test_pbaem.cpp:248-254`, the loop's skip of bits 22 to 31.**
  - The skip is not needed. From the 8-channel base, every one-bit change of the channel count gives 0, 9, 10, 12 or 24 to 520 channels, and each of those is refused.
  - Running the loop over all 64 bits would also cover the channel field, one bit at a time, at no cost. The message would then read "a one-bit change is refused, bit N".

## Evidence by lens

### Conformance: CLEAN

- **Delta examined:** the two commits; `docs/POCKETBEAGLE.md:52-67`; and the AAF format words in the new assertions, decoded against the AAF stream-format layout. Round 2 cites that layout from the generator: ut is bit 52, bits 53 to 55 are reserved, the low reserved field is bits 0 to 11, and the channel count is bits 22 to 31.
  - `0x0225…`, `0x0245…` and `0x0285…` are the 48 kHz base with exactly bit 53, 54 or 55 set.
  - `…6800` is bit 11.
  - Refusing them follows AEM-01: accept only "each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU".
- **Model unchanged** (`receipts/model-unchanged.txt`):
  - No source, header, example, configuration or script changed in the delta.
  - The golden constant is still `0xd891cd2f` (`examples/entity_roundtrip.c:314`), and the `entity-golden` gate passes.
  - The configuration's model ID is still `0x001BC5C52E47A158`.
  - My RV32 Release `pbaem.c` object is byte-identical to my round-2 build on the same toolchain: sha256 `4549fe4c…`.
- **Page claims checked true** (`receipts/pocketbeagle-page-checks.txt`):
  - the generator's submodule gitlink and its image builder;
  - the golden's full identity;
  - the board branch statement (RES-4 is the wording of that one).
- **Unchanged code** keeps its round-2 verdict: every descriptor writer against IEEE 1722.1-2021 7.2, and the format words against Milan v1.2 6.2, 6.4 and 7.3.2.

### RTL: CLEAN

- The delta contains no HDL, constraint or RTL file. It holds 1 `.cpp`, 1 `.json` and 5 `.md` files.
- Hardware-facing artifact examined instead: the RV32 freestanding build. Its sources are unchanged, and I ran it at this head: `baremetal.py --jobs 8` rc 0, Debug and Release on QEMU. The smoke line includes "five generated entity round trips; the PocketBeagle AEM image" (`receipts/baremetal.log`).
- Hosted at the exact head: bare-metal ran twice and succeeded twice (`receipts/hosted-check-runs.txt`). Both jobs executed; none was skipped.

### Robustness: CLEAN

- The delta adds no input path or state.
- The format predicate (`src/pbaem.c:53-54`, unchanged) now has a test asserting that it refuses every one-bit change outside the channel count. Nine reviewer probes were each KILLED (`receipts/format-field-probes.txt`):
  - bits 53 to 55 together;
  - bits 52 to 55;
  - bits 1 to 11;
  - bits 1 to 10;
  - bit 0;
  - bit 5;
  - bit 32;
  - bit 47;
  - bit 57.
- Each probe drops one or more bits from the comparison in a scratch copy, then runs `pbaem_tests` and `entity_tests`. The unmodified baseline passes.
- These gates pass: address and undefined-behaviour sanitizers, static analysis with clang-tidy 18.1.3, boundary and conditionals (`receipts/validate-gates.json`).

### Tests: CLEAN

- **Examined:**
  - `tests/test_pbaem.cpp:227-256`;
  - the six new plants at `tests/mutations.json:8884-8961`;
  - `docs/TESTS.md:214-222`, where every anchor matches its `TEST_F` line: 227, 259, 275 and 301.
- **Executed at this head:**
  - `validate.py --jobs 16` with pinned Clang 18.1.3, clang-tidy 18.1.3 and GoogleTest 1.14.0: 27 of 27 gates rc 0 (`receipts/validate-console.log`, `receipts/validate-gates.json`);
  - the campaign inside it: 556 of 556 CAUGHT, and 33 of 33 `pbaem-` plants (`receipts/mutation-statuses.txt`);
  - the reviewer field probes.
- **F1 is closed.** S1 and S2 are suggestions only.

### Docs: CLEAN

- **Examined:** CHANGELOG, POCKETBEAGLE, TESTS, TRACEABILITY and VERIFICATION, the PR body, both commit messages, and the round-3 packet.
- **Checked true:**
  - the counts, 551 + 5 = 556 and 33;
  - the field list, where every named field has a CAUGHT plant;
  - commit `9a0de3c`'s "plant a defect in each format field". Every field of the word has at least one plant: the v bit, subtype, ut, each of bits 53 to 55, nsr, format, bit_depth, channels, samples_per_frame and the low reserved field;
  - the page's identity, submodule and branch statements.
- **Comment rule:** no added line in the delta carries a bench label, lane name, review round, reviewer ID or issue-comment ID (`git diff 40c3111..ebaac61`, scanned). The delta adds no source comment. It adds only test messages and plant entries, and both are free of labels.
- **Wording residue:** RES-1 to RES-4. None makes this lens unclean.

## Reviewer-owned lens ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | AAF words decoded in `tests/test_pbaem.cpp:240-254`; `docs/POCKETBEAGLE.md:52-67`; unchanged `src/`, `examples/` and `configs/`; golden `0xd891cd2f`; model ID; milan-fpga `58f7673b` gitlink `801ef228`; board branch scan | R963-3 (delta); R963-2 (unchanged code) | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| RTL | CLEAN | no HDL in the delta; RV32 `baremetal.py` Debug and Release rc 0 with the AEM image; Release `pbaem.c` object identical to round 2; hosted bare-metal success twice | R963-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Robustness | CLEAN | `src/pbaem.c:53-54` (unchanged); one-bit refusal loop; 9 reviewer probes KILLED; sanitizer, static-analysis, boundary and conditionals gates | R963-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Tests | CLEAN | `tests/test_pbaem.cpp`, `tests/mutations.json` (33 `pbaem-`, 556 total), `docs/TESTS.md`; `validate.py` 27/27; campaign 556/556 CAUGHT by needle | R963-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Docs | CLEAN (RES-1 to RES-4 recorded) | CHANGELOG, POCKETBEAGLE, TESTS, TRACEABILITY, VERIFICATION, PR body, commit messages, round-3 packet; comment-rule scan of every added line | R963-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |

## Other reviewer's prior findings

I read the external reviewer's round-2 report (comment `7238106277`) only after the verdict and the ledger above were written. It lists every round-1 item from both reviews, internal `7237707384` and external `7237757332`, and grades each one at `40c3111`. Reading it changed nothing above.

| Prior item | Status at ebaac61 | Evidence |
|---|---|---|
| External round-2 F1 (MINOR): bits 53 to 55 refused but unchecked, plus the overstated plant claim | **Closed.** | Same cause as my F1. The external probe `aaf-ignore-reserved-high` drops `UINT64_C(0x7) << 53`, which is my probe `ignore-reserved-53-55-together`. At this head it is KILLED by the three new assertions and by the one-bit loop. The required plant and counts are present (see the round-2 table above). |
| External round-2 RES-1: packet `receipts/round2/` pointer | **Retained.** | It is my RES-1. The published `author-r2/` files are unchanged. |
| External round-2 S1: the golden's full identity | **Taken.** | `docs/POCKETBEAGLE.md:65`. |
| External round-2 S2: a one-bit loop over the 54 bits outside the channel count | **Taken.** | `tests/test_pbaem.cpp:248-254`. The external survivor `aaf-ignore-reserved-low-bits-1-to-11` corresponds to my KILLED probe `ignore-low-reserved-bits-1-11`. |
| External round-2 S3: plants for bit depth and the up-to bit | **Taken.** | `pbaem-ignore-bit-depth` and `pbaem-ignore-ut`, both CAUGHT. |
| External round-2 S4: name the one branch | **Taken.** | `docs/POCKETBEAGLE.md:55` names `pb2-aecp-1`. The statement holds. Its "its" is RES-4. |
| Round-1 items from both reviews (external F1 to F7, S1 to S5; internal F1 to F3, S1 to S7) | **Closed at round 2. The delta reopens none.** | <ul><li>The delta changes no source, example, configuration or script, so the clause, LOCALE, origin, RV32 diagnostic and exemption closures stand.</li><li>Every round-1 plant is still CAUGHT (556/556).</li><li>External F7: the page edits at `:55`, `:58` and `:65` keep the "not yet published" statements and stay true (`receipts/pocketbeagle-page-checks.txt`).</li></ul> |

## Evidence inspected, not re-run

- **Author round-3 packet:** milan-fpga branch `pbtsn-review-evidence` at `6aff8627f3a656def30294ed1c2d23f8f4853bab` ("Add the round-3 packet"), `review-evidence/pbtsn-r1/author-r3/`.
  - The link in the review assignment pins `2a261083…`. That is the round-1 archive and an ancestor of this commit; it holds neither `author-r2/` nor `author-r3/`.
  - All ten `author-r3/` files match `MANIFEST.json`, and no file is unlisted (`receipts/author-r3-manifest-check.txt`).
- **Author receipts** claim:
  - 27 of 27 gates;
  - 556 caught, with the six new plants named;
  - `src/pbaem.c` at 224/224 lines and 103/103 branches;
  - RV32 rc 0;
  - privacy: 109 commits, 17 controls.

  My own gate and campaign runs agree. The coverage gate passed in my run. I did not re-extract the per-file coverage figures.
- **Hosted, exact head:** 4 check runs, all executed and all successful: `quality` twice and `bare-metal` twice. Hosted and act acceptance belong to the manager.

## Real limits

- **Toolchain:** GCC 16.2.1 for the C++ builds, plus pinned Clang 18.1.3, clang-tidy 18.1.3 and GoogleTest 1.14.0 (`receipts/environment.txt`). This is not the author's Ubuntu 24.04 replica.
- **Graphs:** I ran `validate.py` without `--graphs`. I did not render the diagrams; the delta changes none.
- **Packet integrity:** the packet commit is unsigned (`verified=false reason=unsigned`). Its integrity rests on the `MANIFEST.json` hashes only. The author's receipts do not record the head SHA inside them; they are tied to `ebaac61` by the packet's text alone. My own runs, which are at the exact head, carry the weight.
- **Board side:** the board branch claim was checked by a file-name scan of each public branch's tree. A configuration under another name would be missed. I did not examine board firmware, AECP logs or SRP suites.
- **Specification text:** clause numbers rest on round 2. I consulted no copy of IEEE 1722.1-2021 or Milan v1.2 this round.
- **Not claimed:** physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the author's receipts plus my own runs above.

## Pending manager duties

- Carry RES-1 to RES-4 to the residue checklist. RES-1 and RES-2 concern the evidence packet. RES-3 concerns the CHANGELOG and the PR body. RES-4 concerns `docs/POCKETBEAGLE.md:55`.
- Correct the evidence pointer for this round. The round-3 packet is at `6aff8627…` on `pbtsn-review-evidence`, not at `2a261083…`.
- Build and validate the current-dev merge candidate at the merge turn (source base `79c4ba8`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), with the builder and native banks. Link its receipts on the PR.
- Own hosted and act acceptance at the head that is finally merged.
- Publish this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R963-3 FINISHED
