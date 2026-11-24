[R883] POSITIVE - exact head e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d

# R883-6: narrow re-review of PR #966 (issue #884), the fix for R883-5-F1

Exact head `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d`, tree `c58fc25595e596d3125a2f50d4ec02f10f8e82a8`. Delta reviewed:
`0acf24d9b5060a263f725c02026446dde64c2574..e05f800a`. That is one commit, whose parent is the R883-5 head. The source
base is `59b098841b1e2826aaf7a38b557faa5345f91c82`.

## Summary

R883-5-F1 is **RESOLVED at its cause**. The delta rewords exactly two lines, and it rewords them together:

- the assertion message at `sw/firmware/ctrl/test/test_aecp.cpp:4681`;
- the campaign needle at `sw/firmware/ctrl/test/aecp_face_mutants.py:31`.

Both now read "AS_CAPABLE is the firmware gPTP owner's". Neither contains a #259 class-R term. The needle is a
substring of the assertion, so the planted AS_CAPABLE leak is still caught by its own named check, on the new words
alone. Nothing else changed: the commit has two `M` paths, and the check logic, the plant, the test name and the
product code are all unchanged.

This round raises no new BLOCKER, MAJOR or MINOR. The prior RESIDUE and SUGGESTION items stay as they were, because
the delta does not touch them.

## Delta

`git diff --name-status 0acf24d9..e05f800a` lists exactly two modified files (`receipts/restore_check.txt`):

- `sw/firmware/ctrl/test/test_aecp.cpp:4681`: the `<<` message changed from "...software gPTP owner's..." to
  "...firmware gPTP owner's...". The `EXPECT_EQ(result.flags&1u,capable?1u:0u)` above it is byte-identical.
- `sw/firmware/ctrl/test/aecp_face_mutants.py:31`: the needle of row `face-software-gptp-keeps-datapath-capable` was
  reworded the same way. The row name, file, old/new plant text and test name are unchanged.

The commit subject is one line, with no body and no trailers (`receipts/restore_check.txt`). It is identical to the
author's published `receipts/delta.diff` (`DELTA-IDENTICAL`, checked locally).

## R883-5-F1 verification items, re-checked by the reviewer

| Required by R883-5-F1 | Result at `e05f800a` | Receipt |
|---|---|---|
| `check_baremetal_only.py --check` rc 0, 0 findings | `baremetal-only: OK (0 findings across 1936 tracked first-party file(s))`, rc 0 | `receipts/baremetal_check_head.txt` |
| `--selftest` passes | rc 0 | `receipts/gates/baremetal_selftest.{log,rc}` |
| Cause removed, using the gate's own class-R regex (`RUNTIME_RE`, `scripts/check_baremetal_only.py:188-209`) | At `0acf24d9`: one hit `software gPTP owner` at each of `test_aecp.cpp:4681` and `aecp_face_mutants.py:31`. At `e05f800a`: 0 hits in both files. "firmware gPTP owner" is not a listed term. | `receipts/term_probe.txt`, `term_probe.py` |
| The leak row is still caught on its new words | The repository's own `campaign()`/`caught()` ran over all 14 `aecp_face_mutants.ROWS`, after the full-table `controls()` (table drift and reader controls) passed: 14 `[ok]`, 0 escaped, rc 0. The leak-row log fails `Face.SoftwareGptpAvbKeepsTheDatapathsLinkAndClass` only on "AS_CAPABLE is the firmware gPTP owner's, whatever the datapath's bit 0 (1)" (`test_aecp.cpp:4680`), once per interface. | `receipts/face_campaign.txt`, `receipts/face_results.json`, `receipts/leak_row.log` |
| The needle is tied to the assertion | Control: the same plant, graded on the OLD needle "AS_CAPABLE is the software gPTP owner's", is reported `[ESCAPED]`, rc 1. So the row is graded by the new words, and a stale needle would be visible as an escape. | `receipts/old_needle_control.txt`, `receipts/old_needle_results.json` |
| The two other software-gPTP face rows are caught on their own words | `[ok] face-software-gptp-clears-link-flags` and `[ok] face-software-gptp-ignores-path-refusal` | `receipts/face_campaign.txt` |
| The unplanted AVB test passes at 1 and 2 interfaces | `app` arm, all 7 face tests selected: `[  PASSED  ] 7 tests`, `verdict: PASS`, rc 0, at both `if1` and `if2` | `receipts/face_clean_if{1,2}.txt`, `receipts/face_clean_if{1,2}.gtest.log` |
| docs-gates-0 steps pass | The author's receipt says 42 run-steps, `ALL-STEPS rc=0`, `porcelain-after 0`. I verified its hash against the published `MANIFEST.json`. I re-ran the delta-sensitive steps myself, and every one is rc 0: bare-metal `--check`/`--selftest`, `docs_check.py`, `check_doc_paths.py`, `docs_inventory.py --check`, C/C++ and Python idiom gates, hygiene, test-evidence, fail-fast, naming and TODO ownership. Hosted `docs-gates-0` is `completed/success` at this head. | `receipts/gates/*`, `receipts/author_r8_manifest_verify.txt`, `receipts/hosted_snapshot.txt` |
| em-dash gate | My local run refused with rc 2 because the pinned Markdown renderer was missing from my environment. That is an environment limit, not a tree result. The gate judges added `*.md` lines only (`scripts/check_em_dash.py:4,20`), and the delta touches no `.md` file. A direct scan finds 0 added lines carrying U+2014 or U+2013. The author's clean-clone receipt reports `0 finding(s) over 502 added line(s)` against base `59b09884`. | `receipts/gates/em_dash_*.log`, `receipts/em_dash_direct.txt` |

