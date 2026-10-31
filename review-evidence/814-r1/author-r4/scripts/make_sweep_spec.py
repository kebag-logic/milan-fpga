"""make_sweep_spec.py <head> <out.json>: the full default sweep for native-shards.py, the #803 and #806 lanes' command
with this lane's scratch paths (pinned Verilator 5.050, sv2v v0.0.12, tsn-gen at rtl.yml's TSN_GEN_REV)."""
import json
import sys

head, out = sys.argv[1:3]
spec = dict(cwd='$LANES/814-soc-timing-cut', head=head, base='1e80128f0a467b58bf884b7d9bf62e013a2fb141',
            commands=[[
    'env',
    'PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$WORKSPACE_HOME/.local/bin:'
    '/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
    'VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',
    'TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen',
    'TMPDIR=$VALIDATION_STORAGE/scratch/814-a703d/tmp-sweep',
    'bash', 'scripts/run_all_suites.sh', '$VALIDATION_STORAGE/scratch/814-a703d/sweep-unused/logs', '--wait']])
open(out, 'w').write(json.dumps(spec, indent=1) + '\n')
