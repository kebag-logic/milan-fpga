[R793] NEGATIVE - exact head a0a32110511e444a23848367b7cbb4231e16ce5a

# R793-4: independent internal review of kebag-logic/tsn-c-stack PR #28 (issue #26), delta round

- Exact head `a0a32110511e444a23848367b7cbb4231e16ce5a`, tree `fedb871bbf9996ccca390fd723105558b447349e` (checked in both clones: `receipts/clone-state.txt`).
- Previously reviewed head: `b7a5988` (R793-3, NEGATIVE on F3 and F4). Source base: `70936b77`.
- Delta since b7a5988: three author commits, `b7b2048` (derivation of the bound), `c4a2bff` (tests and plants), `a0a3211` (wording). Nothing was merged, rebased or amended. `git diff --stat b7a5988 a0a3211 -- src include examples` is empty, so code the delta does not touch keeps its R793-1/2/3 verdicts.
- Verdict: **NEGATIVE**, on two open MINOR findings.
  - R793-3 **F3 and F4 are resolved at their cause.** The derivation `ACMP_OWED_MAX` + 1 + f + r matches the code and every probe I ran with the test port model. All eight of my round-3 plants are registered with byte-identical edits, and each fails at least one of the 123 tests at this head. All 28 gates pass on a clean clone, 441/441 plants are caught, and bare-metal passes in Debug and Release.
  - **F5 (MINOR, Docs, Robustness).** The derivation assumes something the contract never asks for: that after each accepting poll the port offers all its waiting frames, in order, until one is declined. A port that meets every stated rule but offers only the oldest waiting frame per accepted poll lets a timer probe take the slot that an only-answered BIND_RX, or a frame that needs no answer, leaves free. The next kept command then leaves a pass later than the formula says. With two foreign frames in the backlog it is answered at **201 ms** at the documented 189 ms budget.
  - **F6 (MINOR, Docs).** The held-probe bound's "at most one per other sink while no sink's discovery restarts" leaves out a second case. Without any restart, a held probe can wait behind both the TMR_DELAY probe and the TMR_NO_RESP retry of one other sink once its wait passes TMR_NO_RESP. I demonstrated this by probe.

## Reconstruction order followed

1. CONTRIBUTING.md (there is no AGENTS.md), then the docs touched by the delta: PORTING (owed bound, field and counter tables), REQUIREMENTS and requirements.json (ACMP-12), TESTS, TRACEABILITY, VERIFICATION, CHANGELOG.
2. Issue #26: body and acceptance are unchanged since round 3. No maintainer or manager comment narrows the scope.
3. PR #28 body at this head (`headRefOid` = a0a3211): every section, with Round 3 and Round 4 in full.
4. Authorities, as in earlier rounds: ACMP-12 (new scope words), ACMP-03/08/09, PORT-01; IEEE 1722.1-2021 8.2.4, 8.2.5 and Tables 8-1 and 8-3; Milan v1.2 5.5.3.5 (.3, .10, .16, .23, .30, .31, .36) and Table 5.26.
5. `git diff b7a5988..a0a3211`, read in full: 10 files, +791/−51. Then the history `70936b77..a0a3211` (17 commits).
6. Public evidence: milan-fpga `4d36d7ba` (the `tsn26-review-evidence` tip), `review-evidence/tsn26-r1/author-r4`, read by section. I did not open the author-r4 receipts of the other reviewer's scripts (`reviewer-scripts/r794-*`) or the archived reviews until my verdict and ledger were written.
7. My round-3 report and scripts (`tsn26-r793-3-packet`), for F3, F4, S5, S6, RES5 and RES6.

## Answers to the focus items

### 1. The derivation (PORTING:102-111) and its two tests: correct for the test port model; it rests on one unstated port obligation (F5)

- **Code basis.**
  - Each accepting `acmp_poll` sends the oldest owed frame. A command is declined only at 8 owed, or at 7 for a BIND_RX (`src/acmp.c:1099-1103`), so the set never empties while one is kept.
  - Timer service sees either a full set or `bind_waiting` set. `probe_yields` (`:778-792`) then holds every TMR_DELAY expiry and every PRB_W_RESP TMR_NO_RESP (`:797-803`).
  - So for a port that offers its whole waiting backlog before timer service, the kept frames leave in FIFO order, one per pass, after the eight owed frames. The answer pass is `ACMP_OWED_MAX` + 1 + f + r, as PORTING:105 states.
  - The owes rule (two frames for a binding BIND_RX; one for any other command, an only-answered BIND_RX included; none for a frame with no answer) matches `bind()` (`:860-878`) and the unknown-sink and same-talker paths.
