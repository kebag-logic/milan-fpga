[R793] NEGATIVE - exact head b7a59887f5f2ff729206b87a268972c637882dc0

# R793-3: independent internal review of kebag-logic/tsn-c-stack PR #28 (issue #26), delta round

- Exact head: `b7a59887f5f2ff729206b87a268972c637882dc0`, tree `2b5baf1864dd923531f98b9af9255b7e75ad2435` (verified in the clone: `receipts/clone-state.txt`).
- Previously reviewed head: `968a164` (R793-2, NEGATIVE on F2). Source base: `70936b77`.
- Delta since 968a164: three author commits, `8a1cb08` (the hold), `d355236` (S3, a test with commands kept behind the BIND_RX, ARCHITECTURE wording) and `b7a5988` (wording). No merge, rebase or amend.
- Verdict: **NEGATIVE**, on two open MINOR findings.
  - The round-2 finding F2 is **resolved at its cause**. My round-2 probe runs unchanged at this head: a kept BIND_RX with one or two sink timers falling due is now answered in pass 9 with `probes_lost` 0. At 968a164 it was pass 10 and 11.
  - The hold itself is correct in every case I could construct: 16 sinks, two interfaces, mixed commands kept behind, an unknown-sink BIND_RX, the 191 ms margin and a refused poll. All 28 gates pass at the exact head, 426/426 plants are caught, and the cost table and measurement ELFs are byte-identical to the author's receipts.
  - **F3 (MINOR, Docs, Robustness).** The documented budget of `ACMP_OWED_MAX` + 1 passes holds only for the first kept command. A command kept behind the BIND_RX leaves later by one pass per frame owed ahead of it. So at the 191 ms hold that the new test calls "the documented margin", a GET_RX_STATE kept behind the BIND_RX is answered at 202 ms. This was latent before this round. My own round-2 wording carried the same error, and this round's check (1) repeats it.
  - **F4 (MINOR, Tests).** Five reviewer plants, each contradicting a stated sentence of the hold, pass the full 113-test suite. One of them brings back the F2 overtaking for a port that follows the contract literally and meets one refused poll.

## Reconstruction order followed

1. CONTRIBUTING.md (there is no AGENTS.md), then the docs: ARCHITECTURE, PORTING, REQUIREMENTS and requirements.json, TESTS, TRACEABILITY, VERIFICATION, CHANGELOG.
2. Issue #26: body and acceptance are unchanged. Its comments are only the author's TAKEN / REVIEW READY / STOP markers. No maintainer or manager comment narrows the scope. I did not find the manager's ruling (R794-2 option 2) as a public comment. I took it from the review brief and checked the head against it.
3. PR #28 body at this head (all sections, Round 3 in full) and the public review-start comment for R793-3.
4. Authorities, as in earlier rounds: ACMP-12 (updated text), ACMP-03/05/08/09; IEEE 1722.1-2021 8.2.4, 8.2.5, Tables 8-1 and 8-3; Milan v1.2 5.5.3.5 (5.5.3.5.3, .10, .16, .23), Tables 5.26, 5.32 and 5.47.
5. `git diff 70936b77..b7a5988` and history. I read in full `git diff 968a164..b7a5988` (15 files, +513/−38).
6. Public evidence: milan-fpga `28625428` (= `tsn26-review-evidence` tip), `review-evidence/tsn26-r1/author-r3`, read by section: receipts, measure, scripts.
7. I finished my own pass, probes, verdict and ledger before reading any other reviewer's report. I then read the R794-2 findings to resolve them (see the end).

## Answers to the focus items

