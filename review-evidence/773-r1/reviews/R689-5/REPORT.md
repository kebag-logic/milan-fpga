[R689] POSITIVE - exact head ba086243db19700f7773614a5a9e8917f6047d7e

Round R689-5 is a delta-only composition re-review of issue #773 / PR #779. It answers R689-4-F1. The candidate is `ba086243db19700f7773614a5a9e8917f6047d7e`, with tree `cecc5651fb6889a955de5eb996a5b650faf3b8fe`. Its parents are live dev `30d35da8f4ca76e90b070acc0fe93c64b784a7af` and PR head `e658682ed451ba46885225e5b3fc16841f61a5ca`. At 2026-10-25T05:31:15Z, live `dev`, `refs/pull/779/head` and `refs/pull/779/merge` (`0e5cb60a`) were all unchanged (`receipts/live_refs.txt`).

**Verdict in one paragraph.** The only change since R689-4 is the re-signed local-CI manifest, at evidence commit `297bd732`. The candidate tree is unchanged, so every R689-4 tree result still holds. The new manifest verifies with the same single key, and it differs from the R689-4 bytes only under `execution.coverage`. That map now holds exactly the 46 job ids of the four workflow definitions. Every entry is ok, and every act-mapped job's act result is success. Each matrix job lists all of its act legs. `physical-gptp` carries a not-run reason that matches its `if:` triggers. The candidate's 17-worker `verilator-shards` matrix is recorded as hosted run 40152466723's seventeen legs. Their job ids and conclusions match the API. That run checked out `refs/pull/779/merge` `0e5cb60a`, whose tree is the candidate's. Each leg's log shows that checkout, `--shard "i/17"`, and an owned-piece list byte-equal to the candidate's own `--shard i/17 --list`. The union is the 81-piece unsharded list with no duplicate, so every shard i/17 is accounted for exactly once. R689-4-F1 is resolved. One RESIDUE (wording inside the reason string) and one SUGGESTION remain. Neither blocks.

## 1. Delta since R689-4

| Item | Result | Receipt |
|---|---|---|
| Tree under review | HEAD `ba086243`, tree `cecc5651`, unchanged; live refs unchanged | `receipts/live_refs.txt`, `receipts/tree_final.log` |
| Evidence commit | `297bd732` (parent `298b15c2`) changes only `local-ci/e658682e/manifest.json`, `manifest.json.sig` and the index `review-evidence/773-r1/MANIFEST.json` | GitHub commit API (read-only) |
| Index | `MANIFEST.json` now records manifest `edd36bb0…` and sig `892c35d5…` as original and published sha256. The old `b5cfe5db…` no longer appears | §2 |
| Manifest content delta | 142 changed leaf paths, all under `/execution/coverage`. The old value was `null`. `subject`, `definitions`, `environment`, `execution.act` and `execution.banks` are byte-for-byte unchanged | `receipts/manifest_delta_vs_r689-4.txt` |
| allowed_signers | byte-identical to R689-4 (sha256 `4b2a05d3…`) | `receipts/signature_check.log` |

## 2. Signed packet checks (assignment items 1-4)

Packet `review-evidence/773-r1/local-ci/e658682e` at `297bd732`, downloaded raw to `receipts/signed_packet/`. Each file's git blob id equals the contents API sha.

