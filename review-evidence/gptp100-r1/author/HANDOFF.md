# [A733] HANDOFF: FPGA-gPTP #100, Follow_Up information TLV values, announce receipt timeout, three stricter readings

Status: REVIEW READY at head 3e3f041 (resumed 2026-11-05 17:38 after the 13:10 host reset). Every gate the change touches is rc 0 at this head, in the repository and in the scratch parent (with the companion change below). Nothing is pushed.

- Repository: Mister-M-alt/FPGA-gPTP (origin `https://github.com/Mister-M-alt/FPGA-gPTP.git`), branch `100-followup-tlv-values` (local, not pushed).
- Base: main `3e3a4e7695ce66eed609089f280c2fba45b24d36` (the parent pins `135afd04`; main adds documentation and scripts only).
- Head: `3e3f0418ad081e5906d02d872614fe3a81e148e5` (9 commits on the base: c0bb53b, 13670a0, 8f4953a, 07e48cb, db530d4, 9a1c451, 8f77850, 711ff07, 3e3f041).
- Issue posts: TAKEN #100 issuecomment-6654456288 (posted before the reset; not repeated); REVIEW READY 3e3f041 issuecomment-6667454193.

## Resume record

- The reset left a clean tree with seven commits (c0bb53b..8f77850). The repository sweep at 8f77850 had finished at rc 0. The parent consumer gates and the engine mutation arm were cut off part way.
- On resume, review found the late bound's claim ("no response within 15 ms is ever counted lost") false at the extremes. The round trip was not scaled by the clock tolerance, and B.1.2's timestamp granularity was missing. Commit 711ff07 fixes the derivation (generator, harness constant, a new mutant, docs).
- The full engine arm at 711ff07 (its first complete run; the arm before the reset stopped at job 101 of 160) caught 158 of 160. Two controls missed, and both were harness defects of this branch:
  - "a late response completes its exchange" missed `#100 late responses: none moves the delay`, because a completed late pair computed the same 600 ns delay. Late pairs now carry the residence of a 650 ns delay.
  - The #84 control "mastership never publishes the master bit" missed `#84 master cycles were graded`, because the shipping pass segfaulted in phase 52: `tlv_of()` read the empty frame a timed-out `wait_tx` returns. `tlv_of()` now refuses a short frame (`whole` clear, the checks require it), and phase 54 no longer dereferences a missing commit.
  - Commit 3e3f041 fixes both. The control and both mutants were verified caught (`superseded/engine-arm-fixcheck`) before every gate was re-run at 3e3f041.
- The parent's `sw/builder/test_builder.py` at 711ff07 failed `_assert_pre_d8_model_ids_stay_pinned`. The AVB_INTERFACE clock_accuracy is descriptor content, so arty_current's and arty_4x4's model-shape hashes move. The scratch parent's companion change now also re-pins them, following the parent's own #228 precedent (see "Parent companion change").
- PR #99 merged into main as 5184fb3 while this lane was down. This branch is not rebased (rebase and merge are not allowed); see "Merge with main" below.

## Authority (clauses read)

