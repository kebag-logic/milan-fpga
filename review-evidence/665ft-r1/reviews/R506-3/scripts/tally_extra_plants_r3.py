#!/usr/bin/env python3
"""R506-3 probe: listener defects the head's tally self-test does not itself
plant, graded with the head's own cases and campaign() code.
Usage: tally_extra_plants_r3.py <clone>"""
import sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_gtest, tally_selftest as t  # noqa: E402

D = t.Defect
EXTRA = (
    # the suite loop skips the last registered suite / the first
    D("suite-loop-drops-last", "if (suite->ad_hoc_test_result().Failed()) {",
      "if (k + 1 < unit.total_test_suite_count() && suite->ad_hoc_test_result().Failed()) {",
      ("TearDownFails.*",)),
    D("suite-loop-tail-only", "if (suite->ad_hoc_test_result().Failed()) {",
      "if (k + 2 >= unit.total_test_suite_count() && suite->ad_hoc_test_result().Failed()) {",
      ("SetUpFails.*",)),
    # only fatal failures outside a test counted
    D("program-fatal-only", "if (unit.ad_hoc_test_result().Failed()) {",
      "if (unit.ad_hoc_test_result().HasFatalFailure()) {", ("ProgramFails.*",)),
    # the handler prints nothing once a tally was printed, even between tests
    D("crash-reported-inverted", "    if (!state.reported) {\n        put(\"\\n\");",
      "    if (state.reported) {\n        put(\"\\n\");", ("Crash.Bus", "Crash.Fpe", "Crash.Ill")),
    # the handler swallows the signal (returns instead of re-raising)
    D("crash-no-reraise", "    static_cast<void>(std::raise(sig));\n}", "    std::_Exit(0);\n}",
      ("Crash.Bus", "Crash.Fpe", "Crash.Ill", "Crash.Segv", "Crash.Abort")),
    # the disabled-suite test reads the wrong field
    D("disabled-suite-by-test-only", "std::strncmp(suite->name(), \"DISABLED_\", 9) == 0 ||",
      "std::strncmp(info->name(), \"DISABLED_\", 9) == 0 ||", ("DISABLED_Suite.*",)),
)
t.DEFECTS = EXTRA
with tempfile.TemporaryDirectory(prefix="r506-3-tally.") as tmp:
    escaped = t.campaign(fw_gtest.Build(), Path(tmp))
print(f"extra plants escaped: {escaped}")
sys.exit(1 if escaped else 0)
