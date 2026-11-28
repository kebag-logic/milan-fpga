[R964] POSITIVE - exact head ebaac61dfa3c83f9c6663ce1c361bf79f395f704

# R964-3 independent external review: kebag-logic/tsn-c-stack PR #43 (issue #42, AEM-01), round 3

- Exact head `ebaac61dfa3c83f9c6663ce1c361bf79f395f704`, tree `e241f4d87493070283030f71a2c495998b9151c5`.
- Delta judged: `40c3111..ebaac61`, two commits. `9a0de3c` changes `tests/test_pbaem.cpp`, `tests/mutations.json`, `CHANGELOG.md`, `docs/TESTS.md`, `docs/TRACEABILITY.md` and `docs/VERIFICATION.md`. `ebaac61` changes `docs/POCKETBEAGLE.md` only.
- Scope: narrow re-review of my round-2 finding F1, the plant-coverage claim and the residues. Code the delta does not touch keeps its R964-2 and R964-1 verdicts.
- Review start: https://github.com/kebag-logic/tsn-c-stack/pull/43#issuecomment-7238238128
- Order followed: CONTRIBUTING.md (there is no AGENTS.md), the docs, issue #42 (body only; it has no comments), the PR body, the delta, the round-3 evidence packet, my own runs and probes, then the prior reports. See "Reading order" under Limits for one slip.

## Verdict

POSITIVE. There is no open BLOCKER, MAJOR or MINOR finding.

R964-2 F1 is closed at its cause. Each of bits 53, 54 and 55 of the AAF format word is now refused by its own assertion, and each has its own planted defect that the campaign catches by that assertion. The plant-coverage claim now names the fields, and every field it names has a caught plant. The model, the golden CRC `0xd891cd2f` and the model ID `0x001BC5C52E47A158` are unchanged.

One residue is retained (RES-1, evidence packet wording). Two suggestions are recorded. Neither affects the verdict.

## What I established at the exact head