1. **The kept BIND_RX is answered in pass `ACMP_OWED_MAX` + 1 with `probes_lost` 0. Commands kept behind it are not answered by that pass (F3).**
   - Code:
     - A BIND_RX declined with one slot free sets `bind_waiting` (`src/acmp.c:1099-1103`).
     - Only an accepting `acmp_poll` clears it (`:1268`).
     - While it is set, `probe_yields` (`:778-792`) is true. So a TMR_DELAY expiry or TMR_NO_RESP retry in PRB_W_RESP, the only two expiries that send a PROBE_TX (`:806-812`), is re-armed 1 ms on instead of owed (`:798-804`).
     - With the contract's order (poll, redeliver, timers), timer service sees either a full set or `bind_waiting` set while any command is kept. So no probe is owed ahead of a kept command.
   - Reviewer probes (`scripts/probe_r3.cpp`, `receipts/probes/probe-r3-head.txt`), 60 ms hold, 1 ms passes:

     | Case | BIND_RX answer | `probes_lost` | timer probes sent | `probe_held` left |
     |---|---|---|---|---|
     | 16 sinks, 14 retries one per pass | pass 9 (69 ms) | 0 | 14/14 | 0 |
     | 16 sinks, 14 retries all in pass 1 | pass 9 | 0 | 14/14 | 0 |
     | 16 sinks on two interfaces | pass 9 | 0 | 14/14 | 0 |
     | BIND_RX, GET_RX_STATE, BIND_RX, UNBIND_RX, GET_TX_STATE kept; 6 retries | 9, then 11, 12, 14, 15 | 0 | 6/6 | 0 |
     | Unknown-sink BIND_RX, one retry | pass 9 | 0 | 1/1 | 0 |
     | 191 ms hold, 7 retries one per pass | 200 ms | 0 | 7/7 | 0 |
     | 191 ms hold, BIND_RX then GET_RX_STATE kept | BIND_RX 200 ms, **GET 202 ms** | 0 | 2/2 | 0 |

   - My round-2 probe, unchanged (`scripts/probe_timer_ahead.cpp`, `receipts/probes/probe-timer-ahead-head.txt`): BIND_RX with no, one and two timers is answered in pass 9, 9 and 9, `probes_lost` 0. At 968a164 it was 9, 10 and 11 (`probe-timer-ahead-round2-receipt.txt`).
   - My round-2 packet holds only `probe_timer_ahead`. The brief's other two names exist nowhere in my packets or in the repository history; they turned out to be the other reviewer's round-2 probes (see the end). So I wrote them fresh this round as the fixture `TimerProbesAgainstTheDeferredBind` with the case `DocumentedBudgetAtTheMargin`. The 191 ms margin leaves the BIND_RX at exactly 200 ms, as the committed `DeferredBindAtTheDocumentedMarginMeetsItsTimeout` (`tests/test_acmp.cpp:3010`) asserts.
   - **No probe delays any kept command.** But each command kept behind another leaves one pass later for each frame owed ahead of it. Behind a BIND_RX that is two passes (its answer and its probe). The 191 ms case above shows the result. This predates the round: two GET_RX_STATE kept at a 191 ms hold leave at 200 and 201 ms both at this head and at 968a164 (`receipts/probes/backlog-at-968a164.txt`). See F3.
2. **The held probe's bound: correct as an upper bound, and checked pass by pass.**
   - PORTING:88 says a held probe waits from the pass it falls due through the pass that takes the BIND_RX, plus one pass per frame owed by commands kept behind it and per other probe owed before it.
   - `ProbesFallingDueInTheDrainWaitForTheDeferredBind` (`tests/test_acmp.cpp:2952`) asserts this for every probe, pass by pass: `owed_in == taken_in + 1 + behind + j`. It runs five cases: one retry, one TMR_DELAY expiry, four retries one per pass, four in pass 1, and two GET_RX_STATE kept behind. It also asserts `probes_held` equals the sum of held passes.
   - My mixed and 16-sink cases agree: every held probe leaves after the kept commands' frames, in sink order.
   - For a BIND_RX that owes only its answer (an unknown sink), the held probe is owed in the take pass itself. It is sent right after the answer, at position 9. That is one pass earlier than the sentence states, so the sentence is a bound rather than an exact count (RES6).
3. **The hold ends once nothing is held: verified.**
   - `HoldEndsWithTheLastHeldProbe` (`:3027`) shows two things. A held probe whose talker departs is dropped with its probing (`sm_stop` clears `probe_held`, `:355`). With nothing held and no BIND_RX waiting, a retry that finds the set full is lost and counted.
   - In every probe case above, `probe_held` is false on all sinks at the end, and `bind_waiting` is 0.
   - Flag hygiene, by code reading: `probe_held` is cleared on every exit from probing, through `sm_stop` in `sm_expired`, `bind` (new talker), `unbind`, `probe_response`, `tk_departed` and `acmp_tk_registered`, or through `memset` at reset. A same-talker rebind keeps the timer, so keeping the flag there is correct.
   - None of the bind-time clearing is tested (F4 item 4).
