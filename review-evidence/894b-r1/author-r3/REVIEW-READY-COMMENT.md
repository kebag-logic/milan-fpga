[A781] REVIEW READY
Commit: 716a8ae7979a31315a6e085959dc4dcc8b7ee022 (`894-8x8-1if`, round 3; nothing pushed, the PR is opened on `dev-soft-core` after #902 merges)

Round 3 under #894's ruling issuecomment-6878014227, with issuecomment-6871343905 item (b)(ii) and #902's bounds (issuecomment-6867990126). `894-tiers` was at `7398ec0a` (already merged here) at every check through the measurement and the docs, so the round made no sync merge. It has since moved to `9606b3a9` with #902 still OPEN, and that is not merged here: see the first open question.

Changed (three commits on round 2's `184d47ca`):
- **`d8629751`: THE RETRY's round costs keyed on the shape** (item 1).
  - THE SHAPES (`ctrl_loop.h`) states `CTRL_LOOP_RETRY_COLD_US` and `CTRL_LOOP_RETRY_ATTEMPT_US` for each shape: 85 and 34 us at (1, 2, 2), **165 and 25 us at (1, 9, 9)**, and 185 and 34 us at both two-interface shapes.
  - `AECP_ROUND_COLD_US` (`aecp_mbx.h`) and `AECP_ATTEMPT_US` (`aecp.h`) are those names, never the interface count's.
  - `aecp.c` includes `ctrl_loop.h`, because the core charges the attempt as an immediate (see the open question below).
  - The harness grades a round at its build's shape (`round_grade.stated_us`), reading the headers through THE SHAPES.
- **A correction to round 2's report:** `AECP_ATTEMPT_US` was never keyed on `MBX_N_IF`. It was a single 34 us at every shape. Only the cold start was keyed on `MBX_N_IF`.
- **The derivation.** It takes round 2's rounds at 8x8/1if, whose image is byte-identical to `184d47ca`'s: the dearest with no notice and 1, 2 and 4 refused attempts were 12,547, 19,326 and 23,343 cycles.
  - The rule is #665's definition of the attempt: what a round of every port refused costs past its cold start, per refusal. The cold start is what any round implies at that cost.
  - Of the lines that hold every round and charge a round of every port refused exactly its cost, the rule takes the one with the least cold start. It runs through the rounds of two and four refused attempts: 15,309 cycles once and 2,008.5 per attempt.
  - Plus 5 %, rounded up to 5 us, that gives 165 and 25 us. The other arms' rounds were within the earlier 85 + 34 k, which lies under the line up to four ports.
- **`716a8ae7`: the wire comparison's build of the core** (`aecp_wire.py`) takes `-I loop -I mbx`, as the host core arms do. The first full pass, at `bae44edf`, found it refused (firmware-verilator's boundary step: `aecp.c:6: fatal error: ctrl_loop.h: No such file or directory`), a compile context of the core I had not run before the commit. It now passes at one and two interfaces, and the step passes.
- **`bae44edf`: the docs.** FR_NFR 3.4.1, section 13 (the table, "THE RETRY's round costs at 8x8/1if" in place of round 2's "Left for a decision", and the gate's figures), and the AECP and harness READMEs.

New checks and their planted defects (each caught, with the point named):
- **`shape_costs.retry_findings`:**
  - the cold start back on `MBX_N_IF` fails with "8x8/1if: AECP_ROUND_COLD_US is 85 us at its shape (1, 9, 9), not the 165 us THE SHAPES state for it";
  - the attempt back at a single `34u` fails with "8x8/1if: AECP_ATTEMPT_US is 34 us at its shape (1, 9, 9), not the 25 us ...";
  - 8x8/1if's block stating the ternary fails with "... for the shape (1, 9, 9) (8x8/1if)".
  - `shape_costs.py --check --selftest` refuses 24 of 24 controls.
- **The harness self-test** holds a round at 8x8/1if to its shape's costs, apart from the interface count's. Its two mutants (the costs read at the interface count, and the round held at the interface count) are caught by that check.

Byte-identity (sha256 of each ELF and its loadable bytes):
- **With 8x8/1if left at 85 and 34:** all eight images are identical to `184d47ca`'s.
- **At 165 and 25:** the six 1x1 and 8x8/2if images are identical. In both 8x8/1if images exactly two instructions move: `scan`'s `addi -34` becomes `-25`, and `retry`'s `addi -85` becomes `-165`. The platform image is 56.0 RAMB36, with the same ROM and SRAM.
- **At the head:** the full pass's image build on a clean clone at `716a8ae7` gives the six identical to `184d47ca`'s, and both 8x8/1if identical to the measured `d8629751`'s. The platform image is 56.0.

Measured once at 8x8/1if on the new image (`d8629751`, clean clone). It used round 2 phase B's groups: every group of arm A, the `answering-every-port` arm and the `answering-ports` arm's `aecp-largest-notice`. That is 112 groups and 1,680 instances. The gate passes.

| Row (bound, ms) | Worst, ms (round 2's where it moved) |
|---|---:|
| AECP (20) | 4.693 |
| ACMP, ADP, MAAP (30) | 6.813, 5.897 (5.522), 6.020 |
| SRP (90) | 10.284 |
| MRPDU (49) | 3.578 |
| The first queued notice (20) | 2.259 |
| The last queued notice (130), of 40 | 26.195 (23.730) |
| The largest legal command, the paced R4L row (238) | 2.442 |

- **No cost is over its statement.** THE RETRY's 2,455,411 rounds are all within 165 + 255 n + 25 k us; the closest is 89.9 %.
  - Every leg exits 0, and no leg prints a STATED line. The `answering-every-port` arm exited 1 on 1,654 rounds at round 2's costs.
  - The same dearest rounds give the same line again.
  - Every other stated cost is within its measurement (the SRP record 32,421 cycles against 345 us, and every poll), so nothing is restated.
- **Budget misses.** The only ones are the seven held-egress rows, the same figures as round 2's (61.680 to 63.969 ms) and each under its ledger figure. None is new.
- **Joins and run-outs.** 346 joins, 186.687 to 190.705 ms, within 181.0 to 239.0. Of 2,311 run-outs, none was late, absent or unresolved.
- **Slices.** SRP's longest is 146,052, the build's 137,924 and THE RETRY's round 89,462, all within 147,500.
- **The load.** 0.711 at the pin and 0.671 with tsn-c-stack#32, within 0.75.
- **The image cap.** The platform image is 56.0.
- **The aged build's control.** `transmit-aged` is caught: 8 of 8 groups are over 49 ms, at 66.505 to 67.015 ms.

Validation: the full pass at the final head `716a8ae7`, each part on its own clean clone and never piped.
- **The sweep, 4 shards** (`native-shards.py`, each on its own fresh clone and its own picked CPU range): exit 0 each. 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures, nothing skipped.
- **Every hosted job step** of rtl-fast, rtl, elaborate and docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`): 139 run, 226 not run with a reason, 0 bad. firmware-verilator's boundary step passes, with `aecp_wire.py --every` at exit 0.
- **The firmware jobs:** every step 0.
  - The control, AECP and SRP campaigns caught 716, 275 and 345, with 0 escaped. `retry-round-cold-uncharged`, `notice-dropped-with-its-descriptors-next` and `map-table-each-direction-alone` are among them.
  - The boundary gate PASS.
  - firmware-unit's 8x8/1if mailbox arm: `[ok]`.
- **The lane gates:** 55 gates, 51 at 0. The four that exit 1 by design are `rows_tiers --terms`, `flip --check`, `--point 1x1/1if --design as-built` and `--point 8x8/2if`. They include:
  - the harness self-test: 0 failures, 879 checks, 259 mutants caught, 0 escaped;
  - rows_tiers 971/971, flip 581/581 and load 25/25; `load_grade.py --check` 0.513 and 0.509; `tier_grid.py --point 1x1/1if` exit 0; the table of shapes 24/24;
  - the flip check at 8x8/1if PASS (0.711) and at 1x1/1if PASS;
  - diff checks against 15 bases (`7398ec0a` and `184d47ca` added);
  - em-dash, the idioms, docs and `ctrl_hot`;
  - BDD, the twin and its plants, the builder tests, NVM, and boot 1x1, 8x8, native and plants.
- **The harness legs at 1x1 and 8x8/2if** (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`) exit 0, except `srp` at 8x8/2if. That one exits 1 on #910's build of one (138,054 and 147,814 against 121,500), as in round 2 and as #902 reports.
  - The plant control C-R1 is caught.
  - 48 joins in 11 group runs, 185.485 to 190.040 ms. Of 172 run-outs, none was late, absent or unresolved.
- **Every image:** see the byte-identity list above.
- **A first pass, at `bae44edf`, is superseded.** Its only bad step (139 run, 1 bad) was the wire comparison's build of the core, fixed in `716a8ae7`. Everything else there matched this pass.
- **Before the pass:**
  - the harness self-test at `d8629751` (clean clone): 0 failures, 879 checks, 259 mutants caught, 0 escaped;
  - the 8x8/1if mailbox tests (`EIGHT_ONE`): 4 of 4;
  - the host core arms at one and two interfaces, and debug: rc 0.

Acceptance criteria (the round 3 ruling):
- **Item 1 met.** Both costs are keyed on the shape through THE SHAPES (`CTRL_LOOP_SHAPE`'s shape header), with none falling back to the interface count. They are stated at 8x8/1if at the measurement plus 5 %, derived and never mirrored, and checks with planted defects name a falling-back shape.
- **Every 1x1 and 8x8/2if image is byte-identical**, by sha256.
- **Item 2 met.** The re-measurement once at 8x8/1if meets every criterion, and the `answering-every-port` arm shows no cost over its statement.
- **Item 3 met.** Section 13, FR_NFR 3.4.1 and the PR body are restated, and the full pass ran once at the final head.
- **No STOP trigger fired:** no row over its bound, the load 0.711, the platform image 56.0, no slice over 1,600 us, and no 1x1 or 8x8/2if image changed.

Open risks/questions:
- **Left for a decision: `894-tiers` has moved to `9606b3a9`. #902 is OPEN, its round 12 delta reviews NEGATIVE at that head.**
  - **When.** Every fetch through the measurement and the docs showed `7398ec0a`: 15:03, 16:35, 17:3x and 20:1x CET. The move is ten commits, the first committed 16:42 but pushed after 20:1x. I saw it at 23:1x, after the final full pass.
  - **What it changes.** `aecp_maps.c`'s code (new `struct edit` fields and their logic), so every image moves, 8x8/1if's included.
  - **What a merge needs.** #902's new head as the byte-identity base, and a second 8x8/1if measurement and full pass. This round allows one of each, and its sync item applies before measuring, so it is not merged here.
  - **The choice.** Either the planned `dev-soft-core` merge after #902 merges brings it, or a ruling asks for the sync and a measurement now.
- **The AECP core now reads `ctrl_loop.h` at compile time.**
  - **Why.** The attempt cost is the core's immediate, and the shape's interface count is the mailbox contract's.
  - **What it does not do.** The core calls nothing that header (or the `mbx.h` it includes) declares, and the disassembly shows no other change.
  - **The README** (which said the core has no mailbox dependency) now says "at run time", and names the one header.
  - **The alternative.** An adapter-set attempt cost at run time, as `notice_us` is, would move every image, which the ruling forbids. This is for the reviewers to accept or refuse.
- **`AECP_NOTICE_US` stays keyed on the interface count.** The ruling keys the other two, and every round with a notice at 8x8/1if is within it.
- **For a new Issue:** `Mailbox.ARoundFillsWhatItsPassHasLeft` fails at the 8x8 shape at one interface already at `184d47ca`. Its last step expects a queue served to its end within `AECP_NOTICES_MOST` share-sized rounds (`test_aecp.cpp:3121`, `adapter.yields` 3). It was never selected there, is not changed here, and is left out of the 8x8/1if selection.
- **Still left for a decision from round 2:** 1x1/1if's SRP record (26,086 cycles in round 1, over its 250 us).
- **Reported, not held (#872):** 8x8/1if's rows by every source, now with its own round costs: the last queued notice 274.91 ms (266.70 at 85 us) and R4 18.64, and the every-command-largest load 0.993.
- **Environment, not code:**
  - docs-check-no-git strips `.git` by design. Its steps are all rc 0; only the local driver's own post-run `git status` fails, as in round 2.
  - My slips in the pass, each corrected before it counted:
    - the first sweep spec lacked `TSN_GEN_ROOT`, so shard 3 skipped `tsn_fuzz`'s field campaigns. It was run again, with 21,575 checks.
    - the final sweep's first launch reused clones whose `--shared` source I had deleted. Those four units were stopped, and the sweep ran on fresh clones.
