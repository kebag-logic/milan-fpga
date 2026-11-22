// Reviewer probe (#956): the changed destination's wire time at every withdrawal phase, with the join timer in any
// state. HELD: the loop held a JoinTime and THE TRANSMIT's figure from the tick that ends the count, as the shipped
// latest-case test holds it, without its idle-timer precondition. FREE: the loop serviced throughout. Appended to a
// disposable copy of sw/firmware/ctrl/test/srp_talker.cpp; never part of the reviewed tree.
class ReviewerPhase : public Talker {
protected:
void reviewer_phase(unsigned phase, bool held) {
    auto &t=*this;
    t.settle(); t.gate(1u,kBaseA); t.advance(phase);
    while (t.model.tick_div!=0u) t.advance(1);
    t.trace();
    const uint32_t first=t.model.tx_sent;
    const uint32_t at=t.model.now_ms;
    t.gate(0u,kBaseA); t.settle();
    t.advance(2000);
    t.gate(1u,kBaseB);
    if (held) {
        t.advance_to(at+kHoldOffMs-100u);
        for (unsigned k=0;k<1000u && t.adapter.held_cs[0]>1u;++k) t.advance_to(t.model.now_ms+1u);
        while (t.model.tick_div!=9u) t.advance(1);
        unsigned busy=0;
        for (unsigned i=0;i<MBX_N_IF;++i) busy+=t.adapter.join_left[2u*i]!=0u;
        mbx_model_advance_ms(&t.model,1u+kLatestMs);
        t.settle();
        t.advance(1500);
        printf("PROBE held phase %u: join timers busy at the count's end %u\n",phase,busy);
    } else {
        t.advance_to(at+kTwoLongestLeaveAllMs+1500u);
    }
    t.untrace();
    for (unsigned i=0;i<MBX_N_IF;++i) {
        const auto ds=t.talker(i,0,first);
        const auto *lv=t.leave(ds,1);
        ASSERT_NE(lv,nullptr);
        const auto *adv=t.declared(ds,1,lv->time_ms+1u);
        ASSERT_NE(adv,nullptr) << "declared within the observation";
        printf("PROBE %s phase %u if%u: request-to-wire %u ms (deadline %u)\n",held?"held":"free",phase,i,
               unsigned(adv->time_ms-at),kTwoLongestLeaveAllMs);
        EXPECT_LE(adv->time_ms,at+kTwoLongestLeaveAllMs) << "PROBE: on the wire within 30.0 s of the request";
        EXPECT_GE(adv->time_ms,at+kHoldOffMs) << "PROBE: not before the hold-off";
    }
}
};
#define REVIEWER_PHASE(p) \
    TEST_F(ReviewerPhase, Held##p) { reviewer_phase(p,true); } \
    TEST_F(ReviewerPhase, Free##p) { reviewer_phase(p,false); }
REVIEWER_PHASE(0) REVIEWER_PHASE(100) REVIEWER_PHASE(200) REVIEWER_PHASE(300) REVIEWER_PHASE(400)
REVIEWER_PHASE(500) REVIEWER_PHASE(600) REVIEWER_PHASE(700) REVIEWER_PHASE(800) REVIEWER_PHASE(900)
