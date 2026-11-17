[R861] POSITIVE - exact head d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0

# R861-2: narrow delta re-review of PR #944 (issue #936)

Round R861-2 is an internal, cleared-context review of the split AECP's unsolicited GET_STREAM_INFO notice on a Talker's declaration and withdrawal.

- **Head:** `d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0`, tree `e8705c7ca87bb1d0f49be28e78bc54b93192ec1f`.
- **Delta judged:** `7cfb8a04..d1aa4c44`, six commits: `343dfe43`, `bc921e68`, `33f24ca3`, `57a10c8d`, `83f1785f`, `d1aa4c44`. 18 files, +477/-59.
- **Code the delta does not touch** keeps its round-1 verdict at `7cfb8a04`.

All five lenses were applied to the delta. Both round-1 findings are closed at their cause. No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and two SUGGESTIONs are recorded below.

## Round-1 findings, resolved or retained

| Finding | State at this head | Evidence |
|---|---|---|
| R862-1-F1 MAJOR: no harness row timed a real declaration or withdrawal to the last controller's notice | **RESOLVED** | See check 1 below. |
| R861-1-F1 MINOR: the pass that takes SRP's record reported nothing owed, so the loop could go idle with the notice unsent | **RESOLVED** | See check 2 below. |
| R862-1-R1 RESIDUE: the comment in `ctrl_memory.py:247` named a lane | **RESOLVED** | `sw/litex/ctrl_memory.py:246-248` now carries R862-1-R1's exact replacement ("debt owed to the cold-code and descriptor move to QSPI (#665 decision D3)"). The 59.5 entry's reason string still says "debt owed to S14". That string is data, not a comment, it predates this round, and existing instances are #746's. |
| R861-RES1 / R862-1-R2 RESIDUE: the dest-MAC owed row said "no issue owns it" | **RESOLVED** | The owner is now `#943` in `tb/verilator/milan_dp/README.md:1382` and in `twin_compare.py:488`'s label. The live PR body names #943 at lines 10, 29, 132 and 217. No "no issue owns it" text remains. |
| R861-RES2 RESIDUE: same comment as R862-1-R1 | **RESOLVED** | As R862-1-R1. |

## The five delta checks

### 1. `bc921e68` + `d1aa4c44`: the `talker-notices` arm (closes R862-1-F1)

**What the arm does** (`tb/verilator/ctrl_service_budget/talker_notice.py:133-167`):

- Each group registers `AECP_REGISTRATIONS` (16) controllers and starts a save, as `notice-retried-<k>` does.
- It then times two events on source 0:
  - a real PROBE_TX, answered SUCCESS, which opens the DA gate and makes SRP declare the Talker;
  - a peer's range-taking MAAP ANNOUNCE, which closes the gate and makes SRP withdraw it.
- Each row runs from the event's mailbox RX commit (`rxc:acmp`, `rxc:maap`) to the last of the 16 registrations' STREAM_OUTPUT 0 GET_STREAM_INFO commits (`notify:<aecp>:000f:6:0`).
- The declaration's row ends at the later of the notice and the PROBE_TX response.
- The event comes `k` ms (k = 0..7) into `notice_window.RUN_MS` = 130 ms of the existing load (`loaded`, `:106-130`).
- The stream observation answers at every attempt (`FIXTURE_EDITS`), as R862-1 required.

**Bound.** The row uses the existing `notify` family's 20 ms (FR_NFR 3.4.1). The delta adds or moves no bound: it does not touch `scenario.py`, the contract, `FR_NFR.md`'s figures or `notice_window.py`.

**Fail paths.**
- A late row fails an unplanted run whatever `--record-*` records (`run.py:706`, `late` carries `notice_misses`).
- A row with no notice is a refusal, which also fails the run.
- The self-test checks both. I ran it: `receipts/budget-selftest.log` reports "self-test: 0 failures", rc 0, and the four talker-notice checks at lines 881-884 PASS.

**Results** (author receipts `receipts/budget/r4-tn1`, `r4-tn8`, `talker-notice-rows.md`; I verified their hashes):
- 1x1/1if: 16 rows, 2.043 to 6.887 ms, 16 of 16 recipients each, 0 refusals, rc 0.
- 8x8/1if: 16 rows, 2.245 to 7.553 ms, same counts, rc 0.
- Each leg's `ctrl_app.elf` is identical to the fixture arm image built at `d1aa4c44` (`images/image-identity.txt`).

**Controls**, each at 1x1/1if (`talker_notice.py:83-101`, `run.py:604-620`):
- `declared-notice-dropped`: all 16 rows have "no end: no notification", 0 of 16 recipients each, and nothing else is refused.
- `declared-notice-delayed`: all 16 rows are OVER, at 26.6 to 30.6 ms, about the 25 ms hold plus the base path.
- So each control fails the rows for its own reason.

