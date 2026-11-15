[R835] POSITIVE - exact head 16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff

# R835-6: cleared-context internal delta review of PR #901 (issue #895), round 11

- **Head:** `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff`, tree `ed63495c5332415db216457abec37809737e0a0b`. The PR's live head on GitHub is the same commit.
- **Delta:** `1215bd82..16ba667d`, one commit. It changes 10 lines in 3 markdown files: `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md` and `sw/firmware/ctrl/plat/README.md`.
- **Source base:** `cec88385`. The PR targets `dev-soft-core`.
- **Author packet:** `review-evidence/895-r1/author-r11` at archive `de03c96e`. REVIEW READY is #895 issuecomment-6902951918.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. All five lenses are clean at this head.

- **R835-5-F1 (MINOR) is closed at its cause.** Each of the seven statements now gives this head's figure, or names its image by short commit. Each binding is true of the commit it names. My rerun of `f1_sites.py` reports 0 of 7 present.
- **R835-5-RS1, R835-5-RS2 and R836-5-RS1 are closed as written.**
- **Three new residues** (wording only) and one suggestion are listed below. None affects the verdict or any lens.

## The delta, line by line

Every bound figure was checked against the commit it names. The constants come from that commit's tree (`receipts/bound-commits.txt`). The rule figures come from the head's own `record_classes.rule` (`receipts/rule-arith.txt`).

| Site | Now reads | Checked against |
|---|---|---|
| `plat/README.md:110` | 680 B past 60.0 at this head; 392 B and 1,656 B at round 6's `bf0844f1` | The 60.5 granule is 133,120 B. The head image is 131,752 B: 680 B past 60.0, 1,368 B left. `bf0844f1`'s image is 131,464 B: 392 past, 1,656 left. Section 13's round 6 subsection (`:2624`) states 1,656 at that head. |
| `FR_NFR.md:383` (1) | 950 us, "the built slice on #894's head `07ed787e`"; there 8 ms held txL 48.43 … (past tense) | `07ed787e` is the #902 head merged in `056d619d`. In its tree, `CTRL_LOOP_SLICE_US` is 950 at one interface and `AECP_PACE_MS` is 8. |
| `FR_NFR.md:383` (2) | The pace "was 9 ms at round 7B's merge `7e3db6b9`" | `7e3db6b9` is the first commit of round 7B's first-parent run up to the 7B head `0c93071e`. `AECP_PACE_MS` is 9 there. |
| `FR_NFR.md:383` (3) | "the polls' base was 225 us, as at this head" | `poll_grade.STATED_US[1].base` is 225 at `0c93071e` and at the head. |
| `SPLIT_CONTROL_MEMORY.md:515` | "held 124,876 B" | R835-5-RS1, exactly. |
| `:2529` | "its bound at 1x1/1if was, on #894's head," | R835-5-RS2, exactly. At `07ed787e`, `AECP_QUEUED_MS` is 130 at one interface. |
| `:2595` | "950 us on #894's head, which its `ctrl_loop.h` states" | `07ed787e`'s slice is 950. This is a #894 passage, which the preface at `:1170` attributes to #894's head. |
| `:2603` | 245/220 us at round 6's `bf0844f1`; at this head the dearest edit is 255, paced 300, ordinary 225 | 23,306 and 20,525 cycles give 245 and 220 (the round 6 subsection, `:2621`). 23,877 cycles (the paced REMOVE_AUDIO_MAPPINGS in `author-r10/receipts/classes/plants/summary.md:9`) gives 255. 28,288 gives 300 and 21,187 gives 225 (the section 13 table at `:2711-2712`). |
| `:2604` | 9 ms at round 5's head `62298ab5` (and 9 at this head) | `AECP_PACE_MS` is 9 at `62298ab5` and at the head. |
| `:2605` | 33.69 and 94.99 at round 7A's `4c9757ee`; 34.00 and 104.25 at this head | Round 7A's subsection states 33.69 and 94.99. The head's subsections state 34.00 and 104.25. These match my R835-5 flip logs at `1215bd82`, and no image input has changed since. |
| `:2606` | 1,656 at round 6's `bf0844f1`; 1,368 at this head | The same as `plat/README.md:110`. |
| `:2618` | "Its pass at round 6's `bf0844f1`" | This line is inside the subsection marked as round 6's (`:2613`). |

- **The three phrase-sweep fixes the packet names** are `:2595`, `:2604` and `:2618`. They are present and correct.
  - The brief said "four further statements". I count three on the design page. FR_NFR's two added bindings (`7e3db6b9`, and "225 us, as at this head") would be the fourth if counted separately.
  - All of them are correct, so the count makes no difference to the result.
