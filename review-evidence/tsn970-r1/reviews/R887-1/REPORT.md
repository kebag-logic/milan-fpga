[R887] NEGATIVE - exact head 5d14a6d816a43a49299172a34e3eeaea44c267c6

# R887-1: independent internal review of kebag-logic/tsn-c-stack PR #35 (for kebag-logic/milan-fpga#970)

## Scope and identities

| Item | Value |
|---|---|
| Stack head under review | `5d14a6d816a43a49299172a34e3eeaea44c267c6`, tree `2112d0526c8f5ab49440e89202af526b1b9b65fc` (verified in the clone) |
| Stack base | `715589c1db7cf67e2f3259fd7083ebc7f0923376`; delta is two one-line-subject commits, `7e03f71c` and `5d14a6d8` |
| Parent consumer | milan-fpga `27495a06d5569336a098da20381ced3e331ba665`, five commits on the flip PR's reviewed head `dd163e414` |
| Parent gitlink | `third_party/tsn-c-stack` at `5d14a6d816a43a49299172a34e3eeaea44c267c6` (`git ls-tree 27495a06d third_party/`) |
| Evidence tree | milan-fpga `134345784d83af67316c82ac8495d89a489e604e`, `review-evidence/tsn970-r1/author-r1` (HANDOFF-r1.md sections 2 to 5 and `receipts/`) |

I rebuilt the task from these sources, in this order: the stack's CONTRIBUTING.md and docs (VERIFICATION, PORTING, REQUIREMENTS, TRACEABILITY, TESTS); the parent's AGENTS.md; the issue body (its acceptance list) and its two public comments (the take-over and the review-ready notes); PR #35's body; the FR_NFR rows the parent cites; then `git diff 715589c1..5d14a6d8` with each commit, and `git diff dd163e41..27495a06` for the parent; then the published evidence.

**Prior public findings.** PR #35 has only the two review-start comments, and the issue has no review findings. No earlier finding needs to be resolved or kept at this head.

## Verdict summary

One MINOR finding, F1 (Tests), is open, so the verdict is NEGATIVE. Conformance, RTL, Robustness and Docs are clean. Every behaviour the issue asks for is correct at this head and reproduced here:
- The first ENTITY_AVAILABLE comes 0 to 0.5 s after LINK_UP and after a startup with the link up.
- A grandmaster change before the first frame is carried by it, and one after it re-advertises.
- Every other draw stays 0 to 4 s.

F1 is a gap in the stack's own sensitivity. The PR now states that a GM_CHANGE in WAITING keeps the 0 to 4 s draw. It states this in the requirement, the change log and the porting guide. No assertion in the stack's suite holds that statement. A planted wrong draw kind at that call site passes all 10 stack test binaries. Only the parent's walk catches it.

## Findings

### F1 MINOR (Tests): the stack's suite does not hold the GM_CHANGE draw kind that MFDISC-01 now states

- **Where:**
  - `src/adp.c:283`: `adp_gm_change`, `enter_delay(a, ADP_DRAW_DELAY)`.
  - `tests/test_adp.cpp:141-143`: A2 in `AdpCore.A0toA2Schedule`, the MFDISC-01 test for GM_CHANGE. It checks only that a third frame is sent.
  - `docs/requirements.json:311` and `docs/REQUIREMENTS.md:176`, MFDISC-01: "draw every other delay from 0 to 4 s".
  - `CHANGELOG.md:5` and `docs/PORTING.md:195`: "GM_CHANGE in WAITING draw from zero to four seconds".
- **Authority:**
  - The stack's CONTRIBUTING.md: "A protocol change updates its requirement, tests and traceability. A regression needs a failing assertion and a runnable planted defect."
  - Milan v1.2 5.6.3.5.7 and Table 5.50: TMR_DELAY on a GM_CHANGE in WAITING.
  - `docs/TRACEABILITY.md:32` traces MFDISC-01 only to `AdpCore.A0toA2Schedule`, `A9DrawKinds` and `A10toA14DepartingIndex`.
