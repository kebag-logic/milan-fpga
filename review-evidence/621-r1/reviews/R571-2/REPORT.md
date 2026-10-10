[R571] NEGATIVE - exact head d96b4a8471028d3dfd370ce61dbe05ca9957320a

External independent review R571-2 of milan-fpga PR #707 (issue #621). Parent head
`d96b4a8471028d3dfd370ce61dbe05ca9957320a`, tree `19060afdf9e0e8f8c10f8adba9393922028211a4`,
source base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. The donor gitlink is unchanged at
`7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`.

This is a delta round over `e0ee38f9..d96b4a84` (four commits: `7ad00dbc`, `47b9b7e8`,
`167798a0`, `d96b4a84`). It answers round-2 assignment 6095695340 (R570-1-F1..F4,
R571-1-F1..F3 and R571-1-R1). All five lenses were applied at this head.

Verdict basis:
- One MINOR finding (F1, Tests) is open, so the verdict is NEGATIVE.
- Conformance, RTL, Robustness and Docs are clean.
- The round-2 fixes each do what the assignment asked, and every prior finding assigned to
  round 2 is resolved at this head.
- F1 is new. It covers the negative side of the liveness credit that round 2 now tests:
  credit given to a crossing request that never completed. No current check can catch that.
- Two RESIDUE items carry exact wording fixes.

## Reconstruction

Sources were read in this order:
1. AGENTS.md and CONTRIBUTING.md (by reference through AGENTS.md), then docs/README.md.
2. Issue #621 body and comments: assignment 6084306147, correction 6084315762, TAKEN, the
   STOPs, final ruling 6089776382, REVIEW READY 6094760924, round-2 assignment
   6095695340 and REVIEW READY 6096109824.
3. The live PR #707 body.
4. `git diff e0ee38f9..d96b4a84` and the commit history `5603c353..d96b4a84`.
5. The donor generator legs that the delta tests: `gen_gptp_ucode.py:1298`, `:1473-1504`
   and `:1727-1737`.
6. Exact-head hosted check runs, plus the `docs-check` job steps and log.

The author's round-2 handoff artifacts are not published on `621-review-evidence`
(tip `04be25e8`). Round-2 claims were therefore checked by rerunning them here, not by
reading author receipts.

My verdict and ledger were written to `receipts/PROVISIONAL_VERDICT.txt` before I read
R570-1 (PR comment 6095669772) or R571-1 (6095689596). After that I resolved every prior
finding (see the table below). The only prior-reviewer artifact I executed is R570-1's
`probe_receipt_mutation_key.py`, which the assignment names. Its SHA-256 `0c5c1b03…`
matches R570-1's published MANIFEST.

## Findings

### F1 - MINOR - lens: Tests

- **Title:** nothing checks that a crossing request whose exchange never completes earns
  no liveness credit.
- **Artifact:**
  - `tb/verilator/gptp_plane/sim_phc_step.cpp:183` and `:325-357`: the liveness arm always
    answers the crossing request and silences only later requests.
  - Credit gate: donor `gptp-processor/hdl/ucode/gen_gptp_ucode.py:1727-1737` (PDEPOCH,
    reached only on completion) and `:1480-1484` (the judge reads S_PDGOT).
- **Authority:**
  - AGENTS.md section 6, Tests lens: positive, negative and boundary behaviour is covered,
    and each test can fail for the defect it claims to detect.
  - The contract text says the credit needs a *completed* exchange:
    - `docs/design/GPTP_PLANE.md:105`: "An overlapping completed exchange proves liveness…"
    - PDEPOCH's own comment: "an unanswered request still uses the loss path".
