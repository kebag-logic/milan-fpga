# [A750g] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 6

Status: REVIEW READY at 376486b374782147d71e5e9bb4f93c42cd10e636. All 28 gates and `baremetal.py` (Debug and
Release) return 0 on a clean clone of that head.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Start head: 715d20804fd3438edf990c393bf1b0c6e328dede (round 5, pushed).
- Authority: the round 6 ruling on PR #28 (issuecomment-6728504171), items 1 to 4.
- Round 6 adds two commits. There was no rebase, force or amend. Each commit is authored and committed by
  hackerman-kl <hackerman-kl@kebag-logic.com> and has a one-line subject with no body or trailers.
  1. `c0477c8` State that a held probe has no wait bound: it takes a freed slot only at timer service with no
     BIND_RX waiting, after every command the core takes first, kept or offered for the first time (ruling items
     1, 2 and the pins of item 3)
  2. `376486b` Assert that a GET_RX_STATE offered after the accepting poll that follows the taken BIND_RX delays
     the held retry one pass, and plant a held probe owed at that poll (ruling item 3)
- No core change: `git diff --stat 715d208 376486b -- src include examples` is empty.
- Files changed (7, +99/-18): PORTING, VERIFICATION, the generated TESTS and TRACEABILITY,
  `scripts/check_port_contracts.py`, `tests/test_acmp.cpp` and `tests/mutations.json`.
- Not pushed, and no PR was opened or edited. The PR text is in `PR-BODY.md`: the current body, corrected in place
  where round 6 removes or changes a sentence, plus a Round 6 section. Its first line is "[A750g]" and it says
  "Relates to #26".
- Issue #26: "[A750g] TAKEN" was posted at the start (issuecomment-6728520660). "[A750g] REVIEW READY 376486b…" is
  posted at the end (issuecomment-6728747832).

## Ruling items and dispositions

| Item | Disposition |
|---|---|
| 1. Remove the held-probe wait bound and state four facts instead (PORTING and PR body Round 4 item 3, Round 5 item 3) | Done. `docs/PORTING.md:110` drops the "waits at most" sentence, the per-sink count, the TMR_NO_RESP (200 ms) condition, the "past that" list and "These counts assume passes at least 1 ms apart", which qualified only those counts (the 1 ms condition is still stated at `:90`). It now reads: "A held probe is never dropped for want of a slot, and it takes a freed slot only at timer service with no BIND_RX waiting, after every command the core takes first, whether kept or offered for the first time, so no command answer waits for it. Its wait has no upper limit while commands keep taking the freed slots; its own TMR_NO_RESP runs from when it leaves." The command bound (`:107-:109`) and the budget (`:111-:113`) are unchanged. PR body: Round 4 item 3 and Round 5 item 3, and also Round 3 item 1's delay sentence (which repeated the bound), its freed-slot sentence, the How to validate entry for the round 3 test, and the Round 5 probe-table row that cited the removed clause. |
| 2. PORTING :92 and :94 in R794-5's wording | Done, word for word. `:92` "…held probes take freed slots one per pass, after the commands the port still keeps or offers before its timer service." `:94` "While the port keeps or offers commands that take the freed slots, or no owed frame is accepted, a held probe keeps waiting: …" |
| 3. Pins, named assertion, plant, removals | CRITICAL (`scripts/check_port_contracts.py:291-296`, `:299-311`) drops the six pins of removed or changed clauses and pins eight phrases of the new text. The self-test refuses 77 meaning-removal controls, up from 74. New test and plant are below. No test or plant is removed (see "Removals"). |
| 4. RES9 (R794-5) | Done in PR body Round 5 item 4: "a probe that falls due then, with no probe held, is lost". RES8 of both reviews went with the removed clause. |

Further change, needed by item 1:

- The three probing-restart paths (an ADP re-advertisement that does not raise the available index, a new
  discovery after its talker departs or its advertisement times out, or `acmp_tk_unregistered`) qualified the
  removed count. The gated-port sentence (`docs/PORTING.md:114`) also uses "probing restarts" and would have been
  left without a definition. So the parenthesis moved there unchanged, and its two pins moved to the
  `acmp_rx_ready` pins. The gated port's count and budget are unchanged.

Not taken (outside the ruling), and listed in the PR body:

- R793-5 RES9, to add "while no sink's probing restarts" to the integration note's gated-port sentence.
- The optional RV32 smoke step (R793-4 S7, R794-4 S8).

