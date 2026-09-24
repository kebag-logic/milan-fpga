[R311] POSITIVE - exact head af53f79854564bcca35e436758fa625d486c4993

# R311-2 external independent delta review: processor issue #113 / PR #115

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan
- **Exact head:** `af53f79854564bcca35e436758fa625d486c4993`, tree `6c50bc44d630e12507c298962d2fa859b9cbf3ce`. It merges main `265d6762` (processor #117) into the author's round-2 commit `4f6185ce`. Source base `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`. The round-1 reviewed head was `29840136`.
- **Reviewer:** [R311], external role. I worked in a cleared context from an isolated detached clone. There were no source edits, commits, pushes or GitHub writes. All GitHub access was read-only.
- **Scope authorities:**
  - the issue #113 body and decision comment 5821292534;
  - the round-2 assignment comment 5823271483 (items 1–4);
  - the PR #115 body at this head;
  - Milan v1.2 §5.4.5.2 with Table 5.22, as established in round 1;
  - the repository's contracts, unchanged in round 2 except `tb/pp_top/README.md` and REQ-NOT-003.

## Verdict summary

**R311-1-F1 is closed.** The latency comparator's full 32-bit width is now exercised at response level, and the documentation describes exactly what is exercised.

- **My round-1 probes, run unchanged.** The script's sha256 is `399a1e79…ab1c7`, identical to the round-1 publication. At round 1, all four comparator-truncation probes survived with 614 checks and 0 failures. At this head, all four fail named walk checks: [7:0], [15:0], [31:16] and bit 31 dropped.
- **The head's own mutants.** The seven latency mutants are read unmodified from the head's `gsi_mutants.py`: the trigger removal plus the six assigned truncations. Each fails its named check under that runner's grading rule.
- **Additional weakenings of my own.** These are outside the assigned six and all fail named checks: bit 0 dropped, bit 17 masked, rises-only, parity-of-difference, and the [2:0] narrowing named by the prior internal review.
- **Merge integrity.** The merge is mechanically exact: `git merge-tree` of the two parents reproduces the head tree.
- **Runner composition.** The composed `gsi_mutants.py` keeps both the round-2 mutants and #117's removal of the host deadline.
- **RTL.** Relative to `29840136`, the RTL differs only by #117's comment edits. The comment-stripped code is identical.

No finding is open at MINOR or above, so every lens is CLEAN and the verdict is POSITIVE. Two SUGGESTIONs are open and do not block: one new (R311-2-S1) and one retained from round 1 (R311-1-SA).

## Reconstruction

1. **Conventions.** The repository has no AGENTS.md or CONTRIBUTING.md; I checked again at this head. I followed README.md and docs/README.md as in round 1.
2. **Frozen scope.**
   - **Round-1 decision (5821292534):** unchanged.
   - **Round-2 assignment (5823271483):**
     1. Add a walking one and then a walking zero, so every one of the 32 comparator bit positions is at some step the only differing bit. Each step gives exactly one notification, and each unchanged repeat gives none.
     2. Retain mutants for [7:0], [15:0], [31:16], [30:0], [31:30] and bit 31 dropped, each failing a named check in the existing runner.
     3. Correct the README and doc wording.
     4. No RTL change. Existing suite counts stay the same, and the new checks are counted separately.
3. **Diffs examined.**
   - `a8f8ce81..af53f798`: 18 files, +216/-21.
   - `29840136..4f6185ce` (the author's round 2): 4 files, +75/-9. That is three files under `tb/pp_top` (`gsi_internal.hpp`, `gsi_mutants.py`, `README.md`) plus the REQ-NOT-003 row.
   - `4f6185ce..af53f798` (the merge side): 5 files. For each file, the changed-line hash equals that of `a8f8ce81..265d6762`, the #117 delta (`receipts/merge-and-rtl-provenance.txt`).
4. **Evidence.**
   - **Public evidence tree:** `kebag-logic/milan-fpga@21af9e2e…/review-evidence/pp113-r1`. I verified the files I read against `MANIFEST.json`, and all match (`receipts/public-evidence-check.txt`).
   - **Hosted checks at the exact head.**
   - **Prior public findings:** read only after my verdict and ledger were recorded (`receipts/verdict-before-prior-findings.txt`, 2026-09-24T23:15:22Z).

## Lens results

### Conformance: CLEAN

- Table 5.22 requires a GET_STREAM_INFO notification when the Stream Input's MSRP accumulated latency changes, for any change.
- The round-1 conformance analysis stands, because the RTL code is identical (see RTL).
- The round-2 tests now show conformance for single-bit changes at every position, in both directions and on both an Advertise and a Failed sink. Each change gives exactly one byte-exact unsolicited response carrying the new value, and the solicited read agrees.
- Unchanged repeats give none, and the other sink stays silent.

### RTL: CLEAN

- **Author round 2 made no RTL change:** `hdl` tree `83128bca…` is identical at `29840136` and `4f6185ce`.
- **Merge-side edits are comments only.** They come from #117:
  - `hdl/aecp/KL_aecp_desc_mem_guard.sv:40`, a port comment;
  - `hdl/top/protocol_processor_top.sv:521-524`, `:819-820`, `:2531-2532` and `:2546`, which move one comment and add three.
- **Comment-stripped code is identical.** With comments and whitespace stripped, both files hash identically at `29840136` and at the head (`receipts/merge-and-rtl-provenance.txt`, `receipts/rtl-diff-2984013-to-head.txt`).
- The comparator under test is still `hdl/srp/KL_srp_listener_fsm.sv:738`. The round-1 RTL analysis, fan-out, lint and area evidence carry forward unchanged.

### Robustness: CLEAN

My round-1 behavioural probes, rerun unchanged at this head (`receipts/r1-probes-unchanged/`), reproduce their round-1 verdicts:

| Probe | Verdict at this head |
|---|---|
| `r-always-pulse` | killed |
| `r-advertise-only` | killed |
| `r-all-sinks` | killed |
| `r-delayed-strobe` | killed |
| `r-strobe-to-acmp` | survives, as in round 1 (R311-1-SA) |
| `r-strobe-to-applicant` | survives, as in round 1 (R311-1-SA) |

The walk adds live-stream maintenance (`gsi_internal.hpp:310-316`):
- Discovery of both peers before each bit.
- A graded unchanged refresh of the peer.

This means a lapse and re-registration cannot stand in for a latency event. Any extra response in that path fails the exact-count, other-sink and empty-queue checks.

The runner has no host deadline after #117, so termination depends on the simulator's own cycle budgets and on finite loops. The walk is a finite 2 × 32 loop, and every run in this review terminated: my probe, rerun and suite builds each completed in under 6 minutes.

### Tests: CLEAN (R311-1-F1 closed)

**Walk design** (`tb/pp_top/gsi_internal.hpp:302-331`, called at `:345`):
- Sink 0 walks one from baseline 0, and sink 1 walks zero from baseline 0xFFFFFFFF. Both baselines are the latches the original sequence leaves (`:343-344`).
- Each bit is followed by a return to the baseline. Each changed refresh therefore differs from the previously committed value in exactly one bit: 128 changed refreshes, each repeated unchanged.
- Each `latency_refresh` (`:271-297`) checks:
  - the exact unsolicited count and the byte-exact frame;
  - the solicited read;
  - silence on the other sink and the other sink's value;
  - an empty response queue.
- The new checks are counted separately (`:329`).

**Counts at this head** (`receipts/suites/pp_top.log`): the full pp_top suite ran from an exact-head export with rc 0.

| Scope | Checks |
|---|---|
| Default build | 7,622 checks, 0 failures |
| Fixture build | 20 checks, 0 failures |
| Total | 7,642, which is 2,074 original + 5,568 added (the PR's figures) |

**Mutation evidence:**

| Probe (source) | Round-1 result | Result at af53f798 | First named failure |
|---|---|---|---|
| `r-cmp-low8` [7:0] (my R1 script, unchanged) | SURVIVED 614/0 | KILLED, 192 fails | `GI LATENCY-WALK-ONE bit 8 step: exactly one unsolicited response for sink 0, got 0` |
| `r-cmp-low16` [15:0] (R1, unchanged) | SURVIVED | KILLED, 128 | `… bit 16 step …` |
| `r-cmp-high16` [31:16] (R1, unchanged) | SURVIVED | KILLED, 128 | `… bit 0 step …` |
| `r-cmp-no-bit31` [30:0] (R1, unchanged) | SURVIVED | KILLED, 8 | `… bit 31 step …` |
| `r-trigger-removed` (R1, unchanged) | KILLED | KILLED-BY-NAMED-CHECK, 264 | `GI LATENCY-CHANGE: exactly one unsolicited response for sink 0, got 0` |
| `h-latency-trigger-removed` (head runner definition) | n/a | KILLED-BY-NAMED-CHECK, 264 | `GI LATENCY-CHANGE: exactly one …` |
| `h-latency-cmp-low8` (head) | n/a | KILLED-BY-NAMED-CHECK, 192 | `… bit 8 step …` |
| `h-latency-cmp-low16` (head) | n/a | KILLED-BY-NAMED-CHECK, 128 | `… bit 16 step …` |
| `h-latency-cmp-high16` (head) | n/a | KILLED-BY-NAMED-CHECK, 128 | `… bit 0 step …` |
| `h-latency-cmp-low31` (head) | n/a | KILLED-BY-NAMED-CHECK, 8 | `… bit 31 step …` |
| `h-latency-cmp-high2` [31:30] (head) | n/a | KILLED-BY-NAMED-CHECK, 240 | `… bit 0 step …` |
| `h-latency-cmp-bit31-dropped` (head) | n/a | KILLED-BY-NAMED-CHECK, 8 | `… bit 31 step …` |
| `x-cmp-no-bit0` [31:1] (reviewer) | n/a | KILLED-BY-NAMED-CHECK, 8 | `… bit 0 step …` |
| `x-cmp-no-bit17` (reviewer) | n/a | KILLED-BY-NAMED-CHECK, 8 | `… bit 17 step …` |
| `x-cmp-rise-only` (reviewer) | n/a | KILLED-BY-NAMED-CHECK, 130 | `GI LATENCY-WALK-ONE bit 0 return: …` |
| `x-cmp-parity` (reviewer) | n/a | KILLED-BY-NAMED-CHECK, 4 | `GI LATENCY-CHANGE: exactly one …`, from the original even-weight transitions; single-bit walk steps always have odd parity, so the walks alone cannot catch this weakening |
| `x-cmp-low3` [2:0] (reviewer; the prior internal review's probe) | n/a | KILLED-BY-NAMED-CHECK, 232 | `… bit 3 step …` |
| golden (R1 script and R2 script) | PASS 614/0 | PASS 6,182/0 | none |

- **Grading rule.** The `h-*` and `x-*` rows use the head runner's rule: a completed run, rc 1, and a FAIL line with the named prefix. The `r-cmp-*` rows use the round-1 script's unexpected-kill grading, where KILLED means any failure; the named first failure is quoted from the logs.
- **Named checks.** Every head mutant's named check matches the README table (`tb/pp_top/README.md:93-99`).
- **Round-1 `t-*` feasibility variants.** These are also in my unchanged script. They insert two extra refreshes before the walks, which moves sink 1's latch off the walk's 0xFFFFFFFF baseline. So `t-golden` now fails, first at the peer maintenance check (`LATENCY-WALK-PEER-REFRESH`). That is a consequence of the probe edit clashing with the new sequence, not a head defect. The `t-*` variants were a round-1 feasibility demonstration and are superseded by the head's walks. I report them for completeness (`receipts/r1-probes-unchanged/results.json`).

**Composed runner** (`tb/pp_top/gsi_mutants.py`):
- The round-2 mutants are at `:23-37`.
- #117's host-deadline removal is at `:94-100`: no `timeout=` argument, with #117's cycle-budget comment.
- `git grep` finds no `timeout` or `deadline` in the file.
- It holds 20 mutants: 7 latency plus 13 pre-existing.

### Docs: CLEAN

- **`tb/pp_top/README.md:59-77`** now describes exactly what the test does:
  - the original values are retained;
  - the walking one is on Advertise and the walking zero on Failed;
  - the return-to-baseline isolation;
  - 128 changed refreshes and 256 refreshes in total;
  - 64 silent maintenance refreshes;
  - the separate subtotal.

  I confirmed each figure against the code and the run log. The false "full comparison width" sentence is gone; `git grep` finds no residual full-width claim in docs, tb, syn or README.
- **Mutation table** (`:93-99`): matches the runner.
- **REQ-NOT-003** (`docs/00_MILAN_COMPLIANCE_REVIEW.md:377`): the evidence text names the walks and the six mutants; status P is unchanged and correct.
- **PR body:** its Round 2 section and the validation table match the observed counts (7,642; 5,568 added; 20 mutants).
- **Doc gates at the exact head** (`receipts/doc-gates.txt`), all rc 0:
  - links: 856;
  - matrix: 115 REQ and 17 GAP;
  - modmatrix: 92 rows, 0 untested;
  - diagram lint: 41 mermaid and 18 wavedrom;
  - wavedrom check: 18;
  - fixture-guard self-test;
  - `gsi_mutants.py` compiles.

## Findings

No MINOR, MAJOR or BLOCKER finding is open at this head.

### R311-2-S1: SUGGESTION (Docs). README line wrap

`tb/pp_top/README.md:75-76` breaks a sentence after "run log;" and leaves the next line overlong. The rendered Markdown is unaffected. Rewrap it at the next touch. This does not affect the verdict.

### R311-1-SA: SUGGESTION (Tests). Wire-level guard for the latency strobe: RETAINED

- **Where:** `tb/pp_top/gsi_internal.hpp` latency section; `tb/pp_top/gsi_mutants.py`.
- **Evidence:** `r-strobe-to-applicant` and `r-strobe-to-acmp` still pass all 6,182 GI checks (`receipts/r1-probes-unchanged/r-strobe-to-*-run.log`). This was outside the round-2 assignment.
- **Impact:** none today. The RTL keeps these paths closed, as shown by the round-1 fan-out and the unchanged code. The gap is a missing regression guard.
- **Suggested outcome:** a `listener_news() == 0` check around one latency-only refresh, plus a retained mutant that feeds the latency difference into `ind_reg_w`.
- **Verification:** that mutant must fail a named check.

## Prior public review findings: resolved or retained at this head

These were read only after my verdict and ledger were recorded. The prior public reviews on PR #115 are R310-1 (comment 5822538155) and my own R311-1 (5823269222).

| Prior item | Disposition at af53f798 | Basis |
|---|---|---|
| R311-1-F1 MINOR (Tests, Docs): comparator width not exercised; README claims full width | **RESOLVED** | All four of my round-1 truncation probes are killed by named walk checks. The six assigned truncation mutants are retained and killed. The claim is replaced by an accurate description. |
| R310-1 F1 MINOR (Tests, Docs): same defect; its probes include [2:0] and [31:30] | **RESOLVED** | [31:30] is the head's `latency-cmp-high2` (killed at bit 0). [2:0] is my `x-cmp-low3` (killed at bit 3). [15:0] and [30:0] are killed. The README is corrected. |
| R311-1-SA SUGGESTION (Tests): wire-level guard | RETAINED, non-blocking | Unchanged; see above. |
| R310-1 S1 SUGGESTION (Docs): integrator note on live selector-3 derivation | RETAINED, non-blocking | `docs/guides` is unchanged since `29840136`. The contract still holds, as in round 1. |
| R310-1 S2 SUGGESTION (Docs): the A15/A8 latch clear raises no latency strobe | RETAINED, non-blocking | `10_srp_engine.md` is unchanged since `29840136`, and the RTL behaviour is unchanged. |
| R310-1 S3 SUGGESTION (RTL/area): optional shared comparator | RETAINED, optional | The RTL is unchanged. |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 5.22 obligation versus the new single-bit response evidence; round-1 analysis carried forward, as the RTL code is identical to `29840136` | R311-2 (delta) on R311-1 | af53f79854564bcca35e436758fa625d486c4993 |
| RTL | CLEAN | `hdl` diff `29840136..af53f798` (#117 comments only, comment-stripped hashes identical); `hdl` tree identical `29840136`/`4f6185ce`; `git merge-tree` recomputation equal to the head tree; comparator `KL_srp_listener_fsm.sv:738`; round-1 RTL ledger carried forward | R311-2 (delta) on R311-1 | af53f79854564bcca35e436758fa625d486c4993 |
| Robustness | CLEAN | Round-1 behavioural probes rerun unchanged (killed/survived as in round 1); walk maintenance design; no-host-deadline runner termination observed | R311-2 (delta) on R311-1 | af53f79854564bcca35e436758fa625d486c4993 |
| Tests | CLEAN | `gsi_internal.hpp:271-345`; composed `gsi_mutants.py:20-37,94-100`; round-1 script unchanged (17 variants); 7 head latency mutants plus 5 reviewer weakenings; pp_top 7,642/0; author round-2 mutant and reviewer-probe receipts (at `4f6185ce`) | R311-2 | af53f79854564bcca35e436758fa625d486c4993 |
| Docs | CLEAN (S1 suggestion only) | `tb/pp_top/README.md:59-99`; REQ-NOT-003 `:377`; PR body Round 2 and validation table; residual-claim grep; doc gates rc 0 | R311-2 | af53f79854564bcca35e436758fa625d486c4993 |

## Public evidence consulted

**Author round-2 subtree** (`author-r2/`). All 13 files I read match their `MANIFEST.json` published sha256.
- Its receipts are at `4f6185ce`, not at the merge head:
  - `mutants.json`: rc 0 in 790.89 s;
  - `suites.json`: rc 0;
  - `final-integrity.json`: `rtl_unchanged: true`;
  - `review-probe-provenance.json`: records my round-1 script sha256 `399a1e79…ab1c7` as unchanged before and after execution, which matches my copy.
- The pinned tree has no manager subtree: `MANIFEST.json` lists 319 entries, all under `author*` or `reviews/`. So I did not verify the manager's static/builder and native banks at this head from published receipts; that result is taken from the review brief.

**Hosted checks at the exact head** (`receipts/hosted-check-runs.txt`):
- **Runs:** two `hdl` workflow runs, push 36069982021 and pull_request 36069985542.
- **Jobs:** each executed docs-gates, portability and suites. All 6 of 6 check runs completed with success, and none was skipped.
- **Legacy status API:** `pending` with 0 contexts, meaning none are posted.

The manager owns hosted and act acceptance.

## Real limits

- **What I ran.** Focused suites, doc gates and disposable probes only, with at most 8 parallel compile jobs. I did not run:
  - the full processor, parent, gPTP, Yosys or builder banks;
  - OOC synthesis;
  - Docker/act, host act_ci or its self-test;
  - anything on hardware.
- **Mutation coverage.** I did not run the head's complete 20-mutant runner end to end. The 13 non-latency mutants are unchanged in definition, and their RTL is code-identical. Their verdicts rest on the author's `4f6185ce` receipt and on the manager bank reported in the brief.
- **Area.** Area figures are the round-1 published reports. The RTL code is identical, and I did not resynthesize.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof. There is no routed-timing claim.
- **Probe environment.** Probes ran in `git archive` exports of the exact head. The only build change was compile parallelism (`-j 0` → `-j 4`/`-j 8`).
- **Clone state.** The clone was never modified. After all probes (`receipts/clone-restore-check.txt`):
  - HEAD is detached at the exact head;
  - the index tree equals the HEAD tree `6c50bc44…`;
  - all 246 tracked blobs and modes match;
  - there are no untracked or ignored files.

  The repository has no `.gitmodules` and no gitlinks, so no submodule gitlinks are required.
- **Walk scope.** The walks exercise sink 0 (walking one) and sink 1 (walking zero) of a two-input GI image. The comparator is one generate-loop expression per sink, so the other sinks share the same code. Other-descriptor silence is checked through the empty queue.

## Pending manager duties

- The final current-dev candidate build and banks at the merge turn: source base `a8f8ce810ddba1816cd129d0afcd71e6e02ade1b`, live dev `ffcbd33de70278ae34b533dcbadde0b36c8cba13`. The author's parent comparison used dev `573f0052`, not live dev.
- The manager-bank parent consumer 7/7 with the `a8f8ce81` control.
- Hosted and act acceptance.
- Publication of the manager bank receipts at this head. They are not in the pinned evidence tree.
- The parent re-pin as a separate lane after merge.
- The merge-completion bar: two independent positive reviews.

## Reproduction and receipts

- **`scripts/r1_probe_mutants.py`:** my round-1 script, byte-identical (sha256 `399a1e79…ab1c7`). Run it with `--repo <clone> --rev af53f79854564bcca35e436758fa625d486c4993 --verilator <pinned 5.050> --scratch <dir> --out <dir> --workers 2 --jobs 4`. Results are in `receipts/r1-probes-unchanged/` (`results-golden.json`, `results.json`, per-variant logs).
- **`scripts/r2_probes.py`:** the same flags. It loads the latency mutants from the exported head's own `gsi_mutants.py` (`h-*`) and adds reviewer weakenings (`x-*`). Results are in `receipts/r2-probes/`, and `x-cmp-low3` is in `receipts/r2-probes-low3/`.
- **Suite:** `receipts/suites/pp_top.log`, from the default `make` in an exact-head export of `tb/pp_top`.
- **Other receipts:**
  - `receipts/merge-and-rtl-provenance.txt`
  - `receipts/rtl-diff-2984013-to-head.txt`
  - `receipts/doc-gates.txt`
  - `receipts/hosted-check-runs.txt`
  - `receipts/public-evidence-check.txt`
  - `receipts/clone-restore-check.txt`
  - `receipts/verdict-before-prior-findings.txt`
  - `receipts/tool-identity.txt`: the simulator reports 5.050 rev v5.050; wrapper sha256 `905795b9…e92f`, wrapped binary sha256 `44898b22…bfdd`, identical to round 1.

R311-2 FINISHED
