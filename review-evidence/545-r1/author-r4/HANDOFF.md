# [A311] Merge-dev handoff

Status: assignment complete; local merge ready for the assigned delta review.

Branch: `545-crf-servo-slew`
Initial head: `92ad1687d84ff077f872719b4f1df601f82064d2`
Verified dev head: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`
Verified remote: `https://github.com/kebag-logic/milan-fpga.git`

Merge head: `b376f6113b388929fe82e883d400e5361319b966`

## Merge and conflicts

Six conflict paths, six textual hunks and one binary conflict. Both sides were inspected before resolution. No product code was manually changed.

| Conflict | Final artifact | Resolution |
| --- | --- | --- |
| CHANGELOG Contents | `CHANGELOG.md:11` and `:12` | Retained both new rows; Contents generator confirms the result. |
| CHANGELOG unreleased sections | `CHANGELOG.md:32` and `:46` | Preserved the complete lane slew section and complete dev processor section. |
| Pin table | `docs/reference/SUBMODULES.md:24` and `:25` | Kept gPTP `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` from the lane and processor `990f96526bb89356c963a260ebbdcf2a77e6623a` from dev. The automatically merged adoption table and slew contract prose remain. |
| Campaign table | `docs/testing/TESTING.md:267` through `:269` | Kept dev's GSI row and the lane's expanded gmstep row and servo slew row. The lane gmstep row supersedes the older dev inventory and preserves all its triggers. |
| Generated master, whole line | `docs/diagrams/submodule_boundaries.drawio:1` | Regenerated from merged index pins; no marker union or manual generated-content edit. |
| Generated PNG, binary | `docs/diagrams/submodule_boundaries.png` | Re-rendered from regenerated sources and visually inspected. |
| Generated manifest digest hunk | `docs/diagrams/PNG_MANIFEST.json:10` | Restored an intact parent manifest as input, then regenerated the source and raster digests with the repository generator. Other artifact entries are unchanged. |

The generated SVG at `docs/diagrams/submodule_boundaries.svg:29` and `:39` also carries both pins. Raw textual conflicts are preserved in `*.conflicts.diff`.

`git submodule update --init` completed at the merged pins. No missing pinned commit needed a separate fetch. All populated submodules were clean. Merge parents are the requested lane head and exact dev head, in that order.

## Regenerated files

- `python3 docs/diagrams/submodule_boundaries.gen.py`: regenerates Draw.io, SVG, PNG and the manifest entry from both merged gitlinks.
- `cd syn/yosys && ./ooc.sh --record-rom-digests`: rc 0; existing merged ledger rows reproduce exactly, so no additional ledger change.
- `python3 scripts/gen_toc.py --write CHANGELOG.md`: rc 0; combined Contents already matches.
- Committed PNG, direct Draw.io PNG, and A4 landscape render inspected visually. Labels, pins, connectors and contrast are legible; no clipping. Inspection artifacts remain under `/tmp/545-a311-diagrams`.

The pinned Markdown packages are installed in `/tmp/545-a311-python`; no environment or toolchain resides in this output packet.


## Area

Repository `syn/yosys/ooc.sh` recipe: servo baseline at dev is 864 LUT / 790 FF; merged servo is 871 LUT / 792 FF. Delta: +7 LUT / +2 FF. Both retain 1 DSP / 150 CARRY4 and no memory.

The unchanged four-stage release-alignment block measures 1 LUT / 4 FF in isolation. Combined isolated parent additions: +8 LUT / +6 FF. This is not a whole-datapath measurement or a placement result. No merge-round change to these measured blocks occurred, so their merge-round delta is zero.

Baseline source and the extracted alignment block live under `/tmp/545-a311-area`. The recipe differs only in relocated support/root paths and the single measured-top source entry; `area-recipe-deltas.diff` records those substitutions. `area-source-evidence.txt` binds the source bytes. The processor submodules were not edited.

## Gate execution method

Every gate runs in the foreground, without a pipe, with a generous deadline. Per-command `.receipt.json` files record the exact argv, working directory, exit status and elapsed time. Corresponding `.log` files retain stdout and stderr.

