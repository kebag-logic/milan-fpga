"""Scratch probes of the ADP model-count check: header-side plants, fail-closed parsing, an unheld path, old vs new."""
import importlib.util, json, sys
from dataclasses import replace
from pathlib import Path

root, old_file = Path(sys.argv[1]), Path(sys.argv[2])
harness = root / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(harness))
import model_counts as new, scenario  # noqa: E402

spec = importlib.util.spec_from_file_location('old_counts', old_file)
old = importlib.util.module_from_spec(spec)
sys.argv = [str(harness / 'x')]
old.__file__ = str(harness / 'model_counts.py')
src = old_file.read_text().replace("Path(__file__)", f"Path({str(harness / 'model_counts.py')!r})")
exec(compile(src, str(old_file), 'exec'), old.__dict__)

text = new.HEADER.read_text()
base = json.loads(new.ORACLE.read_text())['point']
rc = 0
def verdict(name, n, want):
    global rc
    ok = (n > 0) == want
    rc |= not ok
    print(f'  {name}: {n} finding(s) -> {"DETECTED" if n else "MISSED"} ({"as required" if ok else "WRONG"})')

for interfaces in (1, 2):
    p = scenario.Point(**dict(base, interfaces=interfaces))
    print(f'{interfaces} interface(s)')
    counts = new.bounds(text)
    for path, short in (('adp.link_down', 8), ('adp.shutdown', 28), ('adp.link_up', 11)):
        verdict(f'new check, {path} planted {short}', len(new.findings(new.stale(new.groups_at(p), path, short), counts)), True)
        og = [*scenario.adp_groups(p), *scenario.control_groups(p), *scenario.fixture_groups(p)]
        for g in og:
            g.probes = [replace(pr, accesses=short) if new.path_of(pr) == path else pr for pr in g.probes]
        verdict(f'old check (701a980b), {path} planted {short}', len(old.findings(og, old.bounds(text))), path == 'adp.link_up')
    for macro, value in (('SHUTDOWN 29u', 'SHUTDOWN 30u'), ('LINK 12u', 'LINK 11u'), ('DELAY 39u', 'DELAY 40u')):
        verdict(f'new check, header {value}', len(new.findings(new.groups_at(p), new.bounds(text.replace(macro, value)))), True)
    verdict('new check, header "(down, a stop: 10)"',
            len(new.findings(new.groups_at(p), new.bounds(text.replace('a stop: 9)', 'a stop: 10)')))), True)
    try:
        new.findings(new.groups_at(p), new.bounds(text.replace('(down, a stop: 9)', '')))
        print('  new check, header without the LINK_DOWN count: passed (WRONG)'); rc = 1
    except KeyError as e:
        print(f'  new check, header without the LINK_DOWN count: raises KeyError {e} (fails closed, as required)')
    groups = new.groups_at(p)
    groups[0].probes = groups[0].probes + [scenario.Probe('adp.new_path.if0', 'NEW', 'adp', 'pad:LINK:0', ['arm:0'], accesses=5)]
    verdict('new check, an ADP probe with a count on an unheld path', len(new.findings(groups, counts)), True)
    verdict('new check, the real scenario', len(new.findings(new.groups_at(p), counts)), False)
sys.exit(rc)
