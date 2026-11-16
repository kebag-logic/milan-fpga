# ROM per split image, base 659d7687 against head dfcd8eed (qimg.sh: fixed flash maps, runtimes and CSR map)

| Image | rc base / head | ROM base, B | ROM head, B | Delta, B | ROM banks, B | Tiles base / head | Ledgered point | ELF and loadable identical |
|---|---|---:|---:|---:|---:|---|---|---|
| fixture-1x1-1if | 0 / 0 | 111,024 | 111,048 | +24 | 112,640 | 41.0 / 41.0 | - | no |
| fixture-1x1-2if | 0 / 0 | 112,312 | 112,344 | +32 | 112,640 | 41.5 / 41.5 | - | no |
| fixture-8x8-1if | 0 / 0 | 124,528 | 124,568 | +40 | 124,928 | 54.0 / 54.0 | - | no |
| fixture-8x8-2if | 0 / 0 | 125,792 | 125,824 | +32 | 126,976 | 59.0 / 59.0 | 8x8-two-interfaces (59.0) | no |
| platform-1x1-1if | 0 / 0 | 116,072 | 116,104 | +32 | 116,736 | 42.5 / 42.5 | - | no |
| platform-1x1-2if | 0 / 0 | 117,384 | 117,416 | +32 | 118,784 | 43.5 / 43.5 | - | no |
| platform-8x8-1if | 0 / 0 | 129,624 | 129,664 | +40 | 131,072 | 56.0 / 56.0 | - | no |
| platform-8x8-2if | 0 / 0 | 130,920 | 130,960 | +40 | 131,072 | 60.0 / 60.0 | platform-8x8-two-interfaces (60.0) | no |

Every image differs: the #840 identity (entity_id, entity_model_id, MAC) and clockAccuracy 0x22 reach the generated headers (adp_entity_gen.h, aecp_entity_gen.h, gen/nvm_shape_gen.h); .text grows 24 to 40 B through those immediates (nvm_klj2.o +28 B and ctrl_aecp_image.o +8 B at the 1x1/1if fixture); .rodata and the AEM image's 7,512 B are unchanged. No image leaves its banks or its tile count, and no ledger entry moves.
