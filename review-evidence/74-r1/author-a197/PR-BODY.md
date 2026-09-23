[A197]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `6d1572d6caeb94cd3dd871b9df90e4c5298998b6`. On pinned Verilator 5.050:

- `media_grid_align`: 45/45, and all three negative controls fail as required.
- `chmap_capture`: 204/204, plus the netlist leg at 20/20.
- `milan_dp` `aclk`: 139/139, with output byte-identical to a base build of the same leg.

Branch `74-junction-chatter` -> `dev`, one commit on `ede8d48e`.

## Linked Issue / roles

Relates to #74
<!-- #74 stays open: ledger items 1 and 4 are bench lines, item 3 is another lane. This PR closes item 2 only. -->

Executor: `[A197]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

#74 ledger item 2, from PR #323's [R1] finding 1: the TDM junction counter chattered phantom dups at a slip-free lock whenever the frame marker raced onto the tick. The mechanism choice is recorded in the [A197] DECISION on #74.

| Piece | Change |
|---|---|
| `hdl/ieee1722/crf/KL_media_grid_align.sv` | **Lock-phase keep-off.** The engagement capture, which is the lock target, is clamped into `[LOCK_KEEPOFF_CYC_P, DIV_C - LOCK_KEEPOFF_CYC_P]` cycles after the tick. The default is `DIV_C/128`: 16 cycles, 1/128 sample. A capture already that far from both ticks is used bit for bit. A raced capture is pulled at most the keep-off, which is half the root's 1/64-sample settle band. The new parameter is defaulted, and an elaboration guard refuses a keep-off that leaves no target. |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | **Coincidence branch.** When a tick and a marker land in the same cycle, the tick now takes the pending marker if there is one, and the coincident marker pends in its place (`pend` carries over). The old branch cleared `pend` and dropped a marker without counting it. The KNOWN CAVEAT banner is replaced by the law and the measured failure it fixes. |
| `tb/verilator/media_grid_align` | The wrap instantiates the **real** `KL_chan_map_capture` on the loop's frame marker and tick, wired as `milan_datapath` wires them. New arms: [G7] is a lock raced ON the tick, with one edge of marker delivery jitter; it runs 8 x 0.2 s windows, measures clearance, and injects a held frame and a surplus frame at that lock. [G8] is a lock raced from just below the tick. [G9] is one slow free-running passage in each direction. New mutants `MGA_MUT_NO_KEEPOFF` and `MGA_MUT_COIN` must each fail on their own arm. The C++ copy of the law follows the new coincidence line. |
| `tb/verilator/chmap_capture` | [T0] gains three directed checks: a coincidence over a pending frame carries it over (no dup after it), a frame over a carried frame is a skip, and nothing is left behind. |
| Docs | `REGISTER_MAP.md`: the `SLIP_TDM` paragraph replaces the false "false-alarm only, never a hidden slip" caveat. `TIME_SYNC.md`: Media boundary row for the lock target. `TESTING.md`: suite row. The bench README. |

Why both halves, from measurements on the base (`ede8d48e`, branch harness, real RTL counters):

- **Raced lock at the base:** G7 windows of {0, 0, 771, 2351, 2431, 1980, 1694, 1701} dups. At that lock a held frame counts 73 dups and 36 skips, and a surplus frame counts 13 skips and 21 dups.
- **Free-running at the base:** a slow passage counts 10 dups instead of 1. A fast passage counts **0 skips and 9 dups**, so a skip-direction slip is hidden and inverted. In a 12 s scratch run: 74 dups for about 6 real slips one way, and 65 dups with 0 skips the other way.
- **Counter fix alone** (`MGA_MUT_NO_KEEPOFF`): free-running is exact, but a raced lock with one edge of delivery jitter counts 994 to 1,421 dup/skip pairs per 0.2 s.
- **Keep-off alone** (`MGA_MUT_COIN`): the lock is clean, but the free-running passage still counts 11 dups.
- **Both (this PR):** zero junction counts over 8 x 0.2 s at the raced lock, the marker at least 15 cycles off every tick, a held frame is exactly 1 dup, a surplus frame exactly 1 skip, and each free-running passage counts exactly once in its direction.

Hysteresis was rejected (see the DECISION). A band around the tick makes the marker-to-tick association ambiguous, so a step slip inside the band would go uncounted.

## Authoritative references

- #74 reopening ledger, item 2: https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5507453907
- PR #323 [R1] finding 1: https://github.com/kebag-logic/milan-fpga/pull/323#issuecomment-5506033067
- [A197] DECISION on #74: https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5794560116
- `docs/design/TIME_SYNC.md` Media boundary. `docs/reference/REGISTER_MAP.md` `0x8D4` section (`SLIP_TDM`).

## How to get into the same state

```sh
git fetch origin
git checkout 6d1572d6caeb94cd3dd871b9df90e4c5298998b6
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
verilator --version   # Verilator 5.050
```

## How to validate

```sh
make -C tb/verilator/media_grid_align
make -C tb/verilator/chmap_capture
make -C tb/verilator/milan_dp aclk
python3 scripts/lint_rtl.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/measure_naming.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
```

Expected result / pass criteria:

- `media_grid_align`: `45 checks, 0 failures`, followed by three lines:
  - `MGA_MUT_U_SIGN: RED` in [G2];
  - `MGA_MUT_NO_KEEPOFF: RED` on `[FAIL] G7: zero junction dups ...`;
  - `MGA_MUT_COIN: RED` on `[FAIL] G9: ...`.
- `chmap_capture`: `204 checks, 0 failures`, and netlist `20 checks, 0 failures`.
- `aclk`: `139 checks, 0 failures`.
- Lint: `PASS (90 <= 90)`.
- xvlog: `PASS`, with 0 findings in `hdl/`.
- Docs gates exit 0; the em-dash gate reports 0 findings.

Local results are at the [A197] REVIEW READY comment on #74.

## Known limitations / out of scope

- **Acquisition can still count.** The keep-off steers the lock target, not the acquisition transient. From a capture within the loop's transient reach of a tick (about 4 cycles per ppm of grid offset), acquisition crosses the tick and comes back. With delivery jitter those crossings count balanced dup/skip pairs during acquisition: [G8] prints 84/84. The lock itself counts nothing.
- **Passage exactness has a limit.** A free-running passage counts exactly once while the marker dithers over two adjacent cycles. A wider dither adds balanced dup/skip pairs, and the net stays exact.
- **Top-level jitter is modelled, not measured.** The unit loop models the root's capture-FIFO pop as 0 or 1 edge of random delivery delay. The width of the top-level marker jitter is not measured on silicon; the ledger's bench items 1 and 4 remain.
- **No VERSION bump.** VERSION lives in `hdl/common/csr/milan_csr.sv`, which is outside this lane. `SLIP_TDM` now counts a free-running slip once, in its direction; it used to count about a dozen dups per slip. That wants a release note when the maintainer cuts the next VERSION.
- **Full banks not run.** The parent, protocol-processor, gPTP, Yosys and builder banks were not run in this lane, by instruction. Hosted CI and candidate-merge validation remain part of the merge bar.
- **Declarations.** New declarations (`KEEP_LO_C`, `KEEP_HI_C`, `ref_keep_w`) are declared before use and carry no declaration-with-initialiser split, the construct no gate covers.
- **Scope.** Items 1, 3 and 4 of the #74 ledger are not in this PR.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (item 2 of the #74 ledger; the Issue stays open for items 1, 3 and 4)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (touched suites and gates green; full banks not run in this lane)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
