#!/usr/bin/env python3
"""Read actual descriptor bytes for every tracked configuration with the option requested."""
import argparse, pathlib, sys, yaml, json, tempfile
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);a=p.parse_args()
sys.path[:0]=[str(a.source/'sw/builder'),str(a.source/'avdecc')]
sys.dont_write_bytecode=True
import endstation_builder as b, gen_aem_store as g
scratch=pathlib.Path(__file__).resolve().parent/'scratch'; records=[]
for path in sorted((a.source/'configs').glob('endstation_*.yaml')):
 raw=yaml.safe_load(path.read_text())
 fab=raw.setdefault('audio_interface',{}).setdefault('cluster_mapping',{}).setdefault('fabric',{})
 fab['input_loopback_lane']=True
 with tempfile.TemporaryDirectory(dir=scratch) as tmp:
  new=pathlib.Path(tmp)/path.name;new.write_text(yaml.safe_dump(raw))
  try: cfg=b.load_config(new); m=g.build_model(g.spec_from_overlay(b.emit_aem_overlay(cfg)))
  except (b.ConfigError, ValueError) as error:
   records.append(dict(config=path.name,enabled='REFUSED',reason=str(error)));continue
  clusters=[];ports=[]
  for typ,idx,off,size in m['directory']:
   desc=m['rom'][off:off+size]
   if typ==0x14:
    count=int.from_bytes(desc[84:86],'big');assert count==1
    clusters.append(idx)
   if typ==0x0e:
    n=int.from_bytes(desc[12:14],'big');base=int.from_bytes(desc[14:16],'big');maps=int.from_bytes(desc[16:18],'big')
    assert n>0 and maps==0
    ports.append(dict(index=idx,clusters=n,base=base,maps=maps))
  assert len(clusters)>0 and len(ports)>0
  records.append(dict(config=path.name,enabled='PASS',mono_clusters=len(clusters),input_ports=ports,input_keys=m['DYNMAP']['KEYS'],fixed_pages=m['DYNMAP']['PNMAPS']))
assert sum(r['enabled']=='PASS' for r in records)==2
print(json.dumps(records,indent=2))
