> ⚠️ **SUPERSEDED / HISTORICAL** — archived 2026-07-23. Kept for history; **not current state**.
> Living successor: `findings/HANDOVER_SMALL.md` (live state) + `findings/BENCH_TOPOLOGY.md`. Index: `docs/archive/README.md`; orientation: `docs/SYSTEMS_ENGINEER_GUIDE.md`.

# Session handoff  -  results, topology, harness (read this first)

*Updated 2026-07-11 night. This page states RESULTS and live state; the deep
narratives live in the dedicated docs: PIPELINE_STAGES.md (RX/TX stage map +
obsolete-code ledger), HEADER_SPLIT_DESIGN.md (hs silicon history),
RX_PERF_TUNING_MAP.md (maintainer knob map), BUILDING.md (two-board build/flash
flow), RUNNING_TESTS.md (test layers), QSPI_FLASHBOOT.md (boot),
TROUBLESHOOTING.md (bug forensics incl. section 15 CBS/attribution),
GIGABIT_HEADROOM_ANALYSIS.md + PERFORMANCE_GOAL.md (the why).*

## 1. Results  -  where everything stands

**Standing goal: >500 Mbit/s best-effort TCP both directions at MTU 1500** on
the fully-FPGA Milan NIC (AX7101, 2x VexiiRiscv RV64 @100 MHz, clock locked at
100 by user decision), plus the Milan v1.2 product plane (ADP/AECP/streams).

### Performance (socket TCP, MTU 1500, measured on silicon)

| Metric | Result |
|---|---|
| TX | 525-536 (r2slots-era cell; see the cell-recipe caveat below) |
| RX multi-flow keeper | 381 steady / 374 soak, P4, hsq10-16K + hsplit12 |
| RX single-flow record | 340 steady (hs); cut-through P1 329 (hsq12+hsplit14, parked: multi-flow regresses) |
| RX no-copy ceiling | 585-594 (MSG_TRUNC, P2/P4)  -  proves the >500 lane exists |
| Consumer-ladder verdict | plain copy 363-381 beats every no-copy API on this core+kernel (AF_PACKET ring 124; TCP zc-flip 110 at 87 pct flipped; both REFUTED); remaining >500 lane = AF_XDP ZC driver (campaign-scale) |
| UDP | TX 24 / RX 65 goodput (no TSO/coalesce; not a campaign target) |

⚠ CELL-RECIPE CAVEAT (2026-07-11): a gate number is only valid with its FULL
cell recipe. The 525-536 TX does NOT reproduce in the current default cell
(iperf3 single TCP, hsplit=2/16K/napi_w=48/rsc/hwtso/hwcs, threaded=0,
hash_sel=1, via the AVB switch): BOTH hsq14_spr and cbsf_epo measure ~221
there, with an identical recurring mid-flow stall (env/driver-config class,
open). Never declare a silicon regression without re-measuring the keeper
in-session; A/B in-session is the only valid comparison.

### AREA-70 campaign: CLOSED (silicon keeper = build_cbsf_epo)

| | start (hsq6) | keeper (cbsf_epo) |
|---|---|---|
| LUTs | 51908 (81.9 pct) | **44439 (70.1 pct)** |
| Slices | 96.8 pct | 91.8 pct (packing-bound: 75 pct fill) |
| BRAM | ~79 pct | 112.5 tiles (83.3 pct)  -  the tightest resource |
| WNS | +0.243 | +0.099 |

Banked levers: CQ LUTRAM diet -4866, strip-probes -1135, **CBS sequential
slope engine -6.7K** (serial divider replaces per-cycle divide cones;
bit-exact, multicycle XDC deleted; TROUBLESHOOTING section 15), **byte-ring
fold -781** (legacy_ring elaboration param, ship default folded, unarmed
engines quiesce; PIPELINE_STAGES ledger). Refuted by measurement: the
milan_csr decode brief (927 LUTs standalone; the 5179 was cross-boundary CBS
cones  -  OOC-synth before believing hierarchical reports), the area-synth flow
(trades +6.5 BRAM for -3-5K LUTs while BRAM binds), the is_hdr constant pin
(made the writer BIGGER). Section V complete on cbsf_epo: boot, ID=MILN,
pairing probe, ghost-peer ARP, TX gate == keeper, RX in-session A/B P1 335 vs
330 / P4 ~325 vs ~280 (equal-or-better). **Open user decision for slices <70
pct: the 2nd hart costs 7646 LUTs + 20 BRAM + 16 DSP + 11 slice-points
(1-hart measured: 58 pct LUTs / 68.5 pct BRAM / 80.9 pct slices) but retires
the 2-hart NAPI pipeline that holds the RX records.** Remaining polish:
--rx-fifo-beats 1024 BRAM diet (flag staged, needs a silicon drop-gate).

