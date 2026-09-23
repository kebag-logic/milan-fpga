# [A217] HANDOFF: PR #107 / issue #106, correction round 1

Role: author, correction round 1 of PR #107, answering R270-1 and R271-1.
Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan.
Lane: `$LANES/pp106-leaveall-scope`, branch `106-leaveall-scope`.

| | |
|---|---|
| source base | `fbc1f7156d711e5b7f511da8a16d9494256b017b` |
| reviewed head (R270-1, R271-1) | `fc155c3ca28b04c2220bf41ebea9214379210452` |
| **corrected head** | **`27763677d83d4df7237389ffc0945ef9e224aa31`**, tree `7bfd82de512acd31a3378cf69a6bb30931395a56` |
| working tree | clean |
| pushed / PR edited / merged | **no / no / no** (not allowed this round) |

For the manager: push `106-leaveall-scope` to `27763677`, then replace the PR #107 body with `PR-BODY.md`. It starts with `[A217]` and contains `Closes #106`.

## Commits added on top of `fc155c3c` (one-line subjects, no trailers)

| commit | subject | answers |
|---|---|---|
| `871213549bb83ae5a5a19cddf9de04ea4390081a` | Pin both boundaries of the once-per-MRPDU LeaveAll gate in the decoder suite | R270-F1 = R271-F1 |
| `039ec3269b89064c02318dcf217e4ae3c9217f1c` | Check that a Listener-only LeaveAll never re-declares our Domain | R270-S1 (= R271-S1 R4) |
| `90f4a0f1c731b54b8ec1667d7641c275654e9aef` | Stop crediting a timer restart on a received LeaveAll and track the deviation in #108 | R270-F2 (retained by R271-1); manager correction item 1 |
| `acd44d7fbf6dddd4d346045302cdc3a2b48a01d5` | State the 10.7.5.20 NOTE criterion for the LeaveAll attribute-type constant | R270-S3 |
| `27763677d83d4df7237389ffc0945ef9e224aa31` | Record the gate-boundary and Domain-negative failing arms in the suite READMEs | README tallies for the above |

