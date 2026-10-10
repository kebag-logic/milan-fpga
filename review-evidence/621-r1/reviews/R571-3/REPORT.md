[R571] POSITIVE - exact head 83239549a500604baabc65e443ed90876d65a36e

External independent review R571-3 of milan-fpga PR #707 (issue #621).
Parent head `83239549a500604baabc65e443ed90876d65a36e`, tree `f3ddc144693ad9273f92336ebe206e3af14200ec`.
Source base `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
Donor gitlink `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, unchanged since `d96b4a84`.
Protocol-processor `2ad2f845` and verilog-axis `48ff7a7e` are also unchanged.

This is a delta round over `d96b4a84..83239549`: two one-line commits, `4818cc37` and `83239549`.
It answers round-3 assignment 6096658408: R571-2-F1, R571-2-RES-1 and R571-2-RES-2.

Verdict basis:
- No BLOCKER, MAJOR or MINOR is open at this head.
- All five lenses were applied at this head, and all five are clean.
- R571-2-F1, RES-1 and RES-2 are resolved (table below).
- Every earlier finding stays resolved. The delta touches none of their artifacts, apart from the ones re-checked here.
- This round adds one SUGGESTION (S1), which has no lens effect.

## Reconstruction

Sources were read in this order:
1. AGENTS.md (with CONTRIBUTING.md through its references) and the docs map.
2. Issue #621 body, round-3 assignment 6096658408, and review start 6097488962.
3. `git diff d96b4a84..83239549`, the history `5603c353..83239549`, and the receipt diff `5603c353..83239549` for RES-2.
4. The donor generator legs that the delta tests: `gen_gptp_ucode.py:1289-1299` (`prog_tmr`), `:1411` (`_tmr_cease_rule`), `:1473-1497` (the lost-response judge) and `:1727-1737` (PDEPOCH).
5. The live PR #707 body (`receipts/pr707_view.json`) and the exact-head hosted check runs.

My own pass over the delta, the campaign and the probes was complete before I read R571-2 and R570-2.
I then read them only to resolve their findings.

## Delta examined

| Commit | Change |
|---|---|
| `4818cc37` | RES-1 wording in `GPTP_PLANE.md`, the disposition text and the campaign comment; the RES-2 sentence at `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` |
| `83239549` | New arm `exercise_unanswered_crossing` (`sim_phc_step.cpp:373-389`); shared helpers `requalify` and `silence_across_step` (`:327-356`); flag `answer_probe_` (`:104`, `:186`, `:345`, `:351`); campaign plant `credit-on-step` and control `nocease-control` (`phc_step.py:62-71`, `:85-87`, `:101-107`); design page `GPTP_PLANE.md:130-151`; disposition `measure_test_evidence_readers.py:104-114` |

## Findings

There is no BLOCKER, MAJOR, MINOR or RESIDUE.

### S1 - SUGGESTION - lenses: Tests, Robustness - `tb/verilator/gptp_plane/sim_phc_step.cpp:186`, `:373-389`

- **Title:** a partial crossing exchange (a Pdelay_Resp without its Follow_Up) is not a shipped arm.
- **Evidence:**
  - R571-2-F1's impact named two shapes of credit without completion: credit on the step, and credit on the Pdelay_Resp alone.
  - The new arm drops both messages, so it pins the first shape. A defect that credits on the Pdelay_Resp alone would still pass the shipped suite.
  - Probe `receipts/probe_harness_partial.diff` delivers the crossing Pdelay_Resp and withholds its Follow_Up:
    - Head donor: `unanswered_at_drop=3`, and the named check passes (`receipts/probe_runs/partial-clean.run.log`). So the donor counts a partial exchange as lost, as IEEE 802.1AS-2020 11.2.19 requires.
    - `credit-on-step` ROM: `got=4 exp=3`, so it fails by name (`partial-credit-on-step.run.log`).
    - In both runs, `crossing exchange never completes` also fails. That is expected, because the probe delivers the response.
- **Why SUGGESTION:** R571-2-F1's required outcome asked for one case whose exchange does not complete, and that case is met. The donor's behaviour is correct.
- **Option:** add a third silent arm in which `answer_probe_` delivers only the Pdelay_Resp, and require `unanswered_at_drop == 3`.

## Prior findings at this head

