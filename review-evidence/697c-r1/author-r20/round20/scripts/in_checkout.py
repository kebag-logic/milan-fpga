"""Run a command from its designated disposable checkout."""
import os
import sys
os.chdir(sys.argv[1])
os.execvp(sys.argv[2], sys.argv[2:])
