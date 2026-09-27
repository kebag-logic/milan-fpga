[R360] POSITIVE - exact head 6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1

# R360-2: independent internal re-review of PR #600 (issue #394 acceptance 2, issue #387 acceptance 4)

- **Head and tree:** head `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1`, tree `705d9ab5dd1c6603af7de11abe21ddfcad47d1ff`.
- **Delta under review:** `fddc58e4..6f2cdab6`. This is one commit, `Correct ten-cycle acceptance claims and public evidence locator`. It has a one-line message and no trailer.
- **Scope of the delta:** it changes only `docs/findings/394_387_E1_SWITCH_CYCLES.md` (+70 -22).
- **Lane:** `2a2a7bb6..6f2cdab6` is two commits, and that page is the only file either commit touches (`receipts/full-diff-stat.txt`, `receipts/lane-history.txt`).
- **Public evidence examined:** `review-evidence/394-387-r1` at `8f983d245a12e18a47ced37904d405b624c7e024`. That commit is an ancestor of branch `394-387-review-evidence`, whose tip is `423ed5b7`. After `8f983d24`, only `MANIFEST.json` in that path was modified. Every other later change adds new files.

## How the context was rebuilt

I read, in this order:
1. AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6).
2. docs/README.md.
3. The #394 body with acceptance 2 as frozen, and owner decisions 5789765478, 5810503583 and 5857769804.
4. The assignment 5858215210, the manager comment 5858862351, and the round-2 assignment 5859045504.
5. The #387 body with acceptance 4, decision 5794731090, and the manager's status comments 5858215380 and 5859048589.
6. #599.
7. The authorities:
   - `docs/design/GM_LOSS_RECOVERY.md`: Recovery bound, and Media re-base on a PHC step.
   - `docs/design/TIME_SYNC.md`: Step policy.
   - `docs/reference/REGISTER_MAP.md`: 0x110, 0x71C, 0x774 and 0x8F8.
   - `sw/litex/milan_soc.py:1761-1811` and `sw/firmware/milan_baremetal/milan_baremetal.c`.
   - `hdl/milan/milan_datapath.sv:2886-2914` and `:3465-3500`.
   - `hdl/common/KL_link_guard.sv:320`.
8. The diff and history.
9. The public packet and the PR body.
10. The public TAKEN and REVIEW READY comments of both executors.

I wrote my own verdict and ledger (`receipts/verdict-draft-before-prior-findings.md`) before reading the round-1 review reports. Those reports are resolved below.

## Verdict summary

Every item of the round-2 assignment is met at this head. My independent pass found no BLOCKER, MAJOR or MINOR finding. It found one optional SUGGESTION.

- **#394 acceptance 2** stays **FAIL**, and it is correctly explained.
- **#387 acceptance 4** reads **NOT MET (not exercised)**, as the manager decided.
- **Measurements:** every per-cycle number still recomputes from the public analyses.
- **Artifact index:** all 50 raw-artifact rows match both public indexes.

### The five round-1 checks

**(1) The per-cycle table renders: VERIFIED.**
- In the markdown, the header, the delimiter and all 10 rows each have 9 cells (`docs/findings/394_387_E1_SWITCH_CYCLES.md:235-246`).
- The platform's own rendering of the file at the exact head shows 6 tables, and the per-cycle table renders as 11 rows × 9 cells.
- Control: the round-1 head `fddc58e4` renders 5 tables. The checker reports a MISMATCH there (9 header cells against 10 delimiter cells) and fails.
- A planted 10-cell delimiter at this head also fails.
- Receipts: `receipts/tables-6f2cdab6.txt`, `receipts/tables-fddc58e4-control.txt`, `receipts/github-render-6f2cdab6.html`, `receipts/controls-and-peer.txt`.

