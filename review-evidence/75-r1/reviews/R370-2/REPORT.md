[R370] NEGATIVE - exact head 5c7577e51702b00683a121f97a9806c167eb072b

Round R370-2, internal independent review of PR #604 (Refs #75, phase 2). Tree `e817bda49b6ed644a94c39f07b72762411c0b8dc`, source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. The review covers the round-2 delta `0e8ec0d2..5c7577e5` and re-reads the whole page at the head.

Open findings: 1 MINOR (R370-2-F1), plus 2 SUGGESTIONs. All three round-1 findings of this reviewer (BLOCKER, MAJOR, MINOR) and all four round-1 suggestions are resolved at this head. The verdict is NEGATIVE only because R370-2-F1 is open. It is a factual error in the round-2 text on the DUT-side difference, and the addendum check that backs that text cannot detect the error.

## Reconstruction

- Read in order: AGENTS.md, CONTRIBUTING.md (required contexts at :56-57), docs/README.md, and the #75 body with its three acceptance criteria and the "How we prove it" 100-cycle line.
- #75 comments: phase-2 assignment 5859652809, round-2 decision 5860261220, and [A389] TAKEN / REVIEW READY 5860271442 / 5860418078. Also #606 (open) and the PR #604 body and manager notices.
- Diff `8bc97021..5c7577e5`: two documentation files only (`docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` added, `docs/findings/README.md` +1 row). Two one-line commits, no trailers.
- Public evidence: operator packet `review-evidence/75-r1/author` (pinned `a19f2c92`) and the round-2 addendum `review-evidence/75-r1/author-r2` (evidence branch tip `8791bfa4`). Its MANIFEST.sha256 verifies 32/32.
- Prior review findings were read only after the independent pass below.

## Answers to the round-2 focus

1. **No page link points into a submodule; docs-check passes with and without submodules.**
   - The page's links are the 12 targets in `receipts/link-targets.txt`. The SRP citation (page:64) is now pinned upstream at `870ff88a`. That equals the protocol-processor gitlink at head, and the linked blob `23c5bd4b` equals the local blob. The history links resolve at `eb375c13`.
   - `docs_check.py` returns rc 0 in three trees at the exact head: this clone with submodules (`receipts/gates-full.txt`), a clone with no submodule contents (`receipts/gates-no-submodules.txt`), and a `git archive` tree without Git metadata (`receipts/gates-no-git.txt`).
   - Counterfactual: planting the round-1 relative submodule link in the no-submodule tree makes `docs_check.py` return rc 1, "broken link" at page:64 (`receipts/docs-check-planted-submodule-link.txt`).
   - All nine assigned gates return rc 0 at head. That includes `check_em_dash.py --base 8bc97021` over 1181 added lines, plus `git diff --check` for base..head and for the worktree.
2. **Every sub-PDU-period interval has a recorded stop check. Reclassification, quantiles and counters reconcile.** My own probe (`scripts/stop_check_probe.py`, `receipts/stop-check-probe.txt`, rc 0) derives restart status from the published per-attempt window counts. It does not use the author's label.
   - The window arithmetic holds on all 200 rows: settle equals response + 0.5 s, hold ≥ 2 s (minimum 2.000212 s), settled count = pre-command + command-to-response, and latency matches the anchors.
   - The independent predicate requires zero PDUs from settle to response, a zero final-half-second count, and a first post-settle PDU at or after the response that is the first post-response PDU. It agrees with the published classification on 200/200 rows.
   - The only non-restarts are talker 13, 24 and 75. They are exactly the three sub-period intervals (0.000364, 0.000297, 0.001864 s). Each has 1000 hold PDUs, 250 final-half PDUs and a maximum gap of 0.002000053 s.
   - Every accepted restart shows more than 1.93 s of recorded silence spanning the settled hold. None is below one PDU period.
   - Counters: the active talker's start/stop delta is 1/1 for every restart and 0/0 for every non-restart. Sums are listener 100/100 and talker 97/97. The public setup and restore snapshots read 18/17 → 115/114 (talker) and 12/11 → 112/111 (listener). The inactive DUT output reads 0/0 throughout the listener series.
   - The public records for cycles 1-5 in both directions match the addendum rows on timings, counters, continuity and input hashes. `input-hashes.csv` lists 1000 source records.
   - Recomputed distributions match the page and the summary: listener 100, 0.006641 / 0.110280 / 0.188503 / 0.204859; talker 97, 0.017427 / 0.019175 / 0.042347 / 0.117736. The stated effect (minimum, median and p95 change, maximum unchanged) is correct.
   - The OLS slopes and 95 % intervals match the page to 9 decimals when the t quantile is computed exactly (df 98 and 95). So do the first/last-ten medians and every ten-cycle block median and maximum.
   - The addendum's `assert_stop`, `distribution()` and `fit()` reproduce the summary. `assert_stop` rejects one settled PDU, continuous traffic and early resumption (`receipts/addendum-function-probe.txt`). Its series-expanded t agrees with the exact t to 2e-8.
   - Mutation check (`scripts/mutate_probe.py`, `receipts/mutation-probe.txt`): the probe kills 10/10 planted defects, including a silent-hold relabel, one settled PDU, a counter 0/0, a 1.9 s hold, a median reverted to round 1, a stop-table flip and a +1e-9 interval edit.
