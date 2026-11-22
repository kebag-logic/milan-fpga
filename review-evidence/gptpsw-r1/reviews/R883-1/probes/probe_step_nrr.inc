// Reviewer probe (R883-1): what the port does across a large PHC step.
// Appended to a scratch copy of test_gptp.cpp inside its anonymous namespace.
static void probe_run(Net &n, long double gm_base, long double sl_base, const char *tag)
{
	n.phc[0] = {+20.0, gm_base};   // A, grandmaster (priority1 246)
	n.phc[1] = {-20.0, sl_base};   // B, slave
	n.start(246, 248);
	int drops[2] = {0, 0};
	bool was[2] = {false, false};
	int32_t worst_pd[2] = {0, 0};
	int32_t worst_nrr[2] = {0, 0};
	uint32_t first_lock_ms = 0, relock_ms = 0, drop_ms = 0;
	for (uint32_t ms = 0; ms < 30000; ms += 10) {
		n.run(10);
		for (unsigned i = 0; i < 2; i++) {
			bool c = n.port[i].pd.as_capable;
			if (was[i] && !c) {
				drops[i]++;
				if (!drop_ms) drop_ms = ms;
			}
			if (!was[i] && c && i == 1) {
				if (!first_lock_ms) first_lock_ms = ms; else if (!relock_ms) relock_ms = ms;
			}
			was[i] = c;
			if (n.port[i].pd.d_n && std::abs(n.port[i].pd.delay_ns) > std::abs(worst_pd[i]))
				worst_pd[i] = n.port[i].pd.delay_ns;
			if (n.port[i].pd.nrr_ok && std::abs(n.port[i].pd.nrr_q32) > std::abs(worst_nrr[i]))
				worst_nrr[i] = n.port[i].pd.nrr_q32;
		}
	}
	double worst = 0;
	for (size_t i = n.offsets.size() - 500; i < n.offsets.size(); i++)
		worst = std::fmax(worst, std::fabs(n.offsets[i]));
	std::printf("[PROBE] %s: steps(B) %u, asCapable drops A %d B %d (first drop at %u ms), B asCap first %u ms relock %u ms, "
		    "worst |delay| A %d B %d ns, worst |nrr-1| A %.6f B %.6f, last 5 s worst |offset| %.1f ns, roles A %d B %d\n",
		    tag, n.port[1].ctr.steps, drops[0], drops[1], drop_ms, first_lock_ms, relock_ms, worst_pd[0], worst_pd[1],
		    worst_nrr[0] / 4294967296.0, worst_nrr[1] / 4294967296.0, worst, int(n.port[0].role), int(n.port[1].role));
}

TEST_F(Net, ProbeSmallInitialOffsetNoDrop)
{
	probe_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 1'000'000.0L, "1 ms initial offset");
}

TEST_F(Net, ProbeTaiGrandmasterAgainstPhcAtZero)
{
	// a grandmaster on the PTP timescale (about 1.8e18 ns since 1970) against a PHC that starts at zero
	probe_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, "TAI GM, PHC at 0");
}

TEST_F(Net, ProbeThousandSeconds)
{
	probe_run(*this, 1'000'000'000'000.0L, 3'000'000.0L, "1000 s initial offset (the suite's own case)");
}

TEST_F(Net, ProbeTurn1msThousandSeconds)
{
	g_turn_ns = 1'000'000.0L;   // a 1 ms responder turnaround
	probe_run(*this, 1'000'000'000'000.0L, 3'000'000.0L, "1 ms turnaround, 1000 s initial offset");
	g_turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn1msTai)
{
	g_turn_ns = 1'000'000.0L;
	probe_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, "1 ms turnaround, TAI GM, PHC at 0");
	g_turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn1msSmall)
{
	g_turn_ns = 1'000'000.0L;
	probe_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 1'000'000.0L, "1 ms turnaround, 1 ms initial offset");
	g_turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn10msTai)
{
	g_turn_ns = 10'000'000.0L;   // the 802.1AS-2011 B.2.3 bound
	probe_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, "10 ms turnaround, TAI GM, PHC at 0");
	g_turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn10msNoStep)
{
	g_turn_ns = 10'000'000.0L;
	probe_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 10'000.0L, "10 ms turnaround, 10 us initial offset (no step)");
	g_turn_ns = 0.0L;
}
