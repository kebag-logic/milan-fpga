[R361] POSITIVE - exact head 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1

Round R361-2 is the external independent re-review of PR #600 (Refs #394, Refs #387). It covers the delta `fddc58e4..6f2cdab6` and the whole PR at this head.

- **Head:** tree `705d9ab5dd1c6603af7de11abe21ddfcad47d1ff`, two commits on source base `2a2a7bb655e528edc3087c88033cd3a47546feb4`. Both messages are one line with no trailers (`receipts/range-log.txt`).
- **Scope:** the PR changes only `docs/findings/394_387_E1_SWITCH_CYCLES.md`. The round-2 commit changes it by +70/-22 in 20 hunks (`receipts/delta-fddc58e4-6f2cdab6.diff`, `receipts/delta-hunks.txt`).
- **Result:** all five lenses were applied at this head.
  - No BLOCKER, MAJOR or MINOR finding is open.
  - All four of this reviewer's round-1 findings are resolved: F1 MAJOR and F2-F4 MINOR.
  - All four of the other round-1 review's findings (R360-1) are resolved.
  - Two SUGGESTIONs remain. They do not affect coverage.
- **Verdict order:** the verdict and ledger were fixed in a draft before the other reviewer's report was read. Draft sha256: `10549136f691138dccd3ba6585b55ef1fd7977af6420d597fd4efa04620ae99e`. Reading that report changed neither.

Reconstructed from public state, in this order:

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- #394:
  - the body;
  - owner decisions 5789765478, 5810503583 and 5857769804;
  - bench assignment 5858215210 and manager note 5858862351;
  - round-2 assignment 5859045504;
  - [A378] TAKEN 5859056617 and REVIEW READY 5859147312.
- #387: the body, decisions 5606198212, 5794731090, 5810378282 and 5816509317, and the manager's acceptance-4 status 5859048589. #599 (title and state).
- The authorities:
  - `docs/design/GM_LOSS_RECOVERY.md:88-208` and `docs/design/TIME_SYNC.md:76-132`;
  - `sw/litex/milan_soc.py:1761-1811`;
  - `hdl/milan/milan_datapath.sv:2904-2914` and `:3430-3514`;
  - `hdl/common/KL_link_guard.sv:30-60`;
  - `docs/reference/REGISTER_MAP.md:405,734,736,2027`.
- The base..head and delta diffs, then the history.
- The public archive `review-evidence/394-387-r1` at `8f983d245a12e18a47ced37904d405b624c7e024`. All 166 blobs were fetched and each was checked against its git object id (`fetch_archive.py`, `receipts/archive-fetch.txt`).
- The PR body at this head (`receipts/pr600-body-at-review.txt`) and the hosted check runs at this head.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### S1 - SUGGESTION - Conformance, Docs - the stated #387 stimulus should require a stepping grandmaster change

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:11` and `:347-349`.
- **Authority:** `docs/design/TIME_SYNC.md:81-89`.
  - A locked servo slews offsets up to 100 us and steps only above that.
  - "A grandmaster change keeps the servo locked."
- **Why it matters:** a grandmaster change within 100 us of local time produces no PHC step. With no step, there is no counted `tu`/`mr`/MEDIA_RESET event of the kind `GM_LOSS_RECOVERY.md:142-160` defines. The stated stimulus, "a grandmaster change while a locked CRF stream keeps running", could therefore be met without exercising acceptance 4.
- **Why this is only a suggestion:**
  - `:349` ("the step's counted media event") implies a step.
  - The wording follows the manager's decision.
  - #387 5859048589 leaves the stimulus itself to be decided.
- **Suggested outcome:** when the running-stream stimulus is decided, require the new grandmaster's offset to exceed 100 us, so the policy steps.
- **Verification:** the decided stimulus names the offset condition.

### S2 - SUGGESTION (carried from R361-1 S2) - Docs - the "GM return / PHC step" column mixes clocks

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:235-246`, cycles 2, 5, 6, 7, 8 and 10.
- **Issue:** the step bracket opens 0.06-0.15 s before the GM return. That is inside the stated 0.15 s half-round-trip bound.
- **Suggested outcome:** one sentence saying the usable bracket starts at the GM return.
- **Status:** optional. The round-2 assignment forbade other page changes, so leaving it untouched was correct.

## Verification of the round-2 focus items

### (1) The per-cycle table renders

`table_probe.py` uses the repository's pinned renderer, installed in an isolated environment from `tools/markdown/requirements.txt` with `--require-hashes` (`receipts/table-probe.txt`).

- **At this head:** 6 tables render. The per-cycle table has 9 header cells and 10 body rows of 9 cells each. The raw source lines `:235-246` all have 9 cells.
- **Control at the prior head `fddc58e4`:** only 5 tables render, and the per-cycle table is missing. Its delimiter row has 10 cells.
- The ten body rows are byte-identical to the prior head. The delta changes only the header and delimiter rows of this table.

