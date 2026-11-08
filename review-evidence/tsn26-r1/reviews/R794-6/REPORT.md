[R794] POSITIVE - exact head 376486b374782147d71e5e9bb4f93c42cd10e636

# R794-6: external independent delta review of kebag-logic/tsn-c-stack PR #28 (issue #26), round 6

- **Head:** 376486b374782147d71e5e9bb4f93c42cd10e636, tree f4fd5321cb7d5e1b0fa72f7b894946cec0a9641d (both checked in the isolated review clone).
- **Delta reviewed:** 715d208..376486b, which is my round 5 head to this head: two commits, c0477c8 and 376486b. Nothing was rebased.
- **Authority for this round:** the round 6 ruling on PR #28 (issuecomment-6728504171). It removes the held-probe wait bound rather than patching it. No held-probe upper limit is asked for here.
- **Verdict: POSITIVE.**
  - The round 6 delta does what the ruling asks, items 1 to 4.
  - The core is untouched: `git diff --stat 715d208 376486b -- src include examples` is empty.
  - The new sentences match `src/acmp.c`.
  - The new named assertion fails under its registered plant and passes at the head.
  - All 28 gates pass on a clean clone with `--graphs`, including the full mutation campaign: 444 caught, 0 escaped, 0 errors.
  - `baremetal.py` returns 0 in Debug and Release. The Release ELF is byte-identical to the author's.
  - My round 4 and round 5 probes, run unchanged, give byte-identical PROBE lines and fall within the new sentences.
  - Two new wording RESIDUE items and two new SUGGESTIONs are recorded below. One concurrent-review RESIDUE is retained. No MINOR, MAJOR or BLOCKER is open.

## Reconstruction (in the required order)

1. **Repository rules.** CONTRIBUTING.md and docs/README are unchanged since round 5; the repository has no AGENTS.md. docs/CODING_STANDARD.md and the comment rule were applied to the added lines.
2. **Issue #26 acceptance and scope.** These are unchanged since round 5. The acceptance concerns command answers within their IEEE 1722.1-2021 / Milan v1.2 Table 5.26 timeouts. The ruling restates this, adding that no Milan deadline depends on a held probe's wait.
3. **Requirements and interface authorities.** These are ACMP-12 and ACMP-09 (docs/REQUIREMENTS.md, docs/requirements.json), the "ACMP owed bound" section of docs/PORTING.md, `include/acmp.h` and `src/acmp.c`. REQUIREMENTS, requirements.json, CHANGELOG and every header are unchanged in the delta.
4. **The diff.** `git diff 715d208 376486b` changes seven files: docs/PORTING.md (:92, :94, :110, :114), docs/TESTS.md, docs/TRACEABILITY.md, docs/VERIFICATION.md, scripts/check_port_contracts.py, tests/mutations.json (+1 plant) and tests/test_acmp.cpp (+1 test). The full PR diff against 70936b77 was reviewed in rounds 1 to 5. Only this delta is re-judged.
5. **Public executable evidence.** I checked the author's round 6 receipts at milan-fpga bac9305fbe27af1bb8c9415c056c3b77119cd6fb, `review-evidence/tsn26-r1/author-r6`, against my own runs (`receipts/evidence-check.txt`).
   - 15 receipts were fetched and their git blob ids checked: all match.
   - The evidence commit is unsigned on GitHub, so integrity rests on blob ids only.
6. **PR body.** It was read live at this head (headRefOid 376486b, 50869 characters). It contains the Round 4, Round 5 and Round 6 sections. Rounds 2 and 3 were moved, unchanged, to the linked `PR-BODY-rounds-2-3.md`, which the brief says is not a finding.

## Checks (1) to (6) of the brief

### (1) The held-probe statements in PORTING and the PR body: met

- **PORTING:110 removes everything the ruling names.** The "waits at most" sentence is gone, along with its count of one probe per other sink, its TMR_NO_RESP (200 ms) condition, the "past that" list and "These counts assume passes at least 1 ms apart". A repository-wide search for `waits at most|past that|per other sink|has waited less than|through the pass that takes|These counts assume` finds nothing.
- **PORTING:110 now makes the four ruling statements, nearly word for word.** Each matches the code:

