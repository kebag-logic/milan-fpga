# How the probes were run (all at e6d27f3a188286a5d5e30094e07453e2bbea1945)

Each on a byte copy of the isolated review clone (`cp -a`), never on the clone itself.

1. Split leg: `make -C tb/verilator/milan_dp split VERILATOR=<pinned 5.050> VERILATOR_JOBS=16`
2. CDC structure: `cd tb/verilator/milan_dp && python3 -B split_cdc_check.py --selftest`
3. Placement self-tests: `python3 -B syn/ooc/pp_placement_selftest.py`; `python3 -B syn/ooc/pp_baseline.py --selftest`
4. Own mutants: on two further copies, `python3 -I scripts/own_drop_mutants.py <copy> halved|stuck1`,
   then `rm -rf tb/verilator/milan_dp/obj_split && make -C tb/verilator/milan_dp split ...`; each must fail.
5. Receipt integrity: sha256 of each downloaded author-r3 receipt against `published_sha256` in
   `review-evidence/665s6-r1/MANIFEST.json` at evidence commit d13c2b09.