### (2) The link-counter text

- **MAC_STATUS (`:185-187`):** "DUT MAC_STATUS stayed at its software-published reset value, `0x0d`. Nothing in this build writes it (#599)."
  - `sw/litex/milan_soc.py:1782-1797` sets the reset to link_up 1, speed 2 and full_duplex 1, which is `0x0d`.
  - No `link_status` writer exists under `sw/` outside that file.
  - The archive's `mac_status` is `[13]` in all ten cycles (`receipts/step-context-check.txt`).
- **The counters (`:284`):** "Whatever the PHY did, this status cannot advance LINK_UP/LINK_DOWN."
- **The PHY link (`:189-191`, `:290`):** whether the DUT PHY link dropped was not observed, and the inline capture point may hold that link up.
- **Removed sentence:** the "This run never wrote that status" sentence is gone (hunk `@@ -260`).
- **The FAIL stays:** the #394 acceptance 2 FAIL remains at `:10` and `:298`.
- **The page is more precise than the assignment wording, and correctly so.**
  - LINK_UP/LINK_DOWN count edges of `eff_link_w`.
    - `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` (`hdl/milan/milan_datapath.sv:2904-2905`).
    - The edges are counted at `:3472-3494` and served at `:3513-3514`.
  - So the link guard's RX-clock-alive veto could still move the counters even with MAC_STATUS constant.
  - The page says so (`:286`). It also says neither `LINKG_STAT` (0x774) nor `LINK_CTRL` (0x71C) was sampled (`:288`).
  - The archive's console poll set confirms both were absent. It is `0x110, 0x720, 0x750, 0x764, 0x780, 0x8F8` plus `milan_status` (`receipts/console-poll-set.txt`).
- **The new claim at `:292` holds.** The reference peer's LINK_UP/LINK_DOWN stayed at 1/0, +0/+0, in all ten cycles (`peer:counter-9-0`, `receipts/step-context-check.txt`).

### (3) #387 acceptance 4 is NOT MET (not exercised)

- **Verdict row (`:11`):** says NOT MET (not exercised). It gives the HOLDOVER/streams-absent condition and the needed stimulus.
- **Item 2's contract (`:165-175`):** it matches `GM_LOSS_RECOVERY.md:142-160`:
  - one counted event per step;
  - licensed streams keep running;
  - one `mr` toggle and one MEDIA_RESET;
  - no step-to-relocked-media time bound.
- **Step conditions (`:177-183`):** every step fell in HOLDOVER with both streams absent, so the intervals measure outage recovery. `step_context_check.py` confirms this per cycle from the archive's `analysis.json` (`receipts/step-context-check.txt`, RESULT PASS):
  - MCSRV_STAT[2:0] was 5 (HOLDOVER; `REGISTER_MAP.md:2027`) at both ends of every step bracket;
  - the first DUT and peer PDUs followed the bracket end by 2.69-12.54 s;
  - the recomputed interval ranges equal the column in all ten rows.
- **Column rename:** "Outage media recovery after step" (`:223`, `:235`, `:250-252`).
- **#117 context label:** the #117 media row is labelled "#117 outage-recovery context, not #387's bound" (`:161-163`). That is consistent with `GM_LOSS_RECOVERY.md:88-99`, which was decided on #117.
- **Needed stimulus:** stated at `:347-349`. S1 is one refinement.
- **Negative control:** in a copy of the archive, three faults were planted: HOLDOVER changed to LOCKED, a pre-step PDU added, and a peer LINK_DOWN increment. The checker fails on exactly those three cycles (`receipts/mutation-step-context.txt`, rc 1).

### (4) The locator

The locator at `:383-397` states:
- the archive, branch `394-387-review-evidence`, path `review-evidence/394-387-r1`, commit `8f983d24`;
- the publisher index `MANIFEST.json`;
- that raw captures are in private cold storage;
- that `author/RAW-ARTIFACTS.json` and the per-cycle `author/cycleNN/raw-artifacts.json` index them by size and SHA-256;
- that their temporary-directory paths are historical names.

The `MANIFEST.sha256` claim is replaced by the publisher index.

`locator_check.py` passes (`receipts/locator-check-head.txt`):
- `MANIFEST.json` has 165 entries, and all 165 match the published bytes. The only unlisted file is `MANIFEST.json` itself.
- All 50 page hash rows appear in `RAW-ARTIFACTS.json` and in the matching per-cycle index.
- All 119 index paths are `/tmp` names.
- The page has no absolute path and no private packet name.

Control: the same check at the prior head fails on `2026-09-23/394-a375` and `/tmp/a375/cycleNN/` (`receipts/locator-check-prior.txt`).

