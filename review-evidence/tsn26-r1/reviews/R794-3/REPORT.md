[R794] NEGATIVE - exact head b7a59887f5f2ff729206b87a268972c637882dc0

# R794-3: external independent delta review of kebag-logic/tsn-c-stack PR #28 (issue #26)

- **Exact head:** `b7a59887f5f2ff729206b87a268972c637882dc0`, tree `2b5baf1864dd923531f98b9af9255b7e75ad2435`.
- **Delta reviewed:** `968a164..b7a5988` (my round 2 head to this head: `8a1cb08`, `d355236`, `b7a5988`). Code the delta does not touch keeps its round 2 lens verdict unless the delta changes what it depends on.
- **Verdict:** NEGATIVE on one MINOR of my own (F3, Tests), plus, after reading, the concurrent review's F3 (MINOR, Docs and Conformance), which I concur with.
  - The manager's ruling (R794-2 option 2) is implemented correctly. My unchanged round 2 probes, which falsified the old pass count, now pass: whatever timer probes fall due, the deferred BIND_RX is answered in pass `ACMP_OWED_MAX` + 1, with `probes_lost` 0, and the 191 ms margin now leaves at 200 ms.
  - Commands the port keeps behind the BIND_RX leave after its answer and probe and before any held probe. Each leaves one pass later per frame owed ahead of it, **not** by pass `ACMP_OWED_MAX` + 1.
  - My own open item (F3): the new tests pin that timer probes **are** held. Nothing pins the scope boundary of the hold that ACMP-12 and PORTING now state, namely only the two timer probes, and only for a BIND_RX declined with one slot free. Three one-line regressions of that boundary pass every ctest target and the RV32 smoke in Debug and Release.
- **Correction, disclosed:** my first draft of this report, written before I read any other review, said the BIND_RX "and everything behind it" are answered in pass `ACMP_OWED_MAX` + 1. That was wrong. I corrected it after reading the concurrent R793-3 report and verifying its F3 with my own probe (`receipts/probe5-kept-behind.txt`). See "Concurrent review R793-3". No other finding or lens judgement in my independent pass was changed. The ledger shows the two lenses that move by concurrence.
- **Residue and suggestions:** three RESIDUE items (R2-R4) and two SUGGESTIONs (S6, S7), listed below with exact fixes.

## Reconstruction (in the required order)

1. `CONTRIBUTING.md` (there is no `AGENTS.md`). Docs read: PORTING "ACMP owed bound" (`docs/PORTING.md:74-104`) and the storage and counter tables, ARCHITECTURE, REQUIREMENTS ACMP-12, `requirements.json`, TESTS, TRACEABILITY, VERIFICATION and CHANGELOG.
2. Issue #26:
   - Body and acceptance are unchanged.
   - The comments since round 2 are only the author's `[A750d] TAKEN` and `REVIEW READY b7a5988` markers. No maintainer or manager comment narrows the scope.
   - The manager's ruling (option 2) is as the review brief states. It is implemented as PR body "Round 3" item 1.
3. PR #28 body at this head (all sections) and the review-start comment 6721871894. The PR still says it relates to #26 and does not close it.
4. Authorities, as cited in the repository:
   - ACMP-12, ACMP-09, ACMP-03, ACMP-08 and PORT-01.
   - IEEE 1722.1-2021 8.2.4 and 8.2.5, Tables 8-1 and 8-3.
   - Milan v1.2 5.5.3.5, 5.5.3.5.3, .10, .16, .23, .30 and .36, and Tables 5.26, 5.32 and 5.47.
5. `git diff 70936b77..b7a5988`, and in detail `git diff 968a164..b7a5988`: 15 files, +513/-38. History: three commits, each a one-line message with no body and a single parent. Nothing was rebased (`968a164` is an ancestor).
6. Public evidence: milan-fpga `28625428926b0b015367793495a25884818b488d` (tip of `tsn26-review-evidence`, commit "Round 3 receipts at b7a5988"), `review-evidence/tsn26-r1/author-r3` and `MANIFEST.json` (`receipts/evidence-check.txt`):
   - All 64 `author-r3` files and the manifest were fetched by blob id, and every git blob hash was checked.
   - Each file matches its `published_sha256`, with no unlisted or missing file. 7 files are declared `path_redacted`.
   - The evidence commit is **not signed** (GitHub: "unsigned"). There is no detached signature in the packet. Integrity therefore rests on the manifest sha256 values and git blob ids, not on a signature.
