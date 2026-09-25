[R301] POSITIVE - exact head 551e4b5dfa8ac7ec68a3161c95d4000eb6337396

# R301-5: composition review of issue #545 / PR #563 on the merge-train candidate

- **Role:** [R301], external independent reviewer. Cleared context. Composition acceptance only.
- **Candidate:** `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`, tree `bea28456ef036cb8cd8c94a800b1b6921ab6108c`.
- **Parents:** C_551 `0e26e0ac07abf1043ac2712fe39f92de0b34f2dd` and PR #563 head `ddf8151c478fc54c98608589c1afe9525739d6a4`.
- **Verdict:** POSITIVE.
  - The composed tree adds no defect beyond the reviewed sources.
  - No BLOCKER, MAJOR, MINOR or SUGGESTION finding is raised against the composition.
  - All five lenses were applied at the candidate head.

## 1. Reconstruction

I read the following, in this order:

1. `AGENTS.md`, `CONTRIBUTING.md` sections 2-3 and 6, and `docs/README.md`.
2. The #545 body, which states the frozen acceptance.
3. The public scope decisions on #545:
   - 5816509756 (acceptance 1 decided);
   - 5827358783 (scope, citation correction);
   - 5828714628, 5830332403, 5831902801, 5833028966 and 5835673886 (round decisions);
   - the executor's evidence comments, the last being 5836177064 at `ddf8151c`.
4. The review-start notice 5836962950.
5. `git diff 0e26e0ac..551e4b5d` and the lineage.
6. The exact-head hosted check runs at `ddf8151c`.

I read the prior public review findings only after my own pass and runs (section 7).

## 2. Composition map

**Lineage** (`receipts/lineage.txt`):

- The train (C_551) grows from dev `b3458db0` through the queued candidates, ending #443, #559 and #551.
- Live dev `5c78ce2e` is not an ancestor of C_551. Its two merged PRs are, though:
  - #562 source `fa1b5c36`;
  - #561 source `b3458db0`.
- The PR head carries dev `5c78ce2e`. So the candidate is the first tree that joins #545 to the #559 and #551 changes.

**The merge is delta-preserving in both directions:**

- For every one of the PR's 38 files, the changed-line multiset of `5c78ce2e..ddf8151c` equals that of `0e26e0ac..551e4b5d`.
- For every train file, `5c78ce2e..0e26e0ac` equals `ddf8151c..551e4b5d`.
- Both file sets are identical: 38 files, +686/-56 for the PR.

**Files the PR changes that a predecessor in the candidate also changed** (`receipts/overlap_files.txt`). The list has seven files; the manager's note names six.

| File | #545 hunk | Predecessor hunk | Interaction judged |
|---|---|---|---|
| `hdl/milan/milan_datapath.sv` | Slew wiring: `:1464`, `:2766-2770`, `:5570`, `:6918`, `:7010` | #551 licence: `:6648-6649` and its comments; `crft_res_active_w` `:5314` | Disjoint signals. Both mutant campaigns' anchors resolve exactly once. Every front end and leg below passes |
| `docs/testing/CI_WORKFLOWS.md` | `mmcm_servo` budget row `:159` and prose | #559 docs-check step section `:1200` | Disjoint sections. `ci_events.py --check` reads 1655 contract items |
| `docs/testing/TESTING.md` | Campaign rows `:272-273`; suite row `:494` | #559 harness exception `:165`, `:380`; #562 `crf_rx` row | Rows agree with the candidate's targets and inventories |
| `docs/reference/REGISTER_MAP.md` | `MCSRV_STAT` `0x8F8` row `:2027` | #551 `CRFT_CTRL` `:938`, `LWSRP_*`, prose; #562 `CRF_CTRL` `:839` | Different registers. Anchor and link gates pass |
| `CHANGELOG.md` | New section `:33`, contents `:11` | #551 bullets inside older sections (e.g. `:116`) | TOC regenerates identically. The em-dash gate passes |
| `tb/verilator/milan_dp/README.md` | gmstep inventory `:657`; tail `:1083` | #551 `obj_crflic` row `:27`, licence sections | No cross-reference between them. Counts still match `CONTROLS` |
| `scripts/measure_test_evidence.py` | `slew_mutants.py` `:597`; `gmstep_mutants.py` `:634` | #562/#541 `crf_rx/mutants.py` `:603` | No duplicate dict key (28 keys, 0 duplicates). `--check` and `--selftest` pass |

