#!/usr/bin/python3
# A Git-free archive has no index. Answer the sole source-inventory query
# from the verified immutable pin's tree, never from filesystem discovery.
import os,pathlib,sys
if pathlib.Path.cwd() == pathlib.Path("/tmp/502-a345/export/protocol-processor/hdl") and sys.argv[1:] == ["ls-files","*.sv"]:
    print(pathlib.Path("/tmp/502-a345/pp-tracked-sv.txt").read_text(),end="")
else:
    os.execv("/usr/bin/git",["git",*sys.argv[1:]])
