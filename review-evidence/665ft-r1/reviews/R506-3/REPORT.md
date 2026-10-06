[R506] POSITIVE - exact head 6ca834a782a1bd5574d44998c8e214cf16df3441

# R506-3: internal cleared-context re-review of PR #675 (issue #665, lane FT)

- **Head under review:** `6ca834a782a1bd5574d44998c8e214cf16df3441`, tree `79a9a6b116e9b839e744af76960a10588381a1bb`.
- **Source base:** `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
- **Round:** R506-3. Its delta is the three commits on `e7e0c10f`: `7a2686ae`, `89b02c7f` and `6ca834a7`. It is reviewed against the round-3 assignment (issue comment 6014362247) and against my own R506-2 findings F1 to F3 (PR comment 6014356451).
- **Delta files:** six, all test, test-data or README files (`receipts/delta_scope.txt`):
  - `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp` and `nvm_mutants.py`;
  - `sw/firmware/ctrl_nvm/README.md`;
  - `sw/firmware/gtest/tally_cases.cpp` and `tally_selftest.py`;
  - `sw/firmware/gtest/README.md`.

  The delta changes no firmware source, RTL, bench, workflow, script, builder or shipping-image file. All three commits are one line long with no trailers.
- **Lenses:** all five were applied independently: Conformance, RTL, Robustness, Tests and Docs.
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the issue #665 body, the unit-test directive (6008744385), the FT assignment (6009234414), and the round-2 (6012062072) and round-3 (6014362247) assignments;
  - #678 and its ruling: ports never call back into the core synchronously;
  - the author's round-3 TAKEN and REVIEW READY comments (6014399613, 6015346011);
  - the public headers `adp.h` and `nvm_klj2.h`, and the code behind them (`adp.c`, `adp_mbx.c`, `nvm_klj2.c`, `fw_gtest_main.cpp`);
  - `git diff 423ac5d9..6ca834a7` and its history, with the round-3 delta `e7e0c10f..6ca834a7` read line by line;
  - executable evidence, run here at the exact head, and the hosted run at this head.
- **Order of reading:** I read the prior public findings only after my own pass over the delta and its probes was complete. Those findings are my own R506-2 report and the other reviewer's R507-2 report, which was POSITIVE with one residue.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open.
- Each of R506-2's F1, F2 and F3 is resolved at this head. Each was verified by my own probe as well as by the gates.
- Two SUGGESTIONs and one RESIDUE remain. None of them affects the verdict or any lens.

## Prior public findings at this head

| Finding | Lenses | Disposition at `6ca834a7` |
|---|---|---|
| R506-2-F1, the loaded-prefix guard not pinned at the exact header end | Conformance, Robustness, Tests | **RESOLVED.** See "F1 resolution" below. |
| R506-2-F2, the README's exclusion standard was stated as met while the ADP rows rest on an unstated port premise | Conformance, Tests, Docs | **RESOLVED.** See "F2 resolution" below. |
| R506-2-F3, four listener behaviours not planted, four defects escaping | Tests, Docs | **RESOLVED.** See "F3 resolution" below. |
| R506-2-S1, name the omitted erased-record case in the tree | Docs | **RESOLVED.** `test_nvm_codec.cpp:86-89` names the case left out and cites #677. |
| R506-2-R1 / R507-2-R1, stale hosted status in the PR body | Docs (RESIDUE) | **RETAINED** as R1 below. The round-2 hosted run is now attributed correctly. The sentence about the round-3 head is now stale. |
| R506-1 and R507-1, all findings | (as published) | Resolved at R506-2. Nothing in this delta touches them. The coverage gate (`fw_coverage.py`, `coverage.ratchet`) is unchanged, and its `--check` and `--selftest` pass here. |

### F1 resolution: the guard is pinned at its exact ends

The test is `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:90-131`. For every record of the container of frames, it builds a copy whose record header claims a payload one byte past the container's end. It then reseals the copy, so `nvm_klj2_check` gives `NVM_VD_LEN`, not `NVM_VD_CRC` (`:117`). With that copy:
- at `loaded` = one byte short of the header's end, the guard at `nvm_klj2.c:350` refuses it `NVM_VD_REC` (`:119`);
- at `loaded` = the header's exact end, the result is `NVM_VD_LEN` (`:121`).

Only a guard that passes there can reach `NVM_VD_LEN`. I checked this against the code: the earlier `pos + NVM_REC_HDR > end` test (`:346`) cannot fire at an interior header, so `VD_LEN` can only come from `nvm_klj2_record:306`, after the guard has passed. The payload guard at `:312` is pinned the same way on the last record: `VD_REC` one byte short (`:125`), and `VD_OK` at the exact end (`:127`).

That is the only place the payload guard can be seen in the verdict. For a record that is not the last, the next header's guard returns the same `VD_REC` whatever the payload guard does.

Evidence:
- `receipts/ctrl_nvm_selftest.log`, rc 0: 5 shapes, 434 tests, and "all 106 planted defects reddened". The four new defects are each killed by `codec_loaded_prefix` at the intended assertion:
  - `header_guard_early` fails at "at record 0's header's exact end ... VD_LEN";
  - `header_guard_late` fails at the resealed "one byte short" assertion. The plain one-byte-short assertion on the unmodified container cannot tell that defect apart, because the payload guard would refuse there anyway;
  - `payload_guard_early` fails at "the last record's payload's exact end is accepted";
  - `payload_guard_late` fails at "one byte short of the last record's payload".
- R506-2's own probe, `scripts/r506_2_guard_ge_probe.sh`, was run unchanged from a copy. It plants `>=` on the header guard and runs the whole store gate. It now exits 1, and every one of the 5 shapes fails, only in `NvmCodec.codec_loaded_prefix` (`receipts/r506_2_guard_ge_probe.log`, `.rc`).
- The public contract (`nvm_klj2.h:106-109`) and `nvm_klj2.c` are unchanged by the delta.

### F2 resolution: the ADP rows are marked as resting on #678, and their reach is stated

- **The standard sentence.** `sw/firmware/gtest/README.md:216-219` now says that nine rows meet the standard through their headers as they stand. It says the five `adp.c` rows do not yet, because they rest on a port rule that `adp.h` does not state and that #678 has ruled. The table has 14 rows: 5 in `adp.c` and 9 elsewhere.
- **The premise paragraph.** `README.md:262-296` cites #678, says the rows rest on the ruling until its F0 follow-up lands, and ends with "`adp.c`'s 100 % holds for ports that keep #678's rule, and not for a port that breaks it". The 100 % is therefore no longer claimed unconditionally.
- **The adapter claim** ("its ports call no core function") holds:
  - `adp_mbx.c:16-54` calls only `mbx_*` driver functions;
  - `mbx/mbx.c` and `mbx/mbx.h` hold no callback;
  - the core is called only from `on_frame`, `on_timer`, `on_event`, `on_poll` and `adp_mbx_set_enable`.
- **Row-by-row reach, measured independently.** My own probe, `scripts/adp_reentry_r3.c` with `adp_reentry_r3.sh`, builds the head's `adp.c` under gcov once per scenario and reads each named statement's arcs in gcov's order (`receipts/adp_reentry_r3.log`, rc 0):

  | Scenario | Arcs and lines reached | State left |
  |---|---|---|
  | A1, link-down from inside the ENTITY_AVAILABLE send, then a link-up | `adp.c:208` arc 2 of 2 (row 1) | WAITING, link recorded down, TMR_ADVERTISE running, no DELAY entered |
  | A2, the same from inside SHUTDOWN's DEPARTING send | `:213` arc 2 of 2 (row 2) | as the README says |
  | B1, TMR_ADVERTISE expired inside `timer_start` | `:236` arc 4 (row 3); `:238` arc 2 (row 4); stray line `:241` | WAITING, no timer |
  | B2, TMR_DELAY expired inside `timer_start` on a grandmaster change | `:238` arc 4 (row 4); stray line `:241` | DELAY, no timer |
  | C1, a link port calling back twice from inside `adp_set_enable(true)` | `:274` arc 4 (row 5); line `:277` | DOWN with an ENTITY_AVAILABLE owed |
  | C2, as C1, then `adp_set_enable(false)` | `:274` arc 2 (row 5); line `:277` | as the README says |

  Each row matches the README's bullets at `:276-293` item for item. That includes row 5, which my R506-2 probe had not reached.
- **R506-2's probe** (`scripts/r506_2_adp_reentry_probe.py`) still reproduces rows 1 to 4 (`receipts/r506_2_adp_reentry_probe.log`).
- **PR body.** Its Known limitations bullet carries the same row-by-row reach and the #678 citation. The firmware is unchanged, as the assignment requires.

### F3 resolution: the listener behaviours are planted, and their defects are caught

- **The new planted cases.** `tally_cases.cpp` adds:
  - `Crash.Bus`, `Crash.Fpe` and `Crash.Ill` (`:59-69`);
  - `DISABLED_Suite.NeverRuns` (`:91`);
  - `TearDownFails` (`:104-111`);
  - `ProgramFails`, with a global environment whose set-up fails only under the filter `ProgramFails.*` (`:29-39`).
- **The cases are held to their tally lines.** `tally_selftest.py:87-100` holds each case to its exact tally line, its `RESULT` line, its grade, the test its `[FAIL]` line names, and `suite_tally.py --verdict`.
- **The new defects.** Seven new defects (`:121-175`) are added, and one is widened:
  - each of the five signals dropped from the handler's list;
  - `program-failure-not-counted`;
  - `disabled-suite-not-counted`;
  - `suite-failure-not-counted`, which now also names `TearDownFails`.
- **Every named case must be red.** The campaign requires every case a defect names to read otherwise than planted (`campaign`, `missed`).
- **Results here** (`receipts/tally_selftest_mutants.log`, rc 0): 18 of 18 cases and 18 of 18 defects. The exits seen match the README's Exit column: -7, -8 and -4 for the three signals; 1 for the tear-down and program cases; 0 for the disabled suite.
- **The tally line itself is caught.** `program-failure-not-counted` is caught on the tally line: checks 1, failures 0, where 1/1 is wanted. `result-always-pass` is caught on `TearDownFails.*` and `ProgramFails.*`, so a tally line that lies is caught there, not only by the `[FAIL]` marker.
- **R506-2's probe.** `scripts/r506_2_tally_extra_plants.py`, run unchanged, now shows each of its four defects (SIGFPE, SIGBUS, program failure, disabled suite) reddening the clone's own planted cases (`receipts/r506_2_tally_extra_plants.log`, rc 0).
- **Hosted.** The `firmware-unit` job at this head reports "tally self-test: 18 of 18" on GoogleTest 1.14.0 and gcc 13.3.0 (`receipts/hosted_firmware_unit_job_6ca834a7.txt`).
- **The README** (`:50-110`) lists the planted set and the 18 defects, and they match the code.

## Findings

### S1 SUGGESTION: the tally self-test does not assert a crash case's exit status, so the handler's re-raise is unpinned

- **Lens:** Tests.
- **Where:** `sw/firmware/gtest/tally_selftest.py`, `grade_case`; `sw/firmware/gtest/fw_gtest_main.cpp:99-100`; the Exit column of `README.md:78-97`.
- **Evidence:** `scripts/tally_extra_plants_r3.py` plants `crash-no-reraise`, a handler that prints the failing tally and then calls `_Exit(0)` instead of re-raising. All five crash cases still read as planted (`receipts/tally_extra_plants_r3.log`; rc 1 is the probe reporting the escape). The grade stays red because the tally line says FAIL, and the README names only the tally line and the verdict as what each case proves (`:70-76`). So no claim is false and no verdict changes.
- **Suggestion:** assert each case's exit status: a negative signal number for the crash cases, as the Exit column records. A handler that stops dying of its signal would then redden the self-test.

### S2 SUGGESTION: a listener whose suite loop skips the last-registered suite escapes, because no suite-level failure is planted in that position

- **Lens:** Tests.
- **Where:** `fw_gtest_main.cpp:173-179`; the suite order in `tally_cases.cpp`, where `ProgramFails` is registered after `TearDownFails`.
- **Evidence:** the defect `suite-loop-drops-last` (`k + 1 < unit.total_test_suite_count()`) leaves `TearDownFails.*` reading as planted. `suite-loop-tail-only`, its counterpart, is caught (`receipts/tally_extra_plants_r3.log`). The other probe plants were all caught: `program-fatal-only`, `crash-reported-inverted` and `disabled-suite-by-test-only`.
- **Suggestion:** register one suite with a set-up or tear-down failure last, or plant a second such suite at the end. The loop's bounds would then be pinned at both ends.

### R1 RESIDUE (wording only, retained from R506-2-R1 / R507-2-R1): the PR body says the round-3 head has no hosted run

- **Lens:** Docs.
- **Where:** the PR #675 body. The Status section ends "The round-3 head has no hosted run yet." The Known limitations bullet says "The round-3 head has no hosted run".
- **Why it is stale:** hosted `rtl-fast` run 37457222400 at `6ca834a7` completed with success. It ran on the PR merge ref with dev `bd884631`, and its `firmware-unit` job 112247900469 passed. `rtl-full` 37457223191 and `elaborate` 37457222273 were still running at the 11:56:01 UTC snapshot, and Physical gPTP was skipped (`receipts/hosted_checks_snapshot.txt`).
- **Exact fix (Status):** replace "The round-3 head has no hosted run yet." with "At the round-3 head, hosted `rtl-fast` run 37457222400 (PR merge ref with dev `bd884631`) passed, including `firmware-unit` job 112247900469; `rtl-full` and `elaborate` were still running at the 2026-10-06 11:56 UTC snapshot."
- **Exact fix (Known limitations):** replace "The round-3 head has no hosted run" with "At the round-3 head `rtl-fast` run 37457222400 passed, including `firmware-unit`".

## Clean lenses, in findings format

`[R506] PASS Conformance - test_nvm_codec.cpp:90-131 against nvm_klj2.h:106-109 and nvm_klj2.c:306-313,346-351; nvm_mutants.py:149-158; README.md:209-296 against the #678 ruling and adp.h:129-145; tally_cases.cpp and tally_selftest.py:79-175 against README.md:50-110 and fw_gtest_main.cpp:126-199 - round-3 items 1 to 3 met as assigned: the header guard is refused one byte short and passes at its exact end (VD_LEN, reachable only past the guard), with off-by-one defects in both directions killed; the five adp.c rows are marked as resting on #678, with each row's reached arcs stated, and the 100 % is stated conditionally; every listener behaviour the README names is planted, and its defect turns the run red, including the tally-line falsifiers. The public contract and the firmware are unchanged.`