4. **Nine new plants: each escapes without the three new tests, and RV32 catches seven.**
   - `scripts/escape_without_round3.sh` on this review's mutation binaries (`receipts/escape-without-round3.txt`): all nine fail the full 113-test binary and pass the 110 tests left once the three round-3 tests are excluded.
   - On RV32 (`scripts/rv32_plant_smoke.sh` and `rv32_plant_exit_codes.sh`, `receipts/rv32-plants/summary.txt`), Debug and Release give the same exit codes. `owed-timer-probe-not-held`, `owed-hold-skips-retry`, `owed-bind-wait-unset` and `owed-hold-uncounted` exit 104. `owed-held-probe-lost` exits 105. `owed-bind-wait-kept` and `owed-hold-rearmed-late` exit 106. `owed-hold-skips-delay` and `owed-held-flag-kept` exit 0.
   - These are exactly the author's `rv32-plant-exit-codes.txt`. Smoke checks 102-109 (`examples/rv32/smoke.c:354-377`) step through the hold.
5. **Disclosed limit (gated port): stated and correct.**
   - PORTING:100-101 and the PR integration note give the budget of `ACMP_OWED_MAX` + 1 + `n_sinks` passes for a port that only tests `acmp_rx_ready`.
   - Probe (gated port, 16 sinks): 14 retries one per pass put the BIND_RX at pass 23, within 25. With 14 retries all in pass 1, the answer comes in pass 10 with 13 probes lost. That loss is the documented "no probe held, none waiting" case.
   - A gated port never has a frame declined, so `bind_waiting` is never set: `busy_declined` 0 and `probes_held` 0, as disclosed.
6. **Memory, cost, prior items, port-contract phrases.**
   - `sizeof(struct acmp)` is 5072 B on RV32 and 5080 B on x86-64: +8, from `probes_held` plus 4 bytes of alignment. `struct acmp_sink` stays 256 B and the owed set 640 B (`receipts/measure/sizes.txt`). The two flags fill existing padding (`include/acmp.h:381`, `:423`).
   - Cost table: the author's round-3 harness rebuilt at the exact head gives ELFs byte-identical to the author's (`5f6556bd…` rv32i -O3, `ac27df49…` rv32im -Os). The results are identical row by row, and `acmp.o` text is 19365 and 10789 (`receipts/measure/compare-with-author-r3.txt`).
   - Every "before" and "after" cell of the PR table matches the author's start and final receipts. The bare-metal Release ELF from `baremetal.py` is `f1fd4b90…`, 50504 B, identical to the author's.
   - R793-2 S3, S4 and RES1-RES4: handled (table at the end).
   - `scripts/check_port_contracts.py` pins 12 new CRITICAL phrases: 2 under `acmp_rx_ready`, 4 under `bind_waiting` and 6 under `probes_held`. All are present in PORTING. The gate's self-test refuses 45 meaning-removal controls, up from 33 at 968a164 (`receipts/gates/logs/port-contracts.log`).
   - The fields `bind_waiting` and `probe_held` and the counter `probes_held` are in the field, counter and REQUIRED tables.

## Findings

### F3: MINOR (Docs, Robustness). The answer-time budget covers only the first kept command; commands kept behind it miss 200 ms at the margin the new test calls documented
- **Where:**
  - `docs/PORTING.md:96-98`: "sends it in pass `ACMP_OWED_MAX` + 1 after the egress returns, a BIND_RX included, whatever timer probes fall due meanwhile … That delay plus the egress hold must stay within the 200 ms command timeouts".
  - PR body, Round 3 item 1: "Result: a deferred BIND_RX, like any kept command, is answered in pass `ACMP_OWED_MAX` + 1".
  - `tests/test_acmp.cpp:3010-3024`: 191 ms is "the documented margin".
