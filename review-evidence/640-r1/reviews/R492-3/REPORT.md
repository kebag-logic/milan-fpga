[R492] POSITIVE - exact head 173362fc21c33078b7feed42a24a3636907010f5

# R492-3: internal independent delta re-review of PR #698 (relates to #640), Mark II area plan

- Head `173362fc21c33078b7feed42a24a3636907010f5`, tree `fbc807d191d0c98f7fac332502e93f9c65c81138`.
- Source base and live dev: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Delta reviewed: `7387bb6f..173362fc`, one commit, `173362fc`.
  - Its message is one line with no trailers.
  - It changes only `docs/design/MARK_II_AREA_PLAN.md`: 3 lines added, 2 removed (`receipts/delta.txt`).
  - One blank line after the M3 basis table (`:837`).
  - The two-word command-proxy prefix is removed from the first line of each L11b fence (`:1167`, `:1211`).
  - Nothing else changes. No figure, record, script, RTL, policy value or submodule gitlink moves.
- The whole PR diff from `5603c353` still touches only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md`.
- Role: cleared-context internal reviewer. All five lenses applied independently at this head.
  No source edit, commit, push or GitHub write was made.

## Verdict basis

No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN at this head.

- R492-2-F1 (MINOR) is RESOLVED. Both L11b fences run as printed in a plain POSIX shell, and the prefix token is nowhere in the tree.
- R492-2-F2 (MINOR) and R493-2-R2 (RESIDUE) are RESOLVED. The M3 table ends at its last row, and the prose after it renders as a paragraph.
- Earlier findings stay resolved. The delta touches none of the lines that resolved them.
- 16 of 16 documentation gates pass at this head.
- Four wording-only RESIDUE items are retained from R492-2 (R1 to R4). R493-2-R1 is retained with R492-2-R1. None changes a figure or a claim.

## Resolution of the R492-2 findings and R493-2-R2

### R492-2-F1: the L11b reproduction commands. RESOLVED

- Where: `docs/design/MARK_II_AREA_PLAN.md:1167` and `:1211`, the first lines of the two `sh` fences under "Reproduce L11b core pricing" (`:1137`).
- At the head they read `bash -c 'cat > "$WORK/price_core.tcl"' <<'TCL'` and `flock $VIVADO_LOCK bash -c '`.
- `scripts/probe_l11b_commands.sh` extracts both fences from the page at a given revision.
  It runs them with `/bin/sh` under `env -i`, with a PATH holding only `bash`, `flock`, `cat`, `mkdir` and a stub `vivado`.
  The stub records its arguments and writes the `-log` file.
  The only probe substitution is the lock path, moved into scratch, because the host lock was held by another run.
- At `173362fc` (`receipts/probe_l11b_head.txt`):
  - fence 1 rc 0, and fence 2 rc 0;
  - the Tcl file is written. Its SHA-256 `f75186e9...` equals that of the page's Tcl body, lines `:1168-1204`, and Tcl `info complete` returns 1;
  - each of vexii, vexmin and pico gets `rc=0`, and Vivado is called three times with the documented arguments.
- Control at `7387bb6f` (`receipts/probe_l11b_prev_control.txt`): both fences fail with rc 127, "<proxy>: command not found", and no Tcl file is written.
  So the probe detects the defect it checks for.
- R492-2's own `repro_block_probe.sh`, copied unmodified to `scripts/r492_2/` (manifest digest checked), was re-run at the head (`receipts/r492_2_repro_block_probe_head.txt`).
  Fence 1 as printed: rc 0, Tcl written (1,339 bytes, the same `f75186e9...`), `info complete` 1, and both fences parse.
  Its prefix-stripping arm is now a no-op, because no prefix remains. Its "6 prefix words" line counts the whole first line, an artifact of that script's regex at a prefix-free head.
- Prefix search (`receipts/prefix_search.txt`): a whole-word search of tracked text files at the head finds the token nowhere.
  This covers the superproject and the initialised submodules. It is also absent at base `5603c353`. The control finds 2 matches in the plan at `7387bb6f`.

