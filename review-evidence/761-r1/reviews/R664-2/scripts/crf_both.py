#!/usr/bin/env python3
import concurrent.futures,importlib.util,os,pathlib,subprocess,sys
sys.dont_write_bytecode=True
root=pathlib.Path(sys.argv[1]).resolve();packet=pathlib.Path(sys.argv[2]).resolve()
here=root/"tb/verilator/crf_rx";work=packet/"scratch/crf-both";work.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location("crf_mutants",here/"mutants.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rtl=(root/"hdl/ieee1722/crf/KL_crf_rx.sv").read_text();cpp=(here/"sim_main.cpp").read_text()
model={
 "silence_not_interrupted":("if (bound && !stop) cnt_i++;","if (false) cnt_i++;"),
 "gap_not_interrupted":(m.GAP_REPLICA,"if (false) cnt_i++;"),
 "unbind_interrupts":("if (locked) { locked = false; cnt_u++; }","if (locked) { locked = false; cnt_u++; cnt_i++; }"),
 "unbind_edge_timeout_interrupts":("if (bound && !stop) cnt_i++;","if (!stop) cnt_i++;"),
 "stopped_silence_interrupts":("if (bound && !stop) cnt_i++;","if (bound) cnt_i++;")}
cases=[(name,((a,b),),(model[name],),check) for name,a,b,check in m.UNIT_MUTANTS]+list(m.BOTH_MUTANTS)
env=os.environ.copy();env.update(VERILATOR=str(packet/"scripts/sim_limited.py"),MAKEFLAGS="-j16",TMPDIR=str(work),PYTHONDONTWRITEBYTECODE="1")
def run(case):
 name,re,ce,check=case
 r=m.plant(rtl,re);c=m.plant(cpp,ce);assert r is not None and c is not None
 rp=work/(name+".sv");cp=work/(name+".cpp");rp.write_text(r);cp.write_text(c);mdir=work/(name+"-obj")
 with (work/(name+"-build.log")).open("w") as f:
  rc=subprocess.run(["make","-j16","-s","unit-build",f"RX_RTL={rp}",f"UNIT_CPP={cp}",f"UNIT_MDIR={mdir}"],cwd=here,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 assert rc==0,(name,"build",rc)
 result=subprocess.run([str(mdir/"Vcrf_rx_sim")],cwd=here,env=env,capture_output=True,text=True)
 (packet/"receipts"/("crf-both-"+name+".log")).write_text(result.stdout+result.stderr)
 (packet/"receipts"/("crf-both-"+name+".rc")).write_text(str(result.returncode)+"\n")
 assert result.returncode==1,(name,result.returncode)
 lines=[s for s in result.stdout.splitlines() if "FAIL" in s and check in s]
 assert lines,(name,"named independent count check missing")
 return name+": CAUGHT in engine and replica; "+lines[0].strip()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for line in pool.map(run,cases):print(line,flush=True)
print("PASS 7 paired CRF controls",flush=True)
