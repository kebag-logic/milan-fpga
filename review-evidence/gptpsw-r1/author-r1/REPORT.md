# [A814] REPORT: gPTP in the split firmware on the #872 optimisation line, round 1 (#884, #665 F6)

Head `c1e3055c` (9 local commits on `15168e14`). The gate table is at the end.

Branch `opt-gptp-sw-1` from `15168e14` (`dev-soft-core-optimisation`), local commits only, nothing pushed.
The owner's decisions of 2026-11-21 (#872 issuecomment-7062285874) govern: 64x64/2if first, a second hart, gPTP
all in software, the hardware timestamps of both ports and the PHC kept in fabric.

## Summary

- **gPTP runs in firmware.** One IEEE 802.1AS-2020 time-aware end station port an interface
  (`sw/firmware/ctrl/gptp/gptp.c`) does BMCA, Announce, two-step Sync and Follow_Up as slave and as grandmaster,
  Pdelay as initiator and responder, asCapable, path trace and a fixed-point PI servo on the PHC. It sits behind a
  four-call HAL. Its tests are 34 GoogleTests; 25 planted defects are all killed. The RV32IM object is 11,674 B of
  text, with no float, no libm and no 64-bit divide helper.
- **The fabric gPTP plane leaves the build** under `--sw-gptp` (`GPTP_SW_EN_P`). In its place is a timestamp
  unit, `KL_gptp_tsu` (421 LUT / 378 FF), that keeps the plane's stamp points and corrections.
- **Synthesis of the whole design at 8x8/1if, plane against `--sw-gptp`: −4,593 LUT, −2,134 FF, −3 RAMB36,
  +1 RAMB18 (−2.5 BRAM tiles), −6 DSP.** The plane's own cells were −6,256 LUT / −5,060 FF. Most of the
  difference is the new 704-bit publication, held three times (about 2.1k FF). Narrowing it is the next 1.8k FF
  (R2-3, OWNER DECIDES 7).
- **Mailbox contract 2.5** adds only: channel `gptp` (5), event `TIMESTAMP` (9, not coalesced, credit-flowed), and
  a 22-word gPTP publication an interface, committed by `GEN`.
- **The CPU load is small.** At 1x1/1if a 100 MHz split hart spends **0.207 %** on a slave port and **0.183 %**
  on a grandmaster port in steady state. The dearest gPTP pass is 19,529 cycles (0.195 ms). The Pdelay
  turnaround is at most **0.197 ms** against a provisional 10 ms bound. At 1x1/2if (a scratch harness point), port 0
  as a slave plus port 1 up with no peer cost 0.272 %.
- **It locks in closed loop.** Over the mailbox model and the real stamp path in Verilator, as slave the PHC is
  within 100 ns of the grandmaster after 2.7 s and within 5 ns at 9 s. As grandmaster the peer is within 100 ns
  after 3.4 s and steady at 9 ns.
- **The memory cost is about +11.1 KB ROM and +1 KB SRAM a port.** That is +2.5 RAMB36 at 1x1/1if (43.0 → 45.5).
  The 8x8 images with gPTP are over the 56-RAMB36 budget (58.5 at 8x8/1if, 63.5 at 8x8/2if); see OWNER DECIDES 4.
