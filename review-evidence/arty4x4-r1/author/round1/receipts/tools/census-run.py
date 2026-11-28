"""Arty 4x4 measurement census: the eight image variants and every group the harness runs at arty-4x4, graded as
round 9's runner grades them. Measurement only: findings at the installed statements are recorded, not stopped on;
a native failure or a harness refusal stops the campaign. Resumable: a case is kept only with its trace hash.
usage: census-run.py <outdir>   (cwd = checkout root; env CENSUS_LEGS)"""
import concurrent.futures, hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path
root = Path.cwd(); scratch = Path(__file__).resolve().parents[1]; out = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import build, run, scenario, bind_save
POINT = 'arty-4x4'
UNRULED = {'flight_ms': 10**9, 'saves': 10**6}   # #1009 rules no Arty bind bound; figures recorded, no verdict
bind_save.FLIGHT_MS.setdefault(POINT, UNRULED['flight_ms']); bind_save.BURST_SAVES.setdefault(POINT, UNRULED['saves'])
if (out / 'stop-finding.json').exists(): raise SystemExit('refused: a finding ended the campaign')
out.mkdir(parents=True, exist_ok=True)
kept = json.loads((out / 'completed.json').read_text()) if (out / 'completed.json').exists() else []
kept = [r for r in kept if (out / r['variant'] / 'results' / (r['group'] + '.log')).exists() and hashlib.sha256(
    (out / r['variant'] / 'results' / (r['group'] + '.log')).read_bytes()).hexdigest() == r['trace_sha256']]
variants = ('none', 'answering-ports', 'answering-every-port', 'valid-destinations', 'declaring-outputs',
            'answering-later', 'talker-notices', 'shutdown-entry')
specs, groups, jobs = {}, {}, []
for variant in variants:
    d = out / variant
    try:
        spec = build.reused(d); print('REUSED', variant, flush=True)
    except Exception:
        print('BUILD', variant, flush=True)
        with (out / (variant + '-build.log')).open('w') as sink:
            subprocess.run([sys.executable, '-B', str(scratch / 'tools/build-variant.py'), str(d), variant], cwd=root,
                           stdout=sink, stderr=subprocess.STDOUT, check=True, timeout=10800)
        spec = build.reused(d)
    assert spec['cpu_hz'] == spec['sys_hz'] == 80_000_000
    specs[variant] = spec
    sel = run.all_groups(scenario.point(POINT, spec), spec)
    if variant == 'answering-ports':
        sel = [g for g in sel if g.name in ('aecp', 'aecp-fanout', 'aecp-largest-notice', 'aecp-reboot')]
    groups[variant] = sel
    (d / 'results').mkdir(exist_ok=True)
    done = {r['group'] for r in kept if r['variant'] == variant}
    jobs += [(variant, g) for g in sel if g.name not in done]
total = sum(map(len, groups.values()))
(out / 'manifest.json').write_text(json.dumps(dict(status='MEASUREMENT IN PROGRESS', point=POINT,
    groups={v: [g.name for g in gs] for v, gs in groups.items()},
    executables={v: s['executable_sha256'] for v, s in specs.items()}), indent=2) + '\n')
# Longest first, by round 9's own durations at arty-1x1 (scheduling only; no stimulus changes).
R9 = Path('$VALIDATION_STORAGE/artysplit-a829/r9/final-census/completed.json')
prior = {(r['variant'], r['group']): r['seconds'] for r in json.loads(R9.read_text())} if R9.exists() else {}
jobs.sort(key=lambda j: -prior.get((j[0], j[1].name), 3600))
print('KEPT', len(kept), 'TO RUN', len(jobs), 'OF', total, flush=True)
lock = threading.Lock(); stopped = threading.Event(); active = {}; records = list(kept)
def measured(job):
    variant, g = job
    with lock:
        if stopped.is_set() or (out / 'window-stop.json').exists(): return
        began = time.time(); d = out / variant; results = d / 'results'; spec = specs[variant]
        script = results / (g.name + '.txt'); script.write_text(g.script())
        log = results / (g.name + '.log')
        argv = [str(d / 'native/Vsim'), str(script), spec.get('flash_image') or '-']
        env = bind_save.environment(g.save, run.journal_of(results, g))
        sink = log.open('w')
        process = subprocess.Popen(argv, cwd=d / 'gateware', stdout=sink, stderr=subprocess.STDOUT, env=env)
        active[process.pid] = process
        print('START', variant, g.name, process.pid, flush=True)
    try: rc = process.wait(timeout=86400)
    except subprocess.TimeoutExpired:
        process.terminate(); process.wait(); rc = 124
    finally:
        sink.close()
        with lock: active.pop(process.pid, None)
    if stopped.is_set(): return
    (results / (g.name + '.status')).write_text(str(rc) + '\n')
    graded, refusals, misses = run.graded([g], [log], spec, results)
    shares = run.share_misses(graded)
    late = run.save_misses(graded) + run.burst_misses(graded) + run.notice_misses(graded, 1)
    for result in graded:
        joins = result['passes'].get('joins', {})
        late += [f"{g.name}: join interval {row['ms']} ms outside protocol range" for row in joins.get('over', [])]
        late += [run.run_out_miss(g.name, row) for row in joins.get('failing', [])]
        late += [run.leave_all_miss(g.name, row) for row in joins.get('leave_all', {}).get('failing', [])]
    over = [dict(p, group=g.name) for result in graded for p in result['probes'] if not p.get('within_budget', True)]
    record = dict(variant=variant, group=g.name, native_status=rc,
                  trace_sha256=hashlib.sha256(log.read_bytes()).hexdigest(), refusals=refusals, misses=misses,
                  share=shares, late=late, over_budget=over, stated=run.stated_misses(graded),
                  seconds=time.time() - began,
                  worst_pass_cycles=max([x['passes']['worst']['cycles'] for x in graded] or [0]))
    with lock:
        records.append(record)
        (out / 'completed.json').write_text(json.dumps(records, indent=2) + '\n')
        print('DONE', variant, g.name, rc, 'refusals', len(refusals), 'share', len(shares), 'late', len(late),
              'over', len(over), 'stated', len(record['stated']), round(record['seconds']), flush=True)
        if rc or refusals:
            stopped.set(); (out / 'stop-finding.json').write_text(json.dumps(record, indent=2) + '\n')
            for other in active.values(): other.terminate()
LEGS = int(os.environ.get('CENSUS_LEGS', '6'))
print('LEGS', LEGS, flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=LEGS) as pool:
    list(pool.map(measured, jobs))
if stopped.is_set(): raise SystemExit('measurement ended on a finding; inspect stop-finding.json')
if len(records) < total: print('WINDOW END', len(records), 'OF', total, flush=True); raise SystemExit(0)
for variant in variants: build.reused(out / variant)
print('NATIVE MEASUREMENTS COMPLETE', len(records), flush=True)
