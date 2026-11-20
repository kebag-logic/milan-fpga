# F-G4 second board reading ([A783], the S12b bench lane, 2026-11-19 01:11-01:14)

The manager's resume of 2026-11-19 01:1x, items 1-3. This is a copy of the S12b gating HANDOFF 11.5 F-G4 "second
reading". The receipts are under the S12b gating lane's `receipts/fg4-r2/`. No cable was touched, nothing was chased
and no image was changed.

## Verdict: the TAP (bench). F-G4 is not a DUT defect.

The test machine's "Link partner advertised" is the inline capture tap's PHY, not the DUT. The DUT's own PHY
advertises 1000BASE-T full duplex alone, as #840 requires. It negotiates with the tap's other side, which offers every
mode. My round-2 F-G4 stop read the test machine's `ethtool` as the DUT's advertisement. Through an active tap, that
reading is invalid.

## 1. The cabling, as far as it can be known without touching it

- **The rehearsal's topology** (S12b rehearsal HANDOFF): "the test machine ... cabled to the DUT's port e2 through the
  1G inline tap; the capture host reads that tap passively". The tap is the inline capture tap at MAC `<tap-mac>`.
  Its control and capture host is a VM on the bench server.
- **What the tap reported** (11-15 09:0x, its read-only `show`): "port A DOWN, port B DOWN, all speeds advertised".
  At 11:49 the same day: "port A 1G and port B 1G". So the tap's ports advertise every speed themselves.
- **Its control host is still down** (01:11). `ssh` to it gets "Connection refused" (`fg4-r2/cabling.txt`), so the
  tap's port state cannot be read today. It has been down since the gating round 1.
- **Link counters, both sides** (01:11, the gating image):
  - the test machine's eth0: up at 1000 full, `carrier_up_count` 95 and `carrier_down_count` 94 since its boot;
  - its own advertisement: 1000baseT/Full, no pause;
  - its partner's: all six modes, no pause;
  - the DUT's AVB_INTERFACE 0: LINK_UP 2, LINK_DOWN 1 since its last boot.
- Over the reading below both sides counted +2/+2. The tap propagates a loss from one side to the other.

## 2. The second diagnostic 1x1/1if (bit `4f49291d…`): `milan_mdio` and `milan_phy` beside the test machine

The image was flashed as a detached unit and cold-booted through OUT0. BOOTSTS `0x1`, STAT `0x501079fc` clean, MILN
`0x00020060`.

| Point | The DUT's PHY (address 0 = 1) | `milan_phy` | The test machine |
|---|---|---|---|
| B, the cold boot's link | R1 `796d` (link up, autonegotiation complete). R4 `0401`: own advertisement, no 10/100, pause. R9 `0200`: 1000 full only. **R5 `c1e1`**: the partner offers 10/100 half and full, no pause. **R10 `3c00`**: the partner offers 1000 full and half. R17 `ad42`: 1000 full, link up | `ADDR=0 ADV=0`, `LINK=0000000d`, `R10_NOW=00003c00` | advertises 1000baseT/Full only, no pause; its partner: all six modes, no pause; 1000 full |
| T, the test machine at 10BASE-T half alone | **R1 `7949`: link DOWN, autonegotiation not complete.** R5 `0000`, R10 `0000`, R17 `4000` (no link) | `POLLS` rising, `WRITES` +2 | **carrier up at 10 Mb/s half**; its partner still all six modes; AECP to the DUT times out |
| R, back at 1000baseT/Full | as at B: R5 `c1e1`, R10 `3c00`, R17 `ac82` (1000 full, link up) | `LINK=0000000d` | 1000 full; its partner all six modes |

- **`MDIO_ACK=00000003`:** addresses 0 and 1 answer.
- **Both addresses are one PHY.** Their registers are identical, including PHYID `001c:c915` (RTL8211E), except R6
  (`0f`/`0d` at B, `06`/`04` at T). R6's "page received" bit clears on read, and address 0 is read first. So address
  0 is the RTL8211E's broadcast alias of its strap address 1: the same register file. That matches the composition
  lane's pinout reading: e2's own bus, one PHY.

## 3. Why this decides it

1. **The DUT's partner is not the test machine.** At B the DUT's PHY reads a partner offering 10/100 and 1000 half
   (R5 `c1e1`, R10 `3c00`). The test machine at that moment offers 1000baseT/Full alone.
2. **The test machine's partner is not the DUT.** It reads all six modes and no pause. The DUT's PHY offers 1000
   full alone with pause (R4 `0401`, R9 `0200`, verified since the boot's write).
3. **The two links are separate.** With the test machine at 10BASE-T half alone, the test machine holds a 10 Mb/s
   link while the DUT's PHY has no link at all (R1 link bit clear, no partner page). A 10/100/1000 device between
   them negotiates each side on its own: the tap.
   - The composition lane predicted the DUT would stay at 1000 during that phase. It does not: its side drops. This
     tap does not hold the DUT's side up when the two sides cannot share a speed. Either way the two sides differ.
4. **Both sides see one advertisement:** all six modes, no pause. That is the tap's ports' "all speeds advertised".

## 4. What follows (for the owner; not chased)

- **F-G4 is a bench-topology finding.** The DUT's #840 advertisement is in force on its own PHY on this image. The
  acceptance check ("the partner sees 1000baseT/Full only", "no link with 10BASE-T half alone") can only be judged on
  a direct cable, which needs the owner's hands. With the tap in the path, a 10BASE-T partner gets a link to the tap,
  not to the DUT.
- **The address question is closed:** address 0 is e2's PHY, the broadcast alias of address 1.
- **Likely tap effects as well, not proven:** round 2's "silent link" after the test machine's `ip link` restart. Its
  link came up at 1 Gb/s while nothing passed for 8-9 s, then dropped and returned. That fits the tap renegotiating
  and propagating its two sides one after the other. A direct cable would show it.
