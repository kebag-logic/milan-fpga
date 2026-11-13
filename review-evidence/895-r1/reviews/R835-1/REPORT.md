[R835] NEGATIVE - exact head d023b77a7bf677205e45195e0e1f0daf80d1a4d4

# R835-1: cleared-context internal review of PR #901 (issue #895)

- **Head:** `d023b77a7bf677205e45195e0e1f0daf80d1a4d4`, tree `ea4ed7a01cefd8a672238a19695437eca022cba7`. The review clone was verified byte-exact at the end of the round: 1,586 tracked blobs re-hashed (0 mismatches), `git diff --quiet HEAD` clean (content and mode), index clean, no untracked files, and the gitlinks `third_party/lwSRP` `08ee86e8`, `third_party/tsn-c-stack` `715589c1`, `protocol-processor` `a9e84b66`, `gptp-processor` `135afd04` and `third_party/verilog-axis` `48ff7a7e` checked out clean.
- **Diff reviewed:** `b2d39235..d023b77a`. That is thirteen non-merge commits plus the merge `7392638e` of #810's round-29 head, 29 files, +1,252/-141. No RTL, mailbox-contract (`sw/mailbox/`, `mbx_contract.h`), tsn-c-stack, lwSRP or donor file is in it.
- **Authority, read in this order:**
  - `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
  - The #895 issue body, with acceptance 1 to 6 as corrected.
  - The ruling issuecomment-6824623445 and the #894 owner decision issuecomment-6814835849, which acceptance 4 cites.
  - #890 and its owner decision issuecomment-6798229503 (the 0.75 ceiling).
  - Milan v1.2 4.3.3.1, 5.3.7.4 and 5.5.4.1, as the repository and the issue quote them.
  - IEEE 802.1Q-2018: 35.2.2.8 (the same and a changed FirstValue, two LeaveAllTime periods), Table 10-7, 35.2.2.8.7 and Table 35-6.
  - IEEE 1722-2016 B.3.6.4 and Table B.7, via the test stimuli.
  - The interface documents the diff touches.
- **Then:** the diff, its history, and my own executions, below. The executor's public packet (archive `e60d35c0`, `review-evidence/895-r1/author`) was read as evidence and checked against my own runs. It is not evidence of correctness.
- **Prior public review findings on PR #901:** none exist. At this round, the PR's only comments are the two "review started" notices, and it has no reviews or review comments. There is nothing to resolve or retain.

## Findings

### R835-1-F1 MAJOR: Conformance, Docs. Acceptance 4 is claimed met, but at this head it is not met as written, and no decision reinterprets it

- **Where:** issue #895 acceptance 4. The REVIEW READY comment (issuecomment-6838154041) says "4 met (1x1/1if 0.488 / 0.486 within 0.70; 8x8/2if reported)". The PR #901 body says the same under "Acceptance 4".
- **Authority:** acceptance 4 reads: "The CPU-budget harness load and rows stay within the flip gate: 1x1/1if at most 0.70 with rows by every source, and 8x8/2if at most 0.75 with rows by measurement (owner decision 2026-11-12, #894)". The #894 owner decision says the 8x8/2if flip "holds the long-window load at 0.75" and needs a measurement "in which every row fits its bound". `AGENTS.md` section 4 freezes acceptance and asks for a public change rather than a reinterpretation.
- **Evidence (graders run at this head):**
  - 1x1/1if rows by every source: R4 is **66.77 ms against its 20 ms bound** (`flip_grade.py --check`, rc 1: "OVER 1x1/1if R4"; `receipts/graders/flip_check.log`). It was 66.12 ms at the base.
  - 8x8/2if load: **0.817 at the pin and 0.768 with tsn-c-stack#32, both over 0.75** (`load_grade.py --check`, `receipts/graders/load_check.log`). They were 0.816 and 0.767 at the base (`receipts/graders/load_check_base.log`).
  - 8x8/2if rows by measurement: the executor's own receipt `costs/least-margin-final.txt` records arm A with "7 over" (7 of 996 probe instances over budget, which tsn-c-stack #26 holds).
  - So the 1x1/1if load meets its clause, while the 1x1/1if every-source rows, the 8x8/2if load and the 8x8/2if measured rows do not. The lane also moves each of these the wrong way, slightly (R4 +0.65 ms, load +0.001).
  - The shortfall is not caused by this lane: #894 (tiers), #890 (the 0.75 grader) and tsn-c-stack #26 own it. But the frozen criterion is still stated as met.
- **Impact:** the completion bar's first bullet ("all acceptance criteria are met") would be cleared on a claim that the criterion's own figures contradict. A cold reader of the REVIEW READY sees "4 met".
- **Required outcome:** one of two things.
  - A maintainer decision recorded on #895 that states how acceptance 4 binds this lane, for example no regression of the flip gate's figures owned by #894, #890 and tsn-c-stack #26, with the measured deltas above accepted.
  - Or the figures meet acceptance 4 as written.

  Either way, the PR body and the REVIEW READY must state acceptance 4 per that decision, not as "met".
- **Verification:** the decision's link on #895. Then `load_grade.py --check` and `flip_grade.py --check` at the candidate head, read against the decision's terms.

### R835-1-F2 MINOR: Docs. Section 13's load table keeps 8x8/2if's pass cost at 315 µs; the head's grader prints 320

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:2209`.
- **Evidence:**
  - The row reads `| 8x8/2if | **0.817** | 0.768 | ... | 315 |`.
  - `load_grade.py --check` at the head prints "A pass's own cost, us" **320** for 8x8/2if (`receipts/graders/load_check.log`).
  - The base printed 315 (`receipts/graders/load_check_base.log`). The lane moved `STATED_US_DONOR['8x8/2if']['base']` from 285 to 290.
  - The same table's 1x1/1if row was updated from 180 to 185, so the 8x8/2if cell is a missed update.
