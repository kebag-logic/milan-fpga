[R963] NEGATIVE - exact head ef5e5ce1a6a79cfb317023e3067b89cb510a51db

# R963-1 independent review: kebag-logic/tsn-c-stack PR #43 / issue #42 (AEM-01)

- Role: internal independent reviewer, cleared context, own detached clone.
- Exact head `ef5e5ce1a6a79cfb317023e3067b89cb510a51db`, tree `a8680cc0e56ad0c887aa1e39a549ad2f4a7dfc9a`. Clone verified byte-exact after all probes (`receipts/clone-restore-check.txt`).
- Scope: only this lane's commits `79c4ba8..ef5e5ce`: `aade92b` (privacy-gate exemption of merge `5a07d9b7`), `93ef150` (PocketBeagle entity configuration), `ef5e5ce` (pbaem AEM model). The `dev-linux` commits are out of scope.
- Reconstructed in order: CONTRIBUTING.md (the repository has no AGENTS.md), README and docs, the issue #42 body (no maintainer or manager comments exist on #42), the PR #43 body, the requirement and traceability records, the diff and its history, then the public evidence packet `milan-fpga@2a26108/review-evidence/pbtsn-r1`. Neither the issue nor the PR has any manager evidence comments other than the two review-start notices.

## Verdict

NEGATIVE. There are three open MINOR findings (F1 to F3); there is no BLOCKER and no MAJOR. The core acceptance holds at this head:

- The 84 descriptors (8105 bytes) that `pbaem` produces at this head are byte-identical to the published firmware-generator dump, keyed by each descriptor's own header. CRC-32 is `0x1e668fba`.
- The golden fails on both Linux and RV32 when one descriptor byte drifts.
- `src/pbaem.c` has 100% line and branch coverage.
- The full planted-defect campaign catches all 538 plants.
- The privacy exemption is exact and narrow.

## Findings

### F1: MINOR. AEM-01's traceability names the wrong origin (Docs, Conformance)

- **Where:** `docs/TRACEABILITY.md:58`, generated from:
  - `scripts/requirement_records.py:16-33` (`ADDITIONAL_ORIGINS` has no AEM-01 entry);
  - `docs/requirements.json:995` (AEM-01 has no `origin`);
  - `docs/REQUIREMENTS.md:38-46` (no origin sentence).
- **Authority:**
  - Issue #42 is where AEM-01 is introduced: "A requirement for an AEM descriptor model in tsn-c-stack, AEM-01".
  - Repository precedent: every requirement added since the import names its issue. ACMP-11, ACMP-12 and ACMP-13 are in `ADDITIONAL_ORIGINS`, and `REQUIREMENTS.md:50` says "ACMP-13 originates from issue #32".
  - CONTRIBUTING: "A protocol change updates its requirement, tests and traceability".
- **Evidence:** `origin_link()` (`scripts/requirement_records.py:305-314`) falls through to `'[Import baseline](REQUIREMENTS.md)'` for a non-imported ID with no origin. So the generated row states that AEM-01 came from the milan-fpga import baseline. The traceability gate passes because it does not require an origin for these IDs.
- **Impact:** the generated traceability artifact gives a false origin for the PR's one new requirement. The issue that froze AEM-01's acceptance cannot be reached from the trace.
- **Required outcome:**
  - Add AEM-01 → `tsn-c-stack issue 42` (`https://github.com/kebag-logic/tsn-c-stack/issues/42`) to `ADDITIONAL_ORIGINS` and to the AEM-01 record in `docs/requirements.json`.
  - Add "AEM-01 originates from issue #42" to the REQUIREMENTS section.
  - Regenerate TRACEABILITY.md.
- **Verification:** `python3 scripts/traceability.py --selftest ...` passes, and the AEM-01 row of `docs/TRACEABILITY.md` links issue 42.

### F2: MINOR. The AAF input-format predicate's "PCM32 base format" refusals are untested (Tests, Robustness, Conformance)

- **Where:** `src/pbaem.c:53-54` (`pbaem_input_format_supported`) and `tests/test_pbaem.cpp:167-182`.
- **Authority:**
  - AEM-01 (`docs/requirements.json:995`): "Accept on an AAF input each 48 kHz PCM32 base format of 1 to 8 channels".
  - Milan v1.2 6.2/6.4, as cited by the model.
  - CONTRIBUTING: "A regression needs a failing assertion and a runnable planted defect".
