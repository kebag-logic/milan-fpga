RULING = '[ruling of 2026-11-17](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6950343235)'
R = [
# H1
f'''Three images may plan past the budget, each only as its own point (#665 rulings 6412739248, 6425357821 and 6505997821, the owner's [decision of 2026-11-12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6824896581), and the owner's rule of 2026-11-15 as [#923's ruling of 2026-11-16](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024) applies it, which #665's {RULING} keeps for the composed flip train: the control memory's ROM may overflow as debt owed to S14).
Two are 8x8 with two interfaces; the third, the target platform's 8x8 image with one interface, is a product image, a shipping one. [Section 5](#5-fit) ledgers all three as owed to lane S14:
''',
# H2
'''| `8x8-two-interfaces` | the size fixture's | `nvm_stage` of 13,594 B, `image_allocation` of 16 B | 60.0 |
| `platform-8x8-two-interfaces` | the target platform's | `nvm_stage` of 13,594 B, `ctrl_plat` of 20,672 B | 62.0 |
| `platform-8x8-one-interface` | the target platform's, one interface | `nvm_stage` of 13,594 B, `ctrl_plat` of 18,496 B | 57.5 |
''',
# H3: ours, then theirs' #923 lines, then the composed train's measurement
'OURS3+',
# H4
'''A point's own measurement names its override, through `ctrl_memory.py plan --ledgered-point`, `ctrl_srp_image.py --ledgered-point` or `ctrl_plat_image.py --ledgered-point`.
The product SoC build plans an image at the entry whose every symbol it carries at its listed size (`ctrl_memory.own_point`, called by `add_ctrl_memory`; #923's ruling of 2026-11-16), and every other image at the budget, so every unledgered product SoC build is still held to 56 RAMB36. `ctrl_plat_image.py` without `--ledgered-point` plans the same way. `plan` itself names no point.
''',
# H5
'''It requires `add_ctrl_memory` to plan each ledgered point's image at its own entry, and `budget` to refuse that image without the override and half a tile past its tiles, directly and through `add_ctrl_memory`; `add_ctrl_memory` also refuses an unledgered 8x8 image at 56.5, one with another `ctrl_plat` and one with none, and the product image half a tile past and with a `ctrl_plat` of another size.
It also plants each override on the same image's other points, on the other overrides' images, and on an 8x8 image carrying one of its two symbols alone, and requires `budget` to refuse each.
''',
# H6
'''Ten planted ledgers each widen one entry to another point or image, or past its tiles.
The platform's two-interface entry loses its staging buffer or `ctrl_plat`, takes the 8x8 one-interface `ctrl_plat`, or plans 62.5.
The fixture's loses `image_allocation`, or plans the platform's 62.0.
The one-interface entry loses `ctrl_plat`, takes the 1x1 one-interface image's symbols or the two-interface `ctrl_plat`, or plans 58.0.
''',
# H7
'''`ctrl_memory.LEDGERED` holds the platform's two-interface entry at 62.0 in the composed flip train (#665), its measured tiles with the map edits' commit (#923) on the train's other changes, 61.5 on the train before the commit, 61.0 since the PHY poll's merge (#919) and at #923's head, 60.5 before them, its cap since SRP's Talker declarations' merge with the tiers (#895), which GET_AS_PATH's read composed on them takes (#897), as AECP's REBOOT on them does (#871), and 60.0 before that; the platform's one-interface entry at 57.5 in the composed train, 57.0 on the train before the commit, 56.5 with the PHY poll (#919) and at #923's head; and the size fixture's at 60.0 in the composed train, 59.5 since GET_AS_PATH's read composed with SRP's Talker declarations (#897), by [the owner's decision of 2026-11-15](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745), and at #923's head, 59.0 before it, its cap since the tiers' merge (#894), and 58.5 before that by the [ruling of 2026-11-12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6831583372) on round 30's STOP (below). Each is refused half a tile past ([section 3](#3-named-refusals)).
''',
# H8
'''**At #895's head, #901's review head `16ba667d`, merged into `dev-soft-core` as `70f4056f`** (its images identical by sha256 to its round 9's `449d29d2`, [section 13](#the-transmits-figure-at-two-interfaces-895)), planned the same way (`ledger.sh` on a clean clone; `plat_ledger.py` passes at every point):
''',
]
H3_TAIL = f'''Since #923 (the map edits' commit through the `EDIT` window, 2,168 B of `rom` at every platform point) each entry is its image's measured tiles, by #923's ruling of 2026-11-16: the owner's rule of 2026-11-15 supersedes the 60.5 cap until S14.
At #923's head the size fixture's was 59.5, the platform's two-interface image's 61.0 with `ctrl_plat` at 20,416 B, and the platform's one-interface image, which was 56.0 with 888 B of `rom` spare, had its own entry at 56.5.
In the composed flip train (#665's {RULING}), measured by `plat_ledger.py` and the CPU budget harness's builds ([section 5](#5-fit)), the size fixture's entry is 60.0: every arm's image needs 129,920 to 130,424 B of `rom`, past the 129,024 B that 59.5 holds.
The platform's two-interface entry is 62.0, with `ctrl_plat` at 20,672 B: 137,888 B of `rom`, 672 B past the 137,216 B that 61.5 holds.
Its one-interface entry is 57.5, with `ctrl_plat` at 18,496 B: 136,304 B of `rom`, 1,136 B past the 135,168 B that 57.0 holds.
Each image is refused half a tile past its entry, at 60.5, 62.5 and 58.0.
'''
