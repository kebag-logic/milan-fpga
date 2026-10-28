"""make_sweep_spec.py <head> <out.json>: the full default sweep for native-shards.py, the #780 spec's command with
this lane's scratch paths (pinned Verilator 5.050, sv2v v0.0.12, tsn-gen)."""
import json
import sys

head, out = sys.argv[1:3]
spec = dict(cwd='$LANES/799-adopt6', head=head, base='97aab1d0f28bd753a3e11df6278d5cac54f964dd', commands=[[
    'env',
    'PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$WORKSPACE_HOME/.local/bin:'
    '/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
    'VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',
    'TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen',
    'TMPDIR=$VALIDATION_STORAGE/scratch/799-a692/tmp-sweep',
    'bash', 'scripts/run_all_suites.sh', '$VALIDATION_STORAGE/scratch/799-a692/sweep-unused/logs', '--wait']])
open(out, 'w').write(json.dumps(spec, indent=1) + '\n')
