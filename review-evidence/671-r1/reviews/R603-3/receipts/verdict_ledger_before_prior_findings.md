[R603] NEGATIVE - exact head fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08
Written 2026-10-11T02:49:36Z, after the independent pass and before any prior review report on PR #715 was read.

Independent finding: R603-3-F1 MINOR (Tests, Robustness, Docs): no check pins the re-stage retry bound.
nvm_restage() at sw/firmware/milan_baremetal/milan_baremetal.c:813-825 retries NVM_READ_TRIES times. Plants that set
that bound to 2 or 4 tries, or remove it, all pass checks 13 and 14 on endstation_arty_4x4 (and checks 1 to 14 with the
bound removed). The bound removed also passes checks 13 and 14 on endstation_ax7101_1x1_tdm8 and endstation_ax7101_8x8.
With the bound removed, a judgement read of a blank slot A answered with slot B's container makes the boot never complete.
It prints no boot line and runs no restore walk, and the host stops it at 1,000,001 reads. The head holds after 7 reads.

| lens | state | covering round | head |
|---|---|---|---|
| Conformance | CLEAN | R603-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| RTL | CLEAN | R603-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Robustness | UNCLEAN (F1) | R603-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Tests | UNCLEAN (F1) | R603-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Docs | UNCLEAN (F1) | R603-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
