# HANDOVER  -  topology rules + live states (2026-07-11 night)

*The operational one-pager for the two-board Milan lab: every standing rule
with its reason, and the exact state of boards, branches, builds and open
threads. Results archive: SESSION_HANDOFF.md. Deep docs: ../README.md.*

## 1. Topology

```
┌──────────────── dev VM ─────────────────────────────────────────┐
│ milan-fpga (RTL) · milan-tests-avb (driver/DT/boot) ·           │
│ litex-milan/work (builds) · br-milan-output (buildroot)         │
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
│ Milan node 1 │   │ Milan node 2 │
│ 192.168.127.1│   │ .3 (planned) │
│ 1G GMII      │   │ 100M MII     │
└──────┬───────┘   └──────┬───────┘
       │ 1G               │ 100M
     ┌─▼──────────────────▼─┐
     │      AVB SWITCH      │  gPTP/SRP-capable bridge
     └──────────┬───────────┘
                │ 1G
        ┌───────▼──────┐
        │ amx-pw0 i210 │  192.168.127.2  (ssh, passwordless sudo)
        │ 68:05:ca:95: │
        │       b2:d1  │
        └──────────────┘
```

## 2. The rules (each one was paid for)

**USB / cables**
1. Select serial consoles by `/dev/serial/by-id/`, never ttyUSBn (numbers
   renumber on every replug; three adapters share the bus).
2. Every openFPGALoader call carries `--ftdi-serial <serial>` (two FTDI
   cables: a flash op on the wrong board is destructive).
3. VM USB passthrough rules are address-pinned on the host: a replug breaks
   the rule silently (three separate drop incidents 2026-07-11). Re-add by
   vendor:product (0403:6014, 0403:6010, 10c4:ea60) to end the class.

**Network / measurement**
4. `amx-pw1` is RESERVED. Never touch it.
5. The VM never gets a 192.168.127.x address (data plane is boards+peer only).
6. Ghost-peer check before trusting any number: on the board,
   `ip neigh | grep 127.2` must show `68:05:ca:95:b2:d1`.
7. A gate number is only valid with its FULL cell recipe. Compare A/B
   IN-SESSION on the same cell; never against a scoreboard number from a
   different era (the cbsf_epo "TX regression" was a phantom baseline).
8. Cells: peer byte-counter 5 s deltas, first+last interval excluded, fresh
   client ports per cell, `dmesg -n 1` on the board, TX gate after every RX
   change. Numbers now traverse the AVB switch: re-baseline, do not compare
   raw against direct-cable-era results.

**Pairing (LETHAL class)**
9. Driver `hs_pgsz` MUST equal gateware `--hs-page-bytes`: mismatch = DMA
   overrun = kernel panic. Hardened: capability CSR @0xf000311c + hsplit16
   probe-check refuses with -EINVAL, but the rule stands for older pairs.
10. Ship gateware folds the legacy byte-ring (`legacy_ring=False` default):
    `bd=0` drivers park with counted drops (never DMA to address 0);
    `--legacy-ring` builds restore the A/B path.
11. Arty driver line uses `rsc_clk_mhz=50` (datapath domain is 50 MHz there;
    the AX7101 is 100).

**Flash policies (16 MB QSPI each, board_facts in sw/litex/build.sh)**
12. AX7101: flash = LINUX IMAGES, kernel at offset 0. NEVER
    `openFPGALoader -f` a bitstream at it (clobbers the kernel  -  the
    historical trap; deploy.sh refuses without FORCE_BITSTREAM_FLASH=1).
    Gateware is JTAG-SRAM; power-cycle blanks the FPGA.
13. Arty: SAME images model since the flashboot port (kernel at 0 displaced
    the bitstream  -  16 MB cannot hold both). Gateware JTAG-SRAM. The flash
    verb: `KERNEL=.. ROOTFS=.. DTB=.. OPENSBI=.. PYTHON=<venv> build.sh
    flash arty` (FBI wrap + budget checks + verify, offsets from the build's
    flashboot_layout.json).
14. OpenSBI is PLATFORM-SPECIFIC and EMBEDS a DTB (FW_FDT_PATH overrides the
    flashed dtb slot!)  -  see open thread 1 before touching boot images.

**Builds (sw/litex/build.sh; docs/integration/BUILDING.md)**
15. 32 Vivado threads per build (hard cap), max 3 parallel (96-core box),
    launches staggered 90 s (pythondata index.lock race), always setsid
    (a harness task-kill once reaped 4 live builds).
16. Important configs build as the 3-directive place sweep; keep best WNS.
    Gate: WNS >= 0 (AX7101 keeps margin; QSPI corrupted below +0.03 at
    112.5 MHz). Arty die is -1: sys 83.333 + datapath 50 is the closing
    clocking (100/100 = -1.0 WNS, measured).
17. Elaborate WITHOUT --build before burning P&R (RUNNING_TESTS layer 1);
    OOC-synth a module before believing its hierarchical utilization line.

**Repo**
18. Commits: ONE short line, no attribution trailers, both repos.
19. Workstreams stay on separate branches; main receives merges. Never track
    graphify-out/.gitprep (hook artifacts, gitignored).
20. The CBS traffic shaper is never REMOVED from a build (user rule);
    bit-identical internal optimization is allowed (the slope engine).

