# [A436] merge-dev round 2, PR #616 (#451)

Status: DONE, pending the delta review. Nothing pushed.

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5883651809
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5883658963
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5883709985

## Merge head and tree

| Item | Value |
|---|---|
| Merge head (local only, not pushed) | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |
| Tree | `147d1797e2f833d0e42f5fbf3be00c650320607f` |
| Parents | `0e5ae9c82bbdb5abc3feba84f07d0e6481254906` (branch), `13eda870d1a6cf3f946fc228a98862366b08d102` (dev) |
| Message | "Merge dev into 451-tdm8-first-light": one line, no body, no trailers (`git cat-file -p HEAD`) |
| Stale-statement commit | none; the search found nothing (below) |
| Remote branch | still `0e5ae9c8` (`git ls-remote`); remote `dev` still `13eda870` |
| `protocol-processor` gitlink and checkout | `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3`, equal to dev's |

## Starting state

- `origin` is `https://github.com/kebag-logic/milan-fpga.git`.
- Branch `451-tdm8-first-light` was at `0e5ae9c82bbdb5abc3feba84f07d0e6481254906`, clean.
- `git fetch origin dev` returned `13eda870d1a6cf3f946fc228a98862366b08d102`, as expected.
- Merge base `7390b43627032c71c470e2aa8d0845eb5b740663`. Dev's first-parent
  merges since then: PR #614 (builder YAML hex declarations), PR #603 (#602),
  PR #615 (#607) and PR #609 (#590, #592, #599). In the three shared files, the
  matrix rows come from `f7660247` (PR #603) and `792a57b0` (PR #609).
- `git merge-tree --write-tree --name-only HEAD origin/dev` reported one conflict,
  `docs/reference/MILAN_COMPLIANCE_MATRIX.md`. `docs/findings/README.md` and
  `docs/litex/CLOCK_DOMAINS.md` auto-merged.
- All four gitlinks were identical on both sides before the merge:
  `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor`
  `c951a9ff`, `third_party/verilog-axis` `48ff7a7e`.

## Merge procedure

1. `git merge --no-ff --no-commit 13eda870`. The only conflict was the matrix.
2. Resolved the matrix hunk (below) and ran `git add` on it.
3. `git commit -m "Merge dev into 451-tdm8-first-light"`.
4. `git -C protocol-processor rev-parse --show-toplevel` returned the submodule
   directory itself, not the parent.
5. `git submodule update -- protocol-processor` returned 0. The checkout is
   `c951a9ff`, equal to the gitlink.

## Resolved hunk: `docs/reference/MILAN_COMPLIANCE_MATRIX.md`, section 3 (IEEE 1722-2016, AVTP)

The two sides edited adjacent rows:

- dev's #602 (PR #603) rewrote row 4.4.4.3;
- this branch's `0e5ae9c8` rewrote row 4.4.4.5 / .9.

Neither side touched the other's row. The resolution takes dev's 4.4.4.3 and
this branch's 4.4.4.5 / .9. Row order is unchanged.

### Before: the conflicted hunk, verbatim (lines 206 to 212 of the conflicted file)

```text
<<<<<<< HEAD
| 4.4.4.3 | mr — toggled on media-clock change, held ≥ 8 AVTPDUs | implemented — `KL_media_clock_restart`; RTL tkdiag + milan_dp |
| 4.4.4.5 / .9 | tv + avtp_timestamp (mod-2³² gPTP ns) | implemented -- RTL avtp_stream, aaf; SILICON latency = presentation offset was measured on the I2S shape BEFORE #386: every in-tree I2S shape now renders its DAC through the render setpoint stage (8 media ticks more, constant), so that figure predates the shipped gateware and a re-measurement rides #117's bench; the accept-to-render constant is digital-proven in `tb/verilator/milan_dp` (the true-ratio leg, #386); the TDM render lane is clocked on the shipping AX7101 1x1 TDM8 shape (#447), and [TDM8 first light](../findings/451_TDM8_FIRST_LIGHT.md) (#451) decoded its eight slots in order; its silicon figure rides #117 |
=======
| 4.4.4.3 | `mr` toggles on source change or selected-CRF disruption/received toggle; held >= 8 AVTPDUs | implemented: `KL_media_clock_restart`; tkdiag holds/merging and milan_dp controls. PHC-only re-base is excluded by the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355); `tu` and render re-base remain independent |
| 4.4.4.5 / .9 | tv + avtp_timestamp (mod-2³² gPTP ns) | implemented -- RTL avtp_stream, aaf; SILICON latency = presentation offset was measured on the I2S shape BEFORE #386: every in-tree I2S shape now renders its DAC through the render setpoint stage (8 media ticks more, constant), so that figure predates the shipped gateware and a re-measurement rides #117's bench; the accept-to-render constant is digital-proven in `tb/verilator/milan_dp` (the true-ratio leg, #386); the TDM render lane is not clocked on any shipping build, its silicon figure rides #117 |
>>>>>>> 13eda870d1a6cf3f946fc228a98862366b08d102
```

The upper half is this branch at `0e5ae9c8`, and its 4.4.4.3 is the merge-base
text. The lower half is dev at `13eda870`, and its 4.4.4.5 / .9 is the
merge-base text.

### After: the resolved rows, verbatim (lines 206 and 207 at `caa1df66`)

```text
| 4.4.4.3 | `mr` toggles on source change or selected-CRF disruption/received toggle; held >= 8 AVTPDUs | implemented: `KL_media_clock_restart`; tkdiag holds/merging and milan_dp controls. PHC-only re-base is excluded by the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355); `tu` and render re-base remain independent |
| 4.4.4.5 / .9 | tv + avtp_timestamp (mod-2³² gPTP ns) | implemented -- RTL avtp_stream, aaf; SILICON latency = presentation offset was measured on the I2S shape BEFORE #386: every in-tree I2S shape now renders its DAC through the render setpoint stage (8 media ticks more, constant), so that figure predates the shipped gateware and a re-measurement rides #117's bench; the accept-to-render constant is digital-proven in `tb/verilator/milan_dp` (the true-ratio leg, #386); the TDM render lane is clocked on the shipping AX7101 1x1 TDM8 shape (#447), and [TDM8 first light](../findings/451_TDM8_FIRST_LIGHT.md) (#451) decoded its eight slots in order; its silicon figure rides #117 |
```

### Checks on the resolution

- The resolved file has no conflict markers.
- Against dev `13eda870` it differs by exactly this branch's one line, 4.4.4.5 / .9.
  The `-U0` changed lines equal `git diff 7390b436 0e5ae9c8` for the file.
- Against `0e5ae9c8` it differs by exactly dev's four lines: 5.4.2.15 / .16,
  5.3.11.1 and 4.4.4.3 from #602, and 7.4.42.2 from #609. The `-U0` changed lines
  equal `git diff 7390b436 13eda870` for the file.
- Both rows keep their links: the #602 ruling on 4.4.4.3 and the first-light page
  on 4.4.4.5 / .9. Neither row describes the other lane's behaviour.
- The resolved tree differs from `git merge-tree`'s automatic result only in this
  file.
- The table shape is unchanged: 143 table lines at dev, at `0e5ae9c8` and at the
  merge. In the source and when rendered (`receipts/table_cells.py`), all 14 tables
  have a constant cell count in every row. Each clause row appears once; the only
  repeated lines are the section header rows.

## Auto-merged files

- `docs/findings/README.md`. Dev's #609 reworded the #397 row, and this branch
  added the #451 row. The merge has 10 rows: the #451 row first (the index is
  newest first), then dev's nine rows in dev's order, one of them the reworded
  #397 row. No row is duplicated or lost. The single table has 3 cells in every
  row, in the source and when rendered.
