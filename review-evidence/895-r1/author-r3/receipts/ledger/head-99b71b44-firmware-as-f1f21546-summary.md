tree 99b71b44bfeaa4aaa98a3c534c1921e70cb8005f dirty 0; plat_ledger.py rc 0

| Image | rc | rom B | sram B | RAMB36 | rom banks B | sram banks B | ctrl_plat B | last log line |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| platform 1x1-if1 | 0 | 115240 | 46944 | 40.0 | 116736 | 47104 | 17536 | |
| platform 1x1-if2 | 0 | 117208 | 58400 | 43.5 | 118784 | 59392 | 19072 | |
| platform 8x8-if1 | 0 | 128808 | 88048 | 53.0 | 129024 | 88064 | 18176 | |
| platform 8x8-if2 | 0 | 130728 | 114224 | 60.0 | 131072 | 114688 | 20352 | |
| fixture 1x1-if1 | 0 | 110176 | 45952 | 38.5 | 110592 | 47104 |  | |
| fixture 1x1-if2 | 0 | 112112 | 57376 | 42.0 | 112640 | 59392 |  | |
| fixture 8x8-if1 | 0 | 123696 | 87056 | 52.0 | 124928 | 88064 |  | |
| fixture 8x8-if2 | 2 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125576 bytes in 126976, sram 113232 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
| harness arm answering-every-port 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125884 bytes in 126976, sram 113296 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
| harness arm valid-destinations 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125736 bytes in 126976, sram 113248 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
