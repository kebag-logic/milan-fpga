| Shape | Plan | Transactions | Max transaction cycles | Max poll cycles | Own charge ms | Worst publication bound ms | Service findings |
|---|---|---|---|---|---|---|---|
| endstation_ax7101_1x1_tdm8 | all | 69 | 16957 | 246869 | 5.18181 | 181.95982 (milan_nvm) | none |
| endstation_ax7101_1x1_tdm8 | uart-paced | 62 | 22559 | 246869 | 6.07813 | 189.12720 (milan_nvm) | none |
| endstation_ax7101_8x8 | all | 217 | 16963 | 247411 | 5.18819 | 248.68507 (milan_nvm) | none |

| Shape | One transaction ms | Complete poll ms | Scheduling charge ms | 50 ms page-poll margin |
| --- | --- | --- | --- | --- |
| endstation_ax7101_1x1_tdm8 | 0.22559 | 2.46869 | 6.07813 | 43.92187 |
| endstation_ax7101_8x8 | 0.16963 | 2.47411 | 5.18819 | 44.81181 |

| Shape | Worst duty + UART + charge ms | Maximum permissible trigger ms | Selected trigger ms | Remaining reserve ms |
| --- | --- | --- | --- | --- |
| endstation_ax7101_1x1_tdm8 | 64.12720 | 185.87280 | 125.00000 | 60.87280 |
| endstation_ax7101_8x8 | 123.68507 | 126.31493 | 125.00000 | 1.31493 |

endstation_ax7101_1x1_tdm8: plans all, uart-paced; T 22559 P 246869 cycles; worst duty + UART 58.04907 ms (milan_nvm, uart-paced)
endstation_ax7101_8x8: plans all; T 16963 P 247411 cycles; worst duty + UART 118.49688 ms (milan_nvm, all)
