#!/usr/bin/env python3
"""probe_maap_mac.py TREE OUT - is the composed MAAP's source MAC each
interface's own unicast MAC (the one the filter admits a B.2.1 DEFEND to)?

Appends one reviewer check to TREE's test_acmp_mbx.cpp (the arms compile the
tests from the checkout's test/, so TREE must be a disposable copy made for
this probe) and runs the acmp
and acmpif2 arms twice: on the head's ctrl_app.c (the check must pass) and
with the planted defect `mac[k] = cfg->entity->mac + k` (it must fail at two
interfaces). TREE is an exported copy of the head, never the review clone.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(TREE / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(TREE / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402

CHECK = r'''
namespace {
// Reviewer probe (R530-5): every MAAP frame the composed app sends carries,
// as its source, the own unicast MAC the filter holds for that interface, so
// a DEFEND sent back to it (IEEE 1722-2016 B.2.1) passes the maap row.
TEST_F(AcmpMailbox, R530ProbeMaapSourceIsTheInterfacesOwnMac) {
    mbx_model_reset(&model);
    for (unsigned i = 0; i < MBX_N_IF; ++i) {
        mbx_model_set_gm(&model, i, kGm0, 0);
        mbx_model_set_link(&model, i, true);
    }
    const ctrl_app_config cfg = three_way();
    ASSERT_TRUE(ctrl_app_start(&app, &cfg));
    for (unsigned ms = 0; ms < 1000u; ms += 10u) {
        mbx_model_advance_ms(&model, 10u);
        settle();
    }
    unsigned seen = 0;
    for (std::uint32_t k = 0; k < model.tx_sent; ++k) {
        const mbx_model_tx* f = mbx_model_tx_frame(&model, k);
        if (f == nullptr || f->channel != MBX_CH_MAAP) {
            continue;
        }
        ++seen;
        EXPECT_EQ(wire_be64(f->bytes + 6) >> 16, model.own_mac[f->interface])
            << on_if(f->interface, "R530 MAAP's source is the interface's own unicast MAC");
    }
    EXPECT_GE(seen, MBX_N_IF) << "R530 MAAP sent on every interface";
}
}  // namespace
'''

DEFECT = ("\t\tmac[k] = cfg->entity->mac;\n", "\t\tmac[k] = cfg->entity->mac + k;\n")


def run(name: str, defect: bool, build: fw_gtest.Build, reuse: Path) -> None:
    copy = OUT / name / "ctrl"
    if copy.parent.exists():
        shutil.rmtree(copy.parent)
    shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
    if defect:
        app = copy / "app/ctrl_app.c"
        text = app.read_text(encoding="utf-8")
        assert text.count(DEFECT[0]) == 1
        app.write_text(text.replace(*DEFECT), encoding="utf-8")
    tree = Tree(copy, OUT / name / "build", reuse, build)
    for arm, fn in (("acmp", ctrl_arms.arm_acmp), ("acmpif2", ctrl_arms.arm_acmpif2)):
        o = fn(tree)
        fails = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]
        print(f"[{name}] {arm}: rc {o.rc}, {len(fails)} [FAIL] line(s)", flush=True)
        for ln in fails[:3]:
            print(f"    {ln[:300]}", flush=True)
        verdict = [ln.strip() for ln in o.log.splitlines() if ln.strip().startswith("verdict:")]
        print(f"    {verdict[-1] if verdict else 'no verdict line'}", flush=True)


def main() -> int:
    test = TREE / "sw/firmware/ctrl/test/test_acmp_mbx.cpp"
    text = test.read_text(encoding="utf-8")
    if "R530ProbeMaapSourceIsTheInterfacesOwnMac" not in text:
        test.write_text(text + CHECK, encoding="utf-8")
    build = fw_gtest.Build(jobs=8)
    reuse = OUT / "reuse"
    run("head-with-check", False, build, reuse)
    run("defect-with-check", True, build, reuse)
    return 0


if __name__ == "__main__":
    sys.exit(main())
