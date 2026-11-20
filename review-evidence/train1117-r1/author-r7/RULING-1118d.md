**Ruling: the release image's LUT growth at step 11.** Decided for the owner under the delegation of 2026-11-11. Not an owner matter.

1. **Accept and re-baseline.** The release image fits and meets #818's floor (+0.194 / +0.017), and its slices are unchanged. The +541 LUT growth (about +400 from #927, +110 from the train before it) follows three owner-accepted re-baselines of the same kind. It moves no owner bound and is reversible. Gating #927's release-visible RTL off would put the Thursday date at risk to save about 400 LUTs, so that option is rejected.
2. **Precondition: explain the release image's delta by hierarchy,** from the existing routed checkpoints, before the re-baseline. If it is the AAF clock meter, or another reviewed and intended change, proceed. If any release FIFO instance changed primitives, stop: that contradicts the review and is a behaviour question.
3. **Ownership.** The composition lane authors the re-baseline commit at the train's final head. It touches the record only (LUT, FF and RAMB36 at the route endpoint), with no RTL or firmware. The composition review covers it.
4. **Debt.** The growth and its attribution are recorded on #640. This is not a floor exception.
5. **S12b may proceed on the current head.** It benches the split images, which a record-only commit does not change, so the result carries by byte identity.
6. **The train candidate waits for the re-baseline commit** and runs on the final head.
7. **The owner** is informed; no decision is needed.
