ROM and RAM of each ledger image, base b2d39235 against head e0398c40 (images-base.md, images-head.md).

| Image | Point | rom base | rom head | rom delta | sram base | sram head | sram delta | RAMB36 base / head | ctrl_plat delta |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| fixture | 1x1-if1 | 107,896 | 108,880 | +984 | 45,552 | 45,568 | +16 | 38.0 / 38.5 |  |
| fixture | 1x1-if2 | 109,600 | 110,672 | +1,072 | 56,944 | 56,976 | +32 | 41.0 / 41.5 |  |
| fixture | 8x8-if1 | 121,440 | 122,400 | +960 | 86,416 | 86,464 | +48 | 51.5 / 51.5 |  |
| fixture | 8x8-if2 | 123,112 | 124,136 | +1,024 | 112,576 | 112,624 | +48 | 58.0 / 58.0 |  |
| platform | 1x1-if1 | 112,968 | 113,944 | +976 | 46,512 | 46,576 | +64 | 39.5 / 39.5 | 64 |
| platform | 1x1-if2 | 114,696 | 115,768 | +1,072 | 57,968 | 58,032 | +64 | 43.0 / 43.0 | 64 |
| platform | 8x8-if1 | 126,560 | 127,512 | +952 | 87,392 | 87,456 | +64 | 52.5 / 53.0 | 64 |
| platform | 8x8-if2 | 128,264 | 129,288 | +1,024 | 113,568 | 113,632 | +64 | 59.5 / 60.0 | 64 |

rom delta +952 to +1,072 B; sram delta +16 to +64 B.
