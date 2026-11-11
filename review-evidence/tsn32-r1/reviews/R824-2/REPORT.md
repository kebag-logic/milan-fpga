[R824] POSITIVE - exact head a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e

# R824-2: external independent review of kebag-logic/tsn-c-stack PR #34 (issue #32), round 2

- Exact head `a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e`, tree `3a247e5df4116d29f43c14f4300ce0f3f7d2eb54`, both verified in the reviewer's detached clone (`receipts/clone-integrity.txt`).
- Delta under review: `9043b926..a530ecaf`, three commits by the author (`4cdf2a2f`, `8661947d`, `a530ecaf`). There is no merge, rebase or amend. Source base `main` `9deb0ddb`.
- Governing scope: the manager ruling on PR #34, issuecomment-6789256216, items 1 to 6. Round 2 makes changes to tests, docs and the PR body only.
- **Verdict: POSITIVE.**
  - No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head.
  - Every prior finding is resolved, both mine (R824-1) and the other reviewer's (R823-1). Each is resolved at its cause or by the ruling.
  - I record three SUGGESTIONs. They do not affect the verdict.

## Reconstruction and sources

1. `CONTRIBUTING.md` (the repository has no `AGENTS.md`), `README.md`, and `docs/`: REQUIREMENTS, PORTING, VERIFICATION, TESTS and TRACEABILITY.
2. Issue #32. The body's four acceptance items are unchanged. The issue's only comments are the author's TAKEN and REVIEW READY notices. On PR #34, the ruling issuecomment-6789256216 (items 1 to 6) is the public scope decision for this round.
3. Requirements ACMP-13, ACMP-09 and ACMP-10, and the port contract sections "ACMP changed-sink walk" and "ACMP machine storage".
4. `git diff 9043b926..a530ecaf`: 8 files, +235/-22. **`git diff 9043b926 a530ecaf -- src include` is empty: 0 paths.** I also read the history of the three commits.
5. Public evidence:
   - The milan-fpga archive `bd10795e`, `review-evidence/tsn32-r1`. All 450 `MANIFEST.json` entries match their published SHA-256: 79 `author`, 243 `author-r2`, 128 `reviews`. No file is missing, mismatched or unlisted. Five entries are path-redacted (`receipts/evidence-manifest.txt`, `scripts/verify_manifest.py`). The author packet's `PR-BODY.md` equals the live PR body, up to a trailing newline.
   - The hosted runs at the exact head.
   - The parent comments that the PR body cites.
6. Prior public findings: R823-1 and R824-1, both on PR #34. I read them only after my own pass over the delta. They are resolved below. I read no other reviewer's round 2 material.

## What I executed at a530ecaf

All runs used disposable clones under the packet's unpublished scratch area. The round 1 scripts were copied byte-identical: `receipts/r1-scripts.sha256` equals the round 1 manifest. The driver record is `scripts/runs.sh`.

