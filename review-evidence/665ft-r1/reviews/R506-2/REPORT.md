[R506] NEGATIVE - exact head e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7

# R506-2: internal cleared-context re-review of PR #675 (issue #665, lane FT)

- **Head under review:** `e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7`, tree `0ae619a8c3dd3efdf2cbc9bdbf45ed7221c4e20d`.
- **Source base:** `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
- **Round:** R506-2. Its delta is the four commits on `27433e47` (`8387d18f`, `341ea77e`, `7412748e`, `e7e0c10f`), reviewed against the round-2 assignment (issue comment 6012062072).
- **Lenses:** all five were applied independently: Conformance, RTL, Robustness, Tests, Docs.
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the issue #665 body, the unit-test directive (6008744385), the FT assignment (6009234414) and the round-2 assignment (6012062072);
  - the author's round-2 TAKEN and REVIEW READY comments (6012112514, 6013685269);
  - the public headers `adp.h`, `ctrl_pool.h` and `nvm_klj2.h`;
  - the full diff `423ac5d9..e7e0c10f` and its history, then executable evidence.
- **Order of reading:**
  - I read the prior public findings (R506-1 at 6011948437, R507-1 at 6012056114) only after finishing my own pass over the delta.
  - The same PR-comment fetch also returned the other reviewer's round-2 report (6014209924). It arrived after my findings F1 to F3 and their probes were complete. Nothing below rests on it, and none of its conclusions was adopted.

Verdict: NEGATIVE, because three MINOR findings are open: F1, F2 and F3. Every round-1 finding is resolved at this head. F1 carries forward the one part of R507-1-F1's verification that the new test exercises but does not pin. The coverage gate's new binding of each exclusion to its items is sound: none of the 14 rows accepted a compensating swap I planted.

## Findings

### F1 MINOR: the loaded-prefix test does not pin the guard at the exact header end; an off-by-one guard survives the whole suite

- **Lenses:** Conformance, Robustness, Tests.
- **Where:**
  - `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:93`, the "header ... but not its payload" assertion;
  - the guard at `sw/firmware/ctrl_nvm/nvm_klj2.c:350`;
  - the planted defects at `sw/firmware/ctrl_nvm/test/nvm_mutants.py:145-148`.
- **Authority/evidence:**
  - Round-2 assignment item 1 asks for the direct test "at the boundary and at the adjacent header boundary". R507-1-F1's verification asks the same ("exercise the adjacent header boundary too"). The author's TAKEN reads the second as "at that header's exact end (the guard passes and the walk goes on)".
  - The test's exact-end assertion expects `NVM_VD_REC`. A guard that refuses at the exact end returns the same verdict, so the assertion cannot tell the two apart. Both planted defects are caught by the earlier, short-of-header assertions alone (`receipts/nvm_selftest.log:61-62`).
  - **Probe 1**, `scripts/guard_ge_probe.sh` (`receipts/probe_nvm_ge_guard.log`, rc 0): with the guard changed from `>` to `>=` and nothing else changed, the store gate passes all 434 tests on all 5 shapes.
  - **Probe 2**, `scripts/klj2_boundary_probe.sh` (`receipts/klj2_boundary_probe.log`), shows the change is a public behaviour:
    - The container's CRC closes (`nvm_klj2_check` returns 3, not CRC 4), and its first record header claims a payload past the end.
    - At `loaded` = that header's end, the head returns `NVM_VD_LEN` (3).
    - The off-by-one copy returns `NVM_VD_REC` (7).
  - The verdict numbering is the backend status nibble's (`nvm_klj2.h:21-22`).
- **Impact:** an off-by-one at the boundary the round asked to test passes every test and the coverage gate, and it changes a public verdict.
- **Required outcome:**
  - At `loaded == pos + NVM_REC_HDR`, the test asserts an outcome reachable only when the guard passes. One example is a CRC-closed container whose header at that position yields the record's own non-`VD_REC` verdict.
  - A planted off-by-one defect (`>=`) is killed by that test.
  - The public contract is unchanged.
- **Verification:**
  - `test_ctrl_nvm.py --self-test` reports the new defect caught.
  - `scripts/guard_ge_probe.sh <checkout> <work>` exits non-zero.

### F2 MINOR: the README's exclusion standard is stated as met, while the ADP rows rest on a premise `adp.h` does not state, and the premise's reach is understated

- **Lenses:** Conformance, Tests, Docs.
- **Where:**
  - `sw/firmware/gtest/README.md:199-204`: "Each exclusion is a branch no sequence of calls through the module's public header reaches, with the ports keeping the contract their header states ... A row's proof does not rest on what today's callers happen to pass."
  - `sw/firmware/gtest/README.md:247-256`: the premise paragraph.
  - The PR body's "Needs a decision" bullet: "reaches two of them".
- **Authority/evidence:**
  - Round-2 assignment item 3 asks that every remaining exclusion be re-judged against its module's public header, not against today's callers. Assignment 6009234414 item 4 asks that each exclusion carry its proof.
  - The README's own premise paragraph concedes that `adp.h` does not state "no port calls into the core while the core is calling it". Under the README's standard as written, the ADP rows therefore do not meet it. The author's REVIEW READY nevertheless says all 14 rows "hold".
  - The paragraph names only a timer port, and only the third and fourth rows. `scripts/adp_reentry_probe.py` builds the head's `adp.c` under gcov with ports that call back into the core, then applies the README's own rows to that measurement (`receipts/adp_reentry_probe.log`):
    - A send port that reports a link loss (`adp_link_change(false)`) from inside the ENTITY_AVAILABLE send reaches row 1's named arc. It leaves the machine in WAITING, with the link recorded down and TMR_ADVERTISE running. A later link-up then enters no DELAY.
    - The same send port, called from inside SHUTDOWN's ENTITY_DEPARTING, reaches row 2's named arc.
    - A timer port that expires a timer inside `timer_start` reaches rows 3 and 4, leaving the states the README gives.
    - Neither port reached row 5.
  - A send port that reports the link it found down is an ordinary integration choice, not an exotic one.
- **Impact:**
  - The 100 % figure's stated justification is broader than what holds.
  - The README and the PR body present the pending decision to the manager as a question about the timer port and two rows. A ruling narrowed to the timer port would leave rows 1 and 2 reachable through the send port.
- **Required outcome:** the contract decision itself stays with the manager. Until that ruling lands:
  - the standard sentence names the ADP rows as resting on the unstated premise;
  - the premise paragraph and the PR body's decision bullet say which port calls reach which rows: a send or link port calling `adp_link_change` from inside a core call reaches rows 1 and 2, and a timer port reaches rows 3 and 4.
- **Verification:**
  - Reread the two README passages and the PR bullet.
  - `scripts/adp_reentry_probe.py <checkout> <work>` reproduces the row-by-row reach.

### F3 MINOR: the tally self-test does not plant four listener behaviours the README says it proves; four listener defects escape, one of which falsifies the tally line

- **Lenses:** Tests, Docs.
- **Where:**
  - `sw/firmware/gtest/README.md:51-60` (the counting and signal claims) and `:67` ("`tally_selftest.py` proves each of those with a planted case").
  - `sw/firmware/gtest/tally_selftest.py:79` (`CASES`) and `:111` (`DEFECTS`).
  - The listener: `sw/firmware/gtest/fw_gtest_main.cpp:132-133` (the disabled-suite test), `:170` (failures outside every test) and `:195` (the signal list).
- **Authority/evidence:**
  - The README says the fatal-signal path covers SIGSEGV, SIGBUS, SIGFPE, SIGILL and SIGABRT, and that a suite's tear-down failure adds one. The listener also counts a failure outside every test (a global environment's), and it counts disabled suites as well as disabled tests. The README then says the self-test proves each of these.
  - The planted cases cover only SIGSEGV, `abort()`, a suite set-up failure and a disabled test.
  - `scripts/tally_extra_plants.py` (`receipts/tally_extra_plants.log`) adds the missing cases in a separate binary:
    - SIGFPE, SIGBUS and SIGILL inside a test;
    - a suite tear-down failure;
    - a failing global environment;
    - a `DISABLED_` suite.
  - The head's listener reads every one of those cases as planted, so the listener itself is correct.
  - The probe then plants four listener defects. The clone's own 12 cases redden none of them; the extra cases catch each one:
    - SIGFPE not handled;
    - SIGBUS not handled;
    - a program-level failure not counted: the tally prints `checks 1 failures 0` and `RESULT: PASS`;
    - a disabled suite not counted: `checks 0 failures 0`.
  - The program-level path is live in a shipped binary: `sw/firmware/ctrl_nvm/test/nvm_suite.cpp:74` registers a global environment.
- **Impact:**
  - A regression that makes the tally line itself lie can pass the self-test. That is the defect class R506-1-F2 was about, and the round-2 plants close it only for the paths they name.
  - The README's "proves each of those" is not what the self-test proves.
- **Required outcome:** either of these:
  - planted cases for the four behaviours, with listener defects of those kinds shown caught; or
  - the README states exactly which listener paths the self-test proves.
- **Verification:**
  - `tally_selftest.py --mutants` passes with the added cases.
  - `scripts/tally_extra_plants.py <checkout>` shows each of its four defects reddening the clone's own cases.

### S1 SUGGESTION: say in the tree that `codec_loaded_prefix` leaves out the erased-record header-whole case, and why

- **Lens:** Docs.
- **Where:** `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:69-76`.
- **Evidence:**
  - The PR body and the REVIEW READY comment state honestly that `nvm_klj2_record` reads an erased record's payload past `loaded`.
  - I reproduced it: AddressSanitizer reports a heap-buffer-overflow in `nvm_klj2_record` at `nvm_klj2.c:298`, called from `nvm_klj2_check_body` at `:352`, on a buffer of exactly 48 bytes (`receipts/klj2_boundary_probe.log`).
  - The PR body says the test leaves that case out. The test comment and the store README do not.
  - Nothing in-tree is false, and the ruling on the read itself is the manager's.
- **Suggestion:** add one sentence to the test comment naming the omitted case and its Issue, once one is filed.

### RESIDUE (wording only)

- **R1 (R506-1-R1, retained).** The PR #675 body is stale about hosted evidence at this head.
  - **Where:** the Status section reads "there is no hosted run at this head yet", and the Known limitations bullet says the same.
  - **Why stale:** hosted `rtl-fast` run 37445962183 at `e7e0c10f` completed with success, including `firmware-unit` job 112210865722 (`receipts/hosted_checks_snapshot.txt`, `receipts/hosted_firmware_unit_job.log`).
  - **Exact fix (Status):** "Hosted `rtl-fast` at this head: `firmware-unit` passed (run 37445962183); the act replay is the manager's."
  - **Exact fix (limitations bullet):** "Hosted evidence: `rtl-fast` run 37445962183 at `e7e0c10f` (round 1: 37429204550 at `27433e47`); the act replay is the manager's."

## Prior public findings at this head

| Finding | Lenses | Disposition at `e7e0c10f` |
|---|---|---|
| R507-1-F1, the loaded-prefix exclusion | Conformance, Robustness, Tests, Docs | **Resolved except for the part carried as F1.** `NvmCodec.codec_loaded_prefix` (`test_nvm_codec.cpp:77`) reaches the refusal at the 40-byte prefix and one byte short of every record header. The row is removed, and the ratchet records `nvm_klj2.c` at 195/195 lines and 104/104 branches. `short_prefix_read_on` and `short_prefix_as_len` are caught (`receipts/nvm_selftest.log:61-62`). The comment edit at `nvm_klj2.c:348-349` changes no code. The adjacent boundary is exercised but not pinned (F1). |
| R507-1-F2 and R506-1-S1, exclusion identity | Conformance, Robustness, Tests, Docs (F2); Tests, Docs (S1) | **Resolved.** `fw_coverage.py:278-352` binds each row to its unique statement, its arc count, its exact uncovered positions and its named lines. It removes only those items and refuses any unnamed gap in a function that has rows. Evidence: `fw_coverage.py --selftest` gives 28 of 28 here on gcc 16.2.1 and hosted on gcc 13.3.0, including the real-gcc swap and two-line cases. My round-1 swap probe is now refused (`receipts/r506_1_exclusion_swap_probe.log`). On the real firmware measurement, a compensating swap planted for each of the 14 rows, with the totals unchanged, is refused 14 of 14 (`scripts/row_swap_probe.py`, `receipts/row_swap_probe.log`). The README's "What the gate enforces" (`README.md:223-245`) matches the code. |
| R506-1-F1, the reachable pool exclusion | Conformance, Robustness, Tests, Docs | **Resolved.** `Pool.P9AFreeListShorterThanItsCountIsExhausted` (`test_port_loop.cpp:229`) cuts the head block's link. It asserts the head is still handed out, the count of 3, the spill to the next class, and the counted refusal. `pool-follows-a-cut-free-list` (SIGSEGV) and `pool-cut-list-refuses-outright` are caught (`receipts/ctrl_selftest.log:174-176`). The row is removed, and `ctrl_pool.c` is at 60/60. |
| R506-1-F2, the tally line not asserted | Conformance, Tests | **Resolved for its stated scope.** `tally_wrong` (`tally_selftest.py:165`) asserts each case's exact `checks`, `failures` and `RESULT`, read with `suite_tally.scan`: 12 of 12 cases and 11 of 11 defects (`receipts/tally_mutants.log`). My round-1 plants are all caught: the 6 that build, and the rebuilt `-v2` (`receipts/r506_1_tally_mutants.log`). The paths still unplanted are a new finding, F3. |
| R506-1-F3, toolchain not printed | Docs | **Resolved.** The ctrl gate, the store gate, the coverage gate (check and selftest) and the tally self-test each print `toolchain:` on their first line (the first line of every receipt). `README.md:298-302` says which gates print it. |
| R506-1-S2, inherited `GTEST_*` | Robustness | **Resolved.** `fw_gtest.run` drops `GTEST_*`, and the planted environment case passes (`receipts/tally_mutants.log`). |
| R506-1-R1, stale hosted status | Docs (RESIDUE) | **Retained** as R1 above, with the new run number. |

## Remaining exclusions, re-judged against their public headers (`README.md:258-273`)

| Rows | Judgement | Checked against |
|---|---|---|
| 1-4 (`adp.c`) | **Hold only under a premise `adp.h` does not state.** Re-entrant ports reach them (F2). | the `adp.h` port contract (`struct adp_ports`), `adp.c:42-243`, `receipts/adp_reentry_probe.log` |
| 5 (`adp.c` `adp_poll`) | Holds as far as I probed. It rests on the same unstated premise, but neither the re-entrant send port nor the re-entrant timer port reached it. | `adp.c:121-131`, `:269-281` |
| 6-8 (`adp_mbx.c`, `ctrl_app.c`) | Hold. They rest on generated constants (`MBX_N_IF` = 1; `0 + 1 > 16` is false), and the rows stop matching if a constant moves. | `adp_mbx.h`, the bind contract in `ctrl_loop.h` |
| 9-10 (`nvm_shape_consistent`) | Hold: a walk with no arguments over the generated shape. | `nvm_klj2.c:16-21`, `:186-203` |
| 11-13 (`nvm_store.c`) | Hold through `nvm_store.h`: the stage is read-only, and the target is `!auth`. | `nvm_store.h`; the round-1 trace, unchanged |
| 14 (`ls_in_journal`) | Holds. The public entry points are the `struct nvm_flash` calls, which pass at most `LS_PAGE` or `LS_BLOCK`. | `nvm_flash_litespi.c:178-221` |

## Clean lens, in findings format

`[R506] PASS RTL - git diff 27433e47..e7e0c10f over hdl/, tb/, configs/, sw/builder/, sw/litex/, syn/, .github/ and scripts/ (empty); tb/verilator/mbx at e7e0c10f (receipts/mbx_bench_head.log) - the round-2 delta touches no RTL, bench, configuration, builder, workflow or shipping-image file; the mailbox bench was rerun at this head with the scoped Verilator 5.050 (identity printed: "Verilator 5.050 2026-07-01 rev v5.050"): Wishbone 134, AXI4-Lite 179, cosim 13, mbx mutants 4 of 4; the only firmware source change (nvm_klj2.c:348-349) is a comment; the ADP machine's transitions under re-entrant ports were traced and measured (F2) as evidence for the manager's separate adp.h ruling, which this lane does not own.`

## Evidence at the exact head

Local runs used gcc/gcov 16.2.1 and GoogleTest/GoogleMock 1.18.0 on the host. Each command has its own log and rc file.

| Command / probe | rc | Result | Receipt |
|---|---:|---|---|
| `tally_selftest.py --mutants` | 0 | 12 of 12 cases, 11 of 11 defects | `receipts/tally_mutants.log` |
| `fw_coverage.py --selftest` | 0 | 28 of 28 | `receipts/cov_selftest.log` |
| `fw_coverage.py --check --jobs 8 --keep <scratch>` | 0 | PASS, 14 files, every row matching; raw `adp.c` 73/80, `nvm_klj2.c` 104/108 | `receipts/cov_check.log` |
| `test_ctrl_firmware.py --self-test` | 0 | port 30, adp 26, unit 21+2, walk 41, entity 5x9; `rv32` ran on a local ilp32 SDK; `mutants: 76 of 76 caught` | `receipts/ctrl_selftest.log` |
| `test_ctrl_nvm.py --self-test --jobs 10` | 0 | 5 shapes, 434 tests, all 102 planted defects reddened | `receipts/nvm_selftest.log` |
| docs gates: `check_em_dash.py --base 423ac5d9` (pinned renderer), `check_doc_style.py`, `check_baremetal_only.py --check`, `docs_check.py` | 0 each | 0 findings | `receipts/docs_*.log` |
| `ci_scope.py --selftest`; `ci_events.py --check`; `git diff --check 423ac5d9 HEAD` | 0 / 0 / 0 | PASS; 1741 items; clean | `receipts/ci_*.log`, `receipts/git_diff_check.log` |
| `make -C tb/verilator/mbx -j16` (scoped Verilator 5.050, disposable clone at the head) | 0 | 134 / 179 / 13, 4 of 4 | `receipts/mbx_bench_head.log` (host install path redacted to `<PINNED_VERILATOR_ROOT>`) |
| `scripts/guard_ge_probe.sh` | 0 | F1: the `>=` guard survives 434 tests | `receipts/probe_nvm_ge_guard.log` |
| `scripts/klj2_boundary_probe.sh` | - | F1: VD_LEN against VD_REC at the exact end; S1: the ASan read at `nvm_klj2.c:298` | `receipts/klj2_boundary_probe.log` |
| `scripts/adp_reentry_probe.py` | 0 | F2: rows 1 to 4 reached, row 5 not | `receipts/adp_reentry_probe.log` |
| `scripts/tally_extra_plants.py` | 0 | F3: 6 extra cases read as planted at the head; 4 defects escape the clone's cases | `receipts/tally_extra_plants.log` |
| `scripts/row_swap_probe.py` | 0 | 14 of 14 real-row swaps refused | `receipts/row_swap_probe.log` |
| round-1 probes rerun: `exclusion_swap_probe.py`, `tally_mutants.sh` | 0 / 0 | swap refused; every listener plant caught | `receipts/r506_1_*.log` |
| hosted `rtl-fast` run 37445962183, `firmware-unit` job 112210865722, head `e7e0c10f` | success | **Executed**, not skipped: gcc/gcov 13.3.0, GoogleTest 1.14.0-1; tally 12 of 12; ctrl PASS with `rv32` SKIPPED by name; store 434 tests; coverage selftest 28 of 28; coverage PASS, 14 files | `receipts/hosted_firmware_unit_job.log`, `receipts/hosted_checks_snapshot.txt` |
| checkout restore | - | Index tree = head tree `0ae619a8`; index listing sha256 unchanged; worktree clean. Gitlinks: gptp-processor `5dce647a`, protocol-processor `ead80360`, verilog-axis `48ff7a7e`, external `efeb541a` (not checked out, as before). Submodule worktrees clean. | `receipts/restore_check.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | round-2 items 1-5 against the delta; the `nvm_klj2.h:106-109` contract; `ctrl_pool.c:107-120`; the `adp.h` ports; the README exclusion standard; both campaigns' new defects | R506-2 | e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7 |
| RTL | CLEAN | no RTL, bench, config or workflow file in the delta; mbx bench rerun at the head, 134/179/13, 4 of 4; the firmware change is comment-only | R506-2 | e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7 |
| Robustness | UNCLEAN (F1) | the loaded-prefix boundary (F1); the cut free list (P9, resolved); the listener's crash, exit, environment and disabled paths (extra plants read as planted); the `GTEST_*` drop; re-entrant ADP ports (evidence for F2); the ASan read (S1) | R506-2 | e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7 |
| Tests | UNCLEAN (F1, F2, F3) | `test_nvm_codec.cpp:69-98`; `test_port_loop.cpp:224-248`; both mutant lists; `tally_selftest.py`; `fw_coverage.py` and its selftest; 14 real-row swaps; both campaigns and the coverage gate rerun | R506-2 | e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7 |
| Docs | UNCLEAN (F2, F3) | `sw/firmware/gtest/README.md` (the tally, coverage, exclusions, run and CI sections); `ctrl/README.md`; `ctrl_nvm/README.md` (53 checks, 85 tests and 102 defects, matching the logs); `docs/testing/CI_WORKFLOWS.md`; the PR body (R1, F2); docs gates with 0 findings | R506-2 | e7e0c10f4d4e9f3180b5650507a83aa300c5d4d7 |