**The withdrawal row is not satisfied by another path.** Under the dropped plant, the only change is that the bridge no longer raises from `srp_noticed`. With it, no STREAM_OUTPUT 0 notice follows the ANNOUNCE at all. So the withdrawal row's notice comes from SRP's record through the bridge.

R862-1's required outcome is met: real event origin, answering observation, 16-recipient population under load, both points, no restarted origin, and a named failing control. The acceptance claim in REVIEW READY is restated against these rows.

### 2. `33f24ca3`: the taken record is reported owed (closes R861-1-F1)

**The fix.** `sw/firmware/ctrl/app/ctrl_app_srp.c:66-77` computes `noticed` before it clears each interface's record, and seeds `pending = noticed` (returned at `:123`).

**Why this closes the gap:**
- SRP sets `i->noticed` in `declare_sources` (`srp_mbx.c:352`), reached only from THE TRANSMIT's build (`srp_mbx.c:1288` → `change_domain`).
- That build runs at the pass's start (`ctrl_loop.c:268`), before the polls. So the delivery takes the record in the same pass.
- That pass now reports owed work.
- In the next pass, the bridge raises `aecp_changed` (`ctrl_app_aecp.c:206-213`), and THE RETRY sends the first notice in the same pass (`ctrl_loop.c:333`).

**Tests.**
- `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed` (`test_aecp.cpp:788`) steps single passes from an idle loop. It requires both controllers' notices by the first idle pass, on interface 0 and on the last interface.
- `SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice` (`srp_gate.hpp:373`) uses a real PROBE_TX and its 15 s expiry, and requires the taking pass to return nonzero.
- I built the host suites at this head and ran them (`receipts/head-tests.txt`): the App pair at if1 and if2, and SrpGate F936* with the re-anchored binding test at three SRP points. 13 OK, 0 FAILED.

**Plants, caught by name in the author's campaign receipts:**
- `app-output-notice-owed-unreported` (`aecp_notice_mutants.py:33`): `[ok]` in `firmware-aecp-mutants`.
- `talker-notice-owed-unreported` (`srp_talker_mutants.py:281`): `[ok]` in `firmware-srp-mutants`.
- Both campaigns report 0 ESCAPED (`workflows/logs/rtl-fast__firmware-*-mutants__ci_step_9.log`).

