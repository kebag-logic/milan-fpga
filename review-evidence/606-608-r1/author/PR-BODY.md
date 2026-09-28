[A412] Relates to #606. Relates to #608.

Adopt processor `c951a9ff`, containing the merged destination-allocation retry
and own-LeaveAll transmit-action fixes. Refresh the pin documentation, generated
boundary diagram and ROM digest records, and add the agreed evidence disposition.

Update pp_shadow H/I for the 100 ms retry round, accepted-request source pairing
and grants counted from MAAP enable. Add parent regressions requiring the first
post-acquisition probe to succeed and the CRF path to stop within one PDU period
while counting each STREAM_STOP. The CRF cases cover ordinary withdrawal, the
own-expiry window and reconnect, preserving the documented LV + rLv behavior.

Validation at `e8bf5e080e4b7d586d0484427ec2ef4fe9c51744`:

- Full builder bank with required RV32 and elaboration checks, parent consumer set, pin records and documentation checks: rc 0. The existing placement-calibration arm is explicitly NOT RUN because its report is absent.
- All four pp_shadow legs: 2,120 checks, zero failures.
- First-probe regression: old pin has 14 failures across 37 checks and returns status 3 for both sources; new pin passes all 37 with status 0.
- CRF withdrawal regression: old pin has six failures across 31 checks, four late frames and a missed stop in the expiry window; new pin passes all 31 with three counted stops and no late frames.
- Capture check: rc 0; the existing measurements remain valid, so no re-measurement was needed.

The old-pin arms ran in an isolated scratch export with identical committed
parent regression sources. Their nonzero exits came from completed behavioral
assertions. No processor source, firmware or interface change is included.

Bench re-measurement follows on the next image, so both issues remain open.
