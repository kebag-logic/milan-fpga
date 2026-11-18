[A794] The flip train, composed: eleven frozen PRs merged in train order onto dev-soft-core, each conflict resolved keeping both sides, and the composed images measured at the final head

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

**Ready for the composition review at the final head `73272666`** on `flip-train-1117-p11`. All eleven steps are
composed. The CPU service budget passes at every point by its rule:
8x8/2if carries the base's same eleven findings, reported and not held. The split routes meet #818's floor at
1x1/1if and 8x8/1if. Every split firmware image is hash-equal to the measured one, and the confirmation run on the
final RTL is byte-identical.

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
| `b5802de9`, `68c97849`, `41d2bc2b` | The split image's hot list relearned on the final head by its three-window procedure and the ruled filter, then re-traced on each cut | the third trace window (#665 issuecomment-6959600243) and the filter (issuecomment-6967930396) |
| `26f30fea`, `3e1c3dd9`, `08c28218`, `6448e431` | Attempt 2's cuts carried from the step-9 branch by merge: a notice's per-recipient work (`067c319d`) and its include fix (`0bc158a7`); SRP's delivery tells ACMP only a changed Listener presence (`7b3c1c94`); the DMA driver's test T8 (`112ab9b1`) | #665 issuecomment-6967930396 and issuecomment-6972255348, attempt 2 |
| `bf2c1184` | The ROM ledger at the measured sizes: `ctrl_plat` 18,048 B at 1x1/1if and 21,568 B at 8x8/2if; 8x8/1if's platform entry 58.0 | S14 debt |
| `7a536fc5` | The paced class's SET_CONFIGURATION control re-anchored to where that command is the class's dearer member | after the restatement, the plant would move no figure |
| `0cfe1ddc`, `3cdc613b`, `0b054867`, `c8ff391a`, `4374cc27` | The final head's figures restated by the unchanged rule (below) in the tables, `ctrl_loop.h` and the prose; one self-test check and two own-record controls re-anchored to read the restated figures | issuecomment-6972255348, items 2a and 2b |
| `74481d2e` | `4374cc27` carried onto step 11 | it landed on the step-10 candidate after step 11 was merged |
| `05dc1791` | The blank line at the end of `plat_mutants.py` dropped | `git diff --check` over the train |
| `73272666` | The resource gate's release record (`route-1x1`) re-recorded by `pp_resource_gate.py record --write`, and its provenance note restated; the record only, no RTL or firmware | the release image's +541 LUT, accepted as #640 debt (#665 issuecomment-6979461559, issuecomment-6979996755 and issuecomment-6981065172) |

**The rule for figures.** A figure that two PRs both restate is carried at the side that moved it, the larger where
both did. It is restated from the composed image after the last merge, by its tool or by the rule: stated cost =
measurement + 5 %, rounded up to 5 us, never below the measurement.

**Composed figures at the final head.** The CPU service budget, by `flip_grade.py --check --point`:

| Point | Verdict | The tightest rows |
|---|---|---|
| 1x1/1if | **PASS** | ACMP 29.93 of 30 ms, txL 48.89 of 49, the last queued notice 137.97 of 140; the load 0.522 of 0.70; the paced record 310 of 310 us |
| 8x8/1if | **PASS** over every arm, on the image that carries the SRP unit at 375 us | the SRP record 35,547 cycles, within 375 us; the load 0.744 of 0.75; THE TRANSMIT's row 76.81 ms of 77; 119 join intervals, 187.15 to 190.41 ms (181 to 239); no budget miss but the seven `backlog-owed` egress-hold rows the harness README ledgers at every point |
| 8x8/2if | the base's same eleven findings, no twelfth (owner's decision of 2026-11-12) | THE TRANSMIT's row 104.69 of 105 ms; the notice item 270 of 275 us; the paced record 585 of 595; the load 0.799 |

**Restated at the final head**, by the rule:

- 1x1/1if: the paced record 310 us.
- 8x8/1if:
  - the polls base 300 and the apply 375;
  - the MAAP record 180 and the ADP record 135;
  - the SRP record 375, with `CTRL_LOOP_SRP_UNIT_US` 375 (the unit follows its record);
  - `CTRL_LOOP_TX_MS` 77, which is at most 80, so `SRP_REDECLARE_CS` stays 8 cs.
- 8x8/2if: the MAAP record 160, a pass's events' fixed part 45 and AECP's timer event 120.
- The ROM: the size fixture 60.5 (S14 debt 4.5) and the 8x8/1if platform image 58.0 (S14 debt 2.0).

**The split routes on the final RTL** (the AX7101 split route, three placement directives; #818's floor is WNS >=
+0.030 ns and WHS >= 0 at every signoff corner):

| Point | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high | Floor |
|---|---|---|---|---|
| 1x1/1if | **+0.141 / +0.033** | +0.054 / +0.036 | +0.031 / +0.036 | met on all three |
| 8x8/1if | **+0.073 / +0.034** | +0.064 / +0.027 | +0.006 / +0.036 | met on its best of three |

Before step 11, 8x8/1if missed on all three directives (best +0.005 ns). The worst path ran from the EDIT window's
request to the AAF map's claim enables, and #927 cuts it: the datapath clock's worst is now +0.835 to +0.989 ns. The
1x1/1if image falls from 83 to 80 block RAM tiles. The render master's crossing is shared, not split-only, so the
release image takes the distributed storage too (74 to 71 RAMB36).

**The images and the confirmation.** Every split firmware image of the final head is hash-equal to the measured one
(`ctrl_app.elf`, sha256 prefix):

