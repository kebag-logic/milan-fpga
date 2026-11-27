[R955] POSITIVE - exact head 0f72ca69a0cd85ade9a3f1c42a325b23704cf625

# R955-2 independent re-review: kebag-logic/tsn-c-stack PR #41 for kebag-logic/milan-fpga #977

Exact head `0f72ca69a0cd85ade9a3f1c42a325b23704cf625`, tree `6095ea2547e768550c65e717b9dd9b9450d764cb`. Delta reviewed: `5d03517f..0f72ca69` (two commits, `cc193cc` and `0f72ca6`). Source base `c3bff8f3dea03870ea7ae62965db360b509ee3b3`.

## Verdict

POSITIVE. The delta adds tests, planted defects and regenerated documents only. `git diff --stat 5d03517f 0f72ca69 -- src` is empty, and so is the same diff for `include` (`receipts/clone-integrity.txt`).

All five findings that left Tests unclean in round 1 are closed:

- my F1, F2 and F3 (MINOR);
- the other round-1 report's R956-1-F1 (MAJOR);
- my residue R1.

Each closing test passes on the unmutated head. Each new planted defect compiles, completes and fails its intended assertion, and no older test catches it. Every round-1 probe of those classes is now killed.

The quality and bare-metal jobs and the mutation campaign (522 caught, 0 escaped, 0 errors) were reproduced from the exact-head tree. The hosted runs at the head succeeded.

What remains is four wording residues and two suggestions. None of them makes the verdict negative.

## Reconstruction

| Source | Read |
|---|---|
| Repository rules | `CONTRIBUTING.md` (there is no `AGENTS.md`): a regression needs a failing assertion and a runnable planted defect; one-line commit subjects; neutral role labels. `docs/VERIFICATION.md` (mutation row). |
| Frozen scope | Unchanged since round 1: issue #977's acceptance and the stack rulings, and ACMP-13 (`docs/REQUIREMENTS.md#acmp-changed-sink-walk`, `docs/PORTING.md`, persistence record and changed-sink walk). This delta touches no requirement, interface or source. |
| Round-1 findings | Both public round-1 reports at `5d03517f`, comments 7210417931 (R956-1: F1 MAJOR, R1 RESIDUE) and 7210486981 (R955-1: F1, F2, F3 MINOR, R1 RESIDUE, S1 SUGGESTION). |
| Delta | `git diff 5d03517f 0f72ca69`: `tests/test_acmp.cpp` (+69), `tests/test_acmp_wide.cpp` (+16), `tests/mutations.json` (+152, ten plants), `docs/TESTS.md` and `docs/TRACEABILITY.md` (regenerated), `docs/VERIFICATION.md:24`, `CHANGELOG.md:5`. History: two one-line commits with no body. |
| Author evidence | milan-fpga `82defc73` `review-evidence/tsn977-r1/author-r2`. All 14 files match `MANIFEST.json`'s `published_sha256` (`receipts/author-r2-manifest-check.txt`). The receipts were spot-checked against my own runs: validate 28/28 at `0f72ca69`; mutation 522/0/0; coverage 877/877 lines and 468/468 branches; bare-metal rc 0; and the `cc193cc` `entity-controls` failure that `0f72ca6` fixes. |
| PR text | The live PR #41 body is the packet's `PR-BODY-tsn.md` minus its title line. |
| Hosted, exact head | Two workflow runs (`push` 45961500310, `pull_request` 45961505812). Both `quality` and both `bare-metal` jobs completed `success` at `0f72ca69`, with every step executed, none skipped. The `quality-evidence` artifact's `gates.json` holds 28 gates, all rc 0, and its mutation log ends `{"CAUGHT": 522, "ESCAPED": 0, "ERROR": 0}` (`receipts/hosted-jobs.txt`). |

## Round-1 findings at this head