- IEEE 802.1AS-2011 10.2.8.2.1 i) to l): a ClockMaster's PortSyncSync carries gmTimeBaseIndicator = clockSourceTimeBaseIndicator, lastGmPhaseChange = clockSourcePhaseOffset, lastGmFreqChange = clockSourceFreqOffset; rateRatio = gmRateRatio.
- 10.2.9 and Figure 10-6 (ClockMasterSyncOffset): while not grandmaster, clockSourcePhaseOffset = sourceTime − syncReceiptTime and clockSourceFreqOffset from successive values; when grandmaster and the time base indicator changes, the ClockSource's last changes are taken. 10.2.3.6 to 10.2.3.11 define those globals.
- 11.4.4.3.6 to 11.4.4.3.9: cumulativeScaledRateOffset, gmTimeBaseIndicator, lastGmPhaseChange (ScaledNs, "time of the current grandmaster minus the time of the previous grandmaster, at the time that the current grandmaster became grandmaster"), scaledLastGmFreqChange (× 2^41, truncated to the next smaller signed integer).
- 10.3.9.1: announceReceiptTimeoutTimeInterval = announceReceiptTimeout (10.6.3.2: 3) × the announceInterval of the port at the other end, from logMessageInterval of the received Announce.
- 10.3.11.3 and Figure 10-13: SUPERIOR_MASTER_PORT and REPEATED_MASTER_PORT set announceReceiptTimeoutTime = currentTime + interval. CURRENT → AGED needs `(currentTime >= announceReceiptTimeoutTime || ...) && !updtInfo && !rcvdMsg`; CURRENT → RECEIVE needs `rcvdMsg && !updtInfo`. rcvdMsg is set by PortAnnounceReceive (Figure 10-12), another state machine.
- Annex D (normative): "The order of execution of state blocks in different state machines is undefined except as constrained by their transition conditions"; simultaneous exits of equal precedence are arbitrary.
- 11.2.15.3 and Figure 11-8: RESET increments lostResponses while it is at most allowedLostResponses, else clears asCapable; 11.2.12.4 and 11.5.3: allowedLostResponses shall be 3. So the fifth consecutive loss clears asCapable.
- B.2.3: Pdelay turnaround, measured relative to the TAI frequency, shall be ≤ 10 ms. B.1.1: LocalClock within ±100 ppm of TAI. B.1.2: LocalClock time granularity ≤ 40 ns.
- 8.6.2.3: clockAccuracy a) reflects the LocalClock and ClockSource; else b) 0xFE. IEEE 1588-2008 7.6.2.5, Table 6: 0x22 = "The time is accurate to within 250 ns".
- Milan v1.2 4.2.6.2.3, Table 4.2: announceReceiptTimeout default 3 s, min 2.7 s, max 4.5 s. 4.2.6.2.6: turnaround relaxed by 50 % to a maximum of 15 ms ("shall"); later responses "may or may not be processed", and "should not" clear asCapable if 3 or more consecutive arrive later than 10 ms but before the Pdelay_Req interval. 4.2.6.1.1: neighborPropDelayThresh 800 ns.

## The stricter readings against their clauses (no STOP)

