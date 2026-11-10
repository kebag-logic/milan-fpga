[R809] POSITIVE - exact head 14492f87db567b4c4102d8c171b8b3b054f3098a

# R809-3: delta review of processor issue #217 / PR #219 at the merge head

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #219 (base `main`), issue #217 (parent kebag-logic/milan-fpga#858).
- Exact head `14492f87db567b4c4102d8c171b8b3b054f3098a`, tree `ca0937b08dff8ec148cd74021d0b99815bcfeea8`. This is a merge. Its parents are `fd2d8d2e3facaf5dd6c97a9cf760657e50e0e72f` (the PR side) and `45f03e042bdb4391af2136ef7b4989c356277256` (`main`, PR #218 merged).
- Previously reviewed head: `794f8442c3d9da158c99d358d825c7b277516bba`. R809-2 and R810-1 were POSITIVE there. Original source base: `044cb25f4ed2187bd238490650e73d5d189855d1`.
- Scope (delta round): the two commits since `794f8442`, every named prior finding at its cause, and the three suites plus the parent idiom gate at this head. Code the delta does not touch keeps its prior lens verdict, because nothing it depends on changed (section 3).
- Order followed: the parent's AGENTS.md section 6 and CONTRIBUTING.md, `docs/README.md`, the issue's acceptance, the manager's round-3 notes (issuecomment-6758084284, -6759589148), the diffs and history, then the public evidence. I wrote my own verdict and ledger (`receipts/verdict_ledger_first.txt`, 2026-11-10T06:32:58Z) before I read any prior review report.

## 1. Claim (1): `fd2d8d2` is one line and changes no value

- `git diff 794f8442 fd2d8d2` (`receipts/delta_794f844_fd2d8d2.diff`) is one file and one hunk with one line changed. At `tb/pp_top/sim_main.cpp:855`, `uint32_t adp_last_aidx[4] = {0, 0, 0, 0};` becomes `uint32_t adp_last_aidx[4] = {};`. Nothing else changes, and the comment above the line is untouched.
- Semantics. This is a default member initializer of an array aggregate. Under C++17 [dcl.init.aggr], an empty brace list initializes every element from an empty initializer list, which value-initializes it, so all four `uint32_t` are 0. The explicit form also gives 0, 0, 0, 0. `scripts/init_equiv.cpp` checks both forms in one struct each with `static_assert` at `-std=c++17 -Wall -Wextra`. It compiles with no warning and runs to rc 0 (`receipts/init_equiv.txt`).
- The bench also clears the array at every harness reset (`for (uint32_t& a : adp_last_aidx) a = 0;`, unchanged). So the initializer only covers the time before the first reset, and both forms give the same value there. No expectation in the suite changes. Measured: the pp_top builds at this head give the same per-build totals as `794f8442`, apart from #218's two checks (section 3).
- The parent gate, with a control probe. The scratch parent is milan-fpga dev `123f57a922bf07476cd69f91867f3b6f07080804` plus one local commit, never pushed, that sets the `protocol-processor` gitlink to `14492f87`. `gptp-processor` sits at its pin `1616fc8f`. Both submodules are clean and at their pins (`receipts/cpp_idiom_head.txt`).
  - `python3 scripts/check_cpp_idiom.py` reports 353 translation units, every refused construct at 0 and every ratchet at 0 <= 0. It exits **rc 0**.
  - `--selftest` reports 75 of 75 and rc 0 (`receipts/cpp_idiom_selftest.txt`).
  - Control (`receipts/cpp_idiom_control_probe.txt`): line 855 put back to `= {0, 0, 0, 0};` in the submodule worktree gives `FAIL: multi-declarator declaration 1 > ratchet 0`, rc 1, with `--list` naming `protocol-processor/tb/pp_top/sim_main.cpp`. After the restore the worktree has 0 dirty entries and the gate is back to rc 0. So the gate does read this line, and `fd2d8d2` is what makes it pass.

## 2. Claim (2): the merge `14492f8` has no hand resolution

- Replay. `git merge-tree --write-tree fd2d8d2 45f03e04` (git 2.56.0) exits 0 with no conflict and writes tree `ca0937b08dff8ec148cd74021d0b99815bcfeea8`. That is byte-for-byte the head's tree (`receipts/merge_tree_replay.txt`), so the committed merge is the automatic merge.
- Side by side (`scripts/compare_sides.sh`, `receipts/compare_sides.txt`, rc 0). Index lines and hunk-header offsets are dropped, and then:
  - `git diff 45f03e04 14492f87` is IDENTICAL to `git diff 044cb25f fd2d8d2`. #219's full patch lands on `main` unchanged.
  - `git diff fd2d8d2 14492f87` is IDENTICAL to `git diff 044cb25f 45f03e04`. #218's full patch lands on #219 unchanged.
  - **No hunk differs.** The four raw side diffs are in `receipts/side_*.diff`. The first-parent history since the base holds exactly the six #219 commits, `07f7b04` to `fd2d8d2`, with no rebase.
- The three files both PRs touch (`receipts/files218`, `receipts/files219`) read correctly together:
  - `tb/pp_top/sim_main.cpp`. #218 adds 10 lines in section S1 (`Suite`, around line 10970): two `wait_any(q_msrp, 400)` waits and two byte-exact CHECKs, the Domain New again and then JoinMt. #219 adds the following:
    - the oracle `H::adp_last_aidx` and `H::served_entity` (around line 847);
    - the ADP capture hook (around line 1741), keyed on ethertype 0x22F0 with ADP subtype 0xFA;
    - one harness-reset line (around line 2166);
    - `served_entity` at eleven READ_DESCRIPTOR(ENTITY) expectations;
    - section AI's include and dispatch, and `--avail-index-only`.

    The regions are disjoint. #218 adds no harness reset, no capture path and no section dispatch, and it does not read `q_adp` or READ_DESCRIPTOR(ENTITY). #219 does not touch S1, `q_msrp` or any MSRP expectation. In #219's capture hook the MSRP branch is a different ethertype, so #218's extra MSRP frames cannot reach the ADP oracle. Section AI runs on a fresh processor of its own, so S1's extra 800 ms of waiting does not reach its counts. The other ENTITY reads take octet 36 from the captured wire, so they follow any clock shift S1 adds.
  - Arms. `scripts/apply_check.sh` runs `git apply --check` on every tracked `*.patch` against the head tree: **545 of 545 apply** (`receipts/patch_apply_check.txt`). Only two arms patch the bench harness, `tb/pp_top/ctr_mutations/store-link-detector-resets-up.patch` (re-anchored by #219) and `store-counts-domain-strobes.patch`. No #219 arm targets a file #218 changed. Running those two at the head (`ctr_mutants.py --only ... --jobs 3`, `receipts/ctr_harness_arms_head.txt`) gives a control PASS, KILLED with 7 failures (1 named), and KILLED with 11 failures (1 named). That matches the author's `794f8442` campaign log exactly. So #219's reset line is not shadowed by #218, and #218's S1 checks are not shadowed by #219's interface phases (`interface_phases.hpp` is a separate two-interface build that S1 does not run in).
  - `tb/pp_top/README.md`. #218 extends the S1 bullet (line 746). #219 adds the `avail-index` sentence (line 1394), two arm rows (around line 1492), the new section AI (around line 2746) and the IF4 bullet (around line 3484). The regions are disjoint. No suite-total figure is in either side, so the merge leaves no stale count.
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md`. #218 adds GAP-18 and GAP-19 and links them from REQ-SRP-001, REQ-SRP-006 and the gap table. #219 rewrites the REQ-ADP-011 row. The rows are disjoint. At the head `check-matrix.py` reports 115 REQ rows and 19 GAP findings, OK. `check-links.py` checks 1335 links, OK. `gen_matrix.py --check` reports 94 rows with 0 untested. `check-req-tags.py` (static), `check-ids.py`, `check-figures.py`, `check_aecp_commands.py`, `check-integrator-params.py`, `check_upc_map.py`, `check_m9_opcodes.py` and `git diff --check 45f03e04 HEAD` all end rc 0 (`receipts/doc_gates_head.txt`, run in a clean checkout of the head with 0 dirty entries after).

## 3. Claim (3): the three suites at the head, run by this reviewer

The pinned Verilator is `Verilator 5.050 2026-07-01 rev v5.050`. Its wrapper's sha256 is `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`. `scripts/vl.sh` passes every flag through and replaces only the Makefiles' `-j 0` with `-j 8`. Each tree is a `git archive` of the head (`scripts/run_suite.sh`), and the three suites ran concurrently.

| Suite | Result at `14492f87` | rc | At `794f8442` (author receipts) and at `45f03e04` (#218 body) | Reconciliation |
|---|---|---|---|---|
| `tb/pp_top` (`make`, 7 builds) | `11084 checks: 11084 PASS, 0 FAIL`; AI 16 checks with 0 failures, IF 8 checks with 0 failures | 0 | 11,082 at `794f8442`; 11,066 at `45f03e04` | The default build has 10,527 checks here and 10,525 at `794f8442`. The +2 are exactly #218's two new S1 CHECKs. The other six builds are unchanged (20 + 178 + 292 + 56 + 3 + 8). |
| `tb/adp_engine` (`make`, 2 builds) | `1365 checks: 1365 PASS, 0 FAIL` | 0 | 1,365 at `794f8442` | #218 touches nothing this suite builds. |
| `tb/srp_top` (`make`: the storage shapes, then the suite) | `8706 checks: 8706 PASS, 0 FAIL` | 0 | 8,706 at `45f03e04` | #219 touches nothing this suite builds. |

Logs and rc files: `receipts/{pp_top,adp_engine,srp_top}.{log,rc}`. Host path prefixes are redacted as `<VERILATOR_5.050_PREFIX>` and `<HOME>`, and nothing else changed.

## 4. Lenses at this head

- **Conformance: CLEAN.** The issue's four acceptance bullets are judged at the head as follows:
  - Bullet 1 (READ_DESCRIPTOR(ENTITY) returns the last ENTITY_AVAILABLE's index): graded by AI and IF4, both 0 failures here.
  - Bullet 2 (a planted constant fails the test): the arms' patches still apply, and the files they mutate are byte-identical to `794f8442` apart from the bench line. The kills stand from R809-1 and R810-1.
  - Bullet 3 (no other AEM field or ADP timing changes): the delta changes no HDL or AEM byte from #219. `git diff --stat 794f8442 14492f87` over `hdl/aecp`, `hdl/adp`, `hdl/top`, `docs/architecture/06_aecp_engine.md`, `tb/adp_engine` and `tb/aecp_cmds` is empty (`receipts/prior_findings_at_head.txt`).
  - Bullet 4 (the parent's gates pass with this head pinned): the parent idiom gate, the step that failed the consumer leg at `794f8442`, now exits 0. The rest of the consumer gates and the twin stand from R809-2 at `794f8442`. The current-dev merge candidate is the manager's.

  The IEEE 1722.1-2021 Table 7-2 and 6.2.2.15 reading is unchanged.
- **RTL: CLEAN.** The delta has no RTL of its own. The merge brings #218's `hdl/srp` changes, which were reviewed on #218, beside #219's `hdl/adp`, `hdl/aecp` and `hdl/top` changes, with no file in common. The integrated top builds and passes all seven pp_top builds.
- **Robustness: CLEAN.** The one changed bench line has the same value at every point, and reset still clears the oracle. In the integrated tree the ADP oracle and the extra MSRP frames from #218 use different capture branches. The suite exercises the combined SRP and ADP behaviour with 0 failures.
- **Tests: CLEAN.**
  - The three suites pass at the head, and their totals reconcile per build with the two parents.
  - The parent idiom gate passes, and the control probe shows it can fail on the line in question.
  - All 545 tracked patches apply. The two harness arms are KILLED with the same counts as at `794f8442`.
  - The `794f8442` evidence packet verifies: 541 of 541 manifest entries are present with matching sha256, 0 unlisted and 5 path-redacted (`scripts/verify_manifest.py`, `receipts/evidence_manifest_verify.txt`).
- **Docs: CLEAN.** The delta adds no source comment. `fd2d8d2` changes only an initializer, and the merge brings only #218's reviewed text. So the comment rule has no new instance to judge: no bench lane label, lane name, review round, reviewer ID or issue-comment ID appears in the delta. The three shared files read correctly together (section 2), and the documentation gates pass at the head.

## 5. Findings

No finding of severity MINOR, MAJOR or BLOCKER is open. One own SUGGESTION:

### R809-3-S-1 SUGGESTION (Docs): the PR body does not record the round-3 commits

- **Artifact:** the PR #219 body, "Measured at the head `794f844`" and the paragraphs before it.
- **Evidence:** the body is accurate as labelled. It names `794f844` as the measured head. It does not mention `fd2d8d2`, which exists for the parent idiom gate, or the merge `14492f8` of `main` `45f03e04`. The manager's notes record both (issuecomment-6758084284, -6759589148).
- **Impact:** none on any claim. A cold reader of the body alone would not learn why the head moved, or that its suite totals (pp_top 11,084, srp_top 8,706) differ from the body's figures by #218's checks.
- **Suggestion:** one sentence under the measured table: "`fd2d8d2` value-initializes `adp_last_aidx` with `= {}` for the parent's idiom gate. `14492f8` merges `main` `45f03e04` (#218) cleanly. The figures above are at `794f844`." Not required.

## 6. Prior public review findings, resolved or retained at this head

I read these after writing my own verdict and ledger.

| ID | Severity | State at `14492f87` | Basis at this head |
|---|---|---|---|
| R809-1 F-1 (evidence packet incomplete) | MAJOR | RESOLVED: refuted (manager ruling; R810-1; R809-2) | Re-verified here: `ea450d8d` `review-evidence/pp217-r1` holds 542 files, and all 541 manifest entries match `published_sha256` (`receipts/evidence_manifest_verify.txt`). |
| R809-1 F-2 (PR body suite count) | MINOR | RESOLVED | The live body reads "(36 suites)". At the head `tb/*/Makefile` still counts 36 (`receipts/prior_findings_at_head.txt`). |
| R809-1 R-1 / R810-1 R-1 (the START/STOP 0xD0 comparison) | RESIDUE | RETAINED | `hdl/aecp/ucode/gen_ucode.py:387-388` and `docs/architecture/06_aecp_engine.md:322-323` are byte-identical to `794f8442`, so the text still reads as cited. The exact fix in R809-1 R-1 stands. |
| R809-1 R-2 / R810-1 R-2 (RES-1) (area paragraph explains the FFs only) | RESIDUE | RETAINED | The PR body's area paragraph is unchanged ("The 33 flip-flops ..."). The exact fix in R809-1 R-2 stands. |
| R809-1 S-1 / R810-1 S-2 (pin the per-interface clear on DEPARTING) | SUGGESTION | RETAINED | `hdl/adp` and `tb/adp_engine` are unchanged since `794f8442`. |
| R810-1 S-1 (pin the index's upper octets, index of 256 or more) | SUGGESTION | RETAINED | `hdl/aecp`, `tb/aecp_cmds` and section AI's file are unchanged since `794f8442`. |
| R809-2 S-2 (label the twin log digest as pre-normalisation) | SUGGESTION | RETAINED | The evidence packet `ea450d8d` is unchanged. This round adds no twin evidence. |

The manager carries the two RESIDUE items to the residue checklist. Neither changes a measurement, figure, verdict, test, code or claim.

## 7. Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #217 acceptance 1-4 against the delta; `git diff --stat 794f8442 14492f87` over `hdl/aecp`, `hdl/adp`, `hdl/top` (empty); AI 16/0 and IF 8/0 at the head; parent idiom gate rc 0; #218's and #219's 00 rows together | R809-3 (delta), with R809-2 and R810-1 at `794f8442` for the unchanged code | 14492f87db567b4c4102d8c171b8b3b054f3098a |
| RTL | CLEAN | merge replay giving the head tree; side-by-side patches identical; disjoint HDL file sets (`files218`, `files219`); 7 pp_top builds, adp_engine 2 builds, srp_top storage shapes and suite | R809-3 (delta), with R809-2 and R810-1 for the unchanged RTL | 14492f87db567b4c4102d8c171b8b3b054f3098a |
| Robustness | CLEAN | `sim_main.cpp:855` semantics (C++17 static_assert probe); harness reset clear; ADP and MSRP capture branches; integrated pp_top run 11084/0 | R809-3 (delta), with R809-2 and R810-1 for the unchanged behaviour | 14492f87db567b4c4102d8c171b8b3b054f3098a |
| Tests | CLEAN | pp_top 11084/0, adp_engine 1365/0, srp_top 8706/0 (rc 0 each); per-build reconciliation; idiom gate rc 0, selftest 75/75 and control probe rc 1; 545/545 patches apply; 2 harness arms KILLED with the same counts; evidence manifest 541/541 | R809-3 | 14492f87db567b4c4102d8c171b8b3b054f3098a |
| Docs | CLEAN | `tb/pp_top/README.md` and `docs/00_MILAN_COMPLIANCE_REVIEW.md` read together; doc gates rc 0 at the head; comment-rule scan of the delta (no new comment); PR body (S-1 suggestion); R-1 and R-2 residue retained | R809-3 | 14492f87db567b4c4102d8c171b8b3b054f3098a |

## 8. Real limits

- This reviewer ran the three named suites, the parent idiom gate, the documentation and map gates, the patch-apply census and two counter arms at this head. It did not run the full `scripts/run_suites.sh` sweep, the other mutation campaigns, Yosys or the elaboration guards, the other parent consumer gates or the twin. Those stand from R809-2 and R810-1 at `794f8442`, and the delta does not touch the PR side of anything they measure. The integrated #218 code is covered by #218's own two reviews.
- Build parallelism was capped at `-j 8` in place of `-j 0`. No other build flag changed.
- No manager source bank ran at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts at `794f8442` plus this reviewer's own runs above.
- Hosted checks at `14492f87`, read only (`receipts/hosted_checks_14492f87.tsv`): `docs-gates` and `portability` completed successfully, twice each. `suites` was still `in_progress` in both runs when read. I make no claim on hosted acceptance, which belongs to the manager.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.
- The scratch parent's gitlink commit is local and was never pushed.

## 9. Pending manager duties

- Build and validate the current-dev merge candidate (source base `45f03e04`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`) at the merge turn with the builder and native banks, and link its receipts on the PR. This includes the donor bar at `14492f87`, which is not a review input.
- Hosted and act acceptance, including the `suites` checks still in progress at `14492f87`.
- Carry R809-1 R-1 and R-2 to the residue checklist. The parent's idiom-gate pattern, which reads commas inside a brace initializer, stays the manager's parent residue (#495). It is outside this PR.
- When milan-fpga takes this pin, it deletes the twin's owed row `entity-available-index`, as the PR body says.

## 10. Receipts

Every published file is listed in `MANIFEST.sha256` (sha256sum format, paths relative to the packet root). Scripts are under `scripts/` and raw receipts under `receipts/`. The disposable trees under `scratch/` are not published.

After the probes, the review clone was verified byte-exact (`receipts/clone_integrity.txt`):

- HEAD is `14492f87` and the tree is `ca0937b0`.
- `git status --porcelain --ignored` shows 0 entries; the worktree equals the index and the index equals HEAD.
- The index's modes and blob IDs equal the head tree's, and a rehash of all 868 tracked files gives the head tree's blob IDs.
- The head tree has no gitlinks. The scratch parent's `protocol-processor` gitlink is `14492f87` and `gptp-processor` is at its pin `1616fc8f`.

R809-3 FINISHED
