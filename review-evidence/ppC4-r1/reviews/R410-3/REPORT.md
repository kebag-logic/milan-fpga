[R410] POSITIVE - exact head 4e558491c608dc88efc7963a77cb6b49bce2a46e

# R410-3: independent internal review of PR #137 (lane C4, ACMP), round 3 (the merge of main)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #45 / PR #137
- **Exact head:** `4e558491c608dc88efc7963a77cb6b49bce2a46e`, tree `2cd2648917cdcf1ee850172ab08c6d92cbd23b6b`.
  Verified in the review clone (receipt `receipts/40-clone-integrity.txt`).
- **Round-3 scope** (#45 comment 5921008462, merge only). Two commits on the round-2 head `616cbdf1`, which R410-2 found POSITIVE:
  - `5609f8f`: the merge of processor `main` `d5f73bac` (PR #136 C3 ADP and PR #135 C2 MAAP), with parents `616cbdf1` and `d5f73bac`;
  - `4e55849`: the maap_version validator arm's record restated at the merged head.
- **Method:** I reconstructed the scope from the issue, its manager rulings, the PR body and the author round-3 packet (`review-evidence/ppC4-r1/author-r3` at milan-fpga `7612cc78`). I then made my own pass over `git diff d5f73bac..4e558491` and the history, and ran my own executable checks and probes.
- **Ordering:** my own verdict and ledger were written and hashed before I read any prior review report (`receipts/50-own-verdict-before-prior-findings.md`). I read the prior findings only after that.
- **Process limits:** no private author material, lane scratchpad or other reviewer's packet was read. No GitHub write, source edit, commit or push was made.

## Verdict

POSITIVE. The merge keeps both sides, and its composition is exactly this PR's reviewed content plus the stated renames. Every suite, entry point and mutation campaign I ran at this head passes, or is KILLED in full.

I have no finding at MINOR or above. Every prior finding is resolved, or retained by a public ruling or as a SUGGESTION (table below).

## Composition (the round-3 question)

Evidence: `receipts/10-composition.txt`, from `scripts/composition.sh`.

1. **Merge shape.** `5609f8f` has parents `616cbdf1` and `d5f73bac`, and the merge-base is the lane base `b2db3a97`. It is a merge commit, not a rebase.
2. **Changed paths.**
   - `git diff d5f73bac..4e558491` touches exactly the lane's 11 files plus `tb/maap/README.md`.
   - Nothing under `hdl/` changes, so the RTL at this head is main's.
3. **Replay check.** I replayed the lane diff `b2db3a97..616cbdf1` onto `d5f73bac` with `git apply -3`.
   - Seven lane files come out byte-equal to the head: 00, 09, the acmp_listener README and sim_main, acmp_nvm, and `pp_top_wrap.sv`.
   - `tb/pp_top/README.md`'s lane hunks are identical. The conflict was positional only: main's Section MP is kept, and Section AC follows it unchanged.
   - The hunk-level difference in the other files is exactly the stated resolution:
     - **`tb/pp_top/sim_main.cpp`:** the lane's per-flag guards are replaced by main's `one_section` form. `acmp_only` joins it, and `if (!one_section || acmp_only) run_acmp(h);` sits between D3 and AD. The full run order is suite, GI, NW, D3, AC, AD. MP runs only under `--maap-internal-only`, which is main's design.
     - **`tb/rx_validator/sim_main.cpp`:** the lane's section is renamed F29 to F30. Only the banner and three check labels change ("F30 BIND_RX cdl 84", "F30 PROBE_TX cdl 84", "F30 truncated reference"). It runs after main's F29.
     - **`tb/rx_validator/README.md`:** the tally is 555 (437 + 60 + 58). The V3 bullet cites F30. Main's M5 row is kept, and the lane's row becomes M6.
     - **`tb/pp_top/acmp_mutants.py:97`:** the two validator names become "F30 ...". That is the only edit.
4. **Independent models.** AC and AD each run on a separate model:
   - `AcmpPathPhase` owns `model2`/`h2` (`tb/pp_top/sim_main.cpp:8883-8888`);
   - `AdpConfigPhase` owns `model`/`io` and loads its own image (`:10554-10561`, boot at `:10600-10612`).
   So the AC-before-AD order cannot move AD's timeline.
5. **`4e55849`.** It changes only main's own M5 record (`tb/rx_validator/README.md:87`, `tb/maap/README.md:241`), from "47 FAIL of 497" to "of 555".
   - I re-measured it: the arm fails exactly 47 of 555, all F29a/F29b/F29c (16/15/16) and none in F30 (`receipts/maap_mutants/`).
   - This keeps main's record true at the merged head. It does not change behaviour or grading, so it is consistent with the "keep both sides" ruling.
6. **Stale names and counts.** No ACMP reference to "F29" remains anywhere in `tb/` or `docs/`. No stale 495/497/7931 count remains.
7. **Dated ADP record.** `tb/adp_engine/README.md:184` quotes a full-run denominator dated to PR #132 ("7,924 ... 4 in all").
   - Probe `probes/gate-probe*`: with that arm's patch applied at this head, `--acmp-only` stays 0 of 43 failing and `--adp-only` fails 3 of 55.
   - So adding section AC does not change the record's "4 in all". It is historical, and correctly qualified.

## Executable evidence (this reviewer, at the exact head)

**Tool.** Verilator 5.050.
- The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host.
- I used the sibling pinned wrapper `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator` instead, after checking its identity: `Verilator 5.050 2026-07-01 rev v5.050`, a wrapper script with sha256 `905795b9…` (`receipts/00-tool-identity.txt`).

**Environment.** Every command ran in the foreground, pinned to 8 CPUs (`taskset -c 0-7`). The drivers' temporary copies went to scratch. Everything ran in a disposable clone of the head.

| Check | Result |
|---|---|
| `make -C tb/rx_validator` | rc 0, 555 checks: 555 PASS |
| `make -C tb/acmp_listener` | rc 0, 2988 PASS |
| `make -C tb/acmp_nvm` | rc 0, 360 PASS |
| `make -C tb/maap` | rc 0, 196 PASS |
| `make -C tb/adp_engine` | rc 0, 1367 PASS |
| `make -C tb/pp_top` (both builds) | rc 0, 7992 PASS (default 7972: GI 5568, NW 85, D3 133, ACMP 43, AD 55, in that order; fixture 20) |
| `Vpp_top_sim` `--acmp-only` / `--adp-only` / `--maap-internal-only` / `--gsi-internal-only` / `--name-writes-only` / `--d3-only` | all rc 0: 43 / 55 / 34 / 6182 / 85 / 133 checks, 0 failures, each section alone |
| `acmp_mutants.py` (in 3 groups, `--jobs 8`) | 19 of 19 KILLED, every golden PASS. Every failing count equals the recorded table, e.g. `cdl_not_44_rejected` 27 of 555 (F30 x16, F4 x11) and 19 of 43 (`receipts/20-acmp-mutant-counts.txt`) |
| `make -C tb/maap mutants` | rc 0, 32 of 32: controls maap 196, pp_top MP 34 and rx_validator 555 PASS; 29 arms KILLED |
| `make -C tb/adp_engine mutants` | rc 0, 32 of 32 (2 controls PASS, 30 arms KILLED) |
| `d3_mutants.py` (all 83, in 6 groups) | 83 of 83 KILLED, goldens PASS. The validator control fails 4 (F28) |
| `./scripts/lint_hdl.sh` | rc 0 |
| `make check` | rc 0 |
| `gen_matrix.py --check` | rc 0 |
| `check_upc_map.py` | rc 0 |
| `git diff --check` (`d5f73bac..head`, `b2db3a97..head`) | rc 0 |

**Probe `probes/reanchor-probe*`** (`scripts/probe_reanchor.sh`). In a disposable clone, I reverted only the driver's two validator names to the pre-merge "F29 ...".
- `cdl_not_44_rejected@rx_validator` then reads SURVIVED, with both names missing.
- At the head it is KILLED.
- So the re-anchor is necessary and correct. The planted defect itself still applies once (no REFUSED anywhere).

**Harness note.** My first entry-point pass launched the binary from the repository root rather than from `tb/pp_top`. Its ROM images and tally file are cwd-relative, so every run failed with a harness error ("tally cannot be recorded"). I discarded those logs (they are not receipts), fixed the script, and the rerun from `tb/pp_top` is the result above. It is not a product defect.

**Hosted checks at the head** (`receipts/60-hosted-check-runs.txt`), read only:
- run 36806941848: `suites`, `portability` and `docs-gates` all completed **success**;
- run 36806939869: `docs-gates` and `portability` success, `suites` **still in progress** when read.

Hosted and act acceptance are the manager's.

## Findings

None at BLOCKER, MAJOR or MINOR. No new SUGGESTION.

## Prior public review findings at this head

| Finding | Severity | State at `4e558491` | Evidence |
|---|---|---|---|
| R410-1 F-1: the F00.2 GAP-15 cell | MINOR | **Resolved** (`9151e8b`), unchanged by the merge | `docs/00_MILAN_COMPLIANCE_REVIEW.md:509` reads "none found"; the 00 file is byte-equal to the replay |
| R410-1 S-1: AS6 GET_RX_STATE wait | SUGGESTION | **Resolved** (`06a84f5`), unchanged | `h2.q_acmp.empty()` checks at `tb/pp_top/sim_main.cpp:9149,9267`; the lane's sim_main hunks are identical apart from `main()` |
| R410-1 S-2 / R411-1 S1: IEEE editions | SUGGESTION | **Resolved** (`f55a25f`), unchanged | `09_verification.md:62`; `tb/acmp_nvm/sim_main.cpp:176,185` |
| R411-1 S2: the F00.2 snapshot reading | SUGGESTION | **Closed by ruling** (#45 5903960934) | — |
| R411-1 S3: bound identity survives A8 | SUGGESTION, pre-existing | **Retained by ruling** (manager residue checklist) | the clear on disarm is still at `hdl/top/protocol_processor_top.sv:1677`; no lane `hdl/` change |
| R411-1 S4: per-run timeout | SUGGESTION | **Retained by ruling** (#45 5906539259) | `acmp_mutants.py` differs from `616cbdf` only at `:97`; no timeout |
| R410-2 S-3 = R411-2 S1: a frame ahead of the UNBIND_RX_RESPONSE is not graded | SUGGESTION | **Retained** (round 3 is merge only; listed in the PR body's "What remains, round 3") | `wait_acmp(9, 0x4815, 400)` still at `tb/pp_top/sim_main.cpp:9295` |
| R410-2 S-4 = R411-2 S3: cdl-24 labelled "IEEE 2013 short form" | SUGGESTION, pre-existing | **Retained** (residue) | `tb/rx_validator/README.md:37`, `sim_main.cpp:465` |
| R411-2 S2: F00.2 caption dating | SUGGESTION | **Retained** (residue, manager decision) | `docs/00_MILAN_COMPLIANCE_REVIEW.md:513` |

None of the retained items is MINOR or above, so none of them affects the verdict.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #45 acceptance and rulings 5903960934 / 5906539259 / 5921008462; merge parents and base; replay of the lane on `d5f73bac`; the four conflict resolutions against both sides; `4e55849` against the "keep both sides" rule; PR body round-3 claims; prior findings | R410-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| RTL | CLEAN | `git diff d5f73bac..head -- hdl` empty; `lint_hdl.sh` rc 0; every driver anchor in the merged `hdl/` planted exactly once (no REFUSED in the ACMP or D3 drivers); the MAAP and ADP patches apply | R410-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Robustness | CLEAN | `main()` selector: each of 6 flags runs its section alone and the full run runs all; AC and AD on separate models; probe: the ADP gate defect does not reach AC; MAAP prefix `F29` no longer collides with ACMP checks | R410-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Tests | CLEAN | 6 suites, 6 entry points, `acmp_mutants` 19/19 with counts, MAAP 32/32, ADP 32/32, D3 83/83, all at Verilator 5.050; re-anchor probe | R410-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |
| Docs | CLEAN | `tb/rx_validator/README.md` (tally, V3, M5, M6); `tb/maap/README.md:241`; `tb/pp_top/README.md` MP and AC sections and driver text; `tb/adp_engine/README.md:184` (dated, still true); no stale F29 or count references; `make check` and `gen_matrix --check` rc 0; PR body Round 3 section | R410-3 | 4e558491c608dc88efc7963a77cb6b49bce2a46e |

## Real limits

- **Tool substitution.** The assigned 5.050 wrapper path was absent. I used a sibling pinned 5.050 wrapper and recorded its identity, but did not compare its binary with the absent one. I made no 5.052 rerun at this head.
- **Banks not run, as the brief requires.**
  - I did not run `./scripts/run_suites.sh` (all 33 suites), `syn/yosys`, the gPTP banks, or the parent, builder or act banks.
  - The suites outside the six above, the srp_top, retry, admission and desc_mem_guard campaigns, and the nvm_port figures were not rerun. Their inputs (`hdl/`, `tb/common`, their own `tb/` directories) are byte-identical to main `d5f73bac` (`receipts/10-composition.txt`: no path outside the lane's files changes).
- **No standards text.** I did not re-check the IEEE or Milan text; the clause citations are unchanged since round 2.
- **Hosted checks.** One hosted `suites` context was still in progress when read.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance at this head, including the in-progress `suites` context of run 36806939869.
- The donor bank, and the parent consumer bank at milan-fpga dev `e4b771f9` with this PR's `acmp_mutants.py` disposition line (`author-r3/parent-c4-disposition.patch`).
- The final current-dev candidate at the merge turn (source base `d5f73bac`, live dev `e4b771f9`). It is distinct from this source validation.
- The residue checklist: R411-1 S3, R411-1 S4, R410-2 S-3 = R411-2 S1, R410-2 S-4 = R411-2 S3, R411-2 S2, 03 V3's edition label, and the `KL_acmp_talker.sv` and 05 §3 "Table 8-3" citations.
- Publication of this packet. Only `REPORT.md` and the files in `MANIFEST.sha256` are publishable; `scratch/` is not.

R410-3 FINISHED