The manager's note omits `scripts/measure_test_evidence.py`. The PR's dispositions and the train's `crf_rx` disposition were both merged without conflict. A Python dict literal silently keeps the last duplicate key, so I checked the key set by AST (`receipts/dict_key_audit.log`).

**Other semantic couplings checked.** None of the following changes any file this PR touches:

- **#559:** `.github/workflows/docs.yml` step, `ci_events.py` `CARRIER_STEP_LISTS`, `tb/verilator/README.md`.
- **#551:** `milan_dp/Makefile` `crflic_probes.vlt`, `KL_pp_shadow.sv`.

**PR-only paths carried unchanged.** These are byte-identical between `ddf8151c` and the candidate (`receipts/pr_only_paths_identity.log`), so the source reviews' runs on them carry over unchanged:

- the servo RTL and the whole `mmcm_servo` suite;
- `crf_rx`, `gptp_shadow`, `gptp_txts` and `mmcm_servo_autorepair`;
- `hdl/ieee8021as`;
- the design docs and gPTP guides;
- the diagrams and `SUBMODULES.md`;
- the gPTP gitlink and the ROM ledger.

## 3. Executed evidence on the candidate

Tools:

- **Verilator 5.050:** `--version` prints `Verilator 5.050 2026-07-01 rev v5.050`. `verilator_bin` sha256 is `44898b22...bfdd`.
- **Python:** a venv whose `cmarkgfm 2025.10.22`, `html5lib 1.1` and `cffi 2.1.1` match `tools/markdown/requirements.txt`.

Every command ran in the foreground, using at most 8 parallel jobs.

| Command | Result | Receipt |
|---|---|---|
| 45 static/documentation gates (`scripts/run_static_gates.sh`) | All exit 0 (see below) | `receipts/static/summary.tsv`, per-gate logs |
| `docs_check.py` with Git / on a Git-free `git archive` extraction | 0 findings (scrub 23/23) / 0 findings (only inventory parity skipped). `check_feature_status.py` no-Git: 0 findings | `static/docs_check.log`, `static/nogit_*.log` |
| `gen_toc.py --selftest`, `--verify-anchors`, `--check` | Pass. 179 cross-page anchors reproduced; TOC OK on 108 pages | `static/gen_toc_*.log` |
| `check_em_dash.py --base 0e26e0ac` / `--base 5c78ce2e` / `--selftest` | 0 findings over 165 added lines / 0 over 681 / 339/339 arms | `static/em_dash_*.log` |
| `ci_events.py --check` / `--selftest` | OK: 1655 items across 4 workflows and `CI_WORKFLOWS.md` / pass | `static/ci_events_*.log` |
| `measure_test_evidence.py --check` / `--selftest` | PASS: 0 unexplained DUT readers / pass | `static/test_evidence_*.log` |
| `lint_rtl.py --check`, `--pragmas` | PASS: 90 <= 90 | `static/lint_rtl_*.log` |
| `xvlog_gate.py --check` | PASS: 4 findings == ratchet; processors proved at gitlinks `990f9652` and `5dce647a` | `static/xvlog_gate_check.log` |
| Other gates, all exit 0 | `check_doc_style`, `check_gptp_docs`, `DOC_MAP`/`timesync_chain`/`submodule_boundaries` `--check`, `check_submodule_docs`, `check_diagram_pngs`, `gen_module_matrix --check`, `check_nvm_capture`, `check_rtl_source_lists`, `check_port_contracts`, the naming/fail-fast/TODO/hygiene/idiom ratchets, `check_doc_paths`, `check_archive`, `pp_srcs --check`, and the relevant `--selftest`s | `static/*.log` |
| `git diff --check` vs parent and vs dev | Exit 0 / exit 0 | `receipts/diff_check.log` |
| ROM ledger: independent regeneration at the gitlinks | `gptp_ucode.hex` at `5dce647a` = `c496ed8a...0371`, one ledger row. `ltn_rom.hex` and `ucode.hex` at `990f9652` match their single rows | `receipts/rom_digests.log` |
| ROM ledger: `syn/yosys/ooc.sh tcam` (validates all three images before pricing) | Exit 0 | `receipts/rom_digests.log` |
| `sv2v --top=milan_datapath` over `ooc.sh --emit-dp` with ooc's include flags | Exit 0, empty stderr. The netlist carries both `gptp_slew_tail_r` and `lwsrp_stream_gate` | `receipts/sv2v_milan_datapath.*` |
| Host `yosys` elaboration of that netlist: `read_verilog -sv; hierarchy -check; stat` | Exit 0 | `receipts/yosys_hierarchy.*` |
| `milan_dp` `gmstep-build` + leg (feed delay 0) | 58 checks, 0 failures, all 10 `slew path:` checks included | `dynamic/gmstep_build.log`, `dynamic/gmstep_leg.log` |
| gmstep campaign: anchor audit | 14/14 anchors exactly once | `dynamic/gmstep_anchors.log` |
| gmstep campaign: every entry of `gmstep_mutants.py --all`, run one per invocation | 16/16. Positive gmstep and option-off legs pass. All 14 controls are caught on their named checks, including the three #545 slew controls and the two talker-gate controls #551's gate sits beside | `dynamic/gmstep_campaign/*.log` |
| `crflic-build`; `Vmilan_dp_crflic` default and `--unwarmed-refusal` | 415/0 and 415/0 | `dynamic/crflic_*.log` |
| crflic campaign: anchor audit and `crflic_mutants.py` entries | 6/6 anchors. 7/7: the positive passes and all six raw-verdict/real-grant mutants are caught | `dynamic/crflic_anchors.log`, `dynamic/crflic_campaign/*.log` |
| `make gptp`, `make gptp-lat` (the other gPTP-on default legs, with both changes elaborated) | 181/181 and 181/181 | `dynamic/gptp_leg.log`, `dynamic/gptp_lat_leg.log` |
| Restore proof | EXACT. HEAD, tree and index tree are exact; 0 flagged index entries; 907 tracked entries match mode and blob, with worktree bytes hashed directly; gitlinks match and submodules are clean; 0 untracked or ignored entries | `receipts/verify_restore.log` |

