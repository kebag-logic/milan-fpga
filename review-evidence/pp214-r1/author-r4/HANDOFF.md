# [A736e] HANDOFF: processor issue #214, round 4 (R779-2 F-1, F-2 and R780-2-F1)

**Status: REVIEW READY (posted on the issue) at `7feeccea3a6c8210ece8d5d1d8929d67582163f9`.** Every item of the ruling is closed and
every gate it names is rc 0 at this head. The assignment is the [A10] ruling on R779-2 and R780-2 (issuecomment-6700254065). No check found an
RTL defect, so no STOP: `hdl/` is byte-identical.

- Repository: the processor repository (`git remote get-url origin` checked), branch `214-one-vector-per-value`, local,
  not pushed. Base of this round `1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa`, main `9210065` (unchanged at the last check),
  original base `a9e84b66`.
- Head `7feeccea3a6c8210ece8d5d1d8929d67582163f9`. Two commits on `1c8b485`, history not rewritten:
  - `e28ac5a` Grade a push on the prepared LeaveAll round's start clock, drop PV20's offer on accept and walk every
    identity bit in PV14 and PV15, with two planted arms (issue #214)
  - `7feecce` Record the prepared round's case, the two arms, the bit walk and the measured counts in the encoder README
    and 09 8.14 (issue #214)
- `git rev-parse HEAD:hdl` equals `1c8b485:hdl` and `cc92e90:hdl`, `6f29f7158dc4` (`receipts/IDENTITY.txt`). No port,
  parameter, register-map or MRP timer change exists, the area of round 2 stands, and `KL_srp_listener_fsm.sv` is untouched.

## 1. The ruling, item by item

| Ruling item | Finding | Closure | State |
|---|---|---|---|
| 1. Row and planted arm for a push on the prepared own LeaveAll round's start clock; the arm removes only the `E_COLLECT` term of `start_tgt_w`; the row fails it by name | R779-2-F-1, R780-2-F1 | PV20's third case; `push-on-prepared-start` | closed |
| 2. PV20's offer drops on accept, so a lost push fails; comment corrected; such an offer fails the arm that now survives | R779-2-F-2 | `drop_on_accept`, for the whole of each case; `push-taken-in-alloc` plants the arm that survived | closed |
| Accepted with no row: `rv-search-ignores-start`, `rv-empty-table-searches`; record both as judged; correct the "no tally" wording | both reviews | §4, and `PR-BODY.md` | closed |
| Suggestion: identity-bit walk in PV14 and PV15, only if no more than a loop | R780-2-S1, R779-2-S-1 | taken: one loop in PV14, a wider bound on PV15's loop | taken |
| Suggestion: empty-frame survival, optional | R780-2-S2, R779-2-S-2 | taken: one member initialiser and its constant | taken |
| Gates: the two changed suites, the mutant campaign, the docs gates | | §6 | all rc 0 |

## 2. Changes (file:line at `7feecce`, clause)

| File:line | Change | Clause |
|---|---|---|
| `tb/srp_encoder/sim_main.cpp:308`, `:336` | `H::drop_on_accept`: `tick()` drops the offer on the clock it is taken | harness only; a producer's handshake |
| `tb/srp_encoder/sim_main.cpp:1920` | `offer_on_the_start_clock()`: the `prepared` argument, the offer dropping on accept, the new check that the offer is taken after the drain, and the corrected comment | 802.1Q-2022 10.8.3.1 a); 10 §3 |
| `tb/srp_encoder/sim_main.cpp:1955`, `:1964` | PV20's third case and its corrected comment | 10.8.3.1 a); issue #214 acceptance 1 (an own LeaveAll in the window) |
| `tb/srp_encoder/sim_main.cpp:1809` | PV14 walks all 64 StreamID bits; the function is renamed for it | 35.2.2.8.2, 10.7.7 |
| `tb/srp_encoder/sim_main.cpp:1830` | PV15 walks VID bits 0 to 11 | 11.2.3.1.7 |
| `tb/srp_encoder/sim_main.cpp:283`, `:512` | `got` starts sized, so a row that reads a frame nothing was captured into fails by name | harness only |
| `tb/srp_top/mutants.py:424`, `:429` | four rows for two arms | acceptance 2 |
| `tb/srp_top/mutations/push-on-prepared-start.patch`, `push-taken-in-alloc.patch` | one exact edit each of `KL_srp_encoder.sv`, written by `tools/make_arm_patches.py` | acceptance 2 |
| `tb/srp_encoder/README.md:6`, `:142`, `:153`, `:270`, `:280`, `:289`, `:290`, `:291`, `:293` | the count, the rows, the arm table, the base count | same clauses |
| `docs/architecture/09_verification.md:842`, `:845` | the two §8.14 rows | same clauses |

`docs/architecture/10_srp_engine.md` needs no edit: its rule ("A push that a drain start overtakes rides the next MRPDU")
already covers every start, and PV20 is still the last row. `receipts/STANDARDS.txt` quotes what was read: 10.8.3.1 a),
11.2.3.1.7 (VID 0 is in range, so PV15's bit 1 is a legal value), 10.7.7 and 35.2.2.8.2.

## 3. New checks, planted arms, failing words (measured at `7feecce`)

`tb/srp_encoder` reads `1604 checks: 1604 PASS, 0 FAIL`, up from 888: PV14 and PV15 add 704 (176 more frames of 4 checks),
the new check adds 2 to the two old PV20 cases, and the third case is 10. All passed on first run against the unchanged RTL.

| Check (failing words) | What it requires | Planted arm | At the `1c8b485` suite | At this suite |
|---|---|---|---|---:|
| `PV20 a Domain value on the prepared LeaveAll round's start clock: the offer waits on the clock its drain starts`, `...: the next frame captured`, `...: the offer rides the next MRPDU` | the offer waits on the clock the prepared round starts; the next frame carries it | `push-on-prepared-start` | 888 of 888 | 4 FAIL |
| `PV20 a Domain value on the MSRP drain's start clock: the next frame captured`, `PV20 a VID on the MVRP drain's start clock: the next frame captured`, each `...: the offer rides the next MRPDU` | a push taken while the drain waits for its slot is missing from the next frame | `push-taken-in-alloc` | 888 of 888 | 4 FAIL |

Both arms' rows are in `mutants.py`, so the campaign holds them. `tb/srp_top` does not see either arm (R779-2 measured
`8683 checks: 8683 PASS` under both edits, R780-2 under the first), which is why the encoder rows are the ones that matter.

