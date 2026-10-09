#!/usr/bin/env python3
"""Audit literal ownership in the named test, including positive controls."""
import argparse,copy,json,pathlib,sys
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();sys.dont_write_bytecode=True;sys.path.insert(0,str(a.repo.resolve()/'scripts'))
from needle_audit import validate_needles,assertion_literals
from assertion_messages import inventory
plants=json.loads((a.repo/'tests/mutations.json').read_text());plant=next(x for x in plants if x['name']=='maap-stall-unqueued');rows=[]
for needle,refuse in [('is: 5',True),('5u',True),('r.frames.size()',True),('Which is: 5',True),('Expected equality',True),('equality of these values',True),('both owed frames and ANNOUNCE leave once room returns',False),('timer clock budget for state',True)]:
 target=copy.deepcopy(plant);target['kills'][0]['needle']=needle;errors=validate_needles([target]);rows.append({'test':target['kills'][0]['test'],'needle':needle,'expected_refusal':refuse,'errors':errors,'correct':bool(errors)==refuse})
source='void helper() { EXPECT_TRUE(false) << "helper identifier"; }\nTEST(Probe, Own) { const char *s="unused identifier"; EXPECT_STREQ("argument identifier",s); EXPECT_TRUE(false) << "own identifier"; helper(); }\nTEST(Probe, Other) { EXPECT_TRUE(false) << "other identifier"; }'
messages=inventory(source)
for needle,refuse in [('own identifier',False),('helper identifier',False),('unused identifier',True),('argument identifier',True),('other identifier',True)]:
 errors=validate_needles([{'name':'probe','kills':[{'test':'Probe.Own','needle':needle}]}],messages);rows.append({'test':'Probe.Own','needle':needle,'expected_refusal':refuse,'errors':errors,'correct':bool(errors)==refuse})
real=validate_needles(plants);result={'controls':rows,'real_errors':real,'kill_entries':sum(len(x['kills']) for x in plants),'test_inventories':len(assertion_literals())};a.output.write_text(json.dumps(result,indent=2)+'\n');print('controls',len(rows),'correct',sum(x['correct'] for x in rows),'real errors',len(real),'kill entries',result['kill_entries']);raise SystemExit(bool(real) or not all(x['correct'] for x in rows))
