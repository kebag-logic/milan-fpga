# [A750e] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 4

Status: REVIEW READY at a0a32110511e444a23848367b7cbb4231e16ce5a. Every gate returns 0 on both targets, on a clean
clone of that head.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Start head: b7a59887f5f2ff729206b87a268972c637882dc0 (round 3, pushed).
- Round 4 adds three commits. There was no rebase, force or amend. Each is authored and committed by hackerman-kl
  <hackerman-kl@kebag-logic.com> and has a one-line subject with no body or trailers.
  1. `b7b2048` Derive the answer pass of every kept ACMP command and the egress-hold budget for the deepest backlog,
     and assert both pass by pass (step 1: R793-3 F3)
  2. `c4a2bff` Pin each stated behaviour of the ACMP owed bound and its hold with a named assertion and a registered
     plant, including the hold's scope, a refused poll and the gated port (step 2: R793-3 F4, R794-3 F3)
  3. `a0a3211` Say that probes_held counts each held probe once per pass, that a held probe waits at most its bound
     and is cancelled only when its sink stops probing, and that the 1 ms re-arm means the next pass only for passes
     at least 1 ms apart (step 3: residue and suggestions)
- No core change: `git diff --stat b7a5988 a0a3211 -- src include examples` is empty. Files changed: PORTING,
  REQUIREMENTS, requirements.json, VERIFICATION, CHANGELOG, generated TESTS and TRACEABILITY,
  `scripts/check_port_contracts.py`, `tests/test_acmp.cpp`, `tests/mutations.json`.
- Not pushed; no PR opened or edited. PR text: `PR-BODY.md` (first line "[A750e]", "Relates to #26").
- Issue #26: "[A750e] TAKEN" posted at the start; "[A750e] REVIEW READY a0a32110511e444a23848367b7cbb4231e16ce5a"
  posted at the end.

## Findings addressed

| Finding | Disposition |
|---|---|
| R793-3 F3 (backlog timing) | (a) PORTING "ACMP owed bound" derives the bound for every kept command (`docs/PORTING.md:102-111`). (b) PR body Round 3 "Result" sentence replaced with the reviewer's wording. (c) The drain test's kept-behind case asserts the kept answers' passes 11 and 12 by sequence ID (`tests/test_acmp.cpp:3017-3026`); 16 new CRITICAL phrases. Two new tests assert the whole bound and the budget. |
| R793-3 F4 (five unpinned hold behaviours) | (1) refused poll: `RefusedPollLeavesTheBindWaitingAndItsHold`; (2) BIND_RX declined at 8 owed: `BindDeclinedBehindTheFullSetHoldsNoProbe`; (3) PRB_W_RESP2 timeout, TMR_RETRY, TMR_NO_TK at their deadline: `OnlyTimerProbesAreHeldBesideTheWaitingBind`; (4) new binding clears `probe_held`: `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces`. All eight of the reviewer's plants are registered (equivalents under `owed-` names) and each now fails at least one test in the reviewer's own script. |
| R794-3 F3 (scope boundary unpinned) | Its three plants are registered as `owed-hold-widened-to-every-timer`, `owed-hold-widened-to-second-no-resp`, `owed-bind-wait-set-at-full`; its two controls as `owed-hold-at-seven` and `owed-hold-scan-skips-the-last-sink`. The reviewer's `escape_check.py` and `plant_full.sh` show each failing at this head. ACMP-12 now says "and no other expiry" and "waits for the next accepted owed frame". |
| R793-3 RES5 / R794-3 R2 | `docs/PORTING.md:91` and the counter row `:348`; the test message and its needle now read "each held probe counts once for each pass it is held"; PR body What and Round 3 wording. |
| R793-3 RES6 | `docs/PORTING.md:108` "waits at most from"; PR body Round 3. |
| R793-3 S5 / R794-3 R3 | `docs/PORTING.md:88` "retried at the first timer service 1 ms or more later, which is the next pass for a port whose passes are at least 1 ms apart"; `:108` "These counts assume passes at least 1 ms apart."; CHANGELOG "re-armed 1 ms on". |
| R794-3 R4 | `docs/PORTING.md:93` and the counter row: never dropped for want of a slot, cancelled only when its sink stops probing. Pinned by the departure, other-talker and same-talker tests. |
| R793-3 S6 / R794-3 S6 (taken) | `docs/PORTING.md:92`: while the port keeps commands or no owed frame is accepted, a held probe keeps waiting, re-armed every 1 ms, its probing not advancing. Pinned by the refused-poll test (state PRB_W_RESP and the 1 ms re-arm during the refused pass). |
| R794-3 S7 (taken as a scope condition) | `docs/PORTING.md:108` and `:112`: "at most one per (other) sink while no sink's discovery restarts". The restart case itself is not tested (a condition, not a claim). |
| R794-3 optional RV32 TMR_RETRY step | Not taken. The RV32 smoke is unchanged; the three external-review plants exit 0 there and fail the hosted ACMP target. |

