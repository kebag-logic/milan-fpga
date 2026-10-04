<!-- per-cycle -->
| Cycle | Stream, DUT input | MEDIA_LOCKED reported after bind (ms) | Hold (ms) | UNBIND_RX command to response (µs) | Response to the unlock's GET_COUNTERS (µs) | Order at the DUT's port | Pushed LOCKED/UNLOCKED/INTERRUPTED | Stream frames after the command | Library: input state at that update | Library flags | Library pair after | Capture |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 (control) | AAF, 0 | 1003 | 2000 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 1,168 | NotConnected | none | 1/1/0 | `4fa8c57c4b58` |
| A01 | AAF, 0 | 1003 | 2000 | 7.5 | 115.5 | RESPONSE_FIRST | 1/1/0 | 303 | NotConnected | none | 1/1/0 | `6e2879e6ad58` |
| A02 | AAF, 0 | 1003 | 2137 | 7.5 | 114.2 | RESPONSE_FIRST | 1/1/0 | 448 | NotConnected | none | 1/1/0 | `2da6e350212c` |
| A03 | AAF, 0 | 1003 | 2274 | 7.5 | 114.5 | RESPONSE_FIRST | 1/1/0 | 1,111 | NotConnected | none | 1/1/0 | `95ece933ecb6` |
| A04 | AAF, 0 | 1003 | 2411 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 776 | NotConnected | none | 1/1/0 | `a2cb6bd81919` |
| A05 | AAF, 0 | 1003 | 2548 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 799 | NotConnected | none | 1/1/0 | `03ba3c61e102` |
| A06 | AAF, 0 | 1003 | 2685 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 1,304 | NotConnected | none | 1/1/0 | `c3861dbadd69` |
| A07 | AAF, 0 | 1003 | 2822 | 7.5 | 116.1 | RESPONSE_FIRST | 1/1/0 | 848 | NotConnected | none | 1/1/0 | `303d24587e20` |
| A08 | AAF, 0 | 1003 | 2959 | 7.5 | 114.8 | RESPONSE_FIRST | 1/1/0 | 867 | NotConnected | none | 1/1/0 | `9e34b4baa256` |
| A09 | AAF, 0 | 1003 | 2096 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 1,297 | NotConnected | none | 1/1/0 | `bd9f74e69513` |
| A10 | AAF, 0 | 1003 | 2233 | 7.5 | 115.1 | RESPONSE_FIRST | 1/1/0 | 640 | NotConnected | none | 1/1/0 | `d9469de78767` |
| A11 | AAF, 0 | 1003 | 2370 | 7.5 | 116.0 | RESPONSE_FIRST | 1/1/0 | 425 | NotConnected | none | 1/1/0 | `9a8f2c276fef` |
| A12 | AAF, 0 | 1003 | 2507 | 7.5 | 116.8 | RESPONSE_FIRST | 1/1/0 | 729 | NotConnected | none | 1/1/0 | `80983fa9bd3e` |
| A13 | AAF, 0 | 1003 | 2644 | 7.5 | 114.9 | RESPONSE_FIRST | 1/1/0 | 1,513 | NotConnected | none | 1/1/0 | `6f0de98ab446` |
| A14 | AAF, 0 | 1003 | 2781 | 7.5 | 116.0 | RESPONSE_FIRST | 1/1/0 | 1,256 | NotConnected | none | 1/1/0 | `dd5774b30f8c` |
| A15 | AAF, 0 | 1003 | 2918 | 7.5 | 115.7 | RESPONSE_FIRST | 1/1/0 | 1,562 | NotConnected | none | 1/1/0 | `6f7c12331830` |
| A16 | AAF, 0 | 1003 | 2055 | 7.5 | 115.4 | RESPONSE_FIRST | 1/1/0 | 746 | NotConnected | none | 1/1/0 | `b8293ce029b5` |
| A17 | AAF, 0 | 1003 | 2192 | 7.5 | 116.2 | RESPONSE_FIRST | 1/1/0 | 410 | NotConnected | none | 1/1/0 | `7321a54e63dd` |
| A18 | AAF, 0 | 1003 | 2329 | 7.5 | 114.8 | RESPONSE_FIRST | 1/1/0 | 485 | NotConnected | none | 1/1/0 | `d23198019e43` |
| A19 | AAF, 0 | 1003 | 2466 | 7.5 | 115.3 | RESPONSE_FIRST | 1/1/0 | 1,057 | NotConnected | none | 1/1/0 | `008deccfe05f` |
| A20 | AAF, 0 | 1003 | 2603 | 7.5 | 116.2 | RESPONSE_FIRST | 1/1/0 | 442 | NotConnected | none | 1/1/0 | `8e07888e2ba3` |
| R01 | CRF, 1 | 1003 | 2740 | 7.5 | 99,346.2 | RESPONSE_FIRST | 1/1/0 | 32 | NotConnected | none | 1/1/0 | `970a213ab53c` |
| R02 | CRF, 1 | 1003 | 2877 | 7.5 | 99,731.4 | RESPONSE_FIRST | 1/1/0 | 18 | NotConnected | none | 1/1/0 | `c743c09453ab` |

