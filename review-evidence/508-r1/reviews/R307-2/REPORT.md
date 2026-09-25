[R307] NEGATIVE - exact head 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2

# R307-2 external review: issue #508 / PR #560 (delta, round 3)

- Head `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`, tree `2824fdf51740e86abc2ed3a07f438e4ea701fe9a`. Both were verified in the review clone before and after every probe.
- Source base `573f0052a0e4412e81f0845438fcec2086ce5d55`. Round-2 head `6a9828c172aa4d5d8ee49725e357a10bae2caa52`. Processor gitlink `990f96526bb89356c963a260ebbdcf2a77e6623a`, unchanged since round 2.
- Role: external independent reviewer, cleared context. This is a delta round on assignment 5825850226, and all five lenses were applied at this head.
- **The verdict is NEGATIVE because two findings are open.**
  - F1 (MAJOR; Docs, Tests): round 3 added two Markdown links into the processor submodule. The required `docs-check` and `docs-check-no-git` contexts fail on them at this exact head. The failure reproduces locally in any tree without the submodule checked out.
  - F2 (MINOR; Docs): the eighth mutant was added, but three repository documents and one Makefile comment still say the campaign has seven.
- **All three round-3 assignment items are closed**: the CHANGELOG, the citations and G8. The acceptance-2 decision matches G1/G3. No RTL change is required.

## Reconstruction

Sources read, in this order:

1. `AGENTS.md` and `CONTRIBUTING.md`, including the seven required contexts at `CONTRIBUTING.md:56-57`.
2. `docs/README.md`.
3. Issue #508's body and frozen acceptance 1-6, then its comments:
   - the assignments (5819498419, 5824708827, 5825850226);
   - the decisions (5822047670, and 5825732419 on acceptance 2);
   - the REVIEW READY comments (5822002238, 5825445388, 5826185808).
4. The PR #560 body. The PR is open, not draft, based on `dev`, with head `224ec0e9`.
5. The processor authorities at the pin:
   - `hdl/top/protocol_processor_top.sv:3060-3150` (`listener_gsi_status`, `gsi_owner_read`, `gsi_answer`, `stri_events`);
   - `docs/architecture/05_acmp_engine.md` F05.5 (`:316-325`);
   - `docs/architecture/06_aecp_engine.md` F06.13 (`:295`);
   - `hdl/srp/KL_srp_top.sv`, `KL_srp_listener_fsm.sv`, `KL_srp_admission.sv` and `KL_srp_talker_fsm.sv`.
6. The round-3 delta `6a9828c1..224ec0e9`: six files, one commit, a one-line message with no body. I also read the lane-wide diff `573f0052..224ec0e9` for the citation inventory.
7. The public evidence at `192d6248/review-evidence/508-r1/author-r3`: `gates.jsonl` (19 final-head rows, all rc 0), `completion-check.json`, `citations.log` and `duplicate-mutant-proof.log`. I also read the hosted check runs at the exact head.

I read the prior public review findings (R306-1 and R307-1) only after my own pass over the delta. They are resolved below. I read no private author material, no lane scratchpad and no concurrent round-2 report.

## Findings

### F1 - MAJOR - lenses: Docs, Tests

**Location:** `tb/verilator/milan_dp/README.md:488`. The line was added in round 3:
`See [field lineage](../../../protocol-processor/docs/architecture/06_aecp_engine.md#fig-06-lineage) and [settlement states](../../../protocol-processor/docs/architecture/05_acmp_engine.md#fig-05-settled).`

**Title:** relative links into the processor submodule break the required docs gates.

**Authority/evidence:**
- `CONTRIBUTING.md:56-57` names `docs-check` and `docs-check-no-git` as required status contexts.
- `.github/workflows/docs.yml:12` says: "The documentation-only gates run before any submodule checkout."
- At this exact head, both hosted contexts completed with `failure` (`receipts/receipt_hosted_checks_snapshot.tsv`). Each failed on exactly these two links (`receipts/hosted_docs_check_failed.log`):
  `tb/verilator/milan_dp/README.md:488: broken link -> ../../../protocol-processor/docs/architecture/05_acmp_engine.md` (and the same for `06_aecp_engine.md`). The gate reports 2 findings in each mode.
- Local reproduction (`receipts/receipt_docs_check_submodule_absent.txt`):
  - In the review clone, with the submodule populated, `docs_check.py` returns rc 0.
  - In a `git archive` tree of the exact head, where `protocol-processor/` is empty, it returns rc 1 with the same two findings. This holds both without git (the `docs-check-no-git` shape) and with a fresh git index (the `docs-check` shape).
