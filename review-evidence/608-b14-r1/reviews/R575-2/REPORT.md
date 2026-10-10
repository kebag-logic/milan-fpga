[R575] NEGATIVE - exact head d981b1cc574f757a1d04d1b21d34a078ad85be3d

# R575-2: external independent review of PR #709 (issue #608, lane B14), round 2

Head `d981b1cc574f757a1d04d1b21d34a078ad85be3d`, tree `e0002fa45fb94b21147abc73704b732dd0f7bd69`, base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Delta reviewed: `6ec1a3a9..d981b1cc`, one one-line commit that changes only `docs/findings/B14_BENCH_5603C353.md` (+121/-49).
Evidence: the archived packet `review-evidence/608-b14-r1/` at archive commit `c848925d2e88a98e7f31b663e5dd4f342b765487`.

The delta answers every round-1 finding, and every corrected figure I checked against the packet matches it. Two MINOR findings remain open:
- the rewritten FRAMES observation misstates the repository's declared FRAMES_RX contract (F1);
- the page cites round-2 recompute records that no public archive holds (F2).

One RESIDUE is carried.

## Reconstruction

I read the following, in this order:
1. AGENTS.md, CONTRIBUTING.md (sections 2 and 6), docs/README.md.
2. Issue #608: the body, the B14 assignment (6085135051), the SoC-board ruling (6094000332), the round-2 assignment (6096040548) and the round-2 REVIEW READY (6096216680).
3. The PR #709 body.
4. The delta and its history.
5. The archived packet.

The authorities I used:
- Milan v1.2 Tables 5.4 and 5.6, read from the standard.
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`, `hdl/milan/milan_datapath.sv`.
- `tests/features/counters_contract_milan.feature`.
- `docs/reference/REGISTER_MAP.md` section 0x200.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` "Settle recentre".
- The two #658 ruling comments.

Ordering: my independent pass and its two candidate findings were written to `receipts/independent-pass-before-prior-findings.txt` before I read the round-1 findings (R574-1 and R575-1).

No source edit, commit, push, GitHub write, bench, Docker or act action was made. Execution was limited to:
- the read-only documentation gates at the exact head;
- the recompute scripts in `scripts/`, run over the archive extracted under `scratch/`.

## Findings

### R575-2-F1 MINOR: the FRAMES observation misstates the repository's declared FRAMES_RX contract

- **Lenses:** Conformance, RTL, Docs.
- **Where:** `docs/findings/B14_BENCH_5603C353.md:475-480`. The PR body's first "Observations for triage" bullet repeats the claim.
- **What the page says:**
  - The once-per-second FRAMES_TX (both talkers) and CRF-listener FRAMES_RX match "the contracts the repository declares (`KL_talker_diag_ctx.sv`, `KL_avtp_rx_monitor_ctx.sv`, `counters_contract_milan.feature`)".
  - For the AAF listener's 57,599,387 it says "Table 5.6 and the declared STREAM_INPUT contract allow at most one per interval, so this needs triage".
- **Authority and evidence** (`receipts/frames-contract-excerpts.txt`, `receipts/soak-records.txt`):
  - **The engine the page cites declares and implements the per-frame law.** The AAF listener's FRAMES_RX is served from `KL_avtp_rx_monitor_ctx` (`milan_datapath.sv:3518`). At this head that file:
    - declares the "USER 2026-08-05 FRAMES_RX law: count FRAMES, publish COALESCED at the interval commit - the visible counter advances by the interval's frame total (~8000/s at class A) instead of Table 5.6's +1-per-interval. Both readings are Milan-legal" (`:318-323`);
    - implements it, with "FRAMES_RX commits the interval's FRAME TOTAL (coalesced law, USER 2026-08-05)" (`:627-630`, accumulator `:1150-1164`; commit `f611af391`).
    - Only the file's header, `:28-36`, says "at most one". The file contradicts itself, and the page quotes the stale half.
  - **The cited feature classifies a per-frame rate as consistent, not deviant.** `counters_contract_milan.feature:250-277` says the clause bounds the interval only from above, so "every interval in (0, 1 s] is conformant". It lists 7995.7/s as consistent with the per-frame reading. `:408` grades `FRAMES_RX 240060 over 30` as INFO (per-frame), not FAIL.
  - **The silicon matches the coalesced law.** Over the soak, the DUT's STREAM_INPUT 0 shows FRAMES_RX +57,599,387 against TIMESTAMP_VALID +57,599,252. That is the TV == FRAMES_RX identity the law says it restores.
  - **The CRF listener runs a different engine.** Its once-per-second FRAMES_RX is `KL_crf_rx.sv` (`pdu_count_o`, "intervals with >= 1 accepted PDU", `:233`; `milan_datapath.sv:3701`), not the cited `KL_avtp_rx_monitor_ctx.sv`.
