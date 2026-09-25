[R306] NEGATIVE - exact head 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2

# R306-2 internal delta review: issue #508 / PR #560

- Head `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`, tree `2824fdf51740e86abc2ed3a07f438e4ea701fe9a`. Processor gitlink `990f96526bb89356c963a260ebbdcf2a77e6623a`.
- Delta reviewed: `6a9828c1..224ec0e9` (round-3 commit `224ec0e9a`, 6 files, `receipts/delta_scope.txt`). The full PR range `573f0052..224ec0e9` was re-scanned only for processor citations.
- Assignment: issue 508 comment 5825850226. Acceptance-2 decision: 5825732419.
- Every lens was applied at this head. The round-1 ledger (R306-1, `6a9828c1`) still stands for artifacts this delta did not touch.

## Reconstruction

I read, in this order:

1. `AGENTS.md` and `CONTRIBUTING.md`. The dev merge bar requires seven exact contexts, including `docs-check` and `docs-check-no-git` (`CONTRIBUTING.md:55-57`).
2. The issue #508 body and its frozen acceptance 1-6.
3. The manager comments 5819498419, 5822047670, 5824708827, 5825732419 and 5825850226.
4. At `990f9652`, the processor authorities:
   - `06_aecp_engine.md` F06.13 field lineage, with its coherence bound ("every such change is itself a notification trigger");
   - `05_acmp_engine.md` F05.5 settlement (`SETTLED_RSV_OK --> PRB_W_AVAIL: EVT_TK_UNREGISTERED, talker gone`);
   - `protocol_processor_top.sv:3065-3157` (`listener_gsi_status`, `gsi_owner_read`, `stri_events`);
   - `KL_srp_listener_fsm.sv:728-776,849-860`.
5. The delta diff and history.
6. The public author evidence at `192d6248` `review-evidence/508-r1/author-r3/`: `docs-no-git.log`, `docs-git.log`, `citations.log`, `duplicate-mutant-proof.log`.
7. The exact-head hosted checks.

I read the prior public findings (R306-1 5825848456, R307-1 5825730404) only after this round's verdict and ledger were drafted.

## Findings

### F1 - BLOCKER - Docs, Tests - `tb/verilator/milan_dp/README.md:488` - relative links into the processor submodule turn two required contexts red at this head

- **Authority/evidence.**
  - The round-3 commit added `[field lineage](../../../protocol-processor/docs/architecture/06_aecp_engine.md#fig-06-lineage)` and `[settlement states](../../../protocol-processor/docs/architecture/05_acmp_engine.md#fig-05-settled)`.
  - The docs gates run before any submodule checkout (`.github/workflows/docs.yml:12`). So both links are broken there.
  - Hosted `docs-check` and `docs-check-no-git` both fail at `224ec0e9` with exactly these two findings (`receipts/hosted_docs_check_failed.log`, run 36090501347).
  - Both contexts are required by the dev merge ruleset (`CONTRIBUTING.md:55-57`).
  - I reproduced the failure offline. `git archive 224ec0e9a` gives a tree without the submodule, and `docs_check.py` returns rc 1 with the same 2 findings (`receipts/docs_check_nosubmodule_repro.txt`).
  - The same procedure at the previous head `6a9828c1` gives 0 findings, rc 0 (`receipts/docs_check_nosubmodule_prev_6a9828c1.txt`). The round-3 commit introduced the failure.
  - It is the only relative Markdown link from the parent into a submodule. The repository's convention is a commit-pinned GitHub blob URL, as at the same README's `:728` and `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:175`.
  - The author's local `docs-no-git.log` reports 0 findings because it walked a tree with the submodule checked out (871 files against the hosted 861). That shape does not match the hosted gate. My own local `docs_check.py` in this clone also passes, for the same reason (`receipts/docs_check_local.txt`).
- **Lenses.**
  - Docs: a broken reference in an authoritative document.
  - Tests: an existing required gate is no longer green.
- **Impact.** The merge bar cannot be met. The PR's local "docs set passed" evidence does not predict the hosted verdict.
- **Required outcome.** `README.md:488` no longer links a path the hosted docs gates cannot resolve. Both hosted `docs-check` and `docs-check-no-git` are green at the new exact head.
- **Verification.**
  - Run `docs_check.py` in a `git archive` of the new head, which has no submodule content: 0 findings.
  - Both hosted contexts pass at the new head.

### F2 - MINOR - Docs - `CHANGELOG.md:57`, `tb/verilator/milan_dp/Makefile:451-452`, `scripts/measure_test_evidence.py:620` - the gsi-mutants campaign is still described as seven arms after the eighth was added

