[R400] NEGATIVE - exact head 053f979b9cfc84871ff2e107d43d20bf0e950db4

# R400-2: processor PR #135 (lane C2, MAAP), issues #66, #67, #68, round 2

- Exact head `053f979b9cfc84871ff2e107d43d20bf0e950db4`, tree `33087148b197340778ee033f3f2210ac0f629059`, base `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`. Round-1 head `b03d36f2`, with nine commits since.
- **Verdict: NEGATIVE.** Two MINOR findings are open: R400-2-F1 (Tests) and R400-2-F2 (Docs). There is also one SUGGESTION, and the two round-1 SUGGESTIONs are retained.
- **What is right at this head:**
  - The RTL implements the manager's ruling (#66 comment 5890772857) in every walker state.
  - All three ruling points are met, and I reproduced each one.
  - Every round-1 MINOR (R400-1 F1 to F4, R401-1 F1) is resolved, except the test clause of R400-1 F1. That clause is carried forward as R400-2-F1.
  - Every processor entry point I ran is rc 0, and every author arm is KILLED.
- **Why the verdict is negative:**
  - Three reviewer mutants survive the suite. Each drops one TX-path state from the Release! latch, and each is a real defect: under it, a one-cycle Release! is absorbed. The head behaves correctly, but no test pins that behaviour in those three states.
  - The PR body still carries a round-1 "What remains" paragraph that contradicts both the head and the ruling.

## 1. What was reconstructed, in order

1. The processor repository has no AGENTS.md or CONTRIBUTING.md at this head. Its conventions come from `docs/README.md`: the single-source rules, the citation form, and the editing workflow (`make check`).
2. The issue sources on #66:
   - the issue body and its acceptance list;
   - the lane assignment (5884446021);
   - the round-2 assignment (5887951933);
   - the author's STOP (5890736650);
   - the manager's ruling (5890772857): option 2, per Table B.7's Release! row, B.3.1 (c) and (e), B.3.2, B.3.5.2 and Table F.23;
   - REVIEW READY (5893086634).
