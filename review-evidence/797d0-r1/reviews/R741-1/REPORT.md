[R741] NEGATIVE - exact head bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a

Internal cleared-context review of kebag-logic/milan-fpga PR #815 (#797 lane D0, the documentation
inventory and verification audit) into `dev`, round R741-1. Head `bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a`,
tree `3a039c9e8d8fc05fa9e54a3976edba9f84b21819`, source base dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
Whole-PR review of the three commits `bee02d0c`, `ea8e3642`, `bd16b371`.

Verdict basis: three open MINOR findings of this round (F1, F2, F3), plus three findings of the earlier
external round R742-1 retained at this head after independent re-check (one MAJOR, two MINOR; see
"Prior public findings"). Two RESIDUE items and three SUGGESTIONs do not affect the verdict. The
generator, its freshness gate and the three one-line fixes are otherwise correct:
the population matches `git ls-files` exactly, every row's line count and every finding's line number
are right, every docs gate passes with and without submodules and without Git, and all 23 findings were
checked against their cited source and are real contradictions with correct corrections.

## Authorities reconstructed

- `AGENTS.md`, `CONTRIBUTING.md` (gates and section 6), `docs/README.md`.
- Issue #797 body (scope items 1, 2 and 6, the rules, the acceptance list), the scope addition
  issuecomment-6489587365 and the plan issuecomment-6518880512 section D0 (both by the issue author).
  D0's deliverables: a generator listing every Markdown file and README with area, lines, audience,
  purpose, described code/spec and a status with evidence; the page generated and freshness-gated;
  every normative or numeric statement on the release-facing pages verified, each contradiction written
  as a finding with file:line, source and correction, grouped by lane; no rewrites; one-line fixes only
  on pages no running lane touches.
- PR metadata (`gh pr view 815 --json ...`, receipt `receipts/pr815.json`): head and base as above.
- Sources cited by the findings: `sw/litex/milan_soc.py`, `sw/litex/boot_policy.py`,
  `sw/firmware/milan_baremetal/milan_baremetal.c`, `hdl/common/csr/milan_csr.sv`,
  `hdl/milan/milan_datapath.sv`, `hdl/ieee1722/crf/*`, `docs/reference/EGRESS_QUEUE_MAP.md`, and the
  tree's own clause citations (REQUIREMENTS.md:329, third_party/lwSRP, sw/firmware/ctrl/srp).
- Author's public evidence at `86b070d2` `review-evidence/797d0-r1` (MANIFEST, INDEX, the two head
  `bd16b371` summaries: 60 + 36 = 96 commands, all rc 0; sha256 of both summaries match the INDEX).

## Findings

### F1 - MINOR - Conformance, Docs - `docs/reference/MILAN_COMPLIANCE_MATRIX.md:262`, `:263`, `:264`, `:267` - four more rows claim the uninstantiated classifier/queue/shaper chain is implemented

Authority/evidence: D0 must write each contradiction on the release-facing pages as a finding (plan
D0 item 3). D0-021 and D0-022 record rows 265 (8.6.8.1) and 266 (8.6.8.2) as contradicted because
`milan_datapath` instantiates no classifier, queue bank or shaper since VERSION 0x0056. The same root
contradicts the neighbouring rows, which D0 did not record:

- `:262` 9.4 / 9.6 "implemented - RTL cls / classifier";
- `:263` 6.9.4 priority regeneration on receive, "RTL cls" (the transmit half, AAF/CRF TCI bytes, is true);
- `:264` 8.6.6 + Table 8-4 queue per traffic class, "implemented - RTL queues / classifier";
- `:267` 34.3 / 34.6.1 "implemented - granted slope drives the class-A queue's idleSlope".

