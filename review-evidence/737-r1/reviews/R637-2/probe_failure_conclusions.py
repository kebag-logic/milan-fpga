#!/usr/bin/env python3
"""Each removed terminal conclusion must be caught by the shipped selftest."""
import contextlib,io,pathlib,sys
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/"scripts"))
import ci_fail_fast as production
import ci_fail_fast_selftest as control
for missing in production.FAILURES:
 narrowed=tuple(value for value in production.FAILURES if value!=missing)
 with patch.object(production,"FAILURES",narrowed),contextlib.redirect_stdout(io.StringIO()):
  try:control.main()
  except AssertionError:pass
  else:raise AssertionError("control survives removal of "+missing)
 print("PASS: shipped selftest detects removal of",missing)
