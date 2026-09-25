import copy,json,shlex,subprocess,sys,yaml
from pathlib import Path
root=Path("$LANES/400-403-declaration-truth")
sys.path.insert(0,str(root/"sw/builder"))
import endstation_builder as eb
cwd=root/"tb/verilator/csr"
tmp=Path("$VALIDATION_STORAGE/400-403-a313-tools/csr-matrix");tmp.mkdir(parents=True,exist_ok=True)
plan=subprocess.run(["make","--no-print-directory","-nB","obj_dir/Vcsr_sim","VERILATOR=$VALIDATION_STORAGE/400-403-a313-tools/bin/verilator"],cwd=cwd,check=True,capture_output=True,text=True).stdout
commands=[shlex.split(line) for line in plan.replace("\\\n"," ").splitlines() if line and not line.startswith("#")]
assert len(commands)==1,commands
for path in sorted((root/"configs").glob("endstation_*.yaml")):
 raw=yaml.safe_load(path.read_text())
 for bits in range(4):
  label=path.stem+"-reset"+str(bits);fixture=tmp/label;gen=fixture/"gen";gen.mkdir(parents=True,exist_ok=True)
  mutated=copy.deepcopy(raw);mutated.setdefault("srp",{}).update(enable_at_reset=bool(bits&1),talker_declare_at_reset=bool(bits&2))
  cfgpath=fixture/"config.yaml";cfgpath.write_text(yaml.safe_dump(mutated,sort_keys=False))
  cfg=eb.load_config(cfgpath)
  (gen/"adp_shape_defaults.svh").write_text(eb.emit_adp_shape_svh(cfg))
  (gen/"lwsrp_csr_defaults.svh").write_text(eb.emit_csr_defaults_svh(cfg))
  co=bool(raw.get("clocking",{}).get("crf_output",{}).get("enabled",False))
  ci=bool(raw.get("clocking",{}).get("crf_sink",False))
  talk=((0x4801 if co else 0x4001)<<16)|(len(raw["streams"]["talkers"])+int(co))
  listen=((0x4801 if ci else 0x4001)<<16)|(len(raw["streams"]["listeners"])+int(ci))
  args=list(commands[0]);args[1]="+incdir+"+str(fixture)
  mdir="obj_decl_"+label.replace("-","_")
  args.extend(["--Mdir",mdir,"-CFLAGS",f"-DCSR_DECL_TALK={talk}u -DCSR_DECL_LIST={listen}u -DCSR_SRP_RESET_BITS={bits}u -Wall -Wextra"])
  print("MATRIX",label,"talk",hex(talk),"listen",hex(listen),flush=True)
  print("COMMAND",repr(args),flush=True)
  subprocess.run(args,cwd=cwd,check=True,timeout=14400)
  subprocess.run(["./"+mdir+"/Vcsr_sim"],cwd=cwd,check=True,timeout=14400)
  print("MATRIX PASS",label,flush=True)
