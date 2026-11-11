[A761c] REVIEW READY
Commit: 6171d65473875239d97e6f6b9327c394db65aab8 (branch `665-s11-aecp-reboot`, one commit on round 2's `d08d30c6ec`; not pushed)

Changed (round 3, under the ruling issuecomment-6806697914 on R821-2 F1 and R822-2 F1). Only tests, the two mutant tables and two documents changed; no firmware behaviour changed, because no test exposed a channel the gate misses:
- Every channel's receive is refused from the SUCCESS, each named. The host test `NoFrameOfAnyChannelIsTakenFromTheSuccess` sends an ENTITY_DISCOVER, a BIND_RX, an AEM command, a MAAP PROBE for the entity's own range and an MSRP PDU after the SUCCESS, and checks each channel's `RX_TAIL` by name.
- From the SUCCESS's own cycle: new `B22TheGateHoldsInThePassThatTakesTheReboot` (a MAAP PROBE, an MSRP PDU and a second AEM command queued with the REBOOT are not taken in the pass that takes it) and `B23TheGateHoldsWhileTheResponseCannotBeHandedOver` (AECP's transmit ring full: a frame on each of the five channels stays in its ring). The AECP core test requires `aecp_reboot_accepted` straight after `aecp_rx`, before any poll.
- Nothing but ADP's DEPARTING after the DEPARTING: `NoOtherChannelTransmitsAfterTheDeparting` checks ACMP, AECP, MAAP and SRP by name. `TheDepartingWaitsForEveryOtherRing` holds the ACMP, MAAP and SRP rings in turn. AECP's ring then holds only the REBOOT's own frames, which `aecp_reboot_due` waits for (B12).
- Planted defects, each caught on its own words: the receive gate open on one channel for each of the five (AECP's opens both layers, since AECP refuses a command from its SUCCESS on its own too); the DEPARTING's wait skipping each of the ACMP, MAAP and SRP rings; acceptance only at the handover, in the platform table and in the AECP table. The whole-gate, loop-on and whole-wait defects now require the per-channel words.
- Docs: `REBOOT_RESET.md` section 8's evidence rows and the platform README state what the tests prove (62 platform defects, 22 REBOOT; AECP 14 REBOOT). The comment lines this round rewrote name the tests, not bench labels.

Validation (each on a fresh clean clone of `6171d654`, the ruling's gates):
- `test_ctrl_firmware.py --require-rv32 --self-test`: PASS, control campaign 592 of 592.
- `aecp_mutants.py`: 153 of 153.
- `tb/verilator/ctrl_reboot/run.py --self-test`, no seed in the environment: PASS, 12 of 12 plants and controls.
- `docs.yml`: 64 `run:` steps rc 0, 31 not run with reasons, 0 bad.
- `git diff --check` against the merge base: clean.
- The reviewers' verification probes at `6171d654`, scripts unchanged:
  - R821-2 `probe_plat.py`: `head` passes; `gate-skips-maap-and-srp` and `gate-from-the-handover` each give platboot1 rc 1 on REBOOT words.
  - R821-2 `probe_aecp.py`: `head` passes; `handover` fails on "accepted at its SUCCESS, before any poll hands its frames over".
  - R822-2 `r822_probes.py`: `clean` passes; `gate-skips-maap-and-srp` and `depart-ignores-maap-and-srp-rings` each give platboot1 rc 1.
- Round 2's full pass (every workflow step, the sweep, S2, the builder, behave, coverage) at `d08d30c6ec` stands for the rest: the round 3 delta touches only the two host test files, the two mutant tables, `REBOOT_RESET.md` and the platform README.

Acceptance criteria: items 2 to 5 met; item 1 met for six of the eight items and the binding, so the PR still says Relates to #871, as ruled.

Open risks/questions:
- Not taken, as the ruling lists only the above: R822-2 R2 (the wording of when ADP's poll runs, in three documents), the suggestions of both reviews, and R822-2 R1 beyond the comment lines this round rewrote.
- Still pending from round 2: the decision on R821 S4 (a 0 tie adds one line to the all-fabric top `.v`), and a new issue for the split boot simulation's unpinned hash seed.
