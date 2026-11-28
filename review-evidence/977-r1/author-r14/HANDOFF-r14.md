# #977 round 14 handoff

**Status (2026-11-28 08:50 CET):** REVIEW READY at `a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35`, with tsn-c-stack `5a07d9b7` and lwSRP `e27b34c9`, both unchanged. The tree is clean, and nothing is pushed or posted. Every gate passes, and every product ELF is byte-identical to 25ff0632's (80 of 80).
**ETA:** done. Next: the manager publishes REVIEW-READY.md, PR-BODY.md and receipts/.

## Commit past 4461d77c

- `a5b19f70` cites the owner's decision for the 0.79 ceiling in place of "owner decision pending".
  - Markdown links it ([#977, comment 7235670586](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7235670586)): FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY section 13.
  - Source comments say "#977, the owner's decision of 2026-11-28 on the 8x8/1if load ceiling": flip_grade.py's docstring and FLIP comment, and load_grade.py's ceiling history.

## Log

- 08:02 resumed at 4461d77c (tree clean; no helper units). Read the owner decision (7235670586) and R958-5 (7231383395, NEGATIVE: F1 retained until the owner answers; R1 the PR summary's publication wording).
- 08:03 a5b19f70: no "decision pending" remains in tb/, docs/ or sw/, and no comment ID appears in Python sources. load --check PASS, --selftest 32/32, load_deliveries every control refused; flip --check at 1x1/1if and 8x8/1if PASS, --selftest 628/628. `git diff --check` is clean against 71bad8c0 and 0b594023.
- 08:03 started r14-elf and r14-gates. /data had 22G free.
- 08:04 rm (logged before it runs): `rm -r $VALIDATION_STORAGE/977-a825/r11/oA` frees 4.4G. It is round 11's ELF output set, scratch only, and its identity receipt is in round11/receipts. This keeps /data over 15G while r14-elf writes about 4.4G.
- 08:17 r14-elf done: plat_ledger PASS, 80 ELFs, every sha256 identical to 25ff0632's.
- 08:48 r14-gates done: harness self-tests all rc 0; the idiom gates pass; the docs workflow passes 100 of 100 with no tracked file changed.
- 08:50 receipts copied, host paths replaced, the run.py log gzipped and the index generated. REVIEW-READY.md and PR-BODY.md written. Scratch r14/cE, cG and oF are left in place.
- 08:51 /data had 12G free after the round's builds, under the 15G floor. rm (logged before it runs): `rm -r $VALIDATION_STORAGE/977-a825/r11/oB` and `rm -r $VALIDATION_STORAGE/977-a825/r12/oF`. Both are scratch ELF output sets (rounds 11 and 12) whose identity receipts are in their packets.
- 08:51 /data back to 21G free.
