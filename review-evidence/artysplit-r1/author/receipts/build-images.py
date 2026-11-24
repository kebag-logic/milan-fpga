"""Foreground Arty implementation sweep. Run only after the point is qualified."""
import concurrent.futures,hashlib,json,os,subprocess,sys
from pathlib import Path
root=Path.cwd();scratch=Path("$VALIDATION_STORAGE/artysplit-a829/r4")
sys.path.insert(0,str(root/"sw/builder"))
import endstation_builder as eb
config=root/"configs/endstation_arty_split.yaml"
elf=Path(sys.argv[1]).resolve(strict=True)
out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
# The caller must provide a completed owner-bound qualification receipt.
qualification=json.loads(Path(sys.argv[3]).read_text())
required_checks=("owner-model", "share", "record-classes", "retry-costs", "transmit-costs", "egress-ledger")
if (qualification.get("status")!="PASS" or qualification.get("cpu_hz")!=80_000_000
        or qualification.get("point")!="arty-1x1"
        or qualification.get("shape")!=[1,1,2]
        or qualification.get("kind")!="complete measured Arty FPGA point"
        or any(qualification.get("checks",{}).get(name)!="PASS" for name in required_checks)):
    raise SystemExit("refused: missing qualified 80 MHz point")
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
if head=='4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2' or subprocess.run(['git','diff','--quiet','HEAD'],cwd=root).returncode:
    raise SystemExit('refused: commit the qualified round-4 source before routing')
inputs=dict(head=head,firmware_sha256=hashlib.sha256(elf.read_bytes()).hexdigest(),
            qualification_sha256=hashlib.sha256(Path(sys.argv[3]).read_bytes()).hexdigest())
(out/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
eb.build(str(config),placement="split")
args=eb.emit_soc_argv(eb.load_config(str(config)))
args[args.index("--ctrl-firmware")+1]=str(elf)
args += ["--entity-gen-dir",str(root/"configs/generated/endstation_arty_split")]
directives=("ExtraPostPlacementOpt","AltSpreadLogic_high","ExtraTimingOpt")
env=dict(os.environ,PYTHONHASHSEED="0",COURSIER_MODE="offline",SBT_OPTS="-Dsbt.offline=true",VIVADO_SLOTS="2",VIVADO_MIN_GB="20")
slot="<home-path>/milan-fpga-management/2026-09-23/vivado-slot.sh"
settings="<home-path>/Xilinx2/2026.1/Vivado/settings64.sh"
def one(directive):
    work=out/directive
    argv=["<home-path>/litex-milan/venv/bin/python3","-B",str(root/"sw/litex/milan_soc.py"),*args,
          "--place-directive",directive,"--vivado-max-threads","16",
          "--build","--output-dir",str(work)]
    command=[slot,"bash","-c",'source "$1"; shift; exec "$@"',"arty-build",settings,*argv]
    (out/(directive+".command.json")).write_text(json.dumps(command,indent=2)+"\n")
    with (out/(directive+".log")).open("w") as log:
        proc=subprocess.run(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=28800)
    result=dict(directive=directive,rc=proc.returncode,output=str(work))
    (out/(directive+".result.json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result),flush=True)
    return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results=list(pool.map(one,directives))
(out/"results.json").write_text(json.dumps(results,indent=2)+"\n")
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==head
assert subprocess.run(['git','diff','--quiet','HEAD'],cwd=root).returncode==0
assert hashlib.sha256(elf.read_bytes()).hexdigest()==inputs['firmware_sha256']
raise SystemExit(any(r["rc"] for r in results))
