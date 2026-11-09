# Vivado runs at the head (recipe form, under the slot wrapper)

| Run | rc and seconds | Vivado peak memory (MB) | `Synth 8-4445` | `Synth 8-6901` | Log SHA-256 | Log bytes |
|---|---|---:|---:|---:|---|---:|
| route-1x1, ExtraPostPlacementOpt, with synthesis | 0 4085s | 8,537 | 0 | 1 | `fc2be49d556d3dcdb24ea2bdcc6a5f17fd877116f5f4b39350e22d03dab0f9d6` | 910,032 |
| route-1x1, AltSpreadLogic_high | 0 1621s | 5,175 | 0 | 0 | `0c251dd4e9d642ab2c2dcd7beb40fcf439443a17d4f69b76514a169d2bcd7ba9` | 453,021 |
| route-1x1, ExtraTimingOpt | 0 1375s | 5,273 | 0 | 0 | `f2e986d942d622b23352bde2d8a74cd159e9231dfc584ab4f91b7678db4e956c` | 412,791 |
| ooc-1x1 | 0 1257s | 5,402 | 0 | 1 | `f359269d9b7f87d53f950f5f9dfb37140b054a63edfafddaa121e15ab3584a3c` | 315,782 |
| rtl-8x8 (RTL elaboration for the 8x8 parameters) | 0 79s | 4,390 | 0 | 1 | `f1b773a309c50be82aa4c1d0bd149c71502865db9196caf9e704b033ef6f1a46` | 207,987 |
| ooc-8x8 | 0 2267s | 6,491 | 0 | 1 | `2e7cd457ed0a821c45ec102bf57efdbf13cb1560f46fc8a791cadd4dca1a3a4d` | 319,267 |
