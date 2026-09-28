# Merge-dev round handoff

Status: REVIEW READY at merge head `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` (tree `9ce926b910ca80772667bb5722eb6ded5e93d223`, unchanged).
- The manager chose option (a) in the #590 [A10] disposition (comment 5870597087).
- All 15 native service runs were re-run at that head and all 15 regrade rc 0.
- The capture harness compiles two merged files, so it was re-measured.
- Every service and capture log is byte-identical to round 3's, so no figure and no file in the tree changed.
- Every gate is now rc 0.

The first-session STOP record below is kept unchanged. The continuation is in "Native re-run at the merge head".
Role: executor [A422]. Reviewers: [R368] (delta review of the merge), then the candidate, composition review and act steps named in the assignment.
Scope: PR #609 (#590, #592, #599). Assignment: #590 comment 5869849644.
Starting head: `93262f2512054166ae753eda24d76c99f2ea6714`, branch `590-592-599-firmware`, remote `https://github.com/kebag-logic/milan-fpga.git`, clean at start.
Dev: `origin/dev` fetched at `7a7582f03ce5ba7863a90ac342c21be18d90db0b`. Previous merge base: `20aa4eabf310a43b654e0c74c5374c3a0458fd4b`.
Processor gitlink: `16be6768f710e79450aace277abacd6c2c3336e5` on both sides.

## Merge

