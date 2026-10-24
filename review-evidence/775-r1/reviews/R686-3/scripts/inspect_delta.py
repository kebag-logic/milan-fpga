#!/usr/bin/env python3
"""Check executable-source equality, mutation bytes and sweep accounting."""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
repo, packet, simulator = map(Path, sys.argv[1:4])
scratch = packet/'scratch'
path = 'hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv'
def git(*args):
    return subprocess.check_output(['git','-C',str(repo),*args])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
stripped, preprocessed = {}, {}
for rev in ['c2a080ae', '220b51f2']:
    p = scratch/(rev+'.sv')
    p.write_bytes(git('show',rev+':'+path))
    s = subprocess.check_output([sys.executable,str(packet/'scripts/strip_sv_comments.py'),str(p)])
    stripped[rev] = {'sha256':hashlib.sha256(s).hexdigest(), 'lines':len(s.splitlines())}
    data = subprocess.check_output([str(simulator),'-E','-P',str(p)])
    data = b'\n'.join(l.rstrip() for l in data.splitlines() if l.strip())+b'\n'
    preprocessed[rev] = {'sha256':hashlib.sha256(data).hexdigest(),'lines':len(data.splitlines())}
assert stripped['c2a080ae'] == stripped['220b51f2']
assert preprocessed['c2a080ae'] == preprocessed['220b51f2']
fm = load('format_mutants',repo/'tb/verilator/avtp_rxmon/format_mutants.py')
probe = load('probe_sq_claims',packet/'scripts/probe_sq_claims.py')
matches = {}
for name, rep, check in fm.BOTH_COPIES:
    if name.startswith('mr seed'):
        key = name.split(':')[0].replace(' ','_')
        expected = '            monst_r <= '+probe.MUTANTS[key].replace('%s','BUNDLE')
        matches[key] = rep == expected
assert all(matches.values())
sys.path.insert(0,str(repo/'scripts'))
import suite_tally
rows = []
for rc, fails in [(0,0),(1,3)]:
    raw = f'lockstep N=1: checks: 116 failures: {fails}\nlockstep N=8: checks: 119 failures: {fails}\n'
    shapes = ', '.join(f'N={n} {c}/{f}' for n,c,f in fm.LS_TALLY.findall(raw))
    line = f'    lockstep on the planted pair, as measured and not graded: rc {rc}, {shapes} (checks/failures)'
    scan = suite_tally.scan(line)
    failure = suite_tally.log_reports_failure(line)
    assert scan[:2] == (0,0) and not scan[2] and not scan[3] and not failure[1]
    rows.append({'line':line,'scan':scan,'failure_verdict':failure})
log = packet/'scratch/public/author-r3/receipts/round3/suites-220b51f2/avtp_rxmon.log'
scan = suite_tally.scan(log.read_text())
assert scan[:2] == (577,0) and not scan[3]
result = {'stripped':stripped,'preprocessed':preprocessed,'seed_mutations_byte_equal':matches,
          'mutant_tally_controls':rows,'published_suite_tally':scan,
          'delta_files':git('diff','--name-only','c2a080ae..HEAD').decode().splitlines(),
          'unchanged_reference_and_crf':not git('diff','c2a080ae..HEAD','--','tb/verilator/avtp_rxmon/reference','hdl/ieee1722/crf','tb/verilator/crf_rx'),
          'diff_check_rc':subprocess.run(['git','-C',str(repo),'diff','--check','a032c6d6..HEAD']).returncode}
(packet/'delta-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['published_suite_tally']},indent=2))
