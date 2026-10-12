[R558] POSITIVE - exact head 26e2748f47b0d8fa533f53203264d9f31fc13c48

# R558-12 - issue #696 / PR #706 - delta review at `26e2748f`

- **Head:** `26e2748f47b0d8fa533f53203264d9f31fc13c48`, tree `b93fd1d39c06c069c01aa8ceeeb74fbb6083472e`.
- **Previous source head:** `aa980479aafd1d72c72015707fa6618b5aa47cb1`. R558-10 and R559-8 are POSITIVE at that head.
- **Commits since `aa980479`:**
  - `b075a994` merges live dev `c6bd08c6`, which carries #722 (M5, #640) and #707 (#621).
  - `26e2748f` rewords `docs/design/MARK_II_AREA_PLAN.md:1095-1096` and `:1111`.
- **Role:** cleared-context internal reviewer. I applied all five lenses.
- **Verdict:** POSITIVE.
  - The merge is the mechanical merge, and the wording commit changes only those three lines.
  - R558-11-F1 (MINOR) and R558-11-R1 (RESIDUE) are both resolved, in exactly the wording the review asked for.
  - This round finds no new BLOCKER, MAJOR, MINOR or RESIDUE.
  - The RESIDUE items retained from earlier rounds do not affect any lens.

## 1. Scope reconstructed from public state

- **Read in order:**
  1. AGENTS.md (the completion bar and the lens rules).
  2. The #696 issue: its title, state and body.
  3. The round start comment, 6118407882.
  4. `syn/ooc/pp_resource_baseline.json` at `e8454e27`, `c6bd08c6`, `aa980479` and `26e2748f`.
  5. `docs/design/MARK_II_AREA_PLAN.md` at `c6bd08c6` and at this head.
  6. The diffs `aa980479..b075a994`, `b075a994..26e2748f` and `c6bd08c6..26e2748f`, and the history.
  7. The public evidence index at `97f433d6:review-evidence/696-r1` (it holds `MANIFEST.json` and `author/`).
- **Prior public findings:** I read them only after my own pass over the delta and my own executed checks (section 5).
- **Question for this round:** does `26e2748f` add anything beyond (a) the automatic merge of dev `c6bd08c6` and (b) R558-11's F1/R1 wording? Does the merged plan name, for every lane, the record that lane was compared against, without implying that the current `route-1x1` record is 50,267?

## 2. Delta facts

Receipts: `receipts/merge_provenance.txt`, `receipts/composition_check.log`, `receipts/pr_files_blob_vs_aa980479.txt` and `receipts/delta_b075a994_26e2748f.diff`.

- **The merge is mechanical.**
  - `git merge-tree --write-tree aa980479 c6bd08c6` gives `4650fd5d9d5c940bc6788491229dc808cf866962`, rc 0, with no conflict.
  - That is exactly the tree of `b075a994`, whose parents are `aa980479` and `c6bd08c6`.
- **The PR delta is carried unchanged.**
  - Each of the 17 files in `c6bd08c6..b075a994` has the same per-file patch-id as `09c7231e..aa980479`. `09c7231e` is the lane base.
  - Excluding the plan, `c6bd08c6..26e2748f` and `09c7231e..aa980479` have the same stable patch-id, `b93344d5...`.
  - At `26e2748f`, 16 of those 17 files are byte-identical blobs to `aa980479`. The 17th is `MARK_II_AREA_PLAN.md`.
  - So `KL_maap.sv`, `milan_datapath.sv`, the MAAP harnesses and campaign, the firmware differential, the record file and the other documents are all unchanged since the reviewed source.
- **The file changed on both sides** since the lane base is only `MARK_II_AREA_PLAN.md`:
  - dev added the M5 section;
  - the PR edits are disjoint from it.
- **The wording commit:** `b075a994..26e2748f` is 1 file, +3/-3, at `:1095`, `:1096` and `:1111`.
  - The new text is exactly R558-11's required wording for F1 and its exact fix for R1. I compared it against the R558-11 public comment, section 3.
  - No figure, table or other line changes.

## 3. Record identity across the merged plan

Receipts: `receipts/lane_vs_both_records.log`, `receipts/record_vs_lane_routes.log`, `receipts/plan_composition.log` and `receipts/plan_record_citations.txt`.

- **The records:**
  - #645/#647's record, as stored at dev `e8454e27` and still at dev `c6bd08c6`: LUT 50,267, FF 54,413, slices 15,779, RAMB 74/27, WNS +0.299, WHS +0.031.
  - #696's record, at this head: LUT 50,013, FF 54,306, slices 15,753, RAMB 74/27, WNS +0.233, WHS +0.017.
