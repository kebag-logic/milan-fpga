#!/usr/bin/env python3
"""Prove retained bind resets and the new snapshot/rate regressions can fail."""
import argparse
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import sys

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('packet',type=Path);a=ap.parse_args()
    root=a.root.resolve();packet=a.packet.resolve();work=packet/'scratch/contracts';work.mkdir(parents=True,exist_ok=True)
    base=(root/'tb/tools/torture_campaign.py').read_text()
    variants=[('snapshot-old-guard','if total > frx:','if frx and total > frx:',
               ('test_unpublished_zero_receive_snapshot',)),
              ('xside-suppressed','return sem, [role for role in ticks if sem[role] == "interval"]','return sem, []',
               ('test_packet_agreement_attributes_interval_sides','test_concurrent_packet_law_attributes_each_direction'))]
    records=[]
    for name,old,new,omit in variants:
        assert base.count(old)==1
        source=work/(name+'.py');source.write_text(base.replace(old,new))
        tc=load(name.replace('-','_'),source)
        for escape in (False,True):
            if escape:
                for method in omit:
                    for cls in (tc._CounterLawChecks,tc._StreamingLicenceChecks):
                        if hasattr(cls,method):delattr(cls,method)
            out=io.StringIO()
            with contextlib.redirect_stderr(out):rc=tc.self_test()
            suffix='escape' if escape else 'detect'
            (packet/'receipts'/f'{name}-{suffix}.log').write_text(out.getvalue())
            assert rc==(0 if escape else 1),(name,escape,rc)
            records.append(dict(plant=name,omitted=escape,rc=rc))
    steps=load('review_counter_steps',root/'tests/steps/counters_contract_steps.py')
    src=steps._crf_rx_source();key='if (w_bind_rise_w) begin';at=src.index(key)
    clean=src[at:];end=clean.index('\n      end');body=clean[:end]
    checks=(steps.step_cc_crf_era_wipe,steps.step_cc_crf_era_edge,steps.step_cc_crf_era_lock)
    for check in checks:check(None)
    for symbol in (*steps.CRF_COUNTER_REG.values(),'iv_uf_r','iv_sm_r','iv_mr_r','iv_tu_r','iv_lt_r','iv_et_r'):
        pattern=rf'\b{symbol}\s*<=\s*(?:\x270|1\x27b0)\s*;'
        changed,n=re.subn(pattern,f'/* review plant: omit reset of {symbol} */',body);assert n==1,(symbol,n)
        planted=src[:at]+changed+clean[end:]
        steps._crf_rx_source=lambda s=planted:s
        try:steps.step_cc_crf_era_wipe(None)
        except AssertionError as exc:
            assert symbol in str(exc)
            print('DETECTED retained-reset',symbol,str(exc).splitlines()[-1])
        else:raise AssertionError('escaped retained reset '+symbol)
        # The unrelated era-edge and lock checks still pass when the wipe check is omitted.
        for check in checks[1:]:check(None)
        records.append(dict(plant='reset-'+symbol,detected=True,omission_escape=True))
    (packet/'receipts/contract-controls.json').write_text(json.dumps(records,indent=2)+'\n')
    print('PASS: snapshot and cross-device detection/omission; sixteen retained resets detected')

if __name__=='__main__':main()
