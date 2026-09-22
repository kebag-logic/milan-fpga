import hashlib,json,runpy,sys
from pathlib import Path
scripts=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(scripts))
import gen_toc_closer_cases as closers
import gen_toc_cases as cases
fams={"walk":cases.walk_arms(),"tag":cases.tag_arms(),"guard":cases.guard_arms(),
"heading":cases.heading_arms(),"predecessor":cases.predecessor_arms(),
"provenance":cases.provenance_arms(),"refusal":cases.refusal_arms(),"I440":closers.closer_arms()}
rows=[{"family":f,"name":a[0],"fixture":a[1],"fixture_sha256":hashlib.sha256(repr(a[1]).encode()).hexdigest()} for f,aa in fams.items() for a in aa]
print(json.dumps({"toc_counts":{f:len(aa) for f,aa in fams.items()},"toc":rows,"label_rows":closers._label_rows()},indent=2,ensure_ascii=True))
