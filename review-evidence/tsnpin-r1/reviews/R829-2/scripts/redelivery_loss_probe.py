"""Reviewer probe 3: a disposable test, three commands behind the full owed
set, each must be answered once and in arrival order. Run at the head's code
(must pass) and with the redelivery's stop-on-decline removed (shows the
loss). Usage: python3 -I redelivery_loss_probe.py <checkout> <workdir> <jobs>"""
import sys
from pathlib import Path
checkout, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
ANCHOR = "TEST_F(AcmpMailbox, K2ABindDeclinedAtTheFullSetWaitsForTwoSlotsAndLosesNoProbe) {"
PROBE = r'''TEST_F(AcmpMailbox, ZProbeThreeCommandsBehindTheFullOwedSetEachAnsweredOnce) {
    fill_owed();
    const unsigned i = acfg.sink_interface[1];
    for (std::uint16_t s = 0x7801; s <= 0x7803; ++s) {
        ASSERT_TRUE(offer(command(spec::MSG_GET_RX_STATE_COMMAND, 1, kCtl1, s), spec::MULTICAST_MAC, i));
    }
    for (unsigned p = 0; p < 20u; ++p) {
        static_cast<void>(pass());
    }
    mbx_model_tx_pause(&model, false);
    std::uint32_t base = model.tx_sent;
    std::vector<std::uint16_t> got;
    for (unsigned p = 1; p <= ACMP_MBX_KEPT_PASSES + 8u; ++p) {
        static_cast<void>(pass());
        for (std::uint32_t j = base; j < model.tx_sent; ++j) {
            const Pdu w = wire(j);
            if (w.seq >= 0x7801u && w.seq <= 0x7803u) {
                got.push_back(w.seq);
            }
        }
        base = model.tx_sent;
    }
    const std::vector<std::uint16_t> want{0x7801, 0x7802, 0x7803};
    EXPECT_EQ(got, want) << "ZPROBE each of three commands behind the full owed set answered once, in arrival order";
}

'''
C = "acmp/acmp_mbx.c"
T = "test/test_acmp_mbx.cpp"
DEFECT = ("k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k)", "k < ACMP_MBX_REDELIVER_RECORDS; ++k)")
orig_plant = ctrl_mutants.plant


def plant(m, root):
    ctrl, stack = orig_plant(m, root)
    if m.name.endswith("+defect"):
        f = ctrl / C
        text = f.read_text(encoding="utf-8")
        assert text.count(DEFECT[0]) == 1
        f.write_text(text.replace(*DEFECT), encoding="utf-8")
    return ctrl, stack


ctrl_mutants.plant = plant
import ctrl_arms  # noqa: E402
_arm = ctrl_arms.arm_acmp


def arm_acmp(tree):
    o = _arm(tree)
    (work / f"arm-{len(list(work.glob('arm-*.log')))}.log").write_text(o.log, encoding="utf-8")
    return o


ctrl_arms.arm_acmp = arm_acmp
import ctrl_build  # noqa: E402
_ts = ctrl_build.test_source


def test_source(n):
    # the arm compiles tests from the checkout; this probe's test lives in the planted copy
    return work / "work" / "ctrl" / "test" / n if n == "test_acmp_mbx.cpp" else _ts(n)


ctrl_build.test_source = test_source
ctrl_mutants.unnamed_tests = lambda: []
ctrl_mutants.MUTANTS = (
    Mutant("probe-test-at-head-code", T, ANCHOR, PROBE + ANCHOR, "acmp", "", ""),
    Mutant("probe-test+defect", T, ANCHOR, PROBE + ANCHOR, "acmp",
           "AcmpMailbox.ZProbeThreeCommandsBehindTheFullOwedSetEachAnsweredOnce", "ZPROBE"),
)
# head code: "caught" must be False (the arm passes, rc 0); defect: caught on ZPROBE
orig_caught = ctrl_mutants.caught
ctrl_mutants.caught = lambda test, needle, o: (o.rc == 0) if not test else orig_caught(test, needle, o)
work.mkdir(parents=True, exist_ok=True)
ctrl_mutants.campaign(work, work / "reuse", jobs)
print("reading: [ok] probe-test-at-head-code means the arm PASSED with the probe test; "
      "[ok] probe-test+defect means the probe test FAILED on the defect")
