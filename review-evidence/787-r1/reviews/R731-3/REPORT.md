[R731] NEGATIVE - exact head f7d5fc3cc48ca80195428562fa86a46023df8e0d

Review R731-3 of PR #822 (issue #787). This is an internal, independent, cleared-context review. It covers the delta from the reviewed head `4aa5666e` to `f7d5fc3c`, tree `91bdf8b7`:

- Round 4: `5640e4d7` merges dev `02ca829a`; `3e67de9c` re-records the port census.
- Round 5: `f7d5fc3c` merges PR #826's head `4ee2aa96`.

The base is `1e80128f`. Live dev is `02ca829a`, re-read from the remote during this review.

## Verdict

The verdict is NEGATIVE on one MINOR finding (F1, Docs). This branch's own PHY-hold crossing made the generated CDC census stale. It was already stale at the prior head `4aa5666e`, and it is still stale at this head. No earlier round raised it. The PR body discloses it and defers it, which does not resolve it.

The merges themselves check out:

- Every round-4 conflict resolution keeps both sides' facts and drops none.
- Every record the rounds regenerated equals its generator's output at the head.
- The #826 merge has #826's own patch-id, and its tree equals `git merge-tree` of the parents.
- `git diff --check` against dev gives rc 0.
- The round-5 route receipts were made at this head and match the tree's record.

Three RESIDUE wording items and three SUGGESTIONs are listed for one-pass absorption.

## Findings

### F1 - MINOR - Docs - `docs/diagrams/cdc_census.svg:113`, `docs/diagrams/cdc_census.drawio:57`, and the raster `docs/diagrams/cdc_census.png` - the generated CDC census omits this branch's PHY-hold MultiReg

- **Authority/evidence:**
  - `docs/diagrams/cdc_census.gen.py` states that nothing in the census is transcribed. It parses every `MultiReg(...)` in `sw/litex/milan_soc.py`.
  - The authoritative crossing table `docs/litex/CLOCK_DOMAINS.md:235` lists this PR's PHY hold, Milan to `sys`, as a Migen `MultiReg`. Its call site is `sw/litex/milan_soc.py:2131`, the file's third.
  - `docs/litex/CLOCK_DOMAINS.md:289`, `docs/guides/SYSTEM_INTEGRATOR.md:63` and `docs/integration/INTEGRATION_GUIDE.md:132` send readers to the census.
  - I regenerated the census in clean scratch clones (`receipts/cdc_census_regen.txt`, `receipts/r731_3_checks.log`):
    - Base `1e80128f`, dev `02ca829a` and PR #826 `4ee2aa96` reproduce their committed svg and drawio byte for byte.
    - The prior head `4aa5666e` and this head `f7d5fc3c` do not.
  - The only difference at the head is the committed `x2 call sites` against the generated `x3 call sites` (`receipts/cdc_census_head_svg.diff`).
  - So this PR introduces the stale record; it is not inherited from dev. The PR body (line 54) calls it "pre-existing" and leaves it unchanged because the round is merge-only.
- **Impact:**
  - Merging lands on dev a generated CDC inventory that disagrees with its own generator and with `CLOCK_DOMAINS.md`. The picture integrators are told to use is missing a crossing this PR adds.
  - The generator has no `--check` arm and no gate reads it (`scripts/ci_scope.py:304-305` only scopes the files), so nothing downstream would catch it.
  - Moving it to another Issue leaves the defect in the tree (AGENTS.md section 7).
- **Required outcome:** at the PR head, `cdc_census.svg` and `cdc_census.drawio` equal the output of `python3 docs/diagrams/cdc_census.gen.py docs/diagrams/cdc_census`. `cdc_census.png` is re-rendered as the generator's docstring states. This is one record-only commit, with no behaviour change, or a manager ruling, recorded publicly, that takes it out of this PR.
- **Verification:**
  - Re-run the generator into a scratch directory at the new head and `cmp` both files against the tracked copies.
  - Check that the PNG shows `x3 call sites`.
  - Confirm the docs gates still give rc 0.

### RES1 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:485` - route provenance after the gPTP line moved

The round-4 resolution changed the #787 record's line 453 to "FPGA-gPTP stays at `135afd04`". That is correct for the pin. But the route quoted at lines 485-507 (51,828 LUTs, 57 slices, +0.107 ns) was measured with FPGA-gPTP `f97c1803`, and the text now reads as if it used `135afd04`.

Exact fix: "The route below was measured at `1be824fc`." becomes "The route below was measured at `1be824fc` with FPGA-gPTP `f97c1803`."

### RES2 - RESIDUE - Docs - `docs/design/AREA_BUDGET.md:145` - "this change" lost its referent

The merged paragraph now carries both #806's and #787's notes, so "this change" is ambiguous.

Exact fix: "; this change meets the build floor at every corner on its best directive." becomes "; #806's route meets the build floor at every corner on its best directive."

### RES3 - RESIDUE - Docs (PR body) - PR #822 body line 54 - "pre-existing"

This branch's round-2 change made the census record stale, not dev.

Exact fix: drop the paragraph once F1 is fixed. If F1 is ruled out of this PR instead, replace "One pre-existing record was found stale" with "One record this branch made stale in round 2 was found".

### S1 - SUGGESTION - Docs - `docs/design/AREA_BUDGET.md:146-149`, `docs/reference/SUBMODULES.md:485-507`

The tree still quotes the route at `1be824fc` as the latest: +0.107 ns, refused, "redone at the re-pin after #814 merges". This head's route set passes, with AltSpreadLogic_high at +0.365 ns. The text is accurate as history, and the round-3 ruling defers the area record to dev after the last release merge. When that re-record lands, update these notes so a refused route is not left as this change's latest figure.

### S2 - SUGGESTION - Tests - `docs/diagrams/cdc_census.gen.py`

`submodule_boundaries.gen.py` and `timesync_chain.gen.py` have a `--check` arm; the census generator does not. That gap is why F1 passed every bank. A separate Issue for a `--check` arm and a gate would stop it recurring. It is out of this PR's scope.

### S3 - SUGGESTION - Tests - author-r5 `receipts/campaigns-f7d5fc3c/table.txt`

The first LiteX aggregate hit the 900 s member limit (rc 92, result unknown). It passed only on an unchanged re-run with the other load lowered. `test_soc_timing_cuts` takes 686 s alone. This is author-disclosed and was noted in PR #826's review. It is worth tracking wherever the member limit is owned.

## Lens results

```text
[R731] PASS Conformance - issue #787 round-4/5 assignments (issuecomment-6541732410, -6543406776); author-r5 review-ready.md; PR #822 body (receipts/pr822.json, receipts/pr822-body.md) - round 4 items 1-5 and round 5 items 1-6 met: merge not rebase; both sides' facts kept; pin-derived records regenerated; diff --check rc 0; floor met at every corner of the best directive; each directive's deciding family named; the body states it carries PR #826 and merges after it, keeps "Relates to #787", has no closing keyword (closingIssuesReferences empty), and equals author-r5 PR-BODY.md byte for byte
[R731] PASS RTL - hunks of git diff 1e80128f..4aa5666e and 1e80128f..02ca829a in hdl/milan/milan_datapath.sv and sw/litex/milan_soc.py; author-r5 route/results/head-set-check.log, head-figures.md, prep.log; protocol-processor git diff --stat f65c8ff7 a9e84b66 over KL_aecp_ucpu/KL_aecp_nvm_writer/KL_aecp_dyn_state (empty) - auto-merged RTL and SoC hunks are disjoint; the resolutions touch no RTL; #826 adds no HDL; every corner of all three directives meets +0.030/0 ns; F3 (ZQCS) no longer decides; the non-selected directives' AECP path runs through modules this pin leaves equal to dev's; the resolution adds no source comment
[R731] PASS Robustness - CHANGELOG.md and SUBMODULES.md #806 and #787 records; milan_datapath.sv eff_link_w and reboot wiring - the merged behaviours compose without a new hazard: the PHY hold drops the effective link, so #806's portEnabled stops gPTP frames during the hold, before IPROG reloads; the delta changes no reset, ordering or timeout path
[R731] PASS Tests - receipts/r731_3_checks.log, gen_check.log, gen_regen.log, port_contracts_*.log, rom_and_pins.log; author-r5 rtlfast-f7d5fc3c (12/12, 508 scenarios), campaigns-f7d5fc3c (LiteX 8/8 on re-run; soc_timing_cuts 23 arms), static-f7d5fc3c (32/32 rc 0), docs-f7d5fc3c (44 steps, 0 failed), route/offline gate820 selftest rc 0 - my re-runs of boundary-diagram --check and regeneration, port --write-budget, ROM-ledger re-record and submodule-docs check give rc 0 and no byte change; the delta weakens no test
[R731] MINOR Docs - docs/diagrams/cdc_census.{svg,drawio,png} - F1: Docs stays UNCLEAN; RES1-RES3 are wording only
```

## Merge checks performed

**Round 4 conflicts.** `git merge-tree --write-tree 4aa5666e 02ca829a` gives rc 1 with exactly the six named files in conflict. Against that automatic result, `6872bc8d`, the recorded merge `5640e4d7` differs in those six files only:

- **`CHANGELOG.md`:** both Contents bullets and both entries are kept, the #787 entry above the #806 entry. Nothing is dropped.
- **`AREA_BUDGET.md`:** the merge keeps dev's update of the shared shipping-route line (`f97c1803`, 16 left, becomes `135afd04`, 27 left) and dev's two new lines, plus this branch's four #787 lines. The ours-side copy of the shared line is base text that dev superseded (checked against `1e80128f:143`), so no fact is dropped.
- **`SUBMODULES.md`:**
  - The pin table takes dev's gPTP row and this branch's processor row. Both equal the gitlinks `135afd04` and `a9e84b66` (`git ls-tree`).
  - Both adoption records are kept in full, #806 first, then #787.
  - The #787 record's "FPGA-gPTP stays at" is updated to `135afd04` (see RES1).
- **`PNG_MANIFEST.json`, `submodule_boundaries.drawio` and `.png`:** these are the generator's output (below).

**Regenerated records at the head:**

- `submodule_boundaries.gen.py`: `--check` gives rc 0, and regeneration gives rc 0 with zero byte change across the svg, drawio, png and manifest.
- `check_port_contracts.py`: rc 0. `--write-budget` reproduces `scripts/port_docs.budget` byte for byte: hdl 2181, gptp-processor 127, protocol-processor 1771. The ratchets (217/19/111) and the unjustified counts (51/4/3) are unchanged.
- `ooc.sh --record-rom-digests` reproduces `syn/yosys/rom_digests.tsv` byte for byte.
- `check_submodule_docs.py` and `timesync_chain.gen.py --check` give rc 0.

**Round 5:**

- `git diff 1e80128f 4ee2aa96` and `git diff 3e67de9c f7d5fc3c` have the same `patch-id --stable`, `8fa226cc`.
- `git merge-tree --write-tree 3e67de9c 4ee2aa96` gives rc 0 with tree `91bdf8b7`, which is the recorded tree.
- The three files both sides change (`milan_soc.py`, `CLOCK_DOMAINS.md`, `TESTING.md`) take disjoint hunks.

**Whitespace.** `git diff --check 02ca829a f7d5fc3c` gives rc 0.

**Route receipts (author-r5):**

- `prep.log` names head `f7d5fc3c` with gitlinks `a9e84b66` and `135afd04`. One synthesis checkpoint, `631baa7b...`, feeds all three directives.
- The gate is PR #820's `50e5d08d`, which `remote-refs.txt` shows as `refs/pull/820/head`.
- `head-set-check.log` gives rc 0 with `RESULT: PASS`:
  - AltSpreadLogic_high is selected at +0.365 ns at both slow corners and +1.633 ns at both fast corners.
  - Hold is +0.053/+0.015 ns.
  - LUT 52,021, FF 54,102, slices 15,787.
- The record figures the gate compares against (52,012 / 53,707 / 15,780 / +0.440 / +0.036) equal `syn/ooc/pp_resource_baseline.json` at the head. The reversed-order check also passes.
- Deciding families:
  - AltSpreadLogic_high: F4, the VexiiRiscv DMA write bridge, 18 levels.
  - ExtraTimingOpt (+0.204 ns) and ExtraPostPlacementOpt (+0.090 ns): the AECP `u_ucpu/uop_e_r` to `u_d3/deb_cnt_r` path on the 50 MHz clock, 36 levels. `u_d3` is `KL_aecp_nvm_writer` (`protocol-processor/hdl/aecp/KL_aecp_engine.sv:2064-2073`). It is unruled and published as such.

**Commits.** All three delta commits carry one-line messages with no trailers.

## Prior public findings (read after the independent pass and the ledger above)

This round raises no new finding against them.

| Prior finding | Severity; lenses | Artifact | Status at `f7d5fc3c` |
|---|---|---|---|
| R731-1 F1 = R732-1 R2 | RESIDUE; Docs | `tb/verilator/reboot_ctrl/mutants.py:113-114`, a comment with a lane label and an issue-comment ID | **Retained.** Blob `2528a927` is unchanged, and line 113 still reads `# the [A10] arms of issuecomment-6518083444: ...`. The fix is as given in R731-1. |
| R732-1 R1 | RESIDUE; Docs | `tb/tools/torture_campaign.py:3135-3139`, a link-down comment that omits the egress wait | **Retained.** Blob `43b1fc40` is unchanged. |
| R731-1 S1 | SUGGESTION; Tests, Robustness | `.mac_tx_beat_i` and `.mac_flush_i` wirings, now at `hdl/milan/milan_datapath.sv:9765, 9768` | **Retained**, optional. The file changed only by dev's 5-line #806 insertion at line 8899, which shifts these lines. |
| R731-1 S2 | SUGGESTION; Tests | `hdl/milan/KL_reboot_ctrl.sv:290, 296`, the quiet-window edges | **Retained**, optional. Blob `d2c74f47` is unchanged. |
| R732-1 S1 | SUGGESTION; RTL, Robustness | `hdl/milan/KL_reboot_ctrl.sv:257-262` | **Retained**, optional. Blob unchanged. |
| R732-1 S2 | SUGGESTION; Tests | `tb/verilator/reboot_ctrl/mutants.py`, the saturation control | **Retained**, optional. Blob unchanged. |

No prior round raised the CDC census (F1). R731-1 lists `CLOCK_DOMAINS.md` among its Docs artifacts but not the generated census, so F1 is new. It does not re-litigate a cleared finding.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | round-4/5 assignments; PR body and metadata; author-r5 review-ready, route results | R731-3 (delta); R731-1/-2 (rest, untouched) | f7d5fc3cc48ca80195428562fa86a46023df8e0d |
| RTL | CLEAN | auto-merged RTL and SoC hunks; route set, deciding paths, record; processor module diff | R731-3 (delta); R731-1/-2 (rest) | f7d5fc3cc48ca80195428562fa86a46023df8e0d |
| Robustness | CLEAN | merged #806 and #787 behaviour; link and reboot wiring | R731-3 (delta); R731-1/-2 (rest) | f7d5fc3cc48ca80195428562fa86a46023df8e0d |
| Tests | CLEAN | own generator and record re-runs; author-r5 rtl-fast, campaigns, static, docs, gate self-test | R731-3 (delta); R731-1/-2 (rest) | f7d5fc3cc48ca80195428562fa86a46023df8e0d |
| Docs | UNCLEAN (F1 MINOR open; RESIDUE RES1-RES3, R731-1 F1 and R732-1 R1 carried) | the six conflict resolutions; regenerated records; CDC census regenerated at five commits | R731-3 | f7d5fc3cc48ca80195428562fa86a46023df8e0d |

## Real limits

- I re-ran no Vivado route, rtl-fast, LiteX simulation, builder bank or docs workflow. Those results are the author's published receipts, spot-checked for head identity and internal consistency.
- Physical calibration was NOT RUN. Field skips are not hardware proof. The bench REBOOT run that closes #787 is outside this round.
- No manager source bank runs at this head, and none is claimed or inferred.
- I did not re-review #826's own change, which R755-2 and R756-2 reviewed at `4ee2aa96`.
- I inspected no hosted CI context.
- `git fetch` of dev wrote only `FETCH_HEAD` in the review clone.
- The writing probes (port budget, ROM ledger) were restored with `git checkout`, and `git status --porcelain` is empty afterwards.

## Pending manager duties

- Rule on F1: a record-only fix in this PR, or a public ruling.
- Carry RES1-RES3, R731-1 F1 and R732-1 R1 to the residue checklist.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, after PRs #826 and #820, and link its receipts.
- Hosted and act acceptance.
- At the post-release record re-record, apply S1.

R731-3 FINISHED
