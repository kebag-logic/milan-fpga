[R712] NEGATIVE - exact head a3f23bbabdd9800177224432361fcd41b53bf882

# R712-4: external review of PR #810 (#665 S2b), round 14

Head `a3f23bbabdd9800177224432361fcd41b53bf882`, tree `677a44180c838c11ce0852c618cee0b09a63b2be`. The source base is `dev-soft-core` `a68536fa`. The delta reviewed is `4f58214f..a3f23bba`, 11 commits. It is judged against the round 14 assignment (#665 issuecomment-6589337173) and my round 13 findings (R712-3, PR #810 issuecomment-6589327842).

## Verdict in one paragraph

Round 14 fixes R712-3-F1, the round 13 MAJOR, at its cause. The loop now has an age limit (`ctrl_loop.c:160-168`). The stated worst case of a save, 12,110 ms at 8x8/2if and 4,070 ms at 1x1, is derived from the age limit, the step count and the tick. I recomputed S = 370 and S = 102 from the store's constants, and the counts agree with the author's per-kind step receipt. The bound holds in every measured leg. The control with the age limit removed is caught. Every round 13 MINOR is resolved, and both of my residues were applied word for word.

The verdict is NEGATIVE on two MINORs:

- **F1.** The reason given for choosing N = 2 is that "no aged step lands among a window's records", with a least margin of 0.77 ms. That holds only for windows that open with the step's age at zero, which is how every staged window opens. I ran 19 windows at the image the head builds, each preceded by grandmaster changes. This is an event source the PR itself treats as in-contract and unrated. In 10 of the 19, an aged step was taken among the window's records. Against the same input without the age limit, each lengthened the last SRP record by 0.69 to 0.78 ms (one read-back step) in seven of eight comparisons, and by 1.53 ms in the eighth. The tightest result was 17.775 ms against 18 ms, a margin of 0.225 ms, not 0.77 ms. No row went over its bound and no pass went over the share. So what is wrong is the measured basis and the published margin, not a row. This touches every lens.
- **F2.** The test of the age limit cannot tell centiseconds from dispatches. A plant that counts dispatch calls passes the whole host gate (Tests).

The owner's 0.5 s (#823) is not claimed by this PR. The figures are below.

## Method

**Context, in order.** I read:

- AGENTS.md and CONTRIBUTING.md (by reference);
- #665's body, with its 2026-10-31 owner decisions;
- the S2b frozen acceptance (issuecomment-6414297191);
- the round 13 and round 14 assignments;
- the author's TAKEN and REVIEW READY comments on #665;
- the PR body;
- the full diff `4f58214f..a3f23bba`, and `21d0e0f6..a3f23bba` separately.

The second diff shows that after the measured legs' head `21d0e0f6`, only comments, docs and one test plant's anchor (`srp_mutants.py`) changed. No compiled code changed.

I read the prior findings, R712-3 and R711-3, only after my own pass over the diff. I did not read any other reviewer's report for this round.

**The evidence packet.** This is `review-evidence/665s2b-r1` at `73deb391c6b81dfa26040c565dcf988cb3519e1a`, directory `author-r14`.

- 490 files listed, 490 present, 0 bad, 0 missing, 0 unlisted, 33 path-redacted (`receipts/packet_manifest_author_r14.txt`).
- The packet commit has no cryptographic signature (`%G?` = N). Integrity here means the manifest's hashes.
- The `results.json.gz` files were not archived, as disclosed. I relied on the archived `table.md`, `run.log`, `analysis/` and gate logs, and on my own runs.

**Recomputed, not taken on trust:**

- S and the stated worst case, from the store's constants (`scripts/bound_check.py`, `receipts/bound_check.txt`).
- The probe images. I built them with the harness's own build at the head, with Verilator 5.050 at the pinned path: `Verilator 5.050 2026-07-01 rev v5.050`.
  - The image without the plant is `a7d77f31…`, the sha256 of N-A8's.
  - The image with the age limit's plant is `29713a0a…`, AGE-A8's (`receipts/probe-window/images.txt`).
- Two staged windows, run myself at that image:
  - `backlog-adp@blank-0` gives the last SRP record at 17.23372 ms, the author's tightest row (N-A8 `table.md`: 17.234).
  - `backlog-adp@verify-7` gives 16.519 ms.

  The author's legs therefore reproduce exactly here.
- The full host firmware gate at the head, and the same gate with my plant (F2).

**Probes.** All ran in scratch copies, 8x8/2if, arm A. The patches are `receipts/probe-window/probe-groups*.patch`, and the runner scripts are `scripts/probe_*.sh`. Each probe is a staged `backlog-adp` save window preceded by `flood gm 1`, which is the testbench's "grandmaster change as every pass starts", the source `save-starved` uses. The flood ends as the window opens. Three sets:

- **verify-7 (a0-a7):** the flood for 20 to 46.25 ms before the window. The window opens that much later.
- **blank-0 (b0-b3):** the same, with floods of 20 to 42.5 ms.
- **blank-0 at its staged instant (c0-c6):** the flood fills the last 12 to 30 ms before the staged open time, so the window opens exactly where the author's tightest one does.

The same groups ran on the age-limit-removed image (the "ageless" control) where a comparison was needed.

`window_probe.py` reads the harness's own grade of each group and its `STEPPASS` lines. Every probe group was graded with 0 refusals: population, phase guard and owner checks all passed.

## Findings

### R712-4-F1 - MINOR - Conformance, RTL (architecture), Robustness, Tests, Docs - the basis for N = 2 and the published least margin assume a window opens with the step's age at zero

**Where:**

- `sw/firmware/ctrl/loop/ctrl_loop.h:146-150`: "in every window the budget stages … no more than two centiseconds are dispatched between two passes that carry a step, so no aged step lands among a window's records, the least of whose margins (0.77 ms) is below a step (0.96 ms)".
- `docs/design/SPLIT_CONTROL_MEMORY.md:1440-1443` ("with the limit at two no aged step is taken in a window"), `:1589` ("the least margin … 0.77 ms") and `:1593` ("The heaviest window holds a step off for at most 26.4 ms … about 3.6 ms short of the third").
- The PR body: Status (`:18`), item 1 (`:38`), `:128`, and Known limitations (`:352`, `:354`).
- REVIEW READY, acceptance 1 and Open risks.

**Authority:**

- Round 14 item 1: "Choose N, and keep every row and every pass within its bound. The least margin … is below the longest step … so measure this; do not assume it."
- AGENTS.md section 6, Robustness: invalid ordering, backpressure.

**Evidence** (`receipts/probe-window/summary-*.txt`, `AGED-verify/`, `BLANK/`, `INSIDE/` and the ageless `rg-AGELESS/`, `BLANKLESS/`, `INSIDELESS/`):

- **The age is not reset when a window opens.** It counts centiseconds dispatched since the step last ran or owed nothing (`ctrl_loop.c:111,162,182`). Every staged window opens after `wait quiet` and `wait events 0` (`scenario.OPEN_WINDOW`), with an empty pass just before it, so the age is 0. Input that keeps passes non-empty up to the window carries an age of 1 or 2 into it. One tick inside the window then makes the next pass an aged step's, among the records.
- **Aged steps did land among the records.** This happened in 10 of 19 flood-preceded windows:
  - verify-7 a0, a4, a5, a6 and a7, at +1.16, +15.90, +12.35, +8.81 and +6.05 ms into the window;
  - blank b0 and b1, at +10.55 and +4.42 ms;
  - blank-0-at-its-instant c0 to c2, at +10.46 to +10.52 ms.

  In the other nine, the step came just before the window.
- **Each one lengthens the last SRP record, usually by about one read-back step.** The same flood on the ageless image (no aged pass) gives the comparison:

  | Window | Last SRP, ms, age limit | Last SRP, ms, ageless | Difference, ms |
  |---|---:|---:|---:|
  | verify a0 | 17.599 | 16.909 | +0.69 |
  | verify a4 | 17.651 | 16.885 | +0.77 |
  | verify a5 | 17.512 | 16.743 | +0.77 |
  | verify a6 | 16.938 | 16.210 | +0.73 |
  | verify a7 | 17.775 | 16.245 | +1.53 |
  | blank b0 | 17.026 | 16.252 | +0.77 |
  | blank b1 | 17.276 | 16.586 | +0.69 |
  | blank c1 | 17.329 | 16.549 | +0.78 |

  The ageless legs are in `rg-AGELESS/`, `AGELESS-verify/`, `BLANKLESS/` and `INSIDELESS/`. verify-a7 reached **17.775 ms against 18 ms, a margin of 0.225 ms**, 1.53 ms more than the same input without the age limit. That is below the 0.77 ms the PR publishes as the least margin.
- **No row and no pass went over** in any probe: 0 budget misses and 0 passes over the share in every probe leg (`run.log` tails). The 17.234 ms worst case at blank-0 comes from a step taken just before the window. An aged step needs three ticks with no empty pass before it, so it cannot fall in the same place. In the c-set the aged step replaced that step, and the row reached only 17.357 ms. I found no combination over 18 ms, and I did not prove that none exists.
- **The "3.6 ms" margin is the sampled phases' margin.** The author's own `stepgaps-N-A8.txt` grows by about 1.25 ms a tick phase: verify-0 17.55 ms to verify-7 26.36 ms. The window's own drain is about 17.4 to 17.6 ms, and the eight phases stop at 8.75 ms of the 10 ms tick. A window opening just before a tick has its third tick about 20 ms in, not 21.25 ms. So the margin across all phases is about 20 − 17.6 ≈ 2.4 ms, not 3.6 ms. This is a derivation from the author's receipt. I did not run it.

**Impact:**

- The code comment that justifies `CTRL_LOOP_STEP_AGE` and the design page state a property that a reachable input order breaks.
- The published least margin overstates the protection of the tightest row by more than 0.5 ms.
- A later change can lengthen the drain or slow the read-back step. The design page itself warns that such a change "must measure it again". That re-measurement would then run on windows that cannot show the effect.
- The step's worst case is to be inherited by #823's writer, so this basis is the one the next lane reuses.

**Required outcome:**

1. The rows' fit with N = 2 is established for a window entered with the step's age at its limit, as well as at zero. For example, a staged group or groups enter the heaviest window with the age at 1 and at 2. The tick phase must be covered across the whole tick, not 0 to 8.75 ms only. Each row must be graded against its bound. If one does not fit, N or the mechanism changes, or the lane STOPs with the residual as item 1 requires.
2. The rationale at `ctrl_loop.h:146-150` and `SPLIT_CONTROL_MEMORY.md:1440-1443,1589,1593`, the PR body and the acceptance row state what was measured, with the least margin under that load (at most 0.225 ms by this review's probe, or whatever the new groups measure). They should not say that no aged step lands in a window.
3. The "about 3.6 ms" margin is either restated over the whole tick or scoped to the eight sampled phases.

**Verification:** the new groups run in both arms, with each row and its margin printed. A plant that keeps the age at its limit going into the window shows the aged pass among the window's records, and the row's added time, by name. The text cites those receipts.

### R712-4-F2 - MINOR - Tests - the age limit's test does not tell centiseconds from dispatches

**Where:** `sw/firmware/ctrl/test/test_port_loop.cpp:852` (`Loop.L13AnAgedStepIsAPassOfItsOwn`), and the ten planted defects in `loop_step_mutants.py`.

**Authority:**

- `ctrl_loop.h:99-106` and `SPLIT_CONTROL_MEMORY.md:1436` define the age as "the centiseconds the loop has dispatched".
- The stated worst case (`nvm_store.h:16-28`, `save_window.bound_ms`) is counted in ticks.
- One dispatch carries up to `CTRL_LOOP_TICKS_PER_PASS` = 16 centiseconds when TICK records coalesce (`MAILBOX_SPLIT.md:150,539`).
- AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect, and boundary behaviour is covered.

**Evidence:** `receipts/fw-plant/`. The plant `l->step_age += count != 0u;` counts one per dispatch call (`ctrl_loop.c:111`, patch `step-age-counts-dispatches.patch`). With it:

- `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --jobs 2` passes: `test_ctrl_firmware: PASS`, rc 0. The port arm reports "checks: 36 failures: 0", the same as the baseline run at the head.
- The plant's own `test_port_loop --gtest_filter='Loop.L13*'` passes.
- Every L13 pass dispatches exactly one centisecond (`mbx_model_advance_ms(&model, MBX_TICK_MS)` before each pass).

**Impact:** a loop that counted dispatches would hold an aged step off for up to 16 times longer after a coalesced tick backlog, which is the case after a full event ring. That would put a save past its stated worst case, and no gate would see it. The harness's `save-starved` posts one TICK a centisecond, so it would not see it either.

**Required outcome:** a test in which one dispatch carries two or more centiseconds, through one TICK record with a count of 2 or more, or through centiseconds owed past a pass's tick budget. In it, the age limit is reached by centiseconds, not by passes. A planted defect that counts dispatches fails it by name.

**Verification:** the plant above, added to `loop_step_mutants.py`, is caught by `Loop.L13…` or a new named test.

### RESIDUE-1 (wording only; no verdict effect) - `docs/design/SPLIT_CONTROL_MEMORY.md:1609` - the S bullet says the same thing twice

Both reviews' exact texts were appended, so the bullet now states twice that the slope is arm A's at both ends.

**Exact fix:** delete the final sentence, "The slope is arm A's at both ends, from section 13's arm A 1x1/1if figure, since the 8x8/1if point ran in arm A only; the 1x1/1if column below is the worst of the arms." Then change "not the worst-of-arms column below." to "not the 1x1/1if column below, which is the worst of the arms."

### RESIDUE-2 (wording only; no verdict effect) - `docs/design/SPLIT_CONTROL_MEMORY.md:1442` - the age's definition drops "or owed nothing"

`:1436` and `ctrl_loop.h` say the age counts "since the step last ran or owed nothing"; `:1442` says "since it last ran".

**Exact fix:** in `:1442`, "The step's age counts the centiseconds dispatched since it last ran or owed nothing, and in every window …".

### SUGGESTION-1 - state the save's worst case on the product's flash part

The 12,110 ms is "on a flash with no busy time". The store erases a slot with a 64 KiB block erase (`grade.FLASH_ERASE` = 0xD8), and polls it once a step, every three ticks at worst. #823's writer inherits this step, so it would help to state the figure with the product part's maximum block-erase time added, rounded up to 30 ms. The page-program wait already fits inside a step.

### SUGGESTION-2 (retained from R712-3 SUGGESTION-1) - the step's room is not gated

The longest step is 0.966 ms against `NVM_STEP_US` = 1.0 ms: 0.034 ms of room, which the author discloses. A per-kind step-cost check against `NVM_STEP_US`, with a plant, would make a slower flash port fail by name.

### SUGGESTION-3 (outside this PR; for a new Issue) - `capture_coherence`'s mutant driver scales its memory with the CPU set it is given

See judgement (5).

## The five judgements requested

**(1) The shared MAJOR, mechanism (b). Resolved at its cause, with F1 against its stated basis.**

- `ctrl_loop.c:160-168`: an owed step aged past `CTRL_LOOP_STEP_AGE` = 2 centiseconds is the whole next pass. It runs before any input, with the deadline read as the pass starts, and returns 1. A step deferred for room keeps its age (`:182`). `nvm_store_step` returns true only when deferred (`nvm_store.c:799-811`), so "ran or owed nothing" is exactly the reset condition.
- N was chosen by measurement on the staged windows. The author's `analysis/stepgaps-*` shows at most two centiseconds between step-carrying passes in every staged window, against three in `save-starved`. Every row and pass fits at both points, in both arms, with and without the drafts. The least margin is 0.77 ms in the staged windows (N-A8 `table.md`: 17.234 ms, which I reproduced exactly). F1 is the part of the basis that does not hold.
- The harness groups `save-held` and `save-starved` run at the contract refill rates in both arms (N-B1, N-B8, D-*). `held_load` refuses a group that commits fewer records than it offered (`save_grade.py:94-101`).
- Removing the age limit is caught. AGE-A8: "CONTROL store-step-ageless caught … not durable 12618.411 ms after its change (stated worst case 12,110 ms)", rc 0. This is my image `29713a0a…`.

**(2) The stated worst case: derived, not fitted.**

- T ≤ 1,000 + S × 3 × 10 + 10 ms (`save_window.py:84-97`, `nvm_store.h:16-28`).
- The step count follows `nvm_store.c:464-775` phase by phase. At 8x8 (container 13,256 B): 1 + 3 + 52 + 2 + 104 + 104 + 104 = 370. At 1x1 (3,336 B): 102 (`receipts/bound_check.txt`).
- The author's per-kind counts for one 8x8 save agree with S: erase 1, polls 53, blank 104, pages 52, verify 104, and capture or seal 56 (`analysis/stepkinds-N-A8.txt`).
- The 10 ms slack is argued, not fitted. Steps are anchored to ticks, so the per-step lateness of a few ms (the 31.3 to 31.5 ms flash-step gaps) does not accumulate. The worst debounce phase gives at most 12,100 ms plus the mark's and the final tick's latency, a few passes.
- Measured: 12,087.0 to 12,088.0 ms at 8x8 and 4,047.9 to 4,049.0 ms at 1x1, both arms, with and without the drafts. Every save is within its bound at every measured point.

**How 12.1 s relates to the owner's 0.5 s (#823, 2026-10-31).** 12.11 s is about 24 times the owner's 0.5 s worst case, and it does not include the flash part's erase time.

- The PR does not claim the 0.5 s, and says so in several places: `SPLIT_CONTROL_MEMORY.md:1455` "this image states its own worst case and does not meet 0.5 s", `:1593`, the PR body `:351`, and REVIEW READY Open risks.
- The round 14 assignment decided that "This image does not have to meet 0.5 s … It must state and test its own bound", and it does.
- So I make no finding. What the PR records is a stated, tested 12,110 ms bound for this image on a busy-free flash. Whether that is acceptable for Mark II, or the step must change for the #823 writer, is the manager's and the owner's scope decision.

**(3) The round 13 MINORs. Resolved.**

- **One build a pass in both orientations (R711-3-F2).**
  - `turn_builds` reads the turn interface's state before any visit (`srp_mbx.c:840-845,852-859`). I traced it: it predicts exactly whether the turn interface builds in this poll (no participants, not withdrawing, link level held).
  - The mirrored test `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` (`srp_app.cpp:414`) and the plant `build-turn-read-after-its-visit` are caught (`gates/firmware/fwshard-*.log`).
  - The re-anchored `srp-poll-extra-read` is caught.
  - `y-links` is 1.741 / 1.809 ms (X-A8, X-B8).
- **The step-pass maximum (R712-3-F2 = R711-3-F3).** Over every group: 1.218 / 1.231 ms at 1x1 and 1.292 / 1.266 ms at 8x8, arm A / arm B; 1.182 / 1.177 and 1.246 / 1.249 ms with the drafts (`measure/*/table.md`, "Longest pass that carries a step"). That is at least the 1.26 ms required, on one basis at both points (`SPLIT_CONTROL_MEMORY.md:1487`). `:1350` is the round 13 record, scoped to what it measured.
- **The verify phase's end (R711-3-F4).** `grade.save_phase` refuses a verify window once its read-backs have read back the programmed image (`grade.py:830-848`). The self-test mutant "a verify window is graded after its read-backs read back the container" is caught (`gates/lane/harness_selftest.log`: 0 failures).

**(4) Residues.**

- R712-3 RESIDUE-1 is applied word for word (`SPLIT_CONTROL_MEMORY.md:1609`), beside R711-3's. That produced RESIDUE-1 above.
- R712-3 RESIDUE-2 is applied word for word (`nvm_store.h`, the `NVM_READ_BYTES` comment).
- R712-3 SUGGESTION-2 is taken (`:1694`, 1.116 ms). I rechecked its arithmetic: 0.77 − 0.446 = 0.32, 0.77 − 1.116 = −0.35, 0.77 − 8.0 = −7.23.
- The comment rule: no added source line in the delta names a bench lane label, lane name, review round, reviewer ID or issue-comment ID. I scanned the added non-Markdown lines for round, R7xx, A6xx, issuecomment, B-number and lane; the only matches were Python's `round()`. New residue is RESIDUE-1 and RESIDUE-2 above.

**(5) The disclosed deviations.**

- **Sweep shard 2 (`capture_coherence`), OOM-killed at 10 and 24 GB, passing alone on 4 CPUs.** This is a defect of the shard tooling, not of this PR.
  - The delta changes no RTL and nothing under `tb/verilator/capture_coherence` (`git diff --stat 4f58214f a3f23bba`).
  - The suite's mutant driver runs one Verilator `--build -j 0` per CPU in its affinity, so its memory grows with the CPU range a unit is given. Rounds 12 and 13 already peaked at 10 GB with swap (`gates/sweep-shard2-killed/journal-shard2-peaks.txt`).
  - The passing run is the same `run_all_suites.sh … --shard 2/4` command at the head, exit 0 in 5,723.8 s, with `MAKEFLAGS=-j4` (`gates/sweep/shard-2/results.json`).
  - It did run on a host whose root filesystem had been remounted read-only at 08:06. Its outputs were on a writable volume, and its rc and logs are recorded. I accept it as source evidence. SUGGESTION-3: an Issue to cap the driver's workers by `MAKEFLAGS` or the unit's memory.
- **The 8x8 harness gate through the 11-03 07:52-08:06 incident.** `G-A8/table.md` and `N-A8/table.md` share sha256 `3e0cf029…`. `G-A1` and `N-A1` match too, `79954680…`. The images are the legs' (`gates/image-identity.log`: 6 of 6). This is consistent with a deterministic simulation. My own rebuild at the head gives N-A8's image hash and reproduces its tightest row, 17.234 ms, so I accept the gate.

## Lens results at this head

Every lens was applied to the delta. F1 is recorded under all five lenses and F2 under Tests, so none is clean.

| Lens | Result | Artifacts examined at `a3f23bba` | What was checked |
|---|---|---|---|
| Conformance | UNCLEAN (F1) | the round 14 items 1-6 against `ctrl_loop.c:155-195`, `ctrl_loop.h:80-106,143-151`, `nvm_store.h:9-28`, `save_window.py:24-97,152-250`, `save_grade.py`, N-/D-/AGE-/CTL-/X-/G- tables | Items 2-6 met. Item 1's mechanism and N are met; its "measure, do not assume" for the rows is met only for windows entered at age 0 (F1). |
| RTL (architecture) | UNCLEAN (F1) | the loop's pass order with the aged pass; `nvm_store_step`, `_tick`, `nvm_mark`, `nvm_store_changed_id`, `nvm_rec_id_of`, `nvm_rec_id_known` (`nvm_klj2.c:187-202`); AECP's `mark` and poll (`aecp_nvm.c:126-168`); SRP `turn_builds` and poll | The mechanism and the walk-free mark are correct. I found no width, wrap or ordering defect: the int32 deadline difference is wrap-safe, an id is bounded by the shape before it indexes `dirty`, and AECP bits come from `nvm_rec_id_of`. Its latency effect on a window is not what `ctrl_loop.h:146-150` states (F1). |
| Robustness | UNCLEAN (F1) | unrated events before a burst (my probes); a deferred step keeping its age; an idle store under continuous input (an aged pass costs about 0.03 ms of store work); flood and held load; a joint link change in both orientations | F1's input order; nothing else found. |
| Tests | UNCLEAN (F1, F2) | `test_port_loop.cpp` L13; `loop_step_mutants.py` (10 plants caught, `fwshard-*.log`); `srp_app.cpp:414` and its plant; `test_nvm_codec.cpp` `codec_ids_without_the_walk`; `test_nvm_more.cpp` `change_by_record_id`; `test_nvm_write.cpp` `step_room` at exactly `NVM_STEP_US`; `nvm_mutants.py` additions; `selftest_share.py` and `selftest_mutants.py` (124 of 124); my firmware plant; my 37 probe runs (21 on the head's image, 16 on the ageless control) | F2's survivor. F1's untested entry state. The other new tests can fail for their defects, by the author's plants and by my reading. |
| Docs | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md:1429-1595,1597-1700`; `MAILBOX_SPLIT.md`; `ctrl/README.md`; `srp/README.md`; `ctrl_nvm/README.md`; `ctrl_service_budget/README.md`; `ctrl_split_boot/README.md`; the header comments; the PR body; REVIEW READY | F1's statements; RESIDUE-1 and RESIDUE-2. Every other figure I traced matches its receipt. |

## Prior findings at this head

| Finding | State | Evidence at `a3f23bba` |
|---|---|---|
| R712-3-F1 = R711-3-F1, MAJOR: a save's progress unbounded under input | **Resolved at its cause** | The age limit (`ctrl_loop.c:160-168`); the stated bound, derived; `save-starved` within it; the ageless control caught. Its stated basis is F1 (a new MINOR). |
| R712-3-F2 = R711-3-F3, MINOR: the step-pass maximum | **Resolved** | 1.29 / 1.27 ms at 8x8 over every group, one basis at both points (`SPLIT_CONTROL_MEMORY.md:1487`). |
| R711-3-F2, MINOR: one build a pass in one orientation | **Resolved** | `turn_builds`; the mirrored test and its plant caught. |
| R711-3-F4, MINOR: the verify phase's end | **Resolved** | `grade.py:848`; its self-test mutant caught. |
| R712-3 RESIDUE-1, R711-3 RESIDUE-1 | **Applied** | `:1609`, duplicated (RESIDUE-1 here). |
| R712-3 RESIDUE-2 | **Applied** | `nvm_store.h` `NVM_READ_BYTES` comment, the exact text. |
| R712-3 SUGGESTION-1: the step cost against `NVM_STEP_US` | **Retained** | SUGGESTION-2 here; disclosed as ungated. |
| R712-3 SUGGESTION-2: 1.116 ms | **Taken** | `:1694`. |
| R712-3 SUGGESTION-3: boot export nondeterminism (outside the PR) | **Retained, outside the PR** | Not touched by the delta. |
| R711-3 S1: `step_room` at exactly `NVM_STEP_US` | **Taken** | `test_nvm_write.cpp`, plant `step_needs_room_past_its_cost`. |
| R711-3 S2: capture and seal step costs | **Taken** | `ctrl_nvm/README.md` and `SPLIT_CONTROL_MEMORY.md:1491-1499`. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | as in Lens results; F1 open | R712-4 | `a3f23bbabdd9800177224432361fcd41b53bf882` |
| RTL | UNCLEAN | as in Lens results; F1 open | R712-4 | `a3f23bbabdd9800177224432361fcd41b53bf882` |
| Robustness | UNCLEAN | as in Lens results; F1 open | R712-4 | `a3f23bbabdd9800177224432361fcd41b53bf882` |
| Tests | UNCLEAN | as in Lens results; F1, F2 open | R712-4 | `a3f23bbabdd9800177224432361fcd41b53bf882` |
| Docs | UNCLEAN | as in Lens results; F1 open | R712-4 | `a3f23bbabdd9800177224432361fcd41b53bf882` |

## Real limits

- **No row over its bound was found.** F1 rests on aged steps measured among a window's records, their measured cost, and a margin measured at 0.225 ms. The worst combination of entry age, tick phase and flash phase was not searched exhaustively.
- **One arm only.** The probes ran in arm A at 8x8/2if, without the drafts.
- **Not re-run by me:** the author's full legs, the sweep, the mutant campaigns, the harness self-test, docs.yml, behave, the builder, or Yosys. I relied on their receipts, verified against the manifest and spot-checked, and on the image identity I reproduced.
- **No hardware.** No physical calibration and no flash-part busy time.
- **Hosted evidence at the exact head is incomplete.** I read it only (`receipts/hosted_checks_a3f23bba.tsv`):
  - `rtl-fast` success; `yosys-portability` success.
  - `verilator-suites` failure. 11 of 19 Verilator shards were cancelled at 16:46 to 16:47Z, none failed, and the six `Union …` jobs then failed their ownership check. The skipped context: Physical gPTP.
  - This is not an executed failure. It is also not exact-head `verilator-suites` evidence.
- **No manager source bank** runs at this head, and I infer none. The current-dev merge candidate (live dev `e61a4afa`) is the manager's.

## Pending manager duties

- Publish this packet. Carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Route F1 and F2 to the author. F1's outcome may change N, or the mechanism, if the age-at-limit window does not fit.
- Re-run or obtain exact-head hosted `verilator-suites`; the cancelled shards are not evidence.
- Decide with the owner whether a 12.11 s stated worst case, plus the part's erase time, is acceptable for this image, and what #823's writer inherits.
- Consider SUGGESTION-3 as a new Issue on the shard tooling.
- The current-dev merge candidate, builder and native banks are at the merge turn.

R712-4 FINISHED
