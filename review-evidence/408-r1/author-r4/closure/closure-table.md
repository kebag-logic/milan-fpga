# Character-closure table

2520 cells (280 sequences x 9 positions): A 1427, a 43, S 32, = 1018, X 0, ! 0; other rules of S: SUBSET_DOLLAR_PIN 6, SUBSET_UCN_PIN 6, UNTERMINATED_PIN 20

- P1: at offset 0, before `#`
- P2: in a line's lead before `#`
- P3: between `#` and a directive name
- P4: inside a directive name
- P5: after a directive name
- P6: inside an identifier in code
- P7: inside a block comment
- P8: inside a string literal
- P9: inside a character literal

| sequence | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 |
|---|---|---|---|---|---|---|---|---|---|
| byte 0x00 | = | = | = | = | = | = | = | = | = |
| byte 0x01 | A | A | A | A | A | A | = | = | = |
| byte 0x02 | A | A | A | A | A | A | = | = | = |
| byte 0x03 | A | A | A | A | A | A | = | = | = |
| byte 0x04 | A | A | A | A | A | A | = | = | = |
| byte 0x05 | A | A | A | A | A | A | = | = | = |
| byte 0x06 | A | A | A | A | A | A | = | = | = |
| byte 0x07 | A | A | A | A | A | A | = | = | = |
| byte 0x08 | A | A | A | A | A | A | = | = | = |
| byte 0x09 | = | = | = | = | = | = | = | = | = |
| byte 0x0a | = | = | = | = | = | = | = | S | S |
| byte 0x0b | = | = | = | = | = | = | = | = | = |
| byte 0x0c | = | = | = | = | = | = | = | = | = |
| byte 0x0d | = | = | = | = | = | = | = | S | S |
| byte 0x0e | A | A | A | A | A | A | = | = | = |
| byte 0x0f | A | A | A | A | A | A | = | = | = |
| byte 0x10 | A | A | A | A | A | A | = | = | = |
| byte 0x11 | A | A | A | A | A | A | = | = | = |
| byte 0x12 | A | A | A | A | A | A | = | = | = |
| byte 0x13 | A | A | A | A | A | A | = | = | = |
| byte 0x14 | A | A | A | A | A | A | = | = | = |
| byte 0x15 | A | A | A | A | A | A | = | = | = |
| byte 0x16 | A | A | A | A | A | A | = | = | = |
| byte 0x17 | A | A | A | A | A | A | = | = | = |
| byte 0x18 | A | A | A | A | A | A | = | = | = |
| byte 0x19 | A | A | A | A | A | A | = | = | = |
| byte 0x1a | A | A | A | A | A | A | = | = | = |
| byte 0x1b | A | A | A | A | A | A | = | = | = |
| byte 0x1c | A | A | A | A | A | A | = | = | = |
| byte 0x1d | A | A | A | A | A | A | = | = | = |
| byte 0x1e | A | A | A | A | A | A | = | = | = |
| byte 0x1f | A | A | A | A | A | A | = | = | = |
| byte 0x20 | = | = | = | = | = | = | = | = | = |
| byte 0x21 | = | = | = | = | = | = | = | = | = |
| byte 0x22 | S | S | S | S | S | S | = | S | = |
| byte 0x23 | = | = | = | = | = | = | = | = | = |
| byte 0x24 | S | S | S | S | S | S | = | = | = |
| byte 0x25 | = | = | = | = | = | = | = | = | = |
| byte 0x26 | = | = | = | = | = | = | = | = | = |
| byte 0x27 | S | S | S | S | S | S | = | = | S |
| byte 0x28 | = | = | = | = | = | = | = | = | = |
| byte 0x29 | = | = | = | = | = | = | = | = | = |
| byte 0x2a | = | = | = | = | = | = | = | = | = |
| byte 0x2b | = | = | = | = | = | = | = | = | = |
| byte 0x2c | = | = | = | = | = | = | = | = | = |
| byte 0x2d | = | = | = | = | = | = | = | = | = |
| byte 0x2e | = | = | = | = | = | = | = | = | = |
| byte 0x2f | = | = | = | = | = | = | = | = | = |
| byte 0x30 | = | = | = | = | = | = | = | = | = |
| byte 0x31 | = | = | = | = | = | = | = | = | = |
| byte 0x32 | = | = | = | = | = | = | = | = | = |
| byte 0x33 | = | = | = | = | = | = | = | = | = |
| byte 0x34 | = | = | = | = | = | = | = | = | = |
| byte 0x35 | = | = | = | = | = | = | = | = | = |
| byte 0x36 | = | = | = | = | = | = | = | = | = |
| byte 0x37 | = | = | = | = | = | = | = | = | = |
| byte 0x38 | = | = | = | = | = | = | = | = | = |
| byte 0x39 | = | = | = | = | = | = | = | = | = |
| byte 0x3a | = | = | = | = | = | = | = | = | = |
| byte 0x3b | = | = | = | = | = | = | = | = | = |
| byte 0x3c | = | = | = | = | = | = | = | = | = |
| byte 0x3d | = | = | = | = | = | = | = | = | = |
| byte 0x3e | = | = | = | = | = | = | = | = | = |
| byte 0x3f | = | = | = | = | = | = | = | = | = |
| byte 0x40 | = | = | = | = | = | = | = | = | = |
| byte 0x41 | = | = | = | = | = | = | = | = | = |
| byte 0x42 | = | = | = | = | = | = | = | = | = |
| byte 0x43 | = | = | = | = | = | = | = | = | = |
| byte 0x44 | = | = | = | = | = | = | = | = | = |
| byte 0x45 | = | = | = | = | = | = | = | = | = |
| byte 0x46 | = | = | = | = | = | = | = | = | = |
| byte 0x47 | = | = | = | = | = | = | = | = | = |
| byte 0x48 | = | = | = | = | = | = | = | = | = |
| byte 0x49 | = | = | = | = | = | = | = | = | = |
| byte 0x4a | = | = | = | = | = | = | = | = | = |
| byte 0x4b | = | = | = | = | = | = | = | = | = |
| byte 0x4c | = | = | = | = | = | = | = | = | = |
| byte 0x4d | = | = | = | = | = | = | = | = | = |
| byte 0x4e | = | = | = | = | = | = | = | = | = |
| byte 0x4f | = | = | = | = | = | = | = | = | = |
| byte 0x50 | = | = | = | = | = | = | = | = | = |
| byte 0x51 | = | = | = | = | = | = | = | = | = |
| byte 0x52 | = | = | = | = | = | = | = | = | = |
| byte 0x53 | = | = | = | = | = | = | = | = | = |
| byte 0x54 | = | = | = | = | = | = | = | = | = |
| byte 0x55 | = | = | = | = | = | = | = | = | = |
| byte 0x56 | = | = | = | = | = | = | = | = | = |
| byte 0x57 | = | = | = | = | = | = | = | = | = |
| byte 0x58 | = | = | = | = | = | = | = | = | = |
| byte 0x59 | = | = | = | = | = | = | = | = | = |
| byte 0x5a | = | = | = | = | = | = | = | = | = |
| byte 0x5b | = | = | = | = | = | = | = | = | = |
| byte 0x5c | S | S | S | S | S | S | = | S | S |
| byte 0x5d | = | = | = | = | = | = | = | = | = |
| byte 0x5e | = | = | = | = | = | = | = | = | = |
| byte 0x5f | = | = | = | = | = | = | = | = | = |
| byte 0x60 | = | = | = | = | = | = | = | = | = |
| byte 0x61 | = | = | = | = | = | = | = | = | = |
| byte 0x62 | = | = | = | = | = | = | = | = | = |
| byte 0x63 | = | = | = | = | = | = | = | = | = |
| byte 0x64 | = | = | = | = | = | = | = | = | = |
| byte 0x65 | = | = | = | = | = | = | = | = | = |
| byte 0x66 | = | = | = | = | = | = | = | = | = |
| byte 0x67 | = | = | = | = | = | = | = | = | = |
| byte 0x68 | = | = | = | = | = | = | = | = | = |
| byte 0x69 | = | = | = | = | = | = | = | = | = |
| byte 0x6a | = | = | = | = | = | = | = | = | = |
| byte 0x6b | = | = | = | = | = | = | = | = | = |
| byte 0x6c | = | = | = | = | = | = | = | = | = |
| byte 0x6d | = | = | = | = | = | = | = | = | = |
| byte 0x6e | = | = | = | = | = | = | = | = | = |
| byte 0x6f | = | = | = | = | = | = | = | = | = |
| byte 0x70 | = | = | = | = | = | = | = | = | = |
| byte 0x71 | = | = | = | = | = | = | = | = | = |
| byte 0x72 | = | = | = | = | = | = | = | = | = |
| byte 0x73 | = | = | = | = | = | = | = | = | = |
| byte 0x74 | = | = | = | = | = | = | = | = | = |
| byte 0x75 | = | = | = | = | = | = | = | = | = |
| byte 0x76 | = | = | = | = | = | = | = | = | = |
| byte 0x77 | = | = | = | = | = | = | = | = | = |
| byte 0x78 | = | = | = | = | = | = | = | = | = |
| byte 0x79 | = | = | = | = | = | = | = | = | = |
| byte 0x7a | = | = | = | = | = | = | = | = | = |
| byte 0x7b | = | = | = | = | = | = | = | = | = |
| byte 0x7c | = | = | = | = | = | = | = | = | = |
| byte 0x7d | = | = | = | = | = | = | = | = | = |
| byte 0x7e | = | = | = | = | = | = | = | = | = |
| byte 0x7f | A | A | A | A | A | A | = | = | = |
| byte 0x80 | A | A | A | A | A | A | A | A | A |
| byte 0x81 | A | A | A | A | A | A | A | A | A |
| byte 0x82 | A | A | A | A | A | A | A | A | A |
| byte 0x83 | A | A | A | A | A | A | A | A | A |
| byte 0x84 | A | A | A | A | A | A | A | A | A |
| byte 0x85 | A | A | A | A | A | A | A | A | A |
| byte 0x86 | A | A | A | A | A | A | A | A | A |
| byte 0x87 | A | A | A | A | A | A | A | A | A |
| byte 0x88 | A | A | A | A | A | A | A | A | A |
| byte 0x89 | A | A | A | A | A | A | A | A | A |
| byte 0x8a | A | A | A | A | A | A | A | A | A |
| byte 0x8b | A | A | A | A | A | A | A | A | A |
| byte 0x8c | A | A | A | A | A | A | A | A | A |
| byte 0x8d | A | A | A | A | A | A | A | A | A |
| byte 0x8e | A | A | A | A | A | A | A | A | A |
| byte 0x8f | A | A | A | A | A | A | A | A | A |
| byte 0x90 | A | A | A | A | A | A | A | A | A |
| byte 0x91 | A | A | A | A | A | A | A | A | A |
| byte 0x92 | A | A | A | A | A | A | A | A | A |
| byte 0x93 | A | A | A | A | A | A | A | A | A |
| byte 0x94 | A | A | A | A | A | A | A | A | A |
| byte 0x95 | A | A | A | A | A | A | A | A | A |
| byte 0x96 | A | A | A | A | A | A | A | A | A |
| byte 0x97 | A | A | A | A | A | A | A | A | A |
| byte 0x98 | A | A | A | A | A | A | A | A | A |
| byte 0x99 | A | A | A | A | A | A | A | A | A |
| byte 0x9a | A | A | A | A | A | A | A | A | A |
| byte 0x9b | A | A | A | A | A | A | A | A | A |
| byte 0x9c | A | A | A | A | A | A | A | A | A |
| byte 0x9d | A | A | A | A | A | A | A | A | A |
| byte 0x9e | A | A | A | A | A | A | A | A | A |
| byte 0x9f | A | A | A | A | A | A | A | A | A |
| byte 0xa0 | A | A | A | A | A | A | A | A | A |
| byte 0xa1 | A | A | A | A | A | A | A | A | A |
| byte 0xa2 | A | A | A | A | A | A | A | A | A |
| byte 0xa3 | A | A | A | A | A | A | A | A | A |
| byte 0xa4 | A | A | A | A | A | A | A | A | A |
| byte 0xa5 | A | A | A | A | A | A | A | A | A |
| byte 0xa6 | A | A | A | A | A | A | A | A | A |
| byte 0xa7 | A | A | A | A | A | A | A | A | A |
| byte 0xa8 | A | A | A | A | A | A | A | A | A |
| byte 0xa9 | A | A | A | A | A | A | A | A | A |
| byte 0xaa | A | A | A | A | A | A | A | A | A |
| byte 0xab | A | A | A | A | A | A | A | A | A |
| byte 0xac | A | A | A | A | A | A | A | A | A |
| byte 0xad | A | A | A | A | A | A | A | A | A |
| byte 0xae | A | A | A | A | A | A | A | A | A |
| byte 0xaf | A | A | A | A | A | A | A | A | A |
| byte 0xb0 | A | A | A | A | A | A | A | A | A |
| byte 0xb1 | A | A | A | A | A | A | A | A | A |
| byte 0xb2 | A | A | A | A | A | A | A | A | A |
| byte 0xb3 | A | A | A | A | A | A | A | A | A |
| byte 0xb4 | A | A | A | A | A | A | A | A | A |
| byte 0xb5 | A | A | A | A | A | A | A | A | A |
| byte 0xb6 | A | A | A | A | A | A | A | A | A |
| byte 0xb7 | A | A | A | A | A | A | A | A | A |
| byte 0xb8 | A | A | A | A | A | A | A | A | A |
| byte 0xb9 | A | A | A | A | A | A | A | A | A |
| byte 0xba | A | A | A | A | A | A | A | A | A |
| byte 0xbb | A | A | A | A | A | A | A | A | A |
| byte 0xbc | A | A | A | A | A | A | A | A | A |
| byte 0xbd | A | A | A | A | A | A | A | A | A |
| byte 0xbe | A | A | A | A | A | A | A | A | A |
| byte 0xbf | A | A | A | A | A | A | A | A | A |
| byte 0xc0 | A | A | A | A | A | A | A | A | A |
| byte 0xc1 | A | A | A | A | A | A | A | A | A |
| byte 0xc2 | A | A | A | A | A | A | A | A | A |
| byte 0xc3 | A | A | A | A | A | A | A | A | A |
| byte 0xc4 | A | A | A | A | A | A | A | A | A |
| byte 0xc5 | A | A | A | A | A | A | A | A | A |
| byte 0xc6 | A | A | A | A | A | A | A | A | A |
| byte 0xc7 | A | A | A | A | A | A | A | A | A |
| byte 0xc8 | A | A | A | A | A | A | A | A | A |
| byte 0xc9 | A | A | A | A | A | A | A | A | A |
| byte 0xca | A | A | A | A | A | A | A | A | A |
| byte 0xcb | A | A | A | A | A | A | A | A | A |
| byte 0xcc | A | A | A | A | A | A | A | A | A |
| byte 0xcd | A | A | A | A | A | A | A | A | A |
| byte 0xce | A | A | A | A | A | A | A | A | A |
| byte 0xcf | A | A | A | A | A | A | A | A | A |
| byte 0xd0 | A | A | A | A | A | A | A | A | A |
| byte 0xd1 | A | A | A | A | A | A | A | A | A |
| byte 0xd2 | A | A | A | A | A | A | A | A | A |
| byte 0xd3 | A | A | A | A | A | A | A | A | A |
| byte 0xd4 | A | A | A | A | A | A | A | A | A |
| byte 0xd5 | A | A | A | A | A | A | A | A | A |
| byte 0xd6 | A | A | A | A | A | A | A | A | A |
| byte 0xd7 | A | A | A | A | A | A | A | A | A |
| byte 0xd8 | A | A | A | A | A | A | A | A | A |
| byte 0xd9 | A | A | A | A | A | A | A | A | A |
| byte 0xda | A | A | A | A | A | A | A | A | A |
| byte 0xdb | A | A | A | A | A | A | A | A | A |
| byte 0xdc | A | A | A | A | A | A | A | A | A |
| byte 0xdd | A | A | A | A | A | A | A | A | A |
| byte 0xde | A | A | A | A | A | A | A | A | A |
| byte 0xdf | A | A | A | A | A | A | A | A | A |
| byte 0xe0 | A | A | A | A | A | A | A | A | A |
| byte 0xe1 | A | A | A | A | A | A | A | A | A |
| byte 0xe2 | A | A | A | A | A | A | A | A | A |
| byte 0xe3 | A | A | A | A | A | A | A | A | A |
| byte 0xe4 | A | A | A | A | A | A | A | A | A |
| byte 0xe5 | A | A | A | A | A | A | A | A | A |
| byte 0xe6 | A | A | A | A | A | A | A | A | A |
| byte 0xe7 | A | A | A | A | A | A | A | A | A |
| byte 0xe8 | A | A | A | A | A | A | A | A | A |
| byte 0xe9 | A | A | A | A | A | A | A | A | A |
| byte 0xea | A | A | A | A | A | A | A | A | A |
| byte 0xeb | A | A | A | A | A | A | A | A | A |
| byte 0xec | A | A | A | A | A | A | A | A | A |
| byte 0xed | A | A | A | A | A | A | A | A | A |
| byte 0xee | A | A | A | A | A | A | A | A | A |
| byte 0xef | A | A | A | A | A | A | A | A | A |
| byte 0xf0 | A | A | A | A | A | A | A | A | A |
| byte 0xf1 | A | A | A | A | A | A | A | A | A |
| byte 0xf2 | A | A | A | A | A | A | A | A | A |
| byte 0xf3 | A | A | A | A | A | A | A | A | A |
| byte 0xf4 | A | A | A | A | A | A | A | A | A |
| byte 0xf5 | A | A | A | A | A | A | A | A | A |
| byte 0xf6 | A | A | A | A | A | A | A | A | A |
| byte 0xf7 | A | A | A | A | A | A | A | A | A |
| byte 0xf8 | A | A | A | A | A | A | A | A | A |
| byte 0xf9 | A | A | A | A | A | A | A | A | A |
| byte 0xfa | A | A | A | A | A | A | A | A | A |
| byte 0xfb | A | A | A | A | A | A | A | A | A |
| byte 0xfc | A | A | A | A | A | A | A | A | A |
| byte 0xfd | A | A | A | A | A | A | A | A | A |
| byte 0xfe | A | A | A | A | A | A | A | A | A |
| byte 0xff | A | A | A | A | A | A | A | A | A |
| U+0085 | A | A | A | A | A | A | = | = | = |
| U+00A0 | A | A | A | A | A | A | = | = | = |
| U+00B2 | A | A | A | a | a | a | = | = | = |
| U+00B5 | A | A | A | a | a | a | = | = | = |
| U+00B7 | A | A | A | a | a | a | = | = | = |
| U+00E9 | A | A | A | a | a | a | = | = | = |
| U+0301 | A | a | A | a | a | a | = | = | = |
| U+0387 | A | A | A | a | a | a | = | = | = |
| U+0661 | A | A | A | a | a | a | = | = | = |
| U+200B | A | A | A | a | a | a | = | = | = |
| U+2028 | A | A | A | A | A | A | = | = | = |
| U+2029 | A | A | A | A | A | A | = | = | = |
| U+203F | A | A | A | a | a | a | = | = | = |
| U+2460 | A | A | A | a | a | a | = | = | = |
| U+3000 | A | A | A | A | A | A | = | = | = |
| U+4E2D | A | A | A | a | a | a | = | = | = |
| U+FEFF | A | A | A | a | a | a | = | = | = |
| U+FF21 | A | A | A | a | a | a | = | = | = |
| U+1F600 | A | A | A | a | a | a | = | = | = |
| U+10FFFF | A | A | A | A | A | A | = | = | = |
| bytes c0 af (not UTF-8) | A | A | A | A | A | A | A | A | A |
| bytes ed a0 80 (not UTF-8) | A | A | A | A | A | A | A | A | A |
| bytes e2 80 (not UTF-8) | A | A | A | A | A | A | A | A | A |
| bytes f8 88 80 80 80 (not UTF-8) | A | A | A | A | A | A | A | A | A |
