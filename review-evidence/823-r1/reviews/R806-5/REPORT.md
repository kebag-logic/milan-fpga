[R806] NEGATIVE - exact head 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14

# R806-5: external cleared-context review of PR #863 (#823 round 5)

- **Head under review:** `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14`, tree `ffccc6f5afbb06998e37343419d4d722dcd03054`. It is four commits on round 4's `30ca4b21`: `b6a60fbd`, `d01c66ad`, `a9c6391f` and `7c97e99f`. PR base `dev-soft-core`, source base `a9d69c77`.
- **Authorities, read in this order:** AGENTS.md and CONTRIBUTING.md; the #823 round 2, 3 and 5 rulings (issuecomment-6730773797, -6730985093, -6754858510); `docs/design/SAVED_STATE_FORMAT_32X32.md` sections 3 and 4; FASTCONNECT section 5; `sw/firmware/ctrl_nvm/README.md`. Then the delta `30ca4b21..7c97e99f` and the author packet `review-evidence/823-r1/author-r5` at `19491031`.
- **Prior findings:** I read the round 4 reviews (R805-4 and R806-4) only after my own pass over the delta.
- **Verdict: NEGATIVE.**
  - Three MAJOR findings are open. F1: a power cut after a compaction's move boots half of a work set. F2: the 500 ms append deadline and the 32x32 bound do not hold at the shipped composition's service cadence. F3: ruling item 6 (area) is not met, and the split memory plan refuses the ledgered point.
  - One MINOR is open. F4: the page's 32x32 worst case is not the model's.
  - Every ruling item 1 to 5 that is about wording or a suggestion is met. N1, N2, RS5, RS6, RS-a, RS-b, SG3/S-a, SG4/S-b and S-c are all resolved.

## Findings

### F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - a power cut after a compaction's move boots half of a captured work set

- **Where:**
  - the capture marks only records behind the front: `sw/firmware/ctrl_nvm/nvm_store.c:972-974`;
  - "a compaction carries them" when no delta can go: `nvm_store.c:948-951`;
  - the base is taken from the live stage: `nvm_store.c:1286-1295`, `1100-1119`;
  - the move: `nvm_store.c:1064-1089`;
  - the authority on a tie: `nvm_store.c:535-545` (A on a tie);
  - the claims: `docs/design/SAVED_STATE_FORMAT_32X32.md:274-276`, `sw/firmware/ctrl_nvm/README.md:316-319` and the store's header comment `nvm_store.c:71-73`.
- **Authority:**
  - Focus item (4) of this round: a cut at every write step leaves a state the boot accepts, completed or abandoned, never half-applied.
  - The store's own contract says "A power cut at any step boots the old values or the new ones, never a mix" (README:318-319, `nvm_store.c:72-73`).
  - The page says "A cut during compaction leaves the old slot authoritative" (`:275`).
- **Evidence:** two disposable probes, `scripts/probe_straddle.patch`, run at 1x1 and 8x8 on both ports (`receipts/probe/probe_straddle_1x1_8x8.log`).
  - **P1, torn log.** Slot B is authoritative and torn (fixture `torn_pad`), so the next write is a compaction into A. A work set of the first and the last record changes together after the base's first page.
    - The capture latches both records. The first is behind the front, the last ahead of it. The capture then goes idle, because no delta can go to a torn log.
    - The base takes the last record's new value and the first record's old one. The move leaves both in flight.
    - The media image after the move, before the next delta, boots A: `auth=0 seq=6`, both slots OK at sequence 6. It holds the last record new and the first old: `class=1`, a mix.
    - The uncut control ends with both new: `class=2, compactions=1 appends=1`.
  - **P2, blank media, no fault.** A first change starts the first base. The same two-record work set lands while that base is written.
    - After the move the image boots `auth=0 seq=1`, with the last record new and the first at its default: `class=1`, a mix.
    - This needs no fault at all, only a burst that lands while the first base is being written.
  - P1 and P2 hold at both shapes and on both ports (8 failing probe assertions).
  - The image is what a cut at that instant leaves: the move programs nothing, and the next delta's first page has not been issued.