- **Evidence** (`receipts/probes/probe-r3-head.txt`, `backlog-at-968a164.txt`):
  - At a 191 ms hold, a BIND_RX and then a GET_RX_STATE kept give answers at 200 ms and **202 ms**.
  - With five mixed commands kept at a 60 ms hold, the answers come in passes 9, 11, 12, 14 and 15. Each command after the first is later by one pass per frame owed by the kept commands ahead of it: two for a BIND_RX, one for the others.
  - Two GET_RX_STATE kept at 191 ms leave at 200 and 201 ms, at this head and at 968a164, so the gap is latent from earlier rounds.
  - The author's own case `{behind = 2}` checks that the kept answers leave after the BIND_RX frames (positions 10, 11), but not when.
- **Impact:**
  - An integrator who sizes the egress hold from PORTING (hold + 9 passes ≤ 200 ms, so ≤ 191 ms) misses the Milan v1.2 Table 5.26 timeout for every command the port keeps behind the first. A BIND_RX followed by a GET_RX_STATE is an ordinary controller sequence.
  - The core's order is correct. The defect is the contract's timing figure, as with F2 in round 2, so it is not RESIDUE.
  - I raise it now because this round restates the pass count for "a BIND_RX included" and "like any kept command", adds the margin test, and the round's check (1) asks about "every frame behind it". My R793-2 F2 wording ("and every command kept behind it … by pass `ACMP_OWED_MAX` + 1 + `n_sinks`") made the same error, and this corrects it.
- **Required outcome:**
  - (a) In "ACMP owed bound", after PORTING:97, add for example: "A command kept behind other kept commands is sent one pass later for each frame they owe, two for a BIND_RX and one for any other command: it leaves in pass `ACMP_OWED_MAX` + 1 + *f*, where *f* counts the frames owed by the kept commands ahead of it. Budget the egress hold for the deepest backlog the port keeps."
  - (b) In the PR body, change the Round 3 "Result" sentence to, for example: "a deferred BIND_RX at the head of the kept frames is answered in pass `ACMP_OWED_MAX` + 1, whatever probes fall due; a command kept behind it follows one pass per frame owed ahead of it."
  - (c) Recommended: in the `behind` case, assert the kept answers' passes (11 and 12), and pin the new sentence in `CRITICAL`.
- **Verification:** `python3 scripts/validate.py --work <w> --jobs 16 --graphs` gives 28/28 (port-contracts and test-inventory included), and the PR text no longer gives one pass count for every kept command.

### F4: MINOR (Tests). Five stated behaviours of the hold are not pinned; reviewer plants pass the full 113-test suite
- **Where:** `src/acmp.c:798`, `:1100`, `:1268` and `:864`, against `docs/PORTING.md:82` and `:86` and ACMP-12 (`docs/REQUIREMENTS.md:52`, `docs/requirements.json`). The test port model `pass()` is at `tests/test_acmp.cpp:2580-2592`.
- **Evidence:**
  - `scripts/reviewer_plants.json` and `scripts/run_reviewer_plants.sh` produce `receipts/reviewer-plants.txt`. Each plant is built by the repository's own `mutation.py` and its binary is run on all 113 tests.

    | Plant | Contradicts | Full suite |
    |---|---|---|
    | `rv-bind-wait-cleared-by-every-poll`: `acmp_poll` clears `bind_waiting` even when the egress refuses | PORTING:82 "the next `acmp_poll` that accepts an owed frame clears it" (a pinned phrase) | **passes 113/113** |
    | `rv-bind-wait-set-when-full`: also set for a BIND_RX declined with no slot free | ACMP-12 and PORTING:82 "declined with one slot free"; probes falling due during the egress hold become held instead of lost | **passes** |
    | `rv-hold-widened-to-the-timeout`: also holds the TMR_NO_RESP give-up in PRB_W_RESP2 | PORTING:86 (only a TMR_DELAY expiry or TMR_NO_RESP retry); it sends nothing, and delays LISTENER_TALKER_TIMEOUT | **passes** |
    | `rv-hold-widened-to-every-timer`: also holds TMR_RETRY and TMR_NO_TK | PORTING:86, counter table | **passes** |
    | `rv-bind-unsets-no-hold`: a new binding keeps its sink's `probe_held` | "the hold ends once nothing is held"; the stale flag keeps holding full-set probes that should be lost | **passes** |
    | `rv-probe-held-never-set`, `rv-hold-scan-skips-the-last-sink`, `rv-hold-whenever-full` | (controls) | caught (3, 2 and 2 tests) |

  - The first plant is a real regression path to F2, demonstrated by `scripts/probe_intermittent.cpp` (`receipts/probes/refused-poll-*.txt`). The port follows PORTING:83 literally: it redelivers only after an accepting poll. The egress refuses in pass 2, and another sink's retry falls due then.
    - Head: the BIND_RX is answered in pass 10 at position 8 and the retry follows it (`probes_held` 2).
    - With the plant: the retry is owed ahead (position 8), and the BIND_RX slips to pass 11 at position 9.
  - The suite misses it because its port model redelivers in every pass, refused or not. So the BIND_RX sets the flag again before timer service.
