#!/usr/bin/env python3
"""Independently enumerate packed descriptors and compare unchanged-config artifacts."""
import hashlib, json, pathlib, subprocess, sys, types
root=pathlib.Path(sys.argv[1]).resolve(); mode=sys.argv[2]
packet=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(root/"sw/builder"))
module=types.ModuleType("endstation_builder")
module.__file__=str(root/"sw/builder/endstation_builder.py")
sys.modules[module.__name__]=module
source=(subprocess.check_output(["git","show","dd163e41:sw/builder/endstation_builder.py"],cwd=root,text=True)
        if mode=="base" else pathlib.Path(module.__file__).read_text())
exec(compile(source,module.__file__,"exec"),module.__dict__)
results={}
for config in sorted((root/"configs").glob("endstation_*.yaml")):
    for placement in ("all-fabric","split"):
        path=config
        if mode=="base" and config.stem=="endstation_ax7101_8x8":
            path=packet/"scratch"/config.name
            path.write_bytes(subprocess.check_output(["git","show","dd163e41:configs/"+config.name],cwd=root))
        a=module._derive_artifacts(path,placement)
        image=module._entity_model_image(a.cfg,a.overlay)
        import gen_aem_store as store
        model=store.build_model(store.spec_from_overlay(a.overlay))
        # Raw served descriptor bytes, independent of the layout-count helpers.
        descriptors={(t,i): bytes(model["rom"][b:b+n]) for t,i,b,n in model["directory"]}
        if not isinstance(descriptors,dict):
            print("model type",type(model),flush=True)
        rows=[]
        for key,b in descriptors.items():
            if not isinstance(b,(bytes,bytearray)): continue
            typ=int.from_bytes(b[:2],"big")
            if typ in (14,15):
                count=int.from_bytes(b[12:14],"big"); base=int.from_bytes(b[14:16],"big")
                maps=int.from_bytes(b[16:18],"big")
                rows.append((typ,int.from_bytes(b[2:4],"big"),count,base,maps))
                if mode!="base": assert count>=1
                if typ==14: assert maps==0
            elif typ==20: assert int.from_bytes(b[84:86],"big")==1
        assert rows, "descriptor census cannot be empty"
        fields={k:getattr(a,k) for k in ("argv","overlay","lwsrp","lwsrp_svh","csr_svh","adp_svh","aem_rom","iparams","shape","marks","est","plan","sweep","nvm_split")}
        fields.update(image)
        def digest(v):
            if not isinstance(v,(str,bytes)): v=json.dumps(v,sort_keys=True)
            if isinstance(v,str): v=v.replace(str(path),str(config)).encode()
            return hashlib.sha256(v).hexdigest()
        results[config.stem+"/"+placement]={"id":str(a.cfg["entity"]["entity_model_id"]),"ports":rows,"hashes":{k:digest(v) for k,v in fields.items()}}
        print(config.stem,placement,"ports",rows,"image",[(k,len(v)) for k,v in image.items()],flush=True)
(packet/("configs-"+mode+".json")).write_text(json.dumps(results,indent=2)+"\n")
