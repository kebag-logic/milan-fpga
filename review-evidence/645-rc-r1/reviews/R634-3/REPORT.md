[R634] POSITIVE - exact head c66904a5b810a05527e8831eda5152f09f441bbe

# R634-3: composition review of PR #742 (#645 bind round) as the merge-train candidate

- **Candidate.** `c66904a5b810a05527e8831eda5152f09f441bbe`, tree `8979dd5abcb94b5af62c492f72343369dba6a64e`.
  - Parents: live dev `84f9e3001b7d9b77835c4a9a599dbe6230a8031b` and PR head `fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c` (tree `77e1321b`).
  - No other queued predecessor is in the candidate. The dev side since the PR's base `f62602531d41` is 77 commits over 77 files, PR #739 (#737, CI wall clock) among them, and #741 (bench lane B17) as well.
- **Scope.** Composition acceptance only. The source head already has two POSITIVE source reviews: R635-2 ([6195987516](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6195987516)) and R634-2 ([6196059375](https://github.com/kebag-logic/milan-fpga/pull/742#issuecomment-6196059375)).
- **Verdict.** The composed tree adds no defect beyond the reviewed sources.
  - No BLOCKER, MAJOR or MINOR is open.
  - Two new SUGGESTIONs are recorded, and one prior RESIDUE is retained in its design-page part.
  - This is not merge authorization, hosted acceptance or bench acceptance.

## 1. What composes, and how it was proved

### 1.1 The candidate is the clean automatic merge

`git merge-tree --write-tree 84f9e300 fb5dd3da` reproduces `8979dd5a`, the candidate tree, with rc 0. So there are no conflicts and no evil-merge bytes (`receipts/composition_identity.txt`).

- Candidate against the PR head: 11 of the PR's 12 files are blob-equal. The twelfth, `docs/testing/TESTING.md`, differs only by dev's hunk.
- Candidate against dev: 76 of dev's 77 changed files are blob-equal. The exception is `TESTING.md`.
- `git patch-id --stable` gives the same patch for each of the PR's 12 files across the PR delta (`f6260253..fb5dd3da`) and the composition delta (`84f9e300..c66904a5`).
- All six submodule gitlinks are equal across the candidate, dev and the PR head (`receipts/restore_verify.txt`).

### 1.2 Files both sides change

There is exactly one, `docs/testing/TESTING.md`. In candidate line numbers, the hunks do not overlap:

- the PR's hunks are at `:271`, `:304-306`, `:345-364` and `:630` (the merge bank row, the leg-count prose, the bind-round replica table and projection, and the `follow_ring` suite row);
- dev's hunk is at `:538-551` (the sixteen `--ci-pieces` workers).

The PR-added lines say nothing about worker counts, shards or `--ci-pieces` (a grep finds none). So dev's sixteen-worker rewrite leaves no PR sentence stale, and the PR leaves none of dev's stale.

The candidate contains one other "four standing legs" string, `TESTING.md:319`. It is the dated round-2h replica row, and it is correct as history (`receipts/stale_counts.txt`).

### 1.3 Semantic interactions checked

| Interaction | Why it could break | Evidence on the candidate | Result |
|---|---|---|---|
| Dev's mutant drivers plant text edits into `hdl/milan/milan_datapath.sv`, which the PR changes (`:6585-6644`). The dev-changed drivers are `milan_dp_mclk/mclk_mutants.py`, `capture_coherence/mutants.py` and `maap/mutants.py`, and their case lists feed dev's `--ci-pieces` partitions. | An anchor overlapping the new `settle_bind_*` block or the extra `settle_bind_arm_w \|\|` term would stop being unique. The driver would then refuse, or a piece would fail. | `scripts/anchor_probe.py`: 24 datapath-matching literals have equal counts in the dev parent and the candidate (`receipts/anchor_probe.txt`). `mclk_mutants.plant()` applies its selector and every `EDITS` entry to the candidate, with no build (`receipts/mclk_plant.txt`). | No interaction |
| Dev's `scripts/suite_shards.py` (#737) balances sixteen workers from `SUITE_SECONDS`. `follow_ring` is 1158 s there, a figure that predates the bind leg. | The PR's fifth leg measured +7.1 % (`TESTING.md:360-363`). | `scripts/shard_projection.py` reruns `headroom_problems` with `follow_ring` at 1158, ×1.0709, ×1.08 and ×1.10. In every case: no problems, worker 5 at 1539 to 1550 s against the 1620 s budget, and the largest non-dedicated load 1605 s (`receipts/shard_projection.txt`). `suite_shards.py --selftest` PASS. | Fits. See S1 for the stale estimate |
| Dev's `run_all_suites.sh` routes pieces through `ci_suite_pieces.py`. | It could change how `follow_ring` runs. | `follow_ring` is not in `PIECE_SECONDS` (`scripts/suite_shards.py:153-160`). It still runs as `timeout 1800 make -C`, and `suite_timeout`'s default is unchanged (`scripts/run_all_suites.sh:248-256`). | No interaction |
| `follow_ring`'s input closure. | A dev-side change to an input would invalidate the source-head results. | Dev changes 0 files under `hdl/`, `configs/generated/` or `tb/verilator/follow_ring/`. The candidate equals the PR head under all three, and the Makefile has no `include` (`receipts/follow_ring_closure.txt`). | The source receipts carry over |
| Dev's evidence and contract registries: `ci_events.py`, `measure_test_evidence.py`, which imports the PR-changed `measure_test_evidence_readers.py`, the generated workflows and the evidence pins. | A PR-changed reader or a dev-changed contract could disagree. | `ci_events.py --check` OK (2187 items) and `--selftest` PASS. `measure_test_evidence.py --check`: ratchet PASS, 0 unexplained DUT-source readers. `ci_gate_workflows.py --check` and `generate_ci_evidence_pins.py --check` rc 0. | No interaction |
| Dev's builder test (`sw/builder/test_builder.py`). | It asserts on datapath text. | Dev's 61 added lines are the `--list`/`--gates`/`--receipt` leg machinery only. The signed `manager-builder` bank ran at the candidate: 48 of 48 commands exit 0. | No interaction |
| Docs: the B17 section merged by #741 (`docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4612`) and the PR's design text. | Anchors could break, or the two pages could contradict each other. | `gen_toc.py --check` OK (147 pages), `--verify-anchors` (506 cross-page links), `docs_check.py` 0 findings, `check_doc_style.py` OK, `check_doc_paths.py` OK (989 paths), `check_em_dash.py --base 84f9e300` 0 findings over 144 added lines, and `--base f6260253` 0 over 1289. B17's "A bind at INTERNAL arms no settle recentre" (`:4909`) is dated history of the `5603c353` image. The design now changes that behaviour and cites #741. | No contradiction. See S2 |
| rtl-fast scope. | The changes classifier could miss the PR's files. | `scripts/ci_scope.py` is unchanged by dev, and the PR's `hdl/` change keeps the RTL scope. | No interaction |

All gate exit codes and commands are in `receipts/gates/SUMMARY.txt` and `COMMANDS.txt`, with each log beside them.

### 1.4 Signed local CI packet

The packet is at `review-evidence/645-rc-r1/local-ci/fb5dd3da` on `da8d1462` (`receipts/signed/`).

1. `allowed_signers` holds one key, principal `milan-local-ci`, namespace `milan-local-ci`, ED25519 fingerprint `SHA256:dRI12tvJkhueTEGqsRutn2L+dT/5qqOCsCVzBU5CI7k`. That is the required key.
2. `ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci -s manifest.json.sig < manifest.json` gives: `Good "milan-local-ci" signature ... SHA256:dRI12tv...`, rc 0 (`receipts/signed/verify.txt`). The `manifest.json` sha256 is `b21602641da02827e3dd6f3c4c37aadf57c78b7a60cc30d293724a6fc37f8070`, as briefed.
3. The manifest's subject fields all match this candidate and head:
   - `candidate` `c66904a5`, `candidate_parent` `84f9e300` and `candidate_tree` `8979dd5a`;
   - `head` `fb5dd3da` and `head_tree` `77e1321b`;
   - PR 742.

   The four `definitions.candidate` and four `definitions.head` workflow hashes equal sha256 of `.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml` at the candidate and at the head.

   All 22 coverage entries carry `ok: true`, and every bank has exit 0 for every command:
   - census: 1 of 1;
   - firmware: 7 of 7;
   - full-native: 5 of 5;
   - manager-builder: 48 of 48.
   - **The act exit code is 1.** `rtl-fast/publication-census` failed under act on a slot-cgroup OOM (#744), and act then cancelled `firmware-unit`, `verilator-shards` and `yosys-shards`. The manifest maps each of those four to a native bank at the candidate, with its reason. `rtl/physical-gptp` is `not-run`, with a stated reason: it runs nightly and on manual dispatch only.
   - So the coverage claim is consistent with the manifest. The act job verdicts are local evidence, not hosted acceptance.

## 2. Findings

### R634-3-S1 SUGGESTION (Tests): `follow_ring`'s scheduling estimate predates the bind leg

- **Where:** `scripts/suite_shards.py:97`, `"follow_ring": 1158` on the candidate, from dev's #737 table.
- **Evidence:** the PR's own projection puts `follow_ring` at 1114.2 s × 1.0709 = 1193.2 s hosted (`TESTING.md:363`). Scaled the same way, the table's 1158 s would be about 1241 s.
  - Under the table as committed, worker 5 is predicted at 1539 s. With the extra ~83 s it would be about 1622 s, a hair over the 1620 s scheduling budget. The job limit is 45 min, so there is no timeout risk.
  - Re-balanced with the scaled figure, the projection passes: worker 5 at 1546 s and every worker inside its bounds (`receipts/shard_projection.txt`).
  - The module's rule asks for a provisional figure only for new suites, so nothing is violated.
- **Impact:** the scheduler's prediction for one worker is optimistic by about 83 s. No gate result or timeout changes.
- **Optional outcome:** after hosted acceptance of the merged head, refresh `SUITE_SECONDS["follow_ring"]` from that run with `suite_shards.py --measure`.

### R634-3-S2 SUGGESTION (Docs): cite the merged B17 section, not only PR #741

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1268-1269`. The page cites "bench lane B17 ([PR #741], [its report])" and the packet on an evidence branch.
- **Evidence:** in the candidate, B17 is merged as `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md#dev-5603c353-2026-10-15-lane-b17` (`:92`, `:4612`).
- **Optional outcome:** add an in-repo link to that section beside the PR link. No figure changes.

### Prior findings at this head

None of these is reopened by the composition: every affected blob equals the source head.

| Prior ID | Severity, lenses | Status at `c66904a5` | Evidence |
|---|---|---|---|
| R635-1-F1 = R634-1-F1 (the 10 us lower bound) | MINOR; Conformance, Tests, Docs | RESOLVED, retained | `sim_main.cpp` is blob-equal to `fb5dd3da` (`203cd30f`). Both source re-reviews verified the 9.427 us derivation. |
| R634-1-F2 (the in-window one-pair dup) | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED as ruled, retained | The `MEDIA_CLOCK_FOLLOWING.md` blob is equal (`752b9d36`). The residual itself stays owned by #743, which is not hardware acceptance. |
| R634-1-S1 (the area headline) | SUGGESTION; Docs | ADDRESSED | The PR body cites `AREA_BUDGET.md:124` (`receipts/PR-BODY.at-review.md:46`). |
| R635-2-W1 (the overdefinite #743 pointer) | RESIDUE; Docs | FIXED in the PR body | `PR-BODY.at-review.md:100`: "Compare a bench reading ... with #743; its cause still requires evidence." |
| R634-2-R1 (the `c05.json` attribution) | RESIDUE; Docs, Conformance | PR body FIXED. Design page RETAINED. | The PR body's `:39` now names `c06.json`'s read. `MEDIA_CLOCK_FOLLOWING.md:1287` still reads "(its `c05.json`)", and `:1278` "slipped nothing", unchanged (`receipts/prior_residue_readback.txt`). The exact fix stands as R634-2 wrote it: at `:1287`, "(its `c05.json`, with `c06.json`'s first `SLIP_LB` read, 218 and unchanged, 43.9 s after cycle 5's bind; the 30.260 us burst came at 37.5 s, after cycle 5's last poll)", and at `:1278`, "slipped nothing through each cycle's last poll and, for cycles 1 to 9, the next cycle's first read". It stays on the manager's residue checklist. |
| R634-2-S1 (the `b17_bound.py` premise check) | SUGGESTION; Tests | Open, optional | That script is in the author's evidence packet, not in the tree. The composition does not touch it. |
| R634-2-S2 (the #640 budget clause) | SUGGESTION; Docs | ADDRESSED | `PR-BODY.at-review.md:46`: "0.047 % of the #640 plan's 6,373-LUT margin". |

## 3. Reviewer-owned ledger (round R634-3)

A lens the composition does not touch keeps its source coverage, which is named per row.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | **Composition:** issue #645 acceptance and rulings; the PR body ("Relates to #645", with the bench repeat outside the PR); `MEDIA_CLOCK_FOLLOWING.md` blob-equal to the source; dated B17 findings at `629_...BENCH.md:4612-4945` compared with the design's `:1264-1370`, with no contradiction. **Source coverage:** R635-2 and R634-2 at `fb5dd3da`. | R634-3 (composition); R635-2 and R634-2 (source) | c66904a5b810a05527e8831eda5152f09f441bbe |
| RTL | CLEAN | **Untouched by the composition:** `hdl/` is identical to `fb5dd3da` and dev changed nothing under `hdl/`. Also checked: the dev mutant anchors against `milan_datapath.sv:6585-6644` (`anchor_probe.txt`, `mclk_plant.txt`) and the signed full-native Yosys bank at the candidate. **Source coverage:** R635-1 PASS RTL at `2639eecf`, carried by R635-2 and R634-2 with an empty `hdl/` delta. | R634-3 (composition); R635-2 and R634-2 (source) | c66904a5b810a05527e8831eda5152f09f441bbe |
| Robustness | CLEAN | **Untouched by the composition:** the closure is byte-equal (`follow_ring_closure.txt`). The campaign evidence is the source's. **Source coverage:** R635-2 and R634-2 at `fb5dd3da`. | R634-3 (composition); R635-2 and R634-2 (source) | c66904a5b810a05527e8831eda5152f09f441bbe |
| Tests | CLEAN (S1 optional) | **Composition:** `suite_shards.py:97,153-160` with its selftest and the 16-worker projection (`shard_projection.txt`); `run_all_suites.sh:248-256`; `ci_suite_pieces.py` (`follow_ring` undivided); `measure_test_evidence.py --check` with the PR-changed readers table; `ci_events.py --check/--selftest`; `ci_gate_workflows.py --check`; `generate_ci_evidence_pins.py --check`; the signed manifest's full-native and act coverage. **Source coverage:** R635-2 and R634-2 at `fb5dd3da`. | R634-3 | c66904a5b810a05527e8831eda5152f09f441bbe |
| Docs | CLEAN (S2 optional; R634-2-R1 design part retained as RESIDUE) | **Composition:** the `TESTING.md` hunks on both sides (`:271`, `:304-306`, `:345-364`, `:538-551`, `:630`); the docs and TOC gates in `receipts/gates/`; B17 history against the design; `PR-BODY.at-review.md` with the prior residue read back. | R634-3 | c66904a5b810a05527e8831eda5152f09f441bbe |

## 4. Real limits

- **No suite was run here.** That includes `follow_ring`, the mutant campaigns and Yosys. The composition does not change `follow_ring`'s inputs.
  - Candidate execution rests on the signed manager banks. The manifest gives each command's argv hash and exit code, not its logs, and I did not open bank logs.
  - The mutant-anchor probe and the shard projection are static or model checks, not executions.
- **The act replay ran the PR head's workflow definitions, not the candidate's.** The head's are the pre-#737 six-worker files.
  - The candidate's sixteen-worker `verilator-shards` is covered by the native full bank (`parallel-suites.py`), not by the `--ci-pieces` partition itself.
  - Hosted runs at the merged head will be the first execution of this PR's suites under dev's partitioned workflow.
- **The markdown gates ran in a disposable pinned venv.** The first attempt without it refused (that is recorded in `COMMANDS.txt`).
- **The ratchet slack is not attributed.** `measure_test_evidence.py --check` reports slack ("can be lowered to 65"), which is informational. I did not check whether dev alone shows the same slack. The PR adds no suite.
- **No hardware evidence.** Physical calibration was NOT RUN, and the bench repeat of B17 (#645 acceptance item 3) was not run. Field skips are not hardware proof. #743's arming-window residual remains open.

## 5. Pending manager duties

- Exact-head hosted acceptance at the merged head. That includes `verilator-suites` under the sixteen-worker `--ci-pieces` workflow and `follow_ring`'s hosted window against the 1260 s figure `TESTING.md:344` requires.
- Optional S1: refresh `SUITE_SECONDS["follow_ring"]` from that measurement.
- Carry R634-2-R1's design-page wording (§2) on the residue checklist.
- Explicit maintainer authorization of the merge, then post-merge containment.
- After the merge, the bench repeat of B17's ten binds on a built image (#645 acceptance), and #743 kept open.

R634-3 FINISHED
