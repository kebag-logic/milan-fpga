Proposed issue text (for the manager to open; not posted)

Title: The target platform's 8x8/2if image plans 59.5 RAMB36 against its ledgered 59.0, unseen since round 27 because its `ctrl_plat` key was stale

Relates to #665 (S2b, PR #810).

Observed:
- `ctrl_memory.LEDGERED["platform-8x8-two-interfaces"]` ledgers the target platform's 8x8, two-interface image at 59.0 RAMB36 (owner ruling 6505997821), recognised by `nvm_stage` 13,264 B and `ctrl_plat` at its measured size.
- The `ctrl_plat` size the ledger held, 19,968 B, was stale from at least round 27's head `e7e2b744` (measured there 20,096 B), so every link of that image with its override was refused by its key before its tiles were read.
- Linked with the key at its measured size (`ctrl_plat_image.py --ledgered-point platform-8x8-two-interfaces`, the split SoC export of the CPU budget harness's 8x8 build), the image plans 59.5 RAMB36: `rom` 127,544 B at `e7e2b744`, 127,664 B at round 28's `66f71326`, 128,264 B at round 29's composed head (the merge of the tsn-c-stack pin move, `ctrl_plat` 20,288 B), each in 129,024 B of banks, against the 126,976 B the 59.0 plan holds.
- No gate links the platform image with its override: the boundary gate stops at its link on the stand-ins, and `test_ctrl_memory.py` plans synthetic images at the ledger's constants.

Asked:
- A ruling on the platform image's 8x8/2if ledger (59.5, or a cut of at least 1,288 B of its `rom`, or its cold code moved by lane S14 under decision D3).
- A gate that links the platform image at its ledgered point with its override, so a stale key or a tile overrun is refused where it happens.

Receipts: round 29's `receipts/images/` (both images at the four points at the legs' head) and `receipts/merge/` (`ctrl_plat` at the composed build, at `66f71326` and at `e7e2b744`, and the keyed links).
