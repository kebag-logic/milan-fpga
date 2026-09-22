import json,subprocess,datetime,re,html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
OUT=Path(__file__).resolve().parent
rows=json.loads((OUT/'public-packet/author/fixtures.json').read_text())
comments=json.loads((OUT/'comments437-author-manager.json').read_text())
body=next(c['body'] for c in comments if c['id']==5775985191)
original={r['id']:r for r in [json.loads(line) for line in body.splitlines() if line.startswith('{"id":')]}
# Exact new public bytes, never a claim of historical archive identity.
for r in rows:assert r['page']==original[r['id']]['page']
extra=json.loads((OUT/'block-marker-inputs.json').read_text())
def render(row):
 req={'text':row['page'],'mode':'gfm','context':'kebag-logic/milan-fpga'}
 p=subprocess.run(['rtk','proxy','gh','api','markdown','--input','-'],input=json.dumps(req),capture_output=True,text=True);assert p.returncode==0,p.stderr
 hs=[html.unescape(re.sub('<[^>]+>','',s)) for s in re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>',p.stdout,re.S)]
 return {**row,'request':req,'html':p.stdout,'headings':hs,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with ThreadPoolExecutor(max_workers=3) as pool:rendered=list(pool.map(render,rows+extra))
(OUT/'published-replay-responses.json').write_text(json.dumps(rendered,indent=2))
for row in rendered:
 if row['id'] in original:assert row['headings']==original[row['id']]['github'],row
summary={'author_fixtures':len(rows),'same_new_published_inputs_and_heading_results':True,'original_historical_byte_or_row_identity':False,'block_marker_controls':[{k:r[k] for k in ['id','headings']} for r in rendered if r['id'] not in original]}
(OUT/'published-replay-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
