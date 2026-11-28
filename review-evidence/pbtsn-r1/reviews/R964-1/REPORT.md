[R964] NEGATIVE - exact head ef5e5ce1a6a79cfb317023e3067b89cb510a51db

# R964-1 independent external review: kebag-logic/tsn-c-stack PR #43 (issue #42, AEM-01)

- Exact head `ef5e5ce1a6a79cfb317023e3067b89cb510a51db`, tree `a8680cc0e56ad0c887aa1e39a549ad2f4a7dfc9a`.
- Scope reviewed: `79c4ba8..ef5e5ce` only (`aade92b`, `93ef150`, `ef5e5ce`). The `dev-linux` commits and the merge `79c4ba8` are not reviewed here.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/43#issuecomment-7237505793
- Prior public review findings on this PR: none exist. The PR carries two review-start comments, no review, no review comment and no finding. Nothing to resolve or retain.
- No other reviewer's report was read.

## Verdict

NEGATIVE. The code at this head is correct as far as this review could establish, and the main acceptance point holds: the model's 84 descriptors are byte-identical to the firmware generator's image, which I regenerated myself from the public generator. Seven MINOR findings remain open. They are in clause citations, one descriptor string, traceability, test sensitivity and documentation; none is a behaviour defect in the shipped C code.

What I established independently at the exact head:

| Claim | Result | Receipt |
|---|---|---|
| Validation kit, 27 gates | 27 of 27 rc 0 | `receipts/validate.log`, `receipts/validate-gates.json` |
| Planted defects | 538 caught, 0 escaped, 0 error; all 15 `pbaem-` plants and all 4 `entity-` configuration plants caught | `receipts/validate-mutation-lane-plants.txt` |
| Coverage of `src/pbaem.c` | 224/224 lines, 100 % of branches (101/101 with this host's compiler; the ratchet's 103/103 is the CI compiler's count) | `receipts/validate-coverage.log` |
| Address and undefined-behaviour sanitizers | 11 of 11 test binaries pass | `receipts/validate-clang-sanitizers-test.log` |
| RV32 Debug and Release on QEMU | rc 0, smoke exit status 0 in both | `receipts/baremetal.log`, `receipts/probe_rv32.txt` |
| RV32 golden is sensitive | a model plant and a golden plant each exit 92 in Debug and Release | `receipts/probe_rv32.txt` |
| Model equals the published firmware image dump | 84 of 84 identical, 8105 bytes, CRC-32 `0x1e668fba` | `receipts/aem-compare-reviewer.txt` |
| Model equals an image I regenerated with the public generator | 84 of 84 identical, 8105 bytes, CRC-32 `0x1e668fba`; without any pin the generator's hash-derived model ID is `0x001bc5c52e47a158` | `receipts/aem-regenerate-compare.txt` |
| Documented entity commands in `docs/POCKETBEAGLE.md` | all run and pass | `receipts/doc-commands.txt` |
| Hosted checks at this head | 4 jobs in 2 runs (push and pull_request), all executed, all success, none skipped | `receipts/hosted-checks.txt` |
| Published evidence packet | 23 of 23 files match the packet manifest | `receipts/evidence-manifest-check.txt` |

The regeneration used milan-fpga `58f7673b` with its packer gitlink `801ef228` and a configuration I wrote from public facts only (`scripts/reviewer_endstation_pb2_4x4.yaml`). It is not the author's unpublished file. That the output is identical, and that the unpinned hash equals the pinned model ID, shows the documented facts fully determine the image. In `receipts/aem-regenerate-compare.txt` the second comparison prints a different CRC only because it concatenates in the generator's directory order.

## Findings

### F1 - MINOR - Conformance, Docs - wrong Milan v1.2 clause numbers in the model's comments

- Where: `src/pbaem.c:190`, `:214`, `:231`, `:301`, `:319`; imprecise at `:264` and `:125`.
- Authority: Milan v1.2 table of contents, sections 5.3.2 to 5.3.12. The coding standard allows comments to carry only requirement IDs and clause references, so these lines are the per-descriptor clause trace. Issue #42 requires the descriptors to be "traced per clause".

| Line | Function | Cited | What the cited clause is | Correct clause |
|---|---|---|---|---|
| 190 | `stream` | Milan 5.3.6 | AVB_INTERFACE dynamic state | 5.3.3.4 (STREAM_INPUT and STREAM_OUTPUT) |
| 214 | `avb_interface` | Milan 5.3.4 | ENTITY dynamic state | 5.3.3.5 (AVB_INTERFACE) |
| 231 | `clock_source` | Milan 5.3.5 | AUDIO_UNIT dynamic state | 5.3.3.6 (CLOCK_SOURCE) |
| 301 | `control` | Milan 5.3.11 | CLOCK_DOMAIN dynamic state | 5.3.3.10 ("IDENTIFY" CONTROL), 5.3.12 for its state |
| 319 | `clock_domain` | Milan 5.3.2 | Configurations and descriptor trees | 5.3.3.11 (CLOCK_DOMAIN) |
| 264 | `stream_port` | Milan 5.3.3.9 | AUDIO_MAP | 5.3.3.7 (stream ports), with 5.3.3.9 for the absent input map |
| 125 | `named` | IEEE 7.2.2 | CONFIGURATION descriptor | 7.3.7 (localized string reference) |

- The IEEE 1722.1-2021 numbers at the other lines are right (7.2.1, 7.2.2, 7.2.3, 7.2.6, 7.2.8, 7.2.9, 7.2.11, 7.2.12, 7.2.13, 7.2.16, 7.2.19, 7.2.22, 7.2.32, 7.3.5, 7.4.23, Table 7-1). So are the Milan citations at lines 15, 20 and 44 and those in the docs, the tests and the requirement record.
- Impact: five of the model's six Milan citations beside a descriptor point at an unrelated clause. A reader checking the stream descriptor's 2 126 000 ns buffer against "5.3.6" finds gPTP state, not the rule (it is in 5.3.3.4).
- Required outcome: correct the seven citations.
- Verification: compare each comment against the Milan v1.2 contents; `python3 scripts/check_comments.py --selftest` still passes.

### F2 - MINOR - Conformance - LOCALE identifier `en-EN` is not a valid IEEE 1722.1-2021 7.2.11 identifier

- Where: `src/pbaem.c:251`; held in place by `tests/test_pbaem.cpp:220` and by the golden CRC in `examples/entity_roundtrip.c`.
- Authority: IEEE 1722.1-2021 7.2.11: a locale identifier is a language code, then optionally a region code "as defined by ISO 3166-1". `EN` is not an ISO 3166-1 code. Issue #42 acceptance: "The descriptors follow IEEE 1722.1-2021 clause 7".
- Origin: the value is the generator's default, `LOCALE_IDENTIFIER` at milan-fpga `58f7673b` `avdecc/aem_descriptors.py:186`. The generator accepts an `entity.locale` key that overrides it.
- Impact: the one descriptor string that does not follow clause 7. A controller that selects strings by locale cannot match it to a real locale. No stream behaviour depends on it.
- Required outcome: either a conforming identifier (for example `en-US` or `en`) in the bridge configuration or the generator, with the model, its test and the golden CRC updated together; or an explicit entry in `docs/DEVIATIONS.md` and `docs/POCKETBEAGLE.md` naming the deviation and the upstream issue, with the owner's decision.
- Verification: LOCALE descriptor 0 from octet 4; `scripts/compare_aem.py` still reports 84 of 84 against the regenerated image.

### F3 - MINOR - Docs - AEM-01 is traced to the import baseline instead of issue #42

- Where: `docs/TRACEABILITY.md:58` (origin column "Import baseline"), `docs/REQUIREMENTS.md:38-46` (no originating issue), `docs/requirements.json:995` (no `origin`), `scripts/requirement_records.py:16` (`ADDITIONAL_ORIGINS` has no AEM-01 entry, so `origin_link` falls through to "Import baseline").
- Authority: AEM-01 is new in this PR and originates from tsn-c-stack issue #42. `docs/REQUIREMENTS.md:15` says the first table is the import baseline and later tables add local issue requirements. `docs/VERIFICATION.md:208` says local issue requirements retain their linked origin. Every other local requirement names its issue (ACMP-10 to ACMP-13, ENTITY-01).
- Impact: the generated matrix states a false origin, and the traceability gate cannot notice because AEM-01 takes the legacy path.
- Required outcome: record the origin "tsn-c-stack issue 42" for AEM-01 in `requirements.json` and `ADDITIONAL_ORIGINS`, add the "AEM-01 originates from issue #42" sentence to its section, and regenerate `docs/TRACEABILITY.md`.
- Verification: `python3 scripts/traceability.py --selftest`; row AEM-01 links issue 42.

### F4 - MINOR - Tests - the input-format predicate and its stream bound survive reviewer probes

- Where: `src/pbaem.c:45-55` (`pbaem_input_format_supported`), `tests/test_pbaem.cpp:167-182`.
- Evidence: `scripts/probe_pbaem.py`, `receipts/probe_pbaem.txt`, `receipts/probe_absent_stream.txt`. Each probe changes one line in a scratch copy and runs the `pbaem` and `entity` test binaries. Five non-equivalent probes pass every test:

| Probe | Change | Consequence |
|---|---|---|
| `aaf-stream-bound-off-by-one-supported` | line 47 `>=` becomes `>` | An AAF format is supported on the absent input 5. `pbaem_set_input_format(&m, 5, ...)` then returns true and writes past `input_formats[5]`: `available_index` becomes `0x02006000`, `clock_source` 544, `identify` 5. The undefined-behaviour sanitizer reports index 5 out of bounds at line 71. |
| `aaf-ignore-samples-per-frame` | samples-per-frame bits dropped from the comparison | A 48 kHz format with, for example, 12 samples per PDU is accepted. |
| `aaf-ignore-format-field` | AAF format code dropped | A non-PCM32 code (float, 24-bit, 16-bit) is accepted. |
| `aaf-ignore-reserved-low` | low 12 reserved bits dropped | Nonzero reserved bits are accepted. |
| `aaf-ignore-subtype` | version and subtype octet dropped | A non-AAF subtype with the same remaining bits is accepted. |

- The only assertion on input 5 offers the CRF format, which the AAF branch refuses for another reason. Controls behave as expected: the bit-depth, up-to-bit, wrong-stream and output-bound probes are killed.
- Authority: AEM-01 ("each 48 kHz PCM32 base format of 1 to 8 channels"); `docs/CODING_STANDARD.md` ("Add assertions for malformed input, boundary values"); `CONTRIBUTING.md` (a runnable planted defect per regression); issue #42 ("full test coverage").
- Impact: line and branch coverage are 100 %, but a one-character slip in the only guard before an array write, and four ways of widening the accepted formats, would pass the whole kit. The head code itself is correct: at the exact head the absent input is refused and the model is unchanged.
- Required outcome: assertions, each with a registered plant, that input 5 refuses an AAF format and that a refused `pbaem_set_input_format(..., 5, ...)` leaves the model unchanged; and that an AAF input refuses another samples-per-frame value, another AAF format code, nonzero reserved bits and another subtype.
- Verification: rerun `scripts/probe_pbaem.py`; the five probes are killed. `python3 scripts/mutation.py --select pbaem-` catches the new plants.

### F5 - MINOR - Tests - "with the caller's identity" is asserted only for short strings and one model ID

- Where: `src/pbaem.c:59`, `:144`, `:151`, `:154-156`; `tests/test_pbaem.cpp:15-24`, `:69-84`.
- Evidence: `receipts/probe_pbaem.txt`. Five probes pass every test:
  - `name-copy-32`, `firmware-copy-32`, `group-copy-32`, `serial-copy-32`: each ENTITY string copy truncated from 64 to 32 octets. The test strings are 5 to 17 characters and the golden name is 21.
  - `model-id-constant`: `entity_model_id` ignores the caller. The unit test and the golden use the same model ID.
- Related: `init-keeps-old-state` (the clear in `pbaem_init` removed) is killed only by the golden round trip, and only because that example's uninitialised stack model happens to hold nonzero bytes. No test initialises a model that held earlier state.
- Authority: AEM-01 ("Serve each of the 84 descriptors ... with the caller's identity"); IEEE 1722.1-2021 7.2.1 (64-octet strings).
- Impact: a truncated entity name, firmware version, group or serial number, or a fixed model ID, would pass the kit.
- Required outcome: a test with 64-octet strings that have no terminator and a model ID different from the golden's, a test that re-initialises a model whose state fields were set, and a plant for each.
- Verification: rerun `scripts/probe_pbaem.py`; the five probes are killed, and `init-keeps-old-state` is killed by a `Pbaem.*` test.

### F6 - MINOR - Docs - the #41 exemption is not recorded where the gate's exemptions are documented

- Where: `docs/IMPORT.md:135-137` and `docs/VERIFICATION.md:43` describe only the merge of #29. `scripts/check_privacy.py:17` now exempts two commits.
- Authority: precedent commit `62d24a3`, "Record the merge of #29's one-line exemption in the verification and import docs and the change log". Commit `aade92b` changes only the script and the change log. This is documentation of the privacy rule, so it is not treated as wording.
- The exemption itself is sound: it names the exact commit `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`, lifts only the one-line rule, and that commit passes the identity pair and the content scan (`receipts/validate-privacy.log`: 98 commits, 596 blobs, 107 files, pass; 14 controls pass).
- Impact: the import record states one exempt merge while the gate has two; a reader auditing the exemptions from the docs misses one.
- Required outcome: name the merge of #41 beside the merge of #29 in both documents.
- Verification: read both documents against `TWO_LINE_MERGES`.

### F7 - MINOR - Docs, Conformance - `docs/POCKETBEAGLE.md` cites a configuration and suites that are not at the place it names

- Where: `docs/POCKETBEAGLE.md:49` ("The descriptors come from one end-station configuration in the board support repository"), `:88` ("The board support repository's AECP suite at this shape"), `:90` ("The board support repository's SRP suite").
- Evidence, read from the public board support repository on 2026-11-28:
  - Its default branch holds no bridge configuration. Branch `pb2-aecp-1` at `a5cd7c1e` holds `milan-linux/config/endstation_pb2_bridge.yaml`: one AAF input, one CRF input, one AAF output, `model_id_pin` `0x001BC50AC1000100`. That is not this 4x4 + CRF shape and not this model ID.
  - No public branch holds an SRP suite. The AECP suite there is written for the one-stream shape.
  - The author's own published handoff says the 4x4 configuration is uncommitted in that tree and the 4x4 suite changes are a patch series awaiting another lane.
- Impact: the conformance-by-clause table, which issue #42 relies on for the per-clause trace, points two rows at evidence a reader cannot find, and the design section names a source of the descriptors that currently yields a different image.
- Required outcome: either link each row to a published, commit-pinned configuration and suite, or state what is true today (the 4x4 configuration and its suites are not yet published; the image evidence is the generator at a named commit and the dump in the evidence packet).
- Verification: every link resolves to the named shape; regenerating from the linked configuration reproduces CRC-32 `0x1e668fba`.

## Residue (wording only; does not affect the verdict)

- RES-1: `scripts/baremetal.py:39`, message `'freestanding build must compile all three cores'`. The set on line 38 now has four files. Exact fix: `'freestanding build must compile all four cores'`.
- RES-2: "base format of 1 to 8 channels" in `docs/REQUIREMENTS.md:46`, `docs/requirements.json:996`, `docs/POCKETBEAGLE.md:40-41`, `CHANGELOG.md:5` and the PR body. Milan v1.2 6.2 defines Base formats for 1, 2, 4, 6 and 8 channels only; the model also accepts 3, 5 and 7, as 6.5 permits with the up-to bit. Exact fix: "each 48 kHz PCM32 AAF format of 1 to 8 channels with six samples per PDU, which includes every 48 kHz Base format". The behaviour and the 6.4 claim are unchanged.

## Suggestions (do not affect the verdict)

- S1: the integration contract of `pbaem.h` is only partly written down (`docs/ARCHITECTURE.md:13`, `docs/POCKETBEAGLE.md:54-58`). `docs/PORTING.md` does not mention it. Worth stating: the caller writes `available_index` and `identify` directly; identity strings are 64 octets, zero padded and copied verbatim; pointers must be valid; one `pbaem_descriptor` call uses about 500 bytes of stack on RV32 (frame 512 Debug, 496 Release).
- S2: `docs/DEVIATIONS.md` DEV-01 still says AEM enumeration is outside these cores. It remains true of AECP, but the library now supplies a descriptor model; one clause would avoid the apparent contradiction with `README.md:3-4`.
- S3: three points of the image that Milan leaves open and IEEE 1722.1-2021 only recommends, for the generator's owner: all six `clock_source_identifier` fields are zero (7.2.9.3 describes a per-source default from the MAC address and an index); `object_name` is filled where the standard says it should be left blank with a localized description (7.2.6, 7.2.9, 7.2.16, 7.2.22); every AAF input carries CLOCK_SYNC_SOURCE, which the note to Table 7-9 reserves for dedicated media clock streams.
- S4: `scripts/check_privacy.py:60` picks `next(iter(TWO_LINE_MERGES))`. With two entries the set order varies between runs, so each run exercises one exempt commit at random. Iterate over both.
- S5: in the published `aem-firmware-image-4x4.txt`, the label columns of three rows disagree with the descriptors' own indices (CRF STREAM_INPUT labelled index 0, AUDIO_MAP 2 and 3 labelled 0 and 1). The descriptor bytes are right and equal the model's. The two published dump files are therefore not identical as text although `aem-compare.txt` says 84 of 84.

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F7) | `src/pbaem.c` and `include/pbaem.h` field by field against IEEE 1722.1-2021 7.2.1, 7.2.2, 7.2.3, 7.2.6, 7.2.8, 7.2.9, 7.2.11, 7.2.12, 7.2.13, 7.2.16, 7.2.19, 7.2.22, 7.2.32, 7.3.5.2, 7.3.7, 7.4.23 and Milan v1.2 5.3.2, 5.3.3.1 to 5.3.3.11, 5.3.8.1, 5.3.10.1, 5.4.2.7, 5.4.2.15, 6.2, 6.4, 6.5, 7.2.2, 7.2.3, 7.3.2, Tables 4.4, 6.2 and 7.1; `configs/pocketbeagle.yaml` and its generated files; byte comparison with the published image and with an image regenerated from the public generator | R964-1 | `ef5e5ce1a6a79cfb317023e3067b89cb510a51db` |
| RTL | CLEAN | The delta holds no HDL (4 `.c`, 2 `.cpp`, 3 `.h`, 8 `.py`, 10 `.md`, 2 `.json`, 1 `.yaml`, 1 `.txt`, 1 ratchet). Hardware-facing artifact examined instead: the RV32 freestanding build, its imports, unresolved symbols, stack frames and QEMU smoke in Debug and Release, with two fault probes | R964-1 | `ef5e5ce1a6a79cfb317023e3067b89cb510a51db` |
| Robustness | CLEAN | Every index, length and capacity guard in `src/pbaem.c`; refusal without writing; absent types, indices and streams at the head (`receipts/probe_absent_stream.txt`); address and undefined-behaviour sanitizer run; static analysis gate; boundary gate; the exact-commit privacy exemption, its identity and content checks | R964-1 | `ef5e5ce1a6a79cfb317023e3067b89cb510a51db` |
| Tests | UNCLEAN (F4, F5) | `tests/test_pbaem.cpp`, `tests/test_entity.cpp`, `examples/entity_roundtrip.c`, `examples/rv32/smoke.c`, `tests/mutations.json` (538 entries, 15 `pbaem-`, 5 configuration), `tests/coverage.ratchet`; full kit run; 21 reviewer probe runs (19 mutants of which 10 survive and 9 are killed, one unmodified control, one equivalent control); 2 RV32 probes | R964-1 | `ef5e5ce1a6a79cfb317023e3067b89cb510a51db` |
| Docs | UNCLEAN (F1, F3, F6, F7) | `docs/POCKETBEAGLE.md` (every clause, figure and command; the 59.648 Mb/s sum and the 217, 121 and 29 octet sizes recomputed from Milan Table 4.4), `docs/REQUIREMENTS.md`, `docs/requirements.json`, `docs/TRACEABILITY.md`, `docs/TESTS.md`, `docs/VERIFICATION.md`, `docs/ENTITY_YAML.md`, `docs/ARCHITECTURE.md`, `docs/CODING_STANDARD.md`, `docs/IMPORT.md`, `docs/DEVIATIONS.md`, `README.md`, `CHANGELOG.md`, PR body; source comments in the delta against the comment rule | R964-1 | `ef5e5ce1a6a79cfb317023e3067b89cb510a51db` |

