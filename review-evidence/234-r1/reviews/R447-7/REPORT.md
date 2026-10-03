[R447] POSITIVE - exact head d5f56313dc5a5c2716211356f99796664dc843dd

# R447-7 external review: issue #234 / PR #638, round 7 (PR body only)

- Head `d5f56313dc5a5c2716211356f99796664dc843dd`, tree `c6dcc1b61f274a3acf0479bfe47f72c25f86708d`. Source base is dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- The head did not move after R447-6.
  - `receipts/r7/ls_remote.log`: `234-area-baseline` is still `d5f56313`.
  - The PR's last commit is `d5f56313`, and my clone's HEAD, tree and index equal it (`receipts/verify_tree.log`).
- Round 7 is a PR-body edit only. Against my R447-6 snapshot, the body changed in exactly the three places R447-6 F1 and R1 asked for, and in no other byte (`receipts/r7/pr_body_diff_same_capture.log`, `receipts/r7/body_chardiff.log`).
- **The verdict is POSITIVE.**
  - R447-6 F1 (MINOR Docs) is **RESOLVED**. I followed the body's state command verbatim in a fresh clone. It gives HEAD `d5f56313` and tree `c6dcc1b6`. There, the body's eight validate commands all exit 0 and print 260 arms and 174 mutants. The Description row now states the same counts.
  - R447-6 R1 (RESIDUE Docs) is **RESOLVED**. The round-6 assignment is linked, with the text I gave as its exact fix.
- No finding is open. Three earlier SUGGESTIONs are retained (S1 to S3), because the code is unchanged.
- All five lenses are covered clean at this head.
- My verdict, findings and ledger came from my own pass. The table of prior findings was written afterwards.

## Inputs, in order

1. AGENTS.md and CONTRIBUTING.md (as loaded), and the docs map. These are unchanged at this head.
2. Issue #234's assignments and rulings, as in R447-6:
   - the rulings (5967852698) and the owner decision (5967924270);
   - the round-6 assignment (5971250916);
   - round-6 REVIEW READY (5971779548).

   Nothing was posted on #234 after it (`receipts/r7/comment_headers.log`).
3. The review start on the PR (5972121970, `receipts/r7/review_start_comment.md`).
4. The PR body:
   - from the REST API (`receipts/r7/pr_body_snapshot.md`);
   - and, to compare like with like against R447-6, by the same capture method as that snapshot (`receipts/r7/pr_body_snapshot_ghview.md`).

   Read at `receipts/r7/pr_body_snapshot.read_at`.
5. My own R447-6 packet: its report, the body snapshot `receipts/r6/pr_body_snapshot.md`, and its gate and fuzz receipts. It is used read-only, for comparison.
6. Exact-head hosted check runs, as a snapshot only (`receipts/r7/hosted_check_runs.tsv`).
7. After my verdict, findings and ledger were written: the prior public findings, to resolve them.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE item is open. The SUGGESTIONs below are retained from R447-6 unchanged, because the code they concern is byte-identical (same head, same tree).

```text
[R447] S1 SUGGESTION Tests (retained, R447-6 S1) - syn/ooc/pp_resource_gate.py:98-100 against syn/ooc/pp_resource_gate_selftest.py:169-170 and :354-355 - the accepted side is not pinned for SCOPE_NAME's character groups, or for either class's first character and lower bound
Evidence: R447-6 receipts/r6/probe_r6_delta.log (the same tree). Each surviving narrowing refuses with exit 2, naming the key, so it fails closed.
```

```text
[R447] S2 SUGGESTION Robustness (retained, R447-6 S2 / R447-5 S3) - the name walk's memory growth
Evidence: R447-5/R447-6 receipts/r5/probe_r5_size.log. The PR body lists it as open (receipts/r7/pr_body_snapshot.md:424).
```

```text
[R447] S3 SUGGESTION Tests (retained, R447-6 S3 / R447-4 S1 and S2) - the generative oracle's exit-1 source, and the generator operators
Evidence: R447-6 receipts/r4/probe_r4_oracle.log and probe_r4_fuzzkill.log. The PR body lists them as open (:423).
```