1. **Aging at the instant.** Figure 10-13's AGED exit requires `!rcvdMsg`, but rcvdMsg is set by the PortAnnounceReceive machine. Annex D leaves the order between the two machines undefined, so evaluating the timeout before that machine's RECEIVE block is a permitted order. The Announce is not lost: rcvdMsg stays TRUE through AGED, and the engine dispatches it right after the expiry, so it re-elects (checked: "the grandmaster is elected after it"). Milan Table 4.2's 2.7 to 4.5 s holds: the watch fires 2.999 to 3.000 s after the last Announce. No "shall" is broken.
2. **Late responses.** Milan 4.2.6.2.6's "shall" is the 15 ms maximum turnaround. The bound below never counts a turnaround within 15 ms as lost. A response past it is not processed, which the clause permits ("may or may not be processed"), and Figure 11-8 then counts it as any missing response. The "should not" clear asCapable is a recommendation, and the board deliberately does not take it. No "shall" is broken.
3. **clockAccuracy 0x22.** 8.6.2.3 a) requires the value to reflect the LocalClock and ClockSource. 0x22 is the maintainer's statement for the board's characterised oscillator (2026-11-05, documented on milan-fpga #840's page; not verifiable here, since bench access is not allowed). A build without that characterisation passes `--clock-accuracy 0xFE`, satisfying b). No "shall" is broken on that basis.

## New bounds, in milliseconds

- **Announce receipt timeout:** 3000 ms × 2^n, where n is the received logMessageInterval: n = 0 gives 3000 ms, n = 1 gives 6000 ms, n = −1 gives 1500 ms. For n < −11 the value is 1 ms (0 would disarm); for n ≥ 19 it is 3000 × 2^19 ms = 1,572,864,000 ms (the timer's wrap-safe compare spans 2^31 ms). Negative n rounds down to whole ms. The deadline counts whole engine milliseconds from the Announce's last octet, so the port ages in (T − 1 ms, T]. Measured: 5999.74 ms for n = 1 and 1499.74 ms for n = −1.
- **Aging tie:** an Announce whose last octet arrives in the deadline's millisecond or later is aged first. With n = 0, gaps of 3000 ms always age, 2999 ms never, and gaps in between depend on the millisecond phase (all inside Table 4.2's 2700 to 4500 ms).
- **Late Pdelay response:** `PD_LATE_NS_C` = ⌈(15 ms + 2 × 800 ns) × (1 + (100 + 200) × 10^-6)⌉ + 2 × 40 ns = ⌈15,001,600 × 1.0003⌉ + 80 = 15,006,181 ns = **15.006181 ms**, compared against t4 − t1 on this plane's clock. Terms: 15 ms (Milan 4.2.6.2.6), the round trip at `NPD_HI_C` (Milan 4.2.6.1.1), B.1.1's 100 ppm plus `RATE_PPM_C`'s 200 ppm (the most the trimmed clock can read long), and one B.1.2 granule each for t1 and t4. The bound before 711ff07 was 15.0061 ms, without the rate on the round trip and without the granules.

## Changes (file:line at head 3e3f041, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/top/KL_gptp_engine.sv:39` | State region 6, Follow_Up TLV, read-only (internal microCPU address map; no port, parameter or host register map change) | 11.4.4.3 |
| `hdl/top/KL_gptp_engine.sv:464-555` | Announce receipt watch: `ANN_RTO_MS_C`, `ann_rto_ms()` (3000 ms × 2^n, clamped), mirror of slot 2 (armed, deadline), capture of the Announce's last-octet millisecond and logMessageInterval | 10.3.9.1, 10.6.3.2, Figure 10-13 |
| `hdl/top/KL_gptp_engine.sv:716-736` | Queue head: a slot-2 expiry whose watch is not due is dropped; an Announce received at or after a live deadline waits while the expiry dispatches (`t2_force_w`); a dispatched expiry takes its watch | Figure 10-13, Annex D, Milan 4.2.6.2.3 |
| `hdl/top/KL_gptp_engine.sv:767-775` | Forced expiry dispatch (slot 2, timer entry 512) | Figure 10-13 |
| `hdl/top/KL_gptp_engine.sv:909-915`, `:1292-1295` | An Announce handler's nonzero slot-2 arm gets the time still to run from that Announce's arrival | 10.3.9.1 |
| `hdl/top/KL_gptp_engine.sv:917-983` | TLV values: gmTimeBaseIndicator counts BECOME's PHC word-3 write; lastGmPhaseChange = the 64-bit publish offset as ScaledNs; scaledLastGmFreqChange = (kept trim − word-3 estimate) × `TLV_K_C` / 2^16, floored (zero when slewing or no rate since reset) | 10.2.8.2.1 j)-l), Figure 10-6, 11.4.4.3.7-9 |
| `hdl/top/KL_gptp_engine.sv:1048-1055` | Region 6 read mux | 11.4.4.3 |
| `hdl/ucode/gen_gptp_ucode.py:7-29` | Module docstring for #100 | as above |
| `hdl/ucode/gen_gptp_ucode.py:367-373` | `RG_TLV`, `TLV_WORDS_C` | 11.4.4.3 |
| `hdl/ucode/gen_gptp_ucode.py:545-553`, `:624`, `:628-633`, `:1611-1612`, `:2609-2618` | `CQ_C = 0xF822436A`, `CLOCK_ACCURACY_C`, `RUNTIME["cq"]`, `set_clock_accuracy()`, `--clock-accuracy` (Announce body and own priority vector) | 8.6.2.3, 1588-2008 7.6.2.5 |
| `hdl/ucode/gen_gptp_ucode.py:592-610` | `PD_TURNAROUND_MAX_NS_C`, `LOCAL_CLOCK_PPM_C`, `LOCAL_CLOCK_GRAIN_NS_C`, `PD_LATE_NS_C` derivation | Milan 4.2.6.2.6, 4.2.6.1.1; B.2.3, B.1.1, B.1.2 |
| `hdl/ucode/gen_gptp_ucode.py:882-895` | `e_hdr` emits adjacent zero header fields as one wider zero field (same octets), paying for the two new tests | 11.4.2 |
| `hdl/ucode/gen_gptp_ucode.py:1925`, `:1984-1987` | BTCA's 3000 ms arm is scaled by the engine; BECOME's word-3 write is the mastership mark | 10.3.9.1; 10.2.8.2.1 j) |
| `hdl/ucode/gen_gptp_ucode.py:2096`, `:2157-2178` | `_pdpost_late_response`: t4 − t1 > `PD_LATE_NS_C` ends PDPAIR with `S_PDGOT` clear | Figure 11-8, 11.5.3, Milan 4.2.6.2.6 |
| `hdl/ucode/gen_gptp_ucode.py:2399-2408` | Follow_Up leg sends region 6's three words after cumulativeScaledRateOffset 0 | 11.4.4.3.6-9 |
| `syn/ooc/work/gptp_ucode.hex`, `tb/tsngen/gptp_ucode.hex`, `tb/verilator/engine/gptp_ucode.hex`, `tb/verilator/ucpu/gptp_ucode.hex` | Regenerated through their make rules and `syn/ooc/run.sh`'s generator line | - |
| `tb/verilator/engine/sim_main.cpp:247-265`, `:467`, `:373`, `:7380-7861` | Phases 52 to 56 in their own `#100` section; the fourth pass also grades clockAccuracy | acceptance rows |
| `tb/verilator/engine/sim_main.cpp:319`, `:527-538`, `:717-734`, `:1007-1097`, `:5474-5477` | Peers announce the image's clockQuality; Announces carry logMessageInterval 0; the reset-release cycle and `P100_LATE_NS` (15,006,181 ns, `static_assert`ed); `PD_EDGE` answers at the bound with a 600 ns residence, `PD_LATE` 1 ns past it with a 650 ns one; D2c's lost t1 carries a time inside the late bound so its control still shows | - |
| `tb/verilator/engine/p100_mutants.py` | 24 planted #100 controls (table below) | - |
| `tb/verilator/engine/mutants.py:78`, `:91-93`, `:537`, `:892-896` | Wires the #100 controls in; the fourth pass's image is `--p1 255 --clock-accuracy 0xFE` | - |
| `tb/verilator/engine/Makefile:32-33`, `:46-48` | The fourth pass builds its image with `--clock-accuracy 0xFE` | 8.6.2.3 b) |
| `tb/tsngen/run_tsngen.py:29` | `OUR_CQ = 0xF822436A` | 8.6.2.3 |
| `docs/INTEGRATION.md`, `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md`, `docs/MANAGER.md`, `docs/SOURCE_EVIDENCE.md`, `scripts/check_source_evidence.py:32` | Behaviour, constants rows (`PD_TURNAROUND_MAX_NS_C`, `LOCAL_CLOCK_PPM_C`, `LOCAL_CLOCK_GRAIN_NS_C`, `PD_LATE_NS_C`, `CLOCK_ACCURACY_C`), ROM budget (1,015 of 1,024), re-pointed anchors, "Seven state regions" | - |
| `scripts/check_docs.py`, `scripts/check_docs_selftest.py` | PR #99's split of the docs gate, carried byte for byte so the parent's Python idiom gate passes with this gitlink; byte-identical to merged main 5184fb3 | - |

