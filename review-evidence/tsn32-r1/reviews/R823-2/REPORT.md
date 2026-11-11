[R823] POSITIVE - exact head a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e

# R823-2: kebag-logic/tsn-c-stack PR #34 (issue #32), round 2 delta review

Exact head `a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e`, tree `3a247e5df4116d29f43c14f4300ce0f3f7d2eb54`. Delta reviewed: `9043b926..a530ecaf`, three commits by the author (`4cdf2a2`, `8661947`, `a530eca`), under the manager ruling PR #34 issuecomment-6789256216, items 1 to 6. Source base `9deb0ddb`.

## Verdict

POSITIVE. This round changes only tests, docs, a gate script and the PR body. `git diff 9043b926 a530ecaf -- src include` is empty (`git diff --quiet` rc 0), so the round 1 Conformance and implementation verdicts carry over unchanged.

All three round 1 MINOR findings of this reviewer (R823-1-F1, F2, F3) are resolved at this head. So is the other round 1 review's MINOR finding (R824-1 F-1). Every round 1 residue is fixed with the exact text the ruling chose.

- Item 1: the four second-word plants and the rerun of round 1's fault probes show the 33-sink test now reaches sink 32's command and owed paths.
- Item 2: a new assertion catches marks that outlive their completion. Without it the never-cleared plant escapes, which shows the assertion does the work.
- Item 5: the interface-mask width check is refused at 33 interfaces, and the gate's control fails if that check is removed.

Open items: one RESIDUE (CHANGELOG wording) and three suggestions. None of them affects the verdict.

## Findings

### R823-2-RES1 (RESIDUE): the CHANGELOG says the test checks the marks after each entry; it checks after each step
- Lenses: Docs.
- Where: `CHANGELOG.md:5`, last sentence: "After each entry it requires every mark cleared."
- Authority/evidence:
  - `docs/REQUIREMENTS.md:41-43`: `acmp_restore_binding` and `acmp_restore_rollback` mark "right after the reset" for the next walk. So those two entries leave marks by design.
  - `tests/test_acmp_walk.cpp:341-346` asserts after each `step()`. Each step ends with an entry that completes or is refused before it marks, since restore and rollback are always followed by `acmp_open` (`:264-265`, `:322-323`).
  - The PR body's item 2 already says this precisely ("After every step ... Every step ends with an entry that either completes or is refused before it marks").
- Impact: wording only. The assertion, its plants and their figures are unaffected.
- Exact fix: replace the sentence with "After each step, which ends with an entry that completes or is refused before it marks, it requires every mark cleared."
- Verification: read `CHANGELOG.md` at the next head.

### R823-2-S1 (SUGGESTION): tag the 33-sink walk test with ACMP-09 now that it covers owed release at sink 32
- Lenses: Docs, Tests.
- Where: `tests/test_acmp_walk.cpp:378` (`// REQ: ACMP-13, ACMP-10, ACMP-05`), and the generated `docs/TESTS.md` row and `docs/TRACEABILITY.md` ACMP-09 row.
- Why: since this round, the 33-sink test withdraws transmit room. It requires a response of sink 32 to be owed and an owed probe of sink 32 to leave. It catches `walk-release-unmarked`, `walk-release-second-word-unmarked`, `walk-probe-left-unmarked` and `walk-probe-left-second-word-unmarked`, which are ACMP-09 paths. The 1, 8 and 32-sink tests already carry ACMP-09. The omission dates from round 1, when the 33-sink test owed no frame. Nothing claims the matrix is complete, so this is not a defect.
- Suggested outcome: add ACMP-09 to that REQ line and regenerate (`test_inventory.py --write`, `traceability.py --write`).

### R823-2-S2 (SUGGESTION): move the interface-width check into the core at its next change
- Lenses: Robustness.
- Where: `tests/test_acmp_walk.cpp:20`. The shifts it guards are in `src/acmp.c:213` and `:1223`.
- Why: the ruling (item 5, "no core change") put the `static_assert` in the walk test. A consumer build of the core alone is not refused. Today this is safe: `ACMP_MAX_INTERFACES` is a fixed `#define 4u` in `include/acmp.h`, and the gate plants it by text replacement, not by `-D`. A `_Static_assert(ACMP_MAX_INTERFACES <= 32u, ...)` beside #31's storage refusals would cover every build, once a core change is in scope.

