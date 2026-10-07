#!/usr/bin/env python3
"""Record the source identities and stage/selection facts for this focused re-review."""
import argparse,json,subprocess
from pathlib import Path
def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--output',type=Path,required=True);o=a.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(o.repo),*args])
    head=git('rev-parse','HEAD').decode().strip();assert head=='c4539ff107a6a4c7d2e4a4844182b00a2bf33c82'
    rows={}
    for key,rev,path in [('notify_equals_main','c9f74b68','hdl/aecp/KL_aecp_notify.sv'),('arbiter_equals_previous_review','cd9825c9','hdl/packet_engine/KL_pp_tx_arbiter.sv')]:
        rows[key]={'equal':(o.repo/path).read_bytes()==git('show',f'{rev}:{path}'),'path':path,'reference':rev,'head_blob':git('rev-parse',f'{head}:{path}').decode().strip()};assert rows[key]['equal']
    top=(o.repo/'hdl/top/protocol_processor_top.sv').read_text();arb=(o.repo/'hdl/packet_engine/KL_pp_tx_arbiter.sv').read_text();wd=(o.repo/'tb/pp_top/notify_phases.hpp').read_text();cx=(o.repo/'tb/aecp_notify/sim_main.cpp').read_text()
    checks={'reset_mask_to_zero':"if (!rst_n) org_withdraw_mask_r <= '0;" in top,'mask_registered':"else        org_withdraw_mask_r <= org_withdraw_slot_mask_w;" in top,'three_mask_readers':top.count('org_withdraw_mask_r[')==3,'lowest_index_tie':('(j < i) && elig_w[j] && (key_w[j] <= key_w[i])' in arb and '(j > i) && elig_w[j] && (key_w[j] < key_w[i])' in arb),'withdraw_both_races':all(f'WD{i}:' in wd for i in [1,2,3]),'immediate_cancel_and_no_later':'probing && own && later == 0' in cx,'release_also_feeds_abort':'assign arb_start_abort_w = org_withdraw_mask_r[ser_slot_w]\n                           || (txs_release_valid_w' in top}
    assert all(checks.values());rows.update(scoped_checks=checks,head=head,fresh_simulation_executed=False,scope='same-head F1 evidence re-review; source behavior inspected, round-2 executed conclusions carried forward')
    o.output.write_text(json.dumps(rows,indent=2)+'\n');print('PASS: source identities and scoped structural assertions');return 0
if __name__=='__main__':raise SystemExit(main())