### Removals

- No test and no plant is removed, because none asserts a removed bound.
- `ProbesFallingDueInTheDrainWaitForTheDeferredBind` asserts "each held probe is owed in the pass after the BIND_RX is
  taken, one pass per probe before it". That is the exact pass when no command follows the BIND_RX. The retained
  sentence "Held probes follow the frames of the last kept command, one per pass" and the new "after every command
  the core takes first" still state it.
- Its plants `owed-hold-rearmed-late` and `owed-hold-at-seven` stay registered. In the sentence map they now pin the
  new held-probe sentence.

### CRITICAL pins

- Dropped from `probes_held`:
  - "after the commands still kept"
  - "through the pass that takes the BIND_RX"
  - "These counts assume passes at least 1 ms apart"
  - "at most one per other sink while no sink's probing restarts"
  - "the held probe has waited less than TMR_NO_RESP (200 ms)"
  - "past that, another sink's TMR_NO_RESP retry can also be owed before it"
- Moved from `probes_held` to `acmp_rx_ready`:
  - "an ADP re-advertisement that does not raise the available index"
  - "a new discovery after its talker departs or its advertisement times out, or `acmp_tk_unregistered`"
- Added:
  - to `acmp_rx_ready`: "at most one per sink while no sink's probing restarts";
  - to `probes_held`: "after the commands the port still keeps or offers before its timer service", "While the port
    keeps or offers commands that take the freed slots, or no owed frame is accepted", "A held probe is never dropped
    for want of a slot, and it takes a freed slot only at timer service", "with no BIND_RX waiting, after every
    command the core takes first", "whether kept or offered for the first time", "so no command answer waits for
    it", "Its wait has no upper limit while commands keep taking the freed slots" and "its own TMR_NO_RESP runs from
    when it leaves".
- Count: 74 − 6 + 1 + 8 = 77 controls.

## Changes (file:line at 376486b)

- `docs/PORTING.md:92`, `:94`, `:110` and `:114` (above).
- `scripts/check_port_contracts.py:291-296` (`acmp_rx_ready`) and `:299-311` (`probes_held`).
- `tests/test_acmp.cpp:3491-3546` `CommandOfferedAfterTheTakenBindDelaysTheHeldRetry`. Its only comment is
  `// REQ: ACMP-12, ACMP-09`.
- `tests/mutations.json:2742` `owed-held-probe-owed-at-the-poll`. That makes 444 plants: 440 core and 4 generated.
- `docs/VERIFICATION.md:24` 440 core plants.
- Generated: `docs/TESTS.md:118` (the new row; the Wire anchor moves to `#L3549`) and `docs/TRACEABILITY.md`
  (ACMP-09 and ACMP-12 rows list the new test). The coverage ratchet is unchanged (`src/acmp.c` 813/813 lines and
  424/424 branches).
