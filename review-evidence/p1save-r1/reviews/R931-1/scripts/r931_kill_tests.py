#!/usr/bin/env python3
"""R931-1: add two tests to a checkout's test_nvm_delta.cpp (disposable copy only). Usage: r931_kill_tests.py <copy>"""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sw/firmware/ctrl_nvm/test/test_nvm_delta.cpp'
s = p.read_text()
T = '''
// A frame after a whole commit carries what that commit saved, when its record is another: whole A, whole B, frame A.
TEST_P(NvmBoth, r931_frame_after_whole) {
    const unsigned rb = bind_rid();
    const unsigned rb2 = static_cast<unsigned>(fx().num("bind_rid2"));
    Files f = fx().files({{"a5.bin", "golden@5"}, {"b6.bin", "golden@6"}});
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--set",
                                              set_word(rb2, value(rb2, 8)), "--until-idle", "--set",
                                              set_word(rb2, value(rb2, 9)), "--until-idle", "--set",
                                              set_word(rb, value(rb, 9)), "--until-idle"}, kDump)));
    EXPECT_TRUE(r.at("ok") == 4 && r.at("failed") == 0) << r.text();
    const Result b = boot_dumped(port(), f);
    EXPECT_TRUE(b.at("vd_a") == NVM_VD_OK && b.at("vd_b") == NVM_VD_OK && b.at("seq") == 10) << b.text();
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 9)}, {rb2, value(rb2, 9)}}), "four saves");
    Files g = fx().files({{"a5.bin", "golden@5"}, {"b6.bin", "golden@6"}});
    go(port(), g, concat(kTwin, concat({"--boot", "--set", set_word(rb, value(rb, 7)), "--until-idle", "--set",
                                        set_word(rb2, value(rb2, 8)), "--until-idle", "--set", set_word(rb, value(rb, 9)),
                                        "--until-idle"}, kDump)));
    const Result h = boot_dumped(port(), g);
    EXPECT_TRUE(h.at("seq") == 9) << "the third save does not boot back: " << h.text();
    expect_state(g, "st", with(fx().payloads("golden"), {{rb, value(rb, 9)}, {rb2, value(rb2, 8)}}), "whole, whole, frame");
}

// A frame after a retried (whole) save of another record carries that record too.
TEST_P(NvmBoth, r931_frame_after_retry) {
    const unsigned rb = bind_rid();
    const unsigned rb2 = static_cast<unsigned>(fx().num("bind_rid2"));
    Files f = twin();
    const Result r = go(port(), f,
                        concat(kTwin, concat({"--boot", "--fault", "program-drop:1", "--set", set_word(rb, value(rb, 7)),
                                              "--run-ms", "4000", "--until-idle", "--set", set_word(rb2, value(rb2, 8)),
                                              "--until-idle"}, kDump)), {"ls_refused"});
    EXPECT_TRUE(r.at("ok") == 2 && r.at("failed") == 1) << r.text();
    const Result b = boot_dumped(port(), f);
    EXPECT_TRUE(b.at("seq") == 8) << "the save after the retry does not boot back: " << b.text();
    expect_state(f, "st", with(fx().payloads("golden"), {{rb, value(rb, 7)}, {rb2, value(rb2, 8)}}), "after the retry");
}

}  // namespace
}  // namespace nvm_test
'''
i = s.rindex('}  // namespace\n}  // namespace nvm_test')
p.write_text(s[:i] + T.lstrip('\n'))