### Author evidence verified

I fetched `review-evidence/gptpsw-r1/author-r8/` at `71180b29`. These files match the `published_sha256` entries in
the evidence `MANIFEST.json`: `REVIEW-READY.md`, `HANDOFF.md`, `aecp-campaign.summary.txt`,
`docs-gates-0.summary.txt`, `docs-gates-0.coverage.txt`, `delta.diff`, `needle-tie.txt`, `baremetal-check-lane.log`,
`branch-state.txt` and `commit.txt` (`receipts/author_r8_manifest_verify.txt`, 10 MATCH, 0 MISMATCH).

The author's claims agree with my runs:

- full AECP campaign: 388 rows over two shards, 0 escaped;
- needle tie: the new words grade caught, while the old words and the link-flag words grade not caught;
- docs-gates-0: `ALL-STEPS rc=0`.

`branch-state.txt` records "not pushed" at the time of the receipt. The PR head now reads `e05f800a`, so the push
came after the receipt, which is consistent.

## Findings

No new BLOCKER, MAJOR, MINOR or RESIDUE at this head.

### R883-6-S1 | SUGGESTION | Docs | `sw/firmware/ctrl/test/test_aecp.cpp:4679,4681`

The same test now says "software gPTP" in one message and "firmware gPTP owner" in the next.

- `:4679` reads "software gPTP keeps the datapath's link flags". The needles of the other two rows
  (`aecp_face_mutants.py:26,36`) say the same. None of these is a #259 term, and the gate passes.
- `:4681` reads "firmware gPTP owner". This matches `docs/design/GPTP_SOFTWARE.md:153`.
- Optional: unify the words in a later change. Any such change must move each assertion and its needle together.
  It must keep the face campaign caught, keep the bare-metal gate at rc 0, and keep the link-flag words distinct from
  the AS_CAPABLE words.

### Source-comment rule

The delta adds no source comment. The two changed lines are an assertion string and a needle string. Neither contains
a bench lane label, lane name, review round, reviewer ID or issue-comment ID, so there is no new RESIDUE.

## Prior findings, resolved or retained at this head

I read these only after my own pass over the delta.

| Finding | Status at `e05f800a` | Evidence |
|---|---|---|
| R883-5-F1, MAJOR, Conformance/Tests/Docs | **RESOLVED at its cause** | See the verification table above. The class-R hits went from 2 to 0, and the gate is rc 0 at the head. The leak row is caught on its new words, and a control with the old words escapes. The docs workflow was run by the author (`ALL-STEPS rc=0`, manifest-verified), and hosted `docs-gates-0` succeeds at this head. |
| R883-5-S1, SUGGESTION, Tests | RETAINED (optional) | `test_aecp.cpp:4667-4679` is unchanged by the delta: the link-flag bits are still only `0x7a`'s. |
| R883-5-S2, SUGGESTION, Docs | RETAINED (optional) | The comment at `test_aecp.cpp:4667` is unchanged. |
| R883-4-R1, RESIDUE, Docs | RETAINED on the residue checklist | The PR body and `sw/firmware/gtest/README.md` are untouched by the delta. |
| R883-4-R2, RESIDUE, Docs | RETAINED | The docstring at `aecp_face_mutants.py:3-9` is unchanged, and its exact fix still applies. |
| R883-4-R3, RESIDUE, Docs | RETAINED | `test_unit_driver.cpp` is untouched. |
| R883-4-S1, SUGGESTION, Tests | RETAINED (optional) | `test_unit_driver.cpp` is untouched. |

## Lens results (artifact evidence)

