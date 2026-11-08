[R753] NEGATIVE - exact head 1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33

Round R753-7, internal cleared-context review of PR #825 (#797, register reference). Exact head `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33`, tree `f6a15be8c87d2ec70163e7a0b8cb94cd32ff6afc`. Previously reviewed head: `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2` (R753-6, POSITIVE). Dev merged: `0a75aa774b89ac89351700f63dd8cbb89694af6c`.

**Why NEGATIVE:** one MINOR is open, F1. The merge brought in dev's generated audit (#815), with its D0 ledger and the rule that an area lane that fixes a recorded statement removes its entry in the same change. This PR fixes 15 such statements on its two reference pages, and no copy row of them remains anywhere. The PR does not remove the entries. So the audit that lands with this PR shows both reference pages as `stale`, with 16 open findings marked "re-verify: quote not found" and one still marked "on page". The PR body says the same findings are fixed. Everything else the round was asked to check holds at this head: the three conflict resolutions, the extract refresh, the 53-step count, the plants and every gate I ran.

## Order of work

1. Read AGENTS.md, issue #797 (body and acceptance), the PR body, and the author's published receipts at evidence commit `d04d7dfa`.
2. Ran my own pass over the delta, gates and plants. Wrote the verdict and ledger as a draft `REPORT.md`.
3. Only then read the prior review reports on the PR (R753-6, R754-6 and the residue they carry), to retain or resolve their items. Reading them changed nothing.

## The delta

The lane's own patch over dev (`git diff 0a75aa77 1de759d3`) was compared, file by file, with its patch over the round-6 base (`git diff 1f29f189 2c500d0a`). They differ in six files only: `.github/workflows/docs.yml`, `docs/DOCUMENTATION_AUDIT.md`, `docs/design/CSR_REGISTER_NOTES.md`, `docs/reference/REGISTER_MAP.md` (conflict markers only), `scripts/ci_events.py` and `scripts/register_map_soc.json`. I replayed the merge with `git merge-tree --write-tree 2c500d0a 0a75aa77` and diffed the result against `57264e30`. Every hand edit is in those five files, plus the one `check_doc_style.py` line. There are no hidden changes anywhere else (`receipts/merge_tree_replay.txt`, `receipts/merge_hand_edits_small.diff`).

### (1) The three conflict resolutions

- **`.github/workflows/docs.yml`.** The template `.github/ci-templates/docs.yml` merged cleanly and has both steps. The template's `docs-check` job has 53 steps: dev's inventory gate is step 47 and the register gate is step 52 (`receipts/docs_check_step_count.txt`). In the generated workflow, both steps sit in job `docs-gates-0`: inventory as `gate_46`, register as `gate_51`. Later ids moved up by one, with no duplicates. `ci_gate_workflows.py --check` rc 0 (`receipts/gates/ci_gate_workflows_check.rc`). Both sides' intent is kept.
- **`scripts/check_doc_style.py:37-38`.** `DOCUMENTS` holds both `REGISTER_MAP.md` and dev's `STRICTER_READINGS.md`. The gate prints "OK (25 current documents)" (`receipts/gates/doc_style.log`).
- **`docs/reference/REGISTER_MAP.md`.**
  - The page and `docs/diagrams/regmap/` are byte-identical to `2c500d0a` (`git diff --quiet` is empty).
  - Dev changed no CSR input: `git diff 1f29f189 0a75aa77 -- hdl/common/csr scripts/register_descriptions.json docs/reference/milan_feature_status.json` is empty.
  - `--check` is fresh: 203 registers, 34 modules, 240 files.
  - Dev's #839 MAC_ADDR sequencing text is carried word for word. I extracted dev's `**Sequencing (#839):**…` cell text from `0a75aa77:docs/reference/REGISTER_MAP.md` and compared it with `docs/design/CSR_REGISTER_NOTES.md:188` and `:192`. They match (VERBATIM).
  - Dev's other edit, the #599 pointer, was already on the lane's page.
  - Each register links to its notes entry (`REGISTER_MAP.md:478`, `:493`).

### (2) The SoC extract refresh, c73cecf1, and whether anything should gate it

- I re-derived every csv-derived key of the extract (`csr_csv_sha256`, regions, banks, CSR registers, constants) and `pp_windows` from the author's published export files, using my script `check_extract_vs_csv.py` (`receipts/extract_vs_export.txt`):
  - head extract vs head export: equal;
  - round-6 extract vs parent export: equal;
  - round-6 extract vs head export: differs in `csr_csv_sha256` and the constants.
