[R703] NEGATIVE - exact head d58c8e22e9bd96237b9a28ea1ddd55b0426380c4

# [R703] R703-1: internal cleared-context review of PR #792 (issue #665, lane S2)

- Head `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4`, tree `e755f4dafb61b4904a8cecdf908aff3500465cc1`, one commit on `dev-soft-core` `e76a755a`.
- Scope reconstructed from:
  - AGENTS.md and CONTRIBUTING.md;
  - the S2 assignment (issuecomment-6409745905), decisions D3/D4/D5 (issuecomment-6409738976), the executor's STOP (issuecomment-6413662864), and the manager's result and ruling (issuecomment-6413711129);
  - `docs/reference/FR_NFR.md` 3.4.1, `docs/design/MAILBOX_SPLIT.md:495-502`, `:645-657`, `:674-692` and `:753-758`, `sw/mailbox/mailbox.yaml` and `hdl/milan/mailbox/KL_mbx_rx.sv`;
  - the diff `e76a755a..d58c8e22`;
  - the published receipts at `90dd5bdf:review-evidence/665s2-r1`.
- The lane's STOP (T_svc missed) is the expected result and is not itself a finding. The harness and its figures are what is judged.

## Verdict

NEGATIVE. The measurement is real and reproduces exactly, to the cycle, but three MAJOR and four MINOR findings are open:

- **F1 (MAJOR).** The backlog rows and the composed maximum are measured under a lighter load than the rows define, and the "admitted backlog" decision input is not a bound.
- **F2 (MAJOR).** The self-test does not protect the headline pass figures against clock-ratio or bound defects.
- **F3 (MAJOR).** A notification fan-out ends at its first recipient, so a late or missing recipient is not seen.
- **F4 (MINOR).** The README misses a worse measured instance of a path.
- **F5 (MINOR).** The reuse/regrade path does not bind logs to the image.
- **F6 (MINOR).** A regrade with missing logs passes.
- **F7 (MINOR).** The frozen SHUTDOWN row is unmeasured and has not been waived.

F6 and F7 are retained from the prior public review after I reproduced or checked them; see the last section. Four RESIDUE items and two SUGGESTIONs are listed separately.

## What reproduces: the figures are measured clock counts

All runs below were made at the exact head, from my own clone, with the pinned Verilator 5.050; the published runs used 5.052. Every CPU netlist was already cached. An `sbt` shim refused generation, so nothing was written into the shared LiteX tree. Receipts are in `receipts/`.

| Run | Printed result (rc) | Against the published receipts |
|---|---|---|
| `--self-test` | 19 checks pass, 12/12 mutants caught, `self-test: 0 failures` (0) | same |
| arm A 1x1 | `15 groups graded, 0 refusals, 10 T_svc misses` (0) | `results.json`: 0 differences over 15 groups; all 9 published logs byte-identical |
| arm A 8x8 | `14 groups graded, 0 refusals, 44 T_svc misses` (0) | `table.md` byte-identical; 6 published logs and 14 scripts identical |
| arm B 1x1 | `6 groups graded, 0 refusals, 3 T_svc misses` (0) | 0 differences; 3 logs identical |
| arm B 8x8 | `6 groups graded, 0 refusals, 4 T_svc misses` (0) | 0 differences; 2 logs identical |
| `--mutation slow-adp-rx` | `CONTROL slow-adp-rx caught`, 24.614 ms (0) | log identical |
| `--cpu-regions as-built` | `CONTROL as-built caught: an instruction access fault (cause 1)` (0) | log identical |
| reviewer plant: 6,650 spins in the ADP receive handler | `CONTROL r703-over caught`, 10.402 ms (0) | new |
| reviewer plant: 6,200 spins | 9.718 ms, within T_svc, so the control correctly prints `ESCAPED` (1) | new; 1.52 us per spin, the slope of slow-adp-rx |
| `selftest.py --write-fixture` from my 1x1 `fixture` run | `fixture.log` and `oracle.json` byte-identical to the committed files | new |

