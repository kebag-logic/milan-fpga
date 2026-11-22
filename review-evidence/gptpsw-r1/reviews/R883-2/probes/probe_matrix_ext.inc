
// ---- reviewer probe (R883-2): the suite's own step-across-the-link matrix, extended to steps the rate
// envelope admits (above the 100 us locked threshold, under 244 ppm of the window's span) ----
TEST_F(Net, ProbeAForwardStepOf300usAt10msTurnaround) { step_across_the_link(1'000'300'000.0L, 1'000'000'000.0L, 1e7L); }
TEST_F(Net, ProbeAForwardStepOf400usAt10msTurnaround) { step_across_the_link(1'000'400'000.0L, 1'000'000'000.0L, 1e7L); }
TEST_F(Net, ProbeABackwardStepOf400usAt10msTurnaround) { step_across_the_link(1'000'000'000.0L, 1'000'400'000.0L, 1e7L); }
TEST_F(Net, ProbeABackwardStepOf475usAt5msTurnaround) { step_across_the_link(1'000'000'000.0L, 1'000'475'000.0L, 5e6L); }
TEST_F(Net, ProbeAForwardStepOf150usAt10msTurnaround) { step_across_the_link(1'000'150'000.0L, 1'000'000'000.0L, 1e7L); }
