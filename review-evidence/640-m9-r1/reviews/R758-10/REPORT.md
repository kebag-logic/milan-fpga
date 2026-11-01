[R758] POSITIVE - exact head d63b378d27c1c663034744a5b48a99c190271f58

# R758-10: external review of PR #828 (issue #640), round 9 delta

Tree `1a46d16e200ffa03e23ebe520f152add55f25b1e`. Delta `20933ef4..d63b378d`: four one-line commits, 16 Markdown pages, no other file. Source base and live dev are both `1f29f189`.

**Result:** no BLOCKER, MAJOR or MINOR. Four RESIDUE items and one new SUGGESTION. R757-9-F1, R757-9-F2, R758-8-R1 and R758-8-R2 are resolved at their cause.

This is not a merge clearance on its own. The PR is now CI-relevant, and its exact-head long gates had not finished when I checked them (see "Pending manager duties").

Order of work: my draft verdict was frozen in `receipts/draft_before_prior_findings.txt` before I opened any prior report. All four RESIDUE items were already in that draft. Two things changed afterwards: the 52,008 suggestion turned out to be R757-9 S2, so it is retained rather than raised as new, and I added R758-10-S1 when reading the PR body's status line for the closure check.

## Named for the owner, not a finding

**D8's 1 percent margin against the 20,000-LUT ceiling is undecided by any source.** AB:400-402 keeps "requires at least 1 percent planning margin" and marks 37,659 as the replaced target's ceiling. No page and no decision says whether a margin applies to 20,000 LUTs. The owner should say whether it does. (AB = `docs/design/AREA_BUDGET.md`, FR = `docs/reference/FR_NFR.md`, AP = `docs/design/MARK_II_AREA_PLAN.md`, SE = `docs/design/MARK_II_STREAM_ENGINES.md`.)

## The five checks

### 1. AREA_BUDGET.md against NFR-RES-01: holds

| Point | Evidence |
|---|---|
| Target statement gives the ceiling | AB:130 "fewer than 20,000 LUTs"; FR:473 |
| Target row | AB:140: Mark II fewer than 20,000 (about 31.5 %); this image must fit the device. 20,000 / 63,400 = 31.55 % |
| Shipping status | AB:136, AB:140 "no other LUT bound", matching FR:473 "carries no other LUT bound" |
| Acceptance bar | AB:179-180: the NFR-RES-01 ceiling, with timing met |
| Re-record rule and M9 row | AB:524-525 and AB:245 name the Mark II ceiling |
| Measured figures unchanged | Digest of the resource, device, route and used cells is identical at both heads; baseline JSON blob `102f3fee` is identical at base, round 8 and head |
| Gate | `check-baseline` rc 0, "baseline PASS: 3 endpoints"; policy table digest identical at both heads |

Every remaining replaced figure in AB is marked:

| Line | Figure | Marking |
|---|---|---|
| AB:132-133 | 60 percent, 38,040, 13,972 | "That replaces the earlier", "was" |
| AB:182-186 | 60 percent, 10,521, 13,972 | "What follows is history" (see R758-10-R3) |
| AB:199-200 | 38,040 | "This section is the Mark I plan, kept as history" |
| AB:245 | 38,040 | "formerly" |
| AB:369-372 | 38,040, 37,659 | "The two headroom columns are history"; both headers say "replaced" |
| AB:402-405 | 37,659, 38,040 | "was", "was then", "has replaced it" |

Non-Markdown tracked text names none of 38,040, 37,659, 13,972 or 10,521 (`receipts/stale_search_at_head.txt`, section A2, empty).

### 2. Listed pages: hold

Each page against `REQUIREMENTS.md:27-37`, SPLIT:3-4 (`docs/ARCHITECTURE_HW_SW_SPLIT.md`) and `docs/overview/ARCHITECTURE.md:6-16`:

| Page | Transition and end state | Today's facts kept |
|---|---|---|
| `README.md:59-71` | Stated, same wording as ARCHITECTURE | VERSION `0x0002_0060`, shipping default, "no shipping placement changes here" |
| `docs/overview/FULL_FPGA_SOLUTION.md:6-19` | Stated | Current image and core at :3-4; mailbox fact; inventory scope |
| `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:21-32` | Stated, with the contract pointer | Control traffic in fabric; inactive classifier input |
| Same page, :36-45 | "gPTP progress does too, until F6", supported by `REQUIREMENTS.md:44-45` | CSR window uses, interrupt status, service obligation |
| `docs/GLOSSARY.md:29`, `:45` | Stated; matches `REQUIREMENTS.md:34-37` | Current fabric placement |
| AB:219-220 | Stated | Shipping default until the flip |
| MAAP_FABRIC, DATAPLANE_WALKTHROUGH, FPGA_DESIGN, LITEX_SOC, SYSTEM_DOMAIN_MAP, ieee8021q, each :3-7 | Pointer to `#1-ownership-rule` | "stays the shipping default until F2 to F5 acceptance"; acceptance scope; LITEX_SOC's memory link |

