[A430] REVIEW READY
Commit: `4c2a30debb031595b81c5c4bfc53b601a0fec528` (tree `0a9754d44e40de8c734468be2cedad5ac675d794`), branch `590-592-599-firmware`. Local only, not pushed.

**Changed.** Three commits on `1f039cfe`, each with a one-line subject and no body or trailer. The processor gitlink is dev's `c951a9ff`, and the submodule is checked out at it.
- `9f94b246`: merge of dev `b5c0f69d`. The one conflict, `docs/findings/README.md`, keeps dev's `COMMERCIAL_TIMING_395.md` row at dev's position, followed by this PR's `397_SERVICE_BUDGET.md` row.
- `d0203aac`: `"nvm_started": "0"` added to `WRITER_STATICS` (assignment item 2).
- `4c2a30de`: the [A10] disposition (a) of the STOP. The probe's exact stub, a declaration and an empty `bios_dispatch_hook_required()` mirroring `nvm_host.c:67-72`, is added to `tb/verilator/nvm_cosim/cosim_host.c`: six added lines, byte-identical to the probe's copy. Nothing else changed.
- No stale-statement commit was needed. No RTL, firmware, builder, processor or configuration edit.

**Validation at `4c2a30de`.** All runs are rc 0, on the physical path, never piped. The worktree was clean and HEAD unchanged around every runner. No `d0203aac` receipt is reused.
- `make -C tb/verilator/nvm_cosim` with the r4 pinned wrappers: 350 s. `[contract-1x1] 62 case run(s): 315 ok, 0 bad`, `[contract-8x8] 27 case run(s): 150 ok, 0 bad`, `39 of 39 mutant(s) killed by their named check`, `465 checks: 465 PASS, 0 FAIL`, `RESULT: PASS`.
  - All 207 case-run stdouts equal the scratch probe's, apart from the host buffer address.
  - The handoff names every case and every mutant with its killing check.
- Restart cases:
  - **W1 (1x1).** The writer restarts with `hb` 12 at 2,830 ms and reaches `hb` 24 with `backed=1` at 5,830 ms, 3 s later and past the 2,000 ms deadline; seq 2 commits. The only heartbeat write (`:936`) sits behind `if (!nvm_started) return;` (`:926-927`), and the model zeroes that flag. So `nvm_boot()` re-armed it (`:1449`). F08 is killed by `converged@end`.
  - **W2, W3 and W4 (1x1 and 8x8).** They restart a writer that no load admitted. It stays retired with `hb` 0, as the cases require. F11 and R06 are killed.
- Full builder bank, compiler present (`EXCEPT 1 NOT RUN`, gate 11) and compilers absent (`EXCEPT 2 NOT RUN`), including dev's gate 36b and timing-grade checks.
- Host self-test, `check_nvm_capture`, the round-3 kept capture oracles, `fw_service_budget/run.py --self-test` and `ci_scope --selftest`.
- Docs gates under the pinned Markdown environment (`check_em_dash --base b5c0f69d`: 0 findings over 555 added lines), source checks and `git diff --check b5c0f69d`.
  - The logs of all 20 gates and all seven probe and link-guard logs are byte-identical to the `d0203aac` run.
- Reviewer probes, graded 0.
  - A first probe run failed `phase-probe` at the host link because it reused the previous session's scratch work directory: the probe's own `generated/csr.h` shadowed the stub. In a fresh directory all five pass, byte-identical to before.
  - The failed run's receipt and log are kept.
- **Native service and capture re-run**, because dev's #602 RTL, the processor re-pin and `milan_soc.py` move bound inputs.
  - 25 arms and 65 commands, all rc 0 at `4c2a30de`. All 15 service runs regrade from the retained bytes.
  - All 16 service logs, nine capture logs and eight measurement JSONs are byte-identical to the previous merge head's, and so to round 3's. Every graded field is identical, and every capture identity equals the committed receipt.
  - Moved build hashes: only dev's changed inputs, plus generated files that differ only in LiteX timestamps and DWARF. `bios.bin` is identical.
  - Every bound input equals dev parent `b5c0f69d`'s copy except this PR's own files.

**Acceptance criteria (assignment).** Met:
- item 1: one conflict, both rows kept, clean merges checked;
- item 2: one-line restart-model commit; the full suite passes with the restart cases reported;
- item 3: search reported, nothing falsified by this PR;
- item 4: comparison baseline `b5c0f69d`;
- item 5: pinned Markdown environment.

The round-3 figures stand unchanged.

**Open points** (no edit made):
- `397_SERVICE_BUDGET.md:37-38` and `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1616` still name measured commit `26a26e1f` and processor pin `16be6768` as provenance. The re-run at `c951a9ff` reproduces them byte for byte.
- `tb/verilator/README.md:71` says `nvm_cosim` grades "469 checks over 90 case runs". The suite grades 465 over 89. That was stale on dev since `26482899`, not from this PR, so it needs its own issue.
- `origin/dev` has moved to `eaa88a32` (PR #615), fetched outside this session. `git merge-tree` with this head is clean; no merge was made.

Review requested: [R368] delta review of `9f94b246`, `d0203aac` and `4c2a30de`, then the candidate, composition review, act and merge named in the assignment.