| ID | Round-1 severity | Status | Cause addressed and evidence |
|---|---|---|---|
| R955-1-F1 | MINOR, Tests | CLOSED | **Tests:** `P1`–`P3` (`tests/test_acmp.cpp:547`, `:559`, `:571`) rebind changing only the Talker ID's top octet, the controller ID's top octet or the unique ID's high octet. Each requires exactly one `persist` and a saved record equal to `acmp_binding_latch`. `P4` (`:583`) changes each of the 18 ID octets alone.<br>**Plants:** `record-drop-unique`, `record-drop-talker` and `record-drop-controller` are registered and killed by P3, P1 and P2 with their named needles (`receipts/gates/mutation-results.json`).<br>**Round-1 probes, now KILLED:** `r-rec-drop-unique`, `r-rec-drop-talker`, `r-rec-drop-controller`, `r-rec-unique-low-byte-only` and `r-rec-drop-p2`…`p19`. `r-rec-drop-p0` is killed by A24 (`receipts/probe-summary.txt`). |
| R955-1-F2 | MINOR, Tests | CLOSED | **Test:** `AcmpWide.SinkThirtyTwoBoundAloneIsPublishedAndAdmitted` (`tests/test_acmp_wide.cpp:102`) binds sink 32 alone at 33 sinks and asserts both its publication and its admission.<br>**Plants:** `walk-publish-no-reload` and `walk-admit-no-reload` anchor the reloads at `src/acmp.c:221` and `:539`. Each is killed by its own W6 needle (`:113`, `:114`).<br>**Round-1 probes:** `r-publish-no-reload` and `r-admit-no-reload` are now KILLED.<br>**Docs:** `docs/VERIFICATION.md:24` now counts 20 walk plants, which matches the table. |
| R955-1-F3 | MINOR, Tests | CLOSED | **Test:** `P5` (`tests/test_acmp.cpp:608`) reads `binding.streaming_wait` through `acmp_view` (`view()` at `:140`), set for a STREAMING_WAIT bind and clear for a plain one.<br>**Plant:** `view-drop-streaming-wait` (`src/acmp.c:455`) is killed by P5's needle.<br>**Round-1 probe:** `r-viewof-drop-binding-streaming_wait` is now KILLED. |
| R955-1-R1 | RESIDUE, Docs | CLOSED | `docs/VERIFICATION.md:24` now reads "one writes word 0 for every sink and one reads word 0 for every sink in the publication walk", the exact fix. |
| R955-1-S1 | SUGGESTION | TAKEN | `CHANGELOG.md:5` now gives 4,550 cycles "before this change", but the edit introduced R955-2-R3 below. |
| R956-1-F1 | MAJOR, Tests | CLOSED | **Plants:** the three supplied ones are registered as `record-omit-talker-top-octet`, `record-omit-controller-top-octet` and `record-omit-unique-high-octet`, with unique needles. They are killed by P1, P2 and P3, which also check that the saved octet is no longer stale.<br>**Masking:** P4 covers the expanded comparison one octet at a time, so simultaneous changes cannot mask an omitted term.<br>**My probes:** the same `term → 0u` form applied to every ID term (`receipts/octet-probes.json`). All 18 ID octets (`p[2]`…`p[19]`) are KILLED.<br>**Ratchet and inventory:** the coverage ratchet holds (877/877, 468/468), and the inventory and traceability gates pass. |
| R956-1-R1 | RESIDUE, Docs | SUPERSEDED | The PR opening now names `5d03517f` as published. It carries a new stale clause about the two later commits, recorded as R955-2-R1. |

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome (exact fix) | Verification |
|---|---|---|---|---|---|---|---|
| R955-2-R1 | RESIDUE | Docs | PR #41 body, line 1 (same in `author-r2/PR-BODY-tsn.md`) | The body says the two commits after `5d03517f` "add tests only and are local, for the manager to push". PR #41's head is `0f72ca69`, and hosted `push` and `pull_request` runs exist for it (`receipts/hosted-jobs.txt`). | Publication-status wording only. It changes no code, test, figure or verdict. | Replace "add tests only and are local, for the manager to push." with "add tests only and were published at `0f72ca69a0cd85ade9a3f1c42a325b23704cf625`." | Read the PR opening. |
| R955-2-R2 | RESIDUE | Docs | PR #41 body, "Tests added at `cc193cc`" table, rows P1–P4 | The P4 row lists `record-drop-unique`, `record-drop-talker` and `record-drop-controller` as the planted defects it kills. `tests/mutations.json` registers those three against P3, P1 and P2, and `docs/TESTS.md` lists them on those rows. P4 does also kill them (`receipts/registered-new-plants-results.json`), so the row is true. The P1–P3 rows omit their registered field drops. | Description only. The registered mapping and the generated `docs/TESTS.md` are right. | Move each field drop to its registered row: P1 gets "`record-omit-talker-top-octet`, `record-drop-talker`", P2 gets "`record-omit-controller-top-octet`, `record-drop-controller`", P3 gets "`record-omit-unique-high-octet`, `record-drop-unique`". P4 keeps "`record-omit-talker-low-octet` (P4 also fails on each field drop)". | Compare the table with `docs/TESTS.md`'s P1–P4 rows. |
| R955-2-R3 | RESIDUE | Docs | `CHANGELOG.md:5` | The sentence reads "an entry's completion was about 4,550 cycles a completion at nine sinks before this change"; "a completion" repeats the subject. The figure matches the PR body's 40,948 cycles over nine completions. | Wording only. The figure is unchanged. | Replace "an entry's completion was about 4,550 cycles a completion at nine sinks before this change" with "an entry's completion took about 4,550 cycles at nine sinks before this change". | Read the line. |
| R955-2-R4 | RESIDUE | Docs | `docs/VERIFICATION.md:24` | "(caught at 33 sinks, the last by sink 32's own publication and admission)": "the last" is singular, but it refers to the two no-reload plants. | Wording only. The counts (518 + 4, 20 walk plants, 7 record plants, 1 view plant) match `tests/mutations.json`. | Replace "the last by sink 32's own publication and admission" with "the last two by sink 32's own publication and admission". | Read the line. |
| R955-2-S1 | SUGGESTION | Tests | `tests/mutations.json` (P4 plants) | P4 is the only test that catches 14 of the 18 ID-octet omissions: `p[3]`, `p[5]`…`p[10]` and `p[13]`…`p[19]`. My probes show it kills them all (`receipts/octet-probes-results.json`). Only `record-omit-talker-low-octet` is registered against it. | None today. A later edit that weakened P4's loop would not be caught by the campaign for the other 13 terms. | Optionally register one more P4 plant per field, for example `p[3]` (unique low octet) and `p[19]` (controller low octet). | The campaign stays 0 escaped. |
| R955-2-S2 | SUGGESTION | Tests | `scripts/entity_selftest.py:50` (not in the delta) | The entity self-test takes the table's last three entries as its entity plants (`[-3:]`), which is why `cc193cc` failed `entity-controls` and `0f72ca6` had to reorder the table. | None at this head. Appending a plant breaks an unrelated gate. | Optionally select the entity plants by name or by an `arm` field, not by position. | `entity-controls` passes with plants appended. |

