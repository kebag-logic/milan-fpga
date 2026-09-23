[A206] DECISION: the bench switch scopes LeaveAll **per attribute type** (option a). The capture also shows a second cause, on the processor's receive side, that the encoder change alone does not remove.

**Source.**
- The capture is `review-evidence/117-r1/bench-a200/bench/runB/tap-runB.pcap` on the milan-fpga branch `117-review-evidence` (`160debeb`), blob `bf2e79ee`, fetched read-only.
- Every MSRP MRPDU in it was decoded byte by byte: 189 PDUs, 145 from the DUT and 44 from the switch port, none malformed.
- Times below are tap seconds from the first record. The tap stamp is a 64-bit nanosecond count, and its span matches the host clock to 0.03 % over the 114.9 s capture.

**Scope: per attribute type.**
- The DUT's 9 LeaveAll MRPDUs set LeaveAllEvent on the Domain message only.
- After each of them the switch re-declares its Domain within 0.3-3.8 ms, 9 of 9. It sends no other Domain declaration in the capture outside its own LeaveAll PDUs.
- The switch never re-declares its Listener after a DUT LeaveAll. Three DUT LeaveAlls fell while it declared a Listener for the CRF stream (26.839, 37.039, 60.639 s). Each was followed by 0 switch Listener frames within 5 s.
- Two Listener New frames do fall inside a 5 s window, after 13.639 and 47.839 s. They are fresh declarations 12 ms and 40 ms after a PROBE_TX response, not LeaveAll replies.
- A per-participant scope would have re-declared the Listener as well, so prediction part 1 holds.
- The switch's own 9 LeaveAll MRPDUs flag LeaveAll in **every** MSRP message: Listener, Domain, TalkerAdvertise and TalkerFailed, each with LeaveAllEvent 1.
- For a type it declares nothing of toward the DUT, the switch sends a LeaveAll-only VectorAttribute:
  - NumberOfValues 0;
  - an all-zero FirstValue of the full AttributeLength (25, 34 or 8 bytes);
  - no event bytes;
  - AttributeListLength = 2 + AttributeLength + 2 (29, 38 or 12).

  That is the encoding #106 proposes, and it is already on the wire from the switch.

**Prediction part 2: it holds for 3 of 4 bursts and fails for burst 2.**

| burst | last CRF | latest probe + 15 s | latest DUT LeaveAll + 5 s | latest switch LeaveAll + 5 s |
|---|---:|---:|---:|---:|
| 1 | 32.4727 | 32.4737 | 31.8390 | 28.6297 |
| 2 | 52.0289 | 48.5781 | **52.8391** | **52.0296** |
| 3 | 67.6051 | 67.6066 | 65.6391 | 62.8297 |
| 4 (after unbind) | 82.7513 | 82.7524 | 80.4391 | 75.6305 |

- Bursts 1, 3 and 4 end at probe + 15 s, within one 2 ms CRF period.
- Burst 2 ends 0.81 s **before** the predicted later-of. It ends 5.000 s after the **switch's** LeaveAll MRPDU at 47.0296.

**Why burst 2 ends early: the processor's receive side.**
- The switch PDU at 47.0296 is, in order: `[Listener LA=1 n=1 JoinMt/Ready] [Domain LA=1 n=2] [TalkerAdvertise LA=1 n=0] [TalkerFailed LA=1 n=0]`.
- `KL_srp_decoder.sv:383` strobes `la_msrp_o` at **every** VectorHeader with LeaveAllEvent set, so this one PDU makes four rLA! strobes.
- In `KL_srp_talker_fsm.sv`, the Listener JoinMt sets the CRF source's registrar to IN (`:675`). The next strobe, from the Domain message, moves it back to LV and arms T-MRP-LEAVE (`:684`).
- The switch sends no Listener frame between 47.03 and 52.04 s, so the registrar ages to MT at 52.03. The probe window had already closed at 48.58, so the gate closed.
- The same re-aging follows every switch LeaveAll (23.63, 36.83, 57.83, 70.63 s). In bursts 1 and 3 the probe window outlasted it.
- The #530 harness bridge carried its LeaveAll on its single Listener vector, which is why the simulation could not show this.
- `hdl/srp` is identical between the parent's pin `424c688f` and this base.

**What the encoder change alone leaves.**
- The switch's leavealltimer restarts on each DUT LeaveAll: its own LeaveAll lands 9.99 s after every DUT LeaveAll (9 of 9).
- The DUT's timer does not restart on a received LeaveAll. `KL_srp_top` re-draws 10-15 s only at its own expiry, and the flag rides the next 200 ms join tick.
- With LeaveAll flagged on the Listener type, a DUT LeaveAll brings the switch's Listener re-declaration. Every switch LeaveAll still re-ages the registration for 5 s, though. That window is closed only if the DUT's next LeaveAll, plus the switch's reply, lands within 14.99 s of the previous DUT LeaveAll.
- A 15.0 s interval misses that deadline by about 10 ms, and the 10-15 s draw on the 200 ms grid allows one. If the draw is uniform, that is about 2 % of cycles, or roughly one self-ended burst every 10 minutes. This is arithmetic, not a measurement.
- #106 is therefore **necessary but not sufficient** for #530's silicon acceptance.

**Decision.**
- Proceed with #106 as scoped. The encoder will flag LeaveAll in a message of every attribute type the MSRP participant registers, with a NumberOfValues 0 vector where it declares nothing of that type. The MRP state machines stay unchanged.
- The receive-side change is **not** made here. That change would apply a received LeaveAll only to the registrars of the flagged type, or at most once per MRPDU ahead of its attribute events.
- It reverses the documented per-application receive routing (10 §6.5, `KL_srp_top` banner), so it is an interpretation decision for the owner. It should land before the #530 silicon rerun is judged.
- The decode script, its output and the SHA-256 of every input are in the review packet.