- **Every lane section names the record it was compared against.**

  | Lane | Base row | Base row equals `e8454e27` record | Comparison sentence | Lane route vs #645/#647 record | Lane route vs #696 record |
  |---|---|---|---|---|---|
  | M2 | `:691` | YES, all 7 figures | `:696-697`: names #645/#647's record and says #696's replaced it; passes against both | PASS | PASS |
  | M6 | `:943` | YES | `:948`: "Against #645/#647's record ... also passes against #696's record" | PASS | PASS |
  | M5 | `:1088` | YES | `:1095-1096`: same wording as M2 (this commit) | PASS | PASS |

  The M5 route is 49,577 LUT, 54,226 FF, 15,791 slices, 74/27 RAMB, WNS +0.097 and WHS +0.036. Against #696's record it moves LUT -436 (tolerance 500), FF -80 (600) and slices +38 (80). WNS falls 0.136 (limit 0.25) and stays above the +0.030 floor. So both pass claims at `:1096` hold.
- **No sentence implies that the current record is 50,267.** Every 50,267 citation at this head is listed in `plan_record_citations.txt`. Each one is either the dated baseline or ledger start, or the named #645/#647 record:
  - `:27` "Recorded start";
  - `:76` the table under "Baseline recorded on dev `5603c353`";
  - `:317` and `:978` the ledger start;
  - `:656` "the last accepted gate record was #645/#647's", followed by `:657` "now at 50,013 ... that record is the comparison anchor";
  - `:691`, `:943` and `:1088` the base rows at dev `e8454e27`, each named as #645/#647's record;
  - `:1036` and `:1125` the ledger arithmetic.

  `:110-113` makes the distinction explicit: the gate's current record is #696's, and the levers and ledger keep the baseline's route figures.
- **`:293` ("The later adopted records are in the current baseline above") is not a finding.** "Baseline" is the plan's own term for the ledger start (`:113`, `:657`), and it does not name the gate record.
- **D7 lines:** the M2, M6 and M5 lines each read "M<n> does not re-record the gate under D7" (`:707`, `:969` and `:1111`).
- **Other checks still hold:**
  - The current-inventory route column equals the record's scopes: 22 rows and 66 figures, 0 differences.
  - The partial-central figure 37,957 + 166 + 479 + 182 = 38,784, which is 744 over 38,040, matches `:1110`.

## 4. Executed evidence at this head

Toolchain (`receipts/toolchain.txt`):

- Verilator 5.050 (`2026-07-01 rev v5.050`) through the scoped wrapper. I checked the wrapper's target binary: sha256 `fb2cc573...`.
- GNU make 4.4.1 and host python3 3.14.7 with pyyaml.
- A pre-existing documentation environment (cmarkgfm 2025.10.22, html5lib 1.1, pyyaml 6.0.3, wavedrom 2.0.3.post3).

The suites ran concurrently in the review clone (`scripts/run_suites.sh`). Their ignored build outputs were removed afterwards.

- **MAAP target** `make -C tb/verilator/maap all`, rc 0 (`receipts/maap_all.log`, `.rc`):
  - unit: `KL_maap: 186 checks, 0 failures`;
  - campaign: `== maap mutants: checks: 65 failures: 0 ==`.
  - The campaign includes the real-datapath clean control `m4_datapath_clean` (rc 0). It elaborates the merged `milan_datapath` with M5's `milan_csr` and gPTP `7dda9c3b`.
  - Every datapath plant (link, clock, seed and first-offset) is rejected by its named check.
- **CSR suite** `make -C tb/verilator/csr run`, rc 0 (`receipts/csr_run.log`, `.rc`). This is the suite for M5's changed block. Legs: 408/0 (four builds), 121/0, 44/0 and `csr_lock` 5/0 twice. No leg fails.
- **Datapath suite** `make -C tb/verilator/milan_dp run`, rc 0 (`receipts/milan_dp_run.log`, `.rc`):
  - 11,955 checks, 0 failures:
    - gptp 182, gptp-lat 182, 1x1 236, notify 421, crflic 417, dynmap 162;
    - nxn 1,967, divergent 1,969, nxn8 3,751, nxn4c 1,967;
    - nolpf 236, prune 33 (MAAP_P = 0), ax1x1 233, aclk 193;
    - render controls 6/6.
