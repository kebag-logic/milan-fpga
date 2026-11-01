[R760] POSITIVE - exact head fa01979959ebff05af34f5a752408de7b3c41cf1

Round R760-2, issue #665, PR #830. Tree `275c59ba1c6ab453df580bec48f52fbc2f1b47dd`. Delta reviewed: `9f81df00..fa019799`, 3 commits, 4 files (`sw/mailbox/census_ports.py`, `sw/mailbox/mailbox.yaml` and two harness READMEs). No RTL, firmware source or test code changed.

No BLOCKER, MAJOR or MINOR is open. Every restated boot figure and every cell of the new window table was reproduced by this round's own runs at this head and at the no-stage control, and the refusal also at `5b5f4336`. The author's refusal reason holds. Two RESIDUE items and two SUGGESTIONs follow.

## Clean lenses

[R760] PASS Conformance - `tb/verilator/ctrl_split_boot/README.md:78-87`, `tb/verilator/ctrl_service_budget/README.md:822-823,837-860`, `receipts/readme-cells.txt`, `receipts/windows-*.txt` - R759-1 F1 and F2's required outcomes against 12 own window runs and 4 own boots; the 20 s and 500 ms bound statements still hold on the new figures; no clause claim moved

[R760] PASS RTL - `receipts/delta-stat.txt` (the diff touches no `hdl/`, `sw/firmware` or `sw/litex` file), `hdl/milan/mailbox/KL_mbx_evt.sv:162,383-384` - no RTL in the delta, so R760-1's verdict at `9f81df00` stands; the coalescing the README describes was read in the source and matches the measured commit gaps

[R760] PASS Robustness - `receipts/windows-head.txt`, `windows-nostage.txt`, `windows-base.txt`, `receipts/ring-at-open.txt`, `tb/verilator/ctrl_service_budget/grade.py:611-661` - the refused-window path: ring occupancy at open, the GM shortfall and `check_load`'s refusal at each stage setting and at the base; the sync causes no new refusal

[R760] PASS Tests - `receipts/boot-summary.txt`, `receipts/refusals-*.txt`, `receipts/arm-*.rc`, published `author-r2/evidence/census.log` against `reviews/R759-1/receipts/census.log` - no test changed; 4 own boots rc 0; 3 own window arms rc 1 as `run.py` reports refusals; census output identical to `9f81df00` apart from its timing lines, so the reason-string edit moved nothing

[R760] PASS Docs - both READMEs at the head, `receipts/docs-check.log`, `receipts/gen-check.log`, the live PR body - `docs_check` 0 findings; `gen_mailbox.py --check --crosscheck` 0 findings; the delta's prose read against the runs; two RESIDUE items below

Coverage is clean under the owner's rule: RESIDUE does not leave a lens unclean, and a SUGGESTION does not affect coverage.

## Focus items

**(1) R759-1 F1, resolved.** I ran all four boots from a tree exported at this head, and from the same tree with the author's one-call `nostage.diff` applied.

| Run | Boot to ready | CPU cycles | `milan_status` | `milan_gettime` (worst) | rc |
|---|---:|---:|---|---|---:|
| 1x1, staged | 84.393 ms | 4,219,673 | 21.530 / 1.962 / 1.265 | 2.524 / 1.238 / 1.267 | 0 |
| 1x1, none | 84.383 ms | 4,219,150 | 21.531 / 1.962 / 1.265 | 2.523 / 1.238 / 1.265 | 0 |
| 8x8, staged | 184.658 ms | 9,232,883 | 40.200 / 2.855 / 2.206 | 4.051 / 2.131 / 1.857 | 0 |
| 8x8, none | 184.647 ms | 9,232,360 | 40.197 / 2.855 / 2.205 | 4.051 / 2.131 / 1.857 | 0 |

- Every README cell equals my runs, with 0 mismatches (`receipts/readme-cells.txt`). The NATIVE, BOOT, TRACE and UART lines equal the author's published logs.
- The no-stage rows equal the old table at `9f81df00` cell for cell (`receipts/old-rows-vs-none.txt`).
- The derived claims hold: 523 CPU cycles at each shape, about 0.01 ms, and no UART figure moved by more than 0.003 ms (40.197 to 40.200).
- `boot_soc.py:86` and `split_soc.py:359` confirm the stage reaches this SoC, as `README.md:45` and `:74` now say.

**(2) R759-1 F2, resolved, and the refusal reason is right.** I ran the four backlog windows at the 1x1, 4 KiB flash point in three trees, and read the logs with each tree's own `grade.py` using my own script (`scripts/windows_probe.py`).

| Window | Head, staged: GM, ring at open, longest pass | Head, no stage | `5b5f4336` |
|---|---|---|---|
| `backlog` | 15, 1, 87.169 ms | 15, 1, 86.539 ms | 15, 1, 86.539 ms |
| `backlog-owed` | 15, 0, 86.888 ms | 15, 1, 86.256 ms | 15, 1, 86.256 ms |
| `backlog-adp` | 12, 5, 81.402 ms, refused | 13, 4, 78.112 ms, refused | 13, 4, 78.112 ms, refused |
| `backlog-adp-refill` | 12, 5, 88.317 ms, refused | 13, 4, 84.977 ms, refused | 13, 4, 84.977 ms, refused |

