[R570] POSITIVE - exact head 83239549a500604baabc65e443ed90876d65a36e

Round R570-3: internal cleared-context review of issue #621 / PR #707.

- Head `83239549a500604baabc65e443ed90876d65a36e`, tree `f3ddc144693ad9273f92336ebe206e3af14200ec`.
- Delta: `d96b4a84..83239549`, two linear one-line commits with no trailers.
  - `4818cc37`: RES-1 and RES-2.
  - `83239549`: R571-2-F1.
- Donor gitlink `gptp-processor` `7dda9c3b` is unchanged, and so are `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e`.
- Source base `5603c353`.

Verdict basis:
- No BLOCKER, MAJOR or MINOR is open at this head, and no RESIDUE is raised.
- R571-2-F1, RES-1 and RES-2 are resolved. Every earlier finding stays resolved (table below).
- All five lenses were applied, and all five are clean.
- This round adds one SUGGESTION and carries one earlier SUGGESTION. Neither affects a lens.

## Reconstruction (public state only)

- AGENTS.md, CONTRIBUTING.md (by reference) and docs/README.md.
- Issue #621:
  - body, assignment 6084306147 and correction 6084315762, TAKEN 6084330397;
  - the capture rulings 6087415319, 6087498843 and 6087655217, and the STOP 6089759400 attribution evidence;
  - round 3 assignment 6096658408 and REVIEW READY 6097029581.
- PR #707: the live body (`receipts/pr707_body_snapshot.txt`; `closingIssuesReferences` is `[]`) and the comment list.
- `git diff 5603c353..83239549` history, and `git diff d96b4a84..83239549` in full.
- The donor generator legs the delta exercises: `gen_gptp_ucode.py`
  - `:403`: `LOST_N_C`;
  - `:836-838`: S_PDSTEP set at a servo phase step;
  - `:1289-1300`: `prog_tmr`;
  - `:1411-1460`: the cease rule;
  - `:1473-1497`: the lost-response judge;
  - `:1727-1737`: the PDEPOCH credit.
- The public evidence tree `02d43fb7…/review-evidence/621-r1` (round 1 author evidence), plus exact-head hosted check runs (read only).
- My independent pass, probes and draft verdict came first. Only then did I read the prior review reports: R571-2 (PR comment 6096652745) and R570-2 (6096655113). After that I fetched R571-2's two published plant patches, to confirm plant identity.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE at this head.

### R570-3-S1 - SUGGESTION - Tests, Robustness

- **Artifact:** `tb/verilator/gptp_plane/sim_phc_step.cpp:381-382`, `unanswered crossing: step falls between returned t1 and due response`.
- **Observation:** the check is `probe_stamp_ < last_step_cycle_ && last_step_cycle_ < due`. If the crossing request's t1 were never returned, `probe_stamp_` would stay 0 and the first half would pass vacuously. The round 2 arm (`:365-366`) and the crossing arms (`:285-286`) share the same pattern.
- **Evidence it holds at this head:** a diagnostic-only harness copy, `h0` (`probes.sh`), prints the probe fields for the clean image:
  - `probe_request=433600205`
  - `probe_stamp=433600273`
  - `step=433601263`
  - `probe_response=0` and `fu=0`
  - `due` = 433600205 + 6408 = 433606613

  All checks still pass (62/0, `receipts/probe_clean_h0.log`).
- **Suggested outcome (optional):** also require `probe_stamp_ != 0` (or `> probe_request_`).
- No lens effect.

### Carried: R570-2-S1 / R571-2-S1 - SUGGESTION - Conformance, Docs (threshold reading)

- **Unchanged, and not assigned in round 3.** The new arm inherits the donor's existing threshold (`gen_gptp_ucode.py:1491`, `CMP … LOST_N_C + 1`): asCapable falls when the fourth consecutive request is judged lost.
- The PR body's Known limitations states both readings: the 11.2.13.4 definition gives the fourth, and the literal RESET state of Figure 11-9 gives the fifth.
- A follow-up issue is the manager's decision.

## Resolution of the round 3 items and prior findings at this head

