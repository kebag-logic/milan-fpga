| Shape | Plan | Transactions | Max transaction cycles | Max poll cycles | Own charge ms | Worst publication bound ms | Service findings |
|---|---|---|---|---|---|---|---|
| endstation_ax7101_8x8 | queued-input | 499 | 16963 | 247411 | 5.18819 | 248.68507 (milan_nvm) | none |
| endstation_ax7101_8x8 | queued-short | 151 | 16963 | 247411 | 5.18819 | 167.73527 (milan_status) | none |
| endstation_ax7101_8x8 | queued-builtins | 396 | 16963 | 247411 | 5.18819 | 209.60418 (mem_read 0x40000000 128) | none |
| endstation_ax7101_8x8 | device-wait | 231 | 16963 | 247411 | 5.18819 | 236.88863 (milan_nvm commit) | none |

| Shape | One transaction ms | Complete poll ms | Scheduling charge ms | 50 ms page-poll margin |
| --- | --- | --- | --- | --- |
| endstation_ax7101_8x8 | 0.16963 | 2.47411 | 5.18819 | 44.81181 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| endstation_ax7101_8x8 | 123.68507 | 126.31493 | 125.00000 | 1.31493 |

endstation_ax7101_8x8: plans device-wait, queued-builtins, queued-input, queued-short; T 16963 P 247411 cycles; worst duty + UART 118.49688 ms (milan_nvm, queued-input)
