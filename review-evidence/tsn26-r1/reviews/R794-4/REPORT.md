[R794] NEGATIVE - exact head a0a32110511e444a23848367b7cbb4231e16ce5a

# R794-4: external independent delta review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- **Exact head:** `a0a32110511e444a23848367b7cbb4231e16ce5a`, tree `fedb871bbf9996ccca390fd723105558b447349e`.
- **Delta reviewed:** `b7a5988..a0a3211`, my round 3 head to this head (`b7b2048`, `c4a2bff`, `a0a3211`).
  - `git diff --stat b7a5988 a0a3211 -- src include examples` is empty. The core, the RV32 example and every behaviour are as at round 3.
  - Code the delta does not touch keeps its round 3 lens verdict.
- **Verdict:** NEGATIVE on one new MINOR, F4 (Docs, Tests). Everything else the brief names holds.
- **My round 3 F3 is resolved.**
  - All five plants I wrote in round 3 are registered in `tests/mutations.json` and fail at this head.
  - I re-ran them with my own script, and each is killed by its registered needles. The three that escaped every target at round 3 still escape once the round 4 tests are excluded (`receipts/escape-check4.txt`).
  - The hosted campaign and my local campaign both catch all 441 plants.
- **The derivation is right as an upper bound.** That holds for the derivation in `docs/PORTING.md:102-111` in every case, and for its egress-hold budget. A port that budgets as stated cannot miss a 200 ms timeout.
- **F4: the derivation states an exact pass, and that pass is wrong for one reachable case.**
  - The text says a kept command "leaves in pass `ACMP_OWED_MAX` + 1 + f + r". That assumes eight frames are owed when the egress returns.
  - Its own premise (PORTING:103) says a command is kept with seven **or** eight owed. A BIND_RX declined with one slot free leaves the egress returning with seven owed.
  - From seven owed, every kept command leaves **one pass earlier** than stated. The BIND_RX leaves in pass 8, not 9. The commands behind it leave in passes 10 and 11, not 11 and 12 (`receipts/probe6-seven-owed.txt`).
  - No test starts from seven owed.
  - The error is conservative, but it is a wrong figure in the port contract, the CHANGELOG and the PR body. So it is not RESIDUE.
- **Suggestions:** S8 (the RV32 smoke step, declined as optional; acceptable) and S9 (name both restart paths in the "discovery restarts" qualifier; acceptable as stated).
- **No RESIDUE is open.** All four round 3 wording items are fixed at this head.

## Reconstruction (in the required order)

1. Repository guidance and docs:
   - `CONTRIBUTING.md` (there is no `AGENTS.md`) and the README.
   - The docs the delta touches: PORTING "ACMP owed bound" (`docs/PORTING.md:74-116`) and its counter row (`:348`), REQUIREMENTS ACMP-12 (prose and row), `requirements.json`, VERIFICATION, TESTS, TRACEABILITY and CHANGELOG.
2. Issue #26:
   - The body and the frozen acceptance are unchanged.
   - Since round 3 the only comments are the author's `[A750e] TAKEN` and `REVIEW READY a0a3211` markers. No maintainer or manager comment narrows the scope.
   - The manager's round 2 ruling (option 2) stands as implemented at round 3.
3. PR #28 at this head is open, not draft, with base `main`. I read the whole body, and the "Round 4", "Both reviews' scripts at this head" and "Gates at this head" sections in detail. The review-start comment is 6727433119. The PR still relates to #26 and does not close it.
4. Authorities, as the repository cites them:
   - ACMP-12, ACMP-09 and PORT-01.
   - IEEE 1722.1-2021 8.2.4 and 8.2.5, Tables 8-1 and 8-3.
   - Milan v1.2 5.5.3.5 (with .3, .10, .16, .23, .30, .31 and .36) and Table 5.26.
5. `git diff 70936b77..a0a3211` for context, and `git diff b7a5988..a0a3211` in detail: 10 files, +791/-51.
   - Docs: CHANGELOG, PORTING, REQUIREMENTS, `requirements.json`, TESTS, TRACEABILITY and VERIFICATION.
   - Scripts and tests: `check_port_contracts.py`, `mutations.json` (+15 plants) and `test_acmp.cpp` (+10 tests, 2 changed assertions).
   - History: three commits, each with a one-line message, no body and a single parent. None is signed (`%G?` = N). `b7a5988` is an ancestor, so nothing was rebased. There are no submodules.
