[A430] STOP
Branch: `590-592-599-firmware` at `d0203aac9724653ea0fb4a61d28ad2e42e515e74` (tree `73d39ccd`). Local only, not pushed.

**Merge.**
- `9f94b246` merges dev `b5c0f69d` into `1f039cfe`. The subject is one line, with no body and no trailer.
- The processor gitlink is dev's `c951a9ff`, and the submodule is checked out at it.
- Each parent diff carries exactly the other lane's changed lines: dev's delta, 51 files, +2176/-413, and this PR's delta, 28 files, +2886/-648.

**Conflict.** Only `docs/findings/README.md`. Dev's `COMMERCIAL_TIMING_395.md` row stays at dev's position, followed by this PR's `397_SERVICE_BUDGET.md` row. No row is duplicated.

**Clean merges.**
- `BAREMETAL_FIRMWARE.md`, `MILAN_COMPLIANCE_MATRIX.md` and `REGISTER_MAP.md`: dev's #602 rows cover PHC-only re-base, `mr` and MEDIA_RESET. This PR's rows cover the dispatch hook, the capture copy and MDIO link publication. No row describes the other lane's mechanism.
- `test_builder.py`: the hunks are disjoint. Dev adds gate 36b and the timing-grade checks; this PR adds no gate.

**Restart model.** `d0203aac` adds `"nvm_started": "0"` to `WRITER_STATICS`. It is a one-line diff, and no other test or firmware change was made. The refusal at `run_cases.py:199` is gone. The generated restart body now sets `nvm_started = 0;`, then calls `set_idle_hook(0); nvm_boot();`.

**STOP reason: the full `nvm_cosim` suite still fails, one step later.**
- `make -C tb/verilator/nvm_cosim` returns rc 2 after 16 s. It used the pinned wrappers of the manager's r4 bank: Verilator 5.050 and the pinned Markdown environment's Python.
- Every build that reached the link fails on one symbol, `undefined reference to 'bios_dispatch_hook_required'`, from `nvm_boot()` (`milan_baremetal.c:1444`). Those builds are `contract-1x1`, `contract-8x8`, `idw2-1x1`, `mut-A01` and `mut-F01`.
- Round-3 commit `26a26e1f` added both `nvm_started` and the patch-0006 marker call. `93262f25` stubbed the marker in the builder's gate-35 fixture, and `sw/firmware/nvm_hosttest/nvm_host.c:67-72` has it. `tb/verilator/nvm_cosim/cosim_host.c` does not.
- At `1f039cfe` the statics refusal runs before any build and hid this failure. So the failure predates the merge.
- The ruling allows no other test change, so I stopped.

**Probe (a scratch copy outside the checkout; not a gate, and the branch was not touched).**
- The harness copy adds only a declaration and an empty `bios_dispatch_hook_required()` definition to `cosim_host.c`, mirroring `nvm_host.c:67-72`.
- The same full suite returns rc 0 in 344 s. Checks: 1x1 has 62 case runs with 315 ok, and 8x8 has 27 case runs with 150 ok. In total, 465 of 465 checks pass and 39 of 39 mutants are killed by their named check.
- Restart cases:
  - **W1 re-attaches (1x1).** The writer restarts at 2,830 ms with 12 heartbeats. By 5,830 ms it has 24, `backed=1` holds past the 2,000 ms deadline, and seq 2 commits.
  - This proves `nvm_boot()` re-arms `nvm_started` (`:1449`). The only heartbeat write (`:936`) sits behind `if (!nvm_started) return;` (`:926-927`), and the restart zeroes that flag.
  - **W2, W3 and W4 (1x1 and 8x8)** restart a writer that no load admitted. It stays retired, with `hb` 0 throughout, as the cases require.
  - F08 (W1), F11 and R06 (W2) are killed.

**Other gates at `d0203aac`: all rc 0.**
- Full builder bank, compiler present: 958 s, `EXCEPT 1 NOT RUN` (gate 11). Dev's gate 36b, timing-grade and clock-contract checks pass.
- Full builder bank, compilers absent: 680 s, `EXCEPT 2 NOT RUN`.
- Host self-test, `check_nvm_capture`, the round-3 kept capture oracles, `run.py --self-test` and CI scope. Their logs are byte-identical to the previous round's.
- Docs gates with the pinned Markdown environment. `check_em_dash --base b5c0f69d` finds 0 findings over 555 added lines.
- Source checks and `git diff --check b5c0f69d`.
- Reviewer probes, graded 0. All five logs are byte-identical to the previous round's.

**Stale statements.** None found, so no commit was made. The searches are in the handoff.

**Not run: the native service and capture re-run** (about 2 h). It stops at this STOP. The service harness binds no `nvm_cosim` file (`fw_service_budget/run.py:158-179`), so a `cosim_host.c` stub would not make it stale.

**Decision needed:**
- (a) Allow one more one-line-subject commit that adds the marker stub to `tb/verilator/nvm_cosim/cosim_host.c`, the probe's exact six lines. Then run the full suite, the native re-run and the gates at that head.
- (b) Another disposition.

Recommendation: (a). It is the fixture change round 3 made for the other two hosts, and the probe shows it is the only remaining barrier.
