# Small handover — 2026-07-21 evening

Full history: `HANDOVER.md` + `BENCH_TOPOLOGY.md` + `MILAN_COMPLIANCE_GAPS.md`.

## Boards (both QSPI self-boot, milan CSR base 0x90000000)
- **ARTY** = `eppo_milanfinal43` (+0.102): link guard **silicon-proven**
  (freeze drill byte-exact, TX alive after auto-reinit), VERSION 0x0006.
  Playing music (see below).
- **ALINX** = `eppo_milanfinal30` (+0.026): VERSION 0x0005 — **no guard
  yet**: AX31 (6 draws) and AX32 asl/eto all MISS timing (best −0.142).
  Violator = `storage_32` = the MAC TX store-and-forward FIFO's
  ADDR[9] pointer cone + its fanout into ptp_ts_rx.

## In flight / next
1. AX32 eppo still routing; ARTY mf44 sweep chains after it (watcher
   `b1pvmgf39`). Expectation: miss.
2. **Lever armed**: `tx_sf` halved 1024→512 in milan_soc.py (deletes
   ADDR[9]; matches the original 4 KB sizing comment). If eppo misses:
   `sweep.sh ax7101 milanfinal33` + chain `sweep.sh arty milanfinal45`
   (RTL parity). Extra-directive draws: `sweep_extra.sh` (exp/asm/enl).
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