Arm counts this round moved (`receipts/arms/encoder-arm-counts.tsv`, all in the README):

| Arm | Was | Is | Why |
|---|---:|---:|---|
| `second-queueing` | 72 | 68 | PV20 no longer fails: its offer no longer repeats, so it no longer needs the merge. Every PV row except PV8, PV14, PV15, PV19 and PV20 still fails |
| `identity-drops-top-octet` | 6 | 48 | eight bits of octet 0 for each of three types |
| `push-on-drain-start` | 6 | 10 | the third case; the new `the offer is taken` check does not fail under it |

**The base.** `tb/srp_encoder` on main's encoder (byte-identical to `a9e84b66`'s) reads `1604 checks: 1519 PASS, 85 FAIL`
(`receipts/arms/base-encoder.txt`): every PV row except PV8, PV14, PV15 and PV19, and O8. PV20 is 15 of the 85: the base takes
the offer before the start clock, into the drain it starts, so the frame carries both values and no next frame exists.

## 4. Arms judged, recorded

| Arm | Measured at this head | Judgement |
|---|---|---|
| `rv-search-ignores-start` | `1604 checks: 1604 PASS, 0 FAIL` | **Accepted with no row** by the ruling: it changes neither what is accepted nor what is sent. My round 3 word "equivalent" was too strong: R780-2 measured 22 first differences in 8,356,623 clocks, all `ev_ready_o` in the `E_COLLECT` corner, taken sooner from the same table |
| `rv-empty-table-searches` | `1574 checks: 145 PASS, 1429 FAIL`, `E1 push accepted` first (`receipts/arms/rv-empty-table-searches.txt`) | **Accepted with no row** by the ruling: caught by name in E1. **Correction:** round 3 said it "reads rc 2 with no tally" as if nothing named it. It always failed E1 by name; the suite then crashed reading the empty frame and buffered stdout lost those lines. With the empty-frame guard it now prints them and its tally |
| The `la_prepare_i` term of `start_tgt_w`, removed alone | `1604 checks: 1604 PASS, 0 FAIL` | Not in the ruling; both reviews found it latency only, because `E_COLLECT` takes a fresh count |

## 5. The reviewers' arms against this suite

From a clean clone of `7feecce`, with the pinned simulator:

- Second reviews (`receipts/arms/second-reviews-arms-and-bit-walk.tsv`): `x-start-collect-term-dropped` and
  `x-busy-not-in-alloc`, the arms the two findings named, fail PV20, 4 FAIL each. `x-start0-term-dropped` and
  `x-start1-term-dropped` fail PV20. `x-identity-top-octet-low7-dropped` and `x-identity-octet3-bit0-dropped`, which survived
  this suite before, now fail PV14 (42 and 6 FAIL).
- **The bit walk:** masking one key bit at a time, 64 of 64 StreamID bits and 12 of 12 VID bits fail, each by PV14 or PV15.
  R780-2 measured 51 of 64 and VID bits 2 to 7 surviving. VID bits 12 to 15 survive: they are outside the VID (11.2.3.1.7).
- First reviews (`receipts/arms/first-reviews-52-arms.tsv`): 51 of 52 fail by named checks, with a tally; the other is
  `rv-search-ignores-start`. Against round 3's table the only changes are `rv-empty-table-searches`, which now has one, and
  `rv-hit-still-counts`, `rv-hit-counts-entry` and their MVRP twins, which no longer touch PV20 and still fail their other rows.

## 6. Processor gates (clean clones of `7feecce`)

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| diff_check | 0 | 1 | (no output) |
| gen_matrix_check | 0 | 0 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 10 | LINT OK  protocol_processor_top |
| make_check | 0 | 32 | lint: 41 mermaid + 18 wavedrom blocks checked, OK |
| srp_encoder | 0 | 5 | 1604 checks: 1604 PASS, 0 FAIL |
| srp_top | 0 | 551 | 8683 checks: 8683 PASS, 0 FAIL |
| camp-srp | 0 | 3412 | 314 checks: 314 PASS, 0 FAIL |

`make_check` ran every target of `make check` with CI's pins (wavedrom 2.0.3.post3, Mermaid CLI 11.16.0); it ran with `-j8`,
so its last line is whichever target ended last, and the log shows links, matrices, parameters, the AECP command model, IDs,
figures and staleness each OK. `diff_check` is `git diff --check` against main.

The campaign reads `314 checks: 314 PASS, 0 FAIL`: 20 controls, 293 arm verdicts all KILLED by name, 0 UNPROVEN, assertion
coverage 174 of 174, 258 arm names and 258 patches, with `--jobs 8`. Against `1c8b485`
(`receipts/campaigns/1c8b485-vs-head.campdiff.txt`): 284 verdicts identical, 5 moved, 4 new. The five are the two
`identity-drops-top-octet` rows, the two `push-on-drain-start` rows and `second-queueing`'s encoder row, each still KILLED,
each count in §3 and the README. `memory.peak` read 8,332 MB, under the 10 GB target, with 0 OOM events.

**Interpreter.** Every gate asserted `python3` before and after it and would read rc 97 on a mismatch: all read this lane's own
venvs at 3.12.3 (`<gate>.python`), both built this round in this lane's scratch, package lists in `receipts/venv-*.freeze.txt`.
The arm runs outside `g()` printed the same check around each run.

## 7. Scratch-parent consumer gate table

The ruling's gate list does not include the parent. I ran the gates that read what this round changed anyway, because the
bench and `mutants.py` are read by the parent's idiom gates and a failure there would surface only at the gitlink bump. Parent
`604899c0` plus two local commits, never pushed: `480b29e9a5` (gitlink to `7feecce`) and `966aeca078`
(`./syn/yosys/ooc.sh --record-rom-digests`, rc 0). Branch `pp214-7feecce-consumer-gate`.

| Gate | rc | Last tally or verdict line |
|---|---|---|
| rom_digests | 0 | ooc.sh: recorded ROM content digests for protocol-processor pin 7feeccea3a6c |
| check_cpp_idiom | 0 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 75 checks: 75 PASS, 0 FAIL |
| check_py_idiom | 0 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 54 checks: 54 PASS, 0 FAIL |
| check_sv_idiom | 0 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) |
| check_sv_idiom_selftest | 0 | 55 checks: 55 PASS, 0 FAIL |
| check_sh_idiom | 0 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 48 checks: 48 PASS, 0 FAIL |
| check_doc_paths | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted) |
| check_hygiene | 0 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | review inventory line, rc 0 |
| check_rtl_source_lists | 0 | RTL source-list gate: OK (112 files in the milan_datapath closure) |
| docs_check | 0 | docs_check: 0 finding(s) across 213 md files |
| measure_fail_fast | 0 | the ratchets can be lowered to 78, 3 and 0 |
| measure_naming | 0 | NAMING RATCHET: PASS (95 candidate(s)) |
| measure_test_evidence | 0 | the mutation ratchet can be lowered to 67 |

