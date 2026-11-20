[A794] The flip train, composed: twelve frozen PRs merged in train order onto dev-soft-core, each conflict resolved keeping both sides, and the composed images measured at the final head

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Head `15168e14` on `flip-train-1117-p11`: every owner bound holds at 1x1/1if and 8x8/1if.**
- **What is in:**
  - F-G5's composition fix (`01765bb0`);
  - step 13, #953 (#943, `c05d5acb`), and step 14, #952 (#951, `4b9f66c5`);
  - a boundary classification fix (`c1e95dc1`);
  - the SRP cut (#665's ruling of 2026-11-20, item 3, `92de01f7`), and two SRP plants re-targeted after it
    (`fb083864`, tests only);
  - ruling item 4 at 1x1/1if, as the owner decided (#665 issuecomment-7044585511, `8c5e2b4f`), and its re-measure
    recorded (`8dc85884`, docs only);
  - the train's source and test comments and check texts citing rulings by issue, date and item, not by issue-comment
    or review IDs (`15168e14`, comments and message strings only: every image byte-identical to `8dc85884`'s).
- **Item 4's consequence:** at the restated notice path, #894's slice rule takes 950 us at 1x1/1if, not 900. With it
  the queued rule takes `CTRL_LOOP_QUEUED_MS` to 130 ms. The owner's 140 ms bound does not move. The slice is code,
  so 1x1/1if's images change (five immediates), and 1x1/1if was measured again in full on them.
- **1x1/1if:** 0 of 68 statements exceeded.
  - The rows by every source: last 127.31 of 130, ACMP 29.06 of 30, txL 47.88 of 49.
  - The load is 0.5114 of 0.70.
- **8x8/1if:** its images are unchanged, so `92de01f7`'s measurement stands: 0 of 68 exceeded, and the load 0.7436 of
  the owner's 0.75.
- **The gates pass** at `8c5e2b4f` (826 of 826 plants caught), with the previous heads' exceptions. At `15168e14`,
  comments and message strings only, the images, the ledger and the quick list (every self-test, the checks, the
  idioms and the docs) pass again.
- **The gating bench bitstreams of `8c5e2b4f`** (its firmware and gateware are the final head's) meet #818's floor at both points:
  1x1/1if `c7189218…`, 8x8/1if `7d903412…`.
  - Their loaded firmware equals the head's product images byte for byte. Every loaded section and PT_LOAD is listed
    on each side with its VMA, LMA, length and full sha256, and their rom words equal the builds' rom init.
  - The receipt is the lane's `receipts/step16/gating/loaded-identity/`, re-runnable, with planted controls. The
    published manifests sit beside it, and `receipts/step16/gating/clone-state/` gives each build's clone head and
    porcelain line, now and as the chain logged them.
- **The release image** is byte-identical where loaded at every head from step 11's record head `b1f1161b` to this one
  (`bios.bin` `603b9ca3…`, the AEM blob `bdfde7cf…`, the ROM, SRAM and memory init files), its Verilog equal outside
  its comments (the lane's `receipts/step16/release/`).
- **Where the rest is:** the lane's `CPU-TABLE-8c5e2b4f.md` and `CPU-TABLE-92de01f7.md`, its RESOLUTIONS and the
  HANDOFF status.
- **Then:** the manager pushes.

The flip slips to the weekend by the owner's decision of 2026-11-19 12:29. F-G5 (the final gating run's 1x1/1if (h)
#25: a narrowed STREAM_INPUT not kept across a power cut) is fixed at `01765bb0`; the bench re-checks it on new gating
images.

The step-12 sections below (its split routes and its images) are step 12's own, `0839453f`'s. The final head's figures
are in [Composed figures at the final head](#description), and its bench images in the Status above. Each later
composition fix's gates and images are in its composition row and in the lane's RESOLUTIONS.
The composition review of steps 1 to 11 is complete: R865-1 POSITIVE at `73272666` (#945 issuecomment-6986847711),
R866-1 POSITIVE at `73272666` and R866-2 POSITIVE at `b1f1161b`.

**Step 12 is #947 (#946) at its frozen head `fe297847`.**
- **Its reviews:**
  - R867-3 POSITIVE at `fe297847` (#947 issuecomment-6996096094);
  - R868-2 POSITIVE at `9f4f3de0` (#947 issuecomment-6993952183). Round 3 is tests and docs only, so R867-3 covers it
    by the single-reviewer rule for trivial deltas.
- **What it does:** the split platform writes each AAF Stream Input's current format into its receive-monitor
  context, so 8x8/1if's inputs 1 to 7 take their PDUs. It is merged in three rounds:
  - **Round 1** (`66c6edf3`) merges clean (`d09c7118`). One composition fix raises the platform's 8x8 two-interface
    ROM entry to 63.0 (`967b1ca9`, S14 debt).
  - **Round 2** (`9f4f3de0`, merged as `7650a02d`) writes each kept change's contexts in the face's change port, and
    refuses a waiting change whose input was bound meanwhile. Its ledger conflicts take the train's side, which
    already holds 63.0.
  - **Round 3** (`fe297847`, merged as `0839453f`) adds the receive monitor's change-gate tests and their defects.
    Its one ledger-prose conflict takes the train's side.

At the final head:

- the CPU service budget passes at every point by its rule, 8x8/2if carrying the base's same eleven findings,
  reported and not held. Of its twelve images, 1x1/1if's four were measured in full at `8c5e2b4f` and 8x8/1if's four,
  byte-identical, at `92de01f7`; 8x8/2if's are graded from their statements;
- the split gateware's Verilog and constraints are step 14's (compared at `92de01f7`); only the ROM's firmware
  contents differ, and item 4 changes five immediates of 1x1/1if's firmware, not its size;
- the gating bench bitstreams are new builds of `8c5e2b4f`, meeting #818's floor at both points, and their loaded
  firmware is the final head's product images' (the Status above);
- the release image is byte-identical where loaded to step 11's record head's.

**F-G4, from the gating bench run, is WITHDRAWN as a bench-topology finding.** The test machine saw every mode
offered, and got a link with 10BASE-T half alone.
- **The cause was the bench, not the DUT.** A second diagnostic read the DUT's own PHY: it advertises 1000BASE-T full
  alone, as #840 requires, and makes no link with a 10BASE-T-half-only partner. The test machine was negotiating with
  the inline capture tap, which advertises every speed.
- **Nothing goes into the train for it.** The diagnostic and candidate branches stay as scratch, and one gap they found
  is #495 residue (see the known limitations).

The release record is re-baselined by one record-only commit, as #665's three rulings of 2026-11-18 decide:

- issuecomment-6979461559: the release image's LUT growth is accepted;
- issuecomment-6979996755: the render crossing's move to distributed RAM is accepted, and a CDC check comes first;
- issuecomment-6981065172: the check's CDC-15 rows are the expected report.

The gate passes at the final head (see [Release image](#release-image)). `flip-train-1117-p11` -> `dev-soft-core`.

## Linked Issue / roles

Relates to #665
Relates to #871
Relates to #894
Relates to #640
Closes #917
Closes #929
Closes #919
Closes #920
Closes #923
Closes #924
Closes #930
Closes #925
Closes #936
Closes #927
Closes #946

Executor: `[A794]`
Internal cleared-context reviewer: the composition review, by both reviewers (#665 issuecomment-6939574513, item 3)
External reviewer: the same composition review

## Description

One train branch on dev-soft-core `cb96336d`, by the owner's rules for the flip train (#665 issuecomment-6939460730,
option B; issuecomment-6939574513, freeze and compose once). Each frozen PR head is merged with `git merge --no-ff`,
so each becomes an ancestor and GitHub marks it merged when the train lands. There is no rebase, squash or
cherry-pick. Before each merge, the head was checked against the PR's GitHub head. Step 11 is composed on the step-10
candidate by #665's ruling of 2026-11-18 (issuecomment-6975966775). The gitlinks are #934's: `gptp-processor`
`1616fc8f` and `protocol-processor` `801ef228`.

| Step | PR | Frozen head | Its two POSITIVE reviews | Merge | Conflicts |
|---|---|---|---|---|---|
| 1 | #881 (#871, AECP REBOOT and the reset port) | `d3e61e37` | R821 at the head; R822 at its ancestor `d3566d44` | `43b954e6` | 18 |
| 2 | #914 (#930, #894: the 8x8/1if tier rows, THE RETRY keyed on the shape) | `e1ecce20` | R843-7 at the head; R844-5 at its ancestor `d0a2a160` | `877c99e4` | 12 |
| 3 | #918 (#917, the AECP command held to the next refill) | `394612c5` | R846 and R845 at the head | `9c0e1974` | 7 |
| 4 | #935 (#929, the split gates at the base) | `37255683` | R856 and R855 at the head | `22a82038` | 2 |
| 5 | #933 (#919, the PHY poll and 1000BASE-T only) | `1a1e6665` | R852 and R851 at the head | `2078c438` | 13 |
| 6 | #938 (#920, a name burst durable within 5 s) | `81c9a1a0` | R857 at the head; R858 at its ancestor `bd252db1` | `7c28f53f` | 5 |
| 7 | #931 (#923, #924, map edits through the EDIT window) | `d06ded5a` | R847 and R848 at the head | `6a8126e4` | 15 |
| 8 | #932 (#925, the latest Talker registration decides the Listener declaration) | `0fdfdba7` | R849 at the head (issuecomment-6942554887); R850 at its parent `5f625090` (issuecomment-6939719451; the head adds one ledger edit) | `31304b74` | 7 |
| 9 | #934 (dev `6b66f66d` synced into dev-soft-core) | `544fd72c` | R853-4 at the head; R854-3 at its ancestor `9aa55d3b` | `8f6fbb84` | 8 |
| 10 | #944 (#936, the GET_STREAM_INFO notice on a Talker's declaration) | `d1aa4c44` | R861 (issuecomment-6961585565) and R862 (issuecomment-6960786467) at the head | `49f005b9` | 13 |
| 11 | #939 (#927, the timing cut: the EDIT claim search registered in the split build; the meter reference and the render FIFO's distributed storage in every image that carries them, the release image included) | `0297a19a` | R863 (issuecomment-6978630716) and R864 (issuecomment-6976209927) at the head | `3e908539` | 1 (two hunks of a README) |
| 12 | #947 (#946, each AAF Stream Input's current format written into its receive-monitor context on the split platform) | `66c6edf3` | R867 and R868 (round 1) | `d09c7118` | 0 (four files auto-merged, hunks apart) |
| 12, round 2 | #947's round 2 (each kept change's contexts written in the face's change port; a waiting change whose input was bound meanwhile refused) | `9f4f3de0` | R868-2 POSITIVE (#947 issuecomment-6993952183) | `7650a02d` | 7 (the ROM ledger and its prose: each the train's side, the plat README's two ROM hunks the train's text) |
| 12, round 3 (frozen) | #947's round 3 (the receive monitor's change gate tested at a bound input's own index, a STREAM_OUTPUT's waiting format and the input's SET_NAME; tests and docs only) | `fe297847` | R867-3 POSITIVE at the frozen head (#947 issuecomment-6996096094) | `0839453f` | 1 (`ctrl_memory.py`'s ledger comment: the train's side) |
| 13 | #953 (#943, a declaring STREAM_OUTPUT's stream_dest_mac its Talker's MAAP address and REGISTERING / REGISTERING_FAILED its Listener's; the CPU budget's declaring-outputs arm) | `a16899b1` (frozen) | R871-2 POSITIVE (#953 issuecomment-7019514213), R872-2 POSITIVE (issuecomment-7018882584) | `c05d5acb` | 0 (two files auto-merged, both sides kept) |
| 14 | #952 (#951, a withdrawn Talker's changed destination held over two of the longest LeaveAll periods) | `f09d82e0` | R869-1 POSITIVE; R870-2 NEGATIVE pending the final-image CPU timing evidence, which this round's re-measure provides | `4b9f66c5` | 0 (three docs files auto-merged, both sides kept) |

Every conflicted file has a resolution row in the lane's RESOLUTIONS tables, attached to the composition review: both
sides' intent, the resolution and why.

**Composition commits.** Each fixes only what the union broke, or does what a #665 ruling orders. None changes a PR's
own change, and no test or plant is removed.

| Commit | What | Why |
|---|---|---|
| `6fef44b8` | Three `build.py` comments rewrapped, one `grade.parse` comment moved; words and AST unchanged | the union broke the idiom ratchet, which may not be raised |
| `7431b6ba` | `grade.grade`'s `interfaces` and `shape` folded into one parameter; #938's burst mutants in their own module, table AST-identical | the union passed the six-parameter and 1,000-line limits |
| `b1af3b54` | Five SET_STREAM_INFO defects moved to `aecp_stream_info_mutants.py` in place (table identical, 361); three docstring items rewrapped | the idiom gate after step 7 |
| `03c92617` | THE STEP composed: a call owing no centisecond step gives an owed PHY frame the turn, and the store's extra step waits; B12's L5 and L6 and four plants; the coverage ratchet regenerated | #919's PHY poll and #920's paced saves both claim the step (#665 issuecomment-6950343235, decision 2) |
| `45708d9e`, `afbbde54` | THE STEP's plants rewrapped and split into their own function; the table unchanged | the idiom gate |
| `eafe4a16` | #930's Listener-copy oracle composed with #925's declaration rule; the ratchet regenerated | the two Listener-copy suites failed one oracle check at the merge |
| `6ad5c259` | THE STEP's extra-step plant builds: its condition keeps `owes()` referenced | it did not compile under `-Werror`; 797 of 797 caught after |
| `4a5bfb32` | The MRP timers' mutants in `selftest_mutants_mrp.py` in place; `grade.py`'s docstrings rewrapped | the idiom gate after step 9 |
| `dccca6ec` | The two-placement README's contents list restored by `gen_toc.py` | the step-9 merge broke it |
| `ab4bc245`, `d7c8cd95` | The largest legal AECP record's map-edit work cut, and documented | round 1's probe put that record over its statement; the cut is taken at the composed head (#665 issuecomment-6950343235, decision 3; issuecomment-6959600243) |
| `ed5855fe` | The size fixture ledgered at its measured 60.5 | S14 debt, by the owner's rule of 2026-11-15 |
| `082d0037` | #936's talker-notice plants' verdict moved to `talker_notice.py`, body unchanged | the idiom gate after step 10 (`run.py` 994 lines) |
| `b5802de9`, `68c97849`, `41d2bc2b` | The split image's hot list relearned on the step-10 candidate by its three-window procedure and the ruled filter, then re-traced on each cut | the third trace window (#665 issuecomment-6959600243) and the filter (issuecomment-6967930396) |
| `26f30fea`, `3e1c3dd9`, `08c28218`, `6448e431` | Attempt 2's cuts carried from the step-9 branch by merge: a notice's per-recipient work (`067c319d`) and its include fix (`0bc158a7`); SRP's delivery tells ACMP only a changed Listener presence (`7b3c1c94`); the DMA driver's test T8 (`112ab9b1`) | #665 issuecomment-6967930396 and issuecomment-6972255348, attempt 2 |
| `bf2c1184` | The ROM ledger at the measured sizes: `ctrl_plat` 18,048 B at 1x1/1if and 21,568 B at 8x8/2if; 8x8/1if's platform entry 58.0 | S14 debt |
| `7a536fc5` | The paced class's SET_CONFIGURATION control re-anchored to where that command is the class's dearer member | after the restatement, the plant would move no figure |
| `0cfe1ddc`, `3cdc613b`, `0b054867`, `c8ff391a`, `4374cc27` | The step-10 candidate's figures restated by the unchanged rule (below) in the tables, `ctrl_loop.h` and the prose; one self-test check and two own-record controls re-anchored to read the restated figures | issuecomment-6972255348, items 2a and 2b |
| `74481d2e` | `4374cc27` carried onto step 11 | it landed on the step-10 candidate after step 11 was merged |
| `05dc1791` | The blank line at the end of `plat_mutants.py` dropped | `git diff --check` over the train |
| `73272666` | The resource gate's release record (`route-1x1`) re-recorded by `pp_resource_gate.py record --write`, and its provenance note restated; the record only, no RTL or firmware | the release image's +541 LUT, accepted as #640 debt (#665 issuecomment-6979461559, issuecomment-6979996755 and issuecomment-6981065172) |
| `b1f1161b` | `docs/DOCUMENTATION_AUDIT.md` regenerated by `docs_inventory.py --write`, docs only: the step-1 README `tb/verilator/ctrl_reboot/README.md` (#881) listed, six pages' cited paths restated (`MAILBOX_SPLIT`, `REBOOT_RESET`, `FR_NFR`, the plat, srp and split-boot READMEs), and the counts | #934 (step 9) brings the inventory, fresh at its own head `544fd72c`; the steps composed around it were never inventoried, so the step-9 merge `8f6fbb84` left the page stale (122 lines at its check) and step 10's merge `49f005b9` one line more |
| `967b1ca9` | The platform's 8x8 two-interface ROM entry 62.5 to 63.0 (refused at 63.5), the ledger's cases and planted ledgers with it, the debt in SPLIT_CONTROL_MEMORY.md section 5's S14 list (7.0 RAMB36, 28,672 B), and the ledger's case writer re-anchored to reach half a tile past 63.0; no case or plant removed | the union broke the ledger: #947's writes add 960 B of `rom`, so the 8x8 two-interface platform image needs 140,008 B, 744 B past the 139,264 B that 62.5 holds beside its `sram`; S14 debt by the owner's rule of 2026-11-15. Every other point holds its entry |
| `01765bb0` | F-G5: a saved stream format is judged supported alone while the saved state is applied, before the face opens (`aecp_face.c`, `format`); from the open on, the verdict's low byte must be exactly 3 as before. S12 in the sink suite at both shapes, with a far model that keeps the datapath's map store; a Face test before and after the open; three plants and a `platsinks1` arm; the arms dict reflowed by one line to stay within the idiom gate's 1,000 lines | The final gating run's (h) #25 at 1x1/1if: STREAM_INPUT 0 narrowed from 8 ch to 1 ch (its mappings removed first) read 8 ch after a power cut. The boot restore judged the saved format by the datapath's verdict, whose survival bit reads the map store, and before the open that store still holds its reset set, which at 1x1/1if maps input 0's 8 channels. So the restore was refused and the default kept. 8x8/1if's input ports have no reset mappings, so it kept the change. REQUIREMENTS.md's persisted inventory (Milan v1.2 5.3.8.1) |
| `c1e95dc1` | `sink_mutants.py` (#946) and `talker_notice.py` (#936) classified in `ctrl_configs.py`'s `OUTSIDE` | the firmware boundary gate refused them: builders found by text, compiling nothing, which the union left unclassified (found by #943's lane) |
| `92de01f7` | The SRP cut (#665's ruling of 2026-11-20, item 3), `srp_mbx.c`, each exactly equivalent: lwSRP's reclaim owed only where an attribute may be freed, the receive filter's sink pass made only from a Talker indication on, a Listener looked up among the sources once a use, the walk-free snapshot's capture made in place; `srp_listeners.cpp`'s differential against the adapter before it and four tests; 10 plants (`srp_reclaim_mutants.py`) | 8x8/1if's `record.srp` and `item.reclaim` over their statements put its load at 0.7512 restated: `srp-talker-held` alone is now `record.srp` 34,803 (370 us), `item.record` 34,550 (365), `item.reclaim` 0 |
| `fb083864` | Two SRP plants re-targeted where the cut leaves their defects observable: `same`'s skipped last byte under a Talker's near miss of a bound sink (`srp_walk.cpp`), the filter's Failed-first copy against the cut's differential; tests only | shard 3 found them escaped at `92de01f7` |
| `8c5e2b4f` | Ruling item 4 at 1x1/1if: the AECP notice item 210 -> 150 us and the long notice 365 -> 315 restated from their measurement; the paced map edit 315, SET_STREAM_INFO 250, ADP's donor record 105 and the centisecond 170 raised by the rule; then the slice rule's 950 us (was 900) and the queued rule's 130 ms (was 140; the owner's bound stays 140) that follow; THE TRANSMIT's control planted under its row, the shape table's queued fallback plant apart in its own table, run.py's queued constants (130, 130, 62); docs | the SRP cut's code moved two AECP records over their statements by layout at 1x1/1if, taking the last queued notice and ACMP over their owner bounds by the usual rule; the owner decided item 4 applies here (#665 issuecomment-7044585511) |
| `8dc85884` | `SPLIT_CONTROL_MEMORY.md` records 1x1/1if's full re-measure at `8c5e2b4f` (0 of 68 statements exceeded; the centisecond and ACMP's event moved by the slice's scheduling), and its "What is left" states this head's slice and queued bound, 950 us and 130 ms; docs only | the summary still read 900 us and 140 ms |
| `15168e14` | The train's source and test comments and check texts cite rulings by issue, date and item, not by issue-comment or review IDs: 14 files, comments, docstrings and message strings only (two check texts: run.py's self-test's queued constants and the declaring arm's fixture check). With comments removed and string literals masked every file is the same code. The twelve CPU budget images, the four product images and the release export are byte-identical to `8dc85884`'s, and every self-test still refuses every plant | the owner's rule of 2026-10-15 on source comments (R865-4's two residue items); one ID older than the train, in `reboot_ctrl/mutants.py`, is out of its scope |

**The rule for figures.** A figure that two PRs both restate is carried at the side that moved it, the larger where
both did. It is restated from the composed image after the last merge, by its tool or by the rule: stated cost =
measurement + 5 %, rounded up to 5 us, never below the measurement.

**Composed figures at the final head** (`15168e14`, whose figures are `8dc85884`'s). The CPU service budget, by
`flip_grade.py --check --point` and `load_grade.py --check` at the head, and the full re-measures
(`CPU-TABLE-8c5e2b4f.md` at 1x1/1if, `CPU-TABLE-92de01f7.md` at 8x8/1if):

| Point | Verdict | The tightest rows |
|---|---|---|
| 1x1/1if | **PASS**; 0 of 68 statements exceeded, measured in full at `8c5e2b4f` | the last queued notice 127.31 of 130 ms (the owner's bound 140), ACMP 29.06 of 30, txL 47.88 of 49; the load 0.5114 of 0.70 (0.5083 with tsn-c-stack #32); the paced record 315 of 315 us (29,993 cycles) |
| 8x8/1if | **PASS**; 0 of 68 statements exceeded, measured in full at `92de01f7`, its images unchanged since | `record.srp` 34,803 cycles within 375 us, `item.reclaim` 995 within 40 us; the load 0.7436 of 0.75; THE TRANSMIT's row 76.81 ms of 77; no budget miss but the seven `backlog-owed` egress-hold rows the harness README ledgers at every point |
| 8x8/2if | the base's same eleven findings, no twelfth (owner's decision of 2026-11-12); not re-measured | THE TRANSMIT's row 104.69 ms, stated 105; the load 0.799 |

**Restated at the final head**, by the rule:

- 1x1/1if, ruling item 4 as the owner decided on 2026-11-20:
  - from their measurement: the AECP notice item 150 us and a notice longer than `AECP_FAN_BYTES` 315;
  - raised by the rule: the paced map edit 315, SET_STREAM_INFO's AECP record 250, ADP's donor-column record 105 and
    the centisecond 170;
  - then `CTRL_LOOP_SLICE_US` 950 (#894's slice rule) and `CTRL_LOOP_QUEUED_MS` 130 (the queued rule, under the
    owner's 140).
- 8x8/1if:
  - the polls base 300 and the apply 375;
  - the MAAP record 180 and the ADP record 135;
  - the SRP record 375, with `CTRL_LOOP_SRP_UNIT_US` 375 (the unit follows its record);
  - `CTRL_LOOP_TX_MS` 77, which is at most 80, so `SRP_REDECLARE_CS` stays 8 cs.
- 8x8/2if: the MAAP record 160, a pass's events' fixed part 45 and AECP's timer event 120.
- The ROM: the size fixture 60.5 (S14 debt 4.5), the 8x8/1if platform image 58.0 (S14 debt 2.0) and, at step 12,
  the 8x8/2if platform image 63.0 (S14 debt 7.0).

**The split routes** (the AX7101 split route, three placement directives; #818's floor is WNS >= +0.030 ns and WHS
>= 0 at every signoff corner), at step 12 `967b1ca9` and at step 11:

| Point | Head | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high | Floor |
|---|---|---|---|---|---|
| 1x1/1if | step 12 | **+0.334 / +0.034** | +0.231 / +0.028 | +0.179 / +0.025 | met on all three |
| 1x1/1if | step 11 | **+0.141 / +0.033** | +0.054 / +0.036 | +0.031 / +0.036 | met on all three |
| 8x8/1if | step 12 | **+0.073 / +0.034** | +0.064 / +0.027 | +0.006 / +0.036 | met on its best of three |
| 8x8/1if | step 11 | **+0.073 / +0.034** | +0.064 / +0.027 | +0.006 / +0.036 | met on its best of three |

At `7650a02d` (#947's round 2) the split gateware is unchanged against `967b1ca9`, at both points. The rom banks keep
their depths, the exported Verilog is equal outside its comments, and the constraints are equal. Only the banks'
initial contents, the firmware, differ. So the three-directive routes above stand. The two gating bench builds of
`7650a02d` (the gating lane's recipe, `--eth-port e2`, ExtraPostPlacementOpt) sign off:
- 1x1/1if: Slow +0.276 / +0.102, Fast +1.641 / +0.036;
- 8x8/1if: Slow +0.176 / +0.102, Fast +1.523 / +0.036.

Both meet the floor and the ruling's WHS >= +0.030, with 0 routing errors.

Before step 11, 8x8/1if missed on all three directives (best +0.005 ns). The worst path ran from the EDIT window's
request to the AAF map's claim enables, and #927 cuts it: the datapath clock's worst is now +0.835 to +0.989 ns. The
1x1/1if image falls from 83 to 80 block RAM tiles. The render master's crossing is shared, not split-only, so the
release image takes the distributed storage too (74 to 71 RAMB36).

**Why step 12 re-routes.** The split firmware lives in the control memory's block RAM: `rom` is initialised with
the image the build links, and its banks are sized from that image (SPLIT_CONTROL_MEMORY.md section 2). So the
firmware is an input of the routed design, and the bench's image is that build's bitstream.

- At 1x1/1if #947's code takes `rom` from 124,832 to 125,792 B, past a granule. The last bank grows from 512 to
  1,024 words, which changes 5 lines of the exported Verilog outside its comments (the bank, its address and the
  decode). The routed design moves by +104 LUTs; the block RAM totals are unchanged.
- At 8x8/1if the banks keep their depths, the Verilog is equal outside its comments, and the constraints are equal.
  Only the banks' initial contents differ, and the placed utilisation is identical to step 11's in every line.

**The images at step 12** (`ctrl_app.elf`, sha256 prefix):

| Image | Step 11 | Step 12, round 1 (`967b1ca9`) | Step 12, round 2 (`7650a02d`) |
|---|---|---|---|
| The platform's split image, 1x1/1if (the shipping image the bench runs) | `a00828fe` | `f04caf59` | **`e937ca14`** |
| The platform's split image, 8x8/1if (shipping, the bench's) | `5edbba3a` | `22ada381` | **`4818bec6`** |
| The platform's split image, 1x1 with two interfaces | `76eae358` | `0a9a8201` | **`3e67aaea`** |
| The platform's split image, 8x8 with two interfaces | `d090b8d6` | `dcec0148` | **`9c67031d`** |
| The CPU budget harness's twelve images (3 points x 4 arms, below) | | equal, every one | equal, every one |
| The release (all-fabric) image | | byte-identical: `bios.bin`, the AEM blob and the ROM, SRAM and memory init files equal, `bios.elf` equal with debug sections stripped, the gateware Verilog equal outside its comments | byte-identical where loaded: `bios.bin` and the AEM blob equal, the Verilog equal outside its comments |

Step 12's frozen head `0839453f` (#947's round 3, tests and docs only) leaves every image above as at `7650a02d`:
- the four platform images, byte for byte;
- the twelve CPU budget images, equal to step 11's;
- the release, byte-identical where loaded.

At step 12 the gating bench bitstreams were `7650a02d`'s, `550e2d8d…` (1x1/1if) and `b449f2ca…` (8x8/1if). Their
firmware's loaded sections equal the ledger's links above: `ff21e091…` and `f2f81d5f…`. The bench's are now
`8c5e2b4f`'s (the Status above).

A split ELF's whole-file sha256 also follows the toolchain and the stand-in export it is linked against (the
symbol table's order). So a bench build is compared by its loaded sections, as the lane's
`receipts/step16/gating/loaded-identity/` does.

**The CPU budget harness's images and the measurement.** Every CPU budget harness image of the final head
(`ctrl_app.elf`, sha256 prefix; byte-identical at `8c5e2b4f`, `8dc85884` and `15168e14`):

| Point | Arm A | answering-every-port | answering-ports | valid-destinations |
|---|---|---|---|---|
| 1x1/1if | `1d38aa27` | `3514124c` | `125ea330` | `0ef0bb72` |
| 8x8/1if | `d4dee385` | `678a1168` | `a69e9773` | `717afd50` |
| 8x8/2if | `c0f27283` | `196e71fc` | `85d0f4b6` | `908833ab` |

- **1x1/1if** was measured in full on these images at `8c5e2b4f`: every arm and group, 64 parts, 0 refusals, and 0
  of 388,313 passes over the share (`CPU-TABLE-8c5e2b4f.md`).
- **8x8/1if** was measured in full at `92de01f7`, whose images are these byte for byte (`CPU-TABLE-92de01f7.md`).
- **8x8/2if** is reported, not held, and graded from its statements.

**`cdc_pair_fifo`.** #927 reorders the default branch's storage block. It is behaviour-identical by reading, and a
bounded equivalence proof finds no counterexample:

- the proof is from the zero state, with both clocks free, over 30 steps;
- it is complete at every depth a default-branch instance takes: 4, 8 and 16.

A standalone synthesis maps the module identically at three of the four parameter sets a default-branch instance
takes. At 48 x 16 (the I2S playback's FIFO, in none of these images) it uses 2 fewer LUTs. Only the render master's `u_fcdc` takes `DIST_RAM_P = 1`
(the next section).

### Release image

The all-fabric AX7101 image by the baseline recipe, routed at step 11 and the `route-1x1` record since `73272666`.
Its export is byte-identical where loaded at every head from `b1f1161b` to the final head, and its Verilog is equal
outside its comments (the lane's `receipts/step16/release/`), so the route set below stands:

- **The route set:** ExtraPostPlacementOpt +0.115 / +0.033 ns, AltSpreadLogic_high +0.053 / +0.017 and
  ExtraTimingOpt **+0.194 / +0.017** (selected). The route is complete and #818's floor holds.
- **The resource gate** (`pp_resource_gate.py check --endpoint route-1x1`, with both comparisons) exited 1 against
  the previous record, on LUTs alone: 54,002 against 53,461, +541 past the 500 tolerance. The other figures:
  - FF 55,203 (+232) and SLICE 15,849 (unchanged);
  - RAMB36 71 against 74 (a re-baseline recommended), RAMB18 27, DSP 15;
  - WNS 0.194 against the record's 0.334 (a warning, not a failure) and WHS 0.017.
- **Attribution**, on the same directive (ExtraPostPlacementOpt). The candidate before #927 (`c8ff391a`) places
  53,571 LUTs, 54,944 flops and 74 RAMB36; the step-11 head places 53,971, 55,206 and 71. So **#927 brings about +400
  LUTs** (+262 flops, -3 RAMB36), and **the train before it is +110 over the record**, inside the tolerance.
- **By hierarchy**, from the two routed checkpoints (`report_utilization -hierarchical`):

| Where | LUT | FF | RAMB36 | LUTRAM | Its RTL |
|---|---:|---:|---:|---:|---|
| the render master's frame FIFO `u_fcdc`, with its storage | +121 | +192 | **-3** | +128 | #927's `DIST_RAM_P = 1`: 3 RAMB36E1 become 32 RAM32M, and the 192-bit read register leaves the block RAM's output register (24 to 216 flops) |
| `KL_aaf_clock_meter` | +41 | -18 | 0 | 0 | #927: the group reference is loaded through its adder |
| the EDIT window's claim registers | | +96 | | | #927 moves the capture-source word's encode, which is the same function all-fabric; synthesis keeps 96 more bits |
| every other module | about +238 | about -8 | 0 | 0 | unchanged; synthesis and placement of a different netlist (`milan_csr` +338, `KL_render_queue` -213, three transmit arbiters absorbed into the datapath's own cells) |

The TDM capture's `u_tcdc` keeps its storage and flops (34 LUTRAMs, 82 flops, no block RAM).

The render master's crossing is shared, not split-only: every image that carries the render master takes the
distributed storage, the release image and the 1x1/1if split image among them. The 8x8/1if split image carries no
render master.

**The rulings.** All three are on #665 and dated 2026-11-18.

issuecomment-6979461559 accepts a record-only re-baseline at the step-11 head. Its precondition (item 2) stops if a
release FIFO changed primitives. `u_fcdc` did, so the lane stopped there.

issuecomment-6979996755 resolves that stop:

- the change is explicit in #927 and covered by both reviews;
- the distributed-RAM option is not split-only (its item 2 corrects that premise; the paragraph above states it);
- the growth and its attribution go on #640 as debt.

It asks for one check before the record moves. The new crossing must be covered by its timing exceptions and clean in
the CDC report, at the release image and both split images, from the existing routed checkpoints. The check found
CDC-15 rows, so the lane stopped again.

issuecomment-6981065172 resolves that stop:

- "flagged" meant unsafe, unknown, Critical or unconstrained, and none applies;
- CDC-15 is the expected report for this structure, the same class as the capture crossing's;
- no waiver goes into the train, since a waiver changes build inputs, and waiving one crossing but not the other
  would be inconsistent.

**The CDC check** (report_cdc with details, report_timing and report_exceptions on the storage-to-register paths,
report_methodology):

| Image | Covered by an exception | CDC rows on `u_fcdc` | Methodology |
|---|---|---|---|
| release, ExtraTimingOpt (selected) | yes: Asynchronous Clock Groups on every path, slack inf | **CDC-15 (Warning) x192**, clock-enable controlled; CDC-2 x2 and CDC-5 x2 on its pointer synchronizers, as before #927 | nothing on `u_fcdc` |
| 1x1/1if split, ExtraPostPlacementOpt (best) | yes, the same | the same | nothing on `u_fcdc` |
| 8x8/1if split, ExtraPostPlacementOpt (best) | not applicable | none: no render master in this image | nothing on `u_fcdc` |
| the candidate's release image, block RAM (before #927) | | CDC-2 x2 and CDC-5 x2 only; the block RAM holds the crossing inside the primitive | three SYNTH-6 on its block RAMs |

The summary counts every endpoint from the write clock into the read clock as Safe (201 of 201; 0 unsafe, 0 unknown).
CDC-15 is the structure whose read register loads only on `ren_i && !rempty_o`, behind the synchronized write
pointer. So each entry is stable for at least two read-clock synchronizer stages before it is sampled, which is the
safety argument of both reviews. There is no CDC-26 (LUTRAM read/write collision) and nothing Critical. The base's
unchanged capture FIFO `u_tcdc` carries CDC-15 x50 on its own LUTRAM storage in every image, in the shipping release
as well. **This check closes the limit the internal review stated for this crossing.** R863 judged the distributed
RAM's inter-clock arc "from 0 failing endpoints, not read in the report". The report is now read, at the final RTL,
in every image that carries the crossing.

**The re-baseline**, `73272666`, is one record-only commit. `pp_resource_gate.py record … --write` writes the step-11
head's route set as the `route-1x1` record:

- LUT 54,002, FF 55,203 and SLICE 15,849;
- RAMB36 71, RAMB18 27 and DSP 15;
- WNS 0.194 ns and WHS 0.017 ns, with ExtraTimingOpt selected.

The endpoint's provenance note is restated beside it, and every tolerance, floor and ceiling is unchanged. Then:

- `check --endpoint route-1x1` exits 0;
- `check-baseline` and the gate's self-tests exit 0;
- the docs, idiom and hygiene checks pass, and `git diff --check` over the train is empty;
- the 12 split firmware images are hash-equal to the measured ones.

The split images, and so the bench run, do not change. The growth and its attribution are recorded on #640 as area
debt, not as a floor exception.

## Authoritative references

- #665 issuecomment-6939460730 (option B, one train candidate) and issuecomment-6939574513 (freeze, compose once, one
  composition review, one merge).
- #665's rulings of 2026-11-17 and 2026-11-18:
  - issuecomment-6950343235 (THE STEP);
  - issuecomment-6967930396 and issuecomment-6972255348 (the cut, the hot list, THE TRANSMIT's figure and the SRP
    unit);
  - issuecomment-6975966775 (#927 as step 11);
  - issuecomment-6979461559 (the release image's LUT growth), issuecomment-6979996755 (its FIFO stop resolved, the
    corrected premise, the CDC check) and issuecomment-6981065172 (the CDC check's CDC-15 accepted, no waiver).
- Each composed PR's own rulings, cited in its row of the resolution tables: #894's shape, retry-cost and held-egress
  rulings; #895's rulings of 2026-11-14 and 2026-11-15; #897's ruling of 2026-11-15; #923's ruling of 2026-11-16; the
  owner's rule of 2026-11-15 on control-memory ROM as S14 debt.
- [FR_NFR.md 3.4.1](docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing),
  [SPLIT_CONTROL_MEMORY.md](docs/design/SPLIT_CONTROL_MEMORY.md) sections 5 and 13,
  [MAILBOX_SPLIT.md](docs/design/MAILBOX_SPLIT.md), [AREA_BUDGET.md](docs/design/AREA_BUDGET.md),
  [PP_SHADOW_BASELINE_RECIPE.md](docs/testing/PP_SHADOW_BASELINE_RECIPE.md).

## How to get into the same state

```sh
git fetch origin flip-train-1117-p11 dev-soft-core
git checkout --detach origin/flip-train-1117-p11
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
# each frozen head is an ancestor:
for h in d3e61e37 e1ecce20 394612c5 37255683 1a1e6665 81c9a1a0 d06ded5a 0fdfdba7 544fd72c d1aa4c44 0297a19a 66c6edf3; do
  git merge-base --is-ancestor $h HEAD && echo "$h in"; done
git diff --check origin/dev-soft-core...HEAD   # prints nothing
```

## How to validate

```sh
python3 scripts/docs_check.py && python3 scripts/check_py_idiom.py && python3 scripts/check_hygiene.py --check
python3 scripts/gen_toc.py --check && python3 scripts/gen_toc.py --verify-anchors
python3 scripts/docs_inventory.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4 to 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
make -C tb/verilator/milan_dp split split-mutants split-cdc dynmap maprec8 maprec4
make -C tb/verilator/milan_dp_render tdm8render tdm8render-mutants
make -C tb/verilator/aaf_clock_meter all mutants && make -C tb/verilator/mbx all dma-mutants
make -C tb/verilator/avtp_rxmon run
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --self-test
```

Expected result / pass criteria:

- every command exits 0;
- `flip_grade.py --check` at 1x1/1if holds every row by every source at the built 950 us slice, the last queued
  notice 127.31 of 130 ms, ACMP 29.06 of 30 and txL 47.88 of 49;
- `flip_grade.py --check` at 8x8/1if prints THE TRANSMIT's row as HELD (76.81 of 77);
- without `--point`, it fails only on 8x8/2if's rows, the base `cb96336d`'s same eleven findings, reported and not
  held by the owner's decision of 2026-11-12;
- the firmware shards' control campaign catches 826 of 826 plants at this head (825 at step 12's head: 797 before
  step 12, and #947's 28 at its frozen head).

The resource gate: `python3 syn/ooc/pp_resource_gate.py check-baseline` and `--selftest` exit 0. Its
`check --endpoint route-1x1` exits 0 on the release route set, which is the record, and the final head's release
export is byte-identical to it where loaded (see
[Release image](#release-image)).

## Known limitations / out of scope

- **The full CPU budget re-measure is done.** 1x1/1if was measured at `8c5e2b4f` and 8x8/1if at `92de01f7`, whose
  images are the final head's (`CPU-TABLE-8c5e2b4f.md`, `CPU-TABLE-92de01f7.md`). 8x8/2if is reported, not held, and
  was not re-measured.
- **The bench re-check is pending**, on the gating bitstreams of `8c5e2b4f`: 1x1/1if `c7189218…` and 8x8/1if
  `7d903412…`. Their loaded firmware is the final head's. F-G5's (h) #25 and the rest of the gating run are
  re-checked there.
- At 1x1/1if the declaring-outputs arm's paced REMOVE_AUDIO_MAPPINGS that ran no completion measures 30,839 cycles,
  325 us by the rule, over the held 315. It is reported, not held, by #943's design (`record_classes.held`), as at
  `92de01f7`.
- **#946's cause is in the release (all-fabric) image too.** Its AECP is the fabric's, so the fix there is RTL; #947
  leaves the release image byte-identical and hands it to its own ticket.
- **One stream bound to two inputs** (#946's second bench finding) is a different cause: the parser classifies a PDU
  to one context. It needs RTL and its own ticket; #947 does not change it.
- **No CDC waiver.** The render crossing's CDC-15 x192, like the capture crossing's x50, is neither waived nor
  repaired (#665 issuecomment-6981065172, item 3).
- **#495 residue.** The timing findings document is to list the render crossing beside the capture crossing, and
  whether both get a waiver that carries the argument is decided after the flip.
- **#495 residue, for a later ticket (not this train): a link loss published only after a save.** Through a 600 ms
  erase under input that leaves no pass empty, the split's PHY poll publishes a loss only once the save ends.
  - **Why:** every call then owes the store a centisecond's step, and a call whose store took a save's step leaves the
    PHY no room.
  - **Where it is staged:** F-G4 work found it. Its failing test, `Phy.B13APollAPeriodLateTakesItsFrameThroughASave`,
    and a candidate fix are staged as scratch (`round5/fg4/candidate-b.diff`). That fix would change THE STEP's
    order, which #665 ruled on 2026-11-17.
- `AREA_BUDGET.md`'s utilisation table and the #234 findings page still quote the previous record's 53,461 LUT and
  54,971 FF. The re-baseline is record-only, by ruling.
- At 8x8/2if, the base's eleven rows stay over their bounds, by the owner's decision of 2026-11-12.
- 8x8/1if's THE TRANSMIT figure is now 77 ms, a project figure that follows its row. It must stay at most 80.
- The ROM entries at their measured sizes are S14 debt: the fixture 4.5 and the 8x8/1if platform image 2.0.
- 8x8/1if's AltSpreadLogic_high route misses the floor (+0.006 ns); its other two directives meet it.
- A firmware campaign leaves two untracked `dispatch-build/keys/*.yaml` files in its checkout. This predates #935.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