| Statement (PORTING:110) | Code | Evidence |
|---|---|---|
| A held probe is never dropped for want of a slot | `sm_expired` (`src/acmp.c:794-804`) re-arms a yielding probe 1 ms on and returns. A held probe is cleared only by `sm_stop`, which runs on the probe leaving or on its sink's probing being cancelled (:355, :805). A probe goes to `probes_lost` (:744) only through `send_probe` when `probe_yields` is false, which needs no probe held (:786-791) | Reviewer plant `reviewer-held-probe-dropped-after-four-holds` is killed by the new test and four others (`receipts/escape-check6.txt`). In probe 8, `probes_lost` stays 0 for every held probe |
| It takes a freed slot only at timer service, with no BIND_RX waiting, after every command the core takes first, kept or offered for the first time | The only path that owes a held probe is `acmp_timer_expired` → `sm_expired` (:1191-1192). `probe_yields` returns true while `bind_waiting` is set (:780-782). Under the redelivery rule (PORTING:85), every waiting frame is offered before timer service | The new test asserts the pass `taken + 1 + later` exactly. Probe 7, both modes, gives 3, 4, 6 and 13 for 0, 1, 3 and 10 later commands |
| No command answer waits for it | It follows from the row above | The new test asserts `position(answer) < position(retry)` for every GET offered after the BIND_RX is taken |
| No upper limit while commands keep taking freed slots; its TMR_NO_RESP runs from when it leaves | `probe_left` → `no_resp_from_send` (:751-760) | The new test asserts `timer_deadline == retry->at + TMR_NO_RESP_MS`. Probe 7 shows the wait growing one pass per later command |

- **The PR body matches.** Round 4 item 3 (body lines 402-417) and Round 5 item 3 (body lines 515-530) now carry the same statements. Neither states a "waits at most" bound, a per-sink count or a "past that" list.
  - One leftover remains in **Round 4 item 1**; see RES11. It is wording only.

### (2) The command bound and the egress-hold budget: unchanged

- PORTING:103-113 is unchanged except :110. That covers n + 1 + f + r with its n and f definitions (:107-:108), the first-command pass (:109), the budget (:111-:112) and 193 − 2 × Q (:113).
- `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem`, `KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout` and `KeptCommandsBehindSevenOwedLeaveOnePassSooner` are unchanged and pass.
- Probe 6 is byte-identical to round 5: 9, 11 and 12 from eight owed; 8, 10 and 11 from seven owed.

### (3) :92 and :94 count commands offered for the first time: met

- :92 now ends "after the commands the port still keeps or offers before its timer service".
- :94 now begins "While the port keeps or offers commands that take the freed slots, or no owed frame is accepted".
- Both are my round 5 wording, word for word, and both match the code paths above.

### (4) Pins, named assertion, plant and removals: met

- **CRITICAL, `probes_held`.** The six pins of removed or changed clauses are dropped. Eight new phrases are pinned: the :92 ending, the :94 opening, and six phrases of :110.
  - The three restart-path phrases and "at most one per sink while no sink's probing restarts" are now pinned under `acmp_rx_ready`. They now qualify :114, the only remaining count that uses them.
  - On my clean clone, the `port-contracts` gate refuses all name-removal controls and 77 meaning-removal controls (`receipts/gates/port-contracts.log`).
- **Named assertion.** `AcmpOwed.CommandOfferedAfterTheTakenBindDelaysTheHeldRetry` (`tests/test_acmp.cpp:3492`) asserts "after the BIND_RX is taken, a GET_RX_STATE offered after the next accepting poll delays the held retry one pass" with `EXPECT_EQ(owed, taken + 1u + later)`. It runs for 0, 1 and 3 such commands.
  - It uses the same pass model as the fixture's `pass()`: an accepting poll, kept frames until one is declined, the fresh GET, then timer service.
- **Registered plant `owed-held-probe-owed-at-the-poll`** (`receipts/escape-check6.txt`).
  - At the head the full suite passes, 126 of 126.
  - Under the plant only the new test fails, and both registered needles are SEEN inside its block.
  - Without the new test, 125 of 125 pass, so the plant is pinned by this test alone.
  - On my clean clone the campaign reports it CAUGHT (`receipts/gates/mutation-summary.txt`).
- **Two reviewer plants of my own** (`scripts/plants-r6.json`).
  - `reviewer-held-probe-waits-with-a-slot-free` makes a held probe also yield with exactly one slot free and no BIND_RX waiting. The new test kills it, as do two older tests.
  - `reviewer-held-probe-dropped-after-four-holds` lets a held probe fall through to `send_probe` after four holds. The new test kills it, as do four older tests.
