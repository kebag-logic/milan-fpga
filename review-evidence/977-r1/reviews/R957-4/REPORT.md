[R957] POSITIVE - exact head 3256d1d21e525e564eb92d1cf721750ddf44fde2

# R957-4: internal independent re-review of PR #993 (#977), round 12 (`3181a3ec..3256d1d2`)

Tree `6810c12ebf0f060a9557e3fbe356a99cffef8c2a`. This is a narrow round. It covers:

- my round-3 findings (PR comment 7229653191): F1, F2, R1 to R4 and S1;
- the external round-3 F1, R1 and R2 (PR comment 7229617575).

Code the delta does not touch keeps its prior lens verdict. All five lenses were applied to the delta.

**The ceiling, stated plainly.** This verdict is judged against the 8x8/1if flip ceiling of **0.79** that the last commit `3256d1d2` sets, citing "owner decision pending". **At 0.77 the PR does not pass.** At this head with `FLIP['8x8/1if']` at 0.77, the 8x8/1if flip check returns "8x8/1if: the load 0.782 at the pin is over the flip ceiling 0.77" (`receipts/probe-head-3256d1d2.txt`).

The manager's decision, item 4 (#977 comment 7229657853), also applies: the ceiling commit must cite the owner's published answer, never "pending", before merge. So this head is not mergeable as it stands, whatever this verdict says. It needs one of two things:

- the owner approves 0.79 and the citation is amended to that answer; or
- the owner refuses, `3256d1d2` is reverted, and the PR fails 8x8/1if as above.

The verdict covers everything except that owner answer.

## 1. What I checked, and how

**The delta.** It is 4 commits and 8 files:

- `flip_grade.py`, `load_grade.py`, `load_deliveries.py` and `selftest_mutants.py`;
- the ctrl_service_budget README;
- `srp_deliver_mutants.py`, docstring only;
- `SPLIT_CONTROL_MEMORY.md` section 13 and `FR_NFR.md` 3.4.1.

I read the delta in full before the prior findings.

**The packet.** I checked `review-evidence/977-r1/author-r12` at evidence commit `6208d963`:

- All 22 files match the published `MANIFEST.json` `published_sha256`. None is unlisted and none is redacted (`receipts/packet-verify-6208d963.txt`).
- The evidence commit is not GPG-signed (GitHub reports `unsigned`). Integrity rests on the manifest hashes, which I verified.

**ELF identity.**

