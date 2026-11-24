[A834] REVIEW READY
Commit: ed7df79c6f87a4172c885f268ad67629bd56c4eb (branch `lwsrp-pin-r2` in the round-2 worktree, on
`dbba60e68a6e4a46f80e381c30ff823ee4ff7484`; not pushed, the manager pushes it to `20-lwsrp-pin-d1bb4f4`)

## Delta from dbba60e6

Two commits, three files, +34/-10 (`receipts/images/diff-stat.txt`):

- `4ad6c164` Count the twin grade self-test's checks as they run, and check that the sLA's rLA! takes a Registrar
  IN to LV at txLAF!
  - `tb/verilator/milan_dp/twin_mrp.py`:
    - `selftest(ran=None)` appends each named check to `ran` as it runs.
    - `--selftest` prints `OK (<len(ran)> checks)` or `FAILED <names> (<n> checks)`. No count is written into the
      source. It exits 1 if no check ran.
    - `selftest()` still returns the failed names, so outside callers (`probe_twin.py`, round 1's runner) work
      unchanged.
    - Two new checks, on a Domain that has sent JoinMt to QA and then received a peer's JoinIn (the Registrar IN):
      - `omission-from-full-registrar-in`: before the LeaveAll, every configuration has the Registrar IN. The value
        is left out of a full LeaveAll MRPDU, then JoinMt. Expected: 0 findings, configurations
        {(AA, LV), (AA, MT)}, boundary declared. That is txLAF! QA to VP plus the sLA's rLA! IN to LV (Table 10-4),
        then tx! from VP sends sJ with the Registrar not IN.
      - `joinin-after-omission-from-full`: the same with JoinIn. Expected: exactly one finding, "from VP, Table
        10-3's tx! sends JoinMt".
    - The docstring describes both checks.
  - `tb/verilator/milan_dp/README.md` (twin grade, "A value such a frame leaves out"): txLAF! still passes the
    sLA's rLA! to the Registrar. The self-test holds the full-frame case with the Registrar MT and IN, and prints
    the number of checks it ran.
- `ed7df79c` Describe the own-LeaveAll arms in the firmware gate's srp entry
  - `sw/firmware/ctrl/test/test_ctrl_firmware.py`, docstring only. The gate reads only its first line, for
    argparse. The `srp` entry now names the `srp_own_leaveall.cpp` arms: withdrawal 5 to 200 ms after the own
    LeaveAll, sent as Lv within 240 ms; none deregistered without a withdrawal; against an lwSRP MSRP peer; at
    8x8/1if on every input and at 1x1/1if.

## Validation (all at ed7df79c unless stated)

| What | Command | Result |
|---|---|---|
| Self-test | `cd tb/verilator/milan_dp && python3 -B twin_mrp.py --selftest` | `OK (11 checks)`, rc 0 |
| R913-1-F1 mutants | `python3 -I -B <r913-1>/scripts/twin_mutants.py <worktree> <scratch>` (unchanged) | control PASS; 9 of 9 CAUGHT, 0 escaped, rc 0. `txlaf-registrar-kept` is CAUGHT by both new checks; at dbba60e6 it ESCAPED (R913-1's receipt) |
| R913-1 probe | `txlaf_registrar_probe.py` (unchanged) in a copy | `findings=0 configs=[('AA', 'LV'), ('AA', 'MT')]`, the configurations the new check asserts |
| R914-1-F1 census | `python3 -I -B <r914-1>/probe_twin.py <worktree>` (unchanged) | executed 11 named checks, 11 distinct; then rc 1 at its line 22, `assert ... == 9`, the census it pinned at dbba60e6. With that one constant set to 11 (`selftest/probe_twin-adapt.diff`): rc 0, 72 table probes, 1492/1497 decoded boundary, 5 of 5 of its mutations caught |
| Census | `python3 -I -B round2/scripts/census.py <worktree>` | profile-hook count 11 = printed 11, names distinct, no hard-coded total in the source: AGREES, rc 0 |
| Round-1 planted faults | `python3 -I -B round2/scripts/r1_faults.py <worktree> <scratch>` | control PASS; 5 of 5 CAUGHT (old rLA! model, no txLAF!, no FourPacked, room 1499, MVRP walk off) |
| `make twin` (Verilator 5.050) | `make -j24 build-twin`, then `make twin` | rc 0; self-test `OK (11 checks)`; `twin: 0 finding(s)` |
| `make twin-plants` | `make -j2 twin-plants`, a single invocation | rc 0; 16 of 16 plants REFUSED, 32 refusals (each plant twice). Also run as two split invocations (3 sim plants / 13 capture plants): the same 16 and 32 |
| Python idiom gate | `python3 scripts/check_py_idiom.py`, `--selftest` | rc 0; 54 of 54 |
| `docs.yml` steps | `round2/scripts/docs_gates_r2.py`: the workflow's run scripts, em-dash as a push from `aa30d77f` | 44 steps, each rc 0 (`receipts/docs/summary.txt`). Em-dash: 0 findings over 26 added lines in 5 Markdown pages, 339 of 339 arms. TOC selftest 1501 of 1501, TOC gate OK. `docs_check.py` 0 findings, with and without git. `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `docs_inventory.py --check` and `ci_gate_workflows.py --check` pass |
| Image inputs | `git diff --stat dbba60e6..HEAD -- sw/firmware/ctrl/srp 'sw/firmware/ctrl/*.c' hdl configs third_party` | empty |
| Image identity | `plat_ledger.py --build-dir` at dbba60e6 and at ed7df79c, same worktree and tools | 28 of 28 ELF/bin/hex byte-identical, including `ctrl_app.elf` 1x1/1if `30e6ea03…`, 8x8/1if `c59a55a2…`, both 2if and the four harness images. Both PASS, 0 findings. The hashes equal round 1's head hashes |

## Acceptance (round-2 brief)

1. R913-1-F1: met. The self-test fails when the Registrar does not take the sLA's rLA! at txLAF!. The mutant
   `txlaf-registrar-kept` is CAUGHT, the other eight are still CAUGHT, and the control passes.
2. R914-1-F1: met. The census is counted at run time and the printed total equals the executed total (11). The
   PR body is corrected. The twin README states no number, now or before; it now says the count is the number
   of checks run. Historical round-1 receipts still read "OK (10 checks)": those are records of dbba60e6.
3. R913-1-S1: taken (docstring).
4. Gates: all of the above pass.
5. PR-BODY.md: round-2 copy, made from the live body.

Open risks/questions:

- The firmware gate, reproduction, budget model, harness, ledger self-test and OOC map were not re-run at this
  head. They stand from `402834ac`: since then only `twin_mrp.py`, the twin README and a docstring of
  `test_ctrl_firmware.py` changed, and the images are byte-identical.
- R914-1's `probe_twin.py` pins `== 9`. Rerun unchanged, it stops at that assert after printing the census. This is
  expected at the corrected head, not a regression.
