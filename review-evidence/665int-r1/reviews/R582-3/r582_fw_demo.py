#!/usr/bin/env python3
"""r582_fw_demo.py - R582-3: the two escaping plants, every suite, and a demonstration test for each.

Usage: r582_fw_demo.py <disposable-clone> <lwsrp> <scratch-root>

The arms compile their tests from the checkout's own test directory, so the
demonstration tests are appended to a DISPOSABLE CLONE of the head (never the
review checkout); the plants go into the gate's copy of its ctrl tree.

E1 r582-adapter-sid-valid-always (acmp/acmp_mbx.c): a bound or started move
   with no stream asserts SID_VALID, so SID_LO/SID_HI's stale stream_id reaches
   the datapath for a sink that is not settled.
E2 r582-declarations-cleared-at-adoption (srp/srp_mbx.c): TALKER_DECL cleared
   after a Domain adoption while every source stays declared (adds one write).
E2b r582-declarations-zero-at-adoption (srp/srp_mbx.c): the same, count-neutral:
   declare_sources publishes 0 while a Domain adoption is owed.

Part A: each plant against every ctrl arm that links the file and every SRP
suite at one and two interfaces (the gate's own builders); every [FAIL] printed.
Part B: a demonstration test appended to a COPY of the suite, run unplanted
(must pass) and planted (must fail). Nothing in <checkout> is written.
"""
import shutil
import sys
from pathlib import Path

checkout, lwsrp, root = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

build = fw_gtest.Build(jobs=4)
reuse = root / "reuse"
cut_reuse(reuse)
SUITES = ("srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp", "srp_latency.cpp", "srp_walk.cpp")
CTRL_ARMS = {"acmp": ctrl_arms.arm_acmp, "acmpif2": ctrl_arms.arm_acmpif2, "acmpnvm": ctrl_arms.arm_acmpnvm,
             "acmpwalk": ctrl_arms.arm_acmpwalk, "walk": ctrl_arms.arm_walk, "entity": ctrl_arms.arm_entity}

E1 = ("acmp/acmp_mbx.c", "(void)mbx_pub_sink_binding(interface, sink, bound, started, stream_id != 0u);",
      "(void)mbx_pub_sink_binding(interface, sink, bound, started, true);")
E2B = ("srp/srp_mbx.c", "    (void)mbx_pub_talker_decl(i->index,declared);",
       "    (void)mbx_pub_talker_decl(i->index,i->domain_owed ? 0u : declared);")
E2 = ("srp/srp_mbx.c", "    (void)declare_sources(i);\n    i->domain_owed = false;",
      "    (void)declare_sources(i);\n    withdraw_declared(i->index);\n    i->domain_owed = false;")

DEMO_E1 = """
// R582-3 demonstration (disposable): a sink that settled, was unbound and is
// bound again has no stream; the datapath must not take the old stream_id.
TEST_F(AcmpMailbox, R582DemoNoStaleStreamAfterRebind) {
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        SetUp();
        const unsigned k = i;
        bind(k);
        ASSERT_TRUE(offer(answer(k), spec::MULTICAST_MAC, i));
        settle();
        ASSERT_EQ(pub_view(i).sid[k], kSid);
        ASSERT_TRUE(offer(command(spec::MSG_UNBIND_RX_COMMAND, k), spec::MULTICAST_MAC, i));
        settle();
        ASSERT_TRUE(!pub_view(i).bound[k] && pub_view(i).sid[k] == 0u);
        bind(k);
        EXPECT_TRUE(pub_view(i).bound[k] && pub_view(i).sid[k] == 0u)
            << on_if(i, "R582 demo: a re-bound sink with no settled stream carries no stream_id");
    }
}
"""

