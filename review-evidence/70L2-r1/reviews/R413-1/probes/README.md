# R413-1 probes (PR #623, exact head 597dba8593553ad85b1e94936b016907c4d2003a)

All probes run on a disposable copy of the review clone (`scratch/tree`,
never published); the review clone itself is never edited.

1. Gate 1b, shipping firmware only (about 9 s instead of the whole builder
   test): `python3 instrument_builder.py <tree>/sw/builder/test_builder.py`
   adds two environment-guarded edits to the COPY, then
   `R413_STOP_AFTER_BASELINE=1 python3 -u run_gate1b.py <tree>` runs
   `test_baremetal_profile_contract()` with `--require-rv32` and returns
   right after the shipping firmware's `assert_boot_contract()` (every source
   rule plus the resolver). `R413_FORCE_FORGET=1` restores the forget-on-call
   rule. `plants.py <tree> <plant>` writes one verdict override into the
   copy's firmware (`none` restores the head bytes). Receipts:
   `receipts/gate1b_*.log`.
2. `splice_paste_demo.c`: both spellings compile to a store of the static
   (`receipts/splice_paste_compile.txt`, pinned RV32 compiler, `-O2 -S`).
3. `regrade_compare.py <base run.py> <head run.py> <oracle.json> <receipts...>`:
   the service grader at dev 79c36963 against the head's, on the three
   recorded oracle traces and the public 18199bac 8x8/1x1 `all` receipts.
4. `armed_mutants.py <tree>`: six wrong stretch rules planted into the copy's
   `run.py`, each required to fail `run.py --self-test`.
