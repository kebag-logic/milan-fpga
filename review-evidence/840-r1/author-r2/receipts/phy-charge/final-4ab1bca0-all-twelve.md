| Shape | Plan | Transactions | Max transaction cycles | Max poll cycles | Own charge ms | Worst publication bound ms | Service findings |
|---|---|---|---|---|---|---|---|
| endstation_ax7101_1x1_tdm8 | all | 69 | 9474 | 131480 | 2.83064 | 179.60865 (milan_nvm) | none |
| endstation_ax7101_1x1_tdm8 | uart-paced | 62 | 12451 | 131480 | 3.30696 | 186.35603 (milan_nvm) | none |
| endstation_ax7101_1x1_tdm8 | queued-input | 116 | 9474 | 131480 | 2.83064 | 180.24829 (milan_nvm) | none |
| endstation_ax7101_1x1_tdm8 | queued-short | 140 | 9474 | 131480 | 2.83064 | 164.78454 (milan_status) | none |
| endstation_ax7101_1x1_tdm8 | queued-builtins | 387 | 9474 | 131480 | 2.83064 | 207.70251 (mem_read 0x40000000 128) | none |
| endstation_ax7101_1x1_tdm8 | device-wait | 159 | 9474 | 131480 | 2.83064 | 167.71401 (milan_nvm commit) | none |
| endstation_ax7101_8x8 | all | 217 | 9534 | 131864 | 2.84408 | 246.34096 (milan_nvm) | none |
| endstation_ax7101_8x8 | uart-paced | 224 | 12457 | 131864 | 3.31176 | 246.80864 (milan_nvm) | none |
| endstation_ax7101_8x8 | queued-input | 499 | 9534 | 131864 | 2.84408 | 246.34096 (milan_nvm) | none |
| endstation_ax7101_8x8 | queued-short | 151 | 9534 | 131864 | 2.84408 | 164.79798 (milan_status) | none |
| endstation_ax7101_8x8 | queued-builtins | 396 | 9534 | 131864 | 2.84408 | 207.25985 (mem_read 0x40000000 128) | none |
| endstation_ax7101_8x8 | device-wait | 231 | 9534 | 131864 | 2.84408 | 234.55950 (milan_nvm commit) | none |

| Shape | One transaction ms | Complete poll ms | Scheduling charge ms | 50 ms page-poll margin |
| --- | --- | --- | --- | --- |
| endstation_ax7101_1x1_tdm8 | 0.12451 | 1.31480 | 3.30696 | 46.69304 |
| endstation_ax7101_8x8 | 0.12457 | 1.31864 | 3.31176 | 46.68824 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| endstation_ax7101_1x1_tdm8 | 83.17883 | 166.82117 | 125.00000 | 41.82117 |
| endstation_ax7101_8x8 | 121.80864 | 128.19136 | 125.00000 | 3.19136 |

endstation_ax7101_1x1_tdm8: plans all, device-wait, queued-builtins, queued-input, queued-short, uart-paced; T 12451 P 131480 cycles; worst duty + UART 79.87187 ms (mem_read 0x40000000 128, queued-builtins)
endstation_ax7101_8x8: plans all, device-wait, queued-builtins, queued-input, queued-short, uart-paced; T 12457 P 131864 cycles; worst duty + UART 118.49688 ms (milan_nvm, all)
