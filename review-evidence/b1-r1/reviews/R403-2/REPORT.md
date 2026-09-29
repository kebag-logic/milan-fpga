[R403] NEGATIVE - exact head 931c3edfced972e01356cd989b5092a1672de5a3

# R403-2: external delta review of PR #620 (issue #599, with #394 and #387)

- Reviewer: [R403], external, cleared context. Round R403-2.
- Exact head `931c3edfced972e01356cd989b5092a1672de5a3`, tree `56f7cdcd078625cbf8172aa73693a075b0164d4a`. It adds one docs commit to round 1's `f9eab5bf55ca4471e6e48ae3d38018d7e804505b`. The source base is dev `13eda870d1a6cf3f946fc228a98862366b08d102`.
- Delta `f9eab5bf..931c3edf`: `docs/findings/387_SOFTWARE_GM_STEP.md` (+71/-11) and `docs/findings/599_394_E1_LINK_CYCLES.md` (+72/-11). No RTL, firmware, script or other document changes.
- Evidence judged:
  - the public packet `review-evidence/b1-r1/author-r2/` at the pinned commit `04d00b6693315d2b14a6c6b51b681a3136b550c2` on branch `b1-review-evidence` (275 files, all equal to the archive's `MANIFEST.json`);
  - for comparison only, the purged round-1 packet, fetched by SHA as `92e1d7a3c815dbf70faa8f0975cc063040edd967`. Its contents stay in the reviewer's unpublished scratch area.
- Reconstruction order:
  - AGENTS.md and CONTRIBUTING.md;
  - `docs/README.md` and `docs/findings/README.md`;
  - the issue bodies #599, #394 and #387;
  - the round-2 assignment ([5885377252](https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885377252)), the executor's TAKEN and REVIEW READY (5885391766, 5885742531) and #621;
  - the interface authorities: SAVED_STATE_SNAPSHOT_OWNERSHIP.md (sections 3, 6.1 and 11), `CHANGELOG.md` release `0x0002_0060`, REGISTER_MAP.md (`PP_STAT`, `PP_NVM_STAT` and `0x8DC`), GM_LOSS_RECOVERY.md "Media re-base on a PHC step", and TESTING.md 6b;
  - the RTL behind the saved-state claims;
  - then the diff and its history, then the packet.
- My own round-1 findings (R403-1) are resolved or retained below. The other public round-1 review's findings (R402-1) were read only after this verdict and ledger were written; they are resolved or retained in their own section.

## Verdict summary

Every assigned item is met at this head.

- #387 acceptance 4 now reads PARTLY MET everywhere, with every gap named.
- The measurement tables are byte-identical to round 1.
- The retention and public-packet statements are present, and the retention manifest closes over all 213 raw files and all 100 page rows.
- The four previously unarchived claims each have an archived extraction script and its output. The parts I could re-run from public byte-identical inputs match.
- The author packet is clean of every real leaked token.
- Both restore sections record the saved-state layer. The sticky `nvm_pend` matches the contract and the RTL.
- The Markdown gates pass in the pinned environment.

The round is NEGATIVE for one MINOR finding outside the author's diff. The public evidence commit that the PR body pins still carries the controller host's MAC-derived clock identity, in another reviewer's round-1 receipts. The purged round-1 packet is still publicly fetchable by SHA (F5). Both are manager-owned archive fixes: neither needs a new head, and neither un-covers any lens banked here.

## Answers to the assigned questions

1. **#387 acceptance 4 is PARTLY MET everywhere, with every gap named.**
   - Where it says so: the verdict row (`387:12`), the contract-check conclusion (`387:186-194`), the renamed deviation section (`387:196-234`), the PR body (verdict table and Round 2 F1) and REVIEW READY 5885742531.
   - The gaps are named in each place:
     - `tu` is signalled 2-3 times per step against one counted event;
     - asCapable is lost for 2.0 s per step, linked to [#621](https://github.com/kebag-logic/milan-fpga/issues/621), which exists and is open;
     - DUT GPTP_GM_CHANGED rises +3 per edge;
     - the counted render re-base is not observable (`387:106-115`).
   - What would make the re-base observable is stated: an AAF stream bound into the render stage across each step, and the recentre count published on a register or console command. That matches REGISTER_MAP.md:2000 ("recentre counters remain separate verification taps").
   - The bound sentence is consistent. The verdict row says "Item 2 sets no time bound", the contract row `387:184` says "No time bound in item 2", and `387:152` calls the 5 s bound context. The round-1 "inside the 5 s bound" is gone from the verdict row.
   - "Media never unlocked" is reconciled with the CLOCK_DOMAIN UNLOCKED counts (`387:192-194`).
   - Independent checks (`receipts/gm_changed_per_edge.txt`, from the archived analyses):
     - GPTP_GM_CHANGED is +3 at nine edges and +1 at run 4's takeover, against exactly one console and one wire grandmaster change per edge.
     - CLOCK_DOMAIN UNLOCKED per edge is 3/3, 2/3, 3/3, 2/3 and 3/3. That equals the page's `tu` episodes column edge for edge, so the claim "UNLOCKED with each `tu` episode" holds.
   - **The tables are byte-identical** (`receipts/table_diff.txt`):
     - 13 of the 14 round-1 tables are unchanged byte for byte. That covers every measurement, counter, contract, identity and hash table on both pages.
     - The only changed row is the #387 verdict row.
     - The only additions are the two saved-state tables.
     - The PR body's per-cycle and per-step tables are byte-identical to the pages' (`receipts/prbody_tables.txt`). Only its verdict rows are paraphrased.
   - `scripts/rederive.py` (round 1's, unchanged) re-derives every page cell at this head from the republished analyses with **DIFFS: none** (`receipts/rederive_931c3edf.txt`).
2. **Raw retention and the four claims.**
   - Both pages state private cold storage keyed by their hash tables, name the branch and path of the public packet, and say PR #620 records its pinned commit (`599:333-349`, `387:299-307`). The PR body pins `04d00b66`.
   - `scripts/check_retention.py` (`receipts/check_retention.txt`):
     - the retention manifest has 213 entries, all equal in bytes and SHA-256 to the raw index and to `retention/MANIFEST.sha256`;
     - its 100 page-row tags are exactly the pages' 100 raw rows, each with the right page and line;
     - there are 0 mismatches.
   - The private copies themselves were not read (manager duty).
   - The four claims each have an archived script and its output, and each output hash-checks its inputs against the page rows and the raw index:
     - peer delay: `extract_pdelay`;
     - 7,520 console rounds: `extract_console_rounds`;
     - alignment counters 22/60: `extract_alignment_counters`;
     - `asl` `809fcffa`: `extract_seed_crc`.
   - The arithmetic is consistent:
     - 80 + 440 + 120 + 10 × 440 + 5 × 480 + 80 = 7,520 rounds over 19 actions;
     - the peer-delay samples split as 2,359 + 41 = 2,400 = 5 × 480;
     - the page's new "held for four or five samples" matches the output (4 at nine clears, 5 at run 2's takeover).
   - **Re-run** (`scripts/rerun_extractions.py`, `receipts/rerun_extractions.txt`):
     - Only 10 of the 50 extraction inputs survive publicly byte-identical: the dryrun and final consoles, three controller transcripts, and five gm event logs.
     - On those, the author's own code, restricted only by patching its action lists, reproduces the archived per-action lines exactly: console rounds dryrun 80/80 and final 80/80; saved-state dryrun and final, both readbacks, and the baseline-bound DUT binding.
     - Negative controls on disposable copies all behave. A one-byte tamper is refused with exit 2. A flipped `link_status` word is reported (79/80, DISAGREE). Injected CONNECT_RX and SET_NAME records are counted as state-changing.
     - An injected ADD_AUDIO_MAPPINGS is not counted (S5). The claim it would support still holds by construction: the controller reader's allowlist permits only reads, and the actions tool adds only SET_CLOCK_SOURCE, CONNECT_RX and DISCONNECT_RX (`r1/tools/avdecc_ro.py:40-50`, `r1/tools/a438_controller.py`).
     - The rest is not re-runnable publicly, and nothing hash-checked contradicts it. That covers 40 inputs, and the `asl` build directory, which is tied to dev `13eda870` by name only (S7).
3. **Redaction.** The purged round-1 packet was used as a positive control; the scanner finds 255 hits across eight token forms in it.
   - Two scans over the redacted packet `author-r2/` at `04d00b66`:
     - `scripts/scrub_packet.py` (round 1's, byte-identical, SHA-256 `7408e309...`): the repository scrub finds 0 on 275 files and 2 pages. No interface name, host MAC or home path is reported. The only MACs are the public loopback, DUT and peer ones. The one file-listing line is redacted to `<account>` (`receipts/scrub_packet_author_r2.txt`, rc 0).
     - `scripts/scan_private_tokens.py`: the real leaked values from the purged round-1 packet are held in unpublished scratch, in all their forms (colon, bare, dash, `enx`, EUI-64 bare, dotted and colon). It finds **0 hits** in `author-r2/` and 0 in both pages plus the live PR body (`receipts/private_tokens_author_r2.txt`, `receipts/private_tokens_pages_prbody.txt`).
   - The redaction chain closes:
     - Every `r1/REDACTION.json` original hash equals the purged file.
     - Every published hash equals the republished file or, for four files, the input of the manager's path redaction, whose output `MANIFEST.json` records.
     - All 275 packet files equal `MANIFEST.json`.
   - **Outside the author packet, the same commit is not clean** (F5). `review-evidence/b1-r1/reviews/R402-1/receipts/rederive.txt` carries the controller host's MAC-derived clock identity 11 times (`receipts/private_tokens_whole_evidence_tree.txt`). The purged commit `92e1d7a3` also still serves every round-1 token by SHA.
4. **Saved-state layer: recorded, derived and consistent with the contract.**
   - Both restore sections carry the table: slots 227/228 to 229/230, commits ok 0 to 2, `PP_STAT` `nvm_pend` 0 to 1 and `PP_NVM_STAT` `0xc30000e4` to `0xc34000e4` (`599:287-331`, `387:266-291`).
   - Both bit decodes are right: bit 11 in `PP_STAT` (`0x800`) and bit 22 in `PP_NVM_STAT` (`0x400000`), per REGISTER_MAP.md:2247 and :2253. `unres` bit 23, the open-record flag, is 0 at both ends.
   - The cause is derived from the captures in time order. The six state-changing commands, their times and the pend edge between 05:38:29Z and 05:41:16Z match the archived output. The page rounds the times correctly.
   - The not-compared statement (`599:329`, `387:289`) and the reset limitation (`599:331`, `387:291`) are present.
   - **The sticky `nvm_pend` matches the contract.**
     - The clock-source records 0x0A-0x11 have no record writer and publish "nvm_pend 1 until reset" (SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1283; :992-993; :999 "NOTHING ELSE affects it: no ACK, RELEASE, commit"; :277 "No acknowledgement touches it").
     - The binding records 0x20-0x2F are the only writer (:1285).
     - In RTL, `KL_aecp_dyn_state.sv:292` sets `dirty_o` on any persisted-field write except IDENTIFY, and only reset clears it (:266). `KL_pp_shadow.sv:958-959` ORs that level into `nvm_pend`.
     - So both SET_CLOCK_SOURCE writes leave pend at 1, and two successful binding commits cannot clear it.
     - `CHANGELOG.md:289-299` (release `0x0002_0060`) states the same reset-only rule for the name and map marks. It notes (:290) that the dynamic-state level already published class 1, and it keeps donor scope D3 (materialization) open.
     - The commit-order attribution (bind 229, unbind 230) is an inference from alternating slots and a count of two, and the page says so (`599:317`).
5. **R402-1 S1 is taken.**
   - `599:100-102` now reads: a published edge lies inside the 0.25 s console bracket, and the physical edge may precede it by up to the 250 ms publication bound. `599:219-221` gives the same per cycle.
   - That is correct against BAREMETAL_FIRMWARE.md's 125 ms poll and 250 ms publication bound, and it also answers my round-1 S2.
   - The Markdown gates pass in the pinned environment (see Validation).

## Findings

### F5: MINOR (Docs, Conformance). The pinned public evidence commit still publishes a host identity, and the purged round-1 packet is still served

- **Where:**
  - the archive at `04d00b6693315d2b14a6c6b51b681a3136b550c2` (pinned in the PR body), file `review-evidence/b1-r1/reviews/R402-1/receipts/rederive.txt`, lines 322, 323, 366, 367 and seven more;
  - the unreachable commit `92e1d7a3c815dbf70faa8f0975cc063040edd967`, which the branch rewrite removed from `b1-review-evidence` (GitHub compare: diverged from `04d00b66`) but which still fetches by SHA.
- **Authority:**
  - CONTRIBUTING.md section 6 (no bench-identifying information);
  - round-2 assignment ruling 3, which lists the "MAC-derived clock identity of the controller or capture host" among what must not be published;
  - the assignment's own statement that the round-1 packet was removed from the public branch;
  - my R403-1 F3 (MINOR, same class).
- **Evidence:**
  - `receipts/private_tokens_whole_evidence_tree.txt`: 11 hits of the controller host's EUI-64, the bare form of its NIC MAC, in that reviewer receipt. The author packet has 0.
  - `receipts/private_tokens_control_purged_92e1d7a3.txt`: 255 hits in the purged commit, fetched this round with a plain by-SHA fetch. They cover both host interface names, the account name, the tap driver name, both capture-host NIC MACs and the controller host's identity.
  - The manager's `MANIFEST.json` marks that receipt only `path_redacted`, so its EUI-64 shape was not covered.
- **Impact:** the host identity the ruling withholds is still on the commit the PR cites as its public evidence, and every round-1 token remains retrievable. This does not touch the pages, the head or any measurement.
- **Required outcome (manager-owned; no new head needed):**
  - (a) Re-archive the evidence branch with the controller-host identity redacted from the reviewer receipts too, and re-pin the PR body.
  - (b) Record the by-SHA exposure of `92e1d7a3`: request GitHub-side removal of the unreachable objects, or record an owner acceptance of the residual. Stop citing that SHA as current evidence.
- **Verification:** `scripts/scan_private_tokens.py` over the whole `review-evidence/` tree at the new pin gives 0 hits, and a public record exists for (b).

### Suggestions (non-blocking; do not affect coverage)

- **S5 (Tests):** `author-r2/extract/extract_saved_state.py` `mutating()`.
  - It counts ACMP 6/8 and AECP commands named `SET_*` or START/STOP_STREAMING. It would miss ADD/REMOVE_AUDIO_MAPPINGS, ACQUIRE/LOCK_ENTITY and WRITE_DESCRIPTOR (probe N3).
  - The page claim "every other controller command was a read" holds today through the read-only allowlist.
  - Asserting that every answer's command is in that allowlist would make the extraction self-checking.
- **S6 (Docs):** `599:354` and `387:317,319`. The `b1_analyze.py` and `phc_restore.py` hash rows are pre-redaction values. The packet copies now hash `464f92e7...` and `39ec5379...`, and only `r1/REDACTION.json` maps them. One sentence on the pages would spare a cold reader a false mismatch.
- **S7 (Docs):** `599:347`. "From hashed inputs" is exact for the console claims, whose inputs match pre-recorded rows. For the `asl` CRC, the build directory's hashes are recorded only by the extraction itself, and the directory is tied to `13eda870` by name, as the REVIEW READY says. A qualifier on the page would match that.
- **Retained from R403-1, not taken (outside the rulings):**
  - S1 (Tests): the per-action verdict scripts still do not assert the acceptance predicates.
  - S3 (Docs): `387:202` "0.22-0.97 s" is measured from the bracket end; it reaches 1.25 s from the bracket start (run 3 takeover, `receipts/rederive_931c3edf.txt`).
  - S4 (Docs, manager): `docs/findings/README.md` still indexes neither page.
  - S2 is answered by the R402-1 S1 wording.

## Resolution of my round-1 findings (R403-1, head `f9eab5bf`)

| Finding | Status at `931c3edf` | Evidence |
|---|---|---|
| F1 MAJOR (Conformance, Docs): #387 acceptance 4 labelled PASS | **Resolved** | Question 1: PARTLY MET with every gap in all four places. Bound sentence reconciled; CLOCK_DOMAIN reconciled; #621 linked. Tables byte-identical |
| F2 MAJOR (Conformance, Tests, Docs): raw captures unretained, archive unlinked, four claims unarchived | **Resolved** | Question 2: retention stated and manifest closure 0 mismatches. Packet branch, path and pin present. Four claims each have script and output, with a public partial re-run matching |
| F3 MINOR (Docs, Conformance): bench-identifying tokens in the archive | **Resolved for the author packet**; the residual on the same public commit and the purged SHA are carried forward as **F5** | Question 3 |
| F4 MINOR (Robustness, Conformance, Docs): saved-state layer omitted | **Resolved** | Question 4. The difference is recorded with its cause, the non-comparison and the reset limit; the manager owns the issue decision |

## Resolution of the other public round-1 review's findings (R402-1)

I read [R402-1](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5885301111) (at head `f9eab5bf`) after the verdict and ledger above were written. Nothing in it changes them.

| Finding | Status at `931c3edf` | Evidence |
|---|---|---|
| F1 MAJOR (Conformance, Docs): #387 acceptance 4 recorded as PASS | **Resolved** | Question 1. Both named gaps are present (`tu` 2-3 times per step; render re-base not observed), and the bound sentence is consistent. `387:24` no longer calls the loss "the one behaviour outside the contract"; it is now the departure from the one-counted-event contract. Tables byte-identical |
| F2 MINOR (Tests, Docs): peer-delay values and `asl` CRC unarchived | **Resolved** | Question 2: `extract_pdelay` and `extract_seed_crc` with outputs. The `asl` line now exists in the packet. The residual name-only binding of the `asl` directory is S7, a suggestion |
| F3 MINOR (Conformance, Docs): DUT saved-state residue left out; "never ... flashed" | **Resolved** | Question 4. `599:125-127` now reads "The bench never rebooted, flashed or power-cycled the DUT. Its own saved-state writer committed twice". Its required "equal or benign" statement is superseded by ruling 4, which requires stating plainly that the records were not compared; both pages do |
| S1 (Docs): publication-bound wording | **Taken** | `599:100-102`, `:219-221` |
| S2 (Tests): raw only as hashes; no generator for `summary/page-*.md` | Raw part answered by the private retention and extraction scripts. The generator part is **retained** as a suggestion, not addressed in round 2 | `author-r2/r1/summary/` unchanged |
| S3 (Docs): controller-host interface name on 55 packet lines | **Resolved** in the author packet (0 hits, question 3). The same review's own receipts on the pinned commit carry the controller host's clock identity; that residual is F5 | `receipts/private_tokens_whole_evidence_tree.txt` |

## Reviewer-owned completion ledger (this round)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5 MINOR) | `387:12`, `:106-115`, `:152`, `:175-234`; `599:94-102`, `:219-221`, `:267`, `:287-331` against #387 acceptance 4, the manager statement 5859048589, the #602 ruling, GM_LOSS_RECOVERY.md "Media re-base on a PHC step" and the round-2 rulings; `receipts/table_diff.txt`, `gm_changed_per_edge.txt`, `rederive_931c3edf.txt`; the public archive at `04d00b66` for the privacy rule | R403-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| RTL | CLEAN | No RTL in the diff. The pages' saved-state claims were checked against `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:266,292`, `hdl/milan/KL_pp_shadow.sv:958-959`, REGISTER_MAP.md:2247 (`PP_STAT[11]`) and :2253 (`PP_NVM_STAT[22]`, `[23]`), and SAVED_STATE_SNAPSHOT_OWNERSHIP.md:992-999 and :1283-1285. The render-tap claim was checked against REGISTER_MAP.md:1953-2003. All match | R403-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Robustness | CLEAN | The restore and reset paths: `599:265-331` and `387:248-297` against the readbacks `r1/identity/console-identity.txt` and `r1/restore/console-final.txt` (re-read by the author's code, matching). The per-action `PP_STAT` pend/dirty/alarm continuity from the re-run. The polled DUT binding continuity. The reset limitation and the not-compared residual are disclosed | R403-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Tests | CLEAN (S5 suggestion only) | `author-r2/extract/*.py` and their outputs; the partial re-run with negative controls N1-N3 (`receipts/rerun_extractions.txt`); `author-r2/retention/*` closure (`receipts/check_retention.txt`); round 1's `rederive.py` at this head (DIFFS none) | R403-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Docs | UNCLEAN (F5 MINOR) | Both pages in full at this head; the live PR body; REVIEW READY 5885742531. The pinned-environment gates (`receipts/md_gates.txt`, all rc 0). 34 in-repo anchors resolved (`receipts/check_anchors.txt`). The scrub and token scans over the pages, the PR body and the archive | R403-2 | 931c3edfced972e01356cd989b5092a1672de5a3 |

## Validation run by the reviewer (foreground; rc as recorded in receipts)

- **Pinned Markdown environment:** a private virtual environment installed with `--require-hashes` from `tools/markdown/requirements.txt`: cmarkgfm 2025.10.22, html5lib 1.1, CPython 3.14.7 (`receipts/md_env.txt`). All of the following returned rc 0 (`receipts/md_gates.txt`):
  - `docs_check.py`: 0 findings over 176 md files and 938 scrubbed files; self-test 23/23 and 4/4.
  - `check_doc_style.py`.
  - `gen_toc.py --check`.
  - `check_em_dash.py`: 0 findings with base `13eda870` (792 added lines) and with base `f9eab5bf` (143 added lines).
  - `check_doc_paths.py`: 854 paths.
  - `check_feature_status.py --self-test`: 46/46.
  - `ci_scope.py --selftest`.
  - `git diff --check` from both bases.
- `check_baremetal_only.py --check` needs PyYAML, which the Markdown environment lacks (rc 2 there). It returned rc 0 under the system CPython (0 findings over 936 files).
- **Reviewer probes:**
  - `table_diff.py`;
  - `rederive.py`: DIFFS none;
  - `gm_changed_per_edge.py`;
  - `check_retention.py`: 0 mismatches;
  - `rerun_extractions.py`: 10 of 50 inputs covered, every comparable line MATCH, N1-N3 as reported;
  - `scrub_packet.py`: rc 0;
  - `scan_private_tokens.py`: positive control 255 hits; author packet 0; pages and PR body 0; whole evidence tree 11;
  - `check_anchors.py`: 34 resolved, 0 unresolved;
  - `verify_clone.sh`: 962 tracked blobs re-hashed from disk, 0 differ; no residue. Gitlinks `external` efeb541a (not initialised), `gptp-processor` 5dce647a, `protocol-processor` c951a9ff and `third_party/verilog-axis` 48ff7a7e, each at stage 0 and clean.
- **Hosted exact-head contexts, read-only** (`receipts/hosted_checks_931c3edf.tsv`; the manager owns hosted acceptance):
  - success: rtl-fast, changes, full-ci-gate, docs-check-no-git, wire-accountability, bdd-conformance, verilator-lint, yosys-elaboration, Yosys shards 0-3 and Verilator shard 3/5;
  - in progress at read time: docs-check, elaborate, Verilator shards 0, 1, 2 and 4;
  - skipped: Physical gPTP (nightly and manual), which is not hardware proof.

## Real limits

- Physical calibration was NOT RUN. Field skips are not hardware proof. No bench access was used.
- 40 of the 50 extraction inputs and all 213 retained raw copies are private. Those claims are judged from the author's archived, hash-stamped outputs plus the retention closure; they were not re-run.
- The `asl` seed CRC rests on a build directory seen only by the extraction.
- The persisted NVM records were not read back by anyone. Page and reviewer agree they are not compared with the found state.
- The manager's full source, static, builder and native banks at this head were stated in the assignment. I did not find them in a separate public comment and did not re-run them. Source validation is distinct from the final current-dev candidate.
- The only objects fetched were the evidence branch, as a shallow scratch clone, and `92e1d7a3` into that scratch clone. The review clone's refs, index and worktree are unchanged.

## Pending manager duties

- F5: re-redact the reviewer receipts on `b1-review-evidence`, re-pin the PR body, and record the by-SHA exposure of `92e1d7a3`.
- Confirm the private cold-storage copies against `author-r2/retention/MANIFEST.sha256`.
- Decide the sticky-`nvm_pend` issue. The next lane inherits pend 1 until a reset.
- Hosted and local-replica acceptance at the exact head, including the contexts still in progress at read time.
- The final current-dev candidate build: source base `13eda870`, live dev `57b8c867`.
- The findings index entry (S4).

R403-2 FINISHED
