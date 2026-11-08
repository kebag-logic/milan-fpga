[R793] POSITIVE - exact head 376486b374782147d71e5e9bb4f93c42cd10e636

# R793-6: independent internal review of kebag-logic/tsn-c-stack PR #28 (issue #26), delta round

- Exact head `376486b374782147d71e5e9bb4f93c42cd10e636`, tree `f4fd5321cb7d5e1b0fa72f7b894946cec0a9641d`. Both are checked in the review clone and in a clean clone (`receipts/clone-state.txt`).
- Previously reviewed head: `715d208` (R793-5, POSITIVE). Source base: `70936b77`.
- Delta since 715d208: two author commits, `c0477c8` and `376486b`. Each has a one-line subject and no body. History is linear: nothing was merged, rebased or amended.
- `git diff --stat 715d208 376486b -- src include examples` is empty, so the core is unchanged. Code the delta does not touch keeps its R793-1 to R793-5 verdicts.
- The delta is 7 files, +99/−18:
  - `docs/PORTING.md`, `TESTS.md`, `TRACEABILITY.md` and `VERIFICATION.md`;
  - `scripts/check_port_contracts.py`;
  - `tests/mutations.json` (+1 plant);
  - `tests/test_acmp.cpp` (+1 test).
- Authority for this round: the [A10] ruling, issuecomment-6728504171 (`receipts/comment-6728504171.json`). The held-probe wait bound is removed, not patched. I do not ask for a held-probe upper limit.
- Verdict: **POSITIVE**. No finding at MINOR or above is open.
  - R794-5 **F5** is resolved at its cause.
  - R794-5 **RES9** is taken.
  - **RES8** of both reviews went with the clause that was removed.
  - My R793-5 **RES9** is retained as wording. Two new wording residues are recorded, RES10 and RES11, plus one suggestion, S10.
- Gates on a clean clone at the exact head:
  - `validate.py --graphs`: 28 of 28 pass.
  - Full mutation campaign: 444 caught, 0 escaped, 0 errors.
  - `baremetal.py`: passes in Debug and Release. The Release RV32 image is byte-identical to rounds 3, 4 and 5.
  - Every probe from my rounds 3, 4 and 5, and the external review's `probe_owed7.inc`, run unchanged and print the same lines as before.

## Reconstruction order followed

1. CONTRIBUTING.md (there is no AGENTS.md), then each doc the delta touches.
2. Issue #26 body and acceptance, unchanged. On the PR:
   - the [A10] round 6 ruling (6728504171);
   - the public review-start comment (6728781041).
3. The PR #28 body at this head (`headRefOid` = 376486b, `receipts/pr28.json`, `pr28-body.md`): What, Round 4 items 1 and 3, Round 5 items 3 and 4, and Round 6 in full. Also the linked `PR-BODY-rounds-2-3.md`, for the moved Round 2/3 text and the integration note.
4. Authorities:
   - ACMP-12 and ACMP-09.
   - IEEE 1722.1-2021 8.2.4 and 8.2.5.
   - Milan v1.2 5.5.3.5 (.3, .10, .16) and Table 5.26.
   - The code: `src/acmp.c` `probe_yields` :778, `sm_expired` :794, `acmp_timer_expired` :1172-1196, `acmp_poll` :1255-1273, the `acmp_rx` decline :1095-1104, `transmit` :290 and `probe_left`.
5. `git diff 715d208..376486b`, read in full, and the history `715d208..376486b`.
6. Public evidence: milan-fpga `bac9305f` (tip of `tsn26-review-evidence`), `review-evidence/tsn26-r1/author-r6`, read by section.
7. My own round 5 report and scripts.
8. Only after my verdict and ledger were recorded (`receipts/verdict-and-ledger-before-other-review.txt`): the public R794-5 report (issuecomment-6728496625), for its F5, RES8 and RES9, and its `probe_owed7.inc`, run unchanged.

## Answers to the focus items

### 1. The bound is removed, and the new statements match the code

