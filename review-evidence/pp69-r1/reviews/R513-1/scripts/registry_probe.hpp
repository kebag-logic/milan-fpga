// Reviewer-owned tuple model; included only in a disposable test copy.
#include <map>
#include <tuple>
static void reviewer_registry_probe(PortHarness& h) {
  using Key = std::tuple<uint64_t,uint64_t,unsigned>;
  std::map<Key,uint16_t> rows;
  uint32_t seed=0x5130069u;
  auto random = [&]() { seed ^= seed << 13; seed ^= seed >> 17; seed ^= seed << 5; return seed; };
  auto check = [&](bool ok,const char* label,unsigned i) {
    ++h.checks;
    if (!ok) { ++h.fails; printf("FAIL: reviewer tuple %s step %u\n",label,i); }
  };
  h.quiet_inputs(); h.warm_reset(); h.now=10000;
  for (unsigned i=0; i<1024; ++i) {
    if (i && i%127==0) { h.warm_reset(); rows.clear(); }
    const uint64_t eid=(random()&1) ? h.EID_E : h.EID_F;
    const uint64_t mac=(random()&1) ? h.MAC_E : h.MAC_F;
    const unsigned port=random()&1;
    const bool remove=(random()%3)==0;
    const Key key{eid,mac,port};
    uint64_t expected=0;
    if (remove) rows.erase(key);
    else if (!rows.count(key)) {
      if (rows.size()==2) expected=h.NO_RESOURCES;
      else rows[key]=0;
    }
    check(h.op(remove ? h.OP_DEREGISTER : h.OP_REGISTER,eid,mac,port)==expected,"result",i);
    check(h.rows()==rows.size(),"occupancy",i);
    if (i%11==0) {
      h.name_changed();
      auto jobs=h.round(h.now+64);
      std::vector<std::pair<uint64_t,uint16_t>> actual,expected_jobs;
      for (auto& j:jobs) actual.emplace_back(j.mac,j.seq);
      for (auto& r:rows) { expected_jobs.emplace_back(std::get<1>(r.first),r.second); ++r.second; }
      std::sort(actual.begin(),actual.end()); std::sort(expected_jobs.begin(),expected_jobs.end());
      check(actual==expected_jobs,"fanout-and-sequence",i);
    }
  }
  printf("REVIEWER tuple model: 1024 operations, 8 resets, 94 notification rounds\n");
}
