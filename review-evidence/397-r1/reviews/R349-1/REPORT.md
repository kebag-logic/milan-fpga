[R349] NEGATIVE - exact head 7f997b60d5a74d46beca5c263d27496ccce0ae4f

Round R349-1, external independent review of PR #588 for issue #397 (measurement-only
re-scope, issuecomment-5854787465). Head `7f997b60d5a74d46beca5c263d27496ccce0ae4f`, tree
`e2f28554de998383ec0b6116453120633e322f45`, one commit on source base
`ac18b50968b12efe4d15c0a06301264b35656b31`. All five lenses were applied.

## Summary

The measurement machinery is sound and reproducible: both committed scenarios reproduce
bit-for-bit from a fresh build, the markers bracket what they claim, the 50 MHz / 100 MHz
conversion is right, and `nvm_capture_cpu` and `milan_baremetal.c` are untouched. The verdict
is NEGATIVE because of one MAJOR finding: the heartbeat result isn't a property of any duty.
It is set by how the harness feeds the console. The same unmodified harness binary, given a
legal 133-byte pasted command plan, lets `nvm_backed` lapse in the 1x1 shape. The committed
findings present that shape as having "no measured budget refusal", with a 69.38 ms heartbeat
margin. The 2,000 ms liveness deadline is not mentioned anywhere in the deliverable. There are
four MINOR findings and one SUGGESTION.

## Reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md (review bar, lens names), docs/README.md; issue #397
body and comments 5771939108, 5789766422, 5854692469 (assignment), 5854779562 (STOP report),
5854787465 (re-scope), 5854812698 (TAKEN), 5855382440 (REVIEW READY); PR #588 body; the public
evidence packet `review-evidence/397-r1` at `7a649d0c` (MANIFEST.json, author/HANDOFF.md,
author/OMITTED.txt); docs/design/SAVED_STATE_FASTCONNECT.md section 9.4;
docs/integration/BAREMETAL_FIRMWARE.md runtime section (lines 1878-1893);
sw/firmware/milan_baremetal/milan_baremetal.c (heartbeat, poll loops, idle hook, boot order,
console handlers); scripts/nvm_shape.py WRITER_TIMING_MS; sw/litex/milan_soc.py SPI flash and
CPU clock construction; tb/verilator/nvm_capture_cpu/soc.py; the pinned LiteX BIOS readline and
UART driver and the pinned LiteSPI PHY (revisions as recorded in the receipts: LiteX
`a1e1c365`, LiteSPI `02d5a209`). Then `git diff ac18b509..7f997b60` (12 files, +3,841, no
deletions) and the commit (one-line subject, no body or trailers).

Prior public review findings on PR #588: none existed when this round started (the PR thread
held only the two review-start notices). None to resolve or retain. No other reviewer's report
was read.

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs - heartbeat and liveness result depends on harness input, not on any duty; the 2,000 ms liveness deadline isn't addressed

Artifacts: `tb/verilator/fw_service_budget/run.py:204-213` (gap taken between strobes across
back-to-back commands, tail to the final prompt); `tb/verilator/fw_service_budget/sim_main.cpp:46`,
`:116-122`, `:151` (next command injected on the prompt with zero idle, TX never back-pressured);
`docs/findings/397_SERVICE_BUDGET.md:8-11, 58, 78, 148-151, 195-196`;
`tb/verilator/fw_service_budget/README.md:77-78, 87-93`.

Authority and evidence:
- SAVED_STATE_FASTCONNECT.md section 9.4 sets the heartbeat period to at most 500 ms and
  T-NVM-WRITER-ALIVE to 2,000 ms. Issue #397 acceptance 4 is "no liveness lapse (`nvm_backed`
  stays set across every console command and every commit)". The manager's review brief asks
  whether device-maximum WIP pushes the gap past 2,000 ms. The findings document and README
  never mention the 2,000 ms deadline, `nvm_backed`, or the idle hook.
