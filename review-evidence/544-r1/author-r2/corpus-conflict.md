[A289] Round 2 corpus conflict

The existing accepted fixture `identity sample read without modification` inserts `(void)(id & 1u);` between the sampling read and guard (`sw/builder/test_builder.py` at the assigned head). The assigned absence rule refuses that identifier occurrence, while the same assignment requires the legitimate corpus unchanged.

The narrowest proposed exception is that exact discarded bit-mask expression, with the actual sample identifier and whitespace accounted for. No arbitrary rvalue expression or wrapper would qualify. A decision has been requested before adding any exception. The independent address, asm, bypass-control and compiler-free disclosure work continues.
