[R402] POSITIVE - exact head 931c3edfced972e01356cd989b5092a1672de5a3

# R402-2 delta review of PR #620 (issue #599, with #394 and #387)

This is round R402-2, the internal cleared-context review. The head is `931c3edfced972e01356cd989b5092a1672de5a3`, tree `56f7cdcd078625cbf8172aa73693a075b0164d4a`. The delta under review is one docs commit, `f9eab5bf..931c3edf` by [A441], answering R402-1 and R403-1 under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885377252). It changes only the two findings pages: `docs/findings/387_SOFTWARE_GM_STEP.md` (+71/-11) and `docs/findings/599_394_E1_LINK_CYCLES.md` (+72/-11). The whole diff from `13eda870` is those two new pages (792 added lines). The commit subject is one line, with no body and no trailers. No bench access was used this round.

Sources, in this order:

- AGENTS.md and CONTRIBUTING.md (sections 4 and 6), then docs/README.
- The body of issue #599, the manager comments on it (assignment 5884216527, round-2 rulings 5885377252), TAKEN and REVIEW READY for both rounds, and the PR body as live at review time (SHA-256 `db67fabc…`).
- #387: its body, 5859048589 and the owner decision 5862731997. The #602 ruling (5859297355). #621.
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 3, 6.1, 11 and the PP_NVM_STAT layout. `CHANGELOG.md:275-309`. `REGISTER_MAP.md` `PP_STAT` (0x924), `PP_NVM_STAT` (0x93C) and `0x8DC`. `BAREMETAL_FIRMWARE.md:1918-1933,1971-1977`. `SAVED_STATE_MATERIALIZATION.md:6`. The #600 retention precedent (`394_387_E1_SWITCH_CYCLES.md:387-405`).
- The RTL behind the pending bit: `hdl/milan/KL_pp_shadow.sv:905-958` and `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:255-292`, at pin `c951a9ff`.
- The public packet at `04d00b6693315d2b14a6c6b51b681a3136b550c2:review-evidence/b1-r1`. The earlier archive `92e1d7a3` was used for the redaction comparison.
- The retained raw copies, read-only, to re-run the extractions.

The R403-1 findings were read only after this verdict and ledger were drafted (see "Prior public review findings").

## Verdict

**POSITIVE.** Every round-2 ruling is met at this head, and each claim the round added reproduces from hash-checked inputs. No BLOCKER, MAJOR or MINOR finding is open under any lens. Three SUGGESTIONs follow; they do not affect coverage.

