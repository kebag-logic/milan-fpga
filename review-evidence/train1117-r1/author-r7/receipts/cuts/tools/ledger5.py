#!/usr/bin/env python3
"""ledger5.py TREE: restate the platform's ledger entries at step 10's final tip to its measured images (plat_ledger.py
at 41d2bc2b, whose images 6448e431 links unchanged): ctrl_plat 18,048 B at 1x1/1if and 21,568 B at 8x8/2if (#936's 64 B,
which the merge composes), and the 8x8 one-interface entry 58.0 (137,472 B of rom, 256 B past the 137,216 B 57.5
holds), S14 debt by the owner's rule of 2026-11-15. Exact anchors; each must match once."""
import sys
from pathlib import Path

T = Path(sys.argv[1])


def edit(rel, pairs):
    p = T / rel
    s = p.read_text()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f'{rel}: {n} matches for {old[:80]!r}'
        s = s.replace(old, new)
    p.write_text(s)


CUT = "the largest legal record's cut and the hot list relearned on it"

edit('sw/litex/ctrl_memory_ledger.py', [
    ("target platform's 8x8 image with one interface, a product image, at 57.5 (56.5 with the PHY poll, 57.0 on the composed\n"
     "train, 57.5 with the commit); each is refused half a tile past.",
     "target platform's 8x8 image with one interface, a product image, at 58.0 (56.5 with the PHY poll, 57.0 on the composed\n"
     f"train, 57.5 with the commit, 58.0 with {CUT}); each is refused half a tile past."),
    ("PLAT_1X1_1, PLAT_1X1_2, PLAT_8X8_1, PLAT_8X8_2 = 17_984, 19_712, 18_944, 21_504",
     "PLAT_1X1_1, PLAT_1X1_2, PLAT_8X8_1, PLAT_8X8_2 = 18_048, 19_712, 18_944, 21_568"),
    ("PRODUCT: Case(STAGE_8X8, None, PLAT_8X8_1, 57.5)}", "PRODUCT: Case(STAGE_8X8, None, PLAT_8X8_1, 58.0)}"),
    ('("ctrl_plat", PLAT_8X8_1)), 57.5)}', '("ctrl_plat", PLAT_8X8_1)), 58.0)}'),
    ('("its own image at 58.0 RAMB36, half a tile past its 57.5", PRODUCT, OWN[PRODUCT]._replace(tiles=58.0)),\n'
     '    ("the platform\'s 1x1 one-interface image at 57.5", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_1, 57.5)),\n'
     '    ("the platform\'s 1x1 two-interface image at 57.5", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_2, 57.5)),\n'
     '    ("the platform\'s 8x8 two-interface image at 57.5", PRODUCT, OWN[PLATFORM]._replace(tiles=57.5)),\n'
     '    ("an image with the point\'s ctrl_plat and the 1x1 stage at 57.5", PRODUCT,\n'
     '     Case(STAGE_1X1, None, PLAT_8X8_1, 57.5)),\n'
     '    ("an 8x8 image with no ctrl_plat at 57.5", PRODUCT, Case(STAGE_8X8, None, None, 57.5)),\n'
     '    ("the size fixture\'s 8x8 one-interface image at 57.5", PRODUCT, Case(STAGE_8X8, 1, None, 57.5)),',
     '("its own image at 58.5 RAMB36, half a tile past its 58.0", PRODUCT, OWN[PRODUCT]._replace(tiles=58.5)),\n'
     '    ("the platform\'s 1x1 one-interface image at 58.0", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_1, 58.0)),\n'
     '    ("the platform\'s 1x1 two-interface image at 58.0", PRODUCT, Case(STAGE_1X1, None, PLAT_1X1_2, 58.0)),\n'
     '    ("the platform\'s 8x8 two-interface image at 58.0", PRODUCT, OWN[PLATFORM]._replace(tiles=58.0)),\n'
     '    ("an image with the point\'s ctrl_plat and the 1x1 stage at 58.0", PRODUCT,\n'
     '     Case(STAGE_1X1, None, PLAT_8X8_1, 58.0)),\n'
     '    ("an 8x8 image with no ctrl_plat at 58.0", PRODUCT, Case(STAGE_8X8, None, None, 58.0)),\n'
     '    ("the size fixture\'s 8x8 one-interface image at 58.0", PRODUCT, Case(STAGE_8X8, 1, None, 58.0)),'),
    ('("the product entry at 58.0 RAMB36", PRODUCT, {"tiles": 58.0}),',
     '("the product entry at 58.5 RAMB36", PRODUCT, {"tiles": 58.5}),'),
])

edit('sw/litex/ctrl_memory.py', [
    ("#: 58.0, its entry at 57.5 by the same rule: 56.5 with #895's declarations and the PHY poll (#919), 57.0 on the\n"
     "#: composed train before the commit, 57.5 with it. The platform's image is linked at\n",
     "#: 58.5, its entry at 58.0 by the same rule: 56.5 with #895's declarations and the PHY poll (#919), 57.0 on the\n"
     "#: composed train before the commit, 57.5 with it, 58.0 with the largest legal record's cut and the hot list relearned\n"
     "#: on it (#665). The platform's image is linked at\n"),
    ('((STAGE_SYMBOL, 13_594), ("ctrl_plat", 21_504)), 62.5,', '((STAGE_SYMBOL, 13_594), ("ctrl_plat", 21_568)), 62.5,'),
    ('"rule: debt of 6.5 RAMB36 owed to S14"),',
     '"rule: debt of 6.5 RAMB36 owed to S14; ctrl_plat 64 B more with SRP\'s "\n'
     '                                            "record of the STREAM_OUTPUT notices (#936) on that train, 21,568 B, "\n'
     '                                            "and with the largest legal record\'s cut and the hot list relearned "\n'
     '                                            "on it (#665) its rom 139,048 B, within the 62.5"),'),
    ('((STAGE_SYMBOL, 13_594), ("ctrl_plat", 18_944)), 57.5,', '((STAGE_SYMBOL, 13_594), ("ctrl_plat", 18_944)), 58.0,'),
    ('"ctrl_plat at its measured 18,944 B"),',
     '"ctrl_plat at its measured 18,944 B; 58.0 with the largest legal "\n'
     '                                           "record\'s cut and the hot list relearned on it on that train with "\n'
     '                                           "#936 (#665), 137,472 B of rom, 256 B past the 137,216 B 57.5 holds, "\n'
     '                                           "by the same rule: ROM debt of 2.0 RAMB36 owed to S14"),'),
])