7. Hosted checks at the exact head (`receipts/hosted-summary.txt`):
   - The push run 42481173198 and the pull_request run 42481176344 both executed `quality` and `bare-metal`. All 7 steps of each job concluded success, and no context was skipped.
   - The pull_request run's `quality-evidence` artifact has `gates.json` 28/28 rc 0 (including `privacy`, `mutation` and `graphs`), mutation `{"CAUGHT": 426, "ESCAPED": 0, "ERROR": 0}`, and coverage `src/acmp.c` 813/813 lines and 424/424 branches.
   - Its `rv32-evidence` has Debug and Release rc 0.

## Brief checks (1)-(6)

| # | Claim | Result | Evidence |
|---|---|---|---|
| 1 | The kept BIND_RX and every frame behind it are answered by pass `ACMP_OWED_MAX` + 1 with `probes_lost` 0; my probes are run unchanged; the 191 ms margin now leaves at 200 ms | **Holds for the kept BIND_RX; does not hold for frames kept behind it** (corrected after reading; see "Concurrent review R793-3", F3). Each frame kept behind leaves one pass later per frame owed ahead of it: at the 191 ms hold, 202 and 203 ms behind a BIND_RX (`receipts/probe5-kept-behind.txt`). No timer probe is owed ahead of any of them. | `receipts/probe2-unchanged-at-head.txt`, my round 2 `probe_owed2.inc` byte-identical (sha256 checked). With 0, 1, 4 or 14 retries falling due one per pass, the BIND_RX is answered in pass 9, at position 8, with `probes_lost_delta` 0, `busy_declined` 2, and every probe sent (2, 5 and 15). Round 2 gave passes 10, 13 and 23. Margin: 191 ms hold with one retry gives 200 ms, `within_200=1` (round 2: 201 ms). Only those four BIND_RX lines differ from my round 2 receipt; the GET_RX_STATE lines, unknown-sink trade-off lines and hold sweep are unchanged. In-tree, `ProbesFallingDueInTheDrainWaitForTheDeferredBind` (`tests/test_acmp.cpp:2952`) adds two kept GET_RX_STATEs behind the BIND_RX and checks each answer comes after the BIND_RX frames and before any held probe. |
| 2 | The held probe's own bound as PORTING states it (`docs/PORTING.md:88`) | **Holds** (for 1 ms passes; see R3) | Code: a held probe is re-armed `now + 1` (`src/acmp.c:800`). While `bind_waiting` or (full and any probe held) it is held again (`:778-792`). The pass that takes the BIND_RX leaves 8 owed with a held flag set, so the probe is owed one pass later, after each kept frame and each earlier-scanned probe. The test asserts `owed_in[j] == taken_in + 1 + behind + j` and `probes_held == Σ(owed_in − due_in)` for five cases, including two commands kept behind. All pass at this head (hosted and my runs). |
| 3 | The hold ends once nothing is held; after that, a probe that finds the queue full is lost and counted | **Holds** | `HoldEndsWithTheLastHeldProbe` (`tests/test_acmp.cpp:3027`). `probe_held` is cleared only in `sm_stop` (`src/acmp.c:355`) and `sink_reset`. I checked every exit from a held state: `probe_response`, `tk_departed`, `bind`, `unbind`, `acmp_tk_registered`, rollback and restore all pass through `sm_stop` or `sink_reset`. No `sm_timer` call reaches a sink with `probe_held` set, so the flag cannot go stale. `bind_waiting` is cleared by every accepting `acmp_poll` (`:1268`). |
| 4 | Nine new plants, each escaping without the three new tests; RV32 smoke steps 102-109 catch seven | **Holds** | `receipts/escape-check.txt`: unplanted 113/113. Each of the nine fails only round 3 tests, and passes all 110 others once those three are excluded. `receipts/rv32-plant-exit-codes.txt`: seven exit 104/105/106 in both Debug and Release. `owed-hold-skips-delay` and `owed-held-flag-kept` exit 0, as disclosed. This is identical to the author's `rv32-plant-exit-codes.txt`. Hosted full campaign: 426/426 CAUGHT by named needles. **But see F3** for three boundary regressions that nothing catches. |
| 5 | Disclosed limit: a port that only tests `acmp_rx_ready` never has a frame declined, so the hold cannot help it; budget `ACMP_OWED_MAX` + 1 + `n_sinks` passes | **Holds** (see S7 for the "one per sink" premise) | `receipts/probe4-gated-port.txt` (gated port model, 16 sinks): GET_RX_STATE and BIND_RX are answered in pass 9 + e for e = 0, 1, 4 and 14 retries (pass 23 with 14), within the budget of 25. `busy_declined`, `probes_held` and `probes_lost` are all 0, so the hold never engages. Stated at `docs/PORTING.md:100-101` and in the PR integration note. |
| 6 | `struct acmp` +8 bytes; cost table; R793-2 S3/S4/RES1-RES4 and R794-2 R1/S4/S5 handled; 12 new CRITICAL phrases | **Holds** | Sizes (`receipts/struct-sizes.txt`, compile-time asserts on both targets): `struct acmp` 5064→5072 on RV32 and 5072→5080 on x86-64; `acmp_sink` 256 and the owed set 640 are unchanged. Cost: my rebuild of the published `measure/r3/measure.c` at this head (`-DLANE`, rv32i -O3 and rv32im -Os) gives result files, `acmp.o` sizes and ELF sha256 byte-identical to `author-r3/measure/final-*` (`receipts/cost-reproduction.txt`). Every PR-body cost row matches `start-*`/`final-*`; `acmp.o` -Os is 10605 → 10789. Prior items: see "Prior findings at this head". CRITICAL: `check_port_contracts.py` adds 2 (`acmp_rx_ready`) + 4 (`bind_waiting`) + 6 (`probes_held`) = 12 phrases, each present in PORTING. The hosted `port-contracts` gate passes. |

