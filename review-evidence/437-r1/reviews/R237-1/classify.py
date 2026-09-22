import json,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1]);import gen_toc as toc
rows=json.loads(Path(sys.argv[2]).read_text());out={}
for row in rows:
 p=row['page'];name=row['id'];out[name]={'blocks':toc.blocks(p),'line_kinds':toc.line_kinds(p),'headings':toc.headings(p),'generated_block':toc.generated_block(p,row.get('path','page.md')),'refusals':toc.refusals(p)}
Path(sys.argv[3]).write_text(json.dumps(out,indent=2))
