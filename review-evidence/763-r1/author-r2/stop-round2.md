[A653] STOP
Head: `07c6c72fce79e705bcf28a70071497d0ce7040e4` (PR #766, branch `763-map-persist`; no new commit in Round 2, and the tree is clean)

Round 2 (PR #766 comment 6259259419) answers R658-1 (6258733493) and R657-1 (6259255660). Items 2 and 3 are done. Item 1 needs a decision.

**Item 1, the inventory refresh (R658-1-F1, R657-1-F1): STOP.** I ran the documented procedure (`docs/testing/CI_IMAGE.md:766-771`) with the pinned parser and did not hand-edit anything.
- `python3 scripts/ci_tool_inventory.py --write` changes exactly four `inputs` rows of `ci/image/tool-inventory.json`, and no `tools`, `residue` or schema field. Two rows are this lane's (`aecp_arms.py`, `aecp_mutants.py`). Two are inherited: `scripts/check_doc_style.py` (stale since PR #753, one `DOCUMENTS` entry) and `scripts/measure_test_evidence_readers.py` (stale since PR #754, one disposition entry). The generator rewrites all four in the same refresh. I reviewed all four script changes: none adds an installation request.
- Afterwards, `ci_tool_inventory.py --check` exits 0 (it exits 2 at the head), and the eight inventory and image self-tests at `CI_IMAGE.md:657-664` exit 0.
- **The conflict:** `tool-inventory.json` is a recipe input of the CI image (`ci/image/build.py:151`). The refresh moves the recipe digest from `712f7b38` (the value recorded in `ci/image/image.lock.json`) to `1e5e36f7`. So `python3 ci/image/build.py --work <dir> --check-lock` goes from 0 at the head to 2: "image lock does not describe the current recipe". Only an image build re-records the lock (`CI_IMAGE.md:665-667`). On `dev`, every inventory regeneration was followed by a lock re-record "from two byte-identical cold builds" (`e977cc44`/`cd9ef1be`, `ce3dd4bd`/`4df2f2f0`, `e19dd354`/`943d47db`, `f1c041bc`/`54fbcba6`).
- So the refresh alone cannot make every check that covers it exit 0. Committing it would swap the inventory refusal for a lock refusal, on a check that passes at the head today. I did not commit it.

Decision needed, one of:
- **(a) Recommended.** Commit the refresh in this lane as one generator-output commit. The image owner re-records `image.lock.json` on or before the merge candidate. The last re-record changed only `recipe_digest`.
- **(b)** Commit the refresh and re-record the lock in this lane. That means two cold builds of every image layer, far beyond this four-file delta.
- **(c)** Keep the refresh out of this PR, with a public decision and a tracking issue that give all four rows to the inventory's owner.

Separately, `ci/image/exec-audit-receipt.json` also holds the base digests of the two AECP scripts. It is a committed observation of one traced run inside the image (`CI_IMAGE.md:586-597`), so I left it unchanged.

**Item 2, the count (R658-1-F2): corrected.** The Round B evidence (comment 6258557430) said "939 planted controls caught". That overstated the planted controls. Classified against the AECP and SRP tables at the head, over the gate log (full log sha256 `375b9655…`), the 939 lines split as follows: firmware gate PASS; 876 source-mutant executions caught (520 control-source, 78 AECP, 278 SRP) and two pin-refusal controls passed; 61 normal arm outcomes passed (939 top-level `[ok]` lines). The PR body draft and the receipt summary now say this.

**Item 3, residue (R658-1-F3, R657-1-R1): applied** in the PR body draft. The status line now reads "two commits at published head `07c6c72f`". The roles name `[R657]` (internal, 6258585761) and `[R658]` (external, 6258590845). While item 1 is open, the draft says "Relates to #763" instead of "Closes #763".

Gates in Round 2:
- At the head: inventory `--check` exits 2, `--check-lock` exits 0, and the docs gates (`docs_check`, `check_feature_status`, `check_doc_style` and `--selftest`, `gen_toc` `--selftest`/`--verify-anchors`/`--check`, `check_em_dash --base e9cbb676`) all exit 0.
- With the refresh applied: `--write` exits 0, `--check` exits 0, the eight self-tests exit 0, and `--check-lock` exits 2.
- The firmware bank was not re-run. No byte in the tree changed since its rc 0 run at this exact head, and the refresh changes no firmware input.

No push, PR edit, Docker build, hardware or bench access was used. Receipts are in the lane's output directory under `receipts/round-2/`, with an index generated from the files present.
