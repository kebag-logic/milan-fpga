"""Read-only #872 model at the two measured points, using this lane's full raw measurements.
Same load_grade.load equation and opt_model2 derivations; no product table is edited.
"""
from pathlib import Path
import json,re,sys,math
T=Path('<scratch>');tree=sys.argv[1];C=T/'clones'/tree;D=Path(sys.argv[2]);records=Path(sys.argv[3]);out=Path(sys.argv[4])
sys.path.insert(0,str(C/'tb/verilator/ctrl_service_budget'));import load_grade as lg
near=dict(lg.NEAREST);lg.NEAREST={}
text=records.read_text();result={}
for label,point in [('1x1','1x1/1if'),('8x8-1if','8x8/1if')]:
 d=D/label;costs=dict(json.loads((d/'costs.json').read_text())['_most_cycles']);kinds=json.loads((d/'aecp.json').read_text())
 matches=re.findall(re.escape(point)+r' (?:held|reported) other: the dearest ([0-9,]+) CPU cycles',text);assert matches
 costs['record.aecp']=max(int(n.replace(',','')) for n in matches)
 costs['item.aecp.notice']=kinds.get('notice',{}).get('most_cycles',0)
 costs['item.aecp.response']=kinds.get('response',{}).get('most_cycles',0)
 costs['item.aecp.probe']=kinds.get('probe',{}).get('most_cycles',costs['item.aecp.response'])
 costs['item.retained']=costs['record.srp'];costs['item.mrpdu']=costs['build_one']
 if not costs.get('build'):costs['build']=round(costs['build_one']*1795/1475)
 us={k:lg.rule_us(v) for k,v in costs.items() if v}
 fallback=lg.GRADED.get(point) or lg.GRADED[near[point]]
 for k,v in fallback.items():us.setdefault(k,v)
 tables={**lg.GRADED,point:us};terms=lg.load(C,point,tables)
 result[point]={'total':sum(terms.values()),'terms':terms,'cycles':costs,'stated_us_for_analysis':us,'pass_own_us':us['base']+us['events_none'],'owner_bound':0.70 if label=='1x1' else 0.75}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=1)+'\n')
for p,r in result.items():print(p,format(r['total'],'.9f'),'bound',r['owner_bound'])
