[R733] NEGATIVE - exact head 99de3a023abfda5604a70832e23baf7ff73481a3

# R733-1: internal cleared-context review of PR #811 (#665 S3, the split control firmware's target platform)

- Head `99de3a023abfda5604a70832e23baf7ff73481a3`, tree `715917bbb3c732168a35124b1571a3d2f8401580`; source base `f4c9ad4f` (`dev-soft-core`), 17 commits, 45 files.
- Whole-PR review of `git diff f4c9ad4f..99de3a02`, with all five lenses applied independently.
- Context was rebuilt from public state only:
  - AGENTS.md and CONTRIBUTING.md;
  - the #665 body, and the S3 assignment (6493622258) and plan decisions D0-D9 (6409738976);
  - the ledger rulings 6412739248, 6425357821 and 6505997821 (S3's), and the S3 TAKEN, STOP and REVIEW READY receipts;
  - `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 2, `REGISTER_MAP.md`, `milan_baremetal.c`, and the MAAP and SRP READMEs;
  - the published evidence at `608e2f22` (`review-evidence/665s3-r1`, author-r0, author-r1 and author).
- **Prior public review findings on this PR: none.** The PR has two review-start comments, R733-1 and R734-1, and no review. No other reviewer's report was read.

**Verdict: NEGATIVE.** Two MINOR findings are open:
- F-1: the console reads past a command literal on malformed UART input.
- F-2: the tests do not detect a misplaced or unbound saved-state composition step.

Both are small and local, and every other focus item checks out.

## What was verified, against what

### (1) The boot order (Milan v1.2 5.6.1, `ARCHITECTURE_HW_SW_SPLIT.md` section 2)

- `ctrl_plat.c:226-273` runs these steps in order:
  1. banner;
  2. the ID check;
  3. the policy, then MAAP's one-owner report;
  4. the AEM CRC;
  5. compose, with the console poll added;
  6. `nvm_store_boot` and the store tick;
  7. `ctrl_app_open_held`;
  8. SRP;
  9. `ctrl_app_open_aecp`, then `ctrl_app_release_adp`.
- ADP is never enabled before AECP's face commit and release:
  - `ctrl_app.c:74` enables ADP as `!adp_held`;
  - B1 checks that ADP's first timer comes after the face commit;
  - B5 and B6 check that ADP never starts on a refused stage.
- Mutants `plat-adp-before-aecp`, `plat-adp-not-held` and `app-adp-hold-ignored` are all caught in my run.
- One gap: the saved-state step's place, and its write path, are not detected by any test (F-2).

### (2) The CSR initialisation equals `configure_fabric()`

My `plattrace` run compiles `milan_baremetal.c` as shipped, by gate 35's own host run. All five shipped configs give 15 writes equal to `configure_fabric()`'s, address and value, and the arm's three plants are caught (`receipts/raw/plat_arms.log`).

The words come from `ctrl_plat_gen.py` via `boot_policy.fabric_constants()`, and the bus map from the SoC's `csr.csv`:
- I planted three defects in the generator itself, in a disposable copy: two fields swapped, the VID taken from the AAF word, and the CRF word zeroed. The trace caught all three (`receipts/raw/gen_probe.log`).
- The register offsets in `ctrl_plat_csr.h:31-60` are hand-listed. The trace proves them against `milan_baremetal.c`'s own defines, because it compares addresses.

### (3) The block-RAM ledger (ruling 6505997821)

My own links reproduce the PR's figures (`receipts/images/`). They use the boot SoC's own `csr.csv`, exported without CPU generation, and the pinned SDK.

| Point | Platform RAMB36 | Fixture RAMB36 |
|---|---:|---:|
| 1x1, one interface | 39.0 | 37.0 |
| 1x1, two interfaces | 42.0 | 40.5 |
| 8x8, one interface | 52.0 | 50.5 |
| 8x8, two interfaces | 59.0, under `platform-8x8-two-interfaces` | 57.5 |

- At the largest point: `rom` 125,040 B in 126,976, and `sram` 113,936 B in 114,688.
- My four platform ELFs are **byte-identical** to the author's published images at `99de3a02` (`elf_digests.txt`).
- Six refusals exit 2:
  - the platform's largest image with no override, and with the fixture's override;
  - the platform's override at its three other points;
  - the platform's override on the fixture's image.
- `test_ctrl_memory.py` ends `RESULT: PASS`: 47 mutants, and 6 of 6 planted widenings caught.
- The product `add_ctrl_memory` names no override (`milan_soc.py` is unchanged).
- Section 5's region needs and its by-part rows match my measurements, and each column sums exactly to its delta.

### (4) The console (D6), its spans, and clocks

- The pass bound holds: 16 bytes in, 16 out, one command, never into a full FIFO, and the command runs only with 320 B of ring room. The K4 tests and six mutants cover it.
- I fed `scripts/baremetal_uart_smoke.py`'s own `grade()` a host transcript with live-looking register words. Every check passes; `fabric-enabled` fails, as ruled (`console_grade.log`).
- The widest `milan_status` response is 309 B, against 320 (`console_wide.log`).
- The span figures (84.389 / 184.610 ms; 21.6 / 40.2 ms; gaps of at most 2.2 ms against 500 ms and T_svc) come from the author's published simulation receipts at `5edbba1d` (author-r1). They are on the same firmware C bytes as this head: `git diff 5edbba1d..99de3a02` touches only the ledger, its test and docs.
- Their clocks are consistent: 4,219,428 CPU cycles at 84.389 ms, and 9,230,494 at 184.610 ms, are 50 MHz. The bus cycles are 100 MHz.
- The boot README states "CPU at 50 MHz and its bus at 100 MHz". The PR body's figures carry no clock (R-3).

### (5) The four accepted limits

All four are stated in the PR body's "Known limitations" and in the platform's README:
- graders on a split image owed to S12;
- SRP live configuration deferred until `srp_mbx.c` lands;
- the split boot as a recipe until #784 step 2;
- the deferred items: ACMP asking-failed, GET_AS_PATH, F1 addresses, and the face acknowledgement.

### (6) Mutants, plants and coverage

- The 37 platform mutants, run through the control campaign's own `campaign()` in three members: **37 of 37 caught**.
- Every test of `test_plat*.cpp` is named by a defect.
- 18 reviewer probes were added, and 13 are caught. Of the five escapes:
  - one does not compile, and is discarded;
  - four are confirmed complete passing runs, rc 0 (`escape_check*.log`).
- The `plat` arms all pass: `plat`, `platboot` at one and two interfaces, `platrv32` and `plattrace`.
- `fw_coverage.py --check` ends `PASS (35 files)`. The platform files are at 100 % of lines and branches after the three documented exclusions, which I read and found justified.
- The boot simulation's two plants are the author's receipt (`kept-from-a697-at-5edbba1d`). I could not run the simulation (Limits).

## Findings

### F-1: MINOR, under Robustness, Tests and RTL (indexing)

- **Where:** `sw/firmware/ctrl/plat/ctrl_plat_console.c:129-137`, `is()`.
- **Defect:** the compare loop has no stop at the command's terminator. A received line that carries a NUL byte where a command name ends (`milan_status\0...`) makes `is()` read `command[n]` past the string literal, up to `CTRL_PLAT_LINE_MAX - strlen(command) - 1` bytes.
- **Evidence:** C11 6.5.6 makes this undefined behaviour. The issue requires portable C11, and the Robustness lens covers malformed input.
  - AddressSanitizer reports `global-buffer-overflow ... READ of size 1 ... in is ctrl_plat_console.c:133`, called from `run` and `ctrl_plat_console_poll` (`receipts/raw/console_nul_asan.log`, probe `scripts/r733_console_nul.c`).
  - A UART yields 0x00 on a break or line noise.
  - No test sends a NUL byte.
- **Impact:** an out-of-bounds read of adjacent read-only bytes on external input.
  - On this core it reads ROM, and accepts or refuses the line depending on what follows the literal.
  - On a ported hard core with region protection it may fault.
- **Required outcome:** a line containing a NUL, or any byte the commands lack, is refused without reading past the command string. For example, `is()` stops at `command[n] == '\0'`, or `take()` discards a line containing NUL. A test sends such a line and fails on the current code.
- **Verification:**
  - the ASan probe is clean;
  - a named test (K3) fails with the old `is()` restored;
  - a shipped mutant reverting the fix is caught.

### F-2: MINOR, under Tests

- **Where:** `sw/firmware/ctrl/test/test_plat_boot.cpp` (B1, and the fixture's blank flash); `plat_mutants.py`.
- **Defect:** two reviewer-planted defects in `ctrl_plat.c` pass all nine boot tests at the shipping shape (rc 0, `receipts/raw/escape_check.log`):
  - `r733-saved-state-after-mailbox-open` moves `nvm_store_boot` after `ctrl_app_open_held`. The code says "Steps 6-7: the saved state, bindings first, before anything opens" (`ctrl_plat.c:252`), and the README's step table places 6-7 before 8.
  - `r733-store-service-not-bound` drops `ctrl_loop_add_tick(..., nvm_store_service)` (`ctrl_plat.c:258`), so the saved state is never written back on change.
- **Evidence:** AGENTS section 6, Tests: each test can fail for the defect it claims to detect, and real integration wiring is tested where practical.
  - `plat_mutants.py` claims "the boot's order of Milan v1.2 5.6.1, caught by the step order".
  - `plat/README.md` claims `platboot` tests "the boot and composition ... every bus access in one order".
  - The flash model's accesses are outside B1's order, and no platform test makes a persisted change after ready.
  - S3 composes F1 (assignment 6493622258). Valid, torn and wrong-version slots are S4's, but the composition's order and its binding are this PR's code.
- **Impact:** a regression that applies the saved state after the mailbox opens, or that silently disables F1's write-back in the platform image, would merge green.
- **Required outcome:**
  - a platform test fails when the saved-state boot runs after the mailbox opens;
  - a platform test fails when a persisted change after ready never reaches the flash through the loop;
  - each has a named shipped mutant.
- **Verification:** both probes in `scripts/r733_plat_campaign.py` (EXTRAS) are caught by a named test.

### Suggestions (non-blocking)

- **S-1:** a test that formats the widest `milan_status` and asserts it is at most `CTRL_PLAT_RESPONSE_MAX`. Planting `RESPONSE_MAX 200` escapes today; the constant itself is correct (309 against 320).
- **S-2:** `CTRL_PLAT_SNAPSHOT_SPIN` (`ctrl_plat_csr.h:77`) is unobservable on the host and in the simulation, whose snapshot lands at once. Planting 0 escapes. The bench lane should confirm the wait on hardware.
- **S-3:** the policy write that mirrors `configure_fabric()` sets `MAAP_CTRL[0]` for about a microsecond, until MAAP's one-owner report clears it. With the link up, `KL_maap.sv:24-26` sends one PROBE at once on enable.
  - This follows from the frozen acceptance ("writes exactly what milan_baremetal writes"), so it is not a defect here.
  - Record it in `plat/README.md` step 3, and take it to S6/S12 for a ruling on whether the split policy should write the enable clear.

## Residue (wording only; the manager carries it to the checklist)

- **R-1, comment rule (owner 2026-10-15):** new lane names and issue-comment or ruling IDs in source comments and docstrings of the delta. Fix: keep `#665` and the decision IDs (D3, D6), and drop the lane and comment IDs.
  - `(#665 S3)` in the headers of `ctrl_plat.h:5`, `ctrl_plat_csr.h:4`, `ctrl_plat_console.h:4`, `ctrl_plat_io.h`, `ctrl_plat_main.c`, `ctrl_plat_mmio.c`, `ctrl_plat_gen.py:4`, `plat_arms.py`, `plat_mutants.py` ("S3's"), `plat_trace.py` ("S3's acceptance"), `ctrl_plat_image.py` ("the measurement S3 owes"), `plat_bus.*`, `test_plat*.cpp`, `boot_soc.py` ("S2's test-only split SoC"), `run.py` and `sim_main.cpp`.
  - `issuecomment-6409738976` at `ctrl_plat_console.h:8`.
  - "lane S14" at `sw/litex/ctrl_memory.py:210` and `:218`, and "ruling 6505997821, amending 6425357821" in the new `Ledgered` reason string at `:219`.
  - The ruling IDs at `sw/litex/ctrl_memory_ledger.py:7-8`.
- **R-2:** `tb/verilator/ctrl_split_boot/README.md:96` says the 26.5 ms wire time is "longer than any span here", but the 8x8 span is 40.209 ms. Fix: "longer than the 1x1 status span (21.6 ms); the 8x8 span (40.2 ms) is the loop's".
- **R-3:** the PR body's timing figures (Status "Simulation", and the CPU budget limit's ms deltas) state no clock. Fix: add "(split CPU 50 MHz, bus 100 MHz; simulation)".
- **R-4:** `ctrl_plat.c:64-65` says "so no source reports an address the window does not hold". At two interfaces, interface 1's sources report their range with no window (B8 asserts it). Fix: "no interface-0 source ...; interface 1 has no window (ctrl_plat.h)".
- **R-5:** the PR body's row for `c787a3ce` says "the five platform files at 100 %". The commit also re-records `aecp.c`, `aecp_commands.c`, `aecp_face.c`, `aecp_mbx.c`, `ctrl_app_aecp.c` and `mbx.c`, which this PR does not change. Say so.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat.c:226-282` against `ARCHITECTURE_HW_SW_SPLIT.md` section 2 and ADP-after-AECP (B1, B5, B6 and three mutants, all caught); `plattrace` 5 of 5 configs equal to `milan_baremetal.c` `configure_fabric()`, plus generator plants 3 of 3; ledger 39.0 / 42.0 / 52.0 / 59.0 with byte-identical ELFs and six refusals; the PR body's limits (focus 5) | R733-1 | `99de3a02` |
| RTL | UNCLEAN (F-1, indexing) | No HDL in the diff (`git diff --stat`). Firmware architecture: the `ctrl_app` API addition, the CSR offsets against `REGISTER_MAP.md` and `milan_baremetal.c`, `ctrl_plat.h` ports and indexing, `KL_maap.sv` enable behaviour (S-3), `sim_main.cpp` seeded file | R733-1 | `99de3a02` |
| Robustness | UNCLEAN (F-1) | Console malformed, overflowed, NUL and widest input (ASan probe); refused stages B2-B6; the two-interface window drop; TOD retries | R733-1 | `99de3a02` |
| Tests | UNCLEAN (F-1, F-2) | 37 of 37 shipped mutants caught; 18 reviewer probes (4 real escapes); `plat` arms PASS; `fw_coverage --check` PASS (35 files); `test_ctrl_memory` PASS | R733-1 | `99de3a02` |
| Docs | CLEAN (residue R-1 to R-5 only) | `plat/README.md`, `ctrl_split_boot/README.md`, `SPLIT_CONTROL_MEMORY.md` sections 3-6 (figures re-measured), `ARCHITECTURE_HW_SW_SPLIT.md` delta, the MAAP, SRP and ctrl READMEs, the PR body; doc_paths, doc_style, docs_check, hygiene, py and cpp idiom gates rc 0; `git diff --check` clean | R733-1 | `99de3a02` |

