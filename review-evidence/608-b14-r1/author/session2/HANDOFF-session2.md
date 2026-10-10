# [A578] B14 bench handoff

Refs #608 #645 #647 #667 #682 #686 #691

- Base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee` (dev, the flashed image, seed eppo).
- Branch: `608-b14-bench`, clean, no commit (head = base). Findings docs only; none written yet.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6085135051
- TAKEN (session 1, not posted again): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6087724820
- Session 1 STOP (controller host down): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6088157558. Session 1's files are under `session1/`.
- Session 2 (resume) started 2026-10-10T04:46Z, after the controller host returned (booted 04:45 UTC).
- Session 2 STOP: see the end of this file (STOP.md, STOP.readback.md, stop-url.txt).

## Status

**STOP after item 1.** The identity gate passed. Then the SoC board's serial console answered one carriage return with a login prompt. The owner's bench rule for that console is: "If it shows a login prompt, STOP: the manager logs in (never type or store a credential)." Nothing was typed after the carriage return. No bench state changed.

## Items

| Item | Planned | Completed | Result | Evidence |
|---|---:|---:|---|---|
| 1 Identity | 1 | 1 | PASS | identity/identity.json |
| 2 INTERNAL to AAF | 10 | 0 | NOT RUN (STOP) | - |
| 2 AAF to CRF | 10 | 0 | NOT RUN (STOP) | - |
| 3 DUT-talker disconnects | 100 | 0 | NOT RUN (STOP) | - |
| 4 Talker starts | 100 | 0 | NOT RUN (STOP) | - |
| 5 Default maps and soak | 120 min | 0 | NOT RUN (STOP) | - |
| 6 Ethernet receive sanity | soak | 0 | NOT RUN (STOP); decision needed, see below | - |
| 7 MAAP interoperation | 1 | 0 | NOT RUN (STOP); decision needed, see below | - |
| 8 Restore | all | - | Nothing changed, nothing to restore | - |

## Cycle ledger (one row per locked action or check, UTC, 2026-10-10)

| Cycle | UTC | Item | Observation | Result | Evidence |
|---|---|---|---|---|---|
| s2-host-001 | 04:46:55 | - | Controller host up 1 min; AVB interface <ctl-iface> up | OK | precheck/host-checks.json |
| s2-host-002 | 04:52:30 | - | This host (not restarted, up 20 h): board link address <bench-address>.1 present and answering ping; board audio card and external audio card present; DUT console, board console and JTAG adapters present | OK | precheck/host-checks.json |
| s2-host-003 | 04:52:41 | - | Controller: up 7 min; sudo OK; no gPTP daemon; /tmp is an empty tmpfs, so B13's /tmp/667-b13 build is absent (rebuild in /tmp/608-b14 needed) | OK | precheck/host-checks.json |
| s2-host-004 | 04:52:51 | - | Tap host: up 9 h 36 min; both tap interfaces up; sudo OK; no tcpdump running | OK | precheck/host-checks.json |
| identity-001 | 04:54:38.543-04:54:47.713 (locked) | 1 | ATDECC ENTITY: entity_id, name, firmware_version and serial match; console CSR ID 4d494c4e, VERSION 00020060; `crc` of the QSPI AEM bytes and of the RAM copy (0x7f700000, 7,512 B) both 5ba355eb, equal to the flash record's boot line; gPTP SYNC=1 ASCAPABLE=1 TU=0; CLOCK_DOMAIN 0 source 0; ADP shows the DUT and the reference peer under one grandmaster | PASS | identity/ |
| soc-001 | 04:54:42 (inside identity-001's lock) | - | SoC board console: one carriage return, answered by a login prompt; `id -u` not sent (sent only after a root prompt) | STOP | identity/soc-check.txt |
| post-001 | 04:56:47 | - | Both audio cards still present; no lock held by this lane | OK | this file |

## Restore ledger

No bench state changed. The bench lock was taken once (identity-001, 9.2 s) for read-only actions:
- DUT console: `milan_status`, `crc 0x01400000 7512`, `crc 0x7f700000 7512`, `milan_nvm`;
- SoC board console: one carriage return;
- controller: `avdecc_ro.py` READ_DESCRIPTOR (ENTITY, CONFIGURATION, STREAM_INPUT 0-1, STREAM_OUTPUT 0-1, CLOCK_DOMAIN 0, AVB_INTERFACE 0), GET_CLOCK_SOURCE, and a 4 s ADP discovery.

The controller now holds `/tmp/608-b14/avdecc_ro.py` (the staged read-only tool, sha256 `17283696...`). It was left in place for the resume.

## Decisions needed for the resume (also in STOP.md)

- **Item 6 (#691).** The DUT's AVB_INTERFACE GET_COUNTERS mask is `0x23`: LINK_UP, LINK_DOWN, GPTP_GM_CHANGED. `milan_datapath.sv:3638` leaves FRAMES_TX/RX and RX_CRC_ERROR unclaimed. The FCS, preamble/alignment and bad-frame counts are RMON lanes (`REGISTER_MAP.md` section 0x200; `STATS_CAP` `0x1B8` on a LiteEth build). They are read through a `STATS_CTRL[0]` W1S snapshot write. This lane allows no register writes beyond the #451 stream and audio-interface controls. Without a ruling, item 6 grades only link up/down.
- **Item 7 (#686).** The firmware enables MAAP at boot (`MAAP_FABRIC.md`: S50milan provisioning before enable), so the acquisition happened at the last cold boot. With no power cycle and no register write, the lane can record only:
  - the held range and its ANNOUNCE intervals on the tap;
  - the peer's range and any overlap;
  - `MAAP_CTRL`/`MAAP_STAT0`/`MAAP_STAT1` (`0x6CC`-`0x6D4`), read only.

## Resume plan (prepared, not run)

- Build the controller library fork (a71ffa99) in /tmp/608-b14 on the controller. Reproduce B13's build line and its build-inputs hashes. Compile B13's probe.cpp unchanged.
- Item 2 uses B8's method (run_b8.py case SW): the peer's AAF to DUT STREAM_INPUT 0 and the peer's CRF to DUT STREAM_INPUT 1, under the binding rule. The DUT's CLOCK_DOMAIN goes 0 to 2 (hold), 2 to 1 (hold), then 1 to 0, ten times. A console poll reads `SLIP_LB`/`SLIP_TDM`/`RENDER_STAT` (0x8D4, 12 B), the servo (0x8F8) and the AAF meter (0x8E0). DUT and peer GET_COUNTERS are read at each mark, with the tap around each switch. The settle recentre has no silicon counter (`REGISTER_MAP.md:2056`). It is seen as RENDER_STAT's fill step and converged bit about 4.1 s after LOCKED, with `SLIP_LB` static from then on.
- Item 3 uses B2's method (b2_action.py cycle, b2_analyze.py): DUT STREAM_OUTPUT 1 (CRF) to peer STREAM_INPUT 8; DISCONNECT_RX, 2 s, CONNECT_RX. The tap is unfiltered, so the MSRP frames and the VLAN-tagged stream are included. The capture filter named in the bench brief matches only untagged AVTP, so it cannot see the bridge's Listener `Lv` or the tagged stream.
- Item 4 uses B13's run_short.py: DUT STREAM_OUTPUT 0 to peer STREAM_INPUT 0, a 2,000 ms hold, counter polls through the library.
- Items 5 to 7 use B13's four soak bindings, its counter set and a timing read every 5 minutes. Each foreground chunk is under 10 minutes, the bindings stay held in the devices between chunks, and the tap rolls.

## Deviations

- The SoC board console check sent one carriage return and nothing else. `soc_check.py` sends `id -u` only after a root prompt, so it was not sent.

## Large artifacts

None. No capture was taken.

## Posts

- STOP (session 2): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6093984746, posted 2026-10-10 at about 04:59 UTC. STOP.readback.md equals STOP.md except for one trailing newline; the URL is in stop-url.txt. Nothing else was posted.
