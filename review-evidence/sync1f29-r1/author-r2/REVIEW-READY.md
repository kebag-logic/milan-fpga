[A723d] REVIEW READY

Commit: `fa01979959ebff05af34f5a752408de7b3c41cf1` on `sync-dev-1f29f189-into-dev-soft-core`, three commits over `9f81df00`. Not pushed: PR #830 still shows `9f81df00`. Both tips unchanged: dev `1f29f189`, dev-soft-core `5b5f4336`.

Changed, one commit per finding, answering the reviews of `9f81df00` on PR #830:
- `442da911` (R759 RES-1, R760 R1): `census_ports.py` and `mailbox.yaml` cite the issue, not the comment ID. Comments and one reason string only; the generated outputs do not change.
- `cb0be3cd` (R759 F1, R760 R5): `ctrl_split_boot/README.md` restates the boot's figures. The stage does reach that SoC, through `split_soc.add_devices`; the earlier handoff's statement that it does not was wrong, and is corrected in this round's handoff. Staged: 84.393 ms at 1x1, 184.658 ms at 8x8. The no-stage control equals the old figures cell for cell at both shapes. The stage costs 523 CPU cycles at each shape, and no verdict moves.
- `fa019799` (R759 F2, R760 R4): `ctrl_service_budget/README.md` labels both 1x1, 4 KiB composed maxima partial, 2 of 4 windows, says why, and gives all four windows' figures at each stage setting. The event ring holds 5 records (4 with no stage) when `backlog-adp` and `backlog-adp-refill` open, so the coalesced grandmaster source commits 12 events (13 with no stage) against the defined 15, and the grader refuses both windows. The same refusal is at `5b5f4336`, before #814, so it is the firmware's, not the stage's. Across all four windows the longest pass is at least 88.32 ms staged, in a refused window, and at least 86.54 ms with no stage.

No third stale figure. Only these two harnesses reach `add_devices`. The README figures dated "at this head" that predated the stage were re-run and hold: `slow-adp-rx` 24.614 ms; `as-built` cause 5 on both CPUs. Every other stage-sensitive figure is dated to `e76a755a` and stated to have no stage. No other document states these figures.

Validation, all rc 0 unless noted:

| Gate | Result |
|---|---|
| `gen_mailbox.py --check --crosscheck` | 0 findings |
| `gen_mailbox.py --selftest` | 0 arms failed |
| `gen_mailbox.py --check --crosscheck --selftest` | rc 0; this form runs the self-test only |
| `publication_census.py --check --selftest --jobs 14` | 6 shapes, 246 checks, 0 failures; 219 ports; 139 arms, 43 rules, none unproven |
| `docs.yml`: every `run:` step of the gate jobs, then `docs-check` over their receipts | 43 source gates exactly once |
| `ci_builder_legs.py run 0` and `run 1`, `test_builder.py --require-rv32` | rc 0 each, through `docs-gates-1` and `-2`; 1 and 16 gate arms not run, as before |
| `git diff --check 97aab1d0 fa019799` | no finding |
| `ctrl_split_boot/run.py`, 1x1 and 8x8, staged and no-stage; `--native-controls`; `--self-test` | PASS; 6 of 6; 2 of 2 plants caught |
| `ctrl_service_budget/run.py --self-test` | 0 failures |
| `ctrl_service_budget/run.py`, the six staged arms and the 1x1, 4 KiB no-stage control | rc 0 on two arms, rc 1 on the five with refused probes, as `run.py` reports a refusal; each table byte-identical to `9f81df00`'s |
| `run.py --reuse-build --regrade` on the six staged builds, at the head | each attests, with an unchanged table |
| every restated README cell against its run | 0 mismatches |

Firmware digest: `442da911` changes `sw/mailbox`, which the budget harness's `tree:firmware` digest covers, so `--reuse-build` refuses earlier builds. That harness is what attests against the digest, so its arms were rebuilt and re-run. The harness runs started before the last two commits, which change only the two READMEs; the regrade above shows they still attest at the head.

Two `docs-check` attempts returned rc 1 before the passing one, because my local runner had not yet placed the legs' receipts and then the `needs` context. Neither was a fault in the head, and the head did not change.

Not re-run, as assigned, because no RTL or firmware source changed: the firmware shards and mutant campaign, LiteX simulations, `behave` and the native sweep. Those results are from `9f81df00`. The docs workflow ran locally, with provisioning replaced by a presence check; the three jobs that observe a hosted run did not run. No hosted run has seen this head. The harnesses used the product LiteX tree on CPython 3.14.8 at the pinned revisions. No Vivado, hardware or bench run.

Acceptance criteria: met for this round. F1, F2, RES-1, RES-2 and R760's R1 to R5 are closed. The suggestions from both rounds are left as they are.
Open risks/questions: `table.md` and `results.json` report a refused backlog window as "not run", while the README describes that word as a row the run did not include. The README now says what it means for these two rows; the grader is unchanged, and no Issue exists for it.
