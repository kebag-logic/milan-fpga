[R736] POSITIVE - exact head 0c45ebf28e2c11352aa4ad40d46780143b1a77ab

External independent review, round R736-2 (delta over the round-1 head `f99405af0b2caad46e84f50f8251ffbffaa80836`), issue #806 / PR #813. Tree `9aa2966798bf164913cef087f6bdf09bd2e69bcf`; source base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. All five lenses are CLEAN at this head. No BLOCKER, MAJOR or MINOR is open. One RESIDUE from a parallel round is retained (R735-2-R1, wording only). There are two new SUGGESTIONs, and five carried ones. The prior RESIDUE R736-1-R1 is RESOLVED. This source verdict does not discharge the merge-turn, hosted or physical gates.

## Isolation

Before writing my verdict, I read AGENTS.md, CONTRIBUTING.md and the docs map. I read the PR only through `gh pr view --json title,body,headRefOid,baseRefName,baseRefOid,files,commits` (`receipts/pr-view.json`), and the source only through git. The other inputs were the bodies of #814 and #818 (`receipts/issue-814.json`, `receipts/issue-818.json`), the published author packet at `8311a3a16c07d707c21e33ad429e9a654b546ee3:review-evidence/806-r1/author-r2/`, my own round-1 report R736-1, and an exact-head check-run snapshot. I listed no comments and opened no other review report until my verdict and ledger were on disk: `INDEPENDENT-VERDICT.md`, hash and time in `receipts/independent-verdict-checkpoint.sha256`. After that I read the PR comment list and the two R735 reports (R735-1, and R735-2 at this head). I also read the manager's round-2 assignment and the record addendum (#806 issuecomment-6522650491, #814 issuecomment-6525285974). None of that reading changed the verdict. It added one retained RESIDUE, R735-2-R1, which I confirmed independently.

## What the delta can reach

- `git diff --raw f99405af..0c45ebf2` changes three documents, all mode 100644: `CHANGELOG.md`, `docs/design/AREA_BUDGET.md` and `docs/reference/SUBMODULES.md` (7 insertions, 3 deletions). Every gitlink is identical; `gptp-processor` stays at `135afd043309369a87ddbc8d6550aff8ec52a157`. No RTL, test, script, record or generated file changed.
- `git diff --stat cf3ef596..0c45ebf2` is also documentation only (those three plus `docs/guides/gptp/SYSTEM_INTEGRATOR.md`). So the round-1 synthesis checkpoint (built at `cf3ef596`) that the directive runs reuse comes from executable inputs equal to this head. The lens verdicts R736-1 gave the executable content at `f99405af` therefore carry over: nothing they depend on changed.
- The delta contains no source comment, so the comment rule has nothing new to check. The added prose has no lane labels, reviewer IDs, issue-comment IDs or em dashes (grep over the added lines).

## The delta against the rulings

- The manager's round-2 item 4 prescribes this sentence: "Timing recovery is ruled under #814/#818; this change meets the build floor at every corner on its best directive." `AREA_BUDGET.md:145` and PR body line 31 carry it verbatim. `CHANGELOG.md:76-77` and `SUBMODULES.md:429-431` split it into two sentences under the concise-style limit, with the meaning unchanged.
- #818's rule is the best of the three directives, judged at every corner against the build floor: WNS >= +0.030 ns and WHS >= 0 (`docs/integration/BUILDING.md:712`, `docs/testing/RUNNING_TESTS.md:209`). Its acceptance picks the best directive by worst-corner WNS. The pages' claim is true on the receipts below, and the shipping directive meets the floor too (+0.032 / +0.034 ns).
- `AREA_BUDGET.md:144` and the pin page still say the committed gate refuses the route. That stays correct at this head: the gate's rule is unchanged until #818 merges.
- Under the record addendum, a record that does not yet carry this PR's route is not a finding. The PR body states that nothing is re-recorded.

## Round evidence: the two extra placement directives

`directive_probe.py <source-tree> <evidence-root>` writes `receipts/directive-probe.txt` (rc 0). It checks the following:

- **Packet integrity.** All 425 `MANIFEST.json` entries match their published SHA-256, and every file in the evidence tree is listed. No file is unlisted or missing.
- **Same inputs, only the directive changed.** The two `baseline_implementation.tcl` scripts differ in exactly one line, `place_design -directive AltSpreadLogic_high` against `ExtraTimingOpt`. Each opens `<round1-scratch>/viv-cf3ef596/w1/ax7101/gateware/alinx_ax7101_synth.dcp`. That checkpoint's SHA-256, `7253a8c0…81e5fb`, is the same before and after the runs (`synth-dcp.sha256.before/after`). The rest of the script matches the record's flow identity in `syn/ooc/pp_resource_baseline.json`: opt ExploreArea, timing-grade configure, post-place phys_opt AggressiveExplore, route AggressiveExplore and post-route phys_opt AggressiveExplore. It also follows the recipe step at `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:142-185`: the shipping Tcl tail, with its single `ExtraPostPlacementOpt` line replaced. The sourced `sw/litex/*.tcl` files come from the round-1 clone at `cf3ef596` and are unchanged at this head. Both runs ended rc 0 (`vivado.rc`, `timeline.txt`), and both used the default seed (no seed directive in the scripts).
- **Resources.** The committed gate's own `utilization()` parser, run on each `alinx_ax7101_utilization_place.rpt`, reproduces the author's LUT, FF, slice, BRAM tile, RAMB36, RAMB18 and DSP counts exactly. AltSpreadLogic_high has 51,874 LUT, 53,787 FF and 15,837 slices; ExtraTimingOpt has 51,849 LUT, 53,787 FF and 15,837 slices. Both have RAMB36 74, RAMB18 27 and DSP 13.
- **Corners.** Per corner, WNS / WHS in ns:

  | Directive | Slow 0C | Slow 85C | Fast 0C | Fast 85C |
  |---|---|---|---|---|
  | AltSpreadLogic_high | +0.235 / +0.037 | +0.235 / +0.037 | +1.633 / +0.011 | +1.633 / +0.011 |
  | ExtraTimingOpt | +0.218 / +0.037 | +0.218 / +0.037 | +1.633 / +0.011 | +1.633 / +0.011 |

  Every corner meets the floor. The stated worst-corner figures equal the per-corner minima: WNS +0.235 and +0.218, both from the Slow corners, and WHS +0.011 for both, from the Fast corners. The brief's "+0.235/+0.037" and "+0.218/+0.037" are the Slow-corner pairs. The worst hold is the Fast corners' +0.011 ns, and the PR body states it correctly (lines 108-109 and 178). For each directive, all four negative-slack reports read "No timing paths found.", and the route status shows 0 nets with routing errors (102,971 and 102,962 routable nets). The Slow_0C worst-setup reports confirm +0.235 ns (`FDPE_17/C` -> `KL_mac_rmon_events/fcs_cnt_r_reg[17]/R`, 0 levels, 8.757 ns of routing) and +0.218 ns (the bridge-to-flash path, 18 levels). Neither path is in logic this PR changes.
- **The gate's tolerances.** I ran the gate's own `verdict_for()` against the route-1x1 record. Both directives come out "ok" on every figure: for AltSpreadLogic_high, WNS 0.44 -> 0.235 (a fall of 0.205, within 0.25) and WHS 0.036 -> 0.011, with slices +57 (tolerance 80). This matches PR body line 111. The committed gate cannot run on these directories ("NOT COMPARABLE … 0 recipe scripts", `gate/route-1x1-check-*.log`). It counts the placement directive in the flow identity (`syn/ooc/pp_resource_gate_selftest.py:255`), so the parser-level comparison is the right substitute until #818 lands.

## Gates run here at this head

These are focused documentation gates. They were run read-only in the review clone, with outputs in `receipts/docs/` and `receipts/docs/rc.txt`.

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | rc 0: 0 findings across 210 md files plus 1,423 scrubbed text files |
| `scripts/check_doc_style.py` | rc 0: 23 current documents OK |
| `scripts/check_submodule_docs.py` | rc 0: 6 exact gitlinks |
| `scripts/check_doc_paths.py` | rc 0: 1,071 cited paths resolve |
| `scripts/check_gptp_docs.py` | rc 0: 8 current pages |
| `scripts/gen_toc.py --verify-anchors` / `--check`, `scripts/check_em_dash.py` | **not runnable here** (rc 2): the pinned Markdown renderer is not installed, and shared installs are not allowed. The author's exact-head receipts report them rc 0 (`author-r2/receipts/static-0c45ebf2/toc_*.log`; docs workflow `docs-0c45ebf2/all.out`: 44 steps, 0 failed, 2 skipped by rule, head `0c45ebf2`). My grep finds no em dash in the added lines. |

