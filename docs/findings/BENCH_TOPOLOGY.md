# BENCH TOPOLOGY & WHERE-IS-WHAT — the context-reset handover

Written 2026-07-20 (post history-rewrite). This is the single document a
fresh session needs to operate the bench. Live campaign state lives in
`HANDOVER.md` (same directory); the remaining compliance work is
`docs/MILAN_COMPLIANCE_GAPS.md`. Naming rule: the conformance suite is
called **CERT** everywhere (commits, docs, comments) — never any other
name; its material is private (see §7).

## 1. Machines

| Name | Reach | Role |
|---|---|---|
| dev box (this host) | local | Vivado 2026.1 (`/home/alex/Xilinx`, 96 cores), repos, JTAG cables, board serial consoles. NEVER gets a 192.168.127.x address. |
| amx-pw0 | `ssh amx-pw0` | Test controller on the AVB LAN: `enp6s0` = 68:05:ca:95:b2:d1 = 192.168.127.2. All wire probes run here (needs sudo for raw sockets + PACKET_MR_PROMISC — raw AVDECC tools MUST join promisc or responses are NIC-dropped). |
| amx-ubuntu-server | `ssh amx-ubuntu-server` | ProfiShark capture host. `enxe8eb1b37e2c0` = tap1 **inline on the ALINX↔switch link**; `enxe8eb1b39111a` = tap2 **inline on the ARTY↔switch link**. Records carry a **28-byte header**: all tcpdump `ether[]` offsets shift +28 (ethertype at `ether[40:2]`, SMAC at `ether[34:4]`); FCS included. |
| amx-pi | `ssh amx-pi` | Power strip: `powerstrip off/on 4` = **the AVB switch**; OUT0 = AX7101 power. |
| amx-pw1 | — | **NEVER TOUCH** (standing rule). |
| AVB switch | 192.168.127.1 (ssh open, **user holds credentials**) | AVB-certified bridge. clockIdentity `3cc0c6.fffe.fe0210`, port MAC toward AX `3c:c0:c6:fe:02:17`. Claims gPTP priority1=246/cc248/acc0x20 (tap-read) — why boards run priority1=238 (USER default; cert posture 246\|248). MSRP Domain = class A, prio 3, **VID 2**. |

## 2. Boards (DUTs)

| | ARTY (small endstation) | ALINX AX7101 (full endstation) |
|---|---|---|
| Entity/board name | "ARTY", entity :02 | "ALINX", entity :01 |
| MAC / entity_id | 02:00:00:00:00:02 / 020000fffe000002 | 02:00:00:00:00:01 / 020000fffe000001 |
| IP (eth0) | 192.168.127.3 | on the same /24 (read via console `ip -br addr`) |
| JTAG/flash | `--ftdi-serial 210319AFEED0 -c digilent`, part xc7a100tcsg324 | `--ftdi-serial 210512180081 -c ft232`, part xc7a100tfgg484 |
| QSPI policy | **boot**: bitstream@0 + image set (16 MB) | **images only** — a bitstream write is the KNOWN KERNEL-CLOBBER TRAP. Gateware is JTAG-SRAM, reload after every flash-images (flashing loads a JTAG SPI proxy). |
| Datapath clock | 50 MHz | 100 MHz (timing-critical; the serial-MAC LPF exists because a combinational biquad fails here) |
| gPTP role | SLAVE (priority1 248 base cfg) | **GM** (S50 sed-REPLACEs priority1 → 238) |
| Serial console | `/dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0` | `/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce96...-if00-port0` |
| ssh | dropbear, root, no password — `ssh root@192.168.127.3` **from pw0** (large-file path; console base64 fails) | same (find IP first) |

Audio loop: ALINX tone (S50 enables TONE_CTRL) → AAF → ARTY DAC (Pmod
I2S2 HP out, through the render LPF) → analog cable → ARTY ADC (line in)
→ ARTY talker stream → wire. Loop THD+N record −73.4 dB (LPF on).

## 3. Consoles from the dev box

A tiny daemon per board bridges serial↔FIFO+log (session-scratchpad
based — after a context reset, RECREATE it):

```sh
S=<scratchpad>           # this session's scratchpad dir
# console_daemon.py (see below) + per board:
~/litex-milan/venv/bin/python3 $S/console_daemon.py <serial-by-id-path> $S/arty_in $S/arty.log &
mkfifo $S/arty_in first; same for ax. Then:
$S/con.sh arty '<shell cmd>' <wait-secs>     # types cmd, returns new log tail
printf 'root\n' > $S/arty_in                  # login (user root, no password)
```

