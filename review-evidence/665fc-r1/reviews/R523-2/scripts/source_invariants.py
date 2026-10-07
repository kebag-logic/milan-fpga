#!/usr/bin/env python3
"""Source preservation and regeneration checks, without modifying source files."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument("--source",type=pathlib.Path,default=pathlib.Path.cwd());p.add_argument("--packet",type=pathlib.Path,required=True);a=p.parse_args();root=a.source.resolve();out=a.packet.resolve()
def git(*args):return subprocess.check_output(["git",*args],cwd=root)
base="6714181d0c8a16e2983f85b724f4d688f5111835";round1="021b9c1fb966e9a1a4acef6b5233edd3518f32a0";head="db9aa8c9b135b34ff3d070a979dee70440b37cc6"
delta=git("diff","--name-only",round1,head).decode().splitlines()
assert "hdl/milan/mailbox/KL_mbx.sv" not in delta
prod=[p for p in delta if p.startswith("sw/firmware/ctrl/") and p.endswith(".c") and "/host/" not in p and "/test/" not in p]
assert not prod
assert not git("diff",base,head,"--","sw/litex","sw/firmware/milan_baremetal","configs","protocol-processor","gptp-processor","third_party/verilog-axis")
assert not git("diff","dd86e68b",head,"--","hdl","tb/verilator/mbx/tb_mbx_top.sv")
top="hdl/milan/mailbox/KL_mbx.sv"
ports=lambda b:b.split(b"module KL_mbx",1)[1].split(b");",1)[0]
assert ports(git("show",base+":"+top))==ports((root/top).read_bytes())
regen=out/"scratch/cli-regeneration";shutil.copytree(root/"sw/mailbox",regen/"sw/mailbox",dirs_exist_ok=True)
env=dict(os.environ,TMPDIR=str(out/"scratch"),PYTHONDONTWRITEBYTECODE="1")
p=subprocess.run([sys.executable,"-B",str(regen/"sw/mailbox/gen_mailbox.py"),"--write"],capture_output=True,text=True,env=env)
assert p.returncode==0,p.stderr
generated=[top,"hdl/milan/mailbox/KL_mbx_pkg.sv","sw/firmware/ctrl/mbx/mbx_contract.h","docs/reference/MAILBOX_CONTRACT.md"]
hashes={}
for f in generated:
    data=(root/f).read_bytes();assert data==(regen/f).read_bytes();hashes[f]=hashlib.sha256(data).hexdigest()
old=git("show",round1+":sw/mailbox/mailbox.yaml");new=(root/"sw/mailbox/mailbox.yaml").read_bytes()
# The register blocks and capacities did not change in round 2.
import yaml
before=yaml.safe_load(old);after=yaml.safe_load(new)
for k in ("registers","interface_registers","interface_filter_registers","channel_registers","version","interfaces","timers","tick_ms","index_bits"):
    assert before[k]==after[k],k
for b,n in zip(before["channels"],after["channels"]):
    for k in ("id","rx","tx","max_frame_bytes","rate","accept"):assert b[k]==n[k],(b["name"],k)
print(json.dumps(dict(exact_head=head,round2_top_registers_and_production_c_unchanged=True,full_pr_top_ports_unchanged=True,default_build_inputs_unchanged=True,hdl_unchanged_since_area_head="dd86e68b",generated_cli_write_sha256=hashes,round2_changed_paths=delta),indent=2))