6. Public evidence: milan-fpga `4d36d7babae801c0aace6514689c4c82e8ba9ba5`, tip of `tsn26-review-evidence`, commit "Add #28 round 4 author receipts at a0a3211". I checked `review-evidence/tsn26-r1/author-r4` and `MANIFEST.json` (`receipts/evidence-check.txt`):
   - All 64 `author-r4` files and the manifest were fetched by blob id, and every git blob hash was checked.
   - Each file matches its `published_sha256`. No file is unlisted or missing. One file, `HANDOFF.md`, is `path_redacted`.
   - **The evidence commit is unsigned** (GitHub verification: "unsigned"), and the tree holds no detached signature. Integrity therefore rests on the manifest sha256 values and the git blob ids, not on a signature.
7. Hosted checks at the exact head (`receipts/hosted-summary.txt`):
   - Push run 42508553993 and pull_request run 42508558883 both executed `quality` and `bare-metal`. All 7 steps of each job concluded success, and no context was skipped.
   - The pull_request run's `quality-evidence` artifact:
     - `gates.json` is 28/28 rc 0.
     - Mutation is `{"CAUGHT": 441, "ESCAPED": 0, "ERROR": 0}`, and my five plants are CAUGHT.
     - `src/acmp.c` coverage is 813/813 lines and 424/424 branches.
   - Its `rv32-evidence` artifact has Debug and Release rc 0.

## Brief checks (1)-(5)

### Check 1: the derivation and the tests that assert it

**Claim:** PORTING:102-111 derives the answer pass of every kept command, `ACMP_OWED_MAX` + 1 + f + r, and the egress-hold budget for the deepest backlog. Two tests assert the whole bound and the budget pass by pass, and the drain test asserts the kept-behind answers at passes 11 and 12 by sequence ID.

**Result: holds as an upper bound. As an exact pass, it holds only when eight frames are owed at the egress's return (F4).**

The code backs every premise:
- `acmp_poll` sends only `owed[owed_head]` and frees one slot per accepted call (`src/acmp.c:1254-1272`).
- A command is declined only at 8 owed, or at 7 for a BIND_RX (`:1086`, `:1098-1101`). So the set never empties while a command is kept.
- `bind()` always owes its response and a PROBE_TX (`:873-875`).
- A same-talker rebind (`:852-858`), a BIND_RX for an unknown sink, and every other command owe one frame. A foreign frame owes none.
- The only sends outside commands are timer probes (`:807`, `:811`). They are held or lost, never owed ahead (`:778-804`).

So a frame's pass is n + 1 + f + r, where n (7 or 8) is the number of frames owed when the egress returns.

The budget follows, and it is conservative when n = 7:
- The hold plus (9 + f + r) × p must stay within 200 ms.
- With f ≤ 2(Q − 1), that gives a hold of 193 − 2Q ms: 191 ms for one kept command and 189 ms for two.

The tests:
- `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem` (`tests/test_acmp.cpp:3318`) keeps nine frames of every kind. It asserts each answer at `ACMP_OWED_MAX` + 1 + f by sequence ID, then the held probes one per pass in sink order.
- `KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout` (`:3369`) runs five backlogs at a hold of 200 − (9 + f). The last answer comes at exactly 200 ms, and every other within it.
- The drain test's `behind` case (`:3017-3025`) asserts `at − released == ACMP_OWED_MAX + 1 + 2 + i`. That is passes 11 and 12, for sequence IDs 0x7A09 and 0x7A0A.
- All of them start from `fill()`, which leaves eight owed.

My probe from seven owed gives passes 8, 10 and 11 against the stated 9, 11 and 12, with `probes_lost` 0. Its eight-owed control gives 9, 11 and 12.

### Check 2: the hold behaviours are pinned, and my round 3 plants fail

**Claim:** each hold behaviour that R793-3 F4 named is pinned by a named test. Every plant I wrote in round 3 is registered and fails at this head when re-run with my own scripts.

**Result: holds.**