- **Evidence** (`scripts/probe_unanswered_credit.sh`, receipts `unans_*`, `runs/unans_*`):
  - Mutant `credit_on_step` (`receipts/patch_credit_on_step.diff`) credits liveness to any
    request that overlapped a PHC step (S_PDSTEP), whether or not its exchange completed.
  - The ROM has no free word. To make room, the mutant drops the Milan 4.2.6.2.5 cease rule
    from the timer program. The same deletion alone (`nocease`) is the control, and it
    passes all 55 checks, so the deletion is inert in this one-responder regression.
  - `credit_on_step` passes the complete step regression at this head: 55 checks,
    0 failures, rc 0 (`unans_credit_on_step_real.*`). The liveness arm still reports
    `unanswered_at_drop=4`, because its crossing request is always answered.
  - The behaviour is observable. The one-line harness variant in
    `receipts/patch_variant_harness.diff` makes the peer also ignore the crossing request.
    Results under that variant:

    | Generator | unanswered at the asCapable drop |
    |---|---:|
    | head donor (`clean_variant`) | 4: the incomplete crossing request counts as lost |
    | `nocease` control | 4 |
    | `credit_on_step` mutant | 5, so a check on 4 rejects it (`got=5 exp=4`) |

  - In that variant, `liveness: step falls between returned t1 and response` also fails in
    every run, only because the probe is unanswered. A real check needs its own arm.
- **Impact:** a regression that credits a crossing request before or without a completed
  exchange still passes the whole suite. Examples: credit on the step, or credit on the
  Pdelay_Resp without the Follow_Up. A peer that goes silent across a grandmaster step would
  then keep asCapable one interval longer than allowedLostResponses permits. The shipped
  donor behaves correctly (`clean_variant`), so this is a test gap and not a product defect.
- **Required outcome:** the step regression has a self-checking case in which a request
  overlaps a PHC step and its exchange does not complete. asCapable must fall at the same
  count as for any other lost request. With the shipped donor, the variant above shows this
  as the fourth unanswered request, the crossing request included. The case must fail
  against a planted credit-without-completion defect, and that defect should join the
  campaign's planted set.
- **Verification:** run the new case with the head donor (passes), then with
  `credit_on_step` or an equivalent plant (fails by name). The existing 55 checks and the
  six campaign arms must keep their results.

### RES-1 - RESIDUE - lens: Docs (wording only)