Comment rule: no new source comment in the delta carries a bench label, lane name, review round, reviewer ID or issue-comment ID. The delta's comments are SPDX lines, `REQ: AEM-01` and clause references; the one script comment (`scripts/check_privacy.py:16`) states the behaviour and reason with issue numbers. No bench device identity appears in the delta; the MAC `02:00:00:00:00:01` is the generator's placeholder.

## Limits

- Compilers differ from the CI environment: this run used GCC 16.2.1, Clang 23.1.5 and an RV32 GCC 16.2.0, with GoogleTest 1.14.0 and the Clang 18.1.3 lexer pinned (`receipts/environment.txt`). Object hashes and branch counts therefore differ from the author's receipts; every gate passed.
- The Mermaid diagrams were not rendered here. The hosted `quality` job ran the kit with `--graphs` and succeeded.
- The regenerated image comes from a reviewer-written configuration. The author's configuration file is not published, so I could not regenerate from it.
- IEEE 1722-2016 was not consulted directly. The AAF and CRF format words were checked against Milan v1.2 Tables 6.2 and 7.1, and the up-to bit against Milan 6.5.
- The bridge receipts in the evidence packet (`bridge-*.log`, `bridge-*-plants.txt`) concern patches to another repository and were not examined.
- No hardware, board, bench device or simulator beyond QEMU was used. Physical calibration was not run. Nothing here is hardware proof.
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts, the hosted jobs above and this review's own runs.
- The clone was left at the exact head: worktree and index equal `HEAD`, 107 tracked files with no blob or mode difference, no gitlinks, no untracked or ignored files after removing the interpreter cache my runs wrote (`receipts/clone-state.txt`). All probes ran on scratch copies.

