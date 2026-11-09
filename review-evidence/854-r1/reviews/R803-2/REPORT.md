[R803] NEGATIVE - exact head de71984e4fc1b568065dffec483ea3ff51518604

Review R803-2 (internal, cleared context) of issue #854 / PR #862.

- **Head:** `de71984e4fc1b568065dffec483ea3ff51518604`, tree `33ee98fa7e7df8f2534daa08bc435f12deb3ff6d`.
- **Base:** `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, the live `dev` tip.
- **Delta reviewed:** `e87f2179..de71984e`, four commits on the round 1 head.
- **Scope:** the round 2 ruling on #854 (issuecomment-6739837279).

**Verdict: NEGATIVE.**

One MINOR finding under `Docs` (R803-2-F1) is the only cause. One sentence on the new findings page says the route's +13 FF is "the change's". The author's own published hierarchy reports show the change costs +10 FF. The other 3 are placement replication in the SoC, and appear only at ExtraPostPlacementOpt. This is the same kind of attribution error as R803-1-F1, and the fix is one sentence.

Everything else the ruling asked for checks out. I checked it against the published receipts and my own runs at the exact head:

- the re-baseline;
- the record's figures;
- the same-directive comparison;
- the tap's share table;
- the two new `[DR]` legs and their mutants;
- the RTL delta, which is comments only.

## Reconstruction (public state only)

- **Authority.**
  - AGENTS.md sections 3 and 5 to 8, and CONTRIBUTING.md.
  - The #854 body. Its Required items: count from the FIFO's own indication, saturate at 255, a self-checking overflow test, and a mutant that removes the count is caught.
  - The #854 comments: lane open, TAKEN, REVIEW READY (round 1), **the round 2 ruling** (items 1 to 5 and "Done means"), TAKEN (round 2) and REVIEW READY (round 2).
  - The PR #862 body at the head.
- **Interface authority.**
  - `third_party/verilog-axis/rtl/axis_fifo.v` at gitlink `48ff7a7e`:
    - `:76` and `:159-160`: `DROP_WHEN_FULL` requires `DROP_OVERSIZE_FRAME`;
    - `:204`: `full_wr`;
    - `:217`;
    - `:271-284`: `overflow_reg` rises after the last beat of a frame that is dropped, whether the FIFO was full or the frame is oversize.
  - `hdl/ieee8021q/filtering/rx_mac_filter.sv:26,239-244`: a runt is a frame with `tlast` at SOF, and it is always dropped.
  - `hdl/milan/milan_datapath.sv:309,3294`: `RXFILT_P`, default 1.
  - `docs/design/AREA_BUDGET.md:616-621`: the re-baseline rule, as positioned at the head.
- **Diff and history.**
  - `git diff ac0a01e3..de71984e` touches 15 files; `e87f2179..de71984e` touches 14.
  - The four commits:
    - `7a19f62b`: comments only;
    - `4d6a165c`: the `[DR]` runt and oversize legs, and `drops-mutant`;
    - `3a7660b1`: the baseline JSON;
    - `de71984e`: the area pages and the CHANGELOG.
- **Evidence.**
  - The author's round 2 packet is at `edebc85d43b99d3936774e5902df4142deea5bf4:review-evidence/854-r1/author-r2/`. All 535 files hash to their `published_sha256` in the published `MANIFEST.json`, with none missing and none unlisted (`receipts/evidence-manifest-verify.txt`).
  - The manager has posted no round 2 evidence comment. **I do not claim or infer a manager source bank at this head.**

## Ruling items, judged at the head

1. **Area re-baseline: met.**
   - **The measurements.** All six Vivado runs measured `7a19f62b` on `dev` `ac0a01e3`, with the gitlinks as recorded (`chain/aclone.txt`), and each returned rc 0 (`chain/*.rc`, `area/runs/runs.md`).
   - **Slot use.** At most three runs held slots at once, by the start and end times in `chain/*.slot.log`.
   - **No synthesis input moved.** I re-ran the three `git diff --name-only` ranges:
     - `e44a4d20` (record 15's commit) to `ac0a01e3`: documentation, `milan_dp` testbench files and the JSON only;
     - `ac0a01e3` to `7a19f62b`: two RTL files;
     - `7a19f62b` to the head: no `hdl/` file and no gitlink.

     So the record's claim that later commits change no synthesis input holds.
   - **The gate commands.** `check` against record 15 gave rc 0 on `route-1x1` (route set of three directives), `ooc-1x1` and `ooc-8x8`, and `record --write` gave rc 0 on all three. The published `baseline-final.json` is byte-identical to `syn/ooc/pp_resource_baseline.json` at the head, and `baseline-dev-ac0a01e3.json` is byte-identical to dev's file.
   - **The `measured` notes** name #854, `7a19f62b` and `ac0a01e3`. `record --write` does not write them (`pp_resource_gate.py:113`). `set_measured.py` sets them, as on earlier records.
   - **My own gate runs.** `check-baseline` gives `baseline PASS: 3 endpoints`. `--selftest` gives `312 arms and 500 generated cases PASS`.
   - **No STOP is owed.** The selected ExtraPostPlacementOpt route:
     - places 15,820 of 15,850 slices;
     - has WNS +0.166 ns at Slow and +1.633 ns at Fast, against the +0.030 ns floor;
     - has WHS +0.032 ns;
     - routes completely.
   - **The arithmetic agrees.** I checked every delta in the JSON, `AREA_BUDGET.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `MARK_II_AREA_PLAN.md`, `CHANGELOG.md`, the findings `README.md` row and the PR body against the receipts:
     - against record 15: +106 LUT, +13 FF, -9 slices, WNS -0.044 ns, WHS -0.004 ns;
     - against record 15's own ExtraPostPlacementOpt row (`234_...:204`): +151 LUT, +13 FF, -28 slices, WNS +0.054 ns;
     - out of context: +10 LUT and +10 FF at both shapes;
     - the percentages 84.44 %, 43.26 %, 99.81 %, 39.8 % and 70.9 %.
2. **Area text: met, except for one sentence (F1).** The text now:
   - presents the wrapper as the instance total, including `u_pp`'s +27 LUT;
   - gives the tap's own share: +8 LUT / +9 FF on the route, +7 / +9 and +6 / +9 out of context, and `ctl_fifo` +1 FF (`234_...:112-123`, `AREA_BUDGET.md:256-259`, PR body);
   - gives the same-directive comparison;
   - then gives the new record against record 15.

   The sentence at `234_...:110` contradicts that page's own table (F1).
3. **Wording: met.**
   - **Drain rate.** "Eight bytes every nine cycles" now appears in `README.md:175`, in the `sim_main.cpp` header (`:94-95`) and in the PR limitations. No "drains one byte a cycle" remains.
   - **Per-leg tally.** The PR body gives "base 738, vid73 738, crf 778, pending 317" and places `[DR]` in base, vid73 and crf. My run reproduced exactly those four tallies.
4. **Runt and oversize legs: met. The choice to keep the runt build out of the default legs is sound.**
   - **The runt sub-leg** (`sim_main.cpp:2068-2097`) runs in every default leg. There it shows the filter drops every runt: one overflow per kept frame lost, 108 = 108.
   - **The `RXFILT=0` build** (`Makefile:163-171`: `-GRXFILT_P=0` plus `-DRXFILT_PRUNED=1`) is the one build where runts reach the tap. My probe of it gives 157 overflows, 108 kept frames lost and a count of +108 (`receipts/probe_rxfilt0_control.log`).
   - **`counts-runts`** is killed in that build by `drops-mutant`. My probe confirms the PR's claim that the arm is *equivalent* in the filtered build: the same plant passes `[DR]` there, 19 of 19 (`receipts/probe_counts_runts_filtered.log`). The pruned build is therefore needed to kill it.
   - **Why it is not a fifth `make run` case.** The choice is sound:
     - `scripts/suite_shards.py:167` times `pp_shadow` as exactly four pieces, one per leg;
     - a fifth case changes the piece list that the hosted windows are balanced on;
     - the pruned build is a non-default configuration (`endstation_builder.py:412`, `--no-rx-mac-filter`);
     - the ruling's Done list names `drops-mutant`, not a new hosted leg.

     The consequence is recorded below as S1.
   - **The oversize sub-leg** (`sim_main.cpp:2104-2131`):
     - a 4,096-byte frame, 512 words, does not reach `full_wr`: it is kept, handed out whole and not counted;
     - a 4,097-byte frame raises one overflow and counts +1;
     - the 64-byte frame behind it is handed out.
   - **`misses-oversize`** leaves frames over 512 words uncounted. It is killed by exactly its named check, with 1 failing check. The plant's 512/513-word boundary matches the FIFO's 512-word depth.
   - **"Or longer than the FIFO"** appears in all five places it was asked for. Each matches `axis_fifo.v:275` (`full_wr && DROP_OVERSIZE_FRAME`):
     - the banner (`KL_pp_shadow.sv:72-75`);
     - the drop-logic comment (`:857-867`);
     - the port comment (`:752`);
     - `milan_csr.sv:699`;
     - the `PP_DIAG` row (`REGISTER_MAP.md:2456` and `:2469-2472`).
5. **RTL logic unchanged: proved.**
   - `scripts/strip_compare.py` removes `//` and `/* */` comments and whitespace, then compares the files at `e87f2179` and at the head. `KL_pp_shadow.sv`, `milan_csr.sv` and `milan_datapath.sv` all come out **SAME** (`receipts/rtl_comment_only.log`).
   - The delta has no other `hdl/` file, no gitlink and no synthesis script.
   - The new comment says `status_overflow` rises "for the cycle after that frame's last beat". That also holds for the oversize case (`axis_fifo.v:275-284`).

## Prior findings at this head

| Finding | Severity then | State at `de71984e` | Evidence |
|---|---|---|---|
| R803-1-F1 (PR area text: wrapper total, tap share, same-directive comparison) | MINOR | **Resolved** in the PR body, `AREA_BUDGET.md:256-259` and `234_...:98-123`. A new attribution error in the new findings section is R803-2-F1. | PR body "Area"; `check-r15-route-1x1.log` |
| R803-1-F2 (drain rate) | RESIDUE | **Resolved** | `README.md:175`; `sim_main.cpp:94-95`; PR limitations item 1 |
| R803-1-F3 (oversize wording and leg) | SUGGESTION | **Taken**: wording in all five places, plus the oversize sub-leg and `misses-oversize` | item 4 above |
| R803-1-F4 (reset during burst; `RXFILT_P=0`) | SUGGESTION | **Taken** for `RXFILT_P=0`. Reset during an overflow burst goes to #495 by ruling item 5 and stays open there, which is not a lens defect. | ruling item 5; PR limitations |
| R804-1-F1 (re-baseline or exemption) | MAJOR | **Resolved** by option (a) | item 1 above |
| R804-1-S1 (`RXFILT_P=0` runt leg) | SUGGESTION | **Taken** | item 4 above |
| R804-1-R1 (per-leg tally) | RESIDUE | **Resolved** | PR Status and gate table |
| R804-1-R2 (drain rate) | RESIDUE | **Resolved** | as R803-1-F2 |

## Findings

**R803-2-F1: MINOR, lens `Docs`.** At `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:110` the page says: "The LUT figure moves with placement at either directive; the flip-flop figure, +13 at both, is the change's."

- **Evidence.** From the author's published `area/runs/{eppo,aslh,eto}/baseline_hierarchy.rpt`, summarised in `receipts/ff-attribution.txt`:
  - **The RTL change adds 10 FFs:** the 8-bit count, `last_kept_r`, and `ctl_fifo`'s `overflow_reg`. The same page's table and the sentence after it (`:112-123`) say so: +9 in the tap and +1 in `ctl_fifo`. Both out-of-context endpoints moved +10, and the route's wrapper moved +10.
  - **The FF totals at the same RTL:**

    | Directive | This head | Record 15 (`:204`) | Change |
    |---|---:|---:|---:|
    | ExtraPostPlacementOpt | 54,850 | 54,837 | +13 |
    | AltSpreadLogic_high | 54,847 | 54,837 | +10 |
    | ExtraTimingOpt | 54,847 | not compared | |

  - **Where the other 3 FFs are.** `milan_datapath` has 43,435 FF at all three directives. The 3 FFs that only ExtraPostPlacementOpt adds are placement replication in the SoC, in `VexiiRiscvLitex/.../dma_bridge_write_bridge/aligner` (146 FF there against 143).
- **Impact.** The findings page states a wrong figure for the change's FF cost: +13 instead of the measured +10. It also contradicts the table that follows it, on the page this round added to fix area attribution (R803-1-F1). This is a claim about a measured figure, not wording alone, so it is not RESIDUE.
- **Required outcome.** Either option below; no record, JSON or source change is needed.
  - Rewrite the sentence so the change carries +10 FF: the count, `last_kept_r` and the FIFO's overflow register, as measured out of context and at the wrapper. The remaining +3 at ExtraPostPlacementOpt then belongs to SoC placement, as the AltSpreadLogic_high comparison (+10) shows.
  - Or drop the attribution and keep the figure.
- **Verification.** A reviewer re-reads `234_...:108-123` against `:204` and against `area/runs/{eppo,aslh}/baseline_hierarchy.rpt`: its top row, `milan_datapath` and `VexiiRiscvLitex`.

**R803-2-S1: SUGGESTION, lenses `Tests` and `Robustness`.** At `tb/verilator/pp_shadow/Makefile:163-171` and `scripts/suite_shards.py:167`:

- Two things guard the pruned-filter `[DR]` result that runts at a full FIFO are not counted: the `RXFILT=0` clean control and `counts-runts`. Both run only when `make drops-mutant` is run by hand. No hosted job builds `RXFILT=0`.
- Nothing is uncovered at this head. The RTL logic is unchanged, and the default legs cover every case those builds can reach.
- Optional: the next time the `pp_shadow` pieces are re-timed, add an `RXFILT=0 --drops-only` run (19 checks, short) to an existing piece.

**No RESIDUE in the delta.**

- The comment-rule scan of the added `hdl/`, `tb/` and `scripts/` lines found no lane label, review round, reviewer ID or comment ID.
- The JSON `measured` notes say "lane commit". That is record data in the same form as records 14 and 15, not a source comment (`receipts/comment-rule-scan.txt`).

## Executed at the exact head

I used Verilator 5.050 rev v5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version`). Each run used a disposable copy of the clone at the head. The commands are in `scripts/run_gates.sh`, `scripts/probes.sh` and `scripts/docs_subset.sh`.

