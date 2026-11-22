#!/usr/bin/env python3
"""Count every payload transfer for a 65-byte off-format PDU, then verify recovery."""
import os,pathlib,shlex,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;R=pathlib.Path(sys.argv[1]).resolve();RX=R/"tb/verilator/avtp_rxmon";S=P/"scratch"
V=os.environ.get("REVIEW_VERILATOR","$VALIDATION_TOOLS/pinned-verilator-5.050/verilator")
t=(RX/"sim_fanout.cpp").read_text()
a=t.index("        two_inputs_on_one_stream();");b=t.index("        std::printf",a)
t=t[:a]+"        discard_probe();\n"+t[b:]
t=t.replace("    long checks = 0;","    long transfers = 0;\n    long checks = 0;")
t=t.replace("        if (dut->dp_tvalid_o) {","        if (dut->dp_tvalid_o) {\n            transfers++;")
probe=r"""
    void discard_probe() {
        bind(0,kTalkerA,true);bind(1,kTalkerA,true);cyc(200);
        for (bool vlan : {false,true}) {
            const Snap before=snap();
            const long t0=transfers;
            feed(aaf_as(0,kPcm32x8,payload(65),vlan),0);
            flush_iv();
            ck("off-size 65-octet PDU transfers no payload beat",0,transfers-t0,0);
            for(int s:{0,1}) {
                ck("off-size PDU has no accept",s,accepts[s]-before.acc[s],0);
                ck("off-size PDU counted UNSUPPORTED_FORMAT",s,lctx_rd(s,W_UF)-before.uf[s],1);
                ck("off-size PDU leaves no partial payload",s,cur[s].size(),0);
            }
            const Snap next=snap();
            std::vector<Pdu> sent{payload(192)};
            feed(aaf_as(0,kPcm32x8,sent[0],vlan),0);flush_iv();
            for(int s:{0,1})received("next valid PDU",s,next,sent);
        }
    }
"""
t=t.replace("    void two_inputs_on_one_stream() {",probe+"\n    void two_inputs_on_one_stream() {")
f=S/"stack_discard.cpp";f.write_text(t);out=S/"obj_stack_discard"
cmd=shlex.split(subprocess.check_output(["make","-n","fanout-build","VERILATOR="+V,"FO_MDIR="+str(out)],cwd=RX,text=True))
for i in range(len(cmd)-1):
 if cmd[i]=="-j":cmd[i+1]="4"
cmd=[str(f) if x=="sim_fanout.cpp" else x for x in cmd]
with (S/"stack-discard-build.log").open("w") as log:q=subprocess.run(cmd,cwd=RX,stdout=log,stderr=log)
assert q.returncode==0
with (P/"stack-discard.log").open("w") as log:q=subprocess.run([str(out/"Vavtp_rxmon_fanout")],cwd=RX,stdout=log,stderr=log)
(P/"stack-discard.rc").write_text(str(q.returncode)+"\n");print("stack-discard",q.returncode)
assert q.returncode==0