| Check | Result |
|---|---|
| manifest.json sha256 | `edd36bb0a02ddc5570037a6be65e244b087f7f8173ca71669a810802a6f0e0d3`: matches the assignment |
| (1) allowed_signers key | one line, principal `milan-local-ci`, `namespaces="milan-local-ci"`, ED25519 `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`: matches |
| (2) `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` | `Good "milan-local-ci" signature … SHA256:dRI12tvJ…`, rc 0. Controls: a wrong namespace and a one-byte-altered manifest are each refused, rc 255 |
| (3a) subject | `candidate` `ba086243…` (tree `cecc5651…`, first parent `30d35da8…`), `head` `e658682e…` (tree `5023d9f2…`), `pr` 779. Each was checked against `git rev-parse` in this clone |
| (3b) definitions | all eight workflow hashes (candidate and head × `docs`, `elaborate`, `rtl-fast`, `rtl`) equal `sha256(git show <rev>:.github/workflows/<f>)` |
| (3c) coverage = the jobs of the four workflows | 46 keys = 9 `docs` + 6 `elaborate` + 15 `rtl-fast` + 16 `rtl` job ids, at the head and at the candidate. The two revisions define the same job ids; only the `verilator-shards` matrix differs (16 against 17). No key is missing or extra |
| (3d) every entry ok | all 46 entries are `ok: true`. Each of the 45 `by: act` entries names act jobs whose recorded result is `success`. The 63 successful act jobs and the one skipped act job are each mapped by exactly one entry |
| (3e) matrix legs | `rtl/yosys-shards` lists all 4 legs `Yosys shard i/4-(i+1)`. `rtl/verilator-shards` lists all 16 head legs `Verilator shard i/16-(i+1)`. Each act job name equals `<workflow name>/<job name>`, with the matrix expanded |
| (3) physical-gptp | `by: not-run`, with a named reason: "runs only on the schedule and workflow_dispatch events (nightly and manual), never on pull_request; act shows it skipped". This matches `rtl.yml:415-416` (`run_full == 'true' && (event == 'schedule' \|\| event == 'workflow_dispatch')`), the triggers at `rtl.yml:1671-1673` (`workflow_dispatch`, cron `17 1 * * *`), and `CI_WORKFLOWS.md:550-553`. Act shows the job `skipped`, and so does hosted job 121050090306. Wording residue in the reason's last sentence: RES1 |
| (4) candidate 17-worker matrix | `candidate_matrix.legs` holds 17 names, `Verilator shard 0/17` … `16/17`, each once, equal to the candidate `rtl.yml` matrix. For every leg, the job id, `success` conclusion and `run_attempt` 1 equal the API listing of run 40152466723. That run lists exactly 17 Verilator shard jobs. Its merge ref `0e5cb60a` has tree `cecc5651…` and parents (`30d35da8`, `e658682e`), re-fetched this round |

Checker: `check_coverage.py`, 148 checks, `RESULT PASS`, rc 0 (`receipts/coverage_check.log`). Eight planted manifest faults are each refused with rc 1 (`receipts/coverage_negative_controls.txt`): a dropped job, a duplicated leg, a wrong leg job id, a missing reason, a missing Yosys leg, `ok:false`, a failed act job, and a wrong candidate tree.

**Judgement on item (4).** It accounts for every Verilator shard i/17 of the candidate exactly once. `check_shard_legs.sh` read each of the 17 legs' hosted logs (`receipts/shard_legs/summary.tsv`, rc 0). Each log shows `fetch … origin +0e5cb60a…:refs/remotes/pull/779/merge`, `target_sha=0e5cb60a…` and `--ci-pieces --shard "i/17"`. Each log's `Shard i owns:` list is byte-equal to `scripts/run_all_suites.sh --ci-pieces --shard i/17 --list` on this candidate (`hosted_i.txt` against `local_i.txt`). The union of the hosted lists is 81 pieces, all unique, and equals the unsharded `0/1` list. The candidate's 17-worker topology ran only on the hosted runner. The local act replay ran the head's 16-worker `rtl.yml`. The manifest states this in its signed `note`, which matches what the evidence shows. The manager owns hosted acceptance.

## 3. Findings

### R689-4-F1 - MINOR - Tests - RESOLVED

The signed coverage map is now populated. It maps every job of the four workflow definitions, including the candidate's `Verilator shard i/17` legs and `Physical gPTP (nightly and manual)`, as the required outcome asked. Verification was run as specified in §2.

### RES1 - RESIDUE - Tests, Docs - `review-evidence/773-r1/local-ci/e658682e/manifest.json` `execution.coverage["rtl/physical-gptp"].reason`, last sentence

- **Evidence:** the reason ends "Hardware gPTP is bench evidence, not merge CI". The job does not run hardware. `rtl.yml:417` runs it on `ubuntu-latest`, and `CI_WORKFLOWS.md:550-558` says it owns the physical-rate `milan_dp_gptp` Verilator suite, with a 5400 s build-and-run deadline.
- **Why RESIDUE:** the operative part of the reason, the trigger rule, is correct and verified. The "not merge CI" conclusion matches policy ("outside the required PR aggregate"). The sentence changes no check outcome, figure, verdict or test, and it makes no hardware-proof claim.
- **Exact fix:** in the next re-signed packet, replace that sentence with "It is the physical-rate milan_dp_gptp simulation, reported nightly outside the required PR aggregate; it is not hardware evidence."

### SUG1 - SUGGESTION - Tests - same manifest, `execution.coverage["rtl/verilator-shards"]`