- **Anchors.** The added links resolve to existing headings: `#the-record-classes-graded-895` (`:2703`), `#the-rules-slice-built-895` (`:2628`) and `#the-composition-measured-again-895` (`:2611`). The gates below pass.

## My sweep of the same pages

- **The phrase sweep** (`scripts/phrase_sweep.py`, `receipts/phrase-sweep.txt`) covers every markdown line the PR adds or changes against `cec88385`: 832 lines in 13 files, 81 hits of "this head", "the head", "at the head", "head's", "now", "currently" and "today".
  - Every hit outside #894's passages (`:2030-2596`, which the `:1170` preface attributes to #894's head) is listed with its subsection.
  - Each one is either this head's figure, bound to a named round or commit, or about behaviour rather than a figure. The figure hits are:
    - `:2683` and `:2687`: 900 us, 140 ms and 1,368 B;
    - `:2732`: 14.72 and 21.11 ms;
    - `:2733`: 34.00 and 104.25 ms;
    - `FR_NFR.md:390`: 21.11 ms;
    - `plat/README.md:110`: 680 and 1,368 B.
  - The two base-README "this head's" lines in the packet's inventory (`ctrl_service_budget/README.md:1525`, `ctrl_service_hooks/README.md:314`) are not among the PR's added lines. That matches the known scope limit.
- **The figure sweep.** I swept the PR-added lines of FR_NFR and of every touched README and design page outside SPLIT_CONTROL_MEMORY for the superseded figures: 1,656, 1,864, 392 B, 245 us, 33.69, 94.99, 48.43, 127.21, 28.95, 2,029, 2,022, 130 ms, 99 ms, 98 ms and 950 us.
  - Each hit is attributed to #894's head, past tense, or a comparison with a named figure: FR_NFR `:383`, `:385`, `:387`, `:389`; `aecp/README.md`; `srp/README.md`; `ctrl_service_budget/README.md`.
- **The packet's inventory.** Its counts are attributed 86, historical 61, this head's 5 and unrelated 49, which makes 201 with 0 unclassed.
  - I spot-checked the "this head's" rows (`:2672`, `:2673`, `:2694` ×2, `:2701`) and the section 5 rows at `:337` and `:386`. Each is correct.
  - One class label is wrong; see R835-6-RS3. That does not change the inventory's conclusion.

## Findings

No BLOCKER, MAJOR or MINOR.

### RESIDUE (purely wording; does not affect the verdict or any lens)

- **R835-6-RS1 — Docs — PR #901 body, the "Round 11" table, row R835-5-S2, evidence cell.**
  - It cites `round11/scripts/phrase_sweep.py`. That is a lane-local path, not a public one.
  - The published script is `review-evidence/895-r1/author-r11/scripts/phrase_sweep.py` on the `895-review-evidence` branch (archive `de03c96e`).
  - **Exact fix:** "`round11/scripts/phrase_sweep.py`" -> "`review-evidence/895-r1/author-r11/scripts/phrase_sweep.py` (`895-review-evidence`)".
  - The same lane-local prefix also appears in the generated `receipts/INDEX.md` header ("Generated by round11/scripts/index.py"). Optionally restate it the same way the next time the packet is generated.
- **R835-6-RS2 — Docs — PR #901 body, "Linked Issue / roles", the `[R835]` line.**
  - It names R835-6 without its start link. The start is public at issuecomment-6902981741. This is the same class as R836-5-RS1.
  - **Exact fix:** "R835-6, the one delta reviewer of round 11." -> "R835-6 [started](https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6902981741), the one delta reviewer of round 11." Add its verdict link once that verdict is published.
