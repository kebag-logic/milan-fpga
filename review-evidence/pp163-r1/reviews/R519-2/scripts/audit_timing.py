#!/usr/bin/env python3
"""Check the published numeric summaries and available source identities.
This deliberately reports incomplete full input lineage; it does not claim a rerun.
"""
import json, pathlib, subprocess, sys
src=pathlib.Path(sys.argv[1]).resolve();p=pathlib.Path(sys.argv[2]).resolve();e=p/'receipts/public-author-r3/evidence'
head=json.loads((e/'measurement-m3final.json').read_text());base=json.loads((e/'measurement-m3base.json').read_text());identity=json.loads((e/'rtl-scope-m3final.json').read_text())
for key,path in [('arbiter_blob','hdl/packet_engine/KL_pp_tx_arbiter.sv'),('notify_blob','hdl/aecp/KL_aecp_notify.sv')]:
 actual=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD:'+path],text=True).strip();assert actual==identity[key]
for row in [base,head]:
 hist={int(k):v for k,v in row['cone']['histogram'].items()}
 assert sum(hist.values())==row['cone']['pairs'];assert max(hist)==row['cone']['max_levels']
 assert sum(v for k,v in hist.items() if k>20)==row['cone']['above_20']
assert head['timing']['setup']['worst_slack_ns']==3.337
assert head['cone']['max_levels']==16 and head['cone']['above_20']==0
ref=json.loads((e/'resource-reference-m3.json').read_text())
print(json.dumps({'summary_consistent':True,'two_RTL_blobs_match':True,'published_baseline_inputs_sha256':ref['fresh_record']['inputs_sha256'],'candidate_inputs_sha256_published':False,'full_input_lineage_verified':False,'reason':'Final recipe, source/image inventory and bound parameters are absent from the public round-3 archive. Baseline aggregate digest cannot authenticate final inputs.'},indent=2))
raise SystemExit(2)
