[A767] REVIEW READY

Commit: `bfe7a9d676e53ff9b3c45c068b9c31da7893dbfb` on `tsn-c-stack-pin-715589c`. It is six commits on round 1's `50e2a722` (fourteen on `dev-soft-core` `1d6bf555`); no merge, rebase, force or amend, and nothing is pushed. Round 2 answers the [A10] ruling on R829-1 and R830-1 (issuecomment-6806698193) and the two STOP rulings (issuecomment-6807277620, issuecomment-6811790762).

Changed:
- **R829-1 F1.** Test E3 pins the ACMP poll's "still owes" return at exactly one owed frame behind a held egress. Each module's poll is called directly: ACMP's returns true, the others false, and the loop does not sleep. Plant `acmp-poll-owes-nothing-at-one` (R829's P6, `owed_count > 1u`) fails "E3 the ACMP poll says it still owes its one frame behind the held egress". The control campaign rises from 579 to 585: this plant and five redelivery plants.
- **R829-1 F2.** Every RV32 figure and gate this round was built with the pinned SDK (`scripts/ci_rv32_sdk.py --verify-only` rc 0).
  - The gates' eleven "Install and verify the pinned RV32 SDK" steps now run and verify it. Round 1 excused them, naming another build of GCC 14.3.0 as the pinned SDK.
  - Rebuilt on the pinned SDK, round 1's ledger tables come out byte-identical at both pins. The PR description states this.
- **R830-1 F1.** The port contract's redelivery rule is met (`acmp_mbx.c`, `redeliver()`). After a poll that sends an owed frame, the adapter offers the kept record, then up to a full ring (19) of waiting acmp records in arrival order, until one is declined or none is left.
  - Records are taken in the loop's buffer and counted as the loop counts its own.
  - THE KEPT COMMAND restates the later-command bound (n + 1 + f + r) and qualifies the A1 take bound while a command is kept.
  - `ACMP_MBX_PASS_MAX` grows from 1,030 to 2,754 accesses (the redelivery's 1,724). Every figure derived from it is restated in `MAILBOX_SPLIT.md` and the firmware READMEs; `ctrl_service_bounds` reports 47 checks, 0 failures.
  - K4 is R830's P1: the second command leaves in pass 10, not 11. K5 to K7 cover the rest, and each plant fails its test by name.
- **R830-1 F2.** S2's README (:553-557, :576) and `scenario.py:827-828` are labelled as measured at `70936b77`. R830's grep now hits only the labelled line.
- **R830-1 F3.** The docstring is as given.
- **First STOP's ruling.** The size fixture's 1x1/2if plans 41.0 RAMB36, accepted. The 8x8/2if override is re-keyed at `ctrl_plat` 21,392 B (+8 B, the loop pointer), and `SPLIT_CONTROL_MEMORY.md` section 5 is restated at both pins. Every other plan of both images is unchanged.
- **`bfe7a9d6`.** `scenario.py` is back at 1,000 lines. At `8ffcf2fc` the Python idiom gate refused it at 1,003 as a new long module.

Validation (clean clones of `bfe7a9d6`, pinned RV32 SDK):
- Every `run:` step of `docs.yml`, `rtl-fast.yml`, `elaborate.yml` and `rtl.yml`: 150 rc 0, 215 not run with a stated reason, 0 bad.
- The control campaign caught 585 of 585.
- `fw_coverage.py --check`: PASS; the adapter is at 106/106 lines and 42/42 branches.
- `firmware-boundary` and `firmware-verilator`: PASS (3258 and 1019 compiled sources). SRP campaign: 280 `[ok]` lines.
- The sweep's `mbx` suite, the one suite that builds this delta: 2,726 checks, 0 failures; mutants 7 of 7.
- `test_builder.py --require-rv32`: leg 0 passes every arm; leg 1 passes all but the arm that needs a placed hardware build's report.
- `behave`: 508 scenarios passed. `git diff --check` against the merge base: rc 0.
- S2's harness at 1x1/1if and 8x8/2if, both pins, recorded and not graded: T_svc misses 34 -> 34 of 141 and 63 -> 59 of 182. "An ACMP command behind the owed input" goes from never answered to all four answered, the worst after 104.568 ms and 138.526 ms. `run.py --self-test`: 0 failures.

Recorded, not graded (issuecomment-6811790762, item 2). Measured on S2b's head with this PR's firmware delta and the pin at `715589c`:
- 8x8/2if reads 0.767 as the committed rule grades it, and 0.730 with the nested `acmp_rx` attributed to its record.
- 1x1/1if reads 0.483.

#890 carries the rule and the 0.75 ceiling.

Acceptance criteria: each ruling item is met as stated above, and each new check fails on its planted defect (HANDOFF.md, receipts).

Open risks/questions:
- S2b's sync onto this pin owes three updates (item 4): its 8x8/2if size fixture's ledger (58.0 RAMB36), its hot list's `__lshrdi3` entry, and `poll_grade.py`'s 1x1 ACMP item, restated as measured (stated 6,500 cycles, measured 10,974).
- 32x32 is S15's.
