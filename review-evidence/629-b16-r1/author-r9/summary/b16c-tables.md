<!-- four points: Run | Point | Frames | Level, dBFS | 997 Hz: frequency, offset | THD+N, dB | SNR, dB | 9,973 Hz: frequency, offset | THD+N, dB | SNR, dB -->
| `bcrf` | (a) | 1,919,598; 319,933 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.93) | 123.97 |
| `bcrf` | (b) | 1,919,574; 319,929 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.99 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.93) | 123.97 |
| `bcrf` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.90) | 123.97 |
| `baaf` | (a) | 1,919,598; 319,933 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 | 9,973.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 |
| `baaf` | (b) | 1,919,580; 319,930 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.92) | 123.98 | 9,973.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 |
| `baaf` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.92) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.91) | 123.97 |
| `b0-2` | (a) | 1,919,610; 319,935 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.62 (-102.55) | 123.62 | 9,973.0000 Hz, 0.000 ppm | -114.29 (-82.58) | 114.29 |
| `b0-2` | (b) | 1,919,592; 319,932 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.62 (-102.15) | 123.62 | 9,973.0000 Hz, 0.000 ppm | -114.33 (-82.18) | 114.33 |
| `b0-2` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.95 (-100.47) | 123.95 | 9,973.0000 Hz, 0.000 ppm | -122.80 (-80.48) | 122.80 |

<!-- lane B9's grade at (c): Run | Tone | Blocks | Discontinuities | Blocks at the path's floor | THD+N at the floor, dB, median (worst) | SNR at the floor, dB | THD+N, all blocks, dB, median (worst) | Level | Offset, ppm, median (largest block) -->
| `bcrf` | 997 Hz, channel 0 | 300 | 0 | 300 | -123.98 (-123.93) | 123.99 | -123.98 (-123.93) | -14.10 dBFS | 0.0000 (0.000) |
| `bcrf` | 9,973 Hz, channel 1 | 300 | 0 | 300 | -123.97 (-123.90) | 123.97 | -123.97 (-123.90) | -14.10 dBFS | 0.0000 (0.000) |
<!-- `bcrf`: skips 0, repeats 0, inserts 0, glitches 0, silent 0, effective offset 0.0 ppm, phase net -0.0000001 frames -->
| `baaf` | 997 Hz, channel 0 | 300 | 0 | 300 | -123.98 (-123.92) | 123.99 | -123.98 (-123.92) | -14.10 dBFS | 0.0000 (0.000) |
| `baaf` | 9,973 Hz, channel 1 | 300 | 0 | 300 | -123.97 (-123.91) | 123.97 | -123.97 (-123.91) | -14.10 dBFS | 0.0000 (0.000) |
<!-- `baaf`: skips 0, repeats 0, inserts 0, glitches 0, silent 0, effective offset 0.0 ppm, phase net -0.0000000 frames -->
| `b0-2` | 997 Hz, channel 0 | 300 | 0 | 169 | -123.98 (-123.91) | 123.98 | -123.95 (-100.47) | -14.10 dBFS | 0.0000 (0.030) |
| `b0-2` | 9,973 Hz, channel 1 | 300 | 0 | 169 | -123.95 (-120.18) | 123.95 | -122.80 (-80.48) | -14.10 dBFS | 0.0000 (0.030) |
<!-- `b0-2`: skips 0, repeats 0, inserts 0, glitches 0, silent 0, effective offset 0.0 ppm, phase net 0.0005065 frames -->

<!-- (c) against (a) and (b): Run | (c) against (b) | (c) against (a) -->
| `bcrf` | SAMPLE-EXACT over 1,646,473 recorded frames, 34.3 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,647,859 recorded frames, 34.3 s, 0 differing, 0 slips |
| `baaf` | SAMPLE-EXACT over 1,644,390 recorded frames, 34.3 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,641,156 recorded frames, 34.2 s, 0 differing, 0 slips |
| `b0-2` | SAMPLE-EXACT over 1,637,980 recorded frames, 34.1 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,637,452 recorded frames, 34.1 s, 0 differing, 0 slips |

