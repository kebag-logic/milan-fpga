<!-- din-run -->
| Run | Recording | AVTP PDUs | Sequence gaps | Playback region | Torn frames, region | Torn frames, whole recording | Invalid words, region | Result |
|---|---|---|---|---|---|---|---|---|
| `din-long` | 4,551,624 frames | 758,604 | 0 | 3,360,036 frames, 70.001 s | 0 | 0 | 0 | PASS |

<!-- din-channels -->
| Stream channel | Pattern tag | TDM slot | Valid words | +1 steps | Repeats | Skips | Other steps | Result |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 1 | 2 | 1 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 2 | 3 | 2 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 3 | 4 | 3 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 4 | 5 | 4 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 5 | 6 | 5 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 6 | 7 | 6 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 7 | 8 | 7 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |

<!-- dout-run -->
| Run | Frames | Torn | Invalid words | Zero words | Slot order | Beat clusters | Underrun clusters | Result |
|---|---|---|---|---|---|---|---|---|
| `dout-long` | 3,360,000 (70 s) | 0 | 0 | 0 | Identity | 36: 696 repeated, 732 dropped | 23: 12 after logged talker lateness, 11 without | PASS |

<!-- dout-channels -->
| SoC capture channel | Mapped stream channel | TDM slot | Recovered tag | Valid words | Result |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 3,360,000 | In order |
| 1 | 1 | 1 | 2 | 3,360,000 | In order |
| 2 | 2 | 2 | 3 | 3,360,000 | In order |
| 3 | 3 | 3 | 4 | 3,360,000 | In order |
| 4 | 4 | 4 | 5 | 3,360,000 | In order |
| 5 | 5 | 5 | 6 | 3,360,000 | In order |
| 6 | 6 | 6 | 7 | 3,360,000 | In order |
| 7 | 7 | 7 | 8 | 3,360,000 | In order |

<!-- usb-runs -->
| Run | Capture | Frames | Pass the pattern rule | Silent frames (stretches) | Slot order kept | Rotated by 1 to 7 words | Other | Rotation changes | Longest run in one rotation | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| `usb-long` | 75.116 s, rc 0 | 3,600,000 | 0 | 327,339 (2,420) | 344,438 (9.6%) | 2,919,511 | 8,712 | 2,833 | 2,922 frames | FAIL |
| `usb-long2` | 75.108 s, rc 0 | 3,600,000 | 0 | 3,244 (4) | 428,820 (11.9%) | 3,166,358 | 1,578 | 238 | 95,998 frames | FAIL |

<!-- usb-detail -->
| Run | Words with a non-zero low byte | Frames spread one ordinal or more | Steps inside one rotation: +1, repeat, skip, other | Joins between rotations | Joins that continue the ordinal |
|---|---|---|---|---|---|
| `usb-long` | 25,484,975 of 26,163,422 (97.4%) | 636,231 | 3,248,176, 2,825, 601, 7,758 | 4,588 | 5 |
| `usb-long2` | 28,102,227 of 28,773,277 (97.7%) | 188,754 | 3,589,776, 3,269, 743, 889 | 500 | 5 |

