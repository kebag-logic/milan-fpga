[R689] NEGATIVE - exact head ba086243db19700f7773614a5a9e8917f6047d7e

Round R689-4: composition review of issue #773 / PR #779 as the merge-train candidate. Candidate tree `cecc5651fb6889a955de5eb996a5b650faf3b8fe`. Parents: live dev `30d35da8f4ca76e90b070acc0fe93c64b784a7af` (which carries PR #782 / #781) and PR source head `e658682ed451ba46885225e5b3fc16841f61a5ca`, source base `a032c6d6e3775f145349d5a495c1e1ad12294936`.

**Verdict in one paragraph.** The composed tree adds no defect beyond the reviewed sources. The merge is textually trivial: the PR's patch-id equals the candidate's patch-id over dev. The one shared file has disjoint hunks. Every gate that reads the shared files and registries passes on the candidate. Every new case lands in exactly one of the seventeen workers. The hosted `pull_request` run 40152466723 executed exactly this tree, and all 17 Verilator shards, the six unions, `verilator-suites` and `yosys-portability` are green. The verdict is NEGATIVE on one MINOR, F1, which is in the signed local-CI packet and not in the tree. Check (3) of the assignment fails against the signed bytes: `execution.coverage` is `null`. So the packet maps no job, and it does not account for the candidate's own 17-worker `rtl.yml` jobs. Fixing F1 is a manager action and needs no source change. The other four lenses are CLEAN.

## 1. Composition: overlap and semantic interactions

| Item | Result | Evidence |
|---|---|---|
| Merge reproduction | `git merge-tree --write-tree 30d35da8 e658682e` = `cecc5651…` = HEAD^{tree} | `receipts/patch_id_pr_vs_candidate.txt` |
| PR content preserved | `git patch-id --stable` of `a032c6d6..e658682e` = that of `30d35da8..ba086243` = `c84a59bb95b47176d9a0921156bc539ed2c5a236`. The dev side (`a032c6d6..30d35da8` against `e658682e..ba086243`) is also identical once line numbers are ignored | same receipt |
| Files changed on both sides | Only `docs/testing/TESTING.md`. #782 changes the sharding paragraph (lines ~541-554, sixteen to seventeen). This PR changes the `capture_coherence` row (line 619). The hunks are disjoint and the candidate's diff from dev is exactly the PR's one-row hunk | `git diff a032c6d6 30d35da8 -- docs/testing/TESTING.md`; `git diff 30d35da8 HEAD -- docs/testing/TESTING.md` |
| Other dev-side files | `rtl.yml`, `CI_WORKFLOWS.md`, `RUNNING_TESTS.md`, `measure_test_evidence.py`, `run_all_suites.sh`, `suite_shards.py`. The PR touches none of them | `git diff --stat` |
| Shared registries | `PIECE_SECONDS`, `SUITE_SECONDS` (`media_phase` 1400) and `WORKER_OVERHEAD_SECONDS` ×17 come from dev only. The PR adds no suite and no piece, so the registered suite and piece inventory is unchanged. Case membership is driver-derived (`scripts/ci_suite_pieces.py:48-55`) | §2 |

## 2. Gates run on the candidate (all rc 0)

Each gate runs from this clone at the candidate head with the pinned Markdown renderer (`tools/markdown/requirements.txt`, hash-locked, installed in a disposable venv). Runner: `run_gates.sh`. Receipts: `receipts/gates/*.log|.rc`.

