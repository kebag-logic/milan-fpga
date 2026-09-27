#!/usr/bin/env python3
"""Use the internal review witnesses with the equivalent round-3 anchors."""
import runpy
import sys
import tempfile
from pathlib import Path
from review_reanchors import INTERNAL, ROOT, load, retarget

mutations = load(INTERNAL / 'r362_2_mutants.py', 'r362_2_mutants')
mutations.MUTANTS = [(mid, name, *retarget('internal-' + mid, old, new))
                     for mid, name, old, new in mutations.MUTANTS]
source = (INTERNAL / 'r362_2_survivor_witness.py').read_text()
source = source.replace('observation_resolution_s must be less than min(0.25 s, 0.5 s); ',
                        'require 2 * R < 0.25 s so an instant clear fails; ')
with tempfile.TemporaryDirectory(prefix='593-round3-witness-') as temp:
    script = Path(temp) / 'witness.py'
    script.write_text(source)
    sys.argv = [str(script), str(ROOT), str(Path(temp) / 'mutants')]
    runpy.run_path(str(script), run_name='__main__')
