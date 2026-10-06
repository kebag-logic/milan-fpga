[R506] NEGATIVE - exact head 27433e47c6d7805376547a91b418cf6aa9d95d2a

# R506-1: internal cleared-context review of PR #675 (issue #665, lane FT)

- Head under review: `27433e47c6d7805376547a91b418cf6aa9d95d2a`, tree `b8eed7686df2a3a1980ac68f3667da45451e5e3b`; source base `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
- Round: R506-1, the first review of PR #675. All five lenses were applied independently: Conformance, RTL, Robustness, Tests, Docs.
- Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the #665 issue body, the owner unit-test directive (issuecomment-6008744385), the lane FT assignment (issuecomment-6009234414), the takeover and REVIEW READY comments, the PR body, `git diff 423ac5d9..27433e47` with its seven commits, the public evidence tree `review-evidence/665ft-r1` at `b7eb2edc`, and the exact-head hosted run.
- Prior public review findings on PR #675: none. The PR carries only the two review-start notices (issuecomment-6011448005 and -6011448807). My verdict and ledger were drafted before I read them.

Verdict: NEGATIVE, because three MINOR findings are open (F1, F2, F3). The harness, the port, the CI wiring and the campaigns are otherwise sound and were reproduced, as the evidence table below shows.

## Findings

### F1 MINOR: one coverage exclusion hides a reachable branch

- **Lenses:** Conformance, Tests, Robustness, Docs.
- **Where:**
  - `sw/firmware/gtest/README.md:205`: the row `ctrl_pool.c | ctrl_pool_alloc | bin->free_head != NULL | 1 arc`.
  - `sw/firmware/gtest/README.md:183`: "none is a gap a test could close".
  - The guard itself is at `sw/firmware/ctrl/port/ctrl_pool.c:114-115`.
- **Authority/evidence:**
  - Assignment item 4 says the target is 100% branch coverage, the lane writes the missing tests, and an exclusion is for an unreachable branch with its proof. The assignment focus also says an exclusion that hides a reachable branch is a finding.
  - The row's proof reasons only from the pool's own calls ("free_count and the free list move together"). The firmware's own comment at `ctrl_pool.c:114` says the guard exists for the case where they do not: "a free list that disagrees with its count is exhausted, not followed". The free list lives in the freed blocks' first bytes (`ctrl_pool.c:8-9`), so a client that writes into a block after freeing it leaves `free_count > 0` with `free_head == NULL`.
  - The probe `probes/pool_guard_probe.cpp` (run by `probes/pool_guard_probe.sh`) does this with the head's `ctrl_pool.c`. The sequence is: alloc 2, free 2, zero the head block's first word, alloc 1, alloc 1.
  - gcov then reports line 115 `branch 5 taken 25%`: the excluded arc is taken. The probe test passes, and the second alloc is refused and counted.
  - A copy with `&& bin->free_head != NULL` removed dies of SIGSEGV on the same sequence (`receipts/pool_guard_probe.log`, exit 139).
  - The exclusion makes the shipped suite certify this arc as unreachable, so no test fails without the guard.
- **Impact:**
  - The ratchet reports `ctrl_pool.c` at 100% branches by excluding a defensive path a ten-line test reaches.
  - Deleting the guard, which turns a corrupted free list into a NULL dereference on a bare-metal core, survives every test and every planted defect.
  - The README's blanket claim that no exclusion is a test gap is false for this row.
- **Required outcome:**
  - A test (in `test_port_loop.cpp` or the unit binary) reaches the arc and asserts the refusal, and its count, with a planted defect that removes the guard.
  - The row is deleted from the exclusion table.
  - `coverage.ratchet` records `ctrl_pool.c` at the new totals.
  - The README count of exclusion rows and functions, and the PR body's "16 exclusion rows (13 functions)", follow the change.
- **Verification:**
  - `fw_coverage.py --check` passes with the row gone. A stale row would fail it, because the gate refuses rows that no longer match.
  - `test_ctrl_firmware.py --self-test` reports the new defect caught.
  - Rerun `probes/pool_guard_probe.sh <checkout> <workdir>`.

### F2 MINOR: the tally self-test never asserts the tally line, so listener defects that falsify it survive

- **Lenses:** Tests, Conformance.
- **Where:**
  - `sw/firmware/gtest/tally_selftest.py:95-114` (`grade_case`).
  - The listener: `sw/firmware/gtest/fw_gtest_main.cpp:161`, `:175-178` and `:97`.
  - The claim: `sw/firmware/gtest/README.md:50-52` and `:67-82`.
- **Authority/evidence:**
  - Assignment item 2 says a failing or crashing test must make the tally fail, proved with planted cases. The README states that `failures` counts the tests that failed, were skipped or crashed, plus set-up failures.
  - `grade_case` checks the overall grade (`fw_gtest.grade`), a `[FAIL]` line naming the test, and `suite_tally.py --verdict`. Every one of those is satisfied by the `[FAIL]` marker or the exit status alone. Nothing asserts the tally line's own `failures` or `RESULT`.
  - Planted into copies of the listener (`probes/tally_mutants.sh`, `receipts/tally_mutants.log`), three defects survive the self-test (exit 0, 11 of 11 "as planted"):
    - skipped tests not counted (`:161`);
    - a suite set-up failure not counted (`:175-178`);
    - the crash tally not counting the crashed test (`:97`).
  - With the first, the planted skip prints `checks: 1   failures: 0` and `RESULT: PASS`. The run is still refused only by its `[FAIL]` line.
  - Three defects are caught: no atexit handler, no signal handler, and disabled tests not counted.
- **Impact:**
  - The "11 planted cases prove ... fails the tally" claim (README table, PR body "Harness" row) is not what the self-test proves.
  - A regression that makes the tally line itself lie passes the self-test. The sweep's summed failure figure would undercount, and the protection would rest on the `[FAIL]` marker alone, which the self-test does not isolate either.
- **Required outcome:**
  - Each planted case asserts its tally line: the expected `checks` and `failures` numbers, or at least `failures >= 1` and `RESULT: FAIL` for every failing case, read with `suite_tally.scan`.
  - The three listener defects above are shown killed.
  - The README and PR wording say which property each case proves.
- **Verification:** `tally_selftest.py` still passes, and `probes/tally_mutants.sh <checkout> <workdir>` reports every plant caught.

### F3 MINOR: the README says the coverage gate and each gate print the toolchain; only the store gate does

- **Lenses:** Docs.
- **Where:**
  - `sw/firmware/gtest/README.md:166-168`: "there is nothing else to pin: the coverage is gcc's, and the gate prints the gcc and gcov it ran with".
  - `sw/firmware/gtest/README.md:231-232`: "Each gate prints the compiler, gcov and GoogleTest versions it ran with".
- **Authority/evidence:**
  - `fw_gtest.toolchain()` has one caller, `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:252`.
  - `fw_coverage.py` prints no toolchain line. `measure()` keeps only each gate's last 8 lines, so the store gate's line is dropped (`receipts/cov_check.log`).
  - `test_ctrl_firmware.py` prints none (`receipts/ctrl_gate_selftest.log`).
  - The arc totals depend on the gcc version: the README's two-version table exists for that reason. So the README presents the gate's own output as the record of the coverage pin, and that output does not exist.
  - The hosted job's install step does print the versions, which is why this is only MINOR.
- **Impact:** a local `--check` or `--write` leaves no record of the gcc and gcov behind its figures, despite the page saying it does.
- **Required outcome:** either the coverage gate (and the ctrl gate) print the toolchain, or both sentences say exactly where the versions are recorded: the job's install step and the README table.
- **Verification:** the gate's output, or a reread of the two README lines.

### S1 SUGGESTION: an uncovered arc can move inside an excluded function without a finding

- **Lenses:** Tests, Docs.
- **Where:** `sw/firmware/gtest/fw_coverage.py:216-259` (`apply_exclusions`); `sw/firmware/gtest/README.md:189-193`.
- **Evidence:**
  - Rows are matched by per-function counts. `probes/exclusion_swap_probe.py` (`receipts/exclusion_swap_probe.log`) builds a measurement in which the selftest's excluded `if (a == 7)` is now taken, while another arc and another line of the same function go uncovered. The gate reports no finding.
  - Each event alone does fail the gate, as the README says. Only the combination passes.
- **Suggestion:**
  - Also require each row's statement line (or its condition's line span) to hold at least one uncovered arc or line.
  - Add this case to `fw_coverage_selftest.py`.

### S2 SUGGESTION: the gates inherit the `GTEST_*` environment

- **Lens:** Robustness.
- **Where:** `sw/firmware/gtest/fw_gtest.py:85-91`, `:180-186`.
- **Evidence:** `run_binary` passes the parent environment through. GoogleTest honours `GTEST_FILTER` and its relatives. A negative filter (`-*X*`) narrows every binary while each still reports a non-zero tally, so `NOCOUNT` does not fire. CI does not set these; a developer shell might.
- **Suggestion:** drop `GTEST_*` from the environment `run_binary` hands each binary, or print it as part of the verdict.

### RESIDUE (wording only)

R1: the PR #675 body is stale about hosted evidence.

- **Where:** "Status: ... No hosted run yet." and the Known limitations bullet "No hosted or `act_ci.py` run exists yet: the branch is not pushed".
- **Why stale:** the exact-head hosted `rtl-fast` run 37429204550 exists, and its `firmware-unit` job 112155948905 passed.
- **Exact fix:** replace the Status sentence with "Hosted `rtl-fast` at this head: `firmware-unit` passed (run 37429204550); act replay pending." Replace the bullet with "Hosted evidence: `rtl-fast` run 37429204550 at `27433e47`; the act replay is the manager's."

## Clean lenses, in findings format

`[R506] PASS RTL - hdl/ (no change in 423ac5d9..27433e47), tb/verilator/mbx/suite.hpp, receipts/mbx_bench_head.log`

- The diff touches no RTL, configuration, builder or shipping-image file.
- The only bench change is `suite.hpp`, refactored into `run_group()` with the group order and every check kept. I read the diff hunk by hunk.
- `suite.hpp` was rerun through both RTL adapters with the pinned Verilator 5.050 (identity printed): Wishbone `checks: 134`, AXI4-Lite `179`, cosim `13`, `mbx mutants: 4 of 4 caught`, the same figures as base.
- The firmware state-machine reachability behind the ADP exclusions was traced against `sw/firmware/ctrl/adp/adp.c:153-281` (every way into and out of DOWN, DELAY and WAITING, and the timer kind each holds).
- The mailbox contract (`mbx_contract.h`, `mbx_hal.h`) is unchanged.

Every other lens carries an open finding above. What each one still examined clean is listed in the ledger.

## Exclusion judgement (all 16 rows, `sw/firmware/gtest/README.md:197-212`)

| # | File / function | Judgement | Checked against |
|---|---|---|---|
| 1 | `adp.c` `adp_link_change` up, out of DOWN | holds | `adp.c:177-218`: enabled with link recorded down implies DOWN; a disabled machine is DOWN with its timer stopped |
| 2 | `adp.c` `adp_link_change` down, already DOWN | holds | DOWN is reached while enabled only by a link loss; `shutdown` only runs from `adp_set_enable(false)` |
| 3 | `adp.c` `adp_timer_expired` DELAY with ADVERTISE | holds | `timer_start(ADVERTISE)` only in `advertise`, which then enters WAITING (`:121-131`) |
| 4 | `adp.c` `adp_timer_expired` final else | holds | DOWN is always entered with the timer stopped; TMR_DELAY only via `enter_delay` |
| 5 | `adp.c` `adp_poll` owed outside enabled DELAY | holds | `available_owed` is set only in an enabled DELAY and cleared on every exit from it |
| 6 | `adp_mbx.c` `on_poll` second operand | holds | `MBX_N_IF` is 1 (`mbx_contract.h:27`); the row turns stale, and the gate fails, once it grows |
| 7 | `adp_mbx.c` `adp_mbx_attach` bind fail | holds | `ctrl_loop_bind_rx` refuses only `ch >= MBX_N_CH` or a NULL function (`ctrl_loop.c:18-26`) |
| 8 | `ctrl_app.c` `ctrl_app_start` adapter refusal | holds | `0 + 1 > 16` is false; the loop is initialised empty just before |
| 9 | `ctrl_pool.c` `ctrl_pool_alloc` `free_head != NULL` | **reachable: F1** | probe: a client write into a freed block |
| 10 | `nvm_klj2.c` `nvm_shape_consistent` walk order/offset/size | holds | the `_Static_assert`s at `nvm_klj2.c:16-21` and `nvm_shape.h:133`; `nvm_rec_next` adds the same lengths; the uint8 map table can only shrink a length |
| 11 | `nvm_klj2.c` `nvm_shape_consistent` count | holds | `NVM_N_REC` sums the same group counts |
| 12 | `nvm_klj2.c` `nvm_klj2_check_body` header past loaded | holds | callers pass `img_len` or `NVM_STAGE_BYTES` (`nvm_store.c:194`, `nvm_klj2.c:379`); `HDR + AREA_RAW + 8 < IMG_LEN + 8` |
| 13 | `nvm_store.c` `nvm_idle` window open, nothing dirty | holds | dirty bits are set only at `:796` and cleared only by the capture at `:572`, after `:465` closes the window |
| 14 | `nvm_store.c` `nvm_framed_as` | holds | the stage is the blank container, a re-staged container that passed `nvm_klj2_check`, or `nvm_rec_frame` output; erased spans are whole-0xff (`nvm_klj2.c:290-301`) |
| 15 | `nvm_store.c` `nvm_erase_start` target is auth | holds | `nvm_target_slot` returns `!auth`, or 0 or 1 when auth is -1 |
| 16 | `nvm_flash_litespi.c` `ls_in_journal` length | holds | callers pass at most `LS_PAGE` or `LS_BLOCK`; the journal is 128 KiB |

The measured header arcs (`mbx_wire.h`, `wire.h`) were split by object (`probes/header_cov_split.py`). Three `mbx_wire.h` arcs are reached only by the unit tests' direct calls (`test_unit_driver.cpp` D10). That is a deliberate unit test of the inline helpers, stated in `fw_gtest.py:74-76`, so it is not a finding.

## Evidence (this round, at the exact head; host gcc/gcov 16.2.1, GoogleTest 1.18.0)

| Command / probe | rc | Result | Receipt |
|---|---:|---|---|
| `tally_selftest.py` | 0 | 11 of 11 as planted | `receipts/tally_selftest.log` |
| `test_ctrl_firmware.py --require-rv32 --self-test` | 0 | arms model 14, port 29, adp 26, unit 21+2, walk 41, entity 5x9, rv32 1 (local ilp32 SDK); `mutants: 74 of 74 caught` | `receipts/ctrl_gate_selftest.log` |
| `test_ctrl_firmware.py --lwsrp <lwSRP at 19f5796b>` | 0 | lwsrp arm 1 test PASS, pin accepted | `receipts/ctrl_gate_lwsrp.log` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 0 | 5 shapes, 429 tests, all 100 planted defects reddened, RV32 builds | `receipts/nvm_gate_selftest.log` |
| `fw_coverage.py --selftest` | 0 | 18 of 18 | `receipts/cov_selftest.log` |
| `fw_coverage.py --check` (without / with lwsrp) | 0 / 0 | PASS, 14 files; the two tables are identical | `receipts/cov_check.log`, `receipts/cov_check_lwsrp.log` |
| `ci_scope.py --selftest`; `ci_events.py --check`; `ci_events.py --selftest` | 0 / 0 / 0 | PASS; 1741 contract items; 2352 arms | `receipts/ci_*.log` |
| `make -C tb/verilator/mbx` (pinned Verilator 5.050, exported head tree) | 0 | 134 / 179 / 13, 4 of 4 mutants | `receipts/mbx_bench_head.log` |
| docs gates: `check_em_dash.py --base 423ac5d9` (pinned renderer), `check_doc_style.py`, `check_baremetal_only.py --check`, `docs_check.py` | 0 each | 0 findings | `receipts/docs_*.log` |
| `probes/port_words.py` | 0 | 202 of 202 base call sites (121 adp, 81 port) found verbatim at head | `receipts/port_words.log` |
| `probes/port_conditions.py` | 0 | 39 normalised pairs differ: each was read, and all are fixture names, per-test counter deltas or helper calls (S2 "in one call" 2 to 1 and D3 "1 + taken" to "taken" follow per-test fixtures) | `receipts/port_conditions.log` |
| `probes/mutant_sets.py` | 0 | ctrl 51 to 74, ctrl_nvm 82 to 100; no base defect missing or re-planted | `receipts/mutant_sets.log` |
| `probes/pool_guard_probe.sh` | 0 | F1: guarded arc taken; without the guard, SIGSEGV | `receipts/pool_guard_probe.log` |
| `probes/tally_mutants.sh` | 0 | F2: 3 of 7 listener plants survive (the first `disabled-not-counted` plant broke the build and was redone as `-v2`, which was caught) | `receipts/tally_mutants.log` |
| `probes/exclusion_swap_probe.py` | 0 | S1: no finding on a swapped arc | `receipts/exclusion_swap_probe.log` |
| `probes/header_cov_split.py` | 0 | header arcs by object kind | `receipts/header_cov_split.log` |
| pinned Bootlin SDK (sha256 `d42680e9...` = `ARCHIVE_SHA256`) on the ctrl sources at `-mabi=ilp32` | - | 5 of 9 sources fail on glibc headers: the PR's stated pre-existing limitation, confirmed | `receipts/rv32_pinned_sdk_probe.log` |
| Hosted `rtl-fast` run 37429204550, job `firmware-unit` 112155948905, head `27433e47` | success | executed, not skipped. libgtest-dev and libgmock-dev 1.14.0-1, g++/gcov 13.3.0; tally 11 of 11; ctrl arms ok with rv32 SKIPPED by name; store 429 tests; coverage selftest 18 of 18; coverage PASS 14 files; aggregate `rtl-fast` pass | `receipts/hosted_firmware_unit_job.log`, `receipts/hosted_checks_snapshot.txt` |
| Checkout restore | - | index tree = head tree `b8eed768`; worktree = HEAD; gitlinks protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e` | `receipts/restore_check.txt` |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | assignment items 1-6 against the diff: no seam added (four mocks on `mbx_hal.h`, `shlan_port.h`, `nvm_flash.h`, the CSR stubs), firmware unchanged but for 3 comment lines of `adp_mbx.h`; port mapping by words and conditions; both campaigns; gcov JSON reader, ratchet and exclusions; CI job, packages, `ci_events` pin, `ci_scope` cases; F1 misses item 4 for one branch; F2 leaves item 2's proof partial | R506-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| RTL | CLEAN | no `hdl/` change; `tb/verilator/mbx/suite.hpp` refactor and RTL bench rerun 134/179/13, 4 of 4; ADP firmware FSM reachability; mailbox contract unchanged | R506-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Robustness | UNCLEAN (F1) | tally paths for crash, abort, exit, `_exit`, skip, throw, disabled, set-up and empty runs; timeout to NOCOUNT; mock with none alive; longjmp escape; corrupted pool free list (F1); environment inheritance (S2) | R506-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Tests | UNCLEAN (F1, F2) | every base check's words and condition at head; mutant sets base and head; both campaigns rerun; tally listener mutation probe (F2); coverage gate selftest and swap probe (S1); exclusion proofs (F1) | R506-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |
| Docs | UNCLEAN (F1, F3) | `sw/firmware/gtest/README.md`, `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl_nvm/README.md` (counts 52 checks / 84 tests / 429 verified), `docs/testing/CI_WORKFLOWS.md`, `docs/README.md`, `docs/design/MAILBOX_SPLIT.md`, PR body (R1 residue); docs gates 0 findings | R506-1 | 27433e47c6d7805376547a91b418cf6aa9d95d2a |