- **Artifact:**
  - `docs/design/GPTP_PLANE.md:137` ("five planted-defect controls");
  - `scripts/measure_test_evidence_readers.py:104-110` ("one of five named defects … and
    two deletions of a crossing exchange's liveness credit");
  - `tb/verilator/gptp_plane/phc_step.py:69-70` ("delete … through different anchors");
  - PR body ("five planted microcode defects", "five rejected microcode defects").
- **Evidence:**
  - `liveness-not-marked` and `r571-no-liveness` produce byte-identical generator text.
    Both hash to SHA-256 `b7aef03b2a0d237549d024653373ee2c3a637ccd948b94409c55455c51c8f10f`
    (`receipts/plant_identity.txt`).
  - The campaign therefore runs four distinct defects, one of them twice.
  - Every sentence above is literally true, and the assignment asked for both named plants.
    No test, figure or verdict changes, so this is wording only.
- **Exact fix:** after "The first command includes five planted-defect controls." in
  GPTP_PLANE.md, add "The two liveness controls, one per review round, plant the same
  deletion, so four distinct defects run." Add the same clause to the disposition text and
  the PR body.

### RES-2 - RESIDUE - lens: Docs (wording only)

- **Artifact:** `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632`: "Capture-SoC RTL and
  8x8 configuration changes on dev moved the figures from the previous receipt."
- **Evidence:**
  - Per STOP 6089759400 and the PR's field table, the timing figures moved because of the
    capture-SoC RTL drift.
  - Dev `6178aa1bd` (8x8 configuration) changed only the four `config_sha256` fields, and
    the flash image is unchanged.
  - No figure on the page is wrong; only the attribution sentence is loose.
- **Exact fix:** "Capture-SoC RTL changes on dev moved the timing figures from the previous
  receipt; a dev 8x8 configuration change moved only its recorded configuration hash."

### Suggestions (no lens effect)

- **S1 (Conformance):** the author published the threshold reading as an open question
  (fourth versus fifth unanswered request; Figure 11-9 RESET compares before it
  increments). The assignment fixed the fourth. The allowedLostResponses definition
  ("above which") and 11.2.2's "does not exceed" wording support the fourth.
  - At this head the fourth is pinned twice. A fifth-loss donor variant fails both the new
    check (got=0 within the window) and the existing `missing peer still clears asCapable`
    check (`runs/threshold_fifth.run.log`).
  - A third-loss variant fails the new check with got=3 (`runs/threshold_third.run.log`).
  - Settling the reading in a follow-up issue is the manager's decision.
- **S2 (Tests):** with RES-1 in mind, a distinct second liveness plant would add more value
  than a duplicate. One option is the credit-without-completion defect from F1.

## Prior findings at this head

| Prior finding | Status at d96b4a84 | Evidence |
|---|---|---|
| R570-1-F1 = R571-1-F1 (test-evidence ratchet; hosted `docs-check` red) | RESOLVED | Disposition `measure_test_evidence_readers.py:104-110` is accurate, apart from RES-1's wording: the script reads the generator text, plants into scratch copies, requires the named check to fail and the clean image to pass, and its expectations come from the peer model, link constants and allowedLostResponses. `--check` rc 0 with 0 unexplained readers; `--selftest` 105/105 rc 0 (`mte_*`). Hosted `docs-check` job 114182327965 at this head: 55 of 55 steps `success`, none skipped. That includes "Test-evidence ratchet" (step 37) and steps 38-51, which were skipped at `e0ee38f9` (`hosted_docs_check_steps.txt`, `hosted_docs_check_excerpt.txt`). The PR body names the gate. |
| R570-1-F2 (receipt arm could opt out of the production bound) | RESOLVED | `check_nvm_capture.py:55-62` grades every arm through `production_spec` (named scenario keys only, `mutation='none'`). `run.py:78` keys the bound only on `mutation`, and `sys_hz` is cross-checked at `:83`, so no arm field reaches the exemption. The gate passes (rc 0), and `--mutation bytes`, `records`, `clock`, `ignore-off-timing` and `receipt-opt-out` each exit 1 for their named reason (`nvm_*`). Reviewer guard removals: call site back to `dict(arm, **census)` gives rc 1, and the spec builder passing the arm's `mutation` gives rc 1, both with "receipt arm escaped the production timing bound" (`guard_*`). R570-1's probe at this head: plain plant refused (by the grader while the probe builds it, as in R570-1's own log); keyed plant `REFUSED: worst measured copy exceeds half the 49 ms hold floor` (`r570_probe_receipt_mutation_key_at_head.log`). The capture harness files are untouched (`.md` only), so `harness_sha256` still matches. |
| R570-1-F3 = R571-1-F3 (design page quoted the replaced receipt) | RESOLVED | `scripts/compare_page_receipt.py` derives every expected string from `measurements.json`: date, measured commit, tree (equal to `git rev-parse 034e2e30^{tree}`), firmware, both pins, ruling and procedure links, 24.5 ms limit, the worst 8x8 figure with ratio and margin in section 18 and limits item 6, the 1x1 maximum, the 100 MHz maximum, census bytes, and all six table rows. All 26 string comparisons pass, as do the tree, row-count and stale-token checks; rc 0 (`page_vs_receipt.log`). Control: the `e0ee38f9` page fails 22 comparisons (14 differences and 8 stale tokens), rc 1 (`page_vs_receipt_control_e0ee38f9.log`). |
| R570-1-F4 = R571-1-F2 (crossing exchange's liveness credit untested) | RESOLVED (positive path). F1 above is the separate negative path. | Campaign at head: clean 55/0, liveness arm `drops=1 unanswered_at_drop=4`. All five plants are rejected by name. Both liveness plants fail only `asCapable falls at the fourth unanswered request after a crossing exchange got=3 exp=4` (`phc_step_mutants.log`, `runs/campaign_*`). The donor generator is unchanged (gitlink `7dda9c3b` at both `e0ee38f9` and head). Order check: in the donor, the judge runs before the next Pdelay_Req is emitted, and the harness counts a request only at its transmit EOF, so `unanswered_at_drop` counts the requests judged lost. |
| R570-1-F5 (closing keyword) | RESOLVED (not assigned in round 2, but true at this head) | Live body reads "Relates to #621" and "The later lane's physical five-step repeat completes #621". GraphQL `closingIssuesReferences` is `[]` (`pr707_closing_refs.json`). |
| R570-1-R1 / R571-1-R1 (status wording) | RESOLVED | Live body Status: "Pushed; independent review in progress." |
| Prior suggestions (R570-1 S1-S5, R571-1 S1-S3) | No lens effect; not re-adjudicated | R570-1 S3 / R571-1 S2 (ROM headroom) are consistent with this round: a 4-word plant in the timer program does not fit ("leg BECGATE (9 words) does not fit"). |

## Executed evidence (this round, exact head)

Simulator: the scoped pinned wrapper. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and
`verilator_bin` has SHA-256 `44898b22…bfdd` (`simulator_identity.txt`).
Campaign compiles used `VERILATOR_JOBS` 3 to 5, with at most 16 jobs in total.

| Run | Result | Receipt |
|---|---|---|
| `phc_step.py --mutants` | clean 55/0; 5 plants rejected by name; campaign 6/6; rc 0 | `phc_step_mutants.*`, `runs/campaign_*` |
| donor threshold at third loss | rc 1; new check got=3 exp=4 | `phc_step_third.*`, `runs/threshold_third.run.log` |
| donor threshold at fifth loss | rc 1; new check got=0; `missing peer still clears asCapable` got=4 | `phc_step_fifth.*`, `runs/threshold_fifth.run.log` |
| F1 probe, five arms | see F1 | `unans_*`, `runs/unans_*`, `patch_*` |
| `measure_test_evidence.py --check` / `--selftest` | rc 0 / rc 0 (105/105) | `mte_*` |
| `check_nvm_capture.py` plus five `--mutation` runs | 0; 1 each for its named reason | `nvm_*` |
| guard-removal plants (call site, spec builder) | rc 1 each, "receipt arm escaped…" | `guard_*` |
| R570-1 receipt probe | both plants refused | `r570_probe_receipt_mutation_key_at_head.*` |
| page versus receipt, plus control on the old page | rc 0 / rc 1 | `page_vs_receipt*` |
| liveness plants' identity | byte-identical text | `plant_identity.txt` |
| restore check | see below | `restore_check.txt` |

Hosted, read-only (`hosted_check_runs_d96b4a84.tsv`, read 2026-10-10T12:36+02:00):

- **Executed, success:** `docs-check` (55/55 steps), `docs-check-no-git`, `rtl-fast`,
  `bdd-conformance`, `changes`, `elaborate`, `firmware-unit`, `full-ci-gate`,
  `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3, and
  Verilator shards 0 and 3.
- **In progress at the time of reading:** Verilator shards 1, 2 and 4.
- **Skipped (not evidence):** "Physical gPTP (nightly and manual)".

The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-2 assignment items 1-5 against the delta. Final ruling 6089776382 against `measurements.json` and section 18. `sim_phc_step.cpp:325-357` against allowedLostResponses 3, IEEE 802.1AS-2020 11.2.13.4 / 11.2.19 as cited, and donor `gen_gptp_ucode.py:403,1473-1504,1727-1737`. Threshold variants third and fifth. PR body Status and closing references (`[]`). | R571-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| RTL | CLEAN | No RTL or donor artifact changed in the delta: `git diff --stat e0ee38f9..d96b4a84` lists 7 non-RTL files, and the gitlinks `gptp-processor` 7dda9c3b and `protocol-processor` 2ad2f845 are equal at both heads. Microcode behaviour exercised: PDEPOCH credit, judge-before-request ordering (`:1298`, `:1473-1504`), and the S_PDSTEP lifetime (`:836-838`, `:1298`). ROM fill observed (no 4-word headroom in the timer program). | R571-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Robustness | CLEAN | `check_nvm_capture.py:55-62,83-91,131-159` against arms that carry control fields (two guard-removal plants and R570-1's probe). `phc_step.py:25-35`: `plant()` refuses a non-unique anchor, and a missing scope raises. Peer silence after an answered crossing exchange (drop at the 4th) and after an unanswered crossing request (drop at the 4th including it; `clean_variant`); the shipped donor handles both. `run.py:78` fails closed when `mutation` is absent. | R571-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Tests | UNCLEAN (F1) | `sim_phc_step.cpp:102-104,183,234-238,325-357`; `phc_step.py:57-76` (5 plants, of which 2 are identical); the campaign and threshold runs; the F1 mutant, control and variant harness; `check_nvm_capture.py` `opt_out_control` and `--mutation receipt-opt-out`, plus guard removals; `measure_test_evidence.py --check/--selftest` | R571-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |
| Docs | CLEAN (RES-1, RES-2 are residue) | `docs/design/GPTP_PLANE.md:126-140`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1711,1806-1823` via `compare_page_receipt.py` and its control; `tb/verilator/nvm_capture_cpu/README.md:184-195`; disposition text `measure_test_evidence_readers.py:104-110`; the live PR body; hosted `docs-check` steps | R571-2 | d96b4a8471028d3dfd370ce61dbe05ca9957320a |

Earlier coverage of artifacts that the delta did not change stands as recorded by R570-1
and R571-1 at `e0ee38f9`. This includes the donor fix, `sim_gmstep.cpp`, `run.py`,
`measurements.json` and the receipt invariant.

## Real limits

- The capture SoC campaign was not rerun, because it needs the product environment and
  Verilator 5.052. Round 2 changes no capture-harness file, and the receipt is unchanged
  since `e0ee38f9`.
- Not run here (outside this round's allowance; the author's `e0ee38f9` receipts stand):
  `milan_dp` `gmstep` and `gmstep-mutants`, the physical-clock leg, the 61-suite sweep,
  Yosys, lint and the vendor stages. Round 2 changes no input to them.
- The F1 mutant was run only against the step regression. Whether `gmstep` would catch it
  was not tested.
- Clause wording above comes from reading the cited clauses; the standard's text was not
  reproduced in this packet.
- No manager source bank exists at this head; none is claimed or inferred.
- Physical calibration was NOT RUN. Simulation and field skips are not hardware proof.

## Pending manager duties

- Disposition F1, and carry RES-1 and RES-2 to the residue checklist. S1 (threshold
  reading) is a possible follow-up issue.
- Confirm the hosted Verilator shards 1, 2 and 4 at this head (in progress when read). Own
  hosted and act acceptance.
- Validate the current-dev merge candidate (source base `5603c353`, live dev `e8454e27`)
  with the builder and native banks, and link its receipts.
- Publish the donor before the parent, then handle the donor PR and the pin.
- Keep #621 open for the physical five-step repeat.

## Restore check

After all probes (`receipts/restore_check.txt`):
- HEAD is `d96b4a84…` with tree `19060afd…`. The work tree and index equal HEAD, and there
  are 0 assume-unchanged or skip-worktree entries.
- Every tracked blob rehashes to its index id with a matching mode: 1234 in the parent, 104
  in `gptp-processor`, 562 in `protocol-processor` and 214 in `third_party/verilog-axis`.
- Gitlinks `gptp-processor` 7dda9c3b, `protocol-processor` 2ad2f845 and
  `third_party/verilog-axis` 48ff7a7e are checked out at those commits. `external` and
  `third_party/lwSRP` were uninitialised and remain so.
- The temporary probe copies of `check_nvm_capture.py` were deleted. The Python bytecode
  caches that the runs created (parent and `protocol-processor`) were removed.
- `git status --porcelain --ignored` is empty in the parent and every initialised
  submodule. All campaign work trees are under the packet's unpublished `scratch/`.

R571-2 FINISHED