- **Links:** both link targets exist in the tree at `8f983d24`.
- **Pinning:** the commit is an ancestor of the branch tip (behind_by 0). The branch moved during this review, from ahead_by 3 to ahead_by 4. The page pins the commit, so this does not affect it.
- **Identifiers:** the only 12-to-16-hex token outside the hash table is the stream format `041060010000bb80`. There are no MAC-like tokens (`receipts/hygiene-tokens.txt`).

### (5) Nothing else changed

All 20 hunks map to assignment items 1-4 (`receipts/delta-hunks.txt`):

| Hunks | What they change |
|---|---|
| `-10,2` and `-13` | the verdict rows and the open-issues sentence |
| `-161`, `-163`, `-165` and `-167` | the contract, the HOLDOVER condition, MAC_STATUS and the PHY limits |
| `-197`, `-209,2` and `-224` | the column rename and the table repair |
| `-244`, `-254`, `-256` and `-260` | the counter paragraph |
| `-307` and `-309` | the #387 verdict text |
| `-341` to `-349` | the locator |

Unchanged: the identity section, the method, the restore section, every per-cycle number, and the 50-row hash table. The PR body keeps "Refs #394. Refs #387." and says neither issue closes (assignment item 5).

### Gates and anchors

**Gates at this head, all rc 0 (`receipts/gate-*.txt`):**
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`;
- `check_em_dash.py --base 2a2a7bb6`, `check_doc_paths.py`;
- `ci_scope.py --selftest`;
- `check_baremetal_only.py --check`, run on the system interpreter because the isolated renderer environment has no YAML module;
- `check_feature_status.py --self-test`;
- `git diff --check`.

**Anchors.** No gate validates heading anchors. A disposable probe changed `#media-re-base-on-a-phc-step` to a nonexistent anchor, and `check_doc_paths.py` still returned 0 (`receipts/mutation-anchor.txt`; bytes restored). So `anchor_check.py` checks the anchors directly: all 13 anchored relative links resolve against the pinned render of their targets. Its planted control fails 1/13 (`receipts/anchor-check.txt`).

## Prior public review findings at this head

This reviewer's round 1 ([R361-1](https://github.com/kebag-logic/milan-fpga/pull/600#issuecomment-5859029552)):

| Finding | Status | Evidence |
|---|---|---|
| F1 MAJOR: #387 PASS graded on an undecided bound, on steps with no stream | RESOLVED | manager decision 5859045504 item 3; `:11`, `:161-183`, `:345-349`; `receipts/step-context-check.txt` |
| F2 MINOR: the per-cycle table does not render | RESOLVED | `receipts/table-probe.txt` (6 tables at this head, 5 at the prior head) |
| F3 MINOR: the link-counter explanation | RESOLVED | (a) `:185-187`, `:282`; (b) `:286-288`; (c) `:189-193`, `:290-294`; (d) `:292`; the defect is attributed to #599 at `:298` |
| F4 MINOR: the locator | RESOLVED | `:383-397`; `receipts/locator-check-head.txt` |
| S1 SUGGESTION: sample `LINKG_STAT`, `LINK_CTRL` and MDIO in the #599 re-run | carried to manager duties | not a page item |
| S2 SUGGESTION: mixed clocks in one column | retained as S2 | a page change was out of round-2 scope |

