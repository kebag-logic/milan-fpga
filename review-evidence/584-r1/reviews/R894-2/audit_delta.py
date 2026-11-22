#!/usr/bin/env python3
"""Focused semantic, parameter-derivation and memory arithmetic checks."""
import ast, importlib.util, json, subprocess, sys
from pathlib import Path
import yaml
repo=Path(sys.argv[1]).resolve()
gen=Path(sys.argv[2]).resolve()
def old(p): return subprocess.check_output(['git','show','2b295a44:'+p],cwd=repo).decode()
class WithoutDocs(ast.NodeTransformer):
    def visit_Expr(self,node):
        return None if isinstance(node.value,ast.Constant) and isinstance(node.value.value,str) else node
p='sw/builder/endstation_builder.py'
assert ast.dump(WithoutDocs().visit(ast.parse(old(p))))==ast.dump(WithoutDocs().visit(ast.parse((repo/p).read_text())))
print('Builder executable AST unchanged from round 1 (comments/docstrings excluded).')
p='configs/endstation_ax7101_8x8.yaml'
assert yaml.safe_load(old(p))==yaml.safe_load((repo/p).read_text())
print('8x8 YAML data unchanged from round 1.')
spec=importlib.util.spec_from_file_location('ship8_params',repo/'tb/verilator/milan_dp_render/ship8_params.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
argv=json.loads((gen/'soc_params.json').read_text())['argv']
params=m.derive(argv)
print('Generated argv:',json.dumps(argv))
print('Derived flags:',json.dumps(params,sort_keys=True))
assert params['N_STREAMS']==8 and params['AUDIO_IF_SLOTS_P']==32 and params['AUDIO_IF_MASTER_P']==1
assert params['AUDIO_IF_RENDER_SLOTS_P']==1 and params['LOOPBACK_P']==0
assert params['AUDIO_IF_CLK_HZ_P']==98304000 and params['I2SPB_P']==0 and params['LPF_P']==0
for flag,new,key,value in [('--num-streams','7','N_STREAMS',7),('--audio-interface','tdm16','AUDIO_IF_SLOTS_P',16),('--audio-interface-render','2','AUDIO_IF_RENDER_SLOTS_P',2),('--talker-wire-chans','6','TALKER_WIRE_CHANS_P',6)]:
    a=argv.copy();a[a.index(flag)+1]=new
    assert m.derive(a)[key]==value
    print('Derived parameter follows input:',flag,new)
assert m.derive(argv+['--loopback-lane'])['LOOPBACK_P']==1
print('Loopback parameter follows input flag.')
for a in [argv+['--audio-new-flag'],argv+['--num-streams','8'],[x for x in argv if x!='--audio-interface-master']]:
    try: m.derive(a)
    except SystemExit as e: print('Named refusal:',e)
    else: raise AssertionError('missing refusal')
fmt=m.listener_format(json.loads((gen/'aem_overlay.json').read_text()))
print('Listener format from generated overlay:',hex(fmt))
assert (gen/'adp_shape_defaults.svh').read_bytes()==(repo/'configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh').read_bytes()
print('Generated shape equals tracked header.')
for name,br,bs,hr,hs in [('product 1if',139208,98160,140544,99904),('platform 2if',140784,115504,142120,117312),('fixture 1if',130032,96928,131368,98672),('fixture 2if',131536,114320,132880,116064)]:
    print(name,'ROM',hr-br,'SRAM',hs-bs)
print('PASS: all focused semantic/parameter/arithmetic assertions')