## Real limits of this round

- Local runs used gcc/gcov 16.2.1 and GoogleTest 1.18.0. The runner's 13.3.0 and 1.14.0 figures come only from the hosted log, not from a local replay.
- Not run (not permitted in this round):
  - the 48-command builder set;
  - any parent, processor, gPTP or Yosys bank;
  - act or `act_ci.py`;
  - base-head gate reruns. The base comparison was static (mutant sets, check words).
- The local ctrl `rv32` arm passed with a self-built ilp32 Buildroot SDK, not the CI-pinned one. The pinned archive was probed by compile only.
- The lwSRP arm and the coverage-with-lwSRP run used a scratch clone at the pin. That coverage run's builds went to the tool's default temporary directory, which removes itself.
- At the snapshot (`receipts/hosted_checks_snapshot.txt`), hosted Verilator shards 0, 1, 2 and 4, `docs-check` and `elaborate` were still pending. Physical gPTP was skipping, which is not evidence; physical calibration was not run.
- Each campaign ran once. Ignored `__pycache__` directories from the gate runs remain in the clone; tracked bytes are exact.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the hosted contexts still pending at the snapshot.
- The candidate merge build against live `dev` at the merge turn.
- File the pre-existing ctrl `rv32` arm defect (the pinned `ilp32d` SDK cannot build `-mabi=ilp32`: `receipts/rv32_pinned_sdk_probe.log`) as its own Issue, as the PR proposes. No such Issue exists yet.
- Carry R1 to the residue checklist.
- Collect the external review R507.
- Re-review the corrected head for F1 to F3.

R506-1 FINISHED
