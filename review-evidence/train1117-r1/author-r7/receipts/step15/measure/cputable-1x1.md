# The full CPU budget re-measure at `92de01f7` (the SRP cut): every stated cost against its measurement

Every arm the harness holds, every group, the formal measurement's options; 64 parts a point. A cost's measured figure is the most CPU cycles over every instance and leg; "rule" is that figure plus 5 %, rounded up to 5 us. "`c1e95dc1`" is the previous head's measured figure for the same statement.

## 1x1/1if

3 of 68 statements exceeded.

| Cost | Measured, cycles | `c1e95dc1` | Rule, us | Stated, us | Verdict | Statement; where |
|---|---:|---:|---:|---:|---|---|
| base | 19,359 | 19,498 | 205 | 225 | within | load_grade.stated(1x1/1if) GRADED base; valid-destinations-part2/srp-talker-held |
| base | 19,359 | 19,498 | 205 | 225 | within | load_grade.stated(1x1/1if) STATED_US base; valid-destinations-part2/srp-talker-held |
| base | 19,359 | 19,498 | 205 | 225 | within | poll_grade.STATED_US[(1, 2, 2)] base; valid-destinations-part2/srp-talker-held |
| build | 0 | 0 | 0 | 1010 | within | load_grade.stated(1x1/1if) GRADED build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0 | 0 | 1010 | within | load_grade.stated(1x1/1if) STATED_US build; answering-every-port-part0/notice-every-4 |
| build | 0 | 0 | 0 | 1010 | within | whole_grade.stated_us((1, 2, 2)) build (ctrl_loop.h); answering-every-port-part0/notice-every-4 |
| build_one | 53,827 | 53,550 | 570 | 735 | within | load_grade.stated(1x1/1if) GRADED build_one; answering-ports-part19/srp |
| build_one | 53,827 | 53,550 | 570 | 735 | within | load_grade.stated(1x1/1if) STATED_US build_one; answering-ports-part19/srp |
| build_one | 53,827 | 53,550 | 570 | 735 | within | whole_grade.stated_us((1, 2, 2)) build-one (ctrl_loop.h); answering-ports-part19/srp |
| centisecond | 15,976 | 13,011 | 170 | 150 | **OVER-raw** | load_grade.stated(1x1/1if) GRADED centisecond; valid-destinations-part2/srp-talker-held.log |
| centisecond | 15,976 | 13,011 | 170 | 150 | **OVER-raw** | load_grade.stated(1x1/1if) STATED_US centisecond; valid-destinations-part2/srp-talker-held.log |
| event.ACMP | 13,781 | 14,079 | 145 | 170 | within | load_grade.stated(1x1/1if) GRADED event.ACMP; TIMER#1, 46 taken |
| event.ACMP | 13,781 | 14,079 | 145 | 185 | within | load_grade.stated(1x1/1if) STATED_US event.ACMP; TIMER#1, 46 taken |
| event.ADP | 7,257 | 6,685 | 80 | 115 | within | load_grade.stated(1x1/1if) GRADED event.ADP; TIMER#0, 282 taken |
| event.ADP | 7,257 | 6,685 | 80 | 115 | within | load_grade.stated(1x1/1if) STATED_US event.ADP; TIMER#0, 282 taken |
| event.AECP | 6,139 | 6,075 | 65 | 75 | within | load_grade.stated(1x1/1if) GRADED event.AECP; TIMER#3, 15012 taken |
| event.AECP | 6,139 | 6,075 | 65 | 75 | within | load_grade.stated(1x1/1if) STATED_US event.AECP; TIMER#3, 15012 taken |
| event.GM | 3,122 | 2,996 | 35 | 40 | within | load_grade.stated(1x1/1if) GRADED event.GM; GM, 271376 taken |
| event.GM | 3,122 | 2,996 | 35 | 40 | within | load_grade.stated(1x1/1if) STATED_US event.GM; GM, 271376 taken |
| event.LINK | 10,611 | 10,507 | 115 | 155 | within | rows_grade.ROW_COSTS[1x1/1if] event.LINK; LINK, 244 taken |
| event.MAAP | 12,637 | 13,015 | 135 | 170 | within | load_grade.stated(1x1/1if) GRADED event.MAAP; TIMER#2, 667 taken |
| event.MAAP | 12,637 | 13,015 | 135 | 165 | within | load_grade.stated(1x1/1if) STATED_US event.MAAP; TIMER#2, 667 taken |
| event.TICK | 3,629 | 3,792 | 40 | 55 | within | load_grade.stated(1x1/1if) GRADED event.TICK; TICK, 83037 taken |
| event.TICK | 3,629 | 3,792 | 40 | 55 | within | load_grade.stated(1x1/1if) STATED_US event.TICK; TICK, 83037 taken |
| events_none | 3,139 | 3,073 | 35 | 40 | within | load_grade.stated(1x1/1if) GRADED events_none; answering-every-port-part5/notice-burst-5.log |
| events_none | 3,139 | 3,073 | 35 | 40 | within | load_grade.stated(1x1/1if) STATED_US events_none; answering-every-port-part5/notice-burst-5.log |
| item.acmp | 4,739 | 4,646 | 50 | 55 | within | load_grade.stated(1x1/1if) GRADED item.acmp; answering-ports-part2/backlog-owed |
| item.acmp | 4,739 | 4,646 | 50 | 55 | within | load_grade.stated(1x1/1if) STATED_US item.acmp; answering-ports-part2/backlog-owed |
| item.acmp | 4,739 | 4,646 | 50 | 55 | within | poll_grade.STATED_US[(1, 2, 2)] acmp; answering-ports-part2/backlog-owed |
| item.acmp_declined | 1,700 | 1,765 | 20 | 20 | within | load_grade.stated(1x1/1if) GRADED item.acmp_declined; none-part2/backlog-owed |
| item.acmp_declined | 1,700 | 1,765 | 20 | 20 | within | load_grade.stated(1x1/1if) STATED_US item.acmp_declined; none-part2/backlog-owed |
| item.acmp_declined | 1,700 | 1,765 | 20 | 20 | within | poll_grade.STATED_US[(1, 2, 2)] acmp_declined; none-part2/backlog-owed |
| item.acmp_kept | 7,158 | 7,247 | 80 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; answering-ports-part2/backlog-owed |
| item.aecp | 14,084 | 14,111 | 150 | 210 | within | poll_grade.STATED_US[(1, 2, 2)] aecp; declaring-outputs-part1/aecp-fanout |
| item.aecp_long | 0 | 0 | 0 | 365 | within | poll_grade.STATED_US[(1, 2, 2)] aecp_long; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0 | 0 | 735 | within | load_grade.stated(1x1/1if) GRADED item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0 | 0 | 735 | within | load_grade.stated(1x1/1if) STATED_US item.mrpdu; answering-every-port-part0/notice-every-4 |
| item.mrpdu | 0 | 0 | 0 | 735 | within | poll_grade.STATED_US[(1, 2, 2)] mrpdu; answering-every-port-part0/notice-every-4 |
| item.rebuild | 18,186 | 17,214 | 195 | 290 | within | poll_grade.STATED_US[(1, 2, 2)] rebuild; answering-ports-part1/adp-link |
| item.reclaim | 1,767 | 1,613 | 20 | 25 | within | load_grade.stated(1x1/1if) GRADED item.reclaim; none-part19/srp |
| item.reclaim | 1,767 | 1,613 | 20 | 25 | within | load_grade.stated(1x1/1if) STATED_US item.reclaim; none-part19/srp |
| item.reclaim | 1,767 | 1,613 | 20 | 25 | within | poll_grade.STATED_US[(1, 2, 2)] reclaim; none-part19/srp |
| item.record | 24,268 | 22,867 | 255 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; answering-every-port-part2/notice-every-6 |
| item.retained | 0 | 0 | 0 | 285 | within | load_grade.stated(1x1/1if) GRADED item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0 | 0 | 285 | within | load_grade.stated(1x1/1if) STATED_US item.retained; answering-every-port-part0/notice-every-4 |
| item.retained | 0 | 0 | 0 | 285 | within | poll_grade.STATED_US[(1, 2, 2)] retained; answering-every-port-part0/notice-every-4 |
| item.walk | 2,105 | 1,961 | 25 | 35 | within | load_grade.stated(1x1/1if) GRADED item.walk; none-part19/srp |
| item.walk | 2,105 | 1,961 | 25 | 35 | within | load_grade.stated(1x1/1if) STATED_US item.walk; none-part19/srp |
| item.walk | 2,105 | 1,961 | 25 | 35 | within | poll_grade.STATED_US[(1, 2, 2)] walk; none-part19/srp |
| item.withdraw | 4,789 | 4,680 | 55 | 90 | within | poll_grade.STATED_US[(1, 2, 2)] withdraw; none-part20/backlog |
| record.acmp | 19,427 | 19,166 | 205 | 265 | within | load_grade.stated(1x1/1if) GRADED record.acmp; answering-ports-part16/fixture.log |
| record.acmp | 19,427 | 19,166 | 205 | 280 | within | load_grade.stated(1x1/1if) STATED_US record.acmp; answering-ports-part16/fixture.log |
| record.adp | 9,585 | 8,901 | 105 | 100 | **OVER** | load_grade.stated(1x1/1if) GRADED record.adp; answering-ports-part3/backlog-adp-refill.log |
| record.adp | 9,585 | 8,901 | 105 | 105 | within | load_grade.stated(1x1/1if) STATED_US record.adp; answering-ports-part3/backlog-adp-refill.log |
| record.maap | 10,411 | 10,250 | 110 | 115 | within | load_grade.stated(1x1/1if) GRADED record.maap; talker-notices-part0/talker-notice-0.log |
| record.maap | 10,411 | 10,250 | 110 | 115 | within | load_grade.stated(1x1/1if) STATED_US record.maap; talker-notices-part0/talker-notice-0.log |
| record.srp | 24,662 | 23,153 | 260 | 285 | within | load_grade.stated(1x1/1if) GRADED record.srp; answering-every-port-part2/notice-every-6.log |
| record.srp | 24,662 | 23,153 | 260 | 285 | within | load_grade.stated(1x1/1if) STATED_US record.srp; answering-every-port-part2/notice-every-6.log |
| step | 81,365 | 81,188 | 855 | 975 | within | load_grade.stated(1x1/1if) GRADED step; answering-ports-part8/backlog-adp@program-aged2-4 |
| step | 81,365 | 81,188 | 855 | 975 | within | load_grade.stated(1x1/1if) STATED_US step; answering-ports-part8/backlog-adp@program-aged2-4 |
| step | 81,365 | 81,188 | 855 | 975 | within | whole_grade.stated_us((1, 2, 2)) step (ctrl_loop.h); answering-ports-part8/backlog-adp@program-aged2-4 |
| item.aecp.notice | 14,084 | 14,111 | 150 | 210 | within | load_grade.stated(1x1/1if) GRADED item.aecp.notice; declaring-outputs-part1/aecp-fanout (16 frame(s)) |
| item.aecp.notice | 14,084 | 14,111 | 150 | 210 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.notice; declaring-outputs-part1/aecp-fanout (16 frame(s)) |
| item.aecp.response | 2,844 | 2,642 | 30 | 60 | within | load_grade.stated(1x1/1if) GRADED item.aecp.response; none-part2/backlog-owed (1 frame(s)) |
| item.aecp.response | 2,844 | 2,642 | 30 | 60 | within | load_grade.stated(1x1/1if) STATED_US item.aecp.response; none-part2/backlog-owed (1 frame(s)) |
| event.AMAP_LIVE_WRITE | 1,884 | 1,823 | 20 | 30 | within | rows_tiers.DATAPATH_US[1x1/1if] AMAP_LIVE_WRITE; datapath-events.log@72134673 |
| event.AS_PATH_CHANGED | 2,808 | 2,895 | 30 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AS_PATH_CHANGED; datapath-events.log@71933925 |
| event.AVB_INFO_CHANGED | 2,296 | 2,662 | 25 | 35 | within | rows_tiers.DATAPATH_US[1x1/1if] AVB_INFO_CHANGED; datapath-events.log@67532497 |

