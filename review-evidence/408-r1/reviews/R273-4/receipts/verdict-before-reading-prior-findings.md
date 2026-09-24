[R273] NEGATIVE - exact head 8e12d31fefa7df0abb4d9474d0412ce123ac9644
Snapshot written before reading any prior review's findings text.
F1 BLOCKER (Conformance, Robustness, Tests, Docs): _c_phases() has no
header-name state. `#if !__has_include(<r273/*none>)` makes the gate read a
comment to the next `*/` while GCC reads one header-name token, so a line
GCC compiles is blanked from every text the gate reads AND from every arm
selection it compiles. HI1-HI4 are refused at dev with the pinned SDK and
accepted at this head with it (HI1, HI4 also in both modes). Controls HI1q
(quoted), HI1p (#if 1) are refused; HI5 benign accepted.
Ledger: Conformance UNCLEAN, RTL CLEAN, Robustness UNCLEAN, Tests UNCLEAN,
Docs UNCLEAN, all at 8e12d31fefa7df0abb4d9474d0412ce123ac9644, round R273-4.