Named tests for each behaviour:
- **Refused poll:** `RefusedPollLeavesTheBindWaitingAndItsHold` (`:3180`). It runs both with and without redelivery in the refused pass.
- **A BIND_RX declined at 8 owed holds no probe:** `BindDeclinedBehindTheFullSetHoldsNoProbe` (`:3125`). The retry is lost and counted, and its TMR_NO_RESP runs.
- **Only timer probes are held:** `OnlyTimerProbesAreHeldBesideTheWaitingBind` (`:3147`). The PRB_W_RESP2 TMR_NO_RESP, TMR_RETRY and TMR_NO_TK each take their transition beside a waiting BIND_RX, with `probes_held` 0.
- **A new binding clears `probe_held`:** `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces` (`:3230`). The converse is pinned by `SameTalkerRebindKeepsTheHeldProbe` (`:3256`).

My five plants, run by my `scripts/escape_check4.py` on an exported head tree (`receipts/escape-check4.txt`), map one to one, by old and new text, to registered plants:

| My plant | Registered plant |
|---|---|
| `reviewer-bind-wait-at-full` | `owed-bind-wait-set-at-full` |
| `reviewer-hold-every-timer` | `owed-hold-widened-to-every-timer` |
| `reviewer-hold-second-no-resp` | `owed-hold-widened-to-second-no-resp` |
| `reviewer-hold-at-seven` | `owed-hold-at-seven` |
| `reviewer-scan-skips-last-sink` | `owed-hold-scan-skips-the-last-sink` |

- Each plant fails the full 123-test ACMP binary.
- Every registered (test, needle) kill was SEEN in the failing test's output.
- The first three still pass all 113 older tests, so the round 4 tests are what catch them.
- My local campaign (`receipts/gates/mutation-summary.txt`) and the hosted campaign show all five CAUGHT among 441/441.

### Check 3: ACMP-12's new scope words

**Claim:** "and no other expiry" and "waits for the next accepted owed frame" match the code.

**Result: holds.**
- `bind_waiting` is set only for a listener BIND_RX declined with `owed_count < ACMP_OWED_MAX` (`:1099-1101`).
- Only an accepting `acmp_poll` clears it (`:1268`). So "waits for the next accepted owed frame" is exact, and a refused poll leaves it set.
- Only two expiries are held: `ACMP_TIMER_DELAY`, and `ACMP_TIMER_NO_RESP` in `ACMP_PRB_W_RESP` (`:798`). Every other expiry falls through to its Milan transition (`:813-824`), so "no other expiry" is exact.
- After `bind_waiting` clears, the existing "never lose a held probe" clause (`:783-791`) keeps held probes held while the set is full.
- The text is identical in REQUIREMENTS and `requirements.json`, and the prose adds the per-frame delay.

### Check 4: the wording residue

**Claim:** in PORTING, the counter row, CHANGELOG and the PR body:
- `probes_held` is counted once per pass held;
- a held probe "waits at most" its bound;
- a held probe is cancelled only when its sink stops probing;
- the 1 ms re-arm is the next pass only for passes at least 1 ms apart.

**Result: holds.**
- PORTING:91: "Each held probe increments `probes_held` once for each pass it is held".
- PORTING:108: "waits at most from the pass it falls due…" and "These counts assume passes at least 1 ms apart."
- PORTING:88: "retried at the first timer service 1 ms or more later, which is the next pass for a port whose passes are at least 1 ms apart".
- PORTING:93: "never dropped for want of a slot; it is cancelled only when its sink stops probing".
- The counter row (`:348`): "one for each held probe in each pass it is held … cancelled only when its sink stops probing".
- CHANGELOG: "re-armed 1 ms on" replaces "for the next pass".
- PR body: Round 4 item 3, and the round 3 wording is corrected in place.
- The renamed test message "each held probe counts once for each pass it is held" (`:3043`) is re-registered as its needle in `mutations.json`.
- `check_port_contracts.py` pins each new phrase, and its self-test refuses 61 meaning-removal controls (`receipts/gates/port-contracts.log`).

### Check 5: the declined RV32 step and the untested restart condition

**Question:** are the declined optional RV32 TMR_RETRY step and the untested discovery-restart condition acceptable as stated?

**Result: acceptable (S8, S9).**
- **RV32 step:**
  - Under the three boundary plants, both smoke ELFs exit 0 in Debug and Release in my run (`receipts/rv32-boundary-plants.txt`), as the PR body says.
  - The core is the same C source on both targets, and the boundary is target-independent control flow. Host tests and the 441-plant gate pin it.
  - My round 3 report asked for this step only "optionally".