- **Removed.** PORTING and the pins no longer contain:
  - the "waits at most" sentence;
  - "through the pass that takes the BIND_RX";
  - the one-per-other-sink count;
  - the TMR_NO_RESP (200 ms) condition;
  - the "past that" list;
  - "These counts assume passes at least 1 ms apart".

  Each has 0 hits in both PORTING and `check_port_contracts.py` (`receipts/removed-clauses.txt`). The PR body's Round 4 item 3 and Round 5 item 3 no longer state a bound. Round 4 item 1 still does (RES10).
- **PORTING:110 now says** "A held probe is never dropped for want of a slot, and it takes a freed slot only at timer service with no BIND_RX waiting, after every command the core takes first, whether kept or offered for the first time, so no command answer waits for it. Its wait has no upper limit while commands keep taking the freed slots; its own TMR_NO_RESP runs from when it leaves." These are the ruling's four statements. Checked against the code:
  - **Never dropped for want of a slot.**
    - At expiry, `sm_expired` holds a probing expiry whenever `probe_yields` is true. That is the case while `bind_waiting` is set, or while every slot is owed and any probe is held, the expiring one included (`:778-804`). So a held probe is never sent into a full set, and `transmit` never returns LOST for it.
    - Cancellation happens only through `sm_stop` (stop probing) or the cancel-by-response path. Both were reviewed in R793-5 and are unchanged.
  - **Only at timer service.** `sm_expired` is called only from `acmp_timer_expired` (`:1191-1193`, the only call site). The `while (… due(…))` loop stops at once for a re-armed held probe (deadline `now + 1`).
  - **With no BIND_RX waiting.** `probe_yields` returns true first on `bind_waiting`.
  - **After every command the core takes first, kept or offered for the first time.**
    - A command needs only `room()`.
    - Under the redelivery rule (PORTING:85), the port offers every waiting frame, kept ones first, after each accepting poll and before timer service. So any freed slot that a command can take is taken before the held probe's expiry runs.
    - The new test asserts this for commands offered for the first time. Existing tests assert it for kept ones.
  - **No command answer waits for it.** A held probe takes a slot only when no command the core was offered in that pass wanted it. So it never pushes back a command that was waiting. This sentence is the ruling's own wording, and it holds in that sense. S10 suggests one clause to scope it.
  - **No upper limit; TMR_NO_RESP from when it leaves.**
    - `probe_left` calls `no_resp_from_send` when the owed probe frame leaves.
    - My unchanged `probe_r5` holds a retry through pass 5602 with `probes_lost` 0, and `probe_owed7` shows the wait growing one pass per command.
- **The PR body** Round 4 item 3, Round 5 item 3 and Round 6 item 1 state the same four statements. So does the moved Round 3 text in `PR-BODY-rounds-2-3.md:153-160`.

### 2. The command bound and the budget are unchanged

PORTING:104-109 and :111-113 have no diff lines: n + 1 + f + r, the definition of n, `ACMP_OWED_MAX` + 1 + f + r, 193 − 2 × Q, 191 and 189 ms. Their pins are unchanged, the CHANGELOG is unchanged, and so is the What section of the PR body. My `probe_r3`, `probe_r4` and `probe_r4b` give identical lines.

### 3. :92 and :94 count commands offered for the first time

- :92 ends "after the commands the port still keeps or offers before its timer service".
- :94 begins "While the port keeps or offers commands that take the freed slots, or no owed frame is accepted".
- Both match the code above and R794-5's proposed text word for word. Both are pinned (`check_port_contracts.py:300`, `:304`).

### 4. Pins, the new test, the plant and removals

- **CRITICAL.** The six pins of removed or changed clauses are gone. The eight new phrases of :92, :94 and :110 are pinned.
  - The three restart-path phrases moved to the `acmp_rx_ready` pins, with the gated-port sentence (:114) they now qualify. That sentence's "at most one per sink while no sink's probing restarts" is pinned too.
  - The `port-contracts` gate passes, and its self-test refuses 77 meaning-removal controls.
