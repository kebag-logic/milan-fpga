[R618] POSITIVE - exact head 7cc9c492145dd9e7c5c0e1d4695a261ea8025850

# R618-1 internal independent review: issue #48 / PR #81

- Repository: Mister-M-alt/FPGA-gPTP, PR #81 (`g48-readme` into `main`)
- Exact head: `7cc9c492145dd9e7c5c0e1d4695a261ea8025850`, tree `fba21199f65fb1fc9963314495f74a5c42309b18`
- Source base: `bd466e60074539a7147e3d1613c9dcb0f93e2544` (PR base SHA matches)
- Parent authority: kebag-logic/milan-fpga `dev` at `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. A live `ls-remote` at 2026-10-11T05:52:55Z still showed `dev` at this commit.
- Review start: https://github.com/Mister-M-alt/FPGA-gPTP/pull/81#issuecomment-6105965299
- Round: R618-1, cleared context, own detached clone. I applied all five lenses.

## Verdict

POSITIVE. There are no open BLOCKER, MAJOR or MINOR findings. I recorded two RESIDUE wording items, each with its exact fix, and two SUGGESTIONs. Neither class makes the verdict negative.

## Reconstruction

1. Repository rules. There is no `AGENTS.md` or `CONTRIBUTING.md` in the tree; `git ls-files` finds neither. The working rules come from `docs/README.md`:
   - Truth order: RTL, then tests, then current guides, then dated history.
   - "Historical pages never define current behavior."
   - Run `make docs` and `make diagrams-check` before documentation commits.
   - `scripts/check_docs.py` defines the gate rules: at most ten words per sentence unit on current pages, required tokens, local link targets and archive banners.
2. Frozen scope. The issue #48 body sets acceptance items 1-4. The lane comment 6105890010 adds:
   - match parent `dev` at `ac2c5e77`, citing file and line for three statements: default on, fabric product owner, and option-off as a verification-only comparison path;
   - keep option-off documented;
   - keep the gaps issue-linked (#35 in review, #58 open, physical acceptance owed);
   - docs only;
   - add a forward note to any history page that still says default-off;
   - proof: `make docs` passes, a grep finds no current default-off page, and every parent citation resolves.
3. Authorities at `ac2c5e77`:
   - `hdl/milan/milan_datapath.sv` (L64 module header, L73 parameter, L2850-2858, L7614-7624)
   - `docs/design/GPTP_PLANE.md` (L1-55, L350-366)
   - `docs/ARCHITECTURE_HW_SW_SPLIT.md` (L155-178)
   - `README.md` (L158-174)
   - `docs/guides/gptp/MANAGER.md` (L33-35)
   - Linked issues: donor #13, #35, #58 and PR #80; parent #64, #116, #117, #488 and #511.
4. Diff `bd466e60..7cc9c492`. One commit changes five Markdown files (+78/-14). The commit message is the single line `docs: align parent integration ownership at ac2c5e77`, with no body.
5. Public evidence. I read the author packet at milan-fpga `23cf01ec`, `review-evidence/g48-r1/author`. All 24 entries in `ARTIFACTS.sha256` re-hash OK. `PR-BODY.md` matches the live PR body apart from a trailing newline. The validation logs match my own reproduction. No hosted checks are attached to the head: 0 check runs and 0 status contexts, and the repository has no `.github/`.

## Lens results

### Conformance: CLEAN

| Acceptance (issue #48) | Evidence at head | Result |
|---|---|---|
| 1. README matches current parent integration | `README.md:21-23` cites parent L73 (`parameter bit GPTP_PLANE_EN_P = 1'b1`), GPTP_PLANE L6 ("Fabric gPTP owns product time synchronization.") and L49 ("Option-off elaboration exists only for verification.") | Met |
| 2. Default ownership stated unambiguously | README, INTEGRATION, MANAGER and SOURCE_EVIDENCE each state default on plus fabric owner. INTEGRATION adds "Product configurations cannot disable the plane", which GPTP_PLANE L43-44 supports. | Met |
| 3. Option-off behaviour documented | `docs/INTEGRATION.md:33-49`, new "Option-off behavior" table. Each row's claim matches its cited parent lines (see the next table). | Met |
| 4. Donor and hardware gaps visible | `README.md:51-54` and `docs/MANAGER.md:100-115`: #35 with PR #80, #58, parent #117, parent #64/#488. The live states match: #35 open, PR #80 open and unmerged, #58 open, #117 open, #64 open, #488 open. | Met |