- Between the two exports only seven `constant` rows change: identity, MAC and the AEM CRC (`receipts/export_csv_parent_vs_head.diff`). `aem_desc.json` is identical.
- The new station MAC decodes to `02:4B:4C:4B:4C:01` and the entity ID to `0x024B4CFFFE4B4C01`. That is dev's decided identity for `ax7101_1x1_tdm8` (`sw/builder/test_builder.py:26876-26877`).
- The page uses only regions, flash offsets, `pp_windows` and the build parameters (`scripts/register_page.py:654-678`, `:694`). So the refresh correctly leaves the page unchanged.
- **Does anything gate the file?** Not in CI. My plants confirm it:
  - P8: an unrendered constant set back to the old MAC stays green;
  - P9: the whole extract reverted to its pre-refresh content stays green;
  - P7: a rendered fact (a region origin) exits 1.
- The author's receipt `export/merge_soc_from_check.rc=1` shows the merge commit itself carried a stale extract, which every hosted gate would have passed. The PR body discloses this limit. Its refresh recipe lives only in the PR body; the repository holds only the generator's docstring. See S1. This is not a defect of this round: the page cannot go wrong through these constants.

### (3) The step count, 1de759d3

- Dev at `0a75aa77` has six "must carry exactly 52 steps" lines and `("docs-check", 52)`. The head has six "…53…" lines and `"docs-check", 53` (`scripts/ci_events.py:8117`). The template job really has 53 steps, and both `2c500d0a` and `0a75aa77` had 52, so 53 is right.
- `ci_events.py --check` rc 0 (2215 items) and `--selftest` rc 0 (5514 arms) at the head (`receipts/gates/ci_events_*`).
- P10 reverted six of the seven edits back to 52/51. The selftest then fails with 6 failures, "expected … exactly 52 steps … got … 53" (`receipts/plants/p10_ci_events_revert.*`), so the count is enforced.
- The author's earlier run at `c73cecf1` recorded the same failure (`earlier_run_c73cecf1/verify_docs_yml.rc=verify_rc=1`).

### (4) The freshness gate's plants

My plants (`plants.sh`) ran on a disposable export of the head, each restored before the next (`receipts/plants/final_restore.txt` = clean):

| Plant | rc | Gate says |
|---|---:|---|
| P0 control | 0 | fresh |
| P1 dev's hand-written page from `0a75aa77` | 1 | STALE `docs/reference/REGISTER_MAP.md` |
| P2 `MAC_CTRL` reset 0x13 to 0x17 in the flop and the defaults ROM (`milan_csr.sv:1576`, `:2002`) | 1 | STALE (4 files) |
| P3 the flop reset alone changed | 2 | REFUSED: resets to 0x17 but the ROM serves 0x13 |
| P4 `A_MAC_IFG` renamed `A_MAC_GAP` | 2 | REFUSED: register MAC_GAP needs a name and a purpose |
| P5 signal `mac_ifg` renamed `mac_gap` | 1 | STALE `rtl_fingerprint.txt` |
| P6 comment-only edit (`milan_csr.sv:9`) | 0 | fresh, as designed and as the PR's limitations state |
| P7 extract region origin +0x1000 | 1 | STALE page |
| P8 extract station MAC back to the old value | 0 | fresh (unrendered, see S1) |
| P9 extract back to the pre-refresh content | 0 | fresh (see S1) |

The author's plants (dev page 1, MAC_IFG reset 1, field rename 1, register rename 2, comment-only 0) agree with mine. Their receipts verify: 218 files checked against `receipts/INDEX.md` by size and sha256, with zero mismatches (`receipts/author_receipts_verify.txt`).

### (5) Inventory and docs steps at the head

Run at the head in a private venv with the pinned `wavedrom` (hash-pinned URL from `ci/constraints-ci.txt`) and the pinned Markdown renderer. All rc 0 (`receipts/gates/`):

- `gen_register_reference.py --check` (fresh) and `--selftest` (61/61);
- `memory_map.gen.py --check`;
- `docs_inventory.py --check` (fresh) and `--selftest` (60 controls);
- `check_doc_style.py`;
- `gen_toc.py --check`;
- `docs_check.py` (0 findings, 215 md);
- `ci_gate_workflows.py --check`;
- `ci_events.py --check` and `--selftest`.