## Lens evidence

### Conformance: CLEAN

`src/` and `include/` are byte-identical to `5d03517f`, so round 1's Conformance verdict stands: behavioural identity of the walks, `record_moved`, `view_moved` and `view_of` against ACMP-13, ACMP-02/03/07/09/10, Milan v1.2 5.5 and IEEE 1722.1-2021 8.2.

The new tests assert behaviour the contract already requires:

- a changed binding is persisted once, and the saved record equals the latched record (`docs/PORTING.md`: `env->persist`, the 20-octet record with big-endian IDs);
- the second mark word's sink is published and admitted;
- the view's binding carries STREAMING_WAIT (Milan v1.2 5.3.8.3).

P4's octet arithmetic maps loop indices to record octets 2–19 correctly: unique ID at 2–3, Talker ID at 4–11, controller ID at 12–19. This matches `record_of` (`src/acmp.c:493-504`).

### RTL (implementation and targets): CLEAN

There is no RTL, register or HDL in the delta. The target builds were reproduced at the exact head:

- **GCC build:** `-Werror`, 10/10 test binaries.
- **Host-Clang sanitizer build:** 10/10.
- **RV32 bare-metal gate:** `scripts/baremetal.py`, rc 0.

The hosted `bare-metal` jobs both succeeded. The test-only delta cannot change the RV32 image, because `src/` is unchanged.

