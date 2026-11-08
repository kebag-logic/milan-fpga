[R794] NEGATIVE - exact head 715d20804fd3438edf990c393bf1b0c6e328dede

# R794-5: external independent delta review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- **Exact head:** `715d20804fd3438edf990c393bf1b0c6e328dede`, tree `603836cfb8a32ba48a3d7a07a32410f4ad3e7f5a`.
- **Delta reviewed:** `a0a3211..715d208`, from my round 4 head (`8d6786f`, `af31233`, `7960ef7`, `715d208`).
  - `git diff --stat a0a3211 715d208 -- src include examples` is empty, so the core and the RV32 example are as at round 3. Code the delta does not touch keeps its earlier lens verdict.
  - The delta touches 10 files (+161/-18): CHANGELOG, PORTING, REQUIREMENTS, TESTS, TRACEABILITY and VERIFICATION, plus `check_port_contracts.py`, `test_inventory.py`, `mutations.json` (+2 plants) and `test_acmp.cpp` (+2 tests).
- **Verdict: NEGATIVE** on one new MINOR, F5 (Docs, Tests).
  - **What F5 is:** the held-probe wait bound at PORTING:110, and the two sentences it rests on (:92 and :94), count only commands *kept*. A command that arrives after the kept BIND_RX is taken is offered after the next accepting poll and accepted at once. It takes the freed slot ahead of the held probe, so each one adds a pass to the stated bound.
  - **Why the delta matters here:** the new redelivery obligation (:85) is what makes this the prescribed port behaviour.
  - **Probe result:** with one, three and ten such commands, the held retry is owed 1, 3 and 10 passes after the bound (`receipts/probe7-later-commands.txt`).
- **Everything the brief names holds:**
  - My round 4 **F4 is resolved**. The exact form (a) was taken in PORTING, the CHANGELOG and the PR body. The new seven-owed test asserts `ACMP_OWED_MAX` + f for each kept command. Its registered plant fails at this head with both needles seen, and passes every older test.
  - My **S9 is taken**, naming three restart paths where I suggested two.
  - The redelivery obligation and the held wait under TMR_NO_RESP match the code.
  - The RES7 cancel-by-response wording matches the code.
  - The gates pass, apart from one arm that fails for an environment reason.
- **Wording residue:** RES8 (what can be owed past TMR_NO_RESP) and RES9 (a PR-body paraphrase drops a condition). Neither affects the verdict.

## Reconstruction (in the required order)

1. **Repository guidance and docs.**
   - `CONTRIBUTING.md` (there is no `AGENTS.md`) and the README.
   - The docs the delta touches: PORTING "ACMP owed bound" (`docs/PORTING.md:74-118`) and its counter row (`:350`); REQUIREMENTS ACMP-12 (`:41-48`); TESTS, TRACEABILITY, VERIFICATION and CHANGELOG.
2. **Issue #26.**
   - The body and the frozen acceptance are unchanged.
   - Since round 4 the only new comments are the author's `[A750f] TAKEN` and `REVIEW READY 715d208` markers, and the manager's review-start comments on the PR. No maintainer or manager comment narrows the scope.
3. **PR #28 at this head.**
   - It is open, not draft, base `main`, and relates to #26 without closing it.
   - I read the whole "Round 5" section and its subsections.
   - The review-start comment is 6728289514.
4. **Authorities, as the repository cites them:**
   - ACMP-12, ACMP-09 and PORT-01;
   - IEEE 1722.1-2021 8.2.4 and 8.2.5, Tables 8-1 and 8-3;
   - Milan v1.2 5.5.3.5 (.3, .10, .16, .23, .30, .31, .36) and Table 5.26.
5. **Diffs and history.**
   - I read `git diff 70936b77..715d208` for context and `git diff a0a3211..715d208` in full.
   - History (`receipts/history.txt`): four commits. Each has a one-line message and a single parent, and none is signed (`%G?` = N). `a0a3211` is an ancestor, so nothing was rebased. There are no submodules.