- **Why the existing sweep misses it:**
  - T9 (`torn_compaction`, `nvm_rig.cpp:382-416`) always cuts a compaction whose save appends to the old slot. That delta is copied behind the base, so the base's half-taken set is completed before any boot can see it.
  - No sweep cuts a compaction that carries a work set no delta could take: a torn log, a full log, or no authoritative slot.
  - The cause is that the base is the live stage, so it takes in-flight values ahead of the front. Rule 4's "a value only the new base carries stays in flight" (`SAVED_STATE_FORMAT_32X32.md:265`) makes that durable in a slot that wins the tie, or is the only slot, before its work set is whole.
- **Impact:**
  - After a cut in that window the entity restores half of a set of changes it captured together.
  - The torn and full cases are exactly the ones that force a compaction. The first-base case is every first save of a blank board that gets a second burst while its base is written.
  - The page's and README's power-cut claims are false.
- **Required outcome:** no reachable cut boots a work set partly applied. Either:
  - (a) the store guarantees it. For example, a base never carries in-flight values that are not in the old slot, or the new slot never wins until the set is whole. The design is the author's choice.
  - (b) or an owner ruling defines the atomicity unit as the record, not the work set. The README, the page section 4 and the store comment then say so.
  - In either case, the page's `:275` sentence must also match the tie rule. Once the base closes in slot A, a cut boots the new slot, not the old.
- **Verification:**
  - Re-run `probe_straddle.patch`: P1 and P2 report class 0 or 2.
  - Add a sweep that cuts every effect of such a compaction (torn, full and first-base cases), with a plant that the sweep catches.

### F2 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - the 500 ms append deadline and the 32x32 bound assume a 100 us service loop; the shipped split composition services the store once per 10 ms centisecond

- **Where:**
  - the platform: `sw/firmware/ctrl/plat/ctrl_plat.c:261-266` ("The store's service is the loop's first centisecond consumer"; `ctrl_loop_add_tick(&p->app.loop, nvm_store_service)`);
  - the dispatch: `sw/firmware/ctrl/loop/ctrl_loop.c:89-100` (each tick function is called once per owed centisecond);
  - the deadline starts when the capture starts: `nvm_store.c:818-819` and is enforced by `nvm_store.c:1494-1500`;
  - the bound's model: `test_nvm_bound.cpp` with the rig's `kLoopUs = 100u` (`nvm_rig.cpp:32`);
  - the page: `SAVED_STATE_FORMAT_32X32.md:343` ("every service call is a 100 us event loop");
  - the README's own target figure: `README.md:452-454` ("one record a 10 ms tick").
- **Authority:**
  - Ruling item 1: the 32x32 worst case against `T-NVM-COMMIT-TIMEOUT` 500 ms for an append.
  - Round 2 decision 4: each assumption gets a gate or a stated source.
  - The 100 us loop is neither one of A1 to A3 nor sourced, and the tree's own composition contradicts it.
- **Evidence:** a disposable probe, `scripts/probe_cadence.patch`. It sets the rig's loop to 10,000 us, one step per centisecond as `ctrl_plat` dispatches. Run at the 1x1 config with the bound binary (`receipts/probe/probe_cadence_10ms_1x1.log`):
  - One change: read back 222,658 us (model) and 220,111 us (LiteSPI) after it, so it is within 500 ms.
  - Every record of 1x1 at once (54 records): never appended.
    - `failed=4 first=VD_PROGRAM appends=0 compactions=2 exhausted=1 abandoned=1 pending=1 n_inflight=54 stale=1`.
    - The capture alone is one record per 10 ms. A set of more than about 40 records passes the deadline before its first page, every attempt.
  - 32x32 bound shape, A1's burst of 96 names:
    - during the erase: no delta verified in 60 s (`failed=3`);
    - during a compaction: 39,393,356 us;
    - `save_bound` and `commit_deadline` fail.
  - The suspend time the writer reports is quantized by the same tick. `took` is measured from one service step to the next, so on target it reads at least 10 ms whatever the device's latency. The typical-15 us term is not what `suspend_us_max` observes.
- **Impact:**
  - On the shipped split image the 500 ms bound is not met for A1's burst. A large work set is failed by the deadline every attempt and abandoned, so it is reported stale and never appended, even at 1x1.
  - The page and the PR state the bound as met.
- **Required outcome:** the bound and the deadline hold at the service cadence the shipped composition provides, and that cadence is a stated, gated assumption. Either:
  - the composition services the store at the rate the bound needs;
  - or the store's steps, the deadline's start and the bound are graded at the 10 ms tick, and a burst is not abandoned merely by the loop period;
  - or an owner ruling on the deadline's scope.