- `docs/litex/CLOCK_DOMAINS.md`. Dev's #607 (PR #615) added six lines near line
  345. This branch's reworded line 140 is intact.

## Net change

- `git diff 0e5ae9c8 caa1df66` equals `git diff 7390b436 13eda870` in numstat and
  in changed lines, so the merge brings exactly dev's delta.
- Against dev, `git diff --numstat 13eda870 caa1df66` covers the same four files
  as before the merge:
  - `docs/findings/451_TDM8_FIRST_LIGHT.md` +438, blob `cb7dd0aa`, unchanged from
    `0e5ae9c8`;
  - `docs/findings/README.md` +1;
  - `docs/litex/CLOCK_DOMAINS.md` +1/-1;
  - `docs/reference/MILAN_COMPLIANCE_MATRIX.md` +1/-1.

## Stale-statement search

Result: nothing to reword, so no separate commit.

1. **Dev's delta.** I read the added lines of `git diff 7390b436 13eda870`, all 63
   files, looking for TDM, first light, #451, J11, the SoC board, render, DIN,
   DOUT, #448, #386, #617, slip and capture. The new content concerns other things:
   - #602: the PHC-only re-base preserves `mr` and MEDIA_RESET;
   - #607: Ethernet clock-crossing constraints;
   - #590, #592 and #599: firmware service, MDIO publication and word-wide capture
     copies.

   No added line states the TDM render or capture status, the bench link, the slip
   rate or frame coherence.