- **Evidence (`receipts/stack-probes.json`, `receipts/stack-probe-gm-link-up-full-ctest.txt`, `receipts/parent-adp-probe-gm-*.json`, `receipts/parent-arm-gm-*-walk.log`):**
  - With the PR's new third kind, a wrong kind is now possible at each draw site. The PR pins the kind at the other four sites:
    - LINK_UP: A0, A18, A20 and A9;
    - startup: A3 and A9;
    - DISCOVER: A4, and the `valid discovery uses the normal delay range` parameter test;
    - TMR_ADVERTISE: A9.
  - Swapping `ADP_DRAW_DELAY` for `ADP_DRAW_LINK_UP` (or `ADP_DRAW_STARTUP`) at `src/adp.c:283` leaves the stack's `adp_tests` passing. So does the stack's whole ctest set, 10 of 10.
  - With that plant, the parent's ADP arm also passes. G4 still passes because it only bounds the change-to-frame delay by 4 s: "the new grandmaster's the latest 500 ms after the change".
  - Only the parent's walk catches it: `Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING: GM_CHANGE x WAITING: the draw is the 0..4 s kind`.
  - Control: the matching plant at the DISCOVER site is caught by A4 and by the discovery-window test.
- **Impact:**
  - The stack merges and is validated on its own gates before the parent moves its pin.
  - Its 482-plant campaign and its MFDISC-01 trace would accept a GM_CHANGE re-advertise drawn from 0 to 0.5 s. That would contradict the requirement text this PR adds and shorten the storm-avoidance spread of the re-advertisement on a network-wide grandmaster change.
  - Any consumer of the stack other than this parent's walk would not see it.
- **Required outcome:**
  - A stack test linked to MFDISC-01 must fail when the GM_CHANGE draw in WAITING is not the 0 to 4 s kind. For example, after `adp_gm_change` in A2, require `a.last_draw == ADP_DRAW_DELAY` and `fk.last_delay == a.last_draw_ms`, with the range against the literal 4000.
  - A named plant in `tests/mutations.json` must exercise it, for example `gm-change-draws-link-up-kind`.
  - Regenerate `docs/TESTS.md` with `test_inventory.py --write`, and update the plant counts in VERIFICATION.md and the PR body (478 to 479 core, 482 to 483 in all).
- **Verification:** `python3 scripts/mutation.py --work <w> --jobs 16` shows the new plant CAUGHT by its named words, with 483 of 483 caught. Running `scripts/stack_probes.py` from this packet at the new head reports `gm-change-draws-link-up-kind` and `gm-change-draws-startup-kind` as caught. The parent's walk still catches it.

### S1 SUGGESTION (Robustness, RTL): guard the first-draw maxima against the clauses at compile time

`include/adp.h:87-88`. The tests use literals (500 and 4000), so a planted header change is caught today (plants `startup-range-two-seconds` and `link-up-range-four-seconds`). A compile-time check would make the conformance limit part of the build for any integrator who edits the header:
- `ADP_DELAY_STARTUP_MAX_MS <= 2000u` (Milan v1.2 5.6.3.5.2);
- `ADP_DELAY_LINK_UP_MAX_MS <= ADP_DELAY_MAX_MS` (5.6.3.5.3, Table 5.50).

This is optional and does not affect the verdict.

### S2 SUGGESTION (Docs): label the twelve budget-image pairs in the author's image summary as hash-only

In `review-evidence/tsn970-r1/author-r1/receipts/images/SUMMARY.txt`, the twelve `budget-*` rows read `rc 1`. Their `pairs/*.imgdiff.txt` and `*.relink.txt` files are tracebacks, because those images have no `ctrl_app.map`. The handoff and the PR text claim only hashes for those images, and the hashes differ as the `adp.o` change predicts. So the claim is not overstated, but a cold reader sees twelve failures. This is optional evidence presentation.