| Claim | Result | Receipt |
|---|---|---|
| Validation kit, 27 gates | 27 of 27 rc 0 | `receipts/validate.log`, `receipts/validate-gates.json` |
| Planted defects | 556 caught, 0 escaped, 0 error: 551 core and 5 generated configuration plants. Same 556 names and verdicts as the author's round-3 receipt | `receipts/validate-mutation-lane-plants.txt` |
| The six new plants | each CAUGHT, and each registered needle is in its failure text | `receipts/validate-mutation-lane-plants.txt` |
| My round-2 probe `aaf-ignore-reserved-high` | KILLED by `Pbaem.AafFieldRefusals` (it survived in round 2) | `receipts/probe_pbaem.txt` |
| One probe per bit outside the channel count | 54 of 54 KILLED; each fails the one-bit loop, and bits 0, 11, 52 to 56 and 63 also fail a named assertion | `receipts/probe_pbaem.txt`, `receipts/probe_pbaem.json` |
| All reviewer probes | 83 runs: 81 mutants KILLED; the unmodified control and the equivalent control pass, as intended | `receipts/probe_pbaem.txt` |
| Head refuses the 224 words that differ from a valid format only in bits 53 to 55 | offered 224, supported 0, stored 0 | `receipts/probe_reserved_high.txt` |
| Model, golden and model ID unchanged | `src/pbaem.c`, `include/pbaem.h`, `examples/entity_roundtrip.c` and the three PocketBeagle configuration files have the same blob IDs at `40c3111` and `ebaac61` | `receipts/aem-regenerate-compare.txt` |
| Model equals an image regenerated from the public generator | 84 of 84 descriptors, 8105 octets, CRC-32 `0xd891cd2f`; ENTITY model ID `0x001bc5c52e47a158` | `receipts/aem-regenerate-compare.txt`, `receipts/aem-model-at-head.txt` |
| Coverage of `src/pbaem.c` | 224/224 lines, 100 % of branches (101/101 with this host's compiler; the author's 103/103 is the CI compiler's count) | `receipts/validate-coverage.log` |
| Sanitizers | 11 of 11 test binaries pass | `receipts/validate-clang-sanitizers-test.log` |
| Traceability, inventory, needles | 48 requirements, 211 test declarations, 556 plants; needle audit passes | `receipts/validate-traceability.log`, `receipts/validate-test-inventory.log`, `receipts/validate-needles.log` |
| Privacy | 109 commits, 628 historical blobs, 107 files, pass; 17 self-test controls pass | `receipts/validate-privacy.log`, `receipts/validate-privacy-selftest.log` |
| RV32 Debug and Release on QEMU | rc 0 in both; the smoke summary names the five entity round trips and the PocketBeagle AEM image | `receipts/baremetal.log` |
| Hosted checks at this head | 4 jobs in 2 runs (push and pull_request), every job and step executed and succeeded, none skipped | `receipts/hosted-checks.txt` |
| Evidence packet, round 3 | 10 of 10 `author-r3` files match the packet manifest | `receipts/evidence-manifest-check.txt` |

## R964-2 F1 at this head: CLOSED

F1 was: bits 53 to 55 of the AAF format word are refused by the code but checked by no test, and the plant claim "field by field" is overstated.

| Required outcome | State | Evidence at `ebaac61` |
|---|---|---|
| Assert that an AAF input refuses a valid format with a bit of 53 to 55 set | DONE | `tests/test_pbaem.cpp:242-247`: `0x0225022002006000`, `0x0245022002006000` and `0x0285022002006000` are refused on each of the four AAF inputs, each under its own message. Each word differs from the valid word in exactly that one bit. |
| Register a plant for it | DONE, one per bit | `tests/mutations.json:8898`, `:8911`, `:8924`: `pbaem-ignore-reserved-bit-53`, `-54` and `-55` each drop one bit from both sides of the comparison. Each is caught by its named assertion in my campaign run. |
| Update the counts | DONE | `docs/TESTS.md:214` and `:221` list the six new plants; the 33 `pbaem-` names there equal the registry. `docs/VERIFICATION.md:24` says 551 core plants: 551 + 5 = 556 registered. `CHANGELOG.md:5` says thirty-three: 33 `pbaem-` plants. The PR body says 33 and 556. |
| The plant claim states what the plants cover | DONE | `CHANGELOG.md:5` and the PR body name the fields. Each named field has a caught plant: subtype (2), rate (1), the up-to bit (1), bits 53, 54 and 55 (3), format code (1), bit depth (1), channel count (2), samples per frame (1), low reserved bits (2). The CRF input, the absent input, the four identity strings, the model ID and re-initialization have theirs too. |

The cause is closed, not only the example. A change that stops comparing any single bit outside the channel count now fails a test: all 54 one-bit probes are killed. The PR body's sentence "Every bit outside the channel count is refused when flipped alone" is therefore true and tested (`tests/test_pbaem.cpp:248-254`).

The new plants for the bit depth and the up-to bit (`tests/mutations.json:8937`, `:8950`) are caught by "24-bit depth is refused" and "the family entry is not a stream format" (`tests/test_pbaem.cpp:176-177`).

## Other prior findings at this head

### R964-2 (external, 7238106277)

| Item | State | Evidence at `ebaac61` |
|---|---|---|
| F1 | CLOSED | Above. |
| RES-1 packet names a receipts directory under another name | RETAINED as RES-1 below | The published round-2 files are unchanged, and the round-3 files carry a new pointer of the same kind. |
| S1 golden identity incomplete on the page | TAKEN | `docs/POCKETBEAGLE.md:66` adds the clock identity, equal to the entity ID, and the empty serial number and group name. This equals `examples/entity_roundtrip.c:290-297`, and a model dump with exactly that identity equals the regenerated image. |
| S2 one loop over the 54 bits | TAKEN | `tests/test_pbaem.cpp:248-254`. |
| S3 plants for bit depth and the up-to bit | TAKEN | Both registered and caught. |
| S4 name the one branch | TAKEN | `docs/POCKETBEAGLE.md:55`. Of the five public branches of the board support repository today, only `pb2-aecp-1` holds an end-station configuration, with one listener and one talker (`receipts/bsp-public-state.txt`). |

### R963-2 (internal, 7238076326)

| Item | State | Evidence at `ebaac61` |
|---|---|---|
| F1 step 1: refuse a reserved bit of 53 to 55, with its own plant | CLOSED | As R964-2 F1. Three assertions and three plants, where one of each was asked. |
| F1 step 2: plants for bit depth and the up-to bit | CLOSED | `pbaem-ignore-bit-depth` and `pbaem-ignore-ut`, each caught by the assertion that step named. |
| F1 step 3: `docs/TESTS.md` and the counts | CLOSED | As R964-2 F1. Step 4, narrowing the claims, was the alternative and is not needed. |
| RES-1 | RETAINED as RES-1 below | Same residue as R964-2 RES-1. |
| S1 assert bit 11 of the low reserved field | TAKEN | `tests/test_pbaem.cpp:240-241`, plant `pbaem-ignore-reserved-bit-11` at `tests/mutations.json:8885`, caught. My round-2 sub-field probe for bits 1 to 11 is now killed. |
| S2 golden identity | TAKEN | As R964-2 S1. |
| S3 say that regenerating needs the `protocol-processor` submodule | TAKEN and verified | `docs/POCKETBEAGLE.md:58`. The gitlink at `58f7673b` is `801ef228`, and it holds `hdl/aecp/desc/gen_desc_image.py`, which the image generator imports (`receipts/generator-submodule.txt`). With only that submodule present, the generator reproduces the 84 descriptors. Without it, the generator stops and names it (`receipts/aem-regenerate-compare.txt`). |

All round-1 findings of both reviewers were closed at `40c3111` (R964-2 report). The delta touches none of their causes.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### RES-1 - RESIDUE - Docs - the evidence packet points at receipts under names that are not published

- Where (evidence packet on branch `pbtsn-review-evidence` at `6aff8627`, not the PR):
  - `author-r3/REVIEW-READY.md:35`: "Receipts: the round 3 section of `receipts/INDEX.md`."
  - `author-r3/round3/HANDOFF-r3.md:29`: "see the round 3 section of `../receipts/INDEX.md`".
  - `author-r3/REVIEW-READY.md:10` and `author-r3/round3/HANDOFF-r3.md:17` say `round2/HANDOFF-r2.md` now reads "`../receipts-round2/`".
  - Published `author-r2/REVIEW-READY.md:40` still reads "`receipts/round2/`", and `author-r2/round2/HANDOFF-r2.md:21` still reads "`../receipts/round2/`".
- Evidence: `receipts/packet-pointers.txt`. The round-3 receipts are published in `author-r3/receipts-round3/`. The only `INDEX.md` in the packet is `author/receipts/INDEX.md`; it is the round-1 blob and has no round-3 section. Commit `6aff8627` changed no file under `author-r2/`.
- Authority: R964-2 RES-1 and R963-2 RES-1, which the round-3 packet reports as fixed.
- Impact: a reader of the packet looks for a file and a section that are not there. No measurement, figure, receipt content or claim about the PR changes. All ten round-3 files match the manifest.
- Exact fix:
  - `author-r3/REVIEW-READY.md:35`: "Receipts: `receipts-round3/`."
  - `author-r3/round3/HANDOFF-r3.md:29`: "Receipts: `../receipts-round3/`."
  - Either republish the two corrected round-2 files, or change lines 10 and 17 above to say the published round-2 archive keeps its old pointer and the directory is `author-r2/receipts-round2/`.
- Verification: each path the packet names resolves in the published tree.

### S1 - SUGGESTION - Docs - `CHANGELOG.md:5` lists what 22 of the 33 plants cover

- Where: `CHANGELOG.md:5`, "Thirty-three planted defects cover the model: each field of the AAF format word (...), the CRF input, the absent sixth input, full-width identity strings, the caller's model ID and a model that held earlier state."
- Evidence: `tests/mutations.json`. The items named account for 22 plants. The other 11 cover descriptor bounds (2), the clock identity, clusters and port maps (3), clock sources (2), the family list, the output buffer and the identify control. Nothing stated is false: the count is right and every named item has a plant.
- Suggested wording: after "a model that held earlier state", add ", and eleven more cover descriptor bounds and descriptor fields". The PR body's "Others cover" already reads as a partial list.

### S2 - SUGGESTION - Tests - the plant `pbaem-ignore-reserved-bit-11` drops bits 1 to 11

- Where: `tests/mutations.json:8885-8889`. The plant masks `0xffe`, eleven bits, while its name says bit 11.
- Evidence: the plant is caught by "reserved bit 11 is refused", and my one-bit probes for bits 1 to 11 are each killed, so nothing is unprotected.
- Suggested change: name it `pbaem-ignore-reserved-bits-1-to-11`, or mask `UINT64_C(1) << 11` alone as the three sibling plants do. `docs/TESTS.md` regenerates from the registry.

## Lens evidence

- Conformance. The delta changes no descriptor and no predicate. Its conformance content is the four new test words and the page's three new sentences. Each test word differs from the valid 48 kHz PCM32 eight-channel word in one bit: 11, 53, 54 or 55. Bits 53 to 55 lie above the up-to bit (52) of the rate octet, and the model's own family entry `0x0215022002006000` shows bit 52 as the up-to bit. AEM-01's wording is unchanged and still equals the predicate. The model still equals the regenerated image byte for byte.
- RTL. The delta holds no HDL: one `.cpp`, one `.json` and five `.md` files. The hardware-facing artifact is the freestanding RV32 build. It passes in Debug and Release on QEMU with an empty unresolved-symbol list, and the smoke names the AEM image check.
- Robustness. No shipped source changes, so every guard keeps its earlier verdict. Re-run at this head: sanitizers, static analysis and the boundary gate, all rc 0. The predicate is now protected bit by bit against a widening of what `pbaem_set_input_format` stores.
- Tests. The new assertions are specific: each names its bit, and each plant fails exactly its named assertion plus the loop. The loop skips bits 22 to 31, the channel count, which the zero and nine channel assertions and plants protect. The needle audit, the test inventory and the report controls pass.
- Docs. Every changed line was checked against the code or a public source. The anchors in `docs/TESTS.md` and `docs/TRACEABILITY.md` point at the moved test lines (227, 259, 275, 301). No stale "twenty-seven", "545", "550" or "field by field" remains for the model. The PR body's figures hold: 27 gates, 33 and 556 plants.

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta: the four new test words decoded against the AAF format layout; `docs/POCKETBEAGLE.md:55`, `:58` and `:66` against the public board support branches, the generator's gitlink and `examples/entity_roundtrip.c`; byte comparison of all 84 descriptors with an image regenerated from the public generator; blob identity of the model, golden and configuration files with `40c3111`. | R964-3 for the delta, R964-2 and R964-1 for the rest | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| RTL | CLEAN | The delta holds no HDL. Examined instead: the RV32 freestanding build in Debug and Release, its empty unresolved-symbol list and its QEMU smoke at this head; the hosted `bare-metal` jobs. | R964-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Robustness | CLEAN | No shipped-source change in the delta, so each guard keeps its earlier verdict. Re-run at this head: address and undefined-behaviour sanitizers, static analysis, boundary gate. Harness run of 224 malformed words against the head and against the round-2 probe copy. | R964-3 for the delta, R964-2 and R964-1 for the rest | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Tests | CLEAN | `tests/test_pbaem.cpp:240-254`, `tests/mutations.json` (556 entries, 33 `pbaem-`, 6 new); the full kit and campaign; 83 reviewer probe runs (81 mutants killed, 2 controls pass); the author's round-3 campaign receipt compared plant by plant. | R964-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |
| Docs | CLEAN | Every changed line of `CHANGELOG.md`, `docs/POCKETBEAGLE.md`, `docs/TESTS.md`, `docs/TRACEABILITY.md` and `docs/VERIFICATION.md`; the PR body; the round-3 evidence packet. Figures recomputed: 33, 551 + 5, 556, 27 gates, 84 descriptors, 8105 octets, the CRC. | R964-3 | `ebaac61dfa3c83f9c6663ce1c361bf79f395f704` |

Comment rule: the delta adds no source comment. Its new test text is assertion messages, and none carries a bench label, lane name, review round, reviewer ID or issue-comment ID. No bench device identity appears in the delta. Both commit subjects are one line, with no body or trailer.

## Limits

- Reading order. The round-3 packet, which I was told to verify, summarises both round-2 reviews' findings, so I knew the internal reviewer's finding titles from it. I read my own round-2 report after my pass over the delta. One slip: the first attempt to write my draft verdict and ledger to disk failed on a tool error, while the same step listed the section headings of the internal round-2 report. I then wrote the draft, unchanged, before reading that report's body. Of that report I read the verdict, findings, residue and suggestions only. No round-3 report of another reviewer was read.
- The assignment pins the evidence tree at `2a261083`. That commit holds no `author-r3`. I read the round-3 packet at `6aff8627` on `pbtsn-review-evidence`.
- The evidence commit is unsigned. I checked the round-3 packet by its manifest hashes and by git object IDs. The author's `tsn-validate-gates.json` is byte-identical in all three rounds, since it holds only gate names and return codes; it does not identify a head. The campaign receipt does, by its six new plants. My own runs are at the exact head.
- IEEE 1722.1-2021 and Milan v1.2 were not consulted directly this round. The closure of F1 rests on the model's exact-match rule and on the up-to bit shown by the model's own family entry.
- Compilers differ from the CI environment: GCC 16.2.1, Clang 23.1.5 for the sanitizer build and an RV32 GCC 16.2.0, with GoogleTest 1.14.0, the Clang 18.1.3 lexer and clang-tidy 18.1.3 pinned (`receipts/environment.txt`). Object hashes and branch counts differ from the author's receipts; every gate passed.
- The kit ran with `--jobs 4` to stay inside the parallel-job limit.
- The Mermaid diagrams were not rendered here. The delta changes no diagram, and the hosted `quality` job runs the kit with `--graphs` and succeeded.
- The regenerated image comes from a reviewer-written configuration (`scripts/reviewer_endstation_pb2_4x4.yaml`). The author's configuration is not published. That the generator needs only the `protocol-processor` submodule is shown for this configuration.
- The statement about the board support repository's branches is true for the five public branches as read today.
- No hardware, board, bench device or simulator beyond QEMU was used. Physical calibration was not run. Nothing here is hardware proof.
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence is the author's published receipts, the hosted jobs above and this review's own runs.
- The clone was left at the exact head: worktree and index equal `HEAD`, 107 tracked files rehashed with no blob or mode difference, no gitlinks, and nothing untracked or ignored after I removed the interpreter cache my runs wrote (`receipts/clone-state.txt`). All probes ran on scratch copies.

## Pending manager duties

- Carry RES-1 to the residue checklist. S1 and S2 are the author's choice.
- Link evidence commit `6aff8627` where the round-3 packet is cited.
- Carried from R964-2, not re-examined this round: confirm that the round-1 packet's "Private" lines and line 2 of `author/round1/HANDOFF-r1.md` are meant to be public.
- Carried from R964-2: the board's unpublished configuration must carry `entity.locale: en-US` for the board image to equal the model. When it is published, regenerate from it and compare with the golden.
- Build and validate the current-dev merge candidate at the merge turn and link its receipts; own hosted acceptance.
- The PR is still a draft against `main`.

## Packet contents

Scripts (portable; paths are arguments): `scripts/env.sh`, `scripts/run_gates.sh`, `scripts/probe_pbaem.py`, `scripts/reserved_high.c`, `scripts/dump_aem.c`, `scripts/compare_aem.py`, `scripts/fetch_generator.sh`, `scripts/regen_image.py`, `scripts/reviewer_endstation_pb2_4x4.yaml`. Receipts are under `receipts/` and listed with their hashes in `MANIFEST.sha256`.

R964-3 FINISHED
