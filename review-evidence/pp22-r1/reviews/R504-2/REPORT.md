[R504] POSITIVE - exact head d52bd7f277c6339b13fe7c8ebe849b25f3e14638

# R504-2: internal independent review of PR #162 (Relates to #22), round 2

| Item | Value |
|---|---|
| Exact head | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638`, tree `7b74e9bc8bee72a089f20b38578ac6d64b474b96` |
| Shape | `--no-ff` merge: parent 1 `2139f3dc` (round-1 POSITIVE head), parent 2 `7e5415e0` (processor `main`, #134 via PR #160) |
| Source base | `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` |
| Verdict | POSITIVE: no open BLOCKER, MAJOR, MINOR or RESIDUE. Two round-1 SUGGESTIONs are retained, and the delta does not touch either |
| Order kept | My verdict and ledger were recorded (`receipts/verdict-before-prior-findings.txt`, 06:46:52Z) before I read any prior public review report |

## 1. Reconstructed scope

- **Repository instructions.** No `AGENTS.md` or `CONTRIBUTING.md` is tracked. The governing texts are `README.md`, `docs/README.md` (conventions, single-source rules, and `make check` before commit) and `hdl/README.md` (consumption contract: a pin moves only to a commit whose `make check` and `tb/` sweep are green).
- **Issue #22 acceptance.**
  - `xvlog -sv` analyses every module under `hdl/` with rc 0 and no `VRFC 10-3380`.
  - Zero `Synth 8-6901` in Vivado synthesis of the consumer wrapper.
  - Suites stay green.
- **Assignment** (issue comment 6008772151). Two remaining sites, `KL_pp_originator.sv:194` `cancel_hit_w` and `KL_pp_rx_validator.sv:383` `vd_push_w`. The change must be a pure declaration move, with:
  - a patch-context check first;
  - Yosys statistics identical at base and head;
  - zero `VRFC 10-3380`/`10-8530` over the derived list;
  - a parent ratchet patch that drops the two budget lines.
  - STOP on anything that is not a pure move.
- **Manager ruling** (PR body). `Synth 8-6901` is measured at the next parent pin adoption, and #22 closes on that. The PR says `Relates to #22`, which keeps this boundary.
- **Round-2 focus** (review start 6010668449 and assignment):
  - the merge is clean;
  - the #134 files are byte-identical to `main`;
  - the #22 moves are unchanged;
  - xvlog still reports zero at the merge head;
  - the donor and consumer banks pass;
  - every patch and exact-text arm plants, including #134's new ones.
- **Interface authorities.** None is touched. The merge adds no port, parameter or behaviour change to the two packet-engine modules. The #134 SRP change is outside this PR's scope and arrives byte-identical from reviewed `main`.

## 2. Executed evidence (this reviewer, round 2)

All builds ran in disposable `git archive` exports or a scratch clone under `scratch/`. Simulator: the scoped Verilator 5.050 wrapper (identity and sha256 in `receipts/suites/verilator-identity.txt`). Independent campaigns ran concurrently, each with its own log and rc file.