| Point | Arm A | answering-every-port | answering-ports | valid-destinations |
|---|---|---|---|---|
| 1x1/1if | `55484254` | `4e7b53c7` | `6971e95c` | `8ca50418` |
| 8x8/1if | `175418f4` | `ea87356a` | `3c15ec34` | `e764b2fe` |
| 8x8/2if | `ba343fd4` | `f64be15e` | `8c9fe28b` | `cf299386` |

The confirmation run on step 11's RTL covered seven groups:

- 8x8/1if: `srp-talker-held`, and `aecp`, `aecp-largest-notice` and `aecp-fanout` of the answering-ports arm;
- 1x1/1if: `aecp-largest-notice` and `aecp-fanout`;
- 8x8/2if: `aecp-fanout`.

Its diff against the measured receipts is **empty**: the same stimulus, byte-identical logs (761,187 SPAN lines in
`srp-talker-held` alone) and every measured figure equal. So the CPU rows carry to the final head.

**`cdc_pair_fifo`.** #927 reorders the default branch's storage block. It is behaviour-identical by reading, and a
bounded equivalence proof finds no counterexample:

- the proof is from the zero state, with both clocks free, over 30 steps;
- it is complete at every depth a default-branch instance takes: 4, 8 and 16.

A standalone synthesis maps the module identically at three of the four parameter sets a default-branch instance
takes. At 48 x 16 (the I2S playback's FIFO, in none of these images) it uses 2 fewer LUTs. Only the render master's `u_fcdc` takes `DIST_RAM_P = 1`
(the next section).

### Release image

The all-fabric AX7101 image at the final head, by the baseline recipe:

- **The route set:** ExtraPostPlacementOpt +0.115 / +0.033 ns, AltSpreadLogic_high +0.053 / +0.017 and
  ExtraTimingOpt **+0.194 / +0.017** (selected). The route is complete and #818's floor holds.
- **The resource gate** (`pp_resource_gate.py check --endpoint route-1x1`, with both comparisons) exited 1 against
  the previous record, on LUTs alone: 54,002 against 53,461, +541 past the 500 tolerance. The other figures:
  - FF 55,203 (+232) and SLICE 15,849 (unchanged);
  - RAMB36 71 against 74 (a re-baseline recommended), RAMB18 27, DSP 15;
  - WNS 0.194 against the record's 0.334 (a warning, not a failure) and WHS 0.017.
- **Attribution**, on the same directive (ExtraPostPlacementOpt). The candidate before #927 (`c8ff391a`) places
  53,571 LUTs, 54,944 flops and 74 RAMB36; the final head places 53,971, 55,206 and 71. So **#927 brings about +400
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

issuecomment-6979461559 accepts a record-only re-baseline at the final head. Its precondition (item 2) stops if a
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

**The re-baseline**, `73272666`, is one record-only commit. `pp_resource_gate.py record … --write` writes the final
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
for h in d3e61e37 e1ecce20 394612c5 37255683 1a1e6665 81c9a1a0 d06ded5a 0fdfdba7 544fd72c d1aa4c44 0297a19a; do
  git merge-base --is-ancestor $h HEAD && echo "$h in"; done
git diff --check origin/dev-soft-core...HEAD   # prints nothing
```

## How to validate

```sh
python3 scripts/docs_check.py && python3 scripts/check_py_idiom.py && python3 scripts/check_hygiene.py --check
python3 scripts/gen_toc.py --check && python3 scripts/gen_toc.py --verify-anchors
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4 to 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
make -C tb/verilator/milan_dp split split-mutants split-cdc dynmap maprec8 maprec4
make -C tb/verilator/milan_dp_render tdm8render tdm8render-mutants
make -C tb/verilator/aaf_clock_meter all mutants && make -C tb/verilator/mbx all dma-mutants
```

Expected result / pass criteria:

- every command exits 0;
- `flip_grade.py --check` at 8x8/1if prints THE TRANSMIT's row as HELD (76.81 of 77);
- without `--point`, it fails only on 8x8/2if's rows, the base `cb96336d`'s same eleven findings, reported and not
  held by the owner's decision of 2026-11-12;
- the firmware shards catch 797 of 797 plants.

The resource gate: `python3 syn/ooc/pp_resource_gate.py check-baseline` and `--selftest` exit 0. Its
`check --endpoint route-1x1` exits 0 on the final head's release route set, which is the record (see
[Release image](#release-image)).

## Known limitations / out of scope

- **No CDC waiver.** The render crossing's CDC-15 x192, like the capture crossing's x50, is neither waived nor
  repaired (#665 issuecomment-6981065172, item 3).
- **#495 residue.** The timing findings document is to list the render crossing beside the capture crossing, and
  whether both get a waiver that carries the argument is decided after the flip.
- `AREA_BUDGET.md`'s utilisation table and the #234 findings page still quote the previous record's 53,461 LUT and
  54,971 FF. The re-baseline is record-only, by ruling.
- At 8x8/2if, the base's eleven rows stay over their bounds, by the owner's decision of 2026-11-12.
- 8x8/1if's THE TRANSMIT figure is now 77 ms, a project figure that follows its row. It must stay at most 80.
- The ROM entries at their measured sizes are S14 debt: the fixture 4.5 and the 8x8/1if platform image 2.0.
- 8x8/1if's AltSpreadLogic_high route misses the floor (+0.006 ns); its other two directives meet it.
- The release export comparison (`bios.bin` and the AEM blob byte-identical) was last made at step 9. Here the
  release image is measured by its route and resource gate.
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
