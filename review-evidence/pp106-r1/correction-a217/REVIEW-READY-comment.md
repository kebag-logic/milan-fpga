[A217] REVIEW READY: PR #107 correction round 1 for R270-1 and R271-1. Branch `106-leaveall-scope`, head `27763677d83d4df7237389ffc0945ef9e224aa31` (tree `7bfd82de`), five commits on the reviewed head `fc155c3c`, source base `fbc1f715`. Nothing is pushed and the PR is not edited; the new PR body (`[A217]`, `Closes #106`), handoff and receipts are in the review packet.

The RTL behaviour is unchanged: in `hdl/`, `fc155c3c..27763677` changes comment lines only (`KL_srp_encoder.sv`, `KL_srp_top.sv`), and `KL_srp_decoder.sv` is byte-identical. The timer behaviour (#108) is not touched.

| Finding | Commit | Change | Failing arm (at `fc155c3c` → at `27763677`) |
|---|---|---|---|
| R270-F1 = R271-F1, MINOR, Tests / Robustness | `87121354` | `srp_decoder` T, full strobe timelines: T1 one Listener message `[JoinIn][LA JoinIn][LA JoinMt]` = `E3 L3 E3 E3`; T2 across messages `[L JoinIn][Domain LA n=2][L LA JoinMt]` = `E3 L4 E4 E4 L3 E3`; T3 MVRP `[VID][VID LA]` = `E1 M1 E1`. `srp_decoder` U: a lane-firing MRPDU that is then truncated mid-FirstValue (U1), ends after the list EndMark alone (U2), meets a bad AttributeLength whose discarded Domain LeaveAll never fires (U3), or is MVRP with an out-of-alphabet digit (U4); each keeps its prefix and is malformed, and the next well-formed MRPDU fires the lane again. 150 → 177 checks. | X1 = R1: 0 → 6 FAIL (T1-T3). X7: 0 → 4 (U1-U4). R8: 0 → 4 (U1-U4). Own X1-class Y2 (lane only at an MSRP message's first VectorHeader): 0 → 2 (T1). Own X7-class Y1 (re-armed only for an MSRP MRPDU): 0 → 1 (U4). |
| R270-F2 (retained by R271-1), MINOR, Docs | `90f4a0f1` | `docs/10_RESOURCE_AND_EFFORT.md` no longer credits this spec with restart or Passive on a received LeaveAll; it keeps the 10-15 s point and points to 10 §6.5 and #108. docs 10 §6.5 states the deviation against 802.1Q-2014 Table 10-5 (§10.7.9) and §10.6 and now points to #108, not #106; the `KL_srp_top` banner too. | none (docs): `make check` OK, links 810 OK |
| R270-S1 (= R271-S1 R4), SUGGESTION, Tests | `039ec326` | `srp_top` F5c: in a clean 200 ms slot, no Domain JoinIn follows a Listener-only LeaveAll before the next periodic re-join. 252 → 253 checks. | X2 = R4: 0 of 252 → 1 of 253 FAIL (F5c) |
| R270-S2, SUGGESTION, superseded by correction item 1 | `90f4a0f1` | §6.5 and the top banner point to #108 | none |
| R270-S3, SUGGESTION, Docs | `acd44d7f` | the `LA_TYPES_MSRP_C = 4'b1111` comment, encoder and top banners and the §6.5 transmit paragraph state the §10.7.5.20 NOTE criterion ("each Attribute Type supported by the application") instead of "registers" | none (comments and prose) |
| R271-S1 R5, R10, R11 | none | not taken: inherited gaps outside this round's assignment | none |
| R271-S2 (#29 vs #108) | none | not changed: the manager's call | none |

`27763677` records those arms in the two suite READMEs.

**Arms.** Each is planted exactly once into a `git archive` export and run on all four SRP suites. X1/R1, X7, R8 and X2/R4 are the reviewers' own plants, verbatim. The reviewers' scripts, unmodified (SHA-256 equal to their archived manifests), rerun at the new tests: R270-1 `mutation_probes.py` X1 6 FAIL, X7 4 FAIL, X2 1 FAIL; R271-1 `03_mutate.py` R1, R4 and R8 KILLED. Every arm passes all four SRP suites at `fc155c3c`.

**Gates at `27763677`, CI simulator pin 5.050**
- `make check`: OK (links 810, matrix, module matrix 86 rows / 0 untested, stale).
- `scripts/lint_hdl.sh`: 37 OK.
- `scripts/run_suites.sh`: 30/30 suites, 15,464 checks, 0 failing (15,436 at `fc155c3c`; srp_decoder +27, srp_top +1).
- `scripts/gen_matrix.py --check`: OK.
- `syn/yosys/run.sh`: 32 tops OK plus the Xilinx memory map.
- `python3 scripts/check-links.py`: OK.
- `git diff --check fbc1f715..HEAD`: clean. Lines added by this round carry no U+2014.

**Not run by the author:** the parent consumer gates (the manager's), the #530 harness (last at `9370f8ab`), and `tb/nvm_port figures` (untouched). No hardware.

**For the manager:** push `106-leaveall-scope` to `27763677` and replace the PR #107 body from the packet's `PR-BODY.md`. R270 and R271 re-review this head.
