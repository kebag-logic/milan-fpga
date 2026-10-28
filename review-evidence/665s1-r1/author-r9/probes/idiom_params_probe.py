"""The Python idiom gate's own scan (scripts/check_py_idiom.py scan) on the harness's split_soc.py and build.py at
each named revision, from git: its "too many parameters" count and sites per file. Run from the checkout.
usage: idiom_params_probe.py REV...
"""
import subprocess
import sys
sys.path.insert(0, 'scripts')
import check_py_idiom as gate

for rev in sys.argv[1:]:
    for rel in ('tb/verilator/ctrl_service_budget/split_soc.py', 'tb/verilator/ctrl_service_budget/build.py'):
        text = subprocess.run(['git', 'show', f'{rev}:{rel}'], capture_output=True, text=True, check=True).stdout
        counts, sites = gate.scan(text, rel)
        hits = [s for s in sites.get('too many parameters', [])] if isinstance(sites, dict) else sites
        print(f'{rev} {rel}: too many parameters={counts.get("too many parameters", 0)} {hits}')
print(f'MAX_PARAMETERS={gate.MAX_PARAMETERS}; budget: too many parameters={gate.read_budget().get("too many parameters")}')