| Probe | Result | Receipt |
|---|---|---|
| Round 1 `ci_run.sh`, unchanged, **pinned Clang 18.1.3 as `clang` and `clang++`** (round 1's setup) | `validate.py` rc 1. 16 of 17 source gates are rc 0. `conditionals` is rc 1 at the new interface control's first case (4 interfaces, `clang++`): that Clang cannot parse the host's libstdc++ 16 headers (`stl_iterator.h` via `gtest.h`). Every C capacity control before it passes. This is a host limit, the same one that failed `clang-sanitizers-build` in my round 1 run. `baremetal.py` rc 0. The clone status is clean before and after | `receipts/ci-head-ciA/` |
| Round 1 `ci_run.sh`, unchanged, **with the host's Clang 23.1.4 as `clang` and `clang++`** (`clang-18` stays the pinned 18.1.3 for the gates that call it; `receipts/compiler-variants.txt`) | `validate.py --jobs 16 --graphs` rc 0, 28 of 28 gates. Mutation `{"CAUGHT": 477, "ESCAPED": 0, "ERROR": 0}`. `src/acmp.c` 847/847 lines and 436/436 branches. GCC 16.2.1 CTest 10/10 and Clang 23.1.4 sanitizer CTest 10/10, `acmp_walk` passing in both. Interface control: compiles at 4 and 32 interfaces and is refused at 33 by "the interface mark holds a bit for every interface", with gcc and clang. `baremetal.py` Debug and Release rc 0. The clone status is clean before and after | `receipts/ci-head-ciB/` |
| Hosted runs at the exact head (inspected only; the manager owns hosted acceptance) | Push run 42992097714 and pull_request run 42992108757: `quality` and `bare-metal` both completed success. The push-run artifacts show 28/28 gates rc 0 under the CI image's GCC 13.3.0 and Clang 18.1.3, mutation 477/0/0, `acmp.c` 847/847 and 436/436, and the interface control passing with the CI image's `clang++` | `receipts/hosted/` |
| Round 1 differential matrix (`build_dwalk.sh`, `matrix.sh`): `main`'s real core against the head's, under ASan, UBSan and shift sanitizers | **560 of 560 pass**, rc 0. The sorted output lines are identical to round 1's, as expected, because the source is unchanged | `receipts/differential/` |
| Round 1 probe controls on the head's suite (`suite_on_plant.sh`) | `c1` (started unmarked): caught by `acmp_tests`, `acmp_wide` and all four `AcmpWalk` tests. `c2` (release mark in word 0) and `c3` (release mark below 32 only): caught by `AcmpWide` as in round 1, **and now by `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`** ("the changed-sink walk makes the full walk's calls", step 274). **`c4` (probe-left marks word 0), which no test caught in round 1, is now caught** by the same test at step 276 | `receipts/probe-controls-suite.txt` |
| Round 1 probe controls on the differential | Same results as round 1: `c1` differs at step 15; `c2` and `c3` differ under LIFT only; `c4` is not observable in my probe's interface map | `receipts/probe-controls-dwalk.txt` |
| Plant-table audit (round 1 `plant_merge_audit.py`, plus `plant_delta.py`) | 477 = 470 + 7. None dropped. The common order is kept, and both parents' orders are kept. The 25 `walk-` plants are contiguous after `acmp-wide-release-clears-one-word`, and the entity plants are last. The only changes to existing plants: `walk-release-unmarked` and `walk-probe-left-unmarked` gain a 33-sink kill (`kills` and `original_tests` only). Each new plant's `old` text occurs exactly once in `src/acmp.c` | `receipts/plant-merge-audit.txt`, `receipts/plant-delta.txt` |
| Kill words in my campaign (`plant_kills.py`, `plant_failures.py`) | Each of the four second-word plants is CAUGHT only through `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`, by the trace message, at steps 12, 52, 274 and 276 of 8,000. `walk-marks-never-cleared` and `walk-interface-marks-never-cleared` are CAUGHT at 1, 8, 32 and 33 sinks, by "a completed entry leaves no sink marked" or "no interface marked" (step 2), with the trace assertion passing first. `walk-clear-first-word-only` is CAUGHT at 33 sinks only (step 9). The merged and re-anchored plants keep their round 1 kill words | `receipts/new-and-merged-plants.txt`, `receipts/new-plant-failures.txt` |
| Merge survival (round 1 script) | Same as round 1 for `src/acmp.c`, `include/acmp.h`, `CMakeLists.txt`, `scripts/mutation.py`, `test_acmp.cpp` and `test_acmp_wide.cpp`. `test_acmp_walk.cpp` differs only by this round's edits | `receipts/merge-survival.txt` |
| Sanitizer gate (round 1 script, host Clang 23.1.4) | configure, build and test rc 0; 10/10 | `receipts/sanitizer-host/` |
| `sizeof(struct acmp)`, `main` against the head, host x86-64 and RV32 ilp32 | +8 B at 16, 32, 33 and 64 sinks on both targets: the 33-sink word lands in padding. This confirms the PR body's "+8 bytes at 16, 32 and 33 sinks" | `receipts/struct-acmp-size.txt` |
| RV32 sizes at the head (my `baremetal.py` build) | `acmp.c` text Debug 22,189 B and Release 21,077 B. Smoke image text 52,652 B and 42,337 B. These equal the PR body's head figures. The `main` figures (21,429, 20,365, 51,964 and 41,645) agree with my round 1 `acmp.c` receipt and the author's `receipts/rv32` | `receipts/ci-head-ciB/baremetal.log` |
| Comment-rule and privacy scan of all 232 added lines of the delta | No lane label, review round, reviewer ID, issue-comment ID, host path or tool name | (scan over `git diff -U0 9043b926 a530ecaf`) |
| Parent figures in the PR body (S-2, item 3) | Each quoted figure appears in its cited comment: 0.844 to 0.747, the four µs pairs and 123,012 B / 132 B over the granule (6778599191); 18,782 of 22,170 cycles (6751120577); 0.815 and 0.719 (6788757307) | public comments, read-only |

## Delta review by ruling item

1. **Second mark word at 33 sinks.** The changes are in `tests/test_acmp_walk.cpp`:
   - `commanded_sink()` sends a quarter of BIND_RX, UNBIND_RX and GET_RX_STATE to sink 32, and the rest to any sink (`:188-190`). The round 1 fold onto sink 0 is gone.
   - `room` is drawn at every size (`:310`).
   - Sink 32 sits alone on a third interface (`:136-142`).
   - A poll-first bias applies while frames are owed (`:269-272`).
   - The draws are short-circuited on `wide`, so the 1-, 8- and 32-sink entry sequences are round 1's.
   - The two new reach checks (owed response; an owed probe of sink 32 that leaves while its timer waits) pass at the head.

   The four new plants are each caught through the 33-sink test by its own trace message, in my campaign and in the hosted campaign. **Met.**
2. **Completion clears every mark.** After every step, each `dirty` word and `dirty_if` must be zero (`:341-346`). Each step ends with a completing entry or a refusal before marking: the restores are followed by `acmp_open`, and the poll-first branch requires room. The three clear plants are caught by the new messages and only by them. The ACMP-13 row of `docs/TRACEABILITY.md` names the four `AcmpWalk` tests, which carry the assertion, and `docs/TESTS.md` lists the new kills. **Met.**
3. **Parent consumer bar.** The ruling defers it to the milan-fpga pin move. The PR body:
   - links the ruling in its first paragraph;
   - states the code size: `acmp.c` +760 / +712 B, smoke image +688 / +692 B, `struct acmp` +8 B;
   - states the known consumer effect: 123,012 B, 132 B over the 122,880 B granule, citing milan-fpga#665 issuecomment-6778599191 item 5.

   **Met.**
4. **Residue, each fixed with the exact text.**
   - R824-1 RES-1 (`docs/REQUIREMENTS.md:41-42`): verbatim.
   - RES-2 (`docs/VERIFICATION.md:24`): verbatim, then extended for the seven new plants.
   - RES-3 (the PR body's round 1 "Validation" note): verbatim.
   - R823-1 R2 (the PR body's plant sentence): verbatim.
   - R823-1 R1 and R3 cover the same lines as RES-2 and RES-3. Per the ruling, RES-2 and RES-3's text is taken.

   **Met.**
5. **Interface-mask width.**
   - `static_assert(ACMP_MAX_INTERFACES <= sizeof(acmp::dirty_if) * 8u, "the interface mark holds a bit for every interface")` is at `tests/test_acmp_walk.cpp:20`.
   - `scripts/check_conditionals.py` `interface_controls()` (`:175-198`) plants the header bound at 4, 32 and 33. It requires a compile at 4 and 32, and a refusal naming the assertion at 33, with `g++` and `clang++`.
   - It runs green in my host-Clang run and in hosted CI.
   - S-2's parent figures are stated and match their sources.

   **Met** within the ruling's no-core-change bound (see S-A).
6. **Gates.** A clean clone of the head gives validate rc 0 (28/28, mutation 477/0/0) and baremetal Debug and Release rc 0. Both round 1 reviewers' scripts were rerun by the author, and mine are rerun here, unchanged. **Met.**

## Lens notes

- **Conformance.** No core byte changed, so round 1's conformance verdict (IEEE 1722.1-2021 8.2; Milan v1.2 5.5.3 and 5.6.4) holds unchanged. The matrix against `main`'s real core reproduces line for line. The new 33-sink coverage strengthens ACMP-10 (publish before the promising response) and ACMP-13 (call order) at sink 32 itself.
- **RTL.** No HDL is in this repository. The freestanding RV32 Debug and Release builds and the QEMU smoke test pass in my run and in the hosted run. The core imports are unchanged. The image sizes equal the PR body's figures. The consumer rom-fit effect is stated and deferred by the ruling.
- **Robustness.**
  - The interface-mark width is now guarded at compile time on the test side and checked by the conditional gate.
  - `ACMP_MAX_INTERFACES` is a fixed `#define` in `include/acmp.h:163`, not a configuration knob, so the header edit that would widen it is exactly what the gate plants.
  - The struct growth is measured on host and RV32.
  - Mask sizing on every path holds at 16, 32, 33, 64 and 255 under ASan, UBSan and the shift sanitizer.
- **Tests.** The 33-sink differential now drives commands, owed responses, owed probes and releases on the second mark word. The release-loop conflict line is covered by the walk test itself, not only by `AcmpWide`. Plants exist for each second-word mark site and for each clear. The campaign is 0 escaped, and coverage is 100 % after exclusions.
- **Docs.**
  - The REQUIREMENTS, VERIFICATION, CHANGELOG, TESTS and TRACEABILITY changes are accurate against the code and the campaign. TESTS and TRACEABILITY are generator-checked.
  - The PR body's round 2 sections match my measurements: the struct size, the RV32 sizes, the 477/0/0 campaign, my `ci_run.sh` result with the pinned Clang (16 of 17 source gates, `conditionals` rc 1) and the parent figures.
  - No source comment in the delta carries a lane label, review round, reviewer ID or comment ID.

## Resolution of prior findings at this head

| Prior item | State at a530ecaf | Evidence |
|---|---|---|
| R824-1 F-1 (MINOR, parent consumer bar) | **Resolved** by the ruling's deferral (item 3) and the PR body's statement of the code size and the +132 B effect, with the ruling linked | PR body "Item 3" |
| R824-1 RES-1, RES-2, RES-3 | **Resolved**, exact text | `docs/REQUIREMENTS.md:41-42`, `docs/VERIFICATION.md:24`, PR body round 1 "Validation" |
| R824-1 S-1 (lift the 33-sink restriction) | **Taken.** `c2`, `c3` and `c4` are now caught by `acmp_walk` | `receipts/probe-controls-suite.txt` |
| R824-1 S-2 (parent target figures) | **Taken**, figures verified against their sources | PR body "Item 5" |
| R824-1 S-3 (interface-mask width) | **Taken** on the test side, within the ruling (S-A below) | `tests/test_acmp_walk.cpp:20`, `scripts/check_conditionals.py:175-198` |
| R823-1-F1 (second-word paths untested) | **Resolved**: the four plants are CAUGHT by the 33-sink test's own message | `receipts/new-plant-failures.txt` |
| R823-1-F2 (no assertion that marks clear) | **Resolved**: the assertion, the three plants and the ACMP-13 row | `tests/test_acmp_walk.cpp:341-346`, `docs/TRACEABILITY.md` |
| R823-1-F3 (parent consumer gates) | **Resolved** by the ruling's deferral, as F-1 | ruling item 3 |
| R823-1 R1, R2, R3 | **Resolved.** R2 is fixed with its exact text; R1 and R3 are superseded by RES-2 and RES-3 per ruling item 4 | as above |
| R823-1 S1, S3 (that reviewer's suggestions) | S1 is partly taken: the 33-sink poll bias, plus the author's 24-seed sweep. S3 was not taken by the ruling; it stays that reviewer's suggestion | — |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

### S-A (SUGGESTION): move the interface-width assertion into the core at its next change

- **Lens:** Robustness.
- **Where:** `tests/test_acmp_walk.cpp:20`.
- **What:** the assertion fires only where the walk test is compiled. A port that edits `ACMP_MAX_INTERFACES` and builds only `src/acmp.c` would not be refused. The bound is a fixed `#define` today and the conditional gate plants it, so nothing is exposed now.
- **Suggested outcome:** at the next change that is allowed to touch the core (for example the pin-move round), place `_Static_assert(ACMP_MAX_INTERFACES <= sizeof ((struct acmp *)0)->dirty_if * 8u, …)` beside #31's two assertions at `src/acmp.c:35-37`, and point the gate's control at `src/acmp.c` as `capacity_controls()` does.

### S-B (SUGGESTION): let the interface control take its C++ compilers from the environment

- **Lens:** Tests.
- **Where:** `scripts/check_conditionals.py:188` (`for cxx in ('g++', 'clang++')`).
- **What:** on a host whose `clang++` is the pinned Clang 18 with a newer libstdc++, the gate fails before any project check. The author and both reviewers had to swap `clang++`.
- **Suggested outcome:** an override such as `TSN_CXX_COMPILERS`, or reuse of the compilers the sanitizer build is configured with. This would make review hosts reproduce the gate without a PATH swap, and CI is unchanged.

### S-C (SUGGESTION): separate sink k from sink k mod 32 in the reviewer-side differential

- **Lens:** Tests.
- **What:** this one concerns the reviewer's own tooling, not the PR. My `dwalk.cpp` maps sink 32 onto an interface shared with sink 0, so `c4` stays unobservable there. The head's test now covers `c4`, so nothing is missing at this head. A future reviewer reusing `scripts/dwalk.cpp` should take the head test's three-interface map.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src`/`include` identity to `9043b926` (0 paths); differential against `main`'s real core, 560/560, identical to round 1; new 33-sink coverage of ACMP-10 and ACMP-13 at sink 32; hosted run | R824-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| RTL | CLEAN | RV32 Debug and Release builds and QEMU smoke (mine and hosted); core imports; `acmp.c` and image text sizes; `struct acmp` size on RV32; consumer rom-fit effect stated and deferred by the ruling | R824-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Robustness | CLEAN (S-A) | Interface-width `static_assert` and the conditional gate's 4/32/33 control (mine and hosted); mask sizing at widths 16 to 255 under sanitizers; struct growth on host and RV32; parent consumer bar (ruling item 3) | R824-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Tests | CLEAN (S-B, S-C) | `test_acmp_walk.cpp` delta; seven new plants and their kill messages; 477/0/0 campaign (mine and hosted); plant-table audits; probe controls `c1`–`c4` on the suite and the differential; coverage; CI rc under both compiler variants; author evidence archive (450/450 hashes) | R824-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Docs | CLEAN | REQUIREMENTS ACMP-13 wording; VERIFICATION mutation and conditional rows; CHANGELOG; TESTS and TRACEABILITY (generator gates, ACMP-13 row); PR body round 2 and corrected round 1 sections against my measurements and the cited parent comments; comment-rule and privacy scans of the delta | R824-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |

## Real limits

- Compilers:
  - **The conditionals gate was run both ways.** With the pinned Clang 18.1.3 as `clang++`, round 1's setup, it fails on this host's libstdc++ 16 headers. With the host's Clang 23.1.4 as `clang` and `clang++`, it is rc 0.
  - My GCC CTest, coverage and mutation runs used the host's GCC 16.2.1. The `clang-18` gates used the pinned 18.1.3.
  - The CI image's GCC 13.3.0 and Clang 18.1.3 results come from the hosted runs, which I inspected and did not execute.
- Skipped: I did not rerun the host benchmark, because no core or benchmark byte changed. Round 1's reproduction stands.
- Taken from receipts: the `main`-side RV32 image figures come from the author's receipts and my round 1 `acmp.c` receipt; I did not rebuild them this round.
- No parent firmware gate was run. That is outside the allowed scope, and the ruling defers it to the pin move.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts, my own runs and the inspected hosted runs.
- Physical calibration: NOT RUN. Nothing here is hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- At the merge turn, the current-dev merge candidate (builder and native banks; source base `9deb0ddb`, live dev `46c971fa`), with its receipts linked on the PR.
- Carry ruling item 3 to the milan-fpga pin move that takes #28, #31 and #32. That move runs `firmware-unit`, `firmware-control-mutants`, `firmware-boundary`, `firmware-verilator` and the image ROM ledger at the moved pin, and resolves the 132 B over-granule debt of the 8x8/2if `answering-every-port` image.
- The second independent review (R823-2) remains its own.

R824-2 FINISHED
