[R520] NEGATIVE - exact head 5428b044176f95248e6916dc00dd89c0df154078

# R520-1: internal cleared-context review of issue #682 / PR #692

- Repository: kebag-logic/milan-fpga, PR #692 (`682-pp-pin-2ad2f845` into `dev`).
- Exact head `5428b044176f95248e6916dc00dd89c0df154078`, tree `4a12e8029325593169fa91dbbf855dc3d5efee9d`.
- Source base and live dev: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` (the head's second parent; `ls-remote` confirmed dev unchanged during this review).
- Review start: PR #692 comment 6042151368. Role: internal reviewer, separate cleared-context session with its own clone.

## Verdict

NEGATIVE, on two open MINOR findings, both under `Docs`.

The engineering of the adoption holds. Both supplied patches are byte-exact, all records regenerate identically, all three merges are exact, and the 24 imported paths are untouched. The render differential reproduces independently at the exact head, with the same 32 outcomes and byte-identical clean-leg output. The frame-capture patch is load-bearing at the new pin and changes nothing at the old pin. Resource and timing figures are consistent with the committed records.

Two documentation items remain open. Every earlier pin adoption recorded its parent-observable changes in `CHANGELOG.md`; this one does not (F1). The resource recipe also still presents the worker cap as optional, even though baseline F's recorded identity requires it (F2).

`Conformance`, `RTL`, `Robustness` and `Tests` are covered clean at this head.

## Reconstruction (public state only)

1. `AGENTS.md`, `CONTRIBUTING.md` (sections 2 and 3), `docs/README.md`.
2. Issue #682 body and comments: the assignment (6018127147), the executor's TAKEN, STOP (6028310880) and REVIEW READY, and the round-2 ruling (6028334443). The ruling grades acceptance 4 "unchanged from dev; #657" through a pin-revert differential.
3. Issue #657 (the pre-existing 28/32 render defect). Issue #234 owner decision 5967924270 (NFR-RES-01 stays at 60 %; levers #232/#230/#639 before the second pin adoption; redesign under #640). `docs/reference/FR_NFR.md:464` (NFR-RES-01). `docs/design/AREA_BUDGET.md` (resource gate and re-baseline rule). `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`. `docs/reference/SUBMODULES.md`.
4. Processor PRs 156, 159, 160, 161, 162 and 164: bodies and parent-visible lists, and the published processor reviews' statements of both adoption patches.
5. `git diff e21c1ca0..5428b044` (17 files) and the full lane history: 8 one-line commits and 3 `--no-ff` merges. Every commit message is a subject line with no body or trailer.
6. Public evidence tree `8d4e0732:review-evidence/682-r1`: 130 files, all matching its `MANIFEST.json` published digests. Exact-head hosted check runs (read only).

## Findings

### R520-1-F1 - MINOR - Docs - `CHANGELOG.md` (no section for processor pin `2ad2f845`; latest pin section is `CHANGELOG.md:63`)

- **Authority/evidence:**
  - `AGENTS.md:144` requires updating authoritative documentation when behaviour changes.
  - `CHANGELOG.md:3` says the file "records current bare-metal product revisions"; `docs/README.md:108` routes "Find measured changes" to it.
  - Each of the six previous processor pin adoptions added an "Unreleased - processor pin <pin>" section inside its own lane: `990f9652` (`:316`), `0922e434` (`:278`), `16be6768` (`:250`), `b2db3a97` (`:181`), `631eeb34` (`:155`, commit `3370c6cb`) and `ead80360` (`:63`, commit `ca129e38` inside PR #663, with the same issue-scope wording as #682).
  - This adoption changes parent-observable behaviour, as listed by the lane itself in `docs/reference/SUBMODULES.md:158-185`. GET_COUNTERS notification spacing is now measured at grant (#148). Registrar expiry is ordered before same-clock reception (#134). A held DEREGISTER waits for the round boundary and can arrive later (#158). The resource baseline moves to F.
  - `git diff e21c1ca0..5428b044 -- CHANGELOG.md` is empty.
- **Impact:** The product's record of measured changes stops at `ead80360`. Anyone reading changes from the changelog does not see that three wire-observable behaviours changed in this image. That includes the release step and the bench operator running acceptance 5 (#608 withdrawal cycles).
- **Required outcome:** Either of:
  - an "Unreleased - processor pin 2ad2f845" section, with its contents entry, recording the adopted processor PRs, the parent-observable changes and the frame-capture harness adaptation. It should also record baseline F, unchanged ROMs and capture, and an unchanged VERSION.
  - a public manager decision that this adoption carries no changelog entry.
- **Verification:**
  - Read the section against `SUBMODULES.md:158-185`.
  - `scripts/gen_toc.py --check`, `scripts/docs_check.py` and `scripts/check_doc_style.py` return 0.

### R520-1-F2 - MINOR - Docs - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:105-110`, `:121-122`, `:185-186`, `:260`, `:454`