3. The authorities:
   - `docs/architecture/11_maap_engine.md` §6 and §10;
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md` REQ-MAAP-001, REQ-MAAP-005 and REQ-MAAP-007;
   - the quasi-static rule in `02_interfaces.md` §2, rule 4;
   - the `KL_pp_maap.sv` banner;
   - the top's TX-pool access arbiter (`protocol_processor_top.sv:3663-3740`) and its PRNG owner mux (`:2707-2780`);
   - `KL_pp_tx_slots.sv`, for allocation and grant semantics.

   IEEE 1722-2016 Annex B was judged through the clause references in the ruling and in 11. The standard itself is not distributed.
4. The diff and its history:
   - `git diff c951a9ff..053f979b` (37 files) and each of the nine round-2 commits;
   - RTL logic is final at `8ae76ee`. `2c11d6f`, `8382cf6` and `053f979` change only comments in `KL_pp_maap.sv` (`receipts/rtl-logic-by-commit.txt`).
5. The public evidence at milan-fpga `b67b3f67:review-evidence/ppC2-r1`: the author-r2 packet, including the final `run_suites.log` (1,015,996 checks, maap 191), and my own R400-1 packet, whose scripts and patches I re-ran.
6. The PR body and hosted checks.
7. Last, after my verdict and ledger were recorded (`receipts/verdict-before-prior-findings.md`), the prior public findings: R400-1 (5887946706) and R401-1 (5887948102).

## 2. Evidence I produced

| Run | Result | Receipt |
|---|---|---|
| Tool identity | The brief's path `…/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the Verilator **5.050** wrapper at the sibling pinned path `…/372-manager-r2/pinned-tool-bin`, and its identity and binary sha256 are recorded. Every build ran through `scripts/verilator-j8`, which rewrites `-j 0` to `-j 8`. | `receipts/tool-identity.txt` |
| Head `tb/maap run` | rc 0, **191/191**. U23: 5 offsets before the ANNOUNCE's slot request and 75 from it, with a maximum of 63 cycles from the fall to the lane. U28: 17 falls, all 12 walker states. | `receipts/head-tb-maap-run.log` |
| Head `tb/rx_validator run` | rc 0, 453/453 | `receipts/head-tb-rx_validator-run.log` |
| Head `tb/pp_top maap-internal` | rc 0, 33 checks, 0 failures | `receipts/head-tb-pp_top-maap-internal.log` |
| Head `make -C tb/maap mutants` (pristine export) | rc 0, **27/27**: 3 controls PASS and 24/24 arms KILLED, each on its named check | `receipts/head-tb-maap-mutants.log`, `receipts/campaign-logs/*` |
| `make links matrix modmatrix params`, and `git diff --check c951a9ff 053f979b` | all rc 0 | `receipts/head-doc-checks.log` |
| Focused lint of `KL_pp_maap` (`-Wall`, the `lint_hdl.sh` flags) | base rc 0 with 0 warnings; head rc 0 with 0 warnings | `receipts/lint-KL_pp_maap-*.log` |
| Failing first: the head `tb/maap` against the `b03d36f` RTL | rc 2, **20 FAIL** (U17c, U23 x2, U24 x4, U25 x3, U26 x4, U27 x2, U28 x4) | `receipts/head-tb-vs-rtl-b03d36f.log` |
| Failing first: the head `tb/maap` against the `4de2c60` RTL | rc 2, 2 FAIL (U27 W_ADDR arc: the seed is not re-armed) | `receipts/head-tb-vs-rtl-4de2c60.log` |
| Reviewer probe (`scripts/r400_release_probe.cpp`, run by `scripts/run_probe.sh`) at the head | rc 0, **39/39**. PA: 20 one-cycle falls in `W_IVAL`, `W_ALLOC`, `W_GWAIT`, `W_WRITE`, `W_COMMIT`, `W_LANE` and `W_POST`, across PROBE retransmit, DEFEND re-announce and sDefend. Every one gives INITIAL and a fresh 4-PROBE walk. PB: 400 long falls, 100 offsets each from a probe expiry, an announce expiry, an sDefend record and a yielding rAnnounce!. None has a slot request, timer start or expiry, or claim after the fall. At most one frame drains, of the entry's own type, and the latency maximum is 63 cycles. | `receipts/probe-head.log` |
| Reviewer mutants (`scripts/r400_mutants.py`) on `tb/maap` | 12 arms (table below): 7 KILLED, 3 SURVIVE and are non-equivalent (F1), 2 SURVIVE and are equivalent | `receipts/r400-mutants/*` |
| Reviewer probe against the surviving arms | `tx-set-omits-alloc`, `-gwait` and `-commit` are each **KILLED** by PA: 3 of 20 falls absorbed, with a claim kept in DEFEND. `ival-fall-skips-teardown` survives the probe too (equivalent). | `receipts/probe-tx-set-omits-*.log`, `receipts/probe-ival-fall-skips-teardown.log` |
| R400-1 probes P1 to P5 and R400-1 mutants re-run at this head (`scripts/r400_1_rerun.sh`) | P1 and P1c: `0x2000` (seed re-armed). P3 and P5: claim dropped, fresh walk. P4: 0 PDUs from the draw offsets. P2: the claim part is 0 of 160. The PDU part is 64 of 160, starting at k=5, which is exactly U23's pre-request boundary, so these are the drains the ruling admits (see §3, R400-1 F1). `r400-release-waits-for-draw` KILLED (U17c). `r400-release-clears-mark-only-if-prng-idle` KILLED (U17b, U17c). `r400-seed-clamp-off-by-one` KILLED (U18b). `r400-compare-mac-word-reversed` KILLED. `r400-compare-mac-last-octet-only` survives both suites (S1, retained). | `receipts/r400-1-rerun/*` |
| Clone integrity after all probes | HEAD, tree and `git write-tree` all equal `33087148…`. The worktree and index equal HEAD. 0 untracked or ignored entries. 332 tracked blobs match in bytes and mode. 0 gitlinks: this repository has no submodules, so none are required. | `receipts/clone-verify.txt` |
| Hosted checks at the head (15:40 UTC) | push run 36588714000: `portability` success, `docs-gates` success. `suites` in progress: the "Lint + every suite" step executed with success, the SRP campaign was running, and the MAAP campaign, traceability and figures steps were pending (not executed). | `receipts/hosted-check-runs.txt` |