| Gate | Result |
|---|---|
| `docs_check.py` / `--selftest` | 0 findings across 210 md + 1418 scrubbed files; selftest pass |
| `gen_toc.py --check --verify-anchors` | pass; 537 cross-page fragment links reproduced |
| `check_em_dash.py --base 30d35da8` / `--selftest` | 0 findings over 202 added lines in 4 pages, arms 339/339 |
| `check_doc_paths.py`, `check_doc_style.py` | rc 0 |
| `ci_events.py --check` / `--selftest` | OK, 2199 contract items across 4 workflows + CI_WORKFLOWS.md; selftest rc 0 |
| `ci_gate_workflows.py --check` / `ci_gate_workflows_selftest.py` | the generated `rtl.yml` matches its template at 17 workers; selftest rc 0 |
| `suite_shards.py --selftest` | PASS; workers 0-15 predicted ≤ 1605 s (bound 1620), worker 16 2032 s (bound 2160); 17 `--shard` lists stable under two hash seeds; an 18-worker `rtl.yml` is refused |
| `measure_test_evidence.py --check` / `--selftest` | runner evidence contract OK (1400 s budget string); ratchet PASS |
| Piece ownership `shard_union.sh` (`run_all_suites.sh --ci-pieces --shard i/17 --list`, i = 0..16) | 81 pieces; union = unsharded `0/1` list; 0 duplicates (`receipts/shards/`) |
| Case ownership (`partition_check.txt`) | `capture_coherence` 43 cases across 4 legs and `milan_dp` 21 across 4: each case is owned exactly once. Against dev, `capture_coherence` gains exactly the PR's seven #773 mutants (36 to 43). No case is removed (`inventory_delta.txt`). The `milan_dp` inventory comes from `ci_make_cases.py` and the `milan_dp` Makefile, neither of which differs between dev and the candidate |

## 3. Exact-tree hosted evidence (read-only inspection; the manager owns acceptance)

- Run 40152466723 (`pull_request`, head `e658682e`) checked out `refs/pull/779/merge` = `0e5cb60a`. Its parents are `30d35da8` and `e658682e`, and its tree is **`cecc5651…`**, identical to this candidate (`receipts/hosted_merge_ref_tree.json`). Conclusion: success. All 17 `Verilator shard i/17` jobs, the six `Union` jobs, `verilator-suites`, `yosys-portability` and the four Yosys shards succeeded. The only skipped job is `Physical gPTP (nightly and manual)` (`receipts/hosted_run_40152466723.json`).
- **media_phase budget:** PASS in 1102.7 s on worker 4/17, against its 1400 s budget (`run_all_suites.sh:258`, `suite_shards.py:116`). That is 78.8 % of the budget and leaves 297 s. It is inside #781's stated projection ("at most about 1240 s"). This PR's `ofs_wrap.sv` change is comment-only (`git diff 30d35da8 HEAD -- tb/verilator/media_phase/ofs_wrap.sv`), so the PR adds no `media_phase` case. #782's own run 40139678015 measured 558.3 s (`receipts/hosted_suite_windows.txt`).
- Worker job wall times, and per-suite windows against dev's #782 run, are in S1 below.

## 4. Signed local-CI packet (assignment checks)

Packet: `review-evidence/773-r1/local-ci/e658682e` at `298b15c2`, copied to `receipts/signed_packet/`.

| Check | Result |
|---|---|
| manifest sha256 | `b5cfe5dbe69c99416d24dc09389b60380ba7fb9e00a86a9816d1aaa873f62b23`: matches |
| (1) allowed_signers key | one line, principal `milan-local-ci`, ED25519 `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`: matches (`fingerprint.txt`) |
| (2) `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` | `Good "milan-local-ci" signature`, rc 0 |
| (3a) subject | `candidate` = `ba086243…`, `candidate_parent` = `30d35da8…`, `candidate_tree` = `cecc5651…`, `head` = `e658682e…`, `pr` = 779: correct |
| (3b) workflow definitions | the candidate's and head's `docs`, `elaborate` and `rtl-fast` hashes equal the files in this clone. `rtl.yml` candidate `2fb98cbc…` and head `2434c502…` also match the clone, and they differ, as #782 requires |
| (3c) coverage entries | **FAIL: `execution.coverage` is `null`** (F1) |

## 5. Findings

### F1 - MINOR - Tests - `review-evidence/773-r1/local-ci/e658682e/manifest.json` (`execution.coverage`) - the signed packet maps no workflow job, and the candidate's 17-worker `rtl.yml` jobs are in no act or bank entry

