#!/usr/bin/env python3
"""Reviewer's disposable probe tests (#920), appended to a probe clone's test_nvm_write.cpp, and the three probes the
head's checks left green re-planted with these tests as their kill lists.

Usage: store_probe_tests.py PROBE_TREE (a disposable clone of the reviewed head)
  probe_first_change_after_flight: after a save that a change in flight left, a later first change still waits its
      1,000 ms first-dirty window (DR2a; the ruling refuses a shorter first-dirty window for a first change).
  probe_retry_after_rewind: after a capture that walked again, a failed attempt's retry still takes a record in
      flight changed in its backoff, and the change is durable.
  probe_rewound_walk_join: a change to a record no capture holds, marked on the capture's walk again, joins that
      capture: one save holds every change."""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
test = tree / 'sw/firmware/ctrl_nvm/test/test_nvm_write.cpp'
TESTS = r'''
// ---- reviewer probes (#920), disposable ----
TEST_P(NvmBoth, probe_first_change_after_flight) {
    Files f = fx().files({{"g.bin", "golden@5"}});
    const unsigned rid = rids().back(), first = rids().front();
    const Result r = go(port(), f,
                        {"--slot-b", "g.bin", "--boot", "--set", set_word(rid, one_change(1).second), "--until-phase",
                         num(NVM_P_SEAL), "--set", set_word(first, value(first, 9)), "--until-idle", "--run-ms", "5000",
                         "--mark", "--set", set_word(first, value(first, 10)), "--until-idle"});
    EXPECT_TRUE(r.at("ok") == 3 && in(after_mark(r, 2), 1000 * kMs, 1050 * kMs))
        << "a first change after a save a change in flight left: erase " << after_mark(r, 2)
        << " us after it, want 1,000 to 1,050 ms: " << r.text();
}

TEST_P(NvmBoth, probe_retry_after_rewind) {
    const std::vector<unsigned> ids = rids();
    const unsigned behind = ids[0], a = ids[1], b = ids.back();
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                        {"--slot-b", "g.bin", "--boot", "--set", set_word(a, value(a, 1)), "--set",
                         set_word(b, value(b, 1)), "--until-phase", num(NVM_P_CAPTURE), "--service", "1", "--set",
                         set_word(behind, value(behind, 1)), "--until-idle", "--run-ms", "5000", "--fault",
                         "program-drop:1", "--set", set_word(a, value(a, 5)), "--until-phase", num(NVM_P_ERASE_WAIT),
                         "--until-phase", num(NVM_P_IDLE), "--set", set_word(a, value(a, 6)), "--until-idle",
                         "--run-ms", "5000", "--dump-slot-a", "a.bin", "--dump-slot-b", "b.bin"});
    EXPECT_TRUE(r.at("failed") == 1 && r.at("dirty") == 0 && r.at("pending") == 0)
        << "a retry after a capture that walked again: " << r.text();
    const Result boot = go(port(), f, {"--slot-a", "a.bin", "--slot-b", "b.bin", "--boot", "--dump-state", "st"});
    EXPECT_TRUE(boot.at("auth") >= 0) << boot.text();
    expect_state(f, "st", with(fx().payloads("golden"), {{a, value(a, 6)}, {b, value(b, 1)}, {behind, value(behind, 1)}}),
                 "a retry after a capture that walked again");
}

TEST_P(NvmBoth, probe_rewound_walk_join) {
    const std::vector<unsigned> ids = rids();
    const unsigned behind = ids[0], a = ids[1], ahead = ids[2], b = ids.back();
    Files f = fx().files({{"g.bin", "golden@5"}});
    const Result r = go(port(), f,
                        {"--slot-b", "g.bin", "--boot", "--set", set_word(a, value(a, 1)), "--set",
                         set_word(b, value(b, 1)), "--until-phase", num(NVM_P_CAPTURE), "--service", "1", "--set",
                         set_word(behind, value(behind, 1)), "--service", "3", "--set", set_word(ahead, value(ahead, 1)),
                         "--until-idle"});
    EXPECT_TRUE(r.at("ok") == 1 && r.erases.size() == 1u && r.at("dirty") == 0 && r.at("pending") == 0)
        << "a change marked on the walk again joins it: " << r.text();
}
'''
text = test.read_text()
marker = '}  // namespace\n}  // namespace nvm_test'
assert text.count(marker) == 1, 'namespace end'
test.write_text(text.replace(marker, TESTS + '\n' + marker))
mut = tree / 'sw/firmware/ctrl_nvm/test/nvm_mutants.py'
m = mut.read_text()
cut = m.rfind('\n\nMUTANTS = (')
m = m[:cut] if cut >= 0 else m
m += '''

MUTANTS = (
    _m('probe_next_now_kept', STORE, '\\tnvm.next_now = 0;\\n\\tnvm.st.phase = NVM_P_CAPTURE;',
       '\\tnvm.st.phase = NVM_P_CAPTURE;', 'probe_first_change_after_flight'),
    _m('probe_rewound_kept', STORE, '\\tnvm.rewound = 0;\\n', '', 'probe_retry_after_rewind'),
    _m('probe_rewound_walk_refuses_join', STORE, '(!nvm_bit(&nvm.inflight, id) || ',
       '((!nvm.rewound && !nvm_bit(&nvm.inflight, id)) || ', 'probe_rewound_walk_join'),
)
'''
mut.write_text(m)
print('probe tests and three probes planted')
