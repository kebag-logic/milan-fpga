
### hostile

| Case | base sdk | base absent | a13b sdk | a13b absent | head sdk | head absent |
|---|---|---|---|---|---|---|
| R272 r1 plain #: product-only `0 &&` in the choke point verdict test | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: resolver verdict test) | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R272 r1 form feed: product-only `0 &&` in the choke point verdict test | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R272 r1 vertical tab: product-only `0 &&` in the choke point verdict test | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R272 r1 plain #: product-only paged-base cast store to ADP_CTRL in a UART handler | REFUSED (cast set) | REFUSED (cast set) | REFUSED (selection: resolver store) | ACCEPTED | REFUSED (selection: resolver store) | ACCEPTED |
| R272 r1 plain #: product-only literal-address cast store to ADP_CTRL in a UART handler | REFUSED (cast set) | REFUSED (cast set) | REFUSED (selection: census) | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R272 r1 plain #: product-only lui asm store to ADP_CTRL in a UART handler | REFUSED (asm set) | REFUSED (asm set) | REFUSED (selection: resolver store) | ACCEPTED | REFUSED (selection: resolver store) | ACCEPTED |
| R272 r1 plain #: product-only arm moving ADP_EID_LO onto ADP_CTRL (product arm first) | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R272 r1 plain #: product-only arm moving ADP_EID_LO onto ADP_CTRL (product arm last) | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R272 r1 form feed: product-only paged-base cast store to ADP_CTRL in a UART handler | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: resolver store) | ACCEPTED |
| R272 r1 form feed: product-only literal-address cast store to ADP_CTRL in a UART handler | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R272 r1 form feed: product-only lui asm store to ADP_CTRL in a UART handler | REFUSED (asm set) | REFUSED (asm set) | ACCEPTED | ACCEPTED | REFUSED (selection: resolver store) | ACCEPTED |
| R272 r1 form feed: product-only arm moving ADP_EID_LO onto ADP_CTRL (product arm first) | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R272 r1 form feed: product-only arm moving ADP_EID_LO onto ADP_CTRL (product arm last) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R272 r2 control: form feed arm around a SPELLED milan_write enable in a UART handler | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R272 r2 NUL byte before #: product-only literal-address cast store in a UART handler | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R272 r2 unterminated-quote defines around a product-only literal-address cast store in a UART handler | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (open literal) | REFUSED (open literal) |
| R272 r2 unterminated-quote defines around a product-only `0 &&` in the choke point verdict test | REFUSED (verdict-test rule) | REFUSED (verdict-test rule) | REFUSED (verdict-test rule) | REFUSED (verdict-test rule) | REFUSED (open literal) | REFUSED (open literal) |
| R272 r2 form feed: product-only literal-address cast store inside configure_fabric() (a boot-path body) | REFUSED (cast set) | REFUSED (cast set) | REFUSED (-E comparison) | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R272 r3 identity forged through a plain function-like macro | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R272 r3 identity forged through a token-joining splice of the local's name | REFUSED (splice ban) | REFUSED (splice ban) | ACCEPTED | ACCEPTED | REFUSED (six-body splice ban) | REFUSED (six-body splice ban) |
| R272 r3 identity forged through a ## paste of the local's name | REFUSED (## ban) | REFUSED (## ban) | ACCEPTED | ACCEPTED | REFUSED (six-body ## ban) | REFUSED (six-body ## ban) |
| R272 r3 plain #: product-only struct-overlay store to ADP_CTRL in a UART handler | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R272 r3 form feed: product-only struct-overlay store to ADP_CTRL in a UART handler | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 H1 function pointer to milan_write built by a SPLICE, called from a UART handler | REFUSED (splice ban) | REFUSED (splice ban) | REFUSED (resolver entrance) | ACCEPTED | REFUSED (resolver entrance) | ACCEPTED |
| R273 H2 function pointer to milan_write built by a PASTE, called from a UART handler | REFUSED (## ban) | REFUSED (## ban) | REFUSED (resolver entrance) | ACCEPTED | REFUSED (resolver entrance) | ACCEPTED |
| R273 H3 second choke-point call built by a SPLICE, in a UART handler | REFUSED (splice ban) | REFUSED (splice ban) | REFUSED (resolver entrance) | ACCEPTED | REFUSED (resolver entrance) | ACCEPTED |
| R273 H4 verdict overwritten by a PASTE between the verifier and the choke point | REFUSED (## ban) | REFUSED (## ban) | REFUSED (resolver entrance) | ACCEPTED | REFUSED (six-body ## ban) | REFUSED (six-body ## ban) |
| R273 H5 verdict overwritten by a SPLICE between the verifier and the choke point | REFUSED (splice ban) | REFUSED (splice ban) | REFUSED (resolver entrance) | ACCEPTED | REFUSED (six-body splice ban) | REFUSED (six-body splice ban) |
| R273 H11 store through milan_reg() built by a PASTE, in a UART handler | REFUSED (## ban) | REFUSED (## ban) | REFUSED (resolver helper) | ACCEPTED | REFUSED (resolver helper) | ACCEPTED |
| R273 H6 second #define of MILAN_ID_MAGIC as a fresh milan_read(MILAN_ID) | REFUSED (macro-body rule) | REFUSED (macro-body rule) | REFUSED (-E comparison) | ACCEPTED | REFUSED (one definition) | REFUSED (one definition) |
| R273 H7 second #define of MILAN_ID_MAGIC as the sample itself | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (one definition) | REFUSED (one definition) |
| R273 H8 verifier QSPI-slot group with its #else arm deleted | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 H9 verifier #else behind a lone CR, its hidden arm returning 1 | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (verifier return rule) | REFUSED (verifier return rule) |
| R273 H10 product-only 0 && in the choke point's verdict test | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: resolver verdict test) | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R273 H12 the same product-only 0 && with its directives behind lone CRs | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R273 H13 the same product-only 0 && with its directives behind form feeds | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: resolver verdict test) | ACCEPTED |
| R273 H14 pre-AEM ADP clear behind a lone-CR #ifndef (census keeps it, product drops it) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (selection: pre-AEM clear rule) | REFUSED (selection: pre-AEM clear rule) |
| R273 H15 a LINK named init.h beside the firmware to a file outside | REFUSED (directory pin) | REFUSED (directory pin) | REFUSED (-H resolution) | ACCEPTED | REFUSED (-H resolution) | ACCEPTED |
| R273 V1a form feed before #: product-only literal-address cast store in a UART handler | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 V1b vertical tab before #: the same store | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 V1c NUL before #: the same store | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 V1d lone CR before #: the same store | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 V1e form feed before #: product-only lui/sw asm store | REFUSED (asm set) | REFUSED (asm set) | ACCEPTED | ACCEPTED | REFUSED (selection: resolver store) | ACCEPTED |
| R273 V1f control: plain # product-only literal cast store | REFUSED (cast set) | REFUSED (cast set) | REFUSED (selection: census) | ACCEPTED | REFUSED (selection: census) | ACCEPTED |
| R273 V2a identity local forged by a SPLICE between the read and the guard | REFUSED (splice ban) | REFUSED (splice ban) | ACCEPTED | ACCEPTED | REFUSED (six-body splice ban) | REFUSED (six-body splice ban) |
| R273 V2b identity local forged by a PASTE between the read and the guard | REFUSED (## ban) | REFUSED (## ban) | ACCEPTED | ACCEPTED | REFUSED (six-body ## ban) | REFUSED (six-body ## ban) |
| R273 V2c identity local forged by a plain function-like macro | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 V4 unterminated character literals in two #defines bracketing a product-only literal-address store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED (open literal) | REFUSED (open literal) |
| R273 E2 an #elif arm only the product takes enabling ADP before AEM | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R273 E3 nested groups, the inner arm enabling ADP before AEM | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |
| R273 E5 #if 0 around an enable before AEM | REFUSED (reach ban) | REFUSED (reach ban) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) | REFUSED (selection: choke-point rule) |

### accepted

| Case | base sdk | base absent | a13b sdk | a13b absent | head sdk | head absent |
|---|---|---|---|---|---|---|
| R272 r4 a debug helper defined under #ifdef MILAN_DEBUG_TOD and called under a second #ifdef MILAN_DEBUG_TOD in a UART handler | ACCEPTED | ACCEPTED | REFUSED (selection: census compile) | ACCEPTED | ACCEPTED | ACCEPTED |
| R272 r4 control: the same debug printf in ONE #ifdef in a UART handler | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R272 r4 a debug-only static counter declared under #ifdef and incremented under a second #ifdef of the same macro | ACCEPTED | ACCEPTED | REFUSED (selection: census compile) | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 V3a correlated conditionals: debug helper defined and called under two #ifdef MILAN_DEBUG_TOD | ACCEPTED | ACCEPTED | REFUSED (selection: census compile) | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 V3b correlated conditionals: debug counter declared and incremented under two #ifdef MILAN_DEBUG_TOD | ACCEPTED | ACCEPTED | REFUSED (selection: census compile) | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC1 an #ifdef around a debug printf INSIDE milan_init() | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC2 a benign statement in an arm the census tree drops, inside configure_fabric() | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC3 an #ifdef/#else choosing a #define, read in a UART command handler | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC4 a ## token paste building a call outside the boot path | REFUSED (## ban) | REFUSED (## ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC5 a token-joining backslash-newline inside a macro body | REFUSED (splice ban) | REFUSED (splice ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC6 a read-only #define accessor over milan_read() | REFUSED (macro-body rule) | REFUSED (macro-body rule) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC7 a fifth cast to a pointer, resolving outside the window | REFUSED (cast set) | REFUSED (cast set) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC8 a fifth store through a pointer, resolving outside the window | REFUSED (store set) | REFUSED (store set) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC9 parse_u64() and seconds_to_ns() exchanged | REFUSED (store set) | REFUSED (store set) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC10 a fifth inline-asm statement, a fence in a UART handler | REFUSED (asm set) | REFUSED (asm set) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 ACC11 a README and a notes.txt beside the firmware | REFUSED (directory pin) | REFUSED (directory pin) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 E1 #if/#elif/#else debug printfs after the choke-point call | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 E4 #if 0 around a benign statement | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| R273 E6 four independent groups (16 selections, at the bound) | REFUSED (reach ban) | REFUSED (reach ban) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
