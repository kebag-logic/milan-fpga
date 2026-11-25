[A849]

Read an ENTITY_DISCOVER whose control_data_length is above 56

Closes #37.

## What

`adp_rx` discarded any ENTITY_DISCOVER whose `control_data_length` was not exactly 56. It now discards a length below 56, counted in `discarded` as before, and reads a longer PDU by its first 56 octets after `entity_id`. The surplus is ignored, whether or not the buffer holds it. The frame must still hold 14 + 12 + 56 = 82 octets. The core still sends 56, and no other ADP path changes: `src/` differs by that one comparison (`!=` to `<`) and one tracing comment.

## Why

- IEEE 1722.1-2021 6.2.2.6 says the field "is set to 56". That fixes what a sender writes. 6.2.7.1.3 sets rcvdDiscover on an ADPDU with message_type ENTITY_DISCOVER, with no condition on its length.
- Milan v1.2 5.6.3.1 gives one reason to discard an ENTITY_DISCOVER: an entity_id that is neither 0 nor the device's own. Table 5.50 defines RCV_ADP_DISCOVER by the entity_id alone.
- IEEE 1722-2016 4.4.5.4 defines the field as the payload's length in octets. No receive rule there discards a longer PDU.
- The project already tolerates lengths it does not need. Milan v1.2 5.5.2.2 has a device accept the truncated ACMP PDU and lets it accept the longer one, and IEEE 1722.1-2021 7.4.37.1 has an entity accept REGISTER_UNSOLICITED_NOTIFICATION with or without its flags field. ACMP receive in this stack checks a minimum length only.

None of these clauses requires a receiver to accept a longer ADPDU. They give no ground to refuse one.

## Documents

ADP-01 reads "A control_data_length below 56 is discarded; a longer PDU is read by its first 56 octets." `REQUIREMENTS.md`, `PORTING.md`, `VERIFICATION.md` (plant count, RV32 control) and the change log follow. The ADP input validation section states that issue 37 replaced the exact-length rule of issue 3, and the change log links issue 37. `TRACEABILITY.md` and `TESTS.md` are regenerated.

## Tests

`RejectsWrongControlDataLength` becomes three tests, each run in all five receive states, with valid_time 0 and 31:

- `RejectsShortControlDataLength`: every length from 0 to 55, for both accepted targets.
- `AcceptsLongControlDataLength`: every length from 57 to 2047 with the surplus absent, in an allocation of exactly 82 octets; 57, 84 and 2047 with the surplus present, in an allocation of their own. Both accepted targets. The five instances fail on the previous core.
- `ReadsNoOctetPastTheFrame`: every length from 0 to 2047, for both accepted targets and a foreign one, in a frame whose last octet is the last before a protected page. The frames are read in a child process, so a read past the frame fails a named assertion in every build. An address-sanitizer build also reports it in the accept test.

Eleven planted defects replace one: the check removed, the bound one too low, valid_time counted as length, the previous exact comparison, the surplus required in the buffer, 56 itself refused, the field read through 0x03FF, 0x01FF, 0x00FF and 0x007F, and a read of the octet past the frame when the length exceeds 56. `ValidDiscovery` keeps its checks, now in a helper the accept test shares.

The RV32 smoke checks accept a length of 256 in every receive state. They fail with the exact comparison restored, with the mask narrowed to 0x00FF, and with the check removed.

## Validation

- Linux: `validate.py --graphs` rc 0, all 28 steps, on a clean clone. 489 of 489 plants caught (479 before). Lines and branches 100 % after the existing exclusions; in `adp_rx` every line runs and the changed comparison takes both outcomes.
- RV32: `baremetal.py` rc 0, Debug and Release.
- Merging this head into `dev-linux`, and into `main`, gives this head's tree.
