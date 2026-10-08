# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The R532-11 reviewer plants, judged only by the reviewer probe cases
(R11Feedback.*) in a copy whose test_acmp_mbx.cpp includes r532_11_probe.hpp."""
import dataclasses
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location("r532_11_plants", Path(__file__).with_name("r532_11_plants.py"))
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
PROBES = tuple(dataclasses.replace(d, test="R11Feedback.*") for d in _base.PROBES)
