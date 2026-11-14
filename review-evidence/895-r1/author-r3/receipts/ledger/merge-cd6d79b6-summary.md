tree cd6d79b6486a4bd56a604949530b5b051b318e56 dirty 0; plat_ledger.py rc 0

| Image | rc | rom B | sram B | RAMB36 | rom banks B | sram banks B | ctrl_plat B | last log line |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| platform 1x1-if1 | 0 | 114640 | 46944 | 39.5 | 114688 | 47104 | 17536 | |
| platform 1x1-if2 | 0 | 116464 | 58400 | 43.0 | 116736 | 59392 | 19072 | |
| platform 8x8-if1 | 0 | 128200 | 88048 | 53.0 | 129024 | 88064 | 18176 | |
| platform 8x8-if2 | 0 | 129984 | 114224 | 60.0 | 131072 | 114688 | 20352 | |
| fixture 1x1-if1 | 0 | 109576 | 45936 | 38.5 | 110592 | 47104 |  | |
| fixture 1x1-if2 | 0 | 111368 | 57344 | 41.5 | 112640 | 57344 |  | |
| fixture 8x8-if1 | 0 | 123096 | 87040 | 52.0 | 124928 | 88064 |  | |
| fixture 8x8-if2 | 0 | 124832 | 113216 | 58.5 | 124928 | 114688 |  | |
| harness arm answering-every-port 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125140 bytes in 126976, sram 113280 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
| harness arm valid-destinations 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 124992 bytes in 126976, sram 113216 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