### Milan product plane (the AVB-switch era, started 2026-07-11)

The lab is now TWO Milan nodes through an AVB bridge (section 2). First
product smoke found and fixed TWO silicon bugs in the ADP advertiser path,
both invisible before the switch existed:
1. **Enable-after-boot never advertised** (const-link SoC swallowed its only
   link-up pulse while ADP was disabled at reset): the wrapper now synthesizes
   the link-up event on the ADP-enable rising edge; proven on silicon
   (available_index advances) + milan_dp regression.
2. **Source MAC byte-swapped = MULTICAST source address**, which 802.1D
   bridges MUST drop (index advanced, wire silent through the switch): the
   platform mac_addr CSR is LSB-first, the advertiser port is numeric EUI-48;
   byte-reverse added at BOTH instantiation sites (fully-FPGA wrapper + Zynq
   top, same latent bug) + egress-src regression. milan_dp now 17 checks.
**WIRE PROOF LANDED (ax7101_adp2, WNS +0.102, flashed)**: the peer captured
ENTITY_AVAILABLE through the AVB switch  -  src 02:00:00:00:00:01 (fix 2
proven), dst 91:e0:f0:01:00:00, ethertype 0x22F0, subtype 0xFA, valid_time
31, the programmed entity_id, available_index advancing per strobe. The
first Milan ADP advertisement this NIC has ever transmitted.

### Arty A7-100 (second Milan node)  -  port done, bring-up in progress

`--board arty` in milan_soc.py: MII 100M DP83848 + 25 MHz eth_ref_clk out,
MT41K128M16 DDR3, clk100/-1-speedgrade CRG, serial boot (spiflash not ported).
The -1 die does NOT close the AX7101 clocking: measured WNS -0.527 (100 MHz
sys) and -1.026 (83 MHz sys with the datapath still at 100)  -  the datapath
domain is the wall. Canonical arty clocking (in build.sh cfg_arty): **sys
83.333 MHz (the clean VCO-1000 divisor set; 90 MHz has NO PLL solution with
the 25 MHz ref) + datapath 50 MHz** (3.2 Gb/s internal for a 100 Mbit wire).
**Milestone 1 COMPLETE (build_arty_v2, WNS +0.091)**: BIOS up, VexiiRiscv x2
@83 MHz, DDR3 256 MiB @666 MT/s Memtest OK (105.8/269.4 MiB/s), and
mem_read 0x90000000 = MILN  -  the datapath lives on board 2. Next
increments: Linux/DT (83 MHz timebase, 256 MB, MII), kl-eth at 100M, IP
.3, two-node ADP discovery through the switch; later S25FL128S flashboot.

### Hardening shipped

hs page-size pairing is LETHAL (driver hs_pgsz != gateware hs_page_bytes =
DMA overrun = kernel panic, 2026-07-11). SHIPPED: hsq14 capability CSR
@0xf000311c + hsplit16 probe-check  -  the driver refuses lethal pairings with
-EINVAL (silicon-verified both ways). Byte-ring fold quiesce: old bd=0
drivers on folded gateware park with counted drops, never DMA to address 0.

### Open threads (ranked)

