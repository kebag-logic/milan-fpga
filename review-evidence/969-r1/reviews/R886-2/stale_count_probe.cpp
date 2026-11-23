// Reviewer probe (not part of the PR): the kept count after an interface reset, or after a kept Talker left and its
// block was reclaimed, while below the bound, followed by ONE receive carrying a Talker Advertise for every
// STREAM_INPUT's StreamID (a bridge re-declaring after a link flap). Each input bound later must declare its Listener
// in THE TRANSMIT's next MRPDU. ZProbeFresh is the control: the same receive into a fresh registrar.
class SrpStaleCountProbe : public SrpEarlyTalker {
protected:
    // one MRPDU: a Talker Advertise message for each of streams 0 .. CTRL_SRP_SINKS-1
    std::vector<uint8_t> every_input_in_one() {
        auto f = talker(0, kAdvertise, kJoinIn);
        for (unsigned k = 1; k < CTRL_SRP_SINKS; ++k) f = then(f, talker(k, kAdvertise, kJoinIn));
        return f;
    }
    void bind_every_input(const std::string &words) {
        quiet(400);
        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) expect_bound_declares(k, k, kAdvertise, words);
    }
};

TEST_F(SrpStaleCountProbe, ZProbeFreshOneReceiveOfEveryInput) {
    settle(); advance(400);
    offer(every_input_in_one());
    bind_every_input("fresh: one receive of every input");
}

TEST_F(SrpStaleCountProbe, ZProbeResetThenOneReceiveOfEveryInput) {
    settle(); advance(400);
    offer(talker(0x90u, kAdvertise, kJoinIn));   // one unrelated Talker kept, below the bound
    quiet(400);
    mbx_model_set_link(&model, 0, false); settle(); mbx_model_set_link(&model, 0, true); settle(); advance(400);
    offer(every_input_in_one());
    bind_every_input("after a reset: one receive of every input");
}

TEST_F(SrpStaleCountProbe, ZProbeReclaimThenOneReceiveOfEveryInput) {
    settle(); advance(400);
    offer(talker(0x90u, kAdvertise, kJoinIn));   // one unrelated Talker kept, below the bound
    quiet(400);
    offer(talker(0x90u, kAdvertise, kLv));        // it leaves; past its leave timer its block is reclaimed
    advance(5100); settle();
    offer(every_input_in_one());
    bind_every_input("after a reclaim: one receive of every input");
}

