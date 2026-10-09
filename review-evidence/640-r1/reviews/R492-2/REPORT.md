[R492] NEGATIVE - exact head 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783

# R492-2: internal independent re-review of PR #698 (relates to #640), Mark II area plan

- Head `7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`, tree `2f8dac43d7c0efd0350b328818d89dc1cbebca47`.
- Source base and live dev: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Delta reviewed: `c4b8b7d3..7387bb6f`, eight one-line commits with no trailers.
  - Round 1c: `da590e49`, `72ee3083`, `72a215f1`, `30b539ad`, `cee00f59`, `39258a14`.
  - Round 1d: `9b6a04e1`, `7387bb6f`.
- Only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` change.
  The whole PR diff from `5603c353` touches the same two files.
  No RTL, script, record, policy value or submodule pin changes.
- Role: cleared-context internal reviewer. All five lenses applied independently.
  No source edit, commit, push or GitHub write was made.

## Verdict basis

Two MINOR findings are open, so the verdict is NEGATIVE.

- F1: the adopted L11b reproduction command fails as printed (rc 127 in a clean shell).
- F2: a new table absorbs ten following prose lines when rendered.

Conformance, Tests and Docs are unclean. RTL and Robustness are clean.

The substance of the round is sound:

- R492-1-F1, F2 and F3 are resolved.
- The owner's block-RAM decision is carried in full.
- 58 of 58 recomputed figures match the committed record and the stated lever ranges.
- 23 of 23 documentation and resource-policy gates pass at this head.

Both open findings need only small text edits.

## Findings

### R492-2-F1 MINOR - the L11b reproduction command depends on a host-local proxy and fails as printed

- Lenses: Conformance, Tests, Docs.
- Where: `docs/design/MARK_II_AREA_PLAN.md:1166` and `:1210`.
  These are the first lines of the two `sh` fences under "Reproduce L11b core pricing" (`:1136`).
  The commit `cee00f59` introduced them.
- Authority and evidence:
  - The round 1c assignment (#640 comment 6081534590), step 5, adopted R492-1-S1.
    It asks for "the exact reproduction command for the L11b core pricing".
  - Each command starts with a two-word command-proxy prefix.
    That prefix is a host-local output wrapper.
    No other tracked file in the repository uses it.
    No documentation names it as a dependency.
    It is absent at base `5603c353`.
  - `receipts/repro_block_probe.txt` extracts both fences byte for byte.
    It runs the first fence with `PATH=/usr/bin:/bin`.
    Run as printed: `rc=127`, "<proxy>: command not found", and no Tcl file is written.
    Without the prefix: `rc=0`, a 1,339-byte Tcl file, and Tcl `info complete` returns 1.
    Both fences parse with `bash -n`; parsing does not catch this failure.
- Impact: a cold reviewer without that wrapper cannot run the published reproduction.
  So the evidence path for the 3,066 / 843 / 1,051-LUT core pricing does not work as written.
  That pricing is the basis of the 1,700-LUT M8b lever.
  The step-5 deliverable is therefore not met as an exact command.
- Required outcome: both fenced commands run in a plain POSIX shell.
  They use only the tools the section names: bash, flock and Vivado.
  Remove the prefix from `:1166` and `:1210`; no other byte needs to change.
- Verification: rerun `scripts/repro_block_probe.sh` at the fix head.
  Running the first fence as printed must give rc 0 and write the Tcl file.
  A repository-wide search must find the prefix token nowhere.

### R492-2-F2 MINOR - the M3 basis table absorbs the ten prose lines after it

- Lenses: Docs.
- Where: `docs/design/MARK_II_AREA_PLAN.md:832-847`.
  The table at `:832-837` has no blank line before the prose at `:838-847`.
  The commit `30b539ad` introduced it, applying the R493-1-R1 table without a following blank line.
- Authority and evidence:
  - Under GFM, a table runs until the first blank line.
    The repository's pinned renderer (cmark-gfm, as `scripts/gen_toc.py` uses) therefore renders `:838-847` as table rows.
  - `receipts/render_tables.txt` lists the ten lines rendered as one-cell rows.
    Examples: "That displaces about 3,380 LUTs."
    Also: "M10 remains planned there at 1,200 LUTs (900-1,500)."
    Also: "Neither lane receives credit in the default-split total."
  - It is the only such defect: the plan has 30 tables and AREA_BUDGET has 9.
- Impact: the rendered M3 share table gains ten rows with empty "LUT basis" and "Share" cells.
  M3's displaced total, its overhead and the whole M10 pricing and dependency statement then read as M3 basis scopes.
  No figure changes.
  But the M10 figure and the zero-credit rule are shown inside another lever's basis table.
  I was not sure this counts as wording only, so the rule makes it MINOR.
- Required outcome: the table ends at `:837`, and `:838-847` render as paragraph text.
  One blank line after `:837` is enough.
- Verification: `scripts/render_tables.py docs/design/MARK_II_AREA_PLAN.md` reports 0 absorbed prose rows.

### RESIDUE (wording only; for the residue checklist)

- R492-2-R1, sentence length (`docs/README.md:140`).
  - The repository's own analyser counts sentences on lines added in this delta.
    The receipt is `receipts/sentence_probe.txt`.
  - Round 1d lines alone: 36 sentences over ten words in the plan and 25 in AREA_BUDGET.
    Across rounds 1c and 1d the counts are 46 and 48.
  - Most are 11 to 14 words. The tokenizer counts `56,948` and `121.5` as two words each.
  - Examples: plan `:757` (14 words) and AREA_BUDGET `:255` and `:285` (14 words).
  - This continues R492-1-R1 and R493-1-R1. Neither page is in the style gate's list, so the gate passes.
  - Exact fix: split each listed sentence to ten words or fewer.
- R492-2-R2, stale round references.
  - Plan `:148`: "not the Round 1b baseline" should read "not the current baseline".
  - Plan `:1111`: "Rounds 1b and 1c use committed records without new synthesis." should read "Rounds 1b-1d ...", matching `:72`.
- R492-2-R3: plan `:149-150` has two consecutive blank lines. Delete one.
  This was already present at `c4b8b7d3`.
- R492-2-R4: the PR body's two command tables put the same host-local prefix before all 99 commands.
  Its "How to reproduce" section tells the reader to run that table.
  Exact fix: drop the prefix from every command cell, or state that it is optional.

### SUGGESTION

- R492-2-S1: cross-reference the block-RAM position in the partial-flip scenario table.
  Partial central clears 38,040 on LUTs (`:930`).
  But at the 50-tile hold, the memory ledger puts partial placement at 126.5 tiles (`:796-798`), five over the ceiling.
  The preflight's 147,360 B (AECP absent) maps to about 36 tiles at 4 KiB.
  Stating that next to the row would show both resources for each fallback.
- R492-2-S2: name the fabric-AECP to firmware-ACMP state face as a partial-placement cost.
  Examples are stream info and connection-change notifications.
  The partial case reuses the full split's 1,000-LUT allowance (`:897-902`), whose basis (`:668`) does not list this face.
- R492-2-S3: give M6/M7 a maximum block-RAM debit, as M2 has (+2).
  M7 "moves eligible gPTP tables into block RAM" (`:558`).
  The ledger leaves one tile before conditional reclamation and treats M6/M7 as unpriced (`:764`).

## Prior public findings at this head

I read these only after my own pass and the draft ledger above.

| Prior item | Status at `7387bb6f` | Evidence |
|---|---|---|
| R492-1-F1 split-aware measurement | RESOLVED | M0s is lane "0s, now through week 3" (`:966`). It is owned by the manager's resource bench. Step 1 routes integrated F0-F4 with fabric AECP; step 2 follows F5's merge. Both come before week 4 and the default flip (`:983-1003`). A late F5 is a reported missed checkpoint (`:996-999`). D7 uses M0s figures (`:1011-1016`). Split-aware recipe and gate coverage precede both routes (`:1018-1027`). AREA_BUDGET `:336-355` and `:414-416` state the same order. The F0-F5 and M9 rows name M0s as a dependency. |
| R492-1-F2 M8a basis | RESOLVED | The 823 and 873 figures are now "pre-packing LUT cells" (`:576-580`). The 3,231 anonymous cells get zero credit. Both match `649_RESOURCE_MAP_AND_SENSITIVITY.md:262-283`. The 50/75/100 % packing bracket is principled: one LUT site holds at most two cells. M8a is repriced to 1,000 (400-1,500): 448, 1,022 and 1,596, each rounded down. All dependent figures are recomputed and mirrored in AREA_BUDGET. |
| R492-1-F3 no-split and partial flip | RESOLVED | No-split is 45,667 before M3/M10 and 41,867 with them (`:884-887`). The partial case is priced with its assumptions (`:889-916`). Its retained 10,095 and removal basis 8,012 derive from `ooc-1x1` scopes. Both bars are tabled for all nine cases (`:921-931`). Gaps and the needed ruling are stated (`:940-951`). AREA_BUDGET `:288-330` matches. |
| R492-1-R1 sentence length | RETAINED as R492-2-R1 | Shortened where touched, but new long sentences were added. |
| R492-1-R2 bare references | RESOLVED | No bare issue number remains outside links on either page. All listed code paths are linked. 116 relative links resolve. |
| R492-1-R3 present tense in history | RESOLVED | `:153-154` and `:173-174` are now dated. `:1118` is headed "Historical mapping at `e6172750`". A related stale round label remains as R492-2-R2. |
| R492-1-R4 double blank line (AREA_BUDGET) | RESOLVED | AREA_BUDGET has no consecutive blank lines. The plan's older pair is R492-2-R3. |
| R492-1-S1 core reproduction | ADOPTED, now F1 | Sizes, digests, Tcl and serial lock-held run are present. The printed command fails without the host-local prefix. |
| R492-1-S2 surviving M2 FIFOs | ADOPTED | The names exist in `sw/litex/milan_soc.py`: `tx_sf` `:1612`, `mac_tx_cdc`/`mac_rx_cdc` `:1672-1674`, `milan_axil_cdc` `:805`, `memory_port_cdc*` `:2246`, `descmem_*`/`respmem_*`/`nvmmem_*` `:1128-1281`. |
| R493-1-R1 long prose | RETAINED as R492-2-R1 | Both exact fixes were applied. The table fix produced F2. |
| R493-1-R2 links | RESOLVED | Plan `:3`, `:9` and `:419-420` and AREA_BUDGET `:143` and `:152` are linked. They resolve. |

## Round 1d: the owner block-RAM decision (6081706413, assignment 6081895732)

| Required | At head | Judgement |
|---|---|---|
| Up to about 50 RAMB36 tiles (224 KB at 4.5 KB) | Plan `:42`, `:699-703`, `:722-726`; AREA_BUDGET `:222-224`, `:249-251` | Met. The plan also shows that 224 KiB at 4 KiB usable per tile needs 56 tiles. It prices that case (115.5 tiles after reclamation) without changing the owner's threshold. That is the published reading of the gap between 50 tiles and 224 KB, not a private choice. |
| F5 preflight 147,360 B and 94,688 B | Plan `:705-720`; AREA_BUDGET `:225-228` | Met. Comment 6081556432 confirms the sections: 56,948 + 3,458 + 0 + 78,744 + 8,192 = 147,342, plus 18 B alignment. Pools are counted once, and AECP is absent. |
| RAMB36 ledger line | Plan `:733-741`; AREA_BUDGET `:232-240` | Met. Base 74/27 = 87.5; L2 removals -6.5 (AECP 6 RAMB36, SRP 1 RAMB18); mailbox +6 (1 + 10 RAMB18); CPU-memory reuse -18.5 (#649 BIOS ROM/SRAM 18 + 1); firmware +50; M2 +2. Total 120.5. Reserve 13.5 and ceiling 121.5 are kept. |
| Fabric block RAM that gives way beyond 50 tiles | Plan `:769-794`; AREA_BUDGET `:264-272` | Met. The eleven tiles are the full residual wrapper partition of the route record. The scopes total 10 RAMB36 + 2 RAMB18, and together with 6.5 credited tiles they cover the wrapper's 16/3 exactly. Next come M2's deferral, then M6/M7, then a manager ruling. |
| Flip and M0s report against the ledger | Plan `:803-813`, `:1001-1003`; AREA_BUDGET `:277-286` | Met. Both M0s routes, the default flip and M9 report this, with the ruling 6081705916's census duties. |

## What each lens examined

### Conformance

- Issue #640 body (frozen acceptance).
- The decisions in comments 5988586965, 5990755268, 5991591637, 5991605450, 5991626132, 5991695093, 5991737927, 5991745829, 5993114362, 6080904058, 6081534590, 6081706413 and 6081895732.
- The #665 comments 6081556432 and 6081705916.
- Each was checked against plan `:25-63`, `:405-437`, `:450-482`, `:571-599`, `:695-813`, `:875-951`, `:953-1035` and `:1064-1070`, and against AREA_BUDGET `:156-356`.
- Every assignment step for rounds 1c and 1d is met except step 5's "exact reproduction command" (F1).
- The 19 issue-comment links on both pages each resolve to the issue they name (`receipts/comment_link_probe.txt`).

### RTL

- No RTL is in the diff.
- Architecture claims in the changed text were checked in source at the head:
  - `KL_pp_shadow` is instantiated at module scope (`hdl/milan/milan_datapath.sv:8003`).
  - The mailbox datapath side is held idle (`sw/litex/milan_soc.py:2548-2552`).
  - The surviving FIFO names exist (see R492-1-S2 above).
- The route-record scope names and the per-scope RAMB36/RAMB18 used by the memory ledger come from `syn/ooc/pp_resource_baseline.json` (`route-1x1.record.scopes`). The partition is complete (`receipts/recompute_r492_2.txt`).
- No finding.

### Robustness

- The plan's failure and alternate paths:
  - Reuse not confirmed: 139 and 128 tiles, both over the ceiling, so reuse is a prerequisite (`:766-767`).
  - 56-tile packing: 115.5 (`:788-789`).
  - Partial placement at the 50-tile hold: 126.5, over the ceiling; M0s must substitute measured use (`:796-801`).
  - Ceiling exceeded or evidence missing: the flip is prevented (`:812-813`; AREA_BUDGET `:285-286`).
  - Late F5: the checkpoint is reported missed, never passed (`:996-999`).
  - Unpriced debits: they are charged before a LUT saving is accepted (`:764-765`).
  - The D5 revert and the zero-growth primitive policy are unchanged.
- No finding. S1 and S3 are suggestions.

### Tests

- 23 gates were rerun independently at the head: 23 of 23 rc 0 (`receipts/gates_summary.txt`, `receipts/gates/`).
  They include `check_em_dash.py --base 5603c353`, `gen_toc.py` (selftest, anchors, check), `docs_check.py` with and without git, and `pp_resource_gate.py check-baseline`.
- My checker `scripts/recompute_r492_2.py` derives each figure from the record and the stated lever ranges, then finds it on the page(s) that print it: 58 of 58.
  Its mutation control plants two changed figures, and the checker fails with rc 1, naming both (`receipts/recompute_mutant.txt`).
- `scripts/repro_block_probe.sh` exercises the documented reproduction: F1.
- Finding F1.

### Docs

- Both changed pages were read in the delta and in full at the affected sections.
- Relative links and anchors: 116 of 116 resolve (`receipts/link_probe.txt`), using the repository's anchor algorithm.
- Render check over 39 tables (`receipts/render_tables.txt`): F2.
- No stale pre-round figure remains on either page or elsewhere under `docs/`. I searched for 31,067, 35,067, 27,067, 32,767, 36,367, 6,973, 2,973, 18.33 %, 7.82 %, M8a's 1,600 and 45,067.
- The sentence probe and the PR body were read.
- Findings F1 and F2, and residue R1 to R4.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #640 body; decision comments listed above; #665 6081556432, 6081705916; plan `:25-63`, `:405-482`, `:571-599`, `:695-1070`; AREA_BUDGET `:156-356`; `receipts/comment_link_probe.txt` | R492-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv:8003`; `sw/litex/milan_soc.py:805, 1128-1281, 1612-1674, 2246, 2548-2552`; `pp_resource_baseline.json` route scopes; `MAILBOX_SPLIT.md` "Measured area"; `649_RESOURCE_MAP_AND_SENSITIVITY.md:262-287` | R492-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Robustness | CLEAN | plan `:733-813`, `:875-951`, `:983-1027`, `:1029-1062`; AREA_BUDGET `:242-286`, `:316-330`; record tolerances and ceiling | R492-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Tests | UNCLEAN (F1) | `receipts/gates/` (23 rc files); `scripts/recompute_r492_2.py` with `receipts/recompute_mutant.txt`; `receipts/repro_block_probe.txt` | R492-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Docs | UNCLEAN (F1, F2) | both pages; `receipts/render_tables.txt`, `link_probe.txt`, `sentence_probe.txt`; PR #698 body; stale-figure search | R492-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |

