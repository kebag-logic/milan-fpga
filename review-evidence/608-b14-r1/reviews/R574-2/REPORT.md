[R574] NEGATIVE - exact head d981b1cc574f757a1d04d1b21d34a078ad85be3d

# R574-2: internal independent re-review of PR #709 (issue #608, lane B14)

- Head `d981b1cc574f757a1d04d1b21d34a078ad85be3d`, tree `e0002fa45fb94b21147abc73704b732dd0f7bd69`, source base dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Delta under review: `6ec1a3a9..d981b1cc`. That is one one-line commit with no trailers and a single parent `6ec1a3a9` (no rebase or amend). It changes only `docs/findings/B14_BENCH_5603C353.md` (+121/-49, `receipts/delta_6ec1a3a9_d981b1cc.diff`). The gitlinks are unchanged from the base.
- Evidence judged: the archived packet `review-evidence/608-b14-r1` at archive commit `c848925d2e88a98e7f31b663e5dd4f342b765487`, extracted by SHA into a disposable tree. Later commits on the evidence branch hold other reviewers' archives, and I did not read them.
- Verdict: **NEGATIVE**, on three MINOR findings, plus one RESIDUE and one SUGGESTION.
  - Every round 1 finding is answered, and every corrected figure reproduces from the archived packet: the withdrawal times, the loss bursts, the 73-frame `SLIP_LB` ledger, the restore basis, the digests and the RMON lanes.
  - **F1:** the rewritten FRAMES observation misstates what the repository declares for the AAF listener's FRAMES_RX. My own round 1 finding (R574-1-F1) directed that wording, and this round corrects it.
  - **F2:** one cited record does not exist in the archive.
  - **F3:** the round-2 recompute claims rest on records that are not public.

## Reconstruction (public state only)

1. AGENTS.md; CONTRIBUTING.md sections 2.1, 3, 4 and 6 (the lane, the verification bar, bench discipline, wording and privacy); docs/README.md.
2. Issue #608: the body; rulings 5885808887 and 5886425487; the B14 assignment 6085135051; the STOPs 6088157558 and 6093984746; the ruling 6094000332; REVIEW READY 6095837334; the round-2 assignment 6096040548; REVIEW READY (round 2) 6096216680.
3. Interface authorities at the head:
   - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1060-1095` (settle recentre and its arm terms);
   - `docs/reference/REGISTER_MAP.md:455-535` (0x200 RMON, `STATS_CAP`);
   - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`, `hdl/ieee1722/crf/KL_crf_rx.sv`, `hdl/milan/milan_datapath.sv:236-245` and `:3690-3705`;
   - `tests/features/counters_contract_milan.feature`;
   - #658 rulings 5988293154 and 5988843004.
4. `git diff 5603c353..d981b1cc` and `6ec1a3a9..d981b1cc`, and the four commits.
5. Archive `c848925d`: the item2, item3, item4, soak, maap and restore records, the raw indexes and the manifests.
6. The PR body, and the PR and issue comments by the manager and the executor.
7. **Only after** writing my own verdict and ledger (`receipts/independent_pass.md`, timestamped) did I read the round 1 findings R574-1 (6096034494) and R575-1 (6096011678). They are resolved or retained in the table below.

## Findings

### R574-2-F1 MINOR: the FRAMES observation misstates the declared STREAM_INPUT contract for the AAF listener

- Lenses: Conformance, RTL, Docs.
- Where:
  - `docs/findings/B14_BENCH_5603C353.md:478`: "Those three match the clause and the contracts the repository declares (`KL_talker_diag_ctx.sv`, `KL_avtp_rx_monitor_ctx.sv`, ...)".
  - `:480`: "Table 5.6 and the declared STREAM_INPUT contract allow at most one per interval, so this needs triage".
  - The PR body's first "Observations for triage" bullet, which repeats the second statement.
