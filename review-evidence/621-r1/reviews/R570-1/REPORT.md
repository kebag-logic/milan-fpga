[R570] NEGATIVE - exact head e0ee38f9d94bba29289f24f8f80a8d9645643c11

Round R570-1, internal cleared-context review of issue #621 / PR #707.
Parent head `e0ee38f9d94bba29289f24f8f80a8d9645643c11` (tree `f22593159b8ede10eb6d488121225db07e603d9a`) on dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`; donor Mister-M-alt/FPGA-gPTP#77 at `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (one commit on `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`), which is the parent's `gptp-processor` gitlink.

All five lenses were applied. RTL is clean. Conformance, Robustness, Tests and Docs are unclean:

- one BLOCKER: the required hosted `docs-check` context fails at this exact head;
- four MINOR findings;
- one RESIDUE and five SUGGESTIONs.

The gPTP correction itself holds up under independent reproduction. The original defect reproduces with the base donor generator in both harnesses, the fix passes, and every product-side plant I applied is rejected. The defects are in gating, test coverage, documentation and PR metadata around it.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md REQ-PTP-05/07/08.
- Issue #621 body and comments 6084306147 through 6094760924. That includes the assignment (items 1 to 3 and the STOP boundary), and rulings 6087415319 (harness correction) and 6089776382 (FINAL receipt ruling, which replaces 6087498843, 6087655217 and 6088189432).
- PR #707 body and comments. The only PR comment is the review-start notice; there were no prior review findings on PR #707, on the donor PR or on the issue.
- Diff `5603c353..e0ee38f9`, four one-line commits with no trailers. Donor diff `5dce647a..7dda9c3b`.
- Public evidence tree `02d43fb7…/review-evidence/621-r1`. All 57 files match their MANIFEST.json SHA-256.

## Findings

### F1 - BLOCKER - Tests, Docs - hosted `docs-check` fails at the exact head (test-evidence ratchet)

- Artifact:
  - `tb/verilator/gptp_plane/phc_step.py` (new; it reads the donor generator text and rewrites it);
  - `scripts/measure_test_evidence_readers.py` (`DUT_READER_DISPOSITIONS` has no entry for it);
  - hosted job https://github.com/kebag-logic/milan-fpga/actions/runs/38031973368/job/114154638496, step 37 "Test-evidence ratchet".
- Authority/evidence:
  - CONTRIBUTING.md 2.1 makes `docs-check` one of the seven required contexts. AGENTS.md 7 requires the required gates to pass.
  - At `e0ee38f9` the hosted `docs-check` concluded **failure**: `tb/verilator/gptp_plane/phc_step.py: UNEXPLAINED` and `FAIL: 1 unexplained DUT-source reader(s) > ratchet 0`.
  - Reproduced locally: `python3 scripts/measure_test_evidence.py --check` gives rc=1 (`receipts/static_measure_test_evidence.log:141,173`).
  - `docs-check` succeeds on the base `5603c353` and on live dev `554e61d2`, so this PR introduces the failure.
  - Steps 38 to 51 of that job were skipped by the failure, so they have no hosted result at this head. I ran their `--check` forms locally and they pass (see Tests evidence).
  - The PR body's "GREEN locally" and the REVIEW READY static-gate list omit this gate.
- Impact: the PR cannot satisfy the merge ruleset, and a new DUT-source reader lands without the recorded disposition that the Rule 8 measurement requires.
- Required outcome:
  - the reader carries an accurate disposition, so `measure_test_evidence.py --check` and `--selftest` exit 0;
  - the hosted `docs-check`, including its previously skipped steps, succeeds on the new head;
  - the PR's evidence names this gate's result.
  - That table lives under `scripts/`, which is outside the lane's stated boundary, so the manager decides the scope.
- Verification: local `--check`/`--selftest` rc 0; exact-head hosted `docs-check` success.

### F2 - MINOR - Robustness, Tests - the receipt gate lets a receipt arm opt out of the 24.5 ms production bound

