| id | case | base-sdk | head-sdk | head-sdk-disabled | base-absent | head-absent | head-absent-disabled |
|---|---|---|---|---|---|---|---|
| C01 | published R272 macro x = MILAN_ID_MAGIC before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C02 | published R273 macro ((x) = MILAN_ID_MAGIC) before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C03 | header token paste __CONCAT(i, d) = MILAN_ID_MAGIC before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C04 | local ## paste macro MILAN_CAT(i, d) = MILAN_ID_MAGIC | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t | REFUSED other: a `##` paste reaches the boot entry point through #define MILAN_CAT: t |
| C05 | local macro builds the sample through header __CONCAT(a, d) | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C06 | macro takes the address and writes: *&(x) = MAGIC | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C07 | macro sets a pointer alias, then a write through the alias | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C08 | macro takes the address behind __extension__ and writes | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C09 | no macro: *(__extension__ &(id)) = MAGIC | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C10 | macro writes the sample through an asm output operand | ACCEPTED | REFUSED absence rule (asm) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C11 | no macro: asm output operand writes the sample | ACCEPTED | REFUSED absence rule (asm) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C12 | published R273 macro inside a nested block | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C13 | object-like alias of the forging function-like macro | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C14 | published R273 macro invoked AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C15 | plain write id = 0u AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C16 | no macro: (id) = MAGIC before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C17 | no macro: *&(id) = MAGIC before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C18 | alias taken in the mismatch block, goto back before the sample | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ | REFUSED other: milan_init() must not contain 'goto': control that enters the AEM-succ |
| C19 | R273-S3: verifier group's #else deleted | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C20 | read-only macro use (void)(x) of the sample before guard | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C21 | variadic forwarding macro to the forging macro | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C22 | sample passed doubly parenthesized MILAN_FORGE((id)) | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C23 | object-like macro naming the sample used as an lvalue | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C24 | __builtin_memcpy into &id via macro | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
| C25 | compound assignment through a macro, no parentheses: x \|= 0x4d494c4eu | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | REFUSED macro replacement rule | ACCEPTED |
