import json,subprocess,sys,datetime,re,html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
OUT=Path(__file__).resolve().parent
rows=[]
def add(name,prefix,tag='<span>'):
 rows.append({'id':name,'page':prefix+'\n'+tag+'\n## Old\n</span>\n\n## Real\n'})
for indent in range(5):
 for tag in ['<span>','</span>','<span title="x">']:
  add('tag-indent-'+str(indent)+'-'+tag,'- item\n\n  text',' '*indent+tag)
for name,prefix in [
 ('quote-inside','- item\n\n  > quote\n\n  text'),
 ('quote-outside','- item\n\n> quote\n\n  text'),
 ('list-inside','- item\n\n  - nested\n\n  text'),
 ('table-inside','- item\n\n  A | B\n  - | -\n\n  text'),
 ('table-outside','- item\n\nA | B\n- | -\n\n  text'),
 ('setext-inside','- item\n\n  title\n  ====\n\n  text'),
 ('setext-outside','- item\n\ntitle\n====\n\n  text'),
 ('fence-inside','- item\n\n  ```\n  code\n  ```\n\n  text'),
 ('fence-outside','- item\n\n```\ncode\n```\n\n  text'),
 ('html-inside','- item\n\n  <div>\n  x\n  </div>\n\n  text'),
 ('html-outside','- item\n\n<div>\nx\n</div>\n\n  text'),
 ('quote-marker-inert','> - item\n\n  text'),
 ('empty-ordinal','1.\n   first\n\n   text'),
 ('wide-ordinal','12) item\n\n    text'),
 ('sibling-after-blank','- item\n\n 1. next\n\n  text'),
 ('sibling-relative-indent','- item\n\n - next\n\n  text'),
 ('quote-lazy-list-marker','> quote\n- item\n\n  text'),
 ('table-list-looking-row','A | B\n- | -\n2. item\n\n   text'),
 ('table-empty-marker-row','A | B\n- | -\n-\n\n  text'),
 ('type1-cross-name','<pre>\n</style>\n- item\n\n  text'),
 ('fence-trailing-space','```\n- inert\n``` \t\n- item\n\n  text'),
 ('fence-invalid-trailer','```\n- inert\n``` x\n- item\n\n  text'),
 ]:add(name,prefix)
for i,page in enumerate(['Alpha\n===\n','text\n---\n','text\n-\n','> ## Q\n','- item\n\n  ## Inner\n']):rows.append({'id':'omission-'+str(i),'page':page})
(OUT/'renderer-inputs.json').write_text(json.dumps(rows,indent=2))
def render(row):
 req={'text':row['page'],'mode':'gfm','context':'kebag-logic/milan-fpga'}
 p=subprocess.run(['rtk','proxy','gh','api','markdown','--input','-'],input=json.dumps(req),capture_output=True,text=True)
 assert p.returncode==0,(row['id'],p.stderr)
 headings=[html.unescape(re.sub('<[^>]+>','',s)) for s in re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>',p.stdout,re.S)]
 return {**row,'request':req,'html':p.stdout,'headings':headings,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':p.returncode}
with ThreadPoolExecutor(max_workers=3) as pool: rendered=list(pool.map(render,rows))
(OUT/'renderer-responses.json').write_text(json.dumps(rendered,indent=2))
for label in ['base','head']:
 subprocess.run(['rtk','proxy','python3','-B',str(OUT/'classify.py'),str(OUT/'scratch'/label),str(OUT/'renderer-inputs.json'),str(OUT/('renderer-'+label+'.json'))],check=True)
results={label:json.loads((OUT/('renderer-'+label+'.json')).read_text()) for label in ['base','head']}
summary=[]
for row in rendered:
 r={'id':row['id'],'github':row['headings']}
 for label in results:r[label]=[h[1] for h in results[label][row['id']]['headings']]
 summary.append(r)
(OUT/'renderer-summary.json').write_text(json.dumps(summary,indent=2))
for r in summary:print(json.dumps(r))