- ACMP binary: 126 tests (125 ACMP plus main's Wire test), up from 125.

## Test, plant, and escape

| Test | Proves | Plant it kills (registered) | Escape without it |
|---|---|---|---|
| `CommandOfferedAfterTheTakenBindDelaysTheHeldRetry` | Sink 2's TMR_NO_RESP retry is held beside a kept BIND_RX, which is taken in pass 2. Then 0, 1 or 3 GET_RX_STATE are offered for the first time, one after each accepting poll, and each is taken at once ("…takes the freed slot"). The retry is owed in pass 2 + 1 + later (3, 4, 6): "after the BIND_RX is taken, a GET_RX_STATE offered after the next accepting poll delays the held retry one pass". Every answer leaves before the retry ("no command answer waits for the held retry"). `probes_lost` is 0 and TMR_NO_RESP = the retry's send time + 200 ms. | `owed-held-probe-owed-at-the-poll`, with both needles | Escapes: under the plant the full binary fails only this test, and without it 125 of 125 pass (rc 0). That is shown by three independent runs: the scratch trial before registration (`receipts/plant-trial/`), the final campaign's binary (`receipts/escape-final.*`), and the internal review's own `plant_escape.sh` run unchanged (`receipts/probes/internal-plant-escape-owed-held-probe-owed-at-the-poll.txt`). The test also fails under 23 other plants, each of which has other killers (`receipts/per-test-escape.json`). |

How the plant `owed-held-probe-owed-at-the-poll` works (`src/acmp.c`, `acmp_poll`):

- It acts at an accepting poll with no BIND_RX waiting before the poll, and only if no command was declined since
  the previous accepting poll. Then it owes the lowest held probe at once, through `sm_expired`, so the probe takes
  the freed slot ahead of a command offered after that poll.
- To tell "declined since the last accepting poll" apart, it keeps a function-local snapshot of `busy_declined`.
  - A command the port keeps from before was declined after the previous accepting poll. A command offered for the
    first time was not.
  - From the core's view, that is the only difference between the two, so the plant must key on history. The
    accepted round 5 precedent `owed-bind-wait-only-on-a-second-decline` keys on `busy_declined` too.
- With no command after the poll, owing the probe at the poll instead of at timer service puts it in the same pass
  and in the same slot. That is why no older test sees the change.
- The candidate is in `receipts/plant-trial/candidate-plant.json`.
- It is CAUGHT in the s2 step campaign and in the final campaign (444 caught, 0 escaped, 0 error).

Escape evidence on the final campaign's binaries (`receipts/escape-final.json`, `.txt`; 126 tests each):

- 63 plants were checked: the 54 `owed-*` plants and the nine ACMP plants the owed-bound map uses.
- Every one fails the full binary and passes (rc 0) once its failing tests are excluded.
- With only the round 6 test excluded, exactly the round 6 plant passes.

## Every sentence, re-checked (`map/`)

- The round 6 map (`map/sentence_map.py`) and its checker `map/check_map.py TREE CAMPAIGN ESCAPE OUT` were run on
  the clean clone with the final campaign and escape evidence. Result: "65 sentences and clauses, 50 core, 56
  distinct plants; map: every sentence mapped; every core sentence pinned by a registered, caught plant"
  (`map/check-final.txt`, table `map/map-final.md`).
- The removed sentences were "A held probe therefore waits at most…", "These counts assume…" and "Its TMR_NO_RESP
  runs…". They were replaced by two core sentences:
  - "A held probe is never dropped for want of a slot, and it takes a freed slot only at timer service…" is pinned
    by the new test's two needles (new plant), by "one pass per probe before it" (`owed-hold-rearmed-late`,
    `owed-hold-at-seven`), and by "no probe held for the deferred BIND_RX is lost" (`owed-held-probe-lost`).
  - "Its wait has no upper limit while commands keep taking the freed slots; its own TMR_NO_RESP runs from when it
    leaves" is pinned by the new test's named assertion (new plant), and by "each held probe was sent, and its
    timeout runs from when it left" (`acmp-owed-probe-no-resp-2s`).
- The changed `:92` and `:94` sentences also carry the new named assertion.
- Against the code (`src/acmp.c`):
  - A held probe is owed only from `sm_expired`, at timer service (`probe_yields` `:778-792`, `sm_expired`
    from `:794`).
  - A command needs only `room()` (`:328-335`, `:1086-1103`).
  - So any command the core takes before timer service, kept or offered for the first time, takes the freed slot
    first, and no command ever waits for a held probe.
  - The wait ends only when a timer service finds a slot free with no BIND_RX waiting, or when the probe is
    cancelled. The text no longer claims any more than that.

## Reviewers' round 4 and round 5 probes, unchanged, at 376486b (`receipts/probes/`)

Inputs are listed by sha256 in `receipts/probes/inputs.sha256`. The internal review's runners (`run_probe_j4.sh`,
`run_probe_timer_ahead.sh`, `plant_escape.sh`) export the clean clone's commit. The external review's runner
(`run_probes3.sh`, `escape_check5.py`) takes a `git archive` of it. Every run ends with rc 0. Every PROBE line is
byte-identical to the review's own round 5 receipt: r3 14 lines, timer-ahead 5, r4 + r4b 12, r4c 3, r5 3, r5b 6,
owed6 3 and owed7 7.

Each output falls within the new sentences:

| Probe output | New sentence it meets |
|---|---|
| owed7 (R794-5): held retry owed in pass 3 / 4 / 6 / 13 with 0 / 1 / 3 / 10 later commands, offered for the first time or declined and kept; `probes_lost` 0. Its "stated" column prints the removed round 5 limit | `:110` after every command the core takes first, kept or offered for the first time; no upper limit while commands keep taking the freed slots; `:92`, `:94` |
| r5 (R793-5): sink 3 held through pass 5602 with a GET every pass, leaves in pass 5611 after sink 2's two probes; none lost | `:110` no upper limit while commands keep taking the freed slots; never dropped |
| r5b (R793-5): one gap; sink 2 owes three probes before sink 3's held retry (6409, 6410); none lost | `:110` (the removed list named only the retry; nothing now limits what precedes it) |
| r4c sustained: 11, 250, then sink 3 in 251 | `:110` |
| r4c failure response: `probe_held` 1 → 0, PRB_W_RETRY, ACTIVE, TMR_RETRY | `:95`, `:94` (or cancelled) |
| r4/r4b ports "all" and "one" | Command bound `:107` and budget `:112-113`, unchanged; "one" is excluded by `:85` with its cost at `:89` |
| owed6: 9, 11, 12; 8, 10, 11 | `:107` n = 8 and n = 7 |
| r3, intermittent, timer-ahead | The command bound, the budget, `:96` loss and the gated port `:114-115`, unchanged |

The reviewers' plant scripts were also run unchanged (`receipts/reviewer-scripts/`, `receipts/probes/`):

- R794-5 `escape_check5.py`: unplanted, 126 of 126 pass. Its four plants fail the full binary, and every registered
  needle is SEEN.
- R794-5 `escape_check4.py`: as at round 5, except that the new test now also fails under two of its plants
  (`reviewer-hold-at-seven`, `reviewer-scan-skips-last-sink`). Every registered needle is SEEN, and the unplanted
  head passes.
- R793-5 `run_reviewer_plants.sh`: all eight `rv-` plants fail at least one of 126 tests. As before, its "ESCAPED"
  lines come from the script's `--discover` step, which uses a placeholder killer.
- R793-5 `plant_escape.sh` on the three newest plants: each fails only its own test, and passes without it.

## Boundary evidence (asserted at 376486b, 1 ms passes)

| Case | Result |
|---|---|
| Retry held beside a kept BIND_RX, no later command | BIND_RX taken in pass 2; retry owed in pass 3; none lost |
| The same with 1 / 3 GET_RX_STATE offered for the first time after each accepting poll | Each taken at once; retry owed in pass 4 / 6; every answer before the retry; TMR_NO_RESP from its send |
| The same under `owed-held-probe-owed-at-the-poll` | The retry is owed at the pass-3 poll; the first GET is declined and kept; its answer leaves after the retry (positions 11 vs 10); the test fails |
| Round 3-5 cases (unchanged tests) | Unchanged: 9, 11, 12, …; 8, 10, 11 from seven owed; cancel by response |

## Gate table (Linux hosted and bare-metal RV32)

Toolchain:

- GoogleTest/GMock 1.14.0 from the pinned prefix.
- Host GCC and Clang for the hosted arms.
- Clang 18.1.3 and clang-tidy 18.1.3 first on PATH.
- Mermaid CLI 11.16.0 with Node 22.11.0 in scratch.
- riscv64-elf-gcc and QEMU for RV32.

Each step copied the lane's exact working tree to scratch (`scripts/run_step.sh`). It then ran
`python3 scripts/validate.py --work <w> --jobs 16 --graphs` and `python3 scripts/baremetal.py --work <w> --jobs 8`
concurrently. `git status` and the diff sha256 matched before and after each run, and they matched the lane at
commit time. The final run used a clean `git clone --no-local` of 376486b (`scripts/run_final.sh`).

| Gate | s1 tree (c0477c8) | s2 tree (376486b) | Final, clean clone 376486b |
|---|---|---|---|
| 17 source and metadata gates (entity-golden … privacy) | all 0 | all 0 | all 0 |
| port-contracts self-test controls | 77 | 77 | 77 |
| privacy | 0 | 0 | 0 (37 commits, 388 historical blobs, 98 files) |
| gcc configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| coverage | 0 | 0 | 0 (acmp.c 813/813, 424/424) |
| clang-sanitizers configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| static-analysis | 0 | 0 | 0 |
| mutation | 0 (443 caught) | 0 (444 caught) | 0 (444 caught, 0 escaped, 0 error) |
| mutation-controls, graphs | 0, 0 | 0, 0 | 0, 0 |
| `baremetal.py` Debug, Release | 0, 0 | 0, 0 | 0, 0 |

