[A683m] TAKEN

Branch: `665-s2b-cycles` (local, not pushed), at `f884c7e9fb71cdb94c12e3228b1412801c34e1f4`, the head of PR #810. New commits go on top: no rebase, no force. The lane base `origin/dev-soft-core` `e76a755a` is checked as an ancestor (not dev). The PR targets `dev-soft-core`.

Authoritative references:
- the round-11 assignment, issuecomment-6508235352;
- R711-1 (PR #810 issuecomment-6508189374) and R712-1 (issuecomment-6508223902), with their probes;
- the clock correction, issuecomment-6508196970; the frozen S2b items 3 and 6, issuecomment-6414297191;
- FR_NFR 3.4.1 and NFR-SCOUT-03 (`docs/reference/FR_NFR.md`): each family against min(T_svc = 20 ms, its ceiling);
- the share derivation in `sw/firmware/ctrl/loop/ctrl_loop.h`; the mover's contract in `hdl/milan/mailbox/KL_mbx_dma.sv` and `sw/firmware/ctrl/plat/mbx_dma.h`.

Interpreted scope:
1. **The clock (R711-F1).** By default the harness measures the product's split CPU clock: the Milan clock, 50 MHz, with the bus at 100 MHz. `build.json` records that the CPU clock is the product's. Any other CPU clock is an explicit, labelled option, recorded in `build.json` and named on every table and run line. Every composed row is measured at 1x1/1if and 8x8/2if, on arms A and B, with and without the two drafts, at 50 MHz (product) and at 100 MHz (the labelled option). `SPLIT_CONTROL_MEMORY.md` section 13, the harness README and the PR body give the clock of every figure. The SoC's clock is not changed.
2. **The mover's length (R711-F2 = R712-F1).** The word count is formed without the 12-bit wrap, so every length the field accepts, 4093 to 4095 included, obeys the burst and byte contract. The bench checks 4092 to 4095 in both directions, then a CPU access and a recovery transfer. The 17 plants are kept, and a plant of the wrap is added.
3. **R711-F3:** bench checks that fail for each of the three escaping plants, which are added to the mover's plants. **R711-F4:** a host test that builds `mbx.c` with `CTRL_MBX_DMA_BASE` over a register model of the mover. It covers success, ERR in each direction and the unaligned fallback, is in the coverage ratchet, and carries plants.
4. **The per-pass share (R712-F2):** 18 / 9 = 2.0 ms, in CPU-clock time. The harness reports it and asserts it for every work pass, separately from the row verdicts. A planted pass over the share fails even when every row fits. Passes over the share are reported at both clocks, with their composition, and split or bounded where a named constant can do it.
5. **R711 residue R1 and R2:** wording, folded in.

Validation plan, at the final head:
- the firmware self-test (`--require-rv32 --self-test`, four shards), every firmware mutant driver, `fw_coverage.py --check`, `fw_rv32_selftest.py --require-rv32`;
- the mover bench and its plants (`make run-dma`, `dma_mutants.py`) and the mailbox suite;
- `lint_rtl.py --check`, Yosys on the mover, and `xvlog_gate.py --check` under the lock after the sweep;
- `gen_mailbox.py --check --crosscheck --selftest`;
- the harness's self-test and the 16 legs (two points, two arms, with and without the drafts, at two clocks);
- `test_builder.py --require-rv32` and `test_soc_options.py`;
- rtl-fast's `firmware-boundary`, `firmware-verilator` and `bdd-conformance` (`cd tests && behave`), and the docs gates;
- the full Verilator sweep as four shard units, because the mover's RTL changes.

Blockers: none. The exit is REVIEW READY only if every CPU-decided row and every pass fits at 50 MHz. Otherwise it is STOP with the figures at both clocks and the residual of each row and pass, which is the expected outcome while the clock question is open.
