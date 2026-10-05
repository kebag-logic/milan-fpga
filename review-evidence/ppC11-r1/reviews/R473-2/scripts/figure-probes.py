#!/usr/bin/env python3
import pathlib,subprocess,sys,shutil,os
p=pathlib.Path(__file__).resolve().parents[1];root=p/'scratch/figure-probe'
if root.exists():shutil.rmtree(root)
subprocess.run(['git','clone','--quiet','--no-hardlinks',str(p/'scratch/tree'),str(root)],check=True)
os.environ['TMPDIR']=str(p/'scratch');script=root/'scripts/check-figures.py';pristine=script.read_text()
svg=root/'docs/diagrams/20-rtl-dataflow.svg';body=svg.read_text(); inv=root/'docs/diagrams/README.md';inventory=inv.read_text()
def run(label,args,want):
 r=subprocess.run([sys.executable,str(script),*args],capture_output=True,text=True)
 print(label,'rc',r.returncode);print(r.stdout,end='');print(r.stderr,end='');assert r.returncode==want
run('original selftest',['--selftest'],0)
for tag in ['image','feImage','foreignObject']:
 svg.write_text(body.replace('</svg>',f'<{tag}/></svg>'))
 run('real SVG '+tag,['--root',str(root)],1);svg.write_text(body)
for label,text in [('bad-root',body.replace('<svg ','<g ').replace('</svg>','</g>')),('missing-namespace',body.replace('xmlns="http://www.w3.org/2000/svg"','')),('truncated','<svg')]:
 svg.write_text(text);run('real SVG '+label,['--root',str(root)],1);svg.write_text(body)
for label,text in [('missing-heading',inventory.replace('## Inventory (hand-authored SVG)','## Replaced')),('empty-inventory','## Inventory (hand-authored SVG)\n')]:
 inv.write_text(text);run('real '+label,['--root',str(root)],1);inv.write_text(inventory)
extra=root/'docs/diagrams/reviewer/nested.svg';extra.parent.mkdir();extra.write_text(body);run('real nested file',['--root',str(root)],1);extra.unlink();extra.parent.rmdir()
# Disable a single rule at a time, without changing any self-test plant.
mutants=[
 ('image','("image", "feImage", "foreignObject")','("feImage", "foreignObject")'),
 ('feImage','("image", "feImage", "foreignObject")','("image", "foreignObject")'),
 ('foreignObject','("image", "feImage", "foreignObject")','("image", "feImage")'),
 ('root','if svg.tag != f"{SVG_NS}svg":','if False:'),
 ('viewBox','if "viewBox" not in svg.attrib:','if False:'),
 ('inventory-missing','if at < 0:', 'if False:'),
 ('inventory-empty','if not names:', 'if False:'),
 ('nested-format','problems.append(f"{rel}: not a figure format docs/README.md section 3 lists")','pass'),
]
for name,old,new in mutants:
 assert old in pristine;script.write_text(pristine.replace(old,new,1));run('selftest mutant '+name,['--selftest'],1);script.write_text(pristine)
run('restored real figures',['--root',str(root)],0)
