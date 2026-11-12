[A767] REVIEW READY

Commit: `32b43973069ee2742f86c4f92adb5eb9ca6bdfb3` on `tsn-c-stack-pin-715589c`, two commits on round 2's `bfe7a9d6` (16 on `dev-soft-core` `1d6bf555`). No merge, rebase, force or amend; nothing is pushed. This round answers the [A10] ruling on R829-2 and R830-2 (issuecomment-6814546620).

Changed:
- **Item 1 (R829-2 F1 = R830-2 N1).** New test K8, `K8ACommandTheRedeliveryDeclinesKeepsItsPlaceAheadOfTheNext` (`test_acmp_mbx.cpp:1427-1460`):
  - The owed set is full, then three GET_RX_STATEs arrive. The first is declined and kept; two wait behind it.
  - After the egress returns, the frames sent are the eight owed frames, then 0x7901, 0x7902, 0x7903, each once. Each command is declined once, and nothing is kept or owed after.
  - Plant `acmp-redelivery-past-a-decline` drops `&& m->kept.len == 0u` at `acmp_mbx.c:166`. It is the same edit as R829's `rv-continue-after-decline` and R830's `redelivery-past-a-decline.patch`.
  - With the plant, the third command's decline overwrites the second, which is never answered. K8 then fails by name: "K8 the owed frames, then each command answered once, in arrival order".
  - Control campaign: 585 -> 586 caught.
- **Item 2 (R829-2 F2).** Both builder legs re-ran at the head with HOME at the pinned SDK's parent.
  - Leg 0's gate 1b now reads `compiler argv[0]=<pinned-rv32-sdk>/bin/riscv32-linux-gcc version=riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`: ALL GATES PASS.
  - Leg 1 names no RV32 compiler and passes all but gate 11, the placed-build report, as before.
  - `ci_rv32_sdk.py --verify-only --destination <that SDK>` is rc 0 in the same run.
  - The PR body names the build gate 1b used, and says round 2's legs ran the Buildroot 2026.05 build.
- **Item 3, wording only.**
  - R829-2 RES1 = R830-2 RES2: the PR body's round-1 row now says `ctrl_plat` grows by 152 B with one interface and by 144 B with two.
  - R829-2 RES2 = R830-2 RES3: `MAILBOX_SPLIT.md:583` now names the BIND_RX case (fewer than two owed slots free).
  - R829-2 RES3: `SPLIT_CONTROL_MEMORY.md:309` now gives the `sram` growth as the adapter's pointer to its loop.
  - Optional suggestions: no tree change. R830-2 S5 is done in the receipts only: a receipt now computes 0.767 / 0.730 / 0.721 from the recorded column, and the split file's measure is labelled.

Validation (clean clones, pinned RV32 SDK):
- Every `run:` step of the four workflows: 150 rc 0, 215 not run with a stated reason, 0 bad.
  - 110 ran at the head: every `docs.yml` and `elaborate.yml` job, and rtl-fast's `changes`, `bdd-conformance` and six firmware jobs.
  - The other 40 are rtl-fast's `verilator-lint`, `yosys-tool`, `yosys-elaboration`, `split-cdc` and `publication-census`, and `rtl.yml`, reused from `bfe7a9d6`. None of them reads this delta's four files.
- The control campaign caught 586 of 586.
- `fw_coverage.py --check`: PASS; `acmp_mbx.c` is at 106/106 lines and 42/42 branches. The `acmp` arm runs 165 tests with 0 failures; service bounds 47 checks, 0 failures.
- AECP and SRP campaigns, `firmware-boundary` and `firmware-verilator`: PASS.
- `behave`: 508 scenarios passed. `git diff --check` against the merge base: rc 0.
- On this loaded host, `elaborate-gates-1`'s LiteX simulation aggregate needed the runner's own `LITEX_SIM_TIMEOUT=3600` (default 900 s). At 900 s two members were killed and reported as "result UNKNOWN, not a failure". With 3600 s all 8 pass. The override is named in every step log of that job.

Acceptance criteria: ruling items 1 to 3 are met as stated above. K8 fails on its plant, and the two plants on the same loop line still catch theirs (K4, K7).

Open risks/questions: none new. S2b's sync still owes the three items of issuecomment-6811790762, item 4. 32x32 is S15's.