### R492-2-F2 and R493-2-R2: the M3 basis table. RESOLVED

- `:837` (`| AECP dispatch queue | 421 | 40 percent |`) is now followed by a blank line at `:838`, and the prose starts at `:839`.
- `scripts/table_scan.py` renders both pages with the pinned cmark-gfm and html5lib (`tools/markdown/requirements.txt`, hash-locked into a private scratch environment).
  - Head (`receipts/table_scan_173362fc.txt`): the M3 table spans source `832:1-837:42` and has 4 body rows. The last row is "AECP dispatch queue". "That displaces about 3,380 LUTs." renders as 1 paragraph. Unseparated prose after a table occurs 0 times over 30 + 9 tables. rc 0.
  - Control at `7387bb6f` (`receipts/table_scan_7387bb6f.txt`): the same table spans `832:1-847:56` with 14 body rows. The last row is "Neither lane receives credit in the default-split total.". rc 1.
- R492-2's `render_tables.py`, re-run at the head (`receipts/r492_2_render_tables_head.txt`): 30 tables and 9 tables, 0 absorbed prose rows, rc 0 on both pages.
- This also satisfies R493-2-R2's exact fix: one blank line after the dispatch-queue row.

## Prior public findings at this head

I read these only after my own pass over the delta, the gates and the probes above.

| Prior item | Status at `173362fc` | Evidence |
|---|---|---|
| R492-1-F1, F2, F3 | RESOLVED (still) | They were resolved at `7387bb6f` (R492-2). The delta changes no line in the cited ranges (plan `:571-599`, `:875-951`, `:966-1027`; AREA_BUDGET `:288-355`, `:414-416`). Lines after `:837` move down by one. |
| R492-1-R2, R3, R4; R493-1-R2 | RESOLVED (still) | No line they cite changed. `check_doc_paths.py` and `gen_toc.py --verify-anchors` pass. |
| R492-1-S1, S2 | ADOPTED | S1's reproduction now runs as printed (F1 above). |
| R492-2-F1 | RESOLVED | See above. |
| R492-2-F2 / R493-2-R2 | RESOLVED | See above. |
| R492-2-R1 / R493-2-R1 sentence length | RETAINED (RESIDUE) | Unchanged by the delta. Examples: plan `:700` and `:812`, AREA_BUDGET `:265`. |
| R492-2-R2 stale round references | RETAINED (RESIDUE) | Plan `:148` still reads "not the Round 1b baseline". Plan `:1112` still reads "Rounds 1b and 1c use committed records without new synthesis." |
| R492-2-R3 double blank line | RETAINED (RESIDUE) | Plan `:149-150`. |
| R492-2-R4 PR body prefix | RETAINED (RESIDUE) | The PR #698 body still carries the two-word prefix 99 times, in its command tables. |
| R492-2-S1, S2, S3 | Open SUGGESTIONS, unchanged | They are optional, and the delta does not touch them. |

## Findings at this head

No BLOCKER, MAJOR or MINOR finding.

### RESIDUE (wording only; for the residue checklist)

These change no figure, measurement, test, code, generated artifact or clause claim, and touch no privacy rule.

- R492-2-R1 (with R493-2-R1), Docs: sentences over ten words remain on lines added by this PR (`docs/README.md` documentation rule).
  - Examples: plan `:700` and `:812`, AREA_BUDGET `:265`. The candidate lists are R492-2's `sentence_probe.txt` and R493-2's changed-sentence audit.
  - Exact fix: split each listed sentence to ten words or fewer.
- R492-2-R2, Docs: stale round labels.
  - Plan `:148`: change "not the Round 1b baseline" to "not the current baseline".
  - Plan `:1112`: change "Rounds 1b and 1c use committed records without new synthesis." to "Rounds 1b-1d use committed records without new synthesis.", matching `:72`.
