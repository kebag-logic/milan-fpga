[R703] NEGATIVE - exact head cd3525c3ddcbdb5d78bf8fccdab354c468926997

# [R703] R703-2: internal cleared-context review of PR #792 (issue #665, CPU budget), round 2

- **Head:** `cd3525c3ddcbdb5d78bf8fccdab354c468926997`, tree `8880067ab9fbfc65736fea8e245a2e748c1df279`. This is one commit on round 1's `d58c8e22`. The base is `dev-soft-core` `e76a755a`.
- **Scope:** the delta review `d58c8e22..cd3525c3` (11 files, all under `tb/verilator/ctrl_service_budget/`). It answers R703-1 (issuecomment-6415122678) and R704-1 (issuecomment-6414619069), under the round-2 assignment (issue #665 issuecomment-6415127884).
- **Order of reading:** AGENTS.md and CONTRIBUTING.md, then the issue's frozen S2 assignment and decisions D3/D4/D5, round-2 items 1 to 6, `FR_NFR.md` 3.4.1, `MAILBOX_SPLIT.md:495-502`, `:645-657` and `:753-758`, `mailbox.yaml` and `KL_mbx_rx.sv`. Then the diff and the public evidence. I read the prior review findings only after my own pass over the diff.
- **What this is not:** the expected T_svc miss is the result of this lane (D4), and it is not a finding here. Every finding below is about a measurement that is missing, misreported or unprotected.

## Verdict

**NEGATIVE.** Two MAJOR findings and one MINOR finding are open.

- **F1 (MAJOR).** The SRP part of the defined composed load is committed but never serviced in the groups that set the headline composed maximum. It is starved for at least 2 s, and none of this is reported.
- **F2 (MAJOR).** The notification fan-out is measured with one registered controller. At the firmware's registration capacity, SET_NAME misses T_svc at both points: 11.33 ms and 20.68 ms, where the README reports 5.76 ms and 8.39 ms "fits".
- **F3 (MINOR).** One plausible composition defect passes the self-test and halves the published composed maximum.

Every round-1 finding of both reviews is resolved at its stated cause, except R-4, which is carried to the manager as before (see the table below). Every figure the PR publishes reproduces to the cycle.

## What reproduces

Every run below is mine, at the head, from a clean detached clone, on fresh builds (`receipts/runs/`).

| Run | Printed result (rc) | Against the published receipts (`33750832`, `review-evidence/665s2-r1/author-r2`) |
|---|---|---|
| `run.py --self-test` | 51 checks pass, 36/36 mutants caught, `self-test: 0 failures` (0) | same as `gates/selftest.log` |
| arm A 1x1 | `17 groups graded, 0 refusals, 11 T_svc misses (11 of 78 probe instances, 10 of 61 paths)` (0) | 17/17 group grades equal, `table.md` byte-identical, 7/7 published logs byte-identical |
| arm A 8x8 | `16 groups graded, 0 refusals, 45 T_svc misses (45 of 125 probe instances, 37 of 106 paths)` (0) | 16/16 group grades equal, `table.md` byte-identical, 5/5 published logs byte-identical |
| shutdown arm 1x1 / 8x8 | `2 groups graded, 0 refusals, 0 T_svc misses` (0 of 2 / 0 of 3 paths) (0) | grades and `table.md` equal; `results.json` differs only in the executable hash, which depends on where the build ran |
| `--mutation slow-adp-rx` | `CONTROL slow-adp-rx caught`, 24.614 ms (0) | same |
| `--variant shutdown-entry --mutation slow-adp-shutdown` | `CONTROL slow-adp-shutdown caught`, 24.903 ms (0) | same |
| `--cpu-regions as-built` | `CONTROL as-built caught: an instruction access fault (cause 1)` (0) | same |
| arm B 1x1 / 8x8 (7 groups each) | `7 groups graded, 0 refusals, 4 T_svc misses (4 of 20 ...)` / `(4 of 36 ...)` (0 each) | 7/7 group grades equal at each point, `table.md` byte-identical, published `acmp-cmd.log` byte-identical; `results.json` differs only in the executable hash |
| `selftest.py --write-fixture` from my 1x1 `fixture` run, in a sandbox copy | `fixture.log` and `oracle.json` regenerate byte-identical | n/a |

The 1x1 arm A run reused its own fresh build. Its first attempt was discarded (see Limits), and `--reuse-build` attested the build.

My round-1 independent recomputation, rerun unmodified (`scripts/recompute.py`, which does not import the harness grader), reproduces every headline figure from the raw logs (`receipts/recompute_A1.json`, `_A8.json`):

| Figure | 1x1 | 8x8 | README / PR |
|---|---|---|---|
| clock ratio inside the logs | 940 consecutive pass pairs, all sys = 2 x CPU; NOW_MS every 100,000 bus cycles | 836 pairs, all exact | 50 / 100 MHz |
| worst pass | 1,565,803 (31.316 ms), backlog-adp | 2,989,496 (59.79 ms), acmp-notk | same |
| composed maximum | 1,565,803 (31.316 ms), backlog-adp | 2,209,308 (44.186 ms), backlog-adp-refill | same |
| an event behind 15 others | 15.487 ms | 44.651 ms | 15.49 / 44.65 |
| an ACMP command behind a full acmp ring (wire upper bound) | 63.305 ms | 108.713 ms | 63.30 / 108.71 |
| an ENTITY_AVAILABLE behind the adp ring | 67.932 ms | 83.506 ms | 67.93 / 83.51 |
| a response with 7 frames owed ahead (wire upper bound) | 125.79 ms | 151.917 ms | 125.79 / 151.92 |

Other checks against the README and the published packet:

- **README cells.** Each path's worst instance, as `results.json` gives it, is found verbatim in the README tables: 61/61 at 1x1 and 106/106 at 8x8 (`receipts/readme_cells_vs_results.txt`).
- **Published packet.** All 227 blobs under `author-r2` match their git SHA-1 and the top-level `MANIFEST.json` sha256. The 187 kept entries of `receipts/MANIFEST.json` match their published sha256 (`receipts/evidence_manifest_check.txt`).
  - The evidence commit carries no cryptographic signature: GitHub reports it unsigned. The manifests are the attestation.
- **Live PR body.** It is byte-identical to the published `PR-BODY.md`.
- **Gates at the head (`receipts/gates/summary.txt`).** All rc 0: `docs_check`, `check_doc_paths`, `check_doc_style`, `check_em_dash --base e76a755a` and `gen_toc --check/--verify-anchors` (both with the pinned Markdown renderer), `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `check_todo_ownership` and `git diff --check e76a755a HEAD`.
  - The two Markdown gates exit 2 without that renderer, the same as in round 1.
  - behave is not rerun: the delta touches no file it reads. The author's receipt shows 406 scenarios passing.

## Round-1 probes, rerun at this head

1. **The defined load.**
   - Counted independently from the raw logs, without the grader (`receipts/population_fanout_a1x1.txt`, `_a8x8.txt`), every backlog window commits ADP 8 (11 with the refill leg), ACMP 12 (8 in `backlog-owed`), AECP 16, MAAP 7, SRP 32 and GM 15, plus LINK 1 in `backlog`. No offered frame goes uncommitted.
   - The records ahead at each input are 11, 7, 4 (8x8: 6) and 7, the same as the grader's.
   - The bound/observed labelling matches `admission()` and the contract: event, ACMP and MAAP are at room; ADP, AECP and SRP are at their burst.
   - **But the SRP part of the load is never serviced in the headline groups: F1.**
2. **Notification fan-out.**
   - The 8x8 `aecp.set_name.if1` now ends at the second recipient's commit, 8.389 ms. My independent decode pairs each AECP TX commit with its wire frame: solicited at 7.524 ms, CTL1@if0 at 7.933 ms, CTL1@if1 at 8.389 ms.
   - **The set measured is one registered controller: F2.**
3. **Self-protecting figures.**
   - All twelve round-1 mutants, re-anchored to the refactored code with the same defect, are caught (`receipts/review_mutants2.log`, R1 to R12). R8 is inverted because the commit rule is now newest-pending, which is correct: see RTL below.
   - Of thirteen new plants (N1 to N13), the pass-bound (N1 to N3), clock-ratio (N4, N5) and two of the composition plants (N7, N9) are caught, as is N13.
   - **N6 escapes and moves the headline composed maximum: F3.**
   - N8, N11 and N12 escape with no published value changed (`receipts/mutant_regrade_escapes.txt`). N10 changes one group's worst pass but not the headline.
   - The unmodified round-1 script reports seven anchors missing, because the code was refactored (`receipts/review_mutants_unmodified.log`).
4. **Attestation (`receipts/stale_probe2.log`).** I made 14 plants in copies of a finished build. Each is refused by `build.reused()`:
   - the ELF;
   - ROM bank 0 changed, ROM bank 1 deleted, and an unrecorded ROM `.init`;
   - `sim.v`;
   - the CPU netlist, both its content (a private copy under the recorded digest) and its recorded digest;
   - `libc.a`, `budget_config.hpp` and `Vsim`;
   - the firmware tree digest;
   - a bare-basename key and a relative external key;
   - a `build.json` with no inputs.

   The unchanged copy is accepted. `run.py --reuse-build` on the ROM plant prints `REFUSED ... sim_rom_bank0.init changed`, rc 1.
5. **No silent drops (`receipts/regrade_probe.txt`).** Each of these is refused by name with rc 1, with and without `--record-budget-findings`: an empty out directory, one log absent, all logs absent, a stale script and an absent script. The intact explicit subset gives rc 0 when recorded and rc 1 when not. Selecting every group with one log missing gives rc 1.
6. **Tables.**
   - Each path's worst instance is what the README shows (probe 1 above).
   - The counts are per (path, interface) and per instance, and they match a dedupe of `results.json`.
   - SHUTDOWN is measured: 0.58 ms at 1x1, and 0.58 / 1.17 ms at 8x8. Its control is caught.

## Findings

### R703-2-F1 MAJOR: Conformance, RTL, Robustness, Tests, Docs. The SRP part of the defined composed load is never serviced in the groups that set the headline composed maximum, and SRP's receive latency under the load is unmeasured and unreported

- **Where.**
  - `tb/verilator/ctrl_service_budget/scenario.py:634-655`: `bound_talker_groups` ends the window (`mark composed_end`) once the ADP probe settles.
  - `grade.py:542-586`: `population()` and `check_load()` assert receive commits only, and `composed()` takes the longest pass that starts inside the window.
  - `README.md:276`, `:265`, `:354` and `:474-482`, plus the PR body's "Every backlog group's composed window now carries every receive channel's admitted burst at once" and its D4 (b) input.
- **Authority.**
  - Round-2 item 1: "The backlog rows and the composed maximum run with every channel's admitted burst at once, MAAP and SRP included".
  - `FR_NFR.md` 3.4.1: "Backlog ... consume this budget". The MRP ceiling is 18 ms.
  - The assignment: "the worst pass at the composed maximum", and "each figure compared with T_svc".
  - AGENTS.md section 6: RTL and architecture covers stalls and latency; Robustness covers backpressure.
- **Evidence.**
  - `receipts/srp_service.txt`, from my head logs. In arm A's `backlog-adp` and `backlog-adp-refill`, at both points, all 32 SRP records commit inside the window, and no pass releases one before the window (and the run) ends.
    - The windows are 567.99 and 628.34 ms at 1x1, and 583.56 and 658.81 ms at 8x8.
    - The author's own published drains show the same: `drain_A1.txt` and `drain_A8.txt` have no SRP release in those groups, while arm B's `backlog-adp` releases SRP in 19-20 passes.
  - `receipts/srp_tail_1x1.txt`. I extended the 1x1 `backlog-adp` script by 1,500 ms after `composed_end`.
    - 60 more passes of 12.17-28.99 ms run, and still no SRP record is released, more than 2.07 s after the load arrived.
    - The cause is `sw/firmware/ctrl/srp/srp_mbx.c:441-451`. SRP takes a record only when no event is pending (`rx_order_ready`).
    - Arm A's passes after the bind are longer than the 10 ms TICK, so an event is always pending, and SRP starves.
  - Where SRP is served (`backlog`, `backlog-owed`), the head record on the SRP ring waits 76.88 ms (1x1) and 118.99 ms (8x8) from its commit to its release, and 51.79 / 106.92 ms in `backlog-owed`. Nothing is ahead of it on its ring. The 32nd record waits up to 158.94 / 327.85 ms.
    - Arm B, whose callbacks answer, serves SRP in every group, but its head SRP record still waits 59.99 ms (1x1) and 119.77 ms (8x8) in `backlog-adp` (`receipts/srp_service_armB.txt`). So the latency is not only arm A's retry.
    - The README's "SRP Listener Ready RX" row, whose end is the record's release (`README.md:478`), reports 2.77 ms (1x1) and 9.11 ms (8x8). That is an instance with no load.
  - The 1x1 composed maximum (`backlog-adp`, 31.32 ms) and the 8x8 composed maximum (`backlog-adp-refill`, 44.19 ms) therefore come from windows in which none of the SRP load's work ran. The window closes with the load undrained.
- **Impact.**
  - The headline "composed maximum with every channel's admitted burst at once" does not include SRP's service at all.
  - One defined-load path, the SRP receive of the composed SRP burst, misses its 18 ms ceiling by 3 to 18 times where it is served (both arms), and is starved without bound where it is not. Neither appears in any table, count or finding.
  - D4's decision input omits a consumer interaction: SRP is starved while passes exceed the tick. S2b's per-pass cap will be judged on this harness, which would not notice whether SRP is ever served.
- **Required outcome.**
  - A group's composed window must not close before every record of its load is released, or the grader refuses or flags the window per channel, naming the records committed but never released. A starved load cannot stand as a measured composed maximum.
  - The service of each loaded channel under the composed load (at least SRP's first and last record, ending at the record's release, as the SRP rows already end) is graded as probes, with verdicts. A record never released is reported as unbounded, not omitted.
  - The README tables, the counts, the Findings (D4) and the PR body state the starvation mechanism (`srp_mbx.c:441-451` with passes longer than the TICK period) and its measured extent.
  - The composed-maximum figures are restated if the window changes.
- **Verification.**
  - Rerun the backlog groups at both points.
  - Each window's per-channel releases equal its load, or the run fails or reports the starved channel.
  - The SRP rows appear with these magnitudes.
  - A control that starves one loaded channel (the head's arm A `backlog-adp` is one) is caught by a named check.

### R703-2-F2 MAJOR: Conformance, Robustness, Tests, Docs. The notification fan-out is measured with one registered controller; at the firmware's registration capacity SET_NAME misses T_svc at both points

- **Where.**
  - `scenario.py:465-467`: `set_name`'s recipients are CTL1 on the interfaces registered so far, so 1 recipient at 1x1 and at most 2 at 8x8.
  - `README.md:254` and `:258`, `README.md:149` ("a cell is a path's worst measured instance"), and the PR body's SET_NAME row.
- **Authority.**
  - `FR_NFR.md:341`: "The last required recipient's commit ends a notification fan-out". The required recipients are every registered controller.
  - The firmware registers up to `AECP_REGISTRATIONS` = 16 controllers per interface (`sw/firmware/ctrl/aecp/aecp.h:12`, `aecp.c:181-207`) and notifies each in one loop (`aecp.c:401-418`).
  - Round-2 item 2: "with the complete recipient set on every interface".
  - AGENTS.md Robustness: "minimum/maximum values".
- **Evidence.** A disposable reviewer group, `scripts/fanout_full.py` with `scripts/fanout_run.py`, runs on my head builds and is graded by the harness's own `grade.py` rule.
  - It registers 16 controllers on every interface, then a 17th controller sends SET_NAME.
  - At 1x1, the fan-out ends at the 16th recipient's commit, at **11.332 ms** (bound 12.98 ms). The measurement is `status measured`, with no refusal, so every recipient received exactly one notification and nobody else did.
  - At 8x8 (32 recipients) it ends at **20.683 ms** (bound 27.82 ms).
  - My independent decode confirms 16 and 32 unsolicited SET_NAME commits, about 0.41 ms (about 20,000 CPU cycles) per recipient (`receipts/fanout_full_1x1_*.txt`, `_8x8_*.txt`).
  - The README reports the path as 5.76 ms (1x1) and 8.39 ms (8x8), "fits".
- **Impact.**
  - A path the deliverable reports as fitting misses T_svc at its capacity, and at 8x8 it comes within 3.3 ms of its 24 ms ceiling.
  - The tables' "worst measured instance" is not the path's worst case, and the per-recipient cost, a D4 (a) consumer, is not reported.
  - S2b, re-measured on this harness, would not see notification fan-out regress or improve.
- **Required outcome.**
  - Measure the fan-out at the registration capacity on every interface. Alternatively, a recorded owner or manager disposition fixes the recipient count the row is defined at.
  - Report the result in the AECP table, the counts and the Findings, including the per-recipient cost, or state the defined count and the capacity in Results and Limits.
- **Verification.** A group registering `AECP_REGISTRATIONS` controllers per interface reproduces about 11.33 ms at 1x1 and about 20.68 ms at 8x8, ending at the last recipient, and its verdict appears in the tables.

### R703-2-F3 MINOR: Tests. A composition defect that halves the published composed maximum passes the self-test

- **Where.**
  - `grade.py:582` (`top = max(inside, key=lambda p: p.cycles)`).
  - The fixture's composed window (`scenario.py:803-808`, `oracle.json` `passes`) has 3 passes, and its first is its longest.
  - `selftest.py`'s pass checks pin only that window.
- **Authority.**
  - Round-2 item 3: "each changes the headline worst-pass, composed-maximum or pass-bound figure and fails a named check".
  - The `selftest.py` docstring: "a mutant of a headline figure ... fails on that figure".
  - AGENTS.md Tests: each test can fail for the defect it claims to detect.
- **Evidence.**
  - N6 replaces the window's longest pass with its first. The self-test passes (rc 0, `receipts/review_mutants2.log`).
  - Regrading my head logs under N6 (`receipts/mutant_regrade_escapes.txt`) changes the published composed maximum:
    - 1x1: 31.32 to 14.87 ms (`backlog-adp`), 30.63 to 14.87 ms (refill) and 11.65 to 11.25 ms (owed);
    - 8x8: 44.19 to 20.57 ms, 44.17 to 20.57 ms, 27.84 to 17.64 ms and 22.23 to 17.52 ms.
  - Two plants in the same family also escape:
    - N10, where the worst pass ignores the run's last pass, changes `adp-link`'s worst pass 5.48 to 4.97 ms at 1x1 (the headline is unaffected);
    - N8, where a window that committed more than its load is accepted, against `README.md:138`'s "exactly". It changes no value at the head.
- **Impact.** A refactor that picks the wrong pass in the window would halve the headline composed maximum, the figure S2b is to be judged on, without any check failing.
- **Required outcome.** The pinned window includes a pass longer than its first, or a synthetic check has its longest pass neither first nor last, so N6 and N10 fail a named check. An over-population plant is refused.
- **Verification.** `scripts/review_mutants2.py` reports N6, N8 and N10 caught.

## RESIDUE (purely wording; exact fix given; carried to the manager's checklist)

- **R703-2-R1: "every receive channel's admitted burst" is not literal for two groups.**
  - Where: `README.md:276`, the `scenario.py:692-693` docstring, and the PR body's F1 row.
  - `backlog-owed` carries ACMP 8 (seven owed and the input), and the refill leg ADP 11 (`README.md:318-319`).
  - Replace with "Every backlog group's composed window carries every other receive channel's admitted burst at once, and fifteen grandmaster changes; the row's own channel carries the row's records (ACMP 8 in `backlog-owed`, ADP 8, or 11 with the refill leg)".
- **R703-2-R2: comment-rule instances new in this delta.**
  - `README.md:4` adds a review-round label and an issue-comment ID: "with the [round-2 corrections](…issuecomment-6415127884)". Delete that clause.
  - `selftest_mutants.py:6-8` and `README.md:445` mark mutants by a review-round head ("(d58c8e22)", "#665's first measuring head"). Replace with "A mutant whose name ends in '(earlier rule)' restores a rule this harness had before these checks, so its check is the test that fails on that rule", and rename the six suffixes to "(earlier rule)".
  - These are names and docstrings only; no check changes.
- **R703-2-R3: undefined arm labels that collide with lane names.** `README.md:154-161` uses A1, A8, B1, B8, S1 and S8 undefined, and S1 is also a #665 lane. Add before the table: "Arm labels: A is arm A, B is arm B, S is the `shutdown-entry` arm; 1 is 1x1 and 8 is 8x8."
- **R703-2-R4: the "path" count is per interface.** `README.md:152`, "(a path several groups measure is one path, at its worst)". Append "; at 8x8 each interface's instance is its own path".
- **R703-2-R5: "behind 15 others" shows [16 ahead] at 8x8.** `README.md:300`. After `README.md:308`, add: "At 8x8 the event ring was full (16 records) when the LINK change occurred, so the event waited for room, which 3.4.1 counts."
- **R-4 of R703-1 (retained, as the author reports).** `docs/testing/TESTING.md:518` still names one Makefile exception. That fix belongs to the release lanes' file map.

## SUGGESTION

- **S1: refill leg.** It places the input after three refills, with 4 or 6 ahead. Placing it at the peak occupancy the arrival curve produces, or sweeping its phase, would make the observed row the worst observed. It is labelled observed, so this is optional.
- **S2: checkout hygiene.**
  - A run writes `avdecc/__pycache__/`, `sw/litex/platforms/__pycache__/` and `protocol-processor/hdl/aecp/desc/__pycache__/` into the checkout, because `build.py`'s child Python steps run without `-B`. They are git-ignored, so harmless.
  - Passing `-B` (or `PYTHONDONTWRITEBYTECODE=1`) to the build steps would keep a run from writing into the checkout, as the README intends.
- **S3: location-dependent digests.**
  - `sim.v`, the runtime archives and `Vsim` differ between two builds of the same head in different directories, while the ELF and every log are identical (`receipts/build_identity.txt`).
  - Reuse is correctly bound to its own build. The README could say that cross-build identity is the ELF and the logs.

## Prior public findings at this head

| Finding | Status at `cd3525c3` | Evidence |
|---|---|---|
| R703-1 F1 / R704-1 F1 (the load) | **Resolved as stated.** The populations are committed through the shipping filter and asserted, the bounds are labelled from the buckets and rings, and a refill leg is added. The newly present SRP load exposes F1 above, which is a new finding. | probe 1; `population_fanout_*.txt` |
| R703-1 F2 (protection) | **Resolved** for every conversion and the R1-R12 defects. The residual composition gap is F3. | `review_mutants2.log` |
| R703-1 F3 / R704-1 F2 (fan-out) | **Resolved**: last recipient, causal command and descriptor, missing or extra recipient refused, 8.389 ms reproduced. The capacity gap is F2. | probe 2 |
| R703-1 F4 (tables) | **Resolved.** | `readme_cells_vs_results.txt` |
| R703-1 F5 / R704-1 F3 (reuse) | **Resolved.** | `stale_probe2.log` |
| R703-1 F6 / R704-1 F4 (silent drops) | **Resolved.** | `regrade_probe.txt` |
| R703-1 F7 / R704-1 F5 (SHUTDOWN) | **Resolved**: measured through a labelled test-only entry, with its control caught. | runs `s1x1`, `s8x8`, `c-slowsd` |
| R703-1 R-1 / R704-1 R1 (comment labels) | **Resolved** in the files named. New instances are R703-2-R2. | grep at the head |
| R703-1 R-2, R-3 | **Resolved** (`README.md:185`, `:188`). | |
| R703-1 R-4 | **Retained**: not applied, as disclosed. It goes to the manager's residue checklist. | |
| R703-1 S1, S2 | **Applied** (`WIRE` order, timeouts in `table.md`, flash 15-29x). | |

## RTL and the commit rule (checked, clean apart from F1's latency attribution)

- `KL_mbx_rx.sv:199` asserts `rx_ready_o` only in `RECV_S`, and `:565-577` leaves `RECV_S` for `FIN_S` at a frame's end and returns only after the verdict (`HDR1_S` commit, or refusal).
- In every published 1x1 and 8x8 log, each commit is exactly 4 bus cycles after its frame's last byte (65 of 65), and no commit finds an older uncommitted frame pending.
- So `owner()`'s newest-pending rule (`grade.py:87-100`) is correct, and the `COMMIT_LATENCY_MAX` window is conservative.
- `sim_main.cpp`'s changes are the `ENTRY` print (committed PC equals the symbol's address) and `reply ... on=<if>`. Both are passive or test stimulus only.
- No shipping RTL, SoC, firmware, CI or workflow file is in the diff.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `FR_NFR.md` 3.4.1 (`:337-343`) against `grade.py:87-118,273-300,402-475,542-586` and `scenario.py:445-470,531-722`; `MAILBOX_SPLIT.md:495-502,645-657,753-758` against the probes; round-2 items 1-6; both points and both arms rerun, recomputed and compared with the packet; SRP service and capacity fan-out probes | R703-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| RTL | UNCLEAN (F1) | `KL_mbx_rx.sv:159-200,441-483,565-579` against `grade.owner()`; commit latency in the published and my logs; `sim_main.cpp` delta (ENTRY, `on=`); `split_soc.py` delta (comment only); `srp_mbx.c:441-451` with `ctrl_loop.c:121-150` (the loop's SRP admission, which starves under long passes) | R703-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Robustness | UNCLEAN (F1, F2) | the stale-input plants (14), regrade absent/stale cases (13), the refused-frame commit rule, starvation under the composed load, the registration-capacity maximum | R703-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Tests | UNCLEAN (F1, F2, F3) | `selftest.py`, `selftest_mutants.py`, `oracle.json`, `fixture.log` (regenerated identical); 25 reviewer mutants plus regrade of the escapes on real logs; three controls rerun | R703-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |
| Docs | UNCLEAN (F1, F2) | `README.md` (every path cell against `results.json`, the population and backlog tables, Findings, Limits); the live PR body (identical to the packet's); `build.py`/`grade.py`/`scenario.py` docstrings; RESIDUE R1-R5 | R703-2 | cd3525c3ddcbdb5d78bf8fccdab354c468926997 |

No lens is covered clean at this head. Round 1's ledger stands for the code the delta does not touch. Every lens is re-opened here by the findings above.

## Real limits of this review

- **Stated limits of the evidence.**
  - Simulation only: no hardware, bench or physical calibration (NOT RUN). Field skips are not hardware proof.
  - The flash program waits are zero, as the harness states.
  - No manager source bank exists at this head, and I claim none. The final current-dev candidate (source base `e76a755a`, live dev `76de691e`) is the manager's at the merge turn.
- **What I did not run.**
  - behave was not rerun; the delta does not touch what it reads.
  - The full parent, PP, gPTP, Yosys and builder banks are out of my allowance.
  - Hosted and act results are not inspected; they are the manager's acceptance.
- **The F1 extension and the F2 group** are disposable reviewer probes run on my head builds, outside the harness's group list. They are graded by the harness's own `grade.py` and decoded independently. They are not harness receipts.
- **The F1 extension** was run at 1x1 only. 8x8 rests on the window evidence: 0 of 32 SRP records released in 583.56 / 658.81 ms.
- **The 1x1 arm A run.** Its first attempt was discarded after a reviewer process error: a duplicate job overwrote some of its result files. The run was redone in full on the same attested build. Only that clean run is used.

## Pending manager duties

- Carry R703-2-R1 to R5 and R703-1 R-4 to the residue checklist.
- Decide whether the firmware's SRP starvation (`srp_mbx.c:441-451` under passes longer than the TICK) and the per-recipient notification cost become new Issues or S2b scope. This review asks only that the harness measure and report them.
- Validate the current-dev merge candidate and link its receipts; own the hosted/act acceptance.
- Physical calibration remains NOT RUN.

R703-2 FINISHED
