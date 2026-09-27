# Standards citation check

Source pages were extracted directly from the three standards PDFs using
`pdftotext -layout`. Only clause/page references and conclusions are retained
here; the extracted standard text remains unpublished scratch data.

| Source PDF | SHA-256 |
|---|---|
| `Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf` | `6bb902be1c1de8c44f4c4c583a645b0b37e0b2dac27870486ce229e68ce3bba8` |
| `1722-2016.pdf` | `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c` |
| `1722.1-2021.pdf` | `ad7b822008c1b78bce8af1470f1ace177a22344aa48c0da939066d6db9a65b9c` |

| Release criterion | Verified authority | PDF page(s) | Finding |
|---|---|---|---|
| Counter observations | Milan 5.3.7.7 / Table 5.4; 5.3.8.10 / Table 5.6 | 40, 43-44 | Output/input diagnostic counters |
| Sequence mismatch | IEEE 1722-2016 4.4.4.6 | 37 | Sequence field, not uncertainty |
| Timestamp uncertainty | IEEE 1722-2016 4.4.4.7; Milan B.1/B.1.1 | 37; 141 | Distinguish GM-change 0.25 s tu from recommended 5 s media-clock holdover |
| asCapable continuity | Milan 4.2.6.2.4 | 24 | The asCapable clause; preceding clauses address tolerance tables |
| Sampling rate | Milan 5.3.5.1 | 36 | Persistent sampling rate |
| Output format / presentation offset | Milan 5.3.7.1 / 5.3.7.6 | 37, 39 | Persistent output state |
| Input format | Milan 5.3.8.1 | 40 | Persistent input format |
| Bound state / binding parameters | Milan 5.3.8.2 / 5.3.8.3 | 41 | Today's stream-binding inventory |
| Input started/stopped state | Milan 5.3.8.7 | 42 | Persistent listener state |
| Audio maps / clock source | Milan 5.3.9.1 / 5.3.10.1 / 5.3.11.1 | 45 | Persistent maps and clock source |
| User names | Milan 5.3.13 | 46-47 | Persistent user names |
| ADP valid_time | IEEE 1722.1-2021 6.2.2.5 | 49 | Decoded in two-second units |
| ADP advertising | IEEE 1722.1-2021 6.2.4 / 6.2.5; Milan 5.6.3 | 56-57; 109-111 | Advertising behavior, separate from discovery clause 6.2.6 |
| Automatic restoration | Milan 5.5.1.4 / 5.5.2.6 | 72-73, 76 | Automatic listener connection |
| Additional controller reconnect | Milan 5.5.2.4 | 75 | Controller Bind, distinct from automatic restoration |

The pre-cut advertisement expiry rule, T0 origin, provisional 30-second
restoration bound, seven-day duration, 60-second sampling ceiling, 200-cut
phase mix, single-boot criterion, and five-second diagnostic margin are
project release policy. The additional one-second reconnect bound comes
from issue #75. The standards citations identify the associated protocol
behavior; they do not establish those project limits.

Milan 5.3.2 and IEEE 1722.1-2021 7.4.7 were also checked for configuration
retention. Neither is cited as a persistence requirement. Additional declared
state is governed by the project inventory. Existing citations outside the
release contract were left outside this assignment.
