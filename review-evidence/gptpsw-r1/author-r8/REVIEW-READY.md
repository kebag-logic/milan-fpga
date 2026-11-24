STATUS: LOCAL VALIDATION COMPLETE

# [A837] REVIEW READY: PR #966, round 3b (R883-5-F1)

Commit: `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d`. It is one local commit on `0acf24d9b5060a263f725c02026446dde64c2574`.
Branch: `884-gptp-firmware`; PR base: `dev-soft-core-optimisation`. **Not pushed.** The remote tip is still
`0acf24d9` (`receipts/branch-state.txt`). I made no PR edit, posted no comment and give no review verdict.

Subject: `Word the AS_CAPABLE check as the firmware gPTP owner's`. It is one line, with no body and no trailers
(`receipts/commit.txt`).

## Delta from 0acf24d9

Two lines in two test files. Nothing else changed (`receipts/delta.diff`, `receipts/diff-check.txt`).

- `sw/firmware/ctrl/test/test_aecp.cpp:4681`: the assertion message now reads
  `"AS_CAPABLE is the firmware gPTP owner's, whatever the datapath's bit 0 (" << bit << ")"`.
  Only the words changed. The check itself is unchanged.
- `sw/firmware/ctrl/test/aecp_face_mutants.py:31`: the needle for row `face-software-gptp-keeps-datapath-capable` now
  reads `"AS_CAPABLE is the firmware gPTP owner's"`. The plant and the test name are unchanged.
- The new wording comes from the tree: `docs/design/GPTP_SOFTWARE.md:153` already says "the firmware gPTP owner".
  This is also the wording R883-5 suggested. After the change, `sw/` contains no "software gPTP owner"
  (`receipts/wording-grep.txt`).
- The rest of the delta is unchanged:
  - No product C, RTL, config, ratchet or doc file changed.
  - No path outside `sw/firmware/ctrl/test/` changed.
  - The firmware product inputs changed: 0.
- The other two software-gPTP rows are untouched. Their words ("software gPTP keeps the datapath's link flags" and
  "software gPTP forwards the path owner's refusal") contain no #259 term, and the gate passes with them in the tree.

## R883-5-F1 verification items

| Required by F1 | Result at `e05f800a` | Receipt |
|---|---|---|
| `check_baremetal_only.py --check` rc 0, 0 findings | `baremetal-only: OK (0 findings across 1936 tracked first-party file(s))`, rc 0. This held both in the lane checkout and in the clean clone. | `baremetal-check-lane.log`, `docs-gates-0.summary.txt` |
| `--selftest` passes | `baremetal-only selftest: PASS (867 arm(s))` | `docs-gates-0.summary.txt` |
| The docs workflow's local gates | All 42 run-steps of `docs.yml` job `docs-gates-0` gave rc 0 (`ALL-STEPS rc=0`), and the clone was clean afterwards. All 40 `gate_*` run-steps ran. The 18 steps not run are checkout, cache, install, upload and record steps. | `docs-gates-0.summary.txt`, `docs-gates-0.coverage.txt` |
| The needle is a substring of the assertion and distinct from the link-flag words | Both true | `needle-tie.txt` |
| The planted AS_CAPABLE leak is still caught on its new words | Caught in the full campaign (`[ok] face-software-gptp-keeps-datapath-capable`). The test failed only on "AS_CAPABLE is the firmware gPTP owner's, whatever the datapath's bit 0 (1)", once per interface, with no link-flag failure. | `aecp-campaign.summary.txt`, `campaign-leak-row.excerpt.log`, `leak-row.excerpt.log` |
| The planted leak is graded by the new words alone | The same leak log was re-graded with the repository's own `caught()` on each set of words. The new words grade it **caught**. The old words ("...software gPTP owner's") and the link-flag words both grade it **not caught**. So the needle and the assertion are tied to each other: change either one alone and the row escapes. | `needle-tie.txt` |
| The two other software-gPTP face rows are still caught on their own words | `[ok] face-software-gptp-clears-link-flags` and `[ok] face-software-gptp-ignores-path-refusal`, in both the campaign and the probe | `aecp-campaign.summary.txt`, `plant-probe.filtered.log` |
| The unplanted AVB test passes at 1 and 2 interfaces | `baseline if1: rc=0 ... ran=True ok=True`, `baseline if2: rc=0 ... ran=True ok=True` | `plant-probe.filtered.log` |

## Validation (all at `e05f800a`, each in a clean clone pinned to its own CPU range)

| Check | rc | Wall time (CET) | Receipt |
|---|---:|---|---|
| `scripts/check_baremetal_only.py --check` (lane checkout) | 0 | 16:15 to 16:20 | `baremetal-check-lane.log` |
| `docs-gates-0` run-steps (`docs_gates0.sh`, 42 steps; em-dash base `59b09884`, the merge-base with `origin/dev-soft-core-optimisation`) | 0 | 16:20 to 17:53 | `docs-gates-0.summary.txt`, `.coverage.txt` |
| Full AECP campaign, `aecp_mutants.py --output <dir> --shard 0 2` | 0 | 16:24 to 17:20 | `aecp-campaign.summary.txt` |
| Full AECP campaign, `--shard 1 2` (contains the leak row) | 0 | 16:24 to 17:24 | `aecp-campaign.summary.txt` |
| Software-gPTP probe (`plant_proof.py ... new`: three face rows plus a baseline at 1 and 2 interfaces) | 0 | 16:15 to 16:24 | `plant-probe.filtered.log` |
| `git diff --check 0acf24d9 HEAD` | 0 | | `diff-check.txt` |

- The campaign covers all 388 rows: 194 + 194 caught and 0 escaped.
- Each shard's `campaign()` runs `controls()` first. That includes the table-drift control (every TEST in
  `test_aecp*.cpp` is claimed) and the reader controls. Both passed with the new needle in the table.
- I stopped one docs attempt to fix my local runner, not the tree. Its python was outside the pinned venv, and its
  sv2v string match was wrong. I re-ran it from the start. It is recorded in `docs-gates-0.discarded-attempt.txt`
  and not counted.
- I also stopped one unsharded campaign run so I could split it in two. It had 27 rows ok and 0 escaped, and it is
  not counted.

## Not run, and why

- **The four firmware shards (`test_ctrl_firmware.py --require-rv32 --self-test`).** No firmware product input
  changed: 0 paths under `sw/firmware` outside `test/`. The delta changes one assertion's message string and the
  campaign needle that grades it. These shards also compile `test_aecp.cpp`. Within this round, the full AECP
  campaign and the AVB baseline at 1 and 2 interfaces compiled and ran it.
- **`fw_coverage.py --check`.** A message string inside a test cannot change product line or branch coverage.
  `coverage.ratchet` is unchanged.
- **Not done:** `docs-gates-1`/`-2`, `docs-check-no-git`, `act` and the hosted runs.
- **Not done:** push, PR comment, PR-body edit and bench.

Out of scope and untouched: R883-5-S1/S2 (suggestions), R883-4-R1 to R3 (residue) and R883-4-S1.

Open risks/questions: none.