- **Impact:** the authoritative table states a cost the gate no longer uses.
- **Required outcome:** the cell reads 320, the grader's figure.
- **Verification:** the doc row equals `load_grade.py --check`'s table at the candidate head.

### R835-1-F3 MINOR: Docs. The evidence claims 28 Talker plants; the table at the head holds 26

- **Where:**
  - PR #901 body: "Status", "Acceptance 3" and "Tests and planted defects".
  - REVIEW READY: "SRP 392 (the 28 Talker plants ...)" and "28 plants each killed".
  - The executor's HANDOFF section 3.
- **Evidence:**
  - `srp_talker_mutants.defects()` returns **26** plants (`receipts/plant-count.txt`, which lists them).
  - This review's SRP campaign records **52** `talker-` kills: 26 in the two-interface campaign at 8x8/2if and 26 in the one-interface campaign at 1x1/1if (`receipts/fw/shard3.log`).
  - The totals (392) are right, but the stated plant count is not.
- **Impact:** the acceptance 3 evidence misstates what was planted. A cold reviewer counting the plants cannot reconcile it.
- **Required outcome:** the PR body, the REVIEW READY and the handoff state 26 (or the two missing plants are added).
- **Verification:** the count of `srp_talker_mutants.defects()` and of `[ok] talker-` lines in the campaign log.

### R835-1-F4 MINOR: RTL, Robustness, Docs. `srp_bounds.h`'s new bound argument says THE TRANSMIT publishes `TALKER_DECL` once; after a refused join it publishes it twice in one call

- **Where:** `sw/firmware/ctrl/srp/srp_bounds.h:49-53`: "THE TRANSMIT's call ... publishes an interface's declarations within the same terms (#895): IDLE_SLOPE and TALKER_DECL once, an adoption's or a validity change's, never both".
- **Evidence:**
  - `transmit()` (`srp_mbx.c:1214-1238`) calls `prepare_declarations` twice on the interface it builds: once in the loop over interfaces, and again after the build.
  - `change_domain` (`srp_mbx.c:894`) runs `declare_sources` whenever `sources_owed` is set.
  - After a refused join, `sources_owed = !done` (`srp_mbx.c:331`) leaves it set. So the second call runs `declare_sources` again and publishes `IDLE_SLOPE` and `TALKER_DECL` again: a validity change's twice, or an adoption's and then a retry's.
  - An instrumented copy, which never touched the checkout, confirms it executes (`scripts/probe_pubs.py`, `receipts/probes/probe-pubs.txt`). In `Talker.RefusedDeclarationIsDeclaredAgain`, one THE TRANSMIT call published `TALKER_DECL` twice on an interface: 2 times at 1x1/1if, and 4 times over both interfaces at 8x8/2if.
  - The numeric macro `SRP_MBX_PUB_POLL_MAX` still covers it by my count: 5 + S per interface, against `SRP_MBX_PUB_RESET` + 3 + 2 × 16. So the stated reason is wrong, not the bound.
