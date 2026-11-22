
// Reviewer probe (R883-1): the outage a PHC step causes, per port: time not asCapable after first
// rising, role changes, grandmaster identity changes seen by the slave.
static void outage_run(Net &n, long double a_base, long double b_base, long double turn, const char *tag)
{
	g_turn_ns = turn;
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
	g_turn_ns = 0.0L;
}

TEST_F(Net, OutageTai1ms) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 1e6L, "TAI GM vs PHC 0, 1 ms turnaround"); }
TEST_F(Net, OutageTai10ms) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 1e7L, "TAI GM vs PHC 0, 10 ms turnaround"); }
TEST_F(Net, OutageOneSecond1ms) { outage_run(*this, 2'000'000'000.0L, 1'000'000'000.0L, 1e6L, "1 s initial offset, 1 ms turnaround"); }
TEST_F(Net, OutageHundredMs1ms) { outage_run(*this, 1'100'000'000.0L, 1'000'000'000.0L, 1e6L, "100 ms initial offset, 1 ms turnaround"); }
TEST_F(Net, OutageTai200us) { outage_run(*this, 1'795'000'000'000'000'000.0L, 0.0L, 2e5L, "TAI GM vs PHC 0, 0.2 ms turnaround"); }
TEST_F(Net, OutageNoStep1ms) { outage_run(*this, 1'000'000'000.0L, 1'000'000'000.0L - 10'000.0L, 1e6L, "10 us initial offset (under the 20 us threshold), 1 ms turnaround"); }
