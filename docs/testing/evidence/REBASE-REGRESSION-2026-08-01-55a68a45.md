# REBASE REGRESSION — targeted gate record against 55a68a45

Status: **PASS (targeted rebase regression)**. Scope is exactly what is named
below: the lwSRP RTL family affected by the new base `3c82068d` (listener
counters / lwSRP walker) plus the BDD conformance layer. **This is NOT the full
55-suite Verilator sweep** and does not prove Linux boot, virtual-wire behavior,
or hardware timing.

## Contents

- **[Baseline](#baseline)** — the exact commits: HEAD `55a68a45` over base `3c82068d` (the listener-counter/walker RTL delta under test), 128-core host, Verilator 5.050.
- **[Commands and results](#commands-and-results)** — the five lwSRP Verilator suites plus behave, verbatim, with the per-gate table: 638 RTL checks and 520 BDD scenarios, every gate PASS exit 0.
- **[Verdict](#verdict)** — the rebase delta passes its targeted family; virtual-E2E gates were re-verified separately against the same commit.
- **[What this does not cover](#what-this-does-not-cover)** — the full 55-suite sweep, hardware timing/PHY, and the still-blocked T2/T3 virtual-wire gates.

## Baseline

- HEAD: `55a68a45` ("virtual e2e: runner, sim driver, docs, evidence")
- Parent/base: `3c82068d` (listener counters: Milan Table 5.6 interval
  semantics, walker yield) — the RTL delta under test
- Date: 2026-08-01. Host: 128-core, Verilator 5.050.

## Commands and results

```
for suite in lwsrp lwsrp_ctx lwsrp_rx lwsrp_switchpdu lwsrp_tx; do
  make -C tb/verilator/$suite clean >/dev/null && make -C tb/verilator/$suite -j$(nproc)
done
cd tests && behave -f plain
```

| gate | checks | result |
|---|---|---|
| lwsrp | (suite output) | PASS, exit 0 |
| lwsrp_ctx | 43 checks, 0 failures | PASS, exit 0 |
| lwsrp_rx (ingress+walker+registrar) | 143 checks, 0 failures | PASS, exit 0 |
| lwsrp_switchpdu | 7 checks, 0 failures | PASS, exit 0 |
| lwsrp_tx (applicant TX) | 445 checks, 0 failures | PASS, exit 0 |
| behave BDD | 42 features / **520 scenarios passed, 0 failed, 11 skipped** / 3166 steps passed | PASS, exit 0, 3.5 s |

No new dirty-tree artifacts beyond the existing untracked build/log dirs.
Toolchain notes: existing per-suite Verilator flags; no `--threads-dpi` (these
harnesses are `--exe` C++ over UNIX sockets, no DPI imports).

## Verdict

The rebase delta (`3c82068d` listener counters / lwSRP walker) passes its
targeted RTL regression family and the full BDD conformance layer at HEAD
`55a68a45`. The virtual-E2E gates (T0/T1, BLOCKED T2/T3) were separately
re-verified against the same commit — see [`VIRTUAL_E2E_TEST_PROCEDURE.md`](../VIRTUAL_E2E_TEST_PROCEDURE.md) §3.

## What this does not cover

- Full 55-suite Verilator sweep (run [`scripts/run_all_suites.sh`](../../../scripts/run_all_suites.sh) for that).
- Vivado/P&R timing, PHY, analog — hardware-only.
- T2/T3 virtual-wire behavior — blocked on engineering tasks (RAM model,
  wire attachment, two-node bridge).
