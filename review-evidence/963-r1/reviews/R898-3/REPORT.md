[R898] POSITIVE - exact head a18f0996f4b1b654a232dfe56fa64ee7ecaf697e

# R898-3: internal independent review of PR #984 (#963), a narrow re-check

- **Head:** `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e`, tree `a897a1e08c1cd4b63c37b0e5625b819d4649d568`.
- **Source base:** `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`.
- **Previously reviewed head (R898-2):** the same `a18f0996`. No source byte has changed.
- **Delta since R898-2:** text only.
  - The live PR #984 body was corrected in two places.
  - A correction comment was posted on #963 (issuecomment-7101302165).
  - The corrected body was archived at `review-evidence/963-r1/author-r2b/PR-BODY-corrected.md` in evidence commit `975fdfd3b70343327f3fa28253cd79b6ffe1b4b4`.

## 1. Verdict summary

- **R898-2 F1 (MINOR, Tests, Docs) is resolved.** The figure was "a further 4,000 edits carry the new mapping". The PR body now carries the required text word for word. #963 has an explicit public correction of the round-2 REVIEW READY.
- **R898-2 RES-1 (RESIDUE, Docs) is resolved in the PR body,** with the exact fix that was asked for.
- **Body check:** the live PR body is byte-identical to the archived `PR-BODY-corrected.md`. Its sha256 is `5a54e35b…183d`, and its git blob is `779b4a46…` in both places.
- **Figures:** both corrected figures match the published probe logs. They also match an independent replay, written for this round, of the test's own seeded draws and reference model:
  - 469 carriers, packed `45100469` = 451 × 100,000 + 469;
  - 86 unread-stream refusals.
- **New findings:**
  - RES-A, a RESIDUE: the scope wording of the #963 correction comment.
  - SUG-A, a SUGGESTION: a stale archived copy.
- **Open findings:** no MINOR, MAJOR or BLOCKER.
- **Result:** every lens is clean at `a18f0996`.

## 2. What was checked, with evidence

### 2.1 Identity of head and body

- `receipts/pr984.json`: the live PR reports `headRefOid` = `a18f0996f4b1…`, state OPEN, not a draft, and `updatedAt` 2026-11-23T12:34:58Z.
- `receipts/pr984-body-live.md`: the live body as published, 15,739 B.
- `receipts/evidence-975fdfd3__author-r2b_PR-BODY-corrected.md`: fetched at `975fdfd3`.
  - `cmp` against the live body reports them identical, with equal sha256.
  - The git blob id was recomputed locally as `779b4a462ae9cf846f0ae25a128f0291bc4e795f`. It equals the tree entry at `975fdfd3`.
  - Every fetched evidence file was also re-hashed against its tree blob id. All six match.
- `receipts/body-delta-r2-to-live.diff`: the full text delta from the round-2 body (`author-r2/PR-BODY.md`, blob `57db6285…`) to the live body. It has exactly three hunks:
  - **Line 42, the Status table, shard 0 row:**
    - Was: "its 18 AECP arms, the only arms that compile `test_aecp.cpp`".
    - Now: "its 18 AECP arms, which include every arm that compiles `test_aecp.cpp`". This is RES-1's exact fix.
  - **Line 123, the Description, "The check order, held by a test":**
    - Was: "A further 4,000 edits carry the new mapping, and 86 of them are output edits refused at".
    - Now: "A further 4,000 edits are drawn with it as their illegal kind: 469 carry it, and 86 are output edits refused at". This is F1's exact required text.
  - **Line 219:** one trailing empty line was added. It has no effect on content.

  No other byte of the body changed, so none of the body's other claims moved. R898-2's verdicts on them stand.

### 2.2 The figures against the published logs

- **`head-illegal-carriers.gtest.log`** (blob `2f3a517e…`), in the evidence tree under `reviews/R898-2/receipts/probes/`:
  - The probe's assertion prints `carriers[0]*100000u+carriers[1]` = `45100469`.
  - Its label is "no-stream kind*100000 + existing-stream kind".
  - So 451 carriers are of the no-stream kind and 469 of the existing-stream kind. The body's "469 carry it" matches.
- **`head-tally-floors-raised.gtest.log`** (blob `8b13ef1d…`):
  - The row "the seeded edits include an output edit refused at an illegal mapping of a stream it has not read" reports `actual: 86`.
  - The body's "86 are output edits refused at such a mapping of a stream not yet read" matches.

### 2.3 Independent falsification attempt: a replay of the draws

The probe logs are the same counting route that R898-2 used. This round adds a separate route.

- **The replay:** `scripts/replay_map_edit_draws.cpp` reproduces, outside the firmware build, everything the tally depends on in `Core.MapEditsAreTheirDefinitionRowForRow` (`sw/firmware/ctrl/test/test_aecp.cpp:2869-2991`):
  - the xorshift seed `0x904`;
  - the order of every draw (`legal`, `wide`, held, owned, edit, injection, room, streaming);
  - the reference model `definition`.
