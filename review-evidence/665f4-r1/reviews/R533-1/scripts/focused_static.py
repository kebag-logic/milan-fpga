#!/usr/bin/env python3
import subprocess,sys
for cmd in [['python3','sw/mailbox/gen_mailbox.py','--check'],['python3','sw/firmware/gtest/fw_rv32_selftest.py','--require-rv32']]:
 print('RUN',cmd,flush=True);subprocess.run(cmd,check=True)
