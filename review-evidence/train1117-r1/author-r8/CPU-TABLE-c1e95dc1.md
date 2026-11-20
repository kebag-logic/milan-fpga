# The full CPU budget re-measure at `c1e95dc1` (the train's step-14 head): every stated cost against its measurement

Every arm the harness holds, every group, the formal measurement's options; 64 parts a point. A cost's measured figure is the most CPU cycles over every instance and leg; "rule" is that figure in us plus 5 %, rounded up to 5 us (100 cycles a us at the split CPU's 100 MHz); "stated" is the tree's statement it is held to. Generated from `receipts/step14/measure/out/survey-*/compare-*.txt` and `record-classes-*.txt`.

## 1x1/1if

| Cost | Measured, cycles | us | Rule, us | Stated, us | Verdict | Statement; where |
|---|---:|---:|---:|---:|---|---|
| base | 19,498 | 194.98 | 205 | 225 | within | load_grade.stated(1x1/1if) GRADED base; valid-destinations-part2/srp-talker-held |
| base | 19,498 | 194.98 | 205 | 225 | within | load_grade.stated(1x1/1if) STATED_US base; valid-destinations-part2/srp-talker-held |
| base | 19,498 | 194.98 | 205 | 225 | within | poll_grade.STATED_US[(1, 2, 2)] base; valid-destinations-part2/srp-talker-held |
| build | 0 | 0.00 | 0 | 1010 | within | load_grade.stated(1x1/1if) GRADED build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0.00 | 0 | 1010 | within | load_grade.stated(1x1/1if) STATED_US build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0.00 | 0 | 1010 | within | whole_grade.stated_us((1, 2, 2)) build (ctrl_loop.h); answering-every-port-part0/notice-every-4 |
| build_one | 53,550 | 535.50 | 565 | 735 | within | load_grade.stated(1x1/1if) GRADED build_one; answering-ports-part19/srp |
| build_one | 53,550 | 535.50 | 565 | 735 | within | load_grade.stated(1x1/1if) STATED_US build_one; answering-ports-part19/srp |
| build_one | 53,550 | 535.50 | 565 | 735 | within | whole_grade.stated_us((1, 2, 2)) build-one (ctrl_loop.h); answering-ports-part19/srp |
| centisecond | 13,011 | 130.11 | 140 | 150 | within | load_grade.stated(1x1/1if) GRADED centisecond; valid-destinations-part2/srp-talker-held.log |
| centisecond | 13,011 | 130.11 | 140 | 150 | within | load_grade.stated(1x1/1if) STATED_US centisecond; valid-destinations-part2/srp-talker-held.log |
| event.ACMP | 14,079 | 140.79 | 150 | 170 | within | load_grade.stated(1x1/1if) GRADED event.ACMP; TIMER#1, 46 taken |
| event.ACMP | 14,079 | 140.79 | 150 | 185 | within | load_grade.stated(1x1/1if) STATED_US event.ACMP; TIMER#1, 46 taken |
| event.ADP | 6,685 | 66.85 | 75 | 115 | within | load_grade.stated(1x1/1if) GRADED event.ADP; TIMER#0, 282 taken |
| event.ADP | 6,685 | 66.85 | 75 | 115 | within | load_grade.stated(1x1/1if) STATED_US event.ADP; TIMER#0, 282 taken |
| event.AECP | 6,075 | 60.75 | 65 | 75 | within | load_grade.stated(1x1/1if) GRADED event.AECP; TIMER#3, 14970 taken |
| event.AECP | 6,075 | 60.75 | 65 | 75 | within | load_grade.stated(1x1/1if) STATED_US event.AECP; TIMER#3, 14970 taken |
| event.GM | 2,996 | 29.96 | 35 | 40 | within | load_grade.stated(1x1/1if) GRADED event.GM; GM, 268076 taken |
| event.GM | 2,996 | 29.96 | 35 | 40 | within | load_grade.stated(1x1/1if) STATED_US event.GM; GM, 268076 taken |
| event.LINK | 10,507 | 105.07 | 115 | 155 | within | rows_grade.ROW_COSTS[1x1/1if] event.LINK; LINK, 244 taken |
| event.MAAP | 13,015 | 130.15 | 140 | 170 | within | load_grade.stated(1x1/1if) GRADED event.MAAP; TIMER#2, 667 taken |
| event.MAAP | 13,015 | 130.15 | 140 | 165 | within | load_grade.stated(1x1/1if) STATED_US event.MAAP; TIMER#2, 667 taken |
| event.TICK | 3,792 | 37.92 | 40 | 55 | within | load_grade.stated(1x1/1if) GRADED event.TICK; TICK, 83030 taken |
| event.TICK | 3,792 | 37.92 | 40 | 55 | within | load_grade.stated(1x1/1if) STATED_US event.TICK; TICK, 83030 taken |
| events_none | 3,073 | 30.73 | 35 | 40 | within | load_grade.stated(1x1/1if) GRADED events_none; answering-every-port-part1/notice-burst-1.log |
| events_none | 3,073 | 30.73 | 35 | 40 | within | load_grade.stated(1x1/1if) STATED_US events_none; answering-every-port-part1/notice-burst-1.log |
| item.acmp | 4,646 | 46.46 | 50 | 55 | within | load_grade.stated(1x1/1if) GRADED item.acmp; none-part2/backlog-owed |
| item.acmp | 4,646 | 46.46 | 50 | 55 | within | load_grade.stated(1x1/1if) STATED_US item.acmp; none-part2/backlog-owed |
| item.acmp | 4,646 | 46.46 | 50 | 55 | within | poll_grade.STATED_US[(1, 2, 2)] acmp; none-part2/backlog-owed |
| item.acmp_declined | 1,765 | 17.65 | 20 | 20 | within | load_grade.stated(1x1/1if) GRADED item.acmp_declined; none-part2/backlog-owed |
| item.acmp_declined | 1,765 | 17.65 | 20 | 20 | within | load_grade.stated(1x1/1if) STATED_US item.acmp_declined; none-part2/backlog-owed |
| item.acmp_declined | 1,765 | 17.65 | 20 | 20 | within | poll_grade.STATED_US[(1, 2, 2)] acmp_declined; none-part2/backlog-owed |
| item.acmp_kept | 7,247 | 72.47 | 80 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; none-part2/backlog-owed |
| item.aecp | 14,111 | 141.11 | 150 | 210 | within | poll_grade.STATED_US[(1, 2, 2)] aecp; declaring-outputs-part1/aecp-fanout |
| item.aecp_long | 0 | 0.00 | 0 | 365 | within | poll_grade.STATED_US[(1, 2, 2)] aecp_long; answering-every-port-part0/notice-every-4 |
| item.aecp_long | 0 | 0.00 | 0 | 365 | within | poll_grade.STATED_US[(1, 2, 2)] aecp_long; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 735 | within | load_grade.stated(1x1/1if) GRADED item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 735 | within | load_grade.stated(1x1/1if) STATED_US item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 735 | within | poll_grade.STATED_US[(1, 2, 2)] mrpdu; answering-every-port-part0/notice-every-4 |
| item.rebuild | 17,214 | 172.14 | 185 | 290 | within | poll_grade.STATED_US[(1, 2, 2)] rebuild; answering-ports-part16/fixture |
| item.reclaim | 1,613 | 16.13 | 20 | 25 | within | load_grade.stated(1x1/1if) GRADED item.reclaim; none-part19/srp |
| item.reclaim | 1,613 | 16.13 | 20 | 25 | within | load_grade.stated(1x1/1if) STATED_US item.reclaim; none-part19/srp |
| item.reclaim | 1,613 | 16.13 | 20 | 25 | within | poll_grade.STATED_US[(1, 2, 2)] reclaim; none-part19/srp |
| item.record | 22,867 | 228.67 | 245 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; answering-later-part1/notice-retried-7 |
| item.retained | 0 | 0.00 | 0 | 285 | within | load_grade.stated(1x1/1if) GRADED item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0.00 | 0 | 285 | within | load_grade.stated(1x1/1if) STATED_US item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0.00 | 0 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; answering-every-port-part0/notice-every-4 |
| item.walk | 1,961 | 19.61 | 25 | 35 | within | load_grade.stated(1x1/1if) GRADED item.walk; answering-ports-part19/srp |
| item.walk | 1,961 | 19.61 | 25 | 35 | within | load_grade.stated(1x1/1if) STATED_US item.walk; answering-ports-part19/srp |
| item.walk | 1,961 | 19.61 | 25 | 35 | within | poll_grade.STATED_US[(1, 2, 2)] walk; answering-ports-part19/srp |
| item.withdraw | 4,680 | 46.80 | 50 | 90 | within | poll_grade.STATED_US[(1, 2, 2)] withdraw; answering-ports-part20/backlog |
| record.acmp | 19,166 | 191.66 | 205 | 265 | within | load_grade.stated(1x1/1if) GRADED record.acmp; none-part16/fixture.log |
| record.acmp | 19,166 | 191.66 | 205 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; none-part16/fixture.log |
| record.adp | 8,901 | 89.01 | 95 | 100 | within | load_grade.stated(1x1/1if) GRADED record.adp; answering-ports-part3/backlog-adp-refill.log |
| record.adp | 8,901 | 89.01 | 95 | 105 | within | load_grade.stated(1x1/1if) STATED_US record.adp; answering-ports-part3/backlog-adp-refill.log |
| record.maap | 10,250 | 102.50 | 110 | 115 | within | load_grade.stated(1x1/1if) GRADED record.maap; talker-notices-part0/talker-notice-4.log |
| record.maap | 10,250 | 102.50 | 110 | 115 | within | load_grade.stated(1x1/1if) STATED_US record.maap; talker-notices-part0/talker-notice-4.log |
| record.srp | 23,153 | 231.53 | 245 | 285 | within | load_grade.stated(1x1/1if) GRADED record.srp; answering-later-part1/notice-retried-7.log |
| record.srp | 23,153 | 231.53 | 245 | 285 | within | load_grade.stated(1x1/1if) STATED_US record.srp; answering-later-part1/notice-retried-7.log |
| step | 81,188 | 811.88 | 855 | 975 | within | load_grade.stated(1x1/1if) GRADED step; answering-ports-part8/backlog-adp@program-aged2-4 |
| step | 81,188 | 811.88 | 855 | 975 | within | load_grade.stated(1x1/1if) STATED_US step; answering-ports-part8/backlog-adp@program-aged2-4 |
| step | 81,188 | 811.88 | 855 | 975 | within | whole_grade.stated_us((1, 2, 2)) step (ctrl_loop.h); answering-ports-part8/backlog-adp@program-aged2-4 |
| item.aecp.notice | 14,111 | 141.11 | 150 | 210 | within | load_grade.stated(1x1/1if) GRADED item.aecp.notice; declaring-outputs-part1/aecp-fanout (16 frame(s)) |
| item.aecp.notice | 14,111 | 141.11 | 150 | 210 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.notice; declaring-outputs-part1/aecp-fanout (16 frame(s)) |
| item.aecp.response | 2,642 | 26.42 | 30 | 60 | within | load_grade.stated(1x1/1if) GRADED item.aecp.response; none-part2/backlog-owed (1 frame(s)) |
| item.aecp.response | 2,642 | 26.42 | 30 | 60 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.response; none-part2/backlog-owed (1 frame(s)) |
| event.AMAP_LIVE_WRITE | 1,823 | 18.23 | 20 | 30 | within | rows_tiers.DATAPATH_US[1x1/1if] AMAP_LIVE_WRITE; datapath-events.log@67941389 |
| event.AS_PATH_CHANGED | 2,895 | 28.95 | 35 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AS_PATH_CHANGED; datapath-events.log@67735877 |
| event.AVB_INFO_CHANGED | 2,662 | 26.62 | 30 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AVB_INFO_CHANGED; datapath-events.log@67535980 |

The long notice (aecp-largest-notice):

- item.aecp_long (the polls): 29,780 CPU cycles, 315 us by the rule, against aecp_long 365 us at 1x1/1if: within; declaring-outputs-part3/aecp-largest-notice
- the notice kind (aecp_kinds.py): 29,780 CPU cycles, 315 us by the rule, against aecp_long 365 us at 1x1/1if: within; declaring-outputs-part3/aecp-largest-notice (15 frame(s))

The AECP records by class (record_classes.py):

- 1x1/1if reported long: the dearest 91,409 CPU cycles, 960 us by the rule, stated 975 us (declaring-outputs aecp-largest-notice: the largest legal command's)
- 1x1/1if held long: the dearest 91,625 CPU cycles, 965 us by the rule, stated 975 us (answering-ports aecp-largest-notice: the largest legal command's)
- 1x1/1if reported other: the dearest 20,436 CPU cycles, 215 us by the rule, stated 245 us (answering-later notice-retried-0: command 0x0010)
- 1x1/1if held other: the dearest 23,167 CPU cycles, 245 us by the rule, stated 245 us (declaring-outputs aecp-fanout: command 0x000e)
- 1x1/1if reported paced: the dearest 30,232 CPU cycles, 320 us by the rule, stated 310 us (declaring-outputs aecp-fanout: REMOVE_AUDIO_MAPPINGS, paced)
- 1x1/1if held paced: the dearest 29,468 CPU cycles, 310 us by the rule, stated 310 us (answering-ports aecp-fanout: REMOVE_AUDIO_MAPPINGS, paced)
- REPORTED 1x1/1if declaring-outputs aecp-fanout: a record of 30,232 CPU cycles, 320 us by the rule, over the paced record's 310 us (REMOVE_AUDIO_MAPPINGS, paced)
- RESULT: PASS

## 8x8/1if

| Cost | Measured, cycles | us | Rule, us | Stated, us | Verdict | Statement; where |
|---|---:|---:|---:|---:|---|---|
| base | 27,482 | 274.82 | 290 | 300 | within | load_grade.stated(8x8/1if) GRADED base; valid-destinations-part1/srp-talker-held |
| base | 27,482 | 274.82 | 290 | 300 | within | load_grade.stated(8x8/1if) STATED_US base; valid-destinations-part1/srp-talker-held |
| base | 27,482 | 274.82 | 290 | 300 | within | poll_grade.STATED_US[(1, 9, 9)] base; valid-destinations-part1/srp-talker-held |
| build | 0 | 0.00 | 0 | 1795 | within | load_grade.stated(8x8/1if) GRADED build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0.00 | 0 | 1795 | within | load_grade.stated(8x8/1if) STATED_US build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0.00 | 0 | 1795 | within | whole_grade.stated_us((1, 9, 9)) build (ctrl_loop.h); answering-every-port-part0/notice-every-4 |
| build_one | 122,913 | 1229.13 | 1295 | 1475 | within | load_grade.stated(8x8/1if) GRADED build_one; valid-destinations-part1/srp-talker-held |
| build_one | 122,913 | 1229.13 | 1295 | 1475 | within | load_grade.stated(8x8/1if) STATED_US build_one; valid-destinations-part1/srp-talker-held |
| build_one | 122,913 | 1229.13 | 1295 | 1475 | within | whole_grade.stated_us((1, 9, 9)) build-one (ctrl_loop.h); valid-destinations-part1/srp-talker-held |
| centisecond | 27,008 | 270.08 | 285 | 510 | within | load_grade.stated(8x8/1if) GRADED centisecond; valid-destinations-part1/srp-talker-held.log |
| centisecond | 27,008 | 270.08 | 285 | 510 | within | load_grade.stated(8x8/1if) STATED_US centisecond; valid-destinations-part1/srp-talker-held.log |
| event.ACMP | 16,264 | 162.64 | 175 | 210 | within | load_grade.stated(8x8/1if) GRADED event.ACMP; TIMER#1, 46 taken |
| event.ACMP | 16,264 | 162.64 | 175 | 350 | within | load_grade.stated(8x8/1if) STATED_US event.ACMP; TIMER#1, 46 taken |
| event.ADP | 7,331 | 73.31 | 80 | 120 | within | load_grade.stated(8x8/1if) GRADED event.ADP; TIMER#0, 331 taken |
| event.ADP | 7,331 | 73.31 | 80 | 120 | within | load_grade.stated(8x8/1if) STATED_US event.ADP; TIMER#0, 331 taken |
| event.AECP | 7,417 | 74.17 | 80 | 120 | within | load_grade.stated(8x8/1if) GRADED event.AECP; TIMER#3, 34401 taken |
| event.AECP | 7,417 | 74.17 | 80 | 120 | within | load_grade.stated(8x8/1if) STATED_US event.AECP; TIMER#3, 34401 taken |
| event.GM | 2,970 | 29.70 | 35 | 320 | within | load_grade.stated(8x8/1if) GRADED event.GM; GM, 491251 taken |
| event.GM | 2,970 | 29.70 | 35 | 320 | within | load_grade.stated(8x8/1if) STATED_US event.GM; GM, 491251 taken |
| event.LINK | 17,301 | 173.01 | 185 | 300 | within | rows_grade.ROW_COSTS[8x8/2if] event.LINK; LINK, 244 taken |
| event.MAAP | 19,766 | 197.66 | 210 | 225 | within | load_grade.stated(8x8/1if) GRADED event.MAAP; TIMER#2, 667 taken |
| event.MAAP | 19,766 | 197.66 | 210 | 225 | within | load_grade.stated(8x8/1if) STATED_US event.MAAP; TIMER#2, 667 taken |
| event.TICK | 2,518 | 25.18 | 30 | 85 | within | load_grade.stated(8x8/1if) GRADED event.TICK; TICK, 92416 taken |
| event.TICK | 2,518 | 25.18 | 30 | 55 | within | load_grade.stated(8x8/1if) STATED_US event.TICK; TICK, 92416 taken |
| events_none | 2,919 | 29.19 | 35 | 45 | within | load_grade.stated(8x8/1if) GRADED events_none; valid-destinations-part0/srp-talker.log |
| events_none | 2,919 | 29.19 | 35 | 45 | within | load_grade.stated(8x8/1if) STATED_US events_none; valid-destinations-part0/srp-talker.log |
| item.acmp | 6,041 | 60.41 | 65 | 80 | within | load_grade.stated(8x8/1if) GRADED item.acmp; answering-ports-part3/backlog-owed |
| item.acmp | 6,041 | 60.41 | 65 | 80 | within | load_grade.stated(8x8/1if) STATED_US item.acmp; answering-ports-part3/backlog-owed |
| item.acmp | 6,041 | 60.41 | 65 | 80 | within | poll_grade.STATED_US[(1, 9, 9)] acmp; answering-ports-part3/backlog-owed |
| item.acmp_declined | 2,298 | 22.98 | 25 | 30 | within | load_grade.stated(8x8/1if) GRADED item.acmp_declined; none-part3/backlog-owed |
| item.acmp_declined | 2,298 | 22.98 | 25 | 30 | within | load_grade.stated(8x8/1if) STATED_US item.acmp_declined; none-part3/backlog-owed |
| item.acmp_declined | 2,298 | 22.98 | 25 | 30 | within | poll_grade.STATED_US[(1, 9, 9)] acmp_declined; none-part3/backlog-owed |
| item.acmp_kept | 8,793 | 87.93 | 95 | 440 | within | load_grade.stated(8x8/1if) STATED_US record.acmp; none-part3/backlog-owed |
| item.aecp | 13,497 | 134.97 | 145 | 145 | within | poll_grade.STATED_US[(1, 9, 9)] aecp; answering-ports-part9/aecp-fanout |
| item.aecp_long | 0 | 0.00 | 0 | 320 | within | poll_grade.STATED_US[(1, 9, 9)] aecp_long; answering-every-port-part0/notice-every-4 |
| item.aecp_long | 0 | 0.00 | 0 | 320 | within | poll_grade.STATED_US[(1, 9, 9)] aecp_long; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 1475 | within | load_grade.stated(8x8/1if) GRADED item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 1475 | within | load_grade.stated(8x8/1if) STATED_US item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0.00 | 0 | 1475 | within | poll_grade.STATED_US[(1, 9, 9)] mrpdu; answering-every-port-part0/notice-every-4 |
| item.rebuild | 20,686 | 206.86 | 220 | 590 | within | poll_grade.STATED_US[(1, 9, 9)] rebuild; none-part12/fixture |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | load_grade.stated(8x8/1if) GRADED item.reclaim; valid-destinations-part1/srp-talker-held |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | load_grade.stated(8x8/1if) STATED_US item.reclaim; valid-destinations-part1/srp-talker-held |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | poll_grade.STATED_US[(1, 9, 9)] reclaim; valid-destinations-part1/srp-talker-held |
| item.record | 35,536 | 355.36 | 375 | 375 | within | poll_grade.STATED_US[(1, 9, 9)] retained; valid-destinations-part1/srp-talker-held |
| item.retained | 0 | 0.00 | 0 | 375 | within | load_grade.stated(8x8/1if) GRADED item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0.00 | 0 | 375 | within | load_grade.stated(8x8/1if) STATED_US item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0.00 | 0 | 375 | within | poll_grade.STATED_US[(1, 9, 9)] retained; answering-every-port-part0/notice-every-4 |
| item.walk | 3,051 | 30.51 | 35 | 120 | within | load_grade.stated(8x8/1if) GRADED item.walk; valid-destinations-part0/srp-talker |
| item.walk | 3,051 | 30.51 | 35 | 120 | within | load_grade.stated(8x8/1if) STATED_US item.walk; valid-destinations-part0/srp-talker |
| item.walk | 3,051 | 30.51 | 35 | 120 | within | poll_grade.STATED_US[(1, 9, 9)] walk; valid-destinations-part0/srp-talker |
| item.withdraw | 6,014 | 60.14 | 65 | 110 | within | poll_grade.STATED_US[(1, 9, 9)] withdraw; none-part4/backlog |
| record.acmp | 21,598 | 215.98 | 230 | 305 | within | load_grade.stated(8x8/1if) GRADED record.acmp; none-part1/backlog-adp@program-aged1-4.log |
| record.acmp | 21,598 | 215.98 | 230 | 440 | within | load_grade.stated(8x8/1if) STATED_US record.acmp; none-part1/backlog-adp@program-aged1-4.log |
| record.adp | 12,285 | 122.85 | 130 | 135 | within | load_grade.stated(8x8/1if) GRADED record.adp; none-part2/backlog-adp-refill.log |
| record.adp | 12,285 | 122.85 | 130 | 240 | within | load_grade.stated(8x8/1if) STATED_US record.adp; none-part2/backlog-adp-refill.log |
| record.maap | 16,190 | 161.90 | 170 | 180 | within | load_grade.stated(8x8/1if) GRADED record.maap; valid-destinations-part2/srp-talker-loss.log |
| record.maap | 16,190 | 161.90 | 170 | 180 | within | load_grade.stated(8x8/1if) STATED_US record.maap; valid-destinations-part2/srp-talker-loss.log |
| record.srp | 35,846 | 358.46 | 380 | 375 | OVER | load_grade.stated(8x8/1if) GRADED record.srp; valid-destinations-part1/srp-talker-held.log |
| record.srp | 35,846 | 358.46 | 380 | 375 | OVER | load_grade.stated(8x8/1if) STATED_US record.srp; valid-destinations-part1/srp-talker-held.log |
| step | 80,917 | 809.17 | 850 | 1030 | within | load_grade.stated(8x8/1if) GRADED step; none-part12/backlog-adp@program-aged2-3 |
| step | 80,917 | 809.17 | 850 | 1030 | within | load_grade.stated(8x8/1if) STATED_US step; none-part12/backlog-adp@program-aged2-3 |
| step | 80,917 | 809.17 | 850 | 975 | within | whole_grade.stated_us((1, 9, 9)) step (ctrl_loop.h); none-part12/backlog-adp@program-aged2-3 |
| item.aecp.notice | 13,497 | 134.97 | 145 | 275 | within | load_grade.stated(8x8/1if) GRADED item.aecp.notice; answering-ports-part9/aecp-fanout (16 frame(s)) |
| item.aecp.notice | 13,497 | 134.97 | 145 | 275 | within | load_grade.stated(8x8/1if) STATED_US item.aecp.notice; answering-ports-part9/aecp-fanout (16 frame(s)) |
| item.aecp.response | 2,258 | 22.58 | 25 | 65 | within | load_grade.stated(8x8/1if) GRADED item.aecp.response; none-part3/backlog-owed (1 frame(s)) |
| item.aecp.response | 2,258 | 22.58 | 25 | 65 | within | load_grade.stated(8x8/1if) STATED_US item.aecp.response; none-part3/backlog-owed (1 frame(s)) |
| event.AMAP_LIVE_WRITE | 1,704 | 17.04 | 20 | 30 | within | rows_tiers.DATAPATH_US[8x8/2if] AMAP_LIVE_WRITE; datapath-events.log@72440000 |
| event.AS_PATH_CHANGED | 2,645 | 26.45 | 30 | 40 | within | rows_tiers.DATAPATH_US[8x8/2if] AS_PATH_CHANGED; datapath-events.log@71634198 |
| event.AVB_INFO_CHANGED | 2,261 | 22.61 | 25 | 40 | within | rows_tiers.DATAPATH_US[8x8/2if] AVB_INFO_CHANGED; datapath-events.log@71419750 |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | load_grade.stated(8x8/1if) GRADED item.reclaim; valid-destinations-part1/srp-talker-held |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | load_grade.stated(8x8/1if) STATED_US item.reclaim; valid-destinations-part1/srp-talker-held |
| item.reclaim | 3,840 | 38.40 | 45 | 40 | OVER | poll_grade.STATED_US[(1, 9, 9)] reclaim; valid-destinations-part1/srp-talker-held |
| record.srp | 35,846 | 358.46 | 380 | 375 | OVER | load_grade.stated(8x8/1if) GRADED record.srp; valid-destinations-part1/srp-talker-held.log |
| record.srp | 35,846 | 358.46 | 380 | 375 | OVER | load_grade.stated(8x8/1if) STATED_US record.srp; valid-destinations-part1/srp-talker-held.log |

The long notice (aecp-largest-notice):

- item.aecp_long (the polls): 29,498 CPU cycles, 310 us by the rule, against aecp_long 320 us at 8x8/1if: within; answering-ports-part13/aecp-largest-notice
- the notice kind (aecp_kinds.py): 29,498 CPU cycles, 310 us by the rule, against aecp_long 320 us at 8x8/1if: within; answering-ports-part13/aecp-largest-notice (15 frame(s))

The AECP records by class (record_classes.py):

- 8x8/1if reported long: the dearest 167,967 CPU cycles, 1765 us by the rule, stated 1720 us (declaring-outputs aecp-largest-notice: the largest legal command's)
- 8x8/1if held long: the dearest 163,497 CPU cycles, 1720 us by the rule, stated 1720 us (answering-ports aecp-largest-notice: the largest legal command's)
- 8x8/1if reported other: the dearest 19,173 CPU cycles, 205 us by the rule, stated 265 us (talker-notices talker-notice-0: command 0x0010)
- 8x8/1if held other: the dearest 20,697 CPU cycles, 220 us by the rule, stated 265 us (declaring-outputs aecp-fanout: command 0x000e)
- 8x8/1if reported paced: the dearest 56,844 CPU cycles, 600 us by the rule, stated 685 us (declaring-outputs aecp-fanout: SET_CONFIGURATION, paced)
- 8x8/1if held paced: the dearest 56,871 CPU cycles, 600 us by the rule, stated 685 us (answering-ports aecp-fanout: SET_CONFIGURATION, paced)
- REPORTED 8x8/1if declaring-outputs aecp-largest-notice: a record of 167,967 CPU cycles, 1765 us by the rule, over the long record's 1720 us (the largest legal command's)
- REPORTED 8x8/1if declaring-outputs aecp-largest-notice: a record of 164,113 CPU cycles, 1725 us by the rule, over the long record's 1720 us (the largest legal command's)
- RESULT: PASS
