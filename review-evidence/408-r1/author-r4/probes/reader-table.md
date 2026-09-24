# Reader-level reviewer probes, rounds one to four, at the round-four head

S = what S does at this head; readers/GCC = the int names each keeps; allowlist off = the same spelling with the allowlist disconnected.

| review | spelling | S at head | outcome | with the allowlist off |
|---|---|---|---|---|
| R272-1 | cpp/elifdef.c | admitted | AGREE | AGREE |
| R272-1 | cpp/ff-after-hash.c | admitted | AGREE | AGREE |
| R272-1 | cpp/ff-undef.c | admitted | AGREE | AGREE |
| R272-1 | cpp/ff-vt.c | admitted | AGREE | AGREE |
| R272-1 | cpp/lone-cr.c | admitted | AGREE | AGREE |
| R272-1 | cpp/nul.c | admitted | AGREE | AGREE |
| R272-1 | cpp/pragma-pop.c | SUBSET_PRAGMA_PIN | REFUSED | REFUSED |
| R272-2 | control: plain #ifdef | admitted | AGREE | AGREE |
| R272-2 | control: the %: digraph | DIGRAPH_PIN | REFUSED | REFUSED |
| R272-2 | a splice inside the %: digraph | DIGRAPH_PIN | REFUSED | REFUSED |
| R272-2 | a splice with a space inside the %: digraph | DIGRAPH_PIN | REFUSED | REFUSED |
| R272-2 | a form feed before the %: digraph | DIGRAPH_PIN | REFUSED | REFUSED |
| R272-2 | a UTF-8 BOM before # at file start | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R272-3 | dollar_skipped.c | SUBSET_DOLLAR_PIN | REFUSED | REFUSED |
| R272-4 | mid.c | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R272-4 | comb.c | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R272-4 | sup2.c | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R272-4 | eacute.c | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-2 | S1.c | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S2.c | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S3.c | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S4.c | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-2 | S5.c | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S6.c | admitted | AGREE | AGREE |
| R273-2 | S1 `%:` split by a splice (ifdef FOO) | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S2 `%:` split by a splice (ifndef FOO) | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S3 `%:` split by a splice with a blank | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S4 byte order mark then #ifdef FOO on line 1 | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-2 | S5 `%:` split by a splice, #define FOO | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-2 | S6 corpus control: a form feed before # | admitted | AGREE | AGREE |
| R273-3 | BOM then #ifdef at file start | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-3 | BOM then #define at file start | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-3 | a multi-line comment between # and the name | admitted | AGREE | AGREE |
| R273-3 | a lone CR inside a block comment before # | admitted | AGREE | AGREE |
| R273-3 | CRLF splice inside #else | admitted | AGREE | AGREE |
| R273-3 | a splice with trailing blanks and CRLF inside #endif | admitted | AGREE | AGREE |
| R273-3 | a NUL between / and * | admitted | AGREE | AGREE |
| R273-3 | a string whose escaped backslash is a splice | admitted | AGREE | AGREE |
| R273-3 | a form feed and a comment after # | admitted | AGREE | AGREE |
| R273-3 | a directive after a line of only form feeds | admitted | AGREE | AGREE |
| R273-3 | a comment then a NUL then # | admitted | AGREE | AGREE |
| R273-3 | a splice then a form feed before # | admitted | AGREE | AGREE |
| R273-3 | a NEL (U+0085) before # | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-3 | a ZWNBSP (U+FEFF) mid-file before # | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-3 | a Ctrl-Z before # | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-3 | #elifdef behind a vertical tab | admitted | AGREE | AGREE |
| R273-3 | #ifndef behind a CRLF and a form feed | admitted | AGREE | AGREE |
| R273-3 | an apostrophe in a #define then a directive | admitted | AGREE | AGREE |
| R273-3 | a // comment continued by a splice after CRLF | admitted | AGREE | AGREE |
| R273-3 | a splice inside the #define name with CR | admitted | AGREE | AGREE |
| R273-4 | __has_include with an angled header name holding /* (if !) | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | __has_include with an angled header name holding /* (else) | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | __has_include with a quoted header name holding /* (control) | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | __has_include with an angled header name holding // (control) | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | hi-spellings/t1.c | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | hi-spellings/t2.c | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-4 | hi-spellings/t3.c | SUBSET_HAS_INCLUDE_PIN | REFUSED | REFUSED |
| R273-5 | misnest U+0024 dollar (control, refused by S) | SUBSET_DOLLAR_PIN | REFUSED | REFUSED |
| R273-5 | nest U+0024 dollar (control, refused by S) | SUBSET_DOLLAR_PIN | REFUSED | REFUSED |
| R273-5 | misnest U+00B7 middle dot | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+00B7 middle dot | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+0387 greek ano teleia | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+0387 greek ano teleia | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+203F undertie | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+203F undertie | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+00B5 micro sign | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+00B5 micro sign | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+00E9 e acute | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+00E9 e acute | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+00B2 superscript two | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+00B2 superscript two | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+2460 circled one | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+2460 circled one | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+00A0 no-break space | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-5 | nest U+00A0 no-break space | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-5 | misnest U+0661 arabic-indic one | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+0661 arabic-indic one | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | misnest U+FF21 fullwidth A | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | nest U+FF21 fullwidth A | SUBSET_CHARACTER_PIN | REFUSED | DISAGREE |
| R273-5 | control: plain misnest with nothing extra | admitted | AGREE | AGREE |
| R273-5 | control: the S corpus's own within-S firmware | admitted | AGREE | AGREE |
| R273-5 | r2 S1 `%:` split by a splice (ifdef FOO) | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-5 | r2 S2 `%:` split by a splice (ifndef FOO) | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-5 | r2 S3 `%:` split by a splice with a blank | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-5 | r2 S4 byte order mark then #ifdef FOO on line 1 | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-5 | r2 S5 `%:` split by a splice, #define FOO | DIGRAPH_PIN | REFUSED | REFUSED |
| R273-5 | r2 S6 corpus control: a form feed before # | admitted | AGREE | AGREE |
| R273-5 | ident.c | SUBSET_CHARACTER_PIN | REFUSED | AGREE |
| R273-5 | nest.c | SUBSET_CHARACTER_PIN | REFUSED | AGREE |

| review | spellings | refused by S | read as GCC reads them | disagree |
|---|---|---|---|---|
| R272-1 | 7 | 1 | 6 | 0 |
| R272-2 | 6 | 5 | 1 | 0 |
| R272-3 | 1 | 1 | 0 | 0 |
| R272-4 | 4 | 4 | 0 | 0 |
| R273-2 | 12 | 10 | 2 | 0 |
| R273-3 | 20 | 5 | 15 | 0 |
| R273-4 | 7 | 7 | 0 | 0 |
| R273-5 | 32 | 29 | 3 | 0 |