- **Removals.** No test or plant was removed: the delta deletes no line under `tests/`, and the plant names in `mutations.json` go from 443 to 444 with none missing.
  - None of the 125 earlier tests asserted the removed limit.
  - `ProbesFallingDueInTheDrainWaitForTheDeferredBind` asserts the exact held-probe passes with no command after the BIND_RX. The retained sentence "Held probes follow the frames of the last kept command, one per pass" still covers it, for 1 ms passes.

### (5) RES9: resolved

- PR body Round 5 item 4 (line 547) now reads "a probe that falls due then, with no probe held, is lost". That is my exact fix.
- RES8 went with the removed clause.

### (6) My earlier probes, unchanged, at this head: all within the new sentences

- **Probe 7** (`probe_owed7.inc`, round 5): its PROBE7 lines are byte-identical to round 5 (`receipts/probe7-at-376486b.txt`).
  - The held retry is owed in passes 3, 4, 6 and 13 with 0, 1, 3 and 10 later commands, whether those commands are offered fresh or declined and then kept. `probes_lost` is 0.
  - Its "stated owed by pass 3" column prints the limit that round 6 removed. Under the new text the result is "no upper limit while commands keep taking the freed slots", and each pass follows the commands the core takes first.
- **Probe 6** (`probe_owed6.inc`, round 4): byte-identical to round 5 (`receipts/probe6-at-376486b.txt`). It gives n = 8 and n = 7 as in check (2).
- **Round 4 and round 5 plant checks**, run unchanged (`receipts/escape-check4-at-376486b.txt` and `receipts/escape-check5-at-376486b.txt`).
  - Every plant still fails the suite, and every registered needle is SEEN.
  - The only difference from the round 5 receipts is that the new test now also kills three reviewer plants: `reviewer-seven-owed-bind-holds-nothing`, `reviewer-hold-at-seven` and `reviewer-scan-skips-last-sink`.
- **Probe 8** (`probe_owed8.inc`, new this round, `receipts/probe8-subms-passes.txt`): passes less than 1 ms apart. It is the basis of RES10.
  - With passes 1 ms apart, the held probes are owed one per pass (3, 4, 5 and 6), and nothing is lost.
  - With two or four passes per ms and four retries due in the same ms, two or three held probes are owed in the same pass, and nothing is lost.
  - In every case the BIND_RX answer leaves in pass n + 1, so no command answer moves.

### Gates on a clean clone of the exact head

- **`python3 scripts/validate.py --graphs --work <w> --jobs 6`** returns rc 0, with 28 of 28 gates at rc 0 (`receipts/gates/validate.log`, `gates.json`).
  - Mutation: 444 caught, 0 escaped, 0 errors.
  - Coverage of `src/acmp.c`: 813/813 lines and 424/424 branches.
  - The port contracts refuse 77 meaning-removal controls.
  - Both sanitizer arms, static analysis (clang-tidy 18.1.3), privacy and graphs pass.
- **`python3 scripts/baremetal.py --work <w> --jobs 2`** returns rc 0 in Debug and Release (`receipts/rv32-baremetal.log`).
  - The Release ELF is 50504 bytes, sha256 `f1fd4b90…a7c2`. That equals the author's final receipt and round 5.
  - The Debug ELF differs from the author's only by build-path debug info.
- **Hosted runs at this head:** two "Portable core quality" runs, push and pull_request. Their `quality` and `bare-metal` jobs all succeeded, and all 14 steps of the pull_request run executed with none skipped (`receipts/hosted-summary.txt`). This is inspection only; hosted and act acceptance are the manager's.

## Lens results

### Conformance: CLEAN

- **ACMP-12 is unchanged.** Its requirement text (hold each timer probe while a BIND_RX declined with one slot free waits; never lose a held probe) is still met by the unchanged code. The delta removes only a derived local limit, which the ruling says no Milan or IEEE deadline depends on.
- **The Milan clauses cited at PORTING:90-:91 are unchanged:** 5.5.3.5.3, .10, .16, .23, .30, .31, .36 and Table 5.26.
- **The command-answer timing that #26 accepts is unchanged** (check 2). Probe 8 shows that it is unaffected even by passes under 1 ms.

### RTL (C core, both targets): CLEAN

- The core delta is empty.
- The Release RV32 image is byte-identical to round 5 and to the author's image.
- Debug and Release both return rc 0, and the hosted bare-metal job succeeded.
- Nothing the core depends on changed, so the round 5 verdict carries.

### Robustness: CLEAN

