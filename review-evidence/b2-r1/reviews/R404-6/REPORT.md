[R404] POSITIVE - exact head d62b1e1a3a37283ebad039880163873698a011db

# R404-6: delta confirmation of PR #622 after the dev merge

Issue #606, PR #622, bench lane B2. This is an internal, independent review from a cleared context. The head is `d62b1e1a3a37283ebad039880163873698a011db`, tree `b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59`, the manager's "Merge dev into b2-bench-0929" commit. Its parents are the R404-5 POSITIVE head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` and the dev tip `79c36963660c10e4c1c11a744fb5bff41a552b8b`. The PR's previous base was `13eda870d1a6cf3f946fc228a98862366b08d102`, which is `merge-base(5c579274, 79c36963)`.

The verdict is POSITIVE. No BLOCKER, MAJOR or MINOR finding is open under any lens. Two optional SUGGESTIONs are carried.

## What was read, in order

1. AGENTS.md (CONTRIBUTING.md governs it), docs/README, and the findings index `docs/findings/README.md` at head.
2. Issue #606: the body, the [A10] analysis 5860869610, the B2 assignment 5885087413, the round-4 assignment 5889146437 and [A449] REVIEW READY 5889299853. PR #622's live body, which states the scope: evidence only, two findings pages and their index rows, relating to #606, #608 and #75 and closing none.
3. The linked authorities, through the pages' own links: `75_RECONNECT_RESTART_MEASUREMENT.md#method`, `117_GPTP_SILICON_EVIDENCE.md`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11, `TESTING.md` section 6b, and the processor pin `c951a9ff` recorded as a gitlink.
4. `git diff 79c36963..d62b1e1a`, `git diff 13eda870..5c579274`, `git diff 5c579274..d62b1e1a`, the three-way README, `git show --remerge-diff d62b1e1a`, and dev's own delta `13eda870..79c36963`, which is 29 commits from PRs #616, #618, #619 and #620.
5. Public evidence: `review-evidence/b2-r1/author/` at `666d8897`, fetched read-only, and the exact-head hosted check runs.
6. Prior public review findings on PR #622, read only after checks 1 to 6 below were complete and no finding of my own was open.

## Checks

### Check 1: the merged delta is this PR's reviewed content, file for file

This is the manager's item (1). Receipt: `receipts/delta_check.txt`, produced by `delta_check.sh`.

- `git diff --name-status 13eda870 5c579274` and `git diff --name-status 79c36963 d62b1e1a` list the same three paths: `A docs/findings/606_FIRST_BIND_MEASUREMENT.md`, `A docs/findings/608_75_WITHDRAWAL_AND_RESTART.md` and `M docs/findings/README.md`.
- Both pages are blob-identical between `5c579274` and `d62b1e1a`. Their patches are identical, and each is mode 100644 on both sides.
- `docs/findings/README.md` is the only file that differs, as expected.
  - `git diff 5c579274 d62b1e1a` on it is exactly one added line, dev's `451_TDM8_FIRST_LIGHT.md` row.
  - `git diff 79c36963 d62b1e1a` on it is exactly this PR's change: the #75 row is replaced, and the 606 and 608 rows are added.
  - A scripted assertion compares the head README with the PR's README plus dev's added lines (exactly 1) inserted directly above the #75 row, and they are byte-equal.
  - `--remerge-diff` shows that the one conflict was resolved by keeping dev's 451 row above the PR's three rows. Dev's old #75 row was dropped in favour of the PR's reviewed #75 row.
  - No dev line was removed from the README.

### Check 2: everything else at head is dev's content only

This is item (2). Same receipt.

- `git diff --name-status 5c579274 d62b1e1a` and `git diff --name-status 13eda870 79c36963` are the same 62-path list, 11 added and 51 modified.
- Outside the README, every path at head has the same blob as at `79c36963`, and each mode matches. That includes `sw/litex/sweep_extra.sh` at 100755.
- Whole tree: of the 977 paths at head, none is anything other than dev's entry or this PR's entry, apart from the README.
- The gitlinks `external` `efeb541a`, `gptp-processor` `5dce647a` and `protocol-processor` `c951a9ff` are identical at `13eda870`, `79c36963`, `5c579274` and head.
- There are 0 conflict markers in tracked text. The README table has 12 rows, each with three cells and no duplicate target (`receipts/merge_robustness.txt`).

### Check 3: dev's content neither contradicts nor stales the 606/608 pages or the #75 row

This is item (3), checked independently. Receipt: `receipts/staleness_check.txt`, produced by `staleness_check.sh`.

