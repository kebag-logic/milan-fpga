#!/usr/bin/env python3
"""Sequential small verification controls, all subprocesses awaited."""
import pathlib,subprocess,sys
repo=pathlib.Path(sys.argv[1]).resolve()
for args in (("sw/firmware/gtest/fw_coverage.py","--selftest"),("sw/firmware/gtest/tally_selftest.py","--mutants")):
    print("COMMAND",*args,flush=True)
    subprocess.run([sys.executable,*args],cwd=repo,check=True)