## Real limits

- This is a docs-only review. I ran no synthesis, route, simulation or Vivado.
  All LUT and memory figures are committed records, linked measurements or labelled estimates.
  I checked that they are consistent, not that they will hold.
- I did not run the author's evidence-packet scripts; they are not published at this head.
  My arithmetic is my own.
- Gates ran with the pinned Markdown environment.
  The `protocol-processor`, `gptp-processor` and `verilog-axis` submodules were initialised at their gitlinks.
  `external` and `third_party/lwSRP` were not, and no gate I ran needed them.
  I ran a subset of the docs workflow: the gates relevant to two Markdown pages.
  The wavedrom, diagram-PNG, builder, SDK, idiom and selftest-only arms were not rerun.
- Hosted contexts at this head were snapshotted shortly after 13:46 UTC (`receipts/hosted_checks.tsv`).
  - 10 had succeeded, including docs-check-no-git, full-ci-gate and all four Yosys shards.
  - 9 were in progress, including docs-check and every Verilator shard.
  - The physical gPTP context was skipped, which proves nothing.
  - I make no hosted or replica claim.
- Physical calibration NOT RUN. No hardware evidence is claimed or implied.
- No manager source bank ran at this head, and none is inferred.
- After the probes, the clone matches the exact head (`receipts/restore_check.txt`):
  - HEAD, tree and index tree match.
  - 1,233 tracked blobs are byte- and mode-identical.
  - Status is empty, including ignored files.
  - The submodule checkouts equal their gitlinks.
  - Bytecode caches the gates wrote during this session were removed before that check.

## Pending manager duties

- Route F1 and F2 to the executor. Both are text edits, and neither changes a figure.
  Then re-review at the fix head.
  F1 and F2 touch only the Docs, Tests and Conformance scope; RTL and Robustness stay covered unless the fix changes their artifacts.
- Carry R492-2-R1 to R4 to the residue checklist (#495).
- Publish the author's arithmetic scripts if the PR body's reproduction is to depend on them.
- Accept hosted and act runs at the exact head.
  Validate the current-dev merge candidate with the builder and native banks at the merge turn.
- Obtain the external review verdict for this delta. Merge authorization is still outstanding.

R492-2 FINISHED
