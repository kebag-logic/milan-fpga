[R571] NEGATIVE - exact head e0ee38f9d94bba29289f24f8f80a8d9645643c11

External independent review R571-1 of milan-fpga PR #707 (issue #621), parent head
`e0ee38f9d94bba29289f24f8f80a8d9645643c11` (tree `f22593159b8ede10eb6d488121225db07e603d9a`)
on source base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, with donor PR
Mister-M-alt/FPGA-gPTP#77 at `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (one commit on
`5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; the parent's `gptp-processor` gitlink is `7dda9c3b`).
All five lenses were applied. Three lenses are clean; Tests and Docs are not.

Verdict basis: one MAJOR (F1) and two MINOR (F2, F3) findings are open at this head.
The gPTP correction itself is sound: it reproduces, fixes and discriminates as claimed,
and the capture receipt satisfies the final ruling.

## Reconstruction

Sources read, in order: AGENTS.md, CONTRIBUTING.md (sections 2.1 and 3), docs/README.md,
REQUIREMENTS.md REQ-PTP-05..09, issue #621 body and every comment (assignment
6084306147, correction 6084315762, rulings 6087415319, 6087498843, 6087655217,
6088189432, the FINAL ruling 6089776382, the STOPs and REVIEW READY 6094760924),
the PR body, docs/design/GPTP_PLANE.md, docs/findings/387_SOFTWARE_GM_STEP.md,
the full parent diff `5603c353..e0ee38f9` and the donor diff `5dce647a..7dda9c3b`,
then the 57 published evidence files under `review-evidence/621-r1` at
`02d43fb7f99d31b7c0a03dcf9534f779b50f9480` (each verified against its git blob id).
No private material, lane scratchpad or other reviewer report was read. At the
start of this round PR #707 carried no review findings (two review-start notices,
no reviews, no inline comments), so there was nothing to resolve or retain.

Scope as frozen: items 1 and 2 of #621 (simulation reproduction for both signed
10 ms steps through the grandmaster path, cause, fix with a failing planted arm),
item 3 effects (media, `tu`, GPTP_GM_CHANGED, CLOCK_DOMAIN), plus the two
capture-harness extensions (ruling 6087415319; ruling 6089776382 replacing the
earlier receipt invariants). The physical repeat closes #621 later; the PR body
says "Relates to #621" and no commit carries a closing keyword (all four parent
commit bodies and the donor body are empty, one-line subjects).

## Mechanism and fix (independently derived)

The donor rate window (`gen_gptp_ucode.py` `_pdpost_neighbor_rate_ratio`,
S_NR3/S_NR4) divides successive peer t3 differences by successive local t4
differences. A servo phase step lands inside that window, so the next exchange's
neighbour rate ratio is wrong by about 1 percent, its link delay leaves the
-80..800 ns band (`_pdpost_verdict`), the ladder resets and two good exchanges
(about 2 s) are needed to re-raise asCapable. A completed exchange whose t1 and t4
straddle the step is mixed-epoch as well.

The fix (donor `7dda9c3b`): the SERVO step arm clears S_NR3 and sets a new cell
S_PDSTEP (`gen_gptp_ucode.py:836-838`); every request clears S_PDSTEP before it is
sent (`prog_tmr`, `:1298`); both completion entries (in-order Follow_Up `:1697`
and deferred t1 `:1283`) now pass through PDEPOCH (`:1727-1737`), which, while
S_PDSTEP stands, records the exchange as answered (S_PDGOT) and skips the rate,
delay and ladder tail. S_NR4 leaves the init list because it is read only behind
non-zero S_NR3 and every non-zero S_NR3 write (the `save` label) writes S_NR4 in
the same block; cold init and the step both zero S_NR3 (`:270-271`, `:1353`, `:836`).

Clause check against IEEE 802.1AS-2020: 11.2.2 (asCapable from the peer-delay
conditions), 11.2.19.3.3 computePdelayRateRatio (successive t3/t4), 11.2.19.3.4
computePropTime, 11.2.20 (MDPdelayResp, responder timestamps). The repo's
traceability row AS-8 maps peer delay and asCapable to 11.2.19, consistent with
these citations. Skipping computePdelayRateRatio/computePropTime for a measurement
known to straddle a LocalClock phase change while still crediting the received
response (lostResponses reset on receipt in the 11.2.19 machine) is a faithful
adaptation for an implementation whose timestamping clock is the stepped PHC.
The bench link partner is the AVB switch (387 findings page, line 72), whose
responder clock is independent, which is what both regressions now model.

## Findings

### F1 MAJOR - lenses: Tests, Docs
Artifact: `tb/verilator/gptp_plane/phc_step.py` (new in `a99dbccf`), absent from
`DUT_READER_DISPOSITIONS` in `scripts/measure_test_evidence_readers.py`;
hosted context `docs-check` at the exact head, step "Test-evidence ratchet".

Title: the new step regression breaks the repository's test-evidence ratchet.

Evidence: at `e0ee38f9`, `python3 scripts/measure_test_evidence.py --check` exits 1
with `tb/verilator/gptp_plane/phc_step.py: UNEXPLAINED` and
`FAIL: 1 unexplained DUT-source reader(s) > ratchet 0`
(receipts/static/measure_test_evidence.check.log, rc 1), and `--selftest` reports
`105 checks: 104 PASS, 1 FAIL` on "every DUT-source reader has a current
disposition" (receipts/static/measure_test_evidence_selftest.log, rc 1). The hosted
`docs-check` job for this exact head
(https://github.com/kebag-logic/milan-fpga/actions/runs/38031973368/job/114154638496)
concluded failure at the same step with the same line; the base `5603c353`
`docs-check` concluded success. `.github/workflows/docs.yml:311-314` runs both
commands. The script reads the donor generator's source and rewrites it for its
planted arms, which is exactly the class the ratchet requires to be classified.
The REVIEW READY and PR body report the local bar as green without this gate.

Impact: merging as-is turns `docs-check` red on `dev`; the new test is an
unclassified implementation-reading oracle, which the ratchet exists to prevent.

Required outcome: a disposition for `tb/verilator/gptp_plane/phc_step.py` that
truthfully states what it reads and why (it generates each arm's ROM from the
donor generator and plants three named generator defects into scratch copies,
requiring named runtime assertion failures; expected values come from the
independent peer model and the physical link constants, not from source text);
both commands exit 0; the hosted `docs-check` is green on the new exact head.

Verification: rerun both commands at the new head; read the hosted `docs-check`
conclusion for that head.

### F2 MINOR - lens: Tests
Artifact: `gptp-processor/hdl/ucode/gen_gptp_ucode.py:1736` (the S_PDGOT write in
`prog_leg_pdepoch`) against `tb/verilator/gptp_plane/sim_phc_step.cpp`.

Title: the crossing exchange's liveness credit is untested; deleting it escapes.

Evidence: reviewer plant `r571-no-liveness` (scripts/make_plants.py) removes only
that write. The full step regression then passes, `49 checks, 0 failures`, exit 0
(receipts/phc/r571-no-liveness.log/.rc). The behavior is a stated contract in both
donor `docs/INTEGRATION.md:197` ("A complete overlapping exchange still proves peer
liveness") and parent `docs/design/GPTP_PLANE.md:105` ("An overlapping completed
exchange proves liveness without replacing measurements"), and it is the part of
the change that keeps 802.1AS-2020 11.2.19's lostResponses reset on a received
response. AGENTS.md section 5 requires self-checking tests for changed behavior.

Impact: a regression that counts every crossing exchange as lost ships green.
With allowedLostResponses 3 (`LOST_N_C`), asCapable then falls one interval early
whenever a peer outage follows a step, and the documented claim stays unproved.

Required outcome: a check that fails when a crossing exchange is not credited as
answered (for example: after a crossing exchange, silence the peer and require
asCapable to fall exactly at the fourth unanswered request after it, not the
third), with this deletion added to the planted-defect set.

Verification: reapply `r571-no-liveness`; the new check fails and the clean
image passes.

### F3 MINOR - lens: Docs
Artifact: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1628`, `:1641-1643`,
`:1660-1661`, `:1806-1811`; pointer `tb/verilator/nvm_capture_cpu/README.md:137`.

