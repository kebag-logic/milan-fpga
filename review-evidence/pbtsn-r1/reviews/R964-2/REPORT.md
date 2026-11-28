[R964] NEGATIVE - exact head 40c3111a060fc7b430112dc51222da77837169af

# R964-2 independent external review: kebag-logic/tsn-c-stack PR #43 (issue #42, AEM-01), round 2

- Exact head `40c3111a060fc7b430112dc51222da77837169af`, tree `6368a4741bc3849a38fda74efe9c6acf13130103`.
- Delta judged: `ef5e5ce..40c3111` (merge `70a437f` of main `bf02d81`, then `9d06d80`, `9e2a466`, `ee3c173`, `b03d499`, `40c3111`), inside the lane scope `79c4ba8..40c3111`. The `dev-linux` commits are out of scope. Of the merge, only the conflict resolution was reviewed, not PR #44's own content.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/43#issuecomment-7237921791
- Order followed: CONTRIBUTING.md (there is no AGENTS.md), README and docs, issue #42 (body only; it has no comments), the PR body, the delta and its history, the evidence packet, then my own pass. Only after that pass did I read the two round-1 reports (7237707384 and 7237757332). No round-2 report of another reviewer was read.

## Verdict

NEGATIVE, on one narrow MINOR finding (F1, Tests and Docs). Everything else in both round-1 reports is closed at this head, and I confirmed each closure with my own run or probe.

The main acceptance point holds again after the locale change. I regenerated the image from the public generator with `entity.locale: en-US`. It equals the model's 84 descriptors byte for byte, with the new golden CRC `0xd891cd2f`.

F1 in short: the code refuses a format word with any of bits 53 to 55 set, but no assertion and no planted defect checks that. One widening of the accepted formats therefore still passes the whole kit, while the change log and the PR body say the format refusals are covered field by field.

## What I established at the exact head