- **Discovery restart:**
  - The qualifier narrows an "at most one per sink" claim. It adds no behaviour that needs a test, and the restart path is round 1 code.
  - See S9 for one clarity point.

## Lens results

### Conformance: CLEAN

- **The 200 ms budget.** The answer-time budget in PORTING (Milan v1.2 Table 5.26, IEEE 1722.1-2021 Table 8-1) is a sufficient condition in every case (check 1).
  - Round 3's underestimate is closed: a command kept behind the first could miss 200 ms at the stated 191 ms margin. The budget now scales with f, and the budget test asserts it for five backlogs.
  - F4 overstates the pass by one, which only makes the budget conservative. So F4 is not attributed to this lens.
- **The hold's scope.** The hold covers exactly the frame-sending expiries: TMR_DELAY (5.5.3.5.10) and the first TMR_NO_RESP (5.5.3.5.16).
  - TMR_RETRY (5.5.3.5.30/31), the PRB_W_RESP2 TMR_NO_RESP (5.5.3.5.23) and TMR_NO_TK (5.5.3.5.36) keep their deadlines.
  - This is now pinned (check 2) and stated in ACMP-12 and PORTING:89.
- **Unchanged since round 3:** the answering duty (IEEE 1722.1-2021 8.2.4 and 8.2.5) and the decline rule.
- **Limit:** no standards PDFs were available. Clause numbers were checked against the repository's own usage.

### RTL (C core, both targets): CLEAN

This repository has no HDL, so the lens was applied to the C core and both build targets.

- The delta changes no file under `src`, `include` or `examples`. The round 3 verdict on state, termination and cost stands.
- **RV32 at the exact head, on a clean clone:**
  - My `scripts/baremetal.py` run gives Debug and Release rc 0, and both smoke logs end "ADP, ACMP and MAAP smoke checks: rc 0".
  - The Release ELF sha256 `f1fd4b902e73676c…` (50504 bytes) and the Release `acmp.c` object are byte-identical to the author's `final-rv32-results.json` and to round 3.
  - The Debug ELF differs only by build path (`receipts/rv32-reproduction.txt`).
- **PR body image figures:** 50504 bytes, `.text` 38668, `acmp.o` text 19365, and Debug 150332 at equal-length paths. All match `author-r4/receipts/sizes-and-images.txt`.
- **Hosted:** RV32 Debug and Release rc 0. As in earlier rounds, the hosted ELFs differ from local ones because of the toolchain.

### Robustness: CLEAN

- No code changed. The flag lifecycle and the bounded stalled-egress behaviour, both verified in round 3, are unchanged.
- The stalled-egress behaviour is now stated at PORTING:92 (my round 3 S6).
- The new tests pin two lifecycle claims I had verified only by reading:
  - a refused poll keeps `bind_waiting` set (`:3180`);
  - a rebind to another talker clears `probe_held`, while a same-talker rebind keeps it (`:3230`, `:3256`).

### Tests: UNCLEAN (F4)

- **The ten new tests are precise.** Each failure message is a registered needle, and each of the 15 new plants is killed by a named assertion.
  - My escape check confirms this for my five plants.
  - The author's `escape-final.txt` gives it for all 60 owed-bound plants: each fails at least one test and passes once its killers are excluded. I spot-checked that receipt; I did not re-run it.
- **Coverage:** the ratchet stays at 813/813 lines and 424/424 branches, with no new exclusion.
- **Plant count:** VERIFICATION's "437 core plants and four generated" matches `mutations.json` (441). My local campaign gives 441 CAUGHT, 0 ESCAPED, 0 ERROR.
- **Changed assertions:** the drain test's kept-behind case now asserts passes by sequence ID, and the `probes_held` message was reworded together with its needle.
- **Gap (F4):**
  - The derivation's exact pass is asserted only from eight owed.
  - The second reachable start has no test: seven owed, with a BIND_RX first among the kept frames.
  - So the PR body's claim that every core sentence of the owed-bound section is pinned holds only for n = 8.

### Docs: UNCLEAN (F4)

