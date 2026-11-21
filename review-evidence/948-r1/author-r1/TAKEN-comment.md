[A810] TAKEN
Branch: `pf-948-1`, on the flip train's head `15168e14` (PR #945). Once the train merges, the PR's base is `dev-soft-core` and its diff is this lane's commits only.
Authoritative references: the ruling of 2026-11-21 above (fan-out, not refusal); IEEE 1722.1-2021 8.2 (each sink binds on its own); Milan v1.2 5.3.8.10 and Table 5.6 (the counters of each Stream Input), 5.3.8.7 (a stopped input discards).
Interpreted scope: the AVTP receive parser reports every bound table entry a PDU's stream_id matches, as a vector. The shared monitor engine judges and counts that one PDU once for each matched context, from its one queued bundle. The AAF depacketizer stores the frame once, commits it when the engine queues the PDU, and reads it out once for each input that accepted it, so each input has its own counters, clock-meter samples and render path. Nothing is copied per input. With one binding per stream the engine stays cycle-equal to its reference model. No mailbox, firmware or CPU budget bound changes.
Validation plan:
- Failing tests first, each with planted mutants:
  - the receive stack at eight contexts (`avtp_rxmon`): two inputs, then three, bound to one talker stream; unbinding one leaves the others receiving; counters per input;
  - the 8x8 datapath (`milan_dp`);
  - the twin's split half at 8x8/1if. The twin's own shape, 1x1, has one AAF Stream Input.
- Then the RTL suites, the full sweep in four shards, the twin and its plants, the firmware gate, and the CPU budget images (unchanged).
- Fit and timing at 1x1/1if and 8x8/1if: the best of three directives, the floor at every corner, with slice and LUT deltas against the train's gating builds.
Blockers: none. The ruling's STOP applies if 8x8/1if does not fit or does not close timing.
