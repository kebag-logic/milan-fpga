[A10] Round 3 assignment for PR #557. R312-2 F1 (MAJOR) and R313-2 F1 (MINOR) are the same finding, and it traces to my wrong premise, corrected in 5824117439. Executor [A291].

1. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 (Timing, about :1600-1602) and UNRESOLVED 6 (about :1699-1700) must state what happens today:
   - the firmware's `nvm_capture()` copies every CLOSED record of the shape at each capture, whether or not it is materialized, because a RELOAD closes every allocated record (`KL_nvm_backend.sv` around :1122-1133);
   - at 8x8 that is 12,634 bytes, of which 4,672 are output maps, so the 2x-model exposure (0.78x) exists at this head;
   - safety holds through void and retry, and 1x1 is unaffected.
2. The owner of the measurement and the resolution is #559, not the donor writer. Remove the donor-adoption trigger wording, and cite #559 and the counted bytes (R312-2's probe or your own).
3. Change nothing else. Run both reviewers' `capture_copy_probe.py` and `hold_margin.py` unchanged, and show the page matches them.

Gates: the docs set as in round 2, plus `check_nvm_record_space.py`. Review: delta reviews at the new head by [R312] and [R313].