## Rulings on the five requested checks

### (1) The cause: confirmed and reproduced on the base stack

- **Core, standalone** (`scripts/probe/draw_probe.c`; `receipts/draw-probe-base.txt`, `receipts/draw-probe-head.txt`; 100,000 draws of each kind, random seeds):

  | Draw | Base `715589c1` | Head `5d14a6d8` |
  |---|---|---|
  | LINK_UP, maximum | 4000 ms | 500 ms |
  | LINK_UP, draws of 500 ms or less | 12.6 % | 100 % |
  | Startup with the link up, maximum | 2000 ms | 500 ms |
  | TMR_ADVERTISE redraw, maximum | 4000 ms | 4000 ms |

- **Parent host tests on the base stack** (`scripts/parent_adp_probe.py`, `receipts/parent-adp-probe-base.json`, `receipts/parent-arm-base-adp.log`). G1, G2, G3 and G4 fail by their own words:
  - G1: the latest first ENTITY_AVAILABLE is 3990 ms after LINK_UP;
  - G2: 1981 ms after a startup;
  - G3: 3649 ms with a grandmaster change inside the delay;
  - G4: 3364 ms with a change 4.5 s after LINK_UP.

  These are the author's figures exactly.
- **At head** (`receipts/parent-adp-probe-head.json`), the same tests pass:
  - G1: 499 ms, 56 distinct delays;
  - G2: 496 ms, 32 distinct;
  - G3: 457 ms;
  - G4: 421 ms, and the new grandmaster announced within 3994 ms;
  - G5: TMR_ADVERTISE delays up to 3966 ms.
- **Nothing else holds the first frame back:**
  - In the core (`src/adp.c:263-266`), LINK_UP from DOWN goes straight to `enter_delay`, and the frame is built at expiry (`advertise`, `src/adp.c:161-171`).
  - In the adapter, G1 and G2 bound the whole path from the LINK post to the frame on the mailbox model at the draw plus at most 2 ms.
- The 1.8 to 2.8 s the bench saw beyond the draw is a separate issue, as the task scopes it.

### (2) Conformance of the [0, 0.5 s] draw: conformant, and the storm-avoidance intent is kept

- **Milan's own timer.** For a PAAD-AE interface, Milan v1.2 5.6.3 defines the advertising machine (Tables 5.49 to 5.51). Its TMR_DELAY is "a random value between 0 and 4 seconds" (Table 5.50; 5.6.3.5.3 on LINK_UP, and 5.6.3.5.4, .5 and .7). At a startup with the link up it is a random value between 0 and 2 seconds (5.6.3.5.2).
  - The wording constrains the range of the value and that it is random. It sets no distribution and no lower bound on the spread.
  - A uniform draw over [0, 500] ms (`src/adp.c:62-63`: 16 random bits scaled to 0..500 inclusive, about 131 random states per millisecond value) is a random value inside both [0, 2 s] and [0, 4 s].
  - The head is therefore within 5.6.3.5.2 and 5.6.3.5.3.
- **The 1722.1 delay belongs to a machine Milan replaces.** IEEE 1722.1-2021 6.2.4.2.2's randomDeviceDelay draws uniformly over 0 to valid_time/5 (4 s at valid_time 10). It belongs to the Advertising Entity state machine of 6.2.4. For a Milan entity, the per-interface machine of Milan 5.6.3 replaces 6.2.4 and 6.2.5 for advertising. 6.2.4.2.2's whole-range uniform draw is therefore not the governing rule. Under Milan's wording, a narrower random range is a permitted choice.
- **The other draws are unchanged.** DISCOVER, TMR_ADVERTISE and GM_CHANGE in WAITING keep `ADP_DRAW_DELAY`, 0 to 4000 ms (`src/adp.c:283, 301, 333`). Both the standalone probe and the parent's walk show this.
- **Storm avoidance** (`receipts/draw-probe-head.txt`; N entities with random IDs and seeds, one common LINK_UP):

  | Entities | Last first frame | Most in one 1 ms slot | Most in one 10 ms window | Base (1 ms / 10 ms) |
  |---:|---:|---:|---:|---|
  | 1024 | 500 ms | 7 | 33 | 3 / 7 |
  | 256 | 499 ms | 4 | 15 | not recorded |

  - The first frames are still spread at random and decorrelated by entity ID and the port seed.
  - The densest millisecond carries 7 frames of 82 bytes, under 0.1 % of a 100 Mb/s link.
  - The burst a controller sees is about 8x denser, but still spread over 0.5 s.
  - After the first frame, every redraw is 0 to 4 s again, so the steady state is unchanged.
  - The near-identical startup draw across reboots of one entity (handoff section 8, item 3) existed before this PR. It does not reduce the spread between entities.