## New checks, planted mutants, failing words

Every check is named `#100 ...` (the fourth pass prefixes `p1 255 `). `tb/verilator/engine/p100_mutants.py` plants each defect below, and the engine arm requires it to fail every check it names.

| # | Planted mutant (file under hdl/) | Failing words (every named check must fail) |
|---:|---|---|
| 1 | the Follow_Up TLV is sent zero (`ucode/gen_gptp_ucode.py`) | `#100 TLV: the first mastership's Follow_Up carries indicator 1`<br>`#100 TLV settled: gmTimeBaseIndicator increments`<br>`#100 TLV settled: lastGmPhaseChange is the last offset`<br>`#100 TLV settled: scaledLastGmFreqChange is the kept trim less the estimate`<br>`#100 TLV slewing: gmTimeBaseIndicator increments`<br>`#100 TLV slewing: lastGmPhaseChange is the last offset` |
| 2 | gmTimeBaseIndicator does not count mastership (`top/KL_gptp_engine.sv`) | `#100 TLV: the first mastership's Follow_Up carries indicator 1`<br>`#100 TLV settled: gmTimeBaseIndicator increments`<br>`#100 TLV slewing: gmTimeBaseIndicator increments` |
| 3 | lastGmPhaseChange is zero (`top/KL_gptp_engine.sv`) | `#100 TLV settled: lastGmPhaseChange is the last offset`<br>`#100 TLV slewing: lastGmPhaseChange is the last offset` |
| 4 | lastGmPhaseChange is not ScaledNs (`top/KL_gptp_engine.sv`) | `#100 TLV settled: lastGmPhaseChange is the last offset`<br>`#100 TLV slewing: lastGmPhaseChange is the last offset` |
| 5 | lastGmPhaseChange drops the offset's high word (`top/KL_gptp_engine.sv`) | `#100 TLV slewing: lastGmPhaseChange is the last offset` |
| 6 | scaledLastGmFreqChange is zero (`top/KL_gptp_engine.sv`) | `#100 TLV settled: scaledLastGmFreqChange is the kept trim less the estimate` |
| 7 | scaledLastGmFreqChange is the rate estimate (`top/KL_gptp_engine.sv`) | `#100 TLV settled: scaledLastGmFreqChange is the kept trim less the estimate` |
| 8 | a slewing mastership reports its last trim (`top/KL_gptp_engine.sv`) | `#100 TLV slewing: scaledLastGmFreqChange is the kept trim less the estimate` |
| 9 | a rate unknown since reset is taken as zero (`top/KL_gptp_engine.sv`) | `#100 TLV: a mastership after a warm reset, no rate written since, carries no phase or frequency change` |
| 10 | the watch ignores the received interval (`top/KL_gptp_engine.sv`) | `#100 logAnnounceInterval 1: still slave 5998 ms after the Announce`<br>`#100 logAnnounceInterval -1: master within 1502 ms of the Announce` |
| 11 | a negative interval lengthens the watch (`top/KL_gptp_engine.sv`) | `#100 logAnnounceInterval -1: master within 1502 ms of the Announce` |
| 12 | the watch counts from the handler (`top/KL_gptp_engine.sv`) | `#100 3.0 s apart, nine clocks before a tick: the port is aged`<br>`#100 logAnnounceInterval 1: still slave 5998 ms after the Announce` |
| 13 | a late Announce runs before the expiry (`top/KL_gptp_engine.sv`) | `#100 3.0 s apart, a clock after the tick: the port is aged`<br>`#100 3.0 s apart, two clocks after the tick: the port is aged` |
| 14 | an Announce at the instant refreshes the port (`top/KL_gptp_engine.sv`) | `#100 3.0 s apart, a clock after the tick: the port is aged`<br>`#100 3.0 s apart, two clocks after the tick: the port is aged` |
| 15 | lateness is judged at dispatch (`top/KL_gptp_engine.sv`) | `#100 a stalled handler: an Announce received before the deadline refreshes the watch` |
| 16 | a dispatched expiry leaves its watch armed (`top/KL_gptp_engine.sv`) | `#90 no response: runs from a capable plane`<br>`#90 no response: request 1 goes out` |
| 17 | a stale expiry dispatches (`top/KL_gptp_engine.sv`) | `#100 a stalled handler: an Announce received before the deadline refreshes the watch` |
| 18 | a late response completes its exchange (`ucode/gen_gptp_ucode.py`) | `#100 late responses: the fifth clears asCapable`<br>`#100 late responses: none moves the delay` |
| 19 | the late bound is one nanosecond short (`ucode/gen_gptp_ucode.py`) | `#100 responses at the bound: six keep asCapable`<br>`#100 responses at the bound: the delay is published` |
| 20 | the late bound leaves out the clock tolerance (`ucode/gen_gptp_ucode.py`) | `#100 responses at the bound: six keep asCapable` |
| 21 | the late bound leaves out the link (`ucode/gen_gptp_ucode.py`) | `#100 responses at the bound: six keep asCapable` |
| 22 | the late bound leaves out the timestamp granules (`ucode/gen_gptp_ucode.py`) | `#100 responses at the bound: six keep asCapable` |
| 23 | the default clockAccuracy is unknown (`ucode/gen_gptp_ucode.py`) | `#100 the default image announces clockAccuracy 0x22` |
| 24 | --clock-accuracy is ignored (`ucode/gen_gptp_ucode.py`) | `p1 255 #100 a --clock-accuracy 0xFE image announces 0xFE` |

