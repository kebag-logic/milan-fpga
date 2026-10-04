[R463] POSITIVE - exact head 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc

# R463-2: external independent review, processor PR #155 / milan-fpga #639, round 2

- **Head:** `1cba30c91bbc4c0e20343f883b94c3f701cc0dbc`, tree `c81e4a5e52e223e324813dad900953233a3d087f`.
  - The review clone was verified byte-exact at the end: 554 tracked files rehashed, 0 blob or mode mismatches. The index and `write-tree` equal the head tree, and there are no untracked or ignored files.
  - The repository has no submodule gitlinks (`receipts/clone_integrity.txt`).
- **Source base:** `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- **Delta reviewed:** `9e869910..1cba30c9`, which is:
  - the author's four round-2 commits, `89b000c`, `b1b6a5a`, `6b82f9b` and `2ff8183`;
  - the manager's `--no-ff` merge of processor `main` `07b1469d` (PR #154).
- **Assignment:** #639 comment 5981052216 (round 2, test-only).

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open, and all five lenses are CLEAN. I recorded one RESIDUE and two SUGGESTIONs. All four prior public findings on this PR are resolved at this head.

**R462-1 F1 is closed by a committed check, and the round-2 bar is met:**
- R462-1's published `scripts/aq_probe.sh` ran unchanged at this head, under the pinned simulator.
  - `write_refused` exits 1, with AQ3 failing on 8,272 of 90,172 edges.
  - `wr_wrap_hi` exits 1, with AQ3 failing on 19,343 edges.
- Every control in R462-1's `lockstep_armq/gen.py` `--mutant` table fails AQ3. The table was imported unchanged and each edit planted once in the head's top. Its `hd_not_reset` equivalence probe passes.
- AQ passes on the head and on the RTL of `main` `c050d971`, of `main` `07b1469d` and of the base `5c71928a`. All four runs print byte-identical AQ coverage lines.
- `acmp_mutants.py` reports 33 of 33 KILLED, with four goldens PASS. Every `armq_*` arm fails exactly its README count.

## Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R463-2-R1 | RESIDUE | Docs | Author round-2 evidence packet, `review-evidence/pp639-r1/author-r2/lockstep/README.md` (milan-fpga `pp639-review-evidence` `b95bc644`): both "To regenerate and re-run" blocks | (a) It says `sha256sum -c GENERATED.sha256`, but that file has three columns (digest, size, path), so the command reports 19 "FAILED open or read". (b) `sh run_matrix.sh again` calls `./build.sh`, which is published as mode 100644 in both `armq/` and `lsn/`, so the run stops with "Permission denied". Both adaptations are applied in `scripts/lockstep_slice.sh`. With them, all 19 generated inputs match `GENERATED.sha256` byte for byte, and five published `armq` logs reproduce byte for byte (`receipts/lockstep_slice/run.txt`). | Wording of an evidence README's instructions only. No figure, test, code, generated artifact or claim changes, and nothing in the processor tree or PR body is affected. | Exact fix: (a) replace `sha256sum -c GENERATED.sha256` with `awk '{print $1"  "$3}' GENERATED.sha256 \| sha256sum -c`. (b) Precede `sh run_matrix.sh again` with `chmod +x build.sh` (in `armq/` and in `lsn/`). The manager carries both to the residue checklist. | Follow the edited steps from a fresh copy: `sha256sum -c` prints 19 OK, and `run_matrix.sh` builds. |
| R463-2-S1 | SUGGESTION | Docs | `hdl/top/protocol_processor_top.sv:3002-3004` (the S1 banner) | The banner's "1,153 at 631eeb34" matches the #234 baseline (`docs/findings/234_PP_SHADOW_AREA_BASELINE.md:340,447` at dev `241f9184`). "1,152 at 5c71928a" is the author's cell census (`baseline_cells.tsv`, HANDOFF §5.5). That census is not in the published Vivado receipts: base `ooc-1x1` has only the log, hierarchy, utilization, timing, parameter and image files. R462-1 recorded the same limit. | None on behaviour. Neither the RTL nor the netlist changes, and the edit is comment-only (0 non-comment lines). The figure simply cannot be re-derived from public receipts. | Optional: publish the base 1x1 `armq_r` census lines, or `baseline_cells.tsv`, in the next evidence archive. | The banner's 1,152 can be counted from a published file. |
| R463-2-S2 | SUGGESTION | Tests | `tb/pp_top/sim_main.cpp:738-745` (`onto`, `refused`, `multi` counters) and `:13923` (the `AQ drive:` line) | The drive's reach is printed summed over faces. The full-pop+push state (`onto[4]`) is reached mostly by the highest-priority face that pops. I checked that lower faces are reached too. Six single-face plants were each KILLED by AQ3 (`receipts/face_probes/`): `full_pop_refuses` and `wr_wrap_hi` on face 7 and on face 3, plus `write_refused` and `wr_at_head` on face 7. | None today. A later reseed or rate change could narrow per-face reach without AQ4 noticing. | Optional: print `onto[4]` and refusals per face, or require in AQ4 that `onto[4]` is reached on at least two faces. | AQ4 fails if the draw stops filling and popping a face other than face 0. |

## Prior public findings at this head

These were read after this review's own pass, verdict and ledger had been drafted.

| Prior finding | Severity | Status at `1cba30c9` | Evidence |
|---|---|---|---|
| R462-1 F1: the rings' full-queue path has no committed or reproducible check | MINOR | **RESOLVED**, as its required outcome states | Each item checked below. |
| R462-1 S1: name the source of "1,153 flops" | SUGGESTION | **RESOLVED** | Banner `:3002-3004` names 1,152 at `5c71928a` and 1,153 at `631eeb34`. The `hdl/` delta `9e86991..2ff8183` has 0 non-comment lines. |
| R463-1 F1: 09 §8.8 says the benches are "recorded in the issue's pull request" | RESIDUE | **RESOLVED** | The sentence is gone. 09 §8.8 now cites AQ2, AQ3 and AQ4 and the in-tree controls. No file in the lane's set mentions a lockstep bench (`git grep`). |
| R463-1 S1: three ring defects pass every committed check | SUGGESTION | **RESOLVED** | R463-1's published `armq_lockstep/extract.py` table was imported unchanged (sha256 `d39e2272…`) and planted in the head. `write_refused`, `read_write_first` and `full_pop_refuses` each fail AQ3; `read_write_first` fails on 12,481 edges, exactly the drive's full pop+push count. `drop_wraps` fails too, and `probe_head_unreset` passes (`receipts/prior_r463_1/summary.txt`). |

**How R462-1 F1's required outcome is met:**

| Item | Met | Evidence |
|---|---|---|
| counts 2 to 4 | yes | AQ drive: pushes onto a face holding 1, 2 and 3 arms: 48,239, 3,636 and 5,594 |
| full pop+push in one clock, leaving head overwritten | yes | 12,481 |
| refused push with its drop | yes | 352,294 refused in 80,719 drop clocks |
| two faces dropping in one clock | yes | 78,930 clocks |
| counter saturation | yes | 4,096 drop clocks held at 0xFFFF; AQ4 requires it |
| reset with arms queued | yes | 36 resets; 366 arms offered in reset |
| `write_refused` and a depth ≥ 2 write-index control KILLED by a named check | yes | `armq_write_refused` and `armq_write_wrap_hi` are KILLED by AQ3, plus `armq_full_pop_refuses` and `armq_drop_skip_sat` |
| recorded in `tb/pp_top/README.md` section AQ | yes | the nine-row table; counts 72, 3, 12, 3, 3, 1, 1, 1, 1, all reproduced |
| 09 §8.8, README `:2009`/`:2028` and `acmp_mutants.py:165-168` fixed | yes | read at the head |
| R462-1's probes and `gen.py --mutant` caught; passes on head and on `main`'s RTL | yes | see Verdict |

The reach figures come from my own runs. They are identical in the `--arm-queue-only` run and in the full default run of `make run`.

## Evidence by lens

### Conformance: CLEAN

- **Round 2 changes no behaviour.**
  - `git diff 9e86991 2ff8183 -- hdl/` changes only the banner comment: 0 added or removed non-comment lines.
  - The merge's `hdl/`, `tb/pp_top`, `tb/acmp_listener` and `tb/common` delta (`git diff 2ff8183 1cba30c`) equals `git diff c050d971 07b1469d` exactly, so it is PR #154's own.
  - Against `main` `07b1469d`, the head's `hdl/` differs only in the lane's two files: `protocol_processor_top.sv` and `KL_pp_acmp_listener.sv`.
- **Behaviour the issue requires is kept.** The issue's rule is no port, parameter, register or protocol-visible timing change.
  - The drive passes on `main`'s and on the base's shift-queue RTL with byte-identical coverage.
  - So AQ3 grades behaviour the lane kept: drain order, depth 4, the newest arm dropped, and the drop counter counting one per clock and saturating.
- **Scope keywords:** "Relates to milan-fpga#639" and "Relates to milan-fpga#229" are right. The baseline re-record lives in the parent.

### RTL: CLEAN

- **Ring:** `protocol_processor_top.sv:2994-3048`, re-read at the head.
  - A push writes at old head + old count. A refused push (count after the pop = 4) does not write.
  - A full pop+push writes onto the leaving head after the asynchronous read has fed the port register.
  - Head and count reset; the entries are unreset and are never read before a write.
- **S1 banner** (`:3002-3007`): comment only. The 1,153 figure matches the #234 baseline; for 1,152, see S1.
- **Lint:** 41 `LINT OK` lines, rc 0, pinned simulator (`receipts/static/lint_hdl.txt`).
- **Merge `1cba30c`:**
  - Its parents are `2ff8183` and `07b1469d`.
  - `git merge-tree --write-tree 2ff8183 07b1469d` gives `c81e4a5e…`, which is the head tree.
  - `docs/guides/hdl-engineer.md` keeps both sides: main's SRP paragraph (`:88-94`) and the lane's distributed-RAM paragraph (`:96-107`).

### Robustness: CLEAN

- **The drive's independence:**
  - `ArmQueueModel` (`sim_main.cpp:722-818`) is eight C++ `std::deque` FIFOs with a priority pop and a saturating per-clock drop counter. It shares nothing with the ring's index arithmetic.
  - It is fed from the face taps, which read the forced nets.
  - AQ4 reads only the model.
- **The fault matrix at the head** (`receipts/aq_matrix/`, 20 runs, all as expected):
  - Both R462-1 probes fail.
  - All nine `gen.py` controls fail AQ3, and the five round-1 controls also fail AQ2.
  - `hd_not_reset` passes.
- **Red proof:** the four full-queue controls planted in round 1's tree (`9e86991`) pass AQ with 2 of 2 checks, so AQ3 is what kills them.
- **Per-face probes** (beyond the bar; see S2): 6 of 6 KILLED by AQ3, on faces 7 and 3.
- **Reset with arms queued and offered** is graded: the model clears on reset, and the port and counter are compared at reset edges.
- **Determinism:** fixed seed 639. My `--arm-queue-only` and full default runs print figures identical to the README table.

### Tests: CLEAN

| Run (pinned simulator 5.050, exact-head export) | rc | Result |
|---|---:|---|
| `acmp_mutants.py --jobs 8` | 0 | 33 of 33 KILLED, 4 goldens PASS; all 33 failing counts equal their README records (`receipts/acmp/`) |
| `tb/pp_top` `make run` (five builds) | 0 | 10,420 checks: 10,420 PASS, 0 FAIL; AQ 4 checks, 0 failures |
| `tb/acmp_listener` `make run` | 0 | 3,111 of 3,111 PASS |
| `--arm-queue-only` | 0 | AQ 4 checks, 0 failures; build tally 1,655 checks |
| AQ matrix (`scripts/aq_matrix.py --jobs 6`) | 0 | 20 of 20 as expected |
| per-face probes (`scripts/aq_face_probes.py`) | 0 | 6 of 6 KILLED |
| R463-1 control table (`scripts/aq_prior_r463_1.py`) | 124 (stopped by its 590 s cap) | 9 of 10 finished as expected; `read_tail` did not finish (same edit as the KILLED `armq_read_tail` and `gen_read_tail`) |

- Named-check semantics: `acmp_mutants.py:283-287` declares KILLED only when every named check fails. So the five round-1 ring arms now require both AQ2 and AQ3.
- The test-only status of the 41 force targets is established under Docs below.

### Docs: CLEAN (R1 RESIDUE, S1 recorded)

- **Gates:**
  - `make check`: lint, wavedrom, 1,134 links, matrix (115 REQ rows; 94 rows, 0 untested) and 28 parameters all pass. Its `stale` step was run in the git clone, rc 0. In a `.git`-less export, `stale` falls back to mtimes and is not meaningful (`receipts/static/`).
  - `gen_matrix.py --check` rc 0.
- **Checked against the measured runs:**
  - 09 §8.8.
  - `tb/pp_top/README.md` section AQ: the drive prose, the reach table and the nine-row control table.
  - The `acmp_mutants.py:165-168` comment.
  - The ACMP controls paragraph: "fourteen controls: nine here … five in `tb/acmp_listener`"; "all 33 KILLED".
- **The published lockstep benches:**
  - All 19 generated inputs regenerate byte for byte from `5c71928a` and `9eebc61` (`GENERATED.sha256`).
  - A re-cut at this head differs from `dut.sv` only in the S1 comment and the generated first line, as the packet README states.
  - The `build.sh` digest differences against `SHA256SUMS` are the manager's recorded path redactions: MANIFEST.json gives `original_sha256` equal to `SHA256SUMS`.
  - Instruction defects: R1.
- **Parent port-contract inventory, 256 → 297:**
  - The wrap's `u_dut.` references go from 157 to 198, so +41. All 41 are the new `force` lines: 40 face nets, all of them already tapped at `9e86991`, plus `u_dut.u_timer.arm_valid_i`.
  - The parent's `scripts/check_port_contracts.py` at dev `6c22d3ca` counts these in `test_backdoors()`. That function is a "read-only inventory of hierarchical observation confined to test RTL" over `tb/**/*.sv`, outside the ratchet. So the change is just an inventory change.
- **PR body:** the round-2 tables match my runs, and the manager's merge note matches the merge.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #639 body and comments 5976100204, 5981052216; round-2 `hdl/` delta (comment only); merge delta equals PR #154's; AQ on `main` `c050d971`/`07b1469d` and base `5c71928a` RTL; closing keywords | R463-2 | 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc |
| RTL | CLEAN | `protocol_processor_top.sv:2924-3048` incl. the S1 banner; lint, 41/41; merge-tree recomputation; `hdl-engineer.md` merged hunks | R463-2 | 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc |
| Robustness | CLEAN | `ArmQueueModel` and `drive_arm_faces`; `pp_top_wrap.sv` force block; 20-run AQ matrix incl. R462-1 probes and `gen.py` table; red proof on `9e86991`; 6 per-face probes; R463-1 table | R463-2 | 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc |
| Tests | CLEAN | `acmp_mutants.py` 33/33 with counts; `tb/pp_top` `make run` 10,420; `tb/acmp_listener` 3,111; `--arm-queue-only` reach | R463-2 | 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc |
| Docs | CLEAN (R1 RESIDUE) | 09 §8.8; `tb/pp_top/README.md` AQ and ACMP paragraph; `acmp_mutants.py` comment; PR body; author lockstep packet (regeneration, re-cut, digests); parent port-contract inventory; `make check`, `gen_matrix --check` | R463-2 | 1cba30c91bbc4c0e20343f883b94c3f701cc0dbc |

## Real limits

- **Not run** (outside this reviewer's allowance):
  - `run_suites.sh`, `syn/yosys/run.sh`, and every campaign other than `acmp_mutants.py`;
  - the parent consumer set of 17;
  - any Vivado run.
- **Round 2 is test-only plus a comment,** so this review did not re-derive the round-1 Vivado figures. Round 1's reviews covered them, and the netlist cannot change.
- **The drive runs at the default 1x1 shape only.** The round-1 lockstep benches covered slot widths 5 to 8. I re-ran only a slice of them: candidate at widths 6 and 7, and `ctl_write_refused`. The listener bench was regenerated but not re-run.
- **The R463-1 control table's `read_tail` run did not finish** within its cap. The same edit is KILLED in two other runs at this head.
- **Shared host:** other lanes' jobs ran alongside. Every golden and every unplanted run passed.
- **Hosted CI** at the exact head, read at 2026-10-04T18:32Z (`receipts/hosted_checkruns_1cba30c9.json`):
  - `docs-gates` and `portability` succeeded in both workflows;
  - both `suites` jobs were still in progress.
- **Physical calibration NOT RUN.** No hardware was used; field skips are not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the two `suites` jobs still in progress.
- The final current-dev candidate build at the merge turn (source base `5c71928a`, live dev `6c22d3ca`).
- The parent consumer set of 17 at dev `6c22d3ca` + c8, p2-p1, c10 and 232, with the processor at this head. That includes:
  - the port-contract inventory at 297;
  - the #232 xvlog banking (PR #153's `pd_ix_w`);
  - gate 16's T30 behaviour now that #643 is merged.
- The resource-gate baseline re-recorded at the adoption pin (#639's "same reviewed change").
- Carry R463-2-R1 to the residue checklist. S1 and S2 are optional.
- Archive this packet.

R463-2 FINISHED