- **Ruling:** conformant, with the storm-avoidance intent kept. See the limits section for the clause-text caveat.

### (3) The grandmaster: correct in both orders

- **Before the first frame (DELAY):** `adp_gm_change` acts only in WAITING (`src/adp.c:282`). A change in DELAY therefore leaves the running delay alone (Table 5.51). The frame samples the gPTP pair when it is built (`src/adp.c:102`, IEEE 1722.1-2021 6.2.2.16), so the first frame carries the new grandmaster.
  - Probe: delay unchanged, first frame grandmaster `0xB`.
  - Parent G3: 32 runs, the first frame carries the new grandmaster within 457 ms.
- **After the first frame (WAITING):** the change starts a 0 to 4 s `ADP_DRAW_DELAY` (5.6.3.5.7), then sends a new ENTITY_AVAILABLE with the new grandmaster and the next available_index.
  - Probe: kind 2 (`ADP_DRAW_DELAY`), 2237 ms, grandmaster `0xC`, index 1.
  - Parent G4: within 3994 ms.
  - The parent's walk `GM_CHANGE x WAITING` cell holds the kind. The stack does not hold it: see F1.

### (4) Tests, plants, generated docs, clang-tidy and the stack's own gates

- **A0, A3, A9, A18 and A20** are restated against `kFirstDrawMaxMs` 500 and `kDelayDrawMaxMs` 4000 (`tests/test_adp.cpp:19-20`), not against the header names, so a planted header constant is seen. A9 now covers three kinds, and over 400 deterministic iterations each kind comes within 10 % of its maximum.
- **The 5 new plants and 2 restated ones** (`tests/mutations.json`) are each CAUGHT by their named words in the campaign: `link-up-draws-delay-kind`, `link-up-range-is-the-delay-range`, `every-draw-the-first-range`, `startup-range-two-seconds`, `link-up-range-four-seconds`, and the restated `link-up-draws-startup-kind` and `draw-kinds-merged`.
  - Total: 482 of 482 CAUGHT, 0 escaped (`receipts/stack-validate-5d14a6d8/mutation-results-summary.txt`).
  - My extra plants (`receipts/stack-probes.json`) at three ranges (LINK_UP 1000 ms, startup 1000 ms, the delay 500 ms), at the startup kind and at the DISCOVER kind are all caught. Only the GM_CHANGE kind escapes (F1).
