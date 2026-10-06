int PortHarness::run() {
  const milan::tb::Model<VKL_aecp_notify> model;
  d = model.get();
  quiet_inputs();
  warm_reset();
  // Each iteration exercises one of the 32 rows at the production controller depth.
  for (unsigned target = 0; target < 32; ++target) {
    quiet_inputs(); warm_reset(); arms.clear();
    bool registered = true;
    for (unsigned port = 0; port < 2; ++port) {
      for (unsigned i = 0; i < 16; ++i) {
        const unsigned r = 2 * i + port;
        registered &= op(OP_REGISTER, eid_of(r+1), mac_of(r+1), port, true) == 0;
      }
      CHECK(op(OP_REGISTER, eid_of(60+port), mac_of(60+port), port) == NO_RESOURCES,
            "CAP capacity: interface %u rejects entry 17, iteration %u", port,target);
    }
    CHECK(registered && rows() == 32, "CAP capacity: all 32 registrations held, iteration %u",target);
    bool tags = arms.size() == 32;
    for (unsigned p = 0; p < 2; ++p) for (unsigned i = 0; i < 16; ++i) {
      const unsigned k=16*p+i;
      if (k < arms.size()) tags &= arms[k] == Arm{false,false,tl_slot(2*i+p),unsigned(OWN_TL)|i};
    }
    CHECK(tags, "CAP time-limited tags and slots cover both ports and all 16 owners, iteration %u",target);
    const int draws = serve_draws(256);
    CHECK(draws == 32, "CAP independent initial monitor draws = 32, got %d",draws);
    bool mtags = arms.size() == 64;
    for (unsigned r=0; r<32; ++r) {
      if (32+r < arms.size()) mtags &= arms[32+r] == Arm{true,false,mon_slot(r),unsigned(OWN_MON)|(r/2)};
    }
    CHECK(mtags, "CAP monitor tags and slots cover both ports and all 16 owners, iteration %u",target);
    monitor_due(target); d->ca_ready_i=1;
    Face f; watch_for(f,80);
    CHECK(f.probes.size()==1 && f.probes[0]==std::make_pair(target/2,eid_of(target+1)),
          "CAP monitor expiry targets row %u and owner %u",target,target/2);
    report(true,target/2); tick(); report_end();
    const int redraws=serve_draws(160);
    CHECK(redraws==1 && rows()==32,"CAP response rearms only row %u",target);
    monitor_due(target); d->ca_ready_i=1;
    Face second; watch_for(second,80);
    CHECK(second.probes.size()==1 && second.probes[0]==std::make_pair(target/2,eid_of(target+1)),
          "CAP second expiry targets same row %u",target);
    report(false,target/2); tick(); report_end(); idle(16);
    const Job j=presented(now+256); if (j.ms) retire();
    CHECK(rows()==31 && j.ms && j.kind==KIND_DEREG && j.mac==mac_of(target+1),
          "CAP failure removes only row %u and not its same-owner sibling",target);
    CHECK(op(OP_REGISTER,eid_of(60),mac_of(60),1-(target%2))==NO_RESOURCES,
          "CAP hole in row %u cannot be consumed by other interface",target);
    CHECK(op(OP_REGISTER,eid_of(61),mac_of(61),target%2)==0 && rows()==32,
          "CAP refill claims only the freed interface row %u",target);
    // Independent TIME_LIMITED route for this same row after its reuse.
    CHECK(op(OP_REGISTER,eid_of(61),mac_of(61),target%2,true)==0,"CAP refresh of replacement row %u",target);
    expire(tl_slot(target),unsigned(OWN_TL)|(target/2)); idle(16);
    const Job x=presented(now+256); if (x.ms) retire();
    CHECK(rows()==31 && x.ms && x.kind==KIND_DEREG && x.mac==mac_of(61),
          "CAP TIME_LIMITED expiry removes replacement row %u alone",target);
  }
  return fails ? 1 : 0;
}