`console_daemon.py`: opens the port at 115200, thread appends all RX to
the log, main loop forwards FIFO lines to TX. `con.sh`: record log size,
write cmd to FIFO, sleep, print the log delta. Traps: output races the
window (retry with bigger wait); `dmesg -n 1` unburies the console; a
foreground pipe wedges the shell (write ctrl-C to the FIFO).

## 4. Repositories & artifacts

| Path | What |
|---|---|
| `~/prjs-avb-on-fpga/milan-fpga` | THE gateware repo. `hdl/` RTL (aecp, acmp, adp, lwsrp, maap, avtp, 1722, csr, common, 802_1q_traffic_shaper, ptp_timestamp), `tb/verilator/*` (aecp 474, milan_dp 105, pcmlpf 7, + suites), `syn/yosys/run.sh` (28 tops, device-portability gate), `sw/litex/` (milan_soc.py, **sweep.sh**, **build.sh** incl. the `flash` verb, deploy.sh), `avdecc/` (AEM JSON models + `gen_aem_store.py` → `hdl/aecp/gen/aecp_aem_rom.svh` + `milan_controller.py`), `docs/`. Author `hackerman-kl`, ONE-LINE commits, no trailers. |
| `~/milan-tests-avb` | Bench/test repo. `fpga/` (kl-eth driver, buildroot br2-external incl. the **rootfs overlay** = S50milan, linkmon.sh, gptp2csr.sh, stream_phc_sync.sh, gptp.cfg, S65/S66), `fpga/tests/` (tone_thdn.py, pcm_ring_dump.c, silicon_battery.py), `fpga/dts+boot/` (dtb + opensbi per board), `private/` (**untracked, git-ignored**: the CERT suite + official run — see §7). Commits: `-c user.name="Alexandre Malki" -c user.email="alexandremalki89@gmail.com"`, one line. |
| `~/litex-milan` | LiteX + venv (`~/litex-milan/venv` — PATH needed for build/flash python). **`work/`** = all Vivado build dirs (`build_<board>_<seed>_<tag>/`). |
| `~/br-milan-output` | Buildroot out-tree. Rebuild rootfs: `cd ~/br-milan-output && make O=$PWD && xz -9 --check=crc32 -c images/rootfs.cpio > /tmp/scratch/rootfs.cpio.xz`. Kernel `images/Image` (xz it for flashing). |
| `~/repo-backups-0720` | Pre-history-rewrite bundles + the private-material tar. KEEP PRIVATE. |
| `/home/alex/standards/` | All specs: 1722.1-2021.pdf, 1722-2016, Milan v1.2 consolidated, 802.1AS/Q, the official validation test plan, etc. Extracted text: `/tmp/scratch/1722.txt`, `milan12.txt`, `certplan.txt` (re-extract with pdftotext after reboot). |
| `~/refs/AX7101` | Board reference repo (schematic, flash + PHY datasheets). Read-only. |

**Both repos DIVERGE from their GitHub origins** (2026-07-20 history
rewrite). Push ONLY when the user asks — needs `--force`.

## 5. Build → flash → verify pipeline

```sh
# 3-seed Vivado sweep (3 parallel instances × 32 threads = the box rule)
cd ~/prjs-avb-on-fpga/milan-fpga && ./sw/litex/sweep.sh <arty|ax7101> <tag>
# WNS: grep -B2 -A6 "Design Timing Summary" ~/litex-milan/work/build_*_<tag>/gateware/*_timing.rpt
# Gate: WNS >= 0. Pick best seed.

# ARTY (QSPI boot: bitstream + images):
PATH="$HOME/litex-milan/venv/bin:$PATH" PYTHON="$HOME/litex-milan/venv/bin/python3" \
KERNEL=/tmp/scratch/Image.xz ROOTFS=/tmp/scratch/rootfs.cpio.xz \
OPENSBI=~/milan-tests-avb/fpga/boot/opensbi_arty.bin \
DTB=~/milan-tests-avb/fpga/boot/milan_arty_vexii.dtb \
./sw/litex/build.sh flash arty:build_arty_<seed>_<tag>
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent --reset   # then ~100 s boot

# AX (images to QSPI, gateware to SRAM via JTAG — NEVER bitstream to QSPI):
KERNEL=... ROOTFS=... OPENSBI=~/milan-tests-avb/fpga/boot/opensbi.bin \
DTB=~/milan-tests-avb/fpga/dts/milan_ax7101_linux.dtb \
./sw/litex/build.sh flash ax7101:build_ax7101_<seed>_<tag>
openFPGALoader --ftdi-serial 210512180081 -c ft232 --fpga-part xc7a100tfgg484 \
  ~/litex-milan/work/build_ax7101_<seed>_<tag>/gateware/alinx_ax7101.bit
```

