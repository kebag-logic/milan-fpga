[A574]

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

Local gates complete; hosted timing and independent reviews pending. `657-render-mutants` -> `dev`.
Head: `62c261c2d1b899a9cf90c901b25b5a85846dfef6`.
Baseline: 30/34, rc 2, with exactly the four reported failures.
Final campaign: 34/34, rc 0, 7243.92 s: original 32/32 plus both PR #672 additions.
Cold default: rc 0 in 809.21 s on four CPUs; shipping 266/266, multi-stream 71/71, default controls 5/5.
Pull-in: 19/19 legs, 838 checks, zero failures, rc 0. Builder and documentation gates returned rc 0.

## Linked Issue / roles

Relates to #657.
Executor: `[A574]`.
Internal cleared-context reviewer: `[R568]`.
External reviewer: `[R569]`.

## Description

The shortened epoch-only history starts its CRF checks during boot pull-in.
The correction gives it the existing bounded boot dwell and keeps
all four exact recentre expectations.

The nominal serial feed produces no repeats, so freezing the underrun
counter survives the old check. A bounded double-rate audio/serial-clock
burst forces repeats through the real serializer. The new check requires
actual repeats, intact pin-frame identities, and one counter increment per
repeat. It runs after the clock-law checks while the listener is bound.
The campaign names that check and retains every inherited arm.

The documentation records the precondition and manager merge-bank ownership.
The complete campaign passes all retained controls and catches every named mutant.

## Authoritative references

- Issue #657, assignment comment 6082915356.
- Issues #643, #645 and #647; PR #672.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md`, boot pull-in and settle recentre.
- `docs/design/TIME_SYNC.md`, listener render latency.
- IEEE 1722-2016, clauses 4.4.4.3, 10.4.3 and 10.6.

## How to get into the same state

Use the recorded head and initialized simulation dependencies. After the
manager publishes the branch, fetch it in a separate review checkout.
Set `SCRATCH` outside the checkout, `PINNED_COMPILER` to release 5.050,
and `FOUR_CPUS` to four available CPUs. Use a Python environment satisfying
`tools/markdown/requirements.txt`, the required RV32 compiler, and the
patched elaboration environment. Set `MARKDOWN_ENV`, `RV32_BIN` and
`ELABORATION_PYTHON` to those existing installations; keep the HDL conversion
executable on `PATH`.

```sh
git fetch origin 657-render-mutants
git switch --detach 62c261c2d1b899a9cf90c901b25b5a85846dfef6
git submodule update --init --recursive protocol-processor gptp-processor third_party/verilog-axis third_party/lwSRP
export PATH="$MARKDOWN_ENV/bin:$RV32_BIN:$PATH"
export MILAN_LITEX_PYTHON="$ELABORATION_PYTHON"
mkdir -p "$SCRATCH"
export TMPDIR="$SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export VERILATOR="$PINNED_COMPILER"
export VERILATOR_JOBS=2
```

## How to validate

```sh
make -C tb/verilator/milan_dp_render clean
env -u MAKEFLAGS taskset -c "$FOUR_CPUS" make -C tb/verilator/milan_dp_render
make -C tb/verilator/milan_dp_render tdm8render-mutants
make -C tb/verilator/milan_dp_render tdm8render-pullin PULLIN_JOBS=4
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_py_idiom.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee
```

Expected: every clean mode passes and every mutant fails its named check.
The inherited inventory is the original 32 checks plus two from PR #672.
All 34 pass. The pull-in gate passes all 18 boot phases and the full-history leg. The cold default retains its complete population and all 18 LAW phases. The builder bank returned rc 0 in 1169.34 s; its historical calibration limit is recorded below. All 41 applicable documentation/source commands, five timing-document follow-ups and the committed-head added-line gate returned rc 0. The added-line gate also passed all 339 planted arms.

The complete source/documentation command list is recorded in the
[A574] REVIEW READY comment on #657.

## Known limitations / out of scope

- Hosted timing requires publication by the manager. The local cold result has 630.79 s margin to the 1440 s line and 990.79 s to the 1800 s guard; it does not establish hosted acceptance.
- Independent reviews, candidate validation and merge remain pending.
- No RTL or hardware work is included.
- The four initialized dependencies match their pins. The separate `external`
  entry is uninitialized, with its gitlink unchanged; the required gates
  passed in that state.
- The builder bank passed its RV32 and elaboration requirements. Its
  historical placed-report calibration was unrun because the reference
  report is absent; no calibration evidence is claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
