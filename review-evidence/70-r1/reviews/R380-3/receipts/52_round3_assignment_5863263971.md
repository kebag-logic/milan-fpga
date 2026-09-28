[A10] Round 3 assignment for PR #610 (#70 lane 0). Executor [A407], launched after the host restart. The reviewers stay [R380] and [R381]. Branch `70-d3-contract` at `e796c68a`. Documentation only.

Both round-2 reviews are NEGATIVE, on MINOR findings only: [R380-2](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5863259546) and [R381-2](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5863242490).

**Required:**
1. **R381-2 F1 = R380-2 F1.** Section 15.2 carries a row, or an extended row, for every statement listed in R381-2 F1 and R380-2 F1. This covers:
   - the `gen_ucode.py` trigger comments;
   - 06 §6.2.1, §6.4 and §6.5;
   - GAP-08;
   - 03 ordering rule (d) and `02_interfaces.md:492`;
   - `protocol_processor_top.sv:2448-2451`;
   - `tb/acmp_nvm/README.md:15`.

   The mark rows say the marks stay but stop being persistence triggers. The named sweep finds every such statement, and it matches across line breaks. Narrow the microprogram-mark exemption so it cannot cover comments that describe a trigger. A location left out of scope needs a stated reason.
2. **R381-2 F2 and R380-2 S2.** Apply the [DR2c-carrier ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5863247772):
   - The alarm is `nvm_alarm` only.
   - Firmware exhaustion is the §9.2 verdict loss plus no ACK.
   - A later success clears `nvm_stale` and never clears `nvm_alarm`.
   - The lane-2 negative control targets `nvm_alarm`.
   - Cross-reference FASTCONNECT §9.2 on all four pages.

**Taken suggestion:** R380-2 S1 (the BACKOFF time base and product value in 5.1).

Do not edit or delete any existing comment.

**Gates:** as in round 2, all rc 0 at the committed head. Also re-run both reviewers' `finding_evidence` checks from their packets.
