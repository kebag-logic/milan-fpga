Found by review R557-1 on PR #1, finding F4. This behaviour is inherited unchanged from milan-fpga dev `6aa25dec`.

In WAITING, `src/adp.c` (around line 308) acts on discovery frames it should discard. Each of these enters DELAY, restarts the timer and leaves `discarded` at zero:
- a frame with AVTP version 1;
- a frame truncated to 26 bytes;
- a full frame with `control_data_length` 0.

The receiver checks only the minimum bytes it reads, the EtherType, the subtype, the message nibble and the target.

**Acceptance:**
1. The ADP receive path refuses each malformed or unsupported input by clause: the AVTP version, the minimum frame length and the `control_data_length` required for ADPDUs (IEEE 1722.1-2021 clause 6.2; IEEE 1722-2016 header rules). It counts the refusal in `discarded`, with no state change.
2. A test and a planted defect for each of the three inputs, plus the valid control.
3. `docs/REQUIREMENTS.md` (ADP-01), `docs/PORTING.md` and `docs/DEVIATIONS.md` are updated. The deviation that PR #1 records is removed.
4. milan-fpga picks up the fix through its consumer of this repository (kebag-logic/milan-fpga#697).

