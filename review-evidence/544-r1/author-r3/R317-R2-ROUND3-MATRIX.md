# R317-R2-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r317-cases_544_r2-sdk | r317-cases_544_r2-sdk-disconnected | r317-cases_544_r2-absent | r317-cases_544_r2-absent-disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK discarded mask hex literal (void)(id & 0xffu); | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK discarded mask no blanks (void)(id&1); | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK discarded mask ull suffix (void)(id & 0x1ull); | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK discarded mask macro literal (void)(id & MILAN_ID_MAGIC); | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK second diagnostic call argument | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| EXC-OK two sample arguments in one call | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| NEAR argument followed by + 1u | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument followed by conditional | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument extra parentheses (unsigned long)(x) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument then comma assignment in a second statement expr | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument postfix increment | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument cast unsigned long int | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument cast unsigned int | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument via parenthesized callee (printf)(...) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument in statement expression that assigns | REFUSED:OTHER | REFUSED:OTHER | REFUSED:MACRO | ACCEPTED |
| NEAR argument in sizeof | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument in array subscript | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR argument of __typeof__ declaration then assignment | REFUSED:OTHER | REFUSED:OTHER | REFUSED:MACRO | ACCEPTED |
| NEAR statement two masks (void)(x & 1u & 3u) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR statement negative literal (void)(x & -1) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR statement char literal (void)(x & '\1') | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR statement under if (1) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR statement followed by & 2u | REFUSED:SAMPLE | REFUSED:OTHER | REFUSED:MACRO | ACCEPTED |
| NEAR statement mask operand reversed (void)(1u & x) | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR statement mask then pre-increment in next statement | REFUSED:OTHER | REFUSED:OTHER | REFUSED:MACRO | ACCEPTED |
| NEAR statement mask in comma with assignment | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR printf macro routes the argument into a conditional | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| NEAR printf macro keeps a delimited argument and reuses it wrapped | REFUSED:SAMPLE | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| LIM printf macro forwards the argument to a benign identifier call | ACCEPTED | ACCEPTED | REFUSED:MACRO | ACCEPTED |
| ESC sizeof &id after guard | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC __typeof__(&id) after guard | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC asm m input after guard | REFUSED:SAMPLE | REFUSED:ASM | ACCEPTED | ACCEPTED |
| ESC asm +m output after guard | REFUSED:SAMPLE | REFUSED:ASM | ACCEPTED | ACCEPTED |
| ESC pointer initialised from &id after guard | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC &id + 0 after guard | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| ESC macro &(x) after guard | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| LIM asm +r output after guard (no address, after the interval) | REFUSED:ASM | REFUSED:ASM | ACCEPTED | ACCEPTED |
| BOUND C03 header paste | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND C05 macro using header paste | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND C13 object-like macro alias | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND writer alias | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND writer apply | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND C16 parenthesized assignment | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| BOUND C17 indirect assignment | REFUSED:SAMPLE | ACCEPTED | ACCEPTED | ACCEPTED |
| LIM callee asm clobbers a callee-saved register, called in interval | REFUSED:ASM | REFUSED:ASM | ACCEPTED | ACCEPTED |
| LIM frame-address store in interval | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| LIM backward goto writes after the guard | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| LIM backward goto hidden in macros | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| LIM magic definition assigns the sample | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| LIM forged system-header linemarker before a nested capture | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