| Item | Value |
| --- | --- |
| Pre-merge head | `93262f2512054166ae753eda24d76c99f2ea6714` |
| Dev parent | `7a7582f03ce5ba7863a90ac342c21be18d90db0b` |
| Previous merge base | `20aa4eabf310a43b654e0c74c5374c3a0458fd4b` |
| Merge commit | `9e3df3edc025f73278894ff021a2011e46e2575e`, tree `76142a9c62698a0f81b1ad4d4cfe29cafa2e22d0`, subject `Merge dev into 590-592-599-firmware`, no body, no trailers |
| Stale-statement commit | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e`, tree `9ce926b910ca80772667bb5722eb6ded5e93d223`, subject `Reword stale PHY publisher and service-budget index statements` |
| Branch head (merge head) | `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` |
| Processor gitlink | `16be6768f710e79450aace277abacd6c2c3336e5` on both parents and at both new commits |

- `git merge-tree --write-tree HEAD origin/dev` before the merge reported one conflict, `docs/integration/BAREMETAL_FIRMWARE.md`. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `sw/builder/test_builder.py` auto-merged.
- `git diff HEAD^1 HEAD` on the merge commit is exactly dev's delta since the previous merge base: 39 files, +4886/-496, the same as `git diff 20aa4eabf 7a7582f0`.
- Nothing is pushed.

## Conflict resolution

Rule applied: keep both lanes' content (assignment rule 1).

- **Hunk 1 (Runtime paragraph).** This PR rewrote the paragraph and dev changed one clause inside the old paragraph. Resolution: this PR's reviewed text, with dev's clause substituted: "the provisional value section 14 leaves open" becomes "the first-dirty policy ruled by [D3 DR2a](...)". This PR's "the idle hook commits" stays.
- **Hunk 2 (insertions after the commit-failure paragraph).** Both sides inserted new paragraphs at the same point. Resolution: #610's D3 transaction retry paragraph first, unchanged, because it continues the commit-failure paragraph it follows. This PR's capture and PHY paragraphs follow, unchanged.
- Check: `git diff 93262f25 HEAD -- docs/integration/BAREMETAL_FIRMWARE.md` equals dev's own change to the page (+34/-13). `git diff 7a7582f0 HEAD -- docs/integration/BAREMETAL_FIRMWARE.md` equals this PR's own change (+62/-12). No text from either lane was added, dropped or reworded.
- #610's DR2c-carrier item 3 ("Its limit remains three attempts, separated by 500 ms.") stays as merged. Its correction (#70 comment 5868716535) belongs to a later #70 lane.

### Hunk 1 before (conflict as presented, lines 1902-1943)

```text
<<<<<<< HEAD
**Runtime.** The product BIOS calls `command_dispatch_hook` after each line.
[Patch 0006](../../sw/litex/patches/0006-bios-dispatch-hook.patch) supplies the hook and required link marker.
Firmware fails linking when that BIOS patch is absent.
The hook precedes parsing, including built-ins, unknown and empty lines.
Firmware supplies a heartbeat opportunity through this hook.
Identity and shape checks must admit the writer first.
Rejected startup paths cannot arm backing through any console command.
This services chained commands while queued input suppresses idle service.
CRC walks also yield every 256 bytes after writer initialization.
Record-validation walks yield every sixteen records.
Wipe yields between its two slot-erase verification walks.
These placements service long Milan commands, including 8x8 slot status.
Long BIOS built-ins remain a residual under the round-2 decision.
Examples include `mem_test` and large-range `mem_read`.
Their bodies provide no internal heartbeat or PHY service.
They can exceed 500 ms heartbeats and 250 ms PHY publication.
A built-in body can lapse backing after about 1,750 ms.
The 2,000 ms deadline includes up to 250 ms beforehand.
That phase can suppress the dispatch heartbeat write.
The dispatch hook services their boundaries only.
The existing heartbeat rate limit remains 250 ms.
The idle hook supplies opportunities while the console awaits input.
This interval is half the section 9.4 maximum.
When `PP_NVM_STAT` reports `nvm_dirty` for a whole debounce
window (1,000 ms, the provisional value section 14 leaves open) with no record
operation and no commit bracket in flight, the idle hook commits: the container is sealed
=======
**Runtime.** The idle hook runs while the console waits for a key, so a
console command that itself runs for more than the 2,000 ms liveness deadline
lets `nvm_backed` lapse until the prompt returns; with nothing outstanding the
next heartbeat heals it, with a change outstanding `nvm_stale` records the gap.
Queued input also suppresses the idle hook between commands.
Several short commands can therefore exceed that same liveness deadline.
[The service-budget measurements](../findings/397_SERVICE_BUDGET.md) reproduce this at both shapes.
[Issue #590](https://github.com/kebag-logic/milan-fpga/issues/590) owns dispatch and long-walk tick opportunities.
The hook heartbeats every 250 ms, half the section 9.4
maximum, and when `PP_NVM_STAT` reports `nvm_dirty` for a whole debounce
window (1,000 ms, the first-dirty policy ruled by
[D3 DR2a](../design/SAVED_STATE_MATERIALIZATION.md#151-manager-decision-register)) with no record
operation and no commit bracket in flight, it commits: the container is sealed
>>>>>>> origin/dev
```

### Hunk 1 after (merge head, lines 1902-1928)

```text
**Runtime.** The product BIOS calls `command_dispatch_hook` after each line.
[Patch 0006](../../sw/litex/patches/0006-bios-dispatch-hook.patch) supplies the hook and required link marker.
Firmware fails linking when that BIOS patch is absent.
The hook precedes parsing, including built-ins, unknown and empty lines.
Firmware supplies a heartbeat opportunity through this hook.
Identity and shape checks must admit the writer first.
Rejected startup paths cannot arm backing through any console command.
This services chained commands while queued input suppresses idle service.
CRC walks also yield every 256 bytes after writer initialization.
Record-validation walks yield every sixteen records.
Wipe yields between its two slot-erase verification walks.
These placements service long Milan commands, including 8x8 slot status.
Long BIOS built-ins remain a residual under the round-2 decision.
Examples include `mem_test` and large-range `mem_read`.
Their bodies provide no internal heartbeat or PHY service.
They can exceed 500 ms heartbeats and 250 ms PHY publication.
A built-in body can lapse backing after about 1,750 ms.
The 2,000 ms deadline includes up to 250 ms beforehand.
That phase can suppress the dispatch heartbeat write.
The dispatch hook services their boundaries only.
The existing heartbeat rate limit remains 250 ms.
The idle hook supplies opportunities while the console awaits input.
This interval is half the section 9.4 maximum.
When `PP_NVM_STAT` reports `nvm_dirty` for a whole debounce
window (1,000 ms, the first-dirty policy ruled by
[D3 DR2a](../design/SAVED_STATE_MATERIALIZATION.md#151-manager-decision-register)) with no record
operation and no commit bracket in flight, the idle hook commits: the container is sealed
```

### Hunk 2 before (conflict as presented, lines 1955-1996)

```text
<<<<<<< HEAD
Capture copies use aligned 32-bit loads and stores within records.
Unaligned edges retain byte accesses.
No access crosses the next record's boundary.
Open records retain their previously verified staged bytes.
The [capture receipt](../../tb/verilator/nvm_capture_cpu/measurements.json) binds firmware and processor identities.

Firmware also publishes PHY state through the existing MDIO window.
Clause-22 reads obtain link, negotiated speed and duplex.
MDIO sampling follows IEEE 802.3 section 22.3.4.
Two turnaround clocks precede data sampling before each rising edge.
This matches the pinned LiteX `libliteeth/mdio.c` reader.
BMSR latch handling publishes a latched loss, then resolves current state in the same poll.
A second MDIO read separates the loss and recovery publications across the CDC.
Repeated stable readings leave the fabric edge counters unchanged.
Missing acknowledgements and incomplete negotiation publish link down.
Discovery probes one PHY address per service opportunity.
The link-status CSR feeds MAC_STATUS and the existing fabric consumers.
The stated maximum publication period is 250 ms for the measured duties.
The poll trigger is 125 ms, half that allowance.
The other half covers the longest measured duty stretch, UART blocking and a poll charge.
That charge is the measured complete poll plus nine maximum measured MDIO transactions.
Nine reads bound discovery and the longest negotiation fallback.
Using the complete poll as bookkeeping allowance deliberately counts transaction time twice.
The service harness grades this derived publication bound against 250 ms.
The findings page records transaction and complete-poll timings on the target CPU.
[Issue #599](https://github.com/kebag-logic/milan-fpga/issues/599) retains the physical switch-cycle rerun.
=======
The adopted D3 transaction retry policy still requires implementation.
[D3 DR2c](../design/SAVED_STATE_MATERIALIZATION.md#151-manager-decision-register) permits three attempts per unchanged captured work set.
The count includes the initial attempt; failed attempts wait 1,000 ms.
The [DR2c-carrier ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5863247772) names only the port's `nvm_alarm`.
It is the only reset-sticky alarm; no status bit is added.
Firmware transaction exhaustion has no alarm of its own.
It reports `VD_*` verdict loss and never ACKs the failed slot.
[FASTCONNECT section 9.2](../design/SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven) owns the resulting `nvm_stale=1` and recovery.
That producer record stays un-ACKed; exhausting its attempts raises `nvm_alarm`.
Its limit remains three attempts, separated by 500 ms.
A later successful commit clears `nvm_stale` under section 9.2's condition.
It never clears `nvm_alarm`; an asserted alarm retains loss.
[D3 lane 2](../design/SAVED_STATE_MATERIALIZATION.md#182-lane-2-parent-scalars-and-restored-ptof) owns that change and its controls.
>>>>>>> origin/dev
```

### Hunk 2 after (merge head, lines 1940-1979)

```text
The adopted D3 transaction retry policy still requires implementation.
[D3 DR2c](../design/SAVED_STATE_MATERIALIZATION.md#151-manager-decision-register) permits three attempts per unchanged captured work set.
The count includes the initial attempt; failed attempts wait 1,000 ms.
The [DR2c-carrier ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5863247772) names only the port's `nvm_alarm`.
It is the only reset-sticky alarm; no status bit is added.
Firmware transaction exhaustion has no alarm of its own.
It reports `VD_*` verdict loss and never ACKs the failed slot.
[FASTCONNECT section 9.2](../design/SAVED_STATE_FASTCONNECT.md#92-when-it-sets-when-it-is-revoked-and-when-the-loss-is-forgiven) owns the resulting `nvm_stale=1` and recovery.
That producer record stays un-ACKed; exhausting its attempts raises `nvm_alarm`.
Its limit remains three attempts, separated by 500 ms.
A later successful commit clears `nvm_stale` under section 9.2's condition.
It never clears `nvm_alarm`; an asserted alarm retains loss.
[D3 lane 2](../design/SAVED_STATE_MATERIALIZATION.md#182-lane-2-parent-scalars-and-restored-ptof) owns that change and its controls.

Capture copies use aligned 32-bit loads and stores within records.
Unaligned edges retain byte accesses.
No access crosses the next record's boundary.
Open records retain their previously verified staged bytes.
The [capture receipt](../../tb/verilator/nvm_capture_cpu/measurements.json) binds firmware and processor identities.

Firmware also publishes PHY state through the existing MDIO window.
Clause-22 reads obtain link, negotiated speed and duplex.
MDIO sampling follows IEEE 802.3 section 22.3.4.
Two turnaround clocks precede data sampling before each rising edge.
This matches the pinned LiteX `libliteeth/mdio.c` reader.
BMSR latch handling publishes a latched loss, then resolves current state in the same poll.
A second MDIO read separates the loss and recovery publications across the CDC.
Repeated stable readings leave the fabric edge counters unchanged.
Missing acknowledgements and incomplete negotiation publish link down.
Discovery probes one PHY address per service opportunity.
The link-status CSR feeds MAC_STATUS and the existing fabric consumers.
The stated maximum publication period is 250 ms for the measured duties.
The poll trigger is 125 ms, half that allowance.
The other half covers the longest measured duty stretch, UART blocking and a poll charge.
That charge is the measured complete poll plus nine maximum measured MDIO transactions.
Nine reads bound discovery and the longest negotiation fallback.
Using the complete poll as bookkeeping allowance deliberately counts transaction time twice.
The service harness grades this derived publication bound against 250 ms.
The findings page records transaction and complete-poll timings on the target CPU.
[Issue #599](https://github.com/kebag-logic/milan-fpga/issues/599) retains the physical switch-cycle rerun.
```

## Clean-merge checks (assignment rule 2)

**`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`.** Dev (#610) changed the Contents count, added a D3 retry block (`:1093-1107`), and changed section 11's writer note (`:1300-1304`), section 12's alarm lifetime (`:1350-1352`), section 13's D3 status (`:1422-1428`), section 20 items 1, 6 (last three lines), 7 and 10, and one traceability row. This PR changed section 18's timing paragraph and table (`:1609-1673`) and section 20 item 6's capture lines (`:1790-1810`). The only shared item is section 20 item 6. It merged as this PR's capture figures (13.23352 ms, 3.7027x, 11.26648 ms, 11.06894 ms gained, 1x1 3.88779 ms, 100 MHz 9.95464 ms) followed by dev's "Debounce policy is ruled under D3 DR2a. Each writer lane still owes measured normal-load durability." (`:1811-1813`). They do not contradict:
- The receipt's figures concern capture copy time and the 24.5 ms hold limit.
- D3's text concerns debounce policy, retry attempts and alarm lifetime.
- Neither states the other's quantities.
- Section 18 carries no D3 text.

Section 20 item 8 (a SHAPE-mismatch writer "returns before it installs its service hook, so nothing heartbeats") was read against this PR's admission guard. It is still true: `nvm_started` stays clear on that path, so the dispatch hook cannot heartbeat either (`milan_baremetal.c:926,1445-1449`).

**`sw/builder/test_builder.py`.** Dev changed gate 1b's ROM mutation list and message (`:17106-17124`) and added four `test_clock_contract` functions to the main list (`:27561-27570`). This PR changed gate 1b's directive-reader count from 2 to 4 (`:13304`), two comments (`:23297`, `:23382`) and the gate-35 host fixture (`:26645`, `:26666`). The hunks are disjoint, and this PR adds no gate, gate number or main-list entry, so no gate collides. The full builder bank at the merge head is the executable check (Gate table).

## Stale-statement search (assignment rule 3)

Searches at the merge head, excluding `protocol-processor/`, `docs/history/`, other submodules and JSON receipts:

1. `rg -n '#59[029]\b|issues/59[029]\b'` over the whole tree.
2. Dev's 39 changed files: `rg -n -i 'link_status|MAC_STATUS|LINK_UP|LINK_DOWN|mdio|unwritten|never writ|nothing .*writes|no publisher|queued (console )?input|dispatch|idle hook|byte[- ]copy|word[- ](wide|copy)|24\.30246|25\.54|capture (copy|headroom)|#590|#592|#599|nvm_heartbeat_tick|service[- ]budget|#397'`.
3. `docs sw tb scripts hdl configs tests REQUIREMENTS.md README.md CONTRIBUTING.md CHANGELOG.md`: `rg -n -i 'starv|queued (console )?input|no console handler|idle hook|byte[- ]copy|byte-by-byte|word[- ](wide|copy)|24\.30246|6\.60642|0\.19754|2\.0163x|19\.79024|25\.54|four writer defects|six patches|five patches|link_status|MAC_STATUS\[0\]|never (writes|publishes)|not (yet )?publish|nothing publishes|unwritten reset|stays? flat|dispatch hook|command_dispatch|heartbeat (opportunit|tick)|tick opportunit'`.
4. The same directories: `rg -n -i 'power-on straps|reset default until|PHY management|until a driver|driver writes|software-published|link_up=1|link-down|flat (at|over)|counters? (cannot|can never) (advance|move)|hardwired constant|build-time (value|guess|constant)'`.

Reworded in commit `1f039cfe` (one line, no trailers):

| Location | Old statement | Why this PR falsifies it | New statement |
| --- | --- | --- | --- |
| `docs/integration/BOARD_PORTING_AX7101.md:107-111` | MAC_STATUS "reports its reset default until a driver writes it. Until then the data path runs on the PHY power-on straps." | This PR's firmware is that driver: it reads Clause-22 link, speed and duplex and writes `link_status` (#599; `REGISTER_MAP.md:412-417`). | The firmware reads link, speed and duplex and writes the CSR; it writes no PHY register (`milan_baremetal.c` has `phy_mdio_read` only), so the PHY still negotiates from its straps; physical switch-cycle acceptance remains on #599. |
| `docs/findings/README.md:12` | Scope "using unchanged firmware"; state "architecture decision and bench proof remain open" | This PR rewrote `397_SERVICE_BUDGET.md` to measure the #590/#592/#599 repairs under the one-hart decision (#397 comment 5857491046, cited at `BAREMETAL_FIRMWARE.md:72`). | Scope "after the #590, #592 and #599 repairs, with external markers"; state "Simulation measurement under the one-hart decision; future duties, physical torture and bench proof remain open". |

Examined and left unchanged:
- `docs/findings/394_387_E1_SWITCH_CYCLES.md:185-187,282,298` (dev's new page). These record the 2026-09-27 bench run of the `9e9954e9` image. "Nothing in this build writes it" is still true of that measured image.
- `docs/findings/117_GPTP_SILICON_EVIDENCE.md:354,503`. A dated observation.
- `docs/design/SAVED_STATE_FASTCONNECT.md:61,1341`. Dated (2026-09-06) and still true: the idle hook still heartbeats every 250 ms.
- `sw/litex/milan_soc.py:1774-1799`. A conditional comment ("a build whose software never writes this register").
- `REGISTER_MAP.md:412-417`, `MILAN_COMPLIANCE_MATRIX.md:192`, `397_SERVICE_BUDGET.md` and `tb/verilator/fw_service_budget/README.md`. This PR's own reviewed text.

Not reworded, outside what this round may change:
- `tb/verilator/nvm_capture_cpu/sim_main.cpp:42` says "record walk and byte copy". The copy is now word-wide with byte edges. The capture receipt hashes this file (`harness_sha256.sim_main.cpp`), so any edit forces a capture re-measure.
- `sw/litex/litex_pins.txt:30` says "the six patches"; the series has four. That was already wrong at the previous merge base (three patches), so this PR did not falsify it.
- `hdl/milan/milan_datapath.sv:2077` says "constant 1 on boards without HW tracking". This is an RTL comment and was not changed by this PR.


## Gate table

Every gate ran at `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` on the physical `$LANES/590-592-599-firmware` path. Output went to log files and was never piped. The worktree was clean before and after, and HEAD was unchanged.

- Receipts: `gates.json`, `regrade-gates.json`, `probes.json`, `builder-gates.json`.
- `audit.py` → `audit.json`: 42 records, every log re-hashed, no file over 200 KB.
- Diff-based gates use the merge's dev parent `7a7582f0` as base. It is `git merge-base HEAD origin/dev`, the base `check_em_dash.py` names (assignment rule 4). Round 3 used the then-merge-base `20aa4eabf`.
- Markdown and source gates ran under the pinned Markdown environment (`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3`). The builder ran under the LiteX environment round 3 used.

| Gate | Command | rc | Seconds | Notes |
| --- | --- | --- | --- | --- |
| Full builder bank, compiler present, with firmware census | `sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | 953 | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11 calibration, report absent (as in every earlier round). Dev's four `[clock contract]` checks, gate 1b and the gate-35 host link pass. |
| Full builder bank, compilers absent | `full-builder-absent.py` (round-3 wrapper, same SHA-256) | 0 | 663 | `EXCEPT 2 NOT RUN`: the intentional gate-1b compiled census omission and gate 11; `FULL BUILDER ABSENT PASS` |
| Host firmware self-test | `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 59 | 5 shapes; disabled-writer, link-guard and PHY mutants caught. Log identical to round 3's apart from blank lines. |
| Capture receipt | `scripts/check_nvm_capture.py` | 0 | 0.7 | census, clocks, both arms, receipt, planted controls |
| Kept native capture oracles | round-3 `verify_packet.py`, read-only | 0 | 0.1 | 135 artifacts re-hashed; 96 captures regraded; byte-only control |
| #397 harness, portable | `tb/verilator/fw_service_budget/run.py --self-test` | 0 | 0.6 | 47 grading checks |
| **#397 harness, kept logs** | round-3 `run.py … --regrade` × 15, commands unchanged | **1 each** | ≤ 3 each | **`RuntimeError: stale or unbound build; rebuild`** (`run.py:615`), see STOP finding. The 65,145 round-3 build files were unchanged by the run. Superseded by the merge-head re-run: 15 of 15 rc 0 (continuation gate table). |
| CI scope | `scripts/ci_scope.py --selftest` | 0 | 2.6 | |
| Docs gates | `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `gen_toc --check`, `check_em_dash --base 7a7582f0` | 0 | ≤ 4.4 each | em-dash: 0 findings over 555 added lines in 11 pages |
| Source checks | `check_feature_status --self-test`, `pp_srcs --check`, `check_baremetal_only --check`, `check_entity_shape --self-test`, `check_py_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `measure_test_evidence --check` | 0 | ≤ 41 each | |
| Whitespace | `git diff --check 7a7582f0` | 0 | 0.04 | |
| Reviewer probes, unchanged | phase, disabled writer, built-in oracle, `edge-cross` (expected raw rc 1), product link guard (this round's copy writes only to this round's directories) | 0 (graded) | ≤ 31 each | Phase, disabled-writer and edge-cross logs are byte-identical to round 3's final-head logs. |

## STOP finding

**Gate:** #397 kept-log regrade (`run.py … --regrade`), all 15 kept round-3 native service runs. **Result:** rc 1 on every run, with `stale or unbound build; rebuild`.

**Cause.** `run.py` (`:612-615`) reuses a build only if `build_hashes()` still matches the hashes bound at build time. `regrade-drift.json` recomputes them at the merge head for all 15 kept builds (156 bound entries each). In every build exactly three entries differ, and the merge changed all three:

- `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`: dev PR #597, "Bind processor unit counts from the generated entity model". `N_CONTROL_P` is added and wired into the processor shadow, along with the audio-unit and clock-domain counts.
- `sw/litex/milan_soc.py`: dev PR #596, the bare-metal clock-contract CLI refusal and help text. The CSR map is unchanged.

The harness is doing what it was built to do. It refuses to carry round-3 native service evidence onto a build whose RTL and SoC inputs changed. At `93262f25` the same logs regrade rc 0 (round-3 packet `final-target-gates.json`). This is not a defect in this PR's code. The assignment's gate set cannot all be rc 0 at the merge head without new native service runs.

**Related, not failing.** `check_nvm_capture` passes at the merge head. The capture receipt binds firmware, census, clocks and harness scripts, not RTL. The capture was also measured on pre-merge RTL (tree `1ced48e2`), so the #597 change does not trip it.

**Decision needed:**
- (a) Re-run the 15 native service runs (12 positive plans, target `late-sample`, and two `remove-dispatch` controls) at the merge head, then regrade. In round 3 these took about 39,000 s of runs.
- (b) Accept the round-3 regrade at `93262f25` together with the recorded drift as sufficient for this merge.

Executor's recommendation: (a). #597 changes the processor-shadow instance the service harness simulates.


## Native re-run at the merge head

**Disposition.** The #590 [A10] comment 5870597087 chose option (a):
1. Re-run and regrade all 15 native service runs at `1f039cfe`.
2. Re-measure the capture if its harness elaborates a file the merge changed.
3. Make no other change.

**Tree unchanged.** HEAD `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` and tree `9ce926b910ca80772667bb5722eb6ded5e93d223` were the same, and the worktree clean, before and after every step. The processor gitlink stays `16be6768f710e79450aace277abacd6c2c3336e5`. No commit was added, amended or pushed.

**Runner.** `run_native.py` carries round 3's arguments, environment and STOP conditions (8x8 capture over 24.5 ms; MDIO charge over 50 ms).
- Builds run one at a time; simulations run in parallel under `taskset -c 32-63`.
- Build directories are fresh, under `$VALIDATION_STORAGE/590-a422/native/`.
- 25 arms:
  - the 15 service runs: 12 positive plans, target `late-sample`, and `remove-dispatch` on `queued-builtins` and `queued-short`;
  - the `no-publish` control, supplementary and not regradable by design;
  - six capture arms;
  - three capture controls: `byte-only`, `skip-copy` and `no-traffic`.
- 65 commands, all rc 0, all at `1f039cfe`: 25 builds, 25 measurements and 15 immediate regrades (`native-commands.json`).
- Wall time 15:19:03 to 17:10:48 CEST, about 6,700 s. Command time totals 49,575 s. No STOP condition occurred.

**Evidence.** `native-evidence/` holds 138 artifacts: every build log, run log, raw log, receipt and spec. Each is bound by raw and stored SHA-256 and size in `native-artifacts.json`, and gzip-compressed above 200 KB. No binary was copied.

### Continuation gate table

| Gate | Command | rc | Result |
| --- | --- | --- | --- |
| Native arms | `run_native.py` | 0 | `ALL NATIVE MEASUREMENTS COMPLETE: 25 arms at 1f039cfe…` (`logs/run_native.out`) |
| **#397 harness, all 15 service runs** | `regrade_native.py`: restores each raw log and receipt from `native-evidence/` into its build, then runs `run.py … --reuse-build --regrade` | **0 each** | `PASS: all 15 retained service runs regraded at 1f039cfe…` (`native-regrades.json`; `logs/final-regrade-*.log`, five gzip-compressed) |
| Round-3 comparison | `compare_round3.py` → `round3-comparison.json` | 0 | See below |
| Retained native capture oracles | `verify_packet.py` (this packet) | 0 | `PASS: 138 retained native artifacts; 96 captures match the committed receipt; byte-only control` |
| Capture receipt | `scripts/check_nvm_capture.py` (pinned Markdown environment) | 0 | Byte-identical to the first-session log (`9a4196c7…`) |
| Packet audit | `audit_rerun.py` → `audit-rerun.json` | 0 | Every artifact and regrade log re-hashed; no file over 200 KB |

### Result: byte-identical to round 3

The comparison rebuilds both packets from their stored artifacts.
- **Service.** All 16 raw simulation logs (the 15 runs and `no-publish`) are byte-identical to round 3's. Every graded receipt field is identical: rows, events, heartbeat, liveness, PHY statistics and findings.
- **Capture.** All nine capture logs and all eight measurement JSONs are byte-identical: six arms plus the `byte-only` and `no-traffic` controls; `skip-copy` writes none.
- **Bound hashes.** The only differences are in bound build hashes:
  - the three merged inputs, `KL_pp_shadow.sv`, `milan_datapath.sv` and `milan_soc.py`;
  - the generated files `sim.v`, `Vsim`, `bios.elf`, `csr.h`, `soc.h`, `mem.h`, `git.h` and the two `adp_shape_defaults.svh` copies.

  In the measurement-input hashes, only `milan_soc.py` differs. `logs/build-delta-service-1x1-all.log` shows three things:
  - generated headers and `sim.v` differ only in LiteX timestamp lines;
  - `adp_shape_defaults.svh` gains only `localparam int AEM_N_CONTROL_C = 1;`;
  - `bios.bin` is identical.
- **Reason.** For both AX7101 shapes, #597 passes `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P` and `N_CONTROL_P` from `AEM_N_AUDIO_UNIT_C`, `AEM_N_CLKDOM_C` and `AEM_N_CONTROL_C`. All three are 1, equal to the `protocol_processor_top` defaults (`protocol-processor/hdl/top/protocol_processor_top.sv:81-83`). So the elaborated processor parameters are unchanged.

Service figures from this round's receipts:
- Positive plans: all twelve pass with `budget findings: 0` and zero service findings.
- Largest heartbeat gap: 322.47884 ms (8x8 `all` and `queued-input`).
- Largest MDIO transaction: 0.12457 ms. Largest complete poll: 0.83375 ms.
- `remove-dispatch` on `queued-builtins`: 1051 per-line dispatch findings plus heartbeat-gap and backing-lost findings; gap 8238.99253 ms.
- `remove-dispatch` on `queued-short`: 350 per-line findings; gap 2770.22295 ms.
- Target `late-sample`: "PHY initial gigabit negotiation was not published".
- `no-publish`: "missing publication caught by target simulation".

Because every graded field is identical, round 3's derived figures also stand, for example the 120.53971 ms worst 8x8 duty plus UART plus charge.

**Capture.** It was re-measured because it elaborates two merged files. Each arm's `sources.json` lists 118 sources and nine include directories. The list is identical to round 3's after normalizing build paths, and it includes `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`. The capture `soc.py` also imports `milan_soc` and `endstation_builder`.
- All 96 captures equal the committed receipt rows.
- Every receipt-bound identity is equal: CPU netlist, instrumented firmware, BIOS, gPTP microcode and configuration.

| Shape | CPU MHz | Traffic | Minimum to maximum ms | 49 ms floor ratio |
| --- | --- | --- | --- | --- |
| 1x1 | 50 | on | 3.87674 to 3.88779 | 12.6036x |
| 1x1 | 50 | off | 3.82856 to 3.84214 | 12.7533x |
| 8x8 | 50 | on | 13.21274 to 13.23352 | 3.7027x |
| 8x8 | 50 | off | 13.04976 to 13.06923 | 3.7493x |
| 8x8 | 100 comparison | on | 9.94138 to 9.95464 | 4.9223x |
| 8x8 | 100 comparison | off | 9.93764 to 9.94094 | 4.9291x |

Controls:
- `byte-only`: 24.30310 to 24.30446 ms, 1.83648x against the 1.5x bound.
- `skip-copy` and `no-traffic`: caught by their named oracles.

The new figures equal those in `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6, and in the committed receipt. So neither was edited (disposition item 3).

Receipts: `native-commands.json` `0694ee02…`, `native-artifacts.json` `4f0c35ec…`, `native-regrades.json` `4b8f12f8…`, `round3-comparison.json` `c9b82d8c…`, `audit-rerun.json` `3d5df6f3…`.

### Open points

- **Measured-commit lines.** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1614` and `docs/findings/397_SERVICE_BUDGET.md:37` still name `26a26e1f` as the measured commit. The merge-head runs reproduce those measurements byte for byte and no figure changed, so disposition item 3 leaves the text alone. A reviewer who wants the pages to name the merge-head reproduction would need a docs-only commit.
- **Dev has advanced.** Remote dev moved to `ce550952e47fbd92367f0d9b099345100f7f4215` after this merge, with #612 and #613 (`logs/dev-advance-files.txt`, 18 files).
  - It re-pins protocol-processor to `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` and changes `sw/litex/milan_soc.py`.
  - `milan_soc.py` and 45 processor sources are bound by the service builds and compiled by the capture harness.
  - A candidate merge with the live dev tip would therefore make this native evidence stale again: the service harness would refuse it. The candidate would also not keep the `16be6768` pin.
  - `git merge-tree --write-tree HEAD origin/dev` is clean (tree `c6e14332…`, `logs/merge-tree-ce550952.txt`). No merge was made; that is outside this round.


## Delivery

- Commits `9e3df3ed` (merge) and `1f039cfe` (stale statements) are local only. Nothing was pushed, and no PR was created, edited or merged.
- No RTL, firmware, builder, processor or configuration edit. The only changes are the conflict resolution and the one stale-statement commit.
- Public: TAKEN https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5869864538; STOP https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5870577289 (text in `STOP.md`); after the [A10] disposition, REVIEW READY https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5872924337 (text in `REVIEW-READY.md`).
- Continuation files: `run_native.py`, `run_capture_native.py` (byte-identical to round 3's), `regrade_native.py`, `compare_round3.py`, `verify_packet.py`, `audit_rerun.py`, their JSON receipts, `native-evidence/` and the new `logs/` entries. The continuation's build trees stay under `$VALIDATION_STORAGE/590-a422/native/` (about 25 builds, not copied). The only repository state changed was the `origin/dev` remote-tracking ref, which a read-only fetch moved to `ce550952`.
- Packet files: `run_gates.py`, `run_regrades.py`, `run_probes.py`, `product_link_guard.py`, `run_builder.py`, `full-builder-absent.py` (round-3 copy), `audit.py`, their JSON receipts, `regrade-drift.json` and `logs/`. Builder logs are also kept in full under `$VALIDATION_STORAGE/590-a422/`. Nothing over 200 KB is stored here.
- Read-only inputs: the round-3 packet (`verify_packet.py`, `final-target-gates.json`, `native-*.json`) and the round-3 build trees under `$VALIDATION_STORAGE/590-a411/` (service builds and the BIOS objects for the link-guard replay).
- A concurrent builder bank from another lane (`607-xdc-clock-names`, its own worktree) was running when this round's bank started. The builder uses only per-worktree outputs and unique temporary directories, and both modes here returned the round-3 verdicts.