- All eight rows of the README's new table equal my runs, including window lengths, passes and unreleased records. Both cells at `:822-823` carry the partial label. My head and no-stage runs agree with the author's `windows4.log`.
- "8 bus cycles apart, 11 post at once, 12 without the stage, then one more": the measured gaps are ten 8s then 30,188 staged, and eleven 8s then 324,708 with no stage. That is 11 + 1 and 12 + 1 records. `KL_mbx_evt.sv:383-384` holds one pending bit per interface, so the later pulses coalesce into that one record.
- The refusal is not the stage's: the refusal text at `5b5f4336` reads `'GM': 13` for both windows, and that claim had no public receipt until this round (`receipts/refusals-base.txt`). The records held at open are TICK and TIMER events behind a pass of about 72 ms, which is firmware running from flash (`receipts/ring-at-open.txt`).
- The sync did not make it worse in kind. The same two windows are refused at each setting. The base and the no-stage head match on GM, ring occupancy, passes, longest pass and unreleased records in all four windows. The stage adds one record at open and takes one GM event, 13 to 12. That row's refused-probe count falls from 6 to 5. This is not a merge defect, and R760-2-R1 records the one wording consequence.

**(3) No third stale figure.** `git grep` finds `add_devices` called only at `split_soc.py:469` and `boot_soc.py:86`.
- The figures that changed appear only in the two READMEs.
- The staged rows at `:824`, `:826` and `:828` equal the author's `arm-rows.log`. The no-stage rows at `:825`, `:827` and `:829` are unchanged by the delta.
- No other arm's table is partial: each of the others, staged and no-stage, says "over the 4 backlog windows" (`receipts/staged-composed-lines.txt`, `receipts/nostage-composed-lines.txt`), so the two labelled cells are the only partial ones.
- The controls at `:1056` and the `as-built` control match the published logs, which were not re-run here.

**(4) Residue applied.** No ten-digit ID remains on an added source line of the delta. `census_ports.py:59` and `:302`, and `mailbox.yaml:84`, now cite the issue. Generated outputs are unchanged: `gen_mailbox.py --check --crosscheck` reports 0 findings on my run, no generated file is in the diff, and the published census log matches `9f81df00` apart from timings. The other IDs in those two files predate the delta and are tracked by #746. `reboot_ctrl/mutants.py:113` carries one too, and it comes from dev `1f29f189`, so it is also existing. `MAILBOX_SPLIT.md:1161,1659` cite a comment ID in a design document, outside the delta and outside the source-comment rule.

**(5) Round-1 residue and PR body.** See the table below. The live PR body equals the published `PR-BODY.md` apart from a trailing newline, and its figures and return codes match the `.rc` receipts. One overstatement remains in Status (R760-2-R2).

## Prior findings

| Finding | State at this head |
|---|---|
| R759-1 F1 (MINOR) | Resolved; focus item 1 |
| R759-1 F2 (MINOR) | Resolved; focus item 2 |
| R759-1 RES-1, R760-1-R1 | Resolved; focus item 4 |
| R759-1 RES-2, R760-1-R2 | Resolved; "Not yet pushed" is gone from the body |
| R760-1-R3 | Resolved; the generator's two commands are listed apart |
| R760-1-R4 | Resolved; the cells say `refused`, which is more accurate than the `not run` I proposed |
| R760-1-R5 | Resolved; `README.md:45`, the Results rows, and a correction in the round-2 handoff |
| R759-1 S1 to S3, R760-1-S1 to S4 | Retained as suggestions, unchanged, with no effect on coverage |

## Findings

No BLOCKER, MAJOR or MINOR.

### R760-2-R1 - RESIDUE - Docs
- **Where:** `tb/verilator/ctrl_service_budget/README.md:843`.
- **Evidence:** "The firmware, not the stage, makes the ring that full". The sentence before it gives 5 records staged and 4 without, and `receipts/windows-*.txt` confirms that, so one of the staged row's 5 follows from the stage. The conclusion that the refusal is the firmware's is right, and no figure changes.
- **Impact:** wording only.
- **Exact fix:** replace the sentence's opening clause with "The firmware, not the stage, is why both windows are refused; the stage adds one record to the ring and takes one GM event from the window:", and keep the rest of the line.
- **Verification:** read the line against `receipts/windows-base.txt` and `windows-head.txt`.

### R760-2-R2 - RESIDUE - Docs
- **Where:** live PR body, Status.
- **Evidence:** "every gate this round touches exits 0 on the head". The same body's results table gives rc 1 on the budget arms with refused probes, and its validation text expects rc 1 on the last command.
- **Impact:** wording only. The results table is correct.
- **Exact fix:** append ", but for the budget harness arms that report refused probes, rc 1 as the table below states".
- **Verification:** read Status against the `budget-*.rc` receipts.