Title: the hold-sizing design page still states the replaced receipt as current.

Evidence: line 1806 says Section 18 "gives the current receipt's identities and
six maxima", and lines 1808-1811 and Section 18 give measured commit `a2f17342`,
tree `c28595df`, protocol pin `b2db3a97`, 8x8/50 ON 13.84836 to 13.86484 ms
(3.5341x), OFF minimum 13.67682 ms. At this head `measurements.json` (written by
`e0ee38f9`) records base `034e2e30`, tree `a5d1a1b0`, protocol pin `2ad2f845`,
13.84682 to 13.86318 ms, margin 3.534542..., OFF minimum 13.68947 ms
(`measurements.json:487-491`, `:702`, `:1350-1351`, `:1362-1366`). The capture
README sends readers to that section to quantify both arms. The author raised
this as decision 3 in STOP 6089759400; the final ruling 6089776382 does not
address it; the PR body lists it as a limitation; no follow-up issue was found.

Impact: an authoritative design page and the recorded receipt disagree on the
figures and identities of the measurement that sizes the NVM hold. The numeric
change is small (0.00166 ms) and the hold conclusion is unchanged, but these are
figures and provenance claims, not wording, so this is not residue.

Required outcome: at the merge head the page's "current receipt" figures and
identities agree with `measurements.json` (a scope decision is needed, since the
lane boundary excludes that page). Per AGENTS.md section 7, moving this to another
issue does not resolve it.

