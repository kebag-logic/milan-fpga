from run_gate import OUT, run

sdk = run('builder-sdk', ['taskset', '-c', '16-31', 'python3', str(OUT/'builder-sdk.py')])
absent = run('builder-no-compiler', ['taskset', '-c', '16-31', 'python3', str(OUT/'builder-no-compiler.py')])
assert sdk == 0 and absent == 0, (sdk, absent)
