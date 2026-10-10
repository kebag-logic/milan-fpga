[A578] STOP

Head: `5603c353137e90c1fa95429f6d00ef7a2298d9ee` (branch `608-b14-bench`, unchanged, no commit).

This is the resume after the controller host came back at 04:45 UTC. I re-checked every host from the start. **Item 1, the identity gate, passes.** After that, the SoC board's serial console answered a single carriage return with a login prompt instead of the root shell. The bench rule for that console says: stop and leave the login to the manager. I typed nothing at the prompt: no command and no credential. Nothing on the bench changed.

| Cycle | UTC | Item | Observation | Result |
|---|---|---|---|---|
| s2-host-001 | 04:46:55 | - | Controller host up (booted 04:45), AVB interface up | OK |
| s2-host-002 | 04:52:30 | - | This host: board link address present and answering; both audio cards, both consoles and the JTAG adapter present | OK |
| s2-host-003 | 04:52:41 | - | Controller: no gPTP daemon; its temporary directory was wiped, so lane B13's controller build is gone and must be rebuilt | OK |
| s2-host-004 | 04:52:51 | - | Tap host up, both tap interfaces up, no capture running | OK |
| identity-001 | 04:54:38-04:54:47 | 1 | entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001"; console CSR ID `4d494c4e`, VERSION `00020060`; AEM CRC `5ba355eb` over 7,512 B of both the QSPI bytes and the RAM copy; gPTP SYNC=1 ASCAPABLE=1 TU=0 | PASS |
| soc-001 | 04:54:42 | - | SoC board console: one carriage return was answered by a login prompt; nothing else was typed | STOP |

| Item | Planned | Completed | Result |
|---|---:|---:|---|
| 1 Identity | 1 | 1 | PASS |
| 2 INTERNAL→AAF / AAF→CRF | 10 / 10 | 0 / 0 | NOT RUN |
| 3 DUT-talker disconnects | 100 | 0 | NOT RUN |
| 4 Talker starts | 100 | 0 | NOT RUN |
| 5 Default maps, two-hour soak | 120 min | 0 | NOT RUN |
| 6 Ethernet RX sanity | soak | 0 | NOT RUN |
| 7 MAAP interop | 1 | 0 | NOT RUN |
| 8 Restore | - | - | Nothing changed |

**Bench state: unchanged.** The bench lock was held once, for 9 s, by the identity gate. It ran only:
- read-only DUT console commands (`milan_status`, two `crc`, `milan_nvm`);
- one carriage return on the SoC board console;
- AECP READ_DESCRIPTOR and GET_CLOCK_SOURCE reads and an ADP discovery, from the controller.

There was no capture, no bind, and no format, clock or register change. The lock is free.

**To resume:** the manager logs in on the SoC board console. Alternatively, a ruling that the console check does not apply to this lane, which runs no tone or audio path. The lane then re-checks the hosts and the identity gate and continues from item 2.

Two points need a decision before the resume. I have not acted on either:
- **Item 6 (#691).** Over GET_COUNTERS, the DUT's AVB_INTERFACE counters cover only LINK_UP, LINK_DOWN and GPTP_GM_CHANGED (valid mask `0x23`). The FCS, alignment and drop counts are the RMON lanes at `0x210`-`0x230`. Reading them needs a `STATS_CTRL[0]` snapshot write (W1S, self-clearing). This lane allows no register writes beyond the stream and audio-interface controls. As things stand, item 6 can grade the link counters but not the RX error counters.
- **Item 7 (#686).** The firmware enables the DUT's MAAP engine at boot, so its acquisition (the PROBEs) happened at the last cold boot. With no power cycle and no register write allowed, this lane can record only:
  - the held range and its ANNOUNCE intervals on the tap;
  - the reference peer's range and any overlap;
  - the conflict and DEFEND counts in `MAAP_STAT0`/`MAAP_STAT1`, read only.

  It cannot observe a fresh acquisition.

Stopping here.