Verification: compare the page's Section 18 and limitation 6 against the receipt
fields above; no current-tense statement quotes `13.86484`, `3.5341x` or `a2f17342`.

### R1 RESIDUE - lens: Docs (wording only)
Artifact: PR #707 body, "Status" paragraph: "Not yet reviewed; nothing is pushed."
The PR is open, both heads are published and review is running. Exact fix:
replace that sentence with "Pushed; independent review in progress."

### Suggestions (non-blocking, no lens effect)
- S1 (Robustness): only the servo step marks the outstanding exchange. A software
  settime (`PTP_CMD[0]`, which stays with software while the plane runs,
  `hdl/milan/milan_datapath.sv:2852`) is not marked and would reproduce the loss
  if issued while asCapable stands. Outside the assignment's grandmaster path;
  worth an issue if any product path issues settime after boot.
- S2 (RTL): the shipping gPTP ROM grows from 1008 to 1016 of 1024 words (99.2%,
  generator report). Eight words of headroom remain; worth recording in the donor.
- S3 (Robustness): if every exchange straddles a step (a servo stepping each
  interval), the delay is never re-measured while liveness keeps asCapable. Bounded
  by the 100 us locked step threshold; a sentence in INTEGRATION.md would make it
  explicit.

## Executed evidence (this round, exact head, pinned simulator)