## The derivation (`docs/PORTING.md:102-112`)

- Passes are counted from the one in which the egress returns, for a port that polls once per pass and keeps the
  redelivery rule (deliver kept frames after each accepting poll, before timer service; after a refused poll it may
  wait or deliver again, and the frame is declined again).
- Each accepted `acmp_poll` sends the oldest owed frame. The set never empties while a command is kept, since a
  command is declined only with 7 or 8 owed. So owed frames leave one per pass, and each refused poll delays every
  later frame one pass.
- Each freed slot goes to the oldest kept command; no timer probe is owed ahead of a kept command.
- So a command in the kept backlog leaves in pass `ACMP_OWED_MAX` + 1 + f + r: f counts frames owed by the kept
  commands ahead (2 for a BIND_RX that starts a binding, 1 for any other command including an answered-only BIND_RX,
  0 for a frame that needs no answer), r the refused polls.
- Held probes follow the last kept command's frames, one per pass in timer-service order. The held probe's own wait
  is as round 3 stated it, as an upper bound.
- Budget: hold + (`ACMP_OWED_MAX` + 1 + f + r) * p ms within 200 ms (Milan v1.2 Table 5.26) for the last kept
  command; f <= 2 * (Q - 1), so with 1 ms passes and no refused poll a hold of at most 193 - 2 * Q ms: 191 for one,
  189 for two, 187 for three.
- Every probe output from both reviews agrees with it (see "Reviewer scripts" below).

## Changes (file:line at a0a3211)

- `docs/PORTING.md`:
  - `:80` the only-message-type rule names the same-talker rebind.
  - `:82-83` `bind_waiting` set and cleared; a refused poll leaves it set; a BIND_RX declined with no slot free does
    not set it.
  - `:84-85` the redelivery rule and the refused poll.
  - `:88` the 1 ms re-arm (R3); `:89` no other expiry is held.
  - `:90-94` never lost; `probes_held` per probe per pass; S6 sentence; cancelled only when its sink stops probing;
    lost when nothing is held or waiting, including a BIND_RX declined at the full set.
  - `:102-111` the derivation and the budget; `:112` gated port with the S7 condition.
  - `:348` `probes_held` counter row.
- `docs/REQUIREMENTS.md:44-45` (prose: no other expiry is held; a command kept behind others) and `:53` (ACMP-12 row);
  `docs/requirements.json:222` (same row text).
- `docs/VERIFICATION.md:24`: 437 core plants. `CHANGELOG.md:6`: re-armed 1 ms on; the derivation.
- `scripts/check_port_contracts.py:284-307`: 16 new CRITICAL phrases (acmp_rx 2, bind_waiting 4 with one replaced,
  probes_held 5, ACMP_OWED_MAX 6). Self-test: 61 meaning-removal controls (45 at b7a5988).
