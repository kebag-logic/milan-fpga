The measurements behind 1a1e6665's restated figures, on clean clones of the code heads.

- `plat-ledger-self-test-8beada76.log`, `boot-1x1-8beada76.log`, `boot-8x8-8beada76.log`: the images and the boot
  at 8beada76, the outcome check's commit; 33041d64 and 1a1e6665 change tests, docs, the ratchet row and two ledger
  reason strings, and every platform image is byte-identical at 8beada76 and 1a1e6665 (ctrl_app.elf sha256).
- `rom-banking.txt`: every point's ROM and SRAM banks at da8a8b84 and 8beada76, unchanged, so no route.
- `rom-per-file.txt`: per object, base 70f4056f -> 8beada76, and round 4's own share: `ctrl_plat_phy.o` 1,875 ->
  1,939 B, nothing else.
- `fw-coverage-check-8beada76-refused.log`: at 8beada76 the ratchet refused 163/164 branches (the counter's
  saturation never reached); `fw-coverage-check-33041d64.log`: with its test, 178/178 and 164/164, PASS. The row
  is ratcheted there at 1a1e6665.
- `phy-plant-subset-33041d64-tree.log`: the campaign's PHY plants alone on the lane tree at 33041d64: 54 of 54 caught
  (its rc 1 is the subset's unnamed-tests check, which the full campaign passes).
