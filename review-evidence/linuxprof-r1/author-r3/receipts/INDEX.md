# milan-fpga #983 round 3 receipts

Head `58f7673b8c57a80230e716bc1774ff9cc2f71ddc` (tree `6dbb2eba`), parent `66b4def34dcbc0d371ce4eb339d3d0226875befa` (round 2, published), source base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`. Branch `pf-linuxprof-1`, committed locally, not pushed.

How the receipts were made:

- Every command ran in the foreground.
- The service-budget commands, the preprocessing comparison and the mutants ran in disposable trees extracted with `git archive` from each revision. Each tree had its five submodules extracted at the gitlinks that revision pins (the scratch folder, outside this packet).
- The builder gates and the docs gates ran in the lane checkout, because they need `git grep` / `git ls-files`.
- Local paths are written as `<TREE>`, `<SCRATCH>` or `<D>`.
- The tracked tree was clean after every run.

| Receipt | What it shows | rc |
|---|---|---|
| [probe_shape_costs.txt](probe_shape_costs.txt) | R902-1's `probe_shape_costs.py`, unmodified: `shape_costs.listed()` reads `ctrl_loop.h` at `854bd723` and at `58f7673b` as the same four shapes, with the same `at(1)` and `at(2)`. It raises at `66b4def3`. | 1 (from `66b4def3` alone, as expected) |
| `budget_shape_costs_check_{base,r2,head}.txt` | `shape_costs.py --check`: PASS at base and head, with identical output. ValueError at `66b4def3`. | 0 / 1 / 0 |
| `budget_shape_costs_selftest_{base,r2,head}.txt` | `shape_costs.py --selftest`: 25 of 25 planted controls refused at base and head. ValueError at `66b4def3`. | 0 / 1 / 0 |
| `budget_load_grade_check_{base,head}.txt` | `load_grade.py --check`: PASS; HELD 1x1/1if 0.511 against 0.70. Output identical at base and head. | 0 / 0 |
| `budget_flip_grade_check_1x1_{base,head}.txt` | `flip_grade.py --check --point 1x1/1if`: PASS, identical output. | 0 / 0 |
| `budget_flip_grade_check_{base,r2,head}.txt` | `flip_grade.py --check`, all points. It grades and FAILs 8x8/2if at base, which is the documented base state. Head output is byte-identical to the base's. `66b4def3` raises ValueError before grading. | 1 / 1 / 1 |
| `budget_run_selftest_{base,head}.txt` | `run.py --self-test`, 580 s bound, base and head run in parallel on a loaded host. Both reach the bound (rc 124) while still grading controls. Their 1944 output lines are identical, with no traceback. Neither verdict is established. | 124 / 124 |
| [gates_32_41_42_head.txt](gates_32_41_42_head.txt) | Gates 32, 41, 42 at the head. Gate 32: 116 == 116 keys. Gate 41 now reports three lines (see the ledger below). Gate 42: 31/31. | 0 |
| [gate_bad_configs_head.txt](gate_bad_configs_head.txt) | `test_bad_configs_rejected` | 0 |
| [gate41_mutants.txt](gate41_mutants.txt), [scripts/mutant.py](scripts/mutant.py) | Gate 41 against five mutants of the head tree, each failing in its own words. Details below this table. | 1 x 5 (expected) |
| [fpga_preproc_base_vs_head.txt](fpga_preproc_base_vs_head.txt), [scripts/fpga_preproc.sh](scripts/fpga_preproc.sh) | `ctrl_loop.h`'s full macro set and diagnostics (line numbers masked) at 12 points, base vs head. The points are 5 FPGA shape headers and none, each at `MBX_N_IF` 1 and 2. `MBX_N_IF` is set by force-including the contract, and the receipt prints it. All SAME. The 6 compiling points' `ctrl_loop.o` are byte-identical. `CTRL_LOOP_HOST_H` is defined at none. | 0 |
| [mbx_n_if_override.txt](mbx_n_if_override.txt) | An `-I` copy of the contract ahead of `mbx/` leaves `MBX_N_IF` at 1, because `mbx.h` reads its own directory's copy first. A force-included copy gives 2. | - |
| [board_gen_config.txt](board_gen_config.txt), [board_gen_values.txt](board_gen_values.txt) | Details below this table. | 0 / 1 (expected; revision lines only) |
| [board_host_build.txt](board_host_build.txt) | The board's Makefile, unmodified, builds its control program against each tree. It uses `-DCTRL_HOST_PLATFORM` and force-includes `config/srp_entity_gen.h`. **All 35 objects and the linked binary are byte-identical**, `fw/ctrl_loop.o` sha256 `204afd95...`. The host shape macros (950/1010/735/285/85/34/130/35, `MBX_N_IF 1u`) are identical too. | 0 |
| [identity-result.json](identity-result.json), `identity-{854bd723,58f7673b}.json`, [identity_probe.py](identity_probe.py) | Round 2's identity probe (R900-1's), unmodified, run fresh at base and head: 245 FPGA builder, image and generator-header artifacts over 5 configs x own/split/all-fabric. 0 changed vs base, 0 vs round 2's `66b4def3` receipt. No generator source and no builder source changed since `66b4def3`. | 0, 0 |
| [identity_fulltree.txt](identity_fulltree.txt) | R902-1's full-tree `identity_probe.sh`, unmodified, on the extracted base and head trees, each running its own builder and generators: 240 files byte-identical, 0 non-zero rcs. | 0 |
| [docs_gates_head.txt](docs_gates_head.txt), [scripts/docs_gates.sh](scripts/docs_gates.sh) | Round 2's 24 docs and quality gates plus `gen_toc --check`, at the committed head: 25 of 25 rc=0. Details below this table. | 0 x 25 |
| [integrity.txt](integrity.txt) | Details below this table. | - |
| [scripts/budget.sh](scripts/budget.sh) | The wrapper the budget receipts were written with. | - |
| [comment-milan-fpga-983.md](comment-milan-fpga-983.md) | The posted `[A830] REVIEW READY` on #983: https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7102194723 | posted |

The five gate 41 mutants (in `gate41_mutants.txt`, applied by `scripts/mutant.py`):

- **m1:** `66b4def3`'s `ctrl_loop.h` restored. Refused: "shape_costs.py does not read THE SHAPES".
- **m2:** the host figures stated in `ctrl_loop.h` beside the chain. Refused: "defines CTRL_LOOP_SLICE_US 5 times".
- **m3:** the guard stripped to `#if CTRL_LOOP_SHAPE(1u, 1u, 2u)`. The reader then takes it as the chain's head.
- **m3b:** the guard's macro test made `1 &&`, with the gate's guard text following it so that only the compile check can catch it. Refused: "(1, 1, 2) without CTRL_HOST_PLATFORM was not refused".
- **m4:** the host slice set to 900. Refused: "not the 1x1/1if row's".

