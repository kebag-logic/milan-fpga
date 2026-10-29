# [A683l] #665 lane S2b round 10: merge origin/dev-soft-core f4c9ad4f into the lane (HANDOFF)

**Status: REVIEW READY** (2026-10-29). Head `f884c7e9fb71cdb94c12e3228b1412801c34e1f4`: the merge of `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f` into round 9's `bf1773c0eabf0ba7fa1b1268c2a714e6b636e6eb`, and four commits on it. Every composed row the CPU decides fits its own bound at both points, on both arms, with both drafts staged and without them. The STOP condition does not hold: S1's contract 2.3 and the record mover both hold.

- Branch `665-s2b-cycles`, local; nothing pushed by this session. One merge commit, no rebase, no force.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked). Lane base `origin/dev-soft-core` `e76a755a` is an ancestor (checked; not dev). The PR targets `dev-soft-core`.
- No git command changed a submodule of the lane. Each submodule was checked to be its own top level with its own origin before use; the drafts were staged in scratch clones only.
- Assignment: issuecomment-6502579312 (`ASSIGNMENT-A10-6502579312.md`). TAKEN: issuecomment-6502704021 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6507081649 (`REVIEW-READY-COMMENT.md`).
- CPU and memory:
  - every heavy job ran as its own transient unit (MemoryMax 6 to 8 GB) on this session's 16-31, four CPUs each;
  - the full sweep ran as four `native-shards.py` units on 0-15, the range `cpu_ranges.py pick` gave (0-3, 4-7, 8-11, 12-15), started at 45 GB MemAvailable;
  - MemAvailable stayed above 25 GB.
- Vivado: the CPU's netlist is unchanged (section 4), so no route. Only the xvlog front-end gate, under `$VIVADO_LOCK`, exclusive, after the sweep.

Commits:

| Commit | Subject |
|---|---|
| `c5676878` | Merge dev-soft-core f4c9ad4f, with S1's contract 2.3 faces, port census and AECP face writer, into lane S2b, keeping the record mover, the fetch L1, the word-wise primitives and the min(T_svc, ceiling) grading |
| `7efee8fb` | Rebuild the face core's descriptor index around the face test's CLOCK_DOMAIN move, so its no-clock check reaches a missing clock again, and record the firmware coverage at the merge, every line and branch taken |
| `db77201b` | Drop the size fixture's a_stream, which contract 2.3's face replaced, from the split image's hot list, so the merged split image links |
| `51fa5f18` | Keep the merged AECP plant table, the CPU budget harness self-test and its scenario within the Python idiom gate's module length and the image builder's main within its function length |
| `f884c7e9` | Record every composed row and the CPU budget harness's controls at the merge with contract 2.3's face writer, and the four points' planned block RAM after it |

## Contents

1. Outcome against the assignment
2. The merge: each conflict, how both sides were kept (file:line, reason)
3. New checks, planted defects and failing words
4. Method
5. Measurement
6. Gates
7. Findings, conflicts, decisions needed
8. Run history

## 1. Outcome against the assignment

