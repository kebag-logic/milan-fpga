# HANDOVER — machine, topology, live state, tasks

Updated 2026-07-14 (post Milan-talker-SM close-out, milan-fpga @ `3fce652`).
This is THE entry point for a fresh session or person: everything needed to
operate the bench, trust the current state, and pick the next task. Detail
lives in the named normative docs; this file states what is true NOW.

**Project in one paragraph:** a fully-FPGA Milan v1.2 AVB endstation — the
whole TSN datapath AND the AVDECC control plane (ADP + AECP/AEM + ACMP talker
SM) run in fabric, zero-CPU; a VexiiRiscv 2-hart Linux softcore does only
provisioning, linuxptp and ops (USER DIRECTIVE rev 2: "everything goes FPGA,
use lwSRP" — normative split: `docs/design/ARCHITECTURE_HW_SW_SPLIT.md`).
Roles: AX7101 = the full endstation (:01), Arty A7-100 = a small endstation
(:02), nothing bridge-side in scope. Both boards are silicon-validated
**Milan=1 CLEAN** (la_avdecc) as of 2026-07-14.

---

## 1. Topology

```
┌──────────────── dev VM (this machine) ──────────────────────────┐
│ repos + Vivado + buildroot + build tree (see §2)                │
│                                                                 │
│ USB passthrough (BY-ID ONLY, numbers shuffle on every replug):  │
│  FT232H  210512180081 = AX7101 JTAG                             │
│  CP2102N 66e0ce96...  = AX7101 console (115200)                 │
│  FT2232  210319AFEED0 = Arty JTAG (if00) + console (if01)       │
└──────┬──────────────────┬───────────────────────────────────────┘
       │ JTAG+serial      │ JTAG+serial          (VM has NO data
       ▼                  ▼                       plane; mgmt ssh
┌──────────────┐   ┌──────────────┐               to amx-pw0 only)
│ AX7101       │   │ Arty A7-100  │
│ full endstn  │   │ small endstn │
│ EID ...:01   │   │ EID ...:02   │
│ 192.168.127.1│   │ .3           │
│ 1G GMII      │   │ 100M MII     │
└──────┬───────┘   └──────┬───────┘
       │ 1G               │ 100M
     ┌─▼──────────────────▼─┐   d&b audiotechnik AVB switch
     │      AVB SWITCH      │   (OUI 3c:c0:c6, clock 3cc0c6.fffe.fe0210)
     └──────────┬───────────┘   remote power-cycle via amx-pi
                │ 1G (uplink = the only full-control-plane port)
        ┌───────▼──────┐
        │ amx-pw0 i210 │  192.168.127.2  enp6s0  68:05:ca:95:b2:d1
        │ (ssh, sudo)  │  controller drills + la_avdecc live here
        └──────────────┘
```

- **amx-pw1 is RESERVED — never touch it.** The VM never gets a
  192.168.127.x address.
- Entities: AX EID `02:00:00:ff:fe:00:00:01` (MAC 02:00:00:00:00:01),
  Arty EID `...:02` (MAC ...:02). stream_id = {station_mac, uid16} —
  byte-identical across ACMP/AECP/AVTP by construction (bug fixed 07-14).
- Switch behavior is DEFINITIVE (docs/findings/GPTP_RXPAD_ROOTCAUSE.md):
  edge ports are GM-source+pdelay BY DESIGN — boards never receive
  Sync/Announce through it; board-as-slave = direct cable only. Relay recipe
  = exactly ONE strong GM claimant (port 8, prio1 100, cc6). It forwards only
  registered AVB multicast between edge ports and INGRESS-FILTERS VLAN 2
  (hence the VID0 priority-tag policy until lwSRP/MVRP registers VLANs).
- A second session may drive the bench concurrently (attribute ptp4l deaths
  via ps before debugging "crashes").

## 2. Machine (dev VM)

Arch Linux VM, **96 vCPU / 31 GB RAM**. No data-plane NIC (rule above);
bench reach = ssh amx-pw0 (passwordless sudo) + USB serial/JTAG.

| Path | What |
|---|---|
| `~/prjs-avb-on-fpga/milan-fpga` | THIS repo: RTL (`hdl/`), testbenches (`tb/`), LiteX SoC + build system (`sw/litex/`), controller (`avdecc/`), docs |
| `~/milan-tests-avb` | kl-eth Linux driver, DTs, boot images, buildroot glue (`fpga/`) |
| `~/prjs-avb-on-fpga/fpga-ps-tools` | BSP/DT extraction tools (main AHEAD-5 UNPUSHED — user's call) |
| `~/litex-milan` | LiteX env: **venv** `~/litex-milan/venv` + **work/** = all build dirs (~525) |
| `~/br-milan-output` | buildroot output: `images/` (Image, rootfs.cpio.xz), host toolchain, linux-7.0.11 tree; rootfs overlay incl. `.../board/milan_naxriscv/rootfs_overlay/etc/init.d/S50milan` (dir name is historical — CPU is VexiiRiscv) |
| `~/refs/AX7101` | Alinx board repo clone — reference ONLY, push disabled |
| `~/Xilinx`, `~/Xilinx2` | Vivado 2026.1 ×2; **build.sh sources `~/Xilinx2/2026.1/Vivado/settings64.sh`** (has Artix-7 + Zynq-7000) |

- Build env: `source ~/Xilinx2/2026.1/Vivado/settings64.sh` +
  `export PATH=~/litex-milan/venv/bin:$PATH`; long jobs via `setsid nohup`
  with a log under `~/litex-milan/work/` (plain bg jobs die with the session).
- `rtk` proxies/dedups CLI output (token filter); for forensics read raw
  files or `rtk proxy <cmd>`.
- git identities: milan-fpga = default (hackerman-kl); milan-tests-avb
  commits use `-c user.name="Alexandre Malki" -c user.email="alexandremalki89@gmail.com"`.
- pw0 tools: `/tmp/milan_controller.py` (deployed copy of
  `avdecc/milan_controller.py` — REDEPLOY after edits),
  `~/la_avdecc_work/enum-probe` (built with la_avdecc's OWN feature defines —
  ABI trap, see §8), tcpdump, iperf3.

## 3. Boards — facts + live state (2026-07-14)

| | AX7101 | Arty A7-100T |
|---|---|---|
| FPGA | xc7a100t-2fgg484 | xc7a100t-1csg324 (slower die) |
| CPU | VexiiRiscv 2-hart @100 MHz | VexiiRiscv 2-hart @83.333 MHz |
| Milan datapath clk | 100 MHz (`--milan-clk-freq 100e6`) | 50 MHz |
| PHY | RTL8211E GMII 1G | MII 100M |
| EID / IP | ...:01 / 192.168.127.1 | ...:02 / .3 |
| Gateware NOW | `build_ax7101_eto_miltalk` WNS +0.072, **JTAG-SRAM** | `build_arty_eppo_miltick` WNS +0.381, **in QSPI** |
| QSPI (16 MB) | policy `images`: Linux images only, kernel @0 — **NEVER flash a bitstream** (kernel-clobber trap; deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Image set = hwts4-era per-board rootfs + fixed opensbi/dtb | policy `boot` (v3): bitstream @0 (4 MiB) + xz kernel @0x400000 + opensbi @0x700000 + dtb @0x760000 + rootfs @0x780000; **JP1=QSPI, fully self-hosting** |
| Power-cycle | FPGA goes BLANK → JTAG reload needed | reboots to full Milan endstation hands-free |
| Driver | kl-eth auto-loads; `kl,rsc-clk-mhz` from DT (AX 100 / Arty 50); RSC on @250 µs | same |
| Talker | AAF present but **off** (talker half idle) | **TRUE Milan mode**: S50milan writes `0x654=0x1` → silent until PROBE_TX, then 8138 fr/s AAF from the Pmod I2S2, hard stop 15 s after last probe |

Both boards: probe window 14–15 s measured, ADP cadence 31 s (×2 periods),
dormancy self-heal ≤5 s proven, controller drill 41/41, la_avdecc Milan=1
CLEAN. Bench cosmetics: AX console needs `dmesg -n 1` under talker RX;
initramfs "invalid magic" after the real unpack is benign.

**gPTP bench end-state:** reflash bounces re-triggered the switch's port
flap-suppression → the Arty's cc6 announces are not relayed uplink; pw0 is
SLAVE ~5 ns to the SWITCH HOLDOVER (3cc0c6, cc248). Arty GM itself runs
clean (txto=0). Remedy is physical: switch power-cycle (amx-pi) or direct
cable. Data plane unaffected.

**Fallback builds** (all in `~/litex-milan/work/`):

| Build | What | WNS |
|---|---|---|
| build_arty_eppo_miltick | Arty KEEPER (param-fixed tick, flashed) | +0.381 |
| build_ax7101_eto_miltalk | AX KEEPER (talker SM; eppo/asl failed — sweep variance) | +0.072 |
| build_arty_asl_adpfix | Arty pre-talker fallback (dormancy fix) | +0.243 |
| build_ax7101_asl_adpfix | AX pre-talker fallback | +0.158 |
| build_ax7101_eto_hwts_ax2 / arty asl_hwts5 | HW-timestamp keepers | +0.118 / — |
| build_ax7101_eto_acmp2 | first Milan=1 CLEAN control plane | +0.096 |
| build_arty_asl_arty_v8 | first Arty AVDECC stack (probes stripped) | +0.312 |
| build_ax7101_adp2 / build_arty_v7 | AECP-less / probes-only floors | +0.102 / +0.018 |

**Branches (all pushed unless noted):** milan-fpga `milan-arty-bringup` =
3fce652 (the working line, this doc); `main` = f51a27b (PR #12 AECP/AEM
merged). milan-tests-avb `milan-avb-stabilizing-milan` = c03c139.
fpga-ps-tools main ahead-5 unpushed. Never commit `graphify-out/`/.gitprep.

## 4. What works on silicon today (and how it was proven)

| Feature | State | Proof / normative doc |
|---|---|---|
| ADP advertise + depart + **dormancy self-re-arm** | DONE both boards | drill 0x00020001→0x00020101 ≤5 s; `docs/findings/ADP_DORMANCY.md` |
| AECP/AEM Milan entity (5 descriptors, getters/setters, LOCK, MVU, COUNTERS, AS_PATH) | DONE | la_avdecc Milan=1 CLEAN; `hdl/aecp/doc/atdecc_architecture.drawio` |
| AECP streaming cmds (GET/SET_STREAM_INFO Milan semantics, START/STOP=NOT_SUPPORTED, **real unsolicited** 4-slot engine) | DONE | 121-check TB + drill §7/7b; `docs/design/MILAN_TALKER_SM.md` |
| ACMP Milan talker SM (CONNECT_TX==PROBE_TX, 15 s window, near-stateless) | DONE | 71-check TB + wire probe→stream→expiry; same doc |
| AAF talker (48 kHz I2S2 → class-A frames, probe-gated, VID0) | DONE | 8138 fr/s, seq+1/122 µs; `docs/design/MVP_TALKER.md` |
| gPTP PHC + **HW timestamps** | DONE both boards | pdelay 1.3 µs, pw0 rms 2–5 ns through floods; `docs/findings/PTP_TS_METADATA_FIX.md`, `GPTP_RXPAD_ROOTCAUSE.md` |
| QSPI v3 self-hosted boot (Arty) | DONE | flash→login hands-free; `docs/integration/QSPI_FLASHBOOT.md` |
| TCP perf (separate perf-lineage gateware) | TX >500, RX 316 practical ceiling | `docs/findings/PERFORMANCE_GOAL.md` |
| Portability | XPM-free HDL; Yosys/sv2v 20/20 tops (ECP5 check) | `syn/yosys/run.sh` |

Regression: 21 Verilator harnesses under `tb/verilator/<name>/` (latest
counts: acmp 71, aecp 121, milan_dp 53, adp 246, cls 200024) + Yosys 20/20.
`docs/testing/RUNNING_TESTS.md` / `PROTOCOL_VALIDATION_MATRIX.md`.

**The reference that decides Milan semantics:** pipewire module-avb
(`acmp-milan-v12.c` etc.) — ALWAYS extract the contract from it before
writing RTL; it overturned every assumption (probe model, count=0,
DISCONNECT no-op, stream_id formula).

## 5. CSR quickref (milan_csr AXI-Lite @ **0x90000000**, both boards)

Full map: `docs/reference/REGISTER_MAP.md`. The ones you touch on the bench:

| Offset | Reg | Notes |
|---|---|---|
| 0x100 | MAC_CTRL | bit3 allmulti (`ip link set eth0 allmulticast on` — reboot reverts) |
| 0x400+q*0x20 | CBS q0-3 | +0 idle +4 hi +8 lo +C en; reset en=0. Shaper is NEVER removed (user rule) |
| 0x520 | A_PTP_CMD | PHC discipline strobes (0x500 group = INCR/ADJ hooks) |
| 0x600 | ADP_CTRL | 0x1F01 = enabled, valid_time 31; 0x1F00 = silence (single-entity drills) |
| 0x604.. | identity | programmed by `avdecc/aecp_csr_setup.sh` (caps 0x8588) |
| 0x640 | ADP_CMD | bit1 = depart strobe (nothing in SW writes it — see dormancy forensics) |
| 0x644 | ADP_STATUS | available_index; healthy = +1 per 31 s (measure ≥2 periods) |
| 0x648/0x64C | AECP cmd/resp counters | balanced ⇒ no responder mid-frame |
| 0x650 | ACMP counters | |
| 0x654 | AAF_CTRL | {vid[27:16], bypass[1], enable[0]}; reset 0x0002_0002 (VID 2, bypass on). S50milan → 0x1 = TRUE Milan mode (probe-gated, VID0); legacy always-on = `devmem 0x90000654 32 0x3` |
| 0x658/0x65C | AAF DMAC | 0x660 frames / 0x664 pairs counters |
| 0x668 | A_ADP_DIAG RO | {[17:16] last depart src, [15:8] rearm_cnt, [7:0] depart_cnt} |
| 0x66C | A_ACMP_TALKER RO | {bit3 aaf_gate, bit2 lobs, bit1 talker_active, bit0 probe_armed} |
| 0x670 | A_ACMP_LOBS RW | bit0 = listener_observed — **the lwSRP socket** (manual until lwSRP) |

NIC ring/perf/debug CSRs live in the LiteX region (0xf0003xxx ring/steer,
0xf0004xxx probes) — perf-era docs in `docs/findings/`. devmem trap: 64-bit
CSRs read high-word-first.

## 6. Operating recipes

```sh
# Consoles (tmux; litex_term needs the venv path)
tmux new-session -d -s milan_qspi_boot \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0 --speed 115200"
tmux new-session -d -s arty_console \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0 --speed 115200"
# scripted console exec: send-keys + sentinel; grep '^MARKER' (line-anchored,
# else it matches the echoed command). Board busybox has NO timeout/pgrep.

# JTAG loads (SRAM)
openFPGALoader --ftdi-serial 210512180081 -c ft232    <ax7101.bit>
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <arty.bit>
# Arty: reconfigure from QSPI without power touch:
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent --reset

# Builds (sw/litex/build.sh; docs/integration/BUILDING.md)
./sw/litex/build.sh ax7101 --sweep      # 3-directive place sweep, keep best WNS
./sw/litex/build.sh arty   --sweep
# Flash (policy-aware; board_facts in build.sh):
KERNEL=~/br-milan-output/images/Image ROOTFS=~/br-milan-output/images/rootfs.cpio.xz \
DTB=~/milan-tests-avb/fpga/dts/milan_arty_vexii.dtb OPENSBI=~/milan-tests-avb/fpga/boot/opensbi_arty.bin \
PYTHON=~/litex-milan/venv/bin/python3 ./sw/litex/build.sh flash arty:<builddir>

# Milan validation drill (from pw0: ssh amx-pw0)
sudo python3 /tmp/milan_controller.py enp6s0 --eid 01   # AX   -> 41 pass, 0 fail
sudo python3 /tmp/milan_controller.py enp6s0 --eid 02   # Arty -> 41 pass, 0 fail
sudo ~/la_avdecc_work/enum-probe enp6s0 40              # Milan=1, verdict CLEAN
# enum-probe exits at its FIRST clean enumeration -> for a single-entity
# verdict, silence the other board first: devmem 0x90000600 32 0x1F00 (restore 0x1F01)

# ADP census — MUST filter, AVTP shares ethertype 0x22F0 (the arty's 8.1k fr/s
# AAF stream otherwise reads as an ADP flood / drowns :01):
sudo timeout 45 tcpdump -i enp6s0 'ether proto 0x22f0 and ether[14] = 0xfa'

# Probe the talker from pw0 (what activates the arty's stream):
#   milan_controller.py section 9 does it; window = 15 s after the last probe.

# Recovery one-liners (board console)
devmem 0x90000600 32 0x1F00; devmem 0x90000600 32 0x1F01   # ADP re-arm (pre-fix gw only)
dmesg -n 1                                                  # unbury console under RX
ip link set eth0 allmulticast on                            # gPTP RX (reverts on reboot)

# gPTP direct-cable session (Arty-as-slave validation, physical cable move):
sw/litex/gptp_direct_cable.sh   # AX=GM cc6/prio100; gates: SLAVE+rms, pdelay ~1-3us, txto=0
```

## 7. The rules (each one was paid for)

**USB / cables**
1. Serial consoles by `/dev/serial/by-id/` only, never ttyUSBn.
2. Every openFPGALoader call carries `--ftdi-serial` (two FTDI cables; a
   flash op on the wrong board is destructive).
3. VM USB passthrough is pinned by vendor:product (0403:6014, 0403:6010,
   10c4:ea60); a replug without the rule silently drops the device.

**Network / measurement**
4. amx-pw1 RESERVED; VM never gets a .127.x address.
5. Ghost-peer check before trusting any number: board `ip neigh | grep 127.2`
   must show `68:05:ca:95:b2:d1`.
6. A gate number is only valid with its FULL cell recipe; A/B in-session on
   the same cell (the cbsf_epo "TX regression" was a phantom baseline).
7. **Cadence claims need ≥2 periods** (the adpfix "31 s measured" was a
   single-period coin flip that hid the CLK-param gap for a day). ADP capture
   windows ≥70 s.
8. Measure, don't assume: no lever before its HW counter exists; decompose
   the symptom; measure before AND after (`docs/findings/` is full of
   refuted-plausible stories). OOC-synth a module before believing a
   hierarchical utilization line; read the LAST (physopt) timing summary.
9. Busybox `timeout` doesn't exist on the boards — a piped
   `timeout N tcpdump` dies instantly and fakes an empty capture.

**Pairing (LETHAL class)**
10. Driver `hs_pgsz` MUST equal gateware `--hs-page-bytes` (DMA overrun =
    panic). Capability CSR @0xf000311c + probe-check guard new pairs.
11. Ship gateware folds the legacy byte-ring; `bd=0` drivers park with
    counted drops. Arty driver domain = 50 MHz (DT `kl,rsc-clk-mhz` now
    carries it — zero-override boots).

**Flash policies (16 MB QSPI each; `board_facts` in sw/litex/build.sh)**
12. AX7101 = `images`: kernel at offset 0, NEVER flash a bitstream
    (deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Gateware JTAG-SRAM;
    power-cycle blanks the FPGA.
13. Arty = `boot` (v3): bitstream @0 + image set at shifted offsets; JP1=QSPI
    self-hosting. `build.sh flash arty:<dir>` does both stages + verify;
    sweep dirs get their layout reconstructed from soc.h.
14. OpenSBI is BOARD-SPECIFIC and EMBEDS a DTB (FW_FDT_PATH bypasses the
    flashed dtb slot). Build per board via build_opensbi.sh env; ALWAYS from
    a clean build dir (warm-tree rebuilds embedded the previous board's dtb —
    panic@0.000000; script force-cleans now).

**Builds**
15. 32 Vivado threads per build (hard cap), max 3 parallel on the 96-core
    box (USER RULE: saturate it — important configs = 3-seed sweeps, keep
    best WNS), launches staggered 90 s, always setsid.
16. Gate: WNS ≥ 0 (QSPI corrupted below +0.03 at 112.5 MHz once). Arty die
    is -1: sys 83.333 + datapath 50 is the closing clocking.
17. Elaborate WITHOUT --build first (~2 min) before burning 40 min of P&R.
    After scripted SV edits: grep the result AND read synth warnings —
    an undriven data input is silicon-silent (o_ptp_now trap; milan_dp TB
    now runs -Werror-UNDRIVEN).

**Repo / HDL**
18. Commits: ONE short line, no attribution trailers, both repos.
19. New HDL is ALWAYS SystemVerilog; Python only for soft-CPU SoC plumbing
    (USER RULE).
20. The CBS traffic shaper is never REMOVED from a build (USER RULE);
    bit-exact internal optimization is allowed.
21. Workstreams on separate branches; main receives merges. Push only on
    request.

## 8. Traps index (verified, still-live)

- **la_avdecc enum-probe ABI**: build against the lib's own feature defines
  (CBR/JSON/REDUNDANCY/STRICT_2018 + nlohmann) or the vtable mismatches and
  it SIGSEGVs on the first virtual call.
- available_index must +1 on EVERY ADPDU (bump-on-change reads as
  offline/online cycling to la_avdecc).
- ADP entity_id sits at wire byte 18 (not 16); ADP census filter
  `ether[14] = 0xfa`; CDL = frame_len − 26 (tsn-gen's model is WRONG).
- VID0 policy: stream_vlan_id legitimately reads 0 in ACMP/AECP responses —
  never assert vlan≠0 in drills; assert dmac≠0 + ACMP/AECP vlan consistency.
- Milan windows: poll at 0.2 s when measuring the 15 s probe window (1 s
  polls race the expiry and read short).
- kl-eth multicast RX: kl_set_rx_mode ignores mc groups — standalone ptp4l
  is DEAF without allmulti; reboot reverts it (proper fix = open task).
- Switch: multi-GM-claimant makes it announce-SILENT everywhere; one strong
  claimant only. Port flap-suppression from reflash bounces needs a physical
  remedy (power-cycle via amx-pi).
- LiteX `Instance(...)`: parameters are only passed if you pass them —
  `p_MILAN_CLK_FREQ_HZ` was silently defaulted for a week (2 s ticks).
  Grep the generated verilog for every new p_/i_/o_ hookup.
- iperf3/console orchestration: one-off servers (`-s -1`), fresh ports per
  cell, unique grep tags, `ssh -n` inside while-read loops.
- QSPI images from sweep dirs: `layout_from_soch.py` reconstructs the
  manifest (soc.h is the source of truth).
- Canonical Arty images: `br-milan-output/images/rootfs.cpio.xz` (Jul-13
  turnkey). `boot/rootfs.cpio.gz` is a STALE Jul-5 copy without S50milan.

## 9. Tasks

### Closed arcs (chronological; proof in §4)
M-A1..A5 bring-up → perf campaign (TX>500/RX 316, every remaining lever
measured-refuted) → area-70 phase 1 (CBS slope engine −8K LUTs) → de-Xilinx
track 1 (XPM-free + Yosys) → QSPI v3 flashboot → ADP advertiser → AECP/AEM
entity (Milan=1) → ACMP stateless responder → gPTP Phase A (PHC) + Phase B
(HW timestamps, rms 2–5 ns) → MVP AAF talker → ADP dormancy fix → **Milan
talker SM (ACMP PROBE_TX + AECP streaming + unsolicited) — closed 2026-07-14,
both boards Milan=1 CLEAN.**

### Open, ranked (next work; 1–3 are the USER-directed rev-2 order)
1. **lwSRP in fabric** — MSRP talker-advertise/listener-ready + MVRP;
   drives CBS idleSlope (≤75 % gate) and gates TX; `listener_observed` then
   comes from SRP instead of the manual A_ACMP_LOBS CSR; MVRP registers
   VLAN 2 (retires the VID0 workaround). Normative:
   `docs/design/LWSRP_FPGA_ARCHITECTURE.md` — **its CSR sketch 0x660–0x674
   is STALE (those addresses are now AAF/DIAG/ACMP): re-home to 0x680+.**
2. **pw0 PipeWire listener (BIND_RX)** — module-avb listener against the
   arty talker = the audible end-to-end; then media clock recovery (NCO from
   gPTP) per `docs/design/MVP_TALKER.md`.
3. **Fabric ACMP connection table** — acceptance = resource check vs the
   lwSRP grant (rev-2 delimitation).
4. **gPTP direct-cable session** — Arty-as-slave validation; script ready
   (`sw/litex/gptp_direct_cable.sh`), needs the physical cable move.
5. **Switch power-cycle via amx-pi** — clear flap suppression, restore the
   Arty-GM→pw0 relay.
6. **kl-eth set_rx_mode** — honor mc groups (allmulti workaround reverts
   every reboot).
7. **is_1g CBS slopes on the Arty** — true class-A shaping at 100M (today
   the talker injects post-shaper, unshaped).
8. **One-opensbi durable form** — BIOS passes a1=dtb, platform reads
   timebase from FDT (removes the per-board opensbi class).
9. **Priority TX ring / doorbell in kl-eth** — the gPTP TX-flood delay is
   the single 256-slot TX ring.
10. **Area-70 continuation** (USER directive: slices → ~70 %) — next lever:
    byte-ring fold.
11. **Perf follow-ups** (perf lineage): ~220-vs-525 cell-recipe gap, TX
    mid-flow stall, AF_XDP ZC (the RX>500 lane).
12. **Arty listener half** (STREAM_INPUT/CRF) — the small endstation's
    natural next role.
13. **AECP deferred**: NV persistence of SET_*, real HW counter wiring,
    audio maps, MAAP, GET_DYNAMIC_INFO.
14. fpga-ps-tools: push main (ahead-5) — user's call.

### Doc index (normative first)
`docs/design/ARCHITECTURE_HW_SW_SPLIT.md` (rev 2 split) ·
`docs/design/MILAN_TALKER_SM.md` (talker contract + SM) ·
`docs/design/LWSRP_FPGA_ARCHITECTURE.md` (next arc; CSR sketch stale) ·
`docs/design/MVP_TALKER.md` · `docs/overview/FULL_FPGA_SOLUTION.md` ·
`docs/reference/REGISTER_MAP.md` · `docs/integration/BUILDING.md` ·
`docs/integration/QSPI_FLASHBOOT.md` · `docs/testing/RUNNING_TESTS.md` ·
`docs/testing/PROTOCOL_VALIDATION_MATRIX.md` · findings:
`ADP_DORMANCY.md`, `GPTP_RXPAD_ROOTCAUSE.md`, `PTP_TS_METADATA_FIX.md`,
`PERFORMANCE_GOAL.md` (perf lineage), `SESSION_HANDOFF.md` (historical).

### History anchors (git, newest first)
`3fce652` miltick close-out (window 15 s exact, cadence 31 s ×2, 41/41,
Milan=1) · `c3b0e82` MILAN_CLK_FREQ_HZ never passed — plumbed ·
`165d57c` talker SM RTL · `ba76908` ADP dormancy self-re-arm + DIAG ·
PR #12 AECP/AEM merge (`f51a27b`).
