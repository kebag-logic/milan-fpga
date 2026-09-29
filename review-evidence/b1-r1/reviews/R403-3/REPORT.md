[R403] POSITIVE - exact head 931c3edfced972e01356cd989b5092a1672de5a3

# R403-3: external confirmation round for PR #620 (issue #599, with #394 and #387)

- Reviewer: [R403], external, cleared context. Round R403-3.
- Exact head `931c3edfced972e01356cd989b5092a1672de5a3`, tree `56f7cdcd078625cbf8172aa73693a075b0164d4a`. This is the same head and tree that R403-2 reviewed, with no source change since. The source base is dev `13eda870d1a6cf3f946fc228a98862366b08d102`.
- Scope: only my R403-2 finding F5, which the manager owned. It is judged on the rebuilt evidence branch `b1-review-evidence` and on the public exposure record ([5886044527](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5886044527)). R403-2 resolved F1-F4 at this head; this round only confirms that the head did not move.
- Reconstruction order:
  - AGENTS.md and CONTRIBUTING.md;
  - `docs/README.md`;
  - the #599 issue body and comments;
  - the live PR #620 body and comments, including my own R403-2 ([5886023639](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5886023639)) and the exposure record;
  - `git diff 13eda870..931c3edf` and history;
  - the evidence branch, the six unreachable commits, and the GitHub push-activity log for the branch.
- The other public round-2 review (R402-2) was read only after this verdict and the ledger were written.

## Verdict summary

F5 is resolved at this head. No MINOR, MAJOR or BLOCKER finding is open, and all five lenses are clean.

- **(a) The evidence branch is rebuilt, redacted and pinned.**
  - `b1-review-evidence` is `5be3d3a4` → `c0dfcb50` → `8563f65a`. The PR body pins `c0dfcb50`.
  - `8563f65a` only adds `reviews/R402-2/` (32 files) and its 32 `MANIFEST.json` rows.
  - The private-token scan over the whole `review-evidence/` tree finds 0 hits at the branch head and at the pin, over 32 token forms. These cover the controller host's NIC MAC and its EUI-64 in every spelling.
  - The two changed files differ from their predecessors only by that one token substitution, and their manifest rows carry the new hashes.
- **(b) The exposure record is complete and accurate.** It lists exactly the six unreachable commits that the branch's push history leaves behind. Each of them still fetches anonymously by SHA and still carries private tokens. None is cited as current evidence. GitHub-side removal is recorded as a request to the owner.

## F5 (R403-2, MINOR; Docs, Conformance): resolved

### (a) Re-archive, redaction and pin

- **Branch structure** (`receipts/evidence_branch_and_exposure.txt`):
  - The live tip is `8563f65a5a10ecb437c93bcadc84cca4734e85f3`.
  - Its parent is `c0dfcb50b361d2b44dbd0e6bbdc525525e4cc16b` ("Archive the B1 evidence ..., redacted"), whose parent is the opening commit `5be3d3a46d857455147afe9589a4ca87de18a101`.
  - `5be3d3a4` adds only `review-evidence/b1-r1/MANIFEST.json` to its parent.
  - `5be3d3a4..c0dfcb50` touches 350 paths, all under `review-evidence/b1-r1/`.
  - `c0dfcb50..8563f65a` touches 33 paths: 32 added under `reviews/R402-2/` and `MANIFEST.json` modified. That makes it a review archive only.