### Reviewer mutants

| Arm | Planted defect | `tb/maap` | Outcome |
|---|---|---|---|
| `tx-set-omits-alloc` | The Release! latch at `KL_pp_maap.sv:589-590` omits `W_ALLOC` | 191/191 | **SURVIVES**. Non-equivalent: PA kills it (F1). |
| `tx-set-omits-gwait` | … omits `W_GWAIT` | 191/191 | **SURVIVES**. Non-equivalent: PA kills it (F1). |
| `tx-set-omits-commit` | … omits `W_COMMIT` | 191/191 | **SURVIVES**. Non-equivalent: PA kills it (F1). |
| `tx-set-omits-write` | … omits `W_WRITE` | 4 FAIL (U24) | KILLED |
| `tx-set-omits-lane` | … omits `W_LANE` | 3 FAIL (U25) | KILLED |
| `tx-fall-keeps-claim` | The TX-path fall latches but does not withdraw the claim | 3 FAIL (U24) | KILLED |
| `off-keeps-rel-pend` | `W_OFF` never clears the latched Release! | 50 FAIL | KILLED |
| `ival-fall-keeps-draw-mark` | The `W_IVAL` fall keeps `draw_act_r` | 2 FAIL (U17c) | KILLED |
| `post-teardown-keeps-chain` | The `W_POST` Release! keeps a pending probeCount! chain | 1 FAIL (U23) | KILLED |
| `seed-clamp-value-minus-one` | The seed clamps to `0xFE00 - count - 1` | 6 FAIL (U18, U18b) | KILLED |
| `ival-fall-skips-teardown` | The `W_IVAL` fall goes straight to `W_OFF` | 191/191 | Survives. **Equivalent**: no timer runs in `W_IVAL` (every entry into it follows an expiry, a probeCount! with the re-arm skipped, or generate_address), and PA and PB agree. |
| `seed-clamp-ge` | The seed clamp uses `>=` | 191/191 | Survives. **Equivalent**: at seed == fit, the clamp value equals the seed. |

## 3. Prior public findings: resolved or retained at this head

