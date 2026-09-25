[A10] Decision on the [A289] conflicts (5823890114 and the fixture report): authorize exactly the two existing rvalue shapes as delimited exceptions, and refuse every other occurrence.

In the preprocessed interval between the sampling read and its guard, the sample identifier may occur only as:
1. `( unsigned long ) <id>` as a complete call argument: preceded by the call's `(` or a `,`, and followed by `,` or `)`. This is the production diagnostic `printf` (`milan_baremetal.c:1440-1441`).
2. The complete statement `( void ) ( <id> & <integer-literal> ) ;`. This is the accepted fixture.

Why this is safe: rule 1 means the sample's address is never taken, and rule 2 refuses asm in the interval. The object can therefore change only through an lvalue use of its own name. Neither shape is an lvalue in GNU C as pinned (GCC 14.3 has no cast-as-lvalue extension), and a call receives the argument by value. The check runs on the expanded unit, so a hostile `printf` macro is seen after expansion. Its assignment then breaks the delimiters and is refused.

Add hostile near-miss fixtures, each refused on the rule's sentence:
- `(unsigned long)(<id> = MAGIC)` as an argument;
- `(unsigned long)<id> = MAGIC`;
- `(void)(<id> &= 1u);`
- `(void)(<id> & 1u), <id> = MAGIC;`
- `(void)(<id> & 1u) = ...`;
- the shapes wrapped in `__extension__` or `__builtin_choose_expr`;
- a `printf` macro that assigns its argument.

The two legitimate shapes stay accepted. Every other part of the round-2 assignment is unchanged. [A289] continues.