- Through the unchanged code, the new test and my two reviewer plants, a held probe is never lost and never jumps a command the core takes first.
- Probe 8 adds passes under 1 ms: held probes are still never lost, and no command answer moves.
- A retry that falls due just after the last held probe left, and finds every slot owed, is lost and counted. PORTING:96 states exactly that case ("With no probe held and no BIND_RX waiting …"), and ACMP-12 does not cover it. That is not a defect.

### Tests: CLEAN

- **New test.** It is exact-pass and pinned by its plant alone (check 4). It is traced in TESTS.md and in TRACEABILITY.md under ACMP-09 and ACMP-12 with correct line anchors (:3492 and the moved :3549). Its message strings pass the assertion-template and needle gates.
- **Plant registry.** It grows from 443 to 444 entries. VERIFICATION.md says "440 core plants and four generated configuration plants", which matches the campaign's 444.
- **Removed tests and plants:** none.
- **Escape checks.** My round 4 and round 5 escape checks and the new escape check 6 all return rc 0, with every needle SEEN.
- One cosmetic SUGGESTION is recorded (S10).

### Docs: CLEAN (RESIDUE RES10 and RES11 recorded)

- **PORTING:92, :94, :110 and :114 match the code and the ruling** (checks 1 and 3).
- **TESTS, TRACEABILITY and VERIFICATION are consistent.** The commit messages and the added lines contain no lane label, review round, reviewer ID or issue-comment ID (`receipts/comment-scan.txt`: 98 added lines, 0 matches).
- **RES10 (PORTING:92) and RES11 (PR body, Round 4 item 1)** are wording only. Neither changes a measurement, a figure for the case the contract budgets, a test, the code or a clause claim.

## Findings

### RES10: RESIDUE (Docs). "held probes take freed slots one per pass" lacks its 1 ms premise

- **Where:** `docs/PORTING.md:92`: "…and held probes take freed slots one per pass, after the commands the port still keeps or offers before its timer service."
- **Evidence:** probe 8 (`scripts/probe_owed8.inc`, `receipts/probe8-subms-passes.txt`). Four TMR_NO_RESP retries fall due in the same ms beside a BIND_RX kept behind the full set. The port keeps the redelivery rule but runs its passes less than 1 ms apart.
  - **Two passes per ms:** the held probes are owed in passes 3, 5, 5 and 7, so two in pass 5.
  - **Four passes per ms:** they are owed in passes 5, 5, 5 and 9, so three in pass 5.
  - **Passes 1 ms apart:** they are owed in passes 3, 4, 5 and 6, one per pass as stated.
  - **Why:** each held probe is retried only at the first timer service at least 1 ms later (:90). Shorter passes free more than one slot between those services, so several held probes due in the same service each find a free slot.
  - **In every case:** `probes_lost` is 0, the BIND_RX answer leaves in pass n + 1, and the owed frames still leave one per accepted poll.
- **Why it is RESIDUE:**
  - The core behaves as designed, and no command answer, loss, test or budget figure changes.
  - The premise is already stated one sentence earlier, at :90 ("which is the next pass for a port whose passes are at least 1 ms apart").
  - Until this round, the same paragraph group also had "These counts assume passes at least 1 ms apart", which the delta removed with the bound.
  - The wording at :92 itself is older; I passed it in rounds 4 and 5.
- **Exact fix (keeps every CRITICAL pin intact):** add after :92: "With passes less than 1 ms apart, several held probes that fall due in one timer service can each take a freed slot in that pass."
  - Alternatively, insert "for a port whose passes are at least 1 ms apart" after "one per pass" at :92 and at :110's "Held probes follow the frames of the last kept command, one per pass". The :92 pin "after the commands the port still keeps or offers before its timer service" is unaffected either way.
- **Verification:** re-run `scripts/run_probes3.sh HEAD_TREE WORK OUT scripts/probe_owed8.inc 'AcmpOwedProbe8.*'`. Its output should match the amended sentence.

### RES11: RESIDUE (Docs, PR body). Round 4 item 1 still calls the held probe's wait "an upper bound"

- **Where:** PR body, Round 4 item 1, the "Held probes follow…" bullet (body lines 324-325): "A held probe's own wait is as round 3 stated it, now as an upper bound."
- **The gap:**
  - The Round 3 text (moved file, line 153 onward) and Round 4 item 3 now say the wait has no upper limit.
  - The bullet therefore contradicts both, and contradicts the ruling.
  - Round 6 item 1's list of PR-body sentences it re-aligned does not include this one.