6. **Public evidence:** milan-fpga `66d92076f8b141a1341f556ca920ce58a48d12c5`, the tip of `tsn26-review-evidence` ("Round 5 receipts at 715d2080").
   - All 134 `author-r5` files and `MANIFEST.json` were fetched by blob id, and each git blob hash was checked.
   - Every file matches its `published_sha256`. No file is unlisted or missing. `HANDOFF.md` is `path_redacted`, and I did not read it (`receipts/evidence-check.txt`).
   - **The evidence commit is unsigned** (GitHub: "unsigned") and has no detached signature. Integrity rests on the manifest sha256 values and the git blob ids.
7. **Hosted checks at the exact head** (`receipts/hosted-summary.txt`).
   - Pull_request run 42532139282 and push run 42532134610 both executed `quality` and `bare-metal`. Each job's 7 steps concluded success, and no context was skipped.
   - The pull_request run's `quality-evidence` artifact shows:
     - `gates.json` 28/28 rc 0;
     - mutation `{"CAUGHT": 443, "ESCAPED": 0, "ERROR": 0}`, with both new plants CAUGHT;
     - `src/acmp.c` coverage 813/813 lines and 424/424 branches.
   - Its `rv32-evidence` artifact has Debug and Release rc 0.

## Brief checks (1)-(5)

### Check 1: R793-4 F5, the port offers every waiting frame

**Result: holds as the brief states it.** F5 below is a different gap that this obligation exposes.

- **The obligation is stated.** PORTING:85: "After each `acmp_poll` that accepts an owed frame, the port offers its waiting ACMP frames in arrival order, the kept one first, until `acmp_rx` declines one or none is left, and only then services `acmp_timer_expired`."
- **It is pinned.** The three phrases are in `CRITICAL['acmp_rx']` of `check_port_contracts.py`. My `port-contracts` gate refuses all 74 meaning-removal controls.
- **The PR body says the bound assumes it** (Round 5 item 1: "The bound assumes this."), and the CHANGELOG says the same.
- **The test fixture behaves as TESTS says.** TESTS.md's new fixture sentence matches `pass()` (`tests/test_acmp.cpp:2580-2592`), which:
  - advances the clock 1 ms;
  - polls once;
  - offers held frames until `acmp_rx` returns false or none is left;
  - then services due timers.

  `pass()` did not change in this delta.
- **The "one" port of the internal probes is excluded.** A port that offers one frame per accepting poll does not offer "until `acmp_rx` declines one or none is left".
  - PORTING:89 gives that port's cost: "a timer probe owed there delays each later kept command one pass".
  - That matches the author's re-run of `probe_r4`/`probe_r4b`: one pass late behind an only-answered BIND_RX, and two passes late (pass 12, 201 ms) behind two foreign frames with two probes owed.
  - The case analysis also holds: without probes the second GET's answer stays at pass 10 behind the first, so the delay comes only from the probes owed into the slots left free.

### Check 2: R793-4 F6 and my S9, the held probe's conditions

**Result: holds. RES8 records one wording gap.**

- **The new conditions.** PORTING:110 now reads: "at most one per other sink while no sink's probing restarts (an ADP re-advertisement that does not raise the available index, a new discovery after its talker departs or its advertisement times out, or `acmp_tk_unregistered`) and the held probe has waited less than TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also be owed before it."
- **The code backs each named restart path:**
  - `disc_available` → `tk_departed` + `tk_discovered` when the index does not rise (`src/acmp.c:672-678`);
  - `disc_departing` and ADP ageing (`:686-693`, `:1187-1189`), then rediscovery through `tk_discovered` → `delay` (`:598-606`, `:666`);
  - `acmp_tk_unregistered` → `reprobe` (`:1237`).
- **The list is complete for a second probe within 200 ms.** Every other way to start a probe is the timer chain (TMR_DELAY, TMR_NO_RESP, TMR_RETRY ≥ 4 s, TMR_NO_TK 10 s) or a BIND_RX. A BIND_RX's PROBE_TX is a frame owed by a command.
  - The TMR_NO_RESP retry is armed only when a probe *leaves* (`no_resp_from_send`, `:757`). So within 200 ms of the held probe's wait, no other sink can owe a second probe without a restart.
- **The PR body says it too** (Round 5 item 3). The gated-port sentence (:114) also says "probing restarts".
- **The sustained internal probe falls within the sentence** (`author-r5/receipts/probes/probe-r4c.txt`): sink 2's TMR_DELAY probe leaves in pass 11, its retry in pass 250, then sink 3's held retry in pass 251. Sink 2's second probe comes only after 200 ms.

