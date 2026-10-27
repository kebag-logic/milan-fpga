"""Shared loader for the R699-6 probes: import a torture_campaign.py by path and
build the self-test's TestCase so its private sweep helpers can be called."""
import importlib.util
import sys
import unittest


def load(path):
    spec = importlib.util.spec_from_file_location("torture_campaign_probe", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def case(mod):
    class T(mod._ReleaseGateChecks, unittest.TestCase):
        def runTest(self):
            pass
    t = T()
    t.maxDiff = None
    return t