- **Budget arithmetic.** hold + (9 + f) × 1 ms ≤ 200 with f ≤ 2(Q − 1) gives hold ≤ 193 − 2Q: 191 ms for Q = 1 and 189 ms for Q = 2. The PR's figures are correct.
- **Tests.**
  - `KeptCommandsLeaveOnePassPerFrameOwedAheadOfThem` (`tests/test_acmp.cpp:3318`) asserts each of eight answers at exactly 9 + f: 9, 11, 12, 13, 14, 15, 16 and 18. That covers every kept kind, including an unknown-sink BIND_RX, a same-talker rebind and a foreign frame that owes nothing. Held probes follow the last kept frame one per pass, in sink order, none lost.
  - `KeptBacklogWithinTheDocumentedBudgetMeetsItsTimeout` (`:3369`) runs five backlogs at hold = 200 − (9 + f). The last answer leaves at exactly 200 ms and the others within it.
  - The round-3 drain test's `behind = 2` case now asserts the kept answers by sequence ID (0x7A09 and 0x7A0A) at passes 11 and 12 (`:3018-3027`).
- **Reviewer probes** (`receipts/probes/probe-r3-head.txt`): my round-3 probes, unchanged, give the same values at this head. The mixed backlog leaves in passes 9, 11, 12, 14 and 15, each 9 + f. Two GET_RX_STATE at a 191 ms hold leave at 200 and 201 ms. A BIND_RX and then a GET_RX_STATE at 191 ms leave at 200 and 202 ms; that is now outside the documented 189 ms budget for two commands, so it is consistent.
- **Unstated obligation (F5).** Every one of these results uses a port that offers its waiting frames in order until one is declined (`pass()`, `tests/test_acmp.cpp:2580-2592`). The contract does not require that; see F5.

### 2. Each hold behaviour of R793-3 F4 is pinned, and every round-3 plant is registered and fails

| R793-3 F4 item | Test | Registered plant (edit identical to mine) | My plant on the full 123-test binary |
|---|---|---|---|
| (1) refused poll, literal port (redelivers only after accepting polls) | `RefusedPollLeavesTheBindWaitingAndItsHold` (`:3180`), `again = false` and `true` | `owed-bind-wait-cleared-by-refused-poll` | `rv-bind-wait-cleared-by-every-poll` fails 1 |
| (2) BIND_RX declined at 8 owed holds no probe | `BindDeclinedBehindTheFullSetHoldsNoProbe` (`:3125`) | `owed-bind-wait-set-at-full` | `rv-bind-wait-set-when-full` fails 1 |
| (3) only timer probes held: PRB_W_RESP2 timeout, TMR_RETRY, TMR_NO_TK at their deadlines | `OnlyTimerProbesAreHeldBesideTheWaitingBind` (`:3147`) | `owed-hold-widened-to-second-no-resp`, `owed-hold-widened-to-every-timer` | `rv-hold-widened-to-the-timeout` fails 1, `rv-hold-widened-to-every-timer` fails 1 |
| (4) a new binding clears `probe_held` | `BindToAnotherTalkerEndsTheHoldOfTheProbeItReplaces` (`:3230`); counterpart `SameTalkerRebindKeepsTheHeldProbe` (`:3256`) | `owed-rebind-keeps-the-hold` | `rv-bind-unsets-no-hold` fails 1 |
| controls | (several) | `owed-probe-held-never-set`, `owed-hold-scan-skips-the-last-sink`, `owed-hold-whenever-full` | fail 7, 5 and 4 |

