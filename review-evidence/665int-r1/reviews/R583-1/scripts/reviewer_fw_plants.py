#!/usr/bin/env python3
"""Reviewer firmware plants for the publication writers (R583-1).

Usage: python3 reviewer_fw_plants.py <repo-or-copy-root> <scratch-dir> <lwsrp> <group> [jobs]

group "ctrl": ACMP and driver plants, graded by the campaign's own arms
              (ctrl_mutants.plant / ctrl_arms / ctrl_mutants.caught).
group "srp":  SRP adapter and host-model plants, graded by srp_arms.arm_srp at
              two interfaces with srp_mutants.caught.
group "srp-nohold": run against a COPY whose srp_mbx.cpp lost the event hold
              (the base form of the test): the original cancelled-link plant
              is expected to ESCAPE there, which is what the hold exists for.

Each line prints [ok] (caught as expected), [ESCAPED] (expected caught, was
not) or [ESCAPED-AS-EXPECTED]. Exit 0 when every arm met its expectation.
The tree under <root> is only read; every planted copy is under <scratch-dir>.
"""
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
lwsrp = Path(sys.argv[3]).resolve()
group = sys.argv[4]
jobs = int(sys.argv[5]) if len(sys.argv) > 5 else 4
sys.path.insert(0, str(root / "sw" / "firmware" / "ctrl" / "test"))
sys.path.insert(0, str(root / "sw" / "firmware" / "gtest"))

import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, Refusal  # noqa: E402

scratch.mkdir(parents=True, exist_ok=True)
bad = 0


def report(name, ok, expect_escape, detail):
    global bad
    if expect_escape:
        tag = "ESCAPED-AS-EXPECTED" if not ok else "CAUGHT-UNEXPECTEDLY"
        bad += ok
    else:
        tag = "ok" if ok else "ESCAPED"
        bad += not ok
    print(f"[{tag}] {name}: {detail}", flush=True)


if group == "ctrl":
    import ctrl_arms
    import ctrl_mutants
    from ctrl_mutant import Mutant
    from ctrl_reuse import cut_reuse
    reuse = scratch / "reuse"
    cut_reuse(reuse)
    A31 = "AcmpCore.A31TheBindingIsPublishedBeforeTheResponseThatPromisesIt"
    PLANTS = (
        Mutant("rv-acmp-unbind-never-published", "acmp/acmp.c",
               "if (s->bound != s->published_bound || stream != s->published_stream) {",
               "if ((s->bound && !s->published_bound) || stream != s->published_stream) {",
               "acmp", A31, "A31 an UNBIND_RX publishes the sink unbound"),
        Mutant("rv-acmp-no-publish-before-send", "acmp/acmp.c",
               "\tpublish(a);\n\tif (a->owed_count == 0u && p_send(a, interface, frame)) {",
               "\tif (a->owed_count == 0u && p_send(a, interface, frame)) {",
               "acmp", A31, "A31 the binding is published before the BIND_RX response"),
        Mutant("rv-driver-sid-valid-never-set", "mbx/mbx.c",
               "\t\tmbx_hal_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING),\n"
               "\t\t\t\tbinding | mbx_place(1u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH));\n",
               "", "unit", "DriverUnit.D14PublicationBlock", "D14 four writes"),
        Mutant("rv-driver-binding-cleared-after-sid", "mbx/mbx.c",
               "\tmbx_hal_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING), binding);\n"
               "\tif (stream_id != 0u) {\n",
               "\tif (stream_id != 0u) {\n",
               "unit", "DriverUnit.D14PublicationBlock", "D14"),
        Mutant("rv-maap-gate-on-interface-0", "maap/maap_mbx.c",
               "(void)mbx_pub_da_gate(interface, valid", "(void)mbx_pub_da_gate(0u, valid",
               "maap_if2", "MaapHost.DaGateIsPublishedBeforeEachAllocationIsReported", "DA gate"),
    )
    build = fw_gtest.Build(jobs=jobs)
    for m in PLANTS:
        try:
            tree = Tree(ctrl_mutants.plant(m, scratch), scratch / "work" / "build", reuse, build)
            arm = getattr(ctrl_arms, f"arm_{m.arm}")
            outcome = arm(tree)
            ok = ctrl_mutants.caught(m.test, m.needle, outcome)
            fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
            (scratch / f"{m.name}.log").write_text(outcome.log)
            report(m.name, ok, False, f"{m.arm} rc={outcome.rc}, {len(fails)} [FAIL]; first: "
                   f"{fails[0][:180] if fails else '-'}")
        except Refusal as exc:
            report(m.name, False, False, f"refused: {exc}")