| # | Check | Result | Receipt |
|---|---|---|---|
| E1 | Merge cleanliness | `git merge-tree --write-tree 2139f3dc 7e5415e0` gives exactly `7b74e9bc…`, the head tree, so there is no conflict and no manual resolution. `origin/main` = `7e5415e0`; branch and `refs/pull/162/head` = `d52bd7f2` | `receipts/01-merge-integrity.txt` |
| E2 | #134 files vs `main` | All 24 files changed `e6a759de..7e5415e0` have the same blob at head as at `main`. `git diff 7e5415e0 d52bd7f2` is exactly the two PR files (5+/5−). No file is shared between the two sides. Modes are all `100644` | `receipts/01-merge-integrity.txt` |
| E3 | #22 moves unchanged | `KL_pp_originator.sv` blob `0aaeb6e2…` and `KL_pp_rx_validator.sv` blob `158f0b17…` are identical at `2139f3dc` and the head. The diff is four declaration lines and one blank line moved. Every declared name precedes its first use (originator: declared at 188–189, used at 197–198; validator: declared at 232–233, first use at 385) | `receipts/02-pr-source-diff.patch` |
| E4 | xvlog over the derived list (packages first, sorted; fresh library; one invocation per file) | **Head: 46 files, 46 × rc 0, 0 `VRFC 10-3380`, 0 `VRFC 10-8530`**, both with `-d SYNTHESIS` (the consumer gate's define) and without. Base `e6a759de` and `main` `7e5415e0` each fail only the two expected modules, each with one 3380 (`cancel_hit_w`:194, `vd_push_w`:383) and one 8530. So #134's SRP code analyses clean, and the merge head's zero is this PR's work | `receipts/xvlog/*.json`, `*.txt`, `*.rc` |
| E5 | Structural identity (sv2v → yosys `hierarchy; proc; opt_clean; stat -json`) | `KL_pp_originator`, base = head `102354aa…`, and `KL_pp_rx_validator`, base = head `b48ab825…`. Both hashes equal the round-1 published hashes. `protocol_processor_top`: `main` = merge head `81cd62d8…` (59,606 cells, 43 modules). The base top (59,534 cells, equal to the published count) differs only by #134's SRP cells | `receipts/yosys/` |
| E6 | Every `tb/**/*.patch`, `git apply --check` | Head: **283/283** (277 + 6 new from #134). Round-1 head and base: 277/277 | `receipts/planting/planting-*.json` |
| E7 | Exact-text arms, each planted with its table's own `plant()` into a fresh copy | Head: notification 56, ACMP 33, D3 110 = **199/199**, with no refusal and the edited file changed | same |
| E8 | Patch-driven tables: every label resolves to a patch | adp 41, maap 29, aecp-dispatch 40, aecp 61, ctr 17, srp_top **120** (113 + 7 new #134 rows): all present | same |
| E9 | Negative controls | Five of six new #134 patches refuse at base (`lv-never-ends` legitimately applies there). A notification arm with its text removed is refused by `plant()` ("occurs 0 times"). The census can fail | `receipts/planting/negative-control.txt` |
| E10 | Donor suites at head (the changed modules and their consumers) | `originator` 107/107, `rx_validator` 555/555, `pp_top` 10,444/10,444 (six-build canonical tally), `ca_originator` 16/16, `maap` 196/196: every rc 0 | `receipts/suites/` |
| E11 | #134 suites at the merge head | `srp_top` 8,656/8,656, `srp_stream_fsms` 1,347/1,347: rc 0 | same |
| E12 | #134 new mutation arms at the merge head (`tb/srp_top/mutants.py --only <6 new labels> --jobs 4`) | 3 clean controls PASS. 7/7 runs KILLED (S1, S2, SC1 ×3, SC2, SC3 tags). `10 checks: 10 PASS, 0 FAIL` | `receipts/suites/mut134.log` |
| E13 | `scripts/lint_hdl.sh` at head | 41 LINT OK, 0 FAIL/ERROR, rc 0 | `receipts/suites/lint_hdl.log` |
| E14 | `make check` at head (scratch clone) | rc 0: lint, wavedrom, links, matrix, modmatrix, params, ids (+selftest), figures (+selftest), stale | `receipts/suites/make-check.log` |
| E15 | Parent ratchet contract | `parent-adoption-22-28f9666f.patch` (sha256 matches the published manifest) passes `git apply --check` against live dev `423ac5d9`'s `scripts/xvlog.budget`, leaving 0 submodule findings. This matches E4's zero | `receipts/parent/adoption-22-apply.txt` |
| E16 | Public evidence integrity | All 10 downloaded `pp22-r1` files match `MANIFEST.json` published sha256 | `receipts/public-evidence-hashes.txt` |
| E17 | Stale-citation search | No line-number citation into either moved file exists in `docs/`, `tb/` or `hdl/` | (search recorded in this report) |
| E18 | Hosted, exact head (snapshot 06:47Z) | Runs 37423565146 and 37423558584: `docs-gates` success, `portability` success; `suites` **in progress** in both. Combined status `pending` | `receipts/hosted-check-runs.txt` |

## 3. Lenses

- **Conformance: CLEAN.**
  - Assignment items 1–4 hold at the merge head (E3–E8, E15). Item 3 (statistics identity) is re-shown for the leaf modules and, for the top, across the merge (`main` → head).
  - The merge introduces no non-move change to this PR's files (E1–E3).
  - The `Synth 8-6901` item stays deferred by the manager ruling, and the PR keeps `Relates to #22`.
- **RTL: CLEAN.**
  - The source delta is exactly the round-1 move (E3).
  - The merged-in SRP RTL is byte-identical to reviewed `main` (E2).
  - The two sides share no file, and the merged result reproduces mechanically (E1).
  - Lint is clean over all 41 modules (E13), and structure is identical across the merge (E5).
- **Robustness: CLEAN.**
  - Both modules are now eligible for the analysis front-end, and the merge head carries no new front-end finding from #134 (E4, `main` row).
  - The ratchet patch still applies at live dev and agrees with the measured zero (E15).
  - The planting census and its controls show that no patch context drifted across the merge (E6–E9).
- **Tests: CLEAN.**
  - The donor and #134 suites pass at the merge head (E10, E11).
  - #134's own new arms plant (E6, E8) and are killed at the merge head (E12).
  - All 283 patches and 199 exact-text arms plant (E6, E7).
- **Docs: CLEAN.**
  - `make check` passes (E14), and there are no stale line citations (E17).
  - The PR body states its validation revision (`2139f3dc`) explicitly, so its figures (33 suites, 1,021,651 checks, 277 patches) stay accurate as a record of that revision rather than a claim about the merge head.
  - The manager note's deferred-synthesis boundary still holds.

## 4. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE in this round.

**Prior public findings, resolved or retained at this head.** I read these only after recording my own verdict.

- **R505-1:** no findings. Nothing to carry.
- **R504-1 S1** (SUGGESTION, RTL readability; `hdl/packet_engine/KL_pp_rx_validator.sv:232-233`). **RETAINED, unchanged.**
  - The file blob is identical at round 1 and at head (`158f0b17…`), and the merge does not touch it.
  - It stays a SUGGESTION. The 7-space padding and distance from the V9 section follow from the byte-identical-move requirement, with no functional effect.
  - Optional outcome, as stated in round 1: a later cosmetic pointer comment, with a fresh patch-context check.
  - Verification: re-run E6/E7.
- **R504-1 S2** (SUGGESTION, Tests/Docs; `hdl/README.md:46-48`). **RETAINED, unchanged.**
  - `hdl/README.md` is identical at round 1 and at head (`5407ada9…`).
  - No processor-side declare-before-use check exists at head (search of `scripts/`, `.github/` and `hdl/README.md`).
  - Optional outcome: a follow-up issue that either names the rule or adds an analysis-only check.
  - Verification: that issue's own acceptance.
- **Other entries.** The PR has 0 submitted reviews and 0 inline comments (`receipts/prior-findings.txt`). R505-2's report on this same head appeared during this round. It is a concurrent report, not a prior finding, and I did not read it.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #22 body and comments 5974073699/5979513404/6008772151; PR body and manager note; E1–E8, E15 | R504-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| RTL | CLEAN | `KL_pp_originator.sv:185-245`; `KL_pp_rx_validator.sv:229-233,385,620-631`; merge parents and tree (E1); 24 #134 blobs (E2); lint (E13); yosys (E5) | R504-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Robustness | CLEAN | xvlog at base, `main` and head, with and without `SYNTHESIS` (E4); parent budget and patch at live dev (E15); planting controls (E9) | R504-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Tests | CLEAN | 7 suites (E10, E11); #134 new-arm campaign (E12); 283 patches, 199 exact-text arms, 308 patch-table labels (E6–E8) | R504-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |
| Docs | CLEAN | `README.md`, `docs/README.md`, `hdl/README.md`; `make check` (E14); citation search (E17); PR body vs evidence; public `pp22-r1` manifest (E16) | R504-2 | `d52bd7f277c6339b13fe7c8ebe849b25f3e14638` |

## 6. Real limits

- **Banks not run, by rule.** I did not run the full 33-suite processor sweep (`scripts/run_suites.sh`), the full parent consumer set of 17, the Yosys/builder banks, or the parent `xvlog_gate.py --check` in a parent tree. Instead:
  - E10/E11 ran the seven suites that compile the changed modules or the #134 SRP FSMs.
  - E4/E15 cover the submodule section of the parent ratchet.
- **Manager bank evidence not found.** The assignment says the manager's full source static/builder and native banks passed at this head. The public evidence linked for this round (`pp22-r1`) is the round-1 author packet at `2139f3dc`. The issue and PR timelines carry no manager receipt for `d52bd7f2`. I am reporting that statement as given, not as something I verified.
- **Not measured, by ruling.** No `Synth 8-6901` count was taken. No Vivado synthesis or implementation was run; xvlog was used for analysis only.
- **Equivalence evidence.** The structural statistics are a stat-level identity, not formal equivalence. For the two modules, the byte-level move proof (E3) carries the source-level claim.
- **Kill runs.** Mutation kills were run only for #134's six new arms. All other arms were checked for planting only.
- **Hosted.** `suites` was in progress at the snapshot. Hosted and act acceptance belong to the manager.
- **Physical.** Calibration was NOT RUN; no hardware or bench was used. Field skips are not hardware proof.
- **Shared scratch directory.** The structural probe regenerated the `pp_top` ROM images in the same scratch export while the `pp_top` suite ran there. The generators are deterministic, and the suite passed.
- **Clone hygiene.** An analysis-tool version call run with the clone as working directory wrote an untracked 79-byte `xvlog.pb`. I removed it, and the script now runs that call in its scratch work directory. Final check (`receipts/99-clone-integrity.txt`):
  - HEAD, tree and index all equal the exact head;
  - all 562 tracked entries re-hashed, with 0 blob or mode mismatches;
  - `ls-tree` and the index are identical;
  - status is empty, including ignored files;
  - the repository declares no submodule gitlinks and has no `.gitmodules`.

## 7. Pending manager duties

1. Accept the hosted `suites` jobs at `d52bd7f2` (runs 37423565146 and 37423558584) once they complete.
2. Publish or link the manager's own static/builder/native bank receipts for `d52bd7f2`. I could not locate them publicly (§6).
3. Build and validate the merge-turn current-dev candidate (source base `e6a759de`, live dev `423ac5d9`). The 22 patch still applies to live dev's budget (E15).
4. At the next pin adoption, apply `parent-adoption-148-6c22d3ca.patch` and then `parent-adoption-22-28f9666f.patch`. Record the `Synth 8-6901` count and close #22 on it.
5. Merge requires two independent positive reviews and the full completion bar.
6. Optionally, carry the retained S1/S2 to follow-up issues.

## 8. Reproduction

Scripts are in `scripts/`. Paths in the receipts are redacted to `$PACKET`, `$CLONE`, `$SIM_ROOT`, `$PINNED_SIM`, `$VENDOR_ROOT` and `$HOME`.

- `plant_all.py <export> <out.json>`: the patch, exact-text and label census.
- `xvlog_table.py <repo> <commit> <export> <out.json> [--define SYNTHESIS]`: set `XVLOG` to the analysis binary.
- `yosys_stat.sh <export> <top> <out.json>`
- `run_campaigns.sh <packet>`: expects `scratch/exp-head` (a `git archive` of the head), `scratch/clone-head` (a clone checked out at the head) and `scratch/bin/verilator`.

`MANIFEST.sha256` lists every publishable file. `scratch/` is never published.

R504-2 FINISHED