- **Impact:**
  - CONTRIBUTING: "A regression needs a failing assertion and a runnable planted defect."
  - Four sentences of the new ACMP-12 and PORTING text, one of them pinned by the port-contract gate, have no assertion behind them. One of the gaps hides the exact defect this round fixes.
  - The code at this head is correct in each case, by code reading and the refused-poll probe.
- **Required outcome:** add assertions, and register each plant (or an equivalent) with its killer:
  - (1) A case in which the egress refuses one poll while the BIND_RX waits and the port redelivers only after accepting polls, with a retry falling due in the refused pass. No probe leaves ahead of the BIND_RX answer.
  - (2) A BIND_RX declined at 8 owed, with a retry falling due during the hold. The retry is lost and counted, `probes_held` unchanged and `bind_waiting` false. If holding there is wanted, change ACMP-12 and PORTING instead.
  - (3) A PRB_W_RESP2 timeout (and a TMR_RETRY) falling due while `bind_waiting` is set runs at its deadline, with `probes_held` unchanged.
  - (4) A BIND_RX to another talker for a sink whose probe is held clears `probe_held`, and a later full-set probe is lost.
- **Verification:**
  - `python3 scripts/mutation.py --work <w> --select owed- --jobs 16` shows the new plants CAUGHT.
  - `scripts/run_reviewer_plants.sh <clone> <dir>` shows each of the five failing at least one test.
  - validate.py gives 28/28.

### SUGGESTION
- **S5 (Docs).** PORTING:86 says "a port that services its timers once per pass retries it in the next pass". That holds for passes of at least 1 ms. A port that polls faster retries at the next millisecond, so the held probe's bound in passes then reads in milliseconds. Say so in one clause.
- **S6 (Robustness, Docs).** A held probe has no fixed wait while the port keeps commands.
  - Probe `SustainedCommandsBehind`: two retries stay held for 40 passes of continuing GET_RX_STATE (`probes_held` 80, `probes_lost` 0) and leave in pass 52. Their sinks' probing does not time out meanwhile. Before this round they would have been lost and recovered by TMR_NO_RESP.
  - PORTING:88's per-frame term covers this. Saying it outright would help integrators: "while the port keeps commands a held probe keeps waiting, and its sink's probing does not time out."

### RESIDUE (wording only, carried to the residue checklist)
- **RES5 (`docs/PORTING.md:87` and the counter table, `probes_held` row, `:336`).** "Each pass that holds a probe increments `probes_held`" and "Passes that held a timer probe" undercount. The counter rises once per held probe in each pass: 14 probes held in one pass add 14, and the all-in-pass-1 probe ends at 119. The test asserts the per-probe sum.
  - Fix PORTING:87 to: "Each pass increments `probes_held` once for every probe it holds."
  - Fix the table row to: "Timer probes held for a waiting BIND_RX or behind another held probe, counted once per probe for each pass it is held. A held probe is never dropped."
- **RES6 (`docs/PORTING.md:88`).** "A held probe therefore waits from the pass it falls due through the pass that takes the BIND_RX" → "A held probe therefore waits at most from the pass it falls due through the pass that takes the BIND_RX". Behind a BIND_RX that owes only its answer, it is owed in the take pass (unknown-sink probe). The pinned phrase stays intact.

