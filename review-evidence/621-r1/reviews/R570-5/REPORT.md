[R570] POSITIVE - exact head 2cf985f3206dd519d80142fd2479afe24c3051f6

Round R570-5. This is the internal cleared-context review of issue #621 / PR #707.

- Tree: `cee526a44c9ecce9e5728cfec19d67828f22fdb0`.
- Base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
- Donor gitlink `gptp-processor`: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`. The base pin is `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.

All five lenses were applied at this head.

- No BLOCKER, MAJOR or MINOR finding is open.
- One new RESIDUE (PR body wording) goes to the residue checklist.
- Every prior public finding on this PR is resolved at this head.
- Prior SUGGESTIONs are carried, with no lens effect.

## 1. Scope reconstructed

I read the sources in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The issue #621 body.
3. The manager's assignment (6084306147) and its correction (6084315762).
4. The capture rulings: 6087415319, 6087498843, 6087655217, 6088189432 and the final ruling, 6089776382.
5. The runtime-round assignment (6101380300).
6. REQUIREMENTS.md REQ-PTP-05, REQ-PTP-07 and REQ-PTP-08, and the gPTP design pages.
7. `git diff 5603c353..2cf985f3`: 14 commits and 40 files, plus the donor range `5dce647a..7dda9c3b`.
8. The public evidence tree `02d43fb7:review-evidence/621-r1` and the author's REVIEW READY comments.

I read prior review findings only after the independent pass below.

These acceptance terms are in force for this lane:

- **Item 1.** Reproduce a +10 ms and a -10 ms PHC step through the grandmaster path in simulation. Show the 2 s asCapable loss and its mechanism (IEEE 802.1AS-2020 11.2.2, 11.2.19, 11.2.20).
- **Item 2.** Fix it so a PHC step keeps asCapable and a valid link delay. Add a planted defect that fails the test. The evidence decides whether the fix belongs in the parent or the donor.
- **Assignment item 3 (effects).**
  - Media stays unaffected.
  - Simulation checks the `tu` episodes, GPTP_GM_CHANGED and CLOCK_DOMAIN.
  - Every suite and campaign that builds a changed file runs.
  - Resources are re-recorded if the shipping image moves.
- **Issue item 3 (bench repeat).** It belongs to a later bench lane, so the PR must not close #621.
- **Capture rulings.**
  - The byte-only control is graded by its own ratio, not by the production bound, in its own commit.
  - The receipt is refreshed through the record path from the candidate's runs.
  - The lane invariant is that base and candidate write byte-identical capture logs.
- **Runtime round.**
  - Measure each leg natively.
  - Keep `milan_dp` at or under 60% of 4800 s on hosted runners, with no coverage removed.
  - The GM step leg may move to its own every-PR suite on a shard with headroom.
  - No RTL, donor or graded-expectation change.

## 2. Findings at this head

### R570-5-R1 - RESIDUE - Docs - PR #707 body, Status section, lines 1-2

- **Wording now:** "The runtime-round head is pushed; hosted results at `f5d0fb0e` are the manager's to confirm. The round 4 head `2cf985f3` is local and unpushed."
- **Fact:** `2cf985f3` is the published PR head (`gh pr view 707 --json headRefOid`), and hosted runs are executing at it (`receipts/hosted-checks-2cf985f3-snapshot2.tsv`).
- **Why RESIDUE:** it is wording only. It changes no measurement, figure, verdict, test, code, generated artifact or clause claim, and it touches no privacy rule.
- **Exact fix:** replace both sentences with "The round 4 head `2cf985f3` is pushed; hosted results at it are the manager's to confirm."

This round raises no new SUGGESTION. Two observations from this pass repeat suggestions that are already carried, and they are recorded under those:

- step storms: R571-1-S3;
- a software settime: R570-1-S4 / R571-1-S1.

### Observations not attributable to this lane (no lens effect)

- `tb/verilator/milan_dp/README.md:15` still says "The eleven ordinary simulations". The recipe has had twelve since #658 (dev `30e3c018`).
  - This PR does not touch that line.
  - Its line 3, "fourteen elaborations", is accurate at this head: `make -n run` shows 14 Verilator invocations, against 15 at the base.
  - The author has already reported the line for the manager.
- The backpressure runner test also hangs at the base after its 14 direct controls: rc 124 under a 300 s bound (`receipts/base-backpressure.*`). Issue #720 (OPEN) records this.

