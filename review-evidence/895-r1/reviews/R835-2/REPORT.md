[R835] POSITIVE - exact head 18300f6e5f0c63b2ebc81d6bbc243496034f638a

# R835-2: cleared-context internal delta review of PR #901 (issue #895)

- **Head:** `18300f6e5f0c63b2ebc81d6bbc243496034f638a`, tree `d7318d3676d199141e119e0afa1a49145edaba2b`.
  - The clone was verified byte-exact at the end of the round (`receipts/clone-verify.txt`): 1,586 tracked blobs re-hashed with 0 mismatches and no mode differences, work tree and index clean against HEAD, and 0 untracked files.
  - The 108 ignored files are build byproducts of this round's own runs (`__pycache__`, `configs/generated/*.hex`).
  - Gitlinks checked out clean: `third_party/lwSRP` `08ee86e8`, `third_party/tsn-c-stack` `715589c1`, `protocol-processor` `a9e84b66`, `gptp-processor` `135afd04`, `third_party/verilog-axis` `48ff7a7e`. `external` is not initialized, as at round 1.
- **Delta reviewed:** `d023b77a..18300f6e`, seven non-merge commits and no merge. 10 files, +217/-41.
  - Code: `srp_mbx.c`, `srp_bounds.h` (comment only) and `ctrl_memory.py` (reason strings only).
  - Tests: `srp_talker.cpp`, `srp_talker_mutants.py`, `srp_pub_mutants.py` (one anchor) and `coverage.ratchet`.
  - Docs: `MAILBOX_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` and the SRP README.
  - No HDL, mailbox contract, tsn-c-stack, lwSRP or donor file is in it. The full lane diff `b2d39235..18300f6e` was used only where a delta claim depends on it (graders, images, `git diff --check`).