- **F4:** PORTING:105 and :107 state an exact pass that is one too high when the egress returns with seven owed. The CHANGELOG entry and the PR body (Round 4 item 1) repeat it.
- **The rest of the delta is accurate:**
  - the decline and redelivery additions (PORTING:80-86);
  - the hold's scope (:88-89);
  - the held probe's wait (:90-94, :108);
  - the budget (:109-111);
  - the gated-port note (:112);
  - ACMP-12 (prose, row and JSON);
  - VERIFICATION's plant count;
  - the regenerated TESTS and TRACEABILITY rows (the hosted and local `traceability` and `test-inventory` gates pass).
- **Round 3 wording:** R2-R4 and R793-3's RES6 are all fixed (check 4).
- **Comment rule:** I scanned all 734 added lines under `src`, `include`, `tests`, `examples` and `scripts` (`receipts/comment-scan.txt`).
  - Every added comment is a `REQ:` tag or a clause citation.
  - There is no lane label, lane name, review round, reviewer ID or issue-comment ID.
  - Reviewer plant names appear only in the PR body, which may name lanes. The registered names are neutral (`owed-…`).

## Findings

### F4: MINOR (Docs, Tests). The stated pass is one too high when the egress returns with seven frames owed, and no test starts there

The stated figure is "leaves in pass `ACMP_OWED_MAX` + 1 + f + r".

**Where:**
- `docs/PORTING.md:105`: "…therefore leaves in pass `ACMP_OWED_MAX` + 1 + f + r…".
- `docs/PORTING.md:107`: "So the first kept command, a BIND_RX included, leaves in pass `ACMP_OWED_MAX` + 1 after the egress returns when no poll is refused…".
- `CHANGELOG.md:6`: "derives the answer pass of every kept command, `ACMP_OWED_MAX` + 1 + f + r".
- PR body, Round 4 item 1: "So a kept command leaves in pass `ACMP_OWED_MAX` + 1 + f + r", and the corrected Round 3 "Result" sentence.
- `scripts/check_port_contracts.py` pins the PORTING:105 phrase as CRITICAL.

**Evidence:**
- **The premise allows seven owed.** PORTING:103 says "a command is declined only with seven or eight frames owed".
- **When seven are owed, the first declined command is a BIND_RX** (`src/acmp.c:1098-1101` sets `bind_waiting`).
  - This happens whenever a stall leaves seven owed. One example: five frames owed and a BIND_RX taken, then a second BIND_RX arrives.
  - At seven owed, the hold keeps the set at seven. Probes are held, other commands are kept behind, and foreign frames owe nothing.
- **The derivation fixes n at eight.** Each frame's pass is n + 1 + f + r, where n is the number of frames owed when the egress returns. The text writes `ACMP_OWED_MAX` for n.
- **Probe results** (`scripts/probe_owed6.inc`, `receipts/probe6-seven-owed.txt`): a 187 ms hold, which is the stated budget for Q = 3, then a kept BIND_RX and two kept GET_RX_STATE. Stated passes are in parentheses.

  | Start | BIND_RX pass (stated) | GET behind (stated) | 2nd GET behind (stated) | `probes_lost` |
  |---|---|---|---|---|
  | eight owed (control) | 9 (9) | 11 (11) | 12 (12) | 0 |
  | seven GET_RX_STATE owed | **8** (9) | **10** (11) | **11** (12) | 0 |
  | five owed plus a taken BIND_RX | **8** (9) | **10** (11) | **11** (12) | 0 |

- **No test covers this start.** `fill()` always leaves eight owed. `AnsweredOnlyBindAlsoWaitsForTwoSlots` (`:3105`) builds seven owed, but it checks only the decline, not the pass.
- **The gap has been latent since round 3.** Round 3's sentence ("a BIND_RX included … in pass `ACMP_OWED_MAX` + 1") had the same gap. I missed it then because all my round 3 probes started from a full set.

**Impact:**
- The error is conservative. A port that budgets by the stated formula meets every timeout.
- But the port contract presents an exact pass, and this round's purpose was to derive that pass exactly and pin every sentence. The figure is wrong in a reachable case, and the sentence map's "pinned" claim covers only n = 8.
- A figure claim changes, so the owner's RESIDUE definition does not apply.

**Required outcome:** fix the docs in either form (a) or (b), then make the matching changes in all three places listed after them.