3. **Acceptance scope, #606 exception, DUT-side difference.**
   - The acceptance table (page:873-879) scopes criteria 1 and 2 to the two CRF pairs and the `DISCONNECT_RX` / two-second hold / `CONNECT_RX` sequence. It reports talker 97/100 as NOT MET.
   - It lists the 6.889398 s initial bind as an open exception linked to #606, with the rationale "no preceding disconnect/hold" (also page:189-194).
   - The page records that no DUT Talker Advertise precedes the bind (first declaration at +0.079 s), that declarations repeat each second, and that the bridge is silent until its LeaveAll at +6.080 s. It does not attribute the wait only to the peer (page:222-225). I verified these values against the public `talker-setup/msrp.tsv`.
   - **However**, the contrasting sentence at page:219 is false for talker cycle 1 (R370-2-F1).
4. **Index, slope intervals, resolution and predicate, restore difference, Refs #75.**
   - The index row is present (`docs/findings/README.md:11`). Slope intervals are at page:234-250.
   - Resolution: 1 ns timestamp word, 2 ms PDU observation grid, half-wrap limit, maximum unwrap spread 0.106533 s (reproduced). The full validity predicate is at page:99-119. I checked it against CRF header offsets: sv/version mask, type 1, 48 kHz with pull 0, data length 8 with interval 96, VLAN (3, 2), source and destination. `mr`, `fs` and `tu` are recorded as zero on every row.
   - The restore difference (Stream Output 1 destination) is at page:851-855.
   - The PR body and page say "Refs #75", and no closing keyword appears. #75 and #606 are open.
   - **Hygiene of the round-2 addendum.** The scan (`receipts/hygiene-scan.txt`) found no absolute paths, bench host names, instrument, peer or switch names, lane-root variable, command-wrapper name, user names, tool or model names, or e-mail addresses in the 34 addendum files, the page, the index row, the PR body or the commit messages. It has one hit, the upstream repository owner in the pinned SRP URL. That URL is the canonical `.gitmodules` origin that the round-2 decision asked for. The round-1 wrapper and lane-root names do not appear in the addendum tools.

## Findings

