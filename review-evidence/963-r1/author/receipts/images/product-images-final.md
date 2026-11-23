# The target platform's split images (`ctrl_plat_image.py`), base `dd163e41` and the final firmware (`50d3f10e`'s clone)

Built on the base product export's bus map and flash map (the flip lane's split export at `dd163e41`), 8x8/1if at its ledgered point `platform-8x8-one-interface`.

| Point | ROM bytes base / head | ROM RAMB36 | SRAM bytes base / head | SRAM RAMB36 | tiles base / head | ledger |
|---|---|---|---|---|---|---|
| 8x8-1if | 139,208 / 139,208 | 34 / 34 | 98,160 / 98,160 | 24 / 24 | 58.0 / 58.0 | 58.0 |
| 1x1 | 126,432 / 126,432 | 31 / 31 | 56,736 / 56,736 | 14 / 14 | 45.0 / 45.0 | - (budget 56) |