- **Evidence:** reviewer mutation probe `scripts/format_mutants.sh`, receipt `receipts/format-mutants.txt`. Four non-equivalent mutants of the predicate SURVIVE every `pbaem_tests` and `entity_tests` case:
  - ignoring the AAF format byte, which accepts FLOAT32, INT24 and other containers;
  - ignoring samples_per_frame, which accepts non-base formats such as 12 or 64 samples per frame;
  - ignoring the subtype byte;
  - ignoring the 12 reserved low bits.

  A control mutant that ignores bit_depth is KILLED. The tests refuse only one value per field for nsr, bit_depth, channel count and the ut bit. The 15 campaign plants and the golden do not reach these fields: the golden only reads the init defaults.
- **Impact:** a regression that widens SET_STREAM_FORMAT acceptance to non-PCM32 or non-base formats would pass every gate. This is the exact property AEM-01 states. The code at this head is correct; the protection is missing.
- **Required outcome:** in `Pbaem.StreamFormats`, add refusals on an AAF input, each with its own planted defect in `tests/mutations.json`:
  - a format byte other than INT_32BIT, e.g. `0x0205012002006000`;
  - samples_per_frame other than 6, e.g. `0x020502200200c000`;
  - a non-AAF subtype or the vendor bit, e.g. `0x0305022002006000` or `0x8205022002006000`;
  - a reserved bit, e.g. `0x0205022002006001`.

  Update `docs/TESTS.md` and the plant counts in VERIFICATION, CHANGELOG and the PR body.
- **Verification:** rerun `scripts/format_mutants.sh <clone> <work>`; all four mutants are KILLED. `python3 scripts/mutation.py --select pbaem-` catches the new plants.

### F3: MINOR. The RV32 gate's diagnostics still describe three cores (Tests, Docs)

- **Where:**
  - `scripts/baremetal.py:39`: `'freestanding build must compile all three cores'`. The check on line 38 now requires four files, `adp.c`, `acmp.c`, `maap.c` and `pbaem.c`.
  - `scripts/baremetal.py:90`: the smoke log summary `'ADP, ACMP and MAAP smoke checks: rc 0'`. The smoke image now also runs `entity_check_aem`.
- **Authority:** the same commit updated the sibling messages on lines 64-65 ("all five generated entities") and in `scripts/coverage.py:356` ("five required files"). This is the verification guide's own gate output.
- **Impact:** a failing RV32 gate names the wrong file set, and the smoke log understates what was executed. No measurement changes. This is classed MINOR rather than RESIDUE because the defect is in gate code, not prose.
- **Required outcome:** make line 39 name the four required sources (e.g. "all three cores and the AEM model"), and make line 90 include the PocketBeagle AEM image.
- **Verification:** inspect `scripts/baremetal.py:38-39,90`; `python3 scripts/baremetal.py --work build-rv32 --jobs 16` passes.

### Suggestions (do not affect the verdict)

- **S1 (Docs), `docs/POCKETBEAGLE.md:44`.** "An input refuses a format that drops a mapped channel (Milan v1.2 5.4.2.7)" describes the firmware's SET_STREAM_FORMAT. `pbaem_set_input_format` has no map state and accepts any 1 to 8 channel base format. Say that this is the firmware's AECP behaviour, as the clause table does on line 88.
- **S2 (Docs, Tests), `examples/entity_roundtrip.c:313-314` and `docs/POCKETBEAGLE.md:57-58`.** Record the golden's provenance next to the CRC: generator revision `milan-fpga 58f7673b` and the generator configuration and identity. A later generator change could then be traced to a golden update.
- **S3 (Tests), `scripts/check_privacy.py:60`.** The self-test picks `next(iter(TWO_LINE_MERGES))`. With two members, the merge it picks depends on the hash seed (`receipts/privacy-selftest-seed.txt`: 5 of 8 seeds pick `5a07d9b7`, 3 of 8 pick `d7e6a2a1`), so each run exercises only one exemption. Iterate over both. The real gate is unaffected (`receipts/privacy-exemption-probe.txt`).
- **S4 (Robustness), `src/pbaem.c:339`.** `pbaem_descriptor` stages each descriptor in a 452-byte local buffer: about 496 to 512 bytes of stack on RV32 (`-fstack-usage`). State this in the porting guide for small control CPUs.
- **S5 (Tests), `tests/test_pbaem.cpp:131`.** `std::snprintf` is used without `<cstdio>`. It compiles only through transitive includes.
- **S6 (evidence), `author/receipts/aem-firmware-image-4x4.txt`.** The dump's index column prints `5 0` for STREAM_INPUT 4 and `23 0` and `23 1` for AUDIO_MAP 2 and 3. The descriptor headers carry 4, 2 and 3, and a naive key on the column finds a duplicate. The bytes are identical once keyed by header. Correct the dump tool, or explain the column, in the next evidence packet.
- **S7 (Conformance), `src/pbaem.c:251`.** The locale identifier is `en-EN`, and `EN` is not a region subtag. Because of the byte-identity rule, any change must be made in the generator and the model together.