- **(a) Exact form.**
  - PORTING:105: "…therefore leaves in pass n + 1 + f + r, where n, `ACMP_OWED_MAX` or one less, is the number of frames owed when the egress returns (one less only when the first kept frame is a BIND_RX declined with one slot free), f counts…".
  - PORTING:107: "…leaves in pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set) after the egress returns…".
- **(b) Bound form.** Keep the figure, and add one sentence after PORTING:105: "With seven frames owed when the egress returns, which happens only when the first kept frame is a BIND_RX declined with one slot free, each leaves one pass sooner."
- **In either form:**
  - The budget sentences need no change.
  - Make the CHANGELOG and the PR body (Round 4 item 1) say the same.
  - Add a seven-owed start, to `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem` or a sibling test, that asserts pass `ACMP_OWED_MAX` + f for each kept command. Kill it with a registered plant, for example one that makes the seven-owed BIND_RX wait an extra pass. `scripts/probe_owed6.inc` (MIT) is a ready starting point on the existing fixture.

**Verification:**
- `scripts/run_probes3.sh HEAD_TREE WORK OUT scripts/probe_owed6.inc 'AcmpOwedProbe6.*'` prints the passes to compare with the new text.
- The new assertion fails under its plant and passes at the head. The hosted campaign catches the plant by its needle.
- The `port-contracts` gate passes with any re-pinned phrase.

### S8: SUGGESTION (Tests, RTL). The RV32 smoke still does not step through the hold's boundaries

- **Status:** the author declined this step as optional (PR body, "Both reviews' scripts"). `receipts/rv32-boundary-plants.txt` confirms it: under `owed-hold-widened-to-every-timer`, `owed-hold-widened-to-second-no-resp` and `owed-bind-wait-set-at-full`, both smoke ELFs exit 0.
- **Why that is acceptable:** the same C source is pinned on the host by named assertions and by the gate's campaign. The boundary has no target-specific code.
- **Optional, for target parity:** add one smoke step to `acmp_owed_smoke`. It would fire a TMR_RETRY beside a waiting BIND_RX and check that the state leaves PRB_W_RETRY with `probes_held` unchanged. That step would catch the first two plants on RV32.

### S9: SUGGESTION (Docs). Name both restart paths in "while no sink's discovery restarts"

- **Where:** PORTING:108 and :112.
- **Two paths can make a sink owe a second probe inside one wait.** My round 3 S7 named both:
  - an ADP re-advertisement that does not raise the available index (`src/acmp.c:672-678`);
  - `acmp_tk_unregistered` (`:1237`), which re-probes from SETTLED_RSV_OK through `reprobe()`.
- **Why that matters:** the second path is an SRP loss, not a discovery event, so a reader may not count it as a "discovery restart".
- **Suggested wording:** "while no sink's probing restarts (an ADP re-advertisement that does not raise the available index, or `acmp_tk_unregistered`)".
- **Acceptable as stated:** the qualifier only narrows an "at most" claim and needs no test.

## Prior findings at this head

My own items, resolved from my own packets. The concurrent review's round 3 items are in the next section, which was written after my verdict and ledger.