## Lens results

### Conformance: CLEAN in my independent pass; UNCLEAN by concurrence with R793-3 F3 (read after the verdict)

- The 200 ms Table 5.26 budget PORTING gives (hold + `ACMP_OWED_MAX` + 1 passes) covers only the first kept command. See "Concurrent review R793-3".
- The ruling's property now holds: no timer probe is owed ahead of a kept command, so the 200 ms Table 5.26 budget for a deferred BIND_RX rests on the documented pass count again (checks 1 and 2).
- The hold covers exactly the frame-sending expiries: TMR_DELAY (5.5.3.5.10) and the first TMR_NO_RESP in PRB_W_RESP (5.5.3.5.16), at `src/acmp.c:798`.
  - The non-sending expiries keep their timing at this head, as my boundary probes show (`receipts/probe3-boundary-head.txt`): TMR_RETRY (5.5.3.5.30/31), the second TMR_NO_RESP (5.5.3.5.23) and TMR_NO_TK (5.5.3.5.36). (F3 is that nothing keeps it so.)
  - A held NO_RESP still accepts a late PROBE_TX_RESPONSE in PRB_W_RESP (`:956-965`), as Milan allows.
- A held probe keeps its sequence ID and its response window. TMR_NO_RESP starts only when the probe leaves (`:736-741`, `probe_left`).
- The answering duty (IEEE 1722.1-2021 8.2.4/8.2.5; Table 8-3 has no full-queue status) is unchanged from round 2.
- Limit: no standards PDFs were available. Clause numbers were checked against the repository's own usage.

### RTL (C core, both targets): CLEAN

This repository has no HDL. The lens was applied to the C core and both build targets.

- **New state:** `bind_waiting` and `probe_held` fill padding, and `probes_held` adds 4 bytes plus 4 of tail padding (sizes above).
- **Termination:** a held expiry returns with its deadline one ms on, so the `while (sm_running && due)` loop in `acmp_timer_expired` (`src/acmp.c:1191`) terminates. `rearm()` asks the port for the new deadline through `finish()`.
- **Cost:** `probe_yields` is O(`n_sinks`) only when the set is full. The cost rows reproduce byte for byte.
- **Targets at the exact head:**
  - My `scripts/baremetal.py` run: Debug and Release rc 0, and both smoke logs end "ADP, ACMP and MAAP smoke checks: rc 0".
  - The Release ELF sha256 `f1fd4b902e73676c…` (50504 bytes) is identical to the author's `final-rv32-results.json` and `sizes-and-images.txt`. The Debug ELF differs only by build path (`receipts/rv32-reproduction.txt`).
  - Hosted: 28/28 and RV32 rc 0. The hosted ELFs differ from local ones because of the toolchain, as in earlier rounds.

### Robustness: CLEAN

- The hold cannot livelock: each held probe re-checks once per ms, and every accepting poll clears `bind_waiting`.
- The flag lifecycle was checked exhaustively (check 3).
- The hold engages only on the stated conditions. It is global across interfaces, which is correct because the owed set is global.
- New behaviour worth stating: while the egress stays stalled with a probe held, the core asks for its timer every 1 ms, and held sinks stay in PRB_W_DELAY/PRB_W_RESP until a slot frees (S6). Bounded and benign.
- Ports that ignore the return value now lose a BIND_RX at 7 owed. The integration note now says so (my round 2 S5).