- **References.** Dev added no tracked line naming the 606/608 pages or issues #606/#608. There are 41 such lines at both `13eda870` and `79c36963`. The only dev lines naming #75 are on the B1 page, `599_394_E1_LINK_CYCLES.md:157` and `:228`. They say its link-cycle timings "differ in trigger, so this is no #75 verdict", so the PR's #75 row and the #608/#75 page are not contradicted.
- **Image identity.** The B1 page, landed by dev, records the same image as the 606 page:
  - VERSION `0x00020060`, and ROM/QSPI/AEM CRCs `acad92b9`, `d84bce7b` and `93742dd2`;
  - bitstream, AEM and CSR SHA-256s `690d87e4...`, `9b077636...` and `7723d0b8...`;
  - entity `020000fffe000001`, `census_compare.py` `f014c6f2...`, and UART grader `bc41ab03...`. The grader's bytes are unchanged from `13eda870` through head (`receipts/evidence_crosscheck.txt`).

  Dev's CHANGELOG keeps VERSION `0x0002_0060` for its later RTL. The pages identify the image by CRCs and by its named source `13eda870`, not by VERSION alone, so that change does not blur the identification.
- **Saved state.** B1's final restore (`599…:291-296`, 06:22Z) reads slots 229 / 230, image 230, commits 2 / 0, `PP_STAT` `0x5b000c44` with `nvm_pend` 1, and `PP_NVM_STAT` `0xc34000e4`. That equals B2's identity-gate column (`606…:247-253`, 06:49:58Z). The page says `nvm_pend` 1 was inherited from lane B1, and the landed B1 page now shows it in-tree.
  - B1 attributes its two commits to the DUT-listener bind and unbind. The DUT-talker CONNECT_RX to the peer committed nothing on the DUT. This agrees with the 606 page's "binding records are indexed by the DUT's stream inputs".
- **Timing.** B1's restore unbind was at 06:22:05Z, and B2's first action console sample was at 06:53:46Z, 1,901 s later. That is consistent with bind 1's "more than 1,800 s (lane B1's restore)" (`606…:164`).
- **Stream outputs.** B1 bound only DUT Output 1 (`599…:69`), so Output 0 was bound in neither lane on this image. That is consistent with `606…:78-84`, which says Output 0 held a MAAP destination it had not been bound for, and that the acquisition predates the lane and was not observed.
  - Dev's 451 page records Output 0's address as allocated at first probe on image `9e9954e9`. That is a different image, and it agrees with the 606 page's statement that `9e9954e9` read all-zero at the #75 start census.
- **Bench state.** The peer was in configuration 1 at 48 kHz, 18 of 18 stream states were unbound as found, and the reset epoch was 1 in both lanes.
- **Processor state.** The processor gitlink is unchanged by dev (`c951a9ff`). Processor PR #133 is still OPEN and unmerged, and processor issues #108 and #134 are OPEN (`receipts/external_state.txt`). So the #608 page's "met without qualification only after the pin adoption of #133 and a 100-cycle re-run" is still accurate at the dev tip.
- **Dev RTL.** Dev's RTL delta is `KL_chan_map_capture.sv` (frame-atomic TDM capture), `KL_media_grid_align.sv` (comment only) and `KL_media_nco.sv`. The NCO's terminal compare changes from `==` to `>=`, which is equivalent at constant trim. Dev also changed `milan_datapath.sv`: the TDM frame-pairs parameter, and the aligner's marker, tick delay and keep-off. None of these touches ACMP, MSRP, MAAP, the CRF talker licence or STREAM_STOP. The aligner only engages under a CRF clock selection, and both pages measured with the DUT on INTERNAL (`606…:72`, `:231`). In any case, the pages are records of the named `13eda870` image, which later RTL cannot alter.

R405-6's composition review found no contradiction. Independently, I **confirm** that.

### Check 4: documentation gates at head

Receipt: `receipts/doc_gates.txt`, produced by `doc_gates.sh`. The pinned Markdown environment was `cmarkgfm 2025.10.22` and `html5lib 1.1`, in a disposable environment.

- `docs_check.py` found 0 findings.
- `check_doc_style.py`, `gen_toc.py --check` and `check_doc_paths.py` (860 paths) passed.
- `check_em_dash.py --base 79c36963` found 0 over 914 added lines, and `--base 13eda870` found 0 over 2,548.
- `ci_scope.py --selftest`, `check_feature_status.py --self-test`, `git diff --check` over `79c36963..HEAD` and `5c579274..HEAD`, and a clean worktree all passed, rc 0.
- `check_baremetal_only.py --check` returned rc 2 in the pinned environment because pyyaml is absent there. That is environmental. A re-run with pyyaml 6.0.3 was OK: 0 findings over 947 files, rc 0.