- **Documentation, registry and record gates**, two runs, every command rc 0:
  - `scripts/doc_gates.sh` (`receipts/doc_gates_venv/`): 39 of 39 pass.
  - `scripts/run_doc_gates.sh` (`receipts/doc_gates_venv2/`): 38 of 38 pass.
  - Em-dash gate:
    - `--base b075a994`: 0 findings over 3 added lines in 1 page;
    - `--base c6bd08c6`: 0 findings over 347 lines in 7 pages;
    - `--base aa980479`: 0 findings over 346 lines in 19 pages.
  - `docs_check.py`: 0 findings across 204 Markdown files.
  - `gen_toc.py --verify-anchors` (487 links) and `--check` (144 pages).
  - `check_doc_style.py`, `DOC_MAP.gen.py --check`, `gen_module_matrix.py --check`, the code-quality and idiom scans, and `lint_rtl.py --check` (90 <= ratchet 90).
  - `pp_resource_gate.py check-baseline`: "baseline PASS: 3 endpoints". `pp_resource_gate.py --selftest` and `pp_baseline.py --selftest` also pass.
- **Plan checks:**
  - `scripts/check_plan_composition.py` (rc 0);
  - `scripts/record_vs_lane_routes.py aa980479 26e2748f` (rc 0);
  - `scripts/lane_vs_both_records.py` (rc 0): every base row and every lane route against both records, see section 3.
- **Clone integrity** (`receipts/head_integrity.txt`):
  - HEAD, the HEAD tree and the index tree are all `b93fd1d3`;
  - porcelain status is empty;
  - `diff-index HEAD` is clean, so blob bytes and modes match;
  - the ignored-file set equals its state before the run;
  - all five gitlinks are as committed;
  - `gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e` are checked out and clean;
  - `external` and `third_party/lwSRP` are uninitialized at their gitlinks, as they were before.

## 5. Prior public findings at this head

I read these after sections 2-4.

| Finding | State at `26e2748f` | Evidence |
|---|---|---|
| R558-11-F1 (MINOR, Docs; M5 `:1095-1096`) | **Resolved** | The wording is exactly R558-11's required outcome. The base row equals the named `e8454e27` record, and M5 passes against both records (`lane_vs_both_records.log`) |
| R558-11-R1 (RESIDUE; `:1111`) | **Resolved** | `:1111` reads "M5 does not re-record the gate under D7." |
| R558-9-F1 (MINOR; M2/M6 anchor), R558-9-R1 (RESIDUE) | **Still resolved** | `:696-697`, `:707`, `:948` and `:969` are unchanged |
| R558-5-F1 (MINOR; M0s anchor) | **Still resolved** | `:656-657` is unchanged |
| R558-1-F1, R558-3-F1 = R559-3-F1 (BLOCKER), R558-6-F1, R558-7-F1, R559-1-F1/F2/F3, R559-6-F1/F2 | **Still resolved** | Their artifacts are byte-identical to `aa980479`. The campaign is 65/0 and the integration clean control passes |
| R558-2-R1 / R559-2-R1 (RESIDUE; plan `:66-67`, `:317`, `:1125`) | **Retained** | The lines are unchanged. Wording only, with the exact fixes as published |
| R558-5-R1 (RESIDUE; `AREA_BUDGET.md:370`, `:387`, plan `:669`) | **Retained** | Unchanged |
| R558-10-R1 / R559-7-R1 (RESIDUE, PR body) | **Retained** | The live PR body still reads "review ready at `32582421...`" (`:16`), `# 32582421...` (`:175`) and "Hosted checks and the local workflow replica need the pushed head." (`:252`) |
| Earlier SUGGESTIONs (R558-3/4/6/7/8, R559-1/3/4/5/6/7) | **Retained, optional** | No lens effect |

## 6. Findings of this round

None at BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION level.

## 7. Lens results (artifact-specific)

