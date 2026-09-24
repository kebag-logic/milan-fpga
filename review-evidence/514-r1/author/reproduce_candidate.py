import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
checker = root / 'scripts/check_merge_containment.py'
sys.path.insert(0, str(checker.parent))
import check_merge_containment as mc
from merge_containment_selftest_content import _linear_rebase_cases
from merge_containment_selftest_scratch import quiet_git

rows = []
def record(name, branch, base):
    args = [sys.executable, '-B', str(checker), '--no-fetch', '--base', base, branch]
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    def oid(ref):
        return subprocess.check_output(['git', 'rev-parse', ref], text=True).strip()
    row = dict(name=name, branch_head=oid(branch), base_tip=oid(base),
               rc=result.returncode, stdout=result.stdout, stderr=result.stderr)
    rows.append(row)
    print(json.dumps(row, indent=2))
    assert result.returncode == 0 and 'contained' in result.stdout
    optional = subprocess.run([*args, '--current-retention'], capture_output=True, text=True, check=False)
    row['optional_rc'] = optional.returncode
    row['optional_stdout'] = optional.stdout
    assert optional.returncode == 1 and 'current retention: unproved on:' in optional.stdout
    print(optional.stdout, 'optional exit', optional.returncode)
    return result.returncode, result.stdout

with quiet_git(), tempfile.TemporaryDirectory(prefix='514-base-') as scratch:
    os.chdir(scratch)
    fixture = out / 'public/R242/scripts/fixtures.py'
    sys.argv = [str(fixture), str(checker), str(checker), scratch, str(out/'unused.json')]
    spec = importlib.util.spec_from_file_location('published_fixtures', fixture)
    published = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(published)
    Path('fixture30').mkdir()
    os.chdir('fixture30')
    published.s_linear_revert_control()
    record('fixture30', 'pr', 'main')
    original = json.loads((out/'public/R242/rawlogs/fixture-matrix.json').read_text())
    receipt = next(r for r in original['rows'] if r['scenario']=='linear-control-exact-revert')
    assert (rows[-1]['branch_head'], rows[-1]['base_tip']) == (receipt['branch_head'], receipt['base_tip'])
    os.chdir(scratch)
    Path('linear-fallback').mkdir()
    os.chdir('linear-fallback')
    os.environ.update(GIT_AUTHOR_DATE='@1790000000 +0000', GIT_COMMITTER_DATE='@1790000000 +0000')
    for args in [('init','-q','-b','base'), ('config','user.name','s'), ('config','user.email','s@s')]:
        subprocess.run(['git',*args],check=True)
    Path('f').write_text('1')
    subprocess.run(['git','add','f'],check=True)
    subprocess.run(['git','commit','-qm','c0'],check=True)
    def run(args):
        return record('linear-patch-fallback', 'linear-feature', 'linear-base')
    def case(name, got, want, why):
        assert got == want, (name,got,want)
    _linear_rebase_cases(SimpleNamespace(mc=mc,run=run,case=case))
(out/'logs/candidate-reproduction.json').write_text(json.dumps(rows,indent=2)+'\n')