## 3. Prior public findings, resolved or retained at this head

| Finding | Severity | Status at `2cf985f3` | Evidence (this round) |
|---|---|---|---|
| R570-1-F1 = R571-1-F1: test-evidence ratchet (`phc_step.py` reader) | BLOCKER / MAJOR | RESOLVED | `measure_test_evidence.py --check` exits 0, and `--selftest` passes 105 of 105 (`receipts/static-measure_test_evidence-*`). The disposition at `scripts/measure_test_evidence_readers.py:104-113` matches `tb/verilator/gptp_plane/phc_step.py:57-90`. Hosted `docs-check` was still running at the snapshot |
| R570-1-F2: a receipt arm escapes the production bound | MINOR | RESOLVED | `check_nvm_capture.py` exits 0. `--mutation receipt-opt-out` exits 1 with "receipt arm escaped the production timing bound". The other four mutations each exit 1 with their own reason (`receipts/static-check_nvm_capture*`) |
| R570-1-F3 = R571-1-F3: design page figures | MINOR | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1813-1816` equals `measurements.json` at this head. Maxima are 13.86318, 3.96728 and 10.42973 ms. 8x8 ON spans 13.84682-13.86318 ms and OFF 13.68947-13.69390 ms; the ratio is 3.5345x and the margin 10.63682 ms. The measured tree `a5d1a1b0` is the tree of `034e2e30`. The `run.py` hash `c230cb3e...` matches the file |
| R570-1-F4 = R571-1-F2: liveness credit for a crossing exchange | MINOR | RESOLVED | The `gptp_plane` suite logs `ARM liveness ... unanswered_at_drop=4`. It rejects `liveness-not-marked` and `r571-no-liveness` by name (`receipts/gptp_plane-suite.log`) |
| R570-1-F5: closing keyword | MINOR | RESOLVED | `closingIssuesReferences` is `[]`, and the body says "Relates to #621" |
| R570-1-R1 / R571-1-R1: status wording | RESIDUE | Superseded by R570-4-R1, then by R570-5-R1 | - |
| R571-2-F1: an unanswered crossing earns no credit | MINOR | RESOLVED | The suite logs `ARM unanswered crossing ... unanswered_at_drop=3`. It rejects `credit-on-step` by name, `nocease-control` passes, and the campaign passes 8 of 8 |
| R571-2-RES-1, RES-2 | RESIDUE | RESOLVED | `GPTP_PLANE.md:141-151` counts five distinct defects. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` carries the attribution sentence |
| R570-4-F1: the runner tests require a removed `run` step | MINOR | RESOLVED | `test_sim_pool.py` exits 0 with 17 of 17 (`receipts/test_sim_pool.*`). My plant inserts `$(MAKE) -C ../milan_dp_gm_steps` before `render_mutants.py`; it fails the inventory arm by name, 16 of 17 (`receipts/probe-test_sim_pool-gmsuite-before-render.*`). `test_sim_pool_backpressure.py:108` refuses a `gmstep` prerequisite, `:128-129` expect only the render banner, and `:132` refuses a controls run. Its 14 direct controls pass. Its recipe controls hang at base and head alike (#720) |
| R570-4-R1: status wording | RESIDUE | RESOLVED as worded. The next sentence is now stale; see R570-5-R1 | PR body |
| R570-1-S1..S5, R571-1-S1..S3, R570-2-S1 / R571-2-S1, R570-3-S1, R571-3-S1, R570-4-S1, R571-4-S1..S3 | SUGGESTION | Carried, no lens effect | Not reopened. I re-measured the ROM fill behind R570-1-S3 / R571-1-S2: 1016 of 1024 words (`receipts/rom-fill-head.txt`) |

## 4. Lens results

```text
[R570] PASS Conformance - gptp-processor@7dda9c3b hdl/ucode/gen_gptp_ucode.py:831-838,1265-1300,1472-1497,1727-1753,1850-1886; tb/verilator/gptp_plane/sim_phc_step.cpp:59-389; tb/verilator/milan_dp/sim_gmstep.cpp:952-1008; receipts/phc-orig.run.log, gptp_plane-suite.log, gm_steps-suite.log, gmstep-olddonor.log - checked against issue #621 items 1-2, assignment item 3, and IEEE 802.1AS-2020 11.2.2, 11.2.19.3.3, 11.2.19.3.4 and 11.2.20 as GPTP_PLANE.md:111-116 cites them. Mechanism reproduced: under the head harness, the base generator publishes -3466 ns or +4545 ns about 100 ms after a step between exchanges (a stale rate window), and about +/-5 ms for a crossing exchange. asCapable is lost for 2.0 s at all six placements; 14 of 62 checks fail. The fix acts at the servo step: it clears the rate window (S_NR3) and marks the outstanding request (S_PDSTEP). A completed crossing exchange sets only S_PDGOT, so lostResponses resets at the next request and the delay, ratio and ladder stay unchanged. An unanswered request still counts as lost, and each request clears the mark. The head passes 62 of 62 with no drop and no invalid delay, and excessive delay and peer silence still clear asCapable. In the integration leg, both signs under CRF and INTERNAL keep asCapable and the delay every cycle. Each step gives one tu episode and one GPTP_GM_CHANGED, CLOCK_DOMAIN deltas of 0/0 under CRF (the servo is unlocked) and 1/1 under INTERNAL, no mr change and no MEDIA_RESET. The PR does not close #621. Runtime round: no graded check and no CONTROLS entry changed since 83239549.
[R570] PASS RTL - git diff 5603c353..2cf985f3 over hdl/, configs/, syn/ (only syn/yosys/rom_digests.tsv, +1 row) and the gitlinks; donor hdl/ diff 5dce647a..7dda9c3b (generator only); gen_gptp_ucode.py:266-271,339-342,1350-1356; receipts/rom-fill-head.txt - neither parent nor donor RTL changes. S_PDSTEP is scratch cell 44 of 64 and has no other owner. S_NR4 is read only behind a nonzero S_NR3, and the two are saved together, so dropping S_NR4 from the boot clear is safe. Every request path clears S_PDSTEP before SEND, and nothing reads it before a request has been sent. The SERVO leg that sets it runs only while asCapable stands, so acquisition is unaffected. The ROM holds 1016 of 1024 words (base 1008). The regenerated image a435fba6... equals the donor's syn/ooc and ucpu images and the new rom_digests row. The author reported the route and resource gates at e0ee38f9, and no RTL or donor byte has changed since.
[R570] PASS Robustness - gen_gptp_ucode.py:1092-1131,1239-1300,1411-1455,1889-1901; sim_phc_step.cpp:266-389; sim_gmstep.cpp:1301-1334; receipts/gmstep-argparse.txt - checked the step against these paths: a deferred t1; a lost t1 (TXLOST clears the pairing, and the mark waits for the next request); a replayed response (S_PDGOT blocks the re-arm); cease and resume (no request means no clear, and resume credits as before); warm reset (the next request clears the mark); and two steps in one interval. The harness exercises six step placements, an answered and an unanswered crossing, excessive delay and silence. Option parsing exits 2 for an unknown option, a duplicate flag, three positionals, a missing image and a non-numeric delay. Carried SUGGESTIONs cover a software settime (it is not marked) and a step in every interval (the delay is never re-measured).
[R570] PASS Tests - receipts/gptp_plane-suite.log, phc-orig.*, phc-no-step-flag.*, phc-ratio-not-window.*, gmstep-olddonor.*, gm_steps-suite.log, gmstep-short-compare.txt, test_sim_pool.*, probe-test_sim_pool-*, static-check_nvm_capture-mut-*.log - each new test fails for its defect. The base generator fails phc_step (14 of 62) and the head integration leg (40 of 190: every class of 621: check, plus the #387 event checks). The step checks reject both of my plants: the servo no longer marking the request fails 10 of 62, and clearing the ratio instead of the window fails 12 of 62. The shipped campaign rejects its six plants by name while its positive control passes (8 of 8). The new suite passes at this head: 190 of 190, with the positive control passing and all five controls caught by name. The --no-small-steps transcript equals the full one minus one contiguous block of 86 #621 checks (104 = 190 - 86). The runner-test and capture-gate controls fail by name.
[R570] PASS Docs - docs/design/GPTP_PLANE.md:29-36,97-165; gptp-processor docs/INTEGRATION.md:192-213; docs/design/GM_LOSS_RECOVERY.md:227-239,272; docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1619-1667,1711,1813-1816; docs/testing/CI_WORKFLOWS.md:284-305; docs/testing/TESTING.md:278,388-391,599; tb/verilator/README.md:62-64; tb/verilator/milan_dp/README.md:3,81,900-938,1384-1386; tb/verilator/milan_dp_gm_steps/README.md; receipts/static-*.log - the code and this round's runs match each documented item: the phase-step contract, the clause table, the liveness counts, the plant counts, the receipt figures, the suite split and the commands. These gates exit 0: docs_check, check_em_dash (0 findings over 278 added lines), gen_toc --check, check_doc_style, check_doc_paths, check_gptp_docs --with-submodule, check_diagram_pngs and ci_events --check. Every page and both diagrams move the pin from 5dce647a to 7dda9c3b. Only RESIDUE R570-5-R1 (PR body) remains.
```

## 5. Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Donor generator `7dda9c3b` (step, request, epoch and verdict legs); `sim_phc_step.cpp`; the #621 phase of `sim_gmstep.cpp`; issue, assignment and rulings; REQ-PTP-05/07/08; base-generator reproduction; head suites | R570-5 | 2cf985f3206dd519d80142fd2479afe24c3051f6 |
| RTL | CLEAN | Parent `hdl/`, `configs/` and `syn/` diff (one digest row only); donor `hdl/` diff (generator only); scratch map and init list; regenerated ROM image and its fill | R570-5 | 2cf985f3206dd519d80142fd2479afe24c3051f6 |
| Robustness | CLEAN | Pairing, loss, cease, resume, TXLOST and deferred-t1 paths with the new mark; the harness's step placements and silence arms; gmstep option parsing | R570-5 | 2cf985f3206dd519d80142fd2479afe24c3051f6 |
| Tests | CLEAN | `gptp_plane` suite and campaign; base reproduction; two plants of my own; `milan_dp_gm_steps` suite; short-leg transcript comparison; integration probe with the base donor; runner tests and my Makefile plant; capture gate and its mutations | R570-5 | 2cf985f3206dd519d80142fd2479afe24c3051f6 |
| Docs | CLEAN (RESIDUE R570-5-R1 only) | The design, testing, CI, suite and capture pages listed in section 4; donor INTEGRATION.md; diagrams and the PNG manifest; the PR body | R570-5 | 2cf985f3206dd519d80142fd2479afe24c3051f6 |

## 6. Executed evidence (this round)

**Simulator.** All runs used the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`). The wrapper's sha256 is `905795b9...e92f` and the binary's is `fb2cc573...fcdf` (`receipts/verilator-identity.txt`).

**Isolation.** Runs at the exact head used the isolated review clone, with every submodule at its gitlink. Probes that change sources ran in a disposable clone, or on generator copies outside the tree.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/gptp_plane` | rc 0. `run` passes 29 of 29 and `phc_step` 62 of 62. The campaign passes 8 of 8: the positive control passes and all six plants are rejected by name | `receipts/gptp_plane-suite.{log,rc}` |
| `make -C tb/verilator/milan_dp_gm_steps VERILATOR_JOBS=4` | rc 0 in 632.9 s wall, under concurrent load. The clean leg passes 190 of 190. The positive control passes under `--no-small-steps`, and all five controls are caught by their named checks | `receipts/gm_steps-suite.{log,rc}` |
| Base generator `5dce647a` under the head `phc_step` harness | rc 1: 14 of 62 fail. Every step placement loses asCapable for 2.0 s and publishes an invalid delay | `receipts/phc-orig.*` |
| My plant `no-step-flag`: the servo does not mark the request | Rejected: 10 of 62 fail, in the four crossing placements and the liveness arm | `receipts/phc-no-step-flag.*`, `receipts/plants/no-step-flag.diff` |
| My plant `ratio-not-window`: the servo clears the ratio instead of the window | Rejected: 12 of 62 fail, in all six placements | `receipts/phc-ratio-not-window.*`, `receipts/plants/ratio-not-window.diff` |
| Head integration leg with the base donor ROM (disposable clone, donor at `5dce647a`) | rc 2: 40 of 190 fail. They include every `621:` asCapable, delay, tu, GM_CHANGED and CLOCK_DOMAIN check. Each step gives 2-3 tu episodes, as on the bench | `receipts/gmstep-olddonor.{log,rc}` |
| `Vmilan_dp_gmstep aemi.bin 0 --no-small-steps`, then a transcript comparison | rc 0: 104 checks in 44.9 s. The transcript equals the 190-check transcript minus one contiguous block of 86 checks | `receipts/gmstep-short-direct.log`, `receipts/gmstep-short-compare.txt`, `scripts/compare_short.py` |
| gmstep option probes | Each of five malformed argument lists exits 2 | `receipts/gmstep-argparse.txt` |
| `test_sim_pool.py` | rc 0, 17 of 17 | `receipts/test_sim_pool.*` |
| My Makefile plant: the GM step suite invoked before render | Caught: 16 of 17, "run still builds or runs the GM step leg" | `receipts/probe-test_sim_pool-gmsuite-before-render.*` |
| `test_sim_pool_backpressure.py` at head and at base, 300 s bound | Both pass 14 direct controls, then time out with rc 124 (Issue #720) | `receipts/test_sim_pool_backpressure.*`, `receipts/base-backpressure.*` |
| Static gates | Each exits 0: `measure_test_evidence --check` and `--selftest`, `suite_shards --selftest`, `check_nvm_capture`, `docs_check`, `check_em_dash --base 5603c353`, `gen_toc --check`, `check_py_idiom`, `check_cpp_idiom`, `check_doc_style`, `check_gptp_docs --with-submodule`, `check_doc_paths`, `check_diagram_pngs`, `ci_events --check` and `git diff --check` | `receipts/static-*` |
| Capture-gate mutations | Each exits 1 with its named reason: bytes, records, clock, ignore-off-timing and receipt-opt-out | `receipts/static-check_nvm_capture-mut-*` |
| ROM regeneration | The head image equals the committed donor images and the new digest row. It fills 1016 of 1024 words (1008 at the base) | `receipts/rom-fill-head.txt` |
| Clone restore | All 1236 tracked blobs are byte-identical, modes and index equal HEAD, no index entry is hidden and the gitlinks are unchanged | `receipts/restore.txt`, `receipts/submodule-status-{before,after}.txt` |

**Hosted results.** These are observed only; acceptance is the manager's. Snapshots were taken between 01:44 and 01:47 UTC (`receipts/hosted-checks-2cf985f3-snapshot*.tsv`, `receipts/hosted-shard3-job114357691336-excerpt.txt`).

- Exact-head `Verilator shard 3/5` (job 114357691336) completed successfully. It ran `milan_dp_gm_steps` in about 962 s (01:27:02.7 to 01:43:05.2), 53.5% of 1800 s.
- `Verilator shard 4/5` (`milan_dp`), shards 1 and 2, `docs-check` and `elaborate` were still running.
- `Physical gPTP` was skipped for this event, as designed.
- Each Yosys shard completed in about 30 s. This round did not establish whether that was a full run or a selected no-op.

## 7. Real limits

- No manager source bank exists at this head, and none is claimed or inferred.
- This round did not run the full parent sweep, Yosys, the builder or the vendor stages, because they are not allowed here.
  - The author's full-bar receipts are at `e0ee38f9`.
  - Since then, nothing has changed in RTL, the donor or any suite input except the two GM step suites and the runner tests.
- This round did not rerun `milan_dp` itself. The `2cf985f3` delta touches only its two runner tests, and no suite runs those.
- The IEEE clause text was not available to this review. I checked the clause mapping for consistency against the repository's own cited references and the state-machine behaviour, not against the standard's text.
- Retention of the neighbour rate ratio cannot be observed with a unity-rate peer (carried R570-1-S1). My `ratio-not-window` plant is rejected because the rate window spans the step, not because any check reads the ratio.
- The backpressure runner test's 14 recipe controls were not executed as invoked. They hang at base and head (#720).
- Physical calibration was NOT RUN. Simulation does not discharge issue item 3, and field skips are not hardware proof.
- The hosted results are snapshots taken while jobs were still running.

## 8. Pending manager duties

- Confirm the exact-head hosted contexts. These include `milan_dp` on shard 4 at or under 60% of 4800 s, `docs-check`, the `verilator-suites` and `yosys-portability` aggregates, and `rtl-fast`.
- Build and validate the current-dev merge candidate with the builder and native banks, and link the receipts. The source base is `5603c353` and live dev is `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
- Land the donor branch under the donor bar, before or with the parent, so the gitlink stays fetchable from the donor's default branch. FPGA-gPTP `7dda9c3b` is published on branch `621-ascapable-phc-step`.
- Carry R570-5-R1 to the residue checklist. Also carry the #495 capture-gate gap and the #720 runner-test gaps.
- Keep #621 open for the later physical five-step repeat.
- Merge only with explicit maintainer authorization and the external review's verdict at this head.

R570-5 FINISHED
