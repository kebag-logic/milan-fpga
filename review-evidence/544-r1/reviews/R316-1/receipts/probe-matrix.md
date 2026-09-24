| id | variant | base-sdk | head-sdk | head-sdk-disabled | base-absent | head-absent | head-absent-disabled |
|---|---|---|---|---|---|---|---|
| C01 | published R272 macro x = MILAN_ID_MAGIC before guard | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C02 | published R273 macro ((x) = MILAN_ID_MAGIC) before guard | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C03 | header token paste __CONCAT(i, d) = MILAN_ID_MAGIC before guard | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C04 | local ## paste macro MILAN_CAT(i, d) = MILAN_ID_MAGIC | REFUSED other: a `##` paste reaches the boot entry point through #define MI | REFUSED other: a `##` paste reaches the boot entry point through #define MI | REFUSED other: a `##` paste reaches the boot entry point through #define MI | REFUSED other: a `##` paste reaches the boot entry point through #define MI | REFUSED other: a `##` paste reaches the boot entry point through #define MI | REFUSED other: a `##` paste reaches the boot entry point through #define MI |
| C05 | local macro builds the sample through header __CONCAT(a, d) | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C06 | macro takes the address and writes: *&(x) = MAGIC | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C07 | macro sets a pointer alias, then a write through the alias | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C08 | macro takes the address behind __extension__ and writes | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C09 | no macro: *(__extension__ &(id)) = MAGIC | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C10 | macro writes the sample through an asm output operand | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C11 | no macro: asm output operand writes the sample | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C12 | published R273 macro inside a nested block | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C13 | object-like alias of the forging function-like macro | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C14 | published R273 macro invoked AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C15 | plain write id = 0u AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C16 | no macro: (id) = MAGIC before guard | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C17 | no macro: *&(id) = MAGIC before guard | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C18 | alias taken in the mismatch block, goto back before the sample | REFUSED other: milan_init() must not contain 'goto': control that enters th | REFUSED other: milan_init() must not contain 'goto': control that enters th | REFUSED other: milan_init() must not contain 'goto': control that enters th | REFUSED other: milan_init() must not contain 'goto': control that enters th | REFUSED other: milan_init() must not contain 'goto': control that enters th | REFUSED other: milan_init() must not contain 'goto': control that enters th |
| C19 | R273-S3: verifier group's #else deleted | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C20 | read-only macro use (void)(x) of the sample before guard | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C21 | variadic forwarding macro to the forging macro | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C22 | sample passed doubly parenthesized MILAN_FORGE((id)) | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C23 | object-like macro naming the sample used as an lvalue | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C24 | __builtin_memcpy into &id via macro | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
| C25 | compound assignment through a macro, no parentheses: x \|= 0x4d494c4eu | ACCEPTED | REFUSED single-store | ACCEPTED | ACCEPTED | REFUSED macro-replacement | ACCEPTED |