- This is the only Markdown link in the tracked tree, outside the submodules, that points into a submodule path (`git grep` over `*.md`).
- The published author rows `docs-git` and `docs-no-git` ran with the submodule checked out. That is why they report rc 0.

**Impact:**
- Two required contexts are red at the merge candidate, so the PR cannot satisfy CONTRIBUTING's merge bar at this head.
- On the hosted web view, a relative link into a gitlinked submodule path does not resolve. A reader following the G8 rationale gets a dead link.
- The "existing regressions remain green" property of the Tests lens does not hold at this head.

**Required outcome:**
- The README reference to the processor's F06.13 and F05.5 resolves without a submodule checkout. Any form the docs gate accepts will do, for example a code-span path or a link pinned to the adopted revision.
- `docs-check` and `docs-check-no-git` are green at the new exact head.

**Verification:**
- `python3 scripts/docs_check.py` returns rc 0 in a `git archive` tree of the new head with an empty `protocol-processor/`, both with and without a git index. `receipts/receipt_docs_check_submodule_absent.txt` records the commands.
- The hosted `docs-check` and `docs-check-no-git` both show `success` at the new head SHA.

### F2 - MINOR - lenses: Docs

**Title:** the gsi-mutants campaign is still described as seven arms after round 3 added the eighth.

**Location:**
- `CHANGELOG.md:57`: "`make gsi-mutants` holds its seven failing arms."
- `docs/testing/TESTING.md:267`: "#508 GET_STREAM_INFO seam, the seven field mutants".
- `scripts/measure_test_evidence.py:619-620`: the disposition "plants one of seven #508 GET_STREAM_INFO seam defects".
- `tb/verilator/milan_dp/Makefile:451-452`: "seven more elaborations and eight runs of the timed leg".

**Authority/evidence:**
- `gsi_mutants.py` `MUTATIONS` has 8 entries at this head. The eighth is the duplicated-withdrawal mutant this round added.
- The same round's README (`:496-517`) correctly says "eight mutant elaborations and nine runs".
- My run: `make gsi-mutants` reports 9 checks, 9 PASS (the clean control plus eight caught) (`receipts/receipt_notify_gsi_mutants.log`).
- AGENTS.md section 6, Docs lens: changed contracts must be reflected in the authoritative docs. The CHANGELOG and the TESTING.md campaign table are authoritative records of what the campaign holds.

**Impact:**
- The product changelog and the testing authority misstate the size of the campaign that a reviewer of the STREAM_INPUT gather must run (TESTING.md:267 names that audience).
- The test-evidence disposition misdescribes the driver it justifies.
- No gate compares these counts, so the inconsistency persists silently.

**Required outcome:** each location states the campaign's current content: eight arms, or seven field mutants plus the G8 push-count mutant, as the author prefers. The Makefile comment states eight elaborations and nine runs.

**Verification:**
- `grep -n -i 'seven' CHANGELOG.md docs/testing/TESTING.md scripts/measure_test_evidence.py tb/verilator/milan_dp/Makefile` shows no statement about the gsi-mutants campaign.
- `measure_test_evidence.py --check` and `--selftest`, `docs_check.py`, `check_em_dash.py --base c266432d` and `gen_toc.py --check` stay rc 0.

### S1 - SUGGESTION - lenses: Tests

**Location:** `tb/verilator/milan_dp/sim_nxn.cpp:2182-2199`.

The G8 loop names pushes by their order ("registrar withdrawal", "settlement teardown"), not by their cause. Probe P1 removed `srp_evt_tk_unreg_w` from a processor copy's `stri_events`. The one push left, which is the teardown push, is then graded under the label "registrar withdrawal" (`receipts/probe_P1_no_unreg_term.log`).

The exact-count checks catch that mutant and the opposite one (P2), so this is not a coverage gap. Grading each push's `uns_log_when` stamp against the withdrawal ingress, with a bound on their separation, would make the attribution executable rather than ordinal.

### S2 - SUGGESTION - lenses: Docs

**Location:** `tb/verilator/milan_dp/README.md:849`.

The `obj_notify` row reads **345 / 0** under the column "#508 round 1 (measured; date noted)". It is labelled as a dated round-1 measurement, so it is not false. The clean leg is now 380/0 (`README.md:499`), and a note on the row would spare readers the apparent contradiction.

## Round-3 assignment items, verified