- R492-2-R3, Docs: plan `:149-150` has two consecutive blank lines. Delete one.
- R492-2-R4, Docs: the PR #698 body's command tables still put the two-word command-proxy prefix before all 99 commands.
  The plan's own fences no longer do, so the PR body now disagrees with the page it describes.
  Exact fix: drop the prefix from every command cell in the PR body.

### SUGGESTION

- R492-2-S1 to S3 stand as written in R492-2. They are optional.

## What each lens examined at this head

### Conformance

- Issue #640 body (frozen acceptance) and the stage-1 decisions in the issue comments, through the round 1d assignment 6081895732.
- Round 1c assignment 6081534590, step 5: "the exact reproduction command for the L11b core pricing". It is now met as an exact command. The fences run as printed (`receipts/probe_l11b_head.txt`).
- The R492-2-F1 required outcome: a plain POSIX shell using only bash, flock and Vivado, and a prefix token found nowhere (`receipts/prefix_search.txt`). Both are met.
- No acceptance criterion, figure or owner decision is touched by the delta (`receipts/delta.txt`).
- Clean.

### RTL

- No RTL, configuration, register map, parameter or resource record is in the delta or in the whole PR diff (`receipts/delta.txt`: name-status `5603c353..173362fc`).
- The architecture claims R492-2 checked in source sit on lines the delta does not change.
  They are `hdl/milan/milan_datapath.sv:8003`, `sw/litex/milan_soc.py` mailbox and FIFO sites, and the `pp_resource_baseline.json` route scopes.
  Their files are byte-identical to the head (`receipts/restore_check.txt`: 1,233 tracked blobs).
- The Tcl the fence writes is byte-identical to the page's body (`f75186e9...`).
  It names part `xc7a100t-fgg484-2`, `AreaOptimized_high` out-of-context synthesis, and the PicoRV32 override set, all unchanged by the delta.
- Clean.

### Robustness

- Failure paths of the now-runnable fence 2 (`scripts/probe_l11b_failure_paths.sh`, `receipts/probe_l11b_failure_paths.txt`):
  - When the stubbed Vivado fails for vexmin, the fence exits with that rc (3) and records `vexmin.rc=3`. Pico never runs.
  - When WORK is not fresh, `mkdir` fails and the fence exits with rc 1 before any Vivado call. This matches the "Fresh scratch output directory" requirement at `:1147`.
- Fence 1 needs `WORK` exported. The page says "Export the variables above" (`:1163`), and the probe runs under `env -i` with only those variables.
- The lock path `$VIVADO_LOCK` is created by `flock` on any host. It carries no host identity, and `docs_check.py`'s local-info sweep passes.
- Clean.

### Tests

16 documentation gates ran at the head with the pinned Markdown lock, and all 16 returned rc 0 (`receipts/gates_summary.txt`, `receipts/gates/`). They are:

- `docs_check.py`, with 0 findings over 201 md and 1,209 scrubbed text files, and scrub self-test 23/23;
- `check_em_dash.py --base 5603c353`, with 0 findings over 1,508 added lines, and arms 339/339;
- `check_em_dash.py --selftest`;
- `check_doc_style.py` and its `--selftest`;
- `check_doc_paths.py`, with 956 paths;
- `gen_toc.py --check`, `--verify-anchors` and `--selftest`;
- `DOC_MAP.gen.py --check`;
- `check_solution_docs.py`;
- `check_archive.py`;
- `check_hygiene.py --check`;
- `check_feature_status.py`;
- `check_gptp_docs.py`;
- `check_submodule_docs.py`.

Each new probe was shown able to fail on the defect it checks:

- The command probe fails at `7387bb6f` with rc 127.
- The table scan fails at `7387bb6f` with rc 1, naming `:837`.
- R492-2's two scripts were re-run unmodified at the head.

Clean.

### Docs