- **Authority/evidence.**
  - `gsi_mutants.py` now holds 8 `MUTATIONS` entries; `6a9828c1` held 7 (`receipts/stale_mutant_counts.txt`).
  - The README was updated: "eight mutant elaborations and nine runs" at `README.md:517`.
  - Three other statements of the same campaign were not updated:
    - `CHANGELOG.md:57`: "`make gsi-mutants` holds its seven failing arms".
    - `Makefile:451-452`: "seven more elaborations and eight runs". This contradicts the README at the same head.
    - `measure_test_evidence.py:620`: the census disposition says the campaign "plants one of seven #508 GET_STREAM_INFO seam defects".
  - `docs/testing/TESTING.md:267` ("the seven field mutants") is still literally true, since the eighth is a push-count mutant. It becomes misleading only if read as the campaign size.
- **Impact.** The release record, the campaign's own recipe comment and the test-evidence census misstate what `make gsi-mutants` runs.
- **Required outcome.** Every statement of the campaign's size agrees with `MUTATIONS` (8 arms, eight elaborations, nine runs).
- **Verification.**
  - `grep -n "seven" CHANGELOG.md tb/verilator/milan_dp/Makefile scripts/measure_test_evidence.py` finds no stale gsi-mutants count.
  - `measure_test_evidence.py --check` and `docs_check.py` stay green.

### Suggestions (optional; they do not affect coverage)

- **S1 (Robustness, Tests)** - `tb/verilator/milan_dp/sim_nxn.cpp:2175-2200`.
  - The exact counts come from `gsi_ck_pushes` before the solicited read. The per-push loop runs after it, and a push beyond two is only labelled "unexpected extra push" and content-graded. No check fails on its existence.
  - So a push that lands during the solicited read is content-graded but not counted, and G9's `notify_clear()` then discards it.
  - The duplicate mutant lands inside the window and is caught. The gap is only the few cycles of the read.
  - Asserting `seen == 2` per controller after the loop would close it.
- **S2 (Tests)** - parent coverage of the processor's bridge gate (`protocol_processor_top.sv:3109`).
  - Reviewer probe P3 removes the "registered FAILED" gate on the bridge id and passes all 380 checks (`receipts/probe_P3.log`).
  - The reason is that G8's settlement teardown (A8) also zeroes the raw latch (`KL_srp_listener_fsm.sv:760-774`). No `[GSI]` step replaces a Talker Failed with a Talker Advertise, the case where only that gate clears the stale bridge.
  - The processor's own campaign kills the same mutant (`protocol-processor/tb/pp_top/gsi_mutants.py:87-90`, "bridge-gate-removed"), and parent acceptance 5 does not name it. So this is not a finding against this PR.
  - A Failed-to-Advertise replacement step would give the parent leg that coverage.
- **Carried from round 1, untouched by this delta:** R306-1 S1 (= R307-1 S2, the misplaced restore-walk doc block in `sim_tdm8_render.cpp:1419-1426`), S2 and S3 are unchanged and remain optional.

### Observation outside this PR's scope

Pre-existing processor line citations are stale at the pin, and the PR did not touch them:

- `sw/litex/milan_soc.py:2123,2124,2180`;
- `sw/litex/test_pp_mem_bridge.py:13,400,412`;
- `sw/litex/test_pp_boot_bus_freeze.py:602`;
- `tb/verilator/milan_dp/sim_main.cpp:2297`.

Each was already wrong at dev's `09f9bf38` (`receipts/cite_drift_head.txt`, old-pin text shown), and each line predates the source base `573f0052`. Per `AGENTS.md` section 4 this is new work for a separate issue, not a defect of this lane.

## Round-1 findings: resolution at this head

