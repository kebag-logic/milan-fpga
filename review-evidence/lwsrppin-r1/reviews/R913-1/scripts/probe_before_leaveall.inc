// Probe (review only, never committed): a withdrawal d ms BEFORE the board's own LeaveAll MRPDU.
// Appended inside the anonymous namespace of a scratch copy of srp_own_leaveall.cpp.
// ProbeA records, on a fresh fixture, the time L of the board's first LeaveAll MRPDU carrying input 0's Join after
// every input is bound. ProbeB(d) replays the same deterministic run to L - d, unbinds input 0, and reports whether
// that Listener's Lv left within 240 ms, and whether the LeaveAll still left at L.
uint32_t probe_la_ms = 0;
TEST_F(OwnLeaveAll, ProbeARecordsTheFirstOwnLeaveAll) {
    start_peer(3000);
    bind_every_input();
    probe_la_ms = own_leave_all_with(0, 0);
    std::printf("PROBE-A first_own_leaveall_ms=%u\n", probe_la_ms);
    ASSERT_GT(probe_la_ms, 0u);
}
class ProbeBefore : public OwnLeaveAll, public ::testing::WithParamInterface<unsigned> {};
TEST_P(ProbeBefore, WithdrawalBeforeOwnLeaveAll) {
    const unsigned d = GetParam();
    ASSERT_GT(probe_la_ms, d);
    start_peer(3000);
    bind_every_input();
    run_until(probe_la_ms - d);
    const uint32_t asked = model.now_ms;
    const size_t from = board.size();
    unbind(0);
    run_until(asked + kLvBoundMs + 50u);
    uint32_t lv = 0, la = 0; bool sent = false;
    for (size_t n = from; n < board.size(); ++n) {
        if (!la && board[n].leave_all) la = board[n].ms;
        if (!sent && board[n].listener[0] == static_cast<int>(kEvLv)) { sent = true; lv = board[n].ms; }
    }
    run_until(asked + 8000u);
    std::printf("PROBE-B before_ms=%u withdrawn_ms=%u leaveall_ms=%u lv=%s%u peer_left_ms=%u leaves=%u\n", d, asked,
                la, sent ? "" : "none>", sent ? lv : asked + kLvBoundMs + 50u, peer_record.left_ms[0],
                peer_record.leaves[0]);
}
INSTANTIATE_TEST_SUITE_P(Before, ProbeBefore, ::testing::Values(5u, 50u, 100u, 150u, 200u, 400u));
