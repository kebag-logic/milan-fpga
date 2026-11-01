[R759] NEGATIVE - exact head fa01979959ebff05af34f5a752408de7b3c41cf1

Round R759-2, issue #665, PR #830: round 2 delta, `9f81df00..fa019799`, 3 commits, tree `275c59ba1c6ab453df580bec48f52fbc2f1b47dd`.

One open MINOR makes this NEGATIVE: one digit in the new window table, `884.92` where the run gives `884.91`. No verdict depends on that digit. R759-1's F1, F2, RES-1 and RES-2 are all resolved, and every other figure and claim in the delta holds. Reproduction ran at the head, at the no-stage control and at `5b5f4336`.

## Findings

### F3. MINOR. Conformance, Docs. `tb/verilator/ctrl_service_budget/README.md:854`: one window length is rounded twice

- **Authority:** the owner's RESIDUE rule excludes a defect that changes a figure, and this is a figure. Focus item 2 asks for all four windows' figures, and the ruling on #665 owes corrected figures.
- **Evidence:** the staged `backlog-adp-refill` window is 88,491,464 bus cycles at 100 MHz, 884.91464 ms (`receipts/window-exact.txt`). To two places that is 884.91. The README says 884.92. The author's published log prints 884.915 (`author-r2/evidence/windows4.log`), and the table appears to round that value again. The author's `verify-cells.log` lists no cell of this table, so nothing caught it. The other 15 window and longest-pass cells in the table are correct at two places.
- **Impact:** a published figure is 0.01 ms too high in its last digit, 0.005 ms against the exact value, in a window the grader refuses. It feeds no other figure and no verdict.
- **Required outcome:** line 854's window cell reads `884.91`.
- **Verification:** compare that cell with `receipts/window-exact.txt`. No harness re-run is needed: the firmware digest does not cover the README. Only Conformance and Docs need covering again.

### RES-3. RESIDUE. `tb/verilator/ctrl_service_budget/README.md:843`: "makes the ring that full" overstates the firmware's share

- **Evidence:** at `5b5f4336` the ring holds 4 records when the two windows open, and the stage is what makes it 5 (`receipts/windows-reader.txt`). The cause given for the refusal is right, and line 840 states both numbers.
- **Exact fix:** "The firmware, not the stage, causes the refusal: at `dev-soft-core` `5b5f4336`, before dev's #814 was merged, the ring holds 4 records when those windows open and the same two are refused at 13 GM events. The stage adds the fifth record."

### RES-4. RESIDUE. `tb/verilator/ctrl_service_budget/README.md:846`: the sentence has no verb

- **Exact fix:** "This table gives every window, read from each run's logs with `grade.py`'s own `population`, `composed_passes` and `unreleased`, without its refusal."

### S4. SUGGESTION. File an Issue for the grader's "not run" wording

`table.md` and `results.json` call a refused backlog window "not run", while `README.md:216` uses those words for a row the run did not include. Line 839 now explains this for these two rows, and the author records that no Issue exists. The grader is outside this delta.

## Focus items

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | F1, split boot figures | Holds. All four rows match the published logs, read with my own filter rather than the author's checker. My round-1 runs give the same staged figures. My own 8x8 no-stage run, the control round 1 did not run, matches the published log line for line. The stage costs 523 cycles at each shape, and no UART figure moves more than 0.003 ms | `receipts/boot-8x8-nostage.log`; `author-r2/evidence/boot-*.log`; `tb/verilator/ctrl_split_boot/README.md:81-87` |
| 2 | F2, partial labels and the refusal's cause | Holds, apart from F3. Both cells are labelled partial, and all eight table rows are present. The cause is right, with the wording note in RES-3. See below | `receipts/windows-reader.txt`, `window-exact.txt`, `raw-windows/` |
| 3 | No third stale figure | Holds. `add_devices` is called only from `split_soc.py:469` and `boot_soc.py:86`. No other document states these figures: the only hits are coordinates in an unrelated SVG. The two READMEs that take the stage directly from `MilanSoC` state no flash, refill or SPI figure in ms | `receipts/third-figure-sweep.txt` |
| 4 | Residue applied, outputs unchanged | Holds. Neither named comment ID remains in `sw/`, `tb/` or `hdl/`. The IDs left in these two files match `5b5f4336`'s line counts (3 and 9), so they are existing ones under #746. The three generated files have the same blobs at both heads, and the generator check reports 0 findings at the head | `receipts/residue-check.txt`, `gen-head.log` |
| 5 | Round-1 residue and the PR body | Holds. "Not yet pushed" is gone, and I found no other stale text in the body. The live body matches the packet's `PR-BODY.md` but for one blank line. Figures and rc counts in the Round 2 section and the results tables agree with the receipts | `author-r2/PR-BODY.md`, live PR body |