- Artifact: `tb/verilator/nvm_capture_cpu/run.py:78-80` (the bound now keys on `spec.get('mutation', 'none')`), consumed by `scripts/check_nvm_capture.py:81` (`capture.grade_rows(arm['rows'], dict(arm, **census))`, where the spec is the receipt arm itself).
- Authority/evidence:
  - Ruling 6087415319 limits the bound to production arms and requires "no change to … the production bound". Every receipt arm is a production arm by construction: the gate requires exactly the six production points.
  - Probe `scripts/probe_receipt_mutation_key.py` plants a 25.0 ms capture in the 8x8/50 MHz ON arm with consistent summaries:
    - with no extra key, it is refused;
    - with `"mutation": "byte-only"` added to that arm, `check_receipt()` **accepts** a published 8x8 maximum of 25.0 ms (`receipts/probe_receipt_mutation_key.log`);
    - graded through the base revision's `run.py`, the same plant is refused (`receipts/probe_receipt_mutation_key_base_grader.log`).
  - No existing gate control covers this.
- Impact: the input gate that guards the published hold margin trusts a field of the artifact it verifies. A receipt written by a buggy composer, or edited by hand, can publish an over-bound production maximum while staying green.
- Required outcome: the receipt gate applies the production bound to every receipt arm whatever fields the receipt carries (for example, grade receipt arms explicitly as production, or refuse unknown arm keys), with a control that fails if that is undone.
- Verification: the probe reports REFUSED for both plants; `check_nvm_capture.py` and its four `--mutation` controls keep their exit codes; a new control fails when the guard is removed.

### F3 - MINOR - Docs - the design page that claims to give "the current receipt's" figures contradicts the refreshed receipt