### Tests: UNCLEAN (F3)

- The three new tests are strong for what they cover:
  - pass-by-pass owed position of each held probe;
  - `probes_held` exactly equal to the summed hold passes;
  - sink state after send, TMR_NO_RESP from leaving, commands kept behind, the 191 ms margin;
  - talker departure cancelling a held probe, and the return to `probes_lost` once nothing is held.
- The nine plants all escape without them and are caught with them. The coverage ratchet rises to 813/813 and 424/424 with no new exclusion. The RV32 smoke adds steps 102-109.
- The count of 422 core plants plus 4 generated (VERIFICATION) matches `tests/mutations.json` (426), and the hosted campaign catches all of them.
- `DeclinedGetTxStateIsAnsweredAfterTheHold` now asserts `r.count == 0u` (R793-2 S3).
- Gap: F3.

### Docs: CLEAN in my independent pass (R2-R4 are RESIDUE); UNCLEAN by concurrence with R793-3 F3 (read after the verdict)

- PORTING:96-98 and the PR body's Round 3 "Result" give one pass count for "a BIND_RX included" and "like any kept command". That count holds only for the first kept command (R793-3 F3).
- PORTING:82-101 states the decline, `bind_waiting`, the hold, its end, the held probe's bound, the unchanged `ACMP_OWED_MAX` + 1 pass count, and the gated-port limit and budget. Each matches the code and my probes.
- The new storage rows (`probe_held`, `bind_waiting`), the counter row, ACMP-12 (REQUIREMENTS and `requirements.json`, identical text), ARCHITECTURE:11, CHANGELOG, VERIFICATION's mutation and smoke rows, and the regenerated TESTS and TRACEABILITY rows are consistent. The hosted `traceability`, `test-inventory` and `port-contracts` gates pass.
- **Comment rule:** all 474 added lines under `src`, `include`, `tests`, `examples` and `scripts` were scanned. Every added comment is a `REQ:` tag or a clause citation (for example `// Milan v1.2 5.5.3.5.3`). There is no lane label, lane name, review round, reviewer ID or issue-comment ID.
- **PR body:** the Round 3, Evidence, Memory and cost, and Gates sections match the receipts. The earlier sections now carry the residue fixes (see "Prior findings").
- Wording residue: R2-R4.

## Findings

### F3: MINOR (Tests). The scope boundary of the probe hold is unpinned: three one-line regressions of ACMP-12's new clause pass every test on both targets

- **Where:**
  - `src/acmp.c:798` (which expiries are held) and `src/acmp.c:1100` (`bind_waiting` only when the BIND_RX is declined with one slot free, `owed_count < ACMP_OWED_MAX`).
  - Requirement text: ACMP-12 "while a BIND_RX declined with one slot free waits, hold each **timer probe** instead of owing it".
  - PORTING:82 "A BIND_RX declined with one slot free also sets `bind_waiting`" and PORTING:86 "A timer probe that falls due then, a TMR_DELAY expiry or a TMR_NO_RESP retry".
  - PORTING:89 "With no probe held and no BIND_RX waiting, a timer probe that finds every slot owed … is counted in `probes_lost`".
- **Evidence.** Reviewer plants (`scripts/plants-r3.json`), each a single-token change. `receipts/escape-check.txt` and `receipts/full-suite-*.txt`:

  | Plant | Change | ACMP binary (113 tests) | All 8 ctest targets | RV32 smoke Debug / Release |
  |---|---|---|---|---|
  | `reviewer-hold-every-timer` | `bool probes = kind != ACMP_TIMER_NONE;` | pass | pass | exit 0 / 0 |
  | `reviewer-hold-second-no-resp` | `probes = kind == ACMP_TIMER_DELAY \|\| kind == ACMP_TIMER_NO_RESP;` | pass | pass | exit 0 / 0 |
  | `reviewer-bind-wait-at-full` | drop `&& a->owed_count < ACMP_OWED_MAX` at `:1100` | pass | pass | exit 0 / 0 |

  - These are not equivalent mutants. My boundary probes (`scripts/probe_owed3.inc`) encode the stated behaviour. All three pass at this head (`receipts/probe3-boundary-head.txt`), and each plant fails the probe for its boundary (`receipts/probe3-boundary-reviewer-*.txt`).
  - With a BIND_RX waiting at 7 owed, a TMR_RETRY expiry at head moves the sink on: state 1 (PRB_W_AVAIL), since it is undiscovered. Under `hold-every-timer` it is held instead: state stays 5 (PRB_W_RETRY), `probes_held` 1.
  - A second TMR_NO_RESP at head moves the sink to PRB_W_RETRY (5.5.3.5.23). Under either hold plant it is held: state stays 4 (PRB_W_RESP2).
  - A BIND_RX declined at the full set, with the egress still held when another sink's retry falls due: at head the retry is lost and counted (`probes_lost` 1, state RESP2). Under `bind-wait-at-full` it is held (`probes_held` 1, state stays PRB_W_RESP), and it is re-held every ms for the rest of the egress outage.
  - Branch coverage is 100% because both outcomes of `:1100` and `:798` execute, but no assertion distinguishes them.