The board receipts (`board_gen_config.txt`, `board_gen_values.txt`):

- Board repository kebag-logic/ti-sitara-am65x-bsp at `afc35064` (branch `pb2-aecp-1`, which pins `66b4def3`), cloned read-only into the scratch folder.
- Its own `gen-config.sh --check` passes against the `66b4def3` tree.
- Against `58f7673b`, it flags `entity.conf` and `nvm_shape_gen.h` only. Generated side by side, those two differ only in their milan-fpga revision line.
- `aecp_entity_gen.h` and `srp_entity_gen.h` are byte-identical: `CTRL_SRP_SOURCES 1u`, `CTRL_SRP_SINKS 2u`.

The docs and quality gates (`docs_gates_head.txt`):

- `docs_check`: 0 findings over 223 md and 1912 files.
- `check_em_dash --base 854bd723`: 0 findings over 105 added lines.
- `check_baremetal_only --check`: 0 over 1910 files, which includes the new header. `--selftest`: 867 arms.
- `check_py_idiom` and `check_doc_paths` pass.
- The em-dash and TOC gates ran under a scratch venv holding only `tools/markdown/requirements.txt`, installed with `--require-hashes`. The venv is outside this packet.

The integrity receipt (`integrity.txt`):

- HEAD and tree.
- THE SHAPES chain is byte-identical to the base: sha256 `f1bbae92...`, 39 lines.
- The full `ctrl_loop.h` diff from the base is the guard alone: +9 lines.
- `tb/` is untouched since the base.
- The raw diff from `66b4def3` has all modes 100644, one file added.
- The submodules are at their gitlinks, and the status is clean.

Housekeeping, disclosed:

- One `python3 -I` call left a `shape_costs` bytecode cache in the lane, because `-I` ignores `PYTHONDONTWRITEBYTECODE`. That file and its directory were removed.
- Every other ignored cache in the lane predates this session.
- `$LANES/pb2-aecp` was not read or touched.

Not run this round:

- the full builder suite, and gate 1b to completion;
- the firmware gate's four shards and the mutation campaigns;
- act;
- the hosted runs.

The scratch folder (trees, venv, board clone and build, mutants) is disposable and not publishable.
