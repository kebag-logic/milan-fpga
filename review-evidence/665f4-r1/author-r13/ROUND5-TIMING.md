[A560]

# Round 5 conditional service envelope

Head: `500b8f64443777685e6a54049d933476710d26f0`. Host mailbox trace charges 100 ns per access, a total 1 ms CPU/preemption allowance per action and 100 ns observation uncertainty. Each action shares one 10 ms service budget; only the explicit protocol wait is deducted. These assumptions require target validation. The full-ring 11 ms stall is rejected by the budget predicate.

| IF | Action | Elapsed ns | Protocol wait ms | Service ns | Cumulative accesses |
|---:|---|---:|---:|---:|---:|
| 1 | startup | 1005300 | 0 | 1005300 | 56 |
| 1 | JoinTime | 1015300 | 0 | 1015300 | 212 |
| 1 | periodic | 1015700 | 0 | 1015700 | 517 |
| 1 | MVRP LeaveAll | 1002400 | 0 | 1002400 | 17568 |
| 1 | MSRP LeaveAll | 1006800 | 0 | 1006800 | 20450 |
| 1 | RX to licence | 1001900 | 0 | 1001900 | 228 |
| 1 | malformed discard | 1002300 | 0 | 1002300 | 254 |
| 1 | Domain to declarations | 200995000 | 200 | 995000 | 436 |
| 1 | Talker RX to Listener | 200998700 | 200 | 998700 | 623 |
| 1 | unbind to withdrawal | 200999300 | 200 | 999300 | 780 |
| 1 | LeaveTime to stop | 1001100 | 0 | 1001100 | 666 |
| 2 | startup | 1010200 | 0 | 1010200 | 106 |
| 2 | JoinTime | 1019800 | 0 | 1019800 | 308 |
| 2 | periodic | 1020400 | 0 | 1020400 | 696 |
| 2 | MVRP LeaveAll | 1002500 | 0 | 1002500 | 20577 |
| 2 | MSRP LeaveAll | 1006900 | 0 | 1006900 | 21625 |
| 2 | MVRP LeaveAll | 1002500 | 0 | 1002500 | 23112 |
| 2 | MSRP LeaveAll | 1006900 | 0 | 1006900 | 24087 |
| 2 | RX to licence | 1001900 | 0 | 1001900 | 324 |
| 2 | malformed discard | 1002500 | 0 | 1002500 | 354 |
| 2 | Domain to declarations | 200993300 | 200 | 993300 | 573 |
| 2 | Talker RX to Listener | 200995400 | 200 | 995400 | 766 |
| 2 | unbind to withdrawal | 201003400 | 200 | 1003400 | 969 |
| 2 | LeaveTime to stop | 1001100 | 0 | 1001100 | 998 |

The selected processor-wire differential passes five cases per interface count. D1: immediate IN withdrawal and the original LV deadline follow Milan 4.2.7.2.2. D2: the processor emits Ignore on Listener Lv, while firmware retains the last declaration per IEEE 802.1Q 35.2.2.7.2. These documented differences remain explicit; this round does not claim a fresh run of the full processor-only suites.