DEMO_E2 = """
// R582-3 demonstration (disposable): a Domain adoption re-declares every
// source; TALKER_DECL must stay set for every MRPDU carrying a Talker after it.
TEST_F(Srp, R582DemoTalkerDeclHeldAcrossAdoption) {
    const uint32_t all=(1u<<CTRL_SRP_SOURCES)-1u;
    settle();
    commits_seen.clear(); traced_model=&model; mbx_host_trace(commit_trace,nullptr);
    offer(frame(4,{6,4,0,3},0)); advance(200);
    mbx_host_trace(nullptr,nullptr);
    capture();
    unsigned talkers=0;
    for (const auto &d:declarations) {
        if (d.interface!=0 || d.ethertype!=0x22ea || commit_of(d.frame)==nullptr) continue;
        if (d.type!=1 && d.type!=2) continue;
        ++talkers;
        EXPECT_EQ(commit_of(d.frame)->pub[0].talker_decl,all)
            << "R582 demo: every Talker MRPDU after a Domain adoption left with TALKER_DECL set";
    }
    EXPECT_GT(talkers,0u) << "R582 demo: the adoption re-declared the Talkers";
    EXPECT_EQ(pub_of(model,0).talker_decl,all) << "R582 demo: TALKER_DECL holds every source after the adoption";
}
}  // namespace R582_DEMO_TAIL
"""


def install(demo):
    suite, text = demo
    t = checkout / "sw/firmware/ctrl/test" / suite
    s = ORIG.setdefault(t, t.read_text())
    if "R582_DEMO_TAIL" in text:     # srp_mbx.cpp keeps its tests in an anonymous namespace
        s = s.rstrip()
        assert s.endswith("}"), "srp_mbx.cpp does not end in its namespace"
        s = s[:-1] + text.replace("}  // namespace R582_DEMO_TAIL\n", "}\n")
    else:
        s += text
    t.write_text(s)


ORIG = {}


def copy(plant, demo=None):
    work = root / "work" / "ctrl"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(CTRL, work, ignore=shutil.ignore_patterns("__pycache__"))
    if plant:
        p, old, new = plant
        t = work / p
        s = t.read_text()
        assert s.count(old) == 1, (p, s.count(old))
        t.write_text(s.replace(old, new))
    return Tree(work, root / "work" / "build", reuse, build)


def show(label, outs):
    f = [ln.strip() for o in outs for ln in o.log.splitlines() if "[FAIL]" in ln]
    bad = [o for o in outs if o.rc not in (0, 1)]
    print(f"{label}: rc {','.join(f'{o.arm}={o.rc}' for o in outs)}; {len(f)} failing check(s)"
          + (f"; NOT RUN {[o.arm for o in bad]}" if bad else ""), flush=True)
    for x in f[:4]:
        print(f"    {x[:220]}", flush=True)
    for o in bad:
        print("    " + o.log[-600:].replace("\n", "\n    "), flush=True)


print("== Part A: the escaping plants against every suite", flush=True)
for name, plant, arms in (("E2b r582-declarations-zero-at-adoption", E2B, {}),):
    tree = copy(plant)
    outs = [fn(tree) for fn in arms.values()]
    for i in (1, 2):
        for suite in SUITES:
            try:
                outs.append(srp_arms.arm_srp(tree, lwsrp, i, test=suite))
            except Refusal as exc:
                print(f"    refused {suite} if{i}: {exc}", flush=True)
    show(f"[{'ESCAPED' if not any(o.rc for o in outs) else 'CAUGHT'}] {name}", outs)

print("== Part B: demonstration tests", flush=True)
for name, plant, demo, runner in (
        ("E1", E1, ("test_acmp_mbx.cpp", DEMO_E1), lambda t: [ctrl_arms.arm_acmp(t), ctrl_arms.arm_acmpif2(t)]),
        ("E2b", E2B, ("srp_mbx.cpp", DEMO_E2), lambda t: [srp_arms.arm_srp(t, lwsrp, 1), srp_arms.arm_srp(t, lwsrp, 2)])):
    install(demo)
    show(f"[demo {name} unplanted, must pass]", runner(copy(None)))
    show(f"[demo {name} planted, must fail on the demo]", runner(copy(plant)))
for t, text in ORIG.items():
    t.write_text(text)
shutil.rmtree(root / "work", ignore_errors=True)
print("demo done", flush=True)
