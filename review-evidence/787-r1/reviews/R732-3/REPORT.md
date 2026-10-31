[R732] NEGATIVE - exact head f7d5fc3cc48ca80195428562fa86a46023df8e0d

# R732-3: external cleared-context delta review of PR #822 (#787)

Head `f7d5fc3cc48ca80195428562fa86a46023df8e0d`, tree `91bdf8b797065cd63a38650c6f74ff5c19d29690`. The previously reviewed head is `4aa5666e`. Source base is `1e80128f`, and live dev is `02ca829a` (re-read from the API during this round). PR #826 is open at `4ee2aa96` and has not merged.

## Verdict

NEGATIVE. Two MINOR findings are open, both under Docs:

- **F1.** A generated record, the CDC census, disagrees with its generator at this head because of this PR's own change.
- **F2.** The #787 adoption record and area note still say the re-pin's route waits for #814. This head carries #814, and its route set passes.

No BLOCKER or MAJOR is open. The Conformance, RTL, Robustness and Tests lenses are covered clean.

Both merges are mechanically sound:

- **Round 4.** It keeps both sides' facts in every conflicted file.
- **Round 5.** It is exactly the automatic merge: same tree, same patch-id as #826.

Two RESIDUE items and one SUGGESTION are recorded for the residue checklist. Neither prior RESIDUE is fixed at this head, and both are retained.

F1 is not new to rounds 4 and 5. It has been in the tree since round 2, and my own earlier rounds (R732-1 at `667b9bbc`, R732-2 at `4aa5666e`) did not find it. The author published it in round 4's STOP and again in round 5's packet. They called it pre-existing and left it unfixed in a merge-only round. A known stale generated record in the PR's own scope is still open, so it holds the Docs lens unclean here.

## How the task was reconstructed

I read these in order:

1. AGENTS.md, then sections of CONTRIBUTING.md and docs/README.
2. Issue #787's manager assignments for round 4 (issuecomment-6541732410) and round 5 (the ruling, issuecomment-6543406776).
3. Round 4's STOP (issuecomment-6543378747), round 5's REVIEW READY (issuecomment-6544827306) and the manager's acceptance (issuecomment-6544849367).
4. The PR body at the head.
5. `git diff 1e80128f..f7d5fc3c`, narrowed to the delta `4aa5666e..f7d5fc3c` and to each merge's parents.
6. The author-r5 packet in archive `a16caad4`.

I read the prior review findings on this PR only after writing my draft verdict and ledger (`receipts/DRAFT-verdict-before-prior-findings.txt`, sha256 `2384e10e…`). I read no lane scratchpad and no concurrent review.

## What was checked, with receipts

