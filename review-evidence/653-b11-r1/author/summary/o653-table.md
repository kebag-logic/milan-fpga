| Cycle | Input | Bind | Lock (ms) | Hold (ms) | UNBIND_RX cmd to rsp (us) | Rsp to unlock push (us) | Wire order | Decoder order | Pushed ML/MU/SI | Stream frames after cmd | Library: conn at unlock update | Library flags | Library pair after |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s0b/C0 | 0 | Success | 1003 | 2000 | 7.5 | 115.4 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1168 | NotConnected | none | 1/1/0 |
| s0b/C0 control | 0 | own GET_COUNTERS {'ML': 1, 'MU': 0, 'SI': 0} | | | | | COUNTERS_FIRST (vs own response) | | | | | | |
| s1/A01 | 0 | Success | 1003 | 2000 | 7.5 | 115.5 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 303 | NotConnected | none | 1/1/0 |
| s1/A02 | 0 | Success | 1003 | 2137 | 7.5 | 114.2 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 448 | NotConnected | none | 1/1/0 |
| s1/A03 | 0 | Success | 1003 | 2274 | 7.5 | 114.5 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1111 | NotConnected | none | 1/1/0 |
| s1/A04 | 0 | Success | 1003 | 2411 | 7.5 | 116.8 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 776 | NotConnected | none | 1/1/0 |
| s1/A05 | 0 | Success | 1003 | 2548 | 7.5 | 115.4 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 799 | NotConnected | none | 1/1/0 |
| s1/A06 | 0 | Success | 1003 | 2685 | 7.5 | 116.8 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1304 | NotConnected | none | 1/1/0 |
| s1/A07 | 0 | Success | 1003 | 2822 | 7.5 | 116.1 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 848 | NotConnected | none | 1/1/0 |
| s1/A08 | 0 | Success | 1003 | 2959 | 7.5 | 114.8 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 867 | NotConnected | none | 1/1/0 |
| s1/A09 | 0 | Success | 1003 | 2096 | 7.5 | 115.4 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1297 | NotConnected | none | 1/1/0 |
| s1/A10 | 0 | Success | 1003 | 2233 | 7.5 | 115.1 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 640 | NotConnected | none | 1/1/0 |
| s1/A11 | 0 | Success | 1003 | 2370 | 7.5 | 116.0 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 425 | NotConnected | none | 1/1/0 |
| s1/A12 | 0 | Success | 1003 | 2507 | 7.5 | 116.8 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 729 | NotConnected | none | 1/1/0 |
| s1/A13 | 0 | Success | 1003 | 2644 | 7.5 | 114.9 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1513 | NotConnected | none | 1/1/0 |
| s1/A14 | 0 | Success | 1003 | 2781 | 7.5 | 116.0 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1256 | NotConnected | none | 1/1/0 |
| s1/A15 | 0 | Success | 1003 | 2918 | 7.5 | 115.7 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1562 | NotConnected | none | 1/1/0 |
| s1/A16 | 0 | Success | 1003 | 2055 | 7.5 | 115.4 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 746 | NotConnected | none | 1/1/0 |
| s1/A17 | 0 | Success | 1003 | 2192 | 7.5 | 116.2 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 410 | NotConnected | none | 1/1/0 |
| s1/A18 | 0 | Success | 1003 | 2329 | 7.5 | 114.8 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 485 | NotConnected | none | 1/1/0 |
| s1/A19 | 0 | Success | 1003 | 2466 | 7.5 | 115.3 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 1057 | NotConnected | none | 1/1/0 |
| s1/A20 | 0 | Success | 1003 | 2603 | 7.5 | 116.2 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 442 | NotConnected | none | 1/1/0 |
| s1/R01 | 1 | Success | 1003 | 2740 | 7.5 | 99346.2 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 32 | NotConnected | none | 1/1/0 |
| s1/R02 | 1 | Success | 1003 | 2877 | 7.5 | 99731.4 | RESPONSE_FIRST | RESPONSE_FIRST | 1/1/0 | 18 | NotConnected | none | 1/1/0 |
