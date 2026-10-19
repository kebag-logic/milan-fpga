#!/usr/bin/env python3
import concurrent.futures,importlib.util,json,os,pathlib,subprocess,sys
sys.dont_write_bytecode=True
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
scratch=packet/"scratch/probes";scratch.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env.update(VERILATOR=str(packet/"scripts/sim_limited.py"),MAKEFLAGS="-j16",TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE="1")
def execute(name,cmd,cwd=root,publish=True):
    log=(packet/"receipts" if publish else scratch)/(name+".log")
    with log.open("w") as f: rc=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
    if publish:(packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
    print(name,"rc",rc,flush=True);return rc

def aaf():
    here=root/"tb/verilator/avtp_rxmon"
    def pair(tag,rtl,ref):
        mdir=scratch/tag
        cmd=["make","-j16","-s","lockstep-build",f"RXMON_SRC={rtl}",f"REF_SRC={ref}",f"LS_MDIR={mdir}"]
        assert execute(tag+"-build",cmd,here,False)==0
        return [execute(tag+"-N"+n,[str(mdir)+n+"/Vavtp_rxmon_lockstep"],here) for n in ("1","8")]
    rtl=root/"hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"; ref=here/"reference/KL_avtp_rx_monitor_ctx_ref.sv"
    assert pair("aaf-clean",rtl,ref)==[0,0]
    spec=importlib.util.spec_from_file_location("mutants",here/"lockstep_mutants.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for name,edits,check,both in m.MUTATIONS:
        if not name.startswith(("consume race:","gap stop late:")):continue
        tag="aaf-"+name.split(":")[0].replace(" ","-")
        paths=[]
        for label,src in (("rtl",rtl),("ref",ref)):
            s=src.read_text()
            for a,b in edits:assert s.count(a)==1;s=s.replace(a,b)
            path=scratch/(tag+"-"+label+".sv");path.write_text(s);paths.append(path)
        assert pair(tag,*paths)==[1,1]
        for n in ("1","8"):
            log=(packet/"receipts"/(tag+"-N"+n+".log")).read_text()
            assert any("[FAIL]" in line and check in line for line in log.splitlines())
        print(tag,"caught by independent named count check in both shapes",flush=True)

def crf():
    here=root/"tb/verilator/crf_rx"; mdir=scratch/"crf-clean"
    assert execute("crf-clean-build",["make","-j16","-s","unit-build",f"UNIT_MDIR={mdir}"],here,False)==0
    assert execute("crf-clean",[str(mdir/"Vcrf_rx_sim")],here)==0

def gate():
    script=root/"scripts/ci_case_receipts_selftest.py"
    assert execute("receipt-selftest",[sys.executable,str(script)])==0
    # Execute changed source with original __file__, preserving its real inventory authority.
    src=script.read_text();assert src.count("len(names) + 1")==1
    mutated=src.replace("len(names) + 1","len(names)")
    target=scratch/"receipt-vacuous.py";target.write_text(mutated)
    code="import sys;sys.path.insert(0,sys.argv[1]);exec(compile(open(sys.argv[2]).read(),sys.argv[3],'exec'),{'__file__':sys.argv[3],'__name__':'__main__'})"
    assert execute("receipt-vacuous",[sys.executable,"-c",code,str(root/"scripts"),str(target),str(script)])==1
    assert "receipt control accepted: shard 0/34" in (packet/"receipts/receipt-vacuous.log").read_text()
    print("vacuous legal split refused by selftest",flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    tasks=[pool.submit(fn) for fn in (aaf,crf,gate)]
    for task in tasks:task.result()
print("PASS focused spot checks",flush=True)
