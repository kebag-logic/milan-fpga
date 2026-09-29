[R403] NEGATIVE - exact head f9eab5bf55ca4471e6e48ae3d38018d7e804505b

# R403-1: external review of PR #620 (issue #599, with #394 and #387)

- Reviewer: [R403], external, cleared context. Round R403-1.
- Exact head `f9eab5bf55ca4471e6e48ae3d38018d7e804505b`, tree `72e4717edbe4638e83c342720c42987ad979770f`, one commit on dev `13eda870d1a6cf3f946fc228a98862366b08d102`.
- Diff: two new pages only, `docs/findings/599_394_E1_LINK_CYCLES.md` (372 lines) and `docs/findings/387_SOFTWARE_GM_STEP.md` (299 lines). No RTL, firmware, script or other document changes. The PR refers to #599, #394 and #387 and closes none of them.
- Evidence judged: the public archive `review-evidence/b1-r1` at `92e1d7a3c815dbf70faa8f0975cc063040edd967` (branch `b1-review-evidence`), 236 files.
- Reconstruction order: AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6); `docs/findings/README.md`; issue bodies #599, #394 and #387.
  - Decisions read: the assignment 5884216527; the owner decisions on #394 (2026-09-23, 09-24, 09-27) and #387 (5794731090, 5862116683, 5862731997); the manager statements 5859048589 and 5859297500; the #602 ruling 5859297355.
  - Interface authorities read: TIME_SYNC.md step policy, GM_LOSS_RECOVERY.md (recovery bound and media re-base), BAREMETAL_FIRMWARE.md PHY publication, REGISTER_MAP.md (MAC_STATUS, LINKG_STAT, CLKV_STAT, CLKV_TUCNT, CRFT_CTRL, MCSRV_STAT, PP_STAT and PP_NVM_STAT), SAVED_STATE_SNAPSHOT_OWNERSHIP.md nvm_pend, and TESTING.md section 6b.
  - Then the diff and its history, then the archive.
- Prior review findings on this PR: none. At read time the PR carried only the two review-start comments and no review. Nothing to resolve or retain. No other reviewer's report was read before this verdict.

## Verdict summary

The pages' tables are faithful to the archived extraction. Every per-cycle and per-step cell re-derives from the per-action `analysis.json` files with independent code. The only differences are two half-up display roundings of 0.01 s. The identity gate binds, and the #599 and #394 claims hold on that extraction.

The round is NEGATIVE for four reasons:

- The #387 page labels acceptance 4 PASS. The evidence supports only **PARTLY MET** (F1).
- The raw captures behind every measured action are neither archived nor durably retained, and the pages do not link the archive (F2).
- The archive exposes bench-identifying tokens (F3).
- The restore proof omits the DUT's saved-state layer, which ended in a different state from the one found (F4).

## Answers to the assigned questions

1. **Identity gate: binds.**
   - Readback: VERSION `0x00020060`; ROM CRC32 `acad92b9` over 53,344 B; QSPI payload `d84bce7b` over 3,825,788 B; AEM `93742dd2` over 7,352 B. All equal the build record for the `eto` seed of dev `13eda870` (`author/identity/expected-crc.txt`, `console-identity.txt`).
   - ENTITY and CONFIGURATION are byte-exact to the image, entity `020000fffe000001` (`identity-aecp-comparison.txt`). The grader passed 10/10.
   - I regenerated the AEM image from `configs/endstation_ax7101_1x1_tdm8.yaml` at this head through the builder's own entry points. It is byte-identical: len 7352, CRC32 `93742dd2`, SHA-256 `9b0776...4404` (`receipts/aem_from_source.txt`).
   - ROM and QSPI are bound only through the build record; they were not rebuilt here.
   - The page's claim that the `asl` seed reads `809fcffa` has no artifact in the archive (part of F2).
