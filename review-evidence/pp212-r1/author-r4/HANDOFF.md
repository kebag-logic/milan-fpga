# HANDOFF — processor issue #212, round 4 ([A729d])

Status: REVIEW READY at `6162885`. Every round-4 gate is rc 0.

- Repository: processor (`origin` is the processor repository), branch `212-srp-presettle-talker`.
- Base of this round: round-3 head `834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1` (PR #213). Branch base: main `a9e84b66`.
- Head: `6162885ffee5d8e8897732be6479982b8dceaec9` (one commit on top, no rebase, no force). Nothing pushed.
- Assignment: the round-4 [A10] comment on issue #212. Its whole scope is Rule 11 of the parent's
  `docs/development/CODE_QUALITY.md`: split each multi-declarator declaration this PR added into one
  declarator per statement, make no other change, and run the listed gates.

## The change

| # | File:line (head) | Before (`834cc88`) | After | Reason |
|---|---|---|---|---|
| 1 | `tb/pp_top/sim_main.cpp:10619-10620` (`listener_is`) | `int e = -1, q = -1;` | `int e = -1;` / `int q = -1;` | Rule 11 (C++ Core Guidelines ES.10, one declaration per line) |
| 2 | `tb/pp_top/sim_main.cpp:10625-10626` (`listener_any`) | `int e = -1, q = -1;` | `int e = -1;` / `int q = -1;` | Rule 11 |
| 3 | `tb/srp_stream_fsms/sim_main.cpp:2895-2896`, used at `:2899` (PS12, `pre_registered_streams_keep_one_declaration_per_stream`) | `const int sinks[] = {0, 3};`, read as `sinks[0]`, `sinks[1]` | `const int sink_a = 0;` / `const int sink_b = 3;`, read as `sink_a`, `sink_b` | Rule 11: the checker's declaration pattern counts this one-declarator array initializer, because its line has a comma before the `;`. The issue comment names this file with 1 case. Two named scalars state the same two sinks with one declarator per statement |

All three were added by this PR (none is in `a9e84b66`). Test-bench C++ only: no HDL, campaign,
README or doc change, so no area, ROM or register-map effect. The checks and their values are the
same: PS12 still reads `h.l_decl(0) == 2 && h.l_decl(3) == 2`.

No new check, so no new planted mutant. The gate that refuses the defect is the parent's
`scripts/check_cpp_idiom.py`. At the round-3 pin it fails with
"FAIL: multi-declarator declaration 3 > ratchet 0. New C++ uses the named construct; see Rule 11 in
docs/development/CODE_QUALITY.md." (rc 1), and its `--list` names
`protocol-processor/tb/pp_top/sim_main.cpp multi-declarator declaration=2` and
`protocol-processor/tb/srp_stream_fsms/sim_main.cpp multi-declarator declaration=1`
(`receipts/parent/pin-834cc88-repro/`). At this head it passes (below).

## Processor gate table (head `6162885`)

The gates ran on a fresh clone of the head in scratch, with the pinned Verilator 5.050 and
`MAKEFLAGS=-j16`. Receipts: `receipts/processor/head-6162885/`.

| Gate | Result |
|---|---|
| `git diff --check 834cc88 6162885` (and of the working tree before the commit) | rc 0, no output |
| `tb/srp_stream_fsms` (`make`) | rc 0: **1,512 checks: 1,512 PASS, 0 FAIL** (round 3: 1,512) |
| `tb/pp_top` (`make`) | rc 0: **11,064 checks: 11,064 PASS, 0 FAIL** (round 3: 11,064) |

Both counts equal round 3's sweep row, so no check was lost or added. The suite logs had their
scratch and toolchain paths masked after the run; the raw logs' sizes and sha256 are in
`receipts/RAW-RECORDS.txt`.

## Scratch-parent consumer gate table (pin `6162885`)

The scratch parent is the one of rounds 1 to 3: milan-fpga dev `604899c0`, local branch
`pp212-consumer-gate`, push URL `DISABLED-never-push`, never pushed. A top-level identity check
preceded every git command inside `protocol-processor`. Two new local commits:
- `9b39ba29`: protocol-processor → `6162885`;
- `2d58400f`: its ROM digests through `./syn/yosys/ooc.sh --record-rom-digests` (sv2v v0.0.12,
  yosys 0.66), equal to main's and round 3's: ltn `23cc67ee…`, ucode `49a993be…`.

Receipts: `receipts/parent/pin-6162885/`.

| Consumer gate | Result |
|---|---|
| ROM digests (`./syn/yosys/ooc.sh --record-rom-digests`) | rc 0; both rows equal main's |
| `python3 scripts/check_cpp_idiom.py` | rc 0: 351 first-party translation units; `multi-declarator declaration: 0 <= 0`, every rule 0 |
| `python3 scripts/check_cpp_idiom.py --list` | rc 0: no per-file row (round-3 pin: the two rows above); summary `multi-declarator declaration: 0 <= 0` |
| `python3 scripts/check_cpp_idiom.py --selftest` | rc 0: 75 checks, 75 PASS, 0 FAIL |
| The same three, under CI's CPython 3.12.3 (`python3.12 -I`) | rc 0 each, the same output (`--list` byte-identical) |

`check_cpp_idiom.py` is added to the consumer gate list here; round 3's list did not run it. The
manager's run was on dev `cc204c6f`, which is not in this scratch parent. The checker at `604899c0`
gives the same refusal at the round-3 pin, with the same three cases.

The round-3 consumer gates (rtl-fast jobs and milan_dp) were not re-run: this round's assignment
replaces the full gate set, and the change is test-bench C++ inside two processor suites that the
parent does not build.

## Process notes

- The first ROM-digest run failed before reading anything: its `TMPDIR` did not exist yet
  (`mktemp: failed to create directory`). I created it and ran the recorder again from the start:
  rc 0. The failed run is in `receipts/superseded/rom-digests-missing-tmpdir/`.
- Tools: Verilator 5.050 (pinned), yosys 0.66, sv2v v0.0.12, CPython 3.14.8 and 3.12.3
  (`receipts/records/tool-versions.txt`). The suites ran one after the other in this unit, at
  `make -j16`. The unit's `memory.peak` was 5.35 GB, under the 10 GB working limit.
- The scratch head clone used for the suites is outside the lane. The lane's working tree is
  clean (`receipts/records/processor-records.txt`).
- `receipts/tools/gate.sh` is the one-gate recorder used here. It masks the scratch, toolchain
  and home paths in each recorded command.

## Not done (by the assignment's rules)

No push, no PR creation or edit, no merge or rebase, no comment edits, no hardware or bench
access, no sub-agents, no full sweep (this round's gates replace it).
