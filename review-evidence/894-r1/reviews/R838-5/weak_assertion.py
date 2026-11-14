#!/usr/bin/env python3
"""Show the new campaign row escapes with the previous assertion; no checkout writes."""
from pathlib import Path
import contextlib
import io
import json
import shutil
import sys

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
sys.path.insert(0, str(repo/'sw/firmware/ctrl/test'))
import aecp_mutants as campaign

scratch = packet/'scratch/weak-assertion'
src = scratch/'source/ctrl'
shutil.copytree(repo/'sw/firmware/ctrl', src, dirs_exist_ok=True)
shutil.copytree(repo/'sw/firmware/ctrl_nvm', src.parent/'ctrl_nvm', dirs_exist_ok=True)
p = src/'aecp/aecp_maps.c'
text = p.read_text()
new = ('_Static_assert(sizeof ((struct edit *)0)->slot / sizeof ((struct edit *)0)->slot[0] >= (size_t)MAP_DOMAIN,\n'
       '\t       "the table holds every position place() forms");')
old = ('_Static_assert(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS <= MAP_SLOTS &&\n'
       '\t       AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS <= MAP_SLOTS,\n'
       '\t       "the table holds every key of the port\'s domain");')
assert text.count(new) == 1
p.write_text(text.replace(new, old))
campaign.controls()
rows = [i for i,d in enumerate(campaign.DEFECTS) if d.name=='map-table-each-direction-alone']
assert len(rows)==1
campaign.CTRL=src
stream=io.StringIO()
with contextlib.redirect_stdout(stream):
    escaped=campaign.campaign(scratch/'run', jobs=8, shard=(rows[0],len(campaign.DEFECTS)))
log=stream.getvalue()
raw=(scratch/'run/map-table-each-direction-alone.log').read_text()
clean=lambda s:s.replace(str(repo),'<checkout>').replace(str(packet),'<packet>')
(packet/'weak-assertion.log').write_text(clean(log+raw))
assert escaped and '[ESCAPED]' in log and '[  PASSED  ] 0 tests.' in raw
(packet/'weak-assertion.json').write_text(json.dumps({'campaign_return':int(escaped),'expected_return':1,
    'plant':'map-table-each-direction-alone','prior_assertion_restored':True,'tests_run':0,'pass':True},indent=2)+'\n')
print('PASS: prior assertion allows the undersized table; new campaign row escapes with zero tests.')
