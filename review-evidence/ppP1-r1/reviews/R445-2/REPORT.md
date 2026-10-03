[R445] POSITIVE - exact head 5960d8fc7e4f6ef2d7551bb224154ef2c265d894

# R445-2 external independent review: processor issue #83 / PR #150 (lane P1), round 2

- Exact head `5960d8fc7e4f6ef2d7551bb224154ef2c265d894`, tree
  `99a6b049c9e2759799dd86daf26ba66ef466463e`. Source base
  `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`; round-1 reviewed head `c066dd83a2004f9b3640a933860c4d9e677d017e`.
- Round-2 scope (assignment #83 comment 5969765075): docs and comments only, answering R444-1
  (PR #150 comment 5969549669) and R445-1 (5969760336). Delta `c066dd83..5960d8fc`: two
  commits (`219cd67`, `5960d8f`), **7 hunks in 5 files** (3 HDL files comment-only, 2 suite
  READMEs), +25/-15 lines.
- Verdict basis: every round-1 finding (R445-1 F1 to F3, R444-1 F1 to F3) and every round-1
  residue item is **resolved** at this head. No BLOCKER, MAJOR or MINOR is open. Two new
  RESIDUE items (stale line citations, one in a suite README and one in the PR body's
  own note about it) carry exact fixes and do not block. The five round-1 suggestions stay
  open by assignment and are not findings. Hosted CI at the exact head is green: both `hdl` workflow runs (push 37128429648 and pull_request 37128432590), six jobs, all `success`.

## 1. Reconstruction order and sources

1. **Repository guidance.** The tree has no `AGENTS.md` or `CONTRIBUTING.md`; `README.md` and
   `docs/README.md` (conventions, `make check`) were used.
2. **Scope.** Issue #83 body (acceptance 1 to 4) and every comment in order: lane assignment
   5965788915; STOP 5967588719; **ruling 5967611704 (maps are the integrator's)**; REVIEW READY
   5968343520; round 1b 5968352676; STOP 5969239148; **ruling 5969246536 (gate 16: (b),
   milan-fpga #643)**; **round-2 assignment 5969765075**; correction 5969802215; REVIEW READY
   (round 2) 5969914780. PR #150 body as live at review time (`receipts/pr150-body.md`).
3. **Authorities.** `docs/architecture/07_memory_maps.md` §3.4 (:442-463) and §5.1
   (:552-602, "Who persists what": save from the phase-5 commit beat, restore after
   `restore_done_o` judged against the restored formats, roll-back limited to the two AECP
   stores, "the processor writes and restores no map record"). 09 `:56` (randomized cuts),
   `tb/pp_top/README.md:381-400` (D3KR).
4. **Diff and history.** `c066dd83..5960d8fc` hunk by hunk (`receipts/round2-delta.diff`), with
   the authoring context in `ddb3119d..5960d8fc`.
5. **Public evidence.** milan-fpga `3a657083` `review-evidence/ppP1-r1` (round-1 author packet;
   every file's sha256 equals its manifest `published_sha256`, `receipts/evidence/`). It holds
   no round-2 HANDOFF and no manager bank receipts (section 7).
6. **Prior public reviews.** R444-1 and R445-1 were read only after my own pass over the
   delta was written down (`receipts/independent-pass-before-prior-reviews.txt`, timestamped).

## 2. What I executed (all at the exact head unless stated)

| # | Probe | Result | Receipt |
|---:|---|---|---|
| 1 | Pinned simulator identity | Verilator 5.050 2026-07-01 rev v5.050 (the scoped wrapper) | `logs/`, this report |
| 2 | Every changed HDL line of the round-2 delta | **28 changed lines, all `//` comment lines** (non-comment filter finds 0) | `receipts/round2-delta.diff` |
| 3 | `probe_comment_identity.sh`: comment-free token stream (`verilator -E -P`, whitespace-normalised) of the three changed HDL files, base `c066dd83` vs head | **IDENTICAL** | `receipts/probe_comment_identity.out` |
| 4 | Same script: elaborated `protocol_processor_top` (Verilator `--json-only`, 74,685 typed nodes, locations stripped; the 92 source-line numbers Verilator bakes into its own `unique case` assertion text normalised, since a comment that adds a line shifts them) | **IDENTICAL** netlist | same |
| 5 | Same script: control, one constant changed on a code line of the writer (`:577`, `1'b1`→`1'b0`) | **CAUGHT** by both the token and the netlist comparison | same |
| 6 | Same script: every ROM regenerated from its generator at base and head (microcode, listener ROM, both descriptor images and maps) | **byte-identical**; `tb/pp_top`'s own built `ucode.hex`/`ltn_rom.hex` carry the same sha256 | same, `receipts/pp_top_built_roms.sha256` |
| 7 | Stale-claim grep (`map stage`, `later stage`, `reset EMPTY`, `map record`, maps near `not implemented`/`later`/`owed`) over the tree | no claim of a processor map stage: the 9 hits are the amended rule itself (00:264, 02:683, 06:854, 07:462/:564/:708, engine `:470`, top `:782`) or unrelated (`ucpu_pkg.sv:124`); the author's narrower grep finds only `gen_ucode.py:1545` (sampling-rate rule), confirmed | `receipts/grep-map-stage.txt` |
| 8 | No mutation driver, plant or patch anchors on the replaced text | grep over `tb/`, `scripts/`, `*.py`, `*.patch`: only hit is the README passage itself | (this report) |
| 9 | Tracked mutation patches, `git apply --check` | **224 of 224 apply** | `receipts/patch_apply_check.txt` |
| 10 | `./scripts/lint_hdl.sh` (pinned simulator first on PATH) | rc 0, 41 modules LINT OK | `logs/lint_hdl.*` |
| 11 | `make check`; `scripts/gen_matrix.py --check` | rc 0 (1,114 links; 115 REQ rows, 17 GAP findings; 94 matrix rows, 0 untested; parameters 28/28/28); rc 0 | `logs/make_check.*`, `logs/gen_matrix.*` |
| 12 | `make -C tb/pp_top run` (five builds; the suite of all three changed modules) | rc 0, **10,390 checks, 0 FAIL** (default 9,918; D3 319, D3V 11, D3KR 1,000) | `logs/pp_top_run.*` |
| 13 | `tb/pp_top` `--cut-seed 0xD3C0FFEE` (the README text's "`--cut-seed S` reruns one") | rc 0, 39 checks, one seed across all 8 record types | `logs/cut_seed_standing.*` |
| 14 | `make -C tb/nvm_port run` and `make -C tb/nvm_port figures` (the README whose text changed; the figures gate re-measures every figure it quotes) | rc 0, 1,219 checks; rc 0, "all measured figures agree with the tree" | `logs/nvm_port_*` |
| 15 | Hunk count of the published consumer patches | `parent-adoption-c8-bbf704ec.patch` and `-cdf49d1a.patch`: **11 `@@`, 7 `diff --git` each**; `+`/`-` lines identical | `receipts/evidence/` |
| 16 | Hosted CI at the exact head (read-only API) | Workflow `hdl`, runs 37128429648 (push, checks out the exact head) and 37128432590 (pull_request): docs-gates, portability and suites, **6 of 6 jobs `success`** (suites 14:05-16:09 UTC). Every step executed except `Build Verilator v5.050` in both suites jobs, skipped because the pinned build was restored from cache. Executed suites steps: lint + every suite, SRP, MAAP, ADP, AECP deadline/hazard and AECP dispatch campaigns, matrix no-drift, nvm_port figures | `receipts/ci-*.json`, `receipts/ci-*.txt` |
| 17 | Clone integrity after all probes and clean-up | HEAD and tree exact; index tree equal; porcelain (ignored included) empty; 501 index entries, every blob re-hashes to its index blob, every mode matches; **this repository has no gitlinks** | `receipts/clone_integrity.txt` |

Disposable copies (`git archive` extractions, the control plant) lived only under the
packet's `scratch/`. No tracked byte of the review clone was edited; build products were
removed with `git clean -fdX` (the clone had no ignored files before the run).

## 3. Round-1 findings and residue at this head

| Round-1 item | At this head | Evidence |
|---|---|---|
| **R445-1 F1 = R444-1 F3** (MINOR, Docs): c8-bbf704ec "13 hunks" | **RESOLVED** | Live PR body `:292-294` and `:330-333`: "keeps all 11 hunks (7 files), every `+`/`-` line identical to the `cdf49d1a` original" - equal to the artefact (probe 15). Correction posted on #83 (5969802215, its figures and grep commands verified); 5969239148 left as posted (still reads "All 13 hunks", as the no-edit rule requires). The round-2 HANDOFF is not in the public evidence, so its "11" could not be read (section 7) |
| **R445-1 F2 = R444-1 F1** (MINOR, Conformance/RTL/Docs): stale processor map-stage claims | **RESOLVED** | All five of R445-1's exact texts are in place verbatim: `protocol_processor_top.sv:779-782`, `KL_aecp_engine.sv:469-470`, `KL_aecp_nvm_writer.sv:94-101` (the reflowed rule paragraph) and `:119-121`, `tb/pp_top/README.md:665`; R444-1's four places are a subset. The new wording agrees with 07 §5.1 clause by clause (save from phase 5, restore after `restore_done_o` judged against the restored formats, no processor map record). Comment-only: probes 2 to 6. Grep: probe 7. Gates: probes 10 to 12 |
| **R445-1 F3 = R444-1 F2** (MINOR, Tests/Docs): nvm_port README "randomized half still owed" | **RESOLVED** | R445-1's exact parenthetical is appended at `tb/nvm_port/README.md:1064-1067` and `:1348-1351`. Each fact in it holds: D3KR covers every record type both producers write (all 8, `tb/pp_top/README.md:385-387`), 32 standing seeds each (`:390`, run 1,000/0), `rst_n` cut, `--cut-seed S` reruns one seed (probe 13), D3K/T15-T18/T25 fixed cuts unchanged. Read as written: owed port-locally, delivered at the top. The figures gate passes on the edited README (probe 14) |
| R445-1 R1 = R444-1 R1 (RESIDUE): gate 16 described as pending | **RESOLVED** | PR body `:236-238` carries R445-1's exact text plus "The PR does not wait for it." (R444-1's); the (a)/(b) list ends "Ruled (b) on #83 (5969246536)." (`:312`) |
| R445-1 R2 = R444-1 R2 (RESIDUE): area missing from parent-visible list | **RESOLVED** | PR body `:221-224`, item 12, R445-1's text plus R444-1's 8x8 diagnostic sentence |
| R445-1 R3 (RESIDUE): growth itemisation 1,192 of 1,194 | **RESOLVED** | PR body `:151-153` appends "HZ 176 to 177 and ST 18 to 19 (the name saves' drain checks HZ9 and ST1)"; 169+12+11+1,000+1+1 = 1,194 |
| R444-1 S1, S2; R445-1 S1, S2, S3 (SUGGESTION) | open by assignment, not findings | Listed in the PR body's Round 2 item 5 (`:366-379`) |

## 4. Findings at this head

No BLOCKER, MAJOR or MINOR.

### R1 - RESIDUE - Docs

- **Where.** `tb/nvm_port/README.md:100-101`: "`hdl/aecp/KL_aecp_nvm_writer.sv:482-485`" for
  `frame_ok_w`, and "instantiated at `hdl/top/protocol_processor_top.sv:2714`" for the binding
  shadow.
- **Evidence.** `frame_ok_w`'s declaration and assignment are at `:482-485` at `ddb3119d`,
  at `:546-549` from `53e1474` (the name stage) to `c066dd83`, and at **`:549-552`** at this
  head. The shadow's `KL_acmp_nvm_shadow #(` instance is at `:2727` at `ddb3119d` (already
  stale there) and at **`:2730`** at this head. The PR body records both as seen and not fixed.
- **Why RESIDUE.** Pure prose pointers: the sentences' claims (the D3 writer gates its
  records on `frame_ok_w`; the shadow is instantiated at the top) hold at this head and name
  their symbols; no figure, gate, test, code or clause claim moves (`make check` and the
  figures gate pass with the text as is).
- **Exact fix.** `` `hdl/aecp/KL_aecp_nvm_writer.sv:482-485` `` → `` `hdl/aecp/KL_aecp_nvm_writer.sv:549-552` ``;
  `` `hdl/top/protocol_processor_top.sv:2714` `` → `` `hdl/top/protocol_processor_top.sv:2730` ``.
- **Verification.** `grep -n 'logic frame_ok_w' hdl/aecp/KL_aecp_nvm_writer.sv` → 549;
  `grep -n 'KL_acmp_nvm_shadow #(' hdl/top/protocol_processor_top.sv` → 2730.

### R2 - RESIDUE - Docs (PR body)

- **Where.** PR #150 body, Round 2, "Seen, not fixed in this round" (`:395-398`):
  "`KL_aecp_nvm_writer.sv:482-485` (`frame_ok_w`, right at `ddb3119d`, at `:550-553` since
  the name stage)".
- **Evidence.** As R1: `:546-549` since the name stage (`53e1474`, `c066dd83`), `:549-552`
  at this head. `:550-553` was never the block's range.
- **Exact fix.** "at `:550-553` since the name stage" → "at `:546-549` since the name
  stage, `:549-552` at this head".
- **Verification.** `git show <rev>:hdl/aecp/KL_aecp_nvm_writer.sv | grep -n 'logic frame_ok_w'`
  for `53e1474`, `c066dd83`, `5960d8fc` → 546, 546, 549.

## 5. Lens evidence

- **Conformance.** The five banners now state the D3 contract as amended by ruling 5967611704
  and 07 §5.1; the port authority (top banner, `:779-782`) no longer promises a processor
  map stage. No acceptance line moves in round 2: the delta changes no logic (probes 2 to 6),
  so round 1's acceptance evidence (both round-1 reviews found code, tests and merge clean)
  carries to this head, and the issue #83 acceptance-3 statement in the nvm_port README now
  points at its delivering section. CLEAN.
- **RTL.** 28 changed HDL lines, all comments; comment-free token streams identical,
  elaborated top netlist identical, ROMs byte-identical, control caught; lint 41/41. CLEAN.
- **Robustness.** No behaviour change (as RTL). At this head the reset-cut evidence runs green:
  D3 319, D3V 11, D3KR 1,000, `--cut-seed` single-seed rerun. CLEAN.
- **Tests.** `tb/pp_top` 10,390/0 and `tb/nvm_port` 1,219/0 at the head; the nvm_port figures
  gate agrees with the edited README; 224/224 mutation patches apply and none anchors on the
  replaced text. The appended coverage statement is true (section 3). CLEAN.
- **Docs.** All five exact replacements and both appended passages verbatim; PR body hunk
  count, gate-16 status, item 12 and HZ/ST corrected; correction comment posted; open
  suggestions listed; `make check` rc 0 (1,114 links). Residue R1 and R2 recorded with exact
  fixes. CLEAN.

## 6. Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 5967611704, 07 §3.4/§5.1, the five banner/README replacements, stale-claim grep, issue #83 acceptance 3 vs nvm_port README | R445-2 | 5960d8fc7e4f6ef2d7551bb224154ef2c265d894 |
| RTL | CLEAN | `KL_aecp_engine.sv`, `KL_aecp_nvm_writer.sv`, `protocol_processor_top.sv` delta; token, netlist and ROM identity with control; lint 41 modules | R445-2 | 5960d8fc7e4f6ef2d7551bb224154ef2c265d894 |
| Robustness | CLEAN | No-logic-change proof; D3/D3V/D3KR runs; `--cut-seed` rerun | R445-2 | 5960d8fc7e4f6ef2d7551bb224154ef2c265d894 |
| Tests | CLEAN | `tb/pp_top` full run, `tb/nvm_port` run and figures gate, 224 patch applies, anchor grep, hosted suites job (push and pull_request) `success` | R445-2 | 5960d8fc7e4f6ef2d7551bb224154ef2c265d894 |
| Docs | CLEAN (RESIDUE R1, R2 to checklist) | Round-2 delta, `tb/nvm_port/README.md`, `tb/pp_top/README.md`, PR body (live), #83 comments 5969802215 and 5969914780, published c8 patches, `make check` | R445-2 | 5960d8fc7e4f6ef2d7551bb224154ef2c265d894 |

## 7. Real limits

- **Banks not re-run.** Not run here by mandate: `run_suites.sh` over all 33 suites, the
  mutation campaigns (d3, notify, ctr, aecp, dispatch, acmp, gsi, adp, maap, name-write), the
  parent consumer set, Yosys/OOC area. With no logic change proven (probes 2 to 6) their
  round-1 results carry, but their head-level figures are the author's and the manager's.
- **Manager bank receipts.** The manager's source static/builder and native bank receipts at
  this head were not in the public evidence tree at `3a657083` (round-1 author packet only),
  and no evidence comment at this head was found on #83 or PR #150. Not inspected.
- **Round-2 HANDOFF.** Not published; its "11 hunks" could not be read. The published
  round-1 HANDOFF (`3a657083`, `author/HANDOFF.md:745`) still reads "13", which is the frozen
  round-1 artefact.
- **Hosted CI.** Inspected read-only: all six jobs `success`, the only skipped step is the cached simulator build. The pull_request run tests GitHub's merge ref, not the bare head; the push run is the exact-head run. The manager owns hosted/act acceptance; no act run here.
- **Hardware.** Physical calibration NOT RUN; no hardware; field skips are not hardware proof.

## 8. Pending manager duties

- Carry RESIDUE R1 and R2 to the residue checklist.
- Publish the round-2 HANDOFF and the source static/builder and native bank receipts at this
  head.
- Hosted/act acceptance at this head (hosted: six jobs `success`, receipts `receipts/ci-*`).
- Build the final current-dev candidate at the merge turn (source base `ddb3119d`, live dev
  `bbf704ec`); consumer bank with `parent-adoption-c8-bbf704ec.patch` then
  `parent-adoption-p2-p1-1269cdaf.patch`, gate 16 recorded against milan-fpga #643.
- Hosted/act acceptance; merge requires two independent positive reviews and the full
  completion bar.

R445-2 FINISHED