**The long notice** (`compare-long.txt`):

- item.aecp_long (the polls): 29,652 CPU cycles, 315 us by the rule, against aecp_long 365 us at 1x1/1if: within; none-part19/aecp-largest-notice
- the notice kind (aecp_kinds.py): 29,652 CPU cycles, 315 us by the rule, against aecp_long 365 us at 1x1/1if: within; none-part19/aecp-largest-notice (15 frame(s))
- # 0 exceeded

**The AECP records by class** (`record_classes.py`):

- 1x1/1if reported long: the dearest 91,923 CPU cycles, 970 us by the rule, stated 975 us (declaring-outputs aecp-largest-notice: the largest legal command's)
- 1x1/1if held long: the dearest 91,641 CPU cycles, 965 us by the rule, stated 975 us (answering-ports aecp-largest-notice: the largest legal command's)
- 1x1/1if reported other: the dearest 20,554 CPU cycles, 220 us by the rule, stated 245 us (answering-later notice-retried-0: command 0x0010)
- 1x1/1if held other: the dearest 23,726 CPU cycles, 250 us by the rule, stated 245 us (declaring-outputs aecp-fanout: command 0x000e)
- 1x1/1if reported paced: the dearest 30,839 CPU cycles, 325 us by the rule, stated 310 us (declaring-outputs aecp-fanout: REMOVE_AUDIO_MAPPINGS, paced)
- 1x1/1if held paced: the dearest 29,993 CPU cycles, 315 us by the rule, stated 310 us (answering-ports aecp-fanout: REMOVE_AUDIO_MAPPINGS, paced)
- REPORTED 1x1/1if declaring-outputs aecp-fanout: a record of 30,839 CPU cycles, 325 us by the rule, over the paced record's 310 us (REMOVE_AUDIO_MAPPINGS, paced)
- REFUSED 1x1/1if answering-ports aecp-fanout: a record of 29,993 CPU cycles, 315 us by the rule, over the paced record's 310 us (REMOVE_AUDIO_MAPPINGS, paced)
- REFUSED 1x1/1if declaring-outputs aecp-fanout: a record of 23,726 CPU cycles, 250 us by the rule, over the other record's 245 us (command 0x000e)
- RESULT: FAIL