- Artifact: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` lines 1619-1661 (section 18) and 1805-1817 (limits item 6), linked from `tb/verilator/nvm_capture_cpu/README.md:137` as quantifying both arms.
- Authority/evidence:
  - Line 1805 says "Section 18 gives the current receipt's identities and six maxima".
  - The page states:
    - measured 2026-10-02 at commit `a2f17342`, protocol pin `b2db3a97`;
    - worst 8x8 13.86484 ms, 3.5341x, margin 10.63516 ms;
    - 8x8 ON 13.84836-13.86484, OFF 13.67682-13.69390.
  - The receipt this PR records (`measurements.json`) states:
    - 2026-10-09, `base` `034e2e30`, tree `a5d1a1b0`, protocol pin `2ad2f845`, gPTP pin `7dda9c3b`;
    - 8x8/50 MHz maximum 13.86318 ms, margin 3.5345;
    - ON 13.84682-13.86318, OFF 13.68947-13.6939.
  - AGENTS.md 7 requires authoritative documentation to be current, and says that moving a finding to another Issue does not resolve it.
  - The author raised this as decision 3 in STOP 6089759400. Final ruling 6089776382 is silent on it, and the PR lists it as a known limitation.
  - This is a figure claim, not only wording, so it is not RESIDUE.
- Impact: after merge, the authoritative cost page and the receipt it cites as current disagree on the published maximum, margin and provenance.
- Required outcome: at the merge head the page's identities, maxima, margins and table rows agree with the receipt, or a recorded maintainer decision explicitly governs this page.
- Verification: the figures on the page compare equal to `measurements.json` `maxima`/`measurements`.

### F4 - MINOR - Tests - the new liveness behaviour of a crossing exchange has no test that can fail

- Artifact:
  - `gptp-processor/hdl/ucode/gen_gptp_ucode.py:1736` (the `PDEPOCH` write of `S_PDGOT` on a crossing exchange);
  - contract text at `gptp-processor/docs/INTEGRATION.md:197` ("A complete overlapping exchange still proves peer liveness") and `docs/design/GPTP_PLANE.md:105`.
- Authority/evidence:
  - AGENTS.md 5 and 6 (Tests): changed behaviour needs self-checking tests, and each test must be able to fail for its defect.
  - Reviewer plant `liveness-not-marked` deletes that one write. It passes the full `phc_step` regression, 49 checks with 0 failures (`receipts/phc_plant_liveness-not-marked.log`, rc 0), and the 190-check `gmstep` integration binary (`receipts/gmstep_liveness_plant_rom.log`, rc 0).
  - The behaviour is observable. Disposable probe `scripts/sim_phc_liveness_probe.cpp` places a crossing step between returned t1 and the response, then leaves N later requests unanswered (`receipts/liveness_probe.log`):

    | Generator | N = 3 unanswered | N = 4 unanswered |
    |---|---|---|
    | Head | asCapable held | asCapable drops (allowedLostResponses = 3) |
    | Liveness plant | asCapable drops one interval early | asCapable drops |
    | Base donor | asCapable drops one interval early | asCapable drops |

- Impact: a regression that counts a crossing exchange as a lost response would ship undetected, and asCapable would then fall one interval early after a step that coincides with losses.
- Required outcome: a self-checking case shows that a crossing exchange followed by allowedLostResponses unanswered requests keeps asCapable, and that one more clears it. The case fails with the `S_PDGOT` write removed.
- Verification: rerun the new case with the `liveness-not-marked` plant; it must fail by name.

### F5 - MINOR - Conformance, Docs - PR #707 will auto-close #621 at merge, before the physical acceptance

- Artifact: PR #707 body, "Known limitations": "The physical five-step repeat belongs to the later lane and closes #621."
- Authority/evidence:
  - GitHub parses "closes #621" as a closing keyword. GraphQL `closingIssuesReferences` for PR #707 returns `[621]`, and it is not user-linked (`receipts/pr707_closing_refs.json`).
  - Issue scope item 3 and the assignment keep the physical repeat as the closing criterion. The PR states "Relates to #621" and is meant to stay that way.
- Impact: merging would close #621 with acceptance item 3 unmet. That contradicts the issue contract and the board's Done rule.
- Required outcome: at merge, `closingIssuesReferences` for PR #707 is empty, and the body still reads "Relates to #621". For example: "The later lane's physical five-step repeat completes #621."
- Verification: `gh pr view 707 --json closingIssuesReferences` returns `[]`.

### R1 - RESIDUE - Docs - stale status wording in the PR body

- PR #707 body, Status: "Not yet reviewed; nothing is pushed." Both heads are published and the PR is open.
- Exact fix: replace with "Under review; the parent and donor heads are published."
- This is purely wording and touches no measurement.

### Suggestions (optional)

- **S1 - Tests:** retention of the neighbour rate ratio across a step is claimed but not observable. The `phc_step` peer LocalClock and the DUT PHC run at the same rate, so a dropped ratio is indistinguishable from a retained one. A reviewer plant that clears `S_NRR` at the step could not even be placed, because SERVO has no spare word (see S3). A peer with a rate offset (for example ±100 ppm) would make the claim testable.
- **S2 - Docs:** `CHANGELOG.md` records earlier gPTP pin advances (`:329`, for `5dce647a`) but has no Unreleased entry for `7dda9c3b` or the phase-step behaviour.
- **S3 - RTL:** the shipping gPTP ROM is now 1016 of 1024 words (99.2%; base 1008), and the SERVO leg has no spare word: a one-word plant fails with "leg SERVO (17 words) does not fit" (`receipts/phc_plant_drop-ratio-at-step.generate.log`). Recording the headroom would help the next donor change.
- **S4 - Conformance:** only the servo's own step marks a crossing exchange. A CSR settime or adjtime (`hdl/milan/milan_datapath.sv:2034`, the settime face) does not set `S_PDSTEP`. The docs scope this correctly ("A servo phase step"). A follow-up would be needed if software steps can occur while asCapable holds.
- **S5 - Docs:** the `docs/testing/TESTING.md:585` `gptp_plane` row does not mention the new default `phc-step` campaign and its planted defects.

## Evidence by lens

### Conformance

Clean on the protocol; unclean only through F5.

- The ruling-receipt judgement below is against FINAL ruling 6089776382, not the superseded invariants.
- IEEE 802.1AS-2020 clauses cited by the change (clause text not opened in this session):
  - 11.2.2: determination of asCapable.
  - 11.2.19.3.3: computePdelayRateRatio. This clause leaves the estimation scheme implementation-specific, so discarding a rate window that spans a local phase step is within that latitude.
  - 11.2.19.3.4: computePropTime. An exchange whose t1/t4 straddle a local PHC step does not form consistent differences, so retaining the last valid delay is a sound reading.
  - 11.2.20: MDPdelayResp. The responder supplies t2/t3 from its own clock, which is what both new harnesses model.
- `S_PDGOT` on a crossing exchange makes the next request reset `S_PDLOST` (`gen_gptp_ucode.py:1480-1484`). The probe confirms that allowedLostResponses = 3 still holds after a crossing exchange.
- The Milan 2-to-5 ladder is not advanced by a crossing exchange, which is conservative.
- **Assignment items 1 and 2**, reproduced independently:
  - `phc_step` with the base donor generator gives 12 failures, about 2.0 s outages for both signs, and invalid delays (`receipts/phc_base_generator.log`).
  - `gmstep` with the base ROM gives 40 failures, including asCapable, delay, `tu` episodes, GPTP_GM_CHANGED and CLOCK_DOMAIN (`receipts/gmstep_base_rom.log`).
  - At head, `phc_step` gives 49 checks and 0 failures (`receipts/phc_head_mutants.log`), and `gmstep` gives 190 checks and 0 failures (`receipts/gmstep_head.log`).
- **Assignment item 3 effects:** checked by the 621 block of `sim_gmstep.cpp`, both signs, under both CRF and INTERNAL.
- **Receipt against FINAL ruling 6089776382:**
  1. The nine-pair invariant record (`round1f-invariant.json`) shows equal base and candidate log hashes at the same recipe. Independently, the published candidate and base 1x1-50-on logs (`01f72663…`) parse to rows identical to the receipt's 1x1-50-on arm. The old receipt's rows reproduce only at its own tree `a2f17342`; at base `5603c353` nine `requests` fields differ, so the old receipt was stale at base, as recorded.
  2. My field-level diff `receipts/receipt_field_diff.tsv` has 56 changed fields, matching the PR's classes 14/24/1/7/5/5:
     - `tree` `a5d1a1b0` equals `034e2e30^{tree}`;
     - the pins are correct;
     - `gptp_ucode_sha256` `fd3dad06…` reproduces from the product builder for both shapes at head;
     - `harness_sha256` matches, since the gate passes.
  3. Bounds hold:
     - every production capture is at most 13.86318 ms, below 24.5 ms;
     - byte-only is 25.42688 / 13.86318 = 1.834x, at least 1.5x (author receipt);
     - every margin is at least 3.5345.
  4. `scripts/check_nvm_capture.py` gives rc 0 and all four `--mutation` controls give rc 1 (`receipts/check_nvm_capture_*.log`).
  5. The receipt records Verilator 5.052 as actually run, which the ruling requires.

### RTL

CLEAN.

- Reviewed the donor microcode legs SERVO, PDEPOCH, PDPAIR, PDPOST, TXT1OK and the timer/PDREQ path (`gen_gptp_ucode.py:812-845, 1265-1300, 1457-1504, 1687-1753`).
- Register use: PDEPOCH clobbers only RT and preserves RC (t3) for PDPAIR on both entries.
- The crossing branch writes scratch only, so no COMMIT is owed.
- `S_PDSTEP` is cleared on the timer path immediately before every Pdelay_Req (`:1298`). Beats that send no request leave it set until the next request, so no response can pair across it.
- Under warm reset, `S_T1V`/`S_PDWAIT` reset-backed validity prevents a stale pair.
- Scratch cell 44 is not aliased (parsed map: 40 `S_RSPSRC`, 41 `S_TXQ_RESP`, 42 `S_T3`, 43 `S_LOCK`, 44 `S_PDSTEP`).
- Removing `S_NR4` from the init list is safe behind nonzero `S_NR3`.
- All four committed donor ROM images regenerate byte-identical from the generator with their own recipes.
- `syn/yosys/rom_digests.tsv` row `7dda9c3b … a435fba6…` equals my regenerated default image.
- No parent `hdl/` file changes. `gptp_plane_wrap.sv` adds a TB-only `PHC_INCR_P` parameter, whose default keeps the 8.0 ns increment.
- Donor suites at head: engine 1613/0 plus its mutant campaign, rc 0 (`receipts/donor_engine.log`); µCPU 768/0 (`receipts/donor_ucpu.log`).

### Robustness

Unclean (F2). Otherwise checked:

- the loss and multiple-responder paths are unchanged (prove_real_failures in `phc_step`; the liveness probe at N = 4);
- excessive delay still clears asCapable;
- deferred t1 across a step, a response before the step, and t1 before the step in both signs;
- reset and warm-reset handling of `S_PDSTEP`;
- `run.py` defaults to the bound when `mutation` is missing, which fails closed;
- the `no-traffic` control is now unbounded, as the ruling's wording permits.

### Tests

Unclean (F1, F2, F4). Executed at head with Verilator 5.050 (identity verified: "Verilator 5.050 2026-07-01 rev v5.050"):

- **`phc_step.py --mutants`:** 49/0, and the author's three plants are re-applied and each rejected by name.
- **Reviewer plants:**
  - `step-not-flagged`: rejected, 2.0 s outages.
  - `liveness-not-marked`: **survives** (F4).
  - `drop-ratio-at-step`: not placeable (S1, S3).
- **Base generator:** 12 failures.
- **`gmstep`:** 190/0; with the base ROM, 40 failures; with the liveness-plant ROM, 190/0.
- **gmstep controls:** the default control set (`gmstep_mutants.py`) gives 6 checks, 6 PASS, rc 0 (`receipts/gmstep_mutants_acceptance.log`).
  - The full 20-control `--all` run was killed by the host after 11 elaborations, with no verdict, and is not counted.
  - The 20-control result therefore rests on the author's `72848a76` log. `sim_gmstep.cpp`, the RTL and the donor are unchanged since that commit.
- **Static gates, rc 0** (`receipts/static_*.log`):
  - docs_check, check_gptp_docs --with-submodule, check_py_idiom, check_cpp_idiom, check_diagram_pngs, check_doc_style;
  - check_hygiene --check, check_sv_idiom, check_sh_idiom, ci_events --check, check_doc_paths, check_archive, check_feature_status;
  - `git diff --check`.
- **Static gate, rc 1:** measure_test_evidence --check (F1).
- **Em-dash:** manual added-line U+2014 scan finds 0, because the pinned renderer is absent here.

### Docs

Unclean (F1, F3, F5; R1 is residue). Checked clean:

- `docs/design/GPTP_PLANE.md` new section: its contract, commands and counter statements match the tests, and both `make` targets exist;
- the donor `docs/INTEGRATION.md` and `SOURCE_EVIDENCE.md` (`#L848` is the policy leg);
- every pin link moved to `7dda9c3b`: SUBMODULES, guides, TIME_SYNC, traceability and both diagrams;
- `check_gptp_docs` and `check_diagram_pngs` pass.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F5) | `gen_gptp_ucode.py` pdelay/servo legs vs 802.1AS-2020 11.2.2/11.2.19.3.3/11.2.19.3.4/11.2.20; issue items 1-3; ruling 6089776382 vs `measurements.json`, `round1f-invariant.json`, published capture logs; PR #707 closing references | R570-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 (donor 7dda9c3b) |
| RTL | CLEAN | `gen_gptp_ucode.py:265-351,812-845,1265-1300,1457-1504,1687-1753`; regenerated ROM images and `syn/yosys/rom_digests.tsv`; `gptp_plane_wrap.sv`; donor engine/µCPU suites | R570-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 (donor 7dda9c3b) |
| Robustness | UNCLEAN (F2) | `run.py:58-127`, `check_nvm_capture.py:56-120` with receipt probe; loss/excess/deferred/reset paths via `phc_step`, liveness probe | R570-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| Tests | UNCLEAN (F1, F2, F4) | `sim_phc_step.cpp`, `phc_step.py`, `sim_gmstep.cpp` diff, `run.py` controls, `measure_test_evidence.py`; executed runs listed above | R570-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| Docs | UNCLEAN (F1, F3, F5) | `GPTP_PLANE.md`, `TIME_SYNC.md`, guides, `SUBMODULES.md`, `ieee8021as.md`, diagrams, donor `INTEGRATION.md`/`SOURCE_EVIDENCE.md`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, capture README, PR body | R570-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |

## Real limits

- I did not rerun the capture campaign. It needs the product environment and Verilator 5.052. Its invariant rests on the author's published record, plus my row-level cross-check of one published arm pair.
- I did not rerun the physical-clock campaign (197 checks, extended 143; about 3845 s), the full 61-suite sweep, Yosys, the builder bank or the vendor stages. These rest on the author's receipts.
- I did not open the IEEE 802.1AS-2020 text. Clause identification is from the reviewer's reading.
- `check_em_dash.py` and `gen_toc.py --check` could not run, because the pinned renderer is absent. A manual added-line scan replaced the em-dash gate.
- The donor head has no hosted check runs.
- Physical calibration was NOT RUN, and the hardware field skips are not hardware proof.
- The hosted snapshot (`receipts/hosted_check_runs_e0ee38f9.tsv`) is informational only. At the time of writing every exact-head run had completed successfully except two:
  - `docs-check`: failure (F1);
  - `Physical gPTP (nightly and manual)`: skipped, a context that executed nothing.
- The liveness probe and the receipt probe are disposable reviewer instruments, not proposed tests.

## Pending manager duties

- Disposition F1 to F5, including the scope of F1 (`scripts/` table) and F3 (design page), and carry R1 to the residue checklist.
- Hosted and act acceptance at the final head. `docs-check` was red at `e0ee38f9`, and its steps 38 to 51 never ran hosted.
- Validate the current-dev merge candidate (live dev `554e61d2`), using the builder and native banks.
- Publish the donor before the parent, and handle the donor PR merge and pin.
- Keep #621 open for the physical five-step repeat (see F5).

R570-1 FINISHED