### Check 3: my R794-4 F4, the answer pass from seven owed

**Result: resolved.**

- **Text.**
  - PORTING:107: "leaves in pass n + 1 + f + r, where n, `ACMP_OWED_MAX` or one less, is the number of frames owed when the egress returns (one less only when the first kept frame is a BIND_RX declined with one slot free)".
  - :109: "leaves in pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set)".
  - CHANGELOG:6 and PR body Round 5 item 2 say the same. Item 1 of Round 4 is updated.
  - The budget (:112-113) keeps `ACMP_OWED_MAX` for n, which is conservative from either start.
- **"Exactly when" holds in the code.**
  - Frames are owed only by command handlers (`respond`, `:844-1028`, and `bind`'s probe, `:875`) and by timer probes (`:807`, `:811`).
  - A command is declined at 7 owed only if it is a BIND_RX (`:1098-1101`), which sets `bind_waiting`. Timer probes are then held, and later frames are not delivered before the kept one. So the set stays at 7 exactly in that case, and at 8 in every other case.
- **The test.** `KeptCommandsBehindSevenOwedLeaveOnePassSooner` (`tests/test_acmp.cpp:3398`):
  - It builds seven owed both ways: seven GET_RX_STATE, or five plus a taken BIND_RX.
  - It keeps a BIND_RX, a GET_RX_STATE and a second BIND_RX, with two refused passes, with and without redelivery.
  - It asserts each answer at `ACMP_OWED_MAX` + f (passes 8, 10 and 11), and the held retry at pass 13 with `probes_lost` 0.
- **The plant** `owed-bind-wait-only-on-a-second-decline` (`receipts/escape-check5.txt`):
  - It fails the full 125-test binary, and only in this test. Both registered needles are SEEN.
  - It passes the 123 tests that remain without the two round 5 tests, so this test is what catches it.
  - It is CAUGHT in my local campaign and in the hosted one.
- **My probe matches the text.** I re-ran `probe_owed6.inc` unchanged (`receipts/probe6-at-715d208.txt`). Its lines are identical to my round 4 receipt: 9, 11 and 12 from eight owed, and 8, 10 and 11 from seven owed both ways.
  - That is n + 1 + f with n = 8 or 7 and f = 0, 2, 3. The probe's "(stated …)" column still prints the round 4 figure, as the PR body notes.

### Check 4: RES7, cancel by response

**Result: holds.**

- **Text.**
  - PORTING:95: "it is cancelled only when its sink stops probing, as when its talker departs or a BIND_RX binds the sink to another talker, or when a held retry's earlier probe is answered".
  - :94: "until the probe is owed or cancelled".
  - The counter row (`:350`) and PR body Round 4 item 3 / Round 5 item 4 say the same.
- **Code.**
  - A matching PROBE_TX_RESPONSE reaches `sm_stop` (`:965`), which clears `probe_held` (`:355`). A held retry re-uses `probe_seq`, so the answer to its earlier probe matches.
  - A held TMR_DELAY probe has no earlier probe, and responses outside probing are ignored.
- **The test.** `AnsweredProbeEndsTheHoldOfItsRetry` (`:3457`) covers both a failure and a SUCCESS status.
  - The registered plant `owed-answer-keeps-the-hold` fails only this test, with its needle SEEN, and passes all 123 older tests.
  - My own independent plant `reviewer-response-leaves-held-retry`, which keeps the hold and the TMR_NO_RESP kind across the answer, behaves the same way: it is caught only by this test.

### Check 5: ACMP-12 and the owed-bound section against the code; gates

**ACMP-12** (`docs/REQUIREMENTS.md:41-48`; row and `requirements.json` unchanged): "While it waits with one slot free, timer probes of any sink are held, never lost …; no other expiry is held".
- This matches `:1099-1101` and `:778-804`. A BIND_RX declined at 8 holds nothing; `BindDeclinedBehindTheFullSetHoldsNoProbe` pins that.
- The CHANGELOG says the same.

**PORTING owed bound, sentence by sentence (:76-118):**
- **Holds:** the decline (:76-84), the redelivery obligation (:85-89), the hold's scope (:90-91), loss (:96), order (:97), the bound (:104-109), the budget (:111-113), the gated port (:114-115) and the counter row.
- **F5:** :92, :94 and the first clause of the :110 bound.
- **RES8:** the last clause of :110.

**Gates on clean clones of the exact head** (`receipts/gates/`, `receipts/rv32-baremetal.log`):
- **Gate kit:** `python3 scripts/validate.py --graphs --jobs 6`, run with Mermaid CLI 11.16.0, the version CI installs.
  - 26 of the 27 gates that ran return rc 0. That includes `graphs` (4 rendered) and `port-contracts` (74 controls).
  - It also includes the full mutation campaign: 443 CAUGHT, 0 ESCAPED, 0 ERROR, with both new plants and every round 3 and 4 hold plant CAUGHT (`receipts/gates/mutation-summary.txt`).
  - Coverage of `src/acmp.c` is 813/813 lines and 424/424 branches.
  - `clang-sanitizers-build` fails (rc 2), so `clang-sanitizers-test` does not run. The cause is the environment, as at round 4: the pinned clang 18.1.3 cannot parse the host's libstdc++ 16 headers (`receipts/gates/clang-sanitizers-build.errors.txt`), and no other libstdc++ is installed.
  - I re-ran that arm with the host clang 23.1.4 and the gate's ASAN and UBSAN options. Configure, build and test all return rc 0, and 8 of 8 tests pass (`receipts/sanitizers-host-clang.txt`). This is not the pinned compiler.
  - The author's receipts and the hosted run give 28/28 with the pinned arm.
- **`baremetal.py`:** Debug and Release rc 0.
  - The Release ELF (50504 bytes, sha256 `f1fd4b902e73676c…`) is byte-identical to my round 4 build and to the author's `rv32-results.json`, and so is the Release `acmp.c` object.
  - The Debug ELF differs by build path only.
- **Round 4 probes, run unchanged** (all on exported copies):
  - `probe_owed6.inc`: identical output.
  - `escape_check4.py` with `plants-r3.json` (`receipts/escape-check4-at-715d208.txt`): all five of my round 3 plants are still killed by their registered needles, and the three boundary plants still pass every test outside the round 4 additions.
  - `rv32_plants3.sh` (`receipts/rv32-boundary-plants.txt`): both smoke ELFs still exit 0 under the three boundary plants (S8, declined).

## Lens results

### Conformance: CLEAN

- **Command answers.** The 200 ms command-timeout budget (Milan v1.2 Table 5.26, IEEE 1722.1-2021 Table 8-1) is unchanged. It uses n = `ACMP_OWED_MAX`, so it is a sufficient condition from either start (check 3).
- **The hold's scope.** It is unchanged and exact: TMR_DELAY (5.5.3.5.10) and the first TMR_NO_RESP (5.5.3.5.16) only (check 5).
- **F5 is not attributed here.** It concerns how long a held probe waits behind commands, which is a design the earlier rounds accepted (commands ahead of probes). No command timeout depends on it, and no clause claim changes.
- **Limit:** no standards PDFs were available. Clause numbers were checked against the repository's own usage.

### RTL (C core, both targets): CLEAN

This repository has no HDL, so the lens was applied to the C core and both build targets.
- The core delta is empty, so the round 3 verdict on state, termination and cost stands.
- **RV32 at the exact head on a clean clone:** Debug and Release rc 0, and the Release image is byte-identical to round 4 (check 5).
- **Hosted:** RV32 Debug and Release rc 0. As before, the hosted ELFs differ because the toolchain differs.

### Robustness: CLEAN

- **No behaviour changed.**
- **The new tests pin two lifecycle facts:**
  - a matching answer ends a held retry (`:3457`);
  - a BIND_RX declined at seven holds the retry and loses nothing (`:3398`).
- **Probe 7 shows the behaviour behind F5 is sound.** Later commands delay the held retry but never lose it (`probes_lost` 0). The retry is owed in the first pass that leaves a slot free at timer service.
  - Starvation under sustained traffic is the same in kind as the sustained case the text already covers.
  - F5 is about how that behaviour is stated, so it is attributed to Docs and Tests.

### Tests: UNCLEAN (F5)

- **The two new tests are precise.** Each failure message is a registered needle, and each new plant is killed only by its new test (check 3, check 4).
- **Count and coverage.** VERIFICATION's "439 core plants and four generated" matches `mutations.json` (443). My local and the hosted campaign give 443/0/0, and the coverage ratchet is unchanged.
- **Gap (F5).** No assertion covers a held probe that waits behind commands arriving after the BIND_RX is taken. The author's sentence map pins PORTING:110 only by "one pass per probe before it" (`ProbesFallingDueInTheDrainWaitForTheDeferredBind`). So the claim "every core sentence pinned" does not reach the clause F5 corrects.

### Docs: UNCLEAN (F5)

- **F5:** PORTING:92, :94 and :110, and the PR body's Round 5 item 3 (which quotes :110) and Round 4 item 3 (which repeats :94).
- **Accurate:** the rest of the delta, which is the redelivery obligation, the n + 1 + f + r text, the restart list, the cancel-by-response wording, ACMP-12's "with one slot free", TESTS' fixture sentence, VERIFICATION's count, and the regenerated TESTS and TRACEABILITY rows (the `traceability` and `test-inventory` gates pass).
- **Residue:** RES8 and RES9.
- **Comment rule** (`receipts/comment-scan.txt`):
  - The delta adds 142 lines under `src`, `include`, `tests`, `examples` and `scripts`. Its only comments are two `// REQ: ACMP-12, ACMP-09` tags.
  - No added line carries a lane label, lane name, review round, reviewer ID or issue-comment ID.
  - Reviewer and finding names appear only in the PR body, which may name lanes.

## Findings

### F5: MINOR (Docs, Tests). The held-probe wait bound counts only kept commands, but a command offered for the first time after the BIND_RX is taken also takes the freed slot ahead of the held probe

**Where:**
- `docs/PORTING.md:92`: "…and held probes take freed slots one per pass, after the commands still kept."
- `docs/PORTING.md:94`: "While the port keeps commands or no owed frame is accepted, a held probe keeps waiting…"
- `docs/PORTING.md:110`: "A held probe therefore waits at most from the pass it falls due through the pass that takes the BIND_RX, plus one pass for each frame owed by a command kept behind the BIND_RX and for each other probe owed before it, …"
- PR body, Round 5 item 3, which quotes the :110 sentence.
- PR body, Round 4 item 3, which repeats :94 ("while the port keeps commands or nothing is accepted").
- `scripts/check_port_contracts.py` pins the :92 and :94 phrases.

**Evidence:**
- **The code.** A held probe takes a slot only at timer service: `sm_expired` holds it while `probe_yields`, that is while `bind_waiting` is set or every slot is owed with a probe held (`src/acmp.c:778-804`). A command needs only `room()` (`:1086`, `:1098`).
- **The rule.** Under the new redelivery rule (PORTING:85), after each accepting poll the port offers *every* waiting frame before timer service. A frame that reached the port's receive queue since the last pass is such a waiting frame, and it is accepted at its first offer if a slot is free. It is never declined, so it is never "kept".
- **The probe** (`scripts/probe_owed7.inc`, `receipts/probe7-later-commands.txt`). It uses the fixture of `AnsweredProbeEndsTheHoldOfItsRetry`: a full set, then a kept BIND_RX, while sink 2's TMR_NO_RESP retry falls due in the hold.
  - The BIND_RX is taken in pass 2.
  - No command is kept behind it, and no other sink probes, so the stated bound has the retry owed in pass 3.

  | Commands after the BIND_RX is taken | How they reach the core | Declined at arrival | Retry owed in pass (stated 3) | Excess passes | `probes_lost` |
  |---|---|---|---|---|---|
  | none | none | 0 | 3 | 0 | 0 |
  | 1 GET_RX_STATE | offered after the accepting poll | 0 | 4 | 1 | 0 |
  | 3 | offered after the accepting poll | 0 | 6 | 3 | 0 |
  | 10 | offered after the accepting poll | 0 | 13 | 10 | 0 |
  | 1 / 3 / 10 | delivered between passes, declined, then kept | 1 / 3 / 10 | 4 / 6 / 13 | 1 / 3 / 10 | 0 |

- **What the table shows:**
  - The per-frame cost the text states, one pass per frame, is right in both modes.
  - The second mode fits "kept behind the BIND_RX" if that phrase means "behind it in arrival order".
  - The first mode is outside the text as written, and the new rule (:85) prescribes it for every port that drains its receive queue in the pass.
  - Sentence :92 is literally false in that mode, because the freed slot goes to a command that was never kept. Sentence :94's condition is not met, because the port keeps nothing and the owed frames are accepted, yet the probe keeps waiting.
- **This gap predates this round.** These sentences stood at round 4, and I passed them then. This round's obligation at :85 makes the first mode part of the port contract, and :110 was rewritten in this delta. So the gap is in scope under check 5.

**Impact:**
- **No command timeout or loss is affected.**
- **The port contract understates the held probe's delay.** The bound is "at most" and is pinned as core. An integrator with steady controller traffic, such as periodic GET_RX_STATE, would read a shorter probe delay than the core gives.
- **A bound claim changes, not only words,** so this is not RESIDUE. The owner rule makes a doubtful case MINOR.

**Required outcome:**
- Make the three sentences count every command the core takes before the probe's timer service, not only kept ones. Suggested text:
  - :92: "…held probes take freed slots one per pass, after the commands the port still keeps or offers before its timer service."
  - :94: "While the port keeps or offers commands that take the freed slots, or no owed frame is accepted, a held probe keeps waiting…"
  - :110: "…plus one pass for each frame owed by a command the port delivers after the BIND_RX before the probe is owed, kept or not, and for each other probe owed before it, …"
- Make the PR body Round 5 item 3 and Round 4 item 3 say the same.
- Re-pin the changed phrases in `CRITICAL`.
- Pin the corrected clause with a named assertion: after the BIND_RX is taken, a GET_RX_STATE offered after the next accepting poll delays the held retry one pass. `scripts/probe_owed7.inc` (MIT), the first mode, is a ready start on the existing fixture.
- Register a plant that the assertion kills. One option is a plant that lets a held probe take the freed slot ahead of a later command.

**Verification:**
- `scripts/run_probes3.sh HEAD_TREE WORK OUT scripts/probe_owed7.inc 'AcmpOwedProbe7.*'` should show every case owed at "taken + 1 + frames of later commands".
- The new assertion should fail under its plant and pass at the head, and the hosted campaign should catch the plant by its needle.
- The `port-contracts` gate should pass with the re-pinned phrases.

### RES8: RESIDUE (Docs). "Past that" names only the retry

- **Where:** `docs/PORTING.md:110` and PR body Round 5 item 3: "past that, another sink's TMR_NO_RESP retry can also be owed before it".
- **The gap:** in a longer wait (at least TMR_NO_RESP + TMR_RETRY, 4.2 s, with traffic sustained), the same sink's new TMR_DELAY probe after TMR_RETRY (5.5.3.5.31, `src/acmp.c:819-820`) can also be owed before the held probe. So can a settled sink's re-probe after TMR_NO_TK (`:822-823`).
- **Why it is RESIDUE:** the clause states no bound past 200 ms. It only lists what may be owed, so no figure changes.
- **Exact fix:** "past that, another sink's later probes, starting with its TMR_NO_RESP retry, can also be owed before it".

### RES9: RESIDUE (Docs, PR body). The paraphrase drops "with no probe held"

- **Where:** PR body Round 5 item 4: "A BIND_RX declined with no slot free also waits, and a probe that falls due then is lost".
- **The gap:** with a probe already held and every slot owed, a probe that falls due then is held, not lost (`probe_yields`, `src/acmp.c:778-792`). PORTING:96 has the condition right, because its "so is one…" inherits "With no probe held".
- **Exact fix:** "…and a probe that falls due then, with no probe held, is lost".

### S8: SUGGESTION (Tests, RTL), retained as declined. The RV32 smoke does not step through the hold's boundaries

- This is unchanged from round 4. The author declined it again (PR body Round 5 item 5).
- Under the three boundary plants both smoke ELFs still exit 0 (`receipts/rv32-boundary-plants.txt`). The same C source is pinned on the host.
- It remains acceptable as optional.

## Prior findings at this head

My own items, resolved from my own packets. The concurrent review's items are in the next section, which I wrote after my verdict and ledger.

| Item | Status at 715d208 | Basis |
|---|---|---|
| R794-4 **F4** MINOR (Docs, Tests): the stated pass was one too high from seven owed, and no test started there | **Resolved** | Check 3. The exact form (a) is in PORTING:107/:109, CHANGELOG:6 and the PR body. `KeptCommandsBehindSevenOwedLeaveOnePassSooner` asserts `ACMP_OWED_MAX` + f. Its plant fails at the head and passes without the test. Locally and hosted it is CAUGHT. `probe_owed6` matches. |
| R794-4 **S8** (RV32 step) | **Declined; acceptable** | See S8 above |
| R794-4 **S9** (name the restart paths) | **Taken** | PORTING:110 and :114 name three paths, which is one more than I gave. The code backs each (check 2). |
| R794-3 F3, R2-R4, S6, S7 | **Remain resolved or taken** | The text is unchanged or extended consistently. The round 3 plants are still caught (`receipts/escape-check4-at-715d208.txt`). |
| R794-1 and R794-2 items | **Remain resolved** | The code and docs paths are unchanged |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-12 (MD; row and JSON unchanged); PORTING:76-118 against `src/acmp.c:293-321, 721-825, 844-1028, 1063-1104, 1172-1196, 1227-1272`; the hold's scope against Milan 5.5.3.5.10/.16/.23/.30/.31/.36; the budget with n = 7 and n = 8 | R794-5 (delta); unchanged code R794-1 to R794-4 | 715d20804fd3438edf990c393bf1b0c6e328dede |
| RTL (C core, both targets) | CLEAN | Empty core delta; `baremetal.py` on a clean clone (Debug and Release rc 0; the Release ELF and `acmp.o` byte-identical to round 4 and to the author's); hosted RV32 rc 0; RV32 smoke under 3 boundary plants | R794-5 | 715d20804fd3438edf990c393bf1b0c6e328dede |
| Robustness | CLEAN | Hold and cancel lifecycle (unchanged code) with the two new tests; probe 7 (later commands delay but never lose a held retry); the sustained internal probe receipt | R794-5 (delta); R794-3/4 | 715d20804fd3438edf990c393bf1b0c6e328dede |
| Tests | UNCLEAN (F5) | The 2 new tests; `mutations.json` (+2, 443 in all); the escape check of both new plants plus 2 independent reviewer plants (each caught only by its new test); the round 3 plant escape check re-run unchanged; local campaign 443/0/0; hosted 443/0/0; coverage 813/813 and 424/424; the author's sentence map (spot-checked rows 19, 21 and 40) | R794-5 | 715d20804fd3438edf990c393bf1b0c6e328dede |
| Docs | UNCLEAN (F5) | PORTING, REQUIREMENTS, TESTS, TRACEABILITY, VERIFICATION and CHANGELOG deltas; the counter row; `check_port_contracts.py` (13 new phrases, 74 controls); `test_inventory.py`; the PR body Round 5 section; the comment-rule scan of 142 added lines; commit messages | R794-5 | 715d20804fd3438edf990c393bf1b0c6e328dede |

## Concurrent review R793-4 at a0a3211 (read after my verdict and ledger)

- **Source:** the published report `reviews/R793-4/REPORT.md` (blob `77c6fdb9…`, git hash checked) in the same evidence tree.
  - I also fetched its three probe sources by blob id. Their sha256 values equal those in the author's `author-r5/receipts/probes/inputs.sha256`, so the author re-ran the published probes.
- **What changed after reading:** only one location was added to F5 (PR body Round 4 item 3). The verdict, the findings' severities and the ledger are unchanged.
- **What I did not read:** the concurrent review of this round (R793-5).

| Its item | Status at 715d208 | Basis |
|---|---|---|
| **F5** MINOR (Docs, Robustness): the bound assumed the port offers its whole waiting backlog after each accepting poll | **Resolved** | Check 1. Option (a) is taken word for word at PORTING:85 and pinned in `CRITICAL`. The PR body says "The bound assumes this", and TESTS states the `pass()` model. Port "one" is excluded, and :89 gives its cost, which matches the probe receipts. |
| **F6** MINOR (Docs): one per other sink also needs the wait under TMR_NO_RESP | **Resolved** | Check 2. The condition and the "past that" clause are in PORTING:110 and PR body Round 4 item 3 / Round 5 item 3, and the sustained case falls within them. RES8 is a wording extension past 4.2 s. Its sustained case uses GETs that are declined at arrival and then kept (my probe 7's second mode). My F5 is the first mode, commands accepted at their first offer, which neither its F6 nor its F5 covered. |
| **S7** (RV32 smoke step) | **Declined; acceptable** | The same as my S8 |
| **S8** (test the "one" port) | **Not taken; acceptable** | It applies only under option (b), and option (a) was chosen |
| **RES7** (cancel by response) | **Resolved** | Check 4. All three fixes are in, with a test and plant beyond what RES7 asked. |

## Real limits

- **No standards PDFs** were available. Clause numbers and titles were judged from the repository's citations.
- **Sanitizer arm.** The pinned clang 18 sanitizer build cannot run on this host (libstdc++ 16 headers), so the gate kit gives 26 of the 27 gates that ran, with `clang-sanitizers-test` not run. I re-ran the arm with the host clang 23.1.4, which passes and is not the pinned compiler. The pinned arm passes in the author's receipts and in the hosted run.
- **Author evidence was spot-checked, not re-run.** That covers the 66-sentence map, `escape-final.txt` and the author's re-runs of the internal probes. I re-ran my own probes and plants.
- **Evidence commit:** it is unsigned and has no detached signature. Integrity was checked by manifest sha256 and git blob ids only.
- **Probe 7 is a fixture model.** It models the port contract's pass in the existing test fixture, not a real port.
- **No hardware:** no physical calibration or hardware was run. Field skips are not hardware proof.
- **No manager source bank:** I ran no manager source bank, parent build or parent harness, and I infer none. Hosted jobs were judged by their job and step conclusions and their two artifacts. Hosted and act acceptance are the manager's.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`. Host paths in the receipts are replaced by `<scratch>`, `<tools>` and `<reviews>`.
- **Scripts.** Set `TOOLS` to a prefix holding `gtest-1.14.0`. The RV32 scripts also need `riscv64-elf-gcc` and `qemu-system-riscv32`.
  - `scripts/fetch_evidence.sh TREE_TSV OUT`: fetches the evidence blobs by id and checks each git blob hash.
  - `scripts/run_gates5.sh GATES_CLONE RV32_CLONE WORK TOOLS SHIMS`: starts the gate kit with `--graphs` and the RV32 gate, each with its own log and rc file. `scripts/clang18_shims.sh` builds SHIMS.
  - `scripts/escape_check5.py HEAD_TREE WORK OUT scripts/plants-r5.json`: both new registered plants and two reviewer plants, each run with the full ACMP binary and without the two round 5 tests.
  - `scripts/escape_check4.py HEAD_TREE WORK OUT scripts/plants-r3.json`: my round 4 check, unchanged.
  - `scripts/run_probes3.sh HEAD_TREE WORK OUT INC FILTER`: runs `probe_owed6.inc` (unchanged) and `probe_owed7.inc` (F5), using `scripts/apply_plant.py`.
  - `scripts/rv32_plants3.sh HEAD_TREE WORK OUT JOBS PLANT...`: the RV32 gate and both smoke ELFs under registered plants.
- **Clone integrity** (`receipts/clone-state.txt`). All work ran on clones or exported copies, and the review clone was never written.
  - HEAD, the HEAD tree and the index tree are exact.
  - There are no untracked, ignored or modified entries, and all 98 worktree blobs match the index.
  - All entries are mode 100644. No gitlinks are tracked and there is no `.gitmodules`, so no submodule gitlink applies.
  - Both gate clones are at the head with no tracked changes after their runs.

## Pending manager duties

- **Merge-turn validation.** Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts. Hosted and act acceptance are the manager's.
- **Re-review** at the head that addresses F5. Carry RES8 and RES9 to the residue checklist.
- **Parent PR.** The parent PR that moves the pin still has to carry out the integration-note items: the parent killer test and needles, and re-measuring the harness row.
- Until then, #26 stays open, as the PR intends.

R794-5 FINISHED