- **Why the firmware is not needed:** the tallies come from the model's `want`, not from the firmware.
- **Why a free `past` value is enough:**
  - Every edit row is drawn from `legal()` or `lawful`, whose channels are all below 4.
  - The test asserts `past >= 4` (`test_aecp.cpp:2918`).
  - So the fixture's actual `past` value cannot change the counts. The replay runs with `past` = 4, 8 and 64.
- **Result:** `receipts/replay-map-edit-draws.txt`, from `test_aecp.cpp` at sha256 `a07e1a87…`:
  - Carriers: no-stream 451 and existing-stream 469, packed `45100469`, for all three `past` values.
  - Unread refusals: 0 in edits 0-3,999 and 86 in edits 4,000-7,999.
  - So all 86 fall within the 469. `o.unread` requires `!in`, so all 86 are output edits.
  - All 469 second-half carriers are refused with status 7.
- **What this establishes:**
  - "469 carry it" holds, and "86 are output edits refused at such a mapping of a stream not yet read" holds.
  - "drawn with it as their illegal kind" is exact. `test_aecp.cpp:2958` selects the existing-stream kind for every edit with `c >= ABSENT`, and injects it only when the edit is non-empty and `next()%8 == 0`.
  - The figures could have disagreed with the logs, and they do not.

### 2.4 RES-1's corrected claim

- `aecp_arms.py:124` compiles `test_aecp_debug.cpp` for the debug arm and `test_aecp.cpp` otherwise. The image arms compile `test_aecp_image.cpp`.
- So not all 18 shard-0 AECP arms compile `test_aecp.cpp`, and "which include every arm that compiles" is the correct relation within shard 0.
- See RES-A for the global reading of the issue comment's wording.

### 2.5 The #963 correction comment

`receipts/issue963-correction-7101302165.json` was created 2026-11-23T12:34:32Z and has not been edited. It does three things:

- It names R898-2-F1.
- It states "of the further 4,000 edits drawn with the new existing-stream mapping as their illegal kind, **469 carry it**, and 86 are output edits refused at such a mapping of a stream not yet read". It cites both logs.
- It restates RES-1, and it states that the head is unchanged at `a18f0996`.

The round-2 REVIEW READY (`receipts/issue963-review-ready-7100166169.txt`) was not edited and still says "A further 4,000 carry the new mapping". The correction follows it on the same issue and names it explicitly. A public record corrected append-only is traceable for a cold reader, so I count F1's REVIEW READY half as resolved.

### 2.6 Clone integrity

`receipts/clone-integrity.txt` records the following:

- HEAD and tree are exactly as named.
- `git status --porcelain` is empty. The worktree and the index both equal HEAD.
- The `git ls-files -s` digest equals the `ls-tree` digest, so blob ids, modes and stage-0 entries all match.
- The six gitlinks are the HEAD tree's. The checked-out submodules sit at those commits, and `external` is not initialized and was left untouched.
- No probe ran inside the clone. The replay was built under `scratch/replay` from a script in `scripts/`.

## 3. Prior findings at this head

| Finding | Status at `a18f0996` | Evidence |
|---|---|---|
| R898-2 F1 (MINOR, Tests, Docs): "a further 4,000 edits carry the new mapping" | **Resolved** | Live body line 123 is F1's required text. #963 issuecomment-7101302165 corrects the REVIEW READY. The figures are confirmed in sections 2.2 and 2.3 |
| R898-2 RES-1 (RESIDUE, Docs): "the only arms that compile `test_aecp.cpp`" | **Resolved (PR body)** | Live body line 42 is the exact fix. The REVIEW READY's stale wording is superseded by the correction comment. See RES-A |
| R898-2 SUG-1 (SUGGESTION, Tests, Docs): quoted raw hashes in `plant-tally.txt` not tied to published files | **Not acted on (optional)** | The archived receipts are unchanged. A SUGGESTION does not affect coverage |
| R898-1 F1, R1, S1 and R899-1-F1, F2 | **Resolved (R898-2), unchanged** | No byte of source or of the relevant body text has changed since R898-2 confirmed them |

## 4. New findings

**RES-A. RESIDUE. Lens: Docs.**
- **Artifact:** #963 issuecomment-7101302165. It says "The 18 AECP arms of shard 0 include every arm that compiles `test_aecp.cpp`."
- **Evidence:** taken globally, the sentence is untrue, because other arms also compile `test_aecp.cpp`:
  - the AECP plant campaign builds planted copies against `test_aecp.cpp` (`aecp_mutants.py:910`, `test_ctrl_firmware.py:255`);
  - the `stream_counter_f5.py` bench appends a fixture to it (`tb/verilator/milan_dp/stream_counter_f5.py:34,60`).

  The intended claim is about shard 0's own arms, and the PR body's "its 18 AECP arms" scopes it that way. The Status table already states that shard 1, the plants, ran at `50d3f10e`, so no figure, verdict or evidence claim changes.
- **Exact fix,** for any future restatement and for the PR body if it is touched again: "its 18 AECP arms, which include every shard-0 arm that compiles `test_aecp.cpp`".

