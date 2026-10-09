#!/usr/bin/env python3
"""Compare emitted SRP Listener declarations using unchanged pinned sources."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


SOFTWARE = r'''
#include "srp_fixture.hpp"
FW_TALLY_LABEL("SRP emitted-frame preflight");
namespace {
TEST_F(Srp, TwoConsecutiveListenerDeclarations) {
    settle(); advance(1250);
    for (unsigned k=0;k<2;++k) {
        msrp_stream_id id{}; uint8_t mac[6];
        wire_put_be(id.bytes,0x1122334455660001ull+k,8);
        wire_put_be(mac,0x91e0f0112233ull+k,6);
        ASSERT_TRUE(srp_mbx_bind(&adapter,0,k,&id,mac,2));
    }
    const unsigned first=model.tx_sent;
    for (unsigned k=0;k<1;++k) {
        std::vector<uint8_t> v(25,0);
        wire_put_be(v.data(),0x1122334455660001ull+k,8);
        wire_put_be(v.data()+8,0x91e0f0112233ull+k,6);
        wire_put_be(v.data()+14,2,2); wire_put_be(v.data()+16,256,2);
        wire_put_be(v.data()+18,1,2); v[20]=0x70;
        wire_put_be(v.data()+21,0x12345,4);
        auto incoming=frame(1,v,1);
        incoming[20]=2; incoming[46]=42; // two consecutive JoinIn values
        std::printf("INPUT split ");
        for(unsigned b=14;b<incoming.size();++b) std::printf("%02x",incoming[b]);
        std::puts("");
        offer(incoming);
    }
    // offer() drains this response; stop before the next JoinTime repeat.
    unsigned emitted=0;
    for(unsigned k=first;k<model.tx_sent;++k) {
        const auto *f=mbx_model_tx_frame(&model,k);
        ASSERT_NE(f,nullptr);
        if(wire_be16(f->bytes+12)==0x22ea && f->len>15 && f->bytes[15]==3) {
            ++emitted;
            std::printf("WIRE split ");
            for(unsigned b=0;b<f->len;++b) std::printf("%02x",f->bytes[b]);
            std::puts("");
        }
    }
    ASSERT_EQ(emitted,1u);
    capture(); unsigned ready=0;
    for(const auto &d:declarations) if(d.ethertype==0x22ea && d.type==3 &&
        d.event==0 && d.subtype==2 && d.time_ms>=1250) ++ready;
    EXPECT_EQ(ready,2u);
}
}
'''

FABRIC = r'''
int main(int argc, char **argv) {
    Verilated::commandArgs(argc,argv);
    const milan::tb::Model<Vsrp_top_wrap> model;
    H h(model.get()); h.reset(); model->link_up_i=1; h.idle(10);
    h.run_ms(1250);
    for(unsigned k=0;k<2;++k) {
        const auto result=h.op(OP_DECL_LS,k,0x1122334455660001ull+k,
                               0x91e0f0112233ull+k,2,0,0,DECL_READY);
        if(!result.got || result.status!=ST_OK) return 2;
    }
    h.sync();
    for(unsigned k=0;k<1;++k) {
        const Msg adv{1,25,false,{Vec{false,2,
            fv_talker(0x1122334455660001ull+k,0x91e0f0112233ull+k,
                      2,256,1,3,1,0x12345),{EV_JOININ,EV_JOININ},{}}}};
        const auto incoming=mrpdu_body(true,{adv});
        std::printf("INPUT fabric ");
        for(auto byte:incoming) std::printf("%02x",byte);
        std::puts("");
        h.feed(incoming,true);
    }
    auto f=h.wait_frame(true,800,[](const std::vector<uint8_t> &fr) {
        return frame_has(fr,true,3,0x1122334455660001ull,EV_NEW);
    });
    const auto expected=mrpdu_frame(true,{Msg{3,8,true,{Vec{false,2,
        fv_sid(0x1122334455660001ull),{EV_NEW,EV_NEW},{DECL_READY,DECL_READY}}}}});
    if(f!=expected) { dump("unexpected",f); dump("expected",expected); return 1; }
    std::printf("WIRE fabric ");
    for(auto byte:f) std::printf("%02x",byte);
    std::puts("");
    std::puts("3 checks: 3 PASS, 0 FAIL");
    return 0;
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--compiler", type=Path, required=True)
    args = parser.parse_args()
    root, work = args.root.resolve(), args.work.resolve()
    assert root not in work.parents and root != work
    work.mkdir(parents=True, exist_ok=True)
    os.environ.update(TMPDIR=str(work), PYTHONDONTWRITEBYTECODE="1", VERILATOR_JOBS="2")
    sys.dont_write_bytecode = True
    sys.path.insert(0,str(root / "sw/firmware/ctrl/test"))
    import ctrl_build as build
    import ctrl_reuse
    import srp_arms
    import fw_gtest

    def git(*argv, cwd=root):
        if cwd != root:
            top = subprocess.check_output(["git","-C",str(cwd),"rev-parse","--show-toplevel"],text=True).strip()
            assert Path(top).resolve() == cwd.resolve()
        return subprocess.check_output(["git",*argv],cwd=cwd,text=True,
                                       env={**os.environ,"GIT_NO_REPLACE_OBJECTS":"1"}).strip()

    head = git("rev-parse","HEAD")
    pins = {}
    for name in ("protocol-processor","third_party/lwSRP"):
        dep = root / name
        pin = git("rev-parse",f"HEAD:{name}")
        assert git("rev-parse","HEAD",cwd=dep) == pin
        pins[name] = pin
        # Verify all source bytes, independently of any index flags.
        for row in git("ls-tree","-r",pin,cwd=dep).splitlines():
            meta, path = row.split("\t",1)
            mode, kind, blob = meta.split()
            if kind == "blob" and (path.startswith("hdl/") or path.startswith("src/") or path.startswith("tb/")):
                p = dep / path
                assert p.is_file() and not p.is_symlink(), path
                assert git("hash-object","--no-filters",path,cwd=dep) == blob, path

    fixture=(build.HERE / "srp_fixture.hpp").read_text()
    old="config.mac[i]=0x020304050600ull+i;"
    assert fixture.count(old)==1
    (work / "srp_fixture.hpp").write_text(fixture.replace(old,"config.mac[i]=0x0a0b0c0d0e0full+i;"))
    (work / "srp_probe.cpp").write_text(SOFTWARE)
    dep=root / "protocol-processor"
    source=(dep / "tb/srp_top/sim_main.cpp").read_text()
    marker="namespace {\n\n//! The whole end-to-end bench"
    assert source.count(marker)==1
    prefix=source.split(marker)[0]
    (work / "fabric_probe.cpp").write_text(prefix+FABRIC)
    records=[]

    def command(label, argv):
        result=subprocess.run(argv,cwd=work,capture_output=True,text=True,timeout=540,check=False)
        log=result.stdout+result.stderr
        (work / f"{label}.log").write_text(log)
        records.append(dict(label=label,rc=result.returncode,bytes=len(log.encode()),
                            sha256=hashlib.sha256(log.encode()).hexdigest()))
        assert result.returncode==0,(label,result.returncode,log[-4000:])
        return log

    def software():
        tree=build.Tree(build.CTRL,work / "host",work / "reuse",fw_gtest.Build(jobs=4))
        result=srp_arms.arm_srp(tree,root / "third_party/lwSRP",1,test=str(work / "srp_probe.cpp"))
        (work / "split.log").write_text(result.log)
        records.append(dict(label="split",rc=result.rc,bytes=len(result.log.encode()),
                            sha256=hashlib.sha256(result.log.encode()).hexdigest()))
        assert result.rc==0,result.log
        return result.log

    def fabric():
        paths=["common/pp_pkg.sv","srp/srp_pkg.sv","common/KL_pp_prng.sv",
               "common/KL_pp_timer_service.sv","packet_engine/KL_pp_tx_slots.sv"]
        paths += [f"srp/{name}.sv" for name in ("KL_srp_decoder","KL_srp_domain","KL_srp_vlan",
                  "KL_srp_talker_fsm","KL_srp_listener_fsm","KL_srp_admission","KL_srp_encoder","KL_srp_top")]
        command("fabric-build",[str(args.compiler.resolve()),"--cc","--exe","--build","-j","8","--savable",
                "--top-module","srp_top_wrap","-Wall","-Wno-fatal","-Wno-DECLFILENAME","-Wno-UNUSEDSIGNAL",
                "-Wno-WIDTHEXPAND","-Wno-WIDTHTRUNC","-Wno-UNUSEDPARAM","-CFLAGS",
                f"-std=c++17 -O2 -I{dep / 'tb/srp_top'} -Wall -Wextra","--Mdir",str(work / "obj"),
                *[str(dep / "hdl" / path) for path in paths],str(dep / "tb/srp_top/srp_top_wrap.sv"),
                str(work / "fabric_probe.cpp"),"-o","srp_probe"])
        return command("fabric",[str(work / "obj/srp_probe")])

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(software),pool.submit(fabric)]
        logs=[f.result() for f in futures]
    frames={}
    inputs={}
    for log in logs:
        for line in log.splitlines():
            if line.startswith(("WIRE ","INPUT ")):
                kind,placement,hexadecimal=line.split()
                target=frames if kind=="WIRE" else inputs
                assert placement not in target
                target[placement]=bytes.fromhex(hexadecimal)
                print(line,flush=True)
    assert set(frames)=={"fabric","split"}
    assert set(inputs)=={"fabric","split"} and inputs["fabric"]==inputs["split"]
    a,b=frames["fabric"],frames["split"]
    result=dict(head=head,pins=pins,input_mrpdu=inputs["fabric"].hex(),frames={k:v.hex() for k,v in frames.items()},
                lengths={k:len(v) for k,v in frames.items()},equal=a==b,
                differences=[dict(offset=i,fabric=x,split=y) for i,(x,y) in enumerate(zip(a,b)) if x!=y],
                commands=records)
    (work / "comparison.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2),flush=True)
    print("Equal raw SRP frames:",a==b,flush=True)


if __name__=="__main__":
    main()
