
### route-1x1
| Combination | LUT | FF | SLICE | RAMB36 | RAMB18 | BRAM_TILE | DSP | CARRY4 | WNS_ns | WHS_ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 50,128 | 59,006 | 15,815 | 79 | 27 | 92.5 | 14 | 3,405 | +0.063 | +0.036 |
| B | 50,753 | 59,014 | 15,827 | 79 | 27 | 92.5 | 14 | 3,423 | +0.101 | +0.036 |
| B minus A | +625 | +8 | +12 | +0 | +0 | +0 | +0 | +18 | +0.038 | +0 |

### ooc-1x1
| Combination | LUT | FF | RAMB36 | RAMB18 | BRAM_TILE | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 24,343 | 25,344 | 21 | 3 | 22.5 | 8 | 1,623 |
| B | 24,505 | 25,470 | 21 | 3 | 22.5 | 8 | 1,638 |
| B minus A | +162 | +126 | +0 | +0 | +0 | +0 | +15 |

### ooc-8x8
| Combination | LUT | FF | RAMB36 | RAMB18 | BRAM_TILE | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 31,562 | 33,929 | 26 | 5 | 28.5 | 8 | 2,001 |
| B | 31,390 | 33,844 | 26 | 5 | 28.5 | 8 | 2,016 |
| B minus A | -172 | -85 | +0 | +0 | +0 | +0 | +15 |

### ooc-1x1 sub-blocks
| Instance | LUT A | LUT B | FF A | FF B | RAMB36 | RAMB18 | DSP | CARRY4 A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `wrapper` | 24,343 | 24,505 | 25,344 | 25,470 | 21 | 3 | 8 | 1,623 |
| `u_pp` | 23,659 | 23,814 | 24,507 | 24,635 | 20 | 2 | 4 | 1,551 |
| `u_nvm` | 603 | 610 | 475 | 475 | 0 | 0 | 4 | 47 |
| `ctl_fifo` | 79 | 79 | 33 | 33 | 1 | 1 | 0 | 3 |
| `u_pp/u_srp` | 4,573 | 4,555 | 6,439 | 6,438 | 0 | 1 | 2 | 247 |
| `u_pp/u_adp` | 628 | 629 | 479 | 479 | 0 | 0 | 1 | 44 |
| `u_pp/u_talker` | 894 | 881 | 551 | 551 | 0 | 0 | 0 | 18 |
| `u_pp/u_listener` | 1,440 | 1,514 | 1,110 | 1,099 | 5 | 0 | 0 | 31 |
| `u_pp/u_aecp` | 5,598 | 5,604 | 3,500 | 3,500 | 6 | 0 | 1 | 355 |
| `u_pp/u_aecp/u_ucpu` | 1,608 | 1,609 | 495 | 495 | 3 | 0 | 0 | 68 |
| `u_pp/u_notify` | 3,175 | 3,193 | 3,299 | 3,299 | 0 | 0 | 0 | 182 |
| `u_pp/u_nvm_port` | 453 | 536 | 127 | 160 | 0 | 0 | 0 | 58 |
| `u_pp/u_nvm_arb` | 13 | 7 | 4 | 4 | 0 | 0 | 0 | 0 |
| `u_pp/u_nvm_shadow` | 815 | 812 | 1,118 | 1,118 | 0 | 0 | 0 | 51 |
| `u_pp/u_aecp/u_d3` | 1,073 | 1,076 | 485 | 485 | 0 | 0 | 0 | 88 |