| ID | State at 83239549 | Evidence |
|---|---|---|
| R571-2-F1 (MINOR, Tests): no check that an unanswered crossing request earns no credit | RESOLVED | **New arm.** `exercise_unanswered_crossing` (`sim_phc_step.cpp:373-389`) uses the round 2 crossing step through the shared `silence_across_step` (`:336-356`). With `answer_crossing=false`, the peer ignores the crossing request itself (`:186`). The arm requires: one step; the step after the returned t1 and before the due response; the exchange never completing (`probe_response_ == 0 && probe_follow_up_ == 0`); no invalid delay; exactly one drop; and `unanswered_at_drop_ == 3`.<br>**Clean image at this head:** 62 checks, 0 failures, `LOSS … since_step_ns=3999855000 unanswered=3`.<br>**Campaign plant.** `credit-on-step` fails exactly one check, `asCapable falls at the third unanswered request after an unanswered crossing request got=4 exp=3`. `nocease-control` passes 62/62, and the campaign passes 8/8 with rc 0.<br>**Plant identity.** R571-2's published `patch_credit_on_step.diff` and `patch_nocease.diff`, applied to the head generator, give generator text byte-identical to the campaign's `credit-on-step` (sha256 `be720649…`) and `nocease-control` (`6966f456…`) arms (`receipts/plant_identity.txt`).<br>**Independent probes, each failing the new check by name:**<br>- `g2-credit-at-step`: credit written at the servo step itself, a different site from R571-2's plant, with the same ROM-room deletion. It fails only the new check (got=4).<br>- Donor threshold one lower: the new check gets got=2, the round 2 check got=3.<br>- Donor threshold one higher: the new check gets got=4, and the round 2 check, `liveness: asCapable falls once…` and `missing peer still clears asCapable` fail too.<br>- Harness fault `h1` (the peer answers the crossing request regardless): `crossing exchange never completes` and the count check (got=4) fail. |
| R571-2-RES-1 (RESIDUE, Docs): duplicate liveness plant counted twice | RESOLVED | **Text.** `GPTP_PLANE.md:141-151`: six planted-defect controls; the two credit-deletion controls plant the same deletion; so five distinct defects run. The positive control removes only the cease rule. The same accounting appears in the disposition at `measure_test_evidence_readers.py:104-113`, the campaign comment at `phc_step.py:79-81` and PR body lines 64 and 166.<br>**Meaning.** R571-2's "four distinct" is correctly updated to five by the new `credit-on-step` plant. The split into short sentences preserves the meaning, and `check_doc_style.py` passes with rc 0.<br>**Verified:**<br>- the two deletion arms write byte-identical generator text and ROM (hex sha256 `119256d1…` for both);<br>- `defects` has six entries and two controls, so the campaign has 8 arms;<br>- the step-credit plant does not fit with the cease rule kept (`g1-romroom`: `AssertionError: leg BECGATE (9 words) does not fit`; the clean ROM is 1016 of 1024 words). |
| R571-2-RES-2 (RESIDUE, Docs): drift attribution sentence | RESOLVED | **Text.** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` carries the exact fix verbatim.<br>**Meaning checked:**<br>- the four 8x8 `config_sha256` values move `a3f90aab…` → `ca491ba5…`, which are the SHA-256 of `configs/endstation_ax7101_8x8.yaml` at `a2f17342` and at `5603c353` (dev `6178aa1bd` adds the model-lint waiver);<br>- `raw` and `records` are unchanged in every row;<br>- STOP 6089759400 publishes an identical AEM image, BIOS and memory initialization across the trees.<br>**Consistency.** The receipt's own provenance string is not contradicted. |
| R570-1-F1..F5, R571-1-F1..F3, R570-1-R1 / R571-1-R1 | RESOLVED (round 2), unchanged | The delta does not touch `check_nvm_capture.py`, `run.py`, `measurements.json` or the section 18 figures. `check_nvm_capture.py` gives rc 0. `measure_test_evidence.py --check` gives rc 0 (0 unexplained readers), and `--selftest` passes 105/105. `closingIssuesReferences` is `[]`. |
| R570-1-S1..S5, R571-1-S1..S3, R571-2-S2 | SUGGESTION, carried | No lens effect. R571-2-S2 (a distinct second credit plant) is addressed in substance by `credit-on-step`. |

## Executed evidence (exact head 83239549, pinned Verilator 5.050)

Simulator: `Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9…` (`receipts/simulator_identity.txt`).

| Run | Result | Receipt |
|---|---|---|
| `phc_step.py --mutants --work <scratch>` (VERILATOR_JOBS 16) | rc 0. Clean 62/0. `nocease-control` passes. Six plants are rejected by name. Campaign 8/8. | `head_campaign.log`, `head_campaign_*.run.log` |
| Per-arm failure census | `credit-on-step` 1 failure (new check). Both liveness deletions: 1 failure each (round 2 check, got=3). `stale-rate-window` 12, `crossing-exchange` 10, `never-rearm-measurement` 11. | `head_campaign_*.run.log` |
| `probes.sh` | `g1-romroom` generation rc 1 (no ROM room). `g2-credit-at-step` rc 1, only the new check. `h0` rc 0 with diagnostics. `h1` rc 1, two named failures. | `probes_summary.log`, `probe_*.log` |
| `probes_threshold.sh` | third-loss rc 1 (got=2 / got=3). Fifth-loss rc 1 (4 failures). | `probes_threshold_summary.log`, `probe_thr_*.log` |
| Plant identity versus R571-2's patches | byte-identical (both arms) | `plant_identity.txt` |
| Static gates: `check_doc_style`, `check_cpp_idiom`, `check_py_idiom`, `check_doc_paths`, `check_gptp_docs --with-submodule`, `check_nvm_capture`, `measure_test_evidence --check` / `--selftest`, `git diff --check 5603c353` | rc 0 each | `gates.txt`, `gate_*.log` |
| `check_em_dash.py --base 5603c353` / `--base d96b4a84` | rc 2: cannot judge, because the pinned Markdown renderer is not installed here and no install is allowed. Replacement check: 0 added Markdown lines contain U+2014 against either base. Hosted `docs-check` succeeded at this head. | `gate_scripts_check_em_dash_*.log`, `gates.txt` |
| Restore verification | RESTORE: EXACT. 1234 parent blobs, 104 `gptp-processor`, 562 `protocol-processor` and 214 `verilog-axis` rehash equal, with modes. The index equals HEAD, and there are 0 assume-unchanged or skip-worktree entries. The gitlinks are checked out at their recorded commits. `git status --porcelain --ignored` is empty everywhere. | `verify_restore.log` |

Hosted, read only, at this exact head (`receipts/hosted_check_runs.tsv`):
- **Executed, success:** `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, `elaborate`, `changes`, `bdd-conformance`, `firmware-unit`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3.
- **In progress when read:** Verilator shards 1, 2 and 4.
- **Skipped, not evidence:** "Physical gPTP (nightly and manual)".
- The manager owns hosted and act acceptance.

