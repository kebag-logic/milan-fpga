[A551]

## Contents

- **[Status](#status)** -- Candidate and validation result.
- **[Linked Issue / roles](#linked-issue--roles)** -- Task and independent reviews.
- **[Description](#description)** -- Startup admission and regression checks.
- **[Authoritative references](#authoritative-references)** -- Governing clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and dependencies.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Authorized exception and remaining work.
- **[Definition of Done](#definition-of-done)** -- Completion obligations.

## Status

Local validation complete under ruling 6012843714: 60/60 default suites and 58/58 portability tops pass; both aggregates return zero. Independent review and the manager bench repeat remain pending.

Local candidate `5d6164a2da2d4f7374558bf33b464bcd8a9b4fc2` on
`667-talker-start` toward `dev`, based on `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
No implementation change was needed during the resumed validation.

The startup sweep passes 34020 checks across 486 starts and 4860 PDUs.
All eight new mutants are caught. Every first timestamp step is 125000 ns.
The packetizer's own OOC area is -4 LUTs / 0 FFs, within the assigned limit.
Complete datapath area is +77 LUTs / +14 FFs; the unchanged processor subtree
accounts for +91 LUTs. Excluding both processor subtrees, the datapath delta
is -14 LUTs / +14 FFs. All measurements remain disclosed.

## Linked Issue / roles

Closes #667
Relates to #657

The manager retains the B13-style bench repeat after merge and flashing.

Executor: `[A551]`
Internal cleared-context reviewer: `[R514]`
External reviewer: `[R515]`

## Description

An enable arriving after channel pair zero skipped timestamp capture while
the last pair advanced the first-sample counter. The first PDU then read the
previous stream's timestamp from TCTX w4. The base reproduction shows a
-494821316 ns first step, followed by 125000 ns steps with tv=1 and consecutive
sequence numbers.

One admission flag per talker now holds capture until that talker's pair zero
after reset or disable. The first complete sample follows the existing PHC
plus presentation-offset capture path. The RTL change is eight added lines.
Ports, register maps and parameter declarations are unchanged.

The default AAF suite grades every first PDU, payload/sample identity,
sequence wrap, validity, bounded arrival, reset, re-enable and backpressure.
Eight independent planted defects demonstrate those checks. The timing
contract and suite documentation describe the boundary and its limits.
Every existing exact-text mutation site planted before the RTL edit.

## Authoritative references

- #667 assignment comment 6011846710 and continuation ruling 6012843714.
- PR #676, `docs/findings/667_TALKER_START_BENCH.md` on its branch.
- B12 in `docs/findings/653_DISCONNECT_ORDER_BENCH.md`.
- IEEE 1722-2016 4.3.2, 4.4.4.5, 4.4.4.9, 7.3.5 and 7.5.
- Milan v1.2 4.4.2.1 and 5.3.8.10, Table 5.6.
- `docs/design/TIME_SYNC.md` and `docs/design/MEDIA_CLOCK_FOLLOWING.md`.

IEEE 1722-2016 7.5 governs normal-mode AAF timestamp validity and first-sample
presentation time. The assignment's 5.4.4 and 7.3.4 citations concern other fields.

## How to get into the same state

```sh
git checkout --detach 5d6164a2da2d4f7374558bf33b464bcd8a9b4fc2
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
: "${SCRATCH:?set physical scratch outside the checkout}"
: "${VERILATOR:?select the pinned 5.050 executable}"
export VERILATOR TMPDIR="$SCRATCH" SIM_JOBS=2 VERILATOR_JOBS=4 MAKEFLAGS=-j16
export PATH="$(dirname "$VERILATOR"):$PATH"
```

Use the repository-pinned HDL simulator release 5.050, an existing configured
builder environment, and the wire-field generator pinned at
`deca300c9eb4863fa13383b45ba6cb6fd0828671`. Export the respective executable and
dependency variables. Set `SIM_JOBS=2` to respect the ordinary simulation pool ceiling.
Set `SCRATCH` and `TMPDIR` to physical scratch storage
outside the checkout. Use initialized isolated checkouts for concurrent banks.

## How to validate

```sh
make -j16 -C tb/verilator/aaf startup-mutants START_MDIR="$SCRATCH/startup"
bash scripts/run_all_suites.sh "$SCRATCH/suite-logs"
python3 scripts/suite_tally.py "$SCRATCH/suite-logs" --quiet --expect-suite-root tb/verilator
bash syn/yosys/run.sh --results "$SCRATCH/portability-results"
bash syn/yosys/run.sh --list > "$SCRATCH/expected-tops.txt"
python3 scripts/yosys_tally.py "$SCRATCH/portability-results" --expected "$SCRATCH/expected-tops.txt" --require-structural
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
make -j16 -C tb/verilator/milan_dp gmstep-mutants
make -j16 -C tb/verilator/milan_dp gsi-mutants
make -j16 -C tb/verilator/milan_dp unb-mutants
make -j16 -C tb/verilator/milan_dp crflic-mutants
make -j16 -C tb/verilator/milan_dp_render tdm8render-mutants
make -j16 -C tb/verilator/milan_dp_render tdm8render-law-boundary LAW_BOUNDARY_JOBS=16
```

Run the datapath campaign targets separately when they share a build directory.
The --list command derives the expected-top inventory; retain it with the logs.
The complete command/receipt inventory, phase sweep, first ten red PDUs,
mutant failures and OOC recipe are in the handoff packet.

| Gate | Result |
|---|---|
| Full default inventory | 60/60 suites; 2184191 checks; zero failures, skips or timeouts |
| Portability inventory | 58/58 tops; structural checks pass |
| Both aggregates | rc 0 |
| Startup sweep and mutants | 34020 checks; 8/8 caught |
| Datapath, render and mclk suites; explicit campaigns | rc 0, except the authorized full-render findings below |
| Physical-rate simulation and accounting controls | 139 + 40 checks; rc 0 |
| Render boundary campaign | 81/81 diagnostic rounds; rc 0 |
| Builder, native banks, standalone simulations, behavior layer and static gates | rc 0; builder calibration limit below |
| Before/after OOC | rc 0 / 0; own logic within assigned threshold |

The full render campaign has the same 28/32 passing judgments at base and head.
All 32 run stdout files and return codes are byte-identical. The raw campaign
returns 1 at both revisions; the independent equality check returns 0.
The four existing campaign findings are the clean epoch control, its two
clean skew controls, and the surviving uncounted-repeat mutant. The survivor
remains a coverage gap and is not claimed fixed.

The clean `--epoch-only` run has four T30 CRF recentre failures in 114 checks,
at `sim_tdm8_render.cpp:3408`, `:3411`, `:3413` and `:3428`. Both complete stdout
files are 3745 bytes with SHA-256
`7876a3a277df5e06a9381e502249b9638b7a4e04ec676fefba207150b41d4007`.
This satisfies ruling 6012843714's base-equality condition. The historical
#657 hash `8f6ebaae...` used processor pin `631eeb34`; both assigned-base and
candidate runs use `ead80360`. Historical hash equality is not claimed.
The first resumed sweep refused an inherited four-job simulation setting.
The full default inventory was repeated in disjoint shards with the supported
two-job ceiling; the failed setup attempt remains retained. No assertion, campaign judgment or
acceptance criterion was weakened.

## Known limitations / out of scope

- The packetizer-boundary sweep drives post-bind enable; it does not exercise ACMP traffic.
- The authorized #657 exception and surviving mutant remain open work.
- The builder bank returns zero with required elaboration and firmware arms; optional gate 11 calibration is NOT RUN because its historical placement report is absent.
- OOC reports measure synthesis area, not routed timing sign-off.
- Hosted checks, independent reviews and candidate-merge validation remain pending.
- The manager repeats the physical bench starts after merge and flashing.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including the manager's bench read
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes under the recorded #657 ruling
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
