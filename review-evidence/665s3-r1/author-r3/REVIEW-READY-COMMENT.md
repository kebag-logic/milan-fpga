[A697d] REVIEW READY
Commit: ac105b158bb740a65e0154305377fd4a7d0f6f87
Branch: `665-s3-platform` (PR #811, base `dev-soft-core` `f4c9ad4f`); six commits on `99de3a02`, no rebase.

Changed (round 3, [A10] issuecomment-6508869822):
- R734-1-F1 (MAJOR): `tb/verilator/ctrl_split_boot/run.py` saves the native model's exit status beside its log (`sim.status`). The new NATIVE check fails on a nonzero or missing saved status, and on a tally that failed, is missing or measured nothing, read with `scripts/suite_tally.py`. A regrade reads the same saved status. Six native controls run with no build (`--native-controls`, and first in `--self-test`): a stand-in prints a valid boot's observations, then passes, exits 1, fails its tally, stops before its tally, does both, or loses its saved status before the regrade. Each is graded as required on its run and on its regrade, and R734-1's probe now ends `DEFECT REJECTED`. The check exposed that the console plant spun before all three commands (about 2.1 s), so its run passed the 2 s limit and the model failed, which the old driver could not see. The plant now spins only before `milan_status`'s response, and a plant counts as caught only in a run the model completes.
- R733-1-F1 (MINOR): `ctrl_plat_console.c` `is()` stops at the command's terminator. K3 sends `milan_status\0XYZ\r` and `milan_gettime\0\r`. The `plat` arm runs `test_plat` under AddressSanitizer (`abort_on_error=1`). The shipped defect `plat-command-read-past-its-end` (the fix reverted) is caught by K3, `crashed on signal 6`, with `global-buffer-overflow ... in is`. With the sanitizer withheld, the same defect escapes (0 checks fail).
- R733-1-F2 (MINOR): B1 records each flash access against the mailbox's and requires the saved state read before the mailbox's first access. The new B10 binds sink 0 with a BIND_RX_COMMAND through the mailbox after ready, and requires the store's service on the loop's tick to commit it to the flash. The reviewer's two plants are shipped defects: `plat-saved-state-after-mailbox-open` is caught by B1, and `plat-store-service-unbound` by B10.
- R734-1-R1: the new comments carry #665 and its decision IDs only, with no lane labels, comment IDs or ruling numbers; executable strings are unchanged. R-2: the boot README's "longer than any span here" is removed.
- Figures at this head: the platform's `rom` is 8 B larger at every point (the console's compare), and the tiles are unchanged at 39.0 / 42.0 / 52.0 / 59.0. The boot is ready at 84.383 ms / 4,219,150 CPU cycles (1x1) and 184.647 ms / 9,232,360 (8x8), simulated time with the split CPU at 50 MHz and the bus at 100 MHz. The console's coverage, 119/119 lines and 68/68 branches, is written by `fw_coverage.py --write`.

Validation at `ac105b15`, each gate in a fresh clone as its own memory-capped unit, the tree clean after each, all rc 0:
- the firmware self-test, four shards: PASS. The control campaign catches 568 of 568, the 40 platform defects among them; AECP 137; SRP 278 plus the 2 lwSRP pin controls.
- `fw_coverage.py --selftest` and `--check`: PASS (35 files).
- `test_ctrl_memory.py`: `RESULT: PASS`.
- `ctrl_plat_image.py` and the fixture at four points: 39.0 / 42.0 / 52.0 / 59.0 and 37.0 / 40.5 / 50.5 / 57.5. The six refusals exit 2 as wanted, and every ELF is byte-identical to `6987b8d8`'s, where section 5's by-part figures were measured.
- The split boot: `ctrl_split_boot: PASS (0 finding(s))` at 1x1 and at 8x8, each with NATIVE exit status 0 and a regrade that equals it. `--native-controls`: 6 of 6. `--self-test`: 6 of 6 native controls and 2 of 2 plants, each in a completed run.
- the CPU budget harness at both points, at the product clock (CPU 50 MHz, bus 100 MHz): rc 0. At 1x1, 18 groups are graded with 13 of 81 paths missing T_svc; at 8x8, 17 groups with 30 of 129. Both equal `5edbba1d`, and no group refused.
- `test_builder.py --require-rv32`: ALL GATES PASS EXCEPT 1 NOT RUN, gate 11, as at the base.
- `ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS, 0 findings.
- 97 docs, scope, idiom and harness gates, with rtl-fast's bdd-conformance: 0 nonzero. `behave` runs 14 features, 406 scenarios and 1977 steps.
- The lane's own checks: six planted defects of the NATIVE check itself are each caught by a native control. The reviewer's NUL probe is clean on the fix and reports `global-buffer-overflow` on the revert.

Acceptance criteria: met as in the PR body, under the ruled limits (graders' split mode owed to S12, SRP live configuration deferred, the split boot a recipe until #784 step 2, the 8x8 two-interface image ledgered at 59.0).
Open risks/questions: none new. R733-1's R-4 wording and suggestions S-1 to S-3 are not changed. No RTL changed, so neither the full sweep nor a route ran. Hosted and act acceptance, the current-dev merge candidate and re-review remain the manager's.