Comment rule: the delta's new comments in `src`, `include`, `tests`, `examples` and `scripts` carry only requirement and clause IDs (`// REQ: ACMP-12, ACMP-09`, `// Milan v1.2 5.5.3.5.3; Milan v1.2 Table 5.26`). None shows a bench lane label, lane name, review round, reviewer ID or issue-comment ID, and the comments gate passes. The three commit subjects are single lines with no body (privacy gate rc 0). No RESIDUE arises from either.

## Prior public review findings at this head

| Finding | Source | Status at b7a5988 | Evidence |
|---|---|---|---|
| F2 MINOR (Robustness, Docs): a due sink probe takes the freed slot ahead of a kept BIND_RX | R793-2 | **Resolved at its cause** (design change: the hold) | Unchanged round-2 probe gives pass 9, `probes_lost` 0. Three new tests and nine plants, which escape without them. PORTING:85-89 and the Round 2 PR sentence were rewritten. My required outcome (a) misstated commands kept behind the BIND_RX; F3 corrects it. |
| S3 SUGGESTION: GET_TX_STATE test lacks connection_count | R793-2 | **Resolved** | `r.count == 0u` added (`tests/test_acmp.cpp:2908`). |
| S4 SUGGESTION: publish a full validate and baremetal receipt at the exact head | R793-2 | **Resolved** | `author-r3/receipts/final-gates.json` (28 entries, rc 0, head `b7a5988`), `final-mutation.log` (426 CAUGHT) and `final-baremetal.log`; per-commit `gates-s1b/s2/s3`. All hashes match the evidence MANIFEST. |
| RES1: Debug ELF 145380 vs 145180 | R793-2 | **Resolved** | Sync section note added, with the suggested wording. |
| RES2: "Round 3 merges …", privacy bullet | R793-2 | **Resolved** | "This sync merges main d7e6a2a1"; "Main fixed this in #30; see Sync with main cc3362f8." |
| RES3: ARCHITECTURE BIND_RX slot rule | R793-2 | **Resolved** | `docs/ARCHITECTURE.md:11`, with the suggested wording. |
| RES4: test count in "How to validate" | R793-2 | **Resolved** | "the full ACMP test binary (113 tests at this head: 112 ACMP tests and main's Wire test)", which matches the binary. |
| F2, R1, S4, S5 | R794-2 | **Resolved / taken** | See "Other reviewer's findings" below. Read after my verdict and ledger were written. |

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | The hold delays only the send of the two expiries that emit a PROBE_TX (Milan v1.2 5.5.3.5.10 and 5.5.3.5.16; code `:806-812`). TMR_NO_RESP still runs from the send, and no held probe is lost. Every taken own command gets its specified response, never an error status (IEEE 1722.1-2021 8.2.4/8.2.5, Table 8-3). The head-of-queue BIND_RX meets 200 ms at the stated margin (Table 5.26). F3 is a port-budget statement, not a core behaviour; the core's order is per contract. Clause text is judged from repository citations (limits). |
| RTL | CLEAN | No HDL in the delta, so Verilator was not used. Applied to the bare-metal RV32 target: `baremetal.py` rc 0 in Debug and Release at the exact head, and the Release ELF is byte-identical to the author's. Smoke checks 102-109 step through the hold. Seven of nine plants exit 104/105/106 in both builds, identical to the author's codes. Both measurement ELFs are byte-identical. |
| Robustness | UNCLEAN (F3) | Memory +8 B in `struct acmp`, sink and owed set unchanged. The declined BIND_RX at 7 costs 205 / 355 instructions. A held retry costs 5575 / 16753, and a lost retry scans 16 sinks (6491 / 18641). No lost held probe and no stale flag at the end in 11 probe cases, 16-sink worst case included. The refused-poll case is correct at the head. F3: the budget figure is wrong for kept backlogs. S6 is optional. |
| Tests | UNCLEAN (F4) | 426/426 plants CAUGHT at the exact head. The nine new plants escape without the three new tests (110/110 pass). The new tests assert pass by pass, including the commands kept behind. Coverage `acmp.c` is 813/813 lines and 424/424 branches. F4: five reviewer plants against stated behaviours pass all 113 tests. |
| Docs | UNCLEAN (F3) | PORTING owed-bound section, field and counter tables, ACMP-12 (REQUIREMENTS and requirements.json), ARCHITECTURE, VERIFICATION (422 + 4 plants, RV32 row), TESTS, TRACEABILITY, CHANGELOG, 12 new port-contract pins and the PR body were all checked against code and receipts. F3 is the timing-figure defect. RES5 and RES6 are wording only. |