- **Pin:** the live PR body pins [`c0dfcb50`](https://github.com/kebag-logic/milan-fpga/tree/c0dfcb50b361d2b44dbd0e6bbdc525525e4cc16b/review-evidence/b1-r1/author-r2) in "Public evidence packet". It cites no other evidence commit (see (b)).
- **Token scan:** `scripts/scan_private_tokens.py` is byte-identical to R403-2's (SHA-256 `fafc46b0...`). The private token list was rebuilt in unpublished scratch from the purged round-1 packet. It holds the 26 round-2 forms and 6 supplementary modified-EUI-64 forms (the U/L bit flipped, bare and IPv6-grouped).
  - Positive control, `receipts/private_tokens_control_92e1d7a3.txt`: 255 hits over 235 files. Tokens 00-25 give the same per-token counts and first locations as R403-2's control, so the rebuilt list is faithful.
  - Current branch head `8563f65a`, whole `review-evidence/` (382 files): **0 hits**, rc 0 (`receipts/private_tokens_branch_head_8563f65a.txt`).
  - Pin `c0dfcb50`, whole `review-evidence/` (350 files): **0 hits**, rc 0 (`receipts/private_tokens_pinned_c0dfcb50.txt`).
  - Opening commit `5be3d3a4` (1 file) and the two findings pages at the head: 0 hits (`receipts/private_tokens_opening_and_pages.txt`).
  - The live PR #620 body and all its comments, plus the #599 body and all its comments (19 texts, including the exposure record): 0 hits (`receipts/private_tokens_public_text.txt`).
  - The repository's own scrub (`docs_check.SCRUB_RULES` at this head) over the branch head: 382 files, 0 findings, rc 0 (`receipts/scrub_branch_head_8563f65a.txt`). The extra shapes it reports are the same as at R403-2: the redacted file-listing owner, the DUT IPv4, the public loopback, DUT and peer MACs, and regex text in reviewer scripts. `reviews/R402-2/` adds no new shape.
- **The two changed files are substitution-only** (`receipts/substitution_check.txt`, `scripts/check_substitution.py`).
  - Between `04d00b66` and `c0dfcb50`, `reviews/R402-1/receipts/rederive.txt` had 10 occurrences and `reviews/R402-1/scripts/rederive.py` had 1. That makes 11, which equals R403-2's 11 hits.
  - Replacing the controller host's EUI-64 with `<controller-host-id>` in the old bytes gives the new bytes exactly, and 0 occurrences remain.
- **Manifest** (`receipts/manifest_check.txt`, `scripts/check_manifest.py`):
  - At `c0dfcb50`: 349 files and 349 rows, 0 mismatches.
  - Against `04d00b66`: exactly 2 files changed, 28 added (my own `reviews/R403-2/`) and 0 removed.
  - The rows of the two changed files carry the new published hashes (`68970c65...` and `24094180...`), each equal to the file. Their `original_sha256` keeps the old hash, and no other row changed without a byte change.
  - At `8563f65a`: 381 files and rows, 0 mismatches. Only the 32 `reviews/R402-2/` rows were added.
- **My archived R403-2 packet is published byte-exact** (`receipts/r403_2_archive_identity.txt`). All 25 manifest entries, `REPORT.md` and `MANIFEST.sha256` are identical to my packet. Its one path-redacted row is the manager's own execution record.

### (b) By-SHA exposure record

- **Complete** (`receipts/evidence_branch_and_exposure.txt`). The GitHub activity log for `refs/heads/b1-review-evidence` shows:
  - branch creation at `5be3d3a4`;
  - pushes to `92e1d7a3` and `c816526d`;
  - a force-push to `9660f038`;
  - pushes to `9e135b46`, `04d00b66` and `fb6ff2f6`;
  - a force-push to `c0dfcb50`;
  - a push to `8563f65a`.

  The commits no longer reachable are exactly the six the record lists: `92e1d7a3`, `c816526d`, `9660f038`, `9e135b46`, `04d00b66` and `fb6ff2f6`. The commits API resolves each short SHA to a single full SHA whose parent chain matches that log, and none is at any of the 572 remote ref tips.
- **Still exposed, and accurately described.** All six fetch anonymously by SHA, with no credential helper, at depth 1. Each carries private tokens (`receipts/private_tokens_exposed_*.txt`):

  | Commit | Hits |
  |---|---|
  | `92e1d7a3` | 255 (the round-1 author packet) |
  | `c816526d` | 266 (the round-1 packet plus the R402-1 receipt) |
  | `9660f038` | 11 |
  | `9e135b46` | 11 |
  | `04d00b66` | 11 |
  | `fb6ff2f6` | 11 |

  The record's grouping describes `c816526d` only as the R402-1 receipt; see S10.
- **Not cited as current evidence.**
  - The head tree cites none of the seven SHAs (`git grep`).
  - The live PR body cites only `c0dfcb50`.
  - The six unreachable SHAs appear only in review-round comments, which record what each round judged, and in the exposure record itself. #599 cites none of them.
- **Removal is recorded as an owner request:** "Removing the unreachable objects needs a GitHub-side request, which I have asked the owner to make. Until that happens, the residual exposure is recorded here." That meets R403-2 F5's required outcome (b), which allowed either a removal request or a recorded owner acceptance. The removal itself remains a pending manager and owner duty.

## Head unchanged since R403-2

- The local clone, `refs/heads/b1-bench-0929` and the PR `headRefOid` are all `931c3edf`. The tree is `56f7cdcd`.
- `13eda870..931c3edf` is still two files, both under `docs/findings/` (+792).
- `receipts/verify_clone.txt`:
  - 962 tracked blobs re-hashed from disk, 0 differ;
  - modes and index equal HEAD;
  - no residue;
  - the gitlinks `external` `efeb541a` (not initialised), `gptp-processor` `5dce647a`, `protocol-processor` `c951a9ff` and `third_party/verilog-axis` `48ff7a7e` are each at stage 0 and clean.

## Findings

No MINOR, MAJOR or BLOCKER finding is open.

### Suggestions (non-blocking; they do not affect coverage)

- **S8 (Tests, Docs): the redacted R402-1 script no longer re-runs on the public packet.** `c0dfcb50:review-evidence/b1-r1/reviews/R402-1/scripts/rederive.py:15` now sets `HOST = "<controller-host-id>"`, but the public redacted packet `author-r2/r1/` spells the same identity `<controller-host-eui64>`.
  - Run against `author-r2/r1` as its `author/` root, the archived script gives 473 PASS and 10 FAIL. The 10 failures are exactly the host-identity checks.
  - With that one constant changed to the packet's placeholder, it gives 483 PASS and 0 FAIL (`receipts/r402_1_rederive_placeholder.txt`).
  - So the receipt's content is reproducible from public bytes. A one-line note in the archive, or a matching placeholder, would spare a cold reader a false failure. R402-1 is superseded, so this does not affect the current evidence.
- **S9 (Docs): the manifest does not record the kind of redaction.** In `MANIFEST.json`, the two token-redacted R402-1 rows carry `path_redacted: false` with `original_sha256 != published_sha256`, and no field says what was redacted. The change is inferable, and it is proven substitution-only above. A field such as `token_redacted` would make the row self-describing.
- **S10 (Docs): one line of the exposure record undersells `c816526d`.** The record groups `c816526d` with "the R402-1 receipt with the controller-host identity". It is a child of `92e1d7a3`, so it also serves the entire unredacted round-1 author packet (266 hits). The removal request is by SHA and already covers it, so this concerns only the description.
- **Retained unchanged from R403-2** (same head; outside this round's scope): S1 (Tests), S3 (Docs), S4 (Docs, manager: the findings index), S5 (Tests), S6 (Docs) and S7 (Docs).

## Resolution of my prior findings

| Finding | Status at `931c3edf` | Evidence |
|---|---|---|
| R403-1 F1-F4 / R403-2 answers | **Resolved** (R403-2 ledger, same head and tree, unchanged) | `receipts/verify_clone.txt`, diff stat |
| R403-2 F5 MINOR (Docs, Conformance) | **Resolved** | (a) and (b) above |

## Reviewer-owned completion ledger (this round)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | F5 required outcomes (a) and (b) against CONTRIBUTING.md section 6 and round-2 ruling 3: `receipts/private_tokens_branch_head_8563f65a.txt`, `private_tokens_pinned_c0dfcb50.txt`, `private_tokens_public_text.txt`, `evidence_branch_and_exposure.txt`. The live PR body's pin. Both pages, which are byte-unchanged at this head, re-scanned in `private_tokens_opening_and_pages.txt` | R403-3 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| RTL | CLEAN | `git diff --stat 13eda870..931c3edf`: two `docs/findings/` pages, no RTL path. The tree is identical to R403-2's (`receipts/verify_clone.txt`), so R403-2's cross-checks still stand on the same bytes: `KL_aecp_dyn_state.sv:266,292`, `KL_pp_shadow.sv:958-959`, REGISTER_MAP.md:2247 and :2253, and SAVED_STATE_SNAPSHOT_OWNERSHIP.md:992-999 and :1283-1285 | R403-3 (confirming R403-2 at the same tree) | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Robustness | CLEAN | Redaction robustness: 32 spellings including the modified EUI-64. The positive control reproduces 255 hits. Exposure completeness is checked against the push-activity log and all 572 ref tips, with anonymous by-SHA fetches of all six commits (`receipts/evidence_branch_and_exposure.txt`, `private_tokens_exposed_*.txt`). The repository scrub finds no new shapes (`scrub_branch_head_8563f65a.txt`) | R403-3 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Tests | CLEAN (S8 suggestion only) | `scripts/check_manifest.py` closure and diff: 0 mismatches at both commits (`receipts/manifest_check.txt`). `scripts/check_substitution.py`: substitution-only PASS (`substitution_check.txt`). Scanner control. The archived R402-1 `rederive.py` re-run on the public packet (`r402_1_rederive_placeholder.txt`). My archived R403-2 is byte-exact (`r403_2_archive_identity.txt`) | R403-3 | 931c3edfced972e01356cd989b5092a1672de5a3 |
| Docs | CLEAN (S9, S10 suggestions only) | The live PR body, which pins `c0dfcb50`. The exposure record 5886044527. `MANIFEST.json` rows at `c0dfcb50` and `8563f65a`. The pages at this head: the pinned Markdown environment gates all rc 0 (`receipts/doc_gates_pinned_env.txt`: `check_em_dash.py --base 13eda870`, 0 over 792 lines; `gen_toc.py --check`; `docs_check.py`; `check_doc_style.py`; `check_doc_paths.py`, 854 paths). System-interpreter gates in `doc_gates_system_python.txt`: `check_baremetal_only.py --check`, `docs_check.py` and `git diff --check`, all rc 0 | R403-3 | 931c3edfced972e01356cd989b5092a1672de5a3 |

## Validation run by the reviewer (foreground)

- **Token scans** (`scripts/scan_private_tokens.py`):
  - control `92e1d7a3`: 255, rc 1 as expected;
  - branch head: 0;
  - pin: 0;
  - opening commit and pages: 0;
  - public texts: 0;
  - the exposed commits: 255, 266, 11, 11, 11 and 11.
- **Other probes:**
  - `scripts/scrub_packet.py` (R403-2's, byte-identical): rc 0;
  - `scripts/check_manifest.py`: rc 0 twice;
  - `scripts/check_substitution.py`: PASS.
- **Markdown gates:** a private virtual environment installed with `--require-hashes` from `tools/markdown/requirements.txt` (cmarkgfm and html5lib versions recorded in the receipt). All rc 0. Under the system interpreter, `check_em_dash.py` and `gen_toc.py` exit 2 ("cannot judge": renderer absent), so they were judged in the pinned environment instead.
- **Hosted exact-head check runs** (read-only, `receipts/hosted_checks_931c3edf.tsv`, read 08:13Z): 21 completed success. The 1 skipped run is Physical gPTP (nightly and manual), which is not hardware proof. The contexts still in progress at R403-2 have now all completed successfully. The manager owns hosted and local-replica acceptance.
- **Clone:** `scripts/verify_clone.sh` rc 0 after removing the `scripts/__pycache__` that the gate runs created, which is ignored residue.

## Other public round-2 review (R402-2), read after the verdict and ledger above

I read [R402-2](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5886088523) (POSITIVE at `931c3edf`) after writing the verdict and ledger. Nothing in it changes them.

- **Its evidence basis.** R402-2 judged the packet at `04d00b66`, which was pinned before the rebuild, and used `92e1d7a3` for its redaction comparison. That records what the round judged; it is not a current-evidence citation by the PR. `receipts/manifest_check.txt` shows that `04d00b66..c0dfcb50` changes only the two R402-1 files and adds `reviews/R403-2/`. Every `author-r2/` byte R402-2 judged is therefore unchanged at the pin.
- **Its pending manager duties 1-2** (redact the R402-1 publication; the by-SHA fetchability of `92e1d7a3`) are the same subject as F5. They are closed by (a) and recorded by (b) above. Removal stays with the manager and owner.
- **Its S1-S3** (Tests/Docs; Docs; Docs) are suggestions and are **retained**. They do not affect coverage. Its S1 overlaps my retained R403-2 S5.

## Real limits

- Physical calibration NOT RUN. Field skips are not hardware proof. No bench access.
- Only GitHub's own push-activity log and the ref tips show that no other unreachable commit carries the tokens. Objects pushed to other refs, or never recorded in that log, were not searched.
- The rebuilt token list reproduces R403-2's control exactly, but it can only find tokens already known from the purged packet. The repository scrub's generic shapes are the second net.
- The private cold-storage copies were not read (manager duty). The manager's full source, static, builder and native banks were not re-run. Source validation is distinct from the final current-dev candidate.
- Objects were fetched only into scratch clones. The review clone's refs, index and worktree are unchanged.

## Pending manager duties

- Follow the owner's GitHub-side removal request for `92e1d7a3`, `c816526d`, `9660f038`, `9e135b46`, `04d00b66` and `fb6ff2f6` through to completion, or record an owner acceptance of the residual.
- Optionally, S8-S10.
- Confirm the private cold-storage copies against `author-r2/retention/MANIFEST.sha256`.
- Decide the sticky-`nvm_pend` issue: the next lane inherits pend 1 until a reset.
- Hosted and local-replica acceptance at the exact head.
- Build the final current-dev candidate: source base `13eda870`, live dev `57b8c867`.
- Add the findings index entry (S4).

R403-3 FINISHED