### Robustness: CLEAN

The delta adds tests only. P4 calls `SetUp()` again inside its loop, a pattern the file already uses (for example at `tests/test_acmp.cpp:333`). `SetUp` resets the fake, the configuration and the core, and needs no teardown. The address/undefined-behaviour sanitizer arm and the 33-sink shift/undefined arm (`acmp_wide`) pass with the new tests. Round 1's bounds verdict on mark words, re-entry and `saved`/`reported` initialisation stands, since the source is unchanged.

### Tests: CLEAN

Reproduced from an extract of the exact-head tree with pinned GoogleTest/GMock 1.14.0, Clang 18.1.3 and clang-tidy 18.1.3 (`receipts/tools.txt`, `receipts/gates/summary.txt`).

**Mutation campaign:** 522 caught, 0 escaped, 0 errors. Each of the ten new plants:

- matches its anchor exactly once;
- compiles and completes;
- fails its intended test with its intended needle (`receipts/gates/mutation-results.json`).

Run against every test in the `acmp`, `acmp_wide` and `acmp_walk` arms, each new plant is killed only by the new tests. That is P1–P4 for the record plants, W6 for the reloads and P5 for the view (`receipts/registered-new-plants-results.json`). So these tests, and no older test, close the gaps.

**New tests:** P1–P5 and W6 pass on the unmutated head (`receipts/gates/new-tests-gcc.log`). `acmp_tests` lists 132 tests and `acmp_wide` lists 6.

**Coverage:** `src/acmp.c` 877/877 lines and 468/468 branches; the ratchet holds.

**Gates that pass:**

- In the extracted tree: `entity-golden`, `entity-controls`, `boundary`, `needles` (unique literals, zero unspecific killers), `assertion-templates`, `dependencies`, `comments`, `port-contracts`, `acmp-cache`, `registration-controls`, `traceability`, `test-inventory`, `coverage-controls`, `privacy-selftest`, `static-analysis`, `mutation-controls` and `graphs`.
- In a disposable clone at the exact head, because they read git history: `license` and `privacy` (64 commits).

**Reviewer probes** (`receipts/probe-summary.txt`). There are 107 probes in four sets: 69 and 8 from round 1, 20 new per-octet probes, and the 10 registered plants run against every test. Each set also carries two controls.

- **Controls:** the unmutated control passes, and the planted `acmp-nothing-persisted` is killed.
- **Killed:** every probe of the F1, F2, F3 and R956-1-F1 classes.
- **Still surviving:** exactly the probes round 1 classified as equivalent, and none other:
  - the three every-sink walks;
  - `p[1]`, since `saved[1]` is only written by `record_of`;
  - the ungated unique, Talker and controller IDs;
  - the view's stream, destination, VLAN and bound terms, and their ungated forms.
- **Build failures (not counted as kills):** `r2-record-omit-p0`, `r-rec-drop-p0` (probes.json form) and three view-drop forms. Each leaves a variable unused under `-Werror`. Their compiling forms were run: `r-rec-drop-p0` in probes2.json is killed by A24, and the view-drop forms are among the equivalent survivors above.

### Docs: CLEAN (residues R955-2-R1 to R4, suggestions S1 and S2)