## Round-7 review (my own pass)

### 1. Which bytes of the body changed

- I compared like with like. `receipts/r7/pr_body_diff_same_capture.log` compares R447-6's snapshot with today's body captured the same way. It has exactly three changed lines, `40c40`, `380c380` and `391c391`, and nothing else.
- A character-level diff of the same pair (`receipts/r7/body_chardiff.log`) shows only these changes:
  - `:40`: `254` becomes `260` and `162` becomes `174`, nothing else on the line;
  - `:380`: ` and [round-6 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5971250916)` is inserted after the round-5 link. That is byte for byte the "Exact fix" text of R447-6 R1;
  - `:391`: `ec7eb2d8ff81700842f4e3a35b79879c8c3838e5` becomes `d5f56313dc5a5c2716211356f99796664dc843dd`.
- The REST API copy (`pr_body_snapshot.md`) differs from that capture only by the final newline, which the capture tool appends (`receipts/r7/pr_body_diff.log` `444d443`; `receipts/r7/capture_check.log`). That newline is not a body change.

### 2. Following the body's own commands (F1's required verification)

`follow_body.sh` runs the body's "How to get into the same state" verbatim. It works in a fresh clone that takes its objects from my review clone and has its origin set to the public repository. Receipts are in `receipts/r7/follow/`.

- **`state.log`**:
  - `git fetch origin 234-area-baseline` rc 0, and FETCH_HEAD is `d5f56313`;
  - `git switch --detach d5f56313…` rc 0, giving HEAD `d5f56313` and tree `c6dcc1b6`;
  - `git submodule update --init …` rc 0. That checks out `gptp-processor` `5dce647a`, `protocol-processor` `631eeb34` and `third_party/verilog-axis` `48ff7a7e`, which equal the gitlinks.
- **The validate commands** (`SUMMARY.log`): all eight exit 0. Their output against "Expected result" (`:410`):

  | Body command | rc | Printed | Against R447-6 receipt |
  |---|---:|---|---|
  | `pp_resource_gate.py --selftest` | 0 | "260 arms and 500 generated cases PASS", digest `151eb3fc6a0d989c` | byte-identical to `gates/gate_selftest.log` |
  | `pp_resource_gate_mutants.py` | 0 | "control passes, all 174 mutants fail" | byte-identical to `gates/gate_mutants.log` |
  | `pp_resource_gate.py check-baseline` | 0 | "baseline PASS: 3 endpoints" | byte-identical to `gates/gate_check_baseline.log` |
  | `pp_resource_gate.py --fuzz 20000` | 0 | 20,000 cases, 0 failures, digest `0596f2c893188fb0` | byte-identical to `fuzz/fixtures-20000-s234.log` and `percommit/d5f56313.fuzz20k.log` |
  | `pp_baseline.py --selftest` | 0 | PASS | equal except the random `/tmp` export path line |
  | `pp_baseline_mutants.py` | 0 | every mutant PASS | byte-identical to `gates/pp_baseline_mutants.log` |
  | `ci_scope.py --selftest` | 0 | "selftest: PASS" | equal to the first 91 lines of `gates/ci_scope.log`, which also ran a second command |
  | `ci_events.py --check` | 0 | "ci_events: OK (1655 contract item(s) …)" | equal to the first 2 lines of `gates/ci_events.log`, which also ran `--selftest` |

- **The counts at the head.** R447-6's per-commit receipts show that `ec7eb2d8`, the old checkout target, prints 254 and 162. The new target prints 260 and 174. So the body's reproduction entry point now validates the head under review and gives the stated result.
- **The tree after the run** (`verify_follow_after_validate.log`): HEAD, tree, index and tracked bytes and modes are unchanged. The only extra files are ignored `__pycache__` directories that the Python runs wrote in this disposable clone.

### 3. Internal consistency of the edited body

