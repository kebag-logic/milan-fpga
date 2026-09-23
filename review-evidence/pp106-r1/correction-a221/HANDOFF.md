# [A221] HANDOFF: PR #107 / issue #106, correction round 2

Role: author, correction round 2 of PR #107, answering R271-2 F1 (MINOR) and S1.
Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
Lane: `$LANES/pp106-leaveall-scope`, branch `106-leaveall-scope`.
Assignment: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5803173950
REVIEW READY posted: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5804048297 (text: `REVIEW-READY-comment.md`)

| | |
|---|---|
| source base | `fbc1f7156d711e5b7f511da8a16d9494256b017b` |
| reviewed head (R270-2 POSITIVE, R271-2 NEGATIVE) | `27763677d83d4df7237389ffc0945ef9e224aa31` |
| **corrected head** | **`5f8cb1325312002c2c8bda45f30d98abc750ca7c`**, tree `495bfb5d5fbcf7c73cb347b0e5f8b4420be9842c` |
| working tree | clean |
| pushed / PR edited / merged | **no / no / no** (not allowed this round) |

For the manager: push `106-leaveall-scope` to `5f8cb132`, then replace the PR #107 body with `PR-BODY.md`. It starts with `[A221]` and contains `Closes #106`.

## Commits added on top of `27763677` (one-line subjects, no trailers)

| commit | subject | answers |
|---|---|---|
| `c6149b25c46caa91ea1be77f8102b213a88f8232` | Pin the LeaveAll gate closed to the MRPDU end and re-armed after a padded MRPDU | R271-2 F1 (G1-G3) |
| `4f2403566146fc5ccd92bccf6ebb70d3e5eb5f09` | Check that neither talker lane's LeaveAll re-declares our Domain | R271-2 S1 (K13/K14) |
| `5f8cb1325312002c2c8bda45f30d98abc750ca7c` | Record the gate-closure, padding re-arm and talker-lane Domain-negative arms in the suite READMEs | README tallies and arm tables for the above |

Tests only. `git diff 27763677..5f8cb132 -- hdl/` is empty (receipt `00-tools-and-head.txt`). The four changed files are `tb/srp_decoder/{sim_main.cpp,README.md}` and `tb/srp_top/{sim_main.cpp,README.md}`.

## Per finding

| finding | severity, lens | what changed | evidence |
|---|---|---|---|
| R271-2 F1 | MINOR, Tests / Robustness | `tb/srp_decoder` V, the reviewer's G1-G3 with hand-computed constants. **V1** `[L LA JoinIn] [Domain LA n=2] [L LA JoinMt]` (lists 14, 9, 14) = `L3 E3 L4 E4 E4 E3`, lanes once each, first JoinIn first and last JoinMt last. **V2** one Listener message `[LA JoinIn] [JoinIn] [LA JoinMt]` (list 38) = `L3 E3 E3 E3`, values in wire order. **V3** Listener-only LeaveAll MRPDU of 19 octets (1 + 1 + 1 + 2 + 2 + 8 + 2 + 2; list 12), zero-padded with 27 octets to the 46-octet minimum payload (64 − 14 − 4), fed twice: each time exactly `L3` and exactly one done, ok and not malformed, no list-length mismatch. 177 → 190 checks. | K5: 1 of 190 FAIL (V3 second MRPDU). K6: 2 (V1). K7: 2 (V2). K8: 2 (V1). All four SURVIVED at `27763677` (receipts `mutants-head-4f240356.txt`, `mutants-base-27763677.txt`). |
| R271-2 S1 | SUGGESTION, Tests | `tb/srp_top` F5c, after the Listener-only negative: `sync()`, feed a Talker Advertise LeaveAll that re-declares sink 0's Advertise in the flagged vector, require no Domain JoinIn for 400 ms; `sync()`, feed a Talker Failed-only LeaveAll, the same. The F5 comment now states the longer window of step (c). 253 → 255 checks. | K13: 1 of 255 FAIL (F5c Talker Advertise). K14: 1 of 255 (F5c Talker Failed-only). Both SURVIVED at `27763677`. Window timing: step (c) ends 7.64 s after its own LeaveAll; the next one came at 11.8 s, and the draw's minimum is 10 s (receipt `f5c-window-timing.txt`). |
| R271-2 S2 = R270-2 S4 (wording) | SUGGESTION, Docs | **not taken**: round 2 is tests only | none |
| R270-2 S1, S2 (= R271-2 K15-K17), S3 | SUGGESTION | **not taken**: inherited gaps outside this assignment | none |
| #29 vs #108 | SUGGESTION | **not changed**: the manager's call | none |

The previous PR body stated the srp_top base as 236. At `fbc1f715` it measures 235 (R270-2 S4, receipt `base-fbc1f715-srp-suites.txt`), and the new body says 235 → 255.

## The reviewer's mutant script (`scripts/R271-2/`)