- **Generated docs:** in a fresh clone at the head, `traceability.py --write` and `test_inventory.py --write` leave the tree unchanged, with 47 requirements, 185 declarations and 482 plants (`receipts/regen-docs.txt`). So REQUIREMENTS, TRACEABILITY and TESTS are what the generators produce. The `traceability` gate also passes inside validate.
- **clang-tidy 18.1.3:** at `7e03f71c` it refuses `src/adp.c:56` (`bugprone-branch-clone`, `receipts/clang-tidy-7e03f71-adp.txt`). At the head, the static-analysis gate (cppcheck plus clang-tidy) is rc 0.
- **The stack's own gates:**
  - `python3 scripts/validate.py --work <w> --jobs 12 --graphs`: rc 0, 28 of 28 gates rc 0 (`receipts/validate-head.log`, `receipts/stack-validate-5d14a6d8/gates.json`). This includes:
    - coverage at 100 % lines and branches after exclusions, with `src/adp.c` 209/211 lines and 99/106 branches;
    - the address and undefined-behaviour sanitizers;
    - the comments, port-contracts and conditionals gates;
    - privacy, with 52 commits, 465 historical blobs and 100 files.
  - `python3 scripts/baremetal.py`: rc 0 (`receipts/stack-validate-5d14a6d8/baremetal-results.json`).
  - Both commit messages are one line, with no body or trailer.
- **Hosted evidence at the exact head** (`receipts/hosted-check-runs-5d14a6d8.txt`, read only): "Portable core quality" ran on push and on pull_request, `quality` and `bare-metal` both completed successfully, and no step was skipped. Hosted acceptance remains the manager's.

### (5) The parent consumer at 27495a06

- **Gitlink and pin records:**
  - The gitlink is at `5d14a6d8`.
  - SUBMODULES.md, the firmware README's `adp.h` link and MAILBOX_SPLIT.md's `adp.h` link name `5d14a6d8`.
  - `scripts/check_submodule_docs.py` reports OK (6 exact gitlinks).
  - The diagram generator's `--check` reports OK (decoded PNG).
  - `scripts/check_doc_style.py` reports OK (25 documents).
  - Receipts: `receipts/parent-doc-checks.txt`, `receipts/parent-submodule-diagram-check.txt`.
- **Group G and the walk:**
  - At head, the ADP arm passes with G1 to G5, and so does the walk arm.
  - The walk's LINK_UP x DOWN cell (`sw/firmware/ctrl/test/adp_walk.cpp:268-277`) expects `ADP_DRAW_LINK_UP`. Every other drawing cell expects `ADP_DRAW_DELAY`.
  - The comment's "one difference from the processor's T-ADP-DELAY" is accurate: the processor's startup draw is a separate kind, T-ADP-DELAY-START (`protocol-processor/hdl/adp/pp_adp_pkg.sv:56-57`).
  - G3 and G4 test the two grandmaster orders against literals: 1000, 500, 4000 and 5000 ms.
- **The parent's plants** (`scripts/parent_plants_probe.py`, `receipts/parent-plants-probe.json`): the 8 plants of `adp_first_mutants.py`, plus `gm-change-ignored` with its new G4 kill, were each planted into a copy of the pinned stack and rebuilt. Each was CAUGHT, 9 of 9, by every named (arm, test, words) kill.
- **FR_NFR** (`docs/reference/FR_NFR.md:415-416`):
  - Only the two derivation rows' text changes. The split's 0.5 s windows give 50 ms against the 20 ms `T_svc`.
  - ADP's 30 ms row bound, the ceiling table's `ADP | 200 ms | 20 ms` row and the 4.5 s figures are unchanged.
  - No `ctrl_loop.h` or budget constant is in the diff.
- **Firmware gate, CPU budget rows and images:** taken from the author's published receipts, checked for consistency, not re-run here.
  - Firmware gate: all four shards PASS at `27495a06`, and the control campaign catches 832 of 832.
  - CPU legs: 63 of 63 probes paired, 0 verdicts changed, 0 misses, largest difference −0.074 ms at 1x1/1if and +0.097 ms at 8x8/1if, each against 20 ms. The CPU table graders give byte-identical output.
  - Images: 8 platform and fixture pairs, where only `adp.o` and `.text.enter_delay` (176 to 180 bytes) differ, in 5 canonical lines. RAMB36 is unchanged at 45, 46, 58 and 63.
  - First ENTITY_AVAILABLE on the real CPU with the mailbox RTL: 91.142 ms at 1x1/1if and 89.366 ms at 8x8/1if, against 730.108 and 719.315 ms on the base.
  - My attempt to run the gate's suite phase in the foreground was stopped at 590 s, during its builder step (`receipts/parent-fw-gate-head.log`, rc 124). I ran the ADP and walk arms directly instead.