<!-- hashes -->
| Capture | Bytes | SHA-256 |
|---|---|---|
| `b11-a535-s0b-C0.pcap` | 4,385,862 | `4fa8c57c4b58ff3d1ce4fb9c7a25c9a71b0ca6bad107579fc537507a01bbef10` |
| `b11-a535-s1-A01.pcap` | 4,387,470 | `6e2879e6ad58674714d984ed5feff65c527ba90ec2496e99ba64661f375cbe78` |
| `b11-a535-s1-A02.pcap` | 4,463,782 | `2da6e350212c19bcaf11820ef981b11e9d7dab4b2e7a2c9e6c4c1347e3ca2187` |
| `b11-a535-s1-A03.pcap` | 5,058,874 | `95ece933ecb628125e48f7ab7bf0659257e87fbf30874387ebdcda0710ee3279` |
| `b11-a535-s1-A04.pcap` | 5,058,984 | `a2cb6bd81919b1bb9ccc3b1a5ed4387c57795e3b77bcff60e88b0f0dd940e4ef` |
| `b11-a535-s1-A05.pcap` | 5,356,290 | `03ba3c61e102d586e36ccba9f0eb1c3ecb43438f6acf64c054c989c2fd2252dd` |
| `b11-a535-s1-A06.pcap` | 5,653,836 | `c3861dbadd690456b50c251b4b43309a858224df11cae94eeaed1cf04e98d65a` |
| `b11-a535-s1-A07.pcap` | 5,654,184 | `303d24587e209f1f8650f17e51ef85b121f45fa6d9d0250b4408a0f8964da408` |
| `b11-a535-s1-A08.pcap` | 5,951,654 | `9e34b4baa2562a51e16dc7bb5ea982dd3cccd8ff6fc535f8026f38f798052c4b` |
| `b11-a535-s1-A09.pcap` | 4,761,490 | `bd9f74e6951333a4d60314ce14e5542e387cf47e140f60cd41dc807f24888b41` |
| `b11-a535-s1-A10.pcap` | 4,761,330 | `d9469de78767d7a6530f4d7f19a4cac9b7d7eb5955a45befa4043e4bbbf4b787` |
| `b11-a535-s1-A11.pcap` | 5,058,580 | `9a8f2c276feff3c4cbae858b1cbe1d5a44b20ea24fec382733cf80f1cb75d0e7` |
| `b11-a535-s1-A12.pcap` | 5,058,854 | `80983fa9bd3e92815b81612be22d86281f690cc5fa974bf59d7755c6830f5335` |
| `b11-a535-s1-A13.pcap` | 5,653,944 | `6f0de98ab4468ccd9026b0e623b4cdacc8f8a0dc366b1a27b5bc13d94265f692` |
| `b11-a535-s1-A14.pcap` | 5,654,074 | `dd5774b30f8c07dffc5ed2ed2cd3e3abac2746f97e749313b1d358b19ca74b25` |
| `b11-a535-s1-A15.pcap` | 5,951,784 | `6f7c123318303584ad43da24b0829480e377f8da1f4b72abd6d889d29c14f32e` |
| `b11-a535-s1-A16.pcap` | 4,463,674 | `b8293ce029b5a28a9763ed9e5ece5a4940922aed2b603a6133ecef146e22c4ef` |
| `b11-a535-s1-A17.pcap` | 4,761,274 | `7321a54e63ddb8db360e5aff96fa855c3dccd6a8a9d4a7c9b80c0d170990fa0a` |
| `b11-a535-s1-A18.pcap` | 4,763,350 | `d23198019e434c60fae86c6832a229585f932aec55d6ccc6e0566d0c07012caa` |
| `b11-a535-s1-A19.pcap` | 5,058,798 | `008deccfe05f3c9055871989bfc5ac531a166dc6a873dfa4756c0ca8ee1223b3` |
| `b11-a535-s1-A20.pcap` | 5,356,160 | `8e07888e2ba37232fb64e48c5236ea39046199db0fa0c1e7b8e7877a610b0463` |
| `b11-a535-s1-R01.pcap` | 209,072 | `970a213ab53c7797e463ae3ffb23dcaba88e0db65a08d7339bba73ee7b8eaba9` |
| `b11-a535-s1-R02.pcap` | 208,964 | `c743c09453ab8669b74523b5fe5708a27c53bc2850405a346d35d3ecb628ab84` |

<!-- ranges -->
```
{
 "AAF-cmd_to_rsp_us": [
  7.5,
  7.5
 ],
 "AAF-rsp_to_push_us": [
  114.2,
  116.8
 ],
 "AAF-frames_after_cmd": [
  303,
  1562
 ],
 "AAF-last_frame_ms": [
  37.811,
  195.163
 ],
 "AAF-lib_unlock_after_unbind_ms": [
  0.919,
  5.221
 ],
 "AAF-lib_held_ms": [
  0.051,
  0.113
 ],
 "AAF-lock_ms": [
  1003,
  1003
 ],
 "control": {
  "own_counters": {
   "ML": 1,
   "MU": 0,
   "SI": 0
  },
  "order_vs_own": "COUNTERS_FIRST",
  "own_rsp_to_cmd_us": 1629.8
 },
 "orders": {
  "RESPONSE_FIRST": 23
 },
 "decoder_orders": {
  "RESPONSE_FIRST": 23
 },
 "between": {
  "DUT->sw UNSOL GET_STREAM_INFO RSP": 22,
  "DUT->sw UNSOL GET_STREAM_INFO RSP / DUT->sw UNSOL 0x27 RSP": 1
 },
 "monotonic": [
  true
 ],
 "CRF-cmd_to_rsp_us": [
  7.5,
  7.5
 ],
 "CRF-rsp_to_push_us": [
  99346.2,
  99731.4
 ],
 "CRF-frames_after_cmd": [
  18,
  32
 ],
 "CRF-last_frame_ms": [
  35.664,
  63.282
 ],
 "CRF-lib_unlock_after_unbind_ms": [
  99.853,
  102.891
 ],
 "CRF-lib_held_ms": [
  95.0,
  100.016
 ],
 "CRF-lock_ms": [
  1003,
  1003
 ]
}
```
