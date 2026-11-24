#!/usr/bin/env python3
"""Run the existing platform PHC slice against two isolated adoption faults.
Usage: python3 probe.py REPO OUTPUT VERILATOR
All clones and build products stay below OUTPUT/scratch. No input tree edits.
"""
import concurrent.futures, hashlib, os, pathlib, subprocess, sys
repo, out, simulator = map(pathlib.Path, sys.argv[1:])
repo=repo.resolve(); out=out.resolve(); simulator=simulator.resolve()
head="bbfdb6746d585e490508783dc8a88c79fbab02c0"
(out/"scratch").mkdir(parents=True,exist_ok=True)
version=subprocess.check_output([str(simulator),"--version"],text=True)
assert "5.050" in version, version
(out/"simulator-identity.txt").write_text(version+"sha256 "+hashlib.sha256(simulator.read_bytes()).hexdigest()+"\n")
def run(case):
    tree=out/"scratch"/case
    log=out/(case+".log")
    with log.open("w") as f:
        def cmd(args,cwd=repo):
            f.write("COMMAND "+" ".join(map(str,args)).replace(str(repo),"<source>").replace(str(out),"<packet>")+"\n");f.flush()
            subprocess.run(list(map(str,args)),cwd=cwd,stdout=f,stderr=subprocess.STDOUT,check=True)
        cmd(["git","clone","--quiet","--shared","--no-checkout",repo,tree])
        cmd(["git","checkout","--quiet","--detach",head],tree)
        cmd(["git","config","submodule.gptp-processor.url",repo/"gptp-processor"],tree)
        cmd(["git","-c","protocol.file.allow=always","submodule","update","--init","gptp-processor"],tree)
        mf=tree/"tb/verilator/gptp_plane/Makefile"
        mf.write_text(mf.read_text().replace("--build -j 0", "--build -j 5"))
        if case=="delayed-announce":
            path=tree/"gptp-processor/hdl/ucode/gen_gptp_ucode.py"
            s=path.read_text()
            before='    p.emit("WRST", ra=0, imm=RG_TMR | 2, fmt=FMT_Q)   # stop the watch'
            assert s.count(before)==1
            s=s.replace(before,'    p.emit("MOVE", rd=RT, ra=0, imm=2)\n    p.emit("WRST", ra=RT, imm=RG_TMR | 3, fmt=FMT_Q)\n'+before)
            before='    p.emit("BR", label=LB["ANNTX"])'
            assert s.count(before)==1
            s=s.replace(before,'    p.emit("END")')
            path.write_text(s)
        if case=="retained-slave-rate":
            path=tree/"gptp-processor/hdl/top/KL_gptp_engine.sv"
            s=path.read_text()
            before="""                phc_addend_we_o <= 1'b1;
                phc_addend_o    <= st_wdata_w[31:0];
                phc_slew_left_r   <= 2'd0;"""
            assert s.count(before)==1
            s=s.replace(before,"""                if (phc_slew_active_o) begin
                  phc_addend_we_o <= 1'b1;
                  phc_addend_o    <= st_wdata_w[31:0];
                end
                phc_slew_left_r   <= 2'd0;""")
            path.write_text(s)
        diff=subprocess.check_output(["git","diff","--no-ext-diff"],cwd=tree/"gptp-processor",text=True)
        (out/(case+".patch")).write_text(diff)
        env=os.environ.copy();env.update(MAKEFLAGS="--no-print-directory",CCACHE_DISABLE="1",PYTHONDONTWRITEBYTECODE="1")
        command=["make","-j16","--no-print-directory","-C","tb/verilator/gptp_plane","run","VERILATOR="+str(simulator)]
        f.write("COMMAND "+" ".join(command)+"\n");f.flush()
        result=subprocess.run(command,cwd=tree,env=env,stdout=f,stderr=subprocess.STDOUT)
    raw=log.read_text().replace(str(out),"<packet>").replace(str(repo),"<source>")
    log.write_text(raw)
    (out/(case+".rc")).write_text(str(result.returncode)+"\n")
    return case,result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for case,rc in pool.map(run,["baseline","delayed-announce","retained-slave-rate"]):
        print(case,rc,flush=True)