1. **#387 acceptance 4 is PARTLY MET everywhere, and every gap is named.** It appears so in the verdict row (387:12), the contract-check conclusion (:186-194), the renamed deviation section (:196-234), the Contents line (:24), the PR body verdict table and F1 bullet, and REVIEW READY. The gaps are named in each:
   - `tu` is signalled 2-3 times per step instead of one counted event;
   - asCapable is lost for 2.0 s after every step, [#621](https://github.com/kebag-logic/milan-fpga/issues/621), which is open;
   - DUT GPTP_GM_CHANGED rises by +3 at nine of ten edges and +1 at the tenth. Re-derived per edge from the raw controller transcripts: `[3,3,3,3,3,3,1,3,3,3]` (`receipts/rederive_r2.txt` D);
   - the counted render re-base is not observable. The page states what would make it observable (:110-115): an AAF stream bound into the render stage, plus the recentre count on a register or console command. It is correct that today the count is a verification tap only (`REGISTER_MAP.md:2000-2002`).

   The bound sentence reads "Item 2 sets no time bound". That matches the contract row (:184), #387 comment 5859048589 ("with no time bound") and :152, where the 5 s recovery bound is context only. "Media" is now defined (:192), and the DUT's CLOCK_DOMAIN UNLOCKED counts are reconciled with it (:194).

   Every measurement, contract and hash table is byte-identical to round 1. The only table change is the #387 verdict row, plus one added saved-state table per page (`receipts/table_identity.txt`). The PR body's per-cycle and per-step tables equal the pages' tables (`receipts/pr_body_tables.txt`).
2. **Raw retention is real and stated.** Both pages state private cold storage keyed by their hash tables, and name the branch `b1-review-evidence` and the path `review-evidence/b1-r1/author-r2/` (599:335-347, 387:303-307). The PR body pins `04d00b66`, which is the branch tip.

   From the retained copy (`receipts/verify_retention.txt`):
   - all 100 page raw-artifact rows equal their retained file;
   - the 213 retained files equal the packet's raw index entry for entry (176,644,961 bytes);
   - the storage MANIFEST verifies 213/213, and its SHA-256 and TSV forms are byte-identical to the packet's `retention/`;
   - the TSV's page-row column names exactly the 100 rows;
   - all 181 per-action index entries match.

   The four previously unarchived claims are now reproduced, and my re-runs of the executor's extraction scripts against the retained raws and the seed build directories give output **byte-identical** to the archived outputs (`receipts/author_extract_rerun.txt`):
   - peer delay 0 / 4,039-4,701 / 373-389 ns;
   - 7,520 console rounds over nineteen actions;
   - alignment-test GPTP_GM_CHANGED 22/60;
   - the `asl` CRC `809fcffa`;
   - the saved-state extraction as well.

   My own independent code, sharing nothing with those scripts, reproduces the same values (`receipts/rederive_r2.txt` A, C, D, E, F).

   Only the dry-run and final raw consoles are public. A cold reader can re-derive those two (`receipts/public_subset.txt`: 80/80 each, pend 0 and 1), and that matches the extraction's per-action lines.
3. **The redacted author packet is clean.**
   - My `scrub_packet.py` harvests private tokens at run time from the retained raws and the unredacted round-1 tree. It finds 0 hits in `author-r2/` (275 files) and 0 in the two pages plus the live PR body.
   - `redaction_audit.py` checks all 245 records of `REDACTION.json`: 205 byte-identical, 30 redacted, 10 excluded. Every redaction changes only placeholder spans, so no measured value was altered. None of the replaced original values (account, interface names, capture-host MACs, controller-host EUI-64 and interface, tap driver) appears anywhere in `author-r2/`.
   - The manager's archiver path-redacted four of these files further. Its `MANIFEST.json` records both hashes, and every published file matches it at both archive commits: 235/235 at `92e1d7a3` and 321/321 at `04d00b66`, with none outside it (`receipts/archive_manifest.txt`).
   - The same scans find residues **outside** the author packet. They are listed under pending manager duties: one is my own round-1 receipt, the other is the old archive commit.
4. **Both restore sections record the saved-state layer.** They record start and end (slots 227/228 then 229/230, commits ok 0 then 2, `PP_STAT` `0x5b000444` then `0x5b000c44`, `PP_NVM_STAT` `0xc30000e4` then `0xc34000e4`). They give the cause derived from the captures, state that the records were not compared, and state the reset limitation (599:287-331, 387:266-291). The pages' derivation reproduces independently:
   - pend reads 0 through 05:38:28.99Z and 1 from 05:41:15.67Z to the end;
   - exactly six state-changing commands exist in the session: two CONNECT_RX and SET_CLOCK_SOURCE to source 1 in the setup (05:41:01.64Z), then SET_CLOCK_SOURCE to source 0 and two DISCONNECT_RX in the restore (06:22:05Z). My classifier enumerates every command of all 26 retained controller transcripts, and all the others are reads (GET_*, READ_DESCRIPTOR, stream-state reads). The console issued only reads;
   - nvm_dirty and the alarm read 0 in all 7,520 samples.

   "No commit fell inside a sampled action" is sound. The writer commits only after `nvm_dirty` has held for a whole 1,000 ms debounce window (`BAREMETAL_FIRMWARE.md:1925-1928`), and the largest console gap is 0.255 s. Ten link cycles produced no commit, which is consistent with a total of two.

   **Sticky `nvm_pend` after the SET_CLOCK_SOURCE writes matches the contract.**
   - Section 11 lists clock source, ids `0x0A`-`0x11`, with record writer NONE and "nvm_pend 1 until reset" (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1280,1283`). Section 6.1 has "dynamic fields still lack record writers. Their sticky sources therefore clear only at reset" (:992-993), and :277 has "No acknowledgement touches it".
   - The RTL agrees. `KL_aecp_dyn_state.sv:292` sets `dirty_o` on any non-IDENTIFY persisted write, :266 clears it only in reset, and `KL_pp_shadow.sv:958` ORs it into `nvm_pend_w`.
   - The materializer is not implemented (`SAVED_STATE_MATERIALIZATION.md:6`; #70 D3).
   - One precision note on the executor's report, which is in the PR body and REVIEW READY and not on the pages: `CHANGELOG.md:289-294` ("Only reset clears that source") describes the class-6/7 mark source. For class 1 it says only that `aecp_dyn_dirty_o` already publishes it (:290). The clock-source conclusion rests on section 11 and the RTL above, and it stands.
5. **R402-1 S1 is taken** at 599:100-102 and :219-221, and in the PR body's method notes. The wording is correct against `BAREMETAL_FIRMWARE.md:1971-1977` (250 ms publication bound, 125 ms trigger).

   The Markdown gates pass in the pinned environment: `cmarkgfm==2025.10.22` and `html5lib==1.1`, installed with `--require-hashes` from `tools/markdown/requirements.txt` (`receipts/gates.txt`, all rc 0):
   - `docs_check` 0 findings;
   - `check_doc_style` OK;
   - `gen_toc --check` OK;
   - `check_em_dash --base 13eda870` 0 findings over 792 lines, and its selftest 339 arms;
   - `check_doc_paths` OK over 854 paths;
   - `ci_scope --selftest` PASS;
   - `check_baremetal_only --check` 0 findings. It needs PyYAML, which the lock lacks, so it ran under the system interpreter;
   - `check_feature_status --self-test` 46/46;
   - `git diff --check` clean from both bases.

   38/38 page links and anchors resolve (`receipts/anchors.txt`).

## Findings

No BLOCKER, MAJOR or MINOR finding.

### Suggestions (optional; no effect on coverage)

- **S1 - Tests, Docs - `author-r2/extract/extract_saved_state.py` `mutating()`; `docs/findings/599_394_E1_LINK_CYCLES.md:298,305`.**
  - The classifier is a deny-list: ACMP 6/8, `SET_*`, and START/STOP_STREAMING. It would not flag ADD/REMOVE_AUDIO_MAPPINGS, which is the map-write source that :327 rules out.
  - The page attributes "Every other controller command in the session was a read" to that script.
  - The claim is true: `receipts/rederive_r2.txt` B enumerates every command kind in every retained transcript.
  - An allow-list of read commands, where anything else counts as state-changing, would let the archived script fail for that alternative.
- **S2 - Docs - 599:335, 387:303.** The pages name the branch and path, and leave the pinned commit to the PR body, as the round-2 ruling directs. The #600 page carries its archive commit in the page itself (`394_387_E1_SWITCH_CYCLES.md:389-393`), and this evidence branch has already been rewritten once. A page-level pin at the merge turn would make the page self-sufficient. This is the manager's choice.
- **S3 - Docs - PR body and REVIEW READY sticky-`nvm_pend` report.** Cite section 11 and the RTL for the clock-source source rather than `CHANGELOG.md:289-294` (see verdict item 4). This is text only, and the conclusion stands.

## Clean-lens evidence

- [R402] PASS Conformance - 387:12,:24,:106-115,:152,:175-234,:266-291; 599:90-102,:125-127,:218-221,:267,:287-331; live PR body; #599 comment 5885742531.
  - Checked against: #387 acceptance 4 and 5859048589; the #602 ruling; `GM_LOSS_RECOVERY.md` media re-base; round-2 rulings 1-5 (5885377252); `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:277,949-1007,1268-1304`; `CHANGELOG.md:275-309`; `REGISTER_MAP.md:1953-2002,2247,2253`; `BAREMETAL_FIRMWARE.md:1925-1928,1971-1977`.
  - Every ruled item is met, and the executor's sticky-pend report is correct.
  - #599 acceptance 4 and #394 acceptance 2 are unchanged. Their tables are byte-identical to the round R402-1 re-derived.
- [R402] PASS RTL - `hdl/milan/KL_pp_shadow.sv:905-958`; `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:255-292` at `c951a9ff`; `REGISTER_MAP.md:2247` PP_STAT[4,8,10,11] and `:2253` PP_NVM_STAT[23,22,8,7:2].
  - Every decode the new text uses was checked (`0x5b000444`/`0x5b000c44`, `0xc30000e4`/`0xc34000e4`), along with the sticky dyn-state source and its reset-only clear, against the text of 599:309-327.
  - The diff has no RTL, firmware or interface change (`git diff --stat 13eda870..931c3edf`: two pages).
- [R402] PASS Robustness - `receipts/rederive_r2.txt` (A, B, F); `receipts/verify_retention.txt`; `receipts/redaction_audit.txt`. Checked:
  - failure and edge paths of the saved-state derivation: commits failed 0, alarm 0 in all samples, unres 0 at the end, no name or map write, 0 state-changing commands inside any sampled action, and commit visibility against the 1,000 ms writer debounce;
  - the retention chain under a hash mismatch: the extractions exit 2 on a changed input (`receipts/mutation_probe.txt`);
  - that the redaction altered no measured value: redactions touch only placeholder spans.
- [R402] PASS Tests - `receipts/author_extract_rerun.txt` (5/5 byte-identical re-runs); `receipts/rederive_r2.txt` (independent code, 12 PASS, 0 FAIL); `receipts/verify_retention.txt`; `receipts/public_subset.txt`; `receipts/mutation_probe.txt` (7/7 planted defects killed across the executor's `extract_pdelay.py` and my six checks).
  - The first scrub probe planted a port-log line that carried no token, and it survived. The corrected probe plants a token-bearing line and kills it, and the receipt records that final run.
  - S1 above is a non-blocking classifier suggestion.
- [R402] PASS Docs - both pages, full text at the head; `receipts/gates.txt` (all rc 0); `receipts/anchors.txt` (38/38); `receipts/table_identity.txt`; `receipts/pr_body_tables.txt`; `receipts/privacy_scan.txt` (repository deny-list: 0 hits, apart from the public DUT, peer and null MACs and a clause number read as an IPv4 shape); `receipts/scrub_packet.txt` and `receipts/redaction_audit.txt` (author packet, pages and PR body clean).

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | as the PASS Conformance line: both pages, PR body, REVIEW READY, and the #387, #602 and #599 rulings and contracts listed there | R402-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| RTL | CLEAN | `KL_pp_shadow.sv:905-958`, `KL_aecp_dyn_state.sv:255-292` (`c951a9ff`), `REGISTER_MAP.md:2247,2253`, the diff stat | R402-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Robustness | CLEAN | `receipts/rederive_r2.txt`, `verify_retention.txt`, `redaction_audit.txt`, `mutation_probe.txt` | R402-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Tests | CLEAN | `author-r2/extract/*.py` re-run and diffed; independent `scripts/rederive_r2.py`; `public_subset.py`; `mutation_probe.sh` | R402-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Docs | CLEAN | both pages, PR body, `receipts/gates.txt`, `anchors.txt`, `table_identity.txt`, `pr_body_tables.txt`, `privacy_scan.txt`, `scrub_packet.txt` | R402-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |

## Prior public review findings (read after the draft verdict and ledger)

| Finding | Status at `931c3edf` | Evidence |
|---|---|---|
| R402-1 F1 MAJOR (#387 PASS) | RESOLVED | Verdict item 1 |
| R402-1 F2 MINOR (peer delay and `asl` CRC unarchived) | RESOLVED | Verdict item 2 |
| R402-1 F3 MINOR (saved-state residue) | RESOLVED | Verdict item 4; the non-comparison is stated, as ruling 4 requires |
| R402-1 S1 | TAKEN | Verdict item 5 |
| R402-1 S2 (raw captures not public) | Partly addressed, retained as a suggestion | Extractions are archived. Raws stay private, as ruling 2 allows |
| R402-1 S3 (interface name in the packet) | RESOLVED for the author packet | Verdict item 3 |
| R403-1 F1 MAJOR | RESOLVED | PARTLY MET; the 5 s claim is gone from the verdict row; CLOCK_DOMAIN is reconciled at 387:192-194; #621 is linked at :12 and :232 |
| R403-1 F2 MAJOR | RESOLVED under ruling 2 | Retention verified; the pages state the storage and path; the commit is pinned in the PR body (see S2) |
| R403-1 F3 MINOR | RESOLVED for `author-r2/` | 0 private-token hits; residues elsewhere are listed under manager duties |
| R403-1 F4 MINOR | RESOLVED under ruling 4 | The difference is recorded with its cause. The owner decision on an issue rests with the manager |
| R403-1 S1, S3, S4 | Retained as suggestions, not taken | S3's wording is unchanged at 387:202. The S4 index is a manager duty |
| R403-1 S2 | TAKEN | Same as R402-1 S1 |

## Receipts and reproduction

All paths are relative to this packet. `<raw-storage>` is the private retention directory (it holds `raw/` and the manifests), and `<seed-builds>` is the builder's directory of seed builds. Neither location is published. `<packet>` is `review-evidence/b1-r1` at `04d00b66`, and `<r1-archive>` is `review-evidence/b1-r1` at `92e1d7a3`.

- `scripts/verify_retention.py <raw-storage> <clone> <packet>/author-r2` produces `receipts/verify_retention.txt`.
- `scripts/rederive_r2.py <raw-storage>/raw <clone> <packet>/author-r2` produces `receipts/rederive_r2.txt`.
- `receipts/author_extract_rerun.txt` records the executor's five `extract_*.py` scripts, run unchanged against `<raw-storage>/raw`, the clone and `<seed-builds>`, with each output compared byte for byte to the archived `.txt`. The `asl` build log names the working directory `build-dev-13eda870d1a6`. That worktree's HEAD reads `13eda870d1a6cf3f946fc228a98862366b08d102` and is clean.
- `scripts/public_subset.py <packet>/author-r2` produces `receipts/public_subset.txt`.
- `scripts/scrub_packet.py --repo <clone> --private <raw-storage>/raw --private <r1-archive> --target ...` produces `receipts/scrub_packet.txt`. Tokens are labelled only through a keyed digest whose key is discarded, so no hash of a private value is published.
- The same scrub run over this packet's own publishable files (this report, `scripts/`, `receipts/`) gives 0 hits (`receipts/self_scrub.txt`).
- `scripts/redaction_audit.py <r1-archive> <packet>` produces `receipts/redaction_audit.txt`. Its exit status is 1 only because of the two R402-1 files named under manager duties.
- `scripts/archive_manifest.py 92e1d7a3=<r1-archive> 04d00b66=<packet>`, `scripts/table_identity.py <clone> f9eab5bf 931c3edf`, `scripts/pr_body_tables.py`, `scripts/check_anchors.py`, `scripts/privacy_scan.py`, `scripts/run_gates.sh` and `scripts/mutation_probe.sh` produce their same-named receipts.
- `scripts/verify_clone.sh` produces `receipts/verify_clone.txt`:
  - HEAD and tree are exact;
  - the index writes the tree;
  - all 966 entries match in bytes and mode;
  - the gitlinks are `gptp-processor` 5dce647a, `protocol-processor` c951a9ff and `third_party/verilog-axis` 48ff7a7e. `external` (efeb541a) is uninitialised and unchanged;
  - there are no untracked or ignored files.

  It ran after every probe. All probes worked on disposable copies in the packet's unpublished scratch directory.
- `receipts/hosted_checks.txt` is a snapshot at 07:51:52Z.
  - Executed and green: `rtl-fast`, `changes`, `full-ci-gate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3.
  - In progress: `docs-check`, `elaborate`, and Verilator shards 1, 2 and 4.
  - Skipped, which is not evidence: Physical gPTP.

## Real limits

- The per-action raw captures are private. I read the retained copies read-only to re-run the extractions. A cold public reader can re-derive only the dry-run and final consoles.
- The tap and controller-port pcaps were not re-decoded this round. The wire-derived tables are byte-identical to round 1, where they were re-derived from the archived analyses.
- The `asl` build is tied to `13eda870` by its directory name, by its build log's working directory, and by that worktree's current HEAD. It was not rebuilt.
- The persisted binding records were not read back; no bench access was allowed. The pages say the same.
- The scrub harvest covers MACs, EUI-64 identities, interface-shaped names, accounts seen in paths, listings or prompts, and the local host name. It cannot know a bench host name that appears in no private source. The redaction audit closes that gap for every class the executor redacted, including the tap driver name.
- The scoped simulator was not used, because the diff has no RTL, so its identity was not checked.
- Physical calibration NOT RUN. No hardware was touched. Skipped hosted contexts are not hardware or simulation proof.

## Pending manager duties

1. **Redact my own R402-1 publication.** The controller host's MAC-derived clock identity appears in `review-evidence/b1-r1/reviews/R402-1/receipts/rederive.txt` (11 scrub hits) and `reviews/R402-1/scripts/rederive.py` (1) at `04d00b66`, and in branch history from `9660f03`. This was a defect in my round-1 packet, not in the PR. The author packet does not carry it.
2. **The unredacted round-1 author packet is still publicly fetchable by SHA.** This round fetched `92e1d7a3` from the public repository by its SHA. It still holds 249 private-token hits (`receipts/scrub_packet.txt`): the controller host's clock identity and interface name, two capture-host MACs, the capture-host interface and an account name. The round-2 assignment and this review's brief still link it. Removing the branch reference does not delete the object. Decide on a purge request or accepted exposure, and stop citing that URL.
3. Decide on an issue for the sticky `nvm_pend` from the executor's report. It is contract-conformant, and the gap is #70 D3. The lane now on the bench inherits pend 1 until a reset.
4. Own hosted and act acceptance at this head. `docs-check`, `elaborate` and three Verilator shards were still running at the snapshot.
5. Build and validate the current-dev candidate at the merge turn: source base `13eda870`, live dev `57b8c867`.
6. Route the `docs/findings/README.md` index entries (R403-1 S4). Consider S2.
7. Obtain R403-2. A merge needs maintainer authorization.
8. Publish only `REPORT.md` and the files listed in `MANIFEST.sha256`.

R402-2 FINISHED