Known chronic non-error: arty builds print a `write_cfgmem SPI_BUSWIDTH`
failure after the .bit — harmless, our flow flashes the .bit directly.

Regression before any commit: aecp + milan_dp + pcmlpf TBs green,
`./syn/yosys/run.sh` = `RESULT: PASS` (check it REALLY passed — a piped
tail can eat the exit code).

## 6. pw0 wire tooling (all `sudo`, iface `enp6s0`)

| Tool | Purpose |
|---|---|
| `/tmp/milan_controller.py` | Entity(iface) with discover (cdl=56!), read_descriptor, `_aecp`, ACMP helpers. The repo master: `milan-fpga/avdecc/milan_controller.py`. |
| `/tmp/dyninfo_probe.py <01\|02>` | GET_DYNAMIC_INFO (7.4.76) batch vs classic responses, byte-exact + BAD_ARGUMENTS case. Expect PASS on ≥ mf38/AX23 silicon (mf37 had the BSCAN race). |
| `/tmp/crf_inject.py [n]` | 500 Hz Milan CRF source (subtype4/type1/48k/ival96), sid `6805ca95b2d10001`, synthetic exact-2ms timestamps (CRF_RATE reads ≈0). Provision the DUT: CRF_SIDLO/HI + CTRL en, watch 0x744-0x74C + lock. |
| `/tmp/ctr.py` | STREAM_INPUT counters snapshot (LOCKED/UNLOCKED/RESET/UNCERT) — the media-health detector. |
| runner scripts → see §7 | conformance suite runners. |
| capture | `tcpdump -i enp6s0 ether proto 0x22f0` (AVTP/AVDECC). AECP is unicast; ADP/ACMP multicast 91:E0:F0:01:00:00; MAAP 91:E0:F0:00:FF:00. |

THD+N: capture the stream at a tap (`pcap2s32.py` in /tmp/scratch
strips ProfiShark+VLAN, extracts S32BE), or `pcm_ring_dump --ring
0x4ff00000 --bytes N` on the ARTY (ring only in the ARTY DT! `--secs`
segfaults) → scp via pw0 → `tone_thdn.py --chans 2 --f0 1000`.

## 7. The CERT suite (PRIVATE — never in git, never pushed)

- `~/milan-tests-avb/private/recreate` = the behave conformance-recreation
  suite (features es-2.1…es-4.13, hive-counters, link-flap; steps, pdu
  lib, tools-la-avdecc probe). `private/official-run` = the official run
  results. `/private/` is git-ignored; **never `git add` it**; the word
  for it in any committed text is **CERT**.
- Runners live on pw0 under the suite's legacy-named home directory +
  venv, driven by two /tmp run scripts (DUT :02 = the plain one, DUT :01
  = the -alinx one) — pw0-local paths, not in any repo; the EXACT paths
  are in the session memory index (private), or `ls ~pw0` + `/tmp/run*`. Link-flap helpers:
  `~/bin/arty-linkflap.sh`, `~/bin/ax-linkflap.sh` (phy_crg_reset
  0xf0003800 via console). la_avdecc lib+probe: `~/la_avdecc-{src,build,probe}`
  (counters-probe expects ENTITY GET_COUNTERS = SUCCESS+empty).
- Score to beat: **43/43 scenarios per board** (last full pass on
  asl_mf35 + eppo_AX21).

## 8. Board runtime (what runs where)

Boot: QSPI/SRAM gateware → BIOS flash-boot (xz kernel) → buildroot →
`S50milan` provisions CSRs (names, model id, vt=10, MAAP adopt, kernel
shield /32, **AAF_CTRL 0x654 = 0x00020003 — bit-preserve VID 2 [27:16]
or the switch floods the stream as best-effort**, honest counts
0x618/0x61C, ingressLatency sed 3511(ARTY)/1490(AX) ns, priority1 238 on
AX, tone on AX) → daemons: `ptp4l` (tx_timestamp_timeout **500**),
`phc2sys`, `linkmon.sh` (kernel rx_packets liveness, one edge-pair per
outage, up-after-settle, LINK_CTRL 0x71C reinit, RST_EPOCH 0x720
canary), `gptp2csr.sh` (GM 0x624/8 — publishes LOCAL ckid when we are
GM; pdelay 0x6E4; AS_PATH parent bridge 0x730/4 from PARENT_DATA_SET),
`stream_phc_sync.sh` (dormant while ptp4l is SLAVE **or MASTER**; only
steers after 5 consecutive dead polls — earlier versions caused the
~100 s media-unlock cycle).

