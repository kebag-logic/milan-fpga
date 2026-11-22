
// ---- reviewer probe (R883-2): steps between the locked step threshold and the rate envelope's span ----
// Same fixture as the step-across-the-link matrix; the slave B is behind (or ahead of) A by `off` ns.
struct MidStep : Net {
	void diag(long double off, long double turn)
	{
		turn_ns = turn;
		phc[0] = {+20.0, 1'000'000'000.0L + off};
		phc[1] = {-20.0, 1'000'000'000.0L};
		start(246, 248);
		bool rose[2] = {false, false};
		uint32_t down_ms[2] = {0, 0};
		int32_t dmax[2] = {INT32_MIN, INT32_MIN};
		int32_t nmax[2] = {0, 0};
		for (uint32_t ms = 0; ms < 30'000; ms += 10) {
			run(10);
			for (unsigned i = 0; i < 2; i++) {
				rose[i] = rose[i] || port[i].pd.as_capable;
				if (rose[i] && !port[i].pd.as_capable)
					down_ms[i] += 10;
				if (rose[i]) {
					dmax[i] = std::max(dmax[i], port[i].pd.delay_ns);
					nmax[i] = std::max(nmax[i], std::abs(port[i].pd.nrr_q32));
				}
			}
		}
		printf("PROBE off_ns=%.0Lf turn_ns=%.0Lf steps=%u A_down_ms=%u B_down_ms=%u A_delay_max=%d B_delay_max=%d "
		       "A_nrr_max_ppm=%.1f B_nrr_max_ppm=%.1f\n",
		       off, turn, port[1].ctr.steps, down_ms[0], down_ms[1], dmax[0], dmax[1],
		       nmax[0] / 4294.967296, nmax[1] / 4294.967296);
		EXPECT_EQ(down_ms[0], 0u);
		EXPECT_EQ(down_ms[1], 0u);
	}
};
#define MID(name, off, turn) TEST_F(MidStep, name) { diag(off, turn); }
MID(Fwd150us_10ms, 150'000.0L, 1e7L)
MID(Fwd300us_10ms, 300'000.0L, 1e7L)
MID(Fwd450us_10ms, 450'000.0L, 1e7L)
MID(Fwd600us_10ms, 600'000.0L, 1e7L)
MID(Fwd700us_10ms, 700'000.0L, 1e7L)
MID(Fwd1ms_10ms, 1'000'000.0L, 1e7L)
MID(Back300us_10ms, -300'000.0L, 1e7L)
MID(Back600us_10ms, -600'000.0L, 1e7L)
MID(Fwd300us_1ms, 300'000.0L, 1e6L)
MID(Fwd600us_1ms, 600'000.0L, 1e6L)
MID(Fwd300us_5ms, 300'000.0L, 5e6L)
MID(Fwd100ms_10ms, 100'000'000.0L, 1e7L)