- **The figures now agree.** A grep (`receipts/r7/body_counts.log`) shows that 260 and 174 are stated at `:21` (Status), `:40` (Description), `:339-347` (Round 6) and `:410` (How to validate).
- **The 254 and 162 that remain are correct as written.** They appear at `:293`, `:323`, `:339`, `:342` and `:346-347`, and each is a round-5 figure labelled as such ("round 5: …", or inside the Round 5 section).
- **No stale checkout target is left.** `ec7eb2d8` survives only as round 5's head in historical text: `:21` ("three commits on round 5's `ec7eb2d8`"), and the Round 6 section.
- **The reference.** The round-6 assignment link resolves to issue comment 5971250916. That is the round-6 assignment I read in R447-6.

### 4. The code, tests and repository docs are unchanged

- The review clone is byte-exact at `d5f56313` / `c6dcc1b6` (`receipts/verify_tree.log`, PASS).
  - Worktree and index equal HEAD.
  - Nothing is untracked or ignored, and no probe ran in this clone.
  - The gitlinks are `efeb541a`, `5dce647a` and `631eeb34`, with `48ff7a7e` checked out.
- The diff `1269cdaf..d5f56313` is the same 15 files and +4148/-13 as at R447-6 (`receipts/r7/diff_stat_base_head.log`).
- The body edit makes no new claim about code, tests, figures or repository docs. It only replaces stale round-5 figures with the head's, which R447-6 had already verified. So nothing in it contradicts the head reviewed POSITIVE by R446-6 and covered clean for four lenses by R447-6.

### 5. Hosted snapshot at this head

`receipts/r7/hosted_check_runs.tsv`, read at `hosted_check_runs.read_at`:
- completed successfully: `rtl-fast`, `yosys-elaboration`, `verilator-lint`, `elaborate`, `bdd-conformance`, `changes`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `wire-accountability`, Yosys shards 0-3, and Verilator shards 0 and 3;
- still in progress: Verilator shards 1, 2 and 4;
- `Physical gPTP` was skipped, which is not evidence.

The manager owns hosted and local-replica acceptance.

## Prior findings at this head

This section was written after the verdict, findings and ledger above.

I read for their findings:
- my own R447-6 (5972117388);
- R446-6 (5972052581), which is POSITIVE at this head;
- R446-5's open items, as R447-6 carried them.

I ran none of R446-6's probes. Every state below rests on my own receipts.

