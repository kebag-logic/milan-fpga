# [A830] REVIEW READY: milan-fpga #983 / PR #986, round 3

- **Commit:** `58f7673b8c57a80230e716bc1774ff9cc2f71ddc` (`pf-linuxprof-1`, tree `6dbb2eba`). One commit on `66b4def34dcbc0d371ce4eb339d3d0226875befa`. Local, not pushed.
- **Answers:** R902-1 ([PR #986 issuecomment-7101347692](https://github.com/kebag-logic/milan-fpga/pull/986#issuecomment-7101347692)), NEGATIVE at `66b4def3`: F1 BLOCKER, R1 RESIDUE, R2 RESIDUE (which carries R900-2-R1).
- **PR description:** [PR-BODY.md](PR-BODY.md). **Evidence:** [receipts/INDEX.md](receipts/INDEX.md).

## Delta from 66b4def3

`git diff --stat 66b4def3..58f7673b`: 4 files, +252 -88.

- **`sw/firmware/ctrl/loop/ctrl_loop.h`**
  - THE SHAPES chain is restored byte for byte to the base: 39 lines, sha256 `f1bbae92...` at both.
  - The host row and its comment block are gone from it.
  - The diff against the base is now only a guard. It sits between `CTRL_LOOP_SHAPE`'s definition and the chain: `#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)`, then `#include "../host/ctrl_loop_host.h"`, then `#else`. A closing `#endif` follows the chain's own `#endif`. Five comment lines say why.
- **`sw/firmware/ctrl/host/ctrl_loop_host.h`** (new)
  - It carries the host figures, which are 1x1/1if's, unchanged from round 2.
  - It carries round 2's comment on what the stated profile claims and does not claim.
  - It `#error`s unless it is reached through `ctrl_loop.h` by a `CTRL_HOST_PLATFORM` build at (1, 1, 2).
  - It is in `host/` because the firmware's base plant (`ctrl_plants.py` BASE) compiles every `loop/*.h` on its own, and a header that refuses a non-host build would fail there. `../plat/` includes are already the tree's idiom.
- **`sw/builder/test_builder.py`**, gate 41
  - `_check_shapes_text`, `_shapes_as_read` and `_shapes_reader` read `ctrl_loop.h` through `shape_costs.py` itself. The module is loaded from source with no bytecode cache. The table must read and list no host shape, and each of its 8 figure names must be defined once per listed row and nowhere else in `ctrl_loop.h`.
  - Two planted placements must be refused, each in its own words: the round-2 host row inside the chain, and the host figures stated in `ctrl_loop.h` beside the chain.
  - `_check_fpga_rows`, at MBX_N_IF 1 and 2 (R902-1-S1), requires every FPGA config's compiled row to equal its row with the macro and the row `shape_costs.py` reads for its shape.
  - `_contract_at` and `_shape_figures` force-include the contract, and the probe prints `MBX_N_IF` and checks it.
  - The host figures must equal the (1, 2, 2) row's, the rule the header states.
  - The host shape must be refused at two interfaces.
  - `HOST_MACRO_FILES` gains the new header.
  - The text check runs whether or not a C compiler is found.
- **`docs/ENDSTATION_BUILDER.md`**
  - Section 6's key rows are `H1` to `H9`, and row 5d cites "row H2".
  - "The firmware shape" paragraph now describes the header, the guard, the unchanged table and what gate 41 holds.
  - The Contents line follows.

## Closure of each finding

### R902-1-F1 (BLOCKER; Conformance, RTL, Tests): the host row broke THE SHAPES' reader

**The required outcome, item by item** (receipts are named in brackets):

- **The four budget commands reach the base verdicts with the four FPGA rows read unchanged.**
  - `shape_costs.py --check` PASS, `--selftest` 25 of 25, `load_grade.py --check` PASS and `flip_grade.py --check --point 1x1/1if` PASS. Each output is byte-identical to the base's.
  - `66b4def3` gives ValueError on each, as R902-1 recorded.
  - [`budget_*_{base,r2,head}.txt`]
- **`flip_grade.py --check` and `run.py --self-test` grade as at the base rather than raise.**
  - `flip_grade.py --check`: head output byte-identical to the base's, including the base's documented 8x8/2if FAIL (rc 1 at both).
  - `run.py --self-test`: base and head both reach the 580 s bound (rc 124) on a loaded host. Their 1944 output lines are identical, with no traceback at either. The verdict is not established at either, as at R902-1's base run.
- **R902-1's own probe.** `probe_shape_costs.py`, unmodified, gives the same four shapes and `at(1)`/`at(2)` at `854bd723` and at `58f7673b`. It raises at `66b4def3`. [`probe_shape_costs.txt`]
- **The host row is selectable only under `CTRL_HOST_PLATFORM`, and no reader takes it as an FPGA shape.**
  - The host figures are not in `ctrl_loop.h`'s text at all. Every figure name there is defined exactly 4 times, once per FPGA row, as at the base.
  - `tb/` is untouched, so the reader's contract is unchanged and needs no host clause.
  - Gate 41 holds both: one function reads the table, and a second checks it against the compiler at 1 and 2 interfaces. [`gates_32_41_42_head.txt`, `integrity.txt`]
- **A check in this PR's gates fails on this defect.**
  - Mutant m1 restores `66b4def3`'s `ctrl_loop.h` into the head tree. Gate 41 fails: "shape_costs.py does not read THE SHAPES: ctrl_loop.h states "// THE HOST PLATFORM's shape (#983) ..." for the shape (2, 9, 9)", the reader's own words, and `listed()` raises again.
  - The other mutants each fail gate 41 in their own words:
    - m2: the host figures beside the chain;
    - m3: the guard stripped of its macro test, which the reader then takes as the chain's head;
    - m3b: the guard's macro test always true, with the gate's guard text following it, so only the compile check can see it;
    - m4: a host figure that is not 1x1/1if's.
  - Gate 41 is green at the head. [`gate41_mutants.txt`]
- **The reader did not need to change**, so the manager's decision R902-1 asked for in that case is not needed. `shape_costs.py` and its README are untouched.

**The issue's frozen criteria.**

- "The FPGA scheduler-shape guard and its rows are untouched": the chain is byte-identical, and the `CTRL_LOOP_SHAPE` macro and `CTRL_LOOP_SOURCES`/`SINKS` above it are unchanged.
- "FPGA profile validation is unchanged":
  - the budget harness gives the base's outputs (above);
  - `ctrl_loop.h`'s full macro set and diagnostics are SAME at 12 points: 5 FPGA shape headers and none, at `MBX_N_IF` 1 and 2;
  - the 6 points that compile give byte-identical `ctrl_loop.o` [`fpga_preproc_base_vs_head.txt`];
  - 245 of 245 FPGA artifacts are byte-identical to the base and to round 2 [`identity-result.json`];
  - a full-tree run gives 240 of 240 [`identity_fulltree.txt`].

**The board's host build compiles the same (1, 1, 2) shape.** It was cloned read-only: kebag-logic/ti-sitara-am65x-bsp at `afc35064`, which pins `66b4def3`.

- **Generated values.**
  - `aecp_entity_gen.h` and `srp_entity_gen.h` are byte-identical at both trees: `CTRL_SRP_SOURCES 1u`, `CTRL_SRP_SINKS 2u`.
  - `entity.conf` and `nvm_shape_gen.h` differ only in the milan-fpga revision line they record. So the board's `gen-config.sh --check` passes against `66b4def3` and names those two against `58f7673b`.
  - [`board_gen_config.txt`, `board_gen_values.txt`]
- **Object bytes.**
  - The board's unmodified Makefile (`-DCTRL_HOST_PLATFORM`, `-include config/srp_entity_gen.h`) builds its control program at both trees: **35 of 35 objects and the linked binary are byte-identical**. `ctrl_loop.o` is sha256 `204afd95...` at both.
  - The selected shape macros are identical: 950, 1010, 735, 285, 85, 34, 130 and 35 at `MBX_N_IF 1u`.
  - [`board_host_build.txt`]

**An observation on the round's evidence, for the reviewer.**

- R902-1's `preproc_shapes.sh` sets MBX_N_IF 2 with a contract copy in an `-I` directory placed ahead of `mbx/`. But `mbx.h` includes `"mbx_contract.h"` from its own directory first, so that copy is never read and those points ran at MBX_N_IF 1 [`mbx_n_if_override.txt`].
- Gate 41 and `fpga_preproc.sh` force-include the contract instead, as `ctrl_arms.py` does, and print `MBX_N_IF`. With that override the two-interface points are also SAME.
- This does not change R902-1's conclusion.

**Also made explicit.** `arty_current`'s generated shape is (1, 1, 2). Under the macro it takes the host figures, as it would have at `66b4def3`. It is an all-fabric config, and no build input defines the macro. Gate 41 now compiles that case, holds it to the host figures, and reports it apart from the refused points.

### R902-1-R1 (RESIDUE; Docs): section 6 labels collided with section 3

- Section 6's rows are `H1` to `H9`, and row 5d reads "(section 6, row H2)", `board.gptp_owner`.
- `grep -n '^| 6[a-i] |' docs/ENDSTATION_BUILDER.md` lists only line 1033, section 3's `6a`.
- Gate 41's planted row label follows (`H0`).
- Gates 32 and 41 pass.

### R902-1-R2 (RESIDUE; PR body, carrying R900-2-R1)

- The Status paragraph now reads: "Published head: `<sha>`. The evidence below is local source-head evidence; hosted acceptance is tracked separately."
- "once pushed" is gone from the checkout comment.
- The incomplete-gate disclosures are kept.
- `<sha>` is `58f7673b...`, not the reviewer's `66b4def3...`, because the body is to be applied with round 3's push. If the body is published before that push, the manager substitutes `66b4def3...` into that one sentence.

### R902-1-S1 (SUGGESTION; Tests)

Taken: gate 41 checks every FPGA row at MBX_N_IF 1 and 2, with the override proven by the probe.

### R902-1-S2 (SUGGESTION; Robustness)

Not taken. Here, as at the base, a non-integer `gptp.clock_accuracy` raises ValueError. It joins the disclosed `board: null` / integer TypeError as candidate follow-ups, which are not filed.

## Validation at 58f7673b

| Check | Result |
|---|---|
| Gates 32, 41, 42 | pass. 116 == 116 keys. Gate 41: host TSpec 217 not 73; THE SHAPES read as 4 FPGA rows, with both plants refused; the host shape at 1x1/1if's figures; 4 FPGA points unmoved at 1 and 2 interfaces. Gate 42: 31/31. |
| `test_bad_configs_rejected` | pass |
| Service-budget harness, base vs head | `shape_costs --check`/`--selftest`, `load_grade --check`, `flip_grade --check --point 1x1/1if`: pass, output identical to base. `flip_grade --check`: identical to base (base's 8x8/2if FAIL). `run.py --self-test`: bound reached at both, identical to the bound. |
| Gate 41 discriminates | 5 mutants, each refused in its own words |
| FPGA `ctrl_loop.h` preprocessing, base vs head | 12 of 12 SAME, 6 `ctrl_loop.o` byte-identical |
| FPGA identity | 245/245 vs base and vs `66b4def3`; 240/240 full-tree |
| Board host build, `66b4def3` vs `58f7673b` | 35/35 objects and binary byte-identical; generated headers identical but for revision lines |
| Docs and quality gates (25) | 25/25 rc=0, including `docs_check`, `check_em_dash --base 854bd723`, bare-metal `--check` (1910 files) and `--selftest`, `check_py_idiom`, `gen_toc --check` |

**Acceptance criteria (#983): met.**

- FPGA identity holds.
- The FPGA guard and rows are untouched, and the tree's reader reads them as at the base.
- The profile's image and ADP fields generate.
- The docs match the code.

**Open risks and questions:**

- **Not run:** the full builder suite, gate 1b, the firmware shards and mutation campaigns, and act. They are owed on the final candidate. The service-budget harness is in no bank and no hosted workflow, so the candidate validation should name it.
- **Push effects:** pushing `58f7673b` restarts the hosted gates (the PR is not a draft).
- **Re-review:** R900-2's POSITIVE was at `66b4def3`. Round 3 changes artifacts in the Conformance, RTL, Tests and Docs lenses, so those must be covered again at `58f7673b`.
- **The board pin:** the board branch pins `66b4def3` by archive sha256. Re-pinning is the manager's step. The control program builds the same bytes at either revision.