- Firmware heartbeats come only from `nvm_heartbeat_tick()` (`milan_baremetal.c:757-769`,
  rate-limited to 250 ms). It is called from the idle hook (`:1115-1120`) and the flash, restore
  and device poll loops (`:838-849, 884, 1152-1163, 1166-1180`), and not from any console
  handler (`:1516-1584`). The pinned BIOS runs the idle hook only while no UART byte is pending
  (LiteX `software/bios/readline.c` `read_key`: `while (!uart_read_nonblock()) idle_hook_ptr();`).
  The UART is interrupt driven with a 128-byte RX ring (`libbase/uart.c`; generated `soc.h`
  `UART_INTERRUPT 1`).
- In the committed maximum-gap windows the console was idle for 12 system cycles (1x1) and 2
  system cycles (8x8) in total (`receipts/independent_intervals_committed.txt`). The 8x8
  1,449.78 ms gap is the tail of commit #2, the whole 788.88 ms status and the start of wipe,
  with no idle-hook call in between. The 1x1 430.62 ms gap covers 13 back-to-back commands and
  stops only because the command plan ends (the right-censored tail at `run.py:206`).
- Probe P1 (`receipts/probe_P1_uart_paced_*.txt`, `receipts/probe_uart_paced.*`) paces both
  UART directions at 115,200 baud 8N1 on the same 1x1 build. The idle hook then runs between
  commands, and the maximum gap falls to 332.35 ms. The committed figure isn't a physical value.
- Probe P3 (`receipts/probe_P3_*`, `receipts/probe_queued.raw.log`) uses the **unmodified head
  native binary**, firmware and populated 1x1 media, with a 133-byte plan (`milan_nvm` x12, then
  `milan_status`). This is what a host pasting into the 128-byte RX ring produces. One heartbeat
  strobe is written, at 252.583 ms. `backed=1` holds through the status read at ≤1,936 ms after
  that strobe; `backed=0` appears from ≤2,145 ms on; the final `PP_STAT=5b000604` has bit 6
  clear. **The liveness deadline lapses in the shape that the committed tables report as
  passing.** BAREMETAL_FIRMWARE.md:1878-1881 records only the single long-command case, not
  this chaining of short commands.
- Probe P2 (`receipts/probe_P2_wip_split.txt`) uses a 1 s erase and 5 ms page WIP. The erase
  poll loop strobes every 250.0 ms (647.957, 897.957, 1,147.958, 1,397.959 ms), so a
  device-length erase doesn't itself open a gap; maximum gap 412.38 ms. The harness cannot
  express this case as committed (see F5), and the findings don't state it.

Impact: the table the hart decision will be read from has a "Maximum heartbeat gap" row as if
it were a duty. The row says 1x1 fits with 69.38 ms margin and 8x8 misses by 949.78 ms. Neither
figure is a bound or a physical value: both are set by the command plan's queuing and length.
The deliverable does not report the liveness lapse that its own harness reaches in 1x1 with
legal console input. It also never answers the 2,000 ms question it was asked.

Required outcome: the heartbeat and liveness result must be stated in terms the manager can
use for the decision:
- which intervals a reported gap spans, and that queued console input suppresses the idle hook;
- for each duty, the longest stretch with no heartbeat-tick opportunity, and the resulting
  period bound (the 250 ms rate-limit phase plus that stretch plus any UART transmit blocking),
  compared with 500 ms;
- a comparison with the 2,000 ms T-NVM-WRITER-ALIVE, reporting the `backed` evidence the runs
  already print, and whether queued input lapses liveness in each shipped shape;
- what WIP polling does at device-length waits, with executed evidence.

The 1x1 heartbeat row must not stand as a pass without these qualifications. Whether queued
console input is in scope for the product rule is the manager's call. It has to be recorded,
not left implicit.