- `tests/test_acmp.cpp`:
  - `:2679-2688` fixture: the drain helper counts passes with `bind_waiting` set and more than one free slot (0).
  - `:2691-2719` fixture: `Kept`, `kept_bind`, `kept_get`, `kept_answers`, `keep_and_release`.
  - `:3017-3026` drain test kept-behind case: answers' passes by sequence ID; `:3043` message "each held probe counts
    once for each pass it is held".
  - New tests: `:3099` OwedSetIsEightFramesOfEightyBytes, `:3105` AnsweredOnlyBindAlsoWaitsForTwoSlots, `:3125`
    BindDeclinedBehindTheFullSetHoldsNoProbe, `:3147` OnlyTimerProbesAreHeldBesideTheWaitingBind, `:3180`
    RefusedPollLeavesTheBindWaitingAndItsHold, `:3230` BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces, `:3256`
    SameTalkerRebindKeepsTheHeldProbe, `:3282` GatedPortBudgetsOnePassPerProbeOwedAhead, `:3318`
    KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem, `:3369` KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout.
  - ACMP binary: 123 tests (122 ACMP + main's Wire test), up from 113.
- `tests/mutations.json:2596-2876`: 15 new plants. Extra registered kills on existing plants: `owed-timer-probe-not-held`
  (5), `owed-bind-wait-unset` (4), `owed-bind-wait-kept`, `owed-bind-one-slot`, `owed-hold-rearmed-late`,
  `owed-ready-one-slot` (2), `owed-ready-ignores-full`, `acmp-probe-before-response`, `acmp-rebind-same-reprobes`,
  `acmp-owed-probe-no-resp-2s`; `owed-hold-uncounted` needle renamed with its message. 441 plants: 437 core, 4
  generated.
- Generated: `docs/TESTS.md` (172 declarations, 441 plants), `docs/TRACEABILITY.md` (46 requirements). The coverage
  ratchet is unchanged (`src/acmp.c` 813/813 lines, 424/424 branches; no source change).

## Tests and the planted mutants they kill

"Plants it kills" are the registered kills (test and streamed message), all CAUGHT in the final campaign. A plant in
bold escapes once only that test is excluded (`receipts/per-test-escape.json`).

| Test | Proves | Plants it kills | Escape without it |
|---|---|---|---|
| KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem | Nine kept frames (BIND_RX, GET_RX_STATE, unknown-sink BIND_RX, same-talker rebind, UNBIND_RX, foreign frame, GET_TX_STATE, second binding, GET_RX_STATE) with four retries held: answers in passes 9, 11, 12, 13, 14, 15, 16, 18 = 9 + f; held probes at 19-22 = 9 + F + j, sink order; nothing lost | acmp-rebind-same-reprobes, owed-bind-wait-unset, owed-timer-probe-not-held | Each also fails other tests (sole killer of none) |
| KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout | Five backlogs at hold 200 - (9 + f): last answer exactly 200 ms, the others within | owed-bind-wait-unset, owed-timer-probe-not-held | Sole killer of none |
| RefusedPollLeavesTheBindWaitingAndItsHold | Both redelivery styles: refused poll frees nothing, `bind_waiting` stays; redelivered BIND_RX declined; retry held, PRB_W_RESP, deadline now + 1; BIND_RX in pass 10 at position 8; retry after its probe | owed-bind-one-slot, **owed-bind-wait-cleared-by-refused-poll**, owed-hold-rearmed-late, owed-refused-poll-drops-the-frame, owed-timer-probe-not-held | `owed-bind-wait-cleared-by-refused-poll` passes 122/122 without it |
| OnlyTimerProbesAreHeldBesideTheWaitingBind | With `bind_waiting` set and the egress refused: RESP2 timeout -> PRB_W_RETRY (status 7, deadline +4000), TMR_RETRY -> PRB_W_AVAIL, TMR_NO_TK -> PRB_W_AVAIL, each at its deadline; `probes_held` 0 | **owed-hold-widened-to-every-timer**, **owed-hold-widened-to-second-no-resp** | both pass without it |
| BindDeclinedBehindTheFullSetHoldsNoProbe | BIND_RX at 8 owed sets no wait; a retry during the hold is lost and counted, RESP2, TMR_NO_RESP from now | **owed-bind-wait-set-at-full**, owed-hold-whenever-full | `owed-bind-wait-set-at-full` passes without it |
| BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces | Held retry on sink 2; BIND_RX to another talker for sink 2 taken in pass 4 clears `probe_held`; sink 3's retry then lost | owed-hold-whenever-full, **owed-rebind-keeps-the-hold** | `owed-rebind-keeps-the-hold` passes without it |
| SameTalkerRebindKeepsTheHeldProbe | Same-talker rebind keeps the held retry, owed in pass 4 (PRB_W_RESP2, NO_RESP held), none lost | owed-same-talker-rebind-cancels-the-hold | Also killed by an existing rebind test |
| GatedPortBudgetsOnePassPerProbeOwedAhead | Port tests `acmp_rx_ready`: nothing declined or held; four retries owed meanwhile; BIND_RX in pass 13 = 9 + 4 <= 9 + n_sinks | owed-ready-ignores-full, owed-ready-one-slot | Also killed by ReadyPredicate |
| AnsweredOnlyBindAlsoWaitsForTwoSlots | Unknown-sink BIND_RX and same-talker rebind declined at 7 owed, unchanged, `bind_waiting` set | **owed-answered-bind-takes-one-slot** | passes without it |
| OwedSetIsEightFramesOfEightyBytes | 8 x 80 = 640 bytes | **owed-entry-widened** (header plant: `release` widened to 64 bits) | passes without it |
| ProbesFallingDueInTheDrainWaitForTheDeferredBind (extended) | Adds the `bind_waiting` invariant and the kept answers' passes | owed-bind-wait-kept (invariant), plus round 3 kills | **owed-hold-skips-delay** is still its sole kill |

Escape evidence (`receipts/escape-final.json`, `.txt`), on the final campaign's binaries, 123 tests each:

- 60 plants: 51 `owed-*` and the nine ACMP plants the owed-bound map uses (`acmp-full-queue-acts`,
  `acmp-stop-keeps-the-hold`, `acmp-probe-before-response`, `acmp-rebind-same-reprobes`, `acmp-owed-probe-no-resp-2s`,
  `acmp-lost-probe-uncounted`, `acmp-poll-newest-first`, `acmp-poll-drains-everything`,
  `acmp-response-passes-an-owed-frame`).
- Every one fails the full binary and passes (rc 0) once its failing tests are excluded.
- With only the ten round 4 tests excluded, seven pass: `owed-bind-wait-cleared-by-refused-poll`,
  `owed-bind-wait-set-at-full`, `owed-hold-widened-to-second-no-resp`, `owed-hold-widened-to-every-timer`,
  `owed-rebind-keeps-the-hold`, `owed-answered-bind-takes-one-slot`, `owed-entry-widened`. The round 3 suite misses
  each of them. The other eight new plants (`owed-probe-held-never-set`, `owed-hold-scan-skips-the-last-sink`,
  `owed-hold-whenever-full`, `owed-hold-at-seven`, `owed-deferred-answer-error-status`,
  `owed-same-talker-rebind-cancels-the-hold`, `owed-refused-poll-drops-the-frame`, `owed-ninth-frame-taken`) register
  plants for assertions that round 3 or earlier already made but no plant named.

## Every stated behaviour: the sentence map (`map/`)

- `map/sentence_map.py` lists every sentence of PORTING "ACMP owed bound" (48), of the ACMP-12 prose (8) and the
  clauses of the ACMP-12 row (8). For each, it gives the kind and the pins (test, streamed message, plants).
- `map/check_map.py TREE CAMPAIGN_RESULTS ESCAPE_JSON OUT` checks the following and exits 1 on any gap:
  - Every sentence matches exactly one entry.
  - Every pin's message is in its test.
  - Every listed plant is registered with exactly that kill, is CAUGHT in the campaign and escapes without its
    killers.
  - Every core sentence has a pinned plant.
- Result on the clean clone with the final campaign (`map/check-final.txt`): 64 sentences and clauses, 50 core, 53
  distinct plants. "map: every sentence mapped; every core sentence pinned by a registered, caught plant". The table
  is `map/map-final.md`.
- The other kinds:
  - Port obligations (5): the redelivery rule, "deliver no later frame", "a port that cannot keep a frame tests
    `acmp_rx_ready`", the gated-port budget and receive-queue ownership. Where they have an effect on the core it is
    asserted: the first, third and fourth carry pins with plants.
  - Assumptions (2): the once-per-pass model and the 1 ms pass length. Rationale (1): "timer service first could
    ...". References (5).
  - Target (1): "Both Linux and bare-metal RV32 are required", met by the gates.

## Reviewer scripts, unchanged, at a0a3211 (`receipts/reviewer-scripts/`)

Run by `scripts/run_reviewer_scripts.sh` on the clean clone.

- R793-3:
  - `run_reviewer_plants.sh`: all eight `rv-` plants fail at least one of 123 tests. `rv-bind-wait-set-when-full`,
    `rv-hold-widened-to-the-timeout`, `rv-hold-widened-to-every-timer`, `rv-bind-wait-cleared-by-every-poll` and
    `rv-bind-unsets-no-hold` each fail one test; the three controls fail 4-7. At b7a5988 the first five passed
    113/113. The script's "ESCAPED" lines come from its `--discover` step with a placeholder killer; its own pass
    criterion is the full-suite list (`r793-reviewer-plants.txt`, `.json`).
  - `probe_r3.cpp`: 11 probes pass. The mixed backlog leaves at 9, 11, 12, 14, 15 (= 9 + f). The margin BIND_RX then
    GET_RX_STATE case gives 200 and 202 ms (the budget for two is 189 ms). The gated port's 14 retries give pass 23
    (budget 25). The unknown-sink held probe leaves at position 9, inside the "at most" bound. Sustained commands
    hold 2 probes for 40 passes, none lost.
  - `probe_intermittent.cpp` (refused poll): BIND_RX pass 10, position 8, the other probe at position 10,
    `probes_held` 2, none lost.
  - `probe_timer_ahead.cpp`: pass 9 for no, one and two timers.
- R794-3:
  - `escape_check.py` with `plants-r3.json`: unplanted 120/120. All 14 plants fail the full binary.
    `reviewer-bind-wait-at-full`, `reviewer-hold-every-timer`, `reviewer-hold-second-no-resp` and
    `reviewer-hold-at-seven` fail even with the round 3 tests excluded.
  - `plant_full.sh`: each of its three plants makes ctest rc 8 (the ACMP target fails, 7 of 8 pass). `baremetal.py`
    exits 0 and the smoke ELFs exit 0: the RV32 smoke does not cover these boundaries.
  - `probe_owed3.inc` (boundary): passes at head. Under each plant, the probe for its boundary fails.
  - `probe_owed2.inc` is unchanged from round 3's receipt. `probe_owed4.inc` gives the gated port passes 9, 10, 13
    and 23 against a budget of 25. `probe_owed5.inc` gives 200/202/203 and 200/201/202 ms at 191 ms; the budget for
    three kept commands is 187 ms.

## Boundary evidence (60 ms holds unless stated, 1 ms passes)

| Case | Asserted at a0a3211 |
|---|---|
| BIND_RX alone, retries due | pass 9, position 8 (round 3 tests) |
| BIND_RX + two GET_RX_STATE kept | GETs at passes 11 and 12 |
| Nine mixed kept frames | 9, 11, 12, 13, 14, 15, 16, 18; held probes 19-22 |
| Refused poll in pass 2 | BIND_RX pass 10, position 8; retry held, deadline now + 1 |
| Budget, Q = 1, 2 (BIND+GET), 2 (GET+GET), 3 BINDs, 4 mixed | holds 191, 189, 190, 187, 186 ms: last answer at exactly 200 ms |
| Gated port, four retries | pass 13 = 9 + 4 |
| BIND_RX at 8 owed, retry during hold | lost (`probes_lost` 1), not held |
| bind_waiting with more than one free slot | 0 passes in every drain case |

## Gate table (Linux hosted and bare-metal RV32)

Toolchain:

- GoogleTest/GMock 1.14.0 from the pinned prefix.
- Host GCC 16 and host Clang for the hosted arms.
- Clang 18.1.3 and clang-tidy 18.1.3 first on PATH.
- Mermaid CLI 11.16.0 with Node 22.11.0 in scratch.
- riscv64-elf-gcc and QEMU for RV32.

Each step ran `python3 scripts/validate.py --work <w> --jobs 16 --graphs` and `python3 scripts/baremetal.py --work <w>
--jobs 8` concurrently on the exact tree that was then committed. `git status` and the diff hash were the same before
and after each run.

| Gate | b7b2048 tree (s1) | c4a2bff tree (s2) | a0a3211 tree (s3) | Final, clean clone a0a3211 |
|---|---|---|---|---|
| 17 source and metadata gates (entity-golden ... privacy) | all 0 | all 0 | all 0 | all 0 |
| port-contracts self-test controls | 55 | 57 | 61 | 61 |
| privacy | 0 | 0 | 0 | 0 (31 commits, 359 historical blobs, 98 files) |
| gcc configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 (8/8 ctest) |
| coverage | 0 | 0 | 0 | 0 (acmp.c 813/813, 424/424) |
| clang-sanitizers configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| static-analysis | 0 | 0 | 0 | 0 |
| mutation | 0 (426 caught) | 0 (441) | 0 (441) | 0 (441 caught, 0 escaped, 0 error) |
| mutation-controls, graphs | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| `baremetal.py` Debug, Release | 0, 0 | 0, 0 | 0, 0 | 0, 0 |

Runs that failed or were stopped, none of them committed:

- s1, first run: `comments` rc 1. A prose comment on a fixture helper broke the comment rule, which allows only
  requirement and clause tags. I removed the comment and regenerated the inventory. The rerun passed every gate.
- s2 was stopped twice before it finished.
  - First: VERIFICATION still said 434 core plants.
  - Second: the sentence map showed that the kept-behind pass assertion looked up a fixed position, which the
    gap-free queue makes always true. I changed it to look the answer up by sequence ID. I also added the
    same-talker, gated-port and ninth-frame pins, and dropped one kill that could not fire, because an earlier case's
    ASSERT ends the test first.
  - The third run passed every gate.

Receipts:

- `receipts/final-*`: gates.json, validate log, mutation log, coverage, privacy, port contracts, baremetal log,
  rv32 results, head and clone status.
- `receipts/final-campaign-summary.json`: name, status and failing tests for all 441 plants. The full results.json is
  968 KB, so only its sha256 is recorded, in `final-campaign-results.sha256.txt`.
- `receipts/steps/`: s1-s3 gates, logs, rv32 results and heads.
- `receipts/escape-*`, `per-test-escape.json`, `sizes-and-images.txt` and `reviewer-scripts/`.
- Host paths in receipts are replaced by `<scratch>`, `<clone>`, `<reviews>`, `<tools>` and `<lane>`.

## Bare-metal image size, memory and cost

b7a5988 and a0a3211 were exported to paths of equal length (`xa`, `xb`) and built with `scripts/baremetal.py`
(`receipts/sizes-and-images.txt`):

| Build | b7a5988 | a0a3211 |
|---|---|---|
| Release ELF bytes / sha256 | 50504 / `f1fd4b90…a7c2` | 50504 / `f1fd4b90…a7c2` (identical; also from the clean-clone gate build) |
| Release `.text` / `.rodata` / `.bss` | 38668 / 1961 / 8 | 38668 / 1961 / 8 |
| Release `acmp.c` object text | 19365 | 19365 |
| Debug ELF bytes | 150332 | 150332 (sha differs only by the recorded build path; clean clone 150400) |
| Debug `.text` / `acmp.c` object text | 49812 / 21321 | 49812 / 21321 |

Memory and instruction counts are unchanged, because no core source changed:

- `sizeof(struct acmp)` is 5072 bytes on RV32 and 5080 bytes on x86-64.
- `sizeof(struct acmp_sink)` is 256 bytes.
- The owed set is 640 bytes.
- The round 3 cost table stands.

## Acceptance items (issue #26)

| Item | Status | Evidence |
|---|---|---|
| Past the bound the entity still answers every command; bound and behaviour stated in the docs | Met in the core for a port that follows the contract | PORTING now gives the answer pass of every kept command and the hold budget; ACMP-12 states the hold's scope |
| A test fills the owed set with the egress held, sends a further command, answered within its timeout after the egress returns | Met for all seven command types, for backlogs, at the budget | Round 2-3 tests plus KeptCommands and KeptBacklog |
| A planted mutant restoring the silent drop is caught | Met | Unchanged; 441/441 caught |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | Needs the parent to adopt this head (fragments as in the round 3 integration note; round 4 changes no source, so no fragment moves). The gated-port budget applies. |

Hence "Relates to #26".

## Environment notes

- Scratch: `$VALIDATION_STORAGE/tsn26-a750e/` holds:
  - the clean clone (`clone`), the final gate work (`val-final`, `rv32-final`) and the reviewer-script work
    (`rev-work`);
  - the step trees, the final-tree campaign (`mut3`) and the exports `xa`, `xb`;
  - Node, the Mermaid CLI and Puppeteer's cache, copied from round 3's scratch.
- `scripts/make_step.py` regenerated the step 2 and step 3 trees from the final files, so each gated tree is exact.
- Memory: the unit's MemoryCurrent reached 8.2 GB, most of it page cache, while the reviewer scripts ran after the
  final gates. Deleting finished build trees brought it to 4.3 GB. The 12 GB cap was never approached.
- The lane's ignored `build-registration/` predates this session. One inventory check early in the session used it as
  the default build directory; every later run used scratch. Gate runs' `scripts/__pycache__` was removed before
  each commit and from the clean clone.