| Item | Result | Evidence |
|---|---|---|
| CHANGELOG #530 / `09f9bf38` section byte-identical to dev `c266432d`; #116/#113 only in the 990f9652 section | **closed** | `receipts/changelog_sections.txt`: every dev section is IDENTICAL at head, including "Unreleased - licence and LeaveAll scope". The only differences are the new "processor pin 990f9652" section and its Contents line. "Processor issue 116" and "Processor issue 113" each occur once, in the 990f9652 section only. |
| Every processor line citation the PR touched resolves at `990f9652` to the construct it names | **closed** | `receipts/cite_inventory.txt` and `receipts/receipt_citations.txt`. The lane-wide inventory holds nine spans: `KL_srp_top.sv` 451 (`sr_adm_fsm_w`), 787-798 (opt_r aging), 873-876 (window reload, same span as dev's 855-858), 211 (`tk_reg_state_o`, twice); `KL_srp_listener_fsm.sv` 851-853 (`status_map` driver); `KL_srp_admission.sv` 187-190 (`refuse_w`) and 261-266 (`publish`, `sr_admitted_o`); `KL_srp_talker_fsm.sv` 705-710 (gate re-open clears `lstn_val_r`; the file is unchanged `09f9bf38..990f9652`). `cite_shift_proof.py` shows that each re-aimed span at 990f9652 holds exactly the text the round-2 citation named at `a8f8ce81`. The public `cite_drift.py`, run unchanged (sha256 `364b9446...`), flags only the three re-aimed single-line citations. That is expected: it compares the same line number across revisions, and those citations moved deliberately. It does not parse the wrapped `KL_srp_top.sv:` span, which I read by hand. Its other flags (`AGENTS.md:352`, `scripts/hygiene.budget:26`, `sw/litex/milan_soc.py:2123`) are in files this PR does not touch. |
| G8 grades the exact push count per registered controller | **closed** | `sim_nxn.cpp:2175` `gsi_ck_pushes(..., 0, 2)` checks `== 2` to A and to B, plus sink 1 quiet (`:2201`). |
| Each of the two pushes tied to its named change, with content graded | **closed** (S1 optional) | `sim_nxn.cpp:2182-2199` grades both ordered pushes to each controller: PASSIVE, `acmp_status` 0, both failure flags clear, code 0, bridge 0, and the body equal to the solicited answer. 32 checks, all ok (`receipts/receipt_notify_gsi_mutants.log`). My probes confirm the stated causes (`receipts/receipt_g8_probes.txt`). P1 removes `srp_evt_tk_unreg_w` from `stri_events`: G8 sees 1 push per controller, and only the two G8 count checks fail (2 of 364). P2 removes `lstn_gsi_changed_r`: G8 sees 1 push per controller. The remaining withdrawal push is already PASSIVE with cleared failure fields. That confirms the README's claim that the first push "already sees teardown" (the selector-7 status is read from `lstn_gsi_status_r` at gather time, `protocol_processor_top.sv:3063-3079,3106-3115`). |
| README and banner state the count | **closed** | `README.md:477,480-490` and `sim_nxn.cpp:1663-1672` state two pushes and name both causes. The named processor signals exist at the pin (`protocol_processor_top.sv:2210,3065,3148-3149`), as do the anchors `fig-06-lineage` and `fig-05-settled`. The *links* to those anchors are F1. |
| Duplicated-withdrawal mutant fails a named G8 check | **closed** | Reproduced: `[PASS] mutant caught: the processor duplicates the withdrawal push after 4096 cycles - breaks "[GSI] G8 sink 0 withdrawn: unsolicited GET_STREAM_INFO(sink 0) to A" (2 failure(s) across 396 checks)`. The 16 extra checks are the two extra pushes' content grades. The mutant edits only a temporary processor copy through the suite's own recipe. |
| Acceptance 2 decision (5825732419) matches G1/G3 | **matches** | G1 sink 0 bound: `probing_status` 2 (ACTIVE), `acmp_status` 0. G2: ACTIVE with 7. G3 sinks 0 and 1 after the unanswered retry: `probing_status` 1 (PASSIVE), `acmp_status` 0. G4: DISABLED after unbind, and COMPLETED with 0 after settle (`receipts/receipt_notify_gsi_mutants.log:606-692`). |

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence |
|---|---|---|
| R307-1 F1 = R306-1 F1 (MINOR, Docs, CHANGELOG #530 section) | **RESOLVED** | Section byte-identical to `c266432d`; #116/#113 once each. |
| R307-1 F2 = R306-1 F4 (MINOR, Conformance, acceptance 2) | **RESOLVED** by decision 5825732419 | G1/G3 grade exactly the decided reading; no source change needed. |
| R306-1 F2 (MINOR, Docs, stale processor line citations) | **RESOLVED** | Nine-span inventory and shift proof above. |
| R306-1 F3 = R307-1 S1 (MINOR/SUGGESTION, Tests/Docs/Conformance, G8 count) | **RESOLVED** | Exact count, per-push content, sink 1 quiet, README and banner, a named-check mutant, and my P1/P2 attribution probes. The residual ordinal labelling is S1 here, a SUGGESTION. |
| R307-1 S2 = R306-1 S1 (SUGGESTION, `sim_tdm8_render.cpp:1419-1427` banner placement) | **RETAINED** (SUGGESTION) | Not touched this round. |
| R306-1 S2 and S3 (SUGGESTION) | **RETAINED** (SUGGESTION) | Not touched this round. |
| Round-1 author-declared docs-check BLOCKER (5822002238, decided 5822047670) | **RESOLVED** (unchanged since round 2) | The author's final-head rows `port-contracts`, `naming` and `test-evidence` are all rc 0. F1 is a different docs-check failure. |

## Per-lens coverage lines

```text
[R307] PASS Conformance - issue #508 acceptance 2 (decision 5825732419) and 4 against sim_nxn.cpp:2033-2098 (G1-G3), :2162-2208 (G8) at 224ec0e9 - G1 ACTIVE/0 on bind, G3 PASSIVE/0 after unanswered retry, G2 ACTIVE/7, G4 DISABLED/COMPLETED; G8 two pushes per controller, each tied to a real processor event (P1/P2), no fabricated extra push (duplicate mutant caught); acmp_status 0 outside ACTIVE; round-1 ledger stands for acceptance 1, 3, 5, 6
[R307] PASS RTL - hdl/milan/milan_datapath.sv:6600-6605,6680-6686 at 224ec0e9, receipts/receipt_delta_scope.txt - the only HDL delta since 6a9828c1 is comment text (0 non-comment lines); gitlinks unchanged; the re-aimed citations name sr_adm_fsm_w, opt_r aging/reload, tk_reg_state_o and status_map exactly at 990f9652; round-1 RTL ledger stands
[R307] PASS Robustness - sim_nxn.cpp:2172-2207 and gsi_mutants.py:77-95,124-128 (receipt line 826) at 224ec0e9 - G8 now bounds the push count above and below per controller and keeps sink 1 quiet; delayed duplicate (13-bit counter, fires 4096 cycles after the event, inside the 10000-cycle window, reset-cleared) is caught; single-cause removals (P1, P2) are caught; round-1 robustness ledger stands
[R307] UNCLEAN Tests - F1 - required docs-check / docs-check-no-git regression red at 224ec0e9 (hosted and reproduced). Otherwise checked: obj_notify 380/0, gsi-mutants 9/9 with the eighth arm failing its named G8 check, P1/P2 each caught by the named G8 counts
[R307] UNCLEAN Docs - F1 (tb/verilator/milan_dp/README.md:488), F2 (CHANGELOG.md:57, TESTING.md:267, measure_test_evidence.py:619-620, Makefile:451-452). Otherwise checked: CHANGELOG sections, README G8 text and mutant table (counts 7/7/7/7/21/42/14 of 380 and 2 of 396 match my run), banner, citation comments
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #508 acceptance 2 decision 5825732419 against G1-G4; acceptance 4 against G8 and probes P1/P2; processor F05.5/F06.13 and `stri_events` at 990f9652 | R307-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| RTL | CLEAN | `milan_datapath.sv` delta (comments only, `receipt_delta_scope.txt`); gitlinks; the cited processor constructs at 990f9652 | R307-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Robustness | CLEAN | G8 exact bounds and sink isolation; the duplicate-mutant timing; P1/P2 single-cause removals | R307-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Tests | UNCLEAN (F1) | `obj_notify` 380/0; `gsi-mutants` 9/9; P1/P2; the hosted and local docs gates | R307-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |
| Docs | UNCLEAN (F1, F2) | CHANGELOG section proof; milan_dp README :474-517 and :849; `sim_nxn.cpp` banner; TESTING.md :267; `measure_test_evidence.py` dispositions; Makefile campaign comment; citation comments; `docs_check.py` with and without the submodule | R307-2 | `224ec0e9a9fa129924bf8f0433cf70b4140f7bd2` |

The RTL, Robustness and Conformance scopes are clean at this head. They stay covered only if the F1/F2 fixes leave them untouched: a README, CHANGELOG, TESTING, disposition-string or Makefile-comment edit does not touch them. Tests and Docs need a re-review at the fix head.

## Commands run (foreground, at most 8 jobs)

- Simulator identity: the scoped wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`. The host default (5.052) was not used.
- `VERILATOR=<tool-bin>/verilator VERILATOR_JOBS=8 make -C tb/verilator/milan_dp notify gsi-mutants`: rc 0; `checks: 380 failures: 0`; `9 checks: 9 PASS, 0 FAIL`; 4 min 26 s (`receipts/receipt_notify_gsi_mutants.log`).
- `python3 scripts/g8_probes.py <clone> <scratch>/probes`: this reuses the suite's own `gsi_mutants.plant/build/run_leg/verdict`. P1 is caught with 2 failures (both G8 counts). P2 is caught with 35 failures, including both G8 counts (`receipts/receipt_g8_probes.txt`, `receipts/probe_P*.log`).
- `python3 scripts/changelog_sections.py <clone> c266432d 224ec0e9`, `scripts/cite_inventory.py <clone> 573f0052 224ec0e9`, `scripts/cite_shift_proof.py <clone>`, and the public `cite_drift.py` run unchanged with old revisions `a8f8ce81` and `09f9bf38`.
- `python3 scripts/docs_check.py`: in the clone (rc 0), and in a `git archive` tree of the head without submodule contents, with and without git (rc 1 both) (`receipts/receipt_docs_check_submodule_absent.txt`).
- Hosted check runs at the exact head, read only (`receipts/receipt_hosted_checks_snapshot.tsv`, 03:41 UTC), and the failed job log (`receipts/hosted_docs_check_failed.log`).
- `scripts/verify_clone.sh <clone>` (`receipts/receipt_clone_integrity.txt`).

## Real limits

- **Not run by this reviewer:** the full milan_dp default sweep, `pp_shadow`, `milan_dp_render`, `nvm_cosim`, the builder, behave, Yosys, xvlog, the full parent/processor/gPTP banks, Docker/act and host `act_ci`. For those, this round relies on the published final-head author rows (`milan-dp-run`, `pp-shadow` and 17 static rows, all rc 0 at `224ec0e9`), on the manager's source banks, and on my round-1 ledger for scopes the delta does not touch.
- **Hosted snapshot at 03:41 UTC:**
  - `docs-check` and `docs-check-no-git`: **failure** (F1).
  - `rtl-fast`, `elaborate`, `wire-accountability`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0, 2 and 3, `bdd-conformance`, `changes` and `full-ci-gate`: success.
  - Verilator shards 1/5 and 4/5: still in progress.
  - "Physical gPTP (nightly and manual)": skipped. That context was not executed.
  - `verilator-suites` and `yosys-portability` were not yet reported as contexts in the snapshot.
- **Clause text.** Milan clause text was not available locally. The acceptance-2 reading rests on the recorded decision and on the processor's documented contract.
- **Hardware.** Physical calibration was NOT RUN. The field skips are not hardware proof.
- **Parallelism.** Every build ran sequentially with `VERILATOR_JOBS=8`.
- **Clone state.** Probes edited only temporary processor copies under `scratch/`. The build products I created (`obj_notify/`, the run-directory ROM images, and `__pycache__` directories, including one in the processor submodule) were removed. The clone was then verified: HEAD and index tree `2824fdf5`, 885 tracked blobs matching in bytes and mode, no status entries including ignored ones, four gitlinks at their pins, and three required submodules clean.
- **Receipt hygiene.** Host path prefixes in receipts and scripts were replaced by `<clone>`, `<packet>`, `<tool-bin>`, `<tool-root>`, `<home>` and `<tmp>`. Only path strings changed.

## Pending manager duties

- Route F1 and F2 to the executor. Then run a re-review at the fix head covering Tests and Docs, and any other lens whose scope the fix touches.
- Confirm that hosted `docs-check` and `docs-check-no-git` are green at the fix head.
- Accept the hosted runs, including Verilator shards 1/5 and 4/5 and the exact-head `verilator-suites` and `yosys-portability` contexts, and own the act replica.
- Build and validate the final current-dev candidate at the merge turn (source base `573f0052`, live dev `0755923d`).
- Post-merge containment.
- Physical calibration remains NOT RUN.

R307-2 FINISHED
