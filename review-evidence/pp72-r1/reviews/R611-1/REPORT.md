[R611] POSITIVE - exact head 9540c34526c611a4f8ebac2e1b9dac890727e155

# R611-1: external independent review of PR #173 (issue #72), requirement-to-test traceability

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #173, `pp72-traceability`
- Exact head `9540c34526c611a4f8ebac2e1b9dac890727e155`, tree `330588f2998f95d694c5901a8317aed7029fc98d` (verified in the review clone)
- Source base (main) `2cbed0a987c1e68402658d69459ab7e5aa571adc`; four commits `a5bc371`, `ae9f0bb`, `8b35915`, `9540c34`
- Governing scope: issue #72 body (acceptance 1 to 6), lane assignment 6100765289, ruling 6101430201 (option 1: category-matched tracing; `REQ_TAG_LOG` executed evidence; static half in `make check`, executed half in the suites job)
- Verdict: **POSITIVE**. There are no open BLOCKER, MAJOR or MINOR findings. Two RESIDUE wording items and three SUGGESTIONs are recorded below. All five lenses are CLEAN.

## 1. Reconstruction

- **Repository conventions.** The tree has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md`, `docs/README.md` (ID registries, `REQ-` rows in 00 §6, the rule that `make check` is every target of 09 §7) and the guides.
- **Issue #72.** It asks for in-source REQ tags (acceptance 1), a script that fails an unmapped row or a vanished tag and runs in CI next to `check-matrix.py` (2, 5, 6), RND/STORM rows reported instead of passing silently (3), and 09 §8 to stop listing REQ-ID coverage as future work (4).
  - The lane assignment adds the four named failure classes, the five planted defects, the byte-identical records and the REQ → file:line → check-name audit order.
  - The ruling replaces the RND/STORM waiver bullet with category-matched tracing. It names the waivers for AEM-025 (GAP-06) and MAAP-001 (GAP-04) and fixes the CI split.
- **Diff.** 25 files, +1149/−125:
  - `scripts/check-req-tags.py`, new, 560 lines;
  - `tb/common/req_tag.{hpp,py}`, new;
  - 225 `REQ_TAG` statements in 18 sources across 13 suites;
  - `Makefile` (`reqtags` after `matrix`) and `.github/workflows/hdl.yml` (`REQ_TAG_LOG` run piped to `tee` under `pipefail`, then the executed half);
  - 00 §6: a Cov-state suffix on every row, the column key, the GAP-11 landed note and the REQ-VER-001 row; F00.2 GAP-11 "Verified by";
  - 09: §2 pointer, §7 `reqtags` row, the new §8.10, and the removal of the "To add" REQ-ID item.
  - No file under `hdl/` or `syn/` changes.
- **Public evidence.** `kebag-logic/milan-fpga@c47339e8…/review-evidence/pp72-r1` holds `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md`. The downloaded sha256s equal the manifest's `published_sha256` (`receipts/evidence/published_evidence_sha256.txt`).
- **Manager comments.** The issue and PR carry no manager evidence comments beyond the lane, ruling and review-start comments.
- **Prior public review findings at this head.** None exist: the PR has 0 reviews and 0 review comments, and its issue comments are only the two review-start notices. I checked after my own pass, so nothing needs resolving or retaining.

## 2. Lens results

### Conformance (CLEAN)

- **Acceptance against the head.**
  - 1: met for 101 of 109 rows that need a check. The 8 others are waived, and six of those carry no tag at all, so 1 is not literally met. The PR therefore says "Relates to #72", not "Closes". I agree that matches acceptance 1. The issue's disposition is the manager's call (§5).
  - 2/5/6: met. A row with no tag of its category fails as `UNCOVERED`. An in-source tag cannot outlive its check: removing it uncovers the row or the executed half names it. `reqtags` runs in `make check` right after `matrix`, and the hosted docs-gates job ran it at this head with success.
  - 3: superseded by the ruling. RND/STORM rows are traced where a check of that category exists (AEM-005, AEM-016, NOT-002, NOT-001, NOT-003) and waived with their own GAP where none exists (AEM-025 GAP-06, MAAP-001 GAP-04). Neither passes silently.
  - 4: met. 09 §8's "To add" now lists only the single-source scan.
- **Tag sampling.** `receipts/tag_vs_check.txt` lists every one of the 225 tags with the check statement under it. I read the RND/STORM, MTXW, TIM, NVM, TOL and Python tags against their checks and found no mislabel. The notable ones:
  - **RND.** `tb/originator/sim_main.cpp:882` R (zero divergence from an independent inflight model, 16 owners). `tb/pp_top/notify_phases.hpp:1635-1636` RN (20 controllers against a registry/lock model; capacity, NO_RESOURCES and pushes exercised).
  - **STORM.** `notify_phases.hpp:1146` ST1b (fan-out to 15 rows byte-exact), `:1211`/`:1216` ST2/ST2b and `:1356` CS (≤1 GET_COUNTERS round per descriptor per second).
  - **MTXW.** `acmp_listener` (112 F05.3 cells) and `adp_engine` P13 (45 F04.2 and 33 F04.3 cells). `tb/maap` U2 to U20 (the Table B.7 conflict matrix and walk) and `tb/srp_stream_fsms` Δ13 cells both fall inside 09 §3's MTXW definition, which names the SRP FSMs and the MAAP Table B.7 matrix.
  - **TIM.** For example AI3 (exact duplicate probe at T-ACMP-CMD, 195-260 ms), TD1/TD2 (T-LOCK-UNLOCK, T-NOTIF-TIMELIMITED at default), and U10c/e/k (monitor 27-66 s, retry ≤260 ms).
  - **Python.** The MDL rows and ADP-003/004 tag `LintTest.test_mutations`, which holds one refusal per L1-L12 check. `test_every_check_has_a_mutation` and `lint_suppression.py` (56 of 56 killed, rerun here) keep it complete.
  - **Cross-category labels.** These label a check without tracing its row, as designed: AEM-003 L7 DIR, AEM-011 D3N1 NVM, AEM-017 U2 TOL, AEM-026 A6 DIR, NOT-001 U8c DIR, NOT-002 push_step DIR, and the waived rows' TIM/DIR tags.
- **Waivers.**
  - Each of the eight names its own row's Finding GAP: AEM-019 and NET-004 GAP-05, NET-005 and MAAP-001 GAP-04, MVU-003 and MVU-004 GAP-03, AEM-025 GAP-06, SCP-001 GAP-12.
  - Every check a waiver reason cites exists: K9, K10, K11, K16, W23a2, AS2, M4, U17, U18, RN c, DR1b, and `tb/prng` E's kind-7 draw.
- **00 §6 Cov column.** The word diff only appends `; traced`, `; waived GAP-nn` or `; no check`. No Cov letter changed (word diff of 00 at base..head; the gate's `COV RECORD` check holds the suffix).
- **Stale "DOES NOT EXIST" wording** (ruling item 4). The tree does not carry it: a grep over docs, READMEs and scripts finds none.

### RTL (CLEAN)

- No `hdl/` or `syn/` file is in the diff, so `lint_hdl.sh` and `syn/yosys/run.sh` read identical inputs at base and head.
- `./scripts/lint_hdl.sh` at head, pinned Verilator 5.050: rc 0 (`receipts/lint_hdl_head.txt`). I did not run Yosys (see limits).
- The three mutation patches that target changed tb sources (`tb/pp_top/ctr_mutations/store-counts-domain-strobes.patch`, `store-link-detector-resets-up.patch`, `tb/srp_top/mutations/lv-sweep-misses-collision.patch`) apply with `git apply --check` at both base and head.
- Every changed suite source already included `../common/` at base, and every campaign driver copies `tb/common`, so the new header is present in campaign scratch trees.

### Robustness (CLEAN)

- **Placement scan** (`scripts/tag_context.py`, `receipts/tag_context.txt`): 0 of 225 tags sit under an unbraced `if`/`else`/`for`/`while`, so no inserted statement changes control flow.
  - The only conditional check, `tb/adp_engine/sim_main.cpp:997-999` (`if (a >= 0) CHECK…`), is guarded by the preceding `CHECK(a >= 0)`.
- **Static fault probes** (`scripts/gate_probes.py`, `receipts/gate_probes_static.txt`), each restored afterwards. The gate names every one:
  - the assignment's tag removed, unknown REQ, waiver without GAP, and row added with no tag;
  - RND relabelled DIR;
  - a matrix row with its Ver cell dropped (`UNKNOWN VER`; `check-matrix.py` alone passes this one);
  - a duplicate REQ row (`check-matrix.py` also fails);
  - a commented-out tag (`MALFORMED TAG`);
  - a waiver naming another row's GAP;
  - a Cov state edit;
  - a Python tag moved to another method.
- **Executed-half probes** (`receipts/gate_probes_executed.txt`) on my own full tagged run: a missing evidence line gives `DEAD TAG`, an extra line `STRAY EVIDENCE`, and a tag moved to another line with the stale evidence kept gives both.
- **Real dead tag** (`receipts/dead_tag_probe.txt`): the REQ-AEM-005 tag was moved into a never-taken branch in `tb/originator`, and that suite was rebuilt and run with `REQ_TAG_LOG` (107 PASS).
  - The static half passes, as designed.
  - The executed half fails `DEAD TAG REQ-AEM-005 tb/originator/sim_main.cpp:886`.
  - The other suites' evidence came from the full run: a spliced, not whole, rerun.
- **Weaknesses.** None defeats a planted defect, so they are recorded as SUGGESTIONs S1 and S2.

### Tests (CLEAN)

- **Self-test and static half.** `--selftest` gives 29 cases, OK. The static half gives `115 REQ rows: 101 traced, 8 waived, 6 need no check; 225 tags in 18 files, OK`.
- **Three suite runs, from fresh clones, run concurrently, pinned Verilator 5.050:**
  - base, unset;
  - head, unset;
  - head with `REQ_TAG_LOG` set, as the CI step runs it.
  - All three end rc 0 with `suites: 1029620 checks total, 0 failing`, and their outputs are byte-identical: sha256 `b1205c5d8cfb979eb93a54b692587924790bdf4c4de46ddf82547223d37c36f5`, equal to the author's recorded hash.
- **Executed half on that run.** rc 0, `req-tags executed: 225 evidence lines, 13 suites, OK`. 230 lines were written, 225 distinct (header tags run in more than one pp_top build).
- **Per-suite logs, base vs head** (`receipts/suite_logs_base_vs_head.txt`): all 34 suites' printed lines are identical. The only differences are build-tool lines (`receipts/suite_logs_tool_line_shapes.txt`): Verilator walltime reports, compiler command lines, and one unittest duration. Warning count is 180 at both.
- **Two campaigns at head that build changed files** reproduce the author's verdicts:
  - `tb/desc_store/lint_suppression.py`: 56 of 56 killed, rc 0;
  - `tb/acmp_talker/retry_mutants.py --jobs 8`: 62 killed, 7 equivalence controls, 1 performance control, rc 0.
- **Documentation gates, base and head** (`receipts/doc_gates_base_head.txt`): `check-matrix`, `gen_matrix --check`, `check-ids` (+ selftest; 563 → 565 files), `check-links`, `check-figures` (+ selftest) and `check-integrator-params` all give rc 0 with identical lines apart from the ids file count.

### Docs (CLEAN, with RESIDUE R1 and R2)

- 09 §8.10 matches the gate as built: the two halves, the evidence format, the manual recipe (it starts with `rm -f` of the evidence file), the coverage table and the eight waivers.
- 09 §7's `reqtags` row and 00's Cov key and GAP-11 note agree with the code. The PR body's coverage and validation claims agree with my runs.
- Two pieces of prose went stale around the change (R1, R2). Both are wording only.

## 3. Findings

### Open RESIDUE (wording only; not verdict-affecting; for the manager's residue checklist)

**R611-1-R1 (RESIDUE): the HDL engineer guide's gate list omits the new gate**

- Lens: Docs.
- Where: `docs/guides/hdl-engineer.md:255`.
- Evidence: the `make check` row enumerates "diagram lint, WaveDrom freshness, documentation links, compliance-matrix consistency, the module matrix, …" but not the REQ-tag gate. The `run_suites.sh` row at `:258` does not say that CI runs it with `REQ_TAG_LOG`, followed by the executed half.
- Impact: an engineer editing a tagged check is not pointed at 09 §8.10 from the guide.
- Exact fix:
  - after "compliance-matrix consistency," insert "the requirement tags' static half (`reqtags`, [09 §8.10](../architecture/09_verification.md#810-requirement-tags-and-the-traceability-gate-issue-72)),";
  - append to the `./scripts/run_suites.sh` cell: "; CI runs it with `REQ_TAG_LOG` set and then the tags' executed half (09 §8.10)".
- Verification: `make check` (`links`) passes.

**R611-1-R2 (RESIDUE): 09 §8 still counts two MTXW suites**

- Lens: Docs.
- Where: `docs/architecture/09_verification.md:145`.
- Evidence: the sentence "Two suites are MTXW walks in the sense of §3" reads as exhaustive. §8.10's gated coverage table now traces REQ-SRP-005, REQ-MAAP-003 and REQ-MAAP-005 by MTXW tags in `tb/srp_stream_fsms` and `tb/maap`, which §3's MTXW definition covers.
- Impact: the prose undercounts against the gated record. No gate or figure changes.
- Exact fix: change "Two suites are MTXW walks" to "Two suites are full-table MTXW walks". After the paragraph's sentence "Their READMEs carry the tables.", add: "The MTXW checks of the SRP and MAAP rows (§8.10) sit in `tb/srp_stream_fsms` (Tables 10-3/10-4 with Δ13) and `tb/maap` (the Table B.7 conflict matrix)."
- Verification: `make check` (`links`); `check-req-tags.py` unchanged.

### SUGGESTION (not verdict-affecting)

**R611-1-S1: the check-name binding is a bare substring test**

- Lenses: Robustness, Tests.
- Where: `scripts/check-req-tags.py:198-213` (`name_at_check`: `return name in "\n".join(text)`).
- Evidence: `receipts/gate_probes_static.txt` S6 and S6b. The ST1b tag renamed to `"ST1"`, or even to `"1"`, passes both halves.
- Impact: none at head. All 225 names are meaningful prefixes of their checks' messages, and adjacency plus the evidence line bind the tag to its check. But the "check name" column the lane asked for as the audit key is held only loosely.
- Suggested outcome: require the name to be a prefix of the first string literal of the check statement, or of the `expect_*`/`grade` label argument, with a self-test case.

**R611-1-S2: the executed half trusts the evidence file's freshness, and the suite name comes from the working directory**

- Lens: Robustness.
- Where:
  - `scripts/check-req-tags.py:298-321`;
  - `tb/common/req_tag.hpp:50-55` and `tb/common/req_tag.py:40`;
  - `tb/name_state/sim_main.cpp:6` and `tb/name_state/run.py:84`.
- Evidence:
  1. A stale evidence file whose line names a tag's current file:line satisfies that tag even if it no longer runs. CI is safe, because `$RUNNER_TEMP` is fresh per job, and the 09 §8.10 recipe starts with `rm -f`.
  2. `tb/name_state` compiles `tb/pp_top/sim_main.cpp` (and its tagged headers) and runs from a temporary directory. No tag executes there today (no `name_state` or temp-dir line in my evidence file), but a future tag on a helper it reuses would fail closed as `STRAY EVIDENCE <tmpdir> …`.
- Suggested outcome:
  - take the suite from the tag's own `__FILE__` path (`tb/<suite>/…`) rather than the working directory;
  - have the gate refuse an evidence file older than the suites log, or have the CI step write it under a name that is new for the run.

**R611-1-S3: REQ-VER-001's Ver cell**

- Lenses: Conformance, Docs.
- Where: `docs/00_MILAN_COMPLIANCE_REVIEW.md:544`, and `:371` (the Ver key: "lint = CI gate, 09 §7 · — = no dynamic verification").
- Evidence: REQ-VER-001 keeps Ver `—`. Its owning GAP-11 now reads "Verified by: lint: `scripts/check-req-tags.py` …" in F00.2 (`:565`), and REQ-REU-002 (held by `ids`) is `lint`.
- Impact: none on the gate; both values give "no check". This is a choice of record.
- Suggested outcome: consider Ver `lint` for REQ-VER-001, or say in the row why it stays `—`.

### BLOCKER / MAJOR / MINOR

None.

## 4. Reviewer ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #72 acceptance 1-6, assignment 6100765289, ruling 6101430201; all 225 tags against their check statements (`receipts/tag_vs_check.txt`, `receipts/table.md`); 8 waivers against their rows' GAPs and cited checks; the 00 §6 Cov word diff; the stale-wording grep | R611-1 | 9540c34526c611a4f8ebac2e1b9dac890727e155 |
| RTL | CLEAN | diff file list (no `hdl/`, `syn/`); `lint_hdl.sh` at head rc 0; three tb-targeting mutation patches applying at base and head; `../common` include and copy paths of the campaign drivers | R611-1 | 9540c34526c611a4f8ebac2e1b9dac890727e155 |
| Robustness | CLEAN (S1, S2) | `scripts/check-req-tags.py`, `tb/common/req_tag.{hpp,py}`, `hdl.yml`, `Makefile`; tag placement scan; 12 static, 3 executed and 1 rebuilt-suite dead-tag probes, all restored | R611-1 | 9540c34526c611a4f8ebac2e1b9dac890727e155 |
| Tests | CLEAN | selftest 29 OK; static OK; three full `run_suites.sh` runs (base, head, head tagged) byte-identical, 1029620 checks; executed half 225 lines OK; 34 per-suite logs, suite output identical; 2 campaigns at head; 8 documentation gates at base and head | R611-1 | 9540c34526c611a4f8ebac2e1b9dac890727e155 |
| Docs | CLEAN (R1, R2 RESIDUE; S3) | 09 §2, §3, §7, §8, §8.4, §8.10; 00 §6 key and rows, GAP-11 note, F00.2; hdl-engineer guide §6 and §8; README; PR body; published handoff | R611-1 | 9540c34526c611a4f8ebac2e1b9dac890727e155 |

## 5. Real limits and pending manager duties

- **Not run by me:**
  - the full `make check` target: no WaveDrom package is installed, and I did not run the Mermaid `lint` target (no diagram changed);
  - `syn/yosys/run.sh`: its inputs are unchanged, and full Yosys banks are out of my remit;
  - 14 of the author's 16 campaigns;
  - any parent (milan-fpga) gate.
  - The hosted docs-gates job ran `make check` at this exact head with success, which covers the first item.
- **The rebuilt dead-tag probe was spliced.** The originator suite was rerun, and the other suites' evidence came from my full tagged run, not a second full `run_suites.sh`.
- **Hosted CI at this exact head**, snapshot taken 2026-10-11 02:48 UTC (`receipts/hosted_check_runs_9540c34.json`, `receipts/hosted_suites_job_steps.txt`):
  - docs-gates: completed success (push and pull_request);
  - portability: completed success (both);
  - suites (both runs): still in progress. Steps "Lint (zero tolerance) + every suite" and "Every REQ tag ran, in a suite that passed" completed success; the mutation-campaign steps and later steps were in progress or pending.
  - Step logs were not downloadable while the job ran. The manager owns hosted and act acceptance.
- **No manager source bank** runs at this exact head, and I claim none. The current-dev merge candidate (source base `2cbed0a9`, live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`) and its builder and native banks are the manager's at the merge turn.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.
- **Pending manager duties:**
  1. Decide issue #72's disposition. Acceptance 1 stays literally unmet for six untagged waived rows (AEM-019, MVU-003, MVU-004, NET-004, NET-005, SCP-001), so "Relates" is correct; closing needs either an acceptance amended to the ruling or further work.
  2. Confirm the hosted suites job's remaining steps at this head.
  3. Carry R1 and R2 to the residue checklist.
  4. The published `author/HANDOFF.md` (path-redacted copy) shows `<bench-switch-model>: the bridge's` in its coverage-table row for `tb/pp_top/notify_phases.hpp:1771`, where the tree's check name is `<bench-switch-model>: the bridge's`. The redaction replaced a check name. This is an evidence-publication artifact, not a PR defect.
- **Packet.** Portable scripts are in `scripts/` and raw receipts in `receipts/`; both are listed in `MANIFEST.sha256`. Local paths are replaced by neutral tokens. Scratch trees under `scratch/` are not published. The review clone was verified at exact head bytes after all probes: index blobs and modes equal the HEAD tree, the worktree is clean, and there are no gitlinks (`receipts/clone_integrity.txt`).

R611-1 FINISHED