| Finding | Status at `053f979b` | Evidence |
|---|---|---|
| R400-1 F1 (MINOR): Release! across `W_IVAL`, the TX states and `W_POST` | **Resolved** on Conformance, RTL, Robustness and Docs, judged as the ruling's three points. **Its test clause is not fully met** ("each must have a failing arm" for a fall followed by a rise while busy), and that part is carried forward as **R400-2-F1**. | **(1)** No PDU is generated after the fall: `KL_pp_maap.sv:589-593, 613-627, 660-669, 719-728, 747-752, 797-804`. U28 (17 falls, 12 states), my PB (400 falls from four entries) and the arms `idle-serves-a-latched-expiry-first` and `teardown-keeps-announce-timer` are all KILLED. **(2)** At most one frame drains: U23 (75 drained, maximum 63 cycles), PB (maximum 63 in each entry), and `drain-waits-for-the-link` KILLED. R400-1 P2's 64 "PDU after Release!" offsets begin at k=5, the same boundary U23 reports, and each lies in the request-to-grant window. **(3)** 11 §6 (`:136-167`) and the banner (`:58-79`) cite Table B.7, B.3.2 and B.3.5.2, and both say "no PDU generated after the fall". REQ-MAAP-007 is reworded to match. The window is stated as 63 cycles in the unit, longer in the top, and unbounded while the egress stalls (U25). |
| R400-1 F2 (MINOR): the seed re-arm depends on where the Release! lands | **Resolved** | `8ae76ee`: `W_OFF` re-arms the seed (`:597-605`), and the comment at `:315-322` and 11 §6 agree with it. U27 fails against the `4de2c60` RTL and passes at the head. `seed-rearmed-on-idle-release-only` is KILLED. R400-1 P1 and P1c both give `0x2000`. |
| R400-1 F3 (MINOR): seed clamp boundary | **Resolved** | U18b (`sim_main.cpp:813-842`) tests `0xFDF9` (clamped) and `0xFDF8` and `0xFDF7` (taken as given), each byte-exact. `seed-clamp-off-by-one` and my `r400-seed-clamp-off-by-one` are both KILLED on U18b. |
| R400-1 F4 (MINOR): U17b cannot tell abandon from wait | **Resolved** | U17c (`:716-770`) covers draws that fit. `release-waits-for-draw` and my `r400-release-waits-for-draw` are both KILLED on U17c. |
| R400-1 S1 (SUGGESTION): a compare_MAC pair with equal low octets | **Retained** (not in the round-2 assignment) | `r400-compare-mac-last-octet-only` still survives `tb/maap` (191/191) and MP (33/33) |
| R400-1 S2 (SUGGESTION): `MUTANT_OUTPUT` defaults to a shared `/tmp` path | **Retained** (not in the round-2 assignment) | `tb/maap/Makefile:4` |
| R401-1 F1 (MINOR): seed re-arm on the `W_ADDR` exit | **Resolved** by outcome (a) | Same evidence as R400-1 F2 |
| R401-1 F2 (SUGGESTION): a 1- or 2-cycle fall in `W_IDLE` is lost | **Resolved** | `W_OFF` starts on the engage level (`:606`). U26 covers falls of 1 to 4 cycles in `W_IDLE` and 1 cycle on `W_RX`. `off-waits-for-an-edge` is KILLED. |
| R401-1 F3 (SUGGESTION): `W_IVAL` and the TX states ignore the engage level | **Resolved** under the ruling | As R400-1 F1, points (1) and (2) |
| R401-1 F4 (SUGGESTION): name both stalled states | **Resolved** | `8382cf6`: `:615-625` and `tb/maap/README.md:172-174` name `W_ADDR` for an unseeded walk and `W_IVAL` for a seeded one. The comment's line break makes the sentence awkward, but it is accurate. |

The other items I was assigned to judge:

- **Scenario order (`ea79d8b`)**: U19 to U22 still end `run()` (`sim_main.cpp:1495-1498`), so the R400-1 insertion anchors apply unchanged.
- **`fa21c58` and `2c11d6f`**: each has a failing arm (see above).
- **Every author arm**: KILLED at the head (27/27).

## 4. Findings

### R400-2-F1: MINOR. Lens: Tests

- **Where:**
  - `tb/maap/sim_main.cpp:1204-1241` (U26, short falls only in `W_IDLE` and `W_RX`), `:1079-1151` (U24, a 5-cycle bounce only in `W_WRITE`) and `:1336-1354` (U28, whose TX-path points hold the fall for 33 s);
  - the behaviour those tests should pin: `hdl/maap/KL_pp_maap.sv:589-593`, and the claim at `:58-60` and `docs/architecture/11_maap_engine.md:136-137` that a Release! is "seen in every walker state however short".
- **Authority:**
  - Table B.7: Release! goes to INITIAL, then PortOperational! starts a fresh walk.
  - R400-1 F1's required outcome: "a fall followed by a rise while the walker is busy must still produce INITIAL and a fresh walk. Each must have a failing arm."
  - The round-2 assignment: each resolution needs "a failing arm or mutant".
