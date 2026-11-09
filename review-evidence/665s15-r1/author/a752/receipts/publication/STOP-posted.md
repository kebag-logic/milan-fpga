[A752] STOP

Head: `6857012df33f51aa6e3cb6eafff26c4f82f0ea77`, branch `665-s15-32x32`: one commit on `dev-soft-core` `a9d69c77`. No merge, no rebase, no force, no amend, nothing pushed.

The exit fires at item 2 (issuecomment-6723527155): "STOP with the census, and the limit that blocks you, if a generator, the contract or the firmware cannot reach 32x32/2if without a design decision." None of the three can.

**Item 1, committed:** `docs/design/SHAPE_32X32_CENSUS.md`, linked from the docs index.
- The shape is the 8x8 config with 32 listener and 32 talker rows of eight channels, plus the CRF pair. Stream n is on interface n mod 2, as the two-interface build does today.
- Every per-shape limit 32x32/2if crosses, in the nine areas the assignment lists. Each has file:line, what bounds it, its rule, and its figure at 1x1/1if, 8x8/2if and 32x32/2if.
- The rule for each limit that states none; the three limits that need a decision.
- Every figure was taken on a scratch clone of the base, lifting one reported limit at a time. No lift is in the tree.

**The blocking limit: the saved-state record space and slot, owned by #823 (open).**
- The builder's 16 streams per direction (`sw/builder/endstation_builder.py:1464`) has no rule of its own. It is the record space's 16-id blocks for BINDING, FORMAT and OFFSET (`hdl/milan/KL_nvm_backend.sv:285-287`); 33 are needed in each direction.
- 395 writable names, against 128 NAME ids (`KL_nvm_backend.sv:248`; the builder at `:2740`; `sw/firmware/ctrl_nvm/nvm_shape.h:133`).
- 596 records, against the 256 ids of `record_id[7:0]` (`nvm_shape.h:132`).
- A 99,080 B image, against one 64 KiB slot (`nvm_shape.h:134`): 151 %.
- The builder, the F1 store's link and the fabric backend each refuse the shape at these limits. Lifting them changes the KLJ2/F07.8 format every shape's saved state uses. The choices are the record-ID width or allocation, the slot size or a compact name encoding, compatibility with existing journals, and the VERSION chain. #823's scope owns each of them.

**Two more limits that need a decision before items 3 and 5** (census section 4):
- **The contract's per-interface tables are full at 16.** That is the bound-talker, publication and face entries, and the bit-per-source `DA_GATE.OPEN`, `LICENCE.ACTIVE` and `TALKER_DECL.DECLARED` fields (`sw/mailbox/mailbox.yaml:93-97`, `:304-307`, `:340-346`, `:361`, `:372`, `:406`, `:496-499`).
  - The firmware writes sink k into entry k of its interface's table (`sw/firmware/ctrl/acmp/acmp_mbx.c:14-15`, `:57-63`), so 33 entries are needed.
  - Per-interface ordinals would still need 17 on the primary, where both CRF streams are.
  - Any growth moves a field, which the contract's own rule makes a major change (`mailbox.yaml:28-33`).
- **The datapath's fixed-width stream fields.** Elaborated at 32 streams, the datapath stops on five guards:
  - the record blocks;
  - the render crossbar's 3-bit stream field, at most 8 streams (`hdl/ieee1722/aaf/KL_render_queue.sv:324-325`);
  - two 4-bit talker indices (`KL_talker_diag_ctx.sv:131-132`, `KL_media_clock_restart.sv:196-197`);
  - the map writer's 8-bit cursors (`hdl/milan/milan_datapath.sv:5228-5232`).
  - The 5-bit SRP row index (`hdl/common/csr/milan_csr.sv:614`) is behind them.

**Lifted by a rule, once the above are decided** (census section 3):
- ACMP's 16 sinks and sources (`third_party/tsn-c-stack/include/acmp.h:157-162`) to the shape's 33, as a build define or a tsn-c-stack donor patch.
- The SRP pool: 144,832 B at 32x32/2if, from its own formula (`sw/firmware/ctrl/srp/srp_mbx.h:94-98`).
- A simulation-only memory map: `sram` needs at least 243,920 B against its 224 KiB region.
- Each ring and bucket derived from a cited rate or timer. The contract states no derivation for them today.

**Decisions asked, with a recommendation each:**
1. **The record space.** (a) Resume S15 on #823's head once #823 lands a record space sized from the shape: recommended. (b) Size F1's record space and the backend from the shape here, ahead of #823: this would make #823's format choices in the wrong lane. (c) Give the simulation shape saved state for fewer descriptors: it changes what the save groups at 32x32 measure.
2. **The contract's tables.** (a) A variant layout generated from the shape's per-interface counts, as `--variant-interfaces` generates the two-interface contract today, with the tracked 2.4 outputs unchanged: recommended. (b) A major contract sized for the largest shape, which moves every shape's layout.
3. **The datapath.** (a) Hold #859's "the datapath elaborates and runs at the shape" until #640's redesign replaces these per-stream fields; the mailbox and the CPU harness, which hold no datapath, run the point. Recommended. (b) Widen each field from the shape's counts here, which changes the datapath's netlist at every shape.

**Gates at the head**, each on a fresh clean clone, every rc 0:
- **Every `run:` step of every job a pull request to `dev-soft-core` triggers** (rtl-fast, elaborate, rtl as for a ready PR, docs): 136 steps ran, rc 0 each; 221 not run, each with its reason; 0 bad.
  - The firmware jobs: `test_ctrl_firmware: PASS`; `firmware coverage: PASS (35 files)`; control `mutants: 570 of 570 caught`; AECP 137 and SRP 280 plants caught, none escaped; `ctrl_boundary: PASS` in firmware-boundary and firmware-verilator, each with the LiteX venv.
  - behave: 508 scenarios passed. The lint is at its ratchet (89). Yosys: 61 tops, 0 failed. The elaborate legs: `ALL GATES PASS EXCEPT 1 NOT RUN` each, and 8 of 8 LiteX simulations.
  - `full-ci-gate` classifies this docs-only head `rtl=false`.
- **The full sweep as four shard units**, the `capture_coherence` shard on four CPUs: 65 of 65 suites, 2,192,828 checks, 0 in-suite failures, no preflight failure.
  - `milan_dp` hit its 4,800 s wall clock in shard 0 with every CPU of the host booked ("result UNKNOWN, not a failure").
  - Re-run as the sweep runs it, alone on a booked range, it passed: 38 minutes, 13,796 checks.
- `test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's make arm; gate 11's calibration report). `test_ctrl_nvm.py --require-rv32 --self-test` passed; the harness self-test `0 failures`, the hook harness's `28 of 28 checks pass; 96 of 96 mutants caught`, the split store target's `checks: 73   failures: 0`; `gen_mailbox.py --check --crosscheck` and `--selftest` passed; `cd tests && behave` passed; `git diff --check a9d69c774d HEAD` is clean.
- **S2's harness**, every group of the point at this base, the T_svc misses recorded, not graded (S2b's):
  - 8x8/2if: 17 groups, 0 refusals, 57 misses;
  - 1x1/1if: 18 groups, 0 refusals, 34 misses;
  - `fw_service_budget` passed in the sweep.
  - 32x32/2if cannot be built.
- **One booking fault of mine:** two of my dispatchers started two units on one range in the same second. The overlap lasted 3 s, because one of the two failed at once on a flag this base's harness lacks. Both dispatchers now pick under one lock.