**(2) The link-counter text: VERIFIED.** It states each required fact:
- MAC_STATUS stayed at its software-published reset value `0x0d`, and nothing in this build writes it (#599): `:185-187` and `:282`. The source agrees:
  - the reset fields are link_up=1, speed(gmii)=2 and full_duplex=1, which is `0x0d`;
  - there is no writer of `link_status` outside its definition;
  - the bare-metal firmware has no MDIO, link or MAC_STATUS reference (`receipts/source-checks.txt`).
- "Whatever the PHY did, this status cannot advance LINK_UP/LINK_DOWN" (`:284`).
- "Whether the DUT PHY link dropped was not observed. The inline capture point may hold that link up" (`:189-191`, `:290`).
- The page also correctly adds four points:
  - The counters also depend on the link guard's RX-clock-alive veto. This matches the RTL: `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` and `link_est_o = rx_alive_r`.
  - LINKG_STAT and LINK_CTRL were not sampled. The packet's console reads are `0x110`, `0x720`, `0x750`, `0x764`, `0x780` and `0x8f8` only.
  - The peer's own LINK_UP/LINK_DOWN stayed at 1/0 with +0/+0 in all ten cycles.
  - "missing publication, not an observed missed edge" (`:286-294`).
- The sentences "This run never wrote that status to manufacture edges" and "link-counter failure reproduced" are gone (`receipts/prior-finding-greps.txt`).
- The #394 FAIL stays (`:10`, `:298`).
- Scoping "cannot advance" to *this status* is more accurate than an unscoped "the counters cannot advance". The guard term is live at reset (`LINK_CTRL` resets to `0x1`, so `linkg_dis=0`). See O1.

**(3) #387 acceptance 4: VERIFIED as NOT MET (not exercised).**
- The verdict row reads NOT MET (not exercised) (`:11`, `:345`).
- Item 2's contract is stated:
  - it is `GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step` together with `TIME_SYNC.md#step-policy`;
  - one counted event per step, one `mr` toggle and one MEDIA_RESET;
  - licensed streams keep running;
  - there is no step-to-relocked-media time bound (`:165-175`).
- The "one further stream restart" row is labelled as #117 outage-recovery context, not #387's bound (`:161-163`). This matches `GM_LOSS_RECOVERY.md:88-99`, a bound the owner fixed on #117.
- Every step landed in HOLDOVER with both streams absent, so the column is renamed "Outage media recovery after step" and described as outage recovery (`:177-183`, `:223`, `:235`, `:250-252`).
- The stimulus still needed is stated: a grandmaster change while a locked CRF stream keeps running (`:11`, `:347-349`).
- I checked these claims independently against all ten public analyses:
  - each cycle has exactly one PHC discontinuity;
  - MCSRV_STAT is state 5 (HOLDOVER) across the whole step bracket in every cycle;
  - the tap shows no frame between the gap start and the bracket;
  - the first DUT CRF PDU arrives 2.69-12.54 s after the bracket closes, and the first peer CRF PDU 4.43-9.58 s after (`receipts/recompute-6f2cdab6.txt`).

**(4) The locator: VERIFIED.**
- The page names three things:
  - the public archive: branch `394-387-review-evidence`, path `review-evidence/394-387-r1`, commit `8f983d24` (`:383-387`);
  - the publisher index `MANIFEST.json` (`:389`);
  - private cold storage, indexed by size and SHA-256 in `RAW-ARTIFACTS.json` and the per-cycle `author/cycleNN/raw-artifacts.json`, whose temporary-directory paths are historical names (`:391-397`).
- The `MANIFEST.sha256` claim is replaced by the publisher index.
- I checked each part:
  - All three links resolve at `8f983d24` (`receipts/external-links.txt`).
  - `MANIFEST.json` verifies 165/165 published hashes, and no file is unlisted.
  - All 50 page rows equal `RAW-ARTIFACTS.json` and the per-cycle indexes. The 10 `events.jsonl` files that are physically in the archive rehash to their page rows.
  - The indexes' absolute prefixes are only the historical `/tmp/a375...` names.
  - The page contains no private packet name, no `/tmp`, `/home` or `/data` path, and no `MANIFEST.sha256` (`receipts/locator-6f2cdab6.txt`, `receipts/public-subset-rows.txt`).

**(5) Nothing else on the page changed: VERIFIED.**
- The raw delta has 8 hunks (`receipts/delta-fddc58e4-6f2cdab6.diff`), and each maps to assignment items 1-4:
  - the acceptance table and the closing sentence;
  - the method paragraph on bounds, contract and link status;
  - the column rename and its explanation;
  - the counter paragraph and its table row;
  - the #387 closing paragraph;
  - the locator.
- No measurement cell, identity row, restore line or hash row changed.
- The PR body keeps "Refs #394. Refs #387. Neither issue closes." It has no closing keyword and no closing issue reference (`receipts/pr600-body.md`, `receipts/pr600-meta.json`).

## Findings

### S1: SUGGESTION (Docs). "the servo" is ambiguous next to the step-policy link

- **Where:** `docs/findings/394_387_E1_SWITCH_CYCLES.md:177`.
- **Evidence:** "Every observed step occurred while the servo was in HOLDOVER" follows two lines that cite `TIME_SYNC.md#step-policy`. The table there is keyed by the gPTP servo's state (Link-up and Locked). The HOLDOVER meant here is the media servo's MCSRV_STAT state 5, which is what `:69` and `:305` call "media servo".
- **Impact:** a reader could take the sentence as a gPTP servo state. The facts are unaffected.
- **Suggested outcome:** say "the media servo (MCSRV_STAT HOLDOVER)".
- **Verification:** reread `:177`.
- **Effect on coverage:** none, because it is optional.

No BLOCKER, MAJOR or MINOR finding is open at this head.

## Prior public review findings at this head

| Prior finding | Status at `6f2cdab6` | Evidence |
|---|---|---|
| R360-1 F1 = R361-1 F2 (table does not render) | RESOLVED | Check (1): 6 rendered tables, 9/9/9 cells, and a control that fails at `fddc58e4` |
| R360-1 F2 = R361-1 F3 (link-counter explanation) | RESOLVED | Check (2): all four R361-1 F3 parts (a)-(d) are present at `:282-294`, and "defect" is attributed to #599 at `:294` and `:298` |
| R360-1 F3 = R361-1 F1 MAJOR (#387 PASS on an unstated bound, steps while streams were stopped) | RESOLVED | Check (3), implementing the manager's decision (#394 5859045504 item 3; #387 5859048589) |
| R360-1 F4 = R361-1 F4 (locator) | RESOLVED | Check (4). The page no longer cites `MANIFEST.sha256`. The PR-BODY hash inconsistency is packet-side (O2) |
| R360-1 S1 (docs gates accept a mismatched table) | RETAINED as SUGGESTION, out of this PR | Assigned by the manager to #495 at merge |
| R361-1 S1 (sample LINKG_STAT, LINK_CTRL and BMSR in the #599 re-run) | RETAINED as SUGGESTION, out of this PR | Belongs to the #599 re-run. See O1 |
| R361-1 S2 (the "GM return / PHC step" column mixes tap and console clocks) | RETAINED as SUGGESTION, not addressed | `:219-231` unchanged. It is optional and does not affect coverage |

## Clean-lens evidence

```text
[R360] PASS Conformance - docs/findings/394_387_E1_SWITCH_CYCLES.md:8-15,159-193,270-298,343-349,381-399 at 6f2cdab6; issue 394 comment 5859045504 items 1-5; issue 387 comment 5859048589; GM_LOSS_RECOVERY.md:88-99,142-157; TIME_SYNC.md:76-114; PR #600 body - Checked every round-2 item against the page: #394 acceptance 2 stays FAIL with the #599 cause and the unobserved PHY state; #387 acceptance 4 is NOT MET (not exercised), with item 2's count-based, time-unbounded contract, the #117 row labelled as context, and the needed stimulus stated; the locator names the public archive. The PR body keeps Refs #394 and Refs #387 and closes nothing. The recovery-bound row and the re-base contract are quoted correctly from the design pages.
[R360] PASS RTL - sw/litex/milan_soc.py:1782-1797,1966-1975; sw/firmware/milan_baremetal/milan_baremetal.c (no MDIO, link or 0x110 reference); hdl/milan/milan_datapath.sv:2904-2914,3472-3494; hdl/common/KL_link_guard.sv:320; REGISTER_MAP.md:405,734,736 - The page's RTL and firmware claims hold: the MAC_STATUS reset composes to 0x0d; nothing writes link_status; the counters count edges of eff_link_w, which also carries the guard's RX-alive estimate and LINK_CTRL[0]; LINKG_STAT (0x774) and LINK_CTRL (0x71C) were never read (the packet shows only mem_read of 0x110, 0x720, 0x750, 0x764, 0x780 and 0x8f8). No RTL or firmware is changed by the lane (receipts/full-diff-stat.txt). receipts/source-checks.txt.
[R360] PASS Robustness - page :177-193,284-294,345-349 against review-evidence/394-387-r1/author/cycle01..10/analysis.json at 8f983d24 - Checked the record's claims on the failure and boundary paths: the step lands inside media-servo HOLDOVER (state set {5} across every bracket); both streams are off the wire (wire silent before each bracket, first PDUs after it); exactly one discontinuity per cycle; MAC_STATUS is {0x0d} in all samples; DUT and peer LINK_UP/LINK_DOWN deltas are 0/0 in all ten repeated cycles; the unobserved-PHY-link and capture-point limits are stated, not converted into claims. receipts/recompute-6f2cdab6.txt, receipts/controls-and-peer.txt.
[R360] PASS Tests - scripts/recompute_cycles.py, scripts/check_tables.py, scripts/check_locator.py with controls; the nine assigned gates at 6f2cdab6 - The PR adds no test. Its evidence claims are reproduced by independent code: in all 10 rows the OFF duration, GM return, both step-bracket ends, gPTP recovery, first DUT and peer PDU and both outage-media-recovery ends (9 values per row) recompute within ±0.01 s from analysis.json (the controller down/up, mr-change and MEDIA_RESET-sequence cells are unchanged from the round-1 head and were not recomputed this round), table widths match, and the hash rows match both indexes. Each checker fails its planted control (a changed media cell, a reintroduced /tmp locator, a changed hash digit, a 10-cell delimiter) and fails on the round-1 head. The nine gates return 0: docs_check, check_doc_style, gen_toc --check, check_em_dash --base 2a2a7bb6, check_doc_paths, ci_scope --selftest, check_baremetal_only --check, check_feature_status --self-test, git diff --check (receipts/gates-6f2cdab6.txt). The page no longer claims the run exercised #387's contract, so no test-like claim outruns what the run could detect.
[R360] PASS Docs - docs/findings/394_387_E1_SWITCH_CYCLES.md:1-464 at 6f2cdab6, as source and as rendered by the platform (receipts/github-render-6f2cdab6.html); receipts/delta-fddc58e4-6f2cdab6.diff; receipts/external-links.txt; receipts/locator-6f2cdab6.txt - The page renders all six tables. Contents and anchors pass. There are no em dashes, and no private locator, absolute path or bench-identifying name in the page or the PR body. Every link resolves. The delta touches only assignment items 1-4. The commit message is one line with no trailer. S1 is optional.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Page `:8-15`, `:159-193`, `:270-298`, `:343-349`, `:381-399`; #394 acceptance 2 and decisions 5857769804 and 5859045504; #387 acceptance 4 and 5859048589; `GM_LOSS_RECOVERY.md:88-157`; `TIME_SYNC.md:76-114`; #599; PR body and closing references | R360-2 | `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1` |
| RTL | CLEAN | `sw/litex/milan_soc.py:1761-1811,1966-1975`; `milan_baremetal.c`; `milan_datapath.sv:2886-2914,3465-3500`; `KL_link_guard.sv:320`; `REGISTER_MAP.md:405,734,736`; packet console register set | R360-2 | `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1` |
| Robustness | CLEAN | Ten `cycleNN/analysis.json` at `8f983d24` (servo states, discontinuities, wire first and last, MAC_STATUS, DUT and peer link counters); page `:177-193`, `:284-294`, `:345-349` | R360-2 | `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1` |
| Tests | CLEAN | `scripts/recompute_cycles.py`, `scripts/check_tables.py`, `scripts/check_locator.py` and their planted controls; nine assigned gates at head | R360-2 | `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1` |
| Docs | CLEAN (S1 optional) | Whole page, source and platform-rendered; raw delta; external links; locator and index checks; PR body; commit message | R360-2 | `6f2cdab6fcc966bd5f9570fd9e37e34276cd72c1` |

## Other observations (not findings on this PR)

- **O1: two texts outside this PR state the counter consequence without the guard term.**
  - The texts are the round-2 assignment wording ("LINK_UP/LINK_DOWN therefore cannot advance on this image, whatever the PHY did") and the #599 body ("cannot advance").
  - The guard's RX-alive term reaches the counters and is enabled at reset. So a DUT RX clock that stops for `DEAD_CYC_C` = 4096 cycles would move LINK_DOWN even with MAC_STATUS unwritten.
  - The page's scoped wording ("this status cannot advance") is the accurate form.
  - The #599 re-run should sample `LINKG_STAT` and `LINK_CTRL` alongside the planned BMSR read (as in R361-1 S1). Otherwise a counter movement cannot be attributed.
- **O2: the publisher `MANIFEST.json` at `8f983d24` has an inconsistent record for `author/PR-BODY.md`.**
  - It records `original_sha256` equal to the published hash `7407cd57...`.
  - The author's `MANIFEST.sha256` lists `5c71a3d7...`.
  - This affects only the packet's provenance record. The page's claim, that `MANIFEST.json` records the published files' SHA-256 values, holds: 165/165 match.
- **O3: the page's archive links depend on commit `8f983d24` staying reachable.** They pin that commit on a non-default branch, so the branch must not be deleted or force-pushed.

## Real limits

- **Raw captures not available.** They are in private cold storage.
  - The per-cycle recomputation and the HOLDOVER and absence checks use the operator's `analysis.json`, not raw console, tap or controller data.
  - The raw files are tied to the page only by the size and SHA-256 indexes.
  - Cold storage itself was not inspected.
- **No bench access, no hardware, and physical calibration NOT RUN.** Field skips are not hardware proof. The DUT PHY link state remains unobserved, as the page says.
- **Banks not run.** The full parent, PP, gPTP, Yosys and builder banks were not run: they were not permitted, and the lane has no RTL, firmware or builder change.
  - The scoped Verilator was not used, because the delta touches no HDL. Its identity was therefore not checked.
- **Gate environment.** The docs gates ran with the repository's hash-pinned markdown lock in a disposable environment under `scratch/`. `check_baremetal_only.py` first returned rc 2 in that environment because pyyaml was absent. That was an environment gap, not a finding. It returned rc 0 with the system interpreter, which carries pyyaml. Both runs are in `receipts/gates-6f2cdab6.txt`.
- **Hosted checks at the exact head, as of 2026-09-27T19:45:06Z (`receipts/hosted-checks-6f2cdab6.txt`).** These are not my acceptance:
  - succeeded: `rtl-fast`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `full-ci-gate`, `changes` and `bdd-conformance`;
  - still `in_progress`: `docs-check`;
  - skipped contexts, not executed jobs: `verilator-suites`, `yosys-portability`, the Verilator and Yosys shards, `verilator-lint`, `yosys-elaboration` and Physical gPTP.
- **Clone integrity after review (`receipts/clone-integrity.txt`):**
  - HEAD, HEAD tree and index tree are exact, and the status is clean with 0 untracked files;
  - no assume-unchanged or skip-worktree flag is set;
  - all 929 tracked non-gitlink entries rehash equal, with no mode drift;
  - the required gitlinks are checked out at their pins: `gptp-processor 5dce647a`, `protocol-processor 870ff88a`, `third_party/verilog-axis 48ff7a7e`;
  - `external efeb541a` is uninitialised, as it was in round 1.

## Pending manager duties

- Publish this report.
- Get the external R361-2 verdict. Merge needs two independent positives.
- Complete hosted and act acceptance at the exact head, including the in-progress `docs-check`.
- Validate the candidate merge from source base `2a2a7bb6` onto live dev `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
- Get maintainer merge authorization.
- Assign R360-1 S1 to #495 at merge.
- The #599 re-run of #394 acceptance 2 (see O1).
- Decide the stimulus for the #387 running-stream measurement.
- The O2 packet record.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.
- **Scripts** (portable; each takes the page, the archive directory or the clone as arguments):
  - `scripts/check_tables.py`
  - `scripts/recompute_cycles.py`
  - `scripts/check_locator.py`
  - `scripts/source_checks.sh`
  - `scripts/clone_integrity.sh`
- **Receipts:** under `receipts/`.

R360-2 FINISHED
