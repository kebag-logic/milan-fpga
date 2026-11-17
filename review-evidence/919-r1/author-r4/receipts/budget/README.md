The CPU budget's PHY figures at 1a1e6665, 1x1/1if and 8x8/1if.

The CPU service budget harness composes no platform, so ctrl_plat_phy.c is not in its image.
`harness-image-identity-1a1e6665.txt` links the harness's firmware image from the head's tree with this round's
split boot builds' flash maps and runtime archives: both shapes give round 2's harness build's and the base's
(70f4056f) ctrl_app.elf byte for byte (1x1/1if `10684d74...`, 8x8/1if `2cf4e51a...`). Its testbench and RTL are
unchanged (`../head/files-changed.txt`), so round 2's verdict stands: 1x1/1if rc 0, 0 of 130,341 passes over the
2 ms share, 7 misses (the base's backlog-owed rows); 8x8/1if rc 1 on 11 stated-cost lines (the base's), 0 of
270,769 passes over the share, the same 7 rows.

The PHY's cost is THE STEP's, measured by the split boot simulation (`../boot/`): at most 14,537 CPU cycles
(145.37 us) at 1x1/1if and 14,545 (145.45 us) at 8x8/1if, against the stated 155 us, unchanged by THE OUTCOME (it
adds no frame; a restart's poll takes its second BMSR read, one of the poll's nine reads).
