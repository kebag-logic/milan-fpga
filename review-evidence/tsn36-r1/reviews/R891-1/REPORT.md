[R891] NEGATIVE - exact head 61a504eec3ec3de828ccd80076212533ef58644b

# R891-1: independent review of kebag-logic/tsn-c-stack PR #36 (milan-fpga #970 salvage)

- Exact head `61a504eec3ec3de828ccd80076212533ef58644b`, tree `50c5014d5669bb8880b719445e6d737d22b9e285`. One commit on main `715589c1db7cf67e2f3259fd7083ebc7f0923376`, which is the live `main` and the merge base (`receipts/main-and-core.txt`).
- Scope: test only. It adds an assertion that a GM_CHANGE in WAITING enters DELAY with the 0 to 4 s draw kind (Milan v1.2 5.6.3.5.7, Table 5.50, Table 5.51; IEEE 1722.1-2021 6.2.4.2.2 for uniformity), plus the plant `gm-change-draws-startup-kind`. The ADP constants stay unchanged, per the ruling on milan-fpga #970 (issuecomment-7080789556, item 4).
- Verdict: **NEGATIVE**, from one open MINOR (R891-1-F1). The new assertion reads the core's record of the most recent draw. It does not check that this GM_CHANGE made a draw. A call-site defect that re-arms the previous delay without a new draw passes all 10 test binaries.
- Everything else checks out on its own evidence:
  - the registered plant is caught by the new message at the head and escapes at the base;
  - source and constants are byte-unchanged;
  - the stack's full gate set passes at the head, and the generated docs are fresh.
- One RESIDUE (R891-1-F2): a reviewer ID in the CHANGELOG entry.

## Reconstruction (in order)

1. **Repository rules.** The repo has no `AGENTS.md`. `CONTRIBUTING.md` requires:
   - a tracked issue;
   - a failing assertion and a runnable planted defect for a regression;
   - a coverage ratchet that is not lowered;
   - one-line commit subjects with no body or trailers;
   - neutral role labels in public documentation;
   - two independent positive reviews.

   I also read `README.md`, `docs/VERIFICATION.md` (gate table), `docs/TESTS.md`, `docs/TRACEABILITY.md` and `docs/REQUIREMENTS.md` (MFDISC-01, ADP-02).
2. **Issue milan-fpga #970.** I read the body with its corrected acceptance, the author's TAKEN and REVIEW READY comments, and the ruling (comment 7080789556). The ruling makes four points:
   - narrowing the first delay is non-conformant, and #35 was closed;
   - the acceptance is corrected to the declared discovery time;
   - the real fix is #972;
   - the salvage for tsn-c-stack is "the assertion and plant that GM_CHANGE in WAITING draws 0 to 4 s", against unchanged constants.
3. **Authorities as cited by the issue, the ruling and the source:**
   - Milan v1.2 5.6.3.5.7: GM_CHANGE in WAITING starts TMR_DELAY.
   - Table 5.50: TMR_DELAY is a random value from 0 to 4 s.
   - Table 5.49: the purpose is storm avoidance.
   - Table 5.51: GM_CHANGE in DELAY is ignored.
   - IEEE 1722.1-2021 6.2.4.2.2: the draw is uniform.
   - In the source: `include/adp.h:86-87` (`ADP_DELAY_MAX_MS 4000u`, `ADP_DELAY_STARTUP_MAX_MS 2000u`), `src/adp.c:53-62` (`draw_ms`), `src/adp.c:81-85` (`enter_delay`) and `src/adp.c:270-279` (`adp_gm_change`).
4. **Diff and history.** I read `git diff 715589c1..61a504ee` (6 files, +52/-33; `receipts/change.diff`) and the commit object. It has a one-line subject, no body and no trailers, and its author and committer match the privacy gate's identity.
5. **Public executable evidence.** I read milan-fpga `7a5e1e9a` `review-evidence/tsn36-r1/author-r1/receipts/stack/*` and the PR body. The relevant author receipts:
   - `validate.py --graphs`: 28 of 28 gates rc 0, mutation `{"CAUGHT": 478, "ESCAPED": 0, "ERROR": 0}`;
   - `baremetal.py`: rc 0;
   - the plant applied to the base: 10 of 10 pass;
   - the plant applied to the head: `adp_tests` fails.

   PR #36 has no manager evidence comments beyond the two review-start notices. No manager source bank runs at this head, and I claim none.
6. **Prior public review findings on PR #36:** none. The PR has 0 reviews, 0 review comments, and two issue comments that are both review-start notices. The PR answers finding R887-1-F1 on the closed #35. I did not read that report, because it belongs to another reviewer. My own probes cover its subject: before this PR, a wrong draw kind at the GM_CHANGE call site escaped the stack suite. At this head the STARTUP plant (and DRAW_NONE) is caught. The stale-draw variant in F1 is not.