**SUG-A. SUGGESTION. Lenses: Docs (evidence traceability).**
- **Artifact:** `review-evidence/963-r1/author-r2/REVIEW-READY.md` at `975fdfd3`. It is the archived round-2 REVIEW READY and still carries F1's old figure.
- **Problem:** `author-r2b/` holds only `PR-BODY-corrected.md`, so nothing in the packet points from the stale REVIEW READY copy to its correction.
- **Suggestion:** add a one-line pointer in `author-r2b/`, or an archived copy of issuecomment-7101302165. Then the packet alone shows the REVIEW READY's correction.

## 5. Lens results at the head

Lenses whose artifacts the delta does not touch keep R898-2's evidence, which is restated here at the same head. The delta is the PR body and an issue comment, and it changes no source, test, generated artifact or document in the tree.

| Lens | Result | Artifact at `a18f0996` | What was checked |
|---|---|---|---|
| Conformance | PASS | `aecp_maps.c:114-125,275-289,534`; `test_aecp.cpp:2869-2991`, unchanged; live body line 123 | No source change since R898-2's clean coverage. The corrected sentence matches the test's definition: an existing-stream illegal mapping is refused before its port is read (`test_aecp.cpp:2885-2890`) |
| RTL | PASS | `receipts/clone-integrity.txt` (HEAD/tree identity, gitlinks); `receipts/pr984.json` (head unchanged) | No RTL, firmware or interface byte changed since R898-2. The delta is PR text only |
| Robustness | PASS | `test_aecp.cpp:2888-2902,2956-2959`; `receipts/replay-map-edit-draws.txt` | The new illegal kind is drawn for every edit 4,000-7,999 (469 injected, all refused with status 7). The not-yet-read refusal path is reached 86 times, against a floor of 20 |
| Tests | PASS | `test_aecp.cpp:2937-2991`; `head-illegal-carriers.gtest.log`; `head-tally-floors-raised.gtest.log`; `scripts/replay_map_edit_draws.cpp` | The published figures 469 and 86 match both the probe logs and an independent replay of the seeded draws. F1 is closed. No test changed |
| Docs | PASS | `receipts/pr984-body-live.md` vs `evidence-975fdfd3__author-r2b_PR-BODY-corrected.md` (identical); `receipts/body-delta-r2-to-live.diff`; `receipts/issue963-correction-7101302165.json` | The body equals the archive, and its only changes are F1's and RES-1's exact texts. The comment rule is not applicable, because the delta adds no source comment. RES-A is residue and SUG-A optional |

## 6. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `aecp_maps.c` (unchanged); `test_aecp.cpp:2869-2991`; live PR body; R898-2 evidence carried with no source delta | R898-3 (carrying R898-2's clean coverage at the same head) | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| RTL | CLEAN | `receipts/clone-integrity.txt`; `receipts/pr984.json`; R898-2's RTL evidence carried with no source delta | R898-3 (carrying R898-2) | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Robustness | CLEAN | `test_aecp.cpp:2888-2902,2956-2959`; `receipts/replay-map-edit-draws.txt`; R898-2 probes carried | R898-3 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Tests | CLEAN | `test_aecp.cpp`; both R898-2 probe logs at `975fdfd3`; `scripts/replay_map_edit_draws.cpp` and its receipt | R898-3 | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |
| Docs | CLEAN | Live PR #984 body; `author-r2b/PR-BODY-corrected.md`; `body-delta-r2-to-live.diff`; #963 issuecomment-7101302165 and 7100166169 | R898-3 (RES-A residue; SUG-A optional) | `a18f0996f4b1b654a232dfe56fa64ee7ecaf697e` |

## 7. Real limits

- **No source execution this round.**
  - This round ran no firmware gate, suite, campaign, Verilator or Yosys bank.
  - Source-head execution evidence is still the author's published gate receipts, plus R898-1 and R898-2's probes.
  - No manager source bank exists at this head, and none is claimed or inferred.
- **The replay covers the model only.** It re-derives the test's own draws and reference model, not the firmware's behaviour. That the firmware equals the model at this head rests on the test's assertions and the published runs.
- **Shard 0 was not re-run as a gate command at `a18f0996`.** The PR body states this. Only its 18 AECP arms ran at this head.
- **The full native Verilator sweep is NOT RUN.** It is owed to the merge candidate.
- **No hardware evidence.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Hosted and act results were not inspected.** The manager owns their acceptance.

## 8. Pending manager duties

- **Merge candidate:** build and validate the current-dev merge candidate. The source base is `dd163e41`, and live dev is `e275d7950ef3385753e6a15d2e191ba855b171ed`. This covers the builder and native banks, including the owed full Verilator sweep. Link the receipts on the PR.
- **Hosted acceptance:** accept the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` evidence, telling executed jobs apart from skipped contexts.
- **Residue and suggestions:** carry RES-A to the residue checklist. SUG-A, and R898-2's SUG-1, are optional.
- **Completion bar:** confirm the external review and the remaining completion-bar items. Merging still needs explicit maintainer authorization.

R898-3 FINISHED
