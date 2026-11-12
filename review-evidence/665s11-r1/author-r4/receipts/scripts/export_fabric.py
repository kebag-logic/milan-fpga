#!/usr/bin/env python3
"""export_fabric.py CHECKOUT CONFIG OUT: the all-fabric shipping SoC's export (gateware sources, csr maps,
headers; no firmware, no synthesis) for one end-station config, through the builder's own argv."""
import contextlib, subprocess, sys
from pathlib import Path
root, config, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
sys.path.insert(0, str(root / 'sw/builder'))
import endstation_builder as eb  # noqa: E402
cfgp = root / 'configs' / f'endstation_{config}.yaml'
cfg = eb.load_config(str(cfgp))
with contextlib.redirect_stdout(None):
    eb.build(str(cfgp))
argv = eb.emit_soc_argv(cfg) + ['--entity-gen-dir', str(root / 'configs/generated' / cfg['name']),
                                '--no-compile-software', '--no-compile-gateware', '--output-dir', str(out)]
sys.exit(subprocess.run([sys.executable, '-B', str(root / 'sw/litex/milan_soc.py'), *argv], cwd=root / 'sw/litex').returncode)