## Reviewer execution (this head, disposable clones under the packet's scratch)

The toolchain is in `receipts/tools.txt`:
- GCC 16.2.1, with host Clang 23.1.5 for the CMake sanitizer gate;
- pinned Clang 18.1.3 and clang-tidy 18.1.3;
- Cppcheck 2.22.0;
- GoogleTest/GMock 1.14.0;
- CMake 4.5.0, Python 3.14.10;
- Mermaid CLI 11.16.0;
- riscv64-elf-gcc 16.2.0, QEMU 11.1.3.

The scripts are in `scripts/`. `env.sh` takes `TOOLS`, the pinned tool directory. `copies.sh` makes clean clones. `launch.sh` runs the campaigns concurrently, each with its own log and rc file. `probes.py` holds the fault probes.

| Campaign | Command | Result | Receipt |
|---|---|---|---|
| Full stack gates | `python3 scripts/validate.py --work <w> --jobs 8 --graphs` on a clean clone of the head | rc 0 in 467 s; 28 of 28 gates rc 0, including traceability and test-inventory freshness, privacy, comments, coverage at 100% after exclusions, both sanitizer and GCC suites, static analysis, mutation-controls and graphs; mutation `{"CAUGHT": 478, "ESCAPED": 0, "ERROR": 0}`; `gm-change-draws-startup-kind` and `gm-change-ignored` both CAUGHT in `AdpCore.A0toA2Schedule` | `receipts/validate/` |
| RV32 gate, head | `python3 scripts/baremetal.py --work <w> --jobs 4` | rc 0, Debug and Release, no unresolved final symbols. Release ELF `a9cc5f9e…` and core objects match the author's receipt byte for byte | `receipts/rv32/` |
| RV32 gate, base | same, on `715589c1` | rc 0. Release `adp.o`, `acmp.o`, `maap.o` and ELF are **identical** to the head's. Debug differs only by embedded build paths, from different work directories | `receipts/rv32-base/`, `receipts/rv32-base-vs-head.txt` |
| Fault probes | `probes.py` (13 probes) and `--set followup` (4 probes); full CMake build, `ctest` over all 10 binaries, `adp_tests` | see the table below; every edit matched exactly once | `receipts/probes*.json`, `receipts/probe-logs/` |
| Source and constants unchanged | `git diff --stat 715589c1 61a504ee -- src include examples scripts cmake CMakeLists.txt configs .github` | empty | `receipts/main-and-core.txt` |
| Hosted, exact head | check runs and job steps, read only | `quality` and `bare-metal` each **executed**, with every step `success`, on both the push and pull_request runs (45050645679, 45050650666). The manager owns hosted acceptance | `receipts/hosted-jobs.txt` |

The probe JSON's `ctest_summary` is null for passing probes, because ctest prints "100% tests passed out of 10" in that case. The logs carry that line.