Every parent citation, read at `ac2c5e77` (`receipts/parent_citations_all.txt`): **31 occurrences, 14 distinct targets, 0 unresolved.** This matches the author's 31/14. For each target I checked that the cited lines say what the page claims:

| Target | Page claim | Cited text supports it |
|---|---|---|
| datapath L73 (x5) | default on | `= 1'b1` inside `module milan_datapath` (L64): yes |
| GPTP_PLANE L6 (x5) | fabric owns product time | verbatim: yes |
| GPTP_PLANE L49 (x3) | verification-only (comparison) | "exists only for verification": yes. The parent's own term "option-off comparison" appears elsewhere at `ac2c5e77` (e.g. `sw/litex/milan_soc.py:3955`, `docs/reference/REGISTER_MAP.md:1002`). |
| GPTP_PLANE L48 | one atomic bank for every consumer | verbatim: yes |
| GPTP_PLANE L43-44 (x2) | product cannot disable / keep enabled | "Product configurations enable ... builder rejects ... without it": yes |
| ARCH L165 | no supported product image | verbatim: yes |
| ARCH L165-175 (x3) | verification-only, ownerless, safe values | yes |
| parent README L167-170 (x5) | ownerless; GM/parent/path/peer delay zero; sync/asCapable zero; `tu` one; writes inert | yes, all five rows |
| datapath L7614-7624 | control TX passes straight through | `g_gptp_off`: `ctlg3_* = ctlg2_*`: yes |
| datapath L2850-2858 | PHC rate/phase select CSR face | `eff_ptp_adj_w`/`offset`/`adjust` pick `cfg_*` when off: yes |
| datapath L2850-2852 | settime remains on CSR face | "settime ... always stays with software": yes |
| parent guide MANAGER L33-35 | calibration and physical acceptance incomplete | yes |
| GPTP_PLANE L350-366 | v1.2 excludes propagation asymmetry | yes (L352, L358) |
| GPTP_PLANE L363-366 | corrections are parent constants applied once; donor tuner outside contract | yes (L363, L364, L366) |

The MANAGER row for #117 says "fabric publication". The issue #117 body confirms this: it "retains its gPTP synchronization, GM loss/return, wire protocol and fabric-publication scope". #58's title confirms the asymmetry input, calibration triple and live tuner. #64 and #488 confirm the ingress/egress split.

### RTL: CLEAN

- No RTL, script, test, bench, synthesis, Makefile or diagram change. `git diff --stat bd466e60 HEAD -- . ':!*.md'` is empty, and the `hdl`, `tb`, `bench`, `scripts`, `syn`, `Makefile` and `docs/diagrams` tree objects are identical at base and head (`receipts/scope_and_search.txt`).
- The parent RTL descriptions are accurate (L73 default, the L7614-7624 off-branch bypass, L2850-2858 PHC knob selection).
- `make -j16 lint` on an exported head copy with the pinned Verilator 5.050 (identity checked: `Verilator 5.050 2026-07-01 rev v5.050`) returned rc 0 (`receipts/lint_head_copy.txt`).
- The donor RTL claims on the touched pages ("Current shape" bullets, MANAGER delivery rows) are unchanged from base.

### Robustness: CLEAN

