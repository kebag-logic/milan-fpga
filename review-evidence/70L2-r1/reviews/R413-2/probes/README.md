# R413-2 probes (PR #623, exact head 943a3dac973abc7130fe1a19bb6f5943788a01fe)

All probes run on disposable copies of the review clone (`scratch/tree` at the
head, `scratch/tree597` with the round-1 `test_builder.py` from 597dba85);
never published. The review clone is never edited. `R413_HEAD_TREE` points
the scripts at an unmodified checkout of the head (default: the review clone).
The scratch copies get an index-only `git init; git add -A` in the three
submodules, because the builder test and check_nvm_capture call
`git ls-files` there.

1. Gate 1b on the shipping firmware (about 9 s):
   `python3 instrument_builder.py <copy>/sw/builder/test_builder.py`
   (round-1 instrument, unchanged: env-guarded early return after the
   shipping firmware's `assert_boot_contract()`, and `R413_FORCE_FORGET`),
   then `python3 plants.py <copy> <plant>` and
   `R413_STOP_AFTER_BASELINE=1 python3 -u run_gate1b.py <copy>`.
   Receipts: `receipts/gate1b_head_<plant>.log` (head gate),
   `receipts/gate1b_r1gate_<plant>.log` (round-1 gate).
2. The head gate's own nine verdict-pin controls:
   `python3 instrument_verdict_controls.py <copy>/sw/builder/test_builder.py`,
   then `R413_STOP_AFTER_VERDICT_CONTROLS=1 python3 -u run_gate1b.py <copy>`
   runs `test_baremetal_profile_contract()` up to and including its
   verdict-pin control loop and prints each refusal's named pin
   (`receipts/gate1b_head_verdict_controls.log`).
3. `alias_escape_demo.c` / `weakref_escape_demo.c`: what the two accepted
   spellings compile to (pinned RV32 compiler, -O0 and -Os), a host run
   showing the entity enabled after a failed load, and the gate's
   register-variable question asked with `-fsyntax-only` against a full
   compile (`receipts/alias_escape_compile.txt`,
   `receipts/weakref_escape_compile.txt`, `receipts/alias_register_check.txt`).
4. Service grader: `armed_mutants.py <copy>` (round-1's six wrong rules),
   `grader_mutants_other_reviewer.py <copy> <scratch>` (the other reviewer's
   public W0-W6 script, byte-identical copy), `w6_direction.py <head run.py>
   <W6 run.py>` (is W6 stricter or more lenient).