- **Hart, for [A813]:** gPTP's load fits either hart many times over. Its one latency-sensitive path is the
  Pdelay responder, so it should go on the hart whose worst pass is shortest, not the one running SRP's tier-2
  slices. The requirements are listed in [Which hart](#which-hart-for-a813).

## 1. Design

The design page is `docs/design/GPTP_SOFTWARE.md` (new). Its ownership table:

| Piece | Owner on this line | Where |
|---|---|---|
| BMCA, Announce, Sync/Follow_Up, Pdelay, asCapable, servo | Firmware, one port an interface | `sw/firmware/ctrl/gptp/gptp.c` |
| Mailbox adapter: channel, events, tick, publication | Firmware | `sw/firmware/ctrl/gptp/gptp_mbx.c` |
| Ingress and egress stamps | Fabric timestamp unit | `hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv` |
| Launch observer on the MAC's transmit stream | Fabric, unchanged | `KL_gptp_gmii_launch.sv` |
| PHC: counter, rate, step, settime | Fabric, the CSR's PTP block (REQ-PTP-01..04) | `timestamp_counter`, `ptp_csr_sync` |
| Consumers: clock validity, GM counters, AVB_INFO, AS_PATH | Fabric, unchanged, fed by the publication | `milan_datapath.sv` |

Milan v1.2 8.3.4 runs one gPTP an interface. So each AVB interface is a one-port end station with its own PHC.
`struct gptp_port` holds all of one port's state, and a redundant entity runs two instances. Today's fabric has one
MAC, so one timestamp unit and one PHC are elaborated. The second pair comes with the second MAC (round 2).

Every protocol constant is the fabric engine's table, value for value (Milan v1.2 4.2.6): asCapable after 2 good
exchanges, the 5th lost response clears it, 800 ns neighborPropDelayThresh, a cease after 3 multi-answered requests
for 300 s, sync receipt 375 ms, follow-up receipt 125 ms, announce receipt 3 intervals. The servo also keeps the
engine's policy: steps over 20 µs before lock and 100 µs locked, the 200 ppm clamp, and the slew-active level of
gptp-processor #75. The PI gains come from the PHC clock and the Sync interval, with both poles at 0.6 a pair.

### Why a minimal core and not flexPTP as it is (OWNER DECIDES 3)

flexPTP's `gptp` branch was compiled for the split ISA: RV32IM, `-Os`, OS-less, every hook stubbed
(`receipts/flexptp/size-rv32im.md`). The result is **41,848 B text and 9,525 B static state** before soft-float and
libm. The servo, the rate ratio and the BMCA use `double`, `float`, `exp`, `log2` and `llround`, and there is one
global instance (`gPtpCoreState`). The split hart has no FPU, links no libm, and needs two ports. So this round
ports a minimal fixed-point core behind the same HAL shape, at 11,674 B text and about 1 KB of caller-owned state a
port. flexPTP's 802.1AS decisions informed it: the asCapable rules, the delay median, the rate window.

### The timestamp unit

`KL_gptp_tsu` keeps the plane's stamp points and corrections exactly, so the plane's published digital bound
still holds: ±11.2 ns on GMII and ±12.6 ns on MII.

- **Ingress:** the PHC on the edge the first tap beat is accepted, less `INGRESS_LAT_NS_P`.
- **Egress:** the PHC on the edge a launch record lands, less 426 ns (GMII) or 3,770 ns (MII), plus `EGRESS_LAT_NS_P`.

An egress record counts as a measurement only when the frame was whole and the PHC stayed inside the model for
the whole window. That guard and the 200 ppm envelope are `KL_gptp_txret`'s, carried over. The plane's positional
ledger leaves; the firmware pairs records by messageType and sequenceId. The FIFO holds 8 records a port; a dropped
record is counted at `GPTP_DROPW[31:16]` and a rejected one at `GPTP_DROPE[31:16]`.

### Contract 2.5 (`sw/mailbox/mailbox.yaml`, generated outputs)

| Item | Carries | Clause |
|---|---|---|
| Channel `gptp`, id 5 | untagged `01-80-C2-00-00-0E`, `0x88F7`, both ways; burst 16, refill 10 ms (provisional) | IEEE 802.1AS-2020 11.3.4, 11.3.5 |
| Event `TIMESTAMP`, 9 | sequenceId, messageType, direction, OK, 64-bit ns | IEEE 802.1AS-2020 11.3.9 |
| Publication `GPTP_*`, 22 words an interface | GM, parent, peer delay, state, 8 path entries | Milan v1.2 5.4.2.23, 5.4.2.24 |

TIMESTAMP is the one event that is not coalesced, because each record is a measurement. `KL_mbx_cdc` returns a
credit when KL_mbx takes the record, so none is overwritten. The firmware writes every `GPTP_*` word and then
`GPTP_STATE` with `GEN` moved, and the words cross as one snapshot. The datapath decodes `pub_gptp_o` onto the
plane's own `gptp_pub_*` nets, so every consumer keeps its RTL.

### The harness carries the gptp channel: rules A and B (recorded rule)

- **Rule A.** A row's defined load covers the channels the image **opened**, read from its `FILTER_EN` write
  (`sim_main.cpp` prints `OPEN <sys> <mask>`). It does not cover every channel the contract names. A log with no
  `FILTER_EN` write is refused, never read as every channel (`channel_gate.opened`).
- **Rule B.** An opened channel with no load frame is refused (`channel_gate.loaded`). gptp's load frame is a
  Follow_Up with its information TLV, 90 bytes (`grade.LOAD_FRAME_BYTES`), the message a slave port's servo runs on.
- **The new family is `gptp`, 10 ms, PROVISIONAL (OWNER DECIDES 1).** No existing row reads it. It does **not**
  enter THE SHARE (`share.EXCLUDED`). Otherwise the share every row is held to would halve, from 2 ms to 1 ms, and
  that would change approved bounds. The self-test's existing share check failed exactly so before the exclusion.
- **The rows model and the census see no gPTP work in the shipping images.** `gptp/` links only into a
  `--with-gptp` image, and no row's image is one. The census rules the three gPTP split inputs as unread under its
  plane shapes (`census_split.GPTP_SW_ONLY`), where a read is refused. A `GPTP_SW_EN_P` census shape is owed (R2-4).
- **The planted over-budget path** moved from BIND_RX to the first 20 ms probe whose window holds the plant
  (`selftest_opened.planted_probe`). On the split SoC, BIND_RX's window is 1 ms.
- **The fixture trim keeps the tick after each deadline** (`selftest_opened.fixture_kept`). The self-test's mutant
  "a timer path starts one millisecond after its deadline" escaped on the re-recorded trace, because its tick was
  trimmed away. It is now caught by the `tmr_no_resp1` row, and every pinned row is unchanged.
- **The committed fixture is re-recorded** on the split SoC (100/100 MHz), because rule A needs a trace with a
  `FILTER_EN` write. The self-test now grades it at the clocks it was recorded at (`oracle.json` `clocks`). The
  fixture drops the store's `SPAN`/`CALL` trace lines (103,102 B).

## 2. What leaves the fabric (synthesis, 8x8/1if, Vivado 2026.1, the train gate's argv and ELF)

All three builds are synthesis only, with the same recipe, flow flags and firmware ELF. Receipts are in
`receipts/syn/` (`diff-s0-s2.md` is the per-cell table).

| Build | LUT | FF | RAMB36 | RAMB18 | BRAM tiles | DSP |
|---|---:|---:|---:|---:|---:|---:|
| S0, the fabric plane (reproduces the gate) | 44,942 | 51,086 | 78 | 33 | 94.5 | 11 |
| S1, the plane removed, nothing in its place | 39,845 | 43,935 | 75 | 32 | 91.0 | 5 |
| **S2, `--sw-gptp`: the unit, contract 2.5, the decode** (`4493fc95`) | **40,349** | **48,952** | **75** | **34** | **92.0** | **5** |
| **S2 - S0** | **-4,593** | **-2,134** | **-3** | **+1** | **-2.5** | **-6** |

Where S2 differs from S0:

| Cell | LUT | FF | RAMB | DSP |
|---|---:|---:|---|---:|
| the plane, `g_gptp_plane.u_gptp_shadow` + `gptp_ctl_mux` (gone; `KL_gptp_engine` alone 4,016 LUT) | -6,256 | -5,060 | -3 RAMB36, -1 RAMB18 | -6 |
| the timestamp unit, `g_gptp_sw.u_gptp_tsu` | +421 | +378 | | |
| the publication's crossing, `KL_mbx_cdc/u_gptp_pub` (704 bits, GEN-committed) | +785 | +1,384 | | |
| the record's crossing, `KL_mbx_cdc/u_ts` | +5 | +182 | | |
| `KL_mbx`: the GPTP_* registers, the TIMESTAMP source, a sixth channel (`u_rx`, `u_tx`) and its rings | +725 | +882 | +2 RAMB18 | |
| `milan_datapath`'s own logic: the publication's decode | +648 | +70 | | |
| `milan_csr` (-994 LUT, +89 FF) and smaller cells: re-synthesis of unchanged RTL | rest | rest | | |

S1 is the plane cut with its consumers left on constant inputs. Synthesis removed those consumers too, so
S1 overstates the saving. `KL_mbx_cdc/u_edit` and `u_pub` also re-synthesized 2,266 and 676 LUT apart between S0
and S1 with the same RTL; in S2 they are back within 229 LUT of S0. **S2 is the figure to use.**

**What stays:**

- the PHC (`timestamp_counter`, `ptp_csr_sync`);
- the launch observer (`KL_gptp_gmii_launch`, 174 LUT / 230 FF; the unit reads its records);
- `KL_ptp_clock_validity`, the GM counters and AVB_INFO/AS_PATH serving. All of these are fed by the firmware's
  publication.

**The smallest unit at today's precision** keeps the same stamp points, so the same ±11.2/±12.6 ns, and an
8-record FIFO in LUTRAM. It uses 421 LUT / 378 FF with no RAMB and no DSP: the 64-bit corrections are adds of
constants and the guard is compares. Yosys out of context: 2,824 cells, PASS (`receipts/yosys/`).

**Where the next 2k FF are.** The publication is held three times: the GPTP_* registers in `KL_mbx`, then both sides
of its crossing (704 bits, 2,088 FF together). Of its 22 words, 16 are the path trace and 2 the parent identity.
In fabric they feed only `milan_csr`'s gPTP status registers and the AS_PATH head of the stream-info answer
(`milan_datapath.sv` 2513, 2934-2938). The firmware already holds those values in the port. Composing those answers
from the port, and publishing only what fabric logic consumes (GM identity, domain, the state bits and the change
counters, 4 words), would save about 1.8k FF and 0.7k LUT. The CSR status block is a documented interface
(REGISTER_MAP), so narrowing it is OWNER DECIDES 7. It is R2-3, and the saving is measured before it is claimed.

## 3. Verification

| Bench | Proves | Result | Planted defects |
|---|---|---|---|
| `sw/firmware/ctrl/test/test_gptp.cpp` (host, GoogleTest) | each clause on scripted frames; a two-port network over simulated PHCs | 34 checks, 0 failures | 25 of 25 killed (`gptp_mutants.py`) |
| `gptp_arms.py` RV32IM arm | builds for the split hart; no float, libm or muldiv helper | 4 checks | — |
| `tb/verilator/gptp_tsu` | both stamp points, 426 / 3,770 ns, the guard, the seal, the FIFO | 33 checks, 0 failures | 16 of 16 killed (`tsu_mutants.py`) |
| `tb/verilator/gptp_sw` (closed loop) | firmware port + adapter + loop + driver on the mailbox model; fabric half PHC + launch + unit in Verilator; independent peer | 13 checks, 0 failures | none yet (round 2) |
| `tb/verilator/mbx` | contract 2.5 in KL_mbx: gptp tuple, TIMESTAMP credit flow, publication | every suite PASS (Wishbone, AXI4-Lite, 2 interfaces, cosim, record mover) | 13/13 and 25/25 caught |
| `tb/verilator/milan_dp` `split`, `split-cdc` | the split wiring with the unit; every KL_mbx_cdc crossing through a primitive | 145 checks; 13 checks; 0 failures | split-cdc's own plants |
| `test_ctrl_firmware.py --require-rv32` | every firmware arm on the contract-2.5 tree, the gptp arms among them | PASS, 90 arms | anchors of all 1,268 firmware mutants still occur exactly once |
| `ctrl_service_budget --self-test` | the grader, rules A and B, the share, the fixture | 1,015 checks PASS | 295/295 mutants caught |
| `publication_census.py --check --selftest` | every split port classed, every publication field carried or ruled | 6 shapes, 246 checks, 0 failures | 221 plants refused; every rule proven by an arm |

### Accuracy evidence (`receipts/closedloop/run.log`)

| Role | Lock (within 100 ns) | Worst after lock | Steady at 9 s | Link delay |
|---|---:|---:|---:|---:|
| Slave to a modelled GM | 2.7 s, one step | 93 ns | 5 ns | 293 ns (peer models 300) |
| Grandmaster to a modelled slave | 3.4 s | 74.8 ns | 9 ns | 289 ns |

These figures are digital only: the peer's clock is a model with its own rate, and the stamp path is the RTL. They
say nothing about PHY delay asymmetry or real oscillators; that is what the bench qualification owes.

## 4. CPU cost and load (the service-budget harness, the split CPU at 100 MHz)

The images are linked unmodified with `--with-gptp` (`receipts/harness/`). The cycles are summed from the
harness's per-module trace (`gptp`, `gptp_mbx`).

| Point | Roles | Pdelay turnaround (bound) | Dearest gPTP pass | Steady load, work passes |
|---|---|---:|---:|---:|
| 1x1/1if | port 0 slave to a GM peer | 0.193 ms (10 ms) | 19,529 cycles | 0.207 % (207 k cycles/s) |
| 1x1/1if | port 0 grandmaster to a slave peer | 0.197 ms (10 ms) | 17,322 cycles | 0.183 % (183 k cycles/s) |
| 1x1/2if (scratch point) | port 0 slave, port 1 up, no peer | 0.174 ms (10 ms) | 23,688 cycles | 0.272 % |
| 8x8/2if, 32x32/2if, 64x64/2if | per port, modelled | ≤ 2 passes ≤ 4 ms | as 1x1 | ≤ 0.21 % a port, ≤ 0.42 % both |

The two figures behave differently across shapes:

- **The load does not depend on the shape.** A port's work is per message, and the message rates are fixed: Sync
  8/s, Pdelay 1/s, Announce 1/s. So it does not grow with streams.
- **The turnaround does depend on the shape**, because the responder waits for the pass in flight. With every pass
  held to THE SHARE (2 ms), a Pdelay_Req waits at most one pass and is answered in the next: ≤ 4 ms against 10 ms.

The 1x1/2if point is a one-line scratch `POINTS` entry in a scratch clone, not committed. Committing it would also
mean changes to the harness's shape model, the firmware's shape table and the flip check, which are out of scope.

The 8x8 points could not be **measured** with gPTP this round. Their images are refused over the memory budget
(OWNER DECIDES 4), and the 32x32/64x64 points have no harness point yet. The ledger was not touched.

The measured image's PHC hooks write RAM words, not the CSR's PTP block (the fixture has no datapath CSR window).
The split's driver adds a few CSR stores for each Sync, which is 8 a second.

The figures above count gPTP work passes only. Counting every pass after link-up gives 1.14 % / 1.12 % of the CPU,
an upper bound: most of it is the adapter's idle polling, about 129 cycles a pass. Round 2 gates the adapter on its
event bits (R2-5).

### Memory (the image plan, planned RAMB36)

| Image | ROM bytes | SRAM bytes | RAMB36 |
|---|---:|---:|---:|
| 1x1/1if | 104,960 text | — | 43.0 |
| 1x1/1if + gPTP | 116,008 text (+11,048) | +1 KB (same 14 RAMB36) | 45.5 |
| 8x8/1if + gPTP | 141,232 | 98,032 | 58.5, refused (56) |
| 8x8/2if | 131,600 | 114,336 | 60.5, refused (56) |
| 8x8/2if + gPTP | 142,960 (+11,360) | 116,464 (+2,128) | 63.5, refused (56) |

### Which hart (for [A813])

- **Load:** ≤ 0.42 % of one 100 MHz hart for two ports. The dearest pass is 0.24 ms.
- **Latency:** the Pdelay responder (10 ms) is the only path that is not trivially met. Sync to Follow_Up has
  125 ms. The servo is insensitive to a few ms of service delay at a 125 ms Sync interval.
- **Recommendation:** put both gPTP ports on the hart that does **not** run SRP's tier-2 slices (THE TIERS, 1.3 ms
  slices). With A813's split, that is the hart that keeps ADP/ACMP/AECP's command paths short. Either hart meets
  10 ms at the share.