- **Evidence:**
  - The mutants `tx-set-omits-alloc`, `tx-set-omits-gwait` and `tx-set-omits-commit` each remove one state from the TX-path Release! latch, and each passes `tb/maap` 191/191 (`receipts/r400-mutants/`).
  - They are not equivalent. The reviewer probe PA (`scripts/r400_release_probe.cpp`) lands a one-cycle fall in each of those states. Under each mutant, 3 of 20 falls are **absorbed** (`receipts/probe-tx-set-omits-*.log`), with no INITIAL:
    - in PROBE retransmit, the old walk continues (`fresh=2`, then ANNOUNCE);
    - in DEFEND re-announce and in sDefend, the claim stays valid through the Release! and no fresh walk starts.
  - At the head, PA passes 20 of 20.
  - The suite misses these states for two reasons. U28's long falls are always caught again by the next TX state. U28's TX-path points are in the first PROBE's entry, where `pstate` is already INITIAL, so the claim check there is vacuous.
- **Impact:**
  - The RTL is correct today.
  - But a regression that drops any of these three states from the latch would reintroduce the absorbed Release!/PortOperational! pair, the round-1 defect, on reachable one-cycle `link_up_i` or config glitches, and no test or campaign arm would turn red.
  - The docs claim coverage "however short" that the suite does not grade.
- **Required outcome:**
  - Add one-cycle falls (fall and immediate rise) first seen in `W_ALLOC`, `W_GWAIT` and `W_COMMIT`, at least in one DEFEND entry (sDefend or re-announce) and one mid-walk PROBE entry. Each must require INITIAL, no claim valid after the fall, and a fresh 4-PROBE walk.
  - Add campaign arm(s) that omit a single TX state from the latch, KILLED on the new named check, with ledger rows in `tb/maap/README.md`.
- **Verification:**
  - The head stays green.
  - `receipts/r400-mutants/tx-set-omits-{alloc,gwait,commit}.patch` each fail `tb/maap` on the new check.
  - `make -C tb/maap mutants` stays all-KILLED.

### R400-2-F2: MINOR. Lens: Docs

- **Where:** the PR #135 body, section "What remains" (round 1, not superseded).
- **Authority:**
  - The ruling 5890772857: footnote c says the range becomes free, and it does not say that a PDU already produced is withdrawn.
  - The brief's requirement that the PR body state the ruling and its limits accurately.
  - The PR body is the merge record.
- **Evidence:** at this head the paragraph still says, of "two corners of the Release! arc … not in this scope; each would need its own issue", that:
  - "the `W_ADDR` engage-fall exit does not re-arm the footnote-a seed". This is false since `8ae76ee` (`KL_pp_maap.sv:604`; U27).
  - "a frame already being drawn or built when the engage falls still leaves the wire, although footnote c says Release! sends no PDU". This is false for a frame being drawn, which is dropped whole before its slot request (U17c, U23, U28 and PB). For a frame being built, it restates the footnote-c reading the ruling rejected.

  The Round 2 section below it states the ruling correctly, so the body now contradicts itself. Section 1's "RTL fix … `KL_pp_maap.sv:569-577`" line reference is also stale (now `:613-627`).
- **Impact:** a reader of the merge record gets two false statements about the shipped engine's Annex B behaviour, and a misreading of footnote c the manager explicitly ruled on.
- **Required outcome:**
  - Rewrite or strike "What remains" so that it matches the Round 2 section. Both corners are resolved: the seed is re-armed on every Release!, and a frame requested before the fall may drain per Table B.7, B.3.2 and B.3.5.2.
  - Mark the round-1 line references as round-1, or refresh them.
- **Verification:** the PR body at the next head contains no statement that contradicts 11 §6 or the ruling.

### R400-2-S1: SUGGESTION. Lenses: Tests, Docs