| Check | Result | Receipt |
|---|---|---|
| Round 4: `git merge-tree --write-tree 4aa5666e 02ca829a` | Exactly six files conflict: `CHANGELOG.md`, `AREA_BUDGET.md`, `SUBMODULES.md`, `PNG_MANIFEST.json`, `submodule_boundaries.drawio`, `submodule_boundaries.png` | `receipts/r4_merge_tree.txt` |
| Round 4: automatic tree `6872bc8d` against the committed `5640e4d7` | Only those six files differ. Every non-conflicted path, including the auto-merged `milan_datapath.sv`, `milan_soc.py`, `submodule_boundaries.svg` and `rom_digests.tsv`, is byte-equal to the automatic merge | `receipts/r4_resolution_stat.txt`, `r4_resolution_small.diff`, `r4_resolution_submodules.diff` |
| Round 4: both sides kept, line by line against base `1e80128f` | `CHANGELOG.md` and `AREA_BUDGET.md`: every line each side added is present. `SUBMODULES.md`: one branch line is changed on purpose: "FPGA-gPTP stays at `f97c1803`" now names `135afd04`, the current gPTP pin, as the STOP records. Lines dev removed (the old gPTP pin row, the `f97c1803` slice sentence) are gone, and lines the branch replaced (the processor pin row) carry the branch's value | `receipts/r4_both_sides.txt`, `scripts/both_sides.py` |
| ROM ledger | Union of both sides with nothing dropped: dev added one row (`135afd04` gptp_ucode), the branch added six (`013ee63f`, `1be824fc`, `a9e84b66`). Re-recorded here with `ooc.sh --record-rom-digests`: rc 0, `git diff --exit-code` rc 0 | `receipts/rom_digests_union.txt`, `receipts/head_rom_digests_record.txt` |
| Boundary diagram and PNG manifest | `submodule_boundaries.gen.py --check`: `OK (6 exact gitlinks, decoded PNG)`, rc 0. `check_submodule_docs.py`: OK, rc 0 | `receipts/head_submodule_boundaries.gen.py.txt`, `head_check_submodule_docs.py.txt` |
| Port census | `check_port_contracts.py`: OK, hdl 2181 / gptp-processor 127 / protocol-processor 1771, ratchets 217/19/111 unchanged. `--write-budget` at the head reproduces `scripts/port_docs.budget` byte for byte (diff rc 0; restored) | `receipts/head_check_port_contracts.py.txt`, `head_port_write_budget.txt` |
| Round 5: `git merge-tree --write-tree 3e67de9c 4ee2aa96` | Clean, rc 0. Its tree is `91bdf8b7`, the head's tree exactly | `receipts/r5_merge_tree.txt` |
| Round 5: patch-id | `git diff 3e67de9c f7d5fc3c` and `git diff 1e80128f 4ee2aa96` are both `8fa226cc88f7…` | `receipts/r5_patch_id_and_check.txt` |
| Round 5 touches no HDL, test bench or gitlink | `git diff --stat 3e67de9c f7d5fc3c -- hdl tb protocol-processor gptp-processor` is empty. #826 changes six files, none of them a generator or a gitlink | same |
| `git diff --check` against dev | merge-base with `02ca829a` is `02ca829a`: rc 0. Against `1e80128f`: rc 0 | same |
| #826's `milan_soc.py` hunks against this branch's | Disjoint regions. #826's `phy.sink` is the LiteSPI flash PHY's (`SPIPHYStage`, `add_spi_flash`), not the Ethernet PHY seam the frame-end toggle reads. No hunk touches `MilanMAC`, the transmit FIFOs, the toggle or the ICAPE2/PHY hold | read of both diffs (`git diff 1e80128f 4ee2aa96`, `git diff 1e80128f 3e67de9c` on `sw/litex/milan_soc.py`) |
| Round 4's HDL from dev | `milan_datapath.sv`'s only dev hunk drives the gPTP engine's `port_enabled_i` from `eff_link_w` (`:8930-8934`, #806). It lies away from `KL_reboot_ctrl`'s instance and changes nothing the egress account reads. `KL_reboot_ctrl.sv` blob `d2c74f47` is unchanged | `git diff 4aa5666e f7d5fc3c -- hdl/`, `receipts/prior_findings_at_head.txt` |
| Own probe: `[RB]` at the head (pinned Verilator 5.050 `rev v5.050`, wrapper sha256 `905795b9…`) | `pp_shadow: 68 checks, 0 failures`, `RESULT: PASS`, rc 0 | `receipts/probe_pp_shadow_rb.log`, `.rc` |
| Own probe: `make -C tb/verilator/reboot_ctrl` at the head | Legs: 46 and 221 checks, 0 failures. Mutants: `30 of 30 controls killed`, rc 0 (two independent runs) | `receipts/probe_reboot_ctrl_legs.log`, `probe_reboot_ctrl.rc`, `probe_reboot_ctrl_mutants.log`, `probe_reboot_ctrl_legs.note` |
| CDC census generator at five revisions | Equal to the committed file at `1e80128f`, `02ca829a` and `4ee2aa96`. **Differs** at `4aa5666e` and `f7d5fc3c` (F1) | `receipts/cdc_census_generator.txt`, `scripts/cdc_census_at.sh` |
| Archive `a16caad4` packet | 37 downloaded author-r5 files match `MANIFEST.json`'s `published_sha256`, 0 mismatches. `PR-BODY.md` equals the live PR body except for a trailing newline. The packet is hash-manifested; I found no detached signature in it | `receipts/archive_manifest_spotcheck.txt` |
| Route receipts (author-r5) | `prep.log` records head `f7d5fc3c` and pins `a9e84b66` / `135afd04`. The gate (#820's files at `50e5d08d`, per HANDOFF) prints `RESULT: PASS`, rc 0, AltSpreadLogic_high selected at 0.365 ns. Corners: Slow 0.365/0.053, Fast 1.633/0.015. LUT +9, FF +395, SLICE +7. All three Vivado rc 0. Route status: 0 routing errors. The #607 log check is clean on all three, and xvlog reports 0 findings. `deciding-paths.txt` names F4 (VexiiRiscv DMA write bridge) for AltSpreadLogic_high and the AECP `uop_e_r[imm]` -> `deb_cnt_r` path for the other two, and reports "worst listed path naming the ZQCS timer: none listed" for every directive | archive paths `author-r5/receipts/route/…` |
| AECP deciding path outside this PR's pin move | `KL_aecp_ucpu.sv`, `KL_aecp_nvm_writer.sv` and `KL_aecp_dyn_state.sv` have an empty diff between `f65c8ff7` and `a9e84b66` in `protocol-processor` | command in the session; result restated here |
| Author gate tables at `f7d5fc3c` | Static bank 32 rows rc 0 (xvlog run apart, rc 0), builder bank among them. rtl-fast rc 0. LiteX first aggregate rc 92 (`test_soc_timing_cuts` TIMEOUT, result unknown). Re-run 8/8 PASS. `test_soc_timing_cuts` alone: 23 `[ok  ]`, 0 failures. MAC model check (both levels) and `fw_service_budget`: rc 0 | archive `author-r5/receipts/{static,rtlfast,campaigns}-f7d5fc3c/` |
| PR body | States it carries PR #826's commits and merges after it. Keeps "Relates to #787". No closing keyword (`close`/`fix`/`resolve` + `#`) anywhere in the body | live PR body via the API |
| Comment rule on the delta | The added source lines in `4aa5666e..f7d5fc3c` show no new lane label, review round, reviewer ID or issue-comment ID written by this lane. The only hits are in dev's already-merged #70 files (a test string `"Volatile-B1"`, a JSON `remeasurement_assignment` URL), not this lane's | `receipts/delta_files_and_residue_scan.txt` |
| Hosted checks at the exact head | When read: 16 success, 1 skipped (Physical gPTP, nightly and manual), 32 still queued or in progress (Verilator and Yosys shards, firmware-boundary, publication-census, elaborate-gates-1, fail-fast). Not a verdict; the manager owns hosted/act acceptance | `receipts/hosted_checks_f7d5fc3c.txt` |

## Findings

### F1: MINOR (Docs) - the CDC census disagrees with its generator

- **Where:** `docs/diagrams/cdc_census.svg:113`, `docs/diagrams/cdc_census.drawio:57`, and the PNG rendered from the SVG (`docs/diagrams/cdc_census.png`).
- **Authority and evidence.**
  - `cdc_census.gen.py`'s own contract says "NOTHING HERE IS TRANSCRIBED… a new crossing appears in the drawing by itself".
  - `docs/litex/CLOCK_DOMAINS.md:289-290`, `docs/integration/INTEGRATION_GUIDE.md:132` and `docs/guides/SYSTEM_INTEGRATOR.md:63` send integrators to this generated census as the crossing inventory.
  - Run on an exported tree of each revision, the generator reproduces the committed SVG and drawio at `1e80128f`, `02ca829a` and `4ee2aa96`. At `4aa5666e` and at this head it writes `x3 call sites` for `MultiReg 2-FF`, where the committed file says `x2`. The third call site is this PR's PHY-hold MultiReg from round 2.
  - The author's own round-4 STOP and round-5 REVIEW READY say the same.
- **Impact.** The design's published CDC inventory leaves out this PR's new crossing. Its generator says otherwise, so the record a reader is told to trust is wrong. No gate reads the file, so nothing catches it. The crossing itself uses an approved primitive (MultiReg), so the RTL is not affected, which is why RTL is not attributed.
- **Required outcome.** At the merge head the committed census (SVG, drawio and PNG per the generator's usage line) equals the generator's output. Otherwise a reviewer-accepted public decision defers it to a named Issue, and the open finding still counts against Docs until the tree is fixed.
- **Verification.** `scripts/cdc_census_at.sh <repo> <work> <head>` prints `svg=equal drawio=equal`, and the PNG is re-rendered from that SVG.

### F2: MINOR (Docs) - the #787 route record still waits for #814

- **Where:** `docs/reference/SUBMODULES.md:485-507` and `docs/design/AREA_BUDGET.md:146-148`.
- **Authority and evidence.**
  - AGENTS.md section 7: "authoritative documentation is current". The PR body ticks "Documentation is updated where needed".
  - The adoption record gives only the `1be824fc` route (WNS +0.107 ns, refused, 57 slices left) and ends "The route is redone at the re-pin after #814 merges". `AREA_BUDGET.md:147` says the re-pin "is routed again after #814 merges".
  - This head carries #814's cuts, and this PR merges after #826. The re-pin's route set at this head passes the #818 gate: +0.365 ns, rc 0, `RESULT: PASS`, 15,787 slices, 63 free (author-r5 `route/results/head-set-check.log`).
  - The lines were accurate at `4aa5666e`, which did not carry #814. Round 5 changed what they depend on.
- **Impact.** Once merged, dev's authoritative records say the #787 route is still outstanding and refused. In fact it was measured and passes. The next reader of the area note will work from a superseded slice and WNS figure. The fix changes a measurement-status claim, so it is not wording only.
- **Required outcome.** The #787 adoption record and the area note's #787 lines state the route measured at the merge head: the gate's verdict, WNS and slices, citing the receipt. Or they state publicly where that route is recorded. They no longer present it as waiting for #814. The resource table itself stays as the record rule says (the PR body's "not re-recorded here" is not challenged).
- **Verification.** Read both passages at the next head against `head-set-check.log`. Check that `check_submodule_docs.py` and the docs workflow still pass.

### R1: RESIDUE (Docs) - stale push sentence in the PR body

- **Where:** the PR body, "Status", first paragraph.
- **Issue.** "The pushed head stays `4aa5666e` until the manager pushes." The PR's head is now `f7d5fc3c`.
- **Exact fix.** Delete the sentence, or replace it with "The manager pushed `f7d5fc3c`."

### R2: RESIDUE (Docs) - reviewer placeholders in the PR body

- **Where:** the PR body, "Linked Issue / roles".
- **Issue.** "Internal cleared-context reviewer: `[R<n>]`" and "External reviewer: `[R<n>]`" are still placeholders.
- **Exact fix.** "Internal cleared-context reviewer: `[R731]`" and "External reviewer: `[R732]`".

### S1: SUGGESTION (Docs) - ambiguous "this change" in the area note

- **Where:** `docs/design/AREA_BUDGET.md:145`.
- **Issue.** Dev's #806 sentence "this change meets the build floor at every corner on its best directive" now sits in a paragraph that also covers #787, so "this change" is ambiguous. The text is dev's own, carried verbatim by the resolution.
- **Suggestion.** If the area note is touched for F2, consider "#806's route meets…".

### Limit carried from the packet (not a finding)

`test_soc_timing_cuts` takes 686 to 789 s against the LiteX aggregate's 900 s member limit. The first aggregate run timed out as unknown and passed on re-run. This is #826's harness and was reviewed there. It is recorded so the merge-candidate run allows for it.

## Prior public findings at this head

| Finding | Severity, lenses | Status at `f7d5fc3c` |
|---|---|---|
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114`, a comment showing a lane label and an issue-comment ID | RESIDUE; Docs | **Retained.** Blob `2528a927` unchanged; line 113 still reads `# the [A10] arms of issuecomment-6518083444: …` |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, the link-down comment omits the egress wait | RESIDUE; Docs | **Retained.** Blob `43b1fc40` unchanged |
| R732-1 S1: `hdl/milan/KL_reboot_ctrl.sv:257-262`, a stray end on a take at count 0 | SUGGESTION; RTL, Robustness | Retained (optional); blob `d2c74f47` unchanged |
| R732-1 S2: `mutants.py`, no saturation control | SUGGESTION; Tests | Retained (optional); blob unchanged |
| R731-1 S1: `.mac_tx_beat_i` / `.mac_flush_i` wirings survive `[RB]` | SUGGESTION; Tests, Robustness | Retained (optional). The lines moved to `milan_datapath.sv:9765, 9768` because dev's 5-line hunk sits above them; the wirings are unchanged |
| R731-1 S2: quiet-window one-clock edges, `KL_reboot_ctrl.sv:290, 296` | SUGGESTION; Tests | Retained (optional); blob unchanged |

No prior finding is resolved by this delta. F1 above is new to the public record as a review finding. It was missed by R732-1 and R732-2.

## Per-lens results

[R732] PASS Conformance - `receipts/r5_patch_id_and_check.txt`, `receipts/r4_resolution_stat.txt`, the PR body - Round 5 changes no HDL, test bench or gitlink, and its patch-id equals #826's. Round 4's only HDL hunk is dev's #806 `port_enabled_i` wiring (`milan_datapath.sv:8930-8934`), away from the REBOOT path. So the REBOOT and ENTITY_DEPARTING behaviour graded at `4aa5666e` (IEEE 1722.1-2021 7.4.43, Milan v1.2 5.6.3.3) is unchanged, and `[RB]` re-passes here, 68 checks. The PR body keeps "Relates to #787", has no closing keyword, and states it carries #826.

[R732] PASS RTL - `hdl/milan/KL_reboot_ctrl.sv` blob `d2c74f47` (unchanged), `hdl/milan/milan_datapath.sv:8930-8934`, and the author-r5 route receipts (`head-set-check.log`, `timing-design-tables.txt`, `route_status.rpt`, `deciding-paths.txt`, `group-slacks.txt`) - The merged RTL is the two sides' disjoint hunks. The route at the head meets the +0.030 ns setup and 0 ns hold floors at every signoff corner on the selected directive with 0 routing errors. ZQCS (F3) is in no listed path. The AECP path's three modules are unchanged across the processor pin move. #826's SPI `phy.sink` is unrelated to the Ethernet toggle seam.

[R732] PASS Robustness - `receipts/probe_reboot_ctrl_legs.log`, `probe_reboot_ctrl_mutants.log`, `probe_pp_shadow_rb.log` - The delta changes no fault, reset, saturation or timeout path of the REBOOT controller. At this head the unit's bounds, dead-clock and tick-phase legs pass (46 + 221 checks), 30 of 30 mutants are killed, and `[RB]`'s dead-transmit-clock leg passes. #826's flash stage does not alter the drain's 10,000 ms bound or its flash-idle argument (`REBOOT_RESET.md` sections 3-4): the drain waits on the record writer, and IPROG resets the fabric stage.

[R732] PASS Tests - `receipts/probe_*`, author-r5 `static-f7d5fc3c/table.txt`, `rtlfast-f7d5fc3c/table.txt`, `campaigns-f7d5fc3c/{table.txt,table-litex-rerun.txt,litex-sims-rerun.log,soc_timing_cuts_direct-arms.txt}` - These are #826's suite in the aggregate, rc 0 / 8 of 8 / 23 arms. No test logic of this lane is in the delta. My own runs at the head reproduce the REBOOT suites' published counts.

[R732] MINOR Docs - `docs/diagrams/cdc_census.{svg,drawio,png}`; `docs/reference/SUBMODULES.md:485-507`; `docs/design/AREA_BUDGET.md:146-148` - F1 and F2 above. Otherwise the following hold:
- The CHANGELOG, `AREA_BUDGET.md` and `SUBMODULES.md` resolutions keep both sides' facts.
- The boundary diagram, PNG manifest, ROM ledger and port census equal their generators' output at the head.
- `CLOCK_DOMAINS.md` and `TESTING.md` are each the branch's copy plus #826's hunks (clean automatic merge).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Both merges' trees and patch-ids, the dev HDL hunk, `[RB]` re-run, PR body linkage | R732-3 (delta); R732-1 for code the delta does not touch | `f7d5fc3cc48ca80195428562fa86a46023df8e0d` |
| RTL | CLEAN | `KL_reboot_ctrl.sv` (unchanged), `milan_datapath.sv` merge hunks, `milan_soc.py` hunk disjointness, route-1x1 receipts at the head, AECP module diff across pins | R732-3; R732-1 for unchanged RTL | `f7d5fc3cc48ca80195428562fa86a46023df8e0d` |
| Robustness | CLEAN | `reboot_ctrl` legs and 30 mutants, `[RB]` dead-clock leg, drain/flash interaction with #826 | R732-3; R732-1 for unchanged paths | `f7d5fc3cc48ca80195428562fa86a46023df8e0d` |
| Tests | CLEAN | Own probes at the head, author gate tables (static 32, builder, rtl-fast, LiteX 8/8, `test_soc_timing_cuts` 23 arms, MAC model, service budget) | R732-3 | `f7d5fc3cc48ca80195428562fa86a46023df8e0d` |
| Docs | **UNCLEAN** (F1, F2 MINOR open; R1, R2 and the two prior RESIDUE carried) | The six conflict resolutions, regenerated records, CDC census at five revisions, adoption record and area note, PR body | R732-3 | `f7d5fc3cc48ca80195428562fa86a46023df8e0d` |

## Real limits

- I re-ran only the REBOOT unit bench, `[RB]`, the ROM-ledger record, the diagram, port and submodule-doc checks, and the CDC census generator. The rest of the gate evidence is the author's published receipts at this head, spot-checked by hash against the archive manifest. No manager source bank runs at this head, and I claim none.
- I did not re-route. The route figures are the author's receipts. The prep log binds them to `f7d5fc3c` and both processor pins. It records no explicit worktree-clean line; the HANDOFF states the gate files' provenance.
- The port census arithmetic ("base plus each side's per-file additions") was not recomputed per side. I checked only that the head's census equals its generator.
- I did not re-review #826's own change. It has its own reviews at `4ee2aa96`.
- Physical calibration was NOT RUN, and field or nightly skips are not hardware proof. The bench REBOOT run that closes #787 is still owed.
- Hosted checks at the head were still running when read.

## Pending manager duties

- F1 and F2 need a fix at a new head, or a recorded decision, followed by a re-review of Docs at that head.
- Carry R1, R2 and the two retained prior RESIDUE items (`mutants.py:113-114`, `torture_campaign.py:3135-3139`) to the residue checklist.
- Build and validate the current-dev merge candidate at the merge turn, after PR #826 and PR #820, and link its receipts.
- Accept hosted and act results at the exact head.
- Run the bench REBOOT checks on the rebuilt image.

## State after probes

The clone is at `f7d5fc3c`, `git write-tree` = `91bdf8b797065cd63a38650c6f74ff5c19d29690`. Worktree, index and HEAD are equal, and there is no untracked or ignored file. Gitlinks: `gptp-processor 135afd04`, `protocol-processor a9e84b66`, `third_party/lwSRP 08ee86e8`, `third_party/tsn-c-stack 70936b77`, `third_party/verilog-axis 48ff7a7e`, all checked out clean (`receipts/state_after_probes.txt`).

R732-3 FINISHED