[R370] MINOR Conformance, Tests, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:219-220; review-evidence/75-r1/author-r2/verify_disclosures.py:29-31,48; author-r2/disclosures.json; author-r2/HANDOFF.md:26 - "Numbered reconnects instead retain DUT Talker Advertise through the hold" is false for talker cycle 1, and the check behind it cannot fail
ID: R370-2-F1
Requirement/evidence:
- The round-2 decision (#75 comment 5860261220, item 3) requires the page to record the DUT-side difference between the initial bind and the reconnects. Page:219-220 states that numbered reconnects retain DUT Talker Advertise through the hold, "The initial bind therefore differs in DUT-side state too."
- The public record `talker-001/msrp.tsv` shows otherwise (`scripts/hold_declaration_probe.py`, `receipts/hold-declaration-probe.txt`):
  - The bridge withdraws Listener at +0.010 s after the disconnect response. The DUT then sends Talker Advertise **Lv** at +0.121 s, and only **Mt** at +0.521 s and +1.721 s.
  - This leaves zero DUT Talker Advertise declarations (New/JoinIn/JoinMt) in the hold. In, Mt and Lv carry no declaration (802.1Q applicant events, Table 10-3).
  - The DUT's first declaration comes 0.111 s after the response. That is later than the initial bind's 0.079 s. The restart is 0.117736 s, the talker maximum.
  - Cycles 2-5 each carry 2-4 JoinMt in the hold.
- The page's own attribution table agrees with the record: DUT talker Talker Advertise Lv = 1 (page:335). The restore capture's Lv is outside that table, so the one Lv is cycle 1's.
- The addendum check behind the claim counts `In` and `Mt` as advertising (verify_disclosures.py:30). It publishes the literal `numbered_talker_holds_with_dut_advertise=100` (:48). It reports cycle 1 as advertising, so it cannot fail for the defect it is meant to rule out.
Impact:
- The recorded contrast is wrong in the one reconnect that reproduces the initial bind's DUT state: no Talker Advertise declared when the response crosses. That reconnect still restarted in 0.118 s.
- Cycle 1 therefore bears directly on #606's attribution. It weakens "therefore differs in DUT-side state". It is evidence that the missing declaration alone does not produce a 6.9 s wait: the bridge answered Ready 6 ms after the DUT declared (+2.127 s against +2.121 s). A reader of the page, or #606, is pointed the wrong way.
Required change:
- The page must state the exception accurately: talker cycle 1 withdrew and did not declare Talker Advertise through the hold, then restarted in 0.117736 s.
- The count of holds that carry a DUT declaration must be re-derived from declaration events only (New/JoinIn/JoinMt) over the retained talker `msrp.tsv` files and published.
- The "therefore" inference must be qualified or removed to match.
- The backing check must use declaration events and derive its count from the data, not a literal, in a new addendum item. The round-1 and round-2 packets stay unchanged.
Verification:
- `scripts/hold_declaration_probe.py` on the public cycles reports cycle 1 as 0 declarations, and the page agrees.
- The corrected check reports a derived count and fails when run on cycle 1 with the old claim.
- Page:211-225 is re-read against `talker-001/msrp.tsv` and `talker-setup/msrp.tsv`.

### Suggestions (do not affect lens coverage)

[R370] SUGGESTION Robustness, Docs - docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:574-586 - Characterise the three non-restarts against the recorded Listener withdrawal
ID: R370-2-S1
- The page correctly reclassifies talker 13, 24 and 75 and leaves the cause open under #75.
- Across the 97 talker restarts, the DUT's last PDU falls a median of 0.0091 s after the disconnect response (range 0.0076-0.0988 s). In the public cycles the bridge's Listener Lv arrives at +0.010 s.
- The attribution table counts 100 bridge Listener Lv events over the 100 numbered talker captures (page:341). The restore capture is excluded, as R370-2-F1 shows. That suggests the withdrawal also reached the DUT in the three non-restarts.
- If the retained `msrp.tsv` confirms it, the DUT kept transmitting for more than 2 s after a withdrawal it otherwise honours within about 10 ms. That is a stop-path behaviour distinct from #75's restart-latency subject.
- Publishing the per-cycle Lv timing for these three cycles would settle which side holds the stream. Under AGENTS.md section 4 the manager may prefer a separate owner issue.

[R370] SUGGESTION Tests - review-evidence/75-r1/author-r2/recompute.py:216,247-248 - Derive the printed outcome instead of pinning it
ID: R370-2-S2
- Classification at :170-174 is data-derived, and the pin at :216 fails loudly, so this is not a defect.
- The summary lines :247-248 print literal counts (197 PASS; 13, 24, 75) rather than the computed sets. A future rerun with different data would abort at :216 rather than report its own counts.

## Clean-lens evidence

[R370] PASS RTL - `git diff --name-status 8bc97021..5c7577e5` (two docs files); gitlinks identical at base and head (`receipts/rtl-scope.txt`); docs/reference/REGISTER_MAP.md:1069,1180,1236,2242; protocol-processor/docs/architecture/10_srp_engine.md:423 at `870ff88a`; `hdl/ieee8021q/srp/KL_lwsrp_ctx.sv` absent at head and present at `eb375c13` (`receipts/rtl-claims.txt`)
- No RTL, constraint or interface file changes.
- The page's architecture claims hold at this head: the retired lwSRP context is absent, the SRP design documents the LeaveAll deviation, 0x650, 0x69C and 0x6B0 are structural zeros, and 0x930 is `PP_DIAG`.
- The only round-2 change in this scope is the pinned link, which points to the same blob.

[R370] PASS Robustness - author-r2/recompute.py:27-50 (truncation, timestamp reversal, unwrap ambiguity), :108-113 (capture errors, drops, raw hash), :143 (invalid target CRF aborts), :153 (hold ≥ 2 s), :162-192 (settled window, early-resumption censoring, gap bound), :184 (wire/counter agreement); author-r2/stop-checks.csv (200 rows); page:138-167
- My probe confirms the following at head: every accepted restart has more than 1.93 s of silence over the settled hold, no restart precedes its response, and non-restarts are rejected before any distribution.
- The minimum hold is 2.000212 s and no interval reaches 1 s.
- Continuous traffic cannot pass as a zero-time restart. The mutation "talker 24 relabelled RESTART" is killed.
- R370-2-S1 is optional characterisation and does not reopen this lens.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R370-2-F1 MINOR) | #75 body and criteria; decisions 5859652809 and 5860261220; #606; page:1-225, 558-586, 831-881; `talker-setup/msrp.tsv`, `talker-001..005/msrp.tsv`; CRF offsets in recompute.py:137-145 | R370-2 | 5c7577e51702b00683a121f97a9806c167eb072b |
| RTL | CLEAN | diff name-status; gitlinks base and head; REGISTER_MAP.md:1069,1180,1236,2242; 10_srp_engine.md:423 at 870ff88a; history eb375c13 | R370-2 | 5c7577e51702b00683a121f97a9806c167eb072b |
| Robustness | CLEAN | recompute.py:27-50,108-113,143,153,162-192; stop-checks.csv 200 rows; page:138-167; `receipts/stop-check-probe.txt`, `receipts/mutation-probe.txt` | R370-2 | 5c7577e51702b00683a121f97a9806c167eb072b |
| Tests | UNCLEAN (R370-2-F1 MINOR) | nine gates plus no-submodule and no-Git docs gates; planted-link counterfactual; recompute.py functions; verify_disclosures.py:29-31,48; my probes and 10/10 mutants | R370-2 | 5c7577e51702b00683a121f97a9806c167eb072b |
| Docs | UNCLEAN (R370-2-F1 MINOR) | whole page (1-1180) with links, tables and hygiene; README.md:11; PR body; commit messages; addendum README, HANDOFF.md:26 and disclosures.json | R370-2 | 5c7577e51702b00683a121f97a9806c167eb072b |