## Real limits of this round

- **The split boot simulation was not run.** Its export asks for VexiiRiscv netlist `VexiiRiscvLitex_0079ee11ee662fec9292f1041b17ad63`, which is not cached on this host. The author's receipt names `..._903b010f...`, and I could not reproduce that hash's inputs.
  - Generating the netlist would write into the shared LiteX install and the sbt caches, so a refusing `sbt` stub guarded the run. It refused, rc 2 (`split_boot-1x1.log`).
  - The shared netlist directory is unchanged (`vexii_find_baseline.sha`).
  - BOOT, TRACE and UART timing therefore rest on the author's published receipts at `5edbba1d`. The host equivalents I ran instead: `platboot` B1, `plattrace`, the console against `grade()`, and the identical ELFs.
- **Not run:** the full firmware self-test shards; the AECP and SRP campaigns; `ctrl_boundary`; `test_builder`; `behave`; the CPU budget harness; `check_em_dash.py`, whose pinned Markdown renderer `html5lib` is absent.
- Physical calibration was not run, and field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed.
- **Hosted contexts at this head** (`hosted_snapshot.txt`): 19 succeeded, 1 skipped (nightly physical), 28 in progress or queued. Acceptance of those is the manager's.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (source base `f4c9ad4f`, live dev `1e80128f`) with its builder and native banks.
- Carrying R-1 to R-5 to the residue checklist.
- Re-review after F-1 and F-2 are fixed.

## Receipts

Every published file is listed in `MANIFEST.sha256`. The probe scripts are in `scripts/`. `r733_plat_campaign.py` gained a `main()` guard after its run, so that `r733_escape_check.py` can import its table; its behaviour when run directly is unchanged.

Clone integrity after every probe (`receipts/raw/clone_integrity.txt`):
- the worktree and index equal HEAD, with nothing untracked;
- the mode, blob and path listing of the index equals HEAD's tree;
- all five checked-out gitlinks match HEAD and are clean.

R733-1 FINISHED
