# F-G4: the diagnostic and the three fix candidates

Each diff applies to the train head `967b1ca9` with `git apply` (checked). None is on `flip-train-1117-p11`.
The manager names the cause, and that candidate becomes one train commit.

## The diagnostic, `diagnostic.diff`

- Scratch branch `fg4-diag-967b1ca9` at `fcdb9f6c`.
- A bench image only, never a train commit.
- It adds the console command `milan_phy` and the poll's counters, kept file-static so `struct ctrl_plat` and its
  ledgered size stay unchanged.
- For that image only, it raises the 8x8 one-interface ROM entry to 58.5: the command needs 92 B of `rom` past 58.0.

## The second diagnostic, `diagnostic2.diff` (2026-11-19)

- Scratch branch `fg4-diag2-967b1ca9` at `46af043b`, on top of the first. A bench image only.
- `milan_phy` adds `R10_NOW`: register 10, the link partner's 1000BASE-T ability, as the latest poll read it. It
  costs no extra frame, since the poll reads it every time.
- A new command, `milan_mdio`:
  - `MDIO_ACK=`: bit n is set where address n acknowledged a PHYID1 read on the poll's bus.
  - Then one line each for addresses 0 and 1, and for the first two other addresses that answered: registers 0 to 6,
    9, 10, 15, 17 (the RTL8211E's specific status) and 31 (its page select). `ffffffff` means unacknowledged.
  - The reads block for about 12 ms. Reading register 1 clears its latched link-down bit, and reading register 10
    clears its fault bit, so type it at a reading point, not while a loss is being counted.
- Checked:
  - `diag_quick2.c` passes. Its model is one open-drain bus with two PHYs, at addresses 1 and 3. The poll finds
    address 1 and writes it 3 times. Address 3 stays at its defaults, and `MDIO_ACK=0000000a`.
  - The `platboot` arm: 52 of 52.
  - The boot simulation at both points, inside the bench builds.

## The candidates, one per cause

| | Cause | The fix | Its test | Before | After |
|---|---|---|---|---|---|
| `candidate-a.diff` (branch `fg4-fix-a`, `63fb939d`) | (a) the PHY back at its defaults after the boot's write was verified, with no loss the poll published: its own init completing after the fabric's 2.56 us reset pulse, or a reset the poll did not see | THE CANARY: each poll's own register 9 read, in the 1000BASE-T resolution, so no extra frame. A verified advertisement whose register 9 reads otherwise is owed again with its restart, counted in `renegotiations` | `PlatPhy.P14BDefaultsReturnedWithNoPublishedLossAreAdvertisedAgain`: the boot's advertisement verified, then the PHY at its defaults and negotiated on them at 1000 Mb/s with no latched loss. It requires 4 and 9 written again and one restart | FAIL by name: register 9 stays 0x0300, no restart | PASS; `platboot` 53 of 53 |
| `candidate-b.diff` (branch `fg4-fix-b`, `f27ee40f`) | (b) the poll starved. Under input that leaves no pass empty, THE STEP runs only aged, so every call owes the store a centisecond's step, and a save's steps leave the PHY no room for the save's whole length | LIVENESS: a poll a whole period late (in progress since a period ago, or idle and due since a period ago) takes the call's frame ahead of the store's centisecond step, which waits for the next call. Still no call carries a save's step and a frame | `Phy.B13APollAPeriodLateTakesItsFrameThroughASave`: a save behind a 600 ms erase, every call owing a centisecond's step. It requires a link loss published within two poll periods while the save is in flight | FAIL by name: the loss is published only after the save | PASS; `platboot` 53 of 53 |
| `candidate-c.diff` (branch `fg4-fix-c`) | (c) the PHY's handling of the split's bit, which lowers MDC and changes the data in one bus write | THE BIT as the release's `phy_mdio_bit`: MDC lowered with the data and output enable unchanged, and only the next bit's first write changes them | `PlatPhy.P19TheDataIsHeldThroughMdcsFallingEdge`: a stricter pin rule in the host PHY model, no data or output-enable change on MDC's falling edge. Not IEEE 802.3's rule; the release's bit keeps it | FAIL by name, every frame | PASS; `platboot` 53 of 53 |

Every test runs in the firmware harness's `platboot` arm. The receipts are in `receipts/step12/fg4/`: `pb-*0` before
the fix, `pb-*1` after.

## What each needs before it is a train commit

- **Every candidate:**
  - the four firmware shards: the control campaign's PHY anchors may need re-anchoring, and no plant may be removed;
  - `fw_coverage --check`: the new branches need coverage or an exclusion;
  - the twin and its plants, and the docs jobs;
  - the boot simulation at both points;
  - the split routes at 1x1/1if and 8x8/1if (the firmware is the ROM's contents) and the image hashes;
  - the comment and doc text of THE OUTCOME, THE STEP or THE BIT, as the candidate changes it (`ctrl_plat_phy.h`,
    `docs/integration/BAREMETAL_FIRMWARE.md`).
- **A:** no frame or pace change. `rom` grows by tens of bytes: 8x8/1if has 832 B left at 58.0, and 8x8/2if 1,304 B
  at 63.0.
- **B:** it changes THE STEP's precedence in the overdue case, so it needs #665's word, since the ruling of
  2026-11-17 set THE STEP's order. The CPU budget rows are unchanged where no poll is a period late.
- **C:** each frame takes 64 more bus writes. The boot simulation measured 157.92 us at 1x1/1if and 157.57 us at
  8x8/1if, past the stated 155 us; it fails the PHY grade at 155. So `CTRL_PLAT_PHY_STEP_US` is restated by the rule
  (+5 %, rounded up to 5 us) to 170 us in the candidate, and both boot simulations pass at 170. The CPU budget
  harness does not read that figure, its image being the AECP and SRP test image. A frame now needs 170 us of room,
  so THE STEP's admission of PHY frames is slightly stricter.

## The commit subjects

- A: "Re-verify the split PHY's advertisement on every poll's own register 9 read: a PHY back at its defaults with
  no published loss is advertised again with its restart (F-G4)"
- B: "Let a split PHY poll a whole period late take THE STEP's call ahead of the store's centisecond step, so a link
  loss is published through a save under input (F-G4)"
- C: "Hold the split MDIO data and output enable through MDC's falling edge, as the release's bit does (F-G4)"