## Gate table (repository, head 3e3f041)

Receipt: `receipts/final/repo-gates-3e3f041/` (one recorded-gates unit, MemoryMax 10G, `MAKEFLAGS=-j4`, `VERILATOR_JOBS=4`, the pinned Verilator 5.050, Vivado 2026.1). Every command rc 0, none piped.

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make contract` | 0 | PHC interface contract: PASS |
| 2 | `make -C tb/verilator/ucpu` | 0 | 768 checks: 768 PASS, 0 FAIL |
| 3 | `make -C tb/verilator/parser` | 0 | 378 checks: 378 PASS; mutation arm 16 checks: 16 PASS |
| 4 | `make -C tb/verilator/engine run` | 0 | 2098 / 2098 / 2098 PASS (shipping, request-seeded, Sync-seeded), 61 PASS (fourth pass, `--p1 255 --clock-accuracy 0xFE`) |
| 5 | engine mutation arm (`make -C tb/verilator/engine mutants`, run as `arm_jobs.py --jobs 8`) | 0 | 160 checks: 160 PASS, 0 FAIL (the unmutated control and 159 mutants, the 24 #100 controls among them); `receipts/final/engine-arm-3e3f041/jobs.md` |
| 6 | `make -C tb/verilator/gaskets` | 0 | 81 checks PASS; mutation arm 5 PASS |
| 7 | `make -C tb/tsngen` | 0 | 288 checks PASS; mutation arm 4 PASS |
| 8 | `make -C bench/arty test` | 0 | PASS: two MII done toggles carried tags |
| 9 | `make lint` | 0 | Verilator `--lint-only -Wall`, engine and bench tops |
| 10 | `make docs` | 0 | docs check PASS (14 current, 18 historical pages), docs selftest PASS (127 arms), source evidence 20 exact, 0 findings, selftest PASS (7 arms), diagrams PASS |
| 11 | `make diagrams-check` | 0 | diagram check PASS, selftest PASS (10 arms) |
| 12 | `make ooc` | 0 | clock-order selftest PASS (30 arms), both syntheses' logs and timing reports PASS; figures below |
| 13 | `git diff --exit-code --stat`, `git status --porcelain` | 0 | the regenerated ROM images match the committed ones; nothing untracked |

Base comparisons: `receipts/base/engine-run-3e3a4e7/` (`make -C tb/verilator/engine run` at the base: 2048 / 2048 / 2048 / 60 PASS) and `receipts/base/ooc-run-3e3a4e7/` (`make ooc` at the base, rc 0).

`native-shards.py` shards `scripts/run_all_suites.sh`, which FPGA-gPTP does not have (the script asserts exactly one such command in its spec). So the processor's sweep ran as recorded-gates units instead: the list above in one unit, and the 160-job engine arm with the parallel driver at `--jobs 8` in another. No CPU range was free (`cpu_ranges.py pick` found none), so every unit was pinned to this lane's own booking, 80-95. MemAvailable stayed above 30 GB at every reading (43 to 55 GB). Each unit had MemoryMax 10G; the one peak read, the 711ff07 arm unit's, was 5.8 GB.

Superseded runs, kept because they found the defects fixed since: `receipts/superseded/` holds the 711ff07 repository sweep (13 rc 0), the 711ff07 arm (158 of 160, the two misses above) and the fix check of those two (control and both mutants caught).

## Scratch-parent consumer gate table

Scratch parent: `$VALIDATION_STORAGE/scratch/gptp100-parent` (a clone of `$LANES/trusted-dev-20261104-604899c0`, milan-fpga dev `604899c0`), committed locally and never pushed:

- `6515731e39` Consumer check: parent adaptation (configs and `avdecc/aem_specs.py` clock_accuracy 0x22)
- `2699f03ba1`, `af7e7e9e9d` the earlier gitlinks 8f77850 and 711ff07
- `93e3b18657` Consumer check: parent adaptation, model shape pins
- `94a9f1860f` Consumer check: gptp-processor at 3e3f0418 (the head)

milan_dp_gptp ran in a second clone of that commit (`gptp100-parent-C`), with its submodules taken from the first. Before every submodule git command, `git -C <dir> rev-parse --show-toplevel` was checked to be that directory.

List A, `receipts/final/parent-A-3e3f041/` (one unit, commands in this order, none piped):

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make -C tb/verilator/gptp_shadow -j8` | 0 | 325 checks: 325 PASS, 0 FAIL |
| 2 | `make -C tb/verilator/milan_dp gptp` | 0 | 210 checks: 210 PASS, 0 FAIL |
| 3 | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 210 checks: 210 PASS, 0 FAIL |
| 4 | `make -C tb/verilator/gptp_plane` | 0 | RESULT: PASS; 29 PASS; phc_step 62 checks, 0 failures; campaign 8 PASS |
| 5 | `make -C tb/verilator/gptp_txts` | 0 | gptp_txts 95 checks, 0 failures (three shapes) |
| 6 | `make -C tb/verilator/gptp_tables` | 0 | gptp_tables 36 checks, 0 failures |
| 7 | `make -C tb/verilator/tsn_fuzz ptp` | 0 | built the gPTP slice; field campaign SKIPPED (packet generator not installed), not a pass |
| 8 | `make -C tb/verilator/milan_dp_gm_steps` | 0 | gmstep 196 checks, 0 failures; 6 PASS |
| 9 | `python3 scripts/check_cpp_idiom.py` | 0 | |
| 10 | `python3 scripts/check_py_idiom.py` | 0 | |
| 11 | `python3 scripts/xvlog_gate.py --check` | 0 | xvlog gate: PASS (0 findings == ratchet) |
| 12 | `python3 scripts/check_rtl_source_lists.py` | 0 | |
| 13 | `python3 scripts/check_port_contracts.py` | 0 | |
| 14 | `python3 scripts/measure_naming.py --check` | 0 | |
| 15 | `python3 scripts/measure_test_evidence.py --check` | 0 | (reads `gptp-processor/tb/verilator`) |
| 16 | `python3 scripts/docs_check.py` | 0 | |
| 17 | `python3 scripts/lint_rtl.py --check` | 0 | PRAGMA GATE PASS; LINT GATE PASS (89 <= ratchet 89) |
| 18 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a LiteX place report that is not on this machine (not gPTP) |
| 19 | `git status --porcelain` | 0 | clean |