- **Impact:**
  - The page states, as a contract fact, that the AAF listener departs from the repository's declared STREAM_INPUT contract. In fact it implements a deliberately declared law.
  - It omits the real triage facts: the two listener engines implement different FRAMES_RX readings, and the ctx engine's banner contradicts its own law.
  - Triage under this observation would start from a false premise. This is a clause and contract claim, not wording.
- **Required outcome:** the observation, and the PR body, state the contracts as they are at the head:
  - the AAF listener's per-PDU FRAMES_RX is the coalesced frame-total law declared and implemented in `KL_avtp_rx_monitor_ctx.sv:318-323` and `:627-630`, and the file's header `:28-36` says otherwise;
  - the CRF listener's once-per-second count is `KL_crf_rx.sv`'s interval reading;
  - the repository's counters contract treats a per-frame rate as consistent with Table 5.6 (INFO).

  The triage question can stay. It must not assert a contract departure the cited contract does not make.
- **Verification:** re-read the page's lines 475-480 and the PR body against the excerpts in `receipts/frames-contract-excerpts.txt`.

### R575-2-F2 MINOR: the round-2 recompute records are cited but not in any public archive

- **Lenses:** Docs, Tests.
- **Where:** `docs/findings/B14_BENCH_5603C353.md:682-689` ("Round 2 recomputes").
- **What the page says:** "The scripts and their outputs are in the lane's round 2 handoff packet under `round2/`."
- **Authority and evidence:**
  - The page states that its record paths are relative to `review-evidence/608-b14-r1/author/` at `c848925d` (`:643-644`). That tree has no `round2/` directory.
  - The evidence branch tip `da42cd96` adds only the two round-1 review archives.
  - The author's round-2 REVIEW READY says these recomputes "are not yet archived".
  - The round-2 assignment, item 6, requires "the archive commit and the path of each cited record". Its preamble requires every statement to be backed by a record in the packet, or weakened or removed.
- **What rests only on those records:**
  - the claim that the raw re-decode of all 101 item-3 captures agrees with `cycles.tsv` within 0.5 us. The archived `msrp.tsv` and `acmp.tsv` do reproduce the 0.0390, 0.0951 and 0.3184 s figures (`receipts/item3-withdrawals.txt`);
  - the 44-row category recount (2 descriptor counts and 18 formats);
  - the final-read value of the 7 as-found format rows. `restore/` covers the other 8 of the 15 rows (`receipts/restore-rows.txt`).
- **Impact:** a cold reviewer cannot open or re-run the round's own checks, and the citation cannot be resolved. The R574-1-F6 requirement holds for the archived packet but not for these new citations.
- **Required outcome:** one of the following:
  - the `round2/` scripts and outputs are archived, and the page names their archive path and commit; or
  - the paragraph is limited to what the archived records and the hash-indexed raw files show, and the reference to the unarchived handoff packet is removed.
- **Verification:** the cited `round2/` paths resolve at a named public commit, or the paragraph cites only `c848925d` records.

### RESIDUE (wording only)

- **R575-2-R1**, `docs/findings/B14_BENCH_5603C353.md:510`. The register map does not say the lane "reads" "not supported". It says a UI must render a structurally silent lane that way (`REGISTER_MAP.md:482-484`); the register itself reads 0.
  - Replace "and the register map says such a lane reads "not supported", never "0 errors"" with "and the register map says software must render such a lane "not supported", never "0 errors"".
  - The lane facts (bit 6 = 0, no source) are correct.

## Prior findings at this head