## Executed evidence (this review, exact head unless stated)

Pinned tool root: GoogleTest 1.14.0, clang-tidy 18 and the clang-18 lexer (`scripts/env.sh`). Host GCC 16 for the GCC arm and host Clang for the sanitizer arm; RV32 used riscv64-elf-gcc with QEMU.
- `scripts/run_gates.sh` runs `validate.py --graphs` (12 jobs) and `baremetal.py` (4 jobs) concurrently.
  - validate: **28/28 rc 0** (`receipts/gates/validate.out`, `validate.rc`, `gates.json`, `logs/`). Mutation is 426 CAUGHT / 0 ESCAPED / 0 ERROR. Privacy covers 28 commits, 337 historical blobs and 98 files.
  - bare-metal: rc 0 in Debug and Release (`receipts/gates/baremetal.out`). The Release ELF is `f1fd4b90…`, 50504 B. The Debug ELF is 150672 B; its size is path-dependent and was not compared.
- Escape check without the round-3 tests: `scripts/escape_without_round3.sh` (`receipts/escape-without-round3.txt`).
- Reviewer plants: `scripts/run_reviewer_plants.sh` (`receipts/reviewer-plants.{txt,json}`).
- Probes: `scripts/run_probe.sh` with `probe_r3.cpp` and `probe_intermittent.cpp`, and `run_probe_timer_ahead.sh` with `probe_timer_ahead.cpp`, unchanged from round 2 (`receipts/probes/`).
- RV32 plants: `scripts/rv32_plant_smoke.sh` and `rv32_plant_exit_codes.sh` (`receipts/rv32-plants/`).
- Cost and sizes: `scripts/measure.sh` with the author's round-3 harness (`scripts/measure-r3.c`, built as `measure.c`, `-DLANE`) and `scripts/sizes.c` (`receipts/measure/`).
- Author evidence: milan-fpga `28625428`. All 337 `MANIFEST.json` entries hash-match (64 under `author-r3`), and no file is unlisted (`receipts/author-evidence-check.txt`).
- Hosted CI at the exact head, inspected only (`receipts/hosted-checks.txt`, `hosted-steps.txt`): push run `42481173198` and PR run `42481176344` both succeeded. Their quality and bare-metal jobs ran 28 steps, all success, none skipped. Hosted and act acceptance belong to the manager.
- Clone restored and verified (`receipts/clone-state.txt`):
  - HEAD, index tree and worktree all equal `2b5baf18…`, and all 98 files re-hash to their HEAD blobs.
  - All 98 files have mode 100644. No gitlinks or `.gitmodules` are required or present.
  - The gate run's ignored `scripts/__pycache__/` was removed, leaving 0 untracked or ignored entries. All probes, plants and builds ran in exported copies under the packet's `scratch/`.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `src/acmp.c` (`probe_yields`, `sm_expired`, `acmp_rx` decline, `acmp_poll`, `sm_stop`, `bind`, `send_probe`, `probe_left`), ACMP-12 text, PORTING owed bound, new tests' timing and field assertions, issue #26 acceptance | R793-3 (delta). Untouched code keeps its R793-1/2 verdict | b7a59887f5f2ff729206b87a268972c637882dc0 |
