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
	turn_ns = 1'000'000.0L;   // a 1 ms responder turnaround
	probe_run(*this, 1'000'000'000'000.0L, 3'000'000.0L, "1 ms turnaround, 1000 s initial offset");
	turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn1msTai)
{
	turn_ns = 1'000'000.0L;
	probe_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, "1 ms turnaround, TAI GM, PHC at 0");
	turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn1msSmall)
{
	turn_ns = 1'000'000.0L;
	probe_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 1'000'000.0L, "1 ms turnaround, 1 ms initial offset");
	turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn10msTai)
{
	turn_ns = 10'000'000.0L;   // the 802.1AS-2011 B.2.3 bound
	probe_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, "10 ms turnaround, TAI GM, PHC at 0");
	turn_ns = 0.0L;
}

TEST_F(Net, ProbeTurn10msNoStep)
{
	turn_ns = 10'000'000.0L;
	probe_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 10'000.0L, "10 ms turnaround, 10 us initial offset (no step)");
	turn_ns = 0.0L;
}

// Reviewer probe (R883-1): the outage a PHC step causes, per port: time not asCapable after first
// rising, role changes, grandmaster identity changes seen by the slave.
static void outage_run(Net &n, long double a_base, long double b_base, long double turn, const char *tag)
{
	n.turn_ns = turn;
	n.phc[0] = {+20.0, a_base};
	n.phc[1] = {-20.0, b_base};
	n.start(246, 248);
	bool up[2] = {false, false}, rose[2] = {false, false};
	uint32_t down_ms[2] = {0, 0};
	int role_changes[2] = {0, 0};
	int prev_role[2] = {-1, -1};
	unsigned gm_changes = 0;
	uint64_t prev_gm = 0;
	for (uint32_t ms = 0; ms < 30000; ms += 10) {
		n.run(10);
		for (unsigned i = 0; i < 2; i++) {
			up[i] = n.port[i].pd.as_capable;
			if (up[i]) rose[i] = true;
			if (rose[i] && !up[i]) down_ms[i] += 10;
			int r = int(n.port[i].role);
			if (prev_role[i] >= 0 && r != prev_role[i]) role_changes[i]++;
			prev_role[i] = r;
		}
		if (n.port[1].pub.gm_id != prev_gm) { gm_changes++; prev_gm = n.port[1].pub.gm_id; }
	}
	std::printf("[OUTAGE] %s: not asCapable after first rising A %u ms, B %u ms; role changes A %d B %d; "
		    "B grandmaster changes %u; B steps %u; final roles A %d B %d\n", tag, down_ms[0], down_ms[1],
		    role_changes[0], role_changes[1], gm_changes, n.port[1].ctr.steps, int(n.port[0].role), int(n.port[1].role));
	n.turn_ns = 0.0L;
}

TEST_F(Net, OutageTai1ms) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 1e6L, "TAI GM vs PHC 0, 1 ms turnaround"); }
TEST_F(Net, OutageTai10ms) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 1e7L, "TAI GM vs PHC 0, 10 ms turnaround"); }
TEST_F(Net, OutageOneSecond1ms) { outage_run(*this, 2'000'000'000.0L, 1'000'000'000.0L, 1e6L, "1 s initial offset, 1 ms turnaround"); }
TEST_F(Net, OutageHundredMs1ms) { outage_run(*this, 1'100'000'000.0L, 1'000'000'000.0L, 1e6L, "100 ms initial offset, 1 ms turnaround"); }
TEST_F(Net, OutageTai200us) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 2e5L, "TAI GM vs PHC 0, 0.2 ms turnaround"); }
TEST_F(Net, OutageNoStep1ms) { outage_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 10'000.0L, 1e6L, "10 us initial offset (under the 20 us threshold), 1 ms turnaround"); }

// R883-2 rows on R883-1's outage table: initial offsets between the locked step threshold and the rate envelope's span
TEST_F(Net, OutageFwd300us10ms) { outage_run(*this, 1'000'300'000.0L, 1'000'000'000.0L, 1e7L, "300 us initial offset (B behind), 10 ms turnaround"); }
TEST_F(Net, OutageFwd400us10ms) { outage_run(*this, 1'000'400'000.0L, 1'000'000'000.0L, 1e7L, "400 us initial offset (B behind), 10 ms turnaround"); }
TEST_F(Net, OutageBack400us10ms) { outage_run(*this, 1'000'000'000.0L, 1'000'400'000.0L, 1e7L, "400 us initial offset (B ahead), 10 ms turnaround"); }
TEST_F(Net, OutageBack475us5ms) { outage_run(*this, 1'000'000'000.0L, 1'000'475'000.0L, 5e6L, "475 us initial offset (B ahead), 5 ms turnaround"); }
TEST_F(Net, OutageFwd300us1ms) { outage_run(*this, 1'000'300'000.0L, 1'000'000'000.0L, 1e6L, "300 us initial offset (B behind), 1 ms turnaround (control)"); }