- My script `run_reviewer_plants.sh`, unchanged from round 3 (`receipts/reviewer-plants.txt`, `.json`), builds each `rv-` plant with the repository's `mutation.py` and runs its ACMP binary on all 123 tests. All eight fail at least one test. At round 3, five of them passed 113/113. The driver's own CAUGHT/ESCAPED line refers to the placeholder killer the script assigns, not to the suite.
- In my full campaign, all eight registered `owed-` equivalents are CAUGHT (`receipts/registered-reviewer-plants-caught.txt`).
- The refused-poll test asserts what my round-3 probe showed, now with the literal port: `bind_waiting` stays set, the retry is held with deadline now + 1, the BIND_RX is at position 8 in pass 10 = 9 + r, and the retry leaves after the binding's frames. My round-3 refused-poll probe gives the same values (`probe-r3-head.txt`, `refused_poll`).

### 3. ACMP-12's new scope words match the code

- "while a BIND_RX declined with one slot free waits for the next accepted owed frame": the flag is set at `:1101` only when `owed_count` < `ACMP_OWED_MAX`, so with exactly one slot free there. It is cleared only at `:1268`, inside the accepting branch of `acmp_poll`. A refused poll leaves it set (pinned by `RefusedPoll…`).
- "hold each timer probe, and no other expiry": `probes` (`:797`) is true only for TMR_DELAY and for TMR_NO_RESP in PRB_W_RESP. Those are the only two expiries that send a PROBE_TX (`:806-812`). TMR_NO_RESP in PRB_W_RESP2, TMR_RETRY and TMR_NO_TK take their 5.5.3.5.23/.30/.31/.36 transitions at the deadline (`:813-825`; pinned by `OnlyTimerProbes…`).
- The only probe sent outside a timer expiry is the first PROBE_TX of `bind()` (`:875`). It is counted in the BIND_RX's two slots. `reprobe` and `tk_discovered` arm TMR_DELAY rather than probing (`:583-606`).
- "never lose a held probe": the continuation (full set plus any `probe_held`) is at `:783-790`. The requirements.json text is identical to the REQUIREMENTS row.

### 4. Wording residue: RES5, RES6, S5 and S6 taken; one new residue (RES7)

- RES5: PORTING:91 now reads "Each held probe increments `probes_held` once for each pass it is held". The counter row (`:348`) reads "one for each held probe in each pass it is held". The PR body (summary, Round 3 and Round 4) says the same. My all-in-pass-one probe still gives 119, and the drain test asserts the per-probe sum.
- RES6: PORTING:108 reads "waits at most". The PR Round 3 bullet says the same.
- S5: PORTING:88 reads "retried at the first timer service 1 ms or more later, which is the next pass for a port whose passes are at least 1 ms apart". PORTING:108 adds "These counts assume passes at least 1 ms apart". The PR body says the same. Both phrases are pinned.
- S6: PORTING:92 reads "While the port keeps commands or no owed frame is accepted, a held probe keeps waiting … its sink's probing does not advance until the probe is owed". This matches my `SustainedCommandsBehind` probe: `probes_held` 85, `probes_lost` 0, left in pass 52.
- The CHANGELOG now names the derived answer pass and the budget. It does not restate the counting, and does not need to.
- **New, RES7:** "it is cancelled only when its sink stops probing" (PORTING:93, the counter row and PR Round 4 item 3) misses one case. A held TMR_NO_RESP retry is also cancelled when the probe it repeats is answered with a failure status, and the sink then goes on probing. Probe `failure-response` (`receipts/probes/probe-r4c-held-bound-and-cancel.txt`): `probe_held` goes 1 → 0, the state is PRB_W_RETRY, `probing` is ACTIVE and the timer is TMR_RETRY. This follows `probe_response` → `sm_stop` (`:965`). The behaviour is correct; only the sentence is incomplete.

### 5. The declined RV32 TMR_RETRY step and the untested discovery-restart condition

- **RV32 step, declined: acceptable.**
  - The core is target-independent C, and its Release RV32 image is byte-identical to round 3: `f1fd4b90…`, 50504 B, the same as the author's receipt (`receipts/baremetal-compare.txt`).
  - Smoke checks 102-109 already step through the hold. The boundary plants are killed on the host suite, which is the gate of record for behaviour.
  - Adding the step stays optional (S7).