`[R506] PASS RTL - receipts/delta_scope.txt (git diff e7e0c10f..6ca834a7 over hdl, tb, configs, sw/builder, sw/litex, syn, .github, scripts, the submodules and every firmware .c/.h: empty); receipts/mbx_bench_head.log - the delta touches no RTL, bench, configuration, workflow or firmware source; the mailbox bench was rerun at the exact head in a disposable clone with the scoped Verilator 5.050 (identity "Verilator 5.050 2026-07-01 rev v5.050"): AXI4-Lite 179, Wishbone 134, cosim 13, mbx mutants 4 of 4, rc 0; the adapter's ports call only mbx_* driver functions, with no callback (adp_mbx.c:16-54, mbx/mbx.c).`

`[R506] PASS Robustness - nvm_klj2.c:306-313,346-351 boundary behaviour at loaded = header end -1/0 and payload end -1/0 (test_nvm_codec.cpp:111-128; receipts/ctrl_nvm_selftest.log; receipts/r506_2_guard_ge_probe.log); fw_gtest_main.cpp:89-107,167-182 under SIGBUS/SIGFPE/SIGILL, a suite tear-down failure, a global-environment failure and a disabled suite (receipts/tally_selftest_mutants.log); re-entrant port behaviour of adp.c:42-281 (receipts/adp_reentry_r3.log) - boundary, malformed-length and failure paths behave as stated; the erased-record read past loaded stays disclosed and is owned by #677, and re-entrancy is owned by #678; neither is a defect this lane introduced or was asked to fix.`

