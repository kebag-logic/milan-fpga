"""Usage: python3 compare.py <repository> <base-report-dir> <head-report-dir>."""
from pathlib import Path
import importlib.util, json, sys, hashlib, re
sys.dont_write_bytecode=True
root=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('rank',root/'syn/ooc/pp_baseline_rank.py')
rank=importlib.util.module_from_spec(spec); spec.loader.exec_module(rank)
base=Path(sys.argv[2])
head=Path(sys.argv[3])
old=rank.hierarchy(base/'baseline_hierarchy.rpt')
new=rank.hierarchy(head/'baseline_hierarchy.rpt')
keys=['alinx_ax7101','alinx_ax7101/milan_datapath/@own','alinx_ax7101/milan_datapath/chan_map_capture']
rows={k:{'base':old[k],'head':new[k],'delta':{c:new[k][c]-old[k][c] for c in rank.FIELDS}} for k in keys}
def cells(path):
    return dict(line.split('\t',1) for line in path.read_text().splitlines()[1:])
old_cells=cells(base/'baseline_cells.tsv'); new_cells=cells(head/'baseline_cells.tsv')
cap='milan_datapath/chan_map_capture/'
off={k for k,v in old_cells.items() if k.startswith(cap) and v.startswith('FD')}
nff={k for k,v in new_cells.items() if k.startswith(cap) and v.startswith('FD')}
settle=(head/'candidate_settle_cells.tsv').read_text().splitlines()
cone=(head/'candidate_settle_cone.tsv').read_text().splitlines()
result={'scopes':rows,'settle_FF':len(settle),'settle_full_LUT_cone':len(cone),'capture_added_FF':sorted(nff-off),'capture_removed_FF':sorted(off-nff)}
result['own_FF_delta']=len(settle)+len(nff)-len(off)
result['own_LUT_conservative_bound']=len(cone)+rows[keys[-1]]['delta']['LUT']
result['two_changed_scopes_delta']={c:rows[keys[1]]['delta'][c]+rows[keys[2]]['delta'][c] for c in rank.FIELDS}
(head/'candidate_area_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
for name,values in [('capture_added_FF',nff-off),('capture_removed_FF',off-nff)]:
    (head/(name+'.txt')).write_text('\n'.join(sorted(values))+'\n')
lines=['scope\tbase_LUT\thead_LUT\tdelta_LUT\tbase_FF\thead_FF\tdelta_FF']
for k in sorted(old.keys()&new.keys()):
    if k.count('/')==1 or (k.startswith('alinx_ax7101/milan_datapath/') and k.count('/')==2):
        lines.append('\t'.join(map(str,[k,old[k]['LUT'],new[k]['LUT'],new[k]['LUT']-old[k]['LUT'],old[k]['FF'],new[k]['FF'],new[k]['FF']-old[k]['FF']])))
(head/'candidate_hierarchy_delta.tsv').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('capture_added_FF','capture_removed_FF')},indent=2))

# Exclude unchanged LUT functions and count the complete changed capture
# hierarchy separately, so shared pre-existing cones cannot inflate ownership.
def logic(path):
    return {row.split("\t",1)[0]: row for row in path.read_text().splitlines()}
def signature(row):
    name, kind, init, terms = row.split("\t")
    pins = dict(re.findall(r"(I[0-9]+)=(.*?)(?=[ ;]I[0-9]+=|$)", terms))
    assert len(pins) == int(kind[3]) if kind[3].isdigit() else False, row
    ordered = sorted(pins, key=lambda k: int(k[1:]))
    drivers = [pins[k] for k in ordered]
    keys = sorted(set(drivers))
    bits = int(init.split("'h",1)[1],16)
    def truth(n):
        result=[]
        for assignment in range(1 << len(keys)):
            address=sum(((assignment >> keys.index(drivers[i])) & 1) << i for i in range(n))
            result.append((bits >> address) & 1)
        return tuple(result)
    # LUT6_2 has O5 as well as O6; preserve both output functions.
    return kind, tuple(keys), truth(len(drivers)), truth(5) if kind == 'LUT6_2' else ()
base_logic=logic(head/'base_lut_logic.tsv')
head_cone=logic(head/'candidate_settle_cone.tsv')
owned={k:v for k,v in head_cone.items() if not k.startswith(cap)}
unchanged={k for k,v in owned.items() if k in base_logic and signature(v)==signature(base_logic[k])}
remaining={k:v for k,v in owned.items() if k not in unchanged}
(head/'candidate_attributable_LUT_cone.tsv').write_text('\n'.join(remaining[k] for k in sorted(remaining))+'\n')
(head/'candidate_unchanged_LUT_cone.tsv').write_text('\n'.join(owned[k] for k in sorted(unchanged))+'\n')
result['ownership']={'full_cone_LUT':len(head_cone),'capture_cone_LUT_counted_in_module_delta':len(head_cone)-len(owned),'identical_base_functions':len(unchanged),'remaining_cone_LUT_upper_bound':len(remaining),'capture_LUT_delta':rows[keys[-1]]['delta']['LUT'],'own_LUT_upper_bound':len(remaining)+rows[keys[-1]]['delta']['LUT'],'own_FF_delta':result['own_FF_delta']}
(head/'candidate_area_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print('Ownership refinement:',json.dumps(result['ownership'],indent=2))

proof_path=head/'shared_logic_equivalence.json'
if proof_path.exists():
    proof=json.loads(proof_path.read_text())
    verified={r['cell'] for r in proof['cells'] if r['identical'] and r['assignments']==65536 and r['base_sha256']==r['head_sha256']}
    assert proof['negative_control']['caught']
    shared=verified & remaining.keys()
    final={k:v for k,v in remaining.items() if k not in shared}
    result['ownership']['shared_band_functions_proved_identical']=len(shared)
    result['ownership']['final_remaining_cone_LUT_upper_bound']=len(final)
    result['ownership']['final_own_LUT_upper_bound']=len(final)+rows[keys[-1]]['delta']['LUT']
    (head/'candidate_owned_LUT_upper_bound.tsv').write_text('\n'.join(final[k] for k in sorted(final))+'\n')
    (head/'candidate_shared_band_LUT.tsv').write_text('\n'.join(remaining[k] for k in sorted(shared))+'\n')
    (head/'candidate_area_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Final ownership bound:',json.dumps(result['ownership'],indent=2))
