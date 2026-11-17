The measurements behind da8a8b84's restated figures, taken on a clean clone of c79f1c76 (the code head; da8a8b84
adds comments, docs and two ledger reason strings, and every platform image is byte-identical at both:
`rom-banking.txt`).

- `plat-ledger-self-test-c79f1c76.log`: the four platform points (rom 119,436 / 121,020 / 132,140 / 133,708 B;
  43.5 / 44.5 / 56.5 / 61.0 RAMB36; ctrl_plat 17,600 / 19,136 / 18,240 / 20,416 B) and 8 of 8 controls.
- `boot-1x1-c79f1c76.log`, `boot-8x8-c79f1c76.log`: the frame's cost, 145.37 and 145.45 us at most.
- `rom-per-file.txt`: per object, base 70f4056f -> c79f1c76, and round 3's own share, afa3ea19 -> c79f1c76:
  `ctrl_plat_phy.o` 1,883 -> 1,875 B, nothing else.
- `rom-banking.txt`: every point's ROM and SRAM banks at afa3ea19 and da8a8b84, unchanged, so no route was repeated.
- `fw-coverage-check-c79f1c76.log`: `fw_coverage.py --check`, `ctrl_plat_phy.c 172/172 158/158`, PASS (40 files);
  the same at da8a8b84 in the firmware-unit job (`../workflows/logs/rtl-fast__firmware-unit__ci_step_12.log`).