| Command | rc | Result | Receipt |
|---|---|---|---|
| `make -j4 -C tb/verilator/pp_shadow` (base, vid73, crf, pending) | 0 | 738, 738, 778 and 317 checks, 0 failures. `[DR]` runs in three legs (results below the table). | `receipts/pp_shadow_suite.log` |
| `python3 drops_mutant.py` (`make drops-mutant`) | 0 | Both clean controls pass. All 8 arms are KILLED by their named checks. | `receipts/drops_mutant.log` |
| Probe: base leg with `RXFILT=0`, `--drops-only`, unmodified sources | 0 | 19 checks pass. Runt burst: 157 overflows, 108 lost, count +108. | `receipts/probe_rxfilt0_control.log` |
| Probe: `counts-runts` plant in the default filtered build | 0 (the arm survives) | 19 checks pass, so the arm is equivalent there, as the PR says | `receipts/probe_counts_runts_filtered.log` |
| `scripts/strip_compare.py . e87f2179 de71984e` on three RTL files | 0 | SAME, SAME, SAME | `receipts/rtl_comment_only.log` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` | `receipts/check_baseline.log` |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `312 arms and 500 generated cases PASS` | `receipts/gate_selftest.log` |
| `python3 scripts/docs_inventory.py --check` | 0 | OK | `receipts/docs_inventory.log` |
| `git diff --check ac0a01e3 HEAD` | 0 | no output | `receipts/diff_check.log` |
| A subset of 24 docs.yml steps (listed below the table) | 0 each | Three steps first returned 2 because the pinned Markdown renderer was missing, which is a harness artefact. I re-ran all three under a private venv installed from `tools/markdown/requirements.txt`, and each returned 0. | `receipts/docs_subset/` |
| Check the author packet's `MANIFEST.json`, prefix `author-r2/` | 0 | 535 ok, 0 mismatch, 0 missing, 0 unlisted | `receipts/evidence-manifest-verify.txt` |

The `[DR]` results in each of the three legs:

- burst: 31 lost, count 31;
- refused frames: +69 lost, +69 counted (158 overflows);
- runts: +108 lost, +108 counted (108 overflows, filtered);
- 4,096 B: kept and not counted;
- 4,097 B: counted +1;
- 501 lost in all; the count reads 255 and holds.

The docs.yml subset included:

- `check_em_dash.py --base ac0a01e3`;
- `gen_toc.py --verify-anchors`, `--check` and `--selftest`, under the pinned renderer;
- `check_port_contracts.py`, `docs_check.py` and `check_doc_style.py`;
- the idiom checks;
- `measure_test_evidence.py --check`.

**Not re-run.** For these I relied on the author's verified receipts:

- the six Vivado runs;
- `pp_resource_gate_mutants.py`: all 236 mutants fail. The gate code is not in the delta.
- the full docs.yml replay: every runner rc 0 in `gates/docsyml-de71984e/progress.txt`.

**Harness note.** Under `python3 -I` the gate script stopped at import, because isolated mode drops the script's directory from the module path. That is a harness artefact; the result above comes from the rerun without `-I`.

**Hosted checks at the exact head**, inspected but not accepted (`receipts/hosted-checks-snapshot.txt`, 2026-11-09T15:11Z):

- completed with success: 7 contexts;
- skipped: physical gPTP;
- still running or queued: the Verilator shards, the Yosys preparation, the firmware jobs and verilator-lint.

Hosted and act acceptance belong to the manager.

**Clone integrity** (`receipts/clone-integrity.txt`):

- HEAD and the tree are exact, and the index tree equals the HEAD tree;
- there is no tracked, untracked or ignored change;
- the six gitlinks match HEAD: `external` efeb541a (not initialised, as recorded), gptp 1616fc8f, processor 044cb25f, lwSRP 08ee86e8, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e;
- every plant was made only in a disposable copy.

## Reviewer-owned completion ledger (R803-2)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #854 Required R1-R4, with the logic unchanged. Ruling items 1-5 against `syn/ooc/pp_resource_baseline.json` (published `baseline-final.json`, `check-r15-*.log`, `record-*.rc`, `after-*.log`), `AREA_BUDGET.md:616-621` and `axis_fifo.v:204,217,271-284`. The executed `[DR]` figures and `check-baseline`. | R803-2 | de71984e4fc1b568065dffec483ea3ff51518604 |
| RTL | CLEAN | `KL_pp_shadow.sv:70-75,752,857-875` and `milan_csr.sv:699`, proved comment-only against `e87f2179` (`rtl_comment_only.log`). The comment text checked against `axis_fifo.v:76,159-160,275-284`. No other `hdl/` file or gitlink in the delta. | R803-2 | de71984e4fc1b568065dffec483ea3ff51518604 |
| Robustness | CLEAN (S1 is a SUGGESTION) | Runts at a full FIFO in the filtered and pruned builds (108 against 157 overflows, count +108). The oversize boundary at 512/513 words, with the frame behind it handed out. Saturation and hold at 255 (501 lost). Reset during a burst, deferred to #495 by the ruling. | R803-2 | de71984e4fc1b568065dffec483ea3ff51518604 |
| Tests | CLEAN (S1 is a SUGGESTION) | `sim_main.cpp:2058-2131,2178-2190`, `drops_mutant.py:46-90,110-163` and `Makefile:163-171,212-215`. The suite in four legs (738/738/778/317). `drops-mutant` 8 of 8, with both controls. The `counts-runts` equivalence probe in the filtered build. | R803-2 | de71984e4fc1b568065dffec483ea3ff51518604 |
| Docs | **UNCLEAN** (R803-2-F1, MINOR, open) | `234_PP_SHADOW_AREA_BASELINE.md:12-28,53-172`, `AREA_BUDGET.md:13,129-160,241-262,275-281,693-698`, `MARK_II_AREA_PLAN.md:59,940-941`, findings `README.md:25`, `CHANGELOG.md:11,59-84`, `REGISTER_MAP.md:2456,2469-2472`, `TESTING.md:748`, `pp_shadow/README.md:14,165-215`. The PR #862 body, the docs.yml subset and the comment-rule scan. | R803-2 | de71984e4fc1b568065dffec483ea3ff51518604 |

## Real limits

- I ran no Vivado, Yosys or out-of-context build. The area judgement rests on two sources: the author's published round 2 receipts, which I hash-verified against the packet manifest, and the repository's records.
- I ran no full parent, PP, gPTP, builder or docs.yml bank. Round 1's full sweep is not repeated, because the RTL logic is unchanged (proved above).
- **Not simulated:** reset during an overflow burst (#495), and hardware. Physical calibration NOT RUN. Field skips are not hardware proof.
- The manager has posted no round 2 evidence comment, and I infer no manager source bank at this head.

## Pending manager duties

- **F1.** Carry F1 to the author. After the fix, an internal re-review of the `Docs` lens is needed at the new head. If only the prose of `234_PP_SHADOW_AREA_BASELINE.md` changes, the other four lenses keep this round's coverage under AGENTS.md section 7, because nothing in their scope moves.
- **Merge-candidate validation.** At the merge turn, validate the current-dev merge candidate (builder and native banks) against the live `dev` of that time, and run the act replica.
- **Hosted acceptance at the exact head.** Most contexts were still queued or running at my snapshot.
- **#495.** Keep reset during an overflow burst on #495, per ruling item 5.
- **External review.** The external review at this head.
- **Merge.** Maintainer authorization for the merge.

R803-2 FINISHED