### ooc-8x8 sub-blocks
| Instance | LUT A | LUT B | FF A | FF B | RAMB36 | RAMB18 | DSP | CARRY4 A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `wrapper` | 31,562 | 31,390 | 33,929 | 33,844 | 26 | 5 | 8 | 2,001 |
| `u_pp` | 30,364 | 30,189 | 32,543 | 32,458 | 25 | 4 | 4 | 1,912 |
| `u_nvm` | 1,118 | 1,121 | 1,026 | 1,026 | 0 | 0 | 4 | 57 |
| `ctl_fifo` | 79 | 79 | 33 | 33 | 1 | 1 | 0 | 3 |
| `u_pp/u_srp` | 8,702 | 8,652 | 11,191 | 11,191 | 0 | 1 | 2 | 463 |
| `u_pp/u_adp` | 809 | 769 | 465 | 465 | 1 | 0 | 1 | 86 |
| `u_pp/u_talker` | 1,564 | 1,512 | 569 | 569 | 1 | 1 | 0 | 19 |
| `u_pp/u_listener` | 1,616 | 1,534 | 1,124 | 1,132 | 5 | 0 | 0 | 30 |
| `u_pp/u_aecp` | 6,141 | 6,156 | 4,684 | 4,684 | 7 | 0 | 1 | 358 |
| `u_pp/u_aecp/u_ucpu` | 1,608 | 1,614 | 495 | 495 | 3 | 0 | 0 | 68 |
| `u_pp/u_notify` | 2,921 | 2,886 | 3,799 | 3,799 | 0 | 0 | 0 | 67 |
| `u_pp/u_nvm_port` | 455 | 521 | 127 | 160 | 0 | 0 | 0 | 57 |
| `u_pp/u_nvm_arb` | 20 | 23 | 4 | 4 | 0 | 0 | 0 | 0 |
| `u_pp/u_nvm_shadow` | 790 | 788 | 1,013 | 1,014 | 2 | 1 | 0 | 51 |
| `u_pp/u_aecp/u_d3` | 1,282 | 1,397 | 530 | 530 | 0 | 0 | 0 | 88 |

### ooc-1x1 grouped
| Sub-block | Instances | LUT A / B | FF A / B | RAMB36 A / B | RAMB18 A / B | DSP A / B | CARRY4 A / B |
|---|---|---:|---:|---:|---:|---:|---:|
| SRP | `u_pp/u_srp` | 4,573 / 4,555 | 6,439 / 6,438 | 0 / 0 | 1 / 1 | 2 / 2 | 247 / 247 |
| ADP | `u_pp/u_adp` | 628 / 629 | 479 / 479 | 0 / 0 | 0 / 0 | 1 / 1 | 44 / 44 |
| ACMP talker | `u_pp/u_talker` | 894 / 881 | 551 / 551 | 0 / 0 | 0 / 0 | 0 / 0 | 18 / 18 |
| ACMP listener | `u_pp/u_listener`, `u_pp/u_lsn_admit` | 1,441 / 1,516 | 1,111 / 1,100 | 5 / 5 | 0 / 0 | 0 / 0 | 31 / 34 |
| AECP engine, total | `u_pp/u_aecp` | 5,598 / 5,604 | 3,500 / 3,500 | 6 / 6 | 0 / 0 | 1 / 1 | 355 / 354 |
| AECP microcontroller | `u_pp/u_aecp/u_ucpu` | 1,608 / 1,609 | 495 / 495 | 3 / 3 | 0 / 0 | 0 / 0 | 68 / 68 |
| AECP saved-state writer (NVM manager) | `u_pp/u_aecp/u_d3` | 1,073 / 1,076 | 485 / 485 | 0 / 0 | 0 / 0 | 0 / 0 | 88 / 88 |
| Notification | `u_pp/u_notify` | 3,175 / 3,193 | 3,299 / 3,299 | 0 / 0 | 0 / 0 | 0 / 0 | 182 / 179 |
| NVM port | `u_pp/u_nvm_port` | 453 / 536 | 127 / 160 | 0 / 0 | 0 / 0 | 0 / 0 | 58 / 73 |
| NVM manager arbiter | `u_pp/u_nvm_arb` | 13 / 7 | 4 / 4 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| ACMP binding store (NVM manager) | `u_pp/u_nvm_shadow` | 815 / 812 | 1,118 / 1,118 | 0 / 0 | 0 / 0 | 0 / 0 | 51 / 51 |
| NVM backend (wrapper) | `u_nvm` | 603 / 610 | 475 / 475 | 0 / 0 | 0 / 0 | 4 / 4 | 47 / 47 |
| Packet storage: RX pools | `u_pp/g_rx_pool[*].u_rx_slots` | 252 / 256 | 206 / 206 | 5 / 5 | 0 / 0 | 0 / 0 | 19 / 19 |
| Packet storage: TX slots | `u_pp/u_tx_slots` | 347 / 349 | 138 / 138 | 1 / 1 | 0 / 0 | 0 / 0 | 5 / 5 |
| Packet storage: trace ring | `u_pp/u_trace` | 37 / 40 | 18 / 18 | 1 / 1 | 0 / 0 | 0 / 0 | 4 / 4 |
| Packet storage: control frame FIFO (wrapper) | `ctl_fifo` | 79 / 79 | 33 / 33 | 1 / 1 | 1 / 1 | 0 / 0 | 3 / 3 |
| Wrapper total | `wrapper` | 24,343 / 24,505 | 25,344 / 25,470 | 21 / 21 | 3 / 3 | 8 / 8 | 1,623 / 1,638 |