2. **#599 acceptance 4.**
   - The link-drop proof holds on its disclosed method. The "read-only BMSR read" is the firmware's own 125 ms BMSR poll, as published in MAC_STATUS and the `link_status` CSR. The operator published that method in the TAKEN comment before the run, and no one objected.
     - Publication fell at 2.31-2.56 s and returned at 37.07-37.32 s after OFF.
     - The tap saw no far-end frame from 5 s after OFF until ON, and LINKG_STAT `act_recent` cleared at 3.84 s.
     - This is not an independent MDIO read (a limit, not a finding).
   - 10/10 cycles show LINK_DOWN +1 and LINK_UP +1 (DUT 2/1 to 12/11, continuous across cycles). MAC_STATUS and `link_status` each run exactly `0xd`, `0x0`, `0xd` in every cycle (`receipts/mac_sequences.txt`). The CSR follows MAC_STATUS by 14-27 ms within the same round.
   - The poll-period statement ("polls every 125 ms and publishes within 250 ms") matches BAREMETAL_FIRMWARE.md:1971-1972. The bench cannot measure acceptance 1 and the page does not claim to. The wording of 599:98-100 and :215-216 is loose (S2).
3. **#394 acceptance 2 (e1): met on the archived extraction.** Per cycle:
   - The reservation regained `CRFT_CTRL` `0x3002e3`, with bit 6 "reservation active" and bit 7 "licensed" (REGISTER_MAP.md:946). The loss-to-regain times re-derive.
   - Both bindings read conn_count 1 in every successful poll.
   - No reboot: RST_EPOCH was 1 throughout.
   - No re-bind: each cycle's action log holds only power commands.
   - asCapable, sync and `tu=0` returned 0.544-1.786 s after the grandmaster's return, inside the 5 s bound.
   - Both listeners were MEDIA_LOCKED again at 43.95-52.55 s after OFF.
   - MEDIA_UNLOCKED went +1 per cycle and no `tu=1` PDU followed recovery.
   - The restart time is recorded against #75 without a verdict, as the acceptance text asks.
