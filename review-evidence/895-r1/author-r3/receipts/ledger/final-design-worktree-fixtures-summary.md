tree fa3f31ee35b2e93617dd394177ac872e0206146a dirty 7; plat_ledger.py rc -

| Image | rc | rom B | sram B | RAMB36 | rom banks B | sram banks B | ctrl_plat B | last log line |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| platform 1x1-if1 | 0 | 115536 | 47072 | 40.0 | 116736 | 47104 | 17664 | |
| platform 1x1-if2 | 0 | 117520 | 58528 | 43.5 | 118784 | 59392 | 19200 | |
| platform 8x8-if1 | 0 | 129104 | 88176 | 54.0 | 131072 | 90112 | 18304 | |
| platform 8x8-if2 | 2 | | | | | | | REFUSED: allocation over budget: the override 'platform-8x8-two-interfaces' is for the target platform's 8x8, two interfaces image alone, the one carrying {'nvm_stage': 13594, 'ctrl_plat': 20352}; thi |
| fixture 1x1-if1 | 0 | 110176 | 45952 | 38.5 | 110592 | 47104 |  | |
| fixture 1x1-if2 | 0 | 112112 | 57376 | 42.0 | 112640 | 59392 |  | |
| fixture 8x8-if1 | 0 | 123696 | 87056 | 52.0 | 124928 | 88064 |  | |
| fixture 8x8-if2 | 2 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125576 bytes in 126976, sram 113232 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
| harness arm answering-every-port 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125884 bytes in 126976, sram 113296 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
| harness arm valid-destinations 8x8-if2 | 1 | | | | | | | REFUSED: allocation over budget: 59 RAMB36 (rom 125736 bytes in 126976, sram 113248 bytes in 114688) exceeds the 58.5-RAMB36 budget ledgered for 8x8, two interfaces |
