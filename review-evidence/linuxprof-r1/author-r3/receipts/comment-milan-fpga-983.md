[A830] REVIEW READY

Commit: `58f7673b8c57a80230e716bc1774ff9cc2f71ddc`, `pf-linuxprof-1` -> `dev-soft-core`, one commit on `66b4def34dcbc0d371ce4eb339d3d0226875befa`. Committed locally, not yet pushed. It answers R902-1 (NEGATIVE at `66b4def3`, https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7101347692).

Changed (4 files, +252 -88):

- **R902-1-F1 (BLOCKER): the host row broke THE SHAPES' reader.**
  - `ctrl_loop.h`'s THE SHAPES chain is restored byte for byte to the base (39 lines, same sha256).
  - The host shape's figures move to a new `sw/firmware/ctrl/host/ctrl_loop_host.h`. It refuses any build except a `CTRL_HOST_PLATFORM` one at (1, 1, 2).
  - A guard before the chain selects that header: `#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)` / `#include` / `#else` / the chain / `#endif`.
  - `ctrl_loop.h` defines no figure outside the chain, so `shape_costs.py` and every first-definition reader read the FPGA table unchanged. The reader and `tb/` are untouched.
- **Gate 41, in its own words:**
  - It reads `ctrl_loop.h` through `shape_costs.py` itself: no host row, each figure defined once per listed row.
  - It refuses two plants: the host row inside the chain, and the host figures beside it.
  - At MBX_N_IF 1 and 2 (R902-1-S1, with the contract force-included and `MBX_N_IF` checked), it holds every FPGA config's compiled row equal to its row under the macro and to the row the reader reads.
  - It holds the host figures equal to 1x1/1if's.
- **R902-1-R1 (RESIDUE):** section 6's rows are `H1` to `H9`, and row 5d cites row H2.
- **R902-1-R2 (RESIDUE, with R900-2-R1):**
  - The PR body's Status uses the reviewer's sentence, naming the head the body is published with.
  - "once pushed" is gone.
  - The new body is in the author packet, for the manager to apply with the push.

Validation at `58f7673b`:

- **Service-budget harness, base vs head, in trees extracted from each revision:**
  - `shape_costs.py --check` PASS, `--selftest` 25/25, `load_grade.py --check` PASS, `flip_grade.py --check --point 1x1/1if` PASS. Each output is identical to the base's.
  - `flip_grade.py --check` produces output byte-identical to the base's, including the base's documented 8x8/2if FAIL.
  - `run.py --self-test` reaches the 580 s bound at both, with identical output up to it and no traceback.
  - R902-1's `probe_shape_costs.py`: `listed()` reads the same 4 shapes at base and head, and raises at `66b4def3`.
- **Gate 41 discriminates.** Restoring `66b4def3`'s `ctrl_loop.h` fails it in the reader's own words. Four other mutants each fail it too: the figures beside the chain, the guard without its macro test, a guard always true, and a host figure that is not 1x1/1if's.
- **Gates:** 32, 41, 42 and `test_bad_configs_rejected` pass. Docs and quality gates: 25/25 rc=0.
- **FPGA firmware view, base vs head:**
  - `ctrl_loop.h`'s full macro set and diagnostics are the same at 12 points (5 FPGA shape headers and none, at MBX_N_IF 1 and 2).
  - The 6 points that compile give byte-identical `ctrl_loop.o`.
  - FPGA identity: 245/245 byte-identical vs base and vs `66b4def3`; 240/240 full-tree.
- **The board repository's host build** (ti-sitara-am65x-bsp at `afc35064`, unmodified Makefile, `-DCTRL_HOST_PLATFORM`), at `66b4def3` vs `58f7673b`:
  - 35/35 objects and the binary are byte-identical;
  - the same host shape macros;
  - generated headers identical except for their milan-fpga revision lines.

Acceptance criteria: met. The FPGA guard and rows are untouched and read unchanged. Generation, identity and docs hold.

Open risks and questions:

- Not run: the full builder suite, gate 1b, the firmware shards and mutation campaigns. The service-budget harness is in no bank and no hosted workflow, so the candidate validation should run it.
- An observation for the reviewer: an `-I` copy of the contract does not set MBX_N_IF 2, because `mbx.h` reads its own directory's copy first. So R902-1's two-interface preprocessing points ran at 1. The force-included override gives SAME at 2 as well.
- R900-2's POSITIVE was at `66b4def3`. Round 3 touches the Conformance, RTL, Tests and Docs lenses, so they need covering again at `58f7673b`.
- Pushing restarts the hosted gates; the PR is not a draft.
- The board pins `66b4def3`, and re-pinning is the manager's step.