4. **#387 acceptance 4: PARTLY MET, not met.** The media-plane half is met:
   - five takeovers and five releases on a running CRF stream, each a DUT PHC step of +9.987 to +9.988 ms or -10.003 to -10.005 ms (the grandmaster's time moved +9.994 to +9.995 ms and -9.996 to -9.998 ms);
   - outgoing `mr` changed 0 times on either talker;
   - talker and listener MEDIA_RESET +0;
   - DUT and peer MEDIA_UNLOCKED +0;
   - `A_MCSRV_STAT` read LOCKED in every sample, with 1-3 discarded windows per step;
   - the CRF licence never dropped and the largest CRF gap was 2 ms.

   The `tu` half of the decided "one counted event per step" contract is **not** met. After every step the DUT lost asCapable for 2.0 s, and each step then produced:
   - 2-3 `tu` episodes on the wire;
   - 4-5 CLKV_TUCNT intervals;
   - GPTP_GM_CHANGED +3 at nine edges and +1 at one, for exactly one actual grandmaster change per edge;
   - CLOCK_DOMAIN UNLOCKED +2 or +3.

   The counted render re-base cannot be observed on this bench (no AAF stream, no tally CSR). It is covered only by simulation. Step-to-steady was 3.00-4.53 s, but item 2 records no time bound: the page says so itself, and its verdict row contradicts that. See F1.
5. **Restore proof: incomplete** (F4). Outlets, the grandmaster, the streams, the 53/53 census, the grader, the tap and the controller host's clock (frequency and time trajectory, residual 4,352 ns) are proven. The DUT's saved-state layer is not.
6. **Privacy: pages clean, archive not** (F3). The repository's own scrub finds 0 on both pages and on all 236 archive files. The Markdown gates pass in the pinned environment (listed under Validation).

## Findings

### F1: MAJOR (Conformance, Docs). #387 acceptance 4 is labelled PASS; the evidence supports PARTLY MET

- **Where:** `docs/findings/387_SOFTWARE_GM_STEP.md:12` (verdict row), `:143`, `:172`, `:175`, `:179-205`, `:213`.
- **Authority:** #387 objective ("returns to its steady state through one bounded, counted event") and acceptance 4. Manager statement 5859048589 ("one counted `tu`/`mr`/MEDIA_RESET event per step"); the #602 ruling removes only `mr` and MEDIA_RESET from that. GM_LOSS_RECOVERY.md "Media re-base on a PHC step" ("Each step of the step policy is one counted event").
- **Evidence** (`receipts/rederive.txt`, from `author/bench/gm0[1-5]/analysis.json`):
  - Every one of the ten steps is followed 0.22-1.25 s later by a 2.000-2.003 s asCapable loss.
  - Each step shows 2-3 rises of `tu` on the DUT's outgoing CRF, and CLKV_TUCNT rises by 8-10 per run.
  - DUT GPTP_GM_CHANGED rose by +6 per run (+4 in run 4), while the console and wire show exactly one grandmaster change per edge.
  - DUT CLOCK_DOMAIN LOCKED/UNLOCKED rose by +5 or +6 per run.
  - The page records all of this, yet its verdict row says PASS.
  - The contract row "Media never unlocked" (:175) and "neither listener unlocked" (:12) are not reconciled with the DUT's own CLOCK_DOMAIN UNLOCKED counts.
  - The verdict row says "inside the 5 s bound", while :143 calls that bound context rather than #387's, and :175 says item 2 has no time bound.
- **Impact:**
  - A merged page states PASS for an acceptance item whose single-event `tu` half fails.
  - The failure comes from a product behaviour: the DUT's own PHC step costs asCapable, which is consistent with peer delay being computed across the step (0 ns at takeovers, 4,039-4,701 ns at releases).
  - That behaviour has no issue yet, and a later closure of #387 could cite this row.
- **Required outcome:**
  - The page records #387 acceptance 4 as PARTLY MET: the media-plane reactions are met; the single counted `tu` event is not met because of the asCapable loss; the render re-base is not observable on this bench.
  - The verdict row drops or reconciles "inside the 5 s bound".
  - The CLOCK_DOMAIN UNLOCKED counts are reconciled with "media never unlocked".
  - The asCapable-after-step behaviour has a public issue linked from the page (a manager decision). This PR does not have to fix it.
- **Verification:** re-read of the verdict row, the contract table and the deviation section at the corrected head; the linked issue exists.

### F2: MAJOR (Conformance, Tests, Docs). Raw captures for every measured action are unarchived and not durably retained; the pages do not link the archive

- **Where:**
  - `docs/findings/599_394_E1_LINK_CYCLES.md:282-288` ("Raw captures are kept outside the packet on the bench host") and `:306-372`.
  - `docs/findings/387_SOFTWARE_GM_STEP.md:247` and `:263-299`.
  - Archive `author/bench/*/raw-artifacts.json`, whose paths all sit under a temporary directory.
- **Authority:** #394 acceptance 2 ("Artifacts per docs/testing/TESTING.md 6b"). #387 acceptance 4 ("with the raw artifacts retained per docs/testing/TESTING.md 6b"). TESTING.md section 6b ("save external wire captures and controller transcripts with timestamps"). AGENTS.md section 6, Docs lens ("enough evidence for another cold reviewer"). The #600 precedent page links its archive at a pinned commit and states private cold storage (`docs/findings/394_387_E1_SWITCH_CYCLES.md:389-405`).
- **Evidence** (`receipts/restore_and_retention.txt`):
  - For bmsr-proof, cycle01-10 and gm01-05, the console log, the controller transcript, the tap capture and the controller-port capture are all absent from the archive. The controller transcript is archived only for baseline-bound, dryrun and final.
  - Every index path roots at `/tmp`.
  - The tables therefore re-derive only from the author's own extraction.
  - Claims that rest only on unarchived raw data:
    - the peer-delay readings of 0, 4,039-4,701 and 373-389 ns (387:187-191);
    - "Both agreed in all 7,520 console rounds" (599:94); only the change lists can be checked;
    - the standalone alignment-test counters (387:64-66); these are only inferable from counter continuity across runs;
    - "`asl` reads `809fcffa`" (599:39), which has no artifact at all.
- **Impact:** the acceptance-required raw evidence can disappear with a temporary directory, and a cold reader of the merged pages cannot find the archive.
- **Required outcome:**
  - Every action's raw files are retained in a durable, named, non-temporary location (private is acceptable, as for #600), or are published.
  - Both pages state that location and link the public archive at a pinned commit.
  - Each claim listed above either gets an archived source or is removed.
- **Verification:**
  - The corrected pages carry the pinned link and the retention statement.
  - The manager confirms the retained files hash to the pages' tables. `scripts/check_page_hashes.py` gives 0 mismatches today: 100 raw rows, of which 31 have an archived copy.

### F3: MINOR (Docs, Conformance). The published archive carries bench-identifying tokens

- **Where** (archive, not the diff):
  - `author/capture/capture-prerequisite-raw.txt:8,13,14,16`
  - `author/capture/capture-cleanup.txt:8`
  - `author/bench/gm0[1-5]/ptp4l-gm.log` and `ptp4l-slave.log`
  - `author/gm/slave-test.log`
- **Authority:** CONTRIBUTING.md section 6 (no interface names or other bench-identifying information) and the assignment's privacy rule.
- **Evidence** (`receipts/scrub_packet.txt`, values masked):
  - interface names on the capture host and the controller host (55 occurrences);
  - a local account name in a file listing;
  - two capture-host NIC MAC addresses, one printed beside the redaction placeholder for the interface name derived from it, which defeats that redaction.
  - The repository scrub does not cover these shapes and reports 0. The #600 archive carries none of them.
  - The controller host's MAC-derived clock identity also appears in `author/tools/b1_analyze.py` and the gm analyses. The page itself avoids it; the manager should judge it against the precedent that the switch's identity is already public.
- **Impact:** bench identity is published. The pages themselves are clean.
- **Required outcome:** a re-archived, redacted packet.
- **Verification:** `scripts/scrub_packet.py` over the new archive shows no interface name, no account name and no unapproved MAC address.

### F4: MINOR (Robustness, Conformance, Docs). The restore proof omits the DUT saved-state layer, which ended differently from how it was found

- **Where:** `docs/findings/599_394_E1_LINK_CYCLES.md:260-276`, `docs/findings/387_SOFTWARE_GM_STEP.md:219-243`, and the PR body ("All restored and proven").
- **Authority:** assignment item 5 ("Restore everything ... Prove it"); SAVED_STATE_SNAPSHOT_OWNERSHIP.md:277 (nvm_pend is "accepted work that is in no verified slot").
- **Evidence** (`receipts/restore_and_retention.txt`):
  - At the start, PP_STAT `5b000444`, `pend=0`, `commits ok=0`, slots at sequence 227/228.
  - At the end, PP_STAT `5b000c44` with nvm_pend set in all 80 samples of the final action and at the final console, `pend=1`, `commits ok=2`, slots at sequence 229/230.
  - The 53-read census compares AEM state only.
- **Impact:**
  - What a DUT reset would restore (saved bindings or clock source) is unproven and may differ from the found state.
  - The next lane inherits an unknown persistence state.
  - A pending bit that does not clear may itself be a product observation.
- **Required outcome:** the pages record the saved-state layer at start and end, and either show the persisted content equals the found state (for example after pend clears) or record the difference with an owner.
- **Verification:** a later `milan_nvm` readback with `pend=0` and a record comparison, or explicit page text naming the residual state.

### Suggestions (non-blocking; do not affect coverage)

- **S1 (Tests):** `author/tools/b1_check.py` and `b1_gmcheck.py`. The per-action verdict scripts do not assert the acceptance predicates. Five planted defects survive them: LINK_DOWN counted twice, LINK_UP not counted, MAC_STATUS never returning, `mr` toggled at a step, and a talker MEDIA_RESET increment. The tables still expose all five, and the reviewer's re-derivation kills them (`receipts/mutate_checks.txt`). Encoding the predicates would make the PASS rows self-checking.
- **S2 (Docs):** 599:98-100 and :215-216. "The poll adds up to one further period" is ambiguous between the 125 ms trigger and the 250 ms publication bound. The "PHY link dropped/returned" bullets are publication brackets. State the 250 ms bound explicitly.
- **S3 (Docs):** 387:179 gives "0.22-0.97 s", measured from the end of the step bracket. Measured from its start the range reaches 1.25 s (run 3 takeover).
- **S4 (Docs, manager):** `docs/findings/README.md` does not index the new pages, nor PR #600's. The assignment forbade other document edits.

## Reviewer-owned completion ledger (this round)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MAJOR, F3 MINOR, F4 MINOR) | Both pages against #599 acceptance 1 and 4, #394 acceptance 2, #387 acceptance 4, the owner decisions, the #602 ruling, TIME_SYNC.md:76-110, GM_LOSS_RECOVERY.md:88-245 and BAREMETAL_FIRMWARE.md:1963-1979; archive analyses, identity and restore files | R403-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| RTL | CLEAN | The diff has no RTL. Every CSR decoding the extraction uses was checked against REGISTER_MAP.md: MAC_STATUS :406, LINKG_STAT :744, CLKV_STAT :783, CLKV_TUCNT :784, CRFT_CTRL :946, MCSRV_STAT :2035, PP_STAT/PP_NVM_STAT :2247-2253. The pages' step-policy and contract claims were checked against TIME_SYNC.md:76-110 and GM_LOSS_RECOVERY.md:142-245. All match. The asCapable-after-step product behaviour sits outside this diff and is carried by F1 | R403-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Robustness | UNCLEAN (F4 MINOR) | Restore and reset paths: `author/restore/*`, `identity/console-identity.txt`, dryrun and final consoles; RST_EPOCH, bindings, outlet and census continuity; counter continuity across cycles and runs; the console timing artifact in run 4 | R403-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Tests | UNCLEAN (F2 MAJOR) | `author/tools/b1_analyze.py`, `b1_summary.py`, `b1_check.py`, `b1_gmcheck.py`; independent re-derivation of every table cell; a 14-case mutation probe; 122 page hashes cross-checked | R403-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |
| Docs | UNCLEAN (F1, F2 MAJOR; F3, F4 MINOR) | Both pages in full; the pinned-environment gates; docs_check, check_doc_style, gen_toc, check_em_dash and check_doc_paths (all rc 0); scrub over pages and archive; `docs/findings/README.md` entry rules | R403-1 | f9eab5bf55ca4471e6e48ae3d38018d7e804505b |

## Validation run by the reviewer (foreground, rc as recorded in receipts)

Pinned Markdown environment: a private virtual environment installed with `--require-hashes` from `tools/markdown/requirements.txt` (cmarkgfm 2025.10.22, html5lib 1.1, CPython 3.14.7; `receipts/md_env.txt`). All of the following returned rc 0 (`receipts/md_gates.txt`):

- `docs_check.py`: 0 findings over 176 md files and 938 scrubbed files; self-test 23/23 and 4/4.
- `check_doc_style.py`.
- `gen_toc.py --check`.
- `check_em_dash.py --base 13eda870`: 0 findings over 671 added lines; self-test 339 arms.
- `check_doc_paths.py`: 854 paths.
- `check_baremetal_only.py --check`.
- `check_feature_status.py --self-test`.
- `ci_scope.py --selftest`.
- `git diff --check`.

Reviewer probes:

- `scripts/rederive.py`: every table cell, 0 differences beyond display rounding.
- `scripts/check_page_hashes.py`: 0 mismatches.
- `scripts/aem_from_source.py`: AEM byte-identical.
- `scripts/mutate_checks.py`: 14 cases.
- `scripts/scrub_packet.py`.
- `scripts/restore_and_retention.py`.
- `scripts/verify_clone.sh`: 962 tracked blobs re-hashed from disk, 0 differ; no residue; gitlinks `external` efeb541a (not initialised), `gptp-processor` 5dce647a, `protocol-processor` c951a9ff and `third_party/verilog-axis` 48ff7a7e, each at stage 0 and clean.

Hosted exact-head contexts, read-only (`receipts/hosted_checks_f9eab5bf.tsv`):

- success: rtl-fast, elaborate, wire-accountability, docs-check-no-git, full-ci-gate, bdd-conformance, changes;
- in progress at read time: docs-check;
- skipped (the documentation-only no-op path, not proof of execution): verilator-suites, yosys-portability and the shards.

## Real limits

- Physical calibration was NOT RUN, and field skips are not hardware proof.
- No bench access. Every bench value is judged from the author's archived extraction, not from raw captures (F2).
- The ROM and QSPI CRCs were not rebuilt from source; only the AEM image was.
- The upstream digest of the software grandmaster's source tarball was not independently confirmed.
- The link-drop proof reads the BMSR through the firmware under test, not through an independent MDIO read.
- Evidence objects fetched into the clone's object store: `92e1d7a3`, and `8f983d24` for the #600 comparison. No ref, index or worktree change.

## Pending manager duties

- Hosted and local-replica acceptance at the exact head, including the docs-check context still in progress at read time.
- The final current-dev candidate build: source base `13eda870`, live dev `8e2967f9`.
- The asCapable-after-step issue (F1).
- A durable raw retention location (F2).
- A redacted re-archive (F3).
- The saved-state readback (F4).
- The findings index entry (S4).

R403-1 FINISHED