CSR quick map (base 0x90000000, addresses = offsets): 0x600 ADP ctrl ·
0x60C/0x610 model id · 0x618/0x61C caps+counts · 0x624/0x628 GM ·
0x654 AAF_CTRL {vid[27:16],bypass,en} · 0x680 lwSRP · 0x6A4 ACMP-L state
· 0x6B8/0x6BC/0x6C0 RX monitor stat/frames/err · 0x6C4/0x6C8 PCM ring ·
0x6CC-0x6D4 MAAP · 0x6D8 drift rails · 0x6DC TONE · 0x6E4 pdelay ·
0x6EC ts_delta · 0x71C LINK_CTRL · 0x720 RST_EPOCH · 0x724/0x728
ENT_NAME · 0x72C LPF_CTRL (default 1) · 0x730/0x734 AS_PATH parent ·
0x738-0x74C CRF {ctrl+locked@31, sid lo/hi, delta, rate, status}.
New plain-RW CSRs MUST be added to `is_plain_rw()` in milan_csr.sv or
reads lie (shadow).

## 9. State at handover (2026-07-21 morning - campaign closed; log = HANDOVER.md)

- **ARTY QSPI = `eppo_milanfinal41` (+0.078) + rootfs #8**: 0x4B
  byte-exact PASS, CERT 63/63, sink-1 chain proven, CRF rx proven.
  `mf42` (format-family parity, e3391d9) is the one pending ARTY spin -
  flash it when built, re-check dyninfo + READ_DESCRIPTOR formats.
- **ALINX QSPI-BOOT = `eppo_milanfinal30` (+0.026) + rootfs #8** (first
  closing AX after 7 rounds; L2 32K, sweep always 1-hart): 0x4B PASS,
  CERT 63/63, CRF talker LIVE (500.3 PDU/s, DMAC = MAAP claim+1),
  **CRF e2e locked at the ARTY, RATE +6.7 ppm**. JTAG-loaded + QSPI
  written; the --reset self-config test tells whether the mode pins
  boot it standalone.
- The CERT suite = 63 scenarios (private/recreate snapshot
  aets_recreate_20260721); tap helpers gptp_cadence.py + srp_domain.py
  on amx-ubuntu-server; es-4.5 self-quiesces (poll, no fixed sleeps).
- Open for the day shift: analog loop leg (physical; both digital ends
  -135.1 dB), switch gPTP claim for the es-1.1/1.2 BMCA variants,
  gaps-doc deferred list (MMCM-DRP servo actuator, 2nd lwSRP attr,
  GMII CDC reinit, 8ch render, class-B, shadow invalidate,
  pcm_ring_dump segv, kl-eth tx-stamp latency).
- Bench-tooling fragilities learned tonight: arty-linkflap.sh drives
  the SESSION console (a login race eats the flap - verify SHELL-OK
  before cert runs); background flashes need ABSOLUTE paths; `timeout
  N sudo tcpdump` leaves the root child alive; tagged-stream tap
  filters = ether[44:2].

## 10. Standing rules (violating any of these has burned us)

1. amx-pw1 untouchable; dev box never on 192.168.127.x.
2. AX QSPI never receives a bitstream; always JTAG-reload the AX after
   flash-images; every openFPGALoader call carries the right
   `--ftdi-serial`.
3. Commits: one line, no trailers; milan-fpga = hackerman-kl,
   milan-tests-avb = the Alexandre Malki identity. Push only on request
   (and remember: force-push after the rewrite).
4. Max 3 parallel Vivado; WNS ≥ 0 or it doesn't ship. Kill builds by
   output-dir match (killing python parents leaves vivado children).
5. New HDL is SystemVerilog in the house style; CBS shaper is never
   removed; measure-don't-assume (HW counter before any conclusion).
6. CERT naming + `/private/` rules of §7. The word starting with A that
   the suite used to be called must not appear in commits.
7. The 0x654 write preserves VID 2; new RW CSRs go into is_plain_rw;
   validate wire frames by LENGTH, not just header fields.