`[R506] PASS Tests - test_nvm_codec.cpp:90-131; nvm_mutants.py:149-158; tally_cases.cpp; tally_selftest.py:79-175; receipts/{ctrl_nvm_selftest,ctrl_fw_selftest,tally_selftest_mutants,fw_coverage_check,fw_coverage_selftest,tally_extra_plants_r3,r506_2_*}.log - each new assertion is shown able to fail for its defect (the four guard plants, the 7 new listener defects); my independent plants confirm that the new cases have teeth (4 of 6 caught; the 2 escapes are S1 and S2, neither affecting a verdict); store gate 434 tests and 106 of 106; ctrl gate 76 of 76; coverage --check PASS (14 files) and --selftest 28 of 28; hosted firmware-unit at this head green on gcc 13.3.0 / GoogleTest 1.14.0.`

`[R506] PASS Docs - sw/firmware/gtest/README.md:50-110,209-296,315-319; sw/firmware/ctrl_nvm/README.md:443-444,466; test_nvm_codec.cpp:69-89; PR #675 body (Round 3 row, Known limitations); receipts/{docs_check,em_dash,em_dash_selftest,doc_paths,doc_style,gen_toc_check,diff_check}.log - the README counts match the code and logs (18 cases, 18 defects, 106 store defects, 14 rows of which 9 and 5); the #678 premise, its scope and each row's reached items match my measurement; the docs gates are rc 0 (em-dash and TOC with the pinned renderer, in a scratch environment); the one stale prose sentence is R1, a RESIDUE.`