**My own falsification** (`scripts/owed_probe.py`, run through the AECP campaign's own plant/build/caught machinery on a disposable checkout):
- `rv-owed-read-after-clear`: the record is read after it is cleared. **Caught.** No notice was sent by the first idle pass, which is R861-F1's defect itself.
- `rv-owed-first-interface-only`: only interface 0's record is reported. **Caught** by the test's last-interface case.
- `rv-control-noop`: a comment-only edit. Correctly **not caught**; the campaign reports it ESCAPED, as a control should be.
- Receipts: `receipts/owed-probe*.log`.

### 3. `83f1785f`: the re-anchored SRP plant

`binding-poll-adds-access` (`srp_mutants.py:684`) changes only its anchor, from `bool pending = false;` to `bool pending = noticed;`.

It keeps the same injected `(void)mbx_irq_status();`, the same file, the same suite, the same test (`SrpBinding.BindIsDeferredAndKeepsEverySinkAndInterface`) and the same required words. It is not weakened.

### 4. `d1aa4c44`: the size-rule refactor

- **AECP plants moved unchanged.** The five `app-output-notice-*` rows are byte-identical between the removed `aecp_mutants.py` lines and `aecp_notice_mutants.py:8-37`. They are composed back at `aecp_mutants.py:875`.
- **Harness code moved.** `build.py` now takes `talker_notice.PLANTS` and `talker_notice.VARIANTS` instead of the inline `valid-destinations` entry. `VARIANTS['valid-destinations']` keeps the same `talker_window.FIXTURE_EDITS`.
- **`run.py` branches split into functions.** `talker_row`, `talker_table`, `print_notices` and `declared_verdict` are new. The retried notices' NOTICE line and table are unchanged for non-talker rows.
- **No limit raised.** The delta touches no file under `scripts/`. `check_py_idiom.py` at this head passes with "long function: 9 <= 9" and "long module: 10 <= 10" (`receipts/py-idiom.log`).

### 5. `57a10c8d`: the ledger and docs figures

Every figure in `SPLIT_CONTROL_MEMORY.md:145,546-556` and `ctrl_memory.py:269` matches the author's image receipts at `d1aa4c44`:
- fixture and arm images: `images/d1aa4c44/fix.txt`;
- platform images: `final-head/r4-img.log`, where `plat_ledger` PASSes at all four points.

The arithmetic is in `receipts/ledger-arith.txt`:
- rom growth over the base is +192 to +232 B, the most at 1x1/2if;
- sram growth is +16/+32 B in the fixture and 0/+64 B in the platform;
- the three arms are 164, 16 and 72 B past 59.0, each within 59.5;
- the fixture has 144 B spare, and the platform has 1,144 and 680 B left.

The release image's `bios.bin` matches the base at both shapes (`images/d1aa4c44/rel.cmp` against `rel-base.cmp`: 1x1 `860d4771`, 8x8 `d8851b6d`).

## Findings

### R861-2-RES1 RESIDUE (Docs): the arm's figure reads as a one-interface figure

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:145`.
- **Evidence:** The sentence says "its `talker-notices` arm, run at one interface, 127,048 B there, 72 B past". But 127,048 B is that arm built at the fixture's 8x8 two-interface point. At one interface it needs 112,808 B (1x1) and 125,464 B (8x8), as `:555` and `fix.txt` state.
- **Impact:** Wording only. No figure, check or verdict changes.
- **Exact fix:** Replace "and its `talker-notices` arm, run at one interface, 127,048 B there, 72 B past" with "and its `talker-notices` arm, which runs at one interface, 127,048 B at this point, 72 B past".
- **Verification:** Inspect the sentence.

### R861-2-RES2 RESIDUE (Docs): the 59.5 entry's reason omits the third arm

- **Where:** `sw/litex/ctrl_memory.py:268-271`, the reason string of the `8x8-two-interfaces` ledger entry.
- **Evidence:** It names `answering-every-port` (164 B past 59.0) and `valid-destinations` (16 B past). It omits `talker-notices` (127,048 B, 72 B past), which the docs' section 3 lists among the arms the 59.5 entry carries. Nothing reads the string's figures; a repository grep finds them only here and in the doc.
- **Impact:** Wording only. No figure, tile, check or gate changes.
- **Exact fix:** After "and its valid-destinations arm 126,992 B, 16 B past", insert ", and its talker-notices arm 127,048 B, 72 B past". Keep the rest of the string unchanged.
- **Verification:** Inspect the string. `plat_ledger` and the ledger test are unchanged.

### R861-2-S1 SUGGESTION (Tests): run the controls at 8x8/1if too

- **Where:** `talker_notice.PLANTS`, README `:1480-1490`.
- **Evidence:** Both controls are run, and documented, at 1x1/1if only. R862-1 asked for a failing control without naming a point, so this is met.
- **Optional:** Run the controls at 8x8/1if as well, so the 8x8 row is shown able to fail on that image.

### R861-2-S2 SUGGESTION (evidence hygiene, author packet only, not PR content)

- **Where:** `review-evidence/936-r1/author-r2/receipts/INDEX.md`.
- **Evidence:** 275 of 277 receipts match their size and sha256 (`receipts/evidence-verify.txt`). The two `docs-gates` gate-25 logs (`docs__docs-gates-1__gate_25_0.log`, `docs__docs-gates-2__gate_25_1.log`) are 8 and 12 B shorter than indexed, apparently from a scrub after indexing. Their `.rc.txt` files match and record 0.
- **Optional:** Regenerate the index after the final scrub.

**Observation, not a finding.** REVIEW READY cites "304 caught" (AECP) and "447 caught" (SRP). The campaign logs hold 309 and 466 `[ok]` lines, which include control rows such as the lwSRP pin check. Both have 0 ESCAPED.

**Comment rule:** I found no new lane label, round, reviewer ID or comment ID in any added source comment in the delta. Lane names appear only in docs prose, which the rule allows.

## Lens results (each with its artifact)

[R861] PASS Conformance - `talker_notice.py:133-167`, `run.py:604-620,706`, `ctrl_app_srp.c:66-77`, `ctrl_app_aecp.c:206-213`, author `talker-notice-rows.md` (r4-tn1, r4-tn8, r4-dr1, r4-de1) - a real declaration and withdrawal are timed from the event's RX commit to the last of 16 recipients' STREAM_OUTPUT 0 GET_STREAM_INFO, under the existing load, at 1x1/1if and 8x8/1if, against FR_NFR 3.4.1's unchanged 20 ms. The dropped and delayed controls fail every row for their own reason. This matches #936's frozen acceptance and R862-1-F1's required outcome.

[R861] PASS RTL - `ctrl_app_srp.c:66-77,123`, `ctrl_loop.c:268,326-347`, `srp_mbx.c:352,1288`, `ctrl_app_aecp.c:206-213`, image receipts `images/d1aa4c44/*` - the record is set in THE TRANSMIT before the polls and taken in the same pass, which now reports it owed. The notice is raised and sent in the next pass. Masks and indices are unchanged. The firmware costs +8 B of rom in five images, and the release image is byte-identical to the base. The delta has no HDL, CDC or mailbox-contract change.

[R861] PASS Robustness - `test_aecp.cpp:788` (both interfaces), `srp_gate.hpp:373` (declaration and 15 s expiry), `receipts/owed-probe*.log` - I checked the last interface, a withdrawal, the record read-after-clear ordering, partial-interface reporting and the `CTRL_MBX_WFI`-dependent sleep. The test steps `ctrl_loop_service` directly, so it holds with or without WFI. The load phases k = 0..7 meet the bursts at different phases.

[R861] PASS Tests - `receipts/head-tests.txt` (13 OK), `receipts/owed-probe*.log` (two reviewer mutations caught, no-op control not caught), `receipts/budget-selftest.log` (0 failures), `srp_mutants.py:684` (re-anchor not weakened), `aecp_notice_mutants.py` (byte-identical move), author campaign logs (0 ESCAPED) - each new test fails for the defect it claims to detect.

[R861] PASS Docs - `sw/firmware/ctrl/srp/README.md:258-276`, `sw/firmware/ctrl/aecp/README.md:101`, `tb/verilator/ctrl_service_budget/README.md:271-284,1480-1492`, `SPLIT_CONTROL_MEMORY.md:145,546-556`, `ctrl_memory.py:246-271`, `milan_dp/README.md:1382`, the live PR body - the changed contracts are documented and the figures reconcile (`receipts/ledger-arith.txt`). RESIDUE only (RES1, RES2), which leaves the lens clean.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `talker_notice.py`, `run.py` verdict paths, `ctrl_app_srp.c`, `ctrl_app_aecp.c`, FR_NFR 3.4.1 bound, budget receipts (tn1, tn8, dr1, de1) | R861-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| RTL | CLEAN | `ctrl_app_srp.c`, `ctrl_loop.c` pass order, `srp_mbx.c` record site, `ctrl_app_aecp.c`, image and release receipts | R861-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Robustness | CLEAN | `test_aecp.cpp:788`, `srp_gate.hpp:373`, reviewer mutations, load phases | R861-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Tests | CLEAN | head suites, reviewer probe, budget self-test, plant tables, campaign receipts | R861-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |
| Docs | CLEAN (RESIDUE RES1, RES2 carried to the manager's checklist) | SRP, AECP, budget and twin READMEs, SPLIT_CONTROL_MEMORY, `ctrl_memory.py`, PR body | R861-2 | d1aa4c44307edf4a9390c19cbb2c82fe5c5464d0 |

Code outside the delta keeps its R861-1 verdict at `7cfb8a04`. No delta change alters what that code depends on.

## Real limits

- **No harness run of my own.** I did not run the Verilator CPU budget harness. The talker-notices rows and controls rest on the author's receipts, whose hashes I verified (275 of 277; see S2), plus my own self-test run and design reading.
- **No full campaigns.** I did not rerun the full firmware-unit, AECP, SRP or control mutation campaigns, the docs gates, the twin or the image builds. Those results are the author's published receipts.
- **No hosted runs.** There is no hosted check run or commit status at this exact head as of this round (`gh api .../check-runs`: total 0). I infer no hosted result.
- **No manager source bank.** I neither claim nor infer one at this head. Physical calibration is NOT RUN, and field skips are not hardware proof.
- **Clone state.** My clone is byte-identical to the head: the index equals the HEAD tree in mode, blob and path, it is clean, and all six gitlinks are at their pins (`receipts/restore.txt`). All probes ran in a disposable checkout under `scratch/`.
- **Self-test retry.** My first self-test attempt was cut by a foreground timeout. The recorded run is the second one, detached with its own rc file: rc 0, with one summary line in its log.

## Pending manager duties

- Validate the current-dev merge candidate (source base `70f4056f`, live dev `e275d795`) with the builder and native banks at the merge turn.
- Remeasure the CPU budget and the ledger there.
- Resolve the known text conflicts with PR #935, #932 and #914 in the flip train.
- Own hosted and act acceptance, distinguishing executed jobs from skipped contexts.
- Carry RES1 and RES2 to the residue checklist.
- Under the owner's batch rule (#665 issuecomment-6939574513), freeze after two POSITIVE reviews.

Known, not findings: #943; the twin's stale `split-talker-failed` row (PR #935); the 1x1 held-egress growth and the 8x8 STATED retries, owed to #894.

R861-2 FINISHED