- `mutants.py`, `gate_probe.py`, `run_srp_suites.sh` and `verilator_capped.sh` are byte copies of the R271-2 archive (`ref/reviews/R271-2/scripts/`). Their SHA-256 equal the review's `MANIFEST.sha256`. The only difference is the execute bit on the two shell scripts: the archived `verilator_capped.sh` is mode 644, which make cannot exec. The first attempt from `ref/` failed on that, with "Permission denied" and no tallies. It was discarded and rerun from the copy.
- Invocation: `REAL_VERILATOR=<pin> VL_JOBS=2 python3 scripts/R271-2/mutants.py <lane> <rev> <scratch> <receipt> K0 K5 K6 K7 K8 K13 K14`.

| Plant | at `27763677` | at `4f240356` |
|---|---|---|
| K0 control | CONTROL PASSES 177/556/1068/253 | **CONTROL PASSES** 190/556/1068/255 |
| K5 | SURVIVED | **KILLED** srp_decoder 1 of 190 (V3) |
| K6 | SURVIVED | **KILLED** srp_decoder 2 of 190 (V1) |
| K7 | SURVIVED | **KILLED** srp_decoder 2 of 190 (V2) |
| K8 | SURVIVED | **KILLED** srp_decoder 2 of 190 (V1) |
| K13 | SURVIVED | **KILLED** srp_top 1 of 255 (F5c Talker Advertise) |
| K14 | SURVIVED | **KILLED** srp_top 1 of 255 (F5c Talker Failed-only) |

Prior kills still hold at `4f240356`: K1 6 (T1-T3), K3 4 (U1-U4), K10 1 (U4), K12 1 (F5c Listener-only). The planted decoder SHA-256 for K5-K8 equals R271-2 receipt 03's.

`gate_probe.py` was not rerun. Its insertion anchor (`the_gate_re_arms_after_a_malformed_mrpdu();` directly followed by `printf(`) no longer occurs once V is called after U. The same three MRPDUs and timelines are now V1-V3 in the suite itself.

## Gates at `5f8cb132` (CI simulator pin 5.050, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`)

| gate | result | receipt |
|---|---|---|
| `make check` | OK: lint 41 mermaid + 18 wavedrom; links 810; matrix 115 REQ / 17 GAP; module matrix 86 rows, 0 untested; stale OK | `receipts/gates-docs.txt` |
| `scripts/lint_hdl.sh` | 37 OK, 0 FAIL | `receipts/gates-lint.txt` |
| `scripts/run_suites.sh` (clean `obj_dir`s) | 30/30 suites, 15,479 checks, 0 failing; srp_decoder 190, srp_encoder 556, srp_stream_fsms 1068, srp_top 255 | `receipts/gates-suites.txt` |
| `scripts/gen_matrix.py --check` | OK | `receipts/gates-docs.txt` |
| `syn/yosys/run.sh` | 32 tops OK plus the Xilinx memory map, 0 FAIL | `receipts/gates-yosys.txt` |
| `python3 scripts/check-links.py` | 810 checked, OK | `receipts/gates-docs.txt` |
| `git diff --check fbc1f715..HEAD` | clean | `receipts/gates-docs.txt` |
| U+2014 in lines added by `27763677..HEAD` | 0 | `receipts/gates-docs.txt` |

**Not run by the author:**
- The parent consumer gates. They are the manager's, at the final parent candidate.
- The CI step `make -C tb/nvm_port figures`. The testbench is untouched.
- The #530 end-to-end harness. It was last run at `9370f8ab`.
- Hardware: none was used.

## Resume note

A usage limit cut the previous session of this round mid-work, before any commit. Its uncommitted edits were the V section and the F5c extension. They were kept, re-verified by hand (byte layouts, list lengths, timelines) and kept as written, with two comment edits:
- the decoder V comment no longer names the review;
- the F5 comment states the step (c) window.

A patch of the edits as found is in `$VALIDATION_STORAGE/pp106-a221/uncommitted-at-resume.patch`, which is not published. Nothing had been posted on #106 or #107 by this round before the REVIEW READY.

## Inputs read

- Issue #106 comments (list and the assignment 5803173950), PR #107 state and comments list.
- R271-2 (5803168166) and R270-2 (5803079167) in full.
- The R271-2, R270-2 and A217 packets, from the copies already in this packet's `ref/` (from milan-fpga branch `pp106-review-evidence`): scripts, receipts 02 and 03, reports.
- No private transcripts. Nothing under `$MANAGEMENT` outside this directory.

## Packet layout

- `PR-BODY.md`, `HANDOFF.md`, `REVIEW-READY-comment.md`.
- `scripts/R271-2/`: the reviewer's scripts, executable copies.
- `receipts/`: gates, mutants at head and base, base tallies, the F5c timing, tools and head state.
- `ref/`: the reviewers' and A217's archived packets, as fetched.
- `MANIFEST.sha256` covers everything except itself.
- The disposable exports were under `$VALIDATION_STORAGE/pp106-a221/scratch-*` and were removed after the runs.