<!-- (d): Run | decoded | invalid (before the loop) | skips | repeats | net steps | torn | level, THD+N -->
| `bcrf` | 14,583,391 | 104,609 | 0 | 0 | 0 | 0 | -1.00 dBFS, -146.06 (-6.61) dB, 306 blocks; -1.00 dBFS, -145.99 (-6.60) dB, 306 blocks |
| `baaf` | 14,585,924 | 102,076 | 0 | 0 | 0 | 0 | -1.00 dBFS, -146.06 (-8.39) dB, 306 blocks; -1.00 dBFS, -145.99 (-8.39) dB, 306 blocks |
| `b0-2` | 14,583,286 | 104,714 | 0 | 0 | 0 | 0 | -1.00 dBFS, -146.06 (-6.54) dB, 306 blocks; -1.00 dBFS, -145.99 (-6.54) dB, 306 blocks |

<!-- following record -->
<!-- `bcrf` -->
- set-clock peer-internal: peer to 0, SUCCESS, read back 0
- set-clock bcrf: dut to 1, SUCCESS, read back 1
- set-clock restore: dut to 0, SUCCESS, read back 0
- set-clock restore: peer to 1, SUCCESS, read back 1
- servo LOCKED 2.657 to 3.161 s after the DUT's set
- mark before-peer-set: clock {'dut': 0, 'peer': 1}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [22, 21]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- mark after-peer-set: clock {'dut': 0, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [22, 21]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- mark window-mark-0: clock {'dut': 1, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark window-mark-1: clock {'dut': 1, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark window-mark-2: clock {'dut': 1, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark after-captures: clock {'dut': 1, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [6, 5]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark after-restore: clock {'dut': 0, 'peer': 1}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- poll span poll-start..peer-set: 1 polls, servo {'IDLE': 1}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '00000000', 1), '0x748': ('0000098c', '0000098c', 1), '0x8d4': ('000000a2', '000000a2', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0100', 1), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000020', '00000020', 1)}
- poll span peer-set..dut-set: 34 polls, servo {'IDLE': 34}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '80000000', 2), '0x748': ('0000098c', '00001537', 14), '0x8d4': ('000000a2', '000000ac', 6), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0205', 10), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000020', '00000020', 1)}
- poll span dut-set..window-start: 52 polls, servo {'ACQUIRE': 6, 'LOCKED': 46}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '80000000', 1), '0x748': ('00001542', '00001544', 16), '0x8d4': ('000000ac', '000000ae', 2), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a000a', '000a0209', 8), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000033', 'ffa00034', 11)}
- poll span window-start..window-end: 596 polls, servo {'LOCKED': 596}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '80000000', 1), '0x748': ('00001543', '00001537', 28), '0x8d4': ('000000ae', '000000ae', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0209', '000a0208', 7), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('ff9f0034', 'ff9f0034', 5)}
- poll span window-end..restored: 10 polls, servo {'LOCKED': 9, 'IDLE': 1}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '00000000', 2), '0x748': ('00001540', '00001548', 7), '0x8d4': ('000000ae', '000000ae', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a020b', '000a0100', 6), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('ff9f0034', '00000020', 4)}
- poll span restored..poll-end: 12 polls, servo {'IDLE': 12}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '00000000', 1), '0x748': ('00001548', '00001548', 1), '0x8d4': ('000000ae', '000000ae', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0100', 1), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000020', '00000020', 1)}
- tone monitor: 1805 reads, states {'RUNNING': 1805}, trigger times 1, hw_ptr monotonic True
- music checks closed: [True, True, True]
- final read-back equal to the start: True []
<!-- `baaf` -->
- set-clock peer-internal: peer to 0, SUCCESS, read back 0
- set-clock baaf: dut to 2, SUCCESS, read back 2
- set-clock restore: dut to 0, SUCCESS, read back 0
- set-clock restore: peer to 1, SUCCESS, read back 1
- servo LOCKED 6.68 to 7.18 s after the DUT's set
- mark before-peer-set: clock {'dut': 0, 'peer': 1}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- mark after-peer-set: clock {'dut': 0, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [23, 22]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- mark window-mark-0: clock {'dut': 2, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [24, 23]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark window-mark-1: clock {'dut': 2, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [24, 23]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark window-mark-2: clock {'dut': 2, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [24, 23]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark after-captures: clock {'dut': 2, 'peer': 0}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [24, 23]; peer CLOCK_DOMAIN [7, 6]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 0]; DUT in 1 [1, 0]; peer in 0 [1, 0]
- mark after-restore: clock {'dut': 0, 'peer': 1}; DUT CLOCK_DOMAIN LOCKED/UNLOCKED [24, 23]; peer CLOCK_DOMAIN [8, 7]; DUT in 0 MEDIA_LOCKED/UNLOCKED [1, 1]; DUT in 1 [1, 1]; peer in 0 [1, 0]
- poll span poll-start..peer-set: 1 polls, servo {'IDLE': 1}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '00000000', 1), '0x748': ('00001548', '00001548', 1), '0x8d4': ('000000ae', '000000ae', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0100', 1), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000020', '00000020', 1)}
- poll span peer-set..dut-set: 34 polls, servo {'IDLE': 34}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '80000000', 2), '0x748': ('00001548', '0000153f', 12), '0x8d4': ('000000ae', '000000b8', 6), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0208', 8), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('000015e9', '000015e9', 1), '0x8f8': ('00000020', '00000020', 1)}
- poll span dut-set..window-start: 52 polls, servo {'ACQUIRE': 14, 'LOCKED': 38}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '80000000', 1), '0x748': ('00001540', '00001531', 18), '0x8d4': ('000000b8', '000000bc', 3), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a000c', '000a020d', 7), '0x8e0': ('00140005', '001e0007', 4), '0x8e4': ('000015e9', '00001537', 10), '0x8f8': ('00000033', 'ff9f0034', 12)}
- poll span window-start..window-end: 596 polls, servo {'LOCKED': 596}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '80000000', 1), '0x748': ('00001537', '0000153c', 30), '0x8d4': ('000000bc', '000000bc', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a020b', '000a0209', 7), '0x8e0': ('001e0007', '001e0007', 1), '0x8e4': ('00001536', '0000153b', 17), '0x8f8': ('ffa00034', 'ff9f0034', 5)}
- poll span window-end..restored: 10 polls, servo {'LOCKED': 8, 'IDLE': 2}, failed 0; words (first, last, distinct) {'0x738': ('80000000', '00000000', 2), '0x748': ('0000153b', '00001540', 5), '0x8d4': ('000000bc', '000000bc', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0209', '000a0100', 5), '0x8e0': ('001e0007', '00000000', 2), '0x8e4': ('0000153b', '0000153f', 5), '0x8f8': ('ff9f0034', '00000020', 3)}
- poll span restored..poll-end: 12 polls, servo {'IDLE': 12}, failed 0; words (first, last, distinct) {'0x738': ('00000000', '00000000', 1), '0x748': ('00001540', '00001540', 1), '0x8d4': ('000000bc', '000000bc', 1), '0x8d8': ('00000000', '00000000', 1), '0x8dc': ('000a0100', '000a0100', 1), '0x8e0': ('00000000', '00000000', 1), '0x8e4': ('0000153f', '0000153f', 1), '0x8f8': ('00000020', '00000020', 1)}
- tone monitor: 1803 reads, states {'RUNNING': 1803}, trigger times 1, hw_ptr monotonic True
- music checks closed: [True, True, True]
- final read-back equal to the start: True []
<!-- `b0-2` -->
- music checks closed: []
- final read-back equal to the start: True []