### R823-2-S3 (SUGGESTION): let the interface control name its C++ compiler
- Lenses: Tests, Robustness.
- Where: `scripts/check_conditionals.py:188` (`for cxx in ('g++', 'clang++')`).
- Why: on this review host, with the pinned Clang 18.1.3 as `clang++`, the control fails at its first case: "interface control at 4 interfaces with clang++: rc 1", from libstdc++ 16 header errors (`receipts/r2/conditionals-pinned.log`). The gate passes with the host Clang 23.1.4 and on the hosted image. An override such as `TSN_CLANGXX`, like the `TSN_CLANG` that `compiler_tokens.py` already reads, would let a local run use the pinned compiler where it can build. Or the control could say in its error that the C++ library cannot be parsed.

## Prior public review findings: resolution at this head

I read these only after my own pass over the diff (round 1 reports in the evidence archive `bd10795e`, `reviews/R823-1` and `reviews/R824-1`).

| Prior finding | Status at a530ecaf | Evidence |
|---|---|---|
| R823-1-F1 (MINOR) second mark word untested at 33 sinks | RESOLVED | `commanded_sink()` sends a quarter of BIND_RX, UNBIND_RX and GET_RX_STATE to sink 32, and `sink()` covers 0 to 32 (`tests/test_acmp_walk.cpp:188-190`, `:197-209`). Room is withdrawn at every size (`:310`). Sink 32 is alone on interface 2 (`:136-142`). The four plants `walk-{bind,unbind,release,probe-left}-second-word-unmarked` are each CAUGHT only through `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk` with "the changed-sink walk makes the full walk's calls": my walk campaign 25/25, the author's full campaign 477/477, the hosted artifact 477/477. My round 1 fault probes now each fail that test (`receipts/r2/probe-mutants-results.json`). The PR body's 33-sink paragraph is rewritten |
| R823-1-F2 (MINOR) no assertion that completion clears the marks | RESOLVED | `:341-346` asserts every `dirty` word and `dirty_if` is zero after every step. `walk-marks-never-cleared` and `walk-interface-marks-never-cleared` are CAUGHT at 1, 8, 32 and 33 sinks, and `walk-clear-first-word-only` at 33, each by the clear assertion's own message. My probe that removes the two assertions makes the never-cleared plant pass every test, so the assertion is what catches it. My `clear-keeps-third-interface` probe is caught by "a completed entry leaves no interface marked". The ACMP-13 row in `docs/TRACEABILITY.md` names the four `AcmpWalk` tests at L364, L369, L374 and L379, which match the `TEST_F` lines |
| R823-1-F3 / R824-1 F-1 (MINOR) parent consumer bar | RESOLVED by ruling item 3 (deferred to the milan-fpga pin move) | The PR body links the ruling (line 5). It states the code size, and I reproduced every figure on RV32: Debug `acmp.c` 21,429 to 22,189, smoke 51,964 to 52,652; Release 20,365 to 21,077, 41,645 to 42,337 (`receipts/r2/rv32-code-size.txt`); `struct acmp` +8 B at 16, 32 and 33 sinks (`receipts/r2/struct-size.txt`). It states the +132 B over-granule effect (123,012 B against 122,880 B), which matches milan-fpga#665 issuecomment-6778599191 item 5. I did not run the parent gates (deferred) |
| R823-1-R1 / R824-1 RES-2 (VERIFICATION.md plant description) | RESOLVED, R824-1's text as ruled | `docs/VERIFICATION.md:24` carries RES-2's exact text, the count 473, and sentences for the 4 + 3 new plants that match `tests/mutations.json` (25 walk plants, 477 entries) |
| R823-1-R2 (PR body plant sentence) | RESOLVED, exact text | PR body: "18 new plants, one for each mark site, the mark word's write and its read" |
| R823-1-R3 / R824-1 RES-3 (compilers in the PR body) | RESOLVED, R824-1's text as ruled | PR body, round 1 Validation: RES-3's sentence verbatim |
| R824-1 RES-1 (REQUIREMENTS.md mark order for restore) | RESOLVED, exact text | `docs/REQUIREMENTS.md:41-43` |
| R824-1 S-1 / R823-1-S1 | Taken (as F1). Partly for S1: a poll-first bias at 33 sinks only; the in-tree seed is still single | The author reports 24 extra seeds outside the tree. Not a finding |
| R824-1 S-2 (parent target figures) | Taken | The PR body quotes 18,782 of 22,170 cycles (issue #32 body) and #665's per-record costs and loads |
| R824-1 S-3 / R823-1-S2 (interface-mask width) | Taken in the test, as ruled (item 5) | `tests/test_acmp_walk.cpp:20`. The conditional gate refuses 33 interfaces and compiles 4 and 32 with GCC and Clang (`receipts/r2/conditionals-host.log`). With the assert removed, the gate fails "interface control at 33 interfaces with g++: rc 0" (`receipts/r2/r2-probes-results.json`). See R823-2-S2 |
| R823-1-S3 (cross-version differential) | Not taken; kept as a suggestion | My differential against `main`'s real core still passes: 480 cases, 0 divergent |

## Lens evidence

### Conformance (CLEAN)
- `src/` and `include/` are byte-identical to `9043b926`, so the round 1 conformance verdict holds.
- I reran my old-against-new differential unchanged: `main`'s real `src/acmp.c` against the head's at `ACMP_MAX_SINKS=33u` under `-fsanitize=shift,undefined`, at 1, 8, 32 and 33 sinks, lifted and unlifted, 60 seeds each. Result: 480 cases, 0 divergent (`receipts/r2/differential.log`). At 33 sinks with the lift, 68 change reports and 64 unbound publishes reach sinks at or above 32.
- ACMP-13's claim "completion clears every mark" now has an assertion that fails when it is broken (F2 above). ACMP-10's publish-before-response at sink 32 is now exercised by commands to that sink, and the second-word bind and unbind plants are caught.

### RTL / implementation (CLEAN)
- No implementation change in the delta, so the round 1 verdict holds.
- Bare-metal Debug and Release rc 0 at head and at `main` (`receipts/r2/baremetal-*.rc`). The code-size figures reproduce exactly.
- Hosted bare-metal jobs at the exact head executed and succeeded (runs 42992097714 and 42992108757).

### Robustness (CLEAN)
- F1 is resolved: sink 32's command, owed-release and probe-left paths are now differential-tested.
  - My probes `release-marks-folded-sink` (mark `k % 32`) and `sink32-marks-wrong-interface` are each caught by "the changed-sink walk makes the full walk's calls" at 33 sinks.
- The vacuity guards work. Each probe that undoes a round 2 lift fails a guard:
  - without the poll-first bias: "at 33 sinks the second mark word's sink sends an owed probe its timer waits for";
  - with room always present at 33 sinks: that guard plus "the random entries owe a sink's response".
- F3 is deferred by the ruling.
- Width check: test-side, as ruled (S2).

### Tests (CLEAN)
- Walk subset, `scripts/mutation.py --select walk- --jobs 12`: 25 CAUGHT, 0 escaped, 0 error (`receipts/r2/mutation-walk.log`). Each caught as `tests/mutations.json` names it.
- GCC Debug CTest: 10/10. Clang-sanitizer stand-in with the host's Clang 23.1.4: 10/10, `acmp_walk` included.
- My round 1 fault probes, rerun unchanged (`receipts/r2/probe-mutants-results.json`):
  - `bind-`, `unbind-`, `release-` and `probe-left-marks-only-word-zero` each fail `AcmpWalk.ThirtyThreeSinksMatchTheFullWalk`;
  - `marks-never-cleared` fails all four `AcmpWalk` tests;
  - the control passes;
  - the source file was restored, and its hash checked.
- Round 2 probes (`scripts/r2_probes.py`, `receipts/r2/r2-probes-results.json`): see Robustness and the resolution table.
- At 1, 8 and 32 sinks the draw sequence is unchanged. Every new draw is behind `wide &&` short-circuits, and `rng.below(cfg.n_interfaces)` is `below(2u)` there.
- Plant table audits rerun unchanged:
  - `plant_delta` and `plant_defects` output is byte-identical to round 1's receipts;
  - `plant_merge`: both parents' orders kept, no plant dropped, and the seven new plants are the only ones in neither parent.
- Author receipts (archive `bd10795e`, `author-r2`): `validate.rc` 0, 28 gates, mutation 477 CAUGHT / 0 ESCAPED / 0 ERROR, conditionals log with the three interface-control lines, `before.txt` and `after.txt` at the head and tree.
- Hosted quality job 130427239092, an executed job, not a skipped context: 28/28 gates rc 0, including `conditionals` and `mutation`. Its artifact `quality-evidence` (sha256 `adcd344b...`, equal to the digest in the job log) holds 477/477 CAUGHT, all 25 walk plants included (`receipts/r2/hosted-summary.txt`).

### Docs (CLEAN; RESIDUE R823-2-RES1)
- Checked against the head:
  - REQUIREMENTS: RES-1 text exact.
  - VERIFICATION: mutation row matches the 25 walk plants and 473 + 4; the conditional-regions row matches the gate's output.
  - TESTS and TRACEABILITY: line anchors L364 to L379 correct; plant lists match `tests/mutations.json` kill lists.
  - CHANGELOG: see RES1.
  - PR body: items 1 to 5 checked against the code and receipts as above.
- The ruling link in the PR body resolves to the ruling comment.
- Comment rule: the delta adds no source comment that names a bench lane, review round, reviewer or comment ID. The only new comment-like text is the `interface_controls` docstring, which states behaviour.
- The PR body names lanes and reviewers, which is allowed there.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src`/`include` identity to `9043b926`; ACMP-13 text; old-against-new differential 480/0; second-word bind and unbind plants | R823-1 (core) + R823-2 (delta) | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| RTL / implementation | CLEAN | no core change; RV32 Debug and Release builds, code size and `struct acmp` size reproduced; hosted bare-metal executed | R823-1 + R823-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Robustness | CLEAN | `test_acmp_walk.cpp` 33-sink paths; probes on the third interface, folded release and clear; vacuity guards; width static_assert and its control | R823-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Tests | CLEAN | walk campaign 25/25; GCC and sanitizer CTest 10/10; round 1 fault probes and plant audits rerun; author 477/477; hosted 477/477 and 28/28 | R823-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |
| Docs | CLEAN (RESIDUE RES1) | CHANGELOG, REQUIREMENTS, VERIFICATION, TESTS, TRACEABILITY, PR body, ruling link, comment rule | R823-2 | a530ecafe7e503a57c81a5aba4ffe38fa8f37e7e |

## Real limits
- Compiler for the conditional gate: I used the host's Clang 23.1.4 as `clang` and `clang++`, with the pinned Clang 18.1.3 as `clang-18` for the token checks.
  - With the pinned Clang 18.1.3 as `clang++` (round 1 shim), the gate is rc 1 on this host at the interface control's first case, from libstdc++ 16 header errors. This matches the author's note.
  - The hosted image, Clang 18.1.3 with its own C++ library, passes the gate.
- The sanitizer stand-in also used the host's Clang 23.1.4. The GCC CTest build used the host's GCC 16.2.1.
- I did not rerun the full `validate.py` or the full 477-plant campaign. They rest on the author's published receipts and the hosted artifact. I ran the 25 walk plants.
- How my round 1 scripts were run: unchanged, with hashes equal to the archive's `scripts.sha256`, directly in the foreground. I did not use `launch.sh`, which detaches. Concurrent jobs ran inside one foreground command (`scripts/r2_campaign.sh`).
- I did not run the other reviewer's scripts. Their rerun at this head is the author's published receipt.
- The parent consumer bar (firmware gates, ROM granule) is deferred by ruling and was not verified here.
- No manager source bank ran at this head, and I claim none.
- Physical calibration NOT RUN. No hardware was used. Field skips are not hardware proof.
- The archive commit `bd10795e` carries no GPG signature. I verified its `MANIFEST.json` instead: 450 entries, 0 hash mismatches, no unlisted or missing files; 5 entries path-redacted, all in round 1 reviewer files.

## Pending manager duties
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn: source base `9deb0ddb`, live dev `46c971fa0a09e2c8ca21acb95769defdc06c3068`. Link its receipts on the PR.
- Hosted/act acceptance at the exact head.
- Carry R823-2-RES1 to the residue checklist.
- The milan-fpga pin move that carries #28, #31 and #32: run every parent firmware gate at the moved pin, and settle the 132 B over-granule debt of the 8x8/2if `answering-every-port` image (milan-fpga#665).
- The second independent review at this head.

## Packet
- `scripts/`: my round 1 scripts, unchanged, plus `r2_campaign.sh` and `r2_probes.py`.
- `receipts/r2/`: raw logs, rc files, JSON results, integrity.
- Review clone integrity (`receipts/r2/integrity.txt`): head and tree as above, worktree and index equal to HEAD, 0 untracked or ignored files, 0 gitlinks, `.gitmodules` absent. The probe trees were exports under `scratch/`, and the mutated tree's `src/acmp.c` hash was restored to the head's.

R823-2 FINISHED