- **Authority/evidence:** the assignment's check (3) requires that every coverage entry be ok. The packet's stated contract is that every workflow job is mapped as act, bank or a named not-run reason. The signed bytes contain `"coverage":null`. `execution.act.jobs` lists the **head's** jobs, `Verilator shard 0/16-1` … `15/16-16`, because act replayed `e658682e`, whose `rtl.yml` (`2434c502…`) has 16 workers. The candidate's `rtl.yml` (`2fb98cbc…`, recorded in the same manifest) runs `Verilator shard 0/17` … `16/17`, and no act job or coverage entry names those. Both banks (`manager-builder`, 48 commands; `full-native`, 5 commands) carry only argv hashes and exit codes, so a reader cannot tell from the packet that they ran the 17-shard selection. The one skipped act job also has no recorded not-run reason; only its name implies one.
- **Impact:** the signed local evidence does not show what the assignment says it shows. A cold reviewer cannot use the packet to check that every job of the candidate's workflows is accounted for, and the 17-worker topology is exactly what this composition changes. The tree itself is not affected: the hosted exact-tree run (§3) and the gates in §2 independently show it green.
- **Why MINOR and not RESIDUE:** the defect is in an evidence artifact's content (a missing coverage map), not in wording.
- **Required outcome:** publish a re-signed manifest whose `coverage` maps every job of the candidate's four workflow definitions to act, a named bank command or a named not-run reason. That includes `Verilator shard i/17` for i = 0..16 and `Physical gPTP (nightly and manual)`. Alternatively, publish a signed statement that this schema leaves `coverage` empty by design, together with that mapping. No source change is required.
- **Verification:** run `ssh-keygen -Y verify` with the same allowed_signers key, then confirm every coverage entry is ok and the candidate's 17 shard job names are each covered once.

### S1 - SUGGESTION - Robustness, Tests - `scripts/suite_shards.py:164` (`PIECE_SECONDS["capture_coherence"]`), `docs/testing/CI_WORKFLOWS.md:394-397` - refresh the duration figures from run 40152466723

On the exact tree, the hosted worker job times are well above the selector's predictions (`receipts/hosted_shard_compare.tsv`, `hosted_suite_windows.txt`):

- Worker 1/17 took 2428 s against a predicted 1541 s. That is 89.9 % of its 45-minute (2700 s) limit (`rtl.yml:144`).
- Workers 6, 13 and 3 took 2047 s, 2040 s and 2353 s.
- The `capture_coherence` legs ran 1485.6, 610.9, 687.5 and 597.3 s, against 680.8, 262.9, 385.0 and 250.7 s on #782's run and registered figures of 632, 508, 331 and 246 s. That is consistent with the seven added mutants, each building the datapath.
- The largest leg uses 62 % of its inherited 2400 s budget.
- Part of the growth is runner variance: `gptp_plane`, which builds none of the changed files, ran 1.40× slower.

No hard limit is crossed and every job passed. Dev's own worst worker in run 40139678015 was already 2389 s (worker 3), so the composition moves the worst margin by only 39 s. The policy already says the split figures are predictions and must be refreshed from the next complete hosted run (`CI_WORKFLOWS.md:396`). Optional outcome: re-measure the four `capture_coherence` legs, and `media_phase` and `follow_ring`, from a complete hosted run at the merged head, then rebalance. Verification: `suite_shards.py --selftest` with the refreshed figures.

No RESIDUE in the reviewed delta. A scan of the added `hdl/`, `tb/` and `scripts/` lines on the candidate found no bench-lane label, round, reviewer ID or comment ID. The only hit is "the control lane's IFG", which names a datapath lane.

## 6. Prior public findings on this PR (read after the independent pass)