## Evidence by lens

```text
[R570] PASS Conformance - sim_phc_step.cpp:327-389; phc_step.py:59-87; donor gen_gptp_ucode.py:403,836-838,1289-1300,1473-1497,1727-1737 (7dda9c3b); assignment 6096658408 items 1-2 - the new arm silences the crossing request, so its exchange never completes. It requires the drop at the third unanswered request after that request, the fourth lost in all. That is the same count as any other loss under the donor's existing allowedLostResponses reading, and it is the outcome R571-2-F1 required. The credit stays reachable only through PDEPOCH on a completed exchange. The donor is unchanged, as item 1 requires.
[R570] PASS RTL - git diff d96b4a84..83239549 --raw lists 5 files, none RTL or donor; the gitlinks are equal at both heads (7dda9c3b, 2ad2f845, 48ff7a7e) - no RTL, microcode or pin change. The unchanged donor RTL and its microcode were executed at this head: phc_step 62/0. Its ROM fill was measured: 1016 of 1024 words, and a 4-word plant in prog_tmr does not fit.
[R570] PASS Robustness - sim_phc_step.cpp:183-186,336-356,373-389; probes h0/h1 and the threshold variants - every state the shared silence routine uses is reset per arm, and answer_probe_ is restored. The negative path, a peer silent on the stepped request itself, drops capability exactly once, at the standard count, with no invalid delay publication. Answering the crossing request regardless (h1) is detected by name.
[R570] PASS Tests - phc_step.py campaign 8/8; per-arm logs; g2-credit-at-step; threshold third/fifth; h1 - the new check fails for R571-2's plant and for an independently placed credit defect, and it is pinned from both sides (got=2, got=4). The nocease control passes, so the plant's failure is not due to the ROM-room deletion. The round 2 arm keeps its six check names in order (call-site diff d96b4a84 to head). The earlier plants keep their results. measure_test_evidence --check/--selftest give rc 0.
[R570] PASS Docs - GPTP_PLANE.md:126-151; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632; measure_test_evidence_readers.py:104-113; phc_step.py:63-87 comments; PR body lines 39, 64, 127-129, 165-168, 221-225 - every count and claim was checked against execution: 6 plants and 5 distinct (identical text and ROM), the ROM-room reason (g1), "third unanswered request" (clean log), and RES-2's hash-only attribution (yaml blob hashes). Static doc gates give rc 0, and 0 added em dashes.
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_phc_step.cpp:327-389`; donor `gen_gptp_ucode.py:403,836-838,1289-1300,1473-1497,1727-1737`; assignment 6096658408; R571-2-F1 required outcome; threshold variants | R570-3 | 83239549a500604baabc65e443ed90876d65a36e |
| RTL | CLEAN | empty RTL, donor and pin delta `d96b4a84..83239549`; equal gitlinks; donor RTL and microcode executed (62 checks); ROM fill and no-room probe | R570-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Robustness | CLEAN | `sim_phc_step.cpp:183-186,336-356,373-389`; diagnostic harness `h0`; harness fault `h1`; threshold variants | R570-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Tests | CLEAN | `phc_step.py:59-115` campaign (8 arms, per-arm failure census); `credit-on-step` plant identity; `g2-credit-at-step`; third/fifth thresholds; `h1`; check-name continuity; test-evidence ratchet | R570-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Docs | CLEAN | `GPTP_PLANE.md:126-151`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` against `measurements.json` and the config blob hashes; readers disposition `:104-113`; PR body; static doc gates; hosted `docs-check` | R570-3 | 83239549a500604baabc65e443ed90876d65a36e |

Earlier coverage of artifacts this delta does not change stands as recorded by R570-1/R571-1 at `e0ee38f9` and R570-2/R571-2 at `d96b4a84`. This includes the donor fix, `sim_gmstep.cpp`, `run.py`, `measurements.json`, `check_nvm_capture.py` and the section 18 figures.

## Real limits

- No manager source bank runs at this head, and none is claimed or inferred. The source-head execution evidence for the gates I did not run is the author's published receipts.
- Not run here: the full suite sweep, Yosys, the lint ratchet, vendor stages, the builder gate, `milan_dp gmstep` and its mutants, the physical-clock leg and the capture campaign. Round 3 changes none of their inputs. The `gptp_plane` `run` target (`sim_main.cpp`, 29 checks) was not rerun, because its inputs are unchanged in the delta. The changed suite, `phc_step`, was run in full.
- The em-dash gate could not judge here (renderer not installed). It was replaced by a direct U+2014 scan of added Markdown lines and by the hosted `docs-check` success.
- RES-2's hash-only attribution was checked against blob hashes, unchanged `raw`/`records`, and the published STOP 6089759400 firmware-side identity. I did not rerun capture at intermediate dev commits.
- The IEEE 802.1AS-2020 text was not reproduced in this packet. The clause references follow the PR, the donor and the assignment.
- Hosted Verilator shards 1, 2 and 4 were in progress when read.
- Physical calibration NOT RUN. Issue #621 item 3, the bench five-step repeat, is open for a later lane. Simulation passes and skipped field contexts are not hardware proof.
- Receipts replace local absolute paths with `<PACKET>`, `<CHECKOUT>` and `<TOOLS>`. No other receipt content was changed.

## Pending manager duties

- Confirm the hosted `verilator-suites` / `yosys-portability` conclusions on this exact head (shards 1, 2 and 4 were in progress).
- Build and validate the current-dev merge candidate (source base `5603c353`, live dev `e8454e27`) with the builder and native banks, and link the receipts on the PR.
- Publish donor `7dda9c3b` before the parent merge, so the gitlink is fetchable.
- Decide on the carried threshold-reading suggestion (a follow-up issue or not), and optionally on R570-3-S1.
- R571-2's published `receipts/patch_credit_on_step.diff` and `patch_nocease.diff` do not hash to their MANIFEST lines (`ec976ad4…` and `45db0c6a…` published, `ebbd76c1…` and `539ea92e…` listed). Their headers carry a `$REVIEWS` placeholder. This is evidence-archive hygiene, not a PR defect: the patches apply and match the campaign byte for byte.
- Keep #621 open for the physical repeat (`closingIssuesReferences` is `[]`). An external positive review and the rest of the AGENTS.md section 7 bar are still required before merge.

R570-3 FINISHED
