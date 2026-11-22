
// ---- reviewer probe (R883-2): sweep of slave-step sizes against the grandmaster port's asCapable ----
struct MidSweep : Net {
	void one(long double off, long double turn)
	{
		turn_ns = turn;
		phc[0] = {+20.0, 1'000'000'000.0L + off};
		phc[1] = {-20.0, 1'000'000'000.0L};
		start(246, 248);
		bool rose[2] = {false, false}, synced = false;
		uint32_t down_ms[2] = {0, 0}, unsynced_ms = 0;
		int32_t dmax = INT32_MIN;
		for (uint32_t ms = 0; ms < 30'000; ms += 10) {
			run(10);
			for (unsigned i = 0; i < 2; i++) {
				rose[i] = rose[i] || port[i].pd.as_capable;
				if (rose[i] && !port[i].pd.as_capable)
					down_ms[i] += 10;
			}
			if (rose[0])
				dmax = std::max(dmax, port[0].pd.delay_ns);
			synced = synced || port[1].pub.sync_ok;
			if (synced && !port[1].pub.sync_ok)
				unsynced_ms += 10;
		}
		printf("SWEEP off_us=%+.0Lf turn_ms=%.0Lf steps=%u A_asCapable_down_ms=%u B_asCapable_down_ms=%u "
		       "B_sync_ok_lost_ms=%u A_delay_max_ns=%d\n",
		       off / 1000, turn / 1e6, port[1].ctr.steps, down_ms[0], down_ms[1], unsynced_ms, dmax);
	}
};
TEST_F(MidSweep, M600us_1ms) { one(-600000.0L, 1000000.0L); }
TEST_F(MidSweep, M575us_1ms) { one(-575000.0L, 1000000.0L); }
TEST_F(MidSweep, M550us_1ms) { one(-550000.0L, 1000000.0L); }
TEST_F(MidSweep, M525us_1ms) { one(-525000.0L, 1000000.0L); }
TEST_F(MidSweep, M500us_1ms) { one(-500000.0L, 1000000.0L); }
TEST_F(MidSweep, M475us_1ms) { one(-475000.0L, 1000000.0L); }
TEST_F(MidSweep, M450us_1ms) { one(-450000.0L, 1000000.0L); }
TEST_F(MidSweep, M425us_1ms) { one(-425000.0L, 1000000.0L); }
TEST_F(MidSweep, M400us_1ms) { one(-400000.0L, 1000000.0L); }
TEST_F(MidSweep, M375us_1ms) { one(-375000.0L, 1000000.0L); }
TEST_F(MidSweep, M350us_1ms) { one(-350000.0L, 1000000.0L); }
TEST_F(MidSweep, M325us_1ms) { one(-325000.0L, 1000000.0L); }
TEST_F(MidSweep, M300us_1ms) { one(-300000.0L, 1000000.0L); }
TEST_F(MidSweep, M275us_1ms) { one(-275000.0L, 1000000.0L); }
TEST_F(MidSweep, M250us_1ms) { one(-250000.0L, 1000000.0L); }
TEST_F(MidSweep, M225us_1ms) { one(-225000.0L, 1000000.0L); }
TEST_F(MidSweep, M200us_1ms) { one(-200000.0L, 1000000.0L); }
TEST_F(MidSweep, M175us_1ms) { one(-175000.0L, 1000000.0L); }
TEST_F(MidSweep, M150us_1ms) { one(-150000.0L, 1000000.0L); }
TEST_F(MidSweep, M125us_1ms) { one(-125000.0L, 1000000.0L); }
TEST_F(MidSweep, M100us_1ms) { one(-100000.0L, 1000000.0L); }
TEST_F(MidSweep, M75us_1ms) { one(-75000.0L, 1000000.0L); }
TEST_F(MidSweep, M50us_1ms) { one(-50000.0L, 1000000.0L); }
TEST_F(MidSweep, M25us_1ms) { one(-25000.0L, 1000000.0L); }
TEST_F(MidSweep, P25us_1ms) { one(25000.0L, 1000000.0L); }
TEST_F(MidSweep, P50us_1ms) { one(50000.0L, 1000000.0L); }
TEST_F(MidSweep, P75us_1ms) { one(75000.0L, 1000000.0L); }
TEST_F(MidSweep, P100us_1ms) { one(100000.0L, 1000000.0L); }
TEST_F(MidSweep, P125us_1ms) { one(125000.0L, 1000000.0L); }
TEST_F(MidSweep, P150us_1ms) { one(150000.0L, 1000000.0L); }
TEST_F(MidSweep, P175us_1ms) { one(175000.0L, 1000000.0L); }
TEST_F(MidSweep, P200us_1ms) { one(200000.0L, 1000000.0L); }
TEST_F(MidSweep, P225us_1ms) { one(225000.0L, 1000000.0L); }
TEST_F(MidSweep, P250us_1ms) { one(250000.0L, 1000000.0L); }
TEST_F(MidSweep, P275us_1ms) { one(275000.0L, 1000000.0L); }
TEST_F(MidSweep, P300us_1ms) { one(300000.0L, 1000000.0L); }
TEST_F(MidSweep, P325us_1ms) { one(325000.0L, 1000000.0L); }
TEST_F(MidSweep, P350us_1ms) { one(350000.0L, 1000000.0L); }
TEST_F(MidSweep, P375us_1ms) { one(375000.0L, 1000000.0L); }
TEST_F(MidSweep, P400us_1ms) { one(400000.0L, 1000000.0L); }
TEST_F(MidSweep, P425us_1ms) { one(425000.0L, 1000000.0L); }
TEST_F(MidSweep, P450us_1ms) { one(450000.0L, 1000000.0L); }
TEST_F(MidSweep, P475us_1ms) { one(475000.0L, 1000000.0L); }
TEST_F(MidSweep, P500us_1ms) { one(500000.0L, 1000000.0L); }
TEST_F(MidSweep, P525us_1ms) { one(525000.0L, 1000000.0L); }
TEST_F(MidSweep, P550us_1ms) { one(550000.0L, 1000000.0L); }
TEST_F(MidSweep, P575us_1ms) { one(575000.0L, 1000000.0L); }
TEST_F(MidSweep, P600us_1ms) { one(600000.0L, 1000000.0L); }
TEST_F(MidSweep, M600us_5ms) { one(-600000.0L, 5000000.0L); }
TEST_F(MidSweep, M575us_5ms) { one(-575000.0L, 5000000.0L); }
TEST_F(MidSweep, M550us_5ms) { one(-550000.0L, 5000000.0L); }
TEST_F(MidSweep, M525us_5ms) { one(-525000.0L, 5000000.0L); }
TEST_F(MidSweep, M500us_5ms) { one(-500000.0L, 5000000.0L); }
TEST_F(MidSweep, M475us_5ms) { one(-475000.0L, 5000000.0L); }
TEST_F(MidSweep, M450us_5ms) { one(-450000.0L, 5000000.0L); }
TEST_F(MidSweep, M425us_5ms) { one(-425000.0L, 5000000.0L); }
TEST_F(MidSweep, M400us_5ms) { one(-400000.0L, 5000000.0L); }
TEST_F(MidSweep, M375us_5ms) { one(-375000.0L, 5000000.0L); }
TEST_F(MidSweep, M350us_5ms) { one(-350000.0L, 5000000.0L); }
TEST_F(MidSweep, M325us_5ms) { one(-325000.0L, 5000000.0L); }
TEST_F(MidSweep, M300us_5ms) { one(-300000.0L, 5000000.0L); }
TEST_F(MidSweep, M275us_5ms) { one(-275000.0L, 5000000.0L); }
TEST_F(MidSweep, M250us_5ms) { one(-250000.0L, 5000000.0L); }
TEST_F(MidSweep, M225us_5ms) { one(-225000.0L, 5000000.0L); }
TEST_F(MidSweep, M200us_5ms) { one(-200000.0L, 5000000.0L); }
TEST_F(MidSweep, M175us_5ms) { one(-175000.0L, 5000000.0L); }
TEST_F(MidSweep, M150us_5ms) { one(-150000.0L, 5000000.0L); }
TEST_F(MidSweep, M125us_5ms) { one(-125000.0L, 5000000.0L); }
TEST_F(MidSweep, M100us_5ms) { one(-100000.0L, 5000000.0L); }
TEST_F(MidSweep, M75us_5ms) { one(-75000.0L, 5000000.0L); }
TEST_F(MidSweep, M50us_5ms) { one(-50000.0L, 5000000.0L); }
TEST_F(MidSweep, M25us_5ms) { one(-25000.0L, 5000000.0L); }
TEST_F(MidSweep, P25us_5ms) { one(25000.0L, 5000000.0L); }
TEST_F(MidSweep, P50us_5ms) { one(50000.0L, 5000000.0L); }
TEST_F(MidSweep, P75us_5ms) { one(75000.0L, 5000000.0L); }
TEST_F(MidSweep, P100us_5ms) { one(100000.0L, 5000000.0L); }
TEST_F(MidSweep, P125us_5ms) { one(125000.0L, 5000000.0L); }
TEST_F(MidSweep, P150us_5ms) { one(150000.0L, 5000000.0L); }
TEST_F(MidSweep, P175us_5ms) { one(175000.0L, 5000000.0L); }
TEST_F(MidSweep, P200us_5ms) { one(200000.0L, 5000000.0L); }
TEST_F(MidSweep, P225us_5ms) { one(225000.0L, 5000000.0L); }
TEST_F(MidSweep, P250us_5ms) { one(250000.0L, 5000000.0L); }
TEST_F(MidSweep, P275us_5ms) { one(275000.0L, 5000000.0L); }
TEST_F(MidSweep, P300us_5ms) { one(300000.0L, 5000000.0L); }
TEST_F(MidSweep, P325us_5ms) { one(325000.0L, 5000000.0L); }
TEST_F(MidSweep, P350us_5ms) { one(350000.0L, 5000000.0L); }
TEST_F(MidSweep, P375us_5ms) { one(375000.0L, 5000000.0L); }
TEST_F(MidSweep, P400us_5ms) { one(400000.0L, 5000000.0L); }
TEST_F(MidSweep, P425us_5ms) { one(425000.0L, 5000000.0L); }
TEST_F(MidSweep, P450us_5ms) { one(450000.0L, 5000000.0L); }
TEST_F(MidSweep, P475us_5ms) { one(475000.0L, 5000000.0L); }
TEST_F(MidSweep, P500us_5ms) { one(500000.0L, 5000000.0L); }
TEST_F(MidSweep, P525us_5ms) { one(525000.0L, 5000000.0L); }
TEST_F(MidSweep, P550us_5ms) { one(550000.0L, 5000000.0L); }
TEST_F(MidSweep, P575us_5ms) { one(575000.0L, 5000000.0L); }
TEST_F(MidSweep, P600us_5ms) { one(600000.0L, 5000000.0L); }
TEST_F(MidSweep, M600us_10ms) { one(-600000.0L, 10000000.0L); }
TEST_F(MidSweep, M575us_10ms) { one(-575000.0L, 10000000.0L); }
TEST_F(MidSweep, M550us_10ms) { one(-550000.0L, 10000000.0L); }
TEST_F(MidSweep, M525us_10ms) { one(-525000.0L, 10000000.0L); }
TEST_F(MidSweep, M500us_10ms) { one(-500000.0L, 10000000.0L); }
TEST_F(MidSweep, M475us_10ms) { one(-475000.0L, 10000000.0L); }
TEST_F(MidSweep, M450us_10ms) { one(-450000.0L, 10000000.0L); }
TEST_F(MidSweep, M425us_10ms) { one(-425000.0L, 10000000.0L); }
TEST_F(MidSweep, M400us_10ms) { one(-400000.0L, 10000000.0L); }
TEST_F(MidSweep, M375us_10ms) { one(-375000.0L, 10000000.0L); }
TEST_F(MidSweep, M350us_10ms) { one(-350000.0L, 10000000.0L); }
TEST_F(MidSweep, M325us_10ms) { one(-325000.0L, 10000000.0L); }
TEST_F(MidSweep, M300us_10ms) { one(-300000.0L, 10000000.0L); }
TEST_F(MidSweep, M275us_10ms) { one(-275000.0L, 10000000.0L); }
TEST_F(MidSweep, M250us_10ms) { one(-250000.0L, 10000000.0L); }
TEST_F(MidSweep, M225us_10ms) { one(-225000.0L, 10000000.0L); }
TEST_F(MidSweep, M200us_10ms) { one(-200000.0L, 10000000.0L); }
TEST_F(MidSweep, M175us_10ms) { one(-175000.0L, 10000000.0L); }
TEST_F(MidSweep, M150us_10ms) { one(-150000.0L, 10000000.0L); }
TEST_F(MidSweep, M125us_10ms) { one(-125000.0L, 10000000.0L); }
TEST_F(MidSweep, M100us_10ms) { one(-100000.0L, 10000000.0L); }
TEST_F(MidSweep, M75us_10ms) { one(-75000.0L, 10000000.0L); }
TEST_F(MidSweep, M50us_10ms) { one(-50000.0L, 10000000.0L); }
TEST_F(MidSweep, M25us_10ms) { one(-25000.0L, 10000000.0L); }
TEST_F(MidSweep, P25us_10ms) { one(25000.0L, 10000000.0L); }
TEST_F(MidSweep, P50us_10ms) { one(50000.0L, 10000000.0L); }
TEST_F(MidSweep, P75us_10ms) { one(75000.0L, 10000000.0L); }
TEST_F(MidSweep, P100us_10ms) { one(100000.0L, 10000000.0L); }
TEST_F(MidSweep, P125us_10ms) { one(125000.0L, 10000000.0L); }
TEST_F(MidSweep, P150us_10ms) { one(150000.0L, 10000000.0L); }
TEST_F(MidSweep, P175us_10ms) { one(175000.0L, 10000000.0L); }
TEST_F(MidSweep, P200us_10ms) { one(200000.0L, 10000000.0L); }
TEST_F(MidSweep, P225us_10ms) { one(225000.0L, 10000000.0L); }
TEST_F(MidSweep, P250us_10ms) { one(250000.0L, 10000000.0L); }
TEST_F(MidSweep, P275us_10ms) { one(275000.0L, 10000000.0L); }
TEST_F(MidSweep, P300us_10ms) { one(300000.0L, 10000000.0L); }
TEST_F(MidSweep, P325us_10ms) { one(325000.0L, 10000000.0L); }
TEST_F(MidSweep, P350us_10ms) { one(350000.0L, 10000000.0L); }
TEST_F(MidSweep, P375us_10ms) { one(375000.0L, 10000000.0L); }
TEST_F(MidSweep, P400us_10ms) { one(400000.0L, 10000000.0L); }
TEST_F(MidSweep, P425us_10ms) { one(425000.0L, 10000000.0L); }
TEST_F(MidSweep, P450us_10ms) { one(450000.0L, 10000000.0L); }
TEST_F(MidSweep, P475us_10ms) { one(475000.0L, 10000000.0L); }
TEST_F(MidSweep, P500us_10ms) { one(500000.0L, 10000000.0L); }
TEST_F(MidSweep, P525us_10ms) { one(525000.0L, 10000000.0L); }
TEST_F(MidSweep, P550us_10ms) { one(550000.0L, 10000000.0L); }
TEST_F(MidSweep, P575us_10ms) { one(575000.0L, 10000000.0L); }
TEST_F(MidSweep, P600us_10ms) { one(600000.0L, 10000000.0L); }