| Item | Status at a0a3211 | Basis |
|---|---|---|
| R794-3 **F3** MINOR (Tests): the hold's scope boundary was unpinned, and three boundary plants escaped every target | **Resolved** | Check 2. All five of my round 3 plants are registered and caught by named needles, locally and on the hosted runs; the three escapers are caught only by the new tests. The RV32 part was optional (S8). |
| R794-3 **R2** RESIDUE: `probes_held` counts each held probe per pass | **Resolved** | PORTING:91, the counter row and the PR body (check 4) |
| R794-3 **R3** RESIDUE: "next pass" assumes passes at least 1 ms apart | **Resolved** | PORTING:88 and :108 (check 4) |
| R794-3 **R4** RESIDUE: "never dropped" omitted cancellation | **Resolved** | PORTING:93 and the counter row (check 4) |
| R794-3 **S6**: stalled egress | **Taken** | PORTING:92 |
| R794-3 **S7**: one per sink absent a restart | **Taken** | PORTING:108 and :112. See S9 for a clarity point. |
| R794-3 concurrence with R793-3 **F3**: the budget covered only the first kept command | **Resolved for the timeout; see F4 for the exact pass** | Check 1. The pass now scales with f, and the budget is restated and tested pass by pass for five backlogs. The underestimate that could miss 200 ms is gone. F4 is a new, conservative gap in the new text: the exact pass is one too high from seven owed. |
| R794-1 and R794-2 items | **Remain resolved** | The code and docs paths are unchanged; see my round 3 report. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-12 (MD and JSON); PORTING:74-116 against `src/acmp.c:293-335, 721-825, 848-879, 1063-1104, 1254-1272`; the hold's scope against Milan 5.5.3.5.10/.16/.23/.30/.31/.36; the budget arithmetic; the seven-owed probe | R794-4 (delta); unchanged code from R794-1 to R794-3 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| RTL (C core, both targets) | CLEAN | Empty core delta; `baremetal.py` on a clean clone (Debug and Release rc 0; Release ELF and `acmp.o` byte-identical to the author's); the PR body's image figures; hosted RV32 rc 0 | R794-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Robustness | CLEAN | Flag lifecycle (unchanged) with the new refused-poll and rebind tests; stalled-egress wording | R794-4 (delta); R794-3 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Tests | UNCLEAN (F4) | 10 new tests and 2 changed assertions; `mutations.json` (+15, 441 in all); my 5 plants run by my own script (all caught, 3 only by the new tests); local campaign 441/0/0; hosted campaign 441/0/0; coverage 813/813 and 424/424; RV32 smoke under 3 boundary plants; the author's escape and sentence-map receipts (spot-checked) | R794-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Docs | UNCLEAN (F4) | PORTING, REQUIREMENTS, `requirements.json`, VERIFICATION, TESTS, TRACEABILITY and CHANGELOG deltas; the counter row; `check_port_contracts.py` phrases (61 controls); the PR body (Round 4 and after); comment-rule scan of 734 added lines; commit messages | R794-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |

## Concurrent review R793-3 at b7a5988 (read after my verdict and ledger)

- **Source:** the published report `reviews/R793-3/REPORT.md` (blob `cb241e2f…`, hash checked) in the same evidence tree. PR comment 6722039867 carries the same verdict.
- **What changed after reading:** nothing in my verdict, findings or ledger. This section was added afterwards.
- **What I did not read:** the concurrent review of this round (R793-4).

| Its item | Status at a0a3211 | Basis |
|---|---|---|
| **F3** MINOR (Docs, Robustness): the budget covered only the first kept command | **Resolved** | (a) PORTING:102-111 now gives the pass `ACMP_OWED_MAX` + 1 + f + r and "Budget the egress hold for the deepest backlog the port keeps". (b) The PR body's Round 3 "Result" sentence now reads exactly as F3's text proposes. (c) The `behind` case asserts passes 11 and 12 (`tests/test_acmp.cpp:3024-3025`), and the derivation is pinned in `CRITICAL`. The 202 ms miss is gone, and the budget test asserts 200 ms exactly for five backlogs. My F4 is a separate, conservative gap in the new figure: it is one pass too high from seven owed. F3's own sentence "it leaves in pass `ACMP_OWED_MAX` + 1 + *f*" has the same gap. |
| **F4** MINOR (Tests): five stated behaviours of the hold were unpinned | **Resolved** | (1) `RefusedPollLeavesTheBindWaitingAndItsHold` covers it: its `again = false` arm redelivers only after accepting polls, a retry falls due in the refused pass, and no probe leaves ahead of the BIND_RX answer. (2) `BindDeclinedBehindTheFullSetHoldsNoProbe`. (3) `OnlyTimerProbesAreHeldBesideTheWaitingBind` covers the RESP2 timeout, TMR_RETRY and TMR_NO_TK. (4) `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces`. Its five escaping plants are registered as `owed-bind-wait-cleared-by-refused-poll`, `owed-bind-wait-set-at-full`, `owed-hold-widened-to-second-no-resp`, `owed-hold-widened-to-every-timer` and `owed-rebind-keeps-the-hold`. All are CAUGHT in my local campaign and in the hosted one, and so are its three controls (`receipts/gates/mutation-summary.txt`). I did not re-run its own scripts; the author's `reviewer-scripts/` receipts report them run unchanged. |
| **S5** (Docs): "next pass" holds only for passes of at least 1 ms | **Taken** | PORTING:88 and :108 (same as my R3) |
| **S6** (Robustness, Docs): a held probe has no fixed wait while the port keeps commands | **Taken** | PORTING:92: "While the port keeps commands or no owed frame is accepted, a held probe keeps waiting…" |
| **RES5**: `probes_held` undercount wording | **Resolved** | PORTING:91 and the counter row (same as my R2) |
| **RES6**: "waits from" should read "waits at most from" | **Resolved** | PORTING:108 "waits at most from the pass it falls due…" |

