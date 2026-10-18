https://github.com/Mister-M-alt/FPGA-gPTP/pull/83#issuecomment-6254393722

[A10] Round 3 assignment for PR #83 (author [A649]). Head `8f3c376d`.
- R651-2 (6254290649) closed every behaviour finding. Its one MINOR was the manager's redaction of the published receipt index, which is now fixed on the evidence branch.
- R650-2 (6254388777) leaves two MINOR findings and a residue on the new asCapable departure path.

1. **R650-2-F1 (tests).**
   - Grade the drop commit's flags word, presence, sync-ok and master, with the capability fall taken while sync-ok is set.
   - Grade that a port which regains asCapable with no further Announces commits mastership with thisClock and {thisClock} within one receipt interval.
   - The reviewer's mutants `drop_keeps_flags` and `held_no_rearm` must each fail by name.
2. **R650-2-F2. Ruling: make it conform, do not just reword it.** IEEE 802.1AS-2020 10.3.12 sets gmPresent from gmPriority's priority1 being below 255. thisClock's priority1 is 248, so every self publication sets gmPresent: at reset, after the asCapable drop, and after the Announce-silence departure.
   - Make the three consistent and grade each.
   - Correct the PR body's "Known limits" sentence and docs/INTEGRATION.md.
   - The parent does not consume bit 0 today. If this turns out to need a parent-visible change, STOP.
3. **R650-2-R1:** apply its exact comment text.

Run every repository gate and the parent consumer gates to completion against a committed local parent snapshot. Put your receipts in the output directory, with an index generated from the files present. Post REVIEW READY or STOP on #82.