## Evidence

### Conformance

I walked every descriptor writer against the IEEE 1722.1-2021 clause 7.2 layouts:

| Descriptor | Clause | Checked |
|---|---|---|
| ENTITY | 7.2.1 | 312 bytes: capabilities `0xC588` and talker/listener `0x4801` decoded, string references 2/0, configuration count |
| CONFIGURATION | 7.2.2 | 8 top-level counts at offset 74 |
| AUDIO_UNIT | 7.2.3 | 148 bytes; port counts, 48 kHz rate list |
| STREAM_INPUT/OUTPUT | 7.2.6 | formats_offset 138; redundant_offset equals the length; buffer_length; class A and CLOCK_SYNC flags |
| AVB_INTERFACE | 7.2.8 | 102 bytes; interface_flags 7, the gPTP dataset, port 1 |
| CLOCK_SOURCE | 7.2.9 | LOCAL_ID flag; INTERNAL or INPUT_STREAM type; location type and index |
| LOCALE / STRINGS | 7.2.11 / 7.2.12 | `en-EN` with 1 string block (S7); 7 strings × 64 octets = 452 bytes |
| STREAM_PORT | 7.2.13 | clusters, maps, port_flags |
| AUDIO_CLUSTER | 7.2.16 | signal_type, latencies, MBLA format |
| AUDIO_MAP | 7.2.19 | mappings_offset 8 |
| CONTROL | 7.2.22 | IDENTIFY, LINEAR_UINT8 value block at offset 104 |
| CLOCK_DOMAIN | 7.2.32 | sources list at offset 76 |

- The total is 84 descriptors, consistent with `PBAEM_DESCRIPTORS`.
- The AAF base and ut-family formats and the CRF format `0x041060010000BB80` (48 kHz, 96-sample interval, 1 timestamp per PDU) decode consistently with Milan 6.2/6.4/7.3.2 as cited.
- Byte identity:
  - `scripts/compare_aem.py`; receipts `compare-firmware-vs-head-pbaem.txt` and `pbaem-dump-at-head.txt`.
  - The dump was produced at this head by `scripts/dump_pbaem.c` with the golden's identity.
  - It is byte-equal to the author's pbaem dump, and per descriptor equal to the published firmware dump.
- The documented reservation total is reproduced exactly (`scripts/tspec_arith.py`, `receipts/tspec-arith.txt`): 59.648 Mb/s, under 75 Mb/s. This assumes the doc's TSpec sizes, 42 octets of overhead and the 46-octet minimum payload.
- The ADP fields of the entity configuration equal the AEM ENTITY fields (model ID `0x001BC5C52E47A158`, capabilities and counts), and the generated golden passes `entity_yaml.py --check`.

### RTL / target

- The delta contains no HDL, constraint or RTL files.
- Target view: RV32 Debug and Release build, audit and execute under QEMU, rc 0 (`receipts/rv32-results.json`).
- The `pbaem.c` object imports only `memcpy`, `memset`, `__udivsi3` and `__umodsi3`, all within the allowed set. It uses the mandatory freestanding flags.
- The golden-drift probe fails the RV32 smoke (`receipts/probe-golden-result.txt`, `receipts/probe-golden.diff`).

### Robustness

- I inspected the bounds:
  - absent types and indices return 0;
  - a short destination returns 0 and writes nothing (staged buffer, then `memcpy`);
  - a refused format or source leaves the model unchanged;
  - `number()` handles suffixes up to 99, and the largest is 23;
  - every static string is 64 octets or fewer.
- The probes are F2 and S4.

### Tests

- Full campaign `mutation.py --jobs 10`: `{"CAUGHT": 538, "ESCAPED": 0, "ERROR": 0}` (`receipts/mutation-summary.txt`, including all 15 `pbaem-` plants and the 5 `entity-` plants).
- GCC Debug coverage build: all ctest cases pass; `coverage.py` passes with `src/pbaem.c` at 224/224 lines and 101/101 branches (`receipts/coverage-gcc16.txt`). The ratchet records 103 branches; the branch denominator is compiler-dependent and the ratchet compares fractions.
- Sanitizer build passes.
- `static_analysis.py`, `mutation_selftest.py` and 16 of the 17 validate prefix gates pass with the pinned toolchain. The conditionals gate passes with a substitute clang++ (`receipts/gates-summary.txt`).
- The golden probe shows the hosted `Pbaem` unit tests do not see a STRINGS drift, but `EntityYaml.AemImageRoundTrip` does (code 92).
- The privacy exemption probe:
  - the base rule fails `5a07d9b7` and the head rule passes it;
  - a near-miss hash is still refused;
  - a foreign identity on the exempt hash is still refused;
  - the content scan is clean.