- Authority and evidence (`receipts/f1_frames_rx_contract.txt`):
  - **What the module declares and implements.** The module the page cites declares and implements a coalesced frame total for FRAMES_RX on the AAF listeners:
    - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:318-323`: "USER 2026-08-05 FRAMES_RX law: count FRAMES, publish COALESCED at the interval commit - the visible counter advances by the interval's frame total (~8000/s at class A) instead of Table 5.6's +1-per-interval. Both readings are Milan-legal".
    - `:627-630`: "FRAMES_RX commits the interval's FRAME TOTAL (coalesced law, USER 2026-08-05)", with `ram_q_r + frx_add_r` for FRAMES_RX.
    - `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:443` records the same as a project ruling and a known divergence (task #21).
  - So the observed +57,599,387 in 7,200.5 s on the DUT's STREAM_INPUT 0 (`soak/summary.json`, `dut|5|0`; `receipts/soak_counters.txt`) is exactly the behaviour this module declares.
  - **Where the repository conflicts.** Its declarations disagree with each other:
    - the header of the same file (`:27-36`) and `tests/features/counters_contract_milan.feature:196-201` describe +1 per interval;
    - `:318-323` and the implementation say frame total.
  - **The CRF listener has a different server.** Its FRAMES_RX is not served by `KL_avtp_rx_monitor_ctx.sv`. `milan_datapath.sv:242-243` names `KL_crf_rx` as the CRF Media Clock Input's server. GET_COUNTERS word 11 is `crf_pducnt_w` (`:3701`), and `KL_crf_rx.sv:233` says "FRAMES_RX: intervals with >= 1 accepted PDU". The page cites the wrong module as the contract that the CRF listener's +7,200 matches.
  - **Origin.** The page's wording follows R574-1-F1's required outcome. That finding cited only `KL_avtp_rx_monitor_ctx.sv:20-40` and missed `:318-323` and `:627-630`. This round corrects the earlier round. The author applied it faithfully.
- Impact:
  - The page tells triage that the AAF listener departs from "the declared STREAM_INPUT contract", when it follows the law that module declares and implements.
  - The open question is different: whether the coalesced law conforms to Milan v1.2 Table 5.6, and which of the repository's conflicting declarations governs.
  - A triager working from the page would look for an implementation defect rather than a contract decision.
  - The CRF citation points at the wrong server.
- Required outcome:
  - The observation states that `KL_avtp_rx_monitor_ctx.sv` declares and implements a per-interval commit of the frame total for the AAF listeners (ruling of 2026-08-05; `:318-323`, `:627-630`), so the one-per-PDU reading matches that declared law.
  - It states that the repository's declarations conflict (the module header `:27-36` and the feature file against `:318-323`), and that the triage question is the law's conformance to Table 5.6.
  - It cites `KL_crf_rx.sv` for the CRF listener's interval FRAMES_RX.
  - The PR body says the same.
  - No measurement changes.
- Verification: re-read page `:475-480` and the PR body against `KL_avtp_rx_monitor_ctx.sv:27-36`, `:318-323` and `:627-630`, `milan_datapath.sv:242-243` and `:3701`, and `KL_crf_rx.sv:233`.

### R574-2-F2 MINOR: a cited evidence record does not exist in the archive

- Lenses: Conformance, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:662`, the item 4 row of "Records behind each item", which cites `item4/summary.json`.
- Authority and evidence:
  - Round-2 assignment item 6 (issue comment 6096040548) asks for "the path of each cited record".
  - Archive `c848925d` has no `author/item4/summary.json`. Neither `author/MANIFEST.sha256` nor `author/item4/MANIFEST.sha256` lists one.
  - The item 4 summaries that do exist are `item4/short-summary-001-050.json`, `item4/short-summary-051-100.json` and `item4/startup-summary.json` (`receipts/f2_f3_evidence_paths.txt`).
  - `scripts/cited_paths.py` checks every backticked packet path on the page. It finds every other one present (`receipts/cited_paths.txt`).
- Impact: the evidence map that answers R574-1-F6 sends a cold reader to a record that does not exist.
- Required outcome: the item 4 row names only records present at the cited archive commit, for example the two `short-summary-*.json` files, or drops the entry.
- Verification: `scripts/cited_paths.py <page> <archive author dir> <raw-index dir>` reports no missing path other than one resolved by F3's outcome.

