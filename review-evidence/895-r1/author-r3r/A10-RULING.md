[A10] **Ruling on round 3's STOP (8x8/2if ROM cap).** This is a maintainer-delegated decision, applying the #894 ruling 6844175391.

- **The lever is the names patch that ruling already assigned.** It recovers 1,048 B of rom, against the 956 B needed by the worst arm (`answering-every-port`).
- **#895 carries it now, as its own commit, unchanged.** #810 is in its candidate bank, so the patch can't go there without restarting that bank. Whichever of #901 and #902 merges first lands it, and the other takes it by merge.
- **Re-link every 8x8/2if image at the head:** the fixture and both harness arms. Each must be at most 58.5.
- **If any of them is still over 58.5, use the ruling's fallback:** cap 59.0 at 8x8/2if only, for the fixture and both harness arms, recorded in the ledger as debt for S14. This is 2if-only, which the owner made optional on 11-13. Every other point and the platform cap of 60.5 stay as they are.
- **The two srptx findings are not #905's.** Each gets its own issue: `[TIME]` already fails at #810's head, and the hold `[TX]` full-ring path is no longer exercised. Don't fix either in this round. Grade `[SID]` on its own words, and record the `[TIME]` findings as pre-existing with the issue number.
- **Then finish round 3 as assigned:** acceptance 4 re-measured on the head's own legs, the gates, the full pass once, and REVIEW READY.
