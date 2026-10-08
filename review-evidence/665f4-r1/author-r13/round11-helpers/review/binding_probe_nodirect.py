#!/usr/bin/env python3
"""R532-9 adaptation of R533-8's binding_probe.py (sha256 3047858d...bf72):
the direct-delivery workaround (the direct port call and its positive control)
is removed, and the required composed-delivery assertion must now PASS.
usage: binding_probe_nodirect.py REPO LWSRP WORK

Probe the required ACMP-to-SRP delivery through the composed application.

Only the test translation unit is copied/extended. Production sources are
compiled from the exact checkout. Existing fake environment callbacks observe
the ACMP handoff; direct adapter delivery is a separate positive control.
Exit 0 means the missing-delivery failure was reproduced at both interfaces.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
lwsrp = Path(sys.argv[2]).resolve()
work = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import srp_arms
import fw_gtest
from ctrl_build import CTRL, Tree

probe = work
probe.mkdir(parents=True, exist_ok=True)
extra = r'''
namespace {
TEST_F(AcmpMailbox, R533ComposedAcmpDeliveryReachesSrp) {
    mbx_model_reset(&model);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        mbx_model_set_gm(&model, i, kGm0, 0);
        mbx_model_set_link(&model, i, true);
    }
    const ctrl_app_config cfg = three_way();
    ASSERT_TRUE(ctrl_app_start(&app, &cfg));
    attach_srp();
    settle();
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        fk.clear();
        bind(i);
        ASSERT_TRUE(offer(answer(i), spec::MULTICAST_MAC, i));
        settle();
        bool requested = false;
        for (const auto& call : fk.calls) {
            requested = requested || (call.kind == Call::SRP && call.index == i &&
                         call.flag && call.stream.stream_id == kSid);
        }
        ASSERT_TRUE(requested) << "ACMP accepted the response and requested this stream";
        for (unsigned pass_number = 0; pass_number < 32u; ++pass_number) {
            mbx_model_advance_ms(&model, 10u);
            settle();
        }
        std::printf("R533 interface=%u ACMP_requested=%u SRP_bound=%u\n", i,
                    static_cast<unsigned>(requested),
                    static_cast<unsigned>(srp_adapter.ifs[i].sinks[i].bound));
        EXPECT_TRUE(srp_adapter.ifs[i].sinks[i].bound)
            << "R533 required composed delivery is absent";
    }
    srp_mbx_destroy(&srp_adapter);
}
}
'''
original = root / "sw/firmware/ctrl/test/test_acmp_mbx.cpp"
(probe / original.name).write_text(original.read_text() + extra)
srp_arms.HERE = probe
selected = "AcmpMailbox.R533ComposedAcmpDeliveryReachesSrp"
for count in (1, 2):
    out = probe / f"if{count}"
    result = srp_arms.arm_srp(Tree(CTRL, out, out / "reuse", fw_gtest.Build(jobs=2)),
                              lwsrp, count,
                              test=(original.name, selected))
    print(result.log, flush=True)
    assert result.rc == 0, "required composed delivery must pass without direct delivery"
    assert "R533 required composed delivery is absent" not in result.log
    assert result.log.count("SRP_bound=1") == count, "every tested interface reports SRP_bound=1"
print("PASS: accepted ACMP requests reach the attached SRP adapter through the composition, no direct delivery")