Contradicted by `hdl/milan/milan_datapath.sv:654-664` (no general-data TX chain: classifier, per-queue
FIFOs and CBS not instantiated), `hdl/milan/milan_datapath.sv:8552-8558` ("NO SHAPER READS THE SLOPE OR
THE VERDICT HERE ... No shaper consumes either diagnostic"), `hdl/common/csr/milan_csr.sv:18-30` and
`:1996-2000` (CAP.CBS = 0), `docs/reference/EGRESS_QUEUE_MAP.md:3-8`, and the tree itself:
`git grep` finds no instance of `traffic_classifier`, `traffic_queues` or `traffic_controller_802_1q`
outside their own source files. The page states it describes the shipping image (`:3`).

Impact: the reference lane is fed by D0's findings file; it would correct two rows and leave four rows
on a release-facing page still claiming shipped behaviour that the RTL does not have. The page's
status is already `stale`, so no status is wrong, but the findings list, which is D0's deliverable for
this page, is incomplete.

Required outcome: the data file records these rows (as new findings, or by widening D0-021/D0-022's
statement set and correction to every row that depends on the uninstantiated chain), and the page is
regenerated.

Verification: `python3 scripts/docs_inventory.py --check` passes and the Findings table lists rows
262, 263 (receive half), 264 and 267, or a public reason why any of them is not contradicted.

### F2 - MINOR - Conformance, Docs - `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:23` - the D0-001 statement is marked current on another D0 page

Authority/evidence: D0-001 records `README.md:61` "ADP, ACMP, AECP, MAAP and SRP default to
bare-metal firmware." (after "[Mark II] selects each control function at build time") as contradicted
by `sw/litex/milan_soc.py:2621` (`--ctrl-mailbox` default off; the default build carries no mailbox;
argparse `store_true` at `:3838`). `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md:20-24` makes the same
statement in the same structure ("Mark II passes selected control frames ... ADP, ACMP, AECP, MAAP and
SRP are selectable per function. Its default is bare-metal control; all-fabric remains supported.
All-fabric stays the shipping default ..."), and the generated page marks it `current`, "no recorded
contradiction", Verified `D0` (`docs/DOCUMENTATION_AUDIT.md:268`). One statement cannot be both a
verified contradiction and current on two release-facing pages.

Note for the decision: `docs/ARCHITECTURE_HW_SW_SPLIT.md:3-6` and its `:39` table define a "Mark II
default placement", under which both sentences read as the Mark II design default rather than the
build default. Either reading is defensible; the inconsistency is not.

Impact: the generated status of a D0-verified page is wrong under D0's own standard (or D0-001 is a
clarity item recorded as a contradiction). The integration lane receives no finding for the page.

Required outcome: the two statements are treated the same: add a finding for
`AXIS_CORES_ON_BAREMETAL_SOC.md:23` (page becomes `stale`), or re-scope D0-001 publicly as wording and
keep both pages consistent.

Verification: regenerated page; `--check` passes; the two pages carry the same judgement.

### F3 - MINOR - Tests - `scripts/docs_inventory.py:557-578`, `:608-704` - the self-test never runs the gate function the workflow calls, nor the Git listing it runs on

Authority/evidence: AGENTS section 6, Tests: each new test can fail for the defect it claims to detect.
`selftest()` claims "the freshness gate's stale-page mutants" (`:660`), but every control calls
`is_fresh()` (`:575-578`), a second comparison; `check()` (`:557-572`), which `--check` and the workflow
step run, is never exercised. The fixture has no `.git`, so the `git ls-files` branch of `listing()`
(`:197-202`), the path every CI and local run takes, is never exercised either. Disposable mutants
(receipt `receipts/mutants.txt`, script `mutate_selftest.py`):

- `check()` compare replaced by `if True:` - selftest SURVIVED, `--check` on the real tree PASSED;
- `check()` stale branch `return 1` -> `return 0` - selftest SURVIVED, `--check` PASSED;
- `git ls-files -z` -> `git ls-files -z --cached --others` - selftest SURVIVED;
- `line_count()` off by one - selftest SURVIVED (caught only by `--check` on the real tree);
- killed as expected: quote never located, stale rule removed, banner window 1 line.
  (Two further mutants, an extra `RELEASE_FACING` alternative and keeping gitlinks in the listing, are
  equivalent at this head and are not counted.)

The gate itself is correct at this head (planted probes below), so this is a test weakness, not a
broken gate: a later regression that makes `--check` vacuous would pass both CI commands.

Required outcome: the self-test drives the function `--check` uses (or `check()` is built on
`is_fresh()`), including its exit status, and at least one control runs on a Git-initialised fixture
with an untracked Markdown file that must stay out of the population.

Verification: rerun `mutate_selftest.py`; the two `check()` mutants and the untracked-listing mutant
are KILLED by `--selftest`.

### R1 - RESIDUE - `scripts/docs_inventory.py:83-84` - a lane label in a source comment

The comment reads "The pages #797's D0 lane verified statement by statement (the plan's
"release-facing pages")." The owner's comment rule (2026-10-15) forbids lane names in source comments.
Exact fix: "The release-facing pages #797 verifies statement by statement: the README,
`docs/README.md`, guides, integration, reference, `REQUIREMENTS.md` and `FR_NFR.md`." (The generated page
and findings files may name lanes; this concerns the source comment only.)

