# RESOLUTIONS: the flip train's composition, round 4 (#665)

Round 4 continues round 3's branch at `4a5bfb32`. Conventions are round 1's: one row per conflicted file; "Train" is the
branch before the step, "PR" the head merged by `git merge --no-ff`, checked against its GitHub head immediately before
the merge.

The step-9 branch `flip-train-1117` stays at step 9 and takes the cut (`ab4bc245`). The provisional step 10 is
`flip-train-1117-p10`, branched from `4a5bfb32`.

## Provisional step 10: #944 (lane 936) `7cfb8a04`; merge `5ff15cbc`, fix `9a91c39b`

#944's review head, not frozen: #936's round 2 is still running. Merge base `70f4056f`; #944 changes 22 files in 9
commits, and 9 of them conflicted. It moves no submodule: its gitlinks are its base's, so the merge keeps the train's
`gptp-processor` `1616fc8f` and `protocol-processor` `801ef228`. That was checked in the index before the commit, and
the resolved files were staged by path, never with `git add -A` (round 3's lesson).

| File | Train's intent | #936's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/test/test_aecp.cpp` | the AppStore restore test | `App.SrpDeclarationChangeIsItsStreamOutputsNotice` | both | independent tests |
| `tb/verilator/milan_dp/twin_compare.py` (2) | the owed row `stream-output-0-notices` (the split sent no notice at a Talker declaration's changes, #929), its words and `vanished-owed`'s | the notice sent (#936), so that row is gone; a new owed row `stream-output-0-dest-mac` (the split reads `stream_dest_mac` 0 from a MAAP engine it does not build), a plant `output-notice-dropped` | #936's rows, strings and plant; the train's other rows, at #934's identity, unchanged | the row the train owed is what #936 fixes. Every expected string was confirmed by the twin's own run at `5ff15cbc`: `make twin`, `twin-plants` (16 plants, each refused by its own words), `twin-maps` and `twin-maps-plants` all pass |
| `tb/verilator/milan_dp/Makefile` (2) | the twin-maps leg's lines (#923); `talker-failed-back`; `TWIN_FABRIC_PLANTS` empty (#893 at `801ef228`) | `output-notice-dropped` in the capture plants | both: sixteen plants | |
| `tb/verilator/milan_dp/README.md` | the train's legs and owed rows (#858, the split Talker's failed attribute) | the owed table's one row, `stream-output-0-dest-mac`, and `stream-output-0-notices` deleted | #936's owed row and its account of the deletion, with the train's history of its own rows; sixteen plants | as the code |
| `sw/litex/ctrl_memory.py` (5) | the fixture's entry 60.0, the platform's 62.5 with `ctrl_plat` 21,504 B | the fixture 59.5 and `ctrl_plat` 20,416 B on #936's base | the train's entries, restated to the composed images' measurement: the fixture's entry **60.5** (its `answering-ports` arm needs 131,216 B of `rom`, 144 B past the 131,072 B that 60.0 holds), ROM debt owed to S14 under #665's ruling of 2026-11-17 as amended (issuecomment-6959600243: "a fixture at 60.5 is S14 debt"); the platform's `ctrl_plat` 21,568 B, its `rom` 138,816 B within its 62.5 | an entry is its image's measured tiles (the owner's rule of 2026-11-15, #923's ruling) |
| `sw/litex/ctrl_memory_ledger.py` (6) | `PLAT_*` 17,984 / 19,712 / 18,944 / 21,504; the fixture at 60.0 | 17,536 / 19,136 / 18,240 / 20,416; 59.5 | measured: 18,048 / 19,712 / 18,944 / 21,568; the fixture at 60.5, its refusal cases half a tile past, at 61.0 | `plat_ledger.py` reads each image's own `ctrl_plat`: on the composed train, #936's 64 B take the 1x1 one-interface and the 8x8 two-interface points, not its base's 1x1 two-interface one |
| `sw/litex/test_ctrl_memory.py` (2) | 60.0 | 59.5 | 60.5 | as the ledger |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (6) | the composed train's ledger rows and fit tables | the "At #936's head" fit table | the train's text with #936's table kept as its head's; the ledger table and the composed train's entries restated (the fixture 60.5, `ctrl_plat` 21,568 B, refused at 61.0, 63.0 and 58.0); a step-10 fit table, marked provisional (the final head's cut and hot list move every image's `rom`) | as the code |
| `tb/verilator/ctrl_service_budget/README.md` (2) | the fixture's planner entry at 59.5 (stale since #923 composed) | 59.5 since #936 | 60.5, with its history | as the ledger |

`docs/design/MARK_II_AREA_PLAN.md` merged without conflict, but its #936 sentence said 59.5. It is restated in the merge
to the composed 60.5, keeping #936's 59.5 as its head's.

**Fix `9a91c39b`**: the union put `sw/firmware/ctrl/test/aecp_mutants.py` at 1,009 lines (#936 brought it to 1,000,
the train's 22 more), past the idiom gate's 1,000 with its long-module ratchet full (11 > 10). #936's four
STREAM_OUTPUT notice mutants (`app-output-notice-*`), contiguous in the table, move to `aecp_notice_mutants.py`,
spliced back in place as `aecp_stream_info_mutants.py`'s are: the table is the same 365 defects in the same order,
each row identical (compared by import). `aecp_mutants.py` is 989 lines and `py_idiom` passes.

**Checks at step 10** (`5ff15cbc`; the fix `9a91c39b` touches only the AECP campaign's Python, its table identical):

- the four firmware shards PASS (receipts/step10/firmware/), the control campaign 797 of 797;
- the harness self-tests: `run.py --self-test` 0 failures, `rows_tiers`, `record_classes`, the load gate and its
  self-test, the flip self-test, `shape_costs`, `egress_ledger`, `mailbox_margins`; `flip_check` at 1x1/1if PASS,
  and at all points the base's same eleven 8x8/2if findings;
- `py_idiom` failed on `aecp_mutants.py` (fixed at `9a91c39b`, PASS); the docs, hygiene and C++ gates,
  `fw_coverage --check` and `test_ctrl_memory` PASS;
- the two-placement simulation: `twin`, `twin-plants` (16 plants, each refused by its own words), `twin-maps` and
  `twin-maps-plants` PASS (receipts/step10/twin/);
- the ROM ledger, after the restatement: `plat_ledger.py --self-test` PASS at the four points, 9 of 9 controls, and
  the fixture in six arms, `answering-ports` at 60.5 (receipts/step10/ledger/). Before the restatement, the ledger
  refused the stale `ctrl_plat` keys and the fixture at 60.0 (receipts/step10/ledger-before-restatement/).

## Attempt 1: the work cut, on the step-9 branch (`ab4bc245`), carried to p10 by merge (`547c0b1e`)

The largest legal AECP record at step 9 is arm A's `aecp-largest-notice` REMOVE_AUDIO_MAPPINGS of 63 mappings at
an input port, 95,482 CPU cycles at 1x1/1if, 1,005 us by the rule against the 975 us statement. Its committed PCs,
traced and split by function before the cut was chosen (receipts/cut/), put 16,135 of its 22,202 instructions in
`aecp_maps.c`: `aecp_map_command`'s own loops 6,649, `legal` 5,418 (once a mapping, 86 each), `wire_be32` 2,772 (four
calls a mapping, two of them through `wire_be64`, 819), `mark` 477, and `aecp_find` 2,432 (twice a mapping).

The cut (`ab4bc245`, `sw/firmware/ctrl/aecp/aecp_maps.c` only) takes out work every mapping of every edit does,
whatever the mappings are:

- **Each mapping's stream format is checked by the three bytes its channel count reads.** `format_channels(p)` is
  `channels(wire_be64(p))` for every byte pattern: `(f >> 56) == 2` is `p[0] == 2`, and bits 22 to 31 of the
  big-endian word are byte 4 and the top two bits of byte 5. That removes the `wire_be64` call and its two
  `wire_be32` calls from each `legal`.
- **The port's geometry is read once an edit.** `legal` read its streams' descriptor type and its port's cluster count
  and first cluster index for every mapping; `struct geometry` holds them, read once before the edit's table (after
  the port's length check, as before), and `valid` (the restore path) reads it for each call as `legal` did.

No check moves, and every result and response is unchanged. Neither cut depends on the mappings or the toolchain, so
the largest edit of any mapping set takes the same cut. No line a mutant or plant patches is touched (each anchor in
`aecp_mutants.py` and `aecp_map_mutants.py` was checked). A second variant, the same cut plus `wire_be16` written as
a sum (GCC 16 turns the OR form into a byte-swapped halfword it swaps back, ten instructions for five), reached
80,097 cycles. It was not taken: its saving rests on the compiler's choice, not on work removed.

| `aecp-largest-notice`'s dearest record, 1x1/1if, arm A | CPU cycles | Committed instructions | By the rule |
|---|---:|---:|---:|
| step 9 (`4a5bfb32`) | 95,482 | 22,202 | 1,005 us |
| the cut (`ab4bc245`, the step-9 branch) | 84,389 | 18,577 | 890 us |
| not taken: the cut and the sums | 80,097 | | 845 us |

By function, step 9 against the cut (instructions / cycles): `legal` 5,418 / 16,127 against 4,158 / 11,469;
`wire_be64` 819 / 2,036 against none; `wire_be32` 2,772 / 7,721 against 1,386 / 3,941; `aecp_map_command` 6,649 /
26,751 against 6,489 / 26,629; `aecp_find` 2,432 / 7,754 against 2,432 / 7,764. In all, 3,625 instructions and
11,093 cycles fewer, 85 us under the statement at the step-9 placement.

The cut reaches p10 by `git merge --no-ff flip-train-1117` (`547c0b1e`), clean, the gitlinks unchanged.

**`d7c8cd95`** documents the cut where the record's earlier changes are (`docs/design/SPLIT_CONTROL_MEMORY.md`, a
subsection after #923's): the attribution by function, the two changes and the record before and after.

**`dccca6ec`, a step-9 fix round 3 missed.** The merge of #934 (`8f6fbb84`) left `tb/verilator/milan_dp/README.md`'s
contents list with the boot leg's entry twice and without the split control path's and the twin's. `gen_toc.py
--check`, which the docs workflow runs, reports that drift at `8f6fbb84` and `4a5bfb32`. Round 3's quick list ran only
`--selftest`, so it was not seen. The list is rewritten by `gen_toc.py --write` and the two descriptions restored from
the train's step-8 page and #934's own, at step 9's counts (twenty-eight planted defects; fifteen plants). The quick
list now runs `gen_toc.py --check` and `--verify-anchors` at every head. At step 8 (`eafe4a16`) and before, the TOC
gate passes.

Both reach p10 by merge (`45af90b3`), with the twin's entry at step 10's sixteen plants.

**Checks on the cut** (`ab4bc245`): the four firmware shards PASS, the control campaign 797 of 797 (unchanged); the
two-placement simulation's four legs PASS. At the step-9 branch's tip, the quick list with the TOC gates passes but
the base's eleven, and the ledger passes at `ed5855fe`.

## Attempt 1: the relearn, on p10

`febbfc4b` on p10, traced at `547c0b1e` (the cut carried to step 10; `45af90b3` changes only documentation since).
By the recorded procedure and the third window of the amended ruling, item 1: the 1x1/1if split image, arm A, as
run.py builds by default, groups `backlog`, `backlog-adp` and `aecp-largest-notice`, run untraced and then each traced
by committed PC from 300,000 bus cycles before its first record's commit for 900,000 PCs. For `aecp-largest-notice`
that is the first RXC after its `aecp_long.*` mark. `backlog` traced 162,156 PCs (its run ends inside the window),
`backlog-adp` 900,000 and `aecp-largest-notice` 776,535; every PC falls in a `.text.<function>` section. Every
function the windows ran is listed in the order they first ran it, the third window's after the other two
(receipts/hot/relearn.sh, order.py, apply_hot.py; the traces by sha256 in the list's header). Nothing is placed by hand.

- **269 entries** against the 206 before it: 93 added, 30 gone. The third window's functions are the map edit's
  (`aecp_map_command`, `legal`, `mark`, `wire_be32`) and the `EDIT` window's (`aecp_face edit`, `beat`, `record`
  and their callers). They are the rehearsal's (round 3's `hot-rec`, 270), but for `wire_be64`, which the cut removed.
- **Gone, among the 30: MSRP's receive path** (`mrp_rx`, `mrpdu_parse`, `parse_pass`, `msrp_decode_attr`,
  `msrp_join_ind`, `rx_on_attr`, `msrp_map_join`, `apply_receive` and the rest), which these windows no longer run.
  The others gone are `mrp_transmit` and `map_replay`, MAAP's `enqueue` and `send_frame`, the notice fan-out's `fan`
  and `fan_end`, `aecp_tx_complete`, `mbx_hal_read32`, and ACMP's `delay` and `port_seed`. Under the amended ruling,
  item 3, the receive path may leave only if the measured SRP record stays within its statement at every point and the
  SRP rows and the last queued notice hold. The measurement below decides it.
- The list's header now records the procedure with its three windows as standing procedure, and that a fourth window
  or a window chosen for one head needs a ruling. The link script's comment names both windows and the region's size
  (some 57 KB, 56,868 B in the 269 sections). Section 11 of `SPLIT_CONTROL_MEMORY.md` says the list is relearned so.
  `ctrl_hot.py --check --map` passes on the traced image's map, and `--self-test` has 0 failures.

## The ledger after the cut and the relearn

- **`ed5855fe`, on the step-9 branch.** The cut takes the fixture's `answering-ports` arm at 8x8/2if to 131,128 B of
  `rom`, 56 B past the 131,072 B of step 9's 60.0, which had 72 B left (the cut adds 128 B there). That image's build
  was refused at `ab4bc245`. The firmware shards do not build that image, so they passed. Its entry is 60.5, S14 debt
  by the amended ruling, restated as step 10's was. The ledger then passes at the step-9 branch's tip: the platform
  at four points with 9 of 9 controls, the fixture in six arms (130,624 to 131,128 B), `test_ctrl_memory`.
- **`25b2a5b7`, on p10.** With the cut and the relearned list the platform's 8x8 one-interface image needs 137,328 B,
  112 B past the 137,216 B that 57.5 holds, so its entry is 58.0, S14 debt by the owner's rule of 2026-11-15. The
  other platform points are within their entries (124,696, 126,328 and 138,936 B). The fit section's debt list had
  the fixture still at 60.0, missed in step 10's restatement; it now says 60.5. `plat_ledger.py --self-test` passes
  at the four points with 9 of 9 controls.
- **`25299527`, on p10:** `ed5855fe` carried. Its five conflicted files take p10's measured text, and the fit section
  keeps the cut's own figure beside #936's.

Neither commit changes an image the harness builds: arm A's images at 1x1/1if and 8x8/1if built at `25299527` are
byte-identical to the measured `febbfc4b`'s (`ctrl_app.elf` sha256 `c60a4b85`, `77ac5bec`), and their gateware differs
in four comment lines.

## The measurement (HANDOFF-r4.md has the figures)

At the tip `febbfc4b` (and `25299527`, which builds the same images), the formal measurement's legs ran at 1x1/1if and
8x8/1if: arm A in eight parts, the answering-every-port arm, the answering-ports arm's held groups, and the
valid-destinations arm. Every 8x8/2if leg was refused at its link by LINKED (`aecp owe`, `aecp owed_drain`; the
conflict). The scratch variant (receipts/measure/variant.diff: the tip's list without those two entries, not
committed) ran the same legs at 8x8/2if. Verdicts come from `survey_point.py` and `record_classes.py` (round 4's copy
of the survey reads the point's interface count; receipts/tools/). No result was changed or regraded. The tip's other
gates: four shards PASS (the campaign 797 of 797), the twin and its plants PASS, the quick list PASS but the eleven,
and the platform's ledger PASS.
