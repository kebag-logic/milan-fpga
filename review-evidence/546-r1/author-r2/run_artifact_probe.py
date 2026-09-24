import subprocess
from pathlib import Path

root = Path.cwd()
scratch = Path('/tmp/546-a271-review-4gbqea6u')
cpp = scratch / 'review-evidence/546-r1/reviews/R303-1/probes/probe_artifact.cpp'
mdir = scratch / 'artifact-build'
cmd = ['$VALIDATION_TOOLS/verilator-v5.050/bin/verilator', '--cc', '--exe', '--build', '-j', '4', '--public-flat-rw', '--top-module', 'KL_crf_rx', '-Mdir', str(mdir), '-GCLK_FREQ_HZ_P=200000', '-GIVAL_CYC_P=200', '-Wall', '-Wno-fatal', '-Wno-UNUSEDSIGNAL', '-Wno-UNUSEDPARAM', '-Wno-PINMISSING', '-Wno-WIDTHEXPAND', '-Wno-WIDTHTRUNC', '-CFLAGS', '-std=c++17 -O2', str(root / 'hdl/ieee1722/crf/KL_crf_rx.sv'), str(cpp), '-o', 'Vartifact']
subprocess.run(cmd, check=True, timeout=1200)
subprocess.run([str(mdir / 'Vartifact')], check=True, timeout=1200)