The author's receipts cover every `run:` step of the docs jobs at the head. All their rc files are 0 except the planted and the pre-fix runs named above. `docs_inventory.py --check` being fresh does not settle F1, because the generator renders a lost quote as "re-verify" rather than failing.

## Findings

### F1 - MINOR - Docs, Conformance - `scripts/docs_inventory.json` (findings D0-006, -007, -008, -014, -015, -016, -017, -018, -041, -042, -043, -044, -058, -059, -060); `docs/DOCUMENTATION_AUDIT.md:313-314` and its Findings rows; PR #825 body "Fixed on `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md`: …" - the audit landing with this PR reports the lane's fixed statements as open

- **Authority:**
  - `scripts/docs_inventory.py:22` (#797): "a page with an open finding is never current; it renders stale".
  - `scripts/docs_inventory.py:25-28`: "a quote that is no longer on its page is rendered as needing re-verification … and an area lane that fixes a statement removes its entry in the same change, once no copy row of it remains".
  - This rule arrived with dev #815 in this merge. It is not in `2c500d0a` (`4c8b4654` is not an ancestor of it), so the sync is what makes it apply. The audit's Lane column names `reference` for both pages, which is this PR's lane.
- **Evidence:**
  - At the head, 16 Findings rows on `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md` read "re-verify: quote not found"; at `0a75aa77` there were 3.
  - Of those findings, 14 have no copy row on any page (`receipts/d0_copy_rows.txt`). D0-057 and D0-040 still have copies on other pages and must stay.
  - D0-018 is a missing-row finding. The page now has the `0x7D8` ETH_GUARD row (`REGISTER_MAP_CLASSES.md:102`), but the quoted `0x7C8–0x7D4` row stays legitimately, so the entry renders "on page" for good.
  - I spot-checked the corrections on the new pages (`receipts/d0_corrections_spotcheck.txt`):
    - D0-014: `0x7D8` section at `REGISTER_MAP.md:3148`;
    - D0-006: 802.1Q 35.2.2.7.2 (Table 35-3) at `:1769`;
    - D0-007/-008: 1722.1-2021 Table 7-156 and Milan Table 5.6 at `:1957`;
    - D0-058/-059: persistence at `:2907`;
    - D0-041: no `S50milan`;
    - D0-042: `0x4xx` judged inert at `REGISTER_MAP_CLASSES.md:83`.
  - The handoff names this state and leaves the ledger alone ("The status column is D0's ledger, and this round does not change it").
- **Impact:**
  - On dev, the generated, release-facing audit will report the integrator register reference and its classes page as stale, with fixed statements listed as open.
  - A reader cannot tell a fixed statement from one that needs work. The re-verification is left to a lane that did not make the change.
  - The PR body ("Fixed on … D0-006 to -009, -014 to -018, -040 to -044, -057 to -060") and the audit landing with it contradict each other.
  - D0-009 is not in the ledger at the head, and D0-040/-057 cannot be removed while their copies remain, so the body's list also overstates what the ledger can show.
- **Required outcome:** one of these two:
  - (a) The entries whose statement this PR fixed, and of which no copy row remains, are removed from `scripts/docs_inventory.json` in this PR. That is the 14 listed above plus D0-018 once its correction is confirmed. `docs/DOCUMENTATION_AUDIT.md` is then regenerated through `docs_inventory.py --write`. The PR body's "Fixed" sentence matches what the ledger then shows, naming D0-040 and D0-057 as kept for their other-page copies.
  - (b) A maintainer or manager decision is recorded publicly on #797 or the PR: the D0 ledger is outside this lane, and a named Issue carries these 15 entries. The PR body then says so in place of the bare "Fixed" list.
- **Verification:**
  - `docs_inventory.py --check` and `--selftest` rc 0.
  - For (a): `grep -c "re-verify: quote not found"` on the regenerated audit drops by the removed entries. No row of a removed ID remains. `REGISTER_MAP_CLASSES.md` and `REGISTER_MAP.md` stay stale only through D0-040 and D0-057.
  - For (b): the decision link is in the PR body.

### S1 - SUGGESTION - Robustness, Tests, Docs - `scripts/register_map_soc.json`; `scripts/gen_register_reference.py:20-24`, `:43-44`; `docs/DOC_GENERATION.md:176-179` - no CI check notices that the extract has gone stale against SoC changes

- **Evidence:**
  - P8 and P9 stay green.
  - The merge commit `57264e30` carried a stale extract (author `export/merge_soc_from_check.rc=1`), and only a manual export found it.
  - The refresh recipe (builder dry-run export, then `--write --soc-from`) is in the PR body only. `DOC_GENERATION.md` lists `--write`, `--check` and `--selftest` and does not mention `--soc-from`.
  - Today no rendered fact drifted. A later SoC change to a region, bank or flash offset would leave the page stale with CI green.
- **Optional change:**
  - Record in the extract the digests of the SoC sources it depends on: the shape config, `sw/litex/milan_soc.py`, and the builder files that set the constants and windows.
  - Have `--check` say "re-export required" when they move.
  - Put the refresh recipe in `docs/DOC_GENERATION.md`.

### S2 - SUGGESTION - Docs - `docs/reference/REGISTER_MAP.md:466-493`; `scripts/register_descriptions.json:1237-1251` - the #839 transmit hold is behaviour, but it sits only under "Rationale and history"

- **Evidence:** the sequencing text says what firmware must do: write both halves before any CSR-addressed transmitter starts. It now sits only on the design notes, which the page labels "Rationale and history". The page's own MAC_ADDR rows carry the byte order but not the hold. The sync rule ("no new content") made the verbatim carry the right move for this round.
- **Optional change:** in a later docs change, add a short note to the MAC_ADDR register entries in `register_descriptions.json`, for example "Transmitters that take this address hold until both halves are written (#839)", linking to the notes.

### S3 - SUGGESTION - Docs - `scripts/docs_inventory.json` `verified_pages`; `docs/DOCUMENTATION_AUDIT.md:313` - the generated page inherits "Verified: D0" by its path

- **Evidence:**
  - D0 checked the old hand-written page at `1e80128f`. This PR replaces the page wholesale, and the audit still prints "D0" in the Verified column for it.
  - Dev's #848 recorded the D0 pages in the data file so that "a page added after the baseline waits for its area lane instead of inheriting D0 by its path".
  - The new `CSR_REGISTER_NOTES.md` correctly reads "area lane".
- **Optional change:** decide, with F1, whether a page rewritten end to end after D0 should leave `verified_pages`, if the generator allows that while findings still name the page.

### Residue

- **RES1 (commit subject, no action possible):** `57264e30`'s subject says "regenerating … page" though the page came out byte-identical. The subject cannot be amended. The PR body already says "regenerated from dev's RTL: byte-identical", so no further change is needed. Recorded so the residue checklist can close it.
- **Comment rule:** the delta adds no source comment. `ci_events.py` changes only numbers, `check_doc_style.py` gains one path, and the workflow is generated. There is no new bench-lane, lane, round, reviewer or comment-ID label in source.

## Prior findings at this head

| Item | State | Evidence at this head |
|---|---|---|
| R753-6 S1 (SUGGESTION, Tests/Robustness): the STRM_SEL-write clear is caught only through loop order | Retained, optional | `scripts/register_read_sweep.py` untouched since `2c500d0a` |
| R753-6 S2 (SUGGESTION, Docs): "a provisioning write" wording | Retained, optional | same file, untouched |
| R754-6 S1, S2 (SUGGESTION) | Retained, optional | same file, untouched |
| R753-5 S1 (SUGGESTION): "since" has no stated anchor | Retained, optional | page byte-identical to `2c500d0a` |
| R754-4 S1, S2 (SUGGESTION) | Retained, optional | `register_sv.py` and the sweep's shape map untouched |
| R753-3 RES2 (`REGISTER_MAP.md:4503`) | Retained, residue checklist | page byte-identical |
| R753-3 RES3 (`CSR_REGISTER_NOTES.md:974`) | Retained, residue checklist | the notes change only at `:188` and `:192`, and the line count is unchanged |
| R754-3 R1 (`CSR_REGISTER_NOTES.md:78`) | Retained, residue checklist | unchanged |

No prior BLOCKER, MAJOR or MINOR was open at `2c500d0a`. None is reopened.

## Lens results

```text
[R753] UNCLEAN Conformance - scripts/docs_inventory.json (15 entries), docs/DOCUMENTATION_AUDIT.md:313-314 - F1: the #797 audit artifact landing with this PR lists the lane's fixed statements as open, against scripts/docs_inventory.py:22-28; the extract identity matches the decided identity (sw/builder/test_builder.py:26876-26877) and the page is byte-identical from unchanged CSR inputs
[R753] PASS RTL - hdl/common/csr/milan_csr.sv (no change in dev 1f29f189..0a75aa77 or in the lane delta); receipts/plants/p2,p3 - reset derivation and the flop/ROM cross-check still bite at this head; no RTL in the delta
[R753] PASS Robustness - receipts/plants/p3,p4 (rc 2 refusals), p6 (comment-only fresh), p7 (rendered SoC fact rc 1), p8,p9 (unrendered or stale extract green, S1 optional); merge replay shows no unreviewed hand edit (receipts/merge_tree_replay.txt)
[R753] PASS Tests - scripts/ci_events.py:7494-8117 against the template's 53 docs-check steps (receipts/docs_check_step_count.txt); --selftest 5514 arms rc 0, six-line revert fails with 6 failures (receipts/plants/p10_*); regref --selftest 61/61; docs_inventory --selftest 60; all receipts/gates/*.rc = 0
[R753] UNCLEAN Docs - scripts/docs_inventory.json, docs/DOCUMENTATION_AUDIT.md:313-314 and Findings rows, PR #825 body "Fixed on ..." sentence - F1; workflow regenerated (gate_51), DOCUMENTS keeps both pages, #839 text carried verbatim to CSR_REGISTER_NOTES.md:188,:192, docs_check 0 findings, TOC and style green
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `scripts/docs_inventory.json`, `docs/DOCUMENTATION_AUDIT.md`, issue #797 acceptance, `scripts/register_map_soc.json` vs published export, `sw/builder/test_builder.py:26876-26877` | R753-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| RTL | CLEAN | `hdl/common/csr/milan_csr.sv` (unchanged), plants P2 and P3, page byte-identity | R753-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Robustness | CLEAN (S1 optional) | plants P0 to P9, merge replay, `scripts/register_rtl.py` `extract_soc` | R753-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Tests | CLEAN (S1 optional) | `scripts/ci_events.py`, template step count, P10, `receipts/gates/*` (11 gates), author receipts (218 verified) | R753-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |
| Docs | UNCLEAN (F1; S1 to S3 optional; RES1) | `.github/workflows/docs.yml`, `scripts/check_doc_style.py`, `docs/design/CSR_REGISTER_NOTES.md:188,:192`, `docs/reference/REGISTER_MAP.md`, `docs/DOCUMENTATION_AUDIT.md`, `docs/DOC_GENERATION.md`, PR body | R753-7 | `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33` |

RTL, Robustness and Tests are covered clean at this head. Conformance and Docs must be covered again at a head that resolves F1, or after the public decision that F1(b) describes.

## Real limits

- **No builder export of my own.** I checked the extract against the author's published `csr.csv` and `aem_desc.json`, not against an export I made. The top-level Verilog the build parameters come from is not published, so the extract's `parameters` were not re-derived. The page's Build parameters section is byte-identical, and dev changed no CSR source.
- **Not every docs `run:` step ran locally.** I ran eleven docs gates. For the rest of the docs jobs I rely on the author's verified receipts.
- **The plants ran on a disposable export without submodules.** The register generator needs none.
- **Hosted evidence at the exact head is not usable.** `docs-gates-0` and `docs-gates-1` failed at "Install the pinned sv2v release" with `curl: (22) … error: 504` from the third-party release host. That is before any lane gate ran (`receipts/hosted_failed_steps.txt`, `receipts/hosted_sv2v_excerpt.txt`). Of 68 check runs, 34 were cancelled and 20 failed (`receipts/hosted_check_runs.txt`). I did not classify every failed job; the three I opened failed at install or collection steps. Hosted and act acceptance belong to the manager.
- **No manager source bank ran at this head, and I infer none.** Physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 to the author, or record the public scope decision that F1(b) describes.
- Re-run the hosted contexts after the 504. Own hosted and act acceptance.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Residue checklist: R753-3 RES2 and RES3, R754-3 R1, and this round's RES1. Optional suggestions: R753-5 S1, R754-4 S1/S2, R753-6 S1/S2, R754-6 S1/S2, and this round's S1 to S3.
- The external review at the corrected head, and maintainer merge authorization.

R753-7 FINISHED