- **Discovery-restart condition: acceptable as a stated precondition, but incomplete (F6).**
  - A restart re-arms TMR_DELAY (`reprobe`, `tk_discovered`) and can give a sink a second probe. Excluding it is sound, and no test is needed for an excluded case.
  - But the cap of one probe per other sink also fails without a restart. A sink whose TMR_DELAY probe was owed before the held probe owes its TMR_NO_RESP retry 200 ms after that probe leaves (`:806-812`).
  - PORTING:92 lets a held probe wait as long as the port keeps commands, so the wait can exceed 200 ms. Demonstrated in F6.
  - For the gated port (PORTING:112), the waiting command must leave within 200 ms anyway, so one per sink holds there whenever the command meets its timeout. F6 asks only for the held-probe sentence to change.

## Findings

### F5: MINOR (Docs, Robustness). The derived bound assumes the port offers its whole waiting backlog after each accepting poll; the contract does not say so, and a port that keeps every stated rule misses 200 ms at the documented budget

- **Where:**
  - `docs/PORTING.md:84-85`: "the port keeps it and delivers it again after each `acmp_poll` that accepts an owed frame, at once and before it services `acmp_timer_expired`. This is the redelivery rule the bound below assumes."
  - `:95`: "Deliver no later ACMP frame before a kept one".
  - `:104`: "Each slot an accepted poll frees goes to the oldest kept command, and no timer probe is owed ahead of a kept command".
  - `:105`, `:111`: the pass formula and the 193 − 2 × Q budget.
  - PR body, Round 4 item 1, says the same.
- **Evidence** (`scripts/probe_r4.cpp`, `probe_r4b.cpp`; `receipts/probes/probe-r4-one-frame-per-poll.txt`). There are two ports, each with 1 ms passes and one poll per pass. Each delivers its declined frame again after every accepting poll, before timer service, and never offers a later frame before a kept one. "all" offers its waiting frames in order until one is declined; that is the test model. "one" offers only the oldest waiting frame per accepting poll.

  | Backlog behind the full set, retries due | Port "all" | Port "one" |
  |---|---|---|
  | unknown-sink BIND_RX, GET_RX_STATE; retry due in pass 1 | GET in pass 10 (formula 10), retry after it | GET in pass **11**, retry owed **ahead** of it (position 9 against 10) |
  | same-talker rebind, GET_RX_STATE; retry in pass 1 | pass 10 | pass **11**, retry ahead |
  | GET, foreign, foreign, GET at **189 ms** (budget for Q = 2); retries in passes 2 and 3 | 199 ms | **201 ms** (pass 12; two retries owed ahead) |
  | unknown-sink BIND_RX, GET at hold 200 − (9 + f) = 190 ms | 200 ms | **201 ms** |

  - Cause: an only-answered BIND_RX is taken at 6 owed and owes one frame, and a foreign frame, probe response or malformed frame owes none. Each leaves a slot free at timer service. With `bind_waiting` clear and nothing held, `probe_yields` returns false at 7 owed (`src/acmp.c:783-785`), so a due probe is owed ahead of the next waiting command.
  - Port "all" fills that slot with the next waiting command before timer service. Port "one" does not.
  - ACMP is multicast, so frames addressed to other entities arrive at every entity. Foreign frames in a backlog are ordinary.
- **Impact:**
  - "No timer probe is owed ahead of a kept command", the f + r formula and the 193 − 2 × Q budget hold only for a port that offers its waiting frames until one is declined. A port with a single retry slot that reads further frames from its receive ring only later, after timer service, also falls outside them. Nothing in the contract rules out either port.
  - An integrator who follows PORTING literally, budgets 189 ms for two kept commands and receives foreign ACMP traffic during the hold misses the Milan v1.2 Table 5.26 timeout.
  - The core behaves as the contract says. The defect is the contract's timing claim, as with R793-3 F3, so this is not RESIDUE.
  - It is not a regression of round 4: the same port at round 3 had the same exposure. But round 4 newly states the whole bound "for every kept command", and this is that bound's missing assumption.
