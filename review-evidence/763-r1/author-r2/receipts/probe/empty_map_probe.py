#!/usr/bin/env python3
"""Scratch probe for #763 (kept out of the tree).

Runs the firmware AECP saved-state arm at the shipping 1x1 shape with one
extra test appended to a copy of test_aecp.cpp, on the clean sources and on
two planted defects that make an empty map record read as an erased one.
Usage: empty_map_probe.py <repo root> <scratch dir>
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402

EXTRA = r'''
#ifdef AECP_TEST_NVM
namespace {
Bytes map_cmd(unsigned type,const aecp_map &m,size_t from,size_t to){
    Bytes b=target(type,m.index,8+8*(to-from));put(b,4,to-from,2);size_t at=8;
    for(size_t k=from;k<to;++k){auto&r=m.rows[k];put(b,at,r.stream,2);put(b,at+2,r.channel,2);
        put(b,at+4,r.cluster,2);put(b,at+6,r.cluster_channel,2);at+=8;}
    return b;
}
}
TEST_F(Nvm, ProbeEmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle)
{
    for(unsigned empty_type:{14u,15u}){
        SCOPED_TRACE(empty_type);
        a.open=false;ASSERT_TRUE(aecp_restore_defaults(&a));
        nvm_fmodel_blank();nvm_fmodel_power_on();owner.released=false;boot();
        ASSERT_EQ(nvm_store_status()->terminal,NVM_T_BLANK);
        ON_CALL(mock,Changed).WillByDefault([this](aecp_change k,uint16_t t,uint16_t i){aecp_nvm_changed(&owner,k,t,i);});
        aecp_open(&a);
        aecp_map *e=nullptr,*o=nullptr;
        for(auto &m:pools) if(m.index==0) (m.type==empty_type?e:o)=&m;
        ASSERT_TRUE(e&&o);ASSERT_GT(e->count,0u);ASSERT_GT(o->count,1u);
        unsigned other_type=empty_type==14u?15u:14u;
        ask(45,map_cmd(empty_type,*e,0,e->count));
        ask(45,map_cmd(other_type,*o,o->count-1,o->count));
        ASSERT_EQ(e->count,0u);
        unsigned eg=empty_type==14u?NVM_G_MAPI:NVM_G_MAPO, og=empty_type==14u?NVM_G_MAPO:NVM_G_MAPI;
        auto kept=latch(og,0,o->capacity*8);
        while(aecp_nvm_poll(&owner)){}
        ASSERT_TRUE(nvm_store_commit_now());
        for(unsigned n=0;n<10000&&nvm_store_status()->phase!=NVM_P_IDLE;++n){nvm_store_service();nvm_fmodel_advance_us(100);}
        ASSERT_EQ(nvm_store_status()->phase,NVM_P_IDLE);
        auto r=nvm_rec_of(eg,0);ASSERT_TRUE(r.ok);
        const uint8_t *rec=nvm_store_stage()+NVM_KLJ2_HDR+r.off;
        EXPECT_EQ(rec[0],0x17u);EXPECT_EQ(rec[1],0x22u)<<"the empty set is FRAMED, not erased";
        EXPECT_TRUE(nvm_all_erased(rec+NVM_REC_HDR,r.plen))<<"every entry UNUSED";
        a.open=false;ASSERT_TRUE(aecp_restore_defaults(&a));
        ASSERT_GT(e->count,0u)<<"defaults are back before the power cycle";
        owner.released=false;nvm_fmodel_power_on();boot();
        ASSERT_EQ(nvm_store_status()->terminal,NVM_T_COMPLETE);
        EXPECT_EQ(e->count,0u)<<"the empty list survives the power cycle";
        EXPECT_EQ(latch(og,0,kept.size()),kept)<<"the non-default list survives the power cycle";
        EXPECT_EQ(o->count,o->default_count-1u);
    }
}
#endif
'''

PLANTS = {
    "none": None,
    "apply-empty-as-erased": ("ctrl/aecp/aecp_nvm.c",
        "\t\tunsigned status = aecp_map_restore(n->core, m, n->scratch, count);",
        "\t\tif (count == 0) return NVM_APPLIED;\n\t\tunsigned status = aecp_map_restore(n->core, m, n->scratch, count);"),
    "store-payload-as-erased": ("ctrl_nvm/nvm_store.c",
        "\tif (nvm_all_erased(rec, NVM_REC_HDR)) {\n\t\tnvm.st.blank++;",
        "\tif (nvm_all_erased(rec, NVM_REC_HDR) || nvm_all_erased(rec + NVM_REC_HDR, r.plen)) {\n\t\tnvm.st.blank++;"),
}


def main() -> int:
    shipping = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
    results = {}
    for name, plant in PLANTS.items():
        work = SCRATCH / name
        if work.exists():
            shutil.rmtree(work)
        src = work / "ctrl"
        shutil.copytree(ROOT / "sw/firmware/ctrl", src)
        nvm = work / "ctrl_nvm"
        shutil.copytree(ROOT / "sw/firmware/ctrl_nvm", nvm, ignore=shutil.ignore_patterns("test"))
        here = src / "test"
        (here / "test_aecp.cpp").write_text((here / "test_aecp.cpp").read_text() + EXTRA)
        if plant:
            rel, old, new = plant
            path = work / rel
            text = path.read_text()
            assert text.count(old) == 1, (name, rel)
            path.write_text(text.replace(old, new))
        aecp_arms.HERE = here
        original = aecp_arms.saved_state.__wrapped__ if hasattr(aecp_arms.saved_state, "__wrapped__") else aecp_arms.saved_state

        def saved_state(tree, config, out, _orig=original, _nvm=nvm):
            inc, sources, host = _orig(tree, config, out)
            sources = [(_nvm / p.name) if p.parent.name == "ctrl_nvm" else p for p in sources]
            return inc, sources, host
        saved_state.__wrapped__ = original
        aecp_arms.saved_state = saved_state
        tree = ctrl_build.Tree(src, work / "out", work / "reuse", fw_gtest.Build(jobs=4))
        outcome = aecp_arms.core_arm(tree, shipping, 1, mode="nvm", selected="Nvm.*")
        (SCRATCH / f"{name}.log").write_text(outcome.log)
        probe_failed = "[  FAILED  ] Nvm.ProbeEmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle" in outcome.log
        others_failed = [l for l in outcome.log.splitlines()
                         if l.startswith("[  FAILED  ] Nvm.") and "Probe" not in l and "listed below" not in l]
        results[name] = (outcome.rc, probe_failed, others_failed)
        print(f"{name}: rc={outcome.rc} probe_failed={probe_failed} other_failed={others_failed}")
    ok = (results["none"][0] == 0 and not results["none"][1]
          and all(results[k][1] for k in PLANTS if k != "none"))
    print("PROBE VERDICT:", "clean passes, every plant reddens the probe" if ok else "UNEXPECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