The other round-1 review ([R360-1](https://github.com/kebag-logic/milan-fpga/pull/600#issuecomment-5859039274)):

| Finding | Status | Evidence |
|---|---|---|
| F1 MINOR: the table does not render | RESOLVED | same as R361-1 F2 |
| F2 MINOR: the link-counter explanation | RESOLVED | same as R361-1 F3. No sentence asserts or implies an observed DUT PHY link drop (`:10`, `:189-193`, `:272`, `:290-298`) |
| F3 MINOR: the #387 PASS provenance | RESOLVED | same as R361-1 F1 |
| F4 MINOR: the locator | RESOLVED | same as R361-1 F4. The misdated private name is gone. The `TESTING` 6b sentence (`:399`) now follows a durable locator |
| S1 SUGGESTION: the docs gates accept mismatched table cell counts | outside this PR | routed to #495 at merge by 5859045504 |
| O1: stale `MANIFEST.sha256` entry for `PR-BODY.md` | no longer cited by the page | archive-level; manager |
| O2: EUI-64 values in the public packet | not on the page (`receipts/hygiene-tokens.txt`) | archive hygiene decision; manager |
| O3: post-restore stream-info residue | no finding | the page claims "unbound" |

## Out-of-scope observations (not findings against this head)

- **O1 - `hdl/milan/milan_datapath.sv:2906-2914`.**
  - What the code says: the comment says the Milan LINK_UP/LINK_DOWN counters follow `cnt_link_w`, a "counter-only link view ... without firmware qualification".
  - What the code does: `cnt_link_w` has no reader. The counters at `:3472-3494` count `eff_link_w`, which also includes `LINK_CTRL[0]`.
  - This predates the PR, and the page's text matches what the RTL actually does.
  - The #599 re-run should read the counters as `eff_link_w` edges. The contradiction may merit its own issue.
- **O2 - documentation gates.** `check_doc_paths.py` and `docs_check.py` accept a broken heading anchor (`receipts/mutation-anchor.txt`). This is the same class as R360-1 S1 and could join #495.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 SUGGESTION only) | #394 acceptance 2 and decision 5857769804; #387 acceptance 4, decisions 5606198212 and 5794731090, and status 5859048589; round-2 assignment 5859045504 items 1-5; `GM_LOSS_RECOVERY.md:88-160`; `TIME_SYNC.md:76-100`; page `:8-15`, `:155-213`, `:270-351`; PR body | R361-2 | 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1 |
| RTL | CLEAN | the sources behind the page's counter and status claims: `sw/litex/milan_soc.py:1782-1811`; `hdl/milan/milan_datapath.sv:2904-2914,3472-3514`; `hdl/common/KL_link_guard.sv:36-42`; `REGISTER_MAP.md:405,734,736,2027`. The diff changes no RTL | R361-2 | 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1 |
| Robustness | CLEAN | the page's statements at failure and boundary states (unobserved PHY drop, unsampled guard inputs, a step landing in HOLDOVER, the intermediate MEDIA_RESET zero caught in 5 of 10 cycles, the 180 s stop) checked against the ten `author/cycleNN/analysis.json`; locator stability (a pinned commit on a moving branch; 166 git-verified blobs, fetched twice with identical bytes) | R361-2 | 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1 |
| Tests | CLEAN | no executable test changed. Evidence checks `table_probe.py`, `locator_check.py`, `step_context_check.py` and `anchor_check.py`, each with a discriminating control (the prior head or a planted mutation); the nine assigned gates, all rc 0 | R361-2 | 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1 |
| Docs | CLEAN (S1 and S2 SUGGESTION only) | the whole page `docs/findings/394_387_E1_SWITCH_CYCLES.md:1-464`, source and pinned render; its 13 anchors and 7 external link targets; the archive's `MANIFEST.json`, `RAW-ARTIFACTS.json` and per-cycle indexes; the PR body at this head | R361-2 | 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1 |

## Real limits

- **No raw captures.** The per-cycle raw captures are in private cold storage.
  - Page numbers were checked against the archive's `analysis.json`, the operator's analyzer output, not against raw decoding.
  - "Private cold storage" is a public statement by the manager. This round cannot verify it.
- **No hardware.** There was no bench access, and physical calibration was NOT RUN. Field skips are not hardware proof. Whether the DUT PHY link drops on a switch cycle is still unobserved, as the page says.
- **Banks not run.** Full parent, PP, gPTP, Yosys and builder banks were not run. They were not permitted, and the diff is one documentation page. The scoped Verilator was not needed.
- **Hosted checks at this head** (`receipts/hosted-check-runs.tsv`, fetched 2026-09-27T19:46:46Z):
  - `docs-check` was still `in_progress`;
  - `rtl-fast`, `bdd-conformance`, `changes`, `docs-check-no-git`, `elaborate`, `full-ci-gate` and `wire-accountability` succeeded;
  - `verilator-suites`, `yosys-portability`, their shards and lint/elaboration jobs, and the physical gPTP job are skipped contexts, not executed jobs.
- **Clone integrity after the probes** (`receipts/clone-integrity.txt`):
  - HEAD and index tree are `705d9ab5...`, and the status is empty;
  - 929 tracked files rehash with 0 mismatches and 0 mode drift;
  - no assume-unchanged or skip-worktree flags are set;
  - the gitlinks are at their pins: `gptp-processor 5dce647a`, `protocol-processor 870ff88a`, `third_party/verilog-axis 48ff7a7e`, with `external efeb541a` uninitialised by design.

## Pending manager duties

- Publish this report.
- Hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- Candidate merge validation against live dev `6d5ebd7357c1e468e446f18a61527c5be6118a04` from source base `2a2a7bb6`.
- The internal review's (R360-2) verdict, and merge authorization.
- At merge, route R360-1 S1 and O2 above to #495. Consider an issue for O1.
- Re-run #394 acceptance 2 after #599. Carried R361-1 S1: sample `LINKG_STAT`, `LINK_CTRL` and the e1 PHY MDIO link bit during each outage.
- Decide the #387 running-stream stimulus (S1).
- The archive-level items: the stale author `MANIFEST.sha256` entry for `PR-BODY.md`, and the EUI-64 hygiene decision.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.

- **Scripts:** `fetch_archive.py`, `table_probe.py`, `locator_check.py`, `step_context_check.py`, `anchor_check.py`.
- **Evidence:** `receipts/`.

R361-2 FINISHED