- **Impact:**
  - The code at this head is right. The gap is that half of ACMP-12's new clause (only timer probes, only from one free slot) has no failing assertion and no registered plant.
  - A plausible simplification ("hold any timer while a BIND_RX waits") would ship undetected. It delays Milan TMR_RETRY, TMR_NO_TK and second-TMR_NO_RESP transitions while a BIND_RX waits or a probe is held, and holds every probe through an egress outage.
  - CONTRIBUTING requires a protocol change to update its tests. VERIFICATION's mutation row claims the named-assertion discipline for the change.
- **Required outcome:**
  - Add assertions that a non-probe expiry (TMR_RETRY, and the second TMR_NO_RESP) beside a waiting BIND_RX takes its transition on time with `probes_held` unchanged.
  - Add an assertion that a BIND_RX declined at the full set sets no wait, so a probe falling due before the next accepted frame is lost and counted.
  - Register the three plants above (or equivalents) with named kills. `scripts/probe_owed3.inc` is a ready, MIT-licensed starting point: three tests on the existing `AcmpOwed` fixture.
  - Optionally add the TMR_RETRY case to `acmp_owed_smoke`.
- **Verification:** at the new head, the three plants are caught by named needles in the hosted campaign; `validate.py` 28/28; and `scripts/escape_check.py` with `scripts/plants-r3.json` shows them caught.

### R2: RESIDUE (Docs, PR body). `probes_held` counts each held probe per pass, not passes

- **Where:**
  - The counter row at `docs/PORTING.md:336` reads "Passes that held a timer probe…".
  - PORTING:87 reads "Each pass that holds a probe increments `probes_held`".
  - The PR body says "`probes_held` counts the pass".
- **Problem:** the code increments once per held probe per pass (`src/acmp.c:802`). The test asserts the sum over probes: with four retries all due in pass 1, `probes_held` is 2+3+4+5 = 14 over 6 passes.
- **Exact fix:**
  - Counter row: "Holds of a timer probe: one for each held probe in each pass it is held, for a waiting BIND_RX or behind another held probe. A held probe is never dropped for want of a slot."
  - PORTING:87: "Each held probe increments `probes_held` once for each pass it is held."
  - PR body: "`probes_held` counts each held probe once per pass".
  - The test message "each pass that holds a probe counts once" is a registered needle. Leave it, or change it together with its `mutations.json` needle.

### R3: RESIDUE (Docs). "Retries it in the next pass" assumes passes at least 1 ms apart

- **Where:** PORTING:86 says the held probe's "timer is re-armed 1 ms on, so a port that services its timers once per pass retries it in the next pass". PORTING:88 counts the held probe's wait in passes.
- **Problem:** for a port whose passes are shorter than 1 ms, the retry comes at the first timer service 1 ms or more later. The BIND_RX guarantee is unaffected, because the hold re-asserts on every pass.
- **Exact fix:**
  - PORTING:86: replace "so a port that services its timers once per pass retries it in the next pass" with "so it is retried at the first timer service 1 ms or more later, which is the next pass for a port whose passes are at least 1 ms apart".
  - PORTING:88: after "at most one per other sink.", add "These counts assume passes at least 1 ms apart."

### R4: RESIDUE (Docs). "A held probe is never dropped" omits the cancellation the tests pin

- **Where:** PORTING's counter row says "A held probe is never dropped". `HoldEndsWithTheLastHeldProbe` asserts that "a held probe whose talker departs is dropped with the probing it belonged to". The same happens on BIND_RX, UNBIND_RX, rollback or restore for that sink, through `sm_stop` and `sink_reset`.
- **Exact fix:** make the row read "…is never dropped for want of a slot; it is cancelled only when its sink stops probing." This is folded into R2's row text above.

