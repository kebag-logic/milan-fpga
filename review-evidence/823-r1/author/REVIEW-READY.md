[A753c] REVIEW READY
Commit: `f3e902f2a96bb27eac6ed7780c70905af34f389e` on `823-nvm-format`. That is four commits on round 1's `61eec0c3`, from `dev-soft-core` `a9d69c77`; the PR will target `dev-soft-core`. Nothing pushed, no PR opened; no merge, rebase, force or amend.

Changed (round 3 of issuecomment-6730985093, decisions 1, 2 and 6 for the split placement):
- **One declaration, two readers.** `sw/firmware/ctrl_nvm/nvm_layout3.h` declares layout 3: 12 block capacities with chained bases, 1,129 ids, a 10-byte F07.8 header with a 16-bit `record_id`, NAME ids 222 to 1,128.
  - The F1 store's codec compiles it and refuses a shape over any block at compile time.
  - The builder's split output (`emit_nvm_split`, `nvm_split.json`) reads it through `scripts/nvm_layout3.py`. It refuses a model over any block, naming the declaration line. The split SoC and the F1 host bench build the store from that file.
  - The format page's gate fails when the declaration is not the space the builder derives from the 32x32 TDM8 shape.
- **The split store** (`sw/firmware/ctrl_nvm`): KLJ3 over layout 3 in `journal_klj3`, 640 KiB at 14,592 KiB, directly below today's journal, in `FLASHBOOT_RESERVED`.
  - A KLJ2 container is refused `VD_VER`, never reinterpreted.
  - At boot the store reads the two headers of today's journal. A KLJ2 header sets the status field `legacy`, and the blank boot's verdict is then `VD_VER`.
  - Its port refuses any program or erase outside `journal_klj3`, so today's journal is never written.
  - The open bits are two 36-word arrays, each with a count of its bits set (decision 6).
  - The whole-image commit is unchanged, apart from erasing every block its container spans.
- **Reference and gates:** `scripts/nvm_klj3.py` and its gate `scripts/check_nvm_klj3.py`, 6 plants, in the docs workflow's NVM record-space step.
- **The split's link:** the split SoC's `MILAN_NVM3_*` constants, `gen_flash_port.py`'s journal rule, the KLJ3 stage, the memory ledger's stage size, and the split target harness on KLJ3.
- **Unchanged:** the processor (at its pin), `KL_nvm_backend`, `milan_baremetal.c`, KLJ2 and the all-fabric limits. The split's save path is its own LiteSPI port, never the processor or `KL_nvm_backend` (receipt `head/split-save-path.md`).
- **Docs:** the 32x32 format page says the format is the split's and the all-fabric placement keeps KLJ2. It grades A3 at the typical 15 us: the room is 95.29 ms, so a suspend 6,352 times its typical value would still fit. Also updated: the store's README, the split target's README, the memory plan, and FASTCONNECT section 6.

Validation: every run is on a fresh clean clone of the head, and every job left its tree clean. Every rc is 0 unless stated. Receipts are indexed from the files present (`INDEX.md`, `SUMMARY.md`).
- **Every `run:` step** of the four workflows a pull_request to `dev-soft-core` triggers, run job by job and step by step: 149 ran, all rc 0. 193 did not run, each with its reason (`gates/verify.md`).
  - `rtl-fast`: includes `cd tests && behave` (14 features, 508 scenarios, 2,330 steps passed), the firmware jobs and the three mutation campaigns. `firmware-boundary` ran with the LiteX environment.
  - `elaborate`, `rtl` as for a ready PR (four Yosys shards and `yosys-portability`), and `docs` (every gate, the builder legs, and the NVM record-space step with the KLJ3 gate).
- **Repeated first runs, both logs kept.**
  - `full-ci-gate`'s target step was rc 1 at first: the local runner left `GITHUB_REF` unset. After the runner fix it is rc 0, and both runs decided `run_full=true`.
  - The LiteX aggregate exited 92 at first: two simulations timed out beside the sweep. Re-run alone, 8 of 8 PASS.
  - Two jobs a host reboot interrupted re-ran from fresh clones.