## Pending manager duties

- Carry RES-1 and RES-2 to the residue checklist.
- Reconcile `aade92b` with the exemption being added on `main` separately; both edit the same two lines of `scripts/check_privacy.py`. The owner's decision on the exemption is still open in the PR body.
- Build and validate the current-dev merge candidate at the merge turn and link its receipts; own hosted acceptance.
- Check the published evidence packet's wording: `author/REPORT.md` line 3 and `author/receipts/INDEX.md` line 3 are headed as private ("Not for any public repository"), and `author/REPORT.md` line 7 and `author/round1/HANDOFF-r1.md` lines 1, 2 and 31 name a bench board label and a bench device label. Confirm these were meant to be public; I have not repeated the labels here.
- The PR is a draft against `main`. Its body should reflect the outcome of F2 and F7 once decided.

## Packet contents

Scripts (portable; paths are arguments): `scripts/env.sh`, `scripts/run_validate.sh`, `scripts/run_baremetal.sh`, `scripts/probe_pbaem.py`, `scripts/dump_aem.c`, `scripts/compare_aem.py`, `scripts/absent_stream.c`, `scripts/regen_image.py`, `scripts/reviewer_endstation_pb2_4x4.yaml`. Receipts are under `receipts/` and listed with their hashes in `MANIFEST.sha256`.

R964-1 FINISHED