| Probe | Edit | Outcome |
|---|---|---|
| head-clean / base-clean | none | 10/10 pass |
| base-plant | registered plant on base | **escapes** (10/10 pass): before this PR the suite has no killer |
| head-plant | registered plant on head | **caught**: `adp_tests`, `AdpCore.A0toA2Schedule`, "A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)" |
| head-draw-none | `enter_delay(a, ADP_DRAW_NONE)` | caught, same message |
| head-arm-advertise-period | draw, then arm 5000 ms | caught, same message |
| head-arm-twice-the-draw | arm 2x the draw | caught, same message |
| head-stays-waiting | arm, but stay in WAITING | caught (adp_tests, adp_debug, adp_release) |
| **head-no-new-draw** | `timer_start(a, ADP_TIMER_DELAY, a->last_draw_ms); a->state = ADP_STATE_DELAY;` (re-arm the previous delay, no draw) | **escapes: 10/10 pass** (F1) |
| head-delay-max-500 | `ADP_DELAY_MAX_MS` 500 (out of scope) | caught by A9 only |
| head-delay-max-8000 | `ADP_DELAY_MAX_MS` 8000 (out of scope) | caught by the new literal `4000u` (with the fixture's fixed seed) |
| head-plant-without-kind-conjunct | plant, with the new kind conjunct removed | escapes: the kind conjunct is the plant's killer |
| head-symbolic-bound-delay-max-8000 | the new bound written as `ADP_DELAY_MAX_MS`, under 8000 | escapes: the literal is what pins 4 s |
| head-counted-clean (followup) | adds `a.draws == draws + 1u` to the A2 assertion | 10/10 pass |
| head-counted-plant (followup) | the above plus the registered plant | caught, same message |
| head-counted-no-new-draw (followup) | the above plus the no-new-draw edit | **caught**, same message |
| base-no-new-draw (followup) | no-new-draw on base | escapes (the gap predates the PR) |

After the probes, the review clone is at the exact head and tree, with:
- 0 porcelain lines, including untracked and ignored files;
- an empty index diff and an empty worktree diff;
- index modes, blobs and paths identical to the tree;
- every tracked file re-hashing to its index blob;
- no gitlinks in this repository, so no submodule pins to verify.

The disposable head clone used by validate was also left clean (`receipts/clone-state.txt`, `receipts/copies.txt`).

## Findings

### R891-1-F1 - MINOR - Tests, Conformance

- **Where:** `tests/test_adp.cpp:138-141`, the A2 assertion after `adp_gm_change(&a)`, and `tests/mutations.json:362-376` (`gm-change-draws-startup-kind`).
- **Authority:**
  - Milan v1.2 5.6.3.5.7 with Table 5.50: GM_CHANGE in WAITING starts TMR_DELAY with "a random value between 0 and 4 seconds". Table 5.49 gives the purpose: avoiding storms when devices react together, which a grandmaster change, seen by every entity at once, is.
  - The ruling's salvage item: "the assertion and plant that GM_CHANGE in WAITING draws 0 to 4 s".
  - CONTRIBUTING: a failing assertion and a runnable planted defect.
  - The suite's own idiom for this property: `tests/test_adp.cpp:810` ("valid discovery draws one delay", `a.draws == before.draws + 1u`) and `:517` (A23).
- **Evidence:**
  - All four conjuncts hold whether or not `adp_gm_change` draws: state DELAY, `last_draw == ADP_DRAW_DELAY`, `fk.last_delay == a.last_draw_ms`, `<= 4000u`.
  - `last_draw` and `last_draw_ms` are the core's record of the **most recent** draw. In this fixture, that is the TMR_ADVERTISE to DELAY draw two steps earlier, which is also `ADP_DRAW_DELAY` and at most 4000 ms.
  - Probe `head-no-new-draw` re-arms the previous delay with no draw, and passes all 10 binaries at the head (`receipts/probes.json`, `receipts/probe-logs/head-no-new-draw.log`).
- **Impact:**
  - The assertion establishes the kind of the last recorded draw, not that this GM_CHANGE made the fresh random draw that 5.6.3.5.7 requires.
  - A call-site defect that drops the per-event draw escapes the suite, on the very event that synchronises every entity on a network.
  - The assertion message ("DELAY with a 0..4 s draw") and the CHANGELOG ("enters DELAY with the zero to four second draw kind") claim more than the check establishes.
  - The registered plant is still caught, but only because it happens to call `draw_ms`.
- **Required outcome:**
  - The A2 assertion also requires that `adp_gm_change` made exactly one draw, for example `const uint32_t draws = a.draws;` before the call and `a.draws == draws + 1u` in the conjunction.
  - A runnable plant that re-arms the delay without a draw (the probe's edit, or an equivalent) is registered and killed by the A2 message.
  - The generated docs (`docs/TESTS.md`, `docs/TRACEABILITY.md`) and the plant count in `docs/VERIFICATION.md` are regenerated or updated.
- **Verification:**
  - Follow-up probes: with that conjunct, the clean head passes 10/10, the registered plant is caught, and the no-new-draw edit is caught, all by "A2 GM_CHANGE in WAITING: DELAY with a 0..4 s draw (5.6.3.5.7)" (`receipts/probes-followup.json`).
  - At the fixed head, `validate.py --graphs` reports 0 ESCAPED, and the new plant appears in its results.

### R891-1-F2 - RESIDUE - Docs

- **Where:** `CHANGELOG.md:5`, the text "…, review finding R887-1-F1)".
- **Authority:** CONTRIBUTING: "Use neutral role labels in public documentation."
- **Evidence:** At the base, no tracked documentation names a reviewer or review-round ID. The one existing instance is a source comment, `scripts/acmp_cache_controls.py:17`, tracked by #746. The privacy gate passes; the text is not in any of its classes (host locations, account details, equipment identifiers, product names).
- **Impact:** wording only. It changes no measurement, test, code, generated artifact or clause claim.
- **Exact fix:** delete ", review finding R887-1-F1", so that the entry ends "([milan-fpga #970](https://github.com/kebag-logic/milan-fpga/issues/970)). No constant or behaviour changes."
- **Verification:** `git grep -nE "R[0-9]{3}-[0-9]" -- CHANGELOG.md` is empty.

## What was checked clean, by lens

- **Conformance** (unclean only through F1):
  - The production call site is unchanged and conformant: `src/adp.c:276-278` enters DELAY with `ADP_DRAW_DELAY`, and `draw_ms` maps a 16-bit value uniformly onto 0 to `ADP_DELAY_MAX_MS` (4000, Table 5.50). The startup kind keeps 2000 (5.6.3.5.2).
  - The ruling's "constants unchanged" is met: `src` and `include` are empty in the diff, and the Release RV32 objects are identical between base and head.
  - The assertion uses the literal `4000u`, which pins the clause value independently of the constant (probe head-symbolic-bound-delay-max-8000).
  - The A2 step is reached in WAITING: the two preceding expiries end in an advertise.
  - The plant's original-test provenance (`Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING`, the parent walk) follows the sibling `gm-change-ignored`.
- **RTL:** the repository is portable C with no HDL. The diff touches no RTL, register map, mailbox contract or gitlink, and the parent pin does not move (PR body; 100 tracked blobs, 0 gitlinks).
- **Robustness:**
  - No core, port or build change.
  - The new check is a non-fatal `EXPECT_TRUE`, so the following A2 steps still run and report.
  - The sanitizer and RV32 Debug/Release gates pass.
  - The plant's `old` text matches `src/adp.c` exactly once (driver check, and my probe edit counts).
- **Tests** (unclean through F1):
  - The new assertion fails on the registered plant by its own message at the head; on the base the plant escapes.
  - The kind conjunct is what kills it.
  - DRAW_NONE, wrong arm value and stay-in-WAITING variants are also caught.
  - The mutation campaign reports 478/478 caught, and mutation-controls passes.
- **Docs:**
  - `docs/TESTS.md` and `docs/TRACEABILITY.md` are byte-fresh against their generators (test-inventory and traceability gates rc 0).
  - The `docs/VERIFICATION.md` count of 474 core plants matches 478 entries less the four generated configuration plants (477 to 478 in `tests/mutations.json`).
  - The CHANGELOG entry is present, and the commit subject is one line.
  - Only F2 (RESIDUE) is open.
- **Comment rule:** the delta adds no source comment. The plant text keeps only the clause comment `// Milan v1.2 5.6.3.5.7`. No new lane label, lane name, review round, reviewer ID or issue-comment ID appears in source. The one new reviewer ID is in the CHANGELOG (F2).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Milan v1.2 5.6.3.5.7, Tables 5.49-5.51; IEEE 1722.1-2021 6.2.4.2.2; ruling issuecomment-7080789556; `src/adp.c:53-85,270-279`; `include/adp.h:86-87`; `tests/test_adp.cpp:113-145`; base-to-head RV32 Release object identity | R891-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| RTL | CLEAN | tree listing (no HDL, 0 gitlinks); diffstat (no RTL, mailbox or pin input); PR body "parent's pin is not moved" | R891-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Robustness | CLEAN | empty core/build diff; sanitizer and GCC suites; RV32 Debug/Release at head and base; plant single-match; EXPECT non-fatal flow; 17 probes | R891-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Tests | UNCLEAN (F1) | `tests/test_adp.cpp:138-141`; `tests/mutations.json:362-376`; validate mutation 478/478 and plant results; probes base-plant, head-plant, the kind-conjunct ablation and head-no-new-draw; follow-up probes | R891-1 | 61a504eec3ec3de828ccd80076212533ef58644b |
| Docs | CLEAN (F2 RESIDUE) | `CHANGELOG.md:5`; `docs/TESTS.md:148-170`; `docs/TRACEABILITY.md` ADP and MF rows; `docs/VERIFICATION.md:24`; generator freshness gates; commit object | R891-1 | 61a504eec3ec3de828ccd80076212533ef58644b |

## Real limits

- This is source-head execution on this host's pinned toolchain, not the CI Ubuntu image. The sanitizer gate's `clang` is the host's 23.1.5, as it is in the author's receipts. validate ran with `--jobs 8`. Hosted execution at the exact head is shown only as read-only job status.
- No manager source bank, current-dev merge candidate, builder bank or native bank was run or inferred by this review. The current-dev candidate (source base 715589c1, live dev e275d7950ef3385753e6a15d2e191ba855b171ed) is the manager's.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- I did not read finding R887-1-F1 on #35 or any other reviewer's report. Its subject is re-derived above from the PR text and my own probes.
- The probes cover mutants I chose. The 4 s literal kill under the 8000 constant depends on the fixture's fixed seed.

## Pending manager duties

- Carry F1 back to the author, and get a re-review at the fixed head.
- Add F2 to the residue checklist.
- Get the second independent review; merge needs two independent positive reviews.
- Run hosted and act acceptance.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR.
- Track the parent follow-up: the milan-fpga grandmaster-order tests restated to the literal 4,000 and 2,000 ms, a pin move after merge, and the bench re-run after #972.

R891-1 FINISHED
