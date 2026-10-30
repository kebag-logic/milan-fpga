# Sampling ledger: docs/guides/VERIFICATION_DEVELOPER.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 25 | row | \| C with Python \| Shipping trace producer \| `python3 sw/trace/test_trace_roundtrip.py` \| | command 1 | ok: sw/trace/test_trace_roundtrip.py exists (auto) |
| 49 | sentence | C has no general harness framework. | - | F: D0-027 |
| 74 | item | C never judges its own correctness. | - | ok: sw/trace/test_trace_roundtrip.py decodes the C producer's output in Python (lines 71-73 context) |
| 91 | item | Add boundary and reset cases. | - | policy |
| 97 | item | Confirm the mutation fails. | - | policy: AGENTS.md Tests lens |
| 100 | sentence | Never count an unobserved behavior. | - | policy |
| 106 | code | ```sh make -C tb/verilator/cdc ``` | command 1 | ok: tb/verilator/cdc/Makefile (auto) |
| 112 | code | ```sh suite_logs=$(mktemp -d) scripts/run_all_suites.sh "$suite_logs" ``` | command 1 | ok: scripts/run_all_suites.sh writes <outdir>/<suite>.log (header line 14) |
| 119 | code | ```sh cd tests behave -f plain ``` | - | ok: tests/behave.ini, tests/environment.py, tests/features/ |
| 128 | code | ```sh python3 sw/litex/test_gmii_rx_capture.py ``` | command 1 | ok: sw/litex/test_gmii_rx_capture.py in scripts/run_litex_sims.sh INVENTORY (round-1 fix) |
| 134 | code | ```sh protocol-processor/scripts/run_suites.sh make -C gptp-processor ``` | command 2 | ok: protocol-processor/scripts/run_suites.sh and gptp-processor/Makefile (auto) |
| 141 | code | ```sh python3 sw/trace/test_trace_roundtrip.py ``` | command 1 | ok: as line 25 |
| 155 | item | Re-run only the failing suite. | - | policy |
| 157 | item | Compare accepted transfers only. | - | policy |
| 158 | item | Check reset and clock sequencing. | - | policy |
| 162 | item | Never convert unknown results into passes. | - | policy |
| 168 | item | [Link-guard reset](../diagrams/wd_linkguard_reset.svg) | path 1 | ok: docs/diagrams/wd_linkguard_reset.svg exists (auto) |
| 174 | item | Record every exact command. | - | policy |
| 180 | item | Link every finding to an artifact. | - | policy |
| 182 | sentence | Green output alone never proves correctness. | - | policy |