- **Why it is RESIDUE:** it is wording in the PR body only. PORTING, the tests and the pins are right.
- **Exact fix:** replace that sentence with "A held probe's own wait has no upper limit (round 6; see item 3)."

### S10: SUGGESTION (Tests). A doubled blank line before the new test

- **Where:** `tests/test_acmp.cpp:3489-3490`. There are two blank lines between the end of `AnsweredProbeEndsTheHoldOfItsRetry` and `// REQ: ACMP-12, ACMP-09`, where every other test has one.
- **Fix:** delete one of the two blank lines. No gate depends on it.

### S11: SUGGESTION (Docs). Optionally scope "so no command answer waits for it"

- **Where:** `docs/PORTING.md:110`.
- **Why it is only a suggestion:** in context, the "so" ties the clause to "after every command the core takes first", which is true by construction. A command that reaches the core only after a held probe has become owed queues behind that frame, as it would behind any owed probe, and the n + 1 + f + r bound already covers it.
- **Why no change is required:** the wording is the ruling's own. A possible tightening would be "so no command the core takes before it waits for it", which would mean re-pinning `'so no command answer waits for it'`.

### S8: SUGGESTION (Tests, RTL), retained as declined

- This is the RV32 smoke step through the hold's boundaries, unchanged from rounds 4 and 5.
- The author lists it as "not taken, as outside the ruling" (PR body Round 6 item 4). It is acceptable as optional.

## Prior findings at this head

These are my own items, resolved from my own packets. The concurrent review's items are in the next section, which I wrote after this verdict and ledger.

| Item | Status at 376486b | Basis |
|---|---|---|
| R794-5 **F5** MINOR (Docs, Tests): the held-probe bound counted only kept commands | **Resolved by the ruling** | The bound is removed (check 1). :92 and :94 count commands offered for the first time (check 3). The changed phrases are re-pinned. The named assertion and plant I asked for are in, and the plant fails only under the new test (check 4). Probe 7 falls within the new text (check 6) |
| R794-5 **RES8** (the "past that" list named only the retry) | **Resolved** (removed with the clause) | PORTING:110 |
| R794-5 **RES9** ("with no probe held") | **Resolved** | PR body line 547, my exact fix |
| R794-5 / R794-4 **S8** (RV32 step) | **Declined; acceptable** | See S8 |
| R794-4 F4, S9; R794-3 F3, R2-R4, S6, S7; R794-1 and R794-2 items | **Remain resolved or taken** | The code they depend on is unchanged. The restart paths (S9) now qualify :114 and are pinned there. The round 3 and round 5 plants are still caught (check 6) |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-12 and ACMP-09 (unchanged), PORTING:76-118 against `src/acmp.c:721-825, 1085-1110, 1172-1196, 1254-1273`, Milan 5.5.3.5 clauses at :90-:91, the command bound and budget (unchanged), probe 8 (no answer moves) | R794-6 (delta); unchanged code R794-1 to R794-5 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| RTL (C core, both targets) | CLEAN | Empty `src include examples` delta; `baremetal.py` Debug and Release rc 0 on a clean clone, with the Release ELF byte-identical to round 5 and to the author's; hosted bare-metal job success | R794-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Robustness | CLEAN | Hold, cancel and loss paths (unchanged code) under the new test; 2 reviewer plants; probe 7 (later commands delay but never lose a held retry); probe 8 (passes under 1 ms: no held probe lost, no answer moved) | R794-6 (delta); R794-3 to R794-5 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Tests | CLEAN | New test `CommandOfferedAfterTheTakenBindDelaysTheHeldRetry`; plant `owed-held-probe-owed-at-the-poll` (fails only the new test, both needles SEEN, 125/125 without it, CAUGHT in the campaign); 2 reviewer plants; escape checks 4 and 5 re-run unchanged; no test or plant removed; local campaign 444/0/0; coverage 813/813 and 424/424 | R794-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Docs | CLEAN (RES10, RES11 recorded) | PORTING, TESTS, TRACEABILITY and VERIFICATION deltas; `check_port_contracts.py` (6 pins dropped, 8 added, 4 moved to `acmp_rx_ready`, 77 controls); the PR body Round 4, Round 5 and Round 6 sections and the linked rounds 2-3 file; the comment-rule scan of 98 added lines and 2 commit messages | R794-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |

## Concurrent review R793-5 at 715d208 (read after my verdict and ledger)