Verification: rerun `scripts/make_probe.py` / P1-P3 (commands in "Reproduction" below) at the
fixed head. Confirm that the document states the P3 outcome, or a bound that excludes it, and
that the 2,000 ms comparison is present.

### F2 - MINOR - Tests - self-test doesn't pin markers, clock conversion or deadlines; committed tables aren't executable

Artifacts: `tb/verilator/fw_service_budget/run.py:216-262` (the self-test checks only the
budget-finding list of the 1x1 trace plus synthetic intervals; `:261` prints a literal
"checks: 8"); `docs/findings/397_SERVICE_BUDGET.md:174-181` ("eight oracle controls").

Evidence (`receipts/mutation_probes.txt`, `scripts/mutate.py`): 11 single-line mutants of
`run.py` were tested in an isolated mirror. `--self-test` catches 4 (grader threshold scaled
2x, command budget 1,000 ms, command end marker moved, grader no-op). It passes with the other
7:
- heartbeat marker = ACK strobe (8x8 gap 1,449.78 becomes 1,109.16 ms);
- entity-enable marker = walk bit (boot 310.97 becomes 252.58 ms);
- `ms = cycles / 50_000` (every millisecond doubled);
- CPU cycles not halved;
- heartbeat deadline changed to 2,000 ms (the 8x8 heartbeat finding disappears);
- heartbeat tail dropped;
- boot start at cycle 0.

Every mutant is caught only by the reviewer-side regrade of the committed receipts against the
committed rows (`scripts/regrade_check.py`), and no repository gate performs that regrade. The
committed receipts also carry `raw_log`, `product_base` and `tool_revisions`, which `run.py`
does not emit (compare `receipts/rerun_1x1_receipt.json`). The step that assembles them is not
in the harness. The PASS line's claim of "marker integrity" covers only non-empty, ordered
events.

Impact: a later edit that changes the clock conversion, the markers or a deadline passes every
repository gate, and the committed tables can drift from their raw evidence silently.

Required outcome:
- The portable self-test regrades both committed receipts from their raw logs and requires
  exact rows and findings. That pins the markers, the conversion and the deadlines.
- It counts its controls rather than printing a literal.
- The receipt-assembly step is scripted, or the extra keys are documented.

Verification: `scripts/mutate.py` at the fixed head reports a nonzero self-test rc for all 11
mutants.

### F3 - MINOR - Conformance, Docs - AEM copy/CRC is bounded by the whole boot although a much tighter enclosing marker is recorded

Artifacts: `tb/verilator/fw_service_budget/README.md:70-71` ("AEM copy and CRC, which have no
narrower marker"); `run.py:170-171`; `docs/findings/397_SERVICE_BUDGET.md:35-37, 54, 74`.

Evidence: `milan_baremetal.c:1453-1455` runs `nvm_boot()` (which ends with the restore-walk
PP_CTRL[1] clear at `:1179`), then `load_aem_image()`, then `entity_advertise()` (PP_CTRL[0]).
The harness already records both writes. The interval from walk-end write to enable write is:
- 1x1: 5,837,116 system cycles = 2,918,558 CPU cycles = 58.37116 ms (reported: 310.97023 ms);
- 8x8: 13,742,986 system cycles = 6,871,493 CPU cycles = 137.42986 ms (reported: 1,031.43961 ms).

The re-scope asks for the enclosing marked interval, and the README's "no narrower marker"
statement is incorrect.

Impact: the AEM duty is overstated by 5.3x (1x1) and 7.5x (8x8) in the table used for the
decision.

Required outcome: report the tightest enclosing marked interval for AEM copy/CRC, or keep both
figures and correct the README claim.

Verification: recompute from the committed raw logs, where both writes already appear.

### F4 - MINOR - Conformance, Docs - Milan 5.6.3 ADP valid-time deadline replaced by N/A without a recorded decision

Artifacts: `docs/findings/397_SERVICE_BUDGET.md:53-54, 73-74, 103-105`; `README.md:95`.

Evidence: the issue body lists Milan v1.2 5.6.3 as "the ADP valid time the boot must beat".
Assignment 5854692469 says to record each duty "against the deadline it serves (... the Milan
v1.2 §5.6.3 ADP valid time ...)". The deliverable argues that 5.6.3 sets no power-on deadline
and prints N/A. AGENTS.md section 2 requires such a conflict to be published *and marked as
needing a decision*. The PR's open-risks list and the document do not flag it that way.