- **Required outcome** (either option):
  - (a) Preferred: state the obligation in the redelivery rule. For example, after PORTING:84: "After each `acmp_poll` that accepts an owed frame, the port offers its waiting ACMP frames in arrival order, the kept one first, until `acmp_rx` declines one or none is left, and only then services `acmp_timer_expired`." Pin "until `acmp_rx` declines one or none is left" in `CRITICAL`. In the PR body, Round 4 item 1, say that the bound assumes this.
  - (b) Or keep the rule and widen the bound: "a port that offers one waiting frame per accepting poll adds one pass for each only-answered BIND_RX and each frame that needs no answer ahead of the command while timer probes fall due; budget them."
  - Recommended for either: the test model already is a port of the "all" kind. State in the fixture comment, or in a TESTS sentence, that `pass()` offers every waiting frame until one is declined, so that the test and the contract say the same thing.
- **Verification:**
  - `python3 scripts/validate.py --work <w> --jobs 16 --graphs` gives 28/28, with port-contracts refusing the new phrase's meaning-removal control.
  - `cat scripts/probe_r4.cpp scripts/probe_r4b.cpp > <f>`, then `scripts/run_probe.sh <clone> <dir> HEAD <f> 'AcmpOwed.R4Probe*'`: after (a), the PR and PORTING exclude port "one". After (b), its passes match the widened bound.

### F6: MINOR (Docs). "At most one per other sink while no sink's discovery restarts" also needs the wait to stay under TMR_NO_RESP

- **Where:** `docs/PORTING.md:108`: "A held probe therefore waits at most from the pass it falls due through the pass that takes the BIND_RX, plus one pass for each frame owed by a command kept behind the BIND_RX and for each other probe owed before it, at most one per other sink while no sink's discovery restarts." The same clause is in the PR body, Round 4 item 3 ("the one-per-sink counts hold while no sink's discovery restarts").
- **Evidence** (`scripts/probe_r4c.cpp`, `receipts/probes/probe-r4c-held-bound-and-cancel.txt`, case `sustained`):
  - Setup: sink 2's TMR_DELAY expiry and sink 3's TMR_NO_RESP retry fall due beside a deferred BIND_RX. Sink 2's delay draw is moved to 200 ms, inside the 0-1000 ms range a draw may take.
  - Sink 2's first PROBE_TX is owed and leaves in pass 11. Then one GET_RX_STATE arrives after every pass, up to pass 239. Each is kept and delivered first, so sink 3 stays held, as PORTING:92 allows.
  - Sink 2's TMR_NO_RESP retry falls due 200 ms after its probe left. It is held too, and leaves in pass 250, ahead of sink 3's in pass 251.
  - So sink 3 waited behind two probes of sink 2, and no discovery restarted.
  - Code: a TMR_DELAY expiry sends the first probe and arms TMR_NO_RESP from its send (`:806-808`). That retry is another timer probe (`:809-812`).
- **Impact:**
  - The per-sink cap is false once a held probe waits longer than TMR_NO_RESP, which PORTING:92 permits.
  - No Milan deadline depends on the held probe's wait: its own TMR_NO_RESP runs from when it leaves, and no command answer is affected. So the impact is low.
  - But this is a stated bound and the brief's open condition, so by the owner's rule it is MINOR, not RESIDUE.
- **Required outcome:** in PORTING:108, change the clause to, for example, "at most one per other sink while no sink's discovery restarts and the held probe has waited less than TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also be owed before it". Carry the same condition into the PR body, Round 4 item 3. PORTING:112 (gated port) may keep its clause, since there the waiting command leaves within 200 ms.
- **Verification:**
  - validate.py gives 28/28 (port-contracts keeps "These counts assume passes at least 1 ms apart" and the other pins).
  - `probe_r4c.cpp` `sustained` falls within the corrected sentence.

### SUGGESTION

- **S7 (RTL, Tests).** The RV32 smoke still makes the three external boundary plants exit 0. As in focus 5, this is acceptable. An optional smoke step, a TMR_RETRY expiry beside a waiting BIND_RX that runs at its deadline, would make the RV32 target kill `owed-hold-widened-to-every-timer` too.
- **S8 (Tests).** Once F5 is settled, a case that runs the "one" port, asserting the extra pass or that the PR excludes the port, would keep the contract and the model in step. This is only worth adding if option (b) is chosen.

### RESIDUE (wording only, carried to the residue checklist)

- **RES7 (`docs/PORTING.md:93`, counter row `:348`, PR body Round 4 item 3).** "it is cancelled only when its sink stops probing" leaves out the cancel by a response. Each fix keeps the pinned phrase:
  - PORTING:93 → "A held probe is never dropped for want of a slot; it is cancelled only when its sink stops probing, as when its talker departs or a BIND_RX binds the sink to another talker, or when a held retry's earlier probe is answered."
  - Counter row → "… it is cancelled only when its sink stops probing, or when a held retry's earlier probe is answered."
  - PR body item 3 → "… and is cancelled only when its sink stops probing or, for a retry, when the probe it repeats is answered".

Comment rule: the delta's new source comments (`tests/test_acmp.cpp`, `scripts/check_port_contracts.py`) carry only requirement and clause IDs (`// REQ: ACMP-12, ACMP-09`, `// Milan v1.2 5.5.3.5.3`). A scan of every added line in `tests`, `scripts`, `docs` and `tests/mutations.json` finds no bench lane label, lane name, review round, reviewer ID or issue-comment ID, and the comments gate passes. The three commit subjects are single lines with no body, and the privacy gate passes over 31 commits. Neither raises any RESIDUE.

## Prior public review findings at this head

| Finding | Source | Status at a0a3211 | Evidence |
|---|---|---|---|
| F3 MINOR (Docs, Robustness): the budget covers only the first kept command | R793-3 | **Resolved at its cause** | (a) PORTING:102-111 derive 9 + f + r, the owes rule and the deepest-backlog budget. (b) The Round 3 "Result" sentence now reads as I asked. (c) The `behind` case asserts passes 11 and 12 by sequence ID, and 8 phrases are pinned under `ACMP_OWED_MAX`/`probes_held`. Two new tests assert the whole bound and the budget. My probes agree. F5 is the bound's remaining unstated assumption, not a recurrence of F3. |
| F4 MINOR (Tests): five hold behaviours unpinned; plants escaped | R793-3 | **Resolved at its cause** | Items (1)-(4) are each pinned by a named test (focus 2). All eight of my plants are registered with identical edits, CAUGHT in my campaign, and failing at least one of 123 tests with my unchanged script. |
| S5 SUGGESTION: the 1 ms re-arm and sub-ms passes | R793-3 | **Taken** | PORTING:88 and :108, PR body. |
| S6 SUGGESTION: say that a held probe keeps waiting | R793-3 | **Taken** | PORTING:92. F6 follows from this sentence. |
| RES5: `probes_held` counting | R793-3 | **Resolved** | PORTING:91, :348, PR body. |
| RES6: "waits at most" | R793-3 | **Resolved** | PORTING:108, PR body. |

### Other reviewer's round-3 findings (R794-3 at b7a5988, read after this verdict and ledger were written)

| Finding | Status at a0a3211 | Evidence |
|---|---|---|
| F3 MINOR (Tests): the hold's scope boundary is unpinned (three one-line plants) | **Resolved at its cause** | `OnlyTimerProbesAreHeldBesideTheWaitingBind` and `BindDeclinedBehindTheFullSetHoldsNoProbe` assert the transitions and the loss. Its three plants have the same edits as my `rv-hold-widened-to-every-timer`, `rv-hold-widened-to-the-timeout` and `rv-bind-wait-set-when-full`. They are registered as `owed-hold-widened-to-every-timer`, `owed-hold-widened-to-second-no-resp` and `owed-bind-wait-set-at-full`, and all are CAUGHT in my campaign. Its optional RV32 smoke case was declined; I find that acceptable (focus 5, S7). |
| R2 RESIDUE: `probes_held` counts per probe per pass | **Resolved** | Same as my RES5. The test message and its registered needle changed together ("each held probe counts once for each pass it is held", `tests/test_acmp.cpp:3043`, `tests/mutations.json:2544`). |
| R3 RESIDUE: "next pass" assumes passes at least 1 ms apart | **Resolved** | PORTING:88 and :108 use its exact wording. |
| R4 RESIDUE: "never dropped" omits cancellation | **Resolved as written.** My RES7 adds one missed case. | PORTING:93 and :348 now say "never dropped for want of a slot; it is cancelled only when its sink stops probing". A held retry is also cancelled when its earlier probe is answered with a failure status, and its sink keeps probing (RES7). |
| S6 SUGGESTION: say what the hold does while the egress stays stalled | **Taken** | PORTING:92. |
| S7 SUGGESTION: "at most one per sink" holds absent a discovery restart | **Taken; incomplete (my F6)** | PORTING:108 and :112 add the restart condition. Its premise, that a sink's TMR_NO_RESP starts only when its probe leaves, is right. But a held probe may wait longer than 200 ms after another sink's probe left, and then that sink's retry is owed before it too (F6). |