| Item | Outcome |
|---|---|
| 1. Merge `origin/dev-soft-core` into `665-s2b-cycles`: one merge commit, no rebase, no force | `c5676878`, parents `bf1773c0` and `f4c9ad4f`. The eleven conflicting files of the assignment, and no other |
| Keep S1's contract 2.3, face census and face writer | Kept whole: `KL_mbx`'s face ports in the product SoC and the harness's SoC, the census, `aecp_face.c`, the acknowledged-state model (`swap`, `refuse`, IN_PROGRESS) and its 59 plants. The generated mailbox files are S1's, and `gen_mailbox.py --check --crosscheck --selftest` holds them (section 6) |
| Keep the record mover, the fetch L1, the word-wise primitives and the `min(T_svc, ceiling)` grading | Kept whole: `KL_mbx_wb` reaches `KL_mbx` through `KL_mbx_dma` in both SoCs; the 16 KiB two-way fetch L1 and the 8 KiB data cache (the CPU netlist is the same, `VexiiRiscvLitex_c05c5a8e`); `ctrl_mem.c` and the in-place window accesses, which S1's new accesses now use too; `grade.budget_ms` and `T_SVC_MS = 20.0` |
| The mailbox contract regenerated through `gen_mailbox.py` only | The lane changes no contract source; every generated file is S1's, and the generator's `--check --crosscheck` finds them current |
| 2. Round 9's full gate set and the full sweep (four shard units) at the merged head | Section 6 |
| Every composed row at both points, both arms, with and without the two drafts | Section 5: 8 legs, 0 refusals; each leg's misses are exactly the six egress-held instances |
| Re-route the split CPU only if the merge changes its netlist | It does not: every leg and control builds `VexiiRiscvLitex_c05c5a8e0bd42fc384567409f2a37e64`, round 9's netlist. No route |
| 3. REVIEW READY at the merged head, PR-BODY: base `dev-soft-core`, "Relates to #665" | Yes, at `f884c7e9` (`REVIEW-READY-COMMENT.md`); `PR-BODY.md` targets `dev-soft-core` with "Relates to #665" |
| STOP if a row misses its bound, or if S1's contract and the mover cannot both hold | Neither: every row the CPU decides fits; the least margin is the 8x8 last SRP record's, 1.05 ms under 18 ms |

## 2. The merge

### 2.1 The eleven conflicting files (`c5676878`)