```text
[R558] PASS Conformance - hdl/ieee1722/maap/KL_maap.sv, hdl/milan/milan_datapath.sv, docs/design/MAAP_FABRIC.md byte-identical to aa980479 (receipts/pr_files_blob_vs_aa980479.txt); receipts/maap_all.log (186/0, 65/0 incl. m4_datapath_clean) - the Annex B behaviour reviewed POSITIVE at aa980479 is carried unchanged and its unit, campaign and real-datapath checks pass at this head
[R558] PASS RTL - merged milan_datapath (PR KL_maap wiring + dev milan_csr.sv M5 read path + gptp-processor 7dda9c3b) at tree b93fd1d3; receipts/merge_provenance.txt (merge-tree = 4650fd5d), receipts/milan_dp_run.log (11,955/0 incl. MAAP_P=0 prune), receipts/csr_run.log (rc 0), doc_gates_venv2 lint_rtl --check - no RTL changes after the mechanical merge, and every elaboration and leg passes
[R558] PASS Robustness - tb/verilator/maap/mutants.py at this head; receipts/maap_all.log - link-loss/return, clock, seed and truncation plants through the merged eff_link_w / ptp_now_w wiring are rejected by name; dev changes neither driver
[R558] PASS Tests - tb/verilator/maap/{Makefile,integration.mk,mutants.py,sim_main.cpp,sim_integration.cpp} byte-identical to aa980479; integration.mk derivation against dev's milan_dp/Makefile builds (m4_datapath_clean rc 0); receipts/doc_gates_venv (measure_test_evidence --check, suite inventory gates) - every planted defect fails its named check
[R558] PASS Docs - docs/design/MARK_II_AREA_PLAN.md:691-707, :943-969, :1088-1111, every 50,267 citation (receipts/plan_record_citations.txt); receipts/lane_vs_both_records.log, plan_composition.log, doc_gates_venv (39/39), doc_gates_venv2 (38/38), check-baseline PASS - each lane names its comparison record, none implies the current record is 50,267, and R558-11-F1/R1 are resolved; earlier RESIDUE items are retained
```

## 8. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_maap.sv`, `milan_datapath.sv` and `MAAP_FABRIC.md` (byte-equal to the source); MAAP unit, campaign and integration control at this head | R558-12 (this round); source conformance R558-10, R559-8 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| RTL | CLEAN | The merged datapath with M5 `milan_csr` and gPTP `7dda9c3b`; `milan_dp` 11,955/0; CSR suite rc 0; lint | R558-12 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Robustness | CLEAN | Campaign plants through the merged link, clock and seed wiring; truncation plants | R558-12 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Tests | CLEAN (earlier SUGGESTIONs retained) | MAAP harnesses, campaign and `integration.mk` derivation; test-evidence and suite gates | R558-12 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |
| Docs | CLEAN (RESIDUE R558-2-R1 / R559-2-R1, R558-5-R1 and R558-10-R1 / R559-7-R1 retained for the residue checklist) | `MARK_II_AREA_PLAN.md` M2, M5 and M6 sections and the 50,267 citation sweep; record file at four revisions; 39 + 38 gates; check-baseline | R558-12 | `26e2748f47b0d8fa533f53203264d9f31fc13c48` |

## 9. Real limits

- **Not run:**
  - the full parent, PP, gPTP, Yosys and builder banks;
  - the firmware differential: no firmware file changed since `aa980479`;
  - `KL_maap` line coverage: its inputs are byte-equal to `aa980479`;
  - the `milan_dp_gm_steps` suite: dev's suite, and its code inputs are unchanged by the PR's 17 files;
  - Vivado, act and hosted runs, hardware and bench.
- **No manager source bank** exists at this head, and none is claimed or inferred.
- **The route record does not describe this image.** The `route-1x1` record measures #696's `bee1b0d7`. This head also carries M5's `milan_csr.sv` and the #621 gPTP pin. No route was measured, because that needs Vivado.
- **Physical calibration was NOT RUN.** Field skips are not hardware proof.
- **Hosted checks at this head were mostly pending** at snapshot time (`receipts/hosted_checks_snapshot.txt`). Some jobs passed: Yosys shards 1-3, verilator-lint, changes, full-ci-gate, docs-check-no-git, bdd-conformance and wire-accountability. The Physical gPTP context was skipping. Nothing is concluded from that snapshot.
- **Documentation environment:** it has pycparser 3.1, where `tools/markdown/requirements.txt` pins 3.0. The renderer pins (cmarkgfm, html5lib) match.
- **Redaction:** host home-directory paths in the logs are replaced with `<pinned-verilator-root>` / `<home>`. Nothing else was edited.

## 10. Pending manager duties

- The current-dev merge candidate's builder and native banks, at the merge turn. This includes the `AREA_BUDGET.md` merge-bank route comparison: since the record's measured revision, the dev delta touches `milan_csr.sv` and the gPTP pin.
- Hosted and act acceptance at the exact head.
- Carrying the retained RESIDUE items to the residue checklist.
- The external positive review and the maintainer's merge authorization.

R558-12 FINISHED