| Finding | Severity | Status | Evidence at this head |
|---|---|---|---|
| R571-2-F1 | MINOR (Tests) | RESOLVED | See the first table below. The arm exists, the clean donor passes, R571-2's plant fails only the new named check, and the control passes |
| R571-2-RES-1 | RESIDUE | RESOLVED | The duplicate is now counted once in all four places. The count is updated for the new plant: four distinct defects, plus `credit-on-step`, makes five. Proof: the two deletion plants are byte-identical (`b7aef03b…`, `receipts/plant_identity.txt`), and the six defect ROMs give five distinct hashes (`receipts/arm_rom_sha256.txt`). The places: `GPTP_PLANE.md:141-151` (the page caps sentences at 10 words, so the clause is split, with its meaning unchanged); the disposition at `measure_test_evidence_readers.py:104-114`; the comment at `phc_step.py:79-81`; and the PR body (the `tb/verilator/gptp_plane/` row and the reproduction notes) |
| R571-2-RES-2 | RESIDUE | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632` carries R571-2's exact fix, and I checked its meaning independently. Dev `6178aa1bd` adds a `model_lint_waivers` list to `configs/endstation_ax7101_8x8.yaml` and carries it into the packed document. `gen_desc_image.py:532-545` reads `lint_waivers` only for the lint report, and nothing serializes it into image bytes. In the receipt diff, only the four 8x8 `config_sha256` fields change among configuration identities. The 1x1 rows also moved although the 1x1 config did not change, which fits a shared RTL cause |
| R571-2-S1, S2 | SUGGESTION | S1 carried; S2 taken | `credit-on-step` takes S2, a distinct second liveness plant. S1, the allowedLostResponses reading, is unchanged, and the new arm is consistent with the fourth-loss reading |
| R570-2-S1 | SUGGESTION | carried | No lens effect |
| R570-1 and R571-1 findings | various | RESOLVED (stand) | R570-2 and R571-2 resolved them at `d96b4a84`. The delta does not touch the capture gate, the receipt or the page figures, apart from the RES-2 sentence |

R571-2-F1 evidence (`receipts/campaign_head.log`, `receipts/campaign_runs/*.run.log`):

| Arm | Checks / failures | Unanswered requests at the asCapable drop (liveness arm; unanswered-crossing arm) | Result |
|---|---:|---|---|
| clean | 62 / 0 | 4; 3 | PASS |
| `nocease-control` | 62 / 0 | 4; 3 | PASS (control) |
| `credit-on-step` | 62 / 1 | 4; **4** | only `[FAIL] asCapable falls at the third unanswered request after an unanswered crossing request got=4 exp=3` |
| `liveness-not-marked`, `r571-no-liveness` | 62 / 1 each | **3**; 3 | only the fourth-request check fails |
| `stale-rate-window`, `crossing-exchange`, `never-rearm-measurement` | 62 / 12, 10, 11 | - | the named check fails |

Further checks on F1:
- **Plant identity:** R571-2's published `patch_credit_on_step.diff`, applied to the head donor, is byte-identical to the campaign's `credit-on-step/generate.py` (`be720649…`, `receipts/plant_identity.txt`).
- **The new check can fail:** harness probe `answered` (`receipts/probe_harness_answered.diff`) answers the crossing request again. With the clean ROM, the named check fails with `got=4 exp=3` (`receipts/probe_runs/answered-clean.run.log`).
- **The donor generator is unchanged:** the gitlink is `7dda9c3b` at both `d96b4a84` and head, and the campaign's `clean/generate.py` equals the head donor file.
- **The threshold is right:** under IEEE 802.1AS-2020 11.2.19, no response means no reset, and allowedLostResponses is 3 (11.2.13.4). So the crossing request is the first lost, and the third unanswered request after it is the fourth lost. That count exceeds 3 and clears asCapable. The page states this at `GPTP_PLANE.md:132-134`, and the PR body's F1 row says "the fourth lost in all".

## Lens results

```text
[R571] PASS Conformance — sim_phc_step.cpp:373-389, GPTP_PLANE.md:128-134, donor gen_gptp_ucode.py:1473-1497,1727-1737 — checked the new arm's expected count (3 after the crossing request, 4 lost) against IEEE 802.1AS-2020 11.2.19 / 11.2.13.4 and against the donor's judge, which clears asCapable at LOST_N_C+1; the clean donor meets it and also counts a partial exchange as lost (probe partial-clean); assignment items 1-2 met.
[R571] PASS RTL — gitlinks gptp-processor 7dda9c3b / protocol-processor 2ad2f845 (receipts/restore_check.txt), campaign clean/generate.py == head donor, phc_step.py:42-54 — the delta changes no RTL and no microcode; the credit path is reachable only through PDEPOCH on completion (:1727-1737); the plant's ROM room comes from deleting the cease rule, which is a fact about the generator, not shipped code.
[R571] PASS Robustness — sim_phc_step.cpp:336-356,373-389, probe_runs/* — the negative path is now pinned: a silent peer across a step with the crossing request unanswered; checked that each arm resets its probe and drop counters (:342-343) and restores answer_probe_ (:351); the donor handles the partial-exchange shape correctly (S1, no lens effect).
[R571] PASS Tests — phc_step.py:58-112, campaign_runs/*.run.log, probe_runs/answered-clean.run.log, plant_identity.txt, measure_test_evidence_check.log — each defect fails its named check; credit-on-step fails only the new check; nocease-control passes 62/62; the new check fails when the crossing request is answered; campaign rc 0 (8 of 8); evidence ratchet --check rc 0 with 0 unexplained readers.
[R571] PASS Docs — GPTP_PLANE.md:128-151, measure_test_evidence_readers.py:104-114, phc_step.py:63-64,79-87, SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632, PR body (receipts/pr707_view.json) — the arm, the counts (six named, five distinct, one positive control) and RES-2's attribution match the executed campaign, the ROM hashes and the gen_desc_image waiver path.
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `sim_phc_step.cpp:373-389`; `GPTP_PLANE.md:128-134`; donor `gen_gptp_ucode.py:1289-1299,1473-1497,1727-1737`; IEEE 802.1AS-2020 11.2.19, 11.2.13.4; probes `answered-clean`, `partial-clean` | R571-3 | 83239549a500604baabc65e443ed90876d65a36e |
| RTL | CLEAN | gitlinks (`restore_check.txt`); `phc_step.py:42-54` sources; donor ROM text identity (`plant_identity.txt`); `arm_rom_sha256.txt` | R571-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Robustness | CLEAN (S1 suggestion only) | `sim_phc_step.cpp:104,186,327-389`; `probe_runs/*` | R571-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Tests | CLEAN | `phc_step.py:58-112`; `campaign_head.log`; `campaign_runs/*`; `probe_runs/*`; `measure_test_evidence_check.log` | R571-3 | 83239549a500604baabc65e443ed90876d65a36e |
| Docs | CLEAN | `GPTP_PLANE.md:128-151`; `measure_test_evidence_readers.py:104-114`; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1632`; `gen_desc_image.py:532-545`; receipt diff `5603c353..83239549`; PR body | R571-3 | 83239549a500604baabc65e443ed90876d65a36e |

## Commands and receipts

- Verilator identity: `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version` reports `Verilator 5.050 2026-07-01 rev v5.050`.
- Campaign: `VERILATOR=<pinned> VERILATOR_JOBS=12 python3 phc_step.py --mutants --work <scratch>`. Result: rc 0 in 9 min 21 s, 357 MB peak (`campaign_head.*`).
- Probes: built with `scripts/make_harness_probes.py` and `scripts/build_probe.sh`, using the driver's flags. The three runs are in `probe_runs/`. Each exits rc 1 for the reason stated above.
- Ratchet: `python3 scripts/measure_test_evidence.py --check`. Result: rc 0, `0 <= 0 unexplained DUT-source reader(s)`.
- Full reproduction: `scripts/run_review.sh <clone> <packet> <verilator>`.

## Real limits

- The only suite run here is the step campaign: the clean arm, its control and six plants.
  - Not run: the `gptp_plane` `run` suite, `milan_dp` `gmstep`/`gmstep-mutants`, the 61-suite sweep, Yosys, lint, the capture SoC campaign and the vendor stages. The delta changes no input to them, apart from the RES-2 sentence.
  - The PR body's round-3 gate claims are the author's own. I re-executed only the campaign and the ratchet `--check`. The ratchet `--selftest` was not run.
- I did not test whether `gmstep` would catch `credit-on-step`.
- R571-2's MANIFEST lists `receipts/patch_credit_on_step.diff` with SHA-256 `ebbd76c1…`, but the copy fetched from the evidence branch hashes to `ec976ad4…`.
  - Its header carries a `$REVIEWS` path placeholder, so it was probably sanitized after hashing. I did not establish the cause.
  - I compared what the patch does instead: applied to the head donor, it produces the campaign's plant byte for byte.
- Clause readings come from the cited clause numbers and the donor's comments. This packet does not reproduce the standard's text.
- Exact-head hosted runs, as read (`hosted_check_runs.tsv`):
  - Completed with success: rtl-fast, docs-check, Yosys shards 0-3, and Verilator shards 0 and 3.
  - In progress: Verilator shards 1, 2 and 4.
  - Skipped: the Physical gPTP context, which is not hardware evidence.
  - Hosted and act acceptance belong to the manager.
- No manager source bank exists at this head, and none is claimed or inferred.
- Physical calibration was NOT RUN. Simulation results and field skips are not hardware proof.

## Pending manager duties

- Confirm Verilator shards 1, 2 and 4 at this exact head, and own hosted and act acceptance.
- Validate the current-dev merge candidate (source base `5603c353`, live dev `e8454e27`) with the builder and native banks, and link its receipts.
- Publish the donor before the parent (gitlink `7dda9c3b`), then handle the donor PR and the pin.
- Keep #621 open for the physical five-step bench repeat (`closingIssuesReferences` is `[]`).
- Decide on S1 here and on the carried suggestions (R571-2-S1, R570-2-S1, R570-1-S2/S5).

## Restore check

`receipts/restore_check.txt` shows the clone restored after all probes:
- HEAD is `83239549…` with tree `f3ddc144…`, and the index tree equals it.
- `git status --porcelain --untracked-files=all` is empty, and the index listing is byte-identical to the one taken at the start.
- The gitlinks are gptp-processor `7dda9c3b`, protocol-processor `2ad2f845` and verilog-axis `48ff7a7e`, and both checked-out submodules are clean.
- Every probe ran only on copies under the scratch directory.

R571-3 FINISHED