- **Full sweep**, four shard units (`--shard k/4`): 65 suites, 54 PASS, 0 FAIL, 11 TIMEOUT, at two CPUs per shard beside the workflow jobs.
  - The preflight passed in every shard.
  - The 11 were re-run one by one, uncontended, four CPUs each, with the sweep's own timeouts and masked-verdict check. All 11 PASS, 0 in-suite failures.
  - `capture_coherence` took 2,270 s of its 2,400 s.
- **Builder bank** (`test_builder.py --require-rv32`, the docs and elaborate legs): 106 gates exactly once on each union.
  - Not run, each for its recorded reason: gate 11 (it needs a placed build tree) and gate 1b's MAKEFLAGS mutation (this make does not honour it).
  - The LiteX arms the docs legs skip ran in `elaborate`.
- `test_ctrl_nvm.py --require-rv32 --self-test`: OK across 5 shapes, 474 tests, all 123 planted defects reddened.
- Saved-state writer gate: OK across 5 shapes, every planted defect reddened. `git diff --check` against the merge base: rc 0.

Acceptance criteria (the ruling's round 3 list), met:
- NAME first id 222, last 1,128 and one past 1,129 are tested in the F1 codec, at a build with the NAME block full: `name_block_ends`, `capacity_round_trip` across two erase blocks, and `one_past_refused`. 908 names do not compile.
- At capacity accepted and one over refused in the builder: gate 39 accepts the 32x32 TDM8 overlay's 907 names and refuses 908.
  - The all-fabric shape header still refuses that shape at 128 names (gate 38 unchanged).
  - The split reads no RTL `$error` for this space.
- A KLJ2 journal at boot is refused, the store boots blank and records the reason.
  - `klj2_journal_refused`: either slot of today's journal, which the following commit leaves byte for byte as it was.
  - `klj2_in_slot_refused` and `klj2_journal_unreadable`.
- One plant per rule:
  - the F1 self-test: 122 mutants and one compile-refusal control;
  - gate 39: 10 plants;
  - the reference gate: 6 plants;
  - the page gate: 9 plants and a clean-tree control.
- Split memory, measured at the head against `a9d69c77` with one runtime: the size fixture gains 704 to 712 B of `rom` and 352 to 576 B of `sram`.
  - The four points plan 37.5, 41.0, 51.0 and 57.5 RAMB36.
  - The ledgered 8x8 two-interface point fits its 57.5, with 296 B of `rom` left before 58.0.

Open risks/questions:
- **The gateware VERSION is not moved, and needs a ruling.** The format's own VERSION chain is done: KLJ3 major 3, layout 3, KLJ2 recognised and refused `VD_VER`.
  - Moving the gateware VERSION CSR would change the all-fabric image's identity without any gateware change.
  - The split architecture's section 7 lands the split's VERSION with the default flip.
  - If the ruling wants the minor moved now, it is one commit: `milan_csr.sv:201`, the five simulation assertions and the register map entry.
- Not run, each with its reason in the table:
  - hosted-only steps: receipts, uploads, aggregates and orchestration;
  - the hosted tool builds and sudo installs: the pinned Verilator 5.050, sv2v v0.0.12 and Yosys 0.66 are on PATH instead;
  - the LiteX installs: the prepared environment is used.
  - The rtl workflow's 19 Verilator shards and their unions are covered by the sweep. The physical gPTP job is not triggered by a pull_request.
- The split target harness's recorded results predate KLJ3 and were not measured again. Its portable self-test passes, 73 of 73.
- The target platform's split image was not linked again; its `ctrl_plat` is unchanged.
- Round 4 (decisions 3, 4, 5 and 7: the append-only save path) and area under #818 follow review.