No gate run failed in this round. Before step 2's gate run, the test inventory generator refused `EXPECT_LT`, which
is not an allowed assertion form. The assertion became `EXPECT_TRUE(position(s) < position(retry))`, and every gate
run then passed.

Receipts:

- `receipts/final/` holds the final run on the clean clone:
  - all 28 gate logs and rc files, `gates.json` and `validate.log`;
  - `baremetal.log` and `rv32-results.json`;
  - the head, and the clone's status and diff hash before and after;
  - `campaign-summary.json`, with name, status and failing tests for all 444 plants. The full `results.json`
    (977653 bytes) is recorded by sha256 in `receipts/not-copied.sha256.txt`.
- `receipts/steps/`: for s1 and s2, the validate summary and rc, `gates.json`, the mutation log, the bare-metal
  log and rc, and the tree's head, status and diff hash before and after.
- `receipts/escape-final.*`, `per-test-escape.json`, `sizes-and-images.txt`, `plant-trial/`, `probes/` and
  `reviewer-scripts/`.
- `scripts/`:
  - the step and final runners;
  - `run_probes6.sh` and `run_reviewer_plants6.sh`;
  - `escape6.py` and `per_test_escape6.py`;
  - `imgx.sh` and `imgsize.sh`;
  - `pr_body6.py` with `round6-section.md`, and `publish6.py`.
- Host paths in receipts are replaced by `<scratch>`, `<clone>`, `<reviews>`, `<tools>` and `<lane>`.

## Bare-metal image size, memory and cost

715d208 and 376486b were exported to paths of equal length (`xa`, `xb`) and built with `scripts/baremetal.py`
(`receipts/sizes-and-images.txt`):

| Build | 715d208 (before) | 376486b (after) |
|---|---|---|
| Release ELF bytes / sha256 | 50504 / `f1fd4b90…a7c2` | 50504 / `f1fd4b90…a7c2` (identical; also identical in the clean-clone gate build) |
| Release `.text` / `.rodata` / `.bss` | 38668 / 1961 / 8 | 38668 / 1961 / 8 |
| Release `acmp.c` object text | 19365 | 19365 |
| Debug ELF bytes | 150332 | 150332 (the sha differs only by the recorded build path; the clean clone gives 150400) |
| Debug `.text` / `acmp.c` object text | 49812 / 21321 | 49812 / 21321 |

No core source changed, so memory and instruction counts are as before. `sizeof(struct acmp)` is 5072 bytes on
RV32, `sizeof(struct acmp_sink)` is 256 bytes and the owed set is 640 bytes. The round 3 cost table stands.

## Acceptance items (issue #26)

| Item | Status | Evidence |
|---|---|---|
| Past the bound the entity still answers every command; bound and behaviour stated in the docs | Met in the core for a port that follows the contract | PORTING states the command bound, the budget, and now only what holds by construction for a held probe |
| A test fills the owed set with the egress held, sends a further command, answered within its timeout after the egress returns | Met | Round 2-5 tests |
| A planted mutant restoring the silent drop is caught | Met | 444 of 444 caught |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | The parent must adopt this head. Round 6 changes no source, so no parent fragment moves. |

Hence "Relates to #26".

## Environment notes

- Scratch: `$VALIDATION_STORAGE/tsn26-a750g/` holds:
  - the clean clone (`clone`) and the final gate work (`val-final`, `rv32-final`);
  - the step trees and work (`tree-s1`, `tree-s2`, `val-s1`, `val-s2`, `rv32-s1`, `rv32-s2`);
  - the probe and reviewer-script work (`probes`, `probes-out`, `rev`, `rev-out`);
  - the dev and plant-trial copies (`dev`, `dev-build`, `plant1`, `plant1-build`);
  - the image exports (`xa`, `xb`, `xa-rv32`, `xb-rv32`);
  - Node, the Mermaid CLI and Puppeteer's cache, copied from round 5's scratch.
- Memory: the unit's peak (memory.peak) was 10.74 GB. That is under the 12 GB cap but **over the 9 GB target**. It
  happened while the final gates, the probe builds and the two image builds ran at the same time, and most of it
  was page cache. memory.current was 7.5-7.6 GB at the two checks made during that run, and 6.0 GB at the end.
  Next time, run the probes and image builds after the final gates, not alongside them.
- The lane's ignored `build-registration/` predates this session and was not used. Inventory and traceability
  were regenerated with `--build` in scratch, and `scripts/__pycache__` was removed before each commit.
