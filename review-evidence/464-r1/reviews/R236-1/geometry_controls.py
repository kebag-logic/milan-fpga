import sys,json,copy,contextlib,io
from pathlib import Path
root=Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'avdecc'))
import gen_aem_store as g
import aem_maps as maps
results=[]
def check(name,condition,detail=None):
 assert condition,(name,detail)
 results.append({'name':name,'result':'PASS','detail':detail})
f=g._map_fixture();m=g.build_model(f)
check('explicit geometry',len(f['audio_maps'])==2 and len(f['stream_inputs'])==2 and len(f['stream_outputs'])==1 and f['ports_in']==[dict(clusters=8,base_cluster=0,maps=1,base_map=0)] and f['ports_out']==[dict(clusters=8,base_cluster=8,maps=1,base_map=1)])
check('fixture table geometry',m['SMAP']['IN_ROWS']==[8] and m['SMAP']['OUT_ROWS']==[8],m['SMAP'])
fresh=g._map_fixture();f['audio_maps'][0][0][0]=99;f['stream_inputs'][0]['formats'].clear()
check('nested fixture isolation',fresh==g._map_fixture())
d=g.build_model(g.builtin_spec())['SMAP']['DEVIATIONS']
expected={"STREAM_PORT_OUTPUT[0] AUDIO_MAP[0] mapping (0,%d,%d,0): stream_channel %d >= 2, the widest channels_per_frame stream 0 advertises (['0x205022000806000']) - 7.2.6 / IEEE 1722-2016 7.3.1"%(c,c,c) for c in range(2,8)}
check('six exact deployed deviations',set(d)==expected==set(g.KNOWN_MAP_DEVIATIONS),sorted(d))
for n in [0,1,62,63]:
 s=g._map_fixture();s['audio_maps'][1]=[[0,c,c%8,0] for c in range(n)]
 try: mm=g.build_model(s)
 except ValueError as e: check('row-count boundary '+str(n),n==63 and 'has 63 mappings' in str(e),str(e))
 else: check('row-count boundary '+str(n),n<=62,{'deviations':len(mm['SMAP']['DEVIATIONS'])})
s=g._map_fixture();s['audio_maps'][1]=[[0,c,c%8,0] for c in range(63)]
saved=maps.SMAP_MAX_ROWS;maps.SMAP_MAX_ROWS=63
mm=g.build_model(s);maps.SMAP_MAX_ROWS=saved
check('63-vector no second refusal',len(mm['SMAP']['DEVIATIONS'])==61,{'recorded_deviations':len(mm['SMAP']['DEVIATIONS'])})
s=g._map_fixture();s['audio_maps'][0]=[[0,0,0,0],[0,0,1,0]]
g.build_model(s);check('input fan-out permitted',True)
s=g._map_fixture();s['audio_maps'][1]=[[0,0,0,0],[0,1,0,0]]
g.build_model(s);check('output shared cluster permitted',True)
s=g._map_fixture();s['ports_out'].append(dict(clusters=8,base_cluster=16,maps=1,base_map=2));s['audio_maps'].append([[0,0,0,0]])
try:g.build_model(s)
except ValueError as e:check('duplicate output across ports refused','across the entire Configuration' in str(e),str(e))
else:raise AssertionError('accepted duplicate output across ports')
# Test the repair mechanisms themselves, with restored functions afterward.
def test_failure(name,patch,restore,expected):
 patch();b=io.StringIO()
 try:
  with contextlib.redirect_stdout(b):result=g.self_test()
 finally:restore()
 check(name,result==1 and expected in b.getvalue(),b.getvalue())
orig=maps._static_map_of
def fixture_only(port,tag,rows):
 if tag.startswith('STREAM_PORT_INPUT'):raise ValueError('R236 planted fixture-only refusal')
 return orig(port,tag,rows)
test_failure('fixture positive is load-bearing',lambda:setattr(maps,'_static_map_of',fixture_only),lambda:setattr(maps,'_static_map_of',orig),'[FAIL] the two-map fixture')
shared=g._map_fixture();origfixture=g._map_fixture
test_failure('fresh fixture is load-bearing',lambda:setattr(g,'_map_fixture',lambda:shared),lambda:setattr(g,'_map_fixture',origfixture),'refused, but not for')
Path(__file__).with_name('geometry-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS',len(results),'geometry and independent boundary controls')