- **Impact:** the publication bound's argument is false on a reachable failure path. A later change that trusts "once" can break the census.
- **Required outcome:** the comment states what the code does (the interface THE TRANSMIT builds may publish both again after a refused join), or the code publishes once per call.
- **Verification:** a test that counts an interface's publications within one THE TRANSMIT call with a refused join, held to the stated count.

### R835-1-F5 MINOR: Robustness, Conformance. A withdrawal's Leave can be refused and is never retried, which can leave a stale Talker attribute while `TALKER_DECL` shows it withdrawn

- **Where:** `srp_mbx.c:291-293`. The withdrawal's `(void)mrp_mad_leave(...)` result is discarded, then `i->talkers &= ~bit` and the hold-off is armed.
- **Evidence (established by reading the head; not executed):**
  - lwSRP refuses `mrp_mad_leave` while the port holds a prepared PDU (`third_party/lwSRP/src/core/mrp_mad.c:968`).
  - A PDU stays prepared when the adapter's send is refused by a full ring: `srp_mbx.c:802-803`, and `mrp_mad.c:1491-1498`.
  - Inside one THE TRANSMIT call, the second `prepare_declarations` runs on the interface after its build (`srp_mbx.c:1224-1235`). So consider this sequence:
    1. A Domain adoption is owed and its `mvrp_declare` is refused for storage in the first call (`srp_mbx.c:898`). That returns before `sources_owed` is processed.
    2. The MSRP frame built next is refused by the ring.
    3. The `reclaim` before it freed storage, so the second call's `mvrp_declare` succeeds.
    4. `declare_sources(SRP_DECLARE_EVERY)` (`:913`) then withdraws a source whose validity lapsed. Its Leave is refused silently.
  - With its `talkers` bit already clear, nothing withdraws that source again. The attribute stays declared in lwSRP and goes out in later MRPDUs.
  - The Domain's own leave and join in the same path (`:901`, `:912`) carry the same pre-existing pattern.
- **Impact:** in that resource-exhaustion corner, acceptance 2's "no stale Talker Advertise remains" does not hold until a link reset.
- **Required outcome:** one of two things. Either `declare_sources` provably never runs while a participant holds a prepared PDU (stated and enforced, for example by not re-entering the declarations after a refused build), or a refused withdrawal Leave keeps the source owed for withdrawal.
- **Verification:** a unit test that refuses the ring during THE TRANSMIT after a refused adoption, then checks the source's Leave on the wire; or an assertion of the invariant, with a planted defect that removes it.

### R835-1-RS1 RESIDUE: the comment rule. New lane-name and issue-comment-ID instances in a source string

- **Where:** `sw/litex/ctrl_memory.py:217` ("(#895, ruling 6824623445)") and `:224` ("(#895, ruling 6824623445): S14 owes 60.0 - 56 = 4.0 RAMB36").
- These are new instances in the reviewed delta. The older "lane S14" and "rulings 6412739248 ..." text is tracked by #746.
- **Exact fix:** replace ":217" "(#895, ruling 6824623445)" with "(#895)". Replace ":224" "(#895, ruling 6824623445): S14 owes" with "(#895): the cold-code move to flash owes".

### R835-1-RS2 RESIDUE: Docs wording. The SRP README still opens the Talker paragraph as if every output declares from the start

- **Where:** `sw/firmware/ctrl/srp/README.md:193` and `:195`: "Every output starts with Talker Advertise or Talker Failed" and "Unallocated outputs report insufficient resources (code 2)".
- With the gate, an output declares nothing until it is valid, and code 2 arises only with `sources_valid` (the gateless unit fixture). The new paragraph below says so.
- **Exact fix:**
  - Change ":193" to "A declared output's first declaration is Talker Advertise or Talker Failed (Milan 5.5.2.7)."
  - Change ":195" to begin "Without a DA gate (`sources_valid`), unallocated outputs report insufficient resources (code 2);".

### R835-1-S1 SUGGESTION: Tests. The hold-off end's wake-up is not observable at 8x8/2if