## Real limits

- **No standards PDFs** were available. Clause numbers and titles were judged from the repository's citations.
- **Gate kit on a clean clone of the exact head** (`receipts/gates/`):
  - I ran `python3 scripts/validate.py --jobs 8` without `--graphs`, because the host has no Mermaid CLI.
  - 25 of the 26 gates that ran pass. Graphs did not run here; it passes in the hosted run.
  - The one failure is `clang-sanitizers-build` (rc 2), and the cause is the environment. The pinned clang 18.1.3 on this host has no sanitizer runtime and cannot parse the host's libstdc++ 16 headers (`receipts/gates/clang-sanitizers-build.errors.txt`).
  - I re-ran that arm with the host's clang 23.1.4, using `-DTSN_SANITIZERS=ON` and the gate's ASAN and UBSAN options. Configure, build and test all returned rc 0, and 8 of 8 ctest targets passed (`receipts/gates/sanitizers-host-clang23.txt`). This is not the pinned compiler.
  - The hosted run's sanitizer arm, on its own toolchain, passes.
  - The clang 18 shims I used for the other gates link the host's sanitizer runtime (`scripts/clang18_shims.sh`).
  - `scripts/run_gates.sh` records the commands; I ran them as separate steps.
- **Author evidence:** the 60-plant escape evidence and the 64-sentence map were spot-checked, not re-run.
- **Evidence commit:** it is unsigned and carries no detached signature. I checked integrity by manifest sha256 and git blob ids only.
- **S9's restart paths** come from code reading. I did not probe them.
- **No hardware:** no physical calibration or hardware was run. Field skips are not hardware proof.
- **No manager source bank:** I ran no manager source bank, parent build or parent harness, and I infer none. Hosted jobs were judged by their job and step conclusions and their two artifacts. Hosted and act acceptance are the manager's.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`. Host paths in the receipts are replaced by `<scratch>` and `<tools>`.
- **Scripts.** Set `TOOLS` to a prefix holding `gtest-1.14.0`. The RV32 scripts also need `riscv64-elf-gcc` and `qemu-system-riscv32`.
  - `scripts/fetch_evidence.sh TREE_TSV OUT`: fetches the evidence blobs by id and checks each git blob hash.
  - `scripts/escape_check4.py HEAD_TREE WORK OUT scripts/plants-r3.json`: one build, then each of my plants run with the full ACMP binary and without the 10 round 4 tests. It also matches each plant to its registered entry and checks each registered needle.
  - `scripts/run_probes3.sh HEAD_TREE WORK OUT scripts/probe_owed6.inc 'AcmpOwedProbe6.*'`: the seven-owed probe, run on a disposable copy. It uses `scripts/apply_plant.py`.
  - `scripts/rv32_plants3.sh HEAD_TREE WORK OUT JOBS PLANT...`: the RV32 gate and both smoke ELFs under registered plants.
  - `scripts/clang18_shims.sh` and `scripts/run_gates.sh`: the gate environment and commands.
- **Clone integrity** (`receipts/clone-state.txt`). All work ran on clones or exported copies; the review clone was never written.
  - HEAD, the HEAD tree and the index tree are exact.
  - There are no untracked, ignored or modified entries, and all 98 worktree blobs match the index.
  - All entries are mode 100644. No gitlinks are tracked, so no submodule gitlink applies.
  - Both gate clones are at the head and clean after their runs.

## Pending manager duties

- Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts. Hosted and act acceptance are the manager's.
- Re-review at the head that addresses F4.
- The parent PR that moves the pin still has to carry out the integration-note items: the parent killer test and needles, and re-measuring the harness row.
- Until then, #26 stays open, as the PR intends.

R794-4 FINISHED
