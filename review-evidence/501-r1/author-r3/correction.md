[A10] Correction to the capture-hold decision in 5823589125, item 3, following R312-2 F1.

My premise was wrong. I wrote that "maps are not materialized yet (only BINDING is), so no map copy exists to overrun today". The parent firmware's `nvm_capture()` copies every closed record of the shape at each capture, materialized or not. So the 8x8 exposure (2x model 63.8 ms against the 50 ms hold, 0.78x) exists at this head on every 8x8 build. The copy belongs to this repository, not to the donor writer.

Corrected disposition, still with no RTL change in this PR:
- Owner: new parent issue #559. It measures the copy at 8x8, then sizes the hold, makes the copy cheaper, or shows 50 ms is enough.
- Safety holds (void and retry). The shipping 1x1 shape keeps a 3.03x margin.
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6 must state what the firmware copies today, and must point to #559, not to the donor.
- The donor obligation I posted on processor #61 is withdrawn there.