- **R835-6-RS3 — Docs — `author-r11/receipts/docs/superseded-inventory.md:271-273`.**
  - These rows class three `950 us` hits on `FR_NFR.md:383` as "attributed: #894's head". They are #895's own history, all in the past tense:
    - "the loop was built at the slice rule's 950 us" (#895's ruling, item 1);
    - "at 950 us the last queued notice was 134.74 ms";
    - "135.43 ms at 950 us".
  - Only the first `950 us` hit on that line (`:270`) is #894's head's.
  - The tracked text is right and the inventory's "none stated as this head's" still holds. Only the class label of three receipt rows is wrong.
  - **Exact fix:** class rows 271-273 "historical: past tense or a named round or commit" at the next regeneration.

### SUGGESTION (optional; no effect on coverage)

- **R835-6-S1 — Docs — `SPLIT_CONTROL_MEMORY.md:2603`.**
  - "at this head the dearest edit is 255 us" links to the record classes section. That section states the paced class's dearest record (300 us) but not the dearest edit.
  - The 255 us (23,877 cycles, a paced REMOVE_AUDIO_MAPPINGS) is stated only in the round 10 packet (`author-r10/receipts/classes/plants/summary.md:9`).
  - Optional: add the edit's 23,877 cycles to the record classes section, or cite that receipt, so the link supports every figure in the clause.
- **Retained, optional:** R835-5-S1 (publish the graded legs' `read_leg` records) and R835-4-S3 (a plant that drops `gate_seen` from the gate's early return). Their premises are unchanged, since no firmware or packet scope moved.

## Prior findings at this head

| Finding | State | Evidence at `16ba667d` |
|---|---|---|
| R835-5-F1 MINOR; Docs (seven statements give an earlier image's figure as this head's) | **CLOSED** | `receipts/f1-sites.txt`: 0 of 7 present. My script is byte-identical to the packet's copy, and the author's receipt matches mine. Each new binding is checked in the table above. The inventory's figure list now has 392 B, 245, 220, 33.69, 94.99, 1,656 and 1,864, with 0 unclassed. The phrase sweep R835-5-S2 asked for was run, by the author and again by me. |
| R835-5-RS1 RESIDUE; Docs (`:515` "holds") | **CLOSED** | "held 124,876 B", exactly. |
| R835-5-RS2 RESIDUE; Docs (`:2529` "is") | **CLOSED** | "its bound at 1x1/1if was, on #894's head,", exactly. |
| R836-5-RS1 RESIDUE; Docs (roles "(next)") | **CLOSED** | The only "(next)" left in the PR body is the Round 11 table quoting its own fix. R835-5 and R836-5 each link their start and verdict. R835-6's missing start link is a new instance: R835-6-RS2. |
| R835-5-S1, R835-4-S3 SUGGESTION | Retained, optional | As above. |
| R835-5-S2 SUGGESTION | Taken | The packet's `scripts/phrase_sweep.py` and the inventory's phrase table. |
| All earlier closures (R836-4-F2, R835-4-F1, R836-4-F1, R835-4-F2 and the residues R835-5 lists) | Carry | No non-markdown path changed (`receipts/delta-identity.txt`), so nothing they depend on moved. The R835-5 closures stand. |

## Gates and integrity

All of these were run by me in this clone at the head:

- **Delta scope** (`receipts/delta-identity.txt`): the delta has 3 paths, all `M`, all mode 100644 to 100644, with 0 non-markdown paths. The gitlinks are identical at `1215bd82` and the head.
  - The only tracked consumer of these pages is `sw/litex/test_ctrl_memory.py:866`, which reads section 3 of SPLIT_CONTROL_MEMORY. That section's bytes are identical, by sha256, at `1215bd82` and the head.
  - So no image, test or gate input changed.
- **Doc gates:**
  - `docs_check.py`: rc 0, 0 findings across 219 md files.
  - `check_doc_style.py`: rc 0.
  - `check_doc_paths.py`: rc 0, 1,166 cited paths resolve.
  - `check_gptp_docs.py`: rc 0.
  - `git diff --check`: rc 0 for `cec88385..HEAD` and for the delta.
- **The em-dash gate** returned rc 2 here, because its pinned renderer is not installed. My direct scan of the delta's added lines finds 0 em dashes (`receipts/em_dash_added.txt`). The author's docs workflow receipts report the gate (`docs-gates-0` gate_8) at rc 0.
- **Author gate receipts.**
  - Packet integrity (`receipts/packet-verify.log`, `scripts/verify_r11.py`): all 106 INDEX rows match their bytes, with no unlisted file. All 124 files match the archive `MANIFEST.json`'s published sha256.
  - Head binding: every `.rc` file is 0 (78 files). The driver logs and tree-after files name `16ba667d5fdb…` (6 hits).
  - `firmware-unit` reports failed 0, with steps 1, 3, 7, 10, 11 and 12 at rc 0. Step 12 is `fw_coverage.py --selftest` and `--check`.
  - `verify-docs.md` reports 61 steps ran, 34 not run with a reason, and 0 bad.
- **Why I did not rerun the coverage ratchet.** It reads `sw/firmware/gtest/README.md` and the firmware sources, and the delta touches none of them. So I relied on the author's exact-head receipt rather than rerunning it.
- **The comment rule** does not apply: the delta adds no source comment and changes no source file.

## Lens results

```text
[R835] PASS Conformance — docs/reference/FR_NFR.md:383,387 (3.4.1) at 16ba667d, receipts/bound-commits.txt — the normative clause's slice, pace, base and bound statements are each bound to the commit whose constants they are (07ed787e: 950 us/8 ms/130 ms; 7e3db6b9: 9 ms; head: 900 us/9 ms/140 ms/base 225), and no clause states a superseded value as current; no requirement, wire field or timing rule changed
[R835] PASS RTL — receipts/delta-identity.txt (3 markdown paths, 0 non-markdown, gitlinks identical, modes unchanged) — no RTL, firmware, mailbox contract, submodule or image input changed; the prior RTL coverage carries since nothing it depends on moved
[R835] PASS Robustness — receipts/delta-identity.txt, sw/litex/test_ctrl_memory.py:866 (section 3 sha256 identical at 1215bd82 and head) — no input-handling, reset, timeout or configuration-dependent path changed; the only gate that parses the edited page reads an unchanged section
[R835] PASS Tests — receipts/f1-sites.txt (0 of 7), receipts/packet-verify.log (106/106 INDEX, 124/124 manifest), author-r11 receipts/gates (78 rc files 0, firmware-unit failed 0, head-bound) — the verification R835-5-F1 named fails on the old text (7 of 7 at 1215bd82, receipts/f1-sites-1215bd82.txt) and passes here; no test, plant or harness changed, and the author's exact-head gate receipts are intact
[R835] PASS Docs — the full delta (SPLIT_CONTROL_MEMORY.md:515,2529,2595,2603-2606,2618; FR_NFR.md:383; plat/README.md:110), receipts/phrase-sweep.txt (81 hits over 832 PR-added lines), receipts/docs_check.log, check_doc_style.log, check_doc_paths.log, check_gptp_docs.log — every changed figure is this head's or bound to the right commit; no superseded figure is stated as current on the swept pages; residues RS1-RS3 are wording only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `FR_NFR.md` 3.4.1 (`:383`, `:387`, `:390`), `aecp_mbx.h:57,75`, `ctrl_loop.h:282,377`, `poll_grade.py:99`, `receipts/bound-commits.txt` | R835-6 | `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff` |
| RTL | CLEAN | `receipts/delta-identity.txt` (no RTL, firmware or gitlink change) | R835-6 (the earlier RTL coverage carries: nothing in scope changed) | `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff` |
| Robustness | CLEAN | `receipts/delta-identity.txt`, `sw/litex/test_ctrl_memory.py:866` against section 3's unchanged bytes | R835-6 (carries R835-5's coverage; no path in scope changed) | `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff` |
| Tests | CLEAN | `receipts/f1-sites.txt`, `receipts/packet-verify.log`, author-r11 `receipts/gates/` and `receipts/units/` | R835-6 | `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff` |
| Docs | CLEAN (residues RS1 to RS3 are carried, not blocking) | the full markdown delta, `receipts/phrase-sweep.txt`, the doc gate logs, the PR body's roles and Round 11 sections, author-r11 `superseded-inventory.md` | R835-6 | `16ba667d5fdb7b599b9d9459958fd0d7bb6bbdff` |

## Real limits

- **Delta review only.** Code the delta does not touch keeps its R835-5 lens verdicts at `1215bd82`, which is an ancestor of this head that nothing in any lens's code scope has touched since. I ran no parent, PP, gPTP, Yosys, builder, harness or firmware bank.
- **I did not rerun `firmware-unit` or the coverage ratchet.** I proved that their inputs are unchanged, and checked the author's exact-head receipts.
- **The em-dash gate did not run here** (missing renderer, rc 2). It was replaced by a direct scan of the added lines. The author's receipt reports the gate at rc 0.
- **The archive commit `de03c96e` is unsigned in git** (GitHub reports `unsigned`). The packet's integrity rests on the INDEX and manifest hashes, which I verified.
- **The head's row figures** (34.00, 104.25, 14.72, 21.11, 136.65) rest on my R835-5 flip logs at `1215bd82`. They carry to this head because no image input changed. I did not rerun the flip check.
- **Hosted checks at this head were in flight when I looked** (`receipts/hosted-checks.json`): 9 success, 1 skipped, 19 in progress and 21 queued. I judged none of them. The manager owns hosted and act acceptance.
- **No manager source bank ran at this exact head, and none is claimed.**
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone state** (`receipts/clone-integrity.txt`): HEAD and index `write-tree` both equal tree `ed63495c`. There are 0 status lines, including untracked and ignored files, and the six gitlinks are unchanged. No probe edited the clone.

## Pending manager duties

- Carry R835-6-RS1, RS2 and RS3 to the residue checklist.
- Confirm hosted and act acceptance at `16ba667d`, distinguishing executed jobs from skipped contexts.
- At the merge turn, build and validate the current-dev merge candidate, source base `cec88385` against live dev `6b66f66d`. Run the builder and the native banks, and link their receipts on the PR.
- Keep 8x8/1if out of scope as ruled. Acceptance 6 (bench) remains hardware-owned.

R835-6 FINISHED
