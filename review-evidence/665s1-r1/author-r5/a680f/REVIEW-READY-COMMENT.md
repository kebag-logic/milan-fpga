[A680f] REVIEW READY
Commit: `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44` (three commits on `4e3aab32`, nothing pushed)

Changed (only what ruling 6425357821 asks):
1. **The ledgered point plans 57.5.**
   - `sw/litex/ctrl_memory.py:205` `LEDGERED["8x8-two-interfaces"]` is now 57.5, owed to S14 under rulings 6412739248 and 6425357821. The override still recognises only that image, and every SoC build is still held to 56.
   - `sw/litex/test_ctrl_memory.py` plans that image at 57.5 by name. It refuses that image without the override, through `add_ctrl_memory`, and at 58.0. It refuses the override on every other point at 57.5, and within budget.
   - Three plants, each caught by named failures, with a passing control: 57.5 -> 57.0, 57.5 -> 58.0, and the override applied to any image.
   - `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 has this head's figures at all four points. It records the 1,056 B of `rom` and 224 B of `sram` the round-5 model adds at every point (against `989c9f53`), and what they are. It records the two compactions, -64 B each, which leave 119,608 B, still 57.5. Sections 3 and 6 now give the override's figure as 57.5.
2. **Risk 1, by name.** `docs/design/MAILBOX_SPLIT.md:1285` "The firmware's writer" now opens with "The undone value after a failed change". The datapath ends at the values in force, which is R701-4's outcome (a). It holds the undone value from the late acknowledgement until it takes the republished block. This ruling accepts that for the faces' lane, and closing it belongs to the placement switch. The PR body's limits say the same.
3. **The three probe fixtures** are in the PR body: R701-4's and R702-4's expect ENTITY_MISBEHAVING as the first frame, and R702-3's expects SUCCESS. Each now gets IN_PROGRESS by item 1 of ruling 6421238472. R702-3's final frame is ENTITY_MISBEHAVING, because it withholds the acknowledgement past the bound (item 2). Each probe's own assertion holds. The probes are not edited.

Validation at `6d2b77bb`, all rc 0:
- `test_ctrl_memory.py`: 0 failures.
- Linked images: 1x1 one interface 37.0, two interfaces 40.5, and 8x8 one interface 50.5, all within 56. 8x8 two interfaces is 57.5 with `--ledgered-point` and refused without it (rc 2). The override is refused on the other three points (rc 2). The ELFs are byte-identical to those at `9e370841`.
- The docs gates: 69 of 69.
- `cd tests && behave`: 406 scenarios.

Nothing under `hdl/`, `tb/`, `sw/firmware/`, `sw/mailbox/` or `tests/` changed, and no generated file. So `4e3aab32`'s receipts stand for everything else: the firmware self-test, the AECP campaign (128 of 128), coverage, the boundary, the mailbox bench, the census, and the sweep (64 of 64).

Acceptance criteria: met as in round 4. The ledgered point is within its ruled 57.5, and every other point is within 56. This PR relates to #665 and does not close it.

Open risks/questions:
- The ledgered point has 1,096 B of `rom` left before 58.0.
- The stray blank line at `aecp_commands.c:56` is left, to avoid re-running the firmware gates for whitespace.