Impact: an assignment-named deadline silently drops out of the decision table. This matters
for the rest of #397, where the boot also carries the BIOS and UART time this harness excludes.

Required outcome: either compare boot-to-enable with the valid-time window the issue names
(with its derivation and the excluded BIOS/UART time stated), or record the interpretation as an
open manager decision in the findings and the PR.

Verification: document text at the fixed head.

### F5 - MINOR - Robustness, Tests - `--device-wait-us` can't represent the datasheet corner and accepts values it can't run

Artifacts: `sim_main.cpp:19-20` (one wait for both erase and page program); `sim_main.cpp:176`
(a 30 s simulated-time guard); `run.py:289` (accepts 0 to 3,000,000 us).

Evidence:
- The datasheet corner of section 9.4 (tSE 3 s, tPP 5 ms) cannot be configured.
- Using one value for both operations, the 30 s guard allows at most about 0.95 s (1x1: 30 WIP
  operations over a 1.37 s baseline) or 0.24 s (8x8: 104 operations over 5.03 s). Larger
  accepted values fail only after tens of minutes of simulation.
- The split-wait probe P2 (`receipts/probe_wip_split.sim_main.cpp`, a 3-line change) shows the
  case is cheap to support.

Impact: the device-maximum question is answered only by arithmetic projection
(`397_SERVICE_BUDGET.md:118-140`). Accepted inputs fail late.

Required outcome: provide separate erase and program waits, or reject values the run cannot
complete, and state which is the case.

Verification: a run with the tSE/tPP corner, or an immediate refusal of infeasible values.

### S1 - SUGGESTION - RTL, Docs - direction of the SPI PHY substitution bias is not stated

Artifacts: `sim_main.cpp:66-69`; `docs/findings/397_SERVICE_BUDGET.md:111-112`.

Evidence (`scripts/phy_timing.py`, `receipts/phy_timing.txt`): the pinned LiteSPI SDR PHY at
divisor 8 costs 67 cycles per 8-bit transfer (model: 65) and 259 cycles per 32-bit transfer
(model: 257). It costs 78 cycles for the first transfer after CS is re-asserted (model: 65),
because of its 10-cycle CS delay. SPI-bound intervals are therefore about 3% optimistic. SCK =
12.5 MHz itself agrees with `milan_soc.py:2745-2746` and section 9.4. Stating the direction
would help readers of small margins. Optional.

## Assignment checks

1. **Untouched harness and firmware.** `git diff --stat ac18b509..HEAD --
   tb/verilator/nvm_capture_cpu sw/firmware/milan_baremetal` is empty.
   `check_nvm_capture.py` rc 0, seven controls (`receipts/gate_nvm_capture.txt`,
   `gate_untouched.txt`). Met.
