**Ruling: two findings from the gating bench run's qualification replay, on the final images.** Decided for the owner under the delegation of 2026-11-11. The owner is informed and may veto before the merge.

**1. A STREAM_OUTPUT's GET_STREAM_INFO status: merge with it as a named known limitation.**
- **The defect:** a running output reports stream_dest_mac 0 with STREAM_DEST_MAC_VALID set, and never sets REGISTERING or REGISTERING_FAILED (Milan v1.2 5.4.2.10, Table 5.8; IEEE 1722.1-2021 7.4.16). It is pre-existing in the split. It is status reporting only: the frames flow to the MAAP address.
- **Why not fix it in the train:** a fix changes the firmware image after the gating run. The soak and power cycles would no longer carry by byte identity, so the cost is a full bench re-run.
- **"No failure is acceptable"** is the release rule. No release is cut from the split until this passes.
- **The fix starts now under #943,** as the first PR after the flip: the destination MAC from the talker's MAAP address, and both flags from the MSRP registrar's Listener declaration. It has tests on every output and re-measures the AECP rows.
- The train record names the limitation and its clauses.

**2. The re-declare hold-off after a MAAP conflict: cover the randomised LeaveAll, after the flip.**
- **Today:** the split re-declares a withdrawn stream 20.3 s after the unregistration: 2 x LeaveAllTime plus JoinTime and one transmit, #895's accepted reading. By the project's own reading, IEEE 802.1Q-2018 35.2.2.8 sets only the least, so a longer hold still conforms.
- **Why move it:** a real LeaveAll period runs up to 1.5 x LeaveAllTime (10.7.4.3; Milan v1.2 Table 4.3).
- **The change:** derive the constant from two longest LeaveAll periods plus the existing terms, about 30.2 s at one interface. That matches the release.
- **Its PR** shows an image diff limited to that value, and restates the Talker tests, mutants and docs.
- Until then the train record lists it as a known divergence.
