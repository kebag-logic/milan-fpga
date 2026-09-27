[A363] REVIEW READY — Round 2

Commit: `ff75a70807c151517860c73a06d7ea36e2a46008` (local `397-service-budget`; prepared for manager publication).
Refs #397. This is author validation evidence; independent re-review remains pending.

Changed: passive retired-entry observation, per-duty no-tick spans and conditional heartbeat bounds; named UART-paced, queued-input and device-wait plans; exact heartbeat-gap endpoints and backing samples; tighter AEM markers and the 20 s boot comparison; separate device-max waits and early refusal; fixed-trace/mutation controls and an independent busy-refusal test. Raw run receipts now live in the evidence packet, with complete-file hashes in `docs/findings/397_SERVICE_BUDGET.md`. Firmware, RTL, submodule pins and the entire capture harness are unchanged.

Round-2 acceptance: the assigned measurement and documentation corrections are implemented. Every current duty has a marker or enclosing interval; no STOP condition applies. Queued-input liveness failures remain present and are recorded below; their firmware repair is #590. Future duties, board torture and the complete hart decision remain open on #397.

### Updated duty budgets

The following are maxima over the four executed plans at 50 MHz. CPU cycles are elapsed cycles, not retired-instruction counts. AEM timing runs from the first accepted read address at its offset through entity enable. Boot still excludes BIOS CRC, startup delays and memory testing; its 20,000 ms comparison is the ADP validity window, not a complete physical startup proof. N/A means no separate assigned deadline for that envelope.

1x1:

| Duty | Plan at maximum | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | `uart-paced` | 18,698,731 | 373.97461 | 20,000 | 19626.02539 |
| AEM copy/CRC | `uart-paced` | 2,899,797 | 57.99594 | N/A | N/A |
| Binding restore walk | `all` | 1,138 | 0.02276 | 3,000 | 2999.97724 |
| Journal erase envelope | `device-wait` | 151,005,855 | 3020.11709 | 3,500 | 479.88291 |
| Journal START-to-ACK | `device-wait` | 161,067,660 | 3221.35320 | 8,000 | 4778.64680 |
| `milan_status` | `uart-paced` | 1,448,542 | 28.97083 | 500 | 471.02917 |
| `milan_gettime` | `uart-paced` | 265,586 | 5.31171 | 500 | 494.68829 |
| `milan_settime`, maximum tested case | `uart-paced` | 510,995 | 10.21989 | 500 | 489.78011 |
| `milan_utc`, maximum tested case | `uart-paced` | 605,880 | 12.11759 | 500 | 487.88241 |
| `milan_nvm` status | `uart-paced` | 11,682,149 | 233.64297 | 500 | 266.35703 |
| `milan_nvm commit` | `device-wait` | 166,979,731 | 3339.59461 | 8,000 | 4660.40539 |
| `milan_nvm wipe`, whole command | `uart-paced` | 2,472,810 | 49.45619 | N/A | N/A |
| Wipe erase envelope, maximum of two | `uart-paced` | 1,448,160 | 28.96320 | 3,500 | 3471.03680 |
| `milan_nvm invalid` | `uart-paced` | 273,914 | 5.47827 | 500 | 494.52173 |

8x8:

| Duty | Plan at maximum | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | `uart-paced` | 54,724,259 | 1094.48517 | 20,000 | 18905.51483 |
| AEM copy/CRC | `uart-paced` | 6,850,696 | 137.01392 | N/A | N/A |
| Binding restore walk | `uart-paced` | 2,706 | 0.05412 | 3,000 | 2999.94588 |
| Journal erase envelope | `device-wait` | 153,725,874 | 3074.51747 | 3,500 | 425.48253 |
| Journal START-to-ACK | `device-wait` | 192,836,355 | 3856.72710 | 8,000 | 4143.27290 |
| `milan_status` | `uart-paced` | 1,448,542 | 28.97083 | 500 | 471.02917 |
| `milan_gettime` | `uart-paced` | 265,595 | 5.31189 | 500 | 494.68811 |
| `milan_settime`, maximum tested case | `uart-paced` | 510,995 | 10.21989 | 500 | 489.78011 |
| `milan_utc`, maximum tested case | `uart-paced` | 605,880 | 12.11759 | 500 | 487.88241 |
| `milan_nvm` status | `uart-paced` | 40,703,945 | 814.07889 | 500 | -314.07889 |
| `milan_nvm commit` | `device-wait` | 215,384,150 | 4307.68299 | 8,000 | 3692.31701 |
| `milan_nvm wipe`, whole command | `uart-paced` | 7,910,620 | 158.21239 | N/A | N/A |
| Wipe erase envelope, maximum of two | `uart-paced` | 4,167,030 | 83.34060 | 3,500 | 3416.65940 |
| `milan_nvm invalid` | `uart-paced` | 273,914 | 5.47827 | 500 | 494.52173 |