## Resolution of prior public findings on this PR

This section was written after the verdict and ledger above.

| Prior finding | Status at 5c7577e5 | Evidence |
|---|---|---|
| R370-1-F1 BLOCKER, submodule link breaks hosted docs contexts | RESOLVED | Focus 1. Exact-head hosted `docs-check-no-git` is `success` (`receipts/hosted-check-runs.txt`). Hosted `docs-check` was still in progress at 22:41Z. |
| R370-1-F2 MAJOR, three talker "restarts" not shown, counters 97/100 | RESOLVED | Focus 2. The #75 open, public owner holds the non-restarts and the missing three cycles (page:584, 878). The method states the silence precondition, the tap anchor and early-resumption handling (page:90-97, 138-153). |
| R370-1-F3 MINOR, acceptance omits the 6.889 s bind, no owner | RESOLVED | Focus 3 and #606. The accuracy defect in the new contrast sentence is a separate new finding (R370-2-F1). |
| R370-1-S1 slope intervals | TAKEN | page:234-250 |
| R370-1-S2 resolution and predicate | TAKEN | page:99-136. The author is right that the `0xf0` mask does not test `mr` (bit 3). My round-1 wording "validity also requires mr = 0" was wrong. The page now records `mr`, `fs` and `tu` as zero by replay. |
| R370-1-S3 index row | TAKEN | README.md:11 |
| R370-1-S4 restore difference | TAKEN | page:851-855 |