| Finding | Status at `d981b1cc` | Evidence |
|---|---|---|
| R575-1-F1 = R574-1-F2 (withdrawal reference) | RESOLVED. `:191` gives 0.095 and 0.318 s after the bridge's `Lv` and 0.104 and 0.328 s after the response. Pilot 0.039 s. No other cycle holds a DUT Talker Advertise `Lv` | `receipts/item3-withdrawals.txt` |
| R575-1-F2 = R574-1-F3 (loss bursts) | RESOLVED. Captures 002 and 042 lost on four streams, 035 on three (DUT CRF `0001` untouched). AAF 9 to 12, CRF 1 | `receipts/soak-records.txt` |
| R575-1-F3 = R574-1-F5 (`SLIP_LB`) | RESOLVED. The soak-bind step `0x8e` (06:22:39.06) to `0x90` (06:23:23.21) and its bracket are exact. The phase ledger sums to 146 dups / 73 frames, and every listed phase value reproduces, including 0 in all 20 within-cycle gaps. The cause claim is limited to the documented arm terms | `receipts/slip-lb-ledger.txt`, `receipts/item2-phase-times.txt`, `MEDIA_CLOCK_FOLLOWING.md:1090` |
| R575-1-F4 (receive-drop lane) | RESOLVED. `STATS_CAP` `0x1B8`: lanes 3, 4, 5, 7 and 8 are real; lane 6 (`0x228`) has no source. All 27 console reads agree. Wording carried as R575-2-R1 | `receipts/soak-records.txt`, `REGISTER_MAP.md:497-533` |
| R574-1-F1 (FRAMES vs Tables 5.4/5.6) | Clause part RESOLVED: Tables 5.4 and 5.6 are now cited as observation-interval counters of at most 1 s, which matches the standard's text. The contract statement added under its required outcome is superseded by R575-2-F1 | `receipts/frames-contract-excerpts.txt` |
| R574-1-F4 (restore basis) | RESOLVED for the archived basis: the 15 as-found rows are equal at teardown, and 8 of the 15 are equal at the final read in `restore/`; 44 of 44 equal the 06:22 inventory per `restore-compare.txt`. The saved state is marked not read back, with 38 commits, sequence 234 to 272, 54 records and 3,336 B. The final value of the 7 format rows rests on unarchived records (R575-2-F2) | `receipts/restore-rows.txt`, `receipts/nvm-lines.txt` |
| R574-1-F6 (packet identity) | RESOLVED for the archived packet. All three digests, 2,356 manifest entries, 422 redactions, the four raw-index digests, the capture counts and bytes, and the soak index's pre-redaction digest all match. The 16 `MANIFEST.sha256` mismatches are exactly the redacted files' pre-redaction digests. The new `round2/` citation is R575-2-F2 | `receipts/evidence-identity.txt` |
| R575-1-R1 to R6, R574-1-R1 to R3 | Applied (`:35`, `:150`, `:173`, `:189`, `:41`, `:90`, `:431`, `:463`) | page |
| R574-1-S2 | Applied. `:438` matches ruling 5988293154 item 1 and 5988843004 items 1 and 3 | the #658 comments |
| R574-1-S1 = R575-1-S1 (findings index) | Open SUGGESTION; left to the manager | - |

## Assignment checks

- **Withdrawal times:** correct against the right reference. All 101 recomputed bridge-`Lv`-after-response values equal `cycles.tsv`. Graded minimum 8.350, maximum 95.701, median 8.880 ms. The late cycles are 26, 56 and 97 (84.466, 95.701 and 57.499 ms).
- **Soak bursts:** correct per stream.
- **SLIP_LB record:** complete, including the soak-bind slip and the movement behind `0x92`.
- **FRAMES vs Tables 5.4/5.6:**
  - The clause text is correct.
  - The repository-contract statement is wrong (F1).
- **Restore:** narrowed. The saved-state content is marked not read back, and the basis is stated. Part of it rests on unarchived records (F2).
- **Evidence-packet identification:** correct for `c848925d`. The `round2/` citation does not resolve (F2).
- **Receive-drop lane:** correct. The register-contract wording is carried as a RESIDUE.
- **No new measurement campaign:**
  - Every delta figure I checked derives from `c848925d` records, or from raw files indexed there before round 2. No timestamp in the delta is later than 08:23:49.
  - The author states that no bench action and no read-only read was made.
  - Absence of a bench action cannot be proven from public state.
- **Privacy:**
  - `docs_check.py` reports 0 findings at the head.
  - The added lines carry no host, IP, local path, interface or instrument name. The only MAC-form strings on the page are unchanged MAAP multicast range addresses.
  - The controller application name appears only inside a packet record path; merged findings pages name it the same way.

## Lens results (exact head `d981b1cc`)