- **Source:** the public PR comment issuecomment-6728460478 (R793-5, POSITIVE at 715d208). Its packet copy is `reviews/R793-5/REPORT.md` in the evidence tree (blob `92f7acf7…`).
- **What changed after reading:** nothing. The verdict, the findings and the ledger are unchanged.
- **What I did not read:** any round 6 report by another reviewer.

| Its item | Status at 376486b | Basis |
|---|---|---|
| **RES8** (PORTING:110 "past that" named only the retry) | **Resolved** (removed with the clause) | PORTING:110; the ruling says RES8 goes with the removed clause |
| **RES9** (Integration note: "at most one per sink" lacks "while no sink's probing restarts") | **Retained as RESIDUE** | The author declined it as outside the ruling (PR body Round 6 item 4). The note now lives in the linked `PR-BODY-rounds-2-3.md` (line 85) and still lacks the condition, which PORTING:114 now carries. It is wording only. Exact fix, as that review gives it: "at most one per sink while no sink's probing restarts" |
| **S7** (RV32 smoke step) | **Declined; acceptable** | The same as my S8 |
| **S8** (test of port "one") | **Moot** | Option (a) of the redelivery rule excludes port "one" |

## Real limits

- **No standards PDFs.** Clause numbers were judged from the repository's citations.
- **Sanitizer arm.** It used the host's clang 23.1.4 for `clang`/`clang++`, as the author's run did ("Host GCC and Clang for the hosted arms"). The pinned clang 18.1.3 was on PATH as `clang-18` for the comment lexer and clang-tidy 18.1.3 for static analysis. The pinned clang 18 cannot build the gtest arm against this host's libstdc++ 16 (round 5 limit). The hosted run passes the arm.
- **Gate kit.** It ran with `--jobs 6` on 8 cores. A first attempt without `clang-18` on PATH failed seven lexer-dependent gates on my environment alone. It was discarded, and the run reported here used a fresh clean clone.
- **Author evidence was spot-checked, not re-run.** That covers the sentence map, `escape-final.txt` and the author's re-runs of the internal probes. I re-ran my own probes and plants and all gates.
- **Evidence commit.** It is unsigned; its integrity was checked by git blob ids only.
- **Probes 7 and 8 are fixture models** of the port contract's pass, not a real port.
- **No hardware.** No physical calibration or hardware was run, and field skips are not hardware proof.
- **No manager source bank.** I ran no manager source bank, parent build or parent harness, and I infer none. Hosted jobs were judged by job and step conclusions only.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`. Host paths in receipts are replaced by `<scratch>`, `<tools>` and `<reviews>`.
- **Scripts.** Set `TOOLS` to a prefix holding `gtest-1.14.0`. The RV32 gate also needs `riscv64-elf-gcc` and `qemu-system-riscv32`.
  - `scripts/run_gates6.sh GATES_CLONE RV32_CLONE WORK TOOLS JOBS`: the gate kit with `--graphs` and the RV32 gate, each detached with its own log and rc file.
  - `scripts/run_probes3.sh HEAD_TREE WORK OUT INC FILTER`: unchanged from round 5. It runs `probe_owed6.inc` and `probe_owed7.inc` (both unchanged) and `probe_owed8.inc` (new, RES10).
  - `scripts/escape_check6.py HEAD_TREE WORK OUT scripts/plants-r6.json`: the registered round 6 plant and 2 reviewer plants, each run with the full ACMP binary and again without the new test.
  - `scripts/escape_check4.py` with `plants-r3.json`, and `scripts/escape_check5.py` with `plants-r5.json`: unchanged from rounds 4 and 5. Their sha256 values equal my round 5 packet's copies.
- **Clone integrity** (`receipts/clone-state.txt`).
  - In the review clone, HEAD, the HEAD tree and the index tree are exact. There are no status entries of any kind, and all 98 worktree blobs match the index.
  - All entries are mode 100644. No gitlinks are tracked and there is no `.gitmodules`, so no submodule gitlink applies.
  - Both gate clones are at the head with no tracked changes after their runs.
  - The exported probe tree matches HEAD blob for blob.

## Pending manager duties

- **Merge-turn validation.** Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts. Hosted and act acceptance are the manager's.
- **Residue checklist.** Carry RES10 and RES11 to it, and the concurrent review's retained RES9 (the Integration note's gated-port sentence).
- **Parent PR.** The parent PR that moves the pin still has to carry out the integration-note items: the parent killer test and needles, and re-measuring the harness row. Until then #26 stays open, as the PR intends.

R794-6 FINISHED