- **New test.** `AcmpOwed.CommandOfferedAfterTheTakenBindDelaysTheHeldRetry` (`tests/test_acmp.cpp:3492`).
  - It runs with 0, 1 and 3 GET_RX_STATE commands offered for the first time, one after each accepting poll once the BIND_RX is taken in pass 2.
  - It asserts that the retry is owed in pass taken + 1 + later (3, 4, 6).
  - It asserts that every answer leaves before the retry, that `probes_lost` is 0, and that TMR_NO_RESP runs from when the retry leaves.
- **New plant** `owed-held-probe-owed-at-the-poll` (`tests/mutations.json`). It owes a held probe at an accepting poll with no BIND_RX waiting, but only when nothing was declined since the previous accepting poll. That leaves kept commands first and isolates the first-offer case. My `plant_escape.sh` (`receipts/new-plant-escape.txt`) shows:
  - the full suite fails only the new test;
  - the named assertion fails with "Which is: 3" against 4 and 6, and both registered needles appear in the failure log (2 and 4 hits);
  - without the new test, the planted binary passes 125 of 125. The plant needs this test.
  - At the head the test passes (`gcc-test` and both sanitizer arms), and the campaign reports `CAUGHT owed-held-probe-owed-at-the-poll`.
- **Removals.** The delta removes no test and no plant (+56/−0 in tests, +20/−0 in plants). No remaining test or needle asserts a removed clause (grep: no "waits at most", "per other sink", "past that" or "through the pass that takes" in `tests/`). `ProbesFallingDueInTheDrainWaitForTheDeferredBind` asserts exact passes with no later command. That case is still stated by the retained "Held probes follow the frames of the last kept command, one per pass", so it correctly stays.
- **Counts.**
  - VERIFICATION: 440 core plants + 4 generated = 444, which matches the campaign.
  - Registration: 449 instances, up from 448.
  - Sensitivity: 175 declarations and 444 plants, each up from round 5 by one.
  - TESTS.md and TRACEABILITY (ACMP-09, ACMP-12) list the new test at L3492. The Wire anchor moved to L3549, which is correct. The traceability gate passes.

### 5. RES9's wording