**The refusal, measured three ways.** Arm: 1x1, flash code, 4 KiB cache, all four windows.

| Tree | `backlog-adp` and `-refill`: ring at open, of 16 | GM in the first burst | Next GM, bus cycles later | GM committed, of 15 | Refused |
|---|---:|---:|---:|---:|---|
| head, staged | 5 | 11 | 30,188 | 12 | both |
| head, no stage | 4 | 12 | 324,708 | 13 | both |
| `5b5f4336`, which has no stage | 4 | 12 | 324,708 | 13 | both |

- **The mechanism holds.** Burst commits are 8 bus cycles apart. The free slots take the burst, and on 1x1 the one `gm_pend_r` bit (`hdl/milan/mailbox/KL_mbx_evt.sv:109,162,383`) holds the rest as one more record. `grade.check_load` then refuses the window (`grade.py:653`).
- **The records at open are the firmware's backlog.** They are unreleased TICK and TIMER events, the oldest posted up to about 27 ms earlier (`receipts/window-exact.txt`).
- **The base equals the no-stage control.** All four windows give the same figures, and the author's `5b5f4336` table is the same blob as the no-stage table (`receipts/r2-vs-r1-table-blobs.txt`).
- **This sync did not make the refusal worse.** The same two windows are refused with and without the stage, and the probe refusals are 5 staged against 6 at the base's table. The stage moves GM from 13 to 12 and refuses nothing new. So this is recorded firmware behaviour, not a merge defect.

## Prior public findings

| Finding | Status at this head | Evidence |
|---|---|---|
| R759-1 F1, MINOR | Resolved | focus item 1 |
| R759-1 F2, MINOR | Resolved. F3 is a new defect in the table written to answer it | focus item 2 |
| R759-1 RES-1 | Resolved | focus item 4 |
| R759-1 RES-2 | Resolved | focus item 5 |
| R759-1 S1, S2, S3 | Retained as suggestions; the delta does not touch them | no RTL, census logic or harness code in the delta |
| R760-1-R1 | Resolved | focus item 4 |
| R760-1-R2 | Resolved | focus item 5 |
| R760-1-R3 | Resolved. The body lists the generator's two commands apart, each with its own result | PR body, "How to validate" |
| R760-1-R4 | Resolved. The cells say "refused" rather than the exact fix's "not run", which is more accurate | `ctrl_service_budget/README.md:822-823` |
| R760-1-R5 | Resolved. The README is restated, and the handoff corrects the earlier statement | `ctrl_split_boot/README.md:45,73-84`; `author-r2/HANDOFF.md` section 2 |
| R760-1-S1 to S4 | Retained as suggestions; the delta does not touch them | delta file list |

I read R760-1's findings only after this verdict and ledger were written. I did not read any R760-2 material.

## Clean lens results