Simulator: `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, `Verilator 5.050
2026-07-01 rev v5.050`, wrapper SHA-256 `905795b9...e92f`. Raw logs and exit codes
are under `receipts/`; scripts under `scripts/`. In four build logs
(`receipts/{physical,gptp_plane,gmstep,donor}/*.log`) the host home-directory
prefix of the simulator's include path is redacted to `<host-home>/`; nothing
else in any receipt was edited.

| Run | Result | Receipt |
|---|---|---|
| `phc_step.py --mutants` at head | 49 checks, 0 failures; 3 author plants rejected; campaign 4/4; rc 0 | receipts/phc/head-mutants.* |
| same regression, original donor generator `5dce647a` | 12 failures; every one of six placements loses asCapable for about 2.000 s (delays -3466, 4545, 4947029, -5045960 ns); rc 1 | receipts/phc/base-original.* |
| reviewer plant: deferred-t1 completion bypasses PDEPOCH | rejected (deferred arm, 2 failures) | receipts/phc/r571-deferred-bypass.* |
| reviewer plant: Follow_Up completion bypasses PDEPOCH | rejected (3 crossing arms, 6 failures) | receipts/phc/r571-followup-bypass.* |
| reviewer plant: step does not set S_PDSTEP | rejected (4 crossing arms, 8 failures) | receipts/phc/r571-step-unmarked.* |
| reviewer plant: crossing exchange not credited (F2) | ESCAPES: 49/0, rc 0 | receipts/phc/r571-no-liveness.* |
| `milan_dp` `gmstep` at head | 190 checks, 0 failures; rc 0 | receipts/gmstep/gmstep-head.* |
| same model, original donor ROM (`5dce647a`, 2 MHz, cease 3000 ms) | 40 failures incl. every `621:` capability, delay, `tu`, GM_CHANGED and CLOCK_DOMAIN check; rc 1 | receipts/gmstep/gmstep-base-rom.* |
| `gptp_plane` existing `run` target | 29/29; rc 0 | receipts/gptp_plane/run.* |
| donor `tb/verilator/engine` (`all`) | 1613/1613 checks, 34/34 mutants; rc 0 | receipts/donor/engine.* |
| `milan_dp` `ax1x1gptp` physical-clock leg (default windows, its gPTP ROM generated from the head donor) | 143 checks, 0 failures; 16.992556520 simulated s; wall 3796 s; rc 0 | receipts/physical/ax1x1gptp-head.* |
| `scripts/check_nvm_capture.py` | PASS; rc 0; `--mutation` bytes/records/clock/ignore-off-timing each rc 1 for the named reason | receipts/capture/check_nvm_capture* |
| `run.byte_only_controls()` at head | PASS | receipts/capture/byte_only_controls.head.* |
| plant: restore the pre-`034e2e30` bound | rejected ("exceeds half the 49 ms hold floor") | receipts/capture/byte_only_controls.plant-revert.* |
| plant: disable the production bound | rejected ("production timing bound was ignored") | receipts/capture/byte_only_controls.plant-nobound.* |
| `measure_test_evidence.py --check` / `--selftest` | rc 1 / rc 1 (F1) | receipts/static/measure_test_evidence* |
| docs_check, check_gptp_docs --with-submodule, check_diagram_pngs, gen_toc --check and --verify-anchors, check_em_dash --base 5603c353, check_doc_style, check_py/cpp/sv/sh idiom, check_hygiene --check, ci_events --check, check_doc_paths, check_archive, check_feature_status, lint_rtl --check (90 <= 90), git diff --check | all rc 0 | receipts/static/* |

ROM identity: the generator at `7dda9c3b` reproduces all four committed donor
images byte for byte (default `a435fba6...` = `syn/ooc/work` = `tb/verilator/ucpu`
= the new `syn/yosys/rom_digests.tsv` row; `--clk-hz 2000000` = `tb/tsngen`
`a5dd7468...`; `--clk-hz 2000000 --cease-ms 3000` = `tb/verilator/engine`
`b02f66b1...`). The end-station builder at head emits `fd3dad06...` for both
capture shapes, the receipt's `gptp_ucode_sha256`.

## Capture receipt against the final ruling 6089776382

1. Lane invariant: the published invariant (round1f-invariant.json/.log/-table.md)
   pairs all nine arms and controls, candidate `034e2e30`+`7dda9c3b` against base
   `5603c353`+`5dce647a`, same recipe on Verilator 5.052, differing gPTP ROMs, and
   byte-identical capture logs; only the base byte-only control exits 1, from the
   unfixed base grader. I did not rerun the capture SoC (see limits).
2. Refresh as measured with truthful provenance: verified at head that `tree`
   `a5d1a1b0...` is the tree of `034e2e30`; all four 8x8 `config_sha256` values equal
   `configs/endstation_ax7101_8x8.yaml` (`ca491ba5...`) and the 1x1 value equals
   its config (`6e1463f6...`); `gptp_ucode_sha256` equals the builder output above;
   `processor_pins` equal the head gitlinks; `simulator` is "Verilator 5.052";
   `remeasurement_assignment` names the final ruling; the `provenance` text states
   the measured tree, pins, simulator, the base equality and the dev attribution.
   The diff (`034e2e30..e0ee38f9`, 56 lines each way) touches only date, base,
   tree, provenance, assignment, pins, the `run.py` harness hash, six ROM hashes,
   four config hashes, 14 verdict values, 24 `requests` values; nothing else.
3. Bounds: `check_nvm_capture.py` regrades every recorded row through the head
   grader (24.5 ms bound applies, no `mutation` key) and recomputes maxima: PASS.
   Worst production capture 13.86318 ms; floor ratio 3.5345. Byte-only ratio
   1.834x (evidence) against 1.5x.
4. `scripts/check_nvm_capture.py` and its enforcement are unchanged by the PR.
5. `034e2e30` matches ruling 6087415319: the 24.5 ms bound applies only to
   `mutation none`; byte-only keeps completion, bytes, records, ownership, traffic
   and the 1.5x ratio; the two new fixtures exist and are discriminating (both
   plants above are rejected).

## Hosted evidence at the exact head (read-only)

Executed and successful: rtl-fast, bdd-conformance, changes, docs-check-no-git,
elaborate, firmware-unit, full-ci-gate, verilator-lint, wire-accountability,
yosys-elaboration, Yosys shards 0-3, Verilator shards 0-4, and the exact-head
`verilator-suites` and `yosys-portability` contexts (state read at
2026-10-10T08:27:39Z, receipts/hosted-check-runs.txt).
Executed and failed: `docs-check` (F1). Skipped context, not evidence:
"Physical gPTP (nightly and manual)". The manager owns hosted and local-replica
acceptance.

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #621 frozen items 1-2 and assignment effects; rulings 6087415319 and 6089776382; `gen_gptp_ucode.py:831-838,1283,1298,1697,1727-1737` against 802.1AS-2020 11.2.2, 11.2.19.3.3, 11.2.19.3.4, 11.2.20 and `docs/traceability/ieee8021as.md` AS-8; REQ-PTP-07/08 via `sim_gmstep.cpp` `check_small_grandmaster_steps`; base reproduction (receipts/phc/base-original, receipts/gmstep/gmstep-base-rom); receipt provenance and bounds; PR "Relates to #621" | R571-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| RTL | CLEAN | donor microcode legs SERVO, TMR, TXT1OK, PDPOST, PDEPOCH, PDPAIR, init list; scratch invariants S_NR3/S_NR4, S_PDSTEP, S_PDGOT; ROM fill 1016/1024; byte identity of four donor images, capture ROM and `rom_digests.tsv`; `gptp_plane_wrap.sv` PHC_INCR_P default equals the old constant; lint_rtl 90<=90, sv idiom gate | R571-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| Robustness | CLEAN | excessive-delay and missing-peer controls (`sim_phc_step.cpp:307-317`); deferred t1, step between t1 and response, step between response and Follow_Up; cold/warm reset reasoning for S_PDSTEP (cleared by each request, PDWAIT/T1V reset-backed) and S_NR4; cease gate precedes PDEPOCH (`_pdpost_pairing_gates`); multiple-responder bookkeeping untouched; byte-only/no-traffic/skip-copy grading paths in `run.py` | R571-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| Tests | UNCLEAN (F1, F2) | `phc_step.py`, `sim_phc_step.cpp`, `sim_gmstep.cpp` diff, `run.py` controls; executed runs in the table above incl. 4 reviewer plants (1 escaped); `measure_test_evidence.py` | R571-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |
| Docs | UNCLEAN (F1, F3; R1 residue) | `docs/design/GPTP_PLANE.md:97-147`, donor `docs/INTEGRATION.md` and `SOURCE_EVIDENCE.md` (anchor L848 is `prog_leg_slew`), pin updates in 8 parent pages and 2 diagrams, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1811`, capture README, PR body; static documentation gates | R571-1 | e0ee38f9d94bba29289f24f8f80a8d9645643c11 |

## Real limits

- The capture SoC campaign was not rerun: it needs the product LiteX/RV32
  environment and Verilator 5.052. Lane-invariant item 1 rests on the author's
  published hashes and logs; items 2-5 were checked independently.
- The 20-control `gmstep-mutants` campaign, the physical leg's control targets
  (6 + 20 + 14 + 14 checks in the published summary) and its extended arm, the
  61-suite sweep, Yosys, vendor frontend, routes and resource gates were not run
  here (outside this round's allowance); they are the author's published receipts.
  The 20-control log shows each control breaking its named check, and the new
  `621:` checks are among the checks the media controls break.
- Physical calibration was not run; simulation is not hardware proof. Field and
  hosted skips are not evidence.
- No manager source bank exists at this head; none is claimed or inferred.

## Pending manager duties

- Disposition of F1 (one data entry) and the hosted `docs-check` rerun on the new head.
- F2 test and plant; F3 scope decision for the design page (the lane boundary
  excludes it); R1 to the residue checklist.
- Donor PR #77 publication order (donor before parent gitlink), the current-dev
  merge candidate against live dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`
  with builder and native banks, and hosted/act acceptance.
- The physical five-step repeat that closes #621.

## Restore check

After all probes the clone was restored and checked (receipts/restore/restore-check.txt):
HEAD `e0ee38f9d94bba29289f24f8f80a8d9645643c11`, tree
`f22593159b8ede10eb6d488121225db07e603d9a`; the index equals HEAD and the work tree
equals the index; no assume-unchanged or skip-worktree entries; all 1234 parent and
104 donor tracked blobs rehash to their index ids and every mode matches; gitlinks
`gptp-processor` `7dda9c3b`, `protocol-processor` `2ad2f845`, `third_party/verilog-axis`
`48ff7a7e` checked out at those commits (`external` and `third_party/lwSRP` were
uninitialised at the start and remain so). Every build product this round created
inside the clone (ignored ROM images and model directories under
`tb/verilator/gptp_plane`, `tb/verilator/milan_dp` and the donor
`tb/verilator/engine`) was removed; `git status --ignored` is empty in both.

R571-1 FINISHED
