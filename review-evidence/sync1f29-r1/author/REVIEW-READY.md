[A723c] REVIEW READY

Commit: `9f81df0054ecf35507f1b920a7f4b5a9c6f0d8b1` on `sync-dev-1f29f189-into-dev-soft-core`, over the merge commit `97e9a3d3` (parents dev-soft-core `5b5f4336`, dev `1f29f189`). Local only: nothing is pushed and no PR is open. Both tips were unchanged when the gates finished.

Changed, one commit each after the merge:
- `5d22d4fb` The port census, ruling (C). `src_stream_id_o` is class C. `reboot_req_o` is class G, with its cone stopped at `reboot_ctrl.reboot_req_i`, named as a placement-switch acceptance item next to the `amr_fsm` exclusion and listed in `MAILBOX_SPLIT.md`'s open items. Its self-test arm plants a probe on the request's net, and `g-on-wire` refuses it. No REBOOT carrier is added.
- `30973ef5` The 11 living "2.3" citations of the source entries become 2.4. The dated records of the #799 measurement keep 2.3.
- `73338019` **New semantic conflict.** The CPU budget harness's own `KL_mbx` left dev's `pub_src_sid_o` unconnected, and its build refused (PINMISSING).
- `fab0be5b` **New semantic conflict.** The merged `mailbox_emit.emit_doc` is 104 lines, over Rule 12's 100, though each side alone kept within it, so the Python idiom gate failed. The face sections move to their own function; the generated outputs are unchanged.
- `dcd56703` The harness stages its LiteSPI PHY with `stage_spi_phy`. The flash-window, refill and XIP arms are re-measured, each against a no-stage control, and the "same access cost" claim and figures are corrected.
- `9f81df00` `MAILBOX_SPLIT.md`'s verification figures on the head.

Validation on that head, all rc 0:

| Gate | Result |
|---|---|
| `gen_mailbox.py --check --crosscheck --selftest` | 0 findings, 0 arms failed |
| `publication_census.py --check --selftest --jobs 5` | 6 shapes, 0 failures; 219 ports (C 26, F 28, R 34, E 6, M 14, G 111), no G cone on the wire; 139 arms, 43 rules, none unproven |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4`, k = 0 to 3 (the mutant campaigns, `ctrl_mutants.py` among them), with `fw_rv32_selftest.py` and `test_ctrl_nvm.py` | PASS each |
| `run_litex_sims.sh --selftest`, then `run_litex_sims.sh <out>` | 10 of 10; 8 of 8 |
| `ci_builder_legs.py run 0` and `run 1`, `test_builder.py --require-rv32` | rc 0 each, through `docs-gates-1` and `-2` |
| `cd tests && behave --no-capture -f plain` | 14 features, 508 scenarios |
| `docs.yml`: every `run:` step of `wire-accountability`, `docs-check-no-git`, `docs-gates-0` to `-2`, then `docs-check` over their receipts | 43 source gates exactly once |
| four native shards | 65 of 65 suites, 2,192,828 checks, 0 failures |
| `git diff --check 97aab1d0 9f81df00` | no finding |

Three runs did not pass or attest first time, and each was repeated:
- **LiteX aggregate:** the first run returned 92, because `test_soc_timing_cuts` hit the 900 s wall clock while sharing CPUs with other gates (result UNKNOWN). Re-run unchanged on its own CPUs: rc 0.
- **Native shard 1:** the first run failed `gptp_shadow`, `gptp_tables` and `mbx`, because my spec put Make 4.3 on PATH without CI's `--no-print-directory`, and those suites' scripts read `make`'s directory lines as data. I stopped it and re-ran the whole shard with the flag: 17 of 17. Shards 0, 2 and 3 passed without the flag.
- **Harness arms:** five staged builds no longer attested after `fab0be5b`, because the firmware digest covers `sw/mailbox`. They were run again on the head, and their tables are byte-identical.

Limits of this evidence:
- The docs workflow ran locally, each job in a clean clone. `apt` and `sudo install` provisioning was replaced by a presence check. `ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` did not run, because they observe a hosted run.
- Builder leg 1 reports 16 gate arms not run: 15 need LiteX, which the docs workflow does not install, and gate 11 needs a local build report. Leg 0 reports gate 1b not run.
- The LiteX simulations and the harness used the product LiteX tree at the pinned revisions on CPython 3.14.8, not CI's fresh 3.12.3 install.

Acceptance criteria: met.
- Ruling (C) and ruling (B)'s owed items are done, one commit each.
- The merged head's behaviour keeps both lines, and no REBOOT carrier is added.
- The merge itself moved no harness figure: at dev-soft-core `5b5f4336` the three arms compared give tables byte-identical to their no-stage arms.

Stage cost, measured:
- +1 to +4 CPU cycles a flash-window load (mean 266 against 263).
- +16 to +19 a 64-byte refill.
- No path verdict moves on the cacheless core. On the XIP arms verdicts move by a few paths either way: at 8x8 with 32 KiB, 80 of 128 paths miss against 75 of 129, and one more probe is refused.

Open risks/questions:
1. The REBOOT terminal is named by cell and port, like the CSR and shim terminals, not per G output, so a second G output driven into `reboot_req_i` would also stop there. The ruling did not ask for it to be narrower; a reviewer may want it.
2. Not caused by this sync: at `5b5f4336` the harness's 8x8 cacheless arm already refuses two probes (`srp.domain.if1`, `acmp.tmr_no_adp.if0`), and the 4 KiB XIP arms refuse more than the `e76a755a` table records. The harness README now states this. It may deserve its own issue; this lane posts nothing else.