- All 31 parent links use a full 40-hex commit and are immutable. `ac2c5e77` is the live parent `dev`.
- All local Markdown links with fragments resolve to real headings: 16 checked, 0 bad (`receipts/anchor_check.txt`). This includes the new `INTEGRATION.md#option-off-behavior`, `MANAGER.md#open-risks` and the history note's `INTEGRATION.md#parent-ownership`.
- The history page keeps its archive banner, original path, `Archived: 2026-08-31` date and original default-off text (lines 35-36 unchanged). The diff only adds a dated forward note, in the same position as the existing 2026-10-10 #70 note. The archive-metadata gate passes.
- Time-sensitive statements ("#35 remains in review", "PR #80") are true at review time. Re-checking them at the merge turn is listed under pending manager duties.

### Tests: CLEAN

Reproduced at head (`receipts/gates.txt`):

| Command | rc / output |
|---|---|
| `make -j16 docs` | 0 |
| `make -j16 diagrams-check` | 0 |
| `scripts/check_docs.py` | 0; 11 current, 17 historical pages |
| `scripts/check_docs.py --selftest` | 0; 10 arms |
| `scripts/check_source_evidence.py` | 0; 20 exact |
| `scripts/check_source_evidence.py --selftest` | 0; 7 arms |
| `scripts/generate_diagrams.py --check` | 0; 9 assets, 3 PNGs |
| `scripts/generate_diagrams.py --selftest` | 0; 10 arms |
| `make -j16 contract` | 0 |
| `git diff --check bd466e60 HEAD` | 0 |

Default-off search (`receipts/scope_and_search.txt`):
- A case-insensitive multiline search over all 11 current Markdown pages finds no match. It covers `default(s|ed) off/disabled/clear/0`, `off/disabled by default`, `opt(s) in`, `RTL default` and `1'b0`.
- A broader grep for `GPTP_PLANE_EN|by default|comparison|option-off` across all tracked files found only default-on statements on current pages.
- History pages match only at `PROJECT_STATUS.md:20,35,36`. Lines 35-36 are the retained original; line 20 is the new forward note.

Disposable gate probes ran on exported copies (`receipts/gate_probes.txt`, `scripts/gate_probes.sh`):
- The gate still catches removal of the required token (p5, rc 1) and an eleven-word sentence in the new subsection (p6, rc 1).
- The proposed RESIDUE fix wording passes (p1, rc 0).
- The gates do not catch default-off wording (p2), a broken fragment (p3) or a stale parent revision (p4). These gaps are pre-existing and outside this docs-only issue; see SUGGESTION S-01.

### Docs: CLEAN (two RESIDUE items)

- The new prose obeys the ten-word unit rule (gate rc 0) and the truth order.
- The current pages, history note and PR body agree on default on, fabric owner and verification-only option-off.
- The PR body's parent line list (L73, GPTP_PLANE 6 and 43-49, ARCH 165-175, README 167-170) matches the pages.
- The wording defects below change no claim.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R618-1-R01 | RESIDUE | Docs | `README.md:23`, `docs/INTEGRATION.md:16` | Text reads "supports verification-only comparison builds only": "only" appears twice. It is kept because `scripts/check_docs.py:65` requires the token `comparison builds only`. | Redundant wording only; the claim is correct. | Replace `verification-only comparison builds only` with `verification comparison builds only` in both lines. This keeps the required token and the cited link. | Probe p1 (both files): `check_docs.py` rc 0. |
| R618-1-R02 | RESIDUE | Docs | `docs/history/v1/PROJECT_STATUS.md:20-21` | The note says the default-off account is "also recorded in closed issue #13". The #13 body (`receipts/donor13_body.md`) records the stale front page: software owner, integration as future work. It asks for default fabric ownership after parent PR #135. It does not itself record a parent RTL default-off. | Imprecise provenance wording in a dated forward note. No current claim, measurement or verdict changes. | Change lines 20-21 to: `> Integration note (2026-10-11, issue #48): the default-off account below` / `> preserves the earlier state; closed [issue #13](https://github.com/Mister-M-alt/FPGA-gPTP/issues/13) corrected the stale front page.` | Re-read the note against the #13 body; `make docs` rc 0 (history pages are not style-gated). |
| S-01 | SUGGESTION | Tests, Robustness | `scripts/check_docs.py` (unchanged) | Probes p2/p3/p4: the gate accepts default-off wording, broken fragments and a stale parent SHA. The author proved citations with an out-of-tree checker. | No defect at this head; a future regression would rely on manual review. | Optional follow-up issue: gate fragment anchors and pinned parent citations in-repo. Out of scope here, since the issue forbids script changes. | n/a |
| S-02 | SUGGESTION | Docs | `docs/INTEGRATION.md:44-47` | Four rows cite the same parent README L167-170. ARCH L171-174 lists the same facts one per line. | Reader convenience only. | Optional: cite ARCH L171, L172, L173 and L174 per row. | n/a |

