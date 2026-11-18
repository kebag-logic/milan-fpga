**Ruling: the precondition of 1118d item 2.** Decided for the owner under the delegation of 2026-11-11. Not an owner matter.

1. **The stop is resolved: proceed with the record-only re-baseline.** The one release-image FIFO that changed primitives is the render master's frame crossing: 3 RAMB36 become 128 LUTRAMs, and its flops go from 24 to 216. The change is explicit in #927's diff and described in the PR. Both reviews covered it, and the external review's equivalence run covered exactly the distributed branch. The default-branch claim still holds on the TDM capture's crossing, which is unchanged.
2. **Corrected premise.** The distributed-RAM option is not split-only. The render master's crossing is shared, so the release image takes it too. That wording is corrected wherever the train record carries it.
3. **One check, with no new routes.** From the existing routed checkpoints, confirm that the new storage-to-read-register crossing is covered by the crossing's timing exceptions and is clean in the CDC report. This applies to the release image and to both split images. If the reviews already recorded it, cite them. If it is unconstrained or flagged, stop and come back.
4. **Re-baseline.** The composition lane commits the record as measured at the final head: LUT 54,002, FF 55,203, SLICE 15,849, RAMB36 71, RAMB18 27, DSP 15. The composition review covers it.
5. **Debt on #640,** with the attribution:
   - the render crossing: 3 RAMB36 to 128 LUTRAMs, +192 FF;
   - the AAF clock meter: +41 LUT, -18 FF;
   - the EDIT-window claim registers: +96 FF;
   - about +230 LUT of synthesis and placement variation in untouched modules.
6. **S12b continues.** The train candidate starts on the final head once items 3 and 4 are done.
7. **The release image's own bench qualification** stays under its existing gate. This ruling waives nothing there.