The other 27 of the 43 gates, `milan_dp` and the firmware gates among them, were **not** re-run: they carry `1c8b485`'s figures
(`receipts/round3-1c8b485-GATE-TABLE.md`, all rc 0). `hdl/` is byte-identical to that head.

## 8. Residue and suggestions

| Item | Disposition |
|---|---|
| R780-2-R2, PV20's comment | Fixed: ruling item 2 required it |
| R780-2-R3 = R779-2 RES-2, PR body "so it does not change behaviour" | Fixed in `PR-BODY.md` with R779-2's exact wording, plus R780-2's "from the same table", as the ruling's record of the arm |
| R780-2-R1 = R779-2 RES-1, PV19's comment says an unknown type is never held | **Left open.** The ruling does not name it, and the assignment is the ruling. Wording only, and both reviews give an exact fix; it is a two-line comment edit if the manager wants it in |
| R-2, banner "the only reader", `hdl/srp/KL_srp_encoder.sv:76-77` | **Left open.** An RTL file, and the ruling keeps `hdl/` byte-identical |
| R-3, "(Run B, 10 §6.5)", `tb/srp_top/sim_main.cpp:3422` | **Left open.** Not named by the ruling, and this round does not touch that file |
| R780-2-S1 = R779-2 S-1, R780-2-S2 = R779-2 S-2 | Taken (§1) |

## 9. Acceptance items

1. **Met.** Each value at most once per MRPDU, for MSRP Domain, Talker and Listener and MVRP, through a received LeaveAll, an
   own LeaveAll, `periodic!` and a join in one window: OV0 reads every MRPDU of the run, OV1 to OV10 place each case, PV1 to
   PV20 grade each merge, the identity bit by bit, the read port and every kind of drain start. `tb/srp_top` 8683 of 8683,
   `tb/srp_encoder` 1604 of 1604.
2. **Met.** OV0 to OV7 and the PV rows fail without the fix and pass at the head. `second-queueing` re-enables the second
   queueing and fails `OV1:` and `PV1 two re-joins of one Domain value` by name.
3. **Met.** `tb/srp_top/mutants.py` 314 of 314 at this head. The other campaigns were green at `cc92e90`. Area at 2x2 and 8x8 stands, `hdl/` being byte-identical
   (`PR-BODY.md`; round 2's summaries in `receipts/area-round2/`).
4. **Met on the scratch parent.** 43 gates rc 0 at `1c8b485`; the 16 that read this round's files and the ROM recorder rc 0
   at `7feecce` (§7). The real parent bump is still to be done.

## 10. What this round did not do

- **Not re-run at this head:** the full sweep, the other sixteen campaign gates, the area, and 27 consumer gates. The ruling's
  gate list does not name them, and 6 files differ from `1c8b485`, none under `hdl/` or `tb/common/`. Their figures in
  `PR-BODY.md` are labelled with their heads. The executed traceability check needs the sweep, so it did not run; the static
  half in `make check` did, and these rows add no requirement tag.
- **The consumer gates ran on parent `604899c0`,** the parent this lane's brief names, not live dev. Both reviews list the
  merge candidate on live dev as a manager duty.
- **`tb/srp_top` does not drive the prepared-round path end to end.** Both reviews say so, and the ruling takes the encoder row.
- No hardware or bench access, and no timing result.

## 11. Notes for review

1. **Dropping the offer took something away as well as adding.** The held offer merged into itself after the commit, so PV20 was
   also, by accident, a merge check. `second-queueing` and four `rv-hit-*` arms therefore stopped failing PV20. All of them still
   fail their other rows, so nothing went ungraded, but `second-queueing`'s README row now excludes PV20.
2. **The row reads `the offer waits` and `the next frame captured` separately.** The first catches a push taken on the start
   clock. The second also catches a push taken on any later clock up to the commit, which is what `push-taken-in-alloc` plants.
3. **The guard cannot pass a row that should fail.** `got` is only read as zeros if no capture ever filled it, and each such row
   has already failed its own `CHECK` on the capture. At the head no row reads it first: the count is unchanged by the guard.