### S6: SUGGESTION (Robustness, Docs). Say what the hold does while the egress stays stalled

- **What happens:** if the egress stalls again while `bind_waiting` is set, or with the set full and a probe held, each due probe is re-armed every 1 ms. So:
  - the core asks for a timer every millisecond per interface;
  - held sinks stay in PRB_W_DELAY/PRB_W_RESP;
  - nothing advances to PRB_W_RESP2/PRB_W_RETRY until a slot frees.
- **Assessment:** this is bounded and arguably right, since nothing could be sent anyway.
- **Suggested wording:** one sentence in PORTING "ACMP owed bound": "While no owed frame is accepted, a held probe asks for the timer again every 1 ms and its sink's probing does not advance."

### S7: SUGGESTION (Docs). "At most one per sink" holds absent a discovery restart

- **Where:** PORTING:88 and :100 bound the extra passes at one per (other) sink.
- **Why that is usually true:** within one wait, a sink's probe, once owed, starts its 200 ms TMR_NO_RESP only when it leaves.
- **The exception:** an ADP re-advertisement with a non-increasing available index, or a `acmp_tk_unregistered` call, restarts discovery with a fresh TMR_DELAY draw (`src/acmp.c:672-678`, `:1237`). That can owe a second probe from the same sink inside the window if the draw is short.
- **Suggested wording:** "at most one per sink unless that sink's discovery restarts".

## Prior findings at this head

### Disclosure

The verdict, findings and ledger above were written before I read any other reviewer's report for this round. After reading the concurrent R793-3 report, I changed only:

- the BIND_RX-and-behind sentence (verdict and check 1);
- the two lens headings (Conformance and Docs);
- the ledger rows those lenses move by concurrence.

Each change is marked as such where it appears.

- My own items (R794-1, R794-2) are resolved below from my own packets.
- The other reviewer's R793-2 items are as the brief names them. I recorded them in my round 2 report after its verdict. Their status here comes from the code, docs and PR body at this head.

| Item | Status at b7a5988 | Basis |
|---|---|---|
| R794-2 **F2** MINOR: timer probes overtake a deferred BIND_RX | **Resolved** (option 2, as ruled) | Check 1: pass 9 for 0/1/4/14 probes, 200 ms at the margin, `probes_lost` 0. PORTING:97 "whatever timer probes fall due meanwhile". The bound is stated (check 2). The PR-body Round 2 sentence is corrected (body lines "With no timer probe falling due, … Round 3 holds such a probe instead."). |
| R793-2 **F2** MINOR (same defect) | **Resolved** | As above |
| R794-2 **R1** / R793-2 **RES1**: Debug ELF 145380 vs 145180 | **Resolved** | The PR body now says the two tables were built at different paths, so compare Debug ELF bytes only within one table. |
| R794-2 **S4**: pin the timer interplay in the RV32 smoke | **Taken** | `examples/rv32/smoke.c` steps 102-109. 7 of 9 plants are caught (check 4). |
| R794-2 **S5**: parent killer test, needles and wider decline window | **Taken** | The integration note names `AcmpCore.A19AFullQueueDropsTheCommandBeforeItActs` → `…DeclinesTheCommandBeforeItActs`, both needles, the BIND_RX loss at 7 owed for return-ignoring ports, the gated-port budget, and the changed `sm_stop` fragment. Live parent dev `0a75aa77` (read-only) line 143 is `acmp-stop-keeps-the-hold` with `…timer_held = false;\n}`, which no longer matches at this head, as stated. |
| R793-2 **S3**: GET_TX_STATE test omits connection count | **Resolved** | `tests/test_acmp.cpp` adds `r.count == 0u`. |
| R793-2 **S4**: publish full `validate.py` and `baremetal.py` receipts at the exact head | **Resolved** | `author-r3/receipts/final-head.txt` = b7a5988; `final-gates.json` 28/28 rc 0 incl. `graphs`; `final-mutation.log` 426/0/0; `final-coverage.log` 813/813, 424/424; `final-baremetal.log` and `final-rv32-results.json` rc 0, with the Release ELF identical to mine. Per-commit `gates-s1b/s2/s3.json` are 28/28 at 968a164, 8a1cb08 and d355236. |
| R793-2 **RES2**: "Round 3 merges main d7e6a2a1" and stale privacy bullet | **Resolved** | The section is now "Sync with main d7e6a2a1", and its privacy bullet ends "Main fixed this in #30; see Sync with main cc3362f8." |
| R793-2 **RES3**: ARCHITECTURE omits the two-slot BIND_RX case | **Resolved** | `docs/ARCHITECTURE.md:11` reads "…past them a command, and a BIND_RX with fewer than two free, is declined to the port". |
| R793-2 **RES4**: "the full 109-test ACMP suite" | **Resolved** | It now reads "113 tests at this head: 112 ACMP…", which matches the binary (my run: 113; 110 with the round 3 tests excluded). |
| R794-1 F1, S1-S3 and R793-1 F1, S1, S2 | **Remain resolved** | Unchanged code paths; see my R794-2 report. S1's consequence (F2) is now closed. |

