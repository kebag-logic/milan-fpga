[A594] REVIEW READY

M8a-1 round 3, answering [R606-2](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107064124) and [R607-2](https://github.com/kebag-logic/milan-fpga/pull/721#issuecomment-6107065061) per the [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6107088105).

Commit: `ce10328c3d89d81509e47836fa4a48b22ecdbc20` (five new commits on `76605880`, no rebase or amend; local, not pushed)

Changed:
- `22caf735` (item 1, R606-2-F1): `docs/design/SPLIT_CONTROL_MEMORY.md` joins `scripts/ci_scope.py`'s `GATE_READ_DOCS`, with a classification case. `CI_WORKFLOWS.md` lists seven gate-read pages and names `sw/litex/test_ctrl_memory.py` as this one's reader.
- `087df144` (item 2, R606-2-F2): the SoC child refuses every `pythondata_software_*` import in every interpreter, and writes LiteX's headers without the firmware make inputs, as `sw/builder/test_shipping_clock_constraints.py` does. A mutant is graded only against an arm that passed unmutated in the same run. `CI_WORKFLOWS.md` and `TESTING.md` state the arm's needs: PyYAML and the pinned, patched LiteX, and no firmware data package.
  - Why not provision the packages: the arm compiles nothing. LiteX reads the packages only to write `variables.mak`, a software-build make input; the gateware, its init files and `csr.csv` read neither. Provisioning would widen the shared pins and the `elaborate` install for packages no gate here uses.
- `4a2608cd` (item 3, R607-2-F1): new rule `load coverage` (`memory map`): every section with initial bytes must be carried by the load segments' file bytes, the only bytes that program `rom`. `entry bytes` also requires those bytes to carry the first word at the reset address.
  - Regressions: the test's ELFs; the genuinely linked probe with its reset segment emptied or cut to one word, or `.data`'s segment emptied; and the real split SoC build, refused before any Verilog or init file.
  - The linked probe's rom words must also equal the toolchain's `objcopy -O binary`.
  - Four new mutants, 44 in all; 17 registered rules.
- `4a57b41d` (item 4, R606-2-F3): both ledgers give the partial placement `124 + 6 = 130`, 8.5 over 121.5 at the measured 53. The give-way text names the ruled 56-tile firmware allocation.
- `ce10328c` (item 5): R606-1-R1's two exact texts.

Validation: the hosted-parity set, at the committed head, every command unpiped, rc 0:
- `docs.yml`, every command of `docs-check` (80), `wire-accountability` and `docs-check-no-git`: 83 of 83 rc 0.
  - Environment: CPython 3.12.3 with only the job's installs, pinned sv2v v0.0.12, GNU make 4.3, the pinned RV32 SDK installed fresh, no LiteX.
  - The em-dash base is the merge base with `dev` `ac2c5e77`.
  - `test_builder.py --require-rv32` reports `ALL GATES PASS EXCEPT 14 NOT RUN`: the LiteX arms, which that job has no interpreter for, and gate 11.
- `python3 -I scripts/ci_scope.py --selftest`: PASS. `scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md`: `true`.
- `scripts/ci_events.py --check`: OK, 1,749 contract items. `--selftest`: PASS, 2,374 arms.
- The LiteX aggregate in a `litex_pins.txt`-only CPython 3.12.3 interpreter (patch series applied, pinned Verilator 5.050):
  - `run_litex_sims.sh --selftest`: 10 checks PASS.
  - Aggregate: **7 of 7 PASS**.
  - `test_ctrl_memory`: 123 checks, `RESULT: PASS`, 44 of 44 mutants caught.
- `test_builder.py --require-elaboration --require-rv32` in the same interpreter: `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11, the bench build tree, as before).
- `test_ctrl_memory.py` in an interpreter that has the firmware data packages: the same log line for line, once temporary names are normalised.
- Control run with the include hook removed, in that interpreter: rc 1 as planted. The split export fails by name, and all six SoC mutants report `not graded`.

Acceptance criteria (round-3 items): met.
1. `ci_scope.py --selftest` returns rc 0, and the page classifies `true`.
2. In the pins-only interpreter: `RESULT: PASS`, 7 of 7, and every SoC mutant is killed by its own check, not by an ImportError.
   - `main() staging check removed` is killed by the stage-size control, which now exports.
   - `shipping firmware linked` is killed by `the split build adds no shipping firmware`.
3. Refusals before export:
   - R607-2's `probe_load_soc.py`, run unmodified, no longer reproduces: refused `reset entry: no load segment carries the first word at the reset address 0x00000000`, no Verilog.
   - Its `probe_elf_loads.py` reports the empty reset segment refused by `entry bytes` and the short one by `load coverage`.
   - Removing or weakening either rule is killed by name.
   - The four shipped split images plan and program byte-identically.
4. 130 and 8.5 in both documents, re-derived from the table rows.
5. Residue applied verbatim.

Open risks/questions:
- The suite sweep, Yosys and Vivado were not rerun. No file under `hdl/`, `tb/` or `syn/` and no gitlink changed since `76605880`, and the mapping inputs are unchanged.
- The local Actions replica needs the pushed head.
- R606-2's optional S1-S4 are not taken; S5 is the manager's separate Issue.
