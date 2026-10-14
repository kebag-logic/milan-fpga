#!/usr/bin/env python3
"""Build the changed media-NCO child recipe in disposable storage."""
import hashlib,json,pathlib,subprocess,sys,tarfile,io,os,re
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(__file__).resolve().parent
work=packet/"scratch/media-nco";work.mkdir(parents=True,exist_ok=True)
paths=["tb/verilator/media_nco","tb/common","hdl/common","hdl/ieee1722/crf/KL_media_nco.sv"]
raw=subprocess.check_output(["git","-C",str(root),"archive","HEAD",*paths])
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(work,filter="data")
compiler=pathlib.Path(sys.argv[2]).resolve()
version=subprocess.check_output([str(compiler),"--version"],text=True).strip()
assert "Verilator 5.050" in version,version
cmd=["make","-j16","-C",str(work/"tb/verilator/media_nco"),"VERILATOR="+str(compiler),"VERILATOR_JOBS=16"]
with (packet/"media-nco.log").open("w") as log:
 rc=subprocess.run(cmd,env=dict(os.environ,TMPDIR=str(packet/"scratch")),stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
raw_log=(packet/"media-nco.log").read_bytes()
(packet/"scratch/media-nco.raw.log").write_bytes(raw_log)
public_log=re.sub(r"/home/[^\s\"\x27]+","<compiler-runtime-path>",raw_log.decode())
public_log=public_log.replace(str(packet),"<packet>").replace(str(compiler),"<verified-5.050>")
(packet/"media-nco.log").write_text(public_log)
result={"version":version,"compiler_sha256":hashlib.sha256(compiler.read_bytes()).hexdigest(),"command":["make","-j16","-C","<scratch>/media-nco/tb/verilator/media_nco","VERILATOR=<verified-5.050>","VERILATOR_JOBS=16"],"returncode":rc}
(packet/"media-nco.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result));raise SystemExit(rc)