- The ELF receipt pairs 80 paths at `3256d1d2` with 80 at `25ff0632`. The paths are the same and every sha256 is equal (recomputed from the receipt's two tables).
- The only change under `sw/`, `hdl/` and `third_party/` in `3181a3ec..3256d1d2` is the docstring of the test-only `sw/firmware/ctrl/test/srp_deliver_mutants.py`. It is read only by `srp_mutants.py` (the test campaign) and is no product build input.
- The submodule gitlinks are identical at both heads (`receipts/tree-checks-3256d1d2.txt`).
- So the product ELFs at this head equal round 11's, and the receipt's 80 of 80 against `25ff0632` stands.

**My own probes.** `probe_r957_4.py` runs in memory, at the head and at the pre-fix tree `3181a3ec`. The pre-fix tree is a scratch extraction with the same submodule contents. The results are `receipts/probe-head-3256d1d2.txt` and `receipts/probe-prefix-3181a3ec.txt`.

| Probe | Head `3256d1d2` | Pre-fix `3181a3ec` |
|---|---|---|
| `flip_checks()` / `ceiling_checks()` with nothing planted | no failure / no failure | no failure / no failure |
| 8x8/2if at 0.71, `flip_checks()` | fails on "the flip ceilings not 0.70 at 8x8/2if and 0.79 at 8x8/1if" | **no failure** (the escape was swallowed) |
| 8x8/2if at 0.71, `ceiling_checks()` | fails on "a held point not held" and on the ceilings control | fails on "a held point not held" only |
| An escape `flip_grade.controls` does not name | `flip_checks()` fails it as unnamed | **no failure** |
| An escape `load_grade.controls` does not name | `ceiling_checks()` fails it as unnamed | **no failure** |
| 8x8/1if flip check at 0.79 / at 0.77 | PASS / FAIL, load 0.782 | n/a |
| `over()` at 0.790 / 0.791 / 0.7900001 against 0.79 | False / True / True | n/a |
| `FLIP` alone at 0.80; `FLIP` and `RULED_FLIP` both at 0.80 | both controls escape; the edge control still escapes | n/a |
| `DELIVERY_US` 8x8/1if at 155 / 159 / 160 / 125 us | refused / refused / accepted / refused | n/a |
| `DELIVERY_US` 1x1/1if at 195 us | refused ("under its measurement's 200 us by the rule") | n/a |
| `load_deliveries.controls`, `load_grade.findings` | none escaped, none found | none escaped, none found |

Two things follow from the head's adapter results:

- Every control the load gate plants (32) and every one the flip check plants (628) is refused. This reproduces `load_grade --selftest` and `flip_grade --selftest` through the adapters.
- `load_grade.findings` is empty, so 1x1/1if holds its 0.70 in both columns.

The CLI `--selftest` paths already exited 1 on any escape, named or not (`load_grade.py:975-981`, `flip_grade.py:478-484`). The defect the external F1 named was in the two adapters only, and both are now fixed.

**Arithmetic on the deliveries figures.**

- At 8x8/1if the dearest record is the answering-ports swap. Its excess is 135,935 cycles over its after-window median of 12,089. Divided by 9 sinks (the (1, 9, 9) shape) that is 15,104 a sink. By the decision's rule `5·ceil(c/100·1.05/5)` that is 160 us.
- At 1x1/1if the dearest record is answering-ports `register_both_owed`: 18,778 cycles a sink, 200 us.
- The figures beside them check by the same rule: 11,573 → 125 us, 13,642 → 145, 18,076 → 190 and 18,765 → 200.
- The 8x8/1if load is 0.76614 without the term, plus 160 · 9 · 3 / 270,000 = 0.016, which gives 0.78214. That is at least the 0.7806 lower bound my round 3 derived, and it is consistent with it.
- The per-record table (`meas/deliv-8x8-1if-e59cf6ea.txt`) shows a 19-pass window (2 × 9 + 1). After it come 58 ordinary passes in the 50 ms after the window. The swap is a single-record group, so no later record's window falls inside its baseline.

**Hosted evidence.** There are no check runs and no workflow runs at `3256d1d2` (both counts 0; the PR is a draft). I claim no hosted evidence. The manager owns hosted and act acceptance.

## 2. Prior findings at this head

| Finding | Status | Evidence at `3256d1d2` |
|---|---|---|
| R957-3-F1 MAJOR (Conformance, RTL, Tests, Docs) | **Resolved** | See the notes after this table. |
| R957-3-F2 MINOR (Conformance, Docs) | **Resolved** | #977 comment 7229657853 is public. It names option (a), the after-window baseline and its window, and the floor. `SPLIT_CONTROL_MEMORY.md:2561` and `FR_NFR.md:427` link it. The source sites name it: `load_grade.py:13,374`, `load_deliveries.py:3` and `flip_grade.py:66`. How they name it is residue R957-4-R1, not a finding. There is no remaining link to 7226275798 and no remaining "manager's decision of 2026-11-27" (`receipts/tree-checks-3256d1d2.txt`). |
| R957-3-R1 RESIDUE | **Closed** | `load_grade.py:374-385` describes the method. "deliv11" appears nowhere in sw/, tb/ or docs/. |
| R957-3-R2 RESIDUE | **Closed** | `tb/verilator/ctrl_service_budget/README.md:244` carries the `deliveries` exception in the exact words asked. |
| R957-3-R3 RESIDUE | **Closed** | The live PR body, line 18, reads "[the internal review](…7229653191) and [the external review](…7229617575)". |
| R957-3-R4 RESIDUE (packet) | **Retained** (residue, manager) | The round-12 index (`author-r12/receipts/INDEX.md`) carries a correct publication note for its one `.gz` row. The round-10 and round-11 index notes the handoff says were appended are not published at `6208d963`: no "supersed", "publication note" or 2026-11-28 line in either. Exact fix: publish the two appended notes with the next packet. |
| R957-3-S1 SUGGESTION | **Taken** | `srp_deliver_mutants.py:15-16`. It matches `test_ctrl_firmware.py:249-250`, which passes every name without the drain prefix to the `srp-mutants` campaign. |
| External round-3 F1 MINOR (Tests, Robustness) | **Resolved** | See the notes after this table. |
| External round-3 R1 RESIDUE | **Closed** | The same live PR body line 18. There are no duplicated role words. |
| External round-3 R2 RESIDUE (packet) | **Retained** (residue, manager) | Same cause and fix as R957-3-R4. |

**R957-3-F1 in detail.**

- The baseline is the one the decision accepts: the median polls base of the ordinary passes in the 50 ms after the delivery window. `load_grade.py:374-385` and `SPLIT_CONTROL_MEMORY.md` section 13 state the window and the reason.
- `DELIVERY_US` is 160 us at 8x8/1if (`:386`) and 200 us at 1x1/1if. `DELIVERY_MEASURED` (`:387`) holds the measured figures: 15,104 and 18,778 cycles.
- The 50 ms and 500 ms pre-record medians are recorded beside it in `DELIVERY_BESIDE` (`:388`) and are not graded.
- The gate's floor is `rule_us(DELIVERY_MEASURED)` (`load_grade.py:701-703`), and its control plants a cost 5 us under it (`load_deliveries.py:35-38`). My probe refuses 155 and 159 us and accepts 160 us.
- The re-derived 8x8/1if load is 0.78214. It is over 0.77, so it went to the owner (decision item 3), as F1 required.

**External round-3 F1 in detail.**

- The two control names are built from `RULED_FLIP` and `EDGE_1IF` (`flip_grade.py:70-74`), and `CONTROLS` uses the same names.
- Both adapters fail any escape they do not name: `flip_grade.py:463-464` and `load_grade.py:963-964`.
- With 8x8/2if at 0.71, my probe fails the ceilings control through `flip_checks()` and through `ceiling_checks()`. At `3181a3ec` the same mutation failed nothing in `flip_checks()`.
- New mutant: `selftest_mutants.py:540` (the unnamed escape). The harness log at line 2235 shows it caught.

## 3. Findings of this round

No BLOCKER, MAJOR or MINOR finding is open.

### Residue (wording only: no figure, test, code path or verdict changes; for the residue checklist)

- **R957-4-R1 RESIDUE (Docs)**: four new source-comment instances of an issue-comment ID, which the owner's comment rule forbids. The sites are listed below, each with its exact fix. The decision stays linked, by URL, from `SPLIT_CONTROL_MEMORY.md:2561` and `FR_NFR.md:427`, where links are allowed.
  - `tb/verilator/ctrl_service_budget/load_grade.py:13`
    - Reads: "(#977, comment 7229657853, the manager's decision)"
    - Fix: "(#977, the manager's decision on the deferred deliveries, linked from SPLIT_CONTROL_MEMORY.md section 13)"
  - `load_grade.py:374`
    - Reads: "(#977, comment 7229657853, the manager's decision)"
    - Fix: "(#977, the manager's decision on the deferred deliveries)"
  - `load_deliveries.py:3`
    - Reads: "#977, comment 7229657853, the manager's decision"
    - Fix: "#977, the manager's decision on the deferred deliveries"
  - `flip_grade.py:66`
    - Reads: "a load term since #977, comment 7229657853, owner decision pending"
    - Fix: "a load term since the manager's decision on #977's deferred deliveries; owner decision pending"
- **R957-4-R2 RESIDUE (Docs)**: the live PR body, line 61 ("The deliveries term (`71503e5a`)").
  - It reads "internal review F1, option (a)". That is the round-2 internal finding, but the label is the same one line 20 uses for the round-3 internal F1, so a cold reader cannot tell them apart. The label scrub produced it; the packet's PR-BODY.md said R957-2-F1.
  - Exact fix: "the round-2 internal review's F1, option (a)". PR text may name rounds.
- **R957-4-R3 RESIDUE (Docs)**: `load_grade.py:380-381`.
  - "... plus 5 %, rounded up to 5 us (DELIVERY_MEASURED, the gate's floor: a cost stated under it is refused)" attaches `DELIVERY_MEASURED` to the ruled figure. The table holds the unruled cycles; the floor is `rule_us` of them (`:701`).
  - Exact fix: "... plus 5 %, rounded up to 5 us; DELIVERY_MEASURED holds the cycles, and their figure by the rule is the gate's floor: a cost stated under it is refused".
- **R957-3-R4 / external round-3 R2**: retained from section 2. Publish the round-10 and round-11 index notes.

### Suggestions (optional; they do not affect coverage)

- **R957-4-S1 (Tests)**: the load gate's own unnamed-escape branch (`load_grade.py:963-964`) has no planted mutant. My probe shows it fires ("the load gate names every escape it returns: probe: unnamed"), but only the flip-side branch is guarded permanently (`selftest_mutants.py:540`). A sibling mutant would hold it, for example `'load: an escape the load gate does not name'`, patching `load_grade.controls` to append an unnamed name.
- **R957-4-S2 (Tests)**: the mutant `"flip: 8x8/2if's ceiling at 0.71"` (`selftest_mutants.py:539`) is killed through "the load gate refuses a held point not held" (harness log line 2218).
  - That check fails at `3181a3ec` too (`receipts/probe-prefix-3181a3ec.txt`), so this mutant alone would not have caught the adapter defect. The unnamed-escape mutant at `:540` does discriminate.
  - Optionally, run the 0.71 plant against `flip_grade.flip_checks()` alone, or require the ceilings control's name in what fails.

## 4. Lens results at this head

| Lens | Result | Artifact | What was checked, against what |
|---|---|---|---|
| Conformance | PASS (judged at the 0.79 ceiling; the owner's answer is pending, see the opening section) | `load_grade.py:9-13,374-388,690-704`; `flip_grade.py:24-26,62-74`; #977 comment 7229657853 items 1-4 | Option (a), the after-window baseline, the rule, the beside figures and the floor all follow the decision. The 8x8/1if load of 0.78214 is within 0.79 and over 0.77, which is stated plainly. 1x1/1if is 0.533 of 0.70. Item 4's "never pending before merge" is a merge precondition the manager carries. |
| RTL | PASS | `git diff --name-only 3181a3ec..3256d1d2 -- sw hdl third_party` (one test docstring); the gitlinks; `author-r12/receipts/elf-identity-3256d1d2.txt` (80 of 80) | No HDL or firmware product source changed. The ELF identity with `25ff0632` is verified from the receipt and from the change set. The firmware behaviour the load term costs (`ctrl_app_srp.c` `deliver`) is unchanged, so round 3's verdict on it stands; its F1 was a costing defect, now resolved. |
| Robustness | PASS | `receipts/probe-head-3256d1d2.txt`, `receipts/probe-prefix-3181a3ec.txt` | The ceiling edge passes at 0.790 and fails at 0.791 and 0.7900001. `FLIP` drift is caught alone and alongside `RULED_FLIP`. Unnamed escapes are caught in both adapters. The floor holds at 155, 159 and 160 us, and at 195 us for 1x1/1if. The prior-figure regression (125 us) is refused. |
| Tests | PASS (S1 and S2 are optional) | `selftest_mutants.py:539-541`; `load_deliveries.py:14-39`; `flip_grade.py:200-205,458-464`; `load_grade.py:955-965`; harness log lines 2218 and 2235 | Every new or renamed control can fail for its defect, which the pre-fix comparison shows. The adapters report every failure. Self-tests reproduce through the adapters: 32 load-gate controls and 628 flip controls. `load_deliveries` has no escape. |
| Docs | PASS (R1 to R3 and R4 are residue) | `SPLIT_CONTROL_MEMORY.md:2548,2561` (section 13); `FR_NFR.md:427`; the ctrl_service_budget `README.md:244`; `srp_deliver_mutants.py:13-16`; the live PR body; `author-r12/REVIEW-READY.md` | The figures 0.782, 0.766, 0.779/0.781, 0.533, 15,104/160 and 18,778/200 match the probes and the receipts. The decision is linked. The superseded round-11 figures are marked as superseded in the PR body. |

## 5. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN, judged at the 0.79 ceiling (pending the owner's answer; FAILS at 0.77) | decision 7229657853; `load_grade.py` deliveries term and floor; `flip_grade.py` FLIP; section 13; FR_NFR 3.4.1; load-flip receipt; own probe | R957-4 | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| RTL | CLEAN | product change set (none); submodule gitlinks; 80-ELF identity receipt against `25ff0632` | R957-4 | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Robustness | CLEAN | ceiling edge, drift and escape probes; floor probes at both points | R957-4 | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Tests | CLEAN | new mutants; adapters before and after the fix; load_deliveries controls; harness self-test log | R957-4 | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |
| Docs | CLEAN (residue R957-4-R1 to R3 and R957-3-R4 carried to the checklist) | section 13; FR_NFR; README; docstrings; PR body; packet | R957-4 | 3256d1d21e525e564eb92d1cf721750ddf44fde2 |

## 6. Real limits

- **Raw logs.** I did not re-derive `DELIVERY_MEASURED` from raw harness logs, because they are not published. The figures rest on the two hash-verified per-record receipts and the published `deliv12.py`. I checked their arithmetic and the window and baseline logic in the script, but I did not re-run them.
- **Gates not re-run.** I did not rebuild any ELF, and I ran no firmware gate, harness `run.py --self-test`, Verilator, Yosys or docs workflow. I rely on the author's published receipts at this head, plus my in-memory gate and control probes.
- **No hosted evidence.** There is no hosted run at this exact head, and I claim no manager source bank.
- **Calibration.** Physical calibration has not been run. Field skips are not hardware proof.
- **Signing.** The evidence commit is unsigned. The packet's integrity is the manifest-hash binding only.

## 7. Pending manager and owner duties

- **The owner's answer on 0.79** for 8x8/1if. If approved, amend `3256d1d2`'s citations, replacing "owner decision pending" with the published answer:
  - `flip_grade.py:24-26,64-66`;
  - `FR_NFR.md:427`;
  - `SPLIT_CONTROL_MEMORY.md` section 13.
- **If the owner refuses,** revert `3256d1d2`. The PR then fails 8x8/1if at 0.782 > 0.77 and waits for #1025.
- **Before merge,** confirm that no "pending" citation remains (decision item 4).
- **Residue.** Publish the round-10 and round-11 index notes (R957-3-R4 / external R2). Carry R957-4-R1 to R3 to the residue checklist.
- **Merge turn.** Build and validate the current-dev merge candidate: source base dev-soft-core, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. Post its receipts, and own hosted and act acceptance on the exact PR head after it is marked ready.

## Receipts (MANIFEST.sha256)

- `probe_r957_4.py`: the in-memory probes. Run as `python3 -I probe_r957_4.py TREE`.
- `verify_packet.py`: the manifest and ELF-receipt check. Run as `python3 -I verify_packet.py MANIFEST.json PACKET_DIR author-r12/`.
- `receipts/probe-head-3256d1d2.txt` and `receipts/probe-prefix-3181a3ec.txt`.
- `receipts/packet-verify-6208d963.txt`.
- `receipts/tree-checks-3256d1d2.txt`: the stale-name and residue search, the change set, the gitlinks, the hosted counts, the signature status and the index-note check.

The review clone was restored and verified at exact head bytes:

- `git write-tree` gives `6810c12e…`, matching HEAD's tree.
- The worktree and the index are clean against HEAD.
- `git ls-files -s` and `git ls-tree -r HEAD` hash equal.
- The submodule gitlinks are unchanged.
- The bytecode caches my probes created were removed, and there are no untracked or ignored files.

R957-4 FINISHED