- **`docs/VERIFICATION.md:24`:** 518 core plus 4 generated plants, 20 walk plants, 7 record plants and 1 view plant all match `tests/mutations.json`.
- **Generated documents:** `docs/TESTS.md` and `docs/TRACEABILITY.md` are regenerated, and the `test-inventory` and `traceability` gates pass. ACMP-13 now lists P1–P5 and W6.
- **`CHANGELOG.md:5`:** it describes the three closures accurately.
- **Comment rule (owner 2026-10-15):** the delta's only new source comments are six `// REQ: ACMP-13` tags, with no lane labels, lane names, rounds, reviewer IDs or comment IDs, so there is no new residue.
- **Commits:** both subjects are one line with no body.
- **PR body:** apart from R1 and R2, its figures (28 of 28 gates, 522/0/0, 877/877 and 468/468) match my runs and the hosted artifact.

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Empty `src`/`include` delta; new tests against ACMP-13, `docs/PORTING.md` record layout, `record_of`; round-1 identity verdict carried | R955-2 (source verdict carried from R955-1) | 0f72ca69a0cd85ade9a3f1c42a325b23704cf625 |
| RTL | CLEAN | GCC `-Werror` build and tests; host-Clang sanitizer build and tests; RV32 bare-metal gate; hosted `bare-metal` ×2 | R955-2 | 0f72ca69a0cd85ade9a3f1c42a325b23704cf625 |
| Robustness | CLEAN | P4 fixture re-entry, sanitizer and 33-sink shift/undefined arms with the new tests; unchanged source | R955-2 | 0f72ca69a0cd85ade9a3f1c42a325b23704cf625 |
| Tests | CLEAN (S1, S2 suggestions) | `tests/test_acmp.cpp` P1–P5, `tests/test_acmp_wide.cpp` W6, `tests/mutations.json` (522; 10 new); campaign 522/0/0; full-suite killers of the new plants; 107 reviewer probes in four sets, plus controls; coverage; all quality gates; hosted artifact | R955-2 | 0f72ca69a0cd85ade9a3f1c42a325b23704cf625 |
| Docs | CLEAN (R1–R4 residues) | `CHANGELOG.md`, `docs/VERIFICATION.md`, `docs/TESTS.md`, `docs/TRACEABILITY.md`, PR #41 body, author-r2 packet and manifest, delta comments, commit subjects | R955-2 | 0f72ca69a0cd85ade9a3f1c42a325b23704cf625 |

## Real limits

- **Sanitizer compiler.** The local sanitizer arm ran with the host Clang 23.1.5. The pinned Clang 18.1.3 cannot parse this host's GCC 16 libstdc++ headers. The hosted quality job ran the Clang 18 sanitizer arm successfully at the exact head.
- **`conditionals` gate.** It fails locally for the same header reason (`receipts/gates/conditionals.log`, `stl_iterator.h` errors). It passed in the hosted artifact (35 files, 58 region sides).
- **`license` and `privacy` in the extracted tree.** They fail there only because the tree has no git history. They passed in the disposable clone.
- **Packet signature.** The author packet is hash-manifested: all 14 author-r2 entries match `MANIFEST.json`. The milan-fpga evidence commit `82defc73` carries no git signature, so the packet's authenticity rests on that published commit.
- **CPU figures.** The measured figures (THE SETTLE, the registration term, image sizes) are not re-reviewed here. They belong to milan-fpga PR #993, and the source is unchanged since they were measured.
- **No manager source bank.** No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus my own reproduction.
- **No hardware.** Physical calibration was NOT RUN. Nothing here is hardware proof.

## Pending manager duties

- Carry R955-2-R1 to R4 to the residue checklist; the PR-body edits are R1 and R2.
- Own hosted/act acceptance.
- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) on source base `c3bff8f3`, live dev `e275d795`, and link the receipts on the PR.
- Move the milan-fpga pin from `0f72ca69` to the PR's merge commit on `main` once merged, as the stack ruling requires.

R955-2 FINISHED