### R574-2-F3 MINOR: the round-2 recompute claims cite an unarchived, unidentified record set

- Lenses: Conformance, Tests, Docs.
- Where: `docs/findings/B14_BENCH_5603C353.md:682-689` ("The scripts and their outputs are in the lane's round 2 handoff packet under `round2/`"). Also the claims that rest on it:
  - `:687`: the raw re-decode agrees with `item3/cycles.tsv` "within 0.5 us in all 101 cycles";
  - `:688` and `:558`: 15 of 15 equal "at the final read", for the 7 formats and 2 clock sources;
  - `:689` and `:560`: the 44 rows split as 2 descriptor counts, 18 formats, 18 connection states, 2 clock sources and 4 maps.
- Authority and evidence:
  - The round-2 assignment: "Every statement must be backed by a record in the packet, or weakened or removed", and item 6 asks for the archive commit and the path of each cited record.
  - AGENTS.md section 2: a cold reviewer must reconstruct from GitHub and the repository alone.
  - Archive `c848925d` has no `round2/` path, and the page names no archive commit for it (`receipts/f2_f3_evidence_paths.txt`). The executor's REVIEW READY (6096216680) states that these outputs "are not yet archived".
  - What the archived packet does back:
    - the withdrawal times themselves (per-cycle `msrp.tsv`, reproduced in `receipts/item3_hold.txt`);
    - 15 of 15 at item 2's teardown (`item2/teardown/events.jsonl`, `restore-compare`);
    - the final listener states and maps (`restore/final-*.jsonl`);
    - the clock sources at 06:22 and 08:23 (`restore/restore-compare.txt`);
    - "44 of 44 equal" (`restore/restore-compare.txt`).
  - What it does not back: the formats at the final read, the category split of the 44 rows (`restore-compare.txt` prints 24 non-format rows), and the raw re-decode agreement. The raw snapshot files are indexed by hash but not public.
- Impact: three statements added this round cannot be checked by a cold reviewer. The page points to a private lane location as their record.
- Required outcome: either:
  - the round-2 scripts and outputs (with their input hashes) are archived, and the page names their archive path and commit; or
  - the three claims are restated as limited to what archive `c848925d` records, with the remainder marked as not backed by a public record.
- Verification: the cited `round2/` location resolves at a named archive commit, and the 0.5 us agreement, the final 15-of-15 compare and the 44-row split reproduce from it. Or the restated text matches `c848925d`'s records.

### RESIDUE (wording only; it changes no figure, verdict or clause claim)

- **R574-2-R1** (`:510`): "the register map says such a lane reads "not supported", never "0 errors"". The lane reads zero. `REGISTER_MAP.md:483-484` says a UI "must render it "not supported", never "0 errors"". Exact fix: replace "says such a lane reads" with "says such a lane must be rendered".

### SUGGESTION

- **R574-2-S1** (`:479` and `:462`): in the FRAMES observation, note that the reference peer's FRAMES_RX also advanced once per PDU (+57,599,253 and +3,599,953; `soak/summary.json`, `peer|5|0` and `peer|5|8`). The coalesced law's own comment (`KL_avtp_rx_monitor_ctx.sv:322`) cites that peer behaviour, so this context bears on the triage question.

## Round 1 findings at this head