Mutant runs note: `scripts/run_one_control.py` imports the repository's own campaign module and calls its own `build`, `run_control`/`run_mutant` and `verdict`. It only picks which entry runs, so no single foreground call outruns its limit. Planted copies and their builds were kept outside the clone.

## 4. The five questions in the brief

1. **`milan_datapath.sv`:** the #545 slew wiring and the #551 licence gate coexist without shared signals.
   - xvlog, lint, sv2v and Yosys elaboration pass.
   - The gmstep leg and the full `gmstep-mutants` inventory pass.
   - The `crf_licence` leg passes by default and with `--unwarmed-refusal`, and so does its campaign.
2. **`CI_WORKFLOWS.md`:** #559's pinned step section and #545's `mmcm_servo` row coexist, and `ci_events.py --check` and `--selftest` pass.
   - The row's hosted basis (`b94f53cc`) is still valid for this tree. The `mmcm_servo` directory and the servo RTL are byte-identical to the PR head.
3. **`TESTING.md`** at the candidate:
   - The gmstep row states 12 + 2 controls, and `CONTROLS` has 14 (12 gmstep, 2 option-off).
   - The slew row states 8 defects + 2 positives, and `slew_mutants.py` has 5 `MUTANTS` + 3 `STREAK_MUTANTS`. Its target `slew-mutants` exists (`mmcm_servo/Makefile:87`).
   - #559's harness exception is present, and `nvm_capture_cpu` has no Makefile, as the exception says.
   - The #551 licence row: see observation O1.
4. **Anchors:** `REGISTER_MAP.md` anchors pass `docs_check` in both modes and `gen_toc --verify-anchors`. `measure_test_evidence --check` passes.
5. **gPTP gitlink `5dce647a`:** its ROM digest record holds on the candidate, confirmed both by independent regeneration and by the repository gate.

## 5. Findings

No BLOCKER, MAJOR, MINOR or SUGGESTION finding against the composition.

## 6. Observations outside this verdict

These were not introduced by the composition, and they do not affect any lens here.

