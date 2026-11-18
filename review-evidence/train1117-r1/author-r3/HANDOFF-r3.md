# HANDOFF, round 3: the flip train's composition (#665), [A794]

**Tip: `4a5bfb32`** on `flip-train-1117` (local; nothing pushed or posted). Step 9, #934 `544fd72c` (head checked;
R853-4 POSITIVE, R854-3 POSITIVE at its ancestor `9aa55d3b`), is composed: merge `8f6fbb84`, idiom fix `4a5bfb32`.
Every frozen head so far is an ancestor of the tip: `d3e61e37`, `e1ecce20`, `394612c5`, `37255683`, `1a1e6665`,
`81c9a1a0`, `d06ded5a`, `0fdfdba7`, `544fd72c`. **Waiting for #936's head** (PR #944), which the manager names in a
later RESUME. Not cut: the cut is the final head's. No STOP condition was met (below).

## Step 9

RESOLUTIONS.md has every conflicted file (8 of #934's 452) and the fix. Three points need the reader:

- **#934's submodule bumps were dropped by my first commit of the merge and restored before any gate.** #934 is the
  only frozen head that moves submodules (`gptp-processor` to `1616fc8f`, `protocol-processor` to `801ef228`). The
  merge staged them, but staging the resolved files with `git add -A` re-staged the lane's old checkouts. A firmware
  shard showed it within a minute (the builder from #934 passes `--clock-accuracy` to the old gPTP generator). The
  unpushed merge commit was amended to #934's two gitlinks and nothing else (`838e2d21` kept as
  `refs/ref/s9-dropped-submodules`; the two trees differ in those two entries alone), the lane's checkouts moved,
  and every run on `838e2d21` was stopped by PID and set aside (receipts/invalid-838e2d21/). No earlier frozen head
  moves a submodule.
- **`mrpdu_grade.py`**: the train holds an MRP timer's row to THE TRANSMIT's bound (#894's held-egress ruling, item
  (b)(i)); #934 times it from its owner's transmit opportunity (#665's ruling of 2026-11-16, Q1). Both kept; they are
  independent (when a row starts, what it is held to), and the auto-merged `rows()` already joins them.
- **The two-placement simulation's expected strings** (`twin_compare.py`) were composed from #929's rows and plant and
  #934's identity and processor fix, then confirmed by the twin's own run: `make twin`, `twin-plants` (15 plants,
  each refused by its words), `twin-maps`, `twin-maps-plants` all pass.

