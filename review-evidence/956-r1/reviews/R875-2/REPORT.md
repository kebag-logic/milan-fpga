[R875] NEGATIVE - exact head 1825ba4eaccfe40788391b7af5533fae8c910a85

Internal independent review R875-2 of #956 / #957, PR #958. Tree `450fc60a4ae5c1259afe9b487d5593e31e8fa8ee`. This is a
delta round: `0d80f0ed..1825ba4e`, five commits, code head `847b2e21` (`1825ba4e` changes docs only). I worked from a
cleared context and rebuilt the task from public state, then applied all five lenses to the delta, with artifact
evidence for each.

**Every named prior finding is resolved at its cause.** That covers R876-1-F1/F2/F3 and R875-1-F1/F2/F3, re-run with
their reviewers' own probes and with mine. Conformance, RTL, Robustness and Tests are clean.

**One MINOR is open, so the verdict is NEGATIVE.** It is R876-2-F1, a Docs finding, retained:

- PR #958's "Known limitations" section still states round 1's figures as current: 16 B of rom left, and four costs at
  their statements.
- The same body's round-2 section and the current receipts say 128 B, and only two costs at their statements.

I verified it independently in the live PR body. My own Docs pass missed it, and the addendum explains how. No code,
test or repository-document change is needed. A PR-text correction and a Docs re-check clear it.

Also recorded, so the author can absorb everything in one pass:

- three SUGGESTIONs (S1 to S3);
- two RESIDUEs (W1, and W2, which is R876-2-R1 retained).

## Contents

