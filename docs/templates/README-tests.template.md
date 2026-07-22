# README-tests — `<module name(s)>` (TEMPLATE)

<!--
Gaps attack item 4, MERGED with the item-3 per-module spec-test
traceability subtask: every leaf module dir carries a README-tests.md
(this template) + README-parameters.md; each spec-family dir carries a
rolled-up index. The matrix row format below IS the traceability-matrix
row format (clause -> behavior -> test -> why) — rows here roll up 1:1
into the per-spec-family matrix, and (item 10) each confirmed row becomes
an executable behave scenario (CERT-harness pattern).
-->

Module(s): `<hdl/.../KL_x.sv>`
Testbenches: `<tb/verilator/<dir>/ …>`
Specs: `<IEEE 1722.1-2021 / 1722-2016 / 802.1Q-2018 / 802.1AS-2020 /
Milan v1.2 — list the ones this module implements>`

## Traceability matrix

<!-- One row per NORMATIVE behavior this module owns. Test column states
     the mechanism AND its status: existing (name the TB/test), tsn_gen
     (name the generator recipe), or MISSING. "Why" = why this test (or
     this gap) is the right verification for the clause — the reviewer
     (item 10 peer-validation) confirms rows one-to-one. -->

| Clause | Behavior | Test (existing / tsn_gen / MISSING) | Why |
|--------|----------|--------------------------------------|-----|
| `<spec §x.y.z>` | `<observable normative behavior>` | `<existing: tb/...  |  tsn_gen: recipe  |  MISSING>` | `<why this verifies the clause / why the gap matters>` |

## Non-normative / robustness tests

<!-- House additions beyond the spec (CDC drills, reset drills, counter
     W1C, silicon-lesson regressions). Same table, Clause = "house". -->

| Clause | Behavior | Test | Why |
|--------|----------|------|-----|

## How to run

```
<exact commands for the TB(s); note verilator/yosys targets>
```