List B, `receipts/final/parent-B-3e3f041/` (the scheduled physical gPTP suite):

| # | Gate | rc | Tally |
|---:|---|---:|---|
| 1 | `make -C tb/verilator/milan_dp_gptp` | 0 | ax1x1gptp physical 151 checks, 0 failures (RESULT: PASS, 4,943.75 s simulation); setup abort 6, no-TX accounting 20, no-Pdelay accounting 14, recentre controls 14, each 0 failures |
| 2 | `git status --porcelain` | 0 | clean |

Superseded parent runs (`receipts/superseded/`): milan_dp_gptp at gitlink 711ff07, whose RTL and generator are identical to 3e3f041's, rc 0 (physical 151, setup abort 6, no-TX 20, no-Pdelay 14, recentre 14 checks, 0 failures). List A at 711ff07 ran rc 0 through `check_rtl_source_lists`, then `test_builder` failed on the model-shape pins, which led to the companion re-pin.

## Parent companion change (`milan-fpga-companion.patch`)

The parent must land this when it moves the gitlink (milan-fpga #840 records the readings). Without it, the builder refuses the configs, and `test_builder` fails its pins:

- `configs/endstation_ax7101_8x8.yaml` and `configs/endstation_ax7101_1x1_tdm8.yaml`: `gptp.clock_accuracy: 0x22`. The builder refuses a value that diverges from the engine's: "gptp.clock_accuracy 254 diverges from the fabric engine's 34".
- `avdecc/aem_specs.py`: the built-in spec's gptp `clock_accuracy=0x22`.
- `sw/builder/test_builder.py` `_assert_pre_d8_model_ids_stay_pinned`: arty_current's model-shape hash becomes `0x001BC5B812EC1859`, and arty_4x4's hash-derived id becomes `0x001BC5ECED81D3F3`. AVB_INTERFACE clock fields are descriptor content, so IEEE 1722.1 6.2.2.8 obliges the move. Following the parent's #228 precedent, arty_current's served pin `0x001BC50AC1000006` stays. Whether that pin should move is the parent owner's call.

## Area and timing (processor's own gates)

`make ooc` (Vivado 2026.1 out-of-context synthesis, xc7a100tfgg484-2, clk 10 ns from `ooc_clock.xdc`); receipts `receipts/ooc-3e3a4e7/`, `receipts/ooc-3e3f041/`, `receipts/ooc-figures.md`.

| Top | Run | LUTs (logic + LUTRAM) | FFs | BRAM tiles | DSPs | WNS | TNS | Failing / total endpoints |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `KL_gptp_ucpu` | base 3e3a4e7 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 | 0 / 3,165 |
| `KL_gptp_ucpu` | head 3e3f041 | 1,643 (1,511 + 132) | 733 | 1.5 | 4 | +1.941 ns | 0 | 0 / 3,165 |
| `KL_gptp_engine` | base 3e3a4e7 | 4,926 (4,436 + 490) | 3,459 | 1.5 | 4 | +2.249 ns | 0 | 0 / 12,006 |
| `KL_gptp_engine` | head 3e3f041 | 5,425 (4,935 + 490) | 3,618 | 1.5 | 6 | +2.043 ns | 0 | 0 / 12,372 |

The microCPU is unchanged. The engine adds 499 LUTs, 159 FFs and two DSPs (the TLV frequency multiply, a 25 × 32 signed product), and slack falls by 0.206 ns, still +2.043 ns at 10 ns. The dated table in `docs/HDL_DEVELOPER.md` (main 5dce647a) is left as it stands: it records its own date and commit.

## Merge with main (PR #99)

PR #99 (Follow_Up TLV walk, `hdl/wire/KL_gptp_rx_parser.sv`) merged into main as 5184fb3 after the base was cut. This branch does not touch the parser. Its #100 harness rows sit in their own `#100` section (phases 52 to 56), and `scripts/check_docs.py` and `scripts/check_docs_selftest.py` are byte-identical to main's (`git diff 5184fb3 3e3f041 -- scripts/` shows only `check_source_evidence.py`'s one-line region-count row).

Trial merge in a scratch clone (never pushed), 3e3f041 + 5184fb3: the only conflict is `docs/SOURCE_EVIDENCE.md`. Resolve it by keeping this branch's file with main's two parser anchors, `KL_gptp_rx_parser.sv#L439` (Deferred receive event) and `#L521` (Ignored receive flag bits). On that merge, the repository gates (`receipts/final/trial-merge-3e3f041/`: contract, ucpu, parser 482 + 35, engine 2098 × 3 + 61, gaskets, tsngen, bench, lint, docs, diagrams, clean tree) are all rc 0.

## Notes

- **No STOP.** Each stricter reading stays inside its clause (see "The stricter readings against their clauses"). No top-level port or parameter changes, and no host register map changes: region 6 is an internal microCPU state region, `--clock-accuracy` is a generator option, and `git diff 3e3a4e7 3e3f041 -- hdl/top/KL_gptp_engine.sv` adds only `localparam`s and internal logic.
- **clockAccuracy assumption.** The 0x22 default meets 8.6.2.3 a) only for a build whose oscillator is characterised to 250 ns, which is the maintainer's 2026-11-05 decision. Bench access was not allowed, so this lane did not verify it on hardware. A build without that characterisation passes `--clock-accuracy 0xFE`. The parent builder currently feeds the engine generator only priority1, MAC and clock frequency, and refuses a configured clock_accuracy that differs from the engine's constant. A parent that wants 0xFE images would have to pass the option through.
- **Announce granularity.** The receipt deadline is kept in whole engine milliseconds from the Announce's last octet, so the port ages up to 1 ms early (measured 5999.74 ms of 6000). For the default interval the window is 2999 to 3000 ms, inside Table 4.2's 2.7 to 4.5 s.
- **tsn_fuzz.** `make -C tb/verilator/tsn_fuzz ptp` built the gPTP slice against the new gitlink, but its field campaign SKIPPED. The packet generator it drives is not installed at the revision the parent's CI pins (the only local builds are at other revisions), and fetching it was outside this lane's scope. It is an extra beyond the assigned gates; the parent's hosted CI runs it.
- **Session.** The host reset at 13:10 cut the earlier session. TAKEN had been posted (issuecomment-6654456288) and was not repeated. All scratch work lives under the scratch directory (run clones, three scratch parents, two trial-merge clones), and none of it is pushed.