## Evidence at the exact head

The local runs used gcc and gcov 16.2.1 with GoogleTest and GoogleMock 1.18.0 on the host. Each command has its own log and rc file. The campaigns ran concurrently (`scripts/run_campaigns.sh`), with their temporary trees under the packet's scratch directory.

| Command / probe | rc | Result | Receipt |
|---|---:|---|---|
| `tally_selftest.py --mutants` | 0 | 18 of 18 cases, 18 of 18 defects | `receipts/tally_selftest_mutants.log` |
| `test_ctrl_nvm.py --self-test --jobs 7` | 0 | 5 shapes, 434 tests, all 106 planted defects reddened; the 4 new defects caught by `codec_loaded_prefix` | `receipts/ctrl_nvm_selftest.log` |
| `test_ctrl_firmware.py --self-test` | 0 | every arm PASS, the `rv32` arm on a local ilp32 SDK, `mutants: 76 of 76 caught` | `receipts/ctrl_fw_selftest.log` |
| `fw_coverage.py --check --jobs 4` | 0 | PASS, 14 files | `receipts/fw_coverage_check.log` |
| `fw_coverage.py --selftest` | 0 | 28 of 28 | `receipts/fw_coverage_selftest.log` |
| `scripts/adp_reentry_r3.sh` (own probe) | 0 | rows 1 to 5 reached, as the README states (table above) | `receipts/adp_reentry_r3.log` |
| `scripts/tally_extra_plants_r3.py` (own probe) | 1 | 4 of 6 extra listener defects caught; the 2 escapes are S1 and S2 | `receipts/tally_extra_plants_r3.log` |
| `scripts/r506_2_guard_ge_probe.sh` (R506-2 F1 probe) | 1 | the `>=` guard now fails all 5 shapes in `codec_loaded_prefix` (was rc 0) | `receipts/r506_2_guard_ge_probe.log` |
| `scripts/r506_2_tally_extra_plants.py` (R506-2 F3 probe) | 0 | each of its 4 defects reddens the clone's own cases | `receipts/r506_2_tally_extra_plants.log` |
| `scripts/r506_2_adp_reentry_probe.py` (R506-2 F2 probe) | 0 | rows 1 to 4 reproduced | `receipts/r506_2_adp_reentry_probe.log` |
| `make -C tb/verilator/mbx -j16` (scoped Verilator 5.050, disposable clone at the head) | 0 | 179 / 134 / 13, mutants 4 of 4 | `receipts/mbx_bench_head.log` (host paths redacted) |
| `docs_check.py`; `check_doc_paths.py`; `check_doc_style.py` | 0 / 0 / 0 | 0 findings; 927 paths; 22 documents | `receipts/docs_check.log`, `doc_paths.log`, `doc_style.log` |
| `check_em_dash.py --base 423ac5d9` and `--selftest`; `gen_toc.py --check` (pinned renderer, installed by hash into a scratch environment) | 0 / 0 / 0 | 0 findings over 494 added lines; 339 arms; TOC OK | `receipts/em_dash.log`, `em_dash_selftest.log`, `gen_toc_check.log` |
| `ci_scope.py --selftest`; `ci_events.py --check`; `git diff --check 423ac5d9 6ca834a7` | 0 / 0 / 0 | PASS; 1741 items; clean | `receipts/ci_scope_selftest.log`, `ci_events_check.log`, `diff_check.log` |
| hosted `rtl-fast` run 37457222400, `firmware-unit` job 112247900469 (PR merge ref `3b91e77`, i.e. `6ca834a7` into dev `bd884631`) | success | **Executed**, not skipped: gcc/gcov 13.3.0, GoogleTest 1.14.0; tally 18 of 18; ctrl PASS with `rv32` SKIPPED by name; store PASS; coverage selftest 28 of 28; coverage PASS, 14 files | `receipts/hosted_firmware_unit_job_6ca834a7.txt`, `receipts/hosted_checks_snapshot.txt` |
| checkout restore | - | index tree = head tree `79a9a6b1`; index listing unchanged; no tracked change; gitlinks external `efeb541a` (not checked out), gptp-processor `5dce647a`, protocol-processor `ead80360`, verilog-axis `48ff7a7e`; submodule worktrees clean | `receipts/restore_check.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-3 items 1-3 against the delta; `nvm_klj2.h:106-109` and `nvm_klj2.c:306-351`; #678's ruling against `README.md:209-296`; `adp.h:129-145`; listener behaviours against `README.md:50-110` | R506-3 | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| RTL | CLEAN | `receipts/delta_scope.txt` (no RTL, bench, config, workflow or firmware source in the delta); mailbox bench at the head, 179/134/13 and 4 of 4; `adp_mbx.c:16-54` and `mbx/mbx.c` (no callback) | R506-3 | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Robustness | CLEAN | loaded-prefix boundaries at -1/0 for header and payload; listener signal, tear-down, environment and disabled-suite paths; re-entrant ADP ports measured (owned by #678); erased-record read disclosed (owned by #677) | R506-3 | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Tests | CLEAN (S1 and S2 are SUGGESTIONs) | `test_nvm_codec.cpp:90-131`; `nvm_mutants.py:149-158`; `tally_cases.cpp`; `tally_selftest.py`; both campaigns, coverage check and selftest, tally `--mutants`; own and R506-2 probes; hosted `firmware-unit` at the head | R506-3 | 6ca834a782a1bd5574d44998c8e214cf16df3441 |
| Docs | CLEAN (R1 is a RESIDUE) | `sw/firmware/gtest/README.md`, `sw/firmware/ctrl_nvm/README.md`, `test_nvm_codec.cpp:69-89`, the PR #675 body; docs gates rc 0 | R506-3 | 6ca834a782a1bd5574d44998c8e214cf16df3441 |

My R506-2 coverage of RTL at `e7e0c10f` is also still valid at this head, since nothing in that lens's scope has changed. This round re-covers RTL at `6ca834a7` anyway.

## Real limits of this round

- Not reproduced locally:
  - gcc 13.3.0 and GoogleTest 1.14.0: those figures come from the hosted `firmware-unit` log at this head, which ran without `--mutants`.
  - The lwSRP arm and coverage with lwSRP: no lwSRP checkout was used. The delta does not touch the lwSRP port.
  - The ctrl `rv32` arm against the CI-pinned SDK (#679): the local arm ran on an ilp32 SDK.
- Not run, as not permitted: the 48-command builder set; the parent, processor, gPTP and Yosys banks; act and `act_ci.py`; any rerun at the base head.
- The hosted run used the PR merge ref with dev `bd884631`, not the bare head. It is the source-plus-dev result GitHub built. It is not the manager's candidate merge.
- Hosted `rtl-full` (Verilator shards 0, 1, 2 and 4) and `elaborate` were still running at the 11:56:01 UTC snapshot. Physical gPTP was skipped, which is not hardware evidence. Physical calibration was NOT RUN.
- Each campaign ran once. The host was heavily loaded during the runs, with a load average of about 50 to 67, so the timings are not meaningful.
- Ignored `__pycache__` directories from the gate runs remain in the review clone. The tracked bytes are exact.

## Pending manager duties

- Hosted and act acceptance at the exact head, including `rtl-full` and `elaborate`, which were still running at the snapshot.
- The candidate merge build against live dev `bd884631` at the merge turn.
- Carry R1 to the residue checklist.
- Optionally route S1 and S2 to the lane, or to a later harness Issue.
- Track the follow-ups: #678's F0 change (state the rule in `adp.h`, add the guard, then repoint the README premise at the header), #677 (the erased-record read past `loaded`) and #679 (the ctrl `rv32` arm against the CI-pinned SDK).

R506-3 FINISHED
