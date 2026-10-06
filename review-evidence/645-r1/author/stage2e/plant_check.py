import importlib.util,sys,tempfile,json,hashlib,os
from pathlib import Path
repo=Path(os.environ['REPO']);work=Path(os.environ['STAGE_ROOT']);out=Path(os.environ['EVIDENCE'])
def module(name,rel):
    spec=importlib.util.spec_from_file_location(name,repo/rel)
    mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
fr=module('fr_plant','tb/verilator/follow_ring/mutants.py')
cc=module('cc_plant','tb/verilator/capture_coherence/mutants.py')
rows=[]
with tempfile.TemporaryDirectory(dir=work,prefix='plant-') as temp:
    for name,define,edits,cmap_edits,leg,check in fr.MUTANTS:
        parts=[]
        for src,todo in [(fr.DATAPATH,edits),(fr.CAPTURE,cmap_edits)]:
            dst=Path(temp)/(name+'-'+src.name)
            assert fr.plant(src,todo,dst) is None
            if todo: assert dst.read_bytes()!=src.read_bytes()
            parts.append({'source':str(src.resolve().relative_to(repo)), 'edits':len(todo),'planted_sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
        if define:
            text=''.join(p.read_text() for p in (repo/'tb/verilator/follow_ring').iterdir() if p.suffix == '.sv')
            assert define in text
        rows.append({'suite':'follow_ring','arm':name,'define':define,'plants':True,'parts':parts})
    for leg,name,edits,breaks in cc.MUTATIONS:
        src=cc.LEGS[leg][4];mutated=cc.mutate(src.read_text(),edits)
        assert mutated is not None and mutated!=src.read_text(),name
        rows.append({'suite':'capture_coherence','leg':leg,'arm':name,'source':str(src.resolve().relative_to(repo)),'edits':len(edits),'plants':True,'planted_sha256':hashlib.sha256(mutated.encode()).hexdigest()})
(out/'mutation-planting.json').write_text(json.dumps(rows,indent=2)+'\n')
for suite in ['follow_ring','capture_coherence']:print(suite,sum(r['suite']==suite for r in rows),'arms plant')
