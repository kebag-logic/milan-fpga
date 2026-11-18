R = [
'''#: The only images `plan` may let past BUDGET_TILES. A measurement names its point (`plan --ledgered-point`,
#: ctrl_srp_image.py, ctrl_plat_image.py); the product SoC build (milan_soc.add_ctrl_memory) and the platform image's
#: link without --ledgered-point plan an image at the entry whose symbols it carries (`own_point`, #923's ruling of
#: 2026-11-16, kept for the composed train by #665's ruling of 2026-11-17), so every unledgered image is still held
#: to 56 RAMB36; the measurement harness names the size fixture's for that point only (its image and SoC plan,
#: tb/verilator/ctrl_service_budget/build.py, LEDGERED_POINTS). An image is the point when it carries every listed
#: symbol at its listed size: the 8x8 shape's staging buffer, and the image's own object. The size fixture's is its
#: per-interface table (ctrl_aecp_image.c, `uint64_t image_allocation[MBX_N_IF]`). The target platform's is its one
#: static object (plat/ctrl_plat.h, `struct ctrl_plat ctrl_plat`, sized by MBX_N_IF and the shape's streams) at its
#: size in that image, so a change to that struct refuses the override until the size is measured again here. Each
#: is owed to hybrid XIP work (#665 decision D3) in docs/design/SPLIT_CONTROL_MEMORY.md section 5; every other point
#: stays within 56. Each entry is its image's measured tiles, under the owner's rule of 2026-11-15 that the control
#: memory's ROM may overflow as debt owed to the cold-code-to-flash work (S14), which supersedes the 60.5 cap of
#: 2026-11-12 until that work lands (#923's ruling of 2026-11-16), and refuses its image half a tile past: the size
#: fixture's at FIXTURE_PAST, its entry at FIXTURE_TILES (59.5 since GET_AS_PATH's read composed with SRP's Talker
#: declarations, #897, and FIXTURE_HISTORY; 59.0 before it, the cap #894's ruling of 2026-11-13 raised the owner's
#: 58.5 to for the composed image); the target platform's 8x8 two-interface image at PLATFORM_PAST, its entry at
#: PLATFORM_TILES (60.5, the owner's decision's cap, #665, which #895's ruling of 2026-11-14 ledgers for the image with
#: SRP's Talker declarations on the tiers, #897's ruling of 2026-11-15 takes for the image with GET_AS_PATH's read on
#: them, and the owner's decision of 2026-11-15 for AECP's REBOOT on them, #871; 61.0 with the PHY poll, #919, and
#: PLATFORM_HISTORY); and its 8x8 one-interface image, a product image, at PRODUCT_PAST, its entry at PRODUCT_TILES
#: (56.5 with #895's declarations and the PHY poll, #919, and PRODUCT_HISTORY). The platform's image is linked at
#: every point with the override its point takes, against this ledger, by tb/verilator/ctrl_split_boot/plat_ledger.py,
#: so a stale ctrl_plat size or a plan past its tiles is refused where it happens.
''',
'''                                         "declarations plan within it (#895); 59.5 with GET_AS_PATH's read "
                                         "composed on them (#897): the CPU budget harness's arms on it, the size "
                                         "fixture with their test ports, need 127,096 to 127,416 B of rom, past "
                                         "the 126,976 B 59.0 holds, so the entry is raised to the next half tile "
                                         "as named debt owed to S14 by the owner's decision of 2026-11-15 "
                                         "(#665): an image past its entry raises it; FIXTURE_OWED"),
''',
'''                                            ((STAGE_SYMBOL, 13_594), ("ctrl_plat", 20_480)), 61.0,
''',
'''                                            "60.0, by #895's ruling of 2026-11-14, item 4, and with GET_AS_PATH's "
                                            "read through the face composed on them, 992 B of rom past 60.0, "
                                            "as #897's ruling of 2026-11-15, item 1, takes it: ROM debt of 4.5 "
                                            "RAMB36 owed to the hybrid XIP work, the cap fully used; 60.5 with "
                                            "AECP's REBOOT composed on the tiers (#871), by the owner's decision "
                                            "of 2026-11-15; 61.0 with the PHY "
                                            "poll and its 1000BASE-T-only advertisement on that image (#919, "
                                            "#840), 652 B of rom past 60.5 and ctrl_plat 64 B more, by the "
                                            "owner's rule of 2026-11-15 (#923's ruling of 2026-11-16, "
                                            "issuecomment-6906679024): ROM debt of 5.0 RAMB36 owed to S14; the "
                                            "saved-state store's name marks over layout 3's id space and its step "
                                            "a pass (#920), ctrl_plat 128 B more and 296 B more rom; PLATFORM_OWED"),
    "platform-8x8-one-interface": Ledgered("target platform's 8x8, one interface",
                                           ((STAGE_SYMBOL, 13_594), ("ctrl_plat", 18_304)), 56.5,
                                           "lane S14, the hybrid XIP (#665 decision D3: cold code to flash); 56.5, "
                                           "a product image, with SRP's Talker declarations (#895) and the PHY "
                                           "poll and its 1000BASE-T-only advertisement (#919, #840), 1,132 B of "
                                           "rom past 56.0, by the owner's rule of 2026-11-15 (#923's ruling of "
                                           "2026-11-16, issuecomment-6906679024): ROM debt of half a tile owed to "
                                           "S14; PRODUCT_OWED"),
''',
'theirs',
]
