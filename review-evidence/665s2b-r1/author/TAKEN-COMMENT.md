[A683l] TAKEN

Branch: `665-s2b-cycles` (local, not pushed), at round 9's head `bf1773c0eabf0ba7fa1b1268c2a714e6b636e6eb`, whose commits stay. The lane base is `origin/dev-soft-core` `e76a755a`, checked as an ancestor (not dev). The PR targets `dev-soft-core`, now `f4c9ad4f06f185378fd2646298aab51dd108e86f`.

Authoritative references:
- the round-10 assignment, issuecomment-6502579312;
- S1's PR #795 as merged into `dev-soft-core` (the face census, mailbox contract 2.3, the AECP owner's face writer);
- FR_NFR 3.4.1 and NFR-SCOUT-03 (`docs/reference/FR_NFR.md`): approved `T_svc = 20 ms`, each family graded against `min(T_svc, its ceiling)`;
- the mailbox contract through `sw/mailbox/gen_mailbox.py`; S2's harness (`tb/verilator/ctrl_service_budget/`); `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

Interpreted scope:
1. **One merge commit** of `origin/dev-soft-core` into `665-s2b-cycles`: no rebase, no force. In each of the eleven conflicting files both sides' behaviour is kept:
   - S1's contract 2.3, its face census and the AECP owner's face writer;
   - this lane's record mover in front of `KL_mbx`, the fetch L1, the word-wise primitives and the `min(T_svc, ceiling)` grading.

   Generated mailbox files come only from `gen_mailbox.py`. S1's AECP IN_PROGRESS row is stated under the approved rule: a 12 ms cadence ceiling gives that path a 12 ms bound, `min(20, 12)`.
2. **At the merged head:**
   - round 9's full gate set, all rc 0;
   - the full sweep as four shard units, because the merge touches RTL wiring;
   - every composed row at 1x1/1if and 8x8/2if, arms A and B, with and without both drafts (lwSRP's receive path, the TSN stack's wire halves).

   The split CPU is re-routed out of context only if the merge changes its netlist.

Validation plan, at the merged head:
- the firmware self-test (`--require-rv32 --self-test`, four shards) with every firmware mutant driver;
- `fw_coverage.py --check` and `fw_rv32_selftest.py --require-rv32`;
- `gen_mailbox.py --check --crosscheck --selftest` and the publication census;
- S2's harness: its self-test, the eight legs and the controls;
- `test_builder.py --require-rv32` and `test_soc_options.py`;
- the mailbox suite, `lint_rtl.py --check`, `xvlog_gate.py --check`, and Yosys on the mover's rows;
- rtl-fast's `firmware-boundary` and `firmware-verilator`;
- the linked images; the docs, idiom and bare-metal gates; `cd tests && behave`;
- the full Verilator sweep as four shards.

Blockers: none. STOP if a row misses its bound, or if S1's contract and the mover cannot both hold.