- **Where:** U28's check "no TX slot request follows the fall" (`tb/maap/sim_main.cpp:1443-1445`), `tb/maap/README.md:157-158`, and the PR body's "no slot request follows the fall".
- **Evidence:**
  - At the top, a MAAP request is latched into the pool-access arbiter's pending set (`protocol_processor_top.sv:3713`), and a request that finds the pool owned or full is retried (`KL_pp_maap.sv:694-703`, `W_GWAIT` to `W_ALLOC`; the top banner at `:3669`).
  - A fall during that wait is therefore followed by further `txs_alloc_req_o` pulses for the same frame. Abandoning it would leave the arbiter locked on MAAP waiting for a commit, so the retries are correct and the frame is the one the ruling lets drain.
  - The unit bench's pool always grants at once, so it never shows this.
- **Suggestion:** say "no new slot request" (a request already pending is retried until granted) in the check message, the README and the PR body.

### Retained from round 1

- **R400-1 S1 (SUGGESTION, Tests):** there is still no tie-break pair with equal least-significant wire octets.
- **R400-1 S2 (SUGGESTION, Tests):** the shared default `/tmp/maap-mutants`.

## 5. Items examined and found correct (not findings)

- **Release! RTL in all 12 walker states.** Each state handles a Release! as follows:
  - `W_OFF`: starts on the engage level, re-arms the seed, and clears `rel_pend_r`.
  - `W_ADDR`: parks with the draw mark cleared, with no timer running and `pstate` INITIAL on every entry.
  - `W_IVAL`: the fall wins over a same-cycle draw answer, and no arm is issued.
  - The TX states: withdraw the claim and latch the Release!, with the frame past recall. The arbiter's pending latch and `KL_pp_tx_slots`, which has no abort, make that true.
  - `W_POST`: drops the entry's state change and clears `chain_ann_r`.
  - `W_IDLE`: the fall has priority over a latched expiry and over a record.
  - `W_RX`: tears down with no sDefend or yield.
  - `W_TEARDOWN`: cancels both slots.

  Abandoned draws are safe in the unit and in the top (the shared busy covers the flight, and the owner routing reaches only MAAP while its mark is clear). No module port changed.
- **Seed clamp (`fa21c58`).** The boundary is exact. `>=` is equivalent; `+1` and `-1` are KILLED.
- **Drain window.** 63 cycles runs from the request to the lane grant. It is measured in U23 and in PB (maximum 63 in each of four entries) and stated with the limits the ruling asked for.
- **PR body Round 2 section.** It states the ruling (option 2: no cancel path, no port change), its three points, the drain window and the stall bound accurately. Its per-finding table matches the commits, and its tallies match my runs (191, 27/27). The closing references are #66, #67 and #68 (`closingIssuesReferences` = [66, 67, 68]).
- **Parent-visible (round 2).** There is no port, parameter or interface change. `maap_wrap.sv` adds harness-only observation ports and one hierarchical read (`walker_o`). REQ-MAAP-007 is reworded. The engine is dark in the parent (`cfg_maap_internal_i` is tied to 0, per the author and R400-1; not re-checked at dev `ec0cc0c1`).
- **Out of scope.** A `cfg_count_i` change during a drain would alter the drained frame's `requested_count`, because the frame is built from the live input. `cfg_maap_count_i` is quasi-static (02 §2, rule 4; 11 §10), so this is outside the contract and is not a finding.

