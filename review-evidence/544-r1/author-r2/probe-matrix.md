[A289]

Exact head: `77e9ca5ea9e04a7618c577ab511baec63b39dc05`.

Both public probe sets ran unchanged. Each case has four recorded verdicts.
REFUSED (existing) means another contract rule answers before, or independently of, this rule.
The original JSON receipts retain every reported reason.

Internal reviewer cases

| Case | Compiled | Compiled, disconnected | No compiler | No compiler, disconnected |
|---|---|---|---|---|
| C01 published R272 macro x = MILAN_ID_MAGIC before guard | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C02 published R273 macro ((x) = MILAN_ID_MAGIC) before guard | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C03 header token paste __CONCAT(i, d) = MILAN_ID_MAGIC before guard | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C04 local ## paste macro MILAN_CAT(i, d) = MILAN_ID_MAGIC | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| C05 local macro builds the sample through header __CONCAT(a, d) | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C06 macro takes the address and writes: *&(x) = MAGIC | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C07 macro sets a pointer alias, then a write through the alias | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C08 macro takes the address behind __extension__ and writes | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C09 no macro: *(__extension__ &(id)) = MAGIC | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C10 macro writes the sample through an asm output operand | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C11 no macro: asm output operand writes the sample | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C12 published R273 macro inside a nested block | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C13 object-like alias of the forging function-like macro | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C14 published R273 macro invoked AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C15 plain write id = 0u AFTER the guard (must be accepted) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C16 no macro: (id) = MAGIC before guard | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C17 no macro: *&(id) = MAGIC before guard | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| C18 alias taken in the mismatch block, goto back before the sample | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| C19 R273-S3: verifier group's #else deleted | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| C20 read-only macro use (void)(x) of the sample before guard | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C21 variadic forwarding macro to the forging macro | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C22 sample passed doubly parenthesized MILAN_FORGE((id)) | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C23 object-like macro naming the sample used as an lvalue | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C24 __builtin_memcpy into &id via macro | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| C25 compound assignment through a macro, no parentheses: x \|= 0x4d494c4eu | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |

External reviewer cases

| Case | Compiled | Compiled, disconnected | No compiler | No compiler, disconnected |
|---|---|---|---|---|
| CTRL unchanged firmware | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| CTRL published R272 macro x = MILAN_ID_MAGIC | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| CTRL published R273 macro ((x) = MILAN_ID_MAGIC) | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| CTRL plain source assignment | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST paste local macro MILAN_CAT(i, d) = MAGIC | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST paste header macro __CONCAT(i, d) = MAGIC | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| HOST paste builds writer name MILAN_CAT(MILAN_, W)(id) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST macro takes address and stores | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST macro sets local pointer alias then stores | REFUSED (existing) | REFUSED (existing) | REFUSED (replacement) | ACCEPTED |
| HOST pointer alias declared before the sample, set by macro | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST file-scope pointer alias set by macro | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro write in nested block | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro write in if-block | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST plain write in nested block | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST macro __builtin_choose_expr lvalue store | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro _Generic lvalue store | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro (__real__ x) store | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro (__extension__ x) store | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST macro inline asm output operand | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| HOST plain __builtin_choose_expr lvalue store | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| HOST plain inline asm output operand | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| HOST object-like alias of a function-like writer | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| HOST writer name passed through a macro argument | REFUSED (absence) | ACCEPTED | ACCEPTED | ACCEPTED |
| HOST #define of the sample name between read and guard | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| HOST string argument with ) before the sample | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| LEGIT plain write after the guard | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| LEGIT macro write after the guard | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| LEGIT binary and with a constant on the left | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) | REFUSED (existing) |
| LEGIT read through a function-like macro | REFUSED (absence) | ACCEPTED | REFUSED (replacement) | ACCEPTED |
| S3 verifier #else deleted | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |

