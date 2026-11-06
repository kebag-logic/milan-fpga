[R763] POSITIVE - exact head 3e475161e528baa655a5ba84d6a38d78f8c64f3b

# R763-12: internal cleared-context review of PR #834 (issue #833), round 12

- **Head:** `3e475161e528baa655a5ba84d6a38d78f8c64f3b`, tree `e07572ea9d7973c84470cf63341597a47c4a0f95`.
- **Base:** dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`, which is also live remote dev at review time (`receipts/01_topology.txt`).
- **Delta reviewed:** `5843d1af..3e475161`. That is the merge `3f4e39f3` (dev `cc204c6f`: PR #836, the elaborate-gate split, and PR #815, the documentation audit) plus the regeneration commit `3e475161`.
- **Result:** no BLOCKER, MAJOR, MINOR or new RESIDUE. Two SUGGESTIONs. Prior RESIDUE and SUGGESTION items are retained, as listed below.
- **Lenses:** all five applied at this head: Conformance, RTL, Robustness, Tests, Docs.

## Reconstruction

- **Sources, in order:** AGENTS.md and CONTRIBUTING.md; issue #833's body and its comments; the PR body, read in full, with the Round 12 section in detail; issue #838; the diff `cc204c6f..3e475161` and the round 12 commits; then the published author packet `review-evidence/833-r1/author-r12/` at `a73ec2da`.
- **Prior findings:** I read the earlier review rounds only after my own pass over the delta.
- **Scope of round 12:** dev sync and inventory regeneration only. #833's frozen acceptance (state printed per descendant, and a fix or derived deadline backed by evidence) is unchanged. It was judged in rounds 1 to 11 on the four code and test files. Those files are byte-identical at this head, so those verdicts carry forward. The delta does not change anything they depend on (see Robustness).

## Check 1: the merge keeps both sides

- **Parents:** `3f4e39f3` has parents `5843d1af` (round 11's head, POSITIVE from both reviewers) and `cc204c6f` (dev).
- **Independent re-merge:** `git merge-tree --write-tree 5843d1af cc204c6f` gives tree `f3379b02`. That is exactly the recorded tree of `3f4e39f3`. The only message is `Auto-merging docs/testing/TESTING.md`, with rc 0 and no conflict. So the merge commit carries no change of its own. The handoff says there were no conflicts, so there is no resolution list to check against, and that matches (`receipts/02_merge_reproduction.txt`).
- **Files changed on both sides since `1f29f189`:** only `docs/testing/TESTING.md`.
  - Dev's hunks come from #737 (`7b5fd6f742`) and #829 (`d211219145`). They land at merged lines 724, 774, 793-796 and 798-803, which are dev's lines 640, 690, 709 and 714 shifted by the PR's +84.
  - The PR's hunks are at lines 217-364, so the two sides are disjoint (`receipts/13_docs_claims.txt`).
- **Stable patch-id:** `git diff 1f29f189 5843d1af` and `git diff cc204c6f 3f4e39f3` both give `a5e12980a28b73885022d9b0d029df8f1555af6e`. So the PR's change against its base is the one round 11 reviewed.
- **Blob checks:**
  - The four non-TESTING PR files have the same blobs and modes (100644) at `5843d1af` and at HEAD.
  - All 67 dev-side files except TESTING.md are blob-identical to `cc204c6f`.
  - The six submodule gitlinks equal dev's.

## Check 2: regeneration only through `scripts/docs_inventory.py`

All results are in `receipts/03_docs_inventory_regen.txt` and `receipts/04_testing_md_counting.txt`.

- **The generator is dev's:** `scripts/docs_inventory.py` (`fe9cbbc5`) and `scripts/docs_inventory.json` (`242c0553`) are blob-identical at dev, at the merge and at HEAD.
- **At the merge `3f4e39f3`, in a fresh disposable clone:**
  - `--check` gives rc 1, `STALE (4 lines differ)`, first at line 31 (`10,638` to `10,722`).
  - Then `--write` gives rc 0, a 4-line diff, and only `docs/DOCUMENTATION_AUDIT.md` modified.
  - My regenerated page is blob `9fdb8bf4`, byte-identical to the committed page at HEAD (`cmp` silent).
  - The author's published `regen.diff` is byte-identical to `git diff 3f4e39f3 3e475161`.
- **At HEAD, in a fresh clone:**
  - `--check`: rc 0, `OK (540 lines, docs/DOCUMENTATION_AUDIT.md is fresh)`.
  - `--selftest`: rc 0, `OK (50 controls)`.
  - `--write` leaves `git status --porcelain` empty, and the `--check` after it gives rc 0.
- **TESTING.md is counted by the generator's own rules:**
  - Row line count: 2019, which equals `wc -l` at HEAD (dev 1935, round 11 2011, merged 2019).
  - Status stays `stale` through D0-057. The generator locates the finding by its quote at every head (`docs_inventory.py:25-26`, `locate()` at `:357`). The quote's only occurrence at HEAD is line 1902, the same statement as dev's line 1818.
  - Bucket sums recomputed from the Inventory rows: current 176 / 73,487, stale 16 / 10,722, obsolete 21 / 8,002, total 213 / 92,211. These match the summary table. The stale delta, +84, equals 2019 - 1935.

## Check 3: one merge base; docs workflow and the two changed tests pass

- **Merge base:** `git merge-base --all HEAD cc204c6f` gives one base, `cc204c6f`. `git diff --check cc204c6f HEAD` gives rc 0 (`receipts/01_topology.txt`).
- **The two tests, run myself at HEAD** on a fresh clone, run concurrently, with SigIgn 0 and host load 48 to 68 on 16 CPUs (`receipts/06_*`):
  - `python3 scripts/test_suite_cancellation.py`: rc 0, `suite cancellation: PASS (...)`, 60.0 s.
  - `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle`: rc 0, `mutant lifecycle: PASS (...)`, 39.4 s.
- **What dev changes under these tests:** dev's delta does not touch `owned_process.py`, `process_test_support.py`, either test, or `tb/verilator/gptp_shadow/mutants.py`. Dev does touch `KL_gptp_shadow.sv` and `gptp_shadow_wrap.sv` (#829). The lifecycle pass above runs on that merged tree (`receipts/07_dependency_check.txt`).
- **Docs workflow, from the author's published receipts:**
  - Packet integrity: all 244 `author-r12/` files were fetched at `a73ec2da`. Every git blob hash matches, and every `MANIFEST.json` `published_sha256` matches. 0 mismatched and 0 unlisted. 100 entries are marked path-redacted (`receipts/10_evidence_manifest_verify.txt`).
  - My own verifier (`scripts/verify_docsyml_receipts.py`) parses `.github/workflows/docs.yml` at HEAD from git, not from the packet. It gives:
    - 64 steps with rc 0 and the head SHA in the log's first line;
    - 31 not run, each with a stated reason (hosted step context, apt or sudo installs, CI orchestration);
    - 1 step, `docs-gates-2/gate_41`, whose rc file reads 0. Its 354,249-byte log is published only as a tail, with its sha256 in `LARGE-LOGS.txt`. The tail ends `selftest: PASS (2207 contract items, 5501 arms)`.
  - So the author's `65 ran, 31 not run, 0 bad` reconciles (`receipts/05_docsyml_receipts_verify.txt`).
  - Dev's new inventory step `docs-gates-0/gate_46` printed inventory OK and selftest OK (50 controls). The renumbered `ci_step_55` keeps round 1's reason.
  - The discarded first attempt (`attempt-sdk-copied/`, `ci_step_28` rc 1, `SDK provenance mismatch` from a copied SDK cache) is disclosed in the handoff and is not the run counted.
- **Image command-table checker (#838):** it refuses identically at HEAD and at dev, before any pin is compared. See the next section for the pins.

## The command table: does this PR add a mismatch?

- **Re-counted at the merge** (`receipts/08_command_table_pins.txt`, `09_command_table_pins_all.txt`, `scripts/command_table_pins.py`, submodule paths read through their gitlinks):
  - dev `cc204c6f`: 34 stale script pins plus 1 absent file. This agrees with #838's 34 + 1.
  - HEAD: 38 stale plus 1 absent.
- **The 4 extra rows** are `scripts/owned_process.py`, `scripts/process_test_support.py`, `scripts/test_suite_cancellation.py` and `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`. All four match their bytes at dev and differ at HEAD. `ci_command_table.py:219-220` would refuse them as `changed declared script` once #838 unblocks the parser pin.
- **These are not new to round 12.** The same 4 rows were stale at round 1's head. Leaving the table unregenerated was a public decision that both round 1 reviews accepted, because regenerating it would rewrite about 34 unrelated pins. The PR body's Known limitations bullet discloses it, and its figures (34 on dev, 38 here) still hold at the merge.
- **The delta adds no row and changes none of these four.** Dev's newly declared rows, for #836 and #815's `scripts/docs_inventory.py`, match their bytes at HEAD.
- **Verdict:** the decision is retained, not a finding. Sequencing note: R763-12-S1.

## Findings

### R763-12-S1 - SUGGESTION - Docs - PR body, Known limitations, `ci/image/command-table.json` bullet
- **Evidence:** the bullet predates #838 and does not cite it. Its figures are stated "at round 11's head, not re-measured on the round 12 merge". I re-measured them at the merge: 34 + 1 on dev `cc204c6f` and 38 + 1 at this head, so they still hold.
- **Impact:** none on behaviour. #838's acceptance item 3 will make a stale digest fail "the PR that made it stale". Whichever of #834 and #838 lands second has to carry these 4 rows.
- **Optional change:** cite #838 as the tracker in that bullet, and say the 4 rows are this PR's and are absorbed by #838's regeneration, or re-pinned here if #838 lands first.
- **Verification:** read the PR body. Running `scripts/command_table_pins.py <repo> <head>` names the 4 rows.

### R763-12-S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md:27` (generated, dev-owned, outside #833)
- **Evidence:** the caption reads "Findings cite source lines at dev `1f29f189`" (from `docs_inventory.json` `cited_at`, rendered at `docs_inventory.py:585`). But each finding's Line column is located at the rendered head: D0-057 now shows 1902, which is HEAD's line, not `1f29f189`'s. The caption is meant for the "contradicted by" source citations, and that reading is defensible.
- **Impact:** none for this PR. The bytes are the generator's own output.
- **Optional change:** for #797's owner, not this lane. The caption could say the Line column is located at the rendered head.
- **Verification:** not required here.

### Comment rule
- The delta's only non-merge content is the generated page. It contains no source comment, lane label, round, reviewer ID or comment ID (`receipts/13_docs_claims.txt`).
- Both commits are one line with no trailers.
- The merge introduces no author-written line, because its tree equals the automatic merge.

## Prior findings at this head

| ID | Severity | Status at `3e475161` | Evidence |
|---|---|---|---|
| R763-11-R1 | RESIDUE | RETAINED, untaken, for the manager's residue checklist. "has grown by the second pass" is still at `docs/testing/TESTING.md:298` and `scripts/test_suite_cancellation.py:779`. The line numbers are unchanged by the merge (dev's hunks start at line 724), so round 11's exact fix applies verbatim | `receipts/12_prior_findings_check.txt` |
| R763-11-S1 | SUGGESTION | RETAINED, not taken (no `stubborn_parent_beside_under_shell` key). Optional | same |
| R764-11-S1 | SUGGESTION | RETAINED, not taken. `test_suite_cancellation.py:827` loop still has no comment of its own. Optional | same |
| R763-10-R2, R764-10-R3 | RESIDUE | RETAINED as round 11 recorded them. Out-of-domain sweep classes for #495; the code is unchanged | blob identity, `receipts/02_merge_reproduction.txt` |
| R764-6-S1 | SUGGESTION | RETAINED, not taken, outside #833 | PR body round 11 table |
| Round 1 command-table decision (R763-1 item 6, R764-1 item 6; R764-1-F4 and R763-1-X2 resolved in round 2) | DECISION ACCEPTED | RETAINED. The delta adds no mismatch, and the figures hold at the merge. #838 now tracks dev's drift, which answers R763-1-S1's ask for an Issue | section above |
| Every earlier MINOR or higher (rounds 1 to 10) | - | Resolved as round 11 recorded. The code they concern is byte-identical at this head | blob identity |

## Lens results

| Lens | Result | Artifact at `3e475161` | What was checked |
|---|---|---|---|
| Conformance | PASS | issue #833 acceptance; `git diff cc204c6f 3e475161` (6 files); `receipts/02`, `08`, `09` | Acceptance is unchanged and still served by byte-identical code (stable patch-id `a5e12980`). The scope rule "merge plus regeneration, no other file" holds. Command-table decision retained, no new mismatch |
| RTL | PASS | `git diff --stat cc204c6f 3e475161` (no `hdl/`, `tb/**/*.sv` or `syn/` path); dev's `KL_gptp_shadow.sv` and `gptp_shadow_wrap.sv` blob-identical to `cc204c6f` | The PR carries no RTL. Dev's RTL enters unmodified, its contracts are dev's, and the lifecycle harness over it passes |
| Robustness | PASS | `scripts/owned_process.py` `6495a47b`, `scripts/process_test_support.py` `a981083e`, both tests: blobs identical to round 11's head; `receipts/06_*`, `07` | No cleanup, deadline or refusal path changed. Dev touches none of their imports. Both tests green at load 48 to 68. The round 11 robustness verdict carries forward |
| Tests | PASS | `receipts/03`, `05`, `06`; author `author-r12/receipts/gates/` (hash-verified) | Inventory `--check` rc 1, then `--write`, then `--check` and `--selftest` rc 0, all reproduced. The two changed tests pass. docs.yml receipts reconcile 65 / 31 / 0 against the workflow at HEAD |
| Docs | PASS (2 SUGGESTIONs) | `docs/DOCUMENTATION_AUDIT.md` blob `9fdb8bf4`; `docs/testing/TESTING.md` (2019 lines); PR body Round 12 section; `receipts/04`, `13` | Page byte-identical to my regeneration. TESTING.md has both sides, counted by the generator's rules. Every Round 12 PR-body figure checked: 1935 to 2019, 1818 to 1902, 10,638 to 10,722, 92,127 to 92,211, 213/176/16, patch-id, one merge base, the #838 refusal |

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #833 acceptance; merge reproduction; patch-id; command-table pin census | R763-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| RTL | CLEAN | PR diff (no RTL); dev RTL blob identity; lifecycle run on merged tree | R763-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Robustness | CLEAN | owned-process code and test blobs identical to round 11; dependency check; both tests under load | R763-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Tests | CLEAN | inventory check/selftest/write reproduction; the two tests; docs.yml receipt reconciliation | R763-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |
| Docs | CLEAN | regenerated audit page; merged TESTING.md; PR body Round 12; R763-11-R1 retained as RESIDUE | R763-12 | `3e475161e528baa655a5ba84d6a38d78f8c64f3b` |

## Real limits

- **docs.yml and the builder legs:** I did not re-execute docs.yml or the builder legs. That evidence is the author's published, hash-verified receipts, reconciled by my own verifier against the workflow at HEAD.
- **`gate_41`'s full log:** it is not published, only its tail and sha256, so the full log's hash cannot be checked from the packet.
- **The evidence packet:** it is bound by git blob hashes and `MANIFEST.json` digests at commit `a73ec2da`. I found no cryptographic signature to verify.
- **Not rerun this round:** `--mutants`, `--matrix`, `behave` and the full sweep. Round 12 does not change their inputs within this PR, and dev's inputs belong to the merge-turn bank.
- **Each test ran once,** on a shared host at load 48 to 68. One green run is not a load-distribution claim.
- **No manager source bank** runs at this head, and I claim none.
- **Hosted contexts:** a read-only snapshot shows most still queued or in progress (`receipts/11_hosted_checks_snapshot.txt`). `Physical gPTP (nightly and manual)` is skipped, which is not execution. I make no hosted acceptance claim.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **The command-table checker** cannot run past its parser-pin refusal on this host (#838).

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Own hosted and act acceptance at the exact head: `rtl-fast` and, once the PR is ready, `verilator-suites` and `yosys-portability`.
- Carry R763-11-R1 (and R763-10-R2 and R764-10-R3) to the residue checklist.
- Sequence #834 against #838 for the 4 command-table rows (R763-12-S1).
- Obtain the external review's verdict at this head. Merge needs explicit maintainer authorization.

## Probe hygiene

All probes ran in disposable clones under the packet's `scratch/`. The review clone is unchanged:
- HEAD `3e475161`;
- index tree `e07572ea`, which equals HEAD's tree;
- `git diff-index` quiet, porcelain empty;
- index modes and blobs equal to `ls-tree HEAD`;
- all six submodule gitlinks as recorded (`receipts/14_clone_integrity.txt`).

R763-12 FINISHED