### Heartbeat opportunity bounds

Each conditional bound is the maximum measured no-tick span plus 250 ms phase and the maximum full containing-command UART TX allowance. Those maxima can come from different plans. Paced intervals already include TX blocking, so the added allowance is conservative. A negative conditional margin alone is not an observed violation. Queued input can chain duties and suppress the idle hook; the schedule results below demonstrate that case directly.

1x1:

| Duty | Longest no-tick span ms | Plan at maximum | TX allowance ms | Conditional period ms | 500 ms margin | 2,000 ms margin |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 312.73952 | `uart-paced` | 0.00000 | Unarmed prefix | N/A | N/A |
| AEM copy/CRC | 57.99594 | `uart-paced` | 0.00000 | 307.99594 | 192.00406 | 1692.00406 |
| Binding restore walk | 0.01111 | `all` | 0.00000 | 250.01111 | 249.98889 | 1749.98889 |
| Journal erase envelope | 20.14069 | `device-wait` | 9.89583 | 280.03652 | 219.96348 | 1719.96348 |
| Journal START-to-ACK | 121.19479 | `device-wait` | 9.89583 | 381.09062 | 118.90938 | 1618.90938 |
| `milan_status` | 15.54534 | `uart-paced` | 28.47222 | 294.01756 | 205.98244 | 1705.98244 |
| `milan_gettime` | 2.31391 | `all` | 5.20833 | 257.52224 | 242.47776 | 1742.47776 |
| `milan_settime`, maximum tested case | 5.17229 | `all` | 8.50694 | 263.67923 | 236.32077 | 1736.32077 |
| `milan_utc`, maximum tested case | 5.97003 | `all` | 9.46181 | 265.43184 | 234.56816 | 1734.56816 |
| `milan_nvm` status | 220.48254 | `uart-paced` | 32.55208 | 503.03462 | -3.03462 | 1496.96538 |
| `milan_nvm commit` | 137.09021 | `all` | 9.89583 | 396.98604 | 103.01396 | 1603.01396 |
| `milan_nvm wipe`, whole command | 40.34359 | `all` | 11.54514 | 301.88873 | 198.11127 | 1698.11127 |
| Wipe erase envelope, maximum of two | 20.39232 | `uart-paced` | 11.54514 | 281.93746 | 218.06254 | 1718.06254 |
| `milan_nvm invalid` | 1.96577 | `all` | 5.38194 | 257.34771 | 242.65229 | 1742.65229 |

8x8:

| Duty | Longest no-tick span ms | Plan at maximum | TX allowance ms | Conditional period ms | 500 ms margin | 2,000 ms margin |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 954.12026 | `uart-paced` | 0.00000 | Unarmed prefix | N/A | N/A |
| AEM copy/CRC | 137.01392 | `uart-paced` | 0.00000 | 387.01392 | 112.98608 | 1612.98608 |
| Binding restore walk | 0.01111 | `all` | 0.00000 | 250.01111 | 249.98889 | 1749.98889 |
| Journal erase envelope | 74.51875 | `device-wait` | 9.98264 | 334.50139 | 165.49861 | 1665.49861 |
| Journal START-to-ACK | 470.23145 | `device-wait` | 9.98264 | 730.21409 | -230.21409 | 1269.78591 |
| `milan_status` | 15.54488 | `uart-paced` | 28.47222 | 294.01710 | 205.98290 | 1705.98290 |
| `milan_gettime` | 2.32535 | `all` | 5.20833 | 257.53368 | 242.46632 | 1742.46632 |
| `milan_settime`, maximum tested case | 5.17229 | `all` | 8.50694 | 263.67923 | 236.32077 | 1736.32077 |
| `milan_utc`, maximum tested case | 5.97003 | `all` | 9.46181 | 265.43184 | 234.56816 | 1734.56816 |
| `milan_nvm` status | 800.91654 | `uart-paced` | 32.72569 | 1083.64223 | -583.64223 | 916.35777 |
| `milan_nvm commit` | 523.18408 | `uart-paced` | 9.98264 | 783.16672 | -283.16672 | 1216.83328 |
| `milan_nvm wipe`, whole command | 148.49474 | `uart-paced` | 11.54514 | 410.03988 | 89.96012 | 1589.96012 |
| Wipe erase envelope, maximum of two | 74.76972 | `uart-paced` | 11.54514 | 336.31486 | 163.68514 | 1663.68514 |
| `milan_nvm invalid` | 1.96577 | `all` | 5.38194 | 257.34771 | 242.65229 | 1742.65229 |

### Executed schedules and liveness

