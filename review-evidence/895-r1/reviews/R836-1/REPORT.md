[R836] NEGATIVE - exact head d023b77a7bf677205e45195e0e1f0daf80d1a4d4

# R836-1: external review of PR #901 (issue #895) at exact head `d023b77a`

- Head `d023b77a7bf677205e45195e0e1f0daf80d1a4d4`, tree `ea4ed7a01cefd8a672238a19695437eca022cba7`; reviewed delta `b2d39235ab9bba85d7e560b5f5f78fb4be528960..d023b77a` (29 files, +1,252 / -141).
- Role: external, cleared-context, independent reviewer. Context rebuilt from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #895 (body as corrected, the TAKEN, STOP, ruling issuecomment-6824623445 and REVIEW READY comments), #894's and #890's owner decisions (the flip gate acceptance 4 cites), the diff and history, lwSRP, tsn-c-stack's MAAP and ACMP cores, and the author packet at `e60d35c0` (`review-evidence/895-r1`).
- No prior review finding exists on PR #901 (no review, no review comment; the two PR comments are review-start notices). Nothing to resolve or retain.
- Verdict: **NEGATIVE**. One MAJOR (acceptance 4 claimed met while two of its four bounds are not) and two MINOR (figures in the design page and in the PR/issue evidence that the head's own gate, images and campaign contradict). The firmware change itself, its tests and its plants held up under every check below; no RTL, Robustness or Tests defect was found.

## Findings

### F1 - MAJOR - Conformance, Docs - acceptance 4 is not met as written, and the PR and REVIEW READY record it as met

- **Artifact:** issue #895 body, acceptance 4; PR #901 body, Status, "Acceptance 4"; #895 issuecomment-6838154041 ("Acceptance criteria: ... 4 met"); `tb/verilator/ctrl_service_budget/load_grade.py --check` and `flip_grade.py --check` at `d023b77a` (`receipts/grades/`).
- **Authority:** acceptance 4: "1x1/1if at most 0.70 with rows by every source, and 8x8/2if at most 0.75 with rows by measurement (owner decision 2026-11-12, #894)". The #894 owner decision (issuecomment-6814835849) and #890's (issuecomment-6798229503) set the 8x8/2if flip ceiling at 0.75 and the 1x1/1if rows by every source at option B's bounds. AGENTS.md section 4: acceptance criteria are frozen; a wrong or unreachable one is a public change request. Section 2: a conflict is published and marked as needing a decision, not read privately.
- **Evidence (reviewer's runs at the head):**
  - 1x1/1if load 0.488 at the pin, 0.486 with tsn-c-stack#32: within 0.70. **Met.**
  - 1x1/1if rows by every source: `flip_grade.py --check` rc 1, `OVER 1x1/1if R4: by every source 66.77 ms, over its bound 20 ms`. **Not met.**
  - 8x8/2if load: 0.817 at the pin, 0.768 with tsn-c-stack#32. Both are over 0.75. **Not met.**
  - 8x8/2if rows by measurement: the author's least margin is 9.733 ms (arm A), positive. Not re-measured here. **Met on the author's receipts.**
  - At the base `b2d39235` (reviewer's run on an export): 0.486 / 0.483 at 1x1/1if, 0.816 / 0.767 at 8x8/2if. The lane did not cause the two misses. It moves the 8x8/2if load +0.001 and R4 +0.65 ms.
- **Impact:** section 7's bar ("all acceptance criteria are met") is not met. The public record says it is. The PR reads acceptance 4 as "8x8/2if reported", and no ruling on #895 says that. A cold reviewer or the merge turn would take the task as complete against a criterion that fails today.
- **Required outcome:** one of:
  - a maintainer decision on #895 stating how acceptance 4 applies to this lane (for example: no load or row verdict changes, with the deltas stated), with the PR's and the issue's acceptance lines restated against it; or
  - acceptance 4 recorded as not met until #890 and #894 land.
- **Verification:** the decision comment exists on #895, and the PR's Acceptance 4 line quotes it. Otherwise `flip_grade.py --check` and the 0.75 reading pass at the merge candidate.

### F2 - MINOR - Docs - `SPLIT_CONTROL_MEMORY.md` states two figures that the head's own gate and images contradict

- **(a) `docs/design/SPLIT_CONTROL_MEMORY.md:2209`:** the table "At this head (`load_grade.py --check` ...)" gives 8x8/2if's "A pass's own cost, us" as **315**.
  - `load_grade.py --check` at `d023b77a` prints **320** (`receipts/grades/load_grade.py_check.log`).
  - At the base `b2d39235` it printed 315 (`receipts/grades/load_grade_at_base_b2d39235.log`).
  - The lane moved the donor column's `base` from 285 to 290 us. It updated the 1x1/1if cell (180 to 185) but not this one.
- **(b) `docs/design/SPLIT_CONTROL_MEMORY.md:291`:** "The declarations add 800 to 1,040 B of `rom` ... an image".
  - The reviewer linked all eight images at `b2d39235` and at `d023b77a` with the same runtime archives and split exports (`receipts/rom/deltas.md`).
  - The measured rom deltas are **+944 to +1,064 B**. The 1x1 two-interface fixture and platform images grow by 1,064 B, past the stated 1,040.
  - The sram range (16 to 64 B) and `ctrl_plat` +64 B are correct.
- **Authority:** CONTRIBUTING.md section 3 ("Measure, don't assume") and the Docs lens (changed contracts and figures reflected in authoritative docs). Both are figures, so neither is RESIDUE.
- **Impact:** the authoritative memory page misstates the head's gate output and the change's ROM cost. A later lane that ledgers against it starts from wrong numbers.
- **Required outcome:** the page carries the gate's 320 and the measured +944 to +1,064 B, or states the base its range is against.
- **Verification:** `load_grade.py --check` output equals the table row, and an image link at both commits reproduces the stated range.

### F3 - MINOR - Docs - the PR body and REVIEW READY state 28 Talker plants; the table holds 26

- **Artifacts:**
  - PR #901 body: "28 planted Talker defects, each killed by its named test on its words at both points" and "`srp_talker_mutants.py` plants 28 defects".
  - #895 issuecomment-6838154041: "SRP 392 (the 28 Talker plants at both points among them)", "28 plants each killed by name at both points".
- **Evidence:**
  - `srp_talker_mutants.defects()` returns 26 entries. `srp_mutants.DEFECTS` holds 26 names with the `talker-` prefix.
  - The author's own SRP campaign log at the head has 52 `[ok] talker-` lines, which is 26 at each of two points (author packet `receipts/gates/workflows/mutant-counts.txt`).
  - The reviewer's campaign caught 26 of 26 at 1x1/1if and 26 of 26 at 8x8/2if (`receipts/run/tc*.log`).
- **Impact:** an evidence figure a cold reviewer checks acceptance 3 against is wrong. It is a figure, so it is MINOR, not RESIDUE.
- **Required outcome:** the PR body and the evidence comment state 26 (or name the two further plants that make 28).
- **Verification:** the count equals `len(srp_talker_mutants.defects(...))` at the merge candidate.

### RS1 - RESIDUE - `sw/litex/ctrl_memory.py:217` and `:223-224` (source text in the reviewed delta)

- **The rule:** owner rule 2026-10-15. Source text states behaviour and reason with issue and requirement IDs, never lane names or issue-comment IDs.
- **New instances:** the lane added "(#895, ruling 6824623445)" twice, an issue-comment ID, and "S14 owes", a lane name, to the ledger entries' reason strings. The neighbouring pre-existing "lane S14 ... rulings 6412739248 and 6425357821" belong to #746's tracking.
- **Exact fix:**
  - At `:217`: `(#895, ruling 6824623445)` -> `(#895)`.
  - At `:223-224`: `(#895, ruling 6824623445): S14 owes 60.0 - 56 = 4.0 RAMB36` -> `(#895): the move of cold code to flash owes 60.0 - 56 = 4.0 RAMB36`.

### RS2 - RESIDUE - `sw/firmware/ctrl/srp/srp_bounds.h:49-53` (a source comment's count)

- **The comment:** the new text says THE TRANSMIT's call publishes "IDLE_SLOPE and TALKER_DECL once, an adoption's or a validity change's, never both".
- **What the code does:** `transmit` (`srp_mbx.c:1214-1240`) runs `prepare_declarations` for every interface. After the first owing interface's build, it runs it again for that interface. When a join was refused in the first pass, `sources_owed` stays set (`srp_mbx.c:331`), so `change_domain` calls `declare_sources` a second time, and that interface publishes both registers twice. This includes after an adoption.
- **Why it is residue:** the numeric bound `SRP_MBX_PUB_POLL_MAX` is unchanged and still holds with wide margin. The worst case is SR_DOMAIN 1, plus IDLE_SLOPE and TALKER_DECL 2 x 2, plus at most one LICENCE per source, against `3 + 2 * MBX_N_PUB_SOURCES` plus the reset term. Only the comment's count is wrong.
- **Exact fix:** replace "IDLE_SLOPE and TALKER_DECL once, an adoption's or a validity change's, never both," with "IDLE_SLOPE and TALKER_DECL at most twice, the second time for the first owing interface after its build when a join was refused, SR_DOMAIN once for an adoption,".

### Suggestions (optional; no lens is left unclean by them)

- **S1** `sw/firmware/ctrl/srp/srp_mbx.c:291`: the withdrawal ignores `mrp_mad_leave`'s result.
  - lwSRP refuses a Leave while its port holds a prepared PDU or is sending (`third_party/lwSRP/src/core/mrp_mad.c:968`).
  - I traced the current structure. THE TRANSMIT runs only with no owed frame (`transmit_aged`, `srp_mbx.c:1243-1247`). A withdrawal is made by the call's first declarations pass, before any build. A later in-call pass repeats only a refused join. So the refusal is not reachable today.
  - If it ever were reachable, `TALKER_DECL` would drop the source while its Advertise stayed declared. Counting the refusal, or keeping the bit owed when the Leave is refused, would make that invariant explicit.
- **S2** `srp_mbx.c:649`: `moved` compares a valid source's destination with the last destination *recorded* valid, not the last *declared*.
  - Take a source declared at D. It lapses, becomes valid at E, lapses again and comes back at D, all inside the hold-off. It then waits out the hold-off, though D is its unchanged FirstValue and could be declared at once (IEEE 802.1Q-2018 35.2.2.8).
  - This errs conservative and is an unlikely sequence.
- **S3** `sw/firmware/ctrl/test/srp_talker.cpp:360-370`: the refused-swap step fails every allocation, so no MRPDU leaves during the refusal. The swap's join-before-leave order is therefore observed only through `TALKER_DECL`.
  - A reviewer probe that leaves the old type before joining the new one escapes at both points, even with an added wire assertion (`receipts/run/swap_order_probe_if*.log`, `probes*.log`).
  - A join-only refusal while frames still leave would make the order observable on the wire.

## What was checked, against the focus items

1. **Validity feed.**
   - Validity is ACMP's `acmp_declaring` (`third_party/tsn-c-stack/src/acmp.c:1340-1356`: `dest_mac_valid && (answered within da_fresh_ms || listener_registered)`).
   - The MAAP adapter publishes it per interface, own sources only (`sw/firmware/ctrl/maap/maap_mbx.c:51-61`). It is refreshed in MAAP's poll and synchronously at every range report, including the core's restart, which publishes `valid=false` before the base moves (`tsn-c-stack/src/maap.c:53-59,106-122`).
   - `ctrl_app_srp.c:62-67` hands `published_gate[k]` and `core.base` to `srp_mbx_gate` every pass. MAAP's poll is attached before it.
   - `srp_mbx_gate` (`srp_mbx.c:631-668`) does a mask compare and, per valid source, a 6-byte compare and copy. It calls only `hold`, which sets `tx_due` and reads `loop->retry_queued`. It calls no lwSRP function and makes no mailbox access. It refuses before attach, out of range and on reentry.
   - No file under `sw/mailbox/`, `hdl/` or `mbx_contract.h` is in the diff: **no mailbox contract or RTL change**.
2. **The declaration table (HANDOFF 1.3)**, each row read against `declare_sources` (`srp_mbx.c:260-333`), `count_held` (`:130-143`) and the 35.2.2.8 rules as the issue states them. Each row has a test and plants. The reviewer's campaign caught all 26 plants at 1x1/1if and at 8x8/2if (`receipts/run/tc1-*.log`, `tc2-*.log`). Rows:
   - not valid: `VALID`, `talker-declared-while-not-valid`;
   - valid: `VALID`, `ADMIT`, `talker-allocated-unfit-declares-code-2`, `talker-gate-not-fed`, `talker-gate-of-another-range`;
   - lapse: `LAPSE`, `PROBE`, `LISTENER`, `talker-lapse-kept`, `talker-lapse-ignored-by-the-entry`, `talker-decl-kept-at-the-withdrawal`, `talker-licence-closed-after-the-withdrawal`, `talker-listener-demand-not-forwarded`;
   - moved destination: `MOVED`, `talker-change-while-valid-unmarked`;
   - re-valid unchanged: `AGAIN`, `talker-unchanged-held`;
   - re-valid changed after `held_cs` = 2,022 cs: `CHANGED`, `LOST`, `talker-hold-off-skipped`, `-one-leaveall`, `-never-ends`, `talker-lapse-starts-no-hold-off`;
   - admission swap: `ADMIT` and six plants;
   - link reset: `RESET`, `talker-reset-forgets-the-move`;
   - refused join: `REFUSED`, `talker-refused-declaration-forgotten`.

   The reviewer's own boundary probes on the hold-off were each **caught** at both points (`receipts/run/probes1.log`, `probes2.log`):
   - the JoinTime term removed;
   - exactly 2 x 1000 cs;
   - 150 cs short, in the unit suite and through the composition.

   Hold-off arithmetic: the hold count and lwSRP's join timer count the same ticks. A Leave held behind a running join timer leaves at most THE TRANSMIT's bound after that timer's tick. The re-declaration comes no sooner than 2,002 ticks later. So the gap is at least 2,002 cs less the bound: 2,000.0 cs at 8x8/2if (20 ms bound) and 2,000.4 cs at 1x1/1if (16 ms). With the join timer idle, the gap is about 2,017 cs or more. `SRP_REDECLARE_CS` holds two LeaveAllTime periods after the Leave as sent.
3. **Wire evidence.**
   - The reviewer built the `valid-destinations` arm at the head at both points and ran both groups. The decoding is the reviewer's own (`scripts/decode_wire.py`, `scripts/check_decoded.py`), reading the WIRE bytes as 802.1Q 10.8 MRPDUs and 1722 Annex B MAAP PDUs, without the repository's `wire_talkers.py`.
   - Both `srp-talker-loss` logs are **byte-identical** to the author's measured logs (sha256 `26c4747e...` at 1x1, `d574a35e...` at 8x8; `receipts/sim/loss-logs.sha256`).
   - Both `srp-talker` (probe window) logs are **byte-identical** too (`a1b413cb...` at 1x1, `ef1e492f...` at 8x8; `receipts/sim/window-logs.sha256`). The harness legs: rc 0, 0 refusals, 0 of 5 and 0 of 20 budget misses, 0 passes over the share (`receipts/harness/vd*-run.log`).
   - Findings in both groups at both points (`receipts/sim/*.check.txt`):
     - no Talker attribute before the first probe;
     - no Talker Failed at any time;
     - every Advertise on source n's own interface (n mod 2 at 8x8/2if), with DA = MAAP's announced base + n and TSpec 224/1;
     - after each source's Leave, no declaring event of it.
     - each probe window closes 14,999.8 to 15,198.7 ms after its probe at 8x8/2if, and 15,000.1 and 15,196.9 ms at 1x1/1if: 15 s, then up to a JoinTime for the transmit opportunity.
     - the LeaveAll at 14.58 s (1x1) and 14.62 s (8x8, both interfaces) carries LeaveAll messages for every MSRP type with no value. The Talker Failed message among them is no declaration. The Advertises are declared again after it.
   - The loss withdraws each interface's sources at its next transmit opportunity: 199.4 ms at 1x1, 198.9 and 198.8 ms at 8x8. The Leave carries the old DA. The new range is announced, and nothing is declared during the hold-off.
4. **Acceptance 4:** see F1. The reviewer's `load_grade.py --check` rc 0 (0.488 / 0.486 HELD), `--selftest` 25 of 25, `flip_grade.py --check` rc 1 (as at the base), `--selftest` 131 of 131. These match the author's figures exactly.
5. **Acceptance 5**, from the reviewer's own image links (`receipts/rom/images-head.md`):
   - fixture: 38.5 / 41.5 / 51.5 / 58.0 RAMB36;
   - platform: 39.5 / 43.0 / 53.0 / 60.0 RAMB36, `ctrl_plat` 20,352 B at 8x8/2if;
   - every other point at or under 53.0;
   - byte-for-byte the author's table.

   The fixture's 8x8/2if image without its key is refused past 56. The `answering-every-port` arm's 8x8/2if image, built here, plans rom 124,444 B and sram 112,688 B: 58.5 tiles, 48 B past 58.0 (`receipts/rom/aep8-image-plan.txt`). The platform's 8x8/2if image at the base plans 59.5 against its 59.0, refused. That confirms the ruling's premise.

   `test_ctrl_memory.py`: PASS, 0 failures. The ledger entries 58.5 and 60.0 (cap 60.5) follow the ruling's fallback. The author's case that the named cuts recover about 30 of the 48 B is arithmetic on the author packet's `receipts/costs/layout-probe.txt`. It was not built as a variant; the reviewer's own estimate is about 34 B, also short.
6. **Gate pass and campaigns.**
   - The author's table (author packet `receipts/gates/verify-table.md`) has 365 steps: 139 rc 0, 226 NOT RUN each with a reason, 0 bad. The seven full-sweep rows are justified: no `hdl/` file changed.
   - Reviewer runs at the head:
     - `test_ctrl_firmware.py --require-rv32`: PASS, both Talker arms `[ok]`;
     - `fw_coverage.py --check`: PASS, 39 files (`srp_mbx.c` 724/724 lines and branches 100 % by the gate's count; `ctrl_app_srp.c` 89/89 lines, 72/72 branches);
     - `docs_check.py`: 0 findings;
     - `check_em_dash.py --base b2d39235`: 0 findings over 106 added lines;
     - `git diff --check` from the base: clean.
   - Hosted at the exact head (snapshot 2026-11-13T00:46Z, `receipts/gates/hosted-snapshot.txt`): 68 check runs completed **success** and 1 skipped (`Physical gPTP (nightly and manual)`, not run on a pull request). The successes include `firmware-unit`, `firmware-boundary`, `firmware-srp-mutants`, `firmware-aecp-mutants`, `firmware-control-mutants`, the Verilator shards and the Yosys shards. Hosted acceptance is the manager's. The control (696) and AECP (227) campaign counts are the author's receipts and the hosted jobs'; the reviewer did not rerun them.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Acceptance 1 to 5 against #895 as corrected and ruling 6824623445; Milan v1.2 4.3.3.1, 5.3.7.4 and 5.5.4.1 against `srp_mbx.c:260-333,631-668`, `ctrl_app_srp.c:62-67`, `maap_mbx.c:51-61`, `acmp.c:1340-1356`; 802.1Q 35.2.2.8 and Table 10-7 against `SRP_REDECLARE_CS` (`srp_mbx.c:34`) and the tick and join-timer accounting; 35.2.2.8.7 code 1 (`:296-297`); 1722 Table B.7 restart (`maap.c:117-122,297`); the decoded wire of both arms at both points; the gates' load and rows output | R836-1 | `d023b77a` |
| RTL | CLEAN | No `hdl/` change. The firmware architecture: the `gate`/`talkers`/`readdressed`/`held_cs` state and every transition in `declare_sources` and `count_held`; widths (masks under `1u << CTRL_SRP_SOURCES`, at most 16; `uint16_t held_cs` for 2,022); `srp_bounds.h:49-55` publication bound against both declarations passes of one THE TRANSMIT call (the bound holds; its comment's count is RS2); `transmit` / `transmit_aged` / `send_pdu` / lwSRP `mrp_transmit` prepared-PDU lifecycle (S1); `KL_mbx_cdc` taking interface 0's `TALKER_DECL` / `LICENCE` / `DA_GATE` (`milan_soc.py:3236-3237`) against per-interface declarations, consistent with the processor placement | R836-1 | `d023b77a` |
| Robustness | CLEAN | Reset during activity (`RESET`, `held_cs` kept across `reset_interface`); refused join (`REFUSED`, NEW mode's early return and `withdraw_declared`); reentry and before-attach (`ENTRY`); mask bits past the sources; idempotent repeated gate calls; sub-pass gate blips; MAAP restart ordering (`reserve` publishes invalid before the base moves); a Leave refusal (unreachable, S1); D to E to D inside a hold-off (S2) | R836-1 | `d023b77a` |
| Tests | CLEAN | `srp_talker.cpp` (9) and `srp_gate.hpp` (3) read against each table row; 26 of 26 plants caught at 1x1/1if and 8x8/2if; six reviewer probes (hold-off boundary probes caught; the swap-order probe inconclusive, S3); `test_ctrl_firmware.py --require-rv32` PASS; `fw_coverage.py --check` PASS; harness `valid-destinations` arm rebuilt and rerun at both points, all four group logs byte-identical to the author's measured ones | R836-1 | `d023b77a` |
| Docs | UNCLEAN (F1, F2, F3; RS1 and RS2 residue) | `sw/firmware/ctrl/srp/README.md`, `plat/README.md`, `maap/README.md`, `docs/design/MAILBOX_SPLIT.md:1136-1150`, `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 13 against the gate output and the reviewer's images; harness README; PR #901 body and #895 REVIEW READY against the receipts; `docs_check.py` and `check_em_dash.py` | R836-1 | `d023b77a` |

## Receipts

- Everything cited as `receipts/...` or `scripts/...` is listed in `MANIFEST.sha256`.
- Host paths in the receipts are redacted to `<packet>`, `<clone>`, `<home>`, `<tools>` and `<scratch-root>`.
- `scripts/` holds the reviewer's portable drivers:
  - `talker_campaign.py`: the plant campaign and probes;
  - `swap_order_probe.py`;
  - `images.sh`;
  - `decode_wire.py` and `check_decoded.py`: the independent wire decoding and its checks;
  - `bg.sh` and `env.sh`: the launcher and its environment.
- Disposable trees (builds, the base clone, plant copies, the author packet checkout) stayed under `scratch/` and are not published.

## Real limits

- **Hardware:** acceptance 6 (one stream each way with the reference peer, every counter at both ends) is a bench item. It was not examined. Physical calibration NOT RUN. No simulation here is hardware proof.
- **No manager source bank** runs at this head. Source-head execution evidence is the author's receipts plus the reviewer's focused runs listed above. The current-dev merge candidate (live dev `b7d69295`) is not validated here.
- **Not rerun by the reviewer:**
  - the full SRP (392), control (696) and AECP (227) campaigns;
  - arm A and the `answering-every-port` arm's groups, and their cost legs feeding `load_grade.STATED_US` (only the image plan of `answering-every-port` at 8x8/2if was rebuilt);
  - `behave`, `test_builder.py`, the split boot simulation and the full workflow pass.

  Those rest on the author's receipts and the hosted jobs named above.
- **Not built:** the ruling's named RAM cuts were not built as a variant.
- **Not simulated:** the wire has no re-declaration after a hold-off inside either group. The changed-destination re-declaration is covered by the unit and composition tests only.
- **Shared host:** the reviewer's simulations ran on a host shared with other lanes' builds. Timing figures come from simulated cycles, not wall time.

## Pending manager duties

- Obtain or record the maintainer decision F1 asks for, before the merge turn.
- Accept the hosted contexts. At the reviewer's 00:46Z snapshot all were complete: 68 success, 1 skipped by schedule.
- Build and validate the current-dev merge candidate.
- Carry RS1 and RS2 to the residue checklist.
- Re-review is owed at the head that answers F1 to F3. A Docs-only change re-covers Docs; F1 also re-covers Conformance.

R836-1 FINISHED