The RTL behaviour is unchanged. In `hdl/`, `fc155c3c..27763677` changes comment lines only, in `KL_srp_encoder.sv` and `KL_srp_top.sv`. `KL_srp_decoder.sv` is byte-identical (SHA-256 prefix `255adc30e55463a8` in both arm receipts). The timer behaviour (#108) is not touched.

## Per finding

| finding | severity, lens | what changed | evidence |
|---|---|---|---|
| R270-F1 = R271-F1 | MINOR, Tests / Robustness | `tb/srp_decoder` T: only a LeaveAllEvent closes the gate. T1 is one Listener message `[JoinIn][LA JoinIn][LA JoinMt]` giving `E3 L3 E3 E3`. T2 is across messages, `[L JoinIn][Domain LA n=2][L LA JoinMt]` giving `E3 L4 E4 E4 L3 E3`. T3 is MVRP, `[VID][VID LA]` giving `E1 M1 E1`. `tb/srp_decoder` U: the gate re-arms at the MRPDU after a malformed one: U1 truncated mid-FirstValue, U2 single EndMark, U3 bad AttributeLength discard (its Domain LeaveAll never fires), U4 MVRP out-of-alphabet discard. Each is followed by a good MRPDU whose lane must fire again. Full strobe timelines throughout. 150 → 177 checks. | X1/R1: 6 FAIL (T1-T3). Y2: 2 (T1). X7: 4 (U1-U4). R8: 4 (U1-U4). Y1: 1 (U4). Every arm survives all four SRP suites at `fc155c3c` (`receipts/arms-base-fc155c3c.txt`) and is killed at `27763677` (`receipts/arms-head-27763677.txt`). The reviewers' own scripts, unmodified, agree (`receipts/reviewer-scripts-rerun.txt`). |
| R270-F2 (R271-1 retained) | MINOR, Docs | `docs/10_RESOURCE_AND_EFFORT.md` no longer credits this spec with restart or Passive on a received LeaveAll. It keeps the 10-15 s point, says this spec does not restart either, and points to 10 §6.5 and #108. docs 10 §6.5 states the deviation against Table 10-5 (§10.7.9) and §10.6 and now points to #108, not #106. The `KL_srp_top` banner points to #108. | `receipts/gates-docs.txt`: make check OK, links 810 OK |
| R270-S1 (= R271-S1 R4) | SUGGESTION, Tests | `tb/srp_top` F5c: `sync()` into a clean slot, feed the Listener-only LeaveAll, and require no Domain JoinIn for 400 ms (the next periodic is ≥ 650 ms away). The rest of F5c keeps its timing relative to the feed. 252 → 253 checks. | X2/R4: 1 of 253 FAIL (F5c) at head; 0 of 252 at `fc155c3c` |
| R270-S2 | SUGGESTION, Docs; superseded by correction item 1 | §6.5 and the top banner point to #108 | as F2 |
| R270-S3 | SUGGESTION, Docs | The `LA_TYPES_MSRP_C` comment, the encoder banner and inline comments, the top banner and the §6.5 transmit paragraph now state the §10.7.5.20 NOTE criterion ("each Attribute Type supported by the application") rather than "registers". Comments and prose only. | lint 37 OK, yosys 32 + Xilinx OK |
| R271-S1 R5, R10, R11 | SUGGESTION, Tests (inherited gaps) | **not taken**: outside this round's assignment | none |
| R271-S2 (#29 vs #108) | SUGGESTION | **not changed**: linking or closing issues is the manager's | none |

## Arms (`scripts/arms.py`)

- Each arm goes into a fresh `git archive <rev>` export under `scratch/`, never the lane checkout.
- A plant whose pattern does not occur exactly once is refused. The before and after SHA-256 of the planted file are recorded.
- All four SRP suites run under the CI simulator pin 5.050.
- X1/R1, X7, R8 and X2/R4 are copied verbatim from R270-1 `scripts/mutation_probes.py` and R271-1 `scripts/03_mutate.py`.
- Y1 (the gate re-arms only for an MSRP MRPDU) and Y2 (the lane fires only at an MSRP message's first VectorHeader) are mine, of the X7 and X1 classes.
- The rows recorded in the READMEs were measured at `acd44d7f` (`receipts/arms-head-acd44d7.txt`). `acd44d7f..27763677` changes only the two README files, and the rerun at `27763677` gives identical counts.

Reviewer scripts, rerun unmodified at `acd44d7f` (`receipts/reviewer-scripts-rerun.txt`):
- The files' SHA-256 equal the entries in the archived `MANIFEST.sha256` of each review: `mutation_probes.py` b7c0a535…, `run_srp_suites.sh` a31f36a2…, `03_mutate.py` 448f1842….
- R270-1 X1: srp_decoder 6 of 177 FAIL. X7: 4 of 177. X2: srp_top 1 of 253.
- R271-1 R1, R4 and R8: all KILLED.

## Gates at `27763677` (CI simulator pin 5.050, `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`)

| gate | result | receipt |
|---|---|---|
| `make check` | OK: lint 41 mermaid + 18 wavedrom; links 810; matrix 115 REQ / 17 GAP; module matrix 86 rows, 0 untested; stale OK | `receipts/gates-docs.txt` |
| `scripts/lint_hdl.sh` | 37 OK, 0 FAIL | `receipts/gates-lint.txt` |
| `scripts/run_suites.sh` | 30/30 suites, 15,464 checks, 0 failing; srp_decoder 177, srp_encoder 556, srp_stream_fsms 1068, srp_top 253 | `receipts/gates-suites.txt` |
| `scripts/gen_matrix.py --check` | OK | `receipts/gates-docs.txt` |
| `syn/yosys/run.sh` | 32 tops OK plus the Xilinx memory map, 0 FAIL | `receipts/gates-yosys.txt` |
| `python3 scripts/check-links.py` | 810 checked, OK | `receipts/gates-docs.txt` |
| `git diff --check fbc1f715..HEAD` | clean | `receipts/gates-docs.txt` |

**Not run by the author:**
- The parent consumer gates. They are the manager's, at the final parent candidate.
- The CI step `make -C tb/nvm_port figures`. It needs the `refs/pull/13/head` fetch, and the testbench is untouched.
- The #530 end-to-end harness. It was last run at `9370f8ab`.
- Hardware: none was used.

## Inputs read

- Issue #106 and all its comments, including the scope decision 5798176959 and the manager's correction 5801278433. Issue #108 (the timer tracker).
- PR #107 and its body.
- The reviews R270-1 (5801267950) and R271-1 (5801727037).
- Read-only from milan-fpga branch `pp106-review-evidence`, `review-evidence/pp106-r1/reviews/{R270-1,R271-1}/`:
  - the mutation and probe scripts and receipts: X1-X7, R1-R11, Z1-Z3, U/A;
  - both `MANIFEST.sha256`.
  - Copies are in `ref/`.
- The parent's `AGENTS.md` and `CONTRIBUTING.md` (milan-fpga `5e7eb309`), read for the em-dash and role-naming rules.
- No private transcripts. Nothing under `$MANAGEMENT` outside this directory.

## Observations for the manager

- Lines added by this round carry no U+2014. The two round-0 commits (`fbc1f715..fc155c3c`) add 43 lines that do. This donor has no em-dash gate, and neither review flagged them, so they are not changed here.
- The parent's `docs/traceability/ieee8021q.md` row MRP-5 still states per-application receive semantics (R270-1 §7 item 4, R271-1 §9). That is a parent-adoption edit.
- Both reviewers still have to re-review `27763677`. Coverage for Tests, Robustness and Docs was re-opened by the findings. RTL comments changed in `KL_srp_encoder.sv` and `KL_srp_top.sv`.

## Packet layout

- `PR-BODY.md` and `HANDOFF.md`.
- `scripts/arms.py`.
- `receipts/`: gates, arms and the reviewer-script reruns.
- `ref/`: the reviewers' archived scripts and receipts, as fetched.
- `MANIFEST.sha256` covers all of the above.
- `scratch/` held the disposable exports and was removed after the runs.