| Check at step 9 | Result |
|---|---|
| Firmware shards 0 to 3 (`8f6fbb84`) | all PASS; the control campaign 797 of 797 |
| Harness self-tests (`8f6fbb84`, again at the tip `4a5bfb32`) | `run.py --self-test` 0 failures; `rows_tiers` 1033/1033; `record_classes` 20/20; load gate PASS and 28/28; flip self-test 616/616; `shape_costs` 25/25; `egress_ledger` 15 mutants; flip check at 1x1/1if PASS |
| All-points flip check | the base's same eleven 8x8/2if findings (reported, not held) |
| `py_idiom` | failed at the merge on two long modules; fixed at `4a5bfb32` (the MRP timers' mutants in their own module, the table identical; six docstrings rewrapped), PASS at the tip |
| Docs, hygiene, C++ idioms, `fw_coverage --check`, `test_ctrl_memory`, the register reference | PASS (the coverage ratchet stands as it is) |
| ROM ledger (`plat_ledger.py --self-test`, the fixture in six arms) | PASS at all four points, 9 of 9 controls, every entry unchanged; the fixture 60.0 in every arm, **72 B of `rom` left** in the answering-ports arm |
| Release image (the AX7101 shipping export, no Vivado) | the tip's equals #934's own: `bios.bin` and the AEM blob byte-identical, `bios.elf` identical with debug sections stripped, the gateware equal outside the top Verilog's comments. #934 brings dev's gateware (the gPTP fixes, the #839 station-MAC hold), so the fit and timing floor are owed at the final head |

## Decision 3: the attribution row for step 9, and the main cut rehearsed

Measured as in round 2 (1x1/1if; arm A's `aecp-largest-notice`, `acmp-notk`, `datapath-events`; the
answering-every-port arm's `notice-burst-5`, `notice-burst-7`, `notice-every-7`; cycles and committed instructions,
the scratch instruction aid proven cycle-neutral in round 2). Cells are cycles / committed instructions (by the rule,
us; **bold** over the statement: the long record 975 us, event.AECP 75, event.MAAP 165, the datapath events 35).

| Head | Step | Image | Largest record: cycles / instr (us) | CPI | Its pass: rom refills / fetch wait | event.AECP | event.MAAP | AS_PATH_CHANGED | AVB_INFO_CHANGED |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `eafe4a16` | 8: #932 | `0af211aa` | 95,392 / 22,202 (**1005**) | 4.297 | 314 / 26,562 | 6,125 / 1,025 (65) | 13,679 / 2,751 (145) | 2,681 / 362 (30) | 3,130 / 366 (35) |
| `8f6fbb84` | 9: #934 | `1fbf3e3d` | 95,482 / 22,202 (**1005**) | 4.301 | 313 / 26,288 | 5,172 / 1,045 (55) | 14,174 / 2,751 (150) | 2,861 / 362 (35) | 3,099 / 366 (35) |
| `d06ded5a` | #931 alone | `600cc8cf` | 92,489 / 22,192 (975) | 4.168 | 310 / 25,742 | 5,873 / 1,036 (65) | 13,685 / 2,751 (145) | 3,131 / 362 (35) | 3,183 / 366 (35) |
| `4a5bfb32 + hot list` | step 9, hot list relearned (scratch) | `b11fc153` | 94,789 / 22,199 (**1000**) | 4.27 | 316 / 26,454 | 5,333 / 1,025 (60) | 14,236 / 2,751 (150) | 2,255 / 362 (25) | 2,303 / 366 (25) |
| `4a5bfb32 + hot list` | step 9, relearned + untraced kept (scratch) | `30df8bcc` | 94,901 / 22,199 (**1000**) | 4.275 | 313 / 26,199 | 5,454 / 1,050 (60) | 14,353 / 2,751 (155) | 3,269 / 362 (35) | 2,591 / 359 (30) |
| `4a5bfb32 + hot list` | step 9, relearned + the record traced (scratch) | `81c42be7` | 93,394 / 22,199 (**985**) | 4.207 | 296 / 25,042 | 5,333 / 1,025 (60) | 14,395 / 2,751 (155) | 2,247 / 362 (25) | 2,388 / 366 (30) |

Where each event was dearest: AS_PATH_CHANGED none/datapath-events; AVB_INFO_CHANGED none/datapath-events; event.AECP
aep/notice-burst-5, aep/notice-burst-7; event.MAAP aep/notice-burst-5, none/acmp-notk

Step 8's and #931's rows are round 2's, for reference; the image column is arm A's ELF sha256. The tip `4a5bfb32`
builds the same firmware as `8f6fbb84` (the fix touches harness Python alone).

### The rehearsal: `ctrl_split_hot.txt` relearned by its recorded procedure

On scratch clones of the tip only; nothing committed. The procedure is the one `ctrl_split_hot.txt`'s header
records: the 1x1/1if split image, arm A, groups `backlog` and `backlog-adp`, each traced by committed PC from 300,000
bus cycles before its first record's commit for 900,000 committed PCs; every function those passes ran, in the order
they first ran it. The exact commands (`<scratch>` is the lane's scratch root; the tools are in receipts/hot/ and
receipts/tools/):

```sh
bin/clone.sh 4a5bfb32 attr/clones/hot-trace   # any clone of the tip; this round's used 8f6fbb84, same firmware
H=attr/hot B=$H/trace-build C=attr/clones/hot-trace
# 1. build the harness's 1x1/1if image, arm A, as run.py builds by default, and run the two groups untraced
python3 -B tools/legs.py build $C $B 1x1 none 1 backlog,backlog-adp
python3 -B tools/legs.py run   $C $B 1x1 none 0 2
# 2. each group again with its committed PCs traced: from 300,000 bus cycles before its first RXC (its first record's
#    commit, just after the group's `composed` mark), for 900,000 committed PCs (BUDGET_TRACE_AFTER, BUDGET_TRACE_PCS)
for g in backlog backlog-adp; do
  first=$(grep -m1 '^RXC ' $B/part0/$g.log | awk '{print $2}')
  (cd $B/gateware && BUDGET_TRACE_AFTER=$((first - 300000)) BUDGET_TRACE_PCS=900000 \
     $B/native/Vsim $B/part0/$g.txt - | grep '^PC ' > $H/$g.pcs)
done
# 3. the order: each PC mapped through the link map to its `.text.<function>` section, named `<stem> <function>` as
#    ctrl_hot.py names an entry, every section in first-run order, backlog's then backlog-adp's
python3 -I $H/order.py $B/image/ctrl_app.map $H/backlog.pcs $H/backlog-adp.pcs > $H/order.txt
# 4. both copies of the hot list (ctrl_split_hot.txt, its header kept and the traces' sha256 added; ctrl_split.ld's
#    block), then the gate's own check
python3 -I $H/apply.py <clone> $H/order.txt $H/backlog.pcs $H/backlog-adp.pcs
python3 sw/firmware/ctrl/test/ctrl_hot.py --check --map $B/image/ctrl_app.map    # in <clone>
```

At the tip the windows trace 162,183 committed PCs (`backlog`, whose run ends inside its 900,000) and 900,000
(`backlog-adp`); every PC falls in a `.text.<function>` section. The learned list has **233 entries** against the
current 206: 57 added (most from #923's, #920's and #934's code: the face's status and polls, the store's step and
marks, the commit's publication), 30 gone. **Among the 30 gone is MSRP's receive path** (`mrp_rx`, `mrpdu_parse`,
`msrp_decode_attr`, `msrp_join_ind` and the rest), which these two windows no longer run at this head; the recorded
procedure takes them out of the hot region. `ctrl_hot.py --check` passes on the image's map and its self-test passes.

Three variants were measured (receipts/hot/diff/*.diff are their hot lists; receipts/attribution/out/ their figures):

- **as recorded** (233 entries);
- **as recorded, the 30 untraced entries kept** at the end of the list in their old order (263);
- **as recorded, with a third window**: arm A's `aecp-largest-notice` traced the same way (300,000 bus cycles before
  its first record's commit, after its `aecp_long` mark; 796,095 PCs), appended in first-run order (270). This is not
  the recorded procedure; it is here because the record is the one row over.

**Findings.**

- **Step 9 adds no work on these paths.** The largest record commits 22,202 instructions, as at step 8, and the four
  events within 20 of step 8's. The record is 95,482 cycles, 1,005 us by the rule, 2,625 cycles past the 92,857 that
  975 holds. The four events are within their statements (event.AECP 55 us, event.MAAP 150, the datapath events 35
  and 35).
- **The recorded procedure alone does not bring the record within 975 at this head**: 94,789 cycles, 1,000 us, 693
  cycles fewer (0.7 %), still 1,932 over. The events stay within: the datapath events improve by a fifth (2,861 to
  2,255 and 3,099 to 2,303 cycles), event.AECP and event.MAAP move by 161 and 62 cycles. Keeping the 30 untraced
  entries gains nothing on the record and costs AS_PATH_CHANGED 1,014 cycles.
- **With the record's own window traced too** (not the recorded procedure) the record is 93,394 cycles, 985 us, 537
  past 975; the events stay within. Its pass refills 296 rom lines against 313 before.
- **The rows, graded with each record figure alone at 1x1/1if** (a scratch copy of the tip, `LONG_RECORD_US` set to
  the rule's figure; receipts/attribution/out/flip-1x1-step9-long-record-*.txt): txL is 49.07 ms at 1,005 us (as
  the tip stands), **49.04 ms at 1,000 (the recorded procedure), still over 49**, and **48.95 ms at 985 (the record
  traced), within**. The last queued notice (137.89 of 140) and ACMP (29.91 of 30) hold at all three.
- **What the final cut needs, by these figures** (the final head's decide; the probe decides nothing): the recorded
  procedure, one of the ruling's two cuts, leaves the record over its statement and txL 0.04 ms over its bound.
  A work cut on the record path would have to remove about 450 committed instructions with the recorded hot list
  (1,932 cycles at its CPI of 4.27), or about 130 with the record's window in the hot list (537 at 4.21). For
  scale, #923's commit gives this record 1,433. A hot list learned with the record's window is a change of the
  recorded procedure, so it would need the owner's ruling first.
- The procedure takes MSRP's receive path out of the hot region at this head (its windows no longer run it); the
  final cut's measurement must cover the SRP rows at every point before that is accepted.

## STOP conditions

None met. Every failure this round was fixed as a composition commit or before any gate: the dropped submodule bumps
(amended before any gate; no gate ran on the wrong tree) and the two long modules (`4a5bfb32`). No test or plant was
removed. No fit or timing-floor check was due; the release image equals #934's own. No design decision is open.

## Notes

- The fixture has 72 B of `rom` left in 60.0 at step 9 (answering-ports arm, 131,000 of 131,072 B): #936, or the
  final cut's hot list (a reorder moves section padding), may take it to 60.5, which the owner's rule makes debt.
- A hot-list change moves every image's placement, so at the final head the cut must be measured at every point the
  harness holds (1x1/1if, 8x8/1if, 8x8/2if) and the ledger re-run; the rehearsal measured 1x1/1if's six groups.
- The all-points flip check fails only on the base's eleven 8x8/2if findings at every head.
- Units' CPU pins are re-applied from their bookings (the host resets task affinity); the host ran oversubscribed at
  times, which slows wall time and moves no simulated cycle.
- Receipts are under `receipts/`, indexed in INDEX.md; files over 200 KB are stubs with their size and sha256.