### ooc-8x8 grouped
| Sub-block | Instances | LUT A / B | FF A / B | RAMB36 A / B | RAMB18 A / B | DSP A / B | CARRY4 A / B |
|---|---|---:|---:|---:|---:|---:|---:|
| SRP | `u_pp/u_srp` | 8,702 / 8,652 | 11,191 / 11,191 | 0 / 0 | 1 / 1 | 2 / 2 | 463 / 462 |
| ADP | `u_pp/u_adp` | 809 / 769 | 465 / 465 | 1 / 1 | 0 / 0 | 1 / 1 | 86 / 86 |
| ACMP talker | `u_pp/u_talker` | 1,564 / 1,512 | 569 / 569 | 1 / 1 | 1 / 1 | 0 / 0 | 19 / 19 |
| ACMP listener | `u_pp/u_listener`, `u_pp/u_lsn_admit` | 1,616 / 1,534 | 1,125 / 1,133 | 5 / 5 | 0 / 0 | 0 / 0 | 30 / 30 |
| AECP engine, total | `u_pp/u_aecp` | 6,141 / 6,156 | 4,684 / 4,684 | 7 / 7 | 0 / 0 | 1 / 1 | 358 / 358 |
| AECP microcontroller | `u_pp/u_aecp/u_ucpu` | 1,608 / 1,614 | 495 / 495 | 3 / 3 | 0 / 0 | 0 / 0 | 68 / 68 |
| AECP saved-state writer (NVM manager) | `u_pp/u_aecp/u_d3` | 1,282 / 1,397 | 530 / 530 | 0 / 0 | 0 / 0 | 0 / 0 | 88 / 88 |
| Notification | `u_pp/u_notify` | 2,921 / 2,886 | 3,799 / 3,799 | 0 / 0 | 0 / 0 | 0 / 0 | 67 / 67 |
| NVM port | `u_pp/u_nvm_port` | 455 / 521 | 127 / 160 | 0 / 0 | 0 / 0 | 0 / 0 | 57 / 72 |
| NVM manager arbiter | `u_pp/u_nvm_arb` | 20 / 23 | 4 / 4 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| ACMP binding store (NVM manager) | `u_pp/u_nvm_shadow` | 790 / 788 | 1,013 / 1,014 | 2 / 2 | 1 / 1 | 0 / 0 | 51 / 51 |
| NVM backend (wrapper) | `u_nvm` | 1,118 / 1,121 | 1,026 / 1,026 | 0 / 0 | 0 / 0 | 4 / 4 | 57 / 57 |
| Packet storage: RX pools | `u_pp/g_rx_pool[*].u_rx_slots` | 254 / 253 | 206 / 206 | 5 / 5 | 0 / 0 | 0 / 0 | 19 / 19 |
| Packet storage: TX slots | `u_pp/u_tx_slots` | 364 / 221 | 138 / 138 | 1 / 1 | 0 / 0 | 0 / 0 | 5 / 5 |
| Packet storage: trace ring | `u_pp/u_trace` | 28 / 28 | 18 / 18 | 1 / 1 | 0 / 0 | 0 / 0 | 4 / 4 |
| Packet storage: control frame FIFO (wrapper) | `ctl_fifo` | 79 / 79 | 33 / 33 | 1 / 1 | 1 / 1 | 0 / 0 | 3 / 3 |
| Wrapper total | `wrapper` | 31,562 / 31,390 | 33,929 / 33,844 | 26 / 26 | 5 / 5 | 8 / 8 | 2,001 / 2,016 |