edit('sw/litex/test_ctrl_memory.py', [
    ("interfaces and the platform's 8x8 image with one) plans its 60.5, 62.5 or 57.5 by name, and through",
     "interfaces and the platform's 8x8 image with one) plans its 60.5, 62.5 or 58.0 by name, and through"),
    ('f"platform\'s 8x8 image with one at 57.5 ({held})")', 'f"platform\'s 8x8 image with one at 58.0 ({held})")'),
])

edit('tb/verilator/ctrl_split_boot/README.md', [])
readme = T / 'tb/verilator/ctrl_split_boot/README.md'
s = readme.read_text()
line = next(l for l in s.splitlines() if l.startswith('The 8x8 image with two interfaces plans 62.5 RAMB36 in the composed flip train (#665).'))
assert line.count('57.5,') == 1, line
readme.write_text(s.replace(line, line.replace('57.5,', f"58.0 with {CUT}, 57.5 before them,")))

D = 'docs/design/SPLIT_CONTROL_MEMORY.md'
edit(D, [
    ("| `platform-8x8-two-interfaces` | the target platform's | `nvm_stage` of 13,594 B, `ctrl_plat` of 21,504 B | 62.5 |",
     "| `platform-8x8-two-interfaces` | the target platform's | `nvm_stage` of 13,594 B, `ctrl_plat` of 21,568 B | 62.5 |"),
    ("| `platform-8x8-one-interface` | the target platform's, one interface | `nvm_stage` of 13,594 B, `ctrl_plat` of 18,944 B | 57.5 |",
     "| `platform-8x8-one-interface` | the target platform's, one interface | `nvm_stage` of 13,594 B, `ctrl_plat` of 18,944 B | 58.0 |"),
    ("The platform's two-interface entry is 62.5, with `ctrl_plat` at 21,504 B: its",
     "The platform's two-interface entry is 62.5, with `ctrl_plat` at 21,568 B since #936 (21,504 B before it): its"),
    ("Its one-interface entry is 57.5, with `ctrl_plat` at 18,944 B and 136,984 B of `rom`",
     f"Its one-interface entry is 58.0 with {CUT} on the train with #936, 137,472 B of `rom`, 256 B past the "
     "137,216 B that 57.5 holds; it is 57.5 before them, with `ctrl_plat` at 18,944 B and 136,984 B of `rom`"),
    ("Each image is refused half a tile past its entry, at 61.0, 63.0 and 58.0.",
     "Each image is refused half a tile past its entry, at 61.0, 63.0 and 58.5."),
    ("- the target platform's 8x8 image with one interface, a product image, 57.5, a debt of 1.5, 6,144 B, its own entry",
     "- the target platform's 8x8 image with one interface, a product image, 58.0, a debt of 2.0, 8,192 B, its own entry"),
])
d = T / D
s = d.read_text()
anchor = next(l for l in s.splitlines() if l.startswith("The platform's 8x8 image with two interfaces holds 131,976 B of `rom` in 133,120"))
add = ("\n\n**At the composed train's tenth step on #936's final head** (#944's frozen head `d1aa4c44` merged on the ninth, "
       f"with {CUT}, #665's [ruling of 2026-11-18](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6967930396)), "
       "planned the same way:\n\n"
       "| Point | Platform `rom` / `sram` need, B | Platform RAMB36 | Platform `ctrl_plat`, B | Against its limit |\n"
       "|---|---:|---:|---:|---|\n"
       "| 1x1, one interface (shipping) | 124,832 / 56,736 | 44.5 | 18,048 | within 56 |\n"
       "| 1x1, two interfaces | 126,432 / 59,040 | 45.5 | 19,712 | within 56 |\n"
       "| 8x8, one interface (shipping) | 137,472 / 98,096 | 58.0 | 18,944 | at its entry's 58.0, S14's debt, 1,792 B of `rom` left |\n"
       "| 8x8, two interfaces (largest) | 139,048 / 115,504 | 62.5 | 21,568 | at its entry's 62.5, S14's debt, 216 B of `rom` left |\n\n"
       "#936 adds 64 B of `ctrl_plat` at 1x1 with one interface and at 8x8 with two. The 8x8 one-interface image needs 256 B "
       "past the 137,216 B that 57.5 holds, so its entry is 58.0 as debt owed to S14 by the owner's rule of 2026-11-15. "
       "The size fixture's 8x8 image with two interfaces needs 130,952 to 131,448 B of `rom` over the harness's six arms "
       "(114,320 to 114,384 B of `sram`), within its 60.5.")
assert s.count(anchor) == 1
d.write_text(s.replace(anchor, anchor + add))
print('ok')