- **Authority/evidence:**
  - The current baseline, `syn/ooc/pp_resource_baseline.json`, starts every endpoint's recorded flow identity with `set_param synth.maxThreads 1` (`:14`, `:479`, `:937`). This applies to `route-1x1`, `ooc-1x1` and `ooc-8x8`; E carried the same identity.
  - `syn/ooc/pp_resource_gate.py:319-323` returns exit 2 for any identity difference: "NOT COMPARABLE: tool or recipe change in flow; measure the baseline again under the new identity instead of comparing across it".
  - The recipe describes `--single-thread-synthesis` as optional, "For a memory-constrained measurement" (`:105`).
  - Every measurement command omits the flag (`:121-122`, `:185-186`, `:260`). The Resource gate section then says "Run the shipping route and the 1x1 standalone synthesis as above" (`:454`).
- **Impact:** The next adoption or re-baseline that follows the recipe as written gets exit 2 at all three endpoints against F. The gate's own message then directs re-measuring the baseline: three extra Vivado endpoints, or a re-baseline recorded without a growth judgement across a flow change. The gate itself fails closed correctly; the operative procedure no longer matches the recorded baseline.
- **Required outcome:** The recipe states that the current baseline (F) was recorded with `--single-thread-synthesis`, and that measurements judged against it must pass the flag at every endpoint. The commands show it. Alternatively, the recipe states that dropping the flag first requires all three endpoints to be re-recorded at the base.
- **Verification:**
  - Read the recipe against the baseline's `identity.flow`.
  - `scripts/gen_toc.py --check` and `scripts/docs_check.py` return 0.
  - `syn/ooc/pp_baseline.py --selftest` remains PASS.

### R520-1-S1 - SUGGESTION - Docs - PR #692 body "How to validate", and the ruling's command `make -C tb/verilator/milan_dp_render tdm8render-mutants`

- **Evidence:** `tb/verilator/milan_dp_render/tdm8_render_mutants.py:80-82` says to run the campaign with `cd tb/verilator/milan_dp_render && make tdm8render-mutants` (not `make -C`). Under GNU Make 4.4.1 both forms give an identical verilator command (same md5 for `make -n tdm8render-build`), and the executor's `-C` runs under 4.3 reproduce this review's `cd` runs exactly. No result is affected.
- **Suggested outcome:** Quote the suite's documented form next time the body or the suite is touched.

## Prior public findings on this PR

At review start the PR carried only the two review-start comments; there were no review findings to resolve or retain. A later external verdict comment was not read before this report and ledger were written.

## Focus checks

### (1) Pin delta, wiring, regeneration, records and the two patches

