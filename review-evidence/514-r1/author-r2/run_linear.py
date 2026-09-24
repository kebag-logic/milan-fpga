"""Run the linear entry point through the existing self-test fixture harness."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import check_merge_containment as checker
import merge_containment_selftest as suite
from merge_containment_selftest_linear import linear_retention_cases

with patch.object(suite, "_fixture_cases", linear_retention_cases):
    raise SystemExit(checker.main(["check_merge_containment.py", "--selftest"]))
