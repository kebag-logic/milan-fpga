# F-G4 board reading ([A783], the S12b bench lane, 2026-11-19 00:05-00:25)

The manager's resume of 2026-11-18 23:1x, items 1 and 2: the release reference and the two diagnostic images, read
on the bench's ALINX AX7101 through its e2 port. This file is a copy of the S12b gating HANDOFF 11.5 F-G4 "board
reading"; the receipts are under the S12b gating lane's `receipts/rel/`, `receipts/diag1/` and `receipts/diag8/`.
Nothing was chased and no image was changed.

## How each image was read

- **Flash:** flash-pair through `build.sh flash ax7101:<build>`, as a detached unit under the bench lock, then a cold
  boot through OUT0. After each boot: BOOTSTS `0x1` (normal configuration, no CRC error), STAT `0x501079fc` clean,
  MILN, VERSION `0x00020060`, AEM loaded.
- **Partner's view:** the test machine's `ethtool eth0` "Link partner advertised link modes" (its registers 5 and 10),
  and the DUT's AVB_INTERFACE 0 LINK_UP and LINK_DOWN counters.
- **Points** (`diagread.sh` in the S12b lane's tools):
  - **B** the cold boot's link, nothing changed;
  - **L** after a link loss: the test machine advertises 10BASE-T half alone for 5 s, then its owner-approved
    1000baseT/Full (0x020); read 15 s later;
  - **D** during an outage: the test machine's eth0 down, read 4 s into it (its carrier: none);
  - **E** after an Ethernet stop/start: eth0 up, the PHY setting re-applied at once (the harness's order), read 30 s
    later.
- **`milan_phy`:** sent twice about 1 s apart at each point, on the diagnostic images only.

## 1. The release reference: the PHY never takes the 1000-only advertisement

The all-fabric release image built at the train's step-12 head `967b1ca9`:
- **Recipe:** `build.sh ax7101`'s recipe, `configs/endstation_ax7101_1x1_tdm8.yaml`, ExtraPostPlacementOpt, with the
  bench override `--eth-port e2`.
- **Build:** LiteX compiles the bare-metal firmware, so `phy_advertise_gigabit_only()` is in. It finished rc=0. WNS
  +0.362 ns, WHS +0.032 ns, all user timing constraints met. Bitstream sha256 `88404bf4ca56229b…`.
- **Reading** (`receipts/rel/fg4read.txt`). At every point the partner's view is the same, all six modes:
  10baseT/Half, 10baseT/Full, 100baseT/Half, 100baseT/Full, 1000baseT/Half, 1000baseT/Full:
  - at the link as found after the cold boot;
  - 30 s after an Ethernet stop/start;
  - after the restore.
- With 10BASE-T half advertised alone, **a 10 Mb/s half-duplex link formed**.

**So F-G4 is not introduced by the split.** The release firmware's advertisement does not reach the wire on this board
and port either.

## 2. The diagnostic images: what `milan_phy` reads

The same on both images (1x1/1if bit `21aa68e1…`, 8x8/1if bit `d4e4141f…`). One line from each point (1x1/1if):

| Point | Fields that change | Fields that never change | Partner's view | DUT LINK counters |
|---|---|---|---|---|
| B | `POLLS=104` → 114 1 s later, `WRITES=3`, `LINK=0000000d`, `R4_BEFORE=000005e1` | all the others | all six modes | — |
| L | `POLLS=316`, `WRITES=5`, `LINK=0000000d`, `R4_BEFORE=00000401` | | all six modes | +1/+1 |
| D | `POLLS=1189`, `WRITES=9`, `LINK=00000000` | | carrier none | — |
| E | `POLLS=1478`, `WRITES=9`, `LINK=0000000d` | | all six modes | +1/+1 |

The fields that never change at any point: `PHY_ARMED=1 FOUND=1 ADDR=0 ADV=0 RENEG=0 RESTARTS=1 R9_BEFORE=00000200
R4=00000401 R9=00000200 R9_NOW=00000200 R4_NOW=fffffffe R0=00001140 SPIN=1`.

The 8x8/1if image: B `POLLS=112`/122, `WRITES=3`; D `LINK=00000000`; L and E `LINK=0000000d`; every other field as
above. The partner saw all six modes at B, L and E.

## 3. What the reading shows

1. **The poll runs and is not stalled.** `POLLS` rises about 10 a second.
2. **The writes land and verify, in the register set at address 0.**
   - Register 4 reads `05e1` before the boot's write: the 10/100 bits, pause and the selector. It reads back `0401`:
     pause and the selector, no 10/100.
   - Register 9 reads back `0200`, 1000BASE-T full alone; `R9_NOW` holds `0200`.
   - `ADV=0` (verified). The boot's one restart is taken (`RESTARTS=1`, register 0 `1140` before it). After each loss
     registers 4 and 9 are written again, without a restart (`WRITES` +2 each time), as designed.
   - So by the composition lane's table this is the last row: the registers hold the advertisement, and the partner
     sees every mode.
3. **The PHY at address 0 reports the e2 link.** Its link status went down during the outage (D, `LINK=00000000`)
   and up again after it.
4. **The register set at address 0 and the advertisement on the wire disagree, already at the cold boot, before any
   write.**
   - At B, `R9_BEFORE=00000200`: register 9 holds 1000BASE-T full only, before the firmware writes anything. The
     partner sees **1000baseT/Half** as well.
   - After the write register 4 reads `0401`, no 10/100 bits. The partner still sees 10/100 offered, and a
     10BASE-T-only partner gets a 10 Mb/s link.
   - So what is read and written at address 0 is not what the negotiating PHY sends.
5. **The address.** The poll uses address 0, the first address whose PHYID1 answers; the release's probe starts there
   too. The composition lane gives the PHY as **address 1**. Point 4 is what one would see if address 0 were not the
   negotiating PHY's own register set. Two examples: a broadcast or alias address that answers reads with the link
   state but does not carry the advertisement; or a second device. That is a reading, not a proof. Point 3 shows that
   whatever answers at 0 reports the e2 link.

## 4. Not done here (for the composition lane)

- **Reading address 1 directly** would settle point 5: PHYID1/2 and registers 1, 4, 9 and 10 at address 1, beside
  address 0, once with the link up. The diagnostic images read address 0 only. No image was built here, as the brief
  says.
- The S12b lane's gating image is back on the board (the end state), the round-1 8x8/1if bit `0b3ea432…`.
