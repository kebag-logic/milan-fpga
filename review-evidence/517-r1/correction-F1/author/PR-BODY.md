[A183]

The ordinary simulation pool could remain blocked in stdout replay after INT or TERM, leaving owned simulations alive. The correction records ordered output on disk and makes stdout delivery interruptible. Cancellation kills and reaps owned simulations before attempting only immediately writable output; complete/partial per-leg files and the ordered transcript remain attributable. Normal replay preserves every binary byte and legacy order.

The ten commands, two-child ceiling, exclusive ordered five-leg sim_nxn group and presence-based whole-set frame serialization remain unchanged. Build, prerequisite, render, model, processor-pin, policy and budget bytes are unchanged. No #523 driver change is included.

Local unpublished head: `ff7dac3257a321538a1fd1a310ab3190f646153d`. Original 17 runner and 24 phase arms pass, as do 28 new direct/actual-Makefile backpressure controls. Eight restored-original-defect controls fail specifically before consumer drain. Relevant focused gates and selftests pass.

Fresh same-head complete-suite measurements with Verilator 5.050, eight jobs/CPUs and a 12 GiB limit:

| Full suite | Sequential seconds | Two-worker seconds | Saved seconds | Observed gain |
|---|---:|---:|---:|---:|
| Cold | 1133.031 | 1095.719 | 37.312 | 3.293% |
| Warm | 980.614 | 933.414 | 47.200 | 4.813% |

Every run passed 9324 checks with zero failures, 13 tallies and the same 23 render identities. Per-leg bytes, input/executable identities and tracked headers match. Cold means suite build cleanup; warm retains same-mode artifacts. One pair per temperature supports these observed local gains, not a guaranteed or hosted percentage. Raw logs, samples, exact receipts and integrity proofs accompany HANDOFF.md.

R245 F1 remains open under all five original lenses pending independent re-review. R246 external review and manager full-bank, act, hosted timing/gates and current-candidate work remain required. This body is a handoff artifact; the draft PR has not been edited.

Closes #517