## 3. Live states

**Boards**
- AX7101: build_ax7101_adp2 in SRAM (cbsf_epo AREA-70 keeper + both ADP
  fixes, WNS +0.102), hsplit16 hsplit=2 hs_pgsz=16384, IP .1 up, ADP
  ENABLED and advertising (EID 02:00:00:ff:fe:00:00:01)  -  ENTITY_AVAILABLE
  verified at the peer through the switch. QSPI holds the AX7101 image set.
- Arty A7-100: build_arty_v7 in SRAM (flashboot gateware, WNS +0.018,
  sys 83.333/datapath 50, S25FL128S 1x 0x03 reads). QSPI holds
  opensbi+dtb+kernel+rootfs (flashboot copies all four, CRC-clean).
  **Linux PANICS at 0.000000  -  root-caused, see open thread 1.** BIOS +
  DDR3 memtest + ID=MILN all pass (milestone 1 done).

**Branches (all pushed)**
- main = f51a27b: the docs-overhaul merge + AREA-70 + ADP fixes + **PR #12
  (05_aecp_aem) merged by the user**  -  AECP/AEM is now in main.
- milan-arty-bringup = 9a05de2: the Arty port chain (flashboot, S25FL128S
  opcode, baud, flash tooling fixes), REBASED onto f51a27b, force-pushed.
- milan-adp-fixes: the two isolated ADP RTL fixes (enable-after-boot,
  src-MAC byte order) on the ship-cleared base.
- milan-avdecc-fpga: the main working line (pre-rebase state; main carries
  everything that matters from it).
- milan-tests-avb repo: Arty DT/boot artifacts (7938c83), doc-path fix.

**Builds worth keeping**
| Build | What | Numbers |
|---|---|---|
| build_ax7101_adp2 | THE AX7101 keeper (area+ADP) | WNS +0.102, 70.1 pct LUTs, BRAM 83.3 pct |
| build_arty_v7 | THE Arty keeper (flashboot) | WNS +0.018 |
| build_1hart_epo | 1-hart decision datapoint | 58 pct LUTs / 68.5 pct BRAM / 80.9 pct slices |

## 4. Open threads (ranked, with the evidence)

1. **Arty Linux panic  -  ROOT-CAUSED, fix recipe ready.** The kernel dies at
   0.000000 (store access fault, badaddr 0xffffffc4febfe000) because
   **opensbi.bin embeds the AX7101 DTB** (custom litex_nax platform,
   FW_FDT_PATH in fpga/boot/build_opensbi.sh; OpenSBI banner says
   "Milan LiteX NaxRiscv @ 100000000Hz", kernel says "Hardware name:
   alinx_ax7101")  -  the 512 MB memory node makes early init write page
   structs beyond the Arty's 256 MB. The flashed dtb slot is bypassed.
   FIX: build an Arty OpenSBI  -  `OPENSBI_SRC=<tree> CROSS=<prefix>
   NAX_HARTS=2 DTB=fpga/dts/milan_arty_vexii.dtb build_opensbi.sh` AND
   parameterize the timer freq in fpga/opensbi/litex_nax/platform.c
   (100 MHz baked; Arty needs 83333000). Flash the new opensbi slot
   (offset 0x880000) + keep the arty dtb slot. Consider the durable form:
   drop FW_FDT_PATH and honor a1 so ONE opensbi serves both boards with
   per-board flashed dtbs (the BIOS jumps a1=0 today  -  needs the BIOS
   flashboot patch to pass the dtb address instead).
2. **Two-node ADP discovery** (after 1): Arty Linux -> kl-eth
   (rsc_clk_mhz=50) -> IP .3 -> tcpdump 91:e0:f0:01:00:00 on the Arty =
   the AX7101's advertisements through the bridge. Then AECP (now in main
   via PR #12) per reference/MILAN_V12_DEPENDENCY_MATRIX.md.
3. **Slices <70 pct**: the 1-hart user decision (numbers in the table
   above; retires the 2-hart NAPI pipeline that holds RX 381/374).
4. **Perf follow-ups** (both gatewares, env/driver-config class): the ~220
   cell-recipe gap vs the 525-era scoreboard + the recurring TX mid-flow
   stall (~20-30 s dead air; sweep napi_w/hsplit/rsc on the keeper).
5. AF_XDP ZC driver = the remaining RX>500 lane (campaign-scale).
6. Arty polish: is_1g=0 driver wiring (CBS 100M slopes), WNS margin
   (+0.018 is thin  -  sweep directives when it matters), S25FL128S image
   staging is JTAG-slow (~4 min full set  -  fine at this cadence).

## 5. Connect quickrefs

```sh
# AX7101 console            (tmux milan_qspi_boot)
tmux new-session -d -s milan_qspi_boot \
  "/home/alex/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0 --speed 115200"
# Arty console               (tmux arty_console)
tmux new-session -d -s arty_console \
  "/home/alex/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0 --speed 115200"
# JTAG loads (SRAM)
openFPGALoader --ftdi-serial 210512180081 -c ft232    <ax7101 bit>
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <arty bit>
# scripted console exec: scratchpad conx.sh '<cmd>' <timeout>  (AX7101 session)
# builds: sw/litex/build.sh {ax7101|arty} [--sweep] ; flash: build.sh flash <cfg>
```