I read the external round-1 report (R371-1) only after the verdict and ledger were written. Its findings at this head:

| Prior finding | Status at 5c7577e5 | Evidence |
|---|---|---|
| R371-1-F3 BLOCKER, submodule link | RESOLVED | as R370-1-F1 |
| R371-1-F1 MAJOR, initial-bind scope, rationale, DUT-side difference, follow-up | RESOLVED except one sentence, retained as R370-2-F1 | Scope, exception, rationale and the #606 link are present (page:189-225, 873-879). R371-1's own evidence named cycle 1 as the one DUT Talker Advertise withdrawal. The page generalised the contrast to every numbered reconnect (page:219), which R370-2-F1 carries. I found that independently before reading R371-1. |
| R371-1-F2 MINOR, sub-period stop not shown | RESOLVED | Focus 2. The six largest talker captures are explained (page:791-813). The size identity 24 + CRF + other = bytes holds on all 200 rows (`receipts/page-numeric-crosscheck.txt`). |
| R371-1-F4 MINOR, index row | RESOLVED | README.md:11 |
| R371-1-S1 timing uncertainty | TAKEN | page:90-97, 121-136 |
| R371-1-S2 effect-size bound | TAKEN | page:234-250 (t intervals and per-100-cycle upper bounds) |
| R371-1-S3 restore destination | TAKEN | page:851-855 |
| R371-1-S4 restart component breakdown | NOT TAKEN | Optional. No coverage effect. |

## Real limits

- **Raw data.** Raw captures and the per-cycle records for cycles 6-100 are private. My stop-check probe therefore reruns an independent predicate over the addendum's published per-attempt window counts. It cross-checks those counts against the public raw records for cycles 1-5 and the setup and restore snapshots. I replayed no pcap. The 1000-PDU continuous-hold figures for talker 13, 24 and 75 rest on the addendum's replay of private captures. The zero counter deltas corroborate them.
- **Scope of R370-2-F1.** The finding is demonstrated on public cycle 1. Whether any private cycle holds only Mt without an Lv cannot be excluded from public data. The Lv total of 1 limits withdrawals to cycle 1.
- **Hygiene-scan patterns.** The pattern list is not published because it enumerates the private terms it searches for. The receipt lists every hit.
- **Tools and hardware.** No simulator was needed because no RTL changed, and the scoped Verilator was not used. Physical tap calibration was NOT RUN, and no hardware proof is claimed.
- **Hosted snapshot at 2026-09-27T22:41Z.** `rtl-fast`, `docs-check-no-git`, `wire-accountability`, the Yosys shards, `verilator-lint` and `yosys-elaboration` were `success`. `docs-check`, `elaborate` and Verilator shards 1, 2 and 4 were in progress. "Physical gPTP" was skipped. A skip is not hardware proof.
- **Actions not taken.** No Docker, act, host replica, source edit, commit, push or GitHub write was made.
- **Clone integrity** after the probes (`receipts/clone-integrity.txt`): HEAD, tree and the index mode/blob digest equal the exact head. No stage entries remain, worktree bytes have 0 mismatches, there are no untracked or ignored files, and the four gitlinks are unchanged.

## Pending manager duties

- Hosted acceptance at the exact head: `docs-check`, `elaborate` and the Verilator shards were still running at the snapshot. Act replica and candidate-merge validation against live dev `20aa4eab`.
- #606 body says reconnects stayed fast in "100/100 cycles" and that "the DUT kept its Talker Advertise through the hold". Both are now inaccurate: talker demonstrated restarts are 97, and cycle 1 is R370-2-F1. It needs a correction by its owner.
- Decide the owner of the continued-transmission behaviour in talker 13, 24 and 75 (R370-2-S1). #75 currently holds it.
- #75 stays open. AAF is unmeasured and the talker 100-restart line is NOT MET.

R370-2 FINISHED
