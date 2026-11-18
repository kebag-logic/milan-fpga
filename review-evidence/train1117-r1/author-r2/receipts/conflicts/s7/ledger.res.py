R = [
'''`ctrl_memory.LEDGERED` lets three images plan past the 56-RAMB36 budget, each only as its own point, under #665's
documented memory exceptions and the owner's rule of 2026-11-15 (#923's ruling of 2026-11-16): at 8x8 with two
interfaces the size fixture's at 59.5 RAMB36 (59.0 before GET_AS_PATH's read composed with SRP's Talker declarations,
#897) and the target platform's at 61.0 (60.5, the owner's decision's cap of 2026-11-12, with SRP's Talker
declarations, #895, AECP's REBOOT, #871, and the saved-state store's name marks, #920, then 61.0 with the PHY poll and
its advertisement, #919), and the target platform's 8x8 image with one interface, a product image, at 56.5; each is
refused half a tile past. A measurement names its point, and the product SoC build plans an image at the point whose
symbols it carries (`ctrl_memory.own_point`; #665's ruling of 2026-11-17 keeps it for the composed train). A `Case`
here is what the ledger reads of one image. test_ctrl_memory.py writes each as an ELF, through the `write` callable every
''',
'theirs',
'''PLAT_1X1_1, PLAT_1X1_2, PLAT_8X8_1, PLAT_8X8_2 = 17_664, 19_200, 18_304, 20_480
''',
'theirs',
'theirs',
'''     Case(STAGE_8X8, 1, None, 59.5)),
    ("the platform's 8x8 two-interface image, a name the ledger does not hold", "platform-1x1-one-interface",
     OWN[PLATFORM]),
    ("the platform's 1x1 one-interface image, a name the ledger does not hold", "platform-1x1-one-interface",
     Case(STAGE_1X1, None, PLAT_1X1_1, 56.5)),
''',
'theirs',
'''             ("the size fixture's entry at the platform's 61.0", FIXTURE, {"tiles": 61.0}),
             ("the product entry without ctrl_plat", PRODUCT, {"symbols": (stage,)}),
             ("the product entry at the 1x1 one-interface ctrl_plat and stage", PRODUCT,
              {"symbols": ((ctrl_memory.STAGE_SYMBOL, STAGE_1X1), ("ctrl_plat", PLAT_1X1_1))}),
             ("the product entry at 57.0 RAMB36", PRODUCT, {"tiles": 57.0}),
             ("the product entry at the two-interface ctrl_plat", PRODUCT,
              {"symbols": (stage, ("ctrl_plat", PLAT_8X8_2))}))
''',
]
