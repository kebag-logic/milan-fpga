#!/usr/bin/env python3
"""Export an exact revision's SoC with current unchanged builder inputs, without software."""
import argparse, json, pathlib, subprocess, sys, types
ap=argparse.ArgumentParser();ap.add_argument("revision");ap.add_argument("config");ap.add_argument("output",type=pathlib.Path)
ap.add_argument("--firmware",type=pathlib.Path)
a=ap.parse_args(); root=pathlib.Path.cwd(); a.output.mkdir(parents=True,exist_ok=True)
sys.path[:0]=[str(root/"sw/litex"),str(root/"sw/builder")]
import endstation_builder as eb
a.config=str(pathlib.Path(a.config).resolve())
cfg=eb.load_config(a.config)
art=eb.build(a.config,write_fragment=False)
entity=pathlib.Path(art["paths"]["platform_shape"]).parent
socpath=root/"sw/litex/milan_soc.py"
source=subprocess.check_output(["git","show",a.revision+":sw/litex/milan_soc.py"])
soc=types.ModuleType("review_soc");soc.__file__=str(socpath);sys.modules[soc.__name__]=soc
exec(compile(source,str(socpath),"exec"),soc.__dict__)
from litex.soc.integration.builder import Builder
original=Builder._generate_includes
def includes(self,with_bios=True):
 return original(self,with_bios=False)
Builder._generate_includes=includes
sys.argv=[str(socpath),*eb.emit_soc_argv(cfg),"--entity-gen-dir",str(entity),"--output-dir",str(a.output/"export"),"--no-compile-software"]
if a.firmware:sys.argv += ["--ctrl-mailbox","--ctrl-firmware",str(a.firmware.resolve())]
(a.output/"argv.json").write_text(json.dumps(sys.argv,indent=2))
soc.main()
print("RESULT: PASS export",a.revision,cfg["name"])
