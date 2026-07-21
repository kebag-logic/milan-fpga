# Small handover — 2026-07-21 evening (final)

Full history: `HANDOVER.md` + `BENCH_TOPOLOGY.md` + `MILAN_COMPLIANCE_GAPS.md`.

## Consoles — MOVED to `/home/alex/bench-console/`
`console_daemon.py` + `arty_in`/`arty.log` + `ax_in`/`ax.log` (write a
line to `*_in`, read `*.log`; daemons setsid-nohup'd, survive sessions).
**TRAP: (re)opening the ARTY serial port RESETS the board** (DTR
toggle on the Digilent USB-serial) — a daemon restart = an ARTY
reboot = music bind lost. The AX port does not do this.

## Boards (both QSPI self-boot, milan CSR base 0x90000000)
- **ARTY** = `eto_milanfinal44` (+0.308, best ARTY margin ever):
  VERSION 0x0006 — link guard silicon-proven + the full audio round
  (wire-truth walker, prefill rails, LPF fix, 2ch-first ROM: rebind
  needs NO SET_STREAM_FORMAT anymore). Playing music, locked, verified
  after the final reboot.
- **ALINX** = `eppo_milanfinal30` (+0.026): VERSION 0x0005 — **no
  guard yet**: 9 draws missed across AX31/32 (best −0.038 = AX32
  eppo). Violator = `storage_32` = MAC tx_sf PacketFIFO ADDR[9]
  pointer cone.

## In flight / next
1. **AX33 (tx_sf=512 lever) + chained mf45 parity sweep** — driven by
   the session-independent script `~/litex-milan/work/chain_ax33_mf45.sh`
   (log: `chain_ax33_mf45.log` next to it). The lever deletes the
   ADDR[9] cone; from −0.038 it should close.
2. On an AX33 keeper (WNS ≥ 0): flash AX (`build.sh flash
   ax7101:<dir>` writes the bitstream slot, stops harmlessly at the
   images env-check) → power/JPROGRAM reconfig → drills: LINKG_STAT
   0x774 armed, LINK_CTRL[3] freeze drill, REAL bounce `ethtool -r
   eth0` (AX MDIO works) → CERT link-flap re-run.
3. On mf45 (parity): flash ARTY the same way, rebind music (one
   acmp_bind connect), re-run the 63-scenario CERT suite on the new
   pair. Extra-directive draws if needed: `sweep_extra.sh <board>
   <tag>` (exp/asm/enl).
3. On a keeper: `build.sh flash <board>:<dir>` writes the bitstream
   slot then STOPS at the images env-check — that is fine, images
   stay. Reconfigure: `openFPGALoader --ftdi-serial <ser> -c <cable>
   --fpga-part <part> --reset`.
4. AX drills after flash: LINKG_STAT 0x774 armed check, LINK_CTRL[3]
   freeze drill, real bounce via `ethtool -r eth0` (AX MDIO works),
   CERT link-flap scenarios, recovery-time note.
5. Re-bind music after any ARTY reflash (binds do NOT survive reboot):
   pw0 `sudo python3 ~/milanmusic/acmp_bind.py connect 6805CAFFFE95B2D1
   020000FFFE000002 --tuid 3 --luid 0 --dmac 91e0f0002a0d`. On mf44+
   the 2ch ROM default + wire-truth walker make `set_fmt.py`
   unnecessary; the +100 ppm streamer trim becomes unnecessary too
   (prefill rails). Streamer: `~/milanmusic/aaf_stream.py` (pw0,
   running).

## Today's commits (milan-fpga, NOT pushed; push needs --force, USER call)
`ad3dc9b` loop −73.4 disproof · `825b84c`+`1eaa6c9` link guard + 78/78
robustness · `c705091` wire-truth 1-to-1 mapping + prefill rails + LPF
leak + 2ch ROM · `00f7825`/`bc0691b` gaps · (pending) tx_sf 512 +
reorder + this file.

## Deprioritized (USER): es-1.1/1.2 BMCA variants → bottom of the list.

## Fresh traps (details in gaps §5b)
ProfiShark driver is kernel-pinned (reinstall per kernel) · pw0 /tmp
is volatile (tools now in `~/milanmusic/`) · ACMP commands need
distinct sequence_ids · sink-0 derives sid from {talker_mac, tuid}
(synthetic-talker recipe in acmp_bind.py) · pkill self-match via
neighboring args (bracket the pattern, isolate the kill command).