The image ELF digests equal the author's build records for all six builds. The only differing input is `sim.v`, whose LiteX header carries the build date (`receipts/build_identity.txt`).

I recomputed the figures from the raw logs with my own parser (`scripts/recompute.py`, `scripts/access_stats.py`), which does not import `grade.py` or `scenario.py`.

| Figure | 1x1, recomputed | 8x8, recomputed | README / PR |
|---|---|---|---|
| clock ratio inside the log | every consecutive pass pair (1 to 421 per group) has bus delta = 2 x CPU cycles; NOW_MS spacing is exactly 100,000 bus cycles | same | CPU 50 MHz, bus 100 MHz |
| worst pass | 1,552,161 cycles (31.043 ms), acmp-disc | 2,989,496 (59.790 ms), acmp-notk | 31.04 / 59.79 ms |
| composed maximum, arm A | 1,391,312 (27.826 ms), backlog-adp | 2,141,242 (42.825 ms) | 27.83 / 42.82 ms |
| composed maximum, arm B | 685,184 (13.704 ms) | 1,302,022 (26.040 ms) | 13.70 / 26.04 ms |
| event behind 15 others (LINK level to the TMR_CMD cancel) | 14.122 ms | 40.514 ms | 14.12 / 40.51 |
| ACMP command behind the acmp ring (the response's wire departure, an upper bound on its commit) | 60.355 ms | 101.983 ms | 60.35 / 101.98 |
| ENTITY_AVAILABLE behind the adp ring (commit to the TMR_CMD arm) | 43.899 ms | 48.632 ms | 43.90 / 48.63 |
| 7 frames owed ahead (wire departure) | 75.757 ms | 98.926 ms | 75.76 / 98.93 |
| mailbox read / write | 9 / 9 CPU cycles; min = max = 9 over 174,108 / 26,009 accesses | 9 / 9 | 9 / 9 |
| BRAM fetch; flash-window load | 9.099 mean (max 303); 262.8 mean (138-303) | 9.152; 262.5 | 9.10; 263 |
| CPI; fetches per instruction | 9.72; 1.73 | 9.62; 1.70 | same |
| idle pass, CPU cycles | 65,703 to 72,358 | 102,152 to 185,315 | same |
| code fetched, boot / service | 11,160 / 40,532 B | 11,396 / 43,060 B | same |

The harness states no tolerance, and none is needed: every figure repeats to the cycle across the two Verilator versions. A committed-PC trace of whole idle passes is a second observation path (`receipts/idle_profile_A1.txt`). It gives exactly 65,703 CPU cycles per idle pass, the value of the pass-boundary counter.

## Decision inputs checked against receipts

- **Cost ranking.**
  - The 8x8 link-up pass, 2,004,666 cycles, splits by module as `mrp_mad` 473,950, `rt_memset` 361,053, `rt_memcpy` 244,102, `mbx` 119,790, `rt_mulsi3` 111,201 and `rt_udivsi3` 89,954. Each value is reproduced exactly.
  - The 1x1 backlog pass, 685,184 cycles, has `rt_memset` 268,495 as its largest term.
  - The linked `memset` is a byte loop: `sb`, `addi`, `j` at `0x14864`.
  - The image has no M-extension instruction (0 `mul`, `div` or `rem` in `objdump`).
  - `aecp.c:58` and `aecp_commands.c:555` are the cited `memset` calls.
  - The attribution wording is RESIDUE R-2.
- **The 1 ms retry without backoff.** Inside the cited 461-495 loop, `aecp.c:494-495` set `retry_pending` and `retry_at = a->now + 1u` when the port call fails. The fixture's four observation callbacks return `false`. Arm B edits exactly those four, in a scratch copy of the test fixture `sw/firmware/ctrl/test/ctrl_aecp_image.c` (test code). It is labelled, and it is never the formal result.
- **The flash-fetch cost ratio.** A flash-window load averages 262.8 CPU cycles against a 9.10-cycle BRAM fetch, about 29x. The product configures `add_spi_flash(mode="1x", clk_freq=int(12.5e6))`. LiteX's divisor of 8 gives 12.5 MHz SCK at the 100 MHz bus, which matches the harness's 8 bus cycles per bit. See SUGGESTION S2.
- **#791, reproduced.**
  - The as-built netlist `3432f054` differs from the cover netlist `1e5f104c` in 47 diff lines, all of them region decode. The `rom` term is `(addr & 0xfffc8000) == 0`; the `sram` union is decoded correctly.
  - The as-built image traps with cause 1 at `0x6880`, which is `jal b1ec <aecp_image_load>`. `0xb1ec` has bit 15 set. The image reboots every 330,491 CPU cycles.
  - The log is byte-identical to the published control.
- **The shipping core.** Compared with the documented shipping netlist `f5f08b17` (sha256 `c208df0b...`, as `docs/design/MARK_II_AREA_PLAN.md:1375` records):
  - **CPU netlist.** The harness CPU has the same plugin set, the same 1-bit fetch and LSU bus IDs and the same cacheless fetch and LSU logic. It lacks only the DRAM mBus modules (Axi4Bridge, WidthAdapter and their arbiters), which is the stated "no DDR3" limit.
  - **Clocks.** `with_cpu_clk` is set: the CPU runs on the 50 MHz `milan` clock and the bus at 100 MHz (`milan_soc.py:2875`, `:3020`).
  - **Bus.** The main bus is 32-bit Wishbone, the shipping default (`milan_soc.py:2828`); no builder overrides it.
  - **Memory.** The firmware memory is `milan_soc.add_ctrl_memory`.
- **The image.**
  - It is built by `ctrl_srp_image.py --config <shape> --interfaces N --with-aecp --layout split`, and its objects are unmodified.
  - The runtime is rebuilt with `-fno-stack-protector` only (#723); this is disclosed.

## Findings

### F1 MAJOR: Conformance, RTL, Robustness, Tests, Docs. The backlog rows sit behind the instantaneous token-bucket burst, and the "admitted backlog" decision input is not a bound

- **Where.**
  - `tb/verilator/ctrl_service_budget/scenario.py:498-502` (`admitted`) and `:532-579`.
  - `README.md:244-249` and `:270-271`.
  - The STOP comment and the PR body: "The admitted backlog is already min(burst, ring room): 8 ADP, 12 GET_RX_STATE, 16 AECP and 7 MAAP records. A smaller backlog cannot shorten a single 40 ms pass".
- **Authority and evidence.**
  - The rows are defined behind a full ring (`MAILBOX_SPLIT.md:756-757`). The host model's measurement of the adp-ring row put "26 records through the filter" (`:683`).
  - `hdl/milan/mailbox/KL_mbx_rx.sv:603-606` refills one token per `refill_ms`, not back to the burst. The contract rates (`mailbox.yaml:631,650,665,687`) are adp 8 then 1 per 10 ms, acmp and aecp 16 then 1 per 5 ms, and maap 8 then 1 per 20 ms.
  - The harness offers each channel only its burst, at t = 0. Its own head logs show the rings draining more slowly than the buckets refill (`receipts/drain_A1_backlog.txt`, `receipts/drain_A1_backlog-adp.txt`):
    - in `backlog`, AECP releases one record per 6.3-6.9 ms pass, against a refill of one per 5 ms;
    - in arm A's `backlog-adp`, ADP releases 2 records per 14-28 ms pass, about 0.07-0.14 per ms, against a refill of 0.1 per ms.
  - Under sustained offered load at the bucket's rate, those rings therefore grow past the burst toward ring room. The ADP row's input is the 8th record, where the desk and its own host model use a full ring.
  - **The composed load is lighter than claimed.** I added this point after reading the prior public review and reproduced it (`receipts/composed_population.txt`).
    - In both points' `backlog` windows, 43 frames are offered, but the receive commits are adp 8, acmp 12, aecp 16 and maap 0.
    - The seven MAAP ANNOUNCEs (`scenario.py:518`, `:536-537`) do not overlap the entity's range, so the range-overlap filter refuses them. No SRP record is offered at all.
    - `backlog-adp` commits adp 8 and nothing else.
    - `README.md:246-247` ("7 MAAP records", "every other channel's burst arriving too") does not describe the measured load.
- **Impact.**
  - The rows labelled "behind a full adp ring", and the AECP share of the composed load, are measured under less backlog than the rows define. Each is a lower bound presented as the row.
  - The D4 (b) input, which the manager's ruling repeats ("the admitted backlog is already small"), rests on an admission bound the RTL does not have.
  - S2b will be re-measured on this harness, and could pass rows that still miss at the backlog the fabric admits.
- **Required outcome.**
  - Either the ring-row stimulus offers each burst-limited channel its bucket's arrival curve (the burst, then one record per `refill_ms` across the measured service interval, or up to ring room), with the row's input the record behind the largest backlog that curve produces;
  - or a recorded manager or owner ruling makes the instantaneous burst the rows' intended load, and the README, the PR body and the decision input say so.
  - Either way, the statement that the fabric admits only min(burst, ring room) is corrected to the refill semantics.
  - The composed window carries committed records on every channel it claims, MAAP and SRP included, through the shipping filter, and the run asserts those populations.
- **Verification.**
  - Rerun `backlog` and `backlog-adp` at both points.
  - A drain receipt shows the backlog when the probe arrives.
  - A plant (one extra record offered at the refill rate during the lag) moves the row.
  - A per-channel commit count inside the composed window matches the claimed load, and a control that drops one channel's background load fails.

### F2 MAJOR: Tests, Conformance. The self-test does not protect the worst-pass, composed-maximum or pass-bound figures against clock-ratio or bound defects

- **Where.**
  - `tb/verilator/ctrl_service_budget/grade.py:5-7` claims "The clock ratio, the markers and the deadlines live in one place each (Grader.cpu_cycles, Grader.start/end ...)". In fact:
    - the pass figures convert inline at `:437` and `:442` (`/ cpu_hz`);
    - `pass_end`, `taking_pass`, `pass_bound` and `window_passes` each carry their own ratio (`:253`, `:262`, `:276` and `:291`).
  - In `selftest.py:38-39`, `PINNED` holds no bound, worst or composed field, and no check reads `grade()['passes']`.
- **Authority.**
  - The assignment: "The harness's marker, clock-ratio and deadline graders are each mutated and must fail".
  - AGENTS.md section 6, Tests lens: each new test can fail for the defect it claims to detect.
- **Evidence.**
  - `scripts/review_mutants.py` applies twelve exact-text source mutants and runs `run.py --self-test` on each (`receipts/review_mutants.log`). Ten escape.
  - Regrading the head's real 1x1 logs under each mutant (`receipts/mutant_regrade_A1.txt`) shows which published values change:

    | Mutant | Published values changed |
    |---|---|
    | R2: composed ms from the bus clock | composed 27.83 to 13.91 ms, and 13.70 to 6.85 ms |
    | R3: worst-pass ms from the bus clock | worst pass 31.04 to 15.52 ms, in 6 groups |
    | R4: the pass bound treats CPU cycles as bus cycles | 44 bound values halve |
    | R9: the bound starts at the input | 42 bound values change |

  - Also escaping are:
    - R6, the ceiling verdict drops W;
    - R7, the expected-response check skipped;
    - R8, a receive commit given to the newest frame;
    - R10, a T_svc miss never fails a run without `--record-budget-findings`;
    - R11, a refusal does not fail the run;
    - R12, a CPU trap is not refused (only the full as-built control would catch it).
  - R1 (CPU cycles rounded down) and R5 (a timer start 1 ms late) are caught.
- **Impact.**
  - The deliverable's headline figures (the worst pass, the composed maximum and every "(bound)" cell) and the run's exit status sit outside the instrument's regression protection.
  - A halving defect would pass the self-test, and it could make S2b's re-measured rows appear to fit.
- **Required outcome.**
  - Every cycle-to-ms and CPU-to-bus conversion goes through the pinned `Grader` methods.
  - The fixture's worst, composed and bound values are pinned in `oracle.json`; the fixture needs a composed window for this.
  - Named mutants cover each conversion, the bound origin, the ceiling with W, the expectation check, the receive-commit attribution and `run.verdict`'s miss and refusal exits. A named check catches each.
- **Verification.** `scripts/review_mutants.py` reports 0 of 12 escaped at the new head.

### F3 MAJOR: Conformance, Robustness, Tests. A notification fan-out ends at its first recipient, not its last

- **Where.** `tb/verilator/ctrl_service_budget/grade.py:230-233` (`notify` returns `hits[0]`). The README AECP table's `set_name` cell, 8x8 if1, "7.93 (15.20)".
- **Authority.** `FR_NFR.md` 3.4.1: "The last required recipient's commit ends a notification fan-out". `README.md:103` and `grade.combine_ends` likewise say the last required output ends a path.
- **Evidence (`receipts/notify_fanout_A8.txt`).** At 8x8, CTL1 is registered on if0 and on if1 before `aecp.set_name.if1`, so the notification goes to both registrations:
  - the response commits at 7.524 ms;
  - the first notification, on if0, commits at 7.933 ms, which is the graded end;
  - the last, on if1, commits at 8.389 ms.
- **Impact.**
  - The published 8x8 set_name if1 figure is understated by 0.456 ms. Its verdict is unchanged (8.39 < 10 ms).
  - Because the end needs only one unsolicited frame, a late or missing required recipient is graded as on time. A notification path that misses T_svc can therefore pass, and S2b would re-measure on this grader.
  - I first rated this MINOR. I raised it after weighing that consequence, for consistency with F2.
- **Required outcome.**
  - The `notify` end is the commit to the last registered recipient of the causal notification.
  - A missing recipient is refused.
  - Both are proven by synthetic self-test cases (two recipients across interfaces; late, missing and unrelated unsolicited frames) and a mutant that restores `hits[0]`.
- **Verification.** The 8x8 `aecp` regrade gives 8.389 ms, a late-recipient trace misses, a missing-recipient trace is refused, and the self-test catches the mutant.

### F4 MINOR: Conformance, Docs. The ACMP table omits a worse measured instance of a path, and the miss counts are instance counts

- **Where.** `README.md:183`, the 1x1 cell for ENTITY_DEPARTING from its RX_HEAD, "14.42 (22.53) **miss**". The README's and the PR's "10 T_svc misses / 44 T_svc misses".
- **Evidence.**
  - The same path (family `disc`, from `rxc:adp` to `tmr:1`) is measured on arm A at 1x1 by the `fixture` group at 25.172 ms, with a bound of 50.79 ms. That is over its 20 ms ceiling: `fixture.entity_departing.if0` has within_ceiling false.
  - That measurement is counted among the run's 10 misses, but no table shows it.
  - At 8x8, the 44 misses are 36 distinct probes. LINK_UP if0 and if1 are each counted five times, once per group that runs `advertised()`. At 1x1, the 10 include the fixture's duplicate path.
- **Impact.** The deliverable table under-reports that path's worst measured value at 1x1, and its verdict class: over the ceiling, not only a miss. The headline counts are not counts of paths.
- **Required outcome.**
  - Report each path's worst measured instance across groups, or exclude the fixture group from both the tables and the counts and say why.
  - State the counts as distinct paths, or label them as probe instances.
- **Verification.** The table cell matches the worst instance in `results.json`, and the counts match a dedupe of `misses`.

### F5 MINOR: Robustness, Tests. `--reuse-build` / `--regrade` never re-checks the image, the SoC Verilog or the CPU netlist

- **Where.** `tb/verilator/ctrl_service_budget/build.py:7-8`, which claims "Every input of the native model is hashed into build.json, so a reused build is refused when any of them changed". Also `:315-321` and `:352-362`.
- **Evidence (`receipts/stale_probe.log`).**
  - Inputs outside the checkout are keyed by bare file name: `ctrl_app.elf`, `sim.v`, `VexiiRiscvLitex_*.v` and the two RAM models; at two interfaces also the generated `KL_mbx*.sv`.
  - `reused()` resolves those keys against the checkout root, finds nothing, and skips them. With all five digests replaced by zeros it accepted the build. The control, a changed in-checkout digest, was refused.
  - The ROM `.init` files the model reads at run time, and the firmware sources, are not inputs at all.
- **Impact.** A reused or regraded build is not bound to the head's image or SoC. The published evidence "regraded at the head, byte-identical" cannot by itself show that the logs came from the head's image. My fresh rebuild at the head does show it, for this round.
- **Required outcome.** Reuse re-checks every recorded input. That means build-directory-relative keys for build outputs, plus the image (or the firmware source tree) and the `.init` files. A planted stale input is refused by a test.
- **Verification.** The stale probe, rerun, is refused for each of the five planted digests.

### F6 MINOR: Robustness, Tests. A regrade silently drops every selected group whose log is missing, and passes

- **Where.** `tb/verilator/ctrl_service_budget/run.py:168-169`, against the module docstring at `:9-11` ("still requires every probe to be measured, so a missing or malformed observation always fails").
- **Evidence (`receipts/regrade_empty.log`).** `run.py --point 1x1 --build-dir <a1x1> --regrade --out <empty dir> --groups backlog,backlog-adp` prints `0 groups graded, 0 refusals, 0 T_svc misses` and returns rc 0. This finding comes from the prior public review (R704-1-F4); I reproduced it.
- **Impact.** An empty or partial receipt set regrades as clean, and the measurement it claims to cover is never executed or checked.
- **Required outcome.** Every selected group's script, log and probes are required; a missing one is a refusal.
- **Verification.** Delete one selected log, then all of them. Both runs fail, with and without `--record-budget-findings`, and an intact explicit subset passes.

### F7 MINOR: Conformance, Tests. The frozen ADP SHUTDOWN row is unmeasured, and no public disposition waives it

- **Where.** `README.md:163`. The assignment's acceptance includes every row of `MAILBOX_SPLIT.md:495-502`, and SHUTDOWN is `:502`.
- **Evidence.** The executor's STOP comment and the PR body say the row is "not met": the fixture has no shutdown input. The manager ruling (issuecomment-6413711129) does not dispose of it. This finding comes from the prior public review (R704-1-F5); I checked it against the public thread.
- **Impact.** One frozen acceptance path has no measurement and no waiver.
- **Required outcome.** Either measure the path through a labelled, test-only entry with a control, or record an explicit public amendment or disposition of the criterion.
- **Verification.** A measured SHUTDOWN to ENTITY_DEPARTING row, or the linked public disposition.

## RESIDUE (purely wording; exact fix given)

- **R-1: source comments name a lane or a review round** (owner rule 2026-10-15; new instances in this delta).
  - In `build.py:40`, `build.py:48`, `run.py:4`, `scenario.py:3`, `split_soc.py:13` and `sim_main.cpp:4`, replace "#665 S2" with "#665".
  - In `build.py:25`, replace "(the lane's -j16)" with "(-j16)".
  - In `selftest.py:3`, replace "(#665 S2; the method of #397 round 2)" with "(#665; the method of #397)".
- **R-2: `README.md:148` names functions for module totals.**
  - Replace "AECP's two polls: `aecp_poll` 26,497 and `aecp_nvm_poll` 20,254 cycles at 1x1, 73,883 and 20,254 at 8x8" with "AECP's two modules, `aecp` 26,497 and `aecp_nvm` 20,254 cycles at 1x1, 73,883 and 20,254 at 8x8, mostly their polls".
  - In the PR body and the STOP comment, "the two AECP polls" becomes "AECP's two modules (mostly their polls)".
  - My idle-pass PC trace gives the function `aecp_poll` alone 19,436 cycles (`receipts/idle_profile_A1.txt`).
- **R-3: `README.md:150` names the wrong composed maximum.** Replace "The 1x1 composed maximum, 685,184 cycles, is" with "The 1x1 `backlog` group's composed maximum (arm B's maximum), 685,184 cycles, is". Arm A's 1,391,312 is `backlog-adp`'s, and the table above it is already correct.
- **R-4: the authoritative suite index names only one Makefile exception.** In `docs/testing/TESTING.md:518`, replace "The manual `nvm_capture_cpu` measurement is the Makefile exception." with "The manual `nvm_capture_cpu` and [`ctrl_service_budget`](../../tb/verilator/ctrl_service_budget/README.md) measurements are the Makefile exceptions."

## SUGGESTION

- **S1: WIRE fields and timeouts.**
  - `grade.py:57` and `:110` record `WIRE` as (cycle, channel, interface), but `sim_main.cpp:203` prints `WIRE cycle if ch`. Nothing grades on it today; swap the fields before anything does.
  - Consider surfacing each group's `timeouts` in `table.md`. One example is the 1x1 `acmp.disconnect_tx.if0` 20 ms wait, which timed out.
- **S2: flash ratio range.**
  - The ~29x flash ratio is the mean over data loads (262.8 cycles).
  - The burst-continuation minimum is 138 cycles, about 15x, and is closer to straight-line XIP fetch.
  - Quoting the 15x to 29x range would size S14's penalty. The conclusion that no T_svc path may fetch from flash holds at both ends.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3, F4, F7) | FR_NFR.md 3.4.1 markers and ceilings against `scenario.py:79-88` and `grade.py:195-304`; `MAILBOX_SPLIT.md:495-502`, `:645-657`, `:674-692`, `:753-758` against the probes; the assignment's acceptance list; both points and both arms rerun and recomputed | R703-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| RTL | UNCLEAN (F1) | `split_soc.py` against `milan_soc.py:2816-3075` (CPU args, `with_cpu_clk`, the Wishbone default, `add_ctrl_memory`, LiteSPI 1x at 12.5 MHz); netlists `1e5f104c`, `3432f054` and `f5f08b17` diffed; `observe.vlt` (passive public reads; 1-bit bus IDs, so `sim_main.cpp`'s two-entry ID tables are exact); `sim_main.cpp:532-560` clocking; `KL_mbx_rx.sv:597-631` bucket; no shipping RTL, SoC or CI file in the diff | R703-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Robustness | UNCLEAN (F1, F3, F5, F6) | backlog, refill and committed populations from the head logs; the `build.reused` stale probe; the empty-directory regrade; refusal paths (an unknown log line, a trap, an unmeasured probe) and both controls | R703-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Tests | UNCLEAN (F1, F2, F3, F5, F6, F7) | `selftest.py` (19 checks and 12 mutants rerun); 12 reviewer source mutants, regraded on real logs; both controls; two reviewer firmware plants (10.402 ms caught, 9.718 ms correctly within budget); fixture and oracle regenerated byte-identical | R703-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Docs | UNCLEAN (F1, F4); RESIDUE R-1 to R-4 do not affect it | `README.md`, every results table checked against the head runs; the PR body; the STOP comment; the docs gates below; `docs/testing/TESTING.md:514-525` | R703-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |

### Gates at the head (`receipts/gates/`)

All of the following returned rc 0:

- `docs_check`, `check_doc_paths`, `check_doc_style` and its `--selftest`, and `check_archive`.
- `check_em_dash --base e76a755a` (0 findings over 364 added lines), `gen_toc --check`, and `gen_toc --verify-anchors` (545 links). These three ran in the pinned Markdown renderer environment. Under the system interpreter they returned rc 2 because `html5lib` is missing, an environment gap recorded in `summary.txt`.
- `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `check_todo_ownership`, `check_soc_sources`, `check_rtl_source_lists`, and `git diff --check e76a755a HEAD`.
- `cd tests && behave`: 14 features, 406 scenarios and 1,977 steps passed.

The diff is 14 new files, all under `tb/verilator/ctrl_service_budget/`. No docs, RTL, SoC, firmware or CI file is changed.

## Real limits of this review

- Physical calibration was NOT RUN, and nothing here is hardware proof. The harness's own limits stand: zero flash erase and program waits, no wire, ingress or egress time, and no DDR3 or datapath.
- The cover netlist's equivalence to a correctly generated split CPU is argued from the netlist diff (decode lines only). No corrected generator netlist exists to compare against.
- I generated no CPU netlist; sbt was refused by design. So the README's "the shipping split region list produces the same decode" is not independently regenerated. The as-built fault itself is reproduced.
- I did not inspect the exact head's hosted contexts. Hosted and act acceptance are the manager's.
- No manager source bank runs at this head, and none is claimed or inferred.

## Pending manager duties

- Route F1 to F7 and RESIDUE R-1 to R-4 to the executor. F7 alternatively needs a public disposition. F1's alternative, a ruling that the burst is the rows' intended load, is a manager or owner decision.
- At the merge turn, build and validate the current-dev merge candidate (source base `e76a755a`, live dev `76de691e`) with the builder and native banks, and link the receipts.
- Accept the exact head on hosted and act.
- Carry the RESIDUE items to the residue checklist.

## Prior public review findings on this PR

I read the PR's public discussion only after the verdict, findings F1 to F5 and the ledger above were written. It contains:

- two review-start notices;
- the external review's published verdict, `[R704] NEGATIVE` (issuecomment-6414619069, 11:12), posted on the same head after this round began.

There are no submitted reviews and no inline threads. I examined each of its findings at this head:

| Prior finding | Disposition at d58c8e22 |
|---|---|
| R704-1-F1 MAJOR, composed and backlog load reduced (MAAP 0, SRP 0; burst is not maximum occupancy) | **Retained, merged into F1.** I reproduced the populations (`receipts/composed_population.txt`): 43 offered, adp 8 / acmp 12 / aecp 16 / maap 0 committed. My refill and drain evidence is independent. |
| R704-1-F2 MAJOR, notification fan-out ends at the first recipient | **Retained as F3.** I found it independently (`receipts/notify_fanout_A8.txt`: 7.933 against 8.389 ms) and now rate it MAJOR. |
| R704-1-F3 MAJOR, reuse does not bind the ELF, ROM `.init` or generated inputs | **Retained as F5.** I found it independently (`receipts/stale_probe.log`). I rate it MINOR: it cannot alter a fresh run's figures, and this round's figures rest on fresh builds. The severity differs from R704's; either rating keeps the verdict NEGATIVE. |
| R704-1-F4 MAJOR, a regrade with missing logs passes | **Retained as F6, MINOR**, reproduced (`receipts/regrade_empty.log`, rc 0). Severity differs for the same reason as F5: the formal runs grade every group they execute. |
| R704-1-F5 MINOR, SHUTDOWN unmeasured and not waived | **Retained as F7, MINOR**, checked against the public thread. |
| R704-1-R1 RESIDUE, lane and round labels in source comments | **Retained as R-1.** It is the same set of lines; my exact fix is given above. |
| R704 RTL lens CLEAN | **Differs.** I record F1 under RTL as well, because its core is the harness's misreading of `KL_mbx_rx.sv:603-606` admission (AGENTS.md section 6: a finding attributable to several lenses is recorded under each). |

My findings F2 (self-test protection of the pass figures) and F4 (worse fixture instance and instance counts) are not in the prior review. Neither are RESIDUE R-2 to R-4 or S1 and S2.

R703-1 FINISHED
