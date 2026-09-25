| id | case | base-sdk | head-sdk | head-sdk-disabled | base-absent | head-absent | head-absent-disabled |
|---|---|---|---|---|---|---|---|
| N01 | extra diagnostic printf with a complete (unsigned long)id argument | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N02 | discarded mask with an ull-suffixed hex literal | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N03 | discarded mask split across lines | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N04 | cast argument of __alignof (not a call) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N05 | cast argument of __builtin_constant_p | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N06 | cast argument of __typeof in a block-scope declaration | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N07 | authorized argument followed by an assigning argument | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass |
| N08 | discarded mask after a label | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters | REFUSED other: milan_init() must not contain the label 'milan_l': control that enters |
| N09 | discarded mask with a character literal | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N10 | cast argument through a parenthesized callee | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N11 | cast argument after a comma operator in a nested paren | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N12 | cast argument of __builtin_choose_expr hidden behind a call | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N13 | compound assignment to a cast argument | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass | REFUSED other: CSR identity guard must consume the unmodified MILAN_ID sample: no ass |
| N14 | discarded mask whose statement is the body of an if | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N15 | discarded mask whose statement follows a closing initializer brace | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E01 | address in sizeof after the guard | ACCEPTED | REFUSED absence rule (escape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E02 | address in the unselected arm of __builtin_choose_expr after the guard | ACCEPTED | REFUSED absence rule (escape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E03 | address in an unselected _Generic association after the guard | ACCEPTED | REFUSED absence rule (escape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E04 | address in __typeof__ after the guard | ACCEPTED | REFUSED absence rule (escape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E05 | address via __builtin_memcpy source after the guard | ACCEPTED | REFUSED absence rule (escape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W01 | call to a helper whose asm overwrites every callee-saved register | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W02 | function-like macro invoked with the sample expands to the clobbering helper | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W03 | printf redefined to a clobbering helper; production diagnostic unchanged | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W04 | helper call alone, no asm (control for W01) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W05 | store through the frame address in the interval | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use | REFUSED other: only milan_reg() may form a CSR address, but a CSR pointer cast is use |
| A01 | plain *(__extension__ &(id)) = MAGIC (R316-1 C09) | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A02 | plain asm output operand (R316-1 C11) | ACCEPTED | REFUSED absence rule (asm) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A03 | plain __builtin_choose_expr lvalue | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A04 | plain _Generic lvalue | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A05 | plain __real__ lvalue | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A06 | plain __extension__ lvalue | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A07 | plain asm tied output | ACCEPTED | REFUSED absence rule (asm) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A08 | plain __builtin_memcpy into &(id) | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A09 | plain (id)++ repeated to the magic is not needed: (id) \|= MAGIC | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| A10 | plain comma-expression lvalue: (0, id) is not an lvalue; use *(&(id)+0) | ACCEPTED | REFUSED absence rule (shape) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