## Concurrent review R793-3 at this head (comment 6722039867, read after my verdict and ledger)

| Its item | My position | Basis |
|---|---|---|
| **F3** MINOR (Docs, Robustness): the answer-time budget covers only the first kept command; commands kept behind it miss 200 ms at the 191 ms margin | **Concur, MINOR.** I also attribute Conformance (the Table 5.26 budget). I missed it in my own pass, and my first draft repeated the error (see Correction). | `receipts/probe5-kept-behind.txt`, my probe at this head with a 191 ms hold. BIND_RX then two GET_RX_STATE give 200 / **202 / 203 ms**; three GET_RX_STATE give 200 / **201 / 202 ms**. The in-tree `behind` case pins positions 10 and 11, not times. The gap is latent since round 1 for any backlog. Round 3 widens the claim ("a BIND_RX included", "like any kept command"). R793-3's exact fix (a)-(c) is sound: state pass `ACMP_OWED_MAX` + 1 + *f*, where *f* counts the frames owed by the kept commands ahead, two per BIND_RX. |
| **F4** MINOR (Tests): five stated behaviours of the hold unpinned | **Concur; superset of my F3.** | Three of its plants are mine in substance: set-when-full, the RESP2 timeout, every timer. Its two others are new to me and plausible: `bind_waiting` cleared by a refused poll, and a new binding keeping `probe_held`. I did not run them. One F4 test set closes both F4 and my F3. |
| **S5** (Docs): "next pass" holds for passes of at least 1 ms | **Same as my R3** | I rated it RESIDUE with an exact fix; either classification is acceptable to me. |
| **S6** (Robustness, Docs): a held probe has no fixed wait while the port keeps commands | **Concur; same family as my S6** | PORTING:88's per-frame term covers it; one sentence would help. |
| **RES5**: `probes_held` undercount wording | **Same as my R2** | Either exact fix works. Mine also covers R4's "never dropped" qualifier. |
| **RES6**: "waits from … through the pass that takes the BIND_RX" → "waits at most …" | **Concur, RESIDUE** | A BIND_RX that owes only its answer (unknown sink) leaves 7 owed after its take, so a held probe is owed in that same pass (`src/acmp.c:783`). |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R793-3 F3, concurred after the verdict; CLEAN in my independent pass) | ACMP-12 text (MD and JSON); PORTING:74-104; `src/acmp.c:776-825, 948-980, 1096-1104, 1172-1196, 1254-1273`; held and non-held expiry kinds against Milan 5.5.3.5.10/.16/.23/.30/.36; unchanged round 2 probes; gated-port probe; boundary probes | R794-3 (delta); unchanged parts from R794-1/2 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| RTL (C core, both targets) | CLEAN | `acmp.h` and `acmp.c` delta; struct sizes on x86-64 and RV32 (compile-time asserts at both heads); hold-loop termination; `baremetal.py` Debug/Release rc 0 with the Release ELF byte-identical to the author; cost harness byte-identical (2 configs); hosted 28/28 and RV32 rc 0 | R794-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Robustness | CLEAN (S6 suggestion) | Flag lifecycle over every `sm_timer`/`sm_stop`/`sink_reset` site; `bind_waiting` set and clear; multi-interface scope; stalled-egress behaviour; return-ignoring and gated ports | R794-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Tests | UNCLEAN (F3; also R793-3 F4, a superset) | Three new tests plus the changed GET_TX_STATE test; `mutations.json` delta (9 new, 3 re-anchored); escape check of 9 plants (all escape without the round 3 tests and are caught with them); RV32 smoke under 9 plants (7 caught, matching the author); 5 reviewer plants (2 caught, 3 escape all ctest and RV32); coverage 813/813, 424/424; hosted 426/426 | R794-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |
| Docs | UNCLEAN (R793-3 F3, concurred after the verdict; CLEAN in my independent pass, with R2-R4 RESIDUE and S6, S7 suggestions) | PORTING, ARCHITECTURE, REQUIREMENTS, `requirements.json`, TESTS, TRACEABILITY, VERIFICATION, CHANGELOG deltas; the 12 CRITICAL phrases; PR body (all sections, cost rows against receipts); comment-rule scan of 474 added lines; commit messages | R794-3 | b7a59887f5f2ff729206b87a268972c637882dc0 |

