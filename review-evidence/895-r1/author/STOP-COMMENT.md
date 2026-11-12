[A775] STOP — a ROM ledger point overflows
Head: `0f980b5c59e49f4ed806c47ea9b8964882951615` (branch `895-talker-redeclare` on `66f71326`, not pushed)

**What the head does.** MAAP's allocation port passes each report to a new SRP entry, `srp_mbx_allocation`, for the reporting interface's sources. The entry only records the change, so it calls no protocol core and makes no mailbox access. THE TRANSMIT then declares each source:
- Allocated and admitted: Talker Advertise with destination base + n and the generated TSpec.
- Not allocated: Talker Failed, code 2, as acceptance 1 keeps it. Allocated but not fitting: code 1.
- IEEE 802.1Q-2018 35.2.2.8 does not support a changed FirstValue on a StreamID. So a declared source whose destination moves (allocated, changed or lost), or whose admission changes, withdraws:
  - its licence closes, then `TALKER_DECL` and `IDLE_SLOPE` drop it before the Leave is sent;
  - it declares again no sooner than two LeaveAllTime periods (Table 10-7) after the Leave, held across a link reset;
  - no stale Advertise remains after a loss.
- No mailbox contract change, and no other protocol behaviour changes.

**Tests and plants.** `srp_talker.cpp` (8 tests) passes at 1x1/1if and 8x8/2if, and platform test B11 at one and two interfaces. One planted defect per rule (16 SRP, 2 platform) is each refused by its named test on its own words, at both points. The 16 existing SRP plants anchored on the old `declare_sources` were restated, and all were caught again.

**The bytes** (`ctrl_srp_image.py` / `ctrl_plat_image.py`, clean clones). The platform's 8x8/2if image is linked with its ledger key at its measured `ctrl_plat` size: the committed key is stale at the base.

| Image, point | Base `66f71326` | Head | Delta | Ledger | Verdict |
|---|---:|---:|---:|---|---|
| size fixture 8x8/2if | 122,440 rom (57.5) | 123,336 rom, 112,496 sram (58.0) | +896 | 57.5 (122,880 rom) | **over by 456 B** |
| platform 8x8/2if | 127,664 rom (59.5) | 128,624 rom (59.5) | +960 | 59.0 (126,976 rom) | **over already at the base by 688 B** (reported by #810 round 29); 1,648 B at the head |
| the six other points | | | +816 to +968 | 56 | hold (38.0 to 52.5) |

The same head merged with #810's round 29 head `446d3310` (a scratch merge, not pushed):

| Image, point | Round 29 alone | Merged | Delta | Round 29's ledger | Verdict |
|---|---:|---:|---:|---|---|
| size fixture 8x8/2if | 123,112 rom, 112,576 sram (58.0) | 124,016 rom, 112,640 sram (58.0) | +904 | 58.0 | fits: 912 B rom, **0 B sram** spare |
| platform 8x8/2if | 128,264 rom (59.5) | 129,232 rom (**60.0**) | +968 | 59.0 | over; 208 B past 59.5 |

The change costs 816 to 968 B of rom at each point; size passes brought it down from 1,104 B. No form that keeps every rule fits the 440 B the 8x8/2if fixture has under this base's 57.5.

**Asked.**
1. May the lane continue on #810's merged head? There the 8x8/2if size fixture is ledgered at 58.0 and this change fits, with 0 B of sram spare.
2. A ruling on the platform's 8x8/2if image. It is already at 59.5 against its 59.0 at this base, and this change makes it 60.0 on the merged head: either 60.0, or a cut (lane S14, decision D3; 2,256 B gets it back to 59.0).
3. A decision on the hold-off's consequence. Acceptance 1 keeps the boot-time Talker Failed, whose destination differs, so under 35.2.2.8 the first Advertise comes about 20 s after MAAP's first allocation. Milan v1.2 5.3.7.2 and 5.3.7.4 would declare nothing until the destination is valid, so it would advertise at once.

**Not run, by the STOP rule:** the CPU-budget harness at both points (the 8x8 image cannot be built at 57.5 on this branch), the cost restatement in `load_grade.py`, `fw_coverage.py --write`/`--check`, the full mutant campaigns, the split boot simulation, `test_builder.py`, `behave`, and the clean-clone gate pass.

Also noted for an issue: a Domain adoption re-declares every source in place with a changed vlan_identifier, which 35.2.2.8 does not support either. This change leaves that unchanged.
