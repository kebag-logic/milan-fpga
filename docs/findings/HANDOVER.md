# HANDOVER  -  topology rules + live states (2026-07-12)

*The operational one-pager for the two-board Milan lab: every standing rule
with its reason, and the exact state of boards, branches, builds and open
threads. Results archive: SESSION_HANDOFF.md. Deep docs: ../README.md.*

## 1. Topology

```
┌──────────────── dev VM ─────────────────────────────────────────┐
│ milan-fpga (RTL) · the-private-test-repo (driver/DT/boot) ·           │
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
   raw against direct-cable-era results. ADP-class sniffs: the advertise
   cadence is ~15-30 s (valid_time 62), so capture windows must be >=40 s  -
   an 8 s window "proved" the advertiser dead (2026-07-11 phantom). And the
   arty busybox rootfs has NO `timeout`: `timeout N tcpdump ... 2>/dev/null`
   dies instantly with the error swallowed, faking an empty capture.

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
14. OpenSBI is BOARD-SPECIFIC and EMBEDS a DTB (FW_FDT_PATH bypasses the
    flashed dtb slot!). Build per board via build_opensbi.sh env
    (OUT/TIMER_HZ/BOARD_TAG/NAX_HARTS/DTB; the banner names the board):
    AX7101 = opensbi.bin (100 MHz), Arty = opensbi_arty.bin (83333000,
    2 harts). The durable one-opensbi form (BIOS passes a1=dtb) is still
    open  -  thread 1.

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
- AX7101: **build_ax7101_eto_aecp7 in SRAM (NEW KEEPER, 2026-07-12)** = the
  full la_avdecc-clean AECP entity (STREAM_INFO 56 B, caps 0x8588, every-send
  available_index, GET_COUNTERS, GET_AS_PATH) + flattened-interface RTL.
  Sweep: eto +0.091 (keeper) / asl +0.048 / eppo -0.098 (FAILS, discard).
  IP .1 up, identity programmed + ADP enabled (EID 02:00:00:ff:fe:00:00:01),
  **controller 26/26 + la_avdecc IEEE17221=1 zero-AEM-complaints verified on
  BOTH asl and eto bits**. QSPI still holds the adp2-era image set
  (gateware-independent). Fallbacks: eppo_aecp6 (+0.176, no AS_PATH),
  eto_aecp2 (+0.186, r1-era), adp2 (+0.102, AECP-less).
  hsplit16 hsplit=2 hs_pgsz=16384 as before.
- Arty A7-100: build_arty_v7 in SRAM (flashboot gateware, WNS +0.018,
  sys 83.333/datapath 50, S25FL128S 1x 0x03 reads). QSPI holds
  opensbi_arty+dtb+kernel+rootfs (flashboot copies all four, CRC-clean).
  **Linux BOOTS from flash to login** (2026-07-11: opensbi_arty.bin = arty
  dtb embedded + 83333000 timer + 2 harts; the-private-test-repo 1bc7530). kl-eth
  auto-loads (hsplit16; defaults correct on this board: rsc_clk_mhz=50,
  hsplit off). IP re-addressed to .3 live  -  the shared rootfs still BAKES
  .1 (the AX7101's!) on every board; fix pending. **Two-node ADP discovery
  VERIFIED**: this board captures the AX7101's ENTITY_AVAILABLE
  (EID 02:00:00:ff:fe:00:00:01) through the AVB switch. Switch-path baseline
  (driver defaults): TX 83.3 / RX 93.9 Mbit. Cosmetic: "Initramfs unpacking
  failed: invalid magic" AFTER the real unpack succeeds (trailing junk in
  the fixed 16 MiB initrd window)  -  ignore it.

**Branches (all pushed)**
- main = f51a27b: the docs-overhaul merge + AREA-70 + ADP fixes + **PR #12
  (05_aecp_aem) merged by the user**  -  AECP/AEM is now in main.
- milan-arty-bringup = 1dfb7c2: the Arty port chain (flashboot, S25FL128S
  opcode, baud, flash tooling fixes), REBASED onto f51a27b, force-pushed;
  + arty DT board values/IR (sw/dts/boards/arty.json) + this doc update.
- milan-adp-fixes: the two isolated ADP RTL fixes (enable-after-boot,
  src-MAC byte order) on the ship-cleared base.
- milan-avdecc-fpga: the main working line (pre-rebase state; main carries
  everything that matters from it).
- the-private-test-repo repo: milan-avb-stabilizing-milan = 1bc7530 (per-board
  opensbi: OUT/TIMER_HZ/BOARD_TAG + opensbi_arty.bin + boot_arty.json).
- fpga-ps-tools repo: main is AHEAD-5 UNPUSHED (user's call)  -  includes
  395238c: bsp/boards/digilent-arty package + vexii/fw_jump platform
  refresh; the BSP dt target now takes BOARD=digilent-arty (verified
  against build_arty_v7 csr.json; its extract also showed the hand dts
  carries a stale dma-ts window 0x3064 vs the gateware's 0x3100  -
  regenerate when PTP-on-arty matters).

**Builds worth keeping**
| Build | What | Numbers |
|---|---|---|
| build_ax7101_eto_aecp7 | THE AX7101 keeper (la_avdecc-clean AECP) | WNS +0.091 (asl +0.048 backup; eppo -0.098 FAILS) |
| build_ax7101_adp2 | AECP-less fallback (area+ADP) | WNS +0.102, 70.1 pct LUTs, BRAM 83.3 pct |
| build_arty_v7 | THE Arty keeper (flashboot) | WNS +0.018 |
| build_1hart_epo | 1-hart decision datapoint | 58 pct LUTs / 68.5 pct BRAM / 80.9 pct slices |

## 4. Open threads (ranked, with the evidence)

1. **RESOLVED 2026-07-11 (was: Arty Linux panic).** Executed: build_opensbi.sh
   now takes OUT/TIMER_HZ/BOARD_TAG (+ the existing NAX_HARTS/DTB) and the
   banner names the board; opensbi_arty.bin (2 harts, 83333000, arty dtb)
   built + flashed via the flash verb; boot_arty.json points at it
   (the-private-test-repo 1bc7530). Arty boots to login; §3 has the live state.
   STILL OPEN (durable form): drop FW_FDT_PATH and honor a1 so ONE opensbi
   serves both boards with per-board flashed dtbs  -  the BIOS jumps a1=0
   today (patch linux_flashboot to pass MILAN_FLASHBOOT_DTB_ADDR) and
   platform.c would read timebase from the FDT. Piggyback on the next
   gateware spins. Also pending: per-board IP in the shared rootfs (bakes
   192.168.127.1 everywhere  -  the Arty must re-address to .3 by hand).
2. **AECP/AEM Milan v1.2 entity DONE — la_avdecc (Hive) validated on silicon.**
   (2026-07-12.) The KL_aecp_* library is a WORKING listener: 5-descriptor
   Milan entity, READ_DESCRIPTOR + getters/setters, **LOCK 60 s /
   ACQUIRE=NOT_SUPPORTED**, GET_STREAM_INFO (Milan fixed 56 B), GET_COUNTERS
   (full 136 B on EVERY status), GET_AS_PATH (count=1, MAC-EUI64 clock id),
   MVU GET_MILAN_INFO (version 1, cert 0). Architecture documented in
   hdl/aecp/doc/atdecc_architecture.drawio — MULTI-PAGE, overview + one
   bit-level page per block (byte maps, FSMs, segment programs, address maps).
   **The la_avdecc campaign (the real validator; found what nothing else did):**
   - r1: GET_STREAM_INFO 44 B -> Milan fixed 56 B; caps 0x8588 (dropped
     IDENTIFY_CONTROL_INDEX_VALID: advertised with no CONTROL descriptor).
   - r2: available_index must +1 on EVERY ADPDU (bump-on-change-only reads as
     'incoherently changed' -> offline/online cycling; pipewire ref bumps every
     send); GET_COUNTERS is Milan-mandatory AND must be full-size on errors.
   - r3: GET_AS_PATH is Milan-mandatory (the last 5.4.4 item for this model).
   - PROBE TRAP: link enum-probe with la_avdecc's OWN feature defines
     (CBR/JSON/REDUNDANCY/STRICT_2018 + nlohmann include) or the vtable
     mismatches and it segfaults on the first virtual call.
   - CDL truth: CDL = frame_len - 26 (12 + payload). tsn-gen's CDL model
     counts target_eid (frame-18) and is WRONG — never use it as the oracle.
   Verification ladder: tb aecp 68/68, adp 121/121, milan_dp 17/17, cosim
   (tsn-gen<->RTL) 42/42, lint 10/10, **Yosys 19/19 incl. KL_aecp_top (33.6K
   cells) + full milan_datapath** (needed: flatten internal AXIS interface
   links — sv2v v0.0.13 renders interface members of non-top modules as
   top-absolute hierarchical paths; also ifndef-SYNTHESIS the parser $error).
   Silicon verdicts: aecp6 (eppo +0.176) cleared the r2 items (controller
   24/24). **aecp7 (eto +0.091 keeper; asl +0.048 also validated): 26/26 incl.
   AS_PATH on the wire; la_avdecc = entity ONLINE, fully enumerated,
   IEEE17221=1, MISBEHAVING=0, ZERO AECP/AEM complaints — every Milan 5.4.4
   mandatory item answered.** The one residual Milan complaint moved to a
   DIFFERENT protocol: 'Milan 1.3 - 5.5 ACMP GET_TX_STATE' — we have no ACMP
   engine; that is the next increment (a stateless talker responder:
   subtype 0xFC, GET_TX_STATE/GET_TX_CONNECTION RESPONSE with
   connection_count=0 would satisfy it while connections stay out of scope).
   RUNBOOK: JTAG-load the aecp7 best-WNS bit -> board: dmesg -n 1; eth0 up
   .1; avdecc/aecp_csr_setup.sh devmem sequence (caps 0x8588) -> peer:
   `sudo python3 /tmp/milan_controller.py enp6s0` (expect 26/26) and
   `sudo ~/la_avdecc_work/enum-probe enp6s0 40` (expect IEEE17221=1 and
   exactly one complaint: ACMP GET_TX_STATE timeouts; Milan=1 once the ACMP
   responder ships). Deferred: ACMP responder (the Milan=1 gate), NV
   persistence of SET_*, unsolicited push, HW counter values, audio maps.
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