- **O1 (pre-existing in the train, not #545):**
  - `docs/testing/TESTING.md:270` still says "#530 streaming licence, the three gate mutants".
  - `crflic_mutants.py` `MUTATIONS` has six entries (#551 added three), and the `milan_dp` README describes six elaborations.
  - The row is byte-identical at parent `0e26e0ac`, and PR #563 does not touch it (`receipts/crflic_row_observation.log`).
  - Routing belongs to the #551 lane or the manager, not to this PR.
- **O2:** the brief's overlap list omits `scripts/measure_test_evidence.py`, which both sides edited (section 2). The merge is clean and the gate passes, so this is a bookkeeping note for the manager's final-candidate step.

## 7. Prior public findings on PR #563, resolved or retained at this head

I read these after my own pass. Every artifact named below is byte-identical between `ddf8151c` and `551e4b5d`, except `milan_dp/README.md`, which differs only by #551 hunks.

| Finding | Severity | Status at `551e4b5d` | Evidence |
|---|---|---|---|
| R300-1 F1 / R301-1 F1 (servo default over budget) | MAJOR | Resolved | `mmcm_servo` tree identical to `ddf8151c`, where the hosted `verilator-suites` passed; `slew-mutants` explicit (`Makefile:87`) |
| R300-1 F2 / R301-1 F2 (coincident step+slew dedupe untested) | MINOR | Resolved | `sim_main.cpp`, `sim_phc_step.cpp` and the servo identical to `ddf8151c`, where R300-4 ran 10/10 |
| R300-1 F3 (TESTING index stale) | MINOR | Resolved | `TESTING.md:272-273,494` match the inventories (section 4) |
| R301-1 F3 / R300-1 S1 (tail oracle copied RTL) | MINOR / SUGGESTION | Resolved | The "extra addend stage" control is caught at this head (`gmstep_campaign/control_2.log`) |
| R301-1 S1 (streak reset uncontracted) | SUGGESTION | Resolved | Servo, header and tests identical to `ddf8151c` |
| R300-2 F4 (U15 blind to counting variants) | MINOR | Resolved | As above |
| R300-2 F5 (1800 s basis) | MINOR | Resolved | `CI_WORKFLOWS.md:159` present and still valid (section 4) |
| R301-2 S-A (one-sided tail oracle) | SUGGESTION | Retained, open (routed to #495) | `sim_gmstep.cpp` identical |
| R301-2 S-B / S-C | SUGGESTION | Resolved | `CI_WORKFLOWS.md:159`; `TESTING.md:272` trigger list names `KL_gptp_shadow.sv` and the pin |
| R300-3 S1 (U15 level-gated sub-window reset) | SUGGESTION | Retained, open | Servo and `sim_main.cpp` identical |
| R300-3 S2 = R301-3 S1 (six classes for eight) | SUGGESTION | Resolved | `measure_test_evidence.py:597-602` |
| R301-3 F1 (README "all eleven") | MINOR | Resolved | `milan_dp/README.md:657` "all fourteen"; 14 controls planted here |
| R301-4 S1 (dated "eleven" records) | SUGGESTION | Retained, open | Now at README `:685` and `:929` (shifted by #551 text) |
| R300-4 S1 (README "48 of 48") | SUGGESTION | Retained, open | Now README `:634`; the leg reports 58 here |
| R300-4 S2 (`KL_media_nco.sv` cites `drp_servo.sv:604`) | SUGGESTION | Retained, open | `KL_media_nco.sv:43,147` unchanged |

No open MINOR, MAJOR or BLOCKER remains from any prior round.

## 8. Per-lens results

```text
[R301] PASS Conformance - milan_datapath.sv:1464,2766-2770,5570,6918,7010 and :6648-6649 at 551e4b5d; dynamic/gmstep_leg.log; dynamic/crflic_leg_*.log - the #545 acceptance behaviour (LOCKED-through-slew level reaches the servo from real Sync pairs, tail covered, tally) still passes on the composed tree (58/0, slew controls caught); the #551 licence it composes with still passes (415/0 twice); the merge carries both deltas line-for-line (lineage.txt)
[R301] PASS RTL - hdl/milan/milan_datapath.sv at 551e4b5d (slew hunks vs licence hunks) - no shared signal or declaration; xvlog 4==ratchet, lint 90<=90, port contracts and source lists OK; sv2v and yosys hierarchy -check on the composed netlist exit 0; gPTP-on elaborations (gmstep, gptp, gptp-lat) and gPTP-off licence elaboration build and pass on 5.050
[R301] PASS Robustness - dynamic/crflic_leg_unwarmed.log, dynamic/gmstep_campaign/positive_option_off.log, dynamic/gptp_*.log, milan_datapath.sv:7010 - refused/unwarmed licence path, the option-off leg (gPTP-absent tie-off branch) and the gPTP-on legs all pass with both changes elaborated; servo reset/saturation/boundary cases are byte-identical to ddf8151c
[R301] PASS Tests - gmstep_mutants.py CONTROLS (14/14 anchors, 16/16 run), crflic_mutants.py MUTATIONS (6/6 anchors, 7/7 run), measure_test_evidence.py:597-640 (28 keys, 0 duplicates; --check/--selftest pass) at 551e4b5d - both datapath campaigns still plant and are killed on the composed file; no test weakened
[R301] PASS Docs - CHANGELOG.md:11,33; CI_WORKFLOWS.md:158-159,1200; TESTING.md:165,272-273,380,494; REGISTER_MAP.md:839,938,2027; milan_dp/README.md:27,657,1083 at 551e4b5d - composed pages agree with the candidate's targets and inventories; docs_check (both modes), gen_toc selftest/check/verify-anchors, em-dash (parent and dev bases), doc style/paths/gPTP docs, diagram and matrix no-drift, ci_events all exit 0
```

## 9. Reviewer-owned completion ledger

This round's own scope is the composition. Lenses applied at the candidate head are recorded against it. Artifacts outside the composition's reach are byte-identical to `ddf8151c`, where R300-4 covered all five lenses. R301-4 at `4538d7c0` covered them at the ancestor, and the merge `ddf8151c` touched nothing in their scope except the two assigned files.

| Lens | CLEAN/UNCLEAN | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: `milan_datapath.sv` behaviour under #545 acceptance composed with #551 | lineage and delta equality; gmstep leg 58/0; crflic legs 415/0 x2 | R301-5 (composition); R300-4 for PR-only artifacts | `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`; `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| RTL | CLEAN | Yes: `milan_datapath.sv` | Composed datapath; xvlog, lint, sv2v, Yosys hierarchy; 4 elaborations | R301-5; R300-4 for servo RTL (identical) | `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`; `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Robustness | CLEAN (retained SUGGESTIONs R301-2 S-A, R300-3 S1 only) | Yes, marginally: the refusal and feature-off paths of the composed datapath | crflic unwarmed-refusal; option-off leg; gPTP-on legs | R301-5; R300-4 for servo cases (identical) | `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`; `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Tests | CLEAN | Yes: `measure_test_evidence.py`, both datapath campaigns | Anchor audits; gmstep 16/16; crflic 7/7; evidence ratchet | R301-5; R300-4 for `slew-mutants` and `crf_rx` (identical inputs) | `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`; `ddf8151c478fc54c98608589c1afe9525739d6a4` |
| Docs | CLEAN (retained SUGGESTIONs R301-4 S1, R300-4 S1, S2 only) | Yes: six composed pages | Pages and gates in section 3 | R301-5; R300-4 for PR-only pages (identical) | `551e4b5dfa8ac7ec68a3161c95d4000eb6337396`; `ddf8151c478fc54c98608589c1afe9525739d6a4` |

## 10. Limits

- **Verilator wrapper:** the assigned wrapper path did not exist on this host. I wrote equivalent wrappers that execute the same underlying Verilator 5.050 install, with its identity recorded above, and the same pinned-lock Python.
- **Yosys and sv2v:** these ran at host versions (Yosys 0.66, sv2v 0.0.13), not the CI pin. They were a front-end/elaboration probe only, not the `yosys-portability` gate. Only the `tcam` top was synthesised, and that was solely to exercise `ooc.sh`'s ROM validation.
- **Feed delay:** the gmstep leg ran at feed delay 0, which is what the sweep uses. It did not run at other delays.
- **Not run by me:**
  - the full `milan_dp` default sweep (the legs run were gmstep, crflic, gptp, gptp-lat, and option-off as the campaign positive);
  - `mmcm_servo` default and `slew-mutants`, `crf_rx`, `gptp_shadow` (inputs byte-identical to `ddf8151c`);
  - behave, builder, full Yosys/OOC area, parent/PP/gPTP banks, Docker/act.
- **Hosted state:** the candidate is not pushed, so no hosted run exists for `551e4b5d`. At `ddf8151c` the snapshot shows:
  - 20 contexts completed success;
  - `Physical gPTP (nightly and manual)` skipped, which is not hardware proof;
  - `docs-check-no-git` reporting in progress with a success conclusion.

  Receipt: `receipts/hosted_checkruns_ddf8151c.tsv`.
- **Manager evidence:** I found no public manager evidence comment for this candidate beyond the review-start notice.
- **Physical calibration:** NOT RUN. Neither simulation nor field skips are hardware evidence.
- **Host paths:** raw receipts contain absolute host paths of the review area. They contain no identity tokens.

## 11. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn. The source base is `0e26e0ac`; live dev is `5c78ce2e` or its successor.
- Include `scripts/measure_test_evidence.py` in the overlap inventory (O2).
- Accept the hosted and act evidence for the merged result, distinguishing executed jobs from skipped contexts.
- Confirm the CONTRIBUTING review bar: two independent positives, one external.
- Obtain explicit maintainer authorization before any merge. Then run post-merge containment and close #545.
- Optional: route O1 to the #551 owner, and the retained SUGGESTIONs.

R301-5 FINISHED