else:
    import srp_mutants
    from srp_arms import arm_srp
    D = srp_mutants.Defect
    LIC = "PubLicenceIsSetAndClearedBeforeEachChangeIsReported"
    DOM = "PubDomainPrecedesEveryDeclarationThatCarriesIt"
    CLR = "CancelledLinkRecordRecoversFromLevelAndFencesOldReceive"
    if group == "srp":
        PLANTS = (
            (D("rv-srp-stop-owed-licence-after-report", LIC,
               "                ++m->stops;\n                publish_licence(i);\n"
               "                m->config.licence(m->config.ctx,n,s,false);",
               "                ++m->stops;\n                m->config.licence(m->config.ctx,n,s,false);\n"
               "                publish_licence(i);", "PUB"), False),
            (D("rv-srp-reset-publishes-stale-licence", LIC,
               "    bool revoked[CTRL_SRP_SOURCES];\n    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n"
               "        revoked[k] = i->active[k];\n        i->active[k] = false;\n"
               "        i->stop_owed[k] = false;\n    }\n    publish_licence(i);\n",
               "    bool revoked[CTRL_SRP_SOURCES];\n    publish_licence(i);\n"
               "    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n"
               "        revoked[k] = i->active[k];\n        i->active[k] = false;\n"
               "        i->stop_owed[k] = false;\n    }\n",
               "PUB a link loss clears LICENCE before the revocation is reported"), False),
            (D("rv-srp-adoption-published-not-adopted", DOM,
               "(void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);",
               "(void)mbx_pub_domain(i->index,false,i->domain.priority,i->domain.vid);",
               "PUB an MRPDU carrying the adopted Domain or its VID left after SR_DOMAIN published it"), False),
            # the author's two plants on the held record, re-run independently
            (D("author-cancelled-link-never-recovers", CLR, "if (i->link != link)", "if (i->link && !link)",
               "adapter.ifs[i].link"), False),
            (D("author-cancelled-link-record-posted", CLR,
               "if (m->evt_paused || free_words < MBX_EV_WORDS", "if (free_words < MBX_EV_WORDS",
               "the DOWN record stayed held", path="host/mbx_model.c"), False),
        )
    else:  # srp-nohold: the root is a copy whose test lost the hold
        PLANTS = (
            (D("nohold-cancelled-link-never-recovers", CLR, "if (i->link != link)", "if (i->link && !link)",
               "adapter.ifs[i].link"), True),
        )
    build = fw_gtest.Build(jobs=jobs)
    for d, expect_escape in PLANTS:
        out = scratch / "work"
        src = out / "ctrl"
        if src.exists():
            shutil.rmtree(src)
        shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        target = src / d.path
        text = target.read_text()
        if text.count(d.old) != 1:
            report(d.name, False, False, f"fixture occurs {text.count(d.old)} times")
            continue
        target.write_text(text.replace(d.old, d.new))
        selected = "Srp." + d.test
        result = arm_srp(Tree(src, out / "build", out / "reuse", build), lwsrp, 2, test=(d.suite, selected))
        ok = srp_mutants.caught(selected, d.needle, result)
        fails = [ln.strip() for ln in result.log.splitlines() if "[FAIL]" in ln]
        (scratch / f"{d.name}.log").write_text(result.log)
        report(d.name, ok, expect_escape, f"rc={result.rc}, {len(fails)} [FAIL]; first: "
               f"{fails[0][:180] if fails else '-'}")
print(f"reviewer firmware plants ({group}): {'all as expected' if not bad else f'{bad} not as expected'}")
sys.exit(1 if bad else 0)