## Real limits

- No standards PDFs were available. Clause numbers and titles were judged from the repository's citations.
- Under the owner's token-economy rule, I did not rerun the full `validate.py` kit or the full mutation campaign. Exact-head execution evidence for those is the hosted run's artifact (28/28, 426/426, coverage) and the author's published `final-*` receipts. My own runs at the exact head were:
  - `baremetal.py` (Debug and Release);
  - the ACMP test binary unplanted and under 14 plants;
  - all 8 ctest targets and the RV32 gate under 3 plants;
  - the RV32 gate under the 9 registered plants;
  - the cost harness (2 configs);
  - size checks on both targets;
  - five probe files. The fifth, `probe_owed5.inc`, was written after reading R793-3, to verify its F3.
- The evidence commit is unsigned and carries no detached signature. I checked its integrity by manifest sha256 and git blob ids only.
- R3's sub-millisecond-pass case and S7's discovery-restart case come from code reading. I did not probe them.
- No physical calibration or hardware was run. Field skips are not hardware proof.
- I ran no manager source bank, parent build or parent harness, and I infer none. Hosted jobs were judged by their job and step conclusions and their two artifacts. Hosted and act acceptance are the manager's.

## Receipts and reproduction

- Every published file is listed in `MANIFEST.sha256`. The receipts contain no host paths; build paths in gtest failure lines read `<copy>/`.
- Scripts. Set `TOOLS` to a prefix holding `gtest-1.14.0`. The RV32 scripts also need `riscv64-elf-gcc` and `qemu-system-riscv32`.
  - `scripts/fetch_evidence.sh TREE_TSV OUT`: fetches evidence blobs by id and checks each git blob hash.
  - `scripts/run_probes2.sh HEAD_TREE WORK OUT` with `scripts/probe_owed2.inc`: my round 2 probes, unchanged.
  - `scripts/run_probes3.sh HEAD_TREE WORK OUT INC FILTER [PLANT PLANTS_JSON]`: appends a probe file (`probe_owed3.inc` boundary probes, `probe_owed4.inc` gated port, `probe_owed5.inc` commands kept behind the first) to a disposable copy, optionally applies a plant (`scripts/apply_plant.py`), and runs it.
  - `scripts/escape_check.py HEAD_TREE WORK OUT scripts/plants-r3.json`: one build, then each plant run with the full ACMP binary and without the three round 3 tests.
  - `scripts/rv32_plants3.sh HEAD_TREE WORK OUT JOBS PLANT...`: runs the RV32 gate under registered plants, then each smoke ELF directly under QEMU (the exit code is the first failing check).
  - `scripts/plant_full.sh HEAD_TREE WORK OUT PLANT PLANTS_JSON JOBS`: all ctest targets plus the RV32 gate under one plant.
  - `scripts/measure_cost.sh TREE OUT ISA OPT MEASURE_C -DLANE`: rebuilds the published cost harness.
  - `scripts/sizes3.c`: compile-time size asserts.
- Clone integrity after all probes (`receipts/clone-state.txt`). All work ran on exported copies; the clone was never written.
  - HEAD, the HEAD tree and the index tree are exact.
  - The worktree equals the index and HEAD, and all 98 worktree blobs match the index.
  - All 98 entries are mode 100644. The repository tracks no gitlinks, so no submodule gitlink applies.
  - There are no untracked or ignored files.

## Pending manager duties

- Validate the current-dev merge candidate (source base 70936b77, live dev 0a75aa774b89ac89351700f63dd8cbb89694af6c) with the builder and native banks at the merge turn, and link those receipts. Hosted and act acceptance are the manager's.
- Carry R2-R4, and R793-3's RES6 (which I concur with), to the residue checklist. R793-3's RES5 duplicates my R2.
- Re-review at the head that addresses my F3 and R793-3's F3 and F4.
- The parent PR that moves the pin to this head must:
  - update `acmp_mutants.py:452-455` and `acmp_review_mutants.py:143` as the integration note says;
  - re-measure the S2b harness row "an ACMP command behind the owed input".

  Until then #26 stays open, as the PR intends.

R794-3 FINISHED