2. **Markers bracket their duties.** Checked by an independent parser
   (`scripts/independent_intervals.py`, which uses no harness code).
   - Boot: reset release at system cycle 64 (sim_main edge count) to the PP_CTRL[0] write in
     `entity_advertise` (`milan_baremetal.c:1399`) = 310.97023 / 1,031.43961 ms.
   - NVM status: first input byte to the returned prompt; `nvm_print_status` has no tick path.
     Measured 208.50329 / 788.87705 ms.
   - Heartbeat: the 0x93C <- 0x1 strobe is written only at `:766`. Gaps 430.62305 /
     1,449.77764 ms. The gaps are reproduced, but see F1 for what they mean.
   - Clock ratio: the CPU is clocked from `milan_clk` (generated sim.v, CPU clock assigned from
     `milan_clk_1`). It is driven at 50 MHz with rising edges aligned to the 100 MHz system
     clock (`sim_main.cpp:166-173`). CPU cycles are ceil(sys/2); ms is sys/100,000.
   - The datapath is built with MILAN_CLK_FREQ_HZ = 50,000,000 in both shapes, so the backend
     millisecond tick is real time. The firmware PHC tracks the counter 1:1: `milan_gettime`
     reads 321.44 ms at system cycle 32.25M (1x1) and 1,041.90 ms at 104.30M (8x8).
   - Met, except the AEM bound (F3).
3. **Deadlines and the WIP split.** The constants at head come from
   `scripts/nvm_shape.py` WRITER_TIMING_MS through `milan_baremetal.c:336-348` (the issue's
   292-302 citation is stale): heartbeat 250, erase 3,500, program 50, restore 3,000,
   debounce 1,000. The commit bracket uses 8,000. The measured-service-minus-WIP split is
   arithmetically correct and honestly labelled. Not met for liveness: the 2,000 ms comparison
   is absent, and queued input lapses it (F1). ADP valid time: F4.
4. **Planted over-budget duty and mutations.** The self-test plants a duty one system cycle
   over budget and catches it, and catches a 500 ms delay of the final UART response. The
   wrong-marker and wrong-clock-ratio mutants survive the self-test and are caught only by the
   reviewer regrade (F2).
5. **Reproducibility.** Fresh builds of both shapes (CPU netlist `c208df0b...`, firmware
   `0bf43cd4...` as documented) reproduce the committed raw logs bit-for-bit: 1x1 SHA-256
   `e1a48895...2e61`, 8x8 `c38caa7b...6115`. Events, rows and findings are identical, including
   8x8 status 788.87705 ms and heartbeat gap 1,449.77764 ms (`receipts/rerun_*_compare.txt`).
   The build-hash differences are limited to timestamps and absolute paths in generated
   headers, sim.v and the native binary. Met.
6. **Gates and log size.** docs_check, doc_paths, doc_style, archive, gen_toc, em_dash (339/339
   controls), feature_status 46/46, `git diff --check`: all rc 0 (`receipts/gates_summary.txt`).
   The committed receipts are 49.6 KB and 63.3 KB, with 10-15 KB raw logs embedded and bound by
   SHA-256; their input hashes match the head files. Met.

## Clean-lens record and ledger

[R349] PASS RTL - `tb/verilator/fw_service_budget/build.py:29-71`, `sim_main.cpp:144-193`,
`flash.hpp:12-119`, generated sim.v (CPU clock and MILAN_CLK_FREQ_HZ bindings), pinned LiteSPI
`generic_sdr.py`/`clkgen.py`/`cscontrol.py` - no product RTL changed. The observation taps are
passive combinational reads of the system-side Wishbone and NVM-backend handshakes. The device
boundary keeps the product LiteSPI controller. Clock alignment, CPU domain, backend millisecond
tick and PHC rate were checked against the build. The flash model enforces WEL, WIP, journal
bounds and page wrap. The PHY timing bias is recorded as S1 only.

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F1, F3, F4) | issue #397 body, 5854692469, 5854787465; SAVED_STATE 9.4; `milan_baremetal.c` 336-348, 757-1184, 1395-1455, 1516-1584; findings doc 1-223; P1-P3 | R349-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| RTL | CLEAN (S1 only) | as in the PASS line above | R349-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Robustness | UNCLEAN (F1, F5) | `run.py` 102-213, 265-332; `sim_main.cpp` 17-193; `flash.hpp`; queued-input and split-WIP probes | R349-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Tests | UNCLEAN (F1, F2, F5) | `run.py` 216-262; `flash_test.cpp`; 11 mutants; regrade of both receipts; fresh reruns of both shapes | R349-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |
| Docs | UNCLEAN (F1, F3, F4) | `docs/findings/397_SERVICE_BUDGET.md`; harness README; findings index and TESTING.md entries; BAREMETAL_FIRMWARE.md 1878-1893 | R349-1 | 7f997b60d5a74d46beca5c263d27496ccce0ae4f |