| Finding | Status at `d981b1cc` | Evidence |
|---|---|---|
| R574-1-F1 (FRAMES clause) | **Partly resolved; superseded by R574-2-F1.** Tables 5.4 and 5.6 are now cited as observation-interval counters; FRAMES_TX on both talkers and the CRF listener's FRAMES_RX are recorded as +7,200; the AAF listener's per-PDU FRAMES_RX is named for triage. The "declared contract" sentence that R574-1-F1's required outcome led to is wrong (F1) | `:475-480`; `receipts/soak_counters.txt`, `receipts/f1_frames_rx_contract.txt` |
| R574-1-F2 = R575-1-F1 (withdrawal reference) | **Resolved.** 0.095 and 0.318 s after the bridge's `Lv`, 0.104 and 0.328 s after the response, pilot 0.039 s; no other cycle has a DUT Talker Advertise `Lv` | `:191-194`, `:686`; `receipts/item3_hold.txt` |
| R574-1-F3 = R575-1-F2 (loss bursts) | **Resolved.** Captures 002 and 042 on four streams; 035 on three, with the DUT's CRF (port 3, `0001`) intact; AAF 9 to 12, CRF 1 | `:465-467`; `soak/soak-overlap-recovery.txt`, `soak/soak-wire-aggregate.txt` |
| R574-1-F4 (restore basis, saved state) | **Resolved**, with F3 noted. The summary, Contents and PR body give 15 as-found rows and the 44-row 06:22 inventory; the saved-state content is marked not read back. Its final-read half for formats depends on F3 | `:22`, `:41`, `:557-569`; `receipts/nvm_before_after.txt` |
| R574-1-F5 = R575-1-F3 (`SLIP_LB`) | **Resolved.** The soak-bind step and its bracket are recorded (`0x8e` at 06:22:39.06, bind 06:22:39.51, t0 06:23:22.71, `0x90` at 06:23:23.21). The 73-frame phase ledger reproduces exactly: 6+21+0+3+3+35+3+0+1+1 = 73, and the between-run gaps are 11.9 to 63.2 s. The cause claim is limited to the documented arm terms | `:486-497`, `:577-595`; `receipts/slip_lb_ledger.txt`, `receipts/item2_between_runs.txt` |
| R574-1-F6 (packet identity) | **Resolved**, with F2 and F3 noted. The path, branch, commit and all six digests verify; the 422 redactions and 2,356 files check out; the capture counts and bytes match the raw indexes; the pre-redaction soak index digest matches `RAW-ARTIFACTS.json` | `:641-680`; `receipts/archive_digests.txt` |
| R575-1-F4 (receive-drop lane) | **Resolved.** `STATS_CAP` is `0x1B8` at 27 of 27 reads, with bit 6 = 0; lanes 0x220, 0x224 and 0x22C are real; FCS and alignment are NOT RUN; drops have no source. Wording residue: R574-2-R1 | `:507-513`; `receipts/item6_console.txt` |
| R574-1-R1 and R575-1-R6 (NOT RUN) | Applied | `:35`, `:150` |
| R574-1-R2 (05:17 wording) | Applied; no ATDECC record lies between 04:54:47 and 05:17:01 (`precheck/host-checks-s3.json` holds host checks only) | `:431` |
| R574-1-R3 and R575-1-R1 (late `Lv`) | Applied | `:173` |
| R575-1-R2 (Listener declaration) | Applied. The profiles are 86 / 11+1 / 2 | `:189`; `receipts/item3_hold.txt` |
| R575-1-R3 (restore summary) | Applied (as R574-1-F4) | `:41` |
| R575-1-R4 (traffic counters) | Applied. No counter outside LOCKED, UNLOCKED, MEDIA_RESET, FRAMES_TX, FRAMES_RX and TIMESTAMP_VALID moved in the 30 phases | `:90` |
| R575-1-R5 (tap-total basis) | Applied. 121 files, span sum 6,858.7 s, first start 15.97 s before t0 | `:463`; `soak/soak-wire-aggregate.txt`, `soak/soak-coverage.txt` |
| R574-1-S2 (map vs #658) | Applied, and it matches rulings 5988293154 item 1 and 5988843004 items 1 and 3 | `:438` |
| R574-1-S1 = R575-1-S1 (findings index) | Not applied; left to the manager (a suggestion) | - |

## No new measurement campaign

- Every figure added in the delta derives from archive `c848925d` records or from raw files that archive indexes by SHA-256.
- No timestamp or record is later than the round 1 session, which ended at 08:24 UTC.
- The page says the saved-state content "was not read back". This agrees with the executor's statement that the one allowed read-only read was not made and the bench lock was not taken.
- I cannot see the bench-lock log, so the absence of bench action rests on the public record (see Real limits).

## Privacy

- The added lines name no instrument, reference-peer product, host, interface, subnet, address or home path (scan of the 121 added lines).
- They add archive paths, digests, repository source paths and packet record names.
- `soak/hive-events-summary.json` names a controller application already named in merged findings pages (`653_DISCONNECT_ORDER_BENCH.md`, `117_GPTP_SILICON_EVIDENCE.md`). It is not bench equipment.
- `docs_check.py` returns rc 0 (scrub self-test 23/23). Planted controls show it fails on a home path and on a bench address (`receipts/probes/`).

## Lens results (each with the artifact examined at `d981b1cc`)

```text
[R574] MINOR Conformance -- B14_BENCH_5603C353.md:478-480, :662, :682-689 -- F1, F2, F3
[R574] MINOR RTL -- B14_BENCH_5603C353.md:478-480 against KL_avtp_rx_monitor_ctx.sv:318-323/:627-630, KL_crf_rx.sv:233, milan_datapath.sv:242-243/:3701 -- F1
[R574] PASS Robustness -- B14_BENCH_5603C353.md:465-468, :486-497, :507-513, :568-569, :191-194 -- the boundary and failure-path claims added this round, checked against the archived records: the soak-bind bracket (console-prebind.txt 06:22:39.058 0x8e, bind-a-aaf.jsonl 06:22:39.507, soak-coverage.txt t0 1791613402.7085, console-soak-000.txt 06:23:23.211 0x90); the partial-stream loss in capture 035 (soak-overlap-recovery.txt); the no-source lane at 27 of 27 reads (STATS_CAP 0x1B8, bit 6 = 0); the not-read-back saved state (NVM seq 234 to 272, 38 ok, 0 failed, 54 records, 3,336 B); the pilot cycle's withdrawal kept out of the graded count; no format SET anywhere in the packet (every format-check has set null or false)
[R574] MINOR Tests -- B14_BENCH_5603C353.md:682-689 -- F3
[R574] MINOR Docs -- B14_BENCH_5603C353.md:478-480, :662, :682-689; PR body -- F1, F2, F3 (RESIDUE R1 at :510)
```

Checked and found correct, beyond the findings:

- **Conformance:**
  - the arm terms at `:493` against `MEDIA_CLOCK_FOLLOWING.md:1088-1090`;
  - the #658 identity default;
  - the Table 5.4/5.6 paraphrase at `:475-476` against the clause text the repository quotes (`counters_contract_milan.feature:42-46`, `KL_avtp_rx_monitor_ctx.sv:27-31`);
  - item 6 against `REGISTER_MAP.md:475-535`.
- **RTL:**
  - `STATS_CAP` lane mapping (lane n at `0x210+4n`; lane 6 = `0x228`);
  - the `SLIP_LB` address `0x8D4` and its 2-dup-per-frame reading;
  - the CRF and AAF counter servers in `milan_datapath.sv`.
- **Tests:**
  - every corrected figure recomputed from the archive by the scripts below;
  - planted controls catch altered records (`receipts/planted_controls.txt`);
  - the receipts reproduce byte for byte (`receipts/rerun_check.txt`).
- **Docs:** the documentation gates at the head, all rc 0 (`receipts/gates/`):
  - `docs_check.py` and `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors` (423 anchors);
  - `check_em_dash.py --base 5603c353` (691 added lines, 0 findings);
  - `check_doc_paths.py` (953 paths);
  - `git diff --check` for both ranges.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | the page's delta against Milan v1.2 Tables 5.4 and 5.6 as quoted in the repository, `MEDIA_CLOCK_FOLLOWING.md` settle recentre, `REGISTER_MAP.md` 0x200, #658 rulings, the round-2 assignment items 1-8, archive `c848925d` records | R574-2 | d981b1cc574f757a1d04d1b21d34a078ad85be3d |
| RTL | UNCLEAN (F1) | `KL_avtp_rx_monitor_ctx.sv:27-36, 318-325, 624-631`; `KL_crf_rx.sv:233`; `milan_datapath.sv:236-245, 3690-3705`; `REGISTER_MAP.md:455-535`; 27 console reads of 0x110/0x200-0x233; 30 item 2 phases and 30 console reads of 0x8D4 | R574-2 | d981b1cc574f757a1d04d1b21d34a078ad85be3d |
| Robustness | CLEAN | soak-bind bracket records; `soak-overlap-recovery.txt`; `STATS_CAP` reads; NVM status before and after; item 3 pilot and per-cycle `msrp.tsv`; format-check records | R574-2 | d981b1cc574f757a1d04d1b21d34a078ad85be3d |
| Tests | UNCLEAN (F3) | `scripts/item3_hold.py`, `slip_lb_ledger.py`, `soak_counters.py`, `item6_console.py` and `cited_paths.py` over archive `c848925d`; the planted controls; the archive digests | R574-2 | d981b1cc574f757a1d04d1b21d34a078ad85be3d |
| Docs | UNCLEAN (F1, F2, F3) | `docs/findings/B14_BENCH_5603C353.md` (691 lines; delta +121/-49); the PR body; the documentation gates (rc 0); the privacy scan | R574-2 | d981b1cc574f757a1d04d1b21d34a078ad85be3d |

RESIDUE R1 and SUGGESTION S1 leave no lens unclean. Earlier rounds' coverage of the unchanged round 1 content stands. This round reviewed the delta and the statements the delta corrects.

## Real limits

- **No standards text.** No Milan or IEEE text was available locally. I checked the Table 5.4 and 5.6 wording against the repository's quotations only.
- **No raw files.** The raw captures and raw snapshots are outside the archive, indexed by hash only. I could not reproduce:
  - the raw re-decode agreement;
  - the final-read formats;
  - the 44-row category split.

  (That is F3.)
- **Ineffective probe.** The em-dash planted probe could not exercise `check_em_dash.py`, because that gate judges committed lines and this round allows no commit. The gate's own arms report 339/339, and it returned rc 0 on the real diff.
- **Markdown environment.** The documentation gates ran in an existing local Markdown environment with the locked cmarkgfm 2025.10.22. I did not re-verify every transitive pin.
- **No RTL build.** No RTL build, suite or bank ran: the diff is one Markdown page. No manager source bank ran at this head, and none is claimed or inferred.
- **No bench access.** I could not see the bench-lock log. Physical calibration is NOT RUN, and field skips are not hardware proof.

## Hosted evidence at the exact head (observed, not accepted)

- **Executed with success** (`receipts/hosted_checks_d981b1cc.tsv`): `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `wire-accountability`, `docs-check-no-git` and `full-ci-gate`.
- **Still in progress** at query time: `docs-check`.
- **Skipped contexts, not evidence:** `verilator-suites`, `yosys-portability`, their shards, `verilator-lint`, `yosys-elaboration`, `firmware-unit` and Physical gPTP.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the in-progress `docs-check`.
- Current-dev merge-candidate validation (builder and native banks) against live dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- If F3 is answered by archiving: archive the round-2 handoff packet and give its commit.
- Carry R574-2-R1 to the residue checklist.
- Rule on the findings-index suggestion (R574-1-S1 = R575-1-S1).
- Re-review after F1 to F3 are answered.
- Decide #608 closure (the PR says Refs).
- Publish this report.

## Clone state after the review

- HEAD and tree are exact. The index tree equals the HEAD tree, the worktree equals HEAD, and `git status --porcelain --ignored` is empty.
- The page blob is `0b6b4a7b` with mode 100644.
- Gitlinks are unchanged from the base: `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 2ad2f845, `third_party/lwSRP` 9197193e, `third_party/verilog-axis` 48ff7a7e (`receipts/clone_integrity.txt`).
- The probes appended a line to the page and reverted it with `git checkout`. The bytecode cache created by the gate runs was removed.
- No source edits, commits, pushes or GitHub writes were made.

## Publishable files

`REPORT.md`, plus every file listed in `MANIFEST.sha256`: the scripts and the receipts. `scripts/run_all.sh <archive author dir> <out>` reproduces the four recompute receipts.

R574-2 FINISHED
