# HANDOFF round 7: lane 897 (A776), the sync onto dev-soft-core 70f4056f

Status: **REVIEW READY** (2026-11-16, started 03:40 CET), posted once on #897, issuecomment-6928240632 (`REVIEW-READY-COMMENT.md`). No STOP condition holds.
Assignment: the manager's round 7. Round 6's bar was met at `b15da60a` (R833-6 POSITIVE, issuecomment-6897027049, with R834's ancestor). PR #901 merged into `dev-soft-core` as `70f4056f`, after #902 (`659d7687`).
Base: `b15da60a`. The merge base with `dev-soft-core` is `234bc149`. Nothing is pushed; the manager pushes.

## 1. The merge

`git merge --no-ff --no-commit 70f4056f`. Eight files conflicted: the six the assignment names, plus `load_grade.py` and `run.py`.

| File | Hunks | Resolution | Why |
|---|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py` | 1, the arms' comment | this branch's description of the answering-ports arm (its `path` port is `arm_path.py`'s, #897), and #901's `valid-destinations` sentence (#895), at #901's width | both arms exist in the merged `VARIANTS`; the auto-merged code carries both sides' diffs |
| `tb/verilator/ctrl_service_budget/build.py` | none, the module limit | the module docstring's second paragraph rewrapped from about 75 to 118 columns, the same words (checked word for word), 11 lines to 7 | the composition was 1,001 lines, past the 1,000-line module limit (`check_py_idiom.py`, long module 10 of 10); round 2 did the same in this file |
| `tb/verilator/ctrl_service_budget/run.py` | 1, `--variant`'s help | the four ports' wording (this branch) and `valid-destinations` (#895) | both arms |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 2, `STATED_US` and `STATED_US_DONOR` with their comments | #901's tables and comments, with `record.aecp` at 1x1/1if this branch's 245 in both columns; both histories kept, and a sentence for the composition | each cost is the one of the side that moved it from the merge base `234bc149`, the larger where both did (#895's composition ruling, item 2, as #901 applied it). This branch moved only `record.aecp` at 1x1/1if (235 -> 245); #901 moved MAAP's record, AECP's timer slot, the events' fixed part, the polls' base and others. A table diff against `70f4056f` shows that cell alone differs |
| `sw/litex/ctrl_memory.py` | 3: the comment, the 8x8/2if entry's `ctrl_plat`, its reason | the comment this branch's (it carries #901's); `ctrl_plat` 20,352 B, the composed image's as `plat_ledger.py` measures it; the reason both rulings', with the composed 992 B past 60.0 | the ledger holds the built image's `ctrl_plat`, and the entry stays 60.5 |
| `sw/firmware/gtest/coverage.ratchet` | 1, `ctrl_plat.c`'s row (132/132 here, 134/134 on #901, 133/133 at the base) | rewritten by its tool on the composed tree: `fw_coverage.py --write --jobs 8`, as CI checks it (no `--lwsrp`), then `--check` | never by hand |
| `sw/firmware/ctrl/plat/README.md` | 3 | #901's SRP bullet and this branch's AECP bullet (the face reads GET_AS_PATH); the 8x8/2if image's two lines with all three changes and the composed figures | both sides' behaviour |
| `docs/reference/FR_NFR.md` | 1, 3.4.1's paced paragraph | #901's paragraph (9 ms pace, 900 us, the 140 ms bound), with the paced class at 305 us since GET_AS_PATH's read, a sentence for the composition, and the final pass's GET_AS_PATH guard | both |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | 12 | each "current" line states the composed figures. Both lanes' history is kept: #901's paragraphs and subsections, then this branch's (marked as round 6's head's), then a new subsection "GET_AS_PATH on SRP's Talker declarations (#897)" and section 5's composed table | both, in the order the lanes merged (#902, #901, #898) |

**Auto-merged files carry each side exactly** (`merge_sides.py 234bc149 b15da60a 70f4056f WORKTREE`, `receipts/sync/`). For every file either side changed, the merge's diff from the other parent is that side's own diff. The exceptions are the nine hand-resolved files above, and `ctrl_memory_ledger.py` and `test_ctrl_memory.py`. Those two equal `70f4056f`'s byte for byte, because this branch's change to them was #901's `8238156d` text, which git merged once.

## 2. The composed image

Commits after the merge: `4b9dc6ce` (the two restatements: `CTRL_LOOP_TX_MS` 35 at 1x1/1if; the size fixture's 8x8/2if entry 59.5) and `59c934c6` (section 13's composition subsection, as measured).

**The composed images** (`plat_ledger.py --self-test`, 7 of 7 controls, and the size fixture at the four points), against #901's head:

| Image | 1x1/1if | 1x1/2if | 8x8/1if | 8x8/2if |
|---|---|---|---|---|
| size fixture | 112,744 B (+320), 41.5 | 114,304 B (+320), 42.5 | 125,408 B (+320), 55.0 | 126,928 B (+320), 59.0, its entry 59.5 |
| platform | 117,800 B (+312), 43.0 | 119,384 B (+312), 44.0 | 130,504 B (+304), 56.0 | 132,064 B (+312), 60.5, 1,056 B left in 133,120 |
| harness arms on the fixture (arm A / B / every-port / valid-destinations) | 112,744 / 113,232 / 113,068 / 112,872 B, 41.5 | | | 126,928 / 127,416 / 127,252 / 127,096 B, 59.0 / 59.5 / 59.5 / 59.5 |

- `sram` and `ctrl_plat` are #901's at every point.
- Every writable symbol has the address and size it has at `70f4056f` (#909).
- The platform's 8x8/2if image is 992 B past 60.0 and within the 133,120 B ruling item 3 grades the composed #901 and #898 image against.
- The three harness arms on the 8x8/2if fixture need 59.5, so that entry is raised to 59.5 as named debt owed to S14, by the owner's decision of 2026-11-15 (#665 issuecomment-6892332745). `test_ctrl_memory.py` holds the new entry and refuses 60.0.

**The tables and the rows.** At the composed tables every 1x1/1if row holds by every source at the built design, the slice rule's 900 us (tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2):

| R4 (20) | R4L (238) | ACMP (30) | ADP (30) | MAAP (30) | First (20) | R5 (90) | R6 (90) | Last (140) | tx (49) | txL (49) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 13.40 | 203.57 | 29.82 | 28.05 | 28.15 | 14.73 | 76.10 | 73.61 | 136.99 | 34.20 | 48.77 |

- The load is 0.519 at the pin and 0.516 with tsn-c-stack #32, against 0.70.
- The pace by its rule stays 9 ms.
- The slice rule holds 6 of 420 designs and chooses the built one (least margin +0.0047).
- The tx row at 1x1/1if, 34.20 ms, was over the 34 `CTRL_LOOP_TX_MS` stated. By #895's rule (issuecomment-6895331865, item 1) the figure is that row rounded up, 35. A withdrawn Talker's hold-off adds `(CTRL_LOOP_TX_MS + 9) / 10` cs, 4 at both 34 and 35, so it stays 2,023 cs, and all 12 images are byte-identical at either figure. The self-tests' plants move with it (flip 585 of 585, `rows_tiers` 1,033 of 1,033).

**Measured again on the composed image** (every group of every arm at both points: arm A, 96 groups at 1x1/1if and 94 at 8x8/2if; the `answering-every-port` arm, 16; `valid-destinations`, 2; arm B's three):
- Every leg exits 0 with no refusal. The only misses are the seven held-egress `backlog-owed` paths at each point (tsn-c-stack #26), and two arm B `aecp-largest-notice` passes over THE SHARE at 8x8/2if (#894's reported condition).
- The joins are 188.156 to 190.104 ms at 1x1/1if (359) and 185.525 to 190.193 ms at 8x8/2if (750), all within 181 to 239.
- **Every stated 1x1/1if cost holds by the rule.** The nearest are AECP's timer slot at 75 us of 75, and a grandmaster event, AVB_INFO_CHANGED and AMAP_LIVE_WRITE each at its statement. Only two class lines exceed an ordinary statement, each held by its class: the largest legal notice at 360 of 365 us, and the paced SET_CONFIGURATION at 295 of 305. **No cost is restated**, so the rows above stand.
- **`record_classes.py` over every leg at both points: RESULT PASS:**

  | Class | 1x1/1if | 8x8/2if |
  |---|---|---|
  | long | 910 of 975 us | 1,335 of 1,650 |
  | ordinary | 220 of 245 | 200 of 265 |
  | paced | 295 of 305 | 580 of 595 |

  GET_AS_PATH's answered read, held as an ordinary record, is 16,500 cycles (175 us) at 1x1/1if, and 14,521 and 14,318 (155 us) at 8x8/2if. Each response is SUCCESS with its eight entries, control_data_length 80. Arm A's refused response is 11,308 cycles.
- **8x8/2if, reported:** AMAP_LIVE_WRITE is 28.82 us, 35 by the rule, over the 30 stated there. It is not restated (Known limitations).

No STOP condition holds: the last queued notice is 136.99 ms within 140, every 1x1/1if row is within its bound, and the load is 0.519 against 0.70.

Receipts: `receipts/rom/` (both trees' images, the data layout, the tx35 identity), `receipts/ledger/`, `receipts/harness/measure/` (every leg's summary, the three 59.0 refusals, every build's image), `receipts/records/` (the class grading, GET_AS_PATH's records), `receipts/compare/` (the 1x1/1if compare, the 8x8 datapath events).

## 3. Gates

One pass at `59c934c6` (`final_pass7.sh`, `gate_queue7.sh`, `lane_gates7.sh`), each part on its own fresh clean clone. It ran 25 units; the 15:40 power cycle cut 5 of them (the two `valid-destinations` identity legs and the three docs-gates jobs), re-run from scratch, and `publication-census` was re-run alone (below).

| Gate | Result |
|---|---|
| `rtl-fast`: the firmware jobs | the firmware unit suites PASS; `fw_coverage.py --check` PASS (39 files); the AECP campaign 308 caught, none missed, the nine `face-as-path-*` plants by name; the control campaign 717 of 717, `plat-as-path-unavailable` among them; the SRP campaigns 421 caught; `ctrl_boundary` PASS at both builders |
| `rtl-fast`: every other job and the docs workflow, every `run:` step | every job and `run:` step: 108 ran, 94 not run with a stated reason, 0 bad, and the 19 job clones have no tracked change afterwards. `publication-census`'s step 12 timed out once (sv2v's 900 s, on the shared pool at the host's heaviest load) and passes on its own booked range (0 of 57 rules unproven) |
| the Verilator suites that build the split firmware, each alone as `run_all_suites.sh` runs it | `milan_dp` PASS (4,083 s of its 4,800), `mbx` PASS, `milan_dp_gm_steps` PASS, each with `suite_tally.py --verdict` clean |
| lane gates (45) | 39 at 0; the 4 that exit 1 by design, each refusing the rows it refused at round 6 (8x8/2if's ten; as built at 1x1/1if R4 and last); and the `milan_dp` twin and its plants, identical at `dev-soft-core` `70f4056f` (below). Among the 39: the harness self-test (0 failures, every mutant), `record_classes.py --selftest` (14 of 14 and the port check), `rows_tiers` 1,033 of 1,033, flip 585 of 585, load 26 of 26; `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check`, `tier_grid.py` (900 us); `plat_ledger.py`, the fixtures and `test_ctrl_memory.py`; `docs_check` 0 findings, the em-dash gate against `70f4056f` and `234bc149`, both idiom ratchets; the split boot at every point with its controls and plants; `test_builder.py --require-rv32`; the NVM gate; `behave`; the hooks self-test |
| CPU budget harness legs, one a point and arm (8) | every leg rc 0; every ELF byte-identical to its measurement build |

**A red already on `dev-soft-core`:** the `milan_dp` twin (`make -C tb/verilator/milan_dp twin`, a lane gate no workflow runs) and its plants exit 2. Its owed row `split-talker-failed` still expects the split's Talker Failed for both sources from boot, never withdrawn, the behaviour before #895, and the split now declares and withdraws as #895 makes it. The finding and every plant's verdict are identical at #901's merged head `70f4056f` on a clean clone; the composition does not cause it. For #895's lane (#901).

## 4. Notes

- **Host interruptions.** 15:40 (a power cycle for the memory upgrade), 18:46 (a crash) and 19:39 (maintenance). Every unit without a recorded rc was treated as cut: its half-written output removed, then re-run. No unit's result is taken from a cut run.
- **`publication-census` re-run.** In the pass its step 12 hit sv2v's 900 s timeout. That run was on the shared pool at the host's heaviest load, so it was a contention timeout and not a census verdict. This branch's tree has no `hdl/`, `protocol-processor`, `gptp-processor` or `third_party` difference from `70f4056f`. The first run's logs are kept (`receipts/gates/census-first-run/`). The re-run alone on a booked range was cut at 19:39 after 160 passed checks, and its third run is the result above.
- **8x8/2if, reported, not restated:** AMAP_LIVE_WRITE at 28.82 us, 35 by the rule, against the 30 stated there. A restated 8x8/2if cost moves that point's tx row, and so `CTRL_LOOP_TX_MS` and the hold-off at two interfaces, a firmware change outside the sync.
- **The twin's red** is `dev-soft-core`'s own, identical at `70f4056f` (`receipts/twin/`).
- **Not done here, by the assignment:** the 65-suite sweep, which runs in the manager's merge candidate.
- **Nothing pushed.** One comment, the REVIEW READY, is posted on #897.
