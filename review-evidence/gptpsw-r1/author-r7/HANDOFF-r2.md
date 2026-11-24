STATUS: DONE, REVIEW READY. ETA: none (complete 15:31 CET 2026-11-24).

# PR #966 round 2 handoff (R883-4-F1)

Head: `0acf24d9b5060a263f725c02026446dde64c2574`, one local commit on `44c56639`. **Not pushed.** The lane worktree
is clean and one commit ahead of `origin/884-gptp-firmware`.

- Fix (tests only): the AVB test now makes the datapath's bit 0 disagree with the owner's asCapable both ways and
  checks AS_CAPABLE on its own words. The face table gains the unmasked-OR plant
  `face-software-gptp-keeps-datapath-capable`.
- Proof: the leak escapes 44c56639's tests and is caught by the new check alone at `0acf24d9`. The two existing
  face plants are still caught on their own words.
- Gates at `0acf24d9`: coverage `--check` rc 0 with figures unchanged and the ratchet untouched. The four firmware
  shards (`--require-rv32 --self-test`) are rc 0 with 0 escapes, and the AECP campaign in shard 2 includes the new row.
- Manager duties: push, then the hosted gates and act replica at the new head, then a delta re-review of F1.
  R883-4-R1 to R3 and S1 are untouched.

Details: `REVIEW-READY.md`; receipts: `receipts/INDEX.md`; scratch: `/data-2/milan/tmp/opt-a837-r2`.