| File | Lane's side | S1's side (with S2c's harness arms) | Resolution |
|---|---|---|---|
| `sw/firmware/ctrl/aecp/aecp_internal.h:16-17` | `aecp_index` | `aecp_other_lock` | both declarations |
| `sw/firmware/ctrl/aecp/aecp.c:55-85` | `used`, `relist`, `list`: the live event list and the registration mask | `applied`, the face's acknowledgement port | both blocks. The only writer of an event's pending bits is still `aecp_changed`, which links the event into `aecp.live`; S1's `swap` and `aecp_keep` restore values, overrides and lock state, never a key or a pending bit |
| `sw/firmware/ctrl/aecp/aecp_commands.c:44-67`, `:641-646` | `body()`: each command writes exactly its fixed body | `aecp_other_lock`; GET lock reports the lock in force | both. GET's body through `body(out, bytes, 20u)` with S1's `locked \|\| unlocked`. Every command still writes all the `*bytes` it answers with, so S1's `refuse()`, which answers a held command again into `a->response + 38`, never sends a stale byte |
| `sw/firmware/ctrl/test/test_aecp.cpp:171-217` | `rekey`, `stale_key` and `TearDown`: every Core case checks `aecp_find` against a scan | `set_system_id` | both. S1's two face fixtures' `TearDown`s (`:2342` `Face`, `:2919` `AppFace`) now chain to `Core::TearDown` and `Nvm::TearDown`, as the lane's `Nvm` and `Mailbox` ones do, so the index check runs for S1's cases too |
| `sw/firmware/ctrl/test/aecp_mutants.py` | 15 index and list plants | 59 face plants | both lists. Each of the 168 defects' text occurs exactly once in its merged source (checked) |
| `sw/firmware/gtest/coverage.ratchet` | the lane's rows | S1's rows | regenerated by `fw_coverage.py --write` (`7efee8fb`, section 2.2) |
| `sw/litex/milan_soc.py:2656-2768` | `CtrlMailboxDma`, `add_ctrl_mailbox_dma` | `ctrl_mailbox_face_ports` | both. `KL_mbx` takes its host port from the mover and its face ports from `ctrl_mailbox_face_ports`; `CtrlMailbox`'s docstring states both |
| `tb/verilator/ctrl_service_budget/split_soc.py:19-37`, `:192-212` | the mover between `KL_mbx_wb` and `KL_mbx`, the pads on `KL_mbx`'s side | the face ports, `slowest_ack` at `FACE_ACK_CYCLES` | both: `KL_mbx_wb` drives the mover's CPU port, `KL_mbx` takes the mover's host port and S1's face ports with the slowest acknowledgement; the module docstring states both |
| `tb/verilator/ctrl_service_budget/build.py:51-53` | the control comment at the 20 ms budget | the line reference | the lane's text, the reference at the merged page's SHUTDOWN row (`MAILBOX_SPLIT.md:523`) |
| `tb/verilator/ctrl_service_budget/README.md` | the budget sentence, the mover, the 10 ms grading note | the ledgered point, the acknowledgement, the face hookup, the head note | each side's text. The lane's "`milan_soc.CtrlMailbox` and its idle tie-offs are not used" is dropped, since the face ports now come from `milan_soc.ctrl_mailbox_face_ports` |
| `docs/reference/FR_NFR.md:6-9`, `:346`, `:377`, `:386-390` | the 20 ms table, NFR-SCOUT-01's summary (RV32IM, 16 KiB fetch L1, 8 KiB data cache) | IN_PROGRESS adopted for a change of face state; S2c's summary (4 KiB, no data cache) | the lane's rows and summary, since its NFR-SCOUT-01 row is the later amendment; S1's IN_PROGRESS obligation under the approved rule, so that path's bound is `min(T_svc, 12 ms) = 12 ms`; a row for it in the bound table (section 7, for review) |

### 2.2 Semantic conflicts the textual merge did not show

Each was found by a gate at the merged tree; the refusal is in `receipts/merge-findings/`.

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/mbx/mbx.c:274`, `:290`, `:313`, `:325`, `:366`, `:370`, `:372`, `:374`, `:379`, `:380` (`c5676878`) | S1's ten new window accesses (`mbx_pub_licensed`, the face writes, `mbx_face_busy`, `mbx_face_commit`, `mbx_win_read`) through the lane's `mbx_bus_read32` / `mbx_bus_write32` | The lane builds the driver for the window with its accesses in place (`mbx_mmio.h`). S1's direct `mbx_hal_*` calls did not link in `test_mmio_driver` (`undefined reference to mbx_hal_read32`), and would cost a call a word on the split core |
| `sw/firmware/ctrl/test/aecp_mutants.py` (`c5676878`) | S1's `face-commit-not-waited` and `face-window-read-slow` anchors and replacement on `mbx_bus_*` | They plant text in those lines |
| `tb/verilator/ctrl_service_budget/{README.md,scenario.py,grade.py,build.py}` (`c5676878`) | `MAILBOX_SPLIT.md:499-506`, `:649-661`, `:757-762`, `:506` to `:516-523`, `:666-678`, `:773-778`, `:523` | The merged page carries both sides' additions; each reference again names its table |
| `sw/firmware/ctrl/test/test_aecp.cpp:2807-2811` (`7efee8fb`) | `Face.DamagedDescriptorsAndAnInterfaceTheBuildLacksPublishNothing` moves the CLOCK_DOMAIN to configuration 1 through `rekey`, rebuilding the face's own core's index (`aecp_index(&adapter.core)`) as well, and back | The lane's `aecp_find` answers from an index built at init; a key changed after it needs `aecp_index`. Without it the merged face still found the clock, so "no CLOCK_DOMAIN in force" passed without reaching a missing clock |
| `sw/firmware/gtest/coverage.ratchet` (`7efee8fb`) | regenerated by `fw_coverage.py --write`: 33 files, every line and branch taken | its generator |
| `sw/firmware/ctrl/plat/ctrl_split.ld`, `ctrl_split_hot.txt:11-13` (`db77201b`) | the hot-list entry `ctrl_aecp_image a_stream` removed from both, the header saying why | S1 replaced the size fixture's stream observation with the face's port, and the split link refused the entry. Removing a stale entry from both files is round 7's practice (the donor's `__lshrdi3`); 202 entries remain, in the recorded order |
| `sw/firmware/ctrl/test/aecp_index_mutants.py` (new), `aecp_mutants.py:13`, `:853` (`51fa5f18`) | the lane's 15 index and list plants as their own table of `defect()` arguments, which `aecp_mutants.DEFECTS` appends | Merged, `aecp_mutants.py` was 1,018 lines, over the Python idiom gate's 1,000 (lane 721, S1 854). `acmp_mutants.py` appends `acmp_review_mutants.py` the same way. 168 defects, the same names |
| `tb/verilator/ctrl_service_budget/selftest_maximum.py` (new), `selftest.py:54` (`51fa5f18`) | `maximum_checks`, unchanged, in its own module, which `selftest.py` imports | Merged, `selftest.py` was 1,033 lines (lane 981, S1 980). The function uses only `run`; `selftest_mutants.py` never patches `selftest.py` |
| `tb/verilator/ctrl_service_budget/scenario.py:90` (`51fa5f18`) | the lane's two-line T_svc comment in one | Merged, `scenario.py` was 1,001 lines (lane 1,000, S1 1,000) |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:132-137`, `:203` (`51fa5f18`) | the lane's memory-primitive check out of `main` into `memory_calls_nothing` | Merged, `main` was 102 lines, over the gate's 100 (S1 added two). The images are byte-identical (section 5) |
| `sw/firmware/ctrl/aecp/README.md:195-198`, `tb/verilator/ctrl_service_budget/README.md:885` (`51fa5f18`) | each new module named where its parent is | Documentation |

### 2.3 The record at the merged head (`f884c7e9`)

| file:line | Change | Reason |
|---|---|---|
| `docs/design/SPLIT_CONTROL_MEMORY.md:204-216` | section 5: the four points' planned block RAM at the merge, against `bf1773c0` | Measured (`receipts/images/`) |
| `SPLIT_CONTROL_MEMORY.md:618` | section 11: 202 hot-list entries since the face replaced `a_stream` | `db77201b` |
| `SPLIT_CONTROL_MEMORY.md:990-1023` | section 13, "With contract 2.3's face writer": the merge, the acknowledgement at the bound, the rows at both points, both arms, with and without the drafts, the margins, and that no row answers IN_PROGRESS | Item 2 |
| `SPLIT_CONTROL_MEMORY.md:26`, `:1053-1056` ("What is left") | the contents entry; the least margins with the face writer | Same |
| `tb/verilator/ctrl_service_budget/README.md:589`, `:1005-1025` | the merged 1x1 image's `.data` load address (0x19428); the controls' figures at this head, with round 9's and S1's attributed by commit | Measured (`receipts/controls/`) |

## 3. New checks, planted defects and failing words

No check is new in kind. The merge extends two of the lane's checks to S1's code, and each extension is shown to fail without it:

| Check | Planted defect (the state without the change) | Failing words (`receipts/merge-findings/`) |
|---|---|---|
| The MMIO driver's link (`test_mmio_driver`, firmware gate) over S1's face functions | the ten accesses S1 added back on `mbx_hal_*` | `REFUSED: test_mmio_driver does not link: ... in function 'mbx_pub_licensed': ... undefined reference to 'mbx_hal_read32'` |
| The coverage ratchet over `aecp_face.c` with the face test's key move rebuilding the face core's index | the move without `aecp_index`; and with `rekey` rebuilding only the fixture's own core | `REFUSED: sw/firmware/ctrl/aecp/aecp_face.c: branches 151/152 fell below the recorded 144/144` (both) |
| The split link's hot-list gate (`ctrl_hot.py` LINKED) over the merged image | the hot list before `db77201b` | `REFUSED: LINKED: hot-list name *-ctrl_aecp_image.o(.text.a_stream) is no section of the linked image` |
| The Python idiom gate over the merged modules | the tree before `51fa5f18` | `FAIL: long function 10 > ratchet 9`, `FAIL: long module 13 > ratchet 10` |
| The index check (`Core::TearDown`'s `stale_key`) on S1's `Face` and `AppFace` cases | (the lane's existing `key-changed-after-init` plant) | caught by `Indexed.FindAnswersEachKeyAsAScanOfTheModel` with `a key changed after aecp_init needs aecp_index`, as before |

The firmware self-test's 168 AECP plants, the harness's self-test (80 plants) and every other driver run at the head (section 6).

## 4. Method

- **The harness:** S2's, the four backlog groups (`backlog`, `backlog-adp`, `backlog-adp-refill`, `backlog-owed`), at 1x1/1if and 8x8/2if, arms A and B (`--variant answering-ports`), `--record-budget-findings`. Each leg ran from a clean clone at `db77201b` with round 8's labelled profiling variant re-based on the merge (`receipts/variants/harness-profile-merged.patch`: the same added and removed lines as round 8's `harness-profile-cumulative.patch`, only the context moved), `CSB_CPU_HZ=100000000`; the bus stays 100 MHz.
- **The legs** (`receipts/measure/`, each `label.txt`): `N10-<arm><point>` the branch; `D10-<arm><point>` with both drafts staged as round 8 staged them: lwSRP `fc06e7c0` and tsn-c-stack `6532c3b0` by gitlink, from round 9's scratch clone, `ctrl_arms.LWSRP_REV` moved, the runtime's `__lshrdi3` hot-list entry removed (round 8's `parent-with-*.patch`).
- **`db77201b` against the head:** since then the image builder's `main` moved one check into a helper, the harness's self-test split a module, `scenario.py` changed a comment, and the rest is Markdown. The head's arm A images at both points, with and without the drafts, are byte-identical to the legs' (`receipts/images/images-at-head.md`).
- **The CPU:** every leg and control records `VexiiRiscvLitex_c05c5a8e0bd42fc384567409f2a37e64` with round 9's generator arguments, so the split CPU's netlist is round 9's, and no out-of-context route ran.
- **The analysis** (`scripts/rows9.py`, round 9's): each composed row's worst instance over the four groups, graded against min(T_svc, the family's ceiling) + W from the lane's `scenario.py`, beside round 9's legs (`receipts/rows/`).

## 5. Measurement

Every composed row, worst instance over the four groups, ms, arm A / arm B, bold over its own bound (`receipts/rows/rows-1x1.md`, `rows-8x8.md`; SPLIT_CONTROL_MEMORY section 13, "With contract 2.3's face writer"):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.51 / 5.30 | 4.60 / 4.76 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 3.93 / 3.77 | 3.28 / 3.41 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 3.97 / 3.81 | 3.26 / 3.44 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 10.25 / 10.43 | 9.36 / 9.98 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 10.53 / 10.40 | 9.97 / 10.19 | 16.95 / 16.32 | 15.60 / 15.40 |
| An ACMP command behind a full ACMP ring | 20 | 4.07 / 4.04 | 3.64 / 3.70 | 8.13 / 8.15 | 7.64 / 7.45 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.02 / 2.87 | 2.58 / 2.60 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 1.24 / 1.23 | 1.14 / 1.15 | 2.09 / 2.10 | 2.01 / 2.02 |
| AECP record, last, in the owed window | 20 | **62.81** / **62.90** | **62.84** / **62.83** | **65.03** / **64.94** | **65.02** / **65.09** |
| A response with 7 frames owed ahead of it | 20 | **61.99** / **62.06** | **62.01** / **62.00** | **63.70** / **63.64** | **63.69** / **63.74** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

- Every row the CPU decides fits its bound at both points, on both arms, with the drafts staged or not. The STOP condition does not hold.
- The least margin is the 8x8 last SRP record's: 1.05 ms under 18 ms without the drafts (arm A, 16.95), 0.56 ms less than round 9's 1.61; 2.40 ms with them (arm A, 15.60).
- The 8x8 last AECP record keeps 4.16 ms without the drafts (arm B, 15.84) and 5.39 ms with them.
- At 1x1 every such row keeps at least 7.47 ms (the last SRP record, 10.53 ms).
- The first records take at most 5.12 ms, the refilling bucket's row at most 0.23 ms.
- Each leg's run: `4 groups graded, 0 refusals, 6 budget misses`. The six are exactly round 9's egress-held instances: `backlog.owed`, the four `backlog.owed_behind*` (never answered), and `backlog-owed.service.aecp.last` (each `run.log`).
- Against round 9 the rows moved by -0.05 to +0.98 ms at 1x1 and by -0.91 to +0.75 ms at 8x8, with and without the drafts (`receipts/rows/`).

The controls (`receipts/controls/`), at the head, product clocks:

| Control | Planted defect | Failing words |
|---|---|---|
| `slow-adp-rx`, cacheless core | ADP's receive handler spins 32,000 turns before it hands the record on | `BUDGET control.discover.if0: 48.697 ms over its budget 20 ms`, `CONTROL slow-adp-rx caught: every control path missed its budget` (unplanted 0.056 ms) |
| `slow-adp-shutdown`, cacheless core, `shutdown-entry` arm | Disabling ADP spins 32,000 turns before its ENTITY_DEPARTINGs | `BUDGET control.shutdown.if0: 48.933 ms over its budget 20 ms`, `CONTROL slow-adp-shutdown caught` (unplanted 0.292 ms) |
| `as-built`, cacheless core and the split's caches | The generator handed the SoC's regions unchanged | `CONTROL as-built caught: an instruction or load access fault (cause 1 or 5)`, `TRAP 166 0 5 00000020` (cacheless), `TRAP 390 0 5 00000020` (cached) |

Behind the split's own caches the two spins take 17.322 and 17.411 ms and escape (rc 1), as round 9 found: the evidence that the controls are the cacheless core's, not gates.

The four points' planned block RAM (`receipts/images/images-four-points.md`): 36.5 / 40.0 / 50.0 / 56.5 RAMB36 at the head against 35.0 / 38.5 / 48.5 / 55.0 at `bf1773c0`. No point is over its cap; 8x8 with two interfaces is half a tile over 56, within the 57.5 ledgered and owed to S14.

## 6. Gates

Each gate ran on a clean clone of its head (`scripts/clone.sh`), one unit each on four of 16-31 unless named. Its log is in `receipts/gates/` with host paths replaced; `receipts/gates/stale/` keeps the runs the host's scratch cleanup cut short. "Since" says what changed after a gate's head.

| Gate | Command | Where | Result | Receipt |
|---|---|---|---|---|
| Firmware self-test, all four shards (every firmware mutant driver; the service-bounds arm that pins MAILBOX_SPLIT's table; the hot list's arm) | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 4` | `f884c7e9` | rc 0, `test_ctrl_firmware: PASS` each; shard 0 `== ctrl service bounds: checks: 46   failures: 0 ==`, `[ok] arm hot`, `named plants not caught: none`; shard 1 `mutants: 553 of 553 caught`; shard 2 the 168 AECP plants, each `[ok]`; no `ESCAPED` in any shard | `selftest-shard0.log` to `selftest-shard3.log` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check` | `f884c7e9` | rc 0, `firmware coverage: PASS (33 files)` | `fw_coverage_check.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | `f884c7e9` | rc 0, `RV32 build self-test: 25 checks PASS` | `fw_rv32_selftest.log` |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | `f884c7e9` | rc 0, `selftest: 0 arm(s) failed` | `gen_mailbox.log` |
| rtl-fast `publication-census` (S1's face census among its rules) | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4`, sv2v v0.0.12 and Yosys 0.66 named by `SV2V` / `YOSYS` | `f884c7e9` | rc 0, `RESULT: PASS`; `mutations: 0 of 43 rule(s) no arm proves` | `publication_census.log` |
| RTL lint ratchet | `python3 scripts/lint_rtl.py --check` | `f884c7e9` | rc 0, `LINT GATE: PASS (89 violation(s) <= ratchet 89; ...)` | `lint_rtl.log` |
| Vivado front-end, under the lock, after the sweep | `python3 scripts/xvlog_gate.py --check` | `f884c7e9` | rc 0, `xvlog gate: PASS (0 finding(s) == ratchet; 0 hdl/, 0 pinned processors)` | `xvlog_check.log` |
| Yosys: the mover, the adapter, the mailbox | `syn/yosys/run.sh --top KL_mbx_dma --top KL_mbx_wb`; `--top KL_mbx` | `f884c7e9` | rc 0, `[PASS] KL_mbx_dma cells=2302` (round 9's count), `[PASS] KL_mbx_wb cells=5`, `[PASS] KL_mbx cells=420989`, `TAP-PURITY RESULT: PASS` | `yosys-KL_mbx_dma-KL_mbx_wb.log`, `yosys-KL_mbx.log` |
| CPU option test | `python3 sw/builder/test_soc_options.py` | `f884c7e9` | rc 0, `RESULT: PASS` | `soc_options.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `f884c7e9` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the historical Arty report not on disk, as in rounds 3 to 9 (1,985 s) | `builder_require_rv32.log` |
| rtl-fast `firmware-boundary` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `f884c7e9` | rc 0, `ctrl_boundary: PASS` (`0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved`). S2's harness classification (`e0e1b464`) came with the merge, so round 9's refusal is gone; the two new modules need no entry | `ctrl_boundary_without_verilator.log` |
| rtl-fast `firmware-verilator` (the mailbox suite among its builders) | `... --only verilator` | `f884c7e9` | rc 0, `ctrl_boundary: PASS` | `ctrl_boundary_only_verilator.log` |
| The split memory test | `python3 sw/litex/test_ctrl_memory.py` | `f884c7e9` | rc 0, `RESULT: PASS` | `test_ctrl_memory.log` |
| The full sweep, four `native-shards.py` units on 0-3, 4-7, 8-11, 12-15 | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, pinned Verilator 5.050 and sv2v v0.0.12 | `51fa5f18` (since: Markdown only) | rc 0 each (4,689, 3,955, 5,236, 3,717 s): 15, 17, 16 and 16 suites pass, 64 of 64; 250,913 + 1,536,446 + 380,086 + 384,995 = 2,552,440 checks, 0 in-suite failures, 0 timed out | `receipts/sweep/sweep-51fa5f18/` (`tally.md`; files over 200 KB in `large-files.txt`) |
| The harness's self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | `f884c7e9` | rc 0, `self-test: 0 failures`; 109 checks, 80 mutants caught | `harness_selftest.log` |
| S2's harness, both points, both arms, with and without both drafts | `run.py --point 1x1/8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings`, arm B `--variant answering-ports` | `db77201b` + the profiling variant, 8 legs (since: section 4) | rc 0 each, `4 groups graded, 0 refusals, 6 budget misses`, the six the egress-held instances | `receipts/measure/` |
| same, a fresh build at the head | `--groups backlog`, 1x1 arm A | `f884c7e9` + the profiling variant | rc 0, `0 budget misses`; its `backlog.log` and image byte-identical to leg N10-A1's | `receipts/measure/final-head-check/` |
| The harness's controls | section 5's table | `51fa5f18` (since: Markdown only) | rc 0 each: `CONTROL slow-adp-rx caught` (48.697 ms), `CONTROL slow-adp-shutdown caught` (48.933 ms), `CONTROL as-built caught` (cause 5), on the cacheless core; `as-built` caught behind the split's caches too | `receipts/controls/` |
| Linked images at four points | `scripts/images.py`, `bf1773c0` against `51fa5f18` (since: Markdown only) | `51fa5f18` | rc 0; planned tiles 36.5 / 40.0 / 50.0 / 56.5, 0 over a cap; arm A's images with and without the drafts byte-identical to the legs' | `receipts/images/` |
| Docs workflow, bare-metal scope, idiom gates (the Python idiom gate among them), `ci_events`, harness self-test, CPU option test, `behave` (96 gates) | `scripts/docs_gates.sh` (`gates_s2b3.py`) | `f884c7e9` | rc 0, `0 of 96 gates nonzero or left the tree dirty`: `docs_check: 0 finding(s)`, `check_em_dash: 0 finding(s) over 3404 added line(s)`, `TOC gate: OK`, the anchors reproduced, `baremetal-only: OK`, `NAMING RATCHET: PASS`, the C++ and Python idioms within their ratchets (`long function: 9 <= 9`, `long module: 10 <= 10`), `ci_events: OK`, the harness `self-test: 0 failures`; `cd tests && behave`: 14 features, 406 scenarios, 1,977 steps passed. The first run stopped at the HDL-reference gates because round 4's scratch interpreter for them was removed from the host during the session; this run used a fresh one installed from `tools/hdl_reference/requirements.txt` with its pinned hashes (`stale/docs-hdlvenv-removed/`) | `docs/` |

Not run:
- lwSRP's own suite on the draft `fc06e7c0`. The draft is unchanged since round 8 and this merge does not touch lwSRP. The scratch build of its unit framework (cgreen 1.6.5, no host package), which rounds 8 and 9 used, was removed with round 8's scratch tree during this session, and the attempt stopped at `Could not find CGREEN_LIB` (`stale/lwsrp-suite-donor-cgreen-removed.log`). Round 9's result stands for the same commit: `Completed "main": 26690 passes`, 3 scenarios, 6 of 6 plants (round 9's `receipts/donor/`). The draft's code runs in the four with-drafts legs.
- the CI command table's checker (`scripts/ci_tool_inventory.py --check`), which needs the CI image's checksum-pinned shell parser, as in rounds 8 and 9. The merge brings S1's and dev's workflow changes unchanged; the lane changes no CI command.
- an out-of-context route of the split CPU: its netlist is round 9's (section 4).

## 7. Findings, conflicts, decisions needed

- **No STOP.** Every row the CPU decides fits its own bound at both points, on both arms, with both drafts staged and without them. S1's contract 2.3 and the record mover both hold: `KL_mbx` takes its host port from the mover and its face ports as `CtrlMailbox` connects them, and the harness acknowledges each commit at `FACE_ACK_CYCLES`.
- **For review: FR_NFR's bound table gains a row** (`docs/reference/FR_NFR.md:346`): "An AECP command answered IN_PROGRESS", ceiling 12 ms (the 120 ms cadence x 10 %), bound 12 ms. It applies the owner's rule, min(T_svc, C), to the path S1 adopted; it changes no approved value. The AECP derivation row (`:377`) and the conclusion (`:386-390`) say the same.
- **Finding: no measured row answers IN_PROGRESS.** The harness acknowledges every commit within its bound, so no change of face state waits; the 12 ms bound has no row on the CPU. The host suites check the cadence with `aecp_service_limit_ns`, 10 ms, which is tighter (round 9's finding about the host suites still holding 10 ms stands). Measuring it needs a late-acknowledging arm and an `aecp-in-progress` family in the harness; not in this round.
- **Finding: the index check does not see a key changed and restored within a case.** `Core::TearDown`'s `stale_key` runs at the end of a case, and S1's face test moved and restored a key in the middle. The coverage ratchet caught it (`aecp_face.c` 151/152); the assertion itself passes either way, since the fixture's clock source index is 0, the value it expects.
- **The Python idiom gate decided four refactors** (section 2.2): each side kept its files just under the limits, and the merge put four over. The splits follow the tree's own precedent (`acmp_review_mutants.py`); a reviewer may prefer another split.
- **The planned block RAM moves to 56.5 RAMB36 at 8x8 with two interfaces**, half a tile over the 56 budget and within the 57.5 ledgered; S1's own head planned 57.5 there. The ledger itself (124 against 121.5, the area plan) is not in this round.
- **Not in this round, as before:** the egress-held rows (tsn-c-stack #26), the drafts' repository reviews, the host suites' 10 ms.

## 8. Run history

- 2026-10-29 17:41 CET start; assignment and round 9's handoff read; 17:5x TAKEN (issuecomment-6502704021).
- 17:5x the merge, 11 conflicting files; the firmware's host gate, the mailbox generator and the harness self-test on the working tree, rc 0 after the accessor fix; 18:0x `c5676878`.
- 18:0x the first four legs on 48-63 refused at the link (the hot list); `fw_coverage.py --write` refused `aecp_face.c` 151/152, twice; S1's head measured 152/152 the same way.
- 18:2x `7efee8fb`, `db77201b`; 18:2x-18:49 the four legs without the drafts on 16-31.
- 18:3x the Python idiom gate refused the merged tree; 18:39 `51fa5f18`.
- 18:49-19:10 the four legs with both drafts; 18:53 the sweep's four shards on 0-15.
- 19:1x-19:29 the eight controls; the images at four points and against the legs; 19:30 `f884c7e9`.
- 19:3x-21:04 the gates at `f884c7e9` (section 6); 20:2x xvlog under the lock after the sweep; the docs runner again with a fresh HDL-reference interpreter.
- 21:0x REVIEW READY posted: issuecomment-6507081649.
