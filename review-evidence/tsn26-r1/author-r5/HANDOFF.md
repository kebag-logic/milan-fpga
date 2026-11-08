# [A750f] HANDOFF: tsn-c-stack issue #26 (ACMP owed bound), round 5

Status: REVIEW READY at 715d20804fd3438edf990c393bf1b0c6e328dede. All 28 gates and `baremetal.py` (Debug and
Release) return 0 on a clean clone of that head.

- Repository: kebag-logic/tsn-c-stack, PR #28, branch `26-acmp-owed`.
- Start head: a0a32110511e444a23848367b7cbb4231e16ce5a (round 4, pushed).
- Round 5 adds four commits. There was no rebase, force or amend. Each commit is authored and committed by
  hackerman-kl <hackerman-kl@kebag-logic.com> and has a one-line subject with no body or trailers.
  1. `8d6786f` Require the port to offer its waiting ACMP frames in arrival order after each accepting poll until
     one is declined, before timer service, and say that the test port does so (step 1: R793-4 F5)
  2. `af31233` State the kept command's answer pass as n + 1 + f + r, n the frames owed when the egress returns,
     and assert ACMP_OWED_MAX + f for every command kept behind seven owed frames (step 2: R794-4 F4)
  3. `7960ef7` Say that a held retry is also cancelled when its earlier probe is answered, and that the
     one-per-sink count needs no probing restart and a wait under TMR_NO_RESP (step 3: R793-4 F6, R794-4 S9,
     R793-4 RES7)
  4. `715d208` Say in ACMP-12 and the change log that timer probes are held only while a BIND_RX waits with one
     slot free (step 4: found in the final re-check)
- No core change: `git diff --stat a0a3211 715d208 -- src include examples` is empty.
- Files changed (10): CHANGELOG, PORTING, REQUIREMENTS, VERIFICATION, the generated TESTS and TRACEABILITY,
  `scripts/check_port_contracts.py`, `scripts/test_inventory.py` (the TESTS header sentence), `tests/test_acmp.cpp`
  and `tests/mutations.json`. In all: +161/-18.
- Not pushed, and no PR was opened or edited. The PR text is in `PR-BODY.md`: the current body, corrected in place
  where round 5 changes a figure, plus a Round 5 section. Its first line is "[A750f]" and it says "Relates to #26".
- Issue #26: "[A750f] TAKEN" was posted at the start. "[A750f] REVIEW READY 715d208…" was posted at the end.

## Findings addressed

| Finding | Disposition |
|---|---|
| R793-4 F5 (the bound assumes the port offers its whole backlog) | Option (a). `docs/PORTING.md:85` states the obligation in R793-4's own words: after each accepting `acmp_poll`, the port offers its waiting ACMP frames in arrival order, the kept one first, until `acmp_rx` declines one or none is left, and only then services `acmp_timer_expired`. `:89` says what offering fewer costs. Three phrases are pinned in CRITICAL, among them "until `acmp_rx` declines one or none is left" (`scripts/check_port_contracts.py:289-290`). TESTS (`scripts/test_inventory.py:47`, `docs/TESTS.md:9`) says the fixture's `pass()` does this. The comment rule allows no prose in the fixture. The CHANGELOG, the PR What section, Round 4 item 1 and Round 5 also say it. |
| R793-4 F6 (one-per-sink needs the wait under TMR_NO_RESP) | `docs/PORTING.md:110` adds "and the held probe has waited less than TMR_NO_RESP (200 ms); past that, another sink's TMR_NO_RESP retry can also be owed before it". The same condition is in PR Round 4 item 3 and Round 5 item 3. Both phrases are pinned. |
| R794-4 S9 (name the restart paths) | Taken in the same sentence (`:110`), using S9's "probing restarts" and its two paths, an ADP re-advertisement that does not raise the available index and `acmp_tk_unregistered`. The re-check found a third path, a new discovery after the talker departs or its advertisement times out (`src/acmp.c:612-619`, `:665-666`, `:686-693`, `:1187-1189`). It is named as well (see the re-check below). `:114` (gated port) uses the same term, "probing restarts", so that the two sentences agree. |
| R794-4 F4 (stated pass one too high from seven owed) | Option (a), the exact form. `docs/PORTING.md:107` reads: "leaves in pass n + 1 + f + r, where n, `ACMP_OWED_MAX` or one less, is the number of frames owed when the egress returns (one less only when the first kept frame is a BIND_RX declined with one slot free)". `:109` reads: "leaves in pass n + 1 (`ACMP_OWED_MAX` + 1 from a full set)". `CHANGELOG.md:6` and the PR body (What, Round 3 "Result", Round 4 item 1, Round 5) say the same. CRITICAL re-pins the changed phrase and adds three (`:308-311`). The budget sentences are unchanged: they use `ACMP_OWED_MAX` for n, which the PR body now points out. A new test and plant cover the change (below). |
| R793-4 RES7 (cancel by a response) | All three of the reviewer's wording fixes are taken: `docs/PORTING.md:95`, the counter row `:350`, and PR Round 4 item 3. The new clause is pinned (CRITICAL) and tested (`AnsweredProbeEndsTheHoldOfItsRetry` and its plant), because the sentence map requires every core clause to be pinned. |
| R793-4 S7, R794-4 S8, R793-4 S8 | Not taken, as instructed. The PR Round 5 section lists them. |

