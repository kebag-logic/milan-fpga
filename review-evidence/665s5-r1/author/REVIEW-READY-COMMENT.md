[A702] REVIEW READY

Commit: `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` on `665-s5-hooks`, from `dev-soft-core` `5b5f4336`; it merges cleanly onto `dev-soft-core` `a68536fa`. Not pushed: the PR targets `dev-soft-core`.

Changed:
- New `tb/verilator/ctrl_service_hooks/` (`hooks_soc.py`, `hooks_build.py`, `hooks.py`, `run.py`, `hooks_selftest.py`, `README.md`). It measures the eight NFR-SCOUT-03 hooks on S3's platform image, linked unmodified, on S2's split SoC with the Milan CSR window. Shapes: 1x1 (one interface) and 8x8 (two, the ledgered `platform-8x8-two-interfaces`). Face arms: idle (formal) and the labelled answering arm. Each hook runs alone and under the composed load, graded against min(T_svc 20 ms, its ceiling) plus W, with its margin to the normative timeout. Ordering is checked apart from the budget. Each hook has a late plant and an ordering plant, each a scratch copy of the firmware tree.
- Since the owner's decision of 2026-10-30, every hook is graded at the product clock, the CPU at 100 MHz on `sys`; `--cpu-clock milan` gives the 50 MHz history, labelled so. A fit by less than the 6,490-cycle layout swing is a `NARROW` finding (6634982529 item 2). The composed rows open on full buckets with the grandmaster changes first (item 1).
- One shared file outside `tb/`: `sw/firmware/ctrl/test/ctrl_configs.py`, one `OUTSIDE` entry for the TSN stack boundary gate. No RTL, firmware, or S2 or S3 harness file is edited.

Validation (all rc 0, each in a clean clone; `fa925043..eef3d97a` changes only the README):
- `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test`: 22 of 22 checks, 31 of 31 mutants (at `eef3d97a`).
- The 16 plants, `python3 -B tb/verilator/ctrl_service_hooks/run.py --plant <name> --build-dir <build>`: each prints `PLANT <name> caught` with its `LATE <hook>` or `ORDER <hook>` words (at `fa925043`, 1x1, 100 MHz).
- `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1|8x8 [--arm answering] --build-dir <build> --record-findings`: four runs at `fa925043`, regraded at `eef3d97a` with byte-identical tables. Paths 145, 159, 207 and 221; 0 refusals, 0 ordering findings and 0 `NARROW` in each.
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`, all four shards.
- S2's harness: `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1|8x8 --record-budget-findings`, and its `--self-test`.
- `python3 sw/builder/test_builder.py --require-rv32`.
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest`, both `--without verilator` and `--only verilator`.
- 98 docs, scope, idiom and CI gates, including `cd tests && behave` (1977 steps passed).
- Candidate merge onto `dev-soft-core` `a68536fa`, in a scratch clone and not pushed: the self-test passes, and a full 1x1 idle run exits 0 with the same findings by path and verdict.

Acceptance criteria:
- Met: every hook is measured in target cycles at both points, alone and under the composed load, against min(T_svc, its ceiling), with its margin. Ordering is checked apart from the budget, and no ordering defect is found. Each hook's late plant and ordering plant fail with their own words. Every figure names its clock.
- Not met on this firmware base: "each hook within its bound".
  - Alone, every hook fits at both points except H-COUNTERS' ALL push: 27.58 ms at 1x1 and 218.71 ms at 8x8, which is 80 and 608 notices at about 35,000 CPU cycles each.
  - Under the composed load, every hook misses at both points and on both arms except H-DISC at 1x1 on the answering arm (14.03 ms).
  - The four ACMP commands behind the owed one are never answered. On the idle arm, SRP takes no record in the ADP backlog windows. These are the CPU budget harness's two starvations, reproduced on the platform image.
  - S2b's (#810) firmware cuts are not merged at this base (assignment item 3).

Open risks/questions:
- For the maintainer: should S5 re-measure on S2b's head once #810 merges? That is the same four run commands, unchanged.
- For the maintainer: should H-COUNTERS' ALL push be graded as one path, from the event to the last push as the 3.4.2 row reads, or per descriptor?
- The CPU runs at 100 MHz behind this base's crossing to the bus. The product wiring has no crossing; it arrives with S2b, so these figures include the crossing's latency.
- Not measured: the retried notice's row (S2b's), wire timing (S8), and the checks listed in the README's Limits.