1. arty_v2 + ax7101_adp2 builds -> Arty milestone 1 + the ADP wire proof.
2. Two-node ADP discovery (Arty RX of the AX7101's ENTITY_AVAILABLE), then
   AECP/entity model per MILAN_V12_DEPENDENCY_MATRIX.md.
3. The ~220 cell-recipe gap + recurring TX mid-flow stall (both gatewares,
   env/driver-config class: sweep napi_w/hsplit/rsc on the keeper).
4. Slices <70 pct: the 1-hart user decision (numbers above).
5. AF_XDP ZC driver = the remaining RX>500 lane (campaign-scale).
6. TX 2-proc fairness (CONFIG_NET_SCH_FQ kernel rebuild or BQL).

## 2. Topology  -  what plugs into what

```
┌─────────────── dev VM (this machine) ────────────────────────────┐
│ /home/alex/prjs-avb-on-fpga/milan-fpga   (RTL repo)               │
│ /home/alex/milan-tests-avb               (driver)                 │
│ /home/alex/litex-milan/work/build_*      (builds)                 │
│                                                                   │
│  USB (by-id ONLY, numbers shift): FT232H = AX7101 JTAG,           │
│  CP2102N = AX7101 console, FT2232 210319AFEED0 = Arty JTAG+UART   │
└───────────────┬─────────────────┬─────────────────┬──────────────┘
                │ JTAG+serial     │ JTAG+serial     │ (no data plane
                ▼                 ▼                 │  on the VM)
     ┌────────────────────┐  ┌────────────────────┐ │
     │  AX7101 (Milan #1) │  │ Arty A7-100 (#2)   │ │
     │  192.168.127.1     │  │ 192.168.127.3 plan │ │
     │  1 GbE GMII        │  │ 100M MII           │ │
     └─────────┬──────────┘  └─────────┬──────────┘ │
               │ 1G                    │ 100M       │
            ┌──▼────────────────────────▼──┐        │
            │        AVB SWITCH            │        │
            │  (gPTP/SRP-capable bridge,   │        │
            │   added 2026-07-11)          │        │
            └──────────────┬───────────────┘        │
                           │ 1G                     │
                    ┌──────▼───────┐                │
                    │  amx-pw0     │◄───────────────┘ ssh (mgmt net)
                    │ i210 enp6s0  │
                    │ 192.168.127.2│
                    └──────────────┘
```

- **Since 2026-07-11 the data plane is SWITCHED**: both Milan boards and the
  peer's i210 hang off an AVB (802.1BA-class) bridge  -  the product interop
  topology (ADP discovery board<->board, gPTP domain through the bridge, SRP
  reservations, CBS-shaped streams). Perf cells now traverse the switch; the
  in-session A/B discipline (keeper re-measured in the same session) absorbs
  any switch-induced shift, but never compare switched numbers against the
  direct-cable era without an in-session baseline.
- **Data-plane peer = `ssh amx-pw0`** (passwordless, passwordless sudo). Its i210
  (`enp6s0`, MAC `68:05:ca:95:b2:d1`) is at **192.168.127.2**.
  **`amx-pw1` is RESERVED  -  never touch it.**
- IP plan: AX7101 = .1, peer = .2, **Arty = .3** (once its Linux is up).
- The VM has NO data-plane path to the boards (virtio/isolated NICs). JTAG +
  serial only. Do NOT add 192.168.127.x addresses on the VM.
- **Ghost-peer check before trusting ANY number**: on the board,
  `ip neigh | grep 127.2` must show `68:05:ca:95:b2:d1`. Stale services answering
  .2 from elsewhere invalidated a whole night once (now MORE relevant: a switch
  means more places for a ghost to answer from).

## 3. How to connect

**⚠ TWO BOARDS SINCE 2026-07-11 (user added a Digilent Arty A7-100)  -  ttyUSB
NUMBERS SHIFT ON EVERY REPLUG; USE /dev/serial/by-id/ PATHS AND --ftdi-serial
EVERYWHERE:**
- AX7101: JTAG = FT232H "Digilent USB Device" serial **210512180081**
  (`openFPGALoader --ftdi-serial 210512180081 -c ft232 <bit>`); console =
  CP2102N, by-id `usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0`
  (re-attached 2026-07-11; a replug changes the host USB address, so the VM
  passthrough rule must be re-added when it drops).
- Arty A7-100 (xc7a100tcsg324-1, MII 100M DP83848, MT41K128M16, -1 speedgrade):
  ONE FT2232 serial **210319AFEED0** = JTAG (if00) + UART console (if01).
  JTAG: `openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <bit>`
  Console: by-id `usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0`.
  Build: `--board arty` (milan_soc.py; MII PHY + 25 MHz eth_ref_clk out,
  serial boot only  -  spiflash not ported). First build: build_arty1.
  Role: second Milan node for AVDECC/Milan interop + the 100M CBS point.

**AX7101 console** (tmux session `milan_qspi_boot`, recreate if dead  -  litex_term
needs the venv path; use the by-id path of the CP2102N once it re-enumerates):
```sh
tmux new-session -d -s milan_qspi_boot \
  "/home/alex/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0 --speed 115200"
```
**Arty console**:
```sh
tmux new-session -d -s arty_console \
  "/home/alex/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0 --speed 115200"
```
Scripted exec on it: `scratchpad/conx.sh '<cmd>' <timeout>` (unique-tag markers;
survives garbled output). `dmesg -n 1` first on the board. NEVER
`pkill -f litex_term` / `tmux kill-server`  -  kill exact PIDs only.

**Load a bitstream (JTAG SRAM  -  flash holds NO bitstream by design):**
```sh
openFPGALoader -c ft232 ~/litex-milan/work/build_hsq5/gateware/alinx_ax7101.bit
```
Boot is hands-free from QSPI images (SPIFLASH_SKIP_FREQ_INIT validated; ~75 s to
login incl. 35 s initramfs unpack; the "invalid magic" line at ~35 s is benign).
**Power-cycle ⇒ FPGA blank ⇒ JTAG load required.** NEVER `openFPGALoader -f <bit>`
(clobbers the kernel at flash offset 0  -  recovery recipe in QSPI_FLASHBOOT.md;
manual flashboot fallback: `scratchpad/manual_flashboot.sh`).

**Board network + driver (fresh boot):**
```sh
# on the console (root, no password):
ip addr add 192.168.127.1/24 dev eth0; ip link set eth0 up
wget -O /tmp/kl10.ko http://192.168.127.2:8000/kl-eth-hsplit10.ko
rmmod kl_eth; insmod /tmp/kl10.ko rsc=1 rsc_clk_mhz=100 hwtso=1 hwcs=1 hsplit=1
ip addr add 192.168.127.1/24 dev eth0; ip link set eth0 up
echo 0 > /sys/class/net/eth0/threaded; ethtool -C eth0 rx-usecs 500
wget -O /tmp/recv_spin http://192.168.127.2:8000/recv_spin; chmod +x /tmp/recv_spin
```
`hsplit=0` = legacy/mslot-equivalent mode (same .ko). **Driver↔gateware pairing is
STRICT**: hsplit10 (BD ring 256) needs the hsq6+ full-gate  -  on ≤hsq5 it laps the
ring SILENTLY (8-bit seq aliases at 256). hsplit9 (BD 64) is the ≤hsq5 driver. On
2-queue gateware (hsq3) also `devmem 0xf0003094 32 1` (hash_sel→q0) BEFORE TCP; on
1-queue hs builds (hsq4/5/6) that CSR does not exist  -  don't poke it.

**Peer services (amx-pw0, serve dir /tmp/serve):**
```sh
ssh amx-pw0 'cd /tmp/serve && setsid nohup python3 -m http.server 8000 --bind 0.0.0.0 \
  >/tmp/serve/http2.log 2>&1 & setsid nohup /tmp/serve/blast2 5202 >>/tmp/serve/blast2.log 2>&1 &'
```
`blast2` = instrumented TCP sender (logs bytes+errno per connection death). Kill
STALE listeners by exact PID first  -  a wedged old blast produced a fake "collapse."
Stage new driver builds: `scp kl-eth.ko amx-pw0:/tmp/serve/kl-eth-<ver>.ko`.

## 4. How to harness

**Sim/test layers:** see **RUNNING_TESTS.md** (elab smoke + Migen-codegen grep →
`test_ring_bd.py` suite (42 tests incl. the livelock regression and the
byte-ring-fold equivalence/quiesce pair; plain python, no
pytest) → 18 Verilator harnesses (`tb/verilator/*/make`) → Yosys (`syn/yosys/run.sh`)
→ Vivado build scripts (`~/litex-milan/work/build_*.sh`, ≤32 threads, read the LAST
timing summary) → silicon §V checklist). Cycle-exact debugging: `dbg_*` aliases on
RingDMAWriter + the stoppable full-rate watcher via `h.run(stim, extra_gens=[...])`.

**Driver build** (kl-eth, out-of-tree against the buildroot kernel):
```sh
cp /home/alex/milan-tests-avb/fpga/kl-eth/kl-eth.c /home/alex/br-milan-output/build/kl-eth-1.0/
cd /home/alex/br-milan-output/build/kl-eth-1.0 && \
PATH=/home/alex/br-milan-output/host/bin:$PATH make -C /home/alex/br-milan-output/build/linux-7.0.11 \
  M=$PWD ARCH=riscv CROSS_COMPILE=riscv64-buildroot-linux-gnu- modules
strings kl-eth.ko | grep version=        # ALWAYS verify before staging
```

**Measurement discipline** (the rules that kept this campaign honest):
- Sustain metric = peer tx_bytes 5 s deltas ×5+ (`ssh amx-pw0 cat
  /sys/class/net/enp6s0/statistics/tx_bytes`); short cells are slow-start-flattered.
- Cells: `recv_spin <ip> 5202 <cport|0> <secs> 0 0 1 262144` on the board; -PN =
  N instances with distinct cports. `recv_zc` for zerocopy (same args).
- Every cell: drop delta (`devmem 0xf000303c`), `dmesg | grep -c pairing`,
  close-reason deltas when diagnosing (@0xf00040cc..d8: psh/cap/tout/park).
- perf on the board: timer-only (`-F 250`), symbolize on the host via System.map  - 
  full method in PERF_ON_MILAN.md.
- Measure, don't assume  -  probe first, before AND after (measure-dont-assume rule).

**Current board state (2026-07-11 night):** AX7101 = build_ax7101_adp2
(JTAG-SRAM: cbsf_epo keeper shape + BOTH ADP fixes, WNS +0.102) + hsplit16
hsplit=2 hs_pgsz=16384, network up, ADP enabled and advertising (EID
02:00:00:ff:fe:00:00:01). Arty = build_arty_v2 (JTAG-SRAM, WNS +0.091),
sitting at the LiteX BIOS console (milestone 1 passed; no Linux yet). Gateware
lineage table: PIPELINE_STAGES.md; the hsq3..hsq14 ladder history:
HEADER_SPLIT_DESIGN.md.