```text
[R883] PASS Conformance — test_aecp.cpp:4680-4681, aecp_face_mutants.py:31, scripts/check_baremetal_only.py:188-209 — #259 class-R: 0 hits at head (2 at 0acf24d9), gate --check rc 0 / --selftest rc 0; the AS_CAPABLE check itself (bit 0 owned by the firmware gPTP owner, IEEE 1722.1-2021 7.4.40.2) is byte-identical to the R883-5-reviewed assertion
[R883] PASS RTL — git diff --name-status 0acf24d9..e05f800a (two M paths under sw/firmware/ctrl/test/, no hdl/ or product path) — the delta changes nothing an RTL verdict depends on; the R883-5 RTL result (KL_ptp_clock_validity.sv:143,243 live asCapable) carries
[R883] PASS Robustness — test_aecp.cpp:4666-4692 unchanged except the message words at :4681 — both disagreement cases on every interface are still exercised; face tests green unplanted at if1 and if2 (receipts/face_clean_if{1,2}.gtest.log)
[R883] PASS Tests — aecp_face_mutants.py:24-71 via aecp_mutants.campaign()/caught()/controls() — 14/14 face rows caught; leak row fails only on the new words; old-needle control ESCAPED; author full campaign 388/388 (manifest-verified)
[R883] PASS Docs — author-r8 REVIEW-READY/HANDOFF/receipts against MANIFEST.json (10 MATCH); docs-gates-0 author ALL-STEPS rc=0, reviewer re-run of delta-sensitive steps rc 0, hosted docs-gates-0 success; delta adds no source comment (source-comment rule clean)
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `test_aecp.cpp:4680-4681`, `aecp_face_mutants.py:31` against `scripts/check_baremetal_only.py:188-209` (#259). The assertion logic is unchanged from R883-5's check against `aecp_face.c:191-215` (7.4.40.2 bit 0). Receipts: `receipts/term_probe.txt`, `receipts/baremetal_check_head.txt`. | R883-6 | `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d` |
| RTL | CLEAN | The delta path list has no `hdl/` path. The R883-5 RTL coverage (`KL_ptp_clock_validity.sv:143,243`) is unaffected, because nothing in RTL scope changed since `0acf24d9`. | R883-5, carried by R883-6 | `0acf24d9b5060a263f725c02026446dde64c2574` (ancestor; no RTL-scope change to `e05f800a`) |
| Robustness | CLEAN | `test_aecp.cpp:4666-4692`. The unplanted face tests pass at if1 and if2. | R883-6 | `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d` |
| Tests | CLEAN | `aecp_face_mutants.py:24-71`, `aecp_mutants.py:891-970`. Reviewer face campaign: 14 of 14 caught. Old-needle control escaped. Author's full campaign: 388 rows, manifest-verified. | R883-6 | `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d` |
| Docs | CLEAN | The `author-r8` packet against `MANIFEST.json`. docs-gates-0: author receipt, reviewer re-runs and hosted result. The delta was checked under the source-comment rule. | R883-6 | `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d` |

## Real limits

- **Not run by me:**
  - the full AECP campaign (388 rows);
  - the full docs-gates-0 job, including the HDL reference build, the diagram, WaveDrom, gPTP-submodule docs and
    sv2v steps, and the CI-controls steps;
  - docs-gates-1 and docs-gates-2, firmware shards and `fw_coverage --check`.

  For these I rely on the author's manifest-verified receipts. My face campaign covers the 14 face rows only.
- **em-dash gate:** my local run refused (rc 2) because the pinned Markdown renderer is not installed in my
  environment. I judged the gate inapplicable to the delta (no `.md` path) and checked the added lines directly.
- **How my probes ran:** they reuse the repository's own `campaign()`, `caught()`, `controls()` and `core_arm()` on
  disposable copies under the packet's `scratch/`. The checkout was never written, apart from Python bytecode caches,
  which I removed.
- **Restore check:**
  - the HEAD tree and the index tree are both `c58fc255`;
  - the blobs and modes of `test_aecp.cpp`, `aecp_face_mutants.py` and `aecp_face.c` match HEAD;
  - all six gitlinks are as recorded, and the submodule worktrees are clean;
  - `git status --porcelain --ignored` is empty (`receipts/restore_check.txt`).
- **Hosted results were observed, not accepted.** At my snapshot (`receipts/hosted_snapshot.txt`):
  - `docs-gates-0`, `docs-gates-1`, `docs-gates-2` and `docs-check-no-git` are success;
  - `docs-check` is queued;
  - several Verilator, Yosys and firmware jobs are queued or in progress;
  - the physical gPTP context is skipped.

  A skip is not hardware proof.
- **Not claimed:** no manager source bank exists at this head, and none is claimed or inferred. No Docker, act, host
  runner, hardware or physical calibration was run.

## Pending manager duties

- Own hosted and act acceptance at `e05f800a`. In particular, confirm `docs-check` (queued at my snapshot) and the
  remaining long gates finish green on this exact head.
- Carry R883-4-R1 to R3 on the residue checklist. R883-6-S1, R883-5-S1/S2 and R883-4-S1 are optional.
- At the merge turn, run the current-dev merge-candidate builder and native banks (source base `59b09884`, live dev
  `e275d795`), and link their receipts on the PR.
- The merge still needs the external positive review and the rest of the AGENTS.md section 7 bar.

R883-6 FINISHED