```text
[R759] PASS RTL - `git diff --name-status 9f81df00 fa019799` (receipts/residue-check.txt), hdl/milan/mailbox/KL_mbx_evt.sv:109,162,383 - no RTL in the delta; the README's coalescing account read against the source and the measured GM commit times; R759-1's RTL verdict carries
[R759] PASS Robustness - receipts/raw-windows/, receipts/win-*.log - the refused-window path at the head, the control and the base refuses as the README says, with no new refused window; no behaviour changed in the delta; R759-1's verdict carries
[R759] PASS Tests - author-r2/evidence/census.log, control-*.log, receipts/gen-head.log, sw/mailbox/census_ports.py at the head - the delta changes no test logic, only one reason string and comments; the census's 43 rules are proven in the published log; the generator self-test reruns clean here; the harness's stage gap stays S3
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | `ctrl_service_budget/README.md:822-860`, `ctrl_split_boot/README.md:45,73-90`, grader `check_load`, the three-way window runs | R759-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| RTL | CLEAN | delta file list, `KL_mbx_evt.sv` against the README's account | R759-2; R759-1 for the unchanged RTL | `fa01979959ebff05af34f5a752408de7b3c41cf1`; RTL unchanged since `9f81df00` |
| Robustness | CLEAN | refused-window path at head, control and base; raw group logs | R759-2; R759-1 for unchanged code | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| Tests | CLEAN | census log, generator self-test, harness control logs, `census_ports.py` diff | R759-2; R759-1 for unchanged tests | `fa01979959ebff05af34f5a752408de7b3c41cf1` |
| Docs | UNCLEAN (F3) | both harness READMEs, `mailbox.yaml` and `census_ports.py` comments, PR body, stale-figure sweep | R759-2 | `fa01979959ebff05af34f5a752408de7b3c41cf1` |

RESIDUE leaves no lens unclean.

## Commands run by this round

Every run used a scratch tree; the review clone was not modified.

- `gen_mailbox.py --check --crosscheck`: rc 0, 0 findings. `--selftest`: rc 0, 0 arms failed.
- `ctrl_split_boot/run.py --shape endstation_ax7101_8x8` on the no-stage control: rc 0, PASS.
- `ctrl_service_budget/run.py --point 1x1 --xip --fetch-l1 64x1 --groups backlog,backlog-owed,backlog-adp,backlog-adp-refill --record-budget-findings`, on the head, the no-stage control and `5b5f4336`: rc 1 each, as `run.py` reports the two refused windows.
- `scripts/windows.py` and `scripts/window_exact.py` over those raw logs, using each tree's own `grade.py`.
- `scripts/verify_manifest.py` over the packet.

The review clone is unchanged at the exact head: tree, index, modes and the five submodule gitlinks verified (`receipts/clone-restored.txt`). Home-directory paths in the four run logs are replaced with `$HOME`; nothing else in them was edited.

## Real limits

- **Evidence packet:** the evidence commit `a60f9d23` is unsigned according to the hosting API, and the evidence directory holds no signature file. So I verified digests only: all 94 `author-r2` files match `MANIFEST.json`. Three receipts differ from `SHA256SUMS`, and the manifest's original digests and redaction flags account for all three.
- **Not run here, read from published receipts:** census, docs workflow, builder legs, the 8x8 budget arms and the controls. The window runs cover the four backlog groups only, not the whole 1x1, 4 KiB arm; round 1 ran that arm at `9f81df00`.
- **The 1x1 staged and 8x8 staged boots:** not re-run at this head. The figures come from the published logs and my round-1 runs at `9f81df00`; the delta changes only comments and one reason string in that firmware's inputs.
- **Hosted evidence:** in progress when last read, 20 passed, 29 pending and 1 skipped (`receipts/hosted-snapshot.txt`). Among those passed are `publication-census`, `docs-gates-1`, `docs-gates-2`, `wire-accountability` and `docs-check-no-git`. The Physical gPTP context was skipped, not executed. I accept none of this; the manager owns it. The packet's "not pushed" and "no hosted run" lines were true when written and are stale now that the head is pushed.
- **Environment:** LiteX ran from the product tree, as in round 1, and not CI's fresh interpreter. Verilator 5.050 was verified by `--version`.
- **Not done:** no Vivado, no hardware. Physical calibration NOT RUN, and field skips are not hardware proof. No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Route F3 to the executor, with RES-3 and RES-4 on the residue checklist.
- Re-review at the corrected head, covering Conformance and Docs again.
- Decide whether S4 becomes an Issue.
- Build and validate the current-dev merge candidate, accept hosted and act evidence, and hold the second positive and merge authorization.

R759-2 FINISHED