| RTL | CLEAN | `examples/rv32/smoke.c` `acmp_owed_smoke` (checks 102-109), `baremetal.py` Debug and Release, Release ELF against the author's receipt, nine RV32 plants, measurement ELFs | R793-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Robustness | UNCLEAN (F3) | hold predicate and flag lifetime, 11 probe cases (16 sinks, two interfaces, mixed backlog, unknown sink, margin, gated port, sustained commands, refused poll), memory and instruction counts | R793-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Tests | UNCLEAN (F4) | `tests/test_acmp.cpp` (three new tests, S3 change, fixture helpers), `tests/mutations.json` (9 new and 3 re-anchored plants), coverage ratchet, full validate run, escape check, 8 reviewer plants | R793-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Docs | UNCLEAN (F3) | PORTING, REQUIREMENTS, requirements.json, ARCHITECTURE, TRACEABILITY, TESTS, VERIFICATION, CHANGELOG, `check_port_contracts.py`, PR body (all sections), integration note against parent dev `0a75aa77` (`acmp_review_mutants.py:143`, `acmp_mutants.py:452-455`), comment-rule scan | R793-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |

## Other reviewer's findings (read after this verdict and ledger were written)

R794-2 at 968a164 (public PR comment 6721016350) recorded F2, R1, S4 and S5. Its status at b7a5988:

| Finding | Status at b7a5988 | Evidence |
|---|---|---|
| F2 MINOR (Conformance, Robustness, Tests, Docs): timer probes overtake a deferred BIND_RX | **Resolved at its cause.** Its option 2 was adopted. | Its 14-retry case gave the BIND_RX at pass 23 at 968a164. At this head, my 16-sink run with 14 retries one per pass gives pass 9 with `probes_lost` 0. The 191 ms margin now gives 200 ms with one retry (the committed margin test) and with seven (my probe). Its required verification (a test plus a plant that removes the hold, caught) is met by the three new tests and `owed-timer-probe-not-held`. Its phrase "every frame the port holds behind it" is answered by F3: probes no longer delay those frames, but the frames owed ahead of them still do. |
| R1 RESIDUE: Debug ELF 145380 vs 145180 | **Resolved** | Same fix as my RES1: the sync-section note in the PR body. |
| S4 SUGGESTION: pin the timer interplay in the RV32 smoke | **Taken** | Smoke checks 102-109. Seven of nine hold plants make the smoke exit nonzero in Debug and Release (focus 4). |
| S5 SUGGESTION: name the rest of the parent mutant entry and the wider decline window | **Taken** | The PR integration note names the renamed killer test and both needles, and says a port that ignores the return value now also loses a BIND_RX at seven owed. I checked it against parent dev `0a75aa77` `acmp_mutants.py:450-456`. |

Reading this report also showed that the brief's probe names `TimerProbesAgainstTheDeferredBind` and `DocumentedBudgetAtTheMargin` are R794-2's round-2 probes. My probes of those names were written independently this round, before I read it. Nothing in R794-2 changes my verdict, findings or ledger.

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not available. Clause content was judged from the repository's citations, the code's clause tags and the cited table contents.
- The manager's ruling (R794-2 option 2) was taken from the review brief. I found no public comment carrying it.
- The probes use the committed port model (1 ms passes, one poll per pass), plus a gated variant and a literal-contract variant. Ports with sub-millisecond passes or several polls per pass were reasoned about, not run (S5).
- The evidence commit `28625428` has no cryptographic signature (`%G?` = N). Its integrity rests on the MANIFEST.json hashes, which I verified, and on the public branch tip.
- The sanitizer arm and coverage ran with host compilers. CI's Ubuntu 24.04 arms are covered by the hosted run, not by this review. My coverage counts equal the ratchet the author generated with GCC 13.3.
- Debug ELF bytes depend on the build path and were not compared.
- The parent harness row ("an ACMP command behind the owed input") still needs the parent PR. Issue #26 stays open by design ("Relates to").
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus this review's own runs.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base 70936b77 against live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c; builder and native banks), and link those receipts on the PR.
- Own hosted and act acceptance. Both runs at the exact head showed success at inspection.
- Route F3 and F4 to the author. After the fixes, obtain two independent positive reviews at the new head.
- Carry RES5 and RES6 to the residue checklist, and S5 and S6 as optional.
- Track the parent PR. It must bind the ready hook to `acmp_rx_ready` (or keep declined frames), change the `acmp_mutants.py` 452-453 fragment and the `acmp_review_mutants.py` 143 fragment, and then measure the harness row.

R793-3 FINISHED