```text
[R575] MINOR Conformance - docs/findings/B14_BENCH_5603C353.md:475-480 - see R575-2-F1
[R575] MINOR RTL - docs/findings/B14_BENCH_5603C353.md:475-480 vs hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:318-323,627-630 - see R575-2-F1
[R575] PASS Robustness - B14_BENCH_5603C353.md:465-468,486-497,577-595 - bind-outside-transient bracket edges, per-stream burst loss and recovery, ledger completeness incl. 20 within-cycle, 5 between-cycle and 4 between-run intervals, checked against author/item2/summary/switches.json, the 0x8D4 console reads and soak/soak-overlap-recovery.txt (receipts/slip-lb-ledger.txt, soak-records.txt)
[R575] MINOR Tests - B14_BENCH_5603C353.md:682-689 - see R575-2-F2
[R575] MINOR Docs - B14_BENCH_5603C353.md:475-480,682-689 - see R575-2-F1, R575-2-F2; gates rc 0 at head (receipts/gates-rc.txt)
```

The Conformance and RTL lenses applied the following clean, beyond F1:
- the Tables 5.4/5.6 text;
- the RMON lane map;
- the settle-recentre arm terms;
- the 15-row change coverage: no `format-check` in the packet set a format (5 of 5 `set: null`).

The Tests lens re-ran every corrected figure from the archive. Each script reports a mismatch if a published value diverges from the record.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R575-2-F1) | page `:475-480`, Milan v1.2 Tables 5.4 and 5.6, `REGISTER_MAP.md` 0x200, the #658 rulings, PR body | R575-2 | `d981b1cc574f757a1d04d1b21d34a078ad85be3d` |
| RTL | UNCLEAN (R575-2-F1) | `KL_avtp_rx_monitor_ctx.sv:28-36,318-323,627-630,1150-1164`, `KL_crf_rx.sv:233`, `milan_datapath.sv:3518,3701`, `MEDIA_CLOCK_FOLLOWING.md:1090` | R575-2 | `d981b1cc574f757a1d04d1b21d34a078ad85be3d` |
| Robustness | CLEAN | page `:465-468,486-497,577-595`; `switches.json`, the console `0x8D4` reads, `soak-overlap-recovery.txt`, `bind-a-*.jsonl` | R575-2 | `d981b1cc574f757a1d04d1b21d34a078ad85be3d` |
| Tests | UNCLEAN (R575-2-F2) | page `:643-689`; `scripts/*.py` over `c848925d`; all receipts | R575-2 | `d981b1cc574f757a1d04d1b21d34a078ad85be3d` |
| Docs | UNCLEAN (R575-2-F1, R575-2-F2; R575-2-R1 residue) | the whole page at the head, the delta, the PR body, the documentation gates | R575-2 | `d981b1cc574f757a1d04d1b21d34a078ad85be3d` |

## Real limits

- Raw captures and raw snapshots are not public, so I could not re-decode them. Raw-based claims were checked only for consistency with the archived derived records.
- No simulation of the FRAMES_RX law was run. F1 rests on:
  - the RTL text and wiring at the head;
  - the counters feature;
  - the silicon TIMESTAMP_VALID/FRAMES_RX equality in `soak/summary.json`.
- Whether the coalesced law conforms to Table 5.6 is not ruled here. F1 concerns only the page's statement of the declared contract.
- Bench actions during round 2 cannot be excluded from public state.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- No manager source bank was run or inferred at this head.

## Hosted evidence at the exact head (observed, not accepted)

From `receipts/hosted-check-runs.tsv`:
- Executed with success: `rtl-fast`, `elaborate`, `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `wire-accountability`.
- In progress when read: `docs-check`.
- Skipped, not executed: `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit`, `Physical gPTP`.

The manager owns hosted and act acceptance.

## Pending manager duties

- R575-2-F1 and R575-2-F2: a corrected head, then re-review. Alternatively for F2, a ruling plus an archive of `round2/`.
- Carry R575-2-R1 to the residue checklist.
- R574-1-S1 = R575-1-S1, the findings index entry.
- Exact-head hosted `docs-check` completion.
- Current-dev merge-candidate validation (source base `5603c353`, live dev `e8454e27`) at the merge turn.

## Clone state after the review

From `receipts/clone-state.txt`:
- HEAD `d981b1cc`, tree `e0002fa4`.
- Worktree and index equal HEAD, and the porcelain status is empty.
- The page's blob is `0b6b4a7b` in the tree, the index and the worktree, mode 100644.
- The five gitlinks are unchanged: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `2ad2f845`, third_party/lwSRP `9197193e`, third_party/verilog-axis `48ff7a7e`.
- No probe edited the clone.

## Publishable files

`REPORT.md` and every file listed in `MANIFEST.sha256`. To rerun: `scripts/run_all.sh <review-evidence/608-b14-r1 extracted from c848925d> <out dir>`.

R575-2 FINISHED