### R760-2-S1 - SUGGESTION - Tests, Docs
- **Where:** `tb/verilator/ctrl_service_budget/grade.py` and the `table.md` it writes; the author's open risk.
- **Evidence:** a refused window is worded "not run", though it ran, and `results.json` does not carry its figures. The README now explains this for two rows by hand, and no Issue exists.
- **Outcome:** file an Issue so the table says "refused" and carries the refused window's figures. Then the README's table regenerates from the harness. That is new work, so it does not belong in this sync.

### R760-2-S2 - SUGGESTION - Docs
- **Where:** published `author-r2` packet.
- **Evidence:** `windows4.log` and `verify-cells.log` are published, but the handoff's `bin/windows4.py` and `verify_cells.py` are not. I reproduced both results with my own scripts, so nothing rests on them.
- **Outcome:** include such scripts in later packets, so a cold reviewer can rerun the author's exact check.

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Both README figure sets against own runs, F1 and F2 outcomes, bound statements | R760-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| RTL | CLEAN | Delta names (no `hdl/`), `KL_mbx_evt.sv` coalescing against measured gaps; the wider RTL verdict rests on R760-1 at `9f81df00`, which nothing in this lens's scope has touched since | R760-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| Robustness | CLEAN | Refused-window paths at staged, no-stage and base, `grade.check_load`, ring contents at open | R760-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| Tests | CLEAN, one SUGGESTION on record | 4 boots, 3 window arms, published census log compared with `9f81df00`'s, no test code in the delta | R760-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| Docs | CLEAN, two RESIDUE, two SUGGESTIONs on record | Both READMEs, `docs_check`, generator check, live PR body, `census_ports.py` and `mailbox.yaml` citations | R760-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |

## Commands run by this round

Run from disposable trees exported at each commit, with the pinned submodule revisions. Set `PACKET`, `LITEX_VENV`, `SDK_BIN`, `VERILATOR_DIR` and `SV2V_DIR` first; `scripts/env.sh` applies them.

```sh
scripts/run_arm.sh TREE OUT      # at this head, at this head with nostage.diff, and at 5b5f4336: rc 1 each, as run.py reports refusals
scripts/windows_probe.py TREE OUT/results
scripts/ring_at_open.py TREE OUT/results
scripts/run_boot.sh TREE OUT [--shape endstation_ax7101_8x8]    # at this head and with nostage.diff, both shapes: rc 0 each
scripts/readme_cells.py TREE BOOTDIR receipts/windows-head.txt receipts/windows-nostage.txt    # 0 mismatches
python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck    # 0 findings
python3 -B scripts/docs_check.py    # 0 findings
git diff --check 9f81df00 fa019799    # no finding
```

Tools: pinned Verilator 5.050 (identity checked), the RV32 SDK whose archive digest equals `ARCHIVE_SHA256` in `scripts/ci_rv32_sdk.py`, the product LiteX environment at CPython 3.14.8 (`receipts/tool-identity.txt`). The review clone was left at exact head: tree, index, modes and the five required gitlinks verified, no untracked or ignored file remaining (`receipts/clone-restored.txt`).

## Real limits

- **Packet integrity:** all 94 `author-r2` files match `MANIFEST.json`'s `published_sha256` (`receipts/author-r2-manifest-check.txt`). 3 of them differ from the packet's `SHA256SUMS` because of path redaction, which the manifest records for those files. The evidence commit `a60f9d23` is not cryptographically signed, so I checked it by digest and by reproduction, not by signature.
- **Budget arms:** I ran only the four backlog windows at 1x1, 4 KiB. The refused-probe rows, the other arms and the controls were checked against the author's published receipts and were not re-run. R759-1 ran the staged 1x1, 4 KiB arm in full at `9f81df00`.
- **Not re-run, as assigned:** the census and self-test, firmware banks, LiteX simulations, BDD, the native sweep, the builder legs and the full docs workflow. These rest on the author's receipts. Round 2 changes nothing they depend on but a comment and a reason string.
- **Reason string:** I did not re-run the census. Its identical output is read from the author's published log, against R759-1's log at `9f81df00`.
- **Hosted evidence, when read:** 53 contexts on this head, 28 passed, 24 still pending and 1 skipped (`Physical gPTP (nightly and manual)`), with none failing (`receipts/hosted-checks.txt`). `Verilator`, `Yosys` shards and `docs-check` were among the pending. I did not read their logs. A skipped context is not hardware proof, and acceptance is the manager's.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **No source bank at this head:** this review neither claims nor infers a manager source bank.

## Pending manager duties

- Hosted and local-replica acceptance on this exact head, including the contexts still pending above.
- The current-dev merge candidate against dev `1f29f189279f9fc0132f4918e47342b87d22f33a` (builder and native banks), with its receipts linked on the PR.
- Carry R760-2-R1 and R760-2-R2 to the residue checklist.
- The second independent verdict at this head, the completion ledger, maintainer merge authorization, and post-merge containment.

R760-2 FINISHED
