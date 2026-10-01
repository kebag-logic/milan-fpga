[R411] POSITIVE - exact head 4e558491c608dc88efc7963a77cb6b49bce2a46e

# R411-3: external independent review of processor PR #137 (lane C4, ACMP; closes #45, #47, #48), round 3 (merge only)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
- Head `4e558491c608dc88efc7963a77cb6b49bce2a46e`, tree `2cd2648917cdcf1ee850172ab08c6d92cbd23b6b`.
- The round covers two commits on the round-2 head `616cbdf1`, which R411-2 reviewed POSITIVE:
  - `5609f8f`: the merge of processor `main` `d5f73bac` (PR #136, C3 ADP, and PR #135, C2 MAAP);
  - `4e55849`: a MAAP record restated at the merged head.
- Assignment: #45 comment 5921008462 (merge only). Review start: PR #137 comment 5923645913.
- Merge base of the lane and `main`: `b2db3a970cedbbff2f8ba813acb96122c442bc58`.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head, and every lens is CLEAN.

The merge keeps both sides. `git diff d5f73bac..4e558491` is this PR's own reviewed content, with only these differences:

- the allowed renames F29 → F30 and M5 → M6;
- the run-selector composition in `tb/pp_top/sim_main.cpp`;
- the tally and record denominators.

Every suite, entry point and mutation campaign I ran at the merged head passes, or is KILLED, in full. This review adds one SUGGESTION, S1. Every prior finding is either resolved or retained, as the table below shows.

I wrote my verdict and ledger (receipt `receipts/60-independent-ledger-before-prior-findings.md`) before I read any prior review report.

## Reconstruction (order followed)

1. **Contributor rules.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`, so I read the repository `README.md` (building and checking commands, the submodule pin rule) and `docs/README.md` (ID registries, single-source rules, and the `make check` workflow).
2. **Issue #45.**
   - The body: REQ-ACMP-001, Milan v1.2 §5.5.2.2, frozen acceptance items 1-3, and the GAP-15 residue.
   - The manager comments: the lane assignment 5891906554, round 2 5903960934, the STOP ruling 5906539259 and round 3 5921008462.
   - The author's TAKEN and REVIEW READY markers.
3. **PR #137.**
   - The body at this head, including the Round 3 note.
   - The manager's bank comments 5903837095 and 5911579824, and the review starts.
4. **Requirements and interfaces.**
   - 03 V3, and 09 F09.4's tolerance row (`docs/architecture/09_verification.md:62`).
   - 00 F00.2's GAP-15 cell (`docs/00_MILAN_COMPLIANCE_REVIEW.md:509`) and its caption (`:513`).
   - The interfaces the merged files touch: `tb/pp_top/pp_top_wrap.sv`, and the selectors of `tb/pp_top/sim_main.cpp`, `tb/pp_top/Makefile`, `tb/maap/mutants.py` and `tb/adp_engine/mutants.py`.
5. **Diff and history.**
   - `git log --graph` over the merge.
   - `git merge-tree --write-tree 616cbdf d5f73bac`, recomputed independently.
   - `git diff 50ac74c..5609f8f`, which is the resolution against the conflicted auto-merge.
   - `git diff 5609f8f..4e55849`.
   - `git diff d5f73bac..4e558491`, compared line by line against `git diff b2db3a97..616cbdf`.
6. **Public evidence.** `kebag-logic/milan-fpga@7612cc78:review-evidence/ppC4-r1`:
   - its `MANIFEST.json`;
   - `author-r3/HANDOFF.md`, `PR-BODY.md` and `parent-c4-disposition.patch`. Each file's sha256 equals its manifest `published_sha256`, and `PR-BODY.md` equals the live PR body apart from trailing newlines (receipt 51).
   - The hosted check runs at the exact head.

After that, I read the prior public review findings (R410-1, R411-1, R410-2 and R411-2).

## The composition, judged

| Claim (assignment / PR body) | Result | Evidence |
|---|---|---|
| Exactly four files conflict | **Holds.** `git merge-tree` reports conflicts in `tb/pp_top/README.md`, `tb/pp_top/sim_main.cpp`, `tb/rx_validator/README.md` and `tb/rx_validator/sim_main.cpp`, and nothing else. `docs/00`, `docs/09` and `tb/pp_top/pp_top_wrap.sv` auto-merge, and their blobs at `5609f8f` equal the auto-merge result | receipt 01, `git diff 50ac74c 5609f8f` |
| Both sides kept in each conflicted file | **Holds.** See the four rows below | `git diff 50ac74c 5609f8f` |
| `tb/rx_validator/sim_main.cpp` | Main's F29 (maap_version 2, 0 and 31, `:756`) is byte-identical to main's. The lane's section is F30 (`:785-830`). Its banner and three check labels are the only edits (`:785`, `:799-800`, `:804`). It is declared after F29 (`:330-331`) and runs after F29 (`:859-860`) | receipt 01: identical after the rename map |
| `tb/rx_validator/README.md` | The tally line reads 555 (`:5`), and 555 is measured. The V3 bullet cites F30 (`:40`). Main's M5 (`:87`) is kept, and the lane's row is M6 (`:88`) | receipt 10 (555 PASS) |
| `tb/pp_top/sim_main.cpp` | `--acmp-only` (`:10898`) joins main's `one_section` (`:10905`). The full run order is the suite, GI, NW, D3, AC, then AD (`:10907-10912`); the lane's own gating expressions are replaced by main's equivalent idiom. MP runs only under its selector, as on `main` | receipt 11: `ACMP: 43`, then `AD: 55`, total 7992. Receipt 12: `--acmp-only` 43, `--adp-only` 55, `--maap-internal-only` 34 and `--name-writes-only` 85, each section alone |
| `tb/pp_top/README.md` | Main's Section MP is kept (`:1169`). The lane's Section AC follows it unchanged (`:1193`) | receipt 01: identical |
| `git diff d5f73bac..4e558491` = this PR's content plus the renames | **Holds.** Twelve files. Nine are line-identical to the lane's delta, two of them (`acmp_mutants.py`, `tb/rx_validator/sim_main.cpp`) after the rename map. The remaining three differ only by the selector composition (`tb/pp_top/sim_main.cpp`), the tally line 495 → 555 and main's kept M5 row (`tb/rx_validator/README.md`), and the MAAP record restatement (`tb/maap/README.md`) | receipt 01 (`scripts/compose_check.py`) |
| Re-anchored `acmp_mutants.py` | **Holds, and the edit is needed.** Its only edit is `:97`, where the names become "F30 …". A probe that restores the pre-rename "F29 …" names makes `cdl_not_44_rejected@rx_validator` SURVIVE with both names missing (driver rc 1). So the driver refuses a stale anchor, and the re-anchor is what keeps the arm KILLED | receipt 30 |
| The MAAP campaign's `F29` prefix (`tb/maap/mutants.py:28`) | **Holds.** Under `validator-maap-version-1-only` the validator fails 47 checks of 555, and all 47 carry the prefix F29a/b/c: named=47. None is an F30 check | receipt 21 |
| `4e55849` restates "47 FAIL of 497" as "of 555" (`tb/rx_validator/README.md:87`, `tb/maap/README.md:241`) | **Correct.** 47 of 555 is measured. A record of main's that this merge invalidated is restated to the measured value, which the assignment covers ("keep the README rows consistent") | receipt 21 |
| `hdl/` | `git diff d5f73bac..4e558491 -- hdl` is empty, and so is `b2db3a97..616cbdf -- hdl` | receipt 43 |

## Execution at the merged head

The tool is Verilator 5.050 (receipt 00). Every build ran in a disposable `git archive` export whose tree id equals the head's `2cd26489`. Verilator's build make was capped at 8 jobs, or 4 copies at `-j 2` for D3. Every job ran in the foreground.

| Command | rc | Result |
|---|---:|---|
| `make` in `tb/rx_validator` | 0 | 555 checks, 0 FAIL |
| `make` in `tb/acmp_listener` | 0 | 2988 checks, 0 FAIL |
| `make` in `tb/acmp_nvm` | 0 | 360 checks, 0 FAIL |
| `make run` in `tb/pp_top`, both builds | 0 | 7992 checks, 0 FAIL: default 7972, fixture 20; AC 43, AD 55, D3 133, NW 85 |
| `Vpp_top_sim` with `--acmp-only`, `--adp-only`, `--maap-internal-only`, `--name-writes-only` | 0 each | 43, 55, 34 and 85 checks: one section each |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | 19 of 19 KILLED, 3 goldens PASS. Every failing count equals the PR's table: 93/2988, 1/43, 50/2984, 40/2984, 30/2984, 27/555, 19/43, 7×4, 6, 1, 2, 2, 2, 1, 5, 5 (receipt 20) |
| `make -C tb/maap mutants` | 0 | 32 of 32: controls maap 196, pp_top MP 34, rx_validator 555; 29 arms KILLED |
| `make -C tb/adp_engine mutants` | 0 | 32 of 32: 2 controls PASS, 30 arms KILLED |
| `python3 tb/pp_top/d3_mutants.py`, in 8 `--only` slices | 0 each | 83 of 83 KILLED, goldens PASS in every slice. The validator control `validator_admits_held_aecp` fails 4 (M4) |
| `python3 tb/pp_top/name_wr_mutant.py` | 0 | decode killed; golden and restored PASS |
| `./scripts/lint_hdl.sh` | 0 | LINT OK |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `make check` | 0 | 41 mermaid + 18 wavedrom, links 981, 115 REQ / 17 GAP, params 26 |
| `git diff --check` over `b2db3a97..`, `616cbdf..` and `d5f73bac..4e558491` | 0 | clean |

**Hosted checks at the exact head** (receipt 50):

- The `pull_request` run 36806941848 executed `suites`, `portability` and `docs-gates`, and all three succeeded.
- The `suites` job ran these steps: lint, every suite, the SRP, MAAP and ADP campaigns, the matrix, and the nvm_port figures.
- Its Verilator build step was skipped only because the pinned build was cached. That is a skipped context, not a skipped gate.
- The `push` run 36806939869 had `portability` and `docs-gates` successful, and `suites` still in progress when this report was written.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1: SUGGESTION. Lenses: Tests, Docs. Section AC has no single-section `make` target beside main's

- **Where:**
  - `tb/pp_top/Makefile:69-73`: main adds `maap-internal` and `adp-config`, which each run one section after `gsi-build`.
  - `tb/pp_top/README.md:1197-1198` tells the reader to run `./obj_dir/Vpp_top_sim --acmp-only` "after `make gsi-build`". The section has no make target.
- **Evidence:** after the merge, `tb/pp_top` has five single-section selectors. MP and AD each have a make target and NW and GI have theirs (`name-writes`, `gsi-internal`), while D3 and AC have none. `acmp_mutants.py` calls the binary directly, so nothing is broken (receipt 12).
- **Impact:** convention only. A reader of the merged README finds two ways to run one section, and grading is unaffected.
- **Suggested outcome:** at a later touch of `tb/pp_top`, add an `acmp` target (`gsi-build`, then `--acmp-only`) and cite it in Section AC. Round 3 is merge only, so this goes to the manager's residue checklist rather than into this PR.
- **Verification:** `make -C tb/pp_top acmp` runs the 43 AC checks alone, rc 0.

## Prior findings at this head

Each item was re-checked at `4e558491` (receipt 61).

| Finding | Severity | State at this head | Basis |
|---|---|---|---|
| R410-1 F-1: the F00.2 GAP-15 cell | MINOR | **Resolved** (round 2), unchanged by the merge | `docs/00_MILAN_COMPLIANCE_REVIEW.md:509` reads "none found", and the merged docs delta equals the lane's |
| R410-1 S-1: AS6 quiet window | SUGGESTION | **Resolved** (round 2) | `q_acmp` emptiness checks in AS6 (`tb/pp_top/sim_main.cpp:9267`, `:9319`, `:9330`); AC 43/43 |
| R410-1 S-2 = R411-1 S1: the IEEE 1722.1 editions | SUGGESTION | **Resolved** (round 2) | `docs/architecture/09_verification.md:62`; `tb/acmp_nvm/sim_main.cpp:176,185` |
| R411-1 S2: the GAP-15 snapshot reading | SUGGESTION | **Resolved** by the manager's F-1 ruling (5903960934) | as F-1 |
| R411-1 S3: the bound stream identity survives an A8 teardown | SUGGESTION | **Retained**, pre-existing port-visible RTL on the manager's residue checklist | `hdl/` is unchanged by the lane and the merge |
| R411-1 S4: no per-run timeout in `acmp_mutants.py` | SUGGESTION | **Retained** by the STOP ruling (5906539259) | the driver differs from `616cbdf` only at `:97`, and has no timeout |
| R410-2 S-3 = R411-2 S1: AS6 does not grade a frame sent ahead of the UNBIND_RX_RESPONSE | SUGGESTION | **Retained.** Round 3 is merge only; it is listed for the residue checklist in the PR body | `wait_acmp(9, 0x4815, 400)` is unchanged at `tb/pp_top/sim_main.cpp:9295` |
| R410-2 S-4 = R411-2 S3: F4's cdl-24 frame labelled "IEEE 2013 short form" | SUGGESTION | **Retained**, as above | `tb/rx_validator/README.md:37`, `tb/rx_validator/sim_main.cpp:465` |
| R411-2 S2: the F00.2 caption dates the whole residue column | SUGGESTION | **Retained**, as above | `docs/00_MILAN_COMPLIANCE_REVIEW.md:513` unchanged |

## Lens analysis

- **Conformance.** Issue #45's frozen acceptance holds at the merged head:
  1. `tb/rx_validator` F30 drives the 96-byte cdl-84 form as a BIND_RX and as a PROBE_TX. Each is committed, its header beat is field-exact, the slot holds 96 bytes, and there is no rx_length count.
  2. `tb/pp_top` AL1-AL4 pass inside AC 43/43.
  3. The cdl != 44 mutation fails 27 of 555 validator checks and 19 of 43 in AC, and is recorded as M6.
  - The clause text in F30's banner (Milan v1.2 §5.5.2.2; IEEE 1722.1-2021 §8.2.1.6, cdl 84) is the lane's, unchanged.
  - Main's F29 keeps its IEEE 1722-2016 B.2.3 citations.
  - The GAP-15 and F09.4 edits survive the auto-merge beside main's REQ-MAAP-007 edit.
- **RTL.**
  - No file under `hdl/` differs from `main` `d5f73bac`, so the RTL at this head is main's.
  - The wrap's auto-merge adds the lane's four `acmp_bound_*` ports and main's `dbg_adp_cfg_v_o`. These are independent ports and connections at different places.
  - Both builds of `tb/pp_top` elaborate and pass, and `lint_hdl.sh` is rc 0.
- **Robustness.**
  - Each single-section selector runs exactly one section, and the full run runs every section once.
  - AC and AD each build their own model, so neither shifts the other's timeline: AD passes 55 both alone and after AC.
  - The mutation driver refuses a stale check name instead of reporting a false KILLED (receipt 30).
  - The MAAP campaign's `F29` prefix can no longer match an ACMP check.
- **Tests.**
  - The touched suites are at their recorded totals: 555, 2988, 360 and 7992.
  - Every campaign the merge can affect passes or is KILLED in full at the merged head: acmp 19/19, MAAP 32/32, ADP 32/32, D3 83/83 and name-write.
  - The campaigns whose inputs are byte-identical to `main` were covered by the hosted `suites` job at the exact head: the SRP LeaveAll campaign, the suites sweep and the nvm_port figures.
- **Docs.**
  - The merged READMEs are consistent: F30/M6 and F29/M5, the 555 tally, and the MAAP record restated.
  - No reference to the ACMP validator section still says F29 (a grep at the head).
  - `make check` and `gen_matrix --check` are rc 0.
  - The PR body's Round 3 note matches the tree. S1 is a convention suggestion.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #45 acceptance 1-3 against `tb/rx_validator/sim_main.cpp:785-830` (F30), `tb/pp_top` AL1-AL4 in section AC, M6 at `tb/rx_validator/README.md:88`, `docs/00…:509`, `docs/architecture/09…:62`; receipts 10, 11, 20 | R411-3 (round-3 delta; whole-PR conformance carried from R411-1/R411-2 and re-checked for the merge) | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| RTL | CLEAN | `git diff d5f73bac..4e558491 -- hdl` (empty), `tb/pp_top/pp_top_wrap.sv` auto-merge, `lint_hdl.sh`; receipts 40, 43 | R411-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Robustness | CLEAN | `tb/pp_top/sim_main.cpp:10898-10912` selector composition, `tb/pp_top/acmp_mutants.py:97` re-anchor, `tb/maap/mutants.py:28` prefix; re-anchor probe; receipts 12, 21, 30 | R411-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Tests | CLEAN | four touched suites; acmp, MAAP, ADP, D3 and name-write campaigns; hosted `pull_request` run 36806941848; receipts 10-12, 20-24, 50 | R411-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Docs | CLEAN (S1 is a suggestion) | `tb/rx_validator/README.md`, `tb/pp_top/README.md` (MP/AC), `tb/maap/README.md:241`, PR body Round 3 note, `make check`; receipts 01, 42, 51 | R411-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |

## Real limits

- **The Verilator I used is not at the assigned path.** The assigned scoped Verilator path does not exist on this host.
  - I used a launcher with byte-identical content (sha256 `905795b9…`, the same as every pinned launcher on the host). It resolves to Verilator 5.050 rev v5.050.
  - Its `verilator` script hash `fb2cc573…` equals the author's record.
  - Its `verilator_bin` hash (`44898b22…`) differs from the author's recorded `51910d8d…`. It is the same release in a different binary build.
- **What I did not run.**
  - The full `run_suites.sh` sweep (a processor bank).
  - `make -C tb/srp_top mutants`, `tb/acmp_talker/retry_mutants.py`, `tb/srp_admission/mutants.py`, `tb/desc_mem_guard/mutate.py`, `make -C tb/nvm_port figures` and `syn/yosys/run.sh`. Their inputs (`hdl/`, `tb/common`, `tb/srp_top`, `scripts/`, `syn/` and the CI workflow) are byte-identical to `main` `d5f73bac`. The hosted `suites` job executed the sweep, the SRP, MAAP and ADP campaigns and the nvm_port figures at the exact head.
  - `tb/pp_top/gsi_mutants.py`, which runs about 13 minutes serially with no subset option and does not fit this session's foreground limit. Its section GI passes in the full run (receipt 11), and the merge did not touch it.
- **Parent consumer bank and donor bank.** These were not run, by instruction. They are the manager's, at dev `e4b771f9`, with this PR's `acmp_mutants.py` disposition line. The disposition patch I fetched equals the published one.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager bank evidence.** I found no manager bank comment for `4e558491` on #45 or #137 when this review was written. The public evidence directory holds the author's round-3 packet.

## Pending manager duties

- Run the donor bank and the parent consumer bank at milan-fpga dev `e4b771f9`, with the gitlink at this head and the `acmp_mutants.py` disposition line.
- Confirm the hosted `push` run 36806939869 `suites` job completes successfully at this head.
- Build the final current-dev candidate at the merge turn: source base `d5f73bac`, live dev `e4b771f9`.
- Carry these retained items on the residue checklist:
  - R411-1 S3 and S4;
  - R410-2 S-3 and S-4;
  - R411-2 S2;
  - this review's S1.
- Merge requires a second independent positive review at this head.

## Clone integrity

- The review clone is at HEAD `4e558491`, and both its tree and its index tree are `2cd26489`.
- The worktree and index equal HEAD. There are 374 regular blobs (mode 100644) and 13 executables (mode 100755), and no gitlinks, because none is required at this head.
- One ignored `__pycache__`, created when I imported the D3 driver's table, was removed.
- One dangling tree object remains from my `git merge-tree` recompute. It changes no tracked blob, mode, index entry or ref.
- No file in the clone was edited (receipt 70).

R411-3 FINISHED