| Prior finding | State at `d5f56313` | Evidence (this round) |
|---|---|---|
| R447-6 F1 (MINOR Docs): the body's state command checks out `ec7eb2d8`, and the Description row states 254 / 162 | **RESOLVED** | `body_chardiff.log` (`:391` now `d5f56313…`; `:40` now 260 / 174). `follow/state.log` gives HEAD `d5f56313`. `follow/v1_gate_selftest.log` prints "260 arms" and `v2_gate_mutants.log` prints "all 174 mutants fail". Both are byte-identical to R447-6's head receipts. |
| R447-6 R1 (RESIDUE Docs): the round-6 assignment is not linked | **RESOLVED** | `body_chardiff.log` `:380`: the inserted text equals R1's exact fix byte for byte. |
| R447-6 S1, S2, S3 (SUGGESTION) | **Retained**, optional | They are S1 to S3 above. The code is unchanged (same tree). |
| R446-6 R1 (RESIDUE Docs): the reproduction checkout names round 5's head, and the round-6 assignment is not linked | **RESOLVED** | The same two edits, at `:391` and `:380`. Both of its exact-fix steps are applied as written (`body_chardiff.log`). |
| R446-6 S1 (SUGGESTION Tests): list-walk, scope-path and scope-class mutants beyond the shipped ones survive the self-test | **Retained**, optional (R446-6's grading) | The code is unchanged, so its status cannot have moved. Its `SCOPE_NAME` accepted-side part overlaps my S1. I did not rerun its probes. |
| R446-5 R1 (RESIDUE Docs): the Round 5 row says "run by `strict()` on every JSON the gate reads" | **Retained** as RESIDUE | `receipts/r7/r446_5_r1_text.log`: `:285` is unchanged. It was not in the body-edit request. It is wording only, and the manager carries it on the residue checklist with R446-5's exact fix: "run by `strict()` on every JSON that `check`, `record` and `check-baseline` read". |
| R446-5 S1 and the R447-5 / R447-4 suggestions | **Retained**, optional | As in R447-6. They are listed open in the body (`:423-425`), and those lines are unchanged. |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The body's state and validate commands, followed verbatim (`receipts/r7/follow/state.log`, `SUMMARY.log`): 8 of 8 rc 0, with `check-baseline` at 3 endpoints. The acceptance criteria as ruled (5967852698, 5967924270) are unchanged, and no issue comment followed round-6 REVIEW READY. The tree is identical to the head R447-6 covered clean (`receipts/verify_tree.log`). The body edit states no new conformance or clause claim (`receipts/r7/pr_body_diff_same_capture.log`). | R447-7 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| RTL | CLEAN | `receipts/r7/diff_stat_base_head.log` (the diff is unchanged, with no HDL, XDC, Tcl or workflow change since R447-6), `receipts/verify_tree.log` (the gitlinks equal the base), and `receipts/r7/follow/state.log` (the body's submodule command checks out exactly the gitlinks). The body edit touches no RTL claim. | R447-7 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Robustness | CLEAN (S2 optional) | `receipts/r7/follow/v4_fuzz20000.log`: 20,000 generated cases, 0 failures, byte-identical to R447-6. `v3_check_baseline.log`. The gate module is unchanged (same tree). The body's limitation entries `:413-428` are unchanged and still match R447-6's probes. | R447-7 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Tests | CLEAN (S1, S3 optional) | `receipts/r7/follow/v1_gate_selftest.log` (260 arms, 500 cases, digest `151eb3fc6a0d989c`), `v2_gate_mutants.log` (174 of 174, control passes), `v5`/`v6` (`pp_baseline`), `v7` (`ci_scope`), `v8` (`ci_events`). Each equals the R447-6 receipt, as tabled above. | R447-7 | `d5f56313dc5a5c2716211356f99796664dc843dd` |
| Docs | CLEAN | PR body (`receipts/r7/pr_body_snapshot.md`): Description `:40`, references `:380`, state `:389-393`, validate `:399-410`, Status `:21`, Round 6 `:319-376`, limitations `:412-428`. Diff against R447-6's snapshot: 3 lines, as asked. Count consistency: `receipts/r7/body_counts.log`. The repository docs are unchanged (same tree), and R447-6 found them true with no stated counts. | R447-7 | `d5f56313dc5a5c2716211356f99796664dc843dd` |

## Real limits

- **No Vivado run** and no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **No RTL is in the diff**, so the scoped Verilator was not used.
- **Not rerun this round:**
  - my round-1 to round-6 probes, the real-data runs and the 30-gate bank. The tree is byte-identical to the one R447-6 ran them on (`receipts/verify_tree.log`), and the assignment confines this round to the body;
  - the GNU Make 4.3 docs build, as in R447-6.
- **This round reran** exactly the body's state and validate commands.
- **The follow clone** borrows objects from my review clone (`--shared`). It fetched `234-area-baseline` and the three submodules from their public URLs. FETCH_HEAD equals the published head.
- **Hosted acceptance:** three Verilator shards were still in progress when snapshotted. The manager owns hosted and local-replica acceptance.
- **Path substitution:** receipts replace host paths with `$CHECKOUT` (the review clone) and `$FOLLOW` (the disposable follow clone). No other byte was changed.

## Pending manager duties

- R447-6 F1 and R1, and R446-6 R1, are resolved. This round adds no new item to the residue checklist. R446-5 R1 stays on it with its exact fix (body `:285`).
- Hosted and local-replica acceptance at the exact head, including Verilator shards 1, 2 and 4.
- The merge-turn candidate on live dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`, distinct from this source review (source base `1269cdaf`).
- The merge-bank Vivado `check` (manager ruling).
- Publishing this packet: `REPORT.md` and the files listed in `MANIFEST.sha256`.

R447-7 FINISHED
