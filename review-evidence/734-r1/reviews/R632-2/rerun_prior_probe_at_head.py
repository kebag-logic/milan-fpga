#!/usr/bin/env python3
"""[R632] round 2: run R632-1's unchanged probe_scope.py functions with HEAD
rebound to the round-2 head (the probe hard-codes the round-1 head).
Usage: rerun_prior_probe_at_head.py <probe_scope.py> <repo> <workdir> <head>"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("probe_scope", sys.argv[1])
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mod.HEAD = sys.argv[4]
sys.argv = [sys.argv[1], sys.argv[2], sys.argv[3]]
sys.exit(mod.main())