- **Comment rule:** the added source comments in both deltas carry clause and issue IDs only. They contain no bench lane labels, lane names, review rounds, reviewer IDs or comment IDs. "The bench's order" in G4's comment is a plain description. So there is no residue.

## Lens results (artifact-specific)

- `[R887] PASS Conformance`: `src/adp.c:53-68, 247, 263-266, 282-284, 298-301, 332-333`; `include/adp.h:84-117`; issue #970 acceptance list.
  - Checked against Milan v1.2 5.6.3.5.2, .3, .5, .7, .9 and Tables 5.49 to 5.51, and IEEE 1722.1-2021 6.2.2.15, 6.2.2.16, 6.2.4.2.2 and 6.2.5.
  - The draw ranges sit inside the clause ranges, the GM_CHANGE orders are correct and available_index is kept.
  - Acceptance items 1 to 3 are met on the host and the harness. Item 4, the bench re-run, belongs to the manager.
- `[R887] PASS RTL`: no HDL file in either delta (`git diff --stat` of both).
  - The C architecture is sound:
    - `r16 * (max_ms + 1)` stays at or below 2.62e8, so it does not overflow;
    - `ADP_DRAW_LINK_UP = 3` is appended, so existing enum values and the struct layout are unchanged;
    - no firmware outside the tests reads `last_draw`.
  - Images and RAMB36 are unchanged except `adp.o`, and the CPU rows are unchanged (author receipts).
- `[R887] PASS Robustness`: `src/adp.c:253-274, 276-285, 148-171`; `tests/test_adp.cpp` A18, A20 and A19.
  - A zero draw arms a 0 ms timer, which FR_NFR services immediately.
  - Link flaps, departures owed across a link loss, inputs while disabled, a GM change in DOWN or DELAY, and a send that is refused (the frame stays owed and the grandmaster is sampled when it is built) all behave correctly.
  - The kind check is idempotent across re-enable.
  - S1 is optional.
