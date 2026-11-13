Images at the base b2d39235 (#810 round 29), the same inputs. The platform's 8x8/2if image is refused by the base's own ledger (59.0): its sizes are the refusal's, ctrl_plat from its ELF (nm).

| Point | image | rc | rom B | sram B | RAMB36 (tiles) | rom banks B | srp_mbx text B | ctrl_plat B | last log line |
| 1x1-if1 | fixture | 0 | 107896 | 45552 | 38.0 | 108544 | |  | |
| 1x1-if2 | fixture | 0 | 109600 | 56944 | 41.0 | 110592 | |  | |
| 8x8-if1 | fixture | 0 | 121440 | 86416 | 51.5 | 122880 | |  | |
| 8x8-if2 | fixture | 0 | 123112 | 112576 | 58.0 | 124928 | |  | |
| 1x1-if1 | platform | 0 | 112968 | 46512 | 39.5 | 114688 | | 17472 | |
| 1x1-if2 | platform | 0 | 114696 | 57968 | 43.0 | 116736 | | 19008 | |
| 8x8-if1 | platform | 0 | 126560 | 87392 | 52.5 | 126976 | | 18112 | |
| 8x8-if2 | platform | 2 | | | | | | | wrote <scratch>/r2/img-base/platform-8x8-if2/contract/mbx_contract.h (2 interfaces) |

REFUSED: allocation over budget: 59.5 RAMB36 (rom 128264 bytes in 129024, sram 113568 bytes in 114688) exceeds the 59-RAMB36 budget ledgered for target platform's 8x8, two interfaces
ctrl_plat at 8x8/2if: base 0x4f40 = 20288 B; head 0x4f80 = 20352 B
