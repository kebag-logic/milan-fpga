[A594] REVIEW READY

M8a-1 round 5, answering [R606-4](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6118557490) and [R607-4](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6118122865) per the [round-5 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6118560882).

Commit: `42678ae2f77fbbef056f7fb99859e0193181e6d7` (one new commit on `8ab2b539`, no rebase or amend; local, not pushed)

Changed (`42678ae2`, documentation only, 3 files, +50 / -44), answering R606-4-F1 = R607-4-F1:
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 now gives the fit of the firmware at `8ab2b539` (dev `c6bd08c6`: F-INT's publication writers, lwSRP `08ee86e8`) and names that revision. It covers the table, bank fill, headroom, which ROM bank Vivado puts in logic, and the LUT figures.
  - The figures of `ce10328c` are kept, with their source named.
  - Section 3 names the revision that round 1's SoC-build controls linked (`c20ed894`).
- `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` update the ledger rows, arithmetic and headroom:
  - firmware +53 RAMB36, +2 RAMB18, +54 tiles;
  - `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125`, and 114 after the release (7.5 below 121.5, reserve untouched);
  - 126 and 115 with every bank in block RAM; 3.5 over before the release;
  - 143 and 132 if the BIOS were kept; partial placement `125 + 6 = 131`, 9.5 over.

Measured at the head:

| Point | `rom` + `sram` need, B | Planned RAMB36 | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT cells / FF |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface | 96,624 + 45,776 | 35.5 | 34 / 2 | 35.0 | 128 / 8 |
| 1x1, two interfaces | 98,056 + 57,152 | 38.0 | 37 / 1 | 37.5 | 89 / 7 |
| 8x8, one interface | 110,344 + 86,336 | 48.5 | 46 / 2 | 47.0 | 417 / 42 |
| 8x8, two interfaces | 111,848 + 112,464 | 55.0 | 53 / 2 | 54.0 | 266 / 34 |

The largest point keeps 1.0 tile (4 KiB) of planned headroom, or 5,064 B counting the slack inside its banks; its flat span is 223,776 of 229,376 B. Nothing exceeds the 56-tile or 224 KB limit, so there is no STOP.

Validation (every command unpiped, rc 0):
- Links: `ctrl_srp_image.py --with-aecp`, split and flat, both shapes, one and two interfaces, at `8ab2b539`; 12 links and 4 plans rc 0.
  - The runtime is the repository recipe run through R607-4's `runtime_probe.py`, unmodified, which only adds `-fno-stack-protector` (#723). Archive hashes are recorded. They differ run to run because `ar` stores member times; the ELFs do not.
  - Control: the same runtime at `ce10328c` links round 1's four split ELFs byte for byte.
- Mapping: `syn/ooc/ctrl_memory_ooc.py` on the four head ELFs, then its Vivado script out of context (Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`) under the exclusive lock: rc 0, 8 of 8 tops, all 13 ROM images read.
- Reviewers' probes, run unmodified:
  - R607-4 `run_fit.py` (head and `previous-` at `ce10328c`) and `compare_fit.py`: `PASS reproduction`.
  - R606-4 `link_points.sh` on both trees and `fit_summary.py`: the same figures, `headroom 5064 B` at the largest.
  - Every head ELF is byte-identical across the three link runs.
- `docs.yml`, every command of `docs-check` (80), `wire-accountability` and `docs-check-no-git`, at the committed head: 83 of 83 rc 0.
  - Environment: CPython 3.12.3 with only the job's installs, pinned sv2v v0.0.12, GNU make 4.3, a HOME holding only the pinned RV32 SDK, and no LiteX.
  - `check_em_dash.py --base c6bd08c6`: 0 findings over 324 added lines.
  - `ci_events.py --check`: OK, 1,821 contract items. `--selftest`: PASS, 2,530 arms.
  - `test_builder.py --require-rv32` reports `ALL GATES PASS EXCEPT 17 NOT RUN`: 15 LiteX arms that job has no interpreter for, gate 11, and gate 1b's mutation, which GNU make 4.3 does not honour.
- The LiteX aggregate in a `litex_pins.txt`-only CPython 3.12.3 interpreter (pinned Verilator 5.050):
  - `run_litex_sims.sh --selftest`: 10 of 10.
  - Aggregate: **7 of 7 PASS**.
  - `test_ctrl_memory`: `RESULT: PASS`, 44 of 44 mutants caught, and the section-3 rule table equals `ctrl_memory.RULES`.
- `scripts/ci_scope.py --selftest`: PASS. `SPLIT_CONTROL_MEMORY.md` and `AREA_BUDGET.md` classify `true`. `syn/ooc/pp_resource_gate.py check-baseline` (the budget page's reader): `baseline PASS: 3 endpoints`.

Acceptance criteria (round-5 items): met.
1. The four points are relinked with a recorded runtime, and the isolated mapping has been run on those images.
2. The fit table, both ledgers' rows and the headroom statements match the new receipts. Earlier figures are kept only with their source named.
3. Limits: 55.0 of 56 planned; 223,776 of 229,376 B.
4. The runtime workaround is used only as the reviewers used it, and it is recorded.
5. Both reviewers' probes were re-run, and they pass.
- R606-4-R1 (residue) is applied verbatim in the PR body text for the manager, together with the round-5 figures.

Open risks/questions:
- No integrated route and no boot in this round (M8a-2).
- The suite sweep, Yosys, the elaboration gate and the firmware host suites were not run, because `42678ae2` changes three pages under `docs/design/` and nothing they read. The merge `8ab2b539` belongs to the manager's merge-candidate validation.
- The local Actions replica needs the pushed head.
- R606-4-S1 is optional and not taken. This round shows the erosion it describes: one dev merge cost 0.5 RAMB36 at the largest point.
