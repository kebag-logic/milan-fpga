[R941] NEGATIVE - exact head 85569e241625d8e4176aae7d77c524783dff30cd

# R941-1: internal independent review of PR #1017 (Relates to #1009), step 1 of scope ruling 3

Reviewed head `85569e241625d8e4176aae7d77c524783dff30cd`, tree `89dc2ac457b7506fe6e76e877f8635bf757101a5`, on
`dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`: six commits, 31 files. Cleared context, detached
isolated clone. The task was reconstructed from AGENTS.md and CONTRIBUTING.md, docs/README.md, issue #1009 (body and
the three public rulings, the last, [ruling 3](https://github.com/kebag-logic/milan-fpga/issues/1009#issuecomment-7176978406),
governing step 1), REQUIREMENTS.md:482 (binding authority Milan v1.2 5.3.8.2/5.3.8.3/5.3.8.7), the DR2a/DR2c rows of
docs/design/SAVED_STATE_MATERIALIZATION.md, the store's interface documents, then the diff and history, then the
author's public packet (`review-evidence/p1win-r1` at `a7eb193a`; every file's sha256 matches its MANIFEST.json). The
#1014 findings the focus names were read after the independent pass over the diff.

**Order.** This round's own verdict and ledger were written first and are kept unchanged as
`receipts/REPORT-independent-pass.md` (its sha256 and UTC time in `receipts/independent-pass-order.txt`; that
verdict was POSITIVE). Only then was the other review of this PR, [R942-1](https://github.com/kebag-logic/milan-fpga/pull/1017#issuecomment-7182393758),
read; when this round started the PR had only two review-start notices. Its two findings are resolved or retained
below. Retaining R942-1-F2, narrowed, makes this verdict NEGATIVE and leaves Conformance, Tests and Docs unclean.

This is a source-review verdict, not merge authorization, hardware acceptance or a manager source bank. No source
fix, commit, push, GitHub write, hardware operation, container runner or edit of any other checkout was made. After
every probe the clone is byte-exact at the head: index tree `89dc2ac4...`, no status entry, submodule gitlinks
unchanged (`receipts/clone-integrity.txt`).

## What changed (independent reading)

`sw/firmware/ctrl_nvm/nvm_store.c:941-979`: `nvm_binding(id)` is the BINDING block (`id - NVM3_ID_BIND <
NVM3_CAP_BIND`, unsigned, so ids below the block wrap out); `nvm_mark` computes the change's window end, 100 ms
(`NVM_BIND_DEBOUNCE_MS`, `nvm_shape.h:150-153`) for a binding record and 1,000 ms (`MILAN_NVM_DEBOUNCE_MS`) for every
other, and keeps the earliest open end (`due_us`); a binding change the save in flight cannot take no longer sets
`next_now`, so it opens the next 100 ms window, while any other record's still starts the next save at the first idle
step (#920). `nvm_idle` (`:551-561`) captures when `now >= due_us`; `nvm_capture_begin` (`:533-543`) still closes every
window and takes everything dirty. Joining a running capture (`:958-964`), DR2c's backoff (`:555`), the commit path,
the boot and restore path and the two-slot atomicity are unchanged; the format and codec files (`nvm_klj2.c`,
`nvm_klj2.h`, `nvm_layout3.h`, `scripts/nvm_klj3.py`) are byte-identical to `2509db68`. The clock is the port's
monotonic 64-bit microsecond count (`nvm_flash.h:54-60`, `ls_now_us`), so the absolute compare is wrap-safe, as
`retry_at_us` already was. Bind, unbind and started/stopped all reach the same record through the ACMP owner's
`persist` hook (`sw/firmware/ctrl/app/ctrl_app_aecp.c:29-34,249-253`).

## Evidence run at the exact head (this round's receipts)

All from the clone at `85569e24` with a clean tree; the pinned simulator reports `5.050 2026-07-01 rev v5.050`, the
pinned RV32 SDK `riscv32-linux-gcc 14.3.0`. Commands are in `scripts/bg.sh`.

| Run | Result | Receipt |
|---|---|---|
| Store gate, `test_ctrl_nvm.py --require-rv32 --self-test` | OK across 5 shapes, 656 tests (128 a shape), RV32 arm built; all 170 planted defects reddened (165 and five compile-time controls), each of the 16 window plants by its named test | `receipts/store-gate-selftest.txt` |
| Firmware coverage, `fw_coverage.py --check --lwsrp` | PASS, 40 files; `nvm_store.c` 513/513 lines, 317/326 branches, 100 % after its stated arcs | `receipts/coverage-check.txt` |
| CPU budget harness self-test | 1,048 checks, 0 failures; 321 mutants caught, the 26 of `selftest_mutants_bind.py` each by name | `receipts/budget-selftest.txt` |
| Bind groups, 1x1/1if and 8x8/1if (12 each, the committed testbench, erase 120 ms, page 0.5 ms) | every figure equal to the author's to the microsecond; idle 304.535 / 550.481 ms (gate 800); in flight worst 394.959 / 891.169 ms just after the capture (450 / 950), the other nine 298.517-392.866 / 552.760-880.349 ms; burst each sink's last 306.463 / 646.392 ms in 4 / 2 whole saves, an erase each; 0 refusals, rc 0 | `receipts/bind-groups-*.txt`, `*-table.md` |
| Full-run cross-check, `save`, `save-flight`, `save-burst`, `backlog-owed` at both points | every figure equal to the author's regrade to the microsecond: `save` 1,075.874 / 1,298.777 ms; `save-flight` 147.073 / 650.995 ms; `save-burst` 1,097.438 / 1,353.998 ms; the seven `backlog-owed` rows 61.645-63.215 / 63.003-64.762 ms; 0 passes over the share; rc 0 | `receipts/fullrun-crosscheck-*.txt` |
| Long-window load, `load_grade.py --check` | 0.512 at 1x1/1if (0.70), 0.744 at 8x8/1if (held at 0.75, under the ruling's 0.76); PASS | `receipts/load_grade_check.txt` |
| Split-target campaign, 1x1 and 8x8, fresh builds | every case (`commit`, `valid`, `absent`, `torn`, `version`, `guard`) passes and every control is caught at both points, rc 0; the commit's one erase 128.4 ms and 206.9 ms after its changes, the head's own `windowed` grade clean | `receipts/split-target-*.txt`, `*-table.md`, `*-commit-window.txt` |
| Split-target self-test | 79 checks, 0 failures | `receipts/split-target-selftest.txt` |
| Platform ledger, `plat_ledger.py` | rom 127,640 / 129,424 / 141,744 / 143,496 B, 45.5 / 46.5 / 59.5 / 64.5 RAMB36, 0 findings | `receipts/plat-ledger.txt` |
| Reviewer probe of the verify grade (#1014 R932-1 F2) | 7 cases, 0 disagreements: a missing 4-byte tail, overlapping runs whose byte sum exceeds the image, R932-1's 4-bytes-after-a-whole-slot-blank-check shape and a page read three times are not durable; the whole image in any order is; a run straddling a page program is refused | `scripts/probe_verify.py`, `receipts/probe_verify.txt` |

## Acceptance of step 1 (ruling 3, item 3, and item 4)

| Item | Status at this head | Evidence |
|---|---|---|
| Idle store: bind, unbind, start, stop durable within 800 ms of the response, in simulation at both points | met in simulation (this round's runs); board owed | 304.535 / 550.481 ms, one save of each command's own begun after its window |
| Swept cut 0-3 s on the whole path, idle store: old or new, never neither, new from the gate | met (host model; cuts timed from the store's change, not a wire response) | `test_nvm_window.cpp:233-244`, gate 800 ms, both ports, five shapes, erase 150 ms |
| Split-target campaign at both points, case and documents matching the two windows, container checks unweakened | met (this round's fresh campaign) | both points above; `committed()` unchanged and now self-tested (`target_selftest.py:537-578`), `windowed` added (`target_grade.py:357-378`) with three mutants; README:102 and `target_cases.py` state the two windows |
| Full service-budget run at both points (notice 140 ms, ACMP 30 ms, share 2 ms, loads 0.70 / 0.76, #920's 5 s) | **evidence open (R942-1-F2, retained narrowed)** | the author's summary: 113 groups, 0 refusals, the seven `backlog-owed` misses as on the base, one 8x8 pass over the share owed to #977 by the harness's OWED registry; cross-checked exactly here on four store groups a point and the load check; the runs' `results.json`/`table.md` and exit status are not published and the run's tree is `cd9ea485` with one unidentified dirty file |
| 64-bind burst converges within item 4's bound; saves and erases reported | met (this round's runs) | 306.463 / 646.392 ms against 450 / 950; 4 / 2 saves, an erase each, cap 4 / 3 |
| Routed at the +0.030 ns floor; no ledger entry raised; block RAM not above base | met | packet `images.txt`: 8x8/1if +0.045 ns WNS, +0.036 ns WHS; 1x1/1if +0.126 / +0.036 ns; 98.5 and 80.5 tiles as the base; `ctrl_memory.py` untouched, `plat_ledger` 0 findings |
| KLJ3 minor 0, interchange with 2509db68 both ways | met | format and codec files byte-identical to `2509db68`, no boot or restore change; packet `interchange.txt` |
| In-flight bound, item 4: at most 950 / 450 ms over at least eight arrival phases including just after the capture, stated in PR and DR2a | met in simulation; board 1,000 ms at 8x8 owed | ten arrivals, each held to its phase (`bind_save.phase_of`) and to two saves; DR2a row amended (`SAVED_STATE_MATERIALIZATION.md:2394`); `swept_cut_in_flight` sweeps nine phases (`test_nvm_window.cpp:249-271`) |
| Board items (both points, 10 ms resolution, power-cycle cases at about 1 s) | owed, not a source defect | PR "Before it lands"; its resolution note may need a decision |

## The routed LUT difference: placement variance, not design growth

8x8/1if routes at 45,973 LUTs against the base's 45,814 (+159, 0.35 %), at the one pre-registered directive. The
evidence says the logic did not grow:

1. The delta changes no HDL, SoC generator or gateware file (`git diff --stat c34e7d8b..85569e24 -- hdl gateware
   sw/litex` is empty). The only netlist input that differs is the firmware ROM's contents (+64 B at 8x8, +72 B at 1x1;
   `plat_ledger`) and the image's identity strings, which differ between any two builds.
2. The firmware ROM is block RAM: `CtrlMemory` (`sw/litex/milan_soc.py:3400-3428`) builds each bank as a power of two
   of RAMB18 granules with the image's words as the RAM's initial contents, and the plan's tiles are unchanged (98.5 =
   98.5 routed, 59.5 RAMB36 in the ledger). Initial contents of a block RAM add no LUT.
3. The same kind of change moved the 1x1/1if pair the other way, 32,656 to 32,647 (-9), and moved the 8x8 registers
   53,381 to 53,375 (-6). A firmware-only change cannot remove registers from the RTL, so these counts carry the
   placement-driven physical optimisation of one placement each, which the PR already states for the slow WNS.

So the +159 is implementation variance between two placements of the same logic, not design growth. Ruling 3's step-1
acceptance has no LUT band (it names the floor, the ledger and block RAM), and no band is defined in the repository
documents searched. S1 asks for the attribution to be made reproducible by post-synthesis counts.

## Findings

**R942-1-F2 (retained, narrowed) MINOR - Conformance, Tests, Docs - author packet `receipts/win/gates.txt`
(`regrade-1x1`, `regrade-8x8-1if`); PR body "The full service-budget run at both points" - the full service-budget
run is not published in a form that a cold reviewer can tie to this head or inspect.**
Authority/evidence: ruling 3 item 3 requires the full service-budget run at both points (notice 140 ms, ACMP 30 ms, per
-pass share 2 ms); R931-1-F6, which this PR answers, names its verification as both runs' `results.json` and exit
status; AGENTS.md section 5 requires reproducible evidence at the commit. The packet publishes only extracted summary
lines of a regrade at `cd9ea485` with one dirty file not named, and no `results.json`, `table.md` or the notice and
ACMP rows. This round re-ran the store's four groups at each point at the clean head and every figure matches the
author's to the microsecond, and the regrade's reused build is refused unless its firmware digest and every recorded
input match the checkout (`build.py:947-977`), so the firmware very probably equals the head's; but the other 109
groups a point, the notice and ACMP rows among them, are not inspectable, and the dirty file is unidentified.
Impact: the acceptance item and R931-1-F6's verification rest on a summary of a run at an imprecisely identified
tree; a cold reviewer cannot check the rows the ruling names.
Required outcome: from a clean checkout at this head (or its successor), regrade the recorded runs at 1x1/1if and
8x8/1if with `run.py --point <pt> --build-dir <dir> --reuse-build --regrade --record-budget-findings` (the reuse
attestation then binds the build to the head), or re-run them; publish each point's `results.json`, `table.md` and
exit status with the log header naming the commit and a clean status.
Verification: the hashes of the published files; every row the ruling names within its budget, the seven recorded
`backlog-owed` misses and the one #977 pass the only exceptions, as on the base; exit 0; HEAD `85569e24` (or the
successor) and no dirty file in the header.
Closed parts of R942-1-F2 at this head: the split-target campaign and the bind groups (this round's fresh runs at the
clean head, published with tables and exit status) and the interchange (by source identity of the format, codec, boot
and restore code to `2509db68`).

**R941-1-RES1 RESIDUE - Docs - `sw/firmware/ctrl_nvm/nvm_store.h:22-31` - "that many centiseconds" lost its antecedent.**
Authority/evidence: the inserted parenthetical about the two windows now stands between "once every
CTRL_LOOP_STEP_AGE + 1 centiseconds" and "plus that many centiseconds for each step of its save", so "that many" reads
as the windows' milliseconds. Purely wording in a source comment: no figure, test or behaviour changes.
Exact fix: replace "plus that many centiseconds for each step of its save after the window" with "plus
CTRL_LOOP_STEP_AGE + 1 centiseconds for each step of its save after the window".

**R941-1-S1 SUGGESTION - RTL, Docs - PR body "Memory and fit"; packet `receipts/win/images.txt`.**
Publishing the four images' post-synthesis (pre-placement) LUT and register counts, which should agree within the
identity strings, would make the attribution above reproducible rather than inferred, and would let the PR state it.
If the manager reads ruling 2's "fit and timing at both 8x8 points" as still binding on step 1, the two-interface 8x8
image is not routed here (its ledger entry, 64.5, is unchanged); ruling 3's list does not name it.

**R941-1-S2 SUGGESTION - Tests, Docs - packet `receipts/win/gates.txt`, `bind-groups.txt`.**
Beyond R942-1-F2's open part: the other gate logs name the base or a docs-only predecessor with a dirty tree, and the
bind groups a testbench "as committed but for one declaration split". Every one of their figures this round re-ran
reproduces exactly at the clean head with the committed testbench, so nothing else is open; receipts naming the
commit with a clean status would make that hold without a re-run. `test_ctrl_firmware.py`, `test_ctrl_memory.py`
and the size fixture's arms were not re-run here (limits).

## The other review of this PR (R942-1), resolved or retained at this head

| Finding | Disposition |
|---|---|
| R942-1-F1 MINOR, the routed LUT excess has no attribution | **Resolved, not retained.** The attribution it asks for is answered above with artifact evidence: the delta has no HDL, SoC or gateware change; the only differing netlist input is block-RAM initial contents, which add no LUT, with tiles unchanged; the same change moved the 1x1 pair -9 and the 8x8 registers -6, which logic growth cannot do. So the +159 is not design growth, and ruling 3's step-1 acceptance names no LUT band. Its remaining ask, intermediate-stage counts, is S1. |
| R942-1-F2 MINOR, packet does not establish source identity | **Retained, narrowed** to the full service-budget run (finding above). The split-target campaign and the bind groups are closed by this round's fresh exact-head runs, and the interchange by source identity. |

## The #1014 findings the focus names, at this head

| Finding | Applies to the whole path | At this head |
|---|---|---|
| R931-1 F1, split-target campaign fails | yes | **closed**: the `commit` case marks every record at the first centisecond after the rename (`target_cases.py:57-74`), its erase is graded at the binding records' window (`target_grade.windowed`, bounds 50-500 ms, three mutants), `committed()` is unchanged and self-tested; the whole campaign passes at both points in this round's fresh runs, the erase 128.4 / 206.9 ms after the changes; `commit_ms` and README:102 state the two windows |
| R931-1 F2, a bind arriving during another save is over 800 ms | yes | **closed by ruling 3 item 4**: the stated bound (rest of that save plus one save) is in the PR, DR2a (`SAVED_STATE_MATERIALIZATION.md:2394`), `nvm_store.h:36-41`, the store README and `SPLIT_CONTROL_MEMORY.md:1923-1925`; ten harness arrivals hold it (891.169 / 394.959 ms worst against 950 / 450, re-run here); `swept_cut_in_flight` sweeps nine phases with the gate |
| R931-1 F6, CPU bounds not executed at the head | yes | **open in its evidence (R942-1-F2)**: the run exists and its store groups reproduce exactly here, but its stated verification, both runs' `results.json` and exit status at the head, is not published |
| R931-1 F7, the bind grade does not hold what it states | yes (frames do not exist in step 1) | **closed**: `whole_faults`, `idle_faults`, `burst_faults` (erases against `saves_max`), `flight_faults`; the run's modelled times are recorded in `SUMMARY` and a mismatch refused (`flash_times`); 26 bind mutants caught here |
| R931-1 F8, wrong figures | yes, the items present in step 1 | **closed**: README counts (76 checks, 128 tests, 52 + 12 + 5 + 5 + 2; 165 defects and five controls = the 170 the gate executes here), the zero-busy-time statement corrected, harness README:90 and `save_window.py:1-21` restated for the 100 ms window, `SPLIT_CONTROL_MEMORY.md:327` matches `ctrl_memory.py` (64.5, 61.5, 59.5, 57.5, unchanged here) |
| R932-1 F2, verify grade accepts partial post-program coverage | yes | **closed**: the testbench ends a run of reads at every erase and page program (`sim_main.cpp:326-330`), `save_grade.in_order` refuses a run that spans a write, `merged_reads` no longer merges across one, `read_back` counts each byte once and only reads begun after the last page; self-test verify checks through the bind and burst grades, four verify mutants, and this round's probe |

## Comment rule, privacy

The added lines of every non-document file carry no lane label, lane name, review round, reviewer ID or issue-comment
ID; the documents' links (DR2a's ruling link, the README's pre-existing `issuecomment-6899740728`) are permitted there.
No private name, test-plan or lab reference, or tool or model name in the delta.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R942-1-F2 (retained, narrowed) | ruling 3 items 1-7 against the table above; REQUIREMENTS.md:482; DR2a row `SAVED_STATE_MATERIALIZATION.md:2394`; `nvm_store.c:941-979`; `nvm_shape.h:150-153`; `ctrl_app_aecp.c:29-34,249-253`; `bind_save.py:47-55`; bind, cross-check and packet receipts | R941-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| RTL | CLEAN | diffstat (no HDL/SoC/gateware change); store state machine `nvm_store.c:528-561,901-979` (transitions, `next_now`, `dirty_armed`, wrap, unsigned class test); `nvm_flash.h:54-60`; `milan_soc.py:3400-3428` ROM banks; packet `images.txt` (four corners, tiles, LUT/registers; R942-1-F1 resolved); `plat_ledger` | R941-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Robustness | CLEAN | `test_nvm_window.cpp:149-271` (in flight, backoff, burst, swept cuts idle and in flight); DR2c path `nvm_store.c:555,711`; wrap-safety of the absolute compare; burst convergence and erase counts; in-flight arrivals at ten phases | R941-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Tests | UNCLEAN: R942-1-F2 (retained, narrowed) | store gate and its 170 plants (16 window plants by name); harness self-test 1,048 checks, 321 mutants (26 bind); split-target 79 checks and both campaigns; `test_nvm_write.cpp:861-863` (the call count follows the 100 ms window, the stall checks stay); `probe_verify.py`; coverage ratchet `coverage.ratchet:39` | R941-1 | 85569e241625d8e4176aae7d77c524783dff30cd |
| Docs | UNCLEAN: R942-1-F2 (retained, narrowed); RES1 residue carried | `sw/firmware/ctrl_nvm/README.md` (all hunks), `nvm_store.h:22-50`, `SAVED_STATE_MATERIALIZATION.md:2394`, `SPLIT_CONTROL_MEMORY.md:166,327,1923-1925`, harness README:90,136-155, `save_window.py:1-21`, split-target README:102, gtest README:330, `DOCUMENTATION_AUDIT.md:405`, PR body and author packet against receipts | R941-1 | 85569e241625d8e4176aae7d77c524783dff30cd |

## Limits

- Physical calibration NOT RUN; no hardware was touched. The harness's 120 ms erase is calibrated on one board reading
  of the base's save; a 160 ms part would put the in-flight worst near 970 ms at 8x8/1if, above the 950 ms simulation
  bound and under the board's 1,000 ms, as the PR states. The host swept cuts are timed from the store's change, not a
  wire response.
- Not re-run here: 109 of the 113 groups a point of the full service-budget run, `test_ctrl_firmware.py`,
  `test_ctrl_memory.py`, the size fixture's arms, the interchange boots and the routed images (built at `8a4ad2c4`,
  whose firmware and RTL equal the head's: the later commits change documents and the coverage ratchet only). A
  rebuild of the base's platform ledger was not available in this session; the base figures are the author's.
- The 8x8 two-interface image is not routed (S1).
- No manager source bank is claimed or inferred; hosted and container-runner acceptance are the manager's.

## Pending manager duties

- R942-1-F2's open part: the full service-budget run's `results.json`, `table.md` and exit status at both points
  from a clean checkout at the head (a `--reuse-build --regrade` suffices), then a re-review of those lenses.
- The board acceptance of ruling 3 (both points; response to durable for the four commands at 10 ms or better, where
  the PR's resolution note may need a decision; the power-cycle cases at about 1 s; the in-flight 1,000 ms at 8x8; the
  boot comparison).
- Carry R941-1-RES1 to the residue checklist; decide whether ruling 2's two-interface fit item binds step 1 (S1).
- The current-dev merge candidate (source base `c34e7d8b`, live dev `e275d795`): builder and native banks, hosted and
  container-runner evidence at the merge turn.

R941-1 FINISHED