- **R306-1 F1 = R307-1 F1 (CHANGELOG #116/#113 in the `09f9bf38` section): CLOSED.**
  - "Unreleased - licence and LeaveAll scope" is byte-identical to dev `c266432d` (sha256 `f546c55a...`), and so are the two neighbouring sections.
  - `Processor issue 116` and `Processor issue 113` each occur once, at `CHANGELOG.md:51` and `:53`, inside the `990f9652` section (lines 31-59).
  - The whole-file diff against `c266432d` is the new section plus its TOC line only.
  - Receipt: `receipts/changelog_sections.txt`.
- **R306-1 F2 (stale processor line citations): CLOSED.**
  - `cite_resolve.py` lists every processor `file:line` citation on lines the PR adds (`573f0052..224ec0e9`) and prints the cited lines at `990f9652` (`receipts/cite_resolve_pr.txt`). There are 4 citations, and I read the two continuation citations by hand.
  - Each resolves to the construct it names:
    - `KL_srp_top.sv:211` is `tk_reg_state_o`, cited at `milan_datapath.sv:6683` and `pp_shadow/sim_main.cpp:2849`.
    - `KL_srp_listener_fsm.sv:851-853` is `status_map`'s `tk_reg_state_o` driver.
    - `KL_srp_top.sv:451` is `assign sr_adm_fsm_w`.
    - `KL_srp_top.sv:787-798` is the `opt_r` aging block.
    - `KL_srp_top.sv:873-876` is the `opt_r`/`opt_cnt_r` reload.
    - `KL_srp_admission.sv:187-190` is `cand_w`/`fit_w`/`refuse_w`.
    - `KL_srp_admission.sv:261-266` is `publish` (`sr_admitted_o`).
    - `KL_srp_talker_fsm.sv:705-710` is the gate re-open clearing `reg_r`/`lstn_val_r`. That file is unchanged across the pin.
  - `cite_drift.py` compares every processor citation in the parent between `09f9bf38` and `990f9652`. It reports no citation in the PR's touched set that is still wrong. The drifts it lists are either the PR's own updated citations or the pre-existing ones in the observation above.
- **R306-1 F3 (G8 pushes ungraded, "exactly one" false): CLOSED.**
  - `sim_nxn.cpp:2175` grades the exact count, 2 to A and 2 to B.
  - `:2182-2200` grades every G8 push to each controller: SUCCESS at cdl 68, PASSIVE, `acmp_status` 0, all four failure fields cleared, and a body equal to the solicited answer.
  - `:2201` grades sink 1 quiet.
  - The README row `:477` and text `:481-490`, and the banner `sim_nxn.cpp:1663-1671`, state the count and name both changes.
  - Each push is tied to its trigger by executable evidence, not only by order (`receipts/g8_probes.txt`):
    - P1 removes `srp_evt_tk_unreg_w` from `stri_events`. G8 gets 1 push, and the exact-count checks to A and B fail (2 of 364).
    - P4 suppresses only the post-withdrawal `lstn_gsi_changed_r` strobe on sink 0. G8 gets 1 push, and the same two checks fail.
    - The P1 and P4 logs are byte-identical. That is expected: the surviving push reads the same live PASSIVE state either way, and the harness prints no trigger identity. P2's trace is what separates the two triggers.
    - P2 (trace only, 380/380 PASS) shows `srp_evt_tk_unreg` at cycle 5387751, then `lstn_gsi_changed status=20` (pbsta 1 PASSIVE, acmpsta 0) at 5387777, each raising `ntfy_stri_in`.
  - The first push already reads PASSIVE, which matches F06.13's live reads.
  - The duplicate-withdrawal mutant fails the named check `[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to A` (2 of 396, and B also fails).
- **R306-1 F4 = R307-1 F2 (acceptance 2 wording): CLOSED by decision 5825732419.**
  - The decision reads acceptance 2 as ACTIVE with `acmp_status` 0 on bind, then PASSIVE after an unanswered retry.
  - G1 grades exactly that at `sim_nxn.cpp:2040-2043` (`kPbActive`, 0). G3 grades it at `:2090-2091` and `:2095-2096` (`kPbPassive`, 0).
  - Both pass in the clean leg (`receipts/notify_clean.log`).
- **R307-1 S1 (pin G8's count): addressed by the same change as my F3.**
- **R307-1 S2: carried as an optional suggestion (see above).**

## Per-lens coverage lines

[R306] PASS Conformance - `tb/verilator/milan_dp/sim_nxn.cpp:2040-2096,2162-2208` and decision 5825732419 at 224ec0e9 - G1/G3 grade the decided acceptance-2 reading. G8's two pushes are the two owner changes that F06.13 and F05.5 at `990f9652` define as separate triggers (`protocol_processor_top.sv:3141-3157`). Each announces the committed current state, so neither is a fabricated transition. Solicited and unsolicited bodies are equal for both pushes, and sink 1 stays silent (acceptance 3/4).

[R306] PASS RTL - `receipts/delta_scope.txt` (`hdl/milan/milan_datapath.sv:6603-6604,6683-6685`) at 224ec0e9 - the delta changes only comment lines in `hdl/` and `pp_shadow`. Every changed processor citation resolves at `990f9652`. The duplicate mutant's RTL (a 13-bit replay counter set to 4096, and an OR term into `stri_events`) is confined to a processor copy and matches its anchors exactly once.

[R306] PASS Robustness - `tb/verilator/milan_dp/sim_nxn.cpp:2172-2208` and probes P1/P4 at 224ec0e9 - both a missing push (P1, P4) and an extra push (the duplicate mutant) fail named G8 checks for both controllers. The per-push loop does no simulation tick while it holds references into `uns_log`, so there is no #542 reallocation hazard. G10 reset and G6 unchanged-refresh silence still pass. The residual solicited-read window is S1 (SUGGESTION).

Tests: UNCLEAN at 224ec0e9 under F1 (the required hosted `docs-check`/`docs-check-no-git` gates fail). The graded content is clean on its own evidence:
- `make -C tb/verilator/milan_dp notify`: 380/380, `RESULT: PASS`.
- `gsi_mutants.py`: 9/9, with all 8 mutants caught at the README's failure counts (7, 7, 7, 7, 21, 42 and 14 of 380; 2 of 396).
- Probes P1, P2 and P4 behave as expected. P3 survives, and that is attributed in S2.

Docs: UNCLEAN at 224ec0e9 under F1 and F2. The round-1 items F1/F2/F3 are closed, and the README/banner G8 text is accurate against the P2 trace and the hosted run.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #508 acceptance 2-4; decision 5825732419; `[GSI]` G1/G3/G8; processor F06.13, F05.5, `stri_events` at `990f9652` | R306-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| RTL | CLEAN | `milan_datapath.sv` delta (comment-only); processor citations at `990f9652`; `gsi_mutants.py` duplicate-withdrawal RTL | R306-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Robustness | CLEAN | G8 count and per-push loop; probes P1/P4; duplicate mutant; G6/G10 re-run | R306-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Tests | UNCLEAN (F1) | `obj_notify` leg 380/380; `gsi_mutants.py` 8/8; probes P1-P4; hosted `docs-check`/`docs-check-no-git` red | R306-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Docs | UNCLEAN (F1, F2) | `milan_dp/README.md` G8 text and link `:488`; `sim_nxn.cpp` banner; CHANGELOG sections vs `c266432d`; Makefile, `measure_test_evidence.py` and TESTING.md campaign statements; citation resolution | R306-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |

For artifacts this delta did not touch, the R306-1 results at `6a9828c1` carry forward. That covers the `KL_pp_shadow.sv` seam, `nvm_cosim`, the restore-walk harnesses, SUBMODULES, the diagram and REGISTER_MAP. `6a9828c1` is the parent of this head, and nothing in those artifacts changed since.

## Real limits

- **Not run.** I did not run the full parent, processor, gPTP, Yosys or builder banks, the `milan_dp` default sweep, `pp_shadow`, Docker/act, `act_ci` or its selftest, hardware, or physical calibration.
  - The delta's `pp_shadow` change is one comment line, so a rebuild would test nothing new.
  - The manager's source banks and the hosted contexts are the evidence for everything above.
- **Hosted snapshot** (`receipts/hosted_checks_snapshot.txt`, 2026-09-25T03:43:52Z):
  - `docs-check` and `docs-check-no-git` fail.
  - `Verilator shard 1/5` and `4/5` were still pending.
  - `Physical gPTP` was skipped. A skipped context is not hardware proof.
  - All other listed contexts passed.
- **Tools and jobs.** Verilator 5.050 (`rev v5.050`) came from the scoped wrapper, first on PATH, with `VERILATOR_JOBS=8`. Every run was sequential and in the foreground, and temporary trees lived under the packet's `scratch/`.
- **Probe driver exit code.** `g8_probes.py` exits 1 because P3 was exploratory and survived. That survival is the S2 evidence, not a harness failure.
- **Clause text.** The Milan clause reading rests on the processor architecture pages at `990f9652`. The standard's own text was not in this clone.
- **Redaction.** Host path prefixes in receipts are replaced with `<clone>`, `<packet>`, `<tool>` and `<VERILATOR_PREFIX>`.
- **Clone restored** (`receipts/restore_verification.txt`):
  - HEAD, index tree and expected tree are all `2824fdf5...`;
  - worktree and index diffs are empty, and there are 0 status entries, ignored files included;
  - all 885 tracked blobs re-hash and have the right modes;
  - the gitlinks are `efeb541a`, `e5dcea6e`, `990f9652` and `48ff7a7e`, and all three required submodules are clean.

## Pending manager duties

- Route F1 and F2 to the executor. F1 is merge-blocking. The two hosted docs contexts must be green at the fixed exact head.
- After the fix, re-cover:
  - Docs;
  - Tests, since the hosted docs gates must be green;
  - Conformance and Robustness, if `sim_nxn.cpp` or the processor pin changes.

  RTL stays covered unless the fix touches `hdl/`.
- Confirm the pending `Verilator shard 1/5` and `4/5` results at the new exact head.
- Build and validate the final current-dev candidate at the merge turn: source base `573f0052`, live dev `0755923d983218ca6ca9db6891a558cbe6425b8d`. Own hosted and act acceptance.
- Optionally open an issue for the out-of-scope stale citations in the observation above.

R306-2 FINISHED
