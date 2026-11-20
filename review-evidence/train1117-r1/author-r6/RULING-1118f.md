**Ruling: the CDC check of 1118e item 3.** Decided for the owner under the delegation of 2026-11-11. Not an owner matter. The re-baseline proceeds.

1. **The stop is resolved.** "Flagged" in 1118e item 3 meant unsafe, unknown, Critical or unconstrained. None of those applies to the render crossing:
   - the asynchronous clock groups cover its paths;
   - the report counts 201 of 201 endpoints Safe;
   - there is no CDC-26.
2. **CDC-15 is the expected report here.** The read register loads only when the FIFO is read and not empty, and "empty" comes from the synchronized write pointer. Each entry is therefore stable for at least two read-clock synchronizer stages before it is sampled. This is the same class as the 50 rows the TDM capture's crossing already carries in the shipping release.
3. **No waiver in the train.** A waiver changes build inputs. Waiving one crossing while the other stays unwaived would also be inconsistent.
4. **Train record note, now.** The composition lane records:
   - the 192 new CDC-15 rows, the report summary and the safety argument;
   - that this check closes the limit the internal review stated for this crossing;
   - the corrected premise of 1118e item 2.
5. **#495 residue:**
   - list the render crossing's CDC-15 x192 in the timing findings document, beside the capture crossing's, in the same "not waived or repaired" class;
   - decide after the flip whether both get a waiver that carries the argument;
   - reviews of a change to a CDC structure read the CDC report.
6. **The sequence is unchanged.** The record-only re-baseline commit goes in with the values already given, then the candidate runs on the final head. S12b continues; its 1x1/1if image carries the render crossing, so it is the hardware evidence for it.
