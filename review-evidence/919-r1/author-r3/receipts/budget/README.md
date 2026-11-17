The CPU budget's PHY figures at da8a8b84, 1x1/1if and 8x8/1if.

The CPU service budget harness composes no platform, so `ctrl_plat_phy.c` is not in its image.
`harness-image-identity-da8a8b84.txt` links the harness's firmware image from the head's tree, with this round's
split boot builds' flash maps and runtime archives (`ctrl_srp_image.py --interfaces 1 --with-aecp --layout split`).
Both shapes give round 2's harness build's and the base's (dev-soft-core 70f4056f) `ctrl_app.elf` byte for byte:
1x1/1if `10684d74...`, 8x8/1if `2cf4e51a...`. The harness's testbench and RTL have no diff from afa3ea19
(`../head/files-changed.txt`), and none from the base (round 2's identity receipt). So the harness at this head
measures the base's image on the base's testbench, and round 2's verdict stands, unchanged:
- 1x1/1if rc 0: 96 groups, 0 refusals, 0 of 130,341 passes over the 2 ms share, 7 misses (the `backlog-owed`
  held-egress rows, the base's ruled rows);
- 8x8/1if rc 1 on 11 stated-cost lines, the base's (#920 issuecomment-6908928237): 95 groups, 0 refusals, 0 of
  270,769 passes over the share, the same 7 rows.

The PHY's place in the pass is THE STEP's: at most one frame a call, taken only with `CTRL_PLAT_PHY_STEP_US` of the
share left, and none beside a save's step. Its cost is measured by the split boot simulation on the platform image
(`../boot/boot-1x1-da8a8b84.log`, `../boot/boot-8x8-da8a8b84.log`):
- 1x1/1if: 59 frames, the longest 14,537 CPU cycles, 145.37 us;
- 8x8/1if: 59 frames, the longest 14,545 CPU cycles, 145.45 us;
against the stated 155 us, which the rule (the most measured + 5 %, rounded up to 5 us: 152.7 -> 155) restates
unchanged.