| Claim | Result | Receipt |
|---|---|---|
| Validation kit, 27 gates | 27 of 27 rc 0 | `receipts/validate.log`, `receipts/validate-gates.json` |
| Planted defects | 550 caught, 0 escaped, 0 error; all 27 `pbaem-` and all 4 `entity-` plants caught; same names and verdicts as the author's report | `receipts/validate-mutation-lane-plants.txt` |
| Coverage of `src/pbaem.c` | 224/224 lines, 100 % of branches (101/101 with this host's compiler; the ratchet's 103/103 is the CI compiler's count) | `receipts/validate-coverage.log` |
| Sanitizers | 11 of 11 test binaries pass under the address and undefined-behaviour sanitizers | `receipts/validate-clang-sanitizers-test.log` |
| Traceability and test inventory | 48 requirements, 211 test declarations, 550 plants; the AEM-01 row links issue 42 | `receipts/validate-traceability.log`, `receipts/validate-test-inventory.log` |
| Privacy | 107 commits, 621 historical blobs, 107 files, pass; 17 self-test controls pass | `receipts/validate-privacy.log`, `receipts/validate-privacy-selftest.log` |
| RV32 Debug and Release on QEMU | rc 0; smoke exit status 0 in both; the summary line names the entity and AEM image checks | `receipts/baremetal.log`, `receipts/probe_rv32.txt` |
| RV32 golden is sensitive to the new locale | with `en-EN` planted back, the smoke exits 92 in Debug and Release | `receipts/probe_rv32.txt` |
| Model equals an image I regenerated from the public generator | 84 of 84 identical, 8105 bytes, CRC-32 `0xd891cd2f`; the unpinned hash-derived model ID is `0x001bc5c52e47a158` with and without the locale | `receipts/aem-regenerate-compare.txt` |
| Model equals the author's published round-2 dumps | 84 of 84; my model dump is identical text to the author's; dump labels now equal each descriptor's own type and index | `receipts/aem-regenerate-compare.txt` |
| Round-1 probes | all ten that survived in round 1 are now killed by a `Pbaem` test | `receipts/probe_pbaem.txt` |
| New probe | `aaf-ignore-reserved-high` survives (F1) | `receipts/probe_pbaem.txt`, `receipts/probe_reserved_high.txt` |
| Stack figure in the docs | the `pbaem_descriptor` frame on RV32 is 512 bytes at `-O0` and 496 at `-O2` and `-Os`, so "about 500 octets" holds | `receipts/stack-usage-rv32.txt` |
| Hosted checks at this head | 4 jobs in 2 runs (push and pull_request), all executed, all success, none skipped | `receipts/hosted-checks.txt` |
| Evidence packet, round 2 | 14 of 14 `author-r2` files match the packet manifest | `receipts/evidence-manifest-check.txt` |
| Board support repository today | no 4x4 configuration on any public branch; one branch holds the one-input shape | `receipts/bsp-public-state.txt` |

The regeneration used milan-fpga `58f7673b` with its `protocol-processor` gitlink `801ef228` and its `gptp-processor` gitlink `1616fc8f`. The configuration is one I wrote from public facts (`scripts/reviewer_endstation_pb2_4x4.yaml`): my round-1 file plus one key, `entity.locale: "en-US"`. It is not the author's unpublished file.

## Finding

### F1 - MINOR - Tests, Docs - bits 53 to 55 of the AAF format word are refused by the code but checked by no test

- Where:
  - `src/pbaem.c:53-54` (`pbaem_input_format_supported`), unchanged and correct.
  - `tests/test_pbaem.cpp:227-242` (`Pbaem.AafFieldRefusals`) and `:169-178`: no offered format has any of bits 53 to 55 set.
  - `tests/mutations.json`: no plant reaches those bits.
  - `CHANGELOG.md:5`: "Twenty-seven planted defects cover the model: its format refusals field by field".
  - PR body: "27 planted defects cover every format field".
- Evidence: `receipts/probe_pbaem.txt`, `receipts/probe_reserved_high.txt`, `scripts/probe_pbaem.py`, `scripts/reserved_high.c`.
  - Probe `aaf-ignore-reserved-high` drops `UINT64_C(0x7) << 53` from the comparison on line 54. The `pbaem` test binary (9 tests) and the `entity` test binary (5 tests) both pass.
  - The probe is not equivalent. At the head, 224 words that differ from a valid format only in those bits are all refused. With the probe, all 224 are supported and stored; `0x02e5022002006000`, for example, becomes a STREAM_INPUT current format.
  - Every other field of the word is protected. My probes for the subtype octet, its high bit, the up-to bit (bit 52), the rate, the format code, the bit depth, the samples per frame and the low reserved bits are all killed. So are the channel-count plants.
  - Bits 53 to 55 are the three bits above the up-to bit in the rate octet. They are the only bits outside the channel count that no assertion reaches.
- Authority:
  - AEM-01: "Accept on an AAF input each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU". A word with those bits set is none of these.
  - `docs/POCKETBEAGLE.md:63` and `docs/PORTING.md:523`: the setters "accept only what the model advertises" and "refuse what the model does not advertise".
  - `docs/CODING_STANDARD.md`: "Add assertions for malformed input, boundary values".
  - R964-1 F4, required outcome: "that an AAF input refuses ... nonzero reserved bits". The round-2 test covers the low reserved field only.
  - Issue #42: "full test coverage and passes the repository's planted-defect campaign".
- Impact: a change that accepts malformed AAF format words in `pbaem_set_input_format` would pass every gate, and the two statements above overstate what the plants cover. The head code itself is correct. This is the last unprotected field of the one predicate AEM-01 defines. It is small, and it is the same class as the four fields fixed this round.
- Required outcome:
  - In `Pbaem.AafFieldRefusals`, assert that an AAF input refuses a valid format with a bit of 53 to 55 set, for example `0x0225022002006000`, `0x0245022002006000` and `0x0285022002006000`.
  - Register one plant for it in `tests/mutations.json`, for example the probe's line.
  - Update the counts that follow: `docs/TESTS.md`, `docs/VERIFICATION.md:24` (545 core plants), `CHANGELOG.md:5` (twenty-seven) and the PR body (27 and 550).
- Verification:
  - `python3 scripts/probe_pbaem.py <clone> <work> <gtest-prefix>` reports `aaf-ignore-reserved-high` KILLED.
  - `python3 scripts/mutation.py --select pbaem-` catches the new plant. `python3 scripts/test_inventory.py` and `python3 scripts/traceability.py --selftest` still pass.

## Prior findings at this head

Each was checked at its cause, not from the author's table.

### R964-1 (external, 7237757332)

| Finding | State | Evidence at `40c3111` |
|---|---|---|
| F1 wrong Milan clause numbers | CLOSED | `src/pbaem.c:125` cites IEEE 7.3.7; `:190` Milan 5.3.3.4; `:214` 5.3.3.5; `:231` 5.3.3.6; `:264` 5.3.3.7 and 5.3.3.9; `:301` 5.3.3.10 and 5.3.12; `:319` 5.3.3.11. Each equals the "correct clause" column of R964-1 F1. The comment gate passes (`receipts/validate-comments.log`). |
| F2 LOCALE `en-EN` | CLOSED | `src/pbaem.c:251` and `tests/test_pbaem.cpp:221` say `en-US`; the golden is `0xd891cd2f` at `examples/entity_roundtrip.c:314`. The public generator accepts `entity.locale` and, given `en-US`, emits the same 84 descriptors. Probe `locale-en-EN` is killed by the unit test and by the golden, on Linux and on RV32. |
| F3 AEM-01 traced to the import baseline | CLOSED | `scripts/requirement_records.py:17-20`, `docs/requirements.json:1007-1010`, `docs/REQUIREMENTS.md:40`, `docs/TRACEABILITY.md:58`. Traceability gate rc 0. |
| F4 format predicate and stream bound survive probes | CLOSED as stated; one sibling field is this round's F1 | The five probes are killed: `aaf-stream-bound-off-by-one-supported` by `Pbaem.AbsentInputRefusesEverything`, the four field probes by `Pbaem.AafFieldRefusals`. Six plants are registered and caught. |
| F5 identity only for short strings and one model ID | CLOSED | The five probes are killed by `PbaemIdentity.FullWidthStringsAndModel`. `init-keeps-old-state` is now killed by `Pbaem.InitResetsHeldState`. Six plants are registered and caught. |
| F6 #41 exemption undocumented | CLOSED | `docs/IMPORT.md:137` and `docs/VERIFICATION.md:43` name both merges. `scripts/check_privacy.py` and `docs/IMPORT.md` are byte-identical to main `bf02d81`. The lane's duplicate change-log line is gone. |
| F7 page cites things not at the place it names | CLOSED | `docs/POCKETBEAGLE.md:53-59` says the 4x4 configuration is not yet published and names the generator commit, which resolves and reproduces the image. Rows `:101-103` say "not yet published" and `:105` says so plainly. The public repository's state matches (`receipts/bsp-public-state.txt`). |
| RES-1 "three cores" | CLOSED | `scripts/baremetal.py:39` and `:90`; the smoke log carries the new summary. |
| RES-2 "base format of 1 to 8 channels" | CLOSED | `docs/REQUIREMENTS.md:47`, `docs/requirements.json:996`, `docs/POCKETBEAGLE.md:40-45`, `CHANGELOG.md:5`, PR body. |
| S1 porting contract | TAKEN | `docs/PORTING.md:518-525`, `docs/POCKETBEAGLE.md:69-71`. |
| S2 DEV-01 | TAKEN | `docs/DEVIATIONS.md:10`. |
| S3 generator defaults | NOT TAKEN, accepted | These belong to the generator's owner, not to this repository. They stay suggestions upstream. |
| S4 self-test picks one exempt merge at random | CLOSED by #44 | `scripts/check_privacy.py:56` iterates `sorted(TWO_LINE_MERGES)`. |
| S5 dump labels | CLOSED | The round-2 dumps carry each descriptor's own type and index; 0 label differences. |

### R963-1 (internal, 7237707384)

| Finding | State | Evidence at `40c3111` |
|---|---|---|
| F1 AEM-01 origin | CLOSED | As R964-1 F3. |
| F2 PCM32 base-format refusals untested | CLOSED | The format code, samples per frame, subtype, vendor bit and low reserved bits each have an assertion and a caught plant. My equivalent probes are killed. |
| F3 RV32 gate diagnostics | CLOSED | As R964-1 RES-1. |
| S1 mapped-channel refusal attributed to the firmware | TAKEN | `docs/POCKETBEAGLE.md:47-48`. |
| S2 golden provenance | TAKEN | `docs/POCKETBEAGLE.md:57`, `:64-67`. |
| S3 privacy self-test | CLOSED by #44 | As R964-1 S4. |
| S4 stack use | TAKEN | `docs/PORTING.md:524`; figure confirmed. |
| S5 `<cstdio>` | TAKEN | `tests/test_pbaem.cpp:4`. |
| S6 dump index column | TAKEN | As R964-1 S5. |
| S7 locale | CLOSED | As R964-1 F2. |

## Residue (wording only; does not affect the verdict)

- RES-1, evidence packet: `author-r2/REVIEW-READY.md` ends "Receipts: `receipts/round2/`", and `author-r2/round2/HANDOFF-r2.md` says "Receipts are in `../receipts/round2/`". The published directory is `author-r2/receipts-round2/`. Exact fix: "`receipts-round2/`" and "`../receipts-round2/`".

## Suggestions (do not affect the verdict)

- S1, `docs/POCKETBEAGLE.md:65`: the generator identity lists the entity ID, MAC, name and firmware version. The golden also depends on the clock identity (equal to the entity ID) and on empty group and serial strings (`examples/entity_roundtrip.c:290-297`). Naming them would let a reader reproduce the CRC from the page alone.
- S2, `tests/test_pbaem.cpp:227-242`: one loop could flip each of the 54 bits outside the channel count in a valid format and expect a refusal. That protects every bit with one assertion and closes F1 as well. Today only bits 0, 52, 56 and 63 are refused through a one-bit difference; the other examples differ from a valid word in two or more bits. My sub-field probe `aaf-ignore-reserved-low-bits-1-to-11` survives for that reason. I do not require bit-level coverage.
- S3, `tests/mutations.json`: the bit-depth and up-to-bit refusals have assertions but no registered plant. My probes show both assertions are sensitive. Registering them would make "planted defects cover every format field" exact once F1 is fixed.
- S4, `docs/POCKETBEAGLE.md:55`: "Its published branches still hold the earlier one-input shape". One branch, `pb2-aecp-1`, holds that shape; the others hold no end-station configuration. Naming the branch would be more exact.

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta: the seven clause citations in `src/pbaem.c` against the corrected clauses of R964-1 F1; the LOCALE identifier against IEEE 1722.1-2021 7.2.11 in the model, its test and the golden; the AEM-01 wording against the predicate; the format section and conformance table of `docs/POCKETBEAGLE.md`; byte comparison of all 84 descriptors with an image regenerated from the public generator and with the author's round-2 dumps. Untouched descriptor code keeps its R964-1 verdict; the delta changes one string in it. | R964-2 for the delta, R964-1 for the rest | `40c3111a060fc7b430112dc51222da77837169af` |
| RTL | CLEAN | The delta holds no HDL (2 `.c`, 1 `.cpp`, 3 `.py`, 9 `.md`, 2 `.json`, 1 ratchet). Hardware-facing artifact examined instead: the RV32 freestanding build in Debug and Release, its imports, its empty unresolved-symbol list, its stack frames and its QEMU smoke, with one fault probe in both configurations. | R964-2 | `40c3111a060fc7b430112dc51222da77837169af` |
| Robustness | CLEAN | The delta's only shipped-source changes are one string literal and seven comments, so every guard keeps its R964-1 verdict. Re-run at this head: address and undefined-behaviour sanitizers, static analysis, boundary gate. The absent input's refusal, which guards the only array write, now has an assertion and a caught plant. The merge resolution leaves the privacy gate identical to main. | R964-2 for the delta, R964-1 for the rest | `40c3111a060fc7b430112dc51222da77837169af` |
| Tests | UNCLEAN (F1) | `tests/test_pbaem.cpp` (four new cases), `tests/mutations.json` (550 entries, 27 `pbaem-`, 12 new), `tests/coverage.ratchet`, `examples/entity_roundtrip.c`, `scripts/baremetal.py`; the full kit and campaign; 28 reviewer probe runs (26 mutants, of which 24 are killed and 2 survive: F1 and one sub-field probe; one unmodified control; one equivalent control); one harness run on the head and on the F1 probe copy; one RV32 probe in 2 configurations. | R964-2 | `40c3111a060fc7b430112dc51222da77837169af` |
| Docs | UNCLEAN (F1) | Every changed line of `docs/POCKETBEAGLE.md`, `docs/PORTING.md`, `docs/REQUIREMENTS.md`, `docs/requirements.json`, `docs/TRACEABILITY.md`, `docs/TESTS.md`, `docs/VERIFICATION.md`, `docs/DEVIATIONS.md`, `docs/IMPORT.md` and `CHANGELOG.md`; the PR body; the delta's source comments against the comment rule. Figures recomputed: 84 descriptors, 8105 octets, the CRC, the stack frame, and the plant counts 545 + 5 and 27. | R964-2 | `40c3111a060fc7b430112dc51222da77837169af` |

Comment rule: no new source comment in the delta carries a bench label, lane name, review round, reviewer ID or issue-comment ID. The delta's source comments are `REQ: AEM-01` and clause references. No bench device identity appears in the delta. Commit subjects in the delta are one line, with no body or trailer.

## Limits

- The Milan v1.2 text could not be fetched again this round; the public site refused an automated download. R964-1 F1 is judged closed against the corrected clause numbers I recorded in round 1 from the Milan contents.
- IEEE 1722.1-2021 and IEEE 1722-2016 were not consulted directly this round. F1 does not rest on the standard's name for bits 53 to 55. It rests on the model's own exact-match rule.
- Compilers differ from the CI environment: GCC 16.2.1, Clang 23.1.5 for the sanitizer build and an RV32 GCC 16.2.0, with GoogleTest 1.14.0, the Clang 18.1.3 lexer and clang-tidy 18.1.3 pinned (`receipts/environment.txt`). Object hashes and branch counts differ from the author's receipts; every gate passed.
- The kit ran with `--jobs 4` to stay inside the parallel-job limit.
- The Mermaid diagrams were not rendered here. The delta changes no diagram, and the hosted `quality` job runs the kit with `--graphs` and succeeded.
- The regenerated image comes from a reviewer-written configuration. The author's configuration is not published, so I could not regenerate from it.
- The evidence commit is unsigned. I checked the round-2 packet by its manifest hashes and by git object IDs.
- In the round-2 packet, `bridge-aecp-locale.log` concerns another repository. I read it only for the firmware's mapped-channel refusal that `docs/POCKETBEAGLE.md:47` cites.
- No hardware, board, bench device or simulator beyond QEMU was used. Physical calibration was not run. Nothing here is hardware proof.
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts, the hosted jobs above and this review's own runs.
- The clone was left at the exact head: worktree and index equal `HEAD`, 107 tracked files rehashed with no blob or mode difference, no gitlinks, and nothing untracked or ignored after I removed the interpreter cache my runs wrote (`receipts/clone-state.txt`). All probes ran on scratch copies.

## Pending manager duties

- Carry RES-1 to the residue checklist.
- The evidence tree pinned in the assignment, `2a261083`, holds no `author-r2`. I read the round-2 packet at `898af934` on `pbtsn-review-evidence`. Link that commit where the packet is cited.
- At that commit the round-1 packet still opens `author/REPORT.md` and `author/receipts/INDEX.md` with a "Private" line. Line 2 of `author/round1/HANDOFF-r1.md` still carries what reads as a bench device label after the board-name redaction. Confirm these are meant to be public; I have not repeated the label.
- Byte identity is "for the same configuration". The generator's default locale is still `en-EN` at `58f7673b`, so the board's unpublished configuration must carry `entity.locale: en-US` for the board image to equal the model. When that configuration is published, regenerate from it and compare with the golden.
- Build and validate the current-dev merge candidate at the merge turn and link its receipts; own hosted acceptance.
- The PR is a draft against `main`. Its "Tests" bullet should follow the outcome of F1.

## Packet contents

Scripts (portable; paths are arguments): `scripts/env.sh`, `scripts/run_gates.sh`, `scripts/probe_pbaem.py`, `scripts/reserved_high.c`, `scripts/dump_aem.c`, `scripts/compare_aem.py`, `scripts/fetch_generator.sh`, `scripts/regen_image.py`, `scripts/reviewer_endstation_pb2_4x4.yaml`. Receipts are under `receipts/` and listed with their hashes in `MANIFEST.sha256`.

R964-2 FINISHED
