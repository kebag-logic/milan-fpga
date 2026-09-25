| case | r2-head-sdk | r2-head-sdk-disconnect | r2-base-sdk | r2-head-absent | r2-head-absent-disconnect |
|---|---|---|---|---|---|
| CTRL unchanged firmware | ACC | ACC | ACC | ACC | ACC |
| EXC-OK discarded mask hex literal (void)(id & 0xffu); | ACC | ACC | ACC | ACC | ACC |
| EXC-OK discarded mask no blanks (void)(id&1); | ACC | ACC | ACC | ACC | ACC |
| EXC-OK discarded mask ull suffix (void)(id & 0x1ull); | ACC | ACC | ACC | ACC | ACC |
| EXC-OK discarded mask macro literal (void)(id & MILAN_ID_MAGIC); | ACC | ACC | ACC | ACC | ACC |
| EXC-OK second diagnostic call argument | ACC | ACC | ACC | ACC | ACC |
| EXC-OK two sample arguments in one call | ACC | ACC | ACC | ACC | ACC |
| NEAR argument followed by + 1u | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument followed by conditional | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument extra parentheses (unsigned long)(x) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument then comma assignment in a second statement expr | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument postfix increment | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument cast unsigned long int | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument cast unsigned int | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument via parenthesized callee (printf)(...) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument in statement expression that assigns | REF:other | REF:other | REF:other | REF:MACRO | ACC |
| NEAR argument in sizeof | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument in array subscript | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR argument of __typeof__ declaration then assignment | REF:other | REF:other | REF:other | REF:MACRO | ACC |
| NEAR statement two masks (void)(x & 1u & 3u) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR statement negative literal (void)(x & -1) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR statement char literal (void)(x & '\1') | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR statement under if (1) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR statement followed by & 2u | REF:SAMPLE | REF:other | REF:other | REF:MACRO | ACC |
| NEAR statement mask operand reversed (void)(1u & x) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR statement mask then pre-increment in next statement | REF:other | REF:other | REF:other | REF:MACRO | ACC |
| NEAR statement mask in comma with assignment | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR printf macro routes the argument into a conditional | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| NEAR printf macro keeps a delimited argument and reuses it wrapped | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC |
| LIM printf macro forwards the argument to a benign identifier call | ACC | ACC | ACC | REF:MACRO | ACC |
| ESC sizeof &id after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC __typeof__(&id) after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC asm m input after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC asm +m output after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC pointer initialised from &id after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC &id + 0 after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| ESC macro &(x) after guard | REF:SAMPLE | ACC | ACC | ACC | ACC |
| LIM asm +r output after guard (no address, after the interval) | ACC | ACC | ACC | ACC | ACC |
| BOUND C03 header paste | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND C05 macro using header paste | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND C13 object-like macro alias | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND writer alias | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND writer apply | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND C16 parenthesized assignment | REF:SAMPLE | ACC | ACC | ACC | ACC |
| BOUND C17 indirect assignment | REF:SAMPLE | ACC | ACC | ACC | ACC |
| LIM callee asm clobbers a callee-saved register, called in interval | ACC | ACC | ACC | ACC | ACC |
| LIM frame-address store in interval | REF:other | REF:other | REF:other | REF:other | REF:other |
| LIM backward goto writes after the guard | REF:other | REF:other | REF:other | REF:other | REF:other |
| LIM backward goto hidden in macros | REF:other | REF:other | REF:other | REF:other | REF:other |
| LIM magic definition assigns the sample | REF:other | REF:other | REF:other | REF:other | REF:other |
| LIM forged system-header linemarker before a nested capture | REF:other | REF:other | REF:other | REF:other | REF:other |