Its note on my RES6 shows the slot an only-answered BIND_RX leaves free after its take. That is the slot F5 turns on: a port that offers all its waiting frames fills it with the next one, and a port that offers one frame per poll lets a probe take it. Nothing in R794-3 changes my verdict, findings or ledger.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | No core change. ACMP-12's new words match the code (focus 3). The hold delays only the two PROBE_TX-sending expiries, and the PRB_W_RESP2 timeout, TMR_RETRY and TMR_NO_TK keep their Milan v1.2 5.5.3.5.23/.30/.31/.36 deadlines (`OnlyTimerProbes…`). Every kept command is answered with its specified response, never an error status (IEEE 1722.1-2021 8.2.4/8.2.5, Table 8-3), and within 200 ms at the budget for the model port. F5 is a port-contract timing statement, not core behaviour. |
| RTL | CLEAN | No HDL in the delta, so Verilator was not used. Applied to the bare-metal RV32 target: `baremetal.py` rc 0 in Debug and Release on a clean clone, and the Release ELF `f1fd4b90…` (50504 B) and its `acmp.o` are byte-identical to round 3 and to the author's receipt. The declined smoke step is acceptable (S7). |
| Robustness | UNCLEAN (F5) | The core is unchanged (memory and instruction counts as at R793-3). In every round-3 probe case the hold loses no probe and leaves no stale flag, unchanged at this head. The new probes find one port behaviour the bound does not cover (F5). The held-retry cancel on a failure response is correct (RES7 is wording). |
| Tests | CLEAN | 441/441 plants CAUGHT. Fifteen new plants and eleven re-anchored ones are present, with test-inventory, registration and sensitivity gates passing. My eight round-3 plants fail at this head. The new tests assert the bound pass by pass and by sequence ID. Coverage of `src/acmp.c` is 813/813 lines and 424/424 branches. F5 is a port obligation, which a core test cannot enforce; S8 is optional. |
| Docs | UNCLEAN (F5, F6) | PORTING owed bound, field and counter tables, ACMP-12 (REQUIREMENTS and requirements.json), TESTS, TRACEABILITY, VERIFICATION (437 + 4 plants), CHANGELOG, `check_port_contracts.py` (16 new pins, 61 meaning-removal controls refused) and the PR body (all sections) were checked against code, tests and probes. F5 and F6 are bound statements. RES7 is wording only. |

## Executed evidence (this review, exact head unless stated)

Pinned tool root: GoogleTest 1.14.0, clang-tidy 18 and the clang-18 lexer (`scripts/env.sh`; set `TOOLS`). Host GCC and Clang were used for the GCC and sanitizer arms, and riscv64-elf-gcc with QEMU for RV32.
- Clean clone at a0a3211 (`scratch/clean`), with tree, index and blobs verified. `scripts/run_gates.sh` runs validate.py (12 jobs) and baremetal.py (4 jobs) concurrently.
  - validate: **28/28 rc 0** (`receipts/gates/validate.out`, `validate.rc`, `logs/`, `mutation-results.json`). Mutation is 441 CAUGHT / 0 ESCAPED / 0 ERROR. Port contracts refuse 61 meaning-removal controls. Privacy covers 31 commits, 359 historical blobs and 98 files. Registration finds 446 instances, and sensitivity counts 172 declarations and 441 plants.
  - bare-metal: rc 0 in Debug and Release (`receipts/gates/baremetal.out`, `receipts/baremetal-compare.txt`). The Debug ELF size depends on the build path and was not compared.