| Shape / plan | Largest observed gap ms | 500 ms margin | 2,000 ms margin | Gap endpoints ms | Final tail? | Printed backing samples |
| --- | ---: | ---: | ---: | --- | --- | --- |
| 1x1 / `all` | 430.62305 | 69.37695 | 1569.37695 | 942.86687 to 1373.48992 | Yes | 1, 1, 1, 1, 1 |
| 1x1 / `uart-paced` | 332.34992 | 167.65008 | 1667.65008 | 312.74513 to 645.09505 | No | 1, 1, 1, 1, 1 |
| 1x1 / `queued-input` | 2569.49201 | -2069.49201 | -569.49201 | 252.58315 to 2822.07516 | Yes | 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 |
| 1x1 / `device-wait` | 250.00968 | 249.99032 | 1749.99032 | 252.58315 to 502.59283 | No | 1 |
| 8x8 / `all` | 1449.77764 | -949.77764 | 550.22236 | 3390.63747 to 4840.41511 | No | 1, 1, 1, 1, 1 |
| 8x8 / `uart-paced` | 991.91598 | -491.91598 | 1008.08402 | 954.12589 to 1946.04187 | No | 1, 1, 1, 1, 1 |
| 8x8 / `queued-input` | 2513.33593 | -2013.33593 | -513.33593 | 893.96257 to 3407.29850 | Yes | 1, 1, 0, 0 |
| 8x8 / `device-wait` | 588.61054 | -88.61054 | 1411.38946 | 893.96257 to 1482.57311 | No | 1 |

Both queued-input runs exceed the 2,000 ms liveness interval and print backing zero. Final tails are right-censored at the last prompt. The independent public 8x8 observer also sees backing clear directly, with final alive zero/stale one. Isolated commands and long-WIP polling do not establish liveness under arbitrary queued input.

Device-max runs execute 3 s erase and 5 ms page waits. Both erase intervals contain twelve heartbeat writes, with maximum spacing 250.00068 ms. The whole commits take 3339.59461 ms and 4307.68299 ms; their START-to-ACK brackets take 3221.35320 ms and 3856.72710 ms. SPI substitution remains optimistic and these runs are not physical twofold-margin proof.

### Validation

All 19 required local gate commands returned rc 0 on the candidate head. The full builder bank reports one calibration arm NOT RUN because its physical utilization report is absent; all elaboration arms ran. Commands used the physical `$LANES/397-service-budget` path, ran in the foreground and were not piped. The configured build interpreter was used for the bank; the two Markdown commands used the pinned environment. Exact executable paths, argument arrays, return codes and logs are in the packet.

```sh
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 -B scripts/check_nvm_capture.py
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/pp_srcs.py --check
python3 -B scripts/check_baremetal_only.py --check
python3 -B scripts/check_entity_shape.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_archive.py
/tmp/a363-markdown/bin/python -B scripts/gen_toc.py --check
/tmp/a363-markdown/bin/python -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_hygiene.py --check
python3 -B scripts/measure_test_evidence.py --check
git diff --check ac18b50968b12efe4d15c0a06301264b35656b31
python3 -B sw/builder/test_builder.py --require-elaboration
```

All eight final bound-log measurement regrades return rc 0 with `--record-budget-findings`; that mode retains the negative budget findings. Each underlying native measurement completed successfully. The packet records earlier analysis refusals and the resolved split-UART parser issue; it does not treat those initial wrapper results as passing gates. Without the reporting flag the queued-input regrade refuses with the named heartbeat-budget finding, as required.

The portable self-test passes 30 oracle and 14 flash controls. The unchanged public mutation suites reject 11/11 external and 15/15 internal mutants; the unchanged control passes. The bitmask selector mutant is equivalent on the original standalone-write traces and is rejected by the additional combined-word control. Deleting the busy predicate fails its specifically named control. Four unsupported wait inputs refuse before creating a build directory.

Public P1/P2/P3 and PA/PB/PC/PD probe programs were fetched from `397-review-evidence`, extracted with `git show` into temporary storage, verified byte-identical and run unchanged. P1/P2/P3 and both ordinary observer streams reproduce the original receipts. Wrappers that background jobs or pipe results were not invoked; their constituent programs ran in the foreground. The public PHY timing probe confirms the optimistic SPI cost. Source provenance and compact observer boundaries are in the packet.

An independent arithmetic/custody check verifies all eight bound round-2 receipts, ten receipt-file hashes, 28 duty rows and 28 opportunity rows. Ten protected firmware/capture inputs remain byte-identical to the starting head. Build trees and complete large observer streams remain outside the output packet.

### Handoff

`HANDOFF.md`, the full replacement `PR-BODY.md` with a Round 2 section, `CHECK-EVIDENCE.py`, compact receipts, exact gate results and `SHA256SUMS` are ready in the assigned output directory for manager publication. The findings page records the receipt hashes. No push, PR edit or merge was performed.

Open risks/questions: the measured queued-input defects are owned by #590; physical/BIOS exclusions, optimistic SPI timing and the conditional service assumption remain explicit. Independent reviewers must accept the fixes and the coverage ledger at this candidate. Bench and architecture work keep #397 open. Posting this comment is the final task action.
