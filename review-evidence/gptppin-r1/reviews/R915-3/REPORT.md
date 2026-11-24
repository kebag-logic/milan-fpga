[R915] POSITIVE - exact head fc6870cab13f74149864b80b6480ddb3641cb936

# R915-3: internal cleared-context delta re-review of PR #995 (Closes #994)

- Head `fc6870cab13f74149864b80b6480ddb3641cb936`, tree `47c0ec30481efe50fd892060ebeb61ef9bc423c2`. Previously reviewed head `f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21`. Train base `300da99beed5bb1c77e4b04af0bb4f9369856e0d` (base branch `dev-soft-core`).
- Delta: two commits, `567eaa48` (harness, campaign, lifecycle counts) and `fc6870ca` (records). Six paths: `tb/verilator/gptp_shadow/{sim_main.cpp,mutants.py,test_mutant_lifecycle.py,README.md}`, `docs/reference/SUBMODULES.md`, `CHANGELOG.md`. No RTL, generator, firmware, synthesis input, image or gitlink changes.
- Order followed: AGENTS.md and CONTRIBUTING.md; #994's frozen body (it has no comments); the delta and history; then the public packet `review-evidence/gptppin-r1/author-r3` at `1fe0516a`. I read the round-2 findings (R915-2, R916-2) only after my own pass over the delta, and wrote this report before reading any other round-3 report.
- Verdict basis: both round-2 MINORs are fixed at their cause. I ran each reviewer's falsifying probe at the head, and each now fails its named check. Both are also planted as campaign controls and are caught by name. No new MINOR or higher. Three wording RESIDUEs and five SUGGESTIONs follow.

## Evidence integrity

- Packet `1fe0516a:review-evidence/gptppin-r1/MANIFEST.json`: 576 of 576 entries match their `published_sha256`, including all 176 `author-r3/` entries. None mismatch, and no file outside the manifest is present apart from the manifest itself (`receipts/published/evidence-manifest-verify.txt`).
- `git verify-commit` reports no signature on `1fe0516a`. "Signed" therefore means content-hashed here. Signer identity is not verified.
- PR #995's live body is byte-identical to `author-r3/PR-BODY.md`, apart from one trailing blank line.
- Toolchain: scoped `Verilator 5.050 2026-07-01 rev v5.050`, launcher sha256 `905795b9…e92f` (`toolchain.txt`).
- Every probe ran in its own disposable shared clone at the head (`scripts/probe_setup_r3.py`). Host load was 190 to 220.

## My executions at fc6870ca (raw logs in `receipts/published/`)