Removing AB's "Unqualified functions retain fabric placement" is correct: SPLIT:4 leaves no retained-fabric option. It takes no fact about today's image with it.

### 3. Stale-contract search: one residue miss

Commands: `scripts/stale_search.sh`. Full output: `receipts/stale_search_at_head.txt`.

Remaining hits that bear on the contract, all scoped or marked:

| Hit | Why it stands |
|---|---|
| FR:473, AP:67, AP:251, AP:318 and AP's later figures | Marked as replaced, or under AP's "Mark I plan history" |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:5-6` | Bounded: "before the default changes" |
| `docs/design/MAILBOX_SPLIT.md:14`, `:439` | Bounded and shipping-scoped |
| `docs/overview/FULL_FPGA_SOLUTION.md:85`, `:104` | :85 is inside the inventory that :19 scopes to the current build; :104 holds in both placements and after |
| `docs/traceability/ieee8021q.md:39`, `:115`; `docs/design/SAVED_STATE_FASTCONNECT.md:1436`; `docs/design/MAILBOX_SPLIT.md:1078` | "both placements": true until the switch-over, per `REQUIREMENTS.md:58` |
| `README.md:152`; `docs/GLOSSARY.md:30`; `docs/guides/gptp/SYSTEM_INTEGRATOR.md:72` | Today's fact, no permanence claimed |
| `docs/design/GPTP_PLANE.md:22` | Contents line; :6 now scopes the page |
| `docs/reference/REGISTER_MAP.md:293`, `:830`; `docs/reference/REGISTER_MAP_CLASSES.md:97` | Register facts at the current VERSION, dated at the head of the overlay |
| `docs/litex/LITEX_SOC.md:119`; `docs/integration/BAREMETAL_FIRMWARE.md:111`, `:116`, `:195` | Today's option and recipes |
| `docs/design/TIME_SYNC.md:30` | The column is headed "Current owner" |
| `docs/guides/SYSTEM_INTEGRATOR.md:95`; `docs/guides/gptp/TEST_DEVELOPER.md:26` | About entity enablement and test judging, not placement |

**Miss:** `docs/guides/gptp/MANAGER.md:17-18`, which is R758-10-R4 below. The author's sweep did not list it because its wording avoids "gPTP" and "fabric".

### 4. Added edits: hold

- **`docs/ENDSTATION_BUILDER.md:3-7`:** the page stays scoped to the current build, and the pointer replaces "selectable". "Split static control contexts" keeps the old sentence's meaning.
- **`docs/integration/INTEGRATION_GUIDE.md:5-6`:** "It preserves media interfaces, and gPTP interfaces until F6." The author flagged this as a reading. I accept it: `REQUIREMENTS.md:40-45` retains the plane and its deadlines only until F6. The PHC and timestamps staying in fabric after F6 (`REQUIREMENTS.md:37`) do not contradict the sentence.
- **`docs/design/GPTP_PLANE.md:6-7`:** matches `REQUIREMENTS.md:34` and SPLIT:115-117. `check_gptp_docs.py` passes.

### 5. Docs workflow and classifier: hold, and the scope change is real

From `receipts/ci_scope.txt`, with the classifier's selftest passing:

| Path list | Classifier |
|---|---|
| PR at `20933ef4` | false |
| PR at `d63b378d` | **true** |
| PR at `d63b378d` without AB | false |

- **Cause:** AB alone. It is the only `GATE_READ_DOCS` member the PR changes, and the PR changes no file under `scripts`, `.github`, `syn` or `tests`. The hosted runs agree: the Verilator and Yosys shards were pending, not skipped.
- **Negative control** (`receipts/gate_negative_control.txt`): `check-baseline` against four budget texts, the baseline unchanged.

| Budget text | rc | Meaning |
|---|---|---|
| Round 8 | 0 | Passes |
| Head | 0 | Passes |
| Head without the 7 lines naming 38,040 or 60 percent | 0 | The gate does not read those figures, confirming the author's claim |
| Head with the `route-1x1` LUT tolerance +500 changed to +501 | 2 | The gate does read the policy table |

- **Docs gates, re-run here at the head, all rc 0:** `docs_check`, `check_em_dash` (0 over 1,906 added lines in 21 pages), `check_doc_style`, `check_gptp_docs`, `check_solution_docs`, `check_feature_status`, `check_doc_paths`, `gen_toc --verify-anchors` and `--check`, `check_archive`, `check-baseline`. Logs are in `receipts/gates/`.
- **Author receipts:** 120 published files all match `MANIFEST.json`. All 116 `SHA256SUMS` rows match the manifest's original digests. 16 published files differ from `SHA256SUMS`, and each is flagged `path_redacted`. All 50 rc files read 0 (`receipts/author_r9_manifest_check.txt`). The redaction flag is the manifest's statement; I cannot hash the unredacted originals.
- **Hosted at the exact head, snapshot only:** `docs-gates-0`, `-1`, `-2`, `docs-check-no-git`, `changes` and `full-ci-gate` passed; `docs-check` was pending. The count was 15 pass, 34 pending, 1 skipping (`receipts/hosted_checks_snapshot.txt`).

## Findings

All four RESIDUE items are prose only: no figure, grade, gate, test or clause claim changes.

### R758-10-R1 RESIDUE - Docs - `docs/traceability/ieee8021q.md:38` - a new list marker moves today's facts under the Mark II bullet

- **Authority/evidence:** at `20933ef4` the line was an indented continuation of the "Reservation is the protocol processor's." bullet. The delta made it `- Mark II moves reservation to firmware after the switch-over.` So :39-44 now render as part of a Mark II bullet, including "MRP-1..MRP-8 and SRP-1..SRP-10 are now PROCESSOR" and the class-D wiring.
- **Impact:** a reader can take today's processor binding as describing Mark II. The words themselves are unchanged and true.
- **Exact fix:** replace the leading `- ` on :38 with two spaces.
- **Verification:** read :35-44; the docs gates pass.

### R758-10-R2 RESIDUE - Docs, Conformance - `docs/design/AREA_BUDGET.md:130, 140, 180` - the ceiling is given without its 32x32 shape

- **Authority/evidence:** FR:473 sets the ceiling "at the 32x32 shape". AB:130, AB:140 and AB:180 omit the shape, and the row at AB:140 describes a 1x1 route.
- **Why RESIDUE:** each line links FR:473 or sits directly under the sentence that does, and FR:473 governs. The figure is right.
- **Impact:** a reader could grade a smaller build against 20,000 LUTs.
- **Exact fix:**
  - AB:130: "Mark II must use fewer than 20,000 LUTs of `xc7a100t` at 32x32."
  - AB:140: "Mark II fewer than 20,000 at 32x32 (about 31.5 %)".
  - AB:180: "That is fewer than 20,000 LUTs at 32x32, with timing met."
- **Verification:** read the lines against FR:473; `check-baseline` still passes.

### R758-10-R3 RESIDUE - Docs - `docs/design/AREA_BUDGET.md:182` - "What follows is history" has no end

- **Authority/evidence:** the history is AB:183-186. AB:188-195 are current, including the redesign plan, the schedule and "Until M9, comparisons retain".
- **Impact:** a reader could take the current schedule and comparison rule as history.
- **Exact fix:** AB:182: "The next three sentences are history, against the replaced 60 percent."
- **Verification:** read :182-195.

### R758-10-R4 RESIDUE - Docs, Conformance - `docs/guides/gptp/MANAGER.md:17-18` - an unscoped value statement on a page for delivery decisions

- **Authority/evidence:** the lines read "Protocol work stays inside programmable logic." and "One plane owns synchronization and public health." `REQUIREMENTS.md:36` moves the protocol and servo to firmware after F6. The page has no F6 scope or pointer, although `docs/design/GPTP_PLANE.md:6-7` now does.
- **Why RESIDUE, not MINOR:** the title "Fabric gPTP manager guide" scopes the page to the fabric plane, and of that plane the lines are true. This page was not on R757-9's list and no gate reads it.
- **Impact:** a manager reading only this page could plan on gPTP staying in logic.
- **Exact fix:** after :6 insert "This guide covers the fabric plane, which owns product time until F6." and "The [split contract](../../ARCHITECTURE_HW_SW_SPLIT.md) defines that transition."
- **Verification:** `check_gptp_docs.py` and `check_doc_style.py` pass.

### R758-10-S1 SUGGESTION - Docs - PR body line 24 - the status line says "documentation only"

The Round 9 "CI scope" row explains that the PR is now relevant, and "documentation only" is true of the files. But the first status line is what a cold reader sees. Adding "CI-relevant: the exact-head long gates apply" would settle it.

## Prior findings

Read after my independent pass.

| Finding | State at this head | Evidence |
|---|---|---|
| R757-9-F1 MINOR | **Resolved** | Check 1 |
| R757-9-F2 MINOR | **Resolved**, one guide page left as R758-10-R4 | Checks 2 and 3 |
| R758-8-R1 RESIDUE | **Resolved**, exact text | SE:450-453. The script behind the link walks 192 kHz at random and leaves out eight-channel streams (`probe_fewer_bound.py:116-127`) |
| R758-8-R2 RESIDUE | **Resolved**, exact text | AP:60, AP:255, PR body line 28 |
| R757-7-F1 MINOR | Stays resolved | FR is not in the delta |
| R757-8-R1 (96 kHz row), R757-8-R2 RESIDUE | Retained, not taken this round | FR:306 still says "that derivation" |
| R757-7 RR13 RESIDUE | Retained, the manager's | Issue body, not in this delta |
| R757-9 S1, S2; R757-8 S1-S5; R758-8 S1, S2; earlier optional items | Retained, optional | R757-9 S2 is the 52,008 (FR:473, AP:71) against 52,012 (AB:140, gate record) difference. AB and FR do not conflict: AB:147 calls its table the gate's record, and AP:38-39 dates 52,008 as a later measurement |

Earlier rounds are not re-opened.

## Lens results

```text
[R758] PASS Conformance - FR:473; REQUIREMENTS.md:27-45; SPLIT:3-4,115-117; AB:129-140,179-188,199-203,245,369-372,402-405,524-525 - each replaced figure marked and each listed page checked against the amended requirement; residue R758-10-R2 and R4 recorded
[R758] PASS RTL - receipts/ci_scope.txt; receipts/integrity.txt - no HDL, register, generator or constraint file in the delta or the PR; all six gitlinks equal the base; earlier RTL verdicts depend on nothing the delta changed
[R758] PASS Robustness - receipts/gate_negative_control.txt; syn/ooc/pp_resource_gate.py:755-776 - no runtime path changed; the gate refuses a changed policy row with rc 2 and does not depend on the re-marked prose
[R758] PASS Tests - receipts/gates/*; receipts/author_r9_manifest_check.txt; receipts/gate_negative_control.txt - no test in the delta; 11 gates re-run at this head with rc 0; 50 author rc files read 0; the budget reader's negative control can fail and does
[R758] PASS Docs - receipts/stale_search_at_head.txt; the 16 delta pages; docs/guides/gptp/MANAGER.md - search re-run and every contract hit classified; residue R758-10-R1 to R4 and S1 recorded with exact fixes
```

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN, residue R2 and R4 | FR:473; `REQUIREMENTS.md:27-45`; SPLIT:3-4, 115-117; AB; listed pages | R758-10 | d63b378d27c1c663034744a5b48a99c190271f58 |
| RTL | CLEAN | Delta path list; gitlinks; baseline JSON blob | R758-10 for the delta; earlier RTL verdicts carried, nothing they depend on changed | d63b378d27c1c663034744a5b48a99c190271f58 |
| Robustness | CLEAN | `pp_resource_gate.py:755-776`; `receipts/gate_negative_control.txt` | R758-10 | d63b378d27c1c663034744a5b48a99c190271f58 |
| Tests | CLEAN | `receipts/gates/`; author-r9 receipts; negative control; `ci_scope.py --selftest` | R758-10 | d63b378d27c1c663034744a5b48a99c190271f58 |
| Docs | CLEAN, residue R1 to R4, S1 | 16 delta pages; `docs/guides/gptp/`; stale search; docs gates | R758-10 | d63b378d27c1c663034744a5b48a99c190271f58 |

## Real limits

- **Scope:** I judged the round 9 delta and the pages it depends on. The charter's own decisions and figures were not re-reviewed.
- **Long gates:** I ran no Verilator, Yosys, builder or firmware bank, and no local replica. The delta is Markdown only and the one gate-read page's reader passes, but that is reasoning, not execution of those gates at this head.
- **Author gates:** I verified the published receipts by digest and rc, not by re-running them. 16 are redacted copies, as noted in check 5.
- **Hosted state:** a snapshot taken during this review, most jobs still pending.
- **Search:** pattern-based. It found the MANAGER.md miss only by a widened search, so another differently worded line could remain.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof. This round adds no hardware evidence.

## Pending manager duties

- **Long gates now apply.** With the PR classified relevant, `verilator-suites` and `yosys-portability` must conclude successfully at the exact head (AGENTS section 7). CONTRIBUTING:349-354 also requires both equivalent gates to be run locally and recorded on the PR before it is marked validated. The author states these were not run.
- **Local replica.** The signed local candidate's "Only Markdown" reason for not running jobs no longer holds. Refresh that evidence at this head or at the merge candidate.
- **Merge candidate.** Build and validate the current-dev candidate at the merge turn and link its receipts on the PR.
- **Residue checklist.** Carry R758-10-R1 to R4, R757-8-R1, R757-8-R2 and RR13.
- **Owner questions.** Put D8 to the owner (top of this report). Decide whether the owner's approval of the requirement text, given at `3f5fea24`, needs restating for NFR-LAT-03; this is carried from R757-9 and R758-8, and round 9 leaves FR unchanged.
- **Outside this repository.** The daily area measurement's column "Against the 38,040 LUT floor" no longer matches after merge.
- **Merge authorization.** Merge still needs two independent positive reviews and explicit maintainer authorization.

R758-10 FINISHED
