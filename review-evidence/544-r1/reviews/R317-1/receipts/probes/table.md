| case | head-sdk | base-sdk | head-sdk-disconnect | head-absent | base-absent | head-absent-disconnect |
|---|---|---|---|---|---|---|
| CTRL unchanged firmware | ACC | ACC | ACC | ACC | ACC | ACC |
| CTRL published R272 macro x = MILAN_ID_MAGIC | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| CTRL published R273 macro ((x) = MILAN_ID_MAGIC) | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| CTRL plain source assignment | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID |
| HOST paste local macro MILAN_CAT(i, d) = MAGIC | REF:other | REF:other | REF:other | REF:other | REF:other | REF:other |
| HOST paste header macro __CONCAT(i, d) = MAGIC | REF:SAMPLE | ACC | ACC | ACC | ACC | ACC |
| HOST paste builds writer name MILAN_CAT(MILAN_, W)(id) | REF:other | REF:other | REF:other | REF:other | REF:other | REF:other |
| HOST macro takes address and stores | REF:other | REF:other | REF:other | REF:other | REF:other | REF:other |
| HOST macro sets local pointer alias then stores | REF:other | REF:other | REF:other | REF:MACRO | ACC | ACC |
| HOST pointer alias declared before the sample, set by macro | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST file-scope pointer alias set by macro | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro write in nested block | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro write in if-block | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST plain write in nested block | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID |
| HOST macro __builtin_choose_expr lvalue store | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro _Generic lvalue store | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro (__real__ x) store | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro (__extension__ x) store | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST macro inline asm output operand | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| HOST plain __builtin_choose_expr lvalue store | ACC | ACC | ACC | ACC | ACC | ACC |
| HOST plain inline asm output operand | ACC | ACC | ACC | ACC | ACC | ACC |
| HOST object-like alias of a function-like writer | REF:SAMPLE | ACC | ACC | ACC | ACC | ACC |
| HOST writer name passed through a macro argument | REF:SAMPLE | ACC | ACC | ACC | ACC | ACC |
| HOST #define of the sample name between read and guard | REF:other | REF:other | REF:other | REF:other | REF:other | REF:other |
| HOST string argument with ) before the sample | REF:SAMPLE | ACC | ACC | REF:MACRO | ACC | ACC |
| LEGIT plain write after the guard | ACC | ACC | ACC | ACC | ACC | ACC |
| LEGIT macro write after the guard | ACC | ACC | ACC | ACC | ACC | ACC |
| LEGIT binary and with a constant on the left | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID | REF:TEXT-ID |
| LEGIT read through a function-like macro | ACC | ACC | ACC | REF:MACRO | ACC | ACC |
| S3 verifier #else deleted | ACC | ACC | ACC | ACC | ACC | ACC |
