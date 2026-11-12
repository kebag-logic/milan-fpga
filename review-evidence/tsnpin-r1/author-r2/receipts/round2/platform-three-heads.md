| Point | Platform `rom` need B: 70936b77 / round-1 head / redelivery | `sram` need B | RAMB36 | `ctrl_plat` B | room in `rom` banks at the redelivery |
|---|---:|---:|---:|---:|---:|
| 1x1_tdm8-if1 | 109,560 / 109,920 / 110,048 | 47,168 / 47,328 / 47,328 | 39.0 / 39.0 / 39.0 | 18,432 / 18,584 / 18,584 | 544 |
| 1x1_tdm8-if2 | 111,200 / 111,504 / 111,640 | 58,592 / 58,736 / 58,736 | 42.0 / 42.0 / 42.0 | 19,928 / 20,072 / 20,080 | 1,000 |
| 8x8-if1 | 123,304 / 123,672 / 123,800 | 87,760 / 87,904 / 87,904 | 52.0 / 52.0 / 52.0 | 19,088 / 19,240 / 19,240 | 1,128 |
| 8x8-if2 | 125,048 / 125,360 / 125,504 | 113,936 / 114,080 / 114,096 | 59.0 / 59.0 / 59.0 | 21,240 / 21,384 / 21,392 | 1,472 |

The redelivery's 8x8-if2 column is measured with the override re-keyed to `ctrl_plat` 21,392 B in a scratch copy (the head's key, 21,384 B, refuses it by name: platform-8x8-if2-refusal.log).