- The clean servo default uses `/usr/bin/time -p ... taskset -c 8,9 make -C tb/verilator/mmcm_servo`, after `make ... clean`.
- Other runtime gates use CPUs 10-15; the explicit servo campaign uses 12-13. This is a shared-host timing sample.
- The no-Git docs arm sets `GIT_DIR=/tmp/545-a311-no-git`, an absent metadata path, exercising the same filesystem-walk branch as CI. The log explicitly reports that branch and its inventory-parity skip. No checkout metadata was removed and no tree export was created.
- The default datapath `run` expansion is recorded in `milan-dp-run.dry-run.txt` and `milan-dp-run.commands.json`. All non-echo commands run in foreground chunks, with an exit recorded for each. This checkout requires 34 commands, including prerequisite regeneration.
- No hosted validation result or independent review is claimed for the local merge head.

## Validation limits

The builder returned 0. Its real placement-report calibration arm (gate 11) is NOT RUN because the required board report is absent. No compiler-related arm was skipped. The log ends `ALL GATES PASS EXCEPT 1 NOT RUN`; this is the same reported limitation as the pre-merge round.

The no-Git documentation arm skips only Git inventory parity by design. Frontend analysis executed and matched its four existing processor findings; lint matched its unchanged 90-finding ratchet. No ratchet was changed.

No hardware, independent delta review or hosted-CI result is claimed for this local merge head.

## Clean default timing

The default `mmcm_servo` target returned 0 from a clean build under `taskset -c 8,9`. `/usr/bin/time` reports **944.14 s** wall clock; the receipt wrapper reports 944.168 s. All 100 unit, 8 rail, 113 step and 90 slew checks pass. The unchanged 1800 s budget retains **855.86 s (47.5%)** of local margin. Other gates used CPUs 10-15. This shared-host measurement is not hosted evidence.

## Gate table

| Gate | Exit | Seconds | Evidence |
| --- | --- | --- | --- |
| `mmcm-clean` | 0 | 0.008 | `mmcm-clean.log` |
| `mmcm-default` | 0 | 944.168 | `mmcm-default.log` |
| `crf-rx` | 0 | 795.965 | `crf-rx.log` |
| `docs-git` | 0 | 4.438 | `docs-git.log` |
| `builder` | 0 | 857.531 | `builder.log` |
| `docs-no-git` | 0 | 4.174 | `docs-no-git.log` |
| `em-dash` | 0 | 3.525 | `em-dash.log` |
| `doc-style` | 0 | 0.065 | `doc-style.log` |
| `toc-check` | 0 | 2.469 | `toc-check.log` |
| `toc-anchors` | 0 | 1.569 | `toc-anchors.log` |
| `doc-paths` | 0 | 0.064 | `doc-paths.log` |
| `module-matrix` | 0 | 0.966 | `module-matrix.log` |
| `xvlog` | 0 | 147.553 | `xvlog.log` |
| `ooc-servo` | 0 | 4.425 | `ooc-servo.log` |
| `gptp-shadow` | 0 | 277.041 | `gptp-shadow.log` |
| `dp-sweep-00` | 0 | 0.165 | `dp-sweep-00.log` |
| `dp-sweep-01` | 0 | 0.215 | `dp-sweep-01.log` |
| `dp-sweep-02` | 0 | 32.638 | `dp-sweep-02.log` |
| `ooc-base-servo` | 0 | 8.933 | `ooc-base-servo.log` |
| `ooc-alignment` | 0 | 4.473 | `ooc-alignment.log` |
| `rtl-source-lists` | 0 | 1.367 | `rtl-source-lists.log` |
| `sv-idiom` | 0 | 0.414 | `sv-idiom.log` |
| `rtl-lint` | 0 | 12.769 | `rtl-lint.log` |
| `dp-sweep-03` | 0 | 92.634 | `dp-sweep-03.log` |
| `cpp-idiom` | 0 | 1.572 | `cpp-idiom.log` |
| `py-idiom` | 0 | 3.219 | `py-idiom.log` |
| `port-contracts` | 0 | 2.318 | `port-contracts.log` |
| `naming` | 0 | 0.464 | `naming.log` |
| `test-evidence` | 0 | 5.222 | `test-evidence.log` |
| `diagram-check` | 0 | 0.364 | `diagram-check.log` |
| `diagram-pngs` | 0 | 0.364 | `diagram-pngs.log` |
| `submodule-docs` | 0 | 0.465 | `submodule-docs.log` |
| `diff-check` | 0 | 0.032 | `diff-check.log` |
| `behave` | 0 | 1.165 | `behave.log` |
| `dp-sweep-04` | 0 | 23.276 | `dp-sweep-04.log` |
| `mmcm-slew-mutants` | 0 | 1284.123 | `mmcm-slew-mutants.log` |
| `dp-sweep-05` | 0 | 91.896 | `dp-sweep-05.log` |
| `dp-sweep-06` | 0 | 0.214 | `dp-sweep-06.log` |
| `dp-sweep-07` | 0 | 0.064 | `dp-sweep-07.log` |
| `dp-sweep-08` | 0 | 23.391 | `dp-sweep-08.log` |
| `dp-sweep-09` | 0 | 30.726 | `dp-sweep-09.log` |
| `dp-sweep-10` | 0 | 20.614 | `dp-sweep-10.log` |
| `gmstep-mutants` | 0 | 823.068 | `gmstep-mutants.log` |
| `dp-sweep-11` | 0 | 21.435 | `dp-sweep-11.log` |
| `dp-sweep-12` | 0 | 25.141 | `dp-sweep-12.log` |
| `dp-sweep-13` | 0 | 29.463 | `dp-sweep-13.log` |
| `dp-sweep-14` | 0 | 32.136 | `dp-sweep-14.log` |
| `dp-sweep-15` | 0 | 21.736 | `dp-sweep-15.log` |
| `dp-sweep-16` | 0 | 19.885 | `dp-sweep-16.log` |
| `dp-sweep-17` | 0 | 28.367 | `dp-sweep-17.log` |
| `dp-sweep-18` | 0 | 22.021 | `dp-sweep-18.log` |
| `dp-sweep-19` | 0 | 23.054 | `dp-sweep-19.log` |
| `dp-sweep-20` | 0 | 32.297 | `dp-sweep-20.log` |
| `dp-sweep-21` | 0 | 6.296 | `dp-sweep-21.log` |
| `dp-sweep-22` | 0 | 17.919 | `dp-sweep-22.log` |
| `dp-sweep-23` | 0 | 26.314 | `dp-sweep-23.log` |
| `dp-sweep-24` | 0 | 6.636 | `dp-sweep-24.log` |
| `dp-sweep-25` | 0 | 10.382 | `dp-sweep-25.log` |
| `dp-sweep-26` | 0 | 12.758 | `dp-sweep-26.log` |
| `dp-sweep-27` | 0 | 6.527 | `dp-sweep-27.log` |
| `dp-sweep-28` | 0 | 5.725 | `dp-sweep-28.log` |
| `dp-sweep-29` | 0 | 0.665 | `dp-sweep-29.log` |
| `dp-sweep-30` | 0 | 6.226 | `dp-sweep-30.log` |
| `dp-sweep-31` | 0 | 487.182 | `dp-sweep-31.log` |
| `dp-sweep-32` | 0 | 371.793 | `dp-sweep-32.log` |
| `dp-sweep-33` | 0 | 177.974 | `dp-sweep-33.log` |
| `final-state` | 0 | 0.214 | `final-state.log` |