Coverage is banked against this head only. Any commit touching the harness, the findings
documents or the receipts un-covers the affected lenses.

## Reproduction

The scripts are under `scripts/` and take the repository root and build or scratch paths as
arguments. `WS` names the workspace holding the LiteX environment and the RV32 SDK (the same
prerequisites as the capture harness).

```sh
scripts/env_run.sh <repo> --shape endstation_ax7101_1x1_tdm8 --build-dir <b1x1> --build-only
scripts/env_run.sh <repo> --shape endstation_ax7101_1x1_tdm8 --build-dir <b1x1> --reuse-build --populated
scripts/env_run.sh <repo> --shape endstation_ax7101_8x8 --build-dir <b8x8> --build-only
scripts/env_run.sh <repo> --shape endstation_ax7101_8x8 --build-dir <b8x8> --reuse-build --populated --device-wait-us 1000 --record-budget-findings
python3 scripts/compare_receipt.py <b1x1>/service-1-0.json <repo>/docs/findings/397_SERVICE_BUDGET_1X1.json
python3 scripts/make_probe.py <repo> <b1x1> <p_uart> uart_paced      # P1; run <p_uart>/native/Vsim aem slots commands 0 from <b1x1>/gateware
python3 scripts/make_probe.py <repo> <b1x1> <p_wip> wip_split        # P2; args ... 1000000 5000
<b1x1>/native/Vsim <b1x1>/aem_desc.bin <b1x1>/slots.bin receipts/probe_P3_commands.txt 0   # P3, from <b1x1>/gateware
python3 scripts/lapse_analysis.py <raw.log>
python3 scripts/independent_intervals.py <receipt.json|raw.log>
python3 scripts/mutate.py <repo> <scratch>
<litex-venv>/bin/python scripts/phy_timing.py
scripts/gates.sh <repo> <outdir> <markdown-venv-python>
```

## Real limits

- The simulator path given in the brief (a scoped 5.050 binary) does not exist on this host.
  The installed HDL simulator is version 5.052, the version recorded in the committed receipts'
  `tool_revisions`, and it was used unmodified. The bit-identical raw logs confirm equivalence
  for this measurement.
- P1's pacing is a reviewer model: 8N1 at 115,200 baud in both directions, with no host
  latency. The claim that pasted input reproduces P3 physically rests on the pinned BIOS's
  interrupt-driven 128-byte RX ring. It is not bench-proven.
- No 3 s erase run was made (it costs about 1.2G extra simulated cycles). P2 used 1 s and 5 ms.
- Physical calibration and hardware were not run. Field skips are not hardware proof. No
  Docker/act, hosted-run inspection, source bank, candidate merge or full parent, PP, gPTP,
  Yosys or builder bank was run in this round.
- The product builds wrote gitignored files into the review clone
  (`configs/generated/{ltn_rom,ucode}.hex` and bytecode caches), which is inherited product-flow
  behavior. They were removed. `receipts/restore_verification.txt` shows index tree = HEAD tree
  `e2f28554...`, no modified, untracked or ignored entries, and submodule gitlinks and worktrees
  clean.

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Hosted and act acceptance at the exact head.
- The final candidate on live dev `63fe4fb0164d798d44a6476001dc8b887cdd4609` at the merge turn.
- Disposition of F1, including whether queued console input is in scope for the one-hart
  liveness rule, and whether the firmware idle-hook behavior needs its own issue.
- Re-review after fixes.
- The hart decision and the AX7101 release-gates torture remain open under #397.

R349-1 FINISHED