Prior public review findings: none to resolve. When fetched at review start, PR #81 had 0 reviews and 0 review comments. Its issue comments were only the two review-start notices. Issue #48's comments were only the lane, TAKEN and REVIEW READY posts (`receipts/pr81_*.json`, `receipts/issue48_comments.json`). This is round 1.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #48 body and lane comment; 31/14 parent citations at `ac2c5e77` with cited text; live states of donor #13/#35/#58/PR #80 and parent #64/#116/#117/#488/#511 | R618-1 | 7cc9c492145dd9e7c5c0e1d4695a261ea8025850 |
| RTL | CLEAN | Non-Markdown diff (empty); tree-object equality for hdl/tb/bench/scripts/syn/Makefile/diagrams; parent datapath L64/L73/L2850-2858/L7614-7624; `make lint` on head copy rc 0 | R618-1 | 7cc9c492145dd9e7c5c0e1d4695a261ea8025850 |
| Robustness | CLEAN | Full-SHA pinning; live parent dev; 16 fragment anchors; history archive metadata and dates; time-sensitive status lines | R618-1 | 7cc9c492145dd9e7c5c0e1d4695a261ea8025850 |
| Tests | CLEAN | `make docs`, `make diagrams-check`, 6 underlying gates/selftests, `make contract`, `diff --check`; own default-off search; 8 gate probes; author packet hashes (24/24) | R618-1 | 7cc9c492145dd9e7c5c0e1d4695a261ea8025850 |
| Docs | CLEAN | README.md, INTEGRATION.md, MANAGER.md, SOURCE_EVIDENCE.md, history PROJECT_STATUS.md at head vs base; the other 6 current pages for stale defaults; commit message; PR body | R618-1 | 7cc9c492145dd9e7c5c0e1d4695a261ea8025850 |

## Real limits

- No manager source bank runs at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts plus my own focused reproduction listed above.
- I did not run the full `make` (tb/bench suites), the OOC synthesis or any builder/parent bank. The change touches no RTL, script or test bytes.
- No hosted CI contexts exist for this head. Hosted/act acceptance belongs to the manager.
- Physical calibration NOT RUN; no hardware evidence is implied. The pages correctly keep parent #117, #64 and #488 open.
- Semantic citation checks are reviewer reading of the cited lines. No in-repo gate enforces them (S-01).
- My default-off search is a pattern search plus a broad grep and manual read of the matches; it cannot rule out every paraphrase.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (source base `bd466e60`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`) with the builder and native banks, and link the receipts on the PR.
- At merge, re-check the time-sensitive gap rows: `README.md:51` and `docs/MANAGER.md:104` (#35 "in review" with PR #80). If PR #80 merges first, those rows become stale. Also re-check that parent `dev` has not moved in a way that changes the cited claims.
- Carry R618-1-R01 and R618-1-R02 to the residue checklist.
- Collect the second independent review before merge.

## Exact-head restoration

All probes ran on exported copies under the packet's `scratch/`; the review clone was never modified. Final check (`receipts/head_integrity.txt`):
- HEAD and tree match the published head; `write-tree` = `fba21199`.
- The status is clean, including ignored files.
- Index and worktree diffs are empty.
- All 106 tracked blobs re-hash to their index bytes, with no mode mismatches.
- There are 0 gitlinks: this repository has no submodules, so no gitlinks need checking.

Publishable receipts are listed in `MANIFEST.sha256`.

R618-1 FINISHED