Every relative link and anchor in both pages and the README resolves at head. That includes the two links into files dev changed, `TESTING.md#6b-bench-evidence-retention` and `451_TDM8_FIRST_LIGHT.md` (`receipts/link_targets.txt`).

### Check 5: public evidence still binds the pages

Receipt: `receipts/evidence_crosscheck.txt`.

- Ten tool blobs in `review-evidence/b2-r1/author/tools/` at `666d8897` hash exactly to the 606 page's tool table (`606…:312-330`). The 608 page defers to that table at `:456`.
- The archive's `identity/image-sha256.txt` carries the page's bitstream, AEM and CSR SHA-256s.
- The pages are byte-identical to the heads at which that binding was reviewed.

### Check 6: the delta check fails on each fault it claims to detect

Receipt: `receipts/mutation_probes.txt`, produced by `mutation_probes.sh`. Eight mutant merge commits were built in a disposable clone. The unmutated control reproduces tree `b4a1f5ed` and PASSES. Each mutant FAILS, naming its fault:

- a one-token edit to the 606 page;
- the README with dev's 451 row dropped;
- the README resolved to dev's side, which keeps the old #75 row;
- the 451 row placed after the PR's rows;
- dev's `milan_datapath.sv` reverted to `13eda870`;
- a moved `protocol-processor` gitlink;
- `sweep_extra.sh` losing mode 100755;
- a stray extra file.

### Hosted evidence (inspected, not accepted)

`receipts/hosted_checks.tsv` records the exact-head check runs on `d62b1e1a`.

- Eight executed and succeeded: `changes`, `docs-check`, `docs-check-no-git`, `rtl-fast`, `elaborate`, `bdd-conformance`, `wire-accountability` and `full-ci-gate`.
- Seven were skipped: `verilator-lint`, `verilator-suites`, `yosys-elaboration`, `yosys-portability`, both shard templates, and the physical gPTP context.

The skips match `ci_scope.py` over `git diff --no-renames --name-only 79c36963..d62b1e1a`, which classifies the PR's three paths as documentation only (`false`, `receipts/ci_scope.txt`). A skipped context is not executed evidence, and a physical skip is not hardware proof. Hosted and act acceptance belong to the manager.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 SUGGESTION (Docs): point the B1 cross-references at the in-tree B1 page

- **Where:** `docs/findings/606_FIRST_BIND_MEASUREMENT.md:42`, `:74` and `:287`, and `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:430`.
- **Evidence:** these lines cite lane B1's identity and final restore through PR #620 only. With dev merged, that record is in-tree at `599_394_E1_LINK_CYCLES.md` (`#identity-and-setup`, `#saved-state-layer`), and its values agree (check 3).
- **Impact:** none on correctness. A reader must leave the tree to follow the inheritance.
- **Outcome (optional):** add in-tree links in a later docs change. This concurs with R405-6 S1.

### S2 SUGGESTION (Docs, carried from R405-2 S4 / R405-3 S2 / R405-5 S2): processor PR #133 described in the present tense

- **Where:** `608…:32` ("implements") and `:229` ("adds").
- **Evidence:** processor PR #133 is still OPEN and unmerged at review time (`receipts/external_state.txt`). The surrounding lines make adoption and a re-run the condition, so nothing claims it landed.
- **Outcome (optional):** "proposes" wording, or leave as is.

## Prior public findings at this head

Prior findings were read after checks 1 to 6. Each disposition rests on the blob identity in check 1: both pages are byte-identical to `5c579274`, and the README's PR rows are unchanged.