## 6. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5890772857 (Table B.7 Release!, B.3.1 (c) and (e), B.3.2, B.3.5.2, Table F.23) against `KL_pp_maap.sv:58-79, 589-850`; U17c, U23 to U28; PB (400 falls, four entries); PA at the head; R400-1 P1 to P5 re-run; #66, #67 and #68 acceptance still met (U17, U18, U18b, F28, MP4, MP7, campaign 27/27) | R400-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| RTL | CLEAN | The `KL_pp_maap.sv` round-2 diff and the whole walker; RTL logic final at `8ae76ee` (later commits are comment-only); `protocol_processor_top.sv:2707-2780, 3663-3740`; `KL_pp_tx_slots.sv` allocation; `KL_pp_prng.sv` busy; focused lint at base and head (0 warnings); 12 reviewer mutants (2 equivalent, analysed) | R400-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Robustness | CLEAN | One-cycle and long falls in every TX-path state and in `W_IVAL` and `W_POST`, across PROBE, DEFEND re-announce, sDefend and yield (PA, PB); stalled lane (U25); abandoned draws in unit and top; pool contention at the top (S1); quasi-static config (§5) | R400-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Tests | **UNCLEAN (R400-2-F1)**; S1 and retained R400-1 S1 and S2 | `tb/maap/sim_main.cpp` (U17c, U18b, U23 to U28), `maap_wrap.sv`, `mutants.py`, 11 new patches; the head suite against the `b03d36f` and `4de2c60` RTL (failing first); the campaign 27/27; reviewer mutants (3 non-equivalent survivors); reviewer probe 39/39 | R400-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |
| Docs | **UNCLEAN (R400-2-F2)** | `11_maap_engine.md` §6 and §11; REQ-MAAP-007; the `KL_pp_maap.sv` banner and comments (`:58-79, 315-322, 581-627`); `tb/maap/README.md` (ledger rows and tallies match my runs; "13 checks" matches the U23 to U26 failures against the start RTL); the PR body (Round 2 section accurate, "What remains" stale); `make links matrix modmatrix params` rc 0 | R400-2 | 053f979b9cfc84871ff2e107d43d20bf0e950db4 |

## 7. Real limits

- **Tool path.** The brief's Verilator path was absent, so I used an identical-version (5.050) wrapper at a sibling pinned path. Its identity is in `receipts/tool-identity.txt`.
- **Runs I did not make.** As the brief requires, I did not run:
  - the full `run_suites.sh`, the SRP campaign, Yosys, `lint_hdl.sh` over the whole tree, the wavedrom and diagram lint targets of `make check`, or the nvm figures;
  - any parent, donor or builder bank.

  The processor-wide tallies come from the author's receipt (`author-r2/receipts/final/processor/run_suites.log`).
- **Manager bank receipts.** I found none in the published evidence tree or in comments on #66 or #135. The manager's source, static, builder and native banks are taken as the brief states them.
- **Hosted checks.** At my snapshot, the hosted `suites` job had not reached its MAAP campaign step.
- **Probe placement.** The probes read the walker state through `walker_o` only to land falls. The pool-contention retry at the top (S1) was reasoned from the source and not simulated in `tb/pp_top`.
- **R400-1 `common.sh`.** Its published copy is path-redacted, so its sha256 differs from the R400-1 manifest. The other 12 fetched R400-1 scripts and patches match.
- **Path redaction.** Absolute paths in my receipts are redacted to `$PACKET`, `$CLONE` and `$TOOLS` before hashing.
- **Standard text.** Annex B was judged from the ruling's and 11's clause citations, since the standard's text is not distributed.
- **Hardware.** Physical calibration was NOT RUN, and no hardware was involved. Skipped field contexts are not proof of hardware behaviour.
- **Merge composition.** Processor main moved to `b2db3a97`, which conflicts with this branch. The merge composition was not judged here, per the brief.

## 8. Pending manager duties

- Route R400-2-F1 and R400-2-F2 to the author, then order a delta re-review.
- Run and post the donor full bank and the parent consumer bank at milan-fpga dev `ec0cc0c1`, with the gitlink at the reviewed head.
- Accept the hosted `suites` job at the exact head once its SRP campaign, MAAP campaign, traceability and figures steps have executed.
- Decide the retained SUGGESTIONs (R400-1 S1 and S2, R400-2-S1).
- At the merge turn:
  - merge processor main `b2db3a97` (the conflicts in `tb/pp_top/sim_main.cpp` and `tb/rx_validator`), with its own delta review;
  - build the final current-dev candidate (source base `c951a9ff`, live dev `ec0cc0c1`).
- Publish `REPORT.md` and the files listed in `MANIFEST.sha256`.

R400-2 FINISHED