- **Probe:** remove `hold(i)` from `count_held` (`srp_mbx.c:138`).
- **Result:** the probe is killed at 1x1/1if (`Talker.ResetKeepsAnUnchangedSourceAndHoldsAMovedOne`), but it **survives every 8x8/2if arm**: `srp_talker.cpp` and `SrpGate.*` (`receipts/probes/probes-summary.txt`, and the two `hold-off-end-owes-no-pass.*.log` files).
- At 8x8/2if another pass happens to come within the test's 400 ms tolerance. The row stays covered by the lane's `talker-hold-off-never-ends` plant at both points.
- **Suggestion:** a plant for this wake-up, and an 8x8/2if scenario in which nothing else owes a pass at the hold-off's end.

### R835-1-S2 SUGGESTION: Conformance note

- `SRP_REDECLARE_CS` reads "two LeaveAllTime periods" as 2 × Table 10-7's 1000 cs, plus a JoinTime and THE TRANSMIT's bound: 20.22 s from the Leave's request.
- That is acceptance 2's wording. The unit tests hold the wire gap at 20 s or more from the Leave, and my probes `hold-off-margin-dropped` (2000 cs) and `hold-off-1999` are both killed at both points.
- The Mark I design counts the same rule as 2 × a 10 to 15 s LeaveAll draw (`T-SRP-LEAVEALL2`, 20 to 30 s; `protocol-processor/docs/architecture/08_timing.md:36`). This value sits at that range's floor.
- **Suggestion:** state the chosen reading beside the macro, or in the SRP README's paragraph.

## Each lens, with what it examined (exact head `d023b77a`)