- `[R887] FAIL Tests`: F1 (`tests/test_adp.cpp:141-143`, `src/adp.c:283`). Otherwise A0, A3, A9, A18 and A20, the 7 stack plants, G1 to G5, the walk, and the 9 parent plants were each verified to fail on the defect they name.
- `[R887] PASS Docs`: `CHANGELOG.md:5`, `docs/PORTING.md:184-196`, `docs/REQUIREMENTS.md:176`, `docs/requirements.json:311-319`, `docs/VERIFICATION.md:24` (478 + 4 = 482 plants), and the generated TESTS and TRACEABILITY, which regenerate with no change. Parent: MAILBOX_SPLIT.md:530-544, FR_NFR.md:415-416, SUBMODULES.md, README, CHANGELOG, and the diagram (its generator check reports OK). S2 is optional.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/adp.c`, `include/adp.h`, the Milan v1.2 5.6.3 clauses and the 1722.1-2021 6.2.2.16, 6.2.4.2.2 and 6.2.5 readings, `receipts/draw-probe-*.txt`, G1 to G4 at head and base | R887-1 | stack `5d14a6d8` / parent `27495a06` |
| RTL | CLEAN | both diffstats (no HDL), `src/adp.c:53-68` arithmetic, `include/adp.h:112-117` enum, author image, ledger and CPU receipts | R887-1 | stack `5d14a6d8` / parent `27495a06` |
| Robustness | CLEAN | `src/adp.c` link, enable, GM, expiry and owed paths; A18 to A21; the storm spread probe | R887-1 | stack `5d14a6d8` / parent `27495a06` |
| Tests | UNCLEAN (F1) | `tests/test_adp.cpp`, `tests/mutations.json` (482 caught), `receipts/stack-probes.json`, parent `test_adp.cpp` G, `adp_walk.cpp`, `adp_first_mutants.py` (9 of 9 caught) | R887-1 | stack `5d14a6d8` / parent `27495a06` |
| Docs | CLEAN | stack CHANGELOG, PORTING, REQUIREMENTS and requirements.json, VERIFICATION, regenerated TESTS and TRACEABILITY; parent MAILBOX_SPLIT, FR_NFR, SUBMODULES, README, CHANGELOG, diagram | R887-1 | stack `5d14a6d8` / parent `27495a06` |

## Commands run (all inside the review clone or this packet's scratch)

- Stack, exact head:
  - `python3 scripts/validate.py --work <packet>/scratch/val-head --jobs 12 --graphs`: rc 0.
  - `python3 scripts/baremetal.py --work <packet>/scratch/rv32-head --jobs 4`: rc 0.
  - Both run with the pinned GoogleTest 1.14.0 and clang-tidy 18.1.3 (`scripts/env.sh`).
- Generated docs: `traceability.py --write` and `test_inventory.py --write` in a fresh clone, with `git status` empty afterwards.
- Probes:
  - `scripts/probe/draw_probe.c`, built against the base and head `src/adp.c`;
  - `scripts/stack_probes.py` (8 variants);
  - `scripts/parent_adp_probe.py` (head, base stack, and the two GM-kind plants; ADP and walk arms only);
  - `scripts/parent_plants_probe.py` (the parent's #970 plants).
- Parent copies: shallow scratch copies of milan-fpga `27495a06` with the pinned stack, lwSRP `08ee86e8`, protocol-processor `801ef228` and gptp-processor `1616fc8f`.
- Hosted evidence: read-only GitHub API queries for the check runs and jobs at `5d14a6d8`.
- Restore: the review clone is at `5d14a6d8`, tree `2112d052`. Its index writes tree `2112d052`, and the working-tree bytes equal the index blobs. The stack has no gitlinks. The only stray file was the run's ignored `scripts/__pycache__`, which I removed (`receipts/clone-integrity.txt`).

## Real limits

- **Clause text.** Neither the Milan v1.2 nor the IEEE 1722.1-2021 PDF is on this host, and the public download was refused. The conformance ruling rests on the clause wording as both repositories quote it, consistently: the stack's header comments at the base, the parent's FR_NFR rows, and the issue. It also rests on my reading of how 6.2.4 and 6.2.5 relate to Milan 5.6.3. A reader holding the PDFs should confirm two things:
  - that Table 5.50's TMR_DELAY wording sets no distribution;
  - that 5.6.3 replaces 6.2.4.2.2 for a PAAD-AE.

  I could not check which clause the PR body's "Table 5.50: ... between 0 and 2 s" cites, so I record no finding on it.
- **What I did not run.** I did not run the parent's full firmware gate, its `--self-test` campaign shards (832 plants), the twin, the split boot simulation, the CPU budget legs, the image ledger, builder legs or docs workflow. Those are consumer banks outside a focused review, or past the foreground time limit. For them I relied on the author's published receipts at `27495a06` and `b000faa5`, checked for internal consistency.
- **No hardware.** There was no hardware, no physical calibration and no bench run. Host and harness timings are not bench proof.
- **The manager's runs.** No manager source bank exists or was inferred at this head. The current-dev merge candidate (source base `715589c1`, live dev `e275d795`) is the manager's to build.

## Pending manager duties

- Carry F1 to the author. Re-review the corrected stack head, then the parent's pin move to the stack's merge commit and the five pin records it moves.
- Build and validate the current-dev merge candidate (builder and native banks), and publish its receipts on the PR.
- Hosted and act acceptance at the exact heads.
- The bench re-run of the affected scenarios after merge, which is issue #970 acceptance item 4.
- File the recommended separate issue for the boot-path autonegotiation restart, the 1.8 to 2.8 s beyond the draw.

R887-1 FINISHED
