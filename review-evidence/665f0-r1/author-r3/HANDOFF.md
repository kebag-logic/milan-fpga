# HANDOFF: lane F0 of #665 (mailbox contract, harness, ADP slice), [A542]

Status: round 3 REVIEW READY at `3ebd6ca30106a006c20fd2879dcad9c79bf51dca`
(local, not pushed). Round 2 head `a3ea8ffe` was reviewed NEGATIVE by R497-2
(PR #668 comment 5998184135) and R496-2 (5998244827). Round-3 assignment:
#665 comment 5998250555. Round 1 head `0bfef498` was reviewed NEGATIVE by
R496-1 (5995078461) and R497-1 (5994956684); round-2 assignment 5995086086;
rulings 5994730420 (TX commit order, events first) and 5994972330 (DEPARTING
carries the current index).

- Branch: `665-f0-mailbox`, from dev `fa450d301805881ad713b67521477bf042ddadfd`;
  dev merged with `--no-ff` at `510fae60` (round 2) and `28f9666f` (round 3).
- Round heads: 1 `0bfef4987eede4b022b17c7b2f56d079ff84893b`, 2
  `a3ea8ffe16585270911705ffabd68ca5e17fc9e0`, 3
  `3ebd6ca30106a006c20fd2879dcad9c79bf51dca`. One-line commits, no rebase, no
  amend, no trailers.

| SHA | Round 3 subject |
|---|---|
| 592f09cb | L8: a TICK record taken while centiseconds are carried adds to them; defect `carried-ticks-overwritten` (item 2) |
| 7c2df592 | every owed ENTITY_DEPARTING kept across a restart and sent before the restart's ENTITY_AVAILABLE; A15 to A17, E4, three defects (item 1) |
| f67f055e | A7: back-to-back AXI4-Lite writes paired and read back; two drain-cycle READY defects (item 3) |
| 5f4fe8b3 | the design page and suite index: owed frames, the tick carry, A7; inventories referenced, not counted (item 4) |
| 3ebd6ca3 | merge of dev `28f9666f` (item 5) |

- TAKEN: #665 comment 5992024623. REVIEW READY: round 1 5994496304, round 2
  5997778834 (`review_ready_r2.md`), round 3 5998877567 (`review_ready_r3.md`).

## 0. Round 3: item by item

| Item | Finding | What changed | Evidence |
|---|---|---|---|
| 1 | R497-2 F1 (MAJOR) | `adp.c`/`adp.h`: the single pending slot is replaced by `available_owed` (bool) and `departing_owed` (count) with `departing_index` (the oldest one's index). SHUTDOWN appends its DEPARTING (index current at that SHUTDOWN) and tries to send it only when none is owed; `advertise()` marks the AVAILABLE owed and sends nothing while a DEPARTING is owed (machine stays in DELAY, no timer); `adp_poll` sends one frame per call, the oldest DEPARTING first, the AVAILABLE only when none is owed. A DEPARTING queued behind another carries 0 (its run could send no AVAILABLE). An owed AVAILABLE is dropped only by a link loss or a SHUTDOWN. Count saturates at 2^32 - 1. No API precondition; per-pass bound unchanged (a DEPARTING poll costs 28 of the 31 allowed) | `test_adp.c` A15 (the review's case on the core's ports: DEPARTING 1, then AVAILABLE 0, then WAITING with TMR_ADVERTISE 5 s, nothing owed, the schedule runs on with index 1), A16 (second SHUTDOWN while owed: DEPARTING 1, DEPARTING 0, the running restart untouched, its AVAILABLE 0 at its expiry), A17 (room back, expiry before a poll: DEPARTING still first), E4 (the case through the driver, the model's timer and the loop with a HAL that sleeps: DEPARTING 1 then AVAILABLE 0 after the drain, TMR_ADVERTISE armed 5 s after the AVAILABLE, the loop does not sleep while owed, then sleeps and the expiry wakes it). Defects: `available-replaces-owed-departing` (the review's defect: the AVAILABLE takes the DEPARTING's place) caught by A15 (15 checks fail), `available-passes-owed-departing` by A17, `second-departing-dropped` by A16; `departing-sends-zero` moved to the new code, still caught by A10 |
| 2 | R496-2 N1 | no source change | `test_port_loop.c` L8: 40 centiseconds behind a full ring, one more posted as a second TICK record while part of the 40 is carried: 41 of 41 delivered, none owed. Defect `carried-ticks-overwritten` (`=` for `+=` at `ctrl_loop.c:99`) delivers 33 and fails L8 |
| 3 | R496-2 N2 | no RTL change | `axil_checks.hpp` A7: four back-to-back writes to OWN_EID_LO, OWN_EID_HI, MAAP_BASE_LO, MAAP_COUNT, each channel offering its next beat the cycle after its last was taken; with W beside AW and with W 3 clocks ahead: 4 B each, every register reads back its own write. Defects `axil-wready-while-issuing` (R496-2's probe) and `axil-awready-while-issuing` (the AW twin): 2 B for 4 writes, data misplaced, caught by A7 |
| 4 | R497-2 F2 = R496-2 N3 | `MAILBOX_SPLIT.md` Verification row and `tb/verilator/README.md` mbx row reference `mutants.py` and `ctrl_mutants.py` instead of counting; the mbx and firmware READMEs too (no count of either campaign on any of the four pages; the generator self-test's 8 and 7 arms on the design page are its own and exact) | `grep` of the four pages |
| 5 | merge dev | dev `28f9666f` merged with `--no-ff` (`3ebd6ca3`): one findings page from PR #666, no shared file, no submodule change | every gate re-run at the merge head |

Not changed: R496-2 RESIDUE R1 (`docs/testing/CI_WORKFLOWS.md` wording) is
for the manager's residue checklist and outside the round-3 items; R496-2
suggestions S1 to S5 (S1 CI wiring, S2 an A2 arm, S3 the scan's timing
premise, S4 the 26-byte A1 figure, S5 a 65535 ring-counter wrap) are not
taken this round.

## 0b. Round 2: item by item (history)

| Item | Finding | What changed | Evidence |
|---|---|---|---|
| 1 | R496-1 F1 (BLOCKER) | `docs/reference/MAILBOX_CONTRACT.md` added to `GATE_READ_DOCS` in `scripts/ci_scope.py`, with a classification case; `docs/testing/CI_WORKFLOWS.md` names its reader (`gen_mailbox.py --check --crosscheck`) and says six pages | `ci_scope.py --selftest` PASS (was rc 1); `ci_events.py --check` OK |
| 2 | R497-1 F1, R496-1 F2 | `KL_mbx_axil` rewritten: AW, W, AR each into a one-entry slot by its own handshake; READY = slot empty (no VALID term); B and R registered and held until BREADY/RREADY; write first when both wait, the B slot then lets a waiting read through | `axil_checks.hpp` A1 to A6 (40 checks) and A0: the bench perturbs every AXI input with the clock held on every clock of the AXI run and requires every AXI output unchanged (IHI0022H A3.1.1, A3.2.1); 10 adapter mutants, two of them restoring a combinational READY (`axil-arready-follows-awvalid`, `axil-awready-waits-for-wvalid`), all caught |
| 3 | R497-1 F5, ruling 5994730420 | TX record word 1 = SEQ[15:0] (the driver's commit count over all channels) + RSVD[31:16]; `KL_mbx_tx` scans each channel's oldest record's SEQ from the round-robin origin and sends the first modulo 2^16 (ties round-robin); model and driver follow | suite X2 on both adapters and the model: ACMP, ACMP, AECP behind a stalled ACMP frame leave 1, 1, 2; SRP then AECP, ACMP, ADP leave as committed; 0xFFFF before 0x0000; equal SEQs round-robin. Mutants `tx-round-robin`, `tx-seq-wrap-unsigned`, `tx-ties-fixed-priority`, `model-round-robin`, `seq-not-stamped` (driver, `port` D3) all caught |
| 4 | R497-1 F3 | a poll returns whether its module still owes output; `ctrl_loop_service` counts owed output and carried ticks as work; `ctrl_loop_step` (one turn of `ctrl_loop_run`) sleeps only on 0; `adp_poll` returns owed | `test_adp.c` E0 to E3 with a HAL whose wait really sleeps until the model's interrupt (30 s budget, counted dead if none): TX saturated, the TMR_DELAY expiry owed, nothing else pending, TICK off; 16 turns without a sleep; the ring drains; the next pass sends ENTITY_AVAILABLE with TMR_ADVERTISE armed 5 s after the frame; then the loop sleeps and the advertise expiry wakes it. Mutant `poll-owes-nothing` caught by E1 |
| 5 | R497-1 F4 | bound restated with assumptions A1 backlog, A2 callbacks, A3 transmit room, A4 bus (`ctrl_loop.h`); events first (kept); tick fan-out capped at 16 per pass, rest carried; `ADP_MBX_PASS_MAX` 407, `ADP_MBX_EVT_ACCESSES` 1,221, `ADP_MBX_RX_ACCESSES` 8,954 (`adp_mbx.h`); "microseconds on any bus" removed (a 1 us/access figure is stated as an assumption) | `test_adp.c` F0 to F7: event ring full (15 foreign expiries, ADP's TMR_DELAY expiry 16th), 30 centiseconds coalesced behind, ADP receive ring full (28 minimal DISCOVERs, RX_DROP moved; A1 allows 42); events first in every pass; all 16 by pass 2; ENTITY_AVAILABLE in pass 2 at 175 accesses; ring cleared by pass 14 at 457; worst pass 105 of 407; 30 centiseconds at most 16 per pass; no sleep before the backlog is gone. `test_port_loop.c` L6, L7 (40 coalesced centiseconds, 16 per pass). Mutants `events-halved` (bound-breaking), `rx-before-events`, `tick-slice-unbounded`, `owed-ticks-let-it-sleep` caught |
| 6 | ruling 5994972330 | citation of Figures 6-2, 6-3 and 6.2.5.2.2 in `adp.h`, `adp.c` and the design page | `test_adp.c` A10 to A14 read available_index off the wire: SHUTDOWN in WAITING (2) and DELAY (1), immediate and deferred (2), restart's first AVAILABLE (0), wrap 0xFFFFFFFF then 0, DEPARTING after the wrap (1). Mutant `departing-sends-zero` (R497-1-F2's reading) caught by A10 |
| 7 | R496-1 F3 | `ctrl_arms.LWSRP_REV` = `19f5796b63652eb1151906de73cb827d4980a53f`, fetch recipe in the README; the arm refuses another HEAD or a changed `src/` (`git --no-optional-locks status`, the read-only checkout is never written) | self-test pin arms on a scratch clone: one compiled source edited, refused ("differs from the pinned"); HEAD~1 checked out, refused ("is not the pinned") |
| 7 | R496-1 F4 | `KL_mbx_evt` gets the receive rings' guard (used > ring: no free word); model too; the EVT_TAIL, RX_TAIL and TX_HEAD rows state the range rule | suite H0 to H2 on both adapters and the model; mutants `rx-tail-unguarded`, `tx-head-unguarded`, `evt-tail-unguarded` caught |
| 7 | R496-1 F5 | mutant `own-discover-discarded` | caught by the walk row `RCV_ADP_DISCOVER(own eid) x WAITING` |
| 7 | R496-1 F6 | design page: switch-on regenerates the CPU netlist (the VexiiRiscv wrapper hashes the region list into the netlist name and passes each region to the generator) | `litex/soc/cores/cpu/vexiiriscv/core.py` `generate_netlist_name()` and `--memory-region`; switch-on export below |
| 8 | builder gate 44 | `gen_module_matrix.render_leaf` no longer ends with a blank line; the 14 per-leaf `README-tests.md` regenerated (13 existing ones too, since `--check` compares them byte for byte) | `git diff --check fa450d30 HEAD` rc 0; `gen_module_matrix.py --check` OK |
| 9 | merge dev | dev had moved to `510fae60`: merged with `--no-ff` (`a3ea8ffe`), clean auto-merge (`milan_soc.py` and `measure_test_evidence.py` changed on both sides); `protocol-processor` checked out at the new gitlink `ead80360` | every gate below re-run at the merge head; the reused walk proves the new pin and blob and passes 320 of 320 |

Suggestions taken: S2 and S3 (a note beside `CTRL_MBX_WFI` and on device
memory for a weakly ordered hard core, in `mbx_plat_mmio.c` and the design
page). Not taken: S1 (CI wiring of the two firmware-side gates: a reviewed
CI-contract change, its own issue), S4 (a 65535-wrap run), S5 (later lanes
restate the bound; the bound is now generic in `ctrl_loop.h`).

## 1. The contract and its layouts

`sw/mailbox/mailbox.yaml` is the single source; full tables in
`docs/reference/MAILBOX_CONTRACT.md` (generated); design in
`docs/design/MAILBOX_SPLIT.md`. Contract stays 1.0 (never published). Byte
order stated once: every register, record header word and event word is one
32-bit value with fields at fixed bit positions; frame bytes travel four to a
ring word in little-endian lanes; wire fields keep network order.

- Window 0x8000 bytes: registers below 0x400, event ring at 0x400 (64 words),
  channel rings above (receive/transmit words: adp 256/128, acmp 256/256,
  aecp 512/512, maap 128/128, srp 1024/512).
- Records: RX frame (w0 LEN/IF/KIND=1, w1 ARRIVAL_MS, payload); **TX frame (w0
  LEN/IF/KIND=2, w1 SEQ[15:0] and RSVD[31:16]=0, payload)**, sent in commit
  order across channels; event (4 words; TIMER, LINK, GM, TICK), every source
  coalesced.
- Counter range rule (new): an RX_TAIL or EVT_TAIL more than the ring behind
  its head, or ahead of it, leaves no free word until back in range; a TX_HEAD
  more than the ring ahead of TX_TAIL is refused like a malformed record.

## 2. The generator and its self-test

`sw/mailbox/gen_mailbox.py` emits `KL_mbx_pkg.sv`, `KL_mbx.sv`,
`mbx_contract.h` and `MAILBOX_CONTRACT.md`; `--check` (byte drift),
`--crosscheck` (every constant in all three carriers), `--selftest` (positive
control, 8 output mismatches, 7 contract defects: 16 ok). The reference page
is now gate-read in `ci_scope.py` (item 1).

## 3. The HAL and the lwSRP port layer

- Bus port `mbx_hal.h`: read32, write32, wait. `plat/mbx_plat_mmio.c` (volatile
  32-bit accesses at `CTRL_MBX_BASE`; notes on `CTRL_MBX_WFI` wake sources and
  device memory); `host/mbx_plat_host.c` (the model; a bound wait callback).
- Driver `mbx/mbx.h`: contract check, filter, RX take, TX send (stamps SEQ),
  events, timers, tick enable, link, coherent GM read, IRQ.
- Port layer `port/`: lwSRP's `shlan_malloc/calloc/free` on a static
  size-class pool, `shlan_printf` on a bounded debug sink, as of lwSRP
  `19f5796b` (pinned, item 7).
- Loop `loop/ctrl_loop.h`: per pass, events first (at most 8; TICK fan-out at
  most 16 centiseconds, rest carried; a later TICK record's count adds to the
  carry, L8), then each bound channel (at most 2),
  then polls; a pass with work done or owed is followed at once; only an idle,
  owing-nothing pass sleeps. Bound and assumptions A1 to A4 stated there.
- RV32I freestanding (pinned SDK, `-march=rv32i -mabi=ilp32 -ffreestanding
  -fno-stack-protector`): 9 objects, text 11,508 B, data 0, bss 170 B;
  undefined only `memcpy memset vsnprintf` and libgcc `__lshrdi3 __mulsi3
  __udivsi3 __umodsi3`.

## 4. The host model and harness (stimulus reuse)

- `host/mbx_model.c`: the fabric side at transaction level, graded by the
  RTL's own checks (`suite.hpp` run on the model: 134).
- `tb/verilator/mbx`: `suite.hpp` through `KL_mbx_wb` (134) and `KL_mbx_axil`
  (134 + 45 AXI4-Lite handshake checks, `axil_checks.hpp`: A1 to A7, A7 the
  back-to-back write stream read back, with the per-clock input-to-output
  probe A0); co-simulation of the firmware on the RTL and on the
  model (13: five identical frames at identical NOW_MS 117, 7542, 14570,
  18907, 20000; the RTL fabric now allows 16 clocks for a record to start,
  since the commit-order scan adds N_CH + 2).
- **Processor stimulus reused**: `ctrl_reuse.py` proves the gitlink
  (`ead80360` since the round-2 merge), the checkout and the blob of
  `protocol-processor/tb/adp_engine/sim_main.cpp`, then cuts its entity
  constants, its `model_frame` builder and its `ADV` Table 5.51 transcription;
  `adp_walk.cpp` walks 36 cells (9 "DELAY, draw in flight" cells not
  applicable) plus P1, P2, P3, P5, P7, P11, P12: 320 checks.
- lwSRP arm: mrp_mad.c, mrp_pdu.c, timer.c, mvrp.c of the pinned lwSRP on the
  pool, the SRP channel and the fabric TICK: 13 checks.

Host arms (`test_ctrl_firmware.py --require-rv32 --self-test --lwsrp`): model
134, port 81 (L8 added), adp 107 (A15 to A17 and E4 added), walk 320, entity
45, rv32 1, lwsrp 13 (701 checks).

## 5. The ADP slice: clauses, latency bounds, mutants

Milan v1.2 5.6.2, 5.6.3 (5.6.3.1, 5.6.3.5.1 to 5.6.3.5.11, Tables 5.49 to
5.51) over IEEE 1722.1-2021 6.2 (6.2.2.15 with Figures 6-2 and 6-3 and
6.2.5.2.2 for the index a DEPARTING carries: the current one; the restart's
first AVAILABLE carries 0).

Latency: per path, one pass, nothing else pending (measured = bound):
DISCOVER 31, TMR_DELAY 39, TMR_ADVERTISE 11, GM 11, LINK up 11 (down 9),
SHUTDOWN 29. With backlogs (A1 to A4): event taken by pass 2, ADP record by
pass 21; pass at most 407 accesses; response within 1,221 (event) or 8,954
(ADP record) accesses; measured on full rings: 175, 457, worst pass 105
(unchanged in round 3: a poll still sends one frame at most, an owed
DEPARTING costing 28 of the 31 a poll is allowed).

Owed frames (round 3, R497-2 F1): `available_owed` and a count of owed
DEPARTINGs with the oldest one's index. Every SHUTDOWN's DEPARTING stays owed
with its SHUTDOWN index across restart, timer expiry, link change or another
SHUTDOWN, and leaves oldest first; a restart's AVAILABLE never passes it (owed,
machine in DELAY, no timer, until the last DEPARTING has left); a DEPARTING
queued behind another carries 0; an owed AVAILABLE is dropped only by a link
loss or a SHUTDOWN. Stated in `adp.h` and the design page's ADP section.

Planted defects at the head: firmware 41 of 41 (`ctrl_mutants.py`; round 3
adds `available-replaces-owed-departing`, `available-passes-owed-departing`,
`second-departing-dropped`, `carried-ticks-overwritten`), plus the two lwSRP
pin arms; RTL 46 of 46 (`mutants.py`, after both positive controls; round 3
adds `axil-wready-while-issuing`, `axil-awready-while-issuing`; the default
`make` runs a 4-arm subset). The docs reference the inventories and state no
count.

## 6. Default build unchanged: proof

Re-run at the round-3 merge head `3ebd6ca3` against dev `28f9666f`: gateware
exports (`milan_soc.py <builder argv> --entity-gen-dir
configs/generated/<cfg> --no-compile`, LiteX venv, `PYTHONHASHSEED=0`) with
dev `28f9666f`'s
`milan_soc.py` (written beside it, run from there, deleted after) and the
head's, compared after dropping timestamps, output paths and LiteX's
comment-only hierarchy tree (scratch `normdiff.py`, sha256
`0c66396311514ff7...`):

| Config | Argv | Files | Differ |
|---|---|---:|---:|
| ax7101_1x1_tdm8 (shipping) | shipping | 22 | 0 |
| ax7101_8x8 | shipping | 22 | 0 |
| arty_4x4 | shipping + `--sys-clk-freq 100e6` | 22 | 0 |
| arty_8ch | same proxy | 22 | 0 |
| arty_current | same proxy | 22 | 0 |

At the shipping 83.333 MHz the three Arty configs are refused ("No PLL config
found") by this LiteX checkout at the base exactly as at the head, hence the
proxy. Rounds 2 and 3 change no file under `sw/litex`, `sw/builder`,
`configs`, `avdecc` or `sw/firmware/milan_baremetal` (round 3 changes no file
under `hdl/` either: `git diff --stat a3ea8ffe 5f4fe8b3` lists only
`sw/firmware/ctrl`, `tb/verilator` and `docs/design`); the mailbox RTL is
listed only by the switch-on branch, and the RTL source-list gate shows the
datapath closure (108 files, 4 of 4 consumer lists) without it. The builder
bank leaves `git status` clean.

Switch on (both AX7101 configs, round 3 the same as round 2): 8 files differ
(and `litex.log`): the seven
mailbox sources in the tcl, the `KL_mbx_wb` and `KL_mbx` instances, region
`ctrl_mbx` at `0x90100000`, CSR bank `ctrl_mbx` at `CSR_BASE + 0xf000` (no
existing bank moves), interrupt 3, and the CPU netlist
`VexiiRiscvLitex_f5f08b17...` becoming `VexiiRiscvLitex_9aee3fb3...` (the
wrapper hashes the region list into the name and passes each region to the
generator).

## 7. Measured area

Vivado 2026.1, OOC, xc7a100tfgg484-2, 10 ns, `KL_mbx` behind `KL_mbx_wb`
(`tb_mbx_top HOST_P=0`), synth + place + route under the host Vivado lock, at
the round-2 RTL (`ab6806cb`; the mailbox RTL is unchanged after it):
2,641 LUT, 2,737 FF, 1 RAMB36 + 10 RAMB18, 0 DSP; rx 1,003 / 994, evt 731 /
978, tx 546 / 280, `KL_mbx` own 275 / 484, wb 66 / 1; 5,524 of 5,524 routable
nets routed, WNS +0.240 ns. Round 1 (`0bfef498`): 2,756 LUT (tx 678); the
commit-order scan replaced the round-robin arbiter's modulo logic. Digests:
mbx_ooc.tcl 6b7b4388b872ec6d..., util_route.rpt 7f61a21935909bc9...,
util_route_hier.rpt f316e8dc37a7db9d..., timing_route.rpt 0916d761eb227581...,
route_status.rpt cb5432dcb5580bbf....

## 8. Open questions and risks

- CI wiring of the two firmware-side gates (S1): its own issue.
- The datapath tap, the listener's ADP terms (F3), lwSRP's transmit hook (F4),
  the CPU-cycle figure (A4), MMRP: as in the design page's open items.
- The SEQ count belongs to one run of the firmware: the transmit rings are not
  host-readable, so a restart cannot resume it, and records a previous run
  left committed are not ordered against the new run's (stated in `mbx.c` and
  the design page).
- `act` not run: the round-3 head is not pushed, so no PR head exists for
  `act_ci.py --pr 668` to check against.
- R496-2 RESIDUE R1 (`CI_WORKFLOWS.md`'s reason for the sixth gate-read page)
  is left for the manager's residue checklist.

## 9. Gate table

All at the round-3 merge head `3ebd6ca3` (dev `28f9666f` merged, processor
at `ead80360`), each with its own log and rc file, never two Vivado runs or
two heavy builds at once; every rc 0.

| Gate | Result |
|---|---|
| `scripts/ci_scope.py --selftest` | selftest: PASS |
| `scripts/ci_events.py --check` / `--selftest` | OK (1655 items) / PASS (2215 arms) |
| `gen_mailbox.py --check --crosscheck` / `--selftest` | 0 finding(s) / 0 arm(s) failed |
| `make -C tb/verilator/mbx -j16` (pinned Verilator 5.050, from clean) | 134 (Wishbone) + 179 (AXI4-Lite: 134 + 45) + 13 (co-simulation, the same five frames at NOW_MS 117, 7542, 14570, 18907, 20000), 0 failures; quick mutants 4 of 4 |
| `tb/verilator/mbx/mutants.py --jobs 4` | both controls ok; 46 of 46 caught |
| `suite_tally.py --verdict` on the suite log | rc 0 |
| `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp <lwSRP 19f5796b>` | 7 arms ok (model 134, port 81, adp 107, walk 320, entity 45, rv32 1, lwsrp 13 = 701); 41 of 41 caught; both lwSRP pin refusals ok; PASS |
| `test_builder.py --require-rv32` (LiteX interpreter given) | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the Arty route report is not on this host, as in rounds 1 and 2); 23f and 23g elaborate all five recipes |
| `test_nvm_firmware.py --self-test` | OK across 5 shapes, every planted defect reddened |
| sw/litex `test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_cpu_memory_port_cdc`, `test_gptp_tx_timestamp`, `iob_pack_selftest` (LiteX interpreter) | PASS; 21 arms, 21 mutants |
| `lint_rtl.py --check` / `--self-test` | PASS (90 <= ratchet 90) / PASS |
| `syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil`, and `--mode elaborate` | PASS / PASS |
| `check_soc_sources.py`, `check_rtl_source_lists.py` (+ self-tests) | OK / 25 of 25; OK, 4 of 4 consumers / 50 of 50 |
| `check_baremetal_only.py --check` / `--selftest` | 0 findings over 1051 files / 700 arms |
| `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py --self-test` | OK / OK / PASS |
| `check_wire_accountability.py --self-test` | PASS |
| `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest`) | OK, every ratchet holds; 55 / 75 / 54 / 48 self-test checks |
| `check_hygiene.py --check`, `check_todo_ownership.py` | PASS / OK |
| `measure_test_evidence.py --check`, `measure_naming.py --check`, `check_port_contracts.py`, `measure_fail_fast.py --check` | PASS (the same "can be lowered" notes as dev) |
| `pp_srcs.py --check --selftest` | OK |
| `docs/traceability/gen_module_matrix.py --check` | 77 modules, 0 untested |
| `docs_check.py` | 0 findings |
| `check_em_dash.py --base $(git merge-base origin/dev HEAD)` / `--selftest` (pinned renderer venv) | 0 findings over 1413 added lines / 339 arms |
| `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `check_solution_docs.py`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_feature_status.py --self-test`, `check_archive.py`, `check_doc_paths.py` | OK |
| `gen_toc.py --selftest` / `--verify-anchors` / `--check` (pinned renderer venv) | 1501 arms / 343 anchors / OK |
| `gen_hdl_reference.py --selftest` / build to scratch (pyslang 11.0.0) | 44 of 44 / written |
| `git diff --check origin/dev HEAD` and `fa450d30 HEAD` | rc 0 |
| default-build exports, section 6 | 22 of 22 equal for all five configs |

Not run: `act` (the head is not pushed, so no PR head exists for
`act_ci.py --pr 668`); the hosted contexts (manager-owned after a push);
`xvlog_gate.py` and the switch-on OOC area (round 3 changes no RTL; the area
of section 7 stands at the unchanged mailbox RTL); the full Verilator sweep
(the mailbox suite above is the only suite the change reaches, and the sweep
discovers it); `behave` (no file under `tests/` changed in this lane).