## Changes (file:line at 715d208)

- `docs/PORTING.md`:
  - `:85` the offering obligation (F5).
  - `:89` the cost of offering fewer frames (rationale; R793-4's port "one").
  - `:94` "its sink's probing does not advance until the probe is owed or cancelled" (re-check; see below).
  - `:95` and `:350` RES7.
  - `:107` and `:109` n + 1 + f + r and n + 1 (F4).
  - `:110` the F6 condition and the restart paths (F6, S9).
  - `:114` "probing restarts".
- `docs/REQUIREMENTS.md:44` ACMP-12 prose: "While it waits with one slot free, timer probes …" (re-check).
- `CHANGELOG.md:6` the offering obligation, "while it waits with one slot free", and n + 1 + f + r.
- `docs/VERIFICATION.md:24` 439 core plants.
- `scripts/check_port_contracts.py:289-290` and `:301-311`: 13 new phrases and one re-pinned phrase. The
  self-test refuses 74 meaning-removal controls, up from 61.
- `scripts/test_inventory.py:47`: the generated TESTS header now describes the fixture's `pass()`.
- `tests/test_acmp.cpp:3398` `KeptCommandsBehindSevenOwedLeaveOnePassSooner`, `:3457`
  `AnsweredProbeEndsTheHoldOfItsRetry`. Neither uses a prose comment; each carries only `// REQ: ACMP-12, ACMP-09`.
- `tests/mutations.json:2642` `owed-bind-wait-only-on-a-second-decline` and `:2727` `owed-answer-keeps-the-hold`.
  That makes 443 plants: 439 core and 4 generated.
- Generated: `docs/TESTS.md` (174 declarations, 443 plants) and `docs/TRACEABILITY.md` (46 requirements, 174
  test declarations). The coverage ratchet is unchanged (`src/acmp.c` 813/813 lines, 424/424 branches).
- ACMP binary: 125 tests (124 ACMP plus main's Wire test), up from 123.

## Tests and the planted mutants they kill

| Test | Proves | Plants it kills (registered) | Escape without it |
|---|---|---|---|
| `KeptCommandsBehindSevenOwedLeaveOnePassSooner` | The egress returns with 7 owed: either 7 GET_RX_STATE, or 5 plus a taken BIND_RX. Kept behind: a BIND_RX declined with one slot free, a GET_RX_STATE and a second new binding. In the hold, two refused passes run, with and without redelivery, and a retry falls due and is held. After the return, `bind_waiting` is set and the answers leave in passes 8, 10 and 11 = `ACMP_OWED_MAX` + f. The held retry leaves in pass 13 = `ACMP_OWED_MAX` + F, and nothing is lost. | `owed-bind-wait-only-on-a-second-decline` (needles "from seven owed each kept command leaves in pass ACMP_OWED_MAX + f" and "the egress returns with seven owed") | Escapes: it passes all 124 other tests (rc 0). It also fails under 23 other plants, each with other killers (`receipts/per-test-escape.json`). |
| `AnsweredProbeEndsTheHoldOfItsRetry` | The answer to the earlier probe of a held retry waits behind the kept BIND_RX. Once taken, it ends the hold. A failure status gives PRB_W_RETRY, TMR_RETRY and `acmp_status` = the status; SUCCESS gives SETTLED_NO_RSV and TMR_NO_TK. The retry is never sent, held again or lost. | `owed-answer-keeps-the-hold` (needle "an answer to the probe a held retry repeats ends the hold") | Escapes: it passes all 124 other tests (rc 0). It also fails under 14 other plants, each with other killers. |

Plants:

- `owed-bind-wait-only-on-a-second-decline` adds `&& a->busy_declined > 1u` to the `bind_waiting` condition
  (`src/acmp.c:1100`). So `bind_waiting` is set only once some command has been declined before, as if every
  waiting BIND_RX had first met the full set. That is the n = 8 assumption behind F4.
  - Effect: at seven owed in the hold, the retry is owed into the last slot. The egress returns with eight owed,
    and the BIND_RX waits an extra pass (9 instead of 8). The GETs follow at 11 and 12.
  - Why this form: from seven owed, the core passes through the same state as the eight-owed start after its
    first pass, so a mutant that delays only the seven-owed start must key on history. `busy_declined` is the
    history that two existing plants already use.
  - Candidate runs are in `scripts/cand_plants.py` and `scripts/candidate-plant-*.json`.
- `owed-answer-keeps-the-hold` keeps `probe_held` across `sm_stop` in `probe_response` (`src/acmp.c:965`).
- Both plants were tried on a scratch copy before registration: full suite rc 1 with only the new test failing,
  rc 0 without it. They are CAUGHT in all three campaigns that include them (s3 and s4 step runs, final).

Escape evidence on the final campaign's binaries (`receipts/escape-final.json`, `.txt`; 125 tests each):

- 62 plants were checked: 53 `owed-*` plus the nine ACMP plants the owed-bound map uses.
- Every one fails the full binary and passes (rc 0) once its failing tests are excluded.
- With only the two round 5 tests excluded, exactly the two round 5 plants pass.

## Every sentence, re-checked against the code (`map/`)

- I read every sentence of PORTING "ACMP owed bound" (`:76-118`), the ACMP-12 prose and the ACMP-12 row again
  against `src/acmp.c`.
  - The decline is at `:1086-1103`, the hold at `:778-804`, the poll at `:1254-1272`, `bind` and `unbind` at
    `:848-903`, `probe_response` at `:948-980`, discovery at `:583-693`, timer service at `:1172-1196` and SRP at
    `:1198-1239`.
  - Every place that clears `probe_held` was traced: `sm_stop` callers and `sink_reset`.
- The re-check covered the port behaviours the contract allows:
  - after a refused poll, waiting or delivering again;
  - after an accepting poll, offering until a decline;
  - the gated port that tests `acmp_rx_ready`;
  - frames that arrive during a pass, which join the backlog only while it is non-empty.
- Three more inaccuracies were found and fixed:
  1. S9's two restart paths miss one. A sink can owe a second probe within 200 ms when its talker departs
     (ENTITY_DEPARTING, `:686-693`, or ADP valid-time expiry, `:1187-1189`) and is discovered again. Rediscovery
     arms a new TMR_DELAY (`:604`) with a draw from 0 ms. `:110` names it.
  2. `:94` said a held probe's sink does not advance "until the probe is owed". An answer to the earlier probe of
     a held retry also advances it (RES7), so the sentence now ends "or cancelled". The pinned phrase is kept as a
     substring.
  3. ACMP-12's prose (`docs/REQUIREMENTS.md:44`) and the CHANGELOG said "While it waits, timer probes of any sink
     are held, never lost". A BIND_RX declined with no slot free also waits, and a probe that falls due then is
     lost (`:1099-1103`, PORTING `:95`, `BindDeclinedBehindTheFullSetHoldsNoProbe`). Both now say "while it waits
     with one slot free", as the requirement row does.
- Noted, not changed (outside the F6 scope): the gated-port count (`:114-115`) relies on the frame waiting less than
  TMR_NO_RESP after the egress returns. Any port that meets the 200 ms command timeout satisfies that, as R793-4
  said for this sentence.
- `map/sentence_map.py` (round 5) and `map/check_map.py TREE CAMPAIGN ESCAPE OUT`, on the clean clone with the final
  campaign and escape evidence: "66 sentences and clauses, 50 core, 55 distinct plants". The checker reports
  "map: every sentence mapped; every core sentence pinned by a registered, caught plant" (`map/check-final.txt`,
  table `map/map-final.md`).
  - The new PORTING obligation is classed as a port obligation. It is pinned through its effect: both kept-backlog
    tests and their plants.
  - The cost of offering fewer frames is classed as rationale. Its evidence is R793-4's port-"one" probe.

## Reviewers' round 4 probes, unchanged, at 715d208 (`receipts/probes/`)

Inputs are listed by sha256 in `receipts/probes/inputs.sha256`. The internal review's runner exports the clean
clone's commit, and the external review's runner takes a `git archive` of it.

- `probe_r4.cpp` + `probe_r4b.cpp` (`probe-r4-r4b.txt`), `probe_r4c.cpp` (`probe-r4c.txt`) and `probe_owed6.inc`
  (`probe-owed6.txt`) each end with `PASSED` and rc 0.
- Every PROBE line is byte-identical to the review's own receipt, because the core is unchanged.

Each output falls within the corrected sentences:

| Probe output | Corrected sentence it meets |
|---|---|
| r4/r4b port "all": every answer at the formula (9, 10). At 189 ms, 198 and 199 ms; at 190 ms, 200 ms | `:107` n + 1 + f + r with n = 8; `:112-113` budget |
| r4/r4b port "one": one pass late (pass 11 or 12; 201 ms at 189 ms) | Excluded by `:85`, which this port breaks by offering one frame per poll; `:89` gives the cost |
| r4 "get,foreign,get": retry lost, `probes_lost` 1 | `:96` (no probe held, no BIND_RX waiting: lost) |
| r4c sustained: sink 2's probes leave in passes 11 and 250, sink 3's held retry in 251, none lost | `:110` past TMR_NO_RESP, another sink's retry can also be owed before it |
| r4c failure-response: `probe_held` 1 → 0, PRB_W_RETRY, ACTIVE, TMR_RETRY | `:95` (cancelled when a held retry's earlier probe is answered), `:94` (or cancelled) |
| owed6 eight owed: 9, 11, 12 | `:107` n = 8 |
| owed6 seven owed (both constructions): 8, 10, 11, `probes_lost` 0. Its "stated" column is its own hard-coded round 4 figure | `:107` n = 7 (f = 0, 2, 3); `:109` n + 1 = 8 |

Both reviewers' round 4 plant scripts were also run unchanged (`receipts/reviewer-scripts/`):

- R793-4 `run_reviewer_plants.sh`: all eight `rv-` plants fail at least one of 125 tests. As before, the
  "ESCAPED" lines come from the script's `--discover` step, which uses a placeholder killer.
- R794-4 `escape_check4.py`: unplanted, 125 of 125 pass. Each of the five plants fails the full binary, and every
  registered needle is SEEN.

## Boundary evidence (asserted at 715d208, 1 ms passes)

| Case | Result |
|---|---|
| Seven owed at return, BIND_RX + GET + new binding kept, retry held in the hold, with and without redelivery | Answers in passes 8, 10 and 11; retry in pass 13; nothing lost |
| The same start under `owed-bind-wait-only-on-a-second-decline` | The retry is owed in the hold; eight owed at return; passes 9, 11 and 12 (the test fails) |
| Full set (round 4 tests, unchanged) | 9, 11, 12, 13, 14, 15, 16, 18; held probes at 19-22 |
| Answer to a held retry's earlier probe, failure and SUCCESS | Hold ends; PRB_W_RETRY/TMR_RETRY or SETTLED_NO_RSV/TMR_NO_TK; retry never sent |

## Gate table (Linux hosted and bare-metal RV32)

Toolchain:

- GoogleTest/GMock 1.14.0 from the pinned prefix.
- Host GCC and Clang for the hosted arms.
- Clang 18.1.3 and clang-tidy 18.1.3 first on PATH.
- Mermaid CLI 11.16.0 with Node 22.11.0 in scratch.
- riscv64-elf-gcc and QEMU for RV32.

Each step copied the lane's exact working tree to scratch (`scripts/run_step.sh`). It then ran
`python3 scripts/validate.py --work <w> --jobs 16 --graphs` and `python3 scripts/baremetal.py --work <w> --jobs 8`
concurrently. `git status` and the diff sha256 matched before and after each run and matched the lane at commit
time. The final run used a clean `git clone --no-local` of 715d208 (`scripts/run_final.sh`).

| Gate | s1 tree (8d6786f) | s2 tree (af31233) | s3 tree (7960ef7) | s4 tree (715d208) | Final, clean clone 715d208 |
|---|---|---|---|---|---|
| 17 source and metadata gates (entity-golden … privacy) | all 0 | all 0 | all 0 | all 0 | all 0 |
| port-contracts self-test controls | 64 | 67 | 74 | 74 | 74 |
| privacy | 0 | 0 | 0 | 0 | 0 (35 commits, 381 historical blobs, 98 files) |
| gcc configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| coverage | 0 | 0 | 0 | 0 | 0 (acmp.c 813/813, 424/424) |
| clang-sanitizers configure / build / test | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| static-analysis | 0 | 0 | 0 | 0 | 0 |
| mutation | 0 (441 caught) | 0 (442 caught) | 0 (443 caught) | 0 (443 caught) | 0 (443 caught, 0 escaped, 0 error) |
| mutation-controls, graphs | 0, 0 | 0, 0 | 0, 0 | 0, 0 | 0, 0 |
| `baremetal.py` Debug, Release | 0, 0 | 0, 0 | 0, 0 | 0, 0 | 0, 0 |

No gate run failed in this round.

Receipts:

- `receipts/final/` holds the final run on the clean clone:
  - all 28 gate logs and rc files, `gates.json` and `validate.log`;
  - `baremetal.log` and `rv32-results.json`;
  - the head, and the clone's status and diff hash before and after;
  - `campaign-summary.json`, with name, status and failing tests for all 443 plants. The full `results.json`
    (973658 bytes) is recorded by sha256 in `receipts/not-copied.sha256.txt`.
- `receipts/steps/`:
  - For each step: its 28-line validate summary and rc, its bare-metal log (which includes the RV32 results) and
    rc, and its tree's head, status and diff hash before and after.
  - For s4 also: `gates.json` and the mutation log.
  - The s1-s3 work directories were deleted to free space after their gates passed. Their per-gate logs are not
    kept, but every rc is in the summaries.
- `receipts/escape-final.*`, `per-test-escape.json`, `sizes-and-images.txt`, `probes/` and `reviewer-scripts/`.
- `scripts/`: the step and final runners, the candidate-plant runner and candidates, `escape5.py`,
  `per_test_escape5.py`, `imgx.sh`, `imgsize.sh`, `pr_body5.py` and `publish.py`.
- Host paths in receipts are replaced by `<scratch>`, `<clone>`, `<reviews>`, `<tools>` and `<lane>`.

## Bare-metal image size, memory and cost

a0a3211 and 715d208 were exported to paths of equal length (`xa`, `xb`) and built with `scripts/baremetal.py`
(`receipts/sizes-and-images.txt`):

| Build | a0a3211 (before) | 715d208 (after) |
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
| Past the bound the entity still answers every command; bound and behaviour stated in the docs | Met in the core for a port that follows the contract | PORTING now states the offering obligation the bound needs, the exact pass from either start, and the held probe's conditions |
| A test fills the owed set with the egress held, sends a further command, answered within its timeout after the egress returns | Met | Round 2-4 tests, plus the seven-owed start |
| A planted mutant restoring the silent drop is caught | Met | 443 of 443 caught |
| milan-fpga's harness row "an ACMP command behind the owed input" gets an answer time | **Not met here** | The parent must adopt this head. Round 5 changes no source, so no parent fragment moves. |

Hence "Relates to #26".

## Environment notes

- Scratch: `$VALIDATION_STORAGE/tsn26-a750f/` holds:
  - the clean clone (`clone`) and the final gate work (`val-final`, `rv32-final`);
  - `val-s4` and `rv32-s4`, and the image exports and builds (`xa`, `xb`, `xa-rv32`, `xb-rv32`);
  - the probe and reviewer-script work (`probes`, `rev`) and the dev copy (`dev`, `dev-build`);
  - Node, the Mermaid CLI and Puppeteer's cache, copied from round 4's scratch.
- Memory: the unit's peak was 8.08 GB (memory.peak), most of it page cache, during the final gates; it was
  4.4 GB at the end. That is under the 9 GB target.
- The lane's ignored `build-registration/` predates this session and was not used. Inventory and traceability
  were regenerated with `--build` in scratch, and `scripts/__pycache__` was removed before each commit.
