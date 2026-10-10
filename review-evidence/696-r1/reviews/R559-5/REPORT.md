[R559] POSITIVE - exact head 6de3904ec2d6b2f04325c94c7686519ecd92a202

External cleared-context review, round R559-5, of issue #696 / PR #706. Tree `4e0c5d5fc3bf69e7ebaf1c6d234bb144df658e43`, verified in the review clone. This is a delta review of `30073ee9..6de3904e`:

- `941ba746` merges dev `e8454e27` (M0s, #702, and the earlier merges) into the branch.
- `6de3904e` rewrites `AREA_BUDGET.md:368` and `MARK_II_AREA_PLAN.md:653-654` so they name #696's re-recorded route as the comparison record. This answers R558-5-F1.

The earlier rounds stand for everything the delta does not touch. No BLOCKER, MAJOR or MINOR finding is open at this head. This round adds one SUGGESTION. Three RESIDUE items from earlier rounds remain on the residue checklist, with their exact fixes refreshed below.

## Reconstruction

Sources, read in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. `docs/README.md`.
3. Issue #696: the frozen acceptance 1-4, assignment 6076750392, and rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293.
4. The PR body.
5. The diffs `6aa25dec..6de3904e`, `origin/dev..6de3904e` (17 PR files) and `30073ee9..6de3904e`.
6. The public author evidence at `97f433d6:review-evidence/696-r1/author/merge-receipts/record/`.

I read the prior public findings only after my own pass over the delta, which is the basis for the receipts below.

The delta's facts (`receipts/delta_provenance.txt`):

- **The merge is clean.**
  - `941ba746` has parents `30073ee9` and `e8454e27`.
  - Its tree `03143567` equals `git merge-tree --write-tree 30073ee9 e8454e27`, so it was a conflict-free automatic merge.
- **The merge touches only two of the PR's 17 files.**
  - Restricted to the PR's files, the merge changes only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md`.
  - Those changes are exactly dev's own M0s edits since the previously merged dev `8b61b709` (+68/-7 on both sides).
- **No lane byte outside the docs changed.**
  - `git diff 30073ee9..6de3904e` is empty for `hdl/`, `tb/verilator/maap/`, the MAAP differential test files, `sw/litex/` and `syn/ooc/pp_resource_baseline.json`.
  - The baseline blob is `2c1ca9fd` at both commits. It is byte-identical to the author's published post-record file `merge-receipts/record/resource-baseline-after.json`.
- **Head and dev differ only in the PR's 17 files.** Every dev-side file is identical.
- **`6de3904e` is a 3+/3- edit of the two lines.** Its text equals R558-5-F1's required replacement word for word (`receipts/r558_5_f1_text_match.txt`). Its message is one line with no trailer.

## Findings of this round

### R559-5-S1 - SUGGESTION - Tests, Docs - `docs/design/AREA_BUDGET.md:122-127,368`, `docs/design/MARK_II_AREA_PLAN.md:110-141,653-654` - no repository gate ties the area pages' record sentences to the recorded file

- **Evidence:** I built a disposable probe tree and made two plants:
  - restore dev's "The accepted 50,267-LUT route remains the comparison record." at `AREA_BUDGET.md:368`;
  - put 50,267 back at `MARK_II_AREA_PLAN.md:654`.

  `docs_check.py` still reports 0 findings (`receipts/probe_docs_check_on_mutated_text.txt`). The reviewer-side figure check fails each plant (`receipts/probe_revert_368.txt`, `receipts/probe_revert_654.txt`).
- **Impact:** none at this head; all figures match. A future merge that composes stale record text, as R558-5-F1 found, is caught only by review.
- **Optional outcome:** a docs-gate arm that compares the record-table and comparison-record figures with `syn/ooc/pp_resource_baseline.json`.

## Prior public findings, resolved or retained at this head

| Finding | State at `6de3904e` | Evidence |
|---|---|---|
| R558-5-F1 (MINOR, Docs): M0s text still named #645's 50,267 route as the comparison record | **Resolved** | `AREA_BUDGET.md:368` and `MARK_II_AREA_PLAN.md:653-654` equal the required text (`receipts/r558_5_f1_text_match.txt`). Every figure equals the recorded file (`receipts/record_figures.txt`, rc 0). The `git grep -n "50,267"` review below finds no sentence naming 50,267 as the current, last accepted or comparison gate record outside the retained residue |
| R558-5-R1 (RESIDUE): M0s's "records unchanged" lines at `AREA_BUDGET.md:359,376` and `MARK_II_AREA_PLAN.md:666` | **Retained**, unchanged at this head, on the residue checklist | Same three lines at the same numbers |
| R558-2-R1 / R559-2-R1 (RESIDUE): baseline sentences at `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:970` | **Retained**. The M0s insertion moved the third line to **`:1007`**; `:66-67` and `:317` are unchanged | Exact fixes as published in R558-2-R1, with `:970` read as `:1007` |
| R558-4-R1 (RESIDUE): stale head in the PR body | **Retained and widened**. The body still names `f909d6c4` under "Status" and "How to get into the same state", now five commits behind | Refreshed fix: replace both `f909d6c460344527f102f24b8e7a77f09959e755` with `6de3904ec2d6b2f04325c94c7686519ecd92a202`. Add a round-3/4 row ("R558-3-F1 / R559-3-F1: the datapath derivations clear inherited make flags; `b9b38961`, `30073ee9`"). Add a round-5 row ("merge of dev `e8454e27` (`941ba746`); R558-5-F1: the M0s status names #696's route as the comparison record (`6de3904e`)") |
| R558-3-F1 = R559-3-F1 (BLOCKER, make 4.3 capture) | Resolved at `30073ee9` (R558-4, R559-4); **still resolved** | `integration.mk` is byte-unchanged. At this head the integration build and run give 3/0, and the campaign's four datapath rows are `[ok]` (`receipts/maap_integration.log`, `receipts/maap_unit_and_campaign.log`). The hosted shard at this head was still running at report time (manager duty below) |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | Resolved at `f909d6c4`; **still resolved** | The sources are unchanged. Unit 172/0. The `MARK_II_AREA_PLAN.md` inventory equals the record for all 22 rows, and the gate row is correct |
| R559-1 residue R1-R3 | Applied; still applied | `MAAP_FABRIC.md:137,143`; `docs/findings/README.md:25` |
| R558-1-S1 (applied); R559-1-S1..S4, R558-3-S1/S2, R558-4-S1/S2, R559-4-S1/S2 (SUGGESTION) | Retained, optional; no lens effect | The sources are unchanged |

### The `50,267` review

At this head, `git grep -n "50,267"` over both pages gives:

| Location | Reading |
|---|---|
| `AREA_BUDGET.md:133` | "preceding #645 image" |
| `AREA_BUDGET.md:167` | Round 1d table, dated to the `5603c353` records |
| `AREA_BUDGET.md:368` | Dated to base `7c1b52be` |
| `MARK_II_AREA_PLAN.md:27`, `:898`, `:956` | The ledger start. Per `:113`, the levers and the ledger keep the baseline's route figures |
| `MARK_II_AREA_PLAN.md:76` | Section dated to dev `5603c353` |
| `MARK_II_AREA_PLAN.md:653` | Dated to "that base" |
| `MARK_II_AREA_PLAN.md:317`, `:1007` | The retained residue R558-2-R1 |

`:1007`'s "current three-endpoint record" is the wording that residue already carries. No figure on either page conflicts with the recorded file.

## Lens results

- [R559] PASS Conformance - `docs/design/AREA_BUDGET.md:122-129,354,361-370`, `docs/design/MARK_II_AREA_PLAN.md:110-113,638-656`, `syn/ooc/pp_resource_baseline.json` at `6de3904e` and at `7c1b52be`, issue #696 acceptance 3, rulings 6079087547 and 6089712293, `receipts/record_figures.txt`. What I checked:
  - **The record claims.** At base `7c1b52be` the record was #645's route: LUT 50,267 and RAMB36/RAMB18 74/27. At the head it is 50,230 with 74/27 unchanged, and 87.5 = 74 + 27/2. So "comparison record was #645's 50,267-LUT route; #696's 50,230-LUT route has since replaced it" is true, and so is "re-recorded it at 50,230 LUTs with 74/27 unchanged".
  - **Consistency with the rest of the pages.** The composed text agrees with "the table is the gate's record" (`:129`), with D7's "last accepted gate record" (`:354`), and with the ledger rule (`:113`).
  - **M0s claims.** Every M0s claim is kept: STOP, not measured, stored figures, the 121.5-tile ceiling, and M9 alone re-records.
  - **Acceptance 3.** The record is still the one written through the recipe: the blob equals the author's `record --write` output, and `check-baseline` passes.
  - **No interface change.** The delta changes no MAAP clause or interface claim; the Annex B conformance from R559-1/R559-2 stands for unchanged `KL_maap.sv`.
- [R559] PASS RTL - `receipts/delta_provenance.txt` (the `30073ee9..6de3904e` diff over `hdl/`, `sw/litex/`, `tb/verilator/maap/` and the record is empty, and the `e8454e27..6de3904e` diff outside the 17 PR files is empty), `receipts/maap_integration.log`. What I checked:
  - No RTL byte changed in the delta, and dev's merged changes contain no `hdl/` file.
  - The composed real datapath builds and passes 3/0 with the pinned Verilator 5.050 (`--version` reads `5.050 2026-07-01 rev v5.050`).
  - So the lane's clock, reset, CDC and FSM review from earlier rounds applies unchanged to this head's design inputs.
- [R559] PASS Robustness - `receipts/maap_unit_and_campaign.log` (unit `KL_maap: 172 checks, 0 failures`; campaign `checks: 52 failures: 0`, with the `clean` and `m4_datapath_clean` controls at rc 0 and 50 defects at rc 1), `receipts/pp_resource_gate_mutants.log` (192/192 mutants fail, control passes), `receipts/gate_selftest.log`, `receipts/pp_placement_selftest.rc`. What I checked:
  - At the composed head, the truncated-PDU, link-loss/return, supplied-seed boundary and pending-DEFEND plants are still each caught at their named check.
  - The merged M0s placement gate's refusals and selftests (unchanged schema, record and policy; full-split ROUTE INCOMPLETE and recipe-change refusals) all pass with the lane's re-recorded baseline file.
- [R559] PASS Tests - `receipts/maap_unit_and_campaign.log`, `receipts/maap_integration.log`, `receipts/maap_differential_summary.txt` (12/12 clean, 17/17 differential mutants caught), the `receipts/pp_baseline_*` logs, `receipts/measure_test_evidence.log` (ratchet PASS). What I checked:
  - The delta adds no test and removes none.
  - The merged firmware runner composes dev's AECP arms beside the unchanged MAAP arms (`test_ctrl_firmware.py:126-127,186`). The MAAP coverage-ratchet line is unchanged.
  - The figure check behind the Docs claim can fail: it fails each reverted-text plant (`receipts/probe_revert_368.txt`, `receipts/probe_revert_654.txt`).
  - The one gap is S1: no repository gate covers record wording. It is optional.
- [R559] PASS Docs - `docs/design/AREA_BUDGET.md:368-370`, `docs/design/MARK_II_AREA_PLAN.md:652-656`, every `50,267`/`50,230` occurrence on both pages, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:47`. Gate receipts: `docs_check` (0 findings, 202 pages), `gen_toc --check` (OK), `gen_toc --verify-anchors` (462 links reproduced), `check_em_dash --base e8454e27` and `--base 6aa25dec` (0 findings), `--selftest` (339 arms), all rc 0, run with the pinned Markdown renderer. What I checked:
  - The composed sentences are accurate and dated.
  - The record table, the route row of the #234 finding, and all 22 Mark II inventory route cells equal the recorded file.
  - The only wording defects are the retained RESIDUE items above.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `AREA_BUDGET.md:122-129,354,361-370`; `MARK_II_AREA_PLAN.md:110-113,638-656`; `pp_resource_baseline.json` at head and at `7c1b52be`; issue #696 acceptance 3 and the rulings; `receipts/record_figures.txt` | R559-5 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| RTL | CLEAN | Empty `hdl/`/`sw/litex/`/`tb/verilator/maap/`/record diff `30073ee9..6de3904e`; dev diff outside the PR files empty; composed datapath 3/0 | R559-5 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Robustness | CLEAN | MAAP unit 172/0 and campaign 52/0 at head; resource-gate mutants 192/192; placement and gate selftests with the lane's record | R559-5 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Tests | CLEAN (S1 optional) | Unit, campaign, integration, differential 12/12 and 17/17; firmware runner composition; test-evidence ratchet; figure-check plants | R559-5 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |
| Docs | CLEAN (RESIDUE R558-5-R1, R558-2-R1 / R559-2-R1, R558-4-R1 retained) | Composed M0s text; all record figures on both pages and in the #234 finding; five documentation gate runs | R559-5 | `6de3904ec2d6b2f04325c94c7686519ecd92a202` |

**How coverage carries.** This round re-covers every lens whose scope the delta touched, at the exact head. For the lane's unchanged artifacts, the earlier coverage carries because nothing in their scope changed since:

- `KL_maap.sv`, `milan_datapath.sv`, the MAAP harness, campaign and differential, and `MAAP_FABRIC.md`: R559-2 at `f909d6c4`, all five lenses.
- `integration.mk`: R559-4 at `30073ee9`.

My focused reruns at this head reproduce those artifacts' results.

## Real limits

- **No manager source bank at this head.** I neither claim nor infer one. The source-head execution evidence is the author's published gate receipts (through the measured merge `0df48637` and round 2) plus my focused runs above.
- **Banks not run, by scope.**
  - I ran no parent suite sweep, processor, gPTP, Yosys, firmware-bank or builder bank, and no `act` or Vivado run.
  - I re-measured no resource endpoint.
  - The all-fabric legacy parity of dev's recipe change rests on dev's own `pp_baseline.py --selftest` ("legacy parity ... PASS"). I generated no recipe script, because that needs an exported gateware build.
- **Hosted checks were not complete at report time.** At 12:19 UTC:
  - complete and successful: `bdd-conformance`, `changes`, `full-ci-gate`;
  - skipped: `Physical gPTP`, the nightly/manual context, which is not evidence;
  - running or queued: the docs checks, `elaborate`, `firmware-unit`, `verilator-lint`, the Verilator shards 0-4/5, `wire-accountability`, `yosys-elaboration` and the Yosys shards 0-3/4 (`receipts/hosted_check_runs.tsv`).
- **Local make version.** The local runs used the host's GNU Make. The make 4.3 shape of R559-3-F1 is evidenced at this head only once the hosted Verilator shard 1/5 completes.
- **No physical evidence.** Physical calibration was NOT RUN. Field-campaign skips are not hardware proof, and acceptance 4 (bench interop) is the post-merge bench lane.

## Pending manager duties

- Confirm exact-head hosted success for `rtl-fast`, `verilator-suites` (shard 1/5 `maap` 172/0 and 52/0 with the four datapath rows `[ok]`) and `yosys-portability`, plus the act replica, before merge.
- Build and validate the current-dev merge candidate at the merge turn (builder and native banks), and link its receipts on the PR.
- Carry RESIDUE R558-5-R1, R558-2-R1 / R559-2-R1 (`:1007` now) and R558-4-R1 (refreshed fix above) to the residue checklist. S1 and the earlier suggestions are optional.
- Obtain the internal reviewer's positive verdict at this exact head, and close the full completion bar, including post-merge containment.

## Receipts

Everything I ran is reproducible from `scripts/` and `receipts/`, listed in `MANIFEST.sha256`. The tracked blobs, modes, index and gitlinks of the review clone were verified after the probes (`receipts/clone_integrity.txt`). The gitlinks are:

- `protocol-processor` `2ad2f845`
- `gptp-processor` `5dce647a`
- `third_party/verilog-axis` `48ff7a7e`
- `third_party/lwSRP` `9197193e` (not checked out)
- `external` `efeb541a` (not checked out)

Generated `__pycache__` directories were removed, and the clone reports 0 untracked or ignored entries. The probe edits lived only in a disposable clone under `scratch/`.

R559-5 FINISHED
