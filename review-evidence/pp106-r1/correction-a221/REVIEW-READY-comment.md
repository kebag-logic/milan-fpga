[A221] REVIEW READY: PR #107 correction round 2 for R271-2 F1 (MINOR) and S1. Branch `106-leaveall-scope`, head `5f8cb1325312002c2c8bda45f30d98abc750ca7c` (tree `495bfb5d`), three commits on the reviewed head `27763677`, source base `fbc1f715`. Nothing is pushed and the PR is not edited; the new PR body (`[A221]`, `Closes #106`), handoff and receipts are in the review packet.

Tests only: `git diff 27763677..5f8cb132 -- hdl/` is empty. The changed files are `tb/srp_decoder/{sim_main.cpp,README.md}` and `tb/srp_top/{sim_main.cpp,README.md}`.

| Finding | Commit | Change |
|---|---|---|
| R271-2 F1, MINOR, Tests / Robustness | `c6149b25` | `srp_decoder` V, full strobe timelines computed by hand. V1 `[L LA JoinIn] [Domain LA n=2] [L LA JoinMt]` = `L3 E3 L4 E4 E4 E3`. V2 one Listener message `[LA JoinIn] [JoinIn] [LA JoinMt]` = `L3 E3 E3 E3`. V3 a Listener-only LeaveAll MRPDU of 19 octets (1+1+1+2+2+8+2+2, list 12), zero-padded with 27 octets to the 46-octet minimum payload, fed twice. Each time it gives exactly `L3` (no value event, no MVRP strobe) and exactly one done, ok and not malformed, at the dual EndMark. 177 → 190 checks. |
| R271-2 S1, SUGGESTION, Tests | `4f240356` | `srp_top` F5c extends the Domain-row negative to both talker lanes, each in its own clean slot. After a Talker Advertise LeaveAll (sink 0's Advertise re-declared in the flagged vector), and again after a Talker Failed-only LeaveAll, no Domain JoinIn follows for 400 ms. 253 → 255 checks. Step (c) now ends 7.64 s after its own LeaveAll; the next one comes at 11.8 s (draw 10-15 s). |
| (READMEs) | `5f8cb132` | tallies and the arm tables below |

**The reviewer's `mutants.py`, unmodified** (SHA-256 `f15d1953…`, equal to R271-2's manifest). Each plant goes exactly once into a `git archive` export and runs all four SRP suites:

| Plant | at `27763677` | at `4f240356` (`..5f8cb132` changes READMEs only) |
|---|---|---|
| K0 control | CONTROL PASSES (177/556/1068/253) | **CONTROL PASSES** (190/556/1068/255) |
| K5 re-armed only after a malformed or unpadded clean end | SURVIVED | **KILLED**: srp_decoder 1 of 190 (V3 second MRPDU) |
| K6 one register instead of one bit per type | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V1) |
| K7 an unflagged VectorHeader re-opens the gate | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V2) |
| K8 re-armed at every change of message type | SURVIVED | **KILLED**: srp_decoder 2 of 190 (V1) |
| K13 Domain also takes the Talker Advertise lane | SURVIVED | **KILLED**: srp_top 1 of 255 (F5c Talker Advertise) |
| K14 Domain also takes the Talker Failed lane | SURVIVED | **KILLED**: srp_top 1 of 255 (F5c Talker Failed-only) |

- Earlier kills still hold at `4f240356`: K1 6 (T1-T3), K3 4 (U1-U4), K10 1 (U4), K12 1 (F5c Listener-only).
- The planted `KL_srp_decoder.sv` SHA-256 for K5-K8 equal R271-2 receipt 03's.
- The archived `verilator_capped.sh` is mode 644, so the script was run from a byte-identical executable copy.

**Gates at `5f8cb132`, CI simulator pin 5.050**
- `make check`: OK (links 810, matrix, module matrix 86 rows / 0 untested, stale).
- `scripts/lint_hdl.sh`: 37 OK.
- `scripts/run_suites.sh`, clean build directories: 30/30 suites, 15,479 checks, 0 failing (15,464 at `27763677`; srp_decoder +13, srp_top +2).
- `scripts/gen_matrix.py --check`: OK.
- `syn/yosys/run.sh`: 32 tops OK plus the Xilinx memory map.
- `python3 scripts/check-links.py`: OK.
- `git diff --check fbc1f715..HEAD`: clean. Lines added by this round carry no U+2014.

**Not taken:**
- R271-2 S2 = R270-2 S4 (the "its leavealltimer" wording): this round is tests only.
- R270-2 S1-S3 (inherited gaps).
- #29 vs #108: the manager's call.

The new PR body also corrects the srp_top base count to 235 (R270-2 S4).

**Not run by the author:** the parent consumer gates (the manager's), the #530 harness (last at `9370f8ab`), and `tb/nvm_port figures` (untouched). No hardware.

**For the manager:** push `106-leaveall-scope` to `5f8cb132` and replace the PR #107 body from the packet's `PR-BODY.md`. R271 re-reviews this head.