## Completion

All 67 recorded gate/setup/final-state commands returned 0. The 34-command default datapath expansion completed in these foreground chunks:

| Commands | Exits | Sum of command seconds |
| --- | --- | --- |
| 0-9 | All 0 | 295.219 |
| 10-20 | All 0 | 276.149 |
| 21-26 | All 0 | 80.305 |
| 27-33 | All 0 | 1056.092 |

The connected gmstep leg passes 58/58; the clock-ratio leg passes 144/144; default render controls pass 6/6; default gmstep controls pass 4/4. Explicit servo controls pass 10/10 and explicit gmstep controls pass 16/16. The CRF suite passes 13,836 unit, 1,658 discontinuity and 69 connected checks, plus 8/8 controls. The gPTP shadow suite passes 309 checks, nine controls and its lifecycle gate. No new validation failure was found.

`final-state.log` confirms the exact head, ordered parents, one-line commit message, correct remote and branch, and clean root plus all four populated submodules. Both `git diff --check` and the dev-to-head diff check returned 0. No branch push, PR edit, dev merge, other checkout, submodule edit, delegation or hardware action occurred.

The current public PR body was fetched again and is unchanged from the initial fetch. `PR-BODY.md` preserves it in full, changes the first line to `[A311]`, and appends the final merge-dev section; `Closes #545` remains. It has no absolute home paths, model names or attribution footer.

The local merge head still needs the assigned independent delta review and later hosted validation after publication. The author provides evidence, not a review verdict.

Public handoff: `[A311] REVIEW READY` was posted on issue #545 as the final external action: https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5832387213

The exact published text is preserved in `REVIEW-READY.md`. Assignment complete; stopping.