- Reviewer plants: `scripts/run_reviewer_plants.sh` with `reviewer_plants.json`, unchanged from round 3 (`receipts/reviewer-plants.{txt,json}`). Registered equivalents: `receipts/registered-reviewer-plants-caught.txt`.
- Probes, each inserted into an exported copy by `scripts/run_probe.sh`:
  - round-3 `probe_r3.cpp` + `probe_intermittent.cpp` (`receipts/probes/probe-r3-head.txt`) and `probe_timer_ahead.cpp` (`run_probe_timer_ahead.sh`, `probe-timer-ahead-head.txt`), all unchanged and matching round 3;
  - new `probe_r4.cpp` + `probe_r4b.cpp` (F5, `probe-r4-one-frame-per-poll.txt`) and `probe_r4c.cpp` (F6 and RES7, `probe-r4c-held-bound-and-cancel.txt`).
- Author evidence: milan-fpga `4d36d7ba`. All 64 `author-r4` entries of `MANIFEST.json` hash-match, and no file is unlisted (`receipts/author-evidence-check.txt`). `final-gates.json` (28 rc 0, head a0a3211), `final-mutation.log` (441 CAUGHT) and `final-baremetal.log` agree with my runs.
- Hosted CI at the exact head, inspected only (`receipts/hosted-checks.txt`, `hosted-steps.txt`): push run `42508553993` and PR run `42508558883` both succeeded. In each, the quality and bare-metal jobs ran 7 steps, all successful, none skipped. Hosted and act acceptance belong to the manager.
- Clones restored and verified (`receipts/clone-state.txt`). In both, HEAD, index tree and worktree equal `fedb871b…`. All 98 files re-hash to their HEAD blobs and have mode 100644. No gitlinks or `.gitmodules` are required or present. The ignored `scripts/__pycache__/` was removed, leaving 0 untracked or ignored entries. All probes, plants and builds ran in exported copies under `scratch/`.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ACMP-12 text (REQUIREMENTS, requirements.json) against `src/acmp.c` `probe_yields`, `sm_expired`, `acmp_rx` decline, `acmp_poll`, `bind`, `probe_response`; Milan v1.2 5.5.3.5 transitions and Table 5.26 timing in the new tests | R793-4 (delta). Untouched code keeps its R793-1/2/3 verdict | a0a32110511e444a23848367b7cbb4231e16ce5a |
| RTL | CLEAN | `baremetal.py` Debug and Release on a clean clone, Release ELF and `acmp.o` against round 3 and the author, `examples/rv32/smoke.c` hold checks, declined smoke step | R793-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Robustness | UNCLEAN (F5) | derivation against code; 12 round-3 probe cases, 5 round-2 cases, 12 new port-variant cases, sustained hold over 250 passes, failure-response cancel | R793-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Tests | CLEAN | `tests/test_acmp.cpp` (10 new tests, drain test change, fixture helpers), `tests/mutations.json` (15 new, 11 re-anchored), full campaign, my 8 plants on 123 tests, coverage, test inventory | R793-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |
| Docs | UNCLEAN (F5, F6) | PORTING, REQUIREMENTS, requirements.json, TESTS, TRACEABILITY, VERIFICATION, CHANGELOG, `check_port_contracts.py`, PR body (all sections), comment-rule scan | R793-4 | a0a32110511e444a23848367b7cbb4231e16ce5a |

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not available. Clause content was judged from the repository's citations, the code's clause tags and the cited table contents.
- The probes use the committed port model and two variants: one offering one frame per accepted poll, and one with a delay draw moved within its range. No real port, receive ring or network was run.
- The evidence commit `4d36d7ba` has no cryptographic signature (`%G?` = N). Its integrity rests on the MANIFEST.json hashes, which I verified, and on the public branch tip.
- The sanitizer arm and coverage ran with host compilers. CI's Ubuntu 24.04 arms are covered by the hosted run, not by this review.
- Debug ELF bytes depend on the build path and were not compared.
- The parent harness row still needs the parent PR. Issue #26 stays open by design ("Relates to").
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- No manager source bank runs at this head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus this review's own runs.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base 70936b77 against live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c; builder and native banks), and link those receipts on the PR.
- Own hosted and act acceptance. Both runs at the exact head showed success at inspection.
- Route F5 and F6 to the author. After the fixes, obtain two independent positive reviews at the new head.
- Carry RES7 to the residue checklist, and S7 and S8 as optional.
- Track the parent PR. It must bind the ready hook to `acmp_rx_ready` (or keep declined frames), change the parent mutant fragments named in the PR integration note, and then measure the harness row.

R793-4 FINISHED