- **R794-5 RES9** (PR body Round 5 item 4): taken. The body now reads "a probe that falls due then, with no probe held, is lost". This matches `probe_yields`: with every slot owed and no probe held, the expiry is sent into a full set and counted in `probes_lost` (`:744`). It also matches PORTING:96.
- **My R793-5 RES9** (integration note's gated-port sentence): not taken, as outside the ruling. The note now sits in the linked `PR-BODY-rounds-2-3.md:85` and still says "at most one per sink" without the condition that PORTING:114 now carries. It is retained as RESIDUE below.

### 6. Prior probes fall within the new sentences

All ran unchanged on exported trees of the exact head. Every PROBE line is identical to my round 5 receipts (`receipts/probes/`).

| Probe | Result at 376486b | New sentence it meets |
|---|---|---|
| `probe_r3` + `probe_intermittent` (14 tests) | identical 14 lines | command bound, budget, gated port (unchanged) |
| `probe_timer_ahead` (5 tests) | identical | gated port, one pass per probe owed ahead |
| `probe_r4`, `probe_r4b` | identical: the formula holds for port "all" and is one pass late for port "one" | n + 1 + f + r; :85 excludes port "one" |
| `probe_r4c` | identical: sustained case, sink 2 in passes 11 and 250, sink 3 in pass 251; failure response cancels the hold | no upper limit while commands take the slots; cancel by response |
| `probe_r5` | identical: retry held through pass 5602, owed in pass 5611, `probes_lost` 0 | never dropped; no upper limit |
| `probe_r5b` | identical: sink 2's third probe in pass 6409, before sink 3 in pass 6410 | the same two sentences (the removed list was RES8) |
| `probe_owed7.inc` (external, round 5), run unchanged after my verdict | retry owed in pass 3, 4, 6, 13 for 0, 1, 3, 10 later commands, first-offered or kept; `probes_lost` 0; identical to the author's `probe7-head.txt` and to the external review's own receipt | takes a freed slot only after every command the core takes first, kept or offered for the first time; no upper limit; never lost. Its "stated" column prints the removed round 5 limit and no longer applies. |

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### RESIDUE (wording only, carried to the residue checklist)

- **RES9 (retained from R793-5). Lenses: Docs. Linked PR-body file `review-evidence/tsn26-r1/author-r6/receipts/PR-BODY-rounds-2-3.md:85`, Integration note.**
  - **Defect:** the gated-port sentence says "at most one per sink" without the condition that PORTING:114 states and pins.
  - **Why wording only:** it changes no figure. The budget `ACMP_OWED_MAX` + 1 + `n_sinks` is unchanged, and PORTING is right.
  - **Exact fix:** "at most one per sink while no sink's probing restarts (`docs/PORTING.md`, "ACMP owed bound")". Optionally, say in the live body's "(see the integration note)" that the note is in the linked Round 2/3 file.
- **RES10 (new). Lenses: Docs. PR body, Round 4 item 1, `receipts/pr28-body.md:324-325`.**
  - **Defect:** "Held probes follow the frames of the last kept command, one per pass. A held probe's own wait is as round 3 stated it, now as an upper bound." This still claims an upper bound. The Round 3 text it points to (in the linked file) now says the wait has no upper limit, and Round 6 item 1 says this body was brought into line.
  - **Why wording only:** it is a historical PR-body bullet. No figure, test or doc depends on it, and PORTING is right.
  - **Exact fix:** "Held probes follow the frames of the last kept command, one per pass. A held probe's own wait has no upper limit while commands keep taking the freed slots (round 6 removed the earlier limit)."
- **RES11 (new). Lenses: Docs. `docs/PORTING.md:92` ("held probes take freed slots one per pass") and `:110` ("Held probes follow the frames of the last kept command, one per pass").**
  - **Defect:** the delta removed "These counts assume passes at least 1 ms apart". The Round 6 body says no count was left for it to qualify, but "one per pass" is a count, and it holds only for passes at least 1 ms apart.
  - **Why:** a held probe is re-armed to `now + 1` (`src/acmp.c:801`), and `acmp_timer_expired` sends it only once that deadline is due (`:1191`). With sub-millisecond passes, a pass inside the same millisecond owes no held probe. :90 still states the 1 ms condition for the re-arm.
  - **Why wording only:** no figure, test or command bound depends on it, and the condition is derivable from :90.
  - **Exact fix:** in :110, "…, one per pass for passes at least 1 ms apart, in the order …". Optionally, make the same change in :92. Pin the new phrase if :110's first sentence is pinned.

### SUGGESTION

- **S10 (new). Lenses: Docs. `docs/PORTING.md:110`, "so no command answer waits for it".**
  - The sentence is the ruling's and is true in its intended sense: the held probe never takes a slot a command offered in that pass could take.
  - A command that reaches the port after the probe was owed finds the probe among the frames owed ahead of it, like any owed frame. The command bound already counts that through n and the owed set.
  - Optionally add: "; a command that arrives after it is owed finds it among the frames owed ahead of it, which the command bound counts". This keeps a literal reader from taking the sentence as "a held probe never delays any later answer".
- **S7** (RV32 smoke step through the hold's boundaries) is still optional and was not taken. It is the same as R794's S8.

### Comment rule

- The delta adds one source comment, `// REQ: ACMP-12, ACMP-09` (`tests/test_acmp.cpp:3491`).
- A scan of every added line, and of both commit messages, finds no bench lane label, lane name, review round, reviewer ID or issue-comment ID. The `comments` and `privacy` gates pass.

## Prior public review findings at this head

| Finding | Source | Status at 376486b | Evidence |
|---|---|---|---|
| F5 MINOR (Docs, Tests): the held-probe bound and :92/:94 count only kept commands | R794-5 | **Resolved at its cause** (per the [A10] ruling) | The bound is removed. :92 and :94 use R794-5's wording, and :110 states the ruling's four statements, each checked against the code (focus 1, 3). The named assertion is added and fails under its plant, which escapes without it (focus 4). `probe_owed7` falls within the new text (focus 6). |
| RES8 RESIDUE: "past that" names only the retry | R793-5 and R794-5 | **Moot**: the clause was removed | `receipts/removed-clauses.txt` |
| RES9 RESIDUE: "with no probe held" dropped | R794-5 | **Resolved** | PR body Round 5 item 4 matches `probe_yields` and PORTING:96 |
| RES9 RESIDUE: integration note, gated-port condition | R793-5 | **Retained** (RES9 above) | `PR-BODY-rounds-2-3.md:85` |
| S7 / S8 SUGGESTION: RV32 smoke step | R793-4 / R794-4 | Not taken; optional | PR Round 6 item 4 |
| R793-4 F5, F6, RES7; R794-4 F4, S9 | R793-4, R794-4 | **Remain resolved** | The text these rely on (PORTING:85, :89, :95, :107, :109, :114) is unchanged or extended consistently. All 10 registered equivalents of my earlier plants are CAUGHT (`receipts/registered-reviewer-plants-caught.txt`). |
| R793-1 to R793-3 findings | earlier rounds | **Remain resolved** | The core is unchanged, and the Release image is byte-identical. |

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | No core change. The hold still delays only the two expiries that send a PROBE_TX (Milan v1.2 5.5.3.5.10, 5.5.3.5.16). A held probe's own TMR_NO_RESP runs from when it leaves (`probe_left`), so its response window is the specified one. Command answers keep their specified responses, never an error status (IEEE 1722.1-2021 8.2.4/8.2.5, Table 8-3), within the Table 5.26 timeouts at the unchanged budget. The ruling confirms that no Milan deadline depends on a held probe's wait. |
| RTL | CLEAN | No HDL in the delta, so the pinned Verilator was not needed. Applied to the bare-metal RV32 target: `baremetal.py` rc 0 in Debug and Release on a clean clone. The Release ELF is sha256 `f1fd4b902e73676c…` (50504 bytes) and `acmp.c.obj` is `ea582ee8…`. Both are byte-identical to rounds 3, 4 and 5 and to the author's `sizes-and-images.txt` (`receipts/baremetal-compare.txt`). |
| Robustness | CLEAN | Held probes are never lost across all probes (`probes_lost` 0 over 5600 and 6400 passes, and with 10 later commands). A held probe takes no slot a waiting command could take. The probes are unchanged from round 5. |
| Tests | CLEAN | 444/444 CAUGHT. The new test is needed: its plant passes the other 125 tests and fails the named assertion with both needles seen. No test was removed, and no remaining test asserts a removed clause. Coverage of `src/acmp.c` is 813/813 lines and 424/424 branches. The registration and sensitivity gates pass. |
| Docs | CLEAN (RES9, RES10, RES11 wording only) | PORTING :92, :94, :110 and :114, checked against code and probes; TESTS, TRACEABILITY and VERIFICATION counts and anchors; the `check_port_contracts.py` pins (8 new, 6 removed, 3 moved, 77 controls); the PR body Rounds 4 to 6 and the linked Round 2/3 file; the comment-rule scan. |

## Executed evidence (this review, exact head)

Pinned tool root `$VALIDATION_TOOLS` (`scripts/env.sh`: GoogleTest 1.14.0, clang-tidy 18, clang-18 lexer). Host GCC and Clang were used for the GCC and sanitizer arms, and riscv64-elf-gcc with QEMU for RV32. At most 16 jobs ran at once.

- **Gates:** `scripts/run_gates.sh` on the clean clone `scratch/clean`. It ran validate (12 jobs) and baremetal (4 jobs) concurrently, 00:39:54 to 00:44:18 (`receipts/gates/started.txt`).
  - `receipts/gates/validate.{out,rc}`: 28 × rc 0.
  - `receipts/gates/baremetal.{out,rc}`.
  - `receipts/gates/logs/`: every gate log and rc file, including `mutation.log` with summary `{"CAUGHT": 444, "ESCAPED": 0, "ERROR": 0}`.
- **New-plant escape check:** `scripts/plant_escape.sh`, output in `receipts/new-plant-escape.txt`.
- **Probes:**
  - `scripts/run_probe.sh`, `run_probe_j4.sh` and `run_probe_timer_ahead.sh` with the unchanged `probe_*.cpp`. Outputs and rc files are in `receipts/probes/`; all rc 0.
  - `probe_r3` + `probe_intermittent` were run as one concatenated insert, as in round 5 (`r3i.out`).
  - The external `probe_owed7.inc` was run with its own unchanged `run_probes3.sh`. The input hashes are in `receipts/probes/owed7-inputs.sha256`, and the output is `owed7-head.txt`.
- **Author evidence:** milan-fpga `bac9305f` is the branch tip (`git ls-remote`).
  - All 139 `author-r6/` entries of `MANIFEST.json` hash-match their published files, and no `author-r6` file is unlisted (`scripts/check_author_evidence.py`, `receipts/author-evidence-check.txt`).
  - `final/gates.json` has 28 entries, all rc 0. The `final/mutation.log` summary is 444/0/0. `final/validate.rc` and `final/baremetal.rc` are 0, and `probes/head.txt` is the exact head. These agree with my runs.
  - The author's `r3`, `r4`, `r4c`, `r5`, `r5b`, `timer-ahead` and `probe7` PROBE lines match mine.
- **Hosted CI at the exact head, inspected only** (`receipts/hosted-checks.json`, `hosted-runs.json`, `hosted-steps.txt`): push run `42536038937` and PR run `42536044188` both succeeded. In each, the quality and bare-metal jobs ran 7 steps, all successful, none skipped.
- **Clones** (`receipts/clone-state.txt`):
  - In the review clone and the clean clone, HEAD, index tree and HEAD tree equal `f4fd5321…`. All 98 files re-hash to their HEAD blobs, with mode 100644.
  - There are no gitlinks and no `.gitmodules`, and none is required.
  - The review clone has 0 untracked or ignored entries. In the clean clone, the gates wrote `scripts/__pycache__`, which I removed; it now has 0 entries.
  - All probes, plants and builds ran in exported copies under `scratch/`.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PORTING :92, :94 and :110 against `probe_yields`, `sm_expired`, `acmp_timer_expired`, `acmp_poll`, `probe_left` and the `acmp_rx` decline; Milan v1.2 5.5.3.5 and Table 5.26; IEEE 1722.1-2021 8.2.4/8.2.5 | R793-6 (delta). Untouched code keeps its R793-1 to R793-5 verdict | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| RTL | CLEAN | `baremetal.py` Debug and Release on a clean clone; Release ELF and `acmp.c.obj` against rounds 3 to 5 and the author | R793-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Robustness | CLEAN | Round 3, 4 and 5 probes unchanged; external `probe_owed7` unchanged; held-probe never-lost and slot-priority behaviour against the code | R793-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Tests | CLEAN | New test and plant (escape check, needles), full campaign 444/0/0, coverage, registration, sensitivity, no removed test or plant, registered reviewer plants CAUGHT | R793-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |
| Docs | CLEAN (RES9, RES10, RES11 wording only) | PORTING owed-bound section, TESTS, TRACEABILITY, VERIFICATION, `check_port_contracts.py`, PR body Rounds 4 to 6, linked Round 2/3 file, comment-rule scan | R793-6 | 376486b374782147d71e5e9bb4f93c42cd10e636 |

## Real limits

- This is a delta review. Code the delta does not touch keeps its earlier verdicts. I did not re-derive the unchanged command bound beyond re-running the probes.
- No manager source bank runs at this exact head, and I claim none. Source-head execution evidence is my own clean-clone gates plus the author's published receipts.
- Hosted CI was inspected, not owned. Hosted/act acceptance belongs to the manager.
- Physical calibration was NOT RUN. Field skips and the RV32 QEMU smoke are not hardware proof.
- RTL lens: there is no HDL in this repository's delta. The pinned Verilator was not used.
- The Debug RV32 ELF differs from earlier rounds by build path only, as before. Only the Release image is compared byte for byte.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (builder and native banks) against live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`, from source base `70936b77`, and link its receipts on the PR.
- Own hosted/act acceptance.
- Carry RES9, RES10 and RES11 to the residue checklist.
- The parent firmware harness row for issue #26 still needs the parent to adopt this head. Issue #26 stays open, as the PR body states.

R793-6 FINISHED
