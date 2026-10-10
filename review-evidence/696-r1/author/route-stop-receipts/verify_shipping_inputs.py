import hashlib,json,subprocess,sys
from pathlib import Path
w=Path(__file__).resolve().parent
main=Path('$LANES/696-maap-annexb')
repo=Path('$VALIDATION_STORAGE/696-a570/resume-area/validation')
shipping=Path('$VALIDATION_STORAGE/696-a570/resume-differential/shipping')
sys.path.insert(0,str(main/'syn/ooc'))
import pp_resource_gate
head=subprocess.check_output(['git','-C',str(main),'rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()==head
for root in [main,repo]:
 subprocess.run(['git','-C',str(root),'diff','--quiet'],check=True)
 subprocess.run(['git','-C',str(root),'diff','--cached','--quiet'],check=True)
rows=[]
for shape in ['ax7101','ax8x8']:
 directory=shipping/shape/'gateware'
 script=(directory/'baseline_integrated.tcl').read_text()
 files,roots=pp_resource_gate.located(directory,script)
 compared=0;problems=[]
 for p in files:
  if p.is_relative_to(repo):
   relative=p.relative_to(repo);source=main/relative
   if not source.is_file() or p.read_bytes()!=source.read_bytes():problems.append(str(relative))
   compared+=1
 images=json.loads((directory/'baseline_images.json').read_text())
 for item in images:
  assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
 rows.append(dict(shape=shape,input_files=len(files),lane_file_comparisons=compared,verified_images=len(images),inputs_sha256=pp_resource_gate.inputs(directory,script),problems=problems))
 assert compared>100 and not problems
result=dict(head=head,rows=rows)
(w/'shipping-input-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