```text
[R835] PASS Conformance (partial; the lens is UNCLEAN by F1 and F5) - sw/firmware/ctrl/srp/srp_mbx.c:260-333 declare_sources, :631-668 srp_mbx_gate, :130-143 count_held; app/ctrl_app_srp.c:63-67 - checked against issue #895 acceptance 1, 2, 3 and 5, ruling items 1-6, Milan v1.2 4.3.3.1/5.3.7.4/5.5.4.1 and 802.1Q 35.2.2.8/Table 35-6: validity is the MAAP adapter's published DA gate (maap_mbx.c:51-61, acmp_declaring, own interface, s < count, range valid); srp_mbx_gate calls no lwSRP function, makes no mailbox access, masks bits past the sources and refuses before attach, after destroy, out of range and on reentry; no mailbox-contract file changed; every row of HANDOFF 1.3 matches the code
[R835] PASS RTL (partial; the lens is UNCLEAN by F4) - srp_mbx.h:75-82,91-94,123-125; srp_mbx.c:34 (SRP_REDECLARE_CS = 2,022 cs; held_cs uint16_t), :639 mask before shift (CTRL_SRP_SOURCES <= MBX_N_PUB_SOURCES = 16), :646-652 base + n written big-endian over 6 octets; work bounded per source and interface - against the harness's measured costs (0 of 2,637 and 0 of 2,980 work passes over the 200,000-cycle share in my runs; executor's polls' base most 15,078/27,578 cycles, not re-measured here)
[R835] PASS Robustness (partial; the lens is UNCLEAN by F4 and F5) - reset (reset_interface keeps talkers; ResetKeeps... and my reset-forgets-talkers probe killed at both points), repeated gate reports (ValidSource...: at most two New), flapping validity (unchanged destination at once), out-of-range input, refused joins (RefusedDeclaration..., refused swap) - the corner cases in F4 and F5 are open
[R835] PASS Tests - sw/firmware/ctrl/test/srp_talker.cpp (9 tests), srp_gate.hpp (3), srp_talker_mutants.py (26 plants), srp_arms.py:89-95, test_ctrl_firmware.py:194-195,213 - every row of the declaration table has a test and a plant killed at 1x1/1if and 8x8/2if (receipts/fw/shard3.log: 52 talker- kills, 0 escaped); my 7 extra plants (receipts/probes/probes-summary.txt) are killed, one surviving only at 8x8/2if (S1, optional); SrpGate also runs at 1x1 through the existing test_acmp_mbx arms (receipts/fw/shard0.log:330,396)
[R835] PASS Docs (partial; the lens is UNCLEAN by F1, F2, F3 and F4) - docs/design/MAILBOX_SPLIT.md:1139-1148, sw/firmware/ctrl/srp/README.md:192-226,401-427, maap/README.md:119-120, plat/README.md:80,110-111,134-136, docs/design/SPLIT_CONTROL_MEMORY.md sections 3, 5 and 13, tb/verilator/ctrl_service_budget/README.md:49,219-223 - checked against the code and the receipts; scripts/docs_check.py rc 0 (0 findings); git diff --check clean
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F5 MINOR) | #895 acceptance and ruling against `srp_mbx.c`, `ctrl_app_srp.c`, `maap_mbx.c`, the graders' output and my decoded wire | R835-1 | `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` |
| RTL | UNCLEAN (F4 MINOR) | `srp_mbx.c`/`.h`, `srp_bounds.h`, the transmit path and the instrumented probe; no HDL in the diff | R835-1 | `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` |
| Robustness | UNCLEAN (F4, F5 MINOR) | reset, refusal, repeat, flapping and range paths; probes | R835-1 | `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` |
| Tests | CLEAN (S1 SUGGESTION only) | `srp_talker.cpp`, `srp_gate.hpp`, `srp_talker_mutants.py`, all four campaigns rerun, 8 probes, coverage | R835-1 | `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` |
| Docs | UNCLEAN (F1, F2, F3, F4 MINOR; RS1, RS2 RESIDUE) | the eight docs above, PR body, REVIEW READY, handoff, `docs_check.py` | R835-1 | `d023b77a7bf677205e45195e0e1f0daf80d1a4d4` |

## The brief's checks, item by item

1. **Validity and its feed.** Validity is ACMP's `acmp_declaring` as the MAAP adapter publishes it per interface (`maap_mbx.c:96,172-174`, `published_gate`). The composition passes it each delivery poll (`ctrl_app_srp.c:65-67`). `srp_mbx_gate` is bounded at sources × 6 octets per interface, calls no lwSRP function and makes no mailbox access. No mailbox contract changed. **Holds.**
2. **The declaration table, row by row, against the code and 35.2.2.8.** Each row has a test and a lane plant killed at both points:
   - not valid: `talker-declared-while-not-valid`;
   - valid: `talker-gate-not-fed`, plus my `gate-owes-no-pass`;
   - lapse: `talker-lapse-kept`, `-lapse-ignored-by-the-entry`, `-decl-kept-at-the-withdrawal`, `-licence-closed-after-the-withdrawal`;
   - moved destination: `talker-change-while-valid-unmarked`;
   - re-valid unchanged: `talker-unchanged-held`;
   - re-valid changed after `held_cs` = 2,022 cs: `talker-hold-off-skipped`, `-one-leaveall`, `-never-ends`, `-lapse-starts-no-hold-off`, plus my `hold-off-margin-dropped` and `hold-off-1999`;
   - admission swap: four `talker-swap/withdrawal/refused-swap/allocated-unfit` plants;
   - link reset: `talker-reset-forgets-the-move`, plus my `reset-forgets-talkers`;
   - refused join: `talker-refused-declaration-forgotten`.

   Open: F5 (a refused withdrawal Leave) and S1.
3. **No boot-time Talker Failed and no stale Talker Advertise.** These are decoded by my own decoder (`scripts/decode_wire.py`) from my own harness runs at this head (`receipts/sim/*.decoded.txt`). WIRE extracts are re-decodable, and the raw-log hashes are in `receipts/sim/raw-logs.sha256`.
   - **Talker Failed:** 0 values in all four logs.
   - **Before the probes:** no Talker attribute before the first PROBE_TX response (1x1 3,274.523 ms; 8x8 3,314.357 ms).
   - **Destinations:** each source on its own interface at MAAP's base + n (1x1: `91e0f000a134` + 0, + 1; 8x8: `91e0f000d1a4` + 0 to + 8, even sources on if0 and odd on if1).
   - **Window expiry:** each Leave comes 14,999.8 to 15,198.7 ms after its probe's commit.
   - **Range loss:** a peer's ANNOUNCE withdraws the interface's sources 198.8 to 199.4 ms later, while MAAP probes the new range (`91e0f0001ba5`, `91e0f0004dae`).
   - **After a Leave:** no declaring event for that StreamID to the end of any group.
   - **Harness verdicts:** 1x1 rc 0 (0 of 5 instances over budget, 0 of 2,637 passes over the share), 8x8 rc 0 (0 of 20, 0 of 2,980).
   - **Talker rows:** worst 199.406 of 220 ms (1x1) and 199.232 of 220 ms (8x8), identical to the executor's figures.
4. **Acceptance 4.** Not met as written: **F1**.
5. **Acceptance 5.** Holds. I rebuilt the eight ledger images myself (`scripts/images.sh`, `receipts/rom/images.txt`), using the runtime and SoC exports of my own harness builds at this head. Fixture and platform RAMB36 are:
   - 1x1/1if: 38.5 and 39.5;
   - 1x1/2if: 41.5 and 43.0;
   - 8x8/1if: 51.5 and 53.0;
   - 8x8/2if: 58.0 and **60.0** (`ctrl_plat` 20,352 B).

   Every rom, sram and `ctrl_plat` figure equals the executor's. The `answering-every-port` arm's image at 8x8/2if plans **58.5** (rom 124,444 B, sram 112,688 B, 48 B past 112,640; `receipts/rom/arm-answering-every-port.txt`), so the fixture entry at 58.5 is the ruling's fallback. `valid-destinations` plans 58.0. Every other point is at or under 56. `test_ctrl_memory.py` PASS.
6. **Gates and campaigns.** My runs:
   - Campaigns at this head: suites PASS (71 arms); control 696 of 696 caught; AECP 227 caught, 0 escaped; SRP 392 `[ok]`, 0 escaped (`receipts/fw/shard0-3.log`, every rc 0).
   - `fw_coverage.py --check` PASS (39 files; `srp_mbx.c` 724/724 lines, `ctrl_app_srp.c` 89/89, 72/72).
   - Graders: `load_grade.py --check` rc 0 and `--selftest` 25/25. `flip_grade.py --check` rc 1 by design and `--selftest` 131/131.

   The clean-clone workflow pass (139 rc 0, 226 not run) is the executor's. I tallied its table (`gates/verify-table.md`): 139 `0` and 226 `NOT RUN`, each with a reason, `verify.rc` 0. I did not rerun it.

## Real limits

- I did not rerun the arm A, `answering-every-port` and arm B cost legs. The least measured row margins (9.733 and 11.255 ms) and arm A's 7 misses are the executor's receipts. My harness runs are the `valid-destinations` arm only, at both points.
- I did not rerun the four-workflow clean-clone pass. I read and tallied its receipts.
- F5 is established by reading the head; it was not executed.
- No physical calibration or hardware ran. Acceptance 6 (one stream each way on the bench) is outside this review.
- Hosted exact-head contexts were read, not owned. At `2026-11-13T00:40Z`, 24 were successful (firmware unit, boundary, control/AECP/SRP mutants among them) and 1 skipped (physical gPTP). The Verilator and Yosys shards and the publication census were still queued or in progress (`receipts/hosted-checks.txt`).
- No manager source bank ran at this head, and none is claimed or inferred.

## Pending manager duties

- Obtain and record the maintainer decision on acceptance 4 (F1). Then re-review F1 to F5 at the corrected head.
- Carry RS1 and RS2 to the residue checklist.
- Hosted and act acceptance of the exact head's long gates (Verilator, Yosys, publication census).
- The current-dev merge-candidate validation: source base `b2d39235ab9bba85d7e560b5f5f78fb4be528960`, live `dev` `b7d692952305e4e0e132abb8f99c339eeb17a873`.
- File the issue the executor recorded but has not filed: the Domain adoption's in-place vlan_identifier change, a FirstValue change. A search of the repository's issues at this round found none.
- The bench item, acceptance 6.

## Receipts and scripts

All of them are listed in `MANIFEST.sha256`. Host-specific paths in them are replaced by `<packet>`, `<clone>`, `<home>` and `<tools>`.

- **Scripts:**
  - `scripts/decode_wire.py`: an independent MRPDU, MAAP and ACMP decoder.
  - `scripts/probe_talker.py`: eight reviewer plants, run through the repository's arm builder on a copy.
  - `scripts/probe_pubs.py`: the instrumented publication count.
  - `scripts/images.sh`: the eight ledger images.
  - `scripts/arm_image.py`: a harness arm's image.
- **Receipts:**
  - `receipts/fw/`: the four firmware shards, logs and rc files.
  - `receipts/coverage/`: coverage.
  - `receipts/graders/`: load, flip and memory graders, the base load, docs, diff-check.
  - `receipts/rom/`: images and arms.
  - `receipts/harness/`: both points' run logs and rc files.
  - `receipts/sim/`: decoded wire, WIRE extracts, graded tables, raw hashes.
  - `receipts/probes/`: probe summaries and logs.
  - `receipts/plant-count.txt` and `receipts/hosted-checks.txt`.

R835-1 FINISHED