- **Authority, in this order:**
  - `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
  - The #895 issue body, acceptance 1 to 6. Acceptance 6 (hardware) is out of this review.
  - The round-2 ruling issuecomment-6840463408, items 1 to 6, with acceptance 4 as amended there.
  - The owner ROM decisions: the 8x8/2if platform plans 60.0 (cap 60.5) and the fixture 58.0 (cap 58.5).
  - IEEE 802.1Q-2018 35.2.2.8, Table 10-7 and 10.7.4.3, as the code and the README cite them.
  - lwSRP `mrp_mad.c:946-980` (when `mrp_mad_join` and `mrp_mad_leave` refuse).
  - The REVIEW READY issuecomment-6850450637.
  - The author packet `review-evidence/895-r1/author-r2` (archive `5fda6970`).
- **Prior public review findings:** they were read only after my own pass over the delta. They are my own R835-1 (issuecomment-6840458159) and R836-1 (issuecomment-6840411046). Each is resolved or retained below.

## Findings at this head

No BLOCKER, MAJOR or MINOR is open. One RESIDUE and four SUGGESTIONs follow.

### R835-2-RS1 RESIDUE: RTL, Docs. `srp_bounds.h:52-54`: the second pass's parenthetical names a refused withdrawal as something it makes

- **Where:** `sw/firmware/ctrl/srp/srp_bounds.h:52-54`. The text reads: "the second making what the first could not (a join or a withdrawal lwSRP refused, an adoption refused for storage)".
- **What the code does:**
  - THE TRANSMIT runs only with no frame owed (`transmit_aged`, `srp_mbx.c:1250-1254`), so its first declarations pass never meets a refused Leave.
  - The second pass runs on the built interface after its build. If that build left a frame owed, lwSRP refuses the second pass's Leave as well (`mrp_mad.c:968`), and the withdrawal stays owed for the next call.
  - So a refused withdrawal is never made by the same call's second pass. That pass makes a join or an adoption the first pass could not store, and it may meet a withdrawal that stays owed.
- **Why it is residue:** the count "at most twice each", the bound `SRP_MBX_PUB_POLL_MAX` and the code are all right, and the test `Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin` holds the count. Only the reason's parenthetical is loose.
- **Exact fix:** replace "(a join or a withdrawal lwSRP refused, an adoption refused for storage)" with "(a join or an adoption refused for storage; a withdrawal it meets after a refused build stays owed)".

### R835-2-S1 SUGGESTION: Robustness. A refused withdrawal's licence window is closed today only by the Domain adoption's VLAN state

- **Where:**
  - `srp_mbx.c:282-300`: a refused Leave leaves `talkers` set, so `admitted[n]` stays the declared type (`:326`).
  - `srp_mbx.c:1176`: the poll's licence rule is `link && vlan_sent && admitted[s] && registered[s]`, which does not read the DA gate.
- **Reading:**
  - The only reachable refused Leave needs an adoption refused for storage in the first pass, which only a new VID's `mvrp_declare` can be. That adoption is then made in the second pass, which clears `vlan_sent` (`srp_mbx.c:913-915`).
  - `vlan_sent` returns only when an MVRP record is sent, and the next call's first pass takes the Leave before any MVRP build.
  - So a licence closed for a lapse cannot reopen during the window. But that holds by the VID change, not by a stated rule. A future path to a refused Leave that keeps `vlan_sent` would reopen the stream licence of a source whose destination is no longer valid, for up to a JoinTime.
- **Suggestion:** do one of two things.
  - State the invariant beside the refused-Leave branch.
  - Or gate the licence on validity as well, then add a Listener-registered variant of `Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` that asserts no `licence(..., true)` between the refusal and the Leave.

### R835-2-S2 SUGGESTION: Docs (evidence process). Four logs in the author packet no longer match their INDEX hashes

- **Where:** archive `5fda6970`, `review-evidence/895-r1/author-r2/receipts/`. The four files are `gates/workflows/logs/docs__docs-gates-{1,2}__gate_25_{0,1}.log` and `elaborate__elaborate-gates-{0,1}__gate_15_{0,1}.log`.
- **Evidence:**
  - Of the 730 files listed in `receipts/INDEX.md`, 726 match (`scripts/check_index.py`, `receipts/author-index-check.txt`).
  - Each of the four is 8 B shorter than its listed size and carries a `<home-path>` placeholder. A privacy scrub ran after the index was generated.
  - The gate results do not depend on them: each step is rc 0 in `verify-table.md`, and the log body ends "ALL GATES PASS EXCEPT 1 NOT RUN".
  - The archive commit itself is unsigned (`verification.verified` false), so the INDEX is the packet's only integrity record.
- **Suggestion:** regenerate the INDEX after the scrub in the archiving step.

### R835-2-S3 SUGGESTION: Tests. The hold-off end's wake-up is still not observable at 8x8/2if

This is R835-1-S1, retained. It was optional, and the handoff records it as not taken (HANDOFF-r2 item 5). The row stays covered at both points by `talker-hold-off-never-ends`.

### R835-2-S4 SUGGESTION: Conformance note on the reading of "two LeaveAllTime periods"

R835-1-S2 is taken: the SRP README now states the reading (`sw/firmware/ctrl/srp/README.md:222-226`): 2 × the configured 1000 cs, the 20 s floor of the 20 to 30 s that two drawn periods span (802.1Q 10.7.4.3). Nothing further is owed.

## Prior findings, each at its cause

| Finding | State at `18300f6e` | Where it is closed, or why it stays |
|---|---|---|
| R835-1-F1 MAJOR (= R836-1 F1): acceptance 4 claimed met | **CLOSED** | The ruling amends acceptance 4. The REVIEW READY (issuecomment-6850450637) and the prepared PR body (`author-r2/PR-BODY.md`, sha256 `f9eb7668…a5e4`) state it by the ruling, "not as met", with a head-against-base table. I re-derived every figure from the graders at both commits (section A4 below). **The live PR #901 body is still round 1's** (it names `d023b77a`, "28" plants and 724/724). Replacing it with `PR-BODY.md` is a manager publication step (HANDOFF-r2 section 5), listed under the pending duties. |
| R835-1-F2 MINOR (= R836-1 F2 a): section 13's 8x8/2if pass cost 315 | **CLOSED** | `SPLIT_CONTROL_MEMORY.md:2211` reads 320, and `load_grade.py --check` at this head prints 320 (`receipts/graders/load_check_head.log`). |
| R836-1 F2 (b): section 5's rom growth "800 to 1,040 B" | **CLOSED** | `SPLIT_CONTROL_MEMORY.md:291` now reads "944 to 1,064 B" against `b2d39235`. That equals the author's per-image deltas (`author-r2/receipts/rom/deltas.md`) and R836-1's measurement. |
| R835-1-F3 MINOR (= R836-1 F3): 28 plants stated, 26 in the table | **CLOSED** | `srp_talker_mutants.defects()` now holds 29: 26 plus the 3 added in `e0398c40`. My SRP campaign at this head logs 58 `[ok] talker-` lines, 29 at 8x8/2if and 29 at 1x1/1if, and 398 `[ok]` in all (`receipts/fw/shard3.log`). The REVIEW READY and `PR-BODY.md` say 29 and SRP 398. The live body is stale, as for F1. |
| R835-1-F4 MINOR (= R836-1 RS2): `srp_bounds.h` said "once" | **CLOSED** (wording residue RS1 above) | `srp_bounds.h:50-58` now states IDLE_SLOPE and TALKER_DECL at most once per declarations pass, so at most twice on the interface the call builds, SR_DOMAIN once, LICENCE once per closed licence, and at most 5 + `MBX_N_PUB_SOURCES` writes in all. This matches `transmit()` at `srp_mbx.c:1228-1245` and `change_domain` at `:897-923`. `Talker.TransmitPublishesWithinItsTermsAfterARefusedJoin` (`srp_talker.cpp:501-542`) counts 2/2/1/0 on the built interface and 1/1/1/0 on the other. The plant `talker-transmit-publishes-past-its-terms` (`srp_talker_mutants.py:138-140`) is killed at both points (`receipts/fw/shard3.log:1139,1264`). |
| R835-1-F5 MINOR: a refused withdrawal's Leave is never retried | **CLOSED** | Details in the next table. |
| R835-1-RS1 (= R836-1 RS1): comment IDs and a lane name in `ctrl_memory.py` | **CLOSED** | `ctrl_memory.py:217` reads "(#895)". `:223-225` read "(#895): the cold-code move to flash owes …", which is the exact fix. The older "lane S14 … ruling 6505997821" text is the pre-existing instance #746 tracks. |
| R835-1-RS2: SRP README Talker paragraph | **CLOSED** | `README.md:193-198`: "A declared output's first declaration is…" and "Without a DA gate (`sources_valid`), unallocated outputs report… (code 2)". |
| R835-1-S1 | retained, optional | R835-2-S3. |
| R835-1-S2 | taken | R835-2-S4. |
| R836-1 S1 (the ignored Leave result) | superseded by F5's fix | `srp_mbx.c:295` now reads the result. |
| R836-1 S2, S3 | open, optional (that reviewer's) | The delta does not touch `srp_mbx_gate`'s comparison or the refused-swap test. |

**R835-1-F5 in detail.** Each check below holds at this head.

| Check | Result |
|---|---|
| The fix, in the code | `srp_mbx.c:295-300`: when `mrp_mad_leave` refuses, the source keeps its `talkers` bit and `done = false`, so `sources_owed` is set (`:338`). No hold-off starts. Otherwise the bit clears and `held_cs[n] = SRP_REDECLARE_CS`. The licence still closes first (`:284-289`) and is not closed again on the retry, since `active[n]` is already false. |
| The retry is taken | `prepare_declarations` reports the interface owed (`:929-930`), which arms the join count (`:1242-1244`). THE TRANSMIT runs only with no frame owed (`transmit_aged`, `:1250-1254`, called only from `ctrl_loop.c:231`). `owed_len` is set exactly while lwSRP holds the refused PDU (`send_pdu`, `:801-816`). So the next call's first pass meets no prepared PDU, and lwSRP takes the Leave. Its other refusal causes are a null app, an out-of-range port and `in_send`; none applies here. An attribute it cannot find is answered 0 (`mrp_mad.c:975`), so a re-created participant after a link reset clears the bit. |
| The test, at both points | `Talker.RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` (`srp_talker.cpp:545-591`) runs R835-1-F5's sequence: an adoption refused for storage, the ring refusing the built MRPDU, the adoption made after it through the real reclaim, and the Leave refused. It then asserts `TALKER_DECL` held, `sources_owed`, no hold-off, the Leave on the wire, `TALKER_DECL` clear at that Leave's commit, no Advertise after it, the hold-off started and nothing owed. |
| The three plants, at both points | `talker-refused-withdrawal-forgotten` (round 1's code), `talker-refused-withdrawal-not-owed` and `talker-transmit-publishes-past-its-terms` (`srp_talker_mutants.py:56-59,132-140`) are each killed by their named test at 8x8/2if and at 1x1/1if (`receipts/fw/shard3.log:1131,1135,1139` and `:1262-1264`). |
| No lwSRP change | The lwSRP gitlink is unchanged, `08ee86e8`. |

## The brief's checks

1. **Round-1 findings.** All closed. See the table above. F5 and F4 were checked at their cause.
2. **The Domain's leave and join.** **Not done, and stated as not done.** This is the ruling's item 4, "otherwise".
   - HANDOFF-r2 item 4b and section 2, the REVIEW READY's open risks and `PR-BODY.md:233` state it as found and not fixed.
   - A probe test (`author-r2/receipts/probes/domain-refused-path/probe-test.cpp`, run logs at both points) shows the adapter recording VID 3 adopted, while interface 0's MSRP Domain stays VID 2 on the wire (28 declaring events over 25 s, no Leave) and VID 3 is never declared.
   - The handoff argues why the mechanism differs: the new VID is reserved before the Leave, so owing the adoption would leave the reserved VID declared. I agree it is not the same one-line ownership fix.
   - `change_domain` (`srp_mbx.c:897-923`) is unchanged since the base.
   - **No issue for it is filed yet** (issue search at this round). It is a pending manager duty.
3. **Acceptance 4, re-derived** (section A4 below).
4. **The ROM ledger at every point, and the hot layout** (section A5 below).
5. **The gate pass, once, on a clean clone.** The author's single pass on `18300f6e` started 09:43 CET (`author-r2/receipts/gates/dispatch.txt`), before #810's round-30 REVIEW READY at 10:10 CET. So ruling item 6 did not require merging it.
   - I tallied `verify-table.md` myself (`receipts/verify-table-tally.txt`): 139 rc 0, 226 NOT RUN (every one with its reason), 0 bad. `verify.rc` is 0.
   - The Verilator sweep covers 65 suites: 60 logs plus 5 listed in `large.txt` as over 200 KB.
   - `gptp_shadow`, `gptp_tables` and `mbx` were re-run with `MAKEFLAGS=-j4 --no-print-directory`: make rc 0 and tally rc 0 for each, tracked changes 0 before and after (`sweep/rerun-shard1/summary.txt`).
   - The harness re-check: every arm's image loadable bytes are identical to the measured build. The `sha rc 1` values in `gates/harness/summary.txt` are the executables' stamps, explained in each `*-compare.txt`.
   - The only recorded input that differs is `tree:firmware`. Between `17ac263f` and the head, the firmware tree changes only `sw/firmware/gtest/coverage.ratchet`, which is not built into the image.
   - The first `regrade rc 1` of B1 and B8 was re-run to rc 0.
   - I did not re-run this pass, as instructed.

### A4. Acceptance 4, at head and at base, with every delta

I ran both graders at the head (`receipts/graders/*_head.*`) and at the base `b2d39235`, extracted with the same tsn-c-stack `715589c1` (`*_base.*`). `flip_base_vs_head.diff` is the whole difference.

| Point | Figure | Bound | Base | Head | Delta |
|---|---|---|---:|---:|---:|
| 1x1/1if | load at the pin / with tsn-c-stack#32 | ≤ 0.70 | 0.486 / 0.483 | **0.488 / 0.486** (HELD, rc 0) | +0.002 / +0.003 |
| 1x1/1if | R4 / R5 / R6 by every source | 20 / 90 / 90 ms | 66.12 / 35.95 / 28.67 | 66.77 / 36.24 / 28.92 | +0.65 / +0.29 / +0.25 |
| 8x8/2if | load at the pin / with #32 | 0.75 (#890) | 0.816 / 0.767 | 0.817 / 0.768 | +0.001 / +0.001 |
| 8x8/2if | R4 / R5 / R6 | 20 / 90 / 90 ms | 346.15 / 144.15 / 135.80 | 347.69 / 144.53 / 136.15 | +1.54 / +0.38 / +0.35 |
| both | queued notice first / last | 20 / 125 ms | unchanged | unchanged (8x8 first 22.00, OVER at both) | 0 |
| 8x8/2if, 1x1/1if | the load table's pass cost | | 315, 180 | 320, 185 | +5, +5 |

- `flip_grade.py --check` is rc 1 at both commits. Its OVER set is the same five plus "first" at both, and no verdict changes.
- `load_grade.py --check` is rc 0 at both. Its self-tests at the head pass (25/25 and 131/131).
- Every head figure equals R835-1's at `d023b77a`, and equals the REVIEW READY's table.
- The deltas the ruling accepted (R4 +0.65 ms, load +0.001) are unchanged. Every other delta is stated in the REVIEW READY and `PR-BODY.md`.
- **Measured rows** (this round's legs, `author-r2/receipts/costs/least-margin.txt` and `legs/legs-summary.txt`):
  - Arm A misses are 7 of 996 (8x8/2if) and 7 of 945 (1x1/1if), equal to the base's as the base tree's section 13 records them.
  - Least margins: 8x8/2if arm A 9.718 ms (base 8.973) and `answering-every-port` 7.879 (6.246); 1x1/1if arm A 11.233 (11.006) and the arm 9.036 (9.080, −0.044). All four base figures appear in the base tree's `SPLIT_CONTROL_MEMORY.md:2207`.
  - `R3-A8-p3/p4` show 19 refusals. These are duplicate runs the dedupe stopped (`legs/dedupe.log`). The merged 93 groups grade 0 refusals (`legs/mergeA8.txt`).
- **Verdict on acceptance 4 as amended:** the 1x1/1if long-window load holds at most 0.70, and every other figure is measured at both commits with its delta stated. **Holds.**

### A5. The ROM ledger at every point, and the hot layout

- **The images.** The author's eight images at `17ac263f` (`author-r2/receipts/rom/images-head.md`) equal, byte for byte, the eight I linked myself at `d023b77a` in round 1 (`895-r835-1-packet/receipts/rom/images.txt`):

  | Point | Fixture RAMB36 | Platform RAMB36 |
  |---|---:|---:|
  | 1x1/1if | 38.5 | 39.5 |
  | 1x1/2if | 41.5 | 43.0 |
  | 8x8/1if | 51.5 | 53.0 |
  | 8x8/2if | 58.0 (ledgered 58.5) | **60.0** (ledgered 60.0, cap 60.5) |

  - At 8x8/2if, `ctrl_plat` is 20,352 B and the platform rom 129,288 in 131,072.
  - The `answering-every-port` arm's image is 124,444 B (58.5), within its ledgered 58.5.
  - Every other point is at or under 56.
- **Head builds.** The gate pass's head-built arm images are 124,136 B (arm A, 8x8/2if) and 124,444 B (the `answering-every-port` arm), equal to the ledger figures (`gates/harness/*-compare.txt`).
- **`test_ctrl_memory.py`:** PASS, 0 failures, including the ledgered-entry plants (`receipts/graders/test_ctrl_memory.log`).
- **The hot layout, my own probe** (`scripts/layout_probe.sh`, `scripts/layout_compare.py`, `receipts/layout/`). I linked the split size-fixture image on the RV32 stand-ins from my clone at this head, then with `d023b77a`'s and `e0398c40`'s `srp_mbx.c`. That is the only firmware source the delta changes; it was restored by `git show HEAD:` and the clone re-verified. At both points:
  - From `d023b77a` to head, exactly two symbols change size: `moved` 0x68→0x64 and `declare_sources` 0x3b4→0x3b8 at 1x1/1if (0x3a8→0x3ac at 8x8/2if).
  - 3 symbols move, and **0 of the 381 symbols after `declare_sources` move**. 8x8/2if rom is 124,136 at both.
  - From `e0398c40` to head, 309 and 339 of those symbols move. That is the 4 B shift the author found and `17ac263f` undoes.
- **`moved`'s rewrite.** `i->stale |= t->reg_from != t->reg_to` gives the same value as `i->stale = i->stale || …`: `stale` is a `bool` and the right side is 0 or 1. Branch coverage drops by the short-circuit's branches only (raw 653/656 → 651/654, the same 3 exclusions).

## Each lens, with what it examined (exact head `18300f6e`)

```text
[R835] PASS Conformance - sw/firmware/ctrl/srp/srp_mbx.c:282-300,309-338 (the refused Leave kept declared and owed), :1221-1254 (THE TRANSMIT and its due), third_party/lwSRP/src/core/mrp_mad.c:946-980 - against #895 acceptance 1, 2, 3 and 5, acceptance 4 as amended by ruling issuecomment-6840463408 (re-derived by load_grade/flip_grade at head and base, receipts/graders), ruling items 1-6, 802.1Q 35.2.2.8 and 10.7.4.3: no stale Talker remains after a refused withdrawal; the Domain item is stated not done per item 4
[R835] PASS RTL - srp_mbx.c:295-300 (int result tested, bit and hold-off only on success), :399 (bool |= 0/1, same value), srp_bounds.h:43-59 (5 + MBX_N_PUB_SOURCES within SRP_MBX_PUB_POLL_MAX), receipts/layout/layout-compare.txt (symbol sizes and addresses, both points) - no HDL in the delta; the only wording slip is RS1 (RESIDUE)
[R835] PASS Robustness - refused Leave after a refused build (srp_mbx.c:295, :929, :1242, :1253), licence closed once (:284-289), reset during the window (mrp_mad.c:975 finds nothing, bit clears, hold-off arms), re-valid unchanged or moved before the retry (:282, :306-309) - one suggestion, S1
[R835] PASS Tests - sw/firmware/ctrl/test/srp_talker.cpp:501-591 (2 new tests), srp_talker_mutants.py:37-38,56-59,132-140 (3 new plants, 3 re-anchored), receipts/fw/shard0-3.log (all rc 0: control 696/696, AECP and SRP campaigns, 58 talker- kills, 398 [ok]), receipts/coverage/fw_coverage.log (srp_mbx.c 725/725, 651/654 raw = 100 % after the 3 standing exclusions; PASS 39 files)
[R835] PASS Docs - docs/design/MAILBOX_SPLIT.md:1143-1146,1166-1171, docs/design/SPLIT_CONTROL_MEMORY.md:282-291,2202-2211, sw/firmware/ctrl/srp/README.md:193-198,222-236,421-434, sw/litex/ctrl_memory.py:217,223-225, REVIEW READY issuecomment-6850450637, author-r2/PR-BODY.md, author-r2/HANDOFF-r2.md - checked against the code, the graders, the cost receipts (costs/G1, G8: 15,078, 27,578, 1,987, 9,618, 19,439; load_grade STATED centisecond 130 and 510 us) and the images; scripts/docs_check.py rc 0 (0 findings), git diff --check b2d39235..HEAD clean; residue RS1 (RESIDUE) and S2 (packet index) only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c` refused-Leave and THE TRANSMIT paths, `mrp_mad.c` refusals, #895 acceptance 1-5 and the ruling, both graders at head and base | R835-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| RTL | CLEAN (RS1 RESIDUE) | `srp_mbx.c:295-300,399`, `srp_bounds.h:43-59`, the hot-layout probe at both points; no HDL in the diff | R835-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Robustness | CLEAN (S1 SUGGESTION) | refused build, refused Leave, retry, licence, reset, re-validity during the window | R835-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Tests | CLEAN (S3 SUGGESTION) | `srp_talker.cpp` new tests, `srp_talker_mutants.py`, four firmware shards rerun, coverage ratchet | R835-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |
| Docs | CLEAN (RS1 RESIDUE; S2 SUGGESTION) | the three docs and `ctrl_memory.py` in the delta, REVIEW READY, `PR-BODY.md`, handoff, `docs_check.py`, `git diff --check` | R835-2 | `18300f6e5f0c63b2ebc81d6bbc243496034f638a` |

Round 1 (R835-1 at `d023b77a`) covered Tests clean. The delta changes test artifacts, so this round covers Tests again, at this head.

## Real limits

- **No hosted exact-head evidence exists.** At 2026-11-13T10:48Z, the head had 0 check runs and 0 statuses, and PR #901 is `mergeable=CONFLICTING` against `665-s2b-cycles` (`receipts/hosted-checks.txt`). The conflict is the KNOWN base move to #810's round-30 head `32551422`.
- **Not re-run by me:** the CPU budget harness legs, the four-workflow clean-clone pass and the Verilator sweep. I verified their receipts and spot-checked the figures above.
- **The platform images were not rebuilt this round.** No split-SoC exports were available in this round's scratch. Their figures rest on three things: the author's images at `17ac263f`, their byte equality with my own round-1 links, and my layout probe, which shows a net-zero size change in the one changed source.
- **My layout probe ran on the RV32 stand-ins, without the flash map.** That image is 8 B larger at 1x1/1if (108,880 against 108,872). The comparison is relative, between images built the same way.
- **The Domain path:** the author's probe was read, not re-run.
- **The packet archive is unsigned.** Its INDEX matches 726 of 730 files (S2).
- **Not run:** physical calibration and hardware. Acceptance 6 belongs to the bench lane.
- **No manager source bank ran at this head**, and none is claimed or inferred.

## Pending manager duties

- **Replace PR #901's body with `author-r2/PR-BODY.md`** (sha256 `f9eb7668e525cdf89e11a23a4854ef21ccc87af7bf1584e4a49848491106a5e4`). The live body still states round 1's head, 28 plants and 724/724. F1's and F3's closure on the PR depends on it; this verdict covers the prepared body.
- **File the two issues the lane routes out:**
  - the Domain's own leave and join on the refused path (HANDOFF-r2 section 2, with the probe);
  - the Domain adoption's in-place `vlan_identifier` change, a FirstValue change (R835-1's pending duty, still unfiled).
- Carry R835-2-RS1 to the residue checklist.
- The sync with #810's round-30 head (ruling item 6), then hosted and act acceptance of the long gates at the resulting head. This review's coverage is banked at `18300f6e`, so a sync that changes any lens's scope un-covers that lens.
- The current-dev merge-candidate validation: source base `b2d39235ab9bba85d7e560b5f5f78fb4be528960`, live dev `b7d692952305e4e0e132abb8f99c339eeb17a873`.
- The bench item, acceptance 6.

## Receipts and scripts

All are listed in `MANIFEST.sha256`. Host-specific paths are replaced by `<packet>`, `<clone>`, `<home>` and `<tools>`.

- **Scripts:**
  - `scripts/check_index.py`: re-hashes a packet's INDEX.
  - `scripts/layout_probe.sh` and `scripts/layout_compare.py`: the hot-layout probe. The final runs were from the clone, with the file swap shown in the report.
  - `scripts/verify_clone.sh`: the byte-exact check.
- **Receipts:**
  - `receipts/graders/`: load and flip at head and base, their self-tests, the head-against-base diff, `test_ctrl_memory`, `docs_check` and `diff --check`.
  - `receipts/fw/`: the four self-test shards, logs and rc.
  - `receipts/coverage/`: the coverage ratchet check.
  - `receipts/layout/`: symbol tables and the comparison.
  - `receipts/author-index-check.txt`, `receipts/verify-table-tally.txt`, `receipts/hosted-checks.txt` and `receipts/clone-verify.txt`.

R835-2 FINISHED
