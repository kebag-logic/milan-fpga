# Bench report: the 80 MHz split image on the board (#878)

Status: **BENCH PASS.** Every step was met. The board is left on the new image with the three stream connections up.
Date: 2026-11-24, 20:34-23:40 CET. Image: the qualified 80 MHz split image from milan-fpga `248d85c1` (PR #1004),
bitstream SHA-256 `1046292da1e73b2b595f65c66d9c429fb183a43e3466e160d95024651014735c`, layout `a096b761...`,
AEM image `019bced1...` (5,952 B), manifest VERSION `0x00030060`, mailbox 2.4.
Bench: the board is cabled directly to its link partner, with no tap in the path. The controller reads and binds
over AVDECC, and the reference peer is the bench talker and listener.

## Results

| Step | Result |
|---|---|
| 1. As found (read-only) | The previous split image (VERSION `0x00020060`): SYNC 1, asCapable 1 to the bench grandmaster, compensation 1409/100 (the default), PDELAY 0, BOOTSTS `0x1` and STAT `0x501079fc` clean. Three connections bound: peer AAF to board input 0, peer CRF to board input 1, board AAF to peer input 0. |
| 2. Flash | Done with the image's own persistent procedure (`deploy.sh flash-pair`, images first: the AEM slot, then the bitstream, each verified by read-back). rc 0 in 43 s. The first attempt was refused before any write because the installed image was not the one on record (finding 1). |
| 3. Boot and identity | The programmer's end-of-write reconfiguration booted the new image, with no power cycle and no other reset. One boot line and one ready line, no refusal line. ID `0x4d494c4e`, VERSION `0x00030060`, firmware "3.96.0". The firmware's own pre-ready checks accepted mailbox contract 2.4. The image declares a CPU clock of 80,000,000 Hz, and the 115200-baud console that the firmware derives from it works (a 100 MHz clock would be unreadable). PP_STAT `0x5b0050c4`: restore done, no failure, not closed, no alarm. BOOTSTS `0x1` (no fallback, no CRC error) and STAT `0x501079fc` clean. |
| 4. Link | 100BASE-TX full duplex: the image advertises only that mode and publishes link up only for a mode it shares with the partner (IEEE 802.1BA-2011 Table 6-1). AVB_INTERFACE LINK_UP 2 / LINK_DOWN 1 from boot, unchanged over 103 min of reads (21:56-23:39); the one down/up came before the first grandmaster acquisition (GPTP_GM_CHANGED 1), from the boot's negotiation restart. asCapable held at every 5-10 s poll. |
| 5. gPTP | 132 of 132 polls over 655 s: SYNC 1, asCapable 1, TU 0, one grandmaster and parent, path unchanged, PHC monotonic. Then 96 of 96 polls during step 7. At the default compensation PDELAY reads 0..9 ns, with 52 of 132 at 0: the published value floors a negative computed delay at 0, so the delay sits around zero. **Raw delay at 80 MHz, with a runtime compensation of 0/0 for 15 s: 755.1 ns** (sd 3.6, 748-762, 14 samples), against 752 ns measured earlier at 100 MHz. asCapable held. The default 1409/100 was then restored and read back. Two runtime writes in total, none left behind. |
| 6. Enumeration | 33 of 33 READ_DESCRIPTOR (IEEE 1722.1-2021 7.4.5) SUCCESS, covering every descriptor in the image's own AEM file. **32 are byte-identical** to the image's bodies. The ENTITY descriptor differs only in `available_index` (0 in the image, 827 read), which equals the ADP available_index the board advertised 6 s earlier: a run-time field (1722.1-2021 7.2.1, 6.2.2.8). |
| 7. Streams, concurrent | Board AAF talker to the peer, peer AAF talker to the board, and peer CRF to the board's CRF input, all at once for 1,046 s (17.4 min). Board TX 8,366,945 = peer RX 8,366,946 (7,999.9/s). Peer TX 8,366,916 = board timestamps valid 8,366,916. CRF 522,932 = 522,932 (500.0/s). On both listeners MEDIA_LOCKED 1 and **0** MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, TIMESTAMP_NOT_VALID, UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP. Talkers: one STREAM_START each, no STREAM_STOP. Clock domains steady. No Talker Failed. BOOTSTS/STAT clean before and after. |
| 8. Left | The board runs the new image with its default compensation and the three connections up. The console is left with hangup-on-close off. |

## Findings

1. **The installed image was not the one recorded for the board.** flash-pair refused correctly ("live QSPI bitstream
   matches neither supplied artifact"), before any write. A read-only dump showed that the flash held a later build of
   the same VERSION, `0x00020060` (a hardware build of 11-13). With that build named as installed, flash-pair proved
   it and wrote the new set. The dump is kept as an exact restore source. Each proof read reloads the running image
   from flash, so the old image booted twice before the write. Its compensation was the default, so nothing was lost.
2. **The board's AVDECC identity changed with the image, as decided in #840.** It is now entity `024b4cfffe4b4c02`,
   MAC `02:4b:4c:4b:4c:02` (previously `020000fffe000002`). Not a defect. The peer's listener binding to the old
   talker ID was replaced by one to the new ID.
3. **Candidate defect, not confirmed on the wire:** the board's stream inputs report MSRP_ACC_LAT_VALID with an
   accumulated latency of 0. Through the same bridge, the peer's listener of the board's stream reads 137,445 ns. A
   registered Talker Advertise carries the latency accumulated along its path (IEEE 802.1Q-2022 35.2.2.8.6). This
   needs an MSRP capture to confirm and its own issue. It does not affect streaming.
4. **Note:** the ENTITY serial_number reads "AX7101-0001" on this board. That is the value the shared AEM image pins
   for both boards; the per-board identity is the MAC and entity ID.
5. **Note:** the computed link delay at the default compensation sits at about +0.6 ns (755.1 - 754.5). Its noise
   takes it below zero part of the time, but never near the -80 ns where this gPTP engine (which predates the
   negative-delay clamp) would drop asCapable.

## Not covered

- No wire capture: there is no tap in the path, so frame counts come from both ends' counters, not from the wire.
- A cold power-on boot of the new flash content was not exercised, because the board has no remote power. The boot
  seen was the programmer's reconfiguration from the newly written flash.
- The link partner's own port status was not read.