| Case (`make run` in `tb/verilator/gptp_shadow`) | Edit (`probe-diffs/`) | Result |
|---|---|---|
| `head` control | none | **424 checks: 424 PASS, 0 FAIL**, rc 0. Race: last beat +285, re-election +1,281. Reserve arm: 5 outstanding; withheld Announce at 2,000,103 |
| `order-stall` (R916-2's `order-probe.patch`, stall hunk verbatim; its print hunk has no anchor now) | harness: `tx_tready_i = 0` before, `= 1` after the race's queued Announce | rc 2, **423/424**. The one failure is `#106 race: one master Announce reaches the lane before the re-election` (got 0). Last beat +4,659, re-election +1,281 |
| `order-stall-short` (my discrimination control) | harness: lane held only from the queued Announce's injection to 2 ms after it, so the stall starts after the master Announce has left | rc 0, 424/424, last beat +285. The check is not tripped merely by a stall. It grades the order |
| `p106-nocredit` (my R915-2 probe, verbatim) | generator: `e_credit_gate` dropped from `prog_leg_anntx` | rc 2, **421/424**. It fails `#106 reserve: no master Announce reaches the lane without credit` (got 1), `#106 reserve: two master Announces once the credit returns` (got 3) and `#106 reserve: the withheld Announce leaves 1 s after the instant` (first at +279). The seal arm still passes (2,000,097), as its comment now states |

| Other gate at the head | Result |
|---|---|
| Campaign: `mutants.py`'s own `main()` on the two new controls (`scripts/campaign_slice.py`, population 13) | `[ ok ] announce_leg_ignores_the_credit: caught by "#106 reserve: no master Announce reaches the lane without credit"` and `[ ok ] master_announce_reaches_the_lane_after_the_re_election: caught by "#106 race: one master Announce reaches the lane before the re-election"`. Controls 2, failures 0, `RESULT: PASS`, rc 0, 280 s |
| `make lifecycle` | `mutant lifecycle: PASS (normal/repeat, thirteen named defects, ...)`, rc 0, 108 s |
| Docs gates (`doc-gates-head.txt`) | check_doc_style OK (25), check_gptp_docs OK (8 pages), check_submodule_docs OK (6 exact gitlinks), `git diff --check f97e49fe HEAD` clean |
| Images (`images-unchanged.txt`) | `git diff --name-only f97e49fe fc6870ca` lists exactly the six paths above. The 291 png/svg/drawio blobs and gitlinks are identical (0 diff lines). gptp-processor is `1213ac5b`. Pin PNGs: `submodule_boundaries.png` `f5768392…ee66`, `timesync_chain.png` `d209354a…7655`, which match R916-2's hashes. No path in the delta is a synthesis or firmware input |
| Author receipt spot-checks | `gptp_shadow-run.log`: 424/424. The nine campaign slice logs show 13 distinct controls `[ ok ]`, with no failure. Three are caught by other checks than their names, as at f97e49fe (both latency off-by-ones, `credit_never_withheld`). Two slices stopped after their first control, and their second controls completed in later slices. This is disclosed. `plat-ledger`: 24 image digests, 0 diff lines against round 2 |

Static cross-checks of the new arm's credit model:
- `hdl/ieee8021as/gptp_plane/KL_gptp_txticket.sv:259-260`: `tx_credit_o = ~credit_hold_i & (outst_r <= CAP - RSV)`. So credit falls exactly when outstanding > 4. That is the harness's `outstanding() > kCreditMaxOutstanding` (`sim_main.cpp:2840, 2867, 2882`).
- `KL_gptp_txret.sv:700` asserts `outstanding_i == n_led_r + n_res_r`, and `:942-943` packs those counts in `dbg_state_o[7:0]`. So `outstanding()` reads the ticket's count.
- `gptp_shadow_wrap.sv:279-284` overrides neither `TXTS_CAP_N_P` nor `MAND_RSV_C`, so 8 - 4 is the wrapper's value.
- ANNTX's only other gate is asCapable (`mutants.py:69-71`, `ANNTX_GATES`), which the arm checks open at the instant.

**The stated milan_dp gap: I accept the carry.**
- The whole-repo delta is the six paths above. None is named by `tb/verilator/milan_dp`'s sources (`milan-dp-carry.txt`: no reference). `tb/verilator/milan_dp`, `hdl/` and the `gptp-processor` gitlink are byte-identical between f97e49fe and the head.
- The legs' inputs are therefore identical. The round-2 receipts at f97e49fe (`author-r2/receipts/rtl/milan_dp-gptp-f97e49fe.log`, `…-gptp-lat-f97e49fe.log`) read `212 checks: 212 PASS, 0 FAIL` with `[CA]` clockQuality 0xF822436A and 0xF8FE436A. They carry to this head as source-head evidence.
- The six round-3 attempts each ended at rc 124 (for example `milan_dp-gptp-winL.log`: `Terminated`). The author claims none of them as a pass.
- This does not replace the manager's current-dev candidate run.

## Prior public findings at this head

| Item | Disposition |
|---|---|
| **R916-2-F1** (MINOR: Conformance, Robustness, Tests, Docs) | **RESOLVED at its cause.** `sim_main.cpp:2757-2768` counts master Announces at or after `rise` whose last-beat clock `txf_cyc` precedes `fall`. It requires exactly 1, and nothing counts when no fall was recorded. The old `rise + 2 * kSyncTicks` bound is gone. The required verification holds. The pristine run passes, and the delayed-transport observation now fails the named check (423/424). The original #106 fault is still caught by name (author campaign receipt, `first_master_announce_waits_for_a_beat`). The stall is planted as a campaign control and caught by name. My short-stall control shows the check discriminates order, not stall. README row 20 and `SUBMODULES.md:1045-1047` state the same boundary |
| **R915-2-F1** (MINOR: Tests, Robustness) | **RESOLVED at its cause, by the first required option.** The reserve arm (`sim_main.cpp:2851-2909`) withholds credit through the ticket reserve, with the plane unsealed, no barrier, the lane open and asCapable. It runs before the seal arm (`:2786`). `p106-nocredit` fails three named reserve checks at the head. The campaign control `announce_leg_ignores_the_credit` is caught by `#106 reserve: no master Announce reaches the lane without credit`. The seal arm's claim is narrowed to the retry (`:2773-2784`; README row 21; `SUBMODULES.md:1049-1053`) |
| R915-2-R1 (RESIDUE) | Applied exactly: `SUBMODULES.md:984-992` now reads first directive, otherwise all three, best WNS, then the 1x1 instance. The style gate passes |
| R915-2-R2 (RESIDUE) | Applied. The new phases are 19, 20 and 21 at `sim_main.cpp:2368, 2587, 2661, 2773`, README rows 19-21 (`README.md:35-37`) and lines 93-99, `SUBMODULES.md:1039, 1045, 1049`, and in the PR body. `// ---- 18: the PHC trajectory` (`:2258`) is the only phase 18 |
| R915-2-R3 (RESIDUE) | Applied exactly: `CHANGELOG.md:71` "The cadence counts from that Announce (802.1AS-2011 Figure 10-15)." |
| R915-2-S1 | Adopted. README row 19 and the PR state -3,235,644 against +3,517,186, matching my head log (`shadow-run-head.log`, "slewing -100 ppm" and "settled -100 ppm" lines). The donor issue is not filed: carried as S3 below |
| R915-2-S2 | Not taken, with a published reason. The record's sentence is narrowed to "in the deadline's own millisecond". Retained as SUGGESTION S4 |
| R915-2-S3 | Measured locally and projected (PR known limitations). The hosted figure is still pending: manager duty |
| R915-2-S4, S5 | Not addressed; both remain suggestions (S1, S2 below) |
| Round-1 items (R915-1-F1/F2/R1-R3, R916-1-F1/R1) | Resolved at earlier heads. The delta touches none of their artifacts beyond the lines reviewed above |

## Findings at this head

No BLOCKER, MAJOR or MINOR.

### R915-3-R1: RESIDUE. Lens: Docs. "plants four defects" reads as the whole campaign.

- **Where:** `docs/reference/SUBMODULES.md:1057`, "Its campaign plants four defects; each fails by name."
- **Evidence:** the campaign has 13 controls (`mutants.py`; lifecycle "thirteen named defects"). This PR adds four of them.
- **Exact fix:** "Its campaign adds four controls; each fails by name." The style and submodule gates pass with it (`residue-fix-style-check.txt`).

### R915-3-R2: RESIDUE. Lens: Docs. "It also grades" takes the campaign as its antecedent.

- **Where:** `CHANGELOG.md:80`, "It also grades the Announce credit through the ticket reserve."
- **Evidence:** it follows "Its campaign plants both donor defects; each fails by name." (`:79`). The suite grades the credit, not the campaign.
- **Exact fix:** "- `gptp_shadow` also grades the Announce credit through the ticket reserve." The style gate passes.

### R915-3-R3: RESIDUE. Lens: Docs. "its re-election clock" names the Announce's re-election.

- **Where:** `docs/reference/SUBMODULES.md:1047`, "The master Announce's last beat precedes its re-election clock."
- **Evidence:** the re-election is the grandmaster's (the published master bit falls), not the Announce's.
- **Exact fix:** "The master Announce's last beat precedes the re-election clock." The style gate passes.

### Suggestions (do not affect the verdict)

- **R915-3-S1** (`credit_never_withheld`, retained from R915-2-S5). Its expected name "credit: the engine is held off at the reserve" still matches no check. At this head it is caught only by the quiet-start guards of the reserve and seal arms (author receipt `gptp_shadow-mutants-*`). The reserve arm now exercises that exact condition. Renaming the control's expectation to a reserve-arm check, or adding the named check, would make it caught by name. Track it in the separate Issue the PR proposes.
- **R915-3-S2** (`test_mutant_lifecycle.py` `ownership()`, retained from R915-2-S4). It fails under an inherited `make -s`. Pinning `MAKEFLAGS` in the probe environment would make it invocation-independent.
- **R915-3-S3** (donor follow-up from R915-2-S1). Consider a donor issue on scaledLastGmFreqChange after a slewing slave: the opposite sign, -3,235,644 against +3,517,186. The author left filing it to the manager.
- **R915-3-S4** (R915-2-S2, not taken). An arm whose GMID Announce is queued a few hundred clocks before the instant would grade the queued-before-BECOME order too. At this head that order is graded only at millisecond resolution (the Announce is sent 634 clocks after the instant). The author's reason (its own analysis, about 3 s per run) is reasonable; keep it in a follow-up.
- **R915-3-S5** (`sim_main.cpp:2840`). `kCreditMaxOutstanding = 8 - 4` restates the wrapper's defaults. If the wrapper ever overrides `TXTS_CAP_N_P` or `MAND_RSV_C`, the arm silently grades the wrong threshold. Exporting the two parameters through the wrapper, or a bench assertion tying them, would remove the duplicate. A further optional cosmetic change: print "none" rather than "+0" in the race INFO line when no master Announce follows the takeover, which the author already disclosed.

Comment rule: the delta's source comments (`sim_main.cpp`, `mutants.py`, `test_mutant_lifecycle.py`) name no bench lane label, lane, review round, reviewer ID or comment ID. The one hit, `probe.save(...)`, is code. No new RESIDUE of that kind.

## Lens results (each applied at fc6870ca)

- **[R915] PASS Conformance** — `sim_main.cpp:2733-2770` (race), `:2773-2932` (phase 21), `KL_gptp_txticket.sv:259-260`, #994 acceptance 1-3:
  - The race grades 802.1AS-2020 10.6.3 / #106 order against the re-election clock.
  - Credit withholding matches the ticket's credit definition.
  - AC1: 6 exact gitlinks, gptp-processor `1213ac5b`.
  - AC2: gptp_shadow at the head (mine); gptp_plane, phc-step, gptp_tables and gptp_txts from author receipts at the head; milan_dp carried with identical inputs.
  - AC3: no synthesis input changed since the routes.
- **[R915] PASS RTL** — `git diff --name-only f97e49fe fc6870ca` (no RTL or generator path), `KL_gptp_txret.sv:700, 942-943`, `gptp_shadow_wrap.sv:279-284`:
  - The delta changes no RTL.
  - The harness's outstanding-count model and credit threshold match the RTL and the wrapper's parameters.
  - The ANNTX gate anchor in `mutants.py:69-71` matches the generator.
- **[R915] PASS Robustness** — `order-stall`, `order-stall-short` and `p106-nocredit` logs, and `sim_main.cpp:2851-2909`:
  - The lane stalled across the race is caught; a stall after the Announce is not misreported.
  - A credit-less Announce leg is caught where no fence backs it.
  - The reserve arm checks unsealed, no barrier, asCapable, release and drain, and its hold is disarmed before release.
  - The seal arm's start guard still runs after it (424/424).
- **[R915] PASS Tests** — the four `shadow-run-*.log`, `campaign-new2.log`, `shadow-lifecycle.log`, and the author's `gptp_shadow-mutants-*.log`:
  - Each new check fails for the defect it names: my probes, and the two new campaign controls caught by name.
  - The head is green at 424 checks.
  - The lifecycle counts 13.
  - Check-count reconciliation: 408 plus 13 reserve-arm checks plus 3 quiet-start checks gives 424, the head tally.
- **[R915] PASS Docs** (R1-R3 are residue only) — `CHANGELOG.md:65-86`, `SUBMODULES.md:980-1062`, `gptp_shadow/README.md:35-37, 88-99, 147`, and the PR body against `PR-BODY.md` and my executions:
  - Docs gates pass.
  - The README row 19 figures match my head log.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Race and phase-21 checks against #106 and the ticket credit definition; #994 AC1-3 with gitlinks, consumer receipts and the milan_dp carry | R915-3 | `fc6870cab13f74149864b80b6480ddb3641cb936` |
| RTL | CLEAN | Delta path list (no RTL); `KL_gptp_txticket.sv:259-260`, `KL_gptp_txret.sv:700, 942-943`, `gptp_shadow_wrap.sv:279-284` against the harness model; ANNTX anchor | R915-3 | `fc6870cab13f74149864b80b6480ddb3641cb936` |
| Robustness | CLEAN | Lane stall across the race, post-Announce stall control, credit-less leg under the reserve, reserve arm's release/drain and arm ordering | R915-3 | `fc6870cab13f74149864b80b6480ddb3641cb936` |
| Tests | CLEAN | 424-check head run; three probes; two new controls through `mutants.py main()`; lifecycle; author campaign receipts; check-count reconciliation | R915-3 | `fc6870cab13f74149864b80b6480ddb3641cb936` |
| Docs | CLEAN (R1-R3 residue) | CHANGELOG, SUBMODULES #994 record, gptp_shadow README, PR body; docs gates; residue fixes style-checked | R915-3 | `fc6870cab13f74149864b80b6480ddb3641cb936` |

Product RTL and synthesis inputs are unchanged since f97e49fe, and since the routed commit for synthesis. The RTL lens's earlier product coverage therefore carries, and this round re-applied it to the delta's dependencies.

## Real limits

- No manager source bank ran at this head, and I claim none. Source-head consumer evidence beyond gptp_shadow is the author's published receipts, which I spot-checked rather than re-ran: gptp_plane, phc-step, gptp_tables and gptp_txts.
- milan_dp gptp/gptp-lat did not complete at this head. The carry from f97e49fe rests on byte-identical inputs, not on an execution at fc6870ca.
- I did not run the full gptp_shadow campaign (13 controls) myself, only the two new controls. The other eleven rest on the author's slice receipts, and the campaign's inputs for them are unchanged apart from the harness delta.
- Hosted checks at the head, read at 17:21 UTC: `bdd-conformance`, `changes` and `full-ci-gate` were success. `Physical gPTP (nightly and manual)` was skipped. 3 were in progress and 41 queued, including every Verilator shard, Yosys and the docs gates (`hosted-checks-head.txt`). A skipped context is not executed evidence.
- Physical calibration NOT RUN, and field skips are not hardware proof.
- The packet archive carries content hashes but no cryptographic signature.
- The lifecycle test uses its own temporary directory, which it reported removed (`scratch_removed: true`).

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `300da99b`, live dev `e275d795`), with builder and native banks, including milan_dp gptp/gptp-lat. Link the receipts on the PR.
- Own hosted and act acceptance at the exact head: exact-head `verilator-suites` and `yosys-portability` once they complete.
- Measure gptp_shadow's hosted figure at this head. The author projects 840 to 950 s against `scripts/suite_shards.py`'s 393 s.
- Carry R915-3-R1 to R3 to the residue checklist.
- Consider filing the donor scaledLastGmFreqChange issue (S3) and the `credit_never_withheld` naming issue (S1).
- Merge still needs the second independent positive review and the full completion bar, with explicit maintainer authorization.

R915-3 FINISHED
