STATUS: REVIEW READY (round 5 continuation, executor [A680f]): head `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44`; every gate this round touches rc 0

# #665 lane S1 ([A680f]): round 5 continuation, ruling 6425357821

- Branch `665-s1-faces`, from `dev-soft-core` `e76a755a` (`origin` is `kebag-logic/milan-fpga`). Nothing pushed.
- Continues [A680e]'s head `4e3aab32` (STOP 6425326942) with three commits; nothing below it is rewritten.
- The ruling on that STOP: 6425357821 (option (a)). Its handoff `../665s1-a680e/HANDOFF.md` and receipts stand for
  every gate this round does not touch.
- TAKEN: #665 comment 6425377030 (text in `TAKEN-COMMENT.md`); REVIEW READY: 6425827814 (text in `REVIEW-READY-COMMENT.md`).

## Work list (ruling 6425357821)

- [x] 1. The ledgered point (8x8, two interfaces) plans 57.5: the override's figure and its test; section 5 of
  `SPLIT_CONTROL_MEMORY.md` at this head's figures at all four points, with round 5's 1,056 B / 224 B and the two
  compactions, each with its saving. Every other point within 56 (37.0, 40.5, 50.5); the ledgered point 57.5. No STOP.
- [x] 2. Risk 1 named in `MAILBOX_SPLIT.md` "The firmware's writer" and in the PR body's limits.
- [x] 3. The three probe fixtures and the reason, in the PR body (probes not edited, not rerun: firmware unchanged).
- [x] 4. Gates: `test_ctrl_memory.py`, the linked images at four points, the docs gates, `behave`: all rc 0.
- [x] PR-BODY.md, REVIEW READY.

## Changes (file:line, reason)

Commit `9e370841` (the override):
- `sw/litex/ctrl_memory.py:205-207` `LEDGERED["8x8-two-interfaces"]` plans 57.5 (was 57.0), owed to lane S14 under
  rulings 6412739248 and 6425357821; `:202-203` the comment says a tile and a half. The rule, the symbols that make an
  image that point, and the default refusal are unchanged, so every other image is still refused the override and
  every SoC build is still held to 56.
- `sw/litex/test_ctrl_memory.py:19-22` (docstring), `:195-198` the ledgered point's image is now 57.5 RAMB36
  (`BUDGET_BSS + 3 * GRANULE`; renamed `OVER_ONE` -> `LEDGER_IMAGE`, since it is no longer one tile over) and every
  other point is planted at the same 57.5; `:304-308` the refusals: that image without its override, through
  `add_ctrl_memory`, at 58.0 (half a tile past its ledger), and the override on each other point at 57.5;
  `:325-338` the ledger holds exactly 57.5 and the override plans its point at 57.5 against the 56 budget.

Commit `d795d30e` (the ledger), `docs/design/SPLIT_CONTROL_MEMORY.md`:
- `:90-97`, `:105` (section 3) and `:244` (section 6): the override's figure 57.5, its refusal at 58.0, the ruling.
- `:155-191` (section 5): the four points at this head (firmware of `4e3aab32`, byte-identical at `6d2b77bb`) against
  `e76a755a`; the face writer's 6,432 to 6,528 B of `rom` and 336 B of `sram`; the 1,056 B of `rom` and 224 B of
  `sram` the acknowledged-state model adds at every point against `989c9f53`, with what they are; only 8x8 with two
  interfaces crosses a granule (1,096 B left before 58.0; 952 B to return to 57.0); the two compactions, -64 B each,
  leaving 119,608 B, still 57.5; the rulings that ledger it to S14; the flip still needs 56 at every point.