- The changed lines and their sections were read: plan `:828-848` and `:1137-1250`.
- Render check over all 39 tables of both pages. No table absorbs prose (`receipts/table_scan_173362fc.txt`, `receipts/r492_2_render_tables_head.txt`).
- One source-level hit, AREA_BUDGET `:23` followed by `<!-- milan-feature-status:end -->`, was checked by rendering.
  The HTML comment ends that table at 2 body rows, and the lines are unchanged from base. The scanner was refined to treat it as a block start.
- Links and anchors: `check_doc_paths.py` and `gen_toc.py --verify-anchors` pass.
- The PR body was read. It carries R492-2-R4 (RESIDUE).
- No MINOR or above. RESIDUE R1 to R4 is retained.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #640 body and stage-1 decisions; assignment 6081534590 step 5; plan `:1137-1223`; `receipts/probe_l11b_head.txt`, `prefix_search.txt`, `delta.txt` | R492-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| RTL | CLEAN | `receipts/delta.txt` (whole-PR name-status: two Markdown pages); Tcl body plan `:1168-1204` (SHA-256 `f75186e9...`); `receipts/restore_check.txt` (source bytes at head) | R492-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Robustness | CLEAN | plan `:1143-1163`, `:1208-1223`; `scripts/probe_l11b_failure_paths.sh` with `receipts/probe_l11b_failure_paths.txt` | R492-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Tests | CLEAN | `receipts/gates/` (16 rc files, all 0); `scripts/probe_l11b_commands.sh` and its head and control receipts; `scripts/table_scan.py` and its head and control receipts; `scripts/r492_2/` re-runs | R492-3 | 173362fc21c33078b7feed42a24a3636907010f5 |
| Docs | CLEAN (RESIDUE R492-2-R1 to R4 carried) | plan `:828-848`, `:1137-1250`, `:148-150`, `:1112`; AREA_BUDGET `:265`; `receipts/table_scan_*.txt`, `r492_2_render_tables_head.txt`; PR #698 body | R492-3 | 173362fc21c33078b7feed42a24a3636907010f5 |

## Real limits

- This is a docs-only delta review. I ran no synthesis, route, simulation or Vivado.
  - The L11b fences ran against a stub `vivado`. That proves the shell mechanics, not the 3,066 / 843 / 1,051-LUT results.
  - The verbatim host lock path was not exercised, because another run held it. The probe used a scratch lock path, and that is the only substitution.
- The gates are a subset of the docs workflow: those relevant to two Markdown pages.
  - The wavedrom, diagram-PNG, builder, SDK, idiom and selftest-only arms were not re-run.
  - The submodules `external` and `third_party/lwSRP` are not initialised in this clone. No gate I ran needed them.
- The author's published gate receipts in `review-evidence/640-r1` (tree `994453e9`) are for head `c4b8b7d3`. None are published for `173362fc`, so my own gate runs are the head evidence here.
- Hosted contexts at this head were snapshotted at 14:04:48 UTC (`receipts/hosted_checks.tsv`).
  - 10 had completed with success, including docs-check-no-git, full-ci-gate and all four Yosys shards.
  - 9 were in progress, including docs-check, elaborate and all five Verilator shards.
  - The physical gPTP context was skipped, which proves nothing.
  - I make no hosted or replica claim.
- Physical calibration NOT RUN. No hardware evidence is claimed or implied.
- No manager source bank ran at this head, and none is inferred.
- After the probes, the clone matches the exact head (`receipts/restore_check.txt`).
  - HEAD, tree and index tree match.
  - 1,233 tracked blobs are byte- and mode-identical.
  - Status is empty, including ignored files. A bytecode cache the gates wrote was removed first.
  - The three initialised submodules equal their gitlinks.

## Pending manager duties

- Carry R492-2-R1 to R4 (with R493-2-R1) to the residue checklist (#495).
- Accept the hosted and replica runs at the exact head. The docs-check and Verilator contexts were still in progress at my snapshot.
- Validate the current-dev merge candidate with the builder and native banks at the merge turn, and link the receipts.
- Obtain the external review verdict for this delta.
- Merge authorization by a maintainer is still outstanding.

R492-3 FINISHED
