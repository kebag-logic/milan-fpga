import sys,subprocess,os,json,hashlib
from pathlib import Path
root=Path.cwd();r=Path("$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected")
sys.path.insert(0,str(root/"sw/builder"))
import endstation_builder as eb
records=[]
for shape in ("endstation_ax7101_1x1_tdm8","endstation_ax7101_8x8"):
    argv=eb.emit_soc_argv(eb.with_placement(eb.load_config(str(root/"configs"/(shape+".yaml"))), "split"))
    elf=r/"identity-final"/shape/"product/ctrl_app.elf"
    argv[argv.index("--ctrl-firmware")+1]=str(elf)
    argv += ["--entity-gen-dir",str(root/"configs/generated"/shape),"--no-compile-software"]
    for mode in ("base","candidate"):
        out=r/"identity-final-export"/shape/mode
        out.parent.mkdir(parents=True,exist_ok=True)
        with (out.parent/(mode+".log")).open("w") as log:
            subprocess.run([sys.executable,"-B",str(r/"identity-export-worker.py"),mode,*argv,"--output-dir",str(out)],cwd=root,env=dict(os.environ,PYTHONHASHSEED="0",COURSIER_MODE="offline",SBT_OPTS="-Dsbt.offline=true"),stdout=log,stderr=subprocess.STDOUT,timeout=1800,check=True)
    base=r/"identity-final-export"/shape/"base";candidate=base.with_name("candidate")
    names=["csr.csv","gateware/alinx_ax7101.v",*[str(p.relative_to(base)) for p in sorted((base/"gateware").glob("*.init"))]]
    for name in names:
        a=(base/name).read_bytes();b=(candidate/name).read_bytes()
        records.append(dict(shape=shape,file=name,identical=a==b,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
    print(shape,"byte-identical",all(row["identical"] for row in records if row["shape"]==shape),flush=True)
(r/"identity-final-export-compare.json").write_text(json.dumps(dict(status="PASS" if all(row["identical"] for row in records) else "FAIL",method="Original SoC source from 4a89ddcd and candidate source, same AX configurations and proven-identical firmware; same timestamp, PYTHONHASHSEED=0 and deterministic instance display for hierarchy comments; raw output bytes, no normalization; no other checkout modified.",records=records),indent=2)+"\n")
raise SystemExit(not all(row["identical"] for row in records))