Commit `6d2b77bb` (risk 1), `docs/design/MAILBOX_SPLIT.md:1285-1297` "The firmware's writer": the paragraph now names
"the undone value after a failed change", states that the datapath ends at the values in force (R701-4's outcome (a),
cited as PR #795, 6421229873), that ruling 6425357821 accepts the window for this lane, and that closing it needs the
datapath side, so it belongs to the placement switch (#665 F-INT PR 2).

Not changed: the stray second blank line at `sw/firmware/ctrl/aecp/aecp_commands.c:56` ([A680e]'s nit). The ruling
asks for no firmware change, and touching that file would re-open the firmware gates for whitespace.

## New checks, planted mutants, failing words

The test changes move the figure the existing checks hold; three plants show the checks bite at 57.5
(`probes/ledger_mutants.sh`, each in a disposable worktree at `6d2b77bb`, with the unmutated control passing there
first, 0 failures: `receipts/ledger-plants/control.txt`):

| Plant (`ctrl_memory.py`) | rc | Failing words (`test_ctrl_memory.py`) |
|---|---|---|
| `ledger-back-to-57`: `LEDGERED` 57.5 -> 57.0 | 1 | "the ledger holds the one ruled point, 8x8 with two interfaces at 57.5 RAMB36"; "the 8x8-two-interfaces override plans its own point's image: raised Refusal (... exceeds the 57-RAMB36 budget ledgered for ...)"; "that plan is 57.5 RAMB36 ..."; "`plan --ledgered-point 8x8-two-interfaces` accepts its point ... (exit codes [2, 2, 2, 2, 2])" |
| `ledger-at-58`: `LEDGERED` 57.5 -> 58.0 | 1 | "the ledger holds the one ruled point ... at 57.5 RAMB36"; "that plan is 57.5 RAMB36, against the 56-RAMB36 budget and its ledgered 57.5"; "the ledgered point's image half a tile past its ledgered 57.5 RAMB36: accepted, expected 'allocation over budget' rule 'budget'" |
| `override-on-any-image`: `if carried != dict(point.symbols):` -> `if False:` | 1 | "the 8x8-two-interfaces override on the {1x1, one interface / 1x1, two interfaces / 8x8, one interface / 8x8 with no image_allocation} image at 57.5 RAMB36: accepted, expected 'allocation over budget' rule 'budget'"; "... within the budget: accepted"; "`plan --ledgered-point ...` ... (exit codes [0, 0, 0, 0, 0])" |

Each plant also leaves the test's own mutant arms ungraded ("is not graded: the checks arm fails unmutated"), as
designed: the test grades a mutant only against an arm that passed unmutated.

## Gate table

Final head `6d2b77bb`. `git diff --stat 4e3aab32..HEAD`: `sw/litex/ctrl_memory.py`, `sw/litex/test_ctrl_memory.py`,
`docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/design/MAILBOX_SPLIT.md`; nothing under `hdl/`, `tb/`, `syn/`,
`sw/firmware/`, `sw/mailbox/`, `tests/` or `configs/`, and no generated file.

| Gate | Head | Result | Receipt (`receipts/`) |
|---|---|---|---|
| `sw/litex/test_ctrl_memory.py` (LiteX's interpreter, LiteX and migen on `PYTHONPATH`) | `6d2b77bb` | rc 0, 0 failures, 66 s, tree clean | `gates/test-ctrl-memory.txt` |
| the three ledger plants above, with a passing control | `6d2b77bb` (scratch worktree) | control rc 0; each plant rc 1 with named failures; 0 escaped | `ledger-plants/` |
| linked images, four points (`probes/image_points.sh ... ledgered`, the shared `-fno-stack-protector` runtime) | `6d2b77bb` | link and plan rc 0 at each: 37.0, 40.5, 50.5 within 56; 8x8 two interfaces 57.5 with `--ledgered-point` (`"ledgered_tiles": 57.5`); without it refused at 57.5 (rc 2); the override refused on the other three (rc 2) | `images/image-points.txt`, `images/*.plan*.txt` |
| image receipt: base `e76a755a`, round 4 `989c9f53`, head (`probes/image_receipt.py`) | `6d2b77bb` | +1,056 B `rom`, +224 B `sram` round 4 -> head at every point; growth all in `aecp_poll`, `aecp_command`, `aecp_rx`, `refuse`, `swap`, `aecp_keep`, `aecp_override`, `applied`, `aecp_foreign_lock`, `publish`, `aecp_note` and `image_aecp` | `images/linked-images.txt` |
| the same link at `9e370841` | `9e370841` | the four ELFs byte-identical to `6d2b77bb`'s | `images/elf-sha256.txt` |
| docs gates (`probes/docs_gates.sh`: the docs workflow's 69 commands; pinned markdown renderer and pyslang 11.0.0) | `6d2b77bb` | 69 of 69 rc 0, 257 s | `gates/docs-gates.txt` |
| `cd tests && behave --no-capture -f plain` | `6d2b77bb` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| everything else ([A680e]'s table: firmware self-test, AECP campaign 128 of 128, AECP arms, coverage, `ctrl_boundary.py`, `test_builder.py`, `make -C tb/verilator/mbx`, `gen_mailbox.py`, census, `lint_rtl.py`, the four-shard sweep 64 of 64, the probes) | `4e3aab32` | stands: none of their inputs changed. The sweep runs nothing under `sw/litex/`; `ctrl_boundary.py` runs `test_ctrl_memory.py --build-only`, which builds the reset-entry probe and plans no ledgered point | `../665s1-a680e/receipts/`; the probes and compactions this round cites are copied to `at-4e3aab32/` |

## Probe fixtures (PR body, ruling item 3)

Ruling 6421238472 item 1 makes a waiting command's first frame IN_PROGRESS (9). Three fixtures check that frame's
status against their own round's outcome: R701-4 `late_ack_notify_probe.py` expects ENTITY_MISBEHAVING (10) for
SET_CONTROL; R702-4 `delta_probes.py` expects 10 for SET_CONTROL (getter test) and SET_STREAM_INFO (notification
test); R702-3 `probe_ack.py` expects SUCCESS (0), and since it withholds the acknowledgement past `AECP_WAIT_MS` its
final frame is 10 (item 2). Every probe's own assertion holds at `4e3aab32` (`at-4e3aab32/probes/`); the firmware is
unchanged since. The probes are not edited.

## Process notes

- `test_ctrl_memory.py` in a bare scratch worktree needs `protocol-processor` and `gptp-processor` checked out
  (worktrees of each at its pin): the first plant run refused at once without `protocol-processor`, and the first
  control run failed its SoC arm without `gptp-processor`. Neither is counted.
- The plant driver's first run counted a refused run as a kill (rc 1 with no named failure); the driver now requires
  at least one `[FAIL]` line and the control to pass first.
- The scratch worktrees were removed after the plants; the work directory keeps the raw receipts.

## Receipts

`receipts/INDEX.md` is generated from the files present by `probes/collect_receipts.sh` (host paths replaced by
placeholders; files over 200 KB listed in `receipts/large-files.txt`, none). Scripts under `probes/`:
`image_points.sh` ([A680e]'s, unchanged), `image_receipt.py` (now base, round 4 and head), `ledger_mutants.sh`,
`docs_gates.sh` ([A680e]'s, unchanged), `collect_receipts.sh`.