## Real limits of this round

- Not reproduced locally:
  - gcc 13.3.0 and GoogleTest 1.14.0: their figures come from the hosted `firmware-unit` log at this head, not from a local replay.
  - The lwSRP arm (`--lwsrp`) and coverage with lwSRP: no lwSRP checkout was used. The delta does not touch the lwSRP port.
  - The ctrl `rv32` arm against the CI-pinned SDK: the local arm ran on an ilp32 SDK.
- Not run (not permitted): the 48-command builder set; the parent, processor, gPTP and Yosys banks; act and `act_ci.py`; base-head reruns.
- Hosted contexts: `Verilator shard 1/5`, `2/5` and `4/5` were still in progress at the snapshot. Physical gPTP was skipped, which is not hardware evidence. Physical calibration was not run.
- Each campaign ran once.
- Ignored `__pycache__` directories from the gate runs remain in the review clone. Tracked bytes are exact.

## Pending manager duties

- Rule on the two items the author raised:
  - the `adp.h` re-entrancy contract, including F2's evidence that a send or link port reaches rows 1 and 2;
  - the out-of-bounds read at `nvm_klj2.c:298`, and its Issue.
- File the pre-existing ctrl `rv32` arm defect as its own Issue.
- Hosted and act acceptance at the exact head, including the Verilator shards still running at the snapshot.
- The candidate merge build against live `dev` (`30e3c018`) at the merge turn.
- Carry R1 to the residue checklist.
- Re-review the corrected head for F1 to F3.

R506-2 FINISHED