- The gitlink moves `ead80360` -> `2ad2f845` and is the only processor change. The other three gitlinks are unchanged against dev. `ead80360` is an ancestor of `2ad2f845`, and `2ad2f845` is on processor `main` (compare: 24 ahead, 0 behind).
- `hdl/top/protocol_processor_top.sv` is byte-identical at both pins: 237,956 bytes, sha256 `84d89afb…a0e170`. The 46-entry processor source list (`scripts/pp_srcs.py`) is identical at both pins (`receipts/static/pp_srcs_*.txt`). The changed processor RTL is internal and adds no port:
  - `KL_aecp_notify` (#148, #158);
  - the SRP listener and talker FSMs (#134);
  - the originator and RX validator (#22, declaration moves);
  - comments only in side_port, trace_ring and tx_slots.
- Applying the published `parent-adoption-148-6c22d3ca.patch` (sha256 `bbd0301d…ecfea83`, 966 bytes, equal to the digest named in processor PR 164) and `parent-adoption-22-28f9666f.patch` (`8acf2b12…28e94f`) to dev's files gives the head bytes exactly:
  - `sim_nxn.cpp` `0c4b30fa…`;
  - `xvlog.budget` `f10b2bef…`.
- The parent's own `write_budget([])` regenerates `xvlog.budget` byte-identically, and `read_budget` returns empty sections (`receipts/static/xvlog_budget_regen.txt`).
- Generators re-run in a disposable head copy leave zero tracked changes (`receipts/static-rerun/regen_status.txt`, empty). This covers:
  - `check_port_contracts.py --write-budget` (census 2,079; ratchets unchanged);
  - `measure_naming.py --write-budget` (95 identities);
  - `submodule_boundaries.gen.py` (drawio, svg and png byte-identical).

  `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_port_contracts.py`, `measure_naming.py --check` and `pp_srcs.py --check` all return 0.
- ROM digests: the processor's own generators at `2ad2f845` give LTN `23cc67ee…e956` and microcode `518b900c…37f8`, equal to the new `rom_digests.tsv` rows and to the `ead80360` rows. Generator sources are unchanged across pins, and the ledger is in the writer's sort order.

### (2) Render differential

- This review ran two complete `tdm8render-mutants` campaigns concurrently with the pinned Verilator 5.050 (`--jobs`-equivalent `VERILATOR_JOBS=4`):
  - one at the exact head bytes (`tree-head` clean);
  - one at the same tree with only the processor gitlink and checkout reverted to `ead80360` and both patches reversed. That prior tree differs from dev `e21c1ca0` only in docs, records and `syn/` files that the render build does not read (`receipts/render_prior_vs_dev_paths.txt`).
- Both campaigns: rc 2, "32 checks: 28 PASS, 4 FAIL". All 32 case verdict lines are identical between the two runs and identical to the published adopted and prior records (`receipts/render_compare.txt`, OVERALL MATCH).
- The four failures are the #657 set:
  - the clean ship `--epoch-only` leg;
  - its two modelled-arrival-skew clean controls;
  - the surviving "uncounted repeat" mutant.
- The clean `--epoch-only` leg run directly at both pins: rc 1, 127 checks / 4 failures, the four T30 CRF recentre assertions. Stdout is 3,746 bytes, sha256 `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b` at both pins, byte-equal to the published `round2-render-adopted-clean-epoch.log`.
- The four passing clean legs (`multi`, `--crf-only`, `--law-only`, `--serial-only`) are byte-identical across pins. The `multi` digest `3f87ef97…` equals the executor's leg-0 receipt.
- The failing set exists independently of the pin. The executor's differential ran at `342f20ef`; this review reproduces the result at the exact final head.

### (3) Resources

- F against dev's D: route 50,318 -> 49,957 LUT (-361), 54,214 -> 54,274 FF (+60), 15,789 -> 15,734 slices, BRAM 87.5 and DSP 14 unchanged, WNS/WHS +0.124/+0.031 ns.
- F against E: standalone 1x1 and 8x8 are identical. Recipe identities and all policies match E, and `check-baseline` passes. The documented F-minus-E sub-block table matches the committed records cell for cell (`receipts/evidence/f_minus_e_scopes.txt`).
- Every percentage, headroom and gap figure in `AREA_BUDGET.md` and `findings/README.md` recomputes from the record:
  - 78.80 %, 11,917 over, 116 slices free;
  - 42.80 %, 99.27 %, 64.81 %, 5.83 %;
  - 11,211 LUT wrapper limit, 52 %, 0.094 ns fall.
- NFR-RES-01 (60 % LUT) is unmet and disclosed. Under the owner decision the levers (#232, #230, #639) were due before the second adoption (#661, which adopted them); the remaining redesign is #640 (Mark II). The gate holds every resource at its record, and this third adoption shrinks LUTs.
- After F was measured (`4d253880`), the later merges changed only opt-in mailbox RTL (`--ctrl-mailbox` defaults off, `sw/litex/milan_soc.py:3580-3585`), firmware, tests and docs. So no image or resource input moved. `sw/litex/deploy.sh` still hashes `2e176826…cd7` as bound in the image evidence.
- Synth 8-6901: the published per-file table covers exactly the 46 `pp_srcs` files, all zero in the three logs, plus one parent warning. Vivado was not re-run (not allowed).

### (4) Timing

`scripts/audit_timing_resources.py` over the published `round2-timing-directives.json` passes all checks (`receipts/evidence/audit_timing_resources.log`):

- four corners per route;
- worst = corner minimum;
- every corner WNS >= +0.03 ns and WHS >= 0;
- full routing with zero errors;
- worst-path text slack equal to worst WNS;
- every artifact carries a sha256;
- ExtraPostPlacementOpt selected and best (+0.124/+0.031). AltSpreadLogic_high is +0.090/+0.011 and ExtraTimingOpt +0.055/+0.020, matching the PR table;
- the selected route's utilisation equal to the committed route record.

The complete-image record binds bitstream `613a670a…80a8bc` (3,825,992 bytes), manifest `bb3ddd51…5774` and AEM `4fc8d615…396d` (7,512 bytes), with preflight rc 0. Routes and bitstream were not regenerated here (Vivado excluded).

### (5) Dev merges and imported paths

- `git merge-tree --write-tree` reproduces all three merges with rc 0 and tree-equal results (`receipts/merges/merge_tree.txt`):
  - `4d253880` (dev `79b086d4`);
  - `5af03224` (dev `d51b373a`);
  - `5428b044` (dev `e21c1ca0`).
- The final merge changes exactly the 24 paths of `d51b373a..e21c1ca0`. Each is blob- and mode-identical to dev, and none appears in `git diff e21c1ca0 5428b044` (`receipts/merges/final_merge_paths.txt`).

### (6) PR body against receipts

The numeric and structural claims checked above match. They cover:

- the pin;
- the top bytes;
- the patches;
- census 2,079;
- combination F;
- the timing table;
- the bitstream, manifest and AEM;
- 28/32 with identical outcomes;
- the clean-epoch bytes and digest;
- the 24 paths;
- the conflict-free merges;
- the 2,048-cycle bound;
- the 421-check notification target.

Claims that rest on executor-only runs at unchanged inputs are evidence-bound, not re-run. Those are the 60/60 sweep at `591a5752`, the field rerun, the firmware campaign and the vendor syntax. The manager's public static/builder and native banks at this head cover the final-head consumers.

## Probes run by this review

- Frame-capture patch probe on `make -C tb/verilator/milan_dp notify` (the timed [NOTIFY]/[GSI] leg; `receipts/notify/`):

  | Pin | Patch | Result |
  |---|---|---|
  | `2ad2f845` (head) | applied | 421 checks, 0 failures |
  | `2ad2f845` | reversed | rc 2; exactly `[NOTIFY-CRF] ...nor to A got=0x1 exp=0x2` (the defect processor PR 159 describes) |
  | `ead80360` | absent | 421 / 0 |
  | `ead80360` | applied | 421 / 0, with every graded and info line identical to the unpatched run |

  Graded lines at the head and at the old pin are identical. Only info timings move (CRF pushes 997 -> 1012 ms, the #148 effect). The patch is load-bearing at the new pin and masks nothing at the old one. It extends a window only while a frame is in progress, it is bounded at 2,048 cycles, and it keeps no state across calls.
- `scripts/lint_rtl.py --check` at head and at the old pin: PASS, 90 <= 90, with identical violation lists.
- `syn/ooc/pp_baseline.py --selftest` PASS. `syn/ooc/pp_baseline_mutants.py` rc 0, including both new worker-cap mutants ("ignored", "enabled by default") caught.
- `docs_check.py` (0 findings), `check_doc_style.py`, `check_doc_paths.py`, `check_archive.py`, and `gen_toc.py --verify-anchors` and `--check` under the pinned Markdown environment: all rc 0.
- `pp_resource_gate.py check-baseline` and `check_nvm_capture.py`: PASS.
- After all probes: the clone's HEAD, index tree and worktree equal `5428b044` / `4a12e802`. All 1,168 index entries match `ls-tree` in mode and blob, and every regular file rehashes to its blob. All three initialised submodules are clean at their gitlinks (`receipts/integrity/clone_integrity.txt`). Disposable trees under `scratch/` carry only their intended deltas.

## Per-lens results

```text
[R520] PASS Conformance - issue #682 acceptance 1-4 + ruling 6028334443; protocol-processor gitlink, both patches byte-applied to dev files (= head blobs), top/pp_srcs identity across pins, render campaigns at exact head and pin-reverted tree (32/32 outcomes equal, epoch stdout 3ef42e34 both), F record vs NFR-RES-01/owner decision, timing JSON audit vs BUILDING section 5 floors - all acceptance items met or graded per ruling; acceptance 5 is the manager's
[R520] PASS RTL - protocol-processor 2ad2f845 hdl delta (notify, SRP FSMs, originator, rx_validator, comment-only files) vs top byte identity and 46-file list; lint_rtl --check identical at both pins; route/standalone records F vs D/E; Synth 8-6901 per-file table vs pp_srcs; mailbox opt-in source closure for image inputs - no interface, CDC, reset or width change reaches the parent
[R520] PASS Robustness - tb/verilator/milan_dp/sim_nxn.cpp:963-973 drain_tx bound/statelessness (code read + four-way notify probe); render clean/failing legs byte-identical across pins; resource gate fail-closed path pp_resource_gate.py:319-323; disclosed MAC-stall and held-DEREGISTER limits in SUBMODULES.md:175-179 - no new failure mode
[R520] PASS Tests - notify leg 421/421 at head and caught (1 failure) with the harness patch reversed; base-pin control identical with/without patch; tdm8render-mutants full campaign twice at exact head bytes; pp_baseline selftest + 2 new worker-cap mutants caught; record generators re-run with zero drift
[R520] MINOR Docs - CHANGELOG.md (no 2ad2f845 section) - R520-1-F1
[R520] MINOR Docs - docs/testing/PP_SHADOW_BASELINE_RECIPE.md:105-110,121-122,454 - R520-1-F2
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #682 acceptance/ruling; gitlink and patch byte proof; top and source-list identity; two render campaigns and direct legs; baseline F against NFR-RES-01 and the owner decision; timing audit | R520-1 | `5428b044176f95248e6916dc00dd89c0df154078` |
| RTL | CLEAN | Processor hdl delta `ead80360..2ad2f845`; `protocol_processor_top.sv` digest; `pp_srcs`; `lint_rtl --check` at both pins; resource records D/E/F; Synth 8-6901 table; mailbox opt-in closure | R520-1 | `5428b044176f95248e6916dc00dd89c0df154078` |
| Robustness | CLEAN | `sim_nxn.cpp` drain_tx bound; four-way notify probe; cross-pin render leg bytes; gate refusal path; disclosed limits | R520-1 | `5428b044176f95248e6916dc00dd89c0df154078` |
| Tests | CLEAN | Notify probes; full render campaigns; `pp_baseline` selftest and mutants; generator zero-drift re-run; xvlog budget regeneration | R520-1 | `5428b044176f95248e6916dc00dd89c0df154078` |
| Docs | UNCLEAN (F1, F2) | `CHANGELOG.md`; `SUBMODULES.md`; `AREA_BUDGET.md`; `234_PP_SHADOW_AREA_BASELINE.md` (F section, F-E table recomputed); `findings/README.md`; `PP_SHADOW_BASELINE_RECIPE.md`; diagram and manifest; PR #692 body; doc gates | R520-1 | `5428b044176f95248e6916dc00dd89c0df154078` |

## Real limits

- Vivado was not run: synthesis, the three routes, the bitstream, xvlog analysis and `Synth 8-6901` counts are audited from published digests and records, not regenerated. Resource input digests could not be recomputed without a LiteX export; their stability is argued from source closure (no image input changed after `4d253880`).
- Not run, by assignment: the full 60-suite sweep, the full parent, processor, gPTP and Yosys banks, BDD, firmware, NVM and LiteX campaigns, the builder, and any act or hosted job. Those rest on the executor's receipts at `591a5752`, the field rerun and the manager's public banks at this head.
- Per-leg assertion text was compared directly only for the clean `--epoch-only` leg. For the two failing skew controls and the surviving mutant, the comparison is at case-verdict level (both runs and both published records). Their assertion-level equality rests on the published fresh-case receipts.
- Make 4.4.1 was used, not 4.3. Results nonetheless match the executor's 4.3 records byte for byte where comparable.
- Hosted exact-head state at writing: the gate contexts that had completed were success. These were `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, Yosys shards 0-3 and Verilator shards 0, 2, 3 and 4. Verilator shard 1 was still in progress, and the `verilator-suites` and `yosys-portability` aggregates had not yet reported. "Physical gPTP (nightly and manual)" was skipped (not executed). The manager owns hosted and local-replica acceptance.
- Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- Carry F1 and F2 to the executor (or rule on F1), then a re-review of the corrected head.
- Hosted `verilator-suites` / `yosys-portability` exact-head conclusions; local-replica acceptance.
- Final current-dev candidate validation at merge (source base and live dev both `e21c1ca0` at writing).
- Acceptance 5 after merge: the #608 withdrawal cycles (#134's registrar fix), the #658 default audio map, and the stream and counter soak.
- #657 stays open with its own acceptance.

## Receipts and reproduction

The `scripts/` directory holds portable scripts. Paths are arguments, and `VERILATOR` must point at a Verilator 5.050 build:

- `run_render_campaign.sh <tree> <out>`
- `compare_render.py <head-full.log> <prior-full.log> <round2-render-differential.json>`
- `run_notify.sh <tree> <out>`
- `audit_timing_resources.py <evidence-author-dir> <clone> <rev>`
- `static_checks.sh <disposable-head-copy> <out>`

The prior tree is the head copy with:

- `git -C protocol-processor checkout ead80360`;
- `git update-index --cacheinfo 160000,ead8036035affd53ef4b29979190f2f4f67084c0,protocol-processor`;
- `git apply -R` of both published patches.

Raw receipts are under `receipts/`, with host paths redacted to `$PACKET`, `$SCRATCH`, `$CLONE` and `$PINNED_VERILATOR`. Tool identity: `receipts/tools.txt`. Every published file is listed in `MANIFEST.sha256`.

R520-1 FINISHED