### Docs

- Read and checked against the code: `docs/POCKETBEAGLE.md`, the REQUIREMENTS, TESTS, TRACEABILITY, VERIFICATION, ENTITY_YAML, ARCHITECTURE and CODING_STANDARD deltas, the README, the CHANGELOG and the PR body.
- Counts are consistent: 84 descriptors, 15 + 1 new plants, 533 + 5 = 538 plants, 27 gates, and the test-line anchors.
- Comment rule: no lane labels, bench labels, review rounds, reviewer IDs or issue-comment IDs appear in the delta's source comments. Bench device identities are absent; the identities are demonstration values (`02:00:00:00:00:01`, `0x020000fffe000001`), and the public product name PocketBeagle is used as allowed.
- The repository links resolve to public repositories.

### Hosted (read-only; acceptance is the manager's)

At the exact head, the push run 46131939087 and the pull_request run 46132130495 both executed their `quality` (validate.py with graphs) and `bare-metal` jobs, with conclusion success (`receipts/hosted-check-runs.txt`). No job was skipped.

### Prior public findings

PR #43 and issue #42 carry no prior review findings, only the two review-start notices. Nothing needs to be resolved or retained.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `src/pbaem.c`, `include/pbaem.h`, `configs/pocketbeagle.yaml`, the generated entity_config, the firmware dump comparison, the AEM-01 record and clauses | R963-1 | ef5e5ce1a6a79cfb317023e3067b89cb510a51db |
| RTL | CLEAN | delta file list (no HDL), RV32 Debug and Release objects and imports, QEMU smoke, golden-drift probe on RV32 | R963-1 | ef5e5ce1a6a79cfb317023e3067b89cb510a51db |
| Robustness | UNCLEAN (F2) | `pbaem_descriptor` bounds and short-destination path, setters' refusal paths, the format predicate mutants, stack use | R963-1 | ef5e5ce1a6a79cfb317023e3067b89cb510a51db |
| Tests | UNCLEAN (F2, F3) | `tests/test_pbaem.cpp`, `tests/test_entity.cpp`, `examples/entity_roundtrip.c`, `tests/mutations.json`, the coverage ratchet, the 538-plant campaign, reviewer probes, gate scripts | R963-1 | ef5e5ce1a6a79cfb317023e3067b89cb510a51db |
| Docs | UNCLEAN (F1, F3) | `docs/POCKETBEAGLE.md`, REQUIREMENTS, TRACEABILITY, TESTS, VERIFICATION, ENTITY_YAML, ARCHITECTURE, CODING_STANDARD, README, CHANGELOG, PR body, comment rule | R963-1 | ef5e5ce1a6a79cfb317023e3067b89cb510a51db |

## Real limits

- No IEEE 1722.1-2021, IEEE 1722-2016 or Milan v1.2 text was available to the reviewer.
  - The descriptor checks rest on each layout's offset and length consistency, and on the decoded field values against the cited clauses.
  - The Milan subclause numbers (5.3.3.9, 5.3.10.1, 5.4.2.7, Table 4.4 octet values) were not verified against the text.
- The firmware generator was not re-run. Byte identity is established against the published firmware dump (`aem-firmware-image-4x4.txt`, generator `milan-fpga 58f7673b` per the author's index).
- The local environment differs from CI:
  - GCC 16.2.1 and Python 3.14;
  - host Clang 23 for the clang C++ builds, because pinned Clang 18 cannot parse the GCC 16 libstdc++ headers;
  - cppcheck 2.22.0;
  - the graphs gate was not run (no Mermaid CLI).
- No manager source bank exists at this head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts, plus these reviewer runs.
- Physical calibration was NOT RUN. No board, bench or hardware evidence exists, and field skips are not hardware proof.

## Pending manager duties

- Reconcile `scripts/check_privacy.py` (the `TWO_LINE_MERGES` line, its comment and the printed message) with the separate exemption being added on main. The two edits touch the same lines.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn. Source base is `79c4ba8`; live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`. Link the receipts on the PR.
- Own hosted and act acceptance at the exact head.
- Carry S1 to S7 as optional follow-ups. No RESIDUE items are raised.

R963-1 FINISHED