No simulation was needed, because the delta reaches no executable input. I did not use the scoped simulator.

## Findings

**R735-2-R1 | RESIDUE | Docs | `docs/design/AREA_BUDGET.md:146` | RETAINED (raised by the parallel round; I confirmed it independently)**
- Evidence: ":146 The next growth on the shipping image therefore has no slice room" draws its reason from :143, the 27 of 15,850 slices left. Round 1 put :144 between them and this delta added :145, so "therefore" now reads as following from the timing sentences.
- Impact: wording only. No figure, verdict, gate or claim changes.
- Exact fix: open :146 with "With 27 slices left, the next growth on the shipping image has no slice room and needs its own owner decision", keeping the link.
- Verification: `check_doc_style.py` rc 0, and the sentence names its own reason.

**R736-2-S1 | SUGGESTION | Docs | `CHANGELOG.md:77`, `docs/reference/SUBMODULES.md:431`, `docs/design/AREA_BUDGET.md:145` | "the best directive" is not named on the pages (same as R735-2 S6)**
- Evidence: the pages do not say which directive is best, or give its worst-corner figures (AltSpreadLogic_high, +0.235 ns WNS and +0.011 ns WHS, 15,837 slices with 13 free). Only the PR body does. The slice sentence's 27 free applies to the shipping directive.
- Optional outcome: name AltSpreadLogic_high with its worst-corner WNS / WHS on the area page, and/or say "on the shipping directive" in the slice sentence.
- Verification: the page's figures match `directive-figures.txt`.

**R736-2-S2 | SUGGESTION | Docs | `docs/design/AREA_BUDGET.md:148-149` (dev text from `ca39dc1b`) | the critical-path sentence can be read as describing the adopted route**
- Evidence: :148-149 give the record route's path: `…axilite2wishbone_state_reg[1]` -> `milansoc_spiflash_phy_cnt_reg[8]`, 9.531 ns, of which 6.252 ns is routing. Those lines now follow the adopted route's sentences (:143-145). The adopted shipping route's worst path is `…state_reg[3]` -> `…cnt_reg[8]`, 9.835 ns, of which 6.251 ns is routing (`author/receipts/vivado/route-1x1-worst-setup-path.txt:1-10`). It is the same path family, with different figures.
- Optional outcome: open :148 with "The record's routed critical setup path".
- Verification: the sentence names the route its figures come from.

**Carried, unchanged.** None of their artifacts is in the delta. These are R735-1's optional SUGGESTIONs: S1 (Tests: the toggle check's one-interval bound), S2 (Tests, Robustness: no silence check while the port is disabled), S3 (Tests: no parent test of shadow-level withdrawal), S4 (Robustness: the guard-disabled `eff_link` arm is not graded) and S5 (Docs: no 10.2.4.11 traceability row). I agree with R735-2 S7 (Tests, Docs: the per-corner timing summaries are not published raw) and list it under limits below.

**Prior finding R736-1-R1 (RESIDUE, Docs): RESOLVED.** The "owner decision" sentences at `CHANGELOG.md:76`, `AREA_BUDGET.md:144` and `SUBMODULES.md:429` are replaced by the #814/#818 ruling sentence. The PR body no longer contains "owner decision", "open decision" or the accept/re-record-versus-recover choice. Its DoD lines at 191 and 193 point to #818. The ruling postdates my round-1 proposed text, and the manager prescribed the new sentence instead. Figures, the refusal statement and the open acceptance boxes are retained.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Delta sentences against the #814 and #818 bodies and #806 issuecomment-6522650491; build floor `docs/integration/BUILDING.md:712`, `docs/testing/RUNNING_TESTS.md:209`; `receipts/directive-probe.txt` per-corner floor checks. Executable conformance carried from R736-1, since the tree is equal outside three pages (`git diff --raw f99405af..0c45ebf2`) | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| RTL | CLEAN | `git diff --raw f99405af..0c45ebf2` and `cf3ef596..0c45ebf2` (no HDL); both directive `baseline_implementation.tcl` against `PP_SHADOW_BASELINE_RECIPE.md:142-185` and the record flow in `syn/ooc/pp_resource_baseline.json`; worst-setup paths `author-r2/receipts/directives/*/worst-setup-path-Slow_0C.txt:1-10` (outside the changed logic) | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Robustness | CLEAN | The worst corner of every directive, including Fast hold +0.011 ns >= 0; the 8 `*_negative.rpt` and 2 `*_route_status.rpt`; unchanged synthesis checkpoint hash; gate `verdict_for` tolerances. No executable change | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Tests | CLEAN | `directive_probe.py` / `receipts/directive-probe.txt` (the gate's own parsers and verdict_for); the gate's NOT COMPARABLE refusal at `syn/ooc/pp_resource_gate.py:284` and selftest `:255`; own docs gates `receipts/docs/*`; author `docs-0c45ebf2/all.out`, `static-0c45ebf2/*`. No test changed | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |
| Docs | CLEAN (RESIDUE R735-2-R1 carried to the checklist) | `CHANGELOG.md:64-79`, `docs/design/AREA_BUDGET.md:136-151`, `docs/reference/SUBMODULES.md:405-436`; PR body lines 28-31, 67-68, 95-111, 162, 177-193 | R736-2 | 0c45ebf28e2c11352aa4ad40d46780143b1a77ab |

## Real limits

- The per-corner WNS / WHS values, including the +0.011 ns Fast hold and +1.633 ns Fast setup, are the author's extraction. The full `*_signoff_*_timing.rpt` reports are listed only by hash (`large.sha256`), so I could not run the gate's `timing()` parser on them. The published negative-slack reports bound every corner at >= 0 slack, and the Slow_0C worst-path reports confirm the Slow WNS. The +0.03 ns setup margin at the Fast corners and the exact hold figures rest on the author's table.
- I could not run the TOC and em-dash gates here (missing pinned renderer). For those I rely on the author's exact-head receipts.
- The hosted snapshot at 2026-10-30T19:11:26Z (`receipts/hosted-check-runs.tsv`) shows 29 success, 23 cancelled, 7 queued (the `rtl-full` run) and 1 skipped (`Physical gPTP (nightly and manual)`). Two jobs report failure: `Union pp_shadow` (job 124258070861) and `Collect CI manifest` (job 124253696792). In both, every step after job setup has no conclusion, which fits a union/collector job closing on cancelled or still-queued owners rather than a test that ran. I did not establish the cause. This is a snapshot, not a green aggregate and not execution proof.
- No manager source bank exists at this head, and none is claimed or inferred. I ran no full bank, no simulation and no Vivado run. Physical calibration is NOT RUN, field skips are not hardware proof, and built-image link-toggle qualification is still outstanding.

## Pending manager duties

- Build and validate the current-dev merge candidate with the builder and native banks at the merge turn, and link their receipts on the PR.
- Own hosted and act acceptance at the exact head. That includes the queued `rtl-full` contexts and the two failed union/collector jobs above.
- Apply #818 when it lands. Under the record addendum, re-record once on dev from the release image's three-directive routes. Until then, the committed gate's route-1x1 refusal stands as stated on the pages.
- Carry R735-2-R1 to the residue checklist. Keep #806 open with `Relates to #806` until the built-image link-toggle scenario passes. Apply the normal merge and containment rules; an agent merge needs explicit maintainer authorization.

## Receipts

Portable scripts:
- `directive_probe.py <source-tree> <evidence-root>`
- `verify_tree.py <checkout> <commit> [path=sha …]`

Raw receipts are under `receipts/`; `MANIFEST.sha256` lists every publishable file. After the probes, `receipts/source-integrity.txt` (rc 0) checked the review clone at `0c45ebf2`:
- the bytes and mode of all 1,447 tracked blobs;
- stage-0 index entries with no hidden flags;
- 6 gitlinks, including `gptp-processor=135afd04…` and `protocol-processor=f65c8ff7…`;
- an empty `git status --porcelain --ignored`. One probe-created `syn/ooc/__pycache__` was removed before this check, and the probe now disables bytecode writing.

R736-2 FINISHED
