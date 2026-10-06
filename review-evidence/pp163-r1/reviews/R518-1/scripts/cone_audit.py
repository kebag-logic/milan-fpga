#!/usr/bin/env python3
import argparse,json,pathlib,re
ap=argparse.ArgumentParser();ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();p=a.packet.resolve();e=p/'receipts/public-evidence/author/evidence';out={}
for shape in ['base','head']:
 rows=[l.split('\t') for l in (e/f'arbiter-standalone-levels-{shape}.tsv').read_text().splitlines()];ends={r[2].rsplit('/',1)[0] for r in rows};out[shape]={'standalone_endpoint_cells':len(ends),'standalone_endpoint_pins':len({r[2] for r in rows}),'standalone_sof_cells':[x for x in sorted(ends) if 'sof_pend' in x]}
 s=(e/('cone-summary-head-all.txt' if shape=='head' else 'cone-summary-base-over20.txt')).read_text();out[shape].update(summary_header=s.splitlines()[0],covered_endpoint_families=sorted(set(re.findall(r'-> (.*?): \d+ paths',s))),grouped_paths=sum(map(int,re.findall(r'-> .*?: (\d+) paths',s))))
out['integrated_expected_sequential_bits']={'slot_r':3,'owner_r':3,'FSM_onehot_arb_st_r':3,'start_sent_r':1,'pace_nonsol_r':1,'gnt_r':8,'age_r':32,'cnt_r':128,'pend_r':8};out['integrated_expected_total']=sum(out['integrated_expected_sequential_bits'].values())
out['explanation']='The measured wrapper leaves tx_sof_o open at hdl/milan/KL_pp_shadow.sv:1182. sof_pend_r is present in standalone reports and is unused after integration. The nine retained families sum to 187 cells, matching the reported survey. Script and raw integrated per-pin tables are not in the published bundle; this audits consistency and family coverage, not the unseen query implementation.'
(p/'receipts/cone-audit.json').write_text(json.dumps(out,indent=2)+'\n');assert out['base']['grouped_paths']==146535;assert out['head']['grouped_paths']==17989;print('Cone summary arithmetic and endpoint family inventory consistent')
