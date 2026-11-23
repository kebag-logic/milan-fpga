# HANDOFF r3: milan-fpga #983 / PR #986, [A830]

**Status: REVIEW READY at `58f7673b8c57a80230e716bc1774ff9cc2f71ddc`.**

- Committed locally on `pf-linuxprof-1`, one commit on `66b4def3`. NOT pushed: the remote branch is still `66b4def3`.
- All three R902-1 items are addressed, and R902-1-S1 is taken.
- The `[A830] REVIEW READY` is posted on #983: https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7102194723

## What was done

- **F1 (BLOCKER).** `ctrl_loop.h`'s THE SHAPES chain is back to the base byte for byte.
  - The host shape's figures live in a new `sw/firmware/ctrl/host/ctrl_loop_host.h`. A guard before the chain selects it: `#if defined(CTRL_HOST_PLATFORM) && CTRL_LOOP_SHAPE(1u, 1u, 2u)` / include / `#else` / chain / `#endif`.
  - `ctrl_loop.h` defines no figure outside the chain. `shape_costs.py` and `tb/` are unchanged, so no manager decision on the reader was needed.
  - The header is in `host/`, not `loop/`, because `ctrl_plants.py`'s base plant compiles every `loop/*.h` on its own.
- **Budget harness, base vs head, all as at the base:**
  - `shape_costs --check`/`--selftest`, `load_grade --check` and `flip_grade --check --point 1x1/1if`: output identical to the base's;
  - `flip_grade --check`: byte-identical to the base's, including its 8x8/2if FAIL;
  - `run.py --self-test`: reaches the 580 s bound at both, identical to the bound.
- **Gate 41** now reads the table through `shape_costs.py`, and refuses the round-2 placement and the figures-beside-chain placement. At MBX_N_IF 1 and 2 it holds compiled FPGA rows to the reader's rows. Five mutants each fail it in their own words, m1 being `66b4def3`'s `ctrl_loop.h`.
- **Board host build, unmodified** (kebag-logic/ti-sitara-am65x-bsp `pb2-aecp-1` at `afc35064`, cloned read-only into the scratch folder):
  - **35/35 objects and the control program binary are byte-identical** at `66b4def3` and `58f7673b`;
  - the host shape macros are identical;
  - the generated `srp_entity_gen.h` and `aecp_entity_gen.h` are identical;
  - `entity.conf` and `nvm_shape_gen.h` differ only in their recorded revision line.
- **R1:** section 6's rows are `H1` to `H9`, and row 5d cites H2.
- **R2:** the PR body Status uses the reviewer's sentence, and "once pushed" is gone.
- **Identity:** 245/245 FPGA artifacts are byte-identical vs base and vs `66b4def3`, and 240/240 in a full-tree run. `ctrl_loop.h` preprocessing is SAME at 12 points, with 6 `ctrl_loop.o` byte-identical.
- **Docs and quality gates:** 25/25 rc=0.

## For the manager

- **Publish.**
  - Push `pf-linuxprof-1` (`58f7673b`), then replace the PR #986 body with [PR-BODY.md](PR-BODY.md). Its Status names `58f7673b` as the published head.
  - If the body is applied before the push, put `66b4def34dcbc0d371ce4eb339d3d0226875befa` in that one sentence instead.
  - The push restarts the hosted gates (the PR is not a draft), and act must be run from a trusted dev worktree.
- **Re-review.**
  - R902 should re-review `58f7673b`.
  - R900-2's POSITIVE was at `66b4def3`. Round 3 changes artifacts in the Conformance, RTL, Tests and Docs lenses, so the external lenses need covering again at `58f7673b`.
- **Board pin.** `pb2-aecp-1` pins `66b4def3` by archive sha256. Re-pin it to the new head (or to the merge commit) per your plan. The build is byte-identical either way, and its `gen-config.sh --check` will flag only the two revision lines. `$LANES/pb2-aecp` was not read or touched this session.
- **Still owed** (not run this round):
  - the full builder suite and gate 1b;
  - the firmware shards and mutation campaigns;
  - act;
  - candidate-merge validation against current `dev` (`e275d795`).
  - Add the service-budget harness explicitly: `shape_costs.py --check`/`--selftest`, `load_grade.py --check`, `flip_grade.py --check`, `run.py --self-test`. It is in no bank and no hosted workflow.
- **For R902, a note.** Their `preproc_shapes.sh` MBX_N_IF 2 override (an `-I` copy of the contract) never takes effect, because `mbx.h` reads its own directory's contract first, so those points ran at MBX_N_IF 1. The force-included override gives SAME at 2 ([receipts/mbx_n_if_override.txt](receipts/mbx_n_if_override.txt)). Their conclusion stands.
- **Possible new Issues** (not filed): `board: null` or an integer raises TypeError, and a non-integer `gptp.clock_accuracy` raises ValueError (R902-1-S2). Both are base behaviour.
- **Process notes.**
  - `arty_current` (an all-fabric FPGA config) has generated shape (1, 1, 2). Under the macro it takes the host figures, as at `66b4def3`. This is now disclosed in the docs and the PR body, and gate 41 checks and reports it.
  - Disposable work (extracted trees, the board clone and build, mutant trees, a hash-pinned renderer venv) is in `../round3-scratch/`, outside this packet. It is not publishable and can be deleted.
  - One stray bytecode cache this session wrote in the lane (`tb/verilator/ctrl_service_budget/__pycache__`) was removed. Every other ignored cache predates this session.
  - Commit message: one line, no trailers. The PR body carries no tool attribution, per the public-text rule.

Files: [REVIEW-READY.md](REVIEW-READY.md), [PR-BODY.md](PR-BODY.md), [receipts/INDEX.md](receipts/INDEX.md).

REVIEW READY 58f7673b8c57a80230e716bc1774ff9cc2f71ddc
