# R316-ROUND3-MATRIX

Head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.

ASM: unit allowlist; SAMPLE: prior absence rule; MACRO: replacement rule.
OTHER: full refusal retained in the corresponding JSON receipt.

| Case | r316-sdk | r316-sdk-assert_preprocessed_identity_sample | r316-sdk-assert_preprocessed_asm_allowlist | r316-absent | r316-absent-assert_identity_macro_free |
|---|---|---|---|---|---|
| N01 extra diagnostic printf with a complete (unsigned long)id argument | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N02 discarded mask with an ull-suffixed hex literal | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N03 discarded mask split across lines | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N04 cast argument of __alignof (not a call) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N05 cast argument of __builtin_constant_p | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N06 cast argument of __typeof in a block-scope declaration | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| N07 authorized argument followed by an assigning argument | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| N08 discarded mask after a label | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| N09 discarded mask with a character literal | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| N10 cast argument through a parenthesized callee | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| N11 cast argument after a comma operator in a nested paren | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| N12 cast argument of __builtin_choose_expr hidden behind a call | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| N13 compound assignment to a cast argument | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| N14 discarded mask whose statement is the body of an if | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| N15 discarded mask whose statement follows a closing initializer brace | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| E01 address in sizeof after the guard | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| E02 address in the unselected arm of __builtin_choose_expr after the guard | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| E03 address in an unselected _Generic association after the guard | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| E04 address in __typeof__ after the guard | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| E05 address via __builtin_memcpy source after the guard | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| W01 call to a helper whose asm overwrites every callee-saved register | REFUSED:ASM | REFUSED:ASM | ACCEPTED | ACCEPTED | ACCEPTED |
| W02 function-like macro invoked with the sample expands to the clobbering helper | REFUSED:ASM | REFUSED:ASM | ACCEPTED | ACCEPTED | ACCEPTED |
| W03 printf redefined to a clobbering helper; production diagnostic unchanged | REFUSED:ASM | REFUSED:ASM | ACCEPTED | ACCEPTED | ACCEPTED |
| W04 helper call alone, no asm (control for W01) | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED | ACCEPTED |
| W05 store through the frame address in the interval | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER | REFUSED:OTHER |
| A01 plain *(__extension__ &(id)) = MAGIC (R316-1 C09) | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A02 plain asm output operand (R316-1 C11) | REFUSED:SAMPLE | REFUSED:ASM | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A03 plain __builtin_choose_expr lvalue | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A04 plain _Generic lvalue | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A05 plain __real__ lvalue | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A06 plain __extension__ lvalue | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A07 plain asm tied output | REFUSED:SAMPLE | REFUSED:ASM | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A08 plain __builtin_memcpy into &(id) | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A09 plain (id)++ repeated to the magic is not needed: (id) \|= MAGIC | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
| A10 plain comma-expression lvalue: (0, id) is not an lvalue; use *(&(id)+0) | REFUSED:SAMPLE | ACCEPTED | REFUSED:SAMPLE | ACCEPTED | ACCEPTED |
