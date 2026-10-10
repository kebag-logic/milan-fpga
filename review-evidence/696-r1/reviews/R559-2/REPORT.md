[R559] POSITIVE - exact head f909d6c460344527f102f24b8e7a77f09959e755

Round R559-2. External cleared-context review of PR #706 (issue #696). Tree `9d6acafcd88efe041dfed3f008f0d70941c16e5e`.
This is a delta review of `030eb98a..f909d6c4`: three commits (`eb2cac84`, `f03e254e`, `f909d6c4`), answering R559-1-F1/F2/F3 and R558-1-F1 under the round-2 assignment 6093171536.
Source base `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Merged dev `8b61b70902f3ebf118e56967277e2686731081bd`. Live dev named by the manager: `aef7ac66605c4404900ce04cbaaeff88e41bb880` (not built here).

## Verdict in one paragraph

All four prior findings are resolved at this head, and this round adds no BLOCKER, MAJOR or MINOR finding.

- **M5 (R559-1-F1):** the new unit check `M5 B.3.5.9 link loss is no event; return reprobes` holds the port down for 24,000 scaled cycles (2.4 s), which is longer than a full PROBE walk. It does this in PROBE and in ANNOUNCE.
  - It requires that the drop causes no restart and no PROBE.
  - It requires that the fresh four-PROBE walk starts at once after the rise.
  - R559-1's published `r_restart_on_link_loss.patch`, applied unmodified, fails exactly that check: 172 checks, 1 failure.
  - The equivalent campaign row `m5_restart_on_link_loss` is rejected at that check in the default `mutants.py` run.
  - Two of my own new plants (walk released while the link is down; timer frozen while the link is down) are caught only by this check.
- **Docs:** the MAAP area figures match the published reports. The Mark II current inventory and gate row equal the recorded file: 22 rows, 66 figures, 0 differences. The zero-seed fixture is named by its current MAC.
- **No change to design inputs:** from the measured merge `0df48637` to this head, nothing outside `docs/`, `tb/` and the record file changed, so the resource record stands.

I record one RESIDUE (wording only) and retain R559-1's four optional suggestions.
All five lenses are covered clean at this head.

## Reconstruction (public state only)

I read these in order:

1. `AGENTS.md` and `CONTRIBUTING.md`.
2. Issue #696:
   - the body and acceptance 1-4;
   - assignment 6076750392;
   - every author STOP comment;
   - rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293;
   - REVIEW READY 6092935897;
   - the round-2 assignment 6093171536;
   - REVIEW READY 6093452983 (head `f909d6c4`).
3. The IEEE 1722-2016 Annex B text: Table B.3 "Protocol events", Table B.7 "MAAP state machine" (the PortOperational! row) and B.3.5.9. I read them from a licensed copy that is not republished here.
4. `docs/design/MAAP_FABRIC.md`, `MARK_II_AREA_PLAN.md`, `AREA_BUDGET.md`, the #234 findings page, `docs/findings/README.md`, and `syn/ooc/pp_resource_baseline.json` at the head and at `5603c353`.
5. The diff `030eb98a..f909d6c4` and its history. I also checked the changed paths from `0df48637` and from `6aa25dec`.
6. Public evidence:
   - `97f433d6:review-evidence/696-r1`: the author's MAAP utilization reports;
   - `696-review-evidence@b96793c3`: R559-1's plant `r_restart_on_link_loss.patch`, blob `cac1017e`, sha256 `f9e8de81…6a5f`, equal to the R559-1 manifest entry.

I read the prior PR findings (R558-1 and R559-1) only after I had finished my own pass over the diff and run my probes.

## What I executed (receipts in this packet)

All simulation used the pinned Verilator 5.050 wrapper; its identity is checked in `receipts/verilator_identity.txt`.
All builds ran in a scratch clone at the head, never in the review clone.

| Run | Result | Receipt |
|---|---|---|
| MAAP unit harness (`make run`) | 172 checks, 0 failures, rc 0; all five M5 lines pass | `receipts/head/unit_run.*` |
| Real-datapath harness (`integration-build` + run) | 3 checks, 0 failures, rc 0 | `receipts/head/integration.*` |
| Coverage target | `KL_maap.sv` 215/215 lines, gate PASS, rc 0 | `receipts/head/coverage.*` |
| Default campaign, unmodified (`python3 mutants.py`) | `checks: 52 failures: 0`, rc 0; `m5_restart_on_link_loss` rejected at `M5 B.3.5.9 link loss is no event; return reprobes` | `receipts/head/campaign_default.*` |
| Parallel replay of the same campaign (its `MUTANTS` table, `run_case()` rule and four datapath rows) | 52 rows: 2 clean controls, 50/50 defects at their named checks, rc 0 | `scripts/parallel_campaign.py`, `receipts/head/campaign_parallel.*` |
| R559-1 plant `r_restart_on_link_loss.patch`, applied with `patch` unmodified | unit harness: 172 checks, 1 failure, only the new M5 check, rc 1. Datapath harness: 3 checks, 0 failures (its M5 check keeps the short outage, as the author discloses). The plant is byte-equal to the campaign row's replacement. | `scripts/reapply_plant.sh`, `receipts/plant_reapply/*` |
| Reviewer M5 probes (5 plants + clean control) | all 5 fail the new check. `p2_idle_while_down` and `p3_timer_frozen_while_down` fail **only** the new check. `p1_both_edges`, `p4_no_return_event` and `p5_return_counts_conflict` also fail the older M5 checks. | `scripts/probe_m5.py`, `receipts/probes/*` |
| Mark II inventory and gate row vs record | 22 rows, 66 figures, 0 differences. Gate row: 0.114 - 0.030 = 0.084 < 0.25, so the floor binds first. | `scripts/check_markii_inventory.py`, `receipts/markii_inventory_check.*` |
| Previous record vs head record | only `route-1x1` figures and scopes changed; both standalone endpoints keep every figure and scope; tolerance, floor and ceiling unchanged; the `5603c353` file equals the previous record | `receipts/record_previous_vs_head.log`, `receipts/markii_baseline_section_vs_records.log` |
| MAAP area figures vs published reports | `g_maap.maap_engine`: base 439/280; M3 step at `39571196` 441/340; dev `8b61b709` 443/280; merge result 445/340 | `receipts/maap_engine_rows.txt` |
| Design inputs since the measurement | `0df48637..HEAD` changes only 5 docs pages, the record file and 2 MAAP harness files; nothing under `hdl/`, `syn/` (other than the record), `sw/`, `scripts/` or `.github/`; gitlinks identical | `receipts/diff_names_measured_to_head.txt` |
| Static docs and record gates | `docs_check` 0 findings; em-dash 0 findings over `8b61b709..HEAD` and over `030eb98a..HEAD` (339/339 arms); TOC OK; doc style OK; DOC_MAP OK; solution docs OK; module matrix up to date; test-evidence ratchet PASS; `check-baseline` PASS (3 endpoints). All rc 0. | `receipts/static/*` |
| Commit format | 3 commits, each one line with no trailers | `receipts/commit_format.log` |
| Hosted snapshot at the exact head (04:09:47Z) | 13 completed with success, 1 skipped (`Physical gPTP (nightly and manual)`, a conditional skip), 6 in progress (Verilator shards 0, 1, 2 and 4, `firmware-unit`, `elaborate`). This is not acceptance evidence. | `receipts/hosted_check_runs.tsv` |
| Review clone restore | HEAD and tree exact; index tree = HEAD tree; status clean; no untracked or ignored files; no index flags; 1,238 tracked blobs rehash equal with their modes; gitlinks `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` at their pins and clean (`external` and `third_party/lwSRP` are uninitialized, as in the supplied clone) | `scripts/verify_clone.sh`, `receipts/clone_restore.log` |

## Prior findings: resolved or retained at this head

- **R559-1-F1 (MINOR, Tests): RESOLVED.**
  - Where: `tb/verilator/maap/sim_main.cpp:68-71` (`kOutageCyc = 4 * kProbeMaxCyc`) and `:767-803`; the campaign row is at `tb/verilator/maap/mutants.py:70-72`.
  - The outage of 24,000 cycles exceeds the worst-case remaining walk, which is three intervals under 6,000 cycles plus the at-once ANNOUNCE. A restart taken at the loss would therefore finish before the return.
  - In PROBE, the check requires exactly the three remaining timer PROBEs and the ANNOUNCE, all on the original range and none within `kAtOnceCyc` of the loss.
  - In ANNOUNCE, it requires no frame at all.
  - In both states it then requires: state ANNOUNCE with the offset and the conflict counter unchanged; on the rise, PROBE with validity revoked; four PROBEs, the first within `kAtOnceCyc`, then the ANNOUNCE; and no conflict counted.
  - This matches Table B.3, which lists PortOperational! only as the transition *to* an operational state, and Table B.7, whose PortOperational! cell in PROBE and DEFEND is Stop timer, INITIAL/Restart!.
  - The plant and campaign evidence is in the table above.
- **R559-1-F2 (MINOR, Docs): RESOLVED.**
  - `MARK_II_AREA_PLAN.md:110-113` names #696's re-baseline and the measured merge `0df48637`.
  - The route column at `:121-142` equals the head record, 22/22 rows. The standalone columns equal both records.
  - The gate row at `:56` states the binding floor at the +0.114 ns record, consistent with `AREA_BUDGET.md:383`.
- **R559-1-F3 (MINOR, Docs and Tests): RESOLVED.**
  - `MAAP_FABRIC.md:227-228` and the banner at `sim_main.cpp:645-646` name `02:00:00:00:00:00` with clock 0, which is `kZeroSeedMac` at `sim_main.cpp:59`.
  - Under `KL_maap.sv:148-149`, its low 32 bits plus clock 0 are zero, so the `0xACE1` fallback is exercised.
  - `zero_seed_freezes_the_probe_draw` and `zero_seed_freezes_the_announce_draw` are still caught in the default campaign.
- **R558-1-F1 (MINOR, Docs): RESOLVED.**
  - `MAAP_FABRIC.md:143` attributes 441/340 to the M3 step at `39571196`.
  - `:145-147` state the merge-result 445/340 (+6/+60 against `6aa25dec`) and the lane share +2/+60 against dev `8b61b709` (443/280).
  - All four figures equal the published `util_hier_base.rpt` rows.
- **R558-1-S1 (SUGGESTION):** applied at `MARK_II_AREA_PLAN.md:56`.
- **R559-1 residue R1-R3:** applied with the exact wording R559-1 gave, at `MAAP_FABRIC.md:143`, `:36` and `:137-138`, and at `docs/findings/README.md:25`.
- **R559-1-S1 to S4 (SUGGESTION): retained.** They are optional and unchanged; the author gives reasons for not applying them. They do not affect any lens.

## Findings of this round

### R559-2-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:66-67` - baseline source line points at the live record file

- **Evidence:** the dated section "Baseline recorded on dev `5603c353`" says "Source: `pp_resource_baseline.json`, all three `record` objects. Each `measured` note identifies `a5ca6e51…`".
  - Its figures and input SHA-256 values equal the record as committed at `5603c353`, which is byte-equal to the pre-#696 record (`receipts/markii_baseline_section_vs_records.log`).
  - The linked file at this head now holds #696's record, measured at `0df48637`.
  - The section heading dates the baseline, and `:110-113` now say the current record differs, so no figure, measurement or gate claim is affected. This is wording only.
- **Exact fix:** replace "Source: [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json), all three `record` objects." with "Source: [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json) as committed on dev `5603c353`, all three `record` objects; #696 has since re-recorded the file (see [Current processor inventory](#current-processor-inventory))."

No BLOCKER, MAJOR or MINOR finding.

## Lens results with evidence

- [R559] PASS Conformance - `tb/verilator/maap/sim_main.cpp:767-803`, `docs/design/MAAP_FABRIC.md:104-111`, IEEE 1722-2016 Table B.3, Table B.7 (PortOperational! row) and B.3.5.9 - what I checked:
  - The documented and graded M5 contract matches the clause. Entering the operational state is the only event; leaving it is not an event, so the walk continues.
  - The return restarts from PROBE with a fresh walk and counts no conflict (Restart! here is not a conflict).
  - The citation "Table B.3 defines no event for leaving the operational state" is correct: Table B.3 is "Protocol events".
  - No RTL changed since `030eb98a`, so R559-1's clause-by-clause RTL conformance at `030eb98a` stands for `KL_maap.sv` and the datapath integration.
  - Acceptance 1-3 stay met: M5 now has a check that tells loss from return, plus its planted defect. Acceptance 4 is the post-merge bench lane.
- [R559] PASS RTL - `hdl/ieee1722/maap/KL_maap.sv` (unchanged since `030eb98a`; `git diff 030eb98a..HEAD -- hdl syn sw scripts .github` is empty), `receipts/diff_names_measured_to_head.txt` - what I checked:
  - No RTL, synthesis, firmware, script or workflow byte changed in the delta.
  - Only `docs/`, `tb/` and the record changed between the measured merge `0df48637` and the head, with gitlinks identical. So the recorded endpoints and the 445/340 MAAP figure describe this head's design inputs.
  - I re-read `KL_maap.sv:146-157` and `:399-440` for the M5 edge, the restart priority and the pending-response cancel; they agree with the new check's expectations.
- [R559] PASS Robustness - `sim_main.cpp:767-803`, `receipts/probes/summary.txt`, `receipts/head/unit_run.log` - what I checked:
  - A long outage in both active states, a re-rise after it, and the absence of spurious frames, conflicts or offset changes during it.
  - Five link-path defects, each caught, including two that only the new check sees (link-down release and timer freeze).
  - A steady level still makes no repeated restart (`M5 stable operational level does not restart`, twice).
- [R559] PASS Tests - `tb/verilator/maap/sim_main.cpp:68-71,645-646,767-803,974`, `tb/verilator/maap/mutants.py:70-72`, `receipts/head/*`, `receipts/plant_reapply/*`, `receipts/probes/*` - what I checked:
  - The new check runs in `make run` and in the default `make` target (run, then mutants).
  - It can fail for the defect it claims: the unmodified plant fails it alone.
  - The campaign row is the same edit as that plant.
  - Unit 172/0, datapath 3/0, coverage 215/215, campaign 52/0 (50 defects), test-evidence ratchet PASS.
  - The banner names the fixture actually used.
- [R559] PASS Docs - `docs/design/MAAP_FABRIC.md:36,104-111,137-148,224-232`, `docs/design/MARK_II_AREA_PLAN.md:56,108-147`, `docs/findings/README.md:25`, `syn/ooc/pp_resource_baseline.json`, the published `util_hier_base.rpt` rows, `receipts/static/*` - what I checked:
  - Every changed figure equals the recorded file or a published report.
  - The attribution of 441/340 and 445/340 is correct; the M5 loss contract and the fixture MAC are current.
  - The links resolve (`234_PP_SHADOW_AREA_BASELINE.md:32`, `AREA_BUDGET.md:114`).
  - All static docs gates pass.
  - The one wording defect is RESIDUE R559-2-R1.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_main.cpp:767-803`; `MAAP_FABRIC.md:104-111`; IEEE 1722-2016 Table B.3, Table B.7 PortOperational! row, B.3.5.9; issue #696 acceptance, the rulings and assignment 6093171536; unchanged `KL_maap.sv` | R559-2 | `f909d6c460344527f102f24b8e7a77f09959e755` |
| RTL | CLEAN | `KL_maap.sv` (byte-unchanged since `030eb98a`, re-read at `:146-157`, `:399-440`); `0df48637..HEAD` changed-path list; gitlinks | R559-2 | `f909d6c460344527f102f24b8e7a77f09959e755` |
| Robustness | CLEAN | `sim_main.cpp:767-803`; 5 reviewer link-path probes plus control; unit log | R559-2 | `f909d6c460344527f102f24b8e7a77f09959e755` |
| Tests | CLEAN | `sim_main.cpp`, `mutants.py`, `Makefile`, `integration.mk`; unit, datapath, coverage, default and parallel campaign, unmodified plant re-application, test-evidence ratchet | R559-2 | `f909d6c460344527f102f24b8e7a77f09959e755` |
| Docs | CLEAN (RESIDUE R559-2-R1 only) | `MAAP_FABRIC.md`, `MARK_II_AREA_PLAN.md`, `docs/findings/README.md`, `AREA_BUDGET.md:383`, `234_PP_SHADOW_AREA_BASELINE.md:32`, record file at head and `5603c353`, published MAAP reports, static docs gates | R559-2 | `f909d6c460344527f102f24b8e7a77f09959e755` |

## Real limits

- **No Vivado run.** The endpoint records and the MAAP OOC figures are the author's published measurements. I checked them by:
  - equality with the published reports;
  - `check-baseline`;
  - showing that no design input changed between the measured merge and this head.

  I did not re-measure them, and I did not recompute the record's input digests: that needs the measurement directories.
- **Not rerun here (author receipts only):** the parent suite sweep, Yosys portability, the xvlog parser gate, behaviour, lint, the firmware RV32 bank, the firmware differential, the processor banks, field campaigns and the full 94-command documentation bank.
  - I ran 10 documentation and record gates, in `receipts/static`.
  - Lint and portability inputs are unchanged since `030eb98a`.
  - The differential and firmware inputs are unchanged since `0df48637`.
- **Simulator and renderer:**
  - The coverage target's annotation step used the system `verilator_coverage` (5.052). The model was built and run with the pinned 5.050.
  - The pinned Markdown renderer was installed from `tools/markdown/requirements.txt` with `--require-hashes`, into a scratch-only virtual environment.
- **Datapath harness and the loss edge:** the real-datapath M5 check still uses a short outage, so the loss-edge plant passes it (3/0). The author discloses this. F1 required the unit harness, the datapath harness or both, so it is satisfied by the unit check.
- **Invalid early runs:**
  - A first campaign run on a plain export without git metadata could not build the four datapath rows; it was discarded and not counted.
  - An early accidental invocation of the campaign driver with the system simulator wrote only to temporary space; its output was discarded.
  - All counted results come from the scratch git clone at the exact head.
- **Path redaction:** a local home-directory path prefix in build logs is redacted to `$HOME`.
- **Hosted and manager evidence:** the hosted snapshot was mid-run; no hosted verdict is claimed. No manager source bank ran at this head, and none is claimed or inferred.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof. No bench or hardware work was done.

## Pending manager duties

- Carry RESIDUE R559-2-R1 to the residue checklist.
- R559-1-S1 to S4 remain optional.
- Build and validate the current-dev merge candidate against live dev `aef7ac66` (builder and native banks), and link its receipts on the PR.
- Accept the hosted contexts and the local replica on the exact final head. Six hosted jobs were still in progress at my snapshot.
- Obtain the internal reviewer's round at this head; the merge needs two positive reviews and the full completion bar.
- Hand acceptance 4 (bench interop with the reference peer) to the post-merge bench lane, followed by post-merge containment.

## Receipts and reproduction

All paths are relative to this packet and are listed in `MANIFEST.sha256`.

**Scripts**

- `scripts/probe_m5.py <tree> <work> <out>` (set `VERILATOR`)
- `scripts/parallel_campaign.py <tree> <work> [jobs]`
- `scripts/reapply_plant.sh <tree> <patch> <work> <out> <verilator>`
- `scripts/check_markii_inventory.py <repo>`
- `scripts/verify_clone.sh <clone> <head> <tree>`

The default campaign was run as `cd tb/verilator/maap && VERILATOR=<pinned> python3 mutants.py`.

**Receipts:** under `receipts/`.

R559-2 FINISHED