The entry is `by: act`. Its candidate-side evidence, though, is hosted: `candidate_matrix`. The merge-ref sha `0e5cb60a`, its parents and its tree `cecc5651` appear only inside the free-text `note`. Optional: give `candidate_matrix` its own `by: hosted` and structured `merge_ref`, `merge_ref_parents` and `merge_ref_tree` fields, so a checker can verify them without parsing prose.

### Retained from R689-4

- S1 (SUGGESTION, Robustness and Tests): refresh the `capture_coherence`, `media_phase` and `follow_ring` duration figures from a complete hosted run. Optional, unchanged, and goes to the residue checklist.
- R689-3-RES1: PR-body Status names `1b47a3dc`. Carried to the residue checklist.
- R689-3-SUG1, R689-1-S1, R689-2-S2, R689-1-S3 / R689-2-S3: optional, untouched, retained as SUGGESTION.

### Other prior public findings

All earlier MINOR and RESIDUE findings from R689-1..3 and R690-1..3 were resolved at `e658682e`, as R689-4 §6 recorded. The candidate carries those bytes unchanged, so they stay resolved. No review finding was posted on PR #779 or issue #773 after R689-4.

**Comment rule:** the delta changes no source file, so there is no new lane, round or reviewer label in source comments.

## 4. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The delta (an evidence packet only) does not touch conformance scope. R689-4 stands: patch-id equality, and the only shared file is a test-inventory doc. Issue #773 acceptance is from the source reviews | R689-3 and R690-3 (source, `e658682e`); R689-4 composition | ba086243db19700f7773614a5a9e8917f6047d7e |
| RTL | CLEAN | The delta does not touch RTL scope. R689-4 stands: no dev-side `hdl/` change, PR RTL bytes carried identically, hosted `yosys-portability` and Yosys shards green on tree `cecc5651` | R689-3 / R690-3 (source); R689-4 composition | ba086243db19700f7773614a5a9e8917f6047d7e |
| Robustness | CLEAN | The delta does not touch robustness scope. R689-4 stands: `media_phase` 1102.7 s against 1400 s on the exact tree, and worker limits met. S1 is optional | R689-4 | ba086243db19700f7773614a5a9e8917f6047d7e |
| Tests | CLEAN | R689-4 tree gates (unchanged tree). This round: signed manifest `edd36bb0` (signature plus controls), coverage map of 46 jobs against the four workflow definitions at both revisions (`check_coverage.py`, 148 checks, 8 negative controls), the 17 hosted legs' checkout, `--shard` and owned lists against the candidate's `--list`, union 81/81. F1 resolved; RES1 and SUG1 non-blocking | R689-5 | ba086243db19700f7773614a5a9e8917f6047d7e |
| Docs | CLEAN | The delta touches no doc in the tree. R689-4 stands: `TESTING.md` disjoint hunks, and `docs_check`, `gen_toc --check --verify-anchors`, `check_em_dash --base 30d35da8`, `check_doc_paths` and `check_doc_style` all rc 0. RES1 is evidence-packet wording | R689-4 (tree); R689-5 (packet wording) | ba086243db19700f7773614a5a9e8917f6047d7e |

## 5. Real limits

- No suite, bank, build or act run was executed this round. The only commands run in the clone were the read-only `run_all_suites.sh --ci-pieces --list` selections. Hosted evidence was inspected read-only.
- The bank entries (`manager-builder`, 48 commands; `full-native`, 5) still carry only argv hashes and exit codes. They were not needed for, or used in, any coverage judgement above.
- The candidate's 17-worker topology has hosted execution evidence only. Local act ran the head's 16-worker topology.
- Physical calibration was NOT RUN. The skipped physical gPTP job and field skips are not hardware proof.

## 6. Pending manager duties

- Carry RES1, S1 and R689-3-RES1 to the residue checklist. SUG1 is optional.
- At the merge turn: verify that live dev is still `30d35da8` (or rebuild the candidate), check merge-tree equality, and run post-merge containment as CONTRIBUTING requires.

## 7. Integrity after probes

`receipts/tree_final.log`, rc 0:
- HEAD is `ba086243`, and the index tree equals the HEAD tree `cecc5651`. There is no tracked diff.
- 1442 blobs match their bytes and modes.
- The gitlinks `gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack` and `third_party/verilog-axis` match. `external` is uninitialized, as checked out.
- There are 0 untracked or ignored entries.

R689-5 FINISHED