- **[Findings](#findings)**: D1 (MINOR, R876-2-F1 retained), S1 to S3 (SUGGESTION), W1 and W2 (RESIDUE).
- **[Prior findings at their cause](#prior-findings-at-their-cause)**: round 1's six, all resolved, and round 2's two
  concurrent ones, both retained.
- **[The six checks in the brief](#the-six-checks-in-the-brief)**.
- **[Clean results by lens](#clean-results-by-lens)**.
- **[Ledger](#ledger)**.
- **[Limits and pending manager duties](#limits-and-pending-manager-duties)**.
- **[Addendum](#addendum-how-d1-was-reached)**: how D1 was reached.
- **[Receipts](#receipts)**.

## Findings

### D1 (R876-2-F1, retained): MINOR, Docs: the PR body's current limitations state round 1's rom margin and costs

- **Where.** PR #958 body, "Known limitations / out of scope", lines 249 to 259 of the live body
  (`receipts/pr-body-live-1825ba4e.md`; excerpt in `receipts/pr-body-stale-figures.txt`).
- **Evidence.** What the section states as current, against the current receipts:
  - **8x8/1if rom.** The section says "16 bytes left". `rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt` gives 139,136 of
    139,264 B, **128 B** left. The same PR body says so at lines 43-44.
  - **`centisecond` at 1x1/1if.** The section says 16,064 cycles, 170 of 170 us. `cpu-1x1-legs-0d80f0ed-vs-b4a1dde2.md`
    gives **14,213 cycles, 150 of 170**.
  - **`record.srp` at 8x8/1if.** The section says 35,273 cycles, 375 of 375. `cpu-8x8-1if-legs-...md` gives
    **35,507**, 375 of 375.
  - **`record.maap` at 8x8/1if.** The section says 17,259, 185 of 185. The receipt gives **17,014, 180 of 185**. The
    body's own line 63 says the same.
  - **Which costs sit at their statement.** The section says "four of them". At this head it is
    `item.acmp_declined` at both points (20 of 20 at 1x1/1if, 30 of 30 at 8x8/1if) and `record.srp` at 8x8/1if.
- **Authority.** AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer".
  The owner rule of 2026-10-02 says a defect that changes a figure or measurement claim is not RESIDUE.
- **Impact.** One review object gives two different current rom margins and cost-margin risks. A cold reader cannot
  tell which one is the head's. Nothing is wrong in the implementation or the budget.
- **Required outcome.**
  - The limitations section states the head's figures, or labels the old ones as round 1's next to the current ones.
  - The section lists only the costs that sit at their statement now.
  - The formal-measurement limitation stays.
- **Verification.** Compare the revised body with `author-r2/receipts/rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt` and
  both `cpu-*-legs-0d80f0ed-vs-b4a1dde2.md` receipts, then re-check Docs at that body.

### S1: SUGGESTION, Tests: the reset tests exercise only source 0, so a clear limited to source 0 escapes at 8x8

- **Where.** `sw/firmware/ctrl/test/srp_talker.cpp:911-958` (`Talker.ListenerRegistrationAfterAResetIsNoticed`, which
  uses `identity(k,0)` and `declaration[0]` only), and `test_aecp.cpp`'s
  `AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` (output 0 only, as
  `sw/firmware/ctrl/srp/README.md` says).
- **Evidence.**
  - The reviewer plant `r875-reset-clears-source-0-only` changes `reset_interface` to
    `i->declaration[k] = k == 0u ? 0u : i->declaration[k];`.
  - At 8x8/2if (`CTRL_SRP_SOURCES` 8), every shipped test passes: `[ESCAPED]` in `receipts/plants/own2.log`.
  - At 1x1 there is one source, so the same plant is equivalent there (`own1.log`).
  - `r875-reset-records-ready` (the record reset to Ready instead of none) is caught at 1x1/1if and 8x8/2if, and
    `r875-whole-build-keeps-its-due` is caught too.
- **Impact.** None at this head: the shipped clear loops over every source (`srp_mbx.c:1185-1193`). A later edit that
  clears fewer sources would not be caught.
- **Suggested outcome.** At 8x8, also run the register / reset / return sequence on a source other than 0, for example
  the last one.
- **Verification.** `scripts/plants.py <checkout> <out> own 2 - r875-reset-clears-source-0-only` is caught.

### S2: SUGGESTION, Tests: three unchanged hand drivers and helpers still key on `tx_due`, which no longer shows a paused build

- **Where.**
  - `sw/firmware/ctrl/test/srp_rx_retry.cpp:152`: `if(adapter.tx_due!=0u) loop.transmit(...)`.
  - `srp_mbx.cpp:1962-1966` (`idle()`, "it owes no MRPDU").
  - `srp_talker.cpp:694` ("nothing owed").
- **Evidence.**
  - The pause now takes the interface's due, and the build is owed through `tx_resume`/`tx_owed`. The author re-keyed
    `srp_app.cpp` and `srp_feedback.hpp` for this.
  - `scripts/rx_retry_drift.py` counts **38** iterations of `SrpRetry.AnAttributeChangeAloneAllowsTheRetry`'s hand loop
    that leave a paused build undriven (`receipts/probes/rx-retry-drift-count.log`).
  - Re-keyed on `tx_owed`, the test still passes (`rx-retry-drift-owed.log`).
  - `idle()` and the line-694 loop advance a serviced loop, which resumes a paused build within the same `advance`.
- **Impact.** No verdict changes; the drivers now run a slightly different sequence from the one they describe.
- **Suggested outcome.** Key these three on `tx_owed`.
- **Verification.** The suites pass, and the drift probe counts 0.

### S3: SUGGESTION, Tests: the new 8x8/1if Talker arm's sweep is planted only at 1x1/1if and 8x8/2if

- **Where.** `sw/firmware/ctrl/test/srp_arms.py:107` adds the 8x8/1if `srp_talker.cpp` arm. The SRP campaign's 8x8/1if
  table (`test_ctrl_firmware.py:231-235`) takes only the Listener and reclaim prefixes, not `talker-`.
- **Evidence.**
  - At 8x8/1if, 0d80f0ed's firmware fails its own phase band, `Held310` to `Held380`
    (`receipts/probes/SUMMARY-base-0d80f0ed.txt`). R875-1's 100 ms probe missed that band at base (held max 29,997 ms).
  - My run `srp1-8x8-talker` plants `talker-resume-drops-what-came-due`, `...-at-a-phase` and
    `talker-registration-kept-across-a-reset` at 8x8/1if, and all three are caught (`receipts/plants/srp1-8x8-talker.log`).
- **Impact.** None at this head. The gate's plant evidence skips the one point whose band differs.
- **Suggested outcome.** Optionally add the `talker-resume-*` rows to the 8x8/1if campaign.
- **Verification.** They are listed `[ok]` there.

### W1: RESIDUE, Docs: the design page's "112 bytes smaller" names no base

- **Where.** `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, "The rom it fits in". The sentence reads: "In `transmit`
  the kept due took 12 more and filled the rom, 139,264 B; at one interface ... `transmit` is 112 bytes smaller there
  ...: 139,136 B, 128 left."
- **Why it is wording only.**
  - Every figure is right. `transmit` is 1,184 to 1,072 B against `0d80f0ed` (−112; author `imgdiff/plat-8x8-if1`). The
    rom is 139,248 − 112 = 139,136, which is 128 B below the 139,264 B form.
  - Read after "139,264 B", though, the sentence implies 139,264 − 112 = 139,152.
- **Exact fix.** Replace "so `transmit` is 112 bytes smaller there with the kept due and the refused slice's due:
  139,136 B, 128 left" with "so `transmit` is 112 bytes smaller there than at `0d80f0ed`, with the kept due and the
  refused slice's due: 139,136 B, 128 below that form and 128 left".

### W2 (R876-2-R1, retained): RESIDUE, Docs: the PR body's reviewer roles still say "to be assigned"

- **Where.** PR #958 body, lines 76-77 (`receipts/pr-body-stale-figures.txt`).
- **Why it is wording only.** It is administrative wording. No measurement, test, code, contract or verdict changes.
- **Exact fix.**
  - "Internal cleared-context reviewer: [R875] (round 2 start: issuecomment-7073171544)".
  - "External reviewer: [R876] (round 2 start: issuecomment-7073176800)".

## Prior findings at their cause

Round 1's findings were read only after my own pass over the diff, and each was re-run with its reviewer's own probe.

- **R876-1-F1 and R875-1-F1 (MAJOR, a stale Listener record after a reset): resolved.**
  - The fix: `srp_mbx.c:1191` clears `declaration[k]` with `listener_present[k]` in `reset_interface`'s per-source
    loop.
  - R876-1's `reset_probe.cpp`, unchanged: passes at 1x1/1if, 8x8/1if and 8x8/2if, and fails on 0d80f0ed's firmware at
    all three.
  - R875-1's `probe_link_reset_957.cpp`, unchanged: at head, step 5 gives "notices 1/1 answer flags_ex 1" at 1x1/1if,
    1x1/2if and 8x8/1if. On 0d80f0ed it gives "notices 0/0".
  - The two shipped reset tests pass at head and fail on 0d80f0ed. They cover each declaration, equal before and after,
    edges apart, coalesced and twice over, the reset silent, an unchanged repeat silent, the other interface kept, and
    one notice per registered controller with the flags.
  - Closed gates: my P2 sees noticed 0 behind a closed gate after a reset, at all three points.
  - Plants `talker-registration-kept-across-a-reset` (three points) and `registration-notice-kept-across-a-reset` are
    caught.
- **R876-1-F2 (MAJOR, the latest case with the join timer running): resolved.**
  - The fix: the `again` capture and the pause taking the due (`srp_mbx.c:1430-1457`), with `tx_owed` read whole by
    `transmit_aged` and the poll (`srp_mbx.c:1404,1474`; `srp_mbx.h:169-182`).
  - R876-1's `focused.py` phases mode cannot patch the restructured body. R875-1's `probe_phase_956.cpp`, unchanged,
    keeps its semantics: held, no idle precondition, 1.5 s of observation, the absolute bound.
    - Held phases 100 to 900 give at most 29,995 ms (1x1/1if), 29,997 ms (8x8/1if) and 29,995 ms (8x8/2if); serviced
      phases give at least 29,700 ms.
    - On 0d80f0ed: 30,700 ms (1x1/1if, phase 300) and 30,600 ms (8x8/2if, phase 400), R876-1's own figures.
  - `EveryPhase/TalkerPhase.*`: 200 of 200 pass at each point at head. On 0d80f0ed it fails exactly `Held270` to
    `Held340`, `Held310` to `Held380` and `Held340` to `Held410`.
  - Both assertions are absolute: `srp_talker.cpp:190-192` (`EXPECT_LE(adv->time_ms, l.at+kTwoLongestLeaveAllMs)`) for
    the latest, `EXPECT_GE(..., l.at+kHoldOffMs)` for the earliest.
  - Plants caught: `talker-hold-off-adds-its-terms-at-the-latest` and `talker-hold-off-a-centisecond-short`. The
    re-anchored `talker-unchanged-held` is caught by `Talker.UnchangedDestinationIsDeclaredAgainAtOnce`.
- **R876-1-F3 and R875-1-F2 (MINOR, `FR_NFR.md:427`): resolved.**
  - The row gives 2,973 cs at 8x8/1if and 2,970 at two interfaces (2,971 at 99 ms), and says "sooner, 10 ms sooner".
    The older figures are marked as history.
  - Checked against `srp_mbx.c:47` and `ctrl_loop.h:369-396,459`: 3000−19−4 = 2,977, 3000−19−8 = 2,973,
    3000−19−11 = 2,970, and 3000−19−10 = 2,971.
- **R875-1-F3 (MINOR, the SRP README's rom figure): resolved in that artifact.** `README.md` states 139,136 B with
  128 left, and 44 B for the record and the clear (40 + 4). D1 is the separate stale copy in the PR body.
- **R876-2-F1 (MINOR) and R876-2-R1 (RESIDUE), from the concurrent round at this head: retained** as D1 and W2. I
  verified both independently in the live PR body.

## The six checks in the brief

1. **F1 at its cause.** See above. P1 adds a check on the licence: after a reset with no returning Listener there is
   no `licence(true)`, and `active`, `registered`, `listener_present` and `declaration` are all 0, at all three points.
2. **F2 at its cause.**
   - **P3, a reset between a paused build's slices.** The victim is interface 0 at one interface, and each interface in
     turn at two. Nothing wedges: `tx_owed` settles to 0, there are 0 reentries, and every interface sends again.
   - **P4, the request off the centisecond** (`tick_div` 1, 5 and 9; phases 300, 340, 370 and 700; held). It gives
     29,986 to 29,994 ms (1x1/1if and 8x8/2if) and 29,988 to 29,996 ms (8x8/1if): within 30,000 ms and at least
     29,000 ms.
   - **`Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue`** passes at 8x8/1if and 8x8/2if.
   - **Its plants.** The five `build-*` plants and the re-anchored `transmit-due-cleared-with-a-frame-owed` are each
     caught on their own words.
3. **The one-interface build's interface at compile time** (`srp_mbx.c:1434`). It is behaviour-neutral:
   - A resumed build has `resume` of 1 or 2, so its interface was already 0.
   - A whole build is entered only with `tx_owed != 0` (`ctrl_loop.c:267`), so with `resume` 0, `tx_due` bit 0 is set.
   - Both shapes' suites pass.
4. **Memory.**
   - `plat_ledger.py` was refused here (no LiteX; `receipts/plat-ledger-head.log`).
   - The manifest-verified author receipt gives 8x8/1if rom 139,136 B (34 RAMB36 of rom, 128 left, within 58).
     `ctrl_plat` is 18,048, 19,712, 18,944 and 21,568 B, unchanged at all four points.
   - My rv32 `srp_mbx.o` objects corroborate the direction under the arm's flags (`receipts/rv32-fn-sizes-*.log`). At
     1x1/1if, 8x8/1if and 8x8/2if, `transmit` changes by −132, −128 and +36 B, `reset_interface` by 0, +4 and +4, and
     `poll` and `transmit_aged` are unchanged. The image receipt gives −116, −112 and +36.
5. **Docs.** The repository documents are correct. The PR body is D1 and W2, and the design page is W1.
6. **Firmware gate and CPU rows** (author receipts at `847b2e21`, manifest-verified).
   - **Gate.** Four shards, rc 0, 0 escaped. Shard 0 has 76 PASS, including the new 8x8/1if Talker arm. Plants: 826,
     389 and 574 `[ok]`.
   - **CPU legs.** 0 findings at both points, the seven known misses each side, and every stated cost within.
     `grade-checks-b4a1dde2.txt` passes. The formal measurement is not run (limits).

## Clean results by lens

```text
[R875] PASS Conformance — sw/firmware/ctrl/srp/srp_mbx.c:36-49,1185-1193,1430-1474 at 1825ba4e; receipts/probes/SUMMARY.txt, SUMMARY-base-0d80f0ed.txt — #956: hold-off 2,977/2,973/2,970 cs from the named LeaveAll constant less both terms; on the model's wire no later than 30,000 ms and no sooner than the hold-off at every centisecond phase, held and serviced, idle and running join timer, at 1x1/1if, 8x8/1if and 8x8/2if (sweep 200/200 at each point; prior probes held max 29,995/29,997/29,995 ms; off-centisecond 29,986-29,996 ms); #957: the first post-reset Listener registration under an open gate is noticed once whatever it declares (Milan v1.2 5.4.5.2/Table 5.22; IEEE 1722.1-2021 7.5.2); the reset, an unchanged repeat, the other interface and a closed gate are silent; one notice per registered controller on the wire
[R875] PASS RTL — sw/firmware/ctrl/srp/srp_mbx.c:1424-1475, srp_mbx.h:169-182, loop/ctrl_loop.c:263-268 at 1825ba4e — no HDL, CDC, mailbox ABI or gitlink change in 0d80f0ed..1825ba4e (six gitlinks identical, receipts/restore-verification.txt); tx_due is set only by tick, hold and the walk (srp_mbx.c:135,154,541) and cleared by the build's end and reset_interface; the pause takes the due and `again` keeps only what came due between slices; the paused build is aged and owed through tx_owed (the union read whole); MBX_N_IF==1 interface 0 is behaviour-neutral; rv32 sizes corroborate the image receipt
[R875] PASS Robustness — receipts/probes/srp-probes-*.log (P1-P4), receipts/plants/*.log at 1825ba4e — a reset between a paused build's slices (own and other interface) wedges nothing; no licence without a Listener after a reset; a closed gate after a reset is silent; a refused second-slice frame keeps its interface due (A3, plant caught); coalesced and doubled link edges are covered by the shipped test; whole builds still end owing nothing (reviewer plant caught)
[R875] PASS Tests — test/srp_talker.cpp:138-195,421-465,911-958; test/srp_mbx.cpp:1739-1808; test_aecp.cpp's new AppOutputs test; the three changed plant tables at 1825ba4e — every new test fails on 0d80f0ed's firmware (reviewer rerun) and passes at head; 12 named author plants and 2 of 3 reviewer plants are caught on their own words (the escape is S1, a SUGGESTION); existing suites green (srp_talker 219/219 at three points, the srp_mbx subset, AppOutputs)
[R875] MINOR Docs — PR #958 body:249-259 at 1825ba4e — D1 (R876-2-F1 retained): the current limitations state round 1's rom margin and costs; repository docs (FR_NFR.md:427, srp/README.md:317-339,410, SPLIT_CONTROL_MEMORY.md section 13) checked against srp_mbx.c:47, ctrl_loop.h, the ledger receipt and the image diffs, and correct but for W1; no new source comment carries a lane label, round or reviewer ID (receipts/comment-rule-scan.txt: only the loop's own assumption ID A3, ctrl_loop.h:56)
```

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `srp_mbx.c` hold-off and notice paths; sweep, latest and running-timer tests; prior probes and P1/P2/P4 at three points; base reruns | R875-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| RTL | CLEAN | `srp_mbx.c` `transmit`, `transmit_aged`, `poll`, `reset_interface`; `srp_mbx.h` union; `ctrl_loop.c` dispatch; gitlinks; rv32 objects | R875-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Robustness | CLEAN | P1 to P4; reset, closed gate, coalesced links, refused second slice; plants | R875-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Tests | CLEAN (S1, S2 and S3 are SUGGESTIONs) | new and changed tests and plant tables; base discrimination; 12 author and 3 reviewer plants; gate receipts | R875-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |
| Docs | UNCLEAN (D1 MINOR open; W1, W2 RESIDUE) | `FR_NFR.md:427`, SRP README, `SPLIT_CONTROL_MEMORY.md` section 13, PR #958 body, new source comments | R875-2 | `1825ba4eaccfe40788391b7af5533fae8c910a85` |

Code the delta does not touch keeps its prior lens verdicts. Nothing in the delta changes what those verdicts depend
on. D1 is PR text only: after it is corrected, only Docs needs re-covering, because no code, test or repository-document
artifact changes.

## Limits and pending manager duties

- **No manager source bank** runs at this head, and none is claimed or inferred.
  - Source-head execution evidence is the author's published receipts. The files I used, 43 of them, hash-match
    `MANIFEST.json` (`receipts/evidence-manifest-verify.txt`).
  - That is hash consistency only. I verified no cryptographic signature.
- **I did not run the full firmware gate, the twin, the builder, Yosys or Verilator.** I ran focused arms, probes and
  plants only.
  - `plat_ledger.py` was refused here (no LiteX), so the rom figures rest on the author's receipt, corroborated in
    direction by my rv32 objects.
  - I did not run the composed MAAP-conflict arm (`SrpGate`). The author's shard-0 receipt carries it.
- **The formal CPU measurement is not run.** `record.srp` at 8x8/1if sits at its 375 us statement, about 200 cycles
  under the next step, so a group outside the legs could exceed it. The 8x8/1if `srp-talker-held` leg ran twice, the
  second time unbooked, as the author discloses.
- **#956's bench criterion, 29 to 30 s at 1x1/1if and 8x8/1if, is unmet.** It needs hardware. It is a completion
  condition for the manager or bench, not a review finding. Physical calibration was NOT RUN. Model results and skipped
  contexts are not hardware proof.
- **Hosted checks at `1825ba4e`.** When I read them they were mostly queued or in progress, and `bdd-conformance` had
  succeeded (`receipts/hosted-checks-1825ba4e.txt`). I did not audit which jobs executed and which were skipped. Hosted
  and act acceptance belong to the manager.
- **The manager still owns:**
  - the current-dev merge candidate (source base `15168e14` against live dev
    `e275d7950ef3385753e6a15d2e191ba855b171ed`) and its builder and native banks;
  - the positive reviews;
  - W1 and W2 on the residue checklist;
  - merge authorization;
  - post-merge containment.

## Addendum: how D1 was reached

My verdict and ledger were first written POSITIVE. The independent pass had found no MINOR. The pre-addendum report's
sha256 is in `scratch/` and is not published.

I then read the concurrent external verdict at this head, issuecomment-7073265718 (R876-2). That is the first other
review I read for round 2.

- **R876-2-F1.** I checked it against the live PR body (`receipts/pr-body-stale-figures.txt`), and it holds as
  stated. My own PR-body scan had looked for "16 left" and matched only the correctly framed line 196. It missed "16
  bytes left" at line 259 and the stale cost list at lines 253-257. Under the owner's rule a stale figure claim is not
  RESIDUE, so I retain it as MINOR (D1). That makes the verdict NEGATIVE.
- **R876-2-R1.** It also holds (lines 76-77) and is retained as RESIDUE (W2).
- **The rest of R876-2's dispositions** agree with mine. This includes all six of round 1's findings resolved.

## Receipts

Everything listed in `MANIFEST.sha256`, under `receipts/` and `scripts/`.

- **Scripts.** `probe_arm.py`, `run_probes.sh`, `run_base.sh`, `plants.py`, `run_plants.sh`, `rx_retry_drift.py`,
  `rv32_fn_sizes.py`, `summarize.py`, `fetch_evidence.sh`, `verify_manifest.py`, and the reviewer probe
  `probe_r875_2.cpp`.
- **Prior reviewers' probes.** These ran unchanged from the public evidence tree at
  `362a303989763207c30c801b66aa9333a0130204`, `review-evidence/956-r1/reviews/`.
- **Base runs.** They use `git archive 0d80f0ed` with head's `srp_talker.cpp` and `test_aecp.cpp` in place, and the
  submodules linked to the clone's identical gitlinks.
- **The clone after the probes.** It is verified byte-exact at head: blobs, modes, index and gitlinks. The ignored
  caches the arms created were removed (`receipts/restore-verification.txt`).

R875-2 FINISHED
