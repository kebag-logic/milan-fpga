import json,sys,tempfile,subprocess,os
from pathlib import Path
OUT=Path(__file__).resolve().parent
if len(sys.argv)==1:
 for label in ['base','head']:
  subprocess.run(['rtk','proxy','python3','-B',str(Path(__file__).resolve()),label],check=True)
 results={label:json.loads((OUT/('consumer-'+label+'.json')).read_text()) for label in ['base','head']}
 (OUT/'consumer-summary.json').write_text(json.dumps(results,indent=2));print(json.dumps({label:[{'id':r['id'],'tag_indent':r['tag_indent'],'findings':r['findings'],'exempt':r['exempt']} for r in rows] for label,rows in results.items()},indent=2));sys.exit()
sys.dont_write_bytecode=True;label=sys.argv[1];sys.path.insert(0,str(OUT/'scratch'/label))
import gen_toc as toc;import check_em_dash as gate
heading='## Old \u2014 heading\n'
tail='\n## Alpha\n\nAlpha body.\n\n## Beta\n\nBeta body.\n\n## Gamma\n\nGamma body.\n'
nav='## Contents\n\n- **[Old \u2014 heading](#old--heading)** -- Copied.\n- **[Alpha](#alpha)** -- A.\n- **[Beta](#beta)** -- B.\n- **[Gamma](#gamma)** -- C.\n\n'
head_page='# Page\n\n'+nav+heading+tail
rows=[]
with tempfile.TemporaryDirectory(prefix='r237-git-',dir=OUT/'scratch') as tmp:
 repo=Path(tmp)
 env=dict(os.environ,GIT_AUTHOR_NAME='Synthetic Reviewer',GIT_AUTHOR_EMAIL='reviewer@example.invalid',GIT_COMMITTER_NAME='Synthetic Reviewer',GIT_COMMITTER_EMAIL='reviewer@example.invalid')
 def git(*args):return subprocess.check_output(['rtk','proxy','git','-C',str(repo),*args],env=env,text=True).strip()
 git('init','-q','--initial-branch=main')
 cases={}
 for spaces in range(5):
  for tag in ['<span>','</span>','<span title="x">']:
   name=str(spaces)+'-'+str(len(cases))+'.md';page='# Page\n\n- item\n\n  text\n'+' '*spaces+tag+'\n'+heading+'</span>\n'+tail
   cases[name]={'id':name,'tag_indent':spaces,'tag':tag,'base_page':page};(repo/name).write_text(page)
 git('add','.');git('-c','commit.gpgsign=false','commit','-qm','Synthetic base');base=git('rev-parse','HEAD')
 for name in cases:(repo/name).write_text(head_page)
 git('add','.');git('-c','commit.gpgsign=false','commit','-qm','Synthetic head');head=git('rev-parse','HEAD')
 for name,row in cases.items():
  v=gate.Verdict();gate.judge_page(repo,base,gate.Change(name,name),v)
  rows.append({**row,'synthetic_base':base,'synthetic_head':head,'head_page':head_page,'base_headings':toc.headings(row['base_page']),'base_navigation':toc.render(toc.plan(row['base_page']),{},'--'),'head_provenance':toc.generated_block(head_page,name),'findings':v.findings,'exempt':v.exempt,'judged':v.judged})
(OUT/('consumer-'+label+'.json')).write_text(json.dumps(rows,indent=2))