### R2 - RESIDUE - `.github/ci-templates/docs.yml:422-424` - the step comment overstates what the gate catches

"A document added, removed or edited without regenerating the page fails here" is wider than the
gate: an edit that keeps a page's line count, first heading, `Audience:` line, cited directories,
standards and any quoted finding passes (probe p14). The generator's docstring states the scope
correctly. Exact fix: "A document added or removed, or edited in its line count, title, audience line,
cited paths or standards, or in a quoted finding statement, without regenerating the page fails here".

### S1 - SUGGESTION - `scripts/docs_inventory.py:516-519` - a `re-verify` row passes the gate once regenerated

Probe p15 (`receipts/probe_p15_reverify_accepted.txt`): a finding whose quote is on no page,
regenerated with `--write`, passes `--check` with one "re-verify: quote not found" row. This is the
designed behaviour (control "fixed statement asks for re-verification"), but `--check` could refuse a
committed re-verify row so an area lane must remove the entry, and a mistyped quote cannot sit on the
page as a passing row.

### S2 - SUGGESTION - source comments carrying the same errors as two findings

`hdl/milan/KL_pp_shadow.sv:688` and `hdl/milan/milan_datapath.sv:8651` cite 802.1Q 35.2.2.7.4 (D0-006's
miscitation), and `hdl/common/csr/milan_csr.sv:708` and `:890` say ETH_GUARD gates the LiteX
phy_crg_reset chain, which `sw/litex/milan_soc.py:2067-2070` contradicts (exported only "for future
SoC-side gating"; `self.eth_guard` has no consumer). Not D0 page scope; worth a line in the reference
lane's findings file or #746.

### S3 - SUGGESTION - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:324`

"[#509][coordination] retains the remaining bounded follow-up records" names #509, closed 2026-09-27,
as the owner of F8's remaining work. Not strictly contradicted (a closed issue still holds its record),
but the area lane should confirm F8's owner.

## Evidence by check

### (1) Generator, population, freshness gate

- Population: 210 tracked `.md` files (`git ls-files`, gitlinks excluded, no submodule content);
  no tracked README without `.md`; the page's 210 inventory rows equal that list exactly
  (`receipts/ls-files-md.txt`, `receipts/page-rows.txt`, diff empty). 22 archive Markdown pages
  (30 archive files including 8 diagrams and scripts).
- Every row's line count equals `wc -l` (+1 for an unterminated line): 210/210; every finding's line is
  the first line carrying its quote: 23/23 (`receipts/rowcheck.txt`).
- Area, audience (page line or table), purpose (first heading), describes (cited directories and
  standards) and status-with-evidence columns present for every row; summary figures (182 current,
  7 stale, 0 superseded, 21 obsolete; 89,111 lines) match the PR body.
- GENERATED marker at `docs/DOCUMENTATION_AUDIT.md:3-4`; `--check` proves the committed bytes equal a
  fresh render.
- Planted probes, each in a fresh no-submodule clone (`probe_gate.sh`, `receipts/probe_gate.txt`):
  unchanged 0; appended line 1; changed heading 1; edited finding quote in the data file 1 (row becomes
  re-verify); edited finding source 1; statement fixed on its page 1; hand-edited status cell 1;
  hand-edited quote on the audit page 1; untracked `.md` 0 (ignored); new tracked `.md` 1; tracked page
  deleted 1; untracked build-output README 0; malformed data 2; finding on an untracked page 2;
  same-length body edit 0 (outside the gate's scope, see R2).
- Rendering is independent of submodule state: `--check` fresh with submodules checked out, without
  them, and in a `git archive` export with no `.git` (`receipts/nogit-inventory-check.txt`).
- `ci/image/command-table.json` sha256 pin equals the committed script
  (`5ca0f130...b698`, `receipts/inventory-sha.txt`).

### (2) Findings and current pages

All 23 findings checked against the cited line or clause; each is a real contradiction and its
correction is right, with the F2 caveat on D0-001's reading:

| ID | Checked against | Result |
|---|---|---|
| D0-001 | `sw/litex/milan_soc.py:2621`, `:3838`; README:63-64 | holds (see F2) |
| D0-002 | `hdl/milan/milan_datapath.sv:704-720`, `:1750-1770` | holds |
| D0-003 | #75 closed 2026-09-29; `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md` exists | holds |
| D0-004 | `eff99a9c` deletes `KL_lwsrp_ctx.sv`; no tracked file; no `JOIN_TIME_MS_C` definition | holds |
| D0-005 | `KL_media_nco.sv` (2026-08-10) instantiated at `milan_datapath.sv:796`; `KL_media_grid_align.sv` | holds |
| D0-006 | tree's independent citations 35.2.2.7.2 (`third_party/lwSRP`, `sw/firmware/ctrl/srp`) | consistent; clause text not available offline |
| D0-007/008 | REQUIREMENTS.md:329 (Milan 5.3.8.10, Table 5.6); 1722.1-2021 Table 7-156 as cited across the tree | holds |
| D0-009 | `milan_baremetal.c:1086-1094`, `:1655-1668` (only call site of `phy_link_tick`) | holds |
| D0-010 | #599 closed 2026-09-29; finding page exists and records the switch-cycle acceptance | holds |
| D0-011 | #403 closed 2026-09-26; `boot_policy.py:58`; `milan_baremetal.c:1808` | holds |
| D0-012 | #400 closed 2026-09-26; `milan_baremetal.c:1814` | holds |
| D0-013 | `boot_policy.py:56`; CRF output appended to `stream_outputs` only when declared (`boot_policy.py:25-32`, `endstation_builder.py:5132`) | holds |
| D0-014 | `milan_csr.sv:885-897`, `:1578`, `:1731`, `:2389`; no 0x7D8 row | holds |
| D0-015 | `milan_csr.sv:1688`, `:2692`; datapath `o_phy_reset_n` unconnected in `sw/litex/*.py`; patch `0002` `_reset` CSR | holds |
| D0-016 | `milan_csr.sv:1724-1730` | holds |
| D0-017 | `milan_soc.py:1893-1907`, `:2084-2085` | holds |
| D0-018 | `milan_csr.sv:897`; REGISTER_MAP_CLASSES.md:101-102 | holds |
| D0-019/020 | `milan_csr.sv:1996-2000`; `EGRESS_QUEUE_MAP.md:3-8`; FR_NFR.md:50, 228-230 | holds |
| D0-021/022 | `milan_datapath.sv:654-664`; MILAN_COMPLIANCE_MATRIX.md:3 | holds (neighbours missed, F1) |
| D0-023 | as D0-019 | holds |

Current release-facing pages spot-checked (11): `REQUIREMENTS.md` (section 5/6 scope notes, VERSION
0x0002_0060 = `milan_csr.sv:201`), `docs/README.md` (the fixed row), `docs/guides/VERIFICATION_DEVELOPER.md`
(the fixed command), `docs/guides/SYSTEM_INTEGRATOR.md` (boundary, interface table held by the solution
gate), `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md` (F2), `docs/integration/INTEGRATION_GUIDE.md`
(50 MHz `axis_clk` = every `configs/*.yaml` `milan_clk_hz`), `docs/integration/QSPI_FLASHBOOT.md`
(VERSION), `docs/reference/MILAN_FEATURE_STATUS.md` (VERSION fact), `docs/reference/EGRESS_QUEUE_MAP.md`
(0x0056 claim = `milan_csr.sv:18-30`), `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` (S3), and
`docs/reference/REGISTER_MAP.md` 0x7DC (the issue's known stale example, now amended). Issue references
with pending/open wording on 23 current D0 pages were checked against their live state
(`receipts/pending-refs.txt`, `receipts/issue-states.txt`): every closed one is in past tense except S3.

### (3) One-line fixes

- `docs/guides/VERIFICATION_DEVELOPER.md:129`: `sw/litex/test_ring_dma.py` is untracked (deleted in
  `ecf18de2`); `sw/litex/test_gmii_rx_capture.py` is tracked, runs with no arguments (`:140-157`), and is a
  LiteX simulation. Correct.
- `docs/README.md:72`: "implemented" matches `docs/design/MEDIA_CLOCK_FOLLOWING.md:6` and the live
  `media_clk_resolve` block. Correct.
- `docs/reference/REGISTER_MAP.md:428`: #599 closed as completed; the linked finding records the
  switch-cycle acceptance. Correct.
- The diff touches none of CHANGELOG.md, AREA_BUDGET.md, SUBMODULES.md, TESTING.md, BUILDING.md,
  BAREMETAL_FIRMWARE.md, REBOOT_RESET.md or `docs/diagrams/` (`git diff --stat 1e80128f..bd16b371`: 10 files).

### (4) Docs gates on the committed head

Run from the head's own workflow file (`run_gates.py`, 38 gate steps of `docs-gates-0` and `docs-gates-2`
excluding the HDL reference build `gate_1`, the builder leg `gate_25_1` and the local act runner
self-test `gate_42`), with the pinned Markdown renderer and wavedrom in a scratch venv
(`receipts/gates-withsub/`, `receipts/gates-nosub/`):

- with submodules: 37/38 rc 0, including docs_check, em-dash against `1e80128f`, style, DOC_MAP, solution
  facts, submodule docs, wavedrom, PNGs, feature status, traceability, gPTP docs, bare-metal scope, code
  quality ratchets and idiom gates, doc paths, archive, TOC/anchors, the new inventory gate, AEM/sweep/
  deploy/entity shape, CI scheduling controls (`ci_gate_workflows.py --check`, evidence pins) and
  `ci_events.py --check/--selftest`. `gate_24` (compiler-absent firmware controls) passed its selftest
  half and hit the 420 s step cap in the `--absent` half; it reads no changed file.
- without submodules: every gate that the workflow runs before its submodule fetch passes (gates 7-16,
  43-47, 41), including `docs_check.py` and the new inventory gate; the later gates fail for missing
  submodules as expected.
- no Git (`git archive` export): `docs_check.py` and `check_feature_status.py` (the `docs-check-no-git`
  job) rc 0, inventory `--check` fresh (`receipts/nogit-docs-check.txt`).

### (5) Privacy and labels

Added lines (excluding the generated page and the command table) carry no host, device, address,
serial, test-plan, tool or model name and no reviewer or round label; the only lane label is the
source comment recorded as residue R1. The
generated page reproduces existing page titles verbatim, so a pre-existing findings title carrying a
bench label (`docs/findings/B14_BENCH_5603C353.md`) appears in its row; that is a findings page and is
not new text.

## Lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2; retained R742 F1-F3) | #797 acceptance, plan D0 and scope addition against `scripts/docs_inventory.json` (23/23 checked), `docs/DOCUMENTATION_AUDIT.md` rows and Findings table, 11 current D0 pages | R741-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| RTL | UNCLEAN (retained R742 F1, F3 only; own pass found nothing in RTL scope) | Diff touches no `hdl/` file (`git diff --stat`); every RTL line the findings cite verified: `milan_csr.sv:201,708,885-901,1578,1688,1724-1731,1996-2000,2389,2692`, `milan_datapath.sv:654-664,704-720,796,1750-1770,8552-8558`; `KL_pp_shadow.sv:1123`; `ethernet_packet_pkg.sv:218-222` | R741-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Robustness | CLEAN | `scripts/docs_inventory.py` refusals (malformed JSON, untracked finding page, duplicates), unterminated lines, deleted/untracked/new documents, submodule present/absent, no-Git walk, em-dash cell rewrite: probes p00-p15 | R741-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Tests | UNCLEAN (F3; retained R742 F2) | `scripts/docs_inventory.py --selftest` (21 controls) under 10 source mutants; `scripts/ci_events.py` step-count arms 51 -> 52 and `--selftest` (5270 arms) rc 0 | R741-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |
| Docs | UNCLEAN (F1, F2; retained R742 F1-F3; R1, R2 residue) | the three one-line fixes, generated page, `.github/ci-templates/docs.yml:420-433`, generator docstring, PR body figures | R741-1 | bd16b371ae5de1c4d36ea2a018e7d756c62d4b5a |

[R741] PASS Robustness - `scripts/docs_inventory.py:193-216`, `:310-337`, `:557-578`; `receipts/probe_gate.txt`, `receipts/nogit-inventory-check.txt` - population, refusals, stale/edited-quote/hand-edit detection, untracked and submodule independence checked against the generator's documented contract at this head.

## Prior public findings on this PR

Read only after the verdict, findings and ledger above were on disk. At retrieval PR #815 carried two
review-start notes, zero submitted reviews, zero inline comments, and one published round, the external
R742-1 (NEGATIVE at this same head, issue comment 6520356763, published while this round ran). Each of
its findings was re-checked independently at `bd16b371`:

| Prior finding | Re-check at this head | Disposition |
|---|---|---|
| R742 F1 MAJOR (Conformance, RTL, Docs) - `docs/integration/QSPI_FLASHBOOT.md:57-62` says nothing reads or writes the journal range, a blank-flash responder answers, and nothing survives a power cycle | `hdl/milan/KL_pp_shadow.sv:1123` instantiates `KL_nvm_backend`; `sw/firmware/milan_baremetal/milan_baremetal.c:329-331` puts both saved-state slots in `MILAN_FLASH_JOURNAL_OFFSET`, `:854` writes headers, `:1641-1670` judges both slots at boot. Contradicted; the page is marked `current` | RETAINED, open, MAJOR |
| R742 F2 MINOR (Conformance, Tests, Docs) - `docs/guides/VERIFICATION_DEVELOPER.md:32` "Migen scripts lack one aggregate runner." (and `:49`) | `scripts/run_litex_sims.sh:95-100` (INVENTORY) and `:150` `run_aggregate`; the same page names the runner at `:22`. `:49` "C has no general harness framework" needs qualifying against `sw/firmware/gtest/README.md:4-8` | RETAINED, open, MINOR |
| R742 F3 MINOR (Conformance, RTL, Docs) - `docs/reference/EGRESS_QUEUE_MAP.md:37-38` reset roles q3 gPTP, q2 class B | `hdl/common/ethernet_packet_pkg.sv:218-222` `GPTP_CLASS = 2`, `SRB_CLASS = 3`; the page's own slope table `:55-56` agrees with the package | RETAINED, open, MINOR |
| R742 R1 RESIDUE - `scripts/docs_inventory.py:83` lane label in a source comment | same as R1 here | RETAINED as RESIDUE (one item, either exact fix) |
| R742 freshness-limit note (same-length semantic edit passes) | same as probe p14 and R2 here | consistent; R2 carries the wording fix |

This round's F1, F2 and F3 are not in R742-1 and are new. R742-1 F1 and F3 sit on pages this round's
spot-check sampled for other statements only (`QSPI_FLASHBOOT.md` for VERSION, `EGRESS_QUEUE_MAP.md` for
the 0x0056 claim) and R742 F2 on the page sampled for the one-line fix; this round did not catch them.
Together with F1 and F2 here, five D0 release-facing pages carry contradictions the audit does not
record, three of them on pages marked `current`.

Lens consequence: R742 recorded F1 and F3 under RTL as well. This round's own pass found no defect in
RTL scope (the diff carries no RTL), but under AGENTS section 6 a finding attributable to several lenses
is recorded under each, so the retained findings leave RTL unclean in the ledger below.

## Limits

- Source-head execution only; no manager source bank exists at this head and none is claimed. The
  current-dev merge candidate, hosted and act acceptance are the manager's.
- Not run: the HDL reference build (`gate_1`), the builder legs (`gate_25_*`), the local act runner
  self-test (`gate_42`), `gate_24`'s `--absent` half to completion, and the replacement LiteX test (no
  LiteX environment here).
- IEEE and Milan clause texts were not available offline; clause findings (D0-006, D0-007/008) were
  checked against the tree's independent citations only.
- The current-page spot-check is a sample (11 pages), not an exhaustive re-verification.
- Physical calibration NOT RUN; no hardware evidence.

## Pending manager duties

- Merge-candidate validation on live dev: every Markdown change landing on dev before this PR makes the
  page stale (per-page line counts), so the candidate must be regenerated and `--check`ed on the
  combined tree, and running lanes will need `--write` after this lands.
- Hosted and act acceptance at the exact head.
- Carry R1 and R2 to the residue checklist.
- Re-review after the data file records F1, F2 and the retained R742 F1-F3 and F3 here is answered;
  every lens above must be covered again at the new head.

R741-1 FINISHED
