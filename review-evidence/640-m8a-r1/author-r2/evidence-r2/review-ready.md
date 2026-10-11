[A594] REVIEW READY

M8a-1 round 2, answering R606-1 and R607-1 per comment 6105011666.

Commit: `76605880a20005cbc2acad1b23ba2ccebde64ca8` on `640-m8a`, three new commits on `08b90b68` (no rebase or amend). Not pushed.

- `be431eec`: code, test, rule table.
- `516d7fb8`: ledger and fit docs.
- `76605880`: one sentence of the rule section.

Changed:

- **Rules, item 1.** `sw/litex/ctrl_memory.py` registers its 16 refusal rules in `RULES`, and each `Refusal` names its rule. The check names are unchanged. `SPLIT_CONTROL_MEMORY.md` section 3 lists the same rules, and the test requires the two to be equal.
  - New rule `writable in rom` under `memory map` (R606-1-F1).
  - New rule `elf truncated` under `memory map` (item 3): every header, table, symbol, name and load-segment read is bounds-checked.
- **Mutation check, item 1.** `sw/litex/test_ctrl_memory.py` gives every rule a refusal arm and a mutant. 40 mutants each rebuild one function or class from its own source with one edit, and each must be killed by a named FAIL. A rule without an arm or a mutant fails the test.
  - Budget boundary: 56.0 RAMB36 is accepted and 56.5 refused.
  - Simulation: the largest image's sram banks (64, 32, 8, 4 and 2 KiB) in both regions. It samples 47 addresses per region up to word `0xFFFF`, past 224 KiB. Each must answer err alone, and none of 215 alias cells may be written. A read presented on the cycle after an err must ack with its own data.
- **SoC hookup, item 2.** A SoC arm drives `milan_soc.py`'s own `main()` on the shipping 1x1 config's argv, exporting without Vivado or software.
  - Over budget, overlap and the 8x8 stage are each refused by its rule before any Verilog is written.
  - `--ctrl-mailbox` alone and `--ctrl-firmware` alone are each refused (rc 2).
  - The split export holds exactly the image's banks and no BIOS ROM or SRAM, and its rom banks hold the image.
  - The Builder is told to build no BIOS and no shipping firmware.
  - R606-1's `main()`-stage mutant is one of the 40 and turns it red.
- **Docs, item 4.**
  - Both 56-tile sentences: 116 tiles, 5.5 below the ceiling.
  - `AREA_BUDGET.md:382-383`: the ruled limit, and 53 out of context.
  - The plan's lane row names the ruled 56-tile allocation.
  - 231 LUT cells is the `rom` region with its decode and read multiplexer: LUT primitives, 220 Slice LUTs.
  - R607-1-R1 and R607-1-R2 exact texts.
  - The PR body draft names `08b90b68`, the dev merge and the aggregate's 7 of 7.
- **Idiom gate.** `scripts/check_py_idiom.py`'s exec inventory gains the test's one guarded entry: the edit must match once and parse to exactly that one definition.

Validation (each unpiped, rc 0):

- `test_ctrl_memory.py` at `76605880`: 109 checks, 0 failures, `RESULT: PASS`, 40 of 40 mutants caught.
- R607-1's `mutants.py`, unmodified, at `be431eec`: 12 of 12 KILLED by named FAIL lines. The five survivors and the crash of round 1 are among them.
- R606-1's `probe_writable_rom.py` now reports `REFUSED memory map`. R607-1's `probe_malformed.py` refuses every input by name, truncated ELFs included. `probe_ctrlmem_sim.py` and `probe_region_top.py` PASS.
- At `516d7fb8`:
  - `run_litex_sims.sh --selftest` passes, and the aggregate passes 7 of 7.
  - Default and split exports of both AX7101 configs, `08b90b68` against head: 22, 22, 24 and 23 files, 0 differ.
  - The four split and four flat fixture ELFs are byte-identical to round 1's.
  - The OOC inputs are identical to those mapped in round 1, apart from date stamps, so no Vivado run was needed.
  - `test_builder.py --require-elaboration --require-rv32`: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, bench build tree absent, as in round 1).
  - `syn/yosys/run.sh`: 58 of 58.
- At `76605880`:
  - `run_all_suites.sh`: 61 of 61 suites, 2,185,848 checks, 0 failures (4 declared `tsn_fuzz` skips).
  - The idiom, hygiene and documentation gates pass.

Acceptance criteria (round 2, items 1-4): met, with the evidence above. M8a-1's own criteria are unchanged from the round-1 REVIEW READY.

Open risks/questions:

- Not taken, being outside the four items: R606-1-R1 (wording), R606-1-S1 and R606-1-S2. R607-1-S3 is the manager's separate issue.
- The SoC arm exports with `--no-compile-software`, so it reads the Builder's BIOS decision from the flag the Builder reads.
- On a cold metadata cache the hosted `elaborate` job pays one more VexiiRiscv Scala run for the split CPU.
- M8a-2 waits for F-INT PR 2.