2. **Whole merged tree.** Eight pattern families (`receipts/stale_search_families.tsv`)
   ran with `git grep -I -i -E` at `0e5ae9c8` and at `caa1df66`. Excluded:
   `docs/history`, the page itself, `tb/verilator/nvm_capture_cpu/measurements.json`
   and the submodules. The hit sets, with line numbers stripped, were compared
   (`receipts/stale_search_new_hits.diff`):
   - Three hits are new at the merge. All are false positives: "stdin" and
     "including" match the DIN family, and a #602 test string about the render
     re-base matches the render family.
   - One hit went away with dev's #397 rewrite.
   - The other hits are unchanged from `0e5ae9c8`, which R392-3 reviewed and found
     not contradicted.
   - The raw hit lists are over 200 KB, so only their identities are recorded:
     `0e5ae9c8`, 238,725 bytes, sha256
     `4741b289888fcad6c43bf939c7d3f8107c89429edadca2366c155c38a4c1cfc4`;
     `caa1df66`, 238,949 bytes, sha256
     `b0707e4405607d85a88d15407246ea3f12d2ca8f352d33761c12a759f0dd2f9c`.
3. **Reverse direction.** The page contains none of the topics dev changed: `mr`,
   MEDIA_RESET, PHC, re-base, link status, MDIO, constraints, timing, the service
   budget, or #602, #607, #590, #592 and #599. Its only hit is "#386 acceptance 4",
   which stays NOT RUN. So dev's changes make no statement on the page stale.

## Gates at `caa1df666de17ba38ae402c52e1ae219dbd01d8b`

- Run from the physical path `$LANES/451-tdm8-first-light`, where `pwd -P`
  equals the path.
- Markdown gates used the pinned environment
  `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python` (Python 3.14.7).
- Commands were unpiped. Output was redirected to a log and the return code read
  directly (`receipts/gate_outputs.txt`).
- After the gates, the tree was clean, including the submodules.

| Gate | rc | Output |
|---|---|---|
| `scripts/docs_check.py` | 0 | 0 finding(s) across 175 md files + 937 scrubbed text files, scrub self-test 23/23, routing arms 4/4 |
| `scripts/check_doc_style.py` | 0 | documentation style: OK (22 current documents) |
| `scripts/check_doc_style.py --selftest` | 0 | selftest: OK |
| `scripts/check_doc_paths.py` | 0 | OK (854 cited paths all resolve, 1 allowlisted) |
| `scripts/gen_toc.py --check` | 0 | OK (117 pages carry a contents list, 17 below the threshold) |
| `scripts/gen_toc.py --selftest` | 0 | PASS (1501/1501 arms) |
| `scripts/gen_toc.py --verify-anchors` | 0 | 240 existing cross-page fragment links reproduced |
| `scripts/check_em_dash.py --base 13eda870` | 0 | 0 finding(s) over 441 added lines in 4 changed Markdown pages, arms 339/339 |
| `scripts/check_em_dash.py --selftest` | 0 | PASS (339 arms) |
| `scripts/check_baremetal_only.py --check` | 0 | OK (0 findings across 935 tracked first-party files) |
| `scripts/check_baremetal_only.py --selftest` | 0 | PASS (700 arms) |
| `git diff --check` | 0 | no output |
| `git diff --check 13eda870 HEAD` | 0 | no output |
| `git diff --check 7390b436 HEAD` | 0 | no output |

## Not done (outside this round)

- No push, PR edit, candidate merge, act run or merge to dev.
- Next steps, per the assignment: one delta review by [R392], then the candidate,
  the act and the merge (`--partial`). #451 stays open.