- **That hart needs:**
  - the gptp channel's rx/tx rings;
  - the TIMESTAMP and LINK events;
  - the 1 ms tick;
  - the publication window with its `GEN` commit;
  - the CSR's PTP block (rate, step, settime, time read);
  - +11.1 KB ROM and +1 KB SRAM a port.
- **Its state is self-contained** (`struct gptp_port`), so nothing is shared across harts.

## 5. Owed for bench qualification (no bench this round)

- 802.1AS-2020 clause behaviour on the wire against a reference grandmaster and a reference slave on the test
  machine: BMCA, asCapable, the Pdelay cease, the receipt timeouts and the path trace.
- Lock time and steady offset with real PHYs. That means the egress/ingress latency constants of the board's PHY
  (`INGRESS_LAT_NS_P`, `EGRESS_LAT_NS_P`) and the ±11.2 ns digital bound plus the PHY's.
- A long soak: offset histogram and rate wander, with no step after lock.
- Milan v1.2 AVB_INFO/AS_PATH served from the publication, read by the reference talker's controller.
- The CPU figures re-measured on the board's hart with real interrupts and traffic.

## 6. Round 2 plan

- **R2-1.** The second MAC's PHC and timestamp unit: a second port elaborated, and the 2if closed loop with two peers.
- **R2-2.** The fabric plane's deletion on this line. `GPTP_PLANE_EN_P`, its suites and `tb/verilator/gptp_txts`
  (still grading the plane's ledger) move. This waits for OWNER DECIDES 6.
- **R2-3.** The publication narrowed to what fabric logic consumes: about −1.8k FF and −0.7k LUT, measured by
  synthesis before it is claimed. This waits for OWNER DECIDES 7.
- **R2-4.**
  - The census elaborates a `GPTP_SW_EN_P` shape, with a plant for `GPTP_SW_ONLY`.
  - The closed loop gets planted defects: servo sign, timestamp pairing, rate ratio.
  - The harness's gptp groups run at 8x8/2if.
- **R2-5.** The adapter gated on its event bits, taking idle cost to about 0. Then 64x64/2if is measured on [A813]'s
  hart split, once its memory plan places the gPTP image.
- **R2-6.** The bench qualification of section 5, once bench access is granted.

## OWNER DECIDES

1. **The `gptp` family's 10 ms bound.** It is IEEE 802.1AS-2011 B.2.3's turnaround itself, not a 10 % of it;
   Milan v1.2 4.2.6.2.6 tolerates 15 ms. Also whether THE SHARE should follow it (today it does not).
2. **The gptp channel's admission:** burst 16, refill 10 ms, provisional.
3. **A minimal fixed-point 802.1AS core (this round) or flexPTP itself.** flexPTP needs a donor change to drop
   float/libm and to allow two instances.
4. **The memory ledger for gPTP images at 8x8 and above:** +2.5 to +3.0 RAMB36. The 8x8/2if image is already
   over 56 without gPTP.
5. **The second PHC and timestamp unit with the second MAC** (Milan v1.2 8.3.4: one PHC a port).
6. **The requirement text:** NFR-SCOUT-02 and NFR-SCOUT-03 now say the optimisation line removes the plane now.
   Also when the plane's RTL is deleted, rather than left unelaborated under `--sw-gptp`.
7. **Narrowing `milan_csr`'s gPTP status block** (path trace, parent identity) under `--sw-gptp`, so the
   publication can shrink from 22 words to 4 (R2-3). The block is a documented interface (REGISTER_MAP).

## Merge surface (hunks other lanes merge with)

Measured against each lane's head now: [A808] `6e29d496`, [A812] `f0854a50` (no common file), [A813] `d661dcac`.
Line numbers are the base's.

| File | This lane | [A808] opt-exec | [A813] opt-hart2 | Expected |
|---|---|---|---|---|
| `docs/reference/FR_NFR.md` | NFR-SCOUT-02/03 rows (329-330) | | line 8; NFR-SCOUT-01/03 rows (328-330) | textual conflict on the NFR-SCOUT-03 row; keep both sentences |
| `sw/litex/milan_soc.py` | `MilanSoC.__init__` signature (3636) and 19 more hunks | | same signature (3637), 3414-3426, 3792, 4395, 4729, 5076 | conflict on the `**kwargs):` line; keep both keywords |
| `docs/DOCUMENTATION_AUDIT.md` | counts (30-39), 98, 165, 310, 433 | counts (30-40), 101, 214 | counts (30-39), 98, 179 | regenerate with `docs_inventory.py --write` after merge |
| `tb/verilator/ctrl_service_budget/run.py` | `--with-gptp` (609), 821-925 | 624, 639, 927 | | adjacent at 921/927; check by hand |
| `tb/verilator/ctrl_service_budget/scenario.py` | `CEILING_MS` (99), `all_groups` (993-998) | 673 (+85 lines) | | no textual overlap, but at the 1,000-line module limit: [A808]'s +85 needs a split |
| `tb/verilator/ctrl_service_budget/README.md` | 510, 522 | 292 | | no overlap |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` | 168, 185, 227 | | 116-128 | no overlap |
| `docs/README.md` | 71 | | 83 | no overlap |

`grade.py`, `selftest.py`, `scenario.py` and `rows_tiers.py` are at exactly 1,000 lines, the Python long-module
limit. A lane that adds lines there merges into a module split, as this lane did (`channel_gate.py`, `refusal.py`,
`ts_pads.py`, `selftest_opened.py`).

Files only this lane touches: contract 2.5 (`mailbox.yaml` and the generated `KL_mbx_pkg.sv`, `KL_mbx.sv`,
`mbx_contract.h`, `MAILBOX_CONTRACT.md`), `KL_mbx_cdc.sv`, `KL_mbx_evt.sv`, `KL_ctrl_split.sv`,
`milan_datapath.sv`, `gptp_owner_contract.py`, the firmware `mbx` layer and host model, the `mbx`/`milan_dp`
benches, and the new gptp sources and benches. **Every other lane's image changes when it merges contract 2.5,**
because a regenerated `mbx_contract.h` moves the event and publication offsets.

## Gate table

Clean clone `g2` at `eea4a361`; the harness self-test at `c1e3055c`. The only difference is four harness self-test
files: the fixture trim, a re-trimmed `fixture.log` with every pinned row unchanged, and `oracle.json`'s digest.
The fast gates that read those files were re-run at `c1e3055c`. Logs are in `receipts/gates/` and alongside each
bench.

| Gate | Command | Result |
|---|---|---|
| docs wording and privacy | `scripts/docs_check.py` | 0 findings |
| em dash | `scripts/check_em_dash.py --base 15168e14` (pinned renderer) | 0 findings over 529 added lines |
| contents and anchors | `scripts/gen_toc.py --check`, `--verify-anchors` | OK |
| doc style, paths, gPTP pages, inventory | `check_doc_style`, `check_doc_paths`, `check_gptp_docs`, `docs_inventory --check` | OK |
| Python, SV, C++, shell idioms | `check_py_idiom`, `check_sv_idiom`, `check_cpp_idiom`, `check_sh_idiom` | OK, no ratchet raised |
| hygiene, TODO, bare-metal, feature status, archive | the five `check_*` gates | OK |
| RTL source lists, SoC sources, port contracts | `check_rtl_source_lists`, `check_soc_sources`, `check_port_contracts` | OK (114-file closure) |
| module matrix, register reference | `gen_module_matrix --check`, `gen_register_reference --check` | fresh (regenerated) |
| naming, test evidence, fail-fast, CI events | `measure_naming`, `measure_test_evidence`, `measure_fail_fast`, `ci_events --check` | PASS |
| RTL lint | `scripts/lint_rtl.py --check` | PASS, 89 <= 89 |
| Vivado front end | `scripts/xvlog_gate.py --check` | PASS, 0 findings |
| mailbox contract | `sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | 0 findings, selftest 0 failed |
| mbx suites | `make -C tb/verilator/mbx all` | every suite PASS; mutants 13/13, record mover 25/25 |
| datapath, split | `make -C tb/verilator/milan_dp split` | 145 checks, 0 failures |
| datapath, split crossing | `make -C tb/verilator/milan_dp split-cdc` | 13 checks, 0 failures |
| timestamp unit | `make -C tb/verilator/gptp_tsu run`; `tsu_mutants.py` | 33 checks PASS; 16/16 killed |
| Yosys, the unit | `syn/yosys/run.sh --top KL_gptp_tsu` | PASS, 2,824 cells; tied-input and tap-purity PASS |
| firmware port | `gptp_arms.all_arms` (host, RV32IM) | 34 + 4 checks PASS; text 11,674 B |
| firmware port defects | `gptp_mutants.py` | 25/25 killed |
| closed loop | `make -C tb/verilator/gptp_sw run` | 13 checks PASS |
| firmware gate | `test_ctrl_firmware.py --require-rv32` (all arms, no mutation) | PASS, 90 arms, 76 suite verdicts PASS |
| publication census | `publication_census.py --check --selftest --jobs 3` | PASS: 6 shapes, 246 checks; 221 plants refused; 0 of 57 rules unproven |
| harness self-test | `run.py --self-test` at `c1e3055c` | 1,015 checks PASS; 295/295 mutants caught; "self-test: 0 failures" |
| synthesis S2 | Vivado 2026.1, 8x8/1if, `--sw-gptp` | rc 0; section 2 |
| harness legs, final head | `run.py --point 1x1 --groups gptp-slave,gptp-master --with-gptp` | 0 refusals, 0 misses, 0 of 373 passes over the 2 ms share; cycles as section 4 |

Not run this round: the hosted CI, the firmware gate's `--self-test` (planted-defect shards), the act replica (no
PR), and the full Yosys sweep (only the new top).

Receipts: `receipts/INDEX.md`, generated from the files present.