- **Verification:**
  - `save_bound` and `commit_deadline` run at the shipped cadence, or a gate ties the rig's loop to `ctrl_plat`'s.
  - The cadence probe's every-record burst is appended without exhaustion.

### F3 - MAJOR - Conformance, RTL - ruling item 6 (area under #818) is not met, and the append path breaks the ledgered 8x8 two-interface allocation

- **Where:**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:227-245`, the new append-path table;
  - the author's REVIEW READY: item 6 "not met as ruled", and "Decision needed".
- **Authority:**
  - Ruling item 6: area for the split placement under #818's gate against `dev-soft-core`.
  - The owner's 57.5 RAMB36 ledger for 8x8 with two interfaces, which `ctrl_memory` enforces.
- **Evidence:** I reproduced the plan (`scripts/measure_split_memory.sh`, `receipts/memory/{head,base}/*.log`):
  - At this head, `8x8-if2` prints `REFUSED: allocation over budget: 59.5 RAMB36 (rom 125824 bytes in 126976, sram 114832 bytes in 116736) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces` (rc 2).
  - With `30ca4b21`'s store, the same point plans 57.5 tiles: `rom` 120,544 B, `sram` 113,584 B, rc 0. Both figures match the author's table exactly.
  - The other three points plan within budget at both heads (rc 0).
  - #818's routed gate was not run.
- **Impact:**
  - The merge would land a store whose largest ledgered point no longer fits its owner-set budget.
  - No CI gate plans that linked image, so nothing in CI turns red.
  - The ruled area evidence is absent.
- **Required outcome:**
  - An owner decision on the ledger: raise it, or shrink the store or another tenant.
  - #818's area gate run as ruled, or the ruling amended.
  - The table then states the accepted figure.
- **Verification:** `ctrl_srp_image.py --ledgered-point 8x8-two-interfaces` passes against the ruled ledger, and the #818 receipts are linked.

### F4 - MINOR - Conformance, Docs - the page's 32x32 worst case is not the model's, and the two are not reconciled

- **Where:** `SAVED_STATE_FORMAT_32X32.md:297-299`, `:339` and `:365`, against the host suite's printed figures.
- **What disagrees:**
  - The page says the split's worst save is 304.71 ms plus the suspend, and that the deadline must cover twice the worst append, 309.41 ms.
  - At the same shape and maxima, the store under the rig measures 321,274 us (meeting the erase) and 325,187 us (meeting a compaction). The worst append is 175,187 us, so twice it is 350,374 us.
  - My runs reproduce these figures (`receipts/probe/probe_straddle_1x1_8x8.log`, and the self-test receipt).
  - The roughly 20 ms gap is the per-step cost of the service loop. The page's per-page arithmetic (5.335 ms) omits it; the model takes about 6.1 ms a page.
- **Authority:** ruling item 1, "the 32x32 worst case, from the model".
- **Impact:** the page names an arithmetic figure as the worst case, but the implementation exceeds it under the page's own model. The bound still holds at a 100 us loop. F2 is the target-cadence problem.
- **Required outcome:** the page records the model's measured worst case and the head it was measured at, with the loop assumption. Or its arithmetic includes the per-step cost, so the stated worst case bounds the measurement. The drift gate or the suite then holds the two consistent.
- **Verification:** the page's worst-case figure is at least the `save_bound` print, and a gate fails when it is not.

### RESIDUE (wording only)

- **R1.**
  - Where: `sw/firmware/ctrl_nvm/test/nvm_rig.hpp:18` and `sw/firmware/ctrl_nvm/test/nvm_suite.hpp:9`. Both name `scripts/nvm_klj2.py` as the fixture's source, but the fixture writes from `scripts/nvm_klj3.py` (README:521).
  - The author reported this as found and not changed. It is outside RS-b's six places.
  - Exact fix: "scripts/nvm_klj3.py" in both header comments.
- **R2.**
  - Where: the PR body item 1, and REVIEW READY: "The page's arithmetic gives 304.71 ms plus the suspend. That leaves 95.29 ms for the suspend". 500 - 304.71 is 195.29. The 95.29 ms is the all-fabric row's room (500 - 404.71).
  - The same reading is invited at `SAVED_STATE_FORMAT_32X32.md:339-340`, where "The split's worst save is then 304.72 ms" is followed by "The room is 95.29 ms".
  - Exact fix: "the room, taken from the all-fabric worst case (404.71 ms) and so conservative for the split, is 95.29 ms" on the page, and the same wording in the PR text.
  - The figure itself, the room the ruling names, is unchanged.
- **Comment rule.** Every added non-Markdown line of `30ca4b21..7c97e99f` was scanned for lane labels, round labels, reviewer IDs and comment IDs.
  - The one comment ID found (`#665 issue comment 5999350068`, `nvm_store.c:339`) is pre-existing at `30ca4b21:260`, re-wrapped, and tracked by #746.
  - The "F1" labels in `scripts/nvm_format_32x32_tables.py` are generated page text, not source comments.
  - No new instance.

### SUGGESTION

- **S1 (Tests):** `test_nvm_bound.cpp` could print and assert the per-page time it measured beside the page's 5.335 ms, so that a drift between the model and the arithmetic (F4) is caught by name.

## Ruling items (issuecomment-6754858510) and prior findings, at their cause

| Item | Result | Evidence |
|---|---|---|
| 1. Append-only save path | **Built; not met as a power-cut and bound claim (F1, F2, F4)** | Checked against the code, not the summary. A slot is a base and deltas (`nvm_seg_read`, `nvm_log_read`). A save appends only changed records (`nvm_latch` compares the staged bytes; `nvm_delta_begin`), one delta of at most 28 pages, and never erases. A torn or failed delta forces a compaction (`nvm_fail`, `nvm_cmp_wanted`). The compaction runs page by page and yields (`nvm_cmp_next` goes idle per page). The cut record is carried (`nvm_carry_step`). The move comes after the base verifies and the copy (`nvm_cmp_next`, `nvm_move`). The boot replays to the judged end (`nvm_restage_once`). A planted defect exists for each: `torn_appends`, `torn_without_program`, `seg_cap_ignored`, `compaction_never_yields`, `carry_dropped`, `move_before_base_closes`, `move_before_copy`, `base_seq_above_old`, `replay_skipped`, `deltas_applied_out_of_order`, `replay_past_judged_end`, `erase_authoritative`, `save_waits_for_erase`, `no_resume`, `suspend_untimed` and others (183 defects). STOP condition: the save path reaches flash only through `nvm_flash` (`plat/nvm_flash_litespi.c`, PES 0x75, PER 0x7a). No processor or `KL_nvm_backend` line was touched in `30ca4b21..HEAD`, so there is no STOP. |
| 1. Suspend at 15 us typical; margin against 95.29 ms | Stated (page `:336-341`, `NVM_SUSPEND_ROOM_US 95290u`, drift-gated). The timing on target is tick-quantized (F2). Wording: R2 | `check_nvm_format_32x32.py` rc 0 and `--self-test` PASS (`receipts/drift_gate.log`) |
| 2. N1 | **Resolved** | `SPLIT_CONTROL_MEMORY.md:144` now gives 3,344 against 13,264, and points at section 5 for KLJ3 |
| 3. N2 | **Resolved** | `QSPI_FLASHBOOT.md:58-68` now lists who reads and writes each range, as FASTCONNECT section 5 does. The blank-flash sentence is gone |
| 4. RS5, RS6 | **Resolved** | FASTCONNECT contents entry ("three reserved slots") and status row (`journal_klj3` at `0xE4_0000`, 640 KiB) |
| 4. RS-a | **Resolved** | `nvm_klj2.c:3`, `nvm_klj2.h:4` and `nvm_shape.h:4` read "(#665, the split placement's saved-state store)" |
| 4. RS-b | **Resolved** | `test_nvm_write.cpp:17,73,82,96,113,775` name `nvm_klj3.py`. `nvm_rig.cpp:247` and `test_nvm_boot.cpp:12` are kept, as ruled. Remaining instances: R1 |
| 4. RS-c = SG5 | Carried to #495, as ruled | not this round |
| 5. SG3 = S-a | **Met** | `LINE_CITE_RE` covers a range, a list, unquoted, "`path` line N" and `#LN`, with four plant forms. The drift self-test passes |
| 5. SG4 = S-b | **Met** | The suite prints "at width: MILAN_NVM3_MAPIN_ENTRIES_0 = 255, its table's limit, compiles" |
| 5. S-c | **Met** | "doctored outside the host test: refused at compile time" |
| 6. Area under #818 | **Not met (F3)** | `receipts/memory/` |
| Rules: 1x1/8x8 images, tracked outputs | No processor, HDL or `milan_baremetal.c` change in the delta. The builder diff is comments (`endstation_builder.py`, 6 lines) | `git diff --stat 30ca4b21..HEAD` |

## Lens results

- [R806] UNCLEAN **Conformance**: F1 (power-cut claim), F2 (500 ms bound at the shipped cadence), F3 (ruling item 6) and F4 (the worst case from the model) are open. Checked clean: N1, N2, RS5, RS6, the S-a/S-b/S-c items, the STOP condition, and decisions 3, 4, 5 and 7 as code.
- [R806] UNCLEAN **RTL** (firmware architecture and contracts): F1 (compaction ordering against the tie rule), F2 (the store's integration contract with `ctrl_loop`) and F3 (resource effect) are open. Checked clean: `nvm_flash.h` suspend and resume contract, PES/PER codes, the step bound, the erase run-time accounting (`nvm_erase_wait`), and the owed and suspended handling in `nvm_idle`.
- [R806] UNCLEAN **Robustness**: F1 (cut after the move) and F2 (burst abandoned at the target cadence) are open. Checked clean: torn and stale deltas, read faults in the walk and the replay, ignored and slow suspends, the failed save in a suspended erase, and the full log (journal tests at 1x1 and 8x8 in my runs).
- [R806] UNCLEAN **Tests**: the T9 sweep does not cover a compaction carrying an un-appendable work set (F1), and the bound test's loop is not the shipped composition's (F2). Checked clean: the planted-defect bank, each defect tied to named tests (self-test receipt), and the drift gate's new plants.
- [R806] UNCLEAN **Docs**: F1 (README:318-319, page:275), F2 (page:343) and F4 are open. R1 and R2 are residue. Checked clean: N1, N2, RS5, RS6 and the SPLIT_CONTROL_MEMORY append table, which matches my reproduction byte for byte.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | ruling 6754858510 items 1 to 6; `nvm_store.c`, `nvm_store.h`, `nvm_flash.h`, `plat/nvm_flash_litespi.c`; `SAVED_STATE_FORMAT_32X32.md` sections 3 and 4; `receipts/memory/`; `receipts/probe/` | R806-5 | 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 |
| RTL | UNCLEAN | `nvm_store.c` write path, compaction and move; `ctrl_plat.c:261-266`; `ctrl_loop.c:89-100`; split memory plan | R806-5 | 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 |
| Robustness | UNCLEAN | `test_nvm_journal.cpp` (23 tests); probes P1 to P4 | R806-5 | 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 |
| Tests | UNCLEAN | `nvm_mutants.py` (183), `nvm_rig.cpp` power-cut sweeps, `test_nvm_bound.cpp`, `check_nvm_format_32x32.py` self-test, `check_nvm_klj3.py` self-test | R806-5 | 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 |
| Docs | UNCLEAN | `README.md` (ctrl_nvm), `SAVED_STATE_FORMAT_32X32.md`, `SPLIT_CONTROL_MEMORY.md`, `QSPI_FLASHBOOT.md`, FASTCONNECT, `SAVED_STATE_MATERIALIZATION.md`, the PR body | R806-5 | 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14 |

## What I ran (receipts listed in MANIFEST.sha256)

- `test_ctrl_nvm.py --require-rv32 --self-test --jobs 16`, at the head in this clone with the pinned RV32 SDK (`receipts/rv32-cc-version.txt`): rc 0, wall time 1:19:31 (`receipts/ctrl_nvm_selftest.log`).
  - It prints "OK across 5 shape(s), 728 tests, and all 191 planted defects reddened": 191 `self-test OK` lines, 142 checks per shape with 0 failures, and the power-cut sweeps (`--powercut`, `--powercut-compaction`) inside them.
  - The bound prints are "321274 us during the erase, 325187 us during a compaction" and "append ... 175187 us; twice it 350374 us".
  - This is the suite as built. F1 and F2 are what it does not exercise.
- `check_nvm_format_32x32.py` and `--self-test`: rc 0, 0 findings, PASS. `check_nvm_klj3.py` and `--self-test`: rc 0, all 9 planted defects caught (`receipts/drift_gate.log`, `receipts/klj3_gate.log`).
- `ctrl_boundary.py --require-rv32 --selftest --without verilator`: **incomplete locally**, rc 2 (`receipts/ctrl_boundary.log`).
  - Four of its 14 builders exited 0: `fw_rv32_selftest.py`, `test_ctrl_firmware.py` (1,806 s), `test_ctrl_nvm.py` (710 s) and `fw_coverage.py --build-only` (843 s).
  - The fifth, `sw/litex/test_ctrl_memory.py`, refused because this host's Python has no `migen`. That is the environment, not the PR: CI installs `sw/litex/litex_pins.txt`.
  - It was not re-run, with the host at load 140 to 180.
  - The hosted exact-head `firmware-boundary` job executed and succeeded. The author's receipt is `rtl-fast.firmware-boundary__ci_step_9` (`ctrl_boundary: PASS`).
- The split memory plan at four points, at this head and with `30ca4b21`'s store: `receipts/memory/`.
  - The runtime was built from local picolibc, compiler-rt and LiteX sources by a scratch copy of `ctrl_image_runtime.py` with `-fno-stack-protector` added. The local toolchain defaults to the stack protector, which the unmodified builder's archive could not link.
  - Its equivalence is shown by the base point reproducing the ledger's 57.5 tiles and the author's byte figures exactly.
- Probes F1 and F2 on a separate local clone with the patches applied: `scripts/probe_straddle.patch`, `scripts/probe_cadence.patch`, `scripts/run_probe_straddle.sh`; receipts in `receipts/probe/`.
- The author packet at `19491031` was spot-checked:
  - `SUMMARY.md`, the REVIEW READY text and the self-test log tail ("728 tests, and all 191 planted defects reddened");
  - my figures agree on the bound prints and the memory table.
  - The archive commit is unsigned (`verification.verified=false`), so its integrity rests on its `RAW.tsv` digests and my reproduction, not a signature.
- Hosted, exact head (`receipts/hosted_check_runs.tsv`, a snapshot):
  - 44 succeeded, including `firmware-unit`, `firmware-boundary`, `firmware-control-mutants`, the `docs-gates` and the `elaborate` gates;
  - 1 skipped (Physical gPTP, nightly and manual);
  - the Verilator and Yosys shards were still queued or running.
  - The manager owns hosted and act acceptance.

- **Clone restored.** After every run, the clone's index tree is `ffccc6f5afbb06998e37343419d4d722dcd03054`, equal to `HEAD^{tree}`. `git diff --quiet HEAD` passes. No untracked or ignored files remain in the clone or its submodules; the run-made `__pycache__` directories were removed. Every submodule gitlink matches its checkout (`gptp-processor 135afd04`, `protocol-processor a9e84b66`, `lwSRP 08ee86e8`, `tsn-c-stack 70936b77`, `verilog-axis 48ff7a7e`; `external` is not initialized, as at the start). Probes ran only on a separate local clone under the unpublished scratch directory.
- **Receipts.** Host path prefixes in the receipts are replaced by `<home>`, `<clone>` and `<packet>`. `receipts/RAW.tsv` holds each file's sha256 before that replacement.

## Real limits

- Physical calibration was NOT RUN. The suspend latency (typical 15 us, no maximum), the real part's timing and power-cut behaviour are unproven without the board. Field skips are not hardware proof.
- F2's figures are the host rig with its loop set to the platform's centisecond. That is a model of the cadence, not a target run.
- No #818 Vivado route was run. This round's rules exclude it.
- The local firmware boundary gate stopped at builder 5 of 14 because `migen` is missing locally. Builders 6 to 14 were not run here. For those, the hosted exact-head job is the evidence.
- No full sweep, parent, PP, gPTP, Yosys or builder bank was run. The author's sweep at `b6a60fbd` was not re-run.
- No manager source bank runs at this head, and none is claimed.

## Pending manager duties

- An owner decision on F3's ledger, and on F1's atomicity unit and F2's cadence if the author proposes a ruling rather than a fix.
- The current-dev merge candidate (source base `a9d69c77`, live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`) with builder and native banks at the merge turn.
- Hosted exact-head `verilator-suites` and `yosys-portability` completion.
- Carry R1 and R2 to the residue checklist, and RS-c/SG5 to #495 as ruled.

R806-5 FINISHED