| Prior finding | Disposition at ba086243 |
|---|---|
| R689-1-F1, R690-1-F1, R690-1-F2, R689-2-F1 / R690-2-F1 (MINOR) | Resolved at their causes by e658682e (R689-3, R690-3). The composition carries those bytes unchanged (equal patch-id), so they stay resolved |
| R689-1-R1, R689-2-RES1 / R690-2-R1 (RESIDUE) | Resolved at e658682e. Unchanged |
| R689-3-RES1 (RESIDUE, PR body Status names 1b47a3dc) and R689-3-SUG1 | PR-body and issue-thread items outside the tree. The composition does not touch them, so they are carried as before to the manager's residue checklist |
| R689-1-S1 (RTL, Robustness), R689-2-S2 (Tests), R689-1-S3 / R689-2-S3 (Tests) | Optional and not taken. The composition does not touch their artifacts. Retained as SUGGESTION |

## 7. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition does not touch conformance scope: patch-id equality, and the only shared file is a test-inventory doc. Issue #773's acceptance was covered by the source reviews and is carried unchanged | R689-3 and R690-3 (source, e658682e); R689-4 identity check | ba086243db19700f7773614a5a9e8917f6047d7e |
| RTL | CLEAN | No `hdl/` file changes on the dev side (`git diff --stat a032c6d6 30d35da8`). The PR's RTL bytes are carried identically. Hosted exact-tree `yosys-portability` and Yosys shards green | R689-3 / R690-3 (source); R689-4 identity check | ba086243db19700f7773614a5a9e8917f6047d7e |
| Robustness | CLEAN | Composition scope: `media_phase` 1102.7 s against 1400 s on the exact tree; per-piece budgets (max 62 %); 45-minute worker limits all met; S1 is optional | R689-4 | ba086243db19700f7773614a5a9e8917f6047d7e |
| Tests | UNCLEAN (F1) | `suite_shards --selftest`, `ci_gate_workflows --check`, `ci_events --check`/`--selftest`, piece union 81/81 over 17 shards, case partitions 43 and 21, inventory delta +7, hosted run 40152466723 at tree `cecc5651` green; signed packet checks (1)-(3) | R689-4 | ba086243db19700f7773614a5a9e8917f6047d7e |
| Docs | CLEAN | `TESTING.md` disjoint hunks (lines ~541-554 and 619); `docs_check`, `gen_toc --check --verify-anchors`, `check_em_dash --base 30d35da8`, `check_doc_paths`, `check_doc_style` rc 0; no stale `capture_coherence` defect count elsewhere in `docs/` | R689-4 | ba086243db19700f7773614a5a9e8917f6047d7e |

## 8. Real limits

- No suite, bank, build or act run was executed. Tree evidence is hosted (read-only), plus the static and generator gates above. The banks' argv hashes cannot be mapped to commands from the packet.
- The `milan_dp` case inventory at dev was not listed, because the lister needs files missing from a partial archive. It is argued unchanged instead: neither `ci_make_cases.py` nor `tb/verilator/milan_dp/Makefile` differs between dev and the candidate.
- Physical calibration NOT RUN. The skipped physical gPTP job and field skips are not hardware proof.
- Hosted timing is a single sample per run, with visible runner variance.

## 9. Pending manager duties

- Resolve F1: re-sign the manifest with a populated coverage map, or publish the mapping under signature. Then re-review only the packet.
- Optionally take S1: refresh the duration figures from a complete hosted run at the merged head.
- Carry R689-3-RES1 to the residue checklist.
- At the merge turn, post-merge containment and the merge-tree equality check, as CONTRIBUTING requires.

## 10. Integrity after probes

`receipts/tree_final.log`, rc 0:
- The index tree equals the HEAD tree, and there is no tracked worktree diff.
- 1442 blobs match their raw bytes and modes.
- The five initialized gitlinks (`gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack`, `third_party/verilog-axis`) match. `external` is uninitialized, as checked out.
- Interpreter caches the probes generated were removed, and the clone has 0 untracked or ignored entries.

R689-4 FINISHED
