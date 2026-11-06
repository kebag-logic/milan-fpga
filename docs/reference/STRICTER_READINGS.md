# Stricter and narrower readings

This page registers each deliberate narrower reading of a clause.

Each row gives the clause, its allowance and the choice.

The maintainer decided these readings on 2026-11-05.

## Contents

- **[How to read the rows](#how-to-read-the-rows)** -- What each column states.
- **[Station identity](#station-identity)** -- Locally administered prototype addresses and the builder warning.
- **[Link speed](#link-speed)** -- The 1000BASE-T full-duplex-only advertisement.
- **[The certification_version field](#the-certification_version-field)** -- `0.0.0.0` for a device that passed none.
- **[gPTP readings](#gptp-readings)** -- Announce aging, late Pdelay responses and clockAccuracy.

## How to read the rows

- **Clause** cites the governing text by number.
- **The clause allows** states what it permits or requires.
- **The board does** states this end station's behaviour.
- **Why** gives the reason for the choice.
- **Where**, a bullet under each table, names code and tests.
- **Reading** names each gPTP row's behaviour.
- **At the pinned processor** states the current gitlink's behaviour.

A reading found later is added here, with its clause.

## Station identity

[#840](https://github.com/kebag-logic/milan-fpga/issues/840) item 1 gives each prototype a locally administered address.

| Clause | The clause allows | The board does | Why |
|---|---|---|---|
| IEEE 802-2014 8.2 and 8.4 | A universally administered address (U/L bit 0) or a locally administered one (U/L bit 1) | AX7101 `02:4B:4C:4B:4C:01`, Arty `02:4B:4C:4B:4C:02`, both with the U/L bit set | No owned MA-L, MA-M or MA-S block exists yet |
| IEEE 802.1AS-2011 8.5.2.2.1 | A clockIdentity mapped from an EUI-48 the organization owns | clockIdentity `024B4CFFFE4B4C01` and `024B4CFFFE4B4C02`, still mapped from the MAC | One identity source per board |
| IEEE 1588-2008 7.5.2.2.2 | An OUI whose two least significant first-octet bits are both 0 | The U/L bit is 1 | The same prototype limitation |
| IEEE 1722.1-2021 6.2.2.7 | An entity_id the vendor assigns, which can be computed from the MAC | entity_id `024B4CFFFE4B4C01` and `024B4CFFFE4B4C02`, computed from the MAC | Unique on the bench; the boards differ in the last octet |

This is a prototype limitation, not a stricter reading.

- These addresses are not IEEE-assigned EUI-48 values.
- A production build needs an owned MA-L, MA-M or MA-S.
- No octet of either EUI-64 identity is `00`.
- The builder gate refuses any zero identity octet.
- The builder warns when the U/L bit is set.
- The warning goes to stderr; the build still completes.
- Where: `configs/endstation_*.yaml` and `identity_warnings()` in `sw/builder/endstation_builder.py`.
- Tested by gate `test_station_mac_ul_bit_warns` in `sw/builder/test_builder.py`.

## Link speed

[#840](https://github.com/kebag-logic/milan-fpga/issues/840) item 2 limits the link to 1000BASE-T full duplex.

| Clause | The clause allows | The board does | Why |
|---|---|---|---|
| IEEE 802.1BA-2011 6.5 d) | Any medium of 100 Mb/s or more in an AVB domain | 1000BASE-T full duplex only | The AX7101 MAC runs at 1 Gb/s only |
| Milan v1.2 Chapter 1 | The design goal of links at or above 100 Mb/s | 1000BASE-T full duplex only | The same MAC limit |
| IEEE 802.3-2022 28.2.4.1.3, Table 28B-1 | Any supported ability in register 4; management may clear them before renegotiating | Register 4 carries no 10BASE-T, 100BASE-TX or 100BASE-T4 bit | A 100 Mb/s link formed, and the board then stayed silent |
| IEEE 802.3-2022 Table 40-3 | 1000BASE-T full duplex, half duplex, or both, in register 9 | Full duplex only; the MASTER-SLAVE bits are kept | The MAC is full duplex only |
| IEEE 802.3-2022 22.2.4.1.7 | A restart of auto-negotiation through bit 0.9 | One restart per boot, after both writes | 28.2.4.1.3 asks for a renegotiation after a change |
| IEEE 802.3-2022 22.2.4.2.16, 22.2.4.4.3 | Bit 1.8 marks register 15, whose bit 15.13 is the PHY's 1000BASE-T full duplex ability | The init writes only a PHY with both bits set; any other is never written | A 10/100 PHY sits behind a MAC that runs 10 and 100 Mb/s |

A partner without 1000BASE-T gets no link.

`MAC_STATUS` then reports the link down, so the fault is visible.

A PHY lacking 1000BASE-T full duplex keeps its advertisement.

The retired Arty has such a 10/100 PHY. Its MII MAC runs 10 and 100 Mb/s.

- Where: `phy_advertise_gigabit_only()` in `sw/firmware/milan_baremetal/milan_baremetal.c`.
- Tested by `sw/firmware/nvm_hosttest/test_phy_firmware.py`, with fifty-one named mutants.
- The [firmware guide](../integration/BAREMETAL_FIRMWARE.md) describes the PHY poll.

## The certification_version field

[#840](https://github.com/kebag-logic/milan-fpga/issues/840) item 3 keeps `certification_version` at `0.0.0.0`.

| Clause | The clause allows | The board does | Why |
|---|---|---|---|
| Milan v1.2 5.4.4.1, Figure 5.4 | The version the PAAD-AE passed, as four 8-bit numbers, or 0 when it passed none | `0.0.0.0` in every GET_MILAN_INFO response | By decision, the device has passed none |

The clause itself sets zero for such a device.

It is recorded here as a deliberate choice.

The field belongs to the GET_MILAN_INFO response, not a descriptor.

- Where: `MILAN_CERT_VERSION` in the protocol processor's AECP microprogram generator.
- Tested by check M2 of the protocol processor's pp_top harness.
- Also by `tests/features/aecp_response_contract.feature`, against the model.

## gPTP readings

[FPGA-gPTP #100](https://github.com/Mister-M-alt/FPGA-gPTP/issues/100) items 3 to 5 are deliberate stricter readings.

Its items 1 and 2 are defects, tracked there.

These three land with that issue and a gitlink update.

| Reading | Clause | The clause allows | The board does | Why | At the pinned processor |
|---|---|---|---|---|---|
| Announce aging at the instant | Milan v1.2 4.2.6.2.3, Table 4.2; IEEE 802.1AS-2011 Figure 10-13, as Cor1 changes it | announceReceiptTimeout from 2.7 s to 4.5 s. Figure 10-13 guards CURRENT to AGED with `!rcvdMsg`, but does not order PortAnnounceReceive setting `rcvdMsg` against the expiry instant | An Announce arriving exactly at the expiry does not refresh the port; the timeout fires first. With a 1 s interval, Announces 3.0 s apart age the port | 3.0 s lies inside Table 4.2. Such a gap is outside Table 4.1's 1500 ms Announce maximum | The tie is ungraded; FPGA-gPTP #100 adds the row |
| Late Pdelay responses | Milan v1.2 4.2.6.2.6; IEEE 802.1AS-2011 B.2.3, 11.2.15.1.10, Figure 11-8, 11.5.3 | A turnaround of at most 10 ms (B.2.3), relaxed by 50% to 15 ms. Later responses may or may not be processed, and "should not" clear asCapable | A Pdelay_Resp and Pdelay_Resp_Follow_Up pair later than 15 ms counts as a lost response. Above allowedLostResponses, which is 3, asCapable becomes FALSE | "Should not" is a recommendation, and the board takes the stricter path | A pair is lost only when its interval ends unanswered |
| clockAccuracy | IEEE 802.1AS-2011 8.6.2.3; IEEE 1588-2008 7.6.2.5, Table 6 | The value reflecting the LocalClock and ClockSource, or 0xFE when that is unknown | Default 0x22, accurate to within 250 ns. It is a build parameter, so a build with no characterised oscillator says 0xFE | The decision. 7.6.2.5 asks for an estimate behind any claimed value | 0xFE |

- The 15 ms bound is 10 ms relaxed by 50%.
- A build claiming 0x22 owes that oscillator characterisation.
- The processor issue's harness rows are the executable evidence.