| Prior finding | Disposition at `d62b1e1a` |
|---|---|
| R404-1 F1-F4, R405-1 F1-F4, MINOR (Conformance, Docs) | Remain resolved (resolved at `d7676373`). The page text they cover is byte-identical at head. |
| R404-2 F5, R405-2 F5, MINOR (poll count) | Remain resolved. `606…:267-269` is unchanged. |
| R404-3 F6, R405-3 F6, MINOR (census premise) | Remain resolved. `606…:277-279` is unchanged. |
| R404-4 F7, R405-4 F7, MINOR (PR-body census clause) | Remain resolved. The live PR body still reads "210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input, and no AECP write". |
| R405 S2 (#133 tense) | Retained as the optional S2 above. |
| R405-6 S1 (B1 cross-references) | Concurred, as the optional S1 above. |

## Per-lens results

[R404] PASS Conformance — `receipts/delta_check.txt`, `receipts/staleness_check.txt`, `606…:13-20,40-84,247-287`, `608…:28-36,63-69,420-430`, README rows 11-14, PR body — the merged delta matches the reviewed #606 item 3 / #608 item 3 / #75 verdicts byte for byte. Dev's B1 and 451 pages and its RTL contradict none of them, and B1 explicitly makes no #75 verdict.

[R404] PASS RTL — `git diff 13eda870 79c36963 -- hdl` (`KL_chan_map_capture.sv`, `KL_media_nco.sv`, `KL_media_grid_align.sv`, `milan_datapath.sv`), gitlinks at four commits — the PR adds no RTL. The RTL at head is dev's blob for blob, and the gitlinks are unchanged. Dev's RTL changes the TDM capture, the NCO compare and the aligner, not the CRF talker bind, withdrawal or STREAM_STOP path the pages measured on INTERNAL.

[R404] PASS Robustness — `receipts/merge_robustness.txt`, `receipts/mutation_probes.txt`, `git show --remerge-diff d62b1e1a` — the single conflict resolved to the union: no dev line lost, no duplicate row, no conflict marker, modes and gitlinks preserved. Eight classes of merge fault are each detected.

[R404] PASS Tests — `receipts/mutation_probes.txt`, `receipts/evidence_crosscheck.txt`, `receipts/doc_gates.txt` — this review's delta check fails on 8 of 8 planted faults and passes the control. The pages' tool hashes re-derive from the public archive. The documentation gates are rc 0 at head. The PR adds no executable test, so none can be weakened.

[R404] PASS Docs — `docs/findings/README.md` at head, `receipts/link_targets.txt`, `receipts/doc_gates.txt`, the PR body — the index keeps dev's 451 row and the PR's three rows, all links and anchors resolve, the pinned Markdown gates are clean, and the PR body's "no other change" is true against dev `79c36963`. Only the two optional suggestions remain.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merged delta against the reviewed content; 606/608 pages; README rows; PR body; dev's B1, 387 and 451 pages; processor PR/issue state | R404-6 | `d62b1e1a3a37283ebad039880163873698a011db` |
| RTL | CLEAN | Dev's `hdl/` delta; gitlinks at `13eda870`, `79c36963`, `5c579274` and head; ci_scope classification | R404-6 | `d62b1e1a3a37283ebad039880163873698a011db` |
| Robustness | CLEAN | Merge resolution (remerge-diff); whole-tree path/mode/gitlink comparison; conflict markers; README table shape; mutation probes | R404-6 | `d62b1e1a3a37283ebad039880163873698a011db` |
| Tests | CLEAN | `delta_check.sh` against 8 mutants plus a control; archive tool-hash re-derivation; doc gates | R404-6 | `d62b1e1a3a37283ebad039880163873698a011db` |
| Docs | CLEAN (S1, S2 optional) | README at head; link/anchor resolution; pinned Markdown gates; PR body | R404-6 | `d62b1e1a3a37283ebad039880163873698a011db` |

## Limits

- The scoped simulator named in the review brief was not present at its stated path, so its identity could not be verified and no simulation was run. None was needed: the delta carries no PR-owned RTL, and dev's RTL is blob-identical to dev.
- No full parent, PP, gPTP, Yosys, builder or native bank was run, and neither act nor the host runner was run. Those are the manager's. The 48/48 builder, 5/5 native, act and hosted results were not re-executed here.
- Physical calibration was NOT RUN. Field and hosted physical skips are not hardware proof. This review repeats no bench measurement; the page values are checked for consistency, not re-measured.
- Only the round-1 `author/` packet at `666d8897` was fetched. Raw captures are outside the repository and were not accessed.
- The `external` submodule is not initialised in the review clone. Its gitlink was checked as a recorded object id only.
- The pinned Markdown environment lacked pyyaml, so `check_baremetal_only.py` was re-run with pyyaml 6.0.3 (rc 0).
- The README has no normative row order. Placement was checked against the brief's stated resolution only.

## Pending manager duties

- Build and validate the final current-dev merge candidate at the merge turn. The source base and live dev are both `79c36963` at review time; if dev moves, the delta relation in checks 1 and 2 must be re-established.
- Own hosted and act acceptance at the exact head.
- Merge only with explicit maintainer authorisation, then run post-merge containment.
- The PR closes no issue. Still open:
  - #606's post-reset allocation path is not exercised on the bench;
  - the #608 100-cycle re-run after processor PR #133's pin adoption;
  - AAF under #75 is unmeasured.

## Clone restoration

`receipts/verify_clone.txt`, produced by `verify_clone.sh`, confirms the clone state after all probes:

- HEAD is `d62b1e1a` and the tree is `b4a1f5ed`;
- 0 status lines, worktree equal to index, index equal to HEAD;
- 977 index entries equal the tree, and 973 files were re-hashed with 0 byte or mode mismatches;
- the gitlinks `efeb541a`, `5dce647a` and `c951a9ff` are as recorded.

All probes ran in a disposable clone under `scratch/`, which is not published.

R404-6 FINISHED
