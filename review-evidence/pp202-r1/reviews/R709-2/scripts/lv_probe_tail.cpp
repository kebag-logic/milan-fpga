// Probe (reviewer, disposable): a source's gate closes and re-opens under a
// NEW Stream ID before the next tx! (inside one T-MRP-JOIN), as the talker
// does when a declared source returns from a disable with an immediate grant.
// Records every Talker Advertise push: AttributeEvent and its StreamID.
static void dump(const char* tag, const Hn& h) {
  for (const auto& p : h.t_push) {
    uint64_t sid = 0;
    for (int i = 0; i < 8; ++i) sid = (sid << 8) | p.val[i];
    printf("%s push type=%u event=%u sid=%016llx\n", tag, p.type, p.code,
           static_cast<unsigned long long>(sid));
  }
}
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const uint64_t SIDA = 0x02AABBCCDDEE0003ull, SIDB = 0x02AABBCCDDEE0008ull;
  const uint64_t DAA = 0x91E0F0001234ull, DAB = 0x91E0F0001240ull;
  int bad = 0;
  for (int arm = 0; arm < 2; ++arm) {
    Vsrp_stream_fsms_wrap* d = new Vsrp_stream_fsms_wrap;
    Hn h(d); h.reset();
    h.gate(true, 0, SIDA, DAA, 5); h.tick(); h.tick(); h.tick();
    h.clear_logs();
    h.gate(false, 0, SIDA, DAA, 5);              // withdrawal: Lv! -> LA
    if (arm == 1) h.tick();                      // control: Lv goes out first
    h.gate(true, 0, SIDB, DAB, 5);               // re-open under the moved ID
    h.tick(); h.tick();
    const char* tag = arm ? "CONTROL(tx! between close and open)" : "PROBE(open inside one T-MRP-JOIN)";
    dump(tag, h);
    bool lv_old = false, join_new = false;
    for (const auto& p : h.t_push) {
      uint64_t sid = 0;
      for (int i = 0; i < 8; ++i) sid = (sid << 8) | p.val[i];
      if (p.type == 1 && sid == SIDA && p.code == 5) lv_old = true;
      if (p.type == 1 && sid == SIDB && (p.code == 3 || p.code == 1 || p.code == 0)) join_new = true;
    }
    printf("%s: Lv for withdrawn ID sent=%d, new ID declared=%d\n", tag, lv_old, join_new);
    if (arm == 1 && !lv_old) ++bad;              // the harness reads Lv codes right
    h.d->final(); delete d;
  }
  printf("probe harness %s\n", bad ? "BROKEN" : "OK");
  return bad;
}
